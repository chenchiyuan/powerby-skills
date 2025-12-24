# PowerBy迭代流程GitHub最佳实践优化方案

## 1. 现状分析

### 当前PowerBy迭代管理
```
docs/iterations/
├── 001-task-manager/
│   ├── prd.md
│   ├── architecture.md
│   ├── tasks.md
│   └── implementation.md
└── 002-payment-system/
    └── ...
```

**存在的问题**：
- ❌ 缺乏GitHub工作流集成
- ❌ 无自动化版本管理
- ❌ 无自动化发布流程
- ❌ 无代码审查机制
- ❌ 无分支管理策略
- ❌ 无自动化测试集成
- ❌ 无依赖项管理
- ❌ 无发布说明生成

### spec-kit最佳实践参考
```
references/spec-kit/
├── .github/
│   ├── workflows/
│   │   ├── lint.yml
│   │   ├── docs.yml
│   │   └── release.yml
│   └── CODEOWNERS
└── automated scripts for version management
```

## 2. 优化方案

### 2.1 GitHub工作流自动化

#### A. 核心工作流文件

**1. 持续集成工作流** (`.github/workflows/ci.yml`)
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          # 运行所有测试
          npm test
          # 生成测试覆盖率报告
          npm run coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint code
        run: |
          npm run lint
          npm run format-check
```

**2. 自动化发布工作流** (`.github/workflows/release.yml`)
```yaml
name: Release

on:
  push:
    branches: [ main ]
    paths:
      - 'skills/**'
      - 'docs/iterations/**'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Get next version
        id: version
        run: |
          # 自动计算版本号
          echo "new_version=$(npm version patch --no-git-tag-version)" >> $GITHUB_OUTPUT
      - name: Generate changelog
        run: |
          # 从commit生成变更日志
          npm run changelog
      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: v${{ steps.version.outputs.new_version }}
          body_path: CHANGELOG.md
```

**3. 文档自动部署** (`.github/workflows/docs.yml`)
```yaml
name: Deploy Docs

on:
  push:
    branches: [ main ]
    paths: [ 'docs/**' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build docs
        run: |
          npm run build-docs
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist/docs
```

#### B. 版本管理自动化

**版本号策略** (参考spec-kit)
```bash
#!/usr/bin/env bash
# .github/workflows/scripts/get-next-version.sh

# 基于Git标签自动计算版本
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
VERSION=$(echo $LATEST_TAG | sed 's/v//')

# 语义化版本：主版本.次版本.修订版本
# 功能迭代 → 次版本+1
# Bug修复 → 修订版本+1
# 重大变更 → 主版本+1

IFS='.' read -ra VERSION_PARTS <<< "$VERSION"
MAJOR=${VERSION_PARTS[0]:-0}
MINOR=${VERSION_PARTS[1]:-0}
PATCH=${VERSION_PARTS[2]:-0}

# 根据commit消息自动判断版本类型
if git log --oneline $LATEST_TAG..HEAD | grep -qE 'feat|feature'; then
    MINOR=$((MINOR + 1))
else
    PATCH=$((PATCH + 1))
fi

NEW_VERSION="v$MAJOR.$MINOR.$PATCH"
```

### 2.2 分支管理策略

#### GitFlow分支模型
```
main          ←───●────●────●────●────●────
                 │    │    │    │    │
develop       ←───●───●───●───●───●───●───
                 │    │    │    │    │
feature/001   ←───●───●                      (功能分支)
                         │
hotfix/bug001 ←────────────────●────●         (紧急修复)
```

**分支策略**：
- `main`: 生产就绪代码，每次提交触发release
- `develop`: 开发集成分支，每周末合并到main
- `feature/{iteration-id}`: 功能分支，每个迭代创建一个
- `hotfix/{bug-id}`: 紧急修复分支
- `release/{version}`: 发布分支，用于发布前准备

#### 分支保护规则
```yaml
# .github/branch-protection.yml
main:
  required_status_checks:
    strict: true
    contexts: [ci, lint, test]
  enforce_admins: true
  required_pull_request_reviews:
    required_approving_review_count: 2
    dismiss_stale_reviews: true
```

### 2.3 自动化迭代管理

#### A. 迭代创建自动化
```python
# scripts/create-iteration.py

import datetime
import os
import json

def create_iteration(iteration_id, iteration_name, description):
    """自动创建迭代文档结构"""
    iteration_dir = f"docs/iterations/{iteration_id}-{iteration_name.lower()}"

    # 创建目录结构
    os.makedirs(f"{iteration_dir}", exist_ok=True)

    # 生成迭代文档
    templates = {
        "prd.md": "PRD模板",
        "architecture.md": "架构模板",
        "tasks.md": "任务模板",
        "implementation.md": "实施模板"
    }

    for doc, content in templates.items():
        with open(f"{iteration_dir}/{doc}", "w") as f:
            f.write(f"# {doc.replace('.md', '').upper()}\n\n")
            f.write(f"**迭代**: {iteration_id}\n")
            f.write(f"**创建时间**: {datetime.datetime.now()}\n\n")

    # 更新迭代索引
    update_iteration_index(iteration_id, iteration_name, description)

    print(f"✅ 成功创建迭代: {iteration_id}")

def update_iteration_index(iteration_id, name, description):
    """自动更新迭代索引"""
    index_file = "docs/iterations/index.json"

    iterations = []
    if os.path.exists(index_file):
        with open(index_file) as f:
            iterations = json.load(f)

    iterations.append({
        "id": iteration_id,
        "name": name,
        "description": description,
        "status": "active",
        "created_at": datetime.datetime.now().isoformat()
    })

    with open(index_file, "w") as f:
        json.dump(iterations, f, indent=2)
```

#### B. 迭代状态自动化
```python
# scripts/update-iteration-status.py

import json
import subprocess
import datetime

def update_iteration_status(iteration_id, new_status):
    """根据开发进度自动更新迭代状态"""
    index_file = "docs/iterations/index.json"

    with open(index_file) as f:
        iterations = json.load(f)

    for iteration in iterations:
        if iteration["id"] == iteration_id:
            iteration["status"] = new_status
            iteration["updated_at"] = datetime.datetime.now().isoformat()

            # 根据状态自动触发GitHub标签
            if new_status == "completed":
                create_release_tag(iteration_id)

    with open(index_file, "w") as f:
        json.dump(iterations, f, indent=2)

def create_release_tag(iteration_id):
    """创建GitHub标签和发布"""
    version = calculate_version(iteration_id)
    subprocess.run(["git", "tag", f"v{version}"])
    subprocess.run(["git", "push", "origin", f"v{version}"])
```

### 2.4 代码审查机制

#### A. CODEOWNERS文件
```
# .github/CODEOWNERS

# 全局所有者
* @your-username

# 技能相关代码
/skills/powerby-* @your-username
/docs/* @your-username

# 核心架构
/docs/iterations/* @your-username
/docs/architecture/* @your-username
```

#### B. 审查模板
```markdown
<!-- .github/pull_request_template.md -->

## 迭代信息
- [ ] 迭代ID: {iteration-id}
- [ ] 迭代名称: {iteration-name}

## 变更摘要
简要描述本次变更

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 通过所有CI检查

## 关联问题
Closes #{issue-number}
```

### 2.5 自动化测试集成

#### 测试工作流
```yaml
# .github/workflows/test.yml

name: Test

on: [push, pull_request]

jobs:
  unit-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run unit tests
        run: npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  integration-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: npm run test:integration

  e2e-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run E2E tests
        run: npm run test:e2e
```

### 2.6 发布说明自动生成

#### A. 变更日志生成
```bash
#!/usr/bin/env bash
# .github/workflows/scripts/generate-changelog.sh

NEW_VERSION=$1
LAST_TAG=$2

# 生成变更日志
cat > CHANGELOG.md << EOF
# Changelog

## [${NEW_VERSION#v}] - $(date +%Y-%m-%d)

### Added
$(git log --oneline --grep="feat" --format="- %s" $LAST_TAG..HEAD)

### Fixed
$(git log --oneline --grep="fix" --format="- %s" $LAST_TAG..HEAD)

### Changed
$(git log --oneline --grep="docs" --format="- %s" $LAST_TAG..HEAD)

EOF
```

#### B. GitHub Release自动创建
```bash
#!/usr/bin/env bash
# .github/workflows/scripts/create-release.sh

VERSION=$1

gh release create "$VERSION" \
  --title "Release $VERSION" \
  --notes-file CHANGELOG.md \
  --generate-notes
```

### 2.7 依赖项管理

#### 依赖安全检查
```yaml
# .github/workflows/security.yml

name: Security

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security audit
        run: npm audit --audit-level=moderate
      - name: Check for vulnerabilities
        run: npm run security:check
```

## 3. 实施计划

### 第一阶段：基础设置 (Week 1)
- [ ] 创建`.github/workflows/`目录
- [ ] 添加基础CI工作流
- [ ] 设置分支保护规则
- [ ] 配置CODEOWNERS文件

### 第二阶段：自动化版本管理 (Week 2)
- [ ] 实现版本自动计算脚本
- [ ] 配置Git标签自动生成
- [ ] 设置发布工作流
- [ ] 测试版本管理流程

### 第三阶段：迭代自动化 (Week 3)
- [ ] 开发迭代创建脚本
- [ ] 实现状态自动更新
- [ ] 集成GitHub Issues
- [ ] 配置自动化测试

### 第四阶段：文档和发布 (Week 4)
- [ ] 实现变更日志自动生成
- [ ] 配置GitHub Release
- [ ] 部署文档自动化
- [ ] 完整流程测试

## 4. 预期收益

### 开发效率提升
- ✅ 减少手动操作（版本管理、发布、文档更新）
- ✅ 自动化测试和审查
- ✅ 快速迭代和问题定位

### 代码质量提升
- ✅ 强制代码审查（CODEOWNERS + PR模板）
- ✅ 自动化测试覆盖
- ✅ 安全漏洞扫描

### 团队协作改善
- ✅ 清晰的分支管理策略
- ✅ 标准化的提交信息
- ✅ 自动化的发布说明

### 项目可维护性
- ✅ 完整的变更历史追踪
- ✅ 自动化的依赖项更新
- ✅ 标准化的文档管理

## 5. 最佳实践建议

### 提交信息规范
```
type(scope): subject

body

footer
```

**类型**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `refactor`: 重构
- `test`: 测试相关

### 版本号规范
- **主版本号**: 不兼容的API修改
- **次版本号**: 向后兼容的功能性新增
- **修订版本号**: 向后兼容的问题修正

### 分支命名规范
- `feature/迭代ID-功能描述`
- `bugfix/问题ID-问题描述`
- `hotfix/问题ID-紧急修复`
- `release/版本号`

## 6. 参考资料

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [语义化版本](https://semver.org/lang/zh-CN/)
- [GitFlow分支模型](https://nvie.com/posts/a-successful-git-branching-model/)
- [spec-kit实现参考](../references/spec-kit/)

---

**创建时间**: 2025-12-24
**更新版本**: v1.0.0
