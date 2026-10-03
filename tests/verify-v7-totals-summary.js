const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收 V7：待付款与已付款费用总额汇总功能 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V7.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 注入确定性的测试课程数据：
  // 3 门未付课 (600 + 450 + 450 = 1500)
  // 2 门已付课 (500 + 500 = 1000)
  console.log('✔ 注入测试数据 (待付款 1500，已付款 1000) ...');
  await page.evaluate(() => {
    const testLessons = [
      { id: 'ls-v7-unpaid-1', date: '2026-09-19', time: '10:00', subject: '英语', totalAmount: 600, teacher: '唐老师', status: 'unpaid' },
      { id: 'ls-v7-unpaid-2', date: '2026-09-19', time: '14:00', subject: '物理', totalAmount: 450, teacher: '张老师', status: 'unpaid' },
      { id: 'ls-v7-unpaid-3', date: '2026-09-19', time: '18:30', subject: '化学', totalAmount: 450, teacher: '张老师', status: 'unpaid' },
      { id: 'ls-v7-paid-1', date: '2026-09-10', time: '10:00', subject: '数学', totalAmount: 500, teacher: '王老师', status: 'paid' },
      { id: 'ls-v7-paid-2', date: '2026-09-12', time: '14:00', subject: '数学', totalAmount: 500, teacher: '王老师', status: 'paid' }
    ];
    localStorage.setItem('owen_unified_lessons_v1', JSON.stringify(testLessons));
    renderAll();
  });
  await page.waitForTimeout(400);

  // 2. 检查右上角 Tab 按钮上的待付与已付汇总
  const tabUnpaidText = await page.$eval('#tab-filter-unpaid', el => el.innerText.replace(/\s+/g, ' '));
  const tabPaidText = await page.$eval('#tab-filter-paid', el => el.innerText.replace(/\s+/g, ' '));
  const tabAllText = await page.$eval('#tab-filter-all', el => el.innerText.replace(/\s+/g, ' '));

  console.log(`✔ Tab 待付款展示: [${tabUnpaidText}]`);
  console.log(`✔ Tab 已结清展示: [${tabPaidText}]`);
  console.log(`✔ Tab 全部展示: [${tabAllText}]`);

  if (!tabUnpaidText.includes('3') || !tabUnpaidText.includes('1,500')) {
    throw new Error(`待付款 Tab 统计错误: 期望3节¥1,500，实际: ${tabUnpaidText}`);
  }
  if (!tabPaidText.includes('2') || !tabPaidText.includes('1,000')) {
    throw new Error(`已结清 Tab 统计错误: 期望2节¥1,000，实际: ${tabPaidText}`);
  }
  if (!tabAllText.includes('5') || !tabAllText.includes('2,500')) {
    throw new Error(`全部 Tab 统计错误: 期望5节¥2,500，实际: ${tabAllText}`);
  }

  // 3. 检查操作栏上的常驻总额看板
  const barUnpaidAmount = await page.$eval('#bar-unpaid-amount', el => el.innerText.trim());
  const barPaidAmount = await page.$eval('#bar-paid-amount', el => el.innerText.trim());

  console.log(`✔ 操作栏看板 待付款总额: [${barUnpaidAmount}]`);
  console.log(`✔ 操作栏看板 已付款总额: [${barPaidAmount}]`);

  if (!barUnpaidAmount.includes('1,500')) {
    throw new Error(`操作栏待付款总额显示异常: ${barUnpaidAmount}`);
  }
  if (!barPaidAmount.includes('1,000')) {
    throw new Error(`操作栏已付款总额显示异常: ${barPaidAmount}`);
  }

  // 3.5 截取未付款与已付款费用总额汇总看板截图（结算前）
  const screenshotBeforePath = path.resolve(__dirname, '../test-results/v7-totals-before-settle.png');
  await page.evaluate(() => {
    document.querySelector('.reconciliation-panel').scrollIntoView();
  });
  await page.waitForTimeout(300);
  await page.screenshot({ path: screenshotBeforePath });
  console.log(`✔ 结算前费用总额看板截图已保存至: ${screenshotBeforePath}`);

  // 4. 模拟全选待付款课程并进行批量结算
  console.log('✔ 测试批量结算勾兑联动更新 ...');
  await page.click('#check-all-lessons');
  await page.waitForTimeout(200);

  const selectedCount = await page.$eval('#selected-count', el => el.innerText.trim());
  const selectedTotal = await page.$eval('#selected-total', el => el.innerText.trim());
  console.log(`✔ 全选成功，已选节数: ${selectedCount}，结算合计: ${selectedTotal}`);

  if (selectedCount !== '3' || !selectedTotal.includes('1,500')) {
    throw new Error(`全选核算合计异常: ${selectedCount}节, ${selectedTotal}`);
  }

  // 点击批量结算
  await page.click('#btn-batch-settle');
  await page.waitForTimeout(200);

  // 在弹窗中确认结算
  await page.click('button:has-text("确认结算并标记已付款")');
  await page.waitForTimeout(400);

  // 5. 校验结算后金额实时更新：待付款应归 0，已付款应变为 2,500
  const afterUnpaidAmount = await page.$eval('#bar-unpaid-amount', el => el.innerText.trim());
  const afterPaidAmount = await page.$eval('#bar-paid-amount', el => el.innerText.trim());
  const afterTabPaidText = await page.$eval('#tab-filter-paid', el => el.innerText.replace(/\s+/g, ' '));

  console.log(`✔ 结算后操作栏 待付款总额: [${afterUnpaidAmount}] (期望 ¥ 0)`);
  console.log(`✔ 结算后操作栏 已付款总额: [${afterPaidAmount}] (期望 ¥ 2,500)`);
  console.log(`✔ 结算后已结清 Tab: [${afterTabPaidText}] (期望 5节 · ¥2,500)`);

  if (!afterUnpaidAmount.includes('0')) {
    throw new Error(`结算后待付款总额未清零: ${afterUnpaidAmount}`);
  }
  if (!afterPaidAmount.includes('2,500')) {
    throw new Error(`结算后已付款总额未累加: ${afterPaidAmount}`);
  }

  // 6. 截图留存验收报告
  const screenshotPath = path.resolve(__dirname, '../test-results/v7-totals-verified.png');
  // 滚动到操作栏与表格区域完整截图
  await page.evaluate(() => {
    document.querySelector('.reconciliation-panel').scrollIntoView();
  });
  await page.waitForTimeout(300);
  await page.screenshot({ path: screenshotPath });

  console.log(`🎉 测试全部通过！验证截图已保存至: ${screenshotPath}`);
  await browser.close();
})();
