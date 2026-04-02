from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SECTION_HEADERS = [
    "## Purpose",
    "## Success criteria",
    "## Strategy",
    "## Tools and capability boundaries",
    "## Important facts and constraints",
    "## Workflow",
    "## Output format",
    "## Resources",
    "## Subtask / parallelism guidance",
    "## Examples",
    "## Safety",
]


def load_validate_module():
    """Load the iteration validation script as a Python module for direct testing."""

    script_path = REPO_ROOT / ".github/workflows/scripts/validate-iteration-docs.py"
    spec = spec_from_file_location("validate_iteration_docs", script_path)
    module = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_pb_review_v2_skill_layout_and_resources_exist() -> None:
    """pb-review-v2 should follow the 11-section skill layout and ship required references."""

    skill_dir = REPO_ROOT / "skills/pb-review-v2"
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    assert "compatibility:" in skill_text
    for header in SECTION_HEADERS:
        assert header in skill_text

    expected_resources = [
        "audit-checklist-ref.md",
        "product-checklist.md",
        "spec-checklist.md",
        "arch-checklist.md",
        "plan-checklist.md",
        "impl-checklist.md",
        "decision-table.md",
        "audit-template.md",
    ]
    for resource_name in expected_resources:
        assert (skill_dir / "references" / resource_name).exists(), resource_name

    assert not (skill_dir / "scripts").exists()


def test_pb_review_v2_skill_declares_independent_five_stage_review_contract() -> None:
    """pb-review-v2 should be documented as an independent five-stage reviewer."""

    skill_text = (REPO_ROOT / "skills/pb-review-v2/SKILL.md").read_text(encoding="utf-8")

    assert "独立新增的 review skill" in skill_text
    assert "product / spec / architecture / plan / implementation" in skill_text
    assert "Alignment Summary" in skill_text
    assert "AUTO-FIX" in skill_text
    assert "ASK" in skill_text
    assert "ESCALATED" in skill_text
    assert "docs/asp-review-orchestrator-protocol.md" in skill_text
    assert "powerby-asp-reviewer" in skill_text
    assert "不覆盖或修改现有" in skill_text


def test_pb_review_v2_protocol_and_references_are_complete() -> None:
    """The protocol doc and strategy references should cover loop control and archival paths."""

    protocol_text = (REPO_ROOT / "docs/asp-review-orchestrator-protocol.md").read_text(
        encoding="utf-8"
    )
    decision_text = (
        REPO_ROOT / "skills/pb-review-v2/references/decision-table.md"
    ).read_text(encoding="utf-8")
    template_text = (
        REPO_ROOT / "skills/pb-review-v2/references/audit-template.md"
    ).read_text(encoding="utf-8")

    assert "pb-review-v2" in protocol_text
    assert "reviewer -> fixer -> reviewer" in protocol_text
    assert "plan_logs/" in protocol_text
    assert "impl_logs/" in protocol_text
    assert "round > 3" in protocol_text
    assert "AUTO-FIX / ASK / ESCALATE" in decision_text
    assert "Boil the Lake" in decision_text
    assert "PB Review V2 Audit Report" in template_text
    assert "fix_instructions" in template_text


def test_iteration_014_documents_point_to_pb_review_v2() -> None:
    """014 implementation docs should map the new review system to pb-review-v2."""

    architecture_text = (
        REPO_ROOT / "docs/iterations/014-asp-review-skill-upgrade/architecture.md"
    ).read_text(encoding="utf-8")
    tasks_text = (
        REPO_ROOT / "docs/iterations/014-asp-review-skill-upgrade/tasks.md"
    ).read_text(encoding="utf-8")
    traceability_text = (
        REPO_ROOT / "docs/iterations/014-asp-review-skill-upgrade/traceability-matrix.md"
    ).read_text(encoding="utf-8")

    assert "pb-review-v2" in architecture_text
    assert "skills/pb-review-v2/" in architecture_text
    assert "pb-review-v2" in tasks_text
    assert "skills/pb-review-v2/SKILL.md" in traceability_text


def test_validate_iteration_docs_supports_asp_and_legacy_layouts(tmp_path: Path) -> None:
    """Validation script should accept both ASP and legacy iteration layouts."""

    module = load_validate_module()

    asp_dir = tmp_path / "014-asp-review-skill-upgrade"
    asp_dir.mkdir()
    (asp_dir / "design-brief.md").write_text("# design brief\n", encoding="utf-8")
    (asp_dir / "proposal.md").write_text("# proposal\n", encoding="utf-8")
    (asp_dir / "feature-spec-index.md").write_text("# index\n", encoding="utf-8")
    specs_dir = asp_dir / "feature-specs"
    specs_dir.mkdir()
    (specs_dir / "FT-001.md").write_text("# FT-001\n", encoding="utf-8")
    (asp_dir / "architecture.md").write_text("# architecture\n", encoding="utf-8")
    (asp_dir / "tasks.md").write_text("# tasks\n", encoding="utf-8")
    impl_dir = asp_dir / "implementation"
    impl_dir.mkdir()
    (impl_dir / "implementation-report.md").write_text("# report\n", encoding="utf-8")

    legacy_dir = tmp_path / "013-legacy"
    legacy_dir.mkdir()
    (legacy_dir / "prd.md").write_text("# prd\n", encoding="utf-8")
    (legacy_dir / "architecture.md").write_text("# arch\n", encoding="utf-8")
    (legacy_dir / "tasks.md").write_text("# tasks\n", encoding="utf-8")

    invalid_asp_dir = tmp_path / "015-invalid-asp"
    invalid_asp_dir.mkdir()
    (invalid_asp_dir / "feature-spec-index.md").write_text("# index\n", encoding="utf-8")

    assert module.detect_iteration_mode(asp_dir) == "asp"
    assert module.validate_iteration_structure(asp_dir) is True
    assert module.detect_iteration_mode(legacy_dir) == "legacy"
    assert module.validate_iteration_structure(legacy_dir) is True
    assert module.validate_iteration_structure(invalid_asp_dir) is False


def test_validate_iteration_docs_only_checks_bug_instances(tmp_path: Path) -> None:
    """Bug validation should ignore templates, checklists and schema docs."""

    module = load_validate_module()
    bugs_dir = tmp_path / "bugs"
    templates_dir = bugs_dir / "templates"
    templates_dir.mkdir(parents=True)
    global_dir = bugs_dir / "global"
    global_dir.mkdir(parents=True)

    template_path = templates_dir / "bug-template.md"
    template_path.write_text("# template\n", encoding="utf-8")
    bug_path = global_dir / "bug-999-example.md"
    bug_path.write_text(
        "---\n"
        'bug_id: "bug-999"\n'
        'title: "Example"\n'
        'severity: "P1"\n'
        'status: "open"\n'
        "---\n\n"
        "# Example\n",
        encoding="utf-8",
    )

    assert module.is_bug_instance_document(template_path, bugs_dir) is False
    assert module.is_bug_instance_document(bug_path, bugs_dir) is True
