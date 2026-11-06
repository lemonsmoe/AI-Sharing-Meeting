# 新环境主对话接续

此文件是 GitHub 迁移后的入口，优先于旧 main_chat_handoff.md 的首次初始化提示。迁移目标：https://github.com/lemonsmoe/AI-Sharing-Meeting.git 。

## 可以直接发送给新聊天

> 请作为这个项目在新环境的主对话，先读 AGENTS.md、README.md、docs/handoff/new_environment_handoff.md、docs/context/00_current/index.md 和 docs/content/quality_reset_discussion.md。使用仓库内 tools/project_skills/context-management/SKILL.md。用户已授权迁移到本环境，以你真实的 CODEX_THREAD_ID 重绑新克隆，先预览 scripts/migration/bootstrap_context.py，再按迁移手册执行。已有本机状态时不要覆盖。生产与所有旧子聊天仍暂停；先理解质量否决、用户目标和未决优化方案，不自动恢复生产、不继续 WPS 访问、不重新问受众/日期等已确认问题。完成接续后与我讨论下一步。

## 必须保留的项目记忆

- 分享 2026-11-16；希望 11-10 前领导可审阅，原内部目标 11-09 晚。全体部门及领导，约 30 页，少于 1 小时。
- 提示词工程和与 Agent 协作为重点。覆盖会议纪要、PPT 制作过程展示、调研、整理文档/表格、写作；Skill、记忆库、Hook 浅讲。Prompt、MCP、Skill、Agent、Harness 是用户的粗略概括，需要准确解释，不按线性替代关系生搬。
- 用户希望培养 UP 主、剪辑、高质量 PPT 和 AI 讲解视频能力。此次产物用于建立长期工作方式。减少 AI 味只是小议题，不能取代整体目标。
- 公司使用 Office/WPS、飞书、微信、用友；有用户描述的自建知识库、GPU/ESXi/GitLab。具体配置未实地验证。先讲前沿主流与适用场景，再考虑价格和平替。
- 用户希望由 Agent 先研究、列案例菜单、执行验证；不要求用户先写示例或想办公任务。只在确需素材、账号、付费或决定时介入。
- 用户指定参考文章及相关视频：https://ploto.me/posts/how-i-made-a-long-video-with-ai/ 。已有文章阅读记录，不得冒充已看完配套原片。
- 多 Agent 指用户可单独查看和干预的可见 Codex 聊天；不要用隐藏 subagent 代替。旧聊天 ID 在 docs/planning/thread_registry.json，仅是原环境历史，迁移不会重建这些聊天或目标模式。

## 最新裁决优先于旧检查通过记录

用户已完整看过 72 秒样片，反馈动画不连贯、僵硬、像播放 PPT，机械音，视觉和内容差、不知在讲什么。PPT 排版混乱、无趣、色块堆积。**两者创作质量未通过，不是等待首次试听，也不是只需微调。**

所有生产聊天与主目标已暂停；WPS 查看已被用户停止。用户要求先讨论优化。旧文件、代码、技术 QA、来源研究仍保留，不能因此继续扩稿。

待讨论建议：拆解参考原片 → 15—30 秒局部试做与声音比较 → 3 页连续 PPT 代表页 → 用户认可后再扩大。候选 Skill 初查不等于选型成功，未获准安装或启动试做。详见质量返工讨论。

## 跨环境接续顺序

1. 按 docs/runbooks/github_migration.md 预览并重绑克隆，使用新主对话真实身份。仓库内 Skill 可直接读取，无需先覆盖本机全局 Skill。
2. 运行 task_store.py status 和 discussion_store.py sync，读相关领域及讨论；读完才 ack。新任务运行库为空是设计结果，旧任务完整历史见 docs/context/migration/task_history.json 与 docs/context/04_tasks。
3. docs/context/project.json 与 workflow_install.json 中原始路径属于迁移基线；bootstrap 在新克隆本地重写它们。旧聊天、已读游标、信任状态及目标模式不搬运。
4. 汇报已读状态和待讨论方案。得到新的生产指令后，再建任务、认领范围并推进；不要因迁移成功默认重新开目标模式。

Git 可同步文件与项目记忆，无法同步账户凭据、桌面聊天的完整运行状态、个人全局记忆库或插件安装。媒体运行库需要新环境自行获取，历史代码不保证跨版本直接运行。
