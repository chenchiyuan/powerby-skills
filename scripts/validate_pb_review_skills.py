#!/usr/bin/env python3
"""Validate the pb-review skill package layout.

This validator is intentionally narrow: it checks the 009 review-framework
skills added in this iteration for required frontmatter, section headings, and
supporting resource files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
REQUIRED_SECTIONS = [
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
]
EXPECTED_SKILLS = {
    "pb-review": [
        "scripts/review_runner.py",
        "scripts/review_context.py",
        "scripts/registry_store.py",
        "scripts/checkpoint.py",
        "scripts/evidence_packets.py",
        "scripts/review_utils.py",
        "scripts/testability_metrics.py",
        "scripts/render_testability_scorecard.py",
        "scripts/render_test_case_index.py",
        "scripts/render_fixture_contract.py",
        "scripts/render_oracle_matrix.py",
        "assets/testability-scorecard-template.md",
        "assets/test-case-index-template.md",
        "assets/fixture-contract-template.md",
        "assets/oracle-matrix-template.md",
    ],
    "pb-review-project-scope": ["scripts/run.py", "assets/system-context-template.md"],
    "pb-review-evidence-collector": [
        "scripts/run.py",
        "scripts/collect_evidence.py",
        "scripts/parse_git_history.py",
    ],
    "pb-review-conflict-resolver": ["scripts/run.py"],
    "pb-review-product-reconstructor": [
        "scripts/render_catalog.py",
        "assets/product-catalog-template.md",
    ],
    "pb-review-feature-reconstructor": [
        "scripts/render_feature_deliverables.py",
        "assets/feature-spec-index-template.md",
        "assets/feature-spec-card-template.md",
    ],
    "pb-review-relation-builder": [
        "scripts/render_traceability_matrix.py",
        "assets/traceability-matrix-template.md",
    ],
    "pb-review-gap-analyzer": [
        "scripts/render_gap_analysis.py",
        "assets/gap-analysis-template.md",
    ],
    "pb-review-report-composer": ["scripts/run.py", "assets/report-template.md"],
}
DELIVERABLE_STANDARD_SKILLS = {
    "pb-review",
    "pb-review-project-scope",
    "pb-review-product-reconstructor",
    "pb-review-feature-reconstructor",
    "pb-review-relation-builder",
    "pb-review-gap-analyzer",
    "pb-review-report-composer",
}
REFERENCE_DRIVEN_SKILLS = {
    "pb-review-product-reconstructor",
    "pb-review-feature-reconstructor",
    "pb-review-relation-builder",
    "pb-review-gap-analyzer",
}
REFERENCE_REQUIRED_FILES = [
    "references/task-contract.md",
    "references/examples.md",
    "references/failure-modes.md",
]
REFERENCE_RENDERER_SCRIPTS = {
    "pb-review-product-reconstructor": "scripts/render_catalog.py",
    "pb-review-feature-reconstructor": "scripts/render_feature_deliverables.py",
    "pb-review-relation-builder": "scripts/render_traceability_matrix.py",
    "pb-review-gap-analyzer": "scripts/render_gap_analysis.py",
}
FORBIDDEN_BACKEND_PATTERNS = [
    r"run_skill_contract",
    r"llm_client",
    r"chat_json",
    r"PB_REVIEW_LLM_",
    r"AUTOCLAW_POWERBY_URL",
    r"urlopen\(",
    r"chat/completions",
]


def validate_frontmatter(text: str, skill_name: str) -> list[str]:
    """Validate YAML frontmatter shape for a skill."""

    issues: list[str] = []
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return [f"{skill_name}: missing YAML frontmatter"]
    frontmatter = match.group(1)
    if f"name: {skill_name}" not in frontmatter:
        issues.append(f"{skill_name}: frontmatter name mismatch")
    if "description:" not in frontmatter:
        issues.append(f"{skill_name}: missing description")
    if "compatibility:" not in frontmatter:
        issues.append(f"{skill_name}: missing compatibility")
    return issues


def validate_sections(text: str, skill_name: str) -> list[str]:
    """Validate required section headings."""

    issues: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in text:
            issues.append(f"{skill_name}: missing section {section}")
    return issues


def validate_skill(skill_name: str, required_files: list[str]) -> list[str]:
    """Validate a single skill directory."""

    issues: list[str] = []
    skill_dir = SKILLS_ROOT / skill_name
    skill_file = skill_dir / "SKILL.md"
    if not skill_dir.exists():
        return [f"{skill_name}: missing skill directory"]
    if not skill_file.exists():
        return [f"{skill_name}: missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    issues.extend(validate_frontmatter(text, skill_name))
    issues.extend(validate_sections(text, skill_name))

    for relative_path in required_files:
        if not (skill_dir / relative_path).exists():
            issues.append(f"{skill_name}: missing required file {relative_path}")

    if skill_name in REFERENCE_DRIVEN_SKILLS:
        for relative_path in REFERENCE_REQUIRED_FILES:
            if not (skill_dir / relative_path).exists():
                issues.append(f"{skill_name}: missing contract resource file {relative_path}")
        for relative_path in REFERENCE_REQUIRED_FILES:
            if relative_path not in text:
                issues.append(f"{skill_name}: SKILL.md must reference {relative_path}")
        run_script = skill_dir / "scripts" / "run.py"
        if run_script.exists():
            issues.append(f"{skill_name}: abstract skills must not ship scripts/run.py; reasoning must stay in the host skill")
        renderer_script = REFERENCE_RENDERER_SCRIPTS.get(skill_name)
        if renderer_script and renderer_script not in text:
            issues.append(f"{skill_name}: SKILL.md must reference renderer script {renderer_script}")
        skill_text = skill_file.read_text(encoding="utf-8")
        if "后端 LLM" not in skill_text and "HTTP" not in skill_text:
            issues.append(f"{skill_name}: SKILL.md should explicitly forbid backend LLM delegation")

    if skill_name in DELIVERABLE_STANDARD_SKILLS:
        if "deliverable-standard.md" not in text:
            issues.append(f"{skill_name}: SKILL.md must reference deliverable-standard.md")
        if "feature-specification-standard.md" not in text:
            issues.append(f"{skill_name}: SKILL.md must reference feature-specification-standard.md")

    for pattern in FORBIDDEN_BACKEND_PATTERNS:
        for path in skill_dir.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if re.search(pattern, text):
                issues.append(f"{skill_name}: forbidden backend-llm pattern `{pattern}` found in {path.relative_to(skill_dir)}")
    return issues


def main() -> int:
    """Run the validator."""

    issues: list[str] = []
    for skill_name, required_files in EXPECTED_SKILLS.items():
        issues.extend(validate_skill(skill_name, required_files))

    shared_files = [
        SKILLS_ROOT / "pb-review" / "references" / "review-contract.md",
        SKILLS_ROOT / "pb-review" / "references" / "data-model.md",
        SKILLS_ROOT / "pb-review" / "references" / "deliverable-standard.md",
        SKILLS_ROOT / "pb-review" / "references" / "skill-sequence.md",
        REPO_ROOT / "docs" / "review" / "feature-specification-standard.md",
        REPO_ROOT / "docs" / "review" / "pb-review-deliverable-standard.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "d17-oracle-schema.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "d18-fixture-schema.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "d19-test-groups-schema.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "d20-coverage-claim-schema.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "testability-status-rules.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "testability-score-formula.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "gap-severity-rules.md",
        SKILLS_ROOT / "pb-review" / "schemas" / "entry-surface-types.md",
    ]
    for path in shared_files:
        if not path.exists():
            issues.append(f"missing shared resource: {path.relative_to(REPO_ROOT)}")

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        return 1

    print("OK: pb-review skill package structure is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
