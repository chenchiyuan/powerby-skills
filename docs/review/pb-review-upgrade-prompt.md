# pb-review 升级提示词

**版本**: 1.0.0
**制定日期**: 2026-03-30
**用途**: 指导pb-review流程升级，建立测试化标准体系

---

## 升级目标

将pb-review从"还原式评审流程"升级为"标准驱动的评估流程"，核心是**建立标准先行**的工作模式。

---

## 核心原则

### 1. 标准先行
- **先建立标准**：定义测试化的理想状态（what should be）
- **再还原现状**：对照标准，从代码中还原当前状态（what is）
- **最后识别差距**：明确指出哪些标准未达到，差距有多大（gap）

### 2. 职责清晰
- **pb-review的职责**：还原现状 + 识别差距
- **标准的作用**：定义理想状态，作为衡量尺度
- **改造的职责**：基于差距补充内容（不是pb-review的职责）

### 3. 尊重事实
- pb-review必须尊重已有事实，不能创造不存在的内容
- 如果代码中没有Test Oracle定义，应标记为"缺失"，而不是编造一个
- 所有"已定义"的判断都必须有代码证据支撑

---

## 升级方向

### 方向1: 建立独立的标准文档

**目标**：创建 `pb-review-standard.md`，作为pb-review还原的参照目标和gap识别的参照物。

**标准文档应包含**：

#### L1 交付物标准
定义6个交付物的理想状态：
- 02-product-catalog.md：产品目录应包含哪些内容
- 03-feature-spec-index.md：功能索引应包含哪些列
- 04-feature-specs/*.md：功能规格卡应包含哪些维度
- 05-traceability-matrix.md：追踪矩阵应包含哪些链路
- 06-gap-analysis.md：差距分析应识别哪些gap类型
- 07-review-report.md：评审报告应包含哪些摘要

#### L2 功能规格标准
定义功能规格卡的理想状态：
- D-01到D-16：现有维度的标准（引用现有文档）
- **D-17 Test Oracle**：定义测试断言标准
  - 成功输出Schema（JSON Schema格式）
  - 错误码Contract（错误码表）
  - 业务规则定义（计算公式、分类规则）
- **D-18 Test Fixture Contract**：定义测试数据准备规范
  - 最小数据集
  - 时间冻结要求
  - 外部依赖Mock策略
- **D-19 Test Case Groups**：定义测试用例分组
  - 8个必需测试组（主成功路径、参数校验、边界值、异常路径等）
- **D-20 Coverage Claim**：定义测试覆盖声明
  - 允许覆盖声明的判定规则

#### L3 测试资产标准
定义测试资产的理想状态：
- 11-testability-scorecard.md：测试化评分卡标准
- 12-test-case-index.md：测试用例索引标准
- 13-test-fixture-contract.md：Fixture Contract标准
- 14-test-oracle-matrix.md：Test Oracle矩阵标准

#### L4 质量门禁标准
定义测试就绪的判定标准：
- 功能原子化标准（R-01到R-04）
- 测试就绪标准（12项检查清单）
- 系统测试就绪标准（8项判定标准）

#### 量化指标标准
定义7个量化指标的计算公式和目标值：
- M-01 功能闭合集合完成率 = 100%
- M-02 原子功能率 ≥ 95%
- M-03 Oracle完整率 ≥ 90%
- M-04 Fixture完整率 ≥ 90%
- M-05 测试追踪完整率 = 100%
- M-06 规则负向覆盖率 = 100%
- M-07 覆盖宣称可信率（基于M-01~M-06）

**参考文档**：`docs/review/pb-review-standard.md`（已完成）

---

### 方向2: 升级pb-review流程

**目标**：让pb-review流程对照标准进行还原和评估。

#### 2.1 pb-review-project-scope
**当前问题**：只扫描代码入口，未对照标准识别缺失能力

**升级要求**：
1. 对照标准L1，扫描所有entry surface（CLI、API、页面、定时任务、服务编排）
2. 对照权威文档（README、services.md），识别声明的能力
3. 输出：`entry_surface_inventory`（入口清单）、`declared_capability_inventory`（声明能力清单）、`missing_modeled_capability_candidates`（缺失能力候选）

#### 2.2 pb-review-product-reconstructor
**当前问题**：产品目录缺少可验证的成功标准

**升级要求**：
1. 对照标准L1-2.1，还原产品目录
2. 评估每个Goal是否有Acceptance Goal、User-visible Success、Business Invariant
3. 输出：当前完整度评分（如"Goal可量化率60%"）、缺失项清单、改造建议

#### 2.3 pb-review-feature-reconstructor
**当前问题**：功能规格卡缺少D-17到D-20维度

**升级要求**：
1. 对照标准L2，还原功能规格卡
2. 对每个功能评估：
   - D-17 Test Oracle完整度（0-100%）
   - D-18 Test Fixture Contract完整度（0-100%）
   - D-19 Test Case Groups数量（0-8+）
   - D-20 Coverage Claim是否明确
3. 判定testability_status（blocked/partial/test_ready）
4. 输出：功能规格卡 + 完整度评分 + 缺失项清单

**关键**：
- 如果代码中有Test Oracle定义，提取并标记"已定义"
- 如果代码中没有，标记"缺失"，完整度=0%
- 如果部分有，提取已有部分，标记缺失部分，计算完整度

#### 2.4 pb-review-dependency-reconstructor
**当前问题**：只追踪运行时依赖，未追踪测试依赖

**升级要求**：
1. 对照标准L2-D-18，识别测试依赖
2. 补充：`test_dependency`、`mock_required_dependency`、`fixture_source_dependency`
3. 输出：依赖矩阵 + 测试依赖清单

#### 2.5 pb-review-implementation-mapper
**当前问题**：只映射实现代码，未映射测试代码

**升级要求**：
1. 对照标准L2-D-19，识别现有测试
2. 补充：`existing_test_paths`、`missing_test_anchor`、`recommended_test_level`
3. 输出：实现映射 + 测试映射 + 测试缺口

#### 2.6 pb-review-relation-builder
**当前问题**：只建立需求→功能链路，未建立功能→测试链路

**升级要求**：
1. 对照标准L1-2.4，建立测试追踪链路
2. 补充：`feature -> test_case_group`、`constraint -> negative_test_group`、`goal -> acceptance_test_group`
3. 输出：追踪矩阵 + 测试追踪完整率

#### 2.7 pb-review-gap-analyzer
**当前问题**：只识别missing_feature，未识别测试相关gap

**升级要求**：
1. 对照标准L1-2.5，识别4种gap类型
2. 补充：`missing_oracle`、`missing_fixture_contract`、`missing_test_traceability`
3. 对每个gap评估严重程度（Critical/Major/Minor）
4. 输出：差距分析 + 严重程度 + 改造建议

#### 2.8 pb-review-report-composer
**当前问题**：报告只说"completed"，未区分"还原"和"就绪"

**升级要求**：
1. 对照标准L4，生成测试化摘要
2. 补充：testability score、test_ready功能数、blocked功能数、不允许进入TDD的阻塞项
3. 明确区分：
   - 哪些能力已经还原（what is）
   - 哪些能力达到测试就绪（test_ready）
   - 哪些能力存在阻塞（blocked）
4. 输出：评审报告 + 测试化摘要 + 阻塞项清单

---

### 方向3: 新增测试化评估报告

**目标**：基于标准，生成4个评估报告。

#### 3.1 11-testability-scorecard.md
**内容**：
- 当前状态评分（基于M-01到M-07计算）
- 目标状态评分（通常90-100分）
- 差距分析（当前与目标的差距）
- 改造建议（基于差距的优先级和工作量）

#### 3.2 12-test-case-index.md
**内容**：
- 已有测试用例清单（从现有测试代码提取）
- 理想测试用例清单（基于功能规格应该有的）
- 缺口分析（哪些测试用例缺失）
- 优先级建议（哪些缺口应该优先补充）

#### 3.3 13-test-fixture-contract.md
**内容**：
- 已有Fixture清单（从现有测试代码提取）
- 理想Fixture清单（基于功能规格应该有的）
- 缺口分析（哪些fixture缺失）
- 改造建议（如何补充和改进）

#### 3.4 14-test-oracle-matrix.md
**内容**：
- 已有Oracle清单（从代码提取断言标准）
- 理想Oracle清单（基于功能规格应该有的）
- 缺口分析（哪些断言标准缺失）
- 改造建议（如何补充）

---

## 升级实施步骤

### 阶段1: 建立标准（已完成）
- [x] 创建 `pb-review-standard.md`
- [x] 定义L1到L4标准
- [x] 定义M-01到M-07量化指标

### 阶段2: 升级pb-review流程（待执行）
**优先级**：P0（必须完成）

1. **升级pb-review-feature-reconstructor**（最重要）
   - 增加D-17到D-20的还原逻辑
   - 增加完整度评估逻辑
   - 增加testability_status判定逻辑
   - 预计工作量：8-12小时

2. **升级pb-review-gap-analyzer**
   - 增加4种gap类型识别
   - 增加严重程度判定
   - 预计工作量：4-6小时

3. **升级pb-review-report-composer**
   - 增加测试化摘要
   - 增加testability score计算
   - 明确区分"还原"和"就绪"
   - 预计工作量：3-4小时

4. **升级其他skill**（pb-review-project-scope、pb-review-product-reconstructor等）
   - 预计工作量：6-8小时

**总计**：21-30小时（约3-4个工作日）

### 阶段3: 新增评估报告生成（待执行）
**优先级**：P1（高优先级）

1. 创建 `pb-review-testability-scorecard` skill
2. 创建 `pb-review-test-case-index` skill
3. 创建 `pb-review-fixture-contract` skill
4. 创建 `pb-review-oracle-matrix` skill

**预计工作量**：12-16小时（约2个工作日）

### 阶段4: 验证和优化（待执行）
**优先级**：P2（建议完成）

1. 在archer项目上验证升级后的pb-review
2. 对比升级前后的差异
3. 优化评估逻辑和报告格式

**预计工作量**：4-6小时（约1个工作日）

---

## 升级验收标准

### 标准建立验收
- [x] `pb-review-standard.md` 已创建
- [x] 包含L1到L4标准定义
- [x] 包含M-01到M-07量化指标
- [x] 包含完整的示例（JSON Schema、错误码表、业务规则等）

### 流程升级验收
- [ ] pb-review能对照标准还原现状
- [ ] pb-review能识别4种gap类型
- [ ] pb-review能计算testability score
- [ ] pb-review能区分"还原"和"就绪"
- [ ] 所有功能都有testability_status判定

### 报告生成验收
- [ ] 能生成testability-scorecard
- [ ] 能生成test-case-index
- [ ] 能生成fixture-contract
- [ ] 能生成oracle-matrix

### 质量验收
- [ ] 在archer项目上验证，testability score ≥ 75分
- [ ] 识别的gap与实际情况一致
- [ ] 改造建议可执行且工作量估算准确

---

## 使用示例

### 示例1: 对archer项目执行升级后的pb-review

```bash
# 执行pb-review
pb-review /path/to/archer

# 预期输出
.review/
├── deliverables/
│   ├── 01-system-context.md
│   ├── 02-product-catalog.md          # 包含完整度评分
│   ├── 03-feature-spec-index.md       # 包含testability_status列
│   ├── 04-feature-specs/
│   │   ├── OPR-AS-TRND-001.md        # 包含D-17到D-20
│   │   └── ...
│   ├── 05-traceability-matrix.md      # 包含测试追踪链路
│   ├── 06-gap-analysis.md             # 包含4种gap类型
│   ├── 07-review-report.md            # 包含测试化摘要
│   ├── 08-architecture-layered.md
│   ├── 09-dependency-matrix.md
│   ├── 10-data-flow.md
│   ├── 11-testability-scorecard.md    # 新增
│   ├── 12-test-case-index.md          # 新增
│   ├── 13-test-fixture-contract.md    # 新增
│   └── 14-test-oracle-matrix.md       # 新增
└── pb-review-standard.md              # 标准参照
```

### 示例2: 查看testability-scorecard

```markdown
# 测试化评分卡

## 当前状态评分
- 功能闭合集合完成率: 85% (目标100%)
- 原子功能率: 95% (目标≥95%) ✅
- Oracle完整率: 50% (目标≥90%)
- Fixture完整率: 45% (目标≥90%)
- 测试追踪完整率: 60% (目标100%)
- 规则负向覆盖率: 40% (目标100%)
- 副作用断言覆盖率: 55% (目标≥90%)

## Testability Score
**当前评分**: 62分
**目标评分**: 90分
**差距**: 28分

## 判定
❌ 系统未达到测试就绪状态（需≥90分）

## 阻塞项
1. 功能闭合率不足（当前85%，缺3个功能）
2. Oracle完整率不足（当前50%，需提升至≥90%）
3. Fixture完整率不足（当前45%，需提升至≥90%）

## 改造建议
1. 补充3个缺失功能（预计9-15小时）
2. 补充oracle定义（预计10-20小时）
3. 补充fixture定义（预计10-20小时）
4. 总预计工作量: 29-55小时（约4-7个工作日）
```

---

## 关键注意事项

### 1. 标准是衡量尺度，不是强制要求
- pb-review不应创造不存在的内容
- 如果代码中没有，应标记为"缺失"
- 标准用于识别差距，不是用于强制改造

### 2. 尊重已有事实
- 所有"已定义"的判断都必须有代码证据
- 不能因为标准要求就编造内容
- pb-review的职责是还原现状，不是改造系统

### 3. 区分"还原"和"就绪"
- 还原：从代码中提取实际存在的内容
- 就绪：对照标准判断是否达到测试就绪状态
- 报告必须明确区分这两个概念

### 4. 量化评估
- 所有评估都应有量化指标
- 避免"基本完成"、"大部分满足"等模糊描述
- 使用百分比、评分、数量等明确指标

### 5. 可执行的改造建议
- 改造建议应具体、可执行
- 包含工作量估算
- 包含优先级排序

---

## 参考文档

| 文档 | 路径 | 用途 |
|---|---|---|
| pb-review标准 | `docs/review/pb-review-standard.md` | 定义测试化的理想状态标准 |
| 评估标准 | `docs/review/pb-review-testability-upgrade-checklist.md` | 定义评估方法和改造建议 |
| 修正报告 | `docs/review/CORRECTION_REPORT.md` | 记录文档修正过程 |

---

## 总结

**升级核心**：建立标准先行的工作模式
- **标准先行**：先定义理想状态（pb-review-standard.md）
- **还原现状**：对照标准，从代码中还原当前状态
- **识别差距**：明确指出哪些标准未达到，差距有多大
- **提供建议**：基于差距提供改造建议（供参考）

**升级重点**：
1. 建立独立的标准文档（已完成）
2. 升级pb-review流程，对照标准进行还原和评估（待执行）
3. 新增4个测试化评估报告（待执行）

**预期效果**：
- pb-review能准确还原现状，不创造不存在的内容
- pb-review能识别差距，提供量化的完整度评分
- pb-review能提供可执行的改造建议，包含工作量估算
- 最终达到"基于review文档能产出针对完整功能地图的测试用例"的目标
