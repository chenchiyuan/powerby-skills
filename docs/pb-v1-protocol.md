# pb-v1 协议

**版本**: 1.2.0
**状态**: 设计中
**创建日期**: 2026-04-17
**适用范围**: pb-v1 全系列 Skill
**上游依据**: clarifications/architecture/round-1.md, docs/powerby-vnext-total-flow.md

---

## 一、pb-v1 是什么

pb-v1 是一套基于原子 Skill 组合的软件交付体系。它将软件开发生命周期拆解为职责单一的原子 Skill，通过文档契约串联，以"约束逐层还原"为核心思想驱动整个流程。

**一句话定义**: 用户定义目标和边界，系统通过原子 Skill 链逐层还原为可交付的软件。

---

## 二、设计思想

### 2.1 约束逐层还原

pb-v1 的核心信念：**执行是约束还原的过程。**

每个阶段接收上游产物作为硬约束，将其还原为本层产物。"还原"意味着不创造、不脑补、不越界——上游没写的不做，上游写了的必须做。

```
用户想法 → 需求合同 → 功能规格 → 技术架构 → 工程任务 → 代码实现 → 验证通过 → 交付发布
```

每一次转化都是一次约束还原。reviewer 的职责是验证还原是否忠实——本轮产物是否对齐还原了上轮产物。

### 2.2 原子 Skill 组合

每个 Skill 只做一件事，职责边界由红线声明硬性约束。Skill 之间不直接调用，通过文档契约衔接——上游 Skill 的输出文档是下游 Skill 的输入文档。

这意味着：
- 任何 Skill 可以被独立替换，只要它遵守输入/输出契约
- 流程可以从任意节点开始，只要前置产物存在
- Skill 不需要知道"下一步是谁"，只需要交付自己的产物

### 2.3 文档即契约

pb-v1 中的文档不是附属品，是系统运行的核心机制：
- **proposal.md** 是需求合同——下游所有 Skill 都以它为约束源头
- **feature-specs/*.md** 是功能规格——每个维度条目可直接转化为测试用例
- **architecture.md** 是技术契约——实现必须忠实还原架构定义
- **flow-state.md** 是流程状态——断点恢复和调度决策的唯一依据

文档写入即承诺。写入 proposal.md 的每句话，下游都会当作硬约束执行。

### 2.4 执行权与决策权分离

用户拥有决策权：目标、边界、取舍——做不做、做到哪、接受哪个代价。

系统拥有执行权：还原、实现、修复、复审——怎么做。

只有当执行域的问题升级为决策域的问题时，系统才交还用户。"怎么做"默认系统决定，"做不做 / 做到哪 / 接受哪个代价"默认用户决定。

此外，在关键阶段边界（PRD → 架构、架构 → 工程、工程 → 实现），系统通过 Phase Checkpoint 无条件交还用户确认，确保用户在每次重大方向转换前拥有审批权。

---

## 三、流程全景

### 3.1 六阶段框架

pb-v1 采用 Think → Plan → Build → Test → Ship → Reflect 六阶段框架：

| 阶段 | 核心职责 | 关键产物 |
|------|---------|---------|
| Think | 探讨与开创——挑战前提、探索可能性、收敛需求 | proposal.md |
| Plan | 规划与约束——将需求转化为可执行规格 | feature-specs/, architecture.md, tasks.md |
| Build | 实现与还原——基于规格还原为代码 | 代码实现 |
| Test | 测试与质量——验证实现是否满足规格 | 测试报告 |
| Ship | 交付与发布——将代码交付到目标环境 | 发布记录、变更日志 |
| Reflect | 复盘与改进——提取经验、沉淀到全局经验库 | 复盘报告 |

### 3.2 主线 Skill 链路

```
Think:    discovery
             ↓
Plan:     drafting → reviewer(PRD) → 【PC1: 用户确认产品范围】
             ↓
          designing → reviewer(架构) → 【PC2: 用户确认技术方案】
             ↓
          planning → reviewer(工程) → 【PC3: 用户确认任务计划】
             ↓
Build:    implementing → reviewer(实现)
             ↓
Test:     testing
             ↓
Ship:     shipping
             ↓
Reflect:  retrospective
```

reviewer 是贯穿 Plan 和 Build 阶段的质量门禁。每次阶段性产物交付后，reviewer 验证本轮产物是否对齐还原了上轮产物。PASS 则推进，FAIL 则回流修复。

【PC】是贯穿 Plan 阶段的里程碑确认点。reviewer PASS 后，系统无条件交还用户确认产物方向，用户批准后才进入下一阶段。

### 3.3 产物链路

```
用户想法
  → proposal.md (discovery)
    → feature-spec-index.md + feature-specs/*.md (drafting)
      → [reviewer: PRD 对齐需求？] → 【PC1: 用户确认产品范围】
        → architecture.md (designing)
          → [reviewer: 架构对齐 PRD？] → 【PC2: 用户确认技术方案】
            → tasks.md (planning)
              → [reviewer: 工程对齐架构？] → 【PC3: 用户确认任务计划】
                → 代码实现 (implementing)
                  → [reviewer: 实现对齐架构？]
                    → 测试报告 (testing)
                      → 发布记录 (shipping)
                        → 复盘报告 (retrospective)
```

每个箭头是一次约束还原。每个 `[reviewer]` 是一次对齐验证。每个 `【PC】` 是一次用户里程碑确认。

### 3.4 流程类型

| 流程类型 | 适用场景 | 阶段范围 | 说明 |
|---------|---------|---------|------|
| standard | 完整功能开发 | Think → Reflect 全流程 | 默认流程 |
| quick | 小需求/增量开发（≤3 天） | 简化的 Plan → Ship | 跳过深度 discovery |
| bugfix | Bug 诊断与修复 | 独立流程 | 从诊断开始，不走完整 Plan |

---

## 四、Skill 角色定义

### 4.1 主线 Skill

主线 Skill 构成流程的骨干链路，每个 Skill 在链路中有固定位置。

| Skill | 阶段 | 单一职责 | 输入 | 输出 |
|-------|------|---------|------|------|
| discovery | Think | 需求收敛——将模糊想法转化为边界清晰的需求合同 | 用户想法 / design-brief.md | proposal.md |
| drafting | Plan | 规格拆解——将需求合同转化为原子功能规格卡 | proposal.md | feature-spec-index.md, feature-specs/*.md（D-01~D-08, D-17~D-20） |
| designing | Plan | 架构收敛——将功能规格转化为技术架构 | feature-specs/*.md | architecture.md, feature-specs/*.md（补充 D-09~D-16） |
| planning | Plan | 约束传递——将架构约束分解为任务粒度的验收标准 | architecture.md | tasks.md |
| implementing | Build | 约束还原——将任务计划还原为代码 | tasks.md, architecture.md | 代码实现 |
| testing | Test | 质量验证——验证实现是否满足上游约束 | 代码实现, feature-specs/*.md | 测试报告 |
| shipping | Ship | 交付执行——执行发布流程 | 测试通过的代码 | 发布记录、变更日志 |
| retrospective | Reflect | 数据结晶——从执行数据中提取经验 | 全流程数据 | 复盘报告 |

### 4.2 门禁 Skill

| Skill | 职责 | 触发时机 |
|-------|------|---------|
| reviewer | 对齐还原验证——验证本轮产物是否忠实还原了上轮产物 | 每个 Plan/Build 阶段产物交付后 |

reviewer 支持 4 种审查类型：
- PRD 审查：feature-specs 是否对齐还原 proposal.md
- 架构审查：architecture.md 是否对齐还原 feature-specs
- 工程审查：tasks.md 是否对齐还原 architecture.md
- 实现审查：代码是否对齐还原 architecture.md

判定规则：PASS = 无 BLOCKER 且无 MAJOR。FAIL 则回流责任 Skill 修复，最多 3 轮（Refinery 机制）。

### 4.3 编排 Skill

| Skill | 职责 |
|-------|------|
| orchestrator | 中心调度器——评估流程状态、调度 Skill 执行、判断 Gate、管理状态、通知用户 |

orchestrator 是整个流程的驱动核心。它通过 Agent 工具调度每个 Skill，为 agent 构建最小上下文（目标、范围、验证方法、文档地址），接收结果后判断是自推进还是交还用户。

### 4.4 工具 Skill

| Skill | 职责 | 可被调用的阶段 |
|-------|------|-------------|
| clarify | 统一澄清——结构化澄清、持久化记录、冲突检测 | 全阶段 |

clarify 不是流程节点，是被其他 Skill 在需要澄清时调用的工具。澄清记录存储在 clarifications/ 目录，格式统一，支持三种来源分类：user_confirmed、model_inferred、auto_decided。

### 4.5 独立 Skill

独立 Skill 不在主线链路中，按需独立使用。

| Skill | 职责 | 使用场景 |
|-------|------|---------|
| office-hours | 对话式收敛——将模糊想法收敛为 design-brief.md | 用户还在探讨阶段，尚未进入正式需求 |
| talk | 通用讨论——基于事实上下文的顾问式讨论 | 任意阶段，不限主题的讨论与收敛 |
| demo | 产品定义视觉还原——在编码前交付可评审的页面 Demo | 编码前对齐页面理解 |
| preview | 迭代预览——产出可运行的高保真 MVP 预览应用 | 研发开始前的全局预览 |
| ascii | ASCII 布局草图——用 ASCII art 还原页面布局结构 | 编码前最低成本对齐布局 |
| brower | 浏览器评审——连接浏览器执行页面级验证 | 页面级事实采集与验证 |
| frontend | 前端界面设计——将需求还原为高质量前端代码 | 需要独立的前端设计与实现 |
| spec-verify | Spec 逐维度验证——逐张 spec 卡片验证实现完备性 | 验证每张 spec 是否被完整实现 |

---

## 五、执行模型

### 5.1 自推进模式（默认）

流程默认以 `mode: auto` 运行。orchestrator 自动调度 Skill 链路，用户只在命中 Gate 或 Phase Checkpoint 时介入。

```
用户启动流程
  → orchestrator 评估当前状态
  → orchestrator 调度 agent(skill)
    传入：目标、范围、验证方法、文档地址
  → agent 独立执行（独立 context window）
  → agent 返回结果
  → orchestrator 输出状态通知
  → orchestrator 判断 PC / Gate
    ├─ 命中 PC → 交还用户确认里程碑产物
    ├─ 命中 G1-G5 → 交还用户决策
    ├─ 无命中 → 调度下一个 skill
    └─ 连续 3 轮失败 → 升级给用户
  → 循环直到流程完成或用户中断
```

### 5.2 手动模式

用户声明 `mode: manual` 后，每个 Skill 完成后回到用户手动触发。orchestrator 退化为状态评估和建议角色。

切换方式：
- 即时中断：用户在任意时刻发送消息即可中断自推进
- 模式声明：用户声明 mode: manual 或 mode: auto

### 5.3 五个硬 Gate

Gate 是系统必须交还用户的硬判断点：

| Gate | 名称 | 触发条件 |
|------|------|---------|
| G1 | 范围/目标变更 | 会改变产品范围、成功标准、非目标定义 |
| G2 | 外部合同变更 | 会改变用户可见行为、接口契约、交付承诺 |
| G3 | 取舍属于 owner | 多个可行方案都合理，系统无法推出唯一最优 |
| G4 | 外部授权 | 需要安装软件、申请网络、第三方配置等 |
| G5 | 循环未收敛 | 同一问题簇连续 3 次修复-验证后仍失败 |

**判断原则：按影响判断，不按主题判断。** 问题属于"如何还原既有约束"→ 系统自推进；问题升级为"如何定义/修改约束"→ 交给用户。

### 5.4 三级决策分类

| 级别 | 行为 | 适用场景 |
|------|------|---------|
| AUTO_DECIDE | 系统直接执行，不记录 | 阶段推进、回流修复、实现细节、纯流程动作 |
| AUTO_DECIDE_WITH_ASSUMPTION | 系统执行，记录假设到 clarifications/ | 可逆、局部影响、不改外部合同、上游未明确但可强推荐 |
| USER_GATE_REQUIRED | 系统停止，交还用户 | 命中 G1-G5 |
| PHASE_CHECKPOINT | 系统停止，交还用户确认里程碑产物 | reviewer PASS 且 review_type 在 checkpoint_map 中 |

### 5.5 Phase Checkpoint（阶段确认点）

Phase Checkpoint（PC）是系统在关键阶段边界无条件交还用户的里程碑确认点。与 Gate 的区别：Gate 是问题驱动的条件触发（出了问题才停），PC 是里程碑驱动的无条件触发（到了边界必须停）。

| PC | 触发时机 | 确认内容 | 通过后进入 | 反馈回流到 |
|----|---------|---------|-----------|-----------|
| PC1 | `reviewer[prd_review]` PASS 后 | 产品范围与边界 | designing | drafting |
| PC2 | `reviewer[arch_review]` PASS 后 | 架构/技术方案 | planning | designing |
| PC3 | `reviewer[plan_review]` PASS 后 | 任务规划 | implementing | planning |

**用户行为**：
- 批准（`approved`）→ 自动推进到下一个 Skill
- 提出修改意见 → 回流到对应 Skill 迭代，迭代完成后重新走 reviewer → PC

**判断优先级**：orchestrator 在 reviewer PASS 时先检查 checkpoint_map（无条件），再检查 gate_candidate（条件）。PC 拦截优先于 Gate 评估。

**与流程类型的关系**：checkpoint_map 按 review_type 匹配。没有对应 reviewer 的流程类型自然不触发对应 PC（如 quick 流程无 prd_review/arch_review，PC1/PC2 不触发，PC3 正常触发）。

### 5.6 Reviewer 回流规则

reviewer FAIL 是最高频的流程中断点。自推进模式下，orchestrator 对 FAIL 做前置判断：

- issues 全部 MINOR/MAJOR 且修复路径明确 → AUTO_DECIDE，自动回流责任 Skill 修复，重新 review
- issues 指向上游约束问题或范围变更 → USER_GATE_REQUIRED
- 连续 3 轮 FAIL 同一类问题 → G5 升级给用户

### 5.7 按 Skill 的默认 Gate 映射

| Skill | 高频 Gate | 说明 |
|-------|----------|------|
| discovery | G1, G2 | 需求发现容易触发范围变更和外部合同定义 |
| drafting | G1, G2 | PRD 起草涉及功能边界和用户可见行为 |
| designing | G2, G3 | 架构设计涉及接口契约和技术取舍 |
| planning | G3 | 任务拆解涉及优先级取舍 |
| implementing | G4, G5 | 实现可能需要外部环境，循环修复可能不收敛 |
| testing | G5 | 测试验证可能暴露循环不收敛 |
| shipping | G4 | 发布始终需要外部授权 |

---

## 六、状态管理

### 6.1 flow-state.md

每个迭代目录下维护 `flow-state.md`，作为全局状态的唯一持久化文档。orchestrator 是全局状态的唯一写入者。

内容包含：
- **基本信息**: 流程类型、当前模式、启动时间
- **阶段进度表**: 每个 Skill 的状态（待执行/进行中/完成/FAIL/Gate 命中）
- **Phase Checkpoint 记录**: PC 确认的时间、状态、用户反馈
- **Gate 命中记录**: 时间、Gate 类型、Skill、问题、用户决策
- **假设记录**: AUTO_DECIDE_WITH_ASSUMPTION 的决策追溯
- **Refinery 记录**: reviewer 回流修复的轮次和结果

### 6.2 状态通知

orchestrator 在每个 agent 返回时向用户输出状态通知：

| 场景 | 通知格式 |
|------|---------|
| 正常推进 | `✅ {skill} 完成 → 自动推进到 {next_skill}` |
| reviewer PASS | `✅ reviewer({type}) PASS → 自动推进到 {next_skill}` |
| reviewer PASS + PC | `🔵 reviewer({type}) PASS → PC{n}: 等待确认{确认内容}` |
| PC 通过 | `✅ PC{n} 确认通过 → 自动推进到 {next_skill}` |
| PC 回流 | `🔄 PC{n} 用户反馈 → 回流 {skill} 迭代` |
| reviewer FAIL + 自动回流 | `🔄 reviewer({type}) FAIL（{n} 个问题，均可自动修复）→ 回流 {skill}` |
| Gate 命中 | `⛔ Gate {G1-G5}: {问题描述}` |
| 流程完成 | `🏁 流程完成` |

### 6.3 断点恢复

中断后通过 flow-state.md 恢复：
- 扫描 flow-state.md 和文件系统实际状态
- 对比确定恢复点
- 向用户报告恢复状态并确认后继续（中断期间用户可能手动修改了产物）

---

## 七、Unified Handoff Protocol（统一交还协议）

### 7.1 设计原则

**Skill 只报告，Orchestrator 决策。**

每个主线 Skill 执行完后，统一交还 orchestrator。Skill 不需要知道流程拓扑、不需要知道"下一步是谁"，只管做好自己的事并报告结果。所有路由逻辑、流程拓扑、异常处理集中在 orchestrator 一处。

```
任意 Skill 执行完
  → 写 signal 文件（持久化）
  → 调用 /pb-v1-orchestrator
    → orchestrator 读取 signal，评估结果
      ├─ 正常完成，无阻塞 → Agent 调度下一个 Skill（独立 context）
      ├─ 有需要用户决策的问题 → 批量呈现给用户，等待决策后继续
      └─ reviewer FAIL → 判断 reflow(自动修复) 还是 yield(交用户)
```

### 7.2 completion_signal（统一格式）

所有主线 Skill 必须输出的结构化信号：

```yaml
completion_signal:
  skill: string                    # 当前 Skill 名称
  status: enum [completed, failed, blocked]
  artifacts:                       # 产出文件
    - path: string
      type: string
  issues: optional                 # 发现的问题
    - id: string
      description: string
      severity: enum [BLOCKER, MAJOR, MINOR]
      points_to_upstream: boolean  # 问题根因是否指向上游产物
      gate_candidate: optional enum [G1, G2, G3, G4, G5]
  assumptions: optional            # 做出的假设
    - clr_id: string
      summary: string
  review_result: optional          # 仅 reviewer 填写
    status: enum [PASS, FAIL, ESCALATED]
    review_type: string
    round: integer
    blocker_count: integer
    major_count: integer
    minor_count: integer
```

关键约定：
- `issues` 中每个 issue 统一要求 `points_to_upstream` 字段（所有 Skill，不仅是 reviewer）
- 回流判断由 orchestrator 基于 issues 做出，Skill 不自行判断回流目标

### 7.3 signal 文件

每个 Skill 执行完写入持久化 signal 文件，用于 orchestrator 读取和断点恢复：

```
docs/iterations/{iteration_id}/signals/{skill_name}.yaml
```

reviewer 按审查类型区分：`reviewer-prd.yaml`、`reviewer-arch.yaml`、`reviewer-plan.yaml`、`reviewer-impl.yaml`。

文件内容 = completion_signal 的 YAML 序列化 + 时间戳。

### 7.4 Final Step: Handoff（Skill 侧统一模板）

替换每个主线 Skill 当前各不相同的"交付与引导"步骤。所有 Skill 的最后一步完全相同：

```markdown
### Final Step: Handoff

**目的**: 报告执行结果，交还 orchestrator 决策下一步

**执行内容**:

1. **构建 completion_signal**
   按本 Skill 的执行结果填充 completion_signal：
   - status: 根据执行情况填 completed / failed / blocked
   - artifacts: 列出本次产出的文件路径
   - issues: 如有问题，逐条填写（含 severity 和 points_to_upstream）
   - review_result: 仅 reviewer 填写

2. **写入 signal 文件**
   将 completion_signal 写入 `docs/iterations/{iteration_id}/signals/{skill_name}.yaml`

3. **输出状态摘要**（一行，给用户）
   - completed: `✅ {skill_name} 完成，产出: {artifact_list}`
   - failed: `❌ {skill_name} 失败: {reason}`
   - blocked: `⚠️ {skill_name} 受阻: {reason}`

4. **调用 orchestrator**
   通过 Skill 工具调用 `/pb-v1-orchestrator`
```

### 7.5 Orchestrator 决策逻辑

orchestrator 被调用后的处理流程：

```
读取最新 signal 文件 → 更新 flow-state.md → 评估 signal:

1. status == completed 且无 issues 且非 reviewer
   → 按流程序列确定 next_skill
   → Agent 调度 next_skill（独立 context）
   → 输出: ✅ {skill} 完成 → 自动推进到 {next_skill}

2. status == completed 且 review_result 存在
   2a. review_result.status == PASS
     → 检查 checkpoint_map: review_type 是否需要 PC？
       YES → yield PC 确认给用户
             → 用户批准 → 按 review_next_map 确定 next_skill → Agent 调度
             → 用户反馈 → 按 checkpoint_reflow_map 确定 reflow_skill → Agent 调度（附带用户反馈）
             → 输出: 🔵 reviewer({type}) PASS → PC{n}: 等待确认{确认内容}
       NO  → 按 review_next_map 确定 next_skill
             → Agent 调度 next_skill
             → 输出: ✅ reviewer({type}) PASS → 自动推进到 {next_skill}
   
   2b. review_result.status == FAIL
     → 检查 issues:
       - 全部 points_to_upstream == false 且无 BLOCKER
         → 按 reflow_map 确定 responsible_skill
         → Agent 调度 responsible_skill（Refinery 模式，附带 issues）
         → 输出: 🔄 reviewer({type}) FAIL → 回流 {skill} 修复 {n} 个问题
       - 有 points_to_upstream == true 或有 BLOCKER
         → 构建决策请求，交还用户
         → 输出: ⛔ reviewer({type}) FAIL，需要你的决策（{n} 个决策点）
   
   2c. review_result.status == ESCALATED
     → 构建决策请求，交还用户
     → 输出: ⛔ 审查连续 3 轮未通过，需要你的决策

3. status == completed 且有 issues（非 reviewer）
   → 检查 issues 中是否有 gate_candidate
     - 有 → 构建决策请求，交还用户
     - 无 → 按流程序列继续（issues 作为 context 传给下一个 Skill）

4. status == failed
   → 检查重试次数（从 flow-state.md 读取）
     - < 3 次 → 重试当前 Skill
     - ≥ 3 次 → 构建决策请求，交还用户

5. status == blocked
   → 构建决策请求，交还用户
```

**用户决策后的恢复**：用户做出决策后调用 `/pb-v1-orchestrator`，orchestrator 读取用户决策，将决策注入 dispatch_context，Agent 调度目标 Skill 继续。

**决策呈现格式**（交还用户时）：

```markdown
## 需要你的决策

### 决策 1: {title}
**背景**: {前因后果，包括哪个 Skill 产出了什么，为什么走到这一步}
**方案 A**: {描述}（推荐，理由: {reason}）
**方案 B**: {描述}
**不决策的影响**: {impact}

### 决策 2: ...

请选择后告诉我，我会继续推进流程。
```

**Phase Checkpoint 确认格式**（reviewer PASS + PC 命中时）：

```markdown
## 阶段确认: PC{n} — {确认内容}

**已完成的工作**: {哪个 Skill 产出了什么，reviewer 审查结果摘要}

**关键产物**: {产物文件路径列表}

**需要你确认**:
- {产物核心要点 1}
- {产物核心要点 2}
- {产物核心要点 3}

请回复 `approved` 继续推进，或提出修改意见，我会回流迭代。
```

### 7.6 流程序列表

orchestrator 维护的路由表，集中管理流程拓扑。改流程顺序只需改此表，不需要动任何 Skill。

```yaml
flow_sequences:
  standard:
    - discovery
    - drafting
    - reviewer[prd_review]
    - designing
    - reviewer[arch_review]
    - planning
    - reviewer[plan_review]
    - implementing
    - reviewer[impl_review]
    - testing
    - shipping
    - retrospective
  
  quick:
    - discovery
    - drafting
    - designing
    - planning
    - reviewer[plan_review]
    - implementing
    - reviewer[impl_review]
    - testing
    - shipping
  
  bugfix:
    - discovery
    - planning
    - reviewer[plan_review]
    - implementing
    - reviewer[impl_review]
    - testing
    - shipping

review_next_map:
  prd_review: designing
  arch_review: planning
  plan_review: implementing
  impl_review: testing

reflow_map:
  prd_review: drafting
  arch_review: designing
  plan_review: planning
  impl_review: implementing

checkpoint_map:
  prd_review: PC1
  arch_review: PC2
  plan_review: PC3

checkpoint_reflow_map:
  PC1: drafting
  PC2: designing
  PC3: planning
```

---

## 八、实施路线

协议描述的是目标态。落地分三个阶段渐进实施：

| 阶段 | 内容 | 状态 |
|------|------|------|
| Phase 1 | 协议定义（Unified Handoff Protocol）+ completion_signal 统一格式 + signal 文件规范 | 已完成 |
| Phase 2 | 8 个主线 Skill 统一 Final Step: Handoff + reviewer 补 points_to_upstream + discovery/testing/shipping 补 dispatch_context | 进行中 |
| Phase 3 | orchestrator 重构（signal 读取 → 决策逻辑 → Agent 调度 + 流程序列表 + yield 决策呈现 + 断点恢复） | 待启动 |

---

## 附录：术语表

| 术语 | 定义 |
|------|------|
| 约束还原 | 接收上游产物作为硬约束，将其转化为本层产物，不创造、不脑补、不越界 |
| 对齐验证 | reviewer 验证本轮产物是否忠实还原了上轮产物 |
| Gate | 系统必须交还用户决策的硬判断点，问题驱动，条件触发 |
| Phase Checkpoint (PC) | 系统在关键阶段边界无条件交还用户的里程碑确认点，里程碑驱动，无条件触发 |
| Refinery | reviewer FAIL 后回流修复并重新审查的循环机制，最多 3 轮 |
| 主线 Skill | 构成流程骨干链路的 Skill，有固定的上下游关系 |
| 独立 Skill | 不在主线链路中，按需独立使用的 Skill |
| flow-state.md | 迭代级全局状态文档，断点恢复和调度决策的唯一依据 |
| signal 文件 | Skill 执行完写入的持久化 completion_signal，路径 `signals/{skill_name}.yaml` |
| Handoff | Skill 执行完后统一交还 orchestrator 的动作 |
| yield | orchestrator 将需要用户决策的问题批量呈现给用户 |
| reflow | orchestrator 将 reviewer FAIL 的问题回流给上游 Skill 修复 |

## 附录：变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 1.0.0 | 2026-04-17 | 初始版本，基于 CLR-ARCH-001~015 和 vNext 框架统一定义 |
| 1.1.0 | 2026-04-20 | 新增 Unified Handoff Protocol（§7）：统一交还协议、completion_signal 格式、signal 文件规范、Final Step 模板、orchestrator 决策逻辑、流程序列表 |
| 1.2.0 | 2026-04-20 | 新增 Phase Checkpoint（§5.5）：三个里程碑确认点（PC1-PC3）、PHASE_CHECKPOINT 决策级别、checkpoint_map/checkpoint_reflow_map、PC 确认呈现格式、更新流程图和产物链路 |
