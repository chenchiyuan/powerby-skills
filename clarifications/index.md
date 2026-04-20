# Clarifications Index

## architecture

| Round | Scope | Caller | Status | 结论数 |
|-------|-------|--------|--------|-------|
| [Round 1](architecture/round-1.md) | pb-v1 流程自推进机制设计 | pb-v1-talk | 生效 | 15 条 |

### 关键结论速查

- **CLR-ARCH-001**: 执行权与决策权分离——系统执行、用户决策
- **CLR-ARCH-002**: 5 个硬 Gate（G1 范围变更 / G2 外部合同 / G3 取舍属于 owner / G4 外部授权 / G5 循环未收敛）
- **CLR-ARCH-003**: 三级决策分类（AUTO_DECIDE / AUTO_DECIDE_WITH_ASSUMPTION / USER_GATE_REQUIRED）
- **CLR-ARCH-005**: orchestrator 中心化 agent 调度模式
- **CLR-ARCH-006**: orchestrator 传 4 项（目标、范围、验证方法、文档地址），agent 自取文档
- **CLR-ARCH-007**: 协议写入 pb-v1-protocol.md，不写 skill-design-protocol.md
- **CLR-ARCH-008**: flow-state.md 全局状态 + 各 skill 状态文档
- **CLR-ARCH-009**: 新建 pb-v1-resume skill 负责断点恢复
- **CLR-ARCH-014**: 三阶段渐进实施（协议+orchestrator+reviewer → 核心 skill → 全流程）
