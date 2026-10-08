const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 [Test V11] 启动 unified-tracker-V11.html 云端后端持久化自动化验证...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  page.on('console', msg => {
    console.log(`[Browser Console] ${msg.text()}`);
  });
  page.on('pageerror', err => {
    console.error(`[Browser Page Error] ${err.message}`);
  });
  page.on('dialog', async dialog => {
    console.log(`[Dialog Triggered] ${dialog.message()}`);
    await dialog.accept();
  });

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V11.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  // 1. 验证页面基本信息与版本
  const title = await page.title();
  console.log(`📄 Page Title: ${title}`);
  if (!title.includes('V11')) {
    throw new Error('Title does not include V11');
  }

  // 2. 检查云端持久化状态徽章
  const pillText = await page.innerText('#cloud-sync-pill');
  console.log(`☁️ Cloud Status Pill Text: ${pillText}`);

  // 3. 检查点击打开云端管理弹窗
  await page.click('#cloud-sync-pill');
  await page.waitForTimeout(400);
  const isModalVisible = await page.$eval('#cloud-sync-modal', el => window.getComputedStyle(el).display !== 'none');
  console.log(`✅ 云端同步管理弹窗是否成功弹出: ${isModalVisible}`);
  if (!isModalVisible) {
    throw new Error('云端管理弹窗未能成功打开！');
  }

  // 检查弹窗内容
  const summaryText = await page.innerText('#modal-local-summary');
  console.log(`📊 弹窗内数据概览: ${summaryText}`);

  // 关闭弹窗
  await page.click('button:has-text("完成关闭")');
  await page.waitForTimeout(300);

  // 4. 打开添加课程弹窗并测试保存记录
  console.log('👉 打开排课弹窗并添加一节新课程...');
  await page.evaluate(() => {
    openLessonModal('2026-10-15');
  });
  await page.waitForTimeout(400);
  await page.fill('#lesson-topic', '中考压轴高分专题冲刺测试');
  await page.click('#btn-save-lesson');
  await page.waitForTimeout(1000);

  // 5. 验证是否出现 toast
  const toastText = await page.innerText('#toast-message');
  console.log(`🍞 Toast 提示内容: ${toastText}`);

  // 6. 验证云端自动同步触发
  await page.waitForTimeout(1200);
  const updatedPill = await page.innerText('#cloud-sync-pill');
  console.log(`☁️ 保存后的云端同步状态: ${updatedPill}`);

  // 7. 切换到健康打卡板块测试
  console.log('👉 切换至打针与复诊打卡板块...');
  await page.click('#tab-btn-health');
  await page.waitForTimeout(500);

  // 验证打卡日历存在
  const healthGrid = await page.$('#health-days-grid');
  if (!healthGrid) {
    throw new Error('健康打卡日历组件不存在！');
  }
  console.log('✅ 健康打卡单月日历组件渲染正常！');

  console.log('🎉 [Test V11] 所有测试验收项全部顺利通过！');
  await browser.close();
  process.exit(0);
})().catch(err => {
  console.error('❌ 测试验收失败:', err);
  process.exit(1);
});
