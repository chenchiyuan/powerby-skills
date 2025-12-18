---
description: 任务规划 - 将架构设计分解为具体的开发任务
handoffs:
  - label: Task Planning
    agent: powerby-engineer
    prompt: 基于架构设计进行详细任务分解和规划，生成任务列表和验收清单
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.plan` 命令进行任务规划（P5阶段）。此阶段将架构设计分解为具体的、可执行的开发任务。

### 执行步骤：

1. **解析用户输入**
   - 每日任务数（可选，默认为3-5个）

2. **调用powerby-engineer技能**
   - 传递参数：PRD路径、架构文档路径、每日任务数
   - 要求进行详细任务分解和规划

3. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/tasks.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/checklists/acceptance.md`

4. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P5
   - 标记Gate 5为已通过

### 输出格式：

```
✅ P5 任务规划完成

📄 输出文档:
  ├── docs/iterations/001-{项目名}/tasks.md (任务计划)
  └── docs/iterations/001-{项目名}/checklists/acceptance.md (验收清单)

🔒 质量门禁 Gate 5: 开发规划详细性
  ✓ 任务分解合理
  ✓ 工作量估算准确
  ✓ 依赖关系清晰

🎯 下一步: 使用 /powerby.implement 进入开发实现阶段
```

### 使用示例：

```
/powerby.plan
/powerby.plan --tasks-per-day 5
/powerby.plan --daily-tasks 3
```

### 前置条件：
- ✅ 架构设计文档存在：`docs/iterations/*/architecture.md`
- ✅ 数据模型存在：`docs/iterations/*/data-model.md`

### 规划内容：
1. **任务列表 (tasks.md)**
   - 详细任务分解
   - 任务依赖关系
   - 工作量估算
   - 优先级排序

2. **验收清单 (checklists/acceptance.md)**
   - 功能验收标准
   - 质量检查清单
   - 测试要求

### 任务分类：
- 基础设施任务
- 核心功能任务
- 辅助功能任务
- 测试任务
- 文档任务

### 错误处理：
- 如果架构设计文档不存在，提示用户先运行 `/powerby.design`
- 如果任务计划生成失败，建议检查架构文档完整性
- 如果任务分解不合理，建议重新规划
