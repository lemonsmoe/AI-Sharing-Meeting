import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';

const runtime_require = createRequire('C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/runtime.cjs');
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(runtime_require.resolve('@oai/artifact-tool')).href);
const run_root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const build_started = new Date().toISOString();
const workbook = Workbook.create();
// 用无时区的Excel日期序数保留原文钟表时间。
const local_serial = (day, hour, minute = 0) => (Date.UTC(2026, 10, day, hour, minute) - Date.UTC(1899, 11, 30)) / 86400000;

function create_sheet(name, title, headers, rows, widths) {
  const sheet = workbook.worksheets.add(name);
  const last_column = String.fromCharCode(64 + headers.length);
  const last_row = rows.length + 5;
  sheet.showGridLines = false;
  sheet.getRange(`A1:${last_column}${last_row}`).format.font = { name: 'Microsoft YaHei', size: 11, color: '#243247' };
  sheet.getRange('A2').values = [[title]];
  sheet.getRange('A2').format.font = { name: 'Microsoft YaHei', size: 16, bold: true };
  sheet.getRange('A3').values = [['截至2026-11-06 17:00；均为当地钟表时间，不换算时区。']];
  sheet.getRange(`A5:${last_column}${last_row}`).values = [headers, ...rows];
  const table = sheet.tables.add(`A5:${last_column}${last_row}`, true, name === '行动清单' ? 'action_items' : 'meeting_records');
  table.showFilterButton = true;
  sheet.getRange(`A5:${last_column}5`).format = { fill: '#263C58', font: { color: '#FFFFFF', bold: true }, horizontalAlignment: 'center', verticalAlignment: 'center', rowHeight: 30 };
  sheet.getRange(`A6:${last_column}${last_row}`).format = { wrapText: true, verticalAlignment: 'center', rowHeight: 54 };
  widths.forEach((width, index) => {
    sheet.getRange(`${String.fromCharCode(65 + index)}1:${String.fromCharCode(65 + index)}${last_row}`).format.columnWidth = width;
  });
  sheet.getRange(`D6:D${last_row}`).setNumberFormat('yyyy-mm-dd hh:mm');
  sheet.getRange(`D6:D${last_row}`).format.horizontalAlignment = 'right';
  return sheet;
}

create_sheet('行动清单', '会议行动清单', ['事项', '负责人', '执行说明', '截止日期时间', '状态', '来源'], [
  ['更新价格表', '周', '交付时间保持不变', local_serial(9, 12), '待交付', 'M03、C02'],
  ['收集两家支架报价', '周', '按两套支架询价；收集报价不代表采购获批', local_serial(10, 17), '已确认接办，待交付', 'M04、M05、C02、C05、C06'],
  ['交付测试摘要', '林', '原2026-11-10 18:00期限已被会后确认替代', local_serial(11, 12), '待交付', 'M02、C01'],
], [25, 10, 48, 25, 25, 35]);

const records = create_sheet('决定与未决事项', '会议决定与未决事项', ['事项', '负责人', '最新内容', '日期时间', '类别及状态', '来源'], [
  ['材料冻结', null, '会议一致同意的冻结时间', local_serial(11, 12), '已确认决定', 'M01'],
  ['内部彩排', null, '新增内部彩排；地点未提供', local_serial(12, 16), '已确认决定', 'C03'],
  ['正式演示', null, '时间不变；改用会议室A且已预订，原暂定会议室C取消', local_serial(13, 15), '已确认决定', 'M01、M07、C03、C04'],
  ['支架采购', null, '周建议购买两套，数量目前仅作为询价需求；尚无购买批准', null, '建议，未批准', 'M04、M05、C02、C05'],
  ['税费及含税总额', null, '需补齐税种、税率及价格是否含税；含税总额暂不能确认', null, '未决问题', 'M04、C07'],
  ['接口超时', null, '出现两次超时；限流只是可能原因，根因未确认', null, '未决问题', 'M08'],
  ['旧版培训材料', '李', '2026-11-05已上传完成，不再安排为待办；具体时刻未提供', null, '已完成事项', 'M06（会议日期2026-11-06）'],
], [25, 10, 60, 25, 23, 35]);
records.getRange('A15').values = [['支架询价信息（非已批准采购金额）']];
records.getRange('A15').format.font = { bold: true };
records.getRange('A17:D20').values = [
  ['项目', '数值', '口径', '来源'],
  ['建议数量（套）', 2, '仅作询价需求', 'M04、C02'],
  ['报价单价（元/套）', 1200, '是否含税未知', 'M04、C07'],
  ['另列运费（元）', 80, '保留原文金额；未推算含税总额', 'M04、C07'],
];
records.getRange('A17:D17').format = { fill: '#263C58', font: { color: '#FFFFFF', bold: true }, rowHeight: 30 };
records.getRange('A18:D20').format = { wrapText: true, rowHeight: 40, verticalAlignment: 'center' };
records.getRange('B18:B20').setNumberFormat('#,##0');
workbook.recalculate();

const first_path = path.join(run_root, 'first_output', 'meeting_follow_up.xlsx');
try { await fs.access(first_path); throw new Error('首次产物已存在，禁止覆盖'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(first_path);
await fs.writeFile(path.join(run_root, 'qa', 'build_timing.json'), JSON.stringify({build_started, first_exported_utc: new Date().toISOString(), node_version: process.version}, null, 2));
for (const [name, range, file_name] of [['行动清单', 'A1:F9', 'actions'], ['决定与未决事项', 'A1:F21', 'decisions']]) {
  const inspection = await workbook.inspect({kind: 'table', range: `${name}!${range}`, include: 'values,formulas', tableMaxRows: 25, tableMaxCols: 6});
  await fs.writeFile(path.join(run_root, 'qa', `${file_name}_inspection.ndjson`), inspection.ndjson);
  const preview = await workbook.render({sheetName: name, range, scale: 1.5, format: 'png'});
  await fs.writeFile(path.join(run_root, 'qa', `${file_name}.png`), new Uint8Array(await preview.arrayBuffer()));
}
console.log(JSON.stringify({first_path, build_finished_utc: new Date().toISOString()}));
