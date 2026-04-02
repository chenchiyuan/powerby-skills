# PowerBy vNext 整体流程图

**版本**: 2.0.0  
**日期**: 2026-04-01  
**状态**: 设计完成

---

## 核心理念

**执行是约束还原的过程**。问题应该尽早发现解决，越早发现成本越小。我们的交付都是为了让整体损耗最小，效果更优。

每次整体结果交付都必须触发 Review，确保本轮产物与目标对齐还原：
- 功能是否对齐还原产品
- 架构是否对齐还原功能/产品
- 实现是否对齐还原架构

---

## 1. 总循环框架

```mermaid
graph LR
    Think[Think<br/>探讨与开创] --> Plan[Plan<br/>规划与约束]
    Plan --> PlanReview[Review<br/>规格审查]
    PlanReview --> Build[Build<br/>实现与还原]
    Build --> BuildReview[Review<br/>实现审查]
    BuildReview --> Test[Test<br/>测试与质量]
    Test --> Ship[Ship<br/>交付与发布]
    Ship --> Reflect[Reflect<br/>复盘与改进]
    Reflect -.->|Retro-Learn| Think
    
    style Think fill:#e1f5ff
    style Plan fill:#fff4e1
    style PlanReview fill:#ffe1f5
    style Build fill:#e1ffe1
    style BuildReview fill:#ffe1f5
    style Test fill:#f5e1ff
    style Ship fill:#ffe1e1
    style Reflect fill:#e1e1ff
```

### 1.1 七个阶段 + Review 门禁

| 阶段 | 英文 | 核心职责 | 关键产物 | Review 门禁 |
|------|------|---------|---------|-----------|
| 探讨与开创 | Think | 挑战前提、探索可能性 | 需求理解、问题定义 | - |
| 规划与约束 | Plan | 将探讨转化为可执行规格 | PRD、架构设计、工程规划 | 规格审查 |
| 实现与还原 | Build | 基于规格还原为高质量代码 | 代码实现 | 实现审查 |
| 测试与质量 | Test | 通过自动化测试验证功能 | 测试报告 | - |
| 交付与发布 | Ship | 将代码交付到生产环境 | 发布记录 | - |
| 复盘与改进 | Reflect | 总结经验教训并持续改进 | 复盘报告 | - |

### 1.2 Review 门禁机制

**核心原则**: 执行是约束还原的过程，每次交付前必须 Review

```mermaid
graph TD
    subgraph "Plan 阶段"
        P1[产品规格 PRD]
        P2[架构设计]
        P3[工程规划]
    end
    
    subgraph "Plan Review 门禁"
        PR1[Review 上轮产出<br/>确保需求目标经过验证]
        PR2[Review 本轮产物<br/>架构是否对齐还原 PRD]
        PR3[Review 本轮产物<br/>工程规划是否对齐还原架构]
    end
    
    subgraph "Build 阶段"
        B1[代码实现]
    end
    
    subgraph "Build Review 门禁"
        BR1[Review 上轮产出<br/>确保架构设计经过验证]
        BR2[Review 本轮产物<br/>实现是否对齐还原架构]
    end
    
    P1 --> P2
    P2 --> P3
    P3 --> PR1
    PR1 --> PR2
    PR2 --> PR3
    PR3 -->|通过| B1
    PR3 -->|不通过| P1
    
    B1 --> BR1
    BR1 --> BR2
    BR2 -->|通过| Test[Test 阶段]
    BR2 -->|不通过| B1
    
    style PR1 fill:#ffe1f5
    style PR2 fill:#ffe1f5
    style PR3 fill:#ffe1f5
    style BR1 fill:#ffe1f5
    style BR2 fill:#ffe1f5
```


### 1.3 Review 触发机制

Review 可以通过以下三种方式触发：

1. **自动触发**: 每次阶段交付前自动触发 Review 门禁
2. **用户主动触发**: 用户可以随时主动触发 Review 流程
3. **上轮产出 Review**: 本轮任务开始之前，先 Review 上轮的产出

---

## 2. 标准流程（统一版）

```mermaid
graph TD
    subgraph Think["Think 探讨与开创"]
        P0[P0: 需求接收]
        P1[P1: 需求澄清]
    end
    
    subgraph Plan["Plan 规划与约束"]
        P3[P3: 产品规格 PRD]
        P4[P4: 架构设计]
        P5[P5: 工程规划]
    end
    
    subgraph PlanReview["Plan Review 门禁"]
        PR1[Review: 需求目标验证]
        PR2[Review: 架构对齐 PRD]
        PR3[Review: 工程对齐架构]
    end
    
    subgraph Build["Build 实现与还原"]
        P6[P6: 代码实现]
    end
    
    subgraph BuildReview["Build Review 门禁"]
        BR1[Review: 架构设计验证]
        BR2[Review: 实现对齐架构]
    end
    
    subgraph Test["Test 测试与质量"]
        P7T[P7: 测试验证]
    end
    
    subgraph Ship["Ship 交付与发布"]
        P8[P8: 交付发布]
    end
    
    subgraph Reflect["Reflect 复盘与改进"]
        Retro[项目复盘]
    end
    
    P0 --> P1
    P1 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> PR1
    PR1 --> PR2
    PR2 --> PR3
    PR3 -->|通过| P6
    PR3 -->|不通过| P3
    
    P6 --> BR1
    BR1 --> BR2
    BR2 -->|通过| P7T
    BR2 -->|不通过| P6
    
    P7T --> P8
    P8 --> Retro
    Retro -.->|Retro-Learn| P0
    
    style Think fill:#e1f5ff
    style Plan fill:#fff4e1
    style PlanReview fill:#ffe1f5
    style Build fill:#e1ffe1
    style BuildReview fill:#ffe1f5
    style Test fill:#f5e1ff
    style Ship fill:#ffe1e1
    style Reflect fill:#e1e1ff
```

### 2.1 阶段映射关系（统一版）

| 总循环阶段 | P0-P8 阶段 | 负责 Skill | 核心产物 | Review 内容 |
|-----------|-----------|-----------|---------|-----------|
| Think | P0, P1 | powerby-product | 需求理解文档 | - |
| Plan | P3, P4, P5 | powerby-product<br/>powerby-architect<br/>powerby-engineer | PRD<br/>架构设计<br/>工程规划 | 需求验证<br/>架构对齐 PRD<br/>工程对齐架构 |
| Build | P6 | powerby-engineer | 代码实现 | 架构验证<br/>实现对齐架构 |
| Test | P7 | powerby-engineer | 测试报告 | - |
| Ship | P8 | powerby-engineer | 发布记录 | - |
| Reflect | - | powerby-reviewer | 复盘报告 | - |

**说明**: 
- powerby-product 和 powerby-asp-product 已统一为 powerby-product
- powerby-architect 和 powerby-asp-architect 已统一为 powerby-architect
- powerby-product 支持两种模式：标准模式（P0-P1-P3）和深度探讨模式（OFFICE_HOURS-DISCOVERY-DRAFTING-REFINING-REVIEWING-VISUALIZING-CONFIRMATION）

---


## 3. 核心 Skill 编排链路（骨架版）

基于"核心骨架就是不可或缺的环节"原则，以下是必须的 Skill：

```mermaid
graph TD
    subgraph Think["Think 探讨与开创"]
        Product1[powerby-product<br/>产品经理]
    end
    
    subgraph Plan["Plan 规划与约束"]
        Product2[powerby-product<br/>产品经理]
        Architect[powerby-architect<br/>架构师]
        Engineer1[powerby-engineer<br/>工程师]
    end
    
    subgraph PlanReview["Plan Review 门禁"]
        Reviewer1[powerby-reviewer<br/>审查者]
    end
    
    subgraph Build["Build 实现与还原"]
        Engineer2[powerby-engineer<br/>工程师]
    end
    
    subgraph BuildReview["Build Review 门禁"]
        Reviewer2[powerby-reviewer<br/>审查者]
    end
    
    subgraph Test["Test 测试与质量"]
        Engineer3[powerby-engineer<br/>工程师]
    end
    
    subgraph Ship["Ship 交付与发布"]
        Engineer4[powerby-engineer<br/>工程师]
    end
    
    subgraph Reflect["Reflect 复盘与改进"]
        Reviewer3[powerby-reviewer<br/>复盘者]
    end
    
    Product1 --> Product2
    Product2 --> Architect
    Architect --> Engineer1
    Engineer1 --> Reviewer1
    Reviewer1 -->|通过| Engineer2
    Reviewer1 -->|不通过| Product2
    
    Engineer2 --> Reviewer2
    Reviewer2 -->|通过| Engineer3
    Reviewer2 -->|不通过| Engineer2
    
    Engineer3 --> Engineer4
    Engineer4 --> Reviewer3
    Reviewer3 -.->|Retro-Learn| Product1
    
    style Think fill:#e1f5ff
    style Plan fill:#fff4e1
    style PlanReview fill:#ffe1f5
    style Build fill:#e1ffe1
    style BuildReview fill:#ffe1f5
    style Test fill:#f5e1ff
    style Ship fill:#ffe1e1
    style Reflect fill:#e1e1ff
```

### 3.1 核心 Skill 清单（必不可缺）

| Skill | 角色 | 阶段 | 职责 | 为什么必不可缺 |
|-------|------|------|------|--------------|
| powerby-product | 产品经理 | Think + Plan (P0, P1, P3) | 需求探讨和产品规格定义 | 唯一的需求入口和 PRD 产出者 |
| powerby-architect | 架构师 | Plan (P4) | 架构设计和技术选型 | 唯一的架构设计者和技术选型决策者 |
| powerby-engineer | 工程师 | Plan (P5) + Build (P6) + Test (P7) + Ship (P8) | 工程规划、代码实现、测试验证、交付发布 | 唯一的代码实现者和交付发布者 |
| powerby-reviewer | 审查者 | Plan Review + Build Review + Reflect | 规格审查、实现审查、项目复盘 | 唯一的质量守门人和对齐验证者 |

### 3.2 核心 Skill 输入输出协议

| Skill | 输入 | 输出 | 下游 Skill | Review 内容 |
|-------|------|------|-----------|-----------|
| powerby-product | 用户需求 | PRD | powerby-architect | - |
| powerby-architect | PRD | 架构设计 | powerby-engineer | 架构对齐 PRD |
| powerby-engineer (P5) | 架构设计 | 工程规划 | powerby-reviewer | 工程对齐架构 |
| powerby-reviewer (Plan Review) | PRD + 架构设计 + 工程规划 | Review 报告 | powerby-engineer (P6) 或 powerby-product | 需求验证、架构对齐、工程对齐 |
| powerby-engineer (P6) | 工程规划 | 代码实现 | powerby-reviewer | - |
| powerby-reviewer (Build Review) | 架构设计 + 代码实现 | Review 报告 | powerby-engineer (P7) 或 powerby-engineer (P6) | 架构验证、实现对齐 |
| powerby-engineer (P7) | 代码实现 | 测试报告 | powerby-engineer (P8) | - |
| powerby-engineer (P8) | 测试报告 | 发布记录 | powerby-reviewer | - |
| powerby-reviewer (Reflect) | 发布记录 | 复盘报告 | - | - |

---

## 4. Review 门禁详细机制

### 4.1 Plan Review 门禁

**触发时机**: P5 工程规划完成后

**Review 内容**:
1. **Review 上轮产出**: 确保需求目标本身是经过验证的
2. **Review 架构对齐 PRD**: 架构设计是否对齐还原 PRD
3. **Review 工程对齐架构**: 工程规划是否对齐还原架构设计

**负责 Skill**: powerby-reviewer

**输入**:
- PRD（来自 powerby-product）
- 架构设计（来自 powerby-architect）
- 工程规划（来自 powerby-engineer）

**输出**:
- Review 报告（包含通过/不通过决策和具体问题）

**决策**:
- 通过 → 进入 Build 阶段（P6）
- 不通过 → 返回 Plan 阶段（P3/P4/P5）修复问题

---

### 4.2 Build Review 门禁

**触发时机**: P6 代码实现完成后

**Review 内容**:
1. **Review 上轮产出**: 确保架构设计本身是经过验证的
2. **Review 实现对齐架构**: 代码实现是否对齐还原架构设计

**负责 Skill**: powerby-reviewer

**输入**:
- 架构设计（来自 powerby-architect）
- 代码实现（来自 powerby-engineer）

**输出**:
- Review 报告（包含通过/不通过决策和具体问题）

**决策**:
- 通过 → 进入 Test 阶段（P7）
- 不通过 → 返回 Build 阶段（P6）修复问题

---


### 4.3 用户主动触发 Review

用户可以在任何时候主动触发 Review 流程：

```mermaid
graph TD
    User[用户主动触发 Review] --> Reviewer[powerby-reviewer]
    Reviewer --> Check1{检查当前阶段}
    
    Check1 -->|Plan 阶段| PlanReview[执行 Plan Review]
    Check1 -->|Build 阶段| BuildReview[执行 Build Review]
    Check1 -->|其他阶段| GeneralReview[执行通用 Review]
    
    PlanReview --> Report1[生成 Review 报告]
    BuildReview --> Report2[生成 Review 报告]
    GeneralReview --> Report3[生成 Review 报告]
    
    Report1 --> User
    Report2 --> User
    Report3 --> User
    
    style User fill:#e1f5ff
    style Reviewer fill:#ffe1f5
```

---

## 5. 快速流程（简化版）

快速流程是标准流程的简化版，适用于小需求（工作量 ≤ 3 天，P0 功能 ≤ 5 个）。

```mermaid
graph TD
    subgraph ThinkPlan["Think + Plan 融合"]
        Quick[Quick Planning<br/>快速规划]
    end
    
    subgraph QuickReview["Quick Review 门禁"]
        QR[Review: 规划对齐需求]
    end
    
    subgraph Build["Build 实现与还原"]
        IMP[Implementation<br/>代码实现]
    end
    
    subgraph BuildReview["Build Review 门禁"]
        BR[Review: 实现对齐规划]
    end
    
    subgraph Test["Test 测试与质量"]
        TEST[Testing<br/>测试验证]
    end
    
    subgraph Ship["Ship 交付与发布"]
        SHIP[Shipping<br/>交付发布]
    end
    
    Quick --> QR
    QR -->|通过| IMP
    QR -->|不通过| Quick
    
    IMP --> BR
    BR -->|通过| TEST
    BR -->|不通过| IMP
    
    TEST --> SHIP
    
    style ThinkPlan fill:#e1f5ff
    style QuickReview fill:#ffe1f5
    style Build fill:#e1ffe1
    style BuildReview fill:#ffe1f5
    style Test fill:#f5e1ff
    style Ship fill:#ffe1e1
```

### 5.1 快速流程特点

- **Think + Plan 融合**: 产品理解 + 架构适配 + 工程规划在同一角色完成
- **负责 Skill**: powerby-fullstack（执行）+ powerby-reviewer（Review）
- **适用场景**: 工作量 ≤ 3 天，P0 功能 ≤ 5 个
- **核心产物**: 快速规划文档（包含产品 + 架构 + 工程三视角）
- **Review 门禁**: 简化为两个门禁（Quick Review + Build Review）

---

## 6. Bugfix 流程（简化版）

Bugfix 流程是标准流程的简化版，适用于 Bug 修复。

```mermaid
graph TD
    subgraph Think["Think 探讨与开创"]
        Diag[Diagnosis<br/>问题诊断]
    end
    
    subgraph Plan["Plan 规划与约束"]
        Fix[Fix Planning<br/>修复规划]
    end
    
    subgraph PlanReview["Plan Review 门禁"]
        PR[Review: 修复方案对齐问题]
    end
    
    subgraph Build["Build 实现与还原"]
        IMP[Implementation<br/>修复实现]
    end
    
    subgraph BuildReview["Build Review 门禁"]
        BR[Review: 实现对齐方案]
    end
    
    subgraph Test["Test 测试与质量"]
        TEST[Testing<br/>回归测试]
    end
    
    subgraph Ship["Ship 交付与发布"]
        SHIP[Shipping<br/>交付发布]
    end
    
    Diag --> Fix
    Fix --> PR
    PR -->|通过| IMP
    PR -->|不通过| Fix
    
    IMP --> BR
    BR -->|通过| TEST
    BR -->|不通过| IMP
    
    TEST --> SHIP
    
    style Think fill:#e1f5ff
    style Plan fill:#fff4e1
    style PlanReview fill:#ffe1f5
    style Build fill:#e1ffe1
    style BuildReview fill:#ffe1f5
    style Test fill:#f5e1ff
    style Ship fill:#ffe1e1
```

### 6.1 Bugfix 流程特点

- **Think 阶段**: 问题诊断（证据驱动、三层诊断）
- **Plan 阶段**: 修复规划（至少 2 个备选方案）
- **负责 Skill**: powerby-bugfix（执行）+ powerby-reviewer（Review）
- **适用场景**: Bug 修复、问题诊断
- **核心产物**: 诊断报告 + 修复方案
- **Review 门禁**: Plan Review + Build Review

---


## 7. Retro-Learn 自我改进循环

```mermaid
graph LR
    Retro[Retrospective<br/>项目复盘] --> Learn[Learn<br/>提取经验]
    Learn --> Update[Update<br/>更新协议]
    Update --> Apply[Apply<br/>应用到下一个项目]
    Apply -.->|持续改进| Retro
    
    style Retro fill:#e1e1ff
    style Learn fill:#ffe1f5
    style Update fill:#fff4e1
    style Apply fill:#e1ffe1
```

### 7.1 Retro-Learn 四阶段

| 阶段 | 职责 | 负责 Skill | 核心产物 |
|------|------|-----------|---------|
| Retrospective | 项目复盘，识别问题和亮点 | powerby-reviewer | 复盘报告 |
| Learn | 提取经验教训，形成可复用知识 | powerby-reviewer | 经验库 |
| Update | 更新协议、流程、Skill | powerby-reviewer | 更新记录 |
| Apply | 应用到下一个项目 | 所有 Skill | 实践验证 |

---

## 8. 流程选择决策树

```mermaid
graph TD
    Start[收到需求] --> Q1{是 Bug 修复?}
    Q1 -->|是| Bugfix[Bugfix 流程]
    Q1 -->|否| Q2{工作量 ≤ 3 天?}
    
    Q2 -->|是| Q3{P0 功能 ≤ 5 个?}
    Q2 -->|否| Standard[标准流程]
    
    Q3 -->|是| Quick[快速流程]
    Q3 -->|否| Standard
    
    style Standard fill:#e1f5ff
    style Quick fill:#fff4e1
    style Bugfix fill:#ffe1e1
```

### 8.1 流程选择标准

| 流程类型 | 适用场景 | 工作量 | P0 功能数 | 核心 Skill |
|---------|---------|--------|----------|-----------|
| 标准流程 | 常规需求开发 | > 3 天 | > 5 个 | powerby-product<br/>powerby-architect<br/>powerby-engineer<br/>powerby-reviewer |
| 快速流程 | 临时小需求 | ≤ 3 天 | ≤ 5 个 | powerby-fullstack<br/>powerby-reviewer |
| Bugfix 流程 | Bug 修复 | 不限 | 不限 | powerby-bugfix<br/>powerby-reviewer |

---

## 9. 核心原则总结

### 9.1 执行是约束还原的过程

- **功能对齐还原产品**: 架构设计必须对齐还原 PRD
- **架构对齐还原功能**: 工程规划必须对齐还原架构设计
- **实现对齐还原架构**: 代码实现必须对齐还原架构设计

### 9.2 问题尽早发现解决

- **Plan Review 门禁**: 在 Build 之前发现问题，成本最小
- **Build Review 门禁**: 在 Test 之前发现问题，成本较小
- **上轮产出 Review**: 确保需求目标本身是经过验证的

### 9.3 Review 触发机制

1. **自动触发**: 每次阶段交付前自动触发 Review 门禁
2. **用户主动触发**: 用户可以随时主动触发 Review 流程
3. **上轮产出 Review**: 本轮任务开始之前，先 Review 上轮的产出

### 9.4 核心 Skill 统一

- **powerby-product**: 统一标准模式和深度探讨模式（原 powerby-asp-product）
- **powerby-architect**: 统一标准模式和深度探讨模式（原 powerby-asp-architect）
- **powerby-reviewer**: 负责所有 Review 门禁和项目复盘

---

## 10. 总结

### 10.1 核心流程

PowerBy vNext 的核心流程是 **Think → Plan → Review → Build → Review → Test → Ship → Reflect** 八阶段总循环（包含两个 Review 门禁）。

### 10.2 核心 Skill（必不可缺）

1. **powerby-product** - 产品经理（Think + Plan P3）
2. **powerby-architect** - 架构师（Plan P4）
3. **powerby-engineer** - 工程师（Plan P5 + Build + Test + Ship）
4. **powerby-reviewer** - 审查者（Plan Review + Build Review + Reflect）

### 10.3 Review 门禁机制

- **Plan Review**: 确保架构对齐 PRD、工程对齐架构
- **Build Review**: 确保实现对齐架构
- **三种触发方式**: 自动触发、用户主动触发、上轮产出 Review

### 10.4 流程变体

- **标准流程**: 完整的 Think → Plan → Review → Build → Review → Test → Ship → Reflect
- **快速流程**: Think + Plan 融合，简化 Review 门禁
- **Bugfix 流程**: 简化版标准流程，保留 Review 门禁

---

**文档状态**: 设计完成  
**版本**: 2.0.0  
**创建日期**: 2026-04-01  
**修订说明**: 
- 统一 powerby-product 和 powerby-asp-product
- 统一 powerby-architect 和 powerby-asp-architect
- 引入 Review 门禁机制（Plan Review + Build Review）
- 明确核心 Skill 清单（4 个必不可缺）
- 强调执行是约束还原的过程
