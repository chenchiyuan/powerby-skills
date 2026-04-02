# Review Report: Round 2
**Date**: 2026-03-30
**Reviewer**: Codex
**Status**: FAIL

## Previous Rounds Summary
- Round 1 (Claude): FAIL - 4 MAJOR, 3 MINOR。
- Round 1 Patch: 声称已修复 MAJOR #001~#004，并提前修复 MINOR #005。
- 本轮复核结果：Round 1 的 D-17 粒度、blocked 条件、Data Flow 章节、renderer 归属已基本补齐，但仍残留 1 个 proposal 级漏项和 4 个标准/契约级缺陷。

## Summary
覆盖矩阵已基本闭合，且无排除项入侵，但 `spec.md` 仍存在 1 个合同级漏设计和 4 个会导致实现分叉或虚高 coverage 判断的关键问题，不能通过。

## Coverage Matrix
| Proposal REQ | Spec US | Status |
|-------------|---------|--------|
| REQ-001 | US-001, US-002, US-003, US-004 | ✅ Covered |
| REQ-002 | US-005 | ✅ Covered |
| REQ-003 | US-006 | ✅ Covered |
| REQ-004 | US-007 | ✅ Covered |
| REQ-005 | US-008 | ⚠️ Partial |
| REQ-006 | US-009 | ✅ Covered |
| REQ-007 | US-010 | ⚠️ Partial |
| REQ-008 | US-011 | ✅ Covered |
| REQ-009 | US-012 | ✅ Covered |
| REQ-010 | US-013 | ✅ Covered |
| REQ-011 | US-014 | ✅ Covered |
| REQ-012 | US-015 | ✅ Covered |
| REQ-013 | US-016 | ✅ Covered |
| REQ-014 | US-017 | ✅ Covered |
| REQ-015 | US-018 | ✅ Covered |

## Exclusion Invasion Check
| EXC ID | 排除项 | 是否入侵 spec.md | Status |
|--------|--------|-----------------|--------|
| EXC-001 | 自动改造/修复代码中缺失的 Oracle 或 Fixture | 否 | ✅ Clean |
| EXC-002 | 在 archer 项目上实际运行验证 | 否 | ✅ Clean |
| EXC-003 | 修改 pb-review-standard.md 标准文档 | 否 | ✅ Clean |
| EXC-004 | 新增 LLM HTTP 调用或后端推理代理 | 否 | ✅ Clean |

## Issues List
| ID | Type | Description | Location | New/Inherited |
| :--- | :--- | :--- | :--- | :--- |
| 001 | **BLOCKER** | `REQ-005` 要求“输出产品目录完整度评分”，但 `US-008` 只定义了 Goal 可量化率、Scenario 完整率、Constraint 可追踪率 3 个分项比率，未定义总评分、计算公式或等级口径。proposal 合同未被完整设计。 | spec.md / US-008（lines 297-302） | New |
| 002 | **MAJOR** | D-20 仍未对齐 `pb-review-standard.md §3.5`。`US-004` 仅以 `testability_status = test_ready + 无未闭合 gap + 已有测试追踪链路` 判定 `coverage_claim_allowed=yes`；`US-018` 与 `d20_coverage_claim` 也缺少“覆盖范围、未闭合断言点、未标准化 fixture”等必填内容。当前 spec 允许在 `<8` 测试组、错误码/边界条件未闭合时仍宣称 coverage，有违 `P-05 覆盖率不能虚高`。 | spec.md / US-004（lines 158-169）, US-018（lines 517-522）, Data Flow（lines 564-567） | New |
| 003 | **MAJOR** | `REQ-007` 与 `pb-review-standard.md §2.4` 要求建立 `Feature→ExistingTest` 链路，但 `US-010` 和数据流只输出 `Feature->TestFile`。这会把测试追踪粒度退化到文件级，无法可靠支撑“识别已有测试覆盖”与后续追踪矩阵。 | spec.md / US-010（lines 329-340）, Data Flow（lines 593-596） | New |
| 004 | **MAJOR** | `testability_score` 口径仍未消歧。`US-006`、`US-012`、Data Dictionary 固定为 “M-01~M-07 加权”，但 `pb-review-standard.md §4.1` 的 scorecard 公式包含“副作用断言覆盖率”，并未按当前 spec 的方式直接采用 `M-07 覆盖宣称可信率`。spec 没有显式声明以哪套口径为准，renderer 仍可能出现两套实现。 | spec.md / US-006（lines 253-264）, US-012（lines 377-385）, Data Dictionary（line 639） | New |
| 005 | **MAJOR** | Round 1 的 `#003` 仅部分修复。Data Flow schema 定义字段为 `d17_oracle / d18_fixture / d19_test_groups`，但 Renderer Script 表又写成 `feature_spec_registry.d17 / d18 / d19` 作为输入键；同一份 spec 的 registry contract 自相矛盾，违反 `CON-001` 对顺序执行/renderer 落盘/可恢复数据契约的要求。 | spec.md / Data Flow schema（lines 542-563）, Renderer Script 归属（lines 623-626） | Inherited from Round 1 #003（部分修复） |
| 006 | **MINOR** | 文档明确性仍有瑕疵：存在乱码/损坏字符（如“如��文件输出”“├��� 读取”“���能尚未进行测试组统计”），且状态表只有 Empty/Error/Success，没有审查协议 A 节要求的 Loading State。虽不阻塞范围覆盖，但会降低实现一致性和可读性。 | spec.md / lines 36, 594, 671, 667-673 | New |

## Resolved Issues (from Previous Rounds)
| Original ID | Round | Resolution |
| :--- | :--- | :--- |
| R1-001 | Round 1 | ✅ 已修复：D-17 已明确对齐为标准 9 个子项，并补充“不适用不计入分母”规则。 |
| R1-002 | Round 1 | ✅ 已修复：blocked 判定已补全为 3 个 OR 条件。 |
| R1-003 | Round 1 | ⚠️ 部分修复：已新增 Data Flow 章节，但 renderer 输入字段名仍与 schema 不一致，残留问题见本轮 #005。 |
| R1-004 | Round 1 | ✅ 已修复：4 个新增报告的 renderer script 归属已明确到 `pb-review-report-composer`。 |
| R1-005 | Round 1 | ✅ 已修复：D-18 已对齐为标准 6 个子项。 |

## Action Required
Please fix BLOCKER and MAJOR issues. Do not fix MINOR issues in this round to save tokens.