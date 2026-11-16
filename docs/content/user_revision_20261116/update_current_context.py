from pathlib import Path
root=Path(__file__).resolve().parents[3]
latest='''**2026-11-16最新28页修订补图版（自主验收完成）**：用户批准逐页修改，并在休息前允许缺图留位、要求新目标模式及全新Agent多轮验收。已交付 `slides/projects/user_revision_ppt169_20261116/exports/AI分享_28页修订补图版_20261116.pptx` 与 `docs/content/user_revision_20261116/speaker_script.md`；28页备注完全同步，18页含图片。原P27删除、原P28/P29顺延；原P3与末页原生图像素一致。三个全新Agent分别做视觉、讲稿、事实两轮审核，修改了首轮发现的编号、截图、图文证据与Skill前提等问题后复核通过；PowerPoint原生渲染、可编辑标题保存重开和哈希核验通过。仅留用户明确允许的P8上下文附件、P22最初任务输入、P23Codex调用Skill三个截图位；演示附件和替换说明已备。**接手入口：`docs/content/user_revision_20261116/早上从这里开始.md`**；详细记录与来源在同目录。上午补图、删除占位、现场放映与试讲；未真人计时。旧29页与用户稿保留，视频未恢复，本轮未Git提交/推送。'''
index=root/'docs/context/00_current/index.md'
s=index.read_text(encoding='utf-8-sig')
marker='## 当前成果与下一步\n'
if '最新28页修订补图版（自主验收完成）' not in s:
    s=s.replace(marker,marker+'\n- '+latest+'\n\n以下为此前阶段记录，最新交付以上述28页版为准。\n',1)
s=s.replace('**2026-11-16当前29页审阅**','**2026-11-16此前29页审阅**')
index.write_text(s,encoding='utf-8')
domain=root/'docs/context/00_current/domains/content.md'
s=domain.read_text(encoding='utf-8-sig')
if '最新28页修订补图版（自主验收完成）' not in s:
    s=s.replace('# 分享内容状态\n','# 分享内容状态\n\n## 当前：28页修订补图版与两轮自主验收\n\n'+latest+'\n\n最新事件：`evt_user_revision_20261116`。下方为历史阶段，不再据其“待讨论/制作暂停”描述阻断本轮已授权交付。\n',1)
domain.write_text(s,encoding='utf-8')
print('Updated main index and content domain')
