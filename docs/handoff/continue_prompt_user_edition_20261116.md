# 接续提示｜用户自改版全套交付后（2026-11-16 凌晨）

适用于同一本机 `D:\03_Code\03_Company\AI-Sharing-Meeting` 换新 Agent 优化。晚于 `continue_prompt_swiss_20261115.md`；旧 30 页结构与旧三页样稿不再是最新版，最新成果以本文为准。

## 给新 Agent 的提示词

你是本项目的新接续 Agent。当前最新成果是「用户自改版」29 页全套 PPT，已交付并通过机械验证，现交给你做优化。先读 AGENTS.md、`docs/handoff/continue_prompt_swiss_20261115.md`（背景）、本文，以及 `docs/content/swiss_script_20261115/` 下最新文件。使用自己的真实会话身份执行 task_store.py status 与 discussion_store.py sync，读 content 领域与 workshop_scope 议题后再 ack；持久修改先 create/claim。不要冒用原主对话身份（Codex 01a1b28a…）或上一个 Agent 身份（DSH session-5bed8c8e-…），不自动修改主对话绑定或重启旧目标。

## 最新版在哪里

- **成品 PPTX**：`slides/projects/user_edition_ppt169_20261116/exports/user_edition_20261116.pptx`（29 页、29/29 讲者备注、SHA256 C5232044…）
- **逐页预览**：`slides/projects/user_edition_ppt169_20261116/preview/`（29 张 PNG，PowerPoint 12.0 渲染）
- **SVG 源页**：`slides/projects/user_edition_ppt169_20261116/svg_output/`（P01–P29，改这里再重导出）
- **讲稿**：`docs/content/swiss_script_20261115/speaker_script.md`（用户自改版润色校对稿，内容权威）
- **分镜**：`docs/content/swiss_script_20261115/outline_user_edition.md`（29 页、1,970 秒）
- **备注包**：`docs/content/swiss_script_20261115/speaker_notes_per_page.json`（与 notes/total.md 同步）
- **验证**：`slides/projects/user_edition_ppt169_20261116/verification.json`

## 已验证

SVG 质量检查 exit 0（0 错误）；导出 postflight passed；29/29 备注写入；本机 PowerPoint 12.0 逐页渲染 29/29 成功；副本编辑标题→保存→重开持久化通过。视觉逐页终审尚未由用户完成（上一 Agent 会话模型不支持读图）。

## 修改与重新导出流程

1. 改 `svg_output/PXX.svg`（配色：米白 #F6F3EC、黑 #171715、红 #C50000、微软雅黑；字号锚已登记 spec_lock）。
2. 重跑：`python scripts/svg_quality_checker.py <project> --quick-generate --canonical-authoring --stage final --json`（用 `.context_runtime/ppt_master_env/Scripts/python.exe`，SKILL_DIR 的绝对路径展开）。
3. 改备注：先改 `speaker_notes_per_page.json` 与 `notes/total.md`，跑 `scripts/total_md_split.py <project>`。
4. 重导出：`python scripts/svg_to_pptx.py <project> --quick-generate --with-notes -o exports/user_edition_20261116.pptx`。
5. 渲染检查：`research/slides/swiss_preview_20261115/render_powerpoint.ps1`（PowerShell 执行策略需 Bypass）。

## 待优化与边界

- 用户尚未逐页视觉终审；三处截图占位框（P07 豆包界面、P17 Skill 文件夹、P21 Codex 桌面端）由用户后补替换。
- 已知非阻塞项：检查器 warning 为 ungrouped 顶层元素与 <5% 轻微文本溢出（P21/P24 已修，其余为提示级）。
- 边界：视频制作保持暂缓；结构、页序或公司案例改动先与用户讨论；官方素材注明来源、不冒充实测；Git 提交沿用本分支 `task/001-script-grounding`，本机绑定 `docs/context/project.json` 与 `docs/context/workflow_install.json` 保持不提交；推送需用户授权。

## 本机环境

- `.context_runtime/ppt_master_env/Scripts/python.exe`（Python 3.12.13，无 pip，勿装包或改 ComfyUI 环境）；PPT Master 6.9.0 源码 `.context_runtime/ppt_skill_candidates/ppt_master`，attribution_guard 通过。
- context 脚本用该 Python；PowerShell 中文输出前设 `$env:PYTHONIOENCODING='utf-8'`。
