# Schema: D-18 Fixture Contract

**版本**: 1.0.0
**来源**: pb-review-standard.md §3.3
**引用 Skill**: pb-review-feature-reconstructor, pb-review-dependency-reconstructor, pb-review

## 定义

| 子项编号 | 子项名称 | 检查内容 |
|---|---|---|
| D18-1 | 最小数据集 | 功能正常运行所需的最小测试数据 |
| D18-2 | 时间冻结要求 | 是否需要冻结时间及冻结时间点 |
| D18-3 | 外部依赖 Mock 策略 | 哪些外部依赖需要 mock 及返回值 |
| D18-4 | 数据库初始状态 | 测试前数据库应处于什么状态 |
| D18-5 | 前置缓存状态 | 测试前缓存应处于什么状态 |
| D18-6 | 可复用 Fixture 名称 | 可复用的 fixture 函数名 |

## 评估规则

- 完整度 = 已定义子项数 / 适用子项数 × 100%
- 每个 `defined` 子项必须有直接测试证据
- 缺少测试文件时，完整度记为 0

## 数据结构

```yaml
d18_fixture:
  completeness: number
  sub_items:
    - id: D18-1 ~ D18-6
      name: string
      status: defined | missing | not_applicable
      evidence_refs: array | null
```

## 示例

```yaml
d18_fixture:
  completeness: 50
  sub_items:
    - id: D18-3
      name: 外部依赖 Mock 策略
      status: defined
      evidence_refs: [ev-221]
```
