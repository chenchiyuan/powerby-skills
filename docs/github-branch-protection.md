# GitHub分支保护配置指南

## 概述

本文档说明如何配置GitHub分支保护规则，确保代码质量和迭代流程的规范性。

## 分支策略

### 分支命名规范
```
main                 # 生产就绪代码
develop              # 开发集成分支
feature/{id}-{desc}  # 功能分支
bugfix/{id}-{desc}   # Bug修复分支
hotfix/{id}-{desc}   # 紧急修复分支
release/{version}    # 发布分支
```

### 分支用途说明

#### main分支
- **用途**: 生产就绪代码
- **保护**: 强制PR，2个审查者
- **触发**: 自动release
- **策略**: 只接受来自develop或hotfix的PR

#### develop分支
- **用途**: 开发集成分支
- **保护**: 强制PR，1个审查者
- **合并**: 每周五合并到main
- **策略**: 接受feature和bugfix分支

#### feature分支
- **用途**: 新功能开发
- **命名**: feature/001-user-authentication
- **生命周期**: 功能完成后删除
- **分支源**: 从develop创建

#### bugfix分支
- **用途**: Bug修复
- **命名**: bugfix/002-login-error
- **优先级**: P0/P1直接合并到main
- **分支源**: 从main或develop创建

#### hotfix分支
- **用途**: 紧急修复
- **命名**: hotfix/003-security-vulnerability
- **触发**: P0安全漏洞
- **流程**: 修复后合并到main和develop

## 分支保护规则配置

### main分支保护
```yaml
# 在GitHub仓库设置中配置
branch: main
required_status_checks:
  strict: true
  checks:
    - ci
    - validate-docs
    - security-audit
enforce_admins: true
required_pull_request_reviews:
  required_approving_review_count: 2
  dismiss_stale_reviews: true
  require_code_owner_reviews: true
  require_last_push_approval: true
restrictions: null
allow_force_pushes: false
allow_deletions: false
```

### develop分支保护
```yaml
branch: develop
required_status_checks:
  strict: false
  checks:
    - ci
    - validate-docs
enforce_admins: false
required_pull_request_reviews:
  required_approving_review_count: 1
  require_code_owner_reviews: false
restrictions: null
allow_force_pushes: false
```

## GitHub CLI配置命令

### 启用分支保护
```bash
# main分支保护
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"checks":["ci","validate-docs"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":2,"dismiss_stale_reviews":true}'

# develop分支保护
gh api repos/{owner}/{repo}/branches/develop/protection \
  --method PUT \
  --field required_status_checks='{"strict":false,"checks":["ci"]}' \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

### 查看保护规则
```bash
# 查看所有分支保护
gh api repos/{owner}/{repo}/branches --jq '.[].name'

# 查看特定分支保护
gh api repos/{owner}/{repo}/branches/main/protection
```

## 工作流程示例

### 创建功能分支
```bash
# 从develop创建feature分支
git checkout develop
git pull origin develop
git checkout -b feature/004-new-skill

# 开发工作
git add .
git commit -m "feat: add new powerby-skill

- Implement skill initialization
- Add configuration options
- Include documentation

Closes #123"
git push origin feature/004-new-skill

# 创建PR到develop
gh pr create \
  --title "feat: add new powerby-skill" \
  --body "## Summary
Add new powerby-skill with enhanced capabilities

## Changes
- Feature implementation
- Documentation update
- Test coverage

## Testing
- Unit tests: ✅
- Integration tests: ✅" \
  --base develop \
  --head feature/004-new-skill
```

### 合并到main
```bash
# 确保develop是最新的
git checkout develop
git pull origin develop

# 合并到main（通过PR）
gh pr create \
  --title "chore: merge feature/004 to main" \
  --body "## Release Summary
- Version: v1.1.0
- Features: 1 new skill
- Fixes: 2 bugs
- Documentation: Updated" \
  --base main \
  --head develop
```

### 紧急修复流程
```bash
# 创建hotfix分支
git checkout main
git pull origin main
git checkout -b hotfix/005-critical-bug

# 快速修复
git add .
git commit -m "fix: critical security vulnerability

- Patch security hole in authentication
- Add input validation
- Update security headers

Fixes #456"
git push origin hotfix/005-critical-bug

# 创建PR到main
gh pr create \
  --title "hotfix: critical security vulnerability" \
  --body "## Emergency Fix
- Severity: P0
- Impact: All users
- Fix: Input validation and sanitization

## Testing
- Security audit: ✅
- Penetration test: ✅" \
  --base main \
  --head hotfix/005-critical-bug

# 合并后同步到develop
git checkout develop
git merge main
git push origin develop
```

## 自动触发条件

### main分支合并触发
- 自动创建GitHub Release
- 部署到生产环境
- 更新版本标签
- 生成变更日志

### develop分支合并触发
- 运行完整测试套件
- 验证文档完整性
- 更新迭代索引

### feature分支创建触发
- 验证分支命名规范
- 关联迭代跟踪
- 设置自动审查者

## 最佳实践

### 1. PR审查要求
- **main**: 至少2个审查者，CODEOWNERS必需
- **develop**: 至少1个审查者
- **feature**: 1个审查者，自动化检查通过

### 2. 提交信息规范
```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档
- `style`: 格式化
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 3. 审查检查清单
- [ ] 代码遵循项目规范
- [ ] 通过所有CI检查
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 无安全漏洞
- [ ] 性能影响评估

### 4. 合并策略
- **Squash and Merge**: 推荐用于feature分支
- **Rebase and Merge**: 保持线性历史
- **Merge**: 保留完整分支历史（主要分支）

### 5. 分支清理
```bash
# 删除已合并的分支
git branch -d feature/004-new-skill
git push origin --delete feature/004-new-skill

# 清理本地分支
git fetch --prune origin
```

## 配置验证

### 检查保护规则
```bash
# 查看分支保护状态
gh api repos/{owner}/{repo}/branches/main/protection \
  --jq '.required_status_checks.contexts'

# 查看PR要求
gh api repos/{owner}/{repo}/branches/main/protection \
  --jq '.required_pull_request_reviews.required_approving_review_count'
```

### 验证工作流
```bash
# 测试CI流程
gh workflow run ci.yml

# 查看工作流状态
gh run list
```

## 常见问题

### Q: 如何处理大PR？
A: 拆分为多个小PR，每个PR专注于一个功能或修复。

### Q: 如何处理冲突？
A: 使用 `git rebase` 保持线性历史，冲突解决后强制推送。

### Q: 何时使用force push？
A: 仅在feature分支开发期间，用于更新PR。

### Q: 如何回滚错误的合并？
A: 使用 `git revert` 创建回滚提交，而不是强制回退。

## 参考资源

- [GitHub分支保护文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub Actions工作流](../.github/workflows/)
- [提交信息规范](./commit-message-convention.md)
- [迭代跟踪模板](../.github/ISSUE_TEMPLATE/iteration_tracking.md)

---

**创建时间**: 2025-12-24
**更新版本**: v1.0.0
