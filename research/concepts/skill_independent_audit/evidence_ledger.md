# 证据台账（先登记，再裁决）

访问日期均为2026-11-06；语言英文。来源范围仅FFmpeg官方，不构成多机构独立验证。

| ID | URL / 原作者 | 发布日 | 实际阅读位置 | 核心依据与关系 | 推广与局限 | 重复组 / 实例 |
|---|---|---|---|---|---|---|
| E1 | [FFmpeg官方filters.texi](https://raw.githubusercontent.com/FFmpeg/FFmpeg/master/doc/filters.texi)；FFmpeg项目 | 动态master文档，无单独署期；未固定提交版 | loudnorm节，当次行5481—5537；ebur128开篇30479—30497；补读peak true参数30542—30560 | loudnorm支持单次/双次、动态/线性；I、TP、LRA参数存在。线性模式有测量和范围条件；dual_mono涉及播放情境；支持输出统计。ebur128可分析响度。 | 可解释参数及测量能力；不代表本地安装版本、输出达标或完整音画质量。 | ffmpeg_filters；无独立实践实例 |
| E2 | [FFmpeg官方af_loudnorm.c](https://raw.githubusercontent.com/FFmpeg/FFmpeg/master/libavfilter/af_loudnorm.c)；文件版权署名Kyle Swanson，FFmpeg项目维护 | 文件版权2016，不视为当前版本发布时间；动态master | 开头署名；init及输出测量行738—788、统计字段806—845 | 线性模式按条件进入；输出统计分别计算并报告输出I/TP/LRA、实际模式和目标偏差，支持区分设定值与观测值。 | 与E1同一项目，不另算独立作者或实践。 | ffmpeg_loudnorm_implementation；无独立实践实例 |

## 未计有效正文的访问

- ffmpeg.org/ffmpeg-filters.html#loudnorm及www镜像：打开超时。搜索返回了参数节，但搜索摘要不单独计入已读证据。
- ffmpeg.org/pipermail/ffmpeg-cvslog/2020-January/120713.html及www镜像：超时/Cache miss；未读正文，不采用其中更新细节。
- www.ffmpeg.org/doxygen/trunk/af__loudnorm_8c_source.html：超时；改用同项目仓库源文件，不算新增独立来源。
- 搜索命中的邮件列表问答及其他版本Doxygen未进一步打开，不计独立失败案例。未检索/观看视频，视频内容数量为0。

阅读源选择说明：第一方网站访问失败后改用官方仓库原文；并非用搜索摘要假装正文。文档HTML、仓库源和搜索转载同属FFmpeg材料，不能按URL数累加独立性。
