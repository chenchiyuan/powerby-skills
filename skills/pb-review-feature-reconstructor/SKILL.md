---
name: pb-review-feature-reconstructor
description: 当评审流程需要从文档、API、代码和测试中还原 Feature、Rule、Boundary，并标注 `doc_defined`、`implemented`、`partial`、`residual` 等功能状态时使用。它负责描述系统表达了什么能力，不负责评价质量高低。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-feature-reconstructor

Use this skill to reconstruct feature-level capabilities, rules, and boundaries.
Apply it after product objects and evidence are available.
Do not rely on it for final gap judgment or subjective quality scoring.

## Purpose

把项目中的功能能力、规则和边界抽取为结构化对象，补充功能状态注册表，并产出符合功能规格定义标准的功能规格卡。

## Success criteria

- 输出 `feature`、`rule`、`boundary` 对象，并带 `evidence_refs`。
- 输出 `feature_spec_registry`，把 Operation 级能力落成结构化功能规格。
- 输出 `feature_state_registry`，区分 `doc_defined`、`implemented`、`partial`、`residual`。
- 在 010 升级后补充 `D-17` / `D-18` / `D-19` / `D-20` 测试化维度，并输出 `testability_status`。
- 支持 `code_only` / `doc_only` / `both` 来源区分。
- 找不到功能来源时返回 `partial`，保留缺口而非强造功能。
- 生成 `.review/deliverables/03-feature-spec-index.md` 与 `.review/deliverables/04-feature-specs/{function_id}.md`。

## Strategy

1. 先读取用户指定产品文档目录命中的需求证据，再主动搜索代码、测试、配置中的实现证据。
2. 明确区分“功能本体”“业务规则”“边界条件”三个层次。
3. 代码可用于保守推断功能，但必须标注 `source: code_only`。
4. 文档声明但代码缺失的功能不要悄悄忽略，应保留为 `doc_defined`。
5. Operation 级功能必须按照 `D-01 ~ D-08` 维度补齐规格，并尽可能补齐 `D-15` / `D-16` / `D-17` / `D-18` / `D-19` / `D-20` 的候选事实；缺失项要显式标成 `partial` 或 gap。
6. `03/04` 交付物渲染是确定性动作，统一交给 `scripts/render_feature_deliverables.py`。

## Tools and capability boundaries

- 读取 `context.object_registry`、`context.current_facts`、`context.evidence_registry`。
- 允许从路由、handler、service、测试案例中识别功能入口与行为。
- 在结构化规格确定后，使用 `scripts/render_feature_deliverables.py` 负责索引和规格卡落盘。
- 不建立 Goal-Feature 关系；那是 `relation-builder` 的职责。
- 不直接输出差异结论；那是 `gap-analyzer` 的职责。
- 当前宿主模型必须直接完成功能还原与状态判断，不允许通过脚本转发到后端 LLM。

## Important facts and constraints

- 功能必须至少有一个文档或代码证据。
- 规则优先来自显式文档，再辅以代码 guard/validator。
- 边界只记录显式前置条件、edge case、failure mode，不做脑补。
- `goal_ref` 可以为空，但不能虚构一个并不存在的 goal。
- `references/task-contract.md` 用来约束判断口径，不是给脚本外包思考用的。
- 不能只交付“功能列表”；Operation 级能力必须交付独立规格卡。
- 功能规格卡必须遵循 `docs/review/feature-specification-standard.md`。
- `runtime_layer` 是运行时职责字段，不替代 `layer`。
- `D-15` / `D-16` 可先产出候选事实，后续由 `dependency-reconstructor` 和 `implementation-mapper` 做收敛与补全。
- `D-17` / `D-18` / `D-19` / `D-20` 的 `defined` 状态必须由显式证据支撑，严禁脑补。

## Workflow

1. 读取共享协议与数据模型。
2. 验证产品对象已存在；如果没有，只能保守提取 `code_only` 功能并记录 gap。
3. 从产品文档/API/代码/测试抽取 Feature，其中代码主动搜索是主输入之一。
4. 从约束性文本和守卫逻辑抽取 Rule。
5. 从前置条件、失败模式与边界描述中抽取 Boundary。
6. 为每个 Operation 级功能生成 `feature_spec_registry` 记录，并补齐 `D-17` ~ `D-20` 字段。
7. 为每个 feature 生成对应的 feature state，并同步写入 `testability_status`。
8. 调用 `scripts/render_feature_deliverables.py` 输出 `03-feature-spec-index.md` 与 `04-feature-specs/*.md`，并更新 `deliverable_manifest`。

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
  features_with_runtime_layer: number
  deliverables: array
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`scripts/render_feature_deliverables.py`](./scripts/render_feature_deliverables.py)
- [`assets/feature-spec-index-template.md`](./assets/feature-spec-index-template.md)
- [`assets/feature-spec-card-template.md`](./assets/feature-spec-card-template.md)
- [`references/task-contract.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-feature-reconstructor/references/task-contract.md)
- [`references/examples.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-feature-reconstructor/references/examples.md)
- [`references/failure-modes.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-feature-reconstructor/references/failure-modes.md)
- [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)
- [`docs/iterations/009-review-framework/architecture.md`](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/009-review-framework/architecture.md)

## Subtask / parallelism guidance

- 可将 Feature / Rule / Boundary 的抽取拆开，但最后必须统一写回 `feature_state_registry`。
- 规格卡模板与索引模板应由主会话按需读取，不要在子任务里各自发明格式。
- 子任务不要各自定义不同的功能状态枚举。

## Examples

**Example 1**  
Input: 文档 + 测试 + 路由证据  
Output: Feature / Rule / Boundary + `feature_state_registry`

**Example 2**  
Input: 只有代码证据  
Output: `code_only` Feature，并记录缺少文档来源

## Safety

- 不要把技术实现细节直接写成用户可感知功能，除非有文档或测试支撑。
- 不要把一个大型功能拆得过碎，导致后续关系构建失真。
- 不要通过任何 HTTP 推理客户端执行本 skill。
- 不要以“汇总表”替代功能规格卡。
- 不要用本地硬编码规则表给 Feature 强行填依赖或实现映射。
