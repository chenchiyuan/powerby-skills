# Bug-Fix Report #{id} - [问题简述]

## 一、问题报告
### 问题描述
[简明扼要描述问题表现]

### 证据链
- 错误日志: [具体日志内容]
- 堆栈信息: [异常堆栈]
- 代码片段: [相关代码]
- 环境信息: [系统/版本等]

### 复现逻辑
[详细描述如何稳定复现该问题]

### 影响评估
- 影响范围: [影响的功能/模块]
- 严重程度: P0/P1/P2
- 紧急程度: 高/中/低

---

## 二、诊断分析
### 代码路径分析
[Mermaid流程图描述执行路径]

### 根因定位
[明确指出问题根本原因]

### 影响范围
[分析是否影响其他模块]

### 修复建议
[初步修复思路]

---

## 三、修复计划
### 修复方案
[记录最终选择的修复方案]

### 任务清单
- [ ] TASK-{id}-001: [具体修复任务1]
  - 描述: [详细描述]
  - 优先级: P0/P1/P2
  - 预估工时: X小时
  - 验收标准: [具体标准]
  - 状态: 待开始/进行中/已完成

- [ ] TASK-{id}-002: [具体修复任务2]
  - 描述: [详细描述]
  - 优先级: P0/P1/P2
  - 预估工时: X小时
  - 验收标准: [具体标准]
  - 状态: 待开始/进行中/已完成

### 风险评估
- 潜在风险: [可能引入的新问题]
- 缓解措施: [如何避免风险]

---

## 四、实施修复
### 执行记录
[记录实际执行过程，与计划对比]

### 临时文件使用记录
本次修复过程中创建了以下临时文件：

#### 分析脚本
- `temp_scripts/analysis/bug-{id}-code-analyzer.{py|js|sh}` - [用途说明]
- `temp_scripts/logs/bug-{id}-analysis.log` - [分析结果说明]

#### 验证脚本
- `temp_scripts/validation/bug-{id}-test-{component}.{py|js}` - [用途说明]
- `temp_scripts/validation/bug-{id}-regression-check.{py|js|sh}` - [用途说明]

#### 模拟数据
- `temp_scripts/mock/bug-{id}-test-data.{json|csv|yaml}` - [数据说明]
- `temp_scripts/mock/bug-{id}-scenario-{name}.{py|js}` - [场景说明]

#### 清理状态
- [ ] 分析脚本已删除
- [ ] 验证脚本已删除
- [ ] 模拟数据已删除
- [ ] 临时日志已删除
- [ ] temp_scripts目录已清理（如果为空）

### 修改明细
[列出所有代码修改]

---

## 五、验证交付
### 回归测试
[证明修复有效]

### 防御性变更
[是否添加了断言或快速失败逻辑]

### 代码交付
```diff
[提供diff格式的代码变更]
```

### 临时文件清理验证
**清理检查清单**：
- [ ] `temp_scripts/analysis/` 目录已清空
- [ ] `temp_scripts/validation/` 目录已清空
- [ ] `temp_scripts/mock/` 目录已清空
- [ ] `temp_scripts/logs/` 目录已清空
- [ ] `temp_scripts/` 目录已删除（如果为空）
- [ ] 工作目录整洁，无遗留临时文件
- [ ] 项目目录结构完整

**清理命令记录**：
```bash
# 示例清理命令
find temp_scripts -name "*bug-{id}*" -type f -delete
find temp_scripts -type d -empty -delete
[ -d temp_scripts ] && [ -z "$(ls -A temp_scripts)" ] && rmdir temp_scripts
```

### 总结
- 修复时间: [实际用时]
- 效果验证: [是否完全解决]
- 临时文件: [已清理/未清理（说明原因）]
- 经验总结: [学到的教训]
