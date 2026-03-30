# pb-review 流程优化实施清单

> 版本：v1.0
> 制定日期：2026-03-27
> 关联文档：[pb-review-improvement-proposal.md](./pb-review-improvement-proposal.md)

---

## 快速导航

- **问题诊断**：[第一部分](#第一部分问题诊断)
- **优化方案**：[第二部分](#第二部分优化方案)
- **实施计划**：[第三部分](#第三部分实施计划)
- **验收标准**：[第四部分](#第四部分验收标准)

---

## 核心发现

基于 archer 项目评审交付物分析，发现 **pb-review 流程的核心缺陷**：

### ❌ 缺陷 1：功能规格卡缺少依赖关系
- **现状**：只描述"需要什么数据"，不说明"由哪个功能提供"
- **影响**：无法生成依赖图，无法理解功能执行顺序
- **示例**：`OPR-AS-SLCT-001` 依赖 `OPR-AS-BRKO-001`，但规格卡中看不出来

### ❌ 缺陷 2：缺少分层架构文档
- **现状**：21 个功能点是平铺列表，看不出层级关系
- **影响**：无法理解系统整体架构，无法判断依赖是否违反分层规则
- **示例**：虽然提到"L1-L4 分层"，但交付物中没有体现

### ❌ 缺陷 3：缺少模块依赖关系矩阵
- **现状**：只有 Goal→Feature 关系，没有 Feature→Feature 关系
- **影响**：看不出完整的更新链路，无法评估变更影响范围
- **示例**：看不出 A 股域链路：`SYNC → KDAY → FKLN → TRND → BRKO`

### ❌ 缺陷 4：缺少数据流图
- **现状**：没有数据流向文档
- **影响**：无法理解数据生命周期，无法优化数据管道
- **示例**：看不出 `StockInfo → KLine → TrendResult → BreakoutResult` 的数据流

---

## 优化方案总览

### 方案：3+2+1

- **3 个新增交付物**：
  - DLV-008: `architecture-layered.md` (分层架构文档)
  - DLV-009: `dependency-matrix.md` (模块依赖关系矩阵)
  - DLV-010: `data-flow.md` (数据流图)

- **2 个增强维度**：
  - D-09: 依赖关系（上游依赖、下游被依赖、依赖类型）
  - D-10: 实现映射（服务类、Repository、模型、测试文件）

- **1 个流程调整**：
  - 在 `relation-builder` 后增加 `architecture-builder` 和 `data-flow-builder` 步骤

---

## 实施阶段

### Phase 1: 标准更新 (2h, P0)

**任务**：更新 `feature-specification-standard.md`

**变更内容**：
```markdown
### 1.2 扩展维度 (按需填写)

| 维度 ID | 维度名称 | 定义 | 量化标准 | 验证方式 |
|---------|----------|------|----------|----------|
| D-09 | 依赖关系 | 上游依赖、下游被依赖、依赖类型 | 依赖功能ID列表 | 依赖图拓扑排序 |
| D-10 | 实现映射 | 服务类、Repository、模型、测试 | 代码路径列表 | 代码路径存在性检查 |
```

**验收**：
- [ ] `feature-specification-standard.md` 包含 D-09、D-10 定义
- [ ] 提供 D-09、D-10 的填写示例

### Phase 2: 功能规格卡增强 (4h, P0)

**任务**：增强 `pb-review-feature-reconstructor`

**变更内容**：
1. 在生成功能规格卡时，增加 D-09 依赖关系维度
2. 在生成功能规格卡时，增加 D-10 实现映射维度
3. 通过代码分析推断依赖关系和实现映射

**实现策略**：
```python
# D-09 依赖关系推断
def infer_dependencies(function_id, feature_registry):
    upstream = []
    # 1. 从前置条件推断数据依赖
    # 2. 从代码调用图推断编排依赖
    # 3. 从触发器配置推断触发依赖
    return upstream

# D-10 实现映射推断
def infer_implementation(function_id, codebase):
    mapping = {}
    # 1. 从入口点找到命令/API路径
    # 2. 从命令/API找到核心服务类
    # 3. 从服务类找到依赖的Repository
    # 4. 从Repository找到核心模型
    # 5. 从测试目录找到测试文件
    return mapping
```

**验收**：
- [ ] 所有功能规格卡包含 D-09 维度
- [ ] 所有功能规格卡包含 D-10 维度
- [ ] D-09 中的依赖可追溯到具体 Function ID
- [ ] D-10 中的代码路径在代码库中存在

### Phase 3: 关系构建增强 (4h, P0)

**任务**：增强 `pb-review-relation-builder`

**变更内容**：
1. 构建 Feature→Feature 依赖关系
2. 构建 Feature→Service 映射关系
3. 构建 Feature→Model 映射关系
4. 更新 `05-traceability-matrix.md`，增加新的关系表

**实现策略**：
```python
# Feature→Feature 依赖矩阵
def build_feature_dependency_matrix(feature_registry):
    matrix = []
    for feature in feature_registry:
        upstream = feature.get('D-09', {}).get('upstream', [])
        downstream = feature.get('D-09', {}).get('downstream', [])
        matrix.append({
            'function_id': feature['function_id'],
            'upstream': upstream,
            'downstream': downstream,
            'dependency_type': feature.get('D-09', {}).get('type', 'unknown')
        })
    return matrix
```

**验收**：
- [ ] `05-traceability-matrix.md` 包含 Feature→Feature 依赖矩阵
- [ ] `05-traceability-matrix.md` 包含 Feature→Service 映射矩阵
- [ ] `05-traceability-matrix.md` 包含 Feature→Model 映射矩阵

### Phase 4: 架构文档生成 (6h, P1)

**任务**：新增 `pb-review-architecture-builder` skill

**输入**：
- `feature_spec_registry`
- `dependency_matrix`

**输出**：
- `DLV-008: architecture-layered.md`

**核心逻辑**：
```python
def build_architecture_document(feature_registry, dependency_matrix):
    # 1. 提取所有功能的 Layer 字段，分组为 L1-L4
    layers = group_by_layer(feature_registry)

    # 2. 提取所有功能的 Domain 字段，分组为业务域
    domains = group_by_domain(feature_registry)

    # 3. 为每一层生成功能映射表
    layer_mapping = generate_layer_mapping(layers, dependency_matrix)

    # 4. 生成依赖规则说明
    dependency_rules = generate_dependency_rules(layers, domains)

    # 5. 渲染 Markdown 文档
    return render_architecture_document(layers, domains, layer_mapping, dependency_rules)
```

**验收**：
- [ ] 生成 `architecture-layered.md`
- [ ] 包含 L1-L4 分层架构图
- [ ] 包含业务域划分说明
- [ ] 包含 L4 操作层功能映射表
- [ ] 包含 L3 业务层服务映射表
- [ ] 包含依赖规则说明

### Phase 5: 数据流图生成 (6h, P1)

**任务**：新增 `pb-review-data-flow-builder` skill

**输入**：
- `feature_spec_registry`
- `model_registry`

**输出**：
- `DLV-010: data-flow.md`

**核心逻辑**：
```python
def build_data_flow_document(feature_registry, model_registry):
    # 1. 从功能规格卡的 D-08 副作用维度提取数据写入
    data_producers = extract_data_producers(feature_registry)

    # 2. 从功能规格卡的 D-03 前置条件维度提取数据读取
    data_consumers = extract_data_consumers(feature_registry)

    # 3. 从模型定义提取数据对象和关系
    data_objects = extract_data_objects(model_registry)

    # 4. 构建数据流向图
    data_flow_graph = build_data_flow_graph(data_producers, data_consumers, data_objects)

    # 5. 生成 Mermaid 图表
    mermaid_diagram = generate_mermaid_diagram(data_flow_graph)

    # 6. 渲染 Markdown 文档
    return render_data_flow_document(data_flow_graph, mermaid_diagram)
```

**验收**：
- [ ] 生成 `data-flow.md`
- [ ] 包含数据流向 Mermaid 图
- [ ] 包含数据流向表
- [ ] 包含数据转换链路表

### Phase 6: 流程集成 (2h, P1)

**任务**：更新 `pb-review` 主流程

**变更内容**：
```python
# 原流程
workflow = [
    'project-scope',
    'evidence-collector',
    'conflict-resolver',
    'product-reconstructor',
    'feature-reconstructor',
    'relation-builder',
    'gap-analyzer',
    'report-composer'
]

# 新流程
workflow = [
    'project-scope',
    'evidence-collector',
    'conflict-resolver',
    'product-reconstructor',
    'feature-reconstructor',
    'relation-builder',          # 增强：构建 Feature→Feature 关系
    'architecture-builder',      # 新增：生成分层架构文档
    'data-flow-builder',         # 新增：生成数据流图
    'gap-analyzer',
    'report-composer'
]
```

**验收**：
- [ ] `pb-review` skill 集成新的 workflow
- [ ] 新增 skill 的输出正确写入 `deliverable_manifest`
- [ ] checkpoint 正确记录新增步骤的完成状态

### Phase 7: 回归验证 (4h, P1)

**任务**：在 archer 项目上验证优化效果

**验证步骤**：
1. 在 archer 项目上重新运行优化后的 pb-review 流程
2. 检查交付物数量：从 7 个增加到 10 个
3. 检查功能规格卡维度：从 8 个增加到 10 个
4. 检查追踪矩阵维度：从 2 个增加到 5 个
5. 检查架构文档：新增 3 个架构文档
6. 检查可用性：新人可通过交付物理解系统架构

**验收**：
- [ ] 交付物数量 = 10
- [ ] 功能规格卡维度 = 10
- [ ] 追踪矩阵维度 = 5
- [ ] 架构文档数量 = 3
- [ ] 架构完整性评分 ≥ 85%

---

## 验收标准

### 标准 1：功能规格卡完整性

- [ ] 所有功能规格卡都包含 D-09 依赖关系维度
- [ ] 所有功能规格卡都包含 D-10 实现映射维度
- [ ] D-09 中的上游依赖可追溯到具体的 Function ID
- [ ] D-10 中的服务类路径可在代码库中找到

### 标准 2：架构文档完整性

- [ ] 生成 `architecture-layered.md`，包含 L1-L4 分层架构图
- [ ] 生成 `dependency-matrix.md`，包含 Feature→Feature 依赖矩阵
- [ ] 生成 `data-flow.md`，包含数据流向图
- [ ] 所有 Mermaid 图表可正常渲染

### 标准 3：可追溯性

- [ ] 从 Goal 可追溯到 Feature
- [ ] 从 Feature 可追溯到上游依赖的 Feature
- [ ] 从 Feature 可追溯到实现的服务类
- [ ] 从 Feature 可追溯到数据模型

### 标准 4：架构完整性提升

- [ ] 新人可通过架构文档理解系统分层
- [ ] 新人可通过依赖矩阵理解功能执行顺序
- [ ] 新人可通过数据流图理解数据生命周期
- [ ] 架构完整性评分从 40% 提升至 85%

---

## 预期收益

### 定量收益

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 交付物数量 | 7 个 | 10 个 | +43% |
| 功能规格卡维度 | 8 个 | 10 个 | +25% |
| 追踪矩阵维度 | 2 个 | 5 个 | +150% |
| 架构文档覆盖率 | 0% | 100% | +100% |
| 架构完整性评分 | 40% | 85% | +112% |

### 定性收益

| 收益维度 | 描述 |
|----------|------|
| **新人 Onboarding** | 减少 50% 的代码阅读时间 |
| **变更影响分析** | 减少 70% 的影响分析时间 |
| **架构决策** | 避免架构腐化 |
| **数据治理** | 支持数据管道优化 |
| **测试设计** | 提升测试覆盖率 |

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| **代码分析复杂度** | D-10 实现映射可能不准确 | 采用启发式规则 + 人工校验 |
| **依赖关系推断** | D-09 依赖关系可能遗漏隐式依赖 | 结合代码调用图 + 数据流分析 |
| **维护成本** | 新增 3 个交付物，增加维护成本 | 自动化生成 + 增量更新 |
| **学习曲线** | 新增维度增加学习成本 | 提供示例和最佳实践 |

---

## 下一步行动

### 立即行动 (P0)

1. [ ] 提交 Phase 1 实施计划
2. [ ] 更新 `feature-specification-standard.md`
3. [ ] 增强 `pb-review-feature-reconstructor`
4. [ ] 增强 `pb-review-relation-builder`

### 后续行动 (P1)

5. [ ] 新增 `pb-review-architecture-builder` skill
6. [ ] 新增 `pb-review-data-flow-builder` skill
7. [ ] 更新 `pb-review` 主流程
8. [ ] 在 archer 项目上验证优化效果

---

## 参考文档

- [pb-review 流程优化方案](./pb-review-improvement-proposal.md)
- [功能规格定义标准](./feature-specification-standard.md)
- [pb-review 交付物标准](./pb-review-deliverable-standard.md)
- [pb-review skill 定义](../../skills/pb-review/skill.md)

---

**文档状态**: ✅ 已完成
**总工作量**: 28 小时（约 3.5 个工作日）
**优先级**: P0 (Phase 1-3), P1 (Phase 4-7)
