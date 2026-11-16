from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3]
src=root/'slides/projects/user_revision_ppt169_20261116/preview'
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
for start in range(1,29,4):
    out=Image.new('RGB',(1320,800),'#d7d7d7')
    d=ImageDraw.Draw(out)
    for i,n in enumerate(range(start,min(start+4,29))):
        im=Image.open(src/f'revised_{n:02d}.png').convert('RGB'); im.thumbnail((640,360))
        x=10+(i%2)*660;y=34+(i//2)*395
        out.paste(im,(x,y));d.text((x,y-29),f'P{n:02d}',font=font,fill='black')
    out.save(src/f'contact_{start:02d}.jpg',quality=94)
print('7 contact sheets')
