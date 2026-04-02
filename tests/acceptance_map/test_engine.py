from __future__ import annotations

import math

import pytest

from powerby.acceptance_map.axis import build_micro_axis
from powerby.acceptance_map.contracts import AcceptanceMapError, OhlcvCandle
from powerby.acceptance_map.engine import compute_price_acceptance


def test_compute_price_acceptance_gives_more_weight_to_newer_candle() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=0.1, high=0.9, low=0.1, close=0.8, volume=100.0),
        OhlcvCandle(timestamp=2, open=8.1, high=8.9, low=8.1, close=8.8, volume=100.0),
    ]

    result = compute_price_acceptance(candles, axis, decay_lambda=1.0)

    assert math.isclose(result.probability_sum, 1.0, rel_tol=0.0, abs_tol=1e-9)
    assert result.micro_acceptances[8].weighted_volume_contribution > result.micro_acceptances[0].weighted_volume_contribution
    assert result.micro_acceptances[8].price_acceptance_probability > result.micro_acceptances[0].price_acceptance_probability


def test_compute_price_acceptance_splits_multi_bin_coverage_evenly() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=0.1, high=2.9, low=0.1, close=2.8, volume=300.0),
    ]

    result = compute_price_acceptance(candles, axis, decay_lambda=0.5)

    assert math.isclose(result.micro_acceptances[0].weighted_volume_contribution, 100.0)
    assert math.isclose(result.micro_acceptances[1].weighted_volume_contribution, 100.0)
    assert math.isclose(result.micro_acceptances[2].weighted_volume_contribution, 100.0)
    assert math.isclose(result.micro_acceptances[0].price_acceptance_probability, 1 / 3)
    assert math.isclose(result.micro_acceptances[1].price_acceptance_probability, 1 / 3)
    assert math.isclose(result.micro_acceptances[2].price_acceptance_probability, 1 / 3)


def test_compute_price_acceptance_does_not_backfill_left_bin_on_exact_low_boundary() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=1.0, high=2.0, low=1.0, close=1.5, volume=200.0),
    ]

    result = compute_price_acceptance(candles, axis, decay_lambda=0.5)

    assert math.isclose(result.micro_acceptances[0].weighted_volume_contribution, 0.0)
    assert math.isclose(result.micro_acceptances[1].weighted_volume_contribution, 100.0)
    assert math.isclose(result.micro_acceptances[2].weighted_volume_contribution, 100.0)


def test_compute_price_acceptance_rejects_candle_partially_outside_axis() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=-1.0, high=1.0, low=-1.0, close=0.5, volume=100.0),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        compute_price_acceptance(candles, axis, decay_lambda=0.5)

    assert exc_info.value.code == "EMPTY_COVERAGE_SET"


def test_compute_price_acceptance_maps_doji_to_nearest_center_with_lower_tie_break() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=5.0, high=5.0, low=5.0, close=5.0, volume=100.0),
    ]

    result = compute_price_acceptance(candles, axis, decay_lambda=0.5)

    assert math.isclose(result.micro_acceptances[4].price_acceptance_probability, 1.0)
    assert math.isclose(result.micro_acceptances[5].price_acceptance_probability, 0.0)


def test_compute_price_acceptance_rejects_invalid_decay_lambda() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=1.0, high=2.0, low=1.0, close=2.0, volume=100.0),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        compute_price_acceptance(candles, axis, decay_lambda=0.0)

    assert exc_info.value.code == "INVALID_DECAY_LAMBDA"


def test_compute_price_acceptance_rejects_non_numeric_decay_lambda() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=1.0, high=2.0, low=1.0, close=2.0, volume=100.0),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        compute_price_acceptance(candles, axis, decay_lambda="0.1")  # type: ignore[arg-type]

    assert exc_info.value.code == "INVALID_DECAY_LAMBDA"


@pytest.mark.parametrize("decay_lambda", [math.inf, math.nan])
def test_compute_price_acceptance_rejects_non_finite_decay_lambda(decay_lambda: float) -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=1.0, high=2.0, low=1.0, close=2.0, volume=100.0),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        compute_price_acceptance(candles, axis, decay_lambda=decay_lambda)

    assert exc_info.value.code == "INVALID_DECAY_LAMBDA"


def test_compute_price_acceptance_excludes_zero_volume_candles_from_coverage_count() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    candles = [
        OhlcvCandle(timestamp=1, open=1.0, high=2.0, low=1.0, close=1.5, volume=0.0),
        OhlcvCandle(timestamp=2, open=8.0, high=9.0, low=8.0, close=8.5, volume=100.0),
    ]

    result = compute_price_acceptance(candles, axis, decay_lambda=0.5)

    assert result.micro_acceptances[1].coverage_count == 0
    assert result.micro_acceptances[2].coverage_count == 0
    assert result.micro_acceptances[8].coverage_count == 1
    assert result.micro_acceptances[9].coverage_count == 1
