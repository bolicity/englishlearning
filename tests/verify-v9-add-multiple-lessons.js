const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 开始自动化测试验收 V9：点击日历自由新增补课记录与编辑已有记录功能 ...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1100 } });
  const page = await context.newPage();

  const fileUrl = 'file://' + path.resolve(__dirname, '../tracker/unified-tracker-V9.html');
  await page.goto(fileUrl);
  await page.waitForLoadState('networkidle');

  // 1. 注入 9 月 19 日已有 1 门英语课
  console.log('✔ 步骤 1：注入 9月19日 已有的一门英语课程 ...');
  await page.evaluate(() => {
    const initialLessons = [
      { id: 'ls-v9-orig-english', date: '2026-09-19', time: '10:00', subject: '英语', unitPrice: 600, totalAmount: 600, teacher: '唐老师', status: 'unpaid' }
    ];
    localStorage.setItem('owen_unified_lessons_v1', JSON.stringify(initialLessons));
    renderAll();
  });
  await page.waitForTimeout(300);

  // 2. 点击 9 月 19 日日历格子
  console.log('✔ 步骤 2：点击 9月19日 日历格子打开弹窗 ...');
  const month9Card = (await page.$$('#tutoring-year-matrix .mini-month-card'))[8];
  const cell19 = await month9Card.$('.mini-day-cell:has-text("19")');
  await cell19.click();
  await page.waitForTimeout(300);

  // 3. 校验弹窗默认必须为【新增】模式，而不是被篡改为修改老记录！
  const editId = await page.$eval('#lesson-edit-id', el => el.value);
  const modalTitle = await page.$eval('#lesson-modal-title', el => el.innerText);
  const saveBtnText = await page.$eval('#btn-save-lesson', el => el.innerText);
  const existingBoxVisible = await page.$eval('#day-existing-lessons-box', el => el.style.display !== 'none');

  console.log(`✔ 弹窗编辑ID: [${editId}] (期望为空)`);
  console.log(`✔ 弹窗标题: [${modalTitle}]`);
  console.log(`✔ 保存按钮文本: [${saveBtnText}]`);
  console.log(`✔ 当天已有课程横幅是否显示: ${existingBoxVisible}`);

  if (editId !== '') {
    throw new Error(`CRITICAL BUG: 点击日历仍然默认载入了已有记录ID [${editId}]，导致无法新增！`);
  }
  if (!saveBtnText.includes('新增')) {
    throw new Error(`保存按钮未体现新增语义: ${saveBtnText}`);
  }
  if (!existingBoxVisible) {
    throw new Error('未展示当天已有课程横幅');
  }

  // 4. 在当天新增第二门课：物理
  console.log('✔ 步骤 3：在当天新增第二门课程【物理】 ...');
  await page.selectOption('#lesson-subject-select', '物理');
  await page.waitForTimeout(100);
  await page.fill('#lesson-teacher', '张老师');
  await page.click('#btn-save-lesson');
  await page.waitForTimeout(400);

  // 5. 校验 localStorage 中当前必须有 2 节课（英语 + 物理）
  const lessonsAfterAdd = await page.evaluate(() => JSON.parse(localStorage.getItem('owen_unified_lessons_v1') || '[]'));
  console.log(`✔ 新增后 9月19日 课程数: ${lessonsAfterAdd.length} (期望为 2)`);
  const subjects = lessonsAfterAdd.map(l => l.subject);
  console.log(`✔ 当前科目列表: ${subjects.join(', ')}`);

  if (lessonsAfterAdd.length !== 2 || !subjects.includes('英语') || !subjects.includes('物理')) {
    throw new Error(`新增补课失败：老课程被意外覆盖或新课程未写入！当前科目: ${subjects.join(', ')}`);
  }

  // 6. 再次点击 9月19日 测试在弹窗内自由切换编辑与新增
  console.log('✔ 步骤 4：再次点击 9月19日，测试已有课程横幅中的【修改此课】与【切换新增】 ...');
  const reMonth9Card = (await page.$$('#tutoring-year-matrix .mini-month-card'))[8];
  const reCell19 = await reMonth9Card.$('.mini-day-cell:has-text("19")');
  await reCell19.click();
  await page.waitForTimeout(300);

  // 截取弹窗中显示 2 门已有课且处于新增态的高清截图
  const screenshotPath = path.resolve(__dirname, '../test-results/v9-add-and-edit-verified.png');
  await page.screenshot({ path: screenshotPath });
  console.log(`✔ 验收截图已保存至: ${screenshotPath}`);

  // 点击物理课右侧的【修改此课】
  await page.click('.existing-item-row:has-text("物理") button:has-text("修改此课")');
  await page.waitForTimeout(200);

  const editIdNow = await page.$eval('#lesson-edit-id', el => el.value);
  const saveBtnTextNow = await page.$eval('#btn-save-lesson', el => el.innerText);
  console.log(`✔ 切换编辑后 ID: [${editIdNow}]，保存按钮: [${saveBtnTextNow}] (期望为修改)`);

  if (!editIdNow || !saveBtnTextNow.includes('修改')) {
    throw new Error('未能成功切换到修改模式');
  }

  // 点击顶部的【+ 切换为新增下一节课】
  await page.click('button:has-text("切换为新增下一节课")');
  await page.waitForTimeout(200);

  const editIdReset = await page.$eval('#lesson-edit-id', el => el.value);
  const saveBtnTextReset = await page.$eval('#btn-save-lesson', el => el.innerText);
  console.log(`✔ 再次切回新增后 ID: [${editIdReset}]，保存按钮: [${saveBtnTextReset}] (期望重新清空并为新增)`);

  if (editIdReset !== '' || !saveBtnTextReset.includes('新增')) {
    throw new Error('未能成功从修改切回新增模式');
  }

  console.log('\n🎉 测试完全通过！点击日历自由新增、录入多节课与编辑修改完美修复！');
  await browser.close();
})();
