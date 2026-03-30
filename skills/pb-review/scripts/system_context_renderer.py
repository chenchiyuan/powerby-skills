#!/usr/bin/env python3
"""Shared renderer for the pb-review system-context deliverable."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a simple Markdown table."""

    table = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    table.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(table)


def write_system_context(
    project_root: Path,
    project_metadata: dict[str, Any],
    manifest: dict[str, Any],
) -> str:
    """Write the system-context deliverable and return its project-relative path."""

    template_path = Path(__file__).resolve().parents[2] / "pb-review-project-scope" / "assets" / "system-context-template.md"
    template_text = template_path.read_text(encoding="utf-8")
    deliverables_dir = project_root / ".review" / "deliverables"
    deliverables_dir.mkdir(parents=True, exist_ok=True)
    relative_output_path = ".review/deliverables/01-system-context.md"
    output_path = project_root / relative_output_path

    inventory = project_metadata.get("resource_inventory", {})
    product_doc_dirs = project_metadata.get("product_doc_dirs", [])
    product_doc_inventory = project_metadata.get("product_doc_inventory", [])
    entry_surface_inventory = project_metadata.get("entry_surface_inventory", [])
    missing_resources = project_metadata.get("missing_resources", [])

    evidence_summary = render_table(
        ["资源类型", "数量", "示例"],
        [
            [
                str(bucket),
                str(len(records)),
                ", ".join(records[:3]) if records else "-",
            ]
            for bucket, records in inventory.items()
        ]
        or [["-", "0", "-"]],
    )
    deliverable_rows = render_table(
        ["Deliverable ID", "类型", "路径", "责任 skill", "状态"],
        [
            [
                str(item.get("deliverable_id", "")),
                str(item.get("deliverable_type", "")),
                str(item.get("path", "")),
                str(item.get("producer_skill", "")),
                str(item.get("status", "")),
            ]
            for item in manifest.get("required_deliverables", [])
        ]
        or [["-", "-", "-", "-", "-"]],
    )
    entry_surface_rows = render_table(
        ["类型", "路径", "名称"],
        [
            [
                str(item.get("type", "")),
                str(item.get("path", "")),
                str(item.get("name", "")),
            ]
            for item in entry_surface_inventory
        ]
        or [["-", "-", "-"]],
    )

    rendered = template_text
    rendered = rendered.replace("项目名称：", f"项目名称：{project_metadata.get('project_name', '')}")
    rendered = rendered.replace("项目类型：", f"项目类型：{project_metadata.get('project_type', '')}")
    rendered = rendered.replace("评审范围：", f"评审范围：{project_metadata.get('scope', '')}")
    rendered = rendered.replace("文件总数：", f"文件总数：{project_metadata.get('file_count', 0)}")
    rendered = rendered.replace(
        "用户指定产品文档目录：",
        f"用户指定产品文档目录：{', '.join(product_doc_dirs) if product_doc_dirs else '(未提供)'}",
    )
    rendered = rendered.replace(
        "命中的产品文档：",
        f"命中的产品文档：{', '.join(product_doc_inventory) if product_doc_inventory else '(无命中)'}",
    )
    rendered = rendered.replace(
        "未命中的产品文档目录：",
        f"未命中的产品文档目录：{'product_docs' if 'product_docs' in missing_resources else '(无)'}",
    )
    rendered = rendered.replace("| 资源类型 | 数量 | 示例 |\n|---|---|---|", evidence_summary)
    rendered = rendered.replace("| 类型 | 路径 | 名称 |\n|---|---|---|", entry_surface_rows)
    rendered = rendered.replace(
        "- \n\n## 6. 后续交付物清单",
        f"- {', '.join(missing_resources) if missing_resources else '(无)'}\n\n## 6. 后续交付物清单",
    )
    rendered = rendered.replace("| Deliverable ID | 类型 | 路径 | 责任 skill | 状态 |\n|---|---|---|---|---|", deliverable_rows)

    output_path.write_text(rendered + "\n", encoding="utf-8")
    return relative_output_path
