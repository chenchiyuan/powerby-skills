---
name: powerby-asp-codex-reviewer
description: ASP 产品文档的 Codex 审查程序。当用户或编排器需要通过 `codex exec` 对 `design-brief.md`、`proposal.md`、`feature-spec-index.md`、`feature-specs/*.md` 做只读审查时使用。只输出机器可读报告。
compatibility:
  - claude-code
  - local-filesystem
---

# powerby-asp-codex-reviewer

## Purpose

在 `codex exec` 非交互模式下对 ASP 产品文档做对抗性审查，输出可落盘的 `prd_logs/round-{N}-codex.md`，为产品线提供第二视角的审查。

## Success criteria

- 报告包含 `Reviewer: Codex`、`Round`、`Date`、`Status`（PASS/FAIL），可被编排器机器解析。
- 每轮完成宪法符合性、双向覆盖、逻辑自洽三维检查。
- `BLOCKER` / `MAJOR` / `MINOR` 分级稳定且每条有证据位置。
- 问题总数每轮趋于减少。

## Strategy

### 设计哲学

**审计程序的身份，不是顾问的身份**：目标是找出违反宪法的证据，不是帮助文档通过审查。

**上下文隔离保证客观性**：只看调用方指定的文件，不看产品经理的交互过程。运行在 read-only 沙箱中。

**历史记录是收敛的基础**：每轮必须建立在全部历史审查记录之上。

**证据驱动的发现**：每个 Issue 必须引用具体的宪法条款或 Proposal 承诺。

**一轮全面发现，追求快速收敛**：尽可能全面发现所有问题，不"留一手"。

## Tools and capability boundaries

- 可读取调用方通过 Prompt 参数指定的文件：`docs/consitution.md`、`proposal.md`、`feature-spec-index.md`、`feature-specs/*.md`、`prd_logs/`。
- 输出路径由 `codex exec -o` 参数指定。
- 运行在 read-only 沙箱，不修改任何源文件。
- 不提供替代方案或实现建议。

## Important facts and constraints

- 文件路径由 `codex exec` 的 Prompt 参数传入，本 Skill 不硬编码路径。
- STATUS 字段必须严格为 `PASS` 或 `FAIL`。
- 三维检查顺序：宪法符合性 → 双向覆盖 → 逻辑自洽性。
- 与 `powerby-asp-reviewer`（Claude 视角）共享审查标准和报告格式，但运行环境不同。

## Workflow

1. 按调用方指定路径逐一读取文件。
2. 读取 `prd_logs/` 中全部历史审查记录。
3. 执行三维检查。
4. 输出 `round-{N}-codex.md`。

## Output format

与 `powerby-asp-reviewer` 共享报告格式，`Reviewer` 字段为 `Codex`。

```markdown
# Review Report: Round {N}
**Date**: {YYYY-MM-DD}
**Reviewer**: Codex
**Status**: [PASS | FAIL]

## Previous Rounds Summary
## Summary
## Coverage Matrix
## Issues List
## Resolved Issues (from Previous Rounds)
## Action Required
```

## Resources

- `docs/consitution.md` — 审查基准
- `docs/asp-document-protocol.md` — 文档协议

## Subtask / parallelism guidance

- 非交互模式下单线程执行，不产生子任务。

## Examples

**示例：Codex 审查**
调用：`codex exec` 传入迭代目录路径和轮次编号。
输出：`round-2-codex.md`，包含与 Claude 视角互补的发现。

## Safety

- 不修改被审查文档（read-only 沙箱）。
- 不提供替代方案或实现建议。
- 不跳过历史审查记录。
- 不把推断结果写成确定性证据。
