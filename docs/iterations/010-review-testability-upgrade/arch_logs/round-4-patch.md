# Round 4 Patch Notes

**Date**: 2026-03-30
**架构版本**: 1.2.0 → 1.3.0

---

## 修复清单

### R4-MAJOR-001: 组件关系图和写入流中 report-composer 残留

**位置**: §6.1 组件关系图, §4.3 写入流

**修复内容**:
1. §6.1 组件关系图：schema 依赖连线从 `RC` → `PBR`（SCH1/2/3/6 连到 PBR）
2. §6.1 组件关系图：renderer 连线从 `RC → R1~R4` → `PBR → R1~R4`
3. §4.3 写入流：`RC["report-composer"] --> DM` → `PBR["pb-review 编排器 (Step 13~16)"] --> DM`

**验证**: 全文搜索 `report-composer` 确认：仅在以下合法位置出现：
- §3.1 组件总览（FP-003，轻度升级）
- §3.2.3 组件详细设计（FP-003 描述）
- §6.1 组件关系图（RC 节点，仅 FP-003）
- Step 12 相关描述

### R4-MINOR-001: §3.1 重复组件行

**位置**: §3.1 变更组件总览

**修复内容**: 删除重复的 `pb-review (编排器) | 中度升级 | FP-013` 行，保留合并后的 `pb-review (编排器) | 重度升级 | FP-009~013` 行。

### R4-MINOR-002: testability-score-formula 引用收敛

**位置**: §7.1 追溯矩阵

**修复内容**: FP-003 (report-composer) 的 schema 依赖从 `testability-score-formula` 改为 `—`。

**理由**: report-composer (Step 12) 生成测试化摘要时，使用 feature_spec_registry 中已聚合的 testability_status 统计（test_ready/blocked/partial 数量），不直接读取公式 schema。testability_score 的详细计算在 Step 13 由 render_testability_scorecard.py 完成，该脚本由编排器调用，直接读取 schema 文件。
