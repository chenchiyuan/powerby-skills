from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_pb_review_has_no_backend_llm_bridge() -> None:
    """pb-review should not ship an internal backend LLM bridge."""

    assert not (REPO_ROOT / "skills/pb-review/scripts/llm_client.py").exists()
    assert not (REPO_ROOT / "skills/pb-review/scripts/skill_contract_runner.py").exists()


def test_abstract_pb_review_skills_have_no_runner_script() -> None:
    """Abstract reasoning must stay in the host skill, not scripts/run.py."""

    abstract_skills = [
        "pb-review-product-reconstructor",
        "pb-review-feature-reconstructor",
        "pb-review-relation-builder",
        "pb-review-gap-analyzer",
    ]
    for skill_name in abstract_skills:
        assert not (REPO_ROOT / "skills" / skill_name / "scripts" / "run.py").exists()


def test_abstract_pb_review_skills_ship_renderer_scripts() -> None:
    """Abstract skills should provide deterministic renderers for deliverable materialization."""

    required_scripts = [
        "skills/pb-review-product-reconstructor/scripts/render_catalog.py",
        "skills/pb-review-feature-reconstructor/scripts/render_feature_deliverables.py",
        "skills/pb-review-relation-builder/scripts/render_traceability_matrix.py",
        "skills/pb-review-gap-analyzer/scripts/render_gap_analysis.py",
    ]
    for relative_path in required_scripts:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_pb_review_ships_testability_renderers_and_schemas() -> None:
    """010 upgrade should ship deterministic testability renderers and shared schemas."""

    required_files = [
        "skills/pb-review/scripts/render_testability_scorecard.py",
        "skills/pb-review/scripts/render_test_case_index.py",
        "skills/pb-review/scripts/render_fixture_contract.py",
        "skills/pb-review/scripts/render_oracle_matrix.py",
        "skills/pb-review/scripts/testability_metrics.py",
        "skills/pb-review/schemas/d17-oracle-schema.md",
        "skills/pb-review/schemas/d18-fixture-schema.md",
        "skills/pb-review/schemas/d19-test-groups-schema.md",
        "skills/pb-review/schemas/d20-coverage-claim-schema.md",
        "skills/pb-review/schemas/testability-status-rules.md",
        "skills/pb-review/schemas/testability-score-formula.md",
        "skills/pb-review/schemas/gap-severity-rules.md",
        "skills/pb-review/schemas/entry-surface-types.md",
    ]
    for relative_path in required_files:
        assert (REPO_ROOT / relative_path).exists(), relative_path
