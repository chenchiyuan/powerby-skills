# Round 1 Patch Notes

**Date**: 2026-03-30
**修复范围**: MAJOR #001~#004

## 修复清单

| Issue ID | 修复内容 |
|----------|---------|
| #001 | D-17 评估粒度对齐: US-001 已从 3 个子项改为基于标准 9 个子项评估, 新增"不适用子项不计入分母"规则, 完整度计算公式更新 |
| #002 | blocked 判定条件补全: US-001 blocked Scenario 已包含完整的 3 个 OR 条件（D17-9 缺失 OR D17-1 缺失 OR oracle_completeness < 50） |
| #003 | 新增 Data Flow 章节: 定义了 feature_spec_registry 的 D-17~D-20 扩展字段结构, 明确了 skill 间数据流转路径（project-scope -> feature-reconstructor -> dependency-reconstructor -> implementation-mapper -> relation-builder -> gap-analyzer -> report-composer） |
| #004 | Renderer script 归属明确: 4 个新报告的 renderer script 统一归属 pb-review-report-composer skill, 分别为 render_testability_scorecard.py, render_test_case_index.py, render_fixture_contract.py, render_oracle_matrix.py |

## 同步更新

- US-002 D-18 评估粒度同步对齐为标准 6 个子项（提前修复 MINOR #005）
- Data Dictionary 新增 d17_sub_item_status, d18_sub_item_status 术语
- 状态定义表中 blocked 条件更新为包含 D17-9 和 D17-1 检查
- US-012~015 明确指定了各自的 renderer script 名称
- US-016 工作流步骤表新增 renderer script 列
- spec.md 版本从 1.0.0 升级到 1.1.0
