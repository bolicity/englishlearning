const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 [Test Picker] 启动语文基础题库【选题面板与进度记忆】自动化测试...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => {
    consoleErrors.push(err.message);
  });

  const fileUrl = 'file://' + path.resolve(__dirname, '../chinese/recitation-bank-V1.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  // 1. 验证默认加载状态
  console.log('👉 1. 验证默认初次加载状态...');
  const initPillText = await page.innerText('#open-picker-btn');
  console.log(`   底栏选题按钮文字: "${initPillText.trim().replace(/\s+/g, ' ')}"`);
  if (!initPillText.includes('第 1')) throw new Error('初次进入未默认在第 1 题！');

  const topPickerText = await page.innerText('#top-picker-btn');
  console.log(`   顶栏选题按钮文字: "${topPickerText.trim()}"`);
  if (!topPickerText.includes('第1题')) throw new Error('顶栏选题按钮未展示当前题号！');

  // 2. 测试点击底栏【第 1 / 1055 题 📋 选题 ▾】打开弹窗
  console.log('👉 2. 测试点击底栏选题卡按钮打开弹窗...');
  await page.click('#open-picker-btn');
  await page.waitForTimeout(300);
  const isModalVisible = await page.$eval('#picker-modal', el => el.classList.contains('show'));
  console.log(`   选题面板是否弹出: ${isModalVisible}`);
  if (!isModalVisible) throw new Error('点击选题按钮未弹出选题面板！');

  const gridButtons = await page.$$eval('.q-btn', els => els.length);
  console.log(`   答题卡题号按钮总数: ${gridButtons}`);
  if (gridButtons === 0) throw new Error('题卡网格未成功渲染！');

  // 3. 测试通过输入框跳至第 25 题
  console.log('👉 3. 测试在选题卡输入框中输入 25 并点击前往...');
  await page.fill('#jump-val', '25');
  await page.click('#jump-submit-btn');
  await page.waitForTimeout(300);

  const isModalClosed = await page.$eval('#picker-modal', el => !el.classList.contains('show'));
  console.log(`   跳题后弹窗是否自动关闭: ${isModalClosed}`);
  if (!isModalClosed) throw new Error('跳题后弹窗未关闭！');

  const pillText25 = await page.innerText('#open-picker-btn');
  console.log(`   跳转后底栏按钮文字: "${pillText25.trim().replace(/\s+/g, ' ')}"`);
  if (!pillText25.includes('第 25')) throw new Error('跳题后未定位到第 25 题！');

  const topPicker25 = await page.innerText('#top-picker-btn');
  console.log(`   跳转后顶栏按钮文字: "${topPicker25.trim()}"`);
  if (!topPicker25.includes('第25题')) throw new Error('顶栏选题按钮未同步到第 25 题！');

  // 4. 测试页面刷新后的进度恢复记忆（不每次都回到第1题）
  console.log('👉 4. 测试页面刷新，验证是否恢复记忆第 25 题（不再回到第1题）...');
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForTimeout(300);

  const reloadedPillText = await page.innerText('#open-picker-btn');
  console.log(`   刷新后底栏按钮文字: "${reloadedPillText.trim().replace(/\s+/g, ' ')}"`);
  if (!reloadedPillText.includes('第 25')) throw new Error('刷新后未能恢复至上次学习的第 25 题！');

  const hasPosBanner = await page.$('#pos-banner');
  console.log(`   进度恢复提示横幅是否存在: ${!!hasPosBanner}`);
  if (!hasPosBanner) throw new Error('未展示进度恢复提示横幅！');

  const bannerText = await page.innerText('#pos-banner');
  console.log(`   横幅内容: "${bannerText.trim()}"`);

  // 5. 测试横幅上的【从第1题重新开始】
  console.log('👉 5. 测试点击【从第1题重新开始】...');
  await page.click('.pos-banner-btn');
  await page.waitForTimeout(300);
  const resetPillText = await page.innerText('#open-picker-btn');
  console.log(`   重置后题号: "${resetPillText.trim().replace(/\s+/g, ' ')}"`);
  if (!resetPillText.includes('第 1')) throw new Error('点击从第1题重新开始失败！');

  // 6. 测试按键快捷翻题（Shift + ArrowRight 快翻 10 题）
  console.log('👉 6. 测试键盘快捷键 Shift+ArrowRight 快翻 10 题...');
  await page.keyboard.press('Shift+ArrowRight');
  await page.waitForTimeout(200);
  const shiftText = await page.innerText('#open-picker-btn');
  console.log(`   快翻10题后文字: "${shiftText.trim().replace(/\s+/g, ' ')}"`);
  if (!shiftText.includes('第 11')) throw new Error('Shift+ArrowRight 快翻 10 题失败！');

  // 7. 测试快捷键 G 打开选题面板，Escape 关闭
  console.log('👉 7. 测试键盘 G 键唤起面板，Esc 键关闭...');
  await page.keyboard.press('KeyG');
  await page.waitForTimeout(200);
  const gModalShow = await page.$eval('#picker-modal', el => el.classList.contains('show'));
  console.log(`   G 键唤起面板: ${gModalShow}`);
  if (!gModalShow) throw new Error('键盘 G 键未打开选题面板！');

  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);
  const escModalHide = await page.$eval('#picker-modal', el => !el.classList.contains('show'));
  console.log(`   Esc 键关闭面板: ${escModalHide}`);
  if (!escModalHide) throw new Error('键盘 Esc 键未关闭选题面板！');

  // 8. 测试板块记忆切换
  console.log('👉 8. 测试板块独立学习位置记忆...');
  // 切换到成语板块
  await page.click('.sec[data-sid="chengyu"]');
  await page.waitForTimeout(300);
  // 打开选题弹窗并跳到成语第 15 题
  await page.click('#top-picker-btn');
  await page.waitForTimeout(200);
  await page.fill('#jump-val', '15');
  await page.click('#jump-submit-btn');
  await page.waitForTimeout(200);
  const cyPill = await page.innerText('#open-picker-btn');
  console.log(`   成语板块跳转至: "${cyPill.trim().replace(/\s+/g, ' ')}"`);

  // 切换到词语板块
  await page.click('.sec[data-sid="ciyu"]');
  await page.waitForTimeout(300);
  // 跳到词语第 8 题
  await page.click('#top-picker-btn');
  await page.waitForTimeout(200);
  await page.fill('#jump-val', '8');
  await page.click('#jump-submit-btn');
  await page.waitForTimeout(200);
  const ciyuPill = await page.innerText('#open-picker-btn');
  console.log(`   词语板块跳转至: "${ciyuPill.trim().replace(/\s+/g, ' ')}"`);

  // 切回成语板块：应自动回到第 15 题！
  await page.click('.sec[data-sid="chengyu"]');
  await page.waitForTimeout(300);
  const cyBackPill = await page.innerText('#open-picker-btn');
  console.log(`   切回成语板块后自动恢复至: "${cyBackPill.trim().replace(/\s+/g, ' ')}"`);
  if (!cyBackPill.includes('第 15')) throw new Error('板块切换后未自动恢复该板块上次学习题号！');

  // 9. 检查控制台报错
  if (consoleErrors.length > 0) {
    console.error('❌ 测试期间存在控制台报错:', consoleErrors);
    throw new Error('存在控制台报错');
  }

  console.log('🎉 [Test Passed] 所有选题面板交互与进度记忆测试 100% 通过！');
  await browser.close();
})();
