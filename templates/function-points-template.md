# 功能点清单

**项目**: {{project_name}}
**迭代ID**: {{iteration_id}}
**版本**: {{version}}
**生成日期**: {{date}}
**更新日期**: {{last_update}}
**PRD文档**: prd.md

> **说明**: 本文档由 `function-point-checker` 技能自动生成和更新。请勿手动创建新版本，始终维护此文档为最新状态。

---

## 📊 概览统计

- **功能点总数**: {{total_count}}个
- **P0功能**: {{p0_count}}个 ({{p0_percent}}%)
- **P1功能**: {{p1_count}}个 ({{p1_percent}}%)
- **P2功能**: {{p2_count}}个 ({{p2_percent}}%)
- **功能模块**: {{module_count}}个
- **总预估工时**: {{total_effort}}人天

## 📋 功能点详细清单

{{#each modules}}
### 模块{{@index}}: {{module_name}}

{{#each functions}}
#### [{{priority}}] {{function_id}} {{function_name}}
- **需求来源**: {{requirement_source}}
- **功能描述**: {{description}}
- **用户输入**:
{{#each user_inputs}}
  - {{this}}
{{/each}}
- **系统输出**:
{{#each system_outputs}}
  - {{this}}
{{/each}}
- **关键约束**:
{{#each constraints}}
  - {{this}}
{{/each}}
- **验收标准**:
{{#each acceptance_criteria}}
  - [ ] {{this}}
{{/each}}
- **依赖关系**: {{dependencies}}
- **预估工时**: {{effort}}
{{#if issues}}
- **⚠️ 问题**: {{issues}}
{{/if}}

{{/each}}
{{/each}}

---

## 🔗 依赖关系图

```
{{dependency_graph}}
```

**依赖关系说明**:
{{#each dependency_notes}}
- {{this}}
{{/each}}

## 📈 质量检查

### 格式检查
{{#each format_issues}}
- ⚠️ {{this}}
{{/each}}

### 内容检查
{{#each content_issues}}
- ⚠️ {{this}}
{{/each}}

### 建议改进
{{#each improvements}}
- 💡 {{this}}
{{/each}}

## 📊 优先级分布

| 优先级 | 数量 | 占比 | 建议范围 | 状态 |
|-------|------|------|----------|------|
| P0 | {{p0_count}}个 | {{p0_percent}}% | 60-80% | {{p0_status}} |
| P1 | {{p1_count}}个 | {{p1_percent}}% | 15-30% | {{p1_status}} |
| P2 | {{p2_count}}个 | {{p2_percent}}% | 5-15% | {{p2_status}} |

## 💡 审核要点

### P0功能审核重点
{{#each p0_review_points}}
- [ ] {{this}}
{{/each}}

### P1功能审核重点
{{#each p1_review_points}}
- [ ] {{this}}
{{/each}}

## 📝 更新记录

| 版本 | 日期 | 更新内容 | 更新人 |
|-----|------|---------|-------|
| {{version}} | {{date}} | 初始版本 | function-point-checker |
{{#each update_history}}
| {{version}} | {{date}} | {{content}} | {{author}} |
{{/each}}

---

**生成工具**: function-point-checker v1.0.0
**使用说明**: 本文档为功能迭代的功能点清单，始终保持最新状态。团队审核、讨论和开发时请以此文档为准。
