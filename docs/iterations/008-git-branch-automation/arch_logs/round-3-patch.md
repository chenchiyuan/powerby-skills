# Patch Report: Round 3
**Date**: 2026-03-06
**Architect**: powerby-asp-architect (Refinery Mode)

## Fixed Issues

### BLOCKER #011: FP-008 分支历史报告合并后更新未架构化

**原问题**: 架构定义了 `generateBranchHistoryReport()` 在合并前生成初始报告，但未定义合并后如何更新报告补充合并记录（merged_by, merge_commit_hash）。

**修复方案**:
1. 新增 `updateBranchHistoryReport()` 接口（5.1.6）：
   - 输入：iterationId + mergeRecord
   - 功能：读取已生成的报告，补充合并记录部分，保存更新后的报告
   - 前置条件：branch-history.md 已生成，合并操作已成功完成

2. 更新 `mergeIterationBranch()` 执行流程（5.1.3）：
   - 步骤 5：合并成功后，调用 `updateBranchHistoryReport()` 补充合并记录
   - 步骤 6：提交更新后的报告到目标分支

3. 更新数据流图（4.3 和 6.2）：
   - 在正式合并后增加"更新报告"和"提交更新后的报告"步骤
   - 确保合并记录（merged_by, merge_commit_hash）通过 `getLastCommit()` 获取并写入报告

**修复位置**:
- `architecture.md:775-850` (新增 5.1.6 接口)
- `architecture.md:724-735` (更新 5.1.3 执行流程)
- `architecture.md:565-570` (更新 4.3 流程图)
- `architecture.md:1038-1046` (更新 6.2 生命周期图)
- `architecture.md:1163-1166` (更新 ADR-004)

---

### BLOCKER #012: 缺失 powerby-github-branch 兼容性设计

**原问题**: proposal.md 的 CON-004 和"现有能力复用分析"明确要求兼容 powerby-github-branch 并扩展其方法，但 architecture.md 只复用了 powerby-git，未定义兼容层。

**修复方案**:
1. 在"现有架构继承"章节（2.1）新增 powerby-github-branch 兼容层说明：
   - 明确 powerby-github-branch 是基于 powerby-git 的上层封装
   - 本次设计复用 powerby-git 底层能力，不直接依赖 powerby-github-branch
   - 如需扩展 powerby-github-branch 的方法，可在其内部调用 ASP Integration Module
   - 两者通过 powerby-git 共享 Git 操作能力

2. 更新 ADR-001 标题和内容：
   - 标题改为"扩展 powerby-git 并保持与 powerby-github-branch 兼容"
   - 补充兼容性策略和影响说明

**修复位置**:
- `architecture.md:49-66` (新增 powerby-github-branch 兼容层)
- `architecture.md:1107-1122` (更新 ADR-001)

---

### BLOCKER #013: FP-001 缺失"从 develop 创建"的验证逻辑

**原问题**: proposal.md 和 function-points.md 要求新分支必须从 develop 创建，且 develop 不存在时报错，但架构未设计验证和错误处理流程。

**修复方案**:
1. 更新分支创建流程图（4.1）：
   - 在"Branch does not exist"分支中，增加"检查源分支是否存在"步骤
   - 如源分支不存在 → 返回错误，终止流程
   - 如源分支存在 → 切换到源分支 → 创建新分支

2. 更新 `createIterationBranch()` 接口（5.1.1）：
   - 错误处理：新增 `SourceBranchNotFoundError`（develop 不存在）
   - 错误处理：新增 `PermissionDeniedError`（无分支创建权限）
   - 执行流程：明确 5 步流程，包含源分支存在性检查

**修复位置**:
- `architecture.md:439-485` (更新 4.1 流程图)
- `architecture.md:618-632` (更新 5.1.1 错误处理和执行流程)

---

### BLOCKER #014: FP-003 缺失合并前用户确认步骤

**原问题**: proposal.md REQ-003 和 CON-003 明确要求合并属于破坏性操作，需用户确认后才能执行，但架构流程中只有删除分支设计了确认节点。

**修复方案**:
1. 更新分支合并流程图（4.3）：
   - 在"提交报告到当前分支"后，增加"询问用户是否合并？"决策节点
   - 用户拒绝 → 终止流程
   - 用户确认 → 进入冲突检测

2. 更新 `mergeIterationBranch()` 接口（5.1.3）：
   - 执行流程步骤 1：明确"询问用户是否确认合并（CON-003 破坏性操作需用户确认）"
   - 前置条件：新增"用户必须确认合并操作（破坏性操作）"

3. 更新完整生命周期图（6.2）：
   - 在 P8 阶段，生成报告后增加"询问用户是否合并分支？"交互
   - 用户确认后才调用 `mergeIterationBranch()`

**修复位置**:
- `architecture.md:546-598` (更新 4.3 流程图)
- `architecture.md:724-735` (更新 5.1.3 执行流程和前置条件)
- `architecture.md:1020-1027` (更新 6.2 生命周期图)

---

### MAJOR #015: P8 总流程与分支合规检查自相矛盾

**原问题**: 4.2 定义 P8 阶段必须执行 `checkBranchCompliance()` 检查，但 4.3 和 6.2 的 P8 流程直接生成报告，未先执行检查。

**修复方案**:
1. 更新分支合并流程图（4.3）：
   - 在"P8 阶段开始"后，首先执行"执行 P8 分支合规检查"
   - 检查不通过 → 显示警告 → 用户决策（修复/继续）
   - 检查通过 → 生成报告

2. 更新完整生命周期图（6.2）：
   - 在 P8 阶段开始时，首先调用 `checkBranchCompliance(id, 'P8')`
   - 检查当前分支和工作区状态
   - 不符合规范时显示警告和建议，等待用户决策
   - 检查通过或用户选择继续后，才生成报告

**修复位置**:
- `architecture.md:546-598` (更新 4.3 流程图)
- `architecture.md:1020-1027` (更新 6.2 生命周期图)

---

## Summary

本轮修复了 4 个 BLOCKER 和 1 个 MAJOR 问题，主要涉及：
1. 补充 FP-008 的报告更新机制（新增 `updateBranchHistoryReport()` 接口）
2. 补充 powerby-github-branch 兼容性设计（新增兼容层说明）
3. 补充 FP-001 的源分支验证逻辑（检查 develop 是否存在）
4. 补充 FP-003 的合并前用户确认步骤（破坏性操作需确认）
5. 修正 P8 流程顺序（先执行合规检查，再生成报告）

所有修复均遵循宪法原则（显式优于隐式、借鉴现有代码），确保架构与产品文档严格对齐。
