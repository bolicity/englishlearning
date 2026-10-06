// 验证 classic-reading-V4.html：连环画条数、图片加载、渲染无报错
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = 'file://' + path.resolve(__dirname, '../chinese/classic-reading-V4.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto(file, { waitUntil: 'load', timeout: 60000 });

  // 强制 eager 触发全部 comic 图加载（lazy 在程序化滚动下不可靠）
  await page.evaluate(() => {
    document.querySelectorAll('.comic-panels img').forEach(i => {
      i.loading = 'eager';
      const s = i.src; i.src = ''; i.src = s;
    });
  });

  // 轮询等待全部 comic 图加载完成
  await page.waitForFunction(() => {
    const imgs = [...document.querySelectorAll('.comic-panels img')];
    return imgs.length > 0 && imgs.every(i => i.complete && i.naturalWidth > 0);
  }, { timeout: 60000, polling: 500 }).catch(() => {});

  const stats = await page.evaluate(() => {
    const strips = document.querySelectorAll('.comic-strip').length;
    const imgs = [...document.querySelectorAll('.comic-panels img')];
    const broken = imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src'));
    const caps = [...document.querySelectorAll('.comic-panels figcaption')];
    const emptyCaps = caps.filter(c => !c.textContent.trim()).length;
    const books = document.querySelectorAll('.book-block').length;
    return {
      strips, imgTotal: imgs.length, broken: broken.slice(0, 8), brokenCount: broken.length,
      caps: caps.length, emptyCaps, books,
      title: document.querySelector('.hero-headline')?.innerText || ''
    };
  });

  // 截一张带连环画的区域
  const firstStrip = page.locator('.comic-strip').first();
  await firstStrip.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  await firstStrip.screenshot({ path: 'test-results/classic-v4-comic.png' });

  console.log(JSON.stringify(stats, null, 2));
  console.log('页面错误:', errors.length ? errors.slice(0, 5) : '无');
  await browser.close();
})();
