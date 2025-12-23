---
bug_id: "bug-001"
title: "[问题简述]"
description: "[简要描述问题]"
severity: "P1"                               # P0/P1/P2
priority: "high"                             # critical/high/medium/low
status: "open"                               # open/in_progress/fixed/deprecated
category: "security"                         # security/performance/ui/logic/data

# 生命周期管理
discovered_in: "001-task-manager"            # 发现所在迭代
discovered_at: "2025-12-23T10:00:00Z"       # 发现时间 (ISO 8601)
discovered_by: "username"                   # 发现者
fixed_in: null                              # 修复所在迭代 (null表示未修复)
fixed_at: null                              # 修复时间 (null表示未修复)
fixed_by: null                              # 修复者 (null表示未修复)
regression_in: null                         # 回归所在迭代 (可选)

# 关联信息
related_iterations:                         # 相关迭代列表
  - "001-task-manager"
  - "002-payment-system"

related_documents:                          # 关联文档
  - path: "docs/iterations/001-task-manager/prd.md"
    type: "prd"                            # prd/architecture/tasks/implementation
    relation: "defines_requirement"         # defines/impacts/fixed_by/relates_to
  - path: "docs/iterations/001-task-manager/architecture.md"
    type: "architecture"
    relation: "defines_design"

affected_modules:                           # 影响模块
  - "auth"
  - "user-management"
  - "api-gateway"

tags:                                       # 标签
  - "authentication"
  - "jwt"
  - "api-security"

# 技术信息
reproduction_steps:                         # 复现步骤
  - "步骤1: [操作描述]"
  - "步骤2: [操作描述]"
  - "步骤3: [预期结果]"
  - "实际结果: [实际发生了什么]"

environment:                                # 环境信息
  os: "macOS 14.0"
  browser: "Chrome 120.0"
  server: "Node.js 18.0"
  database: "PostgreSQL 14.0"

error_logs:                                 # 错误日志
  - type: "server"
    content: |
      JWT token validation failed: Token expired
      at verifyToken (auth.js:45)
      at processRequest (api.js:123)
  - type: "client"
    content: |
      401 Unauthorized: Invalid or expired token

related_issues:                             # 相关问题
  - "bug-002"                               # 相关Bug ID
  - "#123"                                  # GitHub Issue
  - "REQ-456"                               # 需求文档

# 修复信息
root_cause: "[根因分析：为什么会出现这个问题]"        # 根因分析
fix_summary: "[修复摘要：如何修复的]"                # 修复摘要
testing_notes: "[测试说明：如何验证修复]"            # 测试说明
prevention_measures: "[预防措施：如何避免再次发生]"  # 预防措施
---

# Bug-Fix Report #{id} - [问题简述]

## 一、问题报告

### 问题描述
[简明扼要描述问题表现]

### 证据链
- **错误日志**: [具体日志内容]
- **堆栈信息**: [异常堆栈]
- **代码片段**: [相关代码]
- **环境信息**: [系统/版本等]

### 复现逻辑
[详细描述如何稳定复现该问题]

### 影响评估
- **影响范围**: [影响的功能/模块]
- **严重程度**: P0/P1/P2
- **紧急程度**: 高/中/低

---

## 二、诊断分析

### 代码路径分析
[Mermaid流程图描述执行路径]

### 根因定位
[明确指出问题根本原因]

### 影响范围
[分析是否影响其他模块]

### 修复建议
[初步修复思路]

---

## 三、修复计划

### 修复方案
[记录最终选择的修复方案]

### 任务清单
- [ ] TASK-{id}-001: [具体修复任务1]
  - 描述: [详细描述]
  - 优先级: P0/P1/P2
  - 预估工时: X小时
  - 验收标准: [具体标准]
  - 状态: 待开始/进行中/已完成

- [ ] TASK-{id}-002: [具体修复任务2]
  - 描述: [详细描述]
  - 优先级: P0/P1/P2
  - 预估工时: X小时
  - 验收标准: [具体标准]
  - 状态: 待开始/进行中/已完成

### 风险评估
- **潜在风险**: [可能引入的新问题]
- **缓解措施**: [如何避免风险]

---

## 四、实施修复

### 执行记录
[记录实际执行过程，与计划对比]

### 临时文件使用记录
本次修复过程中创建了以下临时文件：

#### 分析脚本
- `temp_scripts/analysis/bug-{id}-code-analyzer.{py|js|sh}` - [用途说明]
- `temp_scripts/logs/bug-{id}-analysis.log` - [分析结果说明]

#### 验证脚本
- `temp_scripts/validation/bug-{id}-test-{component}.{py|js}` - [用途说明]
- `temp_scripts/validation/bug-{id}-regression-check.{py|js|sh}` - [用途说明]

#### 模拟数据
- `temp_scripts/mock/bug-{id}-test-data.{json|csv|yaml}` - [数据说明]
- `temp_scripts/mock/bug-{id}-scenario-{name}.{py|js}` - [场景说明]

#### 清理状态
- [ ] 分析脚本已删除
- [ ] 验证脚本已删除
- [ ] 模拟数据已删除
- [ ] 临时日志已删除
- [ ] temp_scripts目录已清理（如果为空）

### 修改明细
[列出所有代码修改]

---

## 五、验证交付

### 回归测试
[证明修复有效]

### 防御性变更
[是否添加了断言或快速失败逻辑]

### 临时文件清理验证
**清理检查清单**：
- [ ] `temp_scripts/analysis/` 目录已清空
- [ ] `temp_scripts/validation/` 目录已清空
- [ ] `temp_scripts/mock/` 目录已清空
- [ ] `temp_scripts/logs/` 目录已清空
- [ ] `temp_scripts/` 目录已删除（如果为空）
- [ ] 工作目录整洁，无遗留临时文件
- [ ] 项目目录结构完整

**清理命令记录**：
```bash
# 示例清理命令
find temp_scripts -name "*bug-{id}*" -type f -delete
find temp_scripts -type d -empty -delete
[ -d temp_scripts ] && [ -z "$(ls -A temp_scripts)" ] && rmdir temp_scripts
```

### 代码交付
```diff
[提供diff格式的代码变更]
```

### 总结
- **修复时间**: [实际用时]
- **效果验证**: [是否完全解决]
- **临时文件**: [已清理/未清理（说明原因）]
- **经验总结**: [学到的教训]
- **预防措施**: [如何避免类似问题再次发生]
