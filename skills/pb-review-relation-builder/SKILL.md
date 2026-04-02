---
name: pb-review-relation-builder
description: |
  当产品对象、功能对象、依赖记录和实现映射都已存在，并需要建立 Goal->Feature、Rule->Feature、Feature->Feature、Feature->Implementation 的追踪关系、识别孤立对象并计算覆盖率时使用。
  它负责建立有证据支撑的链路，不负责发明缺失的 goal 或 feature。
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

- 输出 supports、constrains、depends_on、implemented_by 等关系记录。
- 列出无下游支撑的 goal 与无上游归属的 feature。
- 提供 coverage 统计。
- 允许 inferred 关系但必须显式标注置信度。
- 生成 traceability_matrix 与 `05-traceability-matrix.md`。

## Strategy

### 设计哲学

1. **显式优先** -- 优先建立有直接文本证据的显式关系。
2. **保守推断** -- 只在对象语义高度匹配且证据不足以完全显式时建立 inferred 关系。
3. **孤立即 gap** -- 无法合理建立链路的对象保留为孤立对象 gap。
4. **覆盖率是信号** -- 覆盖率是评审信号，不是质量分数；链路满足统计需要即停止。
5. **渲染下沉** -- 追踪矩阵 Markdown 交给 renderer script。

## Tools and capability boundaries

- 读取 `context.object_registry`、`context.dependency_registry`、`context.implementation_registry` 与相关证据。
- 允许对象聚类、关键词映射和覆盖率统计。
- 使用 `scripts/render_traceability_matrix.py` 落盘标准矩阵。
- 不修改 feature state，不输出最终差异判断。
- 不把"语义相似"误当作必然关系。
- 不允许交给后端 LLM 代理。

## Important facts and constraints

- Goal->Feature 使用 supports。
- Rule->Feature 使用 constrains。
- Feature->Feature 使用 depends_on。
- Feature->Implementation 使用 implemented_by。
- 无法建立关系比建立错误关系更可接受。
- 追踪矩阵是一级交付物，不能只把关系散落在 relation_registry 中。

## Workflow

1. 读取共享协议、数据模型与现有对象 registry。
2. 为 Goal 寻找支撑 Feature，为 Rule 寻找约束 Feature。
3. 从 dependency_registry 与 implementation_registry 归并依赖和实现关系。
4. 记录无关系的 Goal/Feature 为 gap。
5. 计算 goal_coverage_rate、feature_traceability_rate。
6. 输出 traceability_matrix。
7. 调用 `scripts/render_traceability_matrix.py` 生成 `05-traceability-matrix.md`。
8. 更新 deliverable_manifest。

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
  deliverables: array
errors: []
```

## Resources

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/references/deliverable-standard.md` -- 渲染时加载
- `scripts/render_traceability_matrix.py` -- 渲染阶段执行
- `references/task-contract.md` -- 判断边界校准
- `references/examples.md` -- 需要参考案例时加载
- `references/failure-modes.md` -- 遇到异常时加载

## Subtask / parallelism guidance

- 可先构建 Goal->Feature，再构建 Rule->Feature，但最终统一 coverage 统计。
- 子任务目标是提出候选关系，不直接篡改 registry。

## Examples

**Example 1**
Input: Goals + Features
Output: supports 关系和 coverage

**Example 2**
Input: Rules + Features
Output: constrains 关系与孤立对象 gap

## Safety

- 不要为提高覆盖率而强行连线。
- 不要把 inferred 关系写成 explicit。
- 不要把本 skill 包装成 HTTP 调用链。
- 不要用静态枚举表硬编码依赖或实现归属。
