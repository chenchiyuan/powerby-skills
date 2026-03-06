---
name: powerby-huicheng-push
description: 慧诚推送通知工具。任务完成后调用慧诚 Alert API 发送结果概览通知。支持自定义标题和内容，预配置 token 和 channel。
---

# PowerBy 慧诚推送通知

## 核心能力

在任务完成后，通过慧诚 Alert API 推送通知消息，让用户在移动端实时收到任务结果概览。

## 使用场景

- ASP 流程完成后，推送精炼结果摘要
- 代码审查完成后，推送审查结论
- Bug 修复完成后，推送修复报告
- 任何需要异步通知用户的场景

## API 配置

- **Endpoint**: `https://huicheng.powerby.com.cn/api/simple/alert/`
- **Method**: POST
- **Content-Type**: application/json
- **Token**: `6020867bc6334c609d4f348c22f90f14`
- **Channel**: `price_monitor`

## 调用协议

当需要推送通知时，使用 Bash 工具执行以下 curl 命令：

```bash
curl -s -X POST 'https://huicheng.powerby.com.cn/api/simple/alert/' \
  -H 'Content-Type: application/json' \
  -d '{
    "token": "6020867bc6334c609d4f348c22f90f14",
    "channel": "price_monitor",
    "title": "{标题}",
    "content": "{内容}"
  }'
```

### 参数说明

| 参数 | 来源 | 说明 |
|------|------|------|
| token | 预配置 | 固定值，不可修改 |
| channel | 预配置 | 固定值 `price_monitor` |
| title | 调用方传入 | 消息标题，简明扼要（如"ASP 流程完成"） |
| content | 调用方传入 | 消息正文，支持 `\n` 换行，包含结果概览 |

### 响应处理

- 成功：`{"errcode": 0, "msg": "success"}` → 向用户确认"通知已推送"
- 失败：`{"errcode": 非0, "msg": "错误描述"}` → 向用户报告推送失败及原因
- 网络异常：curl 超时或连接失败 → 向用户报告网络问题，不阻塞主流程

## 内容格式规范

推送内容应遵循以下格式，确保移动端可读：

### ASP 流程完成通知

```
标题: ASP 完成: {迭代名称}
内容:
状态: {PASS/FAIL}
版本: {spec 版本号}
轮次: {总审查轮次}（{审查序列描述}）
修复: {BLOCKER数} BLOCKER + {MAJOR数} MAJOR
遗留: {MINOR数} MINOR
产出: proposal.md / spec.md / product-map.md
```

### 通用任务完成通知

```
标题: {任务类型}: {简要描述}
内容:
状态: 完成
耗时: {轮次或步骤数}
结果: {一句话总结}
```

## 重要约束

1. **不阻塞主流程**：推送失败不影响任务本身的完成状态
2. **内容精简**：移动端阅读，content 控制在 500 字符以内
3. **敏感信息过滤**：不推送 token、密码、API key 等敏感内容
4. **中文优先**：标题和内容使用中文
