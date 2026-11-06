# 使用与边界

## 第一次使用

告诉 Agent：使用 `$context-management` 为当前项目建立协作上下文，项目目标是什么，并指定哪个真实对话作为主对话。Agent 调用 `context_setup.py init` 预览，再在授权范围内 `--apply`。用户无需手工准备 AGENTS.md、脚本、文档或数据库；Hook 新建或变化仍需在 Codex 中审阅信任。

初始化器不设置目标模式、不创建额外对话、不修改全局配置、不初始化 Git、不控制硬件。它不把当前对话自动设为主对话。版本0.3增加讨论记忆，三个事件各运行任务背景与讨论背景两个脚本；讨论 Stop 可以有界请求当前模型补做整理，详细格式见 discussion_memory.md。

## 日常例子

```powershell
python scripts/context/task_store.py status
python scripts/context/task_store.py create --title "实现数据导出" --domain data --write-path src/export.py --write-path docs/context/00_current/domains/data.md --write-path docs/context/02_events/2026/11/evt_export.md --acceptance "导出文件可重新读取，记录验证结果"
python scripts/context/task_store.py claim <查询到的任务编号>
python scripts/context/task_store.py finish <任务编号> --result "导出实现并验证" --evidence "事件与测试结果路径"
```

只有主对话验收；主对话变更需要用户明确指定后单独迁移，不通过重新初始化偷换身份。SQLite 内部操作历史不等于上下文事件；Markdown 任务文件是派生视图，不手工修改。当前状态、决定和事件存于 `docs/context/`，原始聊天不在其中。

同机多对话必须共享同一上下文根。多 worktree 的 task_store 命令加 `--root <主上下文根>`；Hook 也指向该主根。不要在另一 worktree 再初始化独立认领数据库来协调同一项目。多电脑、网络盘并发和团队权限控制不在此版本支持范围。

## 自检与升级

`context_setup.py doctor --root ...` 是只读检查，返回 errors、warnings、任务数、回执数及安装版本。doctor 不执行 Hook、不修改信任记录、不测试模型是否真正收到提示。配置存在与回执存在也不能证明所有生命周期路径已验收。

`init` 默认仅预览，重复 `--apply` 应没有内容变化。升级保留业务文档、数据库和外部 Hook；手工修改过的受管代码或 AGENTS 区块会报告冲突。原件备份在 `.context_runtime/setup_backups/<批次>/`。发生中途失败，先查看备份和清单再恢复，不能使用强制覆盖来掩盖部分写入。未由本技能创建的旧脚本若内容不同，需先审查迁移，初始化器不会擅自接管。

安装记录 `docs/context/workflow_install.json` 描述受管代码哈希和 Hook 定义，不含聊天、传感器数据或凭据。项目运行时和备份默认忽略 Git；任务数据库需要另行备份，Markdown 任务视图不能完整替代它。数据库在线备份应使用 SQLite backup API，不能直接云同步活动数据库。

Windows Hook 使用 PowerShell EncodedCommand，避免中文、空格和 `$` 等路径字符被当成代码。编码内容仅为调用预览中列出的 Python 和 context_hook.py；可用 Python 的 base64.b64decode(...).decode("utf-16le") 或 PowerShell 解码检查，不从网络下载或执行内容。

应用工具代发消息在本机试点未触发 UserPromptSubmit；接续任务显式查询 status。压缩恢复和同会话自动修订刷新未完成真实验收，不把模板支持的事件名当成实测结论。
