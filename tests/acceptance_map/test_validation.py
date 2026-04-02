from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from powerby.acceptance_map.validation import validate_and_normalize_analysis_input
from powerby.acceptance_map.contracts import AcceptanceMapError
from tests.acceptance_map.helpers import make_ohlcv_payload


def test_validate_and_normalize_analysis_input_accepts_valid_payload() -> None:
    payload = make_ohlcv_payload(500)

    result = validate_and_normalize_analysis_input(payload)

    assert result.symbol == "BTCUSDT"
    assert result.timeframe == "4h"
    assert result.sample_size == 500
    assert result.market_hint == "crypto"
    assert result.price_min < result.price_max
    assert len(result.candles) == 500


def test_validate_and_normalize_analysis_input_accepts_small_positive_sample() -> None:
    payload = make_ohlcv_payload(12)

    result = validate_and_normalize_analysis_input(payload)

    assert result.sample_size == 12


def test_validate_and_normalize_analysis_input_rejects_empty_sample() -> None:
    payload = make_ohlcv_payload(1)
    payload["candles"] = []

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INVALID_SAMPLE_SIZE"


def test_validate_and_normalize_analysis_input_rejects_duplicate_timestamp() -> None:
    payload = make_ohlcv_payload(500)
    payload["candles"][10]["timestamp"] = payload["candles"][9]["timestamp"]

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INVALID_ORDERING"


def test_validate_and_normalize_analysis_input_rejects_invalid_ohlc_relation() -> None:
    payload = make_ohlcv_payload(500)
    payload["candles"][0]["high"] = payload["candles"][0]["low"] - 1

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INVALID_PRICE_RELATION"


def test_validate_and_normalize_analysis_input_rejects_nan_values() -> None:
    payload = make_ohlcv_payload(500)
    payload["candles"][0]["high"] = "NaN"

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INPUT_PARSE_ERROR"


def test_validate_and_normalize_analysis_input_rejects_numeric_strings() -> None:
    payload = make_ohlcv_payload(500)
    payload["candles"][0]["open"] = "100.5"

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INPUT_PARSE_ERROR"


def test_validate_and_normalize_analysis_input_rejects_non_string_market_hint() -> None:
    payload = make_ohlcv_payload(500)
    payload["market_hint"] = ["crypto"]

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INPUT_PARSE_ERROR"


def test_validate_and_normalize_analysis_input_rejects_empty_market_hint() -> None:
    payload = make_ohlcv_payload(500)
    payload["market_hint"] = ""

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INPUT_PARSE_ERROR"


def test_validate_and_normalize_analysis_input_rejects_mixed_uncomparable_timestamps() -> None:
    payload = make_ohlcv_payload(500)
    payload["candles"][1]["timestamp"] = "2026-01-01T00:00:00Z"

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INVALID_ORDERING"


def test_validate_and_normalize_analysis_input_rejects_timestamp_gap_for_integer_series() -> None:
    payload = make_ohlcv_payload(500)
    payload["candles"][250]["timestamp"] += 1

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INVALID_ORDERING"


def test_validate_and_normalize_analysis_input_accepts_continuous_iso8601_timestamps() -> None:
    payload = make_ohlcv_payload(500)
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for index, candle in enumerate(payload["candles"]):
        candle["timestamp"] = (base + timedelta(hours=4 * index)).isoformat().replace("+00:00", "Z")

    result = validate_and_normalize_analysis_input(payload)

    assert result.sample_size == 500


def test_validate_and_normalize_analysis_input_rejects_non_iso8601_string_timestamp() -> None:
    payload = make_ohlcv_payload(500)
    payload["candles"][0]["timestamp"] = "2026/01/01 00:00:00"

    with pytest.raises(AcceptanceMapError) as exc_info:
        validate_and_normalize_analysis_input(payload)

    assert exc_info.value.code == "INPUT_PARSE_ERROR"
