# 三个 PPT Skill 的选择依据

核对日：2026-11-09。当前结论是源码与说明初筛，尚未进行三套同题生成、原生应用回存或独立效果评审。用户读完后已选择 **PPT Master**：认为案例与样式更丰富，更适合此次较多图文的分享培训；Guizang 简约风留作以后使用，Dashi 的预设风格不合偏好。此前“先试 Dashi”提案不再执行。

## 差别在交付路线

|候选|GitHub 页面约数|主要交付|适合本项目的方面|需要实际验证的地方|
|---|---:|---|---|---|
|[PPT Master](https://github.com/hugohe3/ppt-master)|74.9k|内容与规划→SVG→原生 PPTX；可用自己的 PPTX 模板|公司模板、PowerPoint 原生对象、后期编辑、讲者备注；流程较完整|SVG 支持范围、对象可编辑程度、中文字体现实表现；流程完整不保证叙事或审美|
|[Guizang](https://github.com/op7418/guizang-ppt-skill)|29.5k|单文件 HTML 演示；杂志/墨水屏、瑞士风两类视觉体系|浏览器演讲、双屏讲者模式、备注、排练计时；已看瑞士风示例，层级清楚|原生可编辑 PPTX 不是已确认的默认出口；当前演示步进和安装资源完整性需检查|
|[Dashi](https://github.com/chuspeeism/dashi-ppt-skill)|10.5k|结构化内容包→HTML 与浏览器编辑→PPTX/PDF|预设主题、版式、逐页候选，方便在浏览器改字换图；有助于先稳定版式|网页与实际 PPTX 的字体/位置差异；部分导出核心只分发构建产物；不能保证所有对象原生可编辑|

星数是当日网页显示的约数，会变化；代表关注度，不是本次作品质量排名。三者都没有完成本地生成实验，不能给出速度、成功率或视觉胜负的实测排序。

## 读取到的实现线索

### PPT Master

- 已读 [SKILL.md](https://raw.githubusercontent.com/hugohe3/ppt-master/main/skills/ppt-master/SKILL.md)、[生成工作流](https://raw.githubusercontent.com/hugohe3/ppt-master/main/skills/ppt-master/workflows/generate-pptx.md)和 requirements；读取时入口版本为 6.9.0。
- 工作流包含来源整理、模板候选、规划、SVG 页面、质量检查和 PPTX 导出。支持的 SVG 元素编译到 DrawingML；不是只把网页整页截图放进 PPT。
- Python 路线涉及 python-pptx、XlsxWriter、路径和字体处理等依赖。音频、视频及部分扩展依赖不属于当前无视频需求。
- 仓库以 MIT 标示；执行时仍应读取该版本许可及署名要求。
- 推断：若最看重正常 PowerPoint 交付、公司模板和后续修改，它是很有理由优先试的候选。详细流程可能增加准备工序，未计时，不能称更慢。

### Guizang

- 已读 [README](https://raw.githubusercontent.com/op7418/guizang-ppt-skill/main/README.md)和 [SKILL.md](https://raw.githubusercontent.com/op7418/guizang-ppt-skill/main/SKILL.md)。定位首先是 HTML 演讲，不宜把“有漂亮幻灯片”直接等同于“有原生 PPTX”。
- 实际查看了[瑞士风示例图](https://github.com/user-attachments/assets/8960e78c-69bb-4b7e-aa95-6fad64b70314)：大字、留白、蓝白黑层次明确；小字号细节仍需按中文会场视距重做。
- issues 列表出现过讲者模式步进跳过、可编辑 PPTX 请求和安装缺资源反馈。这里只读到列表线索，未在当前版本复现，不能宣称现在仍有这些缺陷。
- 仓库标示 AGPL-3.0；如果要再分发或改造成服务，另核具体使用条件。

### Dashi

- 已读 [SKILL.md](https://raw.githubusercontent.com/chuspeeism/dashi-ppt-skill/main/skills/dashi-ppt/SKILL.md)、package.json、PPTX 导出脚本和导出包入口；读取时入口版本为 0.4.14。
- 文档描述 12 主题、1020 个版式页，以及每个逻辑页多个模板候选和一个自定义候选。这是作者的资源规模说明，不是逐页质量验收。
- 本地浏览器可改字换图；Node 20+ 和 Chrome/Chromium/Edge 是相关依赖。导出代码调用 editable PPTX 路线，另有截图 PDF 路线。
- 默认工作流不自动做截图审美打磨。本项目明确需要逐页视觉审查，应把它写入任务，而非照默认设置省略。
- 完整读过 [issue #22](https://github.com/chuspeeism/dashi-ppt-skill/issues/22)：用户报告 HTML 与 PPTX 字体/字号差异。是历史反馈，需要当前版本重测。
- 仓库根部标示 AGPL-3.0，但导出核心入口注明专有组件并转到压缩构建文件；不能把整个导出链称作可完整审计的开源源码。
- 实际查看[主题总览图](https://raw.githubusercontent.com/chuspeeism/dashi-ppt-skill/main/skills/dashi-ppt/assets/skill/theme-style-grid.png)。它是示意预览，不能证明真实长中文内容的排版。07 冷白调研风、11 高能增长风可作为轻背景候选，未选定。

## 怎么选，避免再做一整套才发现不合适

三者共用 [三页试做任务](../../docs/content/restart_20261109/three_page_brief.md)：讲清任务、解释协作组件、展示纪要与表格成果。先看真实内容，不以封面或主题数量决定。

1. 内容：观众能否快速理解每页结论，段落是否适合听讲。
2. 画面：中文可读、关系清楚、留白充分、没有溢出或重复堆卡片。
3. 编辑：修改一个标题、一个业务字段，保存后重开。
4. 交付：查看实际导出的 PPTX 与讲者备注；浏览器效果单独记，不能代替 PPTX 验收。
5. 用户取舍：哪条路线愿意长期学习，现场能否顺手使用。

已选 PPT Master，以原生 PPTX 和图文表达能力推进。Guizang 收藏备用，Dashi 停止试做；三套已下载不意味着需要都生成完整作品。用户的选择与视觉偏好已确认，具体生成质量仍由样稿检验。

依赖与本地准备状态见 [准备记录](candidate_readiness.md)；完整来源范围见 [读取台账](source_ledger.md)。
