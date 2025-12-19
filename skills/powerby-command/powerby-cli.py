#!/usr/bin/env python3
"""
PowerBy CLI - PowerBy项目命令管理工具

Usage:
    powerby-cli init [项目名称]
    powerby-cli update
    powerby-cli status
    powerby-cli clean
"""

import os
import sys
import shutil
import json
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any

# PowerBy命令列表
POWERBY_COMMANDS = [
    "powerby-init",
    "powerby-initialize",
    "powerby-define",
    "powerby-research",
    "powerby-design",
    "powerby-plan",
    "powerby-implement",
    "powerby-review",
    "powerby-quick",
]

class PowerByCLI:
    """PowerBy命令行工具"""

    def __init__(self):
        self.project_root = Path.cwd()
        self.claude_dir = self.project_root / ".claude"
        self.commands_dir = self.claude_dir / "commands"
        self.powerby_dir = self.project_root / ".powerby"
        self.template_dir = Path(__file__).parent / "templates"

    def init(self, project_name: Optional[str] = None) -> int:
        """初始化PowerBy项目"""
        print("🚀 初始化PowerBy项目...")

        # 1. 创建目录结构
        self._create_directories()

        # 2. 安装PowerBy命令
        self._install_commands()

        # 3. 创建项目配置
        self._create_project_config(project_name)

        # 4. 显示成功信息
        self._show_success_message()

        return 0

    def update(self) -> int:
        """更新PowerBy命令到最新版本"""
        print("🔄 更新PowerBy命令...")

        # 1. 清理旧版本
        self._clean_commands()

        # 2. 安装最新版本
        self._install_commands()

        # 3. 显示更新信息
        print("\n✅ PowerBy命令已更新到最新版本")
        self._list_installed_commands()

        return 0

    def status(self) -> int:
        """检查PowerBy项目状态"""
        print("📊 PowerBy项目状态检查\n")

        # 检查目录结构
        self._check_directories()

        # 检查命令文件
        self._check_commands()

        # 检查项目配置
        self._check_project_config()

        return 0

    def clean(self) -> int:
        """清理PowerBy命令和配置"""
        print("🧹 清理PowerBy命令...")

        # 确认操作
        response = input("确定要删除所有PowerBy命令和配置吗？(y/N): ")
        if response.lower() != 'y':
            print("操作已取消")
            return 0

        # 清理命令文件
        self._clean_commands()

        # 清理项目配置
        if self.powerby_dir.exists():
            shutil.rmtree(self.powerby_dir)
            print(f"✅ 已删除: {self.powerby_dir}")

        print("\n✅ 清理完成")

        return 0

    def _create_directories(self):
        """创建必要的目录结构"""
        directories = [
            self.claude_dir,
            self.commands_dir,
            self.powerby_dir,
            self.powerby_dir / "iterations",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"📁 创建目录: {directory.relative_to(self.project_root)}")

    def _install_commands(self):
        """安装PowerBy命令文件"""
        template_commands_dir = self.template_dir / ".claude" / "commands"

        if not template_commands_dir.exists():
            print(f"❌ 错误: 找不到命令模板目录: {template_commands_dir}")
            return 1

        installed_count = 0
        for command_file in template_commands_dir.glob("*.md"):
            dest_file = self.commands_dir / command_file.name
            shutil.copy2(command_file, dest_file)
            print(f"✅ 安装命令: {command_file.name}")
            installed_count += 1

        print(f"\n📦 总计安装 {installed_count} 个命令文件")

    def _clean_commands(self):
        """清理PowerBy命令文件"""
        if not self.commands_dir.exists():
            return

        cleaned_count = 0
        for command_file in self.commands_dir.glob("powerby-*.md"):
            command_file.unlink()
            print(f"🗑️  删除命令: {command_file.name}")
            cleaned_count += 1

        if cleaned_count > 0:
            print(f"\n🧹 总计删除 {cleaned_count} 个命令文件")
        else:
            print("ℹ️  未找到需要清理的命令文件")

    def _create_project_config(self, project_name: Optional[str] = None):
        """创建项目配置文件"""
        if not project_name:
            project_name = self.project_root.name

        config = {
            "name": project_name,
            "description": "",
            "version": "1.0.0",
            "current_phase": "P0",
            "completed_gates": [],
            "status": "initialized",
            "created_at": subprocess.check_output(
                ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                text=True
            ).strip(),
            "team": {
                "product_manager": "",
                "architect": "",
                "engineer": "",
                "reviewer": ""
            },
            "tech_stack": []
        }

        config_file = self.powerby_dir / "project.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"📝 创建配置文件: {config_file}")

        # 创建迭代追踪文件
        iterations_file = self.powerby_dir / "iterations.json"
        with open(iterations_file, 'w', encoding='utf-8') as f:
            json.dump({"iterations": []}, f, indent=2, ensure_ascii=False)

        print(f"📝 创建迭代文件: {iterations_file}")

        # 创建项目宪章文档
        self._create_constitution_doc(project_name)

    def _create_constitution_doc(self, project_name: str):
        """创建项目宪章文档"""
        template_constitution = self.template_dir / "docs" / "constitution.md"

        if not template_constitution.exists():
            print(f"⚠️  警告: 找不到宪章模板: {template_constitution}")
            return

        # 读取模板内容
        with open(template_constitution, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换模板变量
        timestamp = subprocess.check_output(
            ["date", "-u", "+%Y-%m-%d %H:%M:%S UTC"],
            text=True
        ).strip()

        content = content.replace("{{TIMESTAMP}}", timestamp)
        content = content.replace("{{PROJECT_NAME}}", project_name)

        # 写入文档
        constitution_file = self.project_root / "docs" / "constitution.md"
        with open(constitution_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"📜 创建项目宪章: {constitution_file}")

    def _show_success_message(self):
        """显示成功安装信息"""
        print("\n" + "="*50)
        print("✅ PowerBy项目初始化完成！")
        print("="*50)

        print("\n📋 已安装的命令:")
        for cmd in POWERBY_COMMANDS:
            print(f"  • /{cmd}")

        print("\n📁 目录结构:")
        print(f"  ├── .claude/commands/ - PowerBy命令文件")
        print(f"  └── .powerby/ - 项目配置")

        print("\n🎯 下一步:")
        print("  使用 /powerby.initialize 开始项目")

    def _list_installed_commands(self):
        """列出已安装的命令"""
        if not self.commands_dir.exists():
            print("ℹ️  未找到命令目录")
            return

        installed = list(self.commands_dir.glob("powerby-*.md"))
        if not installed:
            print("ℹ️  未安装任何PowerBy命令")
            return

        print("\n📋 已安装的命令:")
        for cmd_file in sorted(installed):
            print(f"  • {cmd_file.name}")

    def _check_directories(self):
        """检查目录结构"""
        print("📁 目录结构检查:")

        checks = [
            (self.claude_dir, ".claude目录"),
            (self.commands_dir, "命令目录"),
            (self.powerby_dir, "PowerBy配置目录"),
        ]

        for path, name in checks:
            status = "✅ 存在" if path.exists() else "❌ 不存在"
            print(f"  {name}: {status}")

    def _check_commands(self):
        """检查命令文件"""
        print("\n📦 命令文件检查:")

        if not self.commands_dir.exists():
            print("  ❌ 命令目录不存在")
            return

        installed = list(self.commands_dir.glob("powerby-*.md"))
        expected = set(POWERBY_COMMANDS)

        for cmd in expected:
            cmd_file = self.commands_dir / f"{cmd}.md"
            status = "✅" if cmd_file.exists() else "❌"
            print(f"  {status} {cmd}.md")

        missing = expected - {f.stem for f in installed}
        if missing:
            print(f"\n⚠️  缺少命令: {', '.join(missing)}")

    def _check_project_config(self):
        """检查项目配置"""
        print("\n⚙️  项目配置检查:")

        config_file = self.powerby_dir / "project.json"
        if config_file.exists():
            print("  ✅ 项目配置文件存在")
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print(f"  📊 当前阶段: {config.get('current_phase', 'N/A')}")
                    print(f"  📊 状态: {config.get('status', 'N/A')}")
            except Exception as e:
                print(f"  ⚠️  配置文件格式错误: {e}")
        else:
            print("  ❌ 项目配置文件不存在")

        iterations_file = self.powerby_dir / "iterations.json"
        if iterations_file.exists():
            print("  ✅ 迭代追踪文件存在")
        else:
            print("  ❌ 迭代追踪文件不存在")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    command = sys.argv[1]
    cli = PowerByCLI()

    if command == "init":
        project_name = sys.argv[2] if len(sys.argv) > 2 else None
        return cli.init(project_name)
    elif command == "update":
        return cli.update()
    elif command == "status":
        return cli.status()
    elif command == "clean":
        return cli.clean()
    else:
        print(f"❌ 未知命令: {command}")
        print(__doc__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
