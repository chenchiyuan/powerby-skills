---
name: pb-review-product-reconstructor
description: |
  当评审流程已经有 current_facts，并需要从用户指定产品文档目录命中的证据中还原 Goal、Role、Scenario、Constraint、Non-goal 时使用。
  它只还原需求侧世界，不证明实现已满足这些定义。不适用于代码行为推断或架构分解。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-product-reconstructor

Use this skill to reconstruct product-side intent into structured objects.
Apply it after current_facts is available and before feature extraction.
Do not rely on it for implementation truth or architecture decomposition.

## Purpose

把产品证据还原成结构化产品对象（Goal、Role、Scenario、Constraint、Non-goal），为功能与关系分析提供上游锚点。

## Success criteria

- 输出产品对象时都带 `evidence_refs`。
- 无产品文档时返回 `partial`，记录 `missing_evidence` gap。
- 只处理 `current_facts.product_facts` 指向的产品文档证据。
- 不把代码行为等同于产品目标。
- 同步生成 `02-product-catalog.md`。

## Strategy

### 设计哲学

1. **证据约束范围** -- 只读取 current_facts.product_facts 指向的文档，不对全仓库兜底回退。
2. **显式优先于推断** -- 先提取显式目标、角色、场景，再考虑约束与非目标。
3. **缺失即留空** -- 找不到证据就留空并记录 gap，不创造"合理猜测"。
4. **需求侧隔离** -- 只还原需求世界，不从代码逆推产品愿景。
5. **渲染下沉** -- 目录渲染是确定性动作交给脚本，对象判断由当前会话完成。

## Tools and capability boundaries

- 读取 `context.evidence_registry` 与 `context.current_facts`。
- 允许基于文本结构做抽取与归类。
- 使用 `scripts/render_catalog.py` 落盘标准交付物。
- 不生成功能对象、关系对象或实现差异结论。
- 不把 inferred 对象提升为 explicit。
- 不允许通过脚本转发到后端 LLM。

## Important facts and constraints

- `required_sources` 以 `doc` 为主；未提供产品文档目录时返回空结果并记录 gap。
- 任何产品对象必须至少有一个 evidence_ref。
- "无证据时不生成对象"比"生成合理对象"更重要。

## Workflow

1. 读取共享协议与数据模型。
2. 验证 `context.current_facts` 存在。
3. 从产品证据中提取 Goal、Role、Scenario。
4. 补充 Constraint 与 Non-goal。
5. 产出结构化 objects/gaps 结果。
6. 调用 `scripts/render_catalog.py` 生成 `02-product-catalog.md` 并更新 deliverable_manifest。
7. 无产品文档时返回空 Catalog + gap。

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

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/references/deliverable-standard.md` -- 渲染时加载
- `scripts/render_catalog.py` -- 渲染阶段执行
- `references/task-contract.md` -- 判断口径校准
- `references/examples.md` -- 需要参考案例时加载
- `references/failure-modes.md` -- 遇到异常时加载

## Subtask / parallelism guidance

- 可按证据来源拆分（PRD / README / Wiki 分开抽取），再统一去重。
- 子任务不得把 inferred 内容升级为 explicit。

## Examples

**Example 1**
Input: 用户指定产品文档目录中的 PRD + Wiki
Output: Goal / Role / Scenario / Constraint / Non-goal

**Example 2**
Input: 未提供 product_docs_dir
Output: partial + 空对象列表 + missing_evidence gap

## Safety

- 不要从代码实现逆推产品愿景。
- 不要绕过 current_facts.product_facts 直接扫描全仓库。
- 不要把本 skill 包装成脚本后转发给外部 LLM。
