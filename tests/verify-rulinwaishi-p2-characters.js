// 验证 rulinwaishi-p2-V1.html：11 位人物故事插图全部真实加载 + lightbox 可用
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const fileUrl = 'file://' + path.resolve(__dirname, '../chinese/rulinwaishi-p2-V1.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  const thumbs = await page.$$('img.char-thumb');
  console.log(`char-thumb 数量: ${thumbs.length} (期望 11)`);
  if (thumbs.length !== 11) throw new Error(`FAIL: 期望 11 张缩略图，实际 ${thumbs.length}`);

  let broken = 0;
  for (const img of thumbs) {
    const ok = await img.evaluate(el => el.complete && el.naturalWidth > 100 && el.naturalHeight > 100);
    const src = await img.evaluate(el => el.getAttribute('src'));
    if (!ok) { broken++; console.log(`  BROKEN: ${src}`); }
  }
  console.log(`加载失败: ${broken} 张`);
  if (broken > 0) throw new Error(`FAIL: ${broken} 张插图未正常加载`);

  // 点击第一张缩略图，验证 lightbox 打开
  await thumbs[0].click();
  await page.waitForTimeout(300);
  const lightboxActive = await page.$eval('#lightboxModal', el => el.classList.contains('active'));
  const lightboxSrc = await page.$eval('#lightboxImg', el => el.getAttribute('src'));
  console.log(`lightbox 打开: ${lightboxActive}, 加载图: ${lightboxSrc}`);
  if (!lightboxActive || !lightboxSrc.includes('rulinwaishi-p2-maer')) throw new Error('FAIL: lightbox 行为异常');
  await page.screenshot({ path: path.resolve(__dirname, '../test-results/rulinwaishi-p2-characters.png'), fullPage: false });

  await page.keyboard.press('Escape');
  await browser.close();
  console.log('PASS: 11 张人物故事插图全部加载，lightbox 放大正常');
})();
