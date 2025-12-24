# 提交信息规范 (Commit Message Convention)

## 概述

PowerBy项目遵循[约定式提交](https://www.conventionalcommits.org/zh-cn/v1.0.0/)规范，确保提交历史清晰、可追溯，并支持自动化版本管理和变更日志生成。

## 格式规范

### 基本格式
```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

### 示例
```
feat(iteration): add new iteration tracking system

Implement automated iteration status updates based on git commits.
Support for multiple iteration types (feature, bugfix, hotfix).
Integrate with GitHub Issues for tracking.

Closes #123
Refs #456
```

## 类型 (Type)

### 主要类型
- **feat**: 新功能 (minor版本增长)
- **fix**: Bug修复 (patch版本增长)
- **docs**: 文档更新
- **style**: 代码格式化，不影响功能
- **refactor**: 重构，既不是新功能也不是修复
- **test**: 添加或修改测试
- **chore**: 构建/工具相关的变动

### 扩展类型
- **perf**: 性能优化
- **ci**: CI/CD配置修改
- **build**: 构建系统或外部依赖修改
- **revert**: 回滚之前的提交
- **workflow**: 工作流配置

## 作用域 (Scope)

### 迭代相关
- `iteration`: 迭代文档和管理
- `prd`: 产品需求文档
- `architecture`: 架构设计
- `tasks`: 任务列表

### 技能相关
- `skill-powerby-product`: 产品经理技能
- `skill-powerby-architect`: 架构师技能
- `skill-powerby-engineer`: 工程师技能
- `skill-powerby-bugfix`: Bug修复技能

### 功能模块
- `auth`: 认证相关
- `docs`: 文档系统
- `workflow`: 工作流自动化
- `release`: 发布管理

## 提交信息模板

### 新功能开发
```
feat(scope): add new feature description

- Detail 1
- Detail 2
- Detail 3

Closes #issue-number
```

### Bug修复
```
fix(scope): resolve critical bug description

Problem:
- Description of the issue

Solution:
- How the issue was fixed

Fixes #issue-number
```

### 文档更新
```
docs(scope): update documentation for feature

Added:
- Section 1
- Section 2

Updated:
- Section 3

Closes #issue-number
```

### 重构
```
refactor(scope): refactor component for better performance

Before:
- Old implementation details

After:
- New implementation details

Performance impact:
- Improved by X%
```

### 测试
```
test(scope): add unit tests for component

Added tests for:
- Function A
- Function B
- Function C

Coverage:
- Before: 60%
- After: 85%
```

## 版本号自动判断

### 版本计算规则
```bash
# 基于提交类型自动计算版本
feat → minor版本+1
fix → patch版本+1
docs/style/refactor/test/chore → patch版本+1（可选）
perf → patch版本+1
```

### 提交历史分析
```bash
# 查看自上次标签以来的提交类型
git log --oneline --grep="^feat" v1.0.0..HEAD  # 新功能
git log --oneline --grep="^fix" v1.0.0..HEAD   # 修复
git log --oneline --grep="^docs" v1.0.0..HEAD  # 文档
```

## 自动化工具集成

### commitlint配置
```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci", "build", "revert"]
    ],
    "scope-enum": [
      2,
      "always",
      ["iteration", "prd", "architecture", "tasks", "skill-powerby-*", "auth", "docs", "workflow", "release"]
    ]
  }
}
```

### pre-commit钩子
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.0.0
    hooks:
      - id: commitizen
  - repo: https://github.com/commitlint/commitlint
    rev: v17.0.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
```

### GitHub Actions检查
```yaml
# .github/workflows/commitlint.yml
name: Commit Lint

on:
  pull_request:
    types: [opened, synchronize, edited]

jobs:
  lint-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: wagoid/commitlint-github-action@v5
```

## 实际示例

### 完整的提交历史
```bash
# 迭代创建
git commit -m "feat(iteration): create 001-task-manager iteration

- Add PRD document
- Add architecture design
- Add task tracking
- Initialize workflow

Refs #100"

# 功能开发
git commit -m "feat(skill-powerby-product): implement MVP prioritization

- Add P0/P1/P2 priority classification
- Integrate with iteration tracking
- Add validation rules
- Update documentation

Closes #101"

# Bug修复
git commit -m "fix(bug-fix): resolve user confirmation timeout

- Increase timeout from 30s to 48h
- Add reminder notifications
- Improve error handling
- Update tests

Fixes #102"

# 文档更新
git commit -m "docs(workflow): update GitHub best practices guide

- Add branch protection rules
- Add automation scripts
- Update workflow diagrams
- Include examples

Refs #103"

# 性能优化
git commit -m "perf(iteration): optimize index generation

- Reduce build time by 40%
- Cache iteration metadata
- Parallel processing
- Add performance tests

Refs #104"

# 测试添加
git commit -m "test(skills): add integration tests

- Test skill initialization
- Test workflow execution
- Test error handling
- Coverage: 80% → 95%

Refs #105"
```

## 提交信息验证

### 本地验证
```bash
# 使用commitizen验证
cz check --rev-range HEAD~5..HEAD

# 使用commitlint验证
commitlint --from HEAD~5 --to HEAD
```

### 自动验证脚本
```bash
#!/bin/bash
# scripts/validate-commits.sh

echo "🔍 Validating commit messages..."

# 检查最近5个提交
for commit in $(git log -5 --pretty=format:"%H"); do
    message=$(git log -1 --pretty=format:"%s" $commit)

    # 验证格式
    if ! echo "$message" | grep -qE '^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .+'; then
        echo "❌ Invalid commit format: $message"
        exit 1
    fi
done

echo "✅ All commits are valid"
```

## 最佳实践

### 1. 提交原子性
- 每个提交只包含一个逻辑变更
- 相关变更可以拆分多个提交
- 避免混合不相关的变更

### 2. 描述清晰
- 使用现在时（"add"而不是"added"）
- 描述做了什么，而不是怎么做
- 提供足够的上下文信息

### 3. 引用相关
- 使用 `Closes` 关闭Issues
- 使用 `Refs` 引用相关变更
- 使用 `#issue-number` 关联问题

### 4. 正文详细
- 解释为什么做这个变更
- 列出具体的变更内容
- 提供测试或验证说明

### 5. 脚注有用
- 包含相关Issue编号
- 列出破坏性变更
- 提供额外上下文

## 错误示例与修正

### ❌ 错误示例
```bash
# 太简单
git commit -m "fix bug"

# 太复杂
git commit -m "fix: fixed the authentication issue that was causing users to not be able to login when they used invalid credentials which was reported in issue #123 by adding proper validation and error handling"

# 无类型
git commit -m "update documentation for new feature"

# 缺少作用域
git commit -m "feat: add powerby-skill"
```

### ✅ 正确示例
```bash
# 简单清晰
git commit -m "fix(auth): resolve login timeout issue

Add proper validation for invalid credentials.
Improve error messaging for users.

Fixes #123"

# 详细但简洁
git commit -m "feat(skill-powerby-product): implement MVP prioritization

- Add P0/P1/P2 classification system
- Integrate with iteration tracking
- Validate requirements consistency

Closes #124"
```

## 工具支持

### IDE集成
- **VSCode**: Conventional Commits扩展
- **IntelliJ**: Git Commit Template插件
- **Vim**: vim-commit-template

### 命令行工具
```bash
# 使用commitizen
cz commit

# 使用git-cz
git cz

# 交互式提交
git commit
```

## 参考资源

- [约定式提交](https://www.conventionalcommits.org/zh-cn/v1.0.0/)
- [GitHub标签](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-releases)
- [语义化版本](https://semver.org/lang/zh-CN/)
- [Angular提交规范](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)

---

**创建时间**: 2025-12-24
**更新版本**: v1.0.0
