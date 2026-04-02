"""PowerBy CLI 统一入口。"""

from __future__ import annotations

import argparse

from . import acceptance_map


def build_parser() -> argparse.ArgumentParser:
    """构建顶层 CLI 解析器。"""

    parser = argparse.ArgumentParser(description="PowerBy CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    acceptance_map_parser = subparsers.add_parser(
        "acceptance-map",
        help="分析 OHLCV 价格接受度地图",
        parents=[acceptance_map.build_parser(add_help=False)],
        add_help=True,
    )
    acceptance_map_parser.set_defaults(handler=acceptance_map.run_parsed_args)

    return parser


def main(argv: list[str] | None = None) -> int:
    """执行顶层 CLI 分发。"""

    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is not None:
        return handler(args)

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
