# 功能点清单: PowerBy ASP (Autonomous Spec Protocol)

**迭代**: 005-powerby-asp
**版本**: v2.4.0
**基于**: proposal.md (Proposal Lock) + spec.md v2.4.0 (5 轮审查通过)

> 按优先级排序：核心（必须）功能在前，增强（应该）功能在后。每个功能点与 proposal.md 中的 REQ 保持 1:1 对应。

---

## 功能点总览

| FP | REQ | 功能名称 | 优先级 | 模块 |
|----|-----|---------|--------|------|
| FP-001 | REQ-001 | 状态机管理 | 必须 | Orchestrator |
| FP-002 | REQ-002 | 上下文模拟隔离 | 必须 | Orchestrator |
| FP-003 | REQ-003 | 循环控制与 ESCALATION | 必须 | Orchestrator |
| FP-004 | REQ-004 | 文件产物管理 | 必须 | Orchestrator |
| FP-005 | REQ-005 | 三轮递进式探究 | 必须 | Discovery |
| FP-006 | REQ-006 | 结构化 Proposal 生成 | 必须 | Discovery |
| FP-007 | REQ-007 | Gate 1 逐条审核 | 必须 | Discovery |
| FP-008 | REQ-008 | 规格生成 | 必须 | Drafting |
| FP-009 | REQ-009 | User Story 追溯标注 | 必须 | Drafting |
| FP-010 | REQ-010 | Traceability Matrix | 必须 | Drafting |
| FP-011 | REQ-011 | 三维自动化审查 | 必须 | Refining |
| FP-012 | REQ-012 | 双向覆盖检查 | 必须 | Refining |
| FP-013 | REQ-013 | Coverage Matrix 输出 | 必须 | Refining |
| FP-014 | REQ-014 | 自我修正（Refinery Mode） | 必须 | Refining |
| FP-015 | REQ-015 | 功能全景树 | 必须 | Visualizing |
| FP-016 | REQ-016 | 用户旅程流 | 必须 | Visualizing |
| FP-017 | REQ-017 | 决策摘要 | 必须 | Visualizing |
| FP-018 | REQ-018 | Gate 2 确认 | 必须 | Confirmation |
| FP-019 | REQ-019 | Product Agent SKILL.md | 必须 | Skill 基础设施 |
| FP-020 | REQ-020 | Reviewer Agent SKILL.md | 必须 | Skill 基础设施 |
| FP-021 | REQ-021 | Visualizer SKILL.md | 必须 | Skill 基础设施 |
| FP-022 | REQ-022 | 命令文件 powerby-asp.md | 必须 | Skill 基础设施 |
| FP-023 | REQ-023 | marketplace.json 注册 | 必须 | Skill 基础设施 |
| FP-024 | REQ-024 | Gate 0 审查序列配置 | 必须 | 多 AI 审查 |
| FP-025 | REQ-025 | 多 Reviewer 类型支持 | 必须 | 多 AI 审查 |
| FP-026 | REQ-026 | prd_logs 独立存储 | 必须 | 多 AI 审查 |
| FP-027 | REQ-027 | 历史审查记录上下文传递 | 必须 | 多 AI 审查 |
| FP-029 | REQ-029 | 交付文件语法校验 | 必须 | 交付质量 |
| FP-030 | REQ-030 | 功能点清单生成 | 必须 | 交付质量 |
| FP-028 | REQ-028 | 全面审查收敛要求 | 应该 | 多 AI 审查 |

**统计**: 必须 29 个 / 应该 1 个 / 共 30 个功能点

---

## 核心功能详情

### Orchestrator 编排核心

**FP-001 → REQ-001 | 状态机管理 | 必须**
管理五阶段状态流转（DISCOVERY → DRAFTING → REFINING → VISUALIZING → CONFIRMATION），支持 REFINING 循环、CONFIRMATION → DRAFTING 回退、超限 ESCALATION。
> 验收：覆盖所有转换路径——正常流转、循环、回退、ESCALATION

**FP-002 → REQ-002 | 上下文模拟隔离 | 必须**
Reviewer 审查时仅接收 spec.md + constitution.md + proposal.md + prd_logs/ 历史审查记录，屏蔽 Product Agent 思考过程和用户对话历史。
> 验收：Reviewer Prompt 输入中只包含上述文件内容

**FP-003 → REQ-003 | 循环控制与 ESCALATION | 必须**
REFINING 阶段最多 5 轮 PK，超限触发 ESCALATION 报警，输出未解决问题清单并请求人工介入。
> 验收：第 5 轮仍 FAIL 时输出 ESCALATION 报告

**FP-004 → REQ-004 | 文件产物管理 | 必须**
自动在 `docs/iterations/{id}-{name}/` 目录下创建和更新所有产物文件，审查报告存放在 `prd_logs/` 子目录。
> 验收：流程结束后迭代目录包含全部产物文件

### Discovery 阶段

**FP-005 → REQ-005 | 三轮递进式探究 | 必须**
第一轮探究意图与价值 → 第二轮探究功能边界 → 第三轮确认优先级与验收标准。每轮展示摘要并等待用户确认。零假设原则：模糊必追问，必要信息不可跳过。
> 验收：经历三轮交互，每轮有明确的摘要确认环节

**FP-006 → REQ-006 | 结构化 Proposal 生成 | 必须**
proposal.md 采用编号清单格式（REQ-xxx / EXC-xxx / CON-xxx 表格），可逐条审核。
> 验收：包含产品定位、需求清单、明确排除、约束条件四个结构化章节

**FP-007 → REQ-007 | Gate 1 逐条审核 | 必须**
向用户展示 proposal.md 完整需求清单，用户可逐条确认/修改/删除/补充，修订后最终确认即 Proposal Lock。
> 验收：支持用户逐条操作，修订后重新确认

### Drafting 阶段

**FP-008 → REQ-008 | 规格生成 | 必须**
将 proposal.md 转化为 spec.md，包含 User Stories、Gherkin AC、Data Dictionary、状态定义。信息不足时回退 Discovery。
> 验收：spec.md 包含全部四类强制内容，不含技术实现细节

**FP-009 → REQ-009 | User Story 追溯标注 | 必须**
spec.md 中每个 User Story 标注对应的 REQ-xxx，格式为 `### US-001 → REQ-001`。
> 验收：每个 US 标题包含 `→ REQ-xxx` 追溯标注

**FP-010 → REQ-010 | Traceability Matrix | 必须**
spec.md 末尾附加追溯矩阵，展示 Proposal REQ 与 Spec US 的映射关系。
> 验收：包含完整的追溯矩阵表格

### Refining 阶段

**FP-011 → REQ-011 | 三维自动化审查 | 必须**
Reviewer 按三维检查协议审查——宪法符合性、双向覆盖检查、逻辑自洽性，支持多 AI 交替审查。
> 验收：审查报告包含三维检查结果

**FP-012 → REQ-012 | 双向覆盖检查 | 必须**
正向覆盖（REQ 不能少）+ 反向溢出（US 不能多）+ 排除项入侵（EXC 不能出现在 spec 中）。
> 验收：审查报告包含 Coverage Matrix 和 Exclusion Invasion Check

**FP-013 → REQ-013 | Coverage Matrix 输出 | 必须**
审查报告中包含 Coverage Matrix 表格，逐条展示覆盖状态（✅ Covered / ❌ Missing / ⚠️ Overflow）。
> 验收：Coverage Matrix 覆盖所有 REQ 和 US

**FP-014 → REQ-014 | 自我修正（Refinery Mode） | 必须**
根据审查报告逐项修复 BLOCKER 和 MAJOR，严禁镀金，修复后同步更新 Traceability Matrix，防止回归。
> 验收：修复记录保存到 prd_logs/，追溯矩阵同步更新

### Visualizing 阶段

**FP-015 → REQ-015 | 功能全景树 | 必须**
使用 Mermaid mindmap 生成功能树（Root → 核心模块 → 用户故事 → 关键规则）。
> 验收：product-map.md 包含有效的 Mermaid mindmap 代码

**FP-016 → REQ-016 | 用户旅程流 | 必须**
使用 Mermaid sequenceDiagram/flowchart 展示核心路径和异常分支。
> 验收：包含正常路径和异常分支的旅程图

**FP-017 → REQ-017 | 决策摘要 | 必须**
包含一句话价值描述、MVP 裁剪报告、风险提示。
> 验收：product-map.md 包含决策摘要三部分

### Confirmation 阶段

**FP-018 → REQ-018 | Gate 2 确认 | 必须**
向用户展示决策摘要和精炼过程摘要，用户确认则流程结束，提出修改则回退 DRAFTING。
> 验收：用户确认后输出完成确认格式，修改意见触发回退

### Skill 基础设施

**FP-019 → REQ-019 | Product Agent SKILL.md | 必须**
定义 Product Agent 三种模式的提示词（Discovery / Specification / Refinery Mode）。
> 验收：SKILL.md 遵循 Skill 规范，覆盖三种模式

**FP-020 → REQ-020 | Reviewer Agent SKILL.md | 必须**
定义 Reviewer 的对抗性审查协议，含双向覆盖检查和机器可读输出格式。
> 验收：包含审查协议、Coverage Matrix 输出格式

**FP-021 → REQ-021 | Visualizer SKILL.md | 必须**
定义 Visualizer 的 Mermaid 驱动全景图生成规则。
> 验收：定义三个视图的生成规则

**FP-022 → REQ-022 | 命令文件 powerby-asp.md | 必须**
Orchestrator 编排逻辑，通过 handoffs 调用 Skill，包含完整五阶段编排流程。
> 验收：命令文件遵循 handoffs 规范

**FP-023 → REQ-023 | marketplace.json 注册 | 必须**
在 marketplace.json 中注册所有 ASP Skill。
> 验收：Claude Code 能发现并加载 ASP Skill

### 多 AI 审查编排

**FP-024 → REQ-024 | Gate 0 审查序列配置 | 必须**
DISCOVERY 前向用户确认审查序列（Reviewer 类型和顺序），支持自定义和默认序列。
> 验收：流程开始时展示配置界面，用户确认后锁定

**FP-025 → REQ-025 | 多 Reviewer 类型支持 | 必须**
支持 Claude 内部自动审查 + Codex 通过 `codex exec` 自动调用 + 其他外部 AI 用户中转。
> 验收：不同类型 Reviewer 均输出符合规范的审查报告

**FP-026 → REQ-026 | prd_logs 独立存储 | 必须**
每轮审查报告独立存储为 `round-{N}-{reviewer}.md`，修复记录为 `round-{N}-patch.md`。
> 验收：prd_logs/ 包含每轮独立文件，不覆盖历史

**FP-027 → REQ-027 | 历史审查记录上下文传递 | 必须**
每轮 Reviewer 读取 prd_logs/ 下所有前序报告，避免重复提出已解决问题。
> 验收：报告包含 Previous Rounds Summary 和 New/Inherited 标注

### 交付质量保障

**FP-029 → REQ-029 | 交付文件语法校验 | 必须**
VISUALIZING 后对 product-map.md 执行 Mermaid 语法 + Markdown 表格校验，最多重试 3 次。
> 验收：所有 Mermaid 代码块通过校验，无解析错误

**FP-030 → REQ-030 | 功能点清单生成 | 必须**
生成 function-points.md，逐条列出 proposal.md 中每个 REQ 对应的功能点，按优先级排序。
> 验收：与 proposal.md 保持 1:1 对应，核心功能排在前面

### 增强功能

**FP-028 → REQ-028 | 全面审查收敛要求 | 应该**
每轮审查尽可能全面发现所有问题，目标是每次迭代让问题总数收敛。
> 验收：报告包含 Resolved Issues 段落，问题总数呈收敛趋势
