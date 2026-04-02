# Product Map: pb-review 标准驱动评估升级

## 决策摘要

**一句话价值**: 让 pb-review 从"能告诉你系统有什么功能"升级为"能告诉你系统离测试就绪还差多远"。

**MVP 裁剪报告**: 全部 15 条需求纳入, 其中 11 条必须(核心升级+报告生成+基础设施)、4 条应该(辅助 skill 升级), 无裁剪。

**风险提示**:
- feature-reconstructor 是最重量级改动(D-17~D-20 + testability_status 判定), 建议最先实现并验证
- 4 个新增 renderer script 需要与现有 render_feature_deliverables.py 保持架构一致
- D-20 的 8 项判定条件较复杂, 需要 gap-analyzer 和 relation-builder 的数据才能完成最终判定

## 功能全景树

```mermaid
mindmap
  root((pb-review 标准驱动评估))
    核心 Skill 升级
      feature-reconstructor
        D-17 Test Oracle 评估
          9 个子项逐项扫描
          完整度计算
        D-18 Fixture Contract 评估
          6 个子项逐项扫描
          完整度计算
        D-19 Test Case Groups 统计
          测试组识别
          用例计数
        D-20 Coverage Claim 判定
          8 项条件检查
          阻塞原因输出
        testability_status 判定
          blocked / partial / test_ready
      gap-analyzer
        missing_feature
        missing_oracle
        missing_fixture_contract
        missing_test_traceability
        严重程度判定
      report-composer
        测试化摘要
        还原 vs 就绪 区分
        testability_score 计算
    辅助 Skill 升级
      project-scope
        5 类 entry surface 扫描
      product-reconstructor
        产品目录完整度评分
      dependency-reconstructor
        Mock/Stub 策略识别
      implementation-mapper
        函数级测试映射
      relation-builder
        Feature-TestCaseGroup 链路
        Rule-NegativeTest 链路
    新增评估报告
      11-testability-scorecard
        M-01 到 M-07 评分
        等级判定
      12-test-case-index
        已有 vs 理想测试对比
        缺口分析
      13-test-fixture-contract
        已有 vs 理想 Fixture 对比
        Mock 策略建议
      14-test-oracle-matrix
        已有 vs 理想 Oracle 对比
        完整度评分
    基础设施升级
      编排器工作流
        新步骤集成
        checkpoint 支持
      模板和脚本
        feature-spec-index 新列
        feature-spec-card D-17 到 D-20
        4 个 renderer script
```

## 用户旅程流

```mermaid
sequenceDiagram
    participant U as 评审执行者
    participant O as pb-review 编排器
    participant PS as project-scope
    participant FR as feature-reconstructor
    participant DR as dependency-reconstructor
    participant IM as implementation-mapper
    participant RB as relation-builder
    participant GA as gap-analyzer
    participant RC as report-composer

    U->>O: 启动评审(project_path, scope)
    O->>PS: 扫描 entry surface
    PS-->>O: entry_surface_inventory(5类入口)

    Note over O: Phase 1: 证据收集和冲突解决(现有流程)

    O->>FR: 还原功能 + D-17到D-20评估
    FR-->>O: feature_spec_registry(含testability_status)
    Note right of FR: 每个功能: oracle完整度, fixture完整度, 测试组数, 覆盖声明

    O->>DR: 分析依赖 + Mock策略
    DR-->>O: dependency_registry + Mock策略

    O->>IM: 建立测试映射(函数级)
    IM-->>O: implementation_registry + Feature到ExistingTest映射

    O->>RB: 建立测试追踪链路
    RB-->>O: traceability_matrix(含测试链路)

    O->>GA: 识别4种gap
    GA-->>O: difference_registry(4种gap + 严重程度)
    Note right of GA: missing_feature, missing_oracle, missing_fixture, missing_traceability

    O->>RC: 生成报告 + 4个评估文档
    RC-->>O: 07-review-report.md(含测试化摘要)
    RC-->>O: 11-testability-scorecard.md
    RC-->>O: 12-test-case-index.md
    RC-->>O: 13-test-fixture-contract.md
    RC-->>O: 14-test-oracle-matrix.md

    O-->>U: 完整交付物 + Testability Score
    Note over U: 清楚知道: 哪些功能可写测试, 哪些被阻塞, 差距多大
```

## 数据流转全景

```mermaid
flowchart TD
    subgraph 输入
        Code[代码仓库]
        Docs[产品文档]
        Tests[测试代码]
        Standard[pb-review-standard.md]
    end

    subgraph Phase1[Phase 1: 证据与冲突]
        PS[project-scope] --> EC[evidence-collector]
        EC --> CR[conflict-resolver]
    end

    subgraph Phase2[Phase 2: 还原与评估]
        PR[product-reconstructor]
        FR[feature-reconstructor]
        DR[dependency-reconstructor]
        IM[implementation-mapper]
    end

    subgraph Phase3[Phase 3: 关系与差距]
        RB[relation-builder]
        GA[gap-analyzer]
    end

    subgraph Phase4[Phase 4: 报告]
        RC[report-composer]
        RS1[render_testability_scorecard.py]
        RS2[render_test_case_index.py]
        RS3[render_fixture_contract.py]
        RS4[render_oracle_matrix.py]
    end

    subgraph 交付物
        D07[07-review-report.md]
        D11[11-testability-scorecard.md]
        D12[12-test-case-index.md]
        D13[13-test-fixture-contract.md]
        D14[14-test-oracle-matrix.md]
    end

    Code --> PS
    Docs --> PS
    Tests --> PS
    Standard --> FR
    Standard --> GA
    Standard --> RC

    CR --> PR
    CR --> FR
    FR --> DR
    FR --> IM
    DR --> RB
    IM --> RB
    RB --> GA
    GA --> RC

    RC --> D07
    RC --> RS1 --> D11
    RC --> RS2 --> D12
    RC --> RS3 --> D13
    RC --> RS4 --> D14
```
