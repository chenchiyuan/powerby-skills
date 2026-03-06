# Patch Record: Round 2
**Date**: 2026-02-09
**Based on**: round-2-codex.md
**Spec Version**: v2.1.0 → v2.2.0

## Fixed Issues

| Issue ID | Type | Fix Summary |
|----------|------|-------------|
| R2-001 | BLOCKER | spec.md US-005 "用户回答模糊"场景：删除"基于已有信息继续/标注不确定项"，改为"明确告知用户该信息为必要项，要求提供明确回答"；"用户要求跳过某轮"场景：删除"基于推断"，改为区分必要/可选信息，必要信息拒绝跳过 |
| R2-002 | MAJOR | spec.md Drafting 阶段 Error State：删除"基于已有信息生成并标注缺失项"，改为"报错并回退到 Discovery 阶段，要求补充缺失信息" |

## Not Fixed (MINOR, deferred)

| Issue ID | Type | Reason |
|----------|------|--------|
| R2-003 | MINOR | 禁用模糊词字面量出现在示例中，属格式层面，当轮不修复 |
| R2-004 | MINOR | 五阶段表述未纳入 Gate 0，继承自 R1-007，当轮不修复 |

## Additional Changes

- spec.md 版本号 v2.1.0 → v2.2.0
