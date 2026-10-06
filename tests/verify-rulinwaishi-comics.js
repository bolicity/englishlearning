// 验证四个儒林外史页面：连环画图片全部加载、lightbox 可用（先滚动触发 lazy 加载）
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const base = path.resolve(__dirname, '../chinese');
  const pages = ['rulinwaishi-p1-V1.html','rulinwaishi-p2-V1.html','rulinwaishi-p3-V1.html','rulinwaishi-p4-V1.html'];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  let fail = 0;
  for (const f of pages) {
    await page.goto('file://' + path.join(base, f), { waitUntil: 'load', timeout: 30000 });
    // 逐屏滚动触发 loading=lazy
    await page.evaluate(async () => {
      const h = document.body.scrollHeight;
      for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(400);
    const stats = await page.evaluate(async () => {
      const strips = document.querySelectorAll('.comic-strip').length;
      const avatars = document.querySelectorAll('.matrix-avatar, .hero-mini-img').length;
      const imgs = [...document.querySelectorAll('.comic-strip img, .matrix-avatar, .hero-mini-img')];
      await Promise.all(imgs.map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
      const broken = imgs.filter(i => !(i.naturalWidth > 50)).map(i => i.getAttribute('src'));
      return { strips, avatars, total: imgs.length, broken };
    });
    let lb = 'n/a';
    const first = await page.$('.comic-strip img, .matrix-avatar, .hero-mini-img');
    if (first) {
      await first.click();
      await page.waitForTimeout(250);
      lb = await page.evaluate(() => {
        const m = document.getElementById('lightboxModal');
        const i = document.getElementById('lightboxImg');
        const ok = m && m.classList.contains('active') && i && i.src.includes('images/');
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
        return ok ? 'ok' : 'fail';
      });
    }
    const bad = stats.broken.length || lb === 'fail';
    if (bad) fail++;
    console.log(`${f}: strips=${stats.strips} 奇人图/头像=${stats.avatars} 共${stats.total}张 broken=${stats.broken.length} lightbox=${lb} ${bad ? '❌' : '✅'}`);
    if (stats.broken.length) console.log('   缺图:', stats.broken.join(', '));
    await page.screenshot({ path: path.resolve(__dirname, `../test-results/rulin-${f.replace(/rulinwaishi-|-V1\.html/g,'')}-comics.png`), fullPage: false });
  }
  await browser.close();
  console.log(fail ? `\n${fail} 页有问题` : '\n全部通过');
  process.exit(fail ? 1 : 0);
})();
