"""波动自适应区域插件。"""

from __future__ import annotations

import math

from ..contracts import AcceptanceMapError, MicroAxis, OhlcvCandle, RegionDefinition
from .utils import build_regions_by_group_size


def _true_range(previous_close: float, candle: OhlcvCandle) -> float:
    return max(
        candle.high - candle.low,
        abs(candle.high - previous_close),
        abs(candle.low - previous_close),
    )


def compute_latest_atr(candles: list[OhlcvCandle], *, atr_period: int = 20) -> float:
    """按最近窗口计算最新 ATR。"""

    if not isinstance(atr_period, int) or atr_period < 2:
        raise AcceptanceMapError(
            "INVALID_ATR_PERIOD",
            "ATR 周期必须大于等于 2",
            {"atr_period": atr_period},
        )
    if len(candles) < atr_period + 1:
        raise AcceptanceMapError(
            "INSUFFICIENT_VOLATILITY_CONTEXT",
            "缺少波动上下文，无法计算最新 ATR 并生成自适应区域",
            {"sample_size": len(candles), "atr_period": atr_period},
        )

    trailing = candles[-(atr_period + 1) :]
    true_ranges = [
        _true_range(previous.close, current)
        for previous, current in zip(trailing, trailing[1:])
    ]
    return sum(true_ranges) / len(true_ranges)


def build_adaptive_volatility_regions(
    micro_axis: MicroAxis,
    candles: list[OhlcvCandle],
    *,
    atr_period: int = 20,
) -> tuple[list[RegionDefinition], int]:
    """按 ATR 推导组宽并切分区域。"""

    latest_atr = compute_latest_atr(candles, atr_period=atr_period)
    ratio = latest_atr / micro_axis.bin_width
    group_size = max(1, math.floor(ratio + 0.5))
    group_size = min(group_size, micro_axis.micro_bins)
    return build_regions_by_group_size(micro_axis, group_size=group_size), group_size
