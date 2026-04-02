---
name: powerby-github-branch
description: |
  远程 GitHub 分支管理技能。负责 GitFlow 策略下的远程分支创建、合并、清理操作。
  当 P1 阶段完成需要创建 feature 分支、P8 完成需要合并到 develop、Bug 修复需要创建 hotfix/bugfix 分支时使用。
  不处理本地提交检查和文件合规验证 —— 那些由 powerby-git 负责。
compatibility:
  - git
  - github
---

# PowerBy GitHub Branch

远程 GitHub 分支的 GitFlow 管理。执行分支创建、合并、清理等远程操作，为 powerby-command、powerby-bugfix 等上游技能提供分支管理能力。

## Purpose

自动化 GitFlow 分支策略的远程执行：在正确的时机从正确的源分支创建目标分支，在流程完成后合并并清理。成功使用的标志是：分支命名规范、源分支正确、合并策略匹配 Bug 级别、操作后状态一致。

## Success criteria

- 分支从正确的源分支创建（feature/bugfix 从 develop，hotfix 从 main）
- 分支命名符合 `{type}/{id}-{name}` 规范
- 合并操作在上游检查通过且用户确认后执行
- hotfix 同时合并到 main 和 develop
- 操作失败时提供回滚指引

## Strategy

1. **所有分支操作必须经过用户确认。** 创建、合并、删除分支都是不可轻易撤销的操作。上游技能提交请求，本技能执行前必须确认用户已同意。

2. **源分支决定合并策略。** feature 和 bugfix 从 develop 创建、合并回 develop；hotfix 从 main 创建、同时合并到 main 和 develop。这是 GitFlow 的核心规则，不可违反。

3. **操作前验证，操作后确认。** 创建前检查分支是否已存在、源分支是否最新；合并前确认无冲突；操作后验证结果。

4. **主分支保护不可绕过。** 禁止直接推送到 main 或 develop，所有变更必须通过分支合并。

## Tools and capability boundaries

- **git 命令行**：分支创建、推送、合并、删除
- **gh CLI**（如可用）：PR 创建、分支保护查询
- **不做**：本地提交检查、文件白名单验证 —— 由 powerby-git 负责
- **不做**：具体的代码开发或审查

## Important facts and constraints

### 分支类型与生命周期

| 分支类型 | 命名格式 | 源分支 | 合并目标 | 触发时机 |
|---------|---------|--------|---------|---------|
| feature | `feature/{id}-{name}` | develop | develop | P1 完成后 |
| bugfix | `bugfix/{id}-{name}` | develop | develop | P2/P3 级 Bug |
| hotfix | `hotfix/{id}-{name}` | main | main + develop | P0/P1 级 Bug |

- 迭代 ID 为 3 位数字（如 001）
- 项目名称为英文 kebab-case

### 与 powerby-git 的职责分工

- **powerby-git**：本地操作 — 分支创建/切换、提交检查、文件合规验证
- **powerby-github-branch**：远程操作 — 推送、远程合并、远程分支清理
- 典型协作流：powerby-git 本地检查通过 -> powerby-github-branch 远程操作

### 用户确认是硬前置

所有创建、合并、删除操作的参数中必须包含 `user_approved=true`，表示上游技能已获得用户同意。缺少此标志时拒绝执行。

## Workflow

1. **接收请求** — 从上游技能（powerby-command、powerby-bugfix 等）接收分支操作请求，包含操作类型、参数和用户确认状态。

2. **验证前置条件** — 检查源分支存在且最新、目标分支名称合规、无重复分支。

3. **执行操作** — 创建分支并推送设置上游跟踪；或执行合并并根据策略推送。

4. **确认结果** — 验证操作成功，返回分支状态信息给上游技能。

5. **清理（如需要）** — 合并后根据用户选择删除源分支，修剪远程引用。

## Output format

```
分支操作完成

操作: {创建/合并/清理}
分支: {分支名}
状态: {成功/失败}
详情: {操作结果描述}
```

## Resources

- 无独立资源文件。分支操作通过 git 命令执行。

## Subtask / parallelism guidance

- 分支操作为串行操作，不支持并行
- 作为下游技能被调用，不主动发起流程

## Examples

**Example 1: P1 完成后创建 feature 分支**
Input: `create_feature_branch(iteration_id="001", project_name="task-manager", user_approved=true)`
Output: 从 develop 创建 `feature/001-task-manager`，推送远程。

**Example 2: P0 级 Bug 创建 hotfix 分支**
Input: `create_bugfix_branch(id="003", name="security-vuln", level="P0", user_approved=true)`
Output: 从 main 创建 `hotfix/003-security-vuln`，推送远程。

**Example 3: P8 完成后合并**
Input: `merge_branch(branch="feature/001-task-manager", target="develop", delete_source=true, user_approved=true)`
Output: 合并到 develop，删除远程 feature 分支。

## Safety

- 禁止在未获得用户确认的情况下执行任何分支创建、合并或删除操作
- 禁止直接推送到 main 或 develop
- 禁止使用 `git push --force`（回滚机制中的 force push 仅在文档中说明，实际执行需用户明确授权）
- 禁止删除未合并的分支（除非用户明确确认丢弃）
