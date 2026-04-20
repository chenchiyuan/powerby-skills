---
name: design-language-extraction
description: |
  设计语言提取与结构化还原。支持两种路径：（1）有参考网站时，从目标网站的页面、截图、DOM、CSS、computed style、design token 和组件文档中提取；（2）无参考网站时，通过 pb-v1-talk 讨论收敛设计方向，再基于方向描述设计。两种路径都输出符合 schema.json 的结构化规则文件。
  当用户需要参考某个网站的设计风格、或基于方向描述建立设计语言时使用。即使用户只说"参考这个网站的风格"、"提取这个站点的设计规则"、或"我想要一个极简风格的设计"，也应触发此 Skill。
  不适用于：最终网页工程代码生成、品牌战略咨询、自动化爬虫实现。
compatibility:
  - web-access
  - local-filesystem
  - python3
  - pb-v1-talk (工具, 可选, 无参考路径的设计方向讨论)
  - pb-v1-design-system (下游, design-language.json)
---

# Design Language Extraction

Use this skill to extract or design a complete, structured design language.
Apply it when the user wants to reference a website's design style, build a design system from an existing site, extract design specifications for reproduction, or create a design language from a direction description without a reference website.
Do not rely on it for final web engineering code, brand strategy consulting, or crawler implementation.

## Purpose

从目标网站提取完整的设计语言语法体系，或基于方向描述从零设计——不是零散的颜色和字体，而是一套可被程序消费、可验证复现的结构化规则集。成功使用的样子：输出一份符合 `schema.json` 的 JSON 文件，覆盖六层规则，每条规则携带证据链，整体可直接驱动页面生成器。

## Success criteria

- 输出文件通过 `schema.json` 校验，所有 required 字段齐全
- Token 三层（Seed → Map → Alias）完整提取，语义映射率 ≥ 95%
- 核心组件规则覆盖率 ≥ 95%，状态覆盖（default/hover/active/focus/disabled/loading/error/empty）= 100%
- 每条高优先级规则至少有一个证据来源，推断规则显式标注可信度
- 页面模板覆盖目标站点所有核心页面类型
- 输出可被下游页面生成器直接消费，无需人工二次整理

## Strategy

> **设计语言提取是"语法还原"，不是"视觉模仿"。**

模型的惯性是看到网站就开始描述"主色是蓝色、字体是 14px、圆角是 8px"——这是视觉元素罗列，不是设计语言。真正的设计语言是一套语法系统：颜色不是"有哪些"而是"如何使用、如何组合、如何表达层级与状态"。

采用四段式认知框架：

1. **定义成功标准** — 明确本次提取的目标范围（全站 vs 特定页面类型）、输出精度要求、证据完整度要求。不要一上来就开始抓取。
2. **判断路径：有参考 vs 无参考** — 有参考网站时走提取路径（下方 Step 2-8）；无参考网站时走设计路径（调用 pb-v1-talk 讨论收敛方向，再基于方向描述设计 Token 和规则）。两条路径的输出格式完全相同，都必须符合 schema.json。
3. **每一步的结果都是证据** — 提取到的每个值都要标记来源类型（docs/css/computed_style/dom/screenshot/inferred/designed）和可信度。不要把推断当事实。无参考路径的设计决策标记 `source_type: "designed"` 和 `confidence: "high"`（因为是有意设计的，不是推断的）。
4. **对照成功标准，满足即停止** — 用 verification 指标检查覆盖率，达标即停止，不追加无意义的细节。

**对抗模型惯性**：

| 模型惯性 | 真实情况 |
|---------|---------|
| 提取颜色就是列出所有出现过的颜色值 | 颜色必须建立三层语义：Seed（品牌色）→ Map（色阶梯度）→ Alias（组件消费的语义色） |
| 字体提取就是记录 font-family 和 font-size | 字体系统包含字阶、行高、字重、文本角色、层级对比规则 |
| 组件提取就是列出组件名称和样式 | 组件规则包含 anatomy、variants、states、tokens、interaction_rules、composition_rules |
| 提取完视觉元素就算完成 | 还需要提取价值观、原则、文案规则、导航规则、反馈规则、页面模板 |
| 所有提取结果都是确定的事实 | 必须区分显式事实（文档/CSS 明确定义）和推断（从多处证据归纳），推断必须标注可信度 |

## Tools and capability boundaries

**原子行为抽象**：

| 原子行为 | 工具映射 | 适用场景 | 不适用场景 |
|---------|---------|---------|---------|
| 获取页面内容 | WebFetch | 静态页面、文档页、API 端点 | 需要登录的页面、重度 JS 渲染的 SPA |
| 搜索设计资源 | WebSearch | 查找目标站点的设计系统文档、组件库文档 | 已知具体 URL 时不需要搜索 |
| 分析 DOM/CSS | Bash (脚本) | 批量提取 computed style、CSS variables、色值统计 | 需要语义理解的判断 |
| 读写规则文件 | Read/Write | 管理输出的 JSON 规则文件、读取 schema | — |
| 校验输出 | Bash (脚本) | 用 schema.json 校验输出文件的结构完整性 | 语义正确性判断 |
| 设计方向讨论 | pb-v1-talk | 无参考路径：收敛用户的方向描述为结构化设计意图 | 有参考网站时不需要 |

**边界声明**：
- 本 Skill 只负责提取和结构化设计语言规则，不负责基于规则生成页面
- 不做自动化爬虫——页面获取使用 WebFetch，复杂场景由用户提供截图或 DOM
- 不做品牌战略分析——价值观层只提取可观察的 UI 决策倾向，不做商业解读

## Important facts and constraints

**Token 三层架构是核心骨架**：
- Seed Token 是设计意图源头（colorPrimary、fontSizeBase 等），后续所有值从这里派生
- Map Token 是梯度层（色阶、字阶、间距阶梯等），表达系统内部的节奏和层次
- Alias Token 是语义层（colorTextPrimary、colorBgContainer 等），组件直接消费这一层
- 没有 Alias Token 就无法稳定生成页面——这是最容易被跳过但最关键的一层

**证据链是硬约束**：
- 每条规则必须关联证据类型：screenshot / dom / css / computed_style / token / docs / inferred
- 推断规则必须标注可信度（high / medium / low）
- 高优先级规则应尽量双证据验证

**schema.json 是输出契约**：
- 输出必须严格符合 `schemas/schema.json`（已打包在 skill 目录内）
- 17 个顶层字段全部 required：meta, brand, principles, tokens, layout, typography, iconography, elevation, motion, content, navigation, components, patterns, responsive, accessibility, evidence, verification
- 详细字段定义见 `references/schema-guide.md`

**常见失败模式**：
- 只提取了视觉 Token 而遗漏了组件规则和页面模板 → 无法驱动页面生成
- Alias Token 缺失 → 组件无法消费 Token，生成结果不稳定
- 证据链缺失 → 规则可信度无法评估，下游无法判断哪些规则可靠
- 把推断写成事实 → 误导下游生成器

## Workflow

### Step 1: 建立提取范围与成功标准

**目的**：明确本次提取的边界，判断走哪条路径。

- 确认用户是否提供了参考网站 URL
- **有参考网站** → 走提取路径（Step 2-8）
  - 确认目标网站 URL 和需要覆盖的页面类型
  - 确认输出精度要求（全量提取 vs 核心子集）
  - 确认是否有已知的设计系统文档可用
  - 输出：提取计划（目标页面列表 + 预期覆盖范围）
- **无参考网站** → 走设计路径（Step 1b）
  - 确认用户的方向描述（风格关键词、目标受众、产品类型）
  - 输出：进入 Step 1b

### Step 1b: 无参考路径 — 设计方向讨论与设计（仅无参考时执行）

**目的**：通过讨论收敛设计方向，基于方向从零设计完整的设计语言 JSON。

**阶段 A: 方向收敛**
- 调用 pb-v1-talk 进行设计方向讨论，讨论维度包括：
  - 产品类型和目标受众
  - 美学风格倾向（极简/丰富/复古/工业/柔和等）
  - 配色倾向（冷色/暖色/中性/单色/多彩）
  - 字体风格（衬线/无衬线/等宽/手写）
  - 信息密度（稀疏/适中/密集）
- 收敛为结构化方向描述：brand positioning + adjectives + visual priority
- 用户确认方向后进入阶段 B

**阶段 B: Token 设计**
- 基于方向描述设计 Seed Token（品牌色、基础字号、基础圆角、基础间距）
- 从 Seed 派生 Map Token（色阶、字阶、间距阶梯）
- 从 Map 派生 Alias Token（语义色、语义字号、语义间距）
- 所有设计决策标记 `source_type: "designed"`，`confidence: "high"`

**阶段 C: 规则设计**
- 基于 Token 设计七大系统规则（layout, typography, iconography, elevation, motion, content, navigation）
- 设计核心组件规则（Button, Input, Card, Modal 等）
- 设计页面模板规则
- 填充 brand、principles、responsive、accessibility

**阶段 D: 校验与输出**
- 用 schema.json 校验输出完整性
- 输出 design-language.json
- 跳转到 Step 9（最终校验）

### Step 2: 搜索设计系统文档

**目的**：优先从权威文档提取，减少逆向推断。

- 搜索目标站点是否有公开的设计系统文档、组件库、Design Token 定义
- 搜索是否基于已知设计系统（Ant Design、Material Design、Chakra 等）
- 如果找到文档，从文档提取的规则标记为 `source_type: "docs"`，可信度 high
- 输出：可用文档清单 + 基础 Token 初稿

### Step 3: 提取全局 Token（Seed → Map → Alias）

**目的**：建立视觉系统的变量骨架。

- 从 CSS Variables / computed style / 文档中提取 Seed Token
- 从色阶、字阶、间距阶梯中构建 Map Token
- 从组件样式中归纳 Alias Token（语义映射）
- 每个 Token 标记来源和可信度
- 输出：tokens 对象（seed + map + alias）

### Gate: Token 完整性验证

**触发条件**：Step 3 完成后
**验证内容**：Seed Token 6 个 required 字段是否齐全；Map Token 8 个 required 数组是否非空；Alias Token 7 个 required 分类是否覆盖
**通过标准**：所有 required 字段有值，Alias Token 语义映射率 ≥ 80%
**未通过处理**：回退补充缺失的 Token，优先从 computed style 补充

### Step 4: 提取系统级规则

**目的**：建立布局、字体、图标、层级、动效、文案、导航七大系统规则。

- 按 schema 定义逐一提取：layout, typography, iconography, elevation, motion, content, navigation
- 每个系统的 required 字段必须填充
- **布局系统额外提取**：
  - `background_decoration`：识别 Hero 区域及其他 section 的背景装饰层（glow orbs、gradient streaks、gradient overlays），按区域记录每层的类型、颜色、尺寸、模糊、动画和定位
  - `section_pattern`：观察页面 section 背景是否存在交替规律（如奇数 section 用渐变、偶数 section 用纯色），提取交替策略和变体定义
- **动效系统额外提取**：
  - `keyframes`：从 CSS 中提取所有自定义 @keyframes 定义（float、pulse、scroll-right、enter 等），记录名称、定义和用途
  - `entrance`：识别页面是否使用 IntersectionObserver 或 scroll-timeline 触发入场动画，提取触发策略、默认 keyframe、交错延迟和阈值
- 输出：七大系统规则对象

### Step 5: 提取组件规则

**目的**：建立组件字典，覆盖基础原子到复合组件。

- 从页面中识别核心组件（按 schema 的 componentRule 结构）
- 每个组件提取：purpose, anatomy, variants, sizes, states, tokens, interaction_rules, composition_rules
- **状态 overlay 提取**：对于有 hover/active 等交互状态的组件，检查是否存在浮现的 overlay 层（渐变遮罩、内容浮层、高亮层），在 states[].overlays 中结构化记录 overlay 的类型、背景、渐变、模糊、过渡动画
  - 典型场景：卡片 hover 时的渐变 overlay + 内容浮层、按钮 hover 时的内部高亮层（如 foreground/5）
- **无限滚动组件**：识别 marquee/infinite scroll 类组件，作为独立 componentRule 提取，其 tokens 引用 keyframes 中的 scroll 动画
- 优先覆盖高频组件：Button, Input, Table, Card, Modal, Form, Navigation
- 输出：components 数组

### Step 6: 提取页面模板规则

**目的**：从组件级升级到页面级，建立页面结构组合规则。

- 按页面类型分类：Landing, Dashboard, List, Detail, Form, Result, Search, Settings, Auth, Exception
- 每种模板提取：goal, information_architecture, regions, recommended_components
- 输出：patterns 数组

### Gate: 覆盖率验证

**触发条件**：Step 6 完成后
**验证内容**：组件覆盖率、页面模板覆盖率、状态覆盖率、响应式覆盖率
**通过标准**：组件覆盖率 ≥ 95%，页面模板覆盖核心类型，状态覆盖 = 100%
**未通过处理**：识别缺失项，针对性补充

### Step 7: 补充品牌、原则、响应式、可访问性

**目的**：补全六层中的上层（价值观、原则）和横切关注点。

- 从整体视觉风格归纳 brand（positioning, adjectives, values, anti_values, visual_priority）
- 从设计决策中提取 principles（对齐、对比、重复、亲密性等）
- 提取 responsive 规则（断点变化、组件适配）
- 提取 accessibility 规则（对比度、焦点态、键盘可达性）
- 输出：brand, principles, responsive, accessibility 对象

### Step 8: 构建证据链与验证规格

**目的**：为所有规则建立可追溯的证据体系。

- 为每条规则关联 evidence_refs
- 构建 evidence 数组，每条证据包含 id, source_type, source_ref, confidence
- 构建 verification 对象，定义七项覆盖率指标的目标值
- 输出：evidence 数组 + verification 对象

### Step 9: 组装与校验

**目的**：将所有规则组装为最终 JSON 并校验。

- 组装 17 个顶层字段为完整 JSON
- 用 schema.json 校验结构完整性
- 检查缺失字段并发出提醒
- 输出：最终的 design-language.json

## Output format

输出一个符合 `docs/design-language-extraction/schema.json` 的 JSON 文件，保存到用户指定路径（默认 `design-language.json`）。

顶层结构：
```json
{
  "meta": { "site_name": "", "domain": "", "page_types": [], "theme_modes": [], "breakpoints": [] },
  "brand": { "positioning": "", "audience": [], "adjectives": [], "values": [], "anti_values": [], "visual_priority": [] },
  "principles": [],
  "tokens": { "seed": {}, "map": {}, "alias": {} },
  "layout": {},
  "typography": {},
  "iconography": {},
  "elevation": {},
  "motion": {},
  "content": {},
  "navigation": {},
  "components": [],
  "patterns": [],
  "responsive": {},
  "accessibility": {},
  "evidence": [],
  "verification": {}
}
```

## Resources

- `schemas/schema.json` — 输出结构的完整 JSON Schema 定义，Step 9 校验时使用
- `references/schema-guide.md` — schema.json 的字段说明与填写指南，Step 3-8 中按需读取
- `scripts/validate_output.py` — 用 schema.json 校验输出文件，Step 9 执行

## Subtask / parallelism guidance

- Step 2（搜索文档）和 Step 3（提取 Token）可以部分并行：搜索文档的同时可以开始从页面提取 computed style
- Step 4 的七大系统规则之间相互独立，可以并行提取
- Step 5（组件）和 Step 6（页面模板）有依赖：组件规则是页面模板的基础，不能并行
- Step 7 的四个子任务（brand, principles, responsive, accessibility）相互独立，可以并行

## Examples

**Example 1: 提取 Ant Design 官网的设计语言**

Input: "帮我提取 ant.design 的设计语言规则，我想参考它的风格做一个后台管理系统"

Output: 一份完整的 design-language.json，其中：
- brand.positioning = "企业级"
- brand.adjectives = ["确定性", "自然", "效率优先", "克制"]
- tokens.seed.colorPrimary = "#1677ff"
- tokens.seed.fontSizeBase = 14
- tokens.alias.text.primary = "rgba(0, 0, 0, 0.88)"
- components 覆盖 Button, Input, Table, Form, Modal, Drawer, Menu 等核心组件
- 每条规则携带 evidence_refs 指向具体证据

**Example 2: 从截图提取设计语言**

Input: "我有几张竞品网站的截图，帮我提取它的设计风格规则"

Output: 一份 design-language.json，推断规则标注 `source_type: "screenshot"` 和 `confidence: "medium"`，并在 verification 中标注截图来源的覆盖率限制。

**Example 3: 无参考网站，从方向描述设计**

Input: "我想做一个极简风格的 AI 工具产品，目标用户是开发者，不要花哨的装饰"

Output: 调用 pb-v1-talk 讨论收敛方向（极简、开发者、工具型、中性色调、无衬线字体），然后基于方向设计完整的 design-language.json。所有规则标注 `source_type: "designed"` 和 `confidence: "high"`。Token 体系偏向中性色、等宽/无衬线字体、紧凑间距、小圆角。

## Safety

- 不允许把推断结果写成显式事实——所有推断必须标注 `source_type: "inferred"` 和可信度
- 不允许跳过 Token 三层架构直接输出扁平色值——没有语义映射的 Token 无法驱动生成
- 不允许输出不符合 schema.json 的结构——输出必须通过校验
- 不允许在证据不足时声称"高可信度"——证据不足时必须降级为 medium 或 low
- 不允许为了覆盖率指标而填充无意义的占位数据——宁可标注缺失，不可伪造

