---
name: pb-review-v2
description: |
  ASP 通用文档审查闭环 skill。当用户或编排器需要对 ASP 迭代目录执行阶段识别、上游对齐、问题发现、AUTO-FIX/ASK/ESCALATE 决策、修复指令生成和复审归档时使用。
  独立于现有 pb-review 和 powerby-asp-reviewer 体系。不适用于代码评审或还原式评审。
compatibility:
  - claude-code
  - local-filesystem
---

# pb-review-v2

Use this skill to run a structured review loop over ASP iteration documents.
Apply it when you need alignment check, findings analysis, and fix-or-escalate decisions for ASP stage deliverables.
Do not rely on it for code review, reconstruction-style review, or direct document modification.

## Purpose

对 ASP 迭代目录执行五阶段通用 review，输出机器可读的审查报告、修复指令和复审结论，形成"对齐 -> 发现 -> 决策 -> 归档"的质量闭环。

## Success criteria

- 能在 product / spec / architecture / plan / implementation 五个阶段中识别当前审查对象和上游事实链。
- 每轮报告以 Alignment Summary 开头，先确认上游对齐再进入 findings。
- 仅在 C3/C4 信心、证据充分、职责内时输出 AUTO-FIX；否则 ASK 或 ESCALATE。
- round > 3 时强制 ESCALATED，不继续自动修复。
- 不修改现有 pb-review / powerby-asp-reviewer / powerby-asp-arch-reviewer 的职责或文件。

## Strategy

### 设计哲学

1. **对齐先于审查** -- 未确认上游文档完整时不开始 findings 归类；Alignment Summary 失败即整轮 FAIL。
2. **默认自主驾驶** -- 信心充足且证据完整时自动 AUTO-FIX，不询问用户。信心不足或跨职责时才 ASK/ESCALATE。
3. **证据驱动修复** -- 每个 AUTO-FIX 必须包含证据位置、具体修复动作、验证方法，禁止猜测性修复。
4. **有限循环** -- Round 1-3 正常审查修复循环，Round 4 强制 ESCALATE 终止自动循环。
5. **聚焦核心** -- 基于阶段目标和上游对齐结果聚焦当前验收标准，不做无意义的全面检查。

### 信心分级（C1-C4）

| 等级 | 含义 | 决策 |
|------|------|------|
| C4 | 明确协议 + 完整证据 + 历史案例 | AUTO-FIX |
| C3 | 明确协议 + 充分证据 | AUTO-FIX（标注风险） |
| C2 | 部分证据 + 协议模糊 | ASK |
| C1 | 证据不足或跨职责 | ESCALATE |

## Tools and capability boundaries

- 可读取：ASP 迭代目录文档、历史 logs、协议文档、本 skill references
- 可写入：`{stage}_logs/round-{N}-*.md` 和 `round-{N}-fix-instructions.yaml`
- 不修改被审查文档（由 fixer skills 负责）
- 不调度 fixer skill 实际执行修复（由编排器负责）
- 不接管现有 pb-review 或 powerby-asp-*reviewer 的实现

## Important facts and constraints

- 五阶段主审查对象：product->proposal.md, spec->feature-spec-index.md + feature-specs/*.md, architecture->architecture.md, plan->tasks.md, implementation->implementation-report.md。
- 五阶段上游链：product<-design-brief.md, spec<-proposal.md, architecture<-proposal.md+specs, plan<-architecture.md, implementation<-tasks.md。
- Status 只能为 PASS / FAIL / ESCALATED。
- AUTO-FIX 是结构化修复指令，不是本 skill 自行改文档。
- 找不到阶段所需事实源时，必须在 Alignment Summary 中显式失败。

## Workflow

1. 读取 references 中的 checklist、decision-table、audit-template 与相关协议。
2. 识别当前阶段、主审查对象、上游链和历史日志目录。
3. 若 round > 3，直接跳转强制 ESCALATE。
4. 生成 Alignment Summary，检查上游完整性和对齐性；失败则直接 FAIL。
5. 通过后，基于阶段 checklist 生成 findings（严重度 + 信心分级 + 证据位置）。
6. 对每个 finding 决策 AUTO-FIX / ASK / ESCALATE。
7. 按模板输出报告和修复指令，判定最终 PASS / FAIL / ESCALATED。

## Output format

```markdown
# PB Review V2 Audit Report

**Reviewer**: {Claude | Codex | Other}
**Round**: {N}
**Stage**: {product | spec | architecture | plan | implementation}
**Status**: {PASS | FAIL | ESCALATED}

## Alignment Summary
## Findings
## Decision Summary
## Fix Instructions
## Review Result
```

修复指令格式：

```yaml
fix_instructions:
  - finding_id: string
    target_doc: string
    fix_action: string
    evidence_summary: array
    verification: string
```

## Resources

- `references/audit-checklist-ref.md` -- 通用审查闭环口径
- `references/product-checklist.md` -- 产品阶段维度
- `references/spec-checklist.md` -- 规格阶段维度
- `references/arch-checklist.md` -- 架构阶段维度
- `references/plan-checklist.md` -- 计划阶段维度
- `references/impl-checklist.md` -- 实现阶段维度
- `references/decision-table.md` -- 决策规则
- `references/audit-template.md` -- 报告模板
- `docs/asp-review-orchestrator-protocol.md` -- I/O 契约

## Subtask / parallelism guidance

- 可并行读取主审查对象、上游文档和历史日志，但 findings 和 decision 必须统一汇总。
- 不把单个阶段拆成多份报告。
- 不把不同阶段的 findings 混在一轮报告里。

## Examples

**Example 1**
Input: product 阶段审查，缺少 design-brief.md
Output: Alignment Summary FAIL，Status: FAIL，Fix Instructions 指向恢复上游文档。

**Example 2**
Input: architecture 阶段审查，FT-009/FT-010 缺少架构映射
Output: findings MAJ-001，C4 信心，AUTO-FIX 补充架构章节。

## Safety

- 禁止跳过对齐检查直接进入 findings。
- 禁止在证据不足（C1/C2）时输出 AUTO-FIX。
- 禁止 round > 3 时继续输出自动修复。
- 禁止越权修改被审查文档。
- 禁止覆盖或修改现有 pb-review / powerby-asp-reviewer / powerby-asp-arch-reviewer。
- 禁止通过脚本把抽象判断外包给外部 LLM。
