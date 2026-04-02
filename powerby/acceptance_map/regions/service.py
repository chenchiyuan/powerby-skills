"""区域服务编排与合同校验。"""

from __future__ import annotations

import math
from typing import Any

from ..contracts import AcceptanceMapError, MicroAxis, OhlcvCandle, RegionDefinition, RegionPartitionResult
from .adaptive_volatility import build_adaptive_volatility_regions
from .equal_width import build_equal_width_regions


def _validate_config_keys(
    config: dict[str, Any],
    *,
    partition_mode: str,
    allowed_keys: set[str],
) -> None:
    unknown_keys = sorted(key for key in config if key not in allowed_keys)
    if unknown_keys:
        raise AcceptanceMapError(
            "INVALID_PARTITION_CONFIG",
            "区域划分参数非法，无法生成完整区域",
            {
                "partition_mode": partition_mode,
                "unknown_keys": unknown_keys,
            },
        )


def _parse_int_config(
    config: dict[str, Any],
    *,
    key: str,
    default: int,
    error_code: str,
    error_message: str,
) -> int:
    raw_value = config.get(key, default)
    if isinstance(raw_value, bool) or not isinstance(raw_value, int):
        raise AcceptanceMapError(
            error_code,
            error_message,
            {"field": key, "value": raw_value},
        )
    return raw_value


def validate_regions(axis: MicroAxis, regions: list[RegionDefinition]) -> None:
    """校验区域完整覆盖且不重叠。"""

    if not regions:
        raise AcceptanceMapError(
            "INVALID_REGION_COUNT",
            "区域插件未生成有效区域",
            {},
        )

    if regions[0].micro_bin_start != 0:
        raise AcceptanceMapError(
            "REGION_GAP_DETECTED",
            "区域划分结果存在缺口",
            {"expected_start": 0, "actual_start": regions[0].micro_bin_start},
        )

    for previous, current in zip(regions, regions[1:]):
        if current.micro_bin_start <= previous.micro_bin_end:
            raise AcceptanceMapError(
                "REGION_OVERLAP_DETECTED",
                "区域划分结果存在重叠",
                {
                    "previous": previous.region_id,
                    "current": current.region_id,
                },
            )
        if current.micro_bin_start != previous.micro_bin_end + 1:
            raise AcceptanceMapError(
                "REGION_GAP_DETECTED",
                "区域划分结果存在缺口",
                {
                    "previous": previous.region_id,
                    "current": current.region_id,
                },
            )

    for region in regions:
        if region.micro_bin_start < 0 or region.micro_bin_end >= axis.micro_bins:
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {"region_id": region.region_id},
            )

        expected_lower = axis.bins[region.micro_bin_start].lower_bound
        expected_upper = axis.bins[region.micro_bin_end].upper_bound
        if not math.isclose(region.lower_bound, expected_lower, rel_tol=0.0, abs_tol=1e-9):
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {
                    "region_id": region.region_id,
                    "expected_lower_bound": expected_lower,
                    "actual_lower_bound": region.lower_bound,
                },
            )
        if not math.isclose(region.upper_bound, expected_upper, rel_tol=0.0, abs_tol=1e-9):
            raise AcceptanceMapError(
                "REGION_AXIS_MISMATCH",
                "区域集合与底层价格轴不匹配",
                {
                    "region_id": region.region_id,
                    "expected_upper_bound": expected_upper,
                    "actual_upper_bound": region.upper_bound,
                },
            )

    if regions[-1].micro_bin_end != axis.micro_bins - 1:
        raise AcceptanceMapError(
            "REGION_GAP_DETECTED",
            "区域划分结果存在缺口",
            {
                "expected_end": axis.micro_bins - 1,
                "actual_end": regions[-1].micro_bin_end,
            },
        )


def partition_regions(
    axis: MicroAxis,
    *,
    partition_mode: str,
    candles: list[OhlcvCandle] | None = None,
    partition_config: dict[str, Any] | None = None,
) -> RegionPartitionResult:
    """选择区域插件并返回统一区域合同。"""

    config = partition_config or {}
    metadata: dict[str, Any] = {}

    if partition_mode == "equal_width":
        _validate_config_keys(
            config,
            partition_mode=partition_mode,
            allowed_keys={"group_size"},
        )
        group_size = _parse_int_config(
            config,
            key="group_size",
            default=5,
            error_code="INVALID_GROUP_SIZE",
            error_message="等宽切分参数非法",
        )
        regions = build_equal_width_regions(
            axis,
            group_size=group_size,
        )
        metadata["group_size"] = group_size
    elif partition_mode == "adaptive_volatility":
        _validate_config_keys(
            config,
            partition_mode=partition_mode,
            allowed_keys={"atr_period"},
        )
        if candles is None:
            raise AcceptanceMapError(
                "INSUFFICIENT_VOLATILITY_CONTEXT",
                "缺少波动上下文，无法计算最新 ATR 并生成自适应区域",
                {},
            )
        atr_period = _parse_int_config(
            config,
            key="atr_period",
            default=20,
            error_code="INVALID_ATR_PERIOD",
            error_message="ATR 周期必须大于等于 2",
        )
        regions, adaptive_group_size = build_adaptive_volatility_regions(
            axis,
            candles,
            atr_period=atr_period,
        )
        metadata["atr_period"] = atr_period
        metadata["adaptive_group_size"] = adaptive_group_size
    else:
        raise AcceptanceMapError(
            "UNSUPPORTED_PARTITION_MODE",
            "当前版本不支持该区域划分模式",
            {"partition_mode": partition_mode},
        )

    validate_regions(axis, regions)
    return RegionPartitionResult(
        partition_mode=partition_mode,
        regions=regions,
        plugin_metadata=metadata,
    )
