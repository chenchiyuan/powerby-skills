# tool-browse: 前端浏览器证据采集

## 命令模式

browse 调用遵循 pb-v1-brower 的 `$B` 发现机制。所有命令统一使用 `$B <子命令>` 单语句调用。

### $B 发现（一次性）

每次调试会话开始时执行一次，获取 browse 二进制路径：

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
B=""
[ -n "$_ROOT" ] && [ -x "$_ROOT/.claude/skills/gstack/browse/dist/browse" ] && B="$_ROOT/.claude/skills/gstack/browse/dist/browse"
[ -z "$B" ] && B=~/.claude/skills/gstack/browse/dist/browse
echo "$B"
```

### 权限注册

发现 `$B` 的绝对路径后，权限规则为：

```
Bash({$B的绝对路径}:*)
```

后续所有调用直接使用绝对路径，单语句执行，不做变量赋值拼接。

---

## 操作清单

### 连接与导航

```bash
# 连接状态检查
$B status

# 导航到目标页面
$B goto "{url}"

# 等待页面加载
$B chain '[["goto","{url}"],["wait","--load"]]'
```

### 证据采集（结构化数据优先）

```bash
# 页面快照（默认采集）
$B snapshot -i -o "{artifact_root}/round-{N}-snapshot.txt"

# 控制台日志
$B console --errors -o "{artifact_root}/round-{N}-console.log"

# 网络请求日志（按需）
$B network -o "{artifact_root}/round-{N}-network.log"

# 组合采集（推荐）
$B chain '[
  ["goto","{url}"],
  ["wait","--load"],
  ["console","--clear"],
  ["snapshot","-i","-o","{artifact_root}/round-{N}-snapshot.txt"],
  ["console","--errors","-o","{artifact_root}/round-{N}-console.log"]
]'
```

### 证据采集（截图）

```bash
# 视觉问题截图
$B screenshot -o "{artifact_root}/round-{N}-visual.png"

# 人类证据归档截图
$B screenshot -o "{artifact_root}/round-{N}-evidence.png"
```

### 交互操作

```bash
# 点击元素
$B click "{selector}"

# 输入文本
$B type "{selector}" "{text}"

# 执行 JS
$B js '{expression}'

# CSS 属性检查
$B css "{selector}" "{property}"

# 元素可见性检查
$B is visible "{selector}"
```

### 会话管理

```bash
# 连接浏览器
$B connect

# 聚焦标签页
$B focus

# 断开连接
$B disconnect
```

---

## 证据类型选择

| 问题类型 | 优先工具 | 补充工具 |
|---------|---------|---------|
| 白屏/空白页 | `$B js '{bodyChildCount, bodyHeight}'` | `$B console --errors` |
| 按钮不可点 | `$B is visible/enabled "{selector}"` | `$B css "{selector}" "pointer-events"` |
| 元素未显示 | `$B css "{selector}" "display/visibility"` | `$B js '{width, height}'` |
| 布局溢出 | `$B js '{docClientWidth, docScrollWidth}'` | `$B screenshot` |
| 接口失败 | `$B network` | `$B console --errors` |
| 视觉问题 | `$B screenshot`（必须截图） | — |

---

## 产出规范

每轮调试产出存放在 `{artifact_root}/` 下：

```
round-{N}-snapshot.txt    # 页面结构快照
round-{N}-console.log     # 控制台日志
round-{N}-network.log     # 网络请求（按需）
round-{N}-visual.png      # 视觉截图（按需）
round-{N}-evidence.png    # 人类证据截图（按需）
round-{N}-verify.md       # 本轮验证结论
```
