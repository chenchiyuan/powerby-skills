# Spec: ASP 迭代编号体系

## User Stories

### US-001 → REQ-001
**As a** 开发者
**I want** 执行 `/powerby-asp` 时自动从 `iterations.json` 读取最大编号并递增创建新迭代目录
**So that** 每次 ASP 迭代都有唯一的递增编号，文档顺序清晰可追溯

**Acceptance Criteria:**

```gherkin
Scenario: 首次启动 ASP 流程创建新迭代
  Given iterations.json 中最大编号为 006
  And 用户执行 /powerby-asp "我想做一个任务管理系统"
  When ASP Orchestrator 读取 iterations.json
  Then 新迭代编号为 007
  And 创建目录 docs/iterations/007-task-manager/
  And 在目录下创建 prd_logs/ 子目录
  And iterations.json 新增一条记录，id 为 "007"，status 为 "in_progress"

Scenario: iterations.json 不存在时自动初始化
  Given .powerby/iterations.json 不存在
  And 用户执行 /powerby-asp
  When ASP Orchestrator 尝试读取 iterations.json
  Then 创建 .powerby/iterations.json，初始化为空列表
  And 新迭代编号为 001

Scenario: 编号与 P0-P8 流程共享序号空间
  Given iterations.json 中有 P0-P8 流程创建的迭代 005
  And docs/iterations/ 下存在 006-powerby-arch/ 目录（未在 json 中记录）
  When ASP Orchestrator 计算新编号
  Then 同时扫描 iterations.json 和 docs/iterations/ 目录
  And 取两者最大编号 +1 作为新编号

Scenario: iterations.json 与目录编号不一致时的冲突解决
  Given iterations.json 中最大编号为 005
  And docs/iterations/ 下存在 008-some-feature/ 目录（手动创建，未在 json 中记录）
  When ASP Orchestrator 计算新编号
  Then 以 max(iterations.json 最大编号, docs/iterations/ 目录最大编号) + 1 为准
  And 新迭代编号为 009
  And 不修改已有的 iterations.json 记录（不自动补录无关迭代）
```

### US-002 → REQ-002
**As a** 开发者
**I want** 在启动 `/powerby-asp` 时能指定继续已有的迭代
**So that** 我可以在中断后恢复之前的 ASP 流程，而不是每次都新建

**Acceptance Criteria:**

```gherkin
Scenario: 用户指定继续已有迭代
  Given 存在迭代目录 docs/iterations/007-task-manager/
  And 用户执行 /powerby-asp 并指定继续迭代 007
  When ASP Orchestrator 处理请求
  Then 不创建新目录
  And 使用 docs/iterations/007-task-manager/ 作为工作目录
  And 按以下规则判断恢复阶段：
    | 目录下已有文件 | 恢复到阶段 |
    | 无任何 ASP 文件 | DISCOVERY（从头开始） |
    | 仅 proposal.md | DRAFTING（生成 spec.md） |
    | proposal.md + spec.md | REFINING（进入审查循环） |
    | proposal.md + spec.md + product-map.md + function-points.md | CONFIRMATION（用户确认） |

Scenario: 用户指定的迭代不存在
  Given 不存在编号为 099 的迭代目录
  And 用户指定继续迭代 099
  When ASP Orchestrator 处理请求
  Then 提示用户该迭代不存在
  And 询问是否创建新迭代

Scenario: 迭代目录存在但 iterations.json 中无记录
  Given 存在迭代目录 docs/iterations/006-powerby-arch/
  And iterations.json 中无编号 006 的记录
  And 用户指定继续迭代 006
  When ASP Orchestrator 处理请求
  Then 自动在 iterations.json 中补录该迭代记录
  And 使用该目录作为工作目录
```

### US-003 → REQ-003
**As a** 开发者
**I want** `/powerby-asp-arch` 启动时要求我指定已有迭代目录
**So that** 架构文档和产品文档在同一目录下，保持关联性

**Acceptance Criteria:**

```gherkin
Scenario: 指定已有迭代且产品交付物完整
  Given 存在迭代目录 docs/iterations/007-task-manager/
  And 目录下存在 proposal.md、spec.md、function-points.md
  And 用户执行 /powerby-asp-arch 并指定迭代 007
  When ASP Architecture Orchestrator 检查前置条件
  Then 使用该目录作为工作目录
  And 在目录下创建 arch_logs/ 子目录
  And 正常进入架构设计流程

Scenario: 指定已有迭代但产品交付物缺失
  Given 存在迭代目录 docs/iterations/007-task-manager/
  And 目录下缺少 spec.md
  When ASP Architecture Orchestrator 检查前置条件
  Then 提示用户缺少 spec.md
  And 建议先完成 /powerby-asp 产品流程
  And 终止流程

Scenario: 未指定迭代编号
  Given 用户执行 /powerby-asp-arch 但未指定迭代编号
  When ASP Architecture Orchestrator 启动
  Then 列出 iterations.json 中所有迭代及其状态
  And 请求用户选择一个迭代编号
```

### US-004 → REQ-004
**As a** 开发者
**I want** 迭代名从我的需求描述中自动提取为 kebab-case 英文短名
**So that** 目录名简洁可读，无需手动命名

**Acceptance Criteria:**

```gherkin
Scenario: 自动提取迭代名
  Given 用户输入 "我想做一个任务管理系统"
  When ASP Orchestrator 解析需求描述
  Then 自动生成迭代名如 "task-manager"
  And 向用户展示 "迭代目录：docs/iterations/007-task-manager/"
  And 等待用户确认或修改

Scenario: 用户修改自动生成的迭代名
  Given ASP Orchestrator 自动生成迭代名 "task-manager"
  And 用户回复希望改为 "team-collab"
  When ASP Orchestrator 处理修改
  Then 使用 "team-collab" 作为迭代名
  And 创建目录 docs/iterations/007-team-collab/
```

### US-005 → REQ-005
**As a** 开发者
**I want** ASP 文档与 P0-P8 文档在同一迭代目录下兼容共存
**So that** 无论使用哪种流程，文档都在统一的位置管理

**Acceptance Criteria:**

```gherkin
Scenario: ASP 文档写入已有 P0-P8 迭代目录
  Given 迭代目录 docs/iterations/005-powerby-asp/ 下已有 prd.md、clarifications.md
  And 用户指定在该目录下执行 ASP 流程
  When ASP Orchestrator 生成 proposal.md、spec.md
  Then 不覆盖已有的 prd.md 和 clarifications.md
  And proposal.md、spec.md 正常写入同一目录
  And 两套文档共存

Scenario: P0-P8 文档写入已有 ASP 迭代目录
  Given 迭代目录下已有 ASP 产出的 proposal.md、spec.md
  And 用户在该目录下执行 P0-P8 流程
  When P0-P8 流程生成 prd.md
  Then 不覆盖已有的 proposal.md 和 spec.md
```

## Data Dictionary

| 术语 | 定义 |
|------|------|
| 迭代编号 (Iteration ID) | 三位数字字符串（如 "007"），全局唯一递增，所有流程共享 |
| 迭代名 (Iteration Name) | kebab-case 英文短名（如 "task-manager"），描述迭代主题 |
| 迭代全名 (Full Name) | `{id}-{name}` 格式（如 "007-task-manager"），用作目录名 |
| 迭代目录 (Iteration Directory) | `docs/iterations/{full_name}/`，存放该迭代所有文档 |
| iterations.json | `.powerby/iterations.json`，记录所有迭代的元数据 |
| ASP 产品交付物 | proposal.md、spec.md、function-points.md、product-map.md、prd_logs/ |
| ASP 架构交付物 | architecture.md、arch_logs/ |
| P0-P8 交付物 | prd.md、function-points.md、clarifications.md |

## 状态定义

### 迭代目录创建
- **Empty State**: `iterations.json` 为空或不存在，新编号从 001 开始
- **Error State**: 目录创建失败（权限问题），提示用户检查权限
- **Loading State**: 不适用（文件操作为同步）

### 迭代复用
- **Empty State**: 用户指定的迭代编号不存在，提示并询问是否新建
- **Error State**: 迭代目录存在但 `iterations.json` 中无记录，自动补录
- **Loading State**: 不适用

### 架构前置检查
- **Empty State**: 迭代目录下无任何 ASP 产品交付物，提示先完成产品流程
- **Error State**: 部分交付物缺失，逐一列出缺失文件
- **Loading State**: 不适用

## Traceability Matrix
| Proposal REQ | Spec US | 覆盖状态 |
|-------------|---------|---------|
| REQ-001 | US-001 | ✅ 已覆盖 |
| REQ-002 | US-002 | ✅ 已覆盖 |
| REQ-003 | US-003 | ✅ 已覆盖 |
| REQ-004 | US-004 | ✅ 已覆盖 |
| REQ-005 | US-005 | ✅ 已覆盖 |
