---
description: 需求定义+澄清 - 基于产品想法生成PRD和功能点清单，融合澄清过程
handoffs:
  - label: Define+Clarify Requirements
    agent: powerby-product
    prompt: 基于产品想法、用户群体、核心问题等，生成完整的PRD文档和功能点清单，并融合澄清过程消除模糊点
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.define` 命令进行需求定义+澄清（P1阶段）。此阶段将产品想法转化为结构化的需求文档，并融合澄清过程消除模糊点。

### 执行步骤：

1. **解析用户输入**
   - 产品想法（必填）
   - 用户群体（必填）
   - 核心问题（必填）
   - 时间线（可选）
   - 约束条件（可选）

2. **调用powerby-product技能**
   - 传递参数：产品想法、用户群体、核心问题、时间线、约束条件
   - 要求生成PRD文档和功能点清单

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
/powerby.define "我想构建一个任务管理系统，帮助团队更好地协作" --user-group "团队成员和项目经理" --problem "任务分配不清晰，协作效率低"
/powerby.define "电商平台" --user-group "消费者和商家" --problem "线上购物体验不佳，支付流程繁琐"
```

### 前置条件：
- ✅ 项目宪章文件存在：`docs/constitution.md`
- ✅ 项目元数据文件存在：`.powerby/project.json`

### 错误处理：
- 如果缺少前置条件，提示用户先运行 `/powerby.initialize`
- 如果PRD生成失败，提示检查输入参数是否完整
- 如果功能点清单不完整，建议重新定义需求
