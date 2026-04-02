# Function Points: pb-review 标准驱动评估升级

## 总览

| FP | REQ | 功能名称 | 优先级 | 一句话描述 |
|----|-----|---------|--------|-----------|
| FP-001 | REQ-001 | 功能规格卡测试维度评估 | 必须 | feature-reconstructor 新增 D-17~D-20 评估与 testability_status 判定 |
| FP-002 | REQ-002 | 四种 Gap 类型识别 | 必须 | gap-analyzer 从 1 种扩展为 4 种 gap 类型并判定严重程度 |
| FP-003 | REQ-003 | 测试化摘要报告 | 必须 | report-composer 区分"还原"与"就绪"，输出 testability_score |
| FP-004 | REQ-004 | Entry Surface 全面扫描 | 必须 | project-scope 扫描 5 类入口（cli/api/page/cron/orchestration） |
| FP-009 | REQ-009 | Testability Scorecard 生成 | 必须 | 生成 11-testability-scorecard.md（M-01~M-07 评分 + 等级） |
| FP-010 | REQ-010 | Test Case Index 生成 | 必须 | 生成 12-test-case-index.md（已有 vs 理想测试对比） |
| FP-011 | REQ-011 | Fixture Contract 报告生成 | 必须 | 生成 13-test-fixture-contract.md（已有 vs 理想 Fixture 对比） |
| FP-012 | REQ-012 | Oracle Matrix 报告生成 | 必须 | 生成 14-test-oracle-matrix.md（已有 vs 理想 Oracle 对比） |
| FP-013 | REQ-013 | 编排器工作流升级 | 必须 | 集成 4 个新报告步骤 + checkpoint 支持 |
| FP-014 | REQ-014 | Feature Spec Index 模板升级 | 必须 | 索引表新增 5 列测试维度字段 |
| FP-015 | REQ-015 | Feature Spec Card 模板升级 | 必须 | 规格卡新增 D-17~D-20 四个章节 |
| FP-005 | REQ-005 | 产品目录完整度评估 | 应该 | product-reconstructor 评估 Goal/Scenario/Constraint 完整度 |
| FP-006 | REQ-006 | 测试依赖识别 | 应该 | dependency-reconstructor 输出 Mock/Stub 策略建议 |
| FP-007 | REQ-007 | 测试映射建立 | 应该 | implementation-mapper 建立 Feature→ExistingTest 函数级映射 |
| FP-008 | REQ-008 | 测试追踪链路 | 应该 | relation-builder 新增 Feature→TestCaseGroup 和 Rule→NegativeTest 链路 |

---

## 必须（���心）— 11 个功能点

### FP-001 → REQ-001 | 功能规格卡测试维度评估

**归属 Skill**: pb-review-feature-reconstructor

**描述**: 在还原功能规格卡时，基于 pb-review-standard.md §3.2~§3.5 新增 D-17(Test Oracle, 9 子项)、D-18(Fixture Contract, 6 子项)、D-19(Test Case Groups)、D-20(Coverage Claim, 8 项条件) 四个维度评估，并判定 testability_status（blocked/partial/test_ready）。

**验收标准摘要**:
- 每个功能的 D-17 完整度 = 已定义子项数 / 适用子项数 × 100%
- 每个功能的 D-18 完整度 = 已定义子项数 / 适用子项数 × 100%
- 统计 D-19 测试用例分组数量
- D-20 对齐标准 §3.5 全部 8 项条件判定 coverage_claim_allowed
- 输出 testability_status 三态判定
- 缺失项标记为"缺失"，已有项附带 evidence_refs

---

### FP-002 → REQ-002 | 四种 Gap 类型识别

**归属 Skill**: pb-review-gap-analyzer

**描述**: 对照标准 L1-2.5，从只识别 missing_feature 扩展为识别 4 种 gap 类型（missing_feature、missing_oracle、missing_fixture_contract、missing_test_traceability），并对每个 gap 判定严重程度（Critical/Major/Minor）。

**验收标准摘要**:
- 识别 4 种 gap 类型
- 每种 gap 有明确的判定规则和严重程度
- Critical = 阻塞整个功能测试化; Major = 影响覆盖率 >= 20%; Minor = 影响覆盖率 < 20%

---

### FP-003 → REQ-003 | 测试化摘要报告

**归属 Skill**: pb-review-report-composer

**描述**: 报告明确区分"已还原能力"和"测试就绪能力"，包含 testability_score（pb-review-standard.md §4.1 公式, M-01~M-07 加权）、test_ready/blocked/partial 功能数和清单。

**验收标准摘要**:
- testability_score 采用 §4.1 公式（7 项权重）
- 报告分章节列出 test_ready、blocked、partial 功能
- 不使用"completed"掩盖 test_ready 不足

---

### FP-004 → REQ-004 | Entry Surface 全面扫描

**归属 Skill**: pb-review-project-scope

**描述**: 对照标准扫描 5 类入口（cli/api/page/cron/orchestration），输出 entry_surface_inventory 供后续 skill 使用。

**验收标准摘要**:
- 输出包含 5 类入口清单
- 每个入口有类型标识和路径信息

---

### FP-009 → REQ-009 | Testability Scorecard 生成

**归属 Skill**: pb-review-report-composer（render_testability_scorecard.py）

**描述**: 生成 11-testability-scorecard.md，包含 M-01~M-07 当前评分、目标评分、差距分析和综合等级（A/B/C/D）。

**验收标准摘要**:
- 包含 7 项指标的当前值和目标值
- 综合 Testability Score 和等级判定
- 改造优先级建议

---

### FP-010 → REQ-010 | Test Case Index 生成

**归属 Skill**: pb-review-report-composer（render_test_case_index.py）

**描述**: 生成 12-test-case-index.md，对比已有测试用例与 D-19 标准的 8 个必需组，输出缺口分析。

**验收标准摘要**:
- 已有测试用例清单（来源: 代码扫描）
- 理想测试组清单（来源: D-19 标准）
- 缺口 = 理想 - 已有
- 优先级建议（先补 P0 缺口）

---

### FP-011 → REQ-011 | Fixture Contract 报告生成

**归属 Skill**: pb-review-report-composer（render_fixture_contract.py）

**描述**: 生成 13-test-fixture-contract.md，对比已有 Fixture 与 D-18 标准的 6 个子项，输出 Mock/Stub 策略建议。

**验收标准摘要**:
- 已有 Fixture 清单（来源: 测试代码扫描）
- 理想 Fixture 清单（来源: D-18 标准）
- 缺口分析 + Mock/Stub 策略建议

---

### FP-012 → REQ-012 | Oracle Matrix 报告生成

**归属 Skill**: pb-review-report-composer（render_oracle_matrix.py）

**描述**: 生成 14-test-oracle-matrix.md，对比已有 Oracle 与 D-17 标准的 9 项内容，每个功能一行，输出完整度评分。

**验收标准摘要**:
- 已有 Oracle 清单（来源: 代码中的 Schema/错误码/业务规则）
- 理想 Oracle 清单（来源: D-17 标准 9 项）
- 缺口分析 + 每功能 Oracle 完整度评分

---

### FP-013 → REQ-013 | 编排器工作流升级

**归属 Skill**: pb-review

**描述**: 在现有工作流末尾集成 4 个新报告生成步骤（步骤 11~14），checkpoint 支持断点恢复，deliverable_manifest 包含新交付物。

**验收标准摘要**:
- 07-review-report.md 之后依次生成 4 个新交付物
- checkpoint 记录每个新步骤完成状态
- resume=true 时从断点继续

---

### FP-014 → REQ-014 | Feature Spec Index 模板升级

**归属 Skill**: pb-review-feature-reconstructor（render_feature_deliverables.py）

**描述**: 03-feature-spec-index.md 索引表新增 5 列：testability_status、oracle_completeness、fixture_readiness、test_case_group_count、coverage_claim_allowed。

**验收标准摘要**:
- 索引表包含 5 个新增列
- 数据取自 feature_spec_registry 的 D-17~D-20 扩展字段

---

### FP-015 → REQ-015 | Feature Spec Card 模板升级

**归属 Skill**: pb-review-feature-reconstructor（render_feature_deliverables.py）

**描述**: 04-feature-specs/{function_id}.md 规格卡新增 D-17~D-20 四个章节，每项有"已定义/缺失"状态标记和 evidence_refs。

**验收标准摘要**:
- D-17 章节：9 个子项各自状态和完整度
- D-18 章节：6 个子项各自状态和完整度
- D-19 章节：测试组清单和每组用例数
- D-20 章节：覆盖声明判定、阻塞原因、未覆盖子能力

---

## 应该（辅助）— 4 个功能点

### FP-005 → REQ-005 | 产品目录完整度评估

**归属 Skill**: pb-review-product-reconstructor

**描述**: 评估产品目录中 Goal 可量化率、Scenario 完整率、Constraint 可追踪率，计算总评分 = 三项平均，输出等级（A/B/C/D）。

**验收标准摘要**:
- 3 个分项比率 + 总评分 + 等级判定
- 产品文档缺失时降级为 D（0 分）

---

### FP-006 → REQ-006 | 测试依赖识别

**归属 Skill**: pb-review-dependency-reconstructor

**描述**: 识别功能的外部依赖（API/数据库/缓存），输出 Mock/Stub 策略建议，标注已有和缺失的 Mock。

**验收标准摘要**:
- 每个外部依赖有 Mock 策略建议
- 已有 Mock 附带 evidence_refs
- 缺失 Mock 明确标注

---

### FP-007 → REQ-007 | 测试映射建立

**归属 Skill**: pb-review-implementation-mapper

**描述**: 建立 Feature→ExistingTest 映射，粒度到测试函数/方法，每个映射包含 test_file、test_function_name、test_level。

**验收标准摘要**:
- 函数级粒度映射（非文件级）
- 无测试时输出空映射 + existing_test_count = 0
- evidence_refs 指向具体测试函数位置

---

### FP-008 → REQ-008 | 测试追踪链路

**归属 Skill**: pb-review-relation-builder

**描述**: 新增 Feature→TestCaseGroup 和 Rule→NegativeTest 两种关系类型，纳入追踪矩阵。

**验收标准摘要**:
- Feature→TestCaseGroup 映射（基于 D-19 数据）
- Rule→NegativeTest 映射
- 每个关系有 evidence_refs

---

## 1:1 对应校验

| REQ | FP | 状态 |
|-----|-----|------|
| REQ-001 | FP-001 | ✅ |
| REQ-002 | FP-002 | ✅ |
| REQ-003 | FP-003 | ✅ |
| REQ-004 | FP-004 | ✅ |
| REQ-005 | FP-005 | ✅ |
| REQ-006 | FP-006 | ✅ |
| REQ-007 | FP-007 | ✅ |
| REQ-008 | FP-008 | ✅ |
| REQ-009 | FP-009 | ✅ |
| REQ-010 | FP-010 | ✅ |
| REQ-011 | FP-011 | ✅ |
| REQ-012 | FP-012 | ✅ |
| REQ-013 | FP-013 | ✅ |
| REQ-014 | FP-014 | ✅ |
| REQ-015 | FP-015 | ✅ |

**校验结果**: 15 REQ → 15 FP，无遗漏，无溢出。
