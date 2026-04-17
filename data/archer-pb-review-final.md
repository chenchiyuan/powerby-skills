# Archer 项目还原式评审报告

- 评审对象：`/Users/chenchiyuan/projects/archer`
- 产品文档目录：`/Users/chenchiyuan/projects/archer/docs`
- 产出方式：基于 `pb-review` bootstrap 结果继续由当前 Codex 会话完成产品还原、功能还原、关系整理与 gap 归纳
- 生成时间：2026-03-27

---

## 1. 评审结论摘要

Archer 当前已经不是若干离散脚本的集合，而是一个以 Django 单体为底座、以统一编排器为主入口、覆盖 A 股 / Token / 商品三大业务域的量化分析与监控平台。

从产品侧看，系统的主入口已经明确收敛为三类：

1. `initial_data`：首次初始化
2. `update_data`：日常增量更新并自动串联下游
3. `run --task ...`：执行已注册业务任务

从实现侧看，上述主入口与服务注册表、业务命令、测试用例基本对齐，说明这不是“文档声明型产品”，而是已经具备可执行、可验证的系统。

但从 `pb-review` 追踪视角，仍存在两个关键缺口：

1. `scan_ema_signal` 已是正式产品能力，但当前 AI skill 层未见独立封装，AI 路由不完整
2. `intraday_monitor` 的真实前置依赖包含 `fetch_realtime_snapshot`，但统一注册表未显式建模这条依赖，编排层语义仍不完整

---

## 2. 权威来源与边界

### 2.1 权威产品文档

以下文档可视为本次产品还原的主证据：

1. `docs/services.md`
2. `docs/ARCHITECTURE.md`
3. `docs/orchestration-guide.md`
4. `docs/service-dependencies.md`

其中最关键的是：

- `docs/services.md` 明确声明“本文是当前项目唯一对外权威文档”
- `docs/accepted-features.md` 与 `docs/accepted-features-index.md` 也都回指 `docs/services.md`

### 2.2 本次评审边界

本次评审采用如下边界：

- 产品侧：优先使用 `docs/services.md`
- 架构侧：使用 `docs/ARCHITECTURE.md`
- 编排侧：使用 `docs/orchestration-guide.md` 与 `archer/apps/core/orchestration/registry.py`
- 实现侧：使用各业务命令、Service、Repository、Skill、测试文件
- 历史迭代文档：仅作为补充证据，不作为第一权威来源

### 2.3 明确不采用的误导边界

以下做法本次明确排除：

- 不把整个 `docs/` 目录等同于同权产品文档
- 不把 `README.md` 当成 Archer 当前权威产品说明
- 不把 `docs/iterations/*` 当成高于 `docs/services.md` 的需求源

---

## 3. 产品对象还原

## 3.1 Goal

Archer 的目标可以还原为：

构建一个统一的量化数据编排与信号分析平台，覆盖 A 股、Token、商品三类市场，在统一入口下完成初始化、增量更新、趋势分析、策略计算、选股监控与 AI skill 执行接入。

进一步拆开，目标包含：

1. 统一数据入口，避免用户直接操作大量底层命令
2. 把跨市场能力收敛到统一 orchestration 模型
3. 让分析结果可重复执行、可验证、可推送
4. 为 AI skill 提供标准化执行入口

## 3.2 Role

可还原出 3 类核心角色：

### R1. 手动操作者

负责在量化 settings 下执行：

- 首次初始化
- 日常更新
- 指定任务执行
- 排障与补数

### R2. AI 调用者

通过 `archer-*` skills 触发稳定能力，例如：

- `archer-initial-data`
- `archer-update-data`
- `archer-select-stocks`
- `archer-intraday-monitor`
- `archer-manage-stock-pool`
- `archer-monitor-token-trend`
- `archer-get-com-trend`

### R3. 开发 / 排障人员

在必要时直接使用：

- 业务直连命令
- 页面入口
- Service / Repository
- Django Admin

## 3.3 Scenario

主要业务场景可以还原为：

### S1. 首次建库

用户执行 `initial_data`，初始化三大业务域基础主数据。

### S2. 日常盘后增量更新

用户执行 `update_data`，系统自动补齐数据缺口并串联趋势 / 计算链路。

### S3. A 股盘后选股

用户执行 `select_stocks`，系统整合新高突破与智能回调，输出候选结果及 CSV。

### S4. A 股盘中监控

用户先执行 `fetch_realtime_snapshot`，再执行 `intraday_monitor`，实时筛选突破买入与回调买入。

### S5. 股票池管理与预警

用户通过 skill / shell / admin 对股票池进行增删改查，并绑定预警指标。

### S6. Token 趋势监控

用户执行 `monitor_token_trend`，对指定 token 列表进行 EMA 趋势监控，并按条件推送。

### S7. Token 全市场扫描

用户执行 `scan_ema_signal`，对全市场交易对做信号扫描并导出 CSV。

### S8. 商品趋势分析

用户执行 `get_com_trend`，输出商品多头 / 空头趋势及分类结果。

## 3.4 Constraint

当前产品约束可以还原为：

1. Archer 是 Django 单体，不是微服务系统
2. 主执行 settings 为 `archer.projects.quant.settings`
3. 手动执行优先走统一入口，不优先直打底层命令
4. `run --task` 仅执行注册表中已有任务
5. `update_data --only` 只允许 `ashare` / `token` / `commodity`
6. `monitor_token_trend` 在非 dry-run / no-push 模式下要求 `HUICHENG_TOKEN`
7. A 股相关同步在部分场景下要求 `TUSHARE_TOKEN`
8. 架构依赖必须遵循 `apps -> shared -> libs -> core`

## 3.5 Non-goal

以下能力当前不应被误判为主产品目标：

1. 不是通用数据中台
2. 不是通用回测平台
3. 不是统一编排器可覆盖一切命令的系统
4. 股票池“分类”不是独立数据模型字段
5. `intraday_monitor` 不是 `select_stocks` 的替代品

---

## 4. 架构与编排模型还原

## 4.1 技术形态

Archer 被架构文档定义为“多项目共存的 Django 单体框架”。

它采用四层结构：

1. `core`
2. `libs`
3. `shared`
4. `apps`

并显式规定依赖方向：

- `apps -> shared -> libs -> core`
- 禁止反向依赖与循环依赖

## 4.2 统一编排模型

统一编排器对外暴露三类入口：

1. `initial_data`
2. `update_data`
3. `run`

它们的职责分别是：

### initial_data

- 初始化基础数据
- 按业务域执行首轮建库动作

### update_data

- 增量更新数据
- 串联必要下游依赖
- 支持断点恢复与时间范围更新

### run

- 校验任务是否注册
- 检查部分任务的新鲜度
- 执行指定业务任务

## 4.3 服务注册表

当前统一注册表覆盖三大业务域：

### A 股

- `sync_ashare_data`
- `update_ashare_klines`
- `import_fund_klines`
- `get_fund_trend`
- `compute_new_high_breakout`
- `select_stocks`
- `intraday_monitor`
- `query_industry_trend`

### Token

- `sync_contracts`
- `update_symbols`
- `monitor_token_trend`
- `scan_ema_signal`

### 商品

- `update_commodities`
- `import_commodity_klines`
- `get_com_trend`

---

## 5. 功能目录

## 5.1 统一编排层

| 功能 ID | 功能名 | 作用 | 主入口 | 状态 |
|---|---|---|---|---|
| F-ORCH-001 | 首次初始化 | 初始化三域基础主数据 | `initial_data` | 已实现 |
| F-ORCH-002 | 统一增量更新 | 检测缺口并串联自动链路 | `update_data` | 已实现 |
| F-ORCH-003 | 统一任务调度 | 列出并执行已注册任务 | `run --task` | 已实现 |
| F-ORCH-004 | 断点恢复 | 对更新任务做 checkpoint 恢复 | `update_data --resume` | 已实现 |
| F-ORCH-005 | freshness 校验 | 执行部分任务前检查数据新鲜度 | `run --task` | 已实现 |

## 5.2 A 股域

| 功能 ID | 功能名 | 作用 | 入口 | 状态 |
|---|---|---|---|---|
| F-AS-001 | A 股基础数据同步 | 同步股票/ETF 基础主数据 | `sync_ashare_data` | 已实现 |
| F-AS-002 | A 股日线更新 | 批量更新个股日线 K 线 | `update_ashare_klines` | 已实现 |
| F-AS-003 | 基金 / 指数 K 线导入 | 趋势分析数据源 | `import_fund_klines` | 已实现 |
| F-AS-004 | ETF / 行业趋势分析 | 计算基金与行业趋势 | `get_fund_trend` | 已实现 |
| F-AS-005 | 新高突破计算 | 生成 breakout 结果与缓存 | `compute_new_high_breakout` | 已实现 |
| F-AS-006 | 盘后选股 | 整合 breakout + 智能回调 | `select_stocks` | 已实现 |
| F-AS-007 | 实时快照采集 | 盘中写入 `RealtimeQuote` | `fetch_realtime_snapshot` | 已实现 |
| F-AS-008 | 盘中监控 | 输出突破 / 回调买入结果 | `intraday_monitor` | 已实现 |
| F-AS-009 | 行业趋势查询 | 查询行业趋势历史 | `query_industry_trend` | 已实现 |
| F-AS-010 | 股票池管理 | 管理股票池、成员、配置 | Repository / Admin / Skill | 已实现 |
| F-AS-011 | 股票池趋势监控 | 扫描池内新信号，支持导出与推送 | `monitor_stock_pool` | 已实现 |
| F-AS-012 | 预警指标初始化 | 初始化默认 9 个指标及默认池配置 | `init_alert_indicators` | 已实现 |
| F-AS-013 | 单股风险预警缓存 | 计算单股预警缓存 | `compute_risk_alert` | 已实现 |
| F-AS-014 | 宏观总览聚合 | 聚合指数、行业、突破、回调信息 | `macro_overview_service.py` | 已实现 |
| F-AS-015 | 回调总览 | 汇总最近交易日回调股票 | `select_stocks_overview_service.py` | 已实现 |
| F-AS-016 | 股票分析页 v2 | 页面化展示分析能力 | `views.py` / `stock_analysis_v2.html` | 已实现 |

## 5.3 Token 域

| 功能 ID | 功能名 | 作用 | 入口 | 状态 |
|---|---|---|---|---|
| F-TK-001 | 交易对同步 | 同步合约与现货交易对 | `sync_contracts` | 已实现 |
| F-TK-002 | Token K 线更新 | 拉取并落库 Token K 线 | `update_symbols` | 已实现 |
| F-TK-003 | Token 趋势监控 | 对指定 token 列表做 EMA 趋势监控 | `monitor_token_trend` | 已实现 |
| F-TK-004 | EMA 全市场扫描 | 对全市场交易对做信号扫描 | `scan_ema_signal` | 已实现 |

## 5.4 商品域

| 功能 ID | 功能名 | 作用 | 入口 | 状态 |
|---|---|---|---|---|
| F-CM-001 | 商品列表初始化 | 初始化 / 维护商品列表 | `update_commodities` | 已实现 |
| F-CM-002 | 商品 K 线导入 | 导入商品 K 线 | `import_commodity_klines` | 已实现 |
| F-CM-003 | 商品趋势分析 | 输出商品多头 / 空头趋势与分类结果 | `get_com_trend` | 已实现 |

## 5.5 AI Skill 层

| 功能 ID | Skill 名 | 对应能力 | 状态 |
|---|---|---|---|
| F-SK-001 | `archer-initial-data` | 首次初始化 | 已实现 |
| F-SK-002 | `archer-update-data` | 日常统一更新 | 已实现 |
| F-SK-003 | `archer-select-stocks` | 盘后选股 | 已实现 |
| F-SK-004 | `archer-intraday-monitor` | 盘中监控 | 已实现 |
| F-SK-005 | `archer-manage-stock-pool` | 股票池管理 / 指标绑定 | 已实现 |
| F-SK-006 | `archer-monitor-stock-pool` | 股票池监控 / 预警说明 | 已实现 |
| F-SK-007 | `archer-monitor-token-trend` | Token 趋势监控 | 已实现 |
| F-SK-008 | `archer-get-com-trend` | 商品趋势 | 已实现 |

---

## 6. 规则与边界目录

| 规则 ID | 规则 / 边界 | 说明 |
|---|---|---|
| R-001 | 手动执行优先级固定 | `initial_data` > `update_data` > `run --task` > 底层命令 / 页面 / 服务类 |
| R-002 | 非必要不绕过编排器 | 文档明确要求除非明确需要，否则不要优先调用底层命令 |
| R-003 | `initial_data` 不负责完整增量链路 | 只服务于首次初始化 / 换库 / 建库 |
| R-004 | `update_data --only` 仅允许三域 | 只允许 `ashare` / `token` / `commodity` |
| R-005 | `run --task` 一次只能执行一个服务 | 禁止批量调用 |
| R-006 | freshness required 任务需先通过新鲜度检查 | 至少对 `select_stocks`、`intraday_monitor`、`query_industry_trend`、`monitor_token_trend`、`scan_ema_signal`、`get_com_trend` 有约束 |
| R-007 | `intraday_monitor` 依赖实时快照 | 无快照时应提示先执行 `fetch_realtime_snapshot` |
| R-008 | `select_stocks` 依赖 A 股个股日线 | 目标日期无 K 线时应直接失败 |
| R-009 | `monitor_token_trend` interval 受限 | 仅允许 `4h` / `1d` |
| R-010 | `monitor_token_trend` 非 dry-run 模式要求 `HUICHENG_TOKEN` | 否则报错 |
| R-011 | 商品趋势分类固定四类 | `energy` / `metal` / `agriculture` / `other` |
| R-012 | 股票池“分类”不是独立字段 | 通过池名、描述、启停状态、指标绑定表达业务语义 |
| R-013 | `monitor_stock_pool` 与 `AlertIndicatorService` 不是同一功能 | 前者是趋势监控，后者是预警计算 |
| R-014 | Archer 是 Django 单体 | 不是微服务架构 |
| R-015 | 架构依赖方向固定 | `apps -> shared -> libs -> core`，禁止循环依赖 |

---

## 7. 功能验证矩阵

| 功能 ID | 验证入口 | 验证点 | 证据 |
|---|---|---|---|
| F-ORCH-001 | `test_initial_data_command.py` | `--only/--force`、已有数据跳过 | `archer/apps/core/tests/test_initial_data_command.py` |
| F-ORCH-002 | `test_update_data_command.py` | 自动链路、checkpoint、恢复 | `archer/apps/core/tests/test_update_data_command.py` |
| F-ORCH-003 | `test_run_command.py` + `test_registry.py` | 列表、任务调度、非法输入、注册表正确性 | `archer/apps/core/tests/test_run_command.py` |
| F-AS-007 | `test_fetch_realtime_snapshot_command.py` | Sina -> Eastmoney -> AkShare 回退链、正确落库 | `archer/apps/ashare/tests/test_fetch_realtime_snapshot_command.py` |
| F-AS-008 | `test_intraday_monitor_command.py` | 行业上涨二次总结、回调展示过滤 | `archer/apps/ashare/tests/test_intraday_monitor_command.py` |
| F-AS-006 | `test_select_stocks_command.py` | 二次总结、回调显示、目标日无 K 线快速失败 | `archer/apps/ashare/tests/test_select_stocks_command.py` |
| F-AS-011 | `test_monitor_stock_pool_command.py` | 扫描、CSV、推送逻辑、去重 / 统计 | `archer/apps/ashare/tests/test_monitor_stock_pool_command.py` |
| F-AS-010 / F-AS-012 / F-AS-013 | repository / model / indicator tests | 股票池管理、指标初始化、预警绑定 | `archer/apps/ashare/tests/test_stock_pool_repository.py` / `test_stock_alert_indicators.py` |
| F-TK-003 | `test_monitor_token_trend_command.py` | token 列表优先级、交易对筛选、跨市场合并、token 校验 | `archer/apps/tokens/tests/test_monitor_token_trend_command.py` |
| F-TK-004 | `test_scan_ema_signal_optimization.py` | 全市场扫描性能与行为 | `archer/apps/tokens/tests/test_scan_ema_signal_optimization.py` |
| F-CM-001 / F-CM-002 / F-CM-003 | `test_commands.py` | 初始化、导入、趋势输出、CSV、缺数据报错 | `archer/apps/commodities/tests/test_commands.py` |

结论：

- 统一编排层存在明确测试
- A 股主流程存在明确测试
- Token 主流程存在明确测试
- 商品主流程存在明确测试
- 股票池与预警链路也存在专门测试

因此，从“可验证功能系统”的标准看，Archer 已具备较强证据基础。

---

## 8. 产品要求到实现入口追踪矩阵

| 需求对象 | 需求含义 | 实现入口 | AI Skill 入口 | 结论 |
|---|---|---|---|---|
| G-001 | 统一初始化入口 | `initial_data.py` | `archer-initial-data` | 已对齐 |
| G-002 | 统一增量更新入口 | `update_data.py` | `archer-update-data` | 已对齐 |
| G-003 | 统一已注册任务调度 | `run.py` + `registry.py` | 无单独 skill | 已对齐 |
| G-004 | A 股盘后选股 | `select_stocks.py` | `archer-select-stocks` | 已对齐 |
| G-005 | A 股盘中监控 | `intraday_monitor.py` | `archer-intraday-monitor` | 已对齐但依赖建模不完整 |
| G-006 | 股票池管理 | Repository / Model / Admin | `archer-manage-stock-pool` | 已对齐 |
| G-007 | 股票池趋势监控 | `monitor_stock_pool.py` | `archer-monitor-stock-pool` | 已对齐 |
| G-008 | Token 趋势监控 | `monitor_token_trend.py` | `archer-monitor-token-trend` | 已对齐 |
| G-009 | Token 全市场扫描 | `scan_ema_signal.py` | 未见独立 skill | 代码已实现，skill 缺口存在 |
| G-010 | 商品趋势分析 | `get_com_trend.py` | `archer-get-com-trend` | 已对齐 |

---

## 9. 差异与缺口

## 9.1 明确缺口

### GAP-001：`scan_ema_signal` 缺少独立 AI skill 封装

现状：

- 产品文档明确把 `scan_ema_signal` 列为已注册服务
- 代码实现也存在
- 但当前“已封装的 Skill”列表中没有对应独立 skill

影响：

- AI 路由层不完整
- 用户可以手动跑命令，但不能等价地通过标准原子 skill 触发

建议：

- 新增 `archer-scan-ema-signal` skill
- 结构应对齐当前其它 Archer skills 的规范

### GAP-002：`intraday_monitor` 的真实依赖未被注册表完整表达

现状：

- 业务命令明确要求先有 `fetch_realtime_snapshot`
- 注册表只记录了 `sync_ashare_data`、`get_fund_trend`、`compute_new_high_breakout`

影响：

- 编排器层面的依赖语义与业务真实依赖不完全一致
- 可能导致任务被错误判定为“前置已满足”

建议：

- 在注册语义层显式纳入 `fetch_realtime_snapshot` 依赖，或单独定义“运行时实时依赖”字段

### GAP-003：产品文档目录过宽会引入历史噪声

现状：

- 本次 bootstrap 使用 `docs/` 作为产品文档目录
- 其中包含大量 `docs/iterations/*`

影响：

- 容易把历史方案、旧状态、已废弃讨论混入产品事实还原

建议：

- 下次正式评审时，把产品文档入口收敛到：
  - `docs/services.md`
  - `docs/ARCHITECTURE.md`
  - `docs/orchestration-guide.md`
  - `docs/service-dependencies.md`

## 9.2 非缺陷但需明确的边界

### NOTE-001：股票池管理不是 `run --task` 一级入口

这不是 bug。

它当前属于：

- skill 入口
- repository / model / admin 入口

而不是统一编排器主入口。

### NOTE-002：股票池“分类”不是数据库字段

这不是缺失实现，而是当前产品语义定义如此。

所谓分类由以下内容共同表达：

- 池名
- 描述
- 是否启用
- 绑定预警指标

---

## 10. 最终判断

### 10.1 完成度判断

如果从“是否形成稳定产品能力”来看，Archer 当前结论是：

已形成稳定、可执行、可验证、带统一编排入口的三域量化分析平台。

### 10.2 从 `pb-review` 的完成判定看

如果标准是“需求可还原、功能可列举、边界清晰、验证方式明确”，则当前结论为：

1. 产品目标已可还原
2. 角色与场景已可还原
3. 功能列表已可逐条列出
4. 功能边界已可明确
5. 核心验证方式已可指向具体测试
6. 主要 gap 已被显式标出

因此，本轮针对 Archer 的 `pb-review` 目标已经能够产出“可审阅最终稿”。

但如果标准进一步提高到“对象 / 关系 / gap 全量机器化 registry 完整落库”，则仍缺：

- product object registry
- feature object registry
- relation registry
- gap registry

本文件是基于 bootstrap 后由宿主会话继续完成的最终人工编排版结果，不是完整的 `.review/` 机器产物替代品。

---

## 11. 证据索引

### 11.1 权威产品文档

- `/Users/chenchiyuan/projects/archer/docs/services.md`
- `/Users/chenchiyuan/projects/archer/docs/accepted-features.md`
- `/Users/chenchiyuan/projects/archer/docs/accepted-features-index.md`
- `/Users/chenchiyuan/projects/archer/docs/orchestration-guide.md`
- `/Users/chenchiyuan/projects/archer/docs/service-dependencies.md`

### 11.2 架构与编排实现

- `/Users/chenchiyuan/projects/archer/docs/ARCHITECTURE.md`
- `/Users/chenchiyuan/projects/archer/archer/apps/core/orchestration/registry.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/core/management/commands/initial_data.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/core/management/commands/update_data.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/core/management/commands/run.py`

### 11.3 A 股实现证据

- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/management/commands/select_stocks.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/management/commands/intraday_monitor.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/management/commands/fetch_realtime_snapshot.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/management/commands/monitor_stock_pool.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/services/macro_overview_service.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/services/select_stocks_overview_service.py`

### 11.4 Token 实现证据

- `/Users/chenchiyuan/projects/archer/archer/apps/tokens/management/commands/monitor_token_trend.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/tokens/management/commands/scan_ema_signal.py`

### 11.5 商品实现证据

- `/Users/chenchiyuan/projects/archer/archer/apps/commodities/management/commands/get_com_trend.py`

### 11.6 Skill 证据

- `/Users/chenchiyuan/projects/archer/skills/archer-initial-data/SKILL.md`
- `/Users/chenchiyuan/projects/archer/skills/archer-update-data/SKILL.md`
- `/Users/chenchiyuan/projects/archer/skills/archer-select-stocks/SKILL.md`
- `/Users/chenchiyuan/projects/archer/skills/archer-intraday-monitor/SKILL.md`
- `/Users/chenchiyuan/projects/archer/skills/archer-manage-stock-pool/SKILL.md`
- `/Users/chenchiyuan/projects/archer/skills/archer-monitor-token-trend/SKILL.md`
- `/Users/chenchiyuan/projects/archer/skills/archer-get-com-trend/SKILL.md`

### 11.7 测试证据

- `/Users/chenchiyuan/projects/archer/archer/apps/core/tests/test_initial_data_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/core/tests/test_update_data_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/core/tests/test_run_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/core/tests/test_registry.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/tests/test_fetch_realtime_snapshot_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/tests/test_intraday_monitor_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/tests/test_select_stocks_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/tests/test_monitor_stock_pool_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/tests/test_stock_pool_repository.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/ashare/tests/test_stock_alert_indicators.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/tokens/tests/test_monitor_token_trend_command.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/tokens/tests/test_scan_ema_signal_optimization.py`
- `/Users/chenchiyuan/projects/archer/archer/apps/commodities/tests/test_commands.py`

---

## 12. 建议的后续动作

1. 为 `scan_ema_signal` 补齐独立 AI skill
2. 在统一注册语义层补全 `intraday_monitor -> fetch_realtime_snapshot` 依赖表达
3. 让 `pb-review` 下一轮对 Archer 直接以 `docs/services.md` 为产品主入口，而不是宽泛 `docs/`
4. 如果需要完整的机器可恢复评审结果，再把本报告中的对象、关系、gap 进一步落成 `.review/*.json`
