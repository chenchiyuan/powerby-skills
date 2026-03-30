# pb-review 测试化标准

**版本**: 1.0.0
**制定日期**: 2026-03-28
**用途**: 定义测试化的理想状态标准,作为pb-review还原的参照目标和gap识别的参照物

---

## 1. 标准概述

### 1.1 标准定位

本标准定义了一个系统达到"测试就绪"状态应该具备的特性。

**核心定位:**
- 这是一个纯粹的标准定义文档,只定义"what should be"
- 不包含"how to evaluate"(评估方法)
- 不包含"how to fix"(改造建议)
- 作为pb-review还原的参照目标
- 作为gap识别的参照物

### 1.2 标准层次

- **L1 交付物标准**: 定义各交付物的理想状态
- **L2 功能规格标准**: 定义功能规格卡的理想状态
- **L3 测试资产标准**: 定义测试资产的理想状态
- **L4 质量门禁标准**: 定义测试就绪的判定标准

### 1.3 核心原则

#### P-01 闭集优先
功能列表必须先成为闭集,之后才允许谈测试覆盖率。只要权威产品文档、代码入口、API路由、页面、命令、定时任务、skill暴露能力中还有一个能力未进入功能地图,就不允许宣称"coverage = 100%"。

#### P-02 原子功能优先
测试规格的最小单位必须是"可单独断言输入输出的原子功能",不能把多个异质能力强行合并成一个规格卡。

#### P-03 Oracle优先
文档必须先能定义测试oracle,再谈实现映射。"返回success JSON"、"输出候选列表"、"支持导出CSV"都不是可直接用于TDD的oracle。必须进一步写清字段、排序、错误码、空结果contract、文件contract、状态变化contract。

#### P-04 测试可派生
任何一个功能规格卡都必须满足:不阅读代码,也能根据文档列出完整测试组;阅读代码,只是为了定位实现,而不是为了反推需求。

#### P-05 覆盖率不能虚高
只有满足"功能已建模 + 规格可验证 + 用例可派生 + 追踪可闭环"四个条件,才允许把功能标记为test_ready或covered。

---

## 2. L1 交付物标准

### 2.1 产品目录标准(02-product-catalog.md)

#### 标准定义

产品目录应包含以下内容:

| 项目 | 标准 | 示例 |
|---|---|---|
| Acceptance Goal | 每个Goal都有可量化的成功标准 | "用户能在3秒内查看到最新的行业趋势排行" |
| User-visible Success | 每个Goal都有用户可观察的结果 | "页面显示30+个行业的趋势状态,按涨幅排序" |
| Business Invariant | 每个Goal都有业务不变式 | "趋势状态只能是[uptrend, downtrend, sideways]之一" |
| Out of Scope | 每个Goal都明确不做的事 | "不支持分钟级实时趋势计算" |
| Scenario Exit Criteria | 每个Scenario都有结束条件 | "CSV文件已生成且包含所有候选股票" |

#### 质量标准

**定量标准:**
- Goal可量化率 = 100%
- Scenario完整率 = 100%(有进入条件、退出条件、主成功路径)
- Constraint可追踪率 = 100%(能映射到至少1个功能或测试组)

**定性标准:**
- 不存在"提供XX能力"、"支持XX管理"等过粗描述
- 每个User-visible Success都能被用户直接观察到
- 每个Business Invariant都能被自动化测试验证

### 2.2 功能规格索引标准(03-feature-spec-index.md)

#### 标准定义

功能规格索引应包含以下列:

| 列名 | 标准 | 取值范围 |
|---|---|---|
| feature_type | 必须有 | cli/api/page/service/orchestration |
| entry_surface | 必须有 | 具体的入口路径 |
| testability_status | 必须有 | blocked/partial/test_ready |
| test_case_group_count | 必须有 | ≥0 |
| oracle_completeness | 必须有 | 0-100 |
| fixture_readiness | 必须有 | 0-100 |
| coverage_claim_allowed | 必须有 | yes/no |

#### 取值约束与判定规则

**testability_status判定规则:**
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

**coverage_claim_allowed判定规则:**
```
yes:
  - testability_status = test_ready AND
  - 无未闭合的gap AND
  - 已有测试追踪链路

no:
  - 其他所有情况
```

#### 质量标准

**定量标准:**
- 功能闭合率 = 100%(所有能力都已建模)
- 功能原子化率 ≥ 95%
- test_ready功能占比 ≥ 80%
- coverage_claim_allowed=yes的功能占比 ≥ 75%

**定性标准:**
- 任何gap未闭合时,不允许全局宣称coverage = 100%
- 任何功能卡未达到test_ready时,不允许进入"自动生成完整测试用例"阶段
- 索引表能直接回答:"哪些功能可以开始写测试?"

### 2.3 功能规格卡标准(04-feature-specs/*.md)

见第3章"L2 功能规格标准"

### 2.4 追踪矩阵标准(05-traceability-matrix.md)

#### 标准定义

追踪矩阵应包含以下链路:

| 链路类型 | 标准 |
|---|---|
| Goal → Feature | 每个Goal至少映射到1个Feature |
| Feature → Test Case Group | 每个Feature至少映射到1个Test Case Group |
| Feature → Existing Test | 每个Feature至少映射到1个现有测试 |
| Constraint/Rule → Negative Test | 每个Constraint至少映射到1个负向测试 |

#### 统计指标

| 指标 | 计算公式 | 目标值 |
|---|---|---|
| goal_coverage_by_test | (有测试的Goal数 / Goal总数) * 100% | 100% |
| feature_test_group_coverage | (有测试组的Feature数 / Feature总数) * 100% | 100% |
| constraint_negative_coverage | (有负向测试的Rule数 / Rule总数) * 100% | 100% |
| oracle_complete_feature_rate | (oracle完整的Feature数 / Feature总数) * 100% | ≥90% |
| fixture_ready_feature_rate | (fixture就绪的Feature数 / Feature总数) * 100% | ≥90% |

#### 质量标准

**定量标准:**
- Goal覆盖率 = 100%
- Feature测试追踪率 = 100%
- Constraint负向覆盖率 = 100%

**定性标准:**
- 不存在"功能未建模却写covered"的情况
- 不存在"只有实现映射,没有测试映射却写covered"的情况
- 每个covered声明都有测试证据支撑

### 2.5 差距分析标准(06-gap-analysis.md)

#### 标准定义

差距分析应识别以下4种gap:

| Gap类型 | 定义 |
|---|---|
| missing_feature | 权威文档声明了能力,但功能索引没有对应feature |
| missing_oracle | 功能存在,但缺少Test Oracle定义 |
| missing_fixture_contract | 功能存在,但缺少Fixture Contract定义 |
| missing_test_traceability | 功能存在,但缺少测试追踪链路 |

#### 严重程度判定规则

```
Critical(关键):
  - 无法判断功能是否正确
  - 无法编写任何测试用例
  - 阻塞整个功能的测试化

Major(重要):
  - 无法完整生成该功能测试组
  - 测试用例不稳定或不可复现
  - 影响测试覆盖率≥20%

Minor(次要):
  - 可以写测试,但稳定性/复用性不足
  - 影响测试覆盖率<20%
  - 不影响核心测试路径
```

#### 质量标准

**定量标准:**
- 未闭合gap数 = 0
- Critical级别gap数 = 0
- Major级别gap数 ≤ 10%功能数

**定性标准:**
- 所有gap都已分类为4种类型之一
- 所有gap都有严重程度判定
- 严重程度判定符合判定规则

### 2.6 评审报告标准(07-review-report.md)

#### 标准定义

评审报告应包含以下摘要:

| 项目 | 标准 |
|---|---|
| 功能总数 | 必须有 |
| 原子功能总数 | 必须有 |
| test_ready功能数 | 必须有 |
| blocked功能数 | 必须有 |
| 未闭合gap数 | 必须有 |
| 可直接生成测试用例的功能数 | 必须有 |
| 不允许宣称完整覆盖的原因 | 如果未达标,必须说明 |

#### 质量标准

**定量标准:**
- 报告包含所有7项测试化摘要(覆盖率100%)
- 明确列出test_ready功能清单(覆盖率100%)
- 明确列出blocked功能清单和阻塞原因(覆盖率100%)
- 明确列出所有未闭合gap(覆盖率100%)

**定性标准:**
- 不使用"completed"掩盖test_ready不足
- 明确区分"功能还原完成"和"测试就绪"
- 报告能直接回答:"哪些功能可以开始写测试?"

---

## 3. L2 功能规格标准

### 3.1 D-01到D-16标准(现有维度)

保持现有标准不变。功能规格卡的D-01到D-16维度定义参见`feature-specification-standard.md`。

### 3.2 D-17 Test Oracle标准

#### 标准定义

Test Oracle是测试断言的标准答案,定义了"如何判断功能执行正确"。

Test Oracle应包含以下内容:

| 项目 | 标准 | 示例 |
|---|---|---|
| 成功输出Schema | 必须有完整的JSON/CSV/HTML结构定义 | 见JSON Schema示例 |
| 字段级类型 | 每个字段都有数据类型和约束 | `trend_status: enum["uptrend", "downtrend", "sideways"]` |
| 必填字段 | 明确哪些字段必须存在 | `stock_code, stock_name, trend_status` |
| 排序规则 | 明确输出结果的排序逻辑 | `按涨幅降序排列,涨幅相同按股票代码升序` |
| 空结果规则 | 明确何时返回空结果,空结果的格式 | `无符合条件股票时返回空数组[]` |
| 错误码Contract | 每个异常场景都有错误码、触发条件、错误消息 | 见错误码表 |
| 文件输出Contract | 文件格式、编码、列顺序、表头 | `UTF-8 CSV,包含表头,列顺序:代码,名称,趋势` |
| 状态变化Contract | 功能执行后系统状态的变化 | `缓存已更新,最后更新时间已记录` |
| 业务规则定义 | 所有计算逻辑都有明确的公式和规则 | `EMA(N) = Price(t) × K + EMA(t-1) × (1-K)` |

#### JSON Schema示例

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
      "description": "基金趋势列表,按涨幅降序排列",
      "items": {
        "type": "object",
        "required": ["fund_code", "fund_name", "trend_status", "ema_7", "ema_20", "ema_30", "change_pct"],
        "properties": {
          "fund_code": {
            "type": "string",
            "pattern": "^[0-9]{6}$",
            "description": "基金代码,6位数字"
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
            "description": "趋势状态:uptrend=上升趋势,downtrend=下降趋势,sideways=横盘"
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
            "description": "涨跌幅百分比,正数为涨,负数为跌"
          },
          "last_update": {
            "type": "string",
            "format": "date-time",
            "description": "最后更新时间,ISO 8601格式"
          }
        }
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "响应生成时间,ISO 8601格式"
    },
    "error": {
      "type": "object",
      "description": "错误信息,仅在status=error时存在",
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

#### 错误码表示例

| 错误码 | 触发条件 | 错误消息 | HTTP状态码 | 可恢复性 |
|---|---|---|---|---|
| `DATA_SOURCE_UNAVAILABLE` | 数据源API超时或返回5xx | "数据源暂时不可用,请稍后重试" | 503 | 可恢复 |
| `INVALID_FUND_CODE` | 基金代码格式错误 | "基金代码格式错误,必须为6位数字" | 400 | 不可恢复 |
| `FUND_NOT_FOUND` | 基金代码不存在 | "基金代码{code}不存在" | 404 | 不可恢复 |
| `INSUFFICIENT_DATA` | K线数据不足30天 | "数据不足,需要至少30天K线数据" | 422 | 可恢复 |
| `CALCULATION_ERROR` | EMA计算失败 | "趋势计算失败:{reason}" | 500 | 不可恢复 |
| `RATE_LIMIT_EXCEEDED` | 请求频率超限 | "请求过于频繁,请{seconds}秒后重试" | 429 | 可恢复 |

#### 业务规则示例

**趋势分类规则:**
```
uptrend(上升趋势):
  - EMA(7) > EMA(20) > EMA(30)
  - 最近3天收盘价均高于EMA(7)

downtrend(下降趋势):
  - EMA(7) < EMA(20) < EMA(30)
  - 最近3天收盘价均低于EMA(7)

sideways(横盘):
  - 不满足uptrend或downtrend条件
  - EMA(7)、EMA(20)、EMA(30)之间的差异 < 2%
```

**EMA计算公式:**
```
EMA(today) = Price(today) * K + EMA(yesterday) * (1 - K)
其中:K = 2 / (N + 1)
N = 周期(7、20、30)
初始EMA = 前N天收盘价的简单平均
```

#### 质量标准

**定量标准:**
- 成功输出Schema完整度 = 100%(所有字段都有类型、约束、描述)
- 错误码覆盖率 ≥ 90%(覆盖所有主要异常场景)
- 业务规则定义完整度 = 100%(所有计算逻辑都有公式)

**定性标准:**
- Schema可直接用于代码生成(如TypeScript类型、Python dataclass)
- 错误码可直接用于异常测试编写
- 业务规则可直接用于单元测试断言

### 3.3 D-18 Test Fixture Contract标准

#### 标准定义

Test Fixture Contract定义了测试数据准备规范,确保测试环境的可复现性。

Test Fixture Contract应包含以下内容:

| 项目 | 标准 | 示例 |
|---|---|---|
| 最小数据集 | 明确功能正常运行所需的最小数据 | 见最小数据集示例 |
| 时间冻结要求 | 明确是否需要冻结时间,冻结到哪个时间点 | `freeze_time("2024-01-15 09:30:00")` |
| 外部依赖Mock策略 | 明确哪些外部依赖需要mock,mock返回什么 | 见Mock策略表 |
| 数据库初始状态 | 明确测试前数据库应处于什么状态 | `清空fund_trend表,插入3条测试数据` |
| 前置缓存状态 | 明确测试前缓存应处于什么状态 | `清空Redis缓存,预热fund_info缓存` |
| 可复用Fixture名称 | 可以复用的fixture函数名 | `@pytest.fixture fund_with_uptrend_data` |

#### 最小数据集示例

```python
# fixtures/fund_trend_fixtures.py

@pytest.fixture
def minimal_fund_data():
    """最小基金数据集:1只基金,30天K线数据"""
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
    """上升趋势基金数据:EMA(7) > EMA(20) > EMA(30)"""
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
    """数据不足场景:只有15天K线数据"""
    return {
        "fund_code": "000002",
        "kline_data": generate_kline(days=15)
    }
```

#### Mock策略表示例

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
    """冻结时间到2024-01-15 09:30:00(交易日开盘时间)"""
    with freeze_time("2024-01-15 09:30:00"):
        yield

def test_get_fund_trend_with_frozen_time(frozen_time, fund_with_uptrend_data):
    """测试:在固定时间点获取基金趋势"""
    result = get_fund_trend("000001")
    assert result["timestamp"] == "2024-01-15T09:30:00Z"
```

#### 质量标准

**定量标准:**
- 最小数据集覆盖率 = 100%(每个功能都有最小数据集定义)
- 外部依赖Mock覆盖率 ≥ 90%(所有主要外部依赖都有Mock策略)
- 可复用Fixture数量 ≥ 5个/功能

**定性标准:**
- Fixture可直接用于pytest/unittest
- Mock策略可直接用于unittest.mock或responses库
- 时间冻结要求可直接用于freezegun

### 3.4 D-19 Test Case Groups标准

#### 标准定义

Test Case Groups将测试用例按照测试目标分组,确保测试覆盖的完整性和系统性。

每个功能至少包含以下8个必需测试组:

| 测试组 | 标准 | 最小测试用例数 | 优先级 |
|---|---|---|---|
| 1. 主成功路径 | 必须有 | ≥1 | P0 |
| 2. 参数校验 | 必须有 | ≥3 | P0 |
| 3. 边界值 | 必须有 | ≥3 | P0 |
| 4. 前置条件不满足 | 必须有 | ≥2 | P1 |
| 5. 异常路径 | 必须有 | ≥3 | P1 |
| 6. 副作用验证 | 必须有 | ≥1 | P1 |
| 7. 后置状态验证 | 必须有 | ≥1 | P1 |
| 8. 依赖不可用或降级 | 必须有 | ≥2 | P2 |

5个可选测试组(按需增加):

| 测试组 | 标准 | 最小测试用例数 | 优先级 |
|---|---|---|---|
| 9. 幂等性 | 按需 | ≥1 | P2 |
| 10. 事务性 | 按需 | ≥1 | P1 |
| 11. 权限 | 按需 | ≥1 | P1 |
| 12. 性能 | 按需 | ≥1 | P2 |
| 13. 可观测性 | 按需 | ≥1 | P2 |

#### 测试用例表格式

每个测试组中的测试用例应包含以下字段:

| 字段 | 标准 |
|---|---|
| 用例ID | 必须有,格式为TC-{功能编号}-{序号} |
| 测试场景 | 必须有,描述测试目标 |
| 前置条件 | 必须有,描述测试前的系统状态 |
| 输入 | 必须有,描述测试输入 |
| 预期输出/预期行为 | 必须有,描述预期结果 |
| 优先级 | 必须有,P0/P1/P2 |

#### 完整测试用例组示例

**1. 主成功路径(Happy Path)**

| 用例ID | 测试场景 | 前置条件 | 输入 | 预期输出 | 优先级 |
|---|---|---|---|---|---|
| TC-001 | 获取单只上升趋势基金 | 基金000001有30天K线数据,EMA(7)>EMA(20)>EMA(30) | fund_code="000001" | trend_status="uptrend" | P0 |
| TC-002 | 获取单只下降趋势基金 | 基金000002有30天K线数据,EMA(7)<EMA(20)<EMA(30) | fund_code="000002" | trend_status="downtrend" | P0 |
| TC-003 | 获取单只横盘基金 | 基金000003有30天K线数据,EMA差异<2% | fund_code="000003" | trend_status="sideways" | P0 |

**2. 参数校验(Parameter Validation)**

| 用例ID | 测试场景 | 输入 | 预期错误码 | 预期错误消息 | 优先级 |
|---|---|---|---|---|---|
| TC-101 | 基金代码格式错误 | fund_code="abc" | INVALID_FUND_CODE | "基金代码格式错误,必须为6位数字" | P0 |
| TC-102 | 基金代码为空 | fund_code="" | INVALID_FUND_CODE | "基金代码不能为空" | P0 |
| TC-103 | 基金代码长度错误 | fund_code="123" | INVALID_FUND_CODE | "基金代码格式错误,必须为6位数字" | P0 |

**3. 边界值(Boundary Values)**

| 用例ID | 测试场景 | 前置条件 | 输入 | 预期行为 | 优先级 |
|---|---|---|---|---|---|
| TC-201 | 数据刚好30天 | 基金有30天K线数据 | fund_code="000001" | 正常计算趋势 | P0 |
| TC-202 | 数据刚好29天 | 基金有29天K线数据 | fund_code="000002" | 返回INSUFFICIENT_DATA错误 | P0 |
| TC-203 | 数据为空 | 基金无K线数据 | fund_code="000003" | 返回INSUFFICIENT_DATA错误 | P0 |
| TC-204 | EMA差异刚好2% | EMA(7)和EMA(20)差异=2.00% | fund_code="000004" | trend_status="sideways" | P1 |
| TC-205 | EMA差异刚好>2% | EMA(7)和EMA(20)差异=2.01% | fund_code="000005" | trend_status="uptrend"或"downtrend" | P1 |

**4. 前置条件不满足(Precondition Failures)**

| 用例ID | 测试场景 | 前置条件 | 预期错误码 | 预期错误消息 | 优先级 |
|---|---|---|---|---|---|
| TC-301 | 基金不存在 | 基金代码999999不存在 | FUND_NOT_FOUND | "基金代码999999不存在" | P1 |
| TC-302 | 基金已停牌 | 基金status="suspended" | FUND_SUSPENDED | "基金已停牌,无法获取趋势" | P1 |
| TC-303 | 非交易日 | 当前时间为周末 | NON_TRADING_DAY | "非交易日,无法获取实时趋势" | P1 |

**5. 异常路径(Exception Paths)**

| 用例ID | 测试场景 | Mock配置 | 预期错误码 | 预期错误消息 | 优先级 |
|---|---|---|---|---|---|
| TC-401 | 数据源API超时 | Mock超时5秒 | DATA_SOURCE_UNAVAILABLE | "数据源暂时不可用,请稍后重试" | P1 |
| TC-402 | 数据源返回5xx | Mock返回503 | DATA_SOURCE_UNAVAILABLE | "数据源暂时不可用,请稍后重试" | P1 |
| TC-403 | 数据源返回格式错误 | Mock返回非JSON | DATA_FORMAT_ERROR | "数据格式错误" | P1 |
| TC-404 | EMA计算失败 | Mock返回负数价格 | CALCULATION_ERROR | "趋势计算失败:价格不能为负数" | P1 |

**6. 副作用验证(Side Effect Verification)**

| 用例ID | 测试场景 | 预期副作用 | 验证方法 | 优先级 |
|---|---|---|---|---|
| TC-501 | 缓存已更新 | Redis中fund:000001:trend已更新 | 检查Redis key存在且值正确 | P1 |
| TC-502 | 日志已记录 | 日志包含"获取基金趋势成功" | 检查日志文件或日志mock | P1 |
| TC-503 | 指标已上报 | Prometheus指标fund_trend_requests_total+1 | 检查指标值 | P2 |

**7. 后置状态验证(Post-condition Verification)**

| 用例ID | 测试场景 | 预期后置状态 | 验证方法 | 优先级 |
|---|---|---|---|---|
| TC-601 | 数据库状态正确 | fund_trend表已插入新记录 | 查询数据库验证 | P1 |
| TC-602 | 缓存状态正确 | Redis缓存TTL=3600秒 | 检查Redis TTL | P1 |
| TC-603 | 最后更新时间已记录 | last_update字段=当前时间 | 验证时间戳 | P1 |

**8. 依赖不可用或降级(Dependency Failure & Degradation)**

| 用例ID | 测试场景 | Mock配置 | 预期降级行为 | 优先级 |
|---|---|---|---|---|
| TC-701 | Redis不可用 | Mock Redis连接失败 | 跳过缓存,直接计算 | P2 |
| TC-702 | 数据源不可用 | Mock数据源返回503 | 返回缓存数据(如果有) | P2 |
| TC-703 | 数据库不可用 | Mock数据库连接失败 | 返回错误,不影响缓存 | P2 |

#### 质量标准

**定量标准:**
- 每个功能至少有8个测试组(覆盖率100%)
- 主成功路径测试用例数 ≥ 3个
- 参数校验测试用例数 ≥ 3个
- 边界值测试用例数 ≥ 5个
- 异常路径测试用例数 ≥ 4个
- P0优先级测试用例占比 ≥ 40%

**定性标准:**
- 每个测试用例都有明确的前置条件、输入、预期输出
- 每个测试用例都可以直接转化为pytest/unittest代码
- 测试用例覆盖所有错误码
- 测试用例覆盖所有边界条件

### 3.5 D-20 Coverage Claim标准

#### 标准定义

Coverage Claim明确声明当前功能规格卡是否允许作为"该功能测试完成"的依据。

Coverage Claim应包含以下内容:

| 项目 | 标准 |
|---|---|
| 允许覆盖声明 | 明确是否允许宣称该功能测试完成 |
| 覆盖范围 | 明确当前规格卡覆盖的能力范围 |
| 未覆盖子能力 | 明确尚未覆盖的子能力 |
| 未闭合断言点 | 明确尚未定义的断言点 |
| 未标准化Fixture | 明确尚未标准化的fixture |
| 阻塞原因 | 如果不允许覆盖声明,说明原因 |

#### 判定规则

```
允许覆盖声明 = yes,当且仅当:
  1. D-17 Test Oracle 完整度 ≥ 90%
  2. D-18 Test Fixture Contract 完整度 ≥ 90%
  3. D-19 Test Case Groups 数量 ≥ 8
  4. 业务规则已定义(如计算公式、分类规则)
  5. 数据对象Schema已定义
  6. 所有错误码都有对应的测试用例
  7. 所有边界条件都有对应的测试用例
  8. 无未闭合的gap

否则:
  允许覆盖声明 = no
```

#### 质量标准

**定量标准:**
- 每个功能都有Coverage Claim声明(覆盖率100%)
- 允许覆盖声明=yes的功能占比 ≥ 75%
- 每个Coverage Claim都有完整度评分

**定性标准:**
- 不允许覆盖声明时,必须说明阻塞原因
- 未覆盖子能力必须明确列出
- 未闭合断言点必须明确列出

---

## 4. L3 测试资产标准

### 4.1 测试化评分卡标准(11-testability-scorecard.md)

#### 标准定义

测试化评分卡应包含以下指标:

| 指标 | 标准 | 目标值 |
|---|---|---|
| 功能闭合集合完成率 | 必须有 | 100% |
| 原子功能比例 | 必须有 | ≥95% |
| Oracle完整率 | 必须有 | ≥90% |
| Fixture完整率 | 必须有 | ≥90% |
| 规则负向覆盖率 | 必须有 | 100% |
| 副作用断言覆盖率 | 必须有 | ≥90% |
| 测试追踪完整率 | 必须有 | 100% |
| 可直接进入TDD的功能占比 | 必须有 | ≥80% |

#### 评分公式

```
Testability Score
= 25% × 功能闭合集合完成率
+ 10% × 原子功能比例
+ 20% × Oracle完整率
+ 15% × Fixture完整率
+ 10% × 规则负向覆盖率
+ 10% × 副作用断言覆盖率
+ 10% × 测试追踪完整率
```

#### 阈值标准

| 分数范围 | 等级 | 说明 |
|---|---|---|
| ≥90 | A | 可作为完整TDD输入,立即开始测试编写 |
| 75-89 | B | 可作为大部分功能的TDD输入,修复关键gap后开始 |
| 60-74 | C | 仅适合作为测试设计草稿,需大量补充 |
| <60 | D | 不能进入系统化测试编写,需全面改造 |

### 4.2 测试用例索引标准(12-test-case-index.md)

#### 标准定义

测试用例索引应包含以下列:

| 列名 | 标准 |
|---|---|
| test_case_id | 必须有,格式为TC-{feature_id}-{序号} |
| test_case_group_id | 必须有 |
| feature_id | 必须有 |
| test_level | 必须有(unit/service/integration/api/cli/ui/e2e) |
| scenario_type | 必须有(happy_path/validation/boundary/exception/side_effect) |
| goal | 必须有 |
| preconditions | 必须有 |
| input_contract | 必须有 |
| expected_oracle | 必须有 |
| fixture_ref | 必须有 |
| priority | 必须有(P0/P1/P2) |
| automation_ready | 必须有(true/false) |

#### 测试层级定义

| 测试层级 | 说明 | 示例 |
|---|---|---|
| unit | 单元测试,测试单个函数/类 | `test_calculate_ema()` |
| service | 服务测试,测试单个服务 | `test_fund_trend_service()` |
| integration | 集成测试,测试多个服务协作 | `test_fund_trend_with_cache()` |
| api | API测试,测试HTTP端点 | `test_get_fund_trend_api()` |
| cli | CLI测试,测试命令行 | `test_get_fund_trend_command()` |
| ui | UI测试,测试页面交互 | `test_fund_trend_page()` |
| e2e | 端到端测试,测试完整流程 | `test_user_views_fund_trend()` |

### 4.3 Fixture Contract标准(13-test-fixture-contract.md)

#### 标准定义

Fixture Contract应包含以下内容:

| 项目 | 标准 |
|---|---|
| 共享Fixture清单 | 必须有,列出可跨功能复用的fixture |
| Feature专属Fixture | 必须有,列出特定功能的fixture |
| 外部系统Stub规范 | 必须有,列出外部依赖的mock/stub策略 |
| 时间冻结规范 | 必须有,列出时间冻结策略 |
| 文件系统输出隔离规范 | 必须有,列出文件输出隔离策略 |
| 数据库清理规范 | 必须有,列出数据库清理策略 |

#### 共享Fixture示例

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
    """测试数据库会话,每个测试后自动回滚"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def frozen_time():
    """冻结时间到2024-01-15 09:30:00(交易日开盘时间)"""
    with freeze_time("2024-01-15 09:30:00"):
        yield

@pytest.fixture
def redis_client():
    """测试Redis客户端,使用FakeRedis"""
    return fakeredis.FakeStrictRedis()
```

#### 数据库清理规范

- 每个测试前:清空所有表
- 每个测试后:自动回滚事务
- 测试套件结束后:删除测试数据库

#### 文件系统输出隔离规范

- 使用`tmp_path` fixture创建临时目录
- 每个测试使用独立的临时目录
- 测试结束后自动清理临时文件

### 4.4 Test Oracle矩阵标准(14-test-oracle-matrix.md)

#### 标准定义

Test Oracle矩阵应包含以下断言点:

| 断言类型 | 标准 |
|---|---|
| 成功断言 | 每个功能至少1个 |
| 失败断言 | 每个功能至少1个 |
| 边界断言 | 每个功能至少1个 |
| 状态断言 | 每个功能至少1个 |
| 副作用断言 | 每个功能至少1个 |
| 输出排序断言 | 如果有排序,必须有 |
| 空结果断言 | 如果可能返回空,必须有 |

#### 断言示例

**成功断言:**

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 上升趋势 | 趋势状态为uptrend | `assert result["trend_status"] == "uptrend"` |
| 上升趋势 | EMA(7) > EMA(20) > EMA(30) | `assert result["ema_7"] > result["ema_20"] > result["ema_30"]` |
| 响应格式 | 包含所有必填字段 | `assert all(k in result for k in ["fund_code", "trend_status", "ema_7"])` |

**失败断言:**

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 基金代码格式错误 | 错误码为INVALID_FUND_CODE | `assert error["code"] == "INVALID_FUND_CODE"` |
| 数据源超时 | 错误码为DATA_SOURCE_UNAVAILABLE | `assert error["code"] == "DATA_SOURCE_UNAVAILABLE"` |
| 数据源超时 | HTTP状态码为503 | `assert response.status_code == 503` |

**边界断言:**

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 数据刚好30天 | 正常计算趋势 | `assert result["trend_status"] in ["uptrend", "downtrend", "sideways"]` |
| 数据刚好29天 | 返回INSUFFICIENT_DATA错误 | `assert error["code"] == "INSUFFICIENT_DATA"` |
| EMA差异刚好2% | 趋势状态为sideways | `assert result["trend_status"] == "sideways"` |

**状态断言:**

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 数据库已更新 | fund_trend表有新记录 | `assert db.query(FundTrend).filter_by(fund_code="000001").count() == 1` |
| 数据库已更新 | 最后更新时间正确 | `assert record.last_update == frozen_time` |

**副作用断言:**

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 缓存已更新 | Redis中有缓存 | `assert redis.get("fund:000001:trend") is not None` |
| 缓存已更新 | 缓存TTL正确 | `assert redis.ttl("fund:000001:trend") == 3600` |
| 日志已记录 | 日志包含成功信息 | `assert "获取基金趋势成功" in caplog.text` |

**输出排序断言:**

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 按涨幅降序 | 第一个涨幅≥第二个 | `assert result[0]["change_pct"] >= result[1]["change_pct"]` |
| 涨幅相同按代码升序 | 代码按字典序排列 | `assert result[0]["fund_code"] < result[1]["fund_code"]` |

**空结果断言:**

| 场景 | 断言点 | 断言代码 |
|---|---|---|
| 无符合条件基金 | 返回空数组 | `assert result["data"] == []` |
| 无符合条件基金 | 状态为success | `assert result["status"] == "success"` |

---

## 5. L4 质量门禁标准

### 5.1 功能原子化标准

#### R-01: 不同entry surface必须拆分

不同类型的入口不得合并成一张功能卡:

| Entry Surface | 说明 | 示例 |
|---|---|---|
| CLI命令 | 命令行入口 | `python manage.py get_fund_trend` |
| HTTP API | API端点 | `GET /api/fund/{code}/trend` |
| 页面渲染 | 页面入口 | `/fund-trend` |
| 定时任务 | 定时任务入口 | `@celery.task update_fund_trend` |
| 内部服务编排 | 服务编排 | `FundTrendOrchestrator.execute()` |

#### R-02: 不同输出contract必须拆分

如果同一入口下存在多个显著不同的响应或副作用,必须拆分。

示例 — 不能全部归入"股票分析页V2"一个feature,应拆分为:
- `/stocks/{code}/analysis` → "股票分析页"
- `/stocks/{code}/backtest` → "股票回测页"
- `/stocks/{code}/summary` → "股票摘要页"
- `/stocks/bull-industry-distribution` → "牛市行业分布页"
- `/stocks/macro-overview` → "宏观概览页"

#### R-03: 不同业务责任必须拆分

即使共享数据对象,不同业务责任也必须拆成独立feature:
- "股票池趋势监控" → 监控股票池中股票的趋势变化
- "股票池管理" → 创建、删除、修改股票池
- "股票池预警配置" → 配置股票池的预警规则

#### R-04: 不同测试fixture contract必须拆分

如果两个能力需要完全不同的前置数据或外部依赖策略,应拆成不同feature:
- "实时趋势查询" → 需要Mock数据源API、冻结时间
- "历史趋势查询" → 需要历史数据库、不需要Mock API

#### 质量标准

**定量标准:**
- 原子功能比例 ≥ 95%
- 每个功能只有1个entry surface
- 每个功能只有1个主要输出contract

**定性标准:**
- 每个功能的测试边界清晰
- 不存在"多个异质能力合并"的情况
- 功能名称明确描述单一职责

### 5.2 测试就绪标准

#### 12项检查清单

功能达到test_ready状态,必须满足以下12项:

| 编号 | 条件 | 说明 |
|---|---|---|
| 1 | 功能已原子化 | 不与其他异质能力合并 |
| 2 | 输入参数完整 | 类型/默认值/互斥规则明确 |
| 3 | 正常输出有明确schema | 有完整的JSON Schema和字段级oracle |
| 4 | 异常输出有错误码 | 错误码和触发条件明确 |
| 5 | 边界值清单完整 | 所有边界条件已列出 |
| 6 | 后置条件可断言 | 后置条件有明确验证标准 |
| 7 | 副作用可断言 | 副作用有明确验证标准 |
| 8 | 上下游依赖明确 | 依赖关系清晰 |
| 9 | 外部依赖替身策略明确 | Mock/Stub策略明确 |
| 10 | 最小fixture数据集明确 | 测试数据准备规范明确 |
| 11 | 已定义测试组索引 | 测试用例分组明确(≥8个测试组) |
| 12 | 已定义coverage claim边界 | 覆盖范围明确 |

#### 判定流程

```
1. 检查功能是否原子化
   ↓ 是
2. 检查D-02输入参数是否完整
   ↓ 是
3. 检查D-17 Test Oracle是否完整(schema + 错误码)
   ↓ 是
4. 检查D-06边界值是否完整
   ↓ 是
5. 检查D-08后置条件是否可断言
   ↓ 是
6. 检查D-09副作用是否可断言
   ↓ 是
7. 检查D-10依赖关系是否明确
   ↓ 是
8. 检查D-18 Test Fixture Contract是否完整(Mock策略 + 最小数据集)
   ↓ 是
9. 检查D-19 Test Case Groups是否完整(≥8个测试组)
   ↓ 是
10. 检查D-20 Coverage Claim是否明确
    ↓ 是
11. 标记为 test_ready ✅
```

任何一步不满足,则根据缺失程度标记为blocked或partial。

### 5.3 系统测试就绪标准

#### 8项判定标准

| 编号 | 标准 | 目标值 | 严重程度 |
|---|---|---|---|
| 1 | 权威文档声明的能力都已建模 | 100% | Critical |
| 2 | 每个feature只覆盖单一entry surface | ≥95% | Critical |
| 3 | 正常输出有完整schema和字段级oracle | 100% | Critical |
| 4 | 异常行为有完整错误码和触发条件 | 100% | Critical |
| 5 | 有最小fixture数据集定义 | 100% | Major |
| 6 | 有外部依赖mock/stub策略 | 100% | Major |
| 7 | 追踪矩阵与gap文档一致 | 100% | Critical |
| 8 | 报告明确区分"还原"和"就绪" | 100% | Major |

#### 判定流程

```
1. 检查是否存在Critical级别未达标(标准1,2,3,4,7)
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

## 6. 量化指标标准

### 6.1 M-01 功能闭合集合完成率

```
功能闭合集合完成率 = 已建模功能数 / 仓库当前支持功能总数 × 100%
```

**目标值**: 100%

**说明**: 只有100%才允许进入"完整功能地图测试设计"

### 6.2 M-02 原子功能率

```
原子功能率 = 原子功能数 / 已建模功能数 × 100%
```

**目标值**: ≥95%

**说明**: 确保功能拆分粒度合理

### 6.3 M-03 Oracle完整率

```
Oracle完整率 = oracle完整的功能数 / 已建模功能数 × 100%
```

**目标值**: ≥90%

**说明**: 确保每个功能都有明确的测试断言标准

### 6.4 M-04 Fixture完整率

```
Fixture完整率 = fixture就绪的功能数 / 已建模功能数 × 100%
```

**目标值**: ≥90%

**说明**: 确保每个功能都有明确的测试数据准备规范

### 6.5 M-05 测试追踪完整率

```
测试追踪完整率 = 已建立Feature→TestCaseGroup链路的功能数 / 已建模功能数 × 100%
```

**目标值**: 100%

**说明**: 确保每个功能都有测试追踪

### 6.6 M-06 规则负向覆盖率

```
规则负向覆盖率 = 已建立Rule→NegativeTest链路的规则数 / 规则总数 × 100%
```

**目标值**: 100%

**说明**: 确保每个业务规则都有负向测试

### 6.7 M-07 覆盖宣称可信率

```
覆盖宣称可信率 = coverage_claim_allowed=yes的功能数 / 已建模功能数 × 100%
```

**目标值**: 只有在M-01~M-06全部达标后,才允许接近100%

**说明**: 防止虚假的"coverage=100%"声明

### 6.8 综合验收标准

| 指标 | 目标值 | 阻塞级别 |
|---|---|---|
| M-01 功能闭合集合完成率 | 100% | Critical |
| M-02 原子功能率 | ≥95% | Major |
| M-03 Oracle完整率 | ≥90% | Critical |
| M-04 Fixture完整率 | ≥90% | Major |
| M-05 测试追踪完整率 | 100% | Major |
| M-06 规则负向覆盖率 | 100% | Major |
| M-07 覆盖宣称可信率 | ≥75% | Minor |

只有所有Critical指标达标,才允许宣称"测试就绪完成"。

---

## 7. 标准使用说明

### 7.1 pb-review如何使用本标准

1. **还原阶段**: 对照本标准,从代码和文档中还原当前状态
2. **对比阶段**: 将还原的现状与本标准进行逐项对比
3. **识别阶段**: 明确指出哪些标准未达到,差距有多大
4. **量化阶段**: 计算各项量化指标,给出完整度评分

### 7.2 改造如何使用本标准

1. **目标设定**: 基于本标准,设定改造目标
2. **差距分析**: 基于pb-review的差距识别结果,制定改造计划
3. **验收标准**: 基于本标准,制定改造验收标准
4. **进度追踪**: 基于本标准的量化指标,追踪改造进度

---

## 附录

### A. 术语表

| 术语 | 定义 |
|---|---|
| Test Oracle | 测试断言的标准答案,定义了"如何判断功能执行正确" |
| Test Fixture | 测试数据和环境的准备规范,确保测试环境的可复现性 |
| Test Case Group | 按测试目标分组的测试用例集合 |
| Coverage Claim | 对功能测试覆盖范围的明确声明 |
| Feature Closure | 功能闭合,即所有能力都已建模 |
| Atomic Feature | 原子功能,可单独断言输入输出的最小功能单元 |
| Testability Status | 测试就绪状态,分为blocked/partial/test_ready |
| Traceability Matrix | 追踪矩阵,建立需求→功能→测试的映射关系 |
| Gap Analysis | 差距分析,识别现状与理想状态之间的差距 |
| Testability Score | 测试化评分,量化评估系统的测试就绪程度 |
| Entry Surface | 功能入口类型,如CLI/API/页面/定时任务/服务编排 |
| Mock/Stub | 外部依赖的替身,用于隔离测试环境 |
| Fixture Contract | 测试数据准备的契约规范 |
| Negative Test | 负向测试,验证业务规则被违反时的行为 |
| Side Effect | 副作用,功能执行后对系统状态的改变(如缓存更新、日志记录) |

### B. 示例库

#### B.1 完整功能规格卡示例(含D-17~D-20)

参见源文档`pb-review-testability-upgrade-checklist.md`中的archer项目"获取基金趋势"功能完整示例。

#### B.2 追踪矩阵示例

参见本文档2.4节中的追踪矩阵标准定义,以及源文档中的archer项目追踪矩阵示例。

#### B.3 Gap分析示例

参见本文档2.5节中的差距分析标准定义,以及源文档中的archer项目Gap分析示例。

### C. 参考资料

| 资料 | 说明 |
|---|---|
| `pb-review-testability-upgrade-checklist.md` | 测试化评估标准(含评估方法和改造建议) |
| `feature-specification-standard.md` | 功能规格卡标准(D-01~D-16) |
| `pb-review-deliverable-standard.md` | 交付物标准 |

---

**文档结束**

