# 入口矩阵（2026-11-09）

|路线|当前实际证据|账号/套餐|输出能力|下一动作|
|---|---|---|---|---|
|Codex 当前聊天|文件读写与工具已运行|套餐和精确模型未知|本轮尚未正式生成测试交付|隔离执行方式待定，不把本聊天自检算独立盲测|
|ChatGPT Web/Work|已读官方web文档相关正文；应用清单中ChatGPT实际ID为OpenAI.Codex|网页版登录未核|官方描述文档与表格，非本地验证|恢复浏览器后核验|
|WorkBuddy|官方候选workbuddy.ai/docs/zh打开无可读正文|未核|未核|从官方主页确认入口，不使用相似域名登录|
|Microsoft 365 Copilot|本轮未检查入口|未核|未核|核对官方及实际账号|
|Claude Cowork|项目办公议题明确历史无账号|不重复申请|本轮未测|优先其他可测路线|

界面证据：cua.getState 返回 browsers=[]；原生Edge存在三个窗口。对窗口263566和2099242的getApp均返回：window is minimized; call activate_window, refresh with get_window, then retry get_window_state。当前公开cua API没有这两个方法，未猜测调用。已请求用户恢复窗口；这只证明自动化读取阻塞，不证明产品不可用。未读取凭据，未提交测试提示。

## 最新入口核验与阶段裁决
WorkBuddy国内官方FirstTask/Results/Pricing已实际读取，纠正上表早期“未核”文档状态；账号和输出仍未核。Microsoft Copilot Chat/Cowork官方入门已读；Cowork有许可、启用与按量计费前提，未开通。最新浏览器URL识别被策略停止，详见access_failures/browser_access.md。产品实际运行仍0。

其他路线实际推进：11月12日打开WorkBuddy官网，点击可见“在线使用 WorkBuddy”进入/app登录跳转。登录页实际显示微信扫码，以及企业微信/手机号/SSO/QQ/邮箱方式；尚未登录或提交任务。官网有在线入口，当前无需先安装客户端来核验网页路线。登录页注明同意协议，未代用户接受。测试仍0。
