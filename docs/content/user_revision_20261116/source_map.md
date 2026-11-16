# 图片和事实来源

以下区分用户材料、本项目真实操作、官方界面示例及科普图。页面上的示例不能据此说成某款软件已在本项目完成实测。

| 页码 | 内容 | 来源与用途 |
|---|---|---|
| 2、26 | 本稿缩略图 | 当前 28 页 PPT 的 PowerPoint 原生导出；仅展示作品，不宣称一次提示直接生成成品。 |
| 4、21 | ChatGPT、Claude、即梦、小云雀 | [ChatGPT](https://chatgpt.com/)、[Claude 官方标识](https://claude.com/icon.png)、[即梦](https://jimeng.jianying.com/)、[小云雀](https://xyq.jianying.com/)；对应原始文件和哈希在素材 provenance。WorkBuddy 的 WB 为普通缩写标签，并非声称官方图标。 |
| 6 | Karpathy 引语与肖像 | [本人原推](https://x.com/karpathy/status/1617979122625712128)，2023-01-24；X 官方 oEmbed 回应保存在 `assets/revision_research_20261116/karpathy_quote_oembed.json`。[本人官网肖像](https://karpathy.ai/)。英文逐字引用，中文为翻译。 |
| 7 | 豆包手机界面、Arena | 豆包官方 App Store 宣传图；[Arena Text 排行榜](https://arena.ai/leaderboard/text)为本轮浏览器截图，画面榜单日期 2026-11-11。裁剪只放大表格，不改数字。排名用于辨识型号，不作为所有任务的能力结论。 |
| 7 | GPT-6.1 Sol、Claude Opus 5.5、Doubao Seed2.1 Pro | 原始官方链接与核验摘要在 `assets/revision_research_20261116/brief.md` 及 `provenance.json`。它们是厂商型号例子，不等同于左侧 App 的默认模型；OpenAI 入口与用途也有差别。 |
| 8、11 | 豆包输入框 | 本轮在豆包网页版实际输入后截图；未发送、未上传附件、未获得回复。第 8 页右侧留用户补图位，第 11 页仅讲提示词输入。 |
| 9 | 逐 token 预测原理图 | Jay Alammar [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/)。采用原作者自回归 GIF 第 38 帧，未重画。原图用 GPT-2 说明机制，不表示它是当前最新模型。页面保留作者署名。 |
| 10 | 图像与机器人 | 豆包官方宣传图；[Google DeepMind Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/)官方演示图。说明信息模态与具身行动是不同维度，不宣称穷尽 AI 分类。 |
| 15、26 | Swiss Grid | 用户下载并指定的 `assets/references/swiss_grid_systems.pptx`；[原模板项目](https://hugohe3.github.io/ppt-master-examples/viewer.html?project=ppt169_swiss_grid_systems)。 |
| 16 | 旧样稿 | 本项目 `slides/master_restart_20261109/master_preview_20261109/native_validation_v2/slide_01.png`，用于指明具体修改位置。 |
| 17 | 幻觉类型与成因 | [OpenAI：Why language models hallucinate](https://openai.com/index/why-language-models-hallucinate/)；[Huang 等综述 §2.3、§3](https://arxiv.org/html/2311.05232v2)。采用事实性/忠实性幻觉分类；后者包含指令、上下文与逻辑一致性。讲稿解释训练目标与事实核验的差距，以及数据质量和知识边界；避免“总是取最高概率”“不会检索”“完全无法区分真伪”等绝对说法。 |
| 18 | Skill 目录 | 实际读取本机 `.context_runtime/ppt_skill_candidates/ppt_master/`，展示 SKILL.md、workflows、templates、scripts 及真实文件名的节选。目录树不是假造软件界面。 |
| 19 | MCP | [MCP 官方架构](https://modelcontextprotocol.io/docs/learn/architecture)。页面为中文简化关系图，会议记录查询是示例，不声称已接入公司的会议系统。 |
| 20 | Harness / Agent | [Anthropic：Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)。Harness 是运行支撑，Agent 围绕目标决定行动，不保证自动完成或不会出错。 |
| 20、22、23 | Codex 本项目界面 | 用户提供的 `codex-clipboard-2c262479-ec36-4158-a5ab-5738d5578b6b.png`，保存为项目 `images/codex_user.png`；实际显示三页样稿回复。不能当成初次提示词或 Skill 调用截图。 |
| 22 | 上手四类功能入口 | 根据官方 [App 入门](https://learn.chatgpt.com/docs/app)、[项目与聊天](https://learn.chatgpt.com/docs/projects)、[文件预览](https://learn.chatgpt.com/docs/artifacts-viewer?surface=app)归纳；四类是讲解方法，非声称官方固定模块名称或所有平台布局一致。 |
| 24 | Skill 选择菜单 | WorkBuddy 官方教程截图，原链接保存在 `assets/revision_ui_20261116/workbuddy_skill/provenance.json`。只展示实际菜单，不声称此图运行过 PPT Master；右侧留当前 Codex 调用截图位。 |
| 25 | 文件预览、浏览器执行记录 | OpenAI 官方[文件预览](https://learn.chatgpt.com/docs/artifacts-viewer?surface=app)界面示例；[WorkBuddy Agent Browser 官方教程](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/WorkBuddy-Zero-Cost-Skill-Top-10/Agent-Browser)中打开、读取、滚动的实际执行记录截图（未展示被操作网页本体），不是本项目实测。普通对话示例来自豆包官方爱学宣传图。 |
| 26 | 五步 PPT 流程 | 参考知乎公开回答[如何用 Chatgpt 创作 PPT](https://www.zhihu.com/tardis/bd/ans/3595210148)的可读搜索摘录，以及本项目实际流程；知乎直开遇到验证，未称通读或高赞。另参考[公开教学指南](https://jwc.hati.edu.cn/__local/E/73/53/ED9C02DA409BB2970EB4C05E5E6_99467646_10542F1.pdf)的生成、修改大纲、选模板、生成、修改 PPT 流程。五步是整理表达，不是原文引用。 |
| 12 | 公司表情包 | 用户原件 `assets/company_meme/meme_original_20261116.jpg`，4×4 共 16 格。提示词由用户授权根据图像重新拟写，不宣称找回原始提示词。 |
| 27 | 订阅、API、本地部署 | 基本计费方式的概念比较，不提供实时价格或默认所有供应商规则相同；API 计费与会员通常分开，本地也有设备维护成本。 |
| 28 | 结尾 | 按用户要求保留旧版末页和讲稿。原引语来源沿用 NVIDIA FY2026 Sustainability Report；本轮不把用户个人行业观察升级为已验证的行业排名。 |

逐图下载地址、哈希与日期见 `assets/revision_research_20261116/provenance.json`、`assets/revision_ui_20261116/provenance.json`。现场讲稿只保留口语内容，资料核对放在本文件，避免把制作备注念给观众。
