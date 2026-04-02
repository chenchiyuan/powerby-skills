# Patch Report: Round 2
**Date**: 2026-03-27

## Fixed Issues

| Issue ID | Type | Fix Description |
|----------|------|----------------|
| 001 | BLOCKER | 新增 US-009 → REQ-011 (V2)：架构事实还原 User Story，含 AC 和 Empty State |
| 002 | BLOCKER | 新增 US-010 → REQ-012 (V2)：实现事实还原 User Story，含 AC 和 Empty State |
| 003 | BLOCKER | 新增 US-011 → REQ-013 (V2)：验证事实还原 User Story，含 AC 和 Empty State |
| 004 | MAJOR | Data Dictionary 新增 Project Metadata 和 Feature State 定义；Review Context 新增 project_metadata 和 feature_state_registry 字段；ProjectScope 输出改为写入 project_metadata；EvidenceCollector 输出改为写入 evidence_registry。Traceability Matrix 更新 REQ-011/012/013 追溯 |

## Deferred Issues (MINOR)

| Issue ID | Type | Reason |
|----------|------|--------|
| 005 | MINOR | 状态定义细化 - 本轮不修复 |
| 006 | MINOR | Evidence Unit source_type 枚举补充 pr - 本轮不修复 |
| 007 | MINOR | 协作示例格式对齐 - 本轮不修复 |
