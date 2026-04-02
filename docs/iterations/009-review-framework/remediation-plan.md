# 009 Review Framework 重构计划

**迭代编号**: 009  
**文档日期**: 2026-03-27  
**目标**: 将当前仅有 skill 骨架的 009，实现为符合 `docs/skill_best.md` 与 `docs/skill_demo.md` 预期的可执行评审框架。

---

## 1. 现状判断

### 1.1 当前真实状态

009 当前完成的是：

- `pb-review` 与 8 个下游 skill 的基础 `SKILL.md`
- 共享协议 reference
- 两个 evidence helper scripts
- 一个结构级校验脚本

009 当前**未完成**的是：

- 可执行 runner / runtime
- `.review/` registry 持久化与去重归集
- checkpoint / resume 实现
- 多数下游 skill 的真实执行逻辑
- 真实 demo
- baseline / with skill 评估闭环
- 达到 `docs/skill_demo.md` 级别的 skill 文本密度与资源分层

### 1.2 重构原则

- **先修运行时，再修文案**：先让 009 真正能跑，再把 skill 文本提升到最佳实践级。
- **文档驱动**：实现以 `proposal.md`、`spec.md`、`architecture.md` 为合同，不以当前 `tasks.md` 的已完成声明为准。
- **能力产品化**：每个 skill 不只是 prompt，而是 `SKILL.md + scripts + references + assets + examples + eval` 的能力包。
- **渐进披露**：把确定性动作下沉到 `scripts/`，把规则和失败模式下沉到 `references/`。
- **证据闭环**：每个产物都要能回溯到 registry、对象 ID、关系 ID、gap / conflict / evidence。

---

## 2. 目标完成定义

只有当以下条件全部成立，009 才算完成：

1. 可以对任意本地仓库运行一次真实 `pb-review`
2. 可以落地 `.review/` 全套中间产物
3. 可以生成 `review_report.md`
4. 支持 `checkpoint.json` 断点恢复
5. `REQ-003` ~ `REQ-010` 都有真实执行逻辑，不只是 skill 说明
6. 至少有 2 个 demo case
7. 有 baseline vs with_skill 的最小评估记录
8. skill 文本结构和密度达到 `docs/skill_best.md` / `docs/skill_demo.md` 的预期

---

## 3. 分批实施计划

### Batch 1：运行时闭环

**目标**：让 009 先“能跑”。

**交付物**：

- `skills/pb-review/scripts/review_runner.py`
- `skills/pb-review/scripts/review_context.py`
- `skills/pb-review/scripts/registry_store.py`
- `skills/pb-review/scripts/checkpoint.py`

**必须实现**：

- `.review/` 目录初始化
- registry 文件读写
- 标准输出归集
- `context_writes` 持久化
- checkpoint 更新
- resume 恢复
- 顺序执行 8 个下游 executor

**验收标准**：

- 可生成 `.review/project_metadata.json`
- 可生成 `.review/evidence_registry.json`
- 可生成 `.review/review_report.md`
- 失败中断后可从 checkpoint 恢复

### Batch 2：下游 executor 落地

**目标**：让 REQ-003 ~ REQ-010 变成真实能力，而不是文案。

**交付物**：

- 每个下游 skill 的 `scripts/run.py`

**必须实现**：

- `project-scope`：目录扫描与 inventory 归类
- `evidence-collector`：Evidence Unit 生成、Git 历史采集、增量缓存
- `conflict-resolver`：时间优先 + 来源优先 + `current_facts`
- `product-reconstructor`：Goal / Role / Scenario / Constraint / Non-goal
- `feature-reconstructor`：Feature / Rule / Boundary / Feature State
- `relation-builder`：supports / constrains / 覆盖率统计
- `gap-analyzer`：difference_list / gap_registry / conflict 补充
- `report-composer`：真实 Markdown 报告渲染

**验收标准**：

- 每个 executor 都能单独运行
- 主链路跑通后有 objects / relations / conflicts / gaps
- `current_facts`、`feature_state_registry`、`traceability_matrix` 均真实产出

### Batch 3：Skill 文本升级

**目标**：把 skill 从“玩具 prompt”升级成“能力产品”。

**必须实现**：

- 每个 skill 增加：
  - `Use this skill to...`
  - `Apply it when...`
  - `Do not rely on it for...`
  - `compatibility`
  - `Examples`
  - `Subtask / parallelism guidance`
  - 更细粒度 `Resources`
  - `failure-modes.md` / `examples.md`

**验收标准**：

- skill 文本不再只是章节标题 + 几条 bullets
- 与 `docs/skill_demo.md` 在工程密度上同一个量级

### Batch 4：Demo 与评估

**目标**：建立 `skill_best` 要求的闭环。

**交付物**：

- `docs/iterations/009-review-framework/demos/powerby-skills.md`
- `docs/iterations/009-review-framework/demos/sample-repo.md`
- `docs/iterations/009-review-framework/evals/baseline-vs-skill.md`
- `docs/iterations/009-review-framework/acceptance.md`

**验收标准**：

- 至少 2 个真实仓库 demo
- 记录 baseline / with skill 差异
- 给出真实输出截图或关键产物路径

---

## 4. 本轮整改范围

本轮优先做：

1. Batch 1 全部
2. Batch 2 的最小 V1 闭环
3. Batch 4 中 `powerby-skills` demo

本轮不强求全部完成：

- Batch 3 全量 skill 文本升级
- 第二个 demo 仓库
- 完整 baseline 评估体系

---

## 5. 风险与对策

### 风险 1：抽取逻辑过于通用，导致结果粗糙

**对策**：
- 先交付可执行闭环
- 再通过 demo 反向打磨抽取 heuristics

### 风险 2：resume / registry 逻辑复杂，容易写出伪恢复

**对策**：
- 先实现顺序流程
- 再实现 checkpoint 一致性校验
- 所有写入先落盘，再更新 checkpoint

### 风险 3：skill 文本升级会拖慢运行时交付

**对策**：
- 本轮只补关键 intro / compatibility / resource index
- 全量文字增强放到下一批

---

## 6. 本轮完成定义

本轮结束时，至少应满足：

- `pb-review` 能真实执行一轮
- `.review/` 关键文件可落地
- `powerby-skills` 仓库可以产出一份真实 `review_report.md`
- 009 不再只是 skill skeleton，而是最小可运行框架
