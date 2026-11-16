from pathlib import Path
from PIL import Image
import json, re, shutil
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[3]
PROJECT=ROOT/'slides/projects/user_revision_ppt169_20261116'
DOC=Path(__file__).parent
SVG=PROJECT/'svg_output'

# Normalize transport metadata without changing the authored composition.
for f in SVG.glob('*.svg'):
    s=f.read_text(encoding='utf-8-sig')
    s=re.sub(r'<g(?![^>]*data-pptx-bounds)', '<g data-pptx-bounds="0 0 1280 720"', s)
    if f.name=='P01.svg' and 'lang=' not in s.split('>')[0]:
        s=s.replace('<svg ', '<svg lang="zh-CN" ', 1)
    s=s.replace('data-pptx-bounds="80 540 1120 135"','data-pptx-bounds="80 540 1120 155"')
    s=s.replace('data-pptx-bounds="112 206 560 370"','data-pptx-bounds="112 206 560 390"')
    if f.name in {'P02.svg','P05.svg','P08.svg'} and 'id="page-composition"' not in s:
        s=s.replace('<rect width="1280" height="720" fill="#F6F3EC"/>','<rect width="1280" height="720" fill="#F6F3EC"/>\n  <g id="page-composition" data-pptx-bounds="0 0 1280 720">',1)
        s=s.replace('</svg>','</g>\n</svg>')
    f.write_text(s,encoding='utf-8')

# Browser snapshots may have JPEG bytes despite a .png file extension.
# Keep the original evidence; copy using its true format, changing no pixels.
formats={}
for p in (PROJECT/'images').rglob('*'):
    if not p.is_file(): continue
    try:
        with Image.open(p) as im: fmt=im.format
    except Exception: continue
    suffix={'JPEG':'.jpg','PNG':'.png','GIF':'.gif','WEBP':'.webp'}.get(fmt)
    if suffix and p.suffix.lower() not in ({'.jpg','.jpeg'} if fmt=='JPEG' else {suffix}):
        q=p.with_suffix(suffix); shutil.copy2(p,q)
        old='../images/'+p.relative_to(PROJECT/'images').as_posix()
        new='../images/'+q.relative_to(PROJECT/'images').as_posix()
        formats[old]=new
for f in SVG.glob('*.svg'):
    s=f.read_text(encoding='utf-8')
    for old,new in formats.items(): s=s.replace(old,new)
    f.write_text(s,encoding='utf-8')

notes=json.loads((ROOT/'docs/content/user_revision_script_20261116/speaker_notes_per_page.json').read_text(encoding='utf-8'))
notes['meta']['status']='aligned_to_revision_slides'
notes['04']=notes['04'].replace('在讲具体用法之前，先看看咱们平时会碰到的工具。','在讲具体用法之前，先看看咱们平时会碰到的产品和品牌。这里也包括字节 Seed、MiniMax 这些大家可能听过的模型或厂商品牌，后面会把软件和模型分开讲。')
notes['09']=notes['09'].replace('这张图是在说明语言模型生成文字的一个基本过程。','这张图是在说明语言模型生成文字的一个基本过程。图里下面是输入要求和已经写出的内容，上面是正在生成的句子；刚写出的词又放回下面，作为预测下一段的依据。')
notes['08']=notes['08'].replace('右边把这次任务说得更完整：','完整的写法会把这次任务说得更具体：')
notes['12']='先说描述需求。如果我只发一句“帮我做个 PPT”，对方得自己猜：讲给谁、讲多久、讲什么、要什么风格，最后交什么文件。\n\n可以像屏幕上这样，把一段完整的话交代出来：“我要给公司各部门同事和领导做一次 AI 入门分享，控制在四十分钟左右。请根据我提供的大纲，先做开场三页。沿用公司模板的米白、黑、红三色；每页只讲一个重点，配真实界面或成果图，减少大段文字。请交付可编辑的 PPTX，并给每页写一段能直接照读的讲稿。先给我看三页效果，确认后再继续完成整套。”\n\n这里没有什么神秘格式，就是把同事接手时会问的事提前说明白。拿到结果以后，我们也能照着这些要求，一项项看有没有做到。'
notes['14']=notes['14'].replace('比如这里是公司的模板，这里是我找到的 Swiss Grid 版式。','比如我会把公司的模板和找到的 Swiss Grid 版式一起交给它。').replace('再把样稿放在旁边，就能看出 AI 到底参考到了哪一部分。','拿到样稿，再对着参考看，就能看出 AI 到底参考到了哪一部分。')
notes['15']='拿到初稿之后，也别只许一个愿，比如“帮我做得更好看一点”。这句话表达了愿望，对方却还不知道该动哪里。\n\n大家看左边这份 PPT 的早期样稿。我会对着画面说：“左侧提示词太长，移到讲稿；统一字号，去掉左下角页脚；补上实际输入或结果图，让大家能直接看到例子。”这些意见指出了位置、问题和想要的效果，做完以后也容易检查。\n\n改稿就像甲方和乙方对需求。你可以不懂每一个设计术语，但要说清楚和预期差在哪。先拿几页看，再把确认过的要求带到其他页面，比等整套做完以后一起返工省事。'
notes['05']='我们平时说“我用 AI 做的”，其实说的可能不是同一层东西。豆包、ChatGPT 这些，是我们打开来使用的软件；模型是软件里面负责理解输入、生成结果的一部分。软件还可以给模型配上搜索、读文件、生成图片等工具。\n\n如果围绕一个目标，让模型根据当前结果决定下一步，再调用工具继续执行，这就是我们后面要讲的 Agent。Skill 给它提供做事的方法和资源，Harness 则负责支撑这个过程，包括上下文、工具、权限和执行状态。软件把这些能力组合起来，提供给我们使用。\n\n先不用把这几个英文词全记住。接下来从模型、上下文和提示词讲起，再逐个看它们怎么帮我们完成工作。'
notes['26']='这张是我用 AI 做过的公司表情包，四行四列，一共十六个。它把赛感的红色标识变成了卡通人物的头部，穿着米色连帽衫和蓝色裤子，再换成不同的动作和日常用语。\n\n如果要做出类似的一套，可以这样交代：“参考赛感 logo，设计一套十六宫格表情包。让红色标识成为卡通人物的头部，穿米色连帽衫、蓝裤子和棕色鞋。使用温暖的手绘风格、米白背景，保持角色一致。分别表现欢迎、早安、谢谢老板、收到、打工、摸鱼、大笑、疑问、点赞、抱抱等日常场景。每格配清楚的中文短句，用不同的动作和道具表达情绪。”\n\n大家看，主体是什么、排成几格、角色怎么保持一致、分别表达什么，都写进去了。生成以后，再逐格看标识有没有变形、字有没有写错，小图发到手机上还能不能看清。'
notes['22']=notes['22'].replace('看内容有没有漏、文字能不能改、讲稿能不能照着念','看内容有没有漏、版式是否清楚、讲稿能不能照着念')
notes['23']=notes['23'].replace('标题能不能选中修改，图片能不能替换，备注是不是跟这一页对应。','内容有没有讲清楚，图片是否合适，备注是不是跟这一页对应。')
notes['23']=notes['23'].replace('那在任务里怎么用 Skill？有的工作平台提供技能选择入口，也可以在任务里明确点名。','那在任务里怎么用 Skill？先确认平台已经安装了相应 Skill，或者能读取项目里的 Skill 文件。有的工作平台提供技能选择入口，也可以在任务里明确点名。')
notes['23']=notes['23'].replace('点名 Skill，交代这次的材料和要求，这两件事缺一不可。','想明确使用某个 Skill，可以点名或从入口选择；平台也可能根据任务自动选用合适的 Skill。无论哪种方式，都要交代好本次的材料和要求。')
notes['24']=notes['24'].replace('同样是“帮我整理一下”，','右边用 WorkBuddy 官方教程里的浏览器任务举例：执行记录里能看到打开网页、等待加载、读取内容、向下滚动这些动作。它根据网页整理出文档，而不只是告诉你应该怎么做。\n\n同样是“帮我整理一下”，')
notes['25']='做 AI PPT，可以按这五步来。先准备内容：想清楚讲给谁、希望听众记住什么、手上有哪些资料和例子。然后确认大纲，把每一页要讲的事排清楚。\n\n第三步，选参考、做小样。我把公司模板和喜欢的版式一起交给它，并明确说：“保留图片的对齐和留白，文字按照大纲要求的来。”先做几页，把字号、图文比例和整体感觉试出来。\n\n第四步，补充图片和实例，继续完成整套。需要实际软件界面的地方，就用真实截图；需要讲工作成果的地方，就把成果拿出来给大家看。\n\n最后一步，打开检查并修改。从头放映一遍，看内容是否准确、图片是否清楚、版式有没有挤压、讲稿是否跟页面对应。没有满足要求，就回到相应的步骤继续改。它生成了文件，不代表这件事已经结束；我们拿到符合要求、自己能讲明白的成品，才算完成了这次工作。'
(DOC/'speaker_notes_per_page.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
titles={}
for f in sorted(SVG.glob('*.svg')):
    root=ET.fromstring(f.read_text(encoding='utf-8'))
    text=root.find('{http://www.w3.org/2000/svg}text')
    titles[int(f.stem[1:])]=''.join(text.itertext()).strip() if text is not None else f.stem
titles[6]='用日常语言交代任务'
titles[28]='写代码是一项任务，创新才是目的'
body=[]
for n in range(1,29): body.append(f'# {n:02d}_{titles[n]}\n\n{notes[f"{n:02d}"]}\n')
(PROJECT/'notes').mkdir(exist_ok=True)
(PROJECT/'notes/total.md').write_text('\n---\n\n'.join(body),encoding='utf-8')
(DOC/'speaker_script.md').write_text('# 企业 AI 分享｜28 页照读讲稿\n\n'+ '\n---\n\n'.join(x.replace('# ','## ',1) for x in body),encoding='utf-8')
print(json.dumps({'pages':len(titles),'notes':len(notes)-1,'corrected_image_extensions':formats},ensure_ascii=False))
