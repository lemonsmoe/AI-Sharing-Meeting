# 三套候选准备状态

2026-11-09。按用户“先三种都准备好”的要求，使用官方 skill-installer 的下载脚本，把三个上游 Skill 放入项目独立目录；没有修改全局 Skill 列表。用户随后已选 PPT Master，只有它进入后续制作准备。

|候选|项目内入口|状态|
|---|---|---|
|PPT Master 6.9.0|.context_runtime/ppt_skill_candidates/ppt_master/SKILL.md|下载完成；attribution_guard.py 退出 0；已读默认 Generate 路线及确认步骤|
|Guizang|.context_runtime/ppt_skill_candidates/guizang_ppt/SKILL.md|下载完成，收藏备用；不运行本次生成|
|Dashi 0.4.14|.context_runtime/ppt_skill_candidates/dashi_ppt/SKILL.md|下载完成，本次不使用|

快照摘要见 candidate_snapshot.json，登记入口 SHA256、文件数与内容树摘要。下载请求针对 main，未取得可信提交 SHA，因此不能把摘要说成锁定了上游 commit。临时副本不进入 Git；比较、入口与恢复依据保存在 research/selection_20261109。换机器可重新下载并核对版本与摘要，后续要精确重建需按 commit 固定来源。

本机已发现 Python 3.12.3、Node 24.14.0、npm 11.9.0。准备副本本身未安装三套全部依赖，也未完成任何三路生成比较。Master 的最小运行环境与项目初始化由子对话 4 在独立任务目录推进；其实际安装与执行以 research/slides/master_restart_20261109/preparation_report.md 为准，不套用这张准备表宣称全部依赖通过。

使用时显式读取选定 SKILL.md 即可，不依赖全局自动发现。这里的“准备好”指文件和入口已就绪，不是三套都已做出通过审美验收的 PPT。
