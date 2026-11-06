"""用对象运动解释会议记录的结构化与核查。"""
import argparse
import hashlib
import json
import time
import math
from datetime import datetime, timezone
from pathlib import Path
from importlib.metadata import version
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[2]
fonts = {s: ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', s) for s in (22, 26, 32, 40, 50)}
navy, mint, gold, red = '#14243b', '#16836f', '#956309', '#ba353f'
segments = [
    (0, 10, '会议结束了，事情却还散着', '先保留原话，再整理任务。'),
    (10, 22, '从原句中，提取结构', '每个字段，都应该能找到原文依据。'),
    (22, 34, '看起来整齐，也可能改了意思', '模拟错误：把“争取”写成了“承诺”。'),
    (34, 46, '回到原文，修正承诺强度', '预计时间需要确认，不能替同事做承诺。'),
    (46, 60, '不知道的，就保留未知', '预算没有确定，就不能自动补一个数字。'),
    (60, 72, '可交付，也要可追踪', '让AI整理，让证据约束，让人确认。'),
]

def smooth(value):
    value = max(0, min(value, 1))
    return value * value * (3 - 2 * value)

def lerp(start, end, value):
    return start + (end - start) * smooth(value)

def card(draw, x, y, width, height, label, detail='', color=mint):
    draw.rounded_rectangle((x, y, x+width, y+height), 18, fill='white', outline='#d8e1e8', width=2)
    draw.rounded_rectangle((x, y, x+8, y+height), 4, fill=color)
    draw.text((x+24, y+18), label, font=fonts[26], fill=navy)
    if detail:
        draw.text((x+24, y+62), detail, font=fonts[32], fill=color)

def arrow(draw, start, end, progress=1, color=mint):
    x, y = start
    ex, ey = end
    ex, ey = lerp(x, ex, progress), lerp(y, ey, progress)
    draw.line((x, y, ex, ey), fill=color, width=5)
    angle = math.atan2(ey-y, ex-x)
    dx, dy = math.cos(angle), math.sin(angle)
    draw.polygon(((ex, ey), (ex-12*dx-7*dy, ey-12*dy+7*dx),
                  (ex-12*dx+7*dy, ey-12*dy-7*dx)), fill=color)

def frame_at(t):
    image = Image.new('RGB', (1280, 720), '#f1f5f8')
    draw = ImageDraw.Draw(image)
    scene = next((s for s in segments if s[0] <= t < s[1]), segments[-1])
    local = t-scene[0]
    draw.text((60, 32), '工作流实验室  /  模拟会议 · 字幕版', font=fonts[22], fill='#62788c')
    draw.text((60, 88), scene[2], font=fonts[50], fill=navy)
    if t < 10:
        items = [('小林', '我来整理方案初稿', mint), ('交付时间', '争取周五给到', gold), ('预算', '还没有确定', red)]
        for i, (label, detail, color) in enumerate(items):
            x = lerp(1300, 90+i*375, (local-i*1.3)/1.5)
            y = 240 + (i % 2)*70
            card(draw, x, y, 340, 160, label, detail, color)
        if local > 6:
            draw.text((260, 520), '谁负责？做什么？什么时候？哪些还不知道？', font=fonts[32], fill=navy)
    elif t < 22:
        card(draw, 65, 205, 1150, 110, '原始记录', '小林：我来整理方案初稿，争取周五给到。')
        labels = [('负责人', '小林'), ('事项', '方案初稿'), ('时间性质', '周五 · 预计')]
        for i, (label, detail) in enumerate(labels):
            progress = smooth((local-1-i*2)/2)
            x = 95+i*390
            y = lerp(320, 410, progress)
            if progress > 0:
                arrow(draw, (x+150, 320), (x+150, y-15), progress)
                card(draw, x, y, 320, 130, label, detail, gold if i == 2 else mint)
    elif t < 46:
        card(draw, 65, 215, 520, 190, '原文依据', '争取周五给到', gold)
        correcting = t >= 34
        progress = smooth((local-1)/2)
        arrow(draw, (600, 310), (680, 310), progress, mint if correcting else red)
        detail = '周五 · 预计，待确认' if correcting and local >= 3 else '周五 · 承诺完成'
        corrected = correcting and local >= 3
        label = '核查后的字段' if corrected else ('正在核查' if correcting else '模拟AI草稿')
        card(draw, 700, 215, 515, 190, label, detail, mint if corrected else red)
        if not correcting and local > 3:
            draw.line((726, 325, 1120, 325), fill=red, width=5)
            draw.text((700, 440), '“争取” ≠ “承诺”', font=fonts[40], fill=red)
        if correcting:
            draw.rounded_rectangle((86, 270, 350, 340), 10, outline=gold, width=4)
            if local > 4:
                draw.text((210, 470), '保留不确定性 → 交给负责人确认', font=fonts[40], fill=mint)
    elif t < 60:
        card(draw, 65, 225, 485, 180, '原文依据', '预算还没有确定', gold)
        arrow(draw, (570, 315), (685, 315), local/2)
        card(draw, 710, 225, 495, 180, '预算字段', '待确认', gold)
        checks = ['姓名有依据', '时间不夸大', '缺失值不补造']
        for i, label in enumerate(checks):
            if local > 3+i*2:
                x = 90+i*400
                draw.ellipse((x, 480, x+32, 512), fill=mint)
                draw.text((x+45, 477), label, font=fonts[26], fill=navy)
    else:
        rows = [('负责人', '小林', '原文第1句'), ('事项', '方案初稿', '原文第1句'), ('时间', '周五 · 预计待确认', '保留“争取”'), ('预算', '待确认', '原文未确定')]
        for i, row in enumerate(rows):
            if local >= i*.8:
                y = 195+i*70
                draw.rounded_rectangle((90, y, 1190, y+60), 10, fill='white')
                for x, text in zip((115, 330, 850), row):
                    draw.text((x, y+10), text, font=fonts[26], fill=navy)
        if local > 4:
            for i, label in enumerate(['材料', '结构', '初稿', '核查', '交付']):
                x = 105+i*235
                draw.rounded_rectangle((x, 515, x+160, 570), 12, fill=mint if i == 3 else navy)
                draw.text((x+45, 522), label, font=fonts[26], fill='white')
                if i < 4:
                    arrow(draw, (x+170, 542), (x+220, 542))
    draw.rounded_rectangle((40, 620, 1240, 690), 15, fill=navy)
    draw.text((70, 636), scene[3], font=fonts[32], fill='white')
    draw.rectangle((0, 712, int(t/72*1280), 719), fill=mint)
    return image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', required=True)
    args = parser.parse_args()
    if not args.run_id.replace('_', '').isalnum():
        raise ValueError('run_id只能包含字母、数字和下划线')
    output = root / 'videos/experiments' / args.run_id
    output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    started = datetime.now(timezone.utc).isoformat()
    path = output / 'meeting_explainer.mp4'
    with imageio.get_writer(path, fps=24, codec='libx264', quality=8, macro_block_size=1) as writer:
        for frame in range(1728):
            writer.append_data(np.asarray(frame_at(frame/24)))
    render_seconds = time.perf_counter()-start
    samples = [0, 2, 7, 10, 13, 19, 22, 26, 33, 34, 36, 39, 46, 50, 57, 60, 65, 71]
    sheet = Image.new('RGB', (960, 180*6), 'white')
    for index, second in enumerate(samples):
        image = frame_at(second)
        image.save(output / f'frame_{second:02}.png')
        thumb = image.resize((320, 180))
        ImageDraw.Draw(thumb).text((4, 4), f'{second}s', fill='red')
        sheet.paste(thumb, ((index%3)*320, (index//3)*180))
    sheet.save(output / 'contact_sheet.png')
    reader = imageio.get_reader(path)
    meta = reader.get_meta_data()
    meta.pop('nframes', None)
    count = sum(1 for _ in reader)
    reader.close()
    report = dict(started_at=started, ended_at=datetime.now(timezone.utc).isoformat(), render_seconds=render_seconds,
                  decoded_frames=count, metadata=meta, imageio=version('imageio'), pillow=version('Pillow'),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), bytes=path.stat().st_size,
                  paid_external_calls=0, agent_cost='账单未知', voice=False)
    (output/'render_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (output/'storyboard.json').write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
