# Proposal: ASP 文档协议升级

**迭代编号**: 011
**项目名称**: asp-document-upgrade
**创建日期**: 2026-03-30
**状态**: Final

---

## 1. 产品定位

- **目标用户**：
  - 主要：powerby-skills 项目维护者
  - 次要：未来使用 powerby-asp 流程的开发者
  - 下游：pb-review 的消费者

- **核心价值**：
  实现产品→功能→架构→实现→测试的全链路一致性验证，让 ASP 产出的文档能被 pb-review 零修改复用。

- **成功指标**：
  1. pb-review 可以零修改复用 ASP 产出的功能规格卡
  2. 三向对齐验证可以自动化执行
  3. 所有 powerby-asp-* skill 通过 skill-design-protocol.md 的十条核心原则 checklist

---

## 2. 需求清单

| ID | 需求描述 | 优先级 | 验收标准（草案） | 复用策略 |
|----|---------|--------|----------------|---------|
| REQ-001 | ASP 文档协议标准更新 | 必须 | 协议文档包含分阶段组装机制说明、feature-spec-index.md 替代 function-points.md 的说明 | 扩展现有 |
| REQ-002 | proposal.md 格式升级 | 必须 | proposal.md 包含"现有能力分析"和"复用策略"字段 | 扩展现有 |
| REQ-003 | feature-spec-index.md 替代 function-points.md | 必须 | feature-spec-index.md 包含 Feature ID、对应 REQ、功能类型、状态、Oracle/Fixture 完整度、测试组数 | 全新开发 |
| REQ-004 | feature-specs/*.md 分阶段组装机制 | 必须 | 每个功能有独立的 feature-specs/{feature-id}.md，产品阶段填充 D-01~D-08 + D-17~D-20 | 全新开发 |
| REQ-005 | traceability-matrix.md | 必须 | traceability-matrix.md 包含 REQ→Feature、Feature→Test 双向映射 | 全新开发 |
| REQ-006 | testability-scorecard.md | 必须 | testability-scorecard.md 包含 M-01~M-07 指标和综合评分 | 全新开发 |
| REQ-007 | 重写 powerby-asp-product | 必须 | powerby-asp-product SKILL.md 遵循 skill-design-protocol，并落盘为 11 section 标准结构，产出符合新协议的文档 | 重构现有 |
| REQ-008 | 重写 powerby-asp-reviewer | 必须 | powerby-asp-reviewer SKILL.md 遵循 skill-design-protocol，并落盘为 11 section 标准结构，审查新格式文档 | 重构现有 |
| REQ-009 | 重写 powerby-asp-codex-reviewer | 必须 | powerby-asp-codex-reviewer SKILL.md 遵循 skill-design-protocol，并落盘为 11 section 标准结构 | 重构现有 |
| REQ-010 | 重写 powerby-asp-visualizer | 必须 | powerby-asp-visualizer SKILL.md 遵循 skill-design-protocol，并落盘为 11 section 标准结构，生成新格式文档 | 重构现有 |
| REQ-011 | 重写 powerby-asp-architect | 必须 | powerby-asp-architect SKILL.md 遵循 skill-design-protocol，并落盘为 11 section 标准结构，补充 D-09~D-16 | 重构现有 |
| REQ-012 | 重写 powerby-asp-arch-reviewer | 必须 | powerby-asp-arch-reviewer SKILL.md 遵循 skill-design-protocol，并落盘为 11 section 标准结构 | 重构现有 |
| REQ-013 | 重写 powerby-asp-arch-codex-reviewer | 必须 | powerby-asp-arch-codex-reviewer SKILL.md 遵循 skill-design-protocol，并落盘为 11 section 标准结构 | 重构现有 |
| REQ-014 | 流程产出升级 | 必须 | 流程各阶段产出文档符合 asp-document-protocol.md | 扩展现有 |
| REQ-015 | 更新 asp-document-protocol.md | 必须 | 协议文档版本更新为 1.1.0，包含本轮讨论的所有变更 | 扩展现有 |

---

## 3. 明确排除

| ID | 排除项 | 排除理由 |
|----|--------|---------|
| EXC-001 | ASP 五阶段流程重构 | 流程如无必要不更新，只升级文档产物 |
| EXC-002 | pb-review skill 改造 | 不在本次范围，pb-review 已成熟 |
| EXC-003 | 自动化三向对齐验证脚本 | 本次只定义标准，自动化工具后续迭代 |
| EXC-004 | P0-P8 主流程的 skill 改造 | 只改造 powerby-asp-* 系列 |

---

## 4. 约束条件

| ID | 约束描述 | 影响范围 |
|----|---------|---------|
| CON-001 | 所有 skill 必须通过 skill-design-protocol.md 的十条核心原则 checklist | 所有 skill 改造 |
| CON-002 | 文档必须能被 pb-review 零修改复用 | 所有文档格式 |
| CON-003 | 分阶段组装：产品阶段不能填充架构信息，架构阶段不能修改产品信息 | feature-specs/*.md |
| CON-004 | 保持 ASP 五阶段流程不变 | 流程更新 |

---

## 5. 现有能力分析

### 5.1 已有功能

- `docs/asp-document-protocol.md`（v1.0.0）：已定义 7 个标准文档的协议
- 7 个 powerby-asp-* skill：已实现基础的 ASP 流程
- ASP 五阶段流程：DISCOVERY → DRAFTING → REFINING → VISUALIZING → CONFIRMATION

### 5.2 复用策略

| 现有能力 | 复用方式 | 说明 |
|---------|---------|------|
| asp-document-protocol.md | 扩展 | 更新为 v1.1.0，增加分阶段组装机制 |
| powerby-asp-product | 重构 | 保留核心逻辑，重写为 11 section 标准结构 |
| powerby-asp-reviewer | 重构 | 保留审查逻辑，重写为 11 section 标准结构 |
| powerby-asp-codex-reviewer | 重构 | 保留 Codex 调用逻辑，重写为 11 section 标准结构 |
| powerby-asp-visualizer | 重构 | 保留 Mermaid 生成逻辑，重写为 11 section 标准结构 |
| powerby-asp-architect | 重构 | 保留架构设计逻辑，重写为 11 section 标准结构 |
| powerby-asp-arch-reviewer | 重构 | 保留架构审查逻辑，重写为 11 section 标准结构 |
| powerby-asp-arch-codex-reviewer | 重构 | 保留 Codex 架构审查逻辑，重写为 11 section 标准结构 |
| ASP 五阶段流程 | 保持 | 流程不变，只升级文档产出格式 |

---

**文档状态**: Final
**阶段归属**: DISCOVERY 阶段锁定产物
