# Spec: PowerBy ASP (Autonomous Spec Protocol)

**版本**: v2.4.0
**基于**: proposal.md (Proposal Lock 已通过)
**宪法基准**: docs/consitution.md

> **实现载体约束 (CON-001)**：本规格中所有功能均通过 Skill 提示词文件和命令文件实现，不涉及任何代码开发。
>
> **流程隔离约束 (CON-002)**：powerby-asp 与现有 P0-P8 流程完全隔离。

---

## Epic 1: Orchestrator 编排核心

### US-001 → REQ-001
**As a** Orchestrator，**I want to** 管理五阶段状态流转，**so that** ASP 流程按正确顺序推进。

**Acceptance Criteria:**

```gherkin
Scenario: 正常阶段流转
  Given 当前状态为 DISCOVERY
  When proposal.md 已生成且用户通过 Gate 1 确认
  Then 状态转为 DRAFTING

Scenario: Drafting 到 Refining
  Given 当前状态为 DRAFTING
  When spec.md 初版生成完成
  Then 状态转为 REFINING

Scenario: Refining 通过
  Given 当前状态为 REFINING
  When Reviewer 返回 STATUS == PASS
  Then 状态转为 VISUALIZING

Scenario: Refining 循环
  Given 当前状态为 REFINING 且轮次 < 5
  When Reviewer 返回 STATUS == FAIL
  Then Product Agent 修复 spec.md 后重新进入 REFINING

Scenario: Confirmation 回退
  Given 当前状态为 CONFIRMATION
  When 用户提出修改意见
  Then 状态回退为 DRAFTING

Scenario: Visualizing 到 Confirmation
  Given 当前状态为 VISUALIZING
  When product-map.md 生成完成
  Then 状态转为 CONFIRMATION
```

### US-002 → REQ-002
**As a** Orchestrator，**I want to** 在调用 Reviewer 时仅传递规定的文件内容，**so that** 审查基于文档而非创作过程，保证客观性。

**Acceptance Criteria:**

```gherkin
Scenario: Reviewer 上下文隔离
  Given Orchestrator 进入 REFINING 阶段
  When 调用 Reviewer 角色
  Then Reviewer 的 Prompt 输入包含 spec.md、constitution.md、proposal.md
  And 包含 prd_logs/ 下所有前序审查报告（round-{N}-{reviewer}.md）
  And 不包含 Product Agent 的思考过程
  And 不包含用户对话历史

Scenario: 文件缺失
  Given Orchestrator 准备调用 Reviewer
  When spec.md 或 constitution.md 或 proposal.md 不存在
  Then 报错并提示缺失的文件名称

Scenario: 首轮审查无历史记录
  Given prd_logs/ 目录为空或不存在
  When 调用 Reviewer
  Then 正常执行审查，Previous Rounds Summary 标注为"无前序轮次"
```

### US-003 → REQ-003
**As a** Orchestrator，**I want to** 限制精炼循环次数并在超限时报警，**so that** 流程不会无限运行。

**Acceptance Criteria:**

```gherkin
Scenario: ESCALATION 触发
  Given REFINING 循环已达第 5 轮
  When Reviewer 返回 STATUS == FAIL
  Then 触发 ESCALATION
  And 输出当前 prd_logs/ 下最新审查报告摘要
  And 输出未解决的 BLOCKER/MAJOR 项清单
  And 请求用户人工介入决策
  And 终止自动流程

Scenario: 正常退出循环
  Given REFINING 循环在第 N 轮（N < 5）
  When Reviewer 返回 STATUS == PASS
  Then 退出循环，进入 VISUALIZING 阶段
```

### US-004 → REQ-004
**As a** Orchestrator，**I want to** 自动管理迭代目录下的产物文件，**so that** 所有输出存放在正确位置。

**Acceptance Criteria:**

```gherkin
Scenario: 自动创建产物文件
  Given 用户触发 /powerby-asp
  When ASP 流程完整执行
  Then docs/iterations/{id}-{name}/ 目录下包含 proposal.md、spec.md、product-map.md
  And docs/iterations/{id}-{name}/prd_logs/ 目录下包含各轮审查报告（round-{N}-{reviewer}.md）和修复记录（round-{N}-patch.md）

Scenario: 目录不存在
  Given 迭代目录尚未创建
  When ASP 流程启动
  Then 自动创建 docs/iterations/{id}-{name}/ 目录及 prd_logs/ 子目录
```

---

## Epic 2: Discovery 阶段

### US-005 → REQ-005
**As a** Product Agent，**I want to** 通过三轮递进式探究充分挖掘用户需求，**so that** proposal.md 的需求完整、边界清晰。

**Acceptance Criteria:**

```gherkin
Scenario: 第一轮——意图与价值探究
  Given 用户输入一句话需求
  When Product Agent 启动 Discovery Mode
  Then 向用户提出 3-5 个问题（覆盖目标用户、核心痛点、核心价值）
  And 等待用户回答后展示理解摘要
  And 用户确认理解无误后进入第二轮

Scenario: 第二轮——功能边界探究
  Given 第一轮理解已确认
  When Product Agent 进入第二轮
  Then 逐条列出需要的功能并请用户确认/补充/删除
  And 明确排除项及排除理由
  And 展示需求草案（需求清单 + 排除项）
  And 用户确认功能边界后进入第三轮

Scenario: 第三轮——优先级与验收标准
  Given 第二轮功能边界已确认
  When Product Agent 进入第三轮
  Then 为每条需求标注优先级（必须/应该/可选）
  And 为每条需求补充验收标准草案
  And 确认约束条件
  And 用户确认后生成 proposal.md

Scenario: 用户拒绝回答
  Given Product Agent 在任意轮次提出问题
  When 用户拒绝回答
  Then 提示用户至少完成第一轮（意图与价值）的核心问题

Scenario: 用户回答模糊
  Given Product Agent 在任意轮次收到用户回答
  When 回答内容模糊不足以推进
  Then 在当前轮次内追问（最多追问 2 次）
  And 追问后仍模糊则明确告知用户"该信息为必要项，无法跳过"
  And 要求用户提供明确回答后才能继续

Scenario: 用户要求跳过某轮
  Given Product Agent 在第二轮或第三轮
  When 用户要求跳过当前轮次
  Then 评估该轮是否包含必要信息（功能边界/优先级/验收标准）
  And 若包含必要信息则拒绝跳过，向用户说明原因并要求完成
  And 若仅包含可选信息则允许跳过，在 proposal.md 中标注"用户确认跳过"
```

### US-006 → REQ-006
**As a** Product Agent，**I want to** 生成结构化编号清单格式的 proposal.md，**so that** 用户可逐条审核每个需求项。

**Acceptance Criteria:**

```gherkin
Scenario: 结构化 Proposal 生成
  Given 三轮探究完成
  When Product Agent 生成 proposal.md
  Then 文档包含「产品定位」章节（目标用户、核心价值、成功指标）
  And 包含「需求清单」表格（ID 为 REQ-xxx、含需求描述、优先级、验收标准草案）
  And 包含「明确排除」表格（ID 为 EXC-xxx、含排除项、排除理由）
  And 包含「约束条件」表格（ID 为 CON-xxx、含约束描述）
  And 不包含"待定"、"可能"、"后续支持"等模糊词汇
```

### US-007 → REQ-007
**As a** 用户，**I want to** 逐条审核 proposal.md 的需求清单，**so that** 我能确保每条需求都准确反映我的意图。

**Acceptance Criteria:**

```gherkin
Scenario: Gate 1 逐条审核
  Given proposal.md 已生成
  When Orchestrator 展示需求清单
  Then 逐条列出所有 REQ-xxx、EXC-xxx、CON-xxx
  And 用户可对每条执行：确认 / 修改 / 删除 / 补充新需求

Scenario: 修订后重新确认
  Given 用户提出修改意见
  When Product Agent 修订 proposal.md
  Then 重新展示修订后的完整需求清单
  And 用户最终确认后 Proposal Lock 生效
```

---

## Epic 3: Drafting 阶段

### US-008 → REQ-008
**As a** Product Agent，**I want to** 将 proposal.md 转化为工程可执行的 spec.md，**so that** 规格包含完整的用户故事和验收标准。

**Acceptance Criteria:**

```gherkin
Scenario: 规格生成
  Given proposal.md 已通过 Gate 1
  When Product Agent 以 Specification Mode 运行
  Then spec.md 包含 User Stories（As a / I want / So that 格式）
  And 每个 Story 包含 Gherkin Acceptance Criteria（Given/When/Then）
  And 包含 Data Dictionary（核心名词定义）
  And 每个功能定义 Empty State、Error State、Loading State
  And 不包含技术实现细节（数据库、API、代码）
```

### US-009 → REQ-009
**As a** Product Agent，**I want to** 在每个 User Story 标题中标注对应的 REQ-xxx，**so that** 规格与提案之间有明确的追溯链。

**Acceptance Criteria:**

```gherkin
Scenario: 追溯标注
  Given spec.md 正在生成
  When 编写每个 User Story
  Then 标题格式为 "### US-xxx → REQ-xxx, REQ-yyy"
  And 每个 US 至少关联一个 REQ
  And 不存在未标注 REQ 的 User Story
```

### US-010 → REQ-010
**As a** Product Agent，**I want to** 在 spec.md 末尾附加 Traceability Matrix，**so that** 一目了然地看到所有 REQ 的覆盖情况。

**Acceptance Criteria:**

```gherkin
Scenario: 追溯矩阵生成
  Given spec.md 生成完成
  When 检查文档末尾
  Then 包含 Traceability Matrix 表格
  And 表格列出所有 proposal.md 中的 REQ-xxx
  And 每个 REQ 对应的 US 编号已填写
  And 覆盖状态标注为 "✅ 已覆盖"
```

---

## Epic 4: Refining 阶段

### US-011 → REQ-011
**As a** Reviewer Agent，**I want to** 按三维检查协议审查 spec.md，**so that** 只有高质量的规格能通过审查。

**Acceptance Criteria:**

```gherkin
Scenario: 三维审查
  Given Reviewer 接收 spec.md + constitution.md + proposal.md + prd_logs/ 历史审查记录
  When 执行审查协议
  Then 检查宪法符合性（奥卡姆剃刀、状态定义完整性、无模糊词）
  And 检查双向覆盖（正向覆盖 + 反向溢出 + 排除项入侵）
  And 检查逻辑自洽性（无死胡同、无数据孤岛）
  And 输出审查报告到 prd_logs/round-{N}-{reviewer}.md（STATUS: PASS 或 FAIL + Issues List）

Scenario: 多 AI 交替审查
  Given 审查序列为 [Claude, Codex, Claude, ...]
  When 当前轮次 Reviewer 类型为 Claude
  Then 内部自动执行审查
  When 当前轮次 Reviewer 类型为 Codex 或其他外部 AI
  Then 生成审查上下文包，用户中转至外部 AI，粘贴结果回来
```

### US-012 → REQ-012
**As a** Reviewer Agent，**I want to** 执行双向覆盖检查，**so that** spec.md 与 proposal.md 严格对齐——不多不少。

**Acceptance Criteria:**

```gherkin
Scenario: 正向覆盖检查（不能少设计）
  Given proposal.md 包含需求清单（REQ-xxx）
  When Reviewer 逐条检查
  Then 每个 REQ-xxx 在 spec.md 中有至少一个对应的 User Story
  And 遗漏任何一条标记为 BLOCKER

Scenario: 反向溢出检查（不能多设计）
  Given spec.md 包含多个 User Stories
  When Reviewer 逐条检查
  Then 每个 User Story 标注了对应的 REQ-xxx
  And 存在无 REQ 对应的 US 标记为 BLOCKER

Scenario: 排除项入侵检查
  Given proposal.md 包含 EXC-001 到 EXC-007
  When Reviewer 检查 spec.md
  Then spec.md 不包含任何 EXC-xxx 中列出的功能
  And 如有入侵标记为 BLOCKER
```

### US-013 → REQ-013
**As a** Reviewer Agent，**I want to** 在审查报告中输出 Coverage Matrix，**so that** 覆盖状态一目了然。

**Acceptance Criteria:**

```gherkin
Scenario: Coverage Matrix 输出
  Given Reviewer 完成双向覆盖检查
  When 生成审查报告（prd_logs/round-{N}-{reviewer}.md）
  Then 包含 Coverage Matrix 表格
  And 每行展示一个 REQ 或无归属 US
  And 状态标注为 ✅ Covered / ❌ Missing / ⚠️ Overflow
  And 包含 Exclusion Invasion Check 表格
  And 每个 EXC 标注是否入侵 spec.md
```

### US-014 → REQ-014
**As a** Product Agent，**I want to** 根据审查意见逐项修复 spec.md 并同步更新追溯矩阵，**so that** 修复后的规格保持追溯完整性。

**Acceptance Criteria:**

```gherkin
Scenario: 自我修正
  Given prd_logs/round-{N}-{reviewer}.md 中 STATUS == FAIL
  When Product Agent 以 Refinery Mode 运行
  Then 逐项修复 BLOCKER 和 MAJOR 项
  And 不添加任何新功能（严禁镀金）
  And 修复后同步更新 spec.md 末尾的 Traceability Matrix
  And 修复记录保存到 prd_logs/round-{N}-patch.md

Scenario: 防回归
  Given 前序轮次已修复的问题
  When Product Agent 修复当前轮次问题
  Then 不得引入与前序已修复问题相矛盾的变更
```

---

## Epic 5: Visualizing 阶段

### US-015 → REQ-015
**As a** Visualizer，**I want to** 生成 Mermaid mindmap 格式的功能全景树，**so that** 用户一眼看到完整的功能结构。

**Acceptance Criteria:**

```gherkin
Scenario: 功能全景树
  Given spec.md 已通过审查
  When Visualizer 生成 product-map.md
  Then 包含有效的 Mermaid mindmap 代码
  And Root 为产品名称
  And Level 1 为核心模块（Epics）
  And Level 2 为用户故事（Stories）
  And Level 3 为关键规则（Rules）
```

### US-016 → REQ-016
**As a** Visualizer，**I want to** 生成用户旅程流，**so that** 用户可验证核心路径和边界情况。

**Acceptance Criteria:**

```gherkin
Scenario: 用户旅程流
  Given spec.md 已通过审查
  When Visualizer 生成 product-map.md
  Then 包含 Mermaid sequenceDiagram 或 flowchart
  And 展示用户完成核心价值的最短路径
  And 标出异常分支（ESCALATION、回退、空输入等）
```

### US-017 → REQ-017
**As a** Visualizer，**I want to** 生成决策摘要，**so that** 用户快速了解做了什么、砍了什么、有什么风险。

**Acceptance Criteria:**

```gherkin
Scenario: 决策摘要
  Given spec.md + proposal.md + prd_logs/ 审查报告就绪
  When Visualizer 生成 product-map.md
  Then 包含一句话价值描述
  And 包含 MVP 裁剪报告（对比 proposal 和 spec 的差异）
  And 包含风险提示（Reviewer 曾指出的最大风险）
```

---

## Epic 6: Confirmation 阶段

### US-018 → REQ-018
**As a** 用户，**I want to** 确认最终交付物或提出修改意见，**so that** 我对最终规格有最终决定权。

**Acceptance Criteria:**

```gherkin
Scenario: Gate 2 确认通过
  Given product-map.md 已生成
  When Orchestrator 展示决策摘要和精炼过程摘要
  And 用户确认交付
  Then 流程结束，输出完成确认格式
  And 标记 Gate 2 通过

Scenario: Gate 2 回退
  Given 用户查看交付物后提出修改意见
  When Orchestrator 接收修改意见
  Then 状态回退到 DRAFTING
  And 重新进入精炼循环

Scenario: 多次回退警告
  Given 用户已回退超过 3 次
  When 用户再次提出修改
  Then 提示用户考虑重新定义 proposal
```

---

## Epic 7: Skill 基础设施

### US-019 → REQ-019
**As a** 开发者，**I want to** 定义 powerby-asp-product SKILL.md，**so that** ASP 系统有正确配置的产品经理角色。

**Acceptance Criteria:**

```gherkin
Scenario: Product SKILL.md 定义
  Given SKILL.md 遵循 Skill 规范（frontmatter: name + description）
  When 被 Orchestrator 调用
  Then 支持 Discovery Mode（三轮递进式探究）
  And 支持 Specification Mode（规格生成 + 追溯标注）
  And 支持 Refinery Mode（沉默修补 + 严禁镀金）
  And 遵循 No Implementation Details、Ambiguity is a Bug、User-Centric 三原则
```

### US-020 → REQ-020
**As a** 开发者，**I want to** 定义 powerby-asp-reviewer SKILL.md，**so that** ASP 系统有正确配置的审计程序角色。

**Acceptance Criteria:**

```gherkin
Scenario: Reviewer SKILL.md 定义
  Given SKILL.md 遵循 Skill 规范
  When 被 Orchestrator 在 Refining 阶段调用
  Then 执行三维审查协议（宪法符合性 + 双向覆盖 + 逻辑自洽性）
  And 双向覆盖检查包含正向覆盖、反向溢出、排除项入侵三项
  And 输出机器可读格式（STATUS: PASS/FAIL + Issues List + Coverage Matrix）
  And 支持 Reviewer 身份标识（Reviewer 字段）
  And 支持读取 prd_logs/ 历史审查记录
  And 输出包含 Previous Rounds Summary 和 New/Inherited 标注
```

### US-021 → REQ-021
**As a** 开发者，**I want to** 定义 powerby-asp-visualizer SKILL.md，**so that** ASP 系统能生成可视化全景图。

**Acceptance Criteria:**

```gherkin
Scenario: Visualizer SKILL.md 定义
  Given SKILL.md 遵循 Skill 规范
  When 被 Orchestrator 在 Visualizing 阶段调用
  Then 定义功能全景树生成规则（Mermaid mindmap）
  And 定义用户旅程流生成规则（Mermaid sequenceDiagram/flowchart）
  And 定义决策摘要生成规则（价值 + 裁剪 + 风险）
```

### US-022 → REQ-022
**As a** 用户，**I want to** 通过 `/powerby-asp "需求描述"` 触发全流程，**so that** 一键启动自治式规格精炼。

**Acceptance Criteria:**

```gherkin
Scenario: 命令文件定义
  Given powerby-asp.md 遵循命令文件规范（frontmatter: description + handoffs）
  When 用户输入 /powerby-asp "需求描述"
  Then 通过 handoffs 调用 powerby-asp-product Skill
  And Prompt 中包含完整五阶段编排逻辑
  And Refining 阶段通过 Prompt 指令调用 Reviewer SKILL.md
  And Visualizing 阶段通过 Prompt 指令调用 Visualizer SKILL.md

Scenario: 缺少需求描述
  Given 用户输入 /powerby-asp 但未提供需求描述
  When 命令被解析
  Then 提示用户输入一句话需求
```

### US-023 → REQ-023
**As a** 开发者，**I want to** 在 marketplace.json 中注册三个新 Skill，**so that** Claude Code 能发现并加载它们。

**Acceptance Criteria:**

```gherkin
Scenario: Skill 注册
  Given marketplace.json 存在
  When 追加三个 Skill 路径
  Then plugins[0].skills 数组包含 ./skills/powerby-asp-product
  And 包含 ./skills/powerby-asp-reviewer
  And 包含 ./skills/powerby-asp-visualizer
  And Claude Code 能扫描并加载这三个 Skill
```

---

## Epic 8: 多 AI 审查编排

### US-024 → REQ-024
**As a** 用户，**I want to** 在流程开始时配置审查序列（Reviewer 类型和顺序），**so that** 我能控制哪些 AI 参与审查以及审查顺序。

**Acceptance Criteria:**

```gherkin
Scenario: Gate 0 审查序列配置
  Given 用户触发 /powerby-asp
  When Orchestrator 启动流程
  Then 在 DISCOVERY 前展示 Gate 0 配置界面
  And 提示用户选择审查序列（如 Claude→Codex→Claude→Codex→Claude）
  And 提示用户确认最大轮次
  And 用户确认后锁定审查序列

Scenario: 默认审查序列
  Given 用户未指定审查序列
  When Gate 0 配置
  Then 默认使用 [Claude] 单轮审查

Scenario: 提前终止
  Given 审查序列未用完
  When 某轮 Reviewer 返回 STATUS == PASS
  Then 提前终止审查序列，进入 VISUALIZING
```

### US-025 → REQ-025
**As a** Orchestrator，**I want to** 支持多种 Reviewer 类型执行审查，**so that** 不同 AI 的审查视角能互补提升规格质量。

**Acceptance Criteria:**

```gherkin
Scenario: Claude 内部审查
  Given 当前轮次 Reviewer 类型为 Claude
  When Orchestrator 执行审查
  Then 内部自动切换到 Reviewer 角色
  And 按 SKILL.md 协议执行审查
  And 输出审查报告到 prd_logs/round-{N}-claude.md

Scenario: Codex 外部审查
  Given 当前轮次 Reviewer 类型为 Codex
  When Orchestrator 执行审查
  Then 生成审查上下文包（spec.md + constitution.md + proposal.md + prd_logs/ 历史 + SKILL.md 协议）
  And 提示用户将上下文包提交给 Codex
  And 等待用户粘贴 Codex 审查结果
  And 将结果保存到 prd_logs/round-{N}-codex.md
```

### US-026 → REQ-026
**As a** Orchestrator，**I want to** 将每轮审查报告独立存储在 prd_logs/ 目录，**so that** 历史记录完整可追溯，不会被覆盖。

**Acceptance Criteria:**

```gherkin
Scenario: 审查报告独立存储
  Given 第 N 轮审查完成
  When 保存审查报告
  Then 文件路径为 prd_logs/round-{N}-{reviewer}.md
  And 不覆盖任何已有文件

Scenario: 修复记录独立存储
  Given Product Agent 完成第 N 轮修复
  When 保存修复记录
  Then 文件路径为 prd_logs/round-{N}-patch.md
  And 记录修复的 Issue ID 和修复内容摘要
```

### US-027 → REQ-027
**As a** Reviewer Agent，**I want to** 读取 prd_logs/ 下所有前序审查报告，**so that** 我不会重复提出已解决的问题，并能追踪问题演变。

**Acceptance Criteria:**

```gherkin
Scenario: 历史上下文传递
  Given prd_logs/ 下存在 round-1-claude.md 和 round-1-patch.md
  When 第 2 轮 Reviewer 执行审查
  Then 读取所有前序审查报告和修复记录
  And 审查报告中包含 Previous Rounds Summary
  And Issues List 中每项标注 New/Inherited

Scenario: 已解决问题不重复
  Given 前序轮次问题 R1-001 已在 patch 中修复
  When 当前轮次 Reviewer 检查同一区域
  Then 不再将 R1-001 列为问题
  And 在 Resolved Issues 段落中确认其已修复
```

### US-028 → REQ-028
**As a** Reviewer Agent，**I want to** 每轮尽可能全面地发现所有问题，**so that** 问题总数随迭代收敛，减少总审查轮次。

**Acceptance Criteria:**

```gherkin
Scenario: 全面审查
  Given Reviewer 执行审查
  When 发现问题
  Then 不仅报告首个发现的问题，而是完整扫描所有维度
  And 审查报告中问题列表覆盖宪法符合性、双向覆盖、逻辑自洽性全部维度

Scenario: 收敛趋势
  Given 多轮审查已执行
  When 查看 prd_logs/ 下各轮报告
  Then 问题总数呈下降趋势（允许因新发现短暂上升）
```

---

## Epic 9: 交付质量保障

### US-029 → REQ-029
**As a** Orchestrator，**I want to** 在 VISUALIZING 阶段完成后对 product-map.md 进行语法校验，**so that** 交付给用户的文件不包含语法错误。

**Acceptance Criteria:**

```gherkin
Scenario: Mermaid 语法校验
  Given Visualizer 已生成 product-map.md
  When Orchestrator 执行交付前校验
  Then 逐个提取 product-map.md 中所有 mermaid 代码块
  And 对每个代码块检查：图表类型声明、节点/参与者定义、块配对（alt/else/end、loop/end）、Note over 参与者顺序、箭头语法
  And 所有代码块校验通过后才进入 CONFIRMATION 阶段

Scenario: Mermaid 语法错误
  Given product-map.md 中某个 mermaid 代码块存在语法错误
  When Orchestrator 检测到错误
  Then 定位错误所在的代码块和具体行
  And 自动修复语法错误
  And 重新校验（最多重试 3 次）
  And 3 次重试后仍有错误则向用户报告具体错误位置，由用户决定是否继续交付

Scenario: Markdown 表格结构校验
  Given product-map.md 包含 Markdown 表格
  When Orchestrator 执行交付前校验
  Then 检查每个表格是否包含表头行和分隔行
  And 检查列数是否一致
```

### US-030 → REQ-030
**As a** Orchestrator，**I want to** 在 VISUALIZING 阶段生成 function-points.md，**so that** 用户能清晰看到每条功能点及其优先级，与 proposal.md 保持 1:1 对应。

**Acceptance Criteria:**

```gherkin
Scenario: 功能点清单生成
  Given spec.md 已通过审查且 proposal.md 已锁定
  When Orchestrator 进入 VISUALIZING 阶段
  Then 生成 function-points.md 到迭代目录
  And 文件中每个功能点对应 proposal.md 中的一个 REQ-xxx
  And 功能点按优先级排序（必须 > 应该 > 可选），核心功能排在前面

Scenario: 功能点格式要求
  Given function-points.md 正在生成
  When 编写每个功能点
  Then 包含功能点编号（FP-xxx）、对应 REQ 编号、功能名称、优先级、一句话描述、验收标准摘要
  And 使用清晰的表格或列表格式，读者可快速扫描

Scenario: 1:1 对应校验
  Given function-points.md 已生成
  When 校验完整性
  Then proposal.md 中每个 REQ-xxx 在 function-points.md 中有且仅有一个对应 FP
  And 不存在无 REQ 对应的 FP（不允许溢出）
```

---

## Data Dictionary

| 术语 | 定义 |
|------|------|
| **ASP (Autonomous Spec Protocol)** | 自治式规格精炼协议，独立于 P0-P8 的全新研发流程 |
| **Orchestrator** | 编排器，以命令文件实现，协调各 Agent 角色的调用顺序和状态流转 |
| **Product Agent** | 产品经理角色，由 `powerby-asp-product/SKILL.md` 定义，具备 Discovery/Specification/Refinery 三种模式 |
| **Reviewer Agent** | 审计程序角色，由 `powerby-asp-reviewer/SKILL.md` 定义，执行对抗性审查和双向覆盖检查 |
| **Visualizer** | 可视化角色，由 `powerby-asp-visualizer/SKILL.md` 定义，生成 Mermaid 全景图 |
| **Proposal Lock (ASP Gate 1)** | 第一道质量门禁，用户逐条审核 proposal.md 需求清单后锁定 |
| **Spec Approval (ASP Gate 2)** | 第二道质量门禁，Reviewer 返回 PASS 且用户确认交付后通过 |
| **ESCALATION** | 升级报警，REFINING 循环超 5 轮时触发，请求人工介入 |
| **Gold Plating（镀金）** | 在修复阶段添加未经审查的新功能，ASP 严格禁止 |
| **Black Box Loop（黑盒循环）** | Drafting + Refining 的自动化循环，用户无需介入 |
| **Constitution（宪法）** | `docs/consitution.md`，Reviewer 审查的唯一基准 |
| **Coverage Matrix** | Reviewer 输出的覆盖矩阵，展示 REQ 与 US 的映射状态 |
| **Traceability Matrix** | spec.md 末尾的追溯矩阵，展示 REQ→US 的完整映射 |
| **Review Sequence（审查序列）** | Gate 0 中用户配置的 Reviewer 类型和顺序列表，如 [Claude, Codex, Claude, Codex, Claude] |
| **Gate 0 (Review Sequence Config)** | 第零道质量门禁，流程启动时配置审查序列，在 DISCOVERY 之前执行 |
| **prd_logs/** | 迭代目录下的审查日志子目录，存放各轮独立的审查报告和修复记录 |
| **round-{N}-{reviewer}.md** | 第 N 轮由指定 Reviewer 生成的审查报告文件 |
| **round-{N}-patch.md** | 第 N 轮 Product Agent 的修复记录文件 |
| **Previous Rounds Summary** | 审查报告中对前序轮次问题的摘要，用于追踪问题演变 |
| **STATUS** | Reviewer 报告中的状态字段，取值 `PASS` 或 `FAIL` |
| **BLOCKER** | 最高严重级别，违反宪法或范围溢出，必须修复 |
| **MAJOR** | 中等严重级别，逻辑缺陷或定义缺失，必须修复 |
| **MINOR** | 最低严重级别，建议性改进，当轮不修复 |

---

## State Definitions

### Discovery 阶段

| 状态 | 描述 |
|------|------|
| Empty State | 用户输入 `/powerby-asp` 但未提供需求描述 → 提示用户输入一句话需求 |
| Error State | constitution.md 不存在或不可读 → 报错并终止流程 |
| Loading State | Agent 正在分析需求并生成澄清问题 → 展示「正在分析您的需求...」 |

### Drafting 阶段

| 状态 | 描述 |
|------|------|
| Empty State | proposal.md 内容为空或缺少必要章节 → 报错并回退到 Discovery |
| Error State | proposal.md 信息不足以生成完整 spec → 报错并回退到 Discovery 阶段，要求补充缺失信息 |
| Loading State | Product Agent 正在转化规格 → 黑盒模式，用户无感知 |

### Refining 阶段

| 状态 | 描述 |
|------|------|
| Empty State | prd_logs/ 目录为空（首次审查前） → Reviewer 创建并写入首轮审查报告 |
| Error State | Reviewer 输出格式不符合规范（缺少 STATUS 字段） → 视为 FAIL，计入循环次数 |
| Loading State | Reviewer 审查中 / Product Agent 修复中 → 黑盒模式，用户无感知 |

### Visualizing 阶段

| 状态 | 描述 |
|------|------|
| Empty State | spec.md 通过审查但内容过于简单 → 生成最小化全景图并标注信息不足 |
| Error State | Mermaid 语法生成失败 → 降级为纯文本列表格式 |
| Loading State | Visualizer 正在生成 → 展示「正在生成可视化全景图...」 |

### Confirmation 阶段

| 状态 | 描述 |
|------|------|
| Empty State | product-map.md 生成失败 → 降级展示 spec.md 摘要 |
| Error State | 用户多次回退（超过 3 轮） → 提示重新定义 proposal |
| Loading State | 正在准备交付展示 → 展示「正在整理交付物...」 |

---

## Traceability Matrix

| Proposal REQ | Spec US | 覆盖状态 |
|-------------|---------|---------|
| REQ-001 | US-001 | ✅ 已覆盖 |
| REQ-002 | US-002 | ✅ 已覆盖 |
| REQ-003 | US-003 | ✅ 已覆盖 |
| REQ-004 | US-004 | ✅ 已覆盖 |
| REQ-005 | US-005 | ✅ 已覆盖 |
| REQ-006 | US-006 | ✅ 已覆盖 |
| REQ-007 | US-007 | ✅ 已覆盖 |
| REQ-008 | US-008 | ✅ 已覆盖 |
| REQ-009 | US-009 | ✅ 已覆盖 |
| REQ-010 | US-010 | ✅ 已覆盖 |
| REQ-011 | US-011 | ✅ 已覆盖 |
| REQ-012 | US-012 | ✅ 已覆盖 |
| REQ-013 | US-013 | ✅ 已覆盖 |
| REQ-014 | US-014 | ✅ 已覆盖 |
| REQ-015 | US-015 | ✅ 已覆盖 |
| REQ-016 | US-016 | ✅ 已覆盖 |
| REQ-017 | US-017 | ✅ 已覆盖 |
| REQ-018 | US-018 | ✅ 已覆盖 |
| REQ-019 | US-019 | ✅ 已覆盖 |
| REQ-020 | US-020 | ✅ 已覆盖 |
| REQ-021 | US-021 | ✅ 已覆盖 |
| REQ-022 | US-022 | ✅ 已覆盖 |
| REQ-023 | US-023 | ✅ 已覆盖 |
| REQ-024 | US-024 | ✅ 已覆盖 |
| REQ-025 | US-025 | ✅ 已覆盖 |
| REQ-026 | US-026 | ✅ 已覆盖 |
| REQ-027 | US-027 | ✅ 已覆盖 |
| REQ-028 | US-028 | ✅ 已覆盖 |
| REQ-029 | US-029 | ✅ 已覆盖 |
| REQ-030 | US-030 | ✅ 已覆盖 |
