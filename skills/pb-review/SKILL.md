---
name: pb-review
description: 还原式项目评审框架的流程编排器。当用户要对仓库做事实还原、需求到实现追踪、差异审计，或从 `.review/` 断点继续评审时使用。它负责初始化 Review Context，并按顺序协调 project scope、evidence、conflict、feature/dependency/implementation reconstruction、relation、architecture、data-flow、gap、report 等下游 skill。抽象判断必须由当前 Codex/Claude 会话直接执行，不允许走后端 LLM HTTP 调用。
compatibility:
  - python3
  - local-filesystem
---

# pb-review

Use this skill to run a full reconstruction-traceability review workflow over a local repository.
Apply it when the user wants a structured review output rather than ad-hoc observations.
Do not rely on it for code fixing, subjective scoring, or V2 architecture/implementation reconstruction.

## Purpose

作为 009-review-framework 的入口 skill，负责把单次评审组织成一个可恢复、可追溯、可交付的顺序工作流，并输出符合功能规格定义标准的分层交付物。

## Success criteria

- 初始化或恢复 `.review/` 上下文，不跳过必需步骤。
- 严格按架构规定的顺序协调全部下游 skill。
- 只负责编排、归集、checkpoint 更新，不替下游 skill 做事实判断。
- 抽象判断只由当前宿主模型直接执行；脚本只负责确定性工作，不代理思考。
- 在任一子步骤 `failed` 时停止，并把最近成功断点显式暴露给用户。
- 交付物不能只有一份总报告；必须同时产出系统上下文、产品目录、功能规格索引、功能规格卡、追踪矩阵、gap 分析、分层架构文档、依赖矩阵、数据流图、最终报告和 4 份测试化专项报告。
- Operation 级功能必须遵循 [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)，并默认补齐 `D-15` / `D-16`。

## Strategy

1. 先界定本次成功标准：需要的是完整报告、局部恢复，还是单步重跑。
2. 优先读取 checkpoint 判断是否应恢复，而不是盲目重跑全链路。
3. 对确定性步骤优先使用本地脚本，对抽象步骤直接加载对应 skill 与 references 由当前会话完成。
4. 把每个子 skill 的结果当作证据处理：`success` 继续，`partial` 记录警告并继续，`failed` 立即停止。
5. 先持久化 registry/context，再更新 checkpoint，避免“显示完成但状态未落盘”。
6. 把 `deliverable_manifest` 当成一级上下文字段维护，任何交付物缺失都不能被最终报告掩盖。
7. 抽象 skill 里的模板化 Markdown 落盘动作应调用其自带 renderer script，而不是让模型手写最终格式。

## Tools and capability boundaries

- 使用文件系统读取与写入 `.review/` 下的 JSON registry。
- 使用固定的 `.review/deliverables/` 路径输出 Markdown 交付物。
- 使用 `rg`、`find`、`python3` 等工具为下游 skill 提供执行环境。
- 允许通过脚本执行确定性步骤：project-scope、evidence-collector、conflict-resolver，以及 Step 13~16 的专项测试化 renderer。
- 允许抽象 skill 在完成判断后调用各自的 renderer script 做模板渲染，但脚本不能参与抽象判断。
- 不直接做证据采集、冲突决议、事实还原或报告分析，这些职责必须下放给对应 skill。
- 不并行执行下游 skill；本框架明确采用顺序执行。

## Important facts and constraints

- 当前版本覆盖产品层、功能层、依赖层、实现映射层、架构层、数据流层主链路。
- ReviewContext 的逻辑字段与 `.review/` 物理文件是一一对应关系，不能改名。
- 所有 `objects`、`relations`、`conflicts`、`gaps` 的归集与去重由编排器负责。
- 新版最小必备 registry 包括 `feature_spec_registry`、`dependency_registry`、`implementation_registry`、`traceability_matrix`、`architecture_registry`、`data_flow_registry`、`difference_registry`、`deliverable_manifest`。
- 共享 schema 位于 `skills/pb-review/schemas/`，Step 13~16 必须直接读取这些 schema，而不是在多个 skill 内重复定义。
- 断点恢复基于 `checkpoint.json` 与实际文件一致性双重校验，缺文件时必须回退到最近可信步骤重跑。
- 禁止使用任何 `llm_client.py`、HTTP chat-completions、后端推理代理来执行下游抽象判断。
- 最终报告不是唯一交付物；没有功能规格卡、依赖矩阵、分层架构文档的数据还原不算完成。

## Workflow

1. 读取 [`references/review-contract.md`](./references/review-contract.md) 与 [`references/skill-sequence.md`](./references/skill-sequence.md)。
2. 确认 `project_path`、`scope`、`resume` 参数是否完整。
3. 确认用户是否提供产品文档目录；`product_docs_dir` 未提供时，不应把全仓库文档默认当成产品文档，产品层应返回缺失证据。
4. 若 `resume=true`，读取 `.review/checkpoint.json` 并校验 `completed_writes` 是否与目录现状一致。
5. 先执行确定性 bootstrap：
   - `pb-review-project-scope`
   - `pb-review-evidence-collector`
   - `pb-review-conflict-resolver`
6. 再由当前 Codex/Claude 会话直接加载并执行抽象 skill：
   - `pb-review-product-reconstructor`
   - `pb-review-feature-reconstructor`
   - `pb-review-dependency-reconstructor`
   - `pb-review-implementation-mapper`
   - `pb-review-relation-builder`
   - `pb-review-architecture-builder`
   - `pb-review-data-flow-builder`
   - `pb-review-gap-analyzer`
7. 抽象 skill 先产出结构化结果，再调用各自 renderer script 生成对应 Markdown deliverable，并同步更新 `deliverable_manifest`：
   - `01-system-context.md`
   - `02-product-catalog.md`
   - `03-feature-spec-index.md`
   - `04-feature-specs/{function_id}.md`
   - `05-traceability-matrix.md`
   - `06-gap-analysis.md`
   - `08-architecture-layered.md`
   - `09-dependency-matrix.md`
   - `10-data-flow.md`
8. 执行 `pb-review-report-composer` 产出 `07-review-report.md`。
9. 顺序执行 Step 13~16 的确定性 renderer：
   - `11-testability-scorecard.md`
   - `12-test-case-index.md`
   - `13-test-fixture-contract.md`
   - `14-test-oracle-matrix.md`
10. 每一步都先归集标准输出与 `context_writes`，再更新 checkpoint。
11. 最终返回报告路径、已完成步骤、未完成步骤与任何 `partial` 警告。

## Output format

返回统一协议结构：

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: []
context_writes: {}
metadata:
  total_duration_ms: number
  completed_skills: array
  failed_skills: array
  report_path: string
  deliverables: array
errors: []
```

## Resources

- [`references/review-contract.md`](./references/review-contract.md)
- [`references/data-model.md`](./references/data-model.md)
- [`references/deliverable-standard.md`](./references/deliverable-standard.md)
- [`references/skill-sequence.md`](./references/skill-sequence.md)
- [`schemas/d17-oracle-schema.md`](./schemas/d17-oracle-schema.md)
- [`schemas/d18-fixture-schema.md`](./schemas/d18-fixture-schema.md)
- [`schemas/d19-test-groups-schema.md`](./schemas/d19-test-groups-schema.md)
- [`schemas/d20-coverage-claim-schema.md`](./schemas/d20-coverage-claim-schema.md)
- [`schemas/testability-status-rules.md`](./schemas/testability-status-rules.md)
- [`schemas/testability-score-formula.md`](./schemas/testability-score-formula.md)
- [`schemas/gap-severity-rules.md`](./schemas/gap-severity-rules.md)
- [`schemas/entry-surface-types.md`](./schemas/entry-surface-types.md)
- [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)
- [`docs/review/pb-review-deliverable-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/pb-review-deliverable-standard.md)
- [`docs/iterations/009-review-framework/spec.md`](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/009-review-framework/spec.md)
- [`docs/iterations/009-review-framework/architecture.md`](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/009-review-framework/architecture.md)

## Subtask / parallelism guidance

- 不要并行执行下游 skill；009 的依赖链是顺序型。
- 只有在纯读阶段才允许把大仓库扫描拆成独立子任务。
- 子任务只返回摘要和结构化结果，不直接写 `.review/`。
- 不要把子任务或脚本伪装成“另一个后端模型服务”。

## Examples

**Example 1**  
Input: “请对 `/path/to/repo` 做一次完整还原式评审，并以 `docs/product/` 作为产品文档目录。”  
Output: 生成 `.review/` 全套 registry、`deliverable_manifest` 和分层 Markdown deliverables。

**Example 2**  
Input: “上次在 gap-analyzer 前中断了，请从 checkpoint 继续。”  
Output: 校验 checkpoint 后从下一个 step 恢复执行。

## Safety

- 不允许跳过上游依赖直接调用下游 skill。
- 不允许在无 checkpoint 一致性校验的前提下宣称“已恢复”。
- 不允许把推断结果写成显式事实。
- 不允许用脚本把抽象判断偷偷转发到外部 LLM。
- 不允许在没有 `04-feature-specs/*.md` 的情况下宣称“评审已完成”。
