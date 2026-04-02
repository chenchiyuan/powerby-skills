from __future__ import annotations

import math

import pytest

from powerby.acceptance_map.axis import build_micro_axis
from powerby.acceptance_map.contracts import AcceptanceMapError


def test_build_micro_axis_covers_full_price_range() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=100)

    assert axis.axis_mode == "fixed_count"
    assert len(axis.bins) == 100
    assert axis.bins[0].lower_bound == 100.0
    assert axis.bins[-1].upper_bound == 200.0
    assert math.isclose(axis.bin_width, 1.0)
    assert axis.bins[1].lower_bound == axis.bins[0].upper_bound


def test_build_micro_axis_rejects_invalid_range() -> None:
    with pytest.raises(AcceptanceMapError) as exc_info:
        build_micro_axis(price_min=100.0, price_max=100.0, micro_bins=100)

    assert exc_info.value.code == "INVALID_AXIS_RANGE"
