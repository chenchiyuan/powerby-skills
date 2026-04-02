# 开发任务计划

**迭代编号**: 012
**创建日期**: 2026-03-30
**生命周期阶段**: P5 - 开发规划 / P6 - 开发实现

---

## 1. 需求与实现对齐

### 核心目标复述
- 在现有 ASP 协议上新增 `OFFICE_HOURS` 前置阶段。
- 增加 `design-brief.md` 作为 `proposal.md` 的正式上游输入。
- 新增 `powerby-asp-office-hours` skill，并收窄 `powerby-asp-product` 的职责。

### 范围边界
- **本次实现（P0）**: 协议升级到 `v1.2.0`、新增 `powerby-asp-office-hours`、更新 `powerby-asp-product`、补充 012 文档与测试。
- **明确排除**: 改造 `pb-review`、重写架构线 skill、移植 gstack 的 telemetry/YC closing。

### 成功标准
- [x] `docs/asp-document-protocol.md` 升级为 `v1.2.0`
- [x] `skills/powerby-asp-office-hours/` 落盘并符合 11 section 结构
- [x] `skills/powerby-asp-product/SKILL.md` 明确消费 `design-brief.md`
- [x] `pytest` 覆盖新版协议与 skill 边界

## 2. 技术方案

### 方案 A：把 office-hours 逻辑直接塞回 product skill
- **优点**: 文件最少
- **缺点**: 前置探讨与合同化需求重新混在一起，违反单一职责

### 方案 B：新增 `powerby-asp-office-hours`，`powerby-asp-product` 只负责收敛
- **优点**: 边界清晰，最接近 gstack 的前置设计模式
- **缺点**: 新增一个 skill 和一类文档

### 我的建议
- **推荐方案**: 方案 B
- **原因**: 它最符合 `skill-design-protocol.md` 的单一职责，也最符合用户要求的“尽量保持 gstack 原实现骨架”。

## 3. 任务清单

### TASK-012-001: 升级 ASP 协议到 v1.2.0
- **关联需求**: REQ-001 / REQ-002
- **验收标准**:
  - [x] 协议版本更新为 `1.2.0`
  - [x] 文档清单新增 `design-brief.md`
  - [x] 流程阶段新增 `OFFICE_HOURS`
  - [x] `proposal.md` 协议包含 `Upstream Design Input`
- **状态**: 已完成

### TASK-012-002: 新增 `powerby-asp-office-hours`
- **关联需求**: REQ-003 / REQ-005
- **验收标准**:
  - [x] skill 为 11 section 结构
  - [x] 输出 `design-brief.md`
  - [x] reference 明确保留 gstack 核心骨架和 ASP 化差异
- **状态**: 已完成

### TASK-012-003: 重构 `powerby-asp-product`
- **关联需求**: REQ-004
- **验收标准**:
  - [x] Discovery Mode 首选读取 `design-brief.md`
  - [x] 缺失 `design-brief.md` 时显式回退到 `powerby-asp-office-hours`
  - [x] 不再声称从模糊输入直接完成完整需求探究
- **状态**: 已完成

### TASK-012-004: 补充 012 文档与测试
- **关联需求**: REQ-006
- **验收标准**:
  - [x] 012 proposal/tasks/implementation-report 落盘
  - [x] `pytest` 断言新版协议和 skill 边界
- **状态**: 已完成

## 4. 测试矩阵

| 测试点 ID | 关联需求 | 验收标准 |
|----------|----------|----------|
| TC-012-001 | REQ-001 / REQ-002 | 协议版本为 `1.2.0`，且包含 `design-brief.md` 与 `OFFICE_HOURS` |
| TC-012-002 | REQ-003 / REQ-005 | `powerby-asp-office-hours` 为 11 section 结构，且包含 gstack 核心骨架术语 |
| TC-012-003 | REQ-004 | `powerby-asp-product` Discovery Mode 明确消费 `design-brief.md` |
| TC-012-004 | REQ-006 | 012 迭代文档存在且实现报告记录测试执行 |

## 5. Gate 检查

- [x] 方案已明确
- [x] 范围边界已收敛
- [x] 任务与验收标准可验证
- [x] 实现已完成
- [x] 测试已执行
