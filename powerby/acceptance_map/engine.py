"""价格接受度核心计算引擎。"""

from __future__ import annotations

import math

from .axis import find_covered_bin_indices, find_nearest_bin_index
from .contracts import AcceptanceMapError, EngineResult, MicroAcceptance, MicroAxis, OhlcvCandle
from .decay import exponential_time_weight


def compute_price_acceptance(
    candles: list[OhlcvCandle],
    micro_axis: MicroAxis,
    *,
    time_decay_mode: str = "exponential",
    decay_lambda: float = 0.004,
    zero_volume_policy: str = "keep_zero_contribution",
) -> EngineResult:
    """计算底层 micro bin 的接受度概率。"""

    if time_decay_mode != "exponential":
        raise AcceptanceMapError(
            "UNSUPPORTED_DECAY_MODE",
            "当前版本仅支持指数衰减时间权重",
            {"time_decay_mode": time_decay_mode},
        )
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
    if zero_volume_policy != "keep_zero_contribution":
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "当前版本不支持该零成交量策略",
            {"zero_volume_policy": zero_volume_policy},
        )

    contributions = [0.0 for _ in micro_axis.bins]
    coverage_counts = [0 for _ in micro_axis.bins]
    coverage_sources_by_bin = [set() for _ in micro_axis.bins]
    total_candles = len(candles)

    for index, candle in enumerate(candles):
        age = total_candles - 1 - index
        time_weight = exponential_time_weight(age, decay_lambda)
        weighted_volume = time_weight * candle.volume

        if candle.low < micro_axis.price_min or candle.high > micro_axis.price_max:
            raise AcceptanceMapError(
                "EMPTY_COVERAGE_SET",
                "价格轴覆盖异常，存在未被映射的 K 线",
                {
                    "timestamp": candle.timestamp,
                    "candle_low": candle.low,
                    "candle_high": candle.high,
                    "axis_min": micro_axis.price_min,
                    "axis_max": micro_axis.price_max,
                },
            )

        if math.isclose(candle.high, candle.low):
            covered_indices = [find_nearest_bin_index(micro_axis, candle.high)]
        else:
            covered_indices = find_covered_bin_indices(micro_axis, candle.low, candle.high)

        if not covered_indices:
            raise AcceptanceMapError(
                "EMPTY_COVERAGE_SET",
                "价格轴覆盖异常，存在未被映射的 K 线",
                {"timestamp": candle.timestamp},
            )

        per_bin_contribution = weighted_volume / len(covered_indices)
        for covered_index in covered_indices:
            contributions[covered_index] += per_bin_contribution
            if weighted_volume > 0:
                coverage_counts[covered_index] += 1
                coverage_sources_by_bin[covered_index].add(index)

    total_weight = sum(contributions)
    if total_weight <= 0:
        raise AcceptanceMapError(
            "ZERO_TOTAL_WEIGHT",
            "总权重为 0，无法归一化价格接受度概率",
            {},
        )

    micro_acceptances: list[MicroAcceptance] = []
    for micro_bin, contribution, coverage_count in zip(
        micro_axis.bins,
        contributions,
        coverage_counts,
    ):
        micro_acceptances.append(
            MicroAcceptance(
                index=micro_bin.index,
                lower_bound=micro_bin.lower_bound,
                upper_bound=micro_bin.upper_bound,
                center_price=micro_bin.center_price,
                price_acceptance_probability=contribution / total_weight,
                weighted_volume_contribution=contribution,
                coverage_count=coverage_count,
            )
        )

    probability_sum = sum(item.price_acceptance_probability for item in micro_acceptances)
    return EngineResult(
        time_decay_mode=time_decay_mode,
        decay_lambda=decay_lambda,
        micro_acceptances=micro_acceptances,
        probability_sum=probability_sum,
        coverage_sources_by_bin=[frozenset(indices) for indices in coverage_sources_by_bin],
    )
