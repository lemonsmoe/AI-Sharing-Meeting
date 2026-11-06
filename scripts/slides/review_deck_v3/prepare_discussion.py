"""保留已整理来源，加入本轮已审阅的四条记录。"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
directory = root / 'research/integration/v3'
packet = json.loads((directory / 'discussion_packet.json').read_text(encoding='utf-8-sig'))
items = json.loads((directory / 'discussion_input.json').read_text(encoding='utf-8'))['items']
points = packet['previous_summary']['points']
for index, item in enumerate(items):
    points.append({**item, 'sources': [f'note_21f0657974e665c04808#{index}']})
summary = {
    'topic': 'workshop_scope', 'notes_revision': packet['notes_revision'],
    'base_summary_revision': packet['base_summary_revision'],
    'title': '分享会V3审阅包与后续验证',
    'abstract': '30页V3、同步讲稿和离线整包完成，PowerPoint及Excel副本回存通过；完整试听、现场计时和主推研究仍待。',
    'points': points, 'omitted': packet['previous_summary'].get('omitted', [])
}
(directory / 'discussion_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'保留旧来源并增加本轮记录，共{len(points)}条')
