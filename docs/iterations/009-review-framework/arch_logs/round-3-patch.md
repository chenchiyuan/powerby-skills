# Patch Report: Round 3
**Date**: 2026-03-27

## Fixed Issues

| Issue ID | Type | Fix Description |
|----------|------|-----------------|
| 001 | MAJOR | Section 6.1 组件架构图修正：移除所有 Skill→FS 的"写入"虚线，改为 Skill→FS 的"读取"虚线（符合 Section 5.3 Skill 从 .review/ 读取），新增 Orch→FS 的"归集写入"实线（符合 Section 5.4 编排器持久化职责） |
| 002 | MAJOR | 修复 Section 编号冲突：第二个 Section 5.2（核心数据结构）重编号为 Section 5.5，避免与 Section 5.2（协议一致性规则）冲突 |
| 003 | MAJOR | 脚本输出路径修正：C-010 collect_evidence.py 和 C-011 parse_git_history.py 的 `--output` 参数改为临时路径（`/tmp/`），新增说明"由 Skill 读取后通过 context_writes 返回给编排器持久化，脚本不直接写入 .review/ 目录" |

## Deferred Issues (MINOR)

| Issue ID | Type | Reason |
|----------|------|--------|
| 004 | MINOR | min_confidence 枚举值缺少 uncertain - 本轮不修复 |
| 005 | MINOR | include/exclude_patterns 默认值占位符 - 延续 R1-006 |
| 006 | MINOR | 数据流图 object_registry 重复标注 - 延续 R1-007 |
| 007 | MINOR | mtime 回退逻辑未在组件中落地 - 延续 R1-008 |
