"""通过系统已有中文语音生成分段旁白，不改系统配置。"""
import argparse
import hashlib
import json
import sys
import time
import wave
from datetime import datetime, timezone
from importlib.metadata import distributions
from pathlib import Path

root = Path(__file__).resolve().parents[3]
runtime_path = root / 'videos/narrated_review/runtime'
sys.path.insert(0, str(runtime_path))

from winrt.windows.media.speechsynthesis import SpeechSynthesizer
from winrt.windows.storage.streams import DataReader
from winrt.windows.foundation import AsyncStatus


def wait_operation(operation, timeout=30):
    # 原生异步操作直接等待完成，避免创建无必要的网络事件循环。
    deadline = time.monotonic() + timeout
    while operation.status == AsyncStatus.STARTED:
        if time.monotonic() >= deadline:
            operation.cancel()
            raise TimeoutError('系统语音操作等待超时')
        time.sleep(0.02)
    return operation.get_results()


def generate(args):
    items = json.loads(args.input.read_text(encoding='utf-8'))
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    synth = SpeechSynthesizer()
    synth.voice = next(voice for voice in SpeechSynthesizer.all_voices
                       if voice.display_name == args.voice and voice.language == 'zh-CN')
    synth.options.speaking_rate = args.rate
    records = []
    for item in items:
        if not item['id'].replace('_', '').isalnum():
            raise ValueError('片段编号只能使用字母、数字和下划线')
        started_at = datetime.now(timezone.utc).isoformat()
        started = time.perf_counter()
        stream = wait_operation(synth.synthesize_text_to_stream_async(item['text']))
        reader = DataReader(stream.get_input_stream_at(0))
        count = wait_operation(reader.load_async(stream.size))
        data = bytearray(count)
        reader.read_bytes(data)
        reader.close()
        stream.close()
        audio_path = output / f"{item['id']}.wav"
        audio_path.write_bytes(data)
        with wave.open(str(audio_path)) as audio:
            duration = audio.getnframes() / audio.getframerate()
            sample_rate = audio.getframerate()
        records.append({**item, 'started_at': started_at,
                        'generation_seconds': time.perf_counter() - started,
                        'audio_seconds': duration, 'sample_rate': sample_rate,
                        'slot_seconds': item['end'] - item['start'],
                        'sha256': hashlib.sha256(data).hexdigest()})
    synth.close()
    report = {'voice': args.voice, 'speaking_rate': args.rate, 'records': records,
              'dependencies': {dist.metadata['Name']: dist.version
                               for dist in distributions(path=[str(runtime_path)])},
              'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'voice_review': '未完整试听，不以生成成功代替发音和听感验收',
              'paid_external_calls': 0, 'agent_cost': '账单未知'}
    (output / 'synthesis_manifest.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--voice', default='Microsoft Huihui')
    parser.add_argument('--rate', type=float, default=1.10)
    generate(parser.parse_args())
