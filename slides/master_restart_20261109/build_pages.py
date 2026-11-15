from pathlib import Path
from xml.sax.saxutils import escape
import json

root = Path(__file__).parent / 'master_preview_20261109'
out = root / 'svg_output'
out.mkdir(exist_ok=True)
bg, ink, red, teal, muted, rule = '#F7F4EE', '#202933', '#B8372C', '#297B83', '#59616C', '#C9C2B8'

def text(x, y, value, size=32, color=ink, font='Microsoft YaHei', bold=False):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" font-weight="{"bold" if bold else "normal"}">{escape(value)}</text>'

def lines(x, y, values, size=32, color=ink, leading=44):
    spans = ''.join(f'<tspan x="{x}" y="{y+i*leading}">{escape(v)}</tspan>' for i, v in enumerate(values))
    return f'<text font-family="Microsoft YaHei" font-size="{size}" fill="{color}">{spans}</text>'

def rect(x,y,w,h,fill='none',stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>'

def line(x,y,xx,yy,color=rule,arrow=False):
    return f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" stroke="{color}" stroke-width="2"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'

def group(name,bounds,body):
    return f'<g id="{name}" data-pptx-bounds="{bounds}">{body}</g>'

def page(n,title,body):
    header = group('heading','48 32 1184 114', text(48,60,f'AI 协作入门  /  0{n}',18,muted)+text(48,123,title,48, '#243142','SimSun'))
    footer = group('footer','48 670 1184 34',text(48,692,'企业 AI 效率分享 · 三页代表稿 · 2026.11',18,muted)+text(1160,692,f'0{n} / 03',18,muted))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" data-pptx-page-role="content"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="{teal}"/></marker></defs><rect id="background" data-pptx-role="background" x="0" y="0" width="1280" height="720" fill="{bg}"/>{header}{body}{footer}</svg>'

# P01：完整任务与批注对齐，纸张边缘比卡片阵列更接近原文阅读。
body=group('vague-request','48 162 1184 58',text(48,201,'“帮我整理一下会议记录。”',36,muted,'SimSun'))
chunks=[(['依据会议原文和会后补充，'], '01  材料'),(['输出一页纪要和 Excel 行动清单。'], '02  目标与格式'),(['会后确认覆盖原安排；','每个待办列负责人、期限、来源。'], '03  处理规则'),(['未说明的信息留空或标为待确认，','采购建议不要写成批准。'], '04  边界'),(['完成后检查日期变更和来源能否对上。'], '05  验收')]
y=269
for i,(copy,label) in enumerate(chunks):
    h=len(copy)*44
    content=lines(78,y,copy)+line(800,y-10,852,y-10)+text(880,y,label,26,red)
    body+=group(f'annotation-{i+1}',f'64 {y-32} 1168 {h+10}',content)
    y+=h+14
body+=group('check-reminder','48 622 1184 40',text(78,650,'要求变得可检查；生成以后，仍要拿原文核对。',26,muted))
(out/'01_prompt.svg').write_text(page(1,'把“整理一下”变成能验收的任务',body),encoding='utf-8')

# P02：框架表示归属，直线表示接入；组件不是代际升级链。
body=group('harness-field','47 192 1186 432',rect(48,193,1184,430,'none',rule)+text(72,230,'Harness 运行框架',26,muted)+text(700,230,'环境 · 调度 · 检查 · 接续',26,muted))
body+=group('prompt','72 264 1120 48',text(72,296,'提示词：说明目标与交付要求',26,red)+text(720,296,'Agent 据此推进工作',26))
for i,(x,label) in enumerate([(90,'读取材料'),(370,'选择下一步'),(670,'调用工具'),(960,'检查结果')]):
    body+=text(x,365,f'{i+1:02}',26,red)+text(x+46,365,label,26)
    if i<3: body+=line(x+220,354,x+258,354,teal,True)
for i,(x,title,detail,sub,target) in enumerate([(90,'Skill','提供可复用做法','可不使用 MCP',470),(480,'API / MCP','连接数据和操作','MCP 是可选接口',770),(880,'项目记录','保存决定与进度','不等于更新模型参数',1060)]):
    body+=group(f'support-{i}','%s 391 340 170'%x,line(x+120,419,target,391,teal,True)+text(x,464,title,32, '#243142')+text(x,504,detail,26)+text(x,545,sub,26,muted))
body+=group('delivery','72 568 1120 46',text(72,601,'交付：会议纪要 + 行动表',32,red)+text(650,601,'检查未通过，继续处理',26))
body+=group('diagram-limit','48 634 1184 28',text(72,655,'概念示意：这些组件可以配合，不是相互淘汰的升级链；不表示公司已接入。',18,muted))
import re
body = group('collaboration-diagram','47 190 1186 474', re.sub(r' data-pptx-bounds="[^"]*"', '', body))
(out/'02_collaboration.svg').write_text(page(2,'这些组件，在同一次工作里配合',body),encoding='utf-8')

# P03：可编辑表格与可见SVG在同一处定义，避免两份数据漂移。
grid=[['行动','负责人','期限','来源'],['更新价格表','周','11月9日 12:00','M03、C02'],['收齐两家支架报价','周','11月10日 17:00','C05、C06'],['交测试摘要','林','11月11日 12:00','M02、C01']]
widths=[420,140,320,272]
rows=[]; visible=''; yy=214
for r,values in enumerate(grid):
    cells=[]; xx=64
    for c,value in enumerate(values):
        fill='#EDE7DC' if r==0 else bg
        color=red if r==3 and c==2 else ink
        cell={'text':value,'fill':fill,'color':color,'align':'l','valign':'middle','bold':r==0,'font_size':26,'padding':16,'borders':{side:{'style':'none'} for side in ['left','right','top','bottom']}}
        cells.append(cell)
        visible+=rect(xx,yy,widths[c],80,fill)+text(xx+16,yy+50,value,26,color,bold=r==0)
        xx+=widths[c]
    rows.append(cells); yy+=80
payload={'schema':'ppt-master.semantic-table.v2','name':'action-table','x':64,'y':214,'width':1152,'height':320,'columns':rows[0],'rows':rows[1:],'column_widths':widths,'row_heights':[80]*4,'style':{'font_family':'Microsoft YaHei','font_size':26,'band_row':False,'header_fill':'#EDE7DC','header_text':ink,'body_fill':bg,'body_text':ink}}
table=f'<g id="action-table" data-pptx-bounds="64 214 1152 320" data-pptx-replace-with="table"><metadata type="application/json">{escape(json.dumps(payload,ensure_ascii=False))}</metadata>{visible}</g>'
body=group('source-label','64 160 1152 44',text(64,190,'模拟材料，Codex 实际生成',26,muted))+table
body+=group('changed-date','64 553 1152 42',text(64,582,'测试摘要改期：11月10日 18:00 → 11月11日 12:00',26,red))
body+=group('event','64 605 1152 56',text(64,631,'采购仍未批准',26,red)+text(350,631,'正式演示：11月13日 15:00 · 会议室 A',26,muted))
(out/'03_evidence.svg').write_text(page(3,'结果能跟进，还要能对回来源',body),encoding='utf-8')

