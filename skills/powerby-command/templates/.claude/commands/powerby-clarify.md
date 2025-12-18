---
description: 需求澄清 - 识别和解决PRD中的模糊点，生成澄清记录
handoffs:
  - label: Clarify Requirements
    agent: powerby-product
    prompt: 基于现有需求文档进行结构化澄清，识别模糊点并生成澄清记录
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.clarify` 命令进行需求澄清（P2阶段）。此阶段识别并解决需求中的模糊点，确保需求清晰明确。

### 执行步骤：

1. **解析用户输入**
   - 澄清问题数量（可选，默认为5-8个）

2. **调用powerby-product技能**
   - 传递参数：PRD路径、功能点路径、澄清问题数量
   - 要求进行结构化澄清，生成澄清记录

3. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/clarifications.md`

4. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P2
   - 标记Gate 2为已通过

### 输出格式：

```
✅ P2 需求澄清完成

📄 输出文档:
  └── docs/iterations/001-{项目名}/clarifications.md (澄清记录)

🔒 质量门禁 Gate 2: 澄清完整性检查
  ✓ 模糊点识别完整
  ✓ 边界条件明确
  ✓ 业务规则确认

🎯 下一步: 使用 /powerby.research 进入技术调研阶段
```

### 使用示例：

```
/powerby.clarify
/powerby.clarify --questions 8
```

### 前置条件：
- ✅ PRD文档存在：`docs/iterations/*/prd.md`
- ✅ 功能点清单存在：`docs/iterations/*/function-points.md`

### 澄清内容：
澄清记录应包含：
1. 识别的模糊点
2. 澄清后的明确描述
3. 边界条件
4. 业务规则

### 错误处理：
- 如果PRD或功能点清单不存在，提示用户先运行 `/powerby.define`
- 如果澄清记录生成失败，建议检查PRD文档质量
- 如果仍有未解决的模糊点，建议重新澄清
