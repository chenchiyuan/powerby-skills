---
description: 项目初始化 - 创建PowerBy项目结构，定义迭代系统主任务
handoffs:
  - label: Initialize Project
    agent: powerby-command
    prompt: 初始化PowerBy项目，创建基础目录结构，定义迭代系统主任务
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.initialize` 命令初始化一个新的PowerBy项目。此命令是P0阶段，为整个项目奠定基础，定义迭代系统主任务。

### 执行步骤：

1. **解析用户输入**
   - 项目名称（必填）
   - 主任务描述（必填，核心迭代任务）

2. **创建项目目录结构**
   - 创建 `.powerby/` 目录（项目元数据）
   - 创建 `docs/` 目录（项目文档）

3. **生成项目宪章文档**
   - 路径：`docs/constitution.md`
   - 包含：项目概述、主任务、创建时间

4. **创建项目元数据文件**
   - 路径：`.powerby/project.json`
   - 包含：项目名称、主任务、当前阶段(P0)、完成门禁[]、状态

5. **创建迭代追踪文件**
   - 路径：`.powerby/iterations.json`
   - 包含：迭代列表（初始为空）

6. **定义迭代系统主任务**
   - 在project.json中记录主任务
   - 为后续迭代提供核心方向

### 输出格式：

```
✅ P0 项目初始化完成

📁 项目结构已创建:
  ├── .powerby/
  │   ├── project.json (项目元数据)
  │   └── iterations.json (迭代追踪)
  ├── docs/
  │   └── constitution.md (项目宪章)

📋 迭代系统主任务已定义

🎯 下一步: 使用 /powerby.define 开始需求定义阶段
```

### 使用示例：

```
/powerby.initialize 任务管理系统 "实现团队任务协作系统，支持任务创建、分配和跟踪"
/powerby.initialize 电商平台 "构建B2C电商平台核心功能，包括商品展示、购物车和订单管理"
```

### 前置条件：
- 无（任何时候都可以执行）

### 错误处理：
- 如果目录已存在，提示用户选择覆盖或取消
- 如果权限不足，提示用户检查目录权限
