"""隔离验证讨论记忆的来源、类型、过期写入与有界整理触发。"""

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets/runtime"))
from discussion_files import atomic_document, load_document, read_topic, topic_paths
from discussion_hook import handle
from discussion_store import acknowledge, consolidate, packet, record_note, sync_context
from task_store import operate


class DiscussionTests(unittest.TestCase):
    def setUp(self):
        self.parent = Path.cwd() / ".context_runtime/discussion_tests"
        self.parent.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=self.parent)
        self.root = Path(self.directory.name).resolve()
        current = self.root / "docs/context/00_current"
        current.mkdir(parents=True)
        (current / "index.md").write_text("# 测试项目\n目标：比较候选平台。", encoding="utf-8")
        (self.root / "docs/context/project.json").write_text(json.dumps({
            "manager_thread_id": "manager", "manager_paths": ["AGENTS.md"]}), encoding="utf-8")
        self.claim("TASK-A", "a", "docs/context/05_discussions")

    def tearDown(self):
        self.assertTrue(self.root.is_relative_to(self.parent.resolve()))
        self.directory.cleanup()

    def claim(self, task, owner, scope):
        operate(self.root, "create", owner, task, title="隔离测试", domain="test",
                acceptance="检查讨论记忆行为", write_paths=[scope])
        operate(self.root, "claim", owner, task)

    def note(self, text="候选采用平台甲，尚未决定", topic="platform", extra=None):
        payload = dict(topic=topic, title="平台选择", abstract="比较平台候选与未决条件",
                       source_message="隔离测试消息，不是项目事实", items=[dict(kind="proposal", text=text)])
        if extra:
            payload["items"].append(extra)
        return record_note(self.root, "a", "TASK-A", payload)

    def summary(self, topic="platform"):
        material = packet(self.root, topic)
        state = read_topic(self.root, topic)
        points = [dict(kind=item["kind"], text=item["text"], sources=[f"{note['note_id']}#{i}"])
                  for note in state["notes"] for i, item in enumerate(note["items"])]
        return dict(topic=topic, title="平台讨论", abstract="存在候选，等待条件核对",
                    notes_revision=material["notes_revision"], base_summary_revision=material["base_summary_revision"], points=points)

    def test_record_requires_owner_scope_and_valid_topic(self):
        payload = dict(topic="platform", title="测试", abstract="测试", source_message="测试", items=[dict(kind="proposal", text="候选")])
        with self.assertRaisesRegex(ValueError, "正在认领"):
            record_note(self.root, "b", "TASK-A", payload)
        with self.assertRaisesRegex(ValueError, "snake_case"):
            record_note(self.root, "a", "TASK-A", dict(payload, topic="../../outside"))
        operate(self.root, "release", "a", "TASK-A")
        self.claim("TASK-NARROW", "a", "src")
        with self.assertRaisesRegex(ValueError, "认领范围"):
            record_note(self.root, "a", "TASK-NARROW", payload)

    def test_record_deduplicates_and_preserves_source(self):
        first, second = self.note(), self.note()
        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])
        state = read_topic(self.root, "platform")
        self.assertEqual(len(state["notes"]), 1)
        self.assertEqual(state["notes"][0]["author_thread"], "a")
        self.assertIn("隔离测试", state["notes"][0]["source_message"])
        self.assertTrue(state["pending"])

    def test_user_confirmation_needs_evidence(self):
        with self.assertRaisesRegex(ValueError, "确认依据"):
            self.note(extra=dict(kind="user_confirmed", text="已选平台甲"))

    def test_summary_cannot_promote_candidate(self):
        self.note()
        value = self.summary()
        value["points"][0]["kind"] = "user_confirmed"
        with self.assertRaisesRegex(ValueError, "候选升级"):
            consolidate(self.root, "a", "TASK-A", value)
        self.assertTrue(read_topic(self.root, "platform")["pending"])

    def test_summary_requires_coverage_or_explicit_omission(self):
        self.note(extra=dict(kind="question", text="显存是否足够？"))
        value = self.summary()
        omitted_point = value["points"].pop()
        with self.assertRaisesRegex(ValueError, "漏掉"):
            consolidate(self.root, "a", "TASK-A", value)
        value["omitted"] = [dict(source=omitted_point["sources"][0], reason="暂留原记录，等待实测资源")]
        consolidate(self.root, "a", "TASK-A", value)
        self.assertFalse(read_topic(self.root, "platform")["pending"])

    def test_new_record_invalidates_old_summary_packet(self):
        self.note()
        old = self.summary()
        self.note("另一个候选是平台乙")
        with self.assertRaisesRegex(ValueError, "出现新记录"):
            consolidate(self.root, "a", "TASK-A", old)
        self.assertEqual(len(read_topic(self.root, "platform")["notes"]), 2)

    def test_changed_summary_invalidates_old_writer(self):
        self.note()
        old = self.summary()
        consolidate(self.root, "a", "TASK-A", old)
        with self.assertRaisesRegex(ValueError, "总结变化"):
            consolidate(self.root, "a", "TASK-A", old)

    def test_incremental_packet_keeps_previous_summary_and_new_notes(self):
        self.note()
        consolidate(self.root, "a", "TASK-A", self.summary())
        self.assertEqual(packet(self.root, "platform")["new_notes"], [])
        self.note("还需核查平台乙的接口")
        material = packet(self.root, "platform")
        self.assertIsNotNone(material["previous_summary"])
        self.assertEqual(len(material["new_notes"]), 1)

    def test_changed_note_is_reexposed_for_review(self):
        result = self.note()
        consolidate(self.root, "a", "TASK-A", self.summary())
        path = self.root / result["path"]
        note, body = load_document(path)
        note["items"][0]["text"] = "测试手工纠错后的候选"
        atomic_document(path, note, body)
        self.assertEqual(len(packet(self.root, "platform")["new_notes"]), 1)

    def test_sync_does_not_acknowledge_and_later_update_reappears(self):
        self.note()
        first = sync_context(self.root, "b")["topics"][0]
        self.assertTrue(first["changed"])
        self.assertTrue(sync_context(self.root, "b")["topics"][0]["changed"])
        acknowledge(self.root, "b", "platform", first["revision"])
        self.assertFalse(sync_context(self.root, "b")["topics"][0]["changed"])
        self.note("新增一个未决条件")
        self.assertTrue(sync_context(self.root, "b")["topics"][0]["changed"])
        with self.assertRaisesRegex(ValueError, "已有更新"):
            acknowledge(self.root, "b", "platform", first["revision"])

    def test_stop_requests_only_one_continuation(self):
        self.note()
        payload = dict(session_id="a", hook_event_name="Stop", turn_id="turn_one")
        self.assertEqual(handle(payload, self.root)["decision"], "block")
        self.assertEqual(handle(payload, self.root), {})
        self.assertEqual(handle(dict(payload, stop_hook_active=True), self.root), {})
        self.assertTrue(read_topic(self.root, "platform")["pending"])

    def test_stop_after_success_does_not_continue(self):
        self.note()
        consolidate(self.root, "a", "TASK-A", self.summary())
        self.assertEqual(handle(dict(session_id="a", hook_event_name="Stop"), self.root), {})

    def test_failed_batch_is_not_forced_again_on_every_turn(self):
        self.note()
        first = dict(session_id="a", hook_event_name="Stop", turn_id="first")
        self.assertEqual(handle(first, self.root)["decision"], "block")
        self.assertEqual(handle(dict(first, turn_id="later"), self.root), {})
        self.note("新增讨论形成新一批")
        self.assertEqual(handle(dict(first, turn_id="new_batch"), self.root)["decision"], "block")

    def test_plan_mode_does_not_force_writing(self):
        self.note()
        self.assertEqual(handle(dict(session_id="a", hook_event_name="Stop", permission_mode="plan"), self.root), {})

    def test_other_reader_discovers_queue_without_forced_continuation(self):
        self.note()
        started = handle(dict(session_id="b", hook_event_name="SessionStart"), self.root)
        self.assertIn("pending=True", started["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(handle(dict(session_id="b", hook_event_name="Stop"), self.root), {})

    def test_summary_claim_owned_elsewhere_is_not_stolen(self):
        self.note()
        operate(self.root, "release", "a", "TASK-A")
        path = topic_paths(self.root, "platform", "b")["summary_path"]
        self.claim("TASK-B", "b", path)
        self.assertEqual(handle(dict(session_id="a", hook_event_name="Stop", turn_id="busy"), self.root), {})
        with self.assertRaisesRegex(ValueError, "正在认领"):
            consolidate(self.root, "a", "TASK-B", self.summary())

    def test_independent_notes_can_be_written_concurrently(self):
        operate(self.root, "release", "a", "TASK-A")
        for owner in ("a", "b"):
            self.claim("TASK-" + owner, owner, topic_paths(self.root, "platform", owner)["note_scope"])
        def write(owner):
            payload = dict(topic="platform", title="测试", abstract="并发候选", source_message="隔离并发测试",
                           items=[dict(kind="proposal", text="来自 " + owner)])
            return record_note(self.root, owner, "TASK-" + owner, payload)
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(write, ["a", "b"]))
        self.assertEqual(len(read_topic(self.root, "platform")["notes"]), 2)
        self.assertNotEqual(results[0]["path"], results[1]["path"])


if __name__ == "__main__":
    unittest.main()
