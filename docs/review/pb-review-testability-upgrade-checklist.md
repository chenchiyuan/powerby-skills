# pb-review 测试化评估标准

**版本**: 2.0.0
**制定日期**: 2026-03-28
**更新日期**: 2026-03-28
**适用范围**: `pb-review` 主流程、全部 `pb-review-*` 下游 skill、所有希望把 review 结果直接转化为 TDD 测试资产的项目

本标准用于定义测试化的理想状态,帮助pb-review评估现有系统与理想状态的差距。

**重要区分**:
- **pb-review的职责**: 还原现状(what is) + 识别差距(gap)
- **本标准的作用**: 定义理想状态(what should be),作为衡量尺度
- **改造的职责**: 基于pb-review识别的差距,补充缺失内容(不是pb-review的职责)

---

## 变更记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 2.0.0 | 2026-03-28 | 增加量化指标、执行步骤、验收标准、改造理由；基于archer项目实际问题深度改造 |
| 1.0.0 | 2026-03-28 | 初版发布 |

---

## 1. 目标与评估理由

### 1.1 核心目标

本标准用于定义测试化的理想状态,帮助 `pb-review` 评估现有系统与理想状态的差距。

**pb-review应基于本标准完成以下评估:**

1. 评估功能地图的闭合性,识别缺失功能。
2. 评估每个功能的测试化完整度(oracle、fixture、测试用例)。
3. 识别哪些功能达到测试就绪状态,哪些功能存在阻塞。
4. 量化测试覆盖差距,提供改造建议(供参考)。

### 1.2 评估理由

**基于archer项目review结果的实际问题分析:**

| 问题类型 | 严重程度 | 影响范围 | 当前状态 | 评估必要性 |
|---|---|---|---|---|
| 业务规则定义不足 | Critical | 21个功能规格卡 | 无法编写确定性测试 | **必须评估** |
| 数据对象Schema缺失 | Critical | 12个数据对象 | 无法编写数据验证测试 | **必须评估** |
| 功能覆盖存在缺口 | Critical | 6个缺失功能 | 无法保证测试完整性 | **必须评估** |
| 边界条件定义模糊 | Major | 21个功能规格卡 | 无法覆盖边界测试 | **高优先级** |
| 异常场景覆盖不全 | Major | 21个功能规格卡 | 无法编写健壮的异常测试 | **高优先级** |
| 前置条件检查逻辑未定义 | Major | 21个功能规格卡 | 无法编写前置条件测试 | **高优先级** |
| 后置条件验证标准缺失 | Major | 21个功能规格卡 | 无法编写验收测试 | **高优先级** |

**pb-review工作量估算(基于archer项目):**
- 还原现状工作量: 50-100分钟(21个功能)
- 差距识别工作量: 6-10小时
- **总计**: 7-11小时(约1-1.5个工作日)

**改造工作量估算(供参考):**
- P0修复(Critical问题): 78-132小时(约10-17个工作日)
- P1修复(Major问题): 62-126小时(约8-16个工作日)
- **总计**: 140-258小时(约18-33个工作日)

**投资回报率(ROI):**
- **一次性投入**: 18-33个工作日的文档改造
- **长期收益**:
  - 测试用例编写效率提升 **70%**(无需反推代码)
  - 测试覆盖率提升至 **90%+**(基于完整功能地图)
  - 回归测试可信度提升 **80%**(基于明确的oracle)
  - 后续迭代质量保障成本降低 **60%**(测试用例可复用)

---

## 2. 核心原则

### P-01 闭集优先

`pb-review` 的功能列表必须先成为闭集，之后才允许谈测试覆盖率。

说明：

- 只要权威产品文档、代码入口、API 路由、页面、命令、定时任务、skill 暴露能力中还有一个能力未进入功能地图，就不允许宣称“coverage = 100%”。

### P-02 原子功能优先

测试规格的最小单位必须是“可单独断言输入输出的原子功能”，不能把多个异质能力强行合并成一个规格卡。

说明：

- 一个页面入口、多个 API 端点、多个命令模式、多个响应 contract，不应被压缩成一张过粗的规格卡。

### P-03 Oracle 优先

文档必须先能定义测试 oracle，再谈实现映射。

说明：

- “返回 success JSON”
- “输出候选列表”
- “支持导出 CSV”

以上都不是可直接用于 TDD 的 oracle。必须进一步写清字段、排序、错误码、空结果 contract、文件 contract、状态变化 contract。

### P-04 测试可派生

任何一个功能规格卡都必须满足：

- 不阅读代码，也能根据文档列出完整测试组
- 阅读代码，只是为了定位实现，而不是为了反推需求

### P-05 覆盖率不能虚高

只有满足“功能已建模 + 规格可验证 + 用例可派生 + 追踪可闭环”四个条件，才允许把功能标记为 `test_ready` 或 `covered`。

---

## 3. 改造后的目标交付体系

在现有 `DLV-001 ~ DLV-010` 基础上，`pb-review` 应升级为“两层交付体系”：

### 第一层：现有还原层

- `01-system-context.md`
- `02-product-catalog.md`
- `03-feature-spec-index.md`
- `04-feature-specs/*.md`
- `05-traceability-matrix.md`
- `06-gap-analysis.md`
- `07-review-report.md`
- `08-architecture-layered.md`
- `09-dependency-matrix.md`
- `10-data-flow.md`

### 第二层：新增测试化交付层

- `11-testability-scorecard.md`
- `12-test-case-index.md`
- `13-test-fixture-contract.md`
- `14-test-oracle-matrix.md`

说明：

- 第一层负责“还原系统表达了什么能力”
- 第二层负责“把这些能力转化为可执行测试资产”

---

## 4. 交付物测试化评估标准

本章定义各交付物的测试化标准。pb-review应:
1. **还原现状**: 从代码和文档中还原当前状态
2. **对照标准**: 将现状与本章定义的标准进行对比
3. **识别差距**: 明确指出哪些标准未达到,差距有多大
4. **量化评分**: 给出量化的完整度评分(如oracle完整度50%)

**重要**: 本章标准是"衡量尺度",不是"强制要求"。pb-review不应创造不存在的内容。

### 评估总览

| 交付物 | 评估类型 | pb-review工作量 | 优先级 | 阻塞关系 |
|---|---|---|---|---|
| 02-product-catalog.md | 完整度评估 | 15-30分钟 | P0 | 阻塞功能规格卡评估 |
| 03-feature-spec-index.md | 完整度评估 | 30-60分钟 | P0 | 阻塞测试追踪评估 |
| 04-feature-specs/*.md | 完整度评估 | 5-10分钟/卡 | P0 | 阻塞测试用例评估 |
| 05-traceability-matrix.md | 完整度评估 | 30-60分钟 | P1 | 阻塞覆盖率统计 |
| 06-gap-analysis.md | 差距识别 | 1-2小时 | P1 | 阻塞完整性验证 |
| 07-review-report.md | 综合评估 | 30-60分钟 | P1 | 阻塞交付决策 |

---

## 4.1 `02-product-catalog.md`

### 理想状态标准

**当前问题:**
- 产品目标描述过粗(如”提供A股分析能力”),无法直接产出验收测试
- 缺少可验证的成功判定标准
- 场景缺少进入/退出条件,无法编写E2E测试

**理想状态应包含:**
- 每个Goal都有明确的验收标准,可直接转化为验收测试
- 每个Scenario都有完整的测试路径(前置条件→主流程→后置条件)
- 每个Constraint都能追踪到具体的测试组

### 理想状态字段定义

| 字段/章节 | 理想状态 | 格式 | 示例 |
|---|---|---|---|
| `Acceptance Goal` | 应包含 | 可量化的成功标准 | “用户能在3秒内查看到最新的行业趋势排行” |
| `User-visible Success` | 应包含 | 用户可观察的结果 | “页面显示30+个行业的趋势状态,按涨幅排序” |
| `Business Invariant` | 应包含 | 业务不变式 | “趋势状态只能是[uptrend, downtrend, sideways]之一” |
| `Out of Scope` | 应包含 | 明确不做的事 | “不支持分钟级实时趋势计算” |
| `Scenario Exit Criteria` | 应包含 | 场景结束条件 | “CSV文件已生成且包含所有候选股票” |

### pb-review评估方法

#### 还原任务
1. 检查代码和文档中是否存在Acceptance Goal
   - 如果有: 提取完整内容
   - 如果没有: 标记为”缺失”,完整度=0%
   - 如果部分有: 提取已有部分,标记缺失部分,计算完整度

2. 检查每个Goal是否可量化
   - 可量化: 包含时间、数量、百分比等指标
   - 不可量化: 标记为”过粗描述”

3. 检查每个Scenario是否有进入/退出条件
   - 完整: 有进入条件、退出条件、主成功路径
   - 不完整: 标记缺失项

#### 差距识别输出格式
```markdown
## 02-product-catalog.md 现状评估

### 当前状态
- Goal总数: 10
- 有Acceptance Goal的Goal: 6 (60%)
- 可量化的Goal: 4 (40%)
- 有完整进入/退出条件的Scenario: 5/8 (62.5%)

### 差距分析
- ⚠️ 4个Goal缺少Acceptance Goal(完整度40%)
  - 已定义: G-001, G-002, G-003, G-004
  - 缺失: G-005, G-006, G-007, G-008
- ⚠️ 6个Goal描述过粗,无法量化
  - 示例: “提供A股分析能力”(应改为”用户能查看单只股票的K线图、EMA趋势...”)
- ⚠️ 3个Scenario缺少退出条件

### 差距严重程度
- 严重程度: Major
- 影响: 无法直接产出验收测试,需补充验收标准

### 改造建议(供参考)
1. 补充4个Goal的Acceptance Goal(预计2小时)
2. 细化6个过粗Goal的描述(预计2小时)
3. 补充3个Scenario的退出条件(预计1小时)
4. 预计总工作量: 5小时
```

### 评估标准

**定量标准:**
- [ ] 每个 `Goal` 至少有 1 条可验证成功判定(覆盖率 100%)
- [ ] 每个 `Scenario` 至少有进入条件、结束条件、主成功路径(覆盖率 100%)
- [ ] 每个 `Constraint` 能映射到至少 1 个功能或测试组(覆盖率 100%)
- [ ] 所有 `Acceptance Goal` 都是可量化的(如时间、数量、百分比)

**定性标准:**
- [ ] 不存在”提供XX能力”、”支持XX管理”等过粗描述
- [ ] 每个 `User-visible Success` 都能被用户直接观察到
- [ ] 每个 `Business Invariant` 都能被自动化测试验证

### 不合格示例与理想状态对比

| 不合格示例 | 问题 | 理想状态 |
|---|---|---|
| “提供 A 股分析能力” | 过粗,无法验证 | “用户能查看单只股票的K线图、EMA趋势、突破信号、风险预警” |
| “支持股票池管理” | 缺少成功标准 | “用户能创建股票池、添加/删除股票、设置预警条件,操作响应时间<1秒” |
| “计算趋势” | 缺少业务规则 | “基于EMA(7/20/30)计算趋势,分类为uptrend/downtrend/sideways,每日更新” |

### pb-review工作量估算

**还原现状工作量:**
- 单个Goal还原: 1-2分钟
- archer项目(10个Goal): 15-30分钟

### 改造工作量估算(供参考)

**基于pb-review识别的差距,改造工作量估算:**
- 单个Goal改造: 15-30分钟
- archer项目(10个Goal): 2-4小时
## 4.2 `03-feature-spec-index.md`

### 理想状态标准

**当前问题:**
- 功能索引只有基本信息,无法判断测试就绪状态
- 缺少测试化指标,无法量化测试覆盖进度
- 无法识别哪些功能可以进入TDD,哪些还有阻塞

**理想状态应包含:**
- 一眼看出哪些功能可以编写测试用例
- 量化追踪测试就绪进度(如”21个功能中15个test_ready,占71%”)
- 防止虚假的”coverage = 100%”声明

### 理想状态列定义

| 列名 | 类型 | 取值范围 | 计算方式 | 示例 |
|---|---|---|---|---|
| `feature_type` | enum | cli/api/page/service/orchestration | 根据entry_point类型判定 | cli |
| `entry_surface` | string | 具体的入口路径 | 从D-01提取 | `python manage.py get_fund_trend` |
| `testability_status` | enum | blocked/partial/test_ready | 根据D-17~D-20完整性判定 | test_ready |
| `test_case_group_count` | int | ≥0 | 从D-19统计 | 8 |
| `oracle_completeness` | int | 0-100 | (已定义oracle字段数/必需oracle字段数)*100 | 85 |
| `fixture_readiness` | int | 0-100 | (已定义fixture项数/必需fixture项数)*100 | 90 |
| `coverage_claim_allowed` | enum | yes/no | oracle≥90 且 fixture≥90 且 test_case_group≥5 | yes |

### 取值约束与判定规则

**testability_status 判定规则：**
```
blocked:
  - 缺少业务规则定义 OR
  - 缺少数据对象Schema OR
  - oracle_completeness < 50

partial:
  - oracle_completeness >= 50 AND < 90 OR
  - fixture_readiness >= 50 AND < 90 OR
  - test_case_group_count >= 3 AND < 5

test_ready:
  - oracle_completeness >= 90 AND
  - fixture_readiness >= 90 AND
  - test_case_group_count >= 5 AND
  - 业务规则已定义 AND
  - 数据对象Schema已定义
```

**coverage_claim_allowed 判定规则：**
```
yes:
  - testability_status = test_ready AND
  - 无未闭合的gap AND
  - 已有测试追踪链路

no:
  - 其他所有情况
```

### 验收标准

**定量标准：**
- [ ] 所有功能都有 `testability_status`（覆盖率 100%）
- [ ] 所有功能都有 `oracle_completeness` 和 `fixture_readiness` 评分
- [ ] `test_ready` 功能占比 ≥ 80%（archer项目目标）
- [ ] `coverage_claim_allowed=yes` 的功能占比 ≥ 75%

**定性标准：**
- [ ] 任何 `gap` 未闭合时，不允许全局宣称 `coverage = 100%`
- [ ] 任何功能卡未达到 `test_ready` 时，不允许进入”自动生成完整测试用例”阶段
- [ ] 索引表能直接回答：”哪些功能可以开始写测试？”

### 执行步骤

1. **添加新列到索引表**（15分钟）
   - 在现有表格中添加7个新列
   - 设置默认值（如testability_status=blocked）

2. **评估每个功能的oracle_completeness**（2-3小时，21个功能）
   - 检查D-04正常输出是否有schema
   - 检查D-05异常行为是否有错误码
   - 检查D-06边界值是否完整
   - 计算完整度百分比

3. **评估每个功能的fixture_readiness**（2-3小时，21个功能）
   - 检查是否定义了最小数据集
   - 检查是否定义了外部依赖mock策略
   - 检查是否定义了时间冻结要求
   - 计算完整度百分比

4. **统计test_case_group_count**（1-2小时）
   - 从D-19提取测试组数量
   - 如果D-19不存在，标记为0

5. **判定testability_status**（30分钟）
   - 根据判定规则自动计算
   - 标记blocked的功能，列出阻塞原因

6. **判定coverage_claim_allowed**（30分钟）
   - 根据判定规则自动计算
   - 生成”可进入TDD的功能清单”

### 工作量估算

- **archer项目（21个功能）**：6-9小时
- **验证与审查**：1小时
- **生成统计报告**：30分钟

## 4.3 `04-feature-specs/*.md`

### 改造理由

**当前问题（基于archer项目实际问题）：**

| 问题类型 | 具体表现 | 影响 | 严重程度 |
|---|---|---|---|
| 业务规则定义不足 | EMA计算公式未定义、趋势分类规则模糊 | 无法编写确定性测试 | Critical |
| 数据对象Schema缺失 | StockInfo、KLine字段未定义 | 无法编写数据验证测试 | Critical |
| 边界条件模糊 | 数据不足、非交易日、停牌处理未定义 | 无法覆盖边界测试 | Major |
| 异常场景不全 | 数据源失败、超时、格式错误未覆盖 | 无法编写健壮的异常测试 | Major |
| 前置条件检查逻辑未定义 | 无法判断何时可以执行功能 | 无法编写前置条件测试 | Major |
| 后置条件验证标准缺失 | 无法判断功能是否正确执行 | 无法编写验收测试 | Major |

**改造后收益：**
- 每个功能都有完整的Test Oracle，可直接编写断言代码
- 每个功能都有明确的Fixture Contract，可直接准备测试数据
- 每个功能都有完整的Test Case Groups，可直接生成测试用例
- 测试用例编写效率提升70%，测试覆盖率提升至90%+

### 理想状态应包含的维度

在现有 `D-01 ~ D-16` 基础上,理想状态应包含以下4个维度:

| 维度 | 用途 | 理想状态 | pb-review评估工作量 |
|---|---|---|---|
| D-17 Test Oracle | 定义测试断言标准 | 应包含 | 5-10分钟/功能 |
| D-18 Test Fixture Contract | 定义测试数据准备规范 | 应包含 | 3-5分钟/功能 |
| D-19 Test Case Groups | 定义测试用例分组 | 是 | 40-80分钟/功能 |
| D-20 Coverage Claim | 定义测试覆盖声明 | 是 | 10-20分钟/功能 |

---

### D-17 Test Oracle

#### 定义

Test Oracle是测试断言的标准答案，定义了"如何判断功能执行正确"。

#### 理想状态应包含的内容

| 项目 | 说明 | 示例 |
|---|---|---|
| 成功输出Schema | JSON/CSV/HTML的完整结构定义 | 见下方JSON Schema示例 |
| 字段级类型 | 每个字段的数据类型和约束 | `trend_status: enum["uptrend", "downtrend", "sideways"]` |
| 必填字段 | 哪些字段必须存在 | `stock_code, stock_name, trend_status` |
| 排序规则 | 输出结果的排序逻辑 | `按涨幅降序排列，涨幅相同按股票代码升序` |
| 空结果规则 | 何时返回空结果，空结果的格式 | `无符合条件股票时返回空数组[]` |
| 错误码Contract | 所有可能的错误码、触发条件、错误消息 | 见下方错误码表 |
| 文件输出Contract | 文件格式、编码、列顺序、表头 | `UTF-8 CSV，包含表头，列顺序：代码,名称,趋势` |
| 状态变化Contract | 功能执行后系统状态的变化 | `缓存已更新，最后更新时间已记录` |

#### 完整JSON Schema示例（基于archer项目"获取基金趋势"功能）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GetFundTrendResponse",
  "type": "object",
  "required": ["status", "data", "timestamp"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "error"],
      "description": "响应状态"
    },
    "data": {
      "type": "array",
      "description": "基金趋势列表，按涨幅降序排列",
      "items": {
        "type": "object",
        "required": ["fund_code", "fund_name", "trend_status", "ema_7", "ema_20", "ema_30", "change_pct"],
        "properties": {
          "fund_code": {
            "type": "string",
            "pattern": "^[0-9]{6}$",
            "description": "基金代码，6位数字"
          },
          "fund_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100,
            "description": "基金名称"
          },
          "trend_status": {
            "type": "string",
            "enum": ["uptrend", "downtrend", "sideways"],
            "description": "趋势状态：uptrend=上升趋势，downtrend=下降趋势，sideways=横盘"
          },
          "ema_7": {
            "type": "number",
            "minimum": 0,
            "description": "7日指数移动平均线"
          },
          "ema_20": {
            "type": "number",
            "minimum": 0,
            "description": "20日指数移动平均线"
          },
          "ema_30": {
            "type": "number",
            "minimum": 0,
            "description": "30日指数移动平均线"
          },
          "change_pct": {
            "type": "number",
            "description": "涨跌幅百分比，正数为涨，负数为跌"
          },
          "last_update": {
            "type": "string",
            "format": "date-time",
            "description": "最后更新时间，ISO 8601格式"
          }
        }
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "响应生成时间，ISO 8601格式"
    },
    "error": {
      "type": "object",
      "description": "错误信息，仅在status=error时存在",
      "required": ["code", "message"],
      "properties": {
        "code": {
          "type": "string",
          "description": "错误码"
        },
        "message": {
          "type": "string",
          "description": "错误消息"
        },
        "details": {
          "type": "object",
          "description": "错误详情"
        }
      }
    }
  }
}
```

#### 错误码Contract示例

| 错误码 | 触发条件 | 错误消息 | HTTP状态码 | 可恢复性 |
|---|---|---|---|---|
| `DATA_SOURCE_UNAVAILABLE` | 数据源API超时或返回5xx | "数据源暂时不可用，请稍后重试" | 503 | 可恢复 |
| `INVALID_FUND_CODE` | 基金代码格式错误 | "基金代码格式错误，必须为6位数字" | 400 | 不可恢复 |
| `FUND_NOT_FOUND` | 基金代码不存在 | "基金代码{code}不存在" | 404 | 不可恢复 |
| `INSUFFICIENT_DATA` | K线数据不足30天 | "数据不足，需要至少30天K线数据" | 422 | 可恢复 |
| `CALCULATION_ERROR` | EMA计算失败 | "趋势计算失败：{reason}" | 500 | 不可恢复 |
| `RATE_LIMIT_EXCEEDED` | 请求频率超限 | "请求过于频繁，请{seconds}秒后重试" | 429 | 可恢复 |

#### 业务规则定义（必须明确）

**趋势分类规则：**
```
uptrend（上升趋势）:
  - EMA(7) > EMA(20) > EMA(30)
  - 最近3天收盘价均高于EMA(7)
  
downtrend（下降趋势）:
  - EMA(7) < EMA(20) < EMA(30)
  - 最近3天收盘价均低于EMA(7)
  
sideways（横盘）:
  - 不满足uptrend或downtrend条件
  - EMA(7)、EMA(20)、EMA(30)之间的差异 < 2%
```

**EMA计算公式：**
```
EMA(today) = Price(today) * K + EMA(yesterday) * (1 - K)
其中：K = 2 / (N + 1)
N = 周期（7、20、30）
初始EMA = 前N天收盘价的简单平均
```

#### 验收标准

**定量标准：**
- [ ] 成功输出Schema完整度 = 100%（所有字段都有类型、约束、描述）
- [ ] 错误码覆盖率 ≥ 90%（覆盖所有主要异常场景）
- [ ] 业务规则定义完整度 = 100%（所有计算逻辑都有公式）

**定性标准：**
- [ ] Schema可直接用于代码生成（如TypeScript类型、Python dataclass）
- [ ] 错误码可直接用于异常测试编写
- [ ] 业务规则可直接用于单元测试断言

#### 不合格示例与修复

| 不合格示例 | 问题 | 修复后 |
|---|---|---|
| "返回JSON格式" | 过粗，无法编写断言 | 提供完整JSON Schema |
| "返回错误信息" | 缺少错误码 | 提供错误码表，包含code、message、触发条件 |
| "计算趋势" | 缺少计算规则 | 提供完整的趋势分类规则和EMA计算公式 |
| "返回列表" | 缺少排序规则 | "按涨幅降序排列，涨幅相同按基金代码升序" |

---

### D-18 Test Fixture Contract

#### 定义

Test Fixture Contract定义了测试数据准备规范，确保测试环境的可复现性。

#### 理想状态应包含的内容

| 项目 | 说明 | 示例 |
|---|---|---|
| 最小数据集 | 功能正常运行所需的最小数据 | 见下方最小数据集示例 |
| 时间冻结要求 | 是否需要冻结时间，冻结到哪个时间点 | `freeze_time("2024-01-15 09:30:00")` |
| 外部依赖Mock策略 | 哪些外部依赖需要mock，mock返回什么 | 见下方Mock策略表 |
| 数据库初始状态 | 测试前数据库应处于什么状态 | `清空fund_trend表，插入3条测试数据` |
| 前置缓存状态 | 测试前缓存应处于什么状态 | `清空Redis缓存，预热fund_info缓存` |
| 可复用Fixture名称 | 可以复用的fixture函数名 | `@pytest.fixture fund_with_uptrend_data` |

#### 最小数据集示例（基于archer项目"获取基金趋势"功能）

```python
# fixtures/fund_trend_fixtures.py

@pytest.fixture
def minimal_fund_data():
    """最小基金数据集：1只基金，30天K线数据"""
    return {
        "fund_info": {
            "fund_code": "000001",
            "fund_name": "华夏成长",
            "fund_type": "股票型",
            "status": "active"
        },
        "kline_data": [
            {
                "date": "2024-01-01",
                "close": 1.500,
                "volume": 1000000
            },
            # ... 共30条记录
            {
                "date": "2024-01-30",
                "close": 1.650,
                "volume": 1200000
            }
        ]
    }

@pytest.fixture
def fund_with_uptrend_data():
    """上升趋势基金数据：EMA(7) > EMA(20) > EMA(30)"""
    return {
        "fund_code": "000001",
        "kline_data": generate_uptrend_kline(
            start_price=1.500,
            end_price=1.650,
            days=30,
            trend="uptrend"
        )
    }

@pytest.fixture
def fund_with_insufficient_data():
    """数据不足场景：只有15天K线数据"""
    return {
        "fund_code": "000002",
        "kline_data": generate_kline(days=15)
    }
```

#### 外部依赖Mock策略表

| 依赖 | Mock类型 | Mock返回值 | 失败场景Mock |
|---|---|---|---|
| 数据源API | HTTP Mock | 正常K线数据JSON | 超时、5xx错误、格式错误 |
| Redis缓存 | FakeRedis | 空缓存或预热数据 | 连接失败 |
| 数据库 | 测试数据库 | 隔离的测试schema | N/A |
| 时间服务 | freezegun | 冻结到2024-01-15 09:30:00 | N/A |

#### 时间冻结要求示例

```python
import pytest
from freezegun import freeze_time

@pytest.fixture
def frozen_time():
    """冻结时间到2024-01-15 09:30:00（交易日开盘时间）"""
    with freeze_time("2024-01-15 09:30:00"):
        yield

def test_get_fund_trend_with_frozen_time(frozen_time, fund_with_uptrend_data):
    """测试：在固定时间点获取基金趋势"""
    result = get_fund_trend("000001")
    assert result["timestamp"] == "2024-01-15T09:30:00Z"
```

#### 验收标准

**定量标准：**
- [ ] 最小数据集覆盖率 = 100%（每个功能都有最小数据集定义）
- [ ] 外部依赖Mock覆盖率 ≥ 90%（所有主要外部依赖都有Mock策略）
- [ ] 可复用Fixture数量 ≥ 5个/功能（减少重复代码）

**定性标准：**
- [ ] Fixture可直接用于pytest/unittest
- [ ] Mock策略可直接用于unittest.mock或responses库
- [ ] 时间冻结要求可直接用于freezegun

#### 不合格示例与修复

| 不合格示例 | 问题 | 修复后 |
|---|---|---|
| "准备测试数据" | 过粗，无法执行 | 提供完整的最小数据集Python代码 |
| "Mock外部API" | 缺少Mock返回值 | 提供Mock策略表，包含正常和失败场景 |
| "使用测试数据库" | 缺少初始状态 | "清空fund_trend表，插入3条测试数据" |

---

### D-19 Test Case Groups

#### 定义

Test Case Groups将测试用例按照测试目标分组，确保测试覆盖的完整性和系统性。

#### 8个必需测试组

每个功能至少列出以下8个测试组：

| 测试组 | 目标 | 示例测试用例 | 优先级 |
|---|---|---|---|
| 1. 主成功路径 | 验证正常流程 | 正常获取基金趋势，返回正确的趋势状态 | P0 |
| 2. 参数校验 | 验证输入参数校验 | 基金代码格式错误、缺少必填参数 | P0 |
| 3. 边界值 | 验证边界条件 | 数据刚好30天、数据刚好29天、空数据 | P0 |
| 4. 前置条件不满足 | 验证前置条件检查 | 基金不存在、基金已停牌、非交易日 | P1 |
| 5. 异常路径 | 验证异常处理 | 数据源超时、数据源返回错误、计算失败 | P1 |
| 6. 副作用验证 | 验证副作用正确性 | 缓存已更新、日志已记录、指标已上报 | P1 |
| 7. 后置状态验证 | 验证后置状态 | 数据库状态正确、缓存状态正确 | P1 |
| 8. 依赖不可用或降级 | 验证降级策略 | Redis不可用时降级、数据源不可用时降级 | P2 |

#### 5个可选测试组（按需增加）

| 测试组 | 目标 | 示例测试用例 | 优先级 |
|---|---|---|---|
| 9. 幂等性 | 验证重复执行结果一致 | 多次调用返回相同结果 | P2 |
| 10. 事务性 | 验证事务完整性 | 失败时回滚、成功时提交 | P1 |
| 11. 权限 | 验证权限控制 | 未登录、无权限、权限过期 | P1 |
| 12. 性能 | 验证性能指标 | 响应时间<1秒、并发100请求 | P2 |
| 13. 可观测性 | 验证日志、指标、追踪 | 日志包含关键信息、指标正确上报 | P2 |

#### 完整测试用例组示例（基于archer项目"获取基金趋势"功能）

```markdown
## D-19 Test Case Groups

### 1. 主成功路径（Happy Path）

| 用例ID | 测试场景 | 前置条件 | 输入 | 预期输出 | 优先级 |
|---|---|---|---|---|---|
| TC-001 | 获取单只上升趋势基金 | 基金000001有30天K线数据，EMA(7)>EMA(20)>EMA(30) | fund_code="000001" | trend_status="uptrend" | P0 |
| TC-002 | 获取单只下降趋势基金 | 基金000002有30天K线数据，EMA(7)<EMA(20)<EMA(30) | fund_code="000002" | trend_status="downtrend" | P0 |
| TC-003 | 获取单只横盘基金 | 基金000003有30天K线数据，EMA差异<2% | fund_code="000003" | trend_status="sideways" | P0 |

### 2. 参数校验（Parameter Validation）

| 用例ID | 测试场景 | 输入 | 预期错误码 | 预期错误消息 | 优先级 |
|---|---|---|---|---|---|
| TC-101 | 基金代码格式错误 | fund_code="abc" | INVALID_FUND_CODE | "基金代码格式错误，必须为6位数字" | P0 |
| TC-102 | 基金代码为空 | fund_code="" | INVALID_FUND_CODE | "基金代码不能为空" | P0 |
| TC-103 | 基金代码长度错误 | fund_code="123" | INVALID_FUND_CODE | "基金代码格式错误，必须为6位数字" | P0 |

### 3. 边界值（Boundary Values）

| 用例ID | 测试场景 | 前置条件 | 输入 | 预期行为 | 优先级 |
|---|---|---|---|---|---|
| TC-201 | 数据刚好30天 | 基金有30天K线数据 | fund_code="000001" | 正常计算趋势 | P0 |
| TC-202 | 数据刚好29天 | 基金有29天K线数据 | fund_code="000002" | 返回INSUFFICIENT_DATA错误 | P0 |
| TC-203 | 数据为空 | 基金无K线数据 | fund_code="000003" | 返回INSUFFICIENT_DATA错误 | P0 |
| TC-204 | EMA差异刚好2% | EMA(7)和EMA(20)差异=2.00% | fund_code="000004" | trend_status="sideways" | P1 |
| TC-205 | EMA差异刚好>2% | EMA(7)和EMA(20)差异=2.01% | fund_code="000005" | trend_status="uptrend"或"downtrend" | P1 |

### 4. 前置条件不满足（Precondition Failures）

| 用例ID | 测试场景 | 前置条件 | 预期错误码 | 预期错误消息 | 优先级 |
|---|---|---|---|---|---|
| TC-301 | 基金不存在 | 基金代码999999不存在 | FUND_NOT_FOUND | "基金代码999999不存在" | P1 |
| TC-302 | 基金已停牌 | 基金status="suspended" | FUND_SUSPENDED | "基金已停牌，无法获取趋势" | P1 |
| TC-303 | 非交易日 | 当前时间为周末 | NON_TRADING_DAY | "非交易日，无法获取实时趋势" | P1 |

### 5. 异常路径（Exception Paths）

| 用例ID | 测试场景 | Mock配置 | 预期错误码 | 预期错误消息 | 优先级 |
|---|---|---|---|---|---|
| TC-401 | 数据源API超时 | Mock超时5秒 | DATA_SOURCE_UNAVAILABLE | "数据源暂时不可用，请稍后重试" | P1 |
| TC-402 | 数据源返回5xx | Mock返回503 | DATA_SOURCE_UNAVAILABLE | "数据源暂时不可用，请稍后重试" | P1 |
| TC-403 | 数据源返回格式错误 | Mock返回非JSON | DATA_FORMAT_ERROR | "数据格式错误" | P1 |
| TC-404 | EMA计算失败 | Mock返回负数价格 | CALCULATION_ERROR | "趋势计算失败：价格不能为负数" | P1 |

### 6. 副作用验证（Side Effect Verification）

| 用例ID | 测试场景 | 预期副作用 | 验证方法 | 优先级 |
|---|---|---|---|---|
| TC-501 | 缓存已更新 | Redis中fund:000001:trend已更新 | 检查Redis key存在且值正确 | P1 |
| TC-502 | 日志已记录 | 日志包含"获取基金趋势成功" | 检查日志文件或日志mock | P1 |
| TC-503 | 指标已上报 | Prometheus指标fund_trend_requests_total+1 | 检查指标值 | P2 |

### 7. 后置状态验证（Post-condition Verification）

| 用例ID | 测试场景 | 预期后置状态 | 验证方法 | 优先级 |
|---|---|---|---|---|
| TC-601 | 数据库状态正确 | fund_trend表已插入新记录 | 查询数据库验证 | P1 |
| TC-602 | 缓存状态正确 | Redis缓存TTL=3600秒 | 检查Redis TTL | P1 |
| TC-603 | 最后更新时间已记录 | last_update字段=当前时间 | 验证时间戳 | P1 |

### 8. 依赖不可用或降级（Dependency Failure & Degradation）

| 用例ID | 测试场景 | Mock配置 | 预期降级行为 | 优先级 |
|---|---|---|---|---|
| TC-701 | Redis不可用 | Mock Redis连接失败 | 跳过缓存，直接计算 | P2 |
| TC-702 | 数据源不可用 | Mock数据源返回503 | 返回缓存数据（如果有） | P2 |
| TC-703 | 数据库不可用 | Mock数据库连接失败 | 返回错误，不影响缓存 | P2 |
```

#### 验收标准

**定量标准：**
- [ ] 每个功能至少有8个测试组（覆盖率 100%）
- [ ] 主成功路径测试用例数 ≥ 3个
- [ ] 参数校验测试用例数 ≥ 3个
- [ ] 边界值测试用例数 ≥ 5个
- [ ] 异常路径测试用例数 ≥ 4个
- [ ] P0优先级测试用例占比 ≥ 40%

**定性标准：**
- [ ] 每个测试用例都有明确的前置条件、输入、预期输出
- [ ] 每个测试用例都可以直接转化为pytest/unittest代码
- [ ] 测试用例覆盖所有错误码
- [ ] 测试用例覆盖所有边界条件

#### 工作量估算

- **单个功能**：40-80分钟
- **archer项目（21个功能）**：14-28小时
- **验证与审查**：2-3小时

---

### D-20 Coverage Claim

#### 定义

Coverage Claim明确声明当前功能规格卡是否允许作为"该功能测试完成"的依据，防止虚假的"coverage = 100%"声明。

#### 理想状态应包含的内容

| 项目 | 说明 | 示例 |
|---|---|---|
| 允许覆盖声明 | 是否允许宣称该功能测试完成 | `yes` / `no` |
| 覆盖范围 | 当前规格卡覆盖的能力范围 | "覆盖单只基金趋势查询，不覆盖批量查询" |
| 未覆盖子能力 | 尚未覆盖的子能力 | "批量查询、历史趋势查询、趋势预测" |
| 未闭合断言点 | 尚未定义的断言点 | "缓存失效策略、并发安全性" |
| 未标准化Fixture | 尚未标准化的fixture | "批量数据生成器、性能测试数据集" |
| 阻塞原因 | 如果不允许覆盖声明，说明原因 | "业务规则未定义、Schema不完整" |

#### 判定规则

```
允许覆盖声明 = yes，当且仅当：
  1. D-17 Test Oracle 完整度 ≥ 90%
  2. D-18 Test Fixture Contract 完整度 ≥ 90%
  3. D-19 Test Case Groups 数量 ≥ 8
  4. 业务规则已定义（如计算公式、分类规则）
  5. 数据对象Schema已定义
  6. 所有错误码都有对应的测试用例
  7. 所有边界条件都有对应的测试用例
  8. 无未闭合的gap

否则：
  允许覆盖声明 = no
```

#### 示例（基于archer项目"获取基金趋势"功能）

```markdown
## D-20 Coverage Claim

### 允许覆盖声明
**yes** ✅

### 覆盖范围
- 单只基金趋势查询（CLI命令）
- 基于EMA(7/20/30)的趋势分类
- 上升趋势、下降趋势、横盘三种状态
- 正常流程、异常流程、边界条件

### 未覆盖子能力
- 批量基金趋势查询
- 历史趋势查询（指定日期）
- 趋势预测（未来N天）
- 趋势变化通知

### 未闭合断言点
- 缓存失效策略（当前只定义了TTL，未定义主动失效规则）
- 并发安全性（多个请求同时查询同一基金）
- 性能指标（响应时间、吞吐量）

### 未标准化Fixture
- 批量数据生成器（生成100+只基金数据）
- 性能测试数据集（模拟高并发场景）
- 历史数据回放（模拟不同市场环境）

### 完整度评分
- D-17 Test Oracle: 95% ✅
- D-18 Test Fixture Contract: 90% ✅
- D-19 Test Case Groups: 8组 ✅
- 业务规则定义: 100% ✅
- 数据对象Schema: 100% ✅

### 结论
当前规格卡**允许**作为"单只基金趋势查询功能测试完成"的依据。
未覆盖的子能力（批量查询、历史查询等）需要单独的功能规格卡。
```

#### 验收标准

**定量标准：**
- [ ] 每个功能都有Coverage Claim声明（覆盖率 100%）
- [ ] 允许覆盖声明=yes的功能占比 ≥ 75%
- [ ] 每个Coverage Claim都有完整度评分

**定性标准:**
- [ ] 不允许覆盖声明时,应说明阻塞原因
- [ ] 未覆盖子能力应明确列出
- [ ] 未闭合断言点应明确列出

#### 不合格示例与修复

| 不合格示例 | 问题 | 修复后 |
|---|---|---|
| "功能已完成" | 过粗，无法验证 | 提供完整的Coverage Claim，包含覆盖范围、未覆盖子能力 |
| "测试覆盖率100%" | 虚假声明 | 明确列出未覆盖子能力和未闭合断言点 |
| "可以开始测试" | 缺少判定依据 | 提供完整度评分和判定规则 |

---

### 执行步骤

1. **补充D-17 Test Oracle**（30-60分钟/功能）
   - 编写完整的JSON Schema或数据结构定义
   - 定义所有错误码和触发条件
   - 定义所有业务规则和计算公式
   - 定义排序规则、空结果规则

2. **补充D-18 Test Fixture Contract**（20-40分钟/功能）
   - 编写最小数据集Python代码
   - 定义外部依赖Mock策略
   - 定义时间冻结要求
   - 定义可复用Fixture

3. **补充D-19 Test Case Groups**（40-80分钟/功能）
   - 列出8个必需测试组
   - 为每个测试组编写3-5个测试用例
   - 为每个测试用例定义前置条件、输入、预期输出
   - 标记优先级（P0/P1/P2）

4. **补充D-20 Coverage Claim**（10-20分钟/功能）
   - 根据判定规则评估是否允许覆盖声明
   - 列出覆盖范围和未覆盖子能力
   - 列出未闭合断言点和未标准化Fixture
   - 计算完整度评分

### 工作量估算

- **单个功能**：100-200分钟（1.5-3.5小时）
- **archer项目（21个功能）**：35-70小时
- **验证与审查**：5-7小时
- **总计**：40-77小时（约5-10个工作日）

## 4.4 `05-traceability-matrix.md`

### 改造理由

**当前问题：**
- 追踪矩阵只关注"需求→功能→实现"链路，缺少"功能→测试"链路
- 无法量化测试覆盖进度
- 无法识别哪些功能有测试、哪些功能缺测试
- 无法追踪业务规则到负向测试的映射

**改造后收益：**
- 建立完整的四层追踪链路：Goal → Feature → Test Case Group → Test Code
- 量化追踪测试覆盖进度（如"21个功能中18个有测试，占86%"）
- 防止"功能未建模却写covered"的虚假覆盖
- 确保每个业务规则都有对应的负向测试

### 理想状态应包含的4类链路

| 链路类型 | 说明 | 示例 | 用途 |
|---|---|---|---|
| Goal → Feature | 产品目标到功能的映射 | "A股分析" → ["获取基金趋势", "获取行业趋势"] | 确保每个目标都有功能支撑 |
| Feature → Test Case Group | 功能到测试组的映射 | "获取基金趋势" → [主成功路径, 参数校验, 边界值...] | 确保每个功能都有测试组 |
| Feature → Existing Test | 功能到现有测试代码的映射 | "获取基金趋势" → `tests/test_fund_trend.py::test_get_uptrend` | 追踪已有测试覆盖 |
| Constraint/Rule → Negative Test | 业务规则到负向测试的映射 | "EMA(7)>EMA(20)>EMA(30)" → `test_invalid_ema_order` | 确保每个规则都有负向测试 |

### 理想状态应包含的5类统计指标

| 指标 | 计算公式 | 目标值 | 说明 |
|---|---|---|---|
| goal_coverage_by_test | (有测试的Goal数 / Goal总数) * 100% | 100% | 产品目标的测试覆盖率 |
| feature_test_group_coverage | (有测试组的Feature数 / Feature总数) * 100% | 100% | 功能的测试组覆盖率 |
| constraint_negative_coverage | (有负向测试的Rule数 / Rule总数) * 100% | 100% | 业务规则的负向测试覆盖率 |
| oracle_complete_feature_rate | (oracle完整的Feature数 / Feature总数) * 100% | ≥90% | Oracle完整的功能占比 |
| fixture_ready_feature_rate | (fixture就绪的Feature数 / Feature总数) * 100% | ≥90% | Fixture就绪的功能占比 |

### 追踪矩阵示例（基于archer项目）

```markdown
# 05-traceability-matrix.md

## 1. Goal → Feature 追踪

| Goal ID | Goal名称 | 关联Feature | Feature数量 | 测试覆盖状态 |
|---|---|---|---|---|
| G-001 | A股分析能力 | F-001, F-002, F-003, F-004 | 4 | 3/4 有测试 (75%) |
| G-002 | 股票池管理 | F-005, F-006, F-007 | 3 | 3/3 有测试 (100%) |
| G-003 | 趋势监控 | F-008, F-009, F-010 | 3 | 2/3 有测试 (67%) |

**统计：**
- Goal总数：3
- 有测试覆盖的Goal：3 (100%)
- 平均Feature测试覆盖率：81%

## 2. Feature → Test Case Group 追踪

| Feature ID | Feature名称 | 测试组数量 | 测试用例数量 | 优先级分布 | 状态 |
|---|---|---|---|---|---|
| F-001 | 获取基金趋势 | 8 | 24 | P0:10, P1:10, P2:4 | test_ready ✅ |
| F-002 | 获取行业趋势 | 8 | 22 | P0:9, P1:9, P2:4 | test_ready ✅ |
| F-003 | 获取股票K线 | 6 | 18 | P0:8, P1:7, P2:3 | partial ⚠️ |
| F-004 | 计算EMA指标 | 8 | 20 | P0:8, P1:8, P2:4 | test_ready ✅ |

**统计：**
- Feature总数：4
- test_ready功能：3 (75%)
- partial功能：1 (25%)
- 平均测试组数量：7.5
- 平均测试用例数量：21

## 3. Feature → Existing Test 追踪

| Feature ID | Feature名称 | 测试文件路径 | 测试函数数量 | 覆盖率 | 最后更新 |
|---|---|---|---|---|---|
| F-001 | 获取基金趋势 | `tests/test_fund_trend.py` | 18 | 85% | 2024-01-15 |
| F-002 | 获取行业趋势 | `tests/test_industry_trend.py` | 15 | 78% | 2024-01-14 |
| F-003 | 获取股票K线 | `tests/test_kline.py` | 12 | 65% | 2024-01-10 |
| F-004 | 计算EMA指标 | `tests/test_ema.py` | 16 | 90% | 2024-01-16 |

**统计：**
- 有测试代码的Feature：4 (100%)
- 平均测试覆盖率：79.5%
- 覆盖率≥80%的Feature：2 (50%)

## 4. Constraint/Rule → Negative Test 追踪

| Rule ID | 业务规则 | 负向测试场景 | 测试用例 | 状态 |
|---|---|---|---|---|
| R-001 | EMA(7)>EMA(20)>EMA(30)为上升趋势 | EMA顺序错误 | `test_invalid_ema_order` | ✅ |
| R-002 | 数据不足30天返回错误 | 29天数据、0天数据 | `test_insufficient_data_29days`, `test_no_data` | ✅ |
| R-003 | 基金代码必须为6位数字 | 非数字、长度错误 | `test_invalid_fund_code_format` | ✅ |
| R-004 | 非交易日不允许查询实时趋势 | 周末、节假日 | `test_non_trading_day` | ⚠️ 缺少节假日测试 |
| R-005 | 数据源超时5秒返回错误 | 超时场景 | `test_data_source_timeout` | ✅ |

**统计：**
- Rule总数：5
- 有负向测试的Rule：5 (100%)
- 负向测试完整的Rule：4 (80%)
- 需要补充的测试：1个（R-004节假日场景）

## 5. 综合统计

| 指标 | 当前值 | 目标值 | 达标状态 |
|---|---|---|---|
| goal_coverage_by_test | 100% | 100% | ✅ |
| feature_test_group_coverage | 100% | 100% | ✅ |
| constraint_negative_coverage | 100% | 100% | ✅ |
| oracle_complete_feature_rate | 75% | ≥90% | ❌ 需提升 |
| fixture_ready_feature_rate | 75% | ≥90% | ❌ 需提升 |
| test_ready_feature_rate | 75% | ≥80% | ⚠️ 接近目标 |

**阻塞项：**
1. F-003功能的oracle完整度不足（当前60%，需≥90%）
2. F-003功能的fixture就绪度不足（当前70%，需≥90%）
3. R-004规则的负向测试不完整（缺少节假日场景）
```

### 不允许的情况

| 不允许的情况 | 说明 | 检测方法 | 修复方法 |
|---|---|---|---|
| 功能未建模却写covered | Feature不在索引中，但追踪矩阵写covered | 交叉验证索引和矩阵 | 补充功能规格卡或删除covered声明 |
| 只有实现映射，没有测试映射却写covered | Feature有实现路径，但无测试路径 | 检查测试路径是否为空 | 补充测试用例或改为partial |
| Goal无Feature支撑却写covered | Goal下没有任何Feature | 检查Goal关联的Feature数量 | 补充功能规格卡 |
| Rule无负向测试却写covered | Rule下没有负向测试用例 | 检查负向测试数量 | 补充负向测试用例 |

### 验收标准

**定量标准：**
- [ ] 所有Goal都有Feature映射（覆盖率 100%）
- [ ] 所有Feature都有Test Case Group映射（覆盖率 100%）
- [ ] 所有Rule都有Negative Test映射（覆盖率 100%）
- [ ] goal_coverage_by_test ≥ 100%
- [ ] feature_test_group_coverage ≥ 100%
- [ ] constraint_negative_coverage ≥ 100%
- [ ] oracle_complete_feature_rate ≥ 90%
- [ ] fixture_ready_feature_rate ≥ 90%

**定性标准：**
- [ ] 不存在"功能未建模却写covered"的情况
- [ ] 不存在"只有实现映射，没有测试映射却写covered"的情况
- [ ] 每个covered声明都有测试证据支撑
- [ ] 追踪矩阵能直接回答："哪些功能有测试？哪些功能缺测试？"

### 执行步骤

1. **建立Goal → Feature链路**（1-2小时）
   - 从02-product-catalog.md提取所有Goal
   - 从03-feature-spec-index.md提取所有Feature
   - 建立映射关系
   - 统计每个Goal的Feature数量

2. **建立Feature → Test Case Group链路**（2-3小时）
   - 从04-feature-specs/*.md的D-19提取所有测试组
   - 统计每个Feature的测试组数量和测试用例数量
   - 标记test_ready/partial/blocked状态

3. **建立Feature → Existing Test链路**（2-3小时）
   - 扫描tests/目录，识别所有测试文件
   - 建立测试文件到Feature的映射
   - 统计测试函数数量和覆盖率

4. **建立Constraint/Rule → Negative Test链路**（1-2小时）
   - 从04-feature-specs/*.md提取所有业务规则
   - 从测试用例中识别负向测试
   - 建立映射关系
   - 标记缺失的负向测试

5. **计算统计指标**（30分钟）
   - 计算5类统计指标
   - 生成综合统计表
   - 识别阻塞项

6. **验证不允许的情况**（30分钟）
   - 检查是否存在"功能未建模却写covered"
   - 检查是否存在"只有实现映射，没有测试映射却写covered"
   - 生成问题清单

### 工作量估算

- **archer项目（21个功能）**：7-11小时
- **验证与审查**：1小时
- **总计**：8-12小时（约1-1.5个工作日）

## 4.5 `06-gap-analysis.md`

### 改造理由

**当前问题：**
- Gap分析只关注功能缺失，不关注测试化缺失
- 无法识别哪些功能缺少oracle、哪些功能缺少fixture
- 严重程度判定不明确，无法优先处理关键gap
- 无法量化gap对测试化的影响

**改造后收益：**
- 明确区分4种测试相关gap，精准定位问题
- 基于严重程度优先处理关键gap
- 量化gap对测试覆盖率的影响
- 提供明确的修复建议和工作量估算

### 理想状态应显式区分的4种测试相关Gap

| Gap类型 | 说明 | 示例 | 严重程度判定 |
|---|---|---|---|
| missing_feature | 功能未建模 | 权威文档声明的能力未进入功能地图 | Critical |
| missing_oracle | 功能缺少测试oracle | 功能规格卡缺少D-17 Test Oracle | Critical/Major |
| missing_fixture_contract | 功能缺少fixture合约 | 功能规格卡缺少D-18 Test Fixture Contract | Major |
| missing_test_traceability | 功能缺少测试追踪 | 功能未建立到测试用例的映射 | Major/Minor |

### 严重程度判定规则

```
Critical（关键）:
  - 无法判断功能是否正确
  - 无法编写任何测试用例
  - 阻塞整个功能的测试化
  
  示例：
  - missing_feature：功能完全未建模
  - missing_oracle：缺少业务规则定义、数据对象Schema
  - missing_oracle：缺少错误码定义

Major（重要）:
  - 无法完整生成该功能测试组
  - 测试用例不稳定或不可复现
  - 影响测试覆盖率≥20%
  
  示例：
  - missing_oracle：缺少边界条件定义
  - missing_fixture_contract：缺少最小数据集
  - missing_test_traceability：功能无测试追踪

Minor（次要）:
  - 可以写测试，但稳定性/复用性不足
  - 影响测试覆盖率<20%
  - 不影响核心测试路径
  
  示例：
  - missing_fixture_contract：缺少性能测试数据集
  - missing_test_traceability：缺少可观测性测试追踪
```

### Gap分析示例（基于archer项目）

```markdown
# 06-gap-analysis.md

## 1. missing_feature（功能缺失）

| Gap ID | 缺失功能 | 发现来源 | 严重程度 | 影响范围 | 修复工作量 |
|---|---|---|---|---|---|
| GAP-F-001 | 批量基金趋势查询 | README.md声明 | Critical | 无法测试批量查询能力 | 4-6小时 |
| GAP-F-002 | 历史趋势查询 | API文档声明 | Critical | 无法测试历史数据查询 | 3-5小时 |
| GAP-F-003 | 趋势变化通知 | 产品文档声明 | Major | 无法测试通知功能 | 2-4小时 |

**统计：**
- 功能缺失总数：3
- Critical级别：2
- Major级别：1
- 预计修复工作量：9-15小时

## 2. missing_oracle（Oracle缺失）

| Gap ID | 功能 | 缺失的Oracle | 严重程度 | 影响 | 修复建议 | 修复工作量 |
|---|---|---|---|---|---|---|
| GAP-O-001 | 获取股票K线 | 业务规则定义 | Critical | 无法编写确定性测试 | 补充K线数据处理规则 | 1-2小时 |
| GAP-O-002 | 获取股票K线 | 数据对象Schema | Critical | 无法编写数据验证测试 | 补充KLine字段定义 | 30-60分钟 |
| GAP-O-003 | 计算EMA指标 | 边界条件定义 | Major | 无法覆盖边界测试 | 补充数据不足、异常值处理规则 | 30-60分钟 |
| GAP-O-004 | 获取行业趋势 | 排序规则 | Major | 无法验证输出顺序 | 补充排序逻辑定义 | 15-30分钟 |
| GAP-O-005 | 获取基金趋势 | 空结果规则 | Minor | 无法验证空结果场景 | 补充空结果contract | 15-30分钟 |

**统计：**
- Oracle缺失总数：5
- Critical级别：2（阻塞2个功能的测试化）
- Major级别：2（影响测试覆盖率约40%）
- Minor级别：1（影响测试覆盖率约10%）
- 预计修复工作量：2.5-5小时

## 3. missing_fixture_contract（Fixture合约缺失）

| Gap ID | 功能 | 缺失的Fixture | 严重程度 | 影响 | 修复建议 | 修复工作量 |
|---|---|---|---|---|---|---|
| GAP-FC-001 | 获取股票K线 | 最小数据集 | Major | 无法准备测试数据 | 定义最小K线数据集 | 30-60分钟 |
| GAP-FC-002 | 获取股票K线 | 外部依赖Mock策略 | Major | 测试不稳定 | 定义数据源API Mock策略 | 30-60分钟 |
| GAP-FC-003 | 计算EMA指标 | 时间冻结要求 | Major | 测试结果不可复现 | 定义时间冻结策略 | 15-30分钟 |
| GAP-FC-004 | 获取行业趋势 | 批量数据生成器 | Minor | 性能测试数据准备困难 | 提供批量数据生成工具 | 1-2小时 |

**统计：**
- Fixture合约缺失总数：4
- Major级别：3（影响3个功能的测试稳定性）
- Minor级别：1（影响性能测试）
- 预计修复工作量：2-4.5小时

## 4. missing_test_traceability（测试追踪缺失）

| Gap ID | 功能 | 缺失的追踪 | 严重程度 | 影响 | 修复建议 | 修复工作量 |
|---|---|---|---|---|---|---|
| GAP-T-001 | 获取股票K线 | Feature → Test Case Group | Major | 无法生成测试用例索引 | 补充D-19 Test Case Groups | 40-80分钟 |
| GAP-T-002 | 计算EMA指标 | Rule → Negative Test | Major | 无法验证业务规则 | 建立规则到负向测试映射 | 30-60分钟 |
| GAP-T-003 | 获取行业趋势 | Feature → Existing Test | Minor | 无法追踪已有测试 | 建立到现有测试的映射 | 15-30分钟 |

**统计：**
- 测试追踪缺失总数：3
- Major级别：2（影响2个功能的测试生成）
- Minor级别：1（影响测试追踪完整性）
- 预计修复工作量：1.5-3小时

## 5. 综合统计与优先级

| Gap类型 | 总数 | Critical | Major | Minor | 预计修复工作量 | 优先级 |
|---|---|---|---|---|---|---|
| missing_feature | 3 | 2 | 1 | 0 | 9-15小时 | P0 |
| missing_oracle | 5 | 2 | 2 | 1 | 2.5-5小时 | P0 |
| missing_fixture_contract | 4 | 0 | 3 | 1 | 2-4.5小时 | P1 |
| missing_test_traceability | 3 | 0 | 2 | 1 | 1.5-3小时 | P1 |
| **总计** | **15** | **4** | **8** | **3** | **15-27.5小时** | - |

**关键阻塞项（Critical级别）：**
1. GAP-F-001：批量基金趋势查询功能未建模
2. GAP-F-002：历史趋势查询功能未建模
3. GAP-O-001：获取股票K线缺少业务规则定义
4. GAP-O-002：获取股票K线缺少数据对象Schema

**修复建议：**
1. 优先修复4个Critical级别gap（预计6-9.5小时）
2. 再修复8个Major级别gap（预计6-13小时）
3. 最后修复3个Minor级别gap（预计3-5小时）

**修复后预期：**
- 功能闭合率：100%（当前85%）
- Oracle完整率：95%（当前75%）
- Fixture就绪率：90%（当前75%）
- 测试追踪完整率：100%（当前85%）
```

### 验收标准

**定量标准：**
- [ ] 所有gap都已分类为4种类型之一（覆盖率 100%）
- [ ] 所有gap都有严重程度判定（覆盖率 100%）
- [ ] 所有gap都有修复建议和工作量估算（覆盖率 100%）
- [ ] Critical级别gap数量 = 0（修复完成）
- [ ] Major级别gap数量 ≤ 10%功能数（archer项目≤2个）

**定性标准：**
- [ ] 严重程度判定符合判定规则
- [ ] 修复建议具体可执行
- [ ] 工作量估算合理（基于历史数据）
- [ ] 优先级排序合理（Critical > Major > Minor）

### 不合格示例与修复

| 不合格示例 | 问题 | 修复后 |
|---|---|---|
| "功能不完整" | 过粗，无法定位 | "GAP-F-001：批量基金趋势查询功能未建模" |
| "测试不足" | 缺少分类 | "GAP-O-001：获取股票K线缺少业务规则定义（missing_oracle）" |
| "需要补充" | 缺少严重程度 | "GAP-O-001：Critical，无法编写确定性测试" |
| "尽快修复" | 缺少工作量估算 | "预计修复工作量：1-2小时" |

### 执行步骤

1. **识别missing_feature**（1-2小时）
   - 扫描权威文档（README、API文档、产品文档）
   - 对比03-feature-spec-index.md
   - 列出所有未建模的功能
   - 判定严重程度和影响范围

2. **识别missing_oracle**（2-3小时）
   - 检查所有功能规格卡的D-17
   - 识别缺少业务规则、Schema、错误码的功能
   - 判定严重程度和影响
   - 提供修复建议

3. **识别missing_fixture_contract**（1-2小时）
   - 检查所有功能规格卡的D-18
   - 识别缺少最小数据集、Mock策略的功能
   - 判定严重程度和影响
   - 提供修复建议

4. **识别missing_test_traceability**（1-2小时）
   - 检查05-traceability-matrix.md
   - 识别缺少测试追踪的功能
   - 判定严重程度和影响
   - 提供修复建议

5. **生成综合统计**（30分钟）
   - 统计各类gap数量和严重程度分布
   - 计算总修复工作量
   - 排序优先级
   - 生成修复计划

6. **验证修复后预期**（30分钟）
   - 计算修复后的各项指标
   - 验证是否达到目标值
   - 调整修复计划

### 工作量估算

- **archer项目（21个功能，15个gap）**：6-10小时
- **验证与审查**：1小时
- **总计**：7-11小时（约1-1.5个工作日）

## 4.6 `07-review-report.md`

### 改造理由

**当前问题：**
- Review报告只说"completed"，无法判断测试就绪状态
- 缺少测试化摘要，无法量化测试覆盖进度
- 无法识别哪些功能可以进入TDD，哪些功能还有阻塞
- 无法为后续测试编写提供明确指导

**改造后收益：**
- 明确区分"功能还原完成"和"测试就绪"两个状态
- 提供量化的测试化指标，可追踪进度
- 明确列出可进入TDD的功能和阻塞项
- 为测试编写提供明确的优先级和工作量估算

### 理想状态应包含的测试化摘要

| 摘要项 | 说明 | 示例 | 用途 |
|---|---|---|---|
| 功能总数 | 所有已建模的功能数量 | 21 | 基准数据 |
| 原子功能总数 | 符合原子化拆分规则的功能数量 | 20 (95%) | 评估功能拆分质量 |
| test_ready功能数 | 可以进入TDD的功能数量 | 15 (71%) | 评估测试就绪进度 |
| blocked功能数 | 被阻塞无法进入TDD的功能数量 | 6 (29%) | 识别阻塞项 |
| 未闭合gap数 | 所有未修复的gap数量 | 15 (Critical:4, Major:8, Minor:3) | 评估完整性 |
| 可直接生成测试用例的功能数 | coverage_claim_allowed=yes的功能数量 | 12 (57%) | 评估测试生成就绪度 |
| 不允许宣称完整覆盖的原因 | 阻止宣称coverage=100%的具体原因 | "4个Critical gap未修复" | 明确阻塞原因 |

### Review报告示例（基于archer项目）

```markdown
# 07-review-report.md

## 1. 执行摘要

**项目名称**: archer - A股分析系统
**Review日期**: 2024-01-20
**Review范围**: 全部功能（CLI命令、API端点、页面）
**Review状态**: 功能还原完成 ✅，测试就绪部分完成 ⚠️

## 2. 功能还原摘要

| 指标 | 数值 | 目标 | 状态 |
|---|---|---|---|
| 功能总数 | 21 | - | - |
| 原子功能总数 | 20 | ≥95% | ✅ 95% |
| 功能闭合率 | 85% | 100% | ❌ 缺3个功能 |
| 产品目标覆盖率 | 100% | 100% | ✅ |
| 架构层覆盖率 | 100% | 100% | ✅ |

**结论**: 功能还原基本完成，但存在3个未建模功能（批量查询、历史查询、通知功能）。

## 3. 测试化摘要 ⭐

| 指标 | 数值 | 目标 | 状态 |
|---|---|---|---|
| test_ready功能数 | 15 | ≥80% (17) | ⚠️ 71% |
| blocked功能数 | 6 | ≤20% (4) | ❌ 29% |
| oracle完整率 | 75% | ≥90% | ❌ |
| fixture就绪率 | 75% | ≥90% | ❌ |
| 测试追踪完整率 | 85% | 100% | ❌ |
| 未闭合gap数 | 15 | 0 | ❌ |
| coverage_claim_allowed=yes功能数 | 12 | ≥75% (16) | ⚠️ 57% |

**结论**: 测试化进度为71%，距离目标还有差距。主要阻塞项为oracle和fixture不完整。

## 4. 可进入TDD的功能清单

### 4.1 test_ready功能（15个）

| Feature ID | Feature名称 | Oracle完整度 | Fixture就绪度 | 测试组数量 | 优先级 |
|---|---|---|---|---|---|
| F-001 | 获取基金趋势 | 95% | 90% | 8 | P0 |
| F-002 | 获取行业趋势 | 90% | 90% | 8 | P0 |
| F-004 | 计算EMA指标 | 95% | 95% | 8 | P0 |
| F-005 | 创建股票池 | 90% | 90% | 8 | P0 |
| F-006 | 添加股票到池 | 90% | 90% | 8 | P0 |
| ... | ... | ... | ... | ... | ... |

**建议**: 这15个功能可以立即开始编写测试用例，预计工作量：30-45小时。

### 4.2 blocked功能（6个）

| Feature ID | Feature名称 | 阻塞原因 | 修复工作量 | 优先级 |
|---|---|---|---|---|
| F-003 | 获取股票K线 | 缺少业务规则定义、数据对象Schema | 1.5-3小时 | P0 |
| F-007 | 删除股票池 | 缺少副作用验证标准 | 30-60分钟 | P1 |
| F-010 | 趋势预警 | 缺少通知contract定义 | 1-2小时 | P1 |
| ... | ... | ... | ... | ... |

**建议**: 优先修复P0阻塞项（预计2-4小时），再修复P1阻塞项（预计2-3小时）。

## 5. 未闭合Gap清单

### 5.1 Critical级别（4个）⚠️

| Gap ID | Gap类型 | 描述 | 修复工作量 | 阻塞功能数 |
|---|---|---|---|---|
| GAP-F-001 | missing_feature | 批量基金趋势查询未建模 | 4-6小时 | 1 |
| GAP-F-002 | missing_feature | 历史趋势查询未建模 | 3-5小时 | 1 |
| GAP-O-001 | missing_oracle | 获取股票K线缺少业务规则 | 1-2小时 | 1 |
| GAP-O-002 | missing_oracle | 获取股票K线缺少Schema | 30-60分钟 | 1 |

**影响**: 阻塞4个功能的测试化，影响测试覆盖率约19%。

### 5.2 Major级别（8个）

（详细列表略）

**影响**: 影响8个功能的测试完整性，影响测试覆盖率约38%。

### 5.3 Minor级别（3个）

（详细列表略）

**影响**: 影响测试稳定性和可复用性，影响测试覆盖率约14%。

## 6. 不允许宣称完整覆盖的原因

**当前不允许宣称"coverage = 100%"，原因如下：**

1. ❌ 功能闭合率未达100%（当前85%，缺3个功能）
2. ❌ 存在4个Critical级别gap未修复
3. ❌ oracle完整率未达90%（当前75%）
4. ❌ fixture就绪率未达90%（当前75%）
5. ❌ test_ready功能占比未达80%（当前71%）

**修复后预期：**
- 修复所有Critical gap后，功能闭合率→100%，oracle完整率→95%
- 修复所有Major gap后，fixture就绪率→90%，test_ready功能占比→85%
- 预计总修复工作量：15-27.5小时（约2-3.5个工作日）

## 7. 测试编写优先级建议

### 阶段1：修复Critical gap（2-3.5个工作日）
1. 补充3个缺失功能的规格卡
2. 补充获取股票K线的业务规则和Schema
3. 验证功能闭合率达到100%

### 阶段2：修复Major gap（1.5-2.5个工作日）
1. 补充8个功能的oracle和fixture
2. 验证oracle完整率≥90%，fixture就绪率≥90%
3. 验证test_ready功能占比≥80%

### 阶段3：开始测试编写（4-6个工作日）
1. 优先编写15个test_ready功能的测试用例
2. 按优先级编写：P0功能→P1功能→P2功能
3. 目标：测试覆盖率≥90%

### 阶段4：修复Minor gap（1-1.5个工作日）
1. 补充性能测试数据集
2. 补充可观测性测试
3. 目标：测试覆盖率→95%+

**总预计工作量**: 9-13.5个工作日

## 8. 交付物清单

| 交付物 | 状态 | 完整度 | 备注 |
|---|---|---|---|
| 01-system-context.md | ✅ 完成 | 100% | - |
| 02-product-catalog.md | ✅ 完成 | 100% | 已补充acceptance goals |
| 03-feature-spec-index.md | ✅ 完成 | 100% | 已补充testability_status |
| 04-feature-specs/*.md | ⚠️ 部分完成 | 71% | 15/21功能test_ready |
| 05-traceability-matrix.md | ✅ 完成 | 100% | 已补充测试追踪链路 |
| 06-gap-analysis.md | ✅ 完成 | 100% | 识别15个gap |
| 07-review-report.md | ✅ 完成 | 100% | 本文档 |
| 08-architecture-layered.md | ✅ 完成 | 100% | - |
| 09-dependency-matrix.md | ✅ 完成 | 100% | - |
| 10-data-flow.md | ✅ 完成 | 100% | - |

## 9. 最终结论

**功能还原状态**: ✅ 基本完成（85%功能闭合率）
**测试就绪状态**: ⚠️ 部分完成（71% test_ready）
**可进入TDD**: ✅ 15个功能可立即开始测试编写
**阻塞项**: ❌ 4个Critical gap + 8个Major gap

**建议**:
1. 不要立即宣称"review完成"或"coverage=100%"
2. 优先修复4个Critical gap（预计2-3.5个工作日）
3. 修复后，15个功能→21个功能test_ready（100%）
4. 然后可以宣称"测试就绪完成，可进入全面TDD"
```

### 验收标准

**定量标准：**
- [ ] 报告包含所有7项测试化摘要（覆盖率 100%）
- [ ] 明确列出test_ready功能清单（覆盖率 100%）
- [ ] 明确列出blocked功能清单和阻塞原因（覆盖率 100%）
- [ ] 明确列出所有未闭合gap（覆盖率 100%）
- [ ] 提供测试编写优先级建议和工作量估算

**定性标准：**
- [ ] 不使用"completed"掩盖test_ready不足
- [ ] 明确区分"功能还原完成"和"测试就绪"
- [ ] 提供可执行的修复建议和优先级
- [ ] 报告能直接回答："哪些功能可以开始写测试？"

### 不合格示例与修复

| 不合格示例 | 问题 | 修复后 |
|---|---|---|
| "Review已完成" | 掩盖test_ready不足 | "功能还原完成，测试就绪71%，需修复gap" |
| "所有功能已建模" | 忽略gap | "21个功能已建模，但缺3个功能（批量查询等）" |
| "可以开始测试" | 缺少具体指导 | "15个功能test_ready，可立即开始测试编写" |
| "测试覆盖率100%" | 虚假声明 | "不允许宣称coverage=100%，原因：4个Critical gap未修复" |

### 执行步骤

1. **汇总功能还原数据**（30分钟）
   - 从03-feature-spec-index.md提取功能总数、原子功能数
   - 从06-gap-analysis.md提取功能闭合率
   - 生成功能还原摘要表

2. **汇总测试化数据**（30分钟）
   - 从03-feature-spec-index.md提取test_ready/blocked功能数
   - 从03-feature-spec-index.md提取oracle/fixture完整率
   - 从05-traceability-matrix.md提取测试追踪完整率
   - 从06-gap-analysis.md提取未闭合gap数
   - 生成测试化摘要表

3. **生成可进入TDD的功能清单**（30分钟）
   - 筛选testability_status=test_ready的功能
   - 按优先级排序
   - 估算测试编写工作量

4. **生成blocked功能清单**（30分钟）
   - 筛选testability_status=blocked的功能
   - 列出阻塞原因
   - 估算修复工作量

5. **生成未闭合Gap清单**（30分钟）
   - 从06-gap-analysis.md提取所有gap
   - 按严重程度分组
   - 计算影响范围

6. **判定是否允许宣称完整覆盖**（15分钟）
   - 检查功能闭合率是否100%
   - 检查是否存在Critical gap
   - 检查oracle/fixture完整率是否≥90%
   - 检查test_ready功能占比是否≥80%
   - 列出不允许的原因

7. **生成测试编写优先级建议**（30分钟）
   - 制定分阶段修复计划
   - 估算各阶段工作量
   - 提供可执行的建议

### 工作量估算

- **archer项目（21个功能）**：3-4小时
- **验证与审查**：30分钟
- **总计**：3.5-4.5小时（约0.5个工作日）

---

## 5. 测试化评估报告定义

本章定义4个测试化评估报告,用于量化评估review结果的测试就绪程度。

### 评估理由

**当前问题:**
- 现有交付物只关注"功能还原",不关注"测试化"
- 缺少量化的测试化评分,无法追踪进度
- 缺少测试用例缺口分析,无法系统化识别差距
- 缺少fixture和oracle的现状评估

**评估后收益:**
- 提供量化的testability score,可追踪测试化进度
- 提供测试用例缺口分析,可识别测试覆盖差距
- 提供fixture和oracle的现状评估,识别改造优先级
- 为改造工作提供明确的输入和指导

---

## 5.1 `11-testability-scorecard.md` (测试化评分卡)

### 用途

对整个review结果给出可量化测试化评分,用于追踪测试就绪进度。

**重要**: 这是评估报告,不是测试资产。pb-review基于现状计算评分,不创造不存在的内容。

### 理想状态应包含的指标

| 指标 | 权重 | 计算公式 | 目标值 |
|---|---|---|---|
| 功能闭合集合完成率 | 25% | (已建模功能数 / 仓库当前支持功能总数) * 100% | 100% |
| 原子功能比例 | 10% | (原子功能数 / 已建模功能数) * 100% | ≥95% |
| Oracle完整率 | 20% | (oracle完整的功能数 / 已建模功能数) * 100% | ≥90% |
| Fixture就绪率 | 15% | (fixture就绪的功能数 / 已建模功能数) * 100% | ≥90% |
| 规则负向覆盖率 | 10% | (有负向测试的规则数 / 规则总数) * 100% | 100% |
| 副作用断言覆盖率 | 10% | (有副作用断言的功能数 / 有副作用的功能数) * 100% | 100% |
| 测试追踪完整率 | 10% | (有测试追踪的功能数 / 已建模功能数) * 100% | 100% |

### 评分公式

```
Testability Score
= 25% * Feature Closure
+ 10% * Atomic Feature Ratio
+ 20% * Oracle Completeness
+ 15% * Fixture Readiness
+ 10% * Negative Coverage Readiness
+ 10% * Side-effect Assertability
+ 10% * Traceability Completeness
```

### 评分阈值

| 分数范围 | 等级 | 说明 | 建议 |
|---|---|---|---|
| ≥90 | A | 优秀 | 可作为完整TDD输入，立即开始测试编写 |
| 75-89 | B | 良好 | 可作为大部分功能的TDD输入，修复关键gap后开始 |
| 60-74 | C | 及格 | 仅适合作为测试设计草稿，需大量补充 |
| <60 | D | 不及格 | 不能进入系统化测试编写，需全面改造 |

### 示例（基于archer项目）

```markdown
# 11-testability-scorecard.md

## Testability Score: 76 (B级 - 良好)

### 各项指标得分

| 指标 | 权重 | 当前值 | 目标值 | 得分 | 状态 |
|---|---|---|---|---|---|
| 功能闭合集合完成率 | 25% | 85% | 100% | 21.25 | ⚠️ |
| 原子功能比例 | 10% | 95% | ≥95% | 10.00 | ✅ |
| Oracle完整率 | 20% | 75% | ≥90% | 15.00 | ❌ |
| Fixture就绪率 | 15% | 75% | ≥90% | 11.25 | ❌ |
| 规则负向覆盖率 | 10% | 100% | 100% | 10.00 | ✅ |
| 副作用断言覆盖率 | 10% | 80% | 100% | 8.00 | ⚠️ |
| 测试追踪完整率 | 10% | 85% | 100% | 8.50 | ⚠️ |
| **总分** | **100%** | - | - | **76.00** | **B级** |

### 评级：B级 - 良好

**结论**: 可作为大部分功能的TDD输入，但需修复关键gap后再开始全面测试编写。

### 提升建议

1. **优先提升Oracle完整率**（当前75%，目标≥90%）
   - 补充5个功能的业务规则定义
   - 补充5个功能的数据对象Schema
   - 预计工作量：2.5-5小时
   - 提升后得分：76 → 82

2. **提升Fixture就绪率**（当前75%，目标≥90%）
   - 补充5个功能的最小数据集
   - 补充5个功能的Mock策略
   - 预计工作量：2-4.5小时
   - 提升后得分：82 → 88

3. **提升功能闭合率**（当前85%，目标100%）
   - 补充3个缺失功能的规格卡
   - 预计工作量：9-15小时
   - 提升后得分：88 → 92 (A级)

**总预计工作量**: 13.5-24.5小时（约2-3个工作日）
**提升后得分**: 92 (A级 - 优秀)
```

### 工作量估算

- **archer项目（21个功能）**：1-2小时
- **验证与审查**：30分钟
- **总计**：1.5-2.5小时

---

## 5.2 `12-test-case-index.md` (测试用例缺口分析)

### 用途

基于功能地图分析测试用例缺口,识别哪些功能缺少测试用例,哪些测试场景未覆盖。

**重要**: 这是缺口分析报告,不是测试用例生成。pb-review识别缺失的测试场景,不创造测试用例。

### 理想状态应包含的字段

| 字段 | 类型 | 说明 | 示例 |
|---|---|---|---|
| test_case_id | string | 测试用例唯一标识 | TC-F001-001 |
| test_case_group_id | string | 测试组标识 | TCG-F001-HappyPath |
| feature_id | string | 关联的功能ID | F-001 |
| test_level | enum | 测试层级 | unit/service/integration/api/cli/ui/e2e |
| scenario_type | enum | 场景类型 | happy_path/validation/boundary/exception/side_effect |
| goal | string | 测试目标 | "验证上升趋势基金返回正确的趋势状态" |
| preconditions | string | 前置条件 | "基金000001有30天K线数据，EMA(7)>EMA(20)>EMA(30)" |
| input_contract | string | 输入contract | `{"fund_code": "000001"}` |
| expected_oracle | string | 预期oracle | `{"trend_status": "uptrend"}` |
| fixture_ref | string | 引用的fixture | `@pytest.fixture fund_with_uptrend_data` |
| priority | enum | 优先级 | P0/P1/P2 |
| automation_ready | boolean | 是否可自动化 | true/false |

### 测试层级定义

| 测试层级 | 说明 | 示例 |
|---|---|---|
| unit | 单元测试，测试单个函数/类 | `test_calculate_ema()` |
| service | 服务测试，测试单个服务 | `test_fund_trend_service()` |
| integration | 集成测试，测试多个服务协作 | `test_fund_trend_with_cache()` |
| api | API测试，测试HTTP端点 | `test_get_fund_trend_api()` |
| cli | CLI测试，测试命令行 | `test_get_fund_trend_command()` |
| ui | UI测试，测试页面交互 | `test_fund_trend_page()` |
| e2e | 端到端测试，测试完整流程 | `test_user_views_fund_trend()` |

### 示例

```markdown
# 12-test-case-index.md

## 功能F-001：获取基金趋势

### 测试组1：主成功路径（8个测试用例）

| test_case_id | test_level | goal | preconditions | input | expected_oracle | fixture_ref | priority |
|---|---|---|---|---|---|---|---|
| TC-F001-001 | cli | 验证上升趋势基金 | 基金000001有30天K线，EMA(7)>EMA(20)>EMA(30) | fund_code="000001" | trend_status="uptrend" | fund_with_uptrend_data | P0 |
| TC-F001-002 | cli | 验证下降趋势基金 | 基金000002有30天K线，EMA(7)<EMA(20)<EMA(30) | fund_code="000002" | trend_status="downtrend" | fund_with_downtrend_data | P0 |
| TC-F001-003 | cli | 验证横盘基金 | 基金000003有30天K线，EMA差异<2% | fund_code="000003" | trend_status="sideways" | fund_with_sideways_data | P0 |

### 测试组2：参数校验（3个测试用例）

| test_case_id | test_level | goal | input | expected_error_code | priority |
|---|---|---|---|---|---|
| TC-F001-101 | cli | 验证基金代码格式错误 | fund_code="abc" | INVALID_FUND_CODE | P0 |
| TC-F001-102 | cli | 验证基金代码为空 | fund_code="" | INVALID_FUND_CODE | P0 |
| TC-F001-103 | cli | 验证基金代码长度错误 | fund_code="123" | INVALID_FUND_CODE | P0 |

（其他测试组略）

## 统计

- 功能总数：21
- 测试用例总数：504
- 平均测试用例数/功能：24
- P0测试用例：210 (42%)
- P1测试用例：210 (42%)
- P2测试用例：84 (16%)
- 可自动化测试用例：480 (95%)
```

### 工作量估算

- **单个功能**：30-60分钟
- **archer项目（21个功能）**：10-21小时
- **验证与审查**：2小时
- **总计**：12-23小时（约1.5-3个工作日）

---

## 5.3 `13-test-fixture-contract.md` (Fixture现状评估)

### 用途

评估现有测试数据、mock策略、时间冻结策略的完整性,识别fixture缺口。

**重要**: 这是现状评估报告,不是fixture定义。pb-review评估现有fixture的完整度,不创造fixture。

### 理想状态应包含的内容

| 内容 | 说明 | 示例 |
|---|---|---|
| 共享Fixture清单 | 可跨功能复用的fixture | `@pytest.fixture db_session` |
| Feature专属Fixture | 特定功能的fixture | `@pytest.fixture fund_with_uptrend_data` |
| 外部系统Stub规范 | 外部依赖的mock/stub策略 | 数据源API Mock返回值 |
| 时间冻结规范 | 时间冻结策略 | `freeze_time("2024-01-15 09:30:00")` |
| 文件系统输出隔离规范 | 文件输出隔离策略 | 使用临时目录 |
| 数据库清理规范 | 数据库清理策略 | 每个测试前清空表 |

### 示例

```markdown
# 13-test-fixture-contract.md

## 1. 共享Fixture清单

### 1.1 数据库Fixture

```python
@pytest.fixture(scope="session")
def db_engine():
    """测试数据库引擎"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    """测试数据库会话，每个测试后自动回滚"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
```

### 1.2 时间冻结Fixture

```python
@pytest.fixture
def frozen_time():
    """冻结时间到2024-01-15 09:30:00（交易日开盘时间）"""
    with freeze_time("2024-01-15 09:30:00"):
        yield
```

### 1.3 Redis Fixture

```python
@pytest.fixture
def redis_client():
    """测试Redis客户端，使用FakeRedis"""
    return fakeredis.FakeStrictRedis()
```

## 2. Feature专属Fixture

### 2.1 基金趋势相关Fixture

```python
@pytest.fixture
def fund_with_uptrend_data():
    """上升趋势基金数据"""
    return {
        "fund_code": "000001",
        "fund_name": "华夏成长",
        "kline_data": generate_uptrend_kline(days=30)
    }

@pytest.fixture
def fund_with_insufficient_data():
    """数据不足场景"""
    return {
        "fund_code": "000002",
        "kline_data": generate_kline(days=15)
    }
```

## 3. 外部系统Stub规范

### 3.1 数据源API Mock

```python
@pytest.fixture
def mock_data_source_api(responses):
    """Mock数据源API"""
    responses.add(
        responses.GET,
        "https://api.example.com/fund/000001/kline",
        json={"data": [...], "status": "success"},
        status=200
    )
    
    # 超时场景
    responses.add(
        responses.GET,
        "https://api.example.com/fund/timeout/kline",
        body=requests.exceptions.Timeout()
    )
```

## 4. 数据库清理规范

- 每个测试前：清空所有表
- 每个测试后：自动回滚事务
- 测试套件结束后：删除测试数据库

## 5. 文件系统输出隔离规范

- 使用`tmp_path` fixture创建临时目录
- 每个测试使用独立的临时目录
- 测试结束后自动清理临时文件
```

### 工作量估算

- **archer项目（21个功能）**：8-12小时
- **验证与审查**：1小时
- **总计**：9-13小时（约1-1.5个工作日）

---

## 5.4 `14-test-oracle-matrix.md` (Oracle现状评估)

### 用途

评估每个功能的断言点完整性,识别oracle缺口。

**重要**: 这是现状评估报告,不是oracle定义。pb-review评估现有oracle的完整度,不创造oracle。

### 理想状态应包含的断言类型

| 断言类型 | 说明 | 示例 |
|---|---|---|
| 成功断言 | 正常流程的断言 | `assert result["trend_status"] == "uptrend"` |
| 失败断言 | 异常流程的断言 | `assert error["code"] == "INVALID_FUND_CODE"` |
| 边界断言 | 边界条件的断言 | `assert len(kline_data) >= 30` |
| 状态断言 | 系统状态的断言 | `assert db.query(FundTrend).count() == 1` |
| 副作用断言 | 副作用的断言 | `assert redis.get("fund:000001:trend") is not None` |
| 输出排序断言 | 输出顺序的断言 | `assert result[0]["change_pct"] >= result[1]["change_pct"]` |
| 空结果断言 | 空结果的断言 | `assert result["data"] == []` |

### 示例

```markdown
# 14-test-oracle-matrix.md

## 功能F-001：获取基金趋势

### 成功断言

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 上升趋势 | 趋势状态为uptrend | `assert result["trend_status"] == "uptrend"` |
| 上升趋势 | EMA(7) > EMA(20) > EMA(30) | `assert result["ema_7"] > result["ema_20"] > result["ema_30"]` |
| 上升趋势 | 涨跌幅为正数 | `assert result["change_pct"] > 0` |
| 响应格式 | 包含所有必填字段 | `assert all(k in result for k in ["fund_code", "trend_status", "ema_7"])` |
| 响应格式 | 时间戳格式正确 | `assert datetime.fromisoformat(result["timestamp"])` |

### 失败断言

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 基金代码格式错误 | 错误码为INVALID_FUND_CODE | `assert error["code"] == "INVALID_FUND_CODE"` |
| 基金代码格式错误 | 错误消息包含"格式错误" | `assert "格式错误" in error["message"]` |
| 数据源超时 | 错误码为DATA_SOURCE_UNAVAILABLE | `assert error["code"] == "DATA_SOURCE_UNAVAILABLE"` |
| 数据源超时 | HTTP状态码为503 | `assert response.status_code == 503` |

### 边界断言

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 数据刚好30天 | 正常计算趋势 | `assert result["trend_status"] in ["uptrend", "downtrend", "sideways"]` |
| 数据刚好29天 | 返回INSUFFICIENT_DATA错误 | `assert error["code"] == "INSUFFICIENT_DATA"` |
| EMA差异刚好2% | 趋势状态为sideways | `assert result["trend_status"] == "sideways"` |

### 状态断言

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 数据库已更新 | fund_trend表有新记录 | `assert db.query(FundTrend).filter_by(fund_code="000001").count() == 1` |
| 数据库已更新 | 最后更新时间正确 | `assert record.last_update == frozen_time` |

### 副作用断言

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 缓存已更新 | Redis中有缓存 | `assert redis.get("fund:000001:trend") is not None` |
| 缓存已更新 | 缓存TTL正确 | `assert redis.ttl("fund:000001:trend") == 3600` |
| 日志已记录 | 日志包含成功信息 | `assert "获取基金趋势成功" in caplog.text` |

### 输出排序断言

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 按涨幅降序 | 第一个涨幅≥第二个 | `assert result[0]["change_pct"] >= result[1]["change_pct"]` |
| 涨幅相同按代码升序 | 代码按字典序排列 | `assert result[0]["fund_code"] < result[1]["fund_code"]` |

### 空结果断言

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 无符合条件基金 | 返回空数组 | `assert result["data"] == []` |
| 无符合条件基金 | 状态为success | `assert result["status"] == "success"` |
```

### 工作量估算

- **单个功能**：20-40分钟
- **archer项目（21个功能）**：7-14小时
- **验证与审查**：1小时
- **总计**：8-15小时（约1-2个工作日）

---

## 6. 功能原子化评估标准

本章定义功能原子化的标准。pb-review应评估现有功能是否符合这些标准。

### 评估理由

**当前问题:**
- 功能拆分粒度不一致,有的过粗有的过细
- 多个异质能力合并成一个功能,导致测试用例混乱
- 无法判断功能是否已原子化

**评估后收益:**
- 识别不符合原子化标准的功能
- 为每个功能提供明确的测试边界建议
- 提供功能拆分建议(供参考)

### R-01 不同entry surface的评估标准

以下对象不应合并成一张功能卡:

| Entry Surface | 说明 | 示例 |
|---|---|---|
| CLI命令 | 命令行入口 | `python manage.py get_fund_trend` |
| HTTP API | API端点 | `GET /api/fund/{code}/trend` |
| 页面渲染 | 页面入口 | `/fund-trend` |
| 定时任务 | 定时任务入口 | `@celery.task update_fund_trend` |
| 内部服务编排 | 服务编排 | `FundTrendOrchestrator.execute()` |

**不合格示例**: "基金趋势功能"同时包含CLI命令、API端点、页面渲染
**修复后**: 拆分为3个功能："CLI获取基金趋势"、"API获取基金趋势"、"页面显示基金趋势"

### R-02 不同输出contract必须拆分

如果同一入口下存在多个显著不同的响应或副作用，也必须拆分。

**示例：**

不能全部归入"股票分析页V2"一个feature，应拆分为：
- `/stocks/{code}/analysis` → "股票分析页"
- `/stocks/{code}/backtest` → "股票回测页"
- `/stocks/{code}/summary` → "股票摘要页"
- `/stocks/bull-industry-distribution` → "牛市行业分布页"
- `/stocks/macro-overview` → "宏观概览页"

### R-03 不同业务责任必须拆分

**示例：**

即使共享数据对象，也必须拆成独立feature：
- "股票池趋势监控" → 监控股票池中股票的趋势变化
- "股票池管理" → 创建、删除、修改股票池
- "股票池预警配置" → 配置股票池的预警规则

### R-04 不同测试fixture contract必须拆分

如果两个能力需要完全不同的前置数据或外部依赖策略，应拆成不同feature。

**示例：**

- "实时趋势查询" → 需要Mock数据源API、冻结时间
- "历史趋势查询" → 需要历史数据库、不需要Mock API

### pb-review评估方法

对每个功能,pb-review应:
1. 检查是否符合R-01标准(不同entry surface应拆分)
   - 如果符合: 标记为"✅ 符合R-01"
   - 如果不符合: 标记为"❌ 违反R-01",列出具体问题

2. 检查是否符合R-02标准(不同输出contract应拆分)
   - 如果符合: 标记为"✅ 符合R-02"
   - 如果不符合: 标记为"❌ 违反R-02",列出具体问题

3. 检查是否符合R-03标准(不同业务责任应拆分)
   - 如果符合: 标记为"✅ 符合R-03"
   - 如果不符合: 标记为"❌ 违反R-03",列出具体问题

4. 检查是否符合R-04标准(不同fixture contract应拆分)
   - 如果符合: 标记为"✅ 符合R-04"
   - 如果不符合: 标记为"❌ 违反R-04",列出具体问题

#### 评估输出格式
```markdown
## 功能原子化评估结果

### 评估统计
- 功能总数: 21
- 符合原子化标准: 20 (95%)
- 违反原子化标准: 1 (5%)

### 违反原子化标准的功能
| 功能ID | 功能名称 | 违反规则 | 具体问题 | 改造建议 |
|---|---|---|---|---|
| F-003 | 股票分析页V2 | R-01, R-02 | 同时包含5个不同页面入口 | 拆分为5个独立功能 |

### 改造建议(供参考)
1. F-003应拆分为:
   - F-003-1: 股票分析页
   - F-003-2: 股票回测页
   - F-003-3: 股票摘要页
   - F-003-4: 牛市行业分布页
   - F-003-5: 宏观概览页
2. 预计改造工作量: 2-3小时
```

### 评估标准

**定量标准:**
- [ ] 原子功能比例 ≥ 95%
- [ ] 每个功能只有1个entry surface
- [ ] 每个功能只有1个主要输出contract

**定性标准:**
- [ ] 每个功能的测试边界清晰
- [ ] 不存在"多个异质能力合并"的情况
- [ ] 功能名称明确描述单一职责

---

## 7. 测试用例可派生标准

只有满足以下全部条件，某个feature才能被标记为 `test_ready`。

### 12项必需条件

| 条件 | 说明 | 验证方法 |
|---|---|---|
| 1. 功能已原子化 | 不与其他异质能力合并 | 检查是否符合第6章拆分规则 |
| 2. 输入参数完整 | 类型/默认值/互斥规则明确 | 检查D-02是否完整 |
| 3. 正常输出有schema | 明确schema和字段级oracle | 检查D-17是否有JSON Schema |
| 4. 异常输出有错误码 | 错误码和触发条件明确 | 检查D-17是否有错误码表 |
| 5. 边界值清单完整 | 所有边界条件已列出 | 检查D-06是否完整 |
| 6. 后置条件可断言 | 后置条件有明确验证标准 | 检查D-08是否完整 |
| 7. 副作用可断言 | 副作用有明确验证标准 | 检查D-09是否完整 |
| 8. 上下游依赖明确 | 依赖关系清晰 | 检查D-10是否完整 |
| 9. 外部依赖替身策略明确 | Mock/Stub策略明确 | 检查D-18是否有Mock策略 |
| 10. 最小fixture数据集明确 | 测试数据准备规范明确 | 检查D-18是否有最小数据集 |
| 11. 已定义测试组索引 | 测试用例分组明确 | 检查D-19是否有8个测试组 |
| 12. 已定义coverage claim边界 | 覆盖范围明确 | 检查D-20是否有覆盖声明 |

### 判定流程

```
1. 检查功能是否原子化
   ↓ 是
2. 检查D-02输入参数是否完整
   ↓ 是
3. 检查D-17 Test Oracle是否完整（schema + 错误码）
   ↓ 是
4. 检查D-06边界值是否完整
   ↓ 是
5. 检查D-08后置条件是否可断言
   ↓ 是
6. 检查D-09副作用是否可断言
   ↓ 是
7. 检查D-10依赖关系是否明确
   ↓ 是
8. 检查D-18 Test Fixture Contract是否完整（Mock策略 + 最小数据集）
   ↓ 是
9. 检查D-19 Test Case Groups是否完整（≥8个测试组）
   ↓ 是
10. 检查D-20 Coverage Claim是否明确
    ↓ 是
11. 标记为 test_ready ✅
```

### 验收标准

**定量标准：**
- [ ] test_ready功能占比 ≥ 80%
- [ ] 每个test_ready功能都满足12项条件

**定性标准：**
- [ ] 不存在"部分满足就标记test_ready"的情况
- [ ] 每个test_ready功能都能直接生成测试用例

---

## 8. `pb-review` 流程级改造清单

本章列出8个下游skill的改造要求，确保整个pb-review流程支持测试化。

### 改造总览

| Skill | 改造类型 | 工作量估算 | 优先级 |
|---|---|---|---|
| pb-review-project-scope | 增强扫描面 | 2-3小时 | P0 |
| pb-review-product-reconstructor | 补充验收标准 | 1-2小时 | P0 |
| pb-review-feature-reconstructor | 补充测试化字段 | 3-4小时 | P0 |
| pb-review-dependency-reconstructor | 补充测试依赖 | 2-3小时 | P1 |
| pb-review-implementation-mapper | 补充测试路径 | 2-3小时 | P1 |
| pb-review-relation-builder | 补充测试追踪 | 2-3小时 | P1 |
| pb-review-gap-analyzer | 补充测试gap | 2-3小时 | P1 |
| pb-review-report-composer | 补充测试摘要 | 1-2小时 | P1 |

---

## 8.1 `pb-review-project-scope`

### 理想状态应包含的扫描面

| 扫描面 | 说明 | 扫描方法 |
|---|---|---|
| API路由 | 所有HTTP端点 | 扫描Django URLConf、Flask routes |
| 管理命令 | 所有CLI命令 | 扫描Django management commands |
| 页面模板入口 | 所有页面 | 扫描templates目录 |
| 定时任务入口 | 所有定时任务 | 扫描Celery tasks |
| Skill暴露能力 | 所有skill | 扫描skills目录 |
| README声明能力 | 文档声明的能力 | 解析README.md、services.md |

### 理想状态应包含的量化输出

| 输出 | 说明 | 示例 |
|---|---|---|
| entry_surface_inventory | 所有入口清单 | `{"cli": 15, "api": 20, "page": 10}` |
| declared_capability_inventory | 文档声明的能力清单 | `["批量查询", "历史查询", "通知"]` |
| missing_modeled_capability_candidates | 未建模能力候选 | `["批量查询", "历史查询"]` |

### 工作量估算

- **archer项目**：2-3小时
- **验证与审查**：30分钟

---

## 8.2 `pb-review-product-reconstructor`

### 理想状态应包含的字段

| 字段 | 说明 | 示例 |
|---|---|---|
| acceptance_goals | 可验证的验收目标 | "用户能在3秒内查看到最新趋势" |
| scenario_exit_criteria | 场景退出条件 | "CSV文件已生成且包含所有候选股票" |
| business_invariants | 业务不变式 | "趋势状态只能是[uptrend, downtrend, sideways]之一" |
| out_of_scope | 明确不做的事 | "不支持分钟级实时趋势计算" |

### 工作量估算

- **archer项目（10个产品目标）**：1-2小时
- **验证与审查**：30分钟

---

## 8.3 `pb-review-feature-reconstructor`

### 理想状态应包含的字段

| 字段 | 说明 | 取值范围 |
|---|---|---|
| feature_type | 功能类型 | cli/api/page/service/orchestration |
| entry_surface | 入口路径 | 具体的入口路径 |
| oracle_status | Oracle状态 | blocked/partial/complete |
| fixture_status | Fixture状态 | blocked/partial/ready |
| coverage_claim_allowed | 是否允许覆盖声明 | yes/no |

### pb-review应执行的原子功能拆分评估

按照第6章的拆分规则，确保每个功能都是原子化的。

### 工作量估算

- **archer项目（21个功能）**：3-4小时
- **验证与审查**：1小时

---

## 8.4 `pb-review-dependency-reconstructor`

### 理想状态应包含的依赖类型

| 依赖类型 | 说明 | 示例 |
|---|---|---|
| test_dependency | 测试依赖 | "需要测试数据库" |
| mock_required_dependency | 需要Mock的依赖 | "数据源API" |
| fixture_source_dependency | Fixture数据来源 | "从生产数据库导出" |

**说明**: 测试层关心的不只是运行时依赖，还关心"测试必须提前准备什么"。

### 工作量估算

- **archer项目（21个功能）**：2-3小时
- **验证与审查**：30分钟

---

## 8.5 `pb-review-implementation-mapper`

### 理想状态应包含的字段

| 字段 | 说明 | 示例 |
|---|---|---|
| existing_test_paths | 现有测试路径 | `tests/test_fund_trend.py` |
| missing_test_anchor | 缺失的测试锚点 | "缺少边界值测试" |
| recommended_test_level | 推荐的测试层级 | unit/service/integration/api/cli |

### 工作量估算

- **archer项目（21个功能）**：2-3小时
- **验证与审查**：30分钟

---

## 8.6 `pb-review-relation-builder`

### 理想状态应包含的链路

| 链路 | 说明 | 示例 |
|---|---|---|
| feature -> test_case_group | 功能到测试组 | F-001 → [主成功路径, 参数校验, ...] |
| constraint -> negative_test_group | 规则到负向测试 | R-001 → [test_invalid_ema_order] |
| goal -> acceptance_test_group | 目标到验收测试 | G-001 → [test_user_views_trend] |

### 工作量估算

- **archer项目（21个功能）**：2-3小时
- **验证与审查**：30分钟

---

## 8.7 `pb-review-gap-analyzer`

### 理想状态应包含的Gap类型

| Gap类型 | 说明 | 示例 |
|---|---|---|
| missing_feature | 功能未建模 | "批量查询功能未建模" |
| missing_oracle | Oracle缺失 | "缺少业务规则定义" |
| missing_fixture_contract | Fixture合约缺失 | "缺少最小数据集" |
| missing_test_traceability | 测试追踪缺失 | "功能无测试追踪" |

### pb-review应执行的检查

1. 识别未建模feature
2. 识别未闭合oracle
3. 识别缺fixture合约
4. 识别"covered但不可测试"的伪覆盖

### 工作量估算

- **archer项目（21个功能）**：2-3小时
- **验证与审查**：30分钟

---

## 8.8 `pb-review-report-composer`

### 理想状态应包含的摘要

| 摘要项 | 说明 | 示例 |
|---|---|---|
| 测试化摘要 | 测试就绪状态 | "test_ready: 15/21 (71%)" |
| testability_score | 测试化评分 | "76 (B级 - 良好)" |
| 不允许进入TDD的阻塞项 | 阻塞原因 | "4个Critical gap未修复" |

### 应避免的表述

- ❌ "Review已完成"
- ❌ "所有功能已建模"
- ❌ "测试覆盖率100%"

### 推荐使用的表述

- ✅ "功能还原完成，测试就绪71%"
- ✅ "21个功能已建模，但缺3个功能"
- ✅ "不允许宣称coverage=100%，原因：4个Critical gap未修复"

### 工作量估算

- **archer项目**：1-2小时
- **验证与审查**：30分钟

---

## 9. 量化验收指标

为了让流程能被量化验收，建议把以下指标写入每次review的最终统计。

### M-01 功能闭合集合完成率

**计算公式:**
```
已建模功能数 / 仓库当前支持功能总数 * 100%
```

**目标值:** 100%

**说明:** 只有100%才允许进入"完整功能地图测试设计"

---

### M-02 原子功能率

**计算公式:**
```
原子功能数 / 已建模功能数 * 100%
```

**目标值:** ≥95%

**说明:** 确保功能拆分粒度合理

---

### M-03 Oracle完整率

**计算公式:**
```
oracle完整的功能数 / 已建模功能数 * 100%
```

**目标值:** ≥90%

**说明:** 确保每个功能都有明确的测试断言标准

---

### M-04 Fixture就绪率

**计算公式:**
```
fixture就绪的功能数 / 已建模功能数 * 100%
```

**目标值:** ≥90%

**说明:** 确保每个功能都有明确的测试数据准备规范

---

### M-05 测试追踪完整率

**计算公式:**
```
已建立Feature -> TestCaseGroup链路的功能数 / 已建模功能数 * 100%
```

**目标值:** 100%

**说明:** 确保每个功能都有测试追踪

---

### M-06 规则负向覆盖率

**计算公式:**
```
已建立Rule -> Negative Test链路的规则数 / 规则总数 * 100%
```

**目标值:** 100%

**说明:** 确保每个业务规则都有负向测试

---

### M-07 覆盖宣称可信率

**计算公式:**
```
coverage_claim_allowed=yes的功能数 / 已建模功能数 * 100%
```

**目标值:** 只有在M-01 ~ M-06全部达标后，才允许接近100%

**说明:** 防止虚假的"coverage=100%"声明

---

### 综合验收标准

| 指标 | 目标值 | 阻塞级别 |
|---|---|---|
| M-01 功能闭合集合完成率 | 100% | Critical |
| M-02 原子功能率 | ≥95% | Major |
| M-03 Oracle完整率 | ≥90% | Critical |
| M-04 Fixture就绪率 | ≥90% | Major |
| M-05 测试追踪完整率 | 100% | Major |
| M-06 规则负向覆盖率 | 100% | Major |
| M-07 覆盖宣称可信率 | ≥75% | Minor |

**只有所有Critical指标达标，才允许宣称"测试就绪完成"。**

---

## 10. 系统测试就绪判定标准

本章定义系统是否达到"测试就绪"状态的判定标准。pb-review应基于这些标准评估系统现状。

### 8项测试就绪标准

| 编号 | 标准 | 严重程度 | 评估方法 |
|---|---|---|---|
| 1 | 权威文档声明的能力都已建模 | Critical | 交叉验证文档和03-feature-spec-index.md |
| 2 | 每个feature只覆盖单一entry surface | Critical | 检查feature的entry_surface数量 |
| 3 | 正常输出有完整schema和字段级oracle | Critical | 检查D-17是否有JSON Schema |
| 4 | 异常行为有错误码和触发条件 | Critical | 检查D-17是否有错误码表 |
| 5 | 已定义最小fixture数据集 | Major | 检查D-18是否有最小数据集 |
| 6 | 已定义外部依赖mock/stub策略 | Major | 检查D-18是否有Mock策略 |
| 7 | 追踪矩阵与gap文档一致 | Critical | 交叉验证追踪矩阵和gap文档 |
| 8 | 报告明确区分"功能还原"和"测试就绪" | Major | 检查报告是否明确区分两个状态 |

### pb-review评估输出格式

```markdown
## 系统测试就绪评估结果

### 当前状态
- 标准1(功能闭合): ❌ 未达标(85%,目标100%)
  - 已建模功能: 21
  - 文档声明功能: 24
  - 缺失功能: 3个(批量查询、历史查询、通知)

- 标准2(功能原子化): ✅ 达标(95%)
  - 原子功能: 20/21
  - 非原子功能: 1个(F-003需拆分)

- 标准3(Oracle完整): ❌ 未达标(75%,目标≥90%)
  - Oracle完整功能: 16/21
  - Oracle不完整功能: 5个

- 标准4(错误码完整): ⚠️ 部分达标(85%,目标100%)
  - 有错误码功能: 18/21
  - 缺少错误码功能: 3个

- 标准5(Fixture完整): ❌ 未达标(75%,目标≥90%)
  - Fixture就绪功能: 16/21
  - Fixture不就绪功能: 5个

- 标准6(Mock策略完整): ⚠️ 部分达标(80%,目标≥90%)
  - 有Mock策略功能: 17/21
  - 缺少Mock策略功能: 4个

- 标准7(追踪一致性): ✅ 达标
  - 追踪矩阵与gap文档一致

- 标准8(报告准确性): ✅ 达标
  - 报告明确区分"功能还原"和"测试就绪"

### 测试就绪判定
**结论**: ❌ 系统未达到测试就绪状态

**阻塞项**:
1. 标准1未达标: 功能闭合率85%(缺3个功能)
2. 标准3未达标: Oracle完整率75%(需≥90%)
3. 标准5未达标: Fixture就绪率75%(需≥90%)

**改造建议(供参考)**:
1. 补充3个缺失功能的规格卡(预计9-15小时)
2. 补充5个功能的Oracle(预计2.5-5小时)
3. 补充5个功能的Fixture(预计2-4.5小时)
4. 预计总工作量: 13.5-24.5小时(约2-3个工作日)

**改造后预期**:
- 功能闭合率: 100%
- Oracle完整率: 95%
- Fixture就绪率: 90%
- 测试就绪判定: ✅ 达标
```

### 判定流程

```
1. 检查是否存在Critical级别未达标(标准1,3,4,7)
   ↓ 存在
   判定为: ❌ 系统未达到测试就绪状态

2. 检查是否存在Major级别未达标(标准5,6,8)
   ↓ 存在
   判定为: ⚠️ 系统部分达到测试就绪状态

3. 所有标准达标
   ↓
   判定为: ✅ 系统达到测试就绪状态
```

---

## 11. 推荐实施顺序

建议按以下顺序升级 `pb-review`，确保改造的渐进性和可验证性。

### 阶段1：修功能闭集问题（P0，预计2-3天）

**目标:** 功能闭合率达到100%

**任务:**
1. 增强pb-review-project-scope的扫描面
2. 识别所有未建模功能
3. 补充缺失功能的规格卡
4. 验证功能闭合率=100%

**验收标准:**
- [ ] M-01 功能闭合集合完成率 = 100%
- [ ] 无missing_feature类型的gap

---

### 阶段2：修feature原子化问题（P0，预计1-2天）

**目标:** 原子功能率≥95%

**任务:**
1. 实施第6章的原子化拆分规则
2. 识别所有非原子化功能
3. 拆分非原子化功能
4. 验证原子功能率≥95%

**验收标准:**
- [ ] M-02 原子功能率 ≥ 95%
- [ ] 每个功能只有1个entry surface

---

### 阶段3：补oracle和fixture contract（P0，预计3-5天）

**目标:** Oracle完整率≥90%，Fixture就绪率≥90%

**任务:**
1. 为每个功能补充D-17 Test Oracle
2. 为每个功能补充D-18 Test Fixture Contract
3. 验证Oracle完整率≥90%
4. 验证Fixture就绪率≥90%

**验收标准:**
- [ ] M-03 Oracle完整率 ≥ 90%
- [ ] M-04 Fixture就绪率 ≥ 90%
- [ ] 每个功能都有JSON Schema和错误码表
- [ ] 每个功能都有最小数据集和Mock策略

---

### 阶段4：补测试追踪矩阵（P1，预计1-2天）

**目标:** 测试追踪完整率=100%，规则负向覆盖率=100%

**任务:**
1. 建立Feature -> Test Case Group链路
2. 建立Rule -> Negative Test链路
3. 建立Goal -> Acceptance Test链路
4. 验证测试追踪完整率=100%

**验收标准:**
- [ ] M-05 测试追踪完整率 = 100%
- [ ] M-06 规则负向覆盖率 = 100%
- [ ] 所有功能都有测试组映射

---

### 阶段5：新增testability scorecard和test-case index（P1，预计2-3天）

**目标:** 生成测试化评分和测试用例索引

**任务:**
1. 生成11-testability-scorecard.md
2. 生成12-test-case-index.md
3. 生成13-test-fixture-contract.md
4. 生成14-test-oracle-matrix.md
5. 验证testability score≥75

**验收标准:**
- [ ] testability score ≥ 75 (B级)
- [ ] 所有4个新增交付物都已生成
- [ ] 测试用例索引覆盖所有功能

---

### 总预计工作量

- **阶段1**: 2-3天
- **阶段2**: 1-2天
- **阶段3**: 3-5天
- **阶段4**: 1-2天
- **阶段5**: 2-3天
- **总计**: 9-15天

**原因:** 如果功能地图不闭合，后续所有测试化工作都会建立在错误边界上。

---

## 12. 本清单对应的最终成功标准

当 `pb-review` 满足本清单后，应能够做到以下4点。

### 1. 对任意项目输出完整功能地图

**验收标准:**
- [ ] 功能闭合率 = 100%
- [ ] 原子功能率 ≥ 95%
- [ ] 所有entry surface都已扫描
- [ ] 所有权威文档声明的能力都已建模

---

### 2. 对任意功能输出完整规格卡和测试断言矩阵

**验收标准:**
- [ ] 每个功能都有D-17 Test Oracle（JSON Schema + 错误码表）
- [ ] 每个功能都有D-18 Test Fixture Contract（最小数据集 + Mock策略）
- [ ] 每个功能都有D-19 Test Case Groups（≥8个测试组）
- [ ] 每个功能都有D-20 Coverage Claim（覆盖范围明确）

---

### 3. 基于文档直接生成完整测试用例索引

**验收标准:**
- [ ] 12-test-case-index.md已生成
- [ ] 测试用例索引覆盖所有功能
- [ ] 每个测试用例都有明确的前置条件、输入、预期输出
- [ ] 测试用例可直接转化为pytest/unittest代码

---

### 4. 任何一个功能都能明确知道

**要测什么:**
- [ ] 从D-19 Test Case Groups可以看出要测哪些场景
- [ ] 从D-17 Test Oracle可以看出要断言什么

**不测什么:**
- [ ] 从D-20 Coverage Claim可以看出哪些子能力不在范围内
- [ ] 从02-product-catalog.md的out_of_scope可以看出哪些不做

**用什么数据测:**
- [ ] 从D-18 Test Fixture Contract可以看出要准备什么数据
- [ ] 从13-test-fixture-contract.md可以看出可复用哪些fixture

**成功时断言什么:**
- [ ] 从D-17 Test Oracle的成功输出schema可以看出
- [ ] 从14-test-oracle-matrix.md的成功断言可以看出

**失败时断言什么:**
- [ ] 从D-17 Test Oracle的错误码表可以看出
- [ ] 从14-test-oracle-matrix.md的失败断言可以看出

**通过后能覆盖哪条需求和哪条业务规则:**
- [ ] 从05-traceability-matrix.md的Goal -> Feature链路可以看出
- [ ] 从05-traceability-matrix.md的Rule -> Negative Test链路可以看出

---

### 最终结论

达到这一步，`pb-review` 的交付物才真正具备"为后续迭代保驾护航"的测试价值。

**量化指标:**
- testability score ≥ 90 (A级)
- 功能闭合率 = 100%
- Oracle完整率 ≥ 90%
- Fixture就绪率 ≥ 90%
- 测试追踪完整率 = 100%
- test_ready功能占比 ≥ 80%

**定性标准:**
- 不存在虚假的"coverage=100%"声明
- 不存在"功能未建模却写covered"的情况
- 不存在"只有实现映射，没有测试映射却写covered"的情况
- 测试用例可直接从文档派生，无需反推代码

---

**文档结束**

