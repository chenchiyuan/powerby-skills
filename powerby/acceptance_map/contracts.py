"""价格接受度地图的核心数据合同。"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


def _sanitize_error_context(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    if isinstance(value, list):
        return [_sanitize_error_context(item) for item in value]
    if isinstance(value, dict):
        return {key: _sanitize_error_context(item) for key, item in value.items()}
    return value


@dataclass(slots=True)
class AcceptanceMapError(Exception):
    """带错误码和上下文的确定性异常。"""

    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        Exception.__init__(self, self.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "context": _sanitize_error_context(self.context),
            }
        }


@dataclass(slots=True)
class OhlcvCandle:
    """单根标准化 OHLCV K 线。"""

    timestamp: str | int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(slots=True)
class AnalysisRequest:
    """分析入口的标准化请求。"""

    symbol: str
    timeframe: str
    market_hint: str
    sample_size: int
    price_min: float
    price_max: float
    candles: list[OhlcvCandle]


@dataclass(slots=True)
class MicroBin:
    """底层价格单元。"""

    index: int
    lower_bound: float
    upper_bound: float
    center_price: float


@dataclass(slots=True)
class MicroAxis:
    """完整底层价格轴。"""

    axis_mode: str
    price_min: float
    price_max: float
    micro_bins: int
    bin_width: float
    bins: list[MicroBin]


@dataclass(slots=True)
class MicroAcceptance:
    """单个 micro bin 的概率与诊断结果。"""

    index: int
    lower_bound: float
    upper_bound: float
    center_price: float
    price_acceptance_probability: float
    weighted_volume_contribution: float
    coverage_count: int


@dataclass(slots=True)
class EngineResult:
    """底层概率引擎输出。"""

    time_decay_mode: str
    decay_lambda: float
    micro_acceptances: list[MicroAcceptance]
    probability_sum: float
    coverage_sources_by_bin: list[frozenset[int]]


@dataclass(slots=True)
class RegionDefinition:
    """区域插件产出的统一合同。"""

    region_id: str
    micro_bin_start: int
    micro_bin_end: int
    lower_bound: float
    upper_bound: float


@dataclass(slots=True)
class RegionPartitionResult:
    """区域服务输出。"""

    partition_mode: str
    regions: list[RegionDefinition]
    plugin_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RegionAcceptance:
    """区域级聚合结果。"""

    region_id: str
    lower_bound: float
    upper_bound: float
    price_acceptance_probability: float
    coverage_count: int | None
    weighted_volume_contribution: float | None


@dataclass(slots=True)
class AcceptanceMapResult:
    """最终可被 CLI / Web 消费的结果。"""

    input_summary: dict[str, Any]
    params: dict[str, Any]
    heatmap: list[dict[str, Any]] | None
    regions: list[RegionAcceptance]
