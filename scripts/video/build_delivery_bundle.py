"""打包视频审阅件与复现输入，逐条核验压缩包内容。"""
import hashlib
import argparse
import json
import zipfile
from pathlib import Path


root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--run_id', default='delivery_bundle_02')
args = parser.parse_args()
if not args.run_id or any(char not in 'abcdefghijklmnopqrstuvwxyz0123456789_' for char in args.run_id):
    parser.error('run_id仅支持小写英文字母、数字和下划线')
output = root / 'videos/experiments' / args.run_id
output.mkdir(exist_ok=False)
paths = [
    'scripts/video/render_explainer.py',
    'scripts/video/render_caption_candidate.py',
    'scripts/video/narration/synthesize_narration.py',
    'scripts/video/narration/package_narrated_video.py',
    'videos/narrated_review/narration_segments_v2.json',
]
paths += [path.relative_to(root).as_posix() for path in
          (root / 'videos/experiments/caption_candidate_01').iterdir() if path.is_file()]
for name in ['next_animation_brief.md', 'tool_candidates_slide_28.md', 'v3_route_brief.md',
             'narrated_reproduction.md', 'caption_candidate_review.md', 'claim_evidence_review.md']:
    paths.append(f'research/video/{name}')
payload = {name: (root / name).read_bytes() for name in paths}
payload['requirements.txt'] = b'numpy==1.26.4\nPillow==10.4.0\nimageio==2.37.4\nimageio-ffmpeg==0.6.0\n'
payload['voice_requirements.txt'] = (
    'winrt-runtime==3.2.1\nwinrt-Windows.Foundation==3.2.1\n'
    'winrt-Windows.Foundation.Collections==3.2.1\nwinrt-Windows.Media.SpeechSynthesis==3.2.1\n'
    'winrt-Windows.Storage.Streams==3.2.1\ntyping_extensions==4.16.0\n').encode()
payload['readme.md'] = '''# 72秒AI教学视频审阅包

状态：主对话准备采用的V3候选；完整试听、动态审片及最终研究推荐仍未通过。

先播放 `videos/experiments/caption_candidate_01/meeting_captioned.mp4`。
它已烧录单层完整字幕，含Microsoft Huihui通用系统旁白；不需要额外载入字幕。
内容为模拟会议核查，错误草稿是教学设计，不是某产品真实错误录像。

脚本分镜：research/video/next_animation_brief.md；实际旁白：videos/narrated_review/narration_segments_v2.json。
最新路线与费用：research/video/v3_route_brief.md（核实日2026-11-06，含上屏稿、口语和案例，未做工具采购推荐）。
research/video/tool_candidates_slide_28.md保留为历史候选表，以最新路线稿的现状说明为准。
实际复现：research/video/narrated_reproduction.md；字幕修订：research/video/caption_candidate_review.md。
每个文档可能引用原工作区的进一步证据；本包只包含运行和快速审阅所需文件，不是完整研究档案。

## 当前已验证

72秒、1280×720、24fps，1728帧完整解码；六段最终编码截图已检查，无双层字幕遮挡；字幕文字与旁白输入一致，原音轨压缩数据保留。
画面、语音、封装在已配置Windows机器重跑，原旁白版MP4哈希相同。V3修改字幕后又完整解码。
未完整试听或动态观看，不保证发音、逐句同步及现场播放器兼容性。整段字幕不是逐字对齐。

## 在Windows复现

解压到新目录。需要Python 3.12、已安装的Microsoft Huihui中文语音和微软雅黑字体。
包内不分发系统语音、字体或第三方二进制。下列安装步骤仅为依据已用版本整理的准备命令，**尚未在全新环境安装验证**；已有环境的制作命令已运行过。

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pip install --target videos/narrated_review/runtime -r voice_requirements.txt
$env:PYTHONIOENCODING='utf-8'
.venv/Scripts/python.exe scripts/video/render_explainer.py --run_id reproduction_visual_01
.venv/Scripts/python.exe scripts/video/narration/synthesize_narration.py --input videos/narrated_review/narration_segments_v2.json --output videos/experiments/reproduction_voice_01 --voice 'Microsoft Huihui' --rate 1.1
.venv/Scripts/python.exe scripts/video/narration/package_narrated_video.py --source videos/experiments/reproduction_visual_01/meeting_explainer.mp4 --audio_dir videos/experiments/reproduction_voice_01 --output videos/experiments/reproduction_package_01
.venv/Scripts/python.exe scripts/video/render_caption_candidate.py --run_id caption_rebuilt_01
```

最终打开 `videos/experiments/caption_rebuilt_01/meeting_captioned.mp4`。前三步的目录名是字幕修订脚本当前约定，不能随意改名；重复复现宜重新解压到新目录，避免覆盖历史。
不使用中间封装件的同名SRT进行最终展示；最终单层字幕已经写入画面。

## 文件核对

manifest.json列出除清单自身外每个条目的SHA256与字节数。ZIP已按原始字节逐项复核。
这是文件完整性检查，不是媒体听感或教学效果验收。制作未调用外部付费API，但Agent账单、设备和人工成本未知。
'''.encode('utf-8')
manifest = {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            for name, data in payload.items()}
payload['manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8')
archive = output / 'teaching_video_v3_review.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
    for name, data in payload.items():
        bundle.writestr(name, data)
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    for name, data in payload.items():
        assert bundle.read(name) == data, name
report = {'files': len(payload), 'bytes': archive.stat().st_size,
          'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
          'all_entries_match': True, 'clean_environment_install_tested': False}
(output / 'bundle_check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
