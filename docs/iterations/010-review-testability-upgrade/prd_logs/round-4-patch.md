# Round 4 Patch Notes

**Date**: 2026-03-30
**修复范围**: MAJOR #001~#004

## 修复清单

| Issue ID | 修复内容 |
|----------|---------|
| #001 (MAJOR) | US-013 显式定义标准 8 个必需测试组（TG-1~TG-8: 正向功能、边界条件、异常/错误路径、数据验证、状态转换、并发/竞态、性能基线、集成契约），每组有编号、名称和描述; render_test_case_index.py 输入明确包含理想测试组定义; 不适用的组标记为 not_applicable; 缺口分析按组逐项对比; 优先级建议明确 P0 顺序 |
| #002 (MAJOR) | 新增 dependency_registry 数据结构定义: 包含 function_id、dependency_name、dependency_type(api/database/cache/message_queue/file_system)、has_mock(boolean)、mock_evidence_refs、mock_strategy(stub/fake/spy/mock_server/not_needed)、mock_priority(high/medium/low); 更新 Data Flow 中 dependency-reconstructor 输出描述; 明确 render_fixture_contract.py 从 dependency_registry 读取 Mock 策略信息 |
| #003 (MAJOR) | 状态表补充 Loading State 列: D-17("评估中: 正在扫描代码证据...")、D-18("评估中: 正在扫描测试代码...")、D-19("统计中: 正在识别测试分组...")、D-20("判定中: 正在检查 8 项条件...")、Scorecard("生成中: 正在计算 M-01~M-07...") |
| #004 (MAJOR) | Data Dictionary 从 12 项扩展到 30 项, 补充: entry_surface_inventory、feature_spec_registry、feature_state_registry、dependency_registry、implementation_registry、difference_registry、traceability_matrix、product_docs_dir、existing_test_count、coverage_scope、blocking_reasons、uncovered_sub_capabilities、unclosed_assertion_points、unstandardized_fixtures、mock_strategy、test_mapping、test_level、deliverable_manifest |

## 版本变更
spec.md 版本从 1.2.0 升级到 1.3.0
