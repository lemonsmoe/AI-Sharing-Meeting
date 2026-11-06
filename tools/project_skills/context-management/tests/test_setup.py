"""验证初始化、重复执行、配置保留和升级冲突，不模拟真实 Hook 触发。"""

import base64
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from workflow_doctor import doctor
from workflow_installer import INSTALL_PATH, apply_plan, build_plan, digest, hook_groups
from workflow_templates import BLOCK_END, BLOCK_START, json_text


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.parent = Path.cwd() / ".context_runtime/skill_tests"
        self.parent.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=self.parent)
        self.root = Path(self.directory.name).resolve()
        self.environment = patch.dict(os.environ, {"CODEX_THREAD_ID": "test_manager"})
        self.environment.start()

    def tearDown(self):
        self.environment.stop()
        self.assertTrue(self.root.is_relative_to(self.parent.resolve()))
        self.directory.cleanup()

    def plan(self):
        return build_plan(self.root, "测试项目", "test_project", "test_manager")

    def install(self):
        plan = self.plan()
        apply_plan(plan)
        return plan

    def tree(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_preview_no_writes_and_main_explicit(self):
        with self.assertRaisesRegex(ValueError, "必须明确"):
            build_plan(self.root)
        first = self.plan()
        second = self.plan()
        self.assertEqual(first["changes"], second["changes"])
        self.assertEqual(self.tree(), {})

    def test_install_and_repeated_install_preserve_database(self):
        self.install()
        self.assertEqual(doctor(self.root)["errors"], [])
        database = self.root / ".context_runtime/tasks.sqlite3"
        connection = sqlite3.connect(database)
        connection.execute("INSERT INTO tasks VALUES (?, ?)", ("TASK-KEEP", json.dumps({
            "id": "TASK-KEEP", "status": "open", "owner": None})))
        connection.commit()
        connection.close()
        before = self.tree()
        plan = self.plan()
        self.assertEqual(plan["changes"], {})
        apply_plan(plan)
        self.assertEqual(self.tree(), before)

    def test_preserve_agents_existing_hooks_and_facts(self):
        (self.root / "AGENTS.md").write_text("# 旧规则\n必须保留。\n", encoding="utf-8")
        hooks = self.root / ".codex/hooks.json"
        hooks.parent.mkdir()
        external = {"hooks": [{"type": "command", "command": "echo existing"}]}
        hooks.write_text(json_text({"description": "原配置", "hooks": {"Stop": [external]}}), encoding="utf-8")
        current = self.root / "docs/context/00_current/index.md"
        current.parent.mkdir(parents=True)
        current.write_text("# 已确认目标\n保留。", encoding="utf-8")
        self.install()
        self.assertTrue((self.root / "AGENTS.md").read_text(encoding="utf-8").startswith("# 旧规则\n必须保留。"))
        self.assertEqual(current.read_text(encoding="utf-8"), "# 已确认目标\n保留。")
        actual = json.loads(hooks.read_text(encoding="utf-8"))
        self.assertEqual(actual["description"], "原配置")
        self.assertIn(external, actual["hooks"]["Stop"])
        self.assertEqual(len(actual["hooks"]["Stop"]), 2)
        self.assertEqual(self.plan()["changes"], {})

    def test_manual_program_edit_blocks_upgrade_before_writes(self):
        self.install()
        path = self.root / "scripts/context/context_hook.py"
        path.write_text("# 用户修改\n", encoding="utf-8")
        before = self.tree()
        with self.assertRaisesRegex(ValueError, "独立修改"):
            self.plan()
        self.assertEqual(self.tree(), before)
        self.assertTrue(doctor(self.root)["errors"])

    def test_managed_upgrade_has_backup(self):
        self.install()
        path = self.root / "scripts/context/context_hook.py"
        original = b"# older installed program\n"
        path.write_bytes(original)
        metadata = self.root / INSTALL_PATH
        record = json.loads(metadata.read_text(encoding="utf-8"))
        record["managed_files"]["scripts/context/context_hook.py"] = digest(original)
        metadata.write_text(json_text(record), encoding="utf-8")
        backup = apply_plan(self.plan())
        self.assertEqual((Path(backup) / "scripts/context/context_hook.py").read_bytes(), original)
        self.assertEqual(doctor(self.root)["errors"], [])

    def test_changed_agent_block_or_hook_requires_review(self):
        self.install()
        path = self.root / "AGENTS.md"
        original = path.read_text(encoding="utf-8")
        path.write_text(original.replace(BLOCK_END, "自定义规则\n" + BLOCK_END), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "受管区块"):
            self.plan()
        path.write_text(original, encoding="utf-8")
        hooks = self.root / ".codex/hooks.json"
        config = json.loads(hooks.read_text(encoding="utf-8"))
        config["hooks"]["Stop"][0]["hooks"][0]["timeout"] = 7
        hooks.write_text(json_text(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "受管 Hook"):
            self.plan()

    def test_existing_main_not_silently_reassigned(self):
        self.install()
        with self.assertRaisesRegex(ValueError, "不能通过初始化"):
            build_plan(self.root, manager="other")
        with patch.dict(os.environ, {"CODEX_THREAD_ID": "other"}):
            plan = self.plan()
            # 删除一个非业务模板，仅用于隔离测试中的补齐路径。
            (self.root / "docs/context/04_tasks/README.md").unlink()
            plan = self.plan()
            with self.assertRaisesRegex(ValueError, "已登记主对话"):
                apply_plan(plan)

    def test_other_active_claim_blocks_changes(self):
        self.install()
        (self.root / "docs/context/04_tasks/README.md").unlink()
        connection = sqlite3.connect(self.root / ".context_runtime/tasks.sqlite3")
        connection.execute("INSERT INTO tasks VALUES (?, ?)", ("TASK-OTHER", json.dumps({
            "id": "TASK-OTHER", "status": "active", "owner": "other",
            "write_paths": [str(self.root / "docs/context/04_tasks")]})))
        connection.commit()
        connection.close()
        with self.assertRaisesRegex(ValueError, "任务冲突"):
            self.plan()

    def test_doctor_is_read_only(self):
        before = self.tree()
        self.assertTrue(doctor(self.root)["errors"])
        self.assertEqual(self.tree(), before)
        self.install()
        before = self.tree()
        self.assertFalse(doctor(self.root)["errors"])
        self.assertEqual(self.tree(), before)

    def test_change_after_preview_blocks_apply(self):
        plan = self.plan()
        (self.root / "AGENTS.md").write_text("刚刚新增的人工规则", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "预览后文件已变化"):
            apply_plan(plan)
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8"), "刚刚新增的人工规则")
        self.assertFalse((self.root / "scripts").exists())

    def test_claim_after_preview_blocks_apply(self):
        self.install()
        (self.root / "docs/context/04_tasks/README.md").unlink()
        plan = self.plan()
        connection = sqlite3.connect(self.root / ".context_runtime/tasks.sqlite3")
        connection.execute("INSERT INTO tasks VALUES (?, ?)", ("TASK-NEW", json.dumps({
            "id": "TASK-NEW", "status": "active", "owner": "other",
            "write_paths": [str(self.root / "docs/context/04_tasks")]})))
        connection.commit()
        connection.close()
        with self.assertRaisesRegex(ValueError, "执行前出现任务冲突"):
            apply_plan(plan)

    def test_windows_command_preserves_special_path(self):
        if os.name != "nt":
            self.skipTest("仅验证 Windows 编码命令")
        special = self.root / "中文 $目录's"
        command = hook_groups(special, Path(sys.executable))["Stop"]["hooks"][0]["command"]
        decoded = base64.b64decode(command.split()[-1]).decode("utf-16le")
        self.assertIn("中文 $目录''s", decoded)
        self.assertIn("context_hook.py'", decoded)

    def test_cli_preview_apply_and_doctor(self):
        script = Path(__file__).resolve().parents[1] / "scripts/context_setup.py"
        arguments = [sys.executable, str(script), "init", "--root", str(self.root),
                     "--manager-thread-id", "test_manager", "--project-name", "CLI 测试"]
        preview = subprocess.run(arguments, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(json.loads(preview.stdout)["mode"], "preview")
        self.assertEqual(self.tree(), {})
        applied = subprocess.run(arguments + ["--apply"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        checked = subprocess.run([sys.executable, str(script), "doctor", "--root", str(self.root)],
                                 capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(json.loads(checked.stdout)["errors"], [])

    def test_generated_windows_hook_launch_offline(self):
        if os.name != "nt":
            self.skipTest("仅验证 Windows 命令启动")
        special = self.root / "中文 $目录's"
        special.mkdir()
        plan = build_plan(special, "离线启动测试", manager="test_manager")
        apply_plan(plan)
        hooks = json.loads((special / ".codex/hooks.json").read_text(encoding="utf-8"))
        command = hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        payload = json.dumps({"session_id": "manual-validation-only", "hook_event_name": "SessionStart"})
        launched = subprocess.run(command, input=payload, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(launched.returncode, 0, launched.stderr)
        self.assertIn("离线启动测试", json.loads(launched.stdout)["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
    unittest.main()
