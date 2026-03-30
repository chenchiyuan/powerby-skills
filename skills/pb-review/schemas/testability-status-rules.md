# Schema: Testability Status Rules

**版本**: 1.0.0
**来源**: pb-review-standard.md §2.2
**引用 Skill**: pb-review-feature-reconstructor, pb-review-gap-analyzer

## 定义

| 状态 | 判定条件 | 含义 |
|---|---|---|
| blocked | 缺少业务规则定义 OR 缺少数据对象 Schema OR oracle_completeness < 50 | 还原未达到最小测试化门槛 |
| partial | 不满足 blocked，且 oracle 50-89 或 fixture 50-89 或 test groups 3-4 | 可继续补齐，但不能直接进入完整 TDD |
| test_ready | oracle >= 90 AND fixture >= 90 AND groups >= 5 AND D17-1/D17-9 已定义 | 已达到测试就绪 |

## 评估规则

- 判定必须基于显式证据
- implementation-mapper 可上调状态，但不能删除一阶段证据

## 数据结构

```yaml
testability_status: blocked | partial | test_ready
```

## 示例

```yaml
testability_status: partial
```
