# Review Report: Round 2
**Date**: 2026-03-27
**Reviewer**: Codex
**Status**: FAIL

## Previous Rounds Summary
- Round 1 (Claude): FAIL → 2 BLOCKER, 3 MAJOR, 3 MINOR → 修复 5 项（001-005），延迟 3 项 MINOR（006-008）

## Round 1 Fix Verification

| Issue ID | Fix Status | Verification |
|----------|-----------|-------------|
| R1-001 | ✅ Verified | Section 3.2（行 76-89）pb-review 输出已统一为 `status/objects/relations/conflicts/gaps/context_writes/metadata/errors` 标准结构 |
| R1-002 | ⚠️ Verified with regression | Section 3.4（行 176）EvidenceCollector 已改为从 context 读取。但 spec Section 5.2（行 465）未同步更新，产生 spec-architecture 不一致（见 NEW-005） |
| R1-003 | ✅ Verified | Section 4.2（行 591-600）新增 read-dedup-merge-write 追加写入机制，基于唯一 ID 幂等 |
| R1-004 | ⚠️ Verified with regression | Section 7（行 781-782）FP-001 已由 Section 5.1 覆盖。但 C-001 被重映射到 FP-008 与 C-002 冲突（见 NEW-004） |
| R1-005 | ✅ Verified | Section 3.2（行 102-112）checkpoint.json 新增 `completed_writes` 字段，写入顺序和恢复校验机制完整 |

## Coverage Matrix
| Function Point | Architecture Component | Status |
|---------------|----------------------|--------|
| FP-001 | Section 5.1 统一 Skill 协议 | ⚠️ Partial（缺 evidence_policy） |
| FP-002 | .review/ 文件协议 + Section 5.2 数据结构 | ✅ Covered |
| FP-003 | C-004 pb-review-conflict-resolver + C-011 scripts/parse_git_history.py | ✅ Covered |
| FP-004 | C-005 pb-review-product-reconstructor | ✅ Covered |
| FP-005 | C-006 pb-review-feature-reconstructor | ✅ Covered |
| FP-006 | C-007 pb-review-relation-builder | ✅ Covered |
| FP-007 | C-008 pb-review-gap-analyzer | ✅ Covered |
| FP-008 | C-002 pb-review-project-scope | ✅ Covered |
| FP-009 | C-003 pb-review-evidence-collector + C-010 scripts/collect_evidence.py | ✅ Covered |
| FP-010 | C-009 pb-review-report-composer | ✅ Covered |
| FP-011 | — | ⏳ V2 (Not required) |
| FP-012 | — | ⏳ V2 (Not required) |
| FP-013 | — | ⏳ V2 (Not required) |

## Exclusion Invasion Check
| EXC ID | 排除项 | 是否入侵 architecture.md | Status |
|--------|--------|------------------------|--------|
| EXC-001 | 自动修复代码问题 | 否 | ✅ Clean |
| EXC-002 | 生成新的需求文档 | 否 | ✅ Clean |
| EXC-003 | 代码质量打分（A/B/C 评级） | 否 | ✅ Clean |
| EXC-004 | 性能分析、安全扫描 | 否 | ✅ Clean |
| EXC-005 | 项目管理功能 | 否 | ✅ Clean |

## Issues List
| ID | Type | Description | Location | New/Inherited |
| :--- | :--- | :--- | :--- | :--- |
| 001 | **BLOCKER** | `evidence_policy` 完全缺失——spec Section 4.1（行 363-366）将 `evidence_policy`（含 `required_sources`、`min_confidence`、`allow_inference` 三字段）定义为 Skill 协议的必需部分。architecture Section 5.1 统一协议（行 619-637）完全未包含此字段，11 个组件定义（Section 3.2-3.12）也均未声明 evidence_policy。FP-001 要求"定义所有 Skill 的输入输出格式和执行规范"，协议定义不完整直接违反 FP-001 覆盖。 | architecture.md Section 5.1（行 619-637）vs spec.md Section 4.1（行 363-366） | New |
| 002 | **BLOCKER** | Gap 持久化路径不完整——protocol rule 2（spec Section 4.3 行 382，architecture 未显式声明等价规则）要求 Skill 输出的 `gaps` 自动归集到 `context.gap_registry`。但 architecture 中仅 C-008 GapAnalyzer（行 400）写入 `gap_registry.json`。C-005 ProductReconstructor（行 281）、C-006 FeatureReconstructor（行 314）、C-007 RelationBuilder（行 349）均声明输出 `gaps: array`，但无任何持久化路径。上游 Skill 产生的 gap 被静默丢弃。同理 `conflicts` 也受影响：C-008 GapAnalyzer（行 387）输出 conflicts，但仅 C-004 ConflictResolver 写入 `conflict_registry.json`，GapAnalyzer 的 conflicts 无持久化路径。 | architecture.md Section 3.6（行 281）、3.7（行 314）、3.8（行 349）、3.9（行 387, 400） | New |
| 003 | **MAJOR** | 编排器 vs Skill 持久化职责模型矛盾——spec Section 4.3 rule 2-3 定义了两个编排器职责：(a) 标准字段（objects/relations/conflicts/gaps）自动归集到对应 registry；(b) `context_writes` 由编排层负责写入。但 architecture 的序列图（Section 4.1 行 530-531）和组件定义（Section 3.6 行 292、3.7 行 326）显示 Skill 直接写入文件系统。两种模型并存且未声明哪种为权威：如果 Skill 自己写文件，编排器自动归集就是冗余；如果编排器负责归集，Skill 直接写文件就绕过了编排层。架构必须二选一并保持一致。 | architecture.md Section 4.1 序列图 vs spec.md Section 4.3 rule 2-3 | New |
| 004 | **MAJOR** | 追溯矩阵 C-001 映射错误（Round 1 修复引入的回归）——Section 7（行 781）将 C-001 pb-review（编排器）映射到 `FP-008（编排层）`，但 FP-008 按 function-points.md（行 14）定义为"项目接入与范围定义"，实际由 C-002 pb-review-project-scope 覆盖（行 783）。C-001 和 C-002 同时映射到 FP-008 导致追溯关系混乱。C-001 作为流程编排基础设施，不对应任何单一 FP——应标注为"跨功能点（cross-cutting）"或引入独立追溯条目。Round 1 fix 004 将 C-001 从 FP-001 移到 FP-008 时引入此错误。 | architecture.md Section 7（行 781-783） | New（R1-004 regression） |
| 005 | **MAJOR** | Spec-Architecture 输入定义不一致——spec Section 5.2（行 465）将 `resource_inventory: object` 声明为 EvidenceCollector 的直接参数，architecture Section 3.4（行 176）则从 `context.project_metadata.resource_inventory` 读取。Round 1 fix 002 修改了 architecture 但 spec 未同步。实现者面对两份相互矛盾的规格说明。虽然 architecture 的选择正确（符合协议 rule 4），但 architecture 应至少添加偏差说明或要求 spec 更新。 | architecture.md Section 3.4（行 176）vs spec.md Section 5.2（行 465） | New（R1-002 side-effect） |
| 006 | **MINOR** | include/exclude_patterns 默认值仍使用 `[...]` 省略号占位符 | architecture.md Section 3.3（行 131-132） | Inherited from R1-006 |
| 007 | **MINOR** | 数据流图中 `object_registry.json` 出现两次，可能误导读者认为是两个独立文件 | architecture.md Section 6.2（行 756-757） | Inherited from R1-007 |
| 008 | **MINOR** | Section 8.3 声明非 Git 项目回退到文件 mtime，但 C-004 ConflictResolver 冲突决议算法未包含 mtime 回退路径 | architecture.md Section 3.5（行 253-257）vs Section 8.3（行 844-845） | Inherited from R1-008 |
| 009 | **MINOR** | ReviewContext 物理实现未显式声明——architecture 将 `ReviewContext` 同时用作抽象协议概念（Section 5.1 行 623 `context: ReviewContext`）和物理文件系统目录（Section 4.2 `.review/` 目录结构）。两者的等价关系从未被显式声明（即"ReviewContext 等于 .review/ 目录下所有 JSON 文件的集合"）。对实现者而言，是传递内存对象还是让 Skill 直接读文件不明确。 | architecture.md Section 5.1（行 623）vs Section 4.2（行 562-574） | New |

## Resolved Issues (from Previous Rounds)
| Issue ID | Round | Resolution |
|----------|-------|-----------|
| R1-001 | Round 1 | ✅ pb-review 输出格式已统一为标准 Skill 协议 |
| R1-002 | Round 1 | ✅ EvidenceCollector 输入已改为从 context 读取（但引发 NEW-005） |
| R1-003 | Round 1 | ✅ Registry 追加写入机制已定义（read-dedup-merge-write） |
| R1-004 | Round 1 | ⚠️ 追溯矩阵已修正 FP-001 归属，但 C-001 重映射引发 NEW-004 |
| R1-005 | Round 1 | ✅ checkpoint.json 已增强 completed_writes 字段 |

## Action Required
Please fix BLOCKER and MAJOR issues (001-005). Do not fix MINOR issues (006-009) in this round to save tokens.
