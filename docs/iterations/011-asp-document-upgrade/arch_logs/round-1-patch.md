# Round 1 修复记录

**修复日期**: 2026-03-30
**修复人**: powerby-asp-architect (Refinery Mode)
**修复轮次**: Round 1

---

## 修复的问题

### MAJOR-001: C-04 组件输出缺少 traceability-matrix.md
**问题描述**: C-04 (visualizer) 输出列表仅包含 product-map.md 和 testability-scorecard.md，但 FT-005 (traceability-matrix.md) 映射到 C-04，数据流图也显示三个产出物。

**修复措施**:
- C-04 输出更新为 `product-map.md, traceability-matrix.md, testability-scorecard.md`
- C-04 职责更新为"生成产品全景图、追溯矩阵和测试化评分卡"
- C-04 输入移除 traceability-matrix.md（它是产出物，不是输入）
- C-04 核心变更描述同步更新
- 影响文件：architecture.md Section 3.2 C-04 定义

### MAJOR-002: C-02B 输入列表包含 traceability-matrix.md，违反阶段顺序
**问题描述**: reviewer 在 REFINING 阶段运行，traceability-matrix.md 在 VISUALIZING 阶段才生成，REFINING 在 VISUALIZING 之前。

**修复措施**:
- 从 C-02B 输入列表中移除 traceability-matrix.md
- 同步更新 Section 5.3 文档传递表中 visualizer 的输入（移除 traceability-matrix.md）
- 影响文件：architecture.md Section 3.2 C-02B 定义、Section 5.3

### MINOR-001: Section 7.2 复用比例计数错误
**问题描述**: 写的是"扩展 3 + 重构 7 + 全新 3 + 验证 2"，但表格实际是扩展 3 + 重构 9 + 全新 3。

**修复措施**:
- 修正为"扩展 3 个 + 重构 9 个 + 全新 3 个"
- 影响文件：architecture.md Section 7.2

---

## 修复后状态

- ✅ C-04 输出列表完整（product-map.md + traceability-matrix.md + testability-scorecard.md）
- ✅ C-02B 输入不包含 VISUALIZING 阶段产物
- ✅ 复用比例计数正确（3 + 9 + 3 = 15）
- ✅ 数据流图与组件定义一致

---

**修复状态**: 完成
**下一步**: 等待 Round 2 审查
