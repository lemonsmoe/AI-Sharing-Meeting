# 四页样例使用与生产入口

## 直接使用

打开 slides/experiments/output/weekly_report_sample_v1.pptx。它含4页、11个正文文本框、1个原生柱状图和4页讲者备注。所有业务数字都是模拟值。

先在Office或WPS中复制一份，修改第2页文字，再在第3页选择图表编辑数据，将甲组完成数8改为7，确认柱高和标签更新。保存、关闭、重开后再次核对。正式稿需要同步更新第2页原始记录，不能只改图表。已有PowerPoint 16.0副本验证：文字修改保存重开通过；仅改嵌入Excel单元格未同步图表，显式更新系列后才通过。普通编辑数据同步仍未通过，WPS未测，详见native_powerpoint_check.md。

## 当前环境复现

在项目根目录，用已配置的Node执行 scripts/slides/build_sample.mjs run_new，输出到slides/experiments/run_new。目录名只允许小写字母、数字和下划线，已有目录会拒绝覆盖。2026-11-06修正了有效字体参数typeface和纵轴min/max，reproduction_06已重新生成并逐页目检。修改脚本中的输入文字、categories和series即可换案例。不要直接覆盖已有实验目录。源码保留了完整模拟输入，样例未调用外部模型接口。

scripts/slides/finalize_sample.mjs负责包结构、尺寸、图表工作簿和重新导入校验。它目前指向run_03及输出v1；下一版需同时改输入目录、最终文件名和receipt路径。环境变量RUNTIME_NODE_MODULES须指向宿主提供的Node库路径。Windows受限环境可能拒绝官方校验器的硬链接发布，此时需走权限审批，不跳过校验。

scripts/slides/render_template.mjs支持两个可选参数：输入PPTX路径、渲染输出目录。渲染后逐页检查中文、遮挡、数字及备注，结构通过不代替目检。

## 用于领导审阅稿的候选生产方式

主对话的逐页内容JSON与讲稿先冻结一版，再按页型制作。优先挑封面、概念解释、操作案例、数据图表做代表页，人工确认后才扩展到30页。当前已有30页V2，见outputs/leadership_review_v2；PowerPoint原生显示及文字/表格回存已检查，视觉仍待主对话审阅，动画和现场播放未验收。

Copilot、Gamma、WPS AI沿用first_round.md同一4页输入，另存每次原始输出，记录全部人工改动与耗时。Gamma需专查图表是否仍能编辑数据，WPS需核验账号实际导出权限，Copilot需核验所用模板占位符及中文结果。未登录产品不能标实测完成。

最终生产工具由主对话根据效果和兼容证据选择；本地路线是已有可运行产物的条件候选，不是最终工具推荐。

## 新增验收细节

参考practice_evidence_04.md的原始实践，在同题生成前记录产品入口、版本与许可，避免把免费网页聊天与PowerPoint内部功能混为一谈。导出后分别检查文本框、表格、图表：文字可改不代表图表数据可改。检查全页页脚转义符、空洞补写、超高卡片及素材遮挡，保存修改前后文件。Gamma按播放模式与导出文件比对；旧版社区故障只作为检查线索，不预设必现。

## 可复制命令（本机环境）

在项目根目录的PowerShell 7中执行，run_new须改成未使用的目录名：

```powershell
$slide_node = 'C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
& $slide_node scripts/slides/build_sample.mjs run_new
```

生成的是构建草稿，不是已校验交付文件。检查四张PNG：中文、零基线、甲组8/2、乙组6/4、模拟标记和未知原因。修改数据必须同时修改原始记录与图表系列。finalize_sample.mjs为历史固定入口，不要直接运行覆盖v1；复制到新脚本并同时改candidatePath、finalPath和receiptPath后按上述校验流程运行。脚本内运行库路径绑定本机，换机器应先通过宿主依赖工具定位库，不能假设同路径存在。

## 三条产品路线共用的运行记录

产品执行时保存：日期、入口、账号许可、显示版本/模型、输入全文、提示词、原始PPTX、人工改动、修改后文件、准备/生成/核查/返工耗时、逐项错误。Copilot/Gamma/WPS目前只有文档路线，不能用本地确定性脚本的两次运行替代产品独立实验。无可用账号时保留条件候选。
