# Patch Report: Round 4
**Date**: 2026-03-06
**Architect**: powerby-asp-architect (Refinery Mode)

## Fixed Issues

### BLOCKER #016: 合并方向被写反

**原问题**: `proposal.md` 与 `function-points.md` 明确要求在 P8 将 feature 分支合并到 `develop`；但 `Merge Conflict Detector` 的核心逻辑把 `targetBranch` 直接作为 `git merge` 参数，而 6.2 生命周期在未先切换到 `develop` 的前提下直接执行 `git merge ... develop`。按当前数据流，实际发生的是"在 feature 分支上把 develop 合进来"，而不是"把 feature 合入 develop"。

**修复方案**:
1. 更新 `Merge Conflict Detector` 核心逻辑（3.2 组件 3）：
   - 步骤 1：保存当前分支名（sourceBranch，即 feature 分支）
   - 步骤 2：切换到目标分支（targetBranch，即 develop）
   - 步骤 3：执行 `git merge --no-commit --no-ff <sourceBranch>`（预检测）
   - 步骤 4/5：无论成功或失败，都要切换回源分支

2. 更新分支合并流程图（4.3）：
   - 在"执行正式合并"前增加"切换到目标分支 develop"步骤
   - 明确标注"执行正式合并 git merge --no-ff feature分支"

3. 更新 `mergeIterationBranch()` 执行流程（5.1.3）：
   - 步骤 2：明确"切换到 targetBranch，执行 `git merge --no-commit --no-ff <sourceBranch>`"
   - 步骤 4：明确"切换到 targetBranch，执行正式合并 `git merge --no-ff <sourceBranch>`"

4. 更新完整生命周期图（6.2）：
   - 在预检测前增加"保存当前分支名"和"checkout develop"步骤
   - 在预检测后增加"checkout feature分支（切回源分支）"步骤
   - 在正式合并前增加"checkout develop（切换到目标分支）"步骤
   - 明确标注"merge --no-ff feature分支（正式合并）"

**修复位置**:
- `architecture.md:279-293` (更新 Merge Conflict Detector 核心逻辑)
- `architecture.md:576-579` (更新 4.3 流程图)
- `architecture.md:724-730` (更新 5.1.3 执行流程)
- `architecture.md:1073-1091` (更新 6.2 生命周期图)

---

### MAJOR #017: 分支历史报告数据契约自相矛盾

**原问题**: 文档一方面在 5.1.5 和组件说明中明确"合并前生成初始报告，不含合并记录/初始为空"，另一方面又在 5.2.2 将 `merge_record` 定义为必填 `MergeRecord`，其中 `merged_at`、`merged_by`、`merge_commit_hash` 都是必填字符串。当前架构没有说明初始报告应使用 `null`、占位值还是省略字段。

**修复方案**:
1. 更新 `BranchHistoryReport` 接口定义（5.2.2）：
   - 将 `merge_record: MergeRecord` 改为 `merge_record: MergeRecord | null`
   - 添加注释："初始为 null，合并后补充"

**修复位置**:
- `architecture.md:875` (更新 BranchHistoryReport 接口)

---

### MAJOR #018: 多个破坏性 API 缺失显式错误契约

**原问题**: `createIterationBranch()` 明确列出了异常类型，但 `mergeIterationBranch()`、`deleteIterationBranch()`、`generateBranchHistoryReport()`、`updateBranchHistoryReport()` 只给出成功返回结构/前置条件，没有把"冲突检测失败""`git merge --abort` 回滚失败""当前分支不可删""报告不存在""文件写入失败""Git 提交失败"等场景收敛为显式错误码或异常类型。

**修复方案**:
1. 为 `mergeIterationBranch()` 新增错误处理契约（5.1.3）：
   - 冲突检测失败 → 返回 `{ success: false, hasConflict: true, conflictFiles: [...] }`
   - `git merge --abort` 回滚失败 → 抛出 `MergeRollbackError`
   - 切换到目标分支失败 → 抛出 `BranchCheckoutError`
   - 正��合并失败 → 抛出 `MergeExecutionError`
   - 更新报告失败 → 抛出 `ReportUpdateError`
   - Git 提交失败 → 抛出 `GitCommitError`
   - 分支状态更新失败 → 抛出 `StateUpdateError`

2. 为 `deleteIterationBranch()` 新增错误处理契约（5.1.4）：
   - 分支状态不是 `merged` → 抛出 `BranchNotMergedError`
   - 当前分支是待删除分支 → 抛出 `CannotDeleteCurrentBranchError`
   - 分支删除失败 → 抛出 `BranchDeletionError`
   - 分支状态更新失败 → 抛出 `StateUpdateError`

3. 为 `generateBranchHistoryReport()` 新增错误处理契约（5.1.5）：
   - 分支信息不存在 → 抛出 `BranchInfoNotFoundError`
   - Git 提交历史获取失败 → 抛出 `GitHistoryFetchError`
   - 报告文件写入失败 → 抛出 `FileWriteError`
   - Git 提交失败 → 抛出 `GitCommitError`

4. 为 `updateBranchHistoryReport()` 新增错误处理契约（5.1.6）：
   - 报告文件不存在 → 抛出 `ReportFileNotFoundError`
   - 报告文件读取失败 → 抛出 `FileReadError`
   - 报告文件写入失败 → 抛出 `FileWriteError`
   - Git 提交失败 → 抛出 `GitCommitError`

**修复位置**:
- `architecture.md:723-730` (新增 5.1.3 错误处理)
- `architecture.md:760-779` (新增 5.1.4 错误处理)
- `architecture.md:816-823` (新增 5.1.5 错误处理)
- `architecture.md:854-861` (新增 5.1.6 错误处理)

---

## Summary

本轮修复了 1 个 BLOCKER 和 2 个 MAJOR 问题，主要涉及：
1. 修正合并方向（将 feature 合入 develop，而非反向）
2. 修正分支历史报告数据契约（merge_record 改为可空）
3. 补充所有破坏性 API 的显式错误契约

所有修复均遵循宪法原则（显式优于隐式），确保架构与产品文档严格对齐，并为 ASP 上层提供可靠的错误分流机制。
