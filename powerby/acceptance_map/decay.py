"""时间衰减策略。"""

from __future__ import annotations

import math

from .contracts import AcceptanceMapError


def exponential_time_weight(age: int, decay_lambda: float) -> float:
    """返回指数衰减权重，age=0 表示最新 K 线。"""

    if isinstance(decay_lambda, bool) or not isinstance(decay_lambda, (int, float)):
        raise AcceptanceMapError(
            "INVALID_DECAY_LAMBDA",
            "指数衰减参数必须为数值且大于 0",
            {"decay_lambda": decay_lambda},
        )
    if not math.isfinite(decay_lambda):
        raise AcceptanceMapError(
            "INVALID_DECAY_LAMBDA",
            "指数衰减参数必须为有限数值且大于 0",
            {"decay_lambda": decay_lambda},
        )
    if decay_lambda <= 0:
        raise AcceptanceMapError(
            "INVALID_DECAY_LAMBDA",
            "指数衰减参数必须大于 0",
            {"decay_lambda": decay_lambda},
        )
    if isinstance(age, bool) or not isinstance(age, int) or age < 0:
        raise AcceptanceMapError(
            "INVALID_DECAY_LAMBDA",
            "时间衰减 age 不可为负数",
            {"age": age},
        )
    return math.exp(-decay_lambda * age)
