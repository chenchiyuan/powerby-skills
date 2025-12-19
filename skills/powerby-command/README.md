# PowerBy Command

PowerBy Command 是 PowerBy 项目生命周期管理的命令行工具和命令注册系统。它提供了一套完整的命令，用于在 Claude 中自动补全和快速访问 PowerBy 工作流程。

## 🚀 快速开始

### 安装 CLI 工具（Mac/Linux）

```bash
# 1. 进入安装目录
cd /path/to/powerby-skills/skills/powerby-command

# 2. 运行安装脚本
chmod +x setup.sh
./setup.sh
```

### 初始化项目

```bash
# 在您的项目目录中
powerby init my-project
```

### 在 Claude 中使用命令

```
/powerby.init           # 初始化/更新PowerBy命令
/powerby.initialize     # P0: 项目初始化（定义迭代主任务）
/powerby.define         # P1: 需求定义+澄清（融合，输入需求）
/powerby.research       # P3: 技术调研
/powerby.design         # P4: 架构设计
/powerby.plan           # P5: 任务规划
/powerby.implement      # P6: 开发实现
/powerby.review         # P7: 代码审查
/powerby.quick          # 快速流程（≤3天需求）
```

## 📋 功能特性

### 1. 命令自动补全
- 所有 `/powerby.*` 命令在 Claude 中都有自动补全
- 每个命令都有详细的描述和使用说明
- 显示前置条件和预期输出

### 2. 版本更新机制
- `/powerby.init` 命令自动清理旧版本
- 安装最新版本的命令文件
- 保持命令与 PowerBy 技能同步

### 3. 项目生命周期管理
- 完整覆盖 MVP 核心阶段：P0-P1, P3-P7
- P8运维交付为可选流程
- 每个阶段都有明确的质量门禁
- 支持迭代和版本管理
- 快速流程支持≤3天的小需求

### 4. CLI 工具功能

```bash
# 初始化新项目
powerby init [项目名称]

# 更新PowerBy命令到最新版本
powerby update

# 检查项目状态
powerby status

# 清理PowerBy命令和配置
powerby clean
```

## 📁 目录结构

### 安装后的项目结构

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

### 模板目录结构

```
templates/
├── .claude/
│   └── commands/           # 命令文件模板
├── .powerby/               # 项目配置模板
│   ├── project.json
│   └── iterations.json
└── docs/                   # 项目文档模板
    └── constitution.md
```

## 🔄 工作流程

### P0-P8 阶段流程

```
P0: /powerby.initialize  → 项目初始化
   ↓
P1: /powerby.define      → 需求定义+澄清
   ↓
P3: /powerby.research    → 技术调研
   ↓
P4: /powerby.design      → 架构设计
   ↓
P5: /powerby.plan        → 任务规划
   ↓
P6: /powerby.implement   → 开发实现
   ↓
P7-P8: /powerby.review   → 代码审查和交付
```

### 版本更新流程

```
1. 用户运行 /powerby.init
2. 系统检查当前版本
3. 清理旧版本命令文件
4. 安装最新版本命令文件
5. 更新项目配置
6. 验证安装结果
```

## ⚙️ 技术架构

### 组件说明

1. **命令文件** (`.claude/commands/*.md`)
   - Claude 自动读取和显示
   - 包含 YAML frontmatter 和执行指令
   - 支持 handoffs 和 scripts

2. **CLI 工具** (`powerby-cli.py`)
   - Python 实现的命令行工具
   - 提供安装、更新、清理功能
   - 跨平台支持（Mac/Linux）

3. **技能系统** (`SKILL.md`)
   - 实际命令执行逻辑
   - 与其他 PowerBy 技能协作
   - 提供完整的工作流程

### 与技能系统集成

每个命令都会调用对应的 PowerBy 技能：

- **P0-P1**: `powerby-product` (产品管理)
- **P3-P4**: `powerby-architect` (架构设计)
- **P5-P6**: `powerby-engineer` (工程实现)
- **P7**: `powerby-code-review` (代码审查)
- **P8 (可选)**: DevOps (运维交付)

## 📖 详细文档

- [命令注册系统详解](COMMAND_REGISTRATION.md)
- [PowerBy Command Skill](SKILL.md)
- [PowerBy 工作流程](../powerby-lifecycle-overview.md)

## 🛠️ 开发指南

### 添加新命令

1. 在 `templates/.claude/commands/` 创建新命令文件
2. 遵循 YAML frontmatter 格式
3. 更新 `powerby-cli.py` 中的命令列表
4. 测试命令功能

### 更新现有命令

1. 修改 `templates/.claude/commands/` 中的命令文件
2. 运行 `/powerby.init` 更新项目中的命令
3. 测试命令功能

## ❓ 故障排除

### 命令不显示

```bash
# 检查命令目录
ls -la .claude/commands/

# 重新安装命令
/powerby.init
```

### 权限错误

```bash
# 修复权限
chmod 755 .claude/commands/
chmod 644 .claude/commands/powerby-*.md
```

### 命令执行失败

1. 检查前置条件
2. 查看项目配置
3. 重新初始化项目

## 📄 许可证

MIT License - 详见 [LICENSE.txt](LICENSE.txt)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

---

**PowerBy Command** - 让项目管理工作更简单、更高效！
