# Design Brief: PowerBy ASP 通用 Review Skill 升级

## 1. Session Metadata

- **会话日期**: 2026-03-31
- **参与者**: 用户（PowerBy 项目负责人）、Claude（产品顾问）
- **会话模式**: Builder mode（基于现有系统升级）
- **参考实现**: gstack review skill
- **输出目标**: design-brief.md → proposal.md → feature-specs

## 2. Original User Input

**用户原始表述**（基于对话历史还原）：

> "gstack的review skill写得非常好，可以充分借鉴。新的powerby-asp-reviewer skill基于gstack review skill升级。"
> 
> 当前 PowerBy ASP 流程已经有了基础的 reviewer skill，但存在以下问题：
> - 只输出审查报告，不提供修复指令
> - 没有自动对齐上游文档的机制
> - 缺少 Confidence 分级和证据链驱动
> - 没有 AUTO-FIX / ASK / ESCALATE 决策系统
> - 缺少多轮 review loop 编排
> 
> 希望参考 gstack reviewer 的优秀实践，升级为一个通用的、智能的、可自动修复的 review 系统。

## 3. Clarification Log

### 3.1 问题定义澄清

**Q1**: 当前 powerby-asp-reviewer 的主要痛点是什么？

**A1**（基于 proposal 推断）:
- 审查后仍需人工理解报告并手动修复
- 无法自动识别当前处于哪个 ASP 阶段
- 没有上游对齐检查，导致基于错误输入做审查
- 缺少智能决策，所有问题都需要人工判断
- 多轮审查没有标准流程，容易陷入无限循环

**Q2**: 为什么选择 gstack review skill 作为参考？

**A2**（基于上下文推断）:
- gstack reviewer 已经实现了 Fix-First 理念
- 有成熟的 Confidence 分级机制（C1-C4）
- 有证据链驱动的修复协议
- 有多轮融合和 Learnings 沉淀机制
- 经过实战验证，效果良好

**Q3**: 升级后的 reviewer 应该覆盖哪些阶段？

**A3**: 
- 产品阶段（design-brief.md, proposal.md, feature-specs）
- 规格阶段（feature-spec-index.md, feature-specs/*.md）
- 架构阶段（architecture.md）
- 计划阶段（tasks.md, implementation-plan.md）
- 实现阶段（代码、测试）

**Q4**: reviewer 和 fixer 的职责边界是什么？

**A4**:
- Reviewer: 只输出审查报告和结构化修复指令，不直接修改文档
- Fixer: 由 ASP 主编排器调度对应的 skill（如 powerby-asp-product）执行修复
- 分离原因：保持职责单一，支持不同阶段使用不同的 fixer

### 3.2 验证目标澄清

**Q5**: 如何验证升级是否成功？

**A5**:
- **定量指标**: review 后一次通过交付率提升
- **质量指标**: 漏需求、漏功能、漏约束的问题数下降
- **效率指标**: Ask 用户次数下降（更多自动修复）
- **流程指标**: 3 轮内收敛率提升

**Q6**: 最小可验证路径是什么？

**A6**:
- 先实现产品阶段的完整 review loop
- 验证阶段识别、上游对齐、决策引擎、修复指令生成
- 再扩展到其他 4 个阶段

### 3.3 现状与复用澄清

**Q7**: PowerBy 项目中已有哪些可复用的能力？

**A7**:
- `docs/consitution.md`: 项目宪法，可作为审查标准
- `docs/asp-document-protocol.md`: ASP 文档协议，定义了文档结构
- `docs/skill-design-protocol.md`: Skill 设计协议，定义了七层结构框架
- 现有的 `powerby-asp-reviewer`: 基础审查能力，需要升级
- 现有的 `powerby-asp-product`: 产品文档生成能力，可作为 fixer

**Q8**: 与 pb-review 体系的关系是什么？

**A8**:
- 两套并行，不做桥接
- ASP 面向 PowerBy 用户群，pb-review 面向通用项目评审
- 不共享 registry 或 data-model
- 独立运行，互不依赖

## 4. Problem Statement

**核心问题**: 当前 PowerBy ASP 流程的 review 环节是"人工驱动"的，reviewer 只输出问题清单，需要人工理解、判断、修复，效率低且容易遗漏。

**具体表现**:
1. **被动审查**: 只在文档完成后审查，无法提前发现上游对齐问题
2. **报告式输出**: 只告诉"有什么问题"，不告诉"怎么修"
3. **人工决策**: 所有问题都需要人工判断是否修复、如何修复
4. **无限循环风险**: 没有标准的多轮收敛机制，可能陷入反复修改
5. **阶段割裂**: 不同阶段的审查逻辑分散，没有统一框架

**影响范围**:
- PowerBy 用户群在使用 ASP 流程时的交付效率
- 文档质量的稳定性和可预测性
- 团队协作的流畅度

## 5. Validation Goal

**验证假设**: 通过引入"自动对齐 → 智能决策 → 指令化修复 → 自动复审"的闭环机制，可以显著提升 ASP 流程的交付效率和质量稳定性。

**验证方式**:
1. **一次通过率**: 统计 review 后无需人工介入即可通过的比例
2. **问题发现率**: 统计漏需求、漏功能、漏约束的问题数
3. **自动修复率**: 统计 AUTO-FIX 成功率 vs ASK/ESCALATE 比例
4. **收敛轮次**: 统计平均收敛轮次（目标 ≤ 3 轮）

**成功标准**:
- 一次通过率 > 80%
- 自动修复率 > 60%
- 平均收敛轮次 ≤ 2 轮
- 用户满意度提升（定性反馈）

## 6. Target User and Status Quo

**目标用户**: PowerBy 用户群，使用 ASP 流程进行产品设计、架构设计和工程实现的开发者

**用户画像**:
- 熟悉 ASP 文档协议
- 希望快速迭代，减少人工审查负担
- 需要高质量的文档输出
- 愿意接受 AI 辅助决策

**当前状态**:
- 使用基础版 powerby-asp-reviewer，只能输出问题清单
- 需要人工阅读审查报告，逐条判断和修复
- 多轮审查没有标准流程，依赖人工判断何时停止
- 不同阶段的审查逻辑分散在不同 skill 中

**期望状态**:
- 触发 review 后，系统自动完成"对齐 → 发现 → 修复 → 复审"全流程
- 只在必要时（C1/C2 问题、超出职责范围）才 ASK 用户
- 3 轮内自动收敛，超过 3 轮自动 ESCALATE
- 所有阶段使用统一的 review 框架

## 7. Success Criteria

### 7.1 功能完整性
- [ ] 支持 5 个 ASP 阶段的自动识别
- [ ] 支持上游对齐链自动恢复
- [ ] 支持 Alignment Summary 前置输出
- [ ] 支持 AUTO-FIX / ASK / ESCALATE 智能决策
- [ ] 支持 Confidence 分级（C1-C4）
- [ ] 支持证据链驱动的修复协议
- [ ] 支持标准 Review Loop（最多 3 轮）
- [ ] 支持结构化修复指令输出

### 7.2 质量标准
- [ ] 遵循 `docs/skill-design-protocol.md` 七层结构框架
- [ ] 遵循 `docs/asp-document-protocol.md` 文档协议
- [ ] 遵循 `docs/consitution.md` 宪法约束
- [ ] SKILL.md 正文不超过 200 行
- [ ] 差异化内容通过 references/ 按需加载

### 7.3 可测试性
- [ ] 每个 Feature 包含完整的 D-17~D-20 测试化字段
- [ ] 决策表可被单元测试验证
- [ ] Review Loop 可被集成测试验证

## 8. Constraints and Non-goals

### 8.1 约束条件
- **CON-001**: 必须遵守 `docs/skill-design-protocol.md` 七层结构框架
- **CON-002**: 必须遵守 `docs/asp-document-protocol.md` 文档协议
- **CON-003**: 必须遵守 `docs/consitution.md` 宪法约束
- **CON-004**: SKILL.md 正文不超过 200 行，差异化内容通过 references/ 按需加载
- **CON-005**: 抽象判断由模型完成，不允许通过脚本外包
- **CON-006**: 与 pb-review 体系完全独立，不共享 registry 或 data-model
- **CON-007**: 不破坏现有 ASP 文档协议和归档结构
- **CON-008**: 面向 PowerBy 用户群，需要足够的泛化程度

### 8.2 明确排除（Non-goals）
- **EXC-001**: 与 pb-review 体系兼容映射（两套并行，不做桥接）
- **EXC-002**: 独立编排器 skill（由 ASP 主流程编排器调度）
- **EXC-003**: CI/CD 自动化集成（超出 skill 范围）
- **EXC-004**: 自动化测试生成（只做测试化检查，不生成测试代码）
- **EXC-005**: P0-P8 兼容（ASP 与旧流程隔离）
- **EXC-006**: 统计面板 / metrics 可视化（后续阶段）
- **EXC-007**: Reviewer 直接修改文档（Reviewer + Fixer 分离）
- **EXC-008**: 脚本化抽象判断（遵循 skill-design-protocol）
- **EXC-009**: 限定特定 AI 后端（协议化，不绑定 Claude/Codex）

## 9. Premises

### 9.1 技术前提
- **P1**: gstack review skill 的 Fix-First 理念可以迁移到 ASP 流程
- **P2**: Confidence 分级（C1-C4）可以有效区分问题的确定性
- **P3**: 证据链驱动可以避免猜测性修复
- **P4**: 3 轮收敛机制可以平衡质量和效率

### 9.2 业务前提
- **P5**: PowerBy 用户群愿意接受 AI 辅助决策
- **P6**: ASP 文档协议足够稳定，不会频繁变更
- **P7**: 现有的 powerby-asp-product 等 skill 可以作为 fixer 使用

### 9.3 资源前提
- **P8**: 有足够的时间完成 5 个阶段的差异化审查清单
- **P9**: 有参考实现（gstack reviewer）可以借鉴

## 10. Alternatives Considered

### 10.1 方案 A：全新独立体系（推荐）

**描述**:
- 创建全新的 `powerby-asp-reviewer` skill
- 参考 gstack reviewer 的核心理念，但不直接复制代码
- 1 个通用 skill 覆盖 5 个阶段，通过 references/ 差异化配置
- Reviewer + Fixer 分离，由 ASP 主编排器调度

**优点**:
- 独立运行，不引入 pb-review 的复杂依赖
- 可以针对 ASP 流程深度优化
- 架构清晰，易于维护和扩展
- 符合 PowerBy 的 skill 设计协议

**缺点**:
- 需要从零开始设计决策表和审查清单
- 初期开发工作量较大
- 需要时间验证效果

**工作量**: 中等（约 2-3 周）

### 10.2 方案 B：直接复用 pb-review 体系

**描述**:
- 将 pb-review 的 reviewer skill 适配到 ASP 流程
- 复用 pb-review 的 registry 和 data-model
- 通过适配层桥接两套体系

**优点**:
- 可以快速启动，复用现有能力
- pb-review 已经过验证，稳定性高

**缺点**:
- 引入 pb-review 的复杂依赖，增加维护成本
- pb-review 面向通用项目评审，不一定适合 ASP 流程
- 两套体系的概念模型不一致，适配成本高
- 违反 CON-006 约束

**工作量**: 小（约 1 周），但长期维护成本高

### 10.3 方案 C：最小可验证路径（MVP）

**描述**:
- 先只实现产品阶段的 review loop
- 验证核心机制（阶段识别、对齐、决策、修复指令）
- 再逐步扩展到其他 4 个阶段

**优点**:
- 快速验证核心假设
- 降低初期风险
- 可以根据反馈调整方向

**缺点**:
- 初期只能覆盖产品阶段，其他阶段仍需人工审查
- 可能需要后续重构以支持全阶段

**工作量**: 小（约 1 周）

## 11. Recommended Direction

**推荐方案**: 方案 A（全新独立体系） + 方案 C（最小可验证路径）的组合

**理由**:
1. **独立性**: 与 pb-review 并行，不引入复杂依赖，符合 CON-006 约束
2. **可扩展性**: 1 个通用 skill + references/ 差异化配置，易于扩展到 5 个阶段
3. **风险可控**: 先实现产品阶段 MVP，验证核心机制后再扩展
4. **参考成熟**: 借鉴 gstack reviewer 的优秀实践，但针对 ASP 流程深度优化
5. **架构清晰**: Reviewer + Fixer 分离，职责单一，易于维护

**实施路径**:
1. **Phase 1（MVP）**: 实现产品阶段的完整 review loop
   - 阶段识别（只识别产品阶段）
   - 上游对齐（design-brief.md → proposal.md）
   - 决策引擎（AUTO-FIX / ASK / ESCALATE）
   - 修复指令生成
   - Review Loop（最多 3 轮）
2. **Phase 2（扩展）**: 扩展到其他 4 个阶段
   - 补充 5 个阶段的差异化审查清单
   - 完善阶段识别逻辑
   - 完善上游对齐链
3. **Phase 3（优化）**: 根据实际使用反馈优化
   - 调整决策表
   - 优化审查清单
   - 提升自动修复率

## 12. Handoff to Proposal

### 12.1 应继承的目标
- 把 ASP review 从"输出审查报告"升级为"自动对齐 → 自动发现 → 指令化修复 → 自动复审 → 无异常交付"的质量闭环系统

### 12.2 成功验证方式
- **定量指标**: review 后一次通过交付率提升
- **质量指标**: 漏需求、漏功能、漏约束的问题数下降
- **效率指标**: Ask 用户次数下降
- **流程指标**: 3 轮内收敛率提升

### 12.3 关键指标
- 一次通过率 > 80%
- 自动修复率 > 60%
- 平均收敛轮次 ≤ 2 轮

### 12.4 明确排除
- 与 pb-review 体系兼容映射
- 独立编排器 skill
- CI/CD 自动化集成
- 自动化测试生成
- P0-P8 兼容
- 统计面板 / metrics 可视化
- Reviewer 直接修改文档
- 脚本化抽象判断
- 限定特定 AI 后端

### 12.5 现有能力复用线索
- `docs/consitution.md`: 作为审查标准
- `docs/asp-document-protocol.md`: 定义文档结构
- `docs/skill-design-protocol.md`: 定义 skill 结构
- 现有的 `powerby-asp-product`: 作为产品阶段的 fixer
- gstack reviewer: 作为核心理念参考

### 12.6 推荐实施路径
- 先实现产品阶段 MVP（Phase 1）
- 验证核心机制后扩展到其他 4 个阶段（Phase 2）
- 根据反馈优化（Phase 3）

### 12.7 下一步行动
1. 基于本 design-brief.md 创建 `proposal.md`
2. 定义 19 个需求（REQ-001 到 REQ-019）
3. 创建 `feature-spec-index.md` 和 `feature-specs/*.md`
4. 进入产品文档审查流程

---

**Design Brief 完成时间**: 2026-03-31
**下游交接**: powerby-asp-product
**预计 Proposal 完成时间**: 2026-03-31
