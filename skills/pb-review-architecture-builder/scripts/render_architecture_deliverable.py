#!/usr/bin/env python3
"""Render the layered architecture deliverable from structured review output."""

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
    render_records,
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
            json.dumps(build_result(status="failed", errors=["cannot render architecture deliverable from failed payload"]), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return 0

    payload_context = as_dict(payload.get("context_writes"))
    architecture = as_dict(payload_context.get("architecture_registry")) or as_dict(context.get("architecture_registry"))
    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        Path(args.output).write_text(
            json.dumps(build_result(status="failed", errors=[f"project path does not exist: {project_path}"]), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return 0

    runtime_rows = [
        [
            stringify(item.get("layer")),
            ", ".join(as_list(item.get("functions"))),
            stringify(item.get("description")),
        ]
        for item in as_list(architecture.get("runtime_layers"))
    ]
    domain_rows = [
        [
            stringify(item.get("domain_code")),
            stringify(item.get("domain_name")),
            ", ".join(as_list(item.get("functions"))),
        ]
        for item in as_list(architecture.get("domains"))
    ]
    path_rows = [
        [
            stringify(item.get("path_id")),
            stringify(item.get("name")),
            " -> ".join(as_list(item.get("function_ids"))),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(architecture.get("critical_paths"))
    ]

    template = read_template(Path(__file__).resolve().parents[1] / "assets" / "architecture-layered-template.md")
    rendered = render_template(
        template,
        {
            "runtime_layer_table": render_table(
                ["Runtime Layer", "Functions", "Description"],
                runtime_rows or [["-", "-", "-"]],
            ),
            "domain_table": render_table(
                ["Domain", "Name", "Functions"],
                domain_rows or [["-", "-", "-"]],
            ),
            "critical_path_table": render_table(
                ["Path ID", "Name", "Function Chain", "Evidence"],
                path_rows or [["-", "-", "-", "-"]],
            ),
            "dependency_rules": render_records(as_list(architecture.get("dependency_rules"))),
        },
    )

    output_path = ensure_deliverables_dir(project_path) / "08-architecture-layered.md"
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")
    manifest = as_dict(payload_context.get("deliverable_manifest")) or as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-008"])
    result = build_result(
        status=status,
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "deliverables": [
                {
                    "deliverable_id": "DLV-008",
                    "deliverable_type": "architecture_layered",
                    "path": ".review/deliverables/08-architecture-layered.md",
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
