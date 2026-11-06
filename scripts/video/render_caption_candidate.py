"""在独立候选中以单层完整字幕替换摘要，保留原音轨。"""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import imageio.v2 as imageio
import imageio_ffmpeg


def caption_time(seconds):
    value = round(seconds * 100)
    minutes, value = divmod(value, 6000)
    seconds, fraction = divmod(value, 100)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}:{minutes:02}:{seconds:02}.{fraction:02}'


def wrap_caption(text):
    candidates = [i + 1 for i, char in enumerate(text[:-1])
                  if char in '。，；：' and i + 1 <= 32 and len(text)-i-1 <= 32]
    if not candidates:
        raise ValueError('需要人工安排两行字幕断句')
    split = min(candidates, key=lambda i: abs(i-len(text)/2))
    return text[:split] + r'\N' + text[split:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', required=True)
    args = parser.parse_args()
    if not args.run_id.replace('_', '').isalnum():
        raise ValueError('run_id仅允许字母数字与下划线')
    root = Path(__file__).resolve().parents[2]
    source_dir = root / 'videos/experiments/reproduction_package_01'
    source = source_dir / 'meeting_explainer_narrated.mp4'
    source_report = json.loads((source_dir / 'package_check.json').read_text(encoding='utf-8'))
    manifest = json.loads((root / 'videos/experiments/reproduction_voice_01/synthesis_manifest.json').read_text(encoding='utf-8'))
    output = root / 'videos/experiments' / args.run_id
    output.mkdir(exist_ok=True)
    if any(output.iterdir()):
        raise FileExistsError('输出目录非空，必须使用新run_id')
    header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei,32,&H00FFFFFF,&H00FFFFFF,&H003B2414,&H003B2414,0,0,0,0,100,100,0,0,1,0,0,2,60,60,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    cues = []
    for record, check in zip(manifest['records'], source_report['scene_checks'], strict=True):
        assert record['id'] == check['id']
        wrapped = wrap_caption(record['text'])
        assert wrapped.replace(r'\N', '') == record['text']
        cues.append(f"Dialogue: 0,{caption_time(check['start'])},{caption_time(check['end'])},Default,,0,0,0,,{wrapped}")
    (output / 'captions.ass').write_text(header + '\n'.join(cues), encoding='utf-8')
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    def run(arguments):
        result = subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', *arguments],
                                cwd=output, capture_output=True, check=True)
        return result.stdout.decode('utf-8', errors='replace').strip()

    final = output / 'meeting_captioned.mp4'
    run(['-i', str(source), '-vf', 'drawbox=x=0:y=610:w=1280:h=100:color=0x14243b:t=fill,ass=captions.ass',
         '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'copy',
         '-movflags', '+faststart', str(final)])
    audio_hash = lambda path: run(['-i', str(path), '-map', '0:a:0', '-c:a', 'copy',
                                  '-f', 'hash', '-hash', 'sha256', '-'])
    assert audio_hash(source) == audio_hash(final)
    run(['-i', str(final), '-f', 'null', '-'])
    reader = imageio.get_reader(final)
    metadata = reader.get_meta_data()
    metadata.pop('nframes', None)
    seconds = [5, 16, 28, 40, 52, 66]
    frame_count = 0
    for index, frame in enumerate(reader):
        if index in [second * 24 for second in seconds]:
            imageio.imwrite(output / f'frame_{index//24:02}.png', frame)
        frame_count += 1
    reader.close()
    report = {'created_at': datetime.now(timezone.utc).isoformat(),
              'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'output_sha256': hashlib.sha256(final.read_bytes()).hexdigest(),
              'metadata': metadata, 'decoded_frames': frame_count, 'audio_packets_unchanged': True,
              'captions': cues, 'boundary': '整段字幕，非逐字同步；未完整试听和动态审片'}
    (output / 'render_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
