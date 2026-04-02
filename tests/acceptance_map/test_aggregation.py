from __future__ import annotations

import pytest

from powerby.acceptance_map.aggregation import aggregate_acceptance_map
from powerby.acceptance_map.axis import build_micro_axis
from powerby.acceptance_map.contracts import AcceptanceMapError, MicroAcceptance, RegionDefinition


def test_aggregate_acceptance_map_returns_sorted_regions_and_heatmap() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(index=0, lower_bound=100.0, upper_bound=110.0, center_price=105.0, price_acceptance_probability=0.02, weighted_volume_contribution=2.0, coverage_count=1),
        MicroAcceptance(index=1, lower_bound=110.0, upper_bound=120.0, center_price=115.0, price_acceptance_probability=0.04, weighted_volume_contribution=4.0, coverage_count=2),
        MicroAcceptance(index=2, lower_bound=120.0, upper_bound=130.0, center_price=125.0, price_acceptance_probability=0.06, weighted_volume_contribution=6.0, coverage_count=3),
        MicroAcceptance(index=3, lower_bound=130.0, upper_bound=140.0, center_price=135.0, price_acceptance_probability=0.08, weighted_volume_contribution=8.0, coverage_count=4),
        MicroAcceptance(index=4, lower_bound=140.0, upper_bound=150.0, center_price=145.0, price_acceptance_probability=0.10, weighted_volume_contribution=10.0, coverage_count=5),
        MicroAcceptance(index=5, lower_bound=150.0, upper_bound=160.0, center_price=155.0, price_acceptance_probability=0.12, weighted_volume_contribution=12.0, coverage_count=6),
        MicroAcceptance(index=6, lower_bound=160.0, upper_bound=170.0, center_price=165.0, price_acceptance_probability=0.14, weighted_volume_contribution=14.0, coverage_count=7),
        MicroAcceptance(index=7, lower_bound=170.0, upper_bound=180.0, center_price=175.0, price_acceptance_probability=0.16, weighted_volume_contribution=16.0, coverage_count=8),
        MicroAcceptance(index=8, lower_bound=180.0, upper_bound=190.0, center_price=185.0, price_acceptance_probability=0.12, weighted_volume_contribution=12.0, coverage_count=9),
        MicroAcceptance(index=9, lower_bound=190.0, upper_bound=200.0, center_price=195.0, price_acceptance_probability=0.16, weighted_volume_contribution=16.0, coverage_count=10),
    ]
    regions = [
        RegionDefinition(region_id="R-001", micro_bin_start=0, micro_bin_end=4, lower_bound=100.0, upper_bound=150.0),
        RegionDefinition(region_id="R-002", micro_bin_start=5, micro_bin_end=9, lower_bound=150.0, upper_bound=200.0),
    ]

    result = aggregate_acceptance_map(
        axis,
        micro_acceptances,
        regions,
        coverage_sources_by_bin=[
            frozenset({0}),
            frozenset({1}),
            frozenset({2}),
            frozenset({3}),
            frozenset({4}),
            frozenset({5}),
            frozenset({6}),
            frozenset({7}),
            frozenset({8}),
            frozenset({9}),
        ],
    )

    assert len(result.heatmap) == 10
    assert result.regions[0].region_id == "R-002"
    assert result.regions[0].price_acceptance_probability == 0.7
    assert result.regions[0].price_acceptance_probability == 0.7
    assert result.regions[1].price_acceptance_probability == 0.3


def test_aggregate_acceptance_map_hides_optional_sections() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(index=index, lower_bound=100.0 + index * 10, upper_bound=110.0 + index * 10, center_price=105.0 + index * 10, price_acceptance_probability=0.1, weighted_volume_contribution=10.0, coverage_count=1)
        for index in range(10)
    ]
    regions = [
        RegionDefinition(region_id="R-001", micro_bin_start=0, micro_bin_end=9, lower_bound=100.0, upper_bound=200.0),
    ]

    result = aggregate_acceptance_map(
        axis,
        micro_acceptances,
        regions,
        include_heatmap=False,
        include_diagnostics=False,
    )

    assert result.heatmap is None
    assert result.regions[0].coverage_count is None
    assert result.regions[0].weighted_volume_contribution is None


def test_aggregate_acceptance_map_rejects_invalid_probability_sum() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(index=index, lower_bound=100.0 + index * 10, upper_bound=110.0 + index * 10, center_price=105.0 + index * 10, price_acceptance_probability=0.08, weighted_volume_contribution=10.0, coverage_count=1)
        for index in range(10)
    ]
    regions = [
        RegionDefinition(region_id="R-001", micro_bin_start=0, micro_bin_end=9, lower_bound=100.0, upper_bound=200.0),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        aggregate_acceptance_map(
            axis,
            micro_acceptances,
            regions,
            coverage_sources_by_bin=[frozenset({index}) for index in range(10)],
        )

    assert exc_info.value.code == "INVALID_PROBABILITY_SUM"


def test_aggregate_acceptance_map_rejects_region_gap_even_if_probability_sum_is_one() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(index=index, lower_bound=100.0 + index * 10, upper_bound=110.0 + index * 10, center_price=105.0 + index * 10, price_acceptance_probability=0.1, weighted_volume_contribution=10.0, coverage_count=1)
        for index in range(10)
    ]
    regions = [
        RegionDefinition(region_id="R-001", micro_bin_start=0, micro_bin_end=3, lower_bound=100.0, upper_bound=140.0),
        RegionDefinition(region_id="R-002", micro_bin_start=5, micro_bin_end=9, lower_bound=150.0, upper_bound=200.0),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        aggregate_acceptance_map(
            axis,
            micro_acceptances,
            regions,
            coverage_sources_by_bin=[frozenset({index}) for index in range(10)],
        )

    assert exc_info.value.code == "REGION_GAP_DETECTED"


def test_aggregate_acceptance_map_requires_coverage_sources_for_diagnostics() -> None:
    axis = build_micro_axis(price_min=100.0, price_max=200.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(
            index=index,
            lower_bound=100.0 + index * 10,
            upper_bound=110.0 + index * 10,
            center_price=105.0 + index * 10,
            price_acceptance_probability=0.1,
            weighted_volume_contribution=10.0,
            coverage_count=1,
        )
        for index in range(10)
    ]
    regions = [
        RegionDefinition(
            region_id="R-001",
            micro_bin_start=0,
            micro_bin_end=9,
            lower_bound=100.0,
            upper_bound=200.0,
        ),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        aggregate_acceptance_map(axis, micro_acceptances, regions)

    assert exc_info.value.code == "MISSING_DIAGNOSTIC_CONTEXT"


def test_aggregate_acceptance_map_rejects_micro_probabilities_that_do_not_align_with_axis() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(
            index=9 - index,
            lower_bound=float(9 - index),
            upper_bound=float(10 - index),
            center_price=9.5 - index,
            price_acceptance_probability=0.1,
            weighted_volume_contribution=10.0,
            coverage_count=1,
        )
        for index in range(10)
    ]
    regions = [
        RegionDefinition(
            region_id="R-001",
            micro_bin_start=0,
            micro_bin_end=9,
            lower_bound=0.0,
            upper_bound=10.0,
        ),
    ]

    with pytest.raises(AcceptanceMapError) as exc_info:
        aggregate_acceptance_map(
            axis,
            micro_acceptances,
            regions,
            coverage_sources_by_bin=[frozenset({index}) for index in range(10)],
        )

    assert exc_info.value.code == "REGION_AXIS_MISMATCH"


def test_aggregate_acceptance_map_counts_unique_candles_per_region_when_sources_provided() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(
            index=index,
            lower_bound=float(index),
            upper_bound=float(index + 1),
            center_price=index + 0.5,
            price_acceptance_probability=0.5 if index in (1, 2) else 0.0,
            weighted_volume_contribution=50.0 if index in (1, 2) else 0.0,
            coverage_count=1 if index in (1, 2) else 0,
        )
        for index in range(10)
    ]
    regions = [
        RegionDefinition(
            region_id="R-001",
            micro_bin_start=0,
            micro_bin_end=4,
            lower_bound=0.0,
            upper_bound=5.0,
        ),
        RegionDefinition(
            region_id="R-002",
            micro_bin_start=5,
            micro_bin_end=9,
            lower_bound=5.0,
            upper_bound=10.0,
        ),
    ]

    result = aggregate_acceptance_map(
        axis,
        micro_acceptances,
        regions,
        coverage_sources_by_bin=[
            frozenset(),
            frozenset({0}),
            frozenset({0}),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
        ],
    )

    assert result.regions[0].region_id == "R-001"
    assert result.regions[0].coverage_count == 1


def test_aggregate_acceptance_map_excludes_zero_volume_sources_from_region_coverage_count() -> None:
    axis = build_micro_axis(price_min=0.0, price_max=10.0, micro_bins=10)
    micro_acceptances = [
        MicroAcceptance(
            index=index,
            lower_bound=float(index),
            upper_bound=float(index + 1),
            center_price=index + 0.5,
            price_acceptance_probability=0.5 if index in (8, 9) else 0.0,
            weighted_volume_contribution=50.0 if index in (8, 9) else 0.0,
            coverage_count=1 if index in (1, 2, 8, 9) else 0,
        )
        for index in range(10)
    ]
    regions = [
        RegionDefinition(
            region_id="R-001",
            micro_bin_start=0,
            micro_bin_end=4,
            lower_bound=0.0,
            upper_bound=5.0,
        ),
        RegionDefinition(
            region_id="R-002",
            micro_bin_start=5,
            micro_bin_end=9,
            lower_bound=5.0,
            upper_bound=10.0,
        ),
    ]

    result = aggregate_acceptance_map(
        axis,
        micro_acceptances,
        regions,
        coverage_sources_by_bin=[
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset({1}),
            frozenset({1}),
        ],
    )

    assert result.regions[0].region_id == "R-002"
    assert result.regions[0].coverage_count == 1
    assert result.regions[1].region_id == "R-001"
    assert result.regions[1].coverage_count == 0
