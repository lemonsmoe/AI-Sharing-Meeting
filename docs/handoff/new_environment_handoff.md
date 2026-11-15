# 新电脑主对话接续

更新于2026-11-15。仓库：https://github.com/lemonsmoe/AI-Sharing-Meeting.git 。用户本轮要求同步目前进度并在另一台电脑继续工作。

## 先读入口

- 可复制提示词：docs/handoff/continue_prompt_20261115.md
- 最新内容包：docs/content/popular_science_20261112/start_here.md
- 主对话审阅结论：docs/content/autonomous_20261111/review_result.md
- 当前索引：docs/context/00_current/index.md
- 分工：docs/planning/thread_registry.json
- 迁移步骤：docs/runbooks/github_migration.md

本文件覆盖旧版“所有生产暂停、Skill尚未选择”的说法。用户已恢复PPT和讲稿工作并选定PPT Master；视频继续暂缓。三页风格尚无用户认可记录，不能把技术通过当审美通过。

## 已有成果

1. Master三页修订版：slides/master_restart_20261109/master_preview_20261109/exports/master_preview_20261112_181441_native_charts_tables.pptx。SHA256：ac5fda8b326aed5e961e2486ab4e4983e120381316e482720e498c8d2ce25107。
2. 对应新版PowerPoint图在同项目native_validation_v2/slide_01.png至slide_03.png。原机3页、3备注、1张原生表格及标题/表格副本回存通过。edited_copy.pptx是故意修改的测试副本；native_validation是首版证据，不能代替新版。源SVG、设计规范、spec_lock、备注和检查都已保存。
3. 30页完整文字包：docs/content/popular_science_20261112/，含分镜、口语稿、来源、审阅清单。48分钟内容＋5分钟问答＋2分钟机动是预算，未真人计时。
4. Codex模拟办公任务有真实纪要、XLSX、输入和复核；多商业产品基准仍0次，不能冒充WorkBuddy/Copilot实测。
5. 项目Skill在tools/project_skills；Master实际使用的6.9.0源码归档在tools/vendor_packages，带完整许可及逐文件校验。当时未取得上游commit，归档固定本地实际使用源码，不声称上游提交固定。

## 已确认范围与缺口

分享2026-11-16，按接续时实际日期安排，不再使用已经过去的11月10/11检查点。全体部门及领导、约30页、少于1小时；科普介绍和拓宽知识面为主、教学为辅。提示词是主要方法，Skill要讲怎样找和用；会议纪要、PPT、办公Agent是主要场景。概念组件按职责和配合解释，不画线性淘汰链。降低AI味是小议题。

尚缺用户对三页及大纲的反馈、整套新PPTX与对应备注、本人跟做、计时排练、演示设备核验。旧V3和72秒视频创作质量被否决，保留作失败样本；本轮三页与文字仅阶段通过。

ChatGPT因登录失败由用户明确改为之后自己测试，不再催登录。WorkBuddy在线入口已找到但未登录或执行。WPS AI PPT入口曾经用户单独授权检查，会员显示过期，不等于证明不能生成或导出。价格和账号能力使用前再核。

公司环境来自用户描述：Office/WPS、飞书、微信、用友、自建知识库、GPU/ESXi/GitLab，不能宣称本项目已接入公司系统。长期希望培养PPT与视频创作能力，视频当前不恢复。

## 新电脑接续顺序

1. 建议克隆到与旧机不同的路径，如D:/code/AI-Sharing-Meeting，避免bootstrap把同路径判为已绑定。用真实新CODEX_THREAD_ID，不沿用旧身份。
2. 先按迁移手册运行python scripts/migration/bootstrap_context.py预览，核对后加--apply。已有Hook、非空数据库等状态不覆盖，不重置来绕过保护。
3. 再运行task_store.py status和discussion_store.py sync，读索引、内容领域、workshop_scope/office，实际读完再ack。历史任务留档，不恢复旧认领为新权限。
4. python scripts/migration/restore_ppt_master.py预览，再加--apply恢复源码；阅读恢复后的SKILL.md，按教程准备依赖、字体和Office。仅看现有PPTX和讲稿无需安装制作依赖。
5. 先展示三页新版与30页大纲，吸收用户反馈后扩整套。已有认可若在后续消息中给出，不重复确认；可继续不依赖回复的素材、内容核对和可逆准备。

## 记忆、聊天与权限

项目记忆在docs/context，任务历史在docs/context/migration/task_history.json，分工与产物在thread_registry.json。用户可在新电脑读取这些文件；Git不复制完整桌面聊天逐字历史、个人全局记忆、登录态、账号凭据或插件缓存。

旧聊天ID仅供追溯，迁移不自动恢复目标模式和Hook信任。用户偏好独立可见子聊天，不用隐藏subagent替代。需要并行时按既有授权建立新环境可见聊天，划清产物与写入范围；不要唤醒旧电脑暂停/阻塞目标。目标active只按真实工具回执报告。
