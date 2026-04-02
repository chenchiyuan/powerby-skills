from __future__ import annotations

import pytest

from powerby.acceptance_map.axis import build_micro_axis
from powerby.acceptance_map.contracts import AcceptanceMapError, OhlcvCandle, RegionDefinition
from powerby.acceptance_map import analyze_acceptance_map
from powerby.acceptance_map.regions.service import partition_regions, validate_regions
from powerby.acceptance_map.regions.adaptive_volatility import build_adaptive_volatility_regions
from tests.acceptance_map.helpers import make_ohlcv_payload
from powerby.acceptance_map.validation import validate_and_normalize_analysis_input


def test_partition_regions_supports_equal_width_mode() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=100)

    result = partition_regions(axis, partition_mode="equal_width", partition_config={})

    assert result.partition_mode == "equal_width"
    assert len(result.regions) == 20
    assert result.regions[0].micro_bin_start == 0
    assert result.regions[-1].micro_bin_end == 99


def test_analyze_acceptance_map_exposes_equal_width_partition_params() -> None:
    result = analyze_acceptance_map(
        make_ohlcv_payload(500),
        partition_mode="equal_width",
        partition_config={"group_size": 7},
    )

    assert result.params["partition_mode"] == "equal_width"
    assert result.params["group_size"] == 7


def test_partition_regions_supports_adaptive_volatility_mode() -> None:
    request = validate_and_normalize_analysis_input(make_ohlcv_payload(500))
    axis = build_micro_axis(request.price_min, request.price_max, micro_bins=100)

    result = partition_regions(
        axis,
        partition_mode="adaptive_volatility",
        candles=request.candles,
        partition_config={},
    )

    assert result.partition_mode == "adaptive_volatility"
    assert result.plugin_metadata["adaptive_group_size"] >= 1
    assert result.regions[0].micro_bin_start == 0
    assert result.regions[-1].micro_bin_end == 99


def test_analyze_acceptance_map_exposes_adaptive_partition_params() -> None:
    result = analyze_acceptance_map(
        make_ohlcv_payload(500),
        partition_mode="adaptive_volatility",
        partition_config={"atr_period": 14},
    )

    assert result.params["partition_mode"] == "adaptive_volatility"
    assert result.params["atr_period"] == 14
    assert result.params["adaptive_group_size"] >= 1


def test_validate_regions_rejects_gap() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)
    regions = [
        RegionDefinition(
            region_id="R-001",
            micro_bin_start=0,
            micro_bin_end=3,
            lower_bound=axis.bins[0].lower_bound,
            upper_bound=axis.bins[3].upper_bound,
        ),
        RegionDefinition(
            region_id="R-002",
            micro_bin_start=5,
            micro_bin_end=9,
            lower_bound=axis.bins[5].lower_bound,
            upper_bound=axis.bins[9].upper_bound,
        ),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_regions(axis, regions)

    assert exc_info.value.code == "REGION_GAP_DETECTED"


def test_validate_regions_rejects_axis_bound_mismatch() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)
    regions = [
        RegionDefinition(
            region_id="R-001",
            micro_bin_start=0,
            micro_bin_end=4,
            lower_bound=999.0,
            upper_bound=150.0,
        ),
        RegionDefinition(
            region_id="R-002",
            micro_bin_start=5,
            micro_bin_end=9,
            lower_bound=150.0,
            upper_bound=200.0,
        ),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_regions(axis, regions)

    assert exc_info.value.code == "REGION_AXIS_MISMATCH"


def test_partition_regions_rejects_non_numeric_plugin_config() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)

    with pytest.raises(AcceptanceMapError) as group_size_error:
        partition_regions(
            axis,
            partition_mode="equal_width",
            partition_config={"group_size": "abc"},
        )

    assert group_size_error.value.code == "INVALID_GROUP_SIZE"

    with pytest.raises(AcceptanceMapError) as atr_period_error:
        partition_regions(
            axis,
            partition_mode="adaptive_volatility",
            candles=[],
            partition_config={"atr_period": "abc"},
        )

    assert atr_period_error.value.code == "INVALID_ATR_PERIOD"


def test_partition_regions_rejects_non_integer_plugin_config() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)

    with pytest.raises(AcceptanceMapError) as group_size_error:
        partition_regions(
            axis,
            partition_mode="equal_width",
            partition_config={"group_size": 5.9},
        )

    assert group_size_error.value.code == "INVALID_GROUP_SIZE"

    with pytest.raises(AcceptanceMapError) as bool_group_size_error:
        partition_regions(
            axis,
            partition_mode="equal_width",
            partition_config={"group_size": True},
        )

    assert bool_group_size_error.value.code == "INVALID_GROUP_SIZE"


def test_partition_regions_rejects_unknown_equal_width_config_key() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)

    with pytest.raises(AcceptanceMapError) as exc_info:
        partition_regions(
            axis,
            partition_mode="equal_width",
            partition_config={"group_szie": 7},
        )

    assert exc_info.value.code == "INVALID_PARTITION_CONFIG"


def test_partition_regions_rejects_unknown_adaptive_config_key() -> None:
    request = validate_and_normalize_analysis_input(make_ohlcv_payload(500))
    axis = build_micro_axis(request.price_min, request.price_max, micro_bins=100)

    with pytest.raises(AcceptanceMapError) as exc_info:
        partition_regions(
            axis,
            partition_mode="adaptive_volatility",
            candles=request.candles,
            partition_config={"atr_peroid": 14},
        )

    assert exc_info.value.code == "INVALID_PARTITION_CONFIG"


def test_build_adaptive_volatility_regions_rounds_half_up_at_boundary() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=100.0, micro_bins=100)
    candles = [
        OhlcvCandle(timestamp=0, open=10.0, high=10.0, low=10.0, close=10.0, volume=1.0),
        OhlcvCandle(timestamp=1, open=10.0, high=12.5, low=10.0, close=12.5, volume=1.0),
        OhlcvCandle(timestamp=2, open=12.5, high=15.0, low=12.5, close=15.0, volume=1.0),
    ]

    regions, group_size = build_adaptive_volatility_regions(axis, candles, atr_period=2)

    assert group_size == 3
    assert len(regions) == 34


def test_analyze_acceptance_map_rejects_non_dict_partition_config() -> None:
    payload = make_ohlcv_payload(500)

    with pytest.raises(AcceptanceMapError) as exc_info:
        analyze_acceptance_map(payload, partition_config=[])  # type: ignore[arg-type]

    assert exc_info.value.code == "INVALID_PARTITION_CONFIG"


@pytest.mark.parametrize(
    ("field_name", "kwargs"),
    [
        ("include_heatmap", {"include_heatmap": "false"}),
        ("include_heatmap", {"include_heatmap": 0}),
        ("include_diagnostics", {"include_diagnostics": "false"}),
        ("include_diagnostics", {"include_diagnostics": 1}),
    ],
)
def test_analyze_acceptance_map_rejects_non_boolean_toggle_options(
    field_name: str,
    kwargs: dict[str, object],
) -> None:
    payload = make_ohlcv_payload(500)

    with pytest.raises(AcceptanceMapError) as exc_info:
        analyze_acceptance_map(payload, **kwargs)  # type: ignore[arg-type]

    assert exc_info.value.code == "INPUT_PARSE_ERROR"
    assert exc_info.value.context["field"] == field_name
