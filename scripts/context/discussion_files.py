"""讨论文件格式、来源引用与版本计算；文档是内容依据。"""

import hashlib
import json
import os
from pathlib import Path
import re
from uuid import uuid4

BASE_PATH = "docs/context/05_discussions"
KINDS = {"proposal": "候选方案", "question": "待解问题", "constraint": "约束",
         "observation": "观察或调研结果", "objection": "异议与限制", "user_confirmed": "用户已确认"}


def sha(content):
    return hashlib.sha256(content).hexdigest()


def check_topic(topic):
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", topic):
        raise ValueError("议题名称应为小写 snake_case，最多64字符")
    return topic


def checked_path(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("讨论路径越界或链接指向项目外")
    return path


def topic_paths(root, topic, session):
    check_topic(topic)
    base = f"{BASE_PATH}/topics/{topic}"
    owner = sha(session.encode())[:20]
    return dict(note_scope=f"{base}/notes/{owner}", summary_path=f"{base}/summary.md")


def atomic_document(path, metadata, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "---\n" + json.dumps(metadata, ensure_ascii=False, indent=2) + "\n---\n\n" + body.rstrip() + "\n"
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def load_document(path):
    content = path.read_text(encoding="utf-8-sig")
    if not content.startswith("---\n"):
        raise ValueError(f"讨论文件元数据缺失：{path.name}")
    header, separator, body = content[4:].partition("\n---\n")
    if not separator:
        raise ValueError(f"讨论文件分隔符缺失：{path.name}")
    return json.loads(header), body.strip()


def note_body(note):
    lines = [f"# {note['title']}", "", note["abstract"], "",
             f"- 来源对话：`{note['author_thread']}`", f"- 来源位置：{note['source_message']}", ""]
    for index, item in enumerate(note["items"]):
        lines += [f"## {index} · {KINDS[item['kind']]}", "", item["text"], ""]
        if item.get("evidence"):
            lines += ["依据或原话：" + item["evidence"], ""]
    return "\n".join(lines)


def read_topic(root, topic):
    check_topic(topic)
    directory = checked_path(root, f"{BASE_PATH}/topics/{topic}")
    notes = []
    digest = hashlib.sha256()
    for path in sorted((directory / "notes").glob("*/*.md")):
        checked_path(root, path.relative_to(root))
        note, _ = load_document(path)
        if note.get("topic") != topic or note.get("note_id") != path.stem:
            raise ValueError(f"记录身份与路径不一致：{path}")
        note["path"] = path.relative_to(root).as_posix()
        note["file_revision"] = sha(path.read_bytes())
        notes.append(note)
        digest.update(note["path"].encode())
        digest.update(path.read_bytes())
    summary_path = checked_path(root, f"{BASE_PATH}/topics/{topic}/summary.md")
    summary = load_document(summary_path)[0] if summary_path.exists() else None
    revision = digest.hexdigest()[:20]
    summary_revision = sha(summary_path.read_bytes())[:20] if summary else ""
    combined = sha((revision + summary_revision).encode())[:20]
    return dict(topic=topic, notes=notes, notes_revision=revision, summary=summary,
                summary_revision=summary_revision, revision=combined,
                summary_path=summary_path.relative_to(root).as_posix(),
                pending=bool(notes) and (not summary or summary.get("notes_revision") != revision))


def all_topics(root):
    directory = checked_path(root, f"{BASE_PATH}/topics")
    return [read_topic(root, path.name) for path in sorted(directory.glob("*")) if path.is_dir()]


def source_items(state):
    return {f"{note['note_id']}#{index}": item for note in state["notes"]
            for index, item in enumerate(note["items"])}


def summary_body(summary, notes):
    sources = {note["note_id"]: note["path"] for note in notes}
    summary_parent = Path(summary["path"]).parent
    lines = [f"# {summary['title']}", "", summary["abstract"], "",
             "此文件整理讨论，不代表方案获准实施。引用可追溯到独立记录。", ""]
    for kind, label in KINDS.items():
        points = [item for item in summary["points"] if item["kind"] == kind]
        if not points:
            continue
        lines += ["## " + label, ""]
        for item in points:
            links = []
            for ref in item["sources"]:
                relative = os.path.relpath(sources[ref.split("#")[0]], summary_parent).replace("\\", "/")
                links.append(f"[{ref}]({relative})")
            lines += ["- " + item["text"] + "（" + "；".join(links) + "）"]
        lines.append("")
    if summary.get("omitted"):
        lines += ["## 合并或暂不纳入的条目", ""]
        lines += [f"- {item['source']}：{item['reason']}" for item in summary["omitted"]]
    return "\n".join(lines)
