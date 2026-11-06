# 带旁白制作链复现

2026-11-06，视频聊天在独立目录运行主对话语音与封装脚本。没有修改主对话文件，没有安装新依赖，也没有调用外部付费语音API。

## 结果

画面、六段系统语音和封装全部重新生成，三个命令退出码均为0。最终72秒、1280×720、24fps、H.264/AAC，1728帧解码通过。最终MP4 SHA256与主对话旁白版完全一致：`04d4ef305e2ee1fb909ff3790ed7dfa7156235c7dd9b499f271073062cb7b598`。

产物：`videos/experiments/reproduction_package_01/meeting_explainer_narrated.mp4`。这是复现件，**继承原版SRT遮挡摘要问题**，不是修订版或最终推荐版。原问题见narrated_audit/review.md。

## 已执行命令

从项目根目录运行，输出目录必须尚不存在；再次复现时统一更换三个目录名。

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
python scripts/video/render_explainer.py --run_id reproduction_visual_01
python scripts/video/narration/synthesize_narration.py --input videos/narrated_review/narration_segments_v2.json --output videos/experiments/reproduction_voice_01 --voice 'Microsoft Huihui' --rate 1.1
python scripts/video/narration/package_narrated_video.py --source videos/experiments/reproduction_visual_01/meeting_explainer.mp4 --audio_dir videos/experiments/reproduction_voice_01 --output videos/experiments/reproduction_package_01
```

前置条件：已有Windows中文Microsoft Huihui系统语音、微软雅黑字体及本项目Python依赖。语音脚本加载`videos/narrated_review/runtime`内的WinRT依赖，所以只复制三个脚本到另一台机器不能保证运行。实际语音依赖及版本见`videos/experiments/reproduction_voice_01/synthesis_manifest.json`。本轮未验证全新环境安装、其他操作系统或其他声音。

## 时间与费用

|阶段|本轮命令墙钟时间|包含范围|
|---|---:|---|
|画面|20.241秒|渲染、抽帧保存、解码检查；纯渲染13.676秒|
|六段语音|0.831秒|Python启动及已有系统语音合成，不含语音安装|
|封装|6.316秒|音轨排列、AAC编码、数据哈希与解码检查|
|三条命令合计|27.388秒|不含命令间间隔、准备、写稿、修改或人工验收|

本地脚本外部付费调用为0。Agent账单、电力、设备摊销与人工总工时没有计量，不报告“免费”或端到端节时比例。记录见reproduction_execution.json。

## 验收边界

本轮证明已有输入与源码在当前已配置环境可重复生成同一文件，不证明从新需求独立创作两次，也不证明跨机器位级一致。未完整试听、动态播放或验证现场播放器。六段音频适配分镜时长只排除文件越界，不证明逐句语义同步。
