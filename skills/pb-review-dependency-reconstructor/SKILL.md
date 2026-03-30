---
name: pb-review-dependency-reconstructor
description: 当评审流程已经有 `feature_spec_registry`，并需要还原 Feature→Feature、Feature→External、Feature→Data Object 的依赖关系，产出 `dependency_registry` 与依赖矩阵时使用。它负责描述能力之间如何衔接，不负责发明不存在的功能。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-dependency-reconstructor

Use this skill to reconstruct dependency relationships between features, external systems, and data objects.
Apply it after feature specs are available.
Do not rely on it for hardcoded rule matching or for gap severity judgment.

## Purpose

把功能规格中的前置条件、后置链路、副作用和显式调用关系还原为结构化依赖记录，并输出依赖矩阵交付物。

## Success criteria

- 输出 `dependency_registry`，每条依赖都带 `dependency_type`、`evidence_refs`、`confidence`。
- 依赖至少覆盖 `feature`、`external_system`、`data_object` 三类目标。
- 依赖判断不足时返回 `partial`，而不是用本地规则表硬补。
- 生成 `.review/deliverables/09-dependency-matrix.md`。

## Strategy

1. 优先采用显式文档、测试、命令编排和服务调用证据。
2. 只有在上下文高度一致时才建立 `inferred` 依赖，并保留置信度。
3. 缺失依赖比错误依赖更可接受。
4. Markdown 依赖矩阵交给 renderer script，抽象判断由当前宿主模型直接完成。

## Tools and capability boundaries

- 读取 `context.feature_spec_registry`、`context.current_facts`、`context.evidence_registry`。
- 允许从规格卡候选事实、代码入口、测试链路中判断依赖。
- 在依赖结果确定后，使用 `scripts/render_dependency_deliverable.py` 落盘。
- 不修改产品对象，不做最终差异裁定。
- 不允许通过本地硬编码枚举来替代依赖判断。

## Important facts and constraints

- `dependency_type` 推荐使用 `data`、`trigger`、`orchestration`、`external_system`、`shared_state`。
- 依赖的目标必须可回溯到 `function_id`、`external_id` 或 `data_object_id`。
- 依赖矩阵是一级交付物，不能只把结果散落在 JSON 里。

## Workflow

1. 读取共享协议、数据模型与现有 `feature_spec_registry`。
2. 判断每个功能的上游依赖、下游被依赖、外部依赖、数据对象依赖。
3. 输出 `context_writes.dependency_registry`。
4. 必要时回填 `feature_spec_registry[*].dependencies`。
5. 调用 `scripts/render_dependency_deliverable.py` 生成 `09-dependency-matrix.md`。
6. 更新 `deliverable_manifest`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: array
context_writes:
  dependency_registry: array
  feature_spec_registry: array
metadata:
  total_dependencies: number
  feature_dependencies: number
  external_dependencies: number
  data_dependencies: number
  deliverables: array
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`scripts/render_dependency_deliverable.py`](./scripts/render_dependency_deliverable.py)
- [`assets/dependency-matrix-template.md`](./assets/dependency-matrix-template.md)
- [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)

## Safety

- 不要把“同一目录下的文件”当成依赖证据。
- 不要把顺序相邻的命令默认判定为存在依赖。
- 不要用本地规则表替代宿主模型的依赖判断。
