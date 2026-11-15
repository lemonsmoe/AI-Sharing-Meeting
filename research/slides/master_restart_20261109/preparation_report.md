# Master 三页制作准备

2026-11-09，任务 TASK-20261109-c04184fb。仅恢复本轮准备，旧 WPS 与视频任务未续跑。旧目标工具状态仍为 paused，未宣称恢复或替换。

## 路线与已执行

使用用户选定的 PPT Master 6.9.0，attribution_guard 返回 0。按 routing 选择普通 Default Generate，不是 Beautify、Quick 或模板制作。已创建 slides/master_restart_20261109/master_preview_20261109，并通过 import-sources 归档主对话 three_page_brief.md。未生成页面、设计规范、锁或用户确认回执。

## 真实参考

- https://hugohe3.github.io/ppt-master-examples/viewer.html?project=ppt169_what_is_ppt ：索引17页，实际下载并渲染查看第10页“原生对象模型”。左侧说明与右侧大型拆解图对应，细网格、线条和单一红色焦点服务结构表达。借鉴图文对应与视觉主次；不把其层级结构移植为Agent组件关系。
- https://hugohe3.github.io/ppt-master-examples/viewer.html?project=ppt169_infosec_training_zh_long ：索引28页，实际下载并渲染查看第11页“钓鱼邮件”。左侧示例原文、右侧编号解释，暖纸底与细线组织信息。可借鉴提示词逐段批注、事实表格局部注释。未审阅其余页面或验证案例内安全法律主张。

实际SVG与PNG保存在 references/。网页工具读取失败，改用公开站点HTML与其 examples/examples.json 定位原始SVG；没有把索引描述当作目检。

## 依赖与边界

默认 Anaconda Python 的 project_manager 导入 openpyxl 时触发 Windows 注册表 PermissionError。改用 C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe 后，项目初始化与导入成功。该运行时已有 pptx、xlsxwriter、openpyxl、Pillow；任务内 runtime_dependencies 已安装 Flask、PyYAML、skia-pathops、uharfbuzz、resvg-py 及依赖。两张参考SVG经resvg实际渲染成功。后续命令需将该目录设为 PYTHONPATH。尚未证明正式SVG检查、原生PPTX导出、字体匹配或回存通过。

## 传播方案与正式下一步

传播目标：全体部门能把宽泛请求变成可验收任务，理解Agent组件配合，并检查结果来源、变更和未知。三页分别承担提示词批注、协作关系解释、真实行动表核验；主屏讲重点，备注承载解释。16:9建议，中文现场讲述，三页试做后才考虑全稿。

建议自由设计：两套案例是视觉参考，未被选为本地模板工作区。Stage 1推荐已保存 confirm_ui/recommendations.stage1.json，已知受众与时长预填；content_divergence留空。需要用户最少确认的是接受该传播目标和自由设计，或改选模板。

Skill workflows/generate-pptx.md Step 4明确要求“Stage 1 confirms the communication contract and exactly one template mode”；随后才能创作三个完整设计方向并进行Stage 2确认。因此目前不提前伪造三方向、design_spec或result.json。确认后将基于两套参考提供三种实质不同的表达方案，再按所选方案制作三页及备注、进行技术核验并交用户判断观感。

## 确认入口实测与交接事件
本地确认服务经受控提权启动成功，健康检查通过，系统接受浏览器打开请求。短时等待未取得提交，复查 result.json 和 template_selection.json 均不存在；已按Skill清理服务。当前改为聊天待确认上述相同内容，绝不把超时当确认。没有形成Stage 2。准备任务完成，正式设计须等待用户Stage 1回复。

