# ASP Review Orchestrator Protocol

**版本**: 1.0.0  
**制定日期**: 2026-03-31  
**适用范围**: `pb-review-v2` 与 ASP 主编排器、fixer skills 的 I/O 契约

---

## 1. 目标

定义 `reviewer -> fixer -> reviewer` 的机器可读协议，使 ASP review 闭环能在不修改 reviewer 角色边界的前提下自动复审与归档。

## 2. 参与方

- **Reviewer**: `skills/pb-review-v2/SKILL.md`
- **Fixer**:
  - 产品/规格阶段 -> `powerby-asp-product`
  - 架构阶段 -> `powerby-asp-architect`
  - 计划/实现阶段 -> 由 ASP 主编排器决定是否有人类介入或后续 skill 执行
- **Orchestrator**: ASP 主流程编排器

## 3. 阶段与归档目录

| Stage | 主审查对象 | 日志目录 |
|------|-----------|---------|
| `product` | `proposal.md` | `prd_logs/` |
| `spec` | `feature-spec-index.md` + `feature-specs/*.md` | `prd_logs/` |
| `architecture` | `architecture.md` | `arch_logs/` |
| `plan` | `tasks.md` | `plan_logs/` |
| `implementation` | `implementation/implementation-report.md` | `impl_logs/` |

## 4. Reviewer 输入

```yaml
review_request:
  iteration_dir: string
  reviewer_identity: string
  round: integer
  stage: optional string
  review_target: optional string
```

## 5. Reviewer 输出

```yaml
review_response:
  reviewer: string
  round: integer
  stage: enum [product, spec, architecture, plan, implementation]
  status: enum [PASS, FAIL, ESCALATED]
  alignment_summary:
    upstream_complete: boolean
    downstream_clean: boolean
    gaps:
      - type: enum [missing, overflow, conflict]
        description: string
        evidence: string
  findings:
    - id: string
      severity: enum [BLOCKER, MAJOR, MINOR]
      confidence: enum [C1, C2, C3, C4]
      decision: enum [AUTO-FIX, ASK, ESCALATE]
      location: string
      evidence:
        - string
  fix_instructions:
    - finding_id: string
      target_doc: string
      fix_action: string
      evidence_summary:
        - string
      verification: string
```

## 6. Fixer 输入

```yaml
fix_request:
  stage: string
  round: integer
  instructions:
    - finding_id: string
      target_doc: string
      fix_action: string
      evidence_summary:
        - string
      verification: string
```

## 7. Fixer 输出

```yaml
fix_response:
  stage: string
  round: integer
  status: enum [APPLIED, PARTIAL, FAILED]
  patch_notes:
    - target_doc: string
      summary: string
  unresolved:
    - finding_id: string
      reason: string
```

## 8. 复审输入

```yaml
recheck_request:
  iteration_dir: string
  round: integer
  stage: string
  previous_report: string
  fixer_response: optional object
```

## 9. 状态机

1. `PASS`: 结束当前阶段 review loop。
2. `FAIL` + 至少一个 `AUTO-FIX`: orchestrator 交给 fixer 执行，然后触发下一轮复审。
3. `FAIL` + 仅 `ASK`: orchestrator 收集用户决策，再决定是否执行 fixer。
4. `ESCALATED`: 停止自动驾驶，要求人工介入。
5. `round > 3`: reviewer 必须直接返回 `ESCALATED`。

## 10. 命名规则

- 审查报告: `{stage}_logs/round-{N}-{reviewer}.md`
- 修复指令: `{stage}_logs/round-{N}-fix-instructions.yaml`
- 复审结果: `{stage}_logs/round-{N}-review-result.md`

## 11. 失败处理

- 找不到 fixer skill -> 对应 finding 降级为 `ASK`
- 修复指令格式非法 -> fixer 跳过并在 `fix_response.unresolved` 中记录
- 输出文件缺失 -> 视为失败，不允许伪装为 `PASS`
- 历史日志缺失 -> 按第 1 轮处理，不构成失败
