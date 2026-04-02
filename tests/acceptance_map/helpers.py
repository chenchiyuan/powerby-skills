from __future__ import annotations

from typing import Any


def make_candle(
    index: int,
    *,
    open_price: float = 100.0,
    high: float = 110.0,
    low: float = 90.0,
    close: float = 105.0,
    volume: float = 1000.0,
) -> dict[str, Any]:
    return {
        "timestamp": index,
        "open": open_price,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    }


def make_ohlcv_payload(count: int = 500) -> dict[str, Any]:
    candles: list[dict[str, Any]] = []
    for index in range(count):
        base = 100.0 + index * 0.1
        candles.append(
            make_candle(
                index,
                open_price=base,
                high=base + 2.0,
                low=base - 2.0,
                close=base + 1.0,
                volume=1000.0 + index,
            )
        )

    return {
        "symbol": "BTCUSDT",
        "timeframe": "4h",
        "candles": candles,
    }
