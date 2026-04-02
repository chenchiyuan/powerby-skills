#!/usr/bin/env python3
"""Validate iteration documents for both legacy and ASP iteration layouts."""

import os
import sys
import json
from pathlib import Path
import yaml


LEGACY_MARKERS = (
    "prd.md",
    "spec.md",
    "function-points.md",
    "architecture.md",
    "tasks.md",
    "implementation-report.md",
    "implementation/implementation-report.md",
)

ASP_MARKERS = (
    "design-brief.md",
    "proposal.md",
    "feature-spec-index.md",
    "feature-specs",
)


def _exists(iteration_dir: Path, relative_path: str) -> bool:
    """Return whether a relative file or directory exists in the iteration."""

    return (iteration_dir / relative_path).exists()


def detect_iteration_mode(iteration_dir: Path) -> str:
    """Detect whether an iteration follows the ASP or legacy document model."""

    if any(_exists(iteration_dir, marker) for marker in ASP_MARKERS):
        return "asp"
    return "legacy"


def validate_legacy_iteration_structure(iteration_dir: Path) -> tuple[bool, list[str]]:
    """Validate a legacy iteration without assuming every phase artifact already exists."""

    messages: list[str] = []
    present_docs = [marker for marker in LEGACY_MARKERS if _exists(iteration_dir, marker)]

    if not present_docs:
        messages.append("  ❌ 未找到任何 legacy 迭代文档")
        return False, messages

    if _exists(iteration_dir, "tasks.md") and not _exists(iteration_dir, "architecture.md"):
        messages.append("  ❌ 存在 tasks.md 但缺少 architecture.md")

    if _exists(iteration_dir, "implementation/implementation-report.md") and not _exists(
        iteration_dir, "tasks.md"
    ):
        messages.append("  ❌ 存在 implementation/implementation-report.md 但缺少 tasks.md")

    if _exists(iteration_dir, "implementation-report.md") and not _exists(iteration_dir, "tasks.md"):
        messages.append("  ❌ 存在 implementation-report.md 但缺少 tasks.md")

    if not messages:
        messages.append(f"  ✅ 识别为 legacy 迭代，已发现文档: {', '.join(present_docs)}")

    return len([message for message in messages if message.startswith('  ❌')]) == 0, messages


def validate_asp_iteration_structure(iteration_dir: Path) -> tuple[bool, list[str]]:
    """Validate an ASP iteration by checking stage dependencies instead of a fixed file set."""

    messages: list[str] = []
    present_docs = [marker for marker in ASP_MARKERS if _exists(iteration_dir, marker)]

    if not present_docs:
        messages.append("  ❌ 未找到任何 ASP 迭代文档")
        return False, messages

    if _exists(iteration_dir, "feature-spec-index.md") and not _exists(iteration_dir, "proposal.md"):
        messages.append("  ❌ 存在 feature-spec-index.md 但缺少 proposal.md")

    if _exists(iteration_dir, "feature-spec-index.md"):
        specs_dir = iteration_dir / "feature-specs"
        if not specs_dir.exists() or not any(specs_dir.glob("FT-*.md")):
            messages.append("  ❌ 存在 feature-spec-index.md 但缺少 feature-specs/FT-*.md")

    if _exists(iteration_dir, "architecture.md") and not (
        _exists(iteration_dir, "proposal.md") or _exists(iteration_dir, "prd.md")
    ):
        messages.append("  ❌ 存在 architecture.md 但缺少 proposal.md 或 prd.md")

    if _exists(iteration_dir, "tasks.md") and not (
        _exists(iteration_dir, "architecture.md") or _exists(iteration_dir, "proposal.md")
    ):
        messages.append("  ❌ 存在 tasks.md 但缺少 architecture.md 或 proposal.md")

    if _exists(iteration_dir, "implementation/implementation-report.md") and not _exists(
        iteration_dir, "tasks.md"
    ):
        messages.append("  ❌ 存在 implementation/implementation-report.md 但缺少 tasks.md")

    if not messages:
        messages.append(f"  ✅ 识别为 ASP 迭代，已发现文档: {', '.join(present_docs)}")

    return len([message for message in messages if message.startswith('  ❌')]) == 0, messages


def validate_iteration_structure(iteration_dir: Path) -> bool:
    """Validate one iteration directory according to its detected document model."""

    mode = detect_iteration_mode(iteration_dir)
    if mode == "asp":
        is_valid, messages = validate_asp_iteration_structure(iteration_dir)
    else:
        is_valid, messages = validate_legacy_iteration_structure(iteration_dir)

    print(f"📁 Iteration: {iteration_dir.name} ({mode})")
    for message in messages:
        print(message)
    return is_valid

def validate_yaml_frontmatter(file_path):
    """Validate YAML frontmatter in markdown files"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        if not content.startswith('---'):
            return True, "No YAML frontmatter (optional)"

        # Extract YAML frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "YAML frontmatter not properly closed"

        yaml_content = parts[1].strip()

        try:
            data = yaml.safe_load(yaml_content)
            return True, "Valid YAML frontmatter"
        except yaml.YAMLError as e:
            return False, f"Invalid YAML: {e}"

    except Exception as e:
        return False, f"Error reading file: {e}"

def validate_bug_document(file_path):
    """Validate bug document structure and required fields"""
    required_fields = [
        "bug_id",
        "title",
        "severity",
        "status"
    ]

    is_valid, message = validate_yaml_frontmatter(file_path)
    if not is_valid:
        return False, f"YAML validation failed: {message}"

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Missing YAML frontmatter"

        yaml_content = parts[1].strip()
        data = yaml.safe_load(yaml_content)

        missing_fields = []
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)

        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

        # Validate severity values
        valid_severities = ["P0", "P1", "P2", "P3"]
        if data.get("severity") not in valid_severities:
            return False, f"Invalid severity '{data.get('severity')}'. Must be one of: {', '.join(valid_severities)}"

        return True, "Valid bug document"

    except Exception as e:
        return False, f"Error validating bug document: {e}"


def is_bug_instance_document(file_path: Path, bugs_dir: Path) -> bool:
    """Return whether a markdown file should be treated as a concrete bug instance."""

    relative_parts = file_path.relative_to(bugs_dir).parts
    excluded_roots = {"templates", "scripts", "checklists"}

    return (
        file_path.suffix == ".md"
        and file_path.name.startswith("bug-")
        and relative_parts[0] not in excluded_roots
    )

def main():
    print("🔍 Validating PowerBy documentation structure\n")

    iterations_dir = Path("docs/iterations")
    bugs_dir = Path("docs/bugs")

    all_valid = True

    # Validate iterations
    if iterations_dir.exists():
        print("📂 Validating Iterations:")
        for iteration_dir in iterations_dir.iterdir():
            if iteration_dir.is_dir():
                if not validate_iteration_structure(iteration_dir):
                    all_valid = False
        print()
    else:
        print("⚠️  Iterations directory not found\n")

    # Validate bug documents
    if bugs_dir.exists():
        print("🐛 Validating Bug Documents:")
        for root, dirs, files in os.walk(bugs_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    if not is_bug_instance_document(file_path, bugs_dir):
                        continue
                    is_valid, message = validate_bug_document(file_path)
                    status = "✅" if is_valid else "❌"
                    print(f"{status} {file_path.relative_to(bugs_dir)}: {message}")
                    if not is_valid:
                        all_valid = False
        print()
    else:
        print("⚠️  Bugs directory not found\n")

    # Summary
    if all_valid:
        print("✅ All documentation validation checks passed!")
        sys.exit(0)
    else:
        print("❌ Some validation checks failed. Please review the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
