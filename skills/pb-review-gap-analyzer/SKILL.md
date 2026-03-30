---
name: pb-review-gap-analyzer
description: 当对象、关系和冲突已经齐备，并需要识别需求与实现的差异、缺失对象、链路断点与残留冲突时使用。它必须只基于显式证据输出 gap 和 difference，不能脑补问题。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-gap-analyzer

Use this skill to identify explicit differences and missing links after reconstruction is complete.
Apply it after relation building and feature state generation.
Do not rely on it for proposing fixes or writing the final report narrative.

## Purpose

在既有对象、关系和冲突之上识别真正需要关注的差异与缺口。

## Success criteria

- 输出 `gaps` 和必要的新增 `conflicts`。
- 区分文档有代码无、代码有文档无、对象孤立、链路断点，以及 `missing_feature` / `missing_oracle` / `missing_fixture_contract` / `missing_test_traceability`。
- 结论都能回溯到现有 registry 或证据 ID。
- 缺少必需 registry 时停止，而不是凭空分析。
- 输出 `difference_registry`，并生成 `.review/deliverables/06-gap-analysis.md`。

## Strategy

1. 先看显式差异，再看结构性缺口。
2. 用 feature state、relation coverage、testability_status 与 conflict registry 交叉验证。
3. 对任何“看起来不对”的地方，都先找证据链再下结论。
4. 没证据时保留“不确定”，不要制造 alarm。
5. `06-gap-analysis.md` 的模板化输出交给 `scripts/render_gap_analysis.py`。

## Tools and capability boundaries

- 读取 `context.object_registry`、`context.feature_state_registry`、`context.relation_registry`、`context.conflict_registry`。
- 可做集合对比、状态比对、覆盖率异常检测。
- 在差异和缺口结论确定后，使用 `scripts/render_gap_analysis.py` 负责交付物落盘。
- 不新增对象，不重写上游关系。
- 不负责生成最终报告文本。
- 当前宿主模型必须直接完成 gap 判断，不允许通过脚本把分析外包到后端模型。

## Important facts and constraints

- 此 skill 的 `allow_inference` 为 `false`；差异必须来自显式证据。
- 缺口与冲突都要指明具体上下文，而不是抽象结论。
- 这里输出的是“评审发现”，不是“整改方案”。
- 如果上游 registry 缺失，优先停止并指出缺失环节。
- `references/task-contract.md` 只用于校准输出，不允许当成远程 API contract 使用。
- `difference` 与 `gap` 必须分开表达，不能混写成一句模糊评价。
- 010 升级后，gap 需要显式标注 `gap_severity`，并引用共享严重程度规则。

## Workflow

1. 读取共享协议与现有 registry。
2. 识别 `doc_defined` 但未实现、`code_only` 且无文档、无关系支撑，以及测试化缺口。
3. 将残留冲突按需要升级为评审发现。
4. 输出 `context_writes.difference_registry` 与 gap 汇总。
5. 调用 `scripts/render_gap_analysis.py` 生成 `06-gap-analysis.md` 并更新 `deliverable_manifest`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: array
gaps: array
context_writes: {}
metadata:
  difference_list: array
  summary:
    total_gaps: number
    critical_gaps: number
  deliverables: array
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`../pb-review/schemas/testability-status-rules.md`](../pb-review/schemas/testability-status-rules.md)
- [`../pb-review/schemas/gap-severity-rules.md`](../pb-review/schemas/gap-severity-rules.md)
- [`scripts/render_gap_analysis.py`](./scripts/render_gap_analysis.py)
- [`assets/gap-analysis-template.md`](./assets/gap-analysis-template.md)
- [`references/task-contract.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-gap-analyzer/references/task-contract.md)
- [`references/examples.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-gap-analyzer/references/examples.md)
- [`references/failure-modes.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-gap-analyzer/references/failure-modes.md)
- [`docs/iterations/009-review-framework/spec.md`](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/009-review-framework/spec.md)
- [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)

## Subtask / parallelism guidance

- 可分开做“状态差异检查”和“链路缺口检查”，最后统一汇总。
- 子任务只返回 gap / difference 候选，不直接产出报告结论。

## Examples

**Example 1**  
Input: `feature_state_registry` 中存在 `doc_defined` 功能  
Output: `doc_without_code` difference + corresponding gap

**Example 2**  
Input: 关系图中存在无支撑 Goal  
Output: `missing_relation` gap

## Safety

- 不要在没有 `feature_state_registry` 时继续做需求-实现偏差判断。
- 不要把主观意见伪装成 evidence-driven finding。
- 不要通过任何后端 LLM 客户端执行本 skill。
