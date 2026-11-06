# 企业 AI 效率分享会

准备 2026-11-16 面向全体同事与领导的分享，约 30 页、少于 1 小时；以提示词工程和 Agent 协作为重点，覆盖会议纪要、PPT、调研、文档、表格与写作。希望在 11-10 前形成领导可审阅内容，并沉淀长期的视频与内容创作流程。

**当前生产暂停。用户已否决现有 72 秒视频的质量，对 PPT 的排版和内容不满意。V3、样片及检查记录保留作失败样本和可复用材料；技术检查通过不代表作品通过用户验收。迁移不会恢复生产或 WPS 访问。**

## 接续入口

1. [新环境交接](docs/handoff/new_environment_handoff.md)：可直接交给新主对话。
2. [当前状态](docs/context/00_current/index.md)与[质量返工讨论](docs/content/quality_reset_discussion.md)：先理解最新裁决。
3. [GitHub 迁移手册](docs/runbooks/github_migration.md)：克隆、重绑身份/Hook、恢复依赖及同步范围。
4. [讨论总结](docs/context/05_discussions/topics/workshop_scope/summary.md)：已确认范围、候选方案及历史理由。

```bash
git clone https://github.com/lemonsmoe/AI-Sharing-Meeting.git
cd AI-Sharing-Meeting
```

在新 Codex 主对话中阅读交接后，先运行 `python scripts/migration/bootstrap_context.py` 预览，核对后加 `--apply`。迁移使用 Python 3.11+ 标准库；不要把旧主对话 ID 填到新环境。若当前目录已经绑定，则直接按上下文手册接续，不重复初始化。

## 内容与目录

|目录|内容|
|---|---|
|docs/context|项目记忆：当前领域、决策、事件、交接、讨论、任务历史|
|docs/content、docs/planning|大纲、讲稿、内容源、范围和质量反馈|
|research|来源台账、阅读记录、实测、反证及研究门槛|
|tutorials|办公教程与示例材料|
|assets、slides、videos、outputs|原始参考、模板、历次 PPT/视频/表格与产物|
|scripts|上下文工具与原有制作脚本；migration 为迁移工具|
|tools/project_skills|三个项目相关自定义 Skill 的可审阅快照|

旧稿入口为 [V3 审阅页](outputs/leadership_review_v3/start_here.html)，不是当前获准交付版本。仓库不包含账号凭据、个人全局记忆、Codex 插件缓存、node_modules、原环境 Hook 配置及运行数据库。
