const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 [Test Recitation] 启动语文基础题库背诵页面自动化测试...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  page.on('console', msg => console.log(`[Browser Console] ${msg.text()}`));
  page.on('pageerror', err => console.error(`[Browser Page Error] ${err.message}`));

  // 1. 打开初中语文复习中心
  const homeUrl = 'file://' + path.resolve(__dirname, '../chinese/chinese.html');
  await page.goto(homeUrl, { waitUntil: 'networkidle' });

  // 2. 检查题库卡片并点击
  console.log('👉 检查并点击【语文基础题库背诵】卡片...');
  const card = await page.$('a.tile:has-text("语文基础题库背诵")');
  if (!card) throw new Error('未找到语文基础题库背诵卡片！');

  await card.click();
  await page.waitForTimeout(600);

  // 3. 验证进入 recitation-bank-V1.html
  const currentUrl = page.url();
  console.log(`📄 当前页面 URL: ${currentUrl}`);
  if (!currentUrl.includes('recitation-bank-V1.html')) {
    throw new Error('未正确跳转至 recitation-bank-V1.html！');
  }

  // 4. 验证目录和题目渲染
  const secCount = await page.$$eval('.sec', els => els.length);
  console.log(`📚 目录小节数量: ${secCount}`);
  if (secCount === 0) throw new Error('题库目录未成功渲染！');

  // 检查第一题卡片是否存在
  const cardEl = await page.$('.card');
  if (!cardEl) throw new Error('背诵题卡未渲染！');
  const stemText = await page.innerText('.stem');
  console.log(`📝 第一题题干预览: ${stemText.substring(0, 30)}...`);

  // 5. 校验答案直接展示或存在
  const ansBox = await page.$('#ansbox');
  console.log(`✅ 答案区块存在: ${!!ansBox}`);
  if (!ansBox) throw new Error('未找到答案区块！');

  // 6. 测试切换到【速览】模式
  console.log('👉 测试切换到【速览】模式...');
  await page.click('#m-browse');
  await page.waitForTimeout(400);
  const listItems = await page.$$eval('.li', els => els.length);
  console.log(`📋 速览列表条目数: ${listItems}`);
  if (listItems === 0) throw new Error('速览列表未渲染！');

  // 7. 验证返回语文中心按钮
  console.log('👉 测试点击【语文中心】返回按钮...');
  await page.click('a[title="返回初中语文复习中心"]');
  await page.waitForTimeout(500);
  const backUrl = page.url();
  console.log(`🔙 返回后 URL: ${backUrl}`);
  if (!backUrl.includes('chinese.html')) {
    throw new Error('未能正确返回 chinese.html！');
  }

  console.log('🎉 [Test Recitation] 语文基础题库背诵版全部测试验收通过！');
  await browser.close();
  process.exit(0);
})().catch(err => {
  console.error('❌ 测试验收失败:', err);
  process.exit(1);
});
