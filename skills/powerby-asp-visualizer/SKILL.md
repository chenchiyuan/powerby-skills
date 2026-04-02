---
name: powerby-asp-visualizer
description: ASP 产品全景图与测试化产物生成器。当用户需要根据 `proposal.md`、`feature-spec-index.md`、`feature-specs/*.md` 生成 `product-map.md`、`traceability-matrix.md` 和 `testability-scorecard.md` 时使用。
compatibility:
  - claude-code
  - local-filesystem
---

# powerby-asp-visualizer

## Purpose

把通过审查的 ASP 产品文档编译成用户可读的全景图、追溯矩阵和测试化评分卡，帮助决策者从全局视角确认"这真的是我想要的吗？"。

## Success criteria

- `product-map.md` 包含功能全景树、用户旅程流、决策摘要三个视图。
- `traceability-matrix.md` 展示 Goal → REQ → Feature → Implementation 的完整追踪链。
- `testability-scorecard.md` 展示每个 Feature 的测试就绪度评分。
- 所有视图内容忠实于规格文档，不添加规格中不存在的功能。
- 裁剪报告和风险提示基于审查记录的事实，不凭推测。

## Strategy

### 设计哲学

**忠实编译优于创意美化**：全景图是规格文档的忠实映射，不是设计师的创意作品。规格中没有的功能不出现在视图中。

**先展示核心旅程，再标出异常边界**：用户旅程流先展示"核心价值的最短路径"，再用分支标注异常情况，确保决策者先看到主线。

**裁剪和风险必须诚实**：MVP 裁剪报告直接比对 proposal 和 specs 的差异，不美化；风险提示来自审查记录的真实发现。

**可视化是沟通工具，不是验证工具**：本 skill 的产物服务于人类理解，不替代审查和测试。

## Tools and capability boundaries

- 可读取 `proposal.md`、`feature-spec-index.md`、`feature-specs/*.md`、`prd_logs/`、`arch_logs/`。
- 可写入 `product-map.md`、`traceability-matrix.md`、`testability-scorecard.md`。
- 使用 Mermaid 语法生成图表。
- 不修改被编译的源文档。不做需求或架构判断。

## Important facts and constraints

- `product-map.md` 使用 Mermaid mindmap（全景树）、sequenceDiagram/flowchart（旅程流）。
- 追溯矩阵必须覆盖完整链路，缺失环节显式标注为断链。
- 测试化评分基于 `D-17~D-20` 字段的完整度。
- 审查记录中即使已修复的风险也需在风险提示中提及。

## Workflow

1. 读取全部产品文档和审查记录。
2. 生成 `product-map.md`（功能全景树 + 用户旅程流 + 决策摘要）。
3. 生成 `traceability-matrix.md`（Goal → REQ → Feature → Implementation 追踪）。
4. 生成 `testability-scorecard.md`（每个 Feature 的 D-17~D-20 完整度评分）。

## Output format

### product-map.md

```markdown
# Product Panorama: {项目名称}
## 视图 A: 功能全景树 (Mermaid mindmap)
## 视图 B: 用户旅程流 (Mermaid sequenceDiagram/flowchart)
## 视图 C: 决策摘要
### 一句话价值
### MVP 裁剪报告
### 风险提示
```

### traceability-matrix.md

```markdown
# Traceability Matrix
| Goal | REQ | Feature | Implementation | Status |
```

### testability-scorecard.md

```markdown
# Testability Scorecard
| Feature | D-17 | D-18 | D-19 | D-20 | Score |
```

## Resources

- `docs/asp-document-protocol.md` — 文档协议

## Subtask / parallelism guidance

- 三个产出文件可并行生成（互不依赖）。
- 不将可视化判断下放给脚本。

## Examples

**示例：VISUALIZING 阶段**
输入：审查通过的 proposal + feature-specs + 审查记录。
输出：product-map.md + traceability-matrix.md + testability-scorecard.md。

## Safety

- 不修改源文档。
- 不添加规格中不存在的功能。
- 不把推测写成事实。
