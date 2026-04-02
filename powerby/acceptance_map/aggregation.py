"""区域聚合与最终结果拼装。"""

from __future__ import annotations

import math

from .contracts import (
    AcceptanceMapError,
    AcceptanceMapResult,
    MicroAcceptance,
    MicroAxis,
    RegionAcceptance,
    RegionDefinition,
)
from .regions.service import validate_regions


def _validate_micro_probabilities_align_with_axis(
    axis: MicroAxis,
    micro_probabilities: list[MicroAcceptance],
) -> None:
    """确保底层概率结果与价格轴逐 bin 对齐。"""

    if len(micro_probabilities) != axis.micro_bins:
        raise AcceptanceMapError(
            "REGION_AXIS_MISMATCH",
            "区域集合与底层价格轴不匹配",
            {
                "expected_micro_bins": axis.micro_bins,
                "actual_micro_bins": len(micro_probabilities),
            },
        )

    for expected_bin, item in zip(axis.bins, micro_probabilities):
        if item.index != expected_bin.index:
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {
                    "expected_index": expected_bin.index,
                    "actual_index": item.index,
                },
            )
        if not math.isclose(item.lower_bound, expected_bin.lower_bound, rel_tol=0.0, abs_tol=1e-9):
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {
                    "micro_bin_index": expected_bin.index,
                    "expected_lower_bound": expected_bin.lower_bound,
                    "actual_lower_bound": item.lower_bound,
                },
            )
        if not math.isclose(item.upper_bound, expected_bin.upper_bound, rel_tol=0.0, abs_tol=1e-9):
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {
                    "micro_bin_index": expected_bin.index,
                    "expected_upper_bound": expected_bin.upper_bound,
                    "actual_upper_bound": item.upper_bound,
                },
            )
        if not math.isclose(item.center_price, expected_bin.center_price, rel_tol=0.0, abs_tol=1e-9):
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {
                    "micro_bin_index": expected_bin.index,
                    "expected_center_price": expected_bin.center_price,
                    "actual_center_price": item.center_price,
                },
            )


def aggregate_acceptance_map(
    axis: MicroAxis,
    micro_probabilities: list[MicroAcceptance],
    regions: list[RegionDefinition],
    *,
    coverage_sources_by_bin: list[frozenset[int]] | None = None,
    input_summary: dict[str, object] | None = None,
    params: dict[str, object] | None = None,
    include_heatmap: bool = True,
    include_diagnostics: bool = True,
) -> AcceptanceMapResult:
    """把底层概率聚合为区域结果。"""

    probability_sum = sum(item.price_acceptance_probability for item in micro_probabilities)
    if not math.isclose(probability_sum, 1.0, rel_tol=0.0, abs_tol=1e-6):
        raise AcceptanceMapError(
            "INVALID_PROBABILITY_SUM",
            "底层价格接受度概率未归一化",
            {"probability_sum": probability_sum},
        )

    if not regions:
        raise AcceptanceMapError(
            "EMPTY_REGION_RESULT",
            "区域聚合结果为空",
            {},
        )

    validate_regions(axis, regions)
    _validate_micro_probabilities_align_with_axis(axis, micro_probabilities)

    if include_diagnostics and coverage_sources_by_bin is None:
        raise AcceptanceMapError(
            "MISSING_DIAGNOSTIC_CONTEXT",
            "缺少诊断上下文，无法生成区域级 coverage_count",
            {},
        )

    if (
        coverage_sources_by_bin is not None
        and len(coverage_sources_by_bin) != len(micro_probabilities)
    ):
        raise AcceptanceMapError(
            "REGION_AXIS_MISMATCH",
            "区域集合与底层价格轴不匹配",
            {"coverage_source_bins": len(coverage_sources_by_bin)},
        )

    if regions[0].micro_bin_start != 0 or regions[-1].micro_bin_end != axis.micro_bins - 1:
        raise AcceptanceMapError(
            "REGION_AXIS_MISMATCH",
            "区域集合与底层价格轴不匹配",
            {},
        )

    region_results: list[RegionAcceptance] = []
    for region in regions:
        if region.micro_bin_start < 0 or region.micro_bin_end >= len(micro_probabilities):
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {"region_id": region.region_id},
            )

        selected = micro_probabilities[region.micro_bin_start : region.micro_bin_end + 1]
        selected_sources = (
            coverage_sources_by_bin[region.micro_bin_start : region.micro_bin_end + 1]
            if coverage_sources_by_bin is not None
            else None
        )
        region_results.append(
            RegionAcceptance(
                region_id=region.region_id,
                lower_bound=region.lower_bound,
                upper_bound=region.upper_bound,
                price_acceptance_probability=sum(item.price_acceptance_probability for item in selected),
                coverage_count=(
                    len(set().union(*selected_sources))
                    if include_diagnostics and selected_sources is not None
                    else None
                ),
                weighted_volume_contribution=(
                    sum(item.weighted_volume_contribution for item in selected)
                    if include_diagnostics
                    else None
                ),
            )
        )

    region_results.sort(key=lambda item: item.price_acceptance_probability, reverse=True)
    region_probability_sum = sum(item.price_acceptance_probability for item in region_results)
    if not math.isclose(region_probability_sum, 1.0, rel_tol=0.0, abs_tol=1e-6):
        raise AcceptanceMapError(
            "INVALID_PROBABILITY_SUM",
            "区域价格接受度概率未归一化",
            {"probability_sum": region_probability_sum},
        )

    heatmap: list[dict[str, object]] | None = None
    if include_heatmap:
        heatmap = []
        for item in micro_probabilities:
            record: dict[str, object] = {
                "index": item.index,
                "lower_bound": item.lower_bound,
                "upper_bound": item.upper_bound,
                "center_price": item.center_price,
                "price_acceptance_probability": item.price_acceptance_probability,
            }
            if include_diagnostics:
                record["coverage_count"] = item.coverage_count
                record["weighted_volume_contribution"] = item.weighted_volume_contribution
            heatmap.append(record)

    return AcceptanceMapResult(
        input_summary=dict(input_summary or {}),
        params=dict(params or {}),
        heatmap=heatmap,
        regions=region_results,
    )
