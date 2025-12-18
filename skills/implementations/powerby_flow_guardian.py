#!/usr/bin/env python3
"""
PowerBy Flow Guardian - 流程守护者技能实现
版本: v1.0.0
创建日期: 2025-12-18

这个模块实现了powerby-flow-guardian技能的核心功能，
包括状态检测、流程分析、问题诊断和指导建议生成。
"""

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Phase(str, Enum):
    """项目阶段枚举"""
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"
    P6 = "P6"
    P7 = "P7"
    P8 = "P8"
    UNKNOWN = "UNKNOWN"


class GateStatus(str, Enum):
    """门禁状态枚举"""
    PASSED = "PASSED"
    PENDING = "PENDING"
    NOT_REACHED = "NOT_REACHED"
    FAILED = "FAILED"


class Severity(str, Enum):
    """问题严重程度枚举"""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


@dataclass
class DocumentStatus:
    """文档状态"""
    name: str
    path: str
    exists: bool
    is_valid: bool = True
    last_modified: Optional[datetime] = None


@dataclass
class GateInfo:
    """门禁信息"""
    gate_id: int
    status: GateStatus
    checked_at: Optional[datetime] = None
    failure_reason: Optional[str] = None


@dataclass
class Violation:
    """违规信息"""
    type: str
    description: str
    severity: Severity
    location: Optional[str] = None
    recommendation: Optional[str] = None


@dataclass
class ActionItem:
    """行动项"""
    action: str
    command: Optional[str] = None
    priority: str = "medium"
    estimated_time: Optional[str] = None
    blocking_issues: List[str] = field(default_factory=list)


@dataclass
class PhaseStatus:
    """阶段状态"""
    phase: Phase
    status: str  # NOT_STARTED, IN_PROGRESS, COMPLETED
    health_score: int = 0
    blockers: List[str] = field(default_factory=list)
    next_phase: Optional[Phase] = None


class PowerByFlowGuardian:
    """PowerBy流程守护者主类"""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.powerby_dir = self.project_path / ".powerby"
        self.docs_dir = self.project_path / "docs"

        # 阶段到指令的映射
        self.phase_to_command = {
            Phase.P0: "/powerby.initialize",
            Phase.P1: "/powerby.define",
            Phase.P2: "/powerby.clarify",
            Phase.P3: "/powerby.research",
            Phase.P4: "/powerby.design",
            Phase.P5: "/powerby.plan",
            Phase.P6: "/powerby.implement",
            Phase.P7: "/powerby.review",
        }

        # 阶段必需文档
        self.phase_required_docs = {
            Phase.P0: ["docs/constitution.md", ".powerby/project.json"],
            Phase.P1: ["docs/iterations/*/prd.md", "docs/iterations/*/function-points.md"],
            Phase.P2: ["docs/iterations/*/clarifications.md"],
            Phase.P3: ["docs/iterations/*/research.md"],
            Phase.P4: ["docs/iterations/*/architecture.md", "docs/iterations/*/data-model.md"],
            Phase.P5: ["docs/iterations/*/tasks.md"],
            Phase.P6: ["docs/iterations/*/implementation-report.md"],
            Phase.P7: ["docs/iterations/*/code-review-report.md"],
        }

    # ==================== 状态检测功能 ====================

    def analyze_current_state(self) -> Dict:
        """分析当前状态"""
        project_status = self._detect_project_status()
        gate_status = self._check_all_gates()
        document_status = self._scan_document_status()
        iteration_health = self._analyze_iteration_health()

        return {
            "current_phase": project_status.phase.value,
            "current_status": project_status.status,
            "health_score": project_status.health_score,
            "gate_status": {f"gate_{i}": self._gate_to_dict(g) for i, g in gate_status.items()},
            "document_status": {doc.name: self._doc_to_dict(doc) for doc in document_status},
            "iteration_health": iteration_health,
            "recommendations": self._generate_recommendations(project_status, gate_status, document_status)
        }

    def _detect_project_status(self) -> PhaseStatus:
        """检测项目当前阶段"""
        # 读取项目元数据
        project_metadata = self._read_project_metadata()

        if not project_metadata:
            return PhaseStatus(
                phase=Phase.UNKNOWN,
                status="NOT_INITIALIZED",
                health_score=0,
                blockers=["项目未初始化"]
            )

        current_phase = Phase(project_metadata.get("current_phase", "UNKNOWN"))
        current_status = project_metadata.get("current_status", "UNKNOWN")

        # 根据阶段和文档存在性评估健康度
        health_score = self._calculate_health_score(current_phase, current_status)

        return PhaseStatus(
            phase=current_phase,
            status=current_status,
            health_score=health_score,
            blockers=self._identify_blockers(current_phase)
        )

    def _read_project_metadata(self) -> Optional[Dict]:
        """读取项目元数据"""
        project_json_path = self.powerby_dir / "project.json"
        if project_json_path.exists():
            try:
                with open(project_json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return None

    def _check_all_gates(self) -> Dict[int, GateInfo]:
        """检查所有门禁状态"""
        gates = {}
        project_metadata = self._read_project_metadata()

        for gate_id in range(0, 9):
            if project_metadata and "gates" in project_metadata:
                gate_data = project_metadata["gates"].get(f"gate_{gate_id}")
                if gate_data:
                    gates[gate_id] = GateInfo(
                        gate_id=gate_id,
                        status=GateStatus(gate_data.get("status", "NOT_REACHED")),
                        checked_at=datetime.fromisoformat(gate_data.get("checked_at", "")) if gate_data.get("checked_at") else None,
                        failure_reason=gate_data.get("failure_reason")
                    )
                else:
                    gates[gate_id] = GateInfo(gate_id=gate_id, status=GateStatus.NOT_REACHED)
            else:
                gates[gate_id] = GateInfo(gate_id=gate_id, status=GateStatus.NOT_REACHED)

        return gates

    def _scan_document_status(self) -> List[DocumentStatus]:
        """扫描文档状态"""
        documents = []

        # 扫描基础文档
        for doc_path in ["docs/constitution.md", ".powerby/project.json"]:
            full_path = self.project_path / doc_path
            documents.append(DocumentStatus(
                name=os.path.basename(doc_path),
                path=doc_path,
                exists=full_path.exists(),
                is_valid=self._validate_document(full_path) if full_path.exists() else False
            ))

        # 扫描迭代文档
        iterations_dir = self.docs_dir / "iterations"
        if iterations_dir.exists():
            for iteration_dir in iterations_dir.iterdir():
                if iteration_dir.is_dir():
                    for doc_name in ["prd.md", "clarifications.md", "research.md", "architecture.md", "tasks.md"]:
                        doc_path = iteration_dir / doc_name
                        documents.append(DocumentStatus(
                            name=doc_name,
                            path=str(doc_path.relative_to(self.project_path)),
                            exists=doc_path.exists(),
                            is_valid=self._validate_document(doc_path) if doc_path.exists() else False
                        ))

        return documents

    def _validate_document(self, doc_path: Path) -> bool:
        """验证文档格式"""
        if not doc_path.exists():
            return False

        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 基本验证：检查是否为空
                return len(content.strip()) > 0
        except Exception:
            return False

    def _analyze_iteration_health(self) -> Dict:
        """分析迭代健康度"""
        iterations_json_path = self.powerby_dir / "iterations.json"
        if not iterations_json_path.exists():
            return {"overall_score": 0, "issues": []}

        try:
            with open(iterations_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            active_iterations = [it for it in data.get("iterations", []) if it.get("status") != "released"]
            if not active_iterations:
                return {"overall_score": 100, "issues": []}

            # 计算健康度
            total_score = 0
            for iteration in active_iterations:
                score = self._calculate_iteration_score(iteration)
                total_score += score

            avg_score = total_score // len(active_iterations)

            # 识别问题
            issues = []
            for iteration in active_iterations:
                issues.extend(self._identify_iteration_issues(iteration))

            return {
                "overall_score": avg_score,
                "issues": issues
            }
        except (json.JSONDecodeError, FileNotFoundError):
            return {"overall_score": 0, "issues": [{"type": "corrupted_data", "severity": "critical"}]}

    def _calculate_iteration_score(self, iteration: Dict) -> int:
        """计算单个迭代的健康度分数"""
        score = 100

        # 检查文档完整性
        required_docs = ["prd.md", "clarifications.md", "research.md", "architecture.md", "tasks.md"]
        for doc in required_docs:
            if doc not in iteration.get("documents", []):
                score -= 10

        # 检查门禁通过情况
        gates_passed = iteration.get("metrics", {}).get("gates_passed", 0)
        gates_failed = iteration.get("metrics", {}).get("gates_failed", 0)
        if gates_failed > 0:
            score -= gates_failed * 20

        # 检查任务完成情况
        total_tasks = iteration.get("metrics", {}).get("total_tasks", 0)
        completed_tasks = iteration.get("metrics", {}).get("completed_tasks", 0)
        if total_tasks > 0:
            completion_rate = completed_tasks / total_tasks
            score = int(score * completion_rate)

        return max(0, score)

    def def _identify_iteration_issues(self, iteration: Dict) -> List[Dict]:
        """识别迭代问题"""
        issues = []

        # 检查缺失文档
        required_docs = ["prd.md", "clarifications.md", "research.md", "architecture.md", "tasks.md"]
        for doc in required_docs:
            if doc not in iteration.get("documents", []):
                issues.append({
                    "type": "missing_document",
                    "doc": doc,
                    "severity": "major",
                    "iteration": iteration.get("id")
                })

        # 检查进度停滞
        last_activity = iteration.get("last_activity")
        if last_activity:
            days_since_activity = (datetime.now() - datetime.fromisoformat(last_activity)).days
            if days_since_activity > 7:
                issues.append({
                    "type": "stale_progress",
                    "days": days_since_activity,
                    "severity": "major",
                    "iteration": iteration.get("id")
                })

        return issues

    # ==================== 合规检查功能 ====================

    def audit_compliance(self, phase: Optional[Phase] = None) -> Dict:
        """审计合规性"""
        violations = []

        # 检查指令序列
        violations.extend(self._check_command_sequence())

        # 检查门禁绕过
        violations.extend(self._check_gate_bypass())

        # 检查文档完整性
        violations.extend(self._check_document_completeness(phase))

        # 检查命名规范
        violations.extend(self._check_naming_conventions())

        # 计算合规分数
        compliance_score = self._calculate_compliance_score(violations)

        return {
            "compliance_score": compliance_score,
            "violations": [self._violation_to_dict(v) for v in violations],
            "recommendations": self._generate_compliance_recommendations(violations)
        }

    def _check_command_sequence(self) -> List[Violation]:
        """检查指令序列"""
        violations = []
        # 这里需要实现指令执行历史检查
        # 暂时返回空列表
        return violations

    def _check_gate_bypass(self) -> List[Violation]:
        """检查门禁绕过"""
        violations = []
        # 这里需要实现门禁绕过检查
        # 暂时返回空列表
        return violations

    def _check_document_completeness(self, phase: Optional[Phase]) -> List[Violation]:
        """检查文档完整性"""
        violations = []

        if phase and phase in self.phase_required_docs:
            required_docs = self.phase_required_docs[phase]
            for doc_pattern in required_docs:
                if not self._document_exists(doc_pattern):
                    violations.append(Violation(
                        type="missing_document",
                        description=f"缺少必需文档: {doc_pattern}",
                        severity=Severity.MAJOR,
                        recommendation=f"创建文档或执行相应指令生成"
                    ))

        return violations

    def _check_naming_conventions(self) -> List[Violation]:
        """检查命名规范"""
        violations = []
        # 检查分支命名
        # 检查文档路径
        # 检查迭代编号
        return violations

    # ==================== 指导建议功能 ====================

    def generate_guidance(self, current_phase: Phase) -> Dict:
        """生成指导建议"""
        # 分析当前状态
        phase_analysis = self._analyze_phase_state(current_phase)

        # 生成即时行动
        immediate_actions = self._generate_immediate_actions(phase_analysis)

        # 预测下一步
        next_command = self._predict_next_command(current_phase)

        # 生成路线图
        roadmap = self._generate_roadmap(current_phase)

        return {
            "current_phase": current_phase.value,
            "phase_analysis": phase_analysis,
            "immediate_actions": [self._action_to_dict(a) for a in immediate_actions],
            "next_command": next_command,
            "roadmap": roadmap,
            "estimated_total_time": self._estimate_total_time(current_phase)
        }

    def _generate_immediate_actions(self, phase_analysis: Dict) -> List[ActionItem]:
        """生成即时行动建议"""
        actions = []

        if phase_analysis.get("has_blockers"):
            # 有关键阻塞，先解决阻塞
            for blocker in phase_analysis.get("blockers", []):
                actions.append(ActionItem(
                    action=f"解决阻塞: {blocker}",
                    priority="critical",
                    estimated_time="1天"
                ))
        elif not phase_analysis.get("is_completed"):
            # 当前阶段未完成
            current_phase = Phase(phase_analysis.get("phase"))
            command = self.phase_to_command.get(current_phase)
            actions.append(ActionItem(
                action=f"完成{current_phase.value}阶段",
                command=command,
                priority="high",
                estimated_time=self._estimate_phase_time(current_phase)
            ))

        return actions

    def _predict_next_command(self, current_phase: Phase) -> Optional[str]:
        """预测下一步指令"""
        next_phase = self._get_next_phase(current_phase)
        return self.phase_to_command.get(next_phase)

    def _generate_roadmap(self, current_phase: Phase) -> List[Dict]:
        """生成路线图"""
        roadmap = []
        phase = self._get_next_phase(current_phase)

        while phase and phase != Phase.P8:
            command = self.phase_to_command.get(phase)
            estimated_time = self._estimate_phase_time(phase)

            roadmap.append({
                "phase": phase.value,
                "command": command,
                "estimated_time": estimated_time,
                "description": self._get_phase_description(phase)
            })

            phase = self._get_next_phase(phase)

        return roadmap

    # ==================== 问题诊断功能 ====================

    def diagnose_problems(self) -> Dict:
        """诊断问题"""
        problems = []

        # 检查流程跳跃
        problems.extend(self._detect_flow_jumps())

        # 检查长期停滞
        problems.extend(self._detect_stagnation())

        # 检查重复返工
        problems.extend(self._detect_rework())

        # 分析根因
        root_causes = self._analyze_root_causes(problems)

        # 生成解决方案
        solutions = self._generate_solutions(problems)

        return {
            "problems": problems,
            "root_causes": root_causes,
            "solutions": solutions,
            "severity_summary": self._summarize_severity(problems)
        }

    def _detect_flow_jumps(self) -> List[Dict]:
        """检测流程跳跃"""
        # 实现流程跳跃检测逻辑
        return []

    def _detect_stagnation(self) -> List[Dict]:
        """检测长期停滞"""
        # 实现停滞检测逻辑
        return []

    def _detect_rework(self) -> List[Dict]:
        """检测重复返工"""
        # 实现返工检测逻辑
        return []

    def _analyze_root_causes(self, problems: List[Dict]) -> List[Dict]:
        """分析根因"""
        # 实现根因分析逻辑
        return []

    def _generate_solutions(self, problems: List[Dict]) -> List[Dict]:
        """生成解决方案"""
        # 实现解决方案生成逻辑
        return []

    # ==================== 辅助方法 ====================

    def _calculate_health_score(self, phase: Phase, status: str) -> int:
        """计算健康度分数"""
        base_score = 100

        # 根据阶段调整
        phase_multipliers = {
            Phase.P0: 1.0, Phase.P1: 0.9, Phase.P2: 0.9,
            Phase.P3: 0.8, Phase.P4: 0.8, Phase.P5: 0.7,
            Phase.P6: 0.6, Phase.P7: 0.5, Phase.P8: 1.0
        }

        multiplier = phase_multipliers.get(phase, 0.5)
        return int(base_score * multiplier)

    def _identify_blockers(self, phase: Phase) -> List[str]:
        """识别阻塞点"""
        blockers = []

        # 检查必需文档
        if phase in self.phase_required_docs:
            for doc_pattern in self.phase_required_docs[phase]:
                if not self._document_exists(doc_pattern):
                    blockers.append(f"缺少文档: {doc_pattern}")

        # 检查门禁
        gate_id = int(phase.value[1])
        gate_status = self._check_gate_status(gate_id)
        if gate_status == GateStatus.FAILED:
            blockers.append(f"Gate {gate_id} 未通过")

        return blockers

    def _document_exists(self, doc_pattern: str) -> bool:
        """检查文档是否存在（支持通配符）"""
        if "*" in doc_pattern:
            # 处理通配符
            pattern_parts = doc_pattern.split("*")
            prefix = pattern_parts[0]
            suffix = pattern_parts[-1] if len(pattern_parts) > 1 else ""

            # 在docs/iterations目录下搜索
            iterations_dir = self.docs_dir / "iterations"
            if iterations_dir.exists():
                for iteration_dir in iterations_dir.iterdir():
                    if iteration_dir.is_dir():
                        doc_path = iteration_dir / suffix
                        if doc_path.exists():
                            return True
            return False
        else:
            return (self.project_path / doc_pattern).exists()

    def _get_next_phase(self, current_phase: Phase) -> Optional[Phase]:
        """获取下一阶段"""
        phase_order = [Phase.P0, Phase.P1, Phase.P2, Phase.P3, Phase.P4, Phase.P5, Phase.P6, Phase.P7, Phase.P8]
        try:
            current_index = phase_order.index(current_phase)
            if current_index < len(phase_order) - 1:
                return phase_order[current_index + 1]
        except ValueError:
            pass
        return None

    def _estimate_phase_time(self, phase: Phase) -> str:
        """估算阶段耗时"""
        time_estimates = {
            Phase.P0: "0.5天", Phase.P1: "1-3天", Phase.P2: "0.5-1天",
            Phase.P3: "1-2天", Phase.P4: "2-5天", Phase.P5: "1-2天",
            Phase.P6: "N天", Phase.P7: "0.5-1天", Phase.P8: "0.5-1天"
        }
        return time_estimates.get(phase, "未知")

    def _get_phase_description(self, phase: Phase) -> str:
        """获取阶段描述"""
        descriptions = {
            Phase.P0: "项目初始化",
            Phase.P1: "需求定义",
            Phase.P2: "需求澄清",
            Phase.P3: "技术调研",
            Phase.P4: "架构设计",
            Phase.P5: "任务规划",
            Phase.P6: "开发实现",
            Phase.P7: "代码审查",
            Phase.P8: "发布交付"
        }
        return descriptions.get(phase, "未知阶段")

    def _estimate_total_time(self, current_phase: Phase) -> str:
        """估算总耗时"""
        remaining_phases = []
        phase = self._get_next_phase(current_phase)

        while phase and phase != Phase.P8:
            remaining_phases.append(phase)
            phase = self._get_next_phase(phase)

        # 简化估算：平均每个阶段2天
        estimated_days = len(remaining_phases) * 2
        return f"{estimated_days}天"

    def _check_gate_status(self, gate_id: int) -> GateStatus:
        """检查特定门禁状态"""
        gates = self._check_all_gates()
        return gates.get(gate_id, GateInfo(gate_id, GateStatus.NOT_REACHED)).status

    def _analyze_phase_state(self, phase: Phase) -> Dict:
        """分析阶段状态"""
        return {
            "phase": phase.value,
            "is_completed": self._is_phase_completed(phase),
            "has_blockers": len(self._identify_blockers(phase)) > 0,
            "blockers": self._identify_blockers(phase),
            "health_score": self._calculate_health_score(phase, "IN_PROGRESS")
        }

    def _is_phase_completed(self, phase: Phase) -> bool:
        """检查阶段是否完成"""
        # 检查所有必需文档是否存在
        if phase in self.phase_required_docs:
            for doc_pattern in self.phase_required_docs[phase]:
                if not self._document_exists(doc_pattern):
                    return False

        # 检查门禁是否通过
        gate_id = int(phase.value[1])
        gate_status = self._check_gate_status(gate_id)
        return gate_status == GateStatus.PASSED

    # ==================== 输出格式化方法 ====================

    def _gate_to_dict(self, gate: GateInfo) -> Dict:
        """将门禁信息转换为字典"""
        return {
            "status": gate.status.value,
            "checked_at": gate.checked_at.isoformat() if gate.checked_at else None,
            "failure_reason": gate.failure_reason
        }

    def _doc_to_dict(self, doc: DocumentStatus) -> str:
        """将文档状态转换为字符串"""
        status = "✅ 存在" if doc.exists else "❌ 缺失"
        if doc.exists and not doc.is_valid:
            status += " (格式错误)"
        return status

    def _violation_to_dict(self, violation: Violation) -> Dict:
        """将违规信息转换为字典"""
        return {
            "type": violation.type,
            "description": violation.description,
            "severity": violation.severity.value,
            "location": violation.location,
            "recommendation": violation.recommendation
        }

    def _action_to_dict(self, action: ActionItem) -> Dict:
        """将行动项转换为字典"""
        return {
            "action": action.action,
            "command": action.command,
            "priority": action.priority,
            "estimated_time": action.estimated_time,
            "blocking_issues": action.blocking_issues
        }

    def _generate_recommendations(self, project_status: PhaseStatus, gates: Dict[int, GateInfo], docs: List[DocumentStatus]) -> List[str]:
        """生成建议"""
        recommendations = []

        if project_status.phase == Phase.UNKNOWN:
            recommendations.append("项目尚未初始化，请先执行 /powerby.initialize")

        # 检查关键阻塞
        if project_status.blockers:
            recommendations.append(f"当前有 {len(project_status.blockers)} 个阻塞点需要解决")

        # 检查门禁
        pending_gates = [g for g in gates.values() if g.status == GateStatus.PENDING]
        if pending_gates:
            recommendations.append(f"有 {len(pending_gates)} 个门禁等待检查")

        return recommendations

    def _calculate_compliance_score(self, violations: List[Violation]) -> int:
        """计算合规分数"""
        if not violations:
            return 100

        total_penalty = sum(20 if v.severity == Severity.CRITICAL else 10 if v.severity == Severity.MAJOR else 5 for v in violations)
        return max(0, 100 - total_penalty)

    def _generate_compliance_recommendations(self, violations: List[Violation]) -> List[str]:
        """生成合规建议"""
        recommendations = []

        critical_violations = [v for v in violations if v.severity == Severity.CRITICAL]
        if critical_violations:
            recommendations.append(f"发现 {len(critical_violations)} 个严重违规，需要立即修复")

        for violation in violations:
            if violation.recommendation:
                recommendations.append(violation.recommendation)

        return recommendations

    def _summarize_severity(self, problems: List[Dict]) -> Dict:
        """总结问题严重程度"""
        summary = {"critical": 0, "major": 0, "minor": 0}

        for problem in problems:
            severity = problem.get("severity", "minor")
            if severity in summary:
                summary[severity] += 1

        return summary


# ==================== 命令行接口 ====================

def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="PowerBy Flow Guardian - 流程守护者")
    parser.add_argument("command", choices=["analyze", "audit", "guidance", "diagnose"], help="要执行的命令")
    parser.add_argument("--project-path", default=".", help="项目路径")
    parser.add_argument("--phase", type=Phase, choices=list(Phase), help="指定阶段")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    guardian = PowerByFlowGuardian(args.project_path)

    if args.command == "analyze":
        result = guardian.analyze_current_state()
    elif args.command == "audit":
        result = guardian.audit_compliance(args.phase)
    elif args.command == "guidance":
        if not args.phase:
            print("错误: guidance命令需要指定 --phase 参数")
            return
        result = guardian.generate_guidance(args.phase)
    elif args.command == "diagnose":
        result = guardian.diagnose_problems()

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        # 格式化输出（这里可以实现更美观的输出格式）
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
