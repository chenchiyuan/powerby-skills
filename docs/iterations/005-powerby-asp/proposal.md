# Proposal: PowerBy ASP (Autonomous Spec Protocol)

## 1. 产品定位

- **目标用户**：极客开发者/架构师，希望通过自然语言快速启动项目，不愿在文档格式和反复 Prompt 交互中浪费时间，只关心最终的规格质量。
- **核心价值**：用户输入一句话需求，系统自动完成「三轮递进式探究 → 规格草拟（含追溯） → 双向覆盖审查 → 自我修正 → 可视化交付」全流程，产出逻辑自洽、边界清晰、可逐条审核的产品规格。
- **成功指标**：
  - 用户通过 `/powerby-asp "需求描述"` 一键触发全流程
  - 最终 spec.md 中不包含任何"待定"、"可能"等模糊词汇
  - prd_logs/ 目录中至少包含一轮 Reviewer 审查报告（round-{N}-{reviewer}.md）
  - proposal.md 中每个 REQ-xxx 在 spec.md 中有对应 User Story（正向覆盖率 100%）
  - spec.md 中每个 User Story 有对应 REQ-xxx（反向溢出率 0%）

## 2. 需求清单

| ID | 需求描述 | 优先级 | 验收标准（草案） |
|----|---------|--------|----------------|
| REQ-001 | **Orchestrator 状态机管理**：命令文件编排五阶段流转（DISCOVERY → DRAFTING → REFINING → VISUALIZING → CONFIRMATION），支持 REFINING 循环和 CONFIRMATION → DRAFTING 回退 | 必须 | 状态机覆盖所有转换路径：正常流转、循环、回退、ESCALATION |
| REQ-002 | **上下文模拟隔离**：Reviewer 审查时仅接收 spec.md + constitution.md + proposal.md + prd_logs/ 下历史审查记录，屏蔽 Product Agent 思考过程和用户对话历史 | 必须 | Reviewer 的 Prompt 输入中只包含上述文件内容 |
| REQ-003 | **循环控制与 ESCALATION**：REFINING 阶段最多 5 轮 PK，超限触发 ESCALATION 报警，输出未解决问题清单并请求人工介入 | 必须 | 第 5 轮仍 FAIL 时输出 ESCALATION 报告 |
| REQ-004 | **文件产物管理**：自动在 `docs/iterations/{id}-{name}/` 目录下创建和更新 proposal.md、spec.md、product-map.md，审查报告存放在 `prd_logs/` 子目录（round-{N}-{reviewer}.md） | 必须 | 流程结束后迭代目录包含全部产物文件，prd_logs/ 包含各轮审查报告 |
| REQ-005 | **三轮递进式探究（Discovery）**：第一轮探究意图与价值 → 第二轮探究功能边界 → 第三轮确认优先级与验收标准，每轮展示摘要并等待用户确认后再进入下一轮 | 必须 | Discovery 阶段经历三轮交互，每轮有明确的摘要确认环节 |
| REQ-006 | **结构化 Proposal 生成**：proposal.md 采用编号清单格式（REQ-xxx / EXC-xxx / CON-xxx 表格），可逐条审核 | 必须 | proposal.md 包含产品定位、需求清单、明确排除、约束条件四个结构化章节 |
| REQ-007 | **ASP Gate 1 逐条审核**：向用户展示 proposal.md 完整需求清单，用户可逐条确认/修改/删除/补充，修订后用户最终确认即 Proposal Lock | 必须 | Gate 1 展示逐条需求清单，支持用户逐条操作，修订后重新确认 |
| REQ-008 | **规格生成（Drafting）**：将 proposal.md 转化为 spec.md，包含 User Stories（As a/I want/So that）、Gherkin AC（Given/When/Then）、Data Dictionary、状态定义（Empty/Error/Loading State） | 必须 | spec.md 包含全部四类强制内容 |
| REQ-009 | **User Story 追溯标注**：spec.md 中每个 User Story 必须标注对应的 REQ-xxx，格式为 `### US-001 → REQ-001, REQ-002` | 必须 | 每个 US 标题包含 `→ REQ-xxx` 追溯标注 |
| REQ-010 | **Traceability Matrix**：spec.md 末尾附加追溯矩阵，展示 Proposal REQ 与 Spec US 的映射关系 | 必须 | spec.md 末尾包含完整的追溯矩阵表格 |
| REQ-011 | **自动化审查（Refining）**：Reviewer 按三维检查协议审查 spec.md——宪法符合性、双向覆盖检查、逻辑自洽性，支持多 AI 交替审查（每轮由不同 Reviewer 执行） | 必须 | 审查报告（prd_logs/round-{N}-{reviewer}.md）包含三维检查结果 |
| REQ-012 | **双向覆盖检查**：Reviewer 执行正向覆盖（REQ-xxx 不能少）+ 反向溢出（US 不能多）+ 排除项入侵（EXC-xxx 不能出现在 spec.md 中）三项检查 | 必须 | 审查报告包含 Coverage Matrix 和 Exclusion Invasion Check 表格 |
| REQ-013 | **Coverage Matrix 输出**：Reviewer 审查报告中包含 Coverage Matrix 表格，逐条展示 REQ 与 US 的覆盖状态（✅ Covered / ❌ Missing / ⚠️ Overflow） | 必须 | 审查报告中 Coverage Matrix 覆盖所有 REQ 和 US |
| REQ-014 | **自我修正（Refinery Mode）**：Product Agent 根据审查报告（prd_logs/round-{N}-{reviewer}.md）逐项修复 spec.md，严禁镀金（No Gold Plating），修复后同步更新 Traceability Matrix，修复记录保存到 prd_logs/round-{N}-patch.md | 必须 | 修复记录保存到 prd_logs/，spec.md 中 Traceability Matrix 同步更新 |
| REQ-015 | **功能全景树（Visualizing）**：使用 Mermaid mindmap 语法生成功能树（Root → 核心模块 → 用户故事 → 关键规则） | 必须 | product-map.md 包含有效的 Mermaid mindmap 代码 |
| REQ-016 | **用户旅程流（Visualizing）**：使用 Mermaid sequenceDiagram/flowchart 展示核心路径和异常分支 | 必须 | product-map.md 包含正常路径和异常分支的旅程图 |
| REQ-017 | **决策摘要（Visualizing）**：包含一句话价值描述、MVP 裁剪报告、风险提示 | 必须 | product-map.md 包含决策摘要三部分 |
| REQ-018 | **ASP Gate 2 确认（Confirmation）**：向用户展示决策摘要和精炼过程摘要，用户确认则流程结束，提出修改则回退到 DRAFTING | 必须 | 用户确认后输出完成确认格式，修改意见触发回退 |
| REQ-019 | **powerby-asp-product SKILL.md**：定义 Product Agent 三种模式的提示词（Discovery Mode / Specification Mode / Refinery Mode） | 必须 | SKILL.md 遵循 Skill 规范（frontmatter + Markdown），覆盖三种模式 |
| REQ-020 | **powerby-asp-reviewer SKILL.md**：定义 Reviewer Agent 的对抗性审查协议提示词，含双向覆盖检查和机器可读输出格式 | 必须 | SKILL.md 包含审查协议、双向覆盖检查、Coverage Matrix 输出格式 |
| REQ-021 | **powerby-asp-visualizer SKILL.md**：定义 Visualizer 的 Mermaid 驱动全景图生成提示词 | 必须 | SKILL.md 定义三个视图的生成规则 |
| REQ-022 | **powerby-asp.md 命令文件**：Orchestrator 编排逻辑，通过 handoffs 机制调用 Skill，Prompt 中包含完整五阶段编排流程 | 必须 | 命令文件遵循 handoffs 规范，包含五阶段编排指令 |
| REQ-023 | **marketplace.json 注册**：在 marketplace.json 中注册三个新 Skill（powerby-asp-product / powerby-asp-reviewer / powerby-asp-visualizer） | 必须 | Claude Code 能发现并加载三个新 ASP Skill |
| REQ-024 | **审查序列配置（Gate 0）**：DISCOVERY 阶段前向用户确认审查序列（Reviewer 类型和顺序，如 Claude→Codex→Claude→Codex→Claude），支持自定义最大轮次和提前终止条件 | 必须 | 流程开始时展示 Gate 0 配置界面，用户确认后锁定审查序列 |
| REQ-025 | **多 AI Reviewer 支持**：REFINING 阶段支持多种 Reviewer 类型（Claude 内部自动审查 / Codex 等外部 AI 通过用户中转），每个 Reviewer 遵循相同的 SKILL.md 审查协议 | 必须 | 不同类型 Reviewer 均输出符合规范的审查报告 |
| REQ-026 | **prd_logs 独立存储**：每轮审查报告独立存储为 `prd_logs/round-{N}-{reviewer}.md`，修复记录存储为 `prd_logs/round-{N}-patch.md`，不覆盖历史记录 | 必须 | prd_logs/ 目录包含每轮独立的审查报告和修复记录 |
| REQ-027 | **历史审查记录上下文传递**：每轮 Reviewer 审查时必须读取 prd_logs/ 下所有前序审查报告，避免重复提出已解决问题，可继承/升级/降级前序问题 | 必须 | 审查报告中包含 Previous Rounds Summary 和 New/Inherited 标注 |
| REQ-028 | **全面审查收敛要求**：每轮审查必须尽可能全面地发现所有问题，目标是每次迭代让问题总数收敛，避免"挤牙膏"式审查 | 应该 | 审查报告中包含 Resolved Issues 段落，问题总数呈收敛趋势 |
| REQ-029 | **交付文件语法校验**：VISUALIZING 阶段生成 product-map.md 后，必须对文件中的 Mermaid 代码块进行语法校验，确认无语法错误后才能进入 CONFIRMATION 阶段。校验范围包括但不限于：Mermaid 图表语法、Markdown 表格结构 | 必须 | product-map.md 中所有 Mermaid 代码块通过语法校验，无解析错误 |
| REQ-030 | **功能点清单生成（function-points.md）**：VISUALIZING 阶段生成 function-points.md，逐条列出 proposal.md 中每个 REQ-xxx 对应的功能点。按优先级排序（核心功能在前），格式清晰易读，与 proposal.md 保持 1:1 对应关系 | 必须 | function-points.md 中每个功能点对应一个 REQ-xxx，按优先级排序，核心功能排在前面 |

## 3. 明确排除

| ID | 排除项 | 排除理由 |
|----|--------|---------|
| EXC-001 | 多 Agent 真隔离（独立会话） | 需要 Claude Code 支持独立会话管理，当前技术约束不支持 |
| EXC-002 | constitution.md 自动生成 | 宪法文件应由用户手动维护，不属于 ASP 职责 |
| EXC-003 | 跨迭代 Spec 关联 | 复杂度高，MVP 不需要 |
| EXC-004 | Spec 版本对比 (diff) | 增强功能，非核心价值 |
| EXC-005 | 自动化测试用例生成 | 属于后续实现阶段职责 |
| EXC-006 | 与 CI/CD 集成 | 超出 ASP 流程范围 |
| EXC-007 | 编写任何代码 | 本产品纯 Skill 提示词实现，不涉及代码开发 |

## 4. 约束条件

| ID | 约束描述 |
|----|---------|
| CON-001 | **实现载体约束**：所有功能通过 Skill 提示词文件（SKILL.md）和命令文件（.claude/commands/*.md）实现，不写任何代码 |
| CON-002 | **流程隔离约束**：powerby-asp 是全新独立流程，与现有 P0-P8 流程完全隔离，禁止混淆命名、阶段、角色、产物、门禁 |
| CON-003 | **上下文隔离约束**：单会话模拟隔离（通过 Prompt 策略），非物理隔离，接受轻微上下文污染风险 |
| CON-004 | **宪法依赖约束**：Reviewer 审查基准为 `docs/consitution.md`，该文件必须预先存在 |
| CON-005 | **迭代目录约束**：所有产物存放在 `docs/iterations/{id}-{name}/` 目录，沿用现有迭代管理结构 |
