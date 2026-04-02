# 实现报告

**迭代编号**: 013
**项目名称**: ohlcv-price-acceptance-map
**生成日期**: 2026-03-31
**状态**: Final

---

## 1. 实现摘要

本次交付实现了完整的 OHLCV 历史价格接受度分析链路：输入校验、固定 `100` 份微价格轴、指数衰减成交量分配引擎、区域插件框架、区域聚合、CLI JSON 输出和静态 Web 可视化结果页。核心算法遵循 `time_weight * volume` 在 `[low, high]` 覆盖到的 `micro bins` 中均匀分配的产品合同，不引入 Monte Carlo、数据库或在线 API。

## 2. 变更清单

- 新增 `powerby/acceptance_map/` 计算核心与区域插件
- 新增 `powerby/cli/acceptance_map.py` CLI 分析入口
- 新增 `web/acceptance-map/index.html`
- 新增 `web/acceptance-map/app.js`
- 新增 `tests/acceptance_map/` 测试集
- 新增 `tests/conftest.py`
- 新增 `docs/iterations/013-ohlcv-price-acceptance-map/tasks.md`

## 3. 关键实现点

- FT-001: 以确定性错误码实现 OHLCV 输入校验和标准化
- FT-002: 以固定 `micro_bins=100` 构建连续、无重叠价格轴
- FT-003: 以指数衰减权重实现 `price_acceptance_probability`
- FT-004 / FT-005: 实现 `equal_width` 与 `adaptive_volatility` 两类区域插件和合同校验
- FT-006: 输出热力图、区域排序结果和诊断字段开关
- FT-007: 支持本地文件输入、JSON 输出和失败错误透传
- FT-008: 提供静态页面消费分析结果 JSON，并支持无 heatmap 时的降级展示

## 4. 验证记录

- `pytest -q tests/acceptance_map` -> `59 passed`
- `pytest -q tests` -> `93 passed`

## 5. 结果

- 013 文档定义的核心分析链路已经落地为可运行代码。
- CLI 已可通过 `python -m powerby.cli acceptance-map` 产出结构化 JSON。
- Web 结果页已可作为消费层展示热力图和区域列表。
