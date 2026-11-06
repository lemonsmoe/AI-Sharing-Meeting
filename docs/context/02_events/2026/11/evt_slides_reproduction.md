# 四页复现入口修复

2026-11-06；负责人01a1b056-35e7-78f0-bd7f-89fcc0d7cef2；TASK-20261106-91b46501。

审计指南发现build_sample.mjs仍使用fontFamily、minimumScale/maximumScale，后续赋值又覆盖纵轴边界。已修正为typeface及min/max，并对输出目录名做限制、拒绝覆盖已有目录。

新目录slides/experiments/reproduction_06生成4页并逐页查看。source_check.json核对微软雅黑、纵轴0—10、原生图表字面值8/6与2/4。该文件仍是构建草稿，未替换历史最终样例，也不冒称新的独立模型实验。

同步research/slides/reproduction_guide.md、stage_handoff.md、progress.md及领域状态：加入实际PowerPoint结果与失败边界，消除“Office完全未测”“下一步代表页”等过时说法。保留三云端产品未执行、研究门槛未过的限制。

本轮属于进展。目标不能标完成：研究门槛、产品独立实测和主对话最终验收尚有缺口。未新提工具排名或更换已授权生产路线。
