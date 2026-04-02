# Review Report: Round 4
**Date**: 2026-03-30
**Reviewer**: Codex
**Status**: FAIL

## Previous Rounds Summary
- Round 1 (Claude): FAIL - 4 MAJOR, 3 MINOR
- Round 1 Patch: 已补齐 D-17/D-18 粒度、blocked 条件、Data Flow 章节与 renderer 归属
- Round 2 (Codex): FAIL - 1 BLOCKER, 4 MAJOR, 1 MINOR
- Round 2 Patch: 已补齐产品目录完整度评分、D-20 八项条件、Feature→ExistingTest 函数级映射、score 口径、renderer 输入字段名
- Round 3 (Claude): PASS - 认定前序 BLOCKER/MAJOR 已修复，但保留 2 个 MINOR，其中 Loading State 缺失未修复

## Summary
双向覆盖仍完整且无排除项入侵，但 Round 3 的 PASS 结论不能维持：D-19 理想测试组 contract、D-18 测试依赖 schema、Loading State 和 Data Dictionary 仍未闭合，无法通过。

## Coverage Matrix
| Proposal REQ | Spec US | Status |
|-------------|---------|--------|
| REQ-001 | US-001, US-002, US-003, US-004 | ✅ Covered |
| REQ-002 | US-005 | ✅ Covered |
| REQ-003 | US-006 | ✅ Covered |
| REQ-004 | US-007 | ✅ Covered |
| REQ-005 | US-008 | ✅ Covered |
| REQ-006 | US-009 | ⚠️ Partial |
| REQ-007 | US-010 | ✅ Covered |
| REQ-008 | US-011 | ✅ Covered |
| REQ-009 | US-012 | ✅ Covered |
| REQ-010 | US-013 | ⚠️ Partial |
| REQ-011 | US-014 | ⚠️ Partial |
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
| 001 | **MAJOR** | `REQ-010` 要求生成"按 D-19 标准的理想测试组清单"，但 spec 只定义了已观测到的 `d19_test_groups.groups` 与 `render_test_case_index.py` 的现有输入；既没有定义"标准 8 组"的名称/结构，也没有定义该理想清单如何进入 renderer。与此同时 `US-004` 又以 `test_case_group_count >= 8` 作为 D-20 门槛，导致实现只能依赖隐含常量，违反宪法"零假设原则"与"显式优于隐式"，也不满足 `CON-001` 的可恢复数据契约要求。 | spec.md / US-004, US-013, Data Flow, Renderer Script 归属 | New |
| 002 | **MAJOR** | `REQ-006` 承诺 dependency-reconstructor 要"输出 Mock/Stub 策略建议，为 D-18 Fixture Contract 提供数据"，`US-009` 也要求标注哪些依赖已有 Mock、哪些缺少 Mock；但 `d18_fixture` schema 只有子项状态与 `evidence_refs`，Data Flow 仅笼统写 `dependency_registry（含 mock_strategy 字段）` 和"反写外部依赖部分"，没有定义依赖名、已有/缺失 Mock 标记、建议结构或反写字段。`US-009` 与 `US-014` 因而缺少稳定 contract，违反 `CON-001` 与 `CON-002`。 | spec.md / US-009, US-014, Data Flow | New |
| 003 | **MAJOR** | 宪法符合性未闭合。审查协议 A 明确要求定义 Empty State、Error State、Loading State，但状态表只有 Empty/Error/Success，没有 Loading State。Round 3 将该问题降为 MINOR，但当前 spec 仍未补齐，属于明确的状态定义缺失。 | spec.md / 状态定义表 | Inherited from Round 3 #001（级别升级） |
| 004 | **MAJOR** | 逻辑自洽性仍存在 data island。spec 在 User Stories 和 Data Flow 中使用了 `entry_surface_inventory`、`product_docs_dir`、`existing_test_count`、`coverage_scope`、`blocking_reasons`、`feature_state_registry`、`mock_strategy`、`test_mapping` 等关键术语/字段，但 Data Dictionary 只定义到 `d18_sub_item_status`，未覆盖这些 contract 字段。审查协议 C 明确要求术语在 Data Dictionary 中闭合，否则实现与 renderer 会各自解释。 | spec.md / Data Dictionary | New |
| 005 | **MINOR** | `partial` 判定仍使用 `And/Or` 混写，缺少括号化表达；语义上期望为 `not blocked AND (oracle<90 OR fixture<90 OR groups<5)`，但当前文本与状态表都可能被实现者作不同优先级解释。 | spec.md / US-001, 状态定义表 | Inherited from Round 3 #002 |

## Resolved Issues (from Previous Rounds)
| Original ID | Round | Resolution |
| :--- | :--- | :--- |
| R1-001 | Round 1 | ✅ 已修复 |
| R1-002 | Round 1 | ✅ 已修复 |
| R1-003 | Round 1+2 | ✅ 已修复 |
| R1-004 | Round 1 | ✅ 已修复 |
| R1-005 | Round 1 | ✅ 已修复 |
| R2-001 | Round 2 | ✅ 已修复 |
| R2-002 | Round 2 | ✅ 已修复 |
| R2-003 | Round 2 | ✅ 已修复 |
| R2-004 | Round 2 | ✅ 已修复 |
| R2-005 | Round 2 | ✅ 已修复 |
| R2-006 | Round 2 | ✅ 已修复 |

## Action Required
Please fix MAJOR issues. Do not fix MINOR issues in this round to save tokens.
