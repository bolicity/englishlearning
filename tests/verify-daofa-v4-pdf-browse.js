const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('🚀 开始自动化验收：2026.9.30道法综合卷一讲评思路 PDF 网页直接浏览功能...');
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

  // 1. 验证 index.html 中的入口指向 V4
  const indexPath = path.join(__dirname, '../index.html');
  await page.goto(`file://${indexPath}`, { waitUntil: 'networkidle' });
  const daofaHref = await page.$eval('#subject-daofa', el => el.getAttribute('href'));
  console.log('✅ 主页道法入口链接:', daofaHref);
  if (!daofaHref.includes('daofa-V4.html')) {
    throw new Error(`Expected link to daofa-V4.html, but got ${daofaHref}`);
  }

  // 2. 验证 daofa/daofa-V4.html
  const daofaPath = path.join(__dirname, '../daofa/daofa-V4.html');
  await page.goto(`file://${daofaPath}`, { waitUntil: 'networkidle' });

  // 检查标题
  const title = await page.title();
  console.log('✅ 页面标题:', title);
  if (!title.includes('V4')) {
    throw new Error('Title does not include V4!');
  }

  // 检查默认选中的 PDF
  const selectedPdf = await page.$eval('#pdfSelect', el => el.value);
  console.log('✅ 默认首选 PDF:', selectedPdf);
  if (selectedPdf !== '2026.9.30道法综合卷一讲评思路.pdf') {
    throw new Error(`Expected selected PDF to be 2026.9.30道法综合卷一讲评思路.pdf, but got ${selectedPdf}`);
  }

  // 检查 iframe 的 src
  const iframeSrc = await page.$eval('#pdfFrame', el => el.getAttribute('src'));
  console.log('✅ iframe 默认加载源:', iframeSrc);
  if (!iframeSrc.includes('2026.9.30道法综合卷一讲评思路.pdf')) {
    throw new Error('iframe src is not loading 2026.9.30道法综合卷一讲评思路.pdf!');
  }

  // 检查当前预览标题
  const currentTitle = await page.$eval('#currentPdfTitle', el => el.innerText);
  console.log('✅ 当前预览提示文字:', currentTitle);
  if (!currentTitle.includes('2026.9.30道法综合卷一讲评思路.pdf')) {
    throw new Error('currentPdfTitle does not match!');
  }

  // 截取 PDF 视口直接浏览高清图
  const screenshotPath = path.join(resultsDir, 'daofa-v4-pdf-direct-browse-verified.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log('📸 已生成 PDF 网页直接浏览验收截图:', screenshotPath);

  await browser.close();
  console.log('🎉 2026.9.30道法综合卷一讲评思路 PDF 网页直接浏览验收全部通过！');
})();
