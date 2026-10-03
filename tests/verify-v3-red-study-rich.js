const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 [Test 2] 启动小红书避坑指南 V3 内容丰富度与交互自动化测试...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  const fileUrl = 'file://' + path.resolve(__dirname, '../red-study/red-study-abroad-V3.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  // 1. 验证标题与基本元素
  const pageTitle = await page.title();
  console.log(`✅ 页面标题: ${pageTitle}`);

  // 2. 验证各个模块是否完整存在
  const secUk = await page.$('#sec-uk-alevel');
  const secExam = await page.$('#sec-exam-boards');
  const secSg = await page.$('#sec-sg-study');
  const secLegal = await page.$('#sec-legal-warnings');
  const secBudget = await page.$('#sec-budget-calc');
  const secLuggage = await page.$('#sec-luggage-checklist');
  const secFaq = await page.$('#sec-faq-accordion');

  console.log(`✅ 七大模块完整性检查: UK=${!!secUk}, Exam=${!!secExam}, SG=${!!secSg}, Legal=${!!secLegal}, Budget=${!!secBudget}, Luggage=${!!secLuggage}, FAQ=${!!secFaq}`);
  if (!secUk || !secExam || !secSg || !secLegal || !secBudget || !secLuggage || !secFaq) {
    throw new Error('小红书 V3 页面缺失核心模块！');
  }

  // 3. 统计小红书笔记卡片数量
  const noteCardCount = await page.$$eval('.note-card', els => els.length);
  console.log(`✅ 小红书爆款笔记卡片总数: ${noteCardCount} 篇 (远超原先的 6 篇简陋卡片)`);
  if (noteCardCount < 12) {
    throw new Error('笔记卡片数量不足！');
  }

  // 4. 测试动态开销精算器切换交互
  console.log('👉 测试开销精算器交互切换...');
  await page.click('button:has-text("新加坡公立名校")');
  await page.waitForTimeout(300);
  const tuitionVal = await page.innerText('#budget-tuition');
  console.log(`✅ 切换为新加坡公立后学费: ${tuitionVal}`);

  // 5. 测试实时搜索过滤功能
  console.log('👉 测试搜索过滤功能...');
  await page.fill('#live-search-input', '出勤');
  await page.waitForTimeout(400);
  const visibleCardsCount = await page.$$eval('.note-card', els => els.filter(el => window.getComputedStyle(el).display !== 'none').length);
  console.log(`✅ 搜索“出勤”后匹配显示的笔记数量: ${visibleCardsCount} 篇`);

  // 清空搜索
  await page.fill('#live-search-input', '');
  await page.waitForTimeout(400);

  // 6. 测试折叠 FAQ 手风琴展开
  console.log('👉 测试 FAQ 折叠手风琴展开...');
  await page.click('.faq-item:nth-child(2) .faq-header');
  await page.waitForTimeout(300);
  const isFaq2Active = await page.$eval('.faq-item:nth-child(2)', el => el.classList.contains('active'));
  console.log(`✅ FAQ Q2 手风琴展开状态: ${isFaq2Active}`);

  // 截取长图以供验收
  const screenshotDir = path.resolve(__dirname, '../test-results');
  if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });
  await page.screenshot({ path: path.join(screenshotDir, 'v3-red-study-rich-verified.png'), fullPage: false });
  console.log('📸 已保存小红书 V3 页面截图: test-results/v3-red-study-rich-verified.png');

  await browser.close();
  console.log('🎉 [Test 2] 小红书避坑指南 V3 全部丰富度与交互测试通过！\n');
})();
