#!/usr/bin/env python3
"""Shared helpers for pb-review testability-oriented renderers."""

from __future__ import annotations

from pathlib import Path
from typing import Any


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"
TARGET_METRICS = {
    "M-01": 100.0,
    "M-02": 95.0,
    "M-03": 90.0,
    "M-04": 90.0,
    "M-05": 90.0,
    "M-06": 90.0,
    "M-07": 90.0,
}
SCORE_WEIGHTS = {
    "M-01": 0.25,
    "M-02": 0.10,
    "M-03": 0.20,
    "M-04": 0.15,
    "M-05": 0.10,
    "M-06": 0.10,
    "M-07": 0.10,
}


def as_dict(value: Any) -> dict[str, Any]:
    """Return a dict value or an empty dict."""

    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    """Return a list value or an empty list."""

    return value if isinstance(value, list) else []


def schema_path(file_name: str) -> Path:
    """Resolve a shared schema file by name."""

    return SCHEMA_DIR / file_name


def load_schema_text(file_name: str) -> str:
    """Read one shared schema file."""

    return schema_path(file_name).read_text(encoding="utf-8")


def extract_first_markdown_table(markdown_text: str) -> tuple[list[str], list[dict[str, str]]]:
    """Parse the first markdown table in a document."""

    lines = markdown_text.splitlines()
    table_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(stripped)
            continue
        if table_lines:
            break
    if len(table_lines) < 2:
        return [], []

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for row in table_lines[2:]:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return headers, rows


def load_schema_rows(file_name: str) -> list[dict[str, str]]:
    """Load the first table rows from a schema file."""

    _, rows = extract_first_markdown_table(load_schema_text(file_name))
    return rows


def grade_for_score(score: float) -> str:
    """Convert a numeric testability score to the grade band."""

    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def safe_percent(numerator: float, denominator: float) -> float:
    """Return a percentage, guarding against division by zero."""

    if denominator <= 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def average_metric(feature_specs: list[dict[str, Any]], key: str) -> float:
    """Average one numeric feature-level metric."""

    if not feature_specs:
        return 0.0
    total = 0.0
    for item in feature_specs:
        try:
            total += float(item.get(key, 0) or 0)
        except (TypeError, ValueError):
            total += 0.0
    return round(total / len(feature_specs), 2)


def summarize_status_counts(feature_specs: list[dict[str, Any]]) -> dict[str, int]:
    """Count testability_status values on feature specs."""

    counts = {"blocked": 0, "partial": 0, "test_ready": 0}
    for item in feature_specs:
        status = str(item.get("testability_status", "")).strip()
        if status in counts:
            counts[status] += 1
    return counts


def derive_test_traceability_rate(feature_specs: list[dict[str, Any]], traceability_matrix: dict[str, Any]) -> float:
    """Compute M-05 from traceability rows or feature-level fallbacks."""

    rows = as_list(as_dict(traceability_matrix).get("feature_test_rows"))
    if rows:
        covered = 0
        for item in rows:
            coverage_status = str(as_dict(item).get("coverage_status", "")).strip().lower()
            if coverage_status in {"covered", "partial"}:
                covered += 1
        return safe_percent(covered, len(rows))
    covered = sum(1 for item in feature_specs if float(item.get("test_case_group_count", 0) or 0) > 0)
    return safe_percent(covered, len(feature_specs))


def derive_rule_negative_rate(traceability_matrix: dict[str, Any]) -> float:
    """Compute M-06 from negative-test coverage rows."""

    rows = as_list(as_dict(traceability_matrix).get("rule_negative_test_rows"))
    if not rows:
        return 0.0
    covered = 0
    for item in rows:
        coverage_status = str(as_dict(item).get("coverage_status", "")).strip().lower()
        if coverage_status == "covered":
            covered += 1
    return safe_percent(covered, len(rows))


def derive_atomic_feature_rate(feature_specs: list[dict[str, Any]]) -> float:
    """Compute M-02 from explicit atomicity markers or single-entry-surface evidence."""

    if not feature_specs:
        return 0.0
    atomic_count = 0
    for item in feature_specs:
        if is_atomic_feature(item):
            atomic_count += 1
    return safe_percent(atomic_count, len(feature_specs))


def derive_feature_closure_rate(feature_specs: list[dict[str, Any]], gap_registry: list[dict[str, Any]] | None = None) -> float:
    """Compute M-01 from modeled features against modeled + missing-feature gaps."""

    modeled_count = count_modeled_features(feature_specs)
    missing_feature_count = count_missing_feature_gaps(gap_registry or [])
    denominator = modeled_count + missing_feature_count
    if denominator <= 0:
        return 0.0
    return safe_percent(modeled_count, denominator)


def derive_coverage_claim_rate(feature_specs: list[dict[str, Any]]) -> float:
    """Compute M-07 from feature-level coverage claim flags."""

    if not feature_specs:
        return 0.0
    allowed = 0
    for item in feature_specs:
        if str(item.get("coverage_claim_allowed", "")).strip().lower() == "yes":
            allowed += 1
    return safe_percent(allowed, len(feature_specs))


def count_modeled_features(feature_specs: list[dict[str, Any]]) -> int:
    """Count features that have the minimum identity required to be considered modeled."""

    return sum(
        1
        for item in feature_specs
        if str(item.get("function_id", "")).strip() and str(item.get("function_name", "")).strip()
    )


def count_missing_feature_gaps(gap_registry: list[dict[str, Any]]) -> int:
    """Count distinct missing-feature gaps as the unmodeled portion of the closure set."""

    unique_keys: set[str] = set()
    for item in gap_registry:
        gap = as_dict(item)
        if str(gap.get("gap_type", "")).strip() != "missing_feature":
            continue
        context = as_dict(gap.get("context"))
        key = (
            str(gap.get("subject_id", "")).strip()
            or str(context.get("feature_id", "")).strip()
            or str(context.get("entry_surface", "")).strip()
            or str(context.get("path", "")).strip()
            or str(gap.get("description", "")).strip()
            or str(gap.get("gap_id", "")).strip()
        )
        if key:
            unique_keys.add(key)
    return len(unique_keys)


def is_atomic_feature(feature: dict[str, Any]) -> bool:
    """Determine whether a feature is represented as one atomic entry surface."""

    normalized = as_dict(feature)
    atomicity_status = str(normalized.get("atomicity_status", "")).strip().lower()
    if atomicity_status:
        return atomicity_status in {"atomic", "true", "yes"}

    is_atomic = normalized.get("is_atomic")
    if isinstance(is_atomic, bool):
        return is_atomic

    entry_surface_count = normalized.get("entry_surface_count")
    if isinstance(entry_surface_count, (int, float)):
        return int(entry_surface_count) == 1

    entry_surfaces = as_list(normalized.get("entry_surfaces"))
    if entry_surfaces:
        return len(entry_surfaces) == 1

    implementation_mapping = as_dict(normalized.get("implementation_mapping"))
    mapped_entrypoints = as_list(implementation_mapping.get("entrypoints"))
    if mapped_entrypoints:
        return len(mapped_entrypoints) == 1

    entry_point = as_dict(normalized.get("entry_point"))
    return bool(entry_point.get("type") and entry_point.get("path"))


def compute_testability_score(
    feature_specs: list[dict[str, Any]],
    traceability_matrix: dict[str, Any] | None = None,
    gap_registry: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compute M-01~M-07 and the aggregate testability score."""

    matrix = as_dict(traceability_matrix)
    metrics = {
        "M-01": derive_feature_closure_rate(feature_specs, gap_registry),
        "M-02": derive_atomic_feature_rate(feature_specs),
        "M-03": average_metric(feature_specs, "oracle_completeness"),
        "M-04": average_metric(feature_specs, "fixture_readiness"),
        "M-05": derive_test_traceability_rate(feature_specs, matrix),
        "M-06": derive_rule_negative_rate(matrix),
        "M-07": derive_coverage_claim_rate(feature_specs),
    }
    score = 0.0
    for key, value in metrics.items():
        score += value * SCORE_WEIGHTS[key]
    score = round(score, 2)
    return {
        "metrics": metrics,
        "score": score,
        "grade": grade_for_score(score),
        "targets": TARGET_METRICS,
    }
