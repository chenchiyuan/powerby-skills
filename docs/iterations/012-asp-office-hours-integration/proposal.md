# Proposal: ASP Office Hours 前置探讨集成

**迭代编号**: 012
**项目名称**: asp-office-hours-integration
**创建日期**: 2026-03-30
**状态**: Final

---

## 1. 产品定位

- **目标用户**：
  - 主要：使用 ASP 流程定义产品的项目维护者
  - 次要：需要先聊清方向再锁定需求的产品/工程负责人
  - 下游：`powerby-asp-product`

- **核心价值**：
  在 ASP 的合同化需求之前增加一个参照 gstack `office-hours` 的前置探讨阶段，把产品目标、验证方式、方向取舍和成功标准先聊透，再进入 `proposal.md`。

- **成功指标**：
  1. ASP 流程正式包含 `OFFICE_HOURS` 阶段和 `design-brief.md`
  2. `powerby-asp-product` 不再从模糊输入直接生成 `proposal.md`
  3. `design-brief.md` 能保留原始输入、关键澄清过程和最终结论

## 2. 需求清单

| ID | 需求描述 | 优先级 | 验收标准（草案） | 复用策略 |
|----|---------|--------|----------------|---------|
| REQ-001 | 新增 `OFFICE_HOURS` 前置阶段 | 必须 | ASP 协议与流程图显式包含 `OFFICE_HOURS -> DISCOVERY -> DRAFTING -> DESIGNING -> REFINING -> VISUALIZING -> CONFIRMATION` | 扩展现有 |
| REQ-002 | 新增 `design-brief.md` 协议 | 必须 | 协议文档定义 `design-brief.md` 的定位、必填章节和 handoff 要求 | 全新开发 |
| REQ-003 | 新增 `powerby-asp-office-hours` skill | 必须 | skill 遵循 `skill-design-protocol.md` 的 11 section 结构，并输出 `design-brief.md` | 全新开发 |
| REQ-004 | `powerby-asp-product` 消费 `design-brief.md` | 必须 | Discovery Mode 缺少 `design-brief.md` 时回退到前置探讨，存在时收敛为 `proposal.md` | 重构现有 |
| REQ-005 | 尽量保持 gstack 原始交互骨架 | 必须 | skill 中明确保留 `one question at a time`、`premise challenge`、`alternatives generation` | 借鉴现有 |
| REQ-006 | 交付测试覆盖新版协议与 skill 路由 | 必须 | `pytest` 能校验 `v1.2.0` 协议、新 skill、产品 skill 的前置输入约束 | 扩展现有 |

## 3. 明确排除

| ID | 排除项 | 排除理由 |
|----|--------|---------|
| EXC-001 | 重写 gstack `office-hours` 全量实现 | 只适配核心交互骨架与文档契约 |
| EXC-002 | 改造 `pb-review` 与架构线审查协议 | 本次只更新 ASP 前置产品流程 |
| EXC-003 | 在前置阶段直接产出 Feature 卡或架构文档 | 保持阶段边界清晰 |

## 4. 约束条件

| ID | 约束描述 | 影响范围 |
|----|---------|---------|
| CON-001 | skill 设计必须符合 `docs/skill-design-protocol.md` | 新增与重构 skill |
| CON-002 | 用户输入保持自由，不改造成固定表单 | `powerby-asp-office-hours` |
| CON-003 | 原始输入、澄清过程、最终结论必须可追溯 | `design-brief.md` |
| CON-004 | `proposal.md` 仍然是需求边界的单一事实源 | 协议与 product skill |

## 5. 现有能力分析

### 5.1 已有功能

- `docs/asp-document-protocol.md` v1.1.0：已支持 `proposal.md`、`feature-spec-index.md`、`feature-specs/*.md`
- `skills/powerby-asp-product/SKILL.md`：当前 Discovery 直接生成 `proposal.md`
- `/Users/chenchiyuan/projects/gstack/office-hours/SKILL.md`：提供前置探讨的成熟交互骨架

### 5.2 复用策略

| 现有能力 | 复用方式 | 说明 |
|---------|---------|------|
| ASP 协议 v1.1.0 | 扩展 | 升级为 v1.2.0，新增前置探讨层 |
| `powerby-asp-product` | 重构 | 收窄为“Brief -> Proposal” 收敛器 |
| gstack `office-hours` | 借鉴 | 尽量保留对话骨架，移除与 ASP 无关的外围逻辑 |

---

**文档状态**: Final
**阶段归属**: DISCOVERY 阶段锁定产物
