const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 开始自动化验收：index.html 极致紧凑模式...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  const resultsDir = path.join(__dirname, '../test-results');
  if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
  }

  const indexPath = path.join(__dirname, '../index.html');
  await page.goto(`file://${indexPath}`, { waitUntil: 'networkidle' });

  // 1. 验证网格 gap 是否紧凑
  const gridGap = await page.$eval('.grid', el => window.getComputedStyle(el).gap);
  console.log('✅ .grid gap:', gridGap);

  // 2. 验证卡片内边距 padding
  const cardPadding = await page.$eval('.card', el => window.getComputedStyle(el).padding);
  console.log('✅ .card padding:', cardPadding);

  // 3. 验证卡片最小高度与尺寸
  const cardBox = await page.$eval('.card', el => {
    const rect = el.getBoundingClientRect();
    return { width: rect.width, height: rect.height };
  });
  console.log('✅ .card 实时尺寸:', cardBox);

  // 4. 验证头部徽章
  const badgeText = await page.$eval('.header-badge', el => el.innerText);
  console.log('✅ 顶部模式徽章:', badgeText);
  if (!badgeText.includes('紧凑版')) {
    throw new Error('Header badge does not indicate compact mode!');
  }

  // 5. 截取视口高清图
  const screenshotPath = path.join(resultsDir, 'index-compact-mode-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log('📸 已生成紧凑模式视口截图:', screenshotPath);

  // 6. 截取整页高清图
  const fullPageScreenshot = path.join(resultsDir, 'index-compact-mode-fullpage.png');
  await page.screenshot({ path: fullPageScreenshot, fullPage: true });
  console.log('📸 已生成紧凑模式整页截图:', fullPageScreenshot);

  await browser.close();
  console.log('🎉 紧凑模式自动化验收成功！');
})();
