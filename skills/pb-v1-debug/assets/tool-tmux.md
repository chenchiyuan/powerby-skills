# tool-tmux: 后端可视化调试环境

## 命令模式

所有 tmux 操作统一使用 `tmux <子命令>` 单语句调用。

### 权限注册

```
Bash(tmux:*)
```

一条规则覆盖所有 tmux 子命令。

---

## 操作清单

### 初始化 debug session

```bash
tmux new-session -d -s "debug-{bug-id}" -x 200 -y 50
```

### 配置三 pane 布局

```bash
# 左右分屏
tmux split-window -h -t "debug-{bug-id}"
# 右侧上下分屏
tmux split-window -v -t "debug-{bug-id}:0.1"
```

布局结果：
- Pane 0（左, 50%）: 命令执行区 — 运行调试命令、执行实验
- Pane 1（右上, 25%）: 日志监控区 — tail -f 应用日志
- Pane 2（右下, 25%）: 应用状态区 — 进程状态/端口/资源监控

### 向 pane 发送命令

```bash
# 命令执行区
tmux send-keys -t "debug-{bug-id}:0.0" "{命令}" Enter

# 日志监控区
tmux send-keys -t "debug-{bug-id}:0.1" "tail -f {日志路径}" Enter

# 状态监控区
tmux send-keys -t "debug-{bug-id}:0.2" "watch -n 2 '{状态命令}'" Enter
```

注意：`Enter` 是必需的，否则命令不会执行。

### 捕获 pane 输出（证据收集）

```bash
# 捕获完整历史（推荐）
tmux capture-pane -t "debug-{bug-id}:0.0" -p -S -

# 捕获到文件
tmux capture-pane -t "debug-{bug-id}:0.0" -p -S - > /tmp/debug-{bug-id}-pane0.log
```

注意：不加 `-S -` 只捕获可见区域，证据收集时务必加上。

### 中断 pane 中的命令

```bash
tmux send-keys -t "debug-{bug-id}:0.0" C-c
```

### 销毁 session

```bash
tmux kill-session -t "debug-{bug-id}"
```

### 检查 session 是否存在

```bash
tmux has-session -t "debug-{bug-id}" 2>/dev/null && echo "exists" || echo "not found"
```

---

## 常见调试场景

### 日志监控

```bash
# 通用（过滤 ERROR/WARN）
tmux send-keys -t "debug-{bug-id}:0.1" "tail -f {日志路径} | grep --line-buffered 'ERROR\|WARN'" Enter

# Django
tmux send-keys -t "debug-{bug-id}:0.1" "tail -f logs/django.log" Enter
```

### 进程与端口

```bash
tmux send-keys -t "debug-{bug-id}:0.2" "watch -n 2 'lsof -i -P -n | grep LISTEN'" Enter
```

### API 调试

```bash
tmux send-keys -t "debug-{bug-id}:0.0" "curl -s -w '\\nHTTP:%{http_code} TIME:%{time_total}s' {url} | jq ." Enter
```

### 数据库查询

```bash
# PostgreSQL
tmux send-keys -t "debug-{bug-id}:0.0" "psql -U {user} -d {db} -c '{SQL}'" Enter

# SQLite
tmux send-keys -t "debug-{bug-id}:0.0" "sqlite3 {db_path} '{SQL}'" Enter
```

---

## 命名规范

- Session: `debug-{bug-id}`
- Pane 引用: `debug-{bug-id}:0.{pane_number}`
- 证据文件: `/tmp/debug-{bug-id}-pane{N}.log`
