import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

base_path = Path('research/concepts/experiments')
report = json.loads((base_path / 'quote_run.json').read_text(encoding='utf-8'))
actual = {row['supplier']: row for row in report['results']}
expected = {'A': ('9240.00', '满足'), 'B': ('9300.00', '未知'), 'C': ('9000.00', '不满足')}
checks = {
    supplier: Decimal(actual[supplier]['total']) == Decimal(total) and actual[supplier]['status'] == status
    for supplier, (total, status) in expected.items()
}
output = {'checked_at': datetime.now(timezone.utc).isoformat(), 'input_report': 'quote_run.json', 'checks': checks, 'scope': '读取实际执行输出，检查三份模拟报价金额与交期分类；不是模型独立复测'}
(base_path / 'quote_output_check.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
assert all(checks.values()), checks
print('3 quote output checks passed')
