# Function Points: PowerBy Architecture Design (架构设计流程)

**版本**: v1.0.0
**基于**: proposal.md (Proposal Lock)
**功能点总数**: 12（10 必须 + 2 应该）

---

## 功能点总览

| FP | 功能点名称 | 对应 REQ | 优先级 | 所属 Epic |
|----|-----------|---------|--------|----------|
| FP-001 | 架构师角色定义 | REQ-001 | 必须 | Epic 1 |
| FP-002 | 苏格拉底式架构澄清 | REQ-002 | 必须 | Epic 1 |
| FP-003 | 多轮架构审查机制 | REQ-003 | 必须 | Epic 2 |
| FP-004 | 宪法符合性审查 | REQ-004 | 必须 | Epic 2 |
| FP-005 | 双向覆盖检查 | REQ-005 | 必须 | Epic 2 |
| FP-006 | 复用现有 Skill 协议 | REQ-006 | 必须 | Epic 3 |
| FP-007 | 接口/协议规范定义 | REQ-007 | 必须 | Epic 3 |
| FP-008 | 用户触发的独立流程 | REQ-008 | 必须 | Epic 1 |
| FP-009 | 架构可视化 | REQ-009 | 必须 | Epic 4 |
| FP-010 | 架构变更标注 | REQ-010 | 必须 | Epic 4 |
| FP-011 | 技术选型对比流程 | REQ-011 | 应该 | Epic 5 |
| FP-012 | Codex 自动化审查 | REQ-012 | 应该 | Epic 5 |

---

## 功能点详情

### Epic 1: 架构师角色与流程编排

**FP-001 | 架构师角色定义** (REQ-001, 必须)
- 定义 Architect Agent，基于已交付产品文档产出 architecture.md
- 输入：proposal.md、spec.md、function-points.md、product-map.md、constitution.md
- 输出：architecture.md（系统架构、组件划分、数据流、接口/协议定义）
- 验收：architecture.md 包含完整架构内容，每个组件可追溯到功能点

**FP-002 | 苏格拉底式架构澄清** (REQ-002, 必须)
- 正式设计前通过多轮提问穷尽架构疑问（选型、边界、约束、风险）
- 不限轮次，以"没有疑问"为结束条件
- 前期充分沟通，减少后期返工
- 验收：所有架构疑问在设计前解决，澄清记录可追溯

**FP-008 | 用户触发的独立流程** (REQ-008, 必须)
- 产品文档交付后由用户主动触发，独立于产品 ASP 流程
- 启动前校验产品文档完整性
- 验收：流程通过独立命令触发，不与产品 ASP 耦合

### Epic 2: 架构审查机制

**FP-003 | 多轮架构审查机制** (REQ-003, 必须)
- 最多 5 轮，默认序列 [Claude, Codex, Claude, Codex, Claude]
- 每轮全面审查，支持用户自定义序列
- 包含：上下文隔离、历史记录传递、修复流程（Refinery Mode）、ESCALATION
- 验收：审查报告独立存储，STATUS 为 PASS/FAIL

**FP-004 | 宪法符合性审查** (REQ-004, 必须)
- 检查架构是否符合 constitution.md 原则
- 覆盖：SOLID、DRY、奥卡姆剃刀、演进式架构、组合优于继承等
- 验收：审查报告包含宪法符合性检查结果，引用具体条款

**FP-005 | 双向覆盖检查** (REQ-005, 必须)
- 正向覆盖：function-points.md 每个 FP 在架构中有对应设计
- 反向溢出：架构不能多设计（超出需用户审批）
- 排除项入侵：架构不能包含 EXC 排除的功能
- 验收：审查报告包含 Coverage Matrix

### Epic 3: Skill 基础设施

**FP-006 | 复用现有 Skill 协议** (REQ-006, 必须)
- 架构/审查 Skill 参考 powerby-asp-reviewer 等现有 Skill 格式
- frontmatter + Markdown 正文，机器可读输出
- 验收：Skill 文件格式一致，注册到 marketplace.json

**FP-007 | 接口/协议规范定义** (REQ-007, 必须)
- 架构中定义 API 契约、数据结构、服务间通信协议
- 禁止生成任何业务代码
- 验收：architecture.md 包含接口/协议章节，不含业务代码

### Epic 4: 架构可视化与变更管理

**FP-009 | 架构可视化** (REQ-009, 必须)
- 使用 Mermaid + Markdown 产出架构图（组件图、数据流图）
- Mermaid 语法校验（最多 3 次自动修复）
- 验收：架构图语法正确，清晰易读

**FP-010 | 架构变更标注** (REQ-010, 必须)
- 架构图中标注新增/变更部分
- 使用颜色或标记突出显示
- 验收：变更部分有显著视觉标记

### Epic 5: 增强功能

**FP-011 | 技术选型对比流程** (REQ-011, 应该)
- 架构交付后列举选型方案（方案、优点、缺点、推荐理由）
- 用户确认后重新进入架构+review 环节
- 验收：选型对比以结构化表格呈现

**FP-012 | Codex 自动化审查** (REQ-012, 应该)
- Codex 轮次通过 codex exec -s read-only 自动执行
- 失败时生成错误报告保持审查链完整
- 验收：Codex 审查自动执行，输出格式一致
