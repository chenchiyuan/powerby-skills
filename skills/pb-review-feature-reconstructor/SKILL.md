---
name: pb-review-feature-reconstructor
description: |
  当评审流程需要从文档、API、代码和测试中还原 Feature、Rule、Boundary，并标注 doc_defined、implemented、partial、residual 等功能状态时使用。
  它负责描述系统表达了什么能力，不负责评价质量高低。不适用于 gap 判断或主观评分。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-feature-reconstructor

Use this skill to reconstruct feature-level capabilities, rules, and boundaries.
Apply it after product objects and evidence are available.
Do not rely on it for final gap judgment or subjective quality scoring.

## Purpose

把项目中的功能能力、规则和边界抽取为结构化对象，补充功能状态注册表，并产出符合功能规格定义标准的规格卡。

## Success criteria

- 输出 feature、rule、boundary 对象并带 evidence_refs。
- 输出 feature_spec_registry，把 Operation 级能力落成结构化功能规格。
- 输出 feature_state_registry，区分 doc_defined、implemented、partial、residual。
- 补充 D-17 ~ D-20 测试化维度和 testability_status。
- 支持 code_only / doc_only / both 来源区分。
- 生成 `03-feature-spec-index.md` 与 `04-feature-specs/{function_id}.md`。

## Strategy

### 设计哲学

1. **双向搜索** -- 先读需求文档证据，再主动搜索代码/测试/配置中的实现证据。
2. **三层分明** -- 功能本体、业务规则、边界条件是三个不同层次，不混为一谈。
3. **保守推断** -- 代码可推断功能但必须标注 source: code_only；文档声明但代码缺失保留为 doc_defined。
4. **规格化交付** -- Operation 级功能必须交付独立规格卡（D-01~D-08），不能只交付"功能列表"。
5. **渲染下沉** -- 交付物渲染统一交给 renderer script。

## Tools and capability boundaries

- 读取 `context.object_registry`、`context.current_facts`、`context.evidence_registry`。
- 允许从路由、handler、service、测试案例中识别功能入口与行为。
- 使用 `scripts/render_feature_deliverables.py` 负责索引和规格卡落盘。
- 不建立 Goal-Feature 关系（relation-builder 的职责）。
- 不输出差异结论（gap-analyzer 的职责）。
- 不允许通过脚本转发到后端 LLM。

## Important facts and constraints

- 功能必须至少有一个文档或代码证据。
- 规则优先来自显式文档，再辅以代码 guard/validator。
- goal_ref 可为空，但不能虚构不存在的 goal。
- D-15/D-16 先产出候选事实，后续由 dependency-reconstructor 和 implementation-mapper 收敛。
- D-17~D-20 的 defined 状态必须由显式证据支撑。
- 功能规格卡必须遵循 `docs/review/feature-specification-standard.md`。

## Workflow

1. 读取共享协议与数据模型。
2. 验证产品对象已存在；若无，保守提取 code_only 功能并记录 gap。
3. 从文档/API/代码/测试抽取 Feature。
4. 抽取 Rule 和 Boundary。
5. 为每个 Operation 级功能生成 feature_spec_registry 记录。
6. 为每个 feature 生成 feature state 和 testability_status。
7. 调用 `scripts/render_feature_deliverables.py` 输出 03/04 交付物。
8. 更新 deliverable_manifest。

## Output format

```yaml
status: success | partial | failed
objects: array
relations: []
conflicts: []
gaps: array
context_writes:
  feature_spec_registry: array
  feature_state_registry: array
metadata:
  total_features: number
  total_rules: number
  total_boundaries: number
  code_only_features: number
  doc_only_features: number
  deliverables: array
errors: []
```

## Resources

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/references/deliverable-standard.md` -- 渲染时加载
- `scripts/render_feature_deliverables.py` -- 渲染阶段执行
- `references/task-contract.md` -- 判断口径校准
- `references/examples.md` -- 需要参考案例时加载
- `references/failure-modes.md` -- 遇到异常时加载

## Subtask / parallelism guidance

- 可将 Feature / Rule / Boundary 的抽取拆开，但最后统一写回 feature_state_registry。
- 子任务不要各自定义不同的功能状态枚举。

## Examples

**Example 1**
Input: 文档 + 测试 + 路由证据
Output: Feature / Rule / Boundary + feature_state_registry

**Example 2**
Input: 只有代码证据
Output: code_only Feature，记录缺少文档来源

## Safety

- 不要把技术实现细节直接写成用户可感知功能，除非有文档或测试支撑。
- 不要把一个大型功能拆得过碎导致关系构建失真。
- 不要通过任何 HTTP 推理客户端执行本 skill。
- 不要以"汇总表"替代功能规格卡。
