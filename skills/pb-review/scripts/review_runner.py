#!/usr/bin/env python3
"""Run deterministic pb-review helper steps against a local repository."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from checkpoint import is_consistent, load_checkpoint, next_step_index, save_checkpoint
from registry_store import load_records, merge_records, save_records
from review_context import REVIEW_FILE_MAP, STANDARD_REGISTRY_MAP, ReviewContextStore, utc_now

STEP_GROUPS = {
    "bootstrap": [
        ("pb-review-project-scope", Path("skills/pb-review-project-scope/scripts/run.py")),
        ("pb-review-evidence-collector", Path("skills/pb-review-evidence-collector/scripts/run.py")),
        ("pb-review-conflict-resolver", Path("skills/pb-review-conflict-resolver/scripts/run.py")),
    ],
    "report": [
        ("pb-review-report-composer", Path("skills/pb-review-report-composer/scripts/run.py")),
        ("render_testability_scorecard", Path("skills/pb-review/scripts/render_testability_scorecard.py")),
        ("render_test_case_index", Path("skills/pb-review/scripts/render_test_case_index.py")),
        ("render_fixture_contract", Path("skills/pb-review/scripts/render_fixture_contract.py")),
        ("render_oracle_matrix", Path("skills/pb-review/scripts/render_oracle_matrix.py")),
    ],
}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-path", required=True, help="Path to the repository being reviewed")
    parser.add_argument(
        "--mode",
        default="bootstrap",
        choices=["bootstrap", "report"],
        help="bootstrap runs deterministic scope/evidence/conflict steps; report renders the final markdown report.",
    )
    parser.add_argument(
        "--scope",
        default="full_project",
        choices=["full_project", "single_service", "single_feature"],
        help="Review scope",
    )
    parser.add_argument(
        "--product-docs-dir",
        action="append",
        default=[],
        help="Product document directory relative to project root or absolute path. Repeatable.",
    )
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint when possible")
    parser.add_argument("--output", help="Optional file for final JSON result")
    return parser.parse_args()


def build_step_parameters(step_name: str, project_path: str, scope: str, product_docs_dirs: list[str]) -> dict:
    """Build default parameters for each workflow step."""

    if step_name == "pb-review-project-scope":
        return {
            "project_path": project_path,
            "scope": scope,
            "product_docs_dirs": product_docs_dirs,
            "include_patterns": ["**/*.md", "**/*.py", "**/*.js", "**/*.json", "**/*.yml", "**/*.yaml", "**/*.sh"],
            "exclude_patterns": ["node_modules/**", ".git/**", ".review/**", "__pycache__/**"],
        }
    if step_name == "pb-review-evidence-collector":
        return {"collection_depth": "shallow", "incremental": True}
    return {}


def run_step(script_path: Path, context: dict, parameters: dict, temp_dir: Path) -> dict:
    """Execute a step script and return its JSON payload."""

    context_path = temp_dir / "context.json"
    params_path = temp_dir / "parameters.json"
    output_path = temp_dir / "output.json"

    with context_path.open("w", encoding="utf-8") as handle:
        json.dump(context, handle, ensure_ascii=False, indent=2)
    with params_path.open("w", encoding="utf-8") as handle:
        json.dump(parameters, handle, ensure_ascii=False, indent=2)

    if script_path.name.startswith("render_"):
        command = [
            "python3",
            str(script_path),
            "--context",
            str(context_path),
            "--parameters",
            str(params_path),
            "--output",
            str(output_path),
        ]
    else:
        command = [
            "python3",
            str(script_path),
            "--context",
            str(context_path),
            "--parameters",
            str(params_path),
            "--output",
            str(output_path),
        ]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"step failed: {script_path}")

    with output_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if "status" not in payload or "errors" not in payload:
        raise ValueError(f"invalid step payload from {script_path}")
    return payload


def persist_step_output(store: ReviewContextStore, payload: dict) -> list[str]:
    """Persist a step payload into `.review/` files and return touched file names."""

    completed_writes: list[str] = []
    for result_field, context_field in STANDARD_REGISTRY_MAP.items():
        records = payload.get(result_field, [])
        if not records:
            continue
        path = store.file_path(context_field)
        merged = merge_records(load_records(path), records)
        save_records(path, merged)
        completed_writes.append(str(path.relative_to(store.review_dir)))

    for field, value in payload.get("context_writes", {}).items():
        store.write_context_field(field, value)
        completed_writes.append(str(store.file_path(field).relative_to(store.review_dir)))

    report_path = payload.get("metadata", {}).get("report_path")
    if isinstance(report_path, str) and report_path:
        normalized = normalize_review_write_path(store.review_dir, report_path)
        if normalized:
            completed_writes.append(normalized)

    return completed_writes


def normalize_review_write_path(review_dir: Path, report_path: str) -> str | None:
    """Normalize one report path into a checkpoint-relative `.review/` write path."""

    candidate = Path(report_path)
    if candidate.is_absolute():
        try:
            return str(candidate.resolve().relative_to(review_dir))
        except ValueError:
            return None

    raw = report_path.strip()
    if raw.startswith(".review/"):
        return raw.replace(".review/", "", 1)
    if raw.startswith("./.review/"):
        return raw.replace("./.review/", "", 1)
    return raw.lstrip("./")


def main() -> int:
    """Run deterministic pb-review helper steps."""

    args = parse_args()
    store = ReviewContextStore(args.project_path, args.scope)
    store.ensure_dirs()

    if args.mode == "bootstrap" and not args.resume:
        store.reset()

    checkpoint = load_checkpoint(store.review_dir) if args.resume else {}
    if args.resume and checkpoint and not is_consistent(store.review_dir, checkpoint.get("completed_writes", [])):
        checkpoint = {}

    step_definitions = STEP_GROUPS[args.mode]
    step_names = [name for name, _ in step_definitions]
    start_index = next_step_index(step_names, checkpoint) if args.resume else 0
    completed_skills = step_names[:start_index]
    failed_skills: list[str] = []
    completed_writes = checkpoint.get("completed_writes", []) if checkpoint else []

    final_status = "success"
    final_errors: list[str] = []
    total_start = utc_now()

    for step_name, relative_script in step_definitions[start_index:]:
        context = store.load_context()
        parameters = build_step_parameters(step_name, str(store.project_path), args.scope, args.product_docs_dir)
        try:
            payload = run_step(Path(__file__).resolve().parents[3] / relative_script, context, parameters, store.temp_dir)
        except Exception as exc:  # noqa: BLE001
            failed_skills.append(step_name)
            final_status = "failed"
            final_errors.append(str(exc))
            break

        completed_writes = sorted(set(completed_writes + persist_step_output(store, payload)))
        save_checkpoint(store.review_dir, store.review_id, step_name, completed_writes)

        completed_skills.append(step_name)
        if payload["status"] == "failed":
            failed_skills.append(step_name)
            final_status = "failed"
            final_errors.extend(payload.get("errors", []))
            break
        if payload["status"] == "partial" and final_status != "failed":
            final_status = "partial"
            final_errors.extend(payload.get("errors", []))

    result = {
        "status": final_status,
        "objects": [],
        "relations": [],
        "conflicts": [],
        "gaps": [],
        "context_writes": {},
        "metadata": {
            "mode": args.mode,
            "started_at": total_start,
            "finished_at": utc_now(),
            "completed_skills": completed_skills,
            "failed_skills": failed_skills,
            "report_path": str(store.review_dir / "deliverables" / "07-review-report.md"),
            "review_dir": str(store.review_dir),
            "pending_agent_skills": (
                [
                    "pb-review-product-reconstructor",
                    "pb-review-feature-reconstructor",
                    "pb-review-dependency-reconstructor",
                    "pb-review-implementation-mapper",
                    "pb-review-relation-builder",
                    "pb-review-architecture-builder",
                    "pb-review-data-flow-builder",
                    "pb-review-gap-analyzer",
                ]
                if args.mode == "bootstrap"
                else []
            ),
            "deliverables": [],
        },
        "errors": final_errors,
    }

    if args.output:
        with Path(args.output).open("w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if final_status != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
