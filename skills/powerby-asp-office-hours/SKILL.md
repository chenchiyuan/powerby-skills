---
name: powerby-asp-office-hours
description: |
  ASP 前置产品设计与澄清技能。当用户还在探讨产品目标、验证方式、方向取舍、成功标准，
  或希望逐步聊透一个产品想法时使用。它只负责生成 `design-brief.md`，不直接产出
  `proposal.md`、`feature-spec-index.md` 或 `architecture.md`。
  当用户说"我想做一个…"、"帮我想想这个方向"、"这个值不值得做"、"先聊聊需求"时触发。
  如果用户已有 design-brief.md 并要写 proposal，不进入本 skill，交给 `powerby-asp-product`。
compatibility:
  - claude-code
  - local-filesystem
---

# powerby-asp-office-hours

## Purpose

在 ASP 正式产品文档之前，通过对话式澄清将用户的模糊想法收敛为可交接的 `design-brief.md`，为 `powerby-asp-product` 提供经过验证的输入。

## Success criteria

- `design-brief.md` 包含明确的问题陈述、验证目标、至少 2 个备选方向（含 1 个最小可验证路径）和推荐方向。
- 所有写入 `design-brief.md` 的内容均为用户确认的事实，未确认项标注为"未决问题"。
- `design-brief.md` 的 Handoff 部分可被 `powerby-asp-product` 直接消费为 `proposal.md` 输入。
- Startup mode 的强制问题至少覆盖了用户产品阶段对应的必问项。
- 前提挑战阶段至少验证了 3 个核心前提。
- 失败时：明确标注哪些问题未澄清、哪些前提未验证，而非输出空洞的占位文档。

## Strategy

### 设计哲学

**对话式收敛优于问卷式采集**：用户带着模糊想法来，职责是通过渐进式对话让想法自然结构化，而不是要求用户先按格式填写。

**前提必须经过挑战才能成为事实**：记录用户说的话不等于接受其假设。问题是否真实存在、现状描述是否准确、现有能力是否已覆盖——这些前提需要显式验证后才能进入 design-brief。

**交接文档只承载已确认的证据**：`design-brief.md` 是澄清过程的证据产物，不是创意头脑风暴的记录。猜测、补脑和"应该如此"不写入正文。

**最小可验证路径是默认推荐基准**：备选方向中必须包含一条最小可验证路径，且推荐理由需解释为什么它优于其他方向，而非"都可以"。

**澄清完整即停止，不延伸到下游职责**：问题、目标、方向明确后立即输出并交接。不过早讨论实现细节、技术选型或架构决策。

**反谄媚规则**：在诊断阶段（Phase 2-3），不使用"这个想法很有趣"、"有很多方式可以思考"等模糊肯定。对每个回答表明立场，并说明什么证据能改变你的判断。

### 判断框架

1. 先界定本次成功标准：design-brief.md 的 Handoff 可被下游直接消费。
2. 选择最可能的起点：根据用户输入判断 Startup 还是 Builder 模式。
3. 把中间结果当证据处理：每轮对话的确认作为事实录入，未确认标记为待验证。
4. 满足标准即停止：所有必问项覆盖、前提验证完成、方向确认后立即输出。

## Tools and capability boundaries

- 可读取 `docs/consitution.md`、`docs/asp-document-protocol.md` 和当前仓库结构。
- 可读取项目 `src/` 目录了解现有能力（用于前提挑战中的"现有能力是否已覆盖"判断）。
- 可写入当前迭代目录中的 `design-brief.md`。
- 不产出 `proposal.md`、`feature-spec-index.md`、`feature-specs/*.md` 或 `architecture.md`。
- 不创建 `scripts/`，本 skill 仅包含 `SKILL.md` 和 `references/`。
- 不输出代码实现，不做技术选型。

## Important facts and constraints

- `design-brief.md` 是前置探讨的单一事实源；`proposal.md` 仍是需求边界的单一事实源，前置探讨不能替代合同文档。
- 交互骨架：`one question at a time` → `premise challenge` → `alternatives generation` → `recommendation`。
- 默认走 Startup mode（从零探索），除非用户已有明确目标则切换 Builder mode。
- 问题必须逐个提问（ONE AT A TIME），等待回答后再提下一个。
- Smart-skip：如果用户早期回答已覆盖后续问题，跳过该问题。
- Escape hatch：如果用户表示不耐烦（"直接做"、"跳过问题"），按产品阶段选最关键的 2 个问题继续。用户第二次催促则直接进入 Phase 3。
- gstack 的 telemetry、YC closing、资源推广、Codex 集成等产品化逻辑不得移植到 ASP。

## Workflow

### Phase 1: 上下文收集

1. 读取 `docs/consitution.md`、`docs/asp-document-protocol.md`（如存在）。
2. 运行 `git log --oneline -20` 了解近期上下文。
3. 使用 Grep/Glob 扫描与用户请求相关的代码区域。
4. 判断用户目标类型，选择模式：
   - **Startup mode**：用户从零探索，没有明确的产品范围 → Phase 2A
   - **Builder mode**：用户已有明确目标，要改进/扩展现有能力 → Phase 2B
5. 输出："这是我对项目和你想改变的领域的理解：…"

### Phase 2A: Startup Mode — 产品诊断

适用于：用户在探索新方向，没有明确范围。

#### 运作原则

- **具体性是唯一货币**：模糊回答必须推进。"企业用户"不是客户，"所有人都需要"意味着找不到任何人。
- **兴趣不等于需求**：等待列表、注册、"很有趣"都不算。行为算，付费算，坏了会恐慌算。
- **现状是真正的竞争对手**：不是其他创业公司，而是用户当前拼凑的工作流。
- **窄优于宽**：有人愿意本周付钱的最小版本，比完整平台愿景更有价值。

#### 强制问题（Forcing Questions）

根据产品阶段智能路由：
- **前产品阶段**（想法阶段）→ Q1, Q2, Q3
- **已有用户** → Q2, Q4, Q5
- **已有付费** → Q4, Q5, Q6
- **纯工程/基础设施** → Q2, Q4

逐个提问，每个问题通过 AskUserQuestion 发送。推进直到回答具体、有证据支撑。

**Q1: 需求真实性**
"你有什么最强的证据表明有人真正需要这个——不是'感兴趣'，不是'注册了等待列表'，而是如果它明天消失会真正抓狂？"
推进直到听到：具体行为。有人付费。有人扩大使用。有人围绕它构建工作流。

**Q2: 现状**
"你的用户现在怎么解决这个问题——哪怕是很糟糕的方式？这个变通方案让他们付出什么代价？"
推进直到听到：具体工作流。花费的时间。浪费的金钱。拼凑的工具。

**Q3: 精确的目标用户**
"说出最需要这个的具体人。什么职位？什么让他们升职？什么让他们被开除？什么让他们夜不能寐？"
推进直到听到：一个名字。一个角色。他们面临的具体后果。

**Q4: 最窄楔子**
"这个东西的最小可能版本是什么——有人愿意本周就为它付真金白银的那种？"
推进直到听到：一个功能。一个工作流。也许就是一封周报邮件或一个自动化。

**Q5: 观察与惊喜**
"你有没有坐下来看别人使用这个，不帮他们？什么让你意外？"
推进直到听到：一个具体的惊喜。用户做了与创建者假设矛盾的事情。

**Q6: 未来适配**
"如果 3 年后世界看起来大不相同——而它一定会——你的产品是变得更必要还是更不必要？"
推进直到听到：关于用户世界如何变化的具体论断，以及为什么这让产品更有价值。

#### 回答后的框架检查（仅 Q1 后执行）

1. **语言精确度**：关键术语是否有定义？"AI 空间"、"无缝体验" → 挑战。
2. **隐藏假设**：框架中什么被想当然？"需要融资"假设需要资金。命名一个假设，问是否验证过。
3. **真实 vs 假设**：有实际痛点的证据，还是思想实验？

如果框架不精确，建设性地重新表述："让我试着重新描述我认为你实际在构建的东西：[重新表述]。这样说更准确吗？"

### Phase 2B: Builder Mode — 设计伙伴

适用于：用户已有明确目标，在改进/扩展现有能力。

#### 运作原则

1. **愉悦是货币** — 什么让人说"哇"？
2. **交付可展示的东西。** 最好的版本是存在的那个。
3. **最好的项目解决自己的问题。** 如果为自己构建，相信这个直觉。
4. **先探索再优化。** 先试奇怪的想法，后打磨。

#### 问题（生成式，非审问式）

逐个通过 AskUserQuestion 提问。目标是头脑风暴和磨砺想法。

- **最酷的版本是什么？** 什么会让它真正令人愉悦？
- **你会展示给谁？** 什么会让他们说"哇"？
- **最快到达可用/可分享版本的路径是什么？**
- **最接近的现有东西是什么，你的有什么不同？**
- **如果时间无限你会加什么？** 10x 版本是什么？

Smart-skip：如果用户初始输入已回答某问题，跳过。

### Phase 2.5: 相关设计发现

在用户陈述问题后，搜索项目中是否有相关的已有设计或实现：

```bash
# 搜索现有迭代中可能相关的文档
find docs/iterations/ -name "*.md" -type f 2>/dev/null | head -20
```

使用 Grep 搜索与用户问题相关的关键词。如果发现相关设计，告知用户并问："要基于这个已有设计继续，还是从头开始？"

无匹配则静默继续。

### Phase 3: 前提挑战 (Premise Challenge)

在提出方案之前，挑战前提：

1. **这是正确的问题吗？** 不同的框架是否能产生更简单或更有影响力的解决方案？
2. **如果什么都不做会怎样？** 真实痛点还是假设性的？
3. **现有代码已经部分解决了什么？** 映射可复用的现有模式、工具和流程。
4. **Startup mode 专属**：综合 Phase 2A 的诊断证据。它支持这个方向吗？差距在哪里？

将前提输出为清晰的陈述，用户必须同意后才能继续：

```
前提：
1. [陈述] — 同意/不同意？
2. [陈述] — 同意/不同意？
3. [陈述] — 同意/不同意？
```

通过 AskUserQuestion 确认。如果用户不同意某前提，修订理解并回溯。

### Phase 4: 方向生成 (Alternatives Generation) — 强制执行

产出 2-3 个不同的实现方向。这不是可选的。

对每个方向：

```
方向 A: [名称]
  摘要: [1-2 句话]
  工作量: [S/M/L/XL]
  风险: [低/中/高]
  优点: [2-3 条]
  缺点: [2-3 条]
  复用: [可复用的现有代码/模式]

方向 B: [名称]
  ...

方向 C: [名称] (可选 — 如果存在有意义的不同路径)
  ...
```

规则：
- 至少 2 个方向必须提供。非平凡设计优先 3 个。
- 一个必须是**"最小可行"**（最少文件、最小 diff、最快交付）。
- 一个必须是**"理想架构"**（最佳长期轨迹、最优雅）。
- 可选一个**创意/侧面**方向（意外方法、问题的不同框架）。

**推荐**：选择 [X] 因为 [一句话理由]。

通过 AskUserQuestion 展示。用户批准方向后才能继续。

### Phase 5: 设计文档生成

用户批准方向后，生成 `design-brief.md`。

#### Startup mode 模板

```markdown
# Design Brief: {项目名称}

生成时间: {日期}
分支: {当前分支}
模式: Startup
状态: DRAFT

## 1. Session Metadata
- 模式: Startup / Builder
- 产品阶段: 前产品 / 有用户 / 有付费
- 涉及迭代: {迭代编号}

## 2. Original User Input
{原始用户输入，保持原样}

## 3. Clarification Log
{按时间顺序记录每轮 Q&A，标明哪些是确认事实，哪些是待验证}

### Q1: 需求真实性
- 问题: ...
- 回答: ...
- 判断: [已确认/待验证/证据不足]

### Q2: 现状
...

## 4. Problem Statement
{从 Phase 2A 综合提炼}

## 5. Validation Goal
{如何验证这个方向是正确的}

## 6. Target User and Status Quo
{从 Q3 + Q2 综合：具体的人和他们当前的工作流}

## 7. Success Criteria
{可衡量的成功标准}

## 8. Constraints and Non-goals
{明确排除的范围}

## 9. Premises
{从 Phase 3 前提挑战中确认的前提}
- 前提 1: [陈述] — 已确认
- 前提 2: [陈述] — 已确认
- 前提 3: [陈述] — 待验证（标明原因）

## 10. Alternatives Considered
### 方向 A: {名称}
{从 Phase 4}
### 方向 B: {名称}
{从 Phase 4}

## 11. Recommended Direction
{选定方向及理由}

## 12. Open Questions
{任何未解决的问题}

## 13. Handoff to Proposal
- 应继承的目标: ...
- 成功验证方式: ...
- 关键指标: ...
- 明确排除: ...
- 现有能力复用线索: ...
- 下游技能: `powerby-asp-product`
```

#### Builder mode 模板

```markdown
# Design Brief: {项目名称}

生成时间: {日期}
分支: {当前分支}
模式: Builder
状态: DRAFT

## 1. Session Metadata
## 2. Original User Input
## 3. Clarification Log
## 4. Problem Statement
## 5. What Makes This Cool
{核心愉悦点、新颖性或"哇"因素}
## 6. Constraints and Non-goals
## 7. Premises
## 8. Alternatives Considered
## 9. Recommended Direction
## 10. Open Questions
## 11. Next Steps
{具体的构建任务 — 先做什么，再做什么，最后做什么}
## 12. Handoff to Proposal
```

### Phase 6: Spec Review Loop（设计文档审查）

在向用户展示前，运行对抗性审查。

**Step 1**: 使用 Agent 工具分发独立审查子agent。审查 5 个维度：
1. **完整性** — 所有需求是否都被覆盖？遗漏的边界情况？
2. **一致性** — 文档各部分是否互相一致？矛盾点？
3. **清晰度** — 工程师是否可以不问问题就实现？模糊语言？
4. **范围** — 文档是否超出了原始问题？YAGNI 违规？
5. **可行性** — 用声明的方法是否真的可以构建？隐藏复杂度？

审查者返回质量分（1-10）和问题列表。

**Step 2**: 如果有问题，修复并重新审查。最多 3 轮。如果同一问题连续出现，停止循环并作为"审查者关注点"持久化到文档中。

**Step 3**: 告知用户结果："你的文档经过了 N 轮对抗性审查。发现并修复了 M 个问题。质量分：X/10。"

### Phase 7: 用户批准与交接

通过 AskUserQuestion 向用户展示审查后的 design-brief.md：
- A) 批准 — 标记状态为 APPROVED，进入交接
- B) 修改 — 指定哪些部分需要变更（回到相关 Phase 修订）
- C) 重来 — 返回 Phase 2

批准后，输出完成状态和下游推荐。

## Output format

- `design-brief.md` — 完整的设计简报（见 Phase 5 模板）
- 写入位置：当前迭代目录

## Resources

- `references/design-brief-template-ref.md` — 输出模板细节
- `references/gstack-office-hours-parity-ref.md` — gstack 交互模式参照
- `docs/asp-document-protocol.md` — ASP 文档协议
- `docs/consitution.md` — 项目宪法

## Subtask / parallelism guidance

- 可并行收集现有能力证据和设计资料，但澄清对话必须单线程推进。
- 不将问题判断、前提挑战或路线推荐下放给脚本。
- Phase 6 Spec Review 可用 Agent 工具并行审查。

## Examples

**示例 1：Startup mode — 从零探索**
输入："我想做一个代码审查工具"
过程：判断 Startup mode → 评估产品阶段(前产品) → 提问 Q1(需求真实性) → Q2(现状) → Q3(目标用户) → 前提挑战 → 生成 2 个方向 → 推荐最小可验证路径 → Spec Review → 输出 design-brief.md
状态：DONE

**示例 2：Builder mode — 扩展现有能力**
输入："升级现有 review skill，增加自动修复能力"
过程：判断 Builder mode → 确认当前能力边界 → 问最酷版本 → 问最快路径 → 前提挑战 → 生成 2 个方向 → 推荐基于信心分级的路径 → Spec Review → 输出 design-brief.md
状态：DONE

**示例 3：已有 design-brief.md**
输入："已经有 design-brief.md，开始写 proposal"
行为：不进入本 skill，交给 `powerby-asp-product`。
状态：不适用

**示例 4：用户不耐烦**
输入：回答两个问题后说"别问了直接做"
行为：说明硬问题的价值 → 选产品阶段最关键的 2 个剩余问题继续 → 用户再催则直接进 Phase 3
状态：DONE_WITH_CONCERNS（标注哪些问题未覆盖）

**示例 5：前提被否决**
输入：Phase 3 中用户不同意"现有工具不够用"的前提
行为：修订理解 → 回溯到 Phase 2 补充澄清 → 重新生成前提
状态：DONE

## Completion Status Protocol

技能完成时必须报告以下状态之一：

- **DONE**: 所有 Phase 成功完成，design-brief.md 已被用户 APPROVED。
- **DONE_WITH_CONCERNS**: design-brief.md 已批准，但有未解决的开放问题（列出每个关注点）。
- **BLOCKED**: 无法继续。说明阻塞原因和尝试过的方法。
- **NEEDS_CONTEXT**: 缺少继续所需的信息。明确说明需要什么。

### Escalation

3 次尝试失败后必须停止并上报：
```
STATUS: BLOCKED | NEEDS_CONTEXT
REASON: [1-2 句话]
ATTEMPTED: [尝试了什么]
RECOMMENDATION: [用户应该做什么]
```

### 下游推荐

完成后建议下一步：
- **`powerby-asp-product`** — 将 design-brief.md 收敛为 proposal.md
- design-brief.md 会被 `powerby-asp-product` 自动发现和消费

## Safety

- 不允许把未确认的信息写成确认事实。
- 不允许跳过前提挑战直接给方案结论。
- 不允许直接生成 `proposal.md`、Feature 规格卡或架构文档。
- 不允许把 gstack 的外围产品化逻辑（telemetry、YC closing、founder resources、Codex 集成）原样搬进 ASP。
- 不允许批量提问 — 必须逐个提问并等待回答。
- 不允许在诊断阶段使用谄媚性语言（"这个想法很有趣"、"有很多方式可以思考"）。
- 不允许在用户明确提供证据前就宣称"需求已验证"。
