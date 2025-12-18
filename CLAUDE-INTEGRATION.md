# PowerBy Skills - Claude Code 集成指南

## 🎯 概述

PowerBy Skills是一套完整的AI产品开发流程技能包，覆盖从需求定义（P0）到代码审查（P8）的完整生命周期。

## 📦 技能包结构

### 1. powerby-core - 核心流程技能
- **powerby-product**：产品经理技能（P0-P2阶段）
- **powerby-architect**：系统架构师技能（P3-P4阶段）
- **powerby-engineer**：软件工程师技能（P5-P6阶段）
- **powerby-code-review**：代码审查员技能（P7-P8阶段）

### 2. powerby-atomic - 原子化专精技能
- **requirement-alignment**：需求对齐专家
- **mvp-prioritization**：MVP优先级评估专家
- **function-point-checker**：功能点清单生成器
- **solution-evaluation**：方案评估专家
- **mermaid-architecture**：架构可视化专家
- **test-spec-design**：测试规格设计专家

## 🚀 安装步骤

### 通过Claude Code CLI注册（推荐）

1. **打开Claude Code终端**
2. **安装技能包**
   ```bash
   /plugin install powerby-core@git+https://github.com/your-org/powerby-skills
   /plugin install powerby-atomic@git+https://github.com/your-org/powerby-skills
   ```

## 💡 使用示例

### 场景1：新产品需求定义（P0-P1）

**在Claude Code中输入：**
```
请使用powerby-product技能帮助我定义一个电商产品的需求。
```

### 场景2：技术架构设计（P3-P4）

**在Claude Code中输入：**
```
请使用powerby-architect技能为电商推荐系统设计技术架构。
```

## 🎭 技能角色切换

PowerBy Skills支持在同一对话中根据需要切换不同角色：

```
# 启动产品经理模式
Use powerby-product skill

# 切换到架构师模式
Use powerby-architect skill

# 切换到工程师模式
Use powerby-engineer skill

# 切换到审查员模式
Use powerby-code-review skill
```

## 📚 核心原则

1. **零假设原则** - 绝不猜测用户的模糊意图
2. **MVP优先原则** - 识别核心价值，定义最小功能集
3. **Mixin思维** - 增量补充，组合优于完整
4. **逻辑闭环** - 每个决策点都有清晰的逻辑阐述

---

**更多详细信息请查看 [README.md](README.md)**
