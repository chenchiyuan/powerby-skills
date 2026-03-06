# Patch Record: Round 4
**Date**: 2026-02-10
**Based on**: round-4-codex.md
**Spec Version**: v2.3.0 → v2.3.1

## Fixed Issues

| Issue ID | Type | Fix Summary |
|----------|------|-------------|
| R4-001 | MAJOR | spec.md US-012 正向覆盖检查前提从写死"REQ-001 到 REQ-023"改为动态"proposal.md 包含需求清单（REQ-xxx）" |
| R4-002 | MAJOR | spec.md US-029 语法校验增加最大重试 3 次限制，超限向用户报告错误由用户决定是否继续 |

## Not Fixed (MINOR, deferred)

| Issue ID | Type | Reason |
|----------|------|--------|
| R4-003 | MINOR | 禁用模糊词字面量出现在规则定义中，继承自 R2-003，当轮不修复 |
| R4-004 | MINOR | 五阶段表述未纳入 Gate 0，继承自 R1-007，当轮不修复 |
