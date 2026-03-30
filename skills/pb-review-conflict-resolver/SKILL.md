---
name: pb-review-conflict-resolver
description: 当评审流程已经有 `evidence_registry`，并需要按时间与来源优先级决议当前事实、保留文档与代码冲突、产出 `current_facts` 时使用。它负责做证据优先级判断，不负责裁决“谁应该是对的”。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-conflict-resolver

Use this skill to determine which evidence is currently effective and which conflicts must remain visible.
Apply it after evidence collection and before product or feature reconstruction.
Do not rely on it for making product decisions or resolving organizational disputes.

## Purpose

在全量证据中识别“哪些事实当前可采用，哪些冲突必须显式保留”，为下游还原步骤提供可信输入。

## Success criteria

- 按架构规定应用优先级规则，而不是临时发明规则。
- 产出 `conflicts` 与 `context_writes.current_facts`。
- 无法决议时使用 `unresolved` 或 `preserved`，不做强行和解。
- 不评价业务对错，只处理证据优先级。

## Strategy

1. 先验证所有候选证据都具备 `timestamp` 与 `source_type`。
2. 按 Git 时间戳排序，同源多版本保留最新。
3. 文档与代码冲突时，优先把代码视为实现层现状，同时显式保留冲突记录。
4. 如果规则覆盖不到，就把不确定性暴露出来，不隐藏。

## Tools and capability boundaries

- 读取 `context.evidence_registry`。
- 允许使用排序、分组、时间比较与内容对照。
- 不生成产品对象、功能对象、关系或最终报告。
- 不把 commit/issue 当作主事实，只作为背景辅助。

## Important facts and constraints

- 产品层规则：新文档优先于旧文档。
- 实现层规则：代码优先于旧文档。
- 时间相同、优先级相同但内容矛盾时，必须标为 `unresolved`。
- 下游 skill 只能读 `current_facts`，不能跳过这里直接从原始证据自行挑选“喜欢的事实”。

## Workflow

1. 读取 `../pb-review/references/review-contract.md` 与 `../pb-review/references/data-model.md`。
2. 校验 `context.evidence_registry` 非空。
3. 对证据按 `source_path`、`source_type`、`timestamp` 分组与排序。
4. 识别：
   - 新旧文档冲突
   - 文档与代码冲突
   - 无法决议的同级冲突
5. 输出 `conflicts` 与 `current_facts.product_facts` / `current_facts.implementation_facts`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: array
gaps: []
context_writes:
  current_facts:
    product_facts: array
    implementation_facts: array
metadata:
  priority_rules_applied: array
  unresolved_conflicts: number
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`docs/iterations/009-review-framework/spec.md`](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/009-review-framework/spec.md)

## Subtask / parallelism guidance

- 可先按 `source_path` 分组，再统一做优先级决议。
- 不要把冲突判断拆成多个不共享规则的子流程。

## Examples

**Example 1**  
Input: 同一路径存在多份不同时序文档证据  
Output: 选择最新版本进入 `current_facts`，旧版本进入 `conflicts`

**Example 2**  
Input: 文档和代码证据同时存在  
Output: 产品事实走文档，实施事实走代码，冲突保留

## Safety

- 不要把“没有足够证据”误写成“没有冲突”。
- 不要删除冲突记录来追求看起来更整洁的输出。
