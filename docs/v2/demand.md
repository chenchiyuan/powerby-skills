产品需求文档 (PRD): PowerBy Autonomous Spec Protocol (ASP)
版本: v1.0 状态: Draft 对应阶段: P1 (Definition)
1. 产品综述 (Overview)
1.1 核心价值 (Core Value)
本产品旨在构建一个 “自治式规格精炼工厂” (Autonomous Spec Refinery)。 它通过引入一个 Orchestrator (编排器) 来接管 P1（需求定义）阶段，协调 Product Agent（产品经理）与 Reviewer Agent（审查员）进行对抗性协作。用户只需提供初始意图和最终确认，中间的“提问-草拟-审查-修正”循环由 AI 自治完成。
引用原则:
• 零假设原则 (Zero-Assumption Principle): 系统不假设用户一开始就提供了完美需求，必须通过苏格拉底式提问来挖掘。
• MVP 优先原则: 自动化流程的目标是产出最小可行性规格，而非大而全的文档。
1.2 用户画像 (User Persona)
• 极客开发者/架构师: 希望通过自然语言快速启动项目，不愿意在文档格式和反复的 Prompt 交互中浪费时间，只关心最终的规格质量。
--------------------------------------------------------------------------------
2. 用户故事 (User Stories)
ID
角色
行为 (Action)
目的/价值 (Value)
优先级
US-001
用户
输入 /powerby.auto_product "我想做一个..."
触发全自动需求分析流程。
P0
US-002
Product Agent
向用户发起苏格拉底式提问
澄清模糊意图，确立 MVP 边界（参考 Superpowers/Brainstorming）。
P0
US-003
Orchestrator
协调 Product 和 Reviewer 进行多轮 PK
在用户无感知的情况下（黑盒）提升文档质量。
P0
US-004
Reviewer Agent
基于 constitution.md 拒绝不合格的 Spec
确保产出物符合“宪法”和设计原则（参考 Spec-Kit/Constitution）。
P0
US-005
Visualizer
生成产品全景图 (Mermaid)
让用户一眼看懂复杂的规格结构。
P1
--------------------------------------------------------------------------------
3. 功能需求与逻辑流程 (Functional Requirements)
3.1 核心模块：The Orchestrator (流程编排器)
定义: 一个控制脚本或高级指令，用于管理 Agent 间的上下文隔离与消息传递。
• FR-001 (状态机管理):
    ◦ 必须维护以下状态：DISCOVERY (探究) -> DRAFTING (草拟) -> REFINING (精炼/循环) -> VISUALIZING (可视化) -> CONFIRMATION (确认)。
• FR-002 (上下文隔离):
    ◦ 关键逻辑: 在 Reviewer 介入时，Orchestrator 必须提供一个干净的上下文（Clean Context），只包含 spec.md 和 constitution.md，屏蔽 Product Agent 的思考过程。
3.2 阶段一：交互式探究 (Discovery Phase)
执行角色: powerby-product
• FR-003 (苏格拉底式提问):
    ◦ Agent 不得直接生成文档。
    ◦ 输入: 用户的一句话需求。
    ◦ 处理: 检查 constitution.md，识别模糊点（如用户未定义“受众”）。
    ◦ 输出: 3-5 个澄清问题。
    ◦ 结束条件: 获取到足够生成 proposal.md (Why & What) 的信息。
3.3 阶段二：黑盒精炼循环 (The Black Box Loop)
执行角色: powerby-product (Actor) vs powerby-reviewer (Critic)
• FR-004 (规格生成):
    ◦ Product Agent 将 proposal.md 转化为 spec.md。
    ◦ 约束: 必须包含 User Stories 和 Acceptance Criteria (Gherkin格式)。
• FR-005 (自动化审查):
    ◦ Reviewer Agent 读取 spec.md。
    ◦ 依据: docs/constitution.md 和 powerby-reviewer 的审查清单（一致性、完整性、模糊性）。
    ◦ 输出: review_log.md，包含 STATUS: PASS/FAIL 和 ISSUES list。
• FR-006 (自我修正):
    ◦ 如果 STATUS == FAIL，Orchestrator 将 review_log.md 传回给 Product Agent。
    ◦ Product Agent 必须根据 Review 意见修改 spec.md，并记录修改点。
    ◦ 循环限制: 最大循环次数设为 5次。若超过 5 次仍未 PASS，触发 [ESCALATION] 报警，请求人工介入。
3.4 阶段三：全景交付 (Delivery Phase)
执行角色: powerby-visualizer (新角色)
• FR-007 (全景图生成):
    ◦ 读取最终锁定的 spec.md。
    ◦ 生成 product-map.md，必须包含 Mermaid 格式的：
        ▪ Mindmap (功能树)
        ▪ User Flow (核心路径)
--------------------------------------------------------------------------------
4. 数据结构与文件契约 (Data & File Contracts)
遵循 OpenSpec 的文件目录结构，确保每个 artifact 都有明确的定义。
.powerby/
  ├── memory/
  │   └── constitution.md       # [Input] 项目最高原则
  └── specs/
      └── {feature_name}/
          ├── proposal.md       # [Artifact] 阶段一产物：意图与范围
          ├── spec.md           # [Artifact] 阶段二产物：详细规格 (不断迭代)
          ├── review_log.md     # [Log] 阶段二产物：审查记录与PK历史
          └── product-map.md    # [Artifact] 阶段三产物：可视化交付物
--------------------------------------------------------------------------------
5. 验收标准 (Acceptance Criteria)
5.1 流程验收
• [ ] AC-01: 用户输入模糊需求时，系统拒绝直接生成 Spec，而是通过提问澄清。
• [ ] AC-02: 在 specs/ 目录下能找到 review_log.md，其中至少包含一轮 Reviewer 指出的问题和 Product Agent 的修复记录（证明黑盒循环已生效）。
• [ ] AC-03: 最终生成的 spec.md 中不包含任何“待定”、“可能”等模糊词汇（符合 constitution 的清晰性原则）。
5.2 质量门禁 (Quality Gates)
引用: 参考 powerby-skills 的 Gate 1 和 Gate 2 定义。
• Gate 1 (Proposal Lock): 用户必须显式确认 proposal.md 中的 Core Value。
• Gate 2 (Spec Approval): Reviewer Agent 必须返回 STATUS: APPROVED，且无 Critical 级别的阻断项。
--------------------------------------------------------------------------------
6. 附录：关键 Prompt 策略 (Prompt Strategy)
为了实现自动化，Orchestrator 需向 Agent 发送特定的 System Prompt：
• 致 Reviewer: "你是一个冷酷的审计程序。你的目标不是通过文档，而是找出违反 constitution.md 的证据。不要为了礼貌而妥协。如果你发现了逻辑漏洞，必须标记为 BLOCKER。"
• 致 Product: "收到审查意见。现在的任务是Code Patching而非创作。请精确地只修改被指出的问题，不要引入新的未经审查的功能（防止镀金蔓延）。"
