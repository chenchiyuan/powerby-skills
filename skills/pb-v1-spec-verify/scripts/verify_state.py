#!/usr/bin/env python3
"""
pb-v1-spec-verify 验证状态管理脚本

确定性工作下沉到脚本：
- 读写 verify-state.json（状态快照）
- 计算收敛指标（PASS/FAIL/SKIP 统计）
- 检查收敛条件（FAIL 是否减少、轮次是否超限）

用法:
    python verify_state.py init <state_file> <spec_index_file>
    python verify_state.py load <state_file>
    python verify_state.py update <state_file> <spec_id> <dimension> <status> [--evidence <evidence>] [--severity <severity>]
    python verify_state.py check <state_file>
    python verify_state.py save <state_file>
    python verify_state.py summary <state_file>

绝不做语义判断、绝不做需要理解上下文的决策。
"""

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALID_DIM_STATUSES = {"PASS", "FAIL", "SKIP", "PENDING"}
VALID_SPEC_STATUSES = {"PASS", "FAIL", "ESCALATED", "PENDING"}
VALID_SEVERITIES = {"BLOCKER", "MAJOR", "MINOR", None}
MAX_ROUNDS = 3
ALL_DIMENSIONS = [f"D-{i:02d}" for i in range(1, 21)]


def create_initial_state(spec_index_path: str) -> dict[str, Any]:
    """从 spec index 创建初始验证状态。

    读取 feature-spec-index.md 中的 spec 清单，
    为每张 spec 卡片创建初始状态（所有维度 PENDING）。
    """
    specs = _parse_spec_index(spec_index_path)
    state = {
        "version": "1.0.0",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "round": 0,
        "convergence_history": [],
        "specs": {},
    }
    for spec in specs:
        spec_id = spec["id"]
        state["specs"][spec_id] = {
            "name": spec["name"],
            "priority": spec["priority"],
            "status": "PENDING",
            "dimensions": {
                dim: {"status": "PENDING", "severity": None, "evidence": None, "test": None}
                for dim in ALL_DIMENSIONS
            },
        }
    return state


def _parse_spec_index(path: str) -> list[dict[str, str]]:
    """解析 feature-spec-index.md，提取 spec 卡片列表。

    支持 Markdown 表格格式，提取 Spec ID、名称和优先级。
    """
    specs = []
    if not os.path.exists(path):
        print(f"Error: spec index file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("---"):
            if in_table and not stripped:
                in_table = False
            continue

        if "|" in stripped:
            cells = [c.strip() for c in stripped.split("|")]
            cells = [c for c in cells if c]

            # 跳过表头分隔行
            if cells and all(set(c) <= set("- :") for c in cells):
                in_table = True
                continue

            # 尝试解析 spec 行
            if len(cells) >= 3 and cells[0].startswith("F-"):
                spec_id = cells[0]
                name = cells[1]
                priority = cells[2] if len(cells) > 2 else "P1"
                specs.append({
                    "id": spec_id,
                    "name": name,
                    "priority": priority,
                })
                in_table = True

    return specs


def load_state(state_file: str) -> dict[str, Any]:
    """加载验证状态快照。"""
    if not os.path.exists(state_file):
        print(f"Error: state file not found: {state_file}", file=sys.stderr)
        sys.exit(1)

    with open(state_file, encoding="utf-8") as f:
        state = json.load(f)

    print(f"Loaded state: round {state['round']}, "
          f"{len(state['specs'])} specs")
    _print_summary(state)
    return state


def save_state(state: dict[str, Any], state_file: str) -> None:
    """保存验证状态快照。"""
    state["updated_at"] = _now_iso()
    os.makedirs(os.path.dirname(state_file) or ".", exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"State saved to {state_file}")


def update_dimension(
    state: dict[str, Any],
    spec_id: str,
    dimension: str,
    status: str,
    evidence: str | None = None,
    test: str | None = None,
    severity: str | None = None,
) -> None:
    """更新单个维度的验证状态。"""
    if spec_id not in state["specs"]:
        print(f"Error: spec {spec_id} not found in state", file=sys.stderr)
        sys.exit(1)

    if dimension not in ALL_DIMENSIONS:
        print(f"Error: invalid dimension {dimension}", file=sys.stderr)
        sys.exit(1)

    if status not in VALID_DIM_STATUSES:
        print(f"Error: invalid status {status}. "
              f"Valid: {VALID_DIM_STATUSES}", file=sys.stderr)
        sys.exit(1)

    if severity is not None and severity not in {"BLOCKER", "MAJOR", "MINOR"}:
        print(f"Error: invalid severity {severity}. "
              f"Valid: BLOCKER, MAJOR, MINOR", file=sys.stderr)
        sys.exit(1)

    dim_state = state["specs"][spec_id]["dimensions"][dimension]
    dim_state["status"] = status
    if evidence is not None:
        dim_state["evidence"] = evidence
    if test is not None:
        dim_state["test"] = test
    # severity: FAIL 时必须设置，PASS/SKIP 时清除
    if status == "FAIL":
        dim_state["severity"] = severity  # 调用方负责传入
    else:
        dim_state["severity"] = None

    # 更新 spec 整体状态
    _recalculate_spec_status(state, spec_id)
    print(f"Updated {spec_id}/{dimension} -> {status}"
          f"{f' ({severity})' if severity else ''}")


def check_convergence(state: dict[str, Any]) -> dict[str, Any]:
    """检查收敛条件，返回收敛报告。"""
    current = _count_statuses(state)
    severity_counts = _count_severities(state)
    state["round"] += 1
    round_num = state["round"]

    result = {
        "round": round_num,
        "timestamp": _now_iso(),
        "pass_count": current["PASS"],
        "fail_count": current["FAIL"],
        "skip_count": current["SKIP"],
        "pending_count": current["PENDING"],
        "total_dimensions": current["total"],
        "blocker_count": severity_counts["BLOCKER"],
        "major_count": severity_counts["MAJOR"],
        "minor_count": severity_counts["MINOR"],
        "verdict": "",
        "converged": False,
        "should_stop": False,
        "reason": "",
    }

    # PASS: 0 BLOCKER + 0 MAJOR（机械规则）
    if severity_counts["BLOCKER"] == 0 and severity_counts["MAJOR"] == 0 and current["PENDING"] == 0:
        result["converged"] = True
        result["verdict"] = "PASS"
        result["reason"] = "PASS: 0 BLOCKER, 0 MAJOR"
        state["convergence_history"].append(result)
        _print_convergence(result, state)
        return result

    # 检查 FAIL 是否减少
    if state["convergence_history"]:
        prev = state["convergence_history"][-1]
        prev_fail = prev["fail_count"]
        if current["FAIL"] >= prev_fail:
            result["should_stop"] = True
            result["verdict"] = "FAIL"
            result["reason"] = (
                f"STALLED: FAIL 数量未减少 "
                f"(上轮 {prev_fail}, 本轮 {current['FAIL']})"
            )
            state["convergence_history"].append(result)
            _print_convergence(result, state)
            return result

    # 检查轮次
    if round_num >= MAX_ROUNDS:
        result["should_stop"] = True
        result["verdict"] = "ESCALATED"
        result["reason"] = f"ESCALATED: 已达最大轮次 {MAX_ROUNDS}，仍有 {severity_counts['BLOCKER']} BLOCKER, {severity_counts['MAJOR']} MAJOR"
        state["convergence_history"].append(result)
        _print_convergence(result, state)
        return result

    # 可以继续
    result["verdict"] = "FAIL"
    result["reason"] = (
        f"CONTINUE: FAIL 从上轮减少，继续收敛 "
        f"(本轮 {current['FAIL']} FAIL, "
        f"{severity_counts['BLOCKER']} BLOCKER, {severity_counts['MAJOR']} MAJOR, "
        f"轮次 {round_num}/{MAX_ROUNDS})"
    )
    state["convergence_history"].append(result)
    _print_convergence(result, state)
    return result


def print_summary(state: dict[str, Any]) -> None:
    """打印验证状态摘要。"""
    _print_summary(state)


# --- 内部辅助函数 ---


def _count_statuses(state: dict[str, Any]) -> dict[str, int]:
    """统计所有维度的状态计数。"""
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0, "PENDING": 0, "total": 0}
    for spec in state["specs"].values():
        for dim in spec["dimensions"].values():
            status = dim["status"]
            counts[status] = counts.get(status, 0) + 1
            counts["total"] += 1
    return counts


def _count_severities(state: dict[str, Any]) -> dict[str, int]:
    """统计所有 FAIL 维度的严重度计数。"""
    counts = {"BLOCKER": 0, "MAJOR": 0, "MINOR": 0}
    for spec in state["specs"].values():
        for dim in spec["dimensions"].values():
            if dim["status"] == "FAIL" and dim.get("severity"):
                counts[dim["severity"]] = counts.get(dim["severity"], 0) + 1
    return counts


def _recalculate_spec_status(state: dict[str, Any], spec_id: str) -> None:
    """根据维度状态和严重度重算 spec 整体状态。

    使用与 pb-v1-reviewer 一致的机械规则：
    - PASS = 0 BLOCKER + 0 MAJOR（该 spec 内）
    - FAIL = 有 BLOCKER 或 MAJOR
    - PENDING = 仍有 PENDING 维度
    """
    spec = state["specs"][spec_id]
    dims = spec["dimensions"]

    has_pending = any(d["status"] == "PENDING" for d in dims.values())
    has_blocker = any(
        d["status"] == "FAIL" and d.get("severity") == "BLOCKER"
        for d in dims.values()
    )
    has_major = any(
        d["status"] == "FAIL" and d.get("severity") == "MAJOR"
        for d in dims.values()
    )

    if has_pending:
        spec["status"] = "PENDING"
    elif has_blocker or has_major:
        spec["status"] = "FAIL"
    else:
        spec["status"] = "PASS"


def _print_summary(state: dict[str, Any]) -> None:
    """打印状态摘要。"""
    counts = _count_statuses(state)
    severity_counts = _count_severities(state)
    spec_statuses = {}
    for spec in state["specs"].values():
        s = spec["status"]
        spec_statuses[s] = spec_statuses.get(s, 0) + 1

    print("\n=== 验证状态摘要 ===")
    print(f"轮次: {state['round']}")
    print(f"Spec 卡片: {len(state['specs'])} 张")
    for status, count in sorted(spec_statuses.items()):
        print(f"  {status}: {count}")
    print(f"维度统计:")
    print(f"  PASS: {counts['PASS']}")
    print(f"  FAIL: {counts['FAIL']}")
    print(f"    BLOCKER: {severity_counts['BLOCKER']}")
    print(f"    MAJOR: {severity_counts['MAJOR']}")
    print(f"    MINOR: {severity_counts['MINOR']}")
    print(f"  SKIP: {counts['SKIP']}")
    print(f"  PENDING: {counts['PENDING']}")
    print(f"  总计: {counts['total']}")


def _print_convergence(
    result: dict[str, Any], state: dict[str, Any]
) -> None:
    """打印收敛检查结果。"""
    print(f"\n=== 收敛检查 Round {result['round']} ===")
    print(f"PASS: {result['pass_count']}, FAIL: {result['fail_count']}, "
          f"SKIP: {result['skip_count']}, PENDING: {result['pending_count']}")
    print(f"BLOCKER: {result['blocker_count']}, "
          f"MAJOR: {result['major_count']}, "
          f"MINOR: {result['minor_count']}")
    print(f"Verdict: {result['verdict']}")

    if result["converged"]:
        print(f"CONVERGED: {result['reason']}")
    elif result["should_stop"]:
        print(f"STOP: {result['reason']}")
    else:
        print(f"{result['reason']}")

    # 打印收敛历史表
    if len(state["convergence_history"]) > 1:
        print("\n收敛历史:")
        print("| 轮次 | PASS | FAIL | SKIP | BLOCKER | MAJOR | MINOR | Verdict |")
        print("|------|------|------|------|---------|-------|-------|---------|")
        for entry in state["convergence_history"]:
            print(
                f"| {entry['round']} "
                f"| {entry['pass_count']} "
                f"| {entry['fail_count']} "
                f"| {entry['skip_count']} "
                f"| {entry.get('blocker_count', '-')} "
                f"| {entry.get('major_count', '-')} "
                f"| {entry.get('minor_count', '-')} "
                f"| {entry.get('verdict', '-')} |"
            )


def _now_iso() -> str:
    """返回 ISO8601 时间字符串。"""
    return datetime.now(timezone.utc).isoformat()


# --- CLI ---


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) < 4:
            print("Usage: verify_state.py init <state_file> <spec_index_file>",
                  file=sys.stderr)
            sys.exit(1)
        state_file = sys.argv[2]
        spec_index = sys.argv[3]
        state = create_initial_state(spec_index)
        save_state(state, state_file)

    elif command == "load":
        if len(sys.argv) < 3:
            print("Usage: verify_state.py load <state_file>", file=sys.stderr)
            sys.exit(1)
        load_state(sys.argv[2])

    elif command == "update":
        if len(sys.argv) < 6:
            print(
                "Usage: verify_state.py update <state_file> <spec_id> "
                "<dimension> <status> [--evidence <e>] [--test <t>] [--severity <s>]",
                file=sys.stderr,
            )
            sys.exit(1)
        state_file = sys.argv[2]
        spec_id = sys.argv[3]
        dimension = sys.argv[4]
        status = sys.argv[5]
        evidence = None
        test = None
        severity = None
        i = 6
        while i < len(sys.argv):
            if sys.argv[i] == "--evidence" and i + 1 < len(sys.argv):
                evidence = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--test" and i + 1 < len(sys.argv):
                test = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--severity" and i + 1 < len(sys.argv):
                severity = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        state = load_state(state_file)
        update_dimension(state, spec_id, dimension, status, evidence, test, severity)
        save_state(state, state_file)

    elif command == "check":
        if len(sys.argv) < 3:
            print("Usage: verify_state.py check <state_file>",
                  file=sys.stderr)
            sys.exit(1)
        state = load_state(sys.argv[2])
        result = check_convergence(state)
        save_state(state, sys.argv[2])
        # 返回收敛结果的退出码
        if result["converged"]:
            sys.exit(0)
        elif result["should_stop"]:
            sys.exit(2)
        else:
            sys.exit(1)  # 可以继续

    elif command == "save":
        if len(sys.argv) < 3:
            print("Usage: verify_state.py save <state_file>",
                  file=sys.stderr)
            sys.exit(1)
        # save 只是重新保存（更新 updated_at）
        state = load_state(sys.argv[2])
        save_state(state, sys.argv[2])

    elif command == "summary":
        if len(sys.argv) < 3:
            print("Usage: verify_state.py summary <state_file>",
                  file=sys.stderr)
            sys.exit(1)
        state = load_state(sys.argv[2])
        print_summary(state)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
