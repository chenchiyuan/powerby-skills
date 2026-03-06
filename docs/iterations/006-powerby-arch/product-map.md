# Product Panorama: PowerBy Architecture Design (架构设计流程)

**版本**: v1.0.0
**基于**: spec.md v1.2.0

---

## 1. The Big Picture (功能全景树)

```mermaid
mindmap
  root((PowerBy 架构设计))
    Epic 1: 角色与流程
      US-001 架构师角色
        产品文档读取
        architecture.md 生成
      US-002 苏格拉底式澄清
        不限轮次提问
        架构方向确认
      US-003 独立流程触发
        产品文档校验
        流程启动
    Epic 2: 审查机制
      US-014 上下文隔离
        5类文件限定
        屏蔽思考过程
      US-004 多轮审查
        序列配置
        历史上下文传递
        ESCALATION
      US-005 宪法符合性
        SOLID/DRY检查
        奥卡姆剃刀
      US-006 双向覆盖
        正向覆盖
        反向溢出
        排除项入侵
      US-013 Refinery Mode
        逐项修复
        严禁镀金
    Epic 3: Skill 基础设施
      US-007 Skill 协议复用
        frontmatter 格式
        机器可读输出
      US-008 接口/协议定义
        API 契约
        数据结构
        通信协议
    Epic 4: 可视化
      US-009 架构图
        Mermaid 组件图
        数据流图
        语法校验
      US-010 变更标注
        新增标记
        修改标记
    Epic 5: 增强
      US-011 技术选型对比
        结构化表格
        用户决策循环
      US-012 Codex 自动审查
        codex exec
        错误报告
```

## 2. Core Journey (核心流程)

```mermaid
sequenceDiagram
    participant U as 用户
    participant O as Orchestrator
    participant A as Architect
    participant R as Reviewer

    Note over U,O: 流程启动
    U->>O: 触发架构设计命令
    O->>O: 校验产品文档完整性
    alt 文档缺失
        O-->>U: 报错：列出缺失文件
    end

    Note over U,A: 苏格拉底式架构澄清
    O->>A: 进入澄清阶段
    loop 直到无疑问
        A->>U: 提出架构澄清问题
        U->>A: 回答
        A->>A: 判断是否仍有疑问
    end
    A->>U: 展示架构方向摘要
    U->>A: 确认

    Note over U,A: 架构设计
    A->>A: 生成 architecture.md
    A->>A: Mermaid 语法校验

    Note over U,R: 多轮审查循环
    loop 按审查序列（最多5轮）
        O->>R: 触发审查（上下文隔离）
        R->>R: 三维检查
        R-->>O: 审查报告（PASS/FAIL）
        alt STATUS == PASS
            O-->>U: 审查通过
        else STATUS == FAIL
            O->>A: Refinery Mode
            A->>A: 逐项修复
        end
    end

    alt 超限未通过
        O-->>U: ESCALATION 报警
    end

    Note over U,A: 技术选型（如有）
    alt 存在选型对比
        A->>U: 列举选型方案
        U->>A: 整体答复
        A->>A: 更新架构
        Note over U,R: 重新进入审查
    end

    Note over U,O: 最终确认
    O->>U: 展示架构文档 + 审查摘要
    U->>O: 确认交付
```

## 3. Executive Summary (决策摘要)

### 一句话价值
将产品规格自动转化为经过多 AI 对抗审查的高质量架构文档，前期苏格拉底式澄清最大化减少后期返工。

### MVP 裁剪报告
- ✅ 保留：架构师角色、苏格拉底式澄清、多轮审查、双向覆盖、接口/协议定义、架构可视化、变更标注
- ⚠️ 应该级：技术选型对比流程、Codex 自动化审查
- ❌ 排除：业务代码生成、任务拆解（tasks.md）、跨迭代架构关联

### 风险提示
| 风险 | 来源 | 状态 |
|------|------|------|
| Codex 审查失败可能中断审查链 | Round 2 Codex #001 | ✅ 已修复（生成错误报告保持链完整） |
| 架构修复流程缺失导致审查无法闭环 | Round 1 Claude #001 | ✅ 已修复（新增 Refinery Mode） |
| Reviewer 上下文污染导致审查不可复现 | Round 1 Claude #002 | ✅ 已修复（新增上下文隔离） |
| Data Dictionary 行业术语未定义 | Round 2 Codex #002 | ⚠️ MINOR，不影响可执行性 |
