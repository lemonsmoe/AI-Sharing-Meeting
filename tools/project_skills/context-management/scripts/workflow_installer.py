"""预检、合并与有备份的安装；默认不写入。"""

import base64
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import sqlite3
import subprocess
import sys
from uuid import uuid4

from workflow_templates import BLOCK_END, BLOCK_START, VERSION, agent_block, initial_documents, json_text

SKILL_ROOT = Path(__file__).resolve().parents[1]
INSTALL_PATH = "docs/context/workflow_install.json"


def digest(content):
    return hashlib.sha256(content).hexdigest()


def read_json(path, default=None):
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default


def target_path(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"目标路径越界或链接指向项目外：{relative}")
    return path


def hook_groups(root, python_path):
    def command_for(filename):
        arguments = [str(python_path), (root / "scripts/context" / filename).as_posix()]
        if os.name == "nt":
            expression = "& " + " ".join("'" + item.replace("'", "''") + "'" for item in arguments)
            encoded = base64.b64encode(expression.encode("utf-16le")).decode("ascii")
            return "powershell.exe -NoProfile -NonInteractive -EncodedCommand " + encoded
        return shlex.join(arguments)
    result = {}
    for event in ("SessionStart", "UserPromptSubmit", "Stop"):
        handlers = []
        for filename in ("context_hook.py", "discussion_hook.py"):
            handler = dict(type="command", command=command_for(filename), timeout=10)
            if event != "Stop":
                handler["additionalContextLimit"] = 1800
            handlers.append(handler)
        group = {"hooks": handlers}
        if event == "SessionStart":
            group["matcher"] = "startup|resume|clear|compact|fork"
        result[event] = group
    return result


def merge_hooks(current, previous, desired):
    result = deepcopy(current or {"hooks": {}})
    hooks = result.setdefault("hooks", {})
    for event, group in desired.items():
        groups = hooks.setdefault(event, [])
        old = previous.get(event)
        if old:
            if old not in groups:
                raise ValueError(f"受管 Hook 已被修改或删除：{event}，请先审查迁移")
            groups[groups.index(old)] = group
        elif group not in groups:
            if any("context_hook.py" in str(item) for item in groups):
                raise ValueError(f"已有未登记上下文 Hook：{event}，不能自动接管或重复添加")
            groups.append(group)
    return result


def merge_agents(current, previous_hash):
    desired = agent_block()
    if BLOCK_START not in current and BLOCK_END not in current:
        if previous_hash:
            raise ValueError("受管 AGENTS 区块已被删除，请先审查")
        return current.rstrip() + ("\n\n" if current.strip() else "") + desired
    if current.count(BLOCK_START) != 1 or current.count(BLOCK_END) != 1:
        raise ValueError("AGENTS 受管区块标记不完整或重复")
    start = current.index(BLOCK_START)
    end = current.index(BLOCK_END) + len(BLOCK_END)
    block = current[start:end] + "\n"
    if previous_hash and digest(block.encode()) != previous_hash:
        raise ValueError("AGENTS 受管区块已被手工修改，请先审查")
    if not previous_hash and block != desired:
        raise ValueError("无法接管未登记的 AGENTS 受管区块")
    return current[:start] + desired.rstrip("\n") + current[end:]


def read_tasks(root):
    path = root / ".context_runtime/tasks.sqlite3"
    if not path.exists():
        return []
    connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    try:
        return [json.loads(row[0]) for row in connection.execute("SELECT data FROM tasks")]
    finally:
        connection.close()


def overlapping(first, second):
    first = Path(os.path.normcase(str(Path(first).resolve())))
    second = Path(os.path.normcase(str(Path(second).resolve())))
    return first.is_relative_to(second) or second.is_relative_to(first)


def build_plan(root, project_name=None, project_id=None, manager=None, python_path=None):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("项目根目录必须已存在且为目录")
    previous = read_json(target_path(root, INSTALL_PATH), {})
    project = read_json(target_path(root, "docs/context/project.json"), {})
    if project and manager and manager != project["manager_thread_id"]:
        raise ValueError("不能通过初始化更换主对话；需要用户指定并单独迁移")
    manager = project.get("manager_thread_id") or manager
    if not manager:
        raise ValueError("首次初始化必须明确 --manager-thread-id，不自动把当前对话设为主对话")
    python_path = Path(python_path or previous.get("python_path") or sys.executable).resolve()
    if not python_path.is_file():
        raise ValueError("指定 Python 不存在")
    validation = subprocess.run([str(python_path), "-c", "import sys; sys.exit(sys.version_info < (3, 11))"],
                                capture_output=True, timeout=10)
    if validation.returncode:
        raise ValueError("需要可用的 Python 3.11+")
    name = project.get("project_name") or project_name or root.name
    project_id = project.get("project_id") or project_id or digest(root.as_posix().encode())[:12]
    desired = {}
    managed = {}
    for path in sorted((SKILL_ROOT / "assets/runtime").glob("*.py")):
        relative = "scripts/context/" + path.name
        desired[relative] = path.read_bytes()
        managed[relative] = digest(desired[relative])
        target = target_path(root, relative)
        if target.exists() and target.read_bytes() != desired[relative]:
            if previous.get("managed_files", {}).get(relative) != digest(target.read_bytes()):
                raise ValueError(f"程序已有独立修改或未登记：{relative}")
    for relative, content in initial_documents(root, name, project_id, manager).items():
        if not target_path(root, relative).exists():
            desired[relative] = content.encode("utf-8")
    agents = target_path(root, "AGENTS.md")
    current = agents.read_text(encoding="utf-8-sig") if agents.exists() else ""
    desired["AGENTS.md"] = merge_agents(current, previous.get("agent_block_hash")).encode("utf-8")
    hook_path = target_path(root, ".codex/hooks.json")
    groups = hook_groups(root, python_path)
    hooks = merge_hooks(read_json(hook_path, {}), previous.get("owned_hooks", {}), groups)
    desired[".codex/hooks.json"] = json_text(hooks).encode("utf-8")
    ignore_path = target_path(root, ".gitignore")
    ignore = ignore_path.read_text(encoding="utf-8-sig") if ignore_path.exists() else ""
    for line in (".context_runtime/", "__pycache__/", "*.pyc"):
        if line not in ignore.splitlines():
            ignore = ignore.rstrip() + ("\n" if ignore else "") + line + "\n"
    desired[".gitignore"] = ignore.encode("utf-8")
    record = dict(version=VERSION, context_root=root.as_posix(), python_path=str(python_path),
                  managed_files=managed, agent_block_hash=digest(agent_block().encode()), owned_hooks=groups)
    desired[INSTALL_PATH] = json_text(record).encode("utf-8")
    changes = {path: data for path, data in desired.items()
               if not target_path(root, path).exists() or target_path(root, path).read_bytes() != data}
    session = os.environ.get("CODEX_THREAD_ID")
    for task in read_tasks(root):
        if task["status"] == "active" and task["owner"] != session:
            if any(overlapping(root / path, scope) for path in changes for scope in task["write_paths"]):
                raise ValueError(f"安装范围与任务冲突：{task['id']}，责任 {task['owner']}")
    expected = {path: digest(target_path(root, path).read_bytes()) if target_path(root, path).exists() else None
                for path in changes}
    return dict(root=root, changes=changes, expected=expected, existing_project=bool(project), manager=manager,
                python_path=python_path, hooks_changed=".codex/hooks.json" in changes,
                hook_script_changed="scripts/context/context_hook.py" in changes)


def apply_plan(plan):
    root = plan["root"]
    if plan["existing_project"] and plan["changes"]:
        if os.environ.get("CODEX_THREAD_ID") != plan["manager"]:
            raise ValueError("已有项目升级须由已登记主对话执行；不接受伪造身份")
    for relative, expected in plan["expected"].items():
        path = target_path(root, relative)
        actual = digest(path.read_bytes()) if path.exists() else None
        if actual != expected:
            raise ValueError(f"预览后文件已变化，请重新预览：{relative}")
    for task in read_tasks(root):
        if task["status"] == "active" and task["owner"] != os.environ.get("CODEX_THREAD_ID"):
            if any(overlapping(root / path, scope) for path in plan["changes"] for scope in task["write_paths"]):
                raise ValueError(f"执行前出现任务冲突：{task['id']}")
    batch = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_") + uuid4().hex[:8]
    backup = target_path(root, ".context_runtime/setup_backups/" + batch)
    for relative in plan["changes"]:
        target = target_path(root, relative)
        if target.exists():
            original = backup / relative
            original.parent.mkdir(parents=True, exist_ok=True)
            original.write_bytes(target.read_bytes())
    # 清单最后落盘；单文件原子替换，跨文件失败时保留原件供恢复。
    for relative, data in plan["changes"].items():
        target = target_path(root, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name(target.name + "." + uuid4().hex + ".tmp")
        temp.write_bytes(data)
        os.replace(temp, target)
    for relative in ("docs/context/01_decisions/records", "docs/context/02_events", "docs/context/03_handoffs"):
        target_path(root, relative).mkdir(parents=True, exist_ok=True)
    target_path(root, ".context_runtime/tasks.sqlite3")
    result = subprocess.run([str(plan["python_path"]), str(root / "scripts/context/task_store.py"),
                             "status", "--root", str(root)], capture_output=True, text=True, encoding="utf-8", timeout=20)
    if result.returncode:
        raise ValueError("文件已写入但数据库初始化失败，请保留备份并检查：" + result.stderr)
    return backup.as_posix() if backup.exists() else None
