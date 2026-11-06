# 两份会议文件 → 可编辑 Excel

这是2026-11-06的真实文件生成演示，材料为模拟会议。本会话读完原文后整理字段，再由 artifact-tool 生成工作簿；没有在 WorkBuddy、Copilot 或 WPS AI 内执行。

交付：outputs/01a1afcd-c994-7ae0-89e1-3c3770ac406b/meeting_actions.xlsx。

原文保持在 tutorials/office/file_demo/input：meeting_notes.txt 与 follow_up.txt。输入哈希、输出哈希及检查结果见 validation.json。工作簿只有一个工作表，2个行动项、4个决定或未决信息。责任人和日期未知时为空白；报价任务未变成采购批准，网络假设未变成根因。

## 现场演示（约2分钟）

1. 打开两份短原文，让观众看到“负责人另定”“采购没批”。
2. 展示提示词：读取这两份文件，输出一份可编辑Excel。分开行动、已确认变更和未决信息；给来源编号；未知负责人、日期留空并提示待确认；不改原件，不发送消息。
3. 打开已生成的Excel，定位报告期限、演示改期和浅黄色未知字段。说明文件可继续由同事补充，完成情况尚未提供。
4. 演示副本中补一个负责人，期限仍留空，提醒一项信息补齐不代表全部已确定。正式交付文件不在台上覆盖保存。

不要把后台JS生成脚本展示成“普通办公用户必须写代码”；同事学习的是给材料、明确交付、核对结果。脚本保留用于维护和复现。

## 复现与检查

生成器：build_workbook.mjs。使用Codex桌面绑定的Node及官方artifact-tool依赖。node_modules是到已安装运行时的目录连接，不包含复制的依赖；换机器时应重新通过load_workspace_dependencies定位，不安装到本项目根目录。

在项目根运行：

```powershell
& 'C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' tutorials/office/spreadsheet_demo/build_workbook.mjs
```

此命令复现固定材料的排版与数据，并覆盖同名演示Excel；它不是再次独立执行一次AI提取。更换材料时需要重新阅读和核对，不能直接把固定脚本当通用抽取器。

已检查：原文全部逐项对照；导出日期使用原生日期类型（XLSX单元格t=d），估算金额为数值并标“约”；未知字段保留；无公式错误；整张渲染图实际查看并修正日期与来源间距。另读取导出XML核对日期类型、8000数值和两个空白字段。工作簿没有计算公式，不把“无公式错误”夸大为计算能力测试。未在Excel/WPS应用中打开验证，尚需现场设备打开检查。
