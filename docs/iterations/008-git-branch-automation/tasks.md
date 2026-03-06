# 开发任务计划

**迭代编号**: 008
**分支**: `feature/008-git-branch-automation`
**创建日期**: 2026-03-06
**生命周期阶段**: P5 - 开发规划

---

## 1. 需求与架构对齐报告

### 核心目标复述
- 自动化 PowerBy 迭代分支生命周期，覆盖创建、状态追踪、合规检查、合并与清理。
- 保持与现有 `powerby-git` CLI 和 `powerby-github-branch` 兼容，不重写底层 Git 能力。
- 所有破坏性操作继续采用显式调用与 Fail-Fast 报错，禁止静默回退。

### 范围边界
- **本次实现（P0）**: REQ-001 ~ REQ-005。
- **后续实现（P1）**: REQ-006 ~ REQ-008。
- **明确不做**: 自动解决冲突、远程分支托管、非 GitFlow 工作流支持。

### 成功标准
- [x] 可编程方式创建 `feature/{id}-{name}` 分支并写入 `.powerby/iterations.json`
- [x] 可检查当前分支与工作区是否符合 P1/P6/P8 生命周期约束
- [x] 可将迭代分支按 `--no-ff` 合并到 `develop`
- [x] 可在已合并前提下删除本地 feature 分支
- [x] 关键失败路径均有自动化测试约束

## 1.3 现有代码分析报告

### 现有组件清单

| 组件名称 | 路径 | 职责 | 复用可能性 | 备注 |
|---------|------|------|-----------|------|
| `powerby-git` CLI | `skills/powerby-git/src/index.js` | CLI 入口与命令注册 | 高 | 保持命令面不变 |
| Git 工具层 | `skills/powerby-git/src/utils/git.js` | Git 状态、分支与提交查询 | 高 | 适合增量扩展 merge / clean / source branch 能力 |
| 分支命名验证器 | `skills/powerby-git/src/core/branch-validator.js` | 分支格式规范 | 高 | 可直接复用 feature 命名规范 |
| 分支创建命令 | `skills/powerby-git/src/commands/start.js` | 手动创建分支 | 中 | 适合作为行为参考，不直接承载 ASP 生命周期逻辑 |
| Shell 脚本集合 | `scripts/create-iteration-branch.sh` 等 | 一次性 Git 操作脚本 | 中 | 可作为交互参考，但不适合作为可测试核心实现 |

### 编码规范总结
- **代码风格**: Node.js CommonJS + Jest 单元测试
- **命名规范**: `camelCase` 函数，`UPPER_SNAKE_CASE` 常量
- **测试模式**: `skills/powerby-git/tests/unit/*.test.js`
- **注释规范**: JSDoc，公共函数需显式说明参数、返回值、异常语义

### 复用建议
- **可直接复用**: `branch-validator.js`、`errors.js`
- **可扩展复用**: `utils/git.js` 增加 `createBranchFromSource()` / `mergeBranch()` / `isWorkingTreeClean()`
- **需全新开发**: `iteration-tracker.js`、`branch-compliance.js`、`integrations/asp.js`

### 一致性建议
- **风格参考**: `skills/powerby-git/src/commands/start.js`
- **架构模式**: 在 `powerby-git` 内部做基础设施扩展，避免散落到 shell 脚本
- **注意事项**: 当前仓库仍存在历史未跟踪文件，P8 合并检查必须依赖工作区洁净度校验

## 1.5 文档风格定义

- **文档标准**: JavaScript 采用 JSDoc
- **接口模板**: `@param` / `@returns` / `@throws` / 业务意图描述必须完整
- **维护规范**: 复杂状态转换通过函数名和异常上下文表达，不引入“解释代码行为”的废话注释
- **验证方式**: 通过 Jest 覆盖正常路径与失败路径，结合代码审阅检查 JSDoc 完整性

## 2. 技术方案评估

### 方案 A：扩展 `powerby-git` 基础设施层
- **简介**: 在 `skills/powerby-git` 内新增 ASP 集成模块，并扩展 Git Utils 与迭代追踪能力。
- **架构遵循性**: 与 `architecture.md` 的 ADR-001 完全一致。
- **哲学对齐分析**:
  - **SOLID**: Git 原子操作、元数据追踪、合规检查各自独立。
  - **KISS**: 复用现有 CLI 与 Git 工具层，不额外发明执行入口。
  - **DRY**: 不重复实现 branch naming、Git status、错误码体系。
  - **最小影响面**: 仅改动 `skills/powerby-git` 作用域。
  - **最小惊讶原则**: 所有新能力都围绕既有 `powerby-git` 目录演进。
- **优点**: 可测试、可复用、与现有文档最一致。
- **缺点**: 需要补足部分底层 Git API。

### 方案 B：继续堆叠 shell 脚本
- **简介**: 在 `scripts/` 下继续增加 create/check/merge/delete 脚本。
- **架构遵循性**: 偏离 `architecture.md` 中的组件化设计。
- **哲学对齐分析**:
  - **SOLID**: 状态追踪、分支操作、错误处理会耦合在脚本内。
  - **KISS**: 短期简单，长期难以复测与复用。
  - **DRY**: 会重复已有 `powerby-git` 逻辑。
  - **最小影响面**: 表面影响小，但维护成本高。
  - **最小惊讶原则**: 用户很难判断 CLI 与 shell 脚本的职责边界。
- **优点**: 上手快。
- **缺点**: 不利于 TDD 与后续 P1 扩展。

### 我的建议
- **推荐方案**: 方案 A
- **核心理由**: 它最符合现有架构 ADR、最容易做失败路径测试，也能把 008 的功能沉淀为可复用基础设施，而不是一次性脚本。

## 3. 开发任务清单

### P0 核心功能（Must Have）

#### TASK-008-001: 扩展 Git Utils 支撑生命周期操作
- **关联需求**: REQ-001 / REQ-003 / REQ-005
- **关联架构**: 组件 6 `Git Utils`
- **任务描述**: 在 `skills/powerby-git/src/utils/git.js` 新增按源分支创建、无快进合并、工作区洁净度检查、提交历史查询能力。
- **验收标准**:
  - [x] 可从 `develop` 创建新分支并自动切换
  - [x] 可用 `--no-ff` 合并 feature 分支
  - [x] 可返回工作区是否干净
  - [x] **异常路径验证**: 源分支缺失时立即抛错
  - [x] **文档化标准合规**
- **边界检查**:
  - 输入边界: `branchName` / `sourceBranch` 不能为空
  - 资源状态: Git 仓库必须存在目标分支
- **预估工时**: 1 小时
- **依赖关系**: 无
- **测试策略**: 由 ASP 集成测试间接覆盖
- **文档要求**: 为全部公共方法补齐 JSDoc
- **状态**: 已完成

#### TASK-008-002: 实现迭代元数据追踪器
- **关联需求**: REQ-002
- **关联架构**: 组件 5 `Iteration Tracker`
- **任务描述**: 新增 `iteration-tracker.js`，负责读取、创建、更新 `.powerby/iterations.json` 中的 `branch_info` 字段。
- **验收标准**:
  - [x] 缺失迭代记录时可自动创建基础记录
  - [x] 状态变更可回写 `branch_info`
  - [x] 文档索引可基于标准迭代目录自动补齐
  - [x] **异常路径验证**: 名称不一致时立即抛错
  - [x] **文档化标准合规**
- **边界检查**:
  - 输入边界: `iterationId` 必须是三位数字
  - 资源状态: `.powerby/iterations.json` 必须可读写
- **预估工时**: 1.5 小时
- **依赖关系**: TASK-008-001
- **测试策略**: 单元测试
- **文档要求**: 公开函数完整 JSDoc
- **状态**: 已完成

#### TASK-008-003: 实现分支合规检查器
- **关联需求**: REQ-005
- **关联架构**: 组件 2 `Branch Compliance Checker`
- **任务描述**: 新增 `branch-compliance.js`，在 P1/P6/P8 阶段检查当前分支与工作区状态。
- **验收标准**:
  - [x] 可返回 `compliant/currentBranch/expectedBranch/warnings`
  - [x] P8 脏工作区会返回 error 级别警告
  - [x] **异常路径验证**: 缺失 phase 时立即抛错
  - [x] **文档化标准合规**
- **边界检查**:
  - 输入边界: `phase` 不能为空
  - 资源状态: 迭代记录必须存在
- **预估工时**: 1 小时
- **依赖关系**: TASK-008-002
- **测试策略**: 单元测试
- **文档要求**: 公开函数完整 JSDoc
- **状态**: 已完成

#### TASK-008-004: 实现 ASP 分支生命周期集成
- **关联需求**: REQ-001 / REQ-003 / REQ-004 / REQ-005
- **关联架构**: 组件 1 `ASP Integration Module`
- **任务描述**: 新增 `integrations/asp.js`，封装创建、检查、合并、删除四个生命周期接口。
- **验收标准**:
  - [x] 创建分支后写入 `branch_info.active`
  - [x] 合并成功后写入 `branch_info.merged`
  - [x] 删除成功后写入 `branch_info.deleted`
  - [x] **异常路径验证**: 工作区不干净时拒绝合并；未合并分支拒绝删除
  - [x] **文档化标准合规**
- **边界检查**:
  - 输入边界: `iterationId`、`iterationName`、`targetBranch` 不能为空
  - 资源状态: 目标分支存在、当前分支不能删除自身
- **预估工时**: 2 小时
- **依赖关系**: TASK-008-001, TASK-008-002, TASK-008-003
- **测试策略**: 单元测试
- **文档要求**: 公开函数完整 JSDoc
- **状态**: 已完成

#### TASK-008-005: 建立 P0 自动化测试规格
- **关联需求**: REQ-001 ~ REQ-005
- **关联架构**: 第 10 章测试策略
- **任务描述**: 为命名工具、元数据追踪、合规检查、ASP 集成新增单元测试，覆盖成功路径与失败路径。
- **验收标准**:
  - [x] 新增 4 组测试文件
  - [x] P0 核心接口均有失败触发测试
  - [x] **异常路径验证**: 源分支缺失、工作区不干净、名称不一致等用例可复现
  - [x] **文档化标准合规**
- **边界检查**:
  - 输入边界: 非法迭代编号、空 phase
  - 资源状态: 临时测试项目下 `.powerby/iterations.json` 存在
- **预估工时**: 1.5 小时
- **依赖关系**: TASK-008-001 ~ TASK-008-004
- **测试策略**: Jest 单元测试
- **文档要求**: 测试文件标题说明清晰
- **状态**: 已完成

### P1 重要功能（Should Have）

#### TASK-008-101: 实现分支切换提示
- **关联需求**: REQ-006
- **关联架构**: Branch Compliance Checker / ASP Integration Module
- **状态**: 已完成

#### TASK-008-102: 实现合并冲突检测器
- **关联需求**: REQ-007
- **关联架构**: Merge Conflict Detector
- **状态**: 已完成

#### TASK-008-103: 实现分支历史报告生成器
- **关联需求**: REQ-008
- **关联架构**: Branch History Generator
- **状态**: 已完成

## 4. 测试规格矩阵

| 测试点 ID | 关联需求 | 关联架构 | 任务ID | 测试策略 | 可量化成功标准 |
|----------|----------|----------|--------|---------|--------------|
| TC-008-001 | REQ-001 | ASP Integration Module | TASK-008-004 | 单元测试 | 创建后返回 `feature/008-git-branch-automation` |
| TC-008-002 | REQ-001 | Git Utils | TASK-008-001 | 单元测试 | 源分支不存在时抛出明确错误 |
| TC-008-003 | REQ-002 | Iteration Tracker | TASK-008-002 | 单元测试 | branch_info 状态可写回 JSON |
| TC-008-004 | REQ-005 | Branch Compliance Checker | TASK-008-003 | 单元测试 | P8 脏工作区返回 error 级警告 |
| TC-008-005 | REQ-003 | ASP Integration Module | TASK-008-004 | 单元测试 | 合并后 metadata 状态更新为 `merged` |
| TC-008-006 | REQ-004 | ASP Integration Module | TASK-008-004 | 单元测试 | 删除后 metadata 状态更新为 `deleted` |

## 5. Gate 5 检查

- [x] 现有代码分析已完成
- [x] 所有 P0 功能都有对应开发任务
- [x] 任务分解粒度合适
- [x] 依赖关系清晰合理
- [x] 验收标准可验证
- [x] 异常路径覆盖完整
- [x] 工作量估算合理
- [x] 技术方案决策有证据链
- [x] 函数复杂度控制规划已完成

## 6. 当前结论

- P5 已完成，采用“扩展 `powerby-git` 基础设施层”的既定方案。
- P6 已覆盖 008 当前有效范围内的全部用户故事（US-001 ~ US-008）。
- REQ-009 ~ REQ-011 在 `spec.md` 中仍标记为“推迟”，本轮不纳入完成定义。
