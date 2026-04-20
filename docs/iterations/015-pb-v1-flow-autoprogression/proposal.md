# Proposal: pb-v1 流程自推进机制

## 0. Upstream Design Input
- **来源文档**: clarifications/architecture/round-1.md（pb-v1-talk 产出，15 条已确认结论）
- **目标摘要**: 将 pb-v1 流程控制模型从"用户驱动一切"翻转为"系统驱动执行、用户驱动决策"
- **验证方式**: orchestrator 能自动调度完整流程（discovery → shipping），仅在命中 G1-G5 时交还用户
- **推荐方向**: orchestrator 中心化 agent 调度 + 5 Gate 硬判断 + 三级决策分类

## 1. 核心价值定义

pb-v1 流程执行过程中，大量"继续/下一步/再跑一次"的纯流程动作不应打断用户。本次迭代为 pb-v1 系列引入流程自推进机制，让系统自动驱动执行域的工作，仅在问题升级为决策域时交还用户。

## 2. 功能规格框架

### 2.1 模块划分

| 模块 | 职责 | 对应产物 |
|------|------|---------|
| 流程自推进协议 | 定义决策权分配规则（5 Gate + 三级分类 + Gate 映射） | pb-v1-protocol.md |
| orchestrator 升级 | 从"只读建议者"升级为"中心调度器"，负责 agent 调度、Gate 判断、状态管理、用户通知 | orchestrator/SKILL.md 重写 |
| reviewer 自动回流 | FAIL 后前置判断是否属于执行域，自动回流修复 | reviewer/SKILL.md 升级 |
| 状态持久化 | flow-state.md 全局状态 + 各 skill 状态文档 | flow-state.md 格式定义 |
| 假设记录扩展 | clarify 新增 auto_decided 分类 | clarify/SKILL.md 升级 |
| 断点恢复 | 新建 pb-v1-resume skill，扫描状态、恢复执行 | pb-v1-resume/SKILL.md |
| 核心 skill 对接 | drafting/designing/planning/implementing 对接自推进协议 | 各 SKILL.md 升级 |

### 2.2 核心用户故事

- 作为 pb-v1 用户，我想要在启动流程后系统自动推进执行域的工作，以便于我只需要在关键决策点介入，而不是每一步都手动触发
- 作为 pb-v1 用户，我想要在 reviewer FAIL 后系统自动回流修复并重新 review，以便于我不需要手动触发修复-review 循环
- 作为 pb-v1 用户，我想要在中断后能恢复到上次执行的断点继续，以便于不丢失已完成的进度
- 作为 pb-v1 用户，我想要随时能切换回手动模式，以便于在需要时拿回完全控制权

### 2.3 交互流程与规则

```
用户启动流程（默认 mode: auto）
  → orchestrator 评估当前状态
  → orchestrator 调度 agent(skill A)，传入：目标、范围、验证方法、文档地址
  → agent 执行，自行读取所需文档
  → agent 返回结果
  → orchestrator 输出状态通知给用户
  → orchestrator 评估 Gate：
    - 无命中 → AUTO_DECIDE，调度下一个 agent
    - 命中 G1-G5 → USER_GATE_REQUIRED，交还用户决策
    - 连续 3 轮失败 → ESCALATE_TO_USER
  → 循环直到流程完成或用户中断
```

**reviewer 回流规则**：
```
reviewer FAIL
  → orchestrator 前置判断：
    - issues 全部 MINOR/MAJOR 且修复路径明确 → AUTO_DECIDE，回流责任 skill
    - issues 指向上游约束问题或范围变更 → USER_GATE_REQUIRED
    - 第 3 轮 FAIL → G5 ESCALATE_TO_USER
  → 责任 skill 修复
  → 自动重新 review
```

### 2.4 范围边界

**In-Scope（本次做）**:
- pb-v1-protocol.md 协议定义
- orchestrator SKILL.md 重写（中心调度器）
- reviewer SKILL.md 升级（自动回流判断）
- flow-state.md 格式定义
- clarify SKILL.md 升级（auto_decided 分类）
- pb-v1-resume SKILL.md 新建
- drafting/designing/planning/implementing SKILL.md 升级（对接协议）

**Out-of-Scope（本次不做）**:
- 单个 skill 的内部执行逻辑改造（如 implementing 的 TDD 循环优化）
- 非 pb-v1 系列的 skill（powerby-* 系列不受影响）
- testing/shipping/discovery 的深度改造（Phase 3，后续迭代）
- 自动化测试框架（验证靠手动端到端测试）
- UI/可视化（状态通知用文本输出）

## 3. MVP 功能点清单（已确认）

📋 **协议层**
- [P0] F-001: 流程自推进协议定义——pb-v1-protocol.md，包含 5 Gate 定义、三级决策分类、Gate 判断规则、按 skill 的默认 Gate 映射、flow-state.md 格式规范
  - 去掉则：所有 skill 没有统一的决策权分配标准，Gate 判断逻辑无法一致

🎛️ **调度层**
- [P0] F-002: orchestrator 升级为中心调度器——通过 Agent 工具调度 skill、为 agent 构建最小上下文（目标/范围/验证方法/文档地址）、接收结果、判断 Gate、决定下一步
  - 去掉则：没有中心调度能力，流程无法自推进
- [P0] F-003: orchestrator 状态管理——维护 flow-state.md（阶段进度、Gate 命中记录、假设记录、Refinery 记录）、支持 mode: auto/manual 切换
  - 去掉则：无法持久化状态，断点恢复不可能
- [P0] F-004: orchestrator 状态通知——每个 agent 返回时向用户输出一行状态通知（完成/FAIL/Gate 命中）
  - 去掉则：用户对自推进过程完全不可见

🔄 **审查层**
- [P0] F-005: reviewer 自动回流判断——FAIL 后前置判断 issues 是否属于执行域，AUTO_DECIDE 则自动回流，否则 USER_GATE_REQUIRED
  - 去掉则：reviewer FAIL 仍然每次打断用户，这是当前最高频的打断点

📝 **记录层**
- [P0] F-006: clarify 新增 auto_decided 分类——AUTO_DECIDE_WITH_ASSUMPTION 的假设写入 clarifications/，含决策/理由/备选/可逆性
  - 去掉则：系统自决不可追溯，reviewer 无法审计假设

🔌 **对接层**
- [P0] F-007: 核心 skill 对接协议——drafting/designing/planning/implementing 的完成状态协议新增自推进信号输出，支持被 orchestrator 调度
  - 去掉则：orchestrator 无法调度这些 skill

🔁 **恢复层**
- [P1] F-008: pb-v1-resume skill——扫描 flow-state.md 和各 skill 状态文档、对比文件系统实际状态、确定恢复点、向用户报告并确认后继续
  - 建议推迟原因：Phase 1 可以通过 orchestrator 手动评估状态来替代，resume 是体验优化

## 4. 决策记录

### 决策点 1: orchestrator 的调度机制
- **逻辑阐述**: 这决定了整个方案的落地架构。调度机制影响 context window 管理、错误恢复、用户可见性。
- **备选方案**:
  - 方案 A: orchestrator 中心化 agent 调度——orchestrator 通过 Agent 工具调度每个 skill，每次调度是独立的 agent 会话（实现复杂度：中，context window 可控）
  - 方案 B: 链式调用——skill A 完成后直接调用 skill B（实现复杂度：低，但 context window 会无限膨胀）
  - 方案 C: 分布式自推进——每个 skill 自己判断 Gate 并输出 FLOW_SIGNAL（实现复杂度：高，Gate 逻辑分散）
- **⭐ 最终选择**: 方案 A，因为 context window 可控、Gate 逻辑集中、用户可见性好、每个 agent 独立不会互相影响

### 决策点 2: orchestrator 传给 agent 的上下文粒度
- **逻辑阐述**: 传太多浪费 context window，传太少 agent 缺乏信息。这影响每个 agent 的执行质量。
- **备选方案**:
  - 方案 A: 最小必需——只传目标/范围/验证方法/文档地址，agent 自行读取文档（实现复杂度：低，agent 自主性高）
  - 方案 B: 完整摘录——orchestrator 读取所有相关文档并摘录关键内容传入（实现复杂度：高，orchestrator 需要理解每个 skill 的需求）
- **⭐ 最终选择**: 方案 A，因为关键文档已落到文件系统，agent 有能力自行读取，且 orchestrator 不需要理解每个 skill 的细节需求

### 决策点 3: 协议文档的位置
- **逻辑阐述**: 协议需要被所有 pb-v1 skill 引用，位置影响可维护性。
- **备选方案**:
  - 方案 A: 新建 docs/pb-v1-protocol.md——独立文档，pb-v1 专用（实现复杂度：低）
  - 方案 B: 写入 skill-design-protocol.md——与通用协议合并（实现复杂度：低，但污染通用协议）
- **⭐ 最终选择**: 方案 A，因为 pb-v1 的流程控制逻辑是特有的，不应污染通用 skill 设计协议

## 5. 约束条件

### 5.1 时间约束
- 三阶段渐进实施，Phase 1 优先交付

### 5.2 资源约束
- 所有改动在 pb-v1-new 分支上进行

### 5.3 技术约束
- 调度机制依赖 Claude Code 的 Agent 工具（subagent 能力）
- 每个 agent 会话是独立的 context window
- flow-state.md 是纯 markdown 文件，不依赖外部存储

### 5.4 业务约束
- 现有 pb-v1 skill 的内部执行逻辑不变，只改流程控制层
- 向后兼容：mode: manual 时行为与当前完全一致
- orchestrator 的新红线声明必须反映"调度执行权"和"决策权在用户"的分离

## 6. 现有能力分析

### 6.1 已有功能
- orchestrator: 状态评估框架（flow_state.json 格式、产物验证、风险标注、流程类型路由）
- reviewer: Refinery 机制（3 轮上限、ESCALATED、审查报告输出到 *_logs/）
- designing: L1/L2/L3 决策分级（L1 问用户、L2 自主决策、L3 静默处理）
- implementing: 静默执行原则（约束明确时直接还原）
- clarify: source_classification（user_confirmed/model_inferred）+ 冲突检测 + clarifications/ 存储

### 6.2 复用策略
- orchestrator 的状态评估逻辑直接保留，在其上新增调度能力
- reviewer 的 Refinery 机制直接保留，新增 FAIL 后的前置判断
- designing 的 L1/L2/L3 与 G1-G5 对齐映射（L1 ≈ G1-G3，L2/L3 ≈ AUTO_DECIDE）
- clarify 的存储结构直接复用，新增 auto_decided 分类值

### 6.3 新增功能
- orchestrator 的 agent 调度能力（全新）
- orchestrator 的 Gate 判断引擎（全新）
- flow-state.md 全局状态文档（全新）
- pb-v1-protocol.md 协议文档（全新）
- pb-v1-resume skill（全新，P1）

## 7. 成功标准

1. **自推进可用**: orchestrator 能在 mode: auto 下自动调度 drafting → reviewer → designing → reviewer → planning 的完整链路，中间无用户手动触发
2. **Gate 判断准确**: 命中 G1-G5 时正确交还用户，不命中时正确自推进，零误判（不该问的问了）和零漏判（该问的没问）
3. **reviewer 回流自动化**: reviewer FAIL 后，执行域问题自动回流修复并重新 review，无需用户介入
4. **状态可恢复**: 中断后通过 flow-state.md 能准确恢复到断点
5. **向后兼容**: mode: manual 时行为与当前版本完全一致
6. **假设可追溯**: 所有 AUTO_DECIDE_WITH_ASSUMPTION 的决策都有 clarifications/ 记录

## 8. 一致性检查

- 新增的 flow-state.md 格式与现有 orchestrator 的 flow_state.json 格式对齐（markdown 版本）
- pb-v1-protocol.md 的 Gate 定义与 designing 的 L1/L2/L3 分级不冲突（映射关系明确）
- auto_decided 分类与 clarify 现有的 user_confirmed/model_inferred 共存，不破坏现有记录格式
- orchestrator 新红线声明与各原子 skill 的职责边界不冲突（orchestrator 调度执行，skill 负责具体工作）
