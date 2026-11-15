# Swiss 修订版接续提示｜2026-11-15 晚

适用于当前本机 `D:\03_Code\03_Company\AI-Sharing-Meeting` 切换 Agent。此入口晚于 `continue_prompt_20261115.md`；旧入口中指向 11 月 12 日样稿和文字包的内容已被本轮更新。请沿用现有成果推进细节，不重新规划，也不要把旧稿当最新版。

## 可直接交给新 Agent 的提示词

你是本项目的新接续 Agent，请在当前仓库接着推进企业 AI 分享会的细节。先读 AGENTS.md、tools/project_skills/context-management/SKILL.md、docs/context/00_current/index.md，以及本文。用自己的真实 CODEX_THREAD_ID 执行 task_store.py status 和 discussion_store.py sync，阅读 content 领域与 workshop_scope、office 相关讨论后再 ack。持久修改先 create/claim，列明范围。不要冒用原主对话身份，不自动修改主对话绑定或重启旧目标、旧聊天。当前是同机接续，不重复 bootstrap；只有实际换了电脑且 context_root 不匹配时，才按迁移手册预览迁移，不能覆盖已有本机状态。

用户要在 2026-11-16 下午面向全体部门及领导分享，约 30 页、少于 1 小时。最低交付是可编辑 PPTX、逐页讲者备注和能照读的中文讲稿。用户从 11 月 15 日晚开始的总投入约 6–7 小时，还要留睡眠及早上 9 点上班时间；接续不能把这个预算重新起算。视频制作继续暂缓。

先实际打开下面最新版，查看全部三张预览，读分镜和讲稿，不只读总结：

1. `slides/swiss_preview_20261115/exports/swiss_preview_20261115_231045.pptx`
2. `slides/swiss_preview_20261115/preview/slide_01.png`、`slide_02.png`、`slide_03.png`
3. `docs/content/swiss_script_20261115/outline.md`、`speaker_script.md`、`source_map.md`、`case_options.md`
4. `docs/content/swiss_revision_20261115/confirmed_brief.md`、`review_result.md`、`quote_sources.md`
5. 用户大纲快照 `docs/content/local_resume_20261115/user_outline_snapshot.md`，原件 `D:\04 Note\Yancey's_Knowledge_Base\000 New\公司分享.md`。原件有新修改时以最新用户内容为准。

已确认的内容顺序：成果 → 简单原理 → 提示词 → 办公 Agent / Skill → 会议 / PPT → 生图视频 → 费用与展望。30 页照读稿已经写好，主讲预算 48 分钟，含问答与机动 58 分钟，未真人试讲。新版整套 30 页 PPTX 尚未制作。

用户已选 PPT Master。视觉以公司模板 `slides/赛感PPT优化丰富版本.pptx` 为底，更多参考 `assets/references/swiss_grid_systems.pptx` 的组件、网格与留白。黑、米白、红；统一字体，最多两三档字号；少文字、多真实图片和界面，内容接地气。不要左下角固定小字标题。旧三页字体层级多、文字密、抽象的问题已被否决。

最新三页对应全稿第 1、8、13 页，不是连续三页。已在本机 PowerPoint 渲染，逐页查看并修订；原生文字、三页备注、字体主题及标题副本编辑回存已验证。字号为 18/24/43.5 pt，字体微软雅黑。封面嵌套的样稿截图与人物照片是图片，内部文字不宣称原生可编辑。三页通过技术和主对话阶段审阅，用户尚未给出这版视觉认可。若当前新消息已有用户视觉反馈，按新反馈执行，不重复确认；否则先接上视觉反馈，再扩整套。其余措辞精修、来源核对、截图素材整理、可逆的小范围修订可以独立推进。

案例边界：本次 PPT 制作、公司 AI 表情包已获用户认可；表情包原件用户稍后补。办公案例仍需讨论，候选在 case_options.md，不擅自认定为实际公司案例。ChatGPT 实测由用户后补，不再卡登录，不把官方说明、模拟资料或 Codex 产物说成其他产品已实测。

人物页采用照片在左、英文原话在上、中文自译在下。具体人物由 Agent 据内容和原始来源判断，不只照用户举例选。当前第 13 页为 Peter Steinberger；第 30 页文字候选为黄仁勋。引语原文、语境和照片来源在 quote_sources.md；不要把愿景写成已实现能力，不编名言。黄仁勋照片尚待选取。

接续后先给简短核对结果，然后实际推进最有价值的细节。保留已经确认的顺序和设计要求，改动结构或具体公司案例先与用户商量。优先清楚、具体、看得懂的真实材料，不为增加概念而堆文字；每次改图都实际看图验收。需要并行时优先用户可查看的可见子聊天，不自动恢复历史聊天。完成后留下改动、验证与剩余缺口。

## 本机环境与重现

- 已恢复 PPT Master 源码：`.context_runtime/ppt_skill_candidates/ppt_master`。读取其 SKILL.md 和对应工作流后使用，不重新选择另一套生成路线。
- 本机隔离环境：`.context_runtime/ppt_master_env/Scripts/python.exe`，Python 3.12.13。依赖已经配置；不要改 ComfyUI 环境。
- context 脚本使用上述 Python 3.11+ 即可。PowerShell 中文输出前设置 `$env:PYTHONIOENCODING='utf-8'`。
- 渲染脚本：`research/slides/swiss_preview_20261115/render_powerpoint.ps1`；检查脚本与证据：同目录 `verify_pptx.py`、`verification.json`。本机 PowerPoint 12.0 已用于三页原生渲染与编辑回存。Master 实时预览受套接字权限限制，采用 PowerPoint PNG 检查。
- `.context_runtime/` 属本机运行环境，不随 Git 提交。换电脑时用 `tools/vendor_packages/README.md` 和迁移手册恢复，不能只复制 Windows venv。
- `docs/context/project.json` 和 `workflow_install.json` 的本机绑定差异刻意保留未提交；同机新 Agent 应保留。Git 中的历史绑定不应覆盖当前本机文件。
- 两条新制作聊天本轮都已 completed/idle；task_store 中 accepted 代表阶段审阅，不能当用户视觉认可。当前主对话绑定仍是原主对话，执行 Agent 不擅自更换。
- 本次仅本地 Git 保存，未推送。完整提交文件列表见相邻 `swiss_handoff_manifest_20261115.json`；关键交付 SHA256 也在其中。

## 余下交付

用户视觉反馈与办公案例选择 → 全部 30 页可编辑 PPTX → 备注和照读稿逐页对齐 → 全页渲染检查 → 真人计时、现场设备打开。中间穿插真实界面/公司表情包原件，未实测处保留准确状态。不要把已有旧版整套 PPT 当作本轮新稿交差。
