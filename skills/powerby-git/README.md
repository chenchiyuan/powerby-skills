# PowerBy Git Branch Manager Skill

Git分支管理专项技能，负责分支生命周期管理、提交合规检查、文件清理验证。确保每次迭代/bug-fix都在规范分支上进行，流程结束时自动清理临时文件并检查文档归档。

## 快速开始

### 激活命令
```
/powerby-git
```

### 使用示例
```
用户: /powerby-git

Git Manager:
角色已激活：Branch Manager - The Guardian
我已准备就绪，请指定要开始的迭代或bug修复。

用户: 开始一个新的用户认证功能迭代

Git Manager:
✅ 创建分支: feature/user-authentication
✅ 切换到新分支
✅ 安装 pre-commit 钩子
✅ 安装 pre-merge 钩子
分支已就绪，开始开发吧！

用户: 检查当前状态

Git Manager:
当前分支: feature/user-authentication
待提交变更: 3个文件
识别的临时文件: debug.log
建议: 在提交前删除 debug.log

用户: 迭代完成，清理已合并分支

Git Manager:
待清理分支（已合并到主分支）:
  - feature/login-page
  - feature/user-profile
  - bugfix/header-alignment

预览模式（无实际删除）
使用 --force 参数执行清理
```

## 核心特性

- 🔀 **分支生命周期管理**: 创建 → 开发 → 检查 → 合并 → 清理
- ✅ **提交合规检查**: 自动验证文件合规性和提交信息格式
- 🧹 **临时文件清理**: 确保只保留合法文件三类
- 📋 **文档归档检查**: 验证 PowerBy 流程文档完整性
- 🔒 **钢铁纪律约束**: 强制分支命名规范和文件白名单
- ⚙️ **Git Hooks 集成**: pre-commit 和 pre-merge 自动检查
- 👤 **手动清理控制**: 用户对分支清理有完全控制权

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    分支生命周期流程                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 开始 → powerby-git start --type=feature --name=xxx          │
│           ↓                                                     │
│  2. 创建分支 → git checkout -b feature/xxx                      │
│           ↓                                                     │
│  3. 开发 → 编写代码和测试                                        │
│           ↓                                                     │
│  4. 提交 → 触发 pre-commit 检查                                  │
│           ↓                                                     │
│  5. 检查 → powerby-git check --type=commit                      │
│           ↓                                                     │
│  6. 合并 → 触发 pre-merge 检查                                   │
│           ↓                                                     │
│  7. 清理 → powerby-git cleanup --dry-run / --force              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 核心命令

| 命令 | 说明 |
|------|------|
| `powerby-git start --type=feature --name=xxx` | 创建新分支 |
| `powerby-git status` | 查看当前状态 |
| `powerby-git check --type=commit\|merge` | 执行合规检查 |
| `powerby-git list --merged\|--unmerged` | 列出分支 |
| `powerby-git cleanup --dry-run\|--force` | 清理已合并分支 |

## 核心原则

### 1. 强制分支约束（钢铁纪律）

- 所有开发**必须**在独立分支上进行
- **禁止**直接在主分支开发
- 分支名称**必须**符合规范：`feature/{名}` 或 `bugfix/{名}`

### 2. 文件白名单机制（钢铁纪律）

**只有三类文件合法**：
1. 业务代码和持续引用的测试用例
2. PowerBy 流程规定的文档
3. 用户明确指明的文件

### 3. 手动清理原则

- 分支清理**默认手动**执行
- 提供 `--dry-run` 预览模式
- 用户对清理操作有完全控制权

## 分支命名规范

| 类型 | 模式 | 示例 |
|------|------|------|
| Feature | `feature/{迭代名}` | `feature/user-authentication` |
| Bugfix | `bugfix/{问题}` | `bugfix/login-timeout` |
| Hotfix | `hotfix/{版本}-{问题}` | `hotfix/v1.2.3-security` |
| Release | `release/{版本}` | `release/v2.0.0` |

**命名规则**：
- 使用小写字母
- 单词间使用连字符
- 避免中文和特殊字符

## 提交信息规范

```
{类型}({范围}): {描述}

# 示例
feat(auth): add JWT token generation
fix(database): resolve connection leak
docs(readme): update installation guide
```

**类型标识**：
| 类型 | 描述 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式 |
| refactor | 重构 |
| test | 测试 |
| chore | 维护 |

## 文件白名单

### 合法文件

```
src/                           # 源代码
tests/                         # 测试用例
docs/
├── iterations/{id}/           # 迭代文档
│   ├── prd.md
│   ├── task.md
│   └── architecture.md
├── bugs/{id}/                 # Bug文档
└── proposals/                 # 方案提案
package.json / pyproject.toml  # 依赖配置
README.md / LICENSE            # 项目说明
```

### 临时文件（会被标记删除）

```
*.tmp / *.temp                # 临时文件
*.log                         # 日志文件
*.debug / *.bak               # 调试/备份文件
.DS_Store                     # macOS文件
__pycache__/                  # Python缓存
.env                          # 环境变量
```

## Git Hooks 集成

### pre-commit 钩子

每次提交时自动检查：
- 提交信息格式
- 变更文件是否在白名单
- 临时文件识别

### pre-merge 钩子

合并前自动检查：
- 全量文件合规性
- PowerBy 文档完整性
- 临时文件清理

## 与其他技能的协作

- **powerby-command**: 接收分支管理指令
- **powerby-implement**: 负责具体开发，自动触发合规检查
- **powerby-review**: 代码审查后触发合并检查
- **powerby-product**: 迭代规划时创建对应分支

## 质量标准

### 完成定义

- [ ] 分支命名符合规范
- [ ] 提交信息格式正确
- [ ] 所有文件都在白名单内
- [ ] 无临时文件残留
- [ ] PowerBy 文档完整
- [ ] 分支已合并（或已清理）

## 版本信息

- **版本**: v1.0.0
- **发布日期**: 2026-01-12
- **适用范围**: Git 分支管理与合规检查

## 变更日志

### v1.0.0 - 2026-01-12

**初始版本**

- 分支生命周期管理
- 提交合规检查
- 文件白名单验证
- Git Hooks 集成
- 手动清理机制

## 许可证

MIT License - 详见 [LICENSE.txt](../../LICENSE.txt)
