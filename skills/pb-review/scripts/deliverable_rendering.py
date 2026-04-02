#!/usr/bin/env python3
"""Shared helpers for pb-review deliverable rendering scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    """Load JSON content from disk."""

    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_dict(value: Any) -> dict[str, Any]:
    """Return a dict value or an empty dict."""

    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    """Return a list value or an empty list."""

    return value if isinstance(value, list) else []


def stringify(value: Any) -> str:
    """Render a value as a compact string."""

    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a simple Markdown table."""

    table = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    table.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(table)


def render_json_block(data: Any, *, empty_text: str = "(无)") -> str:
    """Render a JSON code block for structured content."""

    if data in (None, "", [], {}):
        return empty_text
    return "```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```"


def render_mermaid_block(diagram: str, *, empty_text: str = "(无)") -> str:
    """Render a Mermaid diagram block."""

    content = (diagram or "").strip()
    if not content:
        return empty_text
    return "```mermaid\n" + content + "\n```"


def render_bullets(items: list[str], *, empty_text: str = "(无)") -> str:
    """Render a flat bullet list."""

    filtered = [item for item in items if item]
    if not filtered:
        return f"- {empty_text}"
    return "\n".join(f"- {item}" for item in filtered)


def render_key_value_bullets(pairs: list[tuple[str, str]], *, empty_text: str = "(无)") -> str:
    """Render key/value items as bullet lines."""

    lines = [f"- **{key}**: {value}" for key, value in pairs if value]
    if not lines:
        return f"- {empty_text}"
    return "\n".join(lines)


def render_records(records: list[Any], *, empty_text: str = "(无)") -> str:
    """Render a list of records as readable bullet lines."""

    lines: list[str] = []
    for item in records:
        if isinstance(item, dict):
            title = (
                stringify(item.get("id"))
                or stringify(item.get("name"))
                or stringify(item.get("code"))
                or stringify(item.get("type"))
            )
            description = (
                stringify(item.get("description"))
                or stringify(item.get("summary"))
                or stringify(item.get("message"))
                or stringify(item.get("check"))
                or stringify(item.get("expected"))
            )
            extras = []
            for key in ["type", "check", "expected", "example", "severity", "path", "command"]:
                value = stringify(item.get(key))
                if value:
                    extras.append(f"{key}={value}")
            suffix = f" ({'; '.join(extras)})" if extras else ""
            if title and description:
                lines.append(f"- **{title}**: {description}{suffix}")
            elif title:
                lines.append(f"- **{title}**{suffix}")
            elif description:
                lines.append(f"- {description}{suffix}")
            else:
                lines.append(f"- `{json.dumps(item, ensure_ascii=False)}`")
            continue
        text = stringify(item)
        if text:
            lines.append(f"- {text}")
    if not lines:
        return f"- {empty_text}"
    return "\n".join(lines)


def read_template(path: Path) -> str:
    """Read a template file from disk."""

    return path.read_text(encoding="utf-8")


def render_template(template_text: str, values: dict[str, str]) -> str:
    """Replace template placeholders with rendered content."""

    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def ensure_deliverables_dir(project_path: Path) -> Path:
    """Ensure the canonical pb-review deliverable directory exists."""

    deliverables_dir = project_path / ".review" / "deliverables"
    deliverables_dir.mkdir(parents=True, exist_ok=True)
    return deliverables_dir


def mark_deliverables_completed(manifest: dict[str, Any], deliverable_ids: list[str]) -> dict[str, Any]:
    """Mark specific deliverables as completed in the manifest."""

    ids = set(deliverable_ids)
    updated = {"version": str(manifest.get("version", "2.0")), "required_deliverables": []}
    for item in as_list(manifest.get("required_deliverables")):
        normalized = as_dict(item)
        if not normalized:
            continue
        if normalized.get("deliverable_id") in ids:
            normalized["status"] = "completed"
        updated["required_deliverables"].append(normalized)
    return updated


def build_result(
    *,
    status: str,
    context_writes: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    errors: list[str] | None = None,
) -> dict[str, Any]:
    """Build a standard pb-review payload."""

    return {
        "status": status,
        "objects": [],
        "relations": [],
        "conflicts": [],
        "gaps": [],
        "context_writes": context_writes or {},
        "metadata": metadata or {},
        "errors": errors or [],
    }
