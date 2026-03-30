#!/usr/bin/env python3
"""Render the gap analysis deliverable from structured review output."""

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
    """Render the gap analysis markdown file."""

    args = parse_args()
    context = as_dict(load_json(args.context))
    payload = as_dict(load_json(args.payload))
    status = str(payload.get("status", "success"))

    if status == "failed":
        result = build_result(status="failed", errors=["cannot render gap analysis from failed payload"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        result = build_result(status="failed", errors=[f"project path does not exist: {project_path}"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    payload_context = as_dict(payload.get("context_writes"))
    differences = as_list(payload_context.get("difference_registry")) or as_list(context.get("difference_registry"))
    conflicts = as_list(payload.get("conflicts")) or as_list(context.get("conflict_registry"))
    gaps = as_list(payload.get("gaps")) or as_list(context.get("gap_registry"))

    difference_rows = [
        [
            stringify(item.get("difference_id")),
            stringify(item.get("difference_type")),
            stringify(item.get("subject_id")),
            stringify(item.get("description")),
            stringify(item.get("severity")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in differences
    ]
    conflict_rows = [
        [
            stringify(item.get("conflict_id")),
            stringify(item.get("conflict_type")),
            stringify(item.get("description")),
            stringify(item.get("priority_winner")),
            stringify(item.get("resolution")),
        ]
        for item in conflicts
    ]
    gap_rows = [
        [
            stringify(item.get("gap_id")),
            stringify(item.get("gap_type")),
            stringify(item.get("description")),
            stringify(item.get("gap_severity")),
            stringify(item.get("severity")),
            json.dumps(item.get("context", {}), ensure_ascii=False),
        ]
        for item in gaps
    ]

    critical_gaps = [item for item in gaps if str(item.get("severity", "")).lower() == "critical"]
    template_path = Path(__file__).resolve().parents[1] / "assets" / "gap-analysis-template.md"
    template_text = read_template(template_path)
    output_path = ensure_deliverables_dir(project_path) / "06-gap-analysis.md"
    rendered = render_template(
        template_text,
        {
            "difference_table": render_table(
                ["ID", "类型", "对象", "描述", "严重程度", "证据"],
                difference_rows or [["-", "-", "-", "-", "-", "-"]],
            ),
            "conflict_table": render_table(
                ["ID", "类型", "描述", "Winner", "Resolution"],
                conflict_rows or [["-", "-", "-", "-", "-"]],
            ),
            "gap_table": render_table(
                ["ID", "类型", "描述", "Gap Severity", "严重程度", "上下文"],
                gap_rows or [["-", "-", "-", "-", "-", "-"]],
            ),
            "summary_bullets": render_bullets(
                [
                    f"Total differences: {len(differences)}",
                    f"Total conflicts: {len(conflicts)}",
                    f"Total gaps: {len(gaps)}",
                    f"Critical gaps: {len(critical_gaps)}",
                    f"Gap types: {', '.join(sorted({str(item.get('gap_type', '')) for item in gaps if item.get('gap_type')})) or '(无)'}",
                ]
            ),
        },
    )
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(payload_context.get("deliverable_manifest")) or as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-006"])
    result = build_result(
        status=status,
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "deliverables": [
                {
                    "deliverable_id": "DLV-006",
                    "deliverable_type": "gap_analysis",
                    "path": ".review/deliverables/06-gap-analysis.md",
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
