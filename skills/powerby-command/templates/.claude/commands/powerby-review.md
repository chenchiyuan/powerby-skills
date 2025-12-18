---
description: 代码审查和交付 - 执行全面的代码审查和项目交付
handoffs:
  - label: Code Review
    agent: powerby-code-review
    prompt: 执行全面的代码审查和项目交付，生成审查报告和交付文档
---

## User Input

```text
$ARGUMENTS
```

## Outline

使用 `/powerby.review` 命令进行代码审查和项目交付（P7-P8阶段）。此阶段进行全面的代码质量审查和项目最终交付。

### 执行步骤：

1. **解析用户输入**
   - PR链接（可选）
   - 审查范围（可选，默认为全量审查）

2. **调用powerby-code-review技能**
   - 传递参数：所有阶段文档、PR链接等
   - 要求进行全面的代码审查和项目交付

3. **验证输出文档**
   - 检查是否生成：`docs/iterations/001-{项目名}/code-review-report.md`
   - 检查是否生成：`docs/iterations/001-{项目名}/delivery-report.md`

4. **更新项目元数据**
   - 在`.powerby/project.json`中更新当前阶段为P8
   - 标记Gate 7和Gate 8为已通过
   - 更新状态为`completed`

### 输出格式：

```
✅ P7-P8 代码审查和项目交付完成

📄 输出文档:
  ├── docs/iterations/001-{项目名}/code-review-report.md (审查报告)
  └── docs/iterations/001-{项目名}/delivery-report.md (交付报告)

🔒 质量门禁 Gate 7: 代码审查严格性
  ✓ 代码规范检查
  ✓ 安全性审查
  ✓ 性能评估

🔒 质量门禁 Gate 8: 项目交付完整性
  ✓ 功能验收通过
  ✓ 文档交付完整
  ✓ 知识转移完成

🎉 项目完成！所有P0-P8阶段已成功完成
```

### 使用示例：

```
/powerby.review
/powerby.review --pr-link https://github.com/xxx/pull/123
/powerby.review --scope full
```

### 前置条件：
- ✅ 实现报告存在：`docs/iterations/*/implementation-report.md`

### 审查内容：
1. **代码审查报告**
   - 代码规范检查
   - 安全性审查
   - 性能评估
   - 最佳实践检查

2. **项目交付报告**
   - 功能验收报告
   - 质量评估
   - 文档完整性
   - 知识转移清单

### 审查维度：
- 代码质量
- 安全性
- 性能
- 可维护性
- 测试覆盖率
- 文档完整性

### 交付清单：
- 源代码
- 部署文档
- 用户手册
- API文档
- 运维手册
- 知识转移文档

### 错误处理：
- 如果实现报告不存在，提示用户先运行 `/powerby.implement`
- 如果代码审查发现问题，建议先修复再重新审查
- 如果交付文档不完整，建议补充必要文档
