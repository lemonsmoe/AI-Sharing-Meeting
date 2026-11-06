import fs from 'node:fs/promises';
import { FileBlob, SpreadsheetFile } from 'file:///C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
import { text, box, connect, slide, notes } from './representative_pages.mjs';

const red = '#C40000', gray = '#626971', ink = '#25282E';
const history_sources = [
  'https://arxiv.org/abs/2005.14165', 'https://openai.com/index/chatgpt/',
  'https://openai.com/index/function-calling-and-other-api-updates/',
  'https://www.anthropic.com/news/model-context-protocol',
  'https://openai.com/index/introducing-codex/',
  'https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills',
  'https://www.anthropic.com/research/effective-harnesses-for-long-running-agents',
  'https://www.anthropic.com/research/managed-agents', 'https://arxiv.org/abs/2210.03629'
];
const tools = JSON.parse(await fs.readFile('research/methodology/tool_landscape/tools.json', 'utf8'));
async function picture(page, file, x, y, width, height) {
  const data = await fs.readFile(file);
  page.images.add({ blob: data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength),
    contentType: 'image/png', alt: file, fit: 'contain', position: { left: x, top: y, width, height } });
}
async function spreadsheet_excerpt() {
  const file = 'slides/review_v3/assets/meeting_actions_excerpt.png';
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(
    'outputs/01a1afcd-c994-7ae0-89e1-3c3770ac406b/meeting_actions.xlsx'));
  const sheet = workbook.worksheets.getItem('会议跟进');
  const before = sheet.getRange('A1:G20').values;
  const excel_epoch = Date.UTC(1899, 11, 30);
  sheet.getRange('D6').values = [[(Date.UTC(2026, 10, 9, 18) - excel_epoch) / 86400000]];
  sheet.getRange('D12').values = [[(Date.UTC(2026, 10, 12) - excel_epoch) / 86400000]];
  workbook.recalculate();
  const after = sheet.getRange('A1:G20').values;
  for (let row = 0; row < 20; row++) for (let col = 0; col < 7; col++) {
    if (col === 3 && [5, 11].includes(row)) continue;
    if (JSON.stringify(before[row][col]) !== JSON.stringify(after[row][col])) throw new Error('日期以外单元格变化');
  }
  await fs.mkdir('outputs/leadership_review_v3/materials', { recursive: true });
  await (await SpreadsheetFile.exportXlsx(workbook)).save('outputs/leadership_review_v3/materials/meeting_actions.xlsx');
  const full_preview = await workbook.render({ sheetName: '会议跟进', range: 'A1:G21', scale: 1.5, format: 'png' });
  await fs.writeFile('slides/review_v3/assets/meeting_actions_full.png', new Uint8Array(await full_preview.arrayBuffer()));
  await fs.writeFile('slides/review_v3/build/workbook_date_check.json', JSON.stringify({
    changed_cells: ['D6', 'D12'], serials: [after[5][3], after[11][3]], other_values_unchanged: true,
    missing_owner_and_due_preserved: after[6][2] === null && after[6][3] === null,
    source_preserved: true, native_application_check: '未执行'
  }, null, 2));
  const preview = await workbook.render({ sheetName: '会议跟进', range: 'A5:E7', scale: 2, format: 'png' });
  await fs.writeFile(file, new Uint8Array(await preview.arrayBuffer()));
  return file;
}

export async function changed_page(id) {
  if (![3, 5, 6, 23, 24, 25, 27, 28, 29].includes(id)) return false;
  if (id === 3) {
    const page = slide(3, 'AI用法演变的代表节点');
    const milestones = [
      ['2020.05  论文', 'GPT-3', '任务说明与少量示例'],
      ['2022.11  产品预览', 'ChatGPT', '来回沟通与修改'],
      ['2023.06  API发布', '函数调用', '由应用执行工具操作'],
      ['2024.11  协议发布', 'MCP', '用统一接口连接系统'],
      ['2025.05  产品预览', '云端 Codex', '在环境里执行任务'],
      ['2025.10  官方介绍', 'Agent Skills', '按需复用做法与资源'],
      ['2025.11  工程文章', 'Harness 运行框架', '记录进度与接续'],
      ['2026.04  工程文章', '托管运行实践', '组件分离，支持接续']
    ];
    milestones.forEach((item, index) => {
      const x = 70 + (index % 4) * 290, y = index < 4 ? 180 : 390;
      text(page, item[0], x, y, 275, 40, 23, gray);
      text(page, item[1], x, y + 55, 275, 55, 28, red, true);
      text(page, item[2], x, y + 112, 265, 75, 25, ink);
    });
    text(page, '提示词、Skills、工具连接与Agent循环可以一起使用', 70, 600, 1140, 45, 28, ink, true);
    notes(page, 3, history_sources, '代表性公开节点，非技术发明或行业普及时间。时间线截至2026年4月的精选实践，不声称此后没有进展。H1—H9见随包history_sources.md，原文核验日2026-11-06。');
  }
  if (id === 5) {
    const page = slide(5, 'Agent怎样推进一项工作');
    text(page, '下一步由当前结果决定', 70, 150, 1100, 55, 30, gray);
    const a = box(page, '读取目标\n与当前材料', 70, 260, 235, 120);
    const b = box(page, '选择下一步\n调用工具', 375, 260, 235, 120, '#FFF0F0');
    const c = box(page, '检查结果\n满足交付条件？', 680, 260, 260, 120);
    const d = box(page, '交付', 1030, 260, 160, 120, '#F8E0E0', 36);
    connect(page, a, b); connect(page, b, c); connect(page, c, d);
    text(page, '是', 955, 270, 65, 40, 23, red, true);
    const e = box(page, '补材料、改步骤、再执行', 375, 480, 565, 80, '#FFF0F0', 28);
    connect(page, c, e, 'bottom', 'top', red); connect(page, e, b, 'top', 'bottom', red);
    text(page, '否', 810, 415, 60, 40, 24, red, true);
    text(page, '缺少必要材料或权限时，请求确认或停止', 70, 605, 1140, 50, 27, gray);
    notes(page, 5, ['research/concepts/chapter_draft.md', 'https://www.anthropic.com/research/building-effective-agents'], '可编辑概念图，包含等待或停止的边界。');
  }
  if (id === 6) {
    const page = slide(6, '长任务需要保存工作现场');
    text(page, 'Harness：围绕Agent的运行与接续框架', 70, 160, 1140, 60, 31, red, true);
    [['当前索引', '目标、已有成果和下一步'], ['讨论记录', '建议与已确认决定分开保存'],
      ['任务认领', '不同聊天各有写入范围'], ['运行记录', '输入、结果、检查与交接依据']].forEach((row, i) => {
      text(page, row[0], 70, 260 + i * 88, 260, 65, 29, red, true);
      text(page, row[1], 390, 260 + i * 88, 820, 65, 28);
    });
    notes(page, 6, ['docs/runbooks/context_workflow.md', ...history_sources.slice(6, 8)], '本项目文件仅作为配套运行机制的例子，不宣称自制上下文系统等同某商业产品。');
  }
  if (id === 23) {
    const page = slide(23, '按工作任务选择工具入口');
    const rows = [
      ['报告与中文初稿', 'ChatGPT、Claude、豆包'],
      ['一批本地文件', 'WorkBuddy、Codex'],
      ['现有办公文档', 'Microsoft 365 Copilot、WPS AI'],
      ['会议与组织知识', '飞书智能纪要、Notion'],
      ['大纲到演示文稿', 'Gamma，也可用现有办公套件']
    ];
    rows.forEach((row, i) => {
      text(page, row[0], 70, 175 + i * 82, 345, 65, 29, red, true);
      text(page, row[1], 445, 175 + i * 82, 765, 65, 29);
    });
    text(page, '代表性候选。先用同一份材料试做，再看权限、费用与复核成本。', 70, 610, 1140, 55, 25, gray);
    notes(page, 23, tools.flatMap(tool => [tool.official_guide, tool.pricing]),
      '2026-11-06核验。能力会重叠，本页不是使用率或效果排名。本项目仅实做Codex文件流程，其余为官方能力核对。豆包/飞书部分页为官方索引正文。详情随包tool_comparison.md、tool_sources.md。');
  }
  if (id === 24) {
    const page = slide(24, '会议文件整理成可编辑Excel');
    text(page, '原始记录', 70, 155, 520, 50, 28, red, true);
    text(page, 'N01  林：11月9日18点前交测试报告\nN03  先收集报价，负责人另定', 70, 215, 580, 100, 26);
    text(page, '会后补充', 685, 155, 520, 50, 28, red, true);
    text(page, 'C01  测试报告期限不变\nC02  会议室B尚未确认', 685, 215, 520, 100, 26);
    text(page, '实际工作簿节选', 70, 330, 1140, 45, 27, red, true);
    await picture(page, await spreadsheet_excerpt(), 70, 380, 1140, 175);
    text(page, '收集报价的负责人、期限保持空白，待补充确认', 70, 585, 1140, 55, 28);
    notes(page, 24, ['tutorials/office/file_demo/input/meeting_notes.txt', 'tutorials/office/file_demo/input/follow_up.txt',
      'materials/meeting_actions.xlsx', 'tutorials/office/spreadsheet_demo/validation.json'],
    '使用真实XLSX生成端渲染的节选图。截图不可编辑，随包另有可编辑工作簿；非WorkBuddy/Copilot/WPS AI实测，Excel/WPS应用打开尚待核验。');
  }
  if (id === 25) {
    const page = slide(25, '可复用做法与项目记录');
    [['Skill / 可复用做法', '研究规则、示例和必要资源'], ['上下文 / 工作记录', '目标、决定、成果与下一步'],
      ['Hook / 事件触发', '事件发生时执行预定动作\n例如启动时提示读取项目状态']].forEach((row, i) => {
      text(page, row[0], 70, 195 + i * 145, 490, 90, 29, red, true);
      text(page, row[1], 590, 195 + i * 145, 620, 115, 28);
    });
    notes(page, 25, ['C:/Users/22796/.codex/skills/ai-workflow-research/SKILL.md', 'docs/runbooks/context_workflow.md'],
      '已观察部分启动与讨论提醒，不保证所有生命周期路径通过验证。');
  }
  if (id === 27) {
    const page = slide(27, '72秒会议整理讲解样片');
    await picture(page, 'videos/experiments/caption_candidate_01/frame_28.png', 70, 190, 760, 428);
    text(page, '原创模拟会议', 870, 215, 330, 90, 31, red, true);
    text(page, '中文系统旁白\n单层完整字幕\n代码动画', 870, 330, 330, 160, 30);
    text(page, '随包视频可单独播放', 870, 540, 330, 85, 26, gray);
    notes(page, 27, ['media/meeting_captioned.mp4', 'research/video/caption_candidate_review.md',
      'videos/experiments/caption_candidate_01/render_report.json'],
    '音轨为Microsoft Huihui通用系统语音，非声音克隆。错误草稿为自编模拟。SHA256 afc31bb04c9837725aa357bf8f82c72f98e39f855b5d4975e8c6d6b8a3c8766d。完整试听及动态验收尚待完成。');
  }
  if (id === 28) {
    const page = slide(28, '视频制作的几条路线');
    const rows = [
      ['流程与原理培训', '代码解释动画', 'Remotion / Python + FFmpeg\n许可、AI服务与渲染投入'],
      ['软件操作与上手', '真实录屏剪辑', 'OBS Studio\n录制工具免费，剪辑配音另计'],
      ['宣传与创意镜头', '生成式视频', 'Runway\n订阅、积分和重试用量']
    ];
    rows.forEach((row, i) => {
      text(page, row[0], 70, 185 + i * 120, 340, 65, 29, red, true);
      text(page, row[1], 430, 185 + i * 120, 280, 65, 29, ink, true);
      text(page, row[2], 735, 185 + i * 120, 475, 95, 25);
    });
    text(page, '总投入包括写稿、生成、重试、剪辑和审片。费用详见配套资料。', 70, 600, 1140, 60, 25, gray);
    notes(page, 28, ['research/video/narrated_reproduction.md', 'materials/video_routes.md',
      'https://www.remotion.dev/docs/license/pricing', 'https://obsproject.com/', 'https://runway.com/pricing'],
      '本地三条命令复现27.388秒，仅对应旧旁白摘要版已有脚本运行，不含创作、审核及后续字幕重渲染。外部付费API调用为0，Agent账单与人工总成本未知。');
  }
  if (id === 29) {
    const page = slide(29, '会后可以复用的材料');
    [['任务卡与场景菜单', '选一个熟悉的小任务，写清交付要求'], ['工具入口与费用说明', '按任务看候选，核对账号与权限'],
      ['会议原文与Excel', '对照来源，继续补充待确认信息'], ['视频与制作说明', '保留文案、分镜和修改依据']].forEach((row, i) => {
      text(page, row[0], 70, 200 + i * 105, 410, 75, 30, red, true);
      text(page, row[1], 510, 200 + i * 105, 700, 75, 28);
    });
    notes(page, 29, ['start_here.html', 'readme.md', 'materials/tool_comparison.md', 'materials/meeting_actions.xlsx', 'media/meeting_captioned.mp4']);
  }
  return true;
}
