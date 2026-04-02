---
name: pb-review
description: |
  还原式项目评审框架的流程编排器。当用户要对仓库做事实还原、需求到实现追踪、差异审计，或从 .review/ 断点继续评审时使用。
  不适用于代码修复、主观评分或单文件 review。
compatibility:
  - python3
  - local-filesystem
---

# pb-review

Use this skill to run a full reconstruction-traceability review workflow over a local repository.
Apply it when the user wants a structured review output rather than ad-hoc observations.
Do not rely on it for code fixing, subjective scoring, or single-file review.

## Purpose

作为 pb-review 体系的入口编排器，把单次评审组织成可恢复、可追溯、可交付的顺序工作流，协调全部下游 skill 并输出分层交付物。

## Success criteria

- 初始化或恢复 `.review/` 上下文，不跳过必需步骤。
- 严格按架构规定的顺序协调全部下游 skill。
- 只负责编排、归集、checkpoint 更新，不替下游 skill 做事实判断。
- 在任一子步骤 `failed` 时停止，暴露最近成功断点。
- 交付物必须包含系统上下文、产品目录、功能规格索引与规格卡、追踪矩阵、gap 分析、架构文档、依赖矩阵、数据流图、最终报告。

## Strategy

### 设计哲学

1. **编排即胶水** -- 编排器只做串联、归集和 checkpoint，所有事实判断下放给对应子 skill。
2. **checkpoint 先于宣称** -- 先持久化 registry，再更新 checkpoint，避免"显示完成但状态未落盘"。
3. **证据即信号** -- 把每个子 skill 的结果当证据：success 继续，partial 记录警告继续，failed 立即停止。
4. **恢复优先于重跑** -- 优先读取 checkpoint 判断是否应恢复，而不是盲目重跑全链路。
5. **确定性下沉** -- 确定性步骤用脚本，抽象判断由当前会话直接完成。

### 判断框架

1. 先界定本次成功标准：完整报告、局部恢复，还是单步重跑。
2. 对确定性步骤优先使用本地脚本，对抽象步骤直接加载对应 skill。
3. 把 `deliverable_manifest` 当一级上下文字段维护，任何交付物缺失都不能被最终报告掩盖。

## Tools and capability boundaries

- 文件系统读写 `.review/` 下的 JSON registry 和 Markdown 交付物。
- `rg`、`find`、`python3` 等工具为下游 skill 提供执行环境。
- 脚本执行确定性步骤（project-scope、evidence-collector、conflict-resolver 和 renderer）。
- 不直接做证据采集、冲突决议、事实还原或报告分析 -- 下放给对应 skill。
- 不并行执行下游 skill；本框架采用顺序执行。

## Important facts and constraints

- ReviewContext 的逻辑字段与 `.review/` 物理文件一一对应，不能改名。
- 所有 `objects`、`relations`、`conflicts`、`gaps` 的归集与去重由编排器负责。
- 断点恢复基于 `checkpoint.json` 与实际文件一致性双重校验，缺文件时回退到最近可信步骤重跑。
- 禁止使用 `llm_client.py`、HTTP chat-completions 或后端推理代理执行抽象判断。
- 最终报告不是唯一交付物；没有功能规格卡、依赖矩阵、分层架构文档的数据还原不算完成。
- 确认用户是否提供产品文档目录；未提供时不应把全仓库文档默认当成产品文档。

## Workflow

1. 读取 `references/review-contract.md` 与 `references/skill-sequence.md`。
2. 确认 `project_path`、`scope`、`product_docs_dir`、`resume` 参数。
3. 若 `resume=true`，校验 checkpoint 与目录现状一致性。
4. 执行确定性 bootstrap：`project-scope` -> `evidence-collector` -> `conflict-resolver`。
5. 加载并执行抽象 skill：`product-reconstructor` -> `feature-reconstructor` -> `dependency-reconstructor` -> `implementation-mapper` -> `relation-builder` -> `architecture-builder` -> `data-flow-builder` -> `gap-analyzer`。
6. 抽象 skill 先产出结构化结果，再调用各自 renderer script 生成 Markdown deliverable。
7. 执行 `report-composer` 产出最终报告。
8. 每一步先归集标准输出与 `context_writes`，再更新 checkpoint。
9. 返回报告路径、已完成步骤、未完成步骤与 partial 警告。

## Output format

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

- `references/review-contract.md` -- 始终加载
- `references/data-model.md` -- 始终加载
- `references/deliverable-standard.md` -- 始终加载
- `references/skill-sequence.md` -- 始终加载
- `schemas/*.md` -- 按需加载

## Subtask / parallelism guidance

- 不并行执行下游 skill；依赖链是严格顺序型。
- 只有纯读阶段允许把大仓库扫描拆成独立子任务。
- 子任务只返回摘要和结构化结果，不直接写 `.review/`。

## Examples

**Example 1**
Input: "请对 `/path/to/repo` 做一次完整还原式评审，产品文档目录为 `docs/product/`。"
Output: `.review/` 全套 registry 和分层 Markdown deliverables。

**Example 2**
Input: "上次在 gap-analyzer 前中断了，请从 checkpoint 继续。"
Output: 校验 checkpoint 后从下一步恢复执行。

## Safety

- 不允许跳过上游依赖直接调用下游 skill。
- 不允许在无 checkpoint 一致性校验的前提下宣称"已恢复"。
- 不允许把推断结果写成显式事实。
- 不允许用脚本把抽象判断转发到外部 LLM。
- 不允许在没有功能规格卡的情况下宣称"评审已完成"。
