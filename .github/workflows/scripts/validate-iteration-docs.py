#!/usr/bin/env python3
"""
validate-iteration-docs.py
Validate iteration documents for completeness and consistency
Usage: validate-iteration-docs.py
"""

import os
import sys
import json
from pathlib import Path
import yaml

def validate_iteration_structure(iteration_dir):
    """Validate that all required files exist in an iteration"""
    required_files = {
        "prd.md": "Product Requirements Document",
        "architecture.md": "Architecture Design Document",
        "tasks.md": "Task List Document",
        "implementation.md": "Implementation Document"
    }

    missing_files = []
    for file, description in required_files.items():
        file_path = iteration_dir / file
        if not file_path.exists():
            missing_files.append(f"  ❌ {file} - {description}")

    if missing_files:
        print(f"📁 Iteration: {iteration_dir.name}")
        for missing in missing_files:
            print(missing)
        return False
    else:
        print(f"✅ Iteration: {iteration_dir.name} - All files present")
        return True

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
