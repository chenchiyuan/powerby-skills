# PowerBy Skills - 安装指南

## 🚀 快速安装

PowerBy Skills 是一套完整的AI驱动产品开发流程技能包。本指南将帮助您在几分钟内完成安装并开始使用。

## 📦 安装方式

### 方式一：通过Claude插件市场安装（推荐）

#### 步骤1：在Claude中安装技能

1. **打开Claude应用**
   - 确保您使用的是Claude Desktop最新版本

2. **访问技能市场**
   - 在左侧菜单中点击"技能市场"
   - 或直接搜索"powerby-skills"

3. **安装PowerBy技能**
   - 点击"powerby-skills"技能卡片
   - 点击"添加到项目"按钮
   - 选择要安装到的项目

4. **安装确认**
   - 技能安装成功后，Claude会显示确认信息

#### 步骤2：安装PowerBy命令

在Claude对话中运行安装命令：

```
/powerby.init
```

这将自动完成：
- ✅ 清理旧版本命令（如果有）
- ✅ 安装最新版本PowerBy命令
- ✅ 创建项目配置目录（.powerby）
- ✅ 创建命令目录（.claude/commands）
- ✅ 初始化项目状态

#### 步骤3：验证安装

在Claude中输入以下命令验证安装：

```
/powerby
```

您应该看到所有可用命令的自动补全提示：

```
/powerby.initialize  - 项目初始化
/powerby.define       - 需求定义+澄清
/powerby.quick        - 快速流程（≤3天需求）
/powerby.research     - 技术调研
/powerby.design       - 架构设计
/powerby.plan         - 任务规划
/powerby.implement    - 开发实现
/powerby.review       - 代码审查
```

### 方式二：GitHub克隆安装

如果您想从GitHub直接安装：

#### 步骤1：克隆仓库

```bash
# 克隆项目
git clone https://github.com/your-org/powerby-skills.git
cd powerby-skills

# 查看项目结构
ls -la
```

#### 步骤2：安装CLI工具

```bash
# 进入powerby-command目录
cd skills/powerby-command

# 给安装脚本执行权限
chmod +x setup.sh

# 运行安装脚本
./setup.sh
```

#### 步骤3：初始化项目

```bash
# 返回您的项目目录
cd /your/project/directory

# 初始化PowerBy项目
powerby init your-project-name

# 安装PowerBy命令
powerby update
```

#### 步骤4：验证安装

```bash
# 检查by status

# 检查命令项目状态
power列表
ls -la .claude/commands/
```

## 🎯 首次使用

### 1. 初始化项目

```bash
/powerby.initialize 任务管理系统 "实现团队协作的任务管理应用"
```

这将创建：
- `docs/constitution.md` - 项目宪章
- `.powerby/project.json` - 项目配置
- `.powerby/iterations.json` - 迭代追踪

### 2. 定义需求

```bash
/powerby.define "构建一个任务管理系统，支持任务创建、分配、跟踪和完成"
```

这将生成：
- `docs/iterations/001-任务管理系统/prd.md` - 产品需求文档
- `docs/iterations/001-任务管理系统/function-points.md` - 功能点清单
- `docs/iterations/001-任务管理系统/clarifications.md` - 澄清记录

### 3. 技术调研

```bash
/powerby.research
```

### 4. 架构设计

```bash
/powerby.design
```

### 5. 任务规划

```bash
/powerby.plan --tasks-per-day 3
```

### 6. 开发实现

```bash
/powerby.implement --tdd
```

### 7. 代码审查

```bash
/powerby.review
```

## ⚡ 快速流程（适用于小需求）

对于工作量≤3天的小需求，可以使用快速流程：

```bash
/powerby.quick 为现有系统添加用户收藏功能，预计2天完成
```

快速流程包括：
- P0: 快速初始化
- P1: 需求定稿制（融合定义与澄清）
- P3: 技术快速调研
- P4: 架构快速设计
- P5: 任务快速规划

**总时间**：≤5小时
**适用场景**：临时功能、简单Bug修复、已有项目的功能扩展

## 📋 系统要求

### 必需条件

- **Claude Desktop**: 最新版本
- **操作系统**: macOS 或 Linux
- **权限**: 对项目目录的读写权限

### 可选条件

- **Python**: 3.7+（用于CLI工具）
- **Git**: 最新版本（用于版本管理）
- **Node.js**: 16+（用于高级功能）

## 🔧 配置说明

### 项目目录结构

安装完成后，您的项目将包含：

```
your-project/
├── .claude/
│   └── commands/              # PowerBy命令文件
│       ├── powerby-init.md
│       ├── powerby-initialize.md
│       ├── powerbydefine.md
│       ├── powerby-research.md
│       ├── powerby-design.md
│       ├── powerby-plan.md
│       ├── powerby-implement.md
│       ├── powerby-review.md
│       └── powerby-quick.md
├── .powerby/                  # PowerBy配置
│   ├── project.json          # 项目元数据
│   └── iterations.json       # 迭代追踪
└── docs/                      # 项目文档
    ├── constitution.md       # 项目宪章
    └── iterations/           # 迭代文档
        └── 001-{项目名}/
            ├── prd.md
            ├── function-points.md
            ├── clarifications.md
            ├── technical-research.md
            ├── architecture.md
            ├── data-model.md
            ├── contracts/
            ├── tasks.md
            ├── implementation-report.md
            ├── code-review-report.md
            └── delivery-report.md
```

### 配置文件

**`.powerby/project.json`**:
```json
{
  "name": "项目名称",
  "version": "1.0.0",
  "current_phase": "P0",
  "completed_gates": [],
  "status": "initialized",
  "created_at": "2025-12-19T14:00:00Z"
}
```

## 🎓 学习资源

### 文档链接

- [PowerBy工作流完整指南](docs/powerby-workflow-complete-guide.md)
- [质量门禁系统](docs/powerby-quality-gates.md)
- [生命周期框架](docs/powerby-lifecycle-framework.md)
- [技能清单](skills/README.md)

### 技能文档

- [powerby-product 技能](skills/powerby-product/SKILL.md)
- [powerby-architect 技能](skills/powerby-architect/SKILL.md)
- [powerby-engineer 技能](skills/powerby-engineer/SKILL.md)
- [powerby-code-review 技能](skills/powerby-code-review/SKILL.md)
- [powerby-command 技能](skills/powerby-command/SKILL.md)

## ❓ 常见问题

### Q1: 安装后命令不显示

**症状**: 输入`/powerby`没有自动补全

**解决方案**:
```bash
# 1. 重新安装命令
/powerby.init

# 2. 检查目录结构
ls -la .claude/commands/

# 3. 验证命令文件
cat .claude/commands/powerby-initialize.md
```

### Q2: 提示权限不足

**症状**: 安装时提示Permission denied

**解决方案**:
```bash
# 修复权限
chmod 755 .claude/commands/
chmod 644 .claude/commands/powerby-*.md

# 重新安装
/powerby.init
```

### Q3: 命令执行失败

**症状**: 运行命令时报错

**解决方案**:
1. 检查项目是否已初始化
2. 确认`.powerby`目录存在
3. 查看Claude错误日志
4. 重新运行`/powerby.init`

### Q4: 如何更新到最新版本

**解决方案**:
```bash
# 自动更新到最新版本
/powerby.init

# 或使用CLI工具
powerby update
```

### Q5: 如何卸载PowerBy

**解决方案**:
```bash
# 使用CLI清理
powerby clean

# 或手动删除
rm -rf .claude/commands/powerby-*.md
rm -rf .powerby/
```

### Q6: 支持哪些操作系统

**当前支持**:
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 18.04+, CentOS 7+)
- ✅ Windows (通过WSL)

**暂不支持**:
- ❌ Windows原生（需要WSL）

## 🛠️ 高级配置

### 自定义命令参数

您可以通过修改`.claude/commands/`中的md文件来自定义命令行为。

### 集成其他工具

PowerBy可以与以下工具集成：
- Git (版本控制)
- Jira (项目管理)
- Slack (团队协作)
- Docker (容器化)
- CI/CD (持续集成)

### 环境变量

```bash
# 可选配置
export POWERBY_DEFAULT_PHASE=P1
export POWERBY_AUTO_NEXT=true
export POWERBY_LOG_LEVEL=INFO
```

## 📞 获取帮助

### 联系方式

- **GitHub Issues**: [提交问题](https://github.com/your-org/powerby-skills/issues)
- **文档反馈**: [提出改进建议](https://github.com/your-org/powerby-skills/discussions)
- **社区讨论**: [加入讨论](https://github.com/your-org/powerby-skills/discussions)

### 反馈渠道

1. **功能建议**: 通过GitHub Issues提交
2. **Bug报告**: 使用Issue模板报告
3. **文档改进**: 提交Pull Request
4. **使用经验**: 分享到 Discussions

## 🎉 恭喜！

如果您看到这里，说明您已经成功安装了PowerBy Skills！

### 下一步

1. **创建您的第一个项目**: 使用`/powerby.initialize`
2. **学习MVP流程**: 阅读[工作流指南](docs/powerby-workflow-complete-guide.md)
3. **加入社区**: 与其他用户交流经验
4. **持续优化**: 根据使用反馈改进流程

### 快速参考卡

```
# 常用命令
/powerby.initialize [项目名] "[描述]"     # 初始化项目
/powerby.define "[需求描述]"              # 定义需求
/powerby.quick "[小需求]"                 # 快速流程
/powerby.design                          # 架构设计
/powerby.implement                       # 开发实现

# 检查状态
ls -la .powerby/                         # 查看项目状态
cat .powerby/project.json                # 查看配置
```

---

**版本**: v3.3.0
**更新时间**: 2025-12-19
**文档维护**: PowerBy Team

祝您使用愉快！ 🎊