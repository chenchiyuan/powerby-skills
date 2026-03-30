#!/usr/bin/env python3
"""Checkpoint helpers for pb-review resume support."""

from __future__ import annotations

import json
from pathlib import Path

from review_context import utc_now


def checkpoint_path(review_dir: Path) -> Path:
    """Return the canonical checkpoint file path."""

    return review_dir / "checkpoint.json"


def load_checkpoint(review_dir: Path) -> dict:
    """Load checkpoint data or return an empty state."""

    path = checkpoint_path(review_dir)
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_checkpoint(review_dir: Path, review_id: str, last_completed_skill: str, completed_writes: list[str]) -> None:
    """Persist the latest completed skill state."""

    path = checkpoint_path(review_dir)
    payload = {
        "review_id": review_id,
        "last_completed_skill": last_completed_skill,
        "timestamp": utc_now(),
        "completed_writes": sorted(set(completed_writes)),
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def is_consistent(review_dir: Path, completed_writes: list[str]) -> bool:
    """Check whether all files claimed by the checkpoint are present."""

    return all((review_dir / file_name).exists() for file_name in completed_writes)


def next_step_index(step_names: list[str], checkpoint: dict) -> int:
    """Determine the step index to resume from."""

    last_completed = checkpoint.get("last_completed_skill")
    if not last_completed:
        return 0
    if last_completed not in step_names:
        return 0
    return step_names.index(last_completed) + 1
