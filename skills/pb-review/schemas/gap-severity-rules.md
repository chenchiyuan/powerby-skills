# Schema: Gap Severity Rules

**版本**: 1.0.0
**来源**: pb-review-standard.md §2.5
**引用 Skill**: pb-review-gap-analyzer

## 定义

| 严重程度 | 判定规则 | 影响 |
|---|---|---|
| Critical | 无法判断功能是否正确 OR 无法编写任何测试 OR 阻塞整个功能测试化 | 必须优先修复 |
| Major | 无法完整生成测试组 OR 测试不稳定 OR 影响覆盖率 >= 20% | 阻碍大部分测试化 |
| Minor | 可以写测试但稳定性不足 OR 影响覆盖率 < 20% | 不阻塞主路径 |

## 评估规则

- `missing_oracle` 可为 Critical 或 Major
- `missing_fixture_contract` 默认 Major
- `missing_test_traceability` 默认 Major
- 所有 gap 必须附带 `context` 和 `evidence_refs`

## 数据结构

```yaml
gap:
  gap_type: string
  gap_severity: Critical | Major | Minor
```

## 示例

```yaml
gap:
  gap_type: missing_oracle
  gap_severity: Critical
```
