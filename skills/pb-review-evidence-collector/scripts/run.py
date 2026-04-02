#!/usr/bin/env python3
"""Executor for pb-review-evidence-collector."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def load_json(path: str) -> dict:
    """Load JSON data from disk."""

    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def hash_file(path: Path) -> str:
    """Compute a SHA256 hash for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def flatten_inventory(inventory: dict) -> list[str]:
    """Flatten the resource inventory into a unique sorted file list."""

    paths: list[str] = []
    for key in ("docs", "code", "tests", "configs"):
        paths.extend(inventory.get(key, []))
    return sorted(set(paths))


def filter_inventory(inventory: dict, changed_files: set[str]) -> dict:
    """Keep only changed files in the inventory."""

    return {
        key: [path for path in inventory.get(key, []) if path in changed_files]
        for key in ("docs", "code", "tests", "configs")
    }


def run_python(script: Path, arguments: list[str]) -> None:
    """Run a Python helper script and fail fast on errors."""

    result = subprocess.run(["python3", str(script), *arguments], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"helper failed: {script}")


def build_commit_evidence(commits: list[dict]) -> list[dict]:
    """Convert Git commit metadata into Evidence Unit records."""

    evidence_units = []
    for commit in commits:
        commit_hash = commit["commit_hash"]
        evidence_units.append(
            {
                "evidence_id": f"ev-commit-{commit_hash[:12]}",
                "source_type": "commit",
                "source_path": commit_hash,
                "timestamp": commit["timestamp"],
                "author": commit.get("author_email") or commit.get("author") or "unknown",
                "content": commit["message"],
                "version_hint": "",
            }
        )
    return evidence_units


def main() -> int:
    """Run the evidence collector executor."""

    args = parse_args()
    context = load_json(args.context)
    parameters = load_json(args.parameters)
    start = time.time()

    project_metadata = context.get("project_metadata") or {}
    inventory = project_metadata.get("resource_inventory") or {}
    project_root = Path(context["project_path"]).expanduser().resolve()
    review_dir = project_root / ".review"
    cache_path = review_dir / "evidence_cache.json"
    cache = load_json(str(cache_path)) if cache_path.exists() else {}

    if not inventory:
        payload = {
            "status": "failed",
            "objects": [],
            "relations": [],
            "conflicts": [],
            "gaps": [],
            "context_writes": {},
            "metadata": {"total_evidence_count": 0, "by_source_type": {}, "cache_hit_rate": 0},
            "errors": ["project_metadata.resource_inventory is required"],
        }
        with Path(args.output).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        return 0

    all_files = flatten_inventory(inventory)
    hashes = {}
    changed_files: set[str] = set()
    cache_hits = 0
    for relative_path in all_files:
        absolute_path = project_root / relative_path
        if not absolute_path.exists():
            changed_files.add(relative_path)
            continue
        current_hash = hash_file(absolute_path)
        hashes[relative_path] = current_hash
        cached = cache.get(relative_path, {})
        if parameters.get("incremental", True) and cached.get("hash") == current_hash:
            cache_hits += 1
        else:
            changed_files.add(relative_path)

    previous_evidence = context.get("evidence_registry", [])
    unchanged_paths = {path for path in all_files if path not in changed_files}
    unchanged_evidence = [item for item in previous_evidence if item.get("source_path") in unchanged_paths]

    temp_dir = review_dir / "_tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    changed_inventory_path = temp_dir / "changed_inventory.json"
    changed_output_path = temp_dir / "evidence_changed.json"
    git_output_path = temp_dir / "git_history.json"

    changed_inventory = filter_inventory(inventory, changed_files)
    with changed_inventory_path.open("w", encoding="utf-8") as handle:
        json.dump({"resource_inventory": changed_inventory}, handle, ensure_ascii=False, indent=2)

    changed_evidence = []
    if any(changed_inventory.values()):
        run_python(
            Path(__file__).with_name("collect_evidence.py"),
            ["--project-path", str(project_root), "--resource-inventory", str(changed_inventory_path), "--output", str(changed_output_path)],
        )
        with changed_output_path.open("r", encoding="utf-8") as handle:
            changed_evidence = json.load(handle)

    commit_evidence = []
    git_errors: list[str] = []
    try:
        run_python(
            Path(__file__).with_name("parse_git_history.py"),
            ["--project-path", str(project_root), "--output", str(git_output_path)],
        )
        with git_output_path.open("r", encoding="utf-8") as handle:
            commit_evidence = build_commit_evidence(json.load(handle))
    except Exception as exc:  # noqa: BLE001
        git_errors.append(str(exc))

    full_evidence = unchanged_evidence + changed_evidence + commit_evidence
    for relative_path, current_hash in hashes.items():
        cache[relative_path] = {
            "hash": current_hash,
            "last_modified": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime((project_root / relative_path).stat().st_mtime)),
            "evidence_ids": [item["evidence_id"] for item in full_evidence if item.get("source_path") == relative_path],
        }
    with cache_path.open("w", encoding="utf-8") as handle:
        json.dump(cache, handle, ensure_ascii=False, indent=2)

    by_source_type = {"doc": 0, "code": 0, "test": 0, "config": 0, "commit": 0, "issue": 0}
    for item in full_evidence:
        source_type = item.get("source_type")
        if source_type in by_source_type:
            by_source_type[source_type] += 1

    payload = {
        "status": "partial" if git_errors else "success",
        "objects": [],
        "relations": [],
        "conflicts": [],
        "gaps": [],
        "context_writes": {"evidence_registry": full_evidence},
        "metadata": {
            "total_evidence_count": len(full_evidence),
            "by_source_type": by_source_type,
            "cache_hit_rate": 0 if not all_files else round(cache_hits / len(all_files), 4),
        },
        "errors": git_errors,
    }

    with Path(args.output).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
