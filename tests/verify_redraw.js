const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto('file:///Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-V4.html', { waitUntil: 'load', timeout: 60000 });

  // eager 加载全部图片
  await page.evaluate(() => {
    document.querySelectorAll('img[loading="lazy"]').forEach(img => { img.loading = 'eager'; });
    window.scrollTo(0, document.body.scrollHeight);
  });
  const ok = await page.waitForFunction(() => {
    const imgs = [...document.querySelectorAll('.comic-panels img')];
    return imgs.every(i => i.complete && i.naturalWidth > 0);
  }, { timeout: 90000 }).then(() => true).catch(() => false);

  const stats = await page.evaluate(() => {
    const imgs = [...document.querySelectorAll('.comic-panels img')];
    const broken = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
    const emptyCap = [...document.querySelectorAll('.comic-panels figcaption')].filter(f => !f.textContent.trim()).length;
    const strips = document.querySelectorAll('.comic-strip').length;
    return { total: imgs.length, broken, emptyCap, strips };
  });
  console.log(JSON.stringify({ loadAll: ok, ...stats, jsErrors: errors }, null, 1));

  // 重点区域截图
  for (const [id, name] of [['book-gangtieshi', 'gangtie'], ['book-tongnian', 'tongnian'], ['book-aiqingshixuan', 'aiqing']]) {
    const el = await page.$('#' + id);
    if (el) { await el.scrollIntoViewIfNeeded(); }
    await page.waitForTimeout(300);
  }
  const shot = await page.$('#book-gangtieshi');
  if (shot) await shot.screenshot({ path: '/tmp/redraw_gangtie.png' });
  const shot2 = await page.$('#book-tongnian');
  if (shot2) await shot2.screenshot({ path: '/tmp/redraw_tongnian.png' });
  await browser.close();
})();
