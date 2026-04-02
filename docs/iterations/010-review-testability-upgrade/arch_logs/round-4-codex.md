# Review Report: Round 4
**Date**: 2026-03-30  
**Reviewer**: Codex  
**Status**: FAIL

## Previous Rounds Summary
| Round | Reviewer | Status | Summary |
|---|---|---|---|
| 1 | Claude | FAIL | 提出 4 个 MAJOR、2 个 MINOR，要求补齐 Evidence Policy、schema 加载、gap 归档和 Step 13~16 执行模型。 |
| 2 | Codex | FAIL | 确认遗留 2 个继承性 MAJOR：`gap_registry` 归档未收敛、Step 13~16 执行归属未收敛。 |
| 3 | Claude | PASS | 宣告 Round 1/2 的 MAJOR 已全部关闭；本轮复核确认其中 `R2-MAJOR-002` 仍有残留。 |

## Summary
`R2-MAJOR-001` 已实质修复，但 `R2-MAJOR-002` 仍未彻底关闭；`producer_skill` 字段本身已修正为 `pb-review`，但组件关系图和 registry 写入流仍把 Step 13~16 的产物链路挂在 `report-composer` 下，全文未达到一致。

## Coverage Matrix
| Function Point | Architecture Component | Status |
|---------------|----------------------|--------|
| FP-001 | pb-review-feature-reconstructor | ✅ Covered |
| FP-002 | pb-review-gap-analyzer | ✅ Covered |
| FP-003 | pb-review-report-composer | ⚠️ Inconsistent |
| FP-004 | pb-review-project-scope | ✅ Covered |
| FP-005 | pb-review-product-reconstructor | ✅ Covered |
| FP-006 | pb-review-dependency-reconstructor | ✅ Covered |
| FP-007 | pb-review-implementation-mapper | ✅ Covered |
| FP-008 | pb-review-relation-builder | ✅ Covered |
| FP-009 | pb-review（编排器） | ⚠️ Inconsistent |
| FP-010 | pb-review（编排器） | ⚠️ Inconsistent |
| FP-011 | pb-review（编排器） | ⚠️ Inconsistent |
| FP-012 | pb-review（编排器） | ⚠️ Inconsistent |
| FP-013 | pb-review（编排器） | ⚠️ Inconsistent |
| FP-014 | pb-review-feature-reconstructor | ✅ Covered |
| FP-015 | pb-review-feature-reconstructor | ✅ Covered |

## Exclusion Invasion Check
| EXC ID | 排除项 | 是否入侵 | Status |
|--------|--------|---------|--------|
| EXC-001 | 自动改造/修复代码中缺失的 Oracle 或 Fixture | 否 | ✅ Clean |
| EXC-002 | 在 archer 项目上实际运行验证 | 否 | ✅ Clean |
| EXC-003 | 修改 pb-review-standard.md 标准文档 | 否 | ✅ Clean |
| EXC-004 | 新增 LLM HTTP 调用或后端推理代理 | 否 | ✅ Clean |

## Issues List
| ID | Type | Description | Location | New/Inherited |
| :--- | :--- | :--- | :--- | :--- |
| R4-MAJOR-001 | MAJOR | `R2-MAJOR-002` 未彻底修复。`§3.2.4` 与 `§5.6` 已把 Step 13~16 和 `producer_skill` 明确归属为 `pb-review`，但 `§6.1` 组件关系图仍显示 `report-composer -> renderers`，`§4.3` 写入流仍显示 `report-composer -> deliverable_manifest`。这会再次把 4 个专项报告的执行者、manifest 维护者和 checkpoint 责任拆成两套语义，违反宪法“显式优于隐式”要求 [consitution.md:132](/Users/chenchiyuan/projects/powerby-skills/docs/consitution.md#L132)，也未完全满足提案对顺序执行与 manifest 维护的一致性约束 [proposal.md:45](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/proposal.md#L45). | [architecture.md:322](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L322), [architecture.md:364](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L364), [architecture.md:376](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L376), [architecture.md:593](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L593), [architecture.md:773](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L773), [architecture.md:832](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L832) | Inherited |
| R4-MINOR-001 | MINOR | `§3.1` 组件总览仍出现两条 `pb-review（编排器）` 记录，且变更类型/FP 归属冲突：一条覆盖 `FP-009~013`，另一条仅覆盖 `FP-013`。这与 `§7.2` 的“9 组件全部有 FP 归属”不一致，削弱了组件清单作为权威索引的作用。 | [architecture.md:171](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L171), [architecture.md:173](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L173), [architecture.md:929](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L929) | New |
| R4-MINOR-002 | MINOR | `testability-score-formula.md` 的引用声明未完全收敛。`§2.2` 仅把该 schema 归给 `pb-review (编排器 Step 13)`，但 `§6.1` 图和 `§7.1` 又把它作为 `report-composer / FP-003` 的依赖。需要明确 Step 12 是直接读取公式计算 score，还是只消费已计算结果。 | [architecture.md:107](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L107), [architecture.md:827](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L827), [architecture.md:910](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/010-review-testability-upgrade/architecture.md#L910) | New |

## Resolved Issues (from Previous Rounds)
| Original ID | Round | Resolution |
| :--- | :--- | :--- |
| MAJOR-001 | 1 | 已补齐 D-17~D-20 Evidence Policy，并明确 `allow_inference: false`。 |
| MAJOR-003 | 1 | 已定义 schema 加载机制与上下文透传策略。 |
| R2-MAJOR-001 | 2 | 4 类新增 gap 已统一归档到 `gap_registry`；`difference_registry` 保持原语义，主文本不再把测试化 gap 归入 `difference_registry`。 |

## Action Required
Please fix BLOCKER and MAJOR issues.

本轮无 BLOCKER；通过前至少需要完成以下收敛：
1. 把 `§6.1` 和 `§4.3` 全部改为 `pb-review` 直连 renderers / `deliverable_manifest`，不要再保留 `report-composer` 的执行或写入归属。
2. 清理 `§3.1` 的重复组件行，并统一 `testability-score-formula.md` 在 Step 12 / Step 13 的依赖声明。