"""导出项目任务历史；不复制本机数据库、阅读游标或 Hook 回执。"""

import argparse
from contextlib import closing
import json
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
import sqlite3


def export_context(root):
    root = root.resolve()
    database = root / ".context_runtime/tasks.sqlite3"
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        tasks = [json.loads(row[0]) for row in connection.execute("SELECT data FROM tasks ORDER BY id")]
        history = [dict(row) for row in connection.execute("SELECT * FROM history ORDER BY id")]
    for task in tasks:
        portable = []
        for value in task["write_paths"]:
            if PureWindowsPath(value).drive:
                relative = PureWindowsPath(value).relative_to(PureWindowsPath(str(root)))
            else:
                relative = Path(value).relative_to(root)
            portable.append(relative.as_posix())
        task["source_write_paths"] = task["write_paths"]
        task["write_paths"] = portable
    return dict(
        schema_version=1,
        exported_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        source_root=root.as_posix(),
        source_project=json.loads((root / "docs/context/project.json").read_text(encoding="utf-8-sig")),
        usage="仅作历史档案；不把旧 owner、active、目标模式或阅读游标恢复为新环境的运行权限。",
        tasks=tasks,
        history=history,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=Path("docs/context/migration/task_history.json"))
    args = parser.parse_args()
    payload = export_context(args.root)
    target = (args.root / args.output).resolve()
    if not target.is_relative_to((args.root / "docs/context/migration").resolve()):
        parser.error("历史导出只允许写入 docs/context/migration")
    if target.exists():
        previous = json.loads(target.read_text(encoding="utf-8"))
        if Path(previous["source_root"]).resolve() != args.root.resolve():
            parser.error("不能覆盖其他环境的历史，请用 --output 指定本环境独立档案文件")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(path=target.as_posix(), tasks=len(payload["tasks"]),
                          history=len(payload["history"])), ensure_ascii=False))


if __name__ == "__main__":
    main()
