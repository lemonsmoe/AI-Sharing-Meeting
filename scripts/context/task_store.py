"""项目任务与写入范围认领；仅使用 Python 标准库。"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone
from uuid import uuid4


DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(root):
    runtime = root / ".context_runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(runtime / "tasks.sqlite3", timeout=10)
    connection.execute("PRAGMA busy_timeout=10000")
    connection.execute("CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, data TEXT NOT NULL)")
    connection.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, time TEXT, session TEXT, task TEXT, operation TEXT)")
    connection.commit()
    return connection


def all_tasks(connection):
    return [json.loads(row[0]) for row in connection.execute("SELECT data FROM tasks ORDER BY id")]


def canonical_path(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("认领范围必须位于本项目内")
    return os.path.normcase(str(path))


def overlaps(first, second):
    first, second = Path(first), Path(second)
    return first.is_relative_to(second) or second.is_relative_to(first)


def export_tasks(root, tasks):
    """可读文件是数据库的派生视图，不允许手工改写。"""
    target = root / "docs/context/04_tasks"
    target.mkdir(parents=True, exist_ok=True)
    for task in tasks:
        lines = [f"# {task['id']} {task['title']}", "", "自动生成；任务状态以 .context_runtime/tasks.sqlite3 为准。", "",
                 f"- 状态：{task['status']}", f"- 责任对话：{task['owner'] or '尚未认领'}",
                 f"- 领域：{task['domain']}", f"- 更新时间：{task['updated_at']}",
                 f"- 依赖：{', '.join(task['depends']) or '无'}", f"- 验收标准：{task['acceptance']}",
                 f"- 结果：{task.get('result', '') or '暂无'}", f"- 证据：{task.get('evidence', '') or '暂无'}", "", "## 写入范围", ""]
        lines.extend(f"- {item}" for item in task["write_paths"])
        path = target / f"{task['id']}.md"
        temp = path.with_name(path.name + f".{uuid4().hex}.tmp")
        temp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.replace(temp, path)


def manager_id(root):
    return json.loads((root / "docs/context/project.json").read_text(encoding="utf-8"))["manager_thread_id"]


def operate(root, action, session, task_id=None, **values):
    connection = connect(root)
    try:
        connection.execute("BEGIN IMMEDIATE")
        tasks = all_tasks(connection)
        by_id = {task["id"]: task for task in tasks}
        if action == "create":
            task_id = task_id or f"TASK-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8]}"
            if not task_id.replace("-", "").isalnum() or task_id in by_id:
                raise ValueError("任务编号无效或已经存在")
            for item in values.get("depends", []):
                if item not in by_id:
                    raise ValueError(f"依赖任务不存在：{item}")
            task = dict(id=task_id, title=values["title"], domain=values["domain"],
                        acceptance=values["acceptance"], depends=values.get("depends", []),
                        write_paths=[canonical_path(root, item) for item in values["write_paths"]],
                        owner=None, status="open", created_at=now())
        else:
            if task_id not in by_id:
                raise ValueError("任务不存在")
            task = by_id[task_id]
            if action == "claim":
                if task["status"] != "open":
                    raise ValueError(f"任务不可认领：{task['status']}；责任对话 {task['owner']}")
                if any(by_id[item]["status"] != "accepted" for item in task["depends"]):
                    raise ValueError("依赖尚未验收")
                protected = json.loads((root / "docs/context/project.json").read_text(encoding="utf-8"))["manager_paths"]
                for path in task["write_paths"]:
                    if session != manager_id(root) and any(overlaps(path, canonical_path(root, item)) for item in protected):
                        raise ValueError("范围包含主对话维护文件，请缩小范围或交给主对话")
                for other in tasks:
                    if other["status"] == "active" and any(overlaps(a, b) for a in task["write_paths"] for b in other["write_paths"]):
                        raise ValueError(f"写入范围冲突：{other['id']}，责任对话 {other['owner']}")
                task.update(owner=session, status="active")
            elif action in ("release", "finish"):
                if task["owner"] != session or task["status"] != "active":
                    raise ValueError("只有正在负责该任务的对话可以提交或释放")
                if action == "finish":
                    if not values.get("result") or not values.get("evidence"):
                        raise ValueError("提交必须提供结果与证据")
                    task.update(status="review", result=values["result"], evidence=values["evidence"])
                else:
                    task.update(status="open", owner=None)
            elif action == "review":
                if session != manager_id(root) or task["status"] != "review":
                    raise ValueError("只有主对话可以验收待审任务")
                task.update(status="accepted" if values["accept"] else "open", owner=None,
                            review_note=values.get("result", ""))
            elif action == "recover":
                if session != manager_id(root) or task["status"] != "active" or not values.get("evidence"):
                    raise ValueError("仅主对话可回收 active 任务，且须提供用户确认原负责人已停止写入的证据")
                task.update(status="open", owner=None, recovery_evidence=values["evidence"])
            else:
                raise ValueError("未知操作")
        task["updated_at"] = now()
        connection.execute("INSERT OR REPLACE INTO tasks VALUES (?, ?)", (task_id, json.dumps(task, ensure_ascii=False)))
        connection.execute("INSERT INTO history(time, session, task, operation) VALUES (?, ?, ?, ?)", (now(), session, task_id, action))
        connection.commit()
        # 在事务外导出最新快照，使用唯一临时文件；跨进程导出可能滞后，以数据库查询为准。
        export_tasks(root, all_tasks(connection))
        return task
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def snapshot(root):
    connection = connect(root)
    try:
        tasks = all_tasks(connection)
    finally:
        connection.close()
    files = [root / name for name in ["AGENTS.md", "docs/context/00_current/index.md",
             "docs/context/project.json", "docs/context/facts.json", "docs/runbooks/context_workflow.md"]
             if (root / name).exists()]
    files += sorted((root / "docs/context/00_current/domains").glob("*.md"))
    files += sorted((root / "docs/context/01_decisions").rglob("*.md"))
    digest = hashlib.sha256()
    for path in files:
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    digest.update(json.dumps(tasks, sort_keys=True, ensure_ascii=False).encode())
    return dict(revision=digest.hexdigest()[:16], tasks=tasks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["status", "create", "claim", "release", "finish", "review", "recover", "export"])
    parser.add_argument("task_id", nargs="?")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--session", default=os.environ.get("CODEX_THREAD_ID"))
    parser.add_argument("--title")
    parser.add_argument("--domain", default="docs-process")
    parser.add_argument("--write-path", action="append", default=[])
    parser.add_argument("--depends", action="append", default=[])
    parser.add_argument("--acceptance")
    parser.add_argument("--result")
    parser.add_argument("--evidence")
    parser.add_argument("--accept", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.action in ("status", "export"):
        result = snapshot(root)
        if args.action == "export":
            export_tasks(root, result["tasks"])
    else:
        if not args.session:
            parser.error("需要 CODEX_THREAD_ID 或 --session，以区分责任对话")
        if args.action == "create" and not (args.title and args.acceptance and args.write_path):
            parser.error("创建任务需要 --title、--acceptance 和至少一个 --write-path")
        result = operate(root, args.action, args.session, args.task_id, title=args.title,
                         domain=args.domain, acceptance=args.acceptance, write_paths=args.write_path,
                         depends=args.depends, result=args.result, evidence=args.evidence, accept=args.accept)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main()
    except (ValueError, sqlite3.Error) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
