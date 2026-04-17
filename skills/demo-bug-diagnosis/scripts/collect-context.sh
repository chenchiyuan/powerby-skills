#!/bin/bash
# collect-context.sh — 收集 Bug 诊断所需的初始证据
#
# 用法: bash scripts/collect-context.sh [error_file] [since_date]
#   error_file: 可选，包含错误信息的文件路径
#   since_date: 可选，起始日期（默认 7 天前），格式 YYYY-MM-DD
#
# 产出: 输出到 stdout，供模型直接消费

set -euo pipefail

ERROR_FILE="${1:-}"
SINCE_DATE="${2:-$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d '7 days ago' +%Y-%m-%d)}"

echo "=== Bug 诊断证据收集 ==="
echo "时间: $(date -Iseconds)"
echo "目录: $(pwd)"
echo ""

# 1. Git 最近变更
echo "--- 最近变更 (since $SINCE_DATE) ---"
if git rev-parse --is-inside-work-tree &>/dev/null; then
    git log --oneline --since="$SINCE_DATE" --no-merges | head -20
    echo ""
    echo "--- 变更文件统计 ---"
    git diff --stat "$(git log --since="$SINCE_DATE" --format=%H | tail -1)..HEAD" 2>/dev/null || echo "(无法获取 diff stat)"
else
    echo "(不在 git 仓库中，跳过)"
fi
echo ""

# 2. 错误文件内容（如提供）
if [[ -n "$ERROR_FILE" && -f "$ERROR_FILE" ]]; then
    echo "--- 错误文件内容: $ERROR_FILE ---"
    head -50 "$ERROR_FILE"
    echo ""
fi

# 3. 最近修改的文件
echo "--- 最近修改的文件 (top 10) ---"
if git rev-parse --is-inside-work-tree &>/dev/null; then
    git diff --name-only HEAD~5..HEAD 2>/dev/null | head -10 || echo "(无法获取)"
else
    find . -type f -newer "$(date -v-1d +%Y%m%d 2>/dev/null || echo '.')" -not -path './.git/*' 2>/dev/null | head -10
fi
echo ""

# 4. 环境信息
echo "--- 环境信息 ---"
echo "OS: $(uname -s) $(uname -r)"
echo "Shell: $SHELL"
[[ -f package.json ]] && echo "Node: $(node --version 2>/dev/null || echo 'N/A')"
[[ -f requirements.txt ]] && echo "Python: $(python3 --version 2>/dev/null || echo 'N/A')"
[[ -f go.mod ]] && echo "Go: $(go version 2>/dev/null || echo 'N/A')"
echo ""

echo "=== 证据收集完成 ==="
