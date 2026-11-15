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


