# Patch Report: Round 1
**Date**: 2026-03-27

## Fixed Issues

| Issue ID | Type | Fix Description |
|----------|------|-----------------|
| 001 | BLOCKER | pb-review 编排器输出格式统一为 Skill 协议标准结构（status/objects/relations/conflicts/gaps/context_writes/metadata/errors），report_path 移入 metadata |
| 002 | BLOCKER | EvidenceCollector 输入明确标注从 `context.project_metadata.resource_inventory` 读取资料清单，不在 parameters 中直接引用上游输出 |
| 003 | MAJOR | 新增 registry 文件追加写入机制说明：读取-去重-合并-写入流程，基于唯一 ID 去重保证幂等性 |
| 004 | MAJOR | 修正架构追溯矩阵：FP-001 由 Section 5.1 统一协议定义覆盖，C-001 编排器对应 FP-008 编排层 |
| 005 | MAJOR | 增强断点恢复设计：checkpoint.json 新增 completed_writes 字段，定义写入顺序（先 registry 后 checkpoint）和恢复时校验机制 |

## Deferred Issues (MINOR)

| Issue ID | Type | Reason |
|----------|------|--------|
| 006 | MINOR | include/exclude_patterns 默认值 - 本轮不修复 |
| 007 | MINOR | 数据流图 object_registry 重复标注 - 本轮不修复 |
| 008 | MINOR | mtime 回退逻辑未在组件中落地 - 本轮不修复 |
