# Bug文档归档管理指南

## 概述

本文档介绍如何在PowerBy项目中管理和归档Bug文档，实现与主流程文档的统一管理和强关联。

## 目录结构

```
docs/
└── bugs/                          # Bug文档根目录
    ├── global/                    # 全局Bug（跨迭代）
    │   ├── bug-001-[问题标识].md
    │   └── index.md
    ├── categories/                # 按分类管理
    │   ├── security/              # 安全相关Bug
    │   ├── performance/           # 性能问题
    │   ├── ui/                    # 界面问题
    │   └── logic/                 # 逻辑问题
    ├── templates/                 # 模板和工具
    │   ├── bug-template.md        # Bug文档模板
    │   └── bug-index-template.md  # 索引模板
    ├── scripts/                   # 自动化脚本
    │   └── generate-bug-index.py  # 索引生成脚本
    ├── metadata-schema.md         # 元数据规范
    └── index.md                   # 全局Bug索引
```

## 核心特性

### 1. 统一管理
- 所有Bug文档统一存放在 `docs/bugs/` 目录下
- 与主流程文档（PRD、架构等）平级管理
- 保持PowerBy文档体系的一致性

### 2. 强关联
- Bug文档与迭代、PRD、架构等文档建立关联
- 支持跨迭代追踪和影响分析
- 便于理解Bug的上下文和修复背景

### 3. 自动化索引
- 自动生成全局Bug索引
- 按迭代、分类、严重程度等维度分类
- 实时更新统计信息

### 4. 元数据驱动
- 完整的YAML元数据字段
- 支持生命周期管理
- 便于数据分析和报告

## 使用流程

### 1. 创建Bug文档

#### 方式1：使用模板
```bash
# 复制模板
cp docs/bugs/templates/bug-template.md docs/bugs/global/bug-002-[问题标识].md

# 编辑文档
vim docs/bugs/global/bug-002-[问题标识].md
```

#### 方式2：从powerby-bugfix技能创建
```bash
# 激活Bug-Fix技能
/powerby-bugfix

# 技能会自动在docs/bugs/下创建文档
```

### 2. 更新元数据

确保Bug文档包含完整的YAML元数据：

```yaml
---
bug_id: "bug-001"
title: "[问题简述]"
severity: "P1"              # P0/P1/P2
status: "open"              # open/in_progress/fixed/deprecated
category: "security"        # security/performance/ui/logic/data
discovered_in: "001-task-manager"
related_documents:
  - path: "docs/iterations/001-task-manager/prd.md"
    type: "prd"
    relation: "defines_requirement"
---
```

### 3. 生成索引

#### 手动生成
```bash
cd /path/to/project
python3 docs/bugs/scripts/generate-bug-index.py --all
```

#### 集成到Git Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 docs/bugs/scripts/generate-bug-index.py --global
```

### 4. 验证文档

```bash
python3 docs/bugs/scripts/generate-bug-index.py --validate
```

## 分类体系

### 按范围分类

| 目录 | 说明 | 示例 |
|------|------|------|
| `global/` | 全局性Bug，跨多个迭代 | token验证问题 |
| `{iteration}/` | 迭代特定Bug | UI显示错误 |

### 按类别分类

| 类别 | 说明 | 优先级 |
|------|------|--------|
| security | 安全漏洞 | P0 |
| performance | 性能问题 | P1 |
| ui | 界面问题 | P2 |
| logic | 逻辑错误 | P1 |
| data | 数据问题 | P1 |

## 最佳实践

### 1. 命名规范

**Bug ID**: `bug-001`, `bug-002`, ...
**文件名**: `bug-{id}-{简述}.md`

### 2. 元数据要求

**必要字段**:
- `bug_id`: 唯一标识
- `title`: Bug标题
- `severity`: 严重程度
- `status`: 状态
- `category`: 分类
- `discovered_in`: 发现迭代
- `discovered_at`: 发现时间

### 3. 关联管理

每个Bug至少关联一个：
- 发现迭代的PRD文档
- 相关的架构文档
- 可能受影响的任务文档

### 4. 生命周期管理

**发现阶段**:
- 设置 `status: open`
- 填写 `discovered_in` 和 `discovered_at`

**修复阶段**:
- 更新 `status: in_progress`
- 添加 `fixed_in` 和 `fixed_at`

**完成阶段**:
- 更新 `status: fixed`
- 完善 `fix_summary` 和 `testing_notes`

## 与其他技能的集成

### powerby-command
```markdown
在P7代码审查阶段：

**检查Bug状态**
docs/bugs/index.md 中查看 status=open 且 severity=P0/P1

**关联Bug到审查**
在 code-review-report.md 中引用相关Bug
```

### powerby-bugfix
```markdown
Bug修复流程中：

**创建Bug文档**
- 自动生成标准元数据
- 关联到相关迭代和文档
- 更新全局索引

**修复完成**
- 更新fixed_in、fixed_at等字段
- 生成修复总结
- 更新相关迭代的Bug列表
```

### powerby-engineer
```markdown
开发实现阶段：

**检查关联Bug**
在 tasks.md 中查看相关Bug
确保任务实现不引入新的Bug

**记录新Bug**
发现新Bug时，创建Bug文档并关联到当前迭代
```

## 自动化工具

### 索引生成脚本

**功能**:
- 扫描所有Bug文档
- 提取元数据
- 生成索引页面
- 更新统计信息

**使用**:
```bash
# 生成全局索引
python3 docs/bugs/scripts/generate-bug-index.py --global

# 生成特定迭代索引
python3 docs/bugs/scripts/generate-bug-index.py --iteration 001-task-manager

# 生成分类索引
python3 docs/bugs/scripts/generate-bug-index.py --category security

# 验证文档
python3 docs/bugs/scripts/generate-bug-index.py --validate
```

### 关联检查脚本

```bash
# 检查关联文档是否存在
for bug in docs/bugs/**/*.md; do
    # 提取related_documents中的路径
    # 检查文件是否存在
done
```

## 示例

### 示例1：全局安全Bug

```yaml
---
bug_id: "bug-001"
title: "SQL注入漏洞"
severity: "P0"
status: "fixed"
category: "security"
discovered_in: "001-task-manager"
fixed_in: "001-task-manager"
related_documents:
  - path: "docs/iterations/001-task-manager/architecture.md"
    type: "architecture"
    relation: "fixed_by"
---
```

### 示例2：迭代特定UI Bug

```yaml
---
bug_id: "bug-002"
title: "登录按钮样式错误"
severity: "P2"
status: "open"
category: "ui"
discovered_in: "002-payment-system"
related_documents:
  - path: "docs/iterations/002-payment-system/tasks.md"
    type: "tasks"
    relation: "impacts"
---
```

## 迁移指南

### 从旧结构迁移

如果之前Bug文档存放在其他位置，需要进行迁移：

```bash
# 1. 创建新目录结构
mkdir -p docs/bugs/{global,categories,templates,scripts}

# 2. 迁移文档
mv old-bugs/*.md docs/bugs/global/

# 3. 添加元数据
for file in docs/bugs/global/*.md; do
    # 添加YAML头部
    # 提取现有信息
done

# 4. 生成索引
python3 docs/bugs/scripts/generate-bug-index.py --all
```

### 兼容性

- 旧结构仍然可用，但建议迁移到新结构
- 索引生成脚本支持读取旧格式文档
- 逐步迁移，不强制立即切换

## 常见问题

### Q: 如何处理跨迭代的Bug？
A: 使用 `related_iterations` 字段列出所有相关迭代。

### Q: Bug修复后是否需要更新关联文档？
A: 建议在相关PRD、架构等文档中记录Bug修复的影响。

### Q: 如何批量更新Bug状态？
A: 可以编写脚本批量更新YAML元数据。

### Q: 是否可以集成GitHub Issues？
A: 可以在 `related_issues` 中引用GitHub Issue编号。

## 总结

通过 `docs/bugs/` 目录归档Bug文档，我们实现了：

- ✅ **统一管理**: 与主流程文档平级，保持一致性
- ✅ **强关联**: 与PRD、架构等文档建立关联
- ✅ **自动化**: 索引生成和状态跟踪自动化
- ✅ **可追踪**: 支持跨迭代生命周期管理
- ✅ **可分析**: 元数据支持数据分析和报告

这符合PowerBy的文档驱动理念，为项目的知识管理和质量跟踪提供了坚实基础。
