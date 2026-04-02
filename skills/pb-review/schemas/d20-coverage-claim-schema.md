# Schema: D-20 Coverage Claim

**版本**: 1.0.0
**来源**: pb-review-standard.md §3.5
**引用 Skill**: pb-review-feature-reconstructor

## 定义

| 条件编号 | 条件名称 | 检查内容 |
|---|---|---|
| D20-1 | Oracle 达标 | oracle_completeness >= 90 |
| D20-2 | Fixture 达标 | fixture_readiness >= 90 |
| D20-3 | 测试组达标 | test_case_group_count >= 8 |
| D20-4 | Schema 已定义 | D17-1 != missing |
| D20-5 | 业务规则已定义 | D17-9 != missing |
| D20-6 | 错误码已有测试 | 所有错误码有对应测试用例 |
| D20-7 | 边界条件已有测试 | 所有边界条件有对应测试用例 |
| D20-8 | 无未闭合 gap | 当前功能无阻塞测试化的 gap |

## 评估规则

- 满足全部 8 项条件时，`allowed = yes`
- 否则 `allowed = no`
- 必须同时输出 `coverage_scope`、`blocking_reasons` 与未覆盖清单

## 数据结构

```yaml
d20_coverage_claim:
  allowed: yes | no
  coverage_scope: string | null
  blocking_reasons: array | null
  uncovered_sub_capabilities: array | null
  unclosed_assertion_points: array | null
  unstandardized_fixtures: array | null
```

## 示例

```yaml
d20_coverage_claim:
  allowed: no
  coverage_scope: null
  blocking_reasons:
    - oracle_completeness < 90
```
