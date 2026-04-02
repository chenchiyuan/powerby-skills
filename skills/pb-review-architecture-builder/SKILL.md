---
name: pb-review-architecture-builder
description: |
  当评审流程已经有 feature_spec_registry、dependency_registry 和 implementation_registry，并需要产出业务域与运行层视图时使用。
  它负责把已还原事实编排成架构文档，不负责重做需求或实现判断。不适用于新增功能或 gap 评分。
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

- 输出 architecture_registry。
- 生成 `08-architecture-layered.md`。
- 清晰区分 layer 与 runtime_layer。
- 关键路径、跨域依赖、运行层职责都有证据锚点。

## Strategy

### 设计哲学

1. **聚合而非发明** -- 架构文档只编排已知事实，不重新裁定功能真假。
2. **域先层后** -- 先按 domain_code 聚合，再按 runtime_layer 分层。
3. **高价值链路优先** -- 优先呈现高价值链路，不追求穷举所有实现细节。
4. **层级分明** -- layer 是功能层级，runtime_layer 是运行时职责，不混写。
5. **渲染下沉** -- 架构文档交给 renderer script 落盘。

## Tools and capability boundaries

- 读取 `context.feature_spec_registry`、`context.dependency_registry`、`context.implementation_registry`。
- 使用 `scripts/render_architecture_deliverable.py` 落盘。
- 不新增功能对象，不做 gap 严重度评分。

## Important facts and constraints

- 架构视图是编排产物，不是分析产物。
- 缺少上游 registry 时应返回 failed 而不是空架构。

## Workflow

1. 读取共享协议、数据模型和上游 registry。
2. 聚合业务域、运行层和关键链路。
3. 输出 `context_writes.architecture_registry`。
4. 调用 `scripts/render_architecture_deliverable.py` 生成 `08-architecture-layered.md`。
5. 更新 deliverable_manifest。

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

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/references/deliverable-standard.md` -- 渲染时加载
- `scripts/render_architecture_deliverable.py` -- 渲染阶段执行

## Safety

- 不要把运行层分层和功能层级混写成同一个字段。
- 不要用空泛术语掩盖缺失证据。
