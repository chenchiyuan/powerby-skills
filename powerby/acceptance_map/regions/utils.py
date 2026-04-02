"""区域插件共享工具。"""

from __future__ import annotations

from ..contracts import AcceptanceMapError, MicroAxis, RegionDefinition


def build_regions_by_group_size(
    micro_axis: MicroAxis,
    *,
    group_size: int,
) -> list[RegionDefinition]:
    """根据组宽构建完整区域集合。"""

    if group_size < 1:
        raise AcceptanceMapError(
            "INVALID_PARTITION_CONFIG",
            "区域划分参数非法，无法生成完整区域",
            {"group_size": group_size},
        )

    regions: list[RegionDefinition] = []
    region_index = 1
    start = 0
    while start < micro_axis.micro_bins:
        end = min(start + group_size - 1, micro_axis.micro_bins - 1)
        regions.append(
            RegionDefinition(
                region_id=f"R-{region_index:03d}",
                micro_bin_start=start,
                micro_bin_end=end,
                lower_bound=micro_axis.bins[start].lower_bound,
                upper_bound=micro_axis.bins[end].upper_bound,
            )
        )
        start = end + 1
        region_index += 1

    if not regions:
        raise AcceptanceMapError(
            "INVALID_REGION_COUNT",
            "区域插件未生成有效区域",
            {},
        )
    return regions
