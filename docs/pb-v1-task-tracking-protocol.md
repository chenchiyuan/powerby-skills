# pb-v1 任务记录协议

**版本**: 1.0.0
**状态**: 设计完成
**创建日期**: 2026-04-21
**适用范围**: 所有执行类 Skill（drafting, designing, planning, implementing, testing, frontend, shipping, reviewer）

---

## 一、目的

任务记录协议解决两个问题：

1. **执行纪律** — 强制所有执行类 Skill 遵循"理解目标 → 规划任务 → 逐个执行"的模式，杜绝跳过规划直接动手
2. **执行可观测性** — 用户在 hands-off 模式下随时可查看当前执行进度、卡在哪步、已耗时多久

---

## 二、核心规则

1. **执行类 Skill 启动后，必须先规划再执行** — 规划结果写入任务记录文件，然后逐个执行并更新状态
2. **任务记录文件是临时文件** — 存放在 `/tmp/`，Skill 完成后删除
3. **orchestrator 可随时读取活跃任务文件** — 用户调用 orchestrator 时展示当前执行状态

---

## 三、文件规范

### 3.1 文件路径

```
/tmp/pb-v1-{iteration_id}-{skill_name}.md
```

- `iteration_id`: 当前迭代目录名（如 `my-feature`、`bugfix-auth`）
- `skill_name`: 当前 Skill 名称（如 `implementing`、`reviewer`）

### 3.2 文件格式

```markdown
# pb-v1-{skill_name}

started: {ISO8601}
skill: {skill_name}
iteration: {iteration_id}

## Tasks

| # | 任务 | 状态 | 开始时间 | 耗时 |
|---|------|------|---------|------|
| 1 | {任务描述} | ✅ done | {HH:MM:SS} | {duration} |
| 2 | {任务描述} | 🔄 running | {HH:MM:SS} | {duration} |
| 3 | {任务描述} | ⏳ pending | - | - |
```

### 3.3 状态枚举

| 状态 | 符号 | 含义 |
|------|------|------|
| pending | ⏳ | 已规划，未开始 |
| running | 🔄 | 正在执行 |
| done | ✅ | 已完成 |
| failed | ❌ | 执行失败 |
| skipped | ⏭️ | 跳过（前置条件不满足或不适用） |

---

## 四、执行流程（所有执行类 Skill 必须遵循）

```
1. 读取目标（从 dispatch_context 或用户输入）
2. 规划任务（拆解为 3-7 个子任务）
3. 创建任务记录文件（写入 /tmp/pb-v1-{iteration}-{skill}.md）
4. 逐个执行子任务：
   - 开始时：更新该行状态为 🔄 running，写入开始时间
   - 完成时：更新该行状态为 ✅ done，写入耗时
   - 失败时：更新该行状态为 ❌ failed，写入耗时
5. 全部完成 → 删除任务记录文件 → 输出 completion_signal
```

### 4.1 规划规则

- 子任务数量：3-7 个，不多不少
- 粒度标准：每个子任务应在 1-5 分钟内可完成
- 任务描述：一句话说清楚做什么，不含实现细节
- 顺序：按执行依赖排列

### 4.2 更新规则

- 每个子任务开始时立即更新文件（不是批量更新）
- 耗时字段在 running 状态时显示"已经过时间"，done 时显示"总耗时"
- 失败时保留 failed 状态，不删除记录（供 orchestrator 诊断）

### 4.3 清理规则

- Skill 正常完成（completion_signal.status == completed）→ 删除文件
- Skill 失败（completion_signal.status == failed）→ 保留文件（供诊断）
- Skill 被中断 → 保留文件（供恢复）

---

## 五、orchestrator 集成

### 5.1 状态查看

orchestrator 被调用时，执行以下步骤：

1. 扫描 `/tmp/pb-v1-{iteration_id}-*.md`
2. 如果存在活跃任务文件 → 解析并展示当前执行状态
3. 展示格式：

```
📋 当前执行状态:
  Skill: {skill_name}
  已启动: {started} ({elapsed} ago)
  进度: {done_count}/{total_count}
  当前任务: #{n} {task_description} (已执行 {duration})
```

### 5.2 异常检测

orchestrator 读取任务文件时，检查以下异常信号：

| 异常 | 条件 | 处理 |
|------|------|------|
| 执行超时 | 单个任务 running 超过 10 分钟 | 标记为潜在卡死，展示警告 |
| 无进展 | 文件存在但最后更新超过 15 分钟 | 标记为可能卡死 |
| 失败未恢复 | 有 ❌ failed 状态的任务 | 展示失败信息，建议介入 |

---

## 六、适用 Skill 清单

| Skill | 适用 | 说明 |
|-------|------|------|
| drafting | ✅ | 规划功能规格卡拆解 → 逐卡编写 |
| designing | ✅ | 规划架构模块 → 逐模块设计 |
| planning | ✅ | 规划任务拆解维度 → 逐维度生成 |
| implementing | ✅ | 规划实现任务 → 逐任务编码 |
| testing | ✅ | 规划测试范围 → 逐项验证 |
| frontend | ✅ | 规划页面/组件 → 逐个实现 |
| shipping | ✅ | 规划发布步骤 → 逐步执行 |
| reviewer | ✅ | 规划检查维度 → 逐维度验证 |
| orchestrator | ❌ | 调度类，不产出产物 |
| talk | ❌ | 对话类，无固定执行步骤 |
| clarify | ❌ | 对话类 |
| office-hours | ❌ | 对话类 |
| discovery | ❌ | 探索类，步骤不可预测 |

---

## 七、与现有协议的关系

- **pb-v1-protocol.md**: 任务记录协议是 pb-v1-protocol 的补充，定义执行层面的纪律
- **flow-state.md**: flow-state 记录 Skill 级别的进度，任务记录文件记录 Skill 内部的子任务进度。两者互补不冲突
- **completion_signal**: 任务记录文件在 completion_signal 输出前删除（正常完成时）

---

**文档状态**: 设计完成
**版本**: 1.0.0
**创建日期**: 2026-04-21
