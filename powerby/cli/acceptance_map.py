"""价格接受度地图 CLI。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from powerby.acceptance_map import analyze_acceptance_map
from powerby.acceptance_map.contracts import AcceptanceMapError
from powerby.acceptance_map.serializer import dump_json, to_serializable


def build_parser(*, add_help: bool = True) -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""

    parser = argparse.ArgumentParser(
        description="分析 OHLCV 价格接受度地图",
        add_help=add_help,
    )
    parser.add_argument("--input-file", required=True, help="本地 OHLCV JSON 文件路径")
    parser.add_argument("--output-format", default="json", help="输出格式，一期只支持 json")
    parser.add_argument(
        "--partition-mode",
        default="equal_width",
        help="区域划分模式",
    )
    parser.add_argument("--no-heatmap", action="store_true", help="关闭热力图输出")
    parser.add_argument(
        "--no-diagnostics",
        action="store_true",
        help="关闭诊断字段输出",
    )
    return parser


def _load_payload(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AcceptanceMapError(
            "INPUT_FILE_NOT_FOUND",
            "指定的 OHLCV 输入文件不存在",
            {"input_file": str(path)},
        )
    if not path.is_file():
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "输入文件无法解析为合法 OHLCV 数据",
            {"input_file": str(path)},
        )

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcceptanceMapError(
            "INPUT_PARSE_ERROR",
            "输入文件无法解析为合法 OHLCV 数据",
            {"input_file": str(path)},
        ) from exc


def run_parsed_args(args: argparse.Namespace) -> int:
    """执行已完成参数解析的 CLI 主流程。"""

    if args.output_format != "json":
        error = AcceptanceMapError(
            "UNSUPPORTED_OUTPUT_FORMAT",
            "当前版本仅支持 JSON 输出",
            {"output_format": args.output_format},
        )
        print(dump_json(error.to_dict()), file=sys.stderr)
        return 1

    try:
        payload = _load_payload(Path(args.input_file))
        result = analyze_acceptance_map(
            payload,
            partition_mode=args.partition_mode,
            include_heatmap=not args.no_heatmap,
            include_diagnostics=not args.no_diagnostics,
        )
    except AcceptanceMapError as exc:
        print(dump_json(exc.to_dict()), file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover
        error = AcceptanceMapError(
            "ANALYSIS_FAILED",
            "价格接受度分析失败，请检查错误详情",
            {"exception_type": type(exc).__name__},
        )
        print(dump_json(error.to_dict()), file=sys.stderr)
        return 1

    print(dump_json(to_serializable(result)))
    return 0


def main(argv: list[str] | None = None) -> int:
    """执行 CLI 主流程。"""

    parser = build_parser()
    args = parser.parse_args(argv)
    return run_parsed_args(args)


if __name__ == "__main__":
    raise SystemExit(main())
