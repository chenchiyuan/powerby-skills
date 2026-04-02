# Patch Record: Round 1
**Date**: 2026-03-31
**Based on**: round-1-claude.md

## Fixed Issues

| Issue ID | Type | Fix Summary |
|----------|------|-------------|
| R1-001 | MAJOR | `proposal.md` 的 `REQ-009` 收窄为“CLI 输入 OHLCV 数据文件”，删除未被规格承接的“数据源”表述，消除 `REQ -> Feature` 覆盖缺口 |
| R1-002 | MAJOR | `proposal.md` 明确锁定 CLI 默认 `partition_mode = equal_width`；`FT-007` 同步改为该默认值，消除未锁定默认行为 |
| R1-003 | MAJOR | `proposal.md` 与 `FT-005` 明确收敛一期区域插件合同：`equal_width` 默认 `group_size = 5`；`adaptive_volatility` 采用 `adaptive_group_size = max(1, round(ATR_20 / micro_bin_width))` 的唯一规则 |
| R1-004 | MINOR | `feature-spec-index.md` 的 Oracle / Fixture 完整度从 `100%` 下调为 `90%`，与规格卡当前仍保留的未闭合断言点保持一致 |

## Not Fixed (MINOR, deferred)

无

## Additional Changes

- `FT-005` 新增 `atr_period` 输入、`INVALID_ATR_PERIOD` 错误码及对应测试夹具要求
- `FT-007` 的成功输出样例同步切换为 `equal_width` 默认模式
