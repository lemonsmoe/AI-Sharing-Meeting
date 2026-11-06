"""初始化或检查项目协作上下文；init 默认仅预览。"""

import argparse
import json
from pathlib import Path
import sys

from workflow_doctor import doctor
from workflow_installer import apply_plan, build_plan
from workflow_templates import VERSION


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["init", "doctor"])
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--project-id")
    parser.add_argument("--manager-thread-id")
    parser.add_argument("--python", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.action == "doctor":
        if args.apply:
            parser.error("doctor 是只读操作，不接受 --apply")
        report = doctor(args.root)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return bool(report["errors"])
    plan = build_plan(args.root, args.project_name, args.project_id, args.manager_thread_id, args.python)
    report = dict(mode="apply" if args.apply else "preview", version=VERSION, root=str(plan["root"]),
                  changed_files=list(plan["changes"]),
                  hook_program=str(plan["root"] / "scripts/context/context_hook.py"),
                  python_path=str(plan["python_path"]),
                  hook_review_required=plan["hooks_changed"] or plan["hook_script_changed"])
    if args.apply:
        report["backup"] = apply_plan(plan)
        report["note"] = "配置已写入；Hook 信任与真实触发请单独验证。"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
