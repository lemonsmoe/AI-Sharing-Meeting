# 第28页：企业视频工具与自部署路线候选

核实日：2026-11-06。供主对话选用；不是采购推荐。所有云端账号、中文效果、公司网络和真实企业数据处理均未实测。

|路线/工具|适合讲什么|运行位置|成本口径|核验与实际状态|
|---|---|---|---|---|
|代码动画：Remotion|流程、图表、界面动效，可按模板参数化|本机/自建渲染服务；编程Agent可为云端|个人及≤3人公司满足条件可免费；企业Creators $25/席位/月；Automators $0.01/次渲染且最低$100/月；Agent、算力另计|已读官方许可和启动流程；未安装实测，不能套用本Python样片结果|
|录屏：OBS + 后期剪辑|真实软件操作、培训演示|本机录制|OBS免费开源；剪辑工具许可、人工、字幕另计|官方首页已读；未本机录屏试验|
|生成镜头：Runway|氛围、难拍摄素材，配合精确代码字幕|云端|Standard年付折合$12/月，625积分；不同模型每秒消耗不同，失败重试也需计入；非单条成片价格|官方价格页已读；未注册或生成，不证明中文教学效果|
|自部署：Python图形+FFmpeg|规范流程图解、重复模板短片|本地；可改为内部批量任务|无本次外部渲染调用；计算机、维护、Agent费用仍存在|本项目已跑72秒字幕样片；尚未部署服务器或完成独立复现验收|
|自部署候选：Manim Community|数学、几何与逐步推导|Python环境，官方亦提供Docker镜像路线|README标明MIT；依赖/字体另核，计算及开发人工另计|已读README示例、社区版区别、Docker与许可说明；未安装实测，不作为最终工具推荐|

## 已读来源

- Remotion：https://www.remotion.dev/docs/license/pricing ，License & Pricing及Creators/Automators段；https://www.remotion.dev/docs/ai/coding-agents ，前提、创建工程、预览步骤。
- OBS：https://obsproject.com/ ，Features及免费开源说明。
- Runway：https://runway.com/pricing ，Standard套餐和积分表。
- 本地实测：videos/experiments/explainer_v2_reviewed/render_report.json、scripts/video/render_explainer.py。
- Manim线索：https://github.com/ManimCommunity/manim 。Blender官方许可页本轮返回402，未据此下许可证结论。

## 幻灯片可直接使用的短句

“讲流程，用代码动画；教操作，用真实录屏；需要氛围镜头，再考虑生成视频。三条路线都要先审脚本、再看片；企业许可、模型调用和人工返工分开算。”

这段为Agent候选写法，主对话裁决。自部署渲染不等于模型推理也在本地；本样片由当前Agent辅助写代码，不能宣传成端到端离线AI。
