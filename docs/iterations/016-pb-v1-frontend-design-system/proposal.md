# 016 - pb-v1 前端设计系统升级

**创建日期**: 2026-04-18
**状态**: 澄清完成，待实现
**来源**: aivideo 首页设计实战复盘

---

## 一、问题清单

### P-001：CSS 双轨冲突
**现象**: aivideo 首页同时存在自定义 CSS 变量和 Tailwind utility class，两套系统的字体、间距、颜色、圆角互相覆盖，视觉语言在页面内部分裂。
**根因**: pb-v1-frontend 没有"单一 CSS 系统"约束，实现过程中引入第二套系统时没有门禁阻止。

### P-002：没有设计 Token 系统
**现象**: 不同卡片的 padding 各自为政（16px / 20px / 24px 混用），圆角没有统一规则，间距没有节奏感。
**根因**: skill 直接从设计方向跳到组件实现，没有"先建立 token 系统"的强制阶段。

### P-003：参考风格提取不结构化
**现象**: 用户说"参考 YouMind 的风格"，skill 只提取了模糊的美学感受（"极简"、"留白多"），没有提取具体数值（背景色 hex、字体名、卡片 padding px、圆角 px）。实现时没有锚点，结果是"感觉像"但细节全错。
**根因**: pb-v1-frontend 没有强制的风格结构化提取协议，design-language-extraction skill 没有被纳入前置流程。

### P-004：方向多次切换导致混乱
**现象**: aivideo 首页经历了"暖橙色原版 → 极简黑白重设计 → 引入 Tailwind 重构"三次方向切换，每次都是渐进式替换而非全量重写，导致两套系统长期并存。
**根因**: skill 没有"方向锁定门禁"——美学方向在实现阶段可以随时切换，没有用户确认机制。

### P-005：大批量盲改，无增量验证
**现象**: 一次性替换整个 CSS 文件（1700+ 行），改完才第一次打开浏览器，发现整体混乱时已无法追溯问题来源。
**根因**: pb-v1-frontend 的增量验证是"建议"而非"门禁"，pb-v1-brower 工具不可用时没有降级策略，验证被跳过。

### P-006：美学验证和功能验证混在一起
**现象**: Phase 4 功能验证同时承担"功能是否完整"和"视觉是否正确"两个职责，两者关注点不同，互相干扰，都做不好。
**根因**: skill 没有把功能验证和美学 Review 分离为独立阶段。

---

## 二、根本原因分析

pb-v1-frontend 是一个优秀的**设计视觉 skill**，但缺少**实现纪律**。

它能帮你想清楚"设计应该长什么样"（Purpose / Tone / Constraints / Differentiation 框架完整），但没有约束"怎么把它稳定地实现出来"。

核心缺失：
- 设计系统建立阶段缺失（token 先于组件）
- 单一 CSS 系统约束缺失
- 方向锁定门禁缺失
- 增量验证是建议而非门禁
- 美学 Review 没有独立 skill

---

## 三、澄清历史

**澄清日期**: 2026-04-18
**澄清方式**: pb-v1-talk 结构化讨论
**参与方**: 用户 + pb-v1-talk（前端架构师角色）

### CLR-001：设计系统 skill 的边界
- **问题**: 把提取的设计语言 JSON 转化为 CSS token，放在哪个 skill？
- **结论**: 新建独立 skill `pb-v1-design-system`，不放在 design-language-extraction 也不放在 pb-v1-frontend
- **来源**: user_confirmed

### CLR-002：design-language-extraction 的"无参考"路径
- **问题**: 用户没有参考网站，只有方向描述时怎么处理？
- **结论**: 放在 design-language-extraction 里处理——有参考就提取，无参考就先调用讨论确认方向再设计
- **来源**: user_confirmed

### CLR-003：组件化粒度
- **问题**: 原子级（Button/Card）还是区块级（Hero/Nav）？
- **结论**: 先原子级，再区块级，这是正确的迭代顺序
- **来源**: user_confirmed

### CLR-004：美学 Review 和功能验证的关系
- **问题**: 两者是同一循环还是分开？
- **结论**: 先做功能验证，再单独做美学 Review，两者是独立阶段
- **来源**: user_confirmed

### CLR-005：美学 Review 的粒度
- **问题**: 组件级还是页面级？
- **结论**: 先组件级 Review，再页面级 Review，两者都要
- **来源**: user_confirmed

### CLR-006：Demo 前置确认
- **问题**: 设计系统建立后，何时让用户确认方向？
- **结论**: pb-v1-design-system 需要调用 pb-v1-demo，基于设计风格和功能出 mock demo（不做后端，数据可 mock），用户确认 demo 后才进入实现阶段
- **来源**: user_confirmed

---

## 四、迭代方案

### 新 Skill 体系架构

```
PHASE 0: 风格确认
  有参考网站 → design-language-extraction（提取 JSON）
  无参考网站 → design-language-extraction（讨论→设计→JSON）
                        ↓ JSON
PHASE 1: 设计系统建立  pb-v1-design-system（新建）
  JSON → design-system.css（token）
       → design-principles.md（规则）
       → 调用 pb-v1-demo（mock 数据，不做后端）
       → 用户确认 Demo ✅ 才进入实现
                        ↓ token + principles + 用户确认
PHASE 2: 实现  pb-v1-frontend（重构）
  Step 1: 原子组件（Button / Input / Card / Badge...）
          ↓ 功能验证（pb-v1-brower）
          ↓ 组件级美学 Review（pb-v1-ui-review）
  Step 2: 区块组件（Hero / Nav / Pricing / FAQ...）
          ↓ 功能验证
          ↓ 组件级美学 Review
  Step 3: 页面组合
          ↓ 功能验证
          ↓ 页面级美学 Review（pb-v1-ui-review）
```

### Skill 变更清单

| Skill | 变更类型 | 核心变更内容 |
|-------|---------|------------|
| `design-language-extraction` | 扩展 | 增加"无参考网站"路径：先讨论确认方向，再设计输出 JSON |
| `pb-v1-design-system` | **新建** | JSON → CSS token + 设计原则文档 + 调用 pb-v1-demo 确认 |
| `pb-v1-frontend` | **重构** | 移除美学决策职责，变为纯执行者；强制原子→区块→页面顺序；每步有验证门禁 |
| `pb-v1-ui-review` | **新建** | 对照 token + 原则做组件级/页面级美学审查，输出具体违规项 |
| `pb-v1-demo` | 不变 | 被 pb-v1-design-system 调用 |
| `pb-v1-brower` | 不变 | 功能验证工具 |

### pb-v1-design-system 核心职责

**输入**:
- `design-language-extraction` 产出的 JSON
- 功能需求描述（用于 demo mock）

**产出**:
1. `design-system.css` — 完整 `:root {}` token
   - Spacing（基于 4px/8px 网格）
   - Color（最多 6 个语义色）
   - Border Radius（统一风格）
   - Typography Scale
   - Shadow
2. `design-principles.md` — 从 token 推导的使用规则
3. Mock Demo（调用 pb-v1-demo）— 用户确认后解锁实现阶段

**门禁**: 用户确认 Demo 前，不得进入 pb-v1-frontend 实现阶段

### pb-v1-frontend 重构方向

**移除**:
- 美学决策职责（交给上游 pb-v1-design-system）
- 模糊的"选择美学方向"阶段

**新增**:
- 强制前置检查：`design-system.css` 和 `design-principles.md` 必须存在
- 单一 CSS 系统声明：实现开始前明确声明使用哪套系统，不得中途引入第二套
- 原子→区块→页面的强制顺序，每步完成后有验证门禁
- pb-v1-brower 不可用时的降级策略（要求用户手动截图确认）

**保留**:
- 功能完整还原的底线要求
- 响应式和可访问性要求
- 代码生产级标准

### pb-v1-ui-review 核心职责

**输入**:
- 运行中的页面 URL
- `design-system.css`（token 参照）
- `design-principles.md`（规则参照）
- 审查粒度：组件级 or 页面级

**审查维度**:
1. Token 合规性：间距/颜色/圆角/字号是否来自 token
2. 视觉节奏：相邻元素的间距是否有规律
3. 层级清晰度：字号/字重/颜色是否形成清晰的信息层级
4. 一致性：同类组件的视觉处理是否统一
5. 整体美学（页面级）：是否符合设计方向的核心特征

**输出**:
- 具体违规项（"这里用了 14px，应该用 `--text-sm: 13px`"，不是"感觉不好看"）
- 修复优先级（critical / major / minor）
- 修复后触发再次 Review

---

## 五、实现优先级

1. **P0**: `pb-v1-design-system`（新建）— 整个体系的基础，其他 skill 依赖它
2. **P0**: `pb-v1-frontend` 重构 — 移除美学决策，增加前置检查和验证门禁
3. **P1**: `pb-v1-ui-review`（新建）— 美学 Review 闭环
4. **P2**: `design-language-extraction` 扩展 — 增加无参考路径

---

## 六、成功标准

- 给定一个参考网站和功能需求，能产出视觉一致、token 合规、功能完整的页面
- 页面内部不存在两套 CSS 系统并存的情况
- 每个设计决策（颜色、间距、圆角）都能追溯到 token 定义
- 美学 Review 输出的是具体可执行的修复指令，不是主观感受
