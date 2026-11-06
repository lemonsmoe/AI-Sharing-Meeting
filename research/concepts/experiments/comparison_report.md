# 三组案例的运行方式与比较

全部输入/提示词/预设检查见protocol.md；本会话作答原文见session_outputs.md。这是真实当前模型作答加工具执行演示，不是隔离上下文的独立基准。

|案例|原始交付|改进交付|实际工具动作|发现与限制|
|---|---|---|---|---|
|E1报价|聊天段落建议|含税总价及交期表，文件交付|Python读取quote_input.json，计算并写quote_deliverable.md；另一个检查脚本读取quote_run.json核对|两版建议均正确，不能宣称准确率提升|
|E2会议|聊天纪要|已确认任务/待分工需求/未决事项三组交接单|模型生成structured_outputs.json；Python渲染meeting_deliverable.md|修正了初稿把未分工需求放进已确认行动表的问题；人工业务验收尚缺|
|E3制度|聊天答复|附依据、排除来源与例外的答复文件|模型选定来源并保存结构化结果；Python计算超额30元并渲染policy_deliverable.md|没有实现通用检索系统，不称RAG系统实测；正式版本选择由当前模型完成|

模型：当前会话，精确后端版本未暴露。代码执行：本机Python；日期2026-11-06。完整模型生成耗时未采集，脚本报告只记录脚本墙钟时间；未收费调用外部API，实际订阅分摊成本未知。未做人工基线计时。

人工修改：无用户人工编辑；Agent修订E2分组，保留原始答复不覆盖。错误重试：文档生成无；研究查询曾有一次JS引号语法错误，修复后重试，不属于案例模型错误。

复现命令（项目根目录）：
- python scripts/concepts/run_quote_workflow.py
- python scripts/concepts/check_quote_output.py
- python scripts/concepts/render_case_documents.py

缺口：两次独立模型执行尚未完成。当前可用工具没有独立文本推理接口；禁止隐藏subagent和新增聊天的任务边界继续遵守。重跑渲染器不能填补模型复测。可由主对话后续安排已有可见聊天或用户提供允许的独立测试入口；当前先继续公开研究，无需阻塞其他工作。
