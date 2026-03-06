# Patch Record: Round 2
**Date**: 2026-02-10
**Based on**: round-2-codex.md
**Spec Version**: v1.1.0 → v1.2.0

## Fixed Issues
| Issue ID | Type | Description | Action |
|----------|------|------------|--------|
| 001 | MAJOR | Codex 审查失败分支破坏审查产物契约 | 修改 US-012 Codex 执行失败 Scenario：失败时仍生成 arch_logs/round-{N}-codex.md 错误报告（STATUS: FAIL），记录错误信息，保持审查产物链完整。该轮视为 FAIL 但 Architect 无需修复（非 spec 问题），直接进入下一轮 |

## Changes Summary
- 更新 US-012 Codex 执行失败 Scenario（错误报告产出 + 审查链完整性）
- 更新 Error State 描述
