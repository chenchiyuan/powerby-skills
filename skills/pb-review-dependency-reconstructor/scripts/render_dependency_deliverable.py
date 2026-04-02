#!/usr/bin/env python3
"""Render the dependency matrix deliverable from structured review output."""

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
            json.dumps(build_result(status="failed", errors=["cannot render dependency deliverable from failed payload"]), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return 0

    payload_context = as_dict(payload.get("context_writes"))
    registry = as_list(payload_context.get("dependency_registry")) or as_list(context.get("dependency_registry"))
    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        Path(args.output).write_text(
            json.dumps(build_result(status="failed", errors=[f"project path does not exist: {project_path}"]), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return 0

    feature_rows = []
    external_rows = []
    data_rows = []
    edges = []
    for item in registry:
        normalized = as_dict(item)
        source = stringify(normalized.get("source_function_id"))
        target_type = stringify(normalized.get("target_type"))
        target = stringify(normalized.get("target_id"))
        dependency_type = stringify(normalized.get("dependency_type"))
        description = stringify(normalized.get("description"))
        confidence = stringify(normalized.get("confidence"))
        evidence = ", ".join(as_list(normalized.get("evidence_refs")))
        if source and target and target_type == "feature":
            feature_rows.append([source, target, dependency_type, confidence, evidence])
            edges.append((source, target, dependency_type))
        elif source and target and target_type == "external_system":
            external_rows.append([source, target, dependency_type, description, evidence])
        elif source and target and target_type == "data_object":
            data_rows.append([source, target, dependency_type, description, evidence])

    mermaid_lines = ["graph TD"]
    for source, target, dependency_type in edges:
        mermaid_lines.append(f"    {source.replace('-', '_')}[{source}] -->|{dependency_type or 'depends'}| {target.replace('-', '_')}[{target}]")

    template = read_template(Path(__file__).resolve().parents[1] / "assets" / "dependency-matrix-template.md")
    rendered = render_template(
        template,
        {
            "dependency_graph": render_mermaid_block("\n".join(mermaid_lines) if len(mermaid_lines) > 1 else ""),
            "feature_dependency_table": render_table(
                ["Function ID", "Upstream / Target", "Dependency Type", "Confidence", "Evidence"],
                feature_rows or [["-", "-", "-", "-", "-"]],
            ),
            "external_dependency_table": render_table(
                ["Function ID", "External ID", "Dependency Type", "Description", "Evidence"],
                external_rows or [["-", "-", "-", "-", "-"]],
            ),
            "data_dependency_table": render_table(
                ["Function ID", "Data Object", "Dependency Type", "Description", "Evidence"],
                data_rows or [["-", "-", "-", "-", "-"]],
            ),
            "summary_bullets": render_bullets(
                [
                    f"Total dependencies: {len(registry)}",
                    f"Feature dependencies: {len(feature_rows)}",
                    f"External dependencies: {len(external_rows)}",
                    f"Data-object dependencies: {len(data_rows)}",
                ]
            ),
        },
    )

    output_path = ensure_deliverables_dir(project_path) / "09-dependency-matrix.md"
    output_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(payload_context.get("deliverable_manifest")) or as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-009"])
    result = build_result(
        status=status,
        context_writes={"deliverable_manifest": updated_manifest},
        metadata={
            "deliverables": [
                {
                    "deliverable_id": "DLV-009",
                    "deliverable_type": "dependency_matrix",
                    "path": ".review/deliverables/09-dependency-matrix.md",
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
