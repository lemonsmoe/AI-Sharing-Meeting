# 讨论记忆：记录、整理、接续

## 什么时候触发

项目讨论出现新增方案、约束、问题、异议或取舍理由时，当前对话主动提取并 record；不要求用户每次提醒。包括 Agent 自己在本轮回答中新提出的项目建议：在回复结束前保存为 proposal，再整理议题，不能只读和整理旧记录。来源写明“本轮Agent建议”，不能冒充用户已确认。若整理后又产生重要新观点，应再记一条并重新整理。普通术语解释或重复内容不必记录。

正常在本轮结束前完成相关议题的 consolidate。若已有记录但遗漏整理，discussion_hook 的 Stop 请求当前模型补做一轮；同一 turn_id 最多一次，同一批记录也最多强制一次，stop_hook_active 时不重复，plan 模式不强制写入。整理范围被其他对话认领则不夺权。失败保留 pending；后续进入相关议题的对话先 sync，读取新记录后补做。用户要求停止时直接结束。未运行的对话不会被后台定时唤醒，此版本没有额外模型 API、独立守护程序或定时任务。

Hook 不读取完整聊天生成笔记，也不能发现所有未保存的重要想法。提取仍由当前对话模型完成。类型、来源和覆盖检查能防常见错误，不证明自然语言摘要绝对正确。

## 文件与任务

每个议题位于 `docs/context/05_discussions/topics/<topic>/`。`notes/<对话哈希>/note_<内容哈希>.md` 为独立记录，`summary.md` 为模型整理结果。记录含 JSON 形式的 YAML 前置信息和人可读正文，可用普通编辑器查看。按内容去重；补充或纠错应新增记录，不覆盖他人原记录。

先 `discussion_store.py paths --topic <snake_case>` 得到自己的 note_scope 和 summary_path。持久写入仍须真实对话 create/claim；可以同一个任务认领本对话 note_scope 和当前议题 summary_path。总结被占用时仅认领自己的 note_scope，先保存记录；不要认领整个讨论目录。读取无需认领。

纯讨论记录不必另写一份重复的事件和领域长总结，原记录本身就是来源证据；finish 引用记录及议题总结到 review。已确认的长期项目决定仍由主对话吸收进入决策层。领域与宏观状态的实施变更按原流程留事件。

## 操作入口

下文 python 指 Python 3.11+。命令中有空格的路径用本机 shell 正确引用；JSON 写到临时输入文件，避免把正文直接拼接成 shell 代码。

```powershell
python scripts/context/discussion_store.py sync
python scripts/context/discussion_store.py paths --topic platform_selection
python scripts/context/discussion_store.py record --task <已认领任务> --input <记录JSON路径>
python scripts/context/discussion_store.py packet --topic platform_selection
python scripts/context/discussion_store.py consolidate --task <已认领任务> --input <总结JSON路径>
python scripts/context/discussion_store.py sync --topic platform_selection
python scripts/context/discussion_store.py ack --topic platform_selection --revision <实际读完的版本>
```

record 输入示意，不把这些例子当作真实项目事实：

```json
{
  "topic": "platform_selection",
  "title": "实验平台选择",
  "abstract": "比较候选平台，尚未定型",
  "source_message": "本对话中对应消息位置或用户原话，不能伪造来源",
  "items": [
    {"kind": "proposal", "text": "考虑平台甲，原因是现有采集工具可能复用。"},
    {"kind": "question", "text": "平台甲是否支持所需触觉输入？"}
  ]
}
```

kind 可为 proposal、question、constraint、observation、objection、user_confirmed。最后一种必须附 evidence 为实际确认原话或依据；不是 Agent 自己推断。脚本取 CODEX_THREAD_ID，不支持命令参数假冒其他对话。

packet 返回当前 notes_revision、base_summary_revision、旧总结、新记录和 required_sources。由当前模型结合这些材料生成总结 JSON：保留 topic 和两个版本字段，填写 title、abstract，以及 points（每项含 kind、text、sources）。sources 使用 packet 提供的 `note_id#条目序号`，不能编造。每个来源条目必须被引用，或在 omitted 中逐条填写 source、reason，防止压缩时无声丢掉异议。

```json
{
  "topic": "platform_selection",
  "title": "实验平台选择讨论",
  "abstract": "仍有候选，等待接口验证",
  "notes_revision": "使用packet返回的值",
  "base_summary_revision": "使用packet返回的值",
  "points": [
    {"kind": "proposal", "text": "平台甲可以复用现有采集工具，但尚未选定。", "sources": ["使用真实note_id#0"]},
    {"kind": "question", "text": "仍需验证触觉输入支持。", "sources": ["使用真实note_id#1"]}
  ],
  "omitted": []
}
```

整理期间若有新记录或总结变化，提交会失败。重新 packet 合并，不用旧版本覆盖。kind 必须与引用条目一致，候选不能改成 user_confirmed；原来的异议和未决问题要继续保留。

## 接续与验收

sync 提供项目简报、议题入口、changed 和 pending。changed 代表与此对话明确 ack 的版本不同；pending 代表总结尚未吸收最新记录。先读相关 summary；pending 时还需 packet 或原记录。新内容不自动被标为已读。

验收覆盖三层：单元测试检查并发、过期写入、类型提升、来源覆盖和有界 Stop；新对话盲读检查实际能否接上讨论；真实 Hook 回执及追加整理回合检查自动触发。手工 handle 或调用脚本只算离线测试。

Git 可保存讨论文档版本；SQLite 保存已读标记和任务协调状态。初始化脚本不自动建 Git 仓库、不推送、不修改主对话身份。原始对话仍保留在 Codex；记忆文档保留来源，不替代全部原文。
