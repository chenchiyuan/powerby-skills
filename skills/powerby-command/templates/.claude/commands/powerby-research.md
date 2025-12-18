---
description: 技术调研 - 分析技术可行性，评估技术方案
handoffs:
  - label: Technical Research
    agent: powerby-architect
    prompt: 基于需求文档进行技术可行性调研，评估技术选型和风险
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.research` 命令进行技术调研（P3阶段）。此阶段评估技术可行性，分析技术选型和潜在风险。

### 执行步骤：

1. **调用powerby-architect技能**
   - 传递参数：PRD路径、功能点路径、澄清记录路径
   - 要求进行技术可行性调研

2. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/research.md`

3. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P3
   - 标记Gate 3为已通过

### 输出格式：

```
✅ P3 技术调研完成

📄 输出文档:
  └── docs/iterations/001-{项目名}/research.md (技术调研报告)

🔒 质量门禁 Gate 3: 技术调研完整性
  ✓ 技术选型评估
  ✓ 可行性分析
  ✓ 风险评估完成

🎯 下一步: 使用 /powerby.design 进入架构设计阶段
```

### 使用示例：

```
/powerby.research
```

### 前置条件：
- ✅ 澄清记录存在：`docs/iterations/*/clarifications.md`

### 调研内容：
技术调研报告应包含：
1. 技术选型分析
2. 可行性评估
3. 风险评估
4. 推荐方案

### 调研维度：
- 技术成熟度
- 开发复杂度
- 维护成本
- 性能表现
- 安全性
- 扩展性
- 团队技能匹配度

### 错误处理：
- 如果澄清记录不存在，提示用户先运行 `/powerby.clarify`
- 如果技术调研报告生成失败，建议检查需求文档质量
- 如果技术风险过高，建议重新评估需求或技术方案
