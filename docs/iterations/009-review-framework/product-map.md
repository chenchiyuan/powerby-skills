# Product Map: 还原式项目评审框架

## 视图 A: 功能全景树

```mermaid
mindmap
  root((还原式项目评审框架))
    范围与证据
      ProjectScope
        接入项目资料
        定义评审范围
        生成资料清单
      EvidenceCollector
        采集标准化证据
        打元信息标签
      ConflictResolver
        证据优先级判断
        冲突识别与保留
        优先级决议规则
    事实还原
      ProductReconstructor
        Goal 产品目标
        Role 用户角色
        Scenario 使用场景
        Constraint 约束
        Non-goal 非目标
      FeatureReconstructor
        Feature 功能清单
        Rule 业务规则
        Boundary 功能边界
        Feature State 功能状态
    关系与差异
      RelationBuilder
        Goal-Feature 追踪
        Rule-Feature 约束
        覆盖率统计
      GapAnalyzer
        需求-实现差异
        对象缺失
        链路断点
    报告输出
      ReportComposer
        Markdown 报告
        追踪矩阵
        证据索引
    V2 扩展
      架构事实还原
      实现事实还原
      验证事实还原
```

## 视图 B: 评审执行流程

```mermaid
sequenceDiagram
    participant U as 评审执行者
    participant PS as ProjectScope
    participant EC as EvidenceCollector
    participant CR as ConflictResolver
    participant PR as ProductReconstructor
    participant FR as FeatureReconstructor
    participant RB as RelationBuilder
    participant GA as GapAnalyzer
    participant RC as ReportComposer

    U->>PS: 提供项目路径和评审范围
    PS->>PS: 扫描项目结构
    alt 项目路径不存在
        PS-->>U: 返回 failed
    else 扫描成功
        PS->>EC: project_metadata + resource_inventory
    end

    EC->>EC: 采集并标准化证据
    alt 部分文件不可读
        EC-->>EC: 标记跳过，返回 partial
    end
    EC->>CR: evidence_registry

    CR->>CR: 分析证据优先级
    CR->>CR: 识别冲突并保留
    Note over CR: 新文档优先于旧文档<br/>代码优先于旧文档<br/>冲突显式保留

    CR->>PR: current_facts (产品事实证据)
    PR->>PR: 还原 Goal/Role/Scenario
    alt 无产品文档
        PR-->>PR: 返回 partial + 空 Catalog
    end

    PR->>FR: 产品对象 + current_facts
    FR->>FR: 还原 Feature/Rule/Boundary
    alt 仅有代码证据
        FR-->>FR: 标注 source: code_only
    end

    FR->>RB: 产品对象 + 功能对象
    RB->>RB: 建立 Goal-Feature 追踪关系
    Note over RB: 证据不足时<br/>标注 confidence: inferred

    RB->>GA: 对象 + 关系 + 冲突
    GA->>GA: 识别差异与缺口

    GA->>RC: 全部上游数据
    RC->>RC: 编排 Markdown 报告
    RC-->>U: 输出 review_report.md
```

## 视图 C: 决策摘要

### 一句话价值
基于项目自身材料，将任意项目从产品目标到功能边界逐层还原为结构化对象与追踪关系网络，系统性地识别需求-实现偏差。

### MVP 裁剪报告

| 范围 | 内容 | V1/V2 |
|------|------|-------|
| V1 核心链路 | 产品 → 功能 → 关系 → 差异 | V1 |
| V1 基础设施 | Skill 协议 + 数据模型 + 证据采集 | V1 |
| V2 扩展 | 架构事实还原 | V2 |
| V2 扩展 | 实现事实还原 | V2 |
| V2 扩展 | 验证事实还原 | V2 |

**V1 包含 8 个 Skill**：ProjectScope、EvidenceCollector、ConflictResolver、ProductReconstructor、FeatureReconstructor、RelationBuilder、GapAnalyzer、ReportComposer

**V2 扩展 3 个 Skill**：ArchitectureReconstructor、ImplementationReconstructor、VerificationReconstructor

### 风险提示

| 风险 | 说明 | 缓解措施 |
|------|------|---------|
| 无产品文档 | 部分项目缺少 PRD，产品还原可能不完整 | Empty State 处理：返回 partial + 空 Catalog |
| 证据冲突 | 文档与代码不一致是常态 | 显式保留冲突，不自动和解 |
| 推断边界 | AI 可能过度推断功能关系 | 严格的 confidence 标注 + 不强行连线 |
