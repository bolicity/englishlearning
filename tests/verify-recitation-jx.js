const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🚀 [Test JX] 启动语文基础题库答案解析专项自动化测试...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 } });
  const page = await context.newPage();

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(err.message));

  const url = 'file://' + path.resolve(__dirname, '../chinese/recitation-bank-V1.html');
  await page.goto(url, { waitUntil: 'networkidle' });

  // 1. 验证左下角解析统计数量为 1055 / 1055
  const jxLabel = await page.innerText('#jx-label');
  console.log(`📊 统计栏解析显示: "${jxLabel}"`);
  if (!jxLabel.includes('1055 / 1055')) {
    throw new Error(`解析题目数量未达到 1055 全覆盖，当前为: ${jxLabel}`);
  }

  // 2. 验证第一题（成语第1题）的解析渲染
  const ansBox = await page.$('#ansbox');
  if (!ansBox) throw new Error('答案容器不存在！');
  
  // 检查是否有解析模块
  const jxEl = await page.$('.card .jx');
  if (!jxEl) throw new Error('第1题卡片内未找到 .jx 解析模块！');

  const jxTitle = await page.innerText('.card .jx .jxlabel');
  console.log(`🏷️ 解析标题: "${jxTitle}"`);
  if (!jxTitle.includes('解析 · 为什么是这个答案')) {
    throw new Error(`解析标题文字不符: ${jxTitle}`);
  }

  const jxText = await page.innerText('.card .jx .jxtext');
  console.log(`📝 第1题解析正文预览: ${jxText.substring(0, 80)}...`);
  if (!jxText.includes('逢场作戏')) {
    throw new Error('成语第1题解析内容缺少“逢场作戏”核心考点解析！');
  }

  // 3. 验证解析开关切换（#f-jx）
  console.log('👉 测试解析显隐开关...');
  const jxBtn = await page.$('#f-jx');
  await jxBtn.click();
  await page.waitForTimeout(200);
  const isHidden = await page.evaluate(() => document.body.classList.contains('nojx'));
  if (!isHidden) throw new Error('点击隐藏解析后 body 未增加 nojx 类！');

  await jxBtn.click();
  await page.waitForTimeout(200);
  const isShownAgain = await page.evaluate(() => !document.body.classList.contains('nojx'));
  if (!isShownAgain) throw new Error('重新开启解析后 body 未移除 nojx 类！');

  // 4. 测试切换板块抽查
  console.log('👉 测试切换板块（词语理解与运用、句子排序、语法综合）...');
  // 点击第2个板块（词语理解与运用）
  const secCiyu = await page.$('.sec:has-text("词语理解与运用")');
  if (secCiyu) {
    await secCiyu.click();
    await page.waitForTimeout(300);
    const ciyuJx = await page.innerText('.card .jx .jxtext');
    console.log(`📝 词语理解第1题解析预览: ${ciyuJx.substring(0, 60)}...`);
    if (!ciyuJx.includes('原本') && !ciyuJx.includes('沙子')) {
      throw new Error('词语第1题解析内容异常！');
    }
  }

  // 点击语法综合
  const secGrammar = await page.$('.sec:has-text("语法综合")');
  if (secGrammar) {
    await secGrammar.click();
    await page.waitForTimeout(300);
    const grammarJx = await page.innerText('.card .jx .jxtext');
    console.log(`📝 语法综合第1题解析预览: ${grammarJx.substring(0, 60)}...`);
    if (!grammarJx.includes('递进关系') && !grammarJx.includes('先人不仅')) {
      throw new Error('语法综合第1题解析内容异常！');
    }
  }

  // 5. 验证速览模式
  console.log('👉 切换至【速览】模式并检查解析展示...');
  await page.click('#m-browse');
  await page.waitForTimeout(400);

  const browseJxCount = await page.$$eval('.li-jx', els => els.length);
  console.log(`📋 当前筛选可见题目中带解析条数: ${browseJxCount}`);
  if (browseJxCount === 0) throw new Error('速览模式未渲染解析条目！');

  // 检查速览列表第一条解析文字
  const firstLiJx = await page.innerText('.li:first-child .li-jx');
  console.log(`📋 速览第一条解析预览: ${firstLiJx.substring(0, 60)}...`);

  if (errors.length > 0) {
    throw new Error(`页面发生 JS 控制台错误: ${errors.join(', ')}`);
  }

  console.log('🎉 [Test JX] 语文基础题库全量解析自动化测试 100% 验收通过！零 JS 错误！');
  await browser.close();
  process.exit(0);
})().catch(err => {
  console.error('❌ 测试验收失败:', err);
  process.exit(1);
});
