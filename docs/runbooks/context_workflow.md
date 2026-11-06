# 项目协作上下文操作手册

## 开始与认领

先 status，读当前索引、相关领域和需要的决策。纯解释只读即可；持久修改前 create 声明验收标准及所有写入路径，再 claim。身份使用真实 CODEX_THREAD_ID。重叠范围被拒绝时等原责任人释放，不绕过工具写文件。

主对话 ID 见 docs/context/project.json；新项目显式指定，不能把新开的工作对话自动注册为主对话。只有主对话可验收任务和维护全局索引、决策索引及手册。

## 完成与记忆

实际子任务完成后：追加 docs/context/02_events/YYYY/MM/ 中的事件，更新相关领域，再 finish --result ... --evidence ... 到 review。主对话复核后 review --accept。事件包含时间、责任、状态、依据与相关路径；领域记录最新吸收事件和核验依据。阶段交接才建立 handoff。建议、已确认、已实施、已验证必须区分。

项目构思中的候选、约束、疑问和异议由当前 Agent 主动提取到独立讨论记录，同轮整理议题总结；不用等最终决定。使用 discussion_store.py sync/paths/record/packet/consolidate/ack，详细格式见 $context-management 的 references/discussion_memory.md。持久修改仍先认领，来源和状态不能伪造。

讨论文件在 docs/context/05_discussions/topics；各对话记录按目录隔离，summary.md 为整理结果。未吸收的新记录显示 pending，未读变化显示 changed。来源逐条引用，无法纳入则说明原因。原始聊天不自动复制。

discussion_hook 的 Stop 仅在本对话已有待整理记录且总结未被其他对话占用时请求模型补做一轮，同一 turn_id 最多一次；失败保留 pending。没有定时守护程序，未运行的对话不会自动醒来。未被提取的重要聊天仍可能遗漏，不保证自然语言摘要绝对正确。不自动完成或释放任务。

## 核验与 Hook

只核验当前任务依赖；稳定结论按来源变化检查，设备与风险操作临执行前复核。facts.json 可登记来源、last_verified_at、evidence 和 recheck_when，不能无依据刷新时间戳。

SessionStart 和 UserPromptSubmit 注入短背景，任务 Stop 提醒，讨论 Stop 可有界请求继续整理。新建或变更 Hook 需用户审阅信任。配置存在不等于对话已加载；查看 .context_runtime/hook_receipts 和 discussion_hook_receipts 并核对模型实际收到的提示。手工调用脚本只能算离线测试。工具代发消息不保证触发 UserPromptSubmit，必须显式 status 和 discussion_store.py sync。压缩和恢复各路径须单独验证。

## 并发、备份和升级

SQLite 认领是协作机制，不是系统权限。读取无需认领；跨对话不要同时覆盖相同文件。多 worktree 使用同一 --root，不为同一项目复制独立认领数据库。SQLite 只支持此处的同机协作，不部署在同步盘或网络盘当作团队服务。

任务状态在 .context_runtime/tasks.sqlite3，任务 Markdown 仅是派生视图。数据库另行备份，在线时用 SQLite backup API。原始聊天由 Codex 保存。故障时暂停持久写入，明确报告；不自动夺取责任。

使用 $context-management 的 doctor 只读自检，init 默认预览，--apply 才执行。升级保留已有知识和外部 Hook，修改过的受管代码停止并报告冲突；原件备份到 .context_runtime/setup_backups。无需每轮初始化或人工提醒更新。离线检查不代表全部生命周期或硬件验收。
