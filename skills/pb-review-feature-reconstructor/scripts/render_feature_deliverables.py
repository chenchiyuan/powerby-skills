#!/usr/bin/env python3
"""Render feature index and feature spec cards from structured review output."""

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
    render_json_block,
    render_key_value_bullets,
    render_records,
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


def choose_registry(payload: dict[str, Any], context: dict[str, Any], field: str) -> list[dict[str, Any]]:
    """Choose the freshest registry list from payload or context."""

    payload_context = as_dict(payload.get("context_writes"))
    candidate = payload_context.get(field)
    if isinstance(candidate, list):
        return [as_dict(item) for item in candidate]
    return [as_dict(item) for item in as_list(context.get(field))]


def with_deliverable_paths(feature_specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ensure every feature spec points at its canonical markdown card."""

    normalized: list[dict[str, Any]] = []
    for item in feature_specs:
        function_id = str(item.get("function_id", "")).strip()
        updated = dict(item)
        if function_id and not updated.get("deliverable_path"):
            updated["deliverable_path"] = f".review/deliverables/04-feature-specs/{function_id}.md"
        normalized.append(updated)
    return normalized


def render_parameters(input_spec: dict[str, Any]) -> str:
    """Render parameter definitions and schema."""

    parameters = []
    for item in as_list(input_spec.get("parameters")):
        normalized = as_dict(item)
        parameters.append(
            [
                stringify(normalized.get("name")),
                stringify(normalized.get("type")),
                stringify(normalized.get("required")),
                stringify(normalized.get("default")),
                ", ".join(as_list(normalized.get("constraints"))),
                stringify(normalized.get("example")),
            ]
        )
    parameter_table = render_table(
        ["参数", "类型", "必填", "默认值", "约束", "示例"],
        parameters or [["-", "-", "-", "-", "-", "-"]],
    )
    schema_block = render_json_block(as_dict(input_spec.get("schema")) or input_spec.get("input_schema"))
    return parameter_table + "\n\n### Input Schema\n\n" + schema_block


def render_entry_point(entry_point: dict[str, Any]) -> str:
    """Render entry point metadata."""

    return render_key_value_bullets(
        [
            ("类型", stringify(entry_point.get("type"))),
            ("路径", stringify(entry_point.get("path"))),
            ("命令", stringify(entry_point.get("command"))),
        ]
    )


def count_mapping_items(mapping: dict[str, Any]) -> int:
    """Count implementation mapping items."""

    return sum(len(as_list(mapping.get(key))) for key in ["entrypoints", "services", "repositories", "models", "tests", "configs"])


def render_dependencies(dependencies: dict[str, Any]) -> str:
    """Render D-15 dependency sections."""

    sections = [
        "### Upstream\n\n" + render_records(as_list(dependencies.get("upstream"))),
        "### Downstream\n\n" + render_records(as_list(dependencies.get("downstream"))),
        "### External\n\n" + render_records(as_list(dependencies.get("external"))),
        "### Data Objects\n\n" + render_records(as_list(dependencies.get("data_objects"))),
    ]
    return "\n\n".join(sections)


def render_implementation_mapping(mapping: dict[str, Any]) -> str:
    """Render D-16 implementation mapping sections."""

    sections = [
        "### Entrypoints\n\n" + render_records(as_list(mapping.get("entrypoints"))),
        "### Services\n\n" + render_records(as_list(mapping.get("services"))),
        "### Repositories\n\n" + render_records(as_list(mapping.get("repositories"))),
        "### Models\n\n" + render_records(as_list(mapping.get("models"))),
        "### Tests\n\n" + render_records(as_list(mapping.get("tests"))),
        "### Configs\n\n" + render_records(as_list(mapping.get("configs"))),
    ]
    return "\n\n".join(sections)


def render_sub_item_table(data: dict[str, Any], headers: list[str]) -> str:
    """Render D-17/D-18 sub-item rows."""

    rows = [
        [
            stringify(item.get("id")),
            stringify(item.get("name")),
            stringify(item.get("status")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(data.get("sub_items"))
    ]
    return render_table(headers, rows or [["-", "-", "-", "-"]])


def render_test_groups(data: dict[str, Any]) -> str:
    """Render D-19 test group sections."""

    rows = [
        [
            stringify(item.get("name")),
            stringify(item.get("test_count")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in as_list(data.get("groups"))
    ]
    summary = render_key_value_bullets([("Test Group Count", stringify(data.get("count")))])
    return summary + "\n\n" + render_table(["测试组", "用例数", "证据"], rows or [["-", "-", "-"]])


def render_coverage_claim(data: dict[str, Any]) -> str:
    """Render D-20 coverage claim details."""

    return "\n\n".join(
        [
            render_key_value_bullets(
                [
                    ("Allowed", stringify(data.get("allowed"))),
                    ("Coverage Scope", stringify(data.get("coverage_scope"))),
                ]
            ),
            "### Blocking Reasons\n\n" + render_bullets(as_list(data.get("blocking_reasons"))),
            "### Uncovered Sub-capabilities\n\n" + render_bullets(as_list(data.get("uncovered_sub_capabilities"))),
            "### Unclosed Assertion Points\n\n" + render_bullets(as_list(data.get("unclosed_assertion_points"))),
            "### Unstandardized Fixtures\n\n" + render_bullets(as_list(data.get("unstandardized_fixtures"))),
        ]
    )


def render_testability_summary(spec: dict[str, Any]) -> str:
    """Render feature-level testability summary bullets."""

    return render_key_value_bullets(
        [
            ("testability_status", stringify(spec.get("testability_status"))),
            ("oracle_completeness", stringify(spec.get("oracle_completeness"))),
            ("fixture_readiness", stringify(spec.get("fixture_readiness"))),
            ("test_case_group_count", stringify(spec.get("test_case_group_count"))),
            ("coverage_claim_allowed", stringify(spec.get("coverage_claim_allowed"))),
        ]
    )


def render_feature_card(template_text: str, spec: dict[str, Any], state_lookup: dict[str, dict[str, Any]]) -> str:
    """Render one feature spec card."""

    function_id = str(spec.get("function_id", ""))
    function_name = str(spec.get("function_name", ""))
    state = state_lookup.get(function_id) or {}
    verification_mapping = {
        "feature_state": state.get("state", state.get("status", "")),
        "source": state.get("source", as_dict(state.get("metadata")).get("source", "")),
        "verification_refs": as_list(spec.get("verification_refs")),
    }

    return render_template(
        template_text,
        {
            "function_id": function_id,
            "function_name": function_name,
            "basic_info": render_key_value_bullets(
                [
                    ("Layer", stringify(spec.get("layer"))),
                    ("Runtime Layer", stringify(spec.get("runtime_layer"))),
                    ("Domain", stringify(spec.get("domain_code"))),
                    ("Module", stringify(spec.get("module_code"))),
                    ("状态", stringify(spec.get("status"))),
                    ("规格卡路径", stringify(spec.get("deliverable_path"))),
                ]
            ),
            "function_summary": stringify(spec.get("summary")) or "(无摘要)",
            "function_identifier": render_key_value_bullets(
                [
                    ("Function ID", function_id),
                    ("Function Name", function_name),
                ]
            )
            + "\n\n### Entry Point\n\n"
            + render_entry_point(as_dict(spec.get("entry_point"))),
            "input_spec": render_parameters(as_dict(spec.get("input_spec"))),
            "preconditions": render_records(as_list(spec.get("preconditions"))),
            "success_output": render_json_block(spec.get("success_output")),
            "error_cases": render_records(as_list(spec.get("error_cases"))),
            "boundary_cases": render_records(as_list(spec.get("boundary_cases"))),
            "postconditions": render_records(as_list(spec.get("postconditions"))),
            "side_effects": render_records(as_list(spec.get("side_effects"))),
            "quality_attributes": render_json_block(spec.get("quality_attributes")),
            "dependencies": render_dependencies(as_dict(spec.get("dependencies"))),
            "implementation_mapping": render_implementation_mapping(as_dict(spec.get("implementation_mapping"))),
            "d17_oracle": render_key_value_bullets([("Completeness", stringify(spec.get("oracle_completeness")))])
            + "\n\n"
            + render_sub_item_table(as_dict(spec.get("d17_oracle")), ["子项", "名称", "状态", "证据"]),
            "d18_fixture": render_key_value_bullets([("Completeness", stringify(spec.get("fixture_readiness")))])
            + "\n\n"
            + render_sub_item_table(as_dict(spec.get("d18_fixture")), ["子项", "名称", "状态", "证据"]),
            "d19_test_groups": render_test_groups(as_dict(spec.get("d19_test_groups"))),
            "d20_coverage_claim": render_coverage_claim(as_dict(spec.get("d20_coverage_claim"))),
            "testability_summary": render_testability_summary(spec),
            "verification_mapping": render_json_block(verification_mapping),
            "evidence_refs": render_bullets(as_list(spec.get("evidence_refs"))),
        },
    )


def main() -> int:
    """Render feature index and cards."""

    args = parse_args()
    context = as_dict(load_json(args.context))
    payload = as_dict(load_json(args.payload))
    status = str(payload.get("status", "success"))

    if status == "failed":
        result = build_result(status="failed", errors=["cannot render feature deliverables from failed payload"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    project_path = Path(str(context.get("project_path", ""))).expanduser().resolve()
    if not project_path.exists():
        result = build_result(status="failed", errors=[f"project path does not exist: {project_path}"])
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    feature_specs = with_deliverable_paths(choose_registry(payload, context, "feature_spec_registry"))
    feature_states = choose_registry(payload, context, "feature_state_registry")
    state_lookup = {
        str(item.get("feature_id") or item.get("object_id") or item.get("function_id")): item
        for item in feature_states
        if str(item.get("feature_id") or item.get("object_id") or item.get("function_id"))
    }

    deliverables_dir = ensure_deliverables_dir(project_path)
    index_path = deliverables_dir / "03-feature-spec-index.md"
    cards_dir = deliverables_dir / "04-feature-specs"
    cards_dir.mkdir(parents=True, exist_ok=True)

    index_template = read_template(Path(__file__).resolve().parents[1] / "assets" / "feature-spec-index-template.md")
    card_template = read_template(Path(__file__).resolve().parents[1] / "assets" / "feature-spec-card-template.md")

    feature_rows = [
        [
            stringify(item.get("function_id")),
            stringify(item.get("function_name")),
            stringify(item.get("domain_code")),
            stringify(item.get("module_code")),
            stringify(as_dict(item.get("entry_point")).get("type")),
            stringify(as_dict(item.get("entry_point")).get("path")),
            stringify(item.get("runtime_layer")),
            stringify(item.get("status")),
            stringify(item.get("testability_status")),
            stringify(item.get("oracle_completeness")),
            stringify(item.get("fixture_readiness")),
            stringify(item.get("test_case_group_count")),
            stringify(item.get("coverage_claim_allowed")),
            str(
                len(as_list(as_dict(item.get("dependencies")).get("upstream")))
                + len(as_list(as_dict(item.get("dependencies")).get("downstream")))
                + len(as_list(as_dict(item.get("dependencies")).get("external")))
                + len(as_list(as_dict(item.get("dependencies")).get("data_objects")))
            ),
            str(count_mapping_items(as_dict(item.get("implementation_mapping")))),
            stringify(item.get("deliverable_path")),
            ", ".join(as_list(item.get("evidence_refs"))),
        ]
        for item in feature_specs
    ]
    state_rows = [
        [
            stringify(item.get("feature_id", item.get("object_id"))),
            stringify(item.get("state", item.get("status"))),
            stringify(item.get("source", as_dict(item.get("metadata")).get("source"))),
            stringify(item.get("description")),
        ]
        for item in feature_states
    ]

    index_content = render_template(
        index_template,
        {
            "feature_spec_table": render_table(
                [
                    "Function ID",
                    "名称",
                    "Domain",
                    "Module",
                    "Entry Type",
                    "Entry Surface",
                    "Runtime Layer",
                    "状态",
                    "testability_status",
                    "oracle_completeness",
                    "fixture_readiness",
                    "test_case_group_count",
                    "coverage_claim_allowed",
                    "依赖数",
                    "实现锚点数",
                    "规格卡路径",
                    "证据",
                ],
                feature_rows or [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]],
            ),
            "feature_state_table": render_table(
                ["Feature ID", "状态", "来源", "说明"],
                state_rows or [["-", "-", "-", "-"]],
            ),
            "coverage_summary": render_bullets(
                [
                    f"Feature count: {len(feature_specs)}",
                    f"Features with runtime_layer: {len([item for item in feature_specs if item.get('runtime_layer')])}",
                    f"Features with dependencies: {len([item for item in feature_specs if as_dict(item.get('dependencies'))])}",
                    f"Features with implementation mapping: {len([item for item in feature_specs if count_mapping_items(as_dict(item.get('implementation_mapping'))) > 0])}",
                ]
            ),
            "testability_summary": render_bullets(
                [
                    f"test_ready features: {len([item for item in feature_specs if item.get('testability_status') == 'test_ready'])}",
                    f"blocked features: {len([item for item in feature_specs if item.get('testability_status') == 'blocked'])}",
                    f"coverage_claim_allowed=yes: {len([item for item in feature_specs if item.get('coverage_claim_allowed') == 'yes'])}",
                ]
            ),
        },
    )
    index_path.write_text(index_content.rstrip() + "\n", encoding="utf-8")

    for spec in feature_specs:
        function_id = str(spec.get("function_id", "")).strip()
        if not function_id:
            continue
        card_path = project_path / str(spec.get("deliverable_path", "")).strip()
        card_path.parent.mkdir(parents=True, exist_ok=True)
        card_content = render_feature_card(card_template, spec, state_lookup)
        card_path.write_text(card_content.rstrip() + "\n", encoding="utf-8")

    manifest = as_dict(as_dict(payload.get("context_writes")).get("deliverable_manifest")) or as_dict(context.get("deliverable_manifest"))
    updated_manifest = mark_deliverables_completed(manifest, ["DLV-003", "DLV-004"])
    result = build_result(
        status=status,
        context_writes={
            "deliverable_manifest": updated_manifest,
            "feature_spec_registry": feature_specs,
        },
        metadata={
            "deliverables": [
                {
                    "deliverable_id": "DLV-003",
                    "deliverable_type": "feature_spec_index",
                    "path": ".review/deliverables/03-feature-spec-index.md",
                    "status": "completed",
                },
                {
                    "deliverable_id": "DLV-004",
                    "deliverable_type": "feature_spec_cards",
                    "path": ".review/deliverables/04-feature-specs/",
                    "status": "completed",
                },
            ],
            "card_count": len([item for item in feature_specs if item.get("function_id")]),
        },
        errors=[str(item) for item in as_list(payload.get("errors")) if str(item)],
    )
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
