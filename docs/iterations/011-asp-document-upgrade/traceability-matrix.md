# 追溯矩阵

**迭代编号**: 011
**项目名称**: asp-document-upgrade
**生成日期**: 2026-03-30
**状态**: Final

---

## 1. REQ → Feature 映射

| REQ ID | 需求描述 | Feature ID | 功能名称 | 覆盖状态 |
|--------|---------|-----------|---------|---------|
| REQ-001 | ASP 文档协议标准更新 | FT-001 | ASP 文档协议标准更新 | ✅ 已覆盖 |
| REQ-002 | proposal.md 格式升级 | FT-002 | proposal.md 格式升级 | ✅ 已覆盖 |
| REQ-003 | feature-spec-index.md 替代 function-points.md | FT-003 | feature-spec-index.md 生成 | ✅ 已覆盖 |
| REQ-004 | feature-specs/*.md 分阶段组装机制 | FT-004 | feature-specs 分阶段组装 | ✅ 已覆盖 |
| REQ-005 | traceability-matrix.md | FT-005 | traceability-matrix.md 生成 | ✅ 已覆盖 |
| REQ-006 | testability-scorecard.md | FT-006 | testability-scorecard.md 生成 | ✅ 已覆盖 |
| REQ-007 | 重写 powerby-asp-product | FT-007 | powerby-asp-product 重写 | ✅ 已覆盖 |
| REQ-008 | 重写 powerby-asp-reviewer | FT-008 | powerby-asp-reviewer 重写 | ✅ 已覆盖 |
| REQ-009 | 重写 powerby-asp-codex-reviewer | FT-009 | powerby-asp-codex-reviewer 重写 | ✅ 已覆盖 |
| REQ-010 | 重写 powerby-asp-visualizer | FT-010 | powerby-asp-visualizer 重写 | ✅ 已覆盖 |
| REQ-011 | 重写 powerby-asp-architect | FT-011 | powerby-asp-architect 重写 | ✅ 已覆盖 |
| REQ-012 | 重写 powerby-asp-arch-reviewer | FT-012 | powerby-asp-arch-reviewer 重写 | ✅ 已覆盖 |
| REQ-013 | 重写 powerby-asp-arch-codex-reviewer | FT-013 | powerby-asp-arch-codex-reviewer 重写 | ✅ 已覆盖 |
| REQ-014 | 流程产出升级 | FT-014 | ASP 流程产出升级 | ✅ 已覆盖 |
| REQ-015 | 更新 asp-document-protocol.md | FT-015 | asp-document-protocol.md 更新 | ✅ 已覆盖 |

---

## 2. Feature → Test 映射

| Feature ID | 功能名称 | Test Case Groups | 测试文件 | 覆盖状态 |
|-----------|---------|-----------------|---------|---------|
| FT-001 | ASP 文档协议标准更新 | 4 | `tests/test_asp_document_upgrade.py::test_asp_document_protocol_upgraded_to_v1_1_0` | ✅ 已覆盖 |
| FT-002 | proposal.md 格式升级 | 4 | `tests/test_asp_document_upgrade.py::test_iteration_011_proposal_includes_reuse_analysis_section` | ✅ 已覆盖 |
| FT-003 | feature-spec-index.md 生成 | 5 | `tests/test_asp_document_upgrade.py::test_iteration_011_feature_index_and_feature_specs_follow_protocol` | ✅ 已覆盖 |
| FT-004 | feature-specs 分阶段组装 | 5 | `tests/test_asp_document_upgrade.py::test_iteration_011_feature_index_and_feature_specs_follow_protocol` | ✅ 已覆盖 |
| FT-005 | traceability-matrix.md 生成 | 5 | `tests/test_asp_document_upgrade.py::test_iteration_011_visualizer_artifacts_are_consistent` | ✅ 已覆盖 |
| FT-006 | testability-scorecard.md 生成 | 4 | `tests/test_asp_document_upgrade.py::test_iteration_011_scorecard_formula_and_grade_are_consistent` | ✅ 已覆盖 |
| FT-007 | powerby-asp-product 重写 | 4 | `tests/test_asp_document_upgrade.py::test_product_line_skills_use_new_document_protocol` | ✅ 已覆盖 |
| FT-008 | powerby-asp-reviewer 重写 | 7 | `tests/test_asp_document_upgrade.py::test_product_line_skills_use_new_document_protocol` | ✅ 已覆盖 |
| FT-009 | powerby-asp-codex-reviewer 重写 | 6 | `tests/test_asp_document_upgrade.py::test_product_line_skills_use_new_document_protocol` | ✅ 已覆盖 |
| FT-010 | powerby-asp-visualizer 重写 | 6 | `tests/test_asp_document_upgrade.py::test_iteration_011_visualizer_artifacts_are_consistent` | ✅ 已覆盖 |
| FT-011 | powerby-asp-architect 重写 | 6 | `tests/test_asp_document_upgrade.py::test_architecture_line_skills_use_feature_specs_instead_of_legacy_function_points` | ✅ 已覆盖 |
| FT-012 | powerby-asp-arch-reviewer 重写 | 7 | `tests/test_asp_document_upgrade.py::test_architecture_line_skills_use_feature_specs_instead_of_legacy_function_points` | ✅ 已覆盖 |
| FT-013 | powerby-asp-arch-codex-reviewer 重写 | 6 | `tests/test_asp_document_upgrade.py::test_architecture_line_skills_use_feature_specs_instead_of_legacy_function_points` | ✅ 已覆盖 |
| FT-014 | ASP 流程产出升级 | 8 | `tests/test_asp_document_upgrade.py::test_iteration_011_visualizer_artifacts_are_consistent` | ✅ 已覆盖 |
| FT-015 | asp-document-protocol.md 更新 | 5 | `tests/test_asp_document_upgrade.py::test_asp_document_protocol_upgraded_to_v1_1_0` | ✅ 已覆盖 |

---

## 3. 覆盖率统计

- **REQ 覆盖率**: 100% (15/15)
- **Feature 测试覆盖率**: 100% (15/15)
- **Test Ready 功能占比**: 6.7% (1/15)

**说明**：
- Feature 测试覆盖率 = 已映射测试文件的功能数 / 功能总数
- Test Ready 功能占比 = 测试组数 ≥8 的功能数 / 功能总数

---

## 4. 未覆盖项

### 4.1 未覆盖的 REQ
- 无

### 4.2 未达到 Test Ready 的 Feature
- FT-001: 测试组数 < 8
- FT-002: 测试组数 < 8
- FT-003: 测试组数 < 8
- FT-004: 测试组数 < 8
- FT-005: 测试组数 < 8
- FT-006: 测试组数 < 8
- FT-007: 测试组数 < 8
- FT-008: 测试组数 < 8
- FT-009: 测试组数 < 8
- FT-010: 测试组数 < 8
- FT-011: 测试组数 < 8
- FT-012: 测试组数 < 8
- FT-013: 测试组数 < 8
- FT-015: 测试组数 < 8

---

**文档状态**: Final
**阶段归属**: VISUALIZING 阶段产出
