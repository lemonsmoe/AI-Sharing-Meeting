"""核对最终字节、备注、日期编码及压缩包中的实际交付物。"""
import hashlib
import json
import re
import xml.etree.ElementTree as element_tree
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[3]
bundle = root / 'outputs/leadership_review_v3'
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      's': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


deck = bundle / 'leadership_review_v3.pptx'
receipt = json.loads((root / 'slides/review_v3/build/validation.json').read_text(encoding='utf-8'))
assert digest(deck) == receipt['finalSha256']
with zipfile.ZipFile(deck) as archive:
    slides = [name for name in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', name)]
    notes = [name for name in archive.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', name)]
    assert len(slides) == len(notes) == 30
    table_count = sum(len(element_tree.fromstring(archive.read(name)).findall('.//a:tbl', ns)) for name in slides)
    assert table_count == 5
    for name in notes:
        text = ''.join(element_tree.fromstring(archive.read(name)).itertext())
        assert len(text) > 100, name
    media_notes = ''.join(element_tree.fromstring(archive.read('ppt/notesSlides/notesSlide27.xml')).itertext())
    assert 'meeting_captioned.mp4' in media_notes and '无声字幕版' not in media_notes

workbook = bundle / 'materials/meeting_actions.xlsx'
with zipfile.ZipFile(workbook) as archive:
    cells = {cell.attrib['r']: cell for cell in element_tree.fromstring(archive.read('xl/worksheets/sheet1.xml')).findall('.//s:c', ns)}
    for address, expected in {'D6': 46335.75, 'D12': 46338, 'D13': 8000}.items():
        assert cells[address].get('t') in {None, 'n'}
        assert float(cells[address].find('s:v', ns).text) == expected
    for address in ['C7', 'D7']:
        assert address not in cells or cells[address].find('s:v', ns) is None

manifest = json.loads((bundle / 'package_manifest.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(bundle / 'leadership_review_v3_bundle.zip') as archive:
    for item in manifest:
        assert digest(bundle / item['path']) == item['sha256'], item['path']
        assert hashlib.sha256(archive.read('leadership_review_v3/' + item['path'])).hexdigest() == item['sha256'], item['path']
script = (bundle / 'materials/rehearsal_script_v3.md').read_text(encoding='utf-8')
headings = re.findall(r'^## \d{2}｜[^\n]+', script, re.M)
minutes = [float(re.search(r'｜([\d.]+)分钟', line).group(1)) for line in headings]
result = {'slides': len(slides), 'notes': len(notes), 'native_tables': table_count, 'native_charts': 0,
          'script_sections': len(headings), 'planned_content_minutes': sum(minutes),
          'actual_rehearsal': '未计时', 'checked_package_files': len(manifest),
          'ppt_sha256': digest(deck), 'xlsx_sha256': digest(workbook),
          'video_sha256': digest(bundle / 'media/meeting_captioned.mp4'),
          'zip_sha256': digest(bundle / 'leadership_review_v3_bundle.zip'),
          'scope': '文件、结构、日期与随包字节检查；原生应用及逐页目检见独立记录，未完整试听视频'}
(root / 'research/integration/v3/final_check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
