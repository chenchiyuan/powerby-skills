#!/usr/bin/env python3
"""Render the test-case index deliverable from persisted review context."""

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
from testability_metrics import load_schema_rows


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def render_feature_rows(feature_specs: list[dict]) -> list[list[str]]:
    """Render per-feature test-case coverage rows."""

    rows: list[list[str]] = []
    for item in feature_specs:
        groups = [as_dict(group) for group in as_list(as_dict(item.get("d19_test_groups")).get("groups"))]
        existing_groups = ", ".join(group.get("name", "") for group in groups if group.get("name"))
        missing_groups = max(0, 8 - int(item.get("test_case_group_count", 0) or 0))
        rows.append(
            [
                str(item.get("function_id", "")),
                str(item.get("function_name", "")),
                str(item.get("testability_status", "")),
                str(item.get("test_case_group_count", 0)),
                existing_groups or "-",
                str(missing_groups),
            ]
        )
    return rows


def main() -> int:
    """Render the test-case index and update deliverable manifest."""

    args = parse_args()
    context = as_dict(load_json(args.context))
    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        result = build_result(status="failed", errors=[f"project path does not exist: {project_path}"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    feature_specs = [as_dict(item) for item in as_list(context.get("feature_spec_registry"))]
    ideal_rows = load_schema_rows("d19-test-groups-schema.md")
    template_text = read_template(Path(__file__).resolve().parents[1] / "assets" / "test-case-index-template.md")
    rendered = render_template(
        template_text,
        {
            "feature_table": render_table(
                ["Function ID", "名称", "状态", "当前组数", "已有测试组", "缺失组数"],
                render_feature_rows(feature_specs) or [["-", "-", "-", "-", "-", "-"]],
            ),
            "ideal_group_table": render_table(
                ["分组编号", "分组名称", "检查内容"],
                [[row.get("分组编号", ""), row.get("分组名称", ""), row.get("检查内容", "")] for row in ideal_rows]
                or [["-", "-", "-"]],
            ),
            "priority_notes": render_bullets(
                [
                    f"{item.get('function_id')}: 优先补齐 {max(0, 8 - int(item.get('test_case_group_count', 0) or 0))} 个测试组"
                    for item in feature_specs
                    if int(item.get("test_case_group_count", 0) or 0) < 8
                ]
            ),
        },
    )
    output_path = ensure_deliverables_dir(project_path) / "12-test-case-index.md"
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-012"])
    result = build_result(
        status="success",
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "report_path": ".review/deliverables/12-test-case-index.md",
            "deliverables": [
                {
                    "deliverable_id": "DLV-012",
                    "deliverable_type": "test_case_index",
                    "path": ".review/deliverables/12-test-case-index.md",
                    "status": "completed",
                }
            ],
        },
    )
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
