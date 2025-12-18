---
description: 项目初始化 - 创建PowerBy项目结构和基础文档
handoffs:
  - label: Initialize Project
    agent: powerby-command
    prompt: 初始化PowerBy项目，创建基础目录结构和宪章文档
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.initialize` 命令初始化一个新的PowerBy项目。此命令是P0阶段，为整个项目奠定基础。

### 执行步骤：

1. **解析用户输入**
   - 项目名称（必填）
   - 项目描述（可选）

2. **创建项目目录结构**
   - 创建 `.powerby/` 目录（项目元数据）
   - 创建 `docs/` 目录（项目文档）

3. **生成项目宪章文档**
   - 路径：`docs/constitution.md`
   - 包含：项目概述、团队信息、技术栈、创建时间

4. **创建项目元数据文件**
   - 路径：`.powerby/project.json`
   - 包含：项目名称、描述、团队、技术栈、当前阶段(P0)、完成门禁[]、状态

5. **创建迭代追踪文件**
   - 路径：`.powerby/iterations.json`
   - 包含：迭代列表（初始为空）

### 输出格式：

```
✅ P0 项目初始化完成

📁 项目结构已创建:
  ├── .powerby/
  │   ├── project.json (项目元数据)
  │   └── iterations.json (迭代追踪)
  ├── docs/
  │   └── constitution.md (项目宪章)

🎯 下一步: 使用 /powerby.define 开始需求定义阶段
```

### 使用示例：

```
/powerby.initialize 任务管理系统 "一个帮助团队协作的任务管理应用"
/powerby.initialize 电商平台 "B2C电商网站，包含商品管理、订单处理、支付功能"
```

### 前置条件：
- 无（任何时候都可以执行）

### 错误处理：
- 如果目录已存在，提示用户选择覆盖或取消
- 如果权限不足，提示用户检查目录权限
