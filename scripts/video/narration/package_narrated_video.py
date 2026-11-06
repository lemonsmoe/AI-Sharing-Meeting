"""按分镜放置旁白并封装视频，校验时长、音轨和视频数据。"""
import argparse
import hashlib
import json
import subprocess
import wave
from datetime import datetime, timezone
from pathlib import Path

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np


def run_ffmpeg(ffmpeg, args):
    result = subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', *args],
                            capture_output=True, text=True, encoding='utf-8',
                            errors='replace', check=True)
    return result.stdout.strip()


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'


def subtitle_lines(text, width=28):
    lines = []
    punctuation = '，。；：！？、'
    while len(text) > width:
        stops = [index + 1 for index, char in enumerate(text[:width])
                 if char in punctuation and index >= width // 2]
        cut = stops[-1] if stops else width
        while cut < len(text) and text[cut] in punctuation:
            cut += 1
        lines.append(text[:cut])
        text = text[cut:]
    return '\n'.join([*lines, text])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--audio_dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((args.audio_dir / 'synthesis_manifest.json').read_text(encoding='utf-8'))
    duration = max(item['end'] for item in manifest['records'])
    sample_rate = 16000
    audio_track = np.zeros(round(duration * sample_rate), dtype='<i2')
    cues, checks = [], []
    for index, item in enumerate(manifest['records']):
        path = args.audio_dir / f"{item['id']}.wav"
        with wave.open(str(path)) as audio:
            assert (audio.getframerate(), audio.getnchannels(), audio.getsampwidth()) == (sample_rate, 1, 2)
            samples = np.frombuffer(audio.readframes(audio.getnframes()), dtype='<i2')
        start = item['start'] + (0 if index == 0 else 0.25)
        end = start + len(samples) / sample_rate
        if end > item['end']:
            raise ValueError(f"{item['id']}旁白超过分镜时长，需缩短文案")
        offset = round(start * sample_rate)
        audio_track[offset:offset + len(samples)] = samples
        non_silent = np.flatnonzero(np.abs(samples.astype(np.int32)) > 327)
        checks.append({'id': item['id'], 'start': start, 'end': end,
                       'slot_end': item['end'], 'fits_without_cutting': True,
                       'last_audible_second': start + (int(non_silent[-1]) / sample_rate if len(non_silent) else 0)})
        cues.append(f"{index+1}\n{timestamp(start)} --> {timestamp(end)}\n" +
                    subtitle_lines(item['text']) + '\n')
    audio_path = args.output / 'narration_full.wav'
    with wave.open(str(audio_path), 'wb') as audio:
        audio.setparams((1, 2, sample_rate, len(audio_track), 'NONE', 'not compressed'))
        audio.writeframes(audio_track.tobytes())
    subtitle_dir = args.output / 'editing_subtitles'
    subtitle_dir.mkdir()
    (subtitle_dir / 'narration_transcript.srt').write_text('\n'.join(cues), encoding='utf-8')
    output_path = args.output / 'meeting_explainer_narrated.mp4'
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    run_ffmpeg(ffmpeg, ['-i', str(args.source), '-i', str(audio_path), '-map', '0:v:0',
                       '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k',
                       '-t', str(duration), '-movflags', '+faststart', str(output_path)])
    packet_hash = lambda path: run_ffmpeg(ffmpeg, ['-i', str(path), '-map', '0:v:0',
                                                  '-c:v', 'copy', '-f', 'hash', '-hash', 'sha256', '-'])
    source_hash, result_hash = packet_hash(args.source), packet_hash(output_path)
    assert source_hash == result_hash, '封装后视频数据变化'
    run_ffmpeg(ffmpeg, ['-i', str(output_path), '-map', '0:a:0', '-f', 'null', '-'])
    reader = imageio.get_reader(output_path)
    metadata = reader.get_meta_data()
    metadata.pop('nframes', None)
    frames = sum(1 for _ in reader)
    reader.close()
    report = {'created_at': datetime.now(timezone.utc).isoformat(),
              'source_video_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
              'output_sha256': hashlib.sha256(output_path.read_bytes()).hexdigest(),
              'voice': manifest['voice'], 'speaking_rate': manifest['speaking_rate'],
              'decoded_frames': frames, 'metadata': metadata, 'scene_checks': checks,
              'video_packets_unchanged': source_hash == result_hash,
              'audio_decode_passed': True,
              'pcm_clipped_samples': int(np.sum(np.abs(audio_track.astype(np.int32)) >= 32767)),
              'pcm_peak': int(np.max(np.abs(audio_track.astype(np.int32)))),
              'qa_boundary': '完整解码及音轨封装校验；尚未完整试听与动态审片。画面已有摘要字幕，逐字SRT仅供剪辑导入，单放editing_subtitles以避免同名自动叠加'}
    (args.output / 'package_check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
