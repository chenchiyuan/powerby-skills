---
description: 项目初始化 - 创建PowerBy项目结构，定义迭代系统主任务 ⚠️已弃用
handoffs:
  - label: Initialize Project
    agent: powerby-command
    prompt: 初始化PowerBy项目，创建基础目录结构，定义迭代系统主任务，并生成项目宪章docs/constitution.md。

重要：必须从模板文件 templates/docs/constitution.md 读取内容，并替换 {{TIMESTAMP}} 和 {{PROJECT_NAME}} 变量。生成的宪章必须完全按照模板内容，包含：1) 核心理念（零假设原则、Mixin思维、小步提交等）；2) 工作流程（顾问式流程）；3) 技术标准（SOLID、DRY、奥卡姆剃刀原则等）；4) 决策框架；5) 质量门禁。

这是约束整个项目的最高法则，包含所有核心理念、工作流程、技术标准等，而不是产品功能文档。绝对不能根据用户输入的项目描述生成产品文档内容。

⚠️ 注意：此命令已弃用，请直接使用 /powerby.define 或 /powerby.quick，它们会自动处理项目初始化。
---

## User Input

```text
$ARGUMENTS
```

## Outline

⚠️ **此命令已弃用** ⚠️

使用 `/powerby.initialize` 命令初始化一个新的PowerBy项目。此命令是P0阶段，为整个项目奠定基础，定义迭代系统主任务。

**推荐用法**：请直接使用 `/powerby.define` 或 `/powerby.quick`，它们会自动处理项目初始化，无需手动运行此命令。

**弃用原因**：P0初始化只是简单的文件创建操作，已合并到P1阶段中自动执行，减少用户操作步骤。

### 执行步骤：

1. **解析用户输入**
   - 项目名称（必填）
   - 主任务描述（必填，核心迭代任务）

2. **创建项目目录结构**
   - 创建 `.powerby/` 目录（项目元数据）
   - 创建 `docs/` 目录（项目文档）

3. **生成项目宪章文档**
   - 路径：`docs/constitution.md`
   - 必须从模板文件 templates/docs/constitution.md 读取内容
   - 替换 {{TIMESTAMP}} 和 {{PROJECT_NAME}} 变量
   - 生成的宪章包含：核心理念、工作流程、技术标准、决策框架、质量门禁等最高法则
   - 这是约束整个项目的最高法则，绝对不能生成产品功能文档

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

---

## 弃用声明

⚠️ **此命令已弃用，不推荐使用** ⚠️

**替代方案**：
- 使用 `/powerby.define` 进行标准流程（自动初始化 + 需求定义）
- 使用 `/powerby.quick` 进行快速流程（自动初始化 + P0-P5快速处理）

**迁移指南**：
1. 如果你之前使用 `/powerby.initialize`，现在可以直接使用 `/powerby.define`
2. 自动初始化会在后台静默执行，无需额外操作
3. 用户体验更流畅，操作步骤更少

**保留说明**：此命令暂时保留以确保向后兼容，未来版本可能会完全移除。
