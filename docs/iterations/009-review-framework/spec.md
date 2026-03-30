# Spec: 还原式项目评审框架（Review Framework）

## 1. 概述

本规格定义了一套基于 Claude Skill 协议的模块化"还原式项目评审框架"。该框架的核心目标是：基于项目自身已有材料（代码、文档、Git 历史），对项目进行事实还原，建立层与层之间的追踪关系，并识别需求-实现偏差。

### 核心原则
- **事实优先**：评审基于已有事实，不做猜测
- **证据驱动**：所有对象都有证据来源，可追溯
- **冲突保留**：需求与实现不一致时，显式保留差异，不自动和解
- **标准化方法**：清晰定义标准，可量化、可追溯

### V1 范围
V1 优先跑通"产品 → 功能 → 关系 → 差异"主链路，包含以下模块：
- 项目接入与范围定义
- 证据采集与标准化
- 证据优先级与冲突决议
- 产品事实还原
- 功能事实还原
- 关系构建
- 差异与缺口识别
- 报告编排与导出

V2 扩展：架构事实还原、实现事实还原、验证事实还原

### Skill 实现基础

本框架的所有模块均基于 **Claude Skill 协议**实现。Skill 的编写必须遵循项目既有的 Skill 最佳实践框架（详见 `docs/skill_best.md`），该框架定义了从设计到交付的完整工程化流程。

**核心依赖**：
- **7 层 Skill 设计结构**：Intent Layer（能力边界）→ Strategy Layer（策略哲学）→ Capability Layer（工具集）→ Knowledge & Constraint Layer（事实说明）→ Structure Layer（渐进披露）→ Writing Layer（编写规范）→ Evaluation Layer（评估闭环）
- **渐进披露原则**：通过 `description` 触发 → `SKILL.md` 正文 → `scripts/` 和 `references/` 按需加载
- **评估驱动迭代**：所有 Skill 必须包含 baseline 对照、定量断言或人工 review，通过评估闭环持续优化
- **最小完备工具集**：每个 Skill 提供覆盖关键原子能力的工具，边界清晰可判断

**实现约束**：
- 每个 Skill 的 `description` 必须明确触发语境，略带主动性以避免 undertrigger
- 策略层写"判断框架"而非固定流程，支持模型根据证据切换路径
- 重复且确定性的操作必须下沉到 `scripts/`，不让模型重复造轮子
- 多领域内容通过 `references/` 分层组织，避免上下文污染

本规格中定义的所有 Skill（ProjectScope、EvidenceCollector、ConflictResolver 等）均遵循上述最佳实践框架进行设计和实现。

---

## 2. User Stories

### US-001 → REQ-001, REQ-002
**As a** 框架开发者
**I want** 定义统一的 Skill 协议和证据驱动的数据模型
**So that** 所有 Skill 可以遵循统一标准，独立运行和编排协作，且所有对象都有证据来源

**Acceptance Criteria:**
- Given 一个 Skill 定义
- When 按照协议规范实现
- Then 该 Skill 可以独立运行，输入输出格式符合协议
- And 所有输出对象都包含证据来源字段

### US-002 → REQ-008, REQ-009
**As a** 评审执行者
**I want** 接入项目并采集标准化证据
**So that** 可以基于项目自身材料进行事实还原

**Acceptance Criteria:**
- Given 一个项目代码仓库和文档目录
- When 执行项目接入和证据采集
- Then 生成资料清单，标记缺失项
- And 所有证据被标准化为 Evidence Unit 格式
- And 每个证据单元包含来源、时间、作者等元信息

### US-003 → REQ-003
**As a** 评审执行者
**I want** 识别证据冲突并按优先级决议
**So that** 可以基于最新、最可信的事实进行还原，同时保留冲突记录

**Acceptance Criteria:**
- Given 多个版本的产品文档和代码实现
- When 执行证据优先级判断
- Then 识别新旧文档冲突、文档与代码冲突
- And 按照"代码优先于旧文档，新文档优先于旧文档"规则决议
- And 显式保留冲突记录，不自动和解
- And 当两条证据时间相同、优先级相同但内容矛盾时，标记为 unresolved 并保留双方证据

### US-004 → REQ-004
**As a** 评审执行者
**I want** 从产品文档中还原产品事实
**So that** 可以识别项目的产品目标、用户角色和使用场景

**Acceptance Criteria:**
- Given PRD、README、Wiki 等产品文档
- When 执行产品事实还原
- Then 输出 Goal Catalog（产品目标清单）
- And 输出 Role Catalog（用户角色清单）
- And 输出 Scenario Catalog（使用场景清单）
- And 每个对象都标注证据来源

**Empty State:**
- Given 项目无任何产品文档（无 PRD、无 README、无 Wiki）
- When 执行产品事实还原
- Then 返回 partial 状态
- And 输出空的 Goal/Role/Scenario Catalog
- And 在 gaps 中记录 "missing_evidence: 无产品文档，无法还原产品事实"
- And 不做任何推断性补充

**Error State:**
- Given 产品文档存在但格式无法解析
- When 执行产品事实还原
- Then 返回 partial 状态，跳过不可解析文件
- And 在 errors 中记录具体文件路径和错误原因

### US-005 → REQ-005
**As a** 评审执行者
**I want** 从多种来源还原功能事实
**So that** 可以识别项目的完整功能清单、业务规则和功能边界

**Acceptance Criteria:**
- Given 产品文档、API 文档、代码、测试用例
- When 执行功能事实还原
- Then 输出 Feature Catalog（功能清单）
- And 输出 Rule Catalog（业务规则清单）
- And 输出 Boundary Catalog（功能边界清单）
- And 每个功能对象都标注证据来源（文档/代码/测试）

**Empty State:**
- Given 项目既无产品文档又无 API 文档
- When 执行功能事实还原
- Then 返回 partial 状态
- And 仅从代码和测试中提取功能（标注 source: code_only）
- And 在 gaps 中记录 "missing_evidence: 无文档来源，功能仅基于代码推断"

**Error State:**
- Given 功能提取过程中遇到不可解析的代码或文档
- When 执行功能事实还原
- Then 返回 partial 状态，跳过不可解析项
- And 在 errors 中记录具体路径和错误原因

### US-006 → REQ-006
**As a** 评审执行者
**I want** 建立跨层追踪关系
**So that** 可以追踪从产品目标到功能实现的完整链路

**Acceptance Criteria:**
- Given 产品对象和功能对象
- When 执行关系构建
- Then 输出 Traceability Matrix（追踪矩阵）
- And 每个 Goal 可以追踪到支撑它的 Feature
- And 每个 Feature 可以追溯到对应的 Goal
- And 关系都有证据支撑
- And 当关系缺乏显式证据时，标注 confidence: inferred
- And 无法确定的关系不强行建立连线

### US-007 → REQ-007
**As a** 评审执行者
**I want** 识别需求-实现差异和缺口
**So that** 可以发现项目中的不一致问题和缺失项

**Acceptance Criteria:**
- Given 产品对象、功能对象和追踪关系
- When 执行差异与缺口识别
- Then 输出 Difference List（差异清单）
- And 输出 Gap List（缺口清单）
- And 输出 Conflict List（冲突清单）
- And 每个差异/缺口都标注具体位置和证据

### US-008 → REQ-010
**As a** 评审结果使用者
**I want** 获得人类可读的 Markdown 报告
**So that** 可以快速理解评审结果并采取行动

**Acceptance Criteria:**
- Given 所有还原对象、关系和差异
- When 执行报告编排与导出
- Then 生成结构化的 Markdown 报告
- And 报告包含：项目概览、对象清单、追踪矩阵、差异清单
- And 报告中所有结论都有证据索引

### US-009 → REQ-011 (V2)
**As a** 评审执行者
**I want** 从代码结构和配置中还原架构事实
**So that** 可以识别系统的模块、实体和依赖关系

**Acceptance Criteria:**
- Given 项目代码仓库、配置文件、部署文件
- When 执行架构事实还原
- Then 输出 Module Catalog（模块清单）
- And 输出 Entity Catalog（实体清单）
- And 输出 Dependency Graph（依赖关系图）
- And 每个对象都标注证据来源

**Empty State:**
- Given 项目无可识别的模块结构
- When 执行架构事实还原
- Then 返回 partial 状态，输出空 Catalog
- And 在 gaps 中记录 "missing_evidence: 无法识别架构模块"

> **V2 说明**：本 User Story 属于 V2 范围，V1 阶段不实现对应 Skill，但保留追溯关系。

### US-010 → REQ-012 (V2)
**As a** 评审执行者
**I want** 识别代码中的实际实现单元和入口点
**So that** 可以建立架构到代码的映射关系

**Acceptance Criteria:**
- Given 项目源代码、配置文件、构建脚本
- When 执行实现事实还原
- Then 输出 Code Unit Catalog（代码单元清单）
- And 输出 Entry Point Catalog（入口点清单）
- And 每个对象都标注所属模块

**Empty State:**
- Given 项目无可解析的代码文件
- When 执行实现事实还原
- Then 返回 partial 状态，输出空 Catalog

> **V2 说明**：本 User Story 属于 V2 范围，V1 阶段不实现对应 Skill，但保留追溯关系。

### US-011 → REQ-013 (V2)
**As a** 评审执行者
**I want** 识别项目中现有的测试和可观测性证据
**So that** 可以评估功能和实现是否有验证支撑

**Acceptance Criteria:**
- Given 测试代码、日志配置、监控配置
- When 执行验证事实还原
- Then 输出 Test Catalog（测试清单）
- And 输出 Observability Catalog（可观测性清单）
- And 每个对象标注覆盖的功能或边界

**Empty State:**
- Given 项目无测试文件和监控配置
- When 执行验证事实还原
- Then 返回 partial 状态，输出空 Catalog
- And 在 gaps 中记录 "missing_evidence: 无验证证据"

> **V2 说明**：本 User Story 属于 V2 范围，V1 阶段不实现对应 Skill，但保留追溯关系。

---

## 3. Data Dictionary

### 3.1 核心数据模型

#### Evidence Unit（证据单元）
项目内所有原始材料的标准化表示。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| evidence_id | string | 唯一标识 | "ev-001" |
| source_type | enum | 证据类型：doc/code/test/config/commit/issue | "doc" |
| source_path | string | 来源路径 | "docs/prd.md" |
| timestamp | datetime | 时间戳 | "2026-03-27T10:00:00Z" |
| author | string | 作者 | "user@example.com" |
| content | string | 内容片段 | "产品目标：..." |
| version_hint | string | 版本线索 | "v2.0" |

#### Object Record（对象记录）
还原出的结构化对象（Goal、Feature 等）。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| object_id | string | 唯一标识 | "goal-001" |
| object_type | enum | 对象类型：goal/role/scenario/feature/rule/boundary/constraint/non_goal/module/entity/code_unit/entry_point/test/observability（V2 类型在 V2 阶段使用） | "goal" |
| name | string | 对象名称 | "提升用户留存率" |
| description | string | 详细描述 | "通过个性化推荐..." |
| evidence_refs | array | 证据引用列表 | ["ev-001", "ev-002"] |
| confidence | enum | 置信度：explicit/inferred（无证据时不生成对象，记录 gap） | "explicit" |
| metadata | object | 扩展元数据 | {"priority": "high"} |

#### Project Metadata（项目元数据）
ProjectScope Skill 的输出，描述项目基本信息。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| project_name | string | 项目名称 | "powerby-skills" |
| project_type | string | 项目类型 | "skill-framework" |
| scope | enum | 评审范围：full_project/single_service/single_feature | "full_project" |
| file_count | number | 文件总数 | 120 |
| resource_inventory | object | 资料清单（docs/code/tests/configs） | {...} |
| missing_resources | array | 缺失的资源类型 | ["测试文件"] |

#### Feature State（功能状态）
FeatureReconstructor Skill 的输出，描述功能的实现状态。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| feature_id | string | 对应的 Feature ID | "feature-001" |
| state | enum | 状态：doc_defined/implemented/partial/residual | "implemented" |
| doc_evidence | array | 文档证据引用 | ["ev-001"] |
| code_evidence | array | 代码证据引用 | ["ev-005"] |

#### Relationship Record（关系记录）
对象之间的追踪关系。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| relation_id | string | 唯一标识 | "rel-001" |
| relation_type | enum | 关系类型：supports/constrains/maps_to/implemented_by/covers | "supports" |
| source_id | string | 起点对象 ID | "feature-001" |
| target_id | string | 终点对象 ID | "goal-001" |
| evidence_refs | array | 证据引用列表 | ["ev-003"] |
| confidence | enum | 置信度 | "explicit" |

#### Conflict Record（冲突记录）
识别出的证据冲突。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| conflict_id | string | 唯一标识 | "conflict-001" |
| conflict_type | enum | 冲突类型：doc_version/doc_code/requirement_implementation | "doc_code" |
| evidence_a | string | 证据 A 引用 | "ev-001" |
| evidence_b | string | 证据 B 引用 | "ev-005" |
| description | string | 冲突描述 | "PRD 声明功能 X，但代码未实现" |
| resolution | enum | 决议状态：preserved/resolved_by_priority | "preserved" |
| priority_winner | string | 优先采用的证据 | "ev-005" |

#### Gap Record（缺口记录）
识别出的缺失项。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| gap_id | string | 唯一标识 | "gap-001" |
| gap_type | enum | 缺口类型：missing_object/missing_relation/missing_evidence | "missing_relation" |
| description | string | 缺口描述 | "Goal-001 无对应 Feature 支撑" |
| severity | enum | 严重程度：critical/major/minor | "major" |
| context | object | 上下文信息 | {"goal_id": "goal-001"} |

#### Review Context（评审上下文）
评审会话的全局上下文。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| review_id | string | 评审会话 ID | "review-20260327-001" |
| project_path | string | 项目路径 | "/path/to/project" |
| scope | enum | 评审范围：full_project/single_service/single_feature | "full_project" |
| timestamp | datetime | 评审时间 | "2026-03-27T10:00:00Z" |
| project_metadata | object | 项目元数据（来自 ProjectScope） | Project Metadata |
| evidence_registry | array | 证据注册表 | [Evidence Unit, ...] |
| current_facts | object | 当前有效事实集（来自 ConflictResolver） | {product_facts: [...], implementation_facts: [...]} |
| object_registry | array | 对象注册表 | [Object Record, ...] |
| feature_state_registry | array | 功能状态注册表 | [Feature State, ...] |
| relation_registry | array | 关系注册表 | [Relationship Record, ...] |
| conflict_registry | array | 冲突注册表 | [Conflict Record, ...] |
| gap_registry | array | 缺口注册表 | [Gap Record, ...] |

---

## 4. 统一 Skill 协议

### 4.1 Skill 接口规范

每个 Skill 必须遵循以下接口规范：

```yaml
skill:
  name: string                    # Skill 名称
  version: string                 # 版本号
  description: string             # 功能描述

  input:
    context: ReviewContext        # 评审上下文（必需）
    parameters: object            # 特定参数（可选）

  evidence_policy:
    required_sources: array       # 必需的证据来源类型
    min_confidence: enum          # 最低置信度要求：explicit/inferred/uncertain
    allow_inference: boolean      # 是否允许推断

  output:                         # 所有 Skill 必须返回以下标准结构
    status: enum                  # 执行状态：success/partial/failed（必需）
    objects: array                # 新增的 Object Record 列表（写入 context.object_registry）
    relations: array              # 新增的 Relationship Record 列表（写入 context.relation_registry）
    conflicts: array              # 新增的 Conflict Record 列表（写入 context.conflict_registry）
    gaps: array                   # 新增的 Gap Record 列表（写入 context.gap_registry）
    context_writes: object        # 写入 ReviewContext 的非标准字段（如 project_metadata、evidence_registry、current_facts）
    metadata: object              # 执行元数据（耗时、处理数量等）
    errors: array                 # 错误信息列表（必需，无错误时为空数组）
```

### 4.3 协议一致性规则

1. **所有 Skill 输出必须包含 `status` 和 `errors` 字段**，即使无错误也必须返回空数组
2. **标准归集规则**：Skill 输出的 objects/relations/conflicts/gaps 自动归集到 ReviewContext 对应的 registry
3. **context_writes 机制**：当 Skill 需要写入 ReviewContext 的非标准字段（如 `project_metadata`、`evidence_registry`、`current_facts`）时，通过 `context_writes` 字段声明，编排层负责写入
4. **下游引用规则**：下游 Skill 必须从 ReviewContext 读取上游数据，不直接引用上游 Skill 的输出变量名

### 4.2 执行状态定义

| 状态 | 说明 | 后续处理 |
|------|------|---------|
| success | 完全成功 | 继续下一个 Skill |
| partial | 部分成功，有警告 | 记录警告，继续执行 |
| failed | 执行失败 | 中止流程，报告错误 |

---

## 5. V1 Skill 定义

### 5.1 Skill: ProjectScope（项目接入与范围定义）

**目标**：接入项目资料，定义评审范围，生成资料清单

**职责**：
- 接入代码仓库、文档目录
- 识别项目类型（单体/微服务/前端/后端）
- 定义评审范围（全项目/单服务/单功能）
- 生成资料清单，标记缺失项

**输入**：
```yaml
parameters:
  project_path: string          # 项目路径
  scope_type: enum              # full_project/single_service/single_feature
  include_patterns: array       # 包含的文件模式
  exclude_patterns: array       # 排除的文件模式
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects: []                     # ProjectScope 不产出 Object Record
relations: []
conflicts: []
gaps: []
context_writes:
  project_metadata:             # 写入 ReviewContext.project_metadata
    project_name: string
    project_type: string
    scope: string
    file_count: number
    resource_inventory:
      docs: array
      code: array
      tests: array
      configs: array
    missing_resources: array
metadata:
  scan_duration_ms: number
errors: array                   # 错误信息列表
```

**边界**：
- 负责：定义评审范围、列资料清单
- 不负责：理解内容含义、推断功能结构

**依赖关系**：无前置依赖（入口 Skill）

**证据要求**：不涉及证据提取，仅做资料发现

**失败处理**：项目路径不存在或无可读文件时返回 failed

---

### 5.2 Skill: EvidenceCollector（证据采集与标准化）

**目标**：采集项目内所有证据，标准化为 Evidence Unit 格式

**职责**：
- 采集文档、代码、测试、配置、Git 历史
- 标准化为 Evidence Unit 格式
- 对证据打元信息标签（来源、时间、作者）

**输入**：
```yaml
parameters:
  resource_inventory: object    # 来自 ProjectScope 的资料清单
  collection_depth: enum        # shallow/deep，控制采集深度
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects: []                     # EvidenceCollector 不产出 Object Record
relations: []
conflicts: []
gaps: []
context_writes:
  evidence_registry: array      # 写入 ReviewContext.evidence_registry [Evidence Unit, ...]
metadata:
  total_evidence_count: number
  by_source_type:
    doc: number
    code: number
    test: number
    config: number
    commit: number
    issue: number
errors: array
```

**边界**：
- 负责：证据对象化、统一格式
- 不负责：事实优先级判断、业务解释

**依赖关系**：依赖 ProjectScope 的 project_metadata.resource_inventory

**证据要求**：采集项目内所有可发现的材料

**失败处理**：部分文件无法读取时返回 partial，记录跳过的文件

---

### 5.3 Skill: ConflictResolver（证据优先级与冲突决议）

**目标**：判断证据优先级，识别冲突，按规则决议

**职责**：
- 对证据按优先级排序
- 识别新旧文档冲突
- 识别文档与代码冲突
- 显式保留冲突记录

**输入**：
```yaml
# 从 ReviewContext 读取
context.evidence_registry       # 来自 EvidenceCollector 的证据列表
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects: []
relations: []
conflicts: array                # Conflict Record 列表，写入 context.conflict_registry
gaps: []
context_writes:
  current_facts:                # 写入 ReviewContext.current_facts
    product_facts: array        # 当前有效的产品事实证据 ID 列表
    implementation_facts: array # 当前有效的实现事实证据 ID 列表
metadata:
  priority_rules_applied:
    - "产品层：新文档优先于旧文档"
    - "实现层：代码优先于旧文档"
    - "架构层：代码结构/配置优先于旧架构图"
  unresolved_conflicts: number
errors: array
```

**边界**：
- 负责：决定"当前采用哪条事实"、显式保留冲突
- 不负责：评价谁对谁错、替项目做需求裁决

**依赖关系**：依赖 EvidenceCollector 的 evidence_units

**证据要求**：所有证据必须有 timestamp 和 source_type

**失败处理**：
- 无法判断优先级时标记为 unresolved
- 冲突决议规则无法覆盖的情况保留为 preserved

**优先级决议规则**：

| 层级 | 规则 | 说明 |
|------|------|------|
| 产品层 | 新文档 > 旧文档 | 越新的产品文档优先级越高 |
| 实现层 | 代码 > 文档 | 代码代表真实实现状态 |
| 架构层 | 代码结构 > 旧架构图 | 代码结构更接近现状 |
| 辅助 | commit/PR/issue | 辅助说明演进背景，不作为主事实 |

---

### 5.4 Skill: ProductReconstructor（产品事实还原）

**目标**：基于产品文档还原产品目标、用户角色、使用场景

**职责**：
- 从 PRD/README/Wiki 提取 Goal
- 从角色描述/权限设计中提取 Role
- 从用户流程/场景描述中提取 Scenario
- 从产品说明中提取 Constraint / Non-goal
- 无 PRD 时，使用 commit/issue 辅助做保守推断

**输入**：
```yaml
# 从 ReviewContext 读取
context.evidence_registry       # 全量证据列表
context.current_facts           # 当前有效事实集（来自 ConflictResolver）
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects:                        # 写入 context.object_registry
  - type: goal
    data:
      goal_id: string
      name: string
      problem_statement: string
      target_user: string
      business_value: string
      evidence_refs: array
      confidence: enum

  - type: role
    data:
      role_id: string
      name: string
      description: string
      usage_context: string
      evidence_refs: array
      confidence: enum

  - type: scenario
    data:
      scenario_id: string
      actor: string
      trigger: string
      expected_outcome: string
      preconditions: array
      evidence_refs: array
      confidence: enum

  - type: constraint
    data:
      constraint_id: string
      description: string
      evidence_refs: array

  - type: non_goal
    data:
      non_goal_id: string
      description: string
      evidence_refs: array

relations: []
conflicts: []
gaps: []                        # 无产品文档时记录缺口
context_writes: {}
metadata:
  total_goals: number
  total_roles: number
  total_scenarios: number
  inference_count: number       # 推断对象数量
errors: array                   # 错误信息列表
```

**边界**：
- 负责：还原需求侧定义的产品世界
- 不负责：证明实现是否已满足、替代功能模块做边界定义

**依赖关系**：依赖 ConflictResolver 的 current_facts

**证据要求**：
- 产品目标必须来自产品文档，不从代码推断
- 如果无 PRD，使用 README/commit/issue 做保守推断，并标注 confidence: inferred
- 无任何证据时，不得生成对象；应在 gaps 中记录 "missing_evidence: 无法为该对象找到任何证据来源"

**失败处理**：
- 无产品文档时返回 partial，输出空 Goal Catalog 并标记缺失
- 仅有 README 时做保守还原，明确标注推断边界

---

### 5.5 Skill: FeatureReconstructor（功能事实还原）

**目标**：从多种来源还原项目功能集合、业务规则和功能边界

**职责**：
- 从产品文档提取功能项
- 从 API/路由提取功能入口
- 从代码 service/handler 提取功能实现
- 从测试用例提取功能行为
- 识别业务规则、边界、流程
- 标记文档功能 vs 已实现功能的差异

**输入**：
```yaml
# 从 ReviewContext 读取
context.object_registry         # 产品对象（来自 ProductReconstructor）
context.current_facts           # 当前有效事实集（来自 ConflictResolver）
context.evidence_registry       # 全量证据列表
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects:                        # 写入 context.object_registry
  - type: feature
    data:
      feature_id: string
      name: string
      goal_ref: string          # 对应的 Goal ID
      summary: string
      source: enum              # doc_only/code_only/both
      evidence_refs: array
      confidence: enum

  - type: rule
    data:
      rule_id: string
      feature_ref: string
      description: string
      trigger_condition: string
      expected_behavior: string
      exception_behavior: string
      evidence_refs: array

  - type: boundary
    data:
      boundary_id: string
      feature_ref: string
      in_scope: array
      out_of_scope: array
      preconditions: array
      edge_cases: array
      failure_modes: array
      evidence_refs: array

relations: []
conflicts: []
gaps: []                        # 无功能来源时记录缺口
context_writes:
  feature_state_registry: array # 写入 ReviewContext.feature_state_registry
    # Feature State 结构：
    # - feature_id: string
    # - state: enum (doc_defined/implemented/partial/residual)
    # - doc_evidence: array
    # - code_evidence: array
metadata:
  total_features: number
  total_rules: number
  total_boundaries: number
  code_only_features: number    # 仅代码证据的功能数量
  doc_only_features: number     # 仅文档证据的功能数量
errors: array                   # 错误信息列表
```

**边界**：
- 负责：还原"系统表达了哪些功能能力"和"边界规则"
- 不负责：设计新功能、假设隐藏需求、给功能打质量分

**依赖关系**：依赖 ProductReconstructor 的产品对象 + ConflictResolver 的事实集

**证据要求**：
- 功能必须有至少一个证据来源（文档或代码）
- 规则优先从文档提取，辅以代码 if/guard/validator
- 边界由显式证据定义，不做脑补

**失败处理**：
- 某些功能仅有代码证据、无文档时，标注 source: code_only
- 功能仅在文档中声明、代码未实现时，标注 state: doc_defined

---

### 5.6 Skill: RelationBuilder（关系构建）

**目标**：将不同层级的事实对象连接成可追踪链路

**职责**：
- 建立 Goal → Feature 关系（supports）
- 建立 Rule → Feature 关系（constrains）
- 识别孤立对象（无关系的 Goal 或 Feature）

**输入**：
```yaml
# 从 ReviewContext 读取
context.object_registry         # 产品对象 + 功能对象
context.evidence_registry       # 相关证据
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects: []
relations:                      # 写入 context.relation_registry
  - type: supports
    data: RelationshipRecord
  - type: constrains
    data: RelationshipRecord
conflicts: []
gaps: []                        # 孤立对象记录为 gap
context_writes: {}
metadata:
  traceability_matrix:
    goals_with_features: array  # 有 Feature 支撑的 Goal
    goals_without_features: array  # 无 Feature 支撑的 Goal
    features_with_goals: array  # 有 Goal 关联的 Feature
    features_without_goals: array  # 无 Goal 关联的 Feature（孤立功能）
  coverage_stats:
    goal_coverage_rate: number  # Goal 被 Feature 覆盖的比率
    feature_traceability_rate: number  # Feature 可追溯到 Goal 的比率
errors: array                   # 错误信息列表
```

**边界**：
- 负责：建链、识别孤立对象
- 不负责：判断关系优劣、修改对象定义

**依赖关系**：依赖 ProductReconstructor + FeatureReconstructor

**证据要求**：
- 关系必须有证据支撑（显式引用或文档中的关联描述）
- 推断的关系标注 confidence: inferred
- 无法确定的关系不强行连线

**失败处理**：
- 对象过少无法建立有意义的关系时返回 partial
- 关系证据不足时标注 confidence: uncertain

---

### 5.7 Skill: GapAnalyzer（差异与缺口识别）

**目标**：基于事实对象与关系，识别显式差异与信息缺口

**职责**：
- 识别需求与实现差异
- 识别对象缺失
- 识别链路断点
- 识别未覆盖边界

**输入**：
```yaml
# 从 ReviewContext 读取
context.object_registry         # 所有还原对象
context.relation_registry       # 所有关系
context.conflict_registry       # 所有冲突
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects: []
relations: []
conflicts: []                   # 输出新识别的冲突（需求-实现冲突）
gaps:                           # 写入 context.gap_registry
  - type: gap_record
    data: GapRecord
context_writes: {}
metadata:
  difference_list:
    - type: doc_exists_code_missing
      description: "文档功能存在，代码未实现"
      items: array
    - type: code_exists_doc_missing
      description: "代码实现存在，产品文档未声明"
      items: array
    - type: goal_no_feature
      description: "产品目标存在，无功能支撑"
      items: array
    - type: feature_no_goal
      description: "功能存在，无产品目标关联"
      items: array
  summary:
    total_gaps: number
    critical_gaps: number
    major_gaps: number
    minor_gaps: number
errors: array                   # 错误信息列表
```

**边界**：
- 负责：报差异、报缺口
- 不负责：定性为 bug/设计差、做主观裁判

**依赖关系**：依赖 RelationBuilder + ConflictResolver

**证据要求**：
- 差异和缺口必须有客观依据
- 描述必须准确指向具体对象和位置

**失败处理**：
- 对象或关系不足时返回 partial，输出已能识别的差异
- 不做推测性的缺口补充

---

### 5.8 Skill: ReportComposer（报告编排与导出）

**目标**：将所有还原结果编排为人类可读的 Markdown 报告

**职责**：
- 组织项目概览
- 编排对象清单
- 编排追踪矩阵
- 编排差异与缺口报告
- 生成证据索引

**输入**：
```yaml
# 从 ReviewContext 读取
context                         # 完整的评审上下文
```

**输出**（遵循统一协议 4.1）：
```yaml
status: enum                    # success/partial/failed
objects: []
relations: []
conflicts: []
gaps: []
context_writes: {}
metadata:
  report_path: string           # 报告文件路径
  report_sections:
    - project_overview
    - product_reconstruction
    - feature_reconstruction
    - traceability_matrix
    - differences_and_gaps
    - evidence_index
errors: array                   # 错误信息列表
```

**报告结构**：

```markdown
# 项目还原评审报告

## 1. 项目概览
- 项目名称、类型、评审范围、评审时间

## 2. 产品层还原
- 目标清单（含证据来源）
- 角色清单
- 场景清单
- 约束与非目标

## 3. 功能层还原
- 功能清单（含状态标注：doc_defined/implemented/partial）
- 业务规则
- 功能边界

## 4. 追踪矩阵
- Goal → Feature 映射表
- 覆盖率统计

## 5. 差异与缺口
- 差异清单
- 缺口清单
- 冲突清单

## 6. 证据索引
- 所有证据来源汇总
```

**边界**：
- 负责：组织输出、格式化
- 不负责：重新解释事实、修改上游对象

**依赖关系**：依赖所有上游 Skill 的输出

**证据要求**：所有输出必须来自统一事实库，报告内容与底层数据一致

**失败处理**：部分上游数据缺失时，在报告中标注"数据缺失"

---

## 6. 状态定义

### 6.1 Skill 执行状态

| Skill | Empty State | Loading State | Error State |
|-------|------------|---------------|-------------|
| ProjectScope | 无项目路径输入 | "正在扫描项目结构..." | 项目路径不存在 |
| EvidenceCollector | 无资料清单 | "正在采集证据..." | 部分文件不可读 |
| ConflictResolver | 无证据输入 | "正在分析证据冲突..." | 证据格式异常 |
| ProductReconstructor | 无产品文档 | "正在还原产品事实..." | 文档解析失败 |
| FeatureReconstructor | 无功能来源 | "正在还原功能事实..." | 功能提取失败 |
| RelationBuilder | 对象不足 | "正在构建追踪关系..." | 关系构建失败 |
| GapAnalyzer | 对象或关系为空 | "正在识别差异与缺口..." | 分析异常 |
| ReportComposer | 无上游数据 | "正在生成报告..." | 报告生成失败 |

---

## 7. 编排流程设计

### 7.1 V1 执行流程

```
阶段 1：范围与证据
  ProjectScope → EvidenceCollector → ConflictResolver

阶段 2：事实还原
  ProductReconstructor → FeatureReconstructor

阶段 3：关系与差异
  RelationBuilder → GapAnalyzer

阶段 4：报告输出
  ReportComposer
```

### 7.2 详细编排

```
┌─────────────────────────────────────────────────┐
│              阶段 1：范围与证据                    │
│                                                   │
│  ProjectScope                                     │
│    └─→ resource_inventory                         │
│         └─→ EvidenceCollector                     │
│              └─→ evidence_units                   │
│                   └─→ ConflictResolver            │
│                        ├─→ current_facts          │
│                        └─→ conflicts              │
├─────────────────────────────────────────────────┤
│              阶段 2：事实还原                       │
│                                                   │
│  ProductReconstructor (← current_facts)           │
│    └─→ goals, roles, scenarios                    │
│         └─→ FeatureReconstructor                  │
│              └─→ features, rules, boundaries      │
├─────────────────────────────────────────────────┤
│              阶段 3：关系与差异                     │
│                                                   │
│  RelationBuilder (← goals, features)              │
│    └─→ relations, traceability_matrix             │
│         └─→ GapAnalyzer                           │
│              └─→ gaps, differences                │
├─────────────────────────────────────────────────┤
│              阶段 4：报告输出                       │
│                                                   │
│  ReportComposer (← 全部上游数据)                   │
│    └─→ review_report.md                           │
└─────────────────────────────────────────────────┘
```

### 7.3 中断与恢复

- 每个 Skill 执行完成后，将结果写入 Review Context
- 如果某个 Skill 返回 failed，中止流程并报告错误
- 如果返回 partial，记录警告并继续
- 支持从任意 Skill 恢复执行（基于 Review Context 的持久化）

---

## 8. V1 最小可行实现建议

### 8.1 实现优先级

| 优先级 | Skill | 理由 |
|--------|-------|------|
| P0 | 统一 Skill 协议 + 数据模型 | 所有 Skill 的基础 |
| P0 | ProjectScope | 入口 Skill |
| P0 | EvidenceCollector | 证据基础 |
| P1 | ConflictResolver | 事实判定核心 |
| P1 | ProductReconstructor | 产品层还原 |
| P1 | FeatureReconstructor | 功能层还原 |
| P2 | RelationBuilder | 跨层追踪 |
| P2 | GapAnalyzer | 差异识别 |
| P3 | ReportComposer | 报告输出 |

### 8.2 V1 验收标准

1. 给定一个包含 PRD 和代码的项目
2. 能够完成 4 个阶段的全流程执行
3. 输出包含以下内容的 Markdown 报告：
   - 产品目标清单（含证据来源）
   - 功能清单（含状态标注）
   - 追踪矩阵（Goal → Feature）
   - 差异与缺口清单
4. 所有对象都有证据引用
5. 冲突被显式保留

---

## 9. 协作示例：以 powerby-skills 项目为例

### 9.1 场景描述

对 powerby-skills 项目执行完整评审，识别需求-实现一致性。

### 9.2 执行过程

**阶段 1：范围与证据**

```
ProjectScope:
  输入: project_path = "/path/to/powerby-skills"
  输出:
    docs: [docs/consitution.md, docs/iterations/*/prd.md, ...]
    code: [skills/*/SKILL.md, ...]
    tests: []
    configs: [package.json, ...]
    missing: [测试文件目录未找到]

EvidenceCollector:
  输入: resource_inventory
  输出:
    - ev-001: {type: doc, path: "docs/consitution.md", content: "项目宪法..."}
    - ev-002: {type: doc, path: "docs/iterations/005-powerby-asp/prd.md", content: "..."}
    - ev-003: {type: code, path: "skills/powerby-asp-product/SKILL.md", content: "..."}
    - ...

ConflictResolver:
  输入: evidence_units
  输出:
    conflicts:
      - conflict-001: {type: doc_version, description: "两个版本的 ASP 流程描述不一致"}
    current_facts:
      product_facts: [ev-001, ev-002]
      implementation_facts: [ev-003, ...]
```

**阶段 2：事实还原**

```
ProductReconstructor:
  输出:
    goals:
      - goal-001: {name: "提供模块化的 Skill 开发框架", evidence: [ev-001]}
    roles:
      - role-001: {name: "开发者", description: "使用 Skill 进行开发"}
    scenarios:
      - scenario-001: {actor: "开发者", trigger: "启动 ASP 流程", outcome: "生成 spec.md"}

FeatureReconstructor:
  输出:
    features:
      - feature-001: {name: "ASP 自治式规格精炼", goal_ref: "goal-001", source: "both"}
      - feature-002: {name: "架构设计流程", goal_ref: "goal-001", source: "both"}
    rules:
      - rule-001: {feature_ref: "feature-001", description: "审查序列最多 5 轮"}
    feature_states:
      - {feature_id: "feature-001", state: "implemented"}
```

**阶段 3：关系与差异**

```
RelationBuilder:
  输出:
    relations:
      - {type: "supports", source: "feature-001", target: "goal-001"}
    traceability_matrix:
      goal_coverage_rate: 85%

GapAnalyzer:
  输出:
    gaps:
      - gap-001: {type: "missing_evidence", description: "feature-002 无测试证据"}
    differences:
      - diff-001: {type: "doc_exists_code_missing", description: "PRD 声明的 X 功能未实现"}
```

**阶段 4：报告输出**

```
ReportComposer:
  输出: review_report.md
```

---

## Traceability Matrix

| Proposal REQ | Spec US | 覆盖状态 |
|-------------|---------|---------|
| REQ-001 | US-001 | 已覆盖 |
| REQ-002 | US-001 | 已覆盖 |
| REQ-003 | US-003 | 已覆盖 |
| REQ-004 | US-004 | 已覆盖 |
| REQ-005 | US-005 | 已覆盖 |
| REQ-006 | US-006 | 已覆盖 |
| REQ-007 | US-007 | 已覆盖 |
| REQ-008 | US-002 | 已覆盖 |
| REQ-009 | US-002 | 已覆盖 |
| REQ-010 | US-008 | 已覆盖 |
| REQ-011 | US-009 | 已覆盖 (V2) |
| REQ-012 | US-010 | 已覆盖 (V2) |
| REQ-013 | US-011 | 已覆盖 (V2) |
