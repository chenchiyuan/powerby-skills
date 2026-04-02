# Spec: pb-review 标准驱动评估升级

**版本**: 1.3.0
**状态**: Draft (Round 4 修复后)
**基于**: proposal.md (Locked)

---

## User Stories

### US-001 → REQ-001

**功能规格卡测试维度评估（D-17 Test Oracle）**

As a 评审执行者,
I want pb-review-feature-reconstructor 在还原功能规格卡时基于 pb-review-standard.md §3.2 的 9 个子项评估 D-17 Test Oracle 完整度,
So that 我能知道每个功能的测试断言标准是否就绪。

**Acceptance Criteria:**

```gherkin
Scenario: D-17 基于标准 9 个子项评估完整度
  Given D-17 评估基于 pb-review-standard.md 3.2 的 9 个子项:
    | 子项编号 | 子项名称 | 检查内容 |
    | D17-1 | 成功输出 Schema | 完整的 JSON/CSV/HTML 结构定义 |
    | D17-2 | 字段级类型 | 每个字段的数据类型和约束 |
    | D17-3 | 必填字段 | 哪些字段必须存在 |
    | D17-4 | 排序规则 | 输出结果的排序逻辑 |
    | D17-5 | 空结果规则 | 空结果的格式和触发条件 |
    | D17-6 | 错误码 Contract | 每个异常的错误码、触发条件、消息 |
    | D17-7 | 文件输出 Contract | 文件格式、编码、列顺序、表头 |
    | D17-8 | 状态变化 Contract | 执行后系统状态的变化 |
    | D17-9 | 业务规则定义 | 所有计算逻辑的公式和规则 |
  When pb-review-feature-reconstructor 对功能 F 逐项扫描代码证据
  Then D-17 完整度 = (已定义子项数 / 适用子项数) x 100%
  And 不适用的子项（如无文件输出的功能不检查 D17-7）不计入分母
  And 每个已定义子项附带 evidence_refs
  And 每个缺失子项标记为"缺失"

Scenario: 代码中存在完整的 Test Oracle（全部适用子项已定义）
  Given 功能 F 有 7 个适用子项（D17-7 文件输出不适用, D17-8 无状态变化）
  And 代码中 7 个适用子项全部有证据
  When pb-review-feature-reconstructor 对功能 F 进行 D-17 评估
  Then D-17 完整度 = 100%（7/7）

Scenario: 代码中部分存在 Test Oracle
  Given 功能 F 有 9 个适用子项
  And 代码中仅有成功输出 Schema（D17-1）和错误码 Contract（D17-6）
  When pb-review-feature-reconstructor 对功能 F 进行 D-17 评估
  Then D-17 完整度 = 22%（2/9）
  And 已有子项标记为"已定义"并附带 evidence_refs
  And 其余 7 项标记为"缺失"

Scenario: 代码中完全没有 Test Oracle 定义
  Given 功能 F 的代码中 9 个子项均无证据
  When pb-review-feature-reconstructor 对功能 F 进行 D-17 评估
  Then D-17 完整度 = 0%
  And 所有子项标记为"缺失"

Scenario: testability_status 判定为 blocked（3 个 OR 条件）
  Given 功能 F 满足以下任一条件:
    - 缺少业务规则定义（D17-9 = 缺失）
    - 缺少数据对象 Schema（D17-1 = 缺失）
    - oracle_completeness < 50
  When pb-review-feature-reconstructor 判定 testability_status
  Then testability_status = "blocked"

Scenario: testability_status 判定为 partial
  Given 功能 F 不满足 blocked 条件
  And oracle_completeness >= 50 且 < 90
  Or fixture_readiness >= 50 且 < 90
  Or test_case_group_count >= 3 且 < 5
  When pb-review-feature-reconstructor 判定 testability_status
  Then testability_status = "partial"

Scenario: testability_status 判定为 test_ready
  Given 功能 F 的 oracle_completeness >= 90
  And fixture_readiness >= 90
  And test_case_group_count >= 5
  And 业务规则已定义（D17-9 != 缺失）
  And 数据对象 Schema 已定义（D17-1 != 缺失）
  When pb-review-feature-reconstructor 判定 testability_status
  Then testability_status = "test_ready"
```

### US-002 → REQ-001

**D-18 Fixture Contract 评估（基于标准 6 个子项）**

As a 评审执行者,
I want pb-review-feature-reconstructor 基于 pb-review-standard.md §3.3 的 6 个子项评估 D-18 Fixture Contract 完整度,
So that 我能知道测试数据准备规范是否就绪。

**Acceptance Criteria:**

```gherkin
Scenario: D-18 基于标准 6 个子项评估完整度
  Given D-18 评估基于 pb-review-standard.md 3.3 的 6 个子项:
    | 子项编号 | 子项名称 | 检查内容 |
    | D18-1 | 最小数据集 | 功能正常运行所需的最小测试数据 |
    | D18-2 | 时间冻结要求 | 是否需要冻结时间及冻结时间点 |
    | D18-3 | 外部依赖 Mock 策略 | 哪些外部依赖需要 mock 及返回值 |
    | D18-4 | 数据库初始状态 | 测试前数据库应处于什么状态 |
    | D18-5 | 前置缓存状态 | 测试前缓存应处于什么状态 |
    | D18-6 | 可复用 Fixture 名称 | 可复用的 fixture 函数名 |
  When pb-review-feature-reconstructor 对功能 F 逐项扫描测试代码证据
  Then D-18 完整度 = (已定义子项数 / 适用子项数) x 100%
  And 不适用的子项不计入分母
  And 每个已定义子项附带 evidence_refs
  And 每个缺失子项标记为"缺失"

Scenario: 测试代码中有完整的 Fixture 定义
  Given 功能 F 的测试代码中所有适用子项均有证据
  When pb-review-feature-reconstructor 对功能 F 进行 D-18 评估
  Then D-18 完整度 = 100%

Scenario: 测试代码中无任何 Fixture 定义
  Given 功能 F 没有测试文件或测试文件中无 fixture
  When pb-review-feature-reconstructor 对功能 F 进行 D-18 评估
  Then D-18 完整度 = 0%
  And 所有子项标记为"缺失"
```

### US-003 → REQ-001

**D-19 Test Case Groups 统计**

As a 评审执行者,
I want pb-review-feature-reconstructor 统计每个功能的测试用例分组数量,
So that 我能知道测试覆盖的系统性程度。

**Acceptance Criteria:**

```gherkin
Scenario: 统计已有测试用例分组
  Given 功能 F 的测试文件中有多个测试类或描述性分组
  When pb-review-feature-reconstructor 统计 D-19
  Then test_case_group_count = 实际识别到的分组数量
  And 每个分组有名称和包含的测试用例数

Scenario: 功能没有测试文件
  Given 功能 F 没有对应的测试文件
  When pb-review-feature-reconstructor 统计 D-19
  Then test_case_group_count = 0
```

### US-004 → REQ-001

**D-20 Coverage Claim 判定**

As a 评审执行者,
I want pb-review-feature-reconstructor 判定每个功能是否允许覆盖声明,
So that 我能防止虚假的"coverage = 100%"。

**Acceptance Criteria:**

```gherkin
Scenario: 功能达到 coverage_claim_allowed = yes（对齐标准 3.5 全部 8 项）
  Given 功能 F 满足以下全部条件:
    - D-17 oracle_completeness >= 90
    - D-18 fixture_readiness >= 90
    - D-19 test_case_group_count >= 8
    - 业务规则已定义（D17-9 != 缺失）
    - 数据对象 Schema 已定义（D17-1 != 缺失）
    - 所有错误码都有对应测试用例
    - 所有边界条件都有对应测试用例
    - 无未闭合的 gap
  When pb-review-feature-reconstructor 判定 D-20
  Then coverage_claim_allowed = "yes"
  And 输出覆盖范围（当前规格卡覆盖的能力范围）
  And 输出未覆盖子能力清单（如有）

Scenario: 功能未达到覆盖声明条件
  Given 功能 F 不满足 coverage_claim_allowed = yes 的任一条件
  When pb-review-feature-reconstructor 判定 D-20
  Then coverage_claim_allowed = "no"
  And 输出阻塞原因清单
  And 输出未闭合断言点清单
  And 输出未标准化 fixture 清单
```

### US-005 → REQ-002

**四种 Gap 类型识别**

As a 评审执行者,
I want pb-review-gap-analyzer 能识别 4 种类型的差距,
So that 我能全面了解系统离测试就绪的差距分布。

**Acceptance Criteria:**

```gherkin
Scenario: 识别 missing_feature gap
  Given 权威文档声明了功能 X
  But 功能索引中没有功能 X
  When pb-review-gap-analyzer 分析差距
  Then 输出 gap 类型 = "missing_feature"
  And 严重程度按判定规则确定

Scenario: 识别 missing_oracle gap
  Given 功能 F 存在于功能索引中
  But D-17 oracle_completeness = 0%（完全缺失 Oracle 定义）
  When pb-review-gap-analyzer 分析差距
  Then 输出 gap 类型 = "missing_oracle"
  And 严重程度 = "Critical"（无法判断功能是否正确）

Scenario: 识别 missing_oracle gap（部分缺失）
  Given 功能 F 存在于功能索引中
  And D-17 oracle_completeness > 0% 且 < 50%
  When pb-review-gap-analyzer 分析差距
  Then 输出 gap 类型 = "missing_oracle"
  And 严重程度 = "Major"（Oracle 不完整，无法完整生成测试）

Scenario: 识别 missing_fixture_contract gap
  Given 功能 F 存在于功能索引中
  But D-18 fixture_readiness = 0%（完全缺失 Fixture 定义）
  When pb-review-gap-analyzer 分析差距
  Then 输出 gap 类型 = "missing_fixture_contract"
  And 严重程度 = "Major"

Scenario: 识别 missing_test_traceability gap
  Given 功能 F 存在于功能索引中
  But 没有 Feature->TestCaseGroup 链路
  When pb-review-gap-analyzer 分析差距
  Then 输出 gap 类型 = "missing_test_traceability"
  And 严重程度 = "Major"

Scenario: Gap 严重程度判定
  Given 识别到一个 gap
  When 判定严重程度
  Then Critical = 无法判断功能正确性 OR 无法编写任何测试 OR 阻塞整个功能测试化
  And Major = 无法完整生成测试组 OR 测试不稳定 OR 影响覆盖率 >= 20%
  And Minor = 可以写测试但稳定性不足 OR 影响覆盖率 < 20%
```

### US-006 → REQ-003

**测试化摘要报告**

As a 评审执行者,
I want pb-review-report-composer 生成明确区分"还原"和"就绪"的报告,
So that 我能一眼看出哪些功能可以开始写测试、哪些被阻塞。

**Acceptance Criteria:**

```gherkin
Scenario: 报告包含测试化摘要
  Given 所有功能已评估完 testability_status
  When pb-review-report-composer 生成报告
  Then 报告包含 testability_score（加权计算 M-01~M-07）
  And 报告包含 test_ready 功能数和清单
  And 报告包含 blocked 功能数和阻塞原因清单
  And 报告包含 partial 功能数和缺失项清单

Scenario: 报告区分"已还原"和"测试就绪"
  Given 功能总数 = 20, test_ready = 12, blocked = 3, partial = 5
  When pb-review-report-composer 生成报告
  Then 报告"已还原能力"章节列出全部 20 个功能
  And 报告"测试就绪能力"章节列出 12 个 test_ready 功能
  And 报告"阻塞能力"章节列出 3 个 blocked 功能及具体阻塞原因
  And 报告不使用"completed"掩盖 test_ready 不足

Scenario: testability_score 计算（采用 pb-review-standard.md 4.1 公式）
  Given 本 spec 采用 pb-review-standard.md 4.1 的 Testability Score 公式为唯一口径:
    score = 25% x M-01(功能闭合完成率)
           + 10% x M-02(原子功能率)
           + 20% x M-03(Oracle完整率)
           + 15% x M-04(Fixture完整率)
           + 10% x M-05(测试追踪完整率)
           + 10% x M-06(规则负向覆盖率)
           + 10% x M-07(覆盖宣称可信率)
  And M-01 = 100%, M-02 = 95%, M-03 = 80%, M-04 = 70%, M-05 = 60%, M-06 = 50%, M-07 = 40%
  When 计算 testability_score
  Then score = 25 + 9.5 + 16 + 10.5 + 6 + 5 + 4 = 76
  And 等级 = B
```

### US-007 → REQ-004

**Entry Surface 全面扫描**

As a 评审执行者,
I want pb-review-project-scope 对照标准扫描所有入口类型,
So that 不会遗漏任何功能入口。

**Acceptance Criteria:**

```gherkin
Scenario: 扫描 5 类 entry surface
  Given 目标项目存在 CLI 命令、HTTP API、页面路由、定时任务、服务编排
  When pb-review-project-scope 执行扫描
  Then 输出 entry_surface_inventory 包含 5 类入口清单
  And 每个入口有类型标识（cli/api/page/cron/orchestration）
  And 每个入口有路径信息
```

### US-008 → REQ-005

**产品目录完整度评估**

As a 评审执行者,
I want pb-review-product-reconstructor 对照标准评估产品目录完整度,
So that 我能知道产品定义的质量水平。

**Acceptance Criteria:**

```gherkin
Scenario: 评估产品目录完整度
  Given 产品文档中有 Goal、Scenario、Constraint 定义
  When pb-review-product-reconstructor 评估完整度
  Then 输出 Goal 可量化率（有可量化成功标准的 Goal 数 / Goal 总数）
  And 输出 Scenario 完整率（有进入/退出条件的 Scenario 数 / Scenario 总数）
  And 输出 Constraint 可追踪率（能映射到功能的 Constraint 数 / Constraint 总数）
  And 输出产品目录完整度总评分 = (Goal可量化率 + Scenario完整率 + Constraint可追踪率) / 3
  And 输出等级判定: A(>=90) / B(75-89) / C(60-74) / D(<60)

Scenario: 产品文档缺失时的降级处理
  Given 用户未提供 product_docs_dir
  When pb-review-product-reconstructor 评估完整度
  Then 所有分项比率 = 0%, 总评分 = 0, 等级 = D
  And 输出"产品文档缺失"提示
```

### US-009 → REQ-006

**测试依赖识别**

As a 评审执行者,
I want pb-review-dependency-reconstructor 补充测试依赖维度,
So that D-18 Fixture Contract 有外部依赖信息可用。

**Acceptance Criteria:**

```gherkin
Scenario: 识别外部依赖并建议 Mock 策略
  Given 功能 F 依赖外部 API、数据库、缓存
  When pb-review-dependency-reconstructor 分析依赖
  Then 输出每个外部依赖的 Mock/Stub 策略建议
  And 标注哪些依赖已有 Mock（evidence_refs 指向测试代码）
  And 标注哪些依赖缺少 Mock
```

### US-010 → REQ-007

**测试映射建立**

As a 评审执行者,
I want pb-review-implementation-mapper 建立 Feature->ExistingTest 映射,
So that 我能知道哪些功能已有测试覆盖。

**Acceptance Criteria:**

```gherkin
Scenario: 建立 Feature->ExistingTest 映射（函数级粒度）
  Given 功能 F 有对应的测试文件
  When pb-review-implementation-mapper 建立映射
  Then 输出 Feature->ExistingTest 映射（粒度到测试函数/方法）
  And 每个映射包含: test_file, test_function_name, test_level(unit/integration/e2e)
  And 标注该功能的已有测试用例总数
  And evidence_refs 指向具体测试函数位置

Scenario: 功能无对应测试
  Given 功能 F 没有对应的测试文件或测试函数
  When pb-review-implementation-mapper 建立映射
  Then 输出空映射
  And 标注 existing_test_count = 0
```

### US-011 → REQ-008

**测试追踪链路**

As a 评审执行者,
I want pb-review-relation-builder 建立测试追踪链路,
So that 追踪矩阵能覆盖测试维度。

**Acceptance Criteria:**

```gherkin
Scenario: 建立 Feature->TestCaseGroup 关系
  Given 功能 F 有 D-19 测试组定义
  When pb-review-relation-builder 建立关系
  Then 输出 Feature->TestCaseGroup 映射
  And 每个关系有 evidence_refs

Scenario: 建立 Rule->NegativeTest 关系
  Given 业务规则 R 有对应的负向测试
  When pb-review-relation-builder 建立关系
  Then 输出 Rule->NegativeTest 映射
```

### US-012 → REQ-009

**Testability Scorecard 生成**

As a 评审执行者,
I want pb-review-report-composer 生成 11-testability-scorecard.md,
So that 我能一眼看到系统的测试化就绪程度。

**Acceptance Criteria:**

```gherkin
Scenario: 生成测试化评分卡
  Given 所有功能已完成 D-17~D-20 评估
  And 所有 gap 已识别并分类
  When pb-review-report-composer 调用 render_testability_scorecard.py 生成 11-testability-scorecard.md
  Then 包含 M-01~M-07 当前评分
  And 包含目标评分（90-100）
  And 包含差距分析（当前值 vs 目标值）
  And 包含综合 Testability Score 和等级（A/B/C/D）
  And 包含改造优先级建议
```

### US-013 → REQ-010

**Test Case Index 生成**

As a 评审执行者,
I want pb-review-report-composer 生成 12-test-case-index.md,
So that 我能看到已有测试和理想测试的全景对比。

**Acceptance Criteria:**

```gherkin
Scenario: 生成测试用例索引
  Given 所有功能的 D-19 已评估
  And implementation-mapper 已建立 Feature->Test 映射
  And 标准 8 个必需测试组定义如下:
    | 组编号 | 组名称 | 描述 |
    | TG-1 | 正向功能测试 | 验证核心功能的正常路径 |
    | TG-2 | 边界条件测试 | 验证输入边界和极端值 |
    | TG-3 | 异常/错误路径测试 | 验证错误处理和异常恢复 |
    | TG-4 | 数据验证测试 | 验证输入校验和数据完整性 |
    | TG-5 | 状态转换测试 | 验证状态机和流程转换 |
    | TG-6 | 并发/竞态测试 | 验证并发安全性（如适用） |
    | TG-7 | 性能基线测试 | 验证响应时间和吞吐量基线（如适用） |
    | TG-8 | 集成契约测试 | 验证与外部依赖的交互契约 |
  When pb-review-report-composer 调用 render_test_case_index.py 生成 12-test-case-index.md
  Then 包含已有测试用例清单（来源: 代码扫描, Feature->ExistingTest 映射）
  And 包含理想测试组清单（来源: 上述标准 8 组, 不适用的组标记为 not_applicable）
  And 包含缺口分析（理想 - 已有 = 缺口, 按组逐项对比）
  And 包含优先级建议（先补 P0 缺口: TG-1 正向功能 > TG-3 错误路径 > TG-2 边界条件）
```

### US-014 → REQ-011

**Fixture Contract 报告生成**

As a 评审执行者,
I want pb-review-report-composer 生成 13-test-fixture-contract.md,
So that 我能看到测试数据准备的差距。

**Acceptance Criteria:**

```gherkin
Scenario: 生成 Fixture Contract 报告
  Given 所有功能的 D-18 已评估
  And dependency-reconstructor 已识别外部依赖
  When pb-review-report-composer 调用 render_fixture_contract.py 生成 13-test-fixture-contract.md
  Then 包含已有 Fixture 清单（来源: 测试代码扫描）
  And 包含理想 Fixture 清单（来源: D-18 标准）
  And 包含缺口分析
  And 包含 Mock/Stub 策略建议
```

### US-015 → REQ-012

**Oracle Matrix 报告生成**

As a 评审执行者,
I want pb-review-report-composer 生成 14-test-oracle-matrix.md,
So that 我能看到测试断言标准的差距。

**Acceptance Criteria:**

```gherkin
Scenario: 生成 Oracle Matrix 报告
  Given 所有功能的 D-17 已评估
  When pb-review-report-composer 调用 render_oracle_matrix.py 生成 14-test-oracle-matrix.md
  Then 包含已有 Oracle 清单（来源: 代码中的 Schema、错误码、业务规则）
  And 包含理想 Oracle 清单（来源: D-17 标准的 9 项内容）
  And 包含缺口分析
  And 每个功能的 Oracle 完整度评分
```

### US-016 → REQ-013

**编排器工作流升级**

As a 评审执行者,
I want pb-review 编排器集成新增的 4 个报告生成步骤,
So that 一次评审执行就能产出全部交付物。

**Acceptance Criteria:**

```gherkin
Scenario: 工作流包含新增步骤
  Given 用户启动 pb-review 评审
  When 工作流执行到报告阶段
  Then 在 07-review-report.md 之后依次生成:
    | 步骤 | 交付物 | renderer script |
    | 11 | 11-testability-scorecard.md | render_testability_scorecard.py |
    | 12 | 12-test-case-index.md | render_test_case_index.py |
    | 13 | 13-test-fixture-contract.md | render_fixture_contract.py |
    | 14 | 14-test-oracle-matrix.md | render_oracle_matrix.py |
  And checkpoint 记录每个新步骤的完成状态
  And deliverable_manifest 包含所有新交付物

Scenario: 断点恢复支持新步骤
  Given 评审在步骤 12 失败
  And 用户以 resume=true 重新启动
  When pb-review 恢复执行
  Then 从步骤 12 继续, 不重复步骤 1~11
```

### US-017 → REQ-014

**Feature Spec Index 模板升级**

As a 评审执行者,
I want 功能规格索引表包含测试维度列,
So that 我能从索引层面快速筛选 test_ready 功能。

**Acceptance Criteria:**

```gherkin
Scenario: 索引表包含新列
  Given 功能规格索引表已生成
  When 查看 03-feature-spec-index.md
  Then 表格包含以下新增列:
    | 列名 | 取值范围 |
    | testability_status | blocked/partial/test_ready |
    | oracle_completeness | 0-100 |
    | fixture_readiness | 0-100 |
    | test_case_group_count | >= 0 |
    | coverage_claim_allowed | yes/no |
```

### US-018 → REQ-015

**Feature Spec Card 模板升级**

As a 评审执行者,
I want 功能规格卡包含 D-17~D-20 章节,
So that 每个功能的测试就绪状态有完整文档。

**Acceptance Criteria:**

```gherkin
Scenario: 规格卡包含 D-17~D-20
  Given 功能 F 的规格卡已生成
  When 查看 04-feature-specs/{function_id}.md
  Then 包含 D-17 Test Oracle 章节（9 个子项各自的状态和完整度评分）
  And 包含 D-18 Fixture Contract 章节（6 个子项各自的状态和完整度评分）
  And 包含 D-19 Test Case Groups 章节（测试组清单、每组测试用例数）
  And 包含 D-20 Coverage Claim 章节（是否允许覆盖声明、未覆盖子能力、阻塞原因）
  And 每项有"已定义/缺失"状态标记
  And "已定义"项有 evidence_refs 指向代码位置
```

---

## Data Flow: D-17~D-20 数据在 skill 间的流转

### context_writes 数据结构

feature-reconstructor 将 D-17~D-20 评估数据写入 `feature_spec_registry` 的扩展字段:

```yaml
feature_spec_registry[i]:
  # 现有字段保持不变
  function_id: string
  feature_type: string
  entry_surface: string
  # ... D-01~D-16 ...

  # 新增 D-17~D-20 字段
  d17_oracle:
    completeness: number  # 0-100
    sub_items:
      - id: "D17-1"
        name: "成功输出 Schema"
        status: "defined" | "missing" | "not_applicable"
        evidence_refs: array | null
      # ... D17-2 到 D17-9
  d18_fixture:
    completeness: number  # 0-100
    sub_items:
      - id: "D18-1"
        name: "最小数据集"
        status: "defined" | "missing" | "not_applicable"
        evidence_refs: array | null
      # ... D18-2 到 D18-6
  d19_test_groups:
    count: number
    groups:
      - name: string
        test_count: number
        evidence_refs: array
  d20_coverage_claim:
    allowed: "yes" | "no"
    coverage_scope: string | null  # 当前规格卡覆盖的能力范围
    blocking_reasons: array | null
    uncovered_sub_capabilities: array | null
    unclosed_assertion_points: array | null  # 未闭合断言点
    unstandardized_fixtures: array | null    # 未标准化 fixture

  # 聚合判定
  testability_status: "blocked" | "partial" | "test_ready"
  oracle_completeness: number  # = d17_oracle.completeness
  fixture_readiness: number    # = d18_fixture.completeness
  test_case_group_count: number  # = d19_test_groups.count
  coverage_claim_allowed: "yes" | "no"  # = d20_coverage_claim.allowed
```

### Skill 间数据流转路径

```
pb-review-project-scope
  └─ 输出: entry_surface_inventory（含 entry surface 类型）
      │
pb-review-feature-reconstructor
  ├─ 读取: entry_surface_inventory、evidence_registry、current_facts
  ├─ 输出: feature_spec_registry（含 D-17~D-20 扩展字段）
  └─ 输出: feature_state_registry（含 testability_status）
      │
pb-review-dependency-reconstructor
  ├─ 读取: feature_spec_registry
  ├─ 输出: dependency_registry（结构见下方 schema）
  └─ 反写: feature_spec_registry[i].d18_fixture.sub_items 中 D18-3 的 evidence_refs
      │
pb-review-implementation-mapper
  |-- 读取: feature_spec_registry
  |-- 输出: implementation_registry（含 test_mapping 字段, 粒度到测试函数）
  +-- 输出: Feature->ExistingTest 映射（函数级）
      │
pb-review-relation-builder
  ├─ 读取: feature_spec_registry, implementation_registry
  ├─ 输出: traceability_matrix（含 Feature->TestCaseGroup, Rule->NegativeTest）
  └─ 输出: 关系清单
      │
pb-review-gap-analyzer
  ├─ 读取: feature_spec_registry（D-17~D-20 字段）、traceability_matrix
  ├─ 输出: difference_registry（含 4 种 gap 类型 + 严重程度）
  └─ 输出: 06-gap-analysis.md
      │
pb-review-report-composer
  ├─ 读取: feature_spec_registry, difference_registry, traceability_matrix
  ├─ 输出: 07-review-report.md（含测试化摘要）
  ├─ 调用: render_testability_scorecard.py → 11-testability-scorecard.md
  ├─ 调用: render_test_case_index.py → 12-test-case-index.md
  ├─ 调用: render_fixture_contract.py → 13-test-fixture-contract.md
  └─ 调用: render_oracle_matrix.py → 14-test-oracle-matrix.md
```

### Renderer Script 归属

4 个新增报告的 renderer script 统一归属于 `pb-review-report-composer` skill:

| 交付物 | Renderer Script | 归属 Skill | 输入数据 |
|--------|----------------|-----------|---------|
| 11-testability-scorecard.md | render_testability_scorecard.py | pb-review-report-composer | feature_spec_registry(全量), difference_registry |
| 12-test-case-index.md | render_test_case_index.py | pb-review-report-composer | feature_spec_registry[].d19_test_groups, implementation_registry |
| 13-test-fixture-contract.md | render_fixture_contract.py | pb-review-report-composer | feature_spec_registry[].d18_fixture, dependency_registry |
| 14-test-oracle-matrix.md | render_oracle_matrix.py | pb-review-report-composer | feature_spec_registry[].d17_oracle |

### dependency_registry 数据结构

dependency-reconstructor 输出的 `dependency_registry` 结构:

```yaml
dependency_registry[i]:
  function_id: string           # 关联的功能 ID
  dependency_name: string       # 外部依赖名称（如 "payment-gateway-api"）
  dependency_type: string       # 依赖类型: api / database / cache / message_queue / file_system
  has_mock: boolean             # 测试代码中是否已有 Mock
  mock_evidence_refs: array | null  # 已有 Mock 的代码证据（has_mock=true 时必填）
  mock_strategy: string | null  # 建议的 Mock 策略: stub / fake / spy / mock_server / not_needed
  mock_priority: string         # 优先级: high（核心依赖）/ medium / low
```

render_fixture_contract.py 从 `dependency_registry` 中读取 Mock 策略信息，与 `feature_spec_registry[].d18_fixture` 合并生成 13-test-fixture-contract.md。

---

## Data Dictionary

| 术语 | 定义 | 数据类型 |
|------|------|---------|
| testability_status | 功能的测试就绪状态 | enum: blocked / partial / test_ready |
| oracle_completeness | D-17 Test Oracle 完整度（基于 9 个子项） | number: 0-100 |
| fixture_readiness | D-18 Test Fixture Contract 完整度（基于 6 个子项） | number: 0-100 |
| test_case_group_count | D-19 测试用例分组数量 | number: >= 0 |
| coverage_claim_allowed | D-20 是否允许覆盖声明 | enum: yes / no |
| testability_score | 系统级测试化评分（M-01~M-07 加权） | number: 0-100 |
| gap_type | 差距类型 | enum: missing_feature / missing_oracle / missing_fixture_contract / missing_test_traceability |
| gap_severity | 差距严重程度 | enum: Critical / Major / Minor |
| evidence_refs | 代码证据引用 | array of {file_path, line_range, type} |
| entry_surface | 功能入口类型 | enum: cli / api / page / cron / orchestration |
| d17_sub_item_status | D-17 子项状态 | enum: defined / missing / not_applicable |
| d18_sub_item_status | D-18 子项状态 | enum: defined / missing / not_applicable |
| entry_surface_inventory | project-scope 输出的入口清单 | array of {type: entry_surface, path: string, name: string} |
| feature_spec_registry | 功能规格注册表（含 D-01~D-20 全部字段） | array of feature_spec object |
| feature_state_registry | 功能状态注册表（含 testability_status） | array of {function_id, testability_status, last_updated} |
| dependency_registry | 外部依赖注册表（含 Mock 策略） | array of {function_id, dependency_name, dependency_type, has_mock, mock_strategy, ...} |
| implementation_registry | 实现映射注册表（含测试映射） | array of {function_id, source_files, test_mapping} |
| difference_registry | 差距注册表（含 4 种 gap 类型） | array of {gap_id, gap_type, gap_severity, function_id, description} |
| traceability_matrix | 追踪矩阵（含测试链路） | object: {feature_to_test, rule_to_negative_test, ...} |
| product_docs_dir | 产品文档目录路径（用户输入参数） | string (file path) |
| existing_test_count | 功能已有测试用例总数 | number: >= 0 |
| coverage_scope | D-20 当前规格卡覆盖的能力范围 | string (描述性文本) |
| blocking_reasons | D-20 阻塞原因清单 | array of string |
| uncovered_sub_capabilities | D-20 未覆盖子能力清单 | array of string |
| unclosed_assertion_points | D-20 未闭合断言点清单 | array of string |
| unstandardized_fixtures | D-20 未标准化 fixture 清单 | array of string |
| mock_strategy | 外部依赖的 Mock 策略建议 | enum: stub / fake / spy / mock_server / not_needed |
| test_mapping | 功能到测试函数的映射 | array of {test_file, test_function_name, test_level} |
| test_level | 测试层级 | enum: unit / integration / e2e |
| deliverable_manifest | 交付物清单（checkpoint 机制） | array of {step, file_path, status} |

---

## 状态定义

### Feature Testability 状态机

```
blocked -> partial -> test_ready
  ^         ^
  +---------+ (随着缺失项补充, 状态逐步升级)
```

| 状态 | 进入条件 | 说明 |
|------|---------|------|
| blocked | oracle_completeness < 50 OR D17-9 缺失 OR D17-1 缺失 | 无法编写任何有意义的测试 |
| partial | 不满足 blocked, 且 oracle_completeness < 90 OR fixture_readiness < 90 OR test_case_group_count < 5 | 可编写部分测试, 但不完整 |
| test_ready | oracle >= 90 AND fixture >= 90 AND groups >= 5 AND D17-9 已定义 AND D17-1 已定义 | 可直接进入 TDD |

### 评审工作流状态

| 步骤 | Empty State | Loading State | Error State | Success State |
|------|------------|---------------|-------------|---------------|
| D-17 评估 | "未扫描: 功能尚未进行 Oracle 评估" | "评估中: 正在扫描代码证据..." | "评估失败: {error_message}" | "完整度 N%, 已定义 X/Y 项" |
| D-18 评估 | "未扫描: 功能尚未进行 Fixture 评估" | "评估中: 正在扫描测试代码..." | "评估失败: {error_message}" | "完整度 N%, 已定义 X/Y 项" |
| D-19 统计 | "未统计: 功能尚未进行测试组统计" | "统计中: 正在识别测试分组..." | "统计失败: {error_message}" | "N 个测试组, 共 M 个测试用例" |
| D-20 判定 | "未判定: 功能尚未进行覆盖声明判定" | "判定中: 正在检查 8 项条件..." | "判定失败: {error_message}" | "allowed=yes/no, 原因: {reason}" |
| Scorecard 生成 | "未生成: 缺少前置数据" | "生成中: 正在计算 M-01~M-07..." | "生成失败: {error_message}" | "Testability Score = N, 等级 = X" |

---

## Traceability Matrix

| Proposal REQ | Spec US | 覆盖状态 |
|-------------|---------|---------|
| REQ-001 | US-001, US-002, US-003, US-004 | ✅ 已覆盖 |
| REQ-002 | US-005 | ✅ 已覆盖 |
| REQ-003 | US-006 | ✅ 已覆盖 |
| REQ-004 | US-007 | ✅ 已覆盖 |
| REQ-005 | US-008 | ✅ 已覆盖 |
| REQ-006 | US-009 | ✅ 已覆盖 |
| REQ-007 | US-010 | ✅ 已覆盖 |
| REQ-008 | US-011 | ✅ 已覆盖 |
| REQ-009 | US-012 | ✅ 已覆盖 |
| REQ-010 | US-013 | ✅ 已覆盖 |
| REQ-011 | US-014 | ✅ 已覆盖 |
| REQ-012 | US-015 | ✅ 已覆盖 |
| REQ-013 | US-016 | ✅ 已覆盖 |
| REQ-014 | US-017 | ✅ 已覆盖 |
| REQ-015 | US-018 | ✅ 已覆盖 |
