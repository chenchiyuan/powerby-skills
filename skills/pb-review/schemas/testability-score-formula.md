# Schema: Testability Score Formula

**版本**: 1.0.0
**来源**: pb-review-standard.md §4.1
**引用 Skill**: pb-review, render_testability_scorecard.py

## 定义

| 指标 | 名称 | 权重 | 说明 |
|---|---|---|---|
| M-01 | 功能闭合集合完成率 | 25% | 已建模功能集合的闭合程度 |
| M-02 | 原子功能率 | 10% | 功能是否按单一 entry surface 原子化 |
| M-03 | Oracle 完整率 | 20% | D-17 平均完整度 |
| M-04 | Fixture 完整率 | 15% | D-18 平均完整度 |
| M-05 | 测试追踪完整率 | 10% | Feature→TestCaseGroup 的覆盖程度 |
| M-06 | 规则负向覆盖率 | 10% | Rule→NegativeTest 的覆盖程度 |
| M-07 | 覆盖宣称可信率 | 10% | coverage_claim_allowed=yes 的功能占比 |

## 评估规则

- `score = Σ(指标值 × 权重)`
- 等级：A >= 90, B = 75-89, C = 60-74, D < 60

## 数据结构

```yaml
score:
  metrics:
    M-01: number
    M-02: number
    M-03: number
    M-04: number
    M-05: number
    M-06: number
    M-07: number
  score: number
  grade: A | B | C | D
```

## 示例

```yaml
score:
  metrics:
    M-01: 100
    M-02: 95
    M-03: 80
    M-04: 70
    M-05: 60
    M-06: 50
    M-07: 40
  score: 76
  grade: B
```
