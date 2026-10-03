const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收 V6：按天选择费用结算功能 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V6.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 切换到 9 月份
  await page.click('#view-tutoring .month-selector button:has-text("‹")');
  await page.waitForTimeout(300);

  // 2. 注入 19 号的 3 门未付课程 (600 + 450 + 450 = 1500)
  await page.evaluate(() => {
    let lessons = JSON.parse(localStorage.getItem('owen_unified_lessons_v1') || '[]');
    lessons = lessons.filter(l => l.date !== '2026-09-19');
    lessons.push(
      { id: 'ls-v6-1', date: '2026-09-19', time: '10:00', subject: '英语', totalAmount: 600, teacher: '唐老师', status: 'unpaid' },
      { id: 'ls-v6-2', date: '2026-09-19', time: '14:00', subject: '物理', totalAmount: 450, teacher: '张老师', status: 'unpaid' },
      { id: 'ls-v6-3', date: '2026-09-19', time: '18:30', subject: '化学', totalAmount: 450, teacher: '张老师', status: 'unpaid' }
    );
    localStorage.setItem('owen_unified_lessons_v1', JSON.stringify(lessons));
    renderAll();
  });
  await page.waitForTimeout(300);

  // 3. 测试在日历格子上直接点击 19 号费用徽标一键全选当天
  console.log('✔ 测试日历格子：点击 19 号费用总额徽标 [¥ 1,500]...');
  const day19Wrap = await page.$('#tutoring-days-grid .day-cell:has(.day-number:text-is("19")) .day-total-wrap');
  if (!day19Wrap) throw new Error('未找到 19 号日历格子费用徽标');

  await day19Wrap.click();
  await page.waitForTimeout(300);

  let selectedCount = await page.$eval('#selected-count', el => el.textContent);
  let selectedTotal = await page.$eval('#selected-total', el => el.textContent);
  console.log(`✔ 点击日历后，已选课程数: ${selectedCount}，结算核算总额: ${selectedTotal}`);

  if (selectedCount !== '3' || !selectedTotal.includes('1,500')) {
    throw new Error(`按天勾选金额计算异常: 期望3节课¥1,500，实际: ${selectedCount}节, ${selectedTotal}`);
  }

  // 4. 测试下方表格中的按天分组栏
  const groupRow = await page.$('.date-group-row:has-text("2026-09-19")');
  console.log(`✔ 下方表格成功检测到 2026-09-19 日期分组小计栏: ${!!groupRow}`);
  if (!groupRow) throw new Error('未找到表格日期分组栏');

  // 5. 点击表格分组栏里的【取消勾选当天】
  console.log('✔ 点击表格中的【取消勾选当天】...');
  const toggleBtn = await groupRow.$('button:has-text("取消勾选当天")');
  if (!toggleBtn) throw new Error('未找到取消勾选当天按钮');
  await toggleBtn.click();
  await page.waitForTimeout(300);

  selectedCount = await page.$eval('#selected-count', el => el.textContent);
  console.log(`✔ 取消勾选当天后，已选数量: ${selectedCount} (应为 0)`);
  if (selectedCount !== '0') throw new Error('取消勾选当天失败');

  // 6. 再次点击【勾选当天全部费用】
  console.log('✔ 再次点击表格中的【勾选当天全部费用】...');
  const checkBtn = await groupRow.$('button:has-text("勾选当天全部费用")');
  await checkBtn.click();
  await page.waitForTimeout(300);

  selectedTotal = await page.$eval('#selected-total', el => el.textContent);
  console.log(`✔ 再次勾选后，核算总额恢复为: ${selectedTotal}`);
  if (!selectedTotal.includes('1,500')) throw new Error('再次勾选恢复总额失败');

  // 7. 保存验收截图
  const screenshotPath = path.resolve(__dirname, '../test-results/v6-day-selection-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`✔ V6 验收截图已保存至: ${screenshotPath}`);

  await browser.close();
  console.log('🎉 V6 按天选择费用结算功能自动化测试全部通过！');
  process.exit(0);
})();
