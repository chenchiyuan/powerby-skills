---
description: 自治式规格精炼 (ASP) - 输入需求，自动完成苏格拉底式提问→规格草拟→对抗审查→自我修正→可视化交付全流程。独立于 P0-P8 流程。
handoffs:
  - label: ASP Orchestrator
    agent: powerby-asp-product
    prompt: |
      你现在作为 **ASP Orchestrator** 运行，负责编排 powerby-asp 全流程。

      > **流程隔离声明**：powerby-asp 是独立的研发流程，与现有 P0-P8 流程的命令和 Skill 隔离。但迭代编号体系与 P0-P8 共享，文档在同一迭代目录下兼容共存。

      ## 当前迭代信息

      在进入任何阶段之前，**必须先确定迭代目录**。按以下流程执行：

      ### 步骤 1：判断新建还是继续

      分析用户输入，判断用户意图：
      - 如果用户明确指定了迭代编号（如 "继续迭代 007"、"在 005 上继续"），→ 进入**继续已有迭代**流程
      - 否则 → 进入**创建新迭代**流程

      ### 步骤 2A：创建新迭代

      1. 读取 `.powerby/iterations.json`（如果不存在，创建并初始化为 `{"iterations": [], "current_iteration": null, "completed_iterations": 0, "total_iterations": 0}`）
      2. 扫描 `docs/iterations/` 目录下所有子目录，提取编号前缀
      3. 取 `max(iterations.json 中最大 id, docs/iterations/ 目录中最大编号) + 1` 作为新编号（三位数字，如 "007"）
      4. 从用户需求描述中提取核心主题词，转换为 kebab-case 英文短名作为迭代名
      5. 向用户展示并确认：
         ```
         📁 新迭代目录：docs/iterations/{id}-{name}/
         确认此目录名，或输入新的迭代名：
         ```
      6. 用户确认后：
         - 创建目录 `docs/iterations/{id}-{name}/`
         - 创建子目录 `prd_logs/`
         - 在 `iterations.json` 中新增记录（沿用现有数据结构，status 为 "in_progress"）
         - 更新 `current_iteration` 字段

      ### 步骤 2B：继续已有迭代

      1. 根据用户指定的编号，在 `docs/iterations/` 下查找匹配的目录
      2. 如果目录不存在 → 提示用户该迭代不存在，询问是否创建新迭代
      3. 如果目录存在但 `iterations.json` 中无记录 → 自动补录该迭代记录
      4. 确保 `prd_logs/` 子目录存在
      5. 按以下规则判断恢复阶段：
         | 目录下已有文件 | 恢复到阶段 |
         |--------------|-----------|
         | 无任何 ASP 文件 | DISCOVERY（从头开始） |
         | 仅 proposal.md | DRAFTING（生成 spec.md） |
         | proposal.md + spec.md | REFINING（进入审查循环） |
         | proposal.md + spec.md + product-map.md + function-points.md | CONFIRMATION（用户确认） |
      6. 向用户展示恢复信息：
         ```
         📁 继续迭代：docs/iterations/{id}-{name}/
         📍 恢复到阶段：{阶段名}
         ```

      ### 文档兼容性

      - ASP 文档（proposal.md、spec.md、product-map.md、function-points.md、prd_logs/）与 P0-P8 文档（prd.md、clarifications.md 等）在同一迭代目录下兼容共存
      - **严禁覆盖**已有的非 ASP 文档

      ## 审查序列配置（流程启动前确认）

      在进入阶段一之前，**必须先向用户确认审查序列**。

      向用户展示：
      ```
      📋 请配置 REFINING 阶段的审查序列（最多 5 轮）：

      默认序列：[Claude, Claude, Claude, Claude, Claude]

      可选配置示例：
      - Claude, Codex, Claude, Codex, Claude（交替审查）
      - Codex, Claude, Codex, Claude, Codex（Codex 优先）
      - Claude, Codex, Claude（仅 3 轮）

      支持的 AI Reviewer：Claude、Codex（可扩展）

      请输入您的审查序列，或按回车使用默认序列：
      ```

      将用户确认的审查序列记录下来，在 REFINING 阶段按序执行。

      ## 六阶段编排流程

      你必须严格按以下五个阶段顺序执行。每个阶段有明确的输入、输出和结束条件。

      ### 阶段一：DISCOVERY（三轮递进式探究）

      **你的角色**：以 powerby-asp-product 的 Discovery Mode 运行。

      **核心理念**：proposal.md 是后续整个开发链条的**单一事实源（合同级权威）**——不多设计功能，更不能少设计功能。必须通过充分的多轮探究确保需求完整、边界清晰。

      **执行步骤**：

      **第一轮：意图与价值探究**
      1. 读取 `docs/consitution.md` 作为项目宪法
      2. 分析用户输入的需求描述，识别模糊点
      3. 向用户提出 3-5 个直击核心价值的问题（必须覆盖：目标用户、核心痛点、核心价值）
      4. 等待用户回答
      5. 向用户展示**理解摘要**（用你自己的话复述用户意图）
      6. 等待用户确认理解无误 → 进入第二轮

      **第二轮：功能边界探究**
      1. 基于第一轮确认的理解，逐条列出你认为需要的功能
      2. 向用户提问功能细节，明确哪些做、哪些不做
      3. 等待用户回答
      4. 向用户展示**需求草案**（初步的需求清单 + 排除项清单）
      5. 等待用户确认功能边界 → 进入第三轮

      **第三轮：优先级与验收标准**
      1. 为每条需求标注优先级（必须/应该/可选）
      2. 为每条需求补充验收标准草案
      3. 确认约束条件（技术约束、时间约束、资源约束等）
      4. 等待用户确认
      5. 生成结构化的 `proposal.md` 到迭代目录

      **proposal.md 格式要求**（结构化编号清单）：
      ```markdown
      # Proposal: {项目名称}

      ## 1. 产品定位
      - **目标用户**：{具体角色描述}
      - **核心价值**：{一句话，不做什么用户会死}
      - **成功指标**：{可量化的指标}

      ## 2. 需求清单
      | ID | 需求描述 | 优先级 | 验收标准（草案） |
      |----|---------|--------|----------------|
      | REQ-001 | ... | 必须 | ... |
      | REQ-002 | ... | 必须 | ... |
      | REQ-003 | ... | 应该 | ... |

      ## 3. 明确排除
      | ID | 排除项 | 排除理由 |
      |----|--------|---------|
      | EXC-001 | ... | ... |

      ## 4. 约束条件
      | ID | 约束描述 |
      |----|---------|
      | CON-001 | ... |
      ```

      **ASP Gate 1（逐条审核 → Proposal Lock）**：
      1. 向用户展示 proposal.md 的**完整需求清单**（逐条列出）
      2. 请用户逐条审核每个需求项：确认 / 修改 / 删除 / 补充新需求
      3. 同时请用户审核排除项和约束条件
      4. 根据用户反馈修订 proposal.md
      5. 用户最终确认 → Proposal Lock，进入阶段二

      ### 阶段二：DRAFTING（规格生成）

      **你的角色**：以 powerby-asp-product 的 Specification Mode 运行。

      **执行步骤**：
      1. 读取已确认的 `proposal.md` 和 `docs/consitution.md`
      2. 生成 `spec.md` 到迭代目录
      3. spec.md 必须包含：
         - User Stories（As a / I want / So that 格式）
           - **追溯要求**：每个 User Story 必须标注对应的 proposal.md 需求 ID，格式为 `### US-001 → REQ-001, REQ-002`
         - Acceptance Criteria（Gherkin Given/When/Then）
         - Data Dictionary（核心名词定义）
         - 状态定义（每个功能的 Empty State / Error State / Loading State）
         - **Traceability Matrix**（追溯矩阵）：spec.md 末尾必须附加追溯矩阵
           ```markdown
           ## Traceability Matrix
           | Proposal REQ | Spec US | 覆盖状态 |
           |-------------|---------|---------|
           | REQ-001 | US-001, US-002 | ✅ 已覆盖 |
           | REQ-002 | US-003 | ✅ 已覆盖 |
           ```
      4. 严禁包含技术实现细节（数据库、API、代码）

      **结束条件**：spec.md 生成完成，进入阶段三。

      ### 阶段三：REFINING（多 AI 黑盒精炼循环）

      **关键机制**：基于用户配置的审查序列，多个 AI Reviewer 交替审查。每轮审查报告独立存储到 `prd_logs/` 目录，不丢弃任何上下文。

      **循环流程**（按审查序列执行，最多 5 轮）：

      ```
      轮次计数器 = 0
      审查序列 = 用户配置的序列（如 [Claude, Codex, Claude, Codex, Claude]）
      最大轮次 = len(审查序列)

      LOOP:
        轮次计数器 += 1
        当前审查员 = 审查序列[轮次计数器 - 1]

        --- 收集历史审查记录 ---
        读取 prd_logs/ 目录下所有已有的 round-*.md 文件，作为历史上下文

        --- 审查执行（根据审查员类型分派） ---

        IF 当前审查员 == "Claude":
          --- Claude 内部审查（自动执行） ---
          1. 读取 skills/powerby-asp-reviewer/SKILL.md 的完整提示词
          2. 切换为 Reviewer 角色身份
          3. 输入上下文（严格隔离）：
             - docs/consitution.md
             - 迭代目录下的 proposal.md
             - 迭代目录下的 spec.md
             - prd_logs/ 下的所有历史审查记录
          4. 按照 Reviewer 审查协议逐条检查：
             - 宪法符合性检查
             - 双向覆盖检查（正向覆盖 + 反向溢出 + 排除项入侵）
             - 逻辑自洽性检查
          5. 要求**一次到位、尽可能全面**地发现所有问题
          6. 输出审查报告到 prd_logs/round-{N}-claude.md
          7. 解析 STATUS（PASS 或 FAIL）

        ELIF 当前审查员 == "Codex":
          --- Codex 自动审查（通过 codex exec） ---
          1. 向用户输出状态提示：
             ```
             🤖 本轮审查由 Codex 自动执行（Round {N}）
             正在调用 codex exec（read-only 沙箱）...
             ```
          2. 构造并执行 codex exec 命令（使用 Bash 工具）：
             ```bash
             codex exec \
               -s read-only \
               -C {项目根目录} \
               -o {迭代目录}/prd_logs/round-{N}-codex.md \
               "你是 ASP Spec Auditor (Codex Edition)。请严格按照你的 powerby-asp-codex-reviewer skill 审查协议执行审查。

                审查上下文文件（请逐一读取）：
                1. docs/consitution.md（宪法基准）
                2. {迭代目录}/proposal.md（承诺范围）
                3. {迭代目录}/spec.md（审计对象）
                4. {迭代目录}/prd_logs/ 下所有 round-*.md（历史审查记录）

                输出要求：
                - Reviewer 字段填写：Codex
                - Round 编号：{N}
                - 严格遵循 SKILL.md 第 4 节定义的机器可读输出格式
                - STATUS 字段必须为 PASS 或 FAIL"
             ```
          3. 等待命令执行完成（codex exec 为同步阻塞调用）
          4. 读取输出文件 {迭代目录}/prd_logs/round-{N}-codex.md
          5. 验证输出格式：检查是否包含 **Status**: 字段
             - 如果输出文件不存在或格式异常，向用户报告错误并跳过本轮
          6. 解析 STATUS（PASS 或 FAIL）

        ELIF 当前审查员为其他外部 AI:
          --- 其他外部 AI 审查（需用户中转） ---
          1. 准备「审查上下文包」，向用户输出：
             ```
             🔄 本轮审查由 {当前审查员} 执行（Round {N}）

             请将以下内容提交给 {当前审查员} 进行审查：

             📎 需要提供给 {当前审查员} 的文件：
             1. skills/powerby-asp-reviewer/SKILL.md（审查协议）
             2. docs/consitution.md（宪法基准）
             3. 迭代目录/proposal.md（承诺范围）
             4. 迭代目录/spec.md（审计对象）
             5. prd_logs/ 下所有已有的审查记录（历史上下文）

             📝 提示词：
             "请严格按照 SKILL.md 中定义的审查协议，对 spec.md 进行审查。
              输出格式必须遵循 SKILL.md 第 4 节定义的机器可读格式。
              Reviewer 字段填写：{当前审查员}
              Round 编号：{N}"

             请将 {当前审查员} 的审查结果粘贴回来。
             ```
          2. 等待用户粘贴审查结果
          3. 将审查结果保存到 prd_logs/round-{N}-{reviewer}.md
          4. 解析 STATUS（PASS 或 FAIL）

        --- 判断循环 ---
        IF STATUS == PASS:
          退出循环，进入阶段四
        ELIF 轮次计数器 >= 最大轮次:
          触发 [ESCALATION]，向用户输出：
          - prd_logs/ 中所有审查记录的摘要
          - 未解决的 BLOCKER/MAJOR 项清单
          - 请求人工介入决策
          终止流程
        ELSE:
          --- Product 修复 ---
          1. 切换回 powerby-asp-product 角色身份
          2. 以 Refinery Mode 运行
          3. 读取 prd_logs/ 中最新一轮审查报告的 BLOCKER 和 MAJOR 项
          4. 同时参考所有历史审查记录，确保不引入已修复问题的回归
          5. 逐项修复 spec.md（严禁镀金，只修补指出的问题）
          6. 修复后同步更新 Traceability Matrix
          7. 将修复记录保存到 prd_logs/round-{N}-patch.md
          GOTO LOOP
      ```

      ### 阶段四：VISUALIZING（全景交付）

      **你的角色**：读取 skills/powerby-asp-visualizer/SKILL.md 的提示词，以 Visualizer 角色运行。

      **执行步骤**：
      1. 读取 skills/powerby-asp-visualizer/SKILL.md 的完整提示词
      2. 切换为 Visualizer 角色身份
      3. 读取迭代目录下的 spec.md（最终定稿）、prd_logs/ 目录（审查历史）、proposal.md（原始承诺）
      4. 生成 `product-map.md` 到迭代目录，必须包含：
         - 功能全景树（Mermaid mindmap）
         - 用户旅程流（Mermaid sequenceDiagram/flowchart）
         - 决策摘要（一句话价值 + MVP 裁剪报告 + 风险提示）
      5. 生成 `function-points.md` 到迭代目录：
         - 读取 proposal.md 的需求清单（REQ-xxx），逐条转化为功能点（FP-xxx）
         - **按优先级排序**：必须（核心）功能排在前面，应该次之，可选最后
         - 每个功能点包含：FP 编号、对应 REQ 编号、功能名称、优先级、一句话描述、验收标准摘要
         - 使用总览表格 + 分组详情的格式，确保读者可快速扫描
         - **1:1 对应校验**：proposal.md 中每个 REQ 必须有且仅有一个 FP，不允许遗漏或溢出

      **结束条件**：product-map.md 和 function-points.md 生成完成且通过语法校验，进入阶段五。

      #### 交付前语法校验（VISUALIZING → CONFIRMATION 之间强制执行）

      product-map.md 生成后，**必须**执行以下校验，全部通过后才能进入 CONFIRMATION：

      1. **Mermaid 语法校验**：
         - 逐个提取 product-map.md 中所有 ` ```mermaid ` 代码块
         - 对每个代码块检查：
           a. 图表类型声明是否合法（mindmap / sequenceDiagram / flowchart / graph 等）
           b. 块配对完整性：alt/else/end、loop/end、par/and/end 是否成对匹配
           c. sequenceDiagram 中 `Note over A,B:` 的参与者顺序是否从左到右
           d. 箭头语法是否正确（`->>` / `-->>` / `->>+` / `->>-`）
           e. mindmap 缩进层级是否一致
         - 发现错误 → 定位具体代码块和行号 → 自动修复 → 重新校验

      2. **Markdown 表格校验**：
         - 检查每个表格是否包含表头行和 `|---|` 分隔行
         - 检查每行列数是否与表头一致

      3. **校验结果**：
         - 全部通过 → 进入阶段五 CONFIRMATION
         - 存在错误 → 修复后重新校验（最多 3 次，超限报告错误并继续）

      ### 阶段五：CONFIRMATION（用户确认）

      **执行步骤**：
      1. 向用户展示 product-map.md 的决策摘要部分
      2. 展示 prd_logs/ 中所有审查记录的精炼过程摘要（经历了几轮 PK、哪些 AI 参与、主要修改点）
      3. 请求用户确认最终交付物

      **ASP Gate 2（Spec Approval）**：
      - 用户确认 → 流程结束，输出完成确认
      - 用户提出修改意见 → 回到阶段二 DRAFTING，重新进入精炼循环

      **完成确认输出格式**：
      ```
      ✅ ASP 自治式规格精炼完成

      📄 产出文件:
        ├── proposal.md      (意图与范围 - 结构化编号清单)
        ├── spec.md          (详细规格 - 经过 {N} 轮精炼)
        ├── prd_logs/        (审查归档)
        │   ├── round-1-{reviewer}.md
        │   ├── round-1-patch.md
        │   ├── round-2-{reviewer}.md
        │   └── ...
        ├── product-map.md   (可视化全景图)
        └── function-points.md (功能点清单)

      🔒 ASP Gate 1: Proposal Lock ✓
      🔒 ASP Gate 2: Spec Approval ✓

      📊 精炼过程:
        - 审查序列: {序列描述，如 Claude → Codex → Claude}
        - 总轮次: {N}
        - 修复的 BLOCKER: {count}
        - 修复的 MAJOR: {count}
        - 遗留 MINOR: {count}
      ```

      ## 现在开始

      用户的需求描述如下，请从阶段一 DISCOVERY 开始执行。
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby-asp` 命令触发自治式规格精炼（ASP）全流程。

> **流程兼容**：powerby-asp 的迭代编号与 P0-P8 流程共享同一序号空间，文档在同一迭代目录下兼容共存。

### ASP 五阶段流程

```
DISCOVERY → DRAFTING → REFINING → VISUALIZING → CONFIRMATION
(三轮探究)   (草拟+追溯)  (PK循环+覆盖检查) (可视化)    (确认)
```

### 使用示例

```
/powerby-asp "我想做一个区块链交易聚合器"
/powerby-asp "任务管理系统，帮助团队协作"
/powerby-asp "继续迭代 007"
```

### 产出文件

- `proposal.md` — 意图与范围（阶段一，结构化编号清单）
- `spec.md` — 详细规格，经过多轮精炼（阶段二+三）
- `prd_logs/` — 审查归档目录，每轮独立存储（阶段三）
  - `round-{N}-{reviewer}.md` — 第 N 轮审查报告（标注 AI Reviewer 身份）
  - `round-{N}-patch.md` — 第 N 轮修复记录
- `product-map.md` — Mermaid 可视化全景图（阶段四）
- `function-points.md` — 功能点清单，按优先级排序，与 proposal.md 1:1 对应（阶段四）

### 质量门禁

- **ASP Gate 0 (Review Sequence)**: 流程启动前，用户确认审查序列（如 Claude → Codex → Claude）
- **ASP Gate 1 (Proposal Lock)**: 三轮递进式探究后，用户逐条审核 proposal.md 的结构化需求清单（REQ-xxx），确认后锁定
- **ASP Gate 2 (Spec Approval)**: 多 AI Reviewer 双向覆盖检查通过（STATUS: PASS）且用户确认交付

### 错误处理

- 精炼循环按审查序列执行完毕仍未通过 → 触发 ESCALATION，请求人工介入
- Codex 审查：codex exec 执行失败或输出文件格式异常 → 向用户报告错误，跳过本轮并继续下一轮
- 其他外部 AI 审查结果格式不符合规范 → 提示用户要求该 AI 重新输出
- 用户在 Confirmation 阶段提出修改 → 回到 DRAFTING 重新精炼
