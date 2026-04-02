# Skill 设计原则检查清单

**迭代编号**: 011  
**审查日期**: 2026-03-30  
**审查范围**: `powerby-asp-*` 7 个 skill

---

## 1. 检查基准

检查基准来自 [`docs/skill-design-protocol.md`](../../../skill-design-protocol.md) 的“十条核心设计原则（Checklist）”。

| # | 原则 | 本轮检查结果 | 证据 |
|---|------|-------------|------|
| 1 | 用户任务定义 Skill | 通过 | 7 个 skill 的 `description` 均描述用户任务与适用场景 |
| 2 | description 是第一触发器 | 通过 | `description` 同时包含能力描述与触发语境 |
| 3 | 先写策略哲学，再写流程 | 通过 | 7 个 skill 均有 `Strategy`，且与 `Workflow` 分离 |
| 4 | 工具最小完备集 | 通过 | 7 个 skill 均有 `Tools and capability boundaries` |
| 5 | 易忘事实前置 | 通过 | 7 个 skill 均有 `Important facts and constraints` |
| 6 | 确定性工作下沉 scripts/ | 通过 | 011 架构约束明确无 `scripts/`，测试已校验目录不存在 |
| 7 | 多领域内容用 references/ 分层 | 通过 | 7 个 skill 全部补齐 `references/*.md` |
| 8 | 子任务写目标不写方法 | 通过 | 7 个 skill 均有 `Subtask / parallelism guidance`，只约束目标和边界 |
| 9 | 内建评估闭环 | 通过 | 新增 `tests/test_asp_document_upgrade.py`，并校验协议、技能和交付物 |
| 10 | 迭代修抽象层不修补丁 | 通过 | 本轮统一升级协议层与 skill 抽象，而非局部替换旧文档名 |

## 2. Skill 逐项结果

| Skill | 结论 | 备注 |
|------|------|------|
| `powerby-asp-product` | 通过 | 产出切到 `proposal.md + feature-spec-index.md + feature-specs/*.md` |
| `powerby-asp-reviewer` | 通过 | 审查输入切到新协议文档集合 |
| `powerby-asp-codex-reviewer` | 通过 | 明确 `codex exec -s read-only` 边界 |
| `powerby-asp-visualizer` | 通过 | 输出扩展到 3 份可视化/测试化文档 |
| `powerby-asp-architect` | 通过 | 明确只补 `D-09~D-16` |
| `powerby-asp-arch-reviewer` | 通过 | 审查覆盖输入切到 `feature-spec-index.md + feature-specs/*.md + architecture.md` |
| `powerby-asp-arch-codex-reviewer` | 通过 | 明确只读审查与输出路径约束 |

## 3. 结论

011 本轮交付已形成“协议文档 + skill 正文 + references + 自动化测试 + 检查清单”的完整证据链，可以支撑“7 个 ASP skill 通过十条核心原则 checklist”的交付结论。
