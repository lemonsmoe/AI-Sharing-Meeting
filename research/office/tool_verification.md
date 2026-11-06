# 工具能力、费用与实践补证

访问日2026-11-06；均为条件候选，未作采购推荐。本轮接续任务TASK-20261106-b4654364，继续active。

## 新来源台账
|ID|作者/URL|日期/语言/渠道/读取范围|具体依据与局限|证据组|
|---|---|---|---|---|
|S6|Teemo Weng https://github.com/teemoweng/lark-video2note |发布日期未知；中文；GitHub；README185—371行|视频字幕优先、妙记ASR兜底、结构化飞书文档；有示例链接和依赖限制。仅仓库作者报告，未运行、未核验样例文档|lark_video2note；独立作者实践1|
|S7|腾讯 https://www.workbuddy.cn/docs/workbuddy/Pricing |发布日期未标，说明7月1日升级；中文；官方；198—228行|个人订阅价格与积分说明；限时权益会变，非企业报价|workbuddy_pricing|
|S8|腾讯 https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes |发布日期未知；中文；官方；198—365行|默认权限与完全访问模式、工作空间边界、备份建议；说明页表格和正文有概括粒度差异，不能保证所有修改都弹确认|workbuddy_permissions|
|S9|Notion https://www.notion.com/help/ai-meeting-notes |发布日期未知；英文；官方；107—150行|Business/Enterprise等资格、桌面版本条件、浏览器仅麦克风；未测试当前账号|notion_meeting_notes|

## 已核实候选比较
|候选|适配方向|官方可核条件|费用证据|本地验证|
|---|---|---|---|---|
|WorkBuddy|批量文件、文档生成|默认权限按工作空间执行；完全访问影响客户端全部任务|标准月付99元，高级199元，旗舰999元；连续包月70/140/700；年付672/1344/6720。体验版500积分/月。S7访问日快照，非账单|未执行|
|Notion AI Meeting Notes|会议到知识库|S9桌面能采集系统音频和麦克风，浏览器仅麦克风；Business/Enterprise等资格|未读定价页，金额未知|未执行；公司迁移成本未知|
|飞书智能纪要|既有飞书协作内沉淀|帮助页正文不可读，暂不确认具体套餐/额度|未知|未执行|
|通用对话+人工复制|模拟逐字稿到结构化纪要|教程提供统一提示和检查项；具体产品能力另核|依选用账号，未核|仅教学参考答案，非两次独立运行|
|WPS AI|既有办公文件处理|购买页仅返回浏览器升级提示|访问失败，旧研报价不代替现价|未执行|

WorkBuddy定价为个人订阅，不说明企业数据策略；本地文件操作不等于模型本地推理或数据不出网。S8仅支持操作权限说明，不支持隐私承诺。

## 社区实践可借鉴内容
S6展示字幕获取、转写、结构化整理、云端归档是不同环节；前置依赖含飞书登录授权和下载工具，部分平台依赖登录。作者报告长文传输可能超限并采用分段追加。这里只用于说明流程拆解和失败路径，不采用作者耗时作本项目实测；未安装仓库或运行其中指令。

## 视频候选更新
检索日11-06，默认相关性；关键词Kevin Stratvert AI meeting notes、Notion AI Meeting Notes tutorial。YouTube已5条：
|URL|作者/发布日期|可见指标|选择理由/阅读状态|
|---|---|---|---|
|https://www.youtube.com/watch?v=mWRe8w6YjO0 |Kevin Stratvert频道；2025-06-20（Glasp页面）|Glasp显示96.9K views；点赞未知|跨场景案例；只读Glasp局部字幕及摘要，Read More失败，不计完整视频|
|https://www.youtube.com/watch?v=DqPfgpVgwFo |Kevin Stratvert；日期未知|未知|会议专题；正文Cache miss|
|https://www.youtube.com/watch?v=YI51S2XnDeo |Supreme Guru Tech；2025-05-22|搜索页717观看、2赞|步骤教程低互动对照；仅描述|
|https://www.youtube.com/watch?v=qT2xzWiPiBk |作者/日期待核|未知|完整指南候选；仅摘要|
|https://www.youtube.com/watch?v=f4ZYEZO3Sq0 |Notion官方帮助页链接；日期未知|未知|官方流程；打开失败|

B站第五条补入 https://www.bilibili.com/video/BV1sxSTBpE6u/ ：标题称68分钟会议跨模型测试；仅搜索摘要，作者日期播放点赞未知，不能认定测试有效。备选 https://www.bilibili.com/video/BV17hsgzuE3W/ 亦未观看。所有视频完整内容计数仍0。

## 门槛更新
去重有效来源9：原5+S6—S9。机构保守6（腾讯、微软、Scribbl、Spellit、Teemo Weng、Notion；论文作者尚待完整登记）。中文4、英文5；一手至少6；社区独立实践1（作者自述，未复现），3个视频0，渠道3（官方/论文、厂商博客、GitHub），两次独立产品执行0。数量不等于已验证，主推仍不通过。下一步应补实际运行与独立实践，避免只增加同厂商文档。
