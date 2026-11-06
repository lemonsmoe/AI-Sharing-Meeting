# 来源台账首轮

访问日均2026-11-06；以下按实际读到范围登记。英文、一手渠道为主，尚未达到研究门槛。相同机构文章可为不同来源，但不增加独立机构数。

|ID|URL|作者/日期|读取范围|主张与依据|关系/推广/局限|重复组|
|---|---|---|---|---|---|---|
|S1|https://www.anthropic.com/research/building-effective-agents|Anthropic/2024-12-19|定义、何时使用、框架、工作流章节|固定路径工作流与动态决策Agent有区别；复杂度增加延迟成本|支持分层；厂商观点；页面已更新，非2024原始快照|agents_architecture|
|S2|https://www.anthropic.com/research/effective-context-engineering-for-ai-agents|Anthropic/2025-09-29|定义与上下文关系章节|上下文包含指令、历史、外部资料与工具反馈|支持组合；厂商观点；不是统一标准|context_engineering|
|S3|https://www.anthropic.com/news/model-context-protocol|Anthropic/2024-11-25|发布介绍与架构|MCP用于AI系统与数据工具连接|支持接口层；厂商发布；不能证明效果收益|mcp_release|
|S4|https://arxiv.org/abs/2005.11401|Lewis等/2020-05-22|摘要与版本信息|结合参数模型与检索记忆生成|支持历史节点；论文；未精读实验，不推广论文成绩到本公司|rag_paper|
|S5|https://arxiv.org/abs/2210.03629|Yao等/2022-10-06|摘要与版本信息|交替推理与动作获取环境信息|支持历史节点；论文；任务特定结果不能推广所有办公场景|react_paper|
|S6|https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills|Anthropic/2025-10-16|定义与渐进加载章节|Skills组织说明、脚本、资源，按需读取|支持复用层；产品推广可能高；具体实现依赖宿主|skills_design|
|S7|https://www.anthropic.com/research/effective-harnesses-for-long-running-agents|Anthropic/发布日期待复核|环境管理、功能列表与增量推进章节|状态文件与增量执行帮助接续；存在过早宣称完成问题|条件支持；厂商实践；非独立验证|harness_design|

有效阅读计数保守口径：S4/S5只计摘要阅读，不计全文精读；7条定位证据，3个作者团队/机构组，1类渠道（官方/论文），英文7、中文0，完整视频0，独立社区实践0。不存在15来源门槛通过结论。

主动负面检索：2026-11-06，查询site.anthropic.com research agent failures evaluation；获得Demystifying evals for AI agents等候选，仅搜索摘要，尚不计有效来源。查询site.simonwillison.net agents context engineering limitations未获得可用目标正文，须换检索式。

视频检索：2026-11-06，B站关键词“提示词 Agent MCP 教程”、YouTube关键词“context engineering agents tutorial”，按搜索返回相关性，不是全平台排行。YouTube https://www.youtube.com/watch?v=4GiqzUHD5AA （LangChain，2025-07-02，搜索可见198192播放/4900赞）仅描述阅读，非完整字幕；B站BV1LB766nEtT、BV1DRNe6wECX、BV1YWNQ6jEFh、BV1xjwizNEXx仅候选摘要，指标未知，未计有效阅读。两平台5候选及3视频门槛未达。

## 第二轮新增来源（访问日2026-11-06）
|ID|URL|作者/日期|实际阅读范围|依据与适用边界|推广/重复组|
|---|---|---|---|---|---|
|S8|https://www.anthropic.com/research/demystifying-evals-for-ai-agents|Anthropic/2026-01-09|Introduction、Structure、Why build evaluations|区分任务、trial、过程轨迹、最终环境状态；模型声称完成不等于环境已改变；多trial处理变异|厂商经验；evals_design|
|S9|https://www.anthropic.com/research/multi-agent-research-system|Anthropic/2025-06-13|Benefits与Architecture|研究查询可分解多方向；依赖密集任务不适合，token成本上升；内部评测不作本公司收益预测|产品案例推广；multi_agent_research|
|S10|https://www.humanlayer.dev/blog/advanced-context-engineering|Dex/HumanLayer，2025-08-29|开篇、Intentional Compaction、What eats context、上下文质量段落|作者用结构化产物保存工作状态；日志噪声和缺失信息影响上下文；只是其编码实践，不能推广普遍效率数字|有产品关联；humanlayer_compaction|
|S11|https://simonwillison.net/2025/Jun/27/context-engineering/|Simon Willison/2025-06-27|正文第6至20行|作者解释术语转向，强调任务可解所需的信息；其中引用他人观点按转述处理，不增加独立实例|个人评论；context_term_comment|

计数更新：11条已读定位来源（2篇仅摘要）；5个作者团队/机构组；2类渠道；英文11，中文0；社区亲历细节仅S10可作为局部实践线索，尚不足6个独立实践；完整视频0。S1/S9含复杂度与成本限制，S10含上下文失败讨论；不能因为反面措辞就宣称独立反证充足。

## 第四轮中文来源（2026-11-06访问）
|ID|URL|作者/发布日|实际阅读范围|主张与具体依据|推广、局限与重复组|
|---|---|---|---|---|---|
|S12|https://qwen.readthedocs.io/zh-cn/latest/framework/function_call.html|Qwen团队/未知|什么是函数调用章节、流程说明|模型选择工具并给参数，应用执行并将结果返回；工具调用不是模型自己直接访问所有业务系统|官方技术文档；未本地运行Qwen；qwen_function_call|
|S13|https://dify.ai/zh/workflows|Dify/未知|Workflow Studio概述、运行方式、日志与人工审核|模型、检索、工具、代码、分支可连接为流程；产品明确区分Workflow与Chatflow触发形式|官方营销页，不能证明可靠性；dify_workflows|
|S14|https://dify.ai/zh/rag|Dify/未知|数据源到检索、分块索引、检索精炼、测试章节|知识管线包括提取处理存储检索，检索结果可过滤重排与标注来源|官方营销页，非效果实验；dify_knowledge_pipeline|

另读Dify中文首页，内容与S13/S14高度重合，不额外计数。AI Engineer的Dex演讲配套页面已打开，只有整理文章可读，不计完整字幕，也不把它与S10作为独立实践。

当前保守计数：14条定位来源（其中2篇仅摘要）；作者/机构7组；官方/论文与个人技术博客2渠道；中文3、英文11；视频有效内容0。至少15来源、8作者、4渠道、6独立实践和3视频均仍未达标。中文3条只代表语言覆盖，不能替代独立实践。

## 第五轮独立作者与反例补证（2026-11-06访问）
|ID|URL|作者/日期|阅读范围|主张与证据|独立性、推广与局限|重复组|
|---|---|---|---|---|---|---|
|S15|https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus|Yichao Ji/Manus，2025-07-18|正文含缓存、工具选择、文件系统、任务清单、错误与重复模式章节|原作者报告框架多次重构；保存外部文件便于恢复，保留失败反馈帮助改进下一步；工具过多与模式模仿也可导致失败|独立于Anthropic的产品团队亲历；产品推广高；无公开对照数据，本地未复现；不沿用历史价格|manus_context|
|S16|https://www.philschmid.de/context-engineering|Philipp Schmid/2025-06-30|全文定义、上下文组成及会议示例|指令、历史、记忆、检索和工具共同构成上下文|独立作者论述；会议示例是说明性例子，不计实际运行案例；“大多数失败源于上下文”缺统计支撑，不采用该强断言|phil_context|
|S17|https://www.langchain.com/blog/context-engineering-for-agents|LangChain团队/2025-07-02|概述、上下文类型、失败类型与四类策略入口|整理写入、选择、压缩、隔离四类做法，强调长期工具反馈会累积|厂商教学兼推广；转述Manus/Anthropic等不增加案例；与其视频合并来源组，不冒算视频阅读|langchain_context|
|S18|https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html|Drew Breunig/2025-06-22|正文四种失败类型|作者提出错误污染、干扰、无关内容混淆、信息冲突的分类|个人原始分类可引用；其中论文数字属二手，不作为技术实证或独立实践，本轮不采用数字|drew_failure_taxonomy|
|S19|https://cognition.com/blog/dont-build-multi-agents|Walden Yan/Cognition，2025-06-12|正文完整原则、单线程与压缩方案|原作者指出并行子任务会携带冲突的隐含决策；团队做过专用压缩模型；需要共享相关决策上下文|独立产品团队；游戏示例是说明性例子，不是假定实测；标题不能解释为永不使用多Agent|cognition_context|

计数审计：登记19条，若严格排除S4/S5仅摘要阅读，正文定位来源17条；作者/机构组12个（Anthropic、Lewis团队、Yao团队、HumanLayer、Simon、Qwen、Dify、Manus、Philipp、LangChain、Drew、Cognition），排除两篇摘要后10组。渠道仍仅官方/论文与个人博客2类。中文3；完整视频0；详细独立实践保守计S10、S15、S19三组，S19细节较薄，待进一步材料。6实践与4渠道/3视频仍未过。

## 第六轮视频内容更新
2026-11-06从AI Engineer页面实际点击Transcript download获得V1/V2/V3，已阅读接口返回的全部演讲文本，覆盖开场至结束语。具体URL、条目范围、时间码和转写限制见video_content_review.md。
- V1与S10同作者同工作流，不增加独立来源组。
- V2与S6为Skills同主题，合并相关组。
- V3为不同演讲及部署案例，可以登记新案例，但不增加独立作者；实践数量仍按独立作者保守核算。
- 原有“完整视频0”是历史进度，当前为发布方完整字幕3、原片视听0；渠道目前3类，仍不足4。
- 第三方Usufn8IQJgw字幕页面本轮访问Cache miss，未读完整，不计。

## 第七轮开发者社区记录（2026-11-06访问）
|ID|URL|作者/日期|实际读取范围|事实层级及依据|局限/重复组|
|---|---|---|---|---|---|
|S20|https://github.com/microsoft/vscode/issues/282699|ainehickey/2025-12-11|问题正文及关闭状态|报告接入GitHub MCP与内置工具后工具数超限，提出按需加载；已因重复关闭|用户报告，未本地复现，不能代表当前版本；vscode_tool_loading|
|S21|https://github.com/anthropics/claude-code/issues/102389|nurma-zimran/2026-10-15；John-Rood/10-16|环境、步骤、错误、workaround及后续复现说明|记录超大工具schema导致请求超限，压缩后仍保留工具定义；附版本、错误与复现路径|独立用户报告，非厂商证实；只读未执行修复脚本；oversized_schema|
|S22|https://github.com/NousResearch/hermes-agent/issues/4589|kingtobi1337/2026-04-02；perlowja/04-28|正文、代码位置、具体提示词与环境反馈|记录Skill未自动加载，后续作者给出模型、运行时、样例提示与轨迹链接|用户报告和产品相关比较；没有核验完整轨迹，不引用成功率；hermes_skill_routing|

实践证据组审计：HumanLayer(S10+V1/V3同作者合并)、Manus(S15)、Cognition(S19，细节有限)、ainehickey(S20)、nurma-zimran(S21)、kingtobi1337/perlowja(S22同一问题合并)共6组；若审查要求排除Cognition细节薄弱组，剩5组，需补。Anthropic S9是额外原作者实践，但厂商自评不冒充独立第三方验证。三条GitHub问题仅证明有人在指定环境报告问题，不能断言当前所有版本都失败。

渠道现为4类：官方/论文、个人技术博客、YouTube原发布方字幕、GitHub开发者社区。来源/作者/语言/视频覆盖数量达最低口径，但案例独立性质量与复现仍需主对话和审计聊天裁决；不得据数量称最终验收。

## 2026-11-06：按最终审计补独立实践

|ID|URL|作者/发布日|实际阅读|窄支持与限制|重复组|
|---|---|---|---|---|---|
|S23|https://lucumr.pocoo.org/2025/7/30/things-that-didnt-work/|Armin Ronacher，2025-07-30；访问2026-11-06|全文正文行12—95，重点Slash Commands与Hooks操作片段|独立使用者提供输入/环境/失败替代路径；可作详细一手实践候选，非本地复现、当前缺陷或效果比较|armin_agentic_workflow|

S19已重读，仍无可定位具体运行输入输出，不计详细实践。S23替补候选的资格矩阵见practice_addendum.md；不在旧6组上再加成7组。若主对话接受S23，则五个既有较具体组加此一组；不能自动记研究门槛/主推效果通过。其他五组本轮未重审。
