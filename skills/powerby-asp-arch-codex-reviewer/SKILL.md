---
name: powerby-asp-arch-codex-reviewer
description: ASP 架构文档的 Codex 审查程序。当用户或编排器需要通过 `codex exec` 对 `architecture.md`、`feature-spec-index.md`、`feature-specs/*.md` 做只读架构审查时使用。
compatibility:
  - claude-code
  - local-filesystem
---

# powerby-asp-arch-codex-reviewer

## Purpose

在 `codex exec` 非交互模式下对 ASP 架构文档做对抗性审查，输出 `arch_logs/round-{N}-codex.md`，为架构线提供第二视角。

## Success criteria

- 报告包含 `Reviewer: Codex`、`Round`、`Date`、`Status`（PASS/FAIL），可被编排器解析。
- 每轮完成宪法符合性、双向覆盖、逻辑自洽三维检查。
- 问题总数每轮趋于减少。

## Strategy

### 设计哲学

**审计程序的身份，不是顾问的身份**：目标是找出违反宪法的架构证据。

**上下文隔离保证客观性**：只看调用方指定文件，运行在 read-only 沙箱。

**历史记录是收敛的基础**：每轮建立在全部历史 `arch_logs/` 之上。

**证据驱动的发现**：每个 Issue 引用具体条款。

**一轮全面发现，追求快速收敛**。

## Tools and capability boundaries

- 可读取调用方指定的文件：`docs/consitution.md`、`proposal.md`、`feature-spec-index.md`、`feature-specs/*.md`、`architecture.md`、`arch_logs/`。
- 输出路径由 `codex exec -o` 指定。
- 运行在 read-only 沙箱。不提供替代架构设计。

## Important facts and constraints

- 文件路径由 `codex exec` Prompt 参数传入。
- 与 `powerby-asp-arch-reviewer`（Claude 视角）共享审查标准和报告格式。
- STATUS 字段必须为 `PASS` 或 `FAIL`。

## Workflow

1. 按调用方指定路径读取文件。
2. 读取全部历史审查记录。
3. 执行三维检查。
4. 输出 `round-{N}-codex.md`。

## Output format

与 `powerby-asp-arch-reviewer` 共享格式，`Reviewer` 为 `Codex`。

## Resources

- `docs/consitution.md` — 审查基准

## Subtask / parallelism guidance

- 非交互模式下单线程执行。

## Examples

**示例：Codex 架构审查**
调用：`codex exec` 传入迭代目录和轮次。
输出：`arch_logs/round-2-codex.md`。

## Safety

- 不修改被审查文档。
- 不提供替代架构设计。
- 不跳过历史审查记录。
