---
name: powerby-huicheng-push
description: |
  慧诚推送通知工具。任务完成后调用慧诚 Alert API 发送结果概览通知到移动端。
  当 ASP 流程完成、代码审查完成、Bug 修复完成、或任何需要异步通知用户的场景时使用。
  不用于实时消息通信或双向交互。
compatibility:
  - bash
  - curl
---

# PowerBy 慧诚推送

通过慧诚 Alert API 向移动端推送任务完成通知，让用户在离开工作台后也能收到结果概览。

## Purpose

在任务完成后发送一条精炼的结果摘要到用户移动端。成功使用的标志是：用户在手机上看到一条包含任务状态和关键结果的通知。

## Success criteria

- API 调用返回 `{"errcode": 0, "msg": "success"}`
- 通知内容精炼（500 字符以内），包含任务状态和核心结果
- 推送失败不阻塞主流程
- 不包含敏感信息（token、密码、API key）

## Strategy

1. **通知是补充，不是主交付。** 推送通知是任务完成后的附加动作，失败不影响任务本身的完成状态。

2. **内容为移动端优化。** 标题简明（一眼看懂任务类型），内容精炼（关键数据 + 状态 + 产出物列表），适合手机屏幕快速浏览。

3. **敏感信息不出站。** 推送内容中只包含业务结果，不包含 token、密码、内部路径等敏感数据。

## Tools and capability boundaries

- **Bash + curl**：通过 POST 请求调用慧诚 Alert API
- **不做**：实时消息通信、双向交互、文件传输

## Important facts and constraints

### API 配置

| 项目 | 值 |
|------|---|
| Endpoint | `https://huicheng.powerby.com.cn/api/simple/alert/` |
| Method | POST |
| Content-Type | application/json |
| Token | `6020867bc6334c609d4f348c22f90f14` |
| Channel | `price_monitor` |

### 调用方式

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

### 响应处理

- 成功：`{"errcode": 0}` -> 向用户确认"通知已推送"
- 失败：`{"errcode": 非0}` -> 报告推送失败及原因，不阻塞主流程
- 网络异常：报告网络问题，不阻塞主流程

## Workflow

1. **组装内容** — 从上游任务结果中提取关键信息，按内容格式规范组装标题和正文。

2. **发送请求** — 执行 curl 调用慧诚 API。

3. **处理响应** — 成功则确认，失败则报告原因但不阻塞。

## Output format

### ASP 流程完成

```
标题: ASP 完成: {迭代名称}
内容:
状态: {PASS/FAIL}
版本: {spec 版本号}
轮次: {总审查轮次}
修复: {BLOCKER数} BLOCKER + {MAJOR数} MAJOR
遗留: {MINOR数} MINOR
产出: proposal.md / spec.md / product-map.md
```

### 通用任务完成

```
标题: {任务类型}: {简要描述}
内容:
状态: 完成
耗时: {轮次或步骤数}
结果: {一句话总结}
```

## Resources

- 无独立资源文件。API 配置已内联在 Important facts 中。

## Subtask / parallelism guidance

- 推送操作独立于主流程，可异步执行
- 不依赖其他技能的返回结果

## Examples

**Example 1: ASP 流程完成推送**
Input: ASP 审查通过，proposal.md 已生成
Output: 推送 "ASP 完成: 任务管理系统 / 状态: PASS / 产出: proposal.md"

**Example 2: Bug 修复完成推送**
Input: Bug-001 已修复并验证通过
Output: 推送 "Bug 修复: 登录超时 / 状态: 完成 / 结果: 连接池泄漏已修复"

## Safety

- 不推送 token、密码、API key 等敏感信息
- 推送失败不阻塞主任务流程
- content 控制在 500 字符以内
- 标题和内容使用中文
