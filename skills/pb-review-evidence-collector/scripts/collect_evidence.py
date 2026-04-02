#!/usr/bin/env python3
"""Collect Evidence Unit records from a review resource inventory.

This helper exists for TASK-009-003. It converts files listed in
`project_metadata.resource_inventory` into deterministic Evidence Unit JSON so
the EvidenceCollector skill does not need to improvise extraction logic.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

MAX_SNIPPET_CHARS = 4000
MARKDOWN_HEADER_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
SYMBOL_RE = re.compile(
    r"^\s*(?:class|def|async\s+def|function|const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for evidence collection."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-path", required=True, help="Absolute or relative project root")
    parser.add_argument("--resource-inventory", required=True, help="Inventory JSON path")
    parser.add_argument("--output", required=True, help="Destination JSON file")
    return parser.parse_args()


def require_existing_path(path_str: str, label: str) -> Path:
    """Validate that a required filesystem path exists."""

    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise ValueError(f"{label} does not exist: {path}")
    return path


def load_inventory(path: Path) -> dict:
    """Load a resource inventory JSON document."""

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if "resource_inventory" in data:
        data = data["resource_inventory"]
    if not isinstance(data, dict):
        raise ValueError("resource inventory must be an object")
    return data


def iter_inventory_files(inventory: dict) -> Iterable[tuple[str, str]]:
    """Yield `(source_type, relative_path)` entries from the inventory."""

    mapping = {
        "docs": "doc",
        "code": "code",
        "tests": "test",
        "configs": "config",
    }
    for key, source_type in mapping.items():
        for relative_path in inventory.get(key, []):
            if not isinstance(relative_path, str) or not relative_path.strip():
                raise ValueError(f"invalid relative path in inventory.{key}: {relative_path!r}")
            yield source_type, relative_path


def read_text(path: Path) -> str:
    """Read a file as UTF-8, warning when replacement decoding is needed."""

    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        print(f"[warn] decoding with replacement: {path}", file=sys.stderr)
        return raw.decode("utf-8", errors="replace")


def iso_timestamp_from_path(path: Path) -> str:
    """Return the path mtime as an ISO-8601 UTC timestamp."""

    timestamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return timestamp.isoformat().replace("+00:00", "Z")


def build_evidence_id(source_type: str, source_path: str, content: str, index: int) -> str:
    """Create a stable evidence identifier from source metadata."""

    digest = hashlib.sha1(f"{source_type}:{source_path}:{index}:{content}".encode("utf-8")).hexdigest()
    return f"ev-{digest[:12]}"


def split_markdown_sections(text: str) -> list[tuple[str, str]]:
    """Split Markdown content into section-level snippets when headings exist."""

    matches = list(MARKDOWN_HEADER_RE.finditer(text))
    if not matches:
        return [("document", text[:MAX_SNIPPET_CHARS])]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = match.group(2).strip()
        content = text[start:end].strip()[:MAX_SNIPPET_CHARS]
        sections.append((title, content))
    return sections


def summarize_code(text: str) -> str:
    """Extract a compact symbol summary from source code text."""

    symbols = SYMBOL_RE.findall(text)
    if symbols:
        return "symbols: " + ", ".join(symbols[:20])
    return text[:MAX_SNIPPET_CHARS]


def build_file_evidence(project_root: Path, source_type: str, relative_path: str) -> list[dict]:
    """Build one or more Evidence Unit records for a file."""

    absolute_path = (project_root / relative_path).resolve()
    if not absolute_path.exists():
        raise ValueError(f"inventory file does not exist: {relative_path}")

    text = read_text(absolute_path)
    source_path = str(absolute_path.relative_to(project_root))
    author = "unknown"
    timestamp = iso_timestamp_from_path(absolute_path)

    snippets = (
        split_markdown_sections(text)
        if source_type == "doc"
        else [("file", summarize_code(text)[:MAX_SNIPPET_CHARS])]
    )

    evidence_units = []
    for index, (_, snippet) in enumerate(snippets, start=1):
        evidence_units.append(
            {
                "evidence_id": build_evidence_id(source_type, source_path, snippet, index),
                "source_type": source_type,
                "source_path": source_path,
                "timestamp": timestamp,
                "author": author,
                "content": snippet,
                "version_hint": "",
            }
        )
    return evidence_units


def collect_evidence(project_root: Path, inventory: dict) -> list[dict]:
    """Collect Evidence Unit records for every file in the inventory."""

    evidence_units: list[dict] = []
    for source_type, relative_path in iter_inventory_files(inventory):
        evidence_units.extend(build_file_evidence(project_root, source_type, relative_path))
    return evidence_units


def main() -> int:
    """Run the CLI entrypoint."""

    args = parse_args()
    project_root = require_existing_path(args.project_path, "project path")
    inventory_path = require_existing_path(args.resource_inventory, "resource inventory")
    inventory = load_inventory(inventory_path)
    evidence_units = collect_evidence(project_root, inventory)

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(evidence_units, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
