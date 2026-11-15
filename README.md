# 企业 AI 效率分享会

准备 2026-11-16 面向全体同事与领导的分享，约 30 页、少于 1 小时；以提示词工程和 Agent 协作为重点，覆盖会议纪要、PPT、调研、文档、表格与写作。希望在 11-10 前形成领导可审阅内容，并沉淀长期的视频与内容创作流程。

**2026-11-15同步状态：用户已恢复PPT与讲稿工作，选用PPT Master；三页修订版和30页完整文字稿已交。用户视觉认可、整套新PPT与排练仍待。视频暂缓，旧V3及72秒样片保留为失败样本，技术检查不等于用户质量认可。**

最新成果：[三页PPTX](slides/master_restart_20261109/master_preview_20261109/exports/master_preview_20261112_181441_native_charts_tables.pptx)、[30页大纲与讲稿](docs/content/popular_science_20261112/start_here.md)、[新Agent提示词](docs/handoff/continue_prompt_20261115.md)。Master源码快照及恢复说明在[tools/vendor_packages](tools/vendor_packages/README.md)。

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
