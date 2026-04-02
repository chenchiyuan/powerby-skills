# 009 Review Framework 当前验收状态

## 已通过

- [x] 有正式整改计划：`remediation-plan.md`
- [x] 有可执行 runner：`skills/pb-review/scripts/review_runner.py`
- [x] 有 `.review/` 持久化与 checkpoint
- [x] 8 个下游 skill 已有 `scripts/run.py`
- [x] `powerby-skills` 仓库可真实跑出 `.review/review_report.md`
- [x] Python 运行时脚本通过 `py_compile`
- [x] skill 结构校验通过
- [x] `product-reconstructor` / `feature-reconstructor` / `relation-builder` / `gap-analyzer` 已改为 `SKILL.md + task-contract + examples + failure-modes` 驱动
- [x] 4 个核心抽象 skill 已移除 `strategy.json`，改为 skill-contract 执行
- [x] 校验器已开始拦截典型硬编码回退，并要求抽象 skill 通过 `run_skill_contract` 执行
- [x] 运行入口已支持用户显式提供 `product_docs_dir`，上游不再默认把全仓库文档当产品证据
- [x] `product-reconstructor` 已取消“无 product_facts 时回退到全仓库 doc”的旧行为，产品还原只消费用户指定目录命中的证据
- [x] 已移除 `pb-review` 内部后端 LLM HTTP 调用；抽象四层改为由 Codex/Claude 直接执行 skill，本地脚本只保留确定性步骤

## 部分通过

- [~] REQ-003 ~ REQ-010 已从“纯文档定义”提升为“skill 直接执行 + 本地确定性脚本辅助”的闭环，且产品证据边界已改为用户显式指定目录，但 live 结果质量仍需继续收敛
- [~] Skill 文本已补 `compatibility`、三句式、examples、subtask guidance，但与 `skill_demo.md` 相比仍偏简
- [~] Demo 已有 1 个真实案例，尚缺第 2 个案例

## 未通过

- [ ] 第二个 demo 仓库
- [ ] baseline vs with skill 评估文档
- [ ] 面向复杂仓库的抽取质量优化
- [ ] 更强的语义对齐策略，替代当前词项重叠式 Feature State / Relation 推断

## 当前判定

009 当前不再是“只有 prompt 壳”的玩具实现，也不再主要依赖本地硬编码匹配。  
但它也还不能被判定为“完整交付”。更准确的状态是：

**Batch 1 已完成，Batch 2 已打通且完成核心去硬编码重构，Batch 3 / Batch 4 仍需继续推进。**
