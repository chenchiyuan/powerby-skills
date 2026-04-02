#!/usr/bin/env python3
"""Render the traceability matrix deliverable from structured review output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SHARED_SCRIPTS = Path(__file__).resolve().parents[2] / "pb-review" / "scripts"
if str(SHARED_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SHARED_SCRIPTS))

from deliverable_rendering import (  # noqa: E402
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
    stringify,
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    """Render the traceability matrix markdown file."""

    args = parse_args()
    context = as_dict(load_json(args.context))
    payload = as_dict(load_json(args.payload))
    status = str(payload.get("status", "success"))

    if status == "failed":
        result = build_result(status="failed", errors=["cannot render traceability matrix from failed payload"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        result = build_result(status="failed", errors=[f"project path does not exist: {project_path}"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    payload_context = as_dict(payload.get("context_writes"))
    matrix = as_dict(payload_context.get("traceability_matrix")) or as_dict(context.get("traceability_matrix"))
    goals = [
        [
            stringify(item.get("goal_id")),
            stringify(item.get("goal_name")),
            ", ".join(as_list(item.get("supporting_features"))),
            stringify(item.get("coverage_status")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(matrix.get("goal_rows"))
    ]
    rules = [
        [
            stringify(item.get("rule_id")),
            stringify(item.get("rule_name")),
            ", ".join(as_list(item.get("constrained_features"))),
            stringify(item.get("coverage_status")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(matrix.get("rule_rows"))
    ]
    feature_dependencies = [
        [
            stringify(item.get("function_id")),
            ", ".join(as_list(item.get("upstream_features"))),
            ", ".join(as_list(item.get("downstream_features"))),
            ", ".join(as_list(item.get("dependency_types"))),
            stringify(item.get("coverage_status")),
        ]
        for item in as_list(matrix.get("feature_dependency_rows"))
    ]
    feature_implementations = [
        [
            stringify(item.get("function_id")),
            stringify(item.get("runtime_layer")),
            ", ".join(as_list(item.get("services"))),
            ", ".join(as_list(item.get("models"))),
            ", ".join(as_list(item.get("tests"))),
            stringify(item.get("coverage_status")),
        ]
        for item in as_list(matrix.get("feature_implementation_rows"))
    ]
    feature_tests = [
        [
            stringify(item.get("function_id")),
            ", ".join(
                f"{as_dict(group).get('group_name', '')}({as_dict(group).get('test_count', '')})"
                for group in as_list(item.get("test_groups"))
            ),
            stringify(item.get("coverage_status")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(matrix.get("feature_test_rows"))
    ]
    negative_tests = [
        [
            stringify(item.get("rule_id")),
            stringify(item.get("rule_name")),
            ", ".join(
                f"{as_dict(test).get('test_file', '')}:{as_dict(test).get('test_function', '')}"
                for test in as_list(item.get("negative_tests"))
            ),
            stringify(item.get("coverage_status")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(matrix.get("rule_negative_test_rows"))
    ]
    coverage = as_dict(matrix.get("coverage_stats"))

    template_path = Path(__file__).resolve().parents[1] / "assets" / "traceability-matrix-template.md"
    template_text = read_template(template_path)
    output_path = ensure_deliverables_dir(project_path) / "05-traceability-matrix.md"
    rendered = render_template(
        template_text,
        {
            "goal_feature_table": render_table(
                ["Goal ID", "Goal 名称", "Supporting Features", "Coverage", "证据"],
                goals or [["-", "-", "-", "-", "-"]],
            ),
            "rule_feature_table": render_table(
                ["Rule ID", "Rule 名称", "Constrained Features", "Coverage", "证据"],
                rules or [["-", "-", "-", "-", "-"]],
            ),
            "feature_dependency_table": render_table(
                ["Function ID", "Upstream Features", "Downstream Features", "Dependency Types", "Coverage"],
                feature_dependencies or [["-", "-", "-", "-", "-"]],
            ),
            "feature_implementation_table": render_table(
                ["Function ID", "Runtime Layer", "Services", "Models", "Tests", "Coverage"],
                feature_implementations or [["-", "-", "-", "-", "-", "-"]],
            ),
            "feature_test_table": render_table(
                ["Function ID", "Test Groups", "Coverage", "证据"],
                feature_tests or [["-", "-", "-", "-"]],
            ),
            "rule_negative_test_table": render_table(
                ["Rule ID", "Rule 名称", "Negative Tests", "Coverage", "证据"],
                negative_tests or [["-", "-", "-", "-", "-"]],
            ),
            "coverage_stats": render_bullets(
                [
                    f"Goal coverage rate: {stringify(coverage.get('goal_coverage_rate')) or '0'}",
                    f"Feature traceability rate: {stringify(coverage.get('feature_traceability_rate')) or '0'}",
                    f"Dependency traceability rate: {stringify(coverage.get('dependency_traceability_rate')) or '0'}",
                    f"Test traceability rate: {stringify(coverage.get('test_traceability_rate')) or '0'}",
                    f"Rule negative test rate: {stringify(coverage.get('rule_negative_test_rate')) or '0'}",
                ]
            ),
        },
    )
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(payload_context.get("deliverable_manifest")) or as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-005"])
    result = build_result(
        status=status,
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "deliverables": [
                {
                    "deliverable_id": "DLV-005",
                    "deliverable_type": "traceability_matrix",
                    "path": ".review/deliverables/05-traceability-matrix.md",
                    "status": "completed",
                }
            ]
        },
        errors=[str(item) for item in as_list(payload.get("errors")) if str(item)],
    )
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
