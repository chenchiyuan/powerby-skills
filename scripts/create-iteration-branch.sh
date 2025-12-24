#!/bin/bash
# create-iteration-branch.sh
# 创建新的迭代分支，配合P0-P8完整生命周期
# Usage: ./scripts/create-iteration-branch.sh <迭代ID> <项目名>
# Example: ./scripts/create-iteration-branch.sh 001 task-manager

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    cat << EOF
${BLUE}PowerBy 迭代分支创建工具${NC}

${YELLOW}用法:${NC}
  $0 <迭代ID> <项目名> [源分支]

${YELLOW}参数:${NC}
  迭代ID      3位数字，如 001, 002, 003...
  项目名      英文短横线分隔，如 task-manager
  源分支      可选，默认 develop

${YELLOW}示例:${NC}
  $0 001 task-manager
  $0 002 payment-system main
  $0 003 user-authentication develop

${YELLOW}分支类型:${NC}
  feature/{ID}-{项目名}  - P0-P8完整迭代分支

${YELLOW}合并策略:${NC}
  P8完成后 → 合并到 develop → 删除分支

EOF
}

# 检查参数
if [ $# -lt 2 ]; then
    echo -e "${RED}❌ 错误：缺少必需参数${NC}"
    show_help
    exit 1
fi

ITERATION_ID="$1"
PROJECT_NAME="$2"
SOURCE_BRANCH="${3:-develop}"

# 验证迭代ID格式
if ! [[ "$ITERATION_ID" =~ ^[0-9]{3}$ ]]; then
    echo -e "${RED}❌ 错误：迭代ID必须是3位数字（如 001, 002, 010）${NC}"
    exit 1
fi

# 验证项目名称格式
if ! [[ "$PROJECT_NAME" =~ ^[a-z0-9][a-z0-9-]*[a-z0-9]$ ]]; then
    echo -e "${RED}❌ 错误：项目名称必须是英文短横线分隔（如 task-manager）${NC}"
    exit 1
fi

BRANCH_NAME="feature/${ITERATION_ID}-${PROJECT_NAME}"

# 检查分支是否已存在
if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
    echo -e "${RED}❌ 错误：分支 $BRANCH_NAME 已存在${NC}"
    echo -e "${YELLOW}提示：使用以下命令查看分支：${NC}"
    echo "  git branch -a | grep $BRANCH_NAME"
    exit 1
fi

# 检查源分支是否存在
if ! git rev-parse --verify "$SOURCE_BRANCH" >/dev/null 2>&1; then
    echo -e "${RED}❌ 错误：源分支 $SOURCE_BRANCH 不存在${NC}"
    echo -e "${YELLOW}提示：可用的分支：${NC}"
    git branch -a | grep -E "(main|develop)" | head -10
    exit 1
fi

echo -e "${BLUE}🚀 开始创建迭代分支${NC}"
echo -e "  ${YELLOW}迭代ID:${NC} $ITERATION_ID"
echo -e "  ${YELLOW}项目名:${NC} $PROJECT_NAME"
echo -e "  ${YELLOW}分支名:${NC} $BRANCH_NAME"
echo -e "  ${YELLOW}源分支:${NC} $SOURCE_BRANCH"
echo ""

# 切换到源分支并更新
echo -e "${BLUE}📥 切换到源分支 $SOURCE_BRANCH${NC}"
git checkout "$SOURCE_BRANCH" || {
    echo -e "${RED}❌ 切换到源分支失败${NC}"
    exit 1
}

echo -e "${BLUE}⬇️  拉取最新代码${NC}"
git pull origin "$SOURCE_BRANCH" || {
    echo -e "${YELLOW}⚠️  警告：拉取失败，可能需要手动解决冲突${NC}"
}

# 创建新分支
echo -e "${BLUE}🌱 创建新分支 $BRANCH_NAME${NC}"
git checkout -b "$BRANCH_NAME" || {
    echo -e "${RED}❌ 创建分支失败${NC}"
    exit 1
}

# 推送到远程并设置上游分支
echo -e "${BLUE}☁️  推送到远程${NC}"
git push -u origin "$BRANCH_NAME" || {
    echo -e "${RED}❌ 推送到远程失败${NC}"
    echo -e "${YELLOW}提示：可能需要配置远程仓库${NC}"
    exit 1
}

# 创建迭代文档结构
echo -e "${BLUE}📁 创建迭代文档结构${NC}"
ITERATION_DIR="docs/iterations/${ITERATION_ID}-${PROJECT_NAME}"
mkdir -p "$ITERATION_DIR"

# 创建基本文档文件
cat > "$ITERATION_DIR/README.md" << EOF
# 迭代 $ITERATION_ID - $PROJECT_NAME

## 迭代信息
- **迭代ID**: $ITERATION_ID
- **项目名称**: $PROJECT_NAME
- **创建时间**: $(date +%Y-%m-%d)
- **分支**: $BRANCH_NAME
- **源分支**: $SOURCE_BRANCH

## 阶段进度

### P0-P1: 需求定义和澄清
- [ ] 项目宪章
- [ ] PRD文档
- [ ] 功能点清单
- [ ] 澄清记录

### P2-P3: 技术调研和优先级
- [ ] 技术选型分析
- [ ] MVP优先级评估
- [ ] 风险评估

### P4-P5: 架构设计和规划
- [ ] 架构设计
- [ ] 数据模型
- [ ] API契约
- [ ] 任务分解

### P6-P8: 实现、审查和交付
- [ ] 开发实现
- [ ] 代码审查
- [ ] 测试验证
- [ ] 项目交付

## 相关文档
- [PRD](prd.md)
- [架构设计](architecture.md)
- [任务计划](tasks.md)
- [实现报告](implementation.md)

## 分支管理
- **当前分支**: $BRANCH_NAME
- **合并目标**: $SOURCE_BRANCH
- **合并时机**: P8完成后

---
*自动生成于 $(date +%Y-%m-%d %H:%M:%S)*
EOF

cat > "$ITERATION_DIR/status.md" << EOF
# 迭代状态追踪

## 基本信息
- **迭代ID**: $ITERATION_ID
- **分支**: $BRANCH_NAME
- **当前阶段**: P0
- **状态**: active
- **创建时间**: $(date +%Y-%m-%d)

## 阶段进度
| 阶段 | 状态 | 完成时间 | 负责人 |
|------|------|----------|--------|
| P0   | 待开始 | - | - |
| P1   | 待开始 | - | - |
| P3   | 待开始 | - | - |
| P4   | 待开始 | - | - |
| P5   | 待开始 | - | - |
| P6   | 待开始 | - | - |
| P7   | 待开始 | - | - |
| P8   | 待开始 | - | - |

## 分支操作记录
- $(date +%Y-%m-%d %H:%M:%S): 创建分支 $BRANCH_NAME

## 下一步行动
- [ ] 开始P1阶段：需求定义和澄清
- [ ] 使用 /powerby.define 指令

---
*最后更新: $(date +%Y-%m-%d %H:%M:%S)*
EOF

# 添加并提交初始文档
echo -e "${BLUE}💾 提交初始文档${NC}"
git add "$ITERATION_DIR"
git commit -m "docs(iteration): initialize $BRANCH_NAME iteration

- Add iteration structure
- Add status tracking
- Add progress template

Refs #$ITERATION_ID" || {
    echo -e "${YELLOW}⚠️  警告：没有文档变更需要提交${NC}"
}

# 推送到远程
echo -e "${BLUE}☁️  推送初始文档${NC}"
git push origin "$BRANCH_NAME" || {
    echo -e "${YELLOW}⚠️  警告：推送失败${NC}"
}

echo ""
echo -e "${GREEN}✅ 迭代分支创建成功！${NC}"
echo ""
echo -e "${BLUE}📊 分支信息:${NC}"
echo -e "  ${YELLOW}分支名:${NC} $BRANCH_NAME"
echo -e "  ${YELLOW}源分支:${NC} $SOURCE_BRANCH"
echo -e "  ${YELLOW}状态:${NC} active"
echo ""
echo -e "${BLUE}📁 文档结构:${NC}"
echo -e "  └── $ITERATION_DIR/"
echo -e "      ├── README.md (迭代概览)"
echo -e "      └── status.md (状态追踪)"
echo ""
echo -e "${BLUE}🎯 下一步:${NC}"
echo -e "  1. 开始P1阶段：使用 /powerby.define 指令"
echo -e "  2. 在 $BRANCH_NAME 分支上进行开发"
echo -e "  3. P8完成后使用 /powerby.branch.merge 合并分支"
echo ""
echo -e "${YELLOW}💡 提示:${NC}"
echo -e "  查看当前分支: git branch --show-current"
echo -e "  切换分支: git checkout $BRANCH_NAME"
echo -e "  查看分支列表: git branch -a"
echo ""
