"""讨论记录、整理材料、增量阅读和有来源的议题总结。"""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sqlite3
import sys

from discussion_files import (BASE_PATH, KINDS, all_topics, atomic_document, checked_path,
                              note_body, read_topic, sha, source_items, summary_body, topic_paths)
from task_store import DEFAULT_ROOT, all_tasks, canonical_path, connect, now


@contextmanager
def state_connection(root):
    connection = connect(root)
    connection.execute("CREATE TABLE IF NOT EXISTS discussion_reads (session TEXT, topic TEXT, revision TEXT, PRIMARY KEY(session, topic))")
    connection.execute("CREATE TABLE IF NOT EXISTS discussion_stops (session TEXT, turn_key TEXT, PRIMARY KEY(session, turn_key))")
    connection.commit()
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def require_claim(connection, root, session, task_id, path):
    tasks = all_tasks(connection)
    task = next((item for item in tasks if item["id"] == task_id), None)
    if not task or task["owner"] != session or task["status"] != "active":
        raise ValueError("讨论写入需要本对话正在认领的任务 --task")
    target = Path(canonical_path(root, path))
    if not any(target.is_relative_to(Path(scope)) for scope in task["write_paths"]):
        raise ValueError("讨论写入路径不在该任务认领范围内")
    for other in tasks:
        if other["status"] == "active" and other["id"] != task_id:
            if any(target.is_relative_to(Path(scope)) or Path(scope).is_relative_to(target) for scope in other["write_paths"]):
                raise ValueError("讨论文件与其他 active 任务范围冲突")


def validate_items(items):
    if not isinstance(items, list) or not 1 <= len(items) <= 40:
        raise ValueError("每条记录需要1至40个条目")
    for item in items:
        if item.get("kind") not in KINDS or not isinstance(item.get("text"), str) or not item["text"].strip():
            raise ValueError("条目需要有效 kind 与非空 text")
        if len(item["text"]) > 6000:
            raise ValueError("单条讨论过长，请分条提取")
        if item["kind"] == "user_confirmed" and not item.get("evidence", "").strip():
            raise ValueError("用户已确认条目必须附实际原话或确认依据")


def record_note(root, session, task_id, payload):
    for field in ("topic", "title", "abstract", "source_message"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise ValueError("记录缺少：" + field)
    if len(payload["abstract"]) > 500:
        raise ValueError("记录摘要最多500字符")
    validate_items(payload.get("items"))
    paths = topic_paths(root, payload["topic"], session)
    content = {key: payload[key] for key in ("topic", "title", "abstract", "source_message", "items")}
    identifier = "note_" + sha((session + json.dumps(content, ensure_ascii=False, sort_keys=True)).encode())[:20]
    relative = paths["note_scope"] + "/" + identifier + ".md"
    path = checked_path(root, relative)
    with state_connection(root) as connection:
        connection.execute("BEGIN IMMEDIATE")
        require_claim(connection, root, session, task_id, relative)
        if path.exists():
            return dict(note_id=identifier, path=relative, duplicate=True)
        note = dict(content, note_id=identifier, author_thread=session, recorded_at=now())
        atomic_document(path, note, note_body(note))
    return dict(note_id=identifier, path=relative, duplicate=False, pending=True)


def packet(root, topic):
    state = read_topic(root, topic)
    if not state["notes"]:
        raise ValueError("该议题尚无讨论记录")
    previous = state["summary"]
    covered = set(previous.get("covered_sources", [])) if previous else set()
    new_notes = []
    for note in state["notes"]:
        unchanged = previous and previous.get("note_fingerprints", {}).get(note["note_id"]) == note["file_revision"]
        items = [dict(item, source=f"{note['note_id']}#{i}") for i, item in enumerate(note["items"])
                 if not unchanged or f"{note['note_id']}#{i}" not in covered]
        if items:
            new_notes.append(dict(path=note["path"], source_message=note["source_message"],
                                  author_thread=note["author_thread"], items=items))
    return dict(topic=topic, notes_revision=state["notes_revision"],
                base_summary_revision=state["summary_revision"], summary_path=state["summary_path"],
                previous_summary=previous, new_notes=new_notes,
                required_sources=list(source_items(state)),
                instruction="保留候选、问题、约束和异议。points 每项含 kind/text/sources，kind须与引用原条目一致；遗漏项逐条写 omitted 的 source/reason。摘要是讨论状态，不是决策批准。")


def consolidate(root, session, task_id, payload):
    state = read_topic(root, payload["topic"])
    with state_connection(root) as connection:
        connection.execute("BEGIN IMMEDIATE")
        require_claim(connection, root, session, task_id, state["summary_path"])
        state = read_topic(root, payload["topic"])
        if payload.get("notes_revision") != state["notes_revision"] or payload.get("base_summary_revision", "") != state["summary_revision"]:
            raise ValueError("整理期间出现新记录或总结变化，请重新 packet 合并，不能覆盖新进展")
        items = source_items(state)
        if not items:
            raise ValueError("没有可整理的讨论")
        covered = set()
        points = payload.get("points", [])
        if not isinstance(points, list) or not points:
            raise ValueError("总结需要 points")
        for point in points:
            if point.get("kind") not in KINDS or not point.get("text", "").strip() or not point.get("sources"):
                raise ValueError("总结条目需要 kind/text/sources")
            for source in point["sources"]:
                if source not in items or items[source]["kind"] != point["kind"]:
                    raise ValueError("来源不存在或状态被改变，不能把候选升级为已确认")
                covered.add(source)
        for item in payload.get("omitted", []):
            if item.get("source") not in items or not item.get("reason", "").strip():
                raise ValueError("未纳入条目必须引用来源并说明原因")
            covered.add(item["source"])
        if covered != set(items):
            raise ValueError("总结漏掉了讨论条目，须引用或逐条说明暂不纳入的原因")
        if not payload.get("title", "").strip() or not payload.get("abstract", "").strip() or len(payload["abstract"]) > 500:
            raise ValueError("总结需要 title 和不超过500字符的 abstract")
        summary = {key: payload[key] for key in ("topic", "title", "abstract", "points")}
        summary.update(omitted=payload.get("omitted", []), notes_revision=state["notes_revision"],
                       note_fingerprints={note["note_id"]: note["file_revision"] for note in state["notes"]},
                       covered_sources=sorted(covered), author_thread=session, updated_at=now(), path=state["summary_path"])
        atomic_document(checked_path(root, state["summary_path"]), summary, summary_body(summary, state["notes"]))
    return dict(path=state["summary_path"], covered_sources=len(covered), pending=False)


def read_cursors(root, session):
    database = root / ".context_runtime/tasks.sqlite3"
    if not database.exists():
        return {}
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        return dict(connection.execute("SELECT topic,revision FROM discussion_reads WHERE session=?", (session,)))
    except sqlite3.OperationalError as error:
        if "no such table" not in str(error):
            raise
        return {}
    finally:
        connection.close()


def sync_context(root, session, topic=None, limit=8):
    states = [read_topic(root, topic)] if topic else all_topics(root)
    cursors = read_cursors(root, session)
    topics = []
    for state in states:
        if not state["notes"]:
            continue
        last_note = max(state["notes"], key=lambda item: item["recorded_at"])
        summary = state["summary"]
        topics.append(dict(topic=state["topic"], revision=state["revision"],
                           changed=cursors.get(state["topic"]) != state["revision"], pending=state["pending"],
                           title=summary["title"] if summary else last_note["title"],
                           abstract=summary["abstract"] if summary else last_note["abstract"],
                           summary_path=state["summary_path"] if summary else None,
                           note_paths=[note["path"] for note in state["notes"]],
                           updated_at=last_note["recorded_at"],
                           points=summary["points"] if topic and summary else None))
    topics.sort(key=lambda item: (item["changed"], item["updated_at"]), reverse=True)
    index = root / "docs/context/00_current/index.md"
    brief = index.read_text(encoding="utf-8-sig").split("\n## ", 1)[0][:1600] if index.exists() else ""
    return dict(project_brief=brief, topics=topics[:limit], omitted_topics=max(0, len(topics) - limit),
                note="pending=true 时总结可能落后，应读新记录；ack 只在实际读完后执行，不能把注入当成已阅读。")


def acknowledge(root, session, topic, revision):
    state = read_topic(root, topic)
    if state["revision"] != revision:
        raise ValueError("阅读后议题已有更新，请再次 sync，不能标记新内容为已读")
    with state_connection(root) as connection:
        connection.execute("INSERT OR REPLACE INTO discussion_reads VALUES (?,?,?)", (session, topic, revision))
    return dict(topic=topic, acknowledged=revision)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["paths", "record", "packet", "consolidate", "sync", "ack"])
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--topic")
    parser.add_argument("--task")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--revision")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    session = os.environ.get("CODEX_THREAD_ID")
    if not session:
        parser.error("需要真实 CODEX_THREAD_ID，不支持通过参数假冒其他对话")
    root = args.root.resolve()
    if args.action in ("paths", "packet", "ack") and not args.topic:
        parser.error("此操作需要 --topic")
    if args.action in ("record", "consolidate"):
        if not args.task:
            parser.error("写入需要 --task")
        payload = json.loads(args.input.read_text(encoding="utf-8-sig")) if args.input else json.load(sys.stdin)
        result = record_note(root, session, args.task, payload) if args.action == "record" else consolidate(root, session, args.task, payload)
    elif args.action == "paths":
        result = topic_paths(root, args.topic, session)
    elif args.action == "packet":
        result = packet(root, args.topic)
    elif args.action == "ack":
        result = acknowledge(root, session, args.topic, args.revision)
    else:
        if not 1 <= args.limit <= 100:
            parser.error("limit 应为1至100")
        result = sync_context(root, session, args.topic, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, sqlite3.Error) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
