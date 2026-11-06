"""预览或更新新克隆的旧媒体脚本依赖路径，不执行内容生产。"""

import argparse
import json
from pathlib import Path
import sys


OLD_NODE = "C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"
OLD_SKILL = "C:/Users/22796/.codex/plugins/cache/openai-primary-runtime/presentations/26.1030.10813/skills/presentations"
OLD_PYTHON = "C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe"


def configured_sources(root, node_modules, presentation_skill, python_path):
    artifact = node_modules / "@oai/artifact-tool/dist/artifact_tool.mjs"
    playwright = node_modules / "playwright/index.mjs"
    utility = presentation_skill / "container_tools/artifact_tool_utils.mjs"
    for path in (artifact, playwright, utility, python_path):
        if not path.is_file():
            raise ValueError(f"依赖不存在：{path}")
    replacements = {
        "file:///" + OLD_NODE + "/@oai/artifact-tool/dist/artifact_tool.mjs": artifact.as_uri(),
        "file:///" + OLD_NODE + "/playwright/index.mjs": playwright.as_uri(),
        "file:///" + OLD_SKILL + "/container_tools/artifact_tool_utils.mjs": utility.as_uri(),
    }
    changes = {}
    scopes = ("scripts/slides", "research/office/office_trial_01", "tutorials/office/spreadsheet_demo")
    for scope in scopes:
        for path in (root / scope).rglob("*.mjs"):
            if "node_modules" in path.parts:
                continue
            if not path.resolve().is_relative_to(root):
                raise ValueError("源文件指向克隆外部")
            text = path.read_text(encoding="utf-8-sig")
            updated = text
            for old, new in replacements.items():
                updated = updated.replace(old, new)
            for old, new in ((OLD_NODE, node_modules.as_posix()),
                             (OLD_SKILL, presentation_skill.as_posix()),
                             (OLD_PYTHON, python_path.as_posix()),
                             ("@oai/artifact-tool", artifact.as_uri())):
                for quote in ("'", '"'):
                    updated = updated.replace(quote + old + quote, json.dumps(new))
            if updated != text:
                changes[path.relative_to(root).as_posix()] = updated
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--node-modules", required=True, type=Path)
    parser.add_argument("--presentation-skill", required=True, type=Path)
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    changes = configured_sources(root, args.node_modules.resolve(), args.presentation_skill.resolve(), args.python.resolve())
    print(json.dumps(dict(mode="apply" if args.apply else "preview", files=list(changes),
                          note="只重绑依赖；不安装依赖、不渲染、不证明新版本 API 兼容"), ensure_ascii=False, indent=2))
    if args.apply:
        snapshot = json.loads((root / "docs/context/migration/task_history.json").read_text(encoding="utf-8"))
        if Path(snapshot["source_root"]).resolve() == root:
            raise ValueError("不能用迁移脚本修改源环境，请在新克隆中运行")
        for relative, text in changes.items():
            path = root / relative
            backup = root / ".context_runtime/media_path_backups" / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_bytes(path.read_bytes())
            path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        sys.exit(str(error))
