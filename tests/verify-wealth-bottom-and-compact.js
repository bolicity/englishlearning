const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 开始自动化验收：1. 家庭财富移至最底部独立板块；2. 卡片仅保留科目核心信息超紧凑...');
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

  // 1. 验证升学规划板块中不再有家庭财富
  const planningCards = await page.$$('#section-planning .card');
  console.log('✅ 升学规划板块卡片数量:', planningCards.length);
  if (planningCards.length !== 4) {
    throw new Error(`Expected 4 cards in planning section, but found ${planningCards.length}`);
  }

  const hasWealthInPlanning = await page.$eval('#section-planning', el => el.innerText.includes('财富传承'));
  console.log('✅ 升学规划板块中是否包含财富传承 (应为 false):', hasWealthInPlanning);
  if (hasWealthInPlanning) {
    throw new Error('Wealth card is still present in planning section!');
  }

  // 2. 验证家庭财富在最底部板块 #section-wealth
  const lastSectionId = await page.$$eval('.section-block', sections => sections[sections.length - 1].id);
  console.log('✅ 最后一个板块 ID (应为 section-wealth):', lastSectionId);
  if (lastSectionId !== 'section-wealth') {
    throw new Error(`Last section is ${lastSectionId}, expected section-wealth!`);
  }

  const wealthTitle = await page.$eval('#section-wealth .card-title', el => el.innerText);
  console.log('✅ 底部板块卡片标题:', wealthTitle);

  // 3. 验证卡片没有长段落 <p>，高度极致紧凑
  const pCount = await page.$$eval('.card p', ps => ps.length);
  console.log('✅ 卡片内部 <p> 标签数量 (应为 0):', pCount);
  if (pCount > 0) {
    throw new Error('Cards still contain <p> tags!');
  }

  const cardHeight = await page.$eval('.card', el => el.getBoundingClientRect().height);
  console.log('✅ 卡片实际渲染高度 (像素):', cardHeight);
  if (cardHeight > 65) {
    throw new Error(`Card height is ${cardHeight}px, too large!`);
  }

  // 4. 截取视口与全屏图
  const screenshotPath = path.join(resultsDir, 'index-wealth-at-bottom-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log('📸 已生成视口截图:', screenshotPath);

  const fullScreenshotPath = path.join(resultsDir, 'index-wealth-at-bottom-fullpage.png');
  await page.screenshot({ path: fullScreenshotPath, fullPage: true });
  console.log('📸 已生成全页截图:', fullScreenshotPath);

  await browser.close();
  console.log('🎉 验收彻底通过！家庭财富已在最下方，所有板块紧凑如仪！');
})();
