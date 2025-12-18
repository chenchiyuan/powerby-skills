---
description: 开发实现 - 根据任务计划执行开发工作
handoffs:
  - label: Implementation
    agent: powerby-engineer
    prompt: 基于任务计划执行开发实现，生成实现报告和代码交付物
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.implement` 命令进行开发实现（P6阶段）。此阶段根据任务计划执行具体的开发工作。

### 执行步骤：

1. **解析用户输入**
   - TDD模式（可选，默认为关闭）
   - 测试覆盖率目标（可选，默认为80%）

2. **调用powerby-engineer技能**
   - 传递参数：任务计划路径、架构文档路径、TDD模式
   - 要求执行开发实现

3. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/implementation-report.md`

4. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P6
   - 标记Gate 6为已通过

### 输出格式：

```
✅ P6 开发实现完成

📄 输出文档:
  └── docs/iterations/001-{项目名}/implementation-report.md (实现报告)

🔒 质量门禁 Gate 6: 开发实现质量
  ✓ 功能完整实现
  ✓ 代码质量达标
  ✓ 测试覆盖充分

🎯 下一步: 使用 /powerby.review 进入代码审查阶段
```

### 使用示例：

```
/powerby.implement
/powerby.implement --tdd
/powerby.implement --test-coverage 90
```

### 前置条件：
- ✅ 任务计划存在：`docs/iterations/*/tasks.md`

### 实现内容：
实现报告应包含：
1. 实现进度
   - 已完成任务
   - 进行中任务
   - 待完成任务

2. 代码质量检查
   - 代码规范检查
   - 静态代码分析
   - 安全扫描

3. 测试覆盖率
   - 单元测试覆盖率
   - 集成测试覆盖率
   - E2E测试覆盖率

4. 交付物清单
   - 源代码
   - 配置文件
   - 部署脚本
   - 文档

### TDD模式：
- 先写测试
- 后写实现
- 重构优化

### 错误处理：
- 如果任务计划不存在，提示用户先运行 `/powerby.plan`
- 如果实现报告生成失败，建议检查任务完成情况
- 如果测试覆盖率不达标，建议补充测试用例
