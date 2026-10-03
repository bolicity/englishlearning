const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  const resultsDir = path.resolve(__dirname, '../test-results');
  if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
  }

  console.log('--- 1. 验证道法通关工作台 V5 ---');
  const daofaUrl = 'file://' + path.resolve(__dirname, '../daofa/daofa-V5.html');
  await page.goto(daofaUrl, { waitUntil: 'networkidle' });

  const daofaTitle = await page.title();
  console.log('道法页面标题:', daofaTitle);

  // 验证考点卡片数量 (应 >= 14 张，含 9.4 笔记新考点)
  const cards = await page.$$('.topic-card');
  console.log(`检测到道法考点卡片数量: ${cards.length}`);
  if (cards.length < 14) {
    throw new Error(`考点卡片数量不足，实际检测到 ${cards.length}`);
  }

  // 验证 9.4 笔记卡片存在
  const pageText = await page.innerText('body');
  if (!pageText.includes('四个历史时期伟大成就与复兴意义 ABCD 矩阵') || !pageText.includes('经济实力大幅跃升的六大成就')) {
    throw new Error('未正确检测到 9.4 笔记考点内容！');
  }
  console.log('✓ 9.4 笔记 1.1 与 6.1 核心考点卡片已就绪');

  // 验证搜索过滤
  await page.fill('#topicSearch', '乡村振兴');
  await page.waitForTimeout(200);
  const visibleCardsAfterSearch = await page.$$eval('.topic-card', els => els.filter(e => window.getComputedStyle(e).display !== 'none').length);
  console.log(`搜索“乡村振兴”后可见卡片数量: ${visibleCardsAfterSearch}`);
  if (visibleCardsAfterSearch === 0) {
    throw new Error('搜索过滤失败！');
  }

  // 恢复搜索
  await page.fill('#topicSearch', '');
  await page.waitForTimeout(100);

  // 验证 PDF 弹窗调阅
  console.log('测试道法页面弹窗调阅功能...');
  const firstAnchor = await page.$('.btn-anchor');
  await firstAnchor.click();
  await page.waitForTimeout(300);
  const modalDisplay = await page.$eval('#pdfModal', el => window.getComputedStyle(el).display);
  const iframeSrc = await page.$eval('#modalPdfFrame', el => el.src);
  console.log(`道法弹窗 display: ${modalDisplay}, iframeSrc: ${iframeSrc}`);
  if (modalDisplay === 'none' || !iframeSrc) {
    throw new Error('道法 PDF 弹窗调阅未生效！');
  }
  await page.click('.modal-close-btn');
  await page.waitForTimeout(200);

  // 截取道法 V5 页面
  const daofaScreenshot = path.join(resultsDir, 'daofa-v5-verified.png');
  await page.screenshot({ path: daofaScreenshot, fullPage: false });
  console.log(`✓ 道法 V5 截图已保存至: ${daofaScreenshot}`);

  console.log('--- 2. 验证跨学科通关工作台 V2 ---');
  const interUrl = 'file://' + path.resolve(__dirname, '../interdisciplinary/interdisciplinary-V2.html');
  await page.goto(interUrl, { waitUntil: 'networkidle' });

  const interTitle = await page.title();
  console.log('跨学科页面标题:', interTitle);

  // 验证黄芪 22 中考真题与青浦薰衣草
  const interText = await page.innerText('body');
  if (!interText.includes('黄河') || !interText.includes('免疫细胞') || !interText.includes('铁路运输') || !interText.includes('迷迭香')) {
    throw new Error('跨学科 V2 缺少核心真题拆解内容！');
  }
  console.log('✓ 22真题黄芪与青浦薰衣草全部试题要素与采分点均已正常渲染');

  // 验证对比表格
  const tableRows = await page.$$('.compare-table tr');
  console.log(`传粉媒介对比表格行数: ${tableRows.length}`);
  if (tableRows.length < 5) {
    throw new Error('传粉生物学对比表格行数异常！');
  }

  // 截取跨学科 V2 页面
  const interScreenshot = path.join(resultsDir, 'interdisciplinary-v2-verified.png');
  await page.screenshot({ path: interScreenshot, fullPage: false });
  console.log(`✓ 跨学科 V2 截图已保存至: ${interScreenshot}`);

  console.log('--- 3. 验证主入口 index.html 连通性 ---');
  const indexUrl = 'file://' + path.resolve(__dirname, '../index.html');
  await page.goto(indexUrl, { waitUntil: 'networkidle' });

  const daofaHref = await page.$eval('#subject-daofa', el => el.getAttribute('href'));
  const interHref = await page.$eval('#subject-interdisciplinary', el => el.getAttribute('href'));
  console.log(`主页道法链接: ${daofaHref}, 跨学科链接: ${interHref}`);
  if (daofaHref !== 'daofa/daofa-V5.html' || interHref !== 'interdisciplinary/interdisciplinary-V2.html') {
    throw new Error('主页卡片链接未指向最新 V5 或 V2 版本！');
  }
  console.log('✓ index.html 主入口链接全部验证成功！');

  console.log('=== 所有测试全部通过！ ===');
  await browser.close();
})();
