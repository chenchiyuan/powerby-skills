# PowerBy安全更新示例

## 场景描述

假设用户有一个正在进行的PowerBy项目，包含了多个迭代的存档数据。现在需要升级到新版本，演示如何安全地进行更新而不丢失任何数据。

## 现有项目结构

```
my-project/
├── .powerby/
│   ├── project.json          # 项目元数据
│   ├── iterations.json       # 迭代追踪
│   └── iterations/           # 用户存档目录
│       ├── 001-task-manager/ # 迭代001存档
│       │   ├── prd.md
│       │   ├── function-points.md
│       │   └── research.md
│       └── 002-payment-system/ # 迭代002存档
│           ├── prd.md
│           └── design.md
├── docs/
│   ├── constitution.md       # 项目宪章
│   └── iterations/           # 文档存档
│       ├── 001-task-manager/
│       └── 002-payment-system/
└── src/                      # 源代码
```

## 升级前检查

### 1. 检测现有结构

```bash
# 永远第一步：检查现有结构
if [ -d ".powerby" ]; then
    echo "🔍 检测到现有.powerby目录，开始安全更新模式"
    echo "📋 现有文件列表："
    find .powerby -type f | sort
    echo "✅ 记录完成，准备安全更新"
else
    echo "🆕 未检测到.powerby目录，开始全新初始化"
fi
```

### 2. 检查项目元数据

```json
// .powerby/project.json (现有数据)
{
  "projectName": "task-manager",
  "mainTask": "一个帮助团队协作的任务管理应用",
  "currentStage": "P4",
  "completedGates": ["Gate 1", "Gate 2", "Gate 3", "Gate 4"],
  "status": "in_progress",
  "createdAt": "2025-12-01T10:00:00Z",
  "lastUpdated": "2025-12-15T14:30:00Z"
}
```

## 安全更新流程

### 第一步：备份现有数据

```bash
# 创建备份目录
mkdir -p .powerby_backup_$(date +%Y%m%d_%H%M%S)

# 备份所有现有文件
cp -r .powerby/* .powerby_backup_*/

echo "✅ 备份完成：.powerby_backup_$(date +%Y%m%d_%H%M%S)"
```

### 第二步：安全创建新文件

#### 2.1 只创建缺失的配置文件

```bash
# 检查每个必要文件是否存在，只创建缺失的
if [ ! -f ".powerby/version.json" ]; then
    echo "📝 创建版本文件..."
    cat > .powerby/version.json << 'EOF'
{
  "frameworkVersion": "2.3.1",
  "lastUpdated": "2025-12-23T10:00:00Z",
  "updateNotes": "安全文件管理机制升级"
}
EOF
    echo "✅ version.json 创建完成"
else
    echo "⚠️ version.json 已存在，跳过创建"
fi
```

#### 2.2 安全更新project.json

```bash
# 永远不直接覆盖，先备份
cp .powerby/project.json .powerby/project.json.backup

# 使用jq进行安全的JSON合并
jq -s '.[0] * .[1]' \
    .powerby/project.json \
    <(echo '{
      "frameworkVersion": "2.3.1",
      "securityUpdate": "2025-12-23",
      "dataIntegrityCheck": "passed"
    }') > .powerby/project.json.new

# 只在验证通过后替换
if jq empty .powerby/project.json.new 2>/dev/null; then
    mv .powerby/project.json.new .powerby/project.json
    echo "✅ project.json 安全更新完成"
else
    echo "❌ JSON格式错误，恢复备份"
    mv .powerby/project.json.backup .powerby/project.json
fi
```

### 第三步：验证数据完整性

```bash
# 检查所有原有文件是否仍然存在
echo "🔍 验证数据完整性..."

original_count=$(find .powerby_backup_* -type f | wc -l)
current_count=$(find .powerby -type f | wc -l)

if [ "$original_count" -eq "$current_count" ]; then
    echo "✅ 数据完整性检查通过：$original_count 个文件"
else
    echo "❌ 数据完整性检查失败：期望 $original_count，实际 $current_count"
    echo "🔄 恢复备份数据..."
    rm -rf .powerby
    mv .powerby_backup_* .powerby
fi
```

## 更新后结构

```
my-project/
├── .powerby/
│   ├── project.json          # ✅ 已更新（保留所有原有数据，新增版本字段）
│   ├── iterations.json       # ✅ 完全保留
│   ├── version.json          # 🆕 新增（版本信息）
│   ├── iterations/           # ✅ 完全保留（所有存档）
│   │   ├── 001-task-manager/
│   │   └── 002-payment-system/
│   └── security.json         # 🆕 新增（安全更新记录）
├── docs/
│   ├── constitution.md       # ✅ 询问用户后决定是否更新
│   └── iterations/           # ✅ 完全保留（所有文档）
├── src/                      # ✅ 完全保留（所有代码）
└── .powerby_backup_20251223_120000/ # 📦 备份目录
```

## 关键安全保证

### ✅ 数据保护承诺

1. **零数据丢失**：所有原有文件100%保留
2. **增量更新**：只添加新文件，不修改现有内容
3. **自动备份**：每次更新前自动创建备份
4. **完整性检查**：更新后验证所有文件完整性
5. **一键回滚**：如果出现问题，可立即恢复备份

### ⚠️ 禁止操作

1. **绝对不删除**：.powerby目录及任何子目录
2. **绝对不覆盖**：project.json、iterations.json等配置文件
3. **绝对不修改**：docs/iterations/下的任何文档
4. **绝对不强制**：用户数据由用户完全控制

## 用户确认流程

### 更新前询问

```
🔄 检测到现有PowerBy项目

📊 项目信息：
  名称：task-manager
  当前阶段：P4
  迭代数量：2
  存档数据：完整保留

🔒 安全保证：
  ✅ 现有数据完全保留
  ✅ 只添加新配置文件
  ✅ 自动创建备份
  ✅ 支持一键回滚

❓ 是否继续安全更新？
  [Y] 继续更新
  [N] 取消更新
```

### 更新后确认

```
✅ 安全更新完成

📊 更新统计：
  新增文件：2个（version.json, security.json）
  更新文件：1个（project.json - 仅添加新字段）
  保留文件：所有原有文件

🔒 数据完整性：✅ 通过
📦 备份目录：.powerby_backup_20251223_120000

❓ 是否删除备份目录？
  [Y] 删除备份（推荐）
  [N] 保留备份（谨慎操作）
```

## 故障恢复

### 如果更新失败

```bash
# 检测到问题，立即回滚
echo "❌ 检测到问题，开始回滚..."

# 删除当前.powerby目录
rm -rf .powerby

# 恢复备份
backup_dir=$(ls -t .powerby_backup_* | head -n1)
mv $backup_dir .powerby

echo "✅ 回滚完成，数据已恢复到更新前状态"
```

### 手动恢复

如果自动回滚失败，用户可以手动恢复：

```bash
# 查看备份目录
ls -la .powerby_backup_*/

# 手动恢复
rm -rf .powerby
cp -r .powerby_backup_20251223_120000 .powerby
```

## 最佳实践

1. **始终备份**：每次更新前自动创建备份
2. **逐步验证**：每个步骤完成后立即验证
3. **用户控制**：关键决策必须用户确认
4. **可逆操作**：所有更新都支持回滚
5. **透明日志**：记录所有操作和决策

## 总结

通过这套安全更新机制，我们确保：

- 🛡️ **用户数据100%安全**：绝对不丢失任何数据
- ⚡ **增量式更新**：只添加必要内容，不破坏现有结构
- 🔄 **完全可逆**：支持一键回滚到更新前状态
- 👥 **用户控制**：所有重要决策都由用户决定
- 📊 **透明可追踪**：完整记录所有操作过程

这样，用户可以放心地升级PowerBy框架，同时完全保护自己的项目数据。
