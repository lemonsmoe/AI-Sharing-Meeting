# 办公来源与交付统一核验索引

2026-11-06；本轮重新读取现有全部台账及示范输入输出，不是重新访问所有网站。外部访问日、URL、具体范围和限制以对应记录为准；旧报告数字是当时快照，当前汇总使用本页。作者自检不等于另一聊天独立审查。

## 24个已登记正文证据组

|ID|发布/作者主体|语言|正文记录位置|计数限制|
|---|---|---|---|---|
|S1|腾讯|中|evidence_ledger.md|产品说明|
|S2|Microsoft|英|evidence_ledger.md|官方操作指南|
|S3|Scribbl|英|round_two_evidence.md；access_and_protocol_review.md|S3b/c及协议合并，修正副本偏差|
|S4|Spellit/Oleg Kulakov|英|round_two_evidence.md|厂商博客，转述论文不另算|
|S5|CHiME研究团队|英|round_two_evidence.md|局部论文正文；完整作者待补|
|S6|Teemo Weng|中|tool_verification.md|作者仓库实践，未本地执行|
|S7|腾讯|中|tool_verification.md|价格页，主体与S1相同|
|S8|腾讯|中|tool_verification.md|权限页，主体与S1相同|
|S9|Notion|英|tool_verification.md|官方帮助|
|S10|Crossing|中|practice_review.md|转载归原作者，商业关系未核|
|S11|shxjnpl|中|practice_review.md|身份与数据未核，不计严格实践|
|S12|AP/Michigan Radio|英|company_cases.md|团队报告，摘要功能未完成|
|S13|OCUL|英|company_cases.md|团队转写FAQ|
|S14|Microsoft/Schneider|英|company_cases.md|厂商客户故事|
|S15|Microsoft/Kantar|英|company_cases.md|厂商客户故事，预期不作实现|
|S16|Microsoft/Lifetime|英|company_cases.md|厂商客户故事|
|S17|AlphaSense/Siemens|英|company_cases.md|付费研究与公开材料混合|
|S18|Microsoft/U.S. AutoForce|英|company_cases.md|对账子场景，未本地复现|
|S19|Cleric/Mixmax|英|company_cases.md|厂商客户故事，非自动修复|
|S20|Wilkey/Wood、PTSEM|英|access_and_protocol_review.md|论文前2页，非全文|
|S21|Alinur|英|practice_and_completion_audit.md|短俄语自述实验，原始材料私有|
|OV01|Anthropic|英|video_text_review.md|全文镜像，原轨未核|
|OV02|Anthropic|英|video_text_review.md|另一原片，同机构|
|OV03|Talking Postgres/Simon Willison|英|video_text_review.md|官方逐字稿，Microsoft赞助|

24是文档/案例证据组数，不是24个独立发布主体、效果试验或全文阅读来源。部分仅读相关正文；S3多URL仍只算1组。若剔除两字幕镜像，仍有22组正文登记。中文6（S1/6/7/8/10/11），英文18；语言数量不证明中文产品适配。

主体保守列至少12个：腾讯、Microsoft、Scribbl、Spellit、Teemo、Notion、Crossing、AP、OCUL、AlphaSense、Cleric、PTSEM。腾讯三页只计一个；微软客户故事不拆成多个独立发布机构。作者独立于彼此不等于独立于商业推广，S10资格仍待裁定。暂不靠S5未登记作者及S11身份补机构数量。

一手来源保守8组：S1、S2、S7、S8、S9、S12、S13、S20；一手是材料来源性质，不是结论可信度或效果验证等级。

## 门槛核验

|门槛|现有证据|裁决|
|---|---|---|
|15正文/8主体|24组登记、保守12主体|数量覆盖；逐条元数据仍有发布日期/作者缺项|
|4渠道|官方/论文、GitHub、中文媒体/社区三类明确；YouTube文字承载为镜像2及官方节目稿1|第四类按视频文字计入的资格待独立审查；不靠厂商博客域名凑数|
|中英各3|中文6、英文18|数量覆盖|
|4一手|保守8组|数量覆盖|
|6独立实践|S6/10/12/13/20/21|6份外部实践登记，S10商业关系和S21原始证据限制使严格资格待审|
|2失败/限制|S3协议偏差、S13幻觉/语言问题、S21运行不稳定|材料覆盖；不外推普遍错误率|
|3完整视频内容|完整文字3份，官方1、镜像2，原片播放0|镜像原轨未核，严格门槛待审|
|两平台各5候选|tool_verification.md及此前候选日志|各5条以上，作者日期热度多未知；不能冒称全平台Top|
|3条可行路线|scenario_menu.md A/B/C及tool_verification.md|三路线概念比较已交；账号、许可、导出与中文效果未全部验证|
|主推项官方核验+2实践+负面检索|分散台账|无一个工具满足全部主推证据，维持条件候选|
|两次独立执行及人工基线|file_demo仅当前聊天一次；概念题另有两聊天输出|办公产品0/2，无真人基线；概念答题不挪用为办公产品测试|
|独立反证审查|methodology/review_round_01/audit_report.md|早期包已审，未覆盖后续全部24组；最终复审待|

## 交付现状实查

- scenario_menu.md重新计数20行，六个短名单具输入、输出、价值假设、路线和资料边界。
- company_cases.md六项短名单已有组织实例；末段补齐早期三项空白，读者应以补齐段为当前状态。
- file_demo两输入、提示、Markdown和JSON输出、执行记录齐全。本轮重新核对采购未批、报价未分工、日期更新、报告期限、会议室待定、网络仅假设六项。4份哈希重算均与记录一致。
- JSON中的报价收集项owner/due为null，正确表达未分工；不得在演示时说已指派。待办JSON并不单独承载全部会议事实，需要与简报一起交付。
- 旧示范由同Agent编题作答、无人工基线，其34.8秒包含工具调度，不能计算提效百分比。
- 本页、菜单、比较和示范均通过共享任务review提交主对话。阶段提交不等于最终验收。

整体未达到最终工具推荐门槛；当前可审阅的是有明确限制的教学研究包。需要的外部条件仍包括可用且获准的办公产品测试入口、真实人工同任务基线，以及另一聊天对新增证据的独立裁决。
