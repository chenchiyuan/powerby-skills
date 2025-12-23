# Bug文档元数据设计方案

## 元数据字段设计

### 基础信息
```yaml
bug_id: "bug-001"                           # Bug唯一标识
title: "用户登录后token验证失败"              # Bug标题
description: "用户登录成功后访问需要认证的API时返回401错误"  # 简要描述
severity: "P1"                               # 严重程度: P0/P1/P2
priority: "high"                             # 优先级: critical/high/medium/low
status: "fixed"                              # 状态: open/in_progress/fixed/deprecated
category: "security"                         # 分类: security/performance/ui/logic/data
```

### 生命周期管理
```yaml
discovered_in: "001-task-manager"            # 发现所在迭代
discovered_at: "2025-12-23T10:00:00Z"       # 发现时间
discovered_by: "user123"                    # 发现者
fixed_in: "001-task-manager"                 # 修复所在迭代
fixed_at: "2025-12-24T15:30:00Z"            # 修复时间
fixed_by: "developer456"                    # 修复者
regression_in: null                         # 回归所在迭代（如果有）
```

### 关联信息
```yaml
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
```

### 技术信息
```yaml
reproduction_steps:                         # 复现步骤
  - "用户登录系统"
  - "获取JWT token"
  - "调用需要认证的API"
  - "收到401未授权错误"

environment:                                # 环境信息
  os: "macOS 14.0"
  browser: "Chrome 120.0"
  server: "Node.js 18.0"
  database: "PostgreSQL 14.0"

error_logs:                                 # 错误日志
  - type: "server"
    content: "JWT token validation failed..."
  - type: "client"
    content: "401 Unauthorized"

related_issues:                             # 相关问题
  - "bug-002"                               # 相关Bug ID
  - "#123"                                  # GitHub Issue
  - "REQ-456"                               # 需求文档
```

### 修复信息
```yaml
root_cause: "JWT token过期时间设置过短，导致API调用时token已失效"  # 根因分析
fix_summary: "将token过期时间从30分钟延长到2小时，并添加token刷新机制"  # 修复摘要
testing_notes: "新增了token过期测试用例，覆盖边界条件"              # 测试说明
prevention_measures: "添加token自动刷新机制，避免用户操作中断"     # 预防措施
```

## 关联机制设计

### 1. 迭代关联
```markdown
## 与迭代的关联关系

发现迭代 (discovered_in)
├── 包含首次发现该Bug的迭代信息
└── 关联到 docs/iterations/{discovered_in}/

修复迭代 (fixed_in)
├── 包含实际修复该Bug的迭代信息
└── 关联到 docs/iterations/{fixed_in}/

相关迭代 (related_iterations)
├── 包含受该Bug影响或相关的其他迭代
└── 用于追踪Bug的跨迭代影响
```

### 2. 文档关联
```markdown
## 文档关联类型

defines (定义)
├── PRD文档定义了需求，Bug描述了需求相关的缺陷
└── 影响: docs/iterations/*/prd.md

defines_design (设计定义)
├── 架构文档定义了设计，Bug与设计实现相关
└── 影响: docs/iterations/*/architecture.md

impacts (影响)
├── Bug影响的功能模块
└── 影响: docs/iterations/*/tasks.md

fixed_by (修复)
├── 修复方案影响了哪些文档
└── 影响: docs/iterations/*/implementation-report.md

relates_to (关联)
├── 存在关联关系但影响较小
└── 影响: 各类文档
```

### 3. 追踪关系
```markdown
## Bug追踪关系

Bug <-> Bug
├── related_issues: [bug-002, bug-003]
├── regression: bug-001 在 bug-002 修复后再次出现
└── duplicate: bug-004 与 bug-001 是同一个问题

Bug <-> Requirement
├── related_issues: ["REQ-123"]
├── requirement_change: Bug由需求变更引起
└── requirement_gap: Bug源于需求不明确

Bug <-> Task
├── related_issues: ["TASK-456"]
├── task_related: Bug与任务实现相关
└── task_blocker: Bug阻塞了任务执行
```

## 索引系统设计

### 1. 全局索引 (docs/bugs/index.md)
```markdown
# 项目Bug总览

## 统计信息
- 总Bug数: 15
- 未修复: 3
- 已修复: 11
- 已废弃: 1

## 按状态分类
### 未修复 (3)
- [bug-001](global/bug-001-login-issue.md) - P1
- [bug-005](global/bug-005-memory-leak.md) - P0
- [bug-012](categories/security/bug-012-sql-injection.md) - P0

### 已修复 (11)
[...]

## 按迭代分类
### 001-task-manager (5)
- [bug-001](global/bug-001-login-issue.md)
- [bug-002](001-task-manager/bug-002-ui-error.md)
[...]

### 002-payment-system (3)
[...]

## 按严重程度分类
### P0 (2)
[...]

### P1 (8)
[...]

### P2 (5)
[...]
```

### 2. 迭代索引 (docs/iterations/{id}/bugs/index.md)
```markdown
# 001-task-manager - Bug列表

## 概述
- 总计: 5个Bug
- 发现: 3个
- 修复: 2个
- 影响迭代: 当前迭代及后续迭代

## Bug列表
### 本迭代发现并修复 (2)
- [bug-002](bug-002-ui-error.md) - UI显示错误 - 已修复
- [bug-003](bug-003-data-validation.md) - 数据验证缺失 - 已修复

### 本迭代发现，后续迭代修复 (1)
- [bug-001](global/bug-001-login-issue.md) - 登录验证失败 - 在002中修复

### 后续迭代发现，影响本迭代 (2)
- [bug-007](global/bug-007-performance-issue.md) - 性能问题 - 影响当前架构
- [bug-010](global/bug-010-security-issue.md) - 安全漏洞 - 影响当前实现

## 关联文档
- [PRD](prd.md) - 3个相关Bug
- [架构](architecture.md) - 2个相关Bug
- [任务](tasks.md) - 1个相关Bug
```

### 3. 分类索引 (docs/bugs/categories/{category}/index.md)
```markdown
# 安全相关Bug

## 概述
- 总计: 4个安全相关Bug
- 未修复: 1个
- 已修复: 3个

## Bug列表
### SQL注入 (1)
- [bug-012](bug-012-sql-injection.md) - P0 - 已修复

### XSS攻击 (1)
- [bug-008](bug-008-xss-vulnerability.md) - P1 - 已修复

### 身份认证 (2)
- [bug-001](global/bug-001-login-issue.md) - P1 - 已修复
- [bug-015](global/bug-015-session-hijack.md) - P0 - 未修复

## 安全修复建议
[基于历史Bug总结的预防措施...]
```

## 自动化生成机制

### 1. 关联文档自动发现
```python
def extract_document_relations(bug_content):
    """自动提取Bug文档中关联的其他文档"""
    relations = []

    # 查找Markdown链接
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', bug_content)

    for text, path in links:
        if 'docs/iterations/' in path:
            doc_type = identify_document_type(path)
            relations.append({
                'text': text,
                'path': path,
                'type': doc_type,
                'relation': 'mentioned'
            })

    return relations
```

### 2. 统计信息自动更新
```python
def update_bug_statistics():
    """更新Bug统计信息"""
    stats = {
        'total': 0,
        'by_status': {},
        'by_severity': {},
        'by_iteration': {}
    }

    for bug_file in glob.glob('docs/bugs/**/*.md'):
        metadata = parse_bug_metadata(bug_file)
        stats['total'] += 1

        # 统计各维度
        stats['by_status'][metadata['status']] += 1
        stats['by_severity'][metadata['severity']] += 1
        stats['by_iteration'][metadata['discovered_in']] += 1

    return stats
```

### 3. 索引页面自动生成
```python
def generate_bug_index():
    """生成Bug索引页面"""
    template = load_template('bug-index-template.md')
    stats = update_bug_statistics()

    return template.render(
        total=stats['total'],
        open=stats['by_status'].get('open', 0),
        fixed=stats['by_status'].get('fixed', 0),
        by_severity=stats['by_severity'],
        recent_bugs=get_recent_bugs()
    )
```

## 与PowerBy流程的集成

### 1. 在powerby-command中的使用
```markdown
在P7阶段代码审查时：

**检查项目Bug状态**
```bash
# 检查是否有未修复的P0/P1 Bug
docs/bugs/index.md 中查看 status=open 且 severity=P0/P1

**关联Bug到审查**
- 在 code-review-report.md 中引用相关Bug
- 确保所有P0/P1 Bug已修复
- 记录新发现的Bug
```
```

### 2. 在powerby-bugfix中的使用
```markdown
Bug修复流程中：

**Bug文档创建**
- 自动生成标准元数据
- 关联到相关迭代和文档
- 更新全局索引

**修复完成**
- 更新fixed_in、fixed_at等字段
- 生成修复总结
- 更新相关迭代的Bug列表
```
```

这个方案的核心优势在于：**统一管理、强关联、自动更新**，完美契合PowerBy的文档驱动理念！
