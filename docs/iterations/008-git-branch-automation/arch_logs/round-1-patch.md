# Patch Report: Round 1
**Date**: 2026-03-06
**Architect**: powerby-asp-architect (Refinery Mode)

## Fixed Issues

### BLOCKER #001: 功能点覆盖缺失 - FP-008 Mermaid gitGraph 生成逻辑

**原问题**: Branch History Generator 组件设计中仅提供了报告内容示例，未定义 Mermaid gitGraph 生成逻辑。

**修复方案**:
在 `architecture.md / 组件 4: Branch History Generator` 中补充了完整的 Mermaid gitGraph 生成逻辑：

1. **数据提取**: 从 Git 历史提取提交记录（`git log --oneline --graph`）
2. **节点识别**: 识别分支创建点和合并点
3. **语法构造**: 构造 gitGraph 语法（commit → branch → commit → merge）
4. **特殊场景处理**:
   - 分支尚未合并：省略 checkout 和 merge 行
   - 特殊字符转义：处理提交消息中的引号等字符
   - 复杂度限制：最多显示最近 20 个提交

**修复位置**: `architecture.md:行号（组件 4）`

---

### BLOCKER #002: 功能点覆盖不完整 - FP-005 P6 阶段检查逻辑

**原问题**: Branch Compliance Checker 组件未明确 P6 阶段的检查触发时机和具体检查项。

**修复方案**:
在 `architecture.md / 组件 2: Branch Compliance Checker` 中补充了阶段检查规则：

**核心逻辑更新**:
```javascript
5. IF phase == 'P6' or 'P8':
     调用 isWorkingTreeClean() 检查工作区状态
     IF 有未提交更改:
       生成警告信息 + 提交建议（git commit 或 git stash）
```

**阶段检查规则**:
- **P1 阶段**: 仅检查当前分支是否为 feature/{id}-{name}
- **P6 阶段**: 检查当前分支 + 是否有未提交更改
- **P8 阶段**: 检查当前分支 + 工作区是否干净（必须无未提交更改）

**修复位置**: `architecture.md:行号（组件 2）`

---

### MAJOR #003: 接口定义不完整 - checkBranchCompliance() 用户交互协议

**原问题**: checkBranchCompliance() 方法未定义用户决策传递机制。

**修复方案**:
在 `architecture.md / 5.1.2 checkBranchCompliance` 中明确了职责边界：

**接口定义更新**:
```typescript
interface ComplianceReport {
  compliant: boolean;
  currentBranch: string;
  expectedBranch: string;
  warnings: Warning[];
  // 注意：用户决策由 ASP Integration 层处理，此接口仅返回检查报告
}
```

**用户交互处理**:
- 本方法仅返回检查报告，不处理用户交互
- 用户决策（继续/切换分支/中止）由 ASP Integration 或 ASP Flow 层处理
- 如需切换分支，调用方应调用 `git.checkout(expectedBranch)`

**修复位置**: `architecture.md:行号（5.1.2）`

---

### MAJOR #004: 数据流逻辑缺陷 - 图 4.2 用户交互流程

**原问题**: 图 4.2 中 User 直接向 Compliance 返回决策，但 Compliance 组件无用户交互能力。

**修复方案**:
重新设计了图 4.2"分支规范检查流程"，将用户交互逻辑上移到 ASP Flow 层：

**修正后的数据流**:
1. Compliance 检测到问题 → 返回 `{ compliant: false, warnings: [...] }` 给 Integration
2. Integration 将警告传递给 ASP Flow
3. ASP Flow 显示警告并询问用户决策
4. 用户选择"切换分支" → ASP Flow 调用 Integration → Integration 调用 Git.checkout()
5. 用户选择"继续" → ASP Flow 继续执行后续流程

**修复位置**: `architecture.md:行号（4.2）`

---

### MAJOR #005: 架构追溯矩阵不完整 - FP-005 Git Utils 扩展方法

**原问题**: 表 7.1 中 FP-005 未说明 Git Utils 需要扩展哪些方法。

**修复方案**:
在 `architecture.md / 7.1 功能点 → 组件映射` 中明确了 Git Utils 扩展方法：

**更新内容**:
```
| FP-005: 分支状态检查 | Branch Compliance Checker → Git Utils | 🆕 + 扩展复用 | 调用 isWorkingTreeClean()（新增方法） |
```

**说明**:
- 现有 `getBranchStatus()` 已包含 `isClean` 字段，可直接复用
- 为保持命名一致性，新增 `isWorkingTreeClean()` 方法作为语义化封装
- 该方法在组件 6"Git Utils（扩展复用）"中已定义

**修复位置**: `architecture.md:行号（7.1）`

---

## Additional Improvements

### 补充技术风险 - Mermaid gitGraph 复杂场景处理

在 `architecture.md / 第 8 章 技术风险与缓解措施` 中补充了风险 6：

**风险 6**: 复杂分支结构（多次合并、分支重命名）导致 gitGraph 渲染异常

**缓解措施**:
- 简化 gitGraph 结构，仅显示主分支和当前 feature 分支
- 忽略中间的临时分支和 rebase 操作
- 如果检测到复杂结构，提示用户使用 `git log --graph` 查看完整历史

---

## Summary

本轮修复了 2 个 BLOCKER 和 3 个 MAJOR 问题，主要涉及：
1. 补充 FP-008 的 Mermaid gitGraph 生成逻辑
2. 明确 FP-005 的 P6 阶段检查规则
3. 澄清 checkBranchCompliance() 的职责边界（不处理用户交互）
4. 修正图 4.2 的数据流设计（用户交互上移到 ASP Flow 层）
5. 明确 FP-005 所需的 Git Utils 扩展方法（isWorkingTreeClean()）
6. 补充 Mermaid gitGraph 复杂场景处理的技术风险

所有修复均遵循宪法原则（显式优于隐式、单一职责），未引入新的架构复杂性。

**MINOR 问题处理**:
- MINOR #006（命名不一致）和 MINOR #007（Mermaid 语法风险）已在修复 BLOCKER 和 MAJOR 时一并解决。
