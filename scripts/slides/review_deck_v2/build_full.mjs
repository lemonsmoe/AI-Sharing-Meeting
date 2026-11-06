import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from 'file:///C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
import {set_deck,representative,text,box,connect,slide,notes} from './representative_pages.mjs';
const root=process.cwd(),out=path.join(root,'slides/review_v2/build');
const deck=Presentation.create({slideSize:{width:1280,height:720}});set_deck(deck);
const red='#C40000',gray='#626971',ink='#25282E';
const source=JSON.parse(await fs.readFile('slides/review_v1/inputs/slides_content_v1.json','utf8'));
const refs={3:['research/concepts/chapter_draft.md','https://www.anthropic.com/research/building-effective-agents'],4:['https://www.anthropic.com/research/building-effective-agents','https://www.anthropic.com/news/model-context-protocol','https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills'],6:['docs/context/00_current/index.md','docs/runbooks/context_workflow.md'],7:['research/concepts/experiments/protocol.md'],8:['research/concepts/experiments/quote_input.json'],9:['research/concepts/experiments/session_outputs.md：E1','research/concepts/experiments/quote_deliverable.md'],11:['research/concepts/case_slide_revision.md','research/concepts/experiments/session_outputs.md：E2'],12:['research/concepts/experiments/quote_input.json','research/concepts/experiments/quote_run.json','research/concepts/experiments/quote_deliverable.md'],13:['docs/planning/thread_registry.json'],15:['tutorials/office/meeting_demo.md'],16:['tutorials/office/meeting_demo.md'],17:['tutorials/office/meeting_demo.md'],19:['research/slides/first_round.md','research/slides/native_powerpoint_check.md'],20:['docs/content/deck_review_v1.md','outputs/leadership_review/leadership_review_v1.pptx：第10页','slides/review_v2/build/representative_10.png'],21:['slides/templates/sycsense_reference.pptx','slides/experiments/output/weekly_report_sample_v1.pptx','outputs/leadership_review/leadership_review_v1.pptx'],22:['docs/content/office_case_cards.md'],23:['https://help.gamma.app/en/articles/8022861-what-s-the-easiest-way-to-export-my-gamma','https://help.gamma.app/en/articles/15939201-why-doesn-t-my-exported-pdf-or-powerpoint-match-what-i-see-in-gamma','research/slides/first_round.md','research/slides/evidence_update_03.md'],25:['C:/Users/22796/.codex/skills/ai-workflow-research/SKILL.md','docs/runbooks/context_workflow.md','docs/context/00_current/index.md'],26:['research/slides/native_powerpoint_check.md','research/concepts/experiments/session_outputs.md'],27:['videos/experiments/explainer_v2_reviewed/meeting_explainer.mp4','videos/experiments/explainer_v2_reviewed/render_report.json'],28:['videos/experiments/explainer_v2_reviewed/render_report.json'],29:['outputs/leadership_review_v2/materials'],30:['docs/content/rehearsal_script_v2.md']};
async function picture(s,file,x,y,w,h){const a=await fs.readFile(file);s.images.add({blob:a.buffer.slice(a.byteOffset,a.byteOffset+a.byteLength),contentType:'image/png',alt:file,fit:'contain',position:{left:x,top:y,width:w,height:h}});}
function table(s,values,widths,y=205){const t=s.tables.add({rows:values.length,columns:values[0].length,left:70,top:y,width:1140,height:values.length*72,values,columnWidths:widths});for(let r=0;r<values.length;r++)for(let c=0;c<values[r].length;c++){const z=t.getCell(r,c);z.fill=r===0?red:(r%2?'#F3F4F5':'#FFFFFF');z.text.style={typeface:'Microsoft YaHei',fontSize:25,color:r===0?'#FFFFFF':ink,bold:r===0};}return t;}
function pair(s,left,right,y,color=red){const a=text(s,left,70,y,660,82,26);const b=text(s,right,850,y,360,82,27,color,true);connect(s,a,b);}
for(const d of source.slides){
 if([5,10,14,18,24].includes(d.id)){representative(d.id);continue;}
 const s=slide(d.id,d.title);
 if(d.id===22) refs[22].push('https://www.alpha-sense.com/resources/case-studies/siemens/','https://www.microsoft.com/en/customers/story/27087-lifetime-products-microsoft-copilot-studio','https://cleric.ai/resources/case-studies/how-mixmax-reduced-incident-resolution-time-by-90-percent-with-cleric');
 if(d.id===29) refs[29]=['materials/task_card.md','materials/scenario_menu.md','materials/meeting_demo.md','media/meeting_explainer.mp4：相对本PPT所在目录'];
 switch(d.id){
 case 1:
  s.background.fill='#24262B';s.shapes.items[0].text.style={typeface:'Microsoft YaHei',fontSize:55,color:'#FFFFFF',bold:true};
  text(s,'企业 AI 效率分享',75,195,1080,65,32,'#FFBABA');
  text(s,'2026年11月16日',75,270,1080,55,28,'#FFFFFF');
  await picture(s,'slides/experiments/final_render/slide_03.png',70,365,530,298);
  await picture(s,'videos/experiments/explainer_v2_reviewed/frame_57.png',675,365,530,298);
  refs[1]=['slides/experiments/output/weekly_report_sample_v1.pptx','videos/experiments/explainer_v2_reviewed/meeting_explainer.mp4'];break;
 case 2:
  text(s,'报价比较',70,150,520,45,28,red,true);text(s,'可编辑汇报',680,150,520,45,28,red,true);
  text(s,'A  9240元 / 7天 / 满足\nB  9300元 / 交期未知\nC  9000元 / 10天 / 不满足',70,215,520,170,29);
  await picture(s,'slides/experiments/final_render/slide_03.png',680,205,480,230);
  text(s,'会议行动项',70,445,520,45,28,red,true);text(s,'讲解样片',680,445,520,45,28,red,true);
  text(s,'林提交测试报告\n11月9日18:00前\n依据 N01 + C01',70,505,530,130,28);
  await picture(s,'videos/experiments/explainer_v2_reviewed/frame_19.png',680,495,480,155);
  refs[2]=['research/concepts/experiments/quote_deliverable.md','tutorials/office/file_demo/output/meeting_brief.md',...refs[1]];break;
 case 3:
  [['生成回答','一句要求','摘要、改写'],['结合资料','指定文件','附出处的回答'],['使用工具','数据与规则','计算结果和文件'],['持续执行','目标与检查条件','分步修改后的成果']].forEach((r,i)=>{let y=190+i*105;text(s,r[0],70,y,240,70,31,red,true);text(s,r[1],365,y,310,70,28);text(s,r[2],770,y,450,70,28);});
  text(s,'四种工作方式可以同时存在，按任务选择。',70,620,1140,40,24,gray);break;
 case 4:{
  const center=box(s,'Agent\n执行与检查',480,300,290,120,'#FFF0F0',33);
  const a=box(s,'提示词\n目标与要求',70,190,300,110),b=box(s,'上下文\n资料与进度',70,440,300,110),c=box(s,'工具\n检索、计算、文件',900,300,310,120);
  connect(s,a,center);connect(s,b,center);connect(s,center,c);
  text(s,'Skill：可复用做法和资源',460,175,700,70,29,red);
  text(s,'MCP：连接工具与数据的一种可选规范',455,520,750,85,27,gray);break;}
 case 6:
  text(s,'本项目保存的工作现场',70,165,1140,55,31,red,true);
  [['当前索引','30页内容骨架、V2修订和待验证项'],['讨论记录','建议、已确认决定分开保存'],['任务认领','PPT、视频等聊天各有写入范围'],['运行记录','输入、成果、检查和交接证据']].forEach((r,i)=>{text(s,r[0],70,255+i*88,260,65,29,red,true);text(s,r[1],390,255+i*88,820,65,28);});break;
 case 7:
  text(s,'“帮我分析这三份报价。”',70,185,1140,90,40,gray);
  text(s,'采购同事接下来要开评审会',70,330,1140,60,34,red,true);
  text(s,'需要比较总价、交期和缺失信息，\n还要留下可以复核的公式与材料。',70,425,1140,130,34);
  text(s,'连续案例使用模拟报价，未接入采购系统。',70,600,1140,45,25,gray);break;
 case 8:table(s,[['供应商','价格口径','运费','交期'],['A','未税80元，税率13%','200元','7天'],['B','含税88元','500元','未提供'],['C','含税90元','免运费','10天']],[180,450,220,290]);text(s,'模拟需求：100件，9天内交付',70,560,1140,65,32,red,true);break;
 case 9:table(s,[['方案','含税到货总价','交期判断','原始材料缺口'],['A','9240元','满足：7天','交期已提供'],['B','9300元','未知','未提供交期'],['C','9000元','不满足：10天','已知超期']],[150,310,300,380]);text(s,'额外追问建议：核对报价有效性与供货能力；与C协商交期。',70,550,1140,80,27,red);break;
 case 11:
  text(s,'原输出：两件事放在同一个事项表',70,175,1140,55,29,gray);
  pair(s,'李工在11月9日前完成样机测试','明确承诺',275);
  pair(s,'包装清单需要更新，负责人和期限未定','待分工需求',395);
  text(s,'具体反馈：分开这两类事项，保留负责人、日期和原文编号。',70,555,1140,80,29,red);
  break;
 case 12:
  [['输入文件','100件，9天内交付\nA：80元未税 + 13%税\n运费200元，7天'],['核算记录','A：9240.00 / 满足\nB：9300.00 / 未知\nC：9000.00 / 不满足'],['交付文件','模拟采购比较表\n待确认：B交期\n保留报价核查建议']].forEach((r,i)=>{const x=70+i*390;text(s,r[0],x,185,360,65,32,red,true);text(s,r[1],x,300,350,220,27);});
  text(s,'实际Python处理了文件；脚本运行时间不等于完整工作耗时。',70,590,1140,65,26,gray);break;
 case 13:{
  const main=box(s,'主对话\n整合、复核、验收',870,300,340,135,'#FFF0F0',32);
  [['研究方法','证据标准与独立复核'],['概念提示词','术语与连续案例'],['企业办公','部门场景与教程'],['PPT制作','模板、样例与审阅稿'],['视频制作','分镜、样片与检查']].forEach((r,i)=>{const n=box(s,r[0]+'  '+r[1],70,165+i*92,650,67,'#F3F4F5',27);connect(s,n,main);});break;}
 case 15:
  pair(s,'M1 演示改到11月12日，大家同意。','已确认决定',200);
  pair(s,'M2 小林：11月9日18点前提交测试报告。','明确承诺',330);
  pair(s,'M3 是否采购两台设备？约8000元。','建议，待批准',460);
  text(s,'模拟文字材料；此处展示教学分类，未测试语音识别。',70,610,1140,45,25,gray);break;
 case 16:
  pair(s,'M4 采购没有批准，先收集报价，负责人未定。','收集报价\n负责人、期限未指定',195);
  pair(s,'M6 地点暂定会议室B，需行政确认。','待确认地点',340);
  pair(s,'M5 失败三次，可能是网络，尚未定位。','网络是风险假设\n不能写成根因',470);
  break;
 case 17:
  text(s,'M2 小林：我在11月9日18点前提交测试报告。',70,190,1140,100,33);
  table(s,[['负责人','行动','期限','来源'],['小林','提交测试报告','11月9日18点前','M2']],[220,420,320,180],350);
  text(s,'人工复核负责人和日期后，再进入团队已有流程。',70,565,1140,70,29,red);break;
 case 19:
  table(s,[['路线','已有证据','尚缺什么'],['Copilot / Gamma / WPS','官方能力和社区记录','统一任务的产品实测'],['本地可编辑生成','文件与PowerPoint检查','WPS和完整修订计时']],[340,400,400]);
  text(s,'原生检查发现：只改图表工作簿，系列未自动更新。\n显式修改系列后回存成功，不能据此宣称自动同步通过。',70,490,1140,125,28,red);break;
 case 20:
  text(s,'第10页 V1：只有价格图',70,165,535,60,29,gray);text(s,'第10页 V2：实际两版输出',675,165,535,60,29,red,true);
  await picture(s,'slides/review_v1/final_render/slide_10.png',70,245,535,301);
  await picture(s,'slides/review_v2/build/representative_10.png',675,245,535,301);
  text(s,'一处关键修改：让正文直接回答“交付层次有什么不同”。',70,585,1140,60,28,red);break;
 case 21:
  text(s,'模板原件',70,160,350,55,29,red,true);text(s,'四页小样',460,160,350,55,29,red,true);text(s,'30页内容初稿',850,160,360,55,29,red,true);
  await picture(s,'slides/templates/rendered/slide_01.png',70,250,350,230);
  await picture(s,'slides/experiments/final_render/slide_03.png',460,250,350,230);
  await picture(s,'slides/review_v1/final_render/slide_13.png',850,250,350,230);
  
  text(s,'保留输入、讲稿、源文件和修改记录，方便下一次继续制作。',70,570,1140,70,29);break;
 case 22:
  [['市场：Siemens','情报团队检索资料、准备月度报告','可试：三家公开竞品的月度变化'],['人事：Lifetime Products','基于手册提供HR制度问答','可试：回答附条款与版本日期'],['研发：Mixmax','汇集故障线索，由工程师验证修复','可试：日志时间线与竞争性假设']].forEach((r,i)=>{const y=185+i*145;text(s,r[0],70,y,430,55,29,red,true);text(s,r[1],510,y,700,55,27);text(s,r[2],510,y+58,700,55,26,gray);});
  text(s,'以上为供应商案例描述；本公司试用建议尚未执行。',70,625,1140,40,23,gray);break;
 case 23:
  text(s,'主张：Gamma支持导出PPTX',70,185,1140,70,35,red,true);
  text(s,'依据：Gamma官方导出说明',70,290,1140,60,30);
  text(s,'条件：导出外观可能变化，没有幻灯片母版。\n仍需在目标办公软件核对字体、版式与可编辑性。',70,390,1140,120,30);
  text(s,'资料访问日：2026年11月6日；本页不是本地Gamma实测。',70,590,1140,65,25,gray);break;
 case 25:
  [['Skill / 可复用做法','研究技能：证据、反证和复现实验要求'],['上下文 / 工作记录','当前索引：目标、已完成成果和下一步'],['Hook / 事件触发','本聊天已收到启动与讨论提醒；\n这不保证所有恢复路径都通过验证']].forEach((r,i)=>{text(s,r[0],70,195+i*145,490,90,29,red,true);text(s,r[1],590,195+i*145,620,115,28);});break;
 case 26:
  text(s,'本项目已有的试用记录',70,170,1140,60,30,red,true);
  table(s,[['检查项','实际记录','结论边界'],['报价计算','两版均算对，详细版有公式','同聊天，非因果实验'],['PowerPoint回存','文字通过，图表自动同步失败','显式改系列后通过'],['完整工作时间','准备、核查、返工未完整计量','不估算提效比例']],[250,480,410],255);break;
 case 27:
  await picture(s,'videos/experiments/explainer_v2_reviewed/frame_57.png',70,190,760,428);
  text(s,'原创会议整理样片',870,215,330,90,31,red,true);
  text(s,'72秒\n无声字幕版\n代码动画',870,330,330,160,30);
  text(s,'随包单独播放\n音画与动态审阅另行验收',870,535,330,100,25,gray);break;
 case 28:
  text(s,'13.43秒',70,195,500,135,76,red,true);
  text(s,'仅本地渲染耗时',70,345,500,65,31);
  text(s,'72秒无声字幕样片\n版本：explainer_v2_reviewed',70,460,530,110,27,gray);
  text(s,'完整投入还包括',690,195,520,65,32,red,true);
  text(s,'脚本与事实检查\n画面修改、配音与剪辑\n许可核查和人工复核',690,300,520,210,30);
  text(s,'本次外部付费API调用：0次\n助手账单与人工总成本：未知',690,545,520,100,26,gray);break;
 case 29:
  [['任务卡','填写自己的目标、材料和交付要求'],['部门场景菜单','挑选一个小任务先试用'],['会议示范材料','复用原文、提示词和核查清单'],['讲解样片','回看讨论怎样分类和溯源']].forEach((r,i)=>{text(s,r[0],70,200+i*105,350,75,31,red,true);text(s,r[1],470,200+i*105,740,75,29);});break;
 case 30:
  text(s,'你最想试的任务是什么？',70,240,1140,90,45,red,true);
  text(s,'现有工作里，哪一步最费时间？',70,405,1140,90,40);break;
 }
 notes(s,d.id,refs[d.id]??['docs/content/rehearsal_script_v2.md'],[3,4].includes(d.id)?'外部概念来源由项目研究包读取并登记，访问日2026-11-06。':d.id===23?'官方说明访问日2026-11-06。原文能力不代表本地测试。':'');
}
await (await PresentationFile.exportPptx(deck)).save(path.join(out,'review_candidate.pptx'));
for(const [i,s] of deck.slides.items.entries()){const b=await deck.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(out,`slide_${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await b.arrayBuffer()));console.log(`已渲染 ${i+1}`);}
