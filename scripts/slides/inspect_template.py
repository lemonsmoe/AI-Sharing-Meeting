import hashlib,json,shutil,zipfile,collections
from pathlib import Path
from xml.etree import ElementTree as E
root=Path.cwd(); src=root/'slides/赛感PPT优化丰富版本.pptx'; dst=root/'slides/templates/sycsense_reference.pptx'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=h(src)
if not dst.exists(): shutil.copy2(src,dst)
assert h(dst)==before==h(src)
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with zipfile.ZipFile(src) as z:
    names=z.namelist(); slides=sorted([n for n in names if __import__('re').fullmatch(r'ppt/slides/slide\d+.xml',n)],key=lambda n:int(__import__('re').search(r'(\d+)\.xml',n).group(1)))
    fonts=collections.Counter(); entries=[]
    for name in slides:
        tree=E.fromstring(z.read(name))
        texts=[e.text for e in tree.findall('.//a:t',ns) if e.text]
        for e in tree.iter():
            if 'typeface' in e.attrib: fonts[e.attrib['typeface']]+=1
        entries.append({'part':name,'texts':texts,'pictures':len(tree.findall('.//p:pic',ns)),'tables':len(tree.findall('.//a:tbl',ns))})
    size=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns).attrib
    result={'source':str(src),'copy':str(dst),'sha256':before,'verified_date':'2026-11-06','size_emu':size,'slide_count':len(slides),'explicit_fonts':dict(fonts),'media':[n for n in names if n.startswith('ppt/media/')],'slides':entries,'verification_limit':'XML结构检查，尚未渲染或验证Office/WPS显示'}
(root/'slides/templates/template_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='slides'},ensure_ascii=False))
