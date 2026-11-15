import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const [nodeModules, browserPath, svgPath, outputPath] = process.argv.slice(2);
const require = createRequire(path.join(nodeModules, '_ppt_preview.cjs'));
const { chromium } = require('playwright');
const browser = await chromium.launch({ executablePath: browserPath, headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto(pathToFileURL(path.resolve(svgPath)).href);
  await page.evaluate(() => document.fonts.ready);
  const png = await page.locator('svg').screenshot({ animations: 'disabled' });
  await fs.writeFile(outputPath, png);
} finally {
  await browser.close();
}
