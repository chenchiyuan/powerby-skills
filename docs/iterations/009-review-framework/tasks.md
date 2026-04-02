# 开发任务计划

**迭代编号**: 009
**分支**: `009-review-framework`
**创建日期**: 2026-03-27
**生命周期阶段**: P5 - 开发规划 / P6 - 开发实现

---

## 1. 需求与架构对齐报告

### 核心目标复述
- 基于 [`proposal.md`](./proposal.md)、[`spec.md`](./spec.md) 与 [`architecture.md`](./architecture.md) 落地 V1 还原式项目评审框架。
- 以 `pb-review` 为编排入口，串联 8 个单一职责 skill，完成“项目接入 → 证据采集 → 冲突决议 → 产品还原 → 功能还原 → 关系构建 → 差异识别 → 报告输出”主链路。
- 所有 skill 必须遵循 [`docs/skill_best.md`](/Users/chenchiyuan/projects/powerby-skills/docs/skill_best.md) 的 7 层设计结构与渐进披露原则，不把架构文档整段塞进 `SKILL.md`。

### 范围边界
- **本次实现（P0）**: FP-001 ~ FP-010 对应的 V1 skill 包、支撑脚本、报告模板、结构校验。
- **本次不做（V2）**: FP-011 ~ FP-013 的架构/实现/验证事实还原 skill。
- **明确排除**: 自动修复代码、生成新需求、质量打分、性能/安全扫描。

### 成功标准
- [x] 新建 `pb-review` 及其 8 个下游 skill，名称、职责、输入输出与架构文档一致。
- [x] `pb-review-evidence-collector` 提供确定性脚本 `collect_evidence.py` 与 `parse_git_history.py`。
- [x] `pb-review-report-composer` 提供可复用 Markdown 报告模板。
- [x] 所有新 skill 都包含主动型 `description`、明确边界、资源引用与输出结构。
- [x] 提供自动校验脚本，验证 skill 结构与关键章节完整性。

## 1.3 现有代码分析报告

### 现有组件清单

| 组件名称 | 路径 | 职责 | 复用可能性 | 备注 |
|---------|------|------|-----------|------|
| `powerby-reviewer` | `skills/powerby-reviewer/` | 评审交付类 skill，已采用 `references/` + `assets/` 分层 | 高 | 直接借鉴目录组织方式 |
| `powerby-bugfix` | `skills/powerby-bugfix/` | 问题诊断模板资产 | 中 | 可借鉴模板资产组织与结构化输出 |
| `powerby-command` | `skills/powerby-command/SKILL.md` | 编排型 skill | 中 | 可借鉴编排与前置条件说明方式 |
| `docs/skill_best.md` | `docs/skill_best.md` | Skill 最佳实践总规范 | 极高 | 本次实现的最高 skill 设计约束 |
| `skill-creator` | `/Users/chenchiyuan/.codex/skills/.system/skill-creator/SKILL.md` | 官方 skill 创建规范 | 极高 | 本次 skill 工程化结构依据 |

### 编码规范总结
- **代码风格**: 以 Markdown skill 文档为主，配合少量 Python 确定性脚本。
- **命名规范**: skill 目录与 skill 名称统一使用 kebab-case；输出字段遵循 `spec.md` 的 snake_case。
- **测试模式**: 当前仓库缺少 skill 自动化校验，本轮补充结构校验脚本。
- **注释规范**: Python 脚本使用 PEP 257 docstring；复杂步骤解释“为什么”和输入边界，而非重复行为。

### 复用建议
- **可直接复用**: `powerby-reviewer` 的资源分层模式。
- **可扩展复用**: `powerby-command` 的编排说明、`powerby-asp-product` 的“流程隔离声明”写法。
- **需全新开发**: 所有 `pb-review-*` skill、本轮 evidence scripts、报告模板、结构校验脚本。

### 一致性建议
- **风格参考**: `skills/powerby-reviewer/` 的简洁 `SKILL.md` + 外部 resources 模式。
- **架构模式**: 单一职责 skill + orchestrator 串联；公共协议下沉到共享 reference。
- **注意事项**: 避免在多个 skill 中重复复制协议原文，通过共享 resource 与明确资源入口保持 DRY。

## 1.5 文档风格定义

- **文档标准**: Skill 采用 YAML frontmatter + 结构化 Markdown；Python 脚本采用 PEP 257 docstring。
- **Skill 骨架要求**: 必须包含 `Purpose`、`Success criteria`、`Strategy`、`Tools and capability boundaries`、`Important facts and constraints`、`Workflow`、`Output format`、`Resources`。
- **模板要求**: 所有输出结构以 `spec.md` 与 `architecture.md` 定义的字段为准，禁止自由发挥字段名。
- **验证方式**: 使用 `scripts/validate_pb_review_skills.py` 做结构校验；脚本使用 `python3 -m py_compile` 做语法校验。

## 2. 技术方案评估

### 方案 A：9 个 skill 全部写成单文件 `SKILL.md`
- **简介**: 每个 skill 仅包含一个 `SKILL.md`，不提供共享 reference、脚本或模板资产。
- **架构遵循性**: 只能覆盖名称与职责，难以承接 scripts/template 的组件要求。
- **哲学对齐分析**:
  - **SOLID**: skill 职责清晰，但正文会膨胀，边界不再清晰。
  - **KISS**: 表面简单，实则把复杂性推给运行时。
  - **DRY**: 协议、数据模型、输出格式会在多个 skill 中重复。
  - **最小影响面**: 文件较少。
  - **最小惊讶原则**: 使用者难以判断哪些步骤依赖确定性脚本。
- **优点**: 交付快。
- **缺点**: 偏离 `skill_best` 的渐进披露与“可重复动作下沉 scripts/”原则。

### 方案 B：分层 skill 包实现
- **简介**: `SKILL.md` 保持精简，公共协议放在 `pb-review/references/`，确定性动作放进 `scripts/`，报告骨架放进 `assets/`。
- **架构遵循性**: 完整对齐 `architecture.md` 的 9 个 skill + 2 个脚本组件。
- **哲学对齐分析**:
  - **SOLID**: 每个 skill 只保留任务边界、策略与输出契约。
  - **KISS**: 复杂度被放到最合适的层次，正文保持清晰。
  - **DRY**: 公共协议、数据模型、顺序编排只写一份。
  - **最小影响面**: 新增文件多，但集中在 009 skill 作用域。
  - **最小惊讶原则**: 触发、执行、输出、恢复点都更明确。
- **优点**: 最符合 `skill_best.md` 与官方 `skill-creator` 规范。
- **缺点**: 首次搭建文件较多，需要额外校验结构一致性。

### 我的建议
- **推荐方案**: 方案 B
- **核心理由**: 本次任务本质上是在交付“能力包”，不是写一组松散 prompt。方案 B 才能同时满足 009 架构、skill 规范和后续可维护性。

## 3. 开发任务清单

### P0 核心功能（Must Have）

#### TASK-009-001: 建立 pb-review 共享协议资源
- **关联需求**: REQ-001 / REQ-002
- **关联架构**: Section 5.1 统一 Skill 协议、`.review/` 文件协议
- **任务描述**: 在 `skills/pb-review/references/` 中沉淀统一协议、数据模型、执行顺序说明，供全部下游 skill 复用。
- **验收标准**:
  - [x] 包含 ReviewContext、registry、状态定义、持久化规则
  - [x] 包含 V1 8 个 skill 的顺序与依赖关系
  - [x] **异常路径验证**: 明确 `failed`/`partial` 的中止或继续规则
  - [x] **文档化标准合规**
- **预估工时**: 1 小时
- **依赖关系**: 无
- **测试策略**: 结构校验 + 人工审阅
- **状态**: 已完成

#### TASK-009-002: 实现 pb-review 编排 skill
- **关联需求**: REQ-001 / REQ-008 / REQ-010
- **关联架构**: C-001 `pb-review`
- **任务描述**: 编写 orchestrator skill，定义入口、断点恢复、归集写入和顺序执行约束。
- **验收标准**:
  - [x] 明确初始化与断点恢复策略
  - [x] 明确 8 个下游 skill 的调用顺序
  - [x] **异常路径验证**: 任一 skill `failed` 时中止并返回 checkpoint 位置
  - [x] **文档化标准合规**
- **预估工时**: 1 小时
- **依赖关系**: TASK-009-001
- **测试策略**: 结构校验 + 人工审阅
- **状态**: 已完成

#### TASK-009-003: 实现 project-scope 与 evidence-collector skill 及脚本
- **关联需求**: REQ-008 / REQ-009
- **关联架构**: C-002 / C-003 / C-010 / C-011
- **任务描述**: 落地项目扫描 skill、证据采集 skill，以及两个 Python helper scripts。
- **验收标准**:
  - [x] `project_metadata` 与 `resource_inventory` 输出结构符合协议
  - [x] `collect_evidence.py` 可读取 inventory 并输出 Evidence Unit JSON
  - [x] `parse_git_history.py` 可导出 commit 元信息 JSON
  - [x] **异常路径验证**: 缺少项目路径/资源清单时立即失败
  - [x] **文档化标准合规**
- **预估工时**: 2 小时
- **依赖关系**: TASK-009-001
- **测试策略**: `py_compile` + 结构校验
- **状态**: 已完成

#### TASK-009-004: 实现 conflict/product/feature 三个还原 skill
- **关联需求**: REQ-003 / REQ-004 / REQ-005
- **关联架构**: C-004 / C-005 / C-006
- **任务描述**: 落地冲突决议、产品事实还原、功能事实还原三类 skill，严格对齐 evidence policy 与输出契约。
- **验收标准**:
  - [x] 冲突决议规则与架构文档一致
  - [x] 产品对象与功能对象字段命名符合规范
  - [x] `feature_state_registry` 输出结构明确
  - [x] **异常路径验证**: 缺少所需证据时返回 `partial` 并记录 gap
  - [x] **文档化标准合规**
- **预估工时**: 1.5 小时
- **依赖关系**: TASK-009-001
- **测试策略**: 结构校验 + 人工审阅
- **状态**: 已完成

#### TASK-009-005: 实现 relation/gap/report 三个下游 skill 与模板
- **关联需求**: REQ-006 / REQ-007 / REQ-010
- **关联架构**: C-007 / C-008 / C-009
- **任务描述**: 落地关系构建、差异识别、报告编排 skill，并提供最终 Markdown 报告模板。
- **验收标准**:
  - [x] 关系类型、coverage 指标与架构一致
  - [x] 差异与 gap 输出区分清楚
  - [x] 报告模板覆盖概览、对象清单、追踪矩阵、差异与证据索引
  - [x] **异常路径验证**: 缺少 registry 时要求停止并补齐上游
  - [x] **文档化标准合规**
- **预估工时**: 1.5 小时
- **依赖关系**: TASK-009-001
- **测试策略**: 结构校验 + 模板检查
- **状态**: 已完成

#### TASK-009-006: 建立 skill 结构校验与迭代元数据
- **关联需求**: REQ-001 / REQ-010
- **关联架构**: cross-cutting
- **任务描述**: 新增校验脚本校验全部 pb-review skill 的 frontmatter、必需章节与支撑资源；更新 `.powerby` 迭代元数据。
- **验收标准**:
  - [x] 校验脚本覆盖 9 个 skill
  - [x] `.powerby/iterations.json` 纳入 009
  - [x] `.powerby/project.json` 更新当前阶段信息
  - [x] **异常路径验证**: 缺少关键文件时校验失败并返回非零退出码
  - [x] **文档化标准合规**
- **预估工时**: 1 小时
- **依赖关系**: TASK-009-002 ~ TASK-009-005
- **测试策略**: 本地执行校验脚本
- **状态**: 已完成

## 4. 测试规格矩阵

| 测试点 ID | 关联需求 | 关联架构 | 任务ID | 测试策略 | 可量化成功标准 |
|----------|----------|----------|--------|---------|--------------|
| TC-009-001 | REQ-001 | 统一 Skill 协议 | TASK-009-001 | 结构校验 | 9 个 skill 均含必需章节与 frontmatter |
| TC-009-002 | REQ-008 | C-002 | TASK-009-003 | `py_compile` + 人工检查 | `project-scope` 输出格式与协议一致 |
| TC-009-003 | REQ-009 | C-003 / C-010 | TASK-009-003 | `py_compile` | `collect_evidence.py` 通过语法校验 |
| TC-009-004 | REQ-003 | C-004 / C-011 | TASK-009-004 | `py_compile` + 人工检查 | 冲突优先级规则被完整记录 |
| TC-009-005 | REQ-010 | C-009 | TASK-009-005 | 模板检查 | 报告模板包含 6 个核心章节 |
| TC-009-006 | REQ-001 / REQ-010 | cross-cutting | TASK-009-006 | 校验脚本 | 缺文件时返回非零，结构正确时输出 OK |

## 5. Gate 5 / Gate 6 检查

- [x] 现有代码分析已完成
- [x] 所有 P0 功能都有对应开发任务
- [x] 任务分解粒度合适
- [x] 依赖关系清晰合理
- [x] 验收标准可验证
- [x] 异常路径覆盖完整
- [x] 技术方案决策有证据链
- [x] 函数复杂度控制规划已完成
- [x] 文档化标准已定义并执行
- [x] 结构化校验脚本已建立

## 6. 当前结论

- P5 已完成，采用“分层 skill 包实现”方案。
- P6 已完成本轮主要范围：`pb-review` V1 skill 包、支撑脚本、模板与结构校验。
- V2 功能点（FP-011 ~ FP-013）保持未实现状态，未纳入本轮完成定义。
