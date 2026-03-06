# Proposal: ASP 迭代编号体系

## 1. 产品定位
- **目标用户**：使用 PowerBy Skills 的开发者/架构师
- **核心价值**：让 ASP 流程的迭代文档与 P0-P8 流程共享统一编号体系，文档顺序一目了然
- **成功指标**：ASP 流程启动时能自动递增编号、创建迭代目录，并与已有文档兼容共存

## 2. 需求清单
| ID | 需求描述 | 优先级 | 验收标准（草案） |
|----|---------|--------|----------------|
| REQ-001 | `/powerby-asp` 启动时从 `iterations.json` 读取最大编号 +1，创建新迭代目录并写入记录 | 必须 | 新迭代编号正确递增，目录 `docs/iterations/{id}-{name}/` 创建成功，`iterations.json` 更新 |
| REQ-002 | `/powerby-asp` 支持复用已有迭代目录（用户指定继续某个迭代） | 必须 | 指定已有编号时不新建目录，直接使用已有目录继续流程 |
| REQ-003 | `/powerby-asp-arch` 启动时要求指定已有迭代目录，不新建 | 必须 | 检查目录下存在 ASP 产品交付物（proposal.md、spec.md、function-points.md），缺失时提示用户补全 |
| REQ-004 | 迭代名从用户需求描述中自动提取为 kebab-case 英文短名 | 应该 | 自动生成合理的短名，用户可确认或修改 |
| REQ-005 | ASP 文档与 P0-P8 文档在同一迭代目录下兼容共存 | 必须 | 不覆盖已有的 P0-P8 文档（prd.md、clarifications.md 等），ASP 文档正常写入 |

## 3. 明确排除
| ID | 排除项 | 排除理由 |
|----|--------|---------|
| EXC-001 | 不改动 P0-P8 流程的 skill 文件 | 范围限定，只更新 ASP 相关 skill |
| EXC-002 | 不改动 reviewer/visualizer 等子 skill | 它们只关心迭代目录路径，不涉及编号逻辑 |
| EXC-003 | 不改动 `iterations.json` 数据结构 | 沿用现有字段结构 |

## 4. 约束条件
| ID | 约束描述 |
|----|---------|
| CON-001 | 只修改 `powerby-asp.md` 和 `powerby-asp-arch.md` 两个 skill 文件 |
| CON-002 | 编号体系与 P0-P8 共享同一序号空间，不能冲突 |
