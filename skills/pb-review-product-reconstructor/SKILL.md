---
name: pb-review-product-reconstructor
description: 当评审流程已经有 `current_facts`，并需要从用户指定产品文档目录命中的证据中还原 Goal、Role、Scenario、Constraint、Non-goal 时使用。它只还原需求侧世界，不证明实现已经满足这些定义。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-product-reconstructor

Use this skill to reconstruct product-side intent into structured objects.
Apply it after `current_facts` is available and before feature extraction.
Do not rely on it for implementation truth or architecture decomposition.

## Purpose

把产品证据还原成结构化产品对象，为功能与关系分析提供上游锚点。

## Success criteria

- 输出 `goal`、`role`、`scenario`、`constraint`、`non_goal` 对象时都带 `evidence_refs`。
- 无产品文档时返回 `partial`，并记录 `missing_evidence` gap。
- 只处理 `current_facts.product_facts` 指向的产品文档证据，不对全仓库文档做兜底回退。
- 不把代码行为直接等同于产品目标。
- 同步生成 `.review/deliverables/02-product-catalog.md`，而不是只把对象留在 registry 里。

## Strategy

1. 只读取 `current_facts.product_facts` 指向的文档证据。
2. 先提取显式目标、角色、场景，再考虑约束与非目标。
3. 找不到证据就留空并记录 gap，不创造“合理猜测”。
4. 如果用户希望某份 README/Wiki 参与产品还原，应通过 `product_docs_dir` 把它纳入产品文档目录。
5. Markdown 目录渲染是确定性动作，交给 `scripts/render_catalog.py`；对象判断本身必须由当前会话完成。

## Tools and capability boundaries

- 读取 `context.evidence_registry` 与 `context.current_facts`。
- 允许基于文本结构做抽取与归类。
- 在对象抽取完成后，使用 `scripts/render_catalog.py` 把结构化结果落盘为标准交付物。
- 不生成功能对象、关系对象或实现差异结论。
- 不把 inferred 对象提升为 explicit。
- 当前宿主模型必须直接完成判断，不允许再调用任何后端 LLM 客户端或 HTTP 推理脚本。

## Important facts and constraints

- `required_sources` 以 `doc` 为主；未提供产品文档目录或目录未命中时，必须返回空结果并记录 gap。
- 任何产品对象都必须至少有一个 `evidence_ref`。
- “无证据时不生成对象”比“生成一个看起来合理的对象”更重要。
- 此 skill 只服务 V1 产品层，不负责 V2 架构层还原。
- `references/task-contract.md` 是判断准绳，但执行者必须是当前 Codex/Claude 会话本身。
- 产品对象目录是必备交付物，不允许把 Goal / Role / Scenario 仅埋在最终报告里。

## Workflow

1. 读取共享协议与数据模型资源。
2. 验证 `context.current_facts` 存在。
3. 从产品证据中提取 Goal、Role、Scenario。
4. 补充 Constraint 与 Non-goal。
5. 先产出结构化 `objects/gaps` 结果。
6. 调用 `scripts/render_catalog.py` 生成 `02-product-catalog.md` 并更新 `deliverable_manifest`。
7. 无产品文档时返回空 Catalog + gap，而不是失败整个流程。

## Output format

```yaml
status: success | partial | failed
objects: array
relations: []
conflicts: []
gaps: array
context_writes: {}
metadata:
  total_goals: number
  total_roles: number
  total_scenarios: number
  inference_count: number
  deliverables: array
errors: []
```

## Resources

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`scripts/render_catalog.py`](./scripts/render_catalog.py)
- [`assets/product-catalog-template.md`](./assets/product-catalog-template.md)
- [`references/task-contract.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-product-reconstructor/references/task-contract.md)
- [`references/examples.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-product-reconstructor/references/examples.md)
- [`references/failure-modes.md`](/Users/chenchiyuan/projects/powerby-skills/skills/pb-review-product-reconstructor/references/failure-modes.md)
- [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)
- [`docs/iterations/009-review-framework/spec.md`](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/009-review-framework/spec.md)

## Subtask / parallelism guidance

- 可按证据来源拆分：PRD / README / Wiki 分开抽取，再统一去重。
- 子任务不得把 inferred 内容升级为 explicit。

## Examples

**Example 1**  
Input: 用户指定产品文档目录中的 PRD + Wiki  
Output: Goal / Role / Scenario / Constraint / Non-goal

**Example 2**  
Input: 未提供 `product_docs_dir`，或目录下没有任何产品文档  
Output: partial + 空对象列表 + `missing_evidence` gap

## Safety

- 不要从代码实现逆推出产品愿景。
- 不要绕过 `current_facts.product_facts` 直接扫描全仓库文档。
- 不要把本 skill 包装成脚本后再转发给外部 LLM 服务。
