from pathlib import Path
import json
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_pb_review_deliverable_standard_exists() -> None:
    """pb-review should ship a canonical deliverable standard document."""

    standard_path = REPO_ROOT / "docs/review/pb-review-deliverable-standard.md"
    text = standard_path.read_text(encoding="utf-8")

    assert standard_path.exists()
    assert "功能规格卡是原子交付单元" in text
    assert ".review/deliverables/04-feature-specs/{function_id}.md" in text
    assert ".review/deliverables/11-testability-scorecard.md" in text
    assert "feature_spec_registry" in text


def test_feature_reconstructor_references_feature_spec_standard() -> None:
    """Feature reconstruction must be explicitly aligned to the feature spec standard."""

    skill_text = (REPO_ROOT / "skills/pb-review-feature-reconstructor/SKILL.md").read_text(encoding="utf-8")
    report_skill_text = (REPO_ROOT / "skills/pb-review-report-composer/SKILL.md").read_text(encoding="utf-8")

    assert "feature-specification-standard.md" in skill_text
    assert "03-feature-spec-index.md" in skill_text
    assert "04-feature-specs/{function_id}.md" in skill_text
    assert "D-17" in skill_text
    assert "最终报告不是唯一交付物" in report_skill_text


def test_abstract_pb_review_skills_ship_deliverable_templates() -> None:
    """Reference-driven review skills should ship concrete template assets."""

    required_assets = [
        "skills/pb-review/assets/testability-scorecard-template.md",
        "skills/pb-review/assets/test-case-index-template.md",
        "skills/pb-review/assets/fixture-contract-template.md",
        "skills/pb-review/assets/oracle-matrix-template.md",
        "skills/pb-review-project-scope/assets/system-context-template.md",
        "skills/pb-review-product-reconstructor/assets/product-catalog-template.md",
        "skills/pb-review-feature-reconstructor/assets/feature-spec-index-template.md",
        "skills/pb-review-feature-reconstructor/assets/feature-spec-card-template.md",
        "skills/pb-review-relation-builder/assets/traceability-matrix-template.md",
        "skills/pb-review-gap-analyzer/assets/gap-analysis-template.md",
    ]
    for relative_path in required_assets:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_report_composer_uses_template_placeholders() -> None:
    """The report composer should consume its template instead of hardcoding the whole layout."""

    template_text = (REPO_ROOT / "skills/pb-review-report-composer/assets/report-template.md").read_text(encoding="utf-8")
    script_text = (REPO_ROOT / "skills/pb-review-report-composer/scripts/run.py").read_text(encoding="utf-8")

    assert "{{project_overview}}" in template_text
    assert "{{feature_spec_table}}" in template_text
    assert "{{testability_summary}}" in template_text
    assert "render_template(" in script_text


def test_report_composer_allows_pending_testability_deliverables(tmp_path: Path) -> None:
    """The Step 12 report should not be blocked by Step 13~16 pending outputs."""

    project_root = tmp_path / "repo"
    deliverables_dir = project_root / ".review" / "deliverables" / "04-feature-specs"
    deliverables_dir.mkdir(parents=True)
    (deliverables_dir / "OPR-AS-SLCT-001.md").write_text("# Card\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "01-system-context.md").write_text("# System\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "02-product-catalog.md").write_text("# Product\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "03-feature-spec-index.md").write_text("# Index\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "05-traceability-matrix.md").write_text("# Trace\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "06-gap-analysis.md").write_text("# Gap\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "08-architecture-layered.md").write_text("# Arch\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "09-dependency-matrix.md").write_text("# Dep\n", encoding="utf-8")
    (project_root / ".review" / "deliverables" / "10-data-flow.md").write_text("# Flow\n", encoding="utf-8")

    context = {
        "review_id": "review-demo",
        "project_path": str(project_root),
        "scope": "full_project",
        "project_metadata": {"project_name": "demo", "project_type": "python-repo", "file_count": 1},
        "object_registry": [],
        "feature_spec_registry": [{"function_id": "OPR-AS-SLCT-001", "testability_status": "partial"}],
        "feature_state_registry": [],
        "dependency_registry": [],
        "implementation_registry": [],
        "traceability_matrix": {"goal_rows": [], "rule_rows": [], "coverage_stats": {}},
        "relation_registry": [],
        "conflict_registry": [],
        "difference_registry": [],
        "gap_registry": [],
        "architecture_registry": {"runtime_layers": [], "critical_paths": []},
        "data_flow_registry": {"data_objects": []},
        "evidence_registry": [],
        "deliverable_manifest": {
            "version": "2.0",
            "required_deliverables": [
                {"deliverable_id": "DLV-001", "deliverable_type": "system_context", "path": ".review/deliverables/01-system-context.md", "producer_skill": "pb-review-project-scope", "status": "completed"},
                {"deliverable_id": "DLV-002", "deliverable_type": "product_catalog", "path": ".review/deliverables/02-product-catalog.md", "producer_skill": "pb-review-product-reconstructor", "status": "completed"},
                {"deliverable_id": "DLV-003", "deliverable_type": "feature_spec_index", "path": ".review/deliverables/03-feature-spec-index.md", "producer_skill": "pb-review-feature-reconstructor", "status": "completed"},
                {"deliverable_id": "DLV-004", "deliverable_type": "feature_spec_cards", "path": ".review/deliverables/04-feature-specs/", "producer_skill": "pb-review-feature-reconstructor", "status": "completed"},
                {"deliverable_id": "DLV-005", "deliverable_type": "traceability_matrix", "path": ".review/deliverables/05-traceability-matrix.md", "producer_skill": "pb-review-relation-builder", "status": "completed"},
                {"deliverable_id": "DLV-006", "deliverable_type": "gap_analysis", "path": ".review/deliverables/06-gap-analysis.md", "producer_skill": "pb-review-gap-analyzer", "status": "completed"},
                {"deliverable_id": "DLV-007", "deliverable_type": "review_report", "path": ".review/deliverables/07-review-report.md", "producer_skill": "pb-review-report-composer", "status": "pending"},
                {"deliverable_id": "DLV-008", "deliverable_type": "architecture_layered", "path": ".review/deliverables/08-architecture-layered.md", "producer_skill": "pb-review-architecture-builder", "status": "completed"},
                {"deliverable_id": "DLV-009", "deliverable_type": "dependency_matrix", "path": ".review/deliverables/09-dependency-matrix.md", "producer_skill": "pb-review-dependency-reconstructor", "status": "completed"},
                {"deliverable_id": "DLV-010", "deliverable_type": "data_flow", "path": ".review/deliverables/10-data-flow.md", "producer_skill": "pb-review-data-flow-builder", "status": "completed"},
                {"deliverable_id": "DLV-011", "deliverable_type": "testability_scorecard", "path": ".review/deliverables/11-testability-scorecard.md", "producer_skill": "pb-review", "status": "pending"},
                {"deliverable_id": "DLV-012", "deliverable_type": "test_case_index", "path": ".review/deliverables/12-test-case-index.md", "producer_skill": "pb-review", "status": "pending"},
                {"deliverable_id": "DLV-013", "deliverable_type": "fixture_contract", "path": ".review/deliverables/13-test-fixture-contract.md", "producer_skill": "pb-review", "status": "pending"},
                {"deliverable_id": "DLV-014", "deliverable_type": "oracle_matrix", "path": ".review/deliverables/14-test-oracle-matrix.md", "producer_skill": "pb-review", "status": "pending"},
            ],
        },
    }

    params = {}
    context_path = tmp_path / "context.json"
    params_path = tmp_path / "params.json"
    output_path = tmp_path / "output.json"
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    params_path.write_text(json.dumps(params, ensure_ascii=False, indent=2), encoding="utf-8")

    subprocess.run(
        [
            "python3",
            str(REPO_ROOT / "skills/pb-review-report-composer/scripts/run.py"),
            "--context",
            str(context_path),
            "--parameters",
            str(params_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["status"] == "success"
    assert (project_root / ".review" / "deliverables" / "07-review-report.md").exists()


def test_report_composer_requires_upstream_deliverables(tmp_path: Path) -> None:
    """The final report should fail if mandatory upstream deliverables are missing."""

    project_root = tmp_path / "repo"
    review_dir = project_root / ".review"
    review_dir.mkdir(parents=True)

    context = {
        "review_id": "review-demo",
        "project_path": str(project_root),
        "scope": "full_project",
        "project_metadata": {"project_name": "demo", "project_type": "python-repo", "file_count": 1},
        "object_registry": [],
        "feature_spec_registry": [{"function_id": "OPR-AS-SLCT-001"}],
        "feature_state_registry": [],
        "traceability_matrix": {"goal_rows": [], "rule_rows": [], "coverage_stats": {}},
        "relation_registry": [],
        "conflict_registry": [],
        "difference_registry": [],
        "gap_registry": [],
        "evidence_registry": [],
        "deliverable_manifest": {
            "version": "2.0",
            "required_deliverables": [
                {
                    "deliverable_id": "DLV-004",
                    "deliverable_type": "feature_spec_cards",
                    "path": ".review/deliverables/04-feature-specs/",
                    "producer_skill": "pb-review-feature-reconstructor",
                    "status": "pending",
                },
                {
                    "deliverable_id": "DLV-007",
                    "deliverable_type": "review_report",
                    "path": ".review/deliverables/07-review-report.md",
                    "producer_skill": "pb-review-report-composer",
                    "status": "pending",
                },
            ],
        },
    }
    params = {}
    context_path = tmp_path / "context.json"
    params_path = tmp_path / "params.json"
    output_path = tmp_path / "output.json"
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    params_path.write_text(json.dumps(params, ensure_ascii=False, indent=2), encoding="utf-8")

    subprocess.run(
        [
            "python3",
            str(REPO_ROOT / "skills/pb-review-report-composer/scripts/run.py"),
            "--context",
            str(context_path),
            "--parameters",
            str(params_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["status"] == "failed"
    assert any("DLV-004" in item for item in payload["errors"])
