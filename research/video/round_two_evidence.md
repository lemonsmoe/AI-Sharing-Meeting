# 第二轮反证与访问记录

访问日统一2026-11-06。此轮采用ai-workflow-research技能；仅下面实际读取内容计证据，搜索结果不计。与first_findings合并去重后仍不足最终门槛。

|ID/来源|作者、发布日期、语言、渠道|实际读取范围与依据|裁决、推广与局限|
|---|---|---|---|
|V06 https://www.remotion.dev/docs/gl-options|Remotion，日期未知，英文，官方|渲染器说明，特别是Using the GPU段；angle可能内存泄漏，建议长渲染分段|限制证据；官方产品方。不是所有配置必然失败，按版本核查|
|V07 https://github.com/remotion-dev/remotion/issues/11283|JonnyBurger转述vel_from_activesnap，2026-09-14，英文，开发社区|问题正文及10月7日至8日评论；用户报告版本升级内存增加，维护者指出管线与配置控制不足，未复现数值，最终关闭|实践组activesnap，一组；不可把关闭解读成已修复，也不可断言确定回归。公开身份未额外认证|
|V08 https://2021.ubucon.asia/sessions/automating_boring_and_repetitive_ubucon_asia_video_and_subtitle_stuffs/Ubucon_Subtitle_Automate.pdf|Youngbin Han，2021，英文，原始会议资料|文本读取第23—39页：参数化片头、长视频缓冲/耗时问题、改为短片头加FFmpeg拼接、CJK字体与字幕人工校对|独立实践组ubucon2021；历史技术限制不可当2026版本现状，支持分段合成的工程动机。非原视频审阅|
|V09 https://www.blotato.com/blog/make-ai-videos-with-claude-code|Sabrina Ramonov，2026-05-22，英文，作者教程|工具栈、安装、分镜先审再渲染及发布段落|实践组sabrina；作者明确拥有Blotato，强商业推广。其Remotion完全免费说法忽略企业许可，不采纳；Skill不是渲染引擎本体，不采纳混用术语|

## 主动负面检索

检索词：site.github.com remotion issue rendering font memory。结果按搜索服务默认相关性排序，无自称全平台排名。V06、V07、V08构成失败/限制证据；结论是需要验证渲染配置与分段策略，不是认定工具不可用。

## 视频线索与访问层级

检索词：site.youtube.com Remotion AI video tutorial；site.bilibili.com AI 科普 视频 Remotion；默认相关性，非播放排序。

|平台/候选|可见指标|访问层级|下一步|
|---|---|---|---|
|B站 BV1xFnt6zE3K，Ploto教程|未知|原页412；配套文章前半|需可读原视频/完整字幕|
|B站 BV16Mbi6yE25，AI Agent一条命令自动做视频|未知|搜索摘要|待读取，不计来源|
|YouTube 4N_TfYVNM7k，Chase AI|Glasp页面显示30.6K views，非YouTube实时核验|Glasp仅提供字幕开头；Read More返回Cache miss|不能计完整字幕|
|YouTube 9PwpJpJJ3IY，Kevin Stratvert|未知|第三方搜索摘要和章节|待原页核验|
|YouTube f393grXJn9E，Full Remotion Tutorial|未知|第三方搜索摘要|作者与原页待核验|
|YouTube t9M38QMcUSA|未知|第三方搜索摘要|不采纳标题模型能力主张|
|YouTube Fp4FnEMj7QI|未知|第三方搜索摘要|待原页核验|

第三方字幕入口：https://glasp.co/youtube/4N_TfYVNM7k 。只读取页面摘要和字幕开头，不能称观看；作为线索不计独立技术依据。

## 主张裁决

- 代码动画可精确控制本例的时间与字幕：本地72秒样片支持，仅限本例。
- 一句话可稳定产出高质量长片：证据不足；作者个案和宣传不能证明。
- 企业内Remotion使用必然免费：不成立，官方许可按组织条件区分。
- 混合流程具有工程可行性：V08支持历史实际案例，当前环境尚需实测。
- 重跑同一源码等于第二次独立AI创作：不成立；本轮仅做渲染复现，不充抵独立创作门槛。

## 官方启动流程补核

V10：https://www.remotion.dev/docs/ai/coding-agents ，Remotion，更新2026-11-05，访问2026-11-06，英文官方文档。实际读取Prerequisites至Start your coding agent：需要Node.js及编程Agent，先创建项目、安装Skill、启动预览。官方明确多数Agent需订阅；不能把渲染框架许可与Agent账单混为一谈。同机构Remotion组，不增加独立作者数；本地未执行Remotion路线。
