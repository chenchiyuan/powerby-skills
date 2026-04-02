# 开发任务计划

**迭代编号**: 010
**分支**: `review`
**创建日期**: 2026-03-30
**生命周期阶段**: P5 - 开发规划 / P6 - 开发实现

---

## 1. 需求与架构对齐报告

### 核心目标复述
- 基于 [`proposal.md`](./proposal.md)、[`spec.md`](./spec.md) 与 [`architecture.md`](./architecture.md)，把 `pb-review` 从“还原式评审”升级为“标准驱动的测试化就绪评估”。
- 严格沿用 009 的扩展复用路线：不新增 skill，只升级既有 skill、共享 schema、renderer、模板和 manifest。
- 新增四类专项交付物：`11-testability-scorecard.md`、`12-test-case-index.md`、`13-test-fixture-contract.md`、`14-test-oracle-matrix.md`。

### 范围边界
- **本次实现（P0）**: FP-001 ~ FP-015 对应的 schema、renderer、模板、manifest、report/testability 汇总、测试。
- **明确排除**: 自动修复缺失 oracle/fixture、修改 `pb-review-standard.md`、引入后端 LLM 代理、在目标业务仓库实际跑一轮完整验证。

### 成功标准
- [x] `feature-spec-index` 与 `feature-spec-card` 支持 D-17 ~ D-20 和 5 个测试化聚合列。
- [x] `project-scope` 输出 `entry_surface_inventory`，manifest 扩展到 DLV-011 ~ DLV-014。
- [x] `relation / gap / report` 三条现有交付链能承载测试化信息。
- [x] `pb-review` 新增 4 个确定性 renderer 与 8 个共享 schema 文件。
- [x] `pb-review` 相关自动化测试覆盖新交付物契约。

## 1.3 现有代码分析报告

### 现有组件清单

| 组件名称 | 路径 | 职责 | 复用可能性 | 备注 |
|---------|------|------|-----------|------|
| `skills/pb-review/` | `skills/pb-review/` | 编排器、共享脚本、共享 references | 极高 | 本轮直接扩展 Step 13~16、schemas、assets |
| `render_feature_deliverables.py` | `skills/pb-review-feature-reconstructor/scripts/` | 生成功能索引和规格卡 | 极高 | D-17~D-20 最适合在这里增量补齐 |
| `render_traceability_matrix.py` | `skills/pb-review-relation-builder/scripts/` | 生成追踪矩阵 | 高 | 直接扩展 Feature→TestCaseGroup / Rule→NegativeTest |
| `render_gap_analysis.py` | `skills/pb-review-gap-analyzer/scripts/` | 渲染差异与缺口 | 高 | 直接扩展 4 种测试化 gap 与 `gap_severity` |
| `tests/test_pb_review_renderers.py` | `tests/` | renderer 契约测试 | 极高 | 可直接扩展到 11~14 交付物 |

### 编码规范总结
- **代码风格**: Python 确定性脚本 + Markdown 模板 / schema / skill 文档。
- **命名规范**: deliverable、schema、registry 字段统一使用 snake_case；目录名保持 kebab-case。
- **测试模式**: `pytest` 做 renderer / contract / layout 测试，`validate_pb_review_skills.py` 做结构校验。
- **注释规范**: Python 使用 PEP 257 docstring，复杂渲染逻辑只解释意图与边界。

### 复用建议
- **可直接复用**: 009 的 `deliverable_rendering.py`、renderer 测试模式、manifest 结构。
- **可扩展复用**: `review_runner.py` 的确定性 step 执行模型、`system_context_renderer.py` 的模板渲染方式。
- **需全新开发**: 8 个 schema 文件、4 个 Step 13~16 renderer、测试化指标聚合 helper。

### 一致性建议
- **风格参考**: 延续 009 的“结构化结果 + 模板落盘”模式。
- **架构模式**: 保持顺序执行和 checkpoint 恢复，不引入并行 / 分叉流程。
- **注意事项**: Step 12 报告与 Step 13~16 专项报告的先后关系必须清晰，不能让 pending 的 DLV-011~014 反向阻塞 `07-review-report.md`。

## 1.5 文档风格定义

- **文档标准**: Markdown 模板 + schema markdown + PEP 257 Python docstring。
- **共享协议**: 所有测试化规则优先下沉到 `skills/pb-review/schemas/`，skill 文档只引用不重复抄写。
- **验证方式**: `python3 scripts/validate_pb_review_skills.py` + `pytest`。

## 2. 技术方案评估

### 方案 A：把测试化规则散落到各个 SKILL.md
- **简介**: 直接在 `feature-reconstructor`、`gap-analyzer`、`pb-review` 等 skill 文本里各自写规则。
- **架构遵循性**: 偏离 010 `schemas/` 协议层设计。
- **哲学对齐分析**:
  - **SOLID**: 差，规则职责会混进多个 skill。
  - **KISS**: 表面快，长期维护复杂。
  - **DRY**: 明显违背。
  - **最小影响面**: 短期文件变少，长期改动面更大。
  - **最小惊讶原则**: 不同 skill 可能出现多套口径。
- **优点**: 落地快。
- **缺点**: 不可维护，无法被 Step 13~16 脚本直接复用。

### 方案 B：共享 schema + 现有 renderer 增量升级
- **简介**: 规则进入 `skills/pb-review/schemas/`，renderer 和模板按 010 架构扩展。
- **架构遵循性**: 完整对齐 `architecture.md` 的协议层、组件划分和 Step 13~16。
- **哲学对齐分析**:
  - **SOLID**: 规则、聚合、落盘职责分离明确。
  - **KISS**: 对现有结构改动小，新增概念集中。
  - **DRY**: 最优。
  - **最小影响面**: 全部改动都限制在 `pb-review` 作用域内。
  - **最小惊讶原则**: 用户能直接从 deliverable 和 schema 理解口径。
- **优点**: 可维护、可测试、可扩展。
- **缺点**: 首次需要补较多文件。

### 我的建议
- **推荐方案**: 方案 B
- **核心理由**: 010 的本质不是“多写几段文案”，而是把测试化规则沉淀为统一可消费协议。只有 schema + renderer 增量升级才能同时满足架构、脚本复用和测试契约。

## 3. 开发任务清单

### P0 核心功能（Must Have）

#### TASK-010-001: 建立测试化共享 schema 与指标聚合层
- **关联需求**: REQ-001 / REQ-002 / REQ-009 ~ REQ-013
- **关联架构**: Section 2 协议层设计、Section 3.2.4 编排器升级
- **任务描述**: 新增 8 个 schema 文件与 `testability_metrics.py`，统一 M-01 ~ M-07、D-17 ~ D-20、gap severity、entry surface 类型。
- **验收标准**:
  - [x] `skills/pb-review/schemas/` 下 8 个文件齐备
  - [x] `testability_metrics.py` 提供评分、等级和状态统计
  - [x] **异常路径验证**: schema 缺失时 validator 失败
  - [x] **文档化标准合规**
- **预估工时**: 1.5h
- **状态**: 已完成

#### TASK-010-002: 升级 project-scope 与 manifest
- **关联需求**: REQ-004 / REQ-013
- **关联架构**: Section 3.2.5、Section 5.6
- **任务描述**: 扫描 `entry_surface_inventory`，扩展 `deliverable_manifest` 到 DLV-011 ~ DLV-014，并更新 system context 模板。
- **验收标准**:
  - [x] `project_metadata` 包含 `entry_surface_inventory`
  - [x] manifest 包含 14 个交付物条目
  - [x] **异常路径验证**: 路径缺失时仍返回 `failed`
  - [x] **文档化标准合规**
- **预估工时**: 1h
- **状态**: 已完成

#### TASK-010-003: 升级 feature deliverables 到 D-17 ~ D-20
- **关联需求**: REQ-001 / REQ-014 / REQ-015
- **关联架构**: Section 3.2.1、Section 5.1
- **任务描述**: 扩展 feature index / card 模板与 renderer，输出 testability 聚合字段。
- **验收标准**:
  - [x] 索引新增 5 个测试化列
  - [x] 规格卡新增 D-17 ~ D-20 章节
  - [x] **异常路径验证**: 缺失项显式渲染为缺失，不默认成功
  - [x] **文档化标准合规**
- **预估工时**: 2h
- **状态**: 已完成

#### TASK-010-004: 升级 relation / gap / report 三条测试化交付链
- **关联需求**: REQ-002 / REQ-003 / REQ-008
- **关联架构**: Section 3.2.2、3.2.3、3.2.9
- **任务描述**: 让追踪矩阵支持测试链路、gap 支持 `gap_severity`，report 支持测试化摘要和 Step 12 / Step 13~16 边界。
- **验收标准**:
  - [x] 追踪矩阵包含 `feature_test_rows` 和 `rule_negative_test_rows`
  - [x] gap analysis 渲染 `gap_severity`
  - [x] report 输出 score / grade / blocked / partial / test_ready 摘要
  - [x] **异常路径验证**: DLV-011~014 pending 不阻塞 `07-review-report.md`
  - [x] **文档化标准合规**
- **预估工时**: 1.5h
- **状态**: 已完成

#### TASK-010-005: 新增 4 个 Step 13~16 renderer
- **关联需求**: REQ-009 / REQ-010 / REQ-011 / REQ-012
- **关联架构**: Section 3.2.4、Section 6.1
- **任务描述**: 新增 scorecard、test-case-index、fixture-contract、oracle-matrix 四个模板与脚本，并接入 `review_runner.py`。
- **验收标准**:
  - [x] 4 个 renderer 均可直接从 context 生成交付物
  - [x] manifest 状态可更新为 completed
  - [x] **异常路径验证**: project path 不存在时返回 failed
  - [x] **文档化标准合规**
- **预估工时**: 2h
- **状态**: 已完成

#### TASK-010-006: 校验、文档与迭代元数据收口
- **关联需求**: REQ-013
- **关联架构**: cross-cutting
- **任务描述**: 扩展自动化测试、更新 deliverable standard / skill 文档 / 010 迭代文档 / `.powerby/iterations.json`。
- **验收标准**:
  - [x] pb-review 相关测试全部通过
  - [x] validator 通过
  - [x] 010 `tasks.md` 与 `implementation-report.md` 补齐
  - [x] **异常路径验证**: 文档缺失会被测试或 validator 发现
  - [x] **文档化标准合规**
- **预估工时**: 1h
- **状态**: 已完成

## 4. 测试规格矩阵

| 测试点 ID | 关联需求 | 关联架构 | 任务ID | 测试策略 | 可量化成功标准 |
|----------|----------|----------|--------|---------|--------------|
| TC-010-001 | REQ-013 | Section 2 / 5.6 | TASK-010-001 / 002 | validator | schema、assets、renderers 全部存在 |
| TC-010-002 | REQ-014 / REQ-015 | Section 3.2.1 | TASK-010-003 | `pytest` | feature index/card 渲染 D-17 ~ D-20 |
| TC-010-003 | REQ-008 | Section 3.2.9 | TASK-010-004 | `pytest` | traceability matrix 输出测试链路 |
| TC-010-004 | REQ-002 | Section 3.2.2 | TASK-010-004 | `pytest` | gap analysis 输出 `gap_severity` |
| TC-010-005 | REQ-003 | Section 3.2.3 | TASK-010-004 | `pytest` | report composer 输出测试化摘要且不阻塞于 11~14 |
| TC-010-006 | REQ-009 ~ REQ-012 | Section 3.2.4 | TASK-010-005 | `pytest` | 4 个新交付物全部生成 |

## 5. Gate 5 / Gate 6 检查

- [x] 现有代码分析已完成
- [x] 所有 P0 功能都有对应开发任务
- [x] 任务分解粒度合适
- [x] 依赖关系清晰合理
- [x] 验收标准可验证
- [x] 异常路径覆盖完整
- [x] 技术方案决策有证据链
- [x] 函数复杂度控制规划已完成
- [x] 文档化标准已定义并执行
- [x] 自动化校验通过

## 6. 当前结论

- P5 已完成，采用“共享 schema + 既有 renderer 增量升级”方案。
- P6 已完成：010 范围内的代码、模板、schema、测试与迭代文档已落盘。
- 后续若进入 P7，重点应审查真实业务仓库上的抽取准确率，而不是结构存在性。
