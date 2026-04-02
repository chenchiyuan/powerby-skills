# 开发任务计划

**迭代编号**: 011
**分支**: `review`
**创建日期**: 2026-03-30
**生命周期阶段**: P5 - 开发规划 / P6 - 开发实现

---

## 1. 需求与架构对齐报告

### 核心目标复述
- 基于 `011-asp-document-upgrade` 的 `proposal.md`、`feature-spec-index.md`、`feature-specs/*.md` 与 `architecture.md`，把 ASP 文档体系从旧的 `spec.md/function-points.md` 协议升级为可被 `pb-review` 零修改复用的新协议。
- 升级范围限定在 `docs/asp-document-protocol.md`、7 个 `powerby-asp-*` skill、各自 `references/` 资源、迭代文档和自动化校验。
- 严格遵守架构约束：保留 ASP 五阶段流程，不引入 scripts/，skill 目录统一为 `SKILL.md + references/`。

### 范围边界
- **本次实现（P0）**: FT-001 ~ FT-015 对应的协议升级、7 个 skill 重写、references 摘要、自动化校验、实现报告与迭代元数据收口。
- **明确排除**: 改造 `pb-review` 本体、重构 ASP 五阶段流程、引入外部 LLM 代理、增加非 011 文档定义的新功能。

### 成功标准
- [x] `docs/asp-document-protocol.md` 升级为 `v1.1.0`，包含分阶段组装机制和 `feature-spec-index.md` 替代说明。
- [x] 7 个 ASP skill 全部升级为 11 section 结构，并切换到新文档协议。
- [x] 每个 ASP skill 均具备对应的 `references/*.md` 摘要文件，且不存在 `scripts/` 目录。
- [x] 自动化测试能够校验协议版本、skill 结构、引用资源、011 交付物一致性和旧协议残留。

## 1.3 现有代码分析报告

### 现有组件清单

| 组件名称 | 路径 | 职责 | 复用可能性 | 备注 |
|---------|------|------|-----------|------|
| `docs/asp-document-protocol.md` | `docs/asp-document-protocol.md` | ASP 文档协议 v1.0.0 | 高 | 直接扩展为 v1.1.0 |
| `powerby-asp-product` | `skills/powerby-asp-product/SKILL.md` | ASP 产品流程 | 中 | 保留三模式，重写输出契约 |
| `powerby-asp-reviewer` | `skills/powerby-asp-reviewer/SKILL.md` | Claude 产品审查 | 中 | 保留三维审查，切换到新文档集合 |
| `powerby-asp-codex-reviewer` | `skills/powerby-asp-codex-reviewer/SKILL.md` | Codex 产品审查 | 中 | 保留 `codex exec` 模式，切换输入协议 |
| `powerby-asp-visualizer` | `skills/powerby-asp-visualizer/SKILL.md` | ASP 可视化产出 | 中 | 保留 Mermaid 可视化，扩展追溯矩阵与评分卡 |
| `powerby-asp-architect` | `skills/powerby-asp-architect/SKILL.md` | ASP 架构设计 | 中 | 保留三模式，切换到 feature spec 协议 |
| `powerby-asp-arch-reviewer` | `skills/powerby-asp-arch-reviewer/SKILL.md` | Claude 架构审查 | 中 | 保留三维审查，切换输入协议 |
| `powerby-asp-arch-codex-reviewer` | `skills/powerby-asp-arch-codex-reviewer/SKILL.md` | Codex 架构审查 | 中 | 保留 `codex exec` 模式，切换输入协议 |

### 编码规范总结
- **代码风格**: Markdown 协议文档 + skill 文档 + `pytest` 结构校验。
- **命名规范**: skill 目录使用 kebab-case；交付物文件与 Feature/REQ ID 使用协议定义的固定命名。
- **测试模式**: 参考 `pb-review` 的文件存在性、结构断言、协议残留检查。
- **注释规范**: 以 Markdown 结构化说明为主，测试代码使用 PEP 257 docstring。

### 复用建议
- **可直接复用**: `pb-review` 的 11 section skill 结构、`references/` 分层方式、pytest 布局校验模式。
- **可扩展复用**: 现有 7 个 ASP skill 的角色定义、工作模式和审查职责。
- **需全新开发**: ASP 协议升级后的测试文件、references 摘要内容、011 实现报告。

### 一致性建议
- **风格参考**: 对齐 `skills/pb-review/SKILL.md` 的结构化写法。
- **架构模式**: 保持“协议层 + skill 层 + references 层”的文档架构，不引入新的执行层目录。
- **注意事项**: 产品阶段与架构阶段的 feature-spec 维度边界必须明确，不能让 skill 文案重新混回旧协议。

## 1.5 文档风格定义

- **文档标准**: Markdown 协议文档 + 11 section skill 文档 + references 摘要文件。
- **验证方式**: `pytest` 校验协议版本、section、references、旧协议残留和无 `scripts/` 约束。
- **引用原则**: 共享规则写入 `docs/asp-document-protocol.md` 和 `docs/skill-design-protocol.md`，各 skill 只保留职责内摘要。

## 2. 技术方案评估

### 方案 A：只改 SKILL.md 文案
- **简介**: 保留现有目录结构，仅替换旧文档名。
- **架构遵循性**: 不能满足 `references/` 分层和统一 11 section 结构要求。
- **优点**: 改动最小。
- **缺点**: 与 011 架构不完全一致，后续维护成本高。

### 方案 B：协议层 + skill 层 + 自动化校验一起升级
- **简介**: 升级协议文档，重写 7 个 skill，补齐 `references/` 和 `pytest` 校验。
- **架构遵循性**: 完整对齐 011 `architecture.md`。
- **优点**: 满足协议一致性、可维护性和测试可验证性。
- **缺点**: 首轮改动面较大。

### 我的建议
- **推荐方案**: 方案 B
- **核心理由**: 011 的目标是建立可复用协议，而不是替换几个旧文件名。只有同时升级协议、skill 结构和自动化校验，才能满足“pb-review 零修改复用”的目标。

## 3. 开发任务清单

### P0 核心功能（Must Have）

#### TASK-011-001: 升级 ASP 文档协议到 v1.1.0
- **关联需求**: REQ-001 / REQ-015
- **关联架构**: Section 3.2 C-01 协议层
- **任务描述**: 更新 `docs/asp-document-protocol.md`，补充分阶段组装机制、`feature-spec-index.md` 替代说明和新文档清单。
- **验收标准**:
  - [ ] 版本号更新为 `1.1.0`
  - [ ] 包含“分阶段组装机制”章节
  - [ ] 包含 `feature-spec-index.md` 替代说明
  - [ ] **异常路径验证**: 缺少新增章节时测试失败
- **预估工时**: 1h
- **状态**: 已完成

#### TASK-011-002: 重写产品线 skill
- **关联需求**: REQ-007 / REQ-008 / REQ-009
- **关联架构**: C-02A / C-02B / C-02C
- **任务描述**: 重写 `powerby-asp-product`、`powerby-asp-reviewer`、`powerby-asp-codex-reviewer` 为 11 section 结构，并切换到新文档协议。
- **验收标准**:
  - [ ] 3 个 skill 均包含 11 个标准 section
  - [ ] 3 个 skill 均不再引用旧的 `spec.md`
  - [ ] 3 个 skill 均具备 references 摘要文件
  - [ ] **异常路径验证**: 缺 section 或缺 reference 时测试失败
- **预估工时**: 2h
- **状态**: 已完成

#### TASK-011-003: 重写可视化 skill
- **关联需求**: REQ-005 / REQ-006 / REQ-010
- **关联架构**: C-04 可视化 Skill
- **任务描述**: 重写 `powerby-asp-visualizer`，使其输出 `product-map.md`、`traceability-matrix.md` 和 `testability-scorecard.md`。
- **验收标准**:
  - [ ] skill 包含 11 个标准 section
  - [ ] 输出格式覆盖 3 份可视化产物
  - [ ] reference 包含评分公式摘要
  - [ ] **异常路径验证**: 缺少评分指标或 Mermaid 校验说明时测试失败
- **预估工时**: 1h
- **状态**: 已完成

#### TASK-011-004: 重写架构线 skill
- **关联需求**: REQ-011 / REQ-012 / REQ-013 / REQ-014
- **关联架构**: C-03A / C-03B / C-03C
- **任务描述**: 重写 `powerby-asp-architect`、`powerby-asp-arch-reviewer`、`powerby-asp-arch-codex-reviewer`，明确 D-09~D-16 补充边界和架构审查协议。
- **验收标准**:
  - [ ] 3 个 skill 均包含 11 个标准 section
  - [ ] 不再引用旧的 `function-points.md`
  - [ ] 明确产品阶段不可变边界
  - [ ] **异常路径验证**: 边界约束缺失时测试失败
- **预估工时**: 2h
- **状态**: 已完成

#### TASK-011-005: 增补 references 与自动化测试
- **关联需求**: REQ-002 ~ REQ-006 / REQ-014
- **关联架构**: Section 5.5 references 协议
- **任务描述**: 为 7 个 skill 增补 `references/*.md`，并新增 pytest 校验协议升级结果。
- **验收标准**:
  - [ ] 7 个 skill 的 references 文件齐备
  - [ ] 自动化测试覆盖协议版本、skill 结构、references、旧协议残留、011 交付物和无 `scripts/`
  - [ ] **异常路径验证**: 任何一个 skill 目录缺 reference 或出现 `scripts/` 时测试失败
- **预估工时**: 1.5h
- **状态**: 已完成

#### TASK-011-006: 实现报告与迭代元数据收口
- **关联需求**: REQ-014
- **关联架构**: Section 6.1 实现顺序
- **任务描述**: 更新 `tasks.md` 状态、生成 `implementation-report.md`，并同步 `.powerby` 元数据。
- **验收标准**:
  - [ ] `tasks.md` 反映最终状态
  - [ ] `implementation-report.md` 落盘
  - [ ] `.powerby/iterations.json` 记录 011
  - [ ] **异常路径验证**: 测试结果未通过时不得标记 Gate 6 完成
- **预估工时**: 0.5h
- **状态**: 已完成

## 4. 测试规格矩阵

| 测试点 ID | 关联需求 | 关联架构 | 任务ID | 测试策略 | 可量化成功标准 |
|----------|----------|----------|--------|---------|--------------|
| TC-011-001 | REQ-001 / REQ-015 | C-01 协议层 | TASK-011-001 | `pytest` | 协议版本为 `1.1.0`，新增章节完整 |
| TC-011-002 | REQ-007 / 008 / 009 | C-02 产品 Skill 组 | TASK-011-002 | `pytest` | 3 个产品线 skill 均为 11 section，且无旧协议残留 |
| TC-011-003 | REQ-005 / 006 / 010 | C-04 可视化 Skill | TASK-011-003 | `pytest` | visualizer 输出契约覆盖 3 个产物 |
| TC-011-004 | REQ-011 / 012 / 013 | C-03 架构 Skill 组 | TASK-011-004 | `pytest` | 3 个架构线 skill 均为 11 section，且有边界说明 |
| TC-011-005 | REQ-002 ~ 006 / 014 | Section 5.5 | TASK-011-005 | `pytest` | 7 个 references 文件齐备且无 `scripts/` 目录 |

## 5. Gate 5 检查

- [x] 现有代码分析已完成
- [x] 所有 P0 功能都有对应开发任务
- [x] 任务分解粒度合适
- [x] 依赖关系清晰合理
- [x] 验收标准可验证
- [x] 异常路径覆盖完整
- [x] 技术方案决策有证据链
- [x] 函数复杂度控制规划已完成
- [x] 文档风格标准已定义

## 6. Gate 6 检查

- [x] 所有 P0 任务已完成
- [x] 自动化测试全部通过
- [x] 协议与 skill 文档已对齐新协议
- [x] 7 个 references 文件已落盘
- [x] 无 `scripts/` 目录违规
- [x] 旧协议残留检查通过
- [x] 评分卡与追溯矩阵数据一致性已校验
- [x] 十条核心原则 checklist 证据已落盘
- [x] 迭代报告与元数据已更新

## 7. 当前结论

- 方案 B 已完整落地：协议层、7 个 ASP skill、references、测试和迭代文档全部收口完成。
- `pytest -q tests` 已通过，且 011 交付物一致性与 checklist 证据已纳入校验。
- P5 / P6 已完成，后续可进入 P7 代码审查阶段。
