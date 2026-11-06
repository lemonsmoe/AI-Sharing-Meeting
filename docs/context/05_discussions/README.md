# 项目讨论记忆

这里保存值得延续的项目讨论，不必等最终决定。各对话独立写记录，议题总结保留方案、理由、问题和来源。

- 原始记录：topics/<议题>/notes/<对话哈希>/note_<内容哈希>.md。
- 议题总结：topics/<议题>/summary.md，由模型整理，脚本检查版本、来源覆盖和类型。
- 进入或接续：运行 python scripts/context/discussion_store.py sync，读相关议题；pending 表示总结尚未吸收新记录，changed 表示尚未明确读过当前版本。实际读完再 ack。
- 写入：用 paths 查询 note_scope 和 summary_path，先 create/claim，再 record。packet 返回旧总结与新记录，模型生成总结 JSON 后 consolidate；finish 引用这些文件提交结果。
- 正常触发：当前对话记录重要讨论后，同轮整理总结。遗漏触发：discussion_hook 的 Stop 最多请求当前模型补做一轮，不需要用户重新调用 skill。失败保留 pending；后续相关对话补做。
- 不占用其他对话的总结认领，不超时夺权。记录候选不等于批准，不把模型建议写成用户决定。
- 没有定时后台模型；未提取的聊天仍可能遗漏。Hook 需用户信任，手工调用不算真实自动触发。

完整 JSON 格式和操作例子见 $context-management 的 references/discussion_memory.md。
