# Proposal: PowerBy ASP 通用 Review Skill 升级

## 0. Upstream Design Input

- **来源文档**: `design-brief.md`
- **目标摘要**: 把 ASP review 从"输出审查报告"升级为"自动对齐 → 自动发现 → 指令化修复 → 自动复审 → 无异常交付"的质量闭环系统
- **验证方式**: 
  - 定量指标：review 后一次通过交付率提升
  - 质量指标：漏需求、漏功能、漏约束的问题数下降
  - 效率指标：Ask 用户次数下降
  - 流程指标：3 轮内收敛率提升
- **推荐方向**: 全新独立体系（参考 gstack reviewer）+ 最小可验证路径（先实现产品阶段 MVP）
- **关键指标**:
  - 一次通过率 > 80%
  - 自动修复率 > 60%
  - 平均收敛轮次 ≤ 2 轮

## 1. 产品定位
- **目标用户**：PowerBy 用户群，使用 ASP 流程进行产品设计、架构设计和工程实现的开发者
- **核心价值**：把 ASP review 从"输出审查报告"升级为"自动对齐 → 自动发现 → 指令化修复 → 自动复审 → 无异常交付"的质量闭环系统
- **成功指标**：review 后一次通过交付率提升；漏需求、漏功能、漏约束的问题数下降；Ask 用户次数下降

## 2. 需求清单
| ID | 需求描述 | 优先级 | 验收标准（草案） |
|----|---------|--------|----------------|
| REQ-001 | 通用 ASP Reviewer Skill：1 个 skill 覆盖 5 个阶段，遵循七层结构框架，只输出审查报告和修复指令，不修改文档 | 必须 | skill 能被 ASP 主编排器调度，输出符合统一报告模板的审查报告 |
| REQ-002 | 阶段自动识别：根据迭代目录内容自动判断所处阶段（产品/规格/架构/计划/实现） | 必须 | 给定迭代目录，能正确识别 5 个阶段，输出"当前阶段 / 审查对象 / 上游事实源" |
| REQ-003 | 上游对齐链恢复：按阶段自动读取上游产物链 | 必须 | 每个阶段能自动读取对应上游产物，缺失上游时按规则处理（FAIL 或 ASK） |
| REQ-004 | Alignment Summary 前置：每次 review 必须先输出对齐摘要 | 必须 | 每份审查报告以 Alignment Summary 开头，未通过对齐时 Status 不能为 PASS |
| REQ-005 | 五阶段差异化审查清单：每个阶段有独立的 references/ 审查清单 | 必须 | 每个阶段有独立审查清单文件，至少覆盖 3 个差异化检查维度 |
| REQ-006 | AI Reviewer 协议化：不限定后端审查员，遵循统一 I/O 协议 | 必须 | 输入输出格式不依赖特定 AI 后端，任何遵循协议的审查员都能产出合规报告 |
| REQ-007 | AUTO-FIX / ASK / ESCALATE 决策表：可执行的三分流规则 | 必须 | 决策表以可执行规则写入 references/，每条规则有明确触发条件和输出动作 |
| REQ-008 | Confidence 分级（C1-C4）：每个问题带 confidence 标签 | 必须 | 每个 Finding 带 C1-C4 标签，C1/C2 不允许进入 AUTO-FIX |
| REQ-009 | Evidence Protocol：禁止猜测性修复 | 必须 | 每个 AUTO-FIX 指令附 evidence summary（至少 2 个证据维度），无证据链只能 ASK 或记录 |
| REQ-010 | 结构化修复指令：输出机器可读的修复指令 | 必须 | 修复指令含问题编号、目标文档、修复动作、证据摘要、验证方式，可被编排器解析 |
| REQ-011 | Boil the Lake 决策化：嵌入决策逻辑 | 必须 | 职责内+C3/C4+证据充分 → 必须输出完整修复指令，不允许 defer |
| REQ-012 | 标准 Review Loop：恢复→对齐→发现→决策→修复指令→复审→PASS/下一轮 | 必须 | 报告有明确轮次编号，每轮包含报告+修复指令+复审结论三件套 |
| REQ-013 | 最多 3 轮自动驾驶：第 4 轮强制 ESCALATE | 必须 | 第 4 轮报告 Status 必须为 ESCALATED，不允许继续输出 AUTO-FIX |
| REQ-014 | 编排器调度协议：定义 reviewer 与 ASP 主编排器的 I/O 契约 | 必须 | reviewer 输出 → 编排器解析 → fixer 执行 → reviewer 复审的完整契约 |
| REQ-015 | 兼容现有归档 + 扩展：保持 prd_logs/、arch_logs/ 不变 | 必须 | 新增阶段使用对应 `{stage}_logs/` 目录，不覆盖历史 |
| REQ-016 | 统一报告模板 | 必须 | 所有阶段报告遵循同一模板：Reviewer/Round/Stage/Alignment/Findings/Decision/Evidence/Status |
| REQ-017 | 修复指令模板 | 必须 | 修复指令文件遵循统一格式，可被编排器机器解析 |
| REQ-018 | 复审记录模板 | 应该 | 复审记录含复审范围、结果、遗留问题、是否进入下一轮 |
| REQ-019 | 功能卡片测试化检查：检查 D-17~D-20 字段完整性 | 应该 | reviewer 能识别测试字段缺失/弱化，列为 MAJOR 或 MINOR |

## 3. 明确排除
| ID | 排除项 | 排除理由 |
|----|--------|---------|
| EXC-001 | 与 pb-review 体系兼容映射 | 两套并行，不做桥接 |
| EXC-002 | 独立编排器 skill | 由 ASP 主流程编排器调度 |
| EXC-003 | CI/CD 自动化集成 | 超出 skill 范围 |
| EXC-004 | 自动化测试生成 | 只做测试化检查，不生成测试代码 |
| EXC-005 | P0-P8 兼容 | ASP 与旧流程隔离 |
| EXC-006 | 统计面板 / metrics 可视化 | 后续阶段 |
| EXC-007 | Reviewer 直接修改文档 | Reviewer + Fixer 分离 |
| EXC-008 | 脚本化抽象判断 | 遵循 skill-design-protocol |
| EXC-009 | 限定特定 AI 后端 | 协议化，不绑定 Claude/Codex |

## 4. 约束条件
| ID | 约束描述 |
|----|---------|
| CON-001 | 必须遵守 `docs/skill-design-protocol.md` 七层结构框架 |
| CON-002 | 必须遵守 `docs/asp-document-protocol.md` 文档协议 |
| CON-003 | 必须遵守 `docs/consitution.md` 宪法约束 |
| CON-004 | SKILL.md 正文不超过 200 行，差异化内容通过 references/ 按需加载 |
| CON-005 | 抽象判断由模型完成，不允许通过脚本外包 |
| CON-006 | 与 pb-review 体系完全独立，不共享 registry 或 data-model |
| CON-007 | 不破坏现有 ASP 文档协议和归档结构 |
| CON-008 | 面向 PowerBy 用户群，需要足够的泛化程度 |

## 5. 关键架构决策
| 决策 | 选择 | 理由 |
|------|------|------|
| 体系定位 | 全新独立体系，与 pb-review 并行 | 独立运行，不引入 pb-review 的 registry 依赖 |
| Skill 拆分 | 1 个通用 reviewer skill，无独立编排器 | 由 ASP 主编排器调度，通过 references/ 分阶段配置差异 |
| 修复模式 | Reviewer + Fixer 分离 | reviewer 只输出修复指令，编排器调度对应 skill 执行修复 |
| AI 后端 | 协议化，不限定 | 任何遵循 I/O 协议的审查员都能接入 |
| 归档结构 | 兼容现有 + 扩展 | 保持 prd_logs/、arch_logs/，新增 plan_logs/、impl_logs/ |
| MVP 范围 | 全阶段统一框架 | 5 个阶段都能跑通完整 review loop |
