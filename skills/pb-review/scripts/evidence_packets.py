#!/usr/bin/env python3
"""Deterministic evidence packet helpers for pb-review."""

from __future__ import annotations

from collections import defaultdict

from review_utils import normalize_text, overlap_score

MAX_PACKET_CHARS = 12000


def chunk_list(items: list, size: int) -> list[list]:
    """Split a list into fixed-size chunks."""

    return [items[index : index + size] for index in range(0, len(items), size)]


def group_evidence_by_path(evidence_items: list[dict]) -> list[dict]:
    """Group evidence units by source path."""

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in evidence_items:
        grouped[str(item.get("source_path", ""))].append(item)

    groups = []
    for source_path, items in sorted(grouped.items()):
        ordered = sorted(items, key=lambda item: (str(item.get("timestamp", "")), str(item.get("evidence_id", ""))))
        groups.append(
            {
                "source_path": source_path,
                "source_type": ordered[0].get("source_type", ""),
                "evidence_ids": [item["evidence_id"] for item in ordered],
                "items": ordered,
            }
        )
    return groups


def summarize_group(group: dict, preview_chars: int = 500) -> dict:
    """Build a compact summary for a grouped evidence packet."""

    preview = "\n\n".join(item.get("content", "") for item in group["items"])[:preview_chars]
    return {
        "source_path": group["source_path"],
        "source_type": group["source_type"],
        "evidence_ids": group["evidence_ids"],
        "preview": preview,
    }


def summarize_groups(groups: list[dict], preview_chars: int = 500) -> list[dict]:
    """Summarize grouped evidence packets."""

    return [summarize_group(group, preview_chars=preview_chars) for group in groups]


def build_group_packet(group: dict, max_chars: int = MAX_PACKET_CHARS) -> dict:
    """Build a model-facing evidence packet for a grouped source path."""

    content_blocks = []
    used = 0
    used_ids = []
    for item in group["items"]:
        block = f"[{item['evidence_id']}]\n{item.get('content', '').strip()}\n"
        if content_blocks and used + len(block) > max_chars:
            break
        content_blocks.append(block)
        used += len(block)
        used_ids.append(item["evidence_id"])
    return {
        "source_path": group["source_path"],
        "source_type": group["source_type"],
        "evidence_ids": used_ids,
        "content": "\n".join(content_blocks).strip(),
    }


def top_k_candidates(query_text: str, candidates: list[dict], text_fn, limit: int = 8) -> list[dict]:
    """Retrieve top-k candidate records using generic token overlap."""

    scored = []
    for candidate in candidates:
        score = overlap_score(query_text, text_fn(candidate), min_length=2)
        scored.append((score, normalize_text(text_fn(candidate)), candidate))
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    selected = [candidate for score, _, candidate in scored if score > 0][:limit]
    if selected:
        return selected
    return [candidate for _, _, candidate in scored[:limit]]
