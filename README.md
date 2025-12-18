# PowerBy Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-org/powerby-skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai/code)

## 🎯 概述

PowerBy Skills是一套完整的AI产品开发流程技能包，专为Claude Code设计。它覆盖从需求定义（P0）到代码审查（P8）的完整产品开发生命周期，帮助团队以MVP优先的方式高效推进项目。

## ✨ 核心特性

- 🔄 **完整生命周期覆盖**：P0-P8全阶段支持
- 🎯 **MVP优先原则**：快速验证核心假设
- 🧩 **Mixin思维协作**：增量补充，动态演进
- 📊 **结构化流程**：清晰的阶段门禁和验收标准
- 🤖 **AI驱动开发**：自动化文档生成和流程管理
- 🔍 **零假设原则**：确保需求理解准确无误

## 📦 技能包结构

### 核心流程技能 (powerby-core)

| 技能 | 角色 | 阶段 | 描述 |
|------|------|------|------|
| `powerby-product` | 产品经理 | P0-P2 | 项目初始化、需求定义、需求澄清 |
| `powerby-architect` | 系统架构师 | P3-P4 | 技术调研、架构设计 |
| `powerby-engineer` | 软件工程师 | P5-P6 | 开发规划、开发实现 |
| `powerby-code-review` | 代码审查员 | P7-P8 | 代码审查、交付管理 |

### 原子化专精技能 (powerby-atomic)

| 技能 | 功能 | 适用场景 |
|------|------|----------|
| `requirement-alignment` | 需求对齐与确认 | P0-P2全阶段 |
| `mvp-prioritization` | MVP优先级评估 | P1需求定义 |
| `function-point-checker` | 功能点清单生成 | P1-P2阶段 |
| `solution-evaluation` | 技术方案评估 | P3-P6阶段 |
| `mermaid-architecture` | 架构可视化 | P3-P4阶段 |
| `test-spec-design` | 测试规格设计 | P5-P6阶段 |

## 🚀 快速开始

### 安装

#### 方法1：通过Git URL直接安装（推荐）

在Claude Code中运行：

```bash
/plugin install powerby-core@git+https://github.com/your-org/powerby-skills
/plugin install powerby-atomic@git+https://github.com/your-org/powerby-skills
```

#### 方法2：克隆到本地

```bash
git clone https://github.com/your-org/powerby-skills.git
```

然后在Claude Code中：

```bash
/plugin marketplace add file:///path/to/powerby-skills
```

### 验证安装

```bash
/plugin list | grep powerby
```

## 💡 使用示例

### 场景1：新产品开发（P0-P1）

```bash
# 启动产品需求定义
请使用powerby-product技能帮助我定义一个AI驱动的电商推荐系统的需求。
```

**Claude Code将引导您完成：**
1. P0 项目初始化 - 创建项目宪章
2. P1 需求定义 - 生成PRD和功能点清单
3. 基于Mixin思维进行多角色协作

### 场景2：技术架构设计（P3-P4）

```bash
# 启动架构设计
请使用powerby-architect技能为电商推荐系统设计技术架构。我已有PRD文档。
```

**Claude Code将：**
1. 分析PRD文档
2. 进行技术调研
3. 设计系统架构
4. 生成Mermaid架构图

### 场景3：MVP优先级评估

```bash
# 评估功能优先级
请使用mvp-prioritization技能帮助我评估这个功能列表的MVP优先级。
```

### 场景4：功能点提取

```bash
# 提取功能点清单
请使用function-point-checker技能从我的PRD中提取功能点。
```

## 🏗️ PowerBy生命周期

PowerBy Skills严格遵循PowerBy生命周期框架：

```
P0: 项目初始化 → P1: 需求定义 → P2: 需求澄清
   ↓
P3: 技术调研 → P4: 架构设计
   ↓
P5: 开发规划 → P6: 开发实现
   ↓
P7: 代码审查 → P8: 交付管理
```

### 阶段门禁机制

每个阶段都有严格的质量门禁：

- **Gate 1 (P1→P2)**：MVP范围确认
- **Gate 2 (P2→P3)**：需求澄清完整性
- **Gate 3 (P4→P5)**：架构方案确认
- **Gate 4 (P6→P7)**：开发完成度检查
- **Gate 5 (P7→P8)**：质量标准验证

## 🧩 Mixin思维协作

PowerBy Skills采用创新的Mixin思维协作模式：

### 核心原则

1. **增量补充**：各角色以Mixin方式共同维护单一功能文档
2. **组合优于完整**：不追求一次性完美，随着项目推进逐步丰富
3. **容忍阶段性缺失**：产品阶段缺失技术和设计细节是正常的
4. **动态演进**：文档像代码一样迭代演进

### 协作流程

```
产品经理 → 定义功能清单和优先级
   ↓ (Mixin补充)
架构师 → 添加技术实现方案
   ↓ (Mixin补充)
工程师 → 添加开发任务和测试方案
   ↓ (Mixin补充)
审查员 → 验证实现一致性
```

## 📚 核心原则

### 1. 零假设原则 (Zero-Assumption Principle)

- 绝不猜测用户的模糊意图
- 信息不足时主动提问澄清
- 所有假设都需要验证

### 2. MVP优先原则

- 识别核心价值，定义最小功能集
- 无情地削减非核心功能
- 明确标记可推迟项

### 3. 逻辑闭环

- 每个决策点都有清晰的逻辑阐述
- 明确影响范围和连锁反应
- 确保前后一致，不自相矛盾

### 4. Mixin思维

- 增量补充，组合优于完整
- 各角色共同维护单一功能文档
- 容忍阶段性缺失，动态演进

## 📁 项目结构

```
powerby-skills/
├── .claude-plugin/
│   └── marketplace.json          # 技能市场配置
├── skills/                       # 技能目录
│   ├── powerby-product/          # 产品经理技能
│   ├── powerby-architect/        # 架构师技能
│   ├── powerby-engineer/         # 工程师技能
│   ├── powerby-code-review/      # 代码审查技能
│   ├── requirement-alignment/    # 需求对齐
│   ├── mvp-prioritization/       # MVP优先级
│   ├── function-point-checker/   # 功能点检查
│   ├── solution-evaluation/      # 方案评估
│   ├── mermaid-architecture/     # 架构可视化
│   └── test-spec-design/         # 测试规格
├── docs/                         # 文档目录
│   ├── powerby-consitution.md    # 项目宪法
│   ├── powerby-lifecycle-overview.md
│   └── powerby-*.md              # 其他文档
├── CLAUDE-INTEGRATION.md         # Claude集成指南
├── README.md                     # 项目说明
├── package.json                  # 项目配置
└── LICENSE                       # 开源协议
```

## 🔧 技能详解

### powerby-product

**产品经理技能（P0-P2）**

- **P0 项目初始化**：建立项目宪章和基础设施
- **P1 需求定义**：将产品想法转化为清晰的功能点清单
- **P2 需求澄清**：通过结构化提问消除需求模糊性

**核心能力：**
- MVP功能分解
- 待决策清单生成
- 需求覆盖率分析
- 功能点清单生成

### powerby-architect

**系统架构师技能（P3-P4）**

- **P3 技术调研**：深度技术方案研究
- **P4 架构设计**：将需求转化为技术架构

**核心能力：**
- 技术选型评估
- 架构方案设计
- Mermaid图表生成
- 方案权衡分析

### powerby-engineer

**软件工程师技能（P5-P6）**

- **P5 开发规划**：制定详细的开发任务计划
- **P6 开发实现**：严格按照计划执行开发

**核心能力：**
- 任务分解
- TDD测试驱动开发
- 小步提交策略
- 文档驱动开发

### powerby-code-review

**代码审查员技能（P7-P8）**

- **P7 代码审查**：确保代码质量和流程闭环
- **P8 交付管理**：最终交付和质量验证

**核心能力：**
- 代码质量审计
- 流程合规性检查
- 文档一致性验证
- 最终质量门禁

### 原子技能

#### requirement-alignment
- 需求结构化复述
- 关键要素提炼
- 边界明确
- 假设识别

#### mvp-prioritization
- 核心价值识别
- 功能原子化
- MVP优先级评估（P0/P1/P2）
- 削减验证

#### function-point-checker
- PRD文档解析
- 功能点提取
- 结构化输出
- 优先级标注

#### solution-evaluation
- 多方案对比
- 权衡分析
- 复杂度评估
- 风险识别

#### mermaid-architecture
- 系统架构图
- 组件关系图
- 序列图
- 流程图

#### test-spec-design
- 测试策略制定
- 测试用例设计
- 验收标准定义
- 覆盖率规划

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 贡献范围

- 🐛 Bug修复
- ✨ 新功能开发
- 📚 文档改进
- 💡 最佳实践分享
- 🎨 代码优化

## 📝 更新日志

### v1.0.0 (2025-12-18)

**初始版本发布**

- ✅ 完整的P0-P8生命周期支持
- ✅ Mixin思维协作模式
- ✅ 10个核心技能
- ✅ 阶段门禁机制
- ✅ 完整的文档体系

## 📄 开源协议

本项目采用 [MIT 协议](LICENSE)。

```
MIT License

Copyright (c) 2025 PowerBy Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 致谢

感谢所有为PowerBy Skills做出贡献的开发者和使用者！

特别感谢：
- Claude Code团队提供的技能系统
- 所有参与测试和反馈的用户
- 开源社区的支持

## 📞 联系我们

- 🐛 [Bug报告](https://github.com/your-org/powerby-skills/issues)
- 💡 [功能请求](https://github.com/your-org/powerby-skills/issues)
- 📧 邮箱：contact@powerby.dev
- 💬 讨论：[GitHub Discussions](https://github.com/your-org/powerby-skills/discussions)

## ⭐ 如果这个项目对您有帮助，请给我们一个星标！

---

**PowerBy Skills** - 让AI驱动的产品开发更简单、更高效 🚀
