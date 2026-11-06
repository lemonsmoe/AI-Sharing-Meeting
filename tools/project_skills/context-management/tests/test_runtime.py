"""验证并发认领、权限边界和非阻断 Hook。"""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets/runtime"))
from context_hook import handle
from task_store import operate, snapshot


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.test_parent = Path.cwd() / ".context_runtime/skill_tests"
        self.test_parent.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=self.test_parent)
        self.root = Path(self.directory.name)
        current = self.root / "docs/context/00_current"
        current.mkdir(parents=True)
        (current / "index.md").write_text("# 测试项目\n候选不等于已确认。", encoding="utf-8")
        (self.root / "docs/context/project.json").write_text(json.dumps({
            "manager_thread_id": "manager", "manager_paths": ["AGENTS.md"]}), encoding="utf-8")

    def tearDown(self):
        self.assertTrue(self.root.resolve().is_relative_to(self.test_parent.resolve()))
        self.directory.cleanup()

    def create(self, name="TASK-A", path="src/a.py", depends=None):
        return operate(self.root, "create", "creator", name, title="测试", domain="test",
                       acceptance="检查通过", write_paths=[path], depends=depends or [])

    def test_parent_child_claim_conflict(self):
        self.create(path="src")
        self.create("TASK-B", "src/a.py")
        operate(self.root, "claim", "one", "TASK-A")
        with self.assertRaisesRegex(ValueError, "写入范围冲突"):
            operate(self.root, "claim", "two", "TASK-B")

    def test_parallel_claim_has_one_winner(self):
        self.create()
        self.create("TASK-B")

        def claim(task_id):
            try:
                operate(self.root, "claim", task_id, task_id)
                return True
            except ValueError:
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(claim, ["TASK-A", "TASK-B"]))
        self.assertEqual(sum(results), 1)

    def test_non_owner_cannot_release(self):
        self.create()
        operate(self.root, "claim", "one", "TASK-A")
        with self.assertRaises(ValueError):
            operate(self.root, "release", "two", "TASK-A")

    def test_review_requires_manager_and_evidence(self):
        self.create()
        operate(self.root, "claim", "one", "TASK-A")
        with self.assertRaises(ValueError):
            operate(self.root, "finish", "one", "TASK-A", result="完成")
        operate(self.root, "finish", "one", "TASK-A", result="完成", evidence="报告")
        with self.assertRaises(ValueError):
            operate(self.root, "review", "one", "TASK-A", accept=True)
        result = operate(self.root, "review", "manager", "TASK-A", accept=True)
        self.assertEqual(result["status"], "accepted")

    def test_dependencies_and_macro_ownership(self):
        self.create()
        self.create("TASK-B", "other.py", ["TASK-A"])
        with self.assertRaisesRegex(ValueError, "依赖"):
            operate(self.root, "claim", "two", "TASK-B")
        self.create("TASK-C", "AGENTS.md")
        with self.assertRaisesRegex(ValueError, "主对话"):
            operate(self.root, "claim", "two", "TASK-C")

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            self.create(path="../outside.py")

    def test_recovery_requires_manager_and_stop_evidence(self):
        self.create()
        operate(self.root, "claim", "one", "TASK-A")
        for session, evidence in [("two", "用户已确认停止"), ("manager", "")]:
            with self.assertRaises(ValueError):
                operate(self.root, "recover", session, "TASK-A", evidence=evidence)
        result = operate(self.root, "recover", "manager", "TASK-A", evidence="用户已确认原对话停止写入")
        self.assertEqual(result["status"], "open")

    def test_hook_refresh_and_stop_do_not_complete_tasks(self):
        self.create()
        operate(self.root, "claim", "one", "TASK-A")
        first = handle({"session_id": "one", "hook_event_name": "SessionStart"}, self.root)
        self.assertIn("测试项目", first["hookSpecificOutput"]["additionalContext"])
        second = handle({"session_id": "one", "hook_event_name": "UserPromptSubmit"}, self.root)
        self.assertIn("未变化", second["hookSpecificOutput"]["additionalContext"])
        stop = handle({"session_id": "one", "hook_event_name": "Stop"}, self.root)
        self.assertNotIn("decision", stop)
        self.assertEqual(snapshot(self.root)["tasks"][0]["status"], "active")
        self.assertEqual(handle({"session_id": "one", "hook_event_name": "Stop", "stop_hook_active": True}, self.root), {})


if __name__ == "__main__":
    unittest.main()
