#!/usr/bin/env python3
"""Render the product catalog deliverable from structured review output."""

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
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def select_objects(payload: dict[str, Any], context: dict[str, Any]) -> list[dict[str, Any]]:
    """Choose the latest product objects to render."""

    payload_objects = as_list(payload.get("objects"))
    if payload_objects:
        return [as_dict(item) for item in payload_objects if as_dict(item).get("object_type")]
    return [as_dict(item) for item in as_list(context.get("object_registry")) if as_dict(item).get("object_type")]


def filter_rows(objects: list[dict[str, Any]], object_type: str, include_confidence: bool = False) -> list[list[str]]:
    """Render rows for one product object category."""

    rows: list[list[str]] = []
    for item in objects:
        if item.get("object_type") != object_type:
            continue
        row = [
            str(item.get("object_id", "")),
            str(item.get("name", "")),
            str(item.get("description", "")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        if include_confidence:
            row.append(str(item.get("confidence", "")))
        rows.append(row)
    return rows


def collect_notes(payload: dict[str, Any]) -> list[str]:
    """Collect partial warnings for the catalog footer."""

    notes = [str(item) for item in as_list(payload.get("errors")) if str(item)]
    for gap in as_list(payload.get("gaps")):
        normalized = as_dict(gap)
        if normalized.get("gap_type") == "missing_evidence":
            notes.append(str(normalized.get("description", "")))
    return notes


def resolve_catalog_completeness(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Read completeness metrics from the iteration-010 metadata contract first."""

    payload_metadata = as_dict(payload.get("metadata"))
    completeness = as_dict(payload_metadata.get("product_catalog_completeness"))
    if completeness:
        return completeness
    return as_dict(as_dict(context.get("project_metadata")).get("product_catalog_completeness"))


def main() -> int:
    """Render the product catalog file and return updated manifest info."""

    args = parse_args()
    context = as_dict(load_json(args.context))
    payload = as_dict(load_json(args.payload))
    status = str(payload.get("status", "success"))

    if status == "failed":
        result = build_result(status="failed", errors=["cannot render product catalog from failed payload"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        result = build_result(status="failed", errors=[f"project path does not exist: {project_path}"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    objects = select_objects(payload, context)
    template_path = Path(__file__).resolve().parents[1] / "assets" / "product-catalog-template.md"
    template_text = read_template(template_path)
    deliverables_dir = ensure_deliverables_dir(project_path)
    output_path = deliverables_dir / "02-product-catalog.md"

    rendered = render_template(
        template_text,
        {
            "goals_table": render_table(
                ["ID", "名称", "描述", "证据", "置信度"],
                filter_rows(objects, "goal", include_confidence=True) or [["-", "-", "-", "-", "-"]],
            ),
            "roles_table": render_table(
                ["ID", "名称", "描述", "证据"],
                filter_rows(objects, "role") or [["-", "-", "-", "-"]],
            ),
            "scenarios_table": render_table(
                ["ID", "名称", "描述", "证据"],
                filter_rows(objects, "scenario") or [["-", "-", "-", "-"]],
            ),
            "constraints_table": render_table(
                ["ID", "名称", "描述", "证据"],
                filter_rows(objects, "constraint") or [["-", "-", "-", "-"]],
            ),
            "non_goals_table": render_table(
                ["ID", "名称", "描述", "证据"],
                filter_rows(objects, "non_goal") or [["-", "-", "-", "-"]],
            ),
            "completeness_summary": render_bullets(
                [
                    f"{key}: {value}"
                    for key, value in resolve_catalog_completeness(payload, context).items()
                ]
            ),
            "review_notes": render_bullets(collect_notes(payload)),
        },
    )
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(payload.get("context_writes", {})).get("deliverable_manifest")
    base_manifest = as_dict(manifest) or as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(base_manifest, ["DLV-002"])
    result = build_result(
        status=status,
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "deliverables": [
                {
                    "deliverable_id": "DLV-002",
                    "deliverable_type": "product_catalog",
                    "path": ".review/deliverables/02-product-catalog.md",
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
