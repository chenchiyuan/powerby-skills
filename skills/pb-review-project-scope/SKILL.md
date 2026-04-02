---
name: pb-review-project-scope
description: |
  当还原式项目评审需要先扫描仓库、定义评审范围并建立资料清单时使用。
  它负责生成 project_metadata 和 resource_inventory，为后续 evidence 采集提供唯一入口。
  不适用于语义分析、冲突决议或功能推断。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-project-scope

Use this skill to define review scope and discover project materials.
Apply it before any evidence extraction or reconstruction step.
Do not rely on it for semantic analysis, conflict resolution, or feature inference.

## Purpose

为评审流程建立范围边界与资料索引，明确"接下来读哪些文件，不读哪些文件"。

## Success criteria

- 输出 `project_metadata`，包含 project_name、project_type、scope、resource_inventory、entry_surface_inventory、missing_resources。
- 初始化 `deliverable_manifest`，列出后续必备交付物路径与责任 skill。
- 只做发现与归类，不解释文件内容含义。
- 无可读文件时返回 `failed`，不伪造 inventory。

## Strategy

### 设计哲学

1. **边界先于内容** -- 先验证路径与 scope，再开始扫描。
2. **归类而非解释** -- 按 docs/code/tests/configs 四类归档，不做语义推断。
3. **发现而非猜测** -- 通过文件存在性判断项目类型，而不是先猜后验。
4. **入口识别是确定性工作** -- 按 entry surface 类型标准扫描，不做功能语义推断。
5. **缺失即记录** -- 资源类型缺失记录在 missing_resources，不评价原因。

## Tools and capability boundaries

- 使用 `find`、`rg --files`、文件系统 API 扫描目录。
- 可根据目录与文件后缀粗略判断项目类型。
- 不读取大文件全文做语义解析。
- 不生成 Evidence Unit，不修改其他 registry。

## Important facts and constraints

- 这是入口 skill，没有上游依赖。
- `resource_inventory` 是 evidence-collector 的唯一合法资料来源。
- `node_modules/`、`.git/` 等默认属于排除范围。
- 本阶段初始化交付物清单，但不负责补写下游交付内容。

## Workflow

1. 读取 `../pb-review/references/review-contract.md`。
2. 验证 `project_path`、`scope`、`include_patterns`、`exclude_patterns`。
3. 扫描项目，按 docs/code/tests/configs 分类。
4. 基于 entry-surface-types 标准识别入口。
5. 估算 project_type。
6. 初始化 `deliverable_manifest`。
7. 写出 `project_metadata`。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: []
context_writes:
  project_metadata:
    project_name: string
    project_type: string
    scope: string
    file_count: number
    resource_inventory:
      docs: array
      code: array
      tests: array
      configs: array
    missing_resources: array
  deliverable_manifest: object
metadata:
  scan_duration_ms: number
errors: []
```

## Resources

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/schemas/entry-surface-types.md` -- 入口识别时加载
- `assets/system-context-template.md` -- 渲染时使用

## Subtask / parallelism guidance

- 大仓库可按目录分片扫描，但最终必须归并成单一 resource_inventory。
- 子任务只负责列清单，不解释文件含义。

## Examples

**Example 1**
Input: `project_path=/repo, scope=full_project`
Output: project_metadata + resource_inventory

**Example 2**
Input: `project_path=/repo/services/api, scope=single_service`
Output: 局部范围的资料清单

## Safety

- 不要把 README 缺失直接解释为"项目无产品定义"。
- 不要在扫描阶段读取敏感目录或外部挂载目录。
