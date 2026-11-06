# 六实践资格校正：V07原始材料追溯

2026-11-06；TASK-20261106-045eb71d。依据最新方法审计开展窄补证；仅两轮检索，未改视频、V3或旧研究记录。原目标保持blocked，本任务不表示目标恢复。

## 结论

**未补到合格替代记录。V07不计直接独立实践。** 现有六候选应改记为：4组有署名的直接制作记录、1组匿名账户原始经验（条件计入）、1组维护者转述（排除直接实践计数）。因此可条件计5组，不能宣布六实践门槛通过。这里的计数不等于五组均已独立复现实测。

## 两轮查找与实际阅读

|轮次|检索／访问|结果|
|---|---|---|
|1|搜索 `"activesnap" "remotion" crash`，默认相关性排序；重读[GitHub #11283](https://github.com/remotion-dev/remotion/issues/11283)|搜索返回无关代码索引，不计来源。Issue明确写由JonnyBurger转发vel_from_activesnap的Discord消息，找到原消息链接。|
|2|打开[原Discord消息](https://discord.com/channels/809501355504959528/844143007183667220/1547285763815899227)；搜索 `"vel_from_activesnap" remotion`、`"activesnap" "Runtime.OutOfMemory"`|原消息返回Cache miss，未读正文；搜索只回到同一Issue，未取得独立作者原文、附件或原始测量日志。依两轮上限结束查找。|

GitHub实际读取范围：正文及全部可见评论，网页行126—332。作者JonnyBurger（维护者）；原消息署名vel_from_activesnap，现实身份未核。Issue发布2026-09-14，后续评论2026-10-07、10-08；访问2026-11-06；英文／开发社区；duplicate_group仍为activesnap，与V07合并，不新增来源。

可支持的窄事实：转述列出了AWS Lambda、Node 24、Remotion两个版本、媒体标签切换与补丁；但未见原始输入素材和测量日志。维护者指出管线切换带来混杂，并明确没有复现报告数值；关闭状态不证明修复。补丁及AI解释也不是原始测量。故保留为失败／方法限制证据，不升级直接用户实测。[Issue正文及评论](https://github.com/remotion-dev/remotion/issues/11283)

## 校正后的六组资格表

本表结合本轮V07追溯与既有已读记录；其余五组未在本轮重新访问，不刷新其证据日期。

|组|直接性与独立性|本轮资格|定位|
|---|---|---|---|
|Ploto|署名原作者制作自述；与工具厂商不同，未独立核验工时或成片|直接实践1组；不当效率对照实验|reference_longform_notes.md；V01|
|activesnap／V07|维护者转述；原Discord正文未取得|排除直接实践计数，保留限制线索|本页两轮记录；round_two_evidence.md|
|UbuCon／Youngbin Han|活动制作人的原始流程讲义，历史版本|直接实践1组；不推当前性能|round_two_evidence.md；V08|
|Griffith／Stephen So等|原始教学制作论文，含制作及反馈细节|直接实践1组；小样本反馈不当因果效果|teaching_sources.md；V17|
|Steven Phan|署名个人流程，公开源码和导出入口；服务推广可能保留|直接实践1组；没有本地执行其项目|independent_practice_addendum.md；V20|
|Reddit制作流程讨论|原账户经验及回复，现实身份和版本未知；全串只算1组|条件计1组，不称实名或受控版本实测|independent_practice_addendum.md；V19|

## 对旧记录的明确修正

- evidence_ledger.md及round_two_evidence.md中把activesnap纳入保守独立实践的历史计数，不再沿用。
- independent_practice_addendum.md的“6候选”只表示六条待审线索，不代表六个合格直接实践；其“5或更少”以本页4＋1条件组的具体拆分为准。
- 总来源组仍20，本轮新增有效来源0；完整视频文字数量不变。GitHub重复返回和不可读Discord不增加来源数量。
- 本轮交付为明确失败及资格纠正；没有证明Remotion确定回归，也没有完成新独立创作、人工基线或完整音画验收。既有研究结论继续为条件候选。
