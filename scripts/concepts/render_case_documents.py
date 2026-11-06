import json
import time
from datetime import datetime, timezone
from pathlib import Path

base_path = Path('research/concepts/experiments')
started_at = datetime.now(timezone.utc).isoformat()
started = time.perf_counter()
data = json.loads((base_path / 'structured_outputs.json').read_text(encoding='utf-8-sig'))
meeting = data['meeting']
rows = ['# 模拟会议交接单', '', '## 已确认任务', '', '|事项|负责人|期限|来源|', '|---|---|---|---|']
for item in meeting['confirmed']:
    rows.append('|{}|{}|{}|{}|'.format(item['task'], item['owner'], item['deadline'], item['source']))
rows.extend(['', '## 待分工需求'])
for item in meeting['unassigned']:
    rows.append(f"- {item['task']}；负责人和期限待确认。依据{item['source']}。")
rows.extend(['', '## 未决事项'])
for item in meeting['undecided']:
    rows.append(f"- {item['question']}：{item['condition']}。依据{item['source']}。")
(base_path / 'meeting_deliverable.md').write_text('\n'.join(rows), encoding='utf-8')
policy = data['policy']
excess = policy['requested'] - policy['limit']
answer = f"# 模拟制度答复\n\n依据{policy['selected_source']}，标准为{policy['limit']}元/晚。申请{policy['requested']}元超过{excess}元，不能直接按标准认定符合。\n\n例外条件：{policy['exception']}；是否获批未知。\n\n排除依据：{'；'.join(policy['excluded_sources'])}。\n\n仅模拟制度，不代表本公司规定。"
(base_path / 'policy_deliverable.md').write_text(answer, encoding='utf-8')
checks = {
    'meeting_no_shipping_commitment': not any('发货' in item['task'] for item in meeting['confirmed']),
    'meeting_unknown_preserved': all(item['owner'] is None and item['deadline'] is None for item in meeting['unassigned']),
    'policy_excess_30': excess == 30,
    'policy_simulation': policy['simulation'],
}
report = {'started_at': started_at, 'ended_at': datetime.now(timezone.utc).isoformat(), 'seconds': time.perf_counter() - started, 'checks': checks, 'scope': '当前模型抽取并保存结构化输入，Python真实渲染及局部验证；不是自动NLP抽取器，不是独立模型复测'}
(base_path / 'document_run.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
assert all(checks.values())
print('2 documents generated; 4 scoped checks passed')
