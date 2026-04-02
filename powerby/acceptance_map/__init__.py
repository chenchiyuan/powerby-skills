"""OHLCV 价格接受度地图分析入口。"""

from __future__ import annotations

from typing import Any

from .aggregation import aggregate_acceptance_map
from .axis import build_micro_axis
from .contracts import AcceptanceMapError, AcceptanceMapResult
from .engine import compute_price_acceptance
from .regions.service import partition_regions
from .validation import validate_and_normalize_analysis_input


def _require_bool(value: Any, *, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            f"{field_name} 必须为布尔值",
            {"field": field_name, "value_type": type(value).__name__},
        )
    return value


def analyze_acceptance_map(
    payload: dict[str, Any],
    *,
    partition_mode: str = "equal_width",
    include_heatmap: bool = True,
    include_diagnostics: bool = True,
    decay_lambda: float = 0.004,
    micro_bins: int = 100,
    partition_config: dict[str, Any] | None = None,
) -> AcceptanceMapResult:
    """执行完整价格接受度分析链路。"""

    if partition_config is not None and not isinstance(partition_config, dict):
        raise AcceptanceMapError(
            "INVALID_PARTITION_CONFIG",
            "区域划分参数非法，无法生成完整区域",
            {"partition_config_type": type(partition_config).__name__},
        )
    include_heatmap = _require_bool(include_heatmap, field_name="include_heatmap")
    include_diagnostics = _require_bool(
        include_diagnostics,
        field_name="include_diagnostics",
    )

    request = validate_and_normalize_analysis_input(payload)
    axis = build_micro_axis(request.price_min, request.price_max, micro_bins=micro_bins)
    engine_result = compute_price_acceptance(
        request.candles,
        axis,
        decay_lambda=decay_lambda,
    )
    partition_result = partition_regions(
        axis,
        partition_mode=partition_mode,
        candles=request.candles,
        partition_config=partition_config,
    )

    params = {
        "partition_mode": partition_mode,
        "include_heatmap": include_heatmap,
        "include_diagnostics": include_diagnostics,
        "micro_bins": micro_bins,
        "decay_lambda": decay_lambda,
    }
    params.update(partition_result.plugin_metadata)

    return aggregate_acceptance_map(
        axis,
        engine_result.micro_acceptances,
        partition_result.regions,
        coverage_sources_by_bin=engine_result.coverage_sources_by_bin,
        input_summary={
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "sample_size": request.sample_size,
            "market_hint": request.market_hint,
            "price_min": request.price_min,
            "price_max": request.price_max,
        },
        params=params,
        include_heatmap=include_heatmap,
        include_diagnostics=include_diagnostics,
    )
