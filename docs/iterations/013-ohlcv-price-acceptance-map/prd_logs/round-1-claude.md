# ASP Spec Audit Report

**Reviewer**: Claude
**Round**: 1
**Audit Date**: 2026-03-31
**Status**: FAIL

---

## Previous Rounds Summary

- 本迭代暂无历史产品审查记录。

---

## 1. 宪法符合性检查

### 1.1 零假设原则
⚠️ **部分通过** - `design-brief.md` 与 `proposal.md` 的探讨链路完整，但 `FT-007` 直接为 `partition_mode` 注入默认值 `adaptive_volatility`，该默认行为未在上游合同中锁定，属于规格阶段补充假设。

### 1.2 小步提交原则
✅ **通过** - 文档按 `design-brief.md -> proposal.md -> feature-spec-index.md -> feature-specs/*.md` 顺序产出，阶段边界清晰。

### 1.3 借鉴现有，而后创造
✅ **通过** - `proposal.md` 已明确仓库现有能力有限，未虚构可复用的领域实现。

### 1.4 务实优于教条
✅ **通过** - 一期范围聚焦在算法、JSON 和最小展示闭环，没有把未来事件概率、交易建议和架构实现提前写入产品阶段。

### 1.5 意图清晰
⚠️ **部分通过** - 主线意图清楚，但 `FT-005` 对“波动自适应区域插件”的核心规则仍保留“尚未收敛为唯一参数口径”的表述，削弱了规格作为合同事实源的清晰度。

---

## 2. 双向覆盖检查

### 2.1 前置探讨追溯（design-brief -> proposal）
✅ **通过** - `proposal.md` 已回溯 `design-brief.md` 的目标摘要、验证方式和推荐方向，主线一致，无方向冲突。

### 2.2 正向覆盖（REQ -> Feature）
⚠️ **未完全通过** - 大部分 `REQ` 已覆盖，但 `REQ-009` 的 CLI 输入边界未被完整承接。`proposal.md` 要求“用户可通过 CLI 输入 OHLCV 数据源或数据文件”，而 `FT-007` 仅定义了 `input_file`，未定义任何“数据源”输入方式。

### 2.3 反向溢出（Feature -> REQ）
⚠️ **未完全通过** - `FT-007` 添加了 `partition_mode` 的默认值 `adaptive_volatility`，该默认行为在 `proposal.md` 中没有对应合同事实，且 `design-brief.md` 明确把“区域插件的默认参数和切分细节”保留为待收敛项。

### 2.4 排除项入侵
✅ **通过** - 未发现 `EXC-001 ~ EXC-006` 重新出现在 `feature-specs` 中。

---

## 3. 逻辑自洽性检查

### 3.1 核心算法主线
✅ **通过** - `price_acceptance_probability`、`micro_bins = 100`、指数衰减、区域聚合等主线在 `design-brief.md`、`proposal.md`、`FT-002`、`FT-003`、`FT-006` 间保持一致。

### 3.2 区域插件合同完整性
❌ **失败** - `REQ-006` 是必须项，且 `FT-005` 被标记为 `P0`；但规格卡自身承认“自适应区域规则尚未收敛为唯一参数口径”，说明该必做功能目前仍不是唯一、可测试、可实现的一组合同事实。

### 3.3 测试化完整性
⚠️ **警告** - `feature-spec-index.md` 将全部功能的 Oracle / Fixture 完整度写为 `100%`，但多张规格卡的 `D-20` 仍保留未闭合断言点与阻塞原因，当前完整度口径偏乐观。

---

## 4. 问题清单

### 4.1 BLOCKER

无

### 4.2 MAJOR

1. **REQ-009 的 CLI 输入边界未完整覆盖**
   - **证据**:
     - `docs/iterations/013-ohlcv-price-acceptance-map/proposal.md:59`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-007.md:18-25`
   - **问题**:
     - `proposal.md` 将 CLI 输入定义为“OHLCV 数据源或数据文件”，但 `FT-007` 只定义了 `input_file`，没有任何“数据源”输入契约。
   - **影响**:
     - `REQ -> Feature` 覆盖不完整，CLI 合同与上游需求边界不一致。

2. **CLI 默认区域插件被规格卡私自锁定，违反上游“待收敛项”边界**
   - **证据**:
     - `docs/iterations/013-ohlcv-price-acceptance-map/design-brief.md:188-190`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-007.md:23`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-007.md:74-77`
   - **问题**:
     - 上游 brief 明确将“区域插件的默认参数和切分细节”保留为待在 `proposal.md` 收敛的未决项，但 `FT-007` 已将 CLI 默认 `partition_mode` 写死为 `adaptive_volatility`。
   - **影响**:
     - 规格阶段引入未被合同锁定的用户可见默认行为，破坏零假设原则和文档追溯闭环。

3. **FT-005 对必做的自适应区域插件仍缺少唯一实现口径**
   - **证据**:
     - `docs/iterations/013-ohlcv-price-acceptance-map/proposal.md:55-56`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-005.md:32-36`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-005.md:78-80`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-005.md:104-107`
   - **问题**:
     - `REQ-006` 要求一期必须支持波动自适应与等宽区域插件两种模式，但 `FT-005` 仍明确写出“自适应区域规则尚未收敛为唯一参数口径”。
   - **影响**:
     - 该 `P0` 功能无法形成唯一、可实现、可验证的产品合同，直接削弱后续架构与实现阶段的确定性。

### 4.3 MINOR

1. **功能索引中的 Oracle / Fixture 完整度口径偏乐观**
   - **证据**:
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-spec-index.md:11-18`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-005.md:104-107`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-006.md:119-122`
     - `docs/iterations/013-ohlcv-price-acceptance-map/feature-specs/FT-007.md:107-110`
   - **问题**:
     - 索引将全部功能标记为 `100%`，但多张规格卡仍写明未闭合断言点和阻塞原因。
   - **影响**:
     - 不阻塞继续修订，但会误导后续 reviewer / visualizer 对测试化成熟度的判断。

---

## 5. 审查结论

**总体评价**：文档主线方向正确，`design-brief -> proposal -> specs` 链路已建立，但当前还不能判定为通过。

**FAIL 理由**：
1. `REQ-009` 在 CLI 规格中未被完整承接，存在明确覆盖缺口。
2. `FT-007` 将上游未锁定的区域插件默认行为写成既定事实，破坏追溯闭环。
3. `FT-005` 对 `P0` 的自适应区域插件仍未形成唯一合同口径，影响后续实现与测试确定性。

**本轮结论**：
- 需要先修复上述 `MAJOR` 问题，再进入下一轮产品审查。

---

**审查状态**: ❌ FAIL
**下一步**: 进入产品文档修补轮次，修复 `MAJOR` 后再发起新一轮 reviewer 审查
