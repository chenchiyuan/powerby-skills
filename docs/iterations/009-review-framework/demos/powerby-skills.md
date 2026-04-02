# Demo: 在 powerby-skills 仓库上执行 pb-review

## 1. 执行命令

```bash
python3 skills/pb-review/scripts/review_runner.py \
  --project-path /Users/chenchiyuan/projects/powerby-skills \
  --scope full_project
```

## 2. 执行结果

- **最终状态**: `partial`
- **原因**: 真实运行成功，但仍存在由 `relation-builder` / `gap-analyzer` 输出的链路缺口与差异
- **报告路径**: `/Users/chenchiyuan/projects/powerby-skills/.review/review_report.md`
- **评审目录**: `/Users/chenchiyuan/projects/powerby-skills/.review`
- **完成时间**: 2026-03-27 09:47 UTC

## 3. 产物清单

运行后实际生成了：

- `.review/checkpoint.json`
- `.review/project_metadata.json`
- `.review/evidence_cache.json`
- `.review/evidence_registry.json`
- `.review/current_facts.json`
- `.review/object_registry.json`
- `.review/feature_state_registry.json`
- `.review/relation_registry.json`
- `.review/gap_registry.json`
- `.review/review_report.md`

## 4. 关键统计

本次真实运行的中间产物规模：

- `evidence_registry.json`: 8420 条 Evidence Unit
- `object_registry.json`: 5337 条 Object Record
- `feature_state_registry.json`: 3023 条 Feature State
- `relation_registry.json`: 2417 条 Relationship Record
- `gap_registry.json`: 2489 条 Gap Record
- `conflict_registry.json`: 0 条 Conflict Record

## 5. 示例发现

报告中可以看到以下类型的真实输出：

- 项目概览：`powerby-skills` 被识别为 `skill-repo`
- 产品层对象：提取出 Goal / Role / Scenario 候选
- 功能层对象：提取出 Feature / Rule / Boundary 候选
- 关系矩阵：建立 Goal → Feature、Rule → Feature 的追踪关系
- 差异与缺口：由于状态与关系并不完全闭环，结果为 `partial`
- 本轮重构后，抽象判断已改为 `SKILL.md + task-contract + examples + failure-modes` 驱动，执行脚本只保留证据打包、contract 调用、结果校验和落盘
- `strategy.json` 已移除，不再使用“声明式规则表”承载抽象判断

## 6. 当前局限

这个 demo 证明了 009 已经从“skill 骨架”提升到“可执行最小闭环”，而且 4 个核心抽象 skill 已完成去硬编码重构，但抽取质量仍然不够强：

- 产品/功能抽取仍偏宽，仍会吸入部分章节标题和流程描述
- 对 skill 仓库这种“文档即实现”的项目，Feature State 仍主要依赖词项重叠，精度有限
- relation / gap 的噪声虽有下降，但离“可直接用于严格验收”仍有距离

结论：  
**运行时闭环已建立，4 个核心抽象 skill 已进入“skill-contract 驱动”形态，009 不再依赖本地规则表；但质量仍处于“已对准正确架构、仍需继续打磨运行效果”的阶段。**
