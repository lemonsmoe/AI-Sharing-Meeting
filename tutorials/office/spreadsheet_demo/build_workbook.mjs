import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const demo_dir = path.dirname(fileURLToPath(import.meta.url));
const project_dir = path.resolve(demo_dir, '../../..');
const output_dir = path.join(project_dir, 'outputs/01a1afcd-c994-7ae0-89e1-3c3770ac406b');
await fs.mkdir(output_dir, { recursive: true });
const input_dir = path.resolve(demo_dir, '../file_demo/input');
const input_files = ['meeting_notes.txt', 'follow_up.txt'];
const inputs = await Promise.all(input_files.map(async name => ({
  name, text: await fs.readFile(path.join(input_dir, name), 'utf8')
})));

const workbook = Workbook.create();
const sheet = workbook.worksheets.add('会议跟进');
sheet.showGridLines = false;
sheet.tabColor = '#23354D';
const range = sheet.getRange('A1:G23');
range.format.font.name = 'Arial';
range.format.font.size = 11;
range.format.verticalAlignment = 'center';
range.format.rowHeight = 28;
range.format.font.color = '#23354D';
for (const [col, width] of Object.entries({ A: 70, B: 205, C: 120, D: 190, E: 150, F: 28, G: 360 })) {
  sheet.getRange(`${col}1:${col}23`).format.columnWidthPx = width;
}
sheet.getRange('A2').values = [['部门周会 · 行动跟进']];
sheet.getRange('A2').format.font.size = 16;
sheet.getRange('A2').format.font.bold = true;
sheet.getRange('A2:E2').format.borders = { bottom: { style: 'thin', color: '#23354D' } };
sheet.getRange('A3').values = [['模拟材料｜会议日期 2026-11-06｜空白负责人或期限需补充确认']];
sheet.getRange('A3').format.font.italic = true;
sheet.getRange('A5:E7').values = [
  ['编号', '已确认的行动', '负责人', '截止时间', '来源'],
  ['A01', '提交测试报告', '林', new Date('2026-11-09T18:00:00Z'), 'N01 / C01'],
  ['A02', '收集设备报价', null, null, 'N03']
];
sheet.getRange('D6:D7').setNumberFormat('yyyy-mm-dd hh:mm');
sheet.getRange('G5:G7').values = [['核对提示'], ['期限不变；完成情况未提供'], ['负责人、期限均未定；采购未批']];
sheet.getRange('G5').format.font.bold = true;
for (const address of ['C6:C7', 'D6:D7']) {
  sheet.getRange(address).conditionalFormats.add('containsBlanks', { format: { fill: '#FFF0CF' } });
}
sheet.getRange('A10').values = [['已确认变更与未决信息']];
sheet.getRange('A10').format.font.bold = true;
sheet.getRange('A11:E15').values = [
  ['编号', '事项', '信息状态', '日期 / 金额', '来源'],
  ['D01', '演示日期调整', '已确认', new Date('2026-11-12T00:00:00Z'), 'N04'],
  ['D02', '购买两台设备', '建议；未批准', 8000, 'N02 / N03'],
  ['D03', '会议室 B', '尚未确认', null, 'C02'],
  ['D04', '接口失败根因', '尚未定位', null, 'C03']
];
sheet.getRange('D12').setNumberFormat('yyyy-mm-dd');
sheet.getRange('D13').setNumberFormat('"约 "#,##0" 元"');
sheet.getRange('E6:E15').format.horizontalAlignment = 'center';
sheet.getRange('G11:G15').values = [
  ['核对提示'], ['由 11 月 9 日改到 11 月 12 日'], ['没有采购批准；金额是估算'], ['不能写成已预订'], ['网络问题仅为假设']
];
sheet.getRange('G11').format.font.bold = true;
for (const header of ['A5:E5', 'A11:E11']) {
  const header_range = sheet.getRange(header);
  header_range.format.fill = '#23354D';
  header_range.format.font.color = '#FFFFFF';
  header_range.format.font.bold = true;
  header_range.format.horizontalAlignment = 'center';
  header_range.format.borders = { insideVertical: { style: 'thin', color: '#FFFFFF' } };
}
sheet.getRange('A7:E7').format.borders = { bottom: { style: 'thin', color: '#D6DBE2' } };
sheet.getRange('A15:E15').format.borders = { bottom: { style: 'thin', color: '#D6DBE2' } };
sheet.getRange('A18').values = [['来源索引（原文不改）']];
sheet.getRange('A18').format.font.bold = true;
sheet.getRange('A19').values = [['N01—N04：meeting_notes.txt；C01—C03：follow_up.txt']];
sheet.getRange('A20').values = [['浅黄色空白：待补充确认。日期按会议当地时间填写，不进行时区换算。']];

workbook.recalculate();
const inspection = await workbook.inspect({ kind: 'region', sheetId: sheet.name, range: 'A1:G20', maxChars: 10000, tableMaxRows: 20, tableMaxCols: 7 });
await fs.writeFile(path.join(demo_dir, 'inspection.ndjson'), inspection.ndjson);
const cells = sheet.getRange('A1:G20').values;
if (cells[6][2] !== null || cells[6][3] !== null) throw new Error('未知责任人或期限被填充');
if (cells[5][2] !== '林' || cells[5][1] !== '提交测试报告') throw new Error('行动提取不符');
const error_cells = cells.flat().filter(value => typeof value === 'string' && /^#(REF!|DIV\/0!|VALUE!|N\/A|NAME\?|NUM!|NULL!)/.test(value));
if (error_cells.length) throw new Error('存在表格错误');
const preview = await workbook.render({ sheetName: sheet.name, range: 'A1:G21', scale: 1.5, format: 'png' });
await fs.writeFile(path.join(demo_dir, 'preview.png'), new Uint8Array(await preview.arrayBuffer()));
const output_file = path.join(output_dir, 'meeting_actions.xlsx');
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(output_file);
const hashes = inputs.map(item => ({ file: item.name, sha256: crypto.createHash('sha256').update(item.text).digest('hex') }));
const result = {
  output: output_file, sha256: crypto.createHash('sha256').update(await fs.readFile(output_file)).digest('hex'),
  inputs: hashes, sheets: 1, action_rows: 2, decision_rows: 4, unknown_fields_retained: true,
  formula_error_count: error_cells.length, calculation_formulas: 0, simulation: true,
  generation_route: '本会话依据原文整理，artifact-tool 生成；未在 WorkBuddy / Copilot 中运行',
  limitations: ['未在 Excel / WPS 实机中打开核验', '数据为模拟材料，不代表真实采购或会议决定']
};
await fs.writeFile(path.join(demo_dir, 'validation.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result));
