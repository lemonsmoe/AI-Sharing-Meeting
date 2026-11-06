# 企业/团队案例补充（访问2026-11-06）

以下是真实组织公开披露，不是本项目独立验证。金额/提效不外推公司环境。

|对应短名单|组织与输入|公开结果|限制与性质|来源|
|---|---|---|---|---|
|会议整理|Michigan Radio：公开市议会视频|转写、关键词检索、邮件提醒及原视频时间戳|维护需开发人员；来源格式分散；项目未完成摘要功能。AP项目报告，原始团队实践；不能说已自动生成会议纪要|https://www.ap.org/wp-content/uploads/2024/02/ap-local-ai-michigan-radio-oct-2023.pdf （25—62行）|
|销售跟进|Schneider Electric：客户邮件、日程、Teams与Salesforce|邮件摘要、联系人预填后由销售确认、工作流内更新CRM|官方客户故事，非独立因果验证；报道部署语种列表不能证明中文适配|https://www.microsoft.com/en/customers/story/18860-schneider-electric-microsoft-365-copilot-for-sales （36—56行）|
|制度问答|Lifetime Products：员工及主管手册|HR自助Agent回答休假累积及政策问题；客户称减少重复咨询|微软客户故事2026-08-26；采用阻力被明确披露；无公开问答准确率|https://www.microsoft.com/en/customers/story/27087-lifetime-products-microsoft-copilot-studio （39—68行）|
|制度知识准备（补充）|Kantar People Team：跨国多语言制度材料|用Agent定位、翻译、去重和整理，为HR顾问Agent准备内容|客户故事；减少HR咨询仍是预期，不能写成已实现结果|https://www.microsoft.com/en/customers/story/25674-kantar-microsoft-copilot-studio （38—67行）|
|表格异常核查|尚未获得直接匹配案例|Lifetime订单关闭自动化是邻近例子，不能替代表格异常检测|保持未证实|同上Lifetime，61—62行只支持订单流程自动化|
|公开竞品调研|尚未获得直接匹配案例|不把销售研究一句话当完整竞品案例|保持未证实|待补|
|研发问题复盘|尚未获得直接匹配案例|不把一般代码助手当故障复盘|保持未证实|待补|

## 补充来源登记
S12：AP/Michigan Radio，2023-10报告，英文原始项目案例；读25—62行及附录文字，未复算WER。输入和输出明确，含失败，独立实践新增1。
S13：OCUL，2026-02 FAQ，英文原始图书馆团队项目；读全文37行。已运行集中转写流程，但需升级硬件、调参及校对；存在幻觉和非英语问题。https://ocul.on.ca/sites/default/public/2026-02/OCUL_AIML_AudioTextProject_FAQ_20260219.pdf 。独立实践新增1。
S14：Schneider/Microsoft客户故事；读36—56行，发布日期待登记；厂商推广高，独立效果不计。
S15：Kantar/Microsoft客户故事；读38—67行，发布日期待登记；厂商推广高，独立效果不计。
S16：Lifetime/Microsoft客户故事；2026-08-26；读4—68行，厂商推广高，独立效果不计。

累计正文16，但新增微软故事不增加独立发布机构。独立实践保守4（Teemo、Crossing、Michigan Radio、OCUL）；完整视频0；两次独立产品执行0。AP/OCUL为组织实践，不是企业商业成功案例。Atla论文和Reddit返回正文被截断，暂未列有效新来源。公开测试原始脚本网页与raw地址均Cache miss；PowerShell请求受本地网络权限阻断，未下载未复算。

## 六项短名单补齐记录（2026-11-06）
以下补充取代上表三项“尚未获得案例”的当前状态；保留上表作为研究过程记录。均为厂商客户自述，不计独立验证。

|短名单|公司/输入|实际公开结果|限制与适配边界|来源|
|---|---|---|---|---|
|竞品调研|Siemens Market Intelligence，跟踪同行、并购和行业趋势的月度领导报告；互联网及付费券商研究|Bob Nelson团队用公司观察列表、时间过滤、提醒与AI自然语言搜索，减少低质量提醒筛选，取得更多相关材料|AlphaSense客户故事，发布日期未标；含付费研究，不等于免费公开网页方案，也未证明生成式Agent自主写完整报告。无公开漏报率或独立计时|https://www.alpha-sense.com/resources/case-studies/siemens/ ，正文20—35行；S17|
|表格核查/对账|U.S. AutoForce（U.S. Venture部门），信用卡交易与银行账单|已部署Copilot for Finance处理两类对账；客户称四周完成设置、每月节省30多小时|微软客户故事，发布日期待核；金额匹配细节和误差未公开。对账是异常核查的具体子场景，不能推广成任意表格自动准确。供应商账单处理在文中仍属下一步|https://www.microsoft.com/en/customers/story/20600-us-venture-microsoft-365-copilot-for-finance ，35—50行；S18|
|研发故障复盘/调查|Mixmax，生产告警与支持工单，付费账号误判免费账号事故|Cleric持续调查并更新假设，最终归因为计算资源不足导致权限检查超时；工程师核验分析后用其他工具修复|Cleric客户故事，日期未标；客户称平均恢复从39小时降至4小时内，非随机对照。完全自动修复仍是计划。覆盖生产软件故障，不能外推硬件根因或运动控制|https://cleric.ai/resources/case-studies/how-mixmax-reduced-incident-resolution-time-by-90-percent-with-cleric ，24—43、71—98行；S19|

三例访问日均11-06；语言英文；渠道官方客户故事，推广可能高；独立证据组分别siemens_alphasense、us_autoforce_finance、mixmax_cleric。正文来源累计19，严谨独立实践仍4，不因客户故事增至7。六项已有可追溯组织实践，其中竞品调研、表格核查和研发复盘的具体适用范围如上。
