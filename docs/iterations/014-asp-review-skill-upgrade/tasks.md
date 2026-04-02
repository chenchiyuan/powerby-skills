# 开发任务计划

**迭代编号**: 014  
**分支**: review  
**创建日期**: 2026-03-31  
**生命周期阶段**: P5 - 开发规划 / P6 - 开发实现

---

## 1. 需求与实现对齐

### 核心目标复述

- 基于 014 的 `proposal.md`、`architecture.md`、`feature-spec-index.md`、`feature-specs/*.md`，交付一个全新独立的五阶段 review skill。
- 新 skill 命名为 `pb-review-v2`，目录固定为 `skills/pb-review-v2/`。
- 本次实现不改造现有 `pb-review/`、`powerby-asp-reviewer/`、`powerby-asp-arch-reviewer/`，保持旧体系稳定。

### 范围边界

- **本次实现（P0）**:
  - 新增 `skills/pb-review-v2/` 与完整 `references/` 策略层
  - 新增 `docs/asp-review-orchestrator-protocol.md`
  - 将 014 的实现锚点、规格映射与追溯文档同步到 `pb-review-v2`
  - 新增 `tests/test_pb_review_v2.py`
  - 修正 `.github/workflows/scripts/validate-iteration-docs.py` 与 CI 文档校验入口
- **明确排除**:
  - 不重写旧 reviewer skill
  - 不新增独立 orchestrator skill
  - 不让 reviewer 直接修改被审查文档
  - 不与现有 `pb-review` 共享脚本、registry 或 data model

### 成功标准

- [x] `pb-review-v2` 作为独立 skill 落盘，且符合 11 section 结构
- [x] `references/` 包含 5 阶段 checklist、`decision-table.md`、`audit-template.md`
- [x] `docs/asp-review-orchestrator-protocol.md` 定义 reviewer -> fixer -> reviewer I/O 契约
- [x] 014 文档的实现锚点已切换到 `skills/pb-review-v2/`
- [x] pytest 覆盖新 skill、协议文档和 ASP/legacy 文档校验兼容性

## 1.3 现有代码分析报告

### 现有组件清单

| 组件名称 | 路径 | 职责 | 复用可能性 | 结论 |
|---------|------|------|-----------|------|
| `pb-review` | `skills/pb-review/` | 还原式项目评审编排框架 | 低 | 名称近似但职责不同，保持隔离 |
| `powerby-asp-reviewer` | `skills/powerby-asp-reviewer/SKILL.md` | ASP 产品线审查 | 中 | 仅参考结构，不直接修改 |
| `powerby-asp-arch-reviewer` | `skills/powerby-asp-arch-reviewer/SKILL.md` | ASP 架构线审查 | 中 | 仅参考结构，不直接修改 |
| `tests/test_asp_document_upgrade.py` | `tests/test_asp_document_upgrade.py` | 文档合同回归测试 | 高 | 沿用 pytest + 文本断言模式 |
| 迭代文档校验脚本 | `.github/workflows/scripts/validate-iteration-docs.py` | 迭代文档校验 | 高 | 需要升级为兼容 ASP / legacy 双模型 |

### 编码规范总结

- 主体资产仍然是 Markdown skill 文档、references 配置和 pytest 文本断言。
- Python 新增逻辑保持 PEP 257 docstring 和 fail-fast 错误消息。
- 新 skill 不创建 `scripts/`，只保留 `SKILL.md` 与 `references/`。

### 复用建议

- **可直接复用**:
  - 11 section skill 布局
  - pytest 文本断言模式
  - 现有 ASP 审查清单中的三维检查口径
- **需全新开发**:
  - `skills/pb-review-v2/`
  - `docs/asp-review-orchestrator-protocol.md`
  - `tests/test_pb_review_v2.py`
  - ASP / legacy 双模型文档校验逻辑

## 1.5 文档风格定义

- Markdown 文档继续使用表格、标题层级和 fenced code block。
- Python 公共函数必须带 docstring，说明输入、失败条件和返回值。
- 测试命名使用 `test_pb_review_v2_*`，直接表达被验证的合同。

## 2. 技术方案决议

### 已确认方案

- **方案名称**: 独立新增 `pb-review-v2`
- **决议来源**: 用户明确指示“严格按照架构和初衷来，这次实现是独立新增新的 skill，不影响之前的架构”，并指定命名为 `pb-review-v2`。

### 证据链

- **证据 1**: `proposal.md` 明确要求“全新独立体系，与 pb-review 并行”。
- **证据 2**: 仓库已存在 `skills/pb-review/`，无法复用同名目录而不破坏旧体系。
- **证据 3**: 用户明确要求“独立新增，不影响之前的架构”，因此不能继续沿用“改造 `powerby-asp-reviewer`”路线。

### 结论

- 实现以 `skills/pb-review-v2/` 为唯一新增 skill 入口。
- 旧 reviewer 体系不动，只保留文档级引用背景。

## 3. 开发任务清单

### P0 核心功能

#### TASK-014-001: 新增独立 skill `pb-review-v2`
- **关联需求**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-006
- **验收标准**:
  - [x] `skills/pb-review-v2/SKILL.md` 存在
  - [x] 明确五阶段识别、上游链恢复、Alignment Summary、Decision Summary、Review Result
  - [x] **异常路径验证**: `round > 3` 时强制 `ESCALATED`
  - [x] **文档化标准合规**: 11-section 结构完整
- **状态**: 已完成

#### TASK-014-002: 补齐 references 策略层
- **关联需求**: REQ-005, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-016, REQ-017
- **验收标准**:
  - [x] 补齐 `product/spec/arch/plan/impl` checklist
  - [x] 补齐 `decision-table.md`
  - [x] 补齐 `audit-template.md`
  - [x] **异常路径验证**: 证据不足时只能 `ASK`
- **状态**: 已完成

#### TASK-014-003: 新增编排器协议文档
- **关联需求**: REQ-012, REQ-013, REQ-014, REQ-015, REQ-018
- **验收标准**:
  - [x] `docs/asp-review-orchestrator-protocol.md` 存在
  - [x] 定义 reviewer、fixer、复审的 I/O schema
  - [x] 明确 `prd_logs/`、`arch_logs/`、`plan_logs/`、`impl_logs/`
  - [x] **异常路径验证**: fixer 不存在时降级为 `ASK`
- **状态**: 已完成

#### TASK-014-004: 同步 014 规格与追溯文档到新 skill
- **关联需求**: REQ-001, REQ-014, REQ-015
- **验收标准**:
  - [x] `architecture.md`、`product-map.md`、`traceability-matrix.md` 指向 `pb-review-v2`
  - [x] `feature-specs` 的实现映射指向 `skills/pb-review-v2/SKILL.md`
  - [x] **异常路径验证**: 不再把 014 的实现锚点写回旧 reviewer
- **状态**: 已完成

#### TASK-014-005: 补充测试并升级文档校验链路
- **关联需求**: REQ-002, REQ-005, REQ-014, REQ-015, REQ-019
- **验收标准**:
  - [x] 新增 `tests/test_pb_review_v2.py`
  - [x] `validate-iteration-docs.py` 支持 ASP / legacy 双模型
  - [x] CI `validate-docs` 调用 Python 校验脚本
  - [x] **异常路径验证**: 非法 ASP 目录显式失败
- **状态**: 已完成

## 4. 测试矩阵

| 测试点 ID | 关联需求 | 任务 ID | 测试策略 | 成功标准 |
|----------|----------|---------|---------|---------|
| TC-014-001 | REQ-001 / REQ-006 | TASK-014-001 | pytest 文本断言 | `pb-review-v2` 为独立五阶段 reviewer |
| TC-014-002 | REQ-005 / REQ-007 / REQ-008 / REQ-009 / REQ-011 | TASK-014-002 | pytest 文本断言 | checklist、决策表、模板齐全 |
| TC-014-003 | REQ-012 / REQ-013 / REQ-014 / REQ-018 | TASK-014-003 | pytest 文本断言 | 协议文档定义状态机与归档路径 |
| TC-014-004 | REQ-001 / REQ-014 / REQ-015 | TASK-014-004 | pytest 文本断言 | 014 文档实现锚点已切到 `pb-review-v2` |
| TC-014-005 | REQ-002 / REQ-005 / REQ-015 / REQ-019 | TASK-014-005 | pytest + 模块测试 | ASP / legacy 迭代都可被校验 |

## 5. 风险评估

### 已处理风险

- **风险**: 新 skill 命名若使用 `pb-review` 会覆盖现有目录。
  - **处理**: 用户确认命名为 `pb-review-v2`。

- **风险**: 旧版校验脚本和 CI 对迭代目录做了过时的硬编码。
  - **处理**: 改为统一调用 Python 校验脚本，并加入 ASP / legacy 双模型判断。

### 剩余风险

- `pb-review-v2` 目前只落了文档合同与回归测试，没有配套独立 orchestrator 执行器。
- 014 的历史评审日志仍保留旧命名背景，这是历史证据，不在本轮重写范围内。

## 6. Gate 5 / Gate 6 检查

- [x] 现有代码分析已完成
- [x] 技术方案已决议
- [x] 所有 P0 功能都有对应任务
- [x] 任务验收标准可验证
- [x] 失败路径已规划并实现测试
- [x] 新增公共 Python 逻辑使用 docstring
- [x] 代码和文档已落盘
- [x] 相关 pytest 已通过

## 7. 阶段结论

- 014 已完成 P5 规划与本轮 P6 实现。
- 下一步可进入代码审查阶段。
