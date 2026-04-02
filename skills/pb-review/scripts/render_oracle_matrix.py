#!/usr/bin/env python3
"""Render the oracle-matrix deliverable from persisted review context."""

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


def collect_missing_oracles(feature: dict) -> str:
    """Collect missing oracle items for one feature."""

    sub_items = [as_dict(item) for item in as_list(as_dict(feature.get("d17_oracle")).get("sub_items"))]
    missing = [item.get("id", "") for item in sub_items if item.get("status") == "missing"]
    return ", ".join(item for item in missing if item) or "-"


def main() -> int:
    """Render oracle matrix report and update deliverable manifest."""

    args = parse_args()
    context = as_dict(load_json(args.context))
    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        result = build_result(status="failed", errors=[f"project path does not exist: {project_path}"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    feature_specs = [as_dict(item) for item in as_list(context.get("feature_spec_registry"))]
    ideal_rows = load_schema_rows("d17-oracle-schema.md")
    feature_rows = [
        [str(item.get("function_id", "")), str(item.get("function_name", "")), str(item.get("oracle_completeness", 0)), collect_missing_oracles(item)]
        for item in feature_specs
    ]
    gap_notes = [
        f"{item.get('function_id')}: oracle={item.get('oracle_completeness', 0)}"
        for item in feature_specs
        if float(item.get("oracle_completeness", 0) or 0) < 90
    ]

    template_text = read_template(Path(__file__).resolve().parents[1] / "assets" / "oracle-matrix-template.md")
    rendered = render_template(
        template_text,
        {
            "feature_table": render_table(
                ["Function ID", "名称", "Oracle 完整度", "缺失子项"],
                feature_rows or [["-", "-", "-", "-"]],
            ),
            "ideal_oracle_table": render_table(
                ["子项编号", "子项名称", "检查内容"],
                [[row.get("子项编号", ""), row.get("子项名称", ""), row.get("检查内容", "")] for row in ideal_rows]
                or [["-", "-", "-"]],
            ),
            "gap_notes": render_bullets(gap_notes),
        },
    )
    output_path = ensure_deliverables_dir(project_path) / "14-test-oracle-matrix.md"
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-014"])
    result = build_result(
        status="success",
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "report_path": ".review/deliverables/14-test-oracle-matrix.md",
            "deliverables": [
                {
                    "deliverable_id": "DLV-014",
                    "deliverable_type": "oracle_matrix",
                    "path": ".review/deliverables/14-test-oracle-matrix.md",
                    "status": "completed",
                }
            ],
        },
    )
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
