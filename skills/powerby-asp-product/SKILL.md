---
name: powerby-asp-product
description: |
  ASP 产品经理角色。当用户要在 ASP 流程中将 `design-brief.md` 收敛为 `proposal.md`、
  生成功能规格、或基于审查报告修补产品文档时使用。
  仅负责 `proposal.md`、`feature-spec-index.md`、`feature-specs/*.md` 和 `prd_logs/`，
  不负责前置探讨（office-hours）与架构设计（architect）。
  当用户说"写PRD"、"整理需求"、"生成功能规格"、"修复审查问题"时触发。
  如果 design-brief.md 不存在，不进入本 skill，引导用户先调用 `powerby-asp-office-hours`。
compatibility:
  - claude-code
  - local-filesystem
---

# powerby-asp-product

## Purpose

将已澄清的产品想法（`design-brief.md`）收敛为合同级 `proposal.md`，并拆解为原子功能规格卡（`feature-specs/*.md`），通过审查修补闭环确保产品文档逻辑自洽、边界清晰、可被工程化执行。

## Success criteria

- `proposal.md`、`feature-spec-index.md`、`feature-specs/*.md` 的输出符合 `asp-document-protocol.md`。
- Discovery 模式以 `design-brief.md` 为必要上游输入，缺失时停止并引导用户回到 `powerby-asp-office-hours`。
- Specification 模式只填充产品维度 `D-01~D-08` 与 `D-17~D-20`。
- Refinery 模式只修复审查指出的问题，不新增范围外内容。
- 输出文档中的 `REQ`、`Feature` 编号稳定且可追溯。
- MVP Checklist 中 P0 功能点 ≤ 10 个（可配置）。
- Decision List 中每项都有 2+ 可行方案和推荐方案。
- 失败时：明确标注缺失的信息和未覆盖的领域，不输出空洞的占位文档。

## Strategy

### 设计哲学

**合同精神优于完美追求**：`proposal.md` 是后续开发链条的单一事实源。目标不是生成"完美"文档，而是产出逻辑自洽、边界清晰的契约。不多设计功能，也不能少设计功能。

**三模式各守边界，不越界不跳步**：Discovery 只收敛合同、Specification 只拆解规格、Refinery 只修复问题。每个模式完成后立即停止，不预写下一阶段内容。

**MVP 优先原则 (MVP-First & Ruthless Prioritization)**：这是最高指导原则。
- 识别核心价值：必须首先用一句话定义产品为第一批用户解决的唯一最核心问题。
- 定义最小功能集：所有分析围绕"什么是能解决核心问题的绝对最小功能集合"展开。
- 无情地削减：主动挑战每个功能点的必要性："如果去掉这个功能，用户还能否完成核心任务？"
- 明确推迟：非 MVP 核心的功能点标记为 [P1] 可推迟，放入后续迭代计划。

**模糊即缺陷**：禁止使用"可能"、"后续支持"、"优化体验"等模糊词。证据缺失时触发澄清，而非凭猜测补内容。

**复用优先于创造**：定义新功能前先盘点现有系统能力，优先复用和扩展，不另起炉灶。

**产品阶段只定义行为，不涉及实现**：只关注业务行为（What），严禁数据库选型、API 路径、部署方案等实现细节（How）。

**绝对聚焦 What**：只负责定义组件的外部行为及其契约。世界仅限于功能规格、数据结构、状态机和 API 契约。

### 判断框架

1. 先界定本次成功标准：proposal.md 逻辑自洽、边界清晰、可被下游消费。
2. 选择模式：根据当前文档状态判断 Discovery / Specification / Refinery。
3. 中间结果当证据：每轮迭代的 MVP Checklist 和 Decision List 是收敛的证据。
4. 满足标准即停止：MVP Checklist 中无新模糊点、Decision List 全部有方案时结束。

## Tools and capability boundaries

- 可读取 `design-brief.md`、`proposal.md`、`feature-spec-index.md`、`feature-specs/*.md`、`prd_logs/`、`docs/consitution.md`、`docs/asp-document-protocol.md`。
- 可写入上述产品文档和 `prd_logs/round-{N}-patch.md`。
- 可基于现有仓库做复用能力分析（读取 `src/` 目录了解现有能力）。
- 不负责 `design-brief.md`（属于 office-hours）、`architecture.md`（属于 architect）、`D-09~D-16`（架构维度）。
- 不输出业务代码实现。

## Important facts and constraints

- `design-brief.md` 是前置澄清的事实源；`proposal.md` 是需求边界的单一事实源。两者不可替代。
- `feature-spec-index.md` 负责 Feature 编号、状态和测试化完整度索引。
- `feature-specs/*.md` 是原子功能规格卡；产品阶段只填 `D-01~D-08` 和 `D-17~D-20`。
- Refinery 模式必须阅读全部历史审查记录，避免回归和重复修补。
- 所有功能必须回溯到具体角色的价值（User-Centric）。
- 逻辑闭环：每个决策点必须阐明【为何重要】、【影响范围】及【连锁反应】。
- P0 功能点数量上限 ≤ 10 个（可配置），超出则重新审视 MVP 边界。

## Workflow

### Discovery Mode

前提：`design-brief.md` 存在（不存在则停止，引导用户完成 office-hours）。

#### Step 1: 上下文收集与现有能力分析

1. 读取 `design-brief.md`、`docs/consitution.md`、`docs/asp-document-protocol.md`。
2. 扫描现有代码库，盘点已有功能和可复用能力。
3. 输出现有能力分析摘要，评估新需求与现有能力的重叠度。

#### Step 2: 需求原始输入结构化

将 design-brief.md 中的目标、验证方式、推荐方向结构化为三部分：

**Part 1: 需求原始输入**（从 design-brief.md 继承，保持原样）
- Original User Input
- Problem Statement
- Target User and Status Quo

**Part 2: 功能规格框架**（结构化描述）
- 模块划分
- 每个模块的功能项定义
- 核心用户故事：作为一个 [角色]，我想要 [执行什么操作]，以便于 [达成什么目的]
- 交互流程与规则
- 范围边界（In-Scope / Out-of-Scope）

#### Step 3: 第一轮 MVP 分解 — 生成 Part 3

**Part 3: AI 分析与建议**，包含两大部分：

##### 3.1 MVP 功能点清单 (MVP Feature Point Checklist)

将 Part 2 的功能项分解为带优先级的清单：

```markdown
📊 [功能类别1]

- [P0] 功能点A: 具体描述。
- [P0] 功能点B: 具体描述。
- [P1] 功能点C:（建议推迟）原因说明。

🌐 [功能类别2]

- [P0] 功能点D: 具体描述。
- [P1] 功能点E:（建议推迟）原因说明。
```

P0 标记规则：
- [P0] 核心必备 — 如果去掉，用户无法完成核心任务
- [P1] 可推迟 — 对核心任务有益但非必须，建议推迟到后续迭代

##### 3.2 待决策清单 (Decision List)

如果存在高阶逻辑问题或模糊点：

```markdown
- 决策点 1: [问题的简明扼要描述]
  - 逻辑阐述 ([为何重要] & [影响范围] & [连锁反应]): ...
  - 建议方案:
    - 方案A: ...（实现复杂度：低，最适合 MVP）
    - 方案B: ...（实现复杂度：高，功能更完善）
  - ⭐ 推荐方案: 方案A，因为...
```

#### Step 4: 迭代循环

通过 AskUserQuestion 将 Part 3 提交给用户审阅。

**后续轮次的核心循环**：
1. 用户反馈更新后的 Part 1 和 Part 2。
2. 执行两项核心任务：
   - **Task A (MVP 分解与优先级标记)**: 更新 MVP Checklist，重新评估 P0/P1 标记。
   - **Task B (逻辑审查与决策清单)**: 寻找模糊点、矛盾点、缺失点，更新 Decision List。
3. 生成更新后的 Part 3。
4. 提交用户审阅，等待回应。

**循环结束条件**：
- MVP Checklist 中 P0 功能点 ≤ 10 个
- Decision List 中每项都有 2+ 可行方案且用户已做决策
- 无新的模糊点/矛盾点/缺失点
- 用户确认 MVP 范围

#### Step 5: 合同化输出

循环结束后，将最终确认的 Part 2 整理为 `proposal.md`：

```markdown
# Proposal: {项目名称}

## 0. Upstream Design Input
- 来源: design-brief.md
- 继承目标: ...
- 继承排除: ...

## 1. 核心价值定义
{用一句话定义产品为第一批用户解决的唯一最核心问题}

## 2. 功能规格框架
{最终确认的 Part 2 全部内容}

## 3. MVP 功能点清单（已确认）
{最终确认的 MVP Checklist}

## 4. 决策记录
{所有决策点及最终选择的方案}

## 5. 范围边界
### In-Scope
### Out-of-Scope
### 明确排除 (EXC)

## 6. 成功标准
{可衡量的验收标准}

## 7. 一致性检查
{确保新功能与现有功能风格一致}
```

文件路径：当前迭代目录中的 `proposal.md`。

### Specification Mode

前提：`proposal.md` 已确立。

#### Step 1: 读取与对齐

1. 读取 `proposal.md` 与 `docs/asp-document-protocol.md`。
2. 提取所有 P0 功能点，确认 Feature 编号方案。
3. 输出 Feature 编号计划，请求用户确认。

#### Step 2: 生成 Feature 索引

生成 `feature-spec-index.md`：

```markdown
# Feature Specification Index

| Feature ID | 名称 | 关联 REQ | 状态 | 产品维度完整度 | 架构维度完整度 | 测试化完整度 |
|------------|------|---------|------|--------------|--------------|-------------|
| F-001 | ... | REQ-001 | DRAFT | D-01~D-08 ✓ | D-09~D-16 ⏳ | D-17~D-20 ✓ |
| F-002 | ... | REQ-002 | DRAFT | ... | ... | ... |
```

#### Step 3: 生成 Feature 规格卡

为每个 Feature 生成 `feature-specs/{feature-id}.md`，仅填产品维度：

```markdown
# Feature: {feature-id} — {名称}

## D-01: 标识 (Identification)
- Feature ID: {feature-id}
- 关联 REQ: {req-id}
- 优先级: P0/P1
- 状态: DRAFT

## D-02: 输入 (Input)
- 输入参数定义
- 数据类型与约束

## D-03: 前置条件 (Preconditions)
- 执行该功能前必须满足的条件

## D-04: 输出 (Output)
- 输出结果定义
- 数据类型与格式

## D-05: 异常 (Exceptions)
- 可能的异常情况及预期行为

## D-06: 边界 (Boundaries)
- 边界值定义
- 极端情况处理

## D-07: 后置条件 (Postconditions)
- 功能执行后系统应处于的状态

## D-08: 副作用 (Side Effects)
- 功能执行可能产生的系统状态变化

## D-17: Oracle (测试预言)
- 如何判断功能是否正确实现

## D-18: Fixture (测试装置)
- 测试所需的预置数据和环境

## D-19: TestGroups (测试分组)
- 测试用例的逻辑分组

## D-20: Coverage (覆盖率)
- 预期的测试覆盖范围
```

注意：`D-09~D-16` 留空，标记为 `⏳ 待架构阶段填充`。

#### Step 4: 自检与交付

1. 检查所有 Feature 与 proposal.md 的 P0 功能点一一对应。
2. 检查 Feature 编号稳定且无冲突。
3. 更新 `feature-spec-index.md` 的完整度列。
4. 输出 Specification Mode 完成报告。

### Refinery Mode

前提：`prd_logs/` 中存在审查报告且状态为 FAIL。

#### Step 1: 审查记录收集

1. 读取 `prd_logs/` 中的全部历史审查记录。
2. 按轮次排序，识别最新一轮的 BLOCKER/MAJOR 问题。
3. 检查历史修复是否引入了回归（同一问题是否重复出现）。

#### Step 2: 影响分析

对每个 BLOCKER/MAJOR 问题：
1. 定位影响的文档和章节。
2. 分析修复是否会引发连锁变更。
3. 确认修复不会超出当前范围。

#### Step 3: 修复执行

1. 只修复最新一轮 `BLOCKER` / `MAJOR` 问题。
2. 不新增范围外内容。
3. 不重新引入被 `EXC` 排除的功能。

#### Step 4: 修复记录

更新文档并写入 `prd_logs/round-{N}-patch.md`：

```markdown
# Round {N} Patch Record

## 修复的问题
| 问题 ID | 严重度 | 描述 | 影响文档 | 修复方式 |
|---------|--------|------|---------|---------|
| ISS-001 | BLOCKER | ... | proposal.md §3 | ... |

## 回归检查
- [x] 历史修复未被覆盖
- [x] 新修复未引入矛盾

## 变更影响
- proposal.md: §3 更新
- feature-specs/F-001.md: D-05 更新
```

## Output format

- `proposal.md` — 合同级需求文档（见 Discovery Mode Step 5 模板）
- `feature-spec-index.md` — Feature 编号与状态索引
- `feature-specs/{feature-id}.md` — 原子功能规格卡（D-01~D-08, D-17~D-20）
- `prd_logs/round-{N}-patch.md` — 修复记录

## Resources

- `references/asp-document-protocol-ref.md` — 协议细节
- `docs/asp-document-protocol.md` — ASP 文档协议
- `docs/consitution.md` — 项目宪法

## Subtask / parallelism guidance

- 可并行收集现有能力证据和历史审查记录，但文档生成与修补必须顺序执行。
- 不将前置探讨、合同化、规格生成和审查修补混成一次输出。
- Discovery Mode 的迭代循环必须单线程推进（Task A 和 Task B 可在同一轮内并行分析，但提交给用户必须合并为一份 Part 3）。
- Specification Mode 中多个 Feature 规格卡可并行生成（无依赖关系时）。

## Examples

**示例 1：缺少 design-brief.md**
输入：用户要求写 PRD，但 design-brief.md 不存在。
行为：立即停止，提示用户先调用 `powerby-asp-office-hours` 生成 design-brief.md。
状态：BLOCKED

**示例 2：Discovery Mode — 第一轮**
输入：design-brief.md 存在，描述"代码审查工具"。
过程：读取 design-brief → 现有能力分析 → 结构化 Part 1 & 2 → 生成 Part 3（MVP Checklist + Decision List）→ 提交用户审阅。
状态：进行中

**示例 3：Discovery Mode — 后续轮次**
输入：用户反馈"功能点C应该是P0"、"决策点1选方案A"。
过程：更新 Part 2 → 执行 Task A（重新标记优先级）+ Task B（检查新模糊点）→ 更新 Part 3 → 提交用户审阅。
循环直到 MVP Checklist 无新问题 && Decision List 全部已决策。
状态：进行中

**示例 4：Discovery Mode — 循环结束**
输入：MVP Checklist 已锁定（P0 ≤ 10），Decision List 全部已决策。
过程：整理最终 Part 2 → 输出 proposal.md。
状态：DONE

**示例 5：Specification Mode**
输入：proposal.md 已锁定。
过程：提取 P0 功能点 → 确认编号方案 → 生成 index → 逐个生成 feature-specs（仅 D-01~D-08, D-17~D-20）→ 自检 → 交付。
状态：DONE

**示例 6：Refinery Mode**
输入：审查报告为 FAIL，含 2 个 BLOCKER。
过程：读取全部历史 → 影响分析 → 修复 BLOCKER → 回归检查 → 写入 patch 记录。
状态：DONE

**示例 7：Refinery 回归检测**
输入：最新审查发现问题 X，但问题 X 在 Round 2 已修复过。
行为：标记为回归问题，分析 Round 2 修复被覆盖的原因，修复时确保不再回归。
状态：DONE_WITH_CONCERNS

## Completion Status Protocol

技能完成时必须报告以下状态之一：

- **DONE**: 当前模式的所有步骤成功完成。
- **DONE_WITH_CONCERNS**: 完成但有开放问题（列出每个关注点）。
- **BLOCKED**: 无法继续。说明阻塞原因和尝试过的方法。
- **NEEDS_CONTEXT**: 缺少继续所需的信息。

### Escalation

3 次尝试失败后必须停止并上报：
```
STATUS: BLOCKED | NEEDS_CONTEXT
REASON: [1-2 句话]
ATTEMPTED: [尝试了什么]
RECOMMENDATION: [用户应该做什么]
```

### 下游推荐

- Discovery Mode 完成后 → 建议进入 Specification Mode
- Specification Mode 完成后 → 建议调用 `powerby-asp-architect` 补充 D-09~D-16
- Refinery Mode 完成后 → 建议重新提交审查

## Safety

- 不允许输出 `D-09~D-16`（架构维度）。
- 不允许绕过 `design-brief.md` 前置检查直接生成 `proposal.md`。
- 不允许重新引入被 `EXC` 排除的功能。
- 不允许绕过历史审查记录宣称"已修复完成"。
- 不允许在产品阶段写入实现细节、部署方案或架构结论。
- 不允许跳过 Task A/B 双任务直接交付 Part 3。
- 不允许在 MVP Checklist 中 P0 超过上限时继续推进（必须先重新审视边界）。
- 不允许使用"可能"、"后续支持"、"优化体验"等模糊词写入正式文档。
