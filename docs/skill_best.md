下面我给你一版**结合你前面那篇 Web Access 方法论 + 这份官方 skill-creator 规范**之后的 **Skill 最佳实践框架**。重点不是把官方规范复述一遍，而是把它们融合成一套**真正可落地的设计、编写、评估、迭代框架**。

一句话先定调：

**好的 Skill 不是“写一段提示词”，而是一个可触发、可执行、可评估、可迭代的能力包。**

下面按“从设计到上线”的顺序展开。

---

## 🧭 一、总原则：把 Skill 当成“能力产品”来做

结合你前面总结的文章，以及官方规范，Skill 的最佳实践可以压缩成一个完整公式：

| **层级** | **核心问题** | **最佳实践** |
|---|---|---|
| **触发层** | 什么时候会被调用？ | 用 description 明确触发语境，写得具体且略“主动” |
| **认知层** | 模型该如何判断任务？ | 提供策略哲学，而不是写死流程 |
| **执行层** | 模型靠什么完成任务？ | 提供最小完备工具集与清晰边界 |
| **约束层** | 哪些事实、风险、前提要强调？ | 补充必要事实说明、环境依赖、安全边界 |
| **扩展层** | 如何处理复杂任务？ | 支持分治、脚本化、资源引用、渐进加载 |
| **验证层** | 怎么知道 Skill 真的更好？ | 做 baseline 对照、定量评估、人工 review |
| **迭代层** | 如何持续变强而不越改越歪？ | 基于反馈泛化修订，避免 overfit |
| **交付层** | 怎么让 Skill 易装、易触发、易维护？ | 包结构清晰、描述优化、资源分层、最终打包 |

所以，一个成熟 Skill 的目标不是“能跑一次”，而是：

- **能触发**
- **能泛化**
- **能评估**
- **能优化**
- **能交付**

---

## 🏗️ 二、Skill 设计总框架：推荐采用 7 层结构

下面这套结构，是我建议你今后写 Skill 时统一采用的“母版框架”。

---

## 1. 🎯 Intent Layer：先定义能力边界，而不是先写 Prompt

这一层解决的是：**这个 Skill 到底是干什么的，不干什么。**

### 需要回答的核心问题
根据官方规范，创建 Skill 前必须先搞清楚：

1. **这个 Skill 要让 Agent 获得什么能力？**
2. **在什么用户语境下应触发？**
3. **输出长什么样？**
4. **这个任务适不适合做测试集和评估？**

### 最佳实践
不要用“功能名词”定义 Skill，要用“用户任务”定义 Skill。

#### 差的定义方式
- 一个网页技能
- 一个数据分析技能
- 一个写报告技能

#### 好的定义方式
- 帮 Agent 在需要联网、登录态、动态页面、网页交互时，自主选择搜索 / 读取 / 浏览器策略并完成任务
- 帮 Agent 在用户提出“调研多个来源并输出结构化结论”时，进行分治式研究与汇总
- 帮 Agent 在处理固定格式输入文件时，稳定地产出指定格式输出

### 建议产出
在写 SKILL.md 前，先写一页“设计卡”：

- **Skill 名称**
- **核心能力**
- **典型触发场景**
- **非适用场景**
- **输入模式**
- **输出模式**
- **成功标准**
- **风险边界**
- **是否适合做定量评估**

这一步非常值钱，能防止后面 Skill 越写越散。

---

## 2. 🧠 Strategy Layer：写“策略哲学”，不要把流程写死

这是你前面那篇文章最强的部分，也是我认为官方规范里“Explain the why / keep prompt lean”的最好落地方式。

### 为什么这是最佳实践
如果 Skill 只写固定步骤：

1. 搜索
2. 打开网页
3. 点击按钮
4. 总结结果

那它只在你预设的环境里有效。

真正强的 Skill，要教模型：

- **先判断任务类型**
- **再选择工具**
- **根据反馈切换路径**
- **到达目标后停止**

这就是“策略哲学”。

### 推荐写法：四段式认知框架
你可以把大多数通用 Skill 的策略层写成类似这种结构：

#### 1）先定义成功标准
- 任务完成意味着什么
- 需要拿到哪些证据或结果
- 最终输出应满足什么条件

#### 2）先走最可能成功的起点
- 根据任务特征选首选路径
- 避免在明显不合适的工具或路径上空转

#### 3）把中间反馈当证据，不是只看成败
- 搜不到，不一定是关键词错
- 页面打不开，不一定是网站挂了
- 遇到弹窗，不一定真的阻塞目标

#### 4）满足标准即停止
- 不追加无意义探索
- 不因为“还可以多查一点”而拉长任务

### 最佳实践原则
Skill 要写的是：

- **判断框架**
- **切换原则**
- **停止条件**

而不是详细的 click-by-click 流程。

### 这一层的核心标准
如果换一个新站点、新文件、新任务，Skill 依然有指导意义，说明策略层写对了。

---

## 3. 🛠️ Capability Layer：工具要“最小完备”，并写清边界

官方规范强调 compatibility、resources、scripts；你前面的文章强调最小完备工具集。这两者其实是完全一致的。

### 最佳实践原则
不要追求工具越多越好，而要追求：

**工具覆盖关键原子能力 + 每个工具的边界清晰可判断**

### 推荐做法：先做原子行为抽象
例如 Web Access 那种抽法就非常好：

- **搜**：找信息源、找入口
- **看**：读取内容
- **做**：执行交互

然后再映射到工具层。

### 在 SKILL.md 里应写什么
每个关键工具都要写清：

- 它适合干什么
- 不适合干什么
- 什么情况下优先用它
- 什么情况下该换别的工具
- 和哪些工具搭配时效果更好

### 推荐模板
| **工具/资源** | **适用场景** | **不适用场景** | **备注** |
|---|---|---|---|
| Search | 找入口、找公开来源 | 登录态内容、站内动态页 | 用于发现，不是完成任务本身 |
| Fetch / curl | 公开静态页面 | 重 JS、登录墙、交互页 | 适合快速读取正文 |
| 浏览器/CDP | 登录态、动态渲染、点击上传 | 简单静态文本页 | 成本较高但能力完整 |
| scripts/xxx.py | 重复、确定性处理 | 开放式推理 | 用于提速与稳定 |

### 一个很重要的实践细节
**把重复出现的“确定性动作”下沉到 scripts/**，而不是让模型每次临时写。

这也是官方规范里非常强调的一点：

> 如果多次测试发现模型总在重复写类似脚本，就应该 bundle 成资源。

这会直接提升：

- 稳定性
- 成本表现
- token 效率
- 跨迭代一致性

---

## 4. 📌 Knowledge & Constraint Layer：补“必要事实说明”

这一层非常关键，很多 Skill 失败不是因为策略不对，而是因为**模型没在当下想起关键事实**。

### 最佳实践：Skill 中必须补三类信息

### 1）惰性知识 / 易忘事实
也就是模型“知道但不一定及时调用”的东西，例如：

- 某类网站通常需要登录态
- 某类文件有编码坑
- 某种渲染结果可能要等异步加载
- 某个环境变量缺失会导致常见报错
- 某类输出应优先读取正文而非原 HTML

### 2）明确存在最优路径的动作
如果某件事已经有最优解，不必假装开放。

例如：

- 优先使用某脚本
- 优先检查某状态
- 某环境下先走某命令
- 某格式转换优先走某模板

### 3）风险边界与禁止事项
这一点官方规范讲得很明确：

- 不要写令人意外的行为
- 不要做越权、误导、恶意或高风险操作
- 不要做和用户意图不一致的隐蔽动作

在你自己的 Skill 里，建议显式写出：

- 哪些资源不能碰
- 哪些动作必须谨慎
- 哪些情况下要停
- 哪些时候需要用户确认

### 最佳实践建议
把这部分单独写成一个 section，例如：

```markdown
## Important facts and constraints
```

比散落在正文里效果好得多，因为这类信息是“降低误判成本”的关键层。

---

## 5. 🪜 Structure Layer：按“渐进披露”组织内容，避免大而乱

官方规范里关于 **Progressive Disclosure** 的部分非常重要，我建议直接作为所有 Skill 的结构原则。

### 三层加载逻辑
#### 第一层：Metadata
- `name`
- `description`

这是触发层，必须短、准、强。

#### 第二层：SKILL.md 正文
- 提供高层工作方式
- 保持在合理长度内
- 不要把所有细节都堆进来

#### 第三层：Bundled Resources
- `scripts/`
- `references/`
- `assets/`

这是重内容区，按需加载。

### 最佳实践结构
```text
my-skill/
├── SKILL.md
├── scripts/
│   ├── normalize_data.py
│   └── build_report.py
├── references/
│   ├── domain-a.md
│   ├── domain-b.md
│   └── schemas.md
└── assets/
    └── template.md
```

### 推荐原则
#### SKILL.md 里只保留：
- 技能定位
- 触发语境
- 策略哲学
- 核心工作流
- 资源何时读取
- 输出要求
- 风险约束

#### references/ 里放：
- 特定领域知识
- 大文档
- 框架差异说明
- 分支场景说明

#### scripts/ 里放：
- 可重复、确定性、可复用操作

### 关键实践
如果 Skill 涉及多个 domain，不要把所有规则塞一页，应该按 variant 分文件组织，让模型按需读对应 reference。

这个组织方式能显著降低：

- 上下文污染
- 无关内容干扰
- 触发后正文过载

---

## 6. ✍️ Writing Layer：怎么写 SKILL.md 才更强

官方规范给了很多有价值的写法原则，这里结合你前面的讨论，整理成一套实操准则。

### 1）description 是第一触发器，必须“略主动”
官方明确说了：**description 要稍微 pushy 一点**，因为当前模型倾向于 undertrigger。

### 推荐写法
description 里同时包含两件事：

- **这个 Skill 做什么**
- **什么时候应该使用它**

而且“什么时候用”要写具体，不要泛。

#### 差的写法
- Helps with web tasks.

#### 好的写法
- Helps Claude handle tasks that require searching, reading, or interacting with websites, especially when the user asks to research across sites, use login-dependent pages, navigate dynamic web apps, submit forms, publish content, or work across multiple pages or tabs. Use this whenever the task involves web browsing beyond a simple one-page fetch, even if the user does not explicitly mention a browser.

这类 description 才更接近官方推荐风格。

### 2）正文多用祈使句，但少堆 MUST / NEVER
官方建议很值得采纳：

- 用 imperative form
- 解释 why
- 避免僵硬的命令式堆叠

#### 好写法
- Start by identifying what would count as a successful outcome.
- Prefer the shortest path that can genuinely test whether the target is reachable.
- Treat each intermediate result as evidence that may support or falsify the current plan.

而不是：

- MUST define success
- NEVER do X
- ALWAYS do Y

当然，风险边界除外，那里可以明确一点。

### 3）用“原因解释”替代僵硬规则
这是最容易把 Skill 写高级的地方。

#### 例子
不要只写：
- Use browser for dynamic pages.

可以写成：
- Use the browser when the target site depends on login state, dynamic rendering, or interaction. In these cases, search or fetch often produces misleading failures that are really tool mismatches rather than evidence that the content is unavailable.

这样模型更容易真的“懂”。

### 4）给固定输出模板时，要明确到可执行
当输出格式很重要时，建议单独给 section：

```markdown
## Output format
Use this structure:
# Title
## Executive summary
## Findings
## Recommendations
```

如果输出不稳定，后面根本没法评估。

### 5）例子要“真实用户化”，而不是教科书化
这和 eval 的原则一致。示例不要太抽象，要像真实请求。

---

## 7. 🧪 Evaluation Layer：Skill 必须内建评估思维

这是官方规范最强的一部分，也是很多人写 Skill 时最缺的部分。

一句话：

**没有评估闭环的 Skill，只能算草稿。**

### 最佳实践：把评估分成三类

| **类型** | **适用场景** | **作用** |
|---|---|---|
| **定性评估** | 写作、设计、研究、复杂产出 | 看是否好用、自然、符合预期 |
| **定量断言** | 结构化输出、格式转换、固定步骤任务 | 看是否客观达标 |
| **基线对照** | 新技能 / 改进技能都适合 | 判断 Skill 是否真的比不用更好 |

### 官方流程的核心价值
最重要的不是“跑几个 case”，而是：

- **with skill**
- **without skill / old skill**
- **同轮并发跑**
- **记录时延、token**
- **做 grading**
- **做 benchmark**
- **做 viewer review**
- **读用户反馈再迭代**

这是一套非常完整的技能评估闭环。

### 最佳实践建议
你以后写 Skill 时，至少要有：

#### 小规模初始测试
- 2–3 个真实 prompt
- 覆盖典型任务
- 每个 case 明确“我期望什么结果”

#### 定量断言（适合客观任务）
例如：

- 是否生成指定文件
- 是否包含指定字段
- 是否完成指定转换
- 是否遵循模板结构

#### 人工 review（适合主观任务）
例如：

- 输出是否清晰
- 是否自然
- 是否漏关键信息
- 是否过度执行
- 是否选择了正确策略

### 一个关键实践
**断言要“有区分度”**。

官方特别提到要识别：

- 总是通过的断言
- 高方差 case
- 不区分 with/without skill 的指标

这点非常专业。否则 benchmark 看起来很热闹，其实没信息量。

---

## 🔁 三、Skill 迭代最佳实践：不是“修 bug”，而是“抽象提升”

官方规范里“Improving the skill”这段，我非常赞同，尤其和你前面那篇文章的思路很合。

### 迭代时最容易犯的错
为了修一个 case，把 Skill 改成对那一个例子特化，最后：

- prompt 变长
- 规则变碎
- 可泛化性下降
- 模型越来越僵

这就是典型 overfit。

### 正确的迭代方法
#### 1）先从反馈里抽象出“共性问题”
不要问：
- 这个 case 哪里错了？

而要问：
- 它暴露了哪一类判断错误？
- 是触发问题、策略问题、工具边界问题、事实缺失问题，还是输出约束问题？

#### 2）优先删掉无效指令
如果某段指令总让模型浪费时间，就删。

Skill 不是说明文越长越好，**没贡献的说明就是噪音。**

#### 3）把“重复劳动”沉入资源层
如果多个 run 都在写同一个 helper script，就正式收编进 `scripts/`。

#### 4）改抽象，不改补丁
例如：
- 不要新增“如果小红书就这样，否则那样”的碎规则
- 更好的改法是提升成“遇到登录态/反爬/动态站点时优先浏览器”的策略原则

### 最佳实践迭代顺序
1. 看 benchmark 和 review
2. 看 transcript，不只看最终输出
3. 找出错误发生在哪一层
4. 优先修：
   - description 触发错误
   - 成功标准不清
   - 工具边界不清
   - 事实说明缺失
   - 输出模板不稳
5. 再跑同一组 eval
6. 需要时扩展测试集

---

## 🧩 四、我建议你采用的统一 SKILL.md 框架

下面给你一版**通用最佳实践模板骨架**。这不是某个具体 Skill 内容，而是你今后写 Skill 时可以复用的结构。

---

## 推荐 SKILL.md 骨架

```markdown
---
name: <skill-name>
description: <这个 skill 做什么 + 在什么具体语境下应触发。描述要具体、主动，覆盖典型表达和隐式需求。>
compatibility:
  - <optional tools / dependencies>
---

# <Skill Title>

Use this skill to <核心任务描述>.
Apply it when <典型触发条件>.
Do not rely on it for <非适用边界>.

## Purpose
Briefly explain the capability this skill provides and what successful use looks like.

## Success criteria
Before acting, identify:
- What result counts as success
- What evidence or outputs are required
- What constraints matter most

Stop once the success criteria are met.

## Strategy
Use this decision pattern:

1. Define the goal clearly.
2. Choose the most direct initial path based on the task.
3. Treat intermediate results as evidence, not just pass/fail signals.
4. Change approach when the evidence suggests a mismatch.
5. Stop when the task is complete.

Explain any domain-specific strategy principles here.

## Tools and capability boundaries
Choose tools based on the task:

- **Tool A**: when to use it, when not to use it
- **Tool B**: when to use it, when not to use it
- **Tool C**: when to use it, when not to use it

If a deterministic or repetitive operation appears, use the bundled script/resource instead of recreating it.

## Important facts and constraints
Keep these in mind:
- <environment fact>
- <common failure mode>
- <known best path>
- <safety/risk constraint>

## Workflow
Follow this high-level workflow:

1. Understand the task and constraints
2. Select the right approach
3. Execute while checking evidence
4. Produce the required output
5. Cleanly stop

## Output format
Use this structure unless the user asks otherwise:

# <Title>
## Summary
## Findings
## Evidence
## Recommendations

## Resources
Use bundled resources as needed:

- `references/<file>.md` for <when to read it>
- `scripts/<file>.py` for <when to execute it>
- `assets/<file>` for <when to use it>

## Subtask / parallelism guidance
If the task contains multiple independent targets:
- split by target
- keep each subtask focused on one objective
- return only synthesized results to the main agent

Describe goals for subtasks without over-prescribing the method.

## Examples
**Example 1**
Input: ...
Output: ...

**Example 2**
Input: ...
Output: ...

## Safety
Never do anything outside the user’s intent.
Avoid destructive, privacy-sensitive, or irreversible actions unless explicitly required and clearly appropriate.
```

---

## 📊 五、最佳实践工作流：从 0 到可交付 Skill 的标准流程

下面这部分，是我建议你以后实际做 Skill 时遵循的“项目流程”。

### 阶段 1：Intent Discovery
- 明确能力边界
- 明确触发场景
- 明确输出格式
- 判断是否适合 eval

### 阶段 2：Draft
- 写 description
- 写策略哲学
- 写工具边界
- 写事实说明
- 写输出模板
- 按需拆 scripts / references

### 阶段 3：Test Set
- 先做 2–3 个真实案例
- prompt 要像真实用户输入
- 覆盖典型与边界情况

### 阶段 4：Baseline + With Skill
- 同轮跑 with_skill 和 baseline
- 记录输出、时间、token

### 阶段 5：Grading + Review
- 客观任务加断言
- 主观任务做人审
- 用 viewer 展示结果

### 阶段 6：Iterate
- 从失败 case 里抽象问题
- 优先修通用原则
- 避免对单 case 过拟合

### 阶段 7：Description Optimization
- 用 trigger eval 做触发测试
- 优化 description，不是乱加关键词
- 同时做 should-trigger / should-not-trigger

### 阶段 8：Package
- 打包 skill
- 保持命名稳定
- 给出安装路径与版本说明

---

## 💡 六、结合前文，我给出的“Skill 最佳实践十条”

最后我把整套框架压成十条最重要的操作原则，适合作为你以后写 Skill 的 checklist。

### 1. 先定义用户任务，不要先定义功能名词
Skill 面向的是“用户要完成什么”，不是“你接了什么工具”。

### 2. description 是第一触发器，必须写得具体、主动、带语境
它既决定会不会触发，也决定会不会误触发。

### 3. 先写策略哲学，再写流程
Skill 最应该教会模型的是“判断方式”，不是“固定步骤”。

### 4. 工具设计遵循最小完备集原则
覆盖关键原子能力即可，重点是边界清楚。

### 5. 把容易忘的事实前置进 Skill
尤其是环境前提、典型误判、最优路径、风险边界。

### 6. 重复且确定性的工作下沉到 scripts/
不要让模型每次重复造轮子。

### 7. 多领域内容用 references/ 分层组织
不要把所有知识堆在 SKILL.md 正文里。

### 8. 子任务写目标，不写死方法
尤其多 Agent 场景，要避免动词把策略提前锚死。

### 9. Skill 完成标准不是“看着不错”，而是“有 baseline、有 review、有迭代”
没有评估闭环，就谈不上最佳实践。

### 10. 迭代时修抽象层，不修案例补丁
从个别失败中提炼普遍规律，才不会越改越脆。

---

## ✅ 最终版定义：什么叫“最佳实践 Skill”

如果用一句更完整的话来定义：

**最佳实践的 Skill，是一个通过 description 精准触发、通过策略哲学校准模型判断、通过最小完备工具集支持执行、通过必要事实说明减少误判、通过资源分层控制上下文、通过评估闭环持续优化的能力模块。**

这比“写一个 Prompt”高了整整一个工程层级。

---

## 🧱 给你的最终建议：以后统一按这个顺序做

你以后如果要系统化产出 Skill，我建议固定采用这个顺序：

1. **写 Intent Card**
2. **写 SKILL.md 初稿**
3. **补 scripts / references**
4. **设计 2–3 个真实 eval**
5. **跑 with_skill vs baseline**
6. **做 grading + review**
7. **抽象修订**
8. **优化 description**
9. **打包交付**

这样做出来的 Skill，才是可复用、可维护、可增长的。

如果用一个更轻松的比喻：  
**别把 Skill 当成“灵机一动写的咒语”，要把它当成“给 Agent 装的一块可升级主板”。**  
写得对，整个系统都会更聪明。
