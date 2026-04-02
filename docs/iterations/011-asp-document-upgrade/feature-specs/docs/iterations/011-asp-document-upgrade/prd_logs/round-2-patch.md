# Round 2 修复记录

**修复日期**: 2026-03-30
**修复人**: powerby-asp-product (Refinery Mode)
**修复轮次**: Round 2

---

## 修复的问题

### BLOCKER-001: 违反分阶段组装原则
**问题描述**: 所有 15 个规格卡已填写 D-15/D-16（依赖关系、实现映射），违反 CON-003 约束。

**修复措施**:
- 删除所有规格卡的 D-15/D-16 章节
- 替换为统一标记：`## D-09~D-16: 扩展维度` + `**待架构阶段补充**`
- 影响文件：FT-001.md ~ FT-015.md（15 个文件）

### MAJOR-002: feature-spec-index.md 测试组数不一致
**问题描述**: 索引表测试组数全为 0，但规格卡已定义测试组。

**修复措施**:
- 更新 feature-spec-index.md 的测试组数列，从规格卡的 D-19 提取实际值
- FT-001~FT-013, FT-015: 4-5 组
- FT-014: 8 组（唯一 Test Ready）
- 更新状态统计：Test Ready 状态从 0 改为 1

### MAJOR-003: traceability-matrix.md 阶段归属矛盾
**问题描述**: FT-005 定义为 REFINING 阶段产物，但 FT-014 和 FT-006 将其列为 VISUALIZING 阶段。

**修复措施**:
- 修正 FT-005.md：入口路径从 `REFINING 阶段产出` 改为 `VISUALIZING 阶段产出`
- 更新 traceability-matrix.md：下一步从 `进入 REFINING 阶段` 改为 `进入 VISUALIZING 阶段`

### MAJOR-004: 测试覆盖率统计口径不一致
**问题描述**: traceability-matrix.md 声称 Feature 测试覆盖率 6.7% (1/15)，但统计口径不明确。

**修复措施**:
- 明确统计口径：Feature 测试覆盖率 = 测试文件已落地的功能数 / 功能总数
- 当前所有功能测试文件均为"待补充"，因此覆盖率应为 0% (0/15)
- 添加说明章节，区分"测试覆盖率"和"Test Ready 占比"

---

## 修复后状态

- ✅ 所有规格卡符合分阶段组装原则
- ✅ feature-spec-index.md 与规格卡数据一致
- ✅ traceability-matrix.md 阶段归属明确
- ✅ 测试覆盖率统计口径清晰

---

**修复状态**: 完成
**下一步**: 等待 Round 3 审查
