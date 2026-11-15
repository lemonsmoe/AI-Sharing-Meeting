# 调研 Skill 候选与使用安排

2026-11-09 初筛。星数为所在 GitHub 仓库的页面约数，不是单个 Skill 的评分；未安装或启动对应框架。已有 `ai-workflow-research` 的证据要求继续有效，本次没有降低门槛。

## 值得先借鉴的两个来源

|来源|仓库约数|具体 Skill|适合负责什么|迁移边界|
|---|---:|---|---|---|
|[ByteDance DeerFlow](https://github.com/bytedance/deer-flow)|85.1k|[github-deep-research](https://github.com/bytedance/deer-flow/blob/main/skills/public/github-deep-research/SKILL.md)|开源项目的 README、代码结构、依赖、issues、历史与替代路线比较|适合 GitHub 项目，不等于通用办公产品实测；先借用流程，不为两天初稿部署整套框架|
|[Anthropic knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)|35.2k|[search-strategy](https://github.com/anthropics/knowledge-work-plugins/blob/main/enterprise-search/skills/search-strategy/SKILL.md) 与 [knowledge-synthesis](https://github.com/anthropics/knowledge-work-plugins/blob/main/enterprise-search/skills/knowledge-synthesis/SKILL.md)|拆问题、安排检索、去重、保留矛盾，把已有资料整理成可讲结论|原包针对 Claude 与企业连接器；在 Codex 需映射可用工具，不能宣称直接安装就功能等同|

已读上述三个 SKILL.md 正文。DeerFlow 有多轮调查与来源追踪，适合本次 PPT 仓库比较；其中固定置信度百分比不直接沿用，因为没有校准依据。Anthropic 的两个 Skill 更适合把已有研究转成讲稿、教程和证据摘要。

另外发现 [Tavily Skills](https://github.com/tavily-ai/skills)，页面约 490 星。只读 README：更偏搜索/提取/深度研究工具入口，部分功能需要认证；没有把其具体 research SKILL.md 读取成功，因此不列为已完成审查的主候选。

## 本项目建议：检索方法、综合方法、证据验收分工

- 查开源工具：参考 DeerFlow，交付“当前版本能做什么、执行入口、问题、最小复现”。
- 整理已有知识：参考 search-strategy / knowledge-synthesis，优先查项目材料，再补精确缺项；保留有出处的分歧。
- 决定能否讲成亲测推荐：继续用本项目 `ai-workflow-research`。官方功能、作者案例、本地实际输出、用户体验分别登记。
- 质量证据不足的产品可以明确标为候选介绍；不能以时间紧为由升级成“验证最好”“普遍节时”。

## 可见子聊天任务书建议，尚未派发

|聊天|具体目标|应交成果|何时完成|
|---|---|---|---|
|概念/提示词|用现有材料解释 LLM、提示词与协作；检查概念和例子|逐页讲稿、一个连续案例、容易误讲处、来源|读者能按提纲讲清，核心说法逐项有依据|
|办公场景|把 O1 与一个可用工具体验做成跟做教程|输入、完整提示、实际输出、3—5 步操作、核对点、失败恢复|用户可在约 10—15 分钟内做一遍；缺账号则交具体缺项与已有路线|
|PPT 制作|按用户最终选择做三页，再扩 30 页|实际 PPTX/HTML、逐页预览、备注、修改记录|先三页质量认可，再完成整套；不能自行选定路线|
|方法复核|查事实越界、来源和教程复现问题|短问题清单与可操作修正|解决具体问题，不反复扩充同类 URL|

沿用原可见聊天和共享上下文，视频聊天继续暂停。启动前明确目标、写入范围与完成证据；目标模式只服务这些边界明确的任务，不用“持续研究”替代交付。研究和制作由不同聊天协作不自动构成盲测。

建议完成一次流程适配后再决定是否安装研究 Skill。当前已研究并推荐，尚未启动新的目标循环或旧子聊天。
