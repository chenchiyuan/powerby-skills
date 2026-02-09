# 分支命名模板

## 标准命名模式

```
{类型}/{名称}
```

## 类型

| 类型 | 前缀 | 用途 |
|------|------|------|
| Feature | `feature/` | 新功能开发 |
| Bugfix | `bugfix/` | Bug 修复 |
| Hotfix | `hotfix/` | 紧急修复 |
| Release | `release/` | 版本发布 |

## 命名规则

1. 使用小写字母
2. 单词间使用连字符（-）
3. 名称应简洁明了
4. 避免中文和特殊字符

## 示例

```
feature/user-authentication
feature/payment-integration
bugfix/login-timeout
bugfix/memory-leak
hotfix/v1.2.3-security-patch
release/v2.0.0
```

## 不推荐

```
feature/User_Authentication  # 使用下划线
feature/用户认证功能          # 使用中文
feature/login-page-v2        # 混合风格
```
