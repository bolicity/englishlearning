const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收 V5：紧凑横排科目 + 上下通栏排版 + 当天费用总额 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V5.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 验证标题
  const title = await page.title();
  console.log('✔ V5 页面标题:', title);
  if (!title.includes('V5')) throw new Error('V5 标题不匹配');

  // 2. 验证科目卡片排版紧凑度
  const subjectCard = await page.$('.subject-price-card');
  const cardBox = await subjectCard.boundingBox();
  console.log(`✔ 科目卡片尺寸: 高度 ${cardBox.height}px, 宽度 ${cardBox.width}px (紧凑精炼)`);
  if (cardBox.height > 65) {
    throw new Error(`科目卡片高度超过65px，不够紧凑: ${cardBox.height}`);
  }

  // 3. 验证排版为上下通栏 (tutoring-grid 为 flex-direction: column)
  const isVertical = await page.$eval('.tutoring-grid', el => {
    const style = window.getComputedStyle(el);
    return style.display === 'flex' && style.flexDirection === 'column';
  });
  console.log(`✔ 补课日历与对账表格是否为上下通栏排版: ${isVertical}`);
  if (!isVertical) throw new Error('排版未改为上下通栏！');

  // 4. 验证表格全宽展开 (宽度应大于 1000px)
  const tablePanel = await page.$('.reconciliation-panel');
  const tableBox = await tablePanel.boundingBox();
  console.log(`✔ 勾兑对账表格面板宽度: ${tableBox.width}px (全宽展开，告别右侧狭窄)`);
  if (tableBox.width < 1000) {
    throw new Error('表格面板未全宽展开');
  }

  // 5. 切换到 9 月并测试 19 号当天费用总额
  await page.click('#view-tutoring .month-selector button:has-text("‹")');
  await page.waitForTimeout(300);

  await page.evaluate(() => {
    let lessons = JSON.parse(localStorage.getItem('owen_unified_lessons_v1') || '[]');
    lessons = lessons.filter(l => l.date !== '2026-09-19');
    lessons.push(
      { id: 'ls-v5-1', date: '2026-09-19', time: '10:00', subject: '英语', totalAmount: 600, teacher: '唐老师', status: 'unpaid' },
      { id: 'ls-v5-2', date: '2026-09-19', time: '14:00', subject: '物理', totalAmount: 450, teacher: '张老师', status: 'unpaid' },
      { id: 'ls-v5-3', date: '2026-09-19', time: '18:30', subject: '化学', totalAmount: 450, teacher: '张老师', status: 'unpaid' }
    );
    localStorage.setItem('owen_unified_lessons_v1', JSON.stringify(lessons));
    renderAll();
  });
  await page.waitForTimeout(300);

  const day19Badge = await page.$eval('#tutoring-days-grid .day-cell:has(.day-number:text-is("19")) .day-total-badge', el => el.textContent.trim());
  console.log(`✔ 19 号日历格子当天总额显示: "${day19Badge}" (期望包含 1,500)`);
  if (!day19Badge.includes('1,500')) throw new Error('当天总额徽标计算不正确');

  // 6. 截图作为验收证据
  const screenshotPath = path.resolve(__dirname, '../test-results/v5-compact-vertical-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`✔ V5 验收全屏截图已保存至: ${screenshotPath}`);

  await browser.close();
  console.log('🎉 V5 紧凑上下通栏版所有测试 100% 通过！');
  process.exit(0);
})();
