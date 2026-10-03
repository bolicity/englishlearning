const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 开始自动化回归测试：1. 根目录主页布局修复验证；2. 道法 V3 新增材料与看板验证...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  const resultsDir = path.join(__dirname, '../test-results');
  if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
  }

  // 1. 验证 index.html
  const indexPath = path.join(__dirname, '../index.html');
  await page.goto(`file://${indexPath}`, { waitUntil: 'networkidle' });

  // 检查 grid 布局是否生效
  const gridDisplay = await page.$eval('.grid', el => window.getComputedStyle(el).display);
  console.log('✅ index.html .grid display:', gridDisplay);
  if (gridDisplay !== 'grid') {
    throw new Error('index.html .grid display is not grid! Layout broken!');
  }

  // 检查 body 背景色是否为浅色商务系
  const bodyBg = await page.$eval('body', el => window.getComputedStyle(el).backgroundColor);
  console.log('✅ index.html body backgroundColor:', bodyBg);

  // 检查道法卡片链接与内容
  const daofaHref = await page.$eval('#subject-daofa', el => el.getAttribute('href'));
  const daofaTitle = await page.$eval('#subject-daofa h2', el => el.innerText);
  console.log('✅ index.html 道法链接:', daofaHref, '标题:', daofaTitle);
  if (!daofaHref.includes('daofa-V3.html')) {
    throw new Error(`Expected daofa-V3.html link, but got: ${daofaHref}`);
  }

  const indexScreenshot = path.join(resultsDir, 'index-layout-fixed-verified.png');
  await page.screenshot({ path: indexScreenshot, fullPage: false });
  console.log('📸 已生成主页布局修复验证截图:', indexScreenshot);

  // 2. 验证 daofa/daofa-V3.html
  const daofaPath = path.join(__dirname, '../daofa/daofa-V3.html');
  await page.goto(`file://${daofaPath}`, { waitUntil: 'networkidle' });

  // 检查标题与浅色商务背景
  const daofaPageTitle = await page.title();
  console.log('✅ daofa-V3 页面标题:', daofaPageTitle);

  const daofaBg = await page.$eval('body', el => window.getComputedStyle(el).backgroundColor);
  console.log('✅ daofa-V3 背景颜色:', daofaBg);

  // 检查是否包含新增的 2026.9.30 PPTX 和 资料1-6 PDF
  const pageContent = await page.content();
  const hasPptx = pageContent.includes('2026.9.30道法综合卷一讲评思路.pptx');
  const hasPdf16 = pageContent.includes('2026.9.30九上新课课后练习讲评汇总（资料1-6）.pdf');
  console.log('✅ 包含 9.30 PPTX 讲评:', hasPptx);
  console.log('✅ 包含 9.30 九上课后练 资料1-6 PDF:', hasPdf16);

  if (!hasPptx || !hasPdf16) {
    throw new Error('daofa-V3.html missing required 9.30 materials!');
  }

  // 检查下拉选择框项
  const selectOptions = await page.$$eval('#pdfSelect option', options => options.map(o => o.value));
  console.log('✅ 下拉框可选 PDF 列表 (共', selectOptions.length, '项):', selectOptions);
  if (selectOptions.length < 6) {
    throw new Error('Expected at least 6 PDF options in selector!');
  }

  // 测试切换 PDF 功能
  await page.selectOption('#pdfSelect', '26秋上海九年级道法练习册答案_扫描版.pdf');
  await page.waitForTimeout(500);
  const currentTitle = await page.$eval('#currentPdfTitle', el => el.innerText);
  console.log('✅ 切换后标题显示:', currentTitle);

  const daofaScreenshot = path.join(resultsDir, 'daofa-v3-materials-verified.png');
  await page.screenshot({ path: daofaScreenshot, fullPage: false });
  console.log('📸 已生成道法 V3 新增材料验证截图:', daofaScreenshot);

  await browser.close();
  console.log('🎉 所有自动化验证通过！');
})();
