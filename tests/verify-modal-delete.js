const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收：在弹窗内直接删除课程记录 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  page.on('dialog', async dialog => {
    console.log(`✔ 自动确认弹窗: "${dialog.message()}"`);
    await dialog.accept();
  });

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V3.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 切换到 9 月份
  console.log('✔ 切换到 2026 年 9 月...');
  await page.click('#view-tutoring .month-selector button:has-text("‹")');
  await page.waitForTimeout(300);

  // 2. 点击 9月20日 格子 (正如用户截图所示)
  console.log('✔ 点击 20 号格子...');
  const day20Cell = await page.$('#tutoring-days-grid .day-cell:has(.day-number:text-is("20"))');
  if (!day20Cell) throw new Error('未找到 20 号日历格子');
  await day20Cell.click();
  await page.waitForTimeout(400);

  // 3. 验证弹窗已弹出，并且左下角红色删除按钮清晰可见！
  const modal = await page.$('#modal-lesson.active');
  if (!modal) throw new Error('弹窗未激活');

  const deleteBtn = await page.$('#btn-delete-current-lesson');
  const isVisible = await deleteBtn.isVisible();
  const btnText = await deleteBtn.textContent();
  console.log(`✔ 弹窗左下角删除按钮可见: ${isVisible}, 文本: "${btnText.trim()}"`);

  if (!isVisible) {
    throw new Error('弹窗内删除按钮未显示！');
  }

  // 4. 截图截取弹窗，证明删除按钮已就绪
  const screenshotPath = path.resolve(__dirname, '../test-results/modal-delete-button-ready.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`✔ 截图已保存至: ${screenshotPath}`);

  // 5. 点击左下角红色【删除此记录】按钮
  console.log('✔ 点击弹窗内的【删除此记录】按钮...');
  await deleteBtn.click();
  await page.waitForTimeout(500);

  // 6. 验证弹窗已自动关闭，且 20 号格子的补课徽标已消失
  const isModalClosed = !(await page.$('#modal-lesson.active'));
  console.log(`✔ 弹窗是否已关闭: ${isModalClosed}`);
  if (!isModalClosed) throw new Error('删除后弹窗未关闭');

  const day20Badges = await page.$$('#tutoring-days-grid .day-cell:has(.day-number:text-is("20")) .badge-item');
  console.log(`✔ 20号格子里剩余补课徽标数量: ${day20Badges.length} (应为0)`);
  if (day20Badges.length !== 0) throw new Error('20号补课记录未被成功删除！');

  await browser.close();
  console.log('🎉 弹窗内直接删除功能测试全部通过！完美解决！');
  process.exit(0);
})();
