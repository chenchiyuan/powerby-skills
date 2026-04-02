"""固定份数微价格轴。"""

from __future__ import annotations

import math

from .contracts import AcceptanceMapError, MicroAxis, MicroBin


def build_micro_axis(
    price_min: float,
    price_max: float,
    *,
    micro_bins: int = 100,
    axis_mode: str = "fixed_count",
) -> MicroAxis:
    """构建固定数量的微价格轴。"""

    if axis_mode != "fixed_count":
        raise AcceptanceMapError(
            "UNSUPPORTED_AXIS_MODE",
            "当前版本不支持该价格轴构建模式",
            {"axis_mode": axis_mode},
        )
    if not isinstance(micro_bins, int) or micro_bins < 10:
        raise AcceptanceMapError(
            "INVALID_BIN_COUNT",
            "micro_bins 必须是大于等于 10 的整数",
            {"micro_bins": micro_bins},
        )
    if not math.isfinite(price_min) or not math.isfinite(price_max) or price_max <= price_min:
        raise AcceptanceMapError(
            "INVALID_AXIS_RANGE",
            "历史价格范围非法，无法构建价格轴",
            {"price_min": price_min, "price_max": price_max},
        )

    bin_width = (price_max - price_min) / micro_bins
    bins: list[MicroBin] = []
    for index in range(micro_bins):
        lower_bound = price_min + index * bin_width
        if index == micro_bins - 1:
            upper_bound = price_max
        else:
            upper_bound = price_min + (index + 1) * bin_width
        bins.append(
            MicroBin(
                index=index,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                center_price=(lower_bound + upper_bound) / 2,
            )
        )

    return MicroAxis(
        axis_mode=axis_mode,
        price_min=price_min,
        price_max=price_max,
        micro_bins=micro_bins,
        bin_width=bin_width,
        bins=bins,
    )


def find_nearest_bin_index(axis: MicroAxis, price: float) -> int:
    """返回与价格最近的中心点 bin，等距时取更低价格的 bin。"""

    best_index = 0
    best_distance = abs(axis.bins[0].center_price - price)
    for micro_bin in axis.bins[1:]:
        distance = abs(micro_bin.center_price - price)
        if distance < best_distance:
            best_index = micro_bin.index
            best_distance = distance
    return best_index


def find_covered_bin_indices(axis: MicroAxis, low: float, high: float) -> list[int]:
    """返回区间覆盖到的全部 bin 索引。"""

    covered_indices: list[int] = []
    for micro_bin in axis.bins:
        # Bins are left-closed/right-open except the last one, so a candle low
        # that lands exactly on the previous upper bound must not back-fill left.
        if micro_bin.upper_bound <= low:
            continue
        if micro_bin.lower_bound > high:
            continue
        covered_indices.append(micro_bin.index)
    return covered_indices
