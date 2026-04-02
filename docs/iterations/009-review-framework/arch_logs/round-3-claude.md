# Review Report: Round 3
**Date**: 2026-03-27
**Reviewer**: Claude
**Status**: FAIL

## Previous Rounds Summary
- Round 1 (Claude): FAIL → 2 BLOCKER, 3 MAJOR, 3 MINOR → 修复 5 项（001-005），延迟 3 项 MINOR（006-008）
- Round 2 (Codex): FAIL → 2 BLOCKER, 3 MAJOR, 4 MINOR → 修复 5 项（001-005），延迟 3 项 MINOR（006-008），009 顺带解决

## Round 2 Fix Verification

| Issue ID | Fix Status | Verification |
|----------|-----------|-------------|
| R2-001 | ✅ Verified | Section 5.1（行 716-727）evidence_policy 完整定义 required_sources/min_confidence/allow_inference，行 724-727 描述约束语义。C-002~C-009 各组件（行 159-165, 212-218, 270-276, 317-323, 359-365, 406-412, 449-455, 489-495）均声明 evidence_policy |
| R2-002 | ✅ Verified | C-005（行 327）、C-006（行 369）、C-007（行 416）、C-008（行 459）均明确"编排器将 gaps 归集到 gap_registry.json（追加去重）"。C-008 同时声明 conflicts 归集路径（行 459）。序列图（行 601-628）一致显示 Orch 执行归集 |
| R2-003 | ⚠️ Verified with regression | Section 5.4（行 765-776）明确编排器持久化职责，行 681 注释强化。序列图一致。**但 Section 6.1 组件架构图（行 864-871）仍显示各 Skill 直接"写入"FS**，与 Section 5.4 矛盾（见 NEW-001） |
| R2-004 | ✅ Verified | Section 7（行 920）C-001 标注为"跨功能点（cross-cutting）"，行 921 新增独立行 Section 5.1 → FP-001。C-002 单独映射 FP-008（行 922），不再冲突 |
| R2-005 | ✅ Verified | C-003（行 229）新增 Spec 偏差说明，明确标注 spec 需同步更新 |

## Coverage Matrix
| Function Point | Architecture Component | Status |
|---------------|----------------------|--------|
| FP-001 | Section 5.1 统一 Skill 协议 + 5.2 协议一致性规则 | ⚠️ Partial（min_confidence 枚举值与 spec 不一致） |
| FP-002 | .review/ 文件协议 + Section 5.2 核心数据结构 | ✅ Covered |
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
| 001 | **MAJOR** | 组件架构图（Section 6.1）与持久化职责模型（Section 5.4）矛盾——Section 5.4（行 767）明确声明"Skill 只负责计算和返回结果，编排器负责所有持久化操作"，但 Section 6.1 组件架构图（行 864-871）显示所有 8 个 Skill 直接以虚线"写入"FS。应改为：仅 Orch 写入 FS，Skill 以虚线"读取"FS（符合 Section 5.3 中 Skill 从 .review/ 读取 ReviewContext 的描述）。Round 2 fix 003 修复了文字描述和序列图，但遗漏了组件架构图的同步更新。 | architecture.md Section 6.1（行 864-871）vs Section 5.4（行 767） | New（R2-003 regression） |
| 002 | **MAJOR** | Section 编号冲突——存在两个"5.2"：行 741 `### 5.2 协议一致性规则` 和行 778 `### 5.2 核心数据结构`。导致文档内交叉引用模糊（如"参见 Section 5.2"无法确定指向哪一节）。建议将核心数据结构重编号为 5.5（5.3 已被 ReviewContext 占用，5.4 已被归集职责占用）。 | architecture.md 行 741 vs 行 778 | New |
| 003 | **MAJOR** | 脚本输出路径与编排器持久化模型冲突——C-010 scripts/collect_evidence.py（行 526-529）的 CLI 参数 `--output evidence_registry.json` 暗示脚本直接写入最终 registry 文件。但 Section 5.4 规定所有持久化由编排器执行。脚本应输出到临时文件或 stdout，由 EvidenceCollector Skill 读取后通过 context_writes 返回给编排器。同理 C-011 scripts/parse_git_history.py（行 545-548）的 `--output git_history.json` 也存在相同问题。 | architecture.md Section 3.11（行 526-529）、3.12（行 545-548）vs Section 5.4（行 767） | New |
| 004 | **MINOR** | min_confidence 枚举值与 spec 不一致——spec Section 4.1（行 365）定义 `min_confidence: explicit/inferred/uncertain` 三级，architecture Section 5.1（行 720）仅列出 `explicit/inferred` 两级，缺少 `uncertain`。虽然当前所有组件 evidence_policy 均使用 explicit，但协议定义的枚举值不完整可能影响 V2 扩展。 | architecture.md Section 5.1（行 720）vs spec.md Section 4.1（行 365） | New |
| 005 | **MINOR** | include/exclude_patterns 默认值仍使用 `[...]` 省略号占位符 | architecture.md Section 3.3（行 131-132） | Inherited from R1-006 |
| 006 | **MINOR** | 数据流图中 `object_registry.json` 出现两次，可能误导读者 | architecture.md Section 6.2（行 895-896） | Inherited from R1-007 |
| 007 | **MINOR** | Section 8.3 声明非 Git 项目回退到文件 mtime，但 C-004 ConflictResolver 冲突决议算法未包含 mtime 回退路径 | architecture.md Section 3.5（行 280-284）vs Section 8.3（行 984） | Inherited from R1-008 |

## Resolved Issues (from Previous Rounds)
| Issue ID | Round | Resolution |
|----------|-------|-----------|
| R1-001 | Round 1 | ✅ pb-review 输出格式已统一为标准 Skill 协议 |
| R1-002 | Round 1 | ✅ EvidenceCollector 输入已改为从 context 读取 |
| R1-003 | Round 1 | ✅ Registry 追加写入机制已定义 |
| R1-004 | Round 1 | ✅ 追溯矩阵已修正（经 Round 2 二次修正） |
| R1-005 | Round 1 | ✅ checkpoint.json 已增强 |
| R2-001 | Round 2 | ✅ evidence_policy 已完整定义 |
| R2-002 | Round 2 | ✅ Gap 持久化路径已补全 |
| R2-003 | Round 2 | ⚠️ 文字和序列图已修复，组件图未同步（NEW-001） |
| R2-004 | Round 2 | ✅ 追溯矩阵 C-001 正确标注 cross-cutting |
| R2-005 | Round 2 | ✅ Spec 偏差说明已添加 |
| R2-009 | Round 2 | ✅ Section 5.3 ReviewContext 物理实现已显式声明 |

## Action Required
Please fix MAJOR issues (001-003). Do not fix MINOR issues (004-007) in this round to save tokens.
