"""等宽区域插件。"""

from __future__ import annotations

from .utils import build_regions_by_group_size
from ..contracts import AcceptanceMapError, MicroAxis, RegionDefinition


def build_equal_width_regions(
    micro_axis: MicroAxis,
    *,
    group_size: int = 5,
) -> list[RegionDefinition]:
    """按固定组宽构建区域。"""

    if not isinstance(group_size, int) or group_size < 1:
        raise AcceptanceMapError(
            "INVALID_GROUP_SIZE",
            "等宽切分参数非法",
            {"group_size": group_size},
        )
    return build_regions_by_group_size(micro_axis, group_size=group_size)
