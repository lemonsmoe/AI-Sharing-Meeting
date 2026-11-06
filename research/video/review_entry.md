# 视频方向审阅入口

状态：阶段交付待审；总目标active。此页不宣称研究门槛通过。

## 当前优先入口（2026-11-06更新）

- [72秒中文旁白、单层字幕V3](../../videos/experiments/caption_candidate_01/meeting_captioned.mp4)：主对话已接受字幕候选，完整试听与动态审片仍待完成。
- [第28页三路线、费用与案例稿](v3_route_brief.md)：最新官方计费口径及约90秒口语，企业用途建议与公开案例分开。
- [新版完整审阅包](../../videos/experiments/delivery_bundle_02/teaching_video_v3_review.zip)：含最新路线稿；旧包保留。

以下为历史阶段记录，“最新V2”等措辞对应当时交付，不代表当前优先版本。

## 请先看成片

- 最新：[72秒视觉解释V2](../../videos/experiments/explainer_v2_reviewed/meeting_explainer.mp4)
- [18帧接触表](../../videos/experiments/explainer_v2_reviewed/contact_sheet.png)
- [编码与运行证据](../../videos/experiments/explainer_v2_reviewed/render_report.json)

内容：模拟会议原句→字段提取→误写承诺→回到原文修正→未知预算保留→可追踪任务表。无旁白，无音乐。素材全部为本项目原创图形及模拟文本。

## 再看制作与研究

- [脚本与分镜](next_animation_brief.md)
- [可复用生产手册](production_playbook.md)
- [原始源码](../../scripts/video/render_explainer.py)
- [三路线与成本初稿](first_findings.md)
- [反证与视频访问记录](round_two_evidence.md)
- [指定文章长片阅读记录](reference_longform_notes.md)
- [修订与检查](explainer_v2_review.md)

## 逐项验收现状

|要求|证据与当前状态|
|---|---|
|60—90秒可播放样片|72秒H.264，1728帧完整解码；有原始文件|
|视觉解释而非纯字幕卡|便签进入、提取连线、错误划线与修正、任务表逐行呈现；已抽检18帧|
|脚本分镜源码|已提供，可复现运行；依赖及Windows字体限制已写明|
|工具成本比较|三路线候选已列；官方定价与本地成本分开；未全部实测|
|参考文章|正文至长片总结已读；配套视频未观看|
|完整动态审片|未完成；抽帧和解码不能代替完整播放判断|
|研究门槛|未通过；来源、完整视频、独立实测及审查不足|
|两次独立制作|未达；V1→V2属于同一任务迭代，同源码重跑仅为渲染复现|
|独立反证审查|作者自查已做；另一聊天审查未完成|

建议主对话先审教学可理解性及节奏，研究结论继续标候选，不将本样片解码通过解释为所有工具或长期生产能力验收。

## 旁白合成版（主对话制作，2026-11-06读取）

[72秒带旁白版](../../videos/narrated_review/meeting_narrated_v1/meeting_explainer_narrated.mp4)已存在；本聊天独立完整解码和视频数据哈希检查通过。重要：同名SRT默认叠加会遮挡已烧录摘要，修订建议及实际截图见[narrated_audit/review.md](narrated_audit/review.md)。未完整试听、未动态审片，不能把此链接理解为最终验收。

## 完整生产链复现

[narrated_reproduction.md](narrated_reproduction.md)提供实际执行的画面、语音、封装三条命令；已在独立目录生成与原旁白版哈希相同的MP4。已知字幕问题仍在，复现不等于验收或独立创作。

## 字幕修订候选（优先审阅）

[72秒单层字幕旁白候选](../../videos/experiments/caption_candidate_01/meeting_captioned.mp4)：解决原旁白版的SRT遮挡与标点断行，六段编码后截图已查看，音轨保持不变。详见[检查与复现](caption_candidate_review.md)。仍待完整试听和动态审片，不作为最终验收。

## 集中交付包

[teaching_video_v3_review.zip](../../videos/experiments/delivery_bundle_01/teaching_video_v3_review.zip)：23个条目、2,068,954字节，包含V3、六段截图、分镜、旁白输入、成本表、四个制作源码、依赖版本、复现说明及manifest。全部ZIP条目按源字节核对通过，详见同目录bundle_check.json。全新环境安装未验证；完整音画及研究门槛仍未验收。
