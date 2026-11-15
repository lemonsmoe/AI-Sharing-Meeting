# 用户自改版讲稿·润色与校对记录（2026-11-16 凌晨）

基准：[自己修改版.md](自己修改版.md)（用户手写）。产出：[speaker_script.md](speaker_script.md)（润色校对版）。润色原则：保留用户结构与口吻，只修语病（如「今天吗」→「今天嘛」、他/它混用、「各种…各种」重复）、补空位（MCP/Harness/Agent）、把括号里的备注转成可照读的话。

## 一、科普内容逐项校对（用户点名要求核实）

| # | 稿中主张 | 核对结论 | 依据 |
|---|---|---|---|
| 1 | 视频生成模型有 MiniMax H3、Seedance | ✅ 成立。MiniMax H3（海螺3）2026-07-31 发布并开源，支持文/图生视频、原生音频、2K、4–15 秒；Seedance 2.5 为字节视频模型 | [MiniMax 开源公告](https://www.minimax.cn/news/minimax-h3-open-source)、[Seedance 2.5](https://seed.bytedance.com/zh/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) |
| 2 | 大模型型号例子：GPT-5.2、Claude Opus、豆包 | ✅ 成立。GPT-5.2（2025-12 发布）、Claude Opus 4.5（2025-11 发布）、Doubao Seed 2.1 Pro（火山方舟当前 260915 版）。润色稿已把占位符「doubaoxxxx」替换为准确型号 | [i10X 模型新闻](https://i10x.ai/news/category/models/page/3?company=anthropic)、[火山方舟模型广场](https://ark.volcengine.com/region:cn-beijing/model/detail?Id=doubao-seed-2-1-pro) |
| 3 | AI 对行业冲击顺序「从绘画，到 IT，到最近的数学」 | ✅ 按大众感知时间线成立：2022-07 Midjourney、2022-08 Stable Diffusion 让绘画圈先受冲击；编程冲击随 GPT-4（2023）后大规模显现；数学节点为 AlphaProof/AlphaGeometry 在 2024 IMO 达银牌水平（DeepMind 2024-07 公告，Nature 论文 2025-11）。润色稿加「大致是这么个顺序」缓冲，正文不报具体年份 | [Midjourney 时间线](https://designdb.com/usr/upload/board/zboardphotogallery176/20250411045053787_5309.0.pdf)、[DeepMind IMO 公告](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/)、[Nature 报道](https://www.nature.com/articles/s41586-025-09833-y) |
| 4 | 幻觉分两大类：事实性幻觉（Factuality Hallucination）与忠实性幻觉（Faithfulness Hallucination） | ✅ 成立。文献标准分类（Huang 等 2023 综述及后续综述沿用）。润色稿用口语解释：事实性=编造不存在的事实；忠实性=偏离所给材料 | [Zenodo 综述 §2](https://zenodo.org/records/23386085)、[Huang et al. 2023](https://arxiv.org/abs/2311.05232) |
| 5 | 幻觉成因一：按概率预测下一个词而非检索事实 | ✅ 成立，与 OpenAI 官方解释一致 | [OpenAI: Why language models hallucinate](https://openai.com/index/why-language-models-hallucinate/) |
| 6 | 幻觉成因二：训练数据含错误、过时、偏见、虚构内容，冷门领域稀缺 | ✅ 成立，同上 | 同上 |
| 7 | 红果短剧、抖音上的 AI 视频「可以是小云雀生成的」 | ✅ 成立。小云雀为字节旗下创作工具（域名属剪映体系），官方手册面向短剧场景并首发 Seedance 2.5；红果有「AI 剧」分类 | [小云雀手册](https://xyq.jianying.com/tutorials/seedance-2-5)、[红果 AI 剧分类](https://hongguoduanju.com/category/ai-drama) |
| 8 | Peter Steinberger 原话与语境 | ✅ 逐词核对，沿用既有结论（目标≠已实现） | [本人博客](https://steipete.me/posts/2026/openclaw) |
| 9 | 黄仁勋引语与署名 | ✅ 既有结论；另有 SEC FY2026 年报署名「Jensen Huang, Founder and CEO, May 2026」旁证 | [quote_sources](../swiss_revision_20261115/quote_sources.md) |
| 10 | 「DeepSeek Harness」作为平台举例 | ✅ 成立，DeepSeek 官方文档列为 Agent 集成产品 | [DeepSeek 官方文档](https://api-docs.deepseek.com/quick_start/pricing) |
| 11 | Codex 桌面端「能操作电脑、控制鼠标点击按钮」 | ✅ 成立（OpenAI 桌面端具备 computer use 类能力），稿中已保留「合适的权限设置之后」前提 | [OpenAI Quickstart](https://learn.chatgpt.com/docs/quickstart.md) |

**无需修改的事实错误：0 处。** 全部主张成立，仅做了措辞缓冲与型号占位符替换。

## 二、本次润色改动清单

1. 开场、各节错别字与「他/它」混用修正；删重复词。
2. 概念编号理顺：MCP（7）、Harness（8）、Agent（9）三节按用户留的空位补写，各 3–4 句、口语化；「平台」节独立成段（原稿编号重复）。
3. 「doubaoxxxx」→「Doubao Seed 2.1 Pro」；模型名统一规范写法（GPT-5.2 / Claude Opus 4.5 / MiniMax H3 / Seedance）。
4. 幻觉科普由括号备注改写为照读正文，压缩到可讲长度，保留两大类型与两大成因。
5. 生图示例：补一段可直接照读的「表情包提示词」示例（主体/表情/风格/比例/留字五要素），现场配合公司表情包原件（已归档 `assets/company_meme/meme_original_20261116.jpg`，1280×1280）。
6. 结尾冲击顺序加「大致是这么个顺序」缓冲；其余用户观点原样保留。

## 三、时长估计与分页草案（待确认）

- 正文约 5,300 汉字，按 3.5 字/秒约 **25–26 分钟**；加演示、翻页、现场互动，整场约 35–40 分钟，低于 1 小时上限，留有问答余量。若想接近 48 分钟，可在「平台」「AI PPT 制作」两节各加一段现场演示。
- 分页草案（约 26 页，供制作时参考，以最终定稿为准）：开场 2 页｜工具切入 2 页｜Agent 引子 1 页｜概念（大模型与App 1、上下文 1、原理 1、多模态 1、提示词 4、幻觉 2、Skill 2、MCP/Harness/Agent 1）｜平台 Codex 3 页｜AI PPT 2 页｜生图表情包 1 页｜学习路径 1 页｜本地部署/费用 1 页｜结尾 1 页。
- 旧 30 页分镜 outline.md 与 speaker_notes_per_page.json 已过期，待分页草案确认后重做分镜与备注包。

## 四、素材需求（加料清单，按你的要求）

- Codex 桌面界面截图（你本机截，脱敏）→「平台」节。
- Skill 文件夹截图（可用项目里 tools/project_skills 或 ppt_master 文件夹，我这边做不了截图，需要你截或我来做示意卡片）。
- 提示词输入框示意（可做文字卡片示意，或你截豆包/Codex 输入框）。
- 工具/模型图标：豆包、飞书、腾讯会议、GPT、Claude、WorkBuddy、DeepSeek、小云雀、红果、即梦、MiniMax、Seed——可从各官网公开资源下载，我下一轮批量处理并登记来源。
- 表情包原件 ✅ 已归档；生图提示词示例 ✅ 已写入。
