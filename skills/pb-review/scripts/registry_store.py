#!/usr/bin/env python3
"""Registry merge and persistence helpers for pb-review."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def unique_id_key(record: dict[str, Any]) -> str | None:
    """Infer the stable unique id field for a registry record."""

    for key in (
        "object_id",
        "relation_id",
        "conflict_id",
        "gap_id",
        "difference_id",
        "dependency_id",
        "mapping_id",
        "feature_id",
        "function_id",
        "evidence_id",
    ):
        value = record.get(key)
        if isinstance(value, str) and value:
            return f"{key}:{value}"
    return None


def merge_records(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge two record lists using their stable ids when possible."""

    ordered: list[dict[str, Any]] = []
    index_by_key: dict[str, int] = {}

    for record in existing:
        ordered.append(record)
        key = unique_id_key(record)
        if key:
            index_by_key[key] = len(ordered) - 1

    for record in incoming:
        key = unique_id_key(record)
        if key and key in index_by_key:
            ordered[index_by_key[key]] = record
            continue
        ordered.append(record)
        if key:
            index_by_key[key] = len(ordered) - 1

    return ordered


def load_records(path: Path) -> list[dict[str, Any]]:
    """Load a registry list or return an empty list."""

    if not path.exists():
        return []
    import json

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"registry must be a list: {path}")
    return data


def save_records(path: Path, records: list[dict[str, Any]]) -> None:
    """Write a registry list to disk."""

    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
