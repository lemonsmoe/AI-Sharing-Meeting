"""生成原创字幕教学样片，所有画面由时间驱动。"""
import json
import time
import argparse
import hashlib
import platform
from importlib.metadata import version
from datetime import datetime, timezone
from pathlib import Path
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--run_id', default=datetime.now().strftime('run_%Y%m%d_%H%M%S'))
args = parser.parse_args()
if not args.run_id.replace('_', '').isalnum():
    raise ValueError('run_id只能包含字母、数字和下划线')
output = root / 'videos/experiments' / args.run_id
output.mkdir(parents=True, exist_ok=False)
scenes = [
    ('一句话，真的够吗？', '请帮我整理一份会议纪要。', '任务太宽，输出就难以验收。'),
    ('先给材料，再给任务', '输入：一段模拟会议记录', '把事实、建议和未决问题分开。'),
    ('让结果有固定结构', '事项 → 负责人 → 截止日 → 原文依据', '没有提及的信息，明确写“待确认”。'),
    ('示例：别替同事做承诺', '原文：小林说，争取周五给初稿。', '应写：周五为预计时间，尚待确认。'),
    ('核查，而不是只看流畅', '逐项回到原文，检查姓名、数字与日期。', '语句自然，并不代表内容正确。'),
    ('把好流程留下来', '材料 → 结构 → 初稿 → 核查 → 交付', '保存提示词和检查表，下次复用。'),
]
font_path = 'C:/Windows/Fonts/msyh.ttc'
fonts = {size: ImageFont.truetype(font_path, size) for size in (24, 32, 42, 58)}

def render_frame(seconds):
    index = min(int(seconds // 12), 5)
    local_time = seconds % 12
    image = Image.new('RGB', (1280, 720), '#101d30')
    draw = ImageDraw.Draw(image)
    draw.text((70, 45), 'AI WORKFLOW  /  工作方法实验', font=fonts[24], fill='#7ce0cc')
    draw.text((70, 135), scenes[index][0], font=fonts[58], fill='white')
    for step in range(6):
        x = 80 + step * 195
        color = '#7ce0cc' if step <= index else '#30435b'
        draw.rounded_rectangle((x, 275, x + 150, 350), radius=16, fill=color)
        draw.text((x + 55, 289), str(step + 1).zfill(2), font=fonts[32], fill='#101d30')
    if local_time >= 1:
        draw.text((70, 415), scenes[index][1], font=fonts[42], fill='#ffffff')
    if local_time >= 5:
        draw.text((70, 505), scenes[index][2], font=fonts[32], fill='#c0d0e6')
    draw.text((70, 625), '模拟材料 · 原创字幕版 · 无配音', font=fonts[24], fill='#91a5bd')
    draw.rectangle((0, 708, int(1280 * seconds / 72), 719), fill='#7ce0cc')
    return np.asarray(image)

start = time.perf_counter()
started_at = datetime.now(timezone.utc).isoformat()
video_path = output / 'workflow_sample.mp4'
with imageio.get_writer(video_path, fps=12, codec='libx264', quality=7, macro_block_size=1) as writer:
    for frame in range(864):
        writer.append_data(render_frame(frame / 12))
elapsed = time.perf_counter() - start
for index in range(6):
    Image.fromarray(render_frame(index * 12 + 7)).save(output / f'scene_{index + 1:02}.png')
reader = imageio.get_reader(video_path)
metadata = reader.get_meta_data()
metadata.pop('nframes', None)
decoded = sum(1 for _ in reader)
reader.close()
report = {'duration_seconds': 72, 'frames_decoded': decoded, 'render_seconds': elapsed,
          'started_at': started_at, 'ended_at': datetime.now(timezone.utc).isoformat(),
          'python': platform.python_version(), 'imageio': version('imageio'),
          'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'video_sha256': hashlib.sha256(video_path.read_bytes()).hexdigest(),
          'bytes': video_path.stat().st_size, 'metadata': metadata,
          'paid_external_calls': 0, 'voice': False, 'agent_cost': '未取得账单，不能视为零'}
(output / 'render_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
(output / 'storyboard.json').write_text(json.dumps([{'start': i*12, 'end': (i+1)*12, 'title': s[0], 'subtitle_1': s[1], 'subtitle_2': s[2]} for i,s in enumerate(scenes)], ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
