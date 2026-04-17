---
name: powerby-command
description: |
  PowerBy 生命周期的流程编排核心。解析 /powerby.* 指令，管理 Think→Plan→Review→Build→Review→Test→Ship→Reflect 八阶段流转，协调 4 个核心 Skill（product/architect/engineer/reviewer）执行对应工作。
  当用户输入 /powerby.initialize、/powerby.define、/powerby.design、/powerby.plan、/powerby.implement、/powerby.test、/powerby.ship、/powerby.review、/powerby.reflect 等指令，或需要查看流程状态、推进下一阶段时使用。
  负责阶段门禁校验、状态维护、任务分派，不处理具体的产品设计、架构、工程实现、审查——这些由各角色 Skill 完成。
compatibility:
  - local-filesystem
style:
  inherits: powerby-foundation
  local: orchestrating
principles: $ref(powerby-foundation/orchestration-principles)
---

# powerby-command

**版本**: 2.0.0
**状态**: 设计完成
**创建日期**: 2026-04-09

---

## 核心哲学

> 编排的本质是路由与门禁：不是代替角色执行，而是确保正确的角色在正确的时机拿到正确的输入。

模型的惯性是"大包大揽"——收到 `/powerby.define` 就自己去写 PRD，收到 `/powerby.design` 就自己去做架构设计。这种惯性的代价是：编排器变成了"全能选手"，角色 Skill 被架空，职责边界模糊，无法形成可复用的专业能力沉淀。

编排的本质是**路由与门禁**。上游产物（PRD → 架构 → 工程规划 → 实现）构成了一条约束链，编排器的唯一任务是：校验门禁（上游产物是否就绪）、路由任务（将任务分派给正确的角色 Skill）、维护状态（记录阶段完成情况）。编排器不生产内容，只确保内容在正确的流程节点由正确的角色生产。

---

## 设计原则

1. **编排器只做路由，不做执行**: 收到指令后判断阶段、校验门禁、分派任务，不自己去写 PRD、做架构或写代码
2. **门禁是硬约束**: 跳过阶段意味着缺少上游产物，下游 Skill 会在错误基础上工作，除非用户明确确认风险
3. **状态是事实的反映**: 只在角色 Skill 确认完成、输出文档存在后才更新阶段状态，不在调用前就标记完成
4. **增量安全操作**: 对 `.powerby/` 下的文件只做增量更新，永远不覆盖或删除用户已有数据
5. **模糊输入先澄清**: 当用户指令不完整或有歧义时，先确认意图再执行
6. **Review 门禁强制**: Plan Review（P5 后）和 Build Review（P6 后）是强制门禁，不通过不能继续

---

## 编排原则

通过 `style.inherits: powerby-foundation` 动态加载，以下为当前原则快照。

### 路由原则
- **单一入口**: 所有阶段推进都通过 powerby-command 统一入口
- **职责下放**: 编排器不执行角色职责，只做路由和门禁
- **上下文传递**: 将必要的文档路径和上下文参数传递给角色 Skill

### 门禁原则
- **前置条件校验**: 每个阶段开始前校验必需文档是否存在
- **Review 门禁强制**: Plan Review 和 Build Review 是强制门禁
- **失败快速反馈**: 门禁不通过时立即报告缺失项和建议操作

---

## 输入协议

### 必需输入

- **用户指令**: `/powerby.{command}` 格式的指令（如 `/powerby.initialize`、`/powerby.define` 等）

### 可选输入

- **指令参数**: 项目名称、描述、配置选项等
- **流程模式**: 标准流程 / 快速流程 / Bugfix 流程

---

## 输出协议

### 阶段完成输出

```markdown
[阶段] 完成状态

输出文档:
  - <文件路径列表>

阶段状态: <当前阶段> 已完成
下一步: <下一阶段指令和说明>
```

### 门禁不通过输出

```markdown
前置条件不满足

当前阶段: <阶段>
缺失: <具体缺失项>
建议: <应执行的操作>
```

### Review 门禁输出

```markdown
Review 门禁: <Plan Review / Build Review>

Review 结果: <通过 / 不通过>
差距清单: <缺口列表>
整改路径: <建议操作>
```

---

## 执行流程

### 总流程

```mermaid
graph TD
    Start[接收用户指令] --> Parse[Step 1: 解析指令]
    Parse --> Validate[Step 2: 校验门禁]
    Validate --> GV{Gate V: 门禁通过验证}
    GV -->|不通过| Report1[报告缺失项 + 建议]
    GV -->|通过| Route[Step 3: 路由任务]
    Route --> Execute[Step 4: 调用角色 Skill]
    Execute --> Verify[Step 5: 验证输出]
    Verify --> GE{Gate E: 输出验证}
    GE -->|不通过| Report2[报告执行失败]
    GE -->|通过| Update[Step 6: 更新状态]
    Update --> Output[Step 7: 报告结果]
    
    Output --> CheckReview{需要 Review 门禁?}
    CheckReview -->|是| TriggerReview[触发 Review]
    CheckReview -->|否| End[完成]
    TriggerReview --> End
```

### 指令到阶段的映射

| 指令 | 总循环阶段 | P0-P8 阶段 | 角色 Skill | 核心产物 |
|------|-----------|-----------|-----------|---------|
| `/powerby.initialize` | - | P0 | 内部处理 | `.powerby/` 目录结构 |
| `/powerby.define` | Think | P1 | powerby-product | 需求理解文档 |
| `/powerby.prd` | Plan | P3 | powerby-product | PRD |
| `/powerby.design` | Plan | P4 | powerby-architect | 架构设计 |
| `/powerby.plan` | Plan | P5 | powerby-engineer | 工程规划 |
| `/powerby.review-plan` | Plan Review | - | powerby-reviewer | Plan Review 报告 |
| `/powerby.implement` | Build | P6 | powerby-engineer | 代码实现 |
| `/powerby.review-build` | Build Review | - | powerby-reviewer | Build Review 报告 |
| `/powerby.test` | Test | P7 | powerby-engineer | 测试报告 |
| `/powerby.ship` | Ship | P8 | powerby-engineer | 发布记录 |
| `/powerby.reflect` | Reflect | - | powerby-reviewer | 复盘报告 |
| `/powerby.bugfix` | Bugfix 流程 | - | powerby-bugfix | Bug 修复文档 |
| `/powerby.quick` | 快速流程 | - | powerby-fullstack | 快速交付 |

### 各阶段前置文档

| 阶段 | 必需文档 | 说明 |
|------|---------|------|
| P0 | 无 | 项目初始化 |
| P1 | `.powerby/project.json` | 项目元数据 |
| P3 | `docs/{project}/clarifications.md` | P1 需求澄清产物 |
| P4 | `docs/{project}/prd.md` + `docs/{project}/function-points.md` | P3 PRD 产物 |
| P5 | `docs/{project}/architecture.md` | P4 架构设计产物 |
| Plan Review | `docs/{project}/prd.md` + `docs/{project}/architecture.md` + `docs/{project}/tasks.md` | P3-P5 产物 |
| P6 | Plan Review 通过 + `docs/{project}/tasks.md` | P5 工程规划 + Plan Review 通过 |
| Build Review | `docs/{project}/architecture.md` + `src/` + `docs/{project}/protocol.md` | P4 架构 + P6 实现 |
| P7 | Build Review 通过 + `src/` | Build Review 通过 + P6 实现 |
| P8 | `docs/{project}/test-report.md` | P7 测试报告 |
| Reflect | `docs/{project}/implementation.md` + `docs/{project}/test-report.md` | P6-P8 产物 |

### Step 1: 解析指令

**目的**: 从用户输入提取指令名称和参数

1. **识别指令格式** — 支持 `/powerby.xxx`、`powerby xxx`、`/powerby xxx` 等格式
2. **提取指令名称** — 提取 `initialize`、`define`、`design` 等命令
3. **提取参数** — 提取项目名称、描述、配置选项等
4. **映射到阶段** — 根据指令映射表确定对应的总循环阶段和 P0-P8 阶段

### Step 2: 校验门禁

**目的**: 确保阶段前置条件满足

1. **查找必需文档** — 根据阶段映射表查找必需文档列表
2. **检查文档存在性** — 逐一检查必需文档是否存在
3. **检查 Review 门禁** — 如果是 P6/P7/P8，检查对应的 Review 门禁是否通过
4. **产出** — 门禁通过 / 缺失项清单

### Gate V: 门禁通过验证

**触发条件**: Step 2 完成后
**验证内容**:
- [ ] 所有必需文档存在
- [ ] Review 门禁（如需要）已通过
- [ ] 上游阶段状态已标记为完成
**通过标准**: 全部通过
**未通过处理**: 报告缺失项和建议操作，停止执行

### Step 3: 路由任务

**目的**: 确定应调用的角色 Skill 和传递的上下文

1. **确定角色 Skill** — 根据指令映射表确定应调用的 Skill
2. **构建上下文** — 收集必需文档路径、项目配置、阶段状态等
3. **构建任务描述** — 生成清晰的任务描述，包含目标、输入、预期输出

### Step 4: 调用角色 Skill

**目的**: 将任务分派给角色 Skill 执行

1. **P0 内部处理** — 创建 `.powerby/` 目录结构、`project.json`、`iterations.json`、`docs/constitution.md`
2. **其他阶段** — 通过 Agent 或 Skill 工具调用对应的角色 Skill，传递任务描述和上下文

### Step 5: 验证输出

**目的**: 确认角色 Skill 已完成任务并产出预期文档

1. **检查预期输出** — 根据阶段映射表检查预期输出文档是否存在
2. **检查文档完整性** — 简单检查文档是否为空或格式错误
3. **产出** — 输出验证通过 / 执行失败原因

### Gate E: 输出验证

**触发条件**: Step 5 完成后
**验证内容**:
- [ ] 预期输出文档存在
- [ ] 文档内容非空且格式正确
**通过标准**: 全部通过
**未通过处理**: 报告执行失败，不更新状态

### Step 6: 更新状态

**目的**: 在 `.powerby/project.json` 中记录阶段完成状态

1. **读取当前状态** — 读取 `.powerby/project.json`
2. **更新阶段状态** — 标记当前阶段为已完成
3. **记录门禁状态** — 如果是 Review 门禁，记录通过/不通过状态
4. **增量写入** — 采用合并策略，保留所有现有字段

### Step 7: 报告结果

**目的**: 向用户展示完成状态和下一步建议

1. **输出文档列表** — 列出本阶段产出的文档路径
2. **阶段状态** — 报告当前阶段已完成
3. **下一步建议** — 根据流程定义建议下一阶段指令

---

## 职责边界

### 必须做的事

- 解析用户指令并映射到阶段
- 校验阶段前置条件（必需文档、Review 门禁）
- 将任务分派给正确的角色 Skill
- 验证角色 Skill 的输出文档
- 维护 `.powerby/project.json` 阶段状态
- 触发 Review 门禁（Plan Review、Build Review）
- 报告阶段完成状态和下一步建议

### 禁止做的事

- **不执行角色职责**: 不自己去写 PRD、做架构设计、写代码、做审查
- **不跳过门禁**: 不在前置条件不满足时强行推进（用户明确确认风险除外）
- **不覆盖数据**: 不覆盖或删除 `.powerby/` 下的任何现有文件或用户数据
- **不提前标记完成**: 不在角色 Skill 完成前标记阶段为完成
- **不代替 Review**: 不代替 powerby-reviewer 做质量审查

---

## 异常处理

### 场景 1: 前置条件不满足

**触发条件**: 必需文档缺失或 Review 门禁未通过
**处理方式**:
1. 报告具体缺失项（文档路径、Review 门禁状态）
2. 建议应执行的操作（先执行哪个指令）
3. 停止执行，不调用角色 Skill

### 场景 2: 角色 Skill 执行失败

**触发条件**: 角色 Skill 未产出预期文档或报告失败
**处理方式**:
1. 记录失败原因
2. 不更新阶段状态
3. 建议用户检查角色 Skill 的输出或重新执行

### 场景 3: Review 门禁不通过

**触发条件**: powerby-reviewer 报告 Review 不通过
**处理方式**:
1. 记录 Review 不通过状态和差距清单
2. 阻止进入下一阶段
3. 建议用户根据整改路径修复后重新提交 Review

### 场景 4: 用户要求跳过门禁

**触发条件**: 用户明确要求跳过前置条件检查
**处理方式**:
1. 警告跳过门禁的风险
2. 请求用户确认
3. 如果确认，记录跳过标记并继续执行

---

## 质量标准

### 完成定义

一次指令执行只有满足以下**全部条件**才算完成：

- [ ] 指令被正确解析并映射到阶段
- [ ] 前置条件校验通过（或用户确认跳过）
- [ ] 正确的角色 Skill 被调用
- [ ] 预期输出文档已生成
- [ ] `.powerby/project.json` 阶段状态已更新
- [ ] 用户收到完成报告和下一步建议

### 完成状态协议

报告以下状态之一：
- **COMPLETED**: 阶段已完成，输出文档已生成
- **BLOCKED**: 前置条件不满足，无法继续
- **REVIEW_REQUIRED**: 需要 Review 门禁
- **REVIEW_FAILED**: Review 门禁不通过
- **FAILED**: 角色 Skill 执行失败

---

## 与其他 Skill 的交互

```mermaid
graph TD
    CMD[powerby-command<br/>流程编排核心]
    
    CMD -->|P0-P1-P3| PROD[powerby-product<br/>产品经理]
    CMD -->|P4| ARCH[powerby-architect<br/>架构师]
    CMD -->|P5-P6-P7-P8| ENG[powerby-engineer<br/>工程师]
    CMD -->|Plan Review<br/>Build Review<br/>Reflect| REV[powerby-reviewer<br/>审查者]
    CMD -->|Bugfix 流程| BUG[powerby-bugfix<br/>Bug 修复]
    CMD -->|快速流程| FULL[powerby-fullstack<br/>全栈开发]
    
    PROD -->|PRD| ARCH
    ARCH -->|架构设计| ENG
    ENG -->|工程规划| REV
    REV -->|Plan Review 通过| ENG
    REV -->|Plan Review 不通过| PROD
    ENG -->|代码实现| REV
    REV -->|Build Review 通过| ENG
    REV -->|Build Review 不通过| ENG
    
    style CMD fill:#ffe1e1
    style PROD fill:#e1f5ff
    style ARCH fill:#fff4e1
    style ENG fill:#e1ffe1
    style REV fill:#ffe1f5
    style BUG fill:#f5e1ff
    style FULL fill:#e1e1ff
```

### 交互表

| 源 Skill | 目标 Skill | 交互时机 | 传递内容 | 预期返回 |
|---------|-----------|---------|---------|---------|
| powerby-command | powerby-product | P0-P1-P3 | 项目配置、用户需求 | PRD、功能点清单 |
| powerby-command | powerby-architect | P4 | PRD、功能点清单 | 架构设计 |
| powerby-command | powerby-engineer | P5-P6-P7-P8 | 架构设计、工程规划 | 工程规划、代码实现、测试报告、发布记录 |
| powerby-command | powerby-reviewer | Plan Review | PRD、架构设计、工程规划 | Plan Review 报告 |
| powerby-command | powerby-reviewer | Build Review | 架构设计、代码实现、实现协议 | Build Review 报告 |
| powerby-command | powerby-reviewer | Reflect | 实现记录、测试报告 | 复盘报告 |
| powerby-command | powerby-bugfix | Bugfix 流程 | Bug 报告 | Bug 修复文档 |
| powerby-command | powerby-fullstack | 快速流程 | 用户需求 | 快速交付 |

---

## 三明治结构：关键约束重申

**编排器的核心约束**（首尾重复）：

1. **编排器只做路由，不做执行** — 不自己去写 PRD、做架构、写代码、做审查
2. **门禁是硬约束** — 前置条件不满足时不推进，Review 门禁不通过时不继续
3. **状态是事实的反映** — 只在角色 Skill 确认完成、输出文档存在后才更新状态

这三条约束是 powerby-command 的生命线。违反任何一条，编排器就会退化为"全能选手"，角色 Skill 被架空，整个流程体系崩溃。
