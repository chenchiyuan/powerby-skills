# PowerBy 命令注册系统

## 概述

PowerBy 命令注册系统允许用户在 Claude 中使用 `/powerby.*` 命令进行自动补全和快速访问。这些命令与 PowerBy 技能系统完全集成，提供完整的项目生命周期管理。

## 架构

### 核心组件

1. **命令文件** (`.claude/commands/*.md`)
   - 存储在项目目录的 `.claude/commands/` 中
   - 每个命令对应一个 Markdown 文件
   - 包含 YAML frontmatter 和执行指令

2. **CLI 工具** (`powerby-cli.py`)
   - 提供命令行接口
   - 负责安装、更新、清理命令
   - 管理项目配置

3. **技能系统** (`SKILL.md`)
   - 实际的命令执行逻辑
   - 与其他 PowerBy 技能协作
   - 提供完整的工作流程

### 命令文件结构

```yaml
---
description: 命令描述
handoffs:
  - label: 操作名称
    agent: 技能名称
    prompt: 提示词
scripts:
  sh: 脚本路径
---

## User Input
$ARGUMENTS

## Outline
详细执行流程...
```

## 安装方式

### 方式一：使用 PowerBy CLI (推荐)

```bash
# 1. 安装 CLI 工具
chmod +x setup.sh
./setup.sh

# 2. 初始化项目
powerby init my-project

# 3. 在 Claude 中使用命令
/powerby.init
/powerby.initialize
/powerby.define
```

### 方式二：手动复制命令文件

```bash
# 复制命令文件到项目
cp templates/.claude/commands/*.md .claude/commands/

# 在 Claude 中使用命令
/powerby.initialize
/powerby.define
```

## 可用命令

### 核心命令 (P0-P8)

| 命令 | 阶段 | 描述 |
|------|------|------|
| `/powerby.initialize` | P0 | 项目初始化 |
| `/powerby.define` | P1 | 需求定义 |
| `/powerby.clarify` | P2 | 需求澄清 |
| `/powerby.research` | P3 | 技术调研 |
| `/powerby.design` | P4 | 架构设计 |
| `/powerby.plan` | P5 | 任务规划 |
| `/powerby.implement` | P6 | 开发实现 |
| `/powerby.review` | P7-P8 | 代码审查和交付 |

### 管理命令

| 命令 | 描述 |
|------|------|
| `/powerby.init` | 初始化/更新 PowerBy 命令 |

## 版本更新机制

### 自动更新

使用 `/powerby.init` 命令时会自动：

1. **清理旧版本**
   - 删除所有 `powerby-*.md` 命令文件
   - 清理过期的配置文件

2. **安装新版本**
   - 下载最新命令文件
   - 更新项目配置

3. **验证安装**
   - 检查命令文件完整性
   - 测试命令可用性

### 版本检查

```bash
# 检查项目状态
powerby status

# 查看已安装的命令
ls .claude/commands/powerby-*.md
```

## 目录结构

### 项目初始化后的结构

```
project/
├── .claude/
│   └── commands/
│       ├── powerby-init.md
│       ├── powerby-initialize.md
│       ├── powerby-define.md
│       ├── powerby-clarify.md
│       ├── powerby-research.md
│       ├── powerby-design.md
│       ├── powerby-plan.md
│       ├── powerby-implement.md
│       └── powerby-review.md
├── .powerby/
│   ├── project.json
│   └── iterations.json
└── docs/
    └── constitution.md
```

## 与技能系统的集成

### 命令执行流程

```
用户输入 /powerby.command
    ↓
Claude 读取 .claude/commands/powerby-command.md
    ↓
执行命令定义中的指令
    ↓
调用对应的 PowerBy 技能
    ↓
技能执行实际工作
    ↓
返回结果给用户
```

### 技能协作

每个命令都可能涉及多个技能：

- **P0-P1**: `powerby-product` (产品管理)
- **P3-P4**: `powerby-architect` (架构设计)
- **P5-P6**: `powerby-engineer` (工程实现)
- **P7**: `powerby-code-review` (代码审查)
- **P8 (可选)**: DevOps (运维交付)

## 最佳实践

### 1. 保持命令同步

定期运行 `/powerby.init` 确保命令与技能版本同步：

```bash
# 更新命令到最新版本
powerby update
```

### 2. 检查项目状态

使用 `powerby status` 检查项目健康度：

```bash
# 查看项目状态
powerby status
```

### 3. 清理不需要的命令

如果不需要 PowerBy 命令，可以清理：

```bash
# 清理所有 PowerBy 命令
powerby clean
```

## 故障排除

### 命令不显示

1. 检查 `.claude/commands/` 目录是否存在
2. 确认命令文件是否正确复制
3. 重新运行 `/powerby.init`

### 权限错误

```bash
# 检查目录权限
ls -la .claude/commands/

# 修复权限
chmod 755 .claude/commands/
chmod 644 .claude/commands/powerby-*.md
```

### 命令执行失败

1. 检查前置条件是否满足
2. 查看项目配置文件 `.powerby/project.json`
3. 重新初始化项目

## 开发指南

### 添加新命令

1. 在 `templates/.claude/commands/` 创建新命令文件
2. 遵循现有的 YAML frontmatter 格式
3. 更新 `powerby-cli.py` 中的命令列表
4. 更新本文档

### 更新现有命令

1. 修改 `templates/.claude/commands/` 中的命令文件
2. 运行 `/powerby.init` 更新项目中的命令
3. 测试命令功能

## 参考资源

- [PowerBy Command Skill](SKILL.md)
- [PowerBy Flow Guardian](../powerby-flow-guardian/SKILL.md)
- [项目结构](../PROJECT_STRUCTURE.md)
- [技能标准合规](SKILL_STANDARD_COMPLIANCE.md)

## 许可证

MIT License - 详见 [LICENSE.txt](LICENSE.txt)
