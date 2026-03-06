# 功能点清单: ASP 迭代编号体系

## 总览

| FP | REQ | 功能名称 | 优先级 | 一句话描述 |
|----|-----|---------|--------|-----------|
| FP-001 | REQ-001 | 自动递增编号创建迭代 | 必须 | ASP 启动时从 json+目录取最大编号 +1，创建新迭代目录并写入记录 |
| FP-002 | REQ-002 | 复用已有迭代目录 | 必须 | 支持指定已有迭代编号继续流程，按文件判断恢复阶段 |
| FP-003 | REQ-003 | 架构流程指定迭代 | 必须 | asp-arch 启动时指定已有迭代，检查产品交付物完整性 |
| FP-004 | REQ-004 | 自动提取迭代名 | 应该 | 从需求描述中提取 kebab-case 英文短名，用户可确认或修改 |
| FP-005 | REQ-005 | ASP 与 P0-P8 文档兼容共存 | 必须 | 两套文档在同一迭代目录下互不覆盖 |

## 详情

### 必须（核心）

#### FP-001 → REQ-001: 自动递增编号创建迭代
- 读取 `.powerby/iterations.json` 和扫描 `docs/iterations/` 目录
- 取 max(json 最大编号, 目录最大编号) + 1 作为新编号
- 创建 `docs/iterations/{id}-{name}/` 和 `prd_logs/` 子目录
- 写入 `iterations.json` 新记录
- 验收：编号正确递增，目录创建成功，json 更新

#### FP-002 → REQ-002: 复用已有迭代目录
- 用户指定已有编号时不新建目录
- 按文件→阶段映射表判断恢复点：无文件→DISCOVERY，仅 proposal→DRAFTING，有 spec→REFINING，有 product-map+function-points→CONFIRMATION
- 迭代不存在时提示，json 无记录时自动补录
- 验收：正确恢复到对应阶段

#### FP-003 → REQ-003: 架构流程指定迭代
- `/powerby-asp-arch` 不创建新迭代，要求指定已有编号
- 检查目录下存在 proposal.md、spec.md、function-points.md
- 缺失时逐一列出并提示补全
- 未指定编号时列出所有迭代供选择
- 验收：交付物完整时正常进入架构流程，缺失时终止并提示

#### FP-005 → REQ-005: ASP 与 P0-P8 文档兼容共存
- ASP 文档（proposal.md、spec.md 等）写入时不覆盖已有 P0-P8 文档（prd.md、clarifications.md 等）
- 两套文档在同一目录下共存
- 验收：互不覆盖，各自正常读写

### 应该

#### FP-004 → REQ-004: 自动提取迭代名
- 从用户需求描述中提取核心主题词
- 转换为 kebab-case 英文短名
- 向用户展示并等待确认或修改
- 验收：自动生成合理短名，用户可修改
