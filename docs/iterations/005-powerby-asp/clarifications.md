# 需求澄清记录

**项目名称**: PowerBy Autonomous Spec Protocol (ASP)
**迭代编号**: 005
**创建日期**: 2026-02-09

---

## 澄清会话记录

### 日期: 2026-02-09

#### Q1: Orchestrator 实现方式

**问题**: ASP 的 Orchestrator 在 Claude Code 的技术约束下如何实现？Claude Code 的 Task 工具可以启动子 Agent，但无法在同一会话中维护真正的上下文隔离（Reviewer 看不到 Product 的思考过程）。您期望的实现方式是？

**选项**:
- A. 单会话模拟隔离 - 通过 Prompt 策略模拟上下文隔离（务实方案，MVP 推荐）
- B. 混合方案 - Product 在主会话，Reviewer 通过 Task 子 Agent 运行
- C. 多 Agent 真隔离 - 使用 Task 工具启动独立子 Agent（更接近 PRD 描述，但复杂度高）

**答案**: **A. 单会话模拟隔离**

**影响**: Reviewer 的上下文隔离通过 Prompt 策略实现，而非物理隔离。Orchestrator 在调用 Reviewer 时仅传递 spec.md 和 constitution.md 的文件内容，屏蔽 Product Agent 的思考过程。

---

#### Q2: 与现有 Skill 的关系

**问题**: ASP 与现有 powerby-product 和 powerby-reviewer 的关系是什么？PRD 中定义了新的 Agent 角色（v4.0），但项目中已有同名 skill。您的意图是？

**选项**:
- A. 创建编排 Skill - 保留现有 skill，新建 orchestrator 来编排调用（增量扩展，复用优先）
- B. 替换现有 Skill - 用 ASP 定义的新版本替换现有 SKILL.md
- C. 新建独立 Skill - 创建全新的 skill（如 powerby-asp-product 等），保留现有 skill 不变

**答案**: **C. 新建独立 Skill**

**影响**: 将创建三个全新的 skill：
- `powerby-asp-product` - ASP 版本的产品经理（三种模式：Discovery/Specification/Refinery）
- `powerby-asp-reviewer` - ASP 版本的审查员（对抗性审查 + 机器可读输出）
- `powerby-asp-visualizer` - 全景图生成器（Mermaid 驱动）

现有的 `powerby-product` 和 `powerby-reviewer` 保持不变，两套体系并行存在。

---

#### Q3: MVP 范围

**问题**: ASP 的 MVP 边界是什么？PRD 中包含了 5 个阶段（Discovery → Drafting → Refining → Visualizing → Confirmation），但 Visualizer 被标记为 P1 优先级。为了尽快上线验证核心价值，MVP 应该包含哪些阶段？

**选项**:
- A. 核心三阶段 - 只包含 Discovery + Drafting + Refining（推荐）
- B. 完整五阶段 - 一次性实现全部五个阶段
- C. 最小两阶段 - 只包含 Discovery + Drafting

**答案**: **B. 完整五阶段**

**影响**: MVP 将一次性实现全部五个阶段，包括 Visualizer 和 Confirmation。所有功能点均标记为 P0 优先级。

---

#### Q4: 文件目录结构

**问题**: ASP 的文件目录结构与现有项目约定存在冲突。PRD 定义的路径是 `.powerby/specs/{feature}/`，但现有项目使用 `docs/iterations/{id}-{name}/`。您期望采用哪种目录结构？

**选项**:
- A. 沿用现有结构 - 继续使用 `docs/iterations/{id}-{name}/`（推荐）
- B. 采用 PRD 新结构 - 创建 `.powerby/specs/{feature}/`
- C. 两者并存 - ASP 产物存放在 `.powerby/specs/`，最终交付物同步到 `docs/iterations/`

**答案**: **A. 沿用现有结构**

**影响**: ASP 的所有产物（proposal.md、spec.md、prd_logs/、product-map.md）将存放在 `docs/iterations/{id}-{name}/` 目录下，与现有迭代管理体系保持一致。

---

#### Q5: 黑盒循环透明度

**问题**: 黑盒精炼循环的透明度如何？用户输入初始需求后，Product-Reviewer 的 PK 循环是完全自动运行（用户等待最终结果），还是每轮循环都需要用户确认？

**选项**:
- A. 全自动黑盒 - 用户只在 Discovery 阶段回答问题，之后完全自动运行
- B. 全自动+摘要 - 循环全自动运行，结束后展示 prd_logs/ 摘要
- C. 半自动透明 - 每轮 Review 结果展示给用户，用户可选择介入

**答案**: **A. 全自动黑盒**

**影响**: 用户只在 Discovery 阶段回答问题，之后 Drafting + Refining 完全自动运行。用户只看到最终的 spec.md 和 product-map.md。

---

#### Q6: 触发命令名称

**问题**: ASP 的触发命令名称是什么？PRD 中提到的是 `/powerby.auto_product`，但现有命令体系使用 `/powerby-xxx` 格式。

**选项**:
- A. /powerby-asp
- B. /powerby-auto-product
- C. /powerby-define-v2

**答案**: **A. /powerby-asp**

**影响**: 用户通过 `/powerby-asp "需求描述"` 触发 ASP 全流程。

---

## 覆盖度状态表

| 类别 | 状态 | 备注 |
|------|------|------|
| 功能范围与边界 | Clear | In-Scope/Out-of-Scope 已明确 |
| 数据模型与实体 | Clear | 文件契约已定义 |
| 交互与UX流程 | Clear | 完整用户旅程已定义 |
| 非功能属性 | Clear | 循环限制(5轮)、Token 优化策略已定义 |
| 集成与外部依赖 | Clear | 依赖 constitution.md、现有迭代管理框架 |
| 边界情况与失败处理 | Clear | ESCALATION 机制、异常流程已定义 |
| 约束与权衡 | Clear | 单会话模拟隔离的权衡已记录 |
| 术语一致性 | Clear | Data Dictionary 要求已纳入 spec.md 规范 |
| 完整性信号 | Clear | Gate 1 + Gate 2 双门禁 |
| 待办项/占位符 | Clear | 无遗留待决策项 |

## 遗留问题清单

> 无遗留问题。所有关键决策点已在澄清阶段解决。

---

## 补充澄清（2026-02-09 第二轮）

#### Q7: 实现载体约束

**问题**: 用户补充需求，明确实现方式。

**用户原话**:
> 1. 我希望基于 skill 规范完成需求，请严格遵循 skill 规范，定义 skill 提示词，用 skill 角色完成任务，而不是写代码
> 2. review 的过程也是调用 skill 的提示词完成

**影响**:
- **所有 Agent 角色**（Product、Reviewer、Visualizer）均通过 SKILL.md 提示词文件定义
- **Orchestrator** 是一个命令文件（`.claude/commands/powerby-asp.md`），通过 `handoffs` 机制调用 Skill
- **Review 循环**通过 Prompt 指令调用 `powerby-asp-reviewer/SKILL.md` 的提示词完成，不写任何代码
- **实现交付物**：3 个 SKILL.md 文件 + 1 个命令文件 + 1 个 marketplace.json 更新
- PRD 已更新至 v1.1.0，功能点清单已更新至 v1.1.0，新增 FP-020（marketplace.json 更新）

**文档同步状态**:
- [x] prd.md 已更新（新增 1.5 实现约束章节，更新 In-Scope 表格）
- [x] function-points.md 已更新（FP-016~FP-019 重写，新增 FP-020）
- [x] clarifications.md 已更新（本条记录）

---

## 补充澄清（2026-02-09 第三轮）

#### Q8: 流程隔离声明

**问题**: 用户补充需求，明确 ASP 与现有流程的关系。

**用户原话**:
> 补充，新的流程先定义为 powerby-asp，确保跟之前的流程严格区分开。新的 powerby-asp 是全新的研发流程，禁止与之前混淆。

**影响**:
- **powerby-asp 是全新的、独立的研发流程**，与现有 P0-P8 生命周期流程完全隔离
- **禁止混淆**：ASP 的五阶段（DISCOVERY → DRAFTING → REFINING → VISUALIZING → CONFIRMATION）与 P0-P8 无任何继承或映射关系
- **命名隔离**：所有 ASP 相关 Skill 以 `powerby-asp-` 为前缀，命令为 `/powerby-asp`
- **角色隔离**：`powerby-asp-product` ≠ `powerby-product`，两者是完全不同的角色定义
- **产物隔离**：ASP 的 spec.md ≠ 现有流程的 prd.md，两者是不同的文档规范
- **门禁隔离**：ASP Gate 1/Gate 2 与现有 Gate 1-8 是完全独立的质量检查体系
- 优先级标记从 `[P0]` 改为 `[核心]`，避免与旧流程阶段编号混淆

**文档同步状态**:
- [x] prd.md 已更新至 v1.2.0（新增 1.6 流程隔离声明章节，含对比表格和隔离规则）
- [x] function-points.md 已更新至 v1.2.0（优先级标记改为 `[核心]`，Gate 名称加 ASP 前缀）
- [x] clarifications.md 已更新（本条记录）
