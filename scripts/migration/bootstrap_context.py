"""在新克隆中重绑上下文和 Hook；默认预览，旧任务仅留作历史档案。"""

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def safe_path(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"路径指向克隆外部：{relative}")
    return path


def build_plan(root, manager, python_path):
    root = root.resolve()
    if sys.version_info < (3, 11):
        raise ValueError("需要 Python 3.11+")
    if not manager:
        raise ValueError("必须在新主对话中运行，使用真实 CODEX_THREAD_ID；不要编造 ID")
    config_path = safe_path(root, "docs/context/project.json")
    project = read_json(config_path)
    snapshot = read_json(safe_path(root, "docs/context/migration/task_history.json"))
    if snapshot.get("schema_version") != 1 or snapshot["source_project"]["project_id"] != project["project_id"]:
        raise ValueError("任务历史与项目身份不匹配")
    if Path(project["context_root"]).resolve() == root:
        raise ValueError("此目录已绑定当前路径；迁移脚本只用于新克隆，不能覆盖原环境")
    runtime = safe_path(root, ".context_runtime")
    database = safe_path(root, ".context_runtime/tasks.sqlite3")
    if (runtime / "migration_receipt.json").exists():
        raise ValueError("本克隆已迁移，禁止重复重置")
    if database.exists():
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as connection:
            tables = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            for table in tables:
                if table not in {"tasks", "history", "discussion_reads", "discussion_stops"}:
                    raise ValueError("发现未知数据库表，需人工检查")
                if connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]:
                    raise ValueError("新环境已有任务或阅读状态，不能覆盖；请使用干净克隆")
    hooks_path = safe_path(root, ".codex/hooks.json")
    if hooks_path.exists():
        raise ValueError("已有本机 Hook 配置，不能覆盖；请先人工核对或使用干净克隆")
    manifest = read_json(safe_path(root, "docs/context/workflow_install.json"))
    for relative, expected in manifest["managed_files"].items():
        actual = hashlib.sha256(safe_path(root, relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"上下文脚本已改变，请先核对安装版本：{relative}")
    templates = safe_path(root, "tools/project_skills/context-management/scripts")
    sys.path.insert(0, str(templates))
    spec = importlib.util.spec_from_file_location("migration_installer", templates / "workflow_installer.py")
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    groups = installer.hook_groups(root, python_path)
    project.update(context_root=root.as_posix(), manager_thread_id=manager,
                   hook_acceptance="pending_user_trust_and_live_test")
    manifest.update(context_root=root.as_posix(), python_path=str(python_path), owned_hooks=groups)
    return {
        "docs/context/project.json": json_bytes(project),
        "docs/context/workflow_install.json": json_bytes(manifest),
        ".codex/hooks.json": json_bytes({"hooks": {event: [group] for event, group in groups.items()}}),
    }


def apply_plan(root, changes):
    runtime = safe_path(root, ".context_runtime")
    backup = runtime / "migration_backups"
    for relative in changes:
        path = safe_path(root, relative)
        if path.exists():
            original = backup / relative
            original.parent.mkdir(parents=True, exist_ok=True)
            original.write_bytes(path.read_bytes())
    for relative, data in changes.items():
        path = safe_path(root, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    with closing(sqlite3.connect(runtime / "tasks.sqlite3")) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, data TEXT NOT NULL)")
        connection.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, time TEXT, session TEXT, task TEXT, operation TEXT)")
        connection.commit()
    receipt = dict(time=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   root=root.as_posix(), manager_thread_id=os.environ["CODEX_THREAD_ID"],
                   old_tasks="保留在 docs/context/migration/task_history.json；未导入运行数据库",
                   production="paused; migration does not resume production")
    (runtime / "migration_receipt.json").write_bytes(json_bytes(receipt))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    changes = build_plan(root, os.environ.get("CODEX_THREAD_ID"), Path(sys.executable).resolve())
    print(json.dumps(dict(mode="apply" if args.apply else "preview", files=list(changes),
                          root=root.as_posix(), manager=os.environ.get("CODEX_THREAD_ID"),
                          tasks="新运行库为空；旧任务历史留在版本库中", production="保持暂停"), ensure_ascii=False, indent=2))
    if args.apply:
        apply_plan(root, changes)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, sqlite3.Error) as error:
        sys.exit(str(error))
