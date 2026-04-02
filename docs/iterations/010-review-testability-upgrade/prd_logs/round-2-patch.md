# Round 2 Patch Notes

**Date**: 2026-03-30
**修复范围**: BLOCKER #001, MAJOR #002~#005, MINOR #006(部分)

## 修复清单

| Issue ID | 修复内容 |
|----------|---------|
| #001 (BLOCKER) | US-008 补充产品目录完整度总评分公式: (Goal可量化率 + Scenario完整率 + Constraint可追踪率) / 3, 新增等级判定(A/B/C/D), 新增产品文档缺失降级场景 |
| #002 (MAJOR) | D-20 对齐标准 3.5 全部 8 项判定条件: 新增 test_case_group_count >= 8、错误码测试覆盖、边界条���测试覆盖等; d20_coverage_claim 数据结构新增 coverage_scope、unclosed_assertion_points、unstandardized_fixtures 字段; 未达标场景输出三类缺失清单 |
| #003 (MAJOR) | US-010 从 Feature->TestFile(文件级) 提升为 Feature->ExistingTest(函数级): 每个映射包含 test_file、test_function_name、test_level; 新增无测试场景; Data Flow 同步更新 |
| #004 (MAJOR) | testability_score 口径消歧: 显式声明采用 pb-review-standard.md 4.1 公式为唯一口径, 列出完整 7 项权重公式 |
| #005 (MAJOR) | Renderer Script 输入字段名统一为 schema 定义的全名: d17_oracle、d18_fixture、d19_test_groups(而非缩写 d17/d18/d19) |
| #006 (MINOR) | 修复乱码字符: 3 处 Unicode 损坏已修复 |

## 版本变更
spec.md 版本从 1.1.0 升级到 1.2.0
