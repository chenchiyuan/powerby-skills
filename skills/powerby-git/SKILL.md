---
name: powerby-git
description: |
  本地 Git 仓库管理技能。负责分支创建与切换、提交合规检查、文件白名单验证、工作区净化。
  当需要创建本地分支、检查提交规范、验证合并前文件合规性、清理临时文件时使用。
  不处理远程分支操作（push/merge/PR）—— 那些由 powerby-github-branch 负责。
compatibility:
  - git
  - local-filesystem
---

# PowerBy Git

本地 Git 仓库的分支与提交管理。确保开发在规范分支上进行，提交信息符合约定，合并前工作区干净合规。

## Purpose

为每次迭代和 Bug 修复提供规范化的本地 Git 操作支撑：分支创建、提交检查、文件合规验证、分支清理。成功使用的标志是：所有开发都在正确命名的分支上进行，提交信息格式规范，合并前无临时文件残留。

## Success criteria

- 分支按 `feature/{name}` 或 `bugfix/{name}` 规范创建
- 提交信息符合 `{type}({scope}): {description}` 格式
- 合并前检查通过：无临时文件、文档完整、所有文件在白名单内
- 失败时给出具体的违规项和修复建议

## Strategy

1. **分支隔离是底线。** 所有功能开发和 Bug 修复必须在独立分支上进行，禁止直接在 main/develop 上提交。这是防止代码混乱的最基本保障。

2. **检查前置于操作。** 在提交前检查文件合规性，在合并前做全量扫描。发现问题立即阻止并报告，不让违规内容进入主分支。

3. **白名单思维。** 只有明确属于项目的文件才合法：业务代码、测试用例、流程文档、用户指定文件。其他一律视为临时文件，合并前必须清理。

4. **清理操作用户主导。** 分支删除和文件清理默认需要用户确认。提供预览模式降低误操作风险。

## Tools and capability boundaries

- **git 命令行**：分支创建/切换、状态查询、提交历史查看
- **文件系统读取**：扫描工作区文件，识别临时文件
- **不做**：远程分支操作（push、远程合并、PR 创建）—— 由 powerby-github-branch 负责
- **不做**：具体的代码开发或审查 —— 由角色技能负责

## Important facts and constraints

### 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| Feature | `feature/{迭代名}` | `feature/user-authentication` |
| Bugfix | `bugfix/{问题简述}` | `bugfix/login-timeout` |
| Hotfix | `hotfix/{版本}-{问题}` | `hotfix/v1.2.3-security-patch` |
| Release | `release/{版本}` | `release/v2.0.0` |

命名规则：小写字母 + 连字符（kebab-case），不超过 50 字符，禁止中文和特殊字符。

### 提交信息格式

```
{类型}({范围}): {描述}
```

类型：feat / fix / docs / style / refactor / test / chore

### 文件白名单

合法文件三类：
1. **业务代码和测试**：`src/`、`lib/`、`tests/`、`*.test.*`、`*.spec.*`
2. **PowerBy 流程文档**：`docs/` 下的 prd.md、architecture.md、tasks.md 等
3. **用户指定文件**：配置文件、README、LICENSE 等

### 临时文件识别

`*.tmp`、`*.log`、`*.debug`、`*.bak`、`*.swp`、`.DS_Store`、`__pycache__/`、`node_modules/`、`.dist/`、`.build/`

## Workflow

1. **创建分支** — 验证类型和名称格式，检查分支是否已存在，从正确的源分支创建并切换。

2. **提交检查** — 提交前验证：提交信息格式、变更文件是否在白名单内、是否包含临时文件。不通过则阻止提交并报告原因。

3. **合并前全量检查** — 扫描工作区所有文件，验证白名单合规性、临时文件清理、PowerBy 文档完整性。

4. **分支清理** — 列出已合并的分支，提供预览（dry-run），用户确认后执行删除。

## Output format

检查通过：
```
检查通过
- 文件合规: N 个文件，全部在白名单内
- 临时文件: 无
- 文档完整性: 通过
```

检查不通过：
```
检查未通过

违规项:
- [E004] 临时文件未清理: debug.log, test.tmp
- [E005] 文档缺失: architecture.md

建议: 删除临时文件后重新提交
```

## Resources

- `templates/` — 分支操作相关模板（如有）

## Subtask / parallelism guidance

- 本技能操作均为本地同步操作，不涉及并行
- 与 powerby-github-branch 配合时：本技能先完成本地检查，通过后由 github-branch 执行远程操作

## Examples

**Example 1: 开始新迭代**
Input: 需要为用户认证功能创建分支
Output: 创建 `feature/user-authentication` 分支并切换。

**Example 2: 合并前检查失败**
Input: 准备合并到 develop，执行全量检查
Output: 发现 debug.log 未清理，阻止合并，建议删除后重试。

## Safety

- 禁止直接在 main/master 上提交代码
- 分支删除操作默认需要用户确认，不自动执行
- 不使用 `git push --force` 或其他破坏性远程操作
- 不覆盖或删除用户明确指定的文件
