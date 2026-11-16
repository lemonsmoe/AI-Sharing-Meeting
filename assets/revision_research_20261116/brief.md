# 2026-11-16 改稿素材交付

任务 TASK-20261115-8992b1fe。全部文件只落在本目录；未操作桌面、未改主PPT/讲稿、未Git。

## 直接可用

1. P06 引语：`karpathy_portrait.jpg`，本人官网1024平方肖像，已看图。英文 **The hottest new programming language is English**。中文 **最热门的新编程语言是英语。** 下标 Andrej Karpathy · AI研究者、OpenAI创始团队成员 · 2023-01-24。X原推网页403，但官方公开oEmbed接口已成功返回作者、完整原话、日期，证据 `karpathy_quote_oembed.json`。不写Tesla现任高管。
2. 原理页首选 `next_token_autoregression.gif`（原作者1432×501、53帧）。需要静态图用 `next_token_autoregression_frame38.png`，这是原GIF原样帧导出，已实际看图，能看到“A robot may”回填进上下文。不是重新画的架构图。保留图内GPT-2标签，并在备注说这是早期模型的原理示意，不代表2026产品界面。来源 Jay Alammar, The Illustrated GPT-2。插入GIF需确认PPT放映实际播放，SVG管线通常只保留首帧，因此静态帧更稳。
3. GPT黑标：`chatgpt_official_black.png`（180平方）/同名SVG，来自ChatGPT官网favicon。已看图为白圆底黑色Blossom。
4. 即梦：`jimeng_official_icon.png`，官网ICO原样转PNG。横标 `jimeng_official.png` 是白字，不建议米白背景上直接使用。
5. 小云雀：`xiaoyunque_official.png`为官网64平方黑白鸟图标；高分辨率优先 `xiaoyunque_inline_0.svg`，是官网header品牌标原样提取，currentColor默认黑色。配可编辑“小云雀”文字即可。

## 型号文字建议

当前公开官方来源可核实 **GPT-6.1 Sol / Claude Opus 5.5 / Doubao Seed2.1 Pro**。可作为模型家族示例，页脚或备注注明核查2026-11-16。OpenAI另有GPT-6.1 Terra（10-26）及GPT-6 Astra，版本号不等于统一性能排名；普通ChatGPT Chat与Work/Codex可选模型不同，不能把GPT-6.1 Sol写成所有ChatGPT账户默认型号。豆包App底层型号不直接等同Seed官网API型号。

## 已剔除/保留备选

- `next_token_output_static.png`技术信息太多，不建议普通同事主画面。
- `next_token_output_scores.png`原图把logits/概率混写，且存在负数，不能拿这些数字当概率讲，不建议使用。
- 来源网页、下载URL、用途、实测/原理示意状态和SHA256均在 `provenance.json`。

## 来源

- 引语：[X原推](https://x.com/karpathy/status/1617979122625712128)，[本人官网](https://karpathy.ai/)
- 原图：[The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/)，文章页标示CC BY-NC-SA 4.0，保持作者归属；不是本项目实测截图。
- GPT：[模型页](https://developers.openai.com/api/docs/models/gpt-6.1-sol)，[API更新记录](https://developers.openai.com/api/docs/changelog)，[产品入口差异](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt)
- Claude：[官方Opus5.5页](https://www.anthropic.com/claude-opus-5-5)
- Seed：[官方模型目录](https://seed.bytedance.com/en/models)
- Logo：[ChatGPT](https://chatgpt.com/)，[即梦](https://jimeng.jianying.com/)，[小云雀](https://xyq.jianying.com/)
