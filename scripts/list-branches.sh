#!/bin/bash
# list-branches.sh
# 查看PowerBy项目分支状态和进度
# Usage: ./scripts/list-branches.sh [选项]
# Options:
#   --type feature|bugfix|hotfix  只显示指定类型的分支
#   --status active|merged|all    显示状态（默认: active）

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 参数解析
FILTER_TYPE=""
FILTER_STATUS="active"

while [[ $# -gt 0 ]]; do
    case $1 in
        --type)
            FILTER_TYPE="$2"
            shift 2
            ;;
        --status)
            FILTER_STATUS="$2"
            shift 2
            ;;
        -h|--help)
            echo -e "${BLUE}PowerBy 分支状态查看工具${NC}"
            echo ""
            echo "查看所有PowerBy相关分支的状态和进度"
            echo ""
            echo "用法:"
            echo "  $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --type <类型>      只显示指定类型的分支 (feature|bugfix|hotfix)"
            echo "  --status <状态>    显示状态 (active|merged|all, 默认: active)"
            echo "  -h, --help         显示此帮助信息"
            echo ""
            echo "示例:"
            echo "  $0                              # 显示所有活跃分支"
            echo "  $0 --type feature               # 只显示feature分支"
            echo "  $0 --status all                 # 显示所有分支（包括已合并）"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 未知选项: $1${NC}"
            echo "使用 -h 或 --help 查看帮助"
            exit 1
            ;;
    esac
done

# 检查是否在git仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ 错误：当前目录不是Git仓库${NC}"
    exit 1
fi

# 获取主分支名称
MAIN_BRANCH=$(git config --get init.defaultBranch 2>/dev/null || echo "main")
if ! git rev-parse --verify "$MAIN_BRANCH" >/dev/null 2>&1; then
    MAIN_BRANCH="master"
fi

# 获取develop分支名称
if git rev-parse --verify develop >/dev/null 2>&1; then
    DEVELOP_BRANCH="develop"
else
    DEVELOP_BRANCH="$MAIN_BRANCH"
fi

# 当前分支
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "未知")

echo -e "${BLUE}📊 PowerBy 项目分支状态报告${NC}"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}📌 项目信息:${NC}"
echo -e "  ${YELLOW}当前分支:${NC} ${GREEN}$CURRENT_BRANCH${NC}"
echo -e "  ${YELLOW}主分支:${NC} $MAIN_BRANCH"
echo -e "  ${YELLOW}开发分支:${NC} $DEVELOP_BRANCH"
echo ""

# 获取分支信息的函数
get_branch_info() {
    local branch=$1
    local branch_type=$(echo "$branch" | cut -d'/' -f1)
    local branch_id=$(echo "$branch" | cut -d'/' -f2)
    local branch_name=$(echo "$branch" | cut -d'/' -f3-)

    # 获取分支状态
    local is_merged=""
    local is_remote=""
    local ahead=0
    local behind=0

    # 检查是否已合并到develop
    if git branch --merged develop 2>/dev/null | grep -q "$branch"; then
        is_merged="已合并"
    elif git branch --merged "$MAIN_BRANCH" 2>/dev/null | grep -q "$branch"; then
        is_merged="已合并"
    else
        is_merged="活跃"
    fi

    # 检查是否远程分支
    if [[ "$branch" == origin/* ]]; then
        is_remote="远程"
        branch=$(echo "$branch" | sed 's|origin/||')
    else
        is_remote="本地"
    fi

    # 获取领先/落后数量
    if [ "$is_remote" = "远程" ]; then
        ahead=$(git rev-list --count "$branch".."$DEVELOP_BRANCH" 2>/dev/null || echo "0")
        behind=$(git rev-list --count "$DEVELOP_BRANCH".."$branch" 2>/dev/null || echo "0")
    else
        local remote_branch="origin/$branch"
        if git rev-parse --verify "$remote_branch" >/dev/null 2>&1; then
            ahead=$(git rev-list --count "$branch".."$remote_branch" 2>/dev/null || echo "0")
            behind=$(git rev-list --count "$remote_branch".."$branch" 2>/dev/null || echo "0")
        fi
    fi

    # 获取最后提交信息
    local last_commit=$(git log -1 --pretty=format:"%h %s (%cr)" "$branch" 2>/dev/null || echo "无提交")

    # 获取分支对应的迭代文档
    local iteration_doc="docs/iterations/$branch_id-$branch_name/README.md 2>/dev/null"
    local stage="未知"
    if [ -f "$iteration_doc" ]; then
        stage=$(grep -A 20 "## 阶段进度" "$iteration_doc" 2>/dev/null | grep -E "^\s*-\s*\[x\]" | wc -l || echo "0")
        if [ "$stage" = "0" ]; then
            stage="P0"
        else
            stage="P$((stage + 1))"
        fi
    fi

    echo -e "${GREEN}├─ $branch${NC}"
    echo -e "   ${YELLOW}类型:${NC} $branch_type | ${YELLOW}状态:${NC} $is_merged | ${YELLOW}位置:${NC} $is_remote"
    echo -e "   ${YELLOW}迭代:${NC} $branch_id | ${YELLOW}项目:${NC} $branch_name | ${YELLOW}阶段:${NC} $stage"
    echo -e "   ${YELLOW}进度:${NC} 领先 $ahead commits, 落后 $behind commits"
    echo -e "   ${YELLOW}最后提交:${NC} $last_commit"
    echo ""
}

# 显示分支列表
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 显示feature分支
if [ -z "$FILTER_TYPE" ] || [ "$FILTER_TYPE" = "feature" ]; then
    echo -e "${MAGENTA}🟢 Feature分支 (P0-P8迭代)${NC}"
    echo ""

    local features=""
    if [ "$FILTER_STATUS" = "active" ]; then
        features=$(git branch 2>/dev/null | grep "^\*.*feature/" | sed 's/^[* ]*//')
        features+=$'\n'$(git branch 2>/dev/null | grep "^\s.*feature/" | grep -v "^\*.*feature/" | sed 's/^[* ]*//')
    elif [ "$FILTER_STATUS" = "merged" ]; then
        features=$(git branch --merged develop 2>/dev/null | grep "feature/" | sed 's/^[* ]*//')
    else
        features=$(git branch -a 2>/dev/null | grep "feature/" | sed 's/^[* ]*//')
    fi

    if [ -z "$features" ]; then
        echo -e "  ${YELLOW}未找到符合条件的feature分支${NC}"
    else
        echo "$features" | while read -r branch; do
            if [ -n "$branch" ]; then
                get_branch_info "$branch"
            fi
        done
    fi
    echo ""
fi

# 显示bugfix分支
if [ -z "$FILTER_TYPE" ] || [ "$FILTER_TYPE" = "bugfix" ]; then
    echo -e "${YELLOW}🟡 Bug修复分支${NC}"
    echo ""

    local bugfixes=""
    if [ "$FILTER_STATUS" = "active" ]; then
        bugfixes=$(git branch 2>/dev/null | grep "^\*.*bugfix/" | sed 's/^[* ]*//')
        bugfixes+=$'\n'$(git branch 2>/dev/null | grep "^\s.*bugfix/" | grep -v "^\*.*bugfix/" | sed 's/^[* ]*//')
    elif [ "$FILTER_STATUS" = "merged" ]; then
        bugfixes=$(git branch --merged develop 2>/dev/null | grep "bugfix/" | sed 's/^[* ]*//')
    else
        bugfixes=$(git branch -a 2>/dev/null | grep "bugfix/" | sed 's/^[* ]*//')
    fi

    if [ -z "$bugfixes" ]; then
        echo -e "  ${YELLOW}未找到符合条件的bugfix分支${NC}"
    else
        echo "$bugfixes" | while read -r branch; do
            if [ -n "$branch" ]; then
                get_branch_info "$branch"
            fi
        done
    fi
    echo ""
fi

# 显示hotfix分支
if [ -z "$FILTER_TYPE" ] || [ "$FILTER_TYPE" = "hotfix" ]; then
    echo -e "${RED}🔴 紧急修复分支${NC}"
    echo ""

    local hotfixes=""
    if [ "$FILTER_STATUS" = "active" ]; then
        hotfixes=$(git branch 2>/dev/null | grep "^\*.*hotfix/" | sed 's/^[* ]*//')
        hotfixes+=$'\n'$(git branch 2>/dev/null | grep "^\s.*hotfix/" | grep -v "^\*.*hotfix/" | sed 's/^[* ]*//')
    elif [ "$FILTER_STATUS" = "merged" ]; then
        hotfixes=$(git branch --merged "$MAIN_BRANCH" 2>/dev/null | grep "hotfix/" | sed 's/^[* ]*//')
    else
        hotfixes=$(git branch -a 2>/dev/null | grep "hotfix/" | sed 's/^[* ]*//')
    fi

    if [ -z "$hotfixes" ]; then
        echo -e "  ${YELLOW}未找到符合条件的hotfix分支${NC}"
    else
        echo "$hotfixes" | while read -r branch; do
            if [ -n "$branch" ]; then
                get_branch_info "$branch"
            fi
        done
    fi
    echo ""
fi

# 统计信息
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 统计各类型分支数量
local feature_count=$(git branch 2>/dev/null | grep -c "feature/" || echo "0")
local bugfix_count=$(git branch 2>/dev/null | grep -c "bugfix/" || echo "0")
local hotfix_count=$(git branch 2>/dev/null | grep -c "hotfix/" || echo "0")

echo -e "${YELLOW}📈 分支统计:${NC}"
echo -e "  ${MAGENTA}Feature分支:${NC} $feature_count 个"
echo -e "  ${YELLOW}Bug修复分支:${NC} $bugfix_count 个"
echo -e "  ${RED}紧急修复分支:${NC} $hotfix_count 个"
echo -e "  ${GREEN}总计:${NC} $((feature_count + bugfix_count + hotfix_count)) 个活跃分支"
echo ""

# 显示主分支状态
echo -e "${YELLOW}🏗️  主分支状态:${NC}"
echo -e "  ${GREEN}main${NC}: $(git log -1 --pretty=format:"%h - %s (%cr)" main 2>/dev/null || echo "无提交")"
echo -e "  ${GREEN}develop${NC}: $(git log -1 --pretty=format:"%h - %s (%cr)" develop 2>/dev/null || echo "无提交")"

# 计算分支间的差异
local ahead_main=$(git rev-list --count develop..main 2>/dev/null || echo "0")
local ahead_develop=$(git rev-list --count main..develop 2>/dev/null || echo "0")

echo -e "  ${YELLOW}分支差异:${NC} develop领先main $ahead_develop commits, main领先develop $ahead_main commits"
echo ""

# 提示信息
echo -e "${CYAN}💡 常用命令:${NC}"
echo -e "  ${BLUE}查看所有分支:${NC} git branch -a"
echo -e "  ${BLUE}查看已合并分支:${NC} git branch --merged develop"
echo -e "  ${BLUE}查看未合并分支:${NC} git branch --no-merged develop"
echo -e "  ${BLUE}创建新迭代分支:${NC} ./scripts/create-iteration-branch.sh <ID> <项目名>"
echo -e "  ${BLUE}清理已合并分支:${NC} ./scripts/cleanup-branches.sh"
echo ""

# 过滤提示
if [ -n "$FILTER_TYPE" ] || [ "$FILTER_STATUS" != "active" ]; then
    echo -e "${YELLOW}🔍 当前过滤条件:${NC}"
    [ -n "$FILTER_TYPE" ] && echo -e "  ${YELLOW}类型:${NC} $FILTER_TYPE"
    [ "$FILTER_STATUS" != "active" ] && echo -e "  ${YELLOW}状态:${NC} $FILTER_STATUS"
    echo ""
    echo -e "${BLUE}显示所有分支:${NC} $0 --status all"
    echo ""
fi

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
