#!/usr/bin/env python3
"""ReviewContext filesystem adapter for pb-review."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REVIEW_FILE_MAP = {
    "project_metadata": "project_metadata.json",
    "evidence_registry": "evidence_registry.json",
    "current_facts": "current_facts.json",
    "object_registry": "object_registry.json",
    "feature_spec_registry": "feature_spec_registry.json",
    "feature_state_registry": "feature_state_registry.json",
    "traceability_matrix": "traceability_matrix.json",
    "relation_registry": "relation_registry.json",
    "conflict_registry": "conflict_registry.json",
    "difference_registry": "difference_registry.json",
    "gap_registry": "gap_registry.json",
    "deliverable_manifest": "deliverable_manifest.json",
    "dependency_registry": "dependency_registry.json",
    "implementation_registry": "implementation_registry.json",
    "architecture_registry": "architecture_registry.json",
    "data_flow_registry": "data_flow_registry.json",
}

STANDARD_REGISTRY_MAP = {
    "objects": "object_registry",
    "relations": "relation_registry",
    "conflicts": "conflict_registry",
    "gaps": "gap_registry",
}


def utc_now() -> str:
    """Return the current UTC time in ISO-8601 format."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ReviewContextStore:
    """Manage `.review/` files as the physical ReviewContext store."""

    def __init__(self, project_path: str, scope: str, review_id: str | None = None) -> None:
        self.project_path = Path(project_path).expanduser().resolve()
        self.scope = scope
        self.review_dir = self.project_path / ".review"
        self.temp_dir = self.review_dir / "_tmp"
        self.review_id = review_id or self._default_review_id()

    def _default_review_id(self) -> str:
        """Build a deterministic review id from project name and time."""

        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return f"review-{self.project_path.name}-{stamp}"

    def ensure_dirs(self) -> None:
        """Create `.review/` and temp directories when missing."""

        self.review_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def reset(self) -> None:
        """Remove prior review outputs for a clean non-resume run."""

        self.ensure_dirs()
        for file_name in list(REVIEW_FILE_MAP.values()) + [
            "checkpoint.json",
            "review_report.md",
            "evidence_cache.json",
        ]:
            path = self.review_dir / file_name
            if path.exists():
                path.unlink()
        deliverables_dir = self.review_dir / "deliverables"
        if deliverables_dir.exists():
            for path in sorted(deliverables_dir.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()

    def file_path(self, context_field: str) -> Path:
        """Resolve a ReviewContext field to its JSON file path."""

        if context_field not in REVIEW_FILE_MAP:
            raise KeyError(f"unknown ReviewContext field: {context_field}")
        return self.review_dir / REVIEW_FILE_MAP[context_field]

    def exists(self, context_field: str) -> bool:
        """Return whether a ReviewContext field file exists."""

        return self.file_path(context_field).exists()

    def load_json(self, path: Path, default: Any) -> Any:
        """Load JSON from disk or return a default value."""

        if not path.exists():
            return default
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def write_json(self, path: Path, data: Any) -> None:
        """Persist JSON data with stable formatting."""

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

    def load_context(self) -> dict[str, Any]:
        """Assemble the logical ReviewContext from `.review/` files."""

        context = {
            "review_id": self.review_id,
            "project_path": str(self.project_path),
            "scope": self.scope,
            "timestamp": utc_now(),
        }
        for field, file_name in REVIEW_FILE_MAP.items():
            default = [] if field.endswith("_registry") else {}
            context[field] = self.load_json(self.review_dir / file_name, default)
        return context

    def write_context_field(self, field: str, value: Any) -> str:
        """Persist a ReviewContext field and return the written file name."""

        path = self.file_path(field)
        self.write_json(path, value)
        return path.name
