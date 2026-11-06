"""从已审阅V2准备V3讲稿与输入快照，保留所有旧文件。"""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[3]
inputs = root / 'slides/review_v3/inputs'
source = (root / 'docs/content/rehearsal_script_v2.md').read_text(encoding='utf-8')
overrides = json.loads((inputs / 'script_overrides.json').read_text(encoding='utf-8'))
parts = re.split(r'(?=^## \d{2}｜)', source, flags=re.M)
parts[0] = parts[0].replace('试讲稿 V2', '试讲稿 V3').replace(
    '对应冻结内容源 `slides_content_v1.json` 的第1—30页。本文件补充口语、演示和转场，不修改正在制作的PPT输入。',
    '对应30页V3；依据V2逐页审阅、历史与工具地图补充以及实际Excel、中文旁白样片修订。V1/V2继续保留。')
for index in range(1, len(parts)):
    section = parts[index]
    number = re.match(r'## (\d{2})｜', section).group(1)
    old_header = section.split('\n', 1)[0]
    if str(int(number)) in overrides:
        item = overrides[str(int(number))]
        budget = old_header.rsplit('｜', 1)[1]
        parts[index] = f'## {number}｜{item["title"]}｜{budget}\n\n{item["body"]}\n\n'
script = ''.join(parts).replace('第27页72秒视频已经接近1.5分钟页预算，应少讲；第21页录屏与第12/16/24页文件操作都要提前排练。',
                                '第27页72秒视频已经接近1.5分钟页预算，应少讲；第21页文件展示与第12/16/24页文件操作都要提前排练。')
script = script.replace('[用报价中“交期未知”的分支演示一次循环，别把所有任务都画成无限自主执行。]',
                        '当缺少必要材料或权限，继续重试不一定有用。应当停下来请求确认，或者交付当前能确定的部分。\n\n[用报价中“交期未知”的分支演示一次循环。]')
(root / 'docs/content/rehearsal_script_v3.md').write_text(script, encoding='utf-8')
(inputs / 'rehearsal_script_v3.md').write_text(script, encoding='utf-8')
files = [
    'outputs/leadership_review_v2/leadership_review_v2.pptx',
    'docs/content/deck_review_v2.md', 'docs/content/integration_addendum_v3.md',
    'research/concepts/history_addendum/history_brief.md',
    'research/concepts/history_addendum/source_register.md',
    'research/methodology/tool_landscape/comparison.md',
    'outputs/01a1afcd-c994-7ae0-89e1-3c3770ac406b/meeting_actions.xlsx',
    'videos/experiments/caption_candidate_01/meeting_captioned.mp4',
    'docs/content/rehearsal_script_v3.md'
]
manifest = [{'path': name, 'sha256': hashlib.sha256((root / name).read_bytes()).hexdigest()}
            for name in files]
(inputs / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
assert len(re.findall(r'^## \d{2}｜', script, re.M)) == 30
print('V3讲稿30页与输入快照已准备')
