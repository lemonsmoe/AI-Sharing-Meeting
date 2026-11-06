"""整理可离线打开的审阅包；原始研究与旧成果保持原位。"""
import hashlib
import html
import json
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[3]
bundle = root / 'outputs/leadership_review_v3'
evidence = root / 'research/integration/v3'
evidence.mkdir(parents=True, exist_ok=True)


def copy_file(source, target):
    target = bundle / target
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / source, target)


def write_file(name, content):
    target = bundle / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')


file_map = {
    'docs/content/rehearsal_script_v3.md': 'materials/rehearsal_script_v3.md',
    'outputs/leadership_review_v2/materials/task_card.md': 'materials/task_card.md',
    'research/office/scenario_menu.md': 'materials/scenario_menu.md',
    'docs/content/office_case_cards.md': 'materials/office_case_cards.md',
    'tutorials/office/meeting_demo.md': 'materials/meeting_demo.md',
    'research/concepts/history_addendum/history_brief.md': 'materials/history_brief.md',
    'research/concepts/history_addendum/source_register.md': 'materials/history_sources.md',
    'research/methodology/tool_landscape/comparison.md': 'materials/tool_comparison.md',
    'research/methodology/tool_landscape/tutorials.md': 'materials/tool_tutorials.md',
    'research/methodology/tool_landscape/source_ledger.md': 'materials/tool_sources.md',
    'research/methodology/tool_landscape/tools.json': 'materials/tools.json',
    'research/methodology/tool_landscape/screen_pages.md': 'materials/tool_screen_pages.md',
    'research/methodology/concepts_trial_02/run_manifest.md': 'materials/trial_02_manifest.md',
    'research/slides/native_powerpoint_check.md': 'materials/native_powerpoint_check.md',
    'research/video/v3_route_brief.md': 'materials/video_routes.md',
    'videos/experiments/caption_candidate_01/meeting_captioned.mp4': 'media/meeting_captioned.mp4',
    'videos/narrated_review/narration_segments_v2.json': 'materials/narration_segments.json',
    'slides/templates/sycsense_reference.pptx': 'materials/production_examples/reference_template.pptx',
    'slides/experiments/output/weekly_report_sample_v1.pptx': 'materials/production_examples/weekly_report_sample.pptx',
    'outputs/leadership_review/leadership_review_v1.pptx': 'materials/production_examples/content_v1.pptx',
    'docs/content/slides_content_v1.json': 'materials/production_examples/slides_content_v1.json',
}
for source, target in file_map.items():
    copy_file(source, target)
for source in (root / 'tutorials/office/file_demo').rglob('*'):
    if source.is_file() and source.suffix in {'.md', '.txt', '.json'}:
        copy_file(source.relative_to(root), 'materials/file_demo/' + source.relative_to(root / 'tutorials/office/file_demo').as_posix())
for number in range(1, 31):
    name = f'slide_{number:02d}.png'
    copy_file('slides/review_v3/native_validation/' + name, 'preview/' + name)

replacements = {
    '../concepts_trial_02/run_manifest.md': 'trial_02_manifest.md',
    '../../../tutorials/office/file_demo/execution_record.md': 'file_demo/execution_record.md',
    '../../slides/native_powerpoint_check.md': 'native_powerpoint_check.md',
    'screen_pages.md': 'tool_screen_pages.md', 'tutorials.md': 'tool_tutorials.md',
    'source_ledger.md': 'tool_sources.md', 'source_register.md': 'history_sources.md',
    '../../research/office/scenario_menu.md': 'scenario_menu.md',
}
for name in ['tool_comparison.md', 'tool_tutorials.md', 'history_brief.md', 'office_case_cards.md']:
    target = bundle / 'materials' / name
    content = target.read_text(encoding='utf-8')
    for old, new in replacements.items():
        content = content.replace('](' + old + ')', '](' + new + ')')
    target.write_text(content, encoding='utf-8')

write_file('materials/spreadsheet_guide.md', '''# 会议文件到可编辑Excel

打开 [原始会议记录](file_demo/input/meeting_notes.txt)、[会后补充](file_demo/input/follow_up.txt)，再看 [会议行动表](meeting_actions.xlsx)。材料为模拟会议，未接入公司系统。

现场用约2分钟展示：给材料 → 指定交付字段 → 打开结果 → 对照原文。不要把生成器代码讲成普通用户必须掌握的步骤。

可复制的要求：读取两份文件，交付可编辑Excel；分开行动、已确认变更和未决信息；给来源编号；未知负责人和日期保持空白并提示；保留原件，不发送消息。

本表包含2个行动项、4条决定或未决信息。测试报告为11月9日18:00，演示改到11月12日；采购尚未批准，网络只是未确认的假设。填写负责人不代表期限也已确定。

V3副本将两个日期单元格改为Excel日期序号，沿用当地钟表时间。2026-11-06在Microsoft Excel 16.0读取显示、修改独立副本文字并保存重开通过；原文件不变。尚需在分享现场设备检查，未宣称WPS已测。

本次由Codex读取和整理材料，文件工具生成工作簿；不代表WorkBuddy、Copilot或WPS AI实测。项目生成源码保留在 tutorials/office/spreadsheet_demo 与 scripts/slides/review_deck_v3；本包供审阅，不包含完整运行环境。
''')
write_file('materials/video_production.md', '''# 72秒会议整理讲解视频

[播放样片](../media/meeting_captioned.mp4)。本包采用中文系统旁白和单层完整字幕版。使用原创模拟会议，画面里的错误草稿是教学示例，不是某产品真实错误录像。

已完成：1280×720、24fps、72秒视频；1728帧及音轨解码；六段字幕关键帧审阅；旁白未超过对应镜头。完整试听、动态同步和现场播放器检查仍待完成。

制作链：拆分概念和原文 → 写六段文案 → 用代码安排画面时间 → Windows Microsoft Huihui通用中文语音 → FFmpeg封装 → 用完整字幕替换旧摘要区。没有声音克隆。

保留的返工：初稿有三段旁白超过镜头，缩短文字后重新合成；同名外挂SRT曾遮挡原摘要，最终视频只保留一层烧录字幕。本包不另放自动加载的同名SRT。

旁白与时段见 [分段文案](narration_segments.json)。三条制作路线、费用与案例见 [视频路线资料](video_routes.md)。源码保留在项目 scripts/video 及 videos/narrated_review；完整复现需要项目环境，本包未携带依赖。

既有源码独立目录复现的27.388秒，只包含画面、语音和封装三条命令，不包含创作、安装、修改和审片。本地系统语音及渲染未调用外部付费API；AI助手账单、设备和人工总成本未计，不称总成本为零。
''')
write_file('materials/review_status.md', '''# 当前版本与使用范围

2026-11-06，内部内容审阅V3。30页主屏、30页讲稿备注与单独试讲稿同步；计划48分钟内容、5分钟问答、2分钟机动，未实际排练计时。

PPT正文和5张原生表格可编辑；截图仍是截图，Excel节选另附可编辑工作簿。Microsoft PowerPoint 16.0逐页导出30张预览，主对话全部查看；独立副本文字和表格修改后保存重开成功。旧四页样例的图表同步限制仍保留，不能由本稿0张原生图表推断图表已验证。

Excel已在本机原生应用核对日期及副本回存。PPT和Excel原件哈希保持一致。尚未完成WPS和分享现场设备检查。

工具地图是候选入口介绍。当前项目实际使用Codex和本地文件生成流程；其他工具的官方能力、公开案例和费用说明不等于本地实测，也不是企业采购或效果排名。

四包研究的最终主推门槛未全部通过，未据此写成普遍准确率、节时、ROI或免费保证。下一步优先补现场视频完整试听与整场计时，再按具体拟主推流程补产品测试。

价格核验日2026-11-06；具体购买前仍需重新核对账号、地区、套餐及权益。包内原始研究摘录的历史状态以本页为当前补充，不回写原始证据。
''')

write_file('readme.md', '''# 企业AI效率分享会 · V3审阅包

建议先打开 [统一入口](start_here.html)，也可直接打开 [30页PPT](leadership_review_v3.pptx)。网页入口完全本地，无需登录或联网。

- [逐页画面与讲稿](preview.html)
- [完整试讲稿](materials/rehearsal_script_v3.md)
- [72秒中文旁白样片](media/meeting_captioned.mp4)
- [可编辑Excel](materials/meeting_actions.xlsx) 与 [演示步骤](materials/spreadsheet_guide.md)
- [任务卡](materials/task_card.md)、[20个部门场景](materials/scenario_menu.md)、[公开组织案例](materials/office_case_cards.md)
- [工具地图与费用](materials/tool_comparison.md)、[试用步骤](materials/tool_tutorials.md)
- [用法演变](materials/history_brief.md)、[视频路线与成本](materials/video_routes.md)、[制作说明](materials/video_production.md)
- [本版状态](materials/review_status.md)

转移到另一台电脑时，请整体复制此文件夹或完整解压ZIP。视频为单独文件，在第27页切换到播放器；不要只复制PPT后假定视频已经嵌入。

主屏30页，内容计划48分钟，另留5分钟问答、2分钟机动。仍需完整试听和整场计时。最适合先审主线是否适合全员、场景是否有共鸣、演示能否看懂。
''')

css = '''body{font:18px/1.75 "Microsoft YaHei",sans-serif;color:#25282e;background:#f5f5f4;margin:0}main{max-width:1080px;margin:40px auto;padding:32px;background:white}h1{font-size:34px;color:#b60000}h2{font-size:24px;margin-top:36px}a{color:#a40000}nav{display:flex;gap:24px;flex-wrap:wrap;padding:12px 0}video,.slide{width:100%;height:auto}section{margin:36px 0}details{padding:12px 20px;background:#faf8f6}summary{cursor:pointer}p{margin:14px 0}.muted{color:#646870}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.8 "Microsoft YaHei",sans-serif}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:12px;text-align:left}@media(max-width:700px){main{margin:0;padding:20px}h1{font-size:28px}}'''


def page(title, body):
    return f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{css}</style><main>{body}</main></html>'


script = (bundle / 'materials/rehearsal_script_v3.md').read_text(encoding='utf-8')
sections = re.split(r'(?=^## \d{2}｜)', script, flags=re.M)[1:]
assert len(sections) == 30
preview = '<h1>逐页画面与讲稿</h1><p><a href="start_here.html">返回审阅入口</a> · 预览来自本机PowerPoint实际导出</p>'
for index, section in enumerate(sections, 1):
    title, body = section.split('\n', 1)
    if index == 30:
        body = body.split('## 排练记录模板')[0]
    preview += f'<section id="slide_{index:02d}"><h2>{html.escape(title.removeprefix("## "))}</h2><img class="slide" loading="lazy" src="preview/slide_{index:02d}.png" alt="第{index}页"><details><summary>展开本页讲稿</summary><pre>{html.escape(body.strip())}</pre></details></section>'
write_file('preview.html', page('V3逐页预览', preview))

main = '''<h1>把AI用进日常工作</h1><p class="muted">2026年11月16日分享 · 内部审阅V3 · 30页</p>
<nav><a href="leadership_review_v3.pptx">打开可编辑PPT</a><a href="preview.html">逐页看画面和讲稿</a><a href="materials/meeting_actions.xlsx">打开Excel演示</a></nav>
<h2>72秒会议整理讲解样片</h2><video controls preload="metadata" src="media/meeting_captioned.mp4"></video>
<p class="muted">原创模拟材料，中文系统旁白、单层字幕。尚需完整试听、动态同步与现场设备检查。</p>
<h2>配套材料</h2><p>先看讲述主线和部门场景，再检查演示节奏。以下阅读版可直接在浏览器查看。</p><ul>'''
entries = [('rehearsal_script_v3','完整试讲稿'),('task_card','可复制任务卡'),('scenario_menu','20个部门场景'),('office_case_cards','公开组织案例'),('tool_comparison','10项工具与费用'),('tool_tutorials','五个试用教程'),('history_brief','AI用法演变'),('video_routes','视频路线、费用与案例'),('video_production','本样片制作说明'),('spreadsheet_guide','Excel演示步骤'),('review_status','当前状态与待核项目')]
for name, title in entries:
    main += f'<li><a href="materials/{name}.html">{title}</a> · <a href="materials/{name}.md">Markdown源文件</a></li>'
    source = (bundle / 'materials' / f'{name}.md').read_text(encoding='utf-8')
    escaped = html.escape(source)
    escaped = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda match: f'<a href="{match[2]}">{match[1]}</a>', escaped)
    write_file(f'materials/{name}.html', page(title, '<p><a href="../start_here.html">返回入口</a></p><pre>' + escaped + '</pre>'))
main += '''</ul><h2>PPT制作过程素材</h2><p><a href="materials/production_examples/reference_template.pptx">模板副本</a> · <a href="materials/production_examples/weekly_report_sample.pptx">四页样例</a> · <a href="materials/production_examples/content_v1.pptx">30页初稿</a></p><p class="muted">完整复制文件夹即可离线阅读。视频未嵌入PPT，第27页单独播放。计划48分钟内容，加5分钟问答和2分钟机动，实际时长待排练。</p>'''
write_file('start_here.html', page('企业AI分享V3审阅入口', main))

inspect_file = bundle / 'materials/meeting_actions.xlsx.inspect.ndjson'
if inspect_file.exists():
    shutil.move(str(inspect_file), root / 'slides/review_v3/build/workbook_export.inspect.ndjson')

broken = []
for source in bundle.rglob('*'):
    if source.suffix not in {'.md', '.html'}:
        continue
    text = source.read_text(encoding='utf-8')
    links = re.findall(r'(?:href|src)="([^"]+)"', text) if source.suffix == '.html' else re.findall(r'\]\(([^)]+)\)', text)
    for link in links:
        link = html.unescape(link)
        parsed = urlsplit(link)
        if parsed.scheme or not parsed.path:
            continue
        target = (source.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(bundle.resolve()) or not target.exists():
            broken.append({'source': source.relative_to(bundle).as_posix(), 'link': link})
manifest = [{'path': file.relative_to(bundle).as_posix(), 'bytes': file.stat().st_size, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
            for file in sorted(bundle.rglob('*')) if file.is_file() and file.name not in {'package_manifest.json', 'leadership_review_v3_bundle.zip'}]
write_file('package_manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
(evidence / 'package_check.json').write_text(json.dumps({'files': len(manifest), 'broken_links': broken, 'slides_with_script': len(sections)}, ensure_ascii=False, indent=2), encoding='utf-8')
if broken:
    print(json.dumps(broken, ensure_ascii=False, indent=2))
    raise RuntimeError('随包链接尚未闭合，暂不生成ZIP')
archive = bundle / 'leadership_review_v3_bundle.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
    for file in sorted(bundle.rglob('*')):
        if file.is_file() and file != archive:
            output.write(file, Path('leadership_review_v3') / file.relative_to(bundle))
print(json.dumps({'files': len(manifest), 'archive_bytes': archive.stat().st_size, 'broken_links': 0}, ensure_ascii=False))
