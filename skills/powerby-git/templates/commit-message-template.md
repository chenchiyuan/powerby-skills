# 提交信息模板

## 标准格式

```
{类型}({范围}): {描述}

{可选的正文}

{可选的脚注}
```

## 类型标识

| 类型 | 描述 | 示例 |
|------|------|------|
| feat | 新功能 | `feat(auth): add OAuth2 login` |
| fix | Bug 修复 | `fix(db): resolve connection leak` |
| docs | 文档更新 | `docs(readme): update install guide` |
| style | 代码格式 | `style: run prettier` |
| refactor | 重构 | `refactor(auth): simplify flow` |
| test | 测试相关 | `test(auth): add login tests` |
| chore | 维护任务 | `chore(deps): update packages` |

## 范围标识

- 范围是被修改的功能模块
- 使用小写字母
- 可选，但如果使用需要用括号包裹

## 示例

### 简单提交

```
feat(auth): add JWT token generation
```

### 带正文提交

```
fix(payment): resolve double-charge bug

The payment callback was triggered twice due to a race
condition in the event handler. Added debounce to prevent
duplicate requests.

Closes #123
```

### 带脚注

```
docs(api): update endpoint documentation

Added rate limiting information and new response formats.

Refs #456
BREAKING CHANGE: Response format has changed
```

## 最佳实践

1. 使用祈使语气（"add" 而不是 "added"）
2. 首行不超过 50 字符
3. 正文在 72 字符处换行
4. 关联相关 issue
