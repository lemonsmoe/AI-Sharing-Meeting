# 30 页扩稿任务书（2026-11-16 凌晨）

状态：备料完成，**待用户确认后开工**。本文把确认过的顺序、设计规范、素材、备注与验收整合成一份可直接执行的制作任务书，供本 Agent 或制作对话使用。

## 一、输入文件（按优先级）

| 用途 | 文件 |
|---|---|
| 页序、页题、秒数、画面要求 | [outline.md](outline.md) |
| 照读稿（正文权威） | [speaker_script.md](speaker_script.md)（口语修订版） |
| 逐页讲者备注（已去操作提示） | [speaker_notes_per_page.json](speaker_notes_per_page.json) |
| 设计规范与用户确认 | [confirmed_brief.md](../swiss_revision_20261115/confirmed_brief.md) |
| 素材与核对边界 | [asset_checklist_20261116.md](asset_checklist_20261116.md)、[source_map.md](source_map.md) |
| 引语原文、署名与照片 | [quote_sources.md](../swiss_revision_20261115/quote_sources.md) |
| 三页样稿（风格基准） | `slides/swiss_preview_20261115/exports/swiss_preview_20261115_231045.pptx` 及 `preview/*.png` |

## 二、视觉规范（沿用三页样稿，未经新一轮用户确认不得改）

- 底：公司模板 `slides/赛感PPT优化丰富版本.pptx`；参考 Swiss Grid `assets/references/swiss_grid_systems.pptx` 的网格与留白。
- 色：黑（正文）、米白（底）、红（重点）；照片天然色不计。
- 字体：微软雅黑单一字体；三档字号 18 / 24 / 43.5 pt。
- 无左下角固定小字标题；少文字、多真实图片与界面；每页主屏一句话能读懂。
- 人物页：照片在左，英文原话在上、中文自译在下，署名与出处写进备注。

## 三、制作路线

- Generate PPTX（Default），PPT Master 6.9.0（`.context_runtime/ppt_skill_candidates/ppt_master`），attribution_guard 已通过（exit 0）。
- 环境：`.context_runtime/ppt_master_env/Scripts/python.exe`（3.12.13）；不动 ComfyUI 环境。
- 先做 3 页对照样稿复核风格延续性（可复用 swiss_preview 三页），再批量全 30 页。
- 导出后：`verify_pptx.py` 同流程检查原生元素；本机 PowerPoint 渲染逐页 PNG 并实际看图；备注与 speaker_notes_per_page.json 逐页对齐。

## 四、素材占位与替换规则

- 已有：三页样稿缩略图、Peter 照片（quote_assets）、黄仁勋官方头像 1920px（assets/screenshots/20261116/nvidia_bio/）、12 款产品图标（assets/icons/20261116/）、WorkBuddy 官方教程图 14 张（assets/screenshots/20261116/workbuddy_first_task/）、表情包原件（assets/company_meme/）。
- **用户后补（占位框规则，2026-11-16 用户确认）**：不再由 Agent 本机截屏；第 17 页 Skill 文件夹截图、第 21 页 Codex 桌面端截图、第 7 页可选豆包界面，制作时放入带说明文字的占位框（如「此处放截图：Codex 桌面端」），用户拿到 PPTX 后自行替换图片。已截两张本机图仅作参考备选，不自动入成品。
- 教学示意页（05、08–16、18、19、22、24、28）用文字组件制作，标「教学示意」。
- 官方截图一律注明来源与抓取日期，不冒充实测。

## 五、未定项（不阻塞开工，按默认值推进，用户选定后替换）

1. 可选加料 A/B/C：用户已定——按用户自改版稿为准，不再使用旧 A/B/C。
2. 办公案例三选：用户新稿未含专门办公案例章节，按新稿执行；如后续想补再议。
3. 黄仁勋照片：默认用已下载官方头像，用户确认后上屏。
4. 分镜草案：见 `outline_user_edition.md`（29 页，1,970 秒），待用户确认后定稿。

## 六、验收清单（做完逐项打勾）

- [ ] 30 页齐全、页题与 outline.md 一致、无左下角固定小字
- [ ] 原生标题/表格/文字可选中编辑（PowerPoint 本机检查）
- [ ] 逐页备注 = speaker_notes_per_page.json 对应正文
- [ ] 每页本机 PowerPoint 渲染 PNG，逐张实际看图（无遮挡、无裁切、字号可读）
- [ ] 官方素材来源标注齐备；未实测边界未冒充
- [ ] 交付 SHA256 记录；真人试讲计时（预计 48 分钟，需本人执行）
- [ ] 现场设备打开测试（本人执行）

## 七、时间与分工

- 制作预算约 3 小时：3 页对照 30 分钟 → 批量 29 页 90 分钟 → 备注合稿 30 分钟 → 渲染检查与修订 30 分钟。
- 真人试讲、现场设备与表情包/截图替换由用户负责；视频制作继续暂缓。
