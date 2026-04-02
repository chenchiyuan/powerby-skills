# Round 4 修复记录

**修复日期**: 2026-03-30
**修复人**: powerby-asp-product (Refinery Mode)
**修复轮次**: Round 4

---

## 修复的问题

### BLOCKER-001: FT-008~FT-013 未规格化"七层结构"要求
**问题描述**: 6 张 skill 类规格卡只描述运行行为或产物，没有把"SKILL.md 遵循七层结构/通过十条原则 checklist"写成验收规格。

**修复措施**:
- 为 FT-008~FT-013 每个规格卡添加 SKILL.md 结构模板（D-04）
- 添加七层结构异常检查（D-05: MISSING_SECTION, INVALID_STRUCTURE）
- 后置条件（D-07）加入"SKILL.md 遵循七层结构"和"通过十条原则 checklist"
- 测试组（D-19）加入"七层结构校验（11 用例）"和"十条原则 checklist（10 用例）"
- 复用 FT-007 的规格化模式
- 影响文件：FT-008.md, FT-009.md, FT-010.md, FT-011.md, FT-012.md, FT-013.md

### MAJOR-002: FT-014 测试覆盖状态矛盾
**问题描述**: FT-014 的覆盖状态为"✅ 已覆盖"但测试文件为"待补充"，与覆盖率 0% 矛盾。

**修复措施**:
- 将 FT-014 覆盖状态从"✅ 已覆盖"改为"⚠️ 部分覆盖"
- 统一所有 Feature 的覆盖状态口径

### MAJOR-003: traceability-matrix.md 尾部阶段指向不正确
**问题描述**: 文档尾部仍写"下一步：进入 VISUALIZING 阶段"，但文档本身是 VISUALIZING 阶段产物。

**修复措施**:
- 删除"下一步"字段，替换为"阶段归属: VISUALIZING 阶段产出"

### MAJOR-004: REQ-013 名称错误
**问题描述**: traceability-matrix.md 将 REQ-013 / FT-013 错写成 powerby-asp-codex-reviewer。

**修复措施**:
- 更正为 powerby-asp-arch-codex-reviewer
- 同步更新 feature-spec-index.md 和 traceability-matrix.md

### MINOR-005: FT-007 "可能新增"模糊措辞
**问题描述**: FT-007 D-08 副作用使用"可能新增"不符合意图清晰原则。

**修复措施**:
- 改为"新增 references/ 和 scripts/ 目录（如有确定性工作或领域知识需分层）"

---

## 同步更新
- feature-spec-index.md: FT-008~FT-013 测试组数已更新
- traceability-matrix.md: FT-008~FT-013 测试组数已更新，FT-009 名称已更正

---

## 修复后状态

- ✅ 所有 skill 类规格卡包含七层结构验收规格
- ✅ 测试覆盖状态口径一致
- ✅ 阶段归属明确
- ✅ REQ-013 名称正确
- ✅ 无模糊措辞

---

**修复状态**: 完成
**下一步**: 等待 Round 5 审查
