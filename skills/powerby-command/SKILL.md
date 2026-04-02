---
name: powerby-command
description: |
  PowerBy 生态的流程编排核心。解析 /powerby.* 指令，管理 P0-P8 阶段流转，协调各角色技能执行对应工作。
  当用户输入 /powerby.initialize、/powerby.define、/powerby.research 等指令，或需要查看流程状态、推进下一阶段时使用。
  不处理具体的产品设计、架构、工程实现 —— 这些由各角色技能完成。
compatibility:
  - local-filesystem
---

# PowerBy Command

管理 PowerBy 生命周期流程的编排器。解析用户指令，校验阶段前置条件，将任务分派给对应角色技能，追踪阶段状态。

## Purpose

将 P0-P8 生命周期的阶段流转和质量门禁集中管理，使用户只需通过指令驱动流程推进，不必关心阶段依赖和文档校验的细节。成功使用的标志是：每个阶段的前置条件自动校验通过，正确的角色技能被调用，阶段状态被准确记录。

## Success criteria

- 指令被正确解析并匹配到对应阶段
- 前置条件校验完整：缺少必需文档时阻止推进并给出具体缺失项
- 正确的角色技能被调用，任务描述包含必要的文档路径和上下文
- `.powerby/project.json` 阶段状态与实际进度一致
- 失败时给出明确的阻塞原因和建议操作

## Strategy

1. **编排器只做路由，不做执行。** 收到指令后判断属于哪个阶段，校验前置条件，将任务分派给角色技能。不要自己去写 PRD、做架构设计或写代码。

2. **阶段门禁是硬约束。** 跳过阶段意味着缺少上游交付物，下游技能会在错误基础上工作。除非用户明确要求跳过并理解后果，否则严格执行顺序。

3. **状态是事实的反映，不是期望的声明。** 只在角色技能确认完成、输出文档存在后才更新阶段状态。不要在调用前就标记为完成。

4. **增量安全操作。** 对 `.powerby/` 下的文件只做增量更新，永远不覆盖或删除用户已有数据。

5. **模糊输入先澄清。** 当用户指令不完整或歧义时，先确认意图再执行。

## Tools and capability boundaries

- **文件系统读写**：读取 `.powerby/project.json`、`.powerby/iterations.json` 管理状态；读取 `docs/` 下的文档校验前置条件
- **子 Agent 调用**：通过 handoff 调用角色技能（powerby-product、powerby-architect、powerby-engineer、powerby-code-review、powerby-bugfix、powerby-fullstack）
- **不做**：不执行具体的产品设计、技术调研、架构设计、代码编写、代码审查 —— 这些职责下放给对应角色技能
- **不做**：不直接管理 Git 分支 —— 由 powerby-git 和 powerby-github-branch 处理

## Important facts and constraints

### 阶段流转顺序

标准流程：P0(initialize) -> P1(define) -> P3(research) -> P4(design) -> P5(plan) -> P6(implement) -> P7(review)

注意 P2 已跳过（历史设计决策），不存在 P2 阶段。

### 指令到阶段的映射

| 指令 | 阶段 | 角色技能 |
|------|------|---------|
| `/powerby.initialize` | P0 | 内部处理 |
| `/powerby.define` | P1 | powerby-product 或 ASP 流程(powerby-asp-office-hours -> powerby-asp-product) |
| `/powerby.research` | P3 | powerby-architect |
| `/powerby.design` | P4 | powerby-architect |
| `/powerby.plan` | P5 | powerby-engineer |
| `/powerby.implement` | P6 | powerby-engineer |
| `/powerby.review` | P7 | powerby-code-review |
| `/powerby-bugfix` | 独立 | powerby-bugfix |
| `/powerby.quick` | 快速 | powerby-fullstack |

### 各阶段前置文档

| 阶段 | 必需文档 |
|------|---------|
| P0 | 无 |
| P1 | `docs/constitution.md`, `.powerby/project.json` |
| P3 | `docs/{project}/prd.md`, `docs/{project}/function-points.md`, `docs/{project}/clarifications.md` |
| P4 | `docs/{project}/technical-research.md` |
| P5 | `docs/{project}/architecture.md` |
| P6 | `docs/{project}/tasks.md` |
| P7 | `docs/{project}/implementation/implementation-report.md` |

### ASP 流程识别

当用户明确要求 ASP 流程、提到 proposal.md/feature-spec 协议、或需要先做产品方向探讨时，P1 阶段走 ASP 分支：先调用 powerby-asp-office-hours 生成 design-brief.md，再调用 powerby-asp-product 收敛为 proposal.md。不得跳过 design-brief.md 直接生成 proposal.md。

### .powerby/ 安全操作

- 目录已存在时只创建缺失文件，不覆盖
- JSON 更新采用合并策略：保留所有现有字段，只添加缺失字段
- iterations.json 保留所有现有迭代记录

## Workflow

1. **解析指令** — 从用户输入提取指令名称和参数。支持 `/powerby.xxx`、`powerby xxx` 等格式。

2. **校验前置条件** — 检查对应阶段的必需文档是否存在。不满足时报告缺失项和建议操作，不继续执行。

3. **分派任务** — 调用对应角色技能，传递必要的文档路径和上下文参数。P0 阶段由本技能内部处理（创建目录结构和元数据文件）。

4. **验证输出** — 角色技能完成后，检查预期输出文档是否已生成。

5. **更新状态** — 在 `.powerby/project.json` 中记录阶段完成状态和门禁通过信息。

6. **报告结果** — 向用户展示完成状态、输出文档列表、下一步建议。

## Output format

每个阶段执行完成后输出：

```
[阶段] 完成状态

输出文档:
  - <文件路径列表>

阶段状态: <当前阶段> 已完成
下一步: <下一阶段指令和说明>
```

前置条件不满足时输出：

```
前置条件不满足

当前阶段: <阶段>
缺失: <具体缺失项>
建议: <应执行的操作>
```

## Resources

- `.powerby/project.json` — 项目元数据和阶段状态
- `.powerby/iterations.json` — 迭代追踪记录

## Subtask / parallelism guidance

- 每个阶段串行执行，不允许并行跨阶段
- Bug-Fix 和快速流程独立于标准流程，可并行进行
- 分支管理操作异步委托给 powerby-github-branch，不阻塞主流程

## Examples

**Example 1: 项目初始化**
Input: `/powerby.initialize 任务管理系统 "帮助团队协作的任务管理应用"`
Output: 创建 .powerby/ 目录结构、project.json、iterations.json、docs/constitution.md，报告 P0 完成。

**Example 2: 前置条件不满足**
Input: `/powerby.research`（但 P1 阶段未完成）
Output: 报告缺失 prd.md、function-points.md，建议先执行 /powerby.define。

**Example 3: ASP 流程**
Input: `/powerby.define`（用户要求 ASP 流程）
Output: 先调用 powerby-asp-office-hours，确认 design-brief.md 后调用 powerby-asp-product 生成 proposal.md。

## Safety

- 不覆盖、不删除 `.powerby/` 下的任何现有文件或用户数据
- 不跳过前置阶段的门禁检查（用户明确确认风险除外）
- 不在角色技能完成前标记阶段为完成
- 不直接执行角色技能的职责（产品设计、架构、编码等）
- 不把推断结果写成显式事实
