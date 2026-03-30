---
name: pb-review-data-flow-builder
description: 当评审流程已经有 `feature_spec_registry`、`dependency_registry` 和模型/存储相关证据，并需要还原数据对象的生产者、消费者和流向时使用。它负责描述数据如何在系统里流动，而不是发明不存在的数据模型。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-data-flow-builder

Use this skill to reconstruct data flows across the reviewed system.
Apply it after feature specs and dependencies are available.
Do not rely on it for reverse-engineering every hidden storage detail when the evidence is insufficient.

## Purpose

把数据对象、生产者、消费者、存储位置、生命周期和关键流向链路编排成结构化数据流交付物。

## Success criteria

- 输出 `data_flow_registry`。
- 生成 `.review/deliverables/10-data-flow.md`。
- 数据对象、生产者和消费者都有证据锚点。
- 证据不足时返回 `partial`，不臆造内部数据流。

## Strategy

1. 从 `D-03`、`D-07`、`D-08` 和实现映射中提取数据读写事实。
2. 优先还原关键业务链路中的核心数据对象。
3. Mermaid 只是展示层，数据流事实判断由当前宿主模型完成。

## Tools and capability boundaries

- 读取 `context.feature_spec_registry`、`context.dependency_registry`、`context.implementation_registry`、`context.evidence_registry`。
- 在判断完成后，使用 `scripts/render_data_flow_deliverable.py` 落盘。
- 不做 gap 裁决，不重写产品目标。

## Workflow

1. 读取共享协议、数据模型与上游 registry。
2. 识别数据对象、生产者、消费者、存储位置、生命周期。
3. 归并关键流向链路。
4. 输出 `context_writes.data_flow_registry`。
5. 调用 `scripts/render_data_flow_deliverable.py` 生成 `10-data-flow.md`。
6. 更新 `deliverable_manifest`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: array
context_writes:
  data_flow_registry: object
metadata:
  data_objects: number
  flow_paths: number
  deliverables: array
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`scripts/render_data_flow_deliverable.py`](./scripts/render_data_flow_deliverable.py)
- [`assets/data-flow-template.md`](./assets/data-flow-template.md)

## Safety

- 不要因为“看起来像表名”就把任何字符串认定为数据对象。
- 不要把日志输出等同于持久化数据流。
