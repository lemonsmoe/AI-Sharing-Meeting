"""生成项目规则和首次初始化文档；不覆盖已有项目知识。"""

import json

VERSION = "0.3.0"
BLOCK_START = "<!-- project_context_workflow:start -->"
BLOCK_END = "<!-- project_context_workflow:end -->"


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def agent_block():
    return f"""{BLOCK_START}
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
{BLOCK_END}
"""


def initial_documents(root, project_name, project_id, manager):
    manifest = dict(project_id=project_id, project_name=project_name,
                    context_root=root.as_posix(), manager_thread_id=manager,
                    manager_paths=["AGENTS.md", "docs/context/project.json",
                                   "docs/context/workflow_install.json",
                                   "docs/context/00_current/index.md",
                                   "docs/context/01_decisions", "docs/runbooks"],
                    workflow_version=VERSION, hook_acceptance="pending_user_trust_and_live_test")
    return {
        "docs/context/project.json": json_text(manifest),
        "docs/context/facts.json": json_text({"facts": []}),
        "docs/context/00_current/index.md": f"""# {project_name} 当前状态

- 当前阶段：协作工作流已初始化，项目目标及任务范围待补充。
- 主对话：`{manager}`，来源为初始化时明确指定。
- 未经确认的方案保留为候选；不要自动把初始化当作业务任务已批准。

阅读[领域状态](domains/docs_process.md)、[执行手册](../../runbooks/context_workflow.md)、[任务说明](../04_tasks/README.md)。
任务状态以 `python scripts/context/task_store.py status` 为准。
项目讨论执行 `python scripts/context/discussion_store.py sync`，按相关议题读取变化。
""",
        "docs/context/00_current/domains/docs_process.md": """---
domain: docs-process
current_status: initialized_pending_live_validation
last_event_id: null
last_event_time: null
last_recorded_at: null
owners: []
active_branches: []
---

# 协作状态

配置已经生成；Hook 信任和真实触发待验证。后续事实与任务由负责对话记录。
""",
        "docs/context/01_decisions/index.md": "# 有效决策索引\n\n尚无业务决策。记录经确认且持续约束项目的决定。\n",
        "docs/context/04_tasks/README.md": "# 任务视图\n\n此目录中的任务 Markdown 由 task_store.py 导出；以 SQLite 查询为准，不手工改派生文件。\n",
        "docs/context/05_discussions/README.md": discussion_readme(),
        "docs/runbooks/context_workflow.md": runbook(),
    }


def discussion_readme():
    return """# 项目讨论记忆

这里保存值得延续的项目讨论，不必等最终决定。各对话独立写记录，议题总结保留方案、理由、问题和来源。

- 原始记录：topics/<议题>/notes/<对话哈希>/note_<内容哈希>.md。
- 议题总结：topics/<议题>/summary.md，由模型整理，脚本检查版本、来源覆盖和类型。
- 进入或接续：运行 python scripts/context/discussion_store.py sync，读相关议题；pending 表示总结尚未吸收新记录，changed 表示尚未明确读过当前版本。实际读完再 ack。
- 写入：用 paths 查询 note_scope 和 summary_path，先 create/claim，再 record。packet 返回旧总结与新记录，模型生成总结 JSON 后 consolidate；finish 引用这些文件提交结果。
- 正常触发：当前对话记录重要讨论后，同轮整理总结。遗漏触发：discussion_hook 的 Stop 最多请求当前模型补做一轮，不需要用户重新调用 skill。失败保留 pending；后续相关对话补做。
- 不占用其他对话的总结认领，不超时夺权。记录候选不等于批准，不把模型建议写成用户决定。
- 没有定时后台模型；未提取的聊天仍可能遗漏。Hook 需用户信任，手工调用不算真实自动触发。

完整 JSON 格式和操作例子见 $context-management 的 references/discussion_memory.md。
"""


def runbook():
    return """# 项目协作上下文操作手册

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
"""
