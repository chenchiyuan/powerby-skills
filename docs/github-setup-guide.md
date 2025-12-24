# GitHub最佳实践实施指南

## 🚀 快速设置

### 步骤1：启用GitHub仓库功能

#### 1.1 启用GitHub Actions
```bash
# 确保仓库已启用GitHub Actions
# 访问: https://github.com/{owner}/{repo}/actions
```

#### 1.2 配置分支保护规则
```bash
# 使用GitHub CLI配置
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"checks":["ci","validate-docs"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":2}'
```

#### 1.3 配置Secrets（如果需要）
```bash
# 在GitHub仓库设置中添加
# Settings > Secrets and variables > Actions
# 添加必要的secrets（如GITHUB_TOKEN已自动提供）
```

### 步骤2：推送配置到GitHub

```bash
# 添加所有新文件
git add .

# 使用约定式提交
git commit -m "feat: implement GitHub best practices

- Add CI/CD workflows
- Implement automated versioning
- Add branch protection rules
- Create issue templates
- Add commit message convention

Refs #999"

# 推送到GitHub
git push origin main
```

### 步骤3：验证设置

#### 3.1 检查工作流
```bash
# 查看工作流状态
gh run list

# 查看特定工作流日志
gh run view <run-id>
```

#### 3.2 测试PR流程
```bash
# 创建测试分支
git checkout -b test/pr-workflow

# 创建PR
gh pr create \
  --title "test: verify PR workflow" \
  --body "Testing PR workflow automation" \
  --base main \
  --head test/pr-workflow

# 查看PR状态
gh pr view
```

## 📋 配置检查清单

### 必需配置
- [ ] GitHub Actions已启用
- [ ] main分支保护已启用
- [ ] develop分支保护已启用
- [ ] CODEOWNERS文件已配置
- [ ] PR模板已激活
- [ ] Issue模板已激活

### 工作流验证
- [ ] CI工作流在PR时触发
- [ ] Release工作流在main合并时触发
- [ ] 文档工作流在docs变更时触发
- [ ] 安全工作流定期运行

### 自动化验证
- [ ] 版本号自动计算
- [ ] 变更日志自动生成
- [ ] GitHub Release自动创建
- [ ] 文档自动部署

## 🔧 常见问题解决

### 问题1：工作流未触发
**原因**: GitHub Actions未启用或权限不足
**解决**:
```bash
# 检查仓库设置
# Settings > Actions > General > Workflow permissions
# 选择 "Read and write permissions"
```

### 问题2：分支保护规则冲突
**原因**: 本地推送被拒绝
**解决**:
```bash
# 拉取最新更改
git fetch origin
git rebase origin/main

# 通过PR合并而非直接推送
```

### 问题3：PR审查要求过高
**原因**: 分支保护规则配置过于严格
**解决**:
```bash
# 临时禁用保护（仅用于测试）
gh api repos/{owner}/{repo}/branches/main/protection \
  --method DELETE

# 调整审查者数量
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

### 问题4：版本计算错误
**原因**: Git历史中没有标签
**解决**:
```bash
# 创建初始标签
git tag v0.0.0
git push origin v0.0.0

# 重新运行发布工作流
```

## 📊 监控工作流状态

### GitHub界面
```
https://github.com/{owner}/{repo}/actions
```

### 命令行监控
```bash
# 查看最近的工作流运行
gh run list --limit 10

# 查看特定工作流详情
gh run view <run-id> --log

# 查看工作流统计
gh api repos/{owner}/{repo}/actions/runs \
  --jq '.workflow_runs[] | {id: .id, status: .status, conclusion: .conclusion}'
```

### 通知设置
```yaml
# 在仓库设置中配置
# Settings > Notifications > Actions
# 选择通知方式：
# - Email
# - Slack (通过webhook)
```

## 🎯 最佳实践建议

### 1. 定期维护
```bash
# 每周检查
- 查看工作流成功率
- 审查未解决的PR
- 更新依赖项

# 每月检查
- 清理已合并的分支
- 更新文档
- 回顾提交规范
```

### 2. 团队培训
```bash
# 确保团队成员了解：
- GitFlow分支策略
- 约定式提交规范
- PR审查流程
- Issue报告模板
```

### 3. 持续改进
```bash
# 收集反馈
- 工作流运行时间
- 审查效率
- 自动化覆盖率

# 优化流程
- 调整分支保护规则
- 改进PR模板
- 优化工作流性能
```

## 📚 扩展资源

### 官方文档
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [分支保护文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests)
- [工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

### 社区资源
- [GitHub Actions市场](https://github.com/marketplace/actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [Actions示例](https://github.com/actions/starter-workflows)

### 学习路径
1. 学习GitHub Actions基础
2. 理解YAML工作流语法
3. 掌握分支保护规则
4. 实践CI/CD流程
5. 探索高级功能

## 🆘 获取帮助

### 内部支持
- 查看项目文档：`docs/github-*.md`
- 检查issue模板：`.github/ISSUE_TEMPLATE/`
- 审阅现有PR和issue

### 外部资源
- [GitHub社区论坛](https://github.community/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/github-actions)
- [GitHub支持](https://support.github.com/)

### 报告问题
使用项目提供的Bug报告模板：
```bash
gh issue create \
  --title "[Bug]: GitHub workflow issue" \
  --body "## 问题描述
描述遇到的问题...

## 重现步骤
1. ...
2. ...

## 预期行为
描述预期结果

## 实际行为
描述实际结果

## 环境信息
- GitHub Actions: latest
- 分支: main
- 工作流: ci.yml" \
  --label "bug,github-actions"
```

---

**创建时间**: 2025-12-24
**适用版本**: v1.0.0
**维护者**: PowerBy Team
