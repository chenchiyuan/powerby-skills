# Round 2 修复记录

**修复日期**: 2026-03-30
**修复人**: powerby-asp-architect (Refinery Mode)
**修复轮次**: Round 2

---

## 修复的问题

### MAJOR-R2-001: traceability-matrix.md 产出描述全局不一致
**问题描述**: Round 1 修复只改了 C-04 组件定义表，但 Section 2.2（复用能力表）和 Phase 4（阶段说明）仍遗漏 traceability-matrix.md。

**修复措施**:
- Section 2.2 powerby-asp-visualizer 变更点：更新为"输出 product-map.md + traceability-matrix.md + testability-scorecard.md"
- Phase 4 可视化 Skill 说明：更新为"产出扩展为 product-map.md + traceability-matrix.md + testability-scorecard.md"
- 影响文件：architecture.md Section 2.2、Section 6.2

### MAJOR-R2-002: 分阶段组装阶段边界自相矛盾
**问题描述**: Section 4.3 标注"Gate 2 后"进入架构阶段，但 Gate 2 在 VISUALIZING 后才触发，而 C-03A 实际只依赖产品规格文档。

**修复措施**:
- Section 4.3 Mermaid 图中"Gate 2 后"改为"产品 CONFIRMATION 后"，明确是产品流程的 CONFIRMATION 阶段（即 Gate 2）通过后才启动架构阶段
- 这与 C-03A 的输入定义一致：architect 依赖的是产品阶段的最终确认产出（proposal.md + feature-spec-index.md + feature-specs/*.md），而非 Gate 2 本身的产物
- 影响文件：architecture.md Section 4.3

### MINOR-R2-001: 组件"对应 Feature"字段不完整
**问题描述**: C-01 只列 FT-001/FT-015，C-02A 只列 FT-007，C-04 只列 FT-010，但 Section 7.1 映射更多 Feature。

**修复措施**:
- C-01 对应 Feature：FT-001, FT-015 → FT-001, FT-004, FT-015
- C-02A 对应 Feature：FT-007 → FT-002, FT-003, FT-004, FT-007
- C-04 对应 Feature：FT-010 → FT-005, FT-006, FT-010
- 影响文件：architecture.md Section 3.2

### MINOR-R2-002: Refinery 产物未建模
**问题描述**: round-N-patch.md 在时序图中出现但未进入组件输出和文档传递协议。

**修复措施**:
- C-02A 输出增加 `prd_logs/round-{N}-patch.md`
- C-03A 输出增加 `arch_logs/round-{N}-patch.md`
- Section 5.3 文档传递协议增加两行 patch.md 传递（产品线和架构线各一行）
- 影响文件：architecture.md Section 3.2、Section 5.3

---

## 修复后状态

- ✅ traceability-matrix.md 在所有章节一致出现（Section 2.2、3.2、4.1、6.2）
- ✅ 阶段边界标注与实际流程一致（"产品 CONFIRMATION 后"启动架构阶段）
- ✅ 组件"对应 Feature"反映完整映射
- ✅ patch.md 进入组件输出契约和文档传递协议

---

**修复状态**: 完成
**下一步**: 等待 Round 3 审查
