"""注入短上下文并记录触发回执，不读取聊天正文、不自动批准决策。"""

import hashlib
import json
import os
from pathlib import Path
import sys

from task_store import DEFAULT_ROOT, now, snapshot


def handle(payload, root=DEFAULT_ROOT):
    event = payload.get("hook_event_name", "SessionStart")
    session = payload.get("session_id") or os.environ.get("CODEX_THREAD_ID", "unknown")
    state = snapshot(root)
    receipt_dir = root / ".context_runtime/hook_receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    path = receipt_dir / (hashlib.sha256(session.encode()).hexdigest()[:20] + ".json")
    previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    owned = [task for task in state["tasks"] if task["owner"] == session and task["status"] == "active"]
    receipt = dict(session_id=session, event=event, source=payload.get("source"),
                   observed_at=now(), revision=state["revision"],
                   active_tasks=[task["id"] for task in owned],
                   event_counts=previous.get("event_counts", {}))
    receipt["event_counts"][event] = receipt["event_counts"].get(event, 0) + 1
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    if event == "Stop":
        if owned and not payload.get("stop_hook_active"):
            return {"systemMessage": "本对话仍有已认领任务，请确认是继续工作还是提交交接；不会自动释放或宣告完成。"}
        return {}
    project = json.loads((root / "docs/context/project.json").read_text(encoding="utf-8"))
    name = project.get("project_name") or project.get("project_id", "项目")
    lines = [f"{name} 公共上下文版本：{state['revision']}；当前对话：{session}。",
             "遵循项目 AGENTS.md。纯解释可只读；有持久写入的任务先认领，禁止覆盖其他对话的写入范围。",
             "主对话维护全局规划；侧边建议必须保留为候选，不能自动提升为已确认决定。"]
    if event == "SessionStart" or previous.get("revision") != state["revision"]:
        lines += ["当前状态有更新或本次为会话开始：", (root / "docs/context/00_current/index.md").read_text(encoding="utf-8")[:2200]]
    else:
        lines.append("公共状态未变化，无需全量重读；依赖事实按风险与证据变化核验。")
    for task in state["tasks"]:
        if task["status"] in ("active", "review"):
            lines.append(f"{task['id']} | {task['status']} | {task['owner']} | 写入范围 {task['write_paths']}")
    lines.append("任务完成后记录事件、刷新相关领域、提交任务结果和证据；纯问答不强制留事件。")
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": "\n".join(lines)[:5000]}}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        print(json.dumps(handle(json.load(sys.stdin)), ensure_ascii=False))
    except Exception as error:
        # 辅助上下文故障不阻断用户工作，明确报告，退回 AGENTS.md 入口。
        print(json.dumps({"systemMessage": f"上下文 Hook 失败，请按 AGENTS.md 手动读取：{error}"}, ensure_ascii=False))
