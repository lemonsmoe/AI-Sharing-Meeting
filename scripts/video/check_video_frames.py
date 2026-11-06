"""从实际编码视频提取逐秒检查图，不替代动态播放。"""
import json
from pathlib import Path
import imageio.v2 as imageio
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
source = root / 'videos/experiments/explainer_v2_reviewed/meeting_explainer.mp4'
output = source.parent / 'qa'
output.mkdir(exist_ok=True)
reader = imageio.get_reader(source)
fps = reader.get_meta_data()['fps']
samples = []
for second in range(72):
    frame = Image.fromarray(reader.get_data(round(second*fps)))
    samples.append(frame)
reader.close()
for batch in range(4):
    sheet = Image.new('RGB', (960, 1080), 'white')
    for index, frame in enumerate(samples[batch*18:(batch+1)*18]):
        thumb = frame.resize((320, 180))
        ImageDraw.Draw(thumb).text((3, 3), str(batch*18+index)+'s', fill='red')
        sheet.paste(thumb, ((index%3)*320, (index//3)*180))
    sheet.save(output / f'seconds_{batch*18:02}_{batch*18+17:02}.png')
(output/'sampling.json').write_text(json.dumps({'source':str(source), 'fps':fps,
    'seconds':list(range(72)), 'scope':'实际MP4逐秒取样，非完整播放'}, ensure_ascii=False,indent=2),encoding='utf-8')
print('72 decoded samples; 4 sheets')
