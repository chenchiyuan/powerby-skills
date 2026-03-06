# Patch Report: Round 1
**Date**: 2026-02-11

## Fixed Issues

### Issue 001 (MAJOR) — 编号冲突解决策略缺失
**修复方式**：在 US-001 中新增 Scenario "iterations.json 与目录编号不一致时的冲突解决"，明确以 max(json, 目录) + 1 为准，不自动补录无关迭代。

### Issue 002 (MAJOR) — 阶段恢复规则模糊
**修复方式**：在 US-002 Scenario 1 中将"根据目录下已有文件判断从哪个阶段继续"替换为明确的文件→阶段映射表。

### Issue 003 (MAJOR) — 状态定义与 US 不对齐
**修复方式**：在 US-002 中新增 Scenario "迭代目录存在但 iterations.json 中无记录"，覆盖状态定义中的 Error State 场景。

## Not Fixed (MINOR, deferred)
- Issue 004: P0-P8 文件保护清单
- Issue 005: 迭代名提取规则
