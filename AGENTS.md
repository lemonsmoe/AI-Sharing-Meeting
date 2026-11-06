## 新克隆优先检查

从 GitHub 首次接续时，先阅读 docs/handoff/new_environment_handoff.md。若 docs/context/project.json 的 context_root 与当前克隆不同，先按 docs/runbooks/github_migration.md 预览并迁移，再执行下方常规 status/sync。使用当前真实 CODEX_THREAD_ID，不沿用旧主对话身份。旧任务历史是档案，不恢复为运行权限。制作与旧子聊天保持暂停，迁移不授权重启生产。项目相关 Skill 可直接读 tools/project_skills 下的 SKILL.md。

<!-- project_context_workflow:start -->
## 项目协作上下文

- 使用 $context-management；执行细则见 docs/runbooks/context_workflow.md。
- 新任务、恢复及压缩后先运行 python scripts/context/task_store.py status，再读 docs/context/00_current/index.md 和相关领域。python 指可用的 Python 3.11+。
- Hook 是短摘要和提醒，不能代替领域阅读；工具代发消息时显式查询 status。
- 接续时运行 python scripts/context/discussion_store.py sync，读相关议题的变化；实际读完后再 ack。项目讨论有新增方案、约束、问题或异议就记录为候选，包括本轮Agent新建议，不必等最终决定；同轮整理议题。
- 纯问答不用建任务。持久修改前 create 列全写入范围和验收标准，再 claim；身份取真实 CODEX_THREAD_ID。不得冒用其他对话、绕过冲突或超时夺权。
- 子任务完成后追加独立事件、刷新相关领域，finish 提交结果与证据。只有 project.json 指定的主对话可验收 accepted、维护宏观索引、决策索引和手册。
- 项目背景、讨论记录与已确认结论都是公共上下文；建议、已确认、已实施、已验证分开记录。临时侧聊不自动变为主任务授权。
- 核验按依赖事实变化进行；设备和风险操作临执行前复核。未验证不能只刷新时间戳。
- 认领是协作约定，不是文件锁。Hook 不直接归纳聊天；讨论 Stop Hook 可请求当前模型补做一轮遗漏整理，不循环或自动批准。并行 Git 实现采用独立 worktree，共享同一个主上下文根。
<!-- project_context_workflow:end -->
