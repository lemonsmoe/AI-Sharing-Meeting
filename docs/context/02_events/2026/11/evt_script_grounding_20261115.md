---
id: EVT-20261115-2355-script-grounding
event_time: 2026-11-15T23:55:00+08:00
recorded_at: 2026-11-15T23:55:00+08:00
agent: session-5bed8c8e-3817-428c-881d-0e734bbdbe31
domain: content
kind: deliverable
status: review
summary: 30页照读稿全稿中文口语修订，分支提交，待用户语感与可选加料确认
related_paths:
  - docs/content/swiss_script_20261115/speaker_script.md
  - docs/content/swiss_script_20261115/script_revision_notes_20261115.md
  - docs/context/05_discussions/topics/workshop_scope/notes/109f71f806ddc2c976ee/note_a38e52231f65933361a0.md
related_commits: []
supersedes: []
---

# 11 月 15 日深夜讲稿中文口语修订

- 新接续 Agent（DSH 会话 session-5bed8c8e-3817-428c-881d-0e734bbdbe31）按用户反馈推进：用户认为 Codex 讲稿中文表达不接地气、不符合中文习惯，PPT 三页风格评价为「还可以」，未按定稿处理。用户同时授权新分支提交保存。
- 按接续提示执行 status/sync/ack，读 content 领域与 workshop_scope、office 议题；以真实会话身份认领任务 TASK-20261115-e233786d，在分支 task/001-script-grounding 上工作，未冒充原主对话，未改动本机绑定文件。
- 全稿 30 页重写：去翻译腔、合并短句、术语口语化，织回用户《公司分享.md》原有比喻（同事交接、老板员工不打螺丝、许愿机、甲方乙方、上下文有限、B站链接）。保留页序、页题、页时预算与全部事实边界：产品/模型表述、两处人物引语、教学示意标记未改。汉字 9,531 → 9,026（-5%），48 分钟预算不变。
- 改动对照与三处可选加料（百度笑话、幻觉实例、分部门例子）在 script_revision_notes_20261115.md，待用户选择；办公案例三选仍待定，确认后再并话术。
- 讨论候选已记录为 workshop_scope 议题 note_a38e52231f65933361a0（pending），总结合并仍由主对话执行。
- 剩余缺口：用户语感反馈、可选加料选择、办公案例定稿、表情包原件、30 页 PPT 扩稿与备注合稿、真人试讲计时与现场设备检查。

## 补充：16 日凌晨关键来源复核

- 逐项复核 17 处主张：Doubao Seed 2.1 Pro、Seedream 5.5 / Seedance 2.5 及上线渠道、小云雀、红果 AI 剧、腾讯会议元宝笔记与 AI 小助手、飞书智能纪要/妙记、PPT Master、WorkBuddy 首任务、DeepSeek 价格结构、Peter 原话、Gamma 导出、Copilot 模板指南、OpenAI 快速入门、吴恩达短课，全部与讲稿一致或按官方页面校准；记录见 `docs/content/swiss_script_20261115/source_check_20261116.md`，关键事实登记 `docs/context/facts.json`。
- 唯一表述升级：第 25 页小云雀按官方手册改为「标称 Seedance 二点五首发体验产品」，source_map 同步；其余正文未动。

## 补充二：素材清单与 ppt-master 环境试运行

- 30 页界面素材清单 `docs/content/swiss_script_20261115/asset_checklist_20261116.md` 完成：逐页列画面需求、来源（已有/本机可制/官方可下/待用户）与上屏前核对要求；明确待用户项为 Codex 脱敏截图、表情包原件、黄仁勋照片来源、第 19 页本机版本核对。
- ppt-master 试运行：attribution_guard 通过（exit 0），workflows/routing.md 已读；扩 30 页路线为 Generate PPTX（Default），沿用三页样稿规范。未启动 30 页制作。

## 补充三：官方界面素材下载归档

- WorkBuddy 首个任务官方教程图 14 张已下载到 `assets/screenshots/20261116/workbuddy_first_task/`，来源登记 provenance.json；全部文件头与尺寸校验通过。本 Agent 会话模型不支持读图，画面内容待用户/主对话过目后上屏。
- 腾讯会议/飞书帮助页为动态渲染，正文图无法直接抓取；第 19 页素材以用户本机测试会截图为准。
- 素材清单状态已同步（第 15、19 行）。

## 补充四：逐页备注包与页时核对

- 生成 `docs/content/swiss_script_20261115/speaker_notes_per_page.json`：30 页纯正文备注（已去括号操作提示），供扩 30 页时直接写入 PPTX 讲者备注。
- 页时核对：全稿平均 3.13 字/秒（含翻页、指图、停顿），预算宽松；最紧第 30 页 4.19 字/秒。可选加料约 +1 分钟不破 48 分钟。修订说明第五节已更新，真人试讲时逐页计时即可。

## 补充五：30页扩稿任务书与黄仁勋照片

- 30 页扩稿任务书 `docs/content/swiss_script_20261115/build_brief_30p.md` 完成：输入文件、视觉规范、Generate PPTX（Default）路线、素材占位规则、未定项默认值、验收清单与时间分工，待用户确认开工。
- 黄仁勋引语补充 SEC 旁证（EDGAR FY2026 年报署名 Founder and CEO, May 2026）；官方新闻室 bios 页现列其为 Founder，署名以签署时身份为准，quote_sources 与 facts.json 已更新。
- 官方头像 1920×1920 已下载至 `assets/screenshots/20261116/nvidia_bio/`（官方 Download Headshot 端点），上屏前待用户确认。

## 补充六：用户自改版讲稿接收、润色与校对

- 用户 2026-11-16 凌晨手写新版讲稿 `自己修改版.md`，作为新一轮内容基准，已原样提交存档；表情包原件（微信收到，1280×1280）复制归档 `assets/company_meme/`。
- 按用户稿润色为 `speaker_script.md`：保留结构与口吻，修语病、补 MCP/Harness/Agent 空位、把幻觉科普备注改写成照读正文、补生图提示词示例。
- 校对记录 `script_factcheck_20261116.md`：11 项科普主张逐项核实全部成立（MiniMax H3、GPT-5.2/Claude Opus 4.5、冲击顺序绘画→IT→数学、幻觉分类与成因等），0 处事实错误；仅替换型号占位符与加措辞缓冲。
- 正文约 5,300 字、约 25–26 分钟；26 页分页草案与图标素材需求已列。旧 30 页分镜与备注包待分页确认后重做。






