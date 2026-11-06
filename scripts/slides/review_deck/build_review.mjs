import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from 'file:///C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const root=process.cwd(), build=path.join(root,'slides/review_v1/build');
await fs.mkdir(build,{recursive:true});
const source=JSON.parse(await fs.readFile(path.join(root,'slides/review_v1/inputs/slides_content_v1.json'),'utf8'));
const source_map=await fs.readFile(path.join(root,'slides/review_v1/inputs/source_map.md'),'utf8');
const p=Presentation.create({slideSize:{width:1280,height:720}});
const red='#C40000', ink='#23272D', muted='#656A70';
function text(s,value,x,y,w,h,size=28,color=ink,bold=false){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=value;t.text.style={typeface:'Microsoft YaHei',fontSize:size,color,bold};return t;
}
function rows(s,values,x=70,y=180,w=1120,size=30){values.forEach((v,i)=>text(s,v,x,y+i*100,w,85,size));}
function table(s,values,widths){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:70,top:185,width:1140,height:Math.min(370,values.length*78),values,columnWidths:widths});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[r].length;c++){const z=t.getCell(r,c);z.fill=r===0?red:(r%2?'#F3F4F5':'#FFFFFF');z.text.style={typeface:'Microsoft YaHei',fontSize:25,color:r===0?'#FFFFFF':ink,bold:r===0};}
 return t;
}
function flow(s,labels){
 const w=250,gap=35;
 const nodes=labels.map((v,i)=>{const q=s.shapes.add({geometry:'rect',position:{left:70+i*(w+gap),top:270,width:w,height:140},fill:i===0?'#FFF0F0':'#F1F2F3',line:{fill:i===0?red:'#C9CDD1',width:1}});q.text=v;q.text.style={typeface:'Microsoft YaHei',fontSize:27,color:ink};return q;});
 for(let i=1;i<nodes.length;i++)s.shapes.connect(nodes[i-1],nodes[i],{kind:'straight',fromSide:'right',toSide:'left',line:{fill:'#777777',width:2},tail:{type:'arrow',width:'med',length:'med'}});
}
async function picture(s,file,x,y,w,h){const a=await fs.readFile(path.join(root,file));s.images.add({blob:a.buffer.slice(a.byteOffset,a.byteOffset+a.byteLength),contentType:'image/png',alt:file,fit:'contain',position:{left:x,top:y,width:w,height:h}});}
const layouts=[];
for(const d of source.slides){
 const s=p.slides.add();s.background.fill='#FFFFFF';let kind='分层正文';
 const dark=[1,7,15,18,22,27,30].includes(d.id);if(dark)s.background.fill='#24262B';
 text(s,d.title,64,48,1150,95,d.id===1?52:40,dark?'#FFFFFF':red,true);
 text(s,'内部审阅初稿 · 候选工具尚未验收',64,672,1060,28,16,dark?'#BFC2C7':muted);text(s,String(d.id).padStart(2,'0'),1160,670,60,30,18,dark?'#FFFFFF':muted);
 if([1,30].includes(d.id)){kind='封面与收尾';rows(s,d.body,70,240,1100,38);for(const q of s.shapes.items.slice(3))q.text.style={typeface:'Microsoft YaHei',fontSize:38,color:'#FFFFFF'};}
 else if([3,5,12,18,21,24].includes(d.id)){kind='流程';if(dark){s.background.fill='#FFFFFF';s.shapes.items[1].text.style={typeface:'Microsoft YaHei',fontSize:16,color:muted};s.shapes.items[2].text.style={typeface:'Microsoft YaHei',fontSize:18,color:muted};}s.shapes.items[0].text.style={typeface:'Microsoft YaHei',fontSize:40,color:red,bold:true};flow(s,d.body.length>4?d.body.slice(0,4):d.body);text(s,d.id===18?'本项目已完成分工、脚本与四页原型，当前进入30页审阅稿制作。':'每一步保存输入、输出和检查结果',70,490,1140,100,28,muted);}
 else if(d.id===4){kind='能力关系图';flow(s,['任务与提示词','Agent执行与检查','工具及文件']);text(s,'上下文：资料、决定、当前进度',70,180,1100,60,30);text(s,'Skill：可复用说明与资源',70,465,1100,60,30);text(s,'MCP：连接工具与数据的一种可选规范，也可直接调用工具',70,550,1140,80,27,muted);}
 else if(d.id===8){kind='原生报价表';table(s,[['供应商','价格口径','运费','交期'],['A','未税80元，税率13%','200元','7天'],['B','含税88元','500元','未提供'],['C','含税90元','免运费','10天']],[180,450,220,290]);text(s,'模拟需求：100件，9天内交付',70,570,1100,60,30,red,true);}
 else if([9,10].includes(d.id)){kind=d.id===9?'原生结果表':'原生价格图';if(d.id===9)table(s,[['方案','含税到货总价','交期','待确认'],['A','9240元','满足','有效期/供货能力'],['B','9300元','未知','交期'],['C','9000元','不满足','能否调整交期']],[150,330,210,450]);else{s.charts.add('bar',{position:{left:100,top:190,width:1080,height:350},categories:['A','B','C'],series:[{name:'含税到货总价（元）',values:[9240,9300,9000],fill:red}],hasLegend:false,dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:'Microsoft YaHei',fontSize:25}},xAxis:{textStyle:{typeface:'Microsoft YaHei',fontSize:25}},yAxis:{min:0,max:10000,textStyle:{typeface:'Microsoft YaHei',fontSize:20}}});}text(s,'模拟数据。A满足交期；B交期未知；C超过9天要求。',70,585,1140,60,27,muted);}
 else if([11,19,23,26,28].includes(d.id)){kind='对照与记录表';const data={11:[['反馈位置','具体意见','保留内容'],['交期判断','B未提供交期，请标未知','价格与公式'],['延期原因','材料没有提供，不要补造','原始数量']],19:[['路线','当前证据','仍需检查'],['Copilot / Gamma / WPS','官方能力与社区记录','同题生成、费用、导出兼容'],['本地可编辑生成','4页文件及图表校验通过','Office/WPS改后保存重开']],23:[['主张','依据','缺口'],['Gamma可导出PPTX','官方导出文档','图表可编辑性需实测'],['某工具更省时间','目前证据不足','人工基线与完整修订计时']],26:[['记录项','完整口径'],['质量','事实、公式、缺失信息'],['时间','准备+生成+核查+修改'],['成本/适配','套餐、调用、人工、权限和流程']],28:[['投入项','当前已知'],['本地样片','72秒，无声字幕版'],['渲染耗时','13.53秒，仅渲染，不含创作'],['外部付费调用','本次0次；助手账单未知'],['后续投入','配音、剪辑、许可及人工核查']]}[d.id];table(s,data,data[0].length===2?[320,820]:[300,420,420]);if(d.id===19)text(s,'比较口径：忠实度、可编辑性、导出兼容、完整修订耗时',70,540,1140,85,28,muted);}
 else if(d.id===17){kind='原文溯源';text(s,'M2 小林：我在11月9日18点前提交测试报告。',70,450,1140,110,30);table(s,[['负责人','事项','截止时间','来源'],['小林','提交测试报告','11月9日18点','M2']],[200,440,300,200]);text(s,'复核重点：不改变负责人和承诺时间；确认后再进入团队流程。',70,560,1140,85,26,red);}
 else if(d.id===16){kind='会议证据表';table(s,[['结果','原文','确认边界'],['11月12日演示','M1','已确认'],['小林提交测试报告','M2','11月9日18点前'],['收集设备报价','M4','负责人/期限未指定'],['采购与地点','M3—M4 / M6','采购未批准，地点暂定']],[430,220,490]);text(s,'模拟会议的预制教学结果，不是语音识别实测。',70,605,1140,45,24,muted);}
 else if(d.id===20){kind='真实成果对照';text(s,'内容要求',70,180,400,50,30,red,true);rows(s,d.body,70,260,430,27);await picture(s,'slides/experiments/final_render/slide_03.png',570,180,640,360);text(s,'真实四页样例的图表页，已按渲染结果放大标注。',570,560,620,75,24,muted);}
 else if(d.id===27){kind='视频入口';await picture(s,'videos/experiments/explainer_v2/frame_57.png',65,180,730,410);rows(s,d.body,835,180,380,23);for(const q of s.shapes.items.slice(3))q.text.style={typeface:'Microsoft YaHei',fontSize:23,color:'#FFFFFF'};text(s,'随包播放：media/meeting_explainer.mp4 · 72秒无声字幕版，未嵌入',70,610,1140,45,23,'#FFFFFF');}
 else if([7,15,22].includes(d.id)){kind='章节与案例';text(s,d.id===7?'01  提示词与材料':d.id===15?'02  会议与行动':'03  部门任务菜单',70,180,1120,60,28,'#FFBABA');rows(s,d.body,70,280,1120,30);for(const q of s.shapes.items.slice(4))q.text.style={typeface:'Microsoft YaHei',fontSize:30,color:'#FFFFFF'};}
 else if(d.id===29){kind='实际资料入口';table(s,[['随包文件','用途'],['materials/task_card.md','填写任务目标、材料、交付和验收'],['materials/scenario_menu.md','浏览部门任务候选'],['materials/meeting_demo.md','复用模拟会议与检查步骤'],['media/meeting_explainer.mp4','72秒无声字幕样片，单独播放']],[570,570]);}
 else if(d.id===14){kind='任务卡';table(s,[['任务卡字段','填写方法'],['目标与使用者','一句话说明要做什么，给谁用'],['材料与范围','列文件、可用工具、允许操作'],['交付与检查','约定格式、来源和验收条件'],['缺信息的处理','保留未知，列待确认项']],[320,820]);}
 else if(d.id===13){kind='分工关系';table(s,[['独立聊天','交付职责'],['方法 / 概念','证据门槛与概念案例'],['办公 / PPT / 视频','场景菜单、制作路线、样片'],['主对话','整合脚本、复核并验收']],[400,740]);}
 else{rows(s,d.body,70,190,1140,d.body.length>3?29:32);}
 s.speakerNotes.text=d.speaker_notes+'\n\n本页正文原稿：'+d.body.join('；')+'\n来源ID：'+d.source_ids.join(', ')+'\n剩余核验：'+d.remaining_validation+'\n当前状态：内部内容审阅初稿。未执行的录屏、产品测试不作为已完成。\n\n来源映射：\n'+source_map;
 layouts.push({id:d.id,title:d.title,layout:kind});
}
await (await PresentationFile.exportPptx(p)).save(path.join(build,'review_candidate.pptx'));
await fs.writeFile(path.join(build,'layout_plan.json'),JSON.stringify(layouts,null,2));
for(const [i,s] of p.slides.items.entries()){const b=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(build,`slide_${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await b.arrayBuffer()));console.log(`已渲染 ${i+1}`);}


