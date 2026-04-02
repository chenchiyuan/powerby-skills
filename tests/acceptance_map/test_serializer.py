from __future__ import annotations

import math
import pytest

from powerby.acceptance_map.axis import build_micro_axis
from powerby.acceptance_map.contracts import (
    AcceptanceMapError,
    AcceptanceMapResult,
    OhlcvCandle,
    RegionAcceptance,
)
from powerby.acceptance_map.engine import compute_price_acceptance
from powerby.acceptance_map.serializer import dump_json, to_serializable


def test_dump_json_rejects_non_finite_float_values() -> None:
    with pytest.raises(AcceptanceMapError) as exc_info:
        dump_json({"value": math.inf, "nan_value": math.nan})

    assert exc_info.value.code == "ANALYSIS_FAILED"


def test_dump_json_can_serialize_error_payload_with_non_finite_context() -> None:
    error = AcceptanceMapError("BROKEN", "bad", {"value": math.nan}).to_dict()
    body = dump_json(error)

    assert '"code": "BROKEN"' in body
    assert '"value": "nan"' in body


def test_to_serializable_omits_none_fields_from_dataclass_payload() -> None:
    result = AcceptanceMapResult(
        input_summary={"symbol": "BTCUSDT"},
        params={"include_heatmap": False},
        heatmap=None,
        regions=[
            RegionAcceptance(
                region_id="R-001",
                lower_bound=100.0,
                upper_bound=110.0,
                price_acceptance_probability=1.0,
                coverage_count=None,
                weighted_volume_contribution=None,
            )
        ],
    )

    serialized = to_serializable(result)

    assert "heatmap" not in serialized
    assert "coverage_count" not in serialized["regions"][0]
    assert "weighted_volume_contribution" not in serialized["regions"][0]


def test_dump_json_omits_internal_coverage_sources_from_engine_result() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=1.0, high=2.0, low=1.0, close=2.0, volume=100.0),
    ]

    result = compute_price_acceptance(candles, axis, decay_lambda=0.5)
    body = dump_json(result)

    assert '"time_decay_mode": "exponential"' in body
    assert '"coverage_sources_by_bin"' not in body
