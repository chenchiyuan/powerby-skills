# Design Brief: ASP Office Hours 前置探讨集成

## 1. Session Metadata

- **迭代编号**: 012
- **模式**: Startup
- **日期**: 2026-03-30
- **状态**: Approved

## 2. Original User Input

- “我想参考gstack office-hours来做需求澄清和探讨”
- “落档的资料作为powerby-asp-product的前置数据输入”
- “先更新powerby-asp的整个流程，自然的加入前置产品设计和讨论”
- “不要限制用户的输入”
- “用户的原始输入，澄清的过程和最后的结论要写入文档”
- “沟通的过程尽可能的参照gstack的原始实现，能不修改尽量不修改”

## 3. Clarification Log

| 轮次 | 关键问题 | 用户回答/约束 | 结论修正 |
|------|---------|--------------|---------|
| 1 | 前置阶段要解决什么问题？ | 先把目标、验证方式、方向、成功标准聊清楚 | 新增独立前置阶段，不再让 `Discovery` 同时承担探讨和定稿 |
| 2 | 前置资料要保留到什么程度？ | 原始输入、过程、结论都很重要 | `design-brief.md` 必须同时保留原始输入、澄清过程、最终结论 |
| 3 | 与 gstack 的关系是什么？ | 尽量参考原始实现，能不改尽量不改 | 保留 `one question at a time`、`premise challenge`、`alternatives generation` 等核心骨架 |
| 4 | 前置阶段和 `proposal.md` 的关系？ | 作为 `powerby-asp-product` 的前置数据输入 | `design-brief.md` 是上游探讨证据源，`proposal.md` 仍是需求边界事实源 |

## 4. Problem Statement

当前 ASP 流程直接由 `Discovery` 产出 `proposal.md`，缺少一个正式的前置设计与澄清阶段。这会让“方向探讨”和“需求合同”混在一起，导致用户想法、验证目标和关键假设在后续文档里丢失。

## 5. Validation Goal

验证 ASP 是否能在合同化需求之前，先通过类似 gstack `office-hours` 的流程把问题、方向、验证方式和成功标准聊透，并把这些信息稳定落盘，供 `powerby-asp-product` 消费。

## 6. Target User and Status Quo

- **目标用户**: 想用 ASP 定义产品、但在写 `proposal.md` 前还需要探讨和澄清的维护者
- **现状**: 直接进入 `Discovery -> proposal.md`
- **现状代价**:
  - 前置讨论没有正式产物
  - `proposal.md` 同时承载探索和定稿，边界模糊
  - 后续 `feature-specs`、`architecture.md` 难以回看最初的验证目标和方向选择

## 7. Success Criteria

- ASP 标准流程显式包含 `OFFICE_HOURS`
- 存在 `design-brief.md` 标准协议
- `powerby-asp-product` 明确以 `design-brief.md` 为上游输入
- 新 skill 尽量保留 gstack 原始交互骨架
- 相关测试通过

## 8. Constraints and Non-goals

- 用户输入保持自由，不改造成固定问卷
- 不移植 gstack 的 telemetry、YC closing、全局配置逻辑
- 不让前置阶段直接产出 `proposal.md`、Feature 卡或架构文档
- 不改造 `pb-review`

## 9. Premises

1. 前置探讨和需求合同应该拆成两类文档，而不是混写在 `proposal.md` 中。
2. 用户更需要“逐步被引导澄清”，而不是一开始被要求填完整表单。
3. gstack `office-hours` 的核心价值来自交互骨架，不来自其外围产品化逻辑。

## 10. Alternatives Considered

### Approach A: 继续把探讨塞进 `powerby-asp-product`
- **优点**: 文件最少
- **缺点**: 单一职责被破坏，`proposal.md` 仍会混入探索痕迹

### Approach B: 新增 `powerby-asp-office-hours`
- **优点**: 与 gstack 最相似，边界最清晰，`design-brief.md -> proposal.md` 链路明确
- **缺点**: 新增一个 skill 和一类文档

## 11. Recommended Direction

选择 Approach B。因为这条路线能保住 gstack `office-hours` 的前置探讨价值，同时又不破坏 ASP 现有的合同化与规格化文档体系。

## 12. Handoff to Proposal

后续 `proposal.md` 必须继承：
- **目标摘要**: 在合同需求前先聊清目标、验证方式、方向和成功标准
- **验证方式**: 以 `design-brief.md` 为上游输入，而不是从模糊想法直接生成合同文档
- **关键约束**: 输入自由、过程落档、尽量保留 gstack 核心交互骨架
- **明确排除**: 不移植 gstack 外围逻辑，不让前置阶段直接产出 Feature/Architecture
