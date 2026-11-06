"""只读检查安装结构和回执，不执行生命周期 Hook。"""

from pathlib import Path
import sqlite3

from workflow_installer import INSTALL_PATH, digest, read_json, read_tasks
from workflow_templates import BLOCK_END, BLOCK_START


def doctor(root):
    root = root.resolve()
    report = dict(root=str(root), errors=[], warnings=[], task_count=0, receipt_count=0)
    required = ["AGENTS.md", "scripts/context/task_store.py", "scripts/context/context_hook.py",
                "docs/context/project.json", "docs/context/00_current/index.md",
                "docs/runbooks/context_workflow.md", ".codex/hooks.json", ".context_runtime/tasks.sqlite3"]
    for relative in required:
        if not (root / relative).is_file():
            report["errors"].append("缺少：" + relative)
    try:
        project = read_json(root / "docs/context/project.json", {})
        if not project.get("manager_thread_id"):
            report["errors"].append("未登记主对话")
        if project.get("context_root") and Path(project["context_root"]).resolve() != root:
            report["errors"].append("context_root 指向其他位置；移动项目后先迁移路径")
        record = read_json(root / INSTALL_PATH, {})
        report["version"] = record.get("version", "legacy_unmanaged")
        if not record:
            report["warnings"].append("旧项目无安装清单，升级前需要审查迁移")
        for relative, expected in record.get("managed_files", {}).items():
            path = root / relative
            if not path.is_file() or digest(path.read_bytes()) != expected:
                report["errors"].append("受管程序变化：" + relative)
        if record:
            agents = (root / "AGENTS.md").read_text(encoding="utf-8-sig")
            if agents.count(BLOCK_START) != 1 or agents.count(BLOCK_END) != 1:
                report["errors"].append("AGENTS 受管区块缺失或重复")
            else:
                block = agents[agents.index(BLOCK_START):agents.index(BLOCK_END) + len(BLOCK_END)] + "\n"
                if digest(block.encode()) != record.get("agent_block_hash"):
                    report["errors"].append("AGENTS 受管区块被修改")
            if not Path(record["python_path"]).is_file():
                report["errors"].append("已配置 Python 不存在")
        hooks = read_json(root / ".codex/hooks.json", {}).get("hooks", {})
        for event in ("SessionStart", "UserPromptSubmit", "Stop"):
            if not hooks.get(event):
                report["errors"].append("缺少 Hook：" + event)
        for event, group in record.get("owned_hooks", {}).items():
            if group not in hooks.get(event, []):
                report["errors"].append("受管 Hook 变化：" + event)
        if (root / ".context_runtime/tasks.sqlite3").exists():
            tasks = read_tasks(root)
            report["task_count"] = len(tasks)
            report["active_tasks"] = [dict(id=t["id"], owner=t["owner"]) for t in tasks if t["status"] == "active"]
        for path in (root / ".context_runtime/hook_receipts").glob("*.json"):
            receipt = read_json(path, {})
            if receipt.get("session_id") == "manual-validation-only":
                continue
            report["receipt_count"] += 1
        report["warnings"].append("Hook 信任与各生命周期真实触发需要单独验证；工具代发消息应显式 status")
        facts = read_json(root / "docs/context/facts.json", {})
        items = facts.get("facts", []) if isinstance(facts, dict) else facts
        report["unverified_facts"] = sum(not item.get("last_verified_at") for item in items if isinstance(item, dict))
    except (ValueError, KeyError, OSError, sqlite3.Error) as error:
        report["errors"].append(str(error))
    return report
