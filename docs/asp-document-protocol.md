# ASP 文档协议标准

**版本**: 1.2.0
**制定日期**: 2026-03-30
**适用范围**: powerby-asp 全流程及所有 `powerby-asp-*` 子 skill
**参考标准**:
- `docs/review/feature-specification-standard.md`
- `docs/review/pb-review-standard.md`
- `docs/review/pb-review-deliverable-standard.md`
- `docs/skill-design-protocol.md`
- `/Users/chenchiyuan/projects/gstack/office-hours/SKILL.md`

---

## 1. 协议目标

本协议定义 powerby-asp 流程的标准文档集合，确保：

1. ASP 产出可被 `pb-review` 零修改复用。
2. 从产品方向探讨到 Feature、架构和测试信息可双向追溯。
3. 前置探讨、产品合同、规格卡与架构阶段边界清晰，不互相污染。
4. 所有 skill 在同一组文档契约上协同工作。

## 2. 核心原则

### P-01 协议先行
先定义字段、结构、边界，再生成文档内容。

### P-02 双层事实源
- `design-brief.md` 是前置产品探讨与澄清证据的单一事实源。
- `proposal.md` 是需求边界的单一事实源。
- `feature-spec-index.md` 是 Feature 编号与状态索引的单一事实源。
- `feature-specs/*.md` 是原子功能规格的单一事实源。
- `architecture.md` 是架构设计的单一事实源。

### P-03 结构化优先
优先使用固定章节、表格、枚举值和稳定编号，不使用不可追溯的自由文本。

### P-04 前置探讨先于合同锁定
- 先通过 `OFFICE_HOURS` 澄清问题、目标、验证方式、关键假设与方向取舍。
- 再通过 `DISCOVERY` 将结论收敛为 `proposal.md`。
- `OFFICE_HOURS` 不替代 `proposal.md`，只为其提供上游证据和 handoff。

### P-05 分阶段组装
- `OFFICE_HOURS` 只负责 `design-brief.md`。
- 产品阶段只负责 `proposal.md`、`feature-spec-index.md`、`D-01~D-08` 与 `D-17~D-20`。
- 架构阶段只负责 `D-09~D-16` 与 `architecture.md`。
- 架构阶段不得回写产品阶段已锁定内容。

### P-06 追溯强制
每张规格卡都必须能追溯到 `REQ`、测试组、依赖关系和实现映射；`proposal.md` 应可回溯到 `design-brief.md` 的结论与验证目标。

### P-07 测试化内建
每张规格卡必须内建 `D-17 Test Oracle`、`D-18 Fixture Contract`、`D-19 Test Case Groups`、`D-20 Coverage Claim`。

## 3. 文档体系

### 3.1 文档清单

| 文档 ID | 文档路径 | 生成阶段 | 对应 pb-review 标准 | 职责 |
|---------|---------|---------|-------------------|------|
| ASP-000 | `design-brief.md` | OFFICE_HOURS | 前置探索记录 | 原始输入、澄清过程、问题定义、验证方式、方案比较、推荐方向 |
| ASP-001 | `proposal.md` | DISCOVERY | DLV-002 产品目录 | 需求清单、排除项、约束条件、现有能力分析 |
| ASP-002 | `feature-spec-index.md` | DRAFTING | DLV-003 功能规格索引 | Feature 索引、状态和测试化完整度 |
| ASP-003 | `feature-specs/{feature-id}.md` | DRAFTING + DESIGNING | DLV-004 功能规格卡 | 分阶段组装的 `D-01~D-20` 规格卡 |
| ASP-004 | `prd_logs/round-{N}-{reviewer}.md` | REFINING | 审查归档 | 产品文档审查报告 |
| ASP-005 | `product-map.md` | VISUALIZING | 可视化全景图 | Mermaid 功能树、核心旅程、决策摘要 |
| ASP-006 | `traceability-matrix.md` | VISUALIZING | DLV-005 追溯矩阵 | `REQ → Feature → Test` 双向追溯 |
| ASP-007 | `testability-scorecard.md` | VISUALIZING | DLV-011 测试化评分 | `M-01~M-07` 测试化评分 |
| ASP-008 | `architecture.md` | DESIGNING | 架构设计交付物 | 架构组件、协议、边界和实现映射 |
| ASP-009 | `arch_logs/round-{N}-{reviewer}.md` | REVIEWING | 架构审查归档 | 架构审查报告 |

### 3.2 文档依赖关系

```text
design-brief.md
    ↓
proposal.md
    ↓
feature-spec-index.md
    ↓
feature-specs/*.md
    ↓
architecture.md + feature-specs/*.md(D-09~D-16)
    ↓
product-map.md + traceability-matrix.md + testability-scorecard.md
```

### 3.3 标准流程阶段

```text
OFFICE_HOURS
    ↓
DISCOVERY
    ↓
DRAFTING
    ↓
DESIGNING
    ↓
REFINING
    ↓
VISUALIZING
    ↓
CONFIRMATION
```

## 4. `feature-spec-index.md` 替代说明

`feature-spec-index.md` 正式替代旧的功能点清单，原因如下：

1. 它不仅记录功能项，还记录状态、Oracle 完整度、Fixture 完整度和测试组数。
2. 它与 `feature-specs/{feature-id}.md` 一一对应，天然支持原子规格卡。
3. 它可以直接被 reviewer、visualizer、architect 作为统一输入索引使用。
4. 它的字段语义直接对齐 `pb-review` 的 `DLV-003` / `DLV-004`。

## 5. 前置探讨与分阶段组装机制

### 5.1 `OFFICE_HOURS` 阶段

`OFFICE_HOURS` 阶段必须：
- 接受自由输入，不要求用户先按固定字段回答。
- 参照 gstack `office-hours` 的原始交互骨架做一问一答式引导。
- 输出 `design-brief.md`，同时保留原始输入、关键澄清过程与最终结论。

`OFFICE_HOURS` 阶段禁止：
- 直接产出 `proposal.md`
- 直接定义 Feature 卡
- 直接下沉到架构实现

### 5.2 产品阶段

产品阶段必须输出：
- `proposal.md`
- `feature-spec-index.md`
- `feature-specs/*.md` 中的 `D-01~D-08`
- `feature-specs/*.md` 中的 `D-17~D-20`

产品阶段必须遵守：
- `Discovery Mode` 以 `design-brief.md` 为首选上游输入。
- 若缺少 `design-brief.md` 且用户意图仍处于探讨阶段，应先回到 `OFFICE_HOURS`。

产品阶段禁止输出：
- `D-09~D-16`
- `architecture.md`
- 任何实现细节、部署策略或架构结论

### 5.3 架构阶段

架构阶段必须输出：
- `architecture.md`
- `feature-specs/*.md` 中的 `D-09~D-16`
- `arch_logs/`

架构阶段禁止修改：
- `design-brief.md`
- `proposal.md`
- `feature-specs/*.md` 中的 `D-01~D-08`
- `feature-specs/*.md` 中的 `D-17~D-20`

### 5.4 违规判定

出现以下任一情况，应视为协议违规：
- 缺少 `design-brief.md` 却把未澄清内容直接写入 `proposal.md`
- `design-brief.md` 未保留原始输入、澄清过程或最终推荐方向
- 产品阶段提前填写 `D-09~D-16`
- 架构阶段回写产品阶段维度
- visualizer 输出与索引或规格卡不一致
- 任何 skill 重新依赖旧的规格文档集作为主输入

## 6. `design-brief.md` 协议

### 6.1 定位

`design-brief.md` 是 `OFFICE_HOURS` 阶段的标准产物，记录产品方向探讨过程与阶段性结论，作为 `proposal.md` 的前置输入。

### 6.2 必填章节

```markdown
# Design Brief: {项目名称}

## 1. Session Metadata
## 2. Original User Input
## 3. Clarification Log
## 4. Problem Statement
## 5. Validation Goal
## 6. Target User and Status Quo
## 7. Success Criteria
## 8. Constraints and Non-goals
## 9. Premises
## 10. Alternatives Considered
## 11. Recommended Direction
## 12. Handoff to Proposal
```

### 6.3 关键要求

- `Original User Input` 应尽量保留用户原话，不做过度改写。
- `Clarification Log` 至少记录关键问题、用户回答、理解修正与未决问题。
- `Alternatives Considered` 至少包含 2 个方向，其中 1 个为最小可验证路线。
- `Recommended Direction` 必须解释为何推荐，而不是只给结论。
- `Handoff to Proposal` 必须明确后续 `proposal.md` 应继承的目标、验证方式、指标、排除项与约束。

## 7. `proposal.md` 协议

### 7.1 定位

`proposal.md` 是 `DISCOVERY` 阶段的合同级文档，定义需求边界、排除项、约束与复用策略。

### 7.2 必填章节

```markdown
# Proposal: {项目名称}

## 0. Upstream Design Input
- **来源文档**: design-brief.md
- **目标摘要**
- **验证方式**
- **推荐方向**

## 1. 产品定位
- **目标用户**
- **核心价值**
- **成功指标**

## 2. 需求清单
| ID | 需求描述 | 优先级 | 验收标准（草案） | 复用策略 |

## 3. 明确排除
| ID | 排除项 | 排除理由 |

## 4. 约束条件
| ID | 约束描述 | 影响范围 |

## 5. 现有能力分析
### 5.1 已有功能
### 5.2 复用策略
```

## 8. `feature-spec-index.md` 协议

### 8.1 定位

功能规格索引，负责 Feature 编号、状态和测试化完整度管理。

### 8.2 必填章节

```markdown
# 功能规格索引

## 1. 功能概览
| Feature ID | 功能名称 | 对应 REQ | 功能类型 | 状态 | Oracle 完整度 | Fixture 完整度 | 测试组数 |

## 2. 状态统计

## 3. 功能分组
### 3.1 按优先级
### 3.2 按功能类型

## 4. 追溯矩阵（简化版）
```

## 9. `feature-specs/{feature-id}.md` 协议

### 9.1 定位

每个 Feature 的完整规格卡，遵循 `feature-specification-standard.md` 的 `D-01~D-20` 模型。

### 9.2 最小骨架

```markdown
# FT-XXX: {功能名称}
## 基本信息
## D-01: 功能标识
## D-02: 输入规格
## D-03: 前置条件
## D-04: 正常输出
## D-05: 异常行为
## D-06: 边界值
## D-07: 后置条件
## D-08: 副作用
## D-17: Test Oracle
## D-18: Fixture Contract
## D-19: Test Case Groups
## D-20: Coverage Claim
## D-09: 性能要求
## D-10: 安全要求
## D-11: 并发要求
## D-12: 数据一致性
## D-13: 可观测性
## D-14: 部署约束
## D-15: 依赖关系
## D-16: 实现映射
```

## 10. 审查报告协议

产品审查与架构审查分别落盘到 `prd_logs/`、`arch_logs/`，但报告契约统一：

```markdown
# ASP {Spec|Architecture} Audit Report

**Reviewer**: {Claude|Codex}
**Round**: {N}
**Audit Date**: {YYYY-MM-DD}
**Status**: {PASS|FAIL}

## Previous Rounds Summary
## 1. 宪法符合性检查
## 2. 双向覆盖检查
## 3. 逻辑自洽性检查
## 4. 问题清单
### 4.1 BLOCKER
### 4.2 MAJOR
### 4.3 MINOR
## 5. 审查结论
```

## 11. 可视化与测试化协议

### 11.1 `product-map.md`
- 包含功能全景树
- 包含核心旅程
- 包含裁剪和风险摘要

### 11.2 `traceability-matrix.md`
- 包含 `REQ → Feature` 映射
- 包含 `Feature → Test` 映射
- 包含覆盖率统计和未覆盖项

### 11.3 `testability-scorecard.md`
- 包含 `M-01~M-07`
- 包含综合评分和等级
- 包含差距分析与改进建议

## 12. 统一质量门禁

- [ ] 协议版本为 `1.2.0`
- [ ] 标准流程包含 `OFFICE_HOURS`
- [ ] `design-brief.md`、`proposal.md`、`feature-spec-index.md`、`feature-specs/*.md` 职责清晰
- [ ] 不再依赖旧的规格文档集作为主协议
- [ ] 所有 skill 输出都能映射到本协议定义的文档
- [ ] `proposal.md` 能回溯到 `design-brief.md` 的关键结论
- [ ] 所有规格卡满足分阶段组装边界
