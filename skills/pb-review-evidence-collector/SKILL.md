---
name: pb-review-evidence-collector
description: |
  当评审流程已经有 project_metadata.resource_inventory，并需要把文档、代码、测试、配置和 Git 历史统一标准化为 evidence_registry 时使用。
  它应优先调用确定性脚本，不适用于证据优先级判断或业务结论推导。
compatibility:
  - python3
  - git
  - local-filesystem
---

# pb-review-evidence-collector

Use this skill to normalize project materials into Evidence Unit records.
Apply it after scope discovery and before any reconstruction step.
Do not rely on it for judging evidence priority or drawing business conclusions.

## Purpose

把分散的项目材料转换成统一的 Evidence Unit，为后续冲突决议和事实还原提供标准输入。

## Success criteria

- 从 `resource_inventory` 读取资料，不绕过上游直接发现文件。
- 优先调用 bundled scripts 生成确定性 JSON。
- 产出 `evidence_registry`，统计按来源类型分布。
- 对不可读文件返回 `partial`，记录错误和跳过信息。

## Strategy

### 设计哲学

1. **上游约束** -- 只采集 resource_inventory 列出的资料，不自行发现新文件。
2. **确定性优先** -- 文件读取与标准化交给脚本，避免每次重写采集逻辑。
3. **多源归一** -- Git 历史与 doc/code/test/config 一起归一化为 Evidence Unit。
4. **采集即停** -- 采集结束即停止，不在此阶段判断真伪或优先级。
5. **诚实记录** -- 拿不到内容就记录错误或 gap，不伪造内容。

## Tools and capability boundaries

- 优先执行 `scripts/collect_evidence.py`。
- 需要 Git 历史时执行 `scripts/parse_git_history.py`。
- 可使用临时 JSON 文件作为脚本中间产物。
- 不做冲突判断、对象提取或报告生成。

## Important facts and constraints

- `source_type` 仅允许 `doc`、`code`、`test`、`config`、`commit`、`issue`。
- `evidence_cache.json` 是内部缓存，不能替代 `evidence_registry.json`。
- 字段命名必须与共享数据模型一致。

## Workflow

1. 读取 `../pb-review/references/review-contract.md` 与 `../pb-review/references/data-model.md`。
2. 验证 `context.project_metadata.resource_inventory` 存在。
3. 运行 `scripts/collect_evidence.py` 采集 docs/code/tests/configs。
4. 运行 `scripts/parse_git_history.py` 采集 commit 元信息。
5. 合并为统一 `evidence_registry`，统计来源数量。
6. 对不可读文件或 git 失败保留错误明细。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: []
context_writes:
  evidence_registry: array
metadata:
  total_evidence_count: number
  by_source_type:
    doc: number
    code: number
    test: number
    config: number
    commit: number
    issue: number
  cache_hit_rate: number
errors: []
```

## Resources

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `scripts/collect_evidence.py` -- 采集阶段执行
- `scripts/parse_git_history.py` -- Git 历史采集时执行

## Subtask / parallelism guidance

- 可按资源类别拆分采集，但最终统一回收到单一 evidence_registry。
- Git 历史和文件证据可独立采集后合并。

## Examples

**Example 1**
Input: 已有 resource_inventory
Output: evidence_registry.json

**Example 2**
Input: 第二次运行且 incremental=true
Output: 复用 evidence_cache.json，只重采变更文件

## Safety

- 不直接把脚本输出写进 `.review/`；统一由编排器持久化。
- 不因 Git 历史不可用就丢弃 doc/code 证据。
