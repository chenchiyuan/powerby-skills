#!/usr/bin/env python3
"""
Bug索引自动生成脚本

功能:
1. 扫描所有Bug文档
2. 提取元数据
3. 生成各类索引页面
4. 更新统计信息

使用方法:
    python3 generate-bug-index.py [选项]

选项:
    --global          生成全局索引 (默认)
    --iteration ID    生成特定迭代索引
    --category CAT    生成分类索引
    --all            生成所有索引
    --validate       仅验证不生成
"""

import os
import sys
import json
import yaml
import glob
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class BugIndexGenerator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.docs_dir = self.root_dir / "docs"
        self.bugs_dir = self.docs_dir / "bugs"
        self.template_dir = self.bugs_dir / "templates"

    def scan_bug_documents(self) -> List[Dict[str, Any]]:
        """扫描所有Bug文档并提取元数据"""
        bugs = []

        # 扫描全局Bug
        for bug_file in glob.glob(str(self.bugs_dir / "**" / "*.md"), recursive=True):
            if "template" in bug_file or "scripts" in bug_file:
                continue

            metadata = self.extract_bug_metadata(bug_file)
            if metadata:
                bugs.append(metadata)

        return bugs

    def extract_bug_metadata(self, file_path: str) -> Dict[str, Any]:
        """从Bug文档中提取元数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取YAML元数据
            metadata_match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if not metadata_match:
                return None

            metadata = yaml.safe_load(metadata_match.group(1))

            # 提取标题
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                metadata['title'] = title_match.group(1)

            # 添加文件路径
            metadata['file_path'] = file_path
            metadata['relative_path'] = os.path.relpath(file_path, self.root_dir)

            return metadata

        except Exception as e:
            print(f"❌ 解析Bug文档失败 {file_path}: {e}")
            return None

    def generate_global_index(self, bugs: List[Dict[str, Any]]):
        """生成全局Bug索引"""
        # 计算统计信息
        stats = self.calculate_statistics(bugs)

        # 生成索引内容
        content = self.render_global_index(bugs, stats)

        # 写入文件
        index_file = self.bugs_dir / "index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 生成全局Bug索引: {index_file}")

    def generate_iteration_index(self, iteration_id: str, bugs: List[Dict[str, Any]]):
        """生成特定迭代的Bug索引"""
        # 筛选该迭代的Bug
        iteration_bugs = [b for b in bugs if iteration_id in b.get('discovered_in', '')]

        # 生成索引
        iteration_bugs_dir = self.docs_dir / "iterations" / iteration_id / "bugs"
        iteration_bugs_dir.mkdir(parents=True, exist_ok=True)

        index_file = iteration_bugs_dir / "index.md"

        content = self.render_iteration_index(iteration_id, iteration_bugs)

        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 生成迭代Bug索引: {index_file}")

    def generate_category_index(self, category: str, bugs: List[Dict[str, Any]]):
        """生成分类Bug索引"""
        # 筛选该分类的Bug
        category_bugs = [b for b in bugs if b.get('category') == category]

        # 生成索引
        category_dir = self.bugs_dir / "categories" / category
        category_dir.mkdir(parents=True, exist_ok=True)

        index_file = category_dir / "index.md"

        content = self.render_category_index(category, category_bugs)

        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 生成分类Bug索引: {index_file}")

    def calculate_statistics(self, bugs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算Bug统计信息"""
        stats = {
            'total': len(bugs),
            'by_status': {},
            'by_severity': {},
            'by_category': {},
            'by_iteration': {},
            'by_month': {}
        }

        for bug in bugs:
            # 按状态统计
            status = bug.get('status', 'unknown')
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1

            # 按严重程度统计
            severity = bug.get('severity', 'unknown')
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1

            # 按分类统计
            category = bug.get('category', 'unknown')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1

            # 按迭代统计
            discovered_in = bug.get('discovered_in', 'unknown')
            stats['by_iteration'][discovered_in] = stats['by_iteration'].get(discovered_in, 0) + 1

            # 按月份统计
            discovered_at = bug.get('discovered_at', '')
            if discovered_at:
                month = discovered_at[:7]  # YYYY-MM
                stats['by_month'][month] = stats['by_month'].get(month, 0) + 1

        return stats

    def render_global_index(self, bugs: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """渲染全局索引"""
        generated_at = datetime.now().isoformat()

        content = f"""# 项目Bug总览

> **最后更新**: {generated_at}
> **自动生成**: 本索引由 `generate-bug-index.py` 脚本自动生成

## 📊 统计信息

| 指标 | 数量 |
|------|------|
| 总Bug数 | {stats['total']} |
| 未修复 | {stats['by_status'].get('open', 0)} |
| 修复中 | {stats['by_status'].get('in_progress', 0)} |
| 已修复 | {stats['by_status'].get('fixed', 0)} |
| 已废弃 | {stats['by_status'].get('deprecated', 0)} |

## 📈 按严重程度分布

| 严重程度 | 数量 | 占比 |
|----------|------|------|
| P0 | {stats['by_severity'].get('P0', 0)} | {self.calculate_percentage(stats['by_severity'].get('P0', 0), stats['total'])} |
| P1 | {stats['by_severity'].get('P1', 0)} | {self.calculate_percentage(stats['by_severity'].get('P1', 0), stats['total'])} |
| P2 | {stats['by_severity'].get('P2', 0)} | {self.calculate_percentage(stats['by_severity'].get('P2', 0), stats['total'])} |

## 📂 按分类分布

"""

        for category, count in stats['by_category'].items():
            content += f"- **{category}**: {count} 个\n"

        content += "\n## 🔍 Bug列表\n\n"

        # 未修复Bug
        content += "### 未修复Bug (按严重程度排序)\n\n"
        open_bugs = [b for b in bugs if b.get('status') == 'open']
        open_bugs.sort(key=lambda x: x.get('severity', 'P2'))

        for bug in open_bugs:
            content += f"- **[{bug.get('bug_id')}]({bug.get('relative_path')})** - {bug.get('title')}\n"
            content += f"  - 严重程度: {bug.get('severity')}\n"
            content += f"  - 分类: {bug.get('category')}\n"
            content += f"  - 发现迭代: {bug.get('discovered_in')}\n\n"

        # 已修复Bug
        content += "### 已修复Bug\n\n"
        fixed_bugs = [b for b in bugs if b.get('status') == 'fixed']

        for bug in fixed_bugs:
            content += f"- **[{bug.get('bug_id')}]({bug.get('relative_path')})** - {bug.get('title')}\n"
            content += f"  - 严重程度: {bug.get('severity')}\n"
            content += f"  - 发现迭代: {bug.get('discovered_in')}\n"
            content += f"  - 修复迭代: {bug.get('fixed_in')}\n\n"

        # 按时间分布
        content += "## 📅 按时间分布\n\n"
        for month, count in sorted(stats['by_month'].items()):
            content += f"- **{month}**: {count} 个Bug\n"

        content += "\n## 🔗 快速链接\n\n"

        # 按迭代查看
        content += "### 按迭代查看\n"
        for iteration, count in sorted(stats['by_iteration'].items()):
            content += f"- [{iteration}](iterations/{iteration}/bugs/index.md): {count} 个Bug\n"

        content += "\n### 按分类查看\n"
        for category in sorted(stats['by_category'].keys()):
            content += f"- [{category}](categories/{category}/index.md): {stats['by_category'][category]} 个Bug\n"

        content += """

---

**说明**:
- 严重程度: P0(致命) > P1(严重) > P2(一般)
- 状态: open(未修复) > in_progress(修复中) > fixed(已修复) > deprecated(已废弃)
- 分类: security(安全) > performance(性能) > ui(界面) > logic(逻辑) > data(数据)
"""

        return content

    def render_iteration_index(self, iteration_id: str, bugs: List[Dict[str, Any]]) -> str:
        """渲染迭代索引"""
        content = f"""# {iteration_id} - Bug列表

## 概述
- 总计: {len(bugs)}个Bug
- 未修复: {len([b for b in bugs if b.get('status') == 'open'])}
- 已修复: {len([b for b in bugs if b.get('status') == 'fixed'])}

## Bug列表

"""

        for bug in bugs:
            status_icon = "✅" if bug.get('status') == 'fixed' else "⏳"
            content += f"### {status_icon} [{bug.get('bug_id')}]({bug.get('relative_path')}) - {bug.get('title')}\n"
            content += f"- 严重程度: {bug.get('severity')}\n"
            content += f"- 分类: {bug.get('category')}\n"
            content += f"- 状态: {bug.get('status')}\n\n"

        content += """
## 关联文档
- [PRD](../prd.md) - 相关需求文档
- [架构](../architecture.md) - 相关架构文档
- [任务](../tasks.md) - 相关任务文档
"""

        return content

    def render_category_index(self, category: str, bugs: List[Dict[str, Any]]) -> str:
        """渲染分类索引"""
        content = f"""# {category} 相关Bug

## 概述
- 总计: {len(bugs)}个{category}相关Bug
- 未修复: {len([b for b in bugs if b.get('status') == 'open'])}
- 已修复: {len([b for b in bugs if b.get('status') == 'fixed'])}

## Bug列表

"""

        for bug in bugs:
            status_icon = "✅" if bug.get('status') == 'fixed' else "⏳"
            content += f"### {status_icon} [{bug.get('bug_id')}]({bug.get('relative_path')}) - {bug.get('title')}\n"
            content += f"- 严重程度: {bug.get('severity')}\n"
            content += f"- 发现迭代: {bug.get('discovered_in')}\n\n"

        return content

    def calculate_percentage(self, count: int, total: int) -> str:
        """计算百分比"""
        if total == 0:
            return "0%"
        return f"{(count / total * 100):.1f}%"

    def validate_bug_documents(self, bugs: List[Dict[str, Any]]) -> bool:
        """验证Bug文档"""
        errors = []

        for bug in bugs:
            # 检查必要字段
            required_fields = ['bug_id', 'title', 'severity', 'status']
            for field in required_fields:
                if field not in bug:
                    errors.append(f"❌ {bug.get('file_path', 'Unknown')}: 缺少必要字段 '{field}'")

            # 检查关联文档是否存在
            for doc in bug.get('related_documents', []):
                doc_path = self.root_dir / doc['path']
                if not doc_path.exists():
                    errors.append(f"⚠️ {bug['bug_id']}: 关联文档不存在 {doc['path']}")

        if errors:
            print("\n".join(errors))
            return False

        print("✅ 所有Bug文档验证通过")
        return True

    def run(self, args):
        """运行索引生成器"""
        # 扫描Bug文档
        print("🔍 扫描Bug文档...")
        bugs = self.scan_bug_documents()
        print(f"📄 发现 {len(bugs)} 个Bug文档")

        # 验证
        if args.validate:
            return self.validate_bug_documents(bugs)

        # 生成索引
        if args.all or not any([args.global_index, args.iteration, args.category]):
            # 默认生成全局索引
            self.generate_global_index(bugs)

        if args.iteration:
            self.generate_iteration_index(args.iteration, bugs)

        if args.category:
            self.generate_category_index(args.category, bugs)

        print("\n🎉 Bug索引生成完成")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Bug索引生成器')
    parser.add_argument('--global', action='store_true', dest='global_index',
                       help='生成全局索引')
    parser.add_argument('--iteration', type=str, metavar='ID',
                       help='生成特定迭代索引')
    parser.add_argument('--category', type=str, metavar='CAT',
                       help='生成分类索引')
    parser.add_argument('--all', action='store_true',
                       help='生成所有索引')
    parser.add_argument('--validate', action='store_true',
                       help='仅验证不生成')
    parser.add_argument('--root', type=str, default='.',
                       help='项目根目录 (默认: 当前目录)')

    args = parser.parse_args()

    generator = BugIndexGenerator(args.root)
    generator.run(args)

if __name__ == '__main__':
    main()
