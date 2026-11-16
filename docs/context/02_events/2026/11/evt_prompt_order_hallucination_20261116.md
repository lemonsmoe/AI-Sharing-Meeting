---
id: evt_prompt_order_hallucination_20261116
event_time: 2026-11-16T09:24:00+08:00
recorded_at: 2026-11-16T09:24:00+08:00
agent: 01a1b28a-425f-7a03-8728-e93cfa030f78
domain: content
kind: presentation_revision
status: verified
summary: 按用户保存的顺序衔接表情包案例，补充幻觉类型与成因，同步28页讲稿备注
related_paths:
  - slides/projects/user_revision_ppt169_20261116/exports/AI分享_28页顺序与幻觉修订版_20261116.pptx
  - docs/content/user_revision_20261116/speaker_script.md
  - docs/content/user_revision_20261116/order_revision.json
  - docs/content/user_revision_20261116/order_verification.json
related_commits: []
supersedes: []
---

用户要求公司表情包放第12页，紧接第11页提示词介绍，用来说明具体需求影响图像输出；幻觉页补回名称、类型和更专业的成因。已确认读取的用户保存版PPT中表情包就在第12页，因此保留该顺序与该页原生对象，另存新版，不覆盖用户原文件。

讲稿第11–13页衔接改为提示词定义→公司表情包具体案例→PPT需求写法。幻觉页顺延第17页，明确事实性幻觉、忠实性幻觉；原因分为训练目标与事实核验的差距，以及数据质量与知识边界。讲稿补英文术语、例子与白话解释；依据用户原稿、Huang等综述和OpenAI原理说明，避免把概率预测、不能检索或无法辨别真伪绝对化。

同步28页备注、照读稿、SVG、原生预览、来源和补图说明。三处待补图现在为P8/P23/P24。旧生成脚本加保护，避免恢复旧页序。

独立Agent核对原始来源并阅读改后讲稿、查看P12/P17原生图，复核通过；采纳其P12开场衔接建议。28页原生导出、备注逐页一致、原生标题编辑保存重开通过。除本轮改写的P17外，26页与历史对应预览像素一致；P12与用户保存原件形状XML完全相同，两次原生渲染仅一个像素差异。第3页与末页继续保留。

最终PPT SHA256：`095333dc4246b9a1804553b6f80abb30e2ee890740c2368f7b1383cb5158264e`。用户原文件SHA256保持`eb2e1ff84a1d8ffc24368f33ea572698550ebfaa20f7f60e090b4bcfb011ef39`。
