# 单层字幕修订候选

2026-11-06，TASK-20261106-86bc946e。视频：videos/experiments/caption_candidate_01/meeting_captioned.mp4。
SHA256：afc31bb04c9837725aa357bf8f82c72f98e39f855b5d4975e8c6d6b8a3c8766d。

修订：覆盖原底部摘要区域，在独立深色区域烧录完整旁白字幕。按标点分成两行，保留全部原始文字，避免行首句号。ASS为制作源，名称不同于MP4；播放不需要另载SRT。主对话原片未改。

检查：完整1728帧解码通过，72秒、24fps、1280×720、H.264/AAC。音轨压缩数据哈希与原旁白版相同。实际查看最终编码后5、16、28、40、52、66秒六张截图：两行字幕均在画面内，没有叠字；第五段最长行仍留左右边距。证据在输出目录frame_*.png及render_report.json。

复现：先按narrated_reproduction.md得到reproduction_package_01及reproduction_voice_01，再运行`python scripts/video/render_caption_candidate.py --run_id 新目录名`。脚本拒绝非空输出目录。需要FFmpeg的libass支持和Microsoft YaHei字体，其他系统未验证。

首次尝试的28字限制无法在第五段找到标点断句，脚本退出，尚未输出视频；放宽至32字并保持32像素字号后成功，已目检最长行。这是布局修订，不改变旁白文字或时长。

剩余：字幕为整段显示，并非逐字同步。未完整试听、动态审片或现场播放器验证；不能将截图验收扩展为最终音画验收。研究门槛亦未自动通过。
