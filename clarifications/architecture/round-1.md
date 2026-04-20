---
dimension: architecture
round: 1
scope: "pb-v1 流程自推进机制设计——从用户驱动执行到系统驱动执行、用户驱动决策"
caller: pb-v1-talk
status: 生效
created: 2026-04-17
updated: 2026-04-17
---

# 架构维度 - Round 1

## 大原则确认

### 目标
将 pb-v1 流程控制模型从"用户驱动一切"翻转为"系统驱动执行、用户驱动决策"，减少不必要的用户打断，同时保留用户对目标/边界/取舍的决策权。

### 范围
- 包含: pb-v1 全系列 skill 的流程控制机制、orchestrator 角色升级、Gate 判断协议、状态持久化与断点恢复
- 不包含: 单个 skill 的内部执行逻辑改造（那是后续迭代的事）、非 pb-v1 系列的 skill

---

## 讨论清单

### CLR-ARCH-001: 核心原则——执行权与决策权的分离
- **模糊点**: 系统和用户各自拥有什么权限？
- **影响范围**: 全流程的决策权分配
- **结论**: 用户拥有"目标、边界、取舍"的决策权；系统拥有"还原、实现、修复、复审"的执行权。只有当执行问题升级为"目标/边界/取舍问题"时，才交还给用户。"怎么做"默认系统决定，"做不做/做到哪/接受哪个代价"默认用户决定。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-002: 5 个硬 Gate 定义
- **模糊点**: 哪些问题必须交由用户？
- **影响范围**: 全流程的用户打断点
- **结论**:
  - G1: 范围/目标变更——会改变产品范围、成功标准、非目标定义
  - G2: 影响外部合同的模糊点——会改变用户可见行为、接口契约、交付承诺、性能承诺、交互路径
  - G3: 多个可行方案都合理，但取舍轴属于 owner——系统无法靠上游文档推出唯一最优方案
  - G4: 需要外部授权或环境动作——安装软件、开 GUI、申请网络、支付/账号/第三方配置
  - G5: 自循环超过阈值仍未收敛——同一问题簇连续 3 次修复-验证后仍失败
  - 命中任意一个 → USER_GATE_REQUIRED 或 ESCALATE_TO_USER
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-003: 三级决策分类
- **模糊点**: 不命中 Gate 的问题如何分类？
- **影响范围**: 系统自决的粒度和可追溯性
- **结论**:
  - AUTO_DECIDE: 阶段推进、review fail 后回流修复、实现细节选择（不改变外部合同）、测试补齐、回归验证、局部重构、纯流程动作
  - AUTO_DECIDE_WITH_ASSUMPTION: 可逆、影响范围局部、不改变外部合同、上游文档没有明确写但能根据现有原则作出强推荐。需记录：为什么这样选、还有什么备选、后面如果 reviewer 挑出问题能追溯回来
  - USER_GATE_REQUIRED / ESCALATE_TO_USER: 命中 G1-G5 的问题
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-004: 判断机制——按影响判断，不按主题判断
- **模糊点**: 同一个问题（如"同步还是异步"）什么时候系统自决，什么时候问用户？
- **影响范围**: Gate 判断的一致性
- **结论**: 不按主题分类，按影响分类。如果上游约束已经推导出唯一答案（如"生成耗时较长+需要任务状态查询" → 异步），则 AUTO_DECIDE。如果上游约束不足以推导（如只说"尽快看到结果"但未定义排队/离开页面/task id），且选择会改变接口形态/交互模型/用户预期，则 USER_GATE_REQUIRED。核心规则：问题还属于"如何还原既有约束" → 系统自推进；问题升级为"如何定义约束/修改约束/接受哪种取舍" → 交给用户。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-005: 技术机制——orchestrator 中心化 agent 调度
- **模糊点**: skill 之间如何实现自动推进？
- **影响范围**: 整个方案的落地架构
- **结论**: 采用 orchestrator 中心化 agent 调度模式。orchestrator 从"只读建议者"升级为"中心调度器"：选择合适的 skill、为每个 agent 构建上下文、调度执行、接收结果、判断 Gate、决定下一步。每个 skill 作为 agent 被调度，不需要知道"下一步是谁"。
- **否决方案**: 链式调用（context window 压力大、调用链断裂风险）、分布式自推进（Gate 逻辑分散、一致性维护成本高）
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-006: orchestrator 为 agent 构建的上下文——最小必需 + 自取
- **模糊点**: orchestrator 传给 agent 多少上下文？
- **影响范围**: context window 效率和 agent 执行质量
- **结论**: orchestrator 必须提供 4 项：目标、范围、验证方法、文档地址。不传完整文档内容。agent 在执行过程中根据文档地址自行读取所需内容。关键文档已落到文件系统，agent 可以自己找。
- **否决方案**: orchestrator 摘录完整上下文传入（浪费 context window、orchestrator 需要理解每个 skill 的细节需求）
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-007: 协议文档位置——新建 pb-v1-protocol.md
- **模糊点**: G1-G5 和三级分类的协议写在哪？
- **影响范围**: 协议的可维护性和适用范围
- **结论**: 新建 `docs/pb-v1-protocol.md`（或 `skills/pb-v1-orchestrator/` 下），专门记录 pb-v1 系列的流程自推进协议。不写在 `skill-design-protocol.md` 中，因为后者是通用的 skill 设计协议，不应包含 pb-v1 特有的流程控制逻辑。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-008: 状态持久化——flow-state.md + 各 skill 状态文档
- **模糊点**: 自推进过程中的状态如何持久化？
- **影响范围**: 断点恢复能力和流程可追溯性
- **结论**: 迭代目录下维护 `flow-state.md` 记录全局进度（阶段进度表、Gate 命中记录、假设记录、Refinery 记录）。每个 skill 维护自己的轻量状态文档。文档是持久化和断点恢复的唯一依据。orchestrator 是全局状态的唯一持有者。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-009: 断点恢复——新建专用 skill
- **模糊点**: 中断后如何恢复状态并继续？
- **影响范围**: 用户体验和流程连续性
- **结论**: 新建一个 pb-v1 系列的 skill（如 `pb-v1-resume`），专门负责：扫描 flow-state.md 和各 skill 状态文档、对比文件系统实际状态、确定恢复点、向用户报告恢复状态并确认后继续。恢复时需要用户确认（因为中断期间用户可能手动修改了产物）。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-010: 手动模式切换
- **模糊点**: 用户如何拿回控制权？
- **影响范围**: 用户对流程的控制感
- **结论**: 两个机制并存：(1) 即时中断——用户在任意时刻发送消息即可中断自推进；(2) 模式声明——用户可声明 mode: manual，所有 skill 完成后回到用户手动触发。默认 mode: auto。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-011: 状态通知——orchestrator 实时告知用户
- **模糊点**: 自推进过程中用户如何了解进度？
- **影响范围**: 用户对流程的可见性
- **结论**: orchestrator 作为中心调度器，在每个 agent 返回时向用户输出状态通知。orchestrator 知道所有的编排、调度和状态，由它统一负责通知。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-012: reviewer FAIL 后的自动回流判断
- **模糊点**: reviewer FAIL 后是否总是自动回流？
- **影响范围**: reviewer 作为最高频打断点的行为
- **结论**: reviewer FAIL 后需要前置判断：(1) FAIL issues 全部是 MINOR/MAJOR 且修复路径明确 → AUTO_DECIDE 自动回流；(2) FAIL issues 中有任何一条指向"上游约束本身有问题"或"需要范围变更" → USER_GATE_REQUIRED；(3) 连续 3 轮 FAIL → G5 ESCALATE_TO_USER。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-013: 假设记录机制——复用 clarify 存储 + 新增 auto_decided
- **模糊点**: AUTO_DECIDE_WITH_ASSUMPTION 的假设如何记录和追溯？
- **影响范围**: 假设的可追溯性和后续修正成本
- **结论**: 复用 clarify 的 clarifications/ 存储结构，新增 source_classification 值 `auto_decided`。记录格式包含：决策、理由、备选、可逆性。reviewer 审查时可扫描 auto_decided 记录追溯决策点。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-014: 实施策略——三阶段渐进
- **模糊点**: 如何安全地落地这个方案？
- **影响范围**: 升级风险和实施节奏
- **结论**:
  - Phase 1: 协议定义（pb-v1-protocol.md）+ orchestrator 改造（中心调度器）+ reviewer 改造（FAIL 自动回流）
  - Phase 2: 核心流程 skill 对接（drafting、designing、planning、implementing）+ clarify 新增 auto_decided
  - Phase 3: 全流程贯通（discovery、testing、shipping）+ 断点恢复 skill（pb-v1-resume）+ 端到端测试
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

### CLR-ARCH-015: Gate 映射——按 skill 定义默认映射
- **模糊点**: G1-G5 在每个 skill 的具体判断锚点是什么？
- **影响范围**: Gate 判断的可操作性
- **结论**: 在 pb-v1-protocol.md 中按 skill 逐个定义默认 Gate 映射。关键映射：discovery(G1/G2)、designing(G2/G3)、implementing(G4/G5)、shipping(始终 G4)、reviewer FAIL(G3/G5)。标注为"默认映射"，每个 skill 可根据具体场景覆盖。
- **来源分类**: user_confirmed
- **状态**: 生效
- **确认时间**: 2026-04-17

---

## 冲突处理

### 与 orchestrator 现有红线声明的冲突
- **现有约束**: "绝不代理调用任何 Skill"（orchestrator/SKILL.md L32）
- **新结论**: orchestrator 升级为中心调度器，通过 agent 方式调度 skill
- **处理**: 这是架构级升级，现有红线声明需要在 orchestrator SKILL.md 重写时更新。新的红线声明应反映"调度执行权"和"决策权在用户"的分离。
- **状态**: 已识别，待 Phase 1 实施时处理
