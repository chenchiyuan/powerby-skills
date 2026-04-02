#!/usr/bin/env python3
"""Export Git commit metadata for the review framework.

This helper exists for TASK-009-003. It turns repository history into a stable
JSON array so the EvidenceCollector skill can merge commit evidence without
rewriting Git parsing logic on every run.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

RECORD_SEPARATOR = "\x1e"
FIELD_SEPARATOR = "\x1f"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for Git history export."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-path", required=True, help="Git repository root")
    parser.add_argument("--output", required=True, help="Destination JSON file")
    return parser.parse_args()


def require_git_repo(path_str: str) -> Path:
    """Validate that the given path exists and looks like a Git repository."""

    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise ValueError(f"project path does not exist: {path}")
    if not (path / ".git").exists():
        raise ValueError(f"project path is not a git repository: {path}")
    return path


def run_git_log(project_root: Path) -> str:
    """Run `git log` with stable separators for parsing."""

    command = [
        "git",
        "log",
        "--all",
        "--date=iso-strict",
        f"--format=--COMMIT--%n%H{FIELD_SEPARATOR}%an{FIELD_SEPARATOR}%ae{FIELD_SEPARATOR}%aI{FIELD_SEPARATOR}%s",
        "--name-only",
    ]
    result = subprocess.run(
        command,
        cwd=project_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git log failed")
    return result.stdout


def parse_git_records(output: str) -> list[dict]:
    """Parse Git log output into structured commit records."""

    commits: list[dict] = []
    for raw_record in output.split("--COMMIT--"):
        record = raw_record.strip()
        if not record:
            continue
        lines = [line for line in record.splitlines() if line.strip()]
        header = lines[0].split(FIELD_SEPARATOR)
        if len(header) != 5:
            raise ValueError(f"unexpected git log header: {lines[0]!r}")
        commit_hash, author_name, author_email, authored_at, subject = header
        files = lines[1:]
        commits.append(
            {
                "commit_hash": commit_hash,
                "author": author_name,
                "author_email": author_email,
                "timestamp": authored_at,
                "message": subject,
                "files": files,
            }
        )
    return commits


def main() -> int:
    """Run the CLI entrypoint."""

    args = parse_args()
    project_root = require_git_repo(args.project_path)
    output = run_git_log(project_root)
    commits = parse_git_records(output)

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(commits, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
