# Schema: D-19 Test Case Groups

**版本**: 1.0.0
**来源**: pb-review-standard.md §3.4
**引用 Skill**: pb-review-feature-reconstructor, pb-review, pb-review-relation-builder

## 定义

| 分组编号 | 分组名称 | 检查内容 |
|---|---|---|
| TG-01 | 正向功能测试 | 主成功路径是否可验证 |
| TG-02 | 参数校验测试 | 非法参数与缺省值行为 |
| TG-03 | 边界值测试 | 空值、极值、非法值边界 |
| TG-04 | 异常路径测试 | 错误码、错误消息、触发条件 |
| TG-05 | 前置条件测试 | 前置状态不满足时的行为 |
| TG-06 | 后置状态测试 | 状态变化与副作用断言 |
| TG-07 | 外部依赖测试 | Mock/Stub/Fake 的交互行为 |
| TG-08 | 回归与覆盖声明测试 | 覆盖边界、未覆盖子能力、回归保护 |

## 评估规则

- `count` 记录当前识别到的测试分组数量
- `groups[*].test_count` 记录该分组下的测试数
- 理想状态至少覆盖 8 个分组

## 数据结构

```yaml
d19_test_groups:
  count: number
  groups:
    - name: string
      test_count: number
      evidence_refs: array
```

## 示例

```yaml
d19_test_groups:
  count: 3
  groups:
    - name: 正向功能测试
      test_count: 5
      evidence_refs: [ev-301]
```
