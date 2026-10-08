const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = 'file://' + path.resolve(__dirname, '../guoji/shanghai-international-highschools-V1.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  await page.goto(file, { waitUntil: 'networkidle' });

  const rows = await page.locator('#schoolTable tbody tr').count();
  const total = await page.locator('#count').textContent();
  console.log('总行数:', rows, '| 初始计数:', total);

  // 搜索
  await page.fill('#q', '平和');
  await page.waitForTimeout(150);
  const afterSearch = await page.locator('#schoolTable tbody tr:not(.hidden)').count();
  console.log('搜索「平和」可见行:', afterSearch);

  await page.fill('#q', '');
  // 区域筛选
  await page.selectOption('#fDist', '浦东新区');
  await page.waitForTimeout(150);
  const afterDist = await page.locator('#schoolTable tbody tr:not(.hidden)').count();
  console.log('筛选「浦东新区」可见行:', afterDist);

  await page.selectOption('#fDist', '');
  // 课程筛选
  await page.selectOption('#fCurr', '日本');
  await page.waitForTimeout(150);
  const afterCurr = await page.locator('#schoolTable tbody tr:not(.hidden)').count();
  console.log('筛选「日本」可见行:', afterCurr);

  await page.selectOption('#fCurr', '');
  await page.waitForTimeout(150);

  await page.screenshot({ path: path.resolve(__dirname, '../test-results/guoji-full.png'), fullPage: true });
  console.log('控制台错误:', errors.length ? errors : '无');

  await browser.close();
})();
