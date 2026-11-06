import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from 'file:///C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const root=process.cwd(),out=path.join(root,'slides/review_v2/build');
await fs.mkdir(out,{recursive:true});
let deck;
const red='#C40000',ink='#25282E',gray='#626971';
export function text(s,t,x,y,w,h,size=28,color=ink,bold=false){const q=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});q.text=t;q.text.style={typeface:'Microsoft YaHei',fontSize:size,color,bold};return q;}
export function box(s,t,x,y,w,h,fill='#F1F2F4',size=28){const q=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});q.text=t;q.text.style={typeface:'Microsoft YaHei',fontSize:size,color:ink};return q;}
export function connect(s,a,b,fromSide='right',toSide='left',color=gray){s.shapes.connect(a,b,{kind:'straight',fromSide,toSide,line:{fill:color,width:3},tail:{type:'arrow',width:'med',length:'med'}});}
export function slide(id,title){const s=deck.slides.add();s.background.fill='#FFFFFF';text(s,title,64,45,1150,90,42,red,true);text(s,'企业 AI 效率分享 · 内部审阅 V2',64,675,1050,25,16,gray);text(s,String(id).padStart(2,'0'),1170,674,60,28,18,gray);return s;}
const script=await fs.readFile(path.join(root,'slides/review_v2/inputs/rehearsal_script_v2.md'),'utf8');
export function notes(s,id,refs,extra=''){const marker=`## ${String(id).padStart(2,'0')}｜`;const start=script.indexOf(marker),end=script.indexOf('\n## ',start+4);s.speakerNotes.text=script.slice(start,end<0?undefined:end)+'\n\n本页来源：\n'+refs.join('\n')+'\n'+extra;}
export function set_deck(value){deck=value;}
export function representative(id){
if(id===5){
 const s=slide(5,'Agent怎样推进一项工作');
 text(s,'下一步由当前结果决定',70,150,1100,55,30,gray);
 const a=box(s,'读取目标\n与当前材料',70,270,235,120);
 const b=box(s,'选择下一步\n调用工具',375,270,235,120,'#FFF0F0');
 const c=box(s,'检查结果\n满足交付条件？',680,270,260,120);
 const d=box(s,'交付',1030,270,160,120,'#F8E0E0',36);
 connect(s,a,b);connect(s,b,c);connect(s,c,d);text(s,'是',955,276,65,40,23,red,true);
 const e=box(s,'补材料、改步骤、再执行',375,495,565,85,'#FFF0F0',28);
 connect(s,c,e,'bottom','top',red);connect(s,e,b,'top','bottom',red);
 text(s,'否',810,425,60,40,24,red,true);
 notes(s,5,['docs/content/rehearsal_script_v2.md：第5页','research/concepts/chapter_draft.md（概念解释；非运行轨迹）'],'此图为可编辑概念图，不冒充具体产品执行截图。');
}
if(id===10){
 const s=slide(10,'同一任务，可以交付不同层次的结果');
 text(s,'简短回答：先给判断',70,160,520,55,30,red,true);
 text(s,'详细回答：留下核算依据',670,160,540,55,30,red,true);
 box(s,'C总价9000元最低，但10天交期超过9天要求。\n\nA总价9240元、7天交付，可优先考虑。\n\nB总价9300元，需确认交期。',70,235,525,325,'#F3F4F5',28);
 box(s,'A  100×80×1.13+200 = 9240元\n     7天，满足\n\nB  100×88+500 = 9300元\n     未提供交期，保留未知\n\nC  100×90 = 9000元\n     10天，不满足',670,235,540,325,'#FFF0F0',25);
 text(s,'两版都算对；详细版增加公式和未知字段。来自同一聊天示范，不证明准确率提升。',70,595,1140,60,25,gray);
 notes(s,10,['research/concepts/experiments/session_outputs.md：E1基线与改进输出','research/concepts/experiments/quote_input.json'],'正文为真实保存输出的节选与版式整理；模拟金额，不是实际采购建议。');
}
if(id===14){
 const s=slide(14,'把任务交代清楚：一份可复制的任务卡');
 text(s,'采购比较 · 已填示例',70,155,1100,55,29,gray);
 const labels=['目标','材料','交付','检查'];
 const values=['比较三家报价，供采购同事评审。','100件，9天内交付；使用给定A/B/C报价。','给出含税到货总价、计算公式、交期判断和待确认项。','不要补造交期；缺失写未知。结果仅供评审，不下单。'];
 labels.forEach((v,i)=>{text(s,v,70,240+i*90,130,60,30,red,true);text(s,values[i],240,240+i*90,940,75,29);});
 notes(s,14,['research/concepts/experiments/quote_input.json','research/concepts/experiments/protocol.md'],'基于已执行模拟任务整理的可复制提示词，不声称逐字等于原提示。空白模板仍随包。');
}
if(id===18){
 const s=slide(18,'这份分享是怎样做出来的');
 const milestones=[['01','保留模板','17页原件副本\n哈希一致'],['02','制作小样','4页周报样例\n正文、图表、备注'],['03','扩展初稿','30页V1\n逐页渲染检查'],['04','审阅后修订','V2修订稿\n补真实输出与循环']];
 milestones.forEach((m,i)=>{const x=70+i*295;text(s,m[0],x,200,230,85,62,red,true);text(s,m[1],x,310,245,60,30,ink,true);text(s,m[2],x,395,240,125,27,gray);});
 text(s,'2026年11月6日的实际制作记录；步骤顺序有依据，耗时未做完整计量。',70,580,1130,55,25,gray);
 notes(s,18,['research/slides/template_review.md','research/slides/local_experiment.md','docs/context/02_events/2026/11/evt_slides_production.md','docs/content/deck_review_v1.md'],'此页为实际版本顺序，不按日志时间推算人工耗时。');
}
if(id===24){
 const s=slide(24,'两份文件，整理成可追踪的会议简报');
 text(s,'输入：原始记录 + 补充消息',70,160,530,55,29,red,true);
 text(s,'输出：简报 + 行动项JSON',675,160,535,55,29,red,true);
 box(s,'会议记录\nN01  林：11月9日18点前交测试报告\nN04  演示由11月9日改为11月12日',70,240,535,155,'#F1F2F4',25);
 box(s,'补充消息\nC01  测试报告期限不变\nC02  会议室B尚未确认\nC03  网络只是猜测，根因未定位',70,420,535,180,'#F1F2F4',25);
 text(s,'确认：演示改为11月12日',680,245,520,60,29,ink,true);
 text(s,'待办：林提交测试报告\n11月9日18:00前  [N01 + C01]',680,330,520,100,28);
 text(s,'JSON节选：收集设备报价\nowner: null  /  due: null',680,455,520,90,25,red);
 text(s,'负责人和期限未指定，保留空值。',680,565,520,60,25,gray);
 notes(s,24,['tutorials/office/file_demo/input/meeting_notes.txt','tutorials/office/file_demo/input/follow_up.txt','tutorials/office/file_demo/output/meeting_brief.md','tutorials/office/file_demo/output/action_items.json'],'模拟输入，当前Agent已实际文件处理；画面为文件节选，非云端产品测试。');
}
}
