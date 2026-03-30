---
name: pb-review-architecture-builder
description: 当评审流程已经有 `feature_spec_registry`、`dependency_registry` 和 `implementation_registry`，并需要产出业务域与运行层视图时使用。它负责把已还原事实编排成架构文档，而不是重做需求或实现判断。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-architecture-builder

Use this skill to build a layered architecture view from reconstructed review artifacts.
Apply it after feature, dependency, and implementation reconstruction are ready.
Do not rely on it for inventing architectural layers that the evidence does not support.

## Purpose

把功能、依赖和实现映射编排成业务域划分、运行层分层和关键编排链路的架构交付物。

## Success criteria

- 输出 `architecture_registry`。
- 生成 `.review/deliverables/08-architecture-layered.md`。
- 清晰区分 `layer` 与 `runtime_layer`。
- 关键路径、跨域依赖、运行层职责都有证据锚点。

## Strategy

1. 先按 `domain_code` 聚合，再按 `runtime_layer` 分层。
2. 优先呈现高价值链路，而不是追求穷举所有实现细节。
3. 架构文档只是编排已知事实，不重新裁定功能真假。

## Tools and capability boundaries

- 读取 `context.feature_spec_registry`、`context.dependency_registry`、`context.implementation_registry`。
- 在判断完成后，使用 `scripts/render_architecture_deliverable.py` 落盘。
- 不新增功能对象，不做 gap 严重度评分。

## Workflow

1. 读取共享协议、数据模型和上游 registry。
2. 聚合业务域、运行层和关键链路。
3. 输出 `context_writes.architecture_registry`。
4. 调用 `scripts/render_architecture_deliverable.py` 生成 `08-architecture-layered.md`。
5. 更新 `deliverable_manifest`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: array
context_writes:
  architecture_registry: object
metadata:
  runtime_layers: number
  domains: number
  critical_paths: number
  deliverables: array
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`scripts/render_architecture_deliverable.py`](./scripts/render_architecture_deliverable.py)
- [`assets/architecture-layered-template.md`](./assets/architecture-layered-template.md)

## Safety

- 不要把运行层分层和功能层级混写成同一个字段。
- 不要用空泛术语掩盖缺失证据。
