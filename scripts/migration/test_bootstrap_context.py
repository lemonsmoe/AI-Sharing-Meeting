"""验证迁移不会冒用旧身份、覆盖运行状态或改变源项目。"""

import base64
from contextlib import closing
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import unittest

from bootstrap_context import apply_plan, build_plan, read_json


SOURCE_ROOT = Path(__file__).resolve().parents[2]


class BootstrapContextTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="ai_sharing_migration_")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for relative in ("scripts/context", "tools/project_skills/context-management/scripts"):
            shutil.copytree(SOURCE_ROOT / relative, self.root / relative,
                            ignore=shutil.ignore_patterns("__pycache__"))
        for relative in ("docs/context/project.json", "docs/context/workflow_install.json",
                         "docs/context/migration/task_history.json"):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE_ROOT / relative, target)
        self.manager = os.environ.get("CODEX_THREAD_ID")
        if not self.manager:
            self.skipTest("本接续测试需在真实 Codex 对话中运行")

    def plan(self):
        return build_plan(self.root, self.manager, Path(sys.executable).resolve())

    def test_preview_is_read_only(self):
        before = (self.root / "docs/context/project.json").read_bytes()
        changes = self.plan()
        self.assertEqual(len(changes), 3)
        self.assertEqual(before, (self.root / "docs/context/project.json").read_bytes())
        self.assertFalse((self.root / ".context_runtime").exists())

    def test_apply_binds_paths_without_restoring_old_claims(self):
        apply_plan(self.root, self.plan())
        project = read_json(self.root / "docs/context/project.json")
        self.assertEqual(project["context_root"], self.root.as_posix())
        self.assertEqual(project["manager_thread_id"], self.manager)
        hooks = read_json(self.root / ".codex/hooks.json")["hooks"]
        for groups in hooks.values():
            self.assertIsInstance(groups, list)
            for handler in groups[0]["hooks"]:
                command = handler["command"]
                if os.name == "nt":
                    command = base64.b64decode(command.split()[-1]).decode("utf-16le")
                self.assertIn(self.root.as_posix(), command)
        with closing(sqlite3.connect(self.root / ".context_runtime/tasks.sqlite3")) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], 0)
        self.assertTrue((self.root / ".context_runtime/migration_receipt.json").exists())
        with self.assertRaises(ValueError):
            self.plan()

    def test_existing_live_database_is_protected(self):
        (self.root / ".context_runtime").mkdir()
        with closing(sqlite3.connect(self.root / ".context_runtime/tasks.sqlite3")) as connection:
            connection.execute("CREATE TABLE tasks (id TEXT, data TEXT)")
            connection.execute("INSERT INTO tasks VALUES ('existing', '{}')")
            connection.commit()
        with self.assertRaisesRegex(ValueError, "已有任务"):
            self.plan()

    def test_existing_hooks_are_protected(self):
        (self.root / ".codex").mkdir()
        (self.root / ".codex/hooks.json").write_text('{}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "已有本机 Hook"):
            self.plan()

    def test_missing_identity_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "真实 CODEX_THREAD_ID"):
            build_plan(self.root, None, Path(sys.executable))

    def test_changed_context_program_is_rejected(self):
        path = self.root / "scripts/context/context_hook.py"
        path.write_text("# changed\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "上下文脚本已改变"):
            self.plan()

    def test_bound_source_directory_is_protected(self):
        project = read_json(self.root / "docs/context/project.json")
        project["context_root"] = self.root.as_posix()
        (self.root / "docs/context/project.json").write_text(json.dumps(project), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "不能覆盖原环境"):
            self.plan()


if __name__ == "__main__":
    unittest.main(verbosity=2)
