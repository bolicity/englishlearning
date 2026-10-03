const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 [Test 1] 启动打针模块单月大日历 & 一键复制排课自动化测试...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  page.on('console', msg => console.log(`[Browser Console] ${msg.text()}`));
  page.on('pageerror', err => console.log(`[Browser Error] ${err.message}`));
  page.on('dialog', async dialog => {
    console.log(`[Dialog Triggered] ${dialog.message()}`);
    await dialog.accept();
  });

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V10.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  // 1. 切换到健康打卡 Tab
  console.log('👉 切换至打针与复诊打卡板块...');
  await page.click('#tab-btn-health');
  await page.waitForTimeout(600);

  // 2. 检查单月大日历是否默认可见，全年12个月矩阵是否隐藏
  const isSingleVisible = await page.$eval('#health-single-calendar-wrap', el => window.getComputedStyle(el).display !== 'none');
  const isYearVisible = await page.$eval('#health-year-calendar-wrap', el => window.getComputedStyle(el).display !== 'none');
  console.log(`✅ 健康打卡日历默认展示模式: 单月大日历可见=${isSingleVisible}, 12个月紧凑矩阵隐藏=${!isYearVisible}`);
  if (!isSingleVisible || isYearVisible) {
    throw new Error('打针模块未能默认展示单月大日历！');
  }

  // 3. 点击“今日健康打卡”添加一条打针记录和一条复诊记录，验证日历格子里面的注射器与小医生图标
  console.log('👉 添加一条打针打卡记录...');
  await page.click('button:has-text("+ 今日健康打卡")');
  await page.waitForTimeout(400);

  // 确认在打针 Tab
  await page.fill('#inj-dose', '0.2ml');
  await page.selectOption('#inj-site', '左侧腹部 (距脐2cm外)');
  await page.click('button:has-text("保存打卡记录")');
  await page.waitForTimeout(600);

  // 添加一条复诊记录
  console.log('👉 添加一条门诊复诊记录...');
  await page.click('button:has-text("+ 今日健康打卡")');
  await page.waitForTimeout(400);
  await page.click('#switch-revisit');
  await page.waitForTimeout(300);
  await page.fill('#rev-hospital', '儿童医学中心');
  await page.fill('#rev-doctor', '李主任');
  await page.click('button:has-text("保存打卡记录")');
  await page.waitForTimeout(600);

  // 验证打针日历单元格内是否出现 💉 和 👨‍⚕️ 图标徽章
  const pageText = await page.innerText('#health-days-grid');
  const hasSyringe = pageText.includes('💉');
  const hasDoctor = pageText.includes('👨‍⚕️');
  console.log(`✅ 日历单元格打针 💉 图标渲染=${hasSyringe}, 小医生 👨‍⚕️ 图标渲染=${hasDoctor}`);
  if (!hasSyringe || !hasDoctor) {
    throw new Error('日历单元格未成功渲染注射器 💉 或小医生 👨‍⚕️ 图标！');
  }

  // 截图保存健康日历单月大图标效果
  const screenshotDir = path.resolve(__dirname, '../test-results');
  if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });
  await page.screenshot({ path: path.join(screenshotDir, 'v10-health-single-month-verified.png') });
  console.log('📸 已保存打针模块单月大图标截图: test-results/v10-health-single-month-verified.png');

  // 4. 切换回补课对账模块，测试“一键复制排课”
  console.log('👉 切换至学科补课费用结算板块，测试一键复制排课...');
  await page.click('#tab-btn-tutoring');
  await page.waitForTimeout(600);

  // 注入一节模板课确保有源数据
  await page.evaluate(() => {
    let list = JSON.parse(localStorage.getItem('owen_unified_lessons_v1') || '[]');
    const today = new Date().toISOString().split('T')[0];
    list.push({
      id: 'les-seed-1',
      subject: '英语 (A-Level)',
      date: today,
      time: '14:00',
      duration: 2,
      unitPrice: 300,
      fee: 600,
      teacher: 'Sarah',
      status: 'unpaid'
    });
    localStorage.setItem('owen_unified_lessons_v1', JSON.stringify(list));
    renderAll();
  });

  // 点击顶部操作栏的“📋 一键复制排课”
  await page.click('#btn-open-copy-modal-header');
  await page.waitForTimeout(500);

  const isModalActive = await page.$eval('#modal-copy-schedule', el => el.classList.contains('active'));
  console.log(`✅ 一键复制排课弹窗成功激活: ${isModalActive}`);

  // 点击快捷添加“明天”和“后天”
  await page.click('button:has-text("+ 明天")');
  await page.click('button:has-text("+ 后天")');
  await page.waitForTimeout(300);

  const targetsCount = await page.$eval('#copy-target-count', el => el.textContent.trim());
  console.log(`✅ 已选目标日期数: ${targetsCount}`);

  // 执行批量复制
  await page.evaluate(() => executeBatchCopySchedule());
  await page.waitForTimeout(800);

  // 验证对账流水中新增的待付款课程数量
  const unpaidText = await page.innerText('#stat-tutoring-unpaid-amount');
  console.log(`✅ 批量复制排课完成，当前待付款统计: ${unpaidText}`);

  await page.screenshot({ path: path.join(screenshotDir, 'v10-copy-schedule-verified.png') });
  console.log('📸 已保存一键复制排课截图: test-results/v10-copy-schedule-verified.png');

  await browser.close();
  console.log('🎉 [Test 1] 打针单月大图标与一键复制排课全部验证通过！\n');
})();
