# P0+P1 流程合并优化方案

## 当前流程分析

### 现有流程
```
P0: /powerby.initialize
  → 创建项目结构
  → 生成宪章文档（固定模板）
  → 创建项目元数据文件

P1: /powerby.define
  → 需求定义+澄清
  → 生成PRD和功能点清单
```

### 问题分析
1. **用户需要执行2次命令**：增加了使用复杂度
2. **P0初始化本质简单**：只是创建文件，宪章是固定模板
3. **流程跳跃风险**：用户可能跳过P0直接进入P1
4. **重复操作**：创建文件是机械性操作

---

## 优化方案设计

### 标准流程优化

**合并后流程**：
```
P0+P1: /powerby.define
  → 步骤1: 检查初始化文件是否存在
  → 步骤2: 如果不存在，自动创建必要文件
  → 步骤3: 进行需求定义+澄清
  → 输出: PRD、功能点清单、澄清记录
```

### 快速流程优化

**合并后流程**：
```
P0-P5: /powerby.quick
  → 步骤1: 检查初始化文件是否存在
  → 步骤2: 如果不存在，自动创建必要文件
  → 步骤3: 执行快速流程（P0-P5）
  → 输出: 快速流程文档集合
```

**快速流程特点**：
- 总时间 ≤ 5小时（P0-P5）
- 适用于 ≤ 3天的开发需求
- 基于现有架构的增量开发
- P1阶段融合需求定义与澄清

---

## 自动初始化实现

### 通用检查逻辑

所有涉及P0阶段的命令都应该包含自动初始化：

```yaml
# 通用自动初始化检查
自动初始化检查：
1. 检查 .powerby/project.json 是否存在
2. 检查 docs/constitution.md 是否存在
3. 如果不存在，从 templates/ 目录复制并创建：
   - .powerby/project.json
   - .powerby/iterations.json
   - docs/constitution.md (使用模板替换变量)
```

### 适用命令范围

**需要自动初始化的命令**：
- ✅ `/powerby.define` - 标准流程P1
- ✅ `/powerby.quick` - 快速流程P0-P5
- ⚠️ `/powerby.research` - 如果用户跳过define直接使用
- ⚠️ `/powerby.design` - 如果用户跳过define直接使用

**可选初始化的命令**：
- `/powerby.initialize` - 保留但标记为deprecated
- `/powerby.plan` - 通常在有PRD后使用
- `/powerby.implement` - 通常在有架构后使用
- `/powerby.review` - 通常在实现后使用

---

## 推荐方案

### 实施步骤

#### 1. 修改powerby-define.md
在handoffs prompt中增加自动初始化逻辑：

```yaml
handoffs:
  - label: Define+Clarify Requirements
    agent: powerby-product
    prompt: |
      首先执行自动初始化检查：
      1. 检查 .powerby/project.json 是否存在
      2. 检查 docs/constitution.md 是否存在
      3. 如果不存在，从 templates/ 目录复制并创建必要文件

      然后进行需求定义+澄清：
      [原有需求定义内容...]
```

#### 2. 修改powerby-quick.md
在handoffs中增加自动初始化逻辑：

```yaml
handoffs:
  - label: Quick Init
    agent: powerby-fullstack
    prompt: |
      首先执行自动初始化检查：
      1. 检查 .powerby/project.json 是否存在
      2. 检查 docs/constitution.md 是否存在
      3. 如果不存在，从 templates/ 目录复制并创建必要文件

      然后进行快速初始化：
      [原有快速初始化内容...]

  - label: Quick Define+Clarify
    agent: powerby-fullstack
    prompt: P1: 需求定稿制 - 融合需求定义与澄清...
```

#### 3. 更新命令描述
在Outline中说明自动初始化：

```markdown
## Outline

使用 `/powerby.define` 命令进行需求定义+澄清（P1阶段）。
**自动初始化**：如果项目未初始化，将自动创建必要文件。

使用 `/powerby.quick` 命令进行快速需求处理（P0-P5）。
**自动初始化**：如果项目未初始化，将自动创建必要文件。
```

#### 4. 更新文档
- 修改README.md中的使用示例
- 更新INSTALL.md中的流程说明
- 标记initialize为deprecated
- 更新快速流程文档

---

## 用户体验对比

### 当前体验 - 标准流程
```bash
# 用户需要记住2步流程
/powerby.initialize 我的项目 "项目描述"
/powerby.define "我想构建一个任务管理系统"
```

### 当前体验 - 快速流程
```bash
# 快速流程也需要先初始化
/powerby.initialize 我的项目 "项目描述"
/powerby.quick 为购物车添加优惠券功能，预计2天
```

### 优化后体验 - 标准流程
```bash
# 用户只需1步，自动处理初始化
/powerby.define "我想构建一个任务管理系统"
```

### 优化后体验 - 快速流程
```bash
# 用户只需1步，自动处理初始化
/powerby.quick 为购物车添加优惠券功能，预计2天
```

---

## 错误处理策略

### 场景1：用户已有项目结构
```
✅ 检测到项目已初始化
✅ 继续执行命令流程
```

### 场景2：用户没有项目结构
```
✅ 自动创建项目结构
✅ 自动生成宪章文档
✅ 继续执行命令流程
```

### 场景3：部分文件存在
```
✅ 检测到部分文件缺失
✅ 补充创建缺失文件
✅ 继续执行命令流程
```

### 场景4：初始化失败
```
❌ 自动初始化失败
💡 提示用户：
   - 检查目录权限
   - 或手动运行 /powerby.initialize
   - 然后重新执行命令
```

---

## 迁移策略

### 向后兼容
- 保留 `/powerby.initialize` 命令（标记为deprecated）
- 现有用户可以继续使用，但建议迁移到新流程
- 新用户直接使用 `/powerby.define`

### 文档更新
- 更新README.md使用示例
- 更新INSTALL.md安装指南
- 更新命令参考文档

---

## 优势总结

### 用户体验
- ✅ 减少命令数量（标准流程2→1，快速流程2→1）
- ✅ 降低学习成本（只需记住1个入口命令）
- ✅ 减少操作错误（自动处理初始化，无遗漏风险）
- ✅ 流程更自然（从需求直接开始）

### 系统设计
- ✅ 符合MVP精简理念
- ✅ 减少状态管理复杂度
- ✅ 自动化程度更高
- ✅ 统一初始化逻辑
- ✅ 错误处理更智能

### 快速流程优势
- ✅ 真正实现"快速"（1步完成）
- ✅ 降低小需求使用门槛
- ✅ 鼓励使用快速流程处理小需求
- ✅ 与标准流程保持一致

---

## 实施优先级

### 高优先级（立即实施）
1. ✅ 修改powerby-define.md - 增加自动初始化
2. ✅ 修改powerby-quick.md - 增加自动初始化
3. ✅ 更新命令描述文档

### 中优先级（后续实施）
1. ✅ 更新README.md使用示例
2. ✅ 更新INSTALL.md流程说明
3. ✅ 标记initialize为deprecated

### 低优先级（长期优化）
1. ⚠️ 考虑完全移除initialize
2. ⚠️ 扩展自动初始化到其他命令
3. ⚠️ 添加初始化状态检查工具

---

## 待确认问题

1. **是否完全移除initialize？**
   - 推荐：保留但标记为deprecated，3个月后移除

2. **初始化文件检查范围？**
   - 推荐：仅检查关键文件（project.json, constitution.md）

3. **是否需要提示用户？**
   - 推荐：静默创建，用户无感知
   - 失败时提示用户手动处理

4. **快速流程是否需要特殊处理？**
   - 推荐：与标准流程保持一致，统一自动初始化逻辑

---

**方案版本**: v2.0
**创建日期**: 2025-12-19
**适用场景**: PowerBy MVP精简流程 + 快速流程
