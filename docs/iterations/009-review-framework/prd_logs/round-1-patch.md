# Patch Report: Round 1
**Date**: 2026-03-27

## Fixed Issues

| Issue ID | Type | Fix Description |
|----------|------|----------------|
| 001 | BLOCKER | US-004 新增 Empty State 和 Error State 定义：无产品文档时返回 partial + 空 Catalog + gap 记录 |
| 002 | BLOCKER | US-005 新增 Empty State 和 Error State 定义：无文档时仅从代码提取功能并标注 code_only |
| 003 | MAJOR | US-003 AC 新增"无法决议"场景：时间/优先级相同但内容矛盾时标记为 unresolved |
| 004 | MAJOR | Object Record object_type 枚举新增 constraint 和 non_goal，与 ProductReconstructor 输出对齐 |
| 005 | MAJOR | US-006 AC 新增关系证据不足时的处理：标注 confidence: inferred，无法确定的关系不强行连线 |
| 006 | MAJOR | 统一 Skill 协议新增 evidence_policy 字段（required_sources、min_confidence、allow_inference） |

## Deferred Issues (MINOR)

| Issue ID | Type | Reason |
|----------|------|--------|
| 007 | MINOR | 状态定义细化 - 本轮不修复 |
| 008 | MINOR | Evidence Unit source_type 枚举补充 pr - 本轮不修复 |
| 009 | MINOR | 协作示例格式对齐 - 本轮不修复 |
