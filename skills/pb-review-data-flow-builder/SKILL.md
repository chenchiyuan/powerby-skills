---
name: pb-review-data-flow-builder
description: |
  当评审流程已经有 feature_spec_registry、dependency_registry 和模型/存储相关证据，并需要还原数据对象的生产者、消费者和流向时使用。
  它负责描述数据如何在系统里流动，不负责发明不存在的数据模型。不适用于 gap 裁决或产品目标重写。
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

- 输出 data_flow_registry。
- 生成 `10-data-flow.md`。
- 数据对象、生产者和消费者都有证据锚点。
- 证据不足时返回 partial，不臆造内部数据流。

## Strategy

### 设计哲学

1. **规格驱动** -- 从 D-03（输入）、D-07（后置）、D-08（副作用）和实现映射中提取数据读写事实。
2. **核心链路优先** -- 优先还原关键业务链路中的核心数据对象，不追求穷举。
3. **事实判断在前** -- 数据流事实判断由当前宿主模型完成，Mermaid 只是展示层。
4. **存储不等于数据流** -- 日志输出不等于持久化数据流，需区分。
5. **渲染下沉** -- 数据流文档交给 renderer script 落盘。

## Tools and capability boundaries

- 读取 `context.feature_spec_registry`、`context.dependency_registry`、`context.implementation_registry`、`context.evidence_registry`。
- 使用 `scripts/render_data_flow_deliverable.py` 落盘。
- 不做 gap 裁决，不重写产品目标。

## Important facts and constraints

- 数据对象必须有证据支撑，不能因为"看起来像表名"就认定为数据对象。
- 缺少上游 registry 时应返回 failed。

## Workflow

1. 读取共享协议、数据模型与上游 registry。
2. 识别数据对象、生产者、消费者、存储位置、生命周期。
3. 归并关键流向链路。
4. 输出 `context_writes.data_flow_registry`。
5. 调用 `scripts/render_data_flow_deliverable.py` 生成 `10-data-flow.md`。
6. 更新 deliverable_manifest。

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

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/references/deliverable-standard.md` -- 渲染时加载
- `scripts/render_data_flow_deliverable.py` -- 渲染阶段执行

## Safety

- 不要因为"看起来像表名"就把任何字符串认定为数据对象。
- 不要把日志输出等同于持久化数据流。
