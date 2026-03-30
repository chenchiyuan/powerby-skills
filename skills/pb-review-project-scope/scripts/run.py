#!/usr/bin/env python3
"""Executor for pb-review-project-scope."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

DOC_SUFFIXES = {".md", ".rst", ".txt"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".rb", ".php", ".sh"}
CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"}
IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".review",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "htmlcov",
}

sys.path.append(str(Path(__file__).resolve().parents[2] / "pb-review" / "scripts"))

from system_context_renderer import write_system_context
from testability_metrics import load_schema_rows


def build_deliverable_manifest() -> dict:
    """Return the canonical pb-review deliverable manifest skeleton."""

    return {
        "version": "2.0",
        "required_deliverables": [
            {
                "deliverable_id": "DLV-001",
                "deliverable_type": "system_context",
                "path": ".review/deliverables/01-system-context.md",
                "producer_skill": "pb-review-project-scope",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-002",
                "deliverable_type": "product_catalog",
                "path": ".review/deliverables/02-product-catalog.md",
                "producer_skill": "pb-review-product-reconstructor",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-003",
                "deliverable_type": "feature_spec_index",
                "path": ".review/deliverables/03-feature-spec-index.md",
                "producer_skill": "pb-review-feature-reconstructor",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-004",
                "deliverable_type": "feature_spec_cards",
                "path": ".review/deliverables/04-feature-specs/",
                "producer_skill": "pb-review-feature-reconstructor",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-005",
                "deliverable_type": "traceability_matrix",
                "path": ".review/deliverables/05-traceability-matrix.md",
                "producer_skill": "pb-review-relation-builder",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-006",
                "deliverable_type": "gap_analysis",
                "path": ".review/deliverables/06-gap-analysis.md",
                "producer_skill": "pb-review-gap-analyzer",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-008",
                "deliverable_type": "architecture_layered",
                "path": ".review/deliverables/08-architecture-layered.md",
                "producer_skill": "pb-review-architecture-builder",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-009",
                "deliverable_type": "dependency_matrix",
                "path": ".review/deliverables/09-dependency-matrix.md",
                "producer_skill": "pb-review-dependency-reconstructor",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-010",
                "deliverable_type": "data_flow",
                "path": ".review/deliverables/10-data-flow.md",
                "producer_skill": "pb-review-data-flow-builder",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-007",
                "deliverable_type": "review_report",
                "path": ".review/deliverables/07-review-report.md",
                "producer_skill": "pb-review-report-composer",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-011",
                "deliverable_type": "testability_scorecard",
                "path": ".review/deliverables/11-testability-scorecard.md",
                "producer_skill": "pb-review",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-012",
                "deliverable_type": "test_case_index",
                "path": ".review/deliverables/12-test-case-index.md",
                "producer_skill": "pb-review",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-013",
                "deliverable_type": "fixture_contract",
                "path": ".review/deliverables/13-test-fixture-contract.md",
                "producer_skill": "pb-review",
                "status": "pending",
            },
            {
                "deliverable_id": "DLV-014",
                "deliverable_type": "oracle_matrix",
                "path": ".review/deliverables/14-test-oracle-matrix.md",
                "producer_skill": "pb-review",
                "status": "pending",
            },
        ],
    }


def mark_deliverable_completed(manifest: dict, deliverable_id: str) -> dict:
    """Mark one deliverable as completed in the manifest."""

    updated = {"version": str(manifest.get("version", "2.0")), "required_deliverables": []}
    for item in manifest.get("required_deliverables", []):
        normalized = dict(item)
        if normalized.get("deliverable_id") == deliverable_id:
            normalized["status"] = "completed"
        updated["required_deliverables"].append(normalized)
    return updated


def merge_manifest(existing_manifest: dict, default_manifest: dict) -> dict:
    """Merge existing manifest statuses into the current canonical skeleton."""

    existing_rows = {
        str(item.get("deliverable_id", "")): item
        for item in existing_manifest.get("required_deliverables", [])
        if isinstance(item, dict)
    }
    merged_rows = []
    for item in default_manifest.get("required_deliverables", []):
        deliverable_id = str(item.get("deliverable_id", ""))
        merged = dict(item)
        if deliverable_id in existing_rows:
            merged["status"] = str(existing_rows[deliverable_id].get("status", merged.get("status", "pending")))
        merged_rows.append(merged)
    return {
        "version": str(default_manifest.get("version", existing_manifest.get("version", "2.0"))),
        "required_deliverables": merged_rows,
    }


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def load_json(path: str) -> dict:
    """Load JSON data from disk."""

    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_dict(value: object) -> dict:
    """Return a dict value or an empty dict."""

    return value if isinstance(value, dict) else {}


def is_test_path(relative_path: str) -> bool:
    """Detect whether a path looks like a test file."""

    lowered = relative_path.lower()
    stem = Path(lowered).stem
    return (
        "/tests/" in lowered
        or lowered.startswith("tests/")
        or lowered.startswith("test/")
        or stem.startswith("test_")
        or stem.endswith("_test")
    )


def classify_path(relative_path: str) -> str | None:
    """Classify a repository file into a resource bucket."""

    suffix = Path(relative_path).suffix.lower()
    if suffix in DOC_SUFFIXES:
        return "docs"
    if is_test_path(relative_path):
        return "tests"
    if suffix in CODE_SUFFIXES:
        return "code"
    if suffix in CONFIG_SUFFIXES:
        return "configs"
    return None


def detect_project_type(project_root: Path, inventory: dict) -> str:
    """Infer a coarse project type from files and directories."""

    if (project_root / "manage.py").exists():
        return "django-monolith"
    if (project_root / "skills").exists():
        return "skill-repo"
    if (project_root / "package.json").exists() and (
        (project_root / "pyproject.toml").exists() or (project_root / "requirements.txt").exists()
    ):
        return "polyglot-repo"
    if (project_root / "package.json").exists():
        return "node-repo"
    if (project_root / "pyproject.toml").exists() or (project_root / "requirements.txt").exists():
        return "python-repo"
    if inventory.get("docs") and inventory.get("code"):
        return "mixed"
    return "unknown"


def should_skip_dir(name: str, exclude_names: set[str]) -> bool:
    """Check whether a directory should be skipped."""

    return name in exclude_names or name.endswith(".egg-info")


def scan_project(project_root: Path) -> tuple[dict, int]:
    """Walk the project tree and classify files."""

    inventory = {"docs": [], "code": [], "tests": [], "configs": []}
    file_count = 0
    exclude_names = set(IGNORED_DIR_NAMES)

    for current_root, dir_names, file_names in os.walk(project_root):
        dir_names[:] = [name for name in dir_names if not should_skip_dir(name, exclude_names)]
        for file_name in file_names:
            relative_path = str((Path(current_root) / file_name).resolve().relative_to(project_root))
            bucket = classify_path(relative_path)
            if bucket is None:
                continue
            inventory[bucket].append(relative_path)
            file_count += 1

    for key in inventory:
        inventory[key].sort()
    return inventory, file_count


def normalize_product_doc_dir(project_root: Path, raw_path: str) -> str:
    """Normalize a configured product-doc path to a project-relative prefix."""

    candidate = Path(raw_path)
    resolved = candidate.expanduser().resolve() if candidate.is_absolute() else (project_root / candidate).resolve()
    try:
        relative = resolved.relative_to(project_root)
    except ValueError as exc:
        raise ValueError(f"product_docs_dir must be inside project root: {raw_path}") from exc
    return str(relative).strip("/")


def select_product_docs(project_root: Path, docs_inventory: list[str], raw_paths: list[str]) -> list[str]:
    """Select product-document files under user-provided directories."""

    if not raw_paths:
        return []
    normalized_dirs = [normalize_product_doc_dir(project_root, raw_path) for raw_path in raw_paths]
    selected = []
    for relative_path in docs_inventory:
        normalized_path = relative_path.strip("/")
        if any(
            normalized_path == prefix or normalized_path.startswith(prefix + "/")
            for prefix in normalized_dirs
        ):
            selected.append(relative_path)
    return sorted(set(selected))


def discover_entry_surfaces(inventory: dict[str, list[str]]) -> list[dict[str, str]]:
    """Discover project entry surfaces using schema-backed type definitions."""

    type_rows = load_schema_rows("entry-surface-types.md")
    type_order = [row.get("类型", "").strip() for row in type_rows if row.get("类型")]
    seen: set[tuple[str, str]] = set()
    surfaces: list[dict[str, str]] = []

    for relative_path in inventory.get("code", []) + inventory.get("configs", []):
        lowered = relative_path.lower()
        candidates: list[str] = []
        if "management/commands" in lowered or lowered.endswith("cli.py") or "powerby-cli.py" in lowered:
            candidates.append("cli")
        if "urls.py" in lowered or "/api/" in lowered or "router" in lowered or "viewset" in lowered:
            candidates.append("api")
        if "/pages/" in lowered or "/templates/" in lowered or lowered.endswith("views.py"):
            candidates.append("page")
        if "cron" in lowered or "scheduler" in lowered or "celery" in lowered or lowered.endswith("tasks.py"):
            candidates.append("cron")
        if "workflow" in lowered or "orchestr" in lowered or "pipeline" in lowered or "runner" in lowered:
            candidates.append("orchestration")

        for surface_type in candidates:
            if surface_type not in type_order:
                continue
            key = (surface_type, relative_path)
            if key in seen:
                continue
            seen.add(key)
            surfaces.append(
                {
                    "type": surface_type,
                    "path": relative_path,
                    "name": Path(relative_path).stem.replace("_", " "),
                }
            )
            break

    return sorted(surfaces, key=lambda item: (item["type"], item["path"]))


def main() -> int:
    """Run the project scope executor."""

    args = parse_args()
    context = load_json(args.context)
    parameters = load_json(args.parameters)
    project_root = Path(parameters["project_path"]).expanduser().resolve()
    scope = parameters["scope"]
    start = time.time()

    if not project_root.exists():
        payload = {
            "status": "failed",
            "objects": [],
            "relations": [],
            "conflicts": [],
            "gaps": [],
            "context_writes": {},
            "metadata": {"scan_duration_ms": 0},
            "errors": [f"project path does not exist: {project_root}"],
        }
    else:
        inventory, file_count = scan_project(project_root)
        product_doc_dirs = parameters.get("product_docs_dirs", [])
        product_doc_inventory = select_product_docs(project_root, inventory["docs"], product_doc_dirs)
        missing = [name for name, records in inventory.items() if not records]
        if product_doc_dirs and not product_doc_inventory:
            missing.append("product_docs")
        status = "success" if file_count > 0 else "failed"
        project_metadata = {
            "project_name": project_root.name,
            "project_type": detect_project_type(project_root, inventory),
            "scope": scope,
            "file_count": file_count,
            "product_doc_dirs": product_doc_dirs,
            "product_doc_inventory": product_doc_inventory,
            "entry_surface_inventory": discover_entry_surfaces(inventory),
            "resource_inventory": inventory,
            "missing_resources": missing,
        }
        manifest = merge_manifest(as_dict(context.get("deliverable_manifest")), build_deliverable_manifest())
        manifest = mark_deliverable_completed(manifest, "DLV-001")
        system_context_path = write_system_context(project_root, project_metadata, manifest)
        payload = {
            "status": status,
            "objects": [],
            "relations": [],
            "conflicts": [],
            "gaps": [],
            "context_writes": {
                "project_metadata": project_metadata,
                "deliverable_manifest": manifest,
            },
            "metadata": {
                "scan_duration_ms": int((time.time() - start) * 1000),
                "deliverables": [
                    {
                        "deliverable_id": "DLV-001",
                        "deliverable_type": "system_context",
                        "path": system_context_path,
                        "status": "completed",
                    }
                ],
            },
            "errors": [] if file_count > 0 else [f"no supported files found under {project_root}"],
        }

    with Path(args.output).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
