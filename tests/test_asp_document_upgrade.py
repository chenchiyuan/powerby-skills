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

ACTIVE_ASP_SKILLS = {
    "powerby-asp-product": "asp-document-protocol-ref.md",
    "powerby-asp-office-hours": "design-brief-template-ref.md",
    "powerby-asp-reviewer": "audit-checklist-ref.md",
    "powerby-asp-codex-reviewer": "audit-checklist-ref.md",
    "powerby-asp-visualizer": "scoring-formula-ref.md",
    "powerby-asp-architect": "asp-document-protocol-ref.md",
    "powerby-asp-arch-reviewer": "arch-audit-checklist-ref.md",
    "powerby-asp-arch-codex-reviewer": "arch-audit-checklist-ref.md",
}

ITERATION_011_ROOT = REPO_ROOT / "docs/iterations/011-asp-document-upgrade"
ITERATION_012_ROOT = REPO_ROOT / "docs/iterations/012-asp-office-hours-integration"


def test_asp_document_protocol_upgraded_to_v1_2_0() -> None:
    """Active ASP protocol should include OFFICE_HOURS and design-brief contracts."""

    protocol_path = REPO_ROOT / "docs/asp-document-protocol.md"
    text = protocol_path.read_text(encoding="utf-8")

    assert "**版本**: 1.2.0" in text
    assert "`design-brief.md`" in text
    assert "OFFICE_HOURS" in text
    assert "## 5. 前置探讨与分阶段组装机制" in text
    assert "`feature-spec-index.md` 正式替代旧的功能点清单" in text
    assert "product-map.md + traceability-matrix.md + testability-scorecard.md" in text
    assert "## 6. `design-brief.md` 协议" in text
    assert "## 7. `proposal.md` 协议" in text
    assert text.count("**版本**: 1.2.0") == 1


def test_asp_skills_follow_skill_native_layout_and_ship_references() -> None:
    """Active ASP skills should adopt the 11-section layout and reference files."""

    for skill_name, reference_name in ACTIVE_ASP_SKILLS.items():
        skill_dir = REPO_ROOT / "skills" / skill_name
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

        assert "compatibility:" in skill_text, skill_name
        for header in SECTION_HEADERS:
            assert header in skill_text, f"{skill_name}: missing {header}"

        assert (skill_dir / "references" / reference_name).exists(), skill_name
        assert not (skill_dir / "scripts").exists(), skill_name


def test_iteration_011_proposal_includes_reuse_analysis_section() -> None:
    """011 proposal should include the upgraded format fields required by REQ-002."""

    proposal_text = (ITERATION_011_ROOT / "proposal.md").read_text(encoding="utf-8")

    assert "**状态**: Final" in proposal_text
    assert "## 5. 现有能力分析" in proposal_text
    assert "### 5.1 已有功能" in proposal_text
    assert "### 5.2 复用策略" in proposal_text
    assert "| REQ-009 | 重写 powerby-asp-codex-reviewer |" in proposal_text
    assert "11 section 标准结构" in proposal_text
    assert "等待 ASP Gate 1" not in proposal_text


def test_iteration_011_feature_index_and_feature_specs_follow_protocol() -> None:
    """011 should ship index/spec cards aligned to the feature-spec protocol."""

    index_text = (ITERATION_011_ROOT / "feature-spec-index.md").read_text(encoding="utf-8")
    spec_root = ITERATION_011_ROOT / "feature-specs"
    feature_spec_ids = sorted(path.stem for path in spec_root.glob("FT-*.md"))

    assert "| Feature ID | 功能名称 | 对应 REQ | 功能类型 | 状态 | Oracle 完整度 | Fixture 完整度 | 测试组数 |" in index_text
    assert len(feature_spec_ids) == 15
    assert feature_spec_ids[0] == "FT-001"
    assert feature_spec_ids[-1] == "FT-015"
    assert "**状态**: Final" in index_text
    assert "| FT-014 | ASP 流程产出升级 | REQ-014 | orchestration | final | 100% | 100% | 8 |" in index_text
    assert "**Final 状态**: 15" in index_text
    assert "**Oracle 完整度 ≥90%**: 15" in index_text
    assert "**Fixture 完整度 ≥90%**: 15" in index_text
    assert "进入 REFINING 阶段审查" not in index_text

    for feature_id in feature_spec_ids:
        spec_text = (spec_root / f"{feature_id}.md").read_text(encoding="utf-8")
        assert "- **状态**: final" in spec_text
        assert "待实现阶段补充" not in spec_text

    sample_card = (spec_root / "FT-004.md").read_text(encoding="utf-8")
    assert "## D-01: 功能标识" in sample_card
    assert "## D-08: 副作用" in sample_card
    assert "## D-17: Test Oracle" in sample_card
    assert "## D-20: Coverage Claim" in sample_card
    assert "## D-09: 性能要求" in sample_card
    assert "## D-16: 实现映射" in sample_card


def test_iteration_011_visualizer_artifacts_are_consistent() -> None:
    """Visualizer outputs should align with proposal and implementation artifacts."""

    traceability_text = (ITERATION_011_ROOT / "traceability-matrix.md").read_text(encoding="utf-8")
    product_map_text = (ITERATION_011_ROOT / "product-map.md").read_text(encoding="utf-8")

    assert "**状态**: Final" in traceability_text
    assert "| REQ-009 | 重写 powerby-asp-codex-reviewer | FT-009 | powerby-asp-codex-reviewer 重写 | ✅ 已覆盖 |" in traceability_text
    assert "| REQ-013 | 重写 powerby-asp-arch-codex-reviewer | FT-013 | powerby-asp-arch-codex-reviewer 重写 | ✅ 已覆盖 |" in traceability_text
    assert "**Feature 测试覆盖率**: 100% (15/15)" in traceability_text
    assert "tests/test_asp_document_upgrade.py::test_iteration_011_visualizer_artifacts_are_consistent" in traceability_text
    assert "traceability-matrix.md" in product_map_text
    assert "testability-scorecard.md" in product_map_text
    assert "FT-014 ASP 流程产出升级" in product_map_text
    assert "11 section 标准结构" in product_map_text


def test_iteration_011_scorecard_formula_and_grade_are_consistent() -> None:
    """Scorecard should report a score and grade consistent with its own formula."""

    scorecard_text = (ITERATION_011_ROOT / "testability-scorecard.md").read_text(encoding="utf-8")

    assert "**Testability Score: 90.67/100**" in scorecard_text
    assert "**等级: A**" in scorecard_text
    assert "= 90.67" in scorecard_text
    assert "M-07 覆盖宣称可信率 | 6.7% | ≥75% | ❌" in scorecard_text
    assert "Feature 测试覆盖率当前为 0%" not in scorecard_text


def test_iteration_011_implementation_report_records_final_test_result() -> None:
    """Implementation report should record the final full-suite pytest result."""

    report_text = (ITERATION_011_ROOT / "implementation/implementation-report.md").read_text(
        encoding="utf-8"
    )

    assert "`pytest -q tests` → `31 passed`" in report_text
    assert "待更新为最终执行结果" not in report_text


def test_iteration_011_checklist_review_evidence_exists() -> None:
    """011 should ship explicit evidence for the ten-principle checklist claim."""

    checklist_text = (ITERATION_011_ROOT / "reviews/skill-design-checklist.md").read_text(
        encoding="utf-8"
    )

    assert "十条核心设计原则（Checklist）" in checklist_text
    for skill_name in ACTIVE_ASP_SKILLS:
        if skill_name == "powerby-asp-office-hours":
            continue
        assert f"`{skill_name}`" in checklist_text
    assert "| 9 | 内建评估闭环 | 通过 |" in checklist_text
    assert "tests/test_asp_document_upgrade.py" in checklist_text


def test_product_line_skills_use_new_document_protocol() -> None:
    """Product-line ASP skills should use design-brief and avoid legacy spec names."""

    product_text = (REPO_ROOT / "skills/powerby-asp-product/SKILL.md").read_text(encoding="utf-8")
    office_hours_text = (REPO_ROOT / "skills/powerby-asp-office-hours/SKILL.md").read_text(
        encoding="utf-8"
    )
    reviewer_text = (REPO_ROOT / "skills/powerby-asp-reviewer/SKILL.md").read_text(encoding="utf-8")
    codex_text = (REPO_ROOT / "skills/powerby-asp-codex-reviewer/SKILL.md").read_text(
        encoding="utf-8"
    )
    visualizer_text = (REPO_ROOT / "skills/powerby-asp-visualizer/SKILL.md").read_text(
        encoding="utf-8"
    )

    for text in [product_text, office_hours_text, reviewer_text, codex_text, visualizer_text]:
        assert "spec.md" not in text

    assert "design-brief.md" in product_text
    assert "powerby-asp-office-hours" in product_text
    assert "one question at a time" in office_hours_text
    assert "alternatives generation" in office_hours_text
    assert "premise challenge" in office_hours_text
    assert "feature-spec-index.md" in product_text
    assert "design-brief.md" in reviewer_text
    assert "design-brief.md" in codex_text
    assert "前置探讨追溯检查" in reviewer_text
    assert "前置探讨追溯检查" in codex_text
    assert "feature-specs/*.md" in reviewer_text
    assert "feature-specs/*.md" in codex_text
    assert "traceability-matrix.md" in visualizer_text
    assert "testability-scorecard.md" in visualizer_text


def test_architecture_line_skills_use_feature_specs_instead_of_legacy_function_points() -> None:
    """Architecture-line ASP skills should enforce stage boundaries on feature specs."""

    architect_text = (REPO_ROOT / "skills/powerby-asp-architect/SKILL.md").read_text(
        encoding="utf-8"
    )
    reviewer_text = (REPO_ROOT / "skills/powerby-asp-arch-reviewer/SKILL.md").read_text(
        encoding="utf-8"
    )
    codex_text = (REPO_ROOT / "skills/powerby-asp-arch-codex-reviewer/SKILL.md").read_text(
        encoding="utf-8"
    )

    for text in [architect_text, reviewer_text, codex_text]:
        assert "function-points.md" not in text

    assert "feature-spec-index.md" in architect_text
    assert "feature-specs/*.md" in architect_text
    assert "D-09~D-16" in architect_text
    assert "D-01~D-08" in architect_text
    assert "architecture.md" in reviewer_text
    assert "architecture.md" in codex_text
    assert "Status" in reviewer_text
    assert "Status" in codex_text


def test_iteration_011_contract_docs_and_skill_specs_match_final_architecture() -> None:
    """Contract docs and active skill specs should align on final 11-section delivery."""

    architecture_text = (ITERATION_011_ROOT / "architecture.md").read_text(encoding="utf-8")
    assert "**状态**: Final" in architecture_text
    assert "11 section 标准结构" in architecture_text

    for feature_id in ["FT-007", "FT-008", "FT-009", "FT-010", "FT-011", "FT-012", "FT-013"]:
        spec_text = (ITERATION_011_ROOT / "feature-specs" / f"{feature_id}.md").read_text(
            encoding="utf-8"
        )
        assert "11 section 标准结构" in spec_text
        assert "不符合七层结构" not in spec_text
        assert "遵循七层结构" not in spec_text
        assert "不创建 scripts/" in spec_text


def test_iteration_012_documents_capture_office_hours_integration() -> None:
    """012 should record the flow update and implementation plan."""

    proposal_text = (ITERATION_012_ROOT / "proposal.md").read_text(encoding="utf-8")
    tasks_text = (ITERATION_012_ROOT / "tasks.md").read_text(encoding="utf-8")
    design_brief_text = (ITERATION_012_ROOT / "design-brief.md").read_text(encoding="utf-8")
    report_text = (ITERATION_012_ROOT / "implementation/implementation-report.md").read_text(
        encoding="utf-8"
    )

    assert "**迭代编号**: 012" in proposal_text
    assert "OFFICE_HOURS" in proposal_text
    assert "`design-brief.md`" in proposal_text
    assert "gstack `office-hours`" in proposal_text
    assert "方案 B" in tasks_text
    assert "powerby-asp-office-hours" in tasks_text
    assert "Original User Input" in design_brief_text
    assert "Clarification Log" in design_brief_text
    assert "docs/asp-document-protocol.md" in report_text
    assert "`pytest -q tests/test_asp_document_upgrade.py` -> `14 passed`" in report_text


def test_iterations_metadata_points_to_iteration_012() -> None:
    """Project metadata should expose the new ASP office-hours iteration."""

    iterations_text = (REPO_ROOT / ".powerby/iterations.json").read_text(encoding="utf-8")

    assert '"id": "012"' in iterations_text
    assert '"current_iteration": "012"' in iterations_text
    assert (
        '"design_brief": "docs/iterations/012-asp-office-hours-integration/design-brief.md"'
        in iterations_text
    )


def test_powerby_command_routes_asp_define_through_office_hours() -> None:
    """Command skill should route ASP define requests through office-hours first."""

    command_text = (REPO_ROOT / "skills/powerby-command/SKILL.md").read_text(encoding="utf-8")

    assert "powerby-asp-office-hours" in command_text
    assert "powerby-asp-product" in command_text
    assert "design-brief.md" in command_text
    assert "不得跳过 `design-brief.md` 直接生成 `proposal.md`" in command_text
    assert "ASP 流程检查是否生成：`design-brief.md`" in command_text
    assert "ASP 流程检查是否生成：`proposal.md`" in command_text
    assert "ASP 流程预期输出" in command_text
