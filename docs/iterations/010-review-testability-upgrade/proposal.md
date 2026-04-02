# Proposal: pb-review 标准驱动评估升级

## 1. 产品定位
- **目标用户**：使用 pb-review skill suite 对项目进行评审的开发者/团队负责人
- **核心价值**：让 pb-review 从"还原式评审"升级为"标准驱动的评估流程"，能量化回答"离测试就绪还差多远"
- **成功指标**：
  - 每个功能都有 testability_status 判定（blocked/partial/test_ready）
  - 能计算 Testability Score（基于 M-01~M-07 量化指标）
  - 在 archer 项目验证时 score >= 75 分
  - 能生成 4 类评估报告（scorecard、test-case-index、fixture-contract、oracle-matrix）

## 2. 需求清单

| ID | 需求描述 | 优先级 | 验收标准（草案） |
|----|---------|--------|----------------|
| REQ-001 | 升级 pb-review-feature-reconstructor：新增 D-17(Test Oracle)、D-18(Fixture Contract)、D-19(Test Case Groups)、D-20(Coverage Claim) 四个维度的评估能力，判定 testability_status | 必须 | 每个功能规格卡包含 D-17~D-20 章节，有量化完整度评分（0-100%），有 testability_status 判定（blocked/partial/test_ready），缺失项标记为"缺失"而非编造 |
| REQ-002 | 升级 pb-review-gap-analyzer：从只识别 missing_feature 扩展为识别 4 种 gap 类型 | 必须 | 能识别 missing_feature、missing_oracle、missing_fixture_contract、missing_test_traceability 四种类型，每个 gap 有严重程度判定（Critical/Major/Minor），判定规则符合 pb-review-standard.md L1-2.5 |
| REQ-003 | 升级 pb-review-report-composer：区分"还原"和"就绪"，生成测试化摘要 | 必须 | 报告包含 testability score（基于 M-01~M-07 计算）、test_ready 功能数、blocked 功能数、不允许进入 TDD 的阻塞项清单，明确区分"已还原"和"测试就绪" |
| REQ-004 | 升级 pb-review-project-scope：对照标准扫描所有 entry surface 类型 | 必须 | 按 R-01 标准扫描 CLI/API/页面/定时任务/服务编排 5 类入口，输出 entry surface 清单供 feature-reconstructor 使用 |
| REQ-005 | 升级 pb-review-product-reconstructor：评估产品目录完整度 | 应该 | 评估 Goal 可量化率、Scenario 完整率、Constraint 可追踪率，输出产品目录完整度评分 |
| REQ-006 | 升级 pb-review-dependency-reconstructor：补充测试依赖维度 | 应该 | 识别外部依赖并输出 Mock/Stub 策略建议，为 D-18 Fixture Contract 提供数据 |
| REQ-007 | 升级 pb-review-implementation-mapper：补充测试映射维度 | 应该 | 建立 Feature→ExistingTest 映射链路，识别已有测试覆盖 |
| REQ-008 | 升级 pb-review-relation-builder：补充测试追踪链路 | 应该 | 新增 Feature→TestCaseGroup 和 Rule→NegativeTest 两种关系类型 |
| REQ-009 | 新增报告：11-testability-scorecard.md 生成能力 | 必须 | 包含 M-01~M-07 当前评分、目标评分（90-100）、差距分析、等级判定（A/B/C/D） |
| REQ-010 | 新增报告：12-test-case-index.md 生成能力 | 必须 | 包含已有测试用例清单、按 D-19 标准的理想测试组清单、缺口分析、优先级建议 |
| REQ-011 | 新增报告：13-test-fixture-contract.md 生成能力 | 必须 | 包含已有 Fixture 清单、按 D-18 标准的理想 Fixture 清单、缺口分析 |
| REQ-012 | 新增报告：14-test-oracle-matrix.md 生成能力 | 必须 | 包含已有 Oracle 清单、按 D-17 标准的理想 Oracle 清单、缺口分析 |
| REQ-013 | 升级 pb-review 编排器：集成新增交付物到工作流 | 必须 | 工作流在现有步骤之后增加 4 个报告生成步骤，checkpoint 支持新步骤，deliverable_manifest 包含新交付物 |
| REQ-014 | 升级 feature-spec-index 模板和渲染脚本 | 必须 | 索引表新增 testability_status、oracle_completeness、fixture_readiness、test_case_group_count、coverage_claim_allowed 列 |
| REQ-015 | 升级 feature-spec-card 模板 | 必须 | 规格卡新增 D-17 Test Oracle、D-18 Fixture Contract、D-19 Test Case Groups、D-20 Coverage Claim 四个章节 |

## 3. 明确排除

| ID | 排除项 | 排除理由 |
|----|--------|---------|
| EXC-001 | 自动改造/修复代码中缺失的 Oracle 或 Fixture | pb-review 职责是还原现状+识别差距，改造是使用方的职责 |
| EXC-002 | 在 archer 项目上实际运行验证 | 验证是后续阶段任务，不在本迭代规格范围内 |
| EXC-003 | 修改 pb-review-standard.md 标准文档 | 标准文档已完成（方向1），本迭代基于已有标准升级 skill |
| EXC-004 | 新增 LLM HTTP 调用或后端推理代理 | 遵循 009 架构约束：抽象判断由当前宿主模型直接执行 |

## 4. 约束条件

| ID | 约束描述 |
|----|---------|
| CON-001 | 必须遵循 009-review-framework 已建立的架构原则：顺序执行、checkpoint 恢复、renderer script 落盘、deliverable_manifest 维护 |
| CON-002 | 所有"已定义"的判断都必须有代码证据支撑（evidence_refs），不能因为标准要求就编造内容 |
| CON-003 | 标准（pb-review-standard.md）是衡量尺度，pb-review 只负责还原现状 + 识别差距，不负责改造 |
| CON-004 | 禁止使用 llm_client.py 或 HTTP chat-completions 做后端推理代理 |
