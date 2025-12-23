# 项目Bug总览

> **最后更新**: {generated_at}
> **自动生成**: 本索引由 `generate-bug-index.py` 脚本自动生成

## 📊 统计信息

| 指标 | 数量 |
|------|------|
| 总Bug数 | {stats.total} |
| 未修复 | {stats.by_status.open} |
| 修复中 | {stats.by_status.in_progress} |
| 已修复 | {stats.by_status.fixed} |
| 已废弃 | {stats.by_status.deprecated} |

## 📈 按严重程度分布

| 严重程度 | 数量 | 占比 |
|----------|------|------|
| P0 | {stats.by_severity.P0} | {percentage: P0} |
| P1 | {stats.by_severity.P1} | {percentage: P1} |
| P2 | {stats.by_severity.P2} | {percentage: P2} |

## 📂 按分类分布

{% for category, count in stats.by_category.items() %}
- **{category}**: {count} 个
{% endfor %}

## 🔍 Bug列表

### 未修复Bug (按严重程度排序)

{% for bug in bugs %}
{% if bug.status == 'open' %}
- **[{bug.bug_id}]({bug.relative_path})** - {bug.title}
  - 严重程度: {bug.severity}
  - 分类: {bug.category}
  - 发现迭代: {bug.discovered_in}
{% endif %}
{% endfor %}

### 已修复Bug

{% for bug in bugs %}
{% if bug.status == 'fixed' %}
- **[{bug.bug_id}]({bug.relative_path})** - {bug.title}
  - 严重程度: {bug.severity}
  - 发现迭代: {bug.discovered_in}
  - 修复迭代: {bug.fixed_in}
{% endif %}
{% endfor %}

## 📅 按时间分布

{% for month, count in stats.by_month.items() %}
- **{month}**: {count} 个Bug
{% endfor %}

## 🔗 快速链接

### 按迭代查看
{% for iteration, count in stats.by_iteration.items() %}
- [{iteration}](iterations/{iteration}/bugs/index.md): {count} 个Bug
{% endfor %}

### 按分类查看
{% for category in stats.by_category.keys() %}
- [{category}](categories/{category}/index.md): {stats.by_category[category]} 个Bug
{% endfor %}

---

**说明**:
- 严重程度: P0(致命) > P1(严重) > P2(一般)
- 状态: open(未修复) > in_progress(修复中) > fixed(已修复) > deprecated(已废弃)
- 分类: security(安全) > performance(性能) > ui(界面) > logic(逻辑) > data(数据)

