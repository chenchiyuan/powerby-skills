#!/bin/bash
# validate-report.sh — 诊断报告结构完整性校验（Sensor / 反馈控制）
#
# 用法: bash scripts/validate-report.sh <report_file>
#
# 校验规则（确定性判断，代码接管）：
#   1. 必填 Section 是否存在
#   2. 根因字段是否非空
#   3. 证据链是否至少有一条
#   4. 最小复现是否非空
#
# 退出码: 0 = 通过, 1 = 失败

set -euo pipefail

REPORT_FILE="${1:-}"

if [[ -z "$REPORT_FILE" ]]; then
    echo "用法: bash scripts/validate-report.sh <report_file>"
    exit 1
fi

if [[ ! -f "$REPORT_FILE" ]]; then
    echo "FAIL: 报告文件不存在: $REPORT_FILE"
    exit 1
fi

ERRORS=()

# 1. 必填 Section 检查
REQUIRED_SECTIONS=("症状描述" "预期行为" "根因" "证据链" "最小复现" "已排除项")
for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "## $section" "$REPORT_FILE"; then
        ERRORS+=("缺少必填 Section: ## $section")
    fi
done

# 2. 根因字段非空检查（排除 HTML 注释和方括号占位符）
ROOT_CAUSE=$(sed -n '/^## 根因/,/^## /p' "$REPORT_FILE" | grep -v '^## ' | grep -v '^$' | grep -v '^<!--' | grep -v '^\[' | head -1 || true)
if [[ -z "$ROOT_CAUSE" ]]; then
    ERRORS+=("根因字段为空或未填写（仍为模板占位符）")
fi

# 3. 证据链至少一条（排除方括号占位符行）
EVIDENCE_LINES=$(sed -n '/^## 证据链/,/^## /p' "$REPORT_FILE" | grep '^[0-9]' || true)
EVIDENCE_COUNT=0
if [[ -n "$EVIDENCE_LINES" ]]; then
    # 过滤掉仍为模板占位符的行（包含 [操作] [发现] 等）
    EVIDENCE_COUNT=$(echo "$EVIDENCE_LINES" | grep -cv '\[操作\]\|\[发现\]\|\[排除\]\|\[确认根因\]' || true)
fi
if [[ "$EVIDENCE_COUNT" -lt 1 ]]; then
    ERRORS+=("证据链为空或仍为模板占位符，至少需要一条真实证据")
fi

# 4. 最小复现非空检查（排除 HTML 注释、方括号占位符和空代码块）
REPRO=$(sed -n '/^## 最小复现/,/^## /p' "$REPORT_FILE" | grep -v '^## ' | grep -v '^$' | grep -v '^<!--' | grep -v '^```' | grep -v '^# 复现命令' | grep -v '^\[' | head -1 || true)
if [[ -z "$REPRO" ]]; then
    ERRORS+=("最小复现字段为空或未填写（仍为模板占位符）")
fi

# 输出结果
echo "=== 诊断报告校验 ==="
echo "文件: $REPORT_FILE"
echo ""

if [[ ${#ERRORS[@]} -eq 0 ]]; then
    echo "PASS: 所有校验通过"
    echo "  - ${#REQUIRED_SECTIONS[@]} 个必填 Section 齐全"
    echo "  - 根因字段已填写"
    echo "  - 证据链包含 $EVIDENCE_COUNT 条证据"
    echo "  - 最小复现已填写"
    exit 0
else
    echo "FAIL: 发现 ${#ERRORS[@]} 个问题"
    for err in "${ERRORS[@]}"; do
        echo "  ✗ $err"
    done
    exit 1
fi
