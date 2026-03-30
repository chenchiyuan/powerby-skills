#!/usr/bin/env python3
"""Render the data-flow deliverable from structured review output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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
    render_mermaid_block,
    render_table,
    render_template,
    stringify,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context = as_dict(load_json(args.context))
    payload = as_dict(load_json(args.payload))
    status = str(payload.get("status", "success"))
    if status == "failed":
        Path(args.output).write_text(
            json.dumps(build_result(status="failed", errors=["cannot render data-flow deliverable from failed payload"]), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return 0

    payload_context = as_dict(payload.get("context_writes"))
    registry = as_dict(payload_context.get("data_flow_registry")) or as_dict(context.get("data_flow_registry"))
    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        Path(args.output).write_text(
            json.dumps(build_result(status="failed", errors=[f"project path does not exist: {project_path}"]), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return 0

    data_object_rows = [
        [
            stringify(item.get("name")),
            ", ".join(as_list(item.get("producers"))),
            ", ".join(as_list(item.get("consumers"))),
            stringify(item.get("storage")),
            stringify(item.get("lifecycle")),
        ]
        for item in as_list(registry.get("data_objects"))
    ]
    flow_rows = [
        [
            stringify(item.get("flow_id")),
            stringify(item.get("name")),
            " -> ".join(as_list(item.get("steps"))),
            ", ".join(as_list(item.get("data_objects"))),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(registry.get("flow_paths"))
    ]
    mermaid_lines = ["graph LR"]
    for item in as_list(registry.get("flow_paths")):
        steps = as_list(as_dict(item).get("steps"))
        for current, nxt in zip(steps, steps[1:]):
            mermaid_lines.append(f"    {str(current).replace('-', '_')}[{current}] --> {str(nxt).replace('-', '_')}[{nxt}]")

    template = read_template(Path(__file__).resolve().parents[1] / "assets" / "data-flow-template.md")
    rendered = render_template(
        template,
        {
            "data_flow_graph": render_mermaid_block("\n".join(mermaid_lines) if len(mermaid_lines) > 1 else ""),
            "data_object_table": render_table(
                ["Data Object", "Producers", "Consumers", "Storage", "Lifecycle"],
                data_object_rows or [["-", "-", "-", "-", "-"]],
            ),
            "flow_path_table": render_table(
                ["Flow ID", "Name", "Steps", "Data Objects", "Evidence"],
                flow_rows or [["-", "-", "-", "-", "-"]],
            ),
            "summary_bullets": render_bullets(
                [
                    f"Data objects: {len(as_list(registry.get('data_objects')))}",
                    f"Flow paths: {len(as_list(registry.get('flow_paths')))}",
                ]
            ),
        },
    )

    output_path = ensure_deliverables_dir(project_path) / "10-data-flow.md"
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(payload_context.get("deliverable_manifest")) or as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-010"])
    result = build_result(
        status=status,
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "deliverables": [
                {
                    "deliverable_id": "DLV-010",
                    "deliverable_type": "data_flow",
                    "path": ".review/deliverables/10-data-flow.md",
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
