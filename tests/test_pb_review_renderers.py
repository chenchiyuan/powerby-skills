from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PB_REVIEW_SCRIPT_DIR = REPO_ROOT / "skills" / "pb-review" / "scripts"
if str(PB_REVIEW_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PB_REVIEW_SCRIPT_DIR))

from review_context import ReviewContextStore
from review_runner import persist_step_output


def run_renderer(
    script_relative_path: str,
    *,
    tmp_path: Path,
    context: dict,
    payload: dict,
) -> dict:
    """Execute a renderer script and return its JSON output."""

    context_path = tmp_path / "context.json"
    payload_path = tmp_path / "payload.json"
    output_path = tmp_path / "output.json"
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    subprocess.run(
        [
            "python3",
            str(REPO_ROOT / script_relative_path),
            "--context",
            str(context_path),
            "--payload",
            str(payload_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )

    return json.loads(output_path.read_text(encoding="utf-8"))


def run_context_renderer(
    script_relative_path: str,
    *,
    tmp_path: Path,
    context: dict,
    parameters: dict | None = None,
) -> dict:
    """Execute a deterministic renderer that reads only context + parameters."""

    context_path = tmp_path / "context.json"
    params_path = tmp_path / "params.json"
    output_path = tmp_path / "output.json"
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    params_path.write_text(json.dumps(parameters or {}, ensure_ascii=False, indent=2), encoding="utf-8")

    subprocess.run(
        [
            "python3",
            str(REPO_ROOT / script_relative_path),
            "--context",
            str(context_path),
            "--parameters",
            str(params_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )

    return json.loads(output_path.read_text(encoding="utf-8"))


def manifest_for(*items: tuple[str, str, str, str]) -> dict:
    """Build a minimal deliverable manifest."""

    return {
        "version": "2.0",
        "required_deliverables": [
            {
                "deliverable_id": deliverable_id,
                "deliverable_type": deliverable_type,
                "path": path,
                "producer_skill": producer_skill,
                "status": "pending",
            }
            for deliverable_id, deliverable_type, path, producer_skill in items
        ],
    }


def test_product_catalog_renderer_writes_catalog_and_manifest(tmp_path: Path) -> None:
    """Product renderer should materialize the catalog markdown file."""

    project_root = tmp_path / "repo"
    project_root.mkdir()
    context = {
        "project_path": str(project_root),
        "project_metadata": {},
        "deliverable_manifest": manifest_for(
            ("DLV-002", "product_catalog", ".review/deliverables/02-product-catalog.md", "pb-review-product-reconstructor"),
        ),
    }
    payload = {
        "status": "partial",
        "objects": [
            {
                "object_id": "goal-001",
                "object_type": "goal",
                "name": "完成需求还原",
                "description": "输出清晰的功能规格卡",
                "evidence_refs": ["ev-001"],
                "confidence": "explicit",
            },
            {
                "object_id": "role-001",
                "object_type": "role",
                "name": "产品评审者",
                "description": "查看 review 交付物",
                "evidence_refs": ["ev-002"],
            },
        ],
        "gaps": [{"gap_type": "missing_evidence", "description": "未提供约束文档"}],
        "errors": ["partial evidence"],
        "context_writes": {},
        "metadata": {
            "product_catalog_completeness": {
                "goal_quantifiable_rate": 80,
                "scenario_completeness_rate": 75,
                "constraint_traceability_rate": 60,
                "total_score": 72,
                "grade": "C",
            }
        },
    }

    result = run_renderer(
        "skills/pb-review-product-reconstructor/scripts/render_catalog.py",
        tmp_path=tmp_path,
        context=context,
        payload=payload,
    )

    deliverable = project_root / ".review" / "deliverables" / "02-product-catalog.md"
    assert result["status"] == "partial"
    assert deliverable.exists()
    text = deliverable.read_text(encoding="utf-8")
    assert "完成需求还原" in text
    assert "partial evidence" in text
    assert "total_score: 72" in text
    manifest = result["context_writes"]["deliverable_manifest"]["required_deliverables"]
    assert manifest[0]["status"] == "completed"


def test_feature_renderer_writes_index_and_cards(tmp_path: Path) -> None:
    """Feature renderer should create both index and feature cards."""

    project_root = tmp_path / "repo"
    project_root.mkdir()
    context = {
        "project_path": str(project_root),
        "deliverable_manifest": manifest_for(
            ("DLV-003", "feature_spec_index", ".review/deliverables/03-feature-spec-index.md", "pb-review-feature-reconstructor"),
            ("DLV-004", "feature_spec_cards", ".review/deliverables/04-feature-specs/", "pb-review-feature-reconstructor"),
        ),
    }
    payload = {
        "status": "success",
        "context_writes": {
            "feature_spec_registry": [
                {
                    "function_id": "OPR-AS-SLCT-001",
                    "function_name": "盘后选股",
                    "layer": "operation",
                    "domain_code": "AS",
                    "module_code": "SLCT",
                    "status": "implemented",
                    "summary": "整合多个信号输出候选股票",
                    "entry_point": {
                        "type": "cli",
                        "path": "archer/apps/ashare/management/commands/select_stocks.py",
                        "command": "python manage.py select_stocks",
                    },
                    "input_spec": {
                        "parameters": [
                            {
                                "name": "date",
                                "type": "string",
                                "required": False,
                                "default": "最近交易日",
                                "constraints": ["必须是交易日"],
                                "example": "2026-03-27",
                            }
                        ],
                        "schema": {"type": "object", "properties": {"date": {"type": "string"}}},
                    },
                    "preconditions": [{"id": "PRE-001", "description": "日线数据已同步"}],
                    "success_output": {"stdout": {"type": "table"}},
                    "error_cases": [{"id": "ERR-001", "description": "日期非法"}],
                    "boundary_cases": [{"id": "BND-001", "description": "未来日期拒绝"}],
                    "postconditions": [{"id": "POST-001", "description": "生成候选列表"}],
                    "side_effects": [{"id": "SIDE-001", "description": "可能写出 CSV"}],
                    "quality_attributes": {"performance": "daily batch"},
                    "d17_oracle": {
                        "completeness": 78,
                        "sub_items": [
                            {"id": "D17-1", "name": "成功输出 Schema", "status": "defined", "evidence_refs": ["ev-201"]},
                            {"id": "D17-9", "name": "业务规则定义", "status": "missing", "evidence_refs": []},
                        ],
                    },
                    "d18_fixture": {
                        "completeness": 50,
                        "sub_items": [
                            {"id": "D18-1", "name": "最小数据集", "status": "defined", "evidence_refs": ["ev-202"]},
                            {"id": "D18-3", "name": "外部依赖 Mock 策略", "status": "missing", "evidence_refs": []},
                        ],
                    },
                    "d19_test_groups": {
                        "count": 3,
                        "groups": [
                            {"name": "正向功能测试", "test_count": 4, "evidence_refs": ["ev-203"]},
                            {"name": "边界值测试", "test_count": 2, "evidence_refs": ["ev-204"]},
                        ],
                    },
                    "d20_coverage_claim": {
                        "allowed": "no",
                        "coverage_scope": None,
                        "blocking_reasons": ["oracle_completeness < 90"],
                        "uncovered_sub_capabilities": ["边界条件未覆盖"],
                        "unclosed_assertion_points": ["D17-9 业务规则定义缺失"],
                        "unstandardized_fixtures": ["D18-3 Mock策略未定义"],
                    },
                    "testability_status": "partial",
                    "oracle_completeness": 78,
                    "fixture_readiness": 50,
                    "test_case_group_count": 3,
                    "coverage_claim_allowed": "no",
                    "verification_refs": ["tests/test_select_stocks.py"],
                    "evidence_refs": ["ev-101"],
                }
            ],
            "feature_state_registry": [
                {
                    "feature_id": "OPR-AS-SLCT-001",
                    "state": "implemented",
                    "source": "both",
                    "description": "文档与代码均存在",
                }
            ],
        },
    }

    result = run_renderer(
        "skills/pb-review-feature-reconstructor/scripts/render_feature_deliverables.py",
        tmp_path=tmp_path,
        context=context,
        payload=payload,
    )

    index_path = project_root / ".review" / "deliverables" / "03-feature-spec-index.md"
    card_path = project_root / ".review" / "deliverables" / "04-feature-specs" / "OPR-AS-SLCT-001.md"
    assert index_path.exists()
    assert card_path.exists()
    index_text = index_path.read_text(encoding="utf-8")
    assert "盘后选股" in index_text
    assert "testability_status" in index_text
    card_text = card_path.read_text(encoding="utf-8")
    assert "## D-17 Test Oracle" in card_text
    assert "## D-20 Coverage Claim" in card_text
    assert "tests/test_select_stocks.py" in card_text
    assert result["context_writes"]["feature_spec_registry"][0]["deliverable_path"].endswith("OPR-AS-SLCT-001.md")
    manifest = result["context_writes"]["deliverable_manifest"]["required_deliverables"]
    assert all(item["status"] == "completed" for item in manifest)


def test_traceability_renderer_writes_matrix(tmp_path: Path) -> None:
    """Relation renderer should materialize the matrix markdown file."""

    project_root = tmp_path / "repo"
    project_root.mkdir()
    context = {
        "project_path": str(project_root),
        "deliverable_manifest": manifest_for(
            ("DLV-005", "traceability_matrix", ".review/deliverables/05-traceability-matrix.md", "pb-review-relation-builder"),
        ),
    }
    payload = {
        "status": "success",
        "context_writes": {
            "traceability_matrix": {
                "goal_rows": [
                    {
                        "goal_id": "goal-001",
                        "goal_name": "完成需求还原",
                        "supporting_features": ["OPR-AS-SLCT-001"],
                        "coverage_status": "covered",
                        "evidence_refs": ["ev-201"],
                    }
                ],
                "rule_rows": [
                    {
                        "rule_id": "rule-001",
                        "rule_name": "必须基于最新数据",
                        "constrained_features": ["OPR-AS-SLCT-001"],
                        "coverage_status": "covered",
                        "evidence_refs": ["ev-202"],
                    }
                ],
                "coverage_stats": {
                    "goal_coverage_rate": 1.0,
                    "feature_traceability_rate": 1.0,
                    "test_traceability_rate": 1.0,
                    "rule_negative_test_rate": 1.0,
                },
                "feature_test_rows": [
                    {
                        "function_id": "OPR-AS-SLCT-001",
                        "test_groups": [{"group_name": "正向功能测试", "test_count": 3}],
                        "coverage_status": "covered",
                        "evidence_refs": ["ev-203"],
                    }
                ],
                "rule_negative_test_rows": [
                    {
                        "rule_id": "rule-001",
                        "rule_name": "必须基于最新数据",
                        "negative_tests": [{"test_file": "tests/test_select_stocks.py", "test_function": "test_invalid_date"}],
                        "coverage_status": "covered",
                        "evidence_refs": ["ev-204"],
                    }
                ],
            }
        },
    }

    result = run_renderer(
        "skills/pb-review-relation-builder/scripts/render_traceability_matrix.py",
        tmp_path=tmp_path,
        context=context,
        payload=payload,
    )

    matrix_path = project_root / ".review" / "deliverables" / "05-traceability-matrix.md"
    assert matrix_path.exists()
    text = matrix_path.read_text(encoding="utf-8")
    assert "完成需求还原" in text
    assert "Feature -> Test Case Groups" in text
    assert "Goal coverage rate: 1.0" in text
    manifest = result["context_writes"]["deliverable_manifest"]["required_deliverables"]
    assert manifest[0]["status"] == "completed"


def test_gap_renderer_writes_analysis(tmp_path: Path) -> None:
    """Gap renderer should materialize difference, conflict, and gap tables."""

    project_root = tmp_path / "repo"
    project_root.mkdir()
    context = {
        "project_path": str(project_root),
        "deliverable_manifest": manifest_for(
            ("DLV-006", "gap_analysis", ".review/deliverables/06-gap-analysis.md", "pb-review-gap-analyzer"),
        ),
        "conflict_registry": [],
    }
    payload = {
        "status": "success",
        "conflicts": [
            {
                "conflict_id": "conflict-001",
                "conflict_type": "doc_code",
                "description": "文档要求 CSV 导出，代码未实现",
                "priority_winner": "ev-301",
                "resolution": "preserved",
            }
        ],
        "gaps": [
            {
                "gap_id": "gap-001",
                "gap_type": "missing_relation",
                "description": "存在无功能支撑的目标",
                "gap_severity": "Critical",
                "severity": "critical",
                "context": {"goal_id": "goal-001"},
            }
        ],
        "context_writes": {
            "difference_registry": [
                {
                    "difference_id": "diff-001",
                    "difference_type": "doc_without_code",
                    "subject_id": "OPR-AS-SLCT-001",
                    "description": "文档声明 CSV 导出但代码缺失",
                    "severity": "major",
                    "evidence_refs": ["ev-301", "ev-302"],
                }
            ]
        },
    }

    result = run_renderer(
        "skills/pb-review-gap-analyzer/scripts/render_gap_analysis.py",
        tmp_path=tmp_path,
        context=context,
        payload=payload,
    )

    gap_path = project_root / ".review" / "deliverables" / "06-gap-analysis.md"
    assert gap_path.exists()
    text = gap_path.read_text(encoding="utf-8")
    assert "doc_without_code" in text
    assert "Gap Severity" in text
    assert "Critical gaps: 1" in text
    manifest = result["context_writes"]["deliverable_manifest"]["required_deliverables"]
    assert manifest[0]["status"] == "completed"


def test_testability_renderers_write_new_deliverables(tmp_path: Path) -> None:
    """Step 13~16 renderers should generate the four testability deliverables."""

    project_root = tmp_path / "repo"
    project_root.mkdir()
    context = {
        "project_path": str(project_root),
        "deliverable_manifest": manifest_for(
            ("DLV-011", "testability_scorecard", ".review/deliverables/11-testability-scorecard.md", "pb-review"),
            ("DLV-012", "test_case_index", ".review/deliverables/12-test-case-index.md", "pb-review"),
            ("DLV-013", "fixture_contract", ".review/deliverables/13-test-fixture-contract.md", "pb-review"),
            ("DLV-014", "oracle_matrix", ".review/deliverables/14-test-oracle-matrix.md", "pb-review"),
        ),
        "feature_spec_registry": [
            {
                "function_id": "OPR-AS-SLCT-001",
                "function_name": "盘后选股",
                "testability_status": "partial",
                "oracle_completeness": 80,
                "fixture_readiness": 60,
                "test_case_group_count": 3,
                "coverage_claim_allowed": "no",
                "d17_oracle": {
                    "sub_items": [
                        {"id": "D17-1", "name": "成功输出 Schema", "status": "defined"},
                        {"id": "D17-9", "name": "业务规则定义", "status": "missing"},
                    ]
                },
                "d18_fixture": {
                    "sub_items": [
                        {"id": "D18-1", "name": "最小数据集", "status": "defined"},
                        {"id": "D18-3", "name": "外部依赖 Mock 策略", "status": "missing"},
                    ]
                },
                "d19_test_groups": {
                    "groups": [{"name": "正向功能测试", "test_count": 3, "evidence_refs": ["ev-401"]}]
                },
            }
        ],
        "dependency_registry": [
            {
                "source_function_id": "OPR-AS-SLCT-001",
                "dependency_name": "quote-api",
                "mock_strategy": "stub",
            }
        ],
        "gap_registry": [{"gap_type": "missing_oracle", "description": "业务规则未闭合", "gap_severity": "Major"}],
        "traceability_matrix": {
            "feature_test_rows": [{"function_id": "OPR-AS-SLCT-001", "coverage_status": "covered"}],
            "rule_negative_test_rows": [{"rule_id": "rule-001", "coverage_status": "covered"}],
        },
    }

    scorecard = run_context_renderer(
        "skills/pb-review/scripts/render_testability_scorecard.py",
        tmp_path=tmp_path,
        context=context,
    )
    case_index = run_context_renderer(
        "skills/pb-review/scripts/render_test_case_index.py",
        tmp_path=tmp_path,
        context=context,
    )
    fixture = run_context_renderer(
        "skills/pb-review/scripts/render_fixture_contract.py",
        tmp_path=tmp_path,
        context=context,
    )
    oracle = run_context_renderer(
        "skills/pb-review/scripts/render_oracle_matrix.py",
        tmp_path=tmp_path,
        context=context,
    )

    assert scorecard["metadata"]["deliverables"][0]["deliverable_id"] == "DLV-011"
    assert case_index["metadata"]["deliverables"][0]["deliverable_id"] == "DLV-012"
    assert fixture["metadata"]["deliverables"][0]["deliverable_id"] == "DLV-013"
    assert oracle["metadata"]["deliverables"][0]["deliverable_id"] == "DLV-014"
    assert (project_root / ".review" / "deliverables" / "11-testability-scorecard.md").exists()
    assert (project_root / ".review" / "deliverables" / "12-test-case-index.md").exists()
    assert (project_root / ".review" / "deliverables" / "13-test-fixture-contract.md").exists()
    assert (project_root / ".review" / "deliverables" / "14-test-oracle-matrix.md").exists()


def test_testability_scorecard_uses_gap_based_closure_and_atomicity(tmp_path: Path) -> None:
    """Scorecard should derive M-01 from missing-feature gaps and M-02 from atomicity evidence."""

    project_root = tmp_path / "repo"
    project_root.mkdir()
    context = {
        "project_path": str(project_root),
        "deliverable_manifest": manifest_for(
            ("DLV-011", "testability_scorecard", ".review/deliverables/11-testability-scorecard.md", "pb-review"),
        ),
        "feature_spec_registry": [
            {
                "function_id": "OPR-001",
                "function_name": "单一入口功能",
                "entry_surface_count": 1,
                "oracle_completeness": 90,
                "fixture_readiness": 90,
                "test_case_group_count": 5,
                "coverage_claim_allowed": "yes",
            },
            {
                "function_id": "OPR-002",
                "function_name": "复合入口功能",
                "entry_surface_count": 2,
                "oracle_completeness": 90,
                "fixture_readiness": 90,
                "test_case_group_count": 5,
                "coverage_claim_allowed": "no",
            },
        ],
        "gap_registry": [
            {
                "gap_id": "gap-001",
                "gap_type": "missing_feature",
                "description": "存在未建模入口",
                "context": {"entry_surface": "api:/v1/orders/export"},
            }
        ],
        "traceability_matrix": {
            "feature_test_rows": [{"function_id": "OPR-001", "coverage_status": "covered"}],
            "rule_negative_test_rows": [],
        },
    }

    run_context_renderer(
        "skills/pb-review/scripts/render_testability_scorecard.py",
        tmp_path=tmp_path,
        context=context,
    )

    text = (project_root / ".review" / "deliverables" / "11-testability-scorecard.md").read_text(encoding="utf-8")
    assert "| M-01 | 66.67 | 100.0 | 33.33 |" in text
    assert "| M-02 | 50.0 | 95.0 | 45.0 |" in text


def test_persist_step_output_tracks_report_paths_relative_to_review_dir(tmp_path: Path) -> None:
    """Checkpoint writes should stay relative even when a step returns an absolute report path."""

    project_root = tmp_path / "repo"
    project_root.mkdir()
    store = ReviewContextStore(str(project_root), "full_project", review_id="review-test")
    store.ensure_dirs()
    absolute_report_path = project_root / ".review" / "deliverables" / "07-review-report.md"

    writes = persist_step_output(
        store,
        {
            "status": "success",
            "errors": [],
            "metadata": {"report_path": str(absolute_report_path)},
        },
    )

    assert "deliverables/07-review-report.md" in writes
    assert all(not item.startswith(str(project_root)) for item in writes)
