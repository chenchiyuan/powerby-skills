# PowerBy Skills - AI驱动的产品开发流程技能包

**版本**: v2.2.0
**更新日期**: 2025-12-20
**技能类型**: 完整技能生态系统 (Complete Skill Ecosystem)

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Compatible](https://img.shields.io/badge/Claude-Compatible-blue.svg)](https://claude.ai)
[![MVP Optimized](https://img.shields.io/badge/MVP-Optimized-green.svg)](#)

## 🚀 快速开始

### 一分钟安装

#### 方式一：Claude插件市场安装（推荐）

1. **在Claude中打开技能市场**
   - 点击左侧菜单"技能市场"
   - 搜索"powerby-skills"

2. **安装技能**
   - 点击"powerby-skills"
   - 点击"添加到项目"

3. **安装命令**
   ```bash
   /powerby.init
   ```

4. **开始使用**
   ```bash
   /powerby.initialize 我的项目 "项目描述"
   ```

#### 方式二：GitHub克隆

```bash
git clone https://github.com/your-org/powerby-skills.git
cd powerby-skills/skills/powerby-command
chmod +x setup.sh && ./setup.sh
```

📖 **详细安装指南**: [INSTALL.md](INSTALL.md)

## 📋 概述

PowerBy Skills 是一套完整的AI驱动产品开发流程技能包，涵盖从产品构思到代码交付的完整生命周期。通过严格的质量门禁和MVP精简流程，帮助团队高效产出高质量产品。

## ✨ 核心特性

- **🎯 MVP驱动**: 基于奥卡姆剃刀原则，专注核心价值交付
- **🔄 技能协作**: 7个核心技能协调，覆盖完整产品生命周期
- **📏 质量门禁**: 8个质量门禁确保每个阶段输出质量
- **⚡ 快速流程**: 支持≤3天小需求的快速处理
- **📚 文档驱动**: 完整的文档体系和可追溯性
- **🛡️ 流程守护**: Flow Guardian确保严格遵循流程

### 核心技能

| 技能 | 角色 | 核心能力 | 适用阶段 |
|------|------|---------|----------|
| **powerby-product** | AI产品经理 | MVP驱动需求精炼、功能拆解 | P0-P1 |
| **powerby-architect** | 首席架构师 | 技术架构设计、可视化 | P3-P4 |
| **powerby-engineer** | 资深工程师 | TDD实现、质量保证 | P5-P6 |
| **powerby-code-review** | 首席审查师 | 代码审计、验收方案 | P7-P8 |
| **powerby-command** | 指令管理 | 流程协调、状态管理 | 全流程 |
| **powerby-flow-guardian** | 流程守护 | 状态检查、问题诊断 | 全流程 |

### 完整工作流程

```mermaid
graph LR
    A[产品想法] -->|powerby-product| B[PRD文档]
    B -->|powerby-architect| C[架构设计]
    C -->|powerby-engineer| D[代码实现]
    D -->|powerby-code-review| E{质量审查}
    E -->|通过| F[产品交付]
    E -->|失败| G[修改代码]
    G --> D
```

## 🏗️ 架构设计

```mermaid
graph TB
    subgraph "PowerBy Skills 生态"
        PM[powerby-product<br/>产品经理]
        ARCH[powerby-architect<br/>架构师]
        ENG[powerby-engineer<br/>工程师]
        CR[powerby-code-review<br/>代码审查]
        FG[powerby-flow-guardian<br/>流程守护者]
        CMD[powerby-command<br/>指令管理] ⭐
    end

    subgraph "指令调用"
        INIT[/powerby.initialize]
        DEFINE[/powerby.define]
        CLARIFY[/powerby.clarify]
        RESEARCH[/powerby.research]
        DESIGN[/powerby.design]
        PLAN[/powerby.plan]
        IMPLEMENT[/powerby.implement]
        REVIEW[/powerby.review]
    end

    %% 指令到CMD的关系
    INIT --> CMD
    DEFINE --> CMD
    CLARIFY --> CMD
    RESEARCH --> CMD
    DESIGN --> CMD
    PLAN --> CMD
    IMPLEMENT --> CMD
    REVIEW --> CMD

    %% CMD到技能的映射
    CMD --> PM
    CMD --> ARCH
    CMD --> ENG
    CMD --> CR

    %% 流程维护
    CMD -.-> FG

    classDef commandSkill fill:#4caf50,stroke:#388e3c,stroke-width:3px,color:#fff
    class CMD commandSkill
```

## 🎯 完整工作流程

### 标准流程（适用于新项目）

```bash
# 步骤1: 项目初始化 (P0)
/powerby.initialize 电商平台 "构建B2C电商核心功能"

# 步骤2: 需求定义+澄清 (P1)
/powerby.define "实现用户注册、商品浏览、购物车和订单管理"

# 步骤3: 技术调研 (P3)
/powerby.research

# 步骤4: 架构设计 (P4)
/powerby.design

# 步骤5: 任务规划 (P5)
/powerby.plan --tasks-per-day 3

# 步骤6: 开发实现 (P6)
/powerby.implement --tdd

# 步骤7: 代码审查 (P7)
/powerby.review
```

### 快速流程（适用于小需求，≤3天）

```bash
# 适用于临时功能、简单Bug修复、功能扩展
/powerby.quick 为购物车添加优惠券功能，预计2天完成
```

**快速流程特点**：
- ⚡ 总时间≤5小时
- 🎯 P1+P2融合（需求定稿制）
- ✅ 关键节点人工确认
- 📦 基于现有架构增量开发

### MVP精简流程

```
P0 → P1 → P3 → P4 → P5 → P6 → P7
```

**注意**：
- ✅ P2（独立澄清阶段）已合并到P1中
- ✅ P8（运维交付）为可选流程
- ✅ 总共7个核心阶段，专注MVP交付

## 📖 完整指令参考

### 核心指令列表

| 指令 | 阶段 | 对应技能 | 主要职责 | 输出文档 |
|------|------|---------|---------|----------|
| `/powerby.initialize` | P0 | powerby-command | 项目初始化，定义迭代主任务 | constitution.md, project.json |
| `/powerby.define` | P1 | powerby-product | 需求定义+澄清，融合P1+P2 | prd.md, function-points.md, clarifications.md |
| `/powerby.quick` | P0-P5 | powerby-fullstack | 快速流程，≤3天需求 | 快速流程文档集合 |
| `/powerby.research` | P3 | powerby-architect | 技术调研，评估技术方案 | technical-research.md |
| `/powerby.design` | P4 | powerby-architect | 架构设计，四阶段强制流程 | architecture.md, data-model.md, contracts/ |
| `/powerby.plan` | P5 | powerby-engineer | 任务规划，分解可执行任务 | tasks.md, checklists/ |
| `/powerby.implement` | P6 | powerby-engineer | 开发实现，TDD开发方式 | 代码+测试+实现报告 |
| `/powerby.review` | P7-P8 | powerby-code-review | 代码审查，质量把控 | code-review-report.md, delivery-report.md |

### 快速流程指令

| 指令 | 适用场景 | 时间控制 | 特点 |
|------|---------|---------|------|
| `/powerby.quick` | ≤3天的小需求 | ≤5小时 | P1融合、人工确认、增量开发 |

### 质量门禁系统

| Gate | 阶段转换 | 检查要点 | 通过标准 |
|------|----------|----------|----------|
| Gate 1 | P1→P3 | MVP需求定稿 | 核心价值、功能完整性、范围明确 |
| Gate 3 | P3→P4 | 技术调研完整性 | 技术选型、可行性、风险评估 |
| Gate 4 | P4→P5 | 架构设计清晰性 | 组件职责、数据流、决策记录 |
| Gate 5 | P5→P6 | 开发规划详细性 | 任务分解、依赖关系、验收标准 |
| Gate 6 | P6→P7 | 开发实现质量 | 功能完整、代码质量、测试覆盖 |
| Gate 7 | P7→完成 | 代码审查严格性 | 规范检查、安全审查、性能评估 |

### 指令执行流程

```mermaid
sequenceDiagram
    participant User
    participant CMD as powerby-command
    participant FG as powerby-flow-guardian
    participant PM as powerby-product
    participant ARCH as powerby-architect
    participant ENG as powerby-engineer
    participant CR as powerby-code-review

    User->>CMD: 输入指令 (如 /powerby.define)
    CMD->>CMD: 解析指令
    CMD->>FG: 检查当前状态和前置条件
    FG-->>CMD: 返回状态分析
    CMD->>CMD: 验证指令合法性

    alt 指令合法
        CMD->>对应技能: 调用相应技能
        对应技能-->>CMD: 返回执行结果
        CMD->>FG: 更新项目状态
        CMD-->>User: 返回成功结果和下一步指导
    else 指令不合法
        CMD-->>User: 返回错误信息和解决建议
    end
```

## 🔍 质量门禁

每个阶段都有对应的质量门禁检查：

| Gate | 阶段 | 检查要点 | 通过标准 |
|------|------|----------|----------|
| Gate 1 | P1→P2 | MVP范围合理性 | 5项验收标准 |
| Gate 2 | P2→P3 | 需求澄清充分性 | 4项验收标准 |
| Gate 3 | P3→P4 | 技术调研完整性 | 4项验收标准 |
| Gate 4 | P4→P5 | 架构设计清晰性 | 5项验收标准 |
| Gate 5 | P5→P6 | 开发规划详细性 | 5项验收标准 |
| Gate 6 | P6→P7 | 开发实现质量 | 6项验收标准 |
| Gate 7 | P7→P8 | 代码审查严格性 | 5项验收标准 |
| Gate 8 | P8→完成 | 项目交付完整性 | 6项验收标准 |

## 🎯 最佳实践

### ✅ 推荐做法

1. **严格遵循流程**: 不跳过任何阶段或门禁
2. **充分确认**: 每个阶段都等待门禁检查通过
3. **记录决策**: 所有重要决策都有文档记录
4. **及时更新**: 状态变化立即更新到项目元数据
5. **主动澄清**: 遇到模糊点主动询问Flow Guardian

### ❌ 避免做法

1. **流程跳跃**: 不要跳过前置阶段直接进入后续阶段
2. **门禁绕过**: 不要绕过质量门禁检查
3. **文档滞后**: 避免代码实现与文档不同步
4. **重复造轮子**: 优先使用现有库和服务

## 📁 项目结构

```
powerby-skills/                          # 项目根目录
├── 📄 README.md                        # 项目说明（本文件）
├── 📄 INSTALL.md                       # 详细安装指南 ⭐
├── 📄 LICENSE                          # MIT许可证
├── 📄 package.json                     # 项目配置
├── 📁 skills/                          # 技能包目录
│   ├── 📁 powerby-command/             # 指令管理技能
│   │   ├── SKILL.md                    # 技能定义文档
│   │   ├── README.md                   # 使用说明
│   │   ├── COMMANDS_VALIDATION_REPORT.md # 命令验证报告
│   │   ├── THIRD_PARTY_INSTALLATION.md # 第三方安装指南
│   │   ├── setup.sh                    # 安装脚本
│   │   ├── powerby-cli.py              # CLI工具
│   │   └── 📁 templates/               # 命令模板
│   │       └── 📁 .claude/
│   │           └── 📁 commands/        # 9个命令模板文件
│   ├── 📁 powerby-product/             # 产品经理技能
│   ├── 📁 powerby-architect/           # 架构师技能
│   ├── 📁 powerby-engineer/            # 工程师技能
│   ├── 📁 powerby-code-review/         # 代码审查技能
│   ├── 📁 solution-evaluation/         # 方案评估技能
│   ├── 📁 requirement-alignment/       # 需求对齐技能
│   ├── 📁 mermaid-architecture/        # 架构可视化技能
│   ├── 📁 test-spec-design/            # 测试规格设计技能
│   ├── 📁 mvp-prioritization/          # MVP优先级评估技能
│   └── 📁 function-point-checker/      # 功能点检查技能
├── 📁 docs/                            # 文档目录
│   ├── powerby-workflow-complete-guide.md # 完整工作流指南
│   ├── powerby-quality-gates.md        # 质量门禁指南
│   └── powerby-lifecycle-framework.md  # 生命周期框架
└── 📁 .claude-plugin/                  # Claude插件配置
    └── marketplace.json                # 市场配置
```

## 🔧 技能协作

### 技能调用链

```
用户输入 /powerby.command
    ↓
powerby-command 解析指令
    ↓
检查前置条件和当前状态
    ↓
调用对应核心技能
    ↓
执行工作流程
    ↓
更新项目状态
    ↓
返回结果给用户
```

### 核心技能职责

**powerby-product (P0-P1)**
- 产品需求定义
- MVP功能拆解
- 优先级评估
- 用户故事编写

**powerby-architect (P3-P4)**
- 技术选型分析
- 系统架构设计
- 数据模型设计
- API契约定义

**powerby-engineer (P5-P6)**
- 任务分解规划
- TDD开发实现
- 代码质量保证
- 测试覆盖率达标

**powerby-code-review (P7-P8)**
- 代码质量审计
- 安全性审查
- 性能评估
- 验收方案设计

### Flow Guardian流程守护

**功能职责**：
- ✅ 状态检查：实时跟踪项目当前阶段
- ✅ 前置验证：确保每个阶段的前置条件满足
- ✅ 门禁检查：验证每个阶段的质量门禁
- ✅ 流程指导：提供下一步操作建议

**使用方式**：
```bash
/powerby-flow-guardian analyze  # 查看当前状态
/powerby-flow-guardian check    # 检查前置条件
/powerby-flow-guardian guide    # 获取操作指导
```

## 📚 学习资源

### 必读文档

- 📖 **[安装指南](INSTALL.md)** - 详细的安装步骤和配置说明 ⭐
- 📋 **[完整工作流指南](docs/powerby-workflow-complete-guide.md)** - PowerBy完整流程说明
- 🔒 **[质量门禁指南](docs/powerby-quality-gates.md)** - 质量检查标准
- 🔄 **[生命周期框架](docs/powerby-lifecycle-framework.md)** - 核心理论框架

### 技能文档

- **powerby-product**: [SKILL.md](skills/powerby-product/SKILL.md) - 产品经理技能
- **powerby-architect**: [SKILL.md](skills/powerby-architect/SKILL.md) - 架构师技能
- **powerby-engineer**: [SKILL.md](skills/powerby-engineer/SKILL.md) - 工程师技能
- **powerby-code-review**: [SKILL.md](skills/powerby-code-review/SKILL.md) - 代码审查技能
- **powerby-command**: [SKILL.md](skills/powerby-command/SKILL.md) - 指令管理技能

### 第三方安装

- 📦 **[第三方安装指南](skills/powerby-command/THIRD_PARTY_INSTALLATION.md)** - Claude插件市场安装
- ✅ **[命令验证报告](skills/powerby-command/COMMANDS_VALIDATION_REPORT.md)** - 安装完整性验证

### 实践案例

- [任务管理系统案例](examples/task-management-system/)
- [电商平台案例](examples/ecommerce-platform/)
- [博客系统案例](examples/blog-system/)

## 🛠️ 故障排除

### 常见问题

#### 问题1：命令不显示
**症状**: 输入`/powerby`没有自动补全

**解决方案**:
```bash
# 1. 重新安装命令
/powerby.init

# 2. 检查目录结构
ls -la .claude/commands/

# 3. 验证安装
cat .claude/commands/powerby-initialize.md
```

#### 问题2：权限错误
**症状**: 安装时提示Permission denied

**解决方案**:
```bash
# 修复权限
chmod 755 .claude/commands/
chmod 644 .claude/commands/powerby-*.md

# 重新安装
/powerby.init
```

#### 问题3：命令执行失败
**症状**: 运行命令时报错

**解决方案**:
1. 检查项目是否已初始化（需要`.powerby`目录）
2. 确认`.claude/commands/`目录中有所有命令文件
3. 查看Claude错误日志
4. 重新运行`/powerby.init`

#### 问题4：前置条件错误
```
❌ 错误: 当前阶段是P0，需要P1阶段才能执行此指令

💡 建议: 请先执行 /powerby.initialize 完成项目初始化
```

#### 问题5：文档缺失错误
```
❌ 错误: 缺少必需文档: docs/constitution.md

💡 建议: 请先执行 /powerby.initialize 创建项目宪章
```

#### 问题6：门禁检查失败
```
❌ 错误: Gate 1检查失败 - MVP范围不合理

💡 建议:
   - 重新审视核心价值定义
   - 削减非必要功能
   - 使用 /powerby.define 重新定义需求
```

### 获取帮助

- 📖 **详细故障排除**: [INSTALL.md](INSTALL.md#-常见问题)
- 🐛 **提交Bug**: [GitHub Issues](https://github.com/your-org/powerby-skills/issues)
- 💬 **社区讨论**: [GitHub Discussions](https://github.com/your-org/powerby-skills/discussions)
- 📧 **邮件联系**: powerby-team@example.com

## 📝 更新日志

### v2.2.0 (2025-12-20) ⭐ 最新版本

**Fail-Fast钢铁纪律与语义化文档契约整合**

#### 重大更新
- ✨ **第6条核心原则**: Fail-Fast钢铁纪律
  - 显式抛出，禁止隐藏
  - 契约先行（Guard Clauses）
  - 报错即文档
  - 防御性编程
  - 异常即规格
  - 确定性抛出
  - 禁止静默返回

- ✨ **第7条核心原则**: 语义化文档契约
  - 注释即负债的抵消
  - 标准化协议（JSDoc/Python Docstrings/GoDoc等）
  - 同步演进（逻辑改动，注释必须先动）
  - 契约透明化

#### 新增功能
- 🔧 **P5阶段优化**: tasks.md模板强制异常路径验证和边界检查
- 🔧 **P6阶段文档驱动TDD**: TDD循环扩展为红-文档-绿-重构
- 🔧 **Gate 6质量门禁强化**: 新增文档化率检查（公共接口100%覆盖）
- 🔧 **架构设计升级**: 整合Fail-Fast要求到原子层定义准则

#### 技能文档更新
- ✅ powerby-engineer: 完整整合7条核心原则
- ✅ powerby-command: 整合7条核心原则到工作流程
- ✅ powerby-architect: 整合Fail-Fast钢铁纪律到架构设计
- ✅ 所有技能文档版本同步到v2.2.0

#### 变更类型
- **核心原则**: 重大增强
- **流程创新**: 文档驱动TDD
- **质量门禁**: 文档化率硬性标准

### v2.1.0 (2025-12-19)

**MVP精简优化版本**

#### 新增功能
- ✅ MVP精简流程：移除P2独立澄清阶段，合并到P1中
- ✅ 快速流程支持：新增`/powerby.quick`命令，支持≤3天小需求
- ✅ 第三方安装支持：完整的Claude插件市场安装指南
- ✅ 命令验证报告：100%命令定义完整性验证

#### 优化改进
- ✅ 奥卡姆剃刀原则应用：移除非功能性属性扫描
- ✅ P8运维流程独立：标记为可选流程
- ✅ 命令参数简化：`initialize`和`define`命令更加简洁
- ✅ 安装方法标准化：支持多种安装方式

#### 修复问题
- ✅ 修复powerby-init.md中P2残留引用
- ✅ 同步POWERBY_COMMANDS列表与实际文件
- ✅ 更新所有文档与MVP精简流程一致

#### 文档更新
- ✅ 新增INSTALL.md详细安装指南
- ✅ 更新README.md完整使用说明
- ✅ 新增第三方安装指南
- ✅ 新增命令验证报告

### 版本规划

**v2.3.0 (计划中)**
- 📋 自动化测试套件
- 📊 可视化进度仪表板
- 🔗 第三方工具集成

**v3.0.0 (未来)**
- 🤖 AI辅助决策优化
- 📱 移动端支持
- 🌐 多语言支持

## 📄 许可证

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

我们欢迎社区贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 贡献方式

- 🐛 提交Bug报告
- 💡 提出功能建议
- 📖 改进文档
- 💻 提交代码改进

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-org/powerby-skills.git
cd powerby-skills

# 安装依赖
npm install

# 运行测试
npm test

# 构建项目
npm run build
```

## 📊 项目统计

[![GitHub stars](https://img.shields.io/github/stars/your-org/powerby-skills.svg?style=social&label=Star)](https://github.com/your-org/powerby-skills)
[![GitHub forks](https://img.shields.io/github/forks/your-org/powerby-skills.svg?style=social&label=Fork)](https://github.com/your-org/powerby-skills/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/your-org/powerby-skills.svg?style=social&label=Watch)](https://github.com/your-org/powerby-skills)

### 技能包统计

- **核心技能**: 5个
- **原子技能**: 6个
- **总指令数**: 9个
- **质量门禁**: 8个
- **文档页数**: 50+

## 👥 团队

- **项目负责人**: PowerBy Team
- **核心开发**: Claude AI
- **文档维护**: Community Contributors
- **质量保证**: PowerBy QA Team

## 🙏 致谢

感谢所有为PowerBy Skills做出贡献的开发者和用户！

### 技术支持

- **Claude AI**: 提供强大的AI能力支持
- **开源社区**: 提供宝贵的反馈和建议
- **早期用户**: 帮助我们不断改进产品

## 🔮 未来规划

### 短期目标（3个月）

- [ ] 自动化测试覆盖率提升至90%
- [ ] 新增5个原子技能
- [ ] 完善可视化工具
- [ ] 社区文档翻译

### 中期目标（6个月）

- [ ] 支持更多AI模型
- [ ] 集成CI/CD流水线
- [ ] 开发VS Code插件
- [ ] 建立认证体系

### 长期愿景（1年）

- [ ] 成为行业标准
- [ ] 构建开发者生态
- [ ] 支持企业级部署
- [ ] 实现完全自动化

---

## 🎯 开始使用

**安装只需3步**:

1. **安装技能**: 在Claude中搜索"powerby-skills"并安装
2. **运行安装命令**: `/powerby.init`
3. **开始第一个项目**: `/powerby.initialize 我的项目 "项目描述"`

📖 **详细说明**: [INSTALL.md](INSTALL.md)

**祝您使用愉快！** 🎉
