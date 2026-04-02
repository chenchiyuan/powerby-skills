# Round 2 Patch Notes

**Date**: 2026-03-30
**架构版本**: 1.1.0 → 1.2.0

---

## 修复清单

### R2-MAJOR-001: 统一 4 种新 gap 的归档目标

**问题**: gap_registry 和 difference_registry 引用不一致。§5.5 已改为 gap_registry，但 report-composer 输入、数据流时序图、写入流图、追溯矩阵仍引用 difference_registry。

**修复内容**（全文搜索替换）:
1. §3.2.3 report-composer 输入：`difference_registry` → `gap_registry`
2. §3.2.3 testability-scorecard 输入数据：`difference_registry` → `gap_registry`
3. §4.1 时序图 GA→RC 消息：`difference_registry (含 4 种 gap)` → `gap_registry (含 4 种 gap) + difference_registry`
4. §4.3 写入流图：`difference_registry (4 种 gap)` → `gap_registry (4 种测试化 gap)`
5. §7.1 追溯矩阵 FP-002 交付物：`difference_registry 扩展` → `gap_registry 扩展`

### R2-MAJOR-002: 统一 Step 13~16 的执行归属

**问题**: §3.2.4 声明 Step 13~16 不加载 report-composer，但 §3.2.3、组件图、deliverable_manifest、FP→组件矩阵仍将 4 个新交付物归属 report-composer。

**修复内容**:
1. §3.2.3 report-composer：FP 缩减为仅 FP-003，移除 4 个新报告的模板/脚本描述，降级为轻度升级
2. §3.2.4 编排器：FP 扩展为 FP-009~013，新增 4 模板 + 4 脚本的描述，升级为重度升级
3. §5.6 deliverable_manifest：producer_skill 从 `pb-review-report-composer` → `pb-review`
4. §7.1 追溯矩阵：FP-009~012 主组件从 `report-composer` → `pb-review (编排器)`
5. §3.1 组件总览表：同步更新变更类型和 FP 归属
6. §6.1 组件关系图：RC 标注改为 `FP-003`，PBR 标注改为 `FP-009~013`，PBR 样式升为红色
7. §6.2 文件变更清单：4 个新模板/脚本从 `report-composer/` → `pb-review/`
8. §2.2 Schema 引用表：引用 Skill 从 `report-composer` → `pb-review (编排器 Step N)`

**设计决策**: 4 个渲染脚本和模板物理归属 `skills/pb-review/` 目录（编排器），而非 `skills/pb-review-report-composer/` 目录。这与 Step 13~16 的确定性执行模型一致（编排器直调脚本，不加载 Skill）。
