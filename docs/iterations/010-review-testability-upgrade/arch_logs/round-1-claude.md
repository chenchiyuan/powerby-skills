# Architecture Review: Round 1 (Claude)

**Reviewer**: Claude
**Round**: 1
**Date**: 2026-03-30
**审查对象**: architecture.md v1.0.0

---

## 审查结论

**STATUS: FAIL**

发现 4 个 MAJOR 问题，需要修复后才能进入下一轮审查。

---

## 三维检查结果

### 维度一：宪法符合性

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 零假设原则 | ✅ PASS | 通过两阶段评估策略明确处理数据依赖，未做隐式假设 |
| 借鉴现有代码而后创造 | ✅ PASS | 扩展复用策略正确，零新建 Skill |
| 单一职责 | ✅ PASS | 每个 Skill 职责边界清晰 |
| SOLID/DRY | ✅ PASS | schema 抽离实现了 DRY |
| 小步提交 | ⚠️ N/A | 架构层面不涉及 |
| 方案选项 | ⚠️ MINOR-001 | 架构只给出一种方案（扩展复用），未提供替代方案对比 |

### 维度二：双向覆盖

#### FP → 组件方向

| FP | 组件归属 | 状态 |
|----|---------|------|
| FP-001 | feature-reconstructor | ✅ |
| FP-002 | gap-analyzer | ✅ |
| FP-003 | report-composer | ✅ |
| FP-004 | project-scope | ✅ |
| FP-005 | product-reconstructor | ✅ |
| FP-006 | dependency-reconstructor | ✅ |
| FP-007 | implementation-mapper | ✅ |
| FP-008 | relation-builder | ✅ |
| FP-009 | report-composer | ✅ |
| FP-010 | report-composer | ✅ |
| FP-011 | report-composer | ✅ |
| FP-012 | report-composer | ✅ |
| FP-013 | pb-review | ✅ |
| FP-014 | feature-reconstructor | ✅ |
| FP-015 | feature-reconstructor | ✅ |

**结果**: 15/15 FP 覆盖 ✅

#### 组件 → FP 方向

| 组件 | FP 归属 | 状态 |
|------|---------|------|
| feature-reconstructor | FP-001, FP-014, FP-015 | ✅ |
| gap-analyzer | FP-002 | ✅ |
| report-composer | FP-003, FP-009~012 | ✅ |
| pb-review | FP-013 | ✅ |
| project-scope | FP-004 | ✅ |
| product-reconstructor | FP-005 | ✅ |
| dependency-reconstructor | FP-006 | ✅ |
| implementation-mapper | FP-007 | ✅ |
| relation-builder | FP-008 | ✅ |

**结果**: 9/9 组件覆盖 ✅

#### Proposal REQ → 架构方向

| REQ | 架构覆盖 | 状态 |
|-----|---------|------|
| REQ-001~015 | 通过 FP 映射到组件 | ✅ |
| CON-001 | 架构继承 009 原则 | ✅ |
| CON-002 | ⚠️ **MAJOR-001** | 见下方 |
| CON-003 | 架构明确"还原+识别"定位 | ✅ |
| CON-004 | No Backend Proxy 约束保留 | ✅ |
| EXC-001~004 | 架构未涉及排除项 | ✅ |

### 维度三：逻辑自洽

检查点及结果：

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 数据依赖无环 | ✅ PASS | Step 5→7 两阶段写入方向正确 |
| Registry 字段不冲突 | ⚠️ **MAJOR-002** | gap_registry vs difference_registry 混淆 |
| 编排器步骤编号连续 | ✅ PASS | Step 1~16 连续 |
| Schema 引用一致性 | ⚠️ **MAJOR-003** | Schema 加载机制未定义 |
| 模板-渲染脚本对应 | ✅ PASS | 4 模板对应 4 脚本 |
| 回写规则完整性 | ✅ PASS | 只补充/上调规则明确 |
| Checkpoint 恢复逻辑 | ⚠️ **MAJOR-004** | Step 13~16 恢复逻辑不完整 |

---

## 问题清单

### MAJOR-001: 缺少 D-17~D-20 的证据策略声明

**位置**: 第三章 §3.2.1 feature-reconstructor 设计

**问题**: Proposal CON-002 明确要求"所有'已定义'的判断都必须有代码证据支撑（evidence_refs），不能因为标准要求就编造内容"。但 architecture.md 的 feature-reconstructor 设计中未声明 D-17~D-20 评估的 evidence policy（required_sources、min_confidence、allow_inference）。

**风险**: 实现者可能在缺乏证据时将子项标记为 "defined"，违反 CON-002。

**建议修复**: 在 §3.2.1 中新增 Evidence Policy 段落，明确：
- D-17 的 `required_sources`: code, test
- D-18 的 `required_sources`: test
- D-19 的 `required_sources`: test
- D-20 依赖 D-17~D-19 的聚合结果，无独立 evidence_source
- `allow_inference`: false（所有子项状态必须有直接证据）
- 缺少证据时标记为 "missing"，不允许推断为 "defined"

### MAJOR-002: gap_registry 与 difference_registry 混淆

**位置**: 第五章 §5.5 difference_registry 扩展

**问题**: 架构在 `difference_registry` 中新增 `gap_type` 和 `gap_severity` 字段，但现有数据模型中 `gap_registry` 和 `difference_registry` 是两个独立 registry：
- `gap_registry`：存储缺失链接（missing_relation, isolated_feature 等）
- `difference_registry`：存储文档与代码的差异（doc_without_code 等）

Spec US-005 定义的 4 种 gap 类型（missing_feature, missing_oracle, missing_fixture_contract, missing_test_traceability）在语义上更接近 `gap_registry`（缺失链接），而非 `difference_registry`（文档/代码差异）。

**风险**: gap-analyzer 输出的数据可能写入错误的 registry，导致 report-composer 读取错误。

**建议修复**:
1. 4 种新 gap 类型写入 `gap_registry`（而非 difference_registry）
2. `gap_registry` 条目扩展 `gap_severity` 字段
3. `difference_registry` 保持原有语义不变
4. 更新 §5.5 标题为 "gap_registry 扩展"

### MAJOR-003: Schema 文件加载机制未定义

**位置**: 第二章 §2.4 Schema 引用协议

**问题**: 架构声明"编排器在加载 Skill 时，同时加载其声明的 schema 文件到上下文"，但未定义具体加载机制。pb-review 的 Skill 是由 LLM 会话直接读取 SKILL.md 执行的，不存在"编排器加载"的技术手段。

当前 pb-review 的 references/ 目录是在 SKILL.md 中通过 `## References` 段落声明的，LLM 在执行 Skill 时会读取这些文件。Schema 文件需要采用相同的机制。

**风险**: 实现者不知道如何让 Skill 访问 schema 文件。

**建议修复**:
1. 明确 schema 文件通过 Skill 的 `## References` 或 `## 依赖 Schema` 段落声明
2. 编排器在切换到下一个 Skill 时，负责将 schema 文件路径传递给 LLM 上下文
3. 或：将 schema 文件复制/符号链接到各 Skill 的 references/ 目录下（但违反 DRY）
4. 推荐：在 pb-review 编排器的 SKILL.md 中声明统一加载所有 schema 文件，下游 Skill 直接从上下文中读取

### MAJOR-004: Step 13~16 的恢复逻辑与执行归属不完整

**位置**: 第三章 §3.2.4 编排器设计

**问题**:
1. Step 13~16 被标记为"report-composer → renderer script"，但这意味着 report-composer Skill 需要在 Step 12 之后仍然处于活跃状态来执行 Step 13~16。在当前编排器模型中，每个 Step 对应一个 Skill 的单次调用。Step 13~16 是 report-composer 的多次调用，还是 report-composer 在 Step 12 中一次性执行所有渲染？
2. Checkpoint 恢复：如果 Step 14 失败，恢复时是从 Step 13 重新开始（因为都是 report-composer），还是从 Step 14 单独恢复？

**风险**: 编排器实现时对 Step 13~16 的执行方式产生歧义。

**建议修复**:
1. 明确 Step 13~16 的执行方式：推荐每步由编排器直接调用 Python renderer 脚本（确定性步骤），无需加载 report-composer Skill
2. 这与 Tier 1 的确定性引导模式一致：renderer 脚本是纯模板渲染，不需要 LLM 判断
3. Checkpoint 每步独立记录，支持单步恢复

---

## MINOR 问题

### MINOR-001: 缺少架构方案对比

**说明**: 宪法要求"必须提供至少两种可行的方案"。虽然架构方向在 CLARIFICATION 阶段已确认，但 architecture.md 本身缺少方案选型记录（如：为什么选择内嵌扩展而非独立注册表，为什么选择 Step 13~16 而非 Step 12 子步骤）。

**建议**: 增加"架构决策记录"章节，记录关键决策及其理由。

### MINOR-002: Schema 文件缺少版本管理策略

**说明**: Schema 文件有版本号字段，但未定义版本升级策略（如：schema 版本变更时，已有的 registry 数据如何迁移）。

**建议**: 在 §2.1 设计原则中增加版本管理说明。

---

## 总结

| 级别 | 数量 | 说明 |
|------|------|------|
| BLOCKER | 0 | — |
| MAJOR | 4 | 全部需要修复 |
| MINOR | 2 | 建议修复 |

**下一步**: Architect 修复 4 个 MAJOR 后进入 Round 2。
