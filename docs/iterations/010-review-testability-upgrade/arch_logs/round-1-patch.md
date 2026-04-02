# Round 1 Patch Notes

**Date**: 2026-03-30
**架构版本**: 1.0.0 → 1.1.0

---

## 修复清单

### MAJOR-001: 新增 D-17~D-20 Evidence Policy

**位置**: §3.2.1 feature-reconstructor

**修复内容**:
- 新增 Evidence Policy 表格，明确 D-17~D-20 各维度的 required_sources、min_confidence、allow_inference
- 明确 `allow_inference: false` — 所有子项状态必须有直接代码证据
- 明确 `missing` 与 `not_applicable` 的使用条件
- 确保符合 Proposal CON-002

### MAJOR-002: 修正 gap_registry 与 difference_registry 混淆

**位置**: §5.5

**修复内容**:
- 将 §5.5 从 "difference_registry 扩展" 改为 "gap_registry 扩展"
- 4 种新增 gap 类型（missing_feature/oracle/fixture_contract/test_traceability）写入 gap_registry
- difference_registry 保持原有语义不变
- 同步更新 §3.2.2 gap-analyzer 的输出描述

### MAJOR-003: 明确 Schema 加载机制

**位置**: §2.4

**修复内容**:
- 将 "Schema 引用协议" 改为 "Schema 加载机制"
- 明确四层加载策略：编排器预加载 → 上下文透传 → Skill 声明依赖 → 脚本文件读取
- 增加加载流程示意图
- 排除"复制到各 Skill 目录"方案（违反 DRY）

### MAJOR-004: 明确 Step 13~16 执行方式和恢复逻辑

**位置**: §3.2.4 编排器设计

**修复内容**:
- 明确 Step 13~16 为 Tier 1 确定性步骤，编排器直接调用 Python 脚本
- 不加载 report-composer Skill，与 Step 1~3 同类
- 每步独立 checkpoint，支持单步恢复
- 恢复前检查前置 registry 完整性
- 同步更新全景图 Tier 4 标签

## MINOR 修复

### MINOR-001: 新增架构决策记录

**位置**: 新增 §八

**修复内容**:
- 新增 4 个 ADR（Architecture Decision Record）
- ADR-001: 扩展复用 vs 新建 Skill
- ADR-002: 数据内嵌 vs 独立注册表
- ADR-003: 独立步骤 vs 子步骤
- ADR-004: gap_registry vs difference_registry

**MINOR-002 未修复**：Schema 版本管理策略为非阻塞项，不在本轮修复范围。
