---
description: 初始化PowerBy命令注册 - 安装或更新PowerBy项目命令到最新版本
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.init` 命令注册或更新PowerBy项目命令。此命令会先清理旧的PowerBy命令，然后安装最新版本的命令文件。

### 执行步骤：

1. **检查Claude环境**
   - 验证是否在Claude项目中
   - 检查`.claude`目录是否存在

2. **清理旧版本命令**
   - 删除所有 `powerby-*.md` 命令文件
   - 删除 `.powerby` 目录（如果存在）
   - 清理项目配置

3. **安装最新命令**
   - 复制8个PowerBy命令文件到 `.claude/commands/` 目录
   - 创建 `.powerby` 目录结构
   - 生成项目配置

4. **验证安装**
   - 检查命令文件是否正确安装
   - 验证目录结构是否完整
   - 显示安装成功的命令列表

### 版本更新机制：

此命令确保PowerBy命令始终保持最新状态：

```
清理旧版本 → 下载最新版本 → 验证安装 → 完成
```

### 输出格式：

```
✅ PowerBy 命令注册完成

📋 已安装命令:
  /powerby.initialize - 项目初始化
  /powerby.define - 需求定义
  /powerby.clarify - 需求澄清
  /powerby.research - 技术调研
  /powerby.design - 架构设计
  /powerby.plan - 任务规划
  /powerby.implement - 开发实现
  /powerby.review - 代码审查

📁 目录结构:
  ├── .claude/commands/ - PowerBy命令文件
  └── .powerby/ - PowerBy项目配置

🔄 版本更新机制:
  - 自动清理旧版本命令
  - 安装最新版本命令
  - 保持命令与技能同步

🎯 下一步: 使用 /powerby.initialize 开始项目
```

### 使用示例：

```
/powerby.init
```

### 功能特性：

1. **版本管理**
   - 自动检测当前版本
   - 下载最新版本命令
   - 备份旧版本配置（可选）

2. **清理机制**
   - 删除所有powerby-*命令文件
   - 清理过期的配置文件
   - 重置项目状态

3. **安装验证**
   - 验证命令文件完整性
   - 检查目录结构
   - 测试命令可用性

4. **回滚支持**
   - 如果安装失败，自动回滚到之前版本
   - 保存错误日志
   - 提供手动修复指导

### 错误处理：

- **权限错误**: 检查目录写入权限
- **网络错误**: 检查网络连接，重试下载
- **版本冲突**: 提示用户选择保留或覆盖
- **安装失败**: 自动回滚并提供错误报告

### 安全说明：

此命令需要写入权限来：
- 创建 `.claude/commands/` 目录
- 安装命令文件
- 创建 `.powerby/` 配置目录

确保在可信环境中运行此命令。
