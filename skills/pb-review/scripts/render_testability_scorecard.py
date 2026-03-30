#!/usr/bin/env python3
"""Render the testability scorecard deliverable from persisted review context."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from deliverable_rendering import (
    as_dict,
    as_list,
    build_result,
    ensure_deliverables_dir,
    load_json,
    mark_deliverables_completed,
    read_template,
    render_bullets,
    render_table,
    render_template,
)
from testability_metrics import compute_testability_score, load_schema_text, summarize_status_counts


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    """Render the scorecard and update deliverable manifest."""

    args = parse_args()
    context = as_dict(load_json(args.context))
    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        result = build_result(status="failed", errors=[f"project path does not exist: {project_path}"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    feature_specs = [as_dict(item) for item in as_list(context.get("feature_spec_registry"))]
    gap_registry = [as_dict(item) for item in as_list(context.get("gap_registry"))]
    score = compute_testability_score(
        feature_specs,
        as_dict(context.get("traceability_matrix")),
        gap_registry,
    )
    status_counts = summarize_status_counts(feature_specs)
    metrics_table = render_table(
        ["指标", "当前值", "目标值", "差距"],
        [
            [
                metric,
                str(score["metrics"][metric]),
                str(score["targets"][metric]),
                str(round(score["targets"][metric] - score["metrics"][metric], 2)),
            ]
            for metric in ["M-01", "M-02", "M-03", "M-04", "M-05", "M-06", "M-07"]
        ],
    )
    template_text = read_template(Path(__file__).resolve().parents[1] / "assets" / "testability-scorecard-template.md")
    rendered = render_template(
        template_text,
        {
            "score_summary": render_bullets(
                [
                    f"Testability score: {score['score']}",
                    f"Grade: {score['grade']}",
                    f"Feature count: {len(feature_specs)}",
                ]
            ),
            "metrics_table": metrics_table,
            "status_summary": render_bullets(
                [
                    f"test_ready: {status_counts['test_ready']}",
                    f"partial: {status_counts['partial']}",
                    f"blocked: {status_counts['blocked']}",
                ]
            ),
            "gap_summary": render_bullets(
                [
                    f"{item.get('gap_type')}: {item.get('description')} ({item.get('gap_severity') or item.get('severity') or 'unknown'})"
                    for item in gap_registry[:20]
                ]
            ),
            "formula_reference": load_schema_text("testability-score-formula.md"),
        },
    )
    output_path = ensure_deliverables_dir(project_path) / "11-testability-scorecard.md"
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-011"])
    result = build_result(
        status="success",
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "report_path": ".review/deliverables/11-testability-scorecard.md",
            "deliverables": [
                {
                    "deliverable_id": "DLV-011",
                    "deliverable_type": "testability_scorecard",
                    "path": ".review/deliverables/11-testability-scorecard.md",
                    "status": "completed",
                }
            ],
        },
    )
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
