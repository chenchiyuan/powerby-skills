#!/usr/bin/env python3
"""Executor for pb-review-conflict-resolver."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
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


def sort_key(item: dict) -> tuple:
    """Sort evidence by timestamp descending, then path and id."""

    return (item.get("timestamp", ""), item.get("source_path", ""), item.get("evidence_id", ""))


def main() -> int:
    """Run the conflict resolver executor."""

    args = parse_args()
    context = load_json(args.context)
    evidence_registry = context.get("evidence_registry", [])
    project_metadata = context.get("project_metadata") or {}
    product_doc_inventory = set(project_metadata.get("product_doc_inventory", []))
    if not evidence_registry:
        payload = {
            "status": "failed",
            "objects": [],
            "relations": [],
            "conflicts": [],
            "gaps": [],
            "context_writes": {},
            "metadata": {"priority_rules_applied": [], "unresolved_conflicts": 0},
            "errors": ["evidence_registry is required"],
        }
        with Path(args.output).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        return 0

    by_path: dict[str, list[dict]] = defaultdict(list)
    for item in evidence_registry:
        by_path[item.get("source_path", item.get("evidence_id", "unknown"))].append(item)

    conflicts = []
    product_facts = []
    implementation_facts = []
    unresolved = 0

    for source_path, items in by_path.items():
        ordered = sorted(items, key=sort_key, reverse=True)
        winner = ordered[0]
        source_type = winner.get("source_type")
        latest_timestamp = winner.get("timestamp")
        latest_items = [item for item in ordered if item.get("timestamp") == latest_timestamp]
        older_items = [item for item in ordered if item.get("timestamp") != latest_timestamp]

        for latest in latest_items:
            if source_type == "doc" and source_path in product_doc_inventory:
                product_facts.append(latest["evidence_id"])
            elif source_type in {"code", "test", "config"}:
                implementation_facts.append(latest["evidence_id"])

        for loser in older_items:
            conflicts.append(
                {
                    "conflict_id": f"conflict-{winner['evidence_id']}-{loser['evidence_id']}",
                    "conflict_type": "version_conflict" if winner.get("source_type") == loser.get("source_type") else "mixed_source",
                    "evidence_a": winner["evidence_id"],
                    "evidence_b": loser["evidence_id"],
                    "description": f"Newer evidence supersedes older evidence for {source_path}",
                    "resolution": "preserved",
                    "priority_winner": winner["evidence_id"],
                }
            )

    payload = {
        "status": "partial" if unresolved else "success",
        "objects": [],
        "relations": [],
        "conflicts": conflicts,
        "gaps": [],
        "context_writes": {
            "current_facts": {
                "product_facts": sorted(set(product_facts)),
                "implementation_facts": sorted(set(implementation_facts)),
            }
        },
        "metadata": {
            "priority_rules_applied": [
                "产品层：新文档优先于旧文档",
                "实现层：代码优先于旧文档",
                "同路径：时间更新者优先",
            ],
            "unresolved_conflicts": unresolved,
        },
        "errors": [] if unresolved == 0 else ["some evidence items could not be fully resolved"],
    }

    with Path(args.output).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
