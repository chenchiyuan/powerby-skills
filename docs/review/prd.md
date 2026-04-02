1. 文档目标

本文档用于定义一套面向任意项目的还原式项目评审框架初版方案。

该方案的核心目标不是直接对代码或项目进行打分，而是先将项目从多个层面进行结构化还原，再基于还原结果开展后续的一致性分析、偏差识别与评审工作。

本方案强调以下原则：

- 先还原，后评审
- 先定义对象结构，再定义评分
- 从产品目标出发，逐层还原到功能、架构、实现与验证
- 建立跨层追踪关系，而不是孤立地看某一层
- 支持 AI 参与抽取和分析，但必须基于结构化对象与证据
  

---

2. 背景与问题定义

传统 code review 主要聚焦于代码实现层，典型关注点包括：

- 代码规范
- 可读性
- 潜在 bug
- 安全问题
- 可维护性
  
但在真实项目中，很多问题并不是单纯的“代码写得不好”，而是出现在更上游或跨层环节，例如：

- 产品目标不清晰
- 功能定义不完整
- 功能边界不明确
- 架构设计未能支撑真实业务需求
- 实现偏离架构设计意图
- 测试与监控无法证明功能真正成立
  
因此，单纯的代码审查无法完整反映一个项目的质量与成熟度。

本方案试图解决的问题是：

如何构建一套适用于任意项目的综合评审框架，能够从产品目标、功能定义、架构设计、实现落地、验证证据等多个层次对项目进行还原，并建立层与层之间的映射关系，从而支持后续的一致性评审。


---

3. 产品需求定义

3.1 核心需求

需要构建一套方法或系统，使 AI 或人工能够针对任意一个已有项目，先完成项目结构还原，再基于还原结果进行评审。

该能力需要覆盖以下几个层面：

1. 产品层
  - 识别项目的产品目标
  - 识别目标用户和使用场景
  - 识别功能诉求
  - 识别功能边界与非目标范围
    
2. 功能层
  - 识别完整功能列表
  - 识别子功能
  - 识别业务规则
  - 识别功能边界、流程与输入输出
    
3. 架构层
  - 识别系统、子系统、模块、服务
  - 识别领域实体和核心数据对象
  - 识别接口、依赖关系和关键流程
  - 识别架构决策和设计意图
    
4. 实现层
  - 识别代码模块、目录、文件、类、函数、接口入口
  - 识别配置、外部依赖、运行单元、部署单元
  - 识别实现对架构的还原情况
    
5. 验证层
  - 识别测试对象
  - 识别日志、埋点、监控、告警
  - 识别验证证据是否覆盖关键功能和边界
    
6. 关系层
  - 建立产品目标到功能的关系
  - 建立功能到架构模块的关系
  - 建立架构模块到实现代码的关系
  - 建立功能/边界到测试/运行证据的关系
    

---

3.2 设计初衷

本方案不是为了替代传统 code review，而是为了建立一个更高层次的评审框架。

其核心设计初衷包括：

- 不把项目看成一堆代码，而是看成一组可识别、可关联的对象
- 不直接做主观评价，而先做结构化还原
- 不只关注“代码是否好”，而关注“实现是否忠实支撑产品诉求”
- 不只看单层质量，而看跨层的一致性与还原关系
- 能适配任意项目，但允许根据项目类型扩展对象与规则
  

---

4. 方案定位

本方案的本质不是一个单纯的 code review 模板，而是一套：

还原-追踪式项目评审框架

英文工作名建议：

RTAF（Reconstruction-Traceability Assessment Framework）

中文可称：

还原-追踪式项目评审框架

框架采用三步核心思路：

1. Reconstruct（还原）
将项目中的核心对象抽取出来并结构化定义
  
2. Trace（追踪）
建立对象之间的映射关系和上下游关系
  
3. Assess（评审）
在结构和关系基础上进行一致性分析与偏差识别
  
当前初版重点放在前两步：

- 先做还原
- 先做对象结构
- 暂不重点讨论评分机制
  

---

5. 借鉴的成熟方法

本方案不是从零发明，而是借鉴多种成熟方法的优点，形成适合当前目标的组合方案。

方法
借鉴内容
在本方案中的作用
Impact Mapping
目标 → 角色 → 行为 → 功能
用于产品目标与功能映射
Story Mapping
用户旅程与功能拆分
用于功能清单组织
BDD
行为、边界、验收条件
用于功能边界与验证表达
Event Storming
事件、命令、实体、边界
用于复杂业务流程还原
C4 Model
分层表达架构
用于架构对象结构化
ADR
架构决策记录
用于还原架构意图
RTM
需求-设计-实现-测试追踪
用于关系层设计
ATAM
场景驱动架构分析
用于后续架构对齐评审
Code Review / 静态分析
实现层质量证据
用于实现对象抽取与辅助验证
测试金字塔 / 可观测性
测试与运行时证据
用于验证对象层


---

6. 初版解决方案概述

初版解决方案采用：

五层对象 + 一层关系

即：

1. 产品目标层
2. 功能定义层
3. 架构对象层
4. 实现对象层
5. 验证证据层
6. 关系层
  
其主要目标是：

- 将任意项目还原成统一结构
- 为后续对齐分析、缺口分析、偏差分析打基础
- 为 AI 的结构化理解和辅助评审提供明确输入输出协议
  

---

7. 对象结构设计

下面定义初版的核心对象结构。


---

7.1 产品目标层

该层用于回答：

这个项目为什么存在？

主要对象
- Product Goal（产品目标）
- User Role（用户角色）
- Scenario（使用场景）
- Product Constraint（产品约束）
- Non-goal（非目标）
  
主要作用
- 明确项目目标
- 明确面向对象
- 明确场景和约束
- 明确做什么、不做什么
  
示例字段

Product Goal
- id
- name
- problem_statement
- target_user
- business_value
- success_signal
- constraints
  
User Role
- id
- name
- description
- usage_context
  
Scenario
- id
- actor
- trigger
- expected_outcome
- preconditions
  

---

7.2 功能定义层

该层用于回答：

项目到底做什么？

主要对象
- Feature（功能）
- Sub-feature（子功能）
- Business Rule（业务规则）
- Feature Boundary（功能边界）
- Feature Flow（功能流程）
- Acceptance Criteria（验收条件）
  
主要作用
- 梳理完整功能清单
- 明确功能边界
- 明确业务规则
- 明确主流程与异常流程
- 为架构和验证建立基础对象
  
示例字段

Feature
- id
- name
- goal_ref
- primary_actor
- summary
- priority
  
Business Rule
- id
- feature_ref
- description
- trigger_condition
- expected_behavior
- exception_behavior
  
Feature Boundary
- id
- feature_ref
- in_scope
- out_of_scope
- preconditions
- edge_cases
- failure_modes
  

---

7.3 架构对象层

该层用于回答：

系统如何组织来支撑这些功能？

主要对象
- System / Subsystem（系统/子系统）
- Module / Service（模块/服务）
- Domain Entity（领域实体）
- API Contract（接口契约）
- Flow（数据流/控制流）
- Dependency（依赖关系）
- Technical Mechanism（技术机制）
- Architecture Decision（架构决策）
  
主要作用
- 还原架构视图
- 识别模块职责
- 识别核心实体和依赖关系
- 识别关键设计意图
  
示例字段

Module
- id
- name
- responsibility
- input
- output
- owned_entities
- dependent_modules
  
Domain Entity
- id
- name
- business_meaning
- owner_module
- lifecycle
  
Architecture Decision
- id
- title
- context
- chosen_option
- rationale
- trade_off
  

---

7.4 实现对象层

该层用于回答：

架构在代码和运行环境中是如何被实现的？

主要对象
- Code Unit（代码单元）
- Runtime Unit（运行单元）
- Entry Point（入口对象）
- Configuration（配置对象）
- Persistence Object（持久化对象）
- Integration Point（外部集成点）
- Deploy Unit（部署对象）
  
主要作用
- 识别代码实现单元
- 识别运行时结构
- 识别外部依赖和配置
- 建立架构对象到实现对象的映射
  
示例字段

Code Unit
- id
- type
- path
- name
- responsibility
- related_module
- related_feature
  
Entry Point
- id
- type
- trigger
- handler
- related_feature
  

---

7.5 验证证据层

该层用于回答：

如何证明功能和实现真正成立？

主要对象
- Test Object（测试对象）
- Acceptance Evidence（验收证据）
- Observability Object（可观测对象）
- Runtime Signal（运行信号）
- Alert Object（告警对象）
  
主要作用
- 识别测试与验收证据
- 识别日志、监控、指标、告警
- 支撑后续验证闭环分析
  
示例字段

Test Object
- id
- test_type
- target_feature
- target_module
- target_boundary
- path
  
Observability Object
- id
- type
- related_feature
- related_flow
- signal_meaning
  

---

8. 关系层设计

关系层是本方案的核心灵魂。

如果只有对象清单而没有关系，这只是一份 inventory（库存清单）；  
只有建立关系后，才构成真正的项目还原模型。

初版核心关系

关系类型
起点
终点
含义
supports
Feature
Goal
功能支撑目标
constrains
Rule
Feature
规则约束功能
maps_to
Feature
Module
功能映射到架构模块
implemented_by
Module
Code Unit
模块由代码实现
covered_by
Feature / Boundary
Test Object
功能或边界被测试覆盖
observed_by
Feature / Flow
Observability Object
功能或流程被监控/日志观察
deviates_from
Implementation / Architecture
Design Intent / Goal
表示偏差关系

关系层目标
- 建立完整的追踪链路
- 支持缺口识别
- 支持后续一致性分析
- 支持 AI 做结构化检索和推理
  

---

9. 初版最小可行对象集（V1）

为降低复杂度，第一版建议只保留最小闭环对象集。

核心对象
- Goal
- User Role
- Scenario
- Feature
- Business Rule
- Feature Boundary
- Module
- Domain Entity
- Code Unit
- Test Object
  
核心关系
- Feature supports Goal
- Rule constrains Feature
- Module supports Feature
- Code Unit implements Module
- Test Object covers Feature / Boundary
  
说明
该 V1 对象集已经足够支持：

- 从目标到功能的还原
- 从功能到架构的映射
- 从架构到实现的映射
- 从功能边界到测试的映射
  

---

10. 还原流程设计

本方案建议按固定顺序进行还原，避免直接从代码倒推全部产品定义。

步骤 1：还原产品层
输入：
- README
- PRD
- Issue
- Wiki
- 产品说明文档
  
输出：
- 目标清单
- 用户角色清单
- 场景清单
- 约束清单
- 非目标清单
  

---

步骤 2：还原功能层
输入：
- PRD
- API 文档
- 页面路由
- 用户流程说明
- 测试用例
  
输出：
- 功能树
- 功能边界说明
- 业务规则清单
- 功能流程描述
- 验收条件清单
  

---

步骤 3：还原架构层
输入：
- 架构图
- 接口文档
- 项目目录结构
- 设计说明
- ADR（如有）
  
输出：
- 模块清单
- 实体清单
- 接口清单
- 依赖图
- 功能-模块映射表
  

---

步骤 4：还原实现层
输入：
- 源代码仓库
- 目录结构
- 配置文件
- 部署脚本
- 外部依赖配置
  
输出：
- 代码单元清单
- 运行单元清单
- 配置对象清单
- 模块-代码映射表
- 外部集成点清单
  

---

步骤 5：还原验证层
输入：
- 单元测试
- 集成测试
- E2E 测试
- 日志
- 埋点
- 监控面板
- 告警规则
  
输出：
- 测试对象清单
- 功能/边界覆盖关系
- 可观测对象清单
- 关键运行证据清单
  

---

步骤 6：建立追踪关系
将上述各层对象建立映射关系，形成初版项目知识图谱或追踪矩阵。

输出：
- Goal → Feature
- Feature → Module
- Module → Code Unit
- Feature / Boundary → Test Object
- Feature / Flow → Observability Object
  

---

11. 证据机制设计

为了避免还原过程完全依赖主观推断，本方案要求每个对象和关系尽量附带证据来源。

证据类型

证据类型
来源
说明
doc
文档、PRD、README、Wiki
文档证据
code
源代码
实现证据
test
测试代码、测试报告
验证证据
runtime
日志、指标、告警、埋点
运行证据
inferred
AI 或人工推断
需要标注置信度

设计要求
- 尽量区分“显式定义”和“推断得出”
- 对关键对象和关键关系必须给出证据来源
- 没有证据时，应标记为“待确认”，而不是直接下结论
  

---

12. 初版实施建议

实施原则
- 不追求一步到位
- 先建立对象字典和关系字典
- 先做少量真实项目验证
- 先人工+AI 半自动协同，而不是追求全自动
  
第一阶段建议产出
1. 对象字典
2. 关系字典
3. 证据字典
4. 统一输出模板
5. 1～2 个真实项目试运行案例
  
第一阶段建议目标
- 能从已有项目中稳定提取目标、功能、模块、代码单元、测试对象
- 能形成基础追踪矩阵
- 能识别明显的缺口与未覆盖对象
  

---

13. 输出模板建议

初版输出模板建议统一为以下结构：

13.1 项目概览
- 项目名称
- 项目类型
- 主要用户
- 项目目标概述
  
13.2 产品层还原
- 目标清单
- 用户角色
- 场景清单
- 约束与非目标
  
13.3 功能层还原
- 功能树
- 功能边界
- 业务规则
- 功能流程
  
13.4 架构层还原
- 模块清单
- 实体清单
- 接口与依赖
- 关键架构决策
  
13.5 实现层还原
- 核心代码单元
- 模块-代码映射
- 配置与运行对象
- 外部集成点
  
13.6 验证层还原
- 测试对象
- 覆盖关系
- 日志、指标、监控、告警
  
13.7 关系与缺口
- 追踪矩阵
- 缺失对象
- 未覆盖对象
- 可疑偏差点
  

---

14. 当前不纳入初版范围的内容

为了避免初版过重，以下内容暂不作为当前重点：

- 复杂评分模型
- 自动化打分体系
- 多项目横向 benchmarking
- 行业专属规则库
- 全自动架构一致性检测
- 全自动缺陷分类与优先级判定
  
这些内容可在后续版本中逐步扩展。


---

15. 初版方案结论

本方案的初版结论如下：

1. 项目评审应从“还原对象结构”开始，而不是从评分开始
2. 应将项目统一建模为产品、功能、架构、实现、验证五层对象
3. 应建立层与层之间的追踪关系，形成结构化链路
4. 应借鉴成熟方法，而不是从零发明
5. 初版应聚焦对象结构、关系结构与证据机制
6. 评分与一致性判定可以作为后续阶段建立在还原结果之上的能力
  
因此，本方案的第一阶段目标不是“评价一个项目好不好”，而是：

把一个项目从产品目标到功能边界、从架构设计到代码实现、再到验证证据，还原为一组结构化对象与关系网络。

这一步完成后，后续的一致性分析、缺口分析、偏差分析与量化评审才能建立在可靠基础之上。


---

16. 一句话定义

还原式项目评审框架，是一套将任意项目从产品目标、功能边界、架构对象、实现单元到验证证据逐层还原为结构化对象与关系网络的综合方法，用于支撑后续的一致性评审与项目治理。


---

17. 附录：初版对象母表（V1）

对象类型
核心字段
作用
Goal
id, name, problem, target_user
定义项目目标
User Role
id, name, context
定义用户对象
Scenario
id, actor, trigger, outcome
定义使用场景
Feature
id, name, goal_ref, summary
定义功能能力
Business Rule
id, feature_ref, condition, behavior
定义规则
Feature Boundary
id, feature_ref, in_scope, out_of_scope
定义边界
Module
id, name, responsibility, feature_refs
定义架构支撑单元
Domain Entity
id, name, meaning, owner_module
定义核心实体
Code Unit
id, path, type, module_ref
定义实现单元
Test Object
id, type, target_ref, boundary_ref
定义验证单元


---

18. 附录：初版关系母表（V1）

关系类型
起点
终点
含义
supports
Feature
Goal
功能支撑目标
constrains
Business Rule
Feature
规则约束功能
maps_to
Feature
Module
功能映射到模块
implemented_by
Module
Code Unit
模块由代码实现
covers
Test Object
Feature / Boundary
测试覆盖功能或边界


---

这份文档已经可以作为你当前阶段的初版方案文档。  
它的重点是把“产品需求”和“初版解决方案”描述清楚，同时为后面继续演进到评分、AI Agent、自动化抽取留下空间。
