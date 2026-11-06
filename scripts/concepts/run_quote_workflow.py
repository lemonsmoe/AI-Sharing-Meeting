import json
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

base_path = Path('research/concepts/experiments')
start_time = datetime.now(timezone.utc).isoformat()
start_counter = time.perf_counter()
data = json.loads((base_path / 'quote_input.json').read_text(encoding='utf-8-sig'))
rows = ['# 模拟采购比较', '', '|供应商|含税到货总价/元|交期判断|', '|---|---:|---|']
results = []
for quote in data['quotes']:
    multiplier = Decimal('1') if quote['tax_included'] else Decimal('1') + Decimal(str(quote['tax_rate']))
    total = Decimal(str(quote['unit_price'])) * data['quantity'] * multiplier + Decimal(str(quote['shipping']))
    days = quote['delivery_days']
    status = '未知' if days is None else ('满足' if days <= data['deadline_days'] else '不满足')
    results.append({'supplier': quote['supplier'], 'total': str(total.quantize(Decimal('0.01'))), 'status': status})
    rows.append(f"|{quote['supplier']}|{total:.2f}|{status}|")
rows.extend(['', '待确认：B交期；所有报价有效期和实际供货能力。仅模拟材料，未下单。'])
(base_path / 'quote_deliverable.md').write_text('\n'.join(rows), encoding='utf-8')
report = {'started_at': start_time, 'ended_at': datetime.now(timezone.utc).isoformat(), 'duration_seconds': time.perf_counter() - start_counter, 'results': results, 'scope': '真实Python执行；非独立模型实验；不含人工耗时'}
(base_path / 'quote_run.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('quote_deliverable.md generated')
