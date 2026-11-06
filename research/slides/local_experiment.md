# 本地四页样例实验记录

2026-11-06，候选路线：Artifact Tool本地可编辑生成。不是Copilot/Gamma/WPS云端产品实测。

输入：first_round.md的4页模拟周报内容。脚本scripts/slides/build_sample.mjs保存完整文本和图表数据，run_01、run_02为两次独立进程执行，输出各自保存，execution.json记录执行与渲染耗时。此为确定性脚本复跑，不代表两次独立模型生成质量。无人工计时基线，尚不能计算节省时间。

会话版本document_015d47ce-f214-403e-a9dd-eba95ade10fd已逐页渲染目检：4页完整、中文可读、无可见遮挡；第3页首次图表标注偏小，修订为24px后重新检查。图表数据甲组8/2、乙组6/4，与输入一致，没有补造延期原因。

本地run_03增加讲者备注。源文件存在正文文本框和原生图表，不是全页图片。尚未完成目标软件内改数据/保存/重开。

失败记录：
- 会话render返回Blob，直接emitImage不支持；改为bytes+mimeType后成功。
- chart.textStyle不接受fontFamily字段；已按接口移除该字段并调大字号。
- 首次Python编辑遇GBK解码，改显式UTF-8成功。
- finalizer在materializeLiteralChartWorkbooks阶段出现WinError 5，临时文件替换candidate.pptx失败。尚未宣称通过最终检查。

交付状态：slides/experiments/run_03/sample_draft.pptx为待校验草稿，非最终领导审阅稿。下一步定位工作簿嵌入错误，校验PPTX并补充备注和兼容边界，再完成三路线研究对比。

更新：硬链接权限问题已由授权执行解决，运行库路径补齐。finalizer于本轮成功，最终文件SHA256为2941ed241563b868ac2ce873540a8f9008ffbb5e7901c4e411aa4ee9da1de425。最终4页渲染已目检，目标软件编辑重开仍待验证。
