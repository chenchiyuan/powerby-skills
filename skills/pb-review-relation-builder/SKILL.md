---
name: pb-review-relation-builder
description: 当产品对象、功能对象、依赖记录和实现映射都已存在，并需要建立 Goal→Feature、Rule→Feature、Feature→Feature、Feature→Implementation 的追踪关系、识别孤立对象并计算覆盖率时使用。它负责建立有证据支撑的链路，而不是强行把所有对象都连起来。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-relation-builder

Use this skill to connect reconstructed objects into traceable chains.
Apply it when product and feature objects are both present.
Do not rely on it for inventing missing goals or features.

## Purpose

把产品层、功能层、依赖层和实现映射层连接成可追踪链路，为覆盖率统计和差异识别提供基础。

## Success criteria

- 输出 `supports`、`constrains`、`depends_on`、`implemented_by` 等关系记录。
- 明确列出没有下游支撑的 goal 与没有上游归属的 feature。
- 提供 coverage 统计，而不是只给零散链接。
- 允许 `inferred` 关系，但必须显式标注置信度。
- 生成 `traceability_matrix` 结构化结果与 `.review/deliverables/05-traceability-matrix.md`。

## Strategy

1. 优先建立有直接文本证据的显式关系。
2. 只有在对象语义高度匹配且证据不足以完全显式时，才建立 `inferred` 关系。
3. 对于无法合理建立的链路，保留为孤立对象 gap。
4. 链路满足覆盖统计需要即可停止，不追求“图一定满”。
5. 追踪矩阵 Markdown 是固定模板输出，交给 `scripts/render_traceability_matrix.py`。

## Tools and capability boundaries

- 读取 `context.object_registry`、`context.dependency_registry`、`context.implementation_registry` 与相关证据。
- 允许做对象聚类、关键词映射和覆盖率统计。
- 在关系结果确定后，使用 `scripts/render_traceability_matrix.py` 负责标准矩阵落盘。
- 不修改 feature state，不输出最终差异判断。
- 不把“语义相似”误当作必然关系。
- 当前宿主模型必须直接完成关系判断，不允许交给后端 LLM 代理。

## Important facts and constraints

- Goal→Feature 使用 `supports`。
- Rule→Feature 使用 `constrains`。
- Feature→Feature 使用 `depends_on`。
- Feature→Implementation 使用 `implemented_by`。
- 无法建立关系比建立错误关系更可接受。
- 覆盖率是评审信号，不是质量分数。
- `references/task-contract.md` 是判断边界，不是远程推理协议。
- 追踪矩阵是一级交付物，不能只把关系散落在 `relation_registry` 中。

## Workflow

1. 读取共享协议、数据模型与现有对象 registry。
2. 为 Goal 寻找支撑 Feature，为 Rule 寻找约束 Feature。
3. 从 `dependency_registry` 与 `implementation_registry` 归并 Feature 依赖关系和实现映射关系。
4. 记录没有关系的 Goal/Feature 为 gap。
5. 计算 `goal_coverage_rate`、`feature_traceability_rate` 与 `dependency_traceability_rate`。
6. 输出 `context_writes.traceability_matrix`。
7. 调用 `scripts/render_traceability_matrix.py` 生成 `05-traceability-matrix.md`。
8. 更新 `deliverable_manifest`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: array
conflicts: []
gaps: array
context_writes: {}
metadata:
  traceability_matrix:
    goals_with_features: array
    goals_without_features: array
    features_with_goals: array
    features_without_goals: array
  coverage_stats:
    goal_coverage_rate: number
    feature_traceability_rate: number
    dependency_traceability_rate: number
  deliverables: array
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`scripts/render_traceability_matrix.py`](./scripts/render_traceability_matrix.py)
- [`assets/traceability-matrix-template.md`](./assets/traceability-matrix-template.md)
- [`references/task-contract.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-relation-builder/references/task-contract.md)
- [`references/examples.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-relation-builder/references/examples.md)
- [`references/failure-modes.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-relation-builder/references/failure-modes.md)
- [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)

## Subtask / parallelism guidance

- 可先构建 Goal→Feature，再构建 Rule→Feature，但最终要统一 coverage 统计。
- 子任务目标是提出候选关系，不是直接篡改 registry。

## Examples

**Example 1**  
Input: Goals + Features  
Output: `supports` 关系和 coverage

**Example 2**  
Input: Rules + Features  
Output: `constrains` 关系与孤立对象 gap

## Safety

- 不要为了提高覆盖率而强行连线。
- 不要把 `inferred` 关系写成 `explicit`。
- 不要把本 skill 包装成 HTTP 调用链。
- 不要用静态枚举表硬编码 Feature 依赖或实现归属。
