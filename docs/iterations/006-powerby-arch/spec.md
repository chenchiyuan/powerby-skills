# Spec: PowerBy Architecture Design (架构设计流程)

**版本**: v1.2.0
**基于**: proposal.md (Proposal Lock) + docs/consitution.md
**迭代**: 006-powerby-arch

---

## Epic 1: 架构师角色与流程编排

### US-001 → REQ-001 | 架构师角色定义

**As a** 开发者/架构师
**I want** 系统定义一个 Architect Agent，基于已交付产品文档自动产出 architecture.md
**So that** 我无需手动从零编写架构文档，系统能基于产品规格自动生成结构完整的架构设计

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: Architect Agent 读取产品文档并生成架构文档
  Given 迭代目录下存在已交付的产品文档（proposal.md、spec.md、function-points.md、product-map.md）
  And docs/consitution.md 存在
  When Architect Agent 被触发执行架构设计
  Then 在迭代目录下生成 architecture.md
  And architecture.md 包含以下章节：系统架构概览、组件划分、数据流设计、接口/协议定义
  And architecture.md 中每个架构组件可追溯到 function-points.md 中的功能点

Scenario: 产品文档缺失时拒绝设计
  Given 迭代目录下缺少 spec.md 或 function-points.md
  When Architect Agent 被触发
  Then 输出错误提示，列出缺失的文件清单
  And 拒绝进入架构设计阶段
```

**States**:
- **Empty State**: 迭代目录下无 architecture.md，提示用户触发架构设计流程
- **Error State**: 产品文档缺失或格式异常，输出具体错误信息并终止
- **Loading State**: 架构设计进行中，展示当前阶段进度

### US-002 → REQ-002 | 苏格拉底式架构澄清

**As a** 开发者/架构师
**I want** Architect 在正式设计前通过苏格拉底式提问穷尽所有架构疑问
**So that** 前期充分沟通，减少后期返工，所有架构决策有据可依

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 架构澄清正常流程
  Given Architect Agent 已读取全部产品文档和 constitution.md
  When 进入架构澄清阶段
  Then Architect 分析产品文档，识别架构层面的疑问点（选型、边界、约束、风险等）
  And 向用户提出具体的架构澄清问题
  And 等待用户回答后，判断是否仍有未解决的疑问
  And 如有疑问则继续提问，直到所有疑问澄清
  And 澄清结束后向用户展示架构方向摘要，请求确认

Scenario: 用户回答模糊时追问
  Given Architect 提出了架构澄清问题
  When 用户回答模糊或未覆盖关键信息
  Then Architect 针对模糊点进一步追问
  And 不基于假设继续设计（零假设原则）

Scenario: 无架构疑问时快速通过
  Given Architect 分析产品文档后未发现架构层面的疑问
  When 进入架构澄清阶段
  Then Architect 向用户说明无需额外澄清，展示初步架构方向
  And 用户确认后直接进入架构设计
```

**States**:
- **Empty State**: 尚未开始澄清，等待 Architect 分析产品文档
- **Error State**: 用户拒绝回答关键问题，提示至少需要回答核心架构方向问题
- **Loading State**: 澄清进行中，展示当前已澄清和待澄清的问题清单

### US-003 → REQ-008 | 用户触发的独立流程

**As a** 开发者/架构师
**I want** 产品文档交付后通过独立命令触发架构设计流程
**So that** 架构设计与产品 ASP 流程解耦，我可以在合适的时机启动架构设计

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 独立命令触发架构设计
  Given 产品 ASP 流程已完成，迭代目录下存在完整产品文档
  When 用户执行架构设计命令
  Then 系统启动架构设计流程
  And 流程不依赖产品 ASP 的会话状态
  And 流程读取迭代目录下的产品文档作为输入

Scenario: 产品文档未交付时拒绝启动
  Given 迭代目录下产品文档不完整
  When 用户执行架构设计命令
  Then 系统提示产品文档未就绪，列出缺失文件
  And 拒绝启动架构设计流程
```

**States**:
- **Empty State**: 命令未触发，等待用户执行
- **Error State**: 产品文档未就绪，输出缺失文件清单
- **Loading State**: 流程启动中，读取产品文档

---

## Epic 2: 架构审查机制

### US-014 → REQ-003 | Reviewer 上下文隔离

**As a** 开发者/架构师
**I want** Reviewer 审查时仅接收指定文件，屏蔽 Architect 思考过程
**So that** 审查结果客观可复现，不受 Architect 主观叙述影响

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: Reviewer 上下文隔离
  Given Reviewer 被触发执行架构审查
  When 构造 Reviewer 输入上下文
  Then 仅包含以下文件：
    | 文件 | 用途 |
    | docs/consitution.md | 宪法基准 |
    | 迭代目录/proposal.md | 承诺范围（含排除项） |
    | 迭代目录/function-points.md | 功能点清单（覆盖检查基准） |
    | 迭代目录/architecture.md | 审计对象 |
    | 迭代目录/arch_logs/ 下所有历史审查记录 | 前序审查上下文 |
  And 屏蔽 Architect 与用户的对话历史
  And 屏蔽 Architect 的思考过程和澄清记录
```

**States**:
- **Empty State**: Reviewer 未触发
- **Error State**: 上下文构造失败（文件缺失）
- **Loading State**: 上下文构造中

### US-004 → REQ-003 | 多轮架构审查机制

**As a** 开发者/架构师
**I want** 架构文档经过多轮 AI 审查（最多 5 轮，可配置审查序列）
**So that** 不同 AI 视角交替审查，最大化发现架构问题

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 按审查序列执行多轮审查
  Given 用户配置审查序列为 [Claude, Codex, Claude, Codex, Claude]
  And architecture.md 已生成
  When 进入架构审查阶段
  Then 第 1 轮由 Claude 执行审查
  And 每轮 Reviewer 必须读取 arch_logs/ 下所有前序审查报告，避免重复提出已解决问题
  And 审查报告存储为 arch_logs/round-{N}-{reviewer}.md（独立文件，不覆盖历史）
  And 修复记录存储为 arch_logs/round-{N}-patch.md
  And 如果 STATUS 为 FAIL，Architect 按 Refinery Mode 修复后进入下一轮
  And 依次按序列执行，直到 STATUS 为 PASS 或达到最大轮次

Scenario: 历史审查记录上下文传递
  Given 当前为第 N 轮审查（N > 1）
  And arch_logs/ 下存在前序审查报告
  When Reviewer 开始审查
  Then 必须读取所有前序 round-*.md 文件
  And 审查报告中包含 Previous Rounds Summary
  And 每个 Issue 标注 New 或 Inherited
  And 不重复提出已修复的问题（除非修复不彻底）
  And 目标是让问题总数在每轮迭代中收敛

Scenario: 审查通过提前终止
  Given 审查序列为 [Claude, Codex, Claude]
  When 第 1 轮 Claude 审查返回 STATUS: PASS
  Then 退出审查循环，进入下一阶段
  And 不执行后续轮次

Scenario: 超限触发 ESCALATION
  Given 审查序列已全部执行完毕
  And 最后一轮 STATUS 仍为 FAIL
  When 轮次计数器达到最大轮次
  Then 触发 ESCALATION
  And 输出所有审查记录摘要和未解决的 BLOCKER/MAJOR 清单
  And 请求人工介入决策
```

**States**:
- **Empty State**: 尚未开始审查，等待 architecture.md 生成
- **Error State**: ESCALATION 触发，输出未解决问题清单
- **Loading State**: 审查进行中，展示当前轮次和审查员信息

### US-005 → REQ-004 | 宪法符合性审查

**As a** 开发者/架构师
**I want** 架构审查检查是否符合 constitution.md 原则
**So that** 架构设计遵循项目的核心技术原则（SOLID、DRY、奥卡姆剃刀、演进式架构等）

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 宪法符合性检查
  Given Reviewer 读取 docs/consitution.md 和 architecture.md
  When 执行宪法符合性审查
  Then 逐条检查架构是否符合宪法中的架构原则（SOLID、DRY、奥卡姆剃刀、演进式架构）
  And 检查是否违反简单原则（是否引入非必要复杂性）
  And 检查是否遵循"组合优于继承"、"接口优于单例"、"显式优于隐式"
  And 审查报告中列出每条检查结果，引用具体宪法条款

Scenario: 违反宪法原则
  Given 架构设计中存在违反宪法原则的设计
  When Reviewer 发现违规
  Then 标记为 BLOCKER，引用具体宪法条款编号
  And STATUS 设为 FAIL
```

**States**:
- **Empty State**: 尚未执行宪法检查
- **Error State**: 发现 BLOCKER 级违规，审查不通过
- **Loading State**: 宪法符合性检查进行中

### US-006 → REQ-005 | 双向覆盖检查（架构↔产品）

**As a** 开发者/架构师
**I want** 审查时执行架构与产品文档的双向覆盖检查
**So that** 架构设计不遗漏任何功能点，也不超出产品范围

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 正向覆盖检查（不能少设计）
  Given Reviewer 读取 function-points.md 和 architecture.md
  When 执行正向覆盖检查
  Then 逐条检查 function-points.md 中每个 FP-xxx 是否在 architecture.md 中有对应架构设计
  And 遗漏任何一条标记为 BLOCKER

Scenario: 反向溢出检查（不能多设计）
  Given Reviewer 读取 function-points.md 和 architecture.md
  When 执行反向溢出检查
  Then 检查 architecture.md 中是否存在超出 function-points.md 范围的架构设计
  And 超出范围的设计标记为 BLOCKER，需用户审批后方可保留

Scenario: 排除项入侵检查
  Given Reviewer 读取 proposal.md 的排除项清单和 architecture.md
  When 执行排除项入侵检查
  Then 检查 architecture.md 中是否包含 proposal.md 明确排除（EXC-xxx）的功能架构
  And 如有入侵标记为 BLOCKER

Scenario: Coverage Matrix 输出
  Given 双向覆盖检查完成
  When 生成审查报告
  Then 报告包含 Coverage Matrix 表格
  And 表格逐条展示 FP-xxx 与架构组件的覆盖状态（✅ Covered / ❌ Missing / ⚠️ Overflow）
```

**States**:
- **Empty State**: 尚未执行覆盖检查
- **Error State**: 发现覆盖缺失或溢出，审查不通过
- **Loading State**: 覆盖检查进行中

### US-013 → REQ-003 | 架构修复流程（Refinery Mode）

**As a** 开发者/架构师
**I want** Architect 收到 FAIL 审查报告后按修复协议逐项修复 architecture.md
**So that** 修复行为有据可循，严禁镀金，修复记录可追溯

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 逐项修复 BLOCKER 和 MAJOR
  Given Reviewer 审查报告 STATUS 为 FAIL
  And 报告中包含 BLOCKER 和 MAJOR 级 Issues
  When Architect 进入 Refinery Mode
  Then 读取 arch_logs/ 下所有历史审查记录，了解完整审查脉络
  And 重点关注最新一轮审查报告中的 BLOCKER 和 MAJOR 项
  And 逐项修复 architecture.md 对应内容
  And 严禁镀金（No Gold Plating）：只修补指出的问题，不顺手添加新设计
  And 修复后同步更新架构图中的变更标注
  And 确保修复不引入已解决问题的回归

Scenario: 修复记录保存
  Given Architect 完成修复
  When 保存修复记录
  Then 修复记录存储为 arch_logs/round-{N}-patch.md
  And 记录包含：修复日期、基于哪份审查报告、每个 Issue 的修复动作
```

**States**:
- **Empty State**: 无需修复（审查 PASS）
- **Error State**: 修复引入新问题或回归，需重新审查
- **Loading State**: 修复进行中

---

## Epic 3: Skill 基础设施

### US-007 → REQ-006 | 复用现有 Skill 协议

**As a** 开发者/架构师
**I want** 架构 Skill 和审查 Skill 复用现有 powerby-asp 系列 Skill 的协议格式
**So that** 保持 Skill 生态一致性，降低学习成本

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: Skill 文件格式一致
  Given 现有 powerby-asp-reviewer/SKILL.md 的格式规范
  When 创建架构相关 Skill
  Then Skill 文件遵循 frontmatter（name + description）+ Markdown 正文格式
  And 审查输出格式与 powerby-asp-reviewer 的机器可读格式一致（STATUS、Coverage Matrix、Issues List）
  And Skill 注册到 marketplace.json
```

**States**:
- **Empty State**: Skill 文件未创建
- **Error State**: Skill 格式不符合规范，Claude Code 无法加载
- **Loading State**: Skill 创建中

### US-008 → REQ-007 | 接口/协议规范定义

**As a** 开发者/架构师
**I want** 架构文档中定义完整的接口和协议规范
**So that** 后续开发阶段有明确的契约可依，减少集成问题

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 接口/协议定义完整
  Given Architect 完成架构设计
  When 生成 architecture.md
  Then 包含接口/协议定义章节
  And 定义 API 契约（输入/输出/错误码）
  And 定义核心数据结构
  And 定义服务间通信协议（同步/异步、消息格式）
  And 不包含任何业务代码实现

Scenario: 检测到业务代码
  Given Reviewer 审查 architecture.md
  When 发现文档中包含业务代码（函数实现、SQL 语句、具体算法代码等）
  Then 标记为 BLOCKER
  And 要求移除业务代码，仅保留接口/协议定义
```

**States**:
- **Empty State**: 接口/协议章节未生成
- **Error State**: 包含业务代码，审查不通过
- **Loading State**: 接口/协议定义生成中

---

## Epic 4: 架构可视化与变更管理

### US-009 → REQ-009 | 架构可视化

**As a** 开发者/架构师
**I want** architecture.md 中包含 Mermaid 格式的架构图
**So that** 我能直观理解系统架构，快速把握全局

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 架构图生成
  Given Architect 完成架构设计
  When 生成 architecture.md
  Then 包含以下 Mermaid 架构图（至少）：
    | 图表类型 | 用途 |
    | 组件图（graph/flowchart） | 展示系统组件及其依赖关系 |
    | 数据流图（sequenceDiagram/flowchart） | 展示核心数据流转路径 |
  And 所有 Mermaid 代码块语法正确，通过校验
  And 图表清晰易读，使用中文标注

Scenario: Mermaid 语法校验
  Given architecture.md 生成完成
  When 执行语法校验
  Then 逐个提取 Mermaid 代码块
  And 检查图表类型声明、箭头语法、块配对完整性
  And 发现错误则自动修复并重新校验（最多 3 次）
```

**States**:
- **Empty State**: 架构图未生成
- **Error State**: Mermaid 语法错误，校验失败超过 3 次
- **Loading State**: 架构图生成中

### US-010 → REQ-010 | 架构变更标注

**As a** 开发者/架构师
**I want** 架构图中清晰标注新增和变更部分
**So that** 我能快速识别本次架构设计的变更点

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 新建架构（首次设计）
  Given 迭代目录下不存在历史 architecture.md
  When 生成架构图
  Then 所有组件标注为"新增"
  And 使用统一的视觉标记（如 Mermaid style 语法设置颜色）

Scenario: 架构修订（审查后修复）
  Given 架构经过审查修复
  When 更新架构图
  Then 修改的组件使用显著标记突出显示
  And 新增的组件使用不同标记区分
  And 未变更的组件保持默认样式
```

**States**:
- **Empty State**: 无历史架构，全部为新增
- **Error State**: 标注样式语法错误
- **Loading State**: 变更标注更新中

---

## Epic 5: 增强功能

### US-011 → REQ-011 | 技术选型对比流程

**As a** 开发者/架构师
**I want** 架构交付后如有技术选型对比，系统逐条列举方案供我决策，决策后重新进入架构+review 环节
**So that** 技术选型有据可依，选型结果融入最终架构

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: 存在技术选型对比
  Given 架构设计中涉及技术选型（如数据库、消息队列、框架等）
  When 架构初版交付后
  Then 系统逐条列举选型方案，每条包含：方案名称、优点、缺点、推荐理由
  And 以结构化表格呈现
  And 等待用户给出整体答复

Scenario: 用户确认选型后重新架构
  Given 用户已对所有选型方案给出答复
  When 用户确认选型决策
  Then 系统基于用户选型重新进入架构设计
  And 更新 architecture.md 中的选型相关内容
  And 重新进入审查环节

Scenario: 无技术选型对比
  Given 架构设计中不涉及技术选型
  When 架构交付后
  Then 跳过选型对比环节，直接进入最终确认
```

**States**:
- **Empty State**: 无选型对比需求
- **Error State**: 用户拒绝所有方案，需重新分析选型
- **Loading State**: 选型方案整理中

### US-012 → REQ-012 | Codex 自动化审查

**As a** 开发者/架构师
**I want** Codex 审查轮次通过 `codex exec` 自动执行
**So that** 多 AI 审查全自动化，无需我手动中转

**Acceptance Criteria (Gherkin)**:

```gherkin
Scenario: Codex 自动审查
  Given 当前轮次审查员为 Codex
  And architecture.md 已生成
  When 进入 Codex 审查轮次
  Then 系统构造 codex exec 命令：
    | 参数 | 值 |
    | -s | read-only |
    | -C | 项目根目录 |
    | -o | 迭代目录/arch_logs/round-{N}-codex.md |
  And 自动执行命令，等待完成
  And 读取输出文件，解析 STATUS
  And 输出格式与 Claude 审查一致

Scenario: Codex 执行失败
  Given codex exec 命令执行失败或输出格式异常
  When 检测到错误
  Then 生成一份错误报告文件 arch_logs/round-{N}-codex.md，STATUS 设为 FAIL
  And 错误报告中记录：错误类型、错误信息、建议的后续动作
  And 向用户报告错误信息
  And 该轮视为 FAIL，Architect 无需修复（非 spec 问题），直接进入下一轮审查
```

**States**:
- **Empty State**: Codex 轮次未到
- **Error State**: codex exec 执行失败，生成错误报告后进入下一轮
- **Loading State**: codex exec 执行中

---

## Data Dictionary

| 术语 | 定义 |
|------|------|
| Architect Agent | 架构师角色，负责基于产品文档产出架构设计 |
| architecture.md | 架构设计文档，包含系统架构、组件划分、数据流、接口/协议定义、架构图 |
| arch_logs/ | 架构审查日志目录，存放每轮审查报告（round-{N}-{reviewer}.md）和修复记录（round-{N}-patch.md） |
| round-{N}-{reviewer}.md | 第 N 轮审查报告，由指定 Reviewer 生成，包含 STATUS、Coverage Matrix、Issues List |
| round-{N}-patch.md | 第 N 轮修复记录，记录 Architect 针对审查报告的逐项修复动作 |
| Refinery Mode | 架构修复模式，Architect 收到 FAIL 审查报告后逐项修复 architecture.md，严禁镀金 |
| 苏格拉底式架构澄清 | 架构设计前的多轮提问环节，穷尽架构疑问，不限轮次，以双方达成共识为结束条件 |
| 上下文隔离 | Reviewer 审查时仅接收指定文件（architecture.md + constitution.md + function-points.md + proposal.md + arch_logs/），屏蔽 Architect 思考过程 |
| Coverage Matrix | 覆盖矩阵，展示 function-points.md 功能点与架构组件的对应关系 |
| ESCALATION | 审查超限报警，请求人工介入 |
| 审查序列 | 用户配置的 Reviewer 类型和顺序（如 [Claude, Codex, Claude]） |
| 技术选型对比 | 架构交付后列举技术方案供用户决策的环节 |
| 接口/协议规范 | API 契约、数据结构、服务间通信协议的定义（不含业务代码） |

---

## Traceability Matrix

| Proposal REQ | Spec US | 覆盖状态 |
|-------------|---------|---------|
| REQ-001 | US-001 | ✅ 已覆盖 |
| REQ-002 | US-002 | ✅ 已覆盖 |
| REQ-003 | US-004, US-013, US-014 | ✅ 已覆盖 |
| REQ-004 | US-005 | ✅ 已覆盖 |
| REQ-005 | US-006 | ✅ 已覆盖 |
| REQ-006 | US-007 | ✅ 已覆盖 |
| REQ-007 | US-008 | ✅ 已覆盖 |
| REQ-008 | US-003 | ✅ 已覆盖 |
| REQ-009 | US-009 | ✅ 已覆盖 |
| REQ-010 | US-010 | ✅ 已覆盖 |
| REQ-011 | US-011 | ✅ 已覆盖 |
| REQ-012 | US-012 | ✅ 已覆盖 |
