---
name: pb-review-project-scope
description: 当还原式项目评审需要先扫描仓库、定义评审范围并建立资料清单时使用。它负责生成 `project_metadata` 和 `resource_inventory`，为后续 evidence 采集提供唯一入口。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-project-scope

Use this skill to define review scope and discover project materials.
Apply it before any evidence extraction or reconstruction step.
Do not rely on it for semantic analysis, conflict resolution, or feature inference.

## Purpose

为评审流程建立范围边界与资料索引，明确“接下来读哪些文件，不读哪些文件”。

## Success criteria

- 正确识别项目路径是否存在且可读。
- 输出 `project_metadata`，包含 `project_name`、`project_type`、`scope`、`resource_inventory`、`entry_surface_inventory`、`missing_resources`。
- 初始化 `deliverable_manifest`，显式列出后续必备交付物路径与责任 skill。
- 只做发现与归类，不解释文件内容含义。
- 无可读文件时返回 `failed`，而不是伪造 inventory。

## Strategy

1. 先验证路径与 scope，再开始扫描。
2. 优先按 include/exclude pattern 建立文件清单，而不是先猜项目类型。
3. 通过 docs/code/tests/configs 四类库存表达可用证据面。
4. 基于 entry surface 类型标准补充 `entry_surface_inventory`，但不做功能语义推断。

## Tools and capability boundaries

- 使用 `find`、`rg --files`、文件系统 API 扫描目录。
- 可根据目录与文件后缀粗略判断项目类型。
- 不读取大文件全文做语义解析。
- 不生成 Evidence Unit，不修改其他 registry。

## Important facts and constraints

- 这是入口 skill，没有上游依赖。
- `resource_inventory` 是 EvidenceCollector 的唯一合法资料来源。
- `missing_resources` 记录的是资源类型缺失，不是质量判断。
- `node_modules/`、`.git/` 等默认属于排除范围，除非用户明确要求纳入。
- 本阶段要初始化交付物清单，但不负责补写下游交付内容。
- 010 升级后，必须维护 `DLV-011` ~ `DLV-014` 的 manifest 条目。

## Workflow

1. 读取 `../pb-review/references/review-contract.md`。
2. 验证 `project_path`、`scope`、`include_patterns`、`exclude_patterns`。
3. 扫描项目，按 docs/code/tests/configs 分类。
4. 基于 `entry-surface-types` 标准识别 CLI / API / page / cron / orchestration 入口。
5. 估算 `project_type`，例如 `frontend`、`backend`、`monorepo`、`mixed`。
6. 初始化 `context_writes.deliverable_manifest`。
7. 写出 `context_writes.project_metadata`。
8. 如果某类资源缺失，保留在 `missing_resources`，但不要推断原因。

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

- [`../pb-review/references/review-contract.md`](../pb-review/references/review-contract.md)
- [`../pb-review/references/data-model.md`](../pb-review/references/data-model.md)
- [`../pb-review/references/deliverable-standard.md`](../pb-review/references/deliverable-standard.md)
- [`../pb-review/schemas/entry-surface-types.md`](../pb-review/schemas/entry-surface-types.md)
- [`assets/system-context-template.md`](./assets/system-context-template.md)
- [`docs/review/feature-specification-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/feature-specification-standard.md)
- [`docs/review/pb-review-deliverable-standard.md`](/Users/chenchiyuan/projects/powerby-skills/docs/review/pb-review-deliverable-standard.md)
- [`docs/iterations/009-review-framework/architecture.md`](/Users/chenchiyuan/projects/powerby-skills/docs/iterations/009-review-framework/architecture.md)

## Subtask / parallelism guidance

- 大仓库可按目录分片扫描，但最终必须归并成单一 `resource_inventory`。
- 子任务只负责列清单，不解释文件含义。

## Examples

**Example 1**  
Input: `project_path=/repo, scope=full_project`  
Output: `project_metadata` + `resource_inventory`

**Example 2**  
Input: `project_path=/repo/services/api, scope=single_service`  
Output: 局部范围的资料清单

## Safety

- 不要把 README 缺失直接解释为“项目无产品定义”。
- 不要在扫描阶段读取敏感目录或外部挂载目录。
