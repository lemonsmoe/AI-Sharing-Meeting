# GitHub 迁移与新环境接续

目标仓库：https://github.com/lemonsmoe/AI-Sharing-Meeting.git 。此次用户明确授权迁移、提交与上传。首次核对远端为空，本地原本未初始化 Git；建立 main 分支，不改写远端历史。

## 同步范围

上传项目源码、参考材料、历版 PPT/视频/表格、研究与证据、讲稿、当前领域、讨论与决策、任务历史、迁移脚本及三个相关自定义 Skill 快照。

排除 `.context_runtime/`、`.codex/`、`node_modules/`、虚拟环境、下载的语音运行库、临时文件和凭据。保留历史成品并不改变用户否决质量的结论；不得自动恢复目标模式或 WPS 访问。

Git 不承载完整桌面聊天、账户凭据、全局个人记忆、插件缓存、Hook 信任及活动目标。`docs/context`、交接手册和研究记录是新环境可读取的项目记忆；`task_history.json` 是旧任务与操作日志的只读档案。

## 在新机器上操作

```bash
git clone https://github.com/lemonsmoe/AI-Sharing-Meeting.git
cd AI-Sharing-Meeting
python --version
```

需要 Python 3.11+ 和 Git。先在 Codex 中打开这个项目，建立一个由用户指定的新主对话，发送 `docs/handoff/new_environment_handoff.md` 的开场消息。不要在普通终端编造 CODEX_THREAD_ID。

```bash
python scripts/migration/bootstrap_context.py
python scripts/migration/bootstrap_context.py --apply
python scripts/context/task_store.py status
python scripts/context/discussion_store.py sync
python tools/project_skills/context-management/scripts/context_setup.py doctor --root .
```

第一个命令只预览。核对当前路径、真实新主对话 ID 和三个写入文件后再 apply。脚本：

- 备份原配置到 `.context_runtime/migration_backups/`，重绑当前克隆、当前 Python 与真实主对话 ID。
- 重新生成本机 Hook；不复制旧命令、不伪造信任或生命周期回执。
- 初始化空任务运行库；旧任务的状态、原负责人、范围和历史全部留在版本库档案中。新任务重新 create/claim，旧 review/accepted 不自动转为新对话的批准。
- 拒绝覆盖已绑定目录、已有 Hook、非空运行数据库或被改变的上下文脚本。已经运行过 status 但数据库完全空时可以迁移。

Hook 若在新客户端要求信任，由用户按新环境正常流程处理；doctor 仅是离线结构核验，不证明真实生命周期触发。新环境读完讨论才 ack，不导入旧已读游标。

`project.json` 和 `workflow_install.json` 会有预期的本机差异。它们包含运行路径与身份，**不要随日常内容提交推回覆盖其他机器**；显式暂存工作成果。新环境长期要成为唯一主环境时，再单独记录主环境变更。不要使用 skip-worktree 隐藏这些差异。

## 恢复制作依赖（需要继续开发时）

已有 PPTX/MP4/XLSX 可直接在合适应用中查看，不依赖制作运行库。读取上下文也没有第三方 Python 依赖。

|部分|要求与限制|
|---|---|
|上下文工具|Python 3.11+ 标准库；三个自定义 Skill 已有仓库副本|
|PPT/Excel 生成|新环境的 Codex Presentations/Spreadsheets 能力、Node 和 `@oai/artifact-tool`；通过新环境 load_workspace_dependencies 查询实际路径，不上传或从 npm 猜装内部运行库|
|网页检查|Playwright 及匹配浏览器；仅依赖路径配置不代表浏览器可用|
|视频旧实验|scripts/migration/requirements_video.txt 记录已有实验版本；Python 3.11 虚拟环境较易复现该历史组合|
|旧中文系统旁白|Windows WinRT 和对应音色；依赖清单保存在 scripts/video/build_delivery_bundle.py，非跨平台能力；用户已否决其听感，不能当默认新声音|
|原生 Office/WPS 验证|目标机器自行安装/授权，再核验；旧机器结果不能证明新机器兼容|
|字体|历史页及动画使用 Microsoft YaHei/Windows 字体；非 Windows 需明确替代字体并重新视觉检查|

旧媒体脚本有本机路径。获得新环境真实依赖目录后，在新克隆运行（尖括号参数替换为真实路径）：

```text
python scripts/migration/configure_media_runtime.py --node-modules "<实际 node_modules>" --presentation-skill "<实际 presentations Skill 目录>" --python "<实际 python>"
```

确认预览后加 `--apply`。只修改脚本里的运行库导入/路径，原件备份到 `.context_runtime/media_path_backups/`；不生成 PPT 或视频，不改历史证据和产物。版本 API、浏览器、中文字体、Office、编解码器仍须独立核验。路径重绑成功不等于完整生产环境验证。

## 后续同步

切换环境前先提交当前工作和讨论记录；任务历史可用 `python scripts/migration/export_context.py` 更新，只包含本机已有任务。脚本拒绝覆盖其他环境的首次迁移历史；新环境用 `--output docs/context/migration/task_history_new_env.json` 保存独立档案。跨环境的新增事件和讨论正常写入 `docs/context`。

已有本机改动先检查 `git status`；不要强制拉取、清理或覆盖。日常使用显式文件列表暂存，检查 `git diff --cached` 再提交推送。不要把迁移脚本当成每次 pull 后的初始化程序。

迁移检查记录见 `docs/context/migration/verification.md`。本次测试覆盖文件迁移与上下文接续，不代表用户已接受 PPT/视频质量或新设备已经跑通全部媒体工具。
