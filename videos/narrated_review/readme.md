# 72秒中文旁白样片

播放入口：meeting_narrated_v1/meeting_explainer_narrated.mp4。

2026-11-06制作。画面来自已有V2代码动画；旁白为本机Windows Microsoft Huihui通用中文声音，语速1.1，无声音克隆。题材是模拟会议：将“争取周五”误写成“周五承诺”的示例由我们编写，不是某个产品真实犯错录像。

## 已完成的验证

- 72秒、1280×720、24fps，1728帧全部解码，AAC音轨解码通过。
- 六段旁白均在分镜时段内；没有通过截尾强行适配。PCM无饱和样本。
- 合成后视频压缩数据与无声V2一致；视频聊天独立复现画面、语音、封装，MP4哈希一致。复现详情见research/video/narrated_reproduction.md。
- MP4 SHA256：04d4ef305e2ee1fb909ff3790ed7dfa7156235c7dd9b499f271073062cb7b598。

这些检查不等于完整试听或动态验收。目前仍未确认发音自然程度、逐句音画同步和现场播放器表现。

## 字幕交付修订

独立复核发现默认播放器字幕样式会让同名SRT遮挡已有摘要。现已把逐字稿移到editing_subtitles/narration_transcript.srt，并修正句号出现在行首的问题；它仅供后续剪辑导入。MP4画面保留原摘要，不再把同名SRT放在旁边供自动加载。若需要逐字字幕，应在下一版替换摘要区，不直接覆盖两层。旧审查和旧复现目录保留原问题证据。

## 制作和复现

1. narration_segments_v2.json保存六段文案、分镜起止；v1保留初稿越界记录，不能用作最终输入。
2. scripts/video/narration/synthesize_narration.py调用系统已有中文声音，输出分段WAV和manifest。
3. scripts/video/narration/package_narrated_video.py按原分镜填入音轨，复用视频编码并执行检查。输出目录必须尚不存在。

```powershell
python scripts/video/narration/synthesize_narration.py --input videos/narrated_review/narration_segments_v2.json --output videos/narrated_review/reproduce_voice_02 --voice 'Microsoft Huihui' --rate 1.1
python scripts/video/narration/package_narrated_video.py --source videos/experiments/explainer_v2_reviewed/meeting_explainer.mp4 --audio_dir videos/narrated_review/reproduce_voice_02 --output videos/narrated_review/reproduce_package_02
```

前置：本项目Python依赖、Windows中文语音、runtime下PyWinRT依赖。已安装winrt-runtime及Foundation/Collections、Media.SpeechSynthesis、Storage.Streams均为3.2.1，typing_extensions为4.16.0。安装仅写本地runtime，没有改全局Python环境或执行策略。用到了[Microsoft系统语音接口](https://learn.microsoft.com/en-us/uwp/api/windows.media.speechsynthesis.speechsynthesizer.allvoices?view=winrt-26100)和[PyWinRT绑定](https://pywinrt.readthedocs.io/en/latest/installing/)。

失败记录：System.Speech仅列英文声；Windows PowerShell脚本被执行策略阻止，未使用Bypass；Python asyncio创建本地socket对在沙箱中挂起，已终止并改为等待WinRT原生异步状态。留存的synthesize_narration.ps1属于未采用路线。第一版旁白有三段超过镜头，通过缩短文案修正。

本地渲染与系统语音未调用外部付费API。Agent账单、设备、人工创作和审核时间未统计，不宣称整个视频“免费”或“只用几十秒”。后续如追求更自然配音，可先用本稿人工试读或另做已有授权产品的小样，不必现在录整场。
