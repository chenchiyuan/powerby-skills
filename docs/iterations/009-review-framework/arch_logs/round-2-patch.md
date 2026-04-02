# Patch Report: Round 2
**Date**: 2026-03-27

## Fixed Issues

| Issue ID | Type | Fix Description |
|----------|------|-----------------|
| 001 | BLOCKER | Section 5.1 新增 evidence_policy 协议定义（required_sources/min_confidence/allow_inference 三字段），C-002~C-009 各组件均已声明各自的 evidence_policy |
| 002 | BLOCKER | C-005/C-006/C-007/C-008 各组件持久化说明统一补充"编排器将 gaps 归集到 gap_registry.json（追加去重）"，C-008 同时补充 conflicts 归集路径 |
| 003 | MAJOR | 新增 Section 5.4 归集与持久化职责，明确"Skill 只负责计算和返回结果，编排器负责所有持久化操作"。Section 4.2 行 681 添加注释强化。序列图（Section 4.1）已一致显示 Orch 执行写入。消除了 Skill 直接写文件 vs 编排器归集的矛盾 |
| 004 | MAJOR | 追溯矩阵 C-001 修正为"跨功能点（cross-cutting）"，不再映射到 FP-008。新增独立行：Section 5.1 统一 Skill 协议 → FP-001。消除 C-001/C-002 同时映射 FP-008 的冲突 |
| 005 | MAJOR | C-003 EvidenceCollector（行 229）新增 Spec 偏差说明，明确标注 spec Section 5.2 将 resource_inventory 声明为直接参数，本架构按协议 rule 4 修正为从 context 读取，spec 需同步更新 |

## Deferred Issues (MINOR)

| Issue ID | Type | Reason |
|----------|------|--------|
| 006 | MINOR | include/exclude_patterns 默认值占位符 - 延续 R1-006，本轮不修复 |
| 007 | MINOR | 数据流图 object_registry 重复标注 - 延续 R1-007，本轮不修复 |
| 008 | MINOR | mtime 回退逻辑未在组件中落地 - 延续 R1-008，本轮不修复 |
| 009 | MINOR | ReviewContext 物理实现未显式声明 - 已由 Section 5.3 修复（超出 MINOR 范围但顺带解决） |

## Notes
- Issue 009 虽标记为 MINOR，但在修复 003 时顺带通过 Section 5.3 解决了 ReviewContext 物理实现的显式声明
