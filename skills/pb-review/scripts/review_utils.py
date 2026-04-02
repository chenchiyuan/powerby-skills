#!/usr/bin/env python3
"""Generic text and identifier helpers for pb-review."""

from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    """Normalize text for deterministic matching."""

    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", text.lower())


def tokenize(text: str, min_length: int = 2) -> set[str]:
    """Tokenize text into normalized alphanumeric words."""

    return {
        token
        for token in re.split(r"[^a-z0-9\u4e00-\u9fff]+", text.lower())
        if len(token) >= min_length
    }


def make_sequential_id(prefix: str, index: int) -> str:
    """Create a stable sequential identifier."""

    return f"{prefix}-{index:03d}"


def overlap_score(left: str, right: str, min_length: int = 2, stopwords: list[str] | None = None) -> int:
    """Compute token overlap score for generic retrieval only."""

    stopwords = stopwords or []
    ignored = {word.lower() for word in stopwords}
    left_tokens = {token for token in tokenize(left, min_length=min_length) if token not in ignored}
    right_tokens = {token for token in tokenize(right, min_length=min_length) if token not in ignored}
    return len(left_tokens & right_tokens)
