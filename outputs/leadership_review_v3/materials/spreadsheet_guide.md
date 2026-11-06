# 会议文件到可编辑Excel

打开 [原始会议记录](file_demo/input/meeting_notes.txt)、[会后补充](file_demo/input/follow_up.txt)，再看 [会议行动表](meeting_actions.xlsx)。材料为模拟会议，未接入公司系统。

现场用约2分钟展示：给材料 → 指定交付字段 → 打开结果 → 对照原文。不要把生成器代码讲成普通用户必须掌握的步骤。

可复制的要求：读取两份文件，交付可编辑Excel；分开行动、已确认变更和未决信息；给来源编号；未知负责人和日期保持空白并提示；保留原件，不发送消息。

本表包含2个行动项、4条决定或未决信息。测试报告为11月9日18:00，演示改到11月12日；采购尚未批准，网络只是未确认的假设。填写负责人不代表期限也已确定。

V3副本将两个日期单元格改为Excel日期序号，沿用当地钟表时间。2026-11-06在Microsoft Excel 16.0读取显示、修改独立副本文字并保存重开通过；原文件不变。尚需在分享现场设备检查，未宣称WPS已测。

本次由Codex读取和整理材料，文件工具生成工作簿；不代表WorkBuddy、Copilot或WPS AI实测。项目生成源码保留在 tutorials/office/spreadsheet_demo 与 scripts/slides/review_deck_v3；本包供审阅，不包含完整运行环境。
