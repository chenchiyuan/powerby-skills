#!/usr/bin/env python3
"""Executor for pb-review-report-composer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[2] / "pb-review" / "scripts"))

from system_context_renderer import write_system_context
from testability_metrics import compute_testability_score, summarize_status_counts


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


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a simple Markdown table."""

    table = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    table.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(table)


def render_template(template_text: str, values: dict[str, str]) -> str:
    """Replace template placeholders with rendered content."""

    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def as_list(value: Any) -> list[Any]:
    """Return a list value or an empty list."""

    return value if isinstance(value, list) else []


def as_dict(value: Any) -> dict[str, Any]:
    """Return a dict value or an empty dict."""

    return value if isinstance(value, dict) else {}


def load_required_deliverables(manifest: dict[str, Any]) -> list[dict[str, str]]:
    """Return manifest entries as a normalized list."""

    rows: list[dict[str, str]] = []
    for item in as_list(manifest.get("required_deliverables")):
        normalized = as_dict(item)
        if not normalized:
            continue
        rows.append(
            {
                "deliverable_id": str(normalized.get("deliverable_id", "")),
                "deliverable_type": str(normalized.get("deliverable_type", "")),
                "path": str(normalized.get("path", "")),
                "producer_skill": str(normalized.get("producer_skill", "")),
                "status": str(normalized.get("status", "")),
            }
        )
    return rows


def check_required_deliverables(project_path: Path, manifest_rows: list[dict[str, str]]) -> list[str]:
    """Validate that upstream deliverables exist before composing the final report."""

    missing: list[str] = []
    for item in manifest_rows:
        deliverable_id = item["deliverable_id"]
        relative_path = item["path"]
        if deliverable_id in {"DLV-007", "DLV-011", "DLV-012", "DLV-013", "DLV-014"}:
            continue
        if not relative_path:
            missing.append(f"{deliverable_id}: missing path in deliverable_manifest")
            continue
        target = project_path / relative_path
        if relative_path.endswith("/"):
            if not target.exists() or not any(target.glob("*.md")):
                missing.append(f"{deliverable_id}: expected directory with markdown files at {relative_path}")
            continue
        if not target.exists():
            missing.append(f"{deliverable_id}: expected file at {relative_path}")
    return missing


def update_manifest_for_final_report(manifest: dict[str, Any]) -> dict[str, Any]:
    """Mark the final report deliverable as completed."""

    updated = dict(manifest)
    rows = []
    for item in load_required_deliverables(manifest):
        if item["deliverable_id"] == "DLV-007":
            item["status"] = "completed"
        rows.append(item)
    updated["required_deliverables"] = rows
    return updated


def main() -> int:
    """Run the report composer executor."""

    args = parse_args()
    context = load_json(args.context)
    template_path = Path(__file__).resolve().parents[1] / "assets" / "report-template.md"
    template_text = template_path.read_text(encoding="utf-8")
    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()

    project_metadata = as_dict(context.get("project_metadata"))
    object_registry = as_list(context.get("object_registry"))
    feature_spec_registry = as_list(context.get("feature_spec_registry"))
    feature_state_registry = as_list(context.get("feature_state_registry"))
    dependency_registry = as_list(context.get("dependency_registry"))
    implementation_registry = as_list(context.get("implementation_registry"))
    traceability_matrix = as_dict(context.get("traceability_matrix"))
    architecture_registry = as_dict(context.get("architecture_registry"))
    data_flow_registry = as_dict(context.get("data_flow_registry"))
    relation_registry = as_list(context.get("relation_registry"))
    conflict_registry = as_list(context.get("conflict_registry"))
    difference_registry = as_list(context.get("difference_registry"))
    gap_registry = as_list(context.get("gap_registry"))
    evidence_registry = as_list(context.get("evidence_registry"))
    deliverable_manifest = as_dict(context.get("deliverable_manifest"))

    required = {
        "project_metadata": bool(project_metadata),
        "object_registry": isinstance(object_registry, list),
        "feature_spec_registry": bool(feature_spec_registry),
        "dependency_registry": isinstance(dependency_registry, list),
        "implementation_registry": isinstance(implementation_registry, list),
        "traceability_matrix": bool(traceability_matrix),
        "architecture_registry": bool(architecture_registry),
        "data_flow_registry": bool(data_flow_registry),
        "difference_registry": isinstance(difference_registry, list),
        "gap_registry": isinstance(gap_registry, list),
        "deliverable_manifest": bool(deliverable_manifest),
    }
    missing_inputs = [name for name, present in required.items() if not present]
    updated_manifest = update_manifest_for_final_report(deliverable_manifest) if deliverable_manifest else {}
    manifest_rows = load_required_deliverables(updated_manifest or deliverable_manifest)
    missing_deliverables = check_required_deliverables(project_path, manifest_rows) if manifest_rows else []
    if missing_inputs or missing_deliverables:
        errors = []
        if missing_inputs:
            errors.append(f"missing required review inputs: {', '.join(missing_inputs)}")
        errors.extend(missing_deliverables)
        payload = {
            "status": "failed",
            "objects": [],
            "relations": [],
            "conflicts": [],
            "gaps": [],
            "context_writes": {},
            "metadata": {"report_path": "", "report_sections": [], "deliverables": []},
            "errors": errors,
        }
        with Path(args.output).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        return 0

    goals = [item for item in object_registry if item.get("object_type") == "goal"]
    roles = [item for item in object_registry if item.get("object_type") == "role"]
    scenarios = [item for item in object_registry if item.get("object_type") == "scenario"]
    constraints = [item for item in object_registry if item.get("object_type") == "constraint"]
    non_goals = [item for item in object_registry if item.get("object_type") == "non_goal"]

    deliverable_table = render_table(
        ["Deliverable ID", "类型", "路径", "责任 skill", "状态"],
        [
            [
                item["deliverable_id"],
                item["deliverable_type"],
                item["path"],
                item["producer_skill"],
                item["status"],
            ]
            for item in manifest_rows
        ]
        or [["-", "-", "-", "-", "-"]],
    )
    system_context_path = write_system_context(project_path, project_metadata, updated_manifest)

    product_rows = [[item["object_id"], item["name"], item.get("description", ""), ", ".join(item.get("evidence_refs", [])), item.get("confidence", "")] for item in goals]
    role_rows = [[item["object_id"], item["name"], item.get("description", ""), ", ".join(item.get("evidence_refs", []))] for item in roles]
    scenario_rows = [[item["object_id"], item["name"], item.get("description", ""), ", ".join(item.get("evidence_refs", []))] for item in scenarios]
    constraint_rows = [
        [item.get("object_type", ""), item["object_id"], item["name"], item.get("description", ""), ", ".join(item.get("evidence_refs", []))]
        for item in constraints + non_goals
    ]

    feature_spec_rows = [
        [
            str(item.get("function_id", "")),
            str(item.get("function_name", "")),
            str(item.get("domain_code", "")),
            str(item.get("module_code", "")),
            str(item.get("status", "")),
            str(item.get("deliverable_path", "")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in feature_spec_registry
    ]
    feature_state_rows = [
        [
            str(item.get("feature_id", item.get("object_id", ""))),
            str(item.get("state", item.get("status", ""))),
            str(item.get("source", item.get("metadata", {}).get("source", ""))),
            str(item.get("description", "")),
        ]
        for item in feature_state_registry
    ]
    status_counts = summarize_status_counts(feature_spec_registry)
    score = compute_testability_score(feature_spec_registry, traceability_matrix, gap_registry)

    goal_rows = [
        [
            str(item.get("goal_id", "")),
            str(item.get("goal_name", "")),
            ", ".join(as_list(item.get("supporting_features"))),
            str(item.get("coverage_status", "")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(traceability_matrix.get("goal_rows"))
    ]
    rule_rows = [
        [
            str(item.get("rule_id", "")),
            str(item.get("rule_name", "")),
            ", ".join(as_list(item.get("constrained_features"))),
            str(item.get("coverage_status", "")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(traceability_matrix.get("rule_rows"))
    ]
    dependency_summary_rows = [
        [
            str(item.get("source_function_id", "")),
            str(item.get("target_type", "")),
            str(item.get("target_id", "")),
            str(item.get("dependency_type", "")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in dependency_registry[:50]
    ]
    implementation_summary_rows = [
        [
            str(item.get("function_id", "")),
            str(item.get("mapping_type", "")),
            str(item.get("path", "")),
            str(item.get("role", "")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in implementation_registry[:50]
    ]
    architecture_summary_rows = [
        [
            "runtime_layer",
            str(item.get("layer", "")),
            ", ".join(as_list(item.get("functions"))),
        ]
        for item in as_list(architecture_registry.get("runtime_layers"))
    ] + [
        [
            "critical_path",
            str(item.get("name", "")),
            " -> ".join(as_list(item.get("function_ids"))),
        ]
        for item in as_list(architecture_registry.get("critical_paths"))
    ]
    data_flow_summary_rows = [
        [
            str(item.get("name", "")),
            ", ".join(as_list(item.get("producers"))),
            ", ".join(as_list(item.get("consumers"))),
            str(item.get("storage", "")),
        ]
        for item in as_list(data_flow_registry.get("data_objects"))
    ]

    difference_rows = [
        [
            str(item.get("difference_id", "")),
            str(item.get("difference_type", "")),
            str(item.get("subject_id", "")),
            str(item.get("description", "")),
            str(item.get("severity", "")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in difference_registry
    ]
    conflict_rows = [
        [
            str(item.get("conflict_id", "")),
            str(item.get("conflict_type", "")),
            str(item.get("description", "")),
            str(item.get("priority_winner", "")),
            str(item.get("resolution", "")),
        ]
        for item in conflict_registry
    ]
    gap_rows = [
        [
            str(item.get("gap_id", "")),
            str(item.get("gap_type", "")),
            str(item.get("description", "")),
            str(item.get("severity", "")),
            json.dumps(item.get("context", {}), ensure_ascii=False),
        ]
        for item in gap_registry
    ]
    evidence_rows = [
        [
            str(item.get("evidence_id", "")),
            str(item.get("source_type", "")),
            str(item.get("source_path", "")),
            str(item.get("timestamp", "")),
            str(item.get("author", "")),
        ]
        for item in evidence_registry[:200]
    ]

    report_dir = project_path / ".review" / "deliverables"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "07-review-report.md"
    legacy_report_path = project_path / ".review" / "review_report.md"
    report_content = render_template(
        template_text,
        {
            "project_overview": "\n".join(
                [
                    f"- **Review ID**: {context.get('review_id', '')}",
                    f"- **项目路径**: {context.get('project_path', '')}",
                    f"- **评审范围**: {context.get('scope', '')}",
                    f"- **项目名称**: {project_metadata.get('project_name', '')}",
                    f"- **项目类型**: {project_metadata.get('project_type', '')}",
                    f"- **文件总数**: {project_metadata.get('file_count', 0)}",
                ]
            ),
            "deliverable_manifest": deliverable_table,
            "goals_table": render_table(["ID", "名称", "描述", "证据", "置信度"], product_rows or [["-", "-", "-", "-", "-"]]),
            "roles_table": render_table(["ID", "名称", "描述", "证据"], role_rows or [["-", "-", "-", "-"]]),
            "scenarios_table": render_table(["ID", "名称", "描述", "证据"], scenario_rows or [["-", "-", "-", "-"]]),
            "constraints_table": render_table(["类型", "ID", "名称", "描述", "证据"], constraint_rows or [["-", "-", "-", "-", "-"]]),
            "feature_spec_table": render_table(
                ["Function ID", "名称", "Domain", "Module", "状态", "规格卡路径", "证据"],
                feature_spec_rows or [["-", "-", "-", "-", "-", "-", "-"]],
            ),
            "feature_state_table": render_table(["Feature ID", "状态", "来源", "说明"], feature_state_rows or [["-", "-", "-", "-"]]),
            "testability_summary": "\n\n".join(
                [
                    render_table(
                        ["指标", "值"],
                        [
                            ["testability_score", str(score["score"])],
                            ["grade", score["grade"]],
                            ["test_ready", str(status_counts["test_ready"])],
                            ["partial", str(status_counts["partial"])],
                            ["blocked", str(status_counts["blocked"])],
                        ],
                    ),
                    render_table(
                        ["M-01", "M-02", "M-03", "M-04", "M-05", "M-06", "M-07"],
                        [
                            [
                                str(score["metrics"]["M-01"]),
                                str(score["metrics"]["M-02"]),
                                str(score["metrics"]["M-03"]),
                                str(score["metrics"]["M-04"]),
                                str(score["metrics"]["M-05"]),
                                str(score["metrics"]["M-06"]),
                                str(score["metrics"]["M-07"]),
                            ]
                        ],
                    ),
                ]
            ),
            "goal_traceability_table": render_table(
                ["Goal ID", "Goal 名称", "Supporting Features", "Coverage", "证据"],
                goal_rows or [["-", "-", "-", "-", "-"]],
            ),
            "rule_traceability_table": render_table(
                ["Rule ID", "Rule 名称", "Constrained Features", "Coverage", "证据"],
                rule_rows or [["-", "-", "-", "-", "-"]],
            ),
            "dependency_summary_table": render_table(
                ["Section", "Type/Name", "Targets", "Notes", "Evidence"],
                (
                    [["dependency", row[0], f"{row[1]}:{row[2]}", row[3], row[4]] for row in dependency_summary_rows]
                    + [["implementation", row[0], row[2], f"{row[1]}/{row[3]}", row[4]] for row in implementation_summary_rows]
                )
                or [["-", "-", "-", "-", "-"]],
            ),
            "architecture_summary_table": render_table(
                ["Section", "Name", "Functions / Chain"],
                architecture_summary_rows or [["-", "-", "-"]],
            ),
            "data_flow_summary_table": render_table(
                ["Data Object", "Producers", "Consumers", "Storage"],
                data_flow_summary_rows or [["-", "-", "-", "-"]],
            ),
            "difference_table": render_table(["ID", "类型", "对象", "描述", "严重程度", "证据"], difference_rows or [["-", "-", "-", "-", "-", "-"]]),
            "conflict_table": render_table(["ID", "类型", "描述", "Winner", "Resolution"], conflict_rows or [["-", "-", "-", "-", "-"]]),
            "gap_table": render_table(["ID", "类型", "描述", "严重程度", "上下文"], gap_rows or [["-", "-", "-", "-", "-"]]),
            "evidence_table": render_table(["Evidence ID", "Source Type", "Source Path", "Timestamp", "Author"], evidence_rows or [["-", "-", "-", "-", "-"]]),
        },
    )
    report_content = report_content.rstrip() + f"\n\n_Template source: {template_path.name}_\n"
    report_path.write_text(report_content, encoding="utf-8")
    legacy_report_path.write_text(report_content, encoding="utf-8")

    payload = {
        "status": "success",
        "objects": [],
        "relations": [],
        "conflicts": [],
        "gaps": [],
        "context_writes": {"deliverable_manifest": updated_manifest},
        "metadata": {
            "report_path": str(report_path),
            "report_sections": [
                "project_overview",
                "deliverable_manifest",
                "product_reconstruction",
                "feature_spec_summary",
                "dependency_and_implementation",
                "traceability_matrix",
                "architecture_view",
                "data_flow",
                "gaps_and_conflicts",
                "evidence_index",
            ],
            "deliverables": [
                {
                    "deliverable_id": "DLV-001",
                    "deliverable_type": "system_context",
                    "path": system_context_path,
                    "status": "completed",
                },
                {
                    "deliverable_id": "DLV-007",
                    "deliverable_type": "review_report",
                    "path": ".review/deliverables/07-review-report.md",
                    "status": "completed",
                }
            ],
        },
        "errors": [],
    }

    with Path(args.output).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
