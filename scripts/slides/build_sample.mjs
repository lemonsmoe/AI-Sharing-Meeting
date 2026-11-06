import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from 'file:///C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const started=new Date();
const out=path.resolve('slides/experiments',process.argv[2]||'run_01');
if (!/^[a-z][a-z0-9_]*$/.test(process.argv[2]||'run_01')) throw new Error('目录名仅允许小写字母、数字和下划线');
try { await fs.access(out); throw new Error('输出目录已存在，请选用新目录以保留证据'); } catch(error) { if(error.code!=='ENOENT') throw error; }
await fs.mkdir(out,{recursive:true});
const presentation=Presentation.create({slideSize:{width:1280,height:720}});
 const addText=(s,text,x,y,w,h,size,color='#202020',bold=false)=>{const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=text;t.text.style={typeface:'Microsoft YaHei',fontSize:size,color,bold};return t;}; const titles=['AI辅助周报整理','原始记录与提示词','本周任务完成情况','人工复核与发布'];for(let i=0;i<4;i++){const s=presentation.slides.add();s.background.fill='#FFFFFF';addText(s,titles[i],64,50,1120,90,44,'#C40000',true);if(i===0){addText(s,'从散乱记录到可核查的行动清单',64,235,1100,100,36);addText(s,'模拟办公案例',64,520,1000,50,24,'#666666');}if(i===1){addText(s,'甲组：完成8项，延期2项\n乙组：完成6项，延期4项',64,175,1100,130,32);addText(s,'请按组汇总完成和延期数量。\n区分事实与建议，不补造延期原因。',64,360,1100,140,32); }if(i===2){s.charts.add('bar',{position:{left:100,top:170,width:1050,height:390},categories:['甲组','乙组'],series:[{name:'完成',values:[8,6],fill:'#C40000'},{name:'延期',values:[2,4],fill:'#888888'}],hasLegend:true,dataLabels:{showValue:true,position:'outEnd'},yAxis:{min:0,max:10}});addText(s,'单位：项。所有数字仅用于模拟演示。',64,600,1100,45,24,'#666666');}if(i===3){addText(s,'核对计数与原始记录\n请负责人补充延期原因\n确认下一步安排后再发布',64,190,1100,240,34);addText(s,'当前结果为草稿',64,530,1100,60,28,'#C40000',true);}}
const c=presentation.slides.items[2].charts.items[0];
const st={typeface:'Microsoft YaHei',fontSize:24};c.xAxis={textStyle:st};c.yAxis={min:0,max:10,textStyle:st};c.legend={textStyle:st};c.dataLabels={textStyle:{...st,bold:true}};
for(const s of presentation.slides.items) s.speakerNotes.text='模拟案例：甲组完成8项、延期2项，乙组完成6项、延期4项。不得推断延期原因；发布前由负责人核对。';
await (await PresentationFile.exportPptx(presentation)).save(path.join(out,'sample_draft.pptx'));
for(const [i,s] of presentation.slides.items.entries()){
 const b=await presentation.export({slide:s,format:'png',scale:1});
 await fs.writeFile(path.join(out,`slide_${i+1}.png`),new Uint8Array(await b.arrayBuffer()));
}
await fs.writeFile(path.join(out,'execution.json'),JSON.stringify({started:started.toISOString(),ended:new Date().toISOString(),seconds:(Date.now()-started.getTime())/1000,tool:'artifact-tool 2.8.119',scope:'确定性脚本执行和渲染时间，不含前期写作及人工检查，不代表产品生成效率',slides:4},null,2));
console.log(out);
