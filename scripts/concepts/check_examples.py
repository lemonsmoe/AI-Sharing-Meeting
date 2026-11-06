import json
import time
from datetime import datetime, timezone
from pathlib import Path

started_at = datetime.now(timezone.utc).isoformat()
started = time.perf_counter()
checks = {
    'quote_a': 100 * 80 * 113 // 100 + 200 == 9240,
    'quote_b': 100 * 88 + 500 == 9300,
    'quote_c': 100 * 90 == 9000,
    'deadline_a': 7 <= 9,
    'deadline_c_rejected': 10 > 9,
    'policy_excess': 480 - 450 == 30,
}
report = {
    'started_at': started_at,
    'ended_at': datetime.now(timezone.utc).isoformat(),
    'duration_seconds': time.perf_counter() - started,
    'scope': '仅独立核算模拟题算术，不是模型复测或自然语言正确性验证',
    'checks': checks,
}
output = Path('research/concepts/experiments/arithmetic_check.json')
output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
