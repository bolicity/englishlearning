const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收：日历格子显示当天费用总额 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V4.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 切换到 9 月份
  console.log('✔ 切换到 2026 年 9 月...');
  await page.click('#view-tutoring .month-selector button:has-text("‹")');
  await page.waitForTimeout(300);

  // 2. 注入或登记 19 号的 3 门课程 (英语 600, 物理 450, 化学 450, 与用户截图完全一致)
  console.log('✔ 模拟登记 19 号的 3 节课 (英语 600, 物理 450, 化学 450)...');
  await page.evaluate(() => {
    let lessons = JSON.parse(localStorage.getItem('owen_unified_lessons_v1') || '[]');
    // 过滤掉原先已有的 19 号测试数据，重新添加
    lessons = lessons.filter(l => l.date !== '2026-09-19');
    lessons.push(
      { id: 'ls-test-19-1', date: '2026-09-19', time: '10:00', subject: '英语', totalAmount: 600, teacher: 'Sarah', status: 'unpaid' },
      { id: 'ls-test-19-2', date: '2026-09-19', time: '14:00', subject: '物理', totalAmount: 450, teacher: '陈名师', status: 'unpaid' },
      { id: 'ls-test-19-3', date: '2026-09-19', time: '18:30', subject: '化学', totalAmount: 450, teacher: '王老师', status: 'unpaid' }
    );
    localStorage.setItem('owen_unified_lessons_v1', JSON.stringify(lessons));
    renderAll();
  });
  await page.waitForTimeout(400);

  // 3. 验证 19 号日历格子的当天费用总额徽标
  const day19Cell = await page.$('#tutoring-days-grid .day-cell:has(.day-number:text-is("19"))');
  if (!day19Cell) throw new Error('未找到 19 号日历格子');

  const badgeText = await day19Cell.$eval('.day-total-badge', el => el.textContent.trim());
  console.log(`✔ 19 号格子上检测到当天总额徽标: "${badgeText}"`);

  if (!badgeText.includes('1,500') && !badgeText.includes('1500')) {
    throw new Error(`当天总额计算错误: 期望包含 1,500，实际为 ${badgeText}`);
  }

  // 4. 验证底部汇总文字
  const cellText = await day19Cell.textContent();
  console.log('✔ 19 号日历格子全部内容摘要:\n', cellText.replace(/\s+/g, ' '));
  if (!cellText.includes('合计: ¥ 1,500') && !cellText.includes('¥ 1,500')) {
    throw new Error('未包含合计 1500');
  }

  // 5. 截图留存作为验收凭据
  const screenshotPath = path.resolve(__dirname, '../test-results/day-total-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`✔ 包含当天总额徽标的验收截图已保存至: ${screenshotPath}`);

  await browser.close();
  console.log('🎉 当天费用总额展示功能自动化测试 100% 通过！');
  process.exit(0);
})();
