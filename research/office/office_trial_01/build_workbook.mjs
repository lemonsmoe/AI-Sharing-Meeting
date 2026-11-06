import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const run_dir = path.dirname(fileURLToPath(import.meta.url));
const output_stage = process.argv[2] || 'first_output';
const first_dir = path.join(run_dir, output_stage);
const workbook = Workbook.create();
const serial_date = (month, day, hour=0) => (Date.UTC(2026,month-1,day,hour)-Date.UTC(1899,11,30))/86400000;
function make_sheet(name, title, headers, rows, widths) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.getRange('A2').values = [[title]];
  sheet.getRange('A3').values = [['模拟会议 2026-11-06；已合并17:00补充；日期为当地钟表时间']];
  sheet.getRange('A5').write([headers,...rows]);
  const end_col = String.fromCharCode(64+headers.length);
  sheet.getRange(`A1:${end_col}${rows.length+5}`).format.font = {name:'Arial',size:11};
  sheet.getRange('A2').format.font = {name:'Arial',size:16,bold:true};
  sheet.getRange(`A5:${end_col}5`).format = {fill:'#334155',font:{color:'#FFFFFF',bold:true},rowHeight:28};
  sheet.getRange(`A6:${end_col}${rows.length+5}`).format.rowHeight = 42;
  sheet.getRange(`A6:${end_col}${rows.length+5}`).format.wrapText = true;
  sheet.getRange(`A5:${end_col}${rows.length+5}`).format.verticalAlignment = 'center';
  widths.forEach((width,index)=>sheet.getRange(`${String.fromCharCode(65+index)}1:${String.fromCharCode(65+index)}${rows.length+5}`).format.columnWidth=width);
  sheet.freezePanes.freezeRows(5);
  return sheet;
}
const actions = make_sheet('行动清单','会后行动清单',
 ['事项','负责人','截止时间','状态','来源','说明'],[
 ['更新价格表','周',serial_date(11,9,12),'已承诺，完成情况未提供','M03、C02','期限不变'],
 ['收集两家支架报价','周',serial_date(11,10,17),'已确认分工，完成情况未提供','M05、C05、C06','周已确认收到；采购仍未批准'],
 ['提交测试摘要','林',serial_date(11,11,12),'已确认改期，完成情况未提供','M02、C01','替代原11月10日18:00期限']
 ],[29,12,25,32,24,42]);
actions.getRange('C6:C8').setNumberFormat('yyyy-mm-dd hh:mm');
actions.getRange('C6:C8').format.horizontalAlignment='left';
actions.getRange('A11').values=[['已完成事项（不再派发）']];
actions.getRange('A12:D13').values=[['事项','报告人','状态','来源'],['旧版培训材料上传','李','已于会议前一天上传完成','M06']];
actions.getRange('A11:F15').format.font={name:'Arial',size:11};
actions.getRange('A12:D12').format.fill='#E2E8F0';
actions.getRange('A13:D13').format.rowHeight=42;
actions.getRange('A13:D13').format.wrapText=true;
actions.getRange('A15').values=[['M编号：meeting_notes.txt；C编号：follow_up.txt。']];
const decisions=make_sheet('决定与未决','决定与未决事项',
 ['事项','负责人','日期时间','状态','来源','具体内容'],[
 ['材料冻结',null,serial_date(11,11,12),'已确认','M01','冻结时间不变；未指定负责人'],
 ['内部彩排',null,serial_date(11,12,16),'新增，已确认','C03','与正式演示分开；地点未提供'],
 ['正式演示',null,serial_date(11,13,15),'已确认','M01、C03、M07、C04','会议室A已预订；原暂定会议室C取消'],
 ['采购展示支架',null,null,'建议，未批准','M04、M05、C02、C05','两套仅为询价需求，不代表购买批准'],
 ['含税总额',null,null,'尚不能确认','M04、C07','需补税种、税率及价格是否含税'],
 ['接口两次超时',null,null,'根因未确认','M08','限流仅为可能原因，未分配排查人或期限']
 ],[29,12,25,32,28,50]);
decisions.getRange('C6:C8').setNumberFormat('yyyy-mm-dd hh:mm');
decisions.getRange('C6:C8').format.horizontalAlignment='left';
decisions.getRange('B6:B11').format.fill='#FFF2CC';
decisions.getRange('C9:C11').format.fill='#FFF2CC';
decisions.getRange('A14').values=[['原始询价信息（不计算含税总额）']];
decisions.getRange('A15:E16').values=[['询价数量（套）','单价（元）','运费（元）','税口径','来源'],[2,1200,80,'税种、税率及是否含税未知','M04、C02、C07']];
decisions.getRange('A14:F20').format.font={name:'Arial',size:11};
decisions.getRange('A15:E15').format.fill='#E2E8F0';
decisions.getRange('A15:E16').format.wrapText=true;
decisions.getRange('A15:E16').format.rowHeight=42;
decisions.getRange('B16:C16').setNumberFormat('#,##0');
decisions.getRange('A18').values=[['空白负责人、日期：原文未明确，需另行确认。']];
decisions.getRange('A20').values=[['M编号：meeting_notes.txt；C编号：follow_up.txt。']];
workbook.recalculate();
const xlsx=await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(path.join(first_dir,'meeting_follow_up.xlsx'));
await fs.writeFile(path.join(run_dir,'qa',`${output_stage}_export_time.txt`),new Date().toISOString());
for (const [sheet_name,range] of [['行动清单','A1:F16'],['决定与未决','A1:F21']]) {
 const preview=await workbook.render({sheetName:sheet_name,range,scale:1,format:'png'});
 await fs.writeFile(path.join(run_dir,'qa',`${output_stage}_${sheet_name}.png`),new Uint8Array(await preview.arrayBuffer()));
}
const inspection=await workbook.inspect({kind:'sheet',include:'id,name'});
await fs.writeFile(path.join(run_dir,'qa','workbook_inspect.ndjson'),inspection.ndjson);
console.log('首次工作簿已导出，两个工作表已渲染。');
