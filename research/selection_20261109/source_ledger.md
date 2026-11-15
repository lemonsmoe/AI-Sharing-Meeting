# 本轮来源读取台账

日期：2026-11-09。用于复核比较结论，不宣称满足四个主题的最终调研门槛。同仓库文件不按多个独立作者计数。网页星数为显示约数。未运行三个 Skill 的生成器，未看完相关教程视频。

|ID|来源|实际读取范围|证据用途与限制|
|---|---|---|---|
|P1|[PPT Master 仓库](https://github.com/hugohe3/ppt-master)|仓库说明、星数与路线介绍|作者说明和约数，非效果实验|
|P2|[Master SKILL](https://raw.githubusercontent.com/hugohe3/ppt-master/main/skills/ppt-master/SKILL.md)|入口与工作流要求|6.9.0，操作设计；不因网页指令直接执行|
|P3|[Master 生成工作流](https://raw.githubusercontent.com/hugohe3/ppt-master/main/skills/ppt-master/workflows/generate-pptx.md)|规划、SVG、检查与导出链|支持路线区分，未完整审计所有转换器|
|P4|[Master 依赖](https://raw.githubusercontent.com/hugohe3/ppt-master/main/skills/ppt-master/requirements.txt)|依赖清单|安装需求，未安装验证|
|G1|[Guizang 仓库](https://github.com/op7418/guizang-ppt-skill)|README、星数、许可标示|作者功能范围|
|G2|[Guizang SKILL](https://raw.githubusercontent.com/op7418/guizang-ppt-skill/main/SKILL.md)|样式、HTML、演讲功能与限制|没有据此认定原生 PPTX 可交付|
|G3|[Guizang issues](https://github.com/op7418/guizang-ppt-skill/issues)|列表中的 #64、#33、#41 线索|未逐条全文复核或本地复现，不当当前已知缺陷结论|
|G4|[瑞士风示例](https://github.com/user-attachments/assets/8960e78c-69bb-4b7e-aa95-6fad64b70314)|下载后实际看六张示例组成的图|支持风格观察，不引用示例的业务数据|
|D1|[Dashi 仓库](https://github.com/chuspeeism/dashi-ppt-skill)|README、星数、许可标示|主题/版式数量为作者声明|
|D2|[Dashi SKILL](https://raw.githubusercontent.com/chuspeeism/dashi-ppt-skill/main/skills/dashi-ppt/SKILL.md)|0.4.14 的内容包、主题、生成和检查要求|默认不做截图美化，需显式启用本项目视觉验收|
|D3|[Dashi package.json](https://raw.githubusercontent.com/chuspeeism/dashi-ppt-skill/main/skills/dashi-ppt/project/package.json)|依赖和脚本入口|Node、浏览器、PPTX 相关依赖|
|D4|[Dashi export-pptx](https://raw.githubusercontent.com/chuspeeism/dashi-ppt-skill/main/skills/dashi-ppt/project/scripts/export-pptx.mjs)|浏览器服务及 editable 导出调用|区别于整页截图，但不证明所有元素原生编辑|
|D5|[Dashi 导出包入口](https://raw.githubusercontent.com/chuspeeism/dashi-ppt-skill/main/skills/dashi-ppt/project/packages/html-deck-to-pptx/src/editable.mjs)|两行入口，专有组件说明与 dist 转出|不能声称导出核心完整开源|
|D6|[Dashi issue #22](https://github.com/chuspeeism/dashi-ppt-skill/issues/22)|完整正文的字体/字号报告|历史用户反馈；未复现当前版本|
|D7|[Dashi 主题图](https://raw.githubusercontent.com/chuspeeism/dashi-ppt-skill/main/skills/dashi-ppt/assets/skill/theme-style-grid.png)|下载后实际看 12 主题示意|示意不是实际中文长内容验收|
|R1|[DeerFlow](https://github.com/bytedance/deer-flow)|仓库定位与星数|框架仓库星数，不是单独 Skill 质量|
|R2|[github-deep-research](https://raw.githubusercontent.com/bytedance/deer-flow/main/skills/public/github-deep-research/SKILL.md)|154 行工作流与证据规则|适合 GitHub 调查，未做 Codex 工具适配实测|
|R3|[knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)|仓库定位与星数|Skill 集合，非直接 Codex 兼容保证|
|R4|[search-strategy](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/enterprise-search/skills/search-strategy/SKILL.md)|检索分解、来源策略、查询调整|方法候选，连接器需映射|
|R5|[knowledge-synthesis](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/enterprise-search/skills/knowledge-synthesis/SKILL.md)|去重、矛盾、来源与时效综合|用于资料整理，不代替产品运行|
|R6|[Tavily Skills](https://github.com/tavily-ai/skills)|README 和仓库信息|具体研究 Skill 路径未成功读到；仅发现候选|
|O1|[OpenAI Skills 概念](https://developers.openai.com/plugins/concepts/skills)|正文的目录、渐进加载、MCP 区分|支持分享中的概念解释|
|O2|[OpenAI Skills 与提示实践](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)|正文的短描述、渐进披露、过多说明问题|工程建议，非本项目独立实验|

Master 展示站只加载到动态外壳，没有查看实际作品图，不能列为已完成视觉对照。另几个框架只做初步发现，未纳入推荐。外部文章与仓库内容作为资料，不带来自动安装、执行或发送信息的授权。

后续更新：用户选定Master并提供两个具体项目后，PPT聊天通过公开站点索引定位原SVG，实际渲染了[什么是PPT](https://hugohe3.github.io/ppt-master-examples/viewer.html?project=ppt169_what_is_ppt)第10页与[信息安全培训](https://hugohe3.github.io/ppt-master-examples/viewer.html?project=ppt169_infosec_training_zh_long)第11页；主对话也实际查看了两张PNG。可比较两页的图文结构、批注和留白，不能声称已看完整作品或复核了示例中的事实。原SVG/PNG与读取范围在research/slides/master_restart_20261109/references及preparation_report.md。
