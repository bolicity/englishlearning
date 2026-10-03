const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收 V8：全年12个月大规模紧凑按月日历 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1100 } });
  const page = await context.newPage();

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V8.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // ==========================================
  // 测试 1：学科补课日历 12 个月大规模紧凑矩阵
  // ==========================================
  console.log('✔ 测试 1：验证学科补课模块 12 个月大规模紧凑日历 ...');
  
  // 注入 9 月与 10 月的补课数据
  await page.evaluate(() => {
    const testLessons = [
      { id: 'ls-v8-1', date: '2026-09-19', time: '10:00', subject: '英语', totalAmount: 600, teacher: '唐老师', status: 'unpaid' },
      { id: 'ls-v8-2', date: '2026-09-19', time: '14:00', subject: '物理', totalAmount: 450, teacher: '张老师', status: 'unpaid' },
      { id: 'ls-v8-3', date: '2026-09-19', time: '18:30', subject: '化学', totalAmount: 450, teacher: '张老师', status: 'unpaid' },
      { id: 'ls-v8-4', date: '2026-10-05', time: '10:00', subject: '数学', totalAmount: 500, teacher: '王老师', status: 'paid' }
    ];
    localStorage.setItem('owen_unified_lessons_v1', JSON.stringify(testLessons));
    renderAll();
  });
  await page.waitForTimeout(300);

  // 验证 12 个月份卡片
  const tutoringMonthCards = await page.$$('#tutoring-year-matrix .mini-month-card');
  console.log(`✔ 补课日历渲染月份卡片数量: ${tutoringMonthCards.length} (期望: 12)`);
  if (tutoringMonthCards.length !== 12) {
    throw new Error(`补课日历未渲染完整 12 个月，实际卡片数: ${tutoringMonthCards.length}`);
  }

  // 验证 9 月卡片内的课程信息与 19 号单元格标记
  const month9Card = tutoringMonthCards[8]; // 9月 (索引8)
  const month9Text = await month9Card.innerText();
  console.log(`✔ 9月补课卡片内容摘要:\n${month9Text.substring(0, 80)}...`);
  if (!month9Text.includes('9月') || !month9Text.includes('3节') || !month9Text.includes('1,500')) {
    throw new Error(`9月卡片统计未正确显示 3节·¥1,500: ${month9Text}`);
  }

  const cell19 = await month9Card.$('.mini-day-cell.has-lesson:has-text("19")');
  if (!cell19) throw new Error('9月19号微型单元格未标记 has-lesson 样式');
  console.log('✔ 9月19号微型单元格成功呈现紧凑标记');

  // 点击微型单元格测试弹窗交互
  await cell19.click();
  await page.waitForTimeout(300);
  const isLessonModalActive = await page.$eval('#modal-lesson', el => el.classList.contains('active'));
  console.log(`✔ 点击 19 号微型格子成功唤起弹窗: ${isLessonModalActive}`);
  if (!isLessonModalActive) throw new Error('点击微型日历格子未成功弹出详情弹窗');

  // 关闭弹窗
  await page.click('#modal-lesson .modal-close');
  await page.waitForTimeout(200);

  // 截取学科补课 12 个月全景大规模紧凑截图
  const screenshotTutoring = path.resolve(__dirname, '../test-results/v8-tutoring-12months-compact.png');
  await page.screenshot({ path: screenshotTutoring });
  console.log(`✔ 补课模块 12 个月紧凑日历截图保存至: ${screenshotTutoring}`);

  // ==========================================
  // 测试 2：健康打卡日历 12 个月大规模紧凑矩阵
  // ==========================================
  console.log('\n✔ 测试 2：切换至健康打卡模块，验证 12 个月大规模紧凑日历 ...');
  await page.click('#tab-btn-health');
  await page.waitForTimeout(300);

  // 注入打针与复诊测试数据
  await page.evaluate(() => {
    const testCheckins = [
      { id: 'hk-v8-1', date: '2026-10-12', type: 'injection', medName: '生长激素', dose: '4.5IU', site: '左大腿' },
      { id: 'hk-v8-2', date: '2026-10-13', type: 'injection', medName: '生长激素', dose: '4.5IU', site: '右大腿' },
      { id: 'hk-v8-3', date: '2026-10-20', type: 'revisit', hospital: '儿童医院', doctor: '内分泌科李主任' }
    ];
    localStorage.setItem('owen_unified_health_v1', JSON.stringify(testCheckins));
    renderAll();
  });
  await page.waitForTimeout(300);

  // 验证健康日历 12 个月份卡片
  const healthMonthCards = await page.$$('#health-year-matrix .mini-month-card');
  console.log(`✔ 打针日历渲染月份卡片数量: ${healthMonthCards.length} (期望: 12)`);
  if (healthMonthCards.length !== 12) {
    throw new Error(`打针日历未渲染完整 12 个月，实际卡片数: ${healthMonthCards.length}`);
  }

  // 验证 10 月卡片
  const month10Card = healthMonthCards[9]; // 10月 (索引9)
  const month10Text = await month10Card.innerText();
  console.log(`✔ 10月打针卡片内容摘要:\n${month10Text.substring(0, 80)}...`);
  if (!month10Text.includes('10月') || !month10Text.includes('💉2') || !month10Text.includes('🏥1')) {
    throw new Error(`10月健康打卡未正确显示 💉2 🏥1: ${month10Text}`);
  }

  const cell12 = await month10Card.$('.mini-day-cell.has-injection:has-text("12")');
  const cell20 = await month10Card.$('.mini-day-cell.has-revisit:has-text("20")');
  if (!cell12 || !cell20) {
    throw new Error('10月12日(打针)或20日(复诊)微型单元格未标记对应样式');
  }
  console.log('✔ 10月12日打针与20日复诊单元格微型标记成功呈现');

  // 点击 12 日微型格子测试弹窗
  await cell12.click();
  await page.waitForTimeout(300);
  const isHealthModalActive = await page.$eval('#modal-checkin', el => el.classList.contains('active'));
  console.log(`✔ 点击健康微型格子成功唤起打卡弹窗: ${isHealthModalActive}`);
  if (!isHealthModalActive) throw new Error('点击健康日历格子未成功弹出打卡弹窗');

  await page.click('#modal-checkin .modal-close');
  await page.waitForTimeout(200);

  // 截取健康打卡 12 个月全景大规模紧凑截图
  const screenshotHealth = path.resolve(__dirname, '../test-results/v8-health-12months-compact.png');
  await page.screenshot({ path: screenshotHealth });
  console.log(`✔ 健康模块 12 个月紧凑日历截图保存至: ${screenshotHealth}`);

  console.log('\n🎉 全部自动化测试验收通过！双日历12个月大规模紧凑功能均完美生效！');
  await browser.close();
})();
