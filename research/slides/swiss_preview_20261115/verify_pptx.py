import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from PIL import Image

project = Path(sys.argv[1])
deck = Path(sys.argv[2])
copy = Path(sys.argv[3])
namespace = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
quote = "My next mission is to build an agent that even my mum can use."


def node(package, name):
    return etree.fromstring(package.read(name))


def slide_text(slide):
    return slide.xpath("//a:t/text()", namespaces=namespace)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preview_row(index):
    path = project / "preview" / f"slide_{index:02}.png"
    with Image.open(path) as png:
        assert png.size == (1280, 720)
        png.verify()
    return {"filename": path.name, "sha256": sha256(path)}


report = {"file": deck.name, "sha256": sha256(deck), "slides": []}
with ZipFile(deck) as package:
    assert package.testzip() is None
    presentation = node(package, "ppt/presentation.xml")
    assert len(presentation.xpath("//p:sldId", namespaces=namespace)) == 3
    assert report["sha256"] != sha256(copy)

    for theme_part in ("ppt/theme/theme1.xml", "ppt/theme/theme2.xml"):
        theme = node(package, theme_part)
        for role in ("majorFont", "minorFont"):
            font_role = theme.xpath(f"//a:{role}", namespaces=namespace)[0]
            faces = font_role.xpath(
                './a:latin/@typeface|./a:ea/@typeface|./a:font[@script="Hans"]/@typeface',
                namespaces=namespace,
            )
            assert faces == ["Microsoft YaHei"] * 3

    for index in range(1, 4):
        slide = node(package, f"ppt/slides/slide{index}.xml")
        note = node(package, f"ppt/notesSlides/notesSlide{index}.xml")
        note_body = note.xpath(
            '//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]/p:txBody//a:t/text()',
            namespaces=namespace,
        )
        native_text_boxes = len(slide.xpath("//p:sp[p:txBody//a:t]", namespaces=namespace))
        pictures = len(slide.xpath("//p:pic", namespaces=namespace))
        sizes = Counter(int(s) / 100 for s in slide.xpath("//a:rPr/@sz", namespaces=namespace))
        assert sizes and sizes.keys() <= {18, 24, 43.5}
        assert native_text_boxes and note_body
        assert pictures == (1, 0, 1)[index - 1]
        assert set(slide.xpath("//a:rPr/a:ea/@typeface", namespaces=namespace)) == {"+mn-ea"}
        assert set(slide.xpath("//a:rPr/a:latin/@typeface", namespaces=namespace)) == {"+mn-lt"}
        assert all(s not in " ".join(slide_text(slide)) for s in ("企业AI效率分享", "企业 AI 效率分享"))
        if index == 3:
            assert quote in " ".join(slide_text(slide))
            note_text = " ".join(note_body)
            for expected in (quote, "2026-02-14", "中文为本项目自译", "steipete.me/posts/2026/openclaw"):
                assert expected in note_text, expected
        report["slides"].append({
            "slide": index,
            "native_text_boxes": native_text_boxes,
            "embedded_pictures": pictures,
            "run_sizes_pt": sorted(sizes),
            "notes_body": True,
            "preview": preview_row(index),
        })

    preview_two = project / "preview" / "slide_02.png"
    cover_capture = project / "images" / "prompt_slide.png"
    with Image.open(preview_two) as rendered, Image.open(cover_capture) as capture:
        assert rendered.convert("RGB").tobytes() == capture.convert("RGB").tobytes()
    capture_bytes = cover_capture.read_bytes()
    assert any(package.read(p) == capture_bytes for p in package.namelist() if p.startswith("ppt/media/"))

with ZipFile(copy) as edited:
    edited_slide = node(edited, "ppt/slides/slide2.xml")
    edited_boxes = edited_slide.xpath("//p:sp[p:txBody//a:t]", namespaces=namespace)
    assert any(
        "".join(box.xpath(".//a:t/text()", namespaces=namespace)) == "把 PPT 的需求说具体"
        for box in edited_boxes
    )
report["embedded_capture_matches_final_slide_2_pixels"] = True
report["powerpoint_title_saved_and_reopened"] = True
report["font"] = "Microsoft YaHei (Latin, East Asian and Hans script mapping)"
print(json.dumps(report, ensure_ascii=True, indent=2))
