"""结果序列化。"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, is_dataclass
from typing import Any

from .contracts import AcceptanceMapError

_INTERNAL_RESULT_FIELDS = {"coverage_sources_by_bin"}


def to_serializable(value: Any) -> Any:
    """递归转换 dataclass 为可序列化字典。"""

    if is_dataclass(value):
        result: dict[str, Any] = {}
        for key, item in asdict(value).items():
            if key in _INTERNAL_RESULT_FIELDS:
                continue
            if item is None:
                continue
            result[key] = to_serializable(item)
        return result
    if isinstance(value, float) and not math.isfinite(value):
        raise AcceptanceMapError(
            "ANALYSIS_FAILED",
            "分析结果包含非法数值，无法序列化为 JSON",
            {"value": str(value)},
        )
    if isinstance(value, (set, frozenset)):
        return [to_serializable(item) for item in sorted(value)]
    if isinstance(value, list):
        return [to_serializable(item) for item in value]
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if item is None:
                continue
            result[key] = to_serializable(item)
        return result
    return value


def dump_json(value: Any) -> str:
    """输出稳定 JSON。"""

    return json.dumps(
        to_serializable(value),
        ensure_ascii=False,
        indent=2,
        sort_keys=False,
        allow_nan=False,
    )
