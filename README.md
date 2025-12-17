# PowerBy Skills Framework

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![PowerBy Lifecycle](https://img.shields.io/badge/PowerBy-Lifecycle%20P0--P8-orange.svg)](./docs/powerby-lifecycle-overview.md)

PowerBy Skills Framework 是一个完整的AI驱动软件开发生命周期管理框架，通过标准化的技能和流程，将产品想法高效转化为可交付的软件产品。

## 🎯 核心价值

- **标准化流程**: P0-P8完整生命周期，每个阶段都有明确的产出和验收标准
- **技能驱动**: 8个核心技能 + 5个原子技能，覆盖产品全生命周期
- **迭代管理**: 自动编号、语义命名、分支隔离的迭代规范
- **文档驱动**: 完整的文档模板和最佳实践指南
- **质量保证**: 8个质量门禁（Gate 1-8），确保每个阶段的质量

## 📚 文档导航

### 快速开始
- [生命周期框架概览](./docs/powerby-lifecycle-overview.md) - 了解完整的P0-P8流程
- [PRD示例](./demo-prd.md) - 查看完整的PRD文档示例
- [功能点描述最佳实践](./docs/Function-Description-Best-Practices.md) - 学习如何编写高质量功能点

### 核心文档
- [更新日志](./CHANGELOG.md) - 版本变更记录
- [PowerBy生命周期框架](./docs/powerby-lifecycle-overview.md) - 详细的生命周期说明
- [PRD模板](./templates/prd-template.md) - 标准的产品需求文档模板

### 技能文档
- **核心技能**:
  - [`powerby-product`](./skills/powerby-product/) - 产品经理（P0-P2）
  - [`powerby-architect`](./skills/powerby-architect/) - 架构师（P3-P4）
  - [`powerby-engineer`](./skills/powerby-engineer/) - 工程师（P5-P6）
  - [`powerby-code-review`](./skills/powerby-code-review/) - 代码审查员（P7-P8）

- **原子技能**:
  - [`requirement-alignment`](./skills/requirement-alignment/) - 需求对齐与确认
  - [`mvp-prioritization`](./skills/mvp-prioritization/) - MVP优先级评估
  - [`solution-evaluation`](./skills/solution-evaluation/) - 技术方案评估
  - [`mermaid-architecture`](./skills/mermaid-architecture/) - 架构可视化
  - [`test-spec-design`](./skills/test-spec-design/) - 测试规格设计

## 🏗️ PowerBy生命周期框架

### 阶段概览

| 阶段 | 名称 | 核心技能 | 主要产出 | 质量门禁 |
|------|------|---------|---------|---------|
| **P0** | 项目初始化 | Product | 项目宪章 | - |
| **P1** | 需求定义 | Product | PRD文档 | Gate 1 |
| **P2** | 需求澄清 | Product | 澄清记录 | Gate 2 |
| **P3** | 技术调研 | Architect | 技术调研报告 | Gate 3 |
| **P4** | 架构设计 | Architect | 架构文档 | Gate 4 |
| **P5** | 开发规划 | Engineer | 任务计划 | Gate 5 |
| **P6** | 开发实现 | Engineer | 实现报告 | Gate 6 |
| **P7** | 代码审查 | Code Review | 审查报告 | Gate 7 |
| **P8** | 项目交付 | Code Review | 交付报告 | Gate 8 |

### 迭代管理规范

每个需求迭代遵循完整的生命周期：

```
迭代编号: 001, 002, 003...
分支名称: {编号}-{功能名}
文档路径: docs/iterations/{id}-{name}/
元数据追踪: .powerby/iterations.json
```

## 🎓 快速入门

### 1. 了解框架
阅读 [生命周期框架概览](./docs/powerby-lifecycle-overview.md) 了解P0-P8各阶段的职责和产出。

### 2. 学习最佳实践
查看 [功能点描述最佳实践](./docs/Function-Description-Best-Practices.md) 学会如何编写清晰、可执行的功能点描述。

### 3. 使用模板
参考 [PRD示例](./demo-prd.md) 和 [PRD模板](./templates/prd-template.md) 编写产品需求文档。

### 4. 应用技能
根据项目阶段选择合适的技能：
- P0-P2: 使用 `powerby-product`
- P3-P4: 使用 `powerby-architect`
- P5-P6: 使用 `powerby-engineer`
- P7-P8: 使用 `powerby-code-review`

## 💡 v2.0.0 重大更新

### 核心改进：功能点描述标准化（方案C）

**8要素功能点结构**:
```
FX.X [功能点名称] [优先级]
✓ 需求来源: US-X
✓ 功能描述: [1-2句话]
✓ 用户输入: [格式化的输入参数]
✓ 系统输出: [格式化的输出结果]
✓ 关键约束: [性能和业务约束]
✓ 验收标准: [SMART原则的可测试标准]
✓ 依赖关系: [功能点依赖图]
✓ 预估工时: [开发成本估算]
```

**优势对比**:

| 维度 | v1.0 | v2.0 (方案C) |
|------|------|-------------|
| 功能点数量 | 13个宏观功能 | 8个原子功能 |
| 描述要素 | 3个要素 | 8个要素 |
| 可追踪性 | 低 | 高 |
| 可执行性 | 中等 | 高 |
| 依赖关系 | 无 | 清晰可视化 |

详细变更请查看 [更新日志](./CHANGELOG.md#200---2025-12-17)。

## 📊 项目结构

```
powerby-skills/
├── docs/                           # 框架文档
│   ├── powerby-lifecycle-overview.md
│   └── Function-Description-Best-Practices.md
├── skills/                         # 技能文档
│   ├── core/                       # 核心技能
│   │   ├── powerby-product/
│   │   ├── powerby-architect/
│   │   ├── powerby-engineer/
│   │   └── powerby-code-review/
│   └── atomic/                     # 原子技能
│       ├── requirement-alignment/
│       ├── mvp-prioritization/
│       ├── solution-evaluation/
│       ├── mermaid-architecture/
│       └── test-spec-design/
├── templates/                      # 文档模板
│   └── prd-template.md
├── demo-prd.md                    # PRD示例
├── PRD-Function-Description-Options.md  # 方案对比
├── CHANGELOG.md                   # 更新日志
└── README.md                      # 本文档
```

## 🛠️ 使用示例

### 示例1：新产品需求定义（P1阶段）

```markdown
# 使用powerby-product技能
用户: "我想做一个多DEX价格聚合器"
系统: "请提供产品想法、目标用户、核心问题等信息"
...
# 输出：完整的PRD文档（应用方案C的8要素结构）
```

### 示例2：技术架构设计（P4阶段）

```markdown
# 使用powerby-architect技能
用户: "我已经完成了PRD，请帮我设计技术架构"
系统: "请提供PRD文档路径"
...
# 输出：architecture.md，包含架构图和技术决策
```

### 示例3：开发任务规划（P5阶段）

```markdown
# 使用powerby-engineer技能
用户: "请基于架构文档制定开发计划"
系统: "请提供架构文档路径"
...
# 输出：tasks.md，包含分解的开发任务
```

## 🎯 适用场景

- ✅ 新产品从0到1的开发
- ✅ 现有产品的功能迭代
- ✅ 团队流程标准化
- ✅ 项目质量管控
- ✅ 敏捷开发管理
- ✅ 文档驱动开发

## 🔧 技术栈支持

PowerBy框架技术栈无关，支持：
- 前端：React、Vue、Angular等
- 后端：Node.js、Python、Java、Go等
- 移动端：iOS、Android、Flutter等
- 区块链：Ethereum、BSC、Polygon等
- 云平台：AWS、Azure、阿里云等

## 📖 深入阅读

### 核心原理
- [零假设原则](./docs/powerby-lifecycle-overview.md#零假设原则)
- [MVP优先原则](./docs/powerby-lifecycle-overview.md#mvp优先原则)
- [文档驱动开发](./docs/powerby-lifecycle-overview.md#文档驱动开发)

### 实践指南
- [如何编写高质量PRD](./docs/Function-Description-Best-Practices.md)
- [功能点优先级评估](./skills/mvp-prioritization/SKILL.md)
- [架构决策记录](./skills/powerby-architect/SKILL.md)

## 🤝 贡献指南

我们欢迎社区贡献！

### 如何贡献
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献内容
- 🐛 报告Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 修复Bug
- 💬 参与讨论

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为PowerBy框架贡献智慧的团队成员和社区开发者。

## 📞 联系我们

- 项目负责人: PowerBy产品团队
- 问题反馈: [GitHub Issues](https://github.com/your-org/powerby-skills/issues)
- 讨论交流: [GitHub Discussions](https://github.com/your-org/powerby-skills/discussions)

---

**PowerBy Skills Framework** - 让软件开发更标准、更高效、更高质量 🚀
