# Function Points: 还原式项目评审框架

## 总览

| FP | REQ | 功能名称 | 优先级 | 一句话描述 |
|----|-----|---------|--------|-----------|
| FP-001 | REQ-001 | 统一 Skill 协议 | 必须 | 定义所有 Skill 的输入输出格式和执行规范 |
| FP-002 | REQ-002 | 证据驱动数据模型 | 必须 | 设计 Evidence Unit、Object Record 等核心数据结构 |
| FP-003 | REQ-003 | 证据优先级与冲突决议 | 必须 | 识别证据冲突并按优先级规则决议，显式保留差异 |
| FP-004 | REQ-004 | 产品事实还原 | 必须 | 从产品文档提取 Goal、Role、Scenario 对象 |
| FP-005 | REQ-005 | 功能事实还原 | 必须 | 从多种来源提取 Feature、Rule、Boundary 对象 |
| FP-006 | REQ-006 | 关系构建 | 必须 | 建立 Goal-Feature 跨层追踪关系 |
| FP-007 | REQ-007 | 差异与缺口识别 | 必须 | 识别需求-实现偏差、对象缺失、链路断点 |
| FP-008 | REQ-008 | 项目接入与范围定义 | 必须 | 接入项目资料，定义评审范围，生成资料清单 |
| FP-009 | REQ-009 | 证据采集与标准化 | 必须 | 采集项目内证据，标准化为 Evidence Unit 格式 |
| FP-010 | REQ-010 | 报告编排与导出 | 必须 | 生成人类可读的 Markdown 评审报告 |
| FP-011 | REQ-011 | 架构事实还原 | 应该 | 从代码结构提取模块、实体、依赖关系（V2） |
| FP-012 | REQ-012 | 实现事实还原 | 应该 | 识别代码单元和入口点（V2） |
| FP-013 | REQ-013 | 验证事实还原 | 应该 | 识别测试和可观测性证据（V2） |

---

## 详情

### 必须（核心）

#### FP-001 → REQ-001: 统一 Skill 协议
- **优先级**：必须
- **描述**：定义所有 Skill 遵循的统一接口规范，包括输入（ReviewContext + parameters）、输出（status/objects/relations/conflicts/gaps/metadata/errors）、evidence_policy 约束和执行状态定义
- **验收标准**：所有 Skill 可独立运行，输入输出格式符合协议

#### FP-002 → REQ-002: 证据驱动数据模型
- **优先级**：必须
- **描述**：设计 Evidence Unit、Object Record、Project Metadata、Feature State、Relationship Record、Conflict Record、Gap Record、Review Context 等核心数据结构
- **验收标准**：所有对象都有证据来源字段（evidence_refs），可追溯

#### FP-003 → REQ-003: 证据优先级与冲突决议
- **优先级**：必须
- **描述**：对证据按优先级排序（新文档 > 旧文档，代码 > 旧文档），识别文档-代码冲突，显式保留差异不自动和解
- **验收标准**：能识别新旧文档冲突、文档与代码冲突，冲突被显式保留

#### FP-004 → REQ-004: 产品事实还原
- **优先级**：必须
- **描述**：从 PRD/README/Wiki 提取 Goal、Role、Scenario、Constraint、Non-goal 对象，每个对象标注证据来源和置信度
- **验收标准**：输出 Goal/Role/Scenario Catalog，无文档时返回 partial + 空 Catalog

#### FP-005 → REQ-005: 功能事实还原
- **优先级**：必须
- **描述**：从产品文档、API、代码、测试提取 Feature、Rule、Boundary 对象，标注功能状态（doc_defined/implemented/partial/residual）
- **验收标准**：输出 Feature/Rule/Boundary Catalog，每个对象标注证据来源

#### FP-006 → REQ-006: 关系构建
- **优先级**：必须
- **描述**：建立 Goal → Feature（supports）、Rule → Feature（constrains）追踪关系，识别孤立对象，输出追踪矩阵和覆盖率
- **验收标准**：输出 Traceability Matrix，关系有证据支撑

#### FP-007 → REQ-007: 差异与缺口识别
- **优先级**：必须
- **描述**：识别需求-实现差异（文档有代码无、代码有文档无）、对象缺失（Goal 无 Feature 支撑）、链路断点
- **验收标准**：输出 Difference List、Gap List、Conflict List

#### FP-008 → REQ-008: 项目接入与范围定义
- **优先级**：必须
- **描述**：接入项目代码仓库和文档目录，定义评审范围，生成资料清单，标记缺失项
- **验收标准**：生成 project_metadata 和 resource_inventory

#### FP-009 → REQ-009: 证据采集与标准化
- **优先级**：必须
- **描述**：采集文档、代码、测试、配置、Git 历史，标准化为 Evidence Unit 格式
- **验收标准**：所有证据被标准化，包含来源、时间、作者等元信息

#### FP-010 → REQ-010: 报告编排与导出
- **优先级**：必须
- **描述**：将所有还原结果编排为包含项目概览、对象清单、追踪矩阵、差异清单、证据索引的 Markdown 报告
- **验收标准**：生成人类可读报告，所有结论有证据索引

---

### 应该（V2 扩展）

#### FP-011 → REQ-011: 架构事实还原
- **优先级**：应该（V2）
- **描述**：从代码结构、配置、部署文件提取模块、实体、依赖关系
- **验收标准**：输出 Module/Entity Catalog 和 Dependency Graph

#### FP-012 → REQ-012: 实现事实还原
- **优先级**：应该（V2）
- **描述**：识别代码单元、入口点、运行形态、外部集成
- **验收标准**：输出 Code Unit/Entry Point Catalog

#### FP-013 → REQ-013: 验证事实还原
- **优先级**：应该（V2）
- **描述**：识别测试对象、监控、日志、告警等验证性证据
- **验收标准**：输出 Test/Observability Catalog

---

## 1:1 对应校验

| Proposal REQ | Function Point | 状态 |
|-------------|----------------|------|
| REQ-001 | FP-001 | ✅ |
| REQ-002 | FP-002 | ✅ |
| REQ-003 | FP-003 | ✅ |
| REQ-004 | FP-004 | ✅ |
| REQ-005 | FP-005 | ✅ |
| REQ-006 | FP-006 | ✅ |
| REQ-007 | FP-007 | ✅ |
| REQ-008 | FP-008 | ✅ |
| REQ-009 | FP-009 | ✅ |
| REQ-010 | FP-010 | ✅ |
| REQ-011 | FP-011 | ✅ |
| REQ-012 | FP-012 | ✅ |
| REQ-013 | FP-013 | ✅ |

**校验结果**：proposal.md 中 13 个 REQ 与 function-points.md 中 13 个 FP 完全 1:1 对应，无遗漏无溢出。
