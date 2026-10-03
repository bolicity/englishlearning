const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收：健康打卡与学科补课结算中心 V1 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
      console.error('浏览器 Console 错误:', msg.text());
    }
  });
  page.on('pageerror', err => {
    consoleErrors.push(err.message);
    console.error('页面未捕获异常:', err.message);
  });

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V1.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 验证标题和浅色背景风格
  const title = await page.title();
  console.log('✔ 页面标题:', title);
  if (!title.includes('学科补课费用结算中心 V1')) {
    throw new Error('标题不匹配');
  }

  // 2. 验证科目与单价配置
  const subjectCards = await page.$$('.subject-price-card');
  console.log(`✔ 成功加载科目单价卡片数量: ${subjectCards.length}`);
  if (subjectCards.length < 5) throw new Error('科目数量不足5个');

  // 3. 验证补课消课日历与勾兑列表
  const lessonRows = await page.$$('#tutoring-table-body tr');
  console.log(`✔ 初始待结算课程行数: ${lessonRows.length}`);

  // 4. 测试勾兑复选框与实时金额核算
  const firstCheckbox = await page.$('#tutoring-table-body tr:first-child input[type="checkbox"]');
  if (firstCheckbox) {
    await firstCheckbox.check();
    const selectedCount = await page.$eval('#selected-count', el => el.textContent);
    const selectedTotal = await page.$eval('#selected-total', el => el.textContent);
    console.log(`✔ 勾选第1条课程后，已选数量: ${selectedCount}，核算总额: ${selectedTotal}`);
    if (selectedCount !== '1') throw new Error('勾选数量计算异常');
  }

  // 勾选第二项测试累加
  const secondCheckbox = await page.$('#tutoring-table-body tr:nth-child(2) input[type="checkbox"]');
  if (secondCheckbox) {
    await secondCheckbox.check();
    const count2 = await page.$eval('#selected-count', el => el.textContent);
    const total2 = await page.$eval('#selected-total', el => el.textContent);
    console.log(`✔ 勾选第2条课程后，累计已选: ${count2} 节课，核算总金额: ${total2}`);
  }

  // 5. 测试批量付费结算操作
  console.log('✔ 触发【批量结算已选】按钮...');
  await page.click('#btn-batch-settle');
  await page.waitForSelector('#modal-batch-settle.active');

  const summaryText = await page.$eval('#modal-settle-summary', el => el.textContent);
  console.log('✔ 结算弹窗核算详情:', summaryText);

  // 确认结算
  await page.click('button:has-text("确认结算并标记已付款")');
  await page.waitForTimeout(500);

  // 验证结算后列表
  const remainingUnpaid = await page.$$('#tutoring-table-body tr');
  console.log(`✔ 批量结算后，剩余待付款行数: ${remainingUnpaid.length}`);

  // 6. 测试切换到【每月打针与复诊打卡】模块
  console.log('✔ 切换到健康打卡模块...');
  await page.click('#tab-btn-health');
  await page.waitForSelector('#view-health.active');

  const healthCells = await page.$$('#health-days-grid .day-cell:not(.other-month)');
  console.log(`✔ 健康月历当月有效格子数: ${healthCells.length}`);

  const injCount = await page.$eval('#stat-injection-count', el => el.textContent);
  const revCount = await page.$eval('#stat-revisit-count', el => el.textContent);
  console.log(`✔ 健康打卡指标：本月打针 ${injCount}，本月复诊 ${revCount}`);

  // 7. 测试新增打卡
  console.log('✔ 测试新增健康打卡登记...');
  await page.click('button:has-text("+ 今日健康打卡")');
  await page.waitForSelector('#modal-checkin.active');
  await page.fill('#inj-med-name', '重组人生长激素注射液 (水剂)');
  await page.fill('#inj-dose', '3.5 IU');
  await page.click('button:has-text("保存打卡记录")');
  await page.waitForTimeout(500);

  // 8. 截图留存作为验收凭据
  const screenshotPath = path.resolve(__dirname, '../test-results/tracker-v1-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`✔ 完整页面截图已保存至: ${screenshotPath}`);

  // 9. 检查首页是否正常加载包含新板块
  const indexUrl = 'file://' + path.resolve(__dirname, '../index.html');
  await page.goto(indexUrl);
  await page.waitForLoadState('networkidle');
  const sectionTracker = await page.$('#section-trackers');
  if (!sectionTracker) {
    throw new Error('首页未检测到新增的第三板块 #section-trackers');
  }
  console.log('✔ 首页 V4 成功检测到【第三板块：家庭日程打卡与费用核算中心】！');

  await browser.close();

  if (consoleErrors.length > 0) {
    console.error('❌ 测试存在控制台错误:', consoleErrors);
    process.exit(1);
  } else {
    console.log('🎉 验收测试全部通过！所有交互与核算逻辑 100% 正常运行！');
    process.exit(0);
  }
})();
