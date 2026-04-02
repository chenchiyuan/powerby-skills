import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_skill_script(tmp_path: Path, script_relative_path: str, context: dict, parameters: dict) -> dict:
    """Execute a pb-review step script with temporary JSON payloads."""

    context_path = tmp_path / "context.json"
    params_path = tmp_path / "parameters.json"
    output_path = tmp_path / "output.json"
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    params_path.write_text(json.dumps(parameters, ensure_ascii=False, indent=2), encoding="utf-8")

    subprocess.run(
        [
            "python3",
            str(REPO_ROOT / script_relative_path),
            "--context",
            str(context_path),
            "--parameters",
            str(params_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )
    return json.loads(output_path.read_text(encoding="utf-8"))


def test_project_scope_limits_product_docs_to_user_selected_dir(tmp_path: Path) -> None:
    """Only files under the user-provided product-doc directory should become product docs."""

    project_root = tmp_path / "repo"
    (project_root / "docs" / "product").mkdir(parents=True)
    (project_root / "docs" / "internal").mkdir(parents=True)
    (project_root / "src").mkdir(parents=True)
    (project_root / "docs" / "product" / "prd.md").write_text("# PRD\n", encoding="utf-8")
    (project_root / "docs" / "internal" / "notes.md").write_text("# Notes\n", encoding="utf-8")
    (project_root / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")

    payload = run_skill_script(
        tmp_path,
        "skills/pb-review-project-scope/scripts/run.py",
        context={},
        parameters={
            "project_path": str(project_root),
            "scope": "full_project",
            "product_docs_dirs": ["docs/product"],
        },
    )

    metadata = payload["context_writes"]["project_metadata"]
    manifest = payload["context_writes"]["deliverable_manifest"]
    assert payload["status"] == "success"
    assert metadata["product_doc_inventory"] == ["docs/product/prd.md"]
    assert "docs/internal/notes.md" in metadata["resource_inventory"]["docs"]
    assert "product_docs" not in metadata["missing_resources"]
    assert metadata["entry_surface_inventory"] == []
    assert manifest["version"] == "2.0"
    assert any(item["deliverable_id"] == "DLV-004" for item in manifest["required_deliverables"])
    assert any(item["deliverable_id"] == "DLV-011" for item in manifest["required_deliverables"])
    assert (project_root / ".review" / "deliverables" / "01-system-context.md").exists()


def test_product_reconstructor_is_skill_native_only() -> None:
    """Product reconstruction should stay in the host skill, without a local runner fallback."""

    run_script = REPO_ROOT / "skills/pb-review-product-reconstructor/scripts/run.py"
    skill_text = (REPO_ROOT / "skills/pb-review-product-reconstructor/SKILL.md").read_text(encoding="utf-8")

    assert not run_script.exists()
    assert "不对全仓库文档做兜底回退" in skill_text
    assert "后端 LLM" in skill_text


def test_pb_review_shared_contract_includes_deliverable_fields() -> None:
    """The shared contract should expose deliverable-oriented review fields."""

    contract_text = (REPO_ROOT / "skills/pb-review/references/review-contract.md").read_text(encoding="utf-8")
    context_text = (REPO_ROOT / "skills/pb-review/scripts/review_context.py").read_text(encoding="utf-8")

    assert "feature_spec_registry" in contract_text
    assert "traceability_matrix" in contract_text
    assert "difference_registry" in contract_text
    assert "deliverable_manifest" in contract_text
    assert "dependency_registry" in contract_text
    assert "implementation_registry" in contract_text
    assert '"feature_spec_registry": "feature_spec_registry.json"' in context_text
    assert '"traceability_matrix": "traceability_matrix.json"' in context_text
    assert '"difference_registry": "difference_registry.json"' in context_text
    assert '"deliverable_manifest": "deliverable_manifest.json"' in context_text
