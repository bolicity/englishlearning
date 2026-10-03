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

  console.log('--- 开始验收《儒林外史》核心考点专题页 ---');

  // 1. 验证 rulinwaishi-V1.html
  const rulinwaishiUrl = 'file://' + path.resolve(__dirname, '../chinese/rulinwaishi-V1.html');
  console.log('正在访问:', rulinwaishiUrl);
  await page.goto(rulinwaishiUrl, { waitUntil: 'networkidle' });

  // 检查标题与核心区块
  const title = await page.title();
  console.log('页面标题:', title);
  if (!title.includes('儒林外史')) {
    throw new Error('页面标题未包含《儒林外史》！');
  }

  // 检查 10 张考点原图加载状态
  const images = await page.$$('.gallery-img');
  console.log(`检测到画廊图片数量: ${images.length}`);
  if (images.length !== 10) {
    throw new Error(`预期 10 张考点图片，实际检测到 ${images.length} 张！`);
  }

  let loadedCount = 0;
  for (let i = 0; i < images.length; i++) {
    const isLoaded = await images[i].evaluate((img) => img.complete && img.naturalWidth > 0);
    const src = await images[i].getAttribute('src');
    if (!isLoaded) {
      throw new Error(`图片加载失败: [${i}] ${src}`);
    }
    loadedCount++;
  }
  console.log(`✓ 10/10 张考点高清原图全部成功加载完成 (naturalWidth > 0)`);

  // 检查点击放大 Modal 弹窗
  console.log('测试点击第 1 张图片放大功能...');
  await images[0].click();
  await page.waitForTimeout(300);

  const modalDisplay = await page.$eval('#imageModal', (el) => window.getComputedStyle(el).display);
  const modalImgSrc = await page.$eval('#modalImg', (el) => el.src);
  console.log(`Modal display 状态: ${modalDisplay}, 弹窗图片路径存在: ${!!modalImgSrc}`);
  if (modalDisplay === 'none' || !modalImgSrc) {
    throw new Error('点击图片未能正确激活高清弹窗预览！');
  }

  // 关闭 Modal
  await page.click('.close-btn');
  await page.waitForTimeout(200);
  const modalClosedDisplay = await page.$eval('#imageModal', (el) => window.getComputedStyle(el).display);
  console.log(`Modal 关闭后 display 状态: ${modalClosedDisplay}`);
  if (modalClosedDisplay !== 'none') {
    throw new Error('点击关闭按钮后 Modal 未正确隐藏！');
  }

  // 截取 rulinwaishi 页面
  const rulinwaishiScreenshot = path.join(resultsDir, 'rulinwaishi-v1-verified.png');
  await page.screenshot({ path: rulinwaishiScreenshot, fullPage: false });
  console.log(`✓ 专题页截图已保存至: ${rulinwaishiScreenshot}`);

  // 2. 验证 chinese.html 导航连通性
  const chineseUrl = 'file://' + path.resolve(__dirname, '../chinese/chinese.html');
  console.log('正在验证语文导航主页:', chineseUrl);
  await page.goto(chineseUrl, { waitUntil: 'networkidle' });

  const rulinLink = await page.$('a[href*="rulinwaishi-V1.html"]');
  if (!rulinLink) {
    throw new Error('chinese.html 未找到前往 rulinwaishi-V1.html 的跳转卡片！');
  }
  console.log('✓ chinese.html 中已存在《儒林外史》核心考点入口卡片');

  // 3. 验证 index.html 主入口
  const indexUrl = 'file://' + path.resolve(__dirname, '../index.html');
  console.log('正在验证网站主入口:', indexUrl);
  await page.goto(indexUrl, { waitUntil: 'networkidle' });
  const chineseCardText = await page.$eval('#subject-chinese', (el) => el.innerText);
  console.log(`主页语文卡片文本:\n${chineseCardText}`);
  if (!chineseCardText.includes('儒林外史考点')) {
    throw new Error('index.html 中语文卡片未显示《儒林外史考点》！');
  }
  console.log('✓ index.html 语文卡片副标提示正常');

  console.log('=== 所有自动化测试与连通性验证全部通过！ ===');
  await browser.close();
})();
