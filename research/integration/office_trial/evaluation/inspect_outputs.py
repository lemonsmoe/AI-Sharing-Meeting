"""只读提取两次实际文件，供主对话逐项复核；不自动裁定语义。"""

from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as et
from zipfile import ZipFile


root = Path(__file__).resolve().parents[4]
evaluation = Path(__file__).resolve().parent
ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_workbook(path):
    with ZipFile(path) as package:
        strings = []
        if "xl/sharedStrings.xml" in package.namelist():
            strings = ["".join(item.itertext()) for item in et.fromstring(package.read("xl/sharedStrings.xml"))]
        workbook = et.fromstring(package.read("xl/workbook.xml"))
        relationships = et.fromstring(package.read("xl/_rels/workbook.xml.rels"))
        targets = {item.attrib["Id"]: item.attrib["Target"] for item in relationships}
        result = {"zip_error": package.testzip(), "sheets": {}}
        for sheet in workbook.find("s:sheets", ns):
            relation = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            target = targets[relation]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            data = et.fromstring(package.read(target))
            cells = {}
            for cell in data.findall(".//s:sheetData/s:row/s:c", ns):
                value_node = cell.find("s:v", ns)
                value = value_node.text if value_node is not None else None
                kind = cell.attrib.get("t", "n")
                if kind == "s" and value is not None:
                    value = strings[int(value)]
                if kind == "inlineStr":
                    value = "".join(cell.find("s:is", ns).itertext())
                if value is not None:
                    cells[cell.attrib["r"]] = {"type": kind, "value": value, "style": cell.attrib.get("s")}
                    if kind == "n" and 46000 < float(value) < 47000:
                        cells[cell.attrib["r"]]["excel_date"] = (datetime(1899, 12, 30) + timedelta(days=float(value))).isoformat(timespec="minutes")
            result["sheets"][sheet.attrib["name"]] = cells
        return result


frozen = json.loads((evaluation / "pre_dispatch_hashes.json").read_text(encoding="utf-8-sig"))
baseline = json.loads((evaluation / "reference_baseline_hash.json").read_text(encoding="utf-8-sig"))
frozen.append({"path": baseline["Path"], "sha256": baseline["Hash"]})
report = {"input_freeze": [{"path": row["path"], "unchanged": sha256(Path(row["path"])) == row["sha256"].lower()} for row in frozen], "runs": {}}
for name, relative in [("run_01", "research/office/office_trial_01"), ("run_02", "research/methodology/office_trial_02")]:
    outputs = {}
    for version in ("first_output", "final_output"):
        folder = root / relative / version
        outputs[version] = {
            "hashes": {file.name: sha256(file) for file in folder.iterdir() if file.suffix in (".md", ".xlsx")},
            "workbook": inspect_workbook(folder / "meeting_follow_up.xlsx"),
        }
    outputs["cell_values_unchanged"] = all(
        {key: (cell["type"], cell["value"]) for key, cell in cells.items()}
        == {key: (cell["type"], cell["value"]) for key, cell in outputs["final_output"]["workbook"]["sheets"][sheet].items()}
        for sheet, cells in outputs["first_output"]["workbook"]["sheets"].items()
    )
    report["runs"][name] = outputs
(evaluation / "file_inspection.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"frozen_unchanged": all(item["unchanged"] for item in report["input_freeze"]), "runs": {name: {"hashes": run["final_output"]["hashes"], "cell_values_unchanged": run["cell_values_unchanged"]} for name, run in report["runs"].items()}}, ensure_ascii=False))
