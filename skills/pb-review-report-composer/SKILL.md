---
name: pb-review-report-composer
description: |
  当所有 review registry 都已经准备好，并需要生成最终 Markdown 评审报告时使用。
  它负责把对象、依赖、实现映射、追踪关系、架构视图、数据流、冲突、差异和证据索引编排成人类可读报告。
  不适用于重新分析或纠正上游数据质量。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-report-composer

Use this skill to turn completed review registries into a human-readable Markdown report.
Apply it only after the upstream review artifacts are present.
Do not rely on it for re-running analysis or correcting upstream data quality.

## Purpose

把 `.review/` 中的结构化结果与前序交付物编排成最终可交付的 Markdown 总报告。

## Success criteria

- 读取全部核心 registry 并输出 `07-review-report.md`。
- 报告至少包含项目概览、交付物清单、产品层、功能规格概览、测试化摘要、依赖与实现、追踪矩阵、架构视图、数据流、差异与缺口、证据索引。
- 所有结论可回溯到对象 ID、关系 ID、冲突 ID 或 evidence ID。
- 不在报告阶段重新发明分析逻辑。

## Strategy

### 设计哲学

1. **编排而非分析** -- 报告只编排已有结论，不重跑上游判断。
2. **齐备性前置** -- registry 缺失时停止并指出缺口，不输出"看起来完整"的报告。
3. **可审计优先** -- 证据索引面向审计可追溯，不面向营销展示。
4. **模板稳定** -- 复用模板骨架保持报告结构稳定可比较。
5. **报告不是唯一** -- 最终报告不能替代前序产品目录、功能规格卡、追踪矩阵和 gap 分析。

## Tools and capability boundaries

- 读取 `.review/` registry 文件。
- 使用 `assets/report-template.md` 作为编排骨架。
- 可填充 Markdown 表格、列表和证据索引。
- 不修改 registry，不新增对象或关系。
- 可读取 deliverable_manifest 校验中间交付物齐备性。

## Important facts and constraints

- 报告是最终输出，不归集到 registry。
- 缺少关键 registry 时返回 failed 并指出缺口。
- 缺少 04-feature-specs/*.md、dependency_registry、traceability_matrix 等关键交付物时，不允许输出"看起来完整"的最终报告。

## Workflow

1. 读取共享协议、数据模型与 `assets/report-template.md`。
2. 确认核心 registry 和 deliverable_manifest 存在。
3. 按模板顺序填充各章节。
4. 输出 `07-review-report.md`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: []
context_writes: {}
metadata:
  report_path: string
  report_sections: array
  deliverables: array
errors: []
```

## Resources

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/references/deliverable-standard.md` -- 始终加载
- `assets/report-template.md` -- 渲染时使用

## Subtask / parallelism guidance

- 可把不同章节的数据预整理为摘要，但最终报告渲染应在单一步骤完成。
- 子任务不能各自输出独立报告文件。

## Examples

**Example 1**
Input: 所有 registry 齐全
Output: `.review/deliverables/07-review-report.md`

**Example 2**
Input: 缺少 object_registry.json
Output: failed，指出缺失的关键输入

## Safety

- 不要在缺少关键 registry 的情况下输出"看起来完整"的报告。
- 不要删除冲突或 gap 章节来美化结果。
- 不要用最终报告替代中间交付物。
