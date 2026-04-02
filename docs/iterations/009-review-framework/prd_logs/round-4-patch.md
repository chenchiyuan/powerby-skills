# Patch Report: Round 4
**Date**: 2026-03-27

## Fixed Issues

| Issue ID | Type | Fix Description |
|----------|------|-----------------|
| 001 | BLOCKER | 统一 Skill 协议：新增 4.3 协议一致性规则，引入 context_writes 机制，所有 Skill 输出统一为 status/objects/relations/conflicts/gaps/context_writes/metadata/errors 格式 |
| 002 | BLOCKER | 证据驱动原则：Object Record.confidence 枚举移除 uncertain，ProductReconstructor 证据要求改为"无证据时记录 gap，不生成对象" |
| 003 | MAJOR | 数据流修复：Review Context 新增 current_facts 字段，ConflictResolver 通过 context_writes 写入，所有下游 Skill 输入改为从 context.current_facts 读取 |
| 004 | MAJOR | V2 对象类型：Object Record.object_type 枚举新增 module/entity/code_unit/entry_point/test/observability，支持 V2 User Stories |
| 005 | MAJOR | GapAnalyzer 输出补全：新增 conflicts 数组输出，与 US-007 验收标准对齐 |
| 006 | MAJOR | RelationBuilder 范围收缩：移除 Feature → Feature (parent/child) 关系，仅保留 supports 和 constrains，符合 REQ-006 承诺范围 |

## Deferred Issues (MINOR)

| Issue ID | Type | Reason |
|----------|------|--------|
| 007 | MINOR | 状态定义细化 - 本轮不修复 |
| 008 | MINOR | Evidence Unit source_type 枚举补充 pr - 本轮不修复 |
| 009 | MINOR | 协作示例格式对齐 - 本轮不修复 |
