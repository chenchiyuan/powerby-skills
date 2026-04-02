"""输入校验与标准化。"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any

from .contracts import AcceptanceMapError, AnalysisRequest, OhlcvCandle


def _as_float(value: Any, *, field_name: str, index: int) -> float:
    if isinstance(value, bool) or isinstance(value, str):
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            f"{field_name} 必须为数值",
            {"field": field_name, "index": index},
        )

    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            f"{field_name} 必须为数值",
            {"field": field_name, "index": index},
        ) from exc

    if not math.isfinite(parsed):
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            f"{field_name} 必须为有限数值",
            {"field": field_name, "index": index, "value": value},
        )
    return parsed


def _normalize_timestamp(
    timestamp: str | int,
    *,
    index: int,
) -> tuple[str, int | datetime]:
    if isinstance(timestamp, int):
        return ("int", timestamp)

    if not isinstance(timestamp, str):
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "timestamp 必须为 ISO 8601 字符串或整数",
            {"field": "timestamp", "index": index, "value": timestamp},
        )

    try:
        normalized = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "timestamp 必须为 ISO 8601 字符串或整数",
            {"field": "timestamp", "index": index, "value": timestamp},
        ) from exc

    return ("iso8601", normalized)


def validate_and_normalize_analysis_input(payload: dict[str, Any]) -> AnalysisRequest:
    """校验输入并返回标准化分析请求。"""

    if not isinstance(payload, dict):
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "分析输入必须为对象",
            {"payload_type": type(payload).__name__},
        )

    symbol = payload.get("symbol")
    timeframe = payload.get("timeframe")
    candles_data = payload.get("candles")
    raw_market_hint = payload.get("market_hint")
    market_hint = "crypto" if raw_market_hint is None else raw_market_hint

    if not isinstance(symbol, str) or not symbol.strip():
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "symbol 必须为非空字符串",
            {"field": "symbol"},
        )
    if not isinstance(timeframe, str) or not timeframe.strip():
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "timeframe 必须为非空字符串",
            {"field": "timeframe"},
        )
    if not isinstance(market_hint, str) or not market_hint.strip():
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "market_hint 必须为非空字符串",
            {"field": "market_hint"},
        )
    if not isinstance(candles_data, list):
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "candles 必须为数组",
            {"field": "candles"},
        )
    if len(candles_data) < 1:
        raise AcceptanceMapError(
            "INVALID_SAMPLE_SIZE",
            "历史 K 线数量不足，至少需要 1 根",
            {"sample_size": len(candles_data)},
        )

    candles: list[OhlcvCandle] = []
    timestamps: list[str | int] = []
    normalized_timestamps: list[tuple[str, int | datetime]] = []
    lows: list[float] = []
    highs: list[float] = []

    for index, candle_data in enumerate(candles_data):
        if not isinstance(candle_data, dict):
            raise AcceptanceMapError(
                "INPUT_PARSE_ERROR",
                "candles 数组元素必须为对象",
                {"index": index},
            )

        timestamp = candle_data.get("timestamp")
        if timestamp is None:
            raise AcceptanceMapError(
                "INPUT_PARSE_ERROR",
                "timestamp 为必填字段",
                {"field": "timestamp", "index": index},
            )
        if isinstance(timestamp, bool) or not isinstance(timestamp, (str, int)):
            raise AcceptanceMapError(
                "INPUT_PARSE_ERROR",
                "timestamp 必须为 ISO 8601 字符串或整数",
                {"field": "timestamp", "index": index, "value": timestamp},
            )

        open_price = _as_float(candle_data.get("open"), field_name="open", index=index)
        high = _as_float(candle_data.get("high"), field_name="high", index=index)
        low = _as_float(candle_data.get("low"), field_name="low", index=index)
        close = _as_float(candle_data.get("close"), field_name="close", index=index)
        volume = _as_float(candle_data.get("volume"), field_name="volume", index=index)

        if open_price <= 0 or close <= 0:
            raise AcceptanceMapError(
                "INVALID_PRICE_RELATION",
                "存在非法 K 线价格关系，请检查 high/low/open/close",
                {"index": index},
            )
        if high < max(open_price, close, low) or low > min(open_price, close, high):
            raise AcceptanceMapError(
                "INVALID_PRICE_RELATION",
                "存在非法 K 线价格关系，请检查 high/low/open/close",
                {"index": index},
            )
        if volume < 0:
            raise AcceptanceMapError(
                "INVALID_VOLUME",
                "成交量必须大于或等于 0",
                {"index": index, "volume": volume},
            )

        candle_timeframe = candle_data.get("timeframe")
        if candle_timeframe is not None and candle_timeframe != timeframe:
            raise AcceptanceMapError(
                "MIXED_TIMEFRAME",
                "输入数据必须来自同一时间周期",
                {"index": index, "timeframe": candle_timeframe},
            )

        timestamps.append(timestamp)
        normalized_timestamps.append(_normalize_timestamp(timestamp, index=index))
        lows.append(low)
        highs.append(high)
        candles.append(
            OhlcvCandle(
                timestamp=timestamp,
                open=open_price,
                high=high,
                low=low,
                close=close,
                volume=volume,
            )
        )

    expected_step: int | float | None = None
    timestamp_kind: str | None = None
    for previous_raw, current_raw, previous, current in zip(
        timestamps,
        timestamps[1:],
        normalized_timestamps,
        normalized_timestamps[1:],
    ):
        previous_kind, previous_value = previous
        current_kind, current_value = current
        if current_kind != previous_kind:
            raise AcceptanceMapError(
                "INVALID_ORDERING",
                "输入 K 线时间序列必须严格升序、不可重复且连续",
                {"previous": previous_raw, "current": current_raw},
            )

        try:
            is_invalid_ordering = current_value <= previous_value
        except TypeError as exc:
            raise AcceptanceMapError(
                "INVALID_ORDERING",
                "输入 K 线时间序列必须严格升序、不可重复且连续",
                {"previous": previous_raw, "current": current_raw},
            ) from exc

        if is_invalid_ordering:
            raise AcceptanceMapError(
                "INVALID_ORDERING",
                "输入 K 线时间序列必须严格升序、不可重复且连续",
                {"previous": previous_raw, "current": current_raw},
            )

        if previous_kind == "int":
            current_step = current_value - previous_value
        else:
            current_step = (current_value - previous_value).total_seconds()

        if expected_step is None:
            expected_step = current_step
            timestamp_kind = previous_kind
            continue

        if current_step != expected_step:
            raise AcceptanceMapError(
                "INVALID_ORDERING",
                "输入 K 线时间序列必须严格升序、不可重复且连续",
                {
                    "previous": previous_raw,
                    "current": current_raw,
                    "expected_step": expected_step,
                    "actual_step": current_step,
                    "timestamp_kind": timestamp_kind,
                },
            )

    return AnalysisRequest(
        symbol=symbol.strip(),
        timeframe=timeframe.strip(),
        market_hint=market_hint.strip(),
        sample_size=len(candles),
        price_min=min(lows),
        price_max=max(highs),
        candles=candles,
    )
