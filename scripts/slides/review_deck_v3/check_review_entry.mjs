import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'file:///C:/Users/22796/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';

const browser = await chromium.launch({ headless: true, channel: 'chrome' });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(pathToFileURL(path.resolve('outputs/leadership_review_v3/start_here.html')).href);
  await page.screenshot({ path: 'slides/review_v3/build/review_entry.png', fullPage: true });
  const entry = await page.locator('video').evaluate(video => ({
    source: video.currentSrc, controls: video.controls, duration: video.duration,
    error: video.error?.message ?? null, paused: video.paused
  }));
  await page.goto(pathToFileURL(path.resolve('outputs/leadership_review_v3/preview.html')).href);
  const preview = { images: await page.locator('img').count(), scripts: await page.locator('details').count() };
  await page.locator('details').first().evaluate(element => { element.open = true; });
  await page.screenshot({ path: 'slides/review_v3/build/review_preview.png', fullPage: false });
  await fs.writeFile('research/integration/v3/entry_check.json', JSON.stringify({ entry, preview,
    scope: '离线入口、预览和媒体元数据；未播放、不证明音画同步或完整试听' }, null, 2));
  if (preview.images !== 30 || preview.scripts !== 30 || entry.error) throw new Error('入口检查失败');
  console.log(JSON.stringify({ entry, preview }));
} finally {
  await browser.close();
}
