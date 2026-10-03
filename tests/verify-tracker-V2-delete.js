const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收 V2：日历一键删除功能 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  // 监听 dialog，自动确认 confirm 弹窗
  page.on('dialog', async dialog => {
    console.log(`✔ 捕获到确认弹窗: "${dialog.message()}" -> 自动确认删除`);
    await dialog.accept();
  });

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V2.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 验证 V2 标题
  const title = await page.title();
  console.log('✔ V2 页面标题:', title);
  if (!title.includes('V2')) throw new Error('V2 标题未正确体现');

  // 2. 切换到 9 月份日历 (用户的截图是 9 月)
  console.log('✔ 切换日历到上一月 (2026年9月)...');
  await page.click('#view-tutoring .month-selector button:has-text("‹")');
  await page.waitForTimeout(300);

  const monthLabel = await page.$eval('#tutoring-month-display', el => el.textContent);
  console.log(`✔ 当前显示月份: ${monthLabel}`);

  // 3. 验证日历格子里是否存在带有删除小叉 × 的徽标
  const badges = await page.$$('#tutoring-days-grid .badge-item');
  console.log(`✔ 9月份日历中找到补课徽标数量: ${badges.length}`);
  if (badges.length === 0) throw new Error('9月份未找到补课徽标');

  const delBtns = await page.$$('#tutoring-days-grid .badge-del-btn');
  console.log(`✔ 找到日历徽标内直达删除按钮 [×] 数量: ${delBtns.length}`);
  if (delBtns.length === 0) throw new Error('日历徽标内缺少删除按钮');

  // 4. 测试点击日历徽标上的 [×] 直接删除一条记录
  const initialBadgeCount = badges.length;
  console.log(`✔ 点击第1个日历徽标的 [×] 按钮执行秒删...`);
  await delBtns[0].click();
  await page.waitForTimeout(500);

  const remainingBadges = await page.$$('#tutoring-days-grid .badge-item');
  console.log(`✔ 删除后，9月份剩余徽标数量: ${remainingBadges.length} (原数量: ${initialBadgeCount})`);
  if (remainingBadges.length !== initialBadgeCount - 1) {
    throw new Error('日历快捷删除未生效');
  }

  // 5. 测试点击剩余的某个日历徽标，弹出修改/删除详情弹窗
  console.log('✔ 点击另一个日历徽标，测试详情弹窗中的【删除此记录】按钮...');
  const nextBadge = await page.$('#tutoring-days-grid .badge-item');
  await nextBadge.click();
  await page.waitForSelector('#modal-lesson.active');

  const deleteBtnInModal = await page.$('#btn-delete-current-lesson');
  const isVisible = await deleteBtnInModal.isVisible();
  console.log(`✔ 详情弹窗中【删除此记录】按钮可见状态: ${isVisible}`);
  if (!isVisible) throw new Error('弹窗中未显示删除此记录按钮');

  await deleteBtnInModal.click();
  await page.waitForTimeout(500);

  // 6. 测试右侧表格切换到【已结清】Tab，点击表格中的【删除】
  console.log('✔ 测试右侧表格：点击【已结清】标签切换...');
  await page.click('#tab-filter-paid');
  await page.waitForTimeout(300);

  const tableDelBtns = await page.$$('#tutoring-table-body button:has-text("删除")');
  console.log(`✔ 右侧【已结清】列表中找到删除按钮数量: ${tableDelBtns.length}`);
  if (tableDelBtns.length > 0) {
    console.log('✔ 点击右侧表格中的【删除】按钮...');
    await tableDelBtns[0].click();
    await page.waitForTimeout(500);
  }

  // 7. 保存验收截图
  const screenshotPath = path.resolve(__dirname, '../test-results/tracker-v2-delete-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`✔ V2 删除功能测试截图已保存至: ${screenshotPath}`);

  await browser.close();
  console.log('🎉 V2 删除功能自动化测试全部通过！');
  process.exit(0);
})();
