from pathlib import Path
import json, re
from revise_order_hallucination import ROOT, DOC, ORDER

old_to_new = {old: new for new, old in enumerate(ORDER, 1)}
p = DOC / 'source_map.md'
s = p.read_text(encoding='utf-8')
def row(match):
    return '| ' + '、'.join(str(old_to_new[int(n)]) for n in match.group(1).split('、')) + ' |'
s = re.sub(r'^\| ([0-9]+(?:、[0-9]+)*) \|', row, s, flags=re.M)
s = s.replace('| 17 | 幻觉解释 |', '| 17 | 幻觉类型与成因 |')
s = s.replace('；生成流畅不等于事实正确，训练、信息缺失、检索和推理等都可能影响结果。', '；[Huang 等综述 §2.3、§3](https://arxiv.org/html/2311.05232v2)。采用事实性/忠实性幻觉分类；后者包含指令、上下文与逻辑一致性。讲稿解释训练目标与事实核验的差距，以及数据质量和知识边界；避免“总是取最高概率”“不会检索”“完全无法区分真伪”等绝对说法。')
p.write_text(s, encoding='utf-8')

p = DOC / '早上从这里开始.md'
s = p.read_text(encoding='utf-8')
s = s.replace('28 页 PPT、逐页备注和照读讲稿已经同步修改。', '最新版已按用户调整的顺序保存：公司表情包在第 12 页，紧接提示词介绍；幻觉在第 17 页，已补齐类型和成因。28 页 PPT、逐页备注和照读讲稿已同步。')
s = s.replace('AI分享_28页修订补图版_20261116.pptx', 'AI分享_28页顺序与幻觉修订版_20261116.pptx')
s = s.replace('| 22 |', '| 23 |').replace('| 23 | 右侧', '| 24 | 右侧').replace('第 23 页可以输入', '第 24 页可以输入')
start = s.index('## 已改好的内容')
end = s.index('## 最后自己过一遍')
s = s[:start] + '''## 当前顺序与修改

- 第 11 页介绍提示词，第 12 页用公司表情包展示具体提示词和输出；第 13–16 页讲需求、背景、参考与修改反馈。
- 第 17 页讲 AI 幻觉，明确“事实性幻觉”“忠实性幻觉”，补上“训练目标与事实核验的差距”“数据质量与知识边界”。讲稿包含英文术语、具体例子和白话解释。
- 原第 12–25 页整体顺延一页；第 27、28 页位置不变。总计仍为 28 页。
- 三个补图位现在是第 8、23、24 页；对应材料及截图要求见上表。

本轮保存为新的 PPT 文件，保留你已经调整过顺序的上一份文件。SVG源文件、逐页备注、预览及来源页码均已对应新版。`prepare_delivery.py` 是旧版生成脚本，已加保护；不要用它把当前内容恢复成旧页序。本轮改动脚本为 `revise_order_hallucination.py`。

''' + s[end:]
p.write_text(s, encoding='utf-8')

record = {
 'topic': 'workshop_scope', 'title': '公司表情包前移与幻觉术语补充',
 'abstract': '用户确认其余内容，表情包移至12页；幻觉页恢复研究分类和更专业的成因表述。',
 'source_message': '本轮用户：把公司表情包放到第12页，紧接提示词介绍；幻觉页要显示幻觉名称、对应类型和造成幻觉的原因，讲稿也补专业词汇。',
 'items': [
  {'kind': 'user_confirmed', 'text': '公司表情包作为提示词具体案例放第12页，紧接提示词介绍；幻觉页补类型、成因与专业术语，其他内容保持。', 'evidence': '用户本轮逐字要求：放到了第12页，也就是提示词后面一页；其他我感觉没有什么问题。'},
  {'kind': 'proposal', 'text': '本轮Agent建议：保留通俗主标题，在正文显示AI幻觉、事实性/忠实性幻觉；原因用训练目标与事实核验的差距、数据质量与知识边界，讲稿以例子解释，避免概率生成等于必然出错、无法检索或无法辨别真伪的绝对说法。'},
  {'kind': 'observation', 'text': '已读取用户保存的原PPT，表情包实际已在第12页；另存新版，保留用户顺序与其他页面，讲稿备注页码同步。幻觉为第17页，原补图位顺延到8/23/24。'}
 ]}
(DOC / 'order_discussion.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Updated source map, handoff and discussion input')
