"""独立检查当前旁白成片，字幕截图仅代表FFmpeg默认渲染。"""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import imageio_ffmpeg
import numpy as np


def main():
    root = Path(__file__).resolve().parents[2]
    source_dir = root / 'videos/narrated_review/meeting_narrated_v1'
    output = root / 'research/video/narrated_audit'
    output.mkdir(exist_ok=True)
    video = source_dir / 'meeting_explainer_narrated.mp4'
    subtitle = source_dir / 'meeting_explainer_narrated.srt'
    caption_copy = output / 'captions.srt'
    caption_copy.write_bytes(subtitle.read_bytes())
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    def run(arguments):
        return subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', *arguments],
                              cwd=output, capture_output=True, check=True).stdout

    audio = np.frombuffer(run(['-i', str(video), '-map', '0:a:0', '-ac', '1', '-ar',
                              '16000', '-f', 'f32le', '-']), dtype='<f4')
    run(['-i', str(video), '-f', 'null', '-'])
    original = root / 'videos/experiments/explainer_v2_reviewed/meeting_explainer.mp4'
    video_hash = lambda path: run(['-i', str(path), '-map', '0:v:0', '-c:v', 'copy',
                                  '-f', 'hash', '-hash', 'sha256', '-']).decode().strip()
    findings = []
    for block in subtitle.read_text(encoding='utf-8').strip().split('\n\n'):
        lines = block.splitlines()
        values = re.findall(r'(\d\d):(\d\d):(\d\d),(\d{3})', lines[1])
        times = [int(h)*3600+int(m)*60+int(s)+int(ms)/1000 for h, m, s, ms in values]
        findings.append({'cue': int(lines[0]), 'start': times[0], 'end': times[1],
                         'characters_per_second': round(len(''.join(lines[2:])) / (times[1]-times[0]), 2),
                         'line_lengths': [len(line) for line in lines[2:]],
                         'punctuation_at_line_start': [line for line in lines[2:] if line[0] in '。，、；：！？']})
    for second in (28, 52, 66):
        run(['-i', str(video), '-vf', 'subtitles=captions.srt', '-ss', str(second),
             '-frames:v', '1', '-y', f'caption_default_{second}.png'])
    report = {'checked_at': datetime.now(timezone.utc).isoformat(),
              'video_sha256': hashlib.sha256(video.read_bytes()).hexdigest(),
              'srt_sha256': hashlib.sha256(subtitle.read_bytes()).hexdigest(),
              'full_av_decode_passed': True, 'video_packets_match_original': video_hash(video) == video_hash(original),
              'decoded_audio_seconds': len(audio)/16000, 'decoded_audio_peak': float(np.max(np.abs(audio))),
              'decoded_audio_samples_at_or_above_full_scale': int(np.sum(np.abs(audio) >= 1)),
              'cues': findings, 'boundary': '未完整试听和动态审片；默认libass截图不代表所有播放器布局'}
    (output / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
