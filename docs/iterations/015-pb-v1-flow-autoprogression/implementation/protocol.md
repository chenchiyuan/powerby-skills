# 实现协议

## 约束来源
- architecture.md → 组件职责、接口定义、变更清单
- tasks.md → 任务拆解、依赖顺序、验收标准
- pb-v1-protocol.md → 协议定义（已完成，作为实现参照）
- arch_decisions.md → 技术决策链

## 工程约束
- 技术栈: Claude Code Skill（SKILL.md markdown 文件）
- 运行环境: Claude Code CLI / Desktop App
- 持久化: 文件系统（markdown 文档）
- 调度机制: Agent 工具（subagent，独立 context window）

## 实现范围
- T-001: ✅ 已完成（pb-v1-protocol.md）
- T-002 ~ T-008: 本次实现（Phase 1 + Phase 2）
- T-009: P1，本次不实现

## 接口定义（从 architecture.md §6.2 提取）

### dispatch_context（orchestrator → agent）
```yaml
dispatch_context:
  goal: string          # 必填
  scope: string         # 必填
  verification: string  # 必填
  doc_paths:            # 必填
    - string
```

### completion_signal（agent → orchestrator）
```yaml
completion_signal:
  skill: string                    # 必填
  status: enum [completed, failed, blocked]  # 必填
  artifacts:                       # 必填
    - path: string
      type: string
  issues: optional array
    - description: string
      gate_candidate: optional enum [G1, G2, G3, G4, G5]
  assumptions: optional array
    - clr_id: string
      summary: string
```

### reflow_recommendation（reviewer → orchestrator，FAIL 时附加）
```yaml
reflow_recommendation:
  decision: enum [AUTO_DECIDE, USER_GATE_REQUIRED, ESCALATE_TO_USER]
  responsible_skill: optional string  # AUTO_DECIDE 时必填
  reason: string
  issues_summary: array
    - id: string
      severity: enum [BLOCKER, MAJOR, MINOR]
      points_to_upstream: boolean
```

### status_notification（orchestrator → 用户）
| 场景 | 格式 |
|------|------|
| 正常推进 | `✅ {skill} 完成 → 自动推进到 {next_skill}` |
| reviewer PASS | `✅ reviewer({type}) PASS → 自动推进到 {next_skill}` |
| reviewer FAIL + 回流 | `🔄 reviewer({type}) FAIL（{n} 个问题）→ 回流 {skill}` |
| Gate 命中 | `⛔ Gate {G1-G5}: {问题}` |
| 流程完成 | `🏁 流程完成` |

## 任务执行顺序

```
T-002 (orchestrator 核心) ──┬── T-003 (状态管理)
                            ├── T-004 (状态通知)
                            ├── T-005 (回流集成) ← T-006
                            └── T-008 (completion_signal)
T-006 (reviewer 回流输出) ──┘
T-007 (clarify auto_decided) — 独立
```

## 还原检查清单

- [ ] orchestrator SKILL.md: 红线声明反映"调度执行权 + 决策权在用户"
- [ ] orchestrator SKILL.md: 核心哲学从"只读建议"变为"调度执行"
- [ ] orchestrator SKILL.md: 输入协议包含 completion_signal 消费
- [ ] orchestrator SKILL.md: 输出协议包含 dispatch_context 构建
- [ ] orchestrator SKILL.md: 执行流程包含调度循环 + Gate 判断
- [ ] orchestrator SKILL.md: 状态管理包含 flow-state.md 读写
- [ ] orchestrator SKILL.md: 状态通知包含 5 种格式
- [ ] orchestrator SKILL.md: 回流判断包含 3 种路径
- [ ] reviewer SKILL.md: completion_signal 新增 reflow_recommendation
- [ ] clarify SKILL.md: source_classification 新增 auto_decided
- [ ] drafting SKILL.md: 输入新增 dispatch_context，输出新增 completion_signal
- [ ] designing SKILL.md: 同上
- [ ] planning SKILL.md: 同上
- [ ] implementing SKILL.md: 同上
