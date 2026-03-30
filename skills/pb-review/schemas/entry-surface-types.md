# Schema: Entry Surface Types

**版本**: 1.0.0
**来源**: pb-review-standard.md R-01
**引用 Skill**: pb-review-project-scope

## 定义

| 类型 | 说明 | 典型线索 |
|---|---|---|
| cli | 命令行入口 | `manage.py`, `management/commands`, `cli.py` |
| api | HTTP / RPC 接口入口 | `urls.py`, `router`, `api`, `viewset` |
| page | 页面路由或模板页面入口 | `pages/`, `templates/`, `views.py` |
| cron | 定时任务入口 | `cron`, `scheduler`, `celery beat`, `tasks.py` |
| orchestration | 服务编排或工作流入口 | `runner`, `workflow`, `orchestr`, `pipeline` |

## 评估规则

- 同一条入口可以被识别为多个候选时，优先选择更具体的类型
- 输出必须包含 `type`、`path`、`name`

## 数据结构

```yaml
entry_surface_inventory:
  - type: cli | api | page | cron | orchestration
    path: string
    name: string
```

## 示例

```yaml
entry_surface_inventory:
  - type: cli
    path: skills/powerby-command/powerby-cli.py
    name: powerby command cli
```
