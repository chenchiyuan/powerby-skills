# PowerBy Skills - 安装指南

## 📋 目录

- [系统要求](#系统要求)
- [安装方法](#安装方法)
- [验证安装](#验证安装)
- [快速开始](#快速开始)
- [卸载技能](#卸载技能)
- [故障排除](#故障排除)

## 系统要求

- **Claude Code**: 最新版本
- **操作系统**: Windows, macOS, Linux
- **网络**: 需要访问GitHub（用于从Git URL安装）

## 安装方法

### 方法1：从GitHub安装（推荐）

这是最简单的安装方法，直接从GitHub安装最新版本。

#### 步骤1：打开Claude Code

在您的终端或命令行中启动Claude Code：

```bash
claude  # 或者使用您的Claude Code启动命令
```

#### 步骤2：安装核心技能包

```bash
/plugin install powerby-core@git+https://github.com/your-org/powerby-skills
```

#### 步骤3：安装原子技能包（可选，但推荐）

```bash
/plugin install powerby-atomic@git+https://github.com/your-org/powerby-skills
```

### 方法2：本地安装

如果您已经克隆了仓库或下载了源代码：

```bash
# 获取项目路径
POWERBY_SKILLS_PATH="/path/to/powerby-skills"

# 在Claude Code中添加技能市场
/plugin marketplace add file://${POWERBY_SKILLS_PATH}

# 安装技能
/plugin install powerby-core@powerby-skills
/plugin install powerby-atomic@powerby-skills
```

## 验证安装

### 检查已安装的技能

```bash
/plugin list | grep powerby
```

## 快速开始

### 示例1：使用产品经理技能

```bash
请使用powerby-product技能帮助我定义一个AI驱动的任务管理应用的需求。
```

## 故障排除

### 问题1：安装失败 - "无法访问GitHub"

**解决方案：**
1. 检查网络连接
2. 确认GitHub URL正确
3. 尝试使用SSH URL

### 问题2：技能未找到

**解决方案：**
1. 确认技能已正确安装
2. 重新安装技能
3. 重启Claude Code会话

---

**祝您使用愉快！** 🎉
