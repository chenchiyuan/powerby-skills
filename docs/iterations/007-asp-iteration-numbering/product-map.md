# Product Panorama: ASP 迭代编号体系

## 1. The Big Picture

```mermaid
mindmap
  root((ASP 迭代编号体系))
    迭代创建
      US-001 自动递增编号
        规则: max json+目录 +1
        规则: 冲突解决策略
      US-004 自动提取迭代名
        规则: kebab-case 英文短名
        规则: 用户可确认或修改
    迭代复用
      US-002 继续已有迭代
        规则: 文件到阶段映射表
        边界: 迭代不存在时提示
        边界: json无记录时补录
    架构关联
      US-003 指定已有迭代
        规则: 检查产品交付物完整性
        边界: 缺失时提示补全
        边界: 未指定时列出选择
    文档兼容
      US-005 ASP与P0-P8共存
        规则: 不覆盖已有文档
```

## 2. Core Journey

```mermaid
sequenceDiagram
    participant U as 用户
    participant ASP as ASP Orchestrator
    participant FS as 文件系统
    participant JSON as iterations.json

    U->>ASP: /powerby-asp "需求描述"
    ASP->>JSON: 读取最大编号
    ASP->>FS: 扫描 docs/iterations/ 目录
    ASP->>ASP: max(json, 目录) + 1
    ASP->>ASP: 提取 kebab-case 迭代名
    ASP-->>U: 确认迭代目录 {id}-{name}
    alt 用户确认
        ASP->>FS: 创建迭代目录 + prd_logs/
        ASP->>JSON: 写入新迭代记录
        ASP-->>U: 进入 DISCOVERY 阶段
    else 用户修改迭代名
        ASP->>ASP: 使用新迭代名
        ASP->>FS: 创建迭代目录 + prd_logs/
        ASP->>JSON: 写入新迭代记录
        ASP-->>U: 进入 DISCOVERY 阶段
    end

    Note over U,ASP: 后续：ASP 架构流程

    U->>ASP: /powerby-asp-arch 指定迭代编号
    ASP->>FS: 检查产品交付物
    alt 交付物完整
        ASP->>FS: 创建 arch_logs/
        ASP-->>U: 进入架构设计流程
    else 交付物缺失
        ASP-->>U: 提示缺失文件，建议先完成产品流程
    end
```

## 3. What we cut (MVP Strategy)

- 无功能裁剪。proposal.md 中所有 REQ 均已在 spec.md 中完整覆盖。
- 2 个 MINOR 建议延期处理：P0-P8 文件保护清单显式化、迭代名提取算法确定性定义。

## 4. Risk Alerts

- Round 1 (Claude) 指出编号双源逻辑存在冲突风险（已修复：明确 max 取值策略），但实际使用中仍需注意手动创建目录可能导致编号跳跃。
- Round 2 (Codex) 指出 US-003 范围加严问题（已修复：移除 product-map.md 前置要求），需注意后续如果 ASP 流程变更交付物清单，需同步更新 proposal 和 spec。
