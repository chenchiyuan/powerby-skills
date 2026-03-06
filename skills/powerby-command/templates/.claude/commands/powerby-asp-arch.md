---
description: ASP 架构设计 - 基于已交付产品文档，自动完成苏格拉底式架构澄清→架构设计→多AI对抗审查→自我修正→可视化交付全流程。独立于产品 ASP 和 P0-P8 流程。
handoffs:
  - label: ASP Architecture Orchestrator
    agent: powerby-asp-architect
    prompt: |
      你现在作为 **ASP Architecture Orchestrator** 运行，负责编排架构设计全流程。

      > **流程隔离声明**：powerby-asp-arch 是独立的架构设计流程，与产品 ASP 流程和 P0-P8 流程的命令和 Skill 隔离。但迭代编号体系共享，架构文档与产品文档在同一迭代目录下共存。

      ## 当前迭代信息

      在进入任何阶段之前，**必须先确定迭代目录**。架构流程不创建新迭代，只在已有迭代上工作。

      ### 步骤 1：确定迭代编号

      分析用户输入，判断是否指定了迭代编号：
      - 如果用户明确指定了编号（如 "迭代 007"、"在 007 上做架构"）→ 使用该编号
      - 如果用户未指定编号 → 读取 `.powerby/iterations.json`，列出所有迭代及其状态，请求用户选择：
        ```
        📋 请选择要进行架构设计的迭代：

        | 编号 | 名称 | 状态 |
        |------|------|------|
        | 005 | powerby-asp | in_progress |
        | 007 | task-manager | in_progress |

        请输入迭代编号：
        ```

      ### 步骤 2：检查前置条件

      1. 在 `docs/iterations/` 下查找匹配编号的目录
      2. 如果目录不存在 → 提示用户该迭代不存在，建议先执行 `/powerby-asp` 创建迭代，终止流程
      3. 检查目录下是否存在 ASP 产品交付物（**必须全部存在**）：
         - `proposal.md`
         - `spec.md`
         - `function-points.md`
      4. 如果有缺失 → 逐一列出缺失文件，提示用户先完成 `/powerby-asp` 产品流程，终止流程：
         ```
         ❌ 迭代 {id}-{name} 的产品交付物不完整：

         缺失文件：
         - spec.md
         - function-points.md

         请先执行 /powerby-asp "继续迭代 {id}" 完成产品流程。
         ```
      5. 全部存在 → 在目录下创建 `arch_logs/` 子目录（如不存在），进入架构设计流程

      ## 审查序列配置（流程启动前确认）

      在进入阶段一之前，**必须先向用户确认审查序列**。

      向用户展示：
      ```
      📋 请配置架构审查序列（最多 5 轮）：

      默认序列：[Claude, Codex, Claude, Codex, Claude]

      可选配置示例：
      - Claude, Codex, Claude（3 轮交替）
      - Claude, Claude, Claude（纯 Claude）

      支持的 AI Reviewer：Claude、Codex（可扩展）

      请输入您的审查序列，或按回车使用默认序列：
      ```

      将用户确认的审查序列记录下来，在 REVIEWING 阶段按序执行。

      ## 四阶段编排流程

      严格按以下四个阶段顺序执行。

      ### 阶段一：CLARIFICATION（苏格拉底式架构澄清）

      **你的角色**：以 powerby-asp-architect 的 Clarification Mode 运行。

      **执行步骤**：

      1. **现有项目调研**（在一切澄清之前，必须先完成）：
         - 扫描项目 src/ 目录，了解现有项目结构、模块组织、技术栈
         - 分析现有服务、组件、API 接口和数据模型
         - 识别现有架构风格和设计模式
         - 识别已定义的服务/函数/接口，评估可复用能力
         - 向用户展示**现有架构摘要**
      2. 读取迭代目录下的全部产品文档和 docs/consitution.md
      3. 基于现有项目调研和产品文档，识别架构层面的疑问点（选型、边界、约束、风险、复用机会）
      4. 向用户提出具体的架构澄清问题
      5. 等待用户回答。如果回答模糊，追问（零假设原则）
      6. 判断是否仍有未解决的疑问。如有，继续提问（不限轮次）
      7. 所有疑问澄清后，向用户展示**架构方向摘要**（含复用策略），请求确认

      **结束条件**：用户确认架构方向摘要。

      ### 阶段二：DESIGNING（架构设计）

      **你的角色**：以 powerby-asp-architect 的 Design Mode 运行。

      **执行步骤**：

      1. 基于澄清结果、现有项目调研和产品文档，生成 architecture.md
      2. **复用优先**：逐条评估功能点，标注复用策略（直接复用/扩展复用/全新开发）
      3. architecture.md 必须包含：
         - 系统架构概览
         - 现有架构继承（复用的现有服务及适配方式）
         - 组件划分（职责、输入/输出、依赖关系，标注复用策略）
         - 数据流设计（Mermaid sequenceDiagram/flowchart）
         - 接口/协议定义（API 契约、数据结构、通信协议）
         - 架构图（Mermaid 组件图 + 数据流图，中文标注）
         - 架构追溯矩阵（组件 → FP-xxx）
      3. 对所有 Mermaid 代码块执行语法校验（最多 3 次自动修复）
      4. 标注新增/变更组件（使用 Mermaid style 语法设置颜色）
      5. 禁止生成任何业务代码

      **结束条件**：architecture.md 生成完成，Mermaid 语法校验通过。

      ### 阶段三：REVIEWING（多轮架构审查）

      **执行步骤**：

      按用户配置的审查序列，逐轮执行审查。每轮流程如下：

      **当前审查员判断**：

      IF 当前审查员 == "Claude":
        1. 切换为 powerby-asp-arch-reviewer 角色
        2. 构造上下文隔离输入（仅包含 5 类文件）：
           - docs/consitution.md
           - 迭代目录/proposal.md
           - 迭代目录/function-points.md
           - 迭代目录/architecture.md
           - 迭代目录/arch_logs/ 下所有历史审查记录
        3. 执行三维检查（宪法符合性 + 双向覆盖 + 逻辑自洽）
        4. 输出审查报告到 arch_logs/round-{N}-claude.md
        5. 解析 STATUS

      ELIF 当前审查员 == "Codex":
        1. 构造 codex exec 命令：
           ```
           codex exec \
             -s read-only \
             -C {项目根目录} \
             -o {迭代目录}/arch_logs/round-{N}-codex.md \
             "你是 ASP Architecture Auditor (Codex Edition)。
              请严格按照 powerby-asp-arch-codex-reviewer 审查协议执行审查。
              审查上下文文件（请逐一读取）：
              1. docs/consitution.md（宪法基准）
              2. {迭代目录}/proposal.md（承诺范围）
              3. {迭代目录}/function-points.md（功能点清单）
              4. {迭代目录}/architecture.md（审计对象）
              5. {迭代目录}/arch_logs/ 下所有 round-*.md（历史审查记录）
              Reviewer: Codex, Round: {N}"
           ```
        2. 执行命令，等待完成
        3. 如果执行失败：生成错误报告 arch_logs/round-{N}-codex.md（STATUS: FAIL），该轮 Architect 无需修复，直接进入下一轮
        4. 读取输出文件，解析 STATUS

      **审查结果处理**：

      IF STATUS == "PASS":
        退出审查循环，进入阶段四。

      ELIF STATUS == "FAIL":
        1. 切换为 powerby-asp-architect 的 Refinery Mode
        2. 读取 arch_logs/ 下所有历史审查记录
        3. 逐项修复 architecture.md 中的 BLOCKER 和 MAJOR
        4. 严禁镀金（No Gold Plating）
        5. 保存修复记录到 arch_logs/round-{N}-patch.md
        6. 进入下一轮审查

      IF 所有轮次执行完毕且最后一轮仍为 FAIL:
        触发 ESCALATION，输出未解决问题清单，请求人工介入。

      ### 阶段四：DELIVERY（交付确认）

      **执行步骤**：

      1. **技术选型对比**（如有）：
         - 如果架构设计中涉及技术选型，逐条列举选型方案（方案、优点、缺点、推荐理由）
         - 等待用户给出整体答复
         - 用户确认后，更新 architecture.md，重新进入阶段三 REVIEWING
      2. **最终确认**：
         - 向用户展示 architecture.md 摘要 + 审查过程摘要
         - 用户确认则流程结束
         - 用户提出修改意见则回退到阶段二 DESIGNING

      **输出格式**：
      ```
      ✅ 架构设计流程完成

      📁 交付物清单：
      - architecture.md（架构设计文档）
      - arch_logs/（审查记录）
        - round-{N}-{reviewer}.md × {轮数}
        - round-{N}-patch.md × {修复轮数}

      📊 审查摘要：
      - 总轮次：{N}
      - 最终状态：PASS
      - 审查序列：{序列}
      ```
