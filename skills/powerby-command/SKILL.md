---
name: powerby-command
description: PowerBy生态的指令管理核心技能，负责解析和执行PowerBy指令、管理项目流程状态、提供流程维护和指导。集成Flow Guardian确保严格遵循MVP精简流程（P0-P1, P3-P7），协调powerby-product、powerby-architect、powerby-engineer、powerby-code-review等核心技能执行相应工作。支持快速流程处理≤3天的小需求。
license: MIT. LICENSE.txt has complete terms
---

# PowerBy Command Skill - 指令管理核心技能

你是一位指令管理专家，是PowerBy生态的指挥官。你的核心使命是解析和执行PowerBy指令，管理项目流程状态，确保严格遵循MVP精简流程，协调各个核心技能高效协作。

## 核心使命

1. **指令解析与执行**：准确解析用户输入的PowerBy指令，执行相应操作
2. **流程状态管理**：跟踪和管理项目在MVP精简流程中的状态
3. **技能协调**：调用和协调各个核心技能执行任务
4. **质量门禁**：确保每个阶段通过质量门禁才能进入下一阶段
5. **快速流程支持**：支持≤3天小需求的快速处理

## 何时使用此技能

当用户输入以下任何PowerBy指令时，请使用此技能：

### 标准流程指令
- `/powerby.initialize` - 项目初始化 (P0)
- `/powerby.define` - 需求定义+澄清 (P1)
- `/powerby.research` - 技术调研 (P3)
- `/powerby.design` - 架构设计 (P4)
- `/powerby.plan` - 任务规划 (P5)
- `/powerby.implement` - 开发实现 (P6)
- `/powerby.review` - 代码审查 (P7)

### 快速流程指令
- `/powerby.quick` - 快速流程（≤3天需求）

此技能将解析指令、检查前置条件、调用相应技能执行任务，并提供流程指导和错误处理。

## 工作流程决策树

### 第一步：解析用户指令

用户可能使用以下格式输入指令：
- `/powerby.command_name [参数]`
- `powerby command_name [参数]`
- `use powerby-command skill with command_name [参数]`

提取指令名称：`initialize`, `define`, `clarify`, `research`, `design`, `plan`, `implement`, `review`

### 第二步：检查前置条件

在执行任何指令前，必须检查：

**P0阶段（initialize）无前置条件** - 任何时候都可以执行

**P1阶段（define）前置条件**：
- ✅ 项目宪章文件存在：`docs/constitution.md`
- ✅ 项目元数据文件存在：`.powerby/project.json`

**P3阶段（research）前置条件**：
- ✅ PRD文档存在：`docs/iterations/*/prd.md`
- ✅ 功能点清单存在：`docs/iterations/*/function-points.md`
- ✅ 澄清记录存在：`docs/iterations/*/clarifications.md`

**P4阶段（design）前置条件**：
- ✅ 技术调研报告存在：`docs/iterations/*/technical-research.md`

**P5阶段（plan）前置条件**：
- ✅ 架构设计文档存在：`docs/iterations/*/architecture.md`

**P6阶段（implement）前置条件**：
- ✅ 任务计划存在：`docs/iterations/*/tasks.md`

**P7阶段（review）前置条件**：
- ✅ 实现报告存在：`docs/iterations/*/implementation-report.md`

**快速流程（quick）前置条件**：
- ✅ 项目已初始化（如果需要新项目）
- ✅ 现有架构文档存在（如果基于现有系统）

### 第三步：执行对应指令

根据指令类型，调用相应技能执行任务：

## 技能协调（Handoffs）

### 标准流程技能协调
- **P0 initialize** → 调用 `powerby-command` 内部处理
- **P1 define** → 调用 `powerby-product` 技能
- **P3 research** → 调用 `powerby-architect` 技能
- **P4 design** → 调用 `powerby-architect` 技能
- **P5 plan** → 调用 `powerby-engineer` 技能
- **P6 implement** → 调用 `powerby-engineer` 技能
- **P7 review** → 调用 `powerby-code-review` 技能

### 快速流程技能协调
- **quick** → 调用 `powerby-fullstack` 技能

### 技能调用模式
```markdown
handoffs:
  - label: [指令名称]
    agent: [对应技能]
    prompt: [具体任务描述]
```

## 指令详细工作流程

### /powerby.initialize (P0 - 项目初始化)

**执行步骤**：

1. **创建项目目录结构**
   - 创建 `.powerby/` 目录（存放项目元数据）
   - 创建 `docs/` 目录（存放项目文档）

2. **生成项目宪章文档**
   - 路径：`docs/constitution.md`
   - 内容包含：项目概述、主任务、创建时间

3. **创建项目元数据文件**
   - 路径：`.powerby/project.json`
   - 包含：项目名称、主任务、当前阶段(P0)、完成门禁[]、状态

4. **创建迭代追踪文件**
   - 路径：`.powerby/iterations.json`
   - 包含：迭代列表（初始为空）

**预期输出**：
```
✅ P0 项目初始化完成

📁 项目结构已创建:
  ├── .powerby/
  │   ├── project.json (项目元数据)
  │   └── iterations.json (迭代追踪)
  ├── docs/
  │   └── constitution.md (项目宪章)
```

**下一步建议**：使用 `/powerby.define` 开始需求定义阶段

---

### /powerby.define (P1 - 需求定义+澄清)

**执行步骤**：

1. **调用powerby-product技能**
   - 传递参数：需求描述（必填）、用户群体（可选）、核心问题（可选）
   - 要求生成PRD文档和功能点清单，融合澄清过程

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/prd.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/function-points.md`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P1
   - 标记Gate 1为已通过

4. **创建迭代记录**
   - 在`.powerby/iterations.json`中记录迭代001

**调用技能**：`powerby-product` - 需求定义

**传递的任务描述模板**：
```
基于以下信息执行需求定义：
- 产品想法: {用户输入的产品想法}
- 目标用户: {用户群体}
- 核心问题: {核心业务问题}
- 预期时间: {时间线}
- 约束条件: {约束条件}

请生成：
1. 完整的PRD文档 (prd.md)
2. 结构化功能点清单 (function-points.md)

遵循MVP优先原则，确保核心功能聚焦。
```

**预期输出**：
```
✅ P1 需求定义完成

📄 输出文档:
  ├── docs/iterations/001-{项目名}/prd.md (产品需求文档)
  └── docs/iterations/001-{项目名}/function-points.md (功能点清单)

🔒 质量门禁 Gate 1: MVP范围合理性检查
  ✓ 核心价值定义清晰
  ✓ 功能点完整性验证
  ✓ 最小可行产品范围确认

🎯 下一步: 使用 /powerby.clarify 进入需求澄清阶段
```

---

### /powerby.clarify (P2 - 需求澄清)

**执行步骤**：

1. **调用powerby-product技能**
   - 传递参数：PRD路径、功能点路径、澄清问题数量
   - 要求进行结构化澄清，生成澄清记录

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/clarifications.md`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P2
   - 标记Gate 2为已通过

**调用技能**：`powerby-product` - 需求澄清

**传递的任务描述模板**：
```
基于现有需求文档进行结构化澄清：
- PRD文档路径: {prd_path}
- 功能点清单路径: {function_points_path}
- 澄清问题数量: {questions}

请生成澄清记录文档 (clarifications.md)，包含：
1. 识别的模糊点
2. 澄清后的明确描述
3. 边界条件
4. 业务规则
```

**预期输出**：
```
✅ P2 需求澄清完成

📄 输出文档:
  └── docs/iterations/001-{项目名}/clarifications.md (澄清记录)

🔒 质量门禁 Gate 2: 澄清完整性检查
  ✓ 模糊点识别完整
  ✓ 边界条件明确
  ✓ 业务规则确认

🎯 下一步: 使用 /powerby.research 进入技术调研阶段
```

---

### /powerby.research (P3 - 技术调研)

**执行步骤**：

1. **调用powerby-architect技能**
   - 传递参数：PRD路径、功能点路径、澄清记录路径
   - 要求进行技术可行性调研

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/research.md`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P3
   - 标记Gate 3为已通过

**调用技能**：`powerby-architect` - 技术调研

**传递的任务描述模板**：
```
基于需求文档进行技术调研：
- PRD文档路径: {prd_path}
- 功能点清单路径: {function_points_path}
- 澄清记录路径: {clarifications_path}

请生成技术调研报告 (research.md)，包含：
1. 技术选型分析
2. 可行性评估
3. 风险评估
4. 推荐方案
```

**预期输出**：
```
✅ P3 技术调研完成

📄 输出文档:
  └── docs/iterations/001-{项目名}/research.md (技术调研报告)

🔒 质量门禁 Gate 3: 技术调研完整性
  ✓ 技术选型评估
  ✓ 可行性分析
  ✓ 风险评估完成

🎯 下一步: 使用 /powerby.design 进入架构设计阶段
```

---

### /powerby.design (P4 - 架构设计)

**执行步骤**：

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

**调用技能**：`powerby-architect` - 架构设计

**传递的任务描述模板**：
```
基于需求和调研结果进行架构设计：
- PRD文档路径: {prd_path}
- 功能点清单路径: {function_points_path}
- 澄清记录路径: {clarifications_path}
- 调研报告路径: {research_path}

请生成架构设计文档，包含：
1. 系统架构图 (architecture.md)
2. 数据模型 (data-model.md)
3. API契约 (contracts/api.yaml)
```

**预期输出**：
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

---

### /powerby.plan (P5 - 任务规划)

**执行步骤**：

1. **调用powerby-engineer技能**
   - 传递参数：PRD路径、架构文档路径、每日任务数
   - 要求进行详细任务分解和规划

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/tasks.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/checklists/acceptance.md`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P5
   - 标记Gate 5为已通过

**调用技能**：`powerby-engineer` - 任务规划

**传递的任务描述模板**：
```
基于架构设计进行任务规划：
- PRD文档路径: {prd_path}
- 架构文档路径: {architecture_path}
- 每日任务数: {tasks_per_day}

请生成任务计划文档，包含：
1. 详细任务分解 (tasks.md)
2. 验收清单 (checklists/acceptance.md)
```

**预期输出**：
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

---

### /powerby.implement (P6 - 开发实现)

**执行步骤**：

1. **调用powerby-engineer技能**
   - 传递参数：任务计划路径、架构文档路径、是否启用TDD
   - 要求执行开发实现

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/implementation-report.md`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P6
   - 标记Gate 6为已通过

**调用技能**：`powerby-engineer` - 开发实现

**传递的任务描述模板**：
```
基于任务计划执行开发实现：
- 任务计划路径: {tasks_path}
- 架构文档路径: {architecture_path}
- TDD模式: {tdd}

请生成实现报告 (implementation-report.md)，包含：
1. 实现进度
2. 代码质量检查
3. 测试覆盖率
4. 交付物清单
```

**预期输出**：
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

---

### /powerby.review (P7-P8 - 代码审查和交付)

**执行步骤**：

1. **调用powerby-code-review技能**
   - 传递参数：所有阶段文档、PR链接等
   - 要求进行全面的代码审查和项目交付

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/code-review-report.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/delivery-report.md`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P8
   - 标记Gate 7和Gate 8为已通过
   - 更新状态为`completed`

**调用技能**：`powerby-code-review` - 代码审查和交付

**传递的任务描述模板**：
```
执行全面的代码审查和项目交付：
- PRD文档路径: {prd_path}
- 功能点清单路径: {function_points_path}
- 架构文档路径: {architecture_path}
- 任务计划路径: {tasks_path}
- 实现报告路径: {implementation_report_path}
- PR链接: {pr：
_link}

请生成1. 代码审查报告 (code-review-report.md)
2. 项目交付报告 (delivery-report.md)
```

**预期输出**：
```
✅ P7-P8 代码审查和项目交付完成

📄 输出文档:
  ├── docs/iterations/001-{项目名}/code-review-report.md (审查报告)
  └── docs/iterations/001-{项目名}/delivery-report.md (交付报告)

🔒 质量门禁 Gate 7: 代码审查严格性
  ✓ 代码规范检查
  ✓ 安全性审查
  ✓ 性能评估

🔒 质量门禁 Gate 8: 项目交付完整性
  ✓ 功能验收通过
  ✓ 文档交付完整
  ✓ 知识转移完成

🎉 项目完成！所有P0-P8阶段已成功完成
```

## 错误处理

### 前置条件错误

**场景**：用户尝试执行需要前置阶段的指令

**响应示例**：
```
❌ 前置条件不满足

当前阶段: P0
需要阶段: P1

💡 建议: 请先执行 /powerby.initialize 完成项目初始化
```

### 文档缺失错误

**场景**：必需文档不存在

**响应示例**：
```
❌ 缺少必需文档

缺失文件: docs/constitution.md

💡 建议: 请先执行 /powerby.initialize 创建项目宪章
```

### 流程跳跃错误

**场景**：用户尝试跳过中间阶段

**响应示例**：
```
❌ 无法跳过阶段

错误: 无法从P0直接跳转到P3

💡 建议: 正确流程: P0 → P1 → P2 → P3
   当前应执行: /powerby.define
```

### 门禁检查失败

**场景**：质量门禁检查未通过

**响应示例**：
```
❌ Gate 1检查失败

失败原因: MVP范围不合理

💡 建议:
   - 重新审视核心价值定义
   - 削减非必要功能
   - 使用 /powerby.define 重新定义需求
```

## 查看当前状态

要查看项目当前状态，可调用Flow Guardian：

```
/powerby-flow-guardian analyze
```

Flow Guardian将提供：
- 当前项目阶段
- 已完成的门禁
- 缺失的文档
- 建议的下一步操作

## 使用示例

### 示例1：完整项目流程

```
用户: 我想构建一个任务管理系统

助手: 我将帮助您通过PowerBy流程完成这个项目。让我们开始：

步骤1: 项目初始化
/powerby.initialize 任务管理系统 "一个帮助团队协作的任务管理应用"

步骤2: 需求定义
/powerby.define "我想构建一个任务管理系统，帮助团队更好地协作" --user-group "团队成员和项目经理" --problem "任务分配不清晰，协作效率低"

步骤3: 需求澄清
/powerby.clarify

步骤4: 技术调研
/powerby.research

步骤5: 架构设计
/powerby.design

步骤6: 任务规划
/powerby.plan --tasks-per-day 3

步骤7: 开发实现
/powerby.implement --tdd

步骤8: 代码审查
/powerby.review
```

### 示例2：查看状态

```
用户: 项目当前状态如何？

助手:
/powerby-flow-guardian analyze

输出：
当前阶段: P3 (技术调研)
已完成: P0, P1, P2
已完成门禁: Gate 1, Gate 2
当前门禁: Gate 3
下一步: /powerby.research
```

## 最佳实践

### ✅ 推荐做法

1. **严格遵循流程**：不跳过任何阶段或门禁
2. **充分确认**：每个阶段都等待门禁检查通过
3. **记录决策**：所有重要决策都有文档记录
4. **及时更新**：状态变化立即更新到项目元数据
5. **主动澄清**：遇到模糊点主动询问Flow Guardian

### ❌ 避免做法

1. **流程跳跃**：不要跳过前置阶段直接进入后续阶段
2. **门禁绕过**：不要绕过质量门禁检查
3. **文档滞后**：避免代码实现与文档不同步
4. **重复造轮子**：优先使用现有库和服务

## 与其他技能的协作

### powerby-product (P0-P1)
- 项目初始化
- 需求定义+澄清（融合）

### powerby-architect (P3-P4)
- 技术调研
- 架构设计

### powerby-engineer (P5-P6)
- 任务规划
- 开发实现

### powerby-code-review (P7)
- 代码审查
- MVP交付

### powerby-fullstack
- 快速流程（≤3天需求）

### powerby-flow-guardian
- 状态检查
- 问题诊断
- 操作指导

每次执行指令时，调用相应技能完成任务，并确保Flow Guardian跟踪状态变化。

## 质量门禁

每个阶段都有对应的质量门禁检查：

| Gate | 阶段 | 检查要点 |
|------|------|----------|
| Gate 1 | P1→P3 | MVP需求定稿 |
| Gate 3 | P3→P4 | 技术调研完整性 |
| Gate 4 | P4→P5 | 架构设计清晰性 |
| Gate 5 | P5→P6 | 开发规划详细性 |
| Gate 6 | P6→P7 | 开发实现质量 |
| Gate 7 | P7→完成 | 代码审查严格性 |
| Gate 8 (可选) | P8→完成 | 运维交付完整性 |

> **说明**：Gate 8属于运维流程，独立于MVP开发流程，在MVP验证成功后进行。

只有通过门禁检查，才能进入下一阶段。
