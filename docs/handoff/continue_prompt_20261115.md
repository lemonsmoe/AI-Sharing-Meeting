# 新Agent接续提示词

将下面内容发给新电脑中打开本仓库的Codex聊天：

```text
你是本项目在新电脑上的主对话，请接续企业AI分享会工作，不从零重新规划。

先读AGENTS.md、docs/handoff/new_environment_handoff.md、docs/context/00_current/index.md，以及tools/project_skills/context-management/SKILL.md。我授权迁移到本环境；使用你真实的CODEX_THREAD_ID，按docs/runbooks/github_migration.md预览并安全应用bootstrap_context.py，不冒用旧身份、不覆盖已有本机运行状态。之后执行status/sync，读内容领域、workshop_scope和office讨论后再ack。

已选PPT Master。三页修订版是slides/master_restart_20261109/master_preview_20261109/exports/master_preview_20261112_181441_native_charts_tables.pptx，正确预览在native_validation_v2。30页完整文字包在docs/content/popular_science_20261112/start_here.md。先读docs/content/autonomous_20261111/review_result.md，实际看三页，读分镜与讲稿。Master源码用scripts/migration/restore_ppt_master.py预览后加--apply恢复，依赖按迁移手册准备。

分享定于2026年11月16日，请按实际日期安排。全体部门及领导，约30页、少于1小时，科普工具介绍为主、教学为辅，提示词与Skill用法为重点。视频暂缓；旧V3质量被否决，不默认复用。三页已过技术检查，尚没有我认可风格的记录：先把样稿和大纲给我看，吸收反馈后扩成整套可编辑PPTX、逐页备注和讲稿。如果我后续已给认可，就直接继续，不重复确认。其余素材核对、缺口整理和可逆准备可并行完成。

ChatGPT实测由我之后单独补，不再卡登录。未真实执行的工具标为待验证，不用Codex产物冒充。48分钟只是预算，整稿后安排本人跟做、计时排练和现场文件检查。

我偏好可以单独查看和干预的可见子聊天，需要并行时按项目规范拆分；旧聊天和目标状态只作历史，不自动续跑。先给简短接续检查结果和最关键的下一步，然后实际推进，只在确需我选择、登录或提供素材时叫我。
```
