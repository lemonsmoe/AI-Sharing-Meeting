from pathlib import Path
from html import escape
import json
from PIL import Image, ImageDraw, ImageFont


root_dir = Path(__file__).resolve().parent
image = Image.new('RGB', (1920, 1080), '#f4f6fa')
draw = ImageDraw.Draw(image)
svg_parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">']
font_path = 'C:/Windows/Fonts/msyh.ttc'
width_checks = []


def rectangle(x, y, width, height, color, radius=0):
    draw.rounded_rectangle((x, y, x + width, y + height), radius, fill=color)
    svg_parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{color}"/>')


def text_line(x, y, value, size, color='#15233b', max_width=1760):
    font = ImageFont.truetype(font_path, size)
    width = draw.textlength(value, font=font)
    width_checks.append({'text': value, 'width': round(width, 1), 'limit': max_width, 'fits': width <= max_width})
    draw.text((x, y), value, font=font, fill=color, anchor='lt')
    svg_parts.append(f'<text x="{x}" y="{y + size}" font-family="Microsoft YaHei, sans-serif" font-size="{size}" fill="{color}">{escape(value)}</text>')


rectangle(0, 0, 1920, 1080, '#f4f6fa')
rectangle(80, 70, 8, 88, '#245ad3', 4)
text_line(112, 65, 'AI用法演变：从给例子，到交付可检查的任务', 52)
text_line(112, 137, '代表性公开节点  ·  按时间阅读  ·  能力逐步组合，旧用法继续有效', 27, '#58657b')

milestones = [
    ('2020.05.28', '论文首版', 'GPT-3：给例子', '给任务说明和少量示例', 'H1'),
    ('2022.11.30', '产品预览', 'ChatGPT：来回聊', '追问、修改、补充要求', 'H2'),
    ('2023.06.13', 'API发布', '函数调用：接工具', '让应用查数据、执行操作', 'H3'),
    ('2024.11.25', '协议发布', 'MCP：统一连接', '用标准接口连接外部系统', 'H4'),
    ('2025.05.16', '产品预览', 'Codex：委派任务', '在环境里改文件、跑检查', 'H5'),
    ('2025.10.16', '官方介绍', 'Skills：复用做法', '按需加载说明、脚本、资源', 'H6'),
    ('2025.11.26', '工程文章', 'Harness：接续工作', '留进度，分步做，跨会话接续', 'H7'),
    ('2026.04.08', '工程文章', '托管运行：分离组件', '会话、调度与执行环境分开', 'H8'),
]
for index, (date, kind, title, body, source_id) in enumerate(milestones):
    row, column = divmod(index, 4)
    x, y = 80 + column * 450, 230 + row * 300
    rectangle(x, y, 410, 245, '#ffffff', 18)
    text_line(x + 24, y + 20, f'{index + 1:02d}', 23, '#245ad3', 50)
    text_line(x + 80, y + 20, date, 25, '#245ad3', 220)
    text_line(x + 24, y + 67, kind, 21, '#68778e', 362)
    text_line(x + 24, y + 110, title, 31, max_width=362)
    text_line(x + 24, y + 166, body, 25, '#4d5d74', 362)
    text_line(x + 350, y + 212, source_id, 17, '#68778e', 45)
    if column < 3:
        text_line(x + 418, y + 109, '→', 25, '#8a9ab2', 30)

text_line(80, 490, '时间续接 ↓  05—08按下行从左向右阅读；箭头只表示先后', 20, '#68778e')
rectangle(80, 825, 1760, 143, '#152b50', 18)
text_line(108, 846, '今天：按任务组合这些能力', 29, '#ffffff')
text_line(108, 894, '提示词讲目标  ·  Skills复用做法  ·  工具/API或MCP连接系统', 28, '#dce7ff')
text_line(108, 931, 'Agent循环执行  ·  运行框架保存进度与支持验收', 25, '#dce7ff')
text_line(80, 992, '日期不等于技术诞生或全民普及。代表节点截至2026.04；2026.11.06核验。来源H1—H8见讲者备注。', 22, '#68778e')
svg_parts.append('</svg>')
(root_dir / 'history_timeline.svg').write_text('\n'.join(svg_parts), encoding='utf-8')
image.save(root_dir / 'history_timeline.png')
(root_dir / 'layout_check.json').write_text(json.dumps(width_checks, ensure_ascii=False, indent=2), encoding='utf-8')
assert all(item['fits'] for item in width_checks), '存在文本超过预留宽度'
print('已生成SVG与PNG；全部文本宽度检查通过。')
