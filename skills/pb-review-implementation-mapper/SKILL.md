---
name: pb-review-implementation-mapper
description: |
  当评审流程已经有 feature_spec_registry，并需要把 Feature 映射到入口、服务、仓储、模型、测试、配置等实现锚点时使用。
  它负责描述"功能落在哪"，不负责评价实现好坏。不适用于代码审查或架构评分。
compatibility:
  - python3
  - local-filesystem
---

# pb-review-implementation-mapper

Use this skill to map reconstructed features onto concrete implementation anchors.
Apply it after feature specs are available.
Do not rely on it for code review or architectural scoring.

## Purpose

把 Feature 与入口、服务、仓储、模型、测试、配置的实现锚点对齐，补全 D-16 并输出 implementation_registry。

## Success criteria

- 输出 implementation_registry。
- 回填 feature_spec_registry[*].implementation_mapping。
- 路径和符号都能回溯到具体代码或配置证据。
- 证据不足时返回 partial，不用路径命名模式硬补。

## Strategy

### 设计哲学

1. **入口驱动** -- 从已知入口点出发，追到服务、仓储、模型、测试和配置。
2. **显式证据优先** -- 优先采用 import、调用、测试断言、配置引用等证据。
3. **存在性可脚本化** -- 路径存在性检查可脚本化，但"是否构成核心映射"必须由当前会话判断。
4. **多锚点允许** -- 一个功能可对应多个实现锚点，但必须标明 role。
5. **不评价只映射** -- 只描述功能落在哪，不评价实现好坏。

## Tools and capability boundaries

- 读取 `context.feature_spec_registry`、`context.evidence_registry`、`context.current_facts`。
- 允许从命令、路由、服务、测试、配置和模型定义中建立实现映射。
- 可在完成判断后调用 feature-reconstructor 的 renderer 刷新 03/04 交付物。
- 不输出差异结论，不做架构分层裁决。

## Important facts and constraints

- implementation_mapping 推荐分为 entrypoints、services、repositories、models、tests、configs。
- 禁止把"同目录文件"自动视为实现映射。

## Workflow

1. 读取共享协议、数据模型与现有 feature_spec_registry。
2. 为每个功能识别入口、服务、仓储、模型、测试、配置。
3. 输出 `context_writes.implementation_registry`。
4. 回填 feature_spec_registry 中的 implementation_mapping。
5. 需要时刷新 03/04 交付物。

## Output format

```yaml
status: success | partial | failed
objects: []
relations: []
conflicts: []
gaps: array
context_writes:
  implementation_registry: array
  feature_spec_registry: array
metadata:
  mapped_features: number
  mapping_records: number
errors: []
```

## Resources

- `../pb-review/references/review-contract.md` -- 始终加载
- `../pb-review/references/data-model.md` -- 始终加载
- `../pb-review/references/deliverable-standard.md` -- 渲染时加载
- `../pb-review-feature-reconstructor/scripts/render_feature_deliverables.py` -- 刷新 03/04 时执行

## Safety

- 不要把实现细节反向伪装成用户功能。
- 不要用硬编码目录规则自动填满 implementation_mapping。
