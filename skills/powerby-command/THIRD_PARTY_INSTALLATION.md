# PowerBy Command - 第三方安装指南

## 概述

本指南帮助第三方用户通过Claude插件市场安装PowerBy流程技能，并正确安装commands到项目中。

## 安装步骤

### 步骤1：通过Claude插件市场安装技能

1. **访问Claude技能市场**
   - 在Claude中点击左侧菜单的"技能市场"
   - 搜索"powerby-skill"或"powerby-command"

2. **安装PowerBy技能**
   - 点击"powerby-skill"技能卡片
   - 点击"添加到项目"按钮
   - 确认安装到当前项目

### 步骤2：安装PowerBy Commands

安装技能后，您需要安装PowerBy命令。有两种方法：

#### 方法A：通过Claude命令安装（推荐）

在Claude对话中直接运行：

```
/powerby.init
```

这将自动：
- 清理旧版本命令
- 安装最新版本的PowerBy命令
- 创建项目配置目录
- 验证安装结果

#### 方法B：通过命令行工具安装

如果您在本地环境中：

```bash
# 1. 进入技能目录
cd /path/to/powerby-skills/skills/powerby-command

# 2. 运行安装脚本
chmod +x setup.sh
./setup.sh

# 3. 在项目中初始化
cd /your/project/directory
powerby init your-project-name
```

### 步骤3：验证安装

安装完成后，您应该能看到：

1. **目录结构**：
   ```
   your-project/
   ├── .claude/
   │   └── commands/
   │       ├── powerby-init.md
   │       ├── powerby-initialize.md
   │       ├── powerby-define.md
   │       ├── powerby-research.md
   │       ├── powerby-design.md
   │       ├── powerby-plan.md
   │       ├── powerby-implement.md
   │       ├── powerby-review.md
   │       └── powerby-quick.md
   └── .powerby/
       ├── project.json
       └── iterations.json
   ```

2. **可用命令**：
   在Claude中输入`/powerby`应该显示所有可用命令的自动补全。

### 步骤4：开始使用

安装完成后，您可以直接在Claude中使用PowerBy命令：

```bash
# 初始化项目
/powerby.initialize 我的项目 "项目描述"

/*
# 定义需求
/powerby.define "我想构建一个任务管理系统"

/*
# 或者使用快速流程
/powerby.quick 为现有系统添加用户收藏功能
```

## 故障排除

### 问题1：命令不显示

**症状**：输入`/powerby`没有自动补全提示

**解决方案**：
1. 确认已安装powerby-skill技能
2. 运行`/powerby.init`重新安装命令
3. 检查`.claude/commands/`目录是否存在

### 问题2：权限错误

**症状**：安装时提示权限不足

**解决方案**：
```bash
# 修复权限
chmod 755 .claude/commands/
chmod 644 .claude/commands/powerby-*.md
```

### 问题3：命令执行失败

**症状**：运行命令时报错

**解决方案**：
1. 检查项目是否已初始化（需要`.powerby`目录）
2. 确认`.claude/commands/`目录中有所有命令文件
3. 重新运行`/powerby.init`

### 问题4：版本过旧

**症状**：命令功能不完整或有错误

**解决方案**：
```bash
# 更新到最新版本
/powerby.init
```

## 完整命令列表

安装成功后，您将获得以下PowerBy命令：

| 命令 | 描述 | 阶段 |
|------|------|------|
| `/powerby.initialize` | 项目初始化，定义迭代系统主任务 | P0 |
| `/powerby.define` | 需求定义+澄清，融合P1+P2 | P1 |
| `/powerby.quick` | 快速流程，处理≤3天需求 | P0-P5 |
| `/powerby.research` | 技术调研，评估技术方案 | P3 |
| `/powerby.design` | 架构设计，四阶段强制流程 | P4 |
| `/powerby.plan` | 任务规划，分解可执行任务 | P5 |
| `/powerby.implement` | 开发实现，TDD开发方式 | P6 |
| `/powerby.review` | 代码审查，质量把控 | P7-P8 |

## MVP精简流程

PowerBy采用MVP精简流程，专注于核心价值交付：

```
P0 → P1 → P3 → P4 → P5 → P6 → P7
```

- **P0**：项目初始化
- **P1**：需求定义+澄清（融合原P1+P2）
- **P3**：技术调研
- **P4**：架构设计
- **P5**：任务规划
- **P6**：开发实现
- **P7**：代码审查和交付

**注意**：P2（独立澄清阶段）已合并到P1中，实现需求定稿制。

## 快速流程

对于≤3天的小需求，使用快速流程：

```
/powerby.quick [需求描述]
```

快速流程特点：
- 总时间≤5小时
- 在关键节点增加人工确认
- 基于现有架构的增量开发
- 文档精简但完整

## 最佳实践

### ✅ 推荐做法

1. **严格遵循流程**：不跳过任何阶段或门禁
2. **充分确认**：每个阶段都等待门禁检查通过
3. **记录决策**：所有重要决策都有文档记录
4. **及时更新**：状态变化立即更新到项目元数据
5. **主动澄清**：遇到模糊点主动询问

### ❌ 避免做法

1. **流程跳跃**：不要跳过前置阶段直接进入后续阶段
2. **门禁绕过**：不要绕过质量门禁检查
3. **文档滞后**：避免代码实现与文档不同步
4. **重复造轮子**：优先使用现有库和服务

## 获取帮助

如果您遇到问题：

1. **查看技能文档**：
   - [PowerBy Command README](./README.md)
   - [PowerBy Command SKILL.md](./SKILL.md)

2. **查看工作流指南**：
   - [PowerBy工作流完整指南](../../docs/powerby-workflow-complete-guide.md)
   - [质量门禁指南](../../docs/powerby-quality-gates.md)

3. **提交Issue**：
   - 在GitHub上提交问题报告
   - 描述具体场景和期望行为

## 版本信息

- **当前版本**：v3.3.0
- **更新时间**：2025-12-19
- **兼容性**：Claude Desktop最新版本
- **支持平台**：Mac、Linux

## 更新日志

### v3.3.0 (2025-12-19)
- MVP精简优化：移除非功能性属性扫描
- P1+P2融合：需求定稿制
- 命令参数简化：initialize和define
- 添加快速流程支持

### v3.2.0
- 完整的10个命令支持
- 标准化安装流程
- 质量门禁系统

### v3.1.0
- 初始版本
- 基础命令注册系统

---

**PowerBy Command** - 让项目管理工作更简单、更高效！