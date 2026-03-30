# Schema: D-17 Test Oracle

**版本**: 1.0.0
**来源**: pb-review-standard.md §3.2
**引用 Skill**: pb-review-feature-reconstructor, pb-review-gap-analyzer, pb-review

## 定义

| 子项编号 | 子项名称 | 检查内容 |
|---|---|---|
| D17-1 | 成功输出 Schema | 完整的 JSON/CSV/HTML 结构定义 |
| D17-2 | 字段级类型 | 每个字段的数据类型和约束 |
| D17-3 | 必填字段 | 哪些字段必须存在 |
| D17-4 | 排序规则 | 输出结果的排序逻辑 |
| D17-5 | 空结果规则 | 空结果的格式和触发条件 |
| D17-6 | 错误码 Contract | 每个异常的错误码、触发条件、消息 |
| D17-7 | 文件输出 Contract | 文件格式、编码、列顺序、表头 |
| D17-8 | 状态变化 Contract | 执行后系统状态的变化 |
| D17-9 | 业务规则定义 | 所有计算逻辑的公式和规则 |

## 评估规则

- 完整度 = 已定义子项数 / 适用子项数 × 100%
- `not_applicable` 不计入分母
- 每个 `defined` 子项必须携带 `evidence_refs`
- 缺失项必须显式标记为 `missing`

## 数据结构

```yaml
d17_oracle:
  completeness: number
  sub_items:
    - id: D17-1 ~ D17-9
      name: string
      status: defined | missing | not_applicable
      evidence_refs: array | null
```

## 示例

```yaml
d17_oracle:
  completeness: 67
  sub_items:
    - id: D17-1
      name: 成功输出 Schema
      status: defined
      evidence_refs: [ev-101]
```
