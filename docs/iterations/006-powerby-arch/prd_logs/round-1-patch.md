# Patch Record: Round 1
**Date**: 2026-02-10
**Based on**: round-1-claude.md
**Spec Version**: v1.0.0 → v1.1.0

## Fixed Issues
| Issue ID | Type | Description | Action |
|----------|------|------------|--------|
| 001 | BLOCKER | 架构修复流程（Refinery Mode）缺失 | 新增 US-013（Refinery Mode），定义逐项修复协议、严禁镀金、修复记录保存 |
| 002 | BLOCKER | Reviewer 上下文隔离未定义 | 新增 US-014（上下文隔离），明确 Reviewer 仅接收 5 类文件，屏蔽 Architect 思考过程 |
| 003 | MAJOR | 历史审查记录上下文传递缺失 | 在 US-004 中新增 Scenario「历史审查记录上下文传递」，要求每轮读取前序报告、标注 New/Inherited |
| 004 | MAJOR | 修复记录存储规则缺失 | 在 US-004 中补充 round-{N}-patch.md 存储规则 |
| 005 | MINOR | Data Dictionary 不完整 | 补充 Refinery Mode、round-{N}-patch.md、上下文隔离等术语定义 |

## Changes Summary
- 新增 US-013（Refinery Mode）、US-014（上下文隔离）
- 更新 US-004 Gherkin（历史上下文传递 + 修复记录存储）
- 更新 Data Dictionary（+5 术语）
- 更新 Traceability Matrix（REQ-003 → US-004, US-013, US-014）
