# 架构决策日志

## 决策链概览

决策 1（调度机制）→ 决策 2（上下文粒度）→ 决策 3（状态格式）→ 决策 4（回流判断位置）→ 决策 5（completion_signal 格式）

---

## 决策 1: orchestrator 调度机制

- **时间**: 2026-04-17
- **级别**: L1（战略级，影响全局架构方向）
- **上下文**: pb-v1 流程需要从用户手动驱动升级为系统自推进。需要选择 Skill 之间的自动推进机制。
- **方案分析**:
  - 方案 A: orchestrator 中心化 agent 调度——orchestrator 通过 Agent 工具调度每个 Skill，每次调度是独立 agent 会话
    - 优点：context window 可控、Gate 逻辑集中、用户可见性好、agent 独立不互相影响
    - 缺点：orchestrator 成为单点、每次调度有启动开销
    - 风险：中（单点可通过 flow-state.md 缓解）
  - 方案 B: 链式调用——Skill A 完成后直接调用 Skill B
    - 优点：实现简单
    - 缺点：context window 无限膨胀、调用链断裂风险高、Gate 逻辑分散
    - 风险：高
  - 方案 C: 分布式自推进——每个 Skill 自己判断 Gate 并输出 FLOW_SIGNAL
    - 优点：无单点
    - 缺点：Gate 逻辑分散、一致性维护成本高
    - 风险：高
- **推荐**: 方案 A
- **推荐理由**: context window 可控是硬约束（长流程会耗尽 context），Gate 逻辑集中便于维护和审计
- **决策结果**: 用户确认方案 A（CLR-ARCH-005）
- **影响**: 后续所有决策基于 orchestrator 中心化调度模式

---

## 决策 2: orchestrator 传给 agent 的上下文粒度

- **时间**: 2026-04-17
- **级别**: L2（战术级，有最佳实践）
- **上下文**: 基于决策 1，orchestrator 需要为每个 agent 构建上下文。传太多浪费 context window，传太少 agent 缺乏信息。
- **方案分析**:
  - 方案 A: 最小必需——只传目标/范围/验证方法/文档地址，agent 自行读取文档
    - 优点：context window 高效、agent 自主性高、orchestrator 不需理解每个 Skill 细节
    - 缺点：agent 需要额外读取步骤
  - 方案 B: 完整摘录——orchestrator 读取所有相关文档并摘录关键内容传入
    - 优点：agent 启动即有完整上下文
    - 缺点：浪费 context window、orchestrator 需要理解每个 Skill 的需求
- **推荐**: 方案 A
- **推荐理由**: 关键文档已落到文件系统，agent 有能力自行读取。4 项上下文足够 agent 定位所需信息。
- **决策结果**: Skill 决策，方案 A（CLR-ARCH-006）
- **影响**: dispatch_context 固定为 4 项（goal, scope, verification, doc_paths）

---

## 决策 3: 状态持久化格式

- **时间**: 2026-04-17
- **级别**: L2（战术级）
- **上下文**: 基于决策 1，orchestrator 需要持久化流程状态。现有 orchestrator 使用 flow_state.json（JSON），新设计需要选择格式。
- **方案分析**:
  - 方案 A: flow-state.md（Markdown）
    - 优点：人类可读、可直接在 IDE 中查看和编辑、与项目其他文档一致
    - 缺点：解析比 JSON 复杂
  - 方案 B: flow-state.json（JSON）
    - 优点：结构化、解析简单
    - 缺点：人类不友好、与项目文档风格不一致
- **推荐**: 方案 A
- **推荐理由**: pb-v1 体系的核心理念是"文档即契约"，状态文档应与其他产物保持一致的 Markdown 格式。Claude 模型解析 Markdown 表格的能力足够。
- **决策结果**: Skill 决策，方案 A（CLR-ARCH-008）
- **影响**: 废弃 flow_state.json，统一为 flow-state.md

---

## 决策 4: reviewer 回流判断的执行位置

- **时间**: 2026-04-17
- **级别**: L2（战术级）
- **上下文**: 基于决策 1，reviewer FAIL 后需要判断是自动回流还是交还用户。判断逻辑放在哪个组件？
- **方案分析**:
  - 方案 A: reviewer 输出建议，orchestrator 做最终判断
    - 优点：Gate 逻辑集中在 orchestrator、reviewer 职责不变（只审查不决策）
    - 缺点：orchestrator 需要理解 review issues 的语义
  - 方案 B: reviewer 直接做回流判断
    - 优点：reviewer 最了解 issues 的性质
    - 缺点：Gate 逻辑分散、reviewer 职责越界（审查 + 决策）
- **推荐**: 方案 A
- **推荐理由**: 与决策 1 一致——Gate 逻辑集中在 orchestrator。reviewer 在 completion_signal 中附加 reflow_recommendation 作为建议，orchestrator 做最终判断。这保持了 reviewer "只审查不决策"的职责边界。
- **决策结果**: Skill 决策，方案 A
- **影响**: reviewer 新增 reflow_recommendation 字段，orchestrator 新增回流判断逻辑

---

## 决策 5: completion_signal 格式

- **时间**: 2026-04-17
- **级别**: L3（实现级）
- **上下文**: 基于决策 1 和决策 2，需要定义 Skill 返回给 orchestrator 的完成信号格式。
- **方案分析**:
  - YAML 格式，嵌入 agent 返回文本中
  - 包含：skill, status, artifacts, issues(optional), assumptions(optional)
  - reviewer 额外包含：review_result + reflow_recommendation
- **决策结果**: Skill 静默决策，采用 YAML 格式
- **影响**: 4 个核心 Skill + reviewer 的输出协议需要新增 completion_signal 章节
