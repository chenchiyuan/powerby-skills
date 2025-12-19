---
description: 需求定义+澄清 - 输入需求，生成PRD和功能点清单，融合澄清过程
handoffs:
  - label: Define+Clarify Requirements
    agent: powerby-product
    prompt: 基于用户输入的需求，生成完整的PRD文档和功能点清单，并融合澄清过程消除模糊点
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.define` 命令进行需求定义+澄清（P1阶段）。此阶段将产品想法转化为结构化的需求文档，并融合澄清过程消除模糊点。

### 执行步骤：

1. **解析用户输入**
   - 需求描述（必填，产品想要实现的功能或目标）
   - 用户群体（可选，如需要可后续澄清）
   - 核心问题（可选，如需要可后续澄清）

2. **调用powerby-product技能**
   - 传递参数：需求描述及可选参数
   - 要求生成PRD文档和功能点清单，融合澄清过程

3. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/prd.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/function-points.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/clarifications.md`

4. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P1
   - 标记Gate 1为已通过

5. **创建迭代记录**
   - 在`.powerby/iterations.json`中记录迭代001

### 输出格式：

```
✅ P1 需求定义+澄清完成

📄 输出文档:
  ├── docs/iterations/001-{项目名}/prd.md (产品需求文档)
  ├── docs/iterations/001-{项目名}/function-points.md (功能点清单)
  └── docs/iterations/001-{项目名}/clarifications.md (需求澄清记录)

🔒 质量门禁 Gate 1: MVP需求定稿检查
  ✓ 核心价值定义清晰
  ✓ 功能点完整性验证
  ✓ 最小可行产品范围确认
  ✓ 模糊点已澄清

🎯 下一步: 使用 /powerby.research 进入技术调研阶段
```

### 使用示例：

```
/powerby.define "我想构建一个任务管理系统，帮助团队更好地协作"
/powerby.define "电商平台，实现商品展示、购物车和订单管理功能"
/powerby.define "博客系统，支持文章发布、评论和用户管理"
```

### 前置条件：
- ✅ 项目宪章文件存在：`docs/constitution.md`
- ✅ 项目元数据文件存在：`.powerby/project.json`

### 错误处理：
- 如果缺少前置条件，提示用户先运行 `/powerby.initialize`
- 如果PRD生成失败，提示检查输入参数是否完整
- 如果功能点清单不完整，建议重新定义需求
