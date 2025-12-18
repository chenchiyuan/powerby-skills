---
description: 架构设计 - 设计系统架构、数据模型和API契约
handoffs:
  - label: System Design
    agent: powerby-architect
    prompt: 基于需求和调研结果进行系统架构设计，生成架构文档、数据模型和API契约
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.design` 命令进行架构设计（P4阶段）。此阶段设计系统的整体架构、数据模型和API接口。

### 执行步骤：

1. **调用powerby-architect技能**
   - 传递参数：PRD路径、功能点路径、澄清记录路径、调研报告路径
   - 要求进行系统架构设计

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/architecture.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/data-model.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/contracts/api.yaml`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P4
   - 标记Gate 4为已通过

### 输出格式：

```
✅ P4 架构设计完成

📄 输出文档:
  ├── docs/iterations/001-{项目名}/architecture.md (架构设计)
  ├── docs/iterations/001-{项目名}/data-model.md (数据模型)
  └── docs/iterations/001-{项目名}/contracts/api.yaml (API契约)

🔒 质量门禁 Gate 4: 架构设计清晰性
  ✓ 系统架构明确
  ✓ 模块职责清晰
  ✓ 数据模型合理

🎯 下一步: 使用 /powerby.plan 进入任务规划阶段
```

### 使用示例：

```
/powerby.design
```

### 前置条件：
- ✅ 技术调研报告存在：`docs/iterations/*/research.md`

### 设计内容：
1. **系统架构图**
   - 整体架构设计
   - 模块划分
   - 依赖关系

2. **数据模型**
   - 实体关系图
   - 数据库设计
   - 数据流转

3. **API契约**
   - RESTful API设计
   - 接口规范
   - 数据格式

### 质量检查：
- 架构是否满足非功能性需求
- 模块耦合度是否合理
- 数据模型是否支持所有功能
- API设计是否符合REST规范

### 错误处理：
- 如果技术调研报告不存在，提示用户先运行 `/powerby.research`
- 如果架构文档生成失败，建议检查调研报告质量
- 如果数据模型不合理，建议重新设计架构
