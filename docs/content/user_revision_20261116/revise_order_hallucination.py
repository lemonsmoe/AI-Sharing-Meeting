"""Apply the user's page order and terminology edit to the saved native deck."""
from pathlib import Path
import hashlib, json, re, shutil
from pptx import Presentation
from lxml import etree

ROOT = Path(__file__).resolve().parents[3]
DOC = Path(__file__).parent
PROJECT = ROOT / 'slides/projects/user_revision_ppt169_20261116'
SOURCE = PROJECT / 'exports/AI分享_28页修订补图版_20261116.pptx'
OUTPUT = PROJECT / 'exports/AI分享_28页顺序与幻觉修订版_20261116.pptx'
ORDER = list(range(1, 12)) + [26] + list(range(12, 26)) + [27, 28]

REPLACEMENTS = {
    'AI 可能编造事实，也可能偏离你给的材料。': 'AI 幻觉：生成内容与事实、任务或材料不一致。',
    '事实不对': '事实性幻觉',
    '编出不存在的资料、来源或事件': '事实错误，或编造无法证实的信息',
    '没忠实于材料': '忠实性幻觉',
    '总结时漏掉限制，或改了原文的意思': '偏离任务、材料，或前后逻辑矛盾',
    '为什么会这样？': '造成幻觉的常见原因',
    '生成合理的文字，不等于核实了事实。': '训练目标与事实核验的差距：预测后续内容，不等于核实事实。',
    '缺少信息、资料有误、检索或推理出错，都可能影响结果。': '数据质量与知识边界：错误、过时信息，以及领域知识不足。',
}

HALLUCINATION = '''答案顺不顺，和答没答对是两回事。AI 把错误或缺少依据的内容写成看似可信的答案，这就是我们常说的 AI 幻觉。这里采用研究中的两类划分。

第一类是事实性幻觉，英文叫 Factuality Hallucination。内容与现实事实不符，或者编出了无法证实的信息。比如日期写错，甚至列出一篇根本不存在的论文。

第二类是忠实性幻觉，英文叫 Faithfulness Hallucination。它没有忠实遵循任务要求、提供的材料，或者前后逻辑不一致。比如会议记录只说“准备讨论”，总结却写成“已经批准”。话可能通顺，但已经改了原意。

成因可以先抓住两点。第一，训练目标与事实核验之间有差距。模型通过预测后续 token 学习语言和知识，生成内容并不意味着每句话都经过事实查询。缺少依据时，如果没有正确表达不确定，就可能给出貌似合理的猜测。有些训练和评估方式也会鼓励猜答，而不是承认不知道。

第二，数据质量和知识边界。训练材料可能包含错误、过时的信息；冷门领域或最新事实也可能覆盖不足。模型并不能稳定地辨别所有信息的真伪，任务材料不全、理解偏差，也会增加出错机会。

所以，提示词要写清要求，提供可靠材料，并允许它说不知道。关键结论要打开原始出处核对，数字要重新计算。另一个 Agent 可以帮忙挑错，但答案一致仍不能代替原文核验。'''

def flat(items):
    for shape in items:
        if shape.shape_type == 6:
            yield from flat(shape.shapes)
        else:
            yield shape

def main():
    before = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    deck = Presentation(SOURCE)
    assert len(deck.slides) == 28
    meme = next(s for s in deck.slides if any('公司表情包：' in x.text for x in flat(s.shapes) if x.has_text_frame))
    meme_pos = list(deck.slides).index(meme)
    if meme_pos != 11:
        nodes = deck.slides._sldIdLst
        node = nodes[meme_pos]
        nodes.remove(node)
        nodes.insert(11, node)
    hall = deck.slides[16]
    found = set()
    scale = deck.slide_width / 1280
    for shape in flat(hall.shapes):
        if not shape.has_text_frame or shape.text not in REPLACEMENTS:
            continue
        old = shape.text
        runs = [r for p in shape.text_frame.paragraphs for r in p.runs]
        assert runs
        runs[0].text = REPLACEMENTS[old]
        for run in runs[1:]:
            run.text = ''
        shape.width = int((490 if shape.top < 320 * scale and shape.left > 100 * scale else 1120) * scale)
        if old == '为什么会这样？':
            shape.width = int(1000 * scale)
        found.add(old)
    assert found == set(REPLACEMENTS), found

    notes = {f'{i:02d}': slide.notes_slide.notes_text_frame.text.strip() for i, slide in enumerate(deck.slides, 1)}
    notes['11'] = notes['11'].replace('下面用这份 PPT 的真实需求讲几个最实用的办法。', '接下来先看公司表情包这个生图案例，看看把要求写具体，会怎样影响输出；再用这份 PPT 的真实需求讲几个实用的办法。')
    notes['12'] = notes['12'].replace('这张是我用 AI 做过的公司表情包，', '刚才说到，提示词就是交给 AI 的任务说明。我们先看这张公司表情包，看看做图时可以怎样把要求写具体。它是我之前用 AI 做的，')
    notes['12'] += '\n\n如果只说“帮我做一套公司表情包”，AI 就得自己猜人物、风格和内容。把这些要求写具体，就更容易让输出接近我们想要的结果。这里展示的写法是根据成图整理的示例。它不是越长越好，关键是把会影响结果的要求交代清楚。下一页再看看，做 PPT 的需求可以怎么写。'
    notes['13'] = notes['13'].replace('先说描述需求。', '接着把同样的方法用到 PPT 上。')
    notes['17'] = HALLUCINATION
    for i in (11, 12, 13, 17):
        deck.slides[i - 1].notes_slide.notes_text_frame.text = notes[f'{i:02d}']
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == before, 'Source changed during revision'
    deck.save(OUTPUT)

    # Remap the existing SVG source once; preserve the user's other slide artwork.
    originals = {n: (PROJECT / f'svg_output/P{n:02d}.svg').read_text(encoding='utf-8-sig') for n in range(1, 29)}
    already_ordered = '公司表情包：' in originals[12]
    for new, old in enumerate(ORDER, 1):
        svg = originals[new if already_ordered else old]
        if new == 12:
            # The user's saved moved slide uses the white blank layout.
            svg = svg.replace('<rect width="1280" height="720" fill="#F6F3EC"/>', '<rect width="1280" height="720" fill="#FFFFFF"/>')
        if new == 17:
            for a, b in REPLACEMENTS.items():
                svg = svg.replace(a, b)
        (PROJECT / f'svg_output/P{new:02d}.svg').write_text(svg, encoding='utf-8')

    meta = json.loads((DOC / 'speaker_notes_per_page.json').read_text(encoding='utf-8'))['meta']
    meta.update(status='aligned_to_user_order_and_hallucination_revision', page_count=28)
    (DOC / 'speaker_notes_per_page.json').write_text(json.dumps({'meta': meta, **notes}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    titles = {}
    for i, slide in enumerate(deck.slides, 1):
        titles[i] = next(x.text for x in flat(slide.shapes) if x.has_text_frame and x.text.strip()).replace('\n', ' ')
    titles[6] = '用日常语言交代任务'
    titles[28] = '写代码是一项任务，创新才是目的'
    bodies = [f'# {i:02d}_{titles[i]}\n\n{notes[f"{i:02d}"]}\n' for i in range(1, 29)]
    for i, body in enumerate(bodies, 1):
        (PROJECT / f'notes/P{i:02d}.md').write_text(body, encoding='utf-8')
    (PROJECT / 'notes/total.md').write_text('\n---\n\n'.join(bodies), encoding='utf-8')
    (DOC / 'speaker_script.md').write_text('# 企业 AI 分享｜28 页照读讲稿\n\n' + '\n---\n\n'.join(b.replace('# ', '## ', 1) for b in bodies), encoding='utf-8')
    # Preview files are repopulated from native PowerPoint after this script.
    result = {'source': SOURCE.relative_to(ROOT).as_posix(), 'source_sha256': before,
              'output': OUTPUT.relative_to(ROOT).as_posix(), 'output_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
              'source_meme_page': meme_pos + 1, 'meme_page': 12, 'hallucination_page': 17,
              'new_to_previous_page': dict(enumerate(ORDER, 1)), 'notes_modified': [11, 12, 13, 17]}
    (DOC / 'order_revision.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
