# Product Panorama: PowerBy ASP (Autonomous Spec Protocol)

**版本**: v2.3.1（基于 5 轮多 AI 对抗性审查精炼）

## 1. The Big Picture

```mermaid
mindmap
  root((PowerBy ASP v2.2))
    Orchestrator 编排核心
      US-001 状态机管理
        六条转换路径 + ESCALATION
        CONFIRMATION 可回退 DRAFTING
      US-002 上下文模拟隔离
        传递 spec + constitution + proposal + prd_logs/
      US-003 循环控制
        最多5轮 PK
        超限触发 ESCALATION
      US-004 文件产物管理
        自动创建迭代目录 + prd_logs/
    Discovery 阶段
      US-005 三轮递进式探究
        第一轮：意图与价值
        第二轮：功能边界
        第三轮：优先级与验收
        零假设原则：模糊必追问，必要信息不可跳过
      US-006 结构化 Proposal
        REQ-xxx / EXC-xxx / CON-xxx
      US-007 Gate 1 逐条审核
    Drafting 阶段
      US-008 规格生成
        User Stories + Gherkin AC
        Data Dictionary + 状态定义
      US-009 追溯标注 US→REQ
      US-010 Traceability Matrix
    Refining 阶段
      US-011 三维审查
        宪法符合性 + 双向覆盖 + 逻辑自洽
      US-012 双向覆盖检查
        正向覆盖 + 反向溢出 + 排除项入侵
      US-013 Coverage Matrix
      US-014 自我修正（严禁镀金 + 防回归）
    Visualizing 阶段
      US-015 功能全景树
      US-016 用户旅程流
      US-017 决策摘要
    Confirmation 阶段
      US-018 Gate 2 确认/回退
    Skill 基础设施
      US-019 asp-product SKILL.md
      US-020 asp-reviewer SKILL.md
      US-021 asp-visualizer SKILL.md
      US-022 命令文件
      US-023 marketplace.json
    多 AI 审查编排
      US-024 Gate 0 审查序列配置
        默认 Claude 单轮 / 自定义序列
      US-025 多 Reviewer 类型
        Claude 内部自动 / Codex 自动 codex exec
      US-026 prd_logs 独立存储
        round-N-reviewer.md / round-N-patch.md
      US-027 历史上下文传递
        Previous Rounds Summary + New/Inherited
      US-028 全面审查收敛
    交付质量保障
      US-029 交付前语法校验
        Mermaid 语法检查 + Markdown 表格检查
        最多重试 3 次 + 用户降级决策
```

## 2. Core Journey

```mermaid
sequenceDiagram
    participant U as 用户
    participant O as Orchestrator
    participant P as Product Agent
    participant RC as Reviewer (Claude)
    participant RX as Reviewer (Codex)
    participant V as Visualizer

    Note over U,O: Gate 0：审查序列配置
    U->>O: /powerby-asp "一句话需求"
    O->>U: 展示审查序列配置（默认/自定义）
    U->>O: 确认序列 [Claude, Codex, Claude]

    Note over U,P: 阶段一：DISCOVERY（三轮递进式探究）
    O->>P: 启动 Discovery Mode

    alt 需求描述为空
        P-->>U: 提示输入需求（Empty State）
    else 正常输入
        Note over U,P: 第一轮：意图与价值
        P->>U: 3-5 个核心问题
        U->>P: 回答
        alt 回答模糊
            P->>U: 追问（最多2次）
            P->>U: 仍模糊→告知必要项，要求明确回答
        end
        P->>U: 展示理解摘要 → 确认

        Note over U,P: 第二轮：功能边界
        P->>U: 逐条列出功能 + 排除项
        U->>P: 确认边界

        Note over U,P: 第三轮：优先级与验收
        P->>U: 优先级标注 + 验收标准
        U->>P: 确认
    end

    P->>O: 生成结构化 proposal.md

    Note over U,O: Gate 1：逐条审核
    O->>U: 展示 REQ/EXC/CON 完整清单
    alt 用户修改
        U->>O: 修改/删除/补充
        O->>P: 修订 → 重新展示
    end
    U->>O: Proposal Lock ✓

    Note over O,RC: 阶段二+三：BLACK BOX（Drafting + Refining）
    O->>P: Specification Mode → 生成 spec.md

    loop 按审查序列执行
        alt 当前 Reviewer = Claude
            O->>RC: spec + constitution + proposal + prd_logs/
            RC->>O: prd_logs/round-N-claude.md
        else 当前 Reviewer = Codex
            O->>RX: codex exec -s read-only -o prd_logs/round-N-codex.md
            RX->>O: prd_logs/round-N-codex.md
        end

        alt STATUS == PASS
            Note over O: 退出循环
        else STATUS == FAIL 且未超限
            O->>P: Refinery Mode → 修复 BLOCKER/MAJOR
            P->>O: 更新 spec.md + prd_logs/round-N-patch.md
        else 超限
            O-->>U: ESCALATION 报警
        end
    end

    Note over O,V: 阶段四：VISUALIZING
    O->>V: spec.md + prd_logs/ + proposal.md
    V->>O: product-map.md

    Note over O: 交付前语法校验
    O->>O: 检查 Mermaid 语法 + Markdown 表格
    alt 校验通过
        Note over O: 进入 CONFIRMATION
    else 校验失败（重试最多3次）
        O->>O: 自动修复 + 重新校验
    end

    Note over U,O: 阶段五：CONFIRMATION
    O->>U: 决策摘要 + 全景图

    alt Gate 2 通过
        U->>O: 确认交付 ✓
    else 用户修改
        U->>O: 回退 DRAFTING
    end
```

## 3. What We Cut (MVP Strategy)

### In-Scope（v2.2 保留）

完整五阶段流程 + Gate 0 审查序列配置 + 多 AI 审查编排 + 交付前语法校验 + 4 个 Skill 提示词 + 1 个命令文件 + marketplace 注册，共 29 个需求项（REQ-001 ~ REQ-029）。

**v2.2 核心特性**：
- 三轮递进式探究 + 零假设原则强制执行（模糊必追问，必要信息不可跳过）
- 结构化 proposal.md（REQ/EXC/CON 编号清单）
- Gate 0 审查序列配置（用户自定义 Reviewer 类型和顺序）
- Gate 1 逐条审核
- 多 AI 交替审查（Claude 内部自动 + Codex 通过 `codex exec` 自动调用）
- prd_logs/ 独立存储（每轮审查报告和修复记录独立文件）
- 历史上下文传递（Previous Rounds Summary + New/Inherited 标注）
- 双向覆盖检查（正向覆盖 + 反向溢出 + 排除项入侵）
- US→REQ 追溯标注 + Traceability Matrix
- Drafting 信息不足时回退 Discovery（不允许带缺失项的规格产出）
- **交付前语法校验**（Mermaid + Markdown 表格，最多重试 3 次，超限用户降级决策）

### Out-of-Scope（明确砍掉）

| 被砍功能 | 砍掉理由 |
|---------|---------|
| 多 Agent 真隔离（独立会话） | 需要 Claude Code 支持独立会话管理，当前技术约束不支持 |
| constitution.md 自动生成 | 宪法文件应由用户手动维护，不属于 ASP 职责 |
| 跨迭代 Spec 关联 | 复杂度高，MVP 不需要 |
| Spec 版本对比 (diff) | 增强功能，非核心价值 |
| 自动化测试用例生成 | 属于后续实现阶段职责 |
| 与 CI/CD 集成 | 超出 ASP 流程范围 |
| 编写任何代码 | 本产品纯 Skill 提示词实现 |

### 关键权衡

- **选择了「单会话模拟隔离」而非「多 Agent 真隔离」**：务实方案，通过 Prompt 策略最大化隔离效果，接受上下文可能轻微污染的风险
- **选择了「零假设原则强制执行」而非「容忍模糊推进」**：宁可多追问用户，也不允许基于推断的信息进入 proposal.md

## 4. Risk Alerts

### v2.2 审查发现（3 轮精炼，已修复）

| 风险来源 | 描述 | 当前状态 |
|---------|------|---------|
| Round 1 (Claude) R1-001 | proposal/spec 缺少多 AI 审查相关需求，实现已超出 proposal 范围 | ✅ 已修复（补齐 REQ-024~028） |
| Round 1 (Claude) R1-002 | 上下文隔离描述过时，未包含 prd_logs/ 历史记录 | ✅ 已修复 |
| Round 1 (Claude) R1-003 | 文件产物仍引用旧的 review_log.md | ✅ 已修复（统一为 prd_logs/） |
| Round 2 (Codex) R2-001 | **零假设原则被显式破坏**：允许"基于推断继续"和"标注不确定项" | ✅ 已修复（强制追问 + 必要信息不可跳过） |
| Round 2 (Codex) R2-002 | Drafting 允许产出带缺失项的规格 | ✅ 已修复（回退 Discovery 补充信息） |
| Round 4 (Codex) R4-001 | 双向覆盖检查前提写死 REQ 范围 | ✅ 已修复（改为动态 REQ-xxx） |
| Round 4 (Codex) R4-002 | 语法校验流程可能无限循环（死胡同） | ✅ 已修复（3 次重试上限 + 用户降级决策） |

### 遗留 MINOR（不阻塞交付，后续优化）

| Issue | 描述 |
|-------|------|
| R1-007 / R2-004 | 五阶段表述未显式纳入 Gate 0（Gate 0 不算独立阶段，表述风险低） |
| R2-003 | 禁用模糊词字面量出现在规则定义示例中（机械扫描可能误报） |

### 架构性风险（持续关注）

| 风险 | 描述 |
|------|------|
| 单会话模拟隔离 | Reviewer 可能受上下文污染，通过严格 Prompt 策略缓解 |
| Token 消耗 | 多轮多 AI PK 循环消耗大量 token，MINOR 延后策略缓解 |
| Codex exec 依赖 | Codex 自动审查依赖 codex-cli 本地安装和 read-only 沙箱支持 |

## 5. Executive Summary

> **一句话价值**：用户输入一句话需求，系统自动完成「三轮递进式探究 → 结构化提案 → 规格草拟 → 多 AI 交替对抗审查 → 自我修正 → 可视化交付」全流程，产出逻辑自洽、边界清晰、不多不少的产品规格。

**实现载体**：纯 Skill 提示词（4 个 SKILL.md + 1 个命令文件），不写任何代码。

**v2.2 核心改进**（相对 v2.0）：
- 新增 **Gate 0 审查序列配置**，用户可自定义多 AI 审查顺序
- 新增 **多 AI 交替审查**（Claude 内部自动 + Codex 通过 `codex exec` 自动调用）
- 新增 **prd_logs/ 独立存储**，每轮审查报告和修复记录独立文件，完整可追溯
- 新增 **历史上下文传递**，Reviewer 读取前序审查记录，问题逐轮收敛
- 新增 **交付前语法校验**（REQ-029）：Mermaid + Markdown 表格语法检查，3 次重试上限
- 强化 **零假设原则**：模糊回答必须追问，必要信息不可跳过，Drafting 信息不足回退 Discovery

**精炼过程**：
- Round 1 (Claude): FAIL → 修复 3 BLOCKER + 3 MAJOR
- Round 2 (Codex): FAIL → 修复 1 BLOCKER + 1 MAJOR
- Round 3 (Claude): PASS
- Round 4 (Codex): FAIL → 修复 2 MAJOR（新增 REQ-029 后重新审查）
- Round 5 (Claude): **PASS** → 遗留 2 MINOR

**最大风险**：单会话模拟隔离的上下文污染 + Codex exec 依赖本地 CLI 安装。
