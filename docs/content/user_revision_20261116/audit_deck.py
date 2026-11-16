from pathlib import Path
import json,hashlib,re
from pptx import Presentation
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[3]
project=root/'slides/projects/user_revision_ppt169_20261116'
deck=project/'exports/AI分享_28页顺序与幻觉修订版_20261116.pptx'
p=Presentation(deck)
notes=json.loads((Path(__file__).parent/'speaker_notes_per_page.json').read_text(encoding='utf-8'))
def flat(shapes):
    for shape in shapes:
        if shape.shape_type==6: yield from flat(shape.shapes)
        else: yield shape
pages=[]
for i,slide in enumerate(p.slides,1):
    shapes=list(flat(slide.shapes)); text=[]; sizes=set()
    for shape in shapes:
        if not shape.has_text_frame: continue
        text.append(shape.text)
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if run.font.size: sizes.add(run.font.size.pt)
    actual=slide.notes_slide.notes_text_frame.text.strip()
    expected=notes[f'{i:02d}'].strip()
    pages.append({'page':i,'native_text_shapes':len(text),'pictures':sum(x.shape_type==13 for x in shapes),'font_sizes_pt':sorted(sizes),'notes_match':actual.replace('\r','')==expected.replace('\r',''),'placeholder':any('待补：' in x for x in text)})
unchanged={}
for old,new in [(3,3),(29,28)]:
    a=Image.open(root/f'slides/projects/user_edition_ppt169_20261116/preview/user_edition_{old:02d}.png').convert('RGB')
    b=Image.open(project/f'preview/revised_{new:02d}.png').convert('RGB')
    unchanged[f'old_{old}_new_{new}']=ImageChops.difference(a,b).getbbox() is None
result={'slide_count':len(p.slides),'notes_all_match':all(x['notes_match'] for x in pages),'pages_with_images':sum(x['pictures']>0 for x in pages),'placeholder_pages':[x['page'] for x in pages if x['placeholder']],'protected_pages_pixel_identical':unchanged,'sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),'pages':pages}
(Path(__file__).parent/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='pages'},ensure_ascii=False))
assert len(p.slides)==28 and result['notes_all_match']
assert result['placeholder_pages']==[8,23,24]
