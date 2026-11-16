from pathlib import Path
import json
p=Path(__file__).parent
packet=json.loads((p/'discussion_packet.json').read_text(encoding='utf-8-sig'))
points=packet['previous_summary']['points']
for note in packet['new_notes']:
    for item in note['items']:
        points.append({'kind':item['kind'],'text':item['text'],'sources':[item['source']]})
result={k:packet[k] for k in ('topic','notes_revision','base_summary_revision')}
result.update(title='28页修订补图版与全新Agent多轮验收',abstract='28页PPT、逐页备注和照读稿已同步交付，三个全新Agent两轮独立审阅通过，原生编辑回读通过；P8/P22/P23按用户授权保留三个补图位，上午按接手清单补图试讲。',points=points,omitted=[])
(p/'discussion_consolidated.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Preserved historical points; integrated',sum(len(n['items']) for n in packet['new_notes']),'new items')
