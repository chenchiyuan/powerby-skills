# pb-review 交付物标准

**版本**: 2.0.0  
**制定日期**: 2026-03-27  
**适用范围**: `pb-review` 主流程及全部 `pb-review-*` 下游 skill

---

## 1. 目标

本标准用于解决 `pb-review` 当前交付物过粗的问题。

旧问题主要有三类：

1. 只有总报告，没有分层中间产物
2. 功能层只停留在功能列表，没有落到“可验证的功能规格卡”
3. 交付文件命名、粒度、责任边界不统一，导致不同项目之间不可比较

本标准要求 `pb-review` 从“还原结论”升级为“标准化交付物流水线”。

---

## 2. 核心原则

### P-01 交付物优先

`pb-review` 的目标不是给出一段总结，而是生成一组可审阅、可追踪、可复用的交付物。

### P-02 功能规格卡是原子交付单元

Operation 级能力必须落成独立的功能规格卡，不能只出现在汇总表里。

### P-03 一层一文档，一文档一职责

每个交付文档只负责一个层级或一个主题：

- 系统上下文
- 产品对象目录
- 功能规格索引
- 功能规格卡
- 追踪矩阵
- 差异与缺口
- 最终总报告

### P-04 所有结论都要可回溯

每个功能规格卡、追踪关系、gap 都必须能回溯到 evidence、对象 ID 或关系 ID。

### P-05 抽象判断必须显式留痕

如果存在 `inferred` 判断，必须标注置信度和证据来源；不允许把推断伪装成显式事实。

### P-06 交付层与存储层分离

`JSON registry` 是机器可恢复层，`Markdown deliverables` 是人类可审阅层。二者缺一不可。

### P-07 命名与路径固定

所有交付文档路径必须固定，避免每次评审输出都长得不一样。

### P-08 模板渲染下沉到 skill 资源层

当某类交付物是固定模板、重复性强的 Markdown 产物时，应由 skill 自带 renderer script 负责落盘。宿主模型负责抽象判断与结构化结果，不负责重复拼接模板细节。

---

## 3. 与功能规格定义标准的关系

`pb-review` 的功能层交付必须遵循 [feature-specification-standard.md](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)。

具体要求如下：

1. `Operation` 级功能必须生成独立功能规格卡
2. 功能规格卡必须以 `D-01` 到 `D-08` 为必填维度
3. `D-09` 到 `D-14` 为质量属性扩展维度
4. `D-15` 依赖关系、`D-16` 实现映射为 `pb-review` 推荐扩展维度
5. 每张卡片必须包含验证方式，而不是只写“功能描述”
6. 功能 ID 必须遵循标准命名规范

---

## 4. 必备交付物

所有完整的 `pb-review` 必须产出以下文档：

| 交付物 ID | 文档路径 | 责任 skill | 最低要求 |
|---|---|---|---|
| DLV-001 | `.review/deliverables/01-system-context.md` | `pb-review-project-scope` | 项目边界、评审范围、文档边界、证据面摘要 |
| DLV-002 | `.review/deliverables/02-product-catalog.md` | `pb-review-product-reconstructor` | Goal / Role / Scenario / Constraint / Non-goal 目录 |
| DLV-003 | `.review/deliverables/03-feature-spec-index.md` | `pb-review-feature-reconstructor` | Domain / Module / Operation 索引与状态概览 |
| DLV-004 | `.review/deliverables/04-feature-specs/{function_id}.md` | `pb-review-feature-reconstructor` | 每个 Operation 的独立功能规格卡 |
| DLV-005 | `.review/deliverables/05-traceability-matrix.md` | `pb-review-relation-builder` | Goal→Feature、Rule→Feature 双向追踪矩阵 |
| DLV-006 | `.review/deliverables/06-gap-analysis.md` | `pb-review-gap-analyzer` | difference、gap、残留 conflict 的结构化分析 |
| DLV-007 | `.review/deliverables/07-review-report.md` | `pb-review-report-composer` | 总结性总报告，必须引用前述交付物 |
| DLV-008 | `.review/deliverables/08-architecture-layered.md` | `pb-review-architecture-builder` | 业务域划分、运行层分层、关键编排链路 |
| DLV-009 | `.review/deliverables/09-dependency-matrix.md` | `pb-review-dependency-reconstructor` | Feature→Feature / External / Data Object 依赖矩阵与依赖图 |
| DLV-010 | `.review/deliverables/10-data-flow.md` | `pb-review-data-flow-builder` | 数据对象生产/消费链路、存储位置、Mermaid 数据流图 |
| DLV-011 | `.review/deliverables/11-testability-scorecard.md` | `pb-review` | M-01~M-07 当前值、目标值、差距、等级判定 |
| DLV-012 | `.review/deliverables/12-test-case-index.md` | `pb-review` | Feature→Test Case Groups 现状、理想组清单、缺口优先级 |
| DLV-013 | `.review/deliverables/13-test-fixture-contract.md` | `pb-review` | D-18 Fixture 现状、理想 Fixture 清单、Mock/Stub 建议 |
| DLV-014 | `.review/deliverables/14-test-oracle-matrix.md` | `pb-review` | D-17 Oracle 现状、理想 Oracle 清单、缺失项矩阵 |

---

## 5. 必备 registry

所有完整的 `pb-review` 必须产出以下 JSON 层：

| registry | 文件路径 | 用途 |
|---|---|---|
| `project_metadata` | `.review/project_metadata.json` | 项目边界与资源盘点 |
| `evidence_registry` | `.review/evidence_registry.json` | 标准化证据单元 |
| `current_facts` | `.review/current_facts.json` | 冲突决议后的当前有效事实 |
| `object_registry` | `.review/object_registry.json` | 产品与功能对象 |
| `feature_spec_registry` | `.review/feature_spec_registry.json` | 功能规格卡的结构化数据 |
| `feature_state_registry` | `.review/feature_state_registry.json` | 功能状态 |
| `traceability_matrix` | `.review/traceability_matrix.json` | 追踪矩阵结构化数据 |
| `relation_registry` | `.review/relation_registry.json` | 关系记录 |
| `conflict_registry` | `.review/conflict_registry.json` | 冲突记录 |
| `difference_registry` | `.review/difference_registry.json` | 差异记录 |
| `gap_registry` | `.review/gap_registry.json` | 缺口记录 |
| `deliverable_manifest` | `.review/deliverable_manifest.json` | 全部交付物路径、状态、责任方清单 |
| `dependency_registry` | `.review/dependency_registry.json` | 功能依赖、外部依赖、数据依赖记录 |
| `implementation_registry` | `.review/implementation_registry.json` | Feature→Entry / Service / Model / Test / Config 映射 |
| `architecture_registry` | `.review/architecture_registry.json` | 分层架构、业务域、关键链路摘要 |
| `data_flow_registry` | `.review/data_flow_registry.json` | 数据对象、生产者、消费者、存储与生命周期 |

---

## 6. 功能规格卡要求

每个 `Operation` 级功能规格卡必须：

1. 文件名等于 `function_id`
2. 存放在 `.review/deliverables/04-feature-specs/`
3. 使用固定章节顺序
4. 每个章节尽量引用 `evidence_id`
5. 显式说明验证方式

推荐最小章节如下：

```markdown
# {function_id} {function_name}

## 基本信息
## 功能描述
## D-01 功能标识
## D-02 输入规格
## D-03 前置条件
## D-04 正常输出
## D-05 异常行为
## D-06 边界值
## D-07 后置条件
## D-08 副作用
## 扩展维度
## D-15 依赖关系
## D-16 实现映射
## D-17 Test Oracle
## D-18 Fixture Contract
## D-19 Test Case Groups
## D-20 Coverage Claim
## 测试化状态
## 验证映射
## 证据引用
```

---

## 7. 交付顺序

完整流程必须按以下顺序产出交付物：

1. `01-system-context.md`
2. `02-product-catalog.md`
3. `03-feature-spec-index.md`
4. `04-feature-specs/*.md`
5. `05-traceability-matrix.md`
6. `06-gap-analysis.md`
7. `08-architecture-layered.md`
8. `09-dependency-matrix.md`
9. `10-data-flow.md`
10. `07-review-report.md`
11. `11-testability-scorecard.md`
12. `12-test-case-index.md`
13. `13-test-fixture-contract.md`
14. `14-test-oracle-matrix.md`

禁止跳过中间交付物后直接写最终报告。

---

## 8. 最终报告约束

`07-review-report.md` 不允许重复替代前面所有交付物。

它的职责是：

1. 汇总关键结论
2. 引用交付物
3. 提供审阅入口
4. 解释高风险 gap

它不负责：

1. 重新发明功能规格卡
2. 重新定义追踪矩阵
3. 隐藏 conflict 或 gap

---

## 9. 验收标准

一次完整 `pb-review` 只有在以下条件全部满足时，才能被视为“交付合格”：

- [ ] 所有必备 registry 已落盘
- [ ] 所有必备 Markdown deliverable 已生成
- [ ] 每个 Operation 级能力都有功能规格卡
- [ ] 功能规格卡符合 `feature-specification-standard.md`
- [ ] 追踪矩阵至少覆盖 Goal→Feature、Rule→Feature、Feature→Feature
- [ ] gap 分析明确区分 difference / gap / conflict
- [ ] 分层架构文档清晰区分功能层级与运行层分层
- [ ] 数据流图明确列出核心数据对象的生产者与消费者
- [ ] 最终报告引用前述交付物，而不是替代它们

---

## 10. 不合格输出示例

以下输出都应被视为不合格：

1. 只有一份 `review_report.md`
2. 只有功能列表，没有功能规格卡
3. 有功能规格卡，但没有验证方式
4. 有追踪矩阵，但没有规则 / 目标双向链路
5. gap 只有“感觉没做完”，没有证据和上下文
6. 用 README 或代码行为直接脑补产品目标
