#!/bin/bash
# cleanup-branches.sh
# 清理已合并的分支，保持仓库整洁
# Usage: ./scripts/cleanup-branches.sh [选项]
# Options:
#   --dry-run    仅显示要清理的分支，不实际删除
#   --force      强制删除，不询问确认

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 参数解析
DRY_RUN=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            echo -e "${BLUE}PowerBy 分支清理工具${NC}"
            echo ""
            echo "清理已合并到主分支的feature、bugfix、hotfix分支"
            echo ""
            echo "用法:"
            echo "  $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --dry-run    仅显示要清理的分支，不实际删除"
            echo "  --force      强制删除，不询问确认"
            echo "  -h, --help   显示此帮助信息"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 未知选项: $1${NC}"
            echo "使用 -h 或 --help 查看帮助"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🧹 PowerBy 分支清理工具${NC}"
echo ""

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

echo -e "${BLUE}📊 分支配置:${NC}"
echo -e "  ${YELLOW}主分支:${NC} $MAIN_BRANCH"
echo -e "  ${YELLOW}开发分支:${NC} $DEVELOP_BRANCH"
echo ""

# 要清理的分支类型和对应的合并目标
declare -A BRANCH_PATTERNS=(
    ["feature"]="$DEVELOP_BRANCH"
    ["bugfix"]="$DEVELOP_BRANCH"
    ["hotfix"]="$MAIN_BRANCH"
)

TOTAL_CLEANED=0
TOTAL_LOCAL=0
TOTAL_REMOTE=0

# 清理函数
cleanup_branches() {
    local pattern=$1
    local merge_target=$2
    local type=$3

    echo -e "${BLUE}🔍 查找已合并的 $type 分支...${NC}"

    # 查找已合并到develop的本地分支（除了develop本身）
    local merged_local=$(git branch --merged "$merge_target" 2>/dev/null | \
        grep "^[* ]*$pattern/" | \
        grep -v "$merge_target" | \
        sed 's/^[* ]*//' || true)

    if [ -z "$merged_local" ]; then
        echo -e "  ${YELLOW}未找到已合并的本地 $type 分支${NC}"
    else
        echo -e "  ${GREEN}找到 ${TOTAL_LOCAL} 个已合并的本地 $type 分支:${NC}"
        echo "$merged_local" | while read -r branch; do
            echo -e "    - $branch"
            TOTAL_LOCAL=$((TOTAL_LOCAL + 1))

            if [ "$DRY_RUN" = false ]; then
                if [ "$FORCE" = true ] || [ -t 0 ]; then
                    echo -e "  ${YELLOW}删除本地分支: $branch${NC}"
                    git branch -d "$branch" 2>/dev/null || {
                        echo -e "    ${RED}删除失败，可能需要强制删除${NC}"
                        echo -e "    ${YELLOW}提示: git branch -D $branch${NC}"
                    }
                else
                    read -p "  删除本地分支 $branch? [y/N]: " -n 1 -r
                    echo
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        echo -e "  ${YELLOW}删除本地分支: $branch${NC}"
                        git branch -d "$branch" 2>/dev/null || {
                            echo -e "    ${RED}删除失败${NC}"
                        }
                    fi
                fi
            fi
        done
    fi

    # 查找远程已合并的分支
    local merged_remote=$(git branch -r --merged "$merge_target" 2>/dev/null | \
        grep "origin/$pattern/" | \
        sed 's/^[* ]*//' | \
        sed 's|origin/||' || true)

    if [ -z "$merged_remote" ]; then
        echo -e "  ${YELLOW}未找到已合并的远程 $type 分支${NC}"
    else
        echo -e "  ${GREEN}找到 ${TOTAL_REMOTE} 个已合并的远程 $type 分支:${NC}"
        echo "$merged_remote" | while read -r branch; do
            echo -e "    - origin/$branch"
            TOTAL_REMOTE=$((TOTAL_REMOTE + 1))

            if [ "$DRY_RUN" = false ]; then
                if [ "$FORCE" = true ] || [ -t 0 ]; then
                    echo -e "  ${YELLOW}删除远程分支: origin/$branch${NC}"
                    git push origin --delete "$branch" 2>/dev/null || {
                        echo -e "    ${RED}删除失败${NC}"
                    }
                else
                    read -p "  删除远程分支 origin/$branch? [y/N]: " -n 1 -r
                    echo
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        echo -e "  ${YELLOW}删除远程分支: origin/$branch${NC}"
                        git push origin --delete "$branch" 2>/dev/null || {
                            echo -e "    ${RED}删除失败${NC}"
                        }
                    fi
                fi
            fi
        done
    fi

    echo ""
}

# 执行清理
echo -e "${YELLOW}开始清理已合并的分支...${NC}"
echo ""

for pattern in "${!BRANCH_PATTERNS[@]}"; do
    merge_target="${BRANCH_PATTERNS[$pattern]}"
    case $pattern in
        "feature") type="功能" ;;
        "bugfix") type="Bug修复" ;;
        "hotfix") type="紧急修复" ;;
    esac

    cleanup_branches "$pattern" "$merge_target" "$type"
done

# 清理远程过期分支引用
echo -e "${BLUE}🧹 清理远程过期分支引用${NC}"
git remote prune origin 2>/dev/null || {
    echo -e "  ${YELLOW}⚠️  警告：清理远程分支引用失败${NC}"
}

# 显示结果
echo ""
echo -e "${GREEN}✅ 分支清理完成！${NC}"
echo ""
echo -e "${BLUE}📊 清理统计:${NC}"
echo -e "  ${YELLOW}本地分支清理:${NC} ${TOTAL_LOCAL} 个"
echo -e "  ${YELLOW}远程分支清理:${NC} ${TOTAL_REMOTE} 个"
echo -e "  ${YELLOW}总计清理:${NC} $((TOTAL_LOCAL + TOTAL_REMOTE)) 个"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}💡 这是试运行模式，未实际删除任何分支${NC}"
    echo ""
    echo -e "${BLUE}执行实际清理:${NC}"
    echo "  $0"
    echo ""
    echo -e "${BLUE}强制清理（不询问）:${NC}"
    echo "  $0 --force"
else
    # 显示剩余活跃分支
    echo -e "${BLUE}📋 当前活跃分支:${NC}"

    # 活跃的feature分支
    local active_features=$(git branch --show-current 2>/dev/null)
    echo -e "  ${YELLOW}当前分支:${NC} $active_features"

    # 其他活跃分支
    local other_branches=$(git branch 2>/dev/null | grep -v "^\*" | grep -E "(feature|bugfix|hotfix)/" | sed 's/^[* ]*//' || true)
    if [ -n "$other_branches" ]; then
        echo -e "  ${YELLOW}其他活跃分支:${NC}"
        echo "$other_branches" | while read -r branch; do
            echo -e "    - $branch"
        done
    fi

    echo ""
    echo -e "${YELLOW}💡 提示:${NC}"
    echo -e "  查看所有分支: git branch -a"
    echo -e "  查看已合并分支: git branch --merged $DEVELOP_BRANCH"
    echo -e "  查看未合并分支: git branch --no-merged $DEVELOP_BRANCH"
fi

echo ""
