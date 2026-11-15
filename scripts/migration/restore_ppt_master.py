"""校验并恢复本项目实际使用的PPT Master源码；默认只预览，不安装依赖。"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import zipfile


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def restore(root, apply=False):
    root = root.resolve()
    package_dir = root / "tools/vendor_packages"
    manifest = json.loads((package_dir / "ppt_master_6_9_0.json").read_text(encoding="utf-8"))
    archive = package_dir / manifest["archive"]
    target = root / ".context_runtime/ppt_skill_candidates/ppt_master"
    if sha256(archive) != manifest["archive_sha256"]:
        raise ValueError("Master归档校验失败，停止恢复")
    expected = manifest["files"]
    with zipfile.ZipFile(archive) as bundle:
        if len(bundle.namelist()) != len(expected) or set(bundle.namelist()) != set(expected):
            raise ValueError("归档文件清单不匹配")
        for name, digest in expected.items():
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
                raise ValueError("归档含不安全路径")
            if hashlib.sha256(bundle.read(name)).hexdigest() != digest:
                raise ValueError(f"归档文件校验失败：{name}")
        if target.exists():
            mismatches = [name for name, digest in expected.items()
                          if not (target / name).is_file() or sha256(target / name) != digest]
            if mismatches:
                raise ValueError(f"已有Master目录与快照不同，不覆盖；差异文件数：{len(mismatches)}")
            return {"state": "already_matches", "path": str(target), "files": len(expected)}
        if not apply:
            return {"state": "preview", "path": str(target), "files": len(expected),
                    "next": "核对后加 --apply；恢复源码不代表已安装Python依赖"}
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="master_restore_", dir=target.parent) as staging:
            staged = Path(staging) / "payload"
            staged.mkdir()
            for name in expected:
                destination = staged / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(bundle.read(name))
            if target.exists():
                raise ValueError("恢复期间目标目录出现，不覆盖")
            shutil.move(str(staged), str(target))
    return {"state": "restored", "path": str(target), "files": len(expected)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        result = restore(args.root, args.apply)
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
