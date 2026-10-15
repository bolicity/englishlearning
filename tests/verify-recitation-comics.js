// 验证 recitation-comics-V1.html：86 篇 / 344 格 / 图↔诗逐格对照 / 全部图片可加载
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const file = 'file://' + path.resolve(__dirname, '../chinese/recitation-comics-V1.html');
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto(file, { waitUntil: 'load', timeout: 60000 });

  const side = await page.evaluate(() => ({
    vols: document.querySelectorAll('#sideBody .vol').length,
    poems: document.querySelectorAll('#sideBody .poem-btn').length,
    sideCount: document.getElementById('sideCount').textContent,
  }));

  // 逐篇切换，采集每格 img src / 诗句 / 图注
  const collected = await page.evaluate(async () => {
    const out = [];
    const grid = document.getElementById('grid');
    const goFn = window.__go;
    const total = document.querySelectorAll('#sideBody .poem-btn').length;
    for (let i = 0; i < total; i++) {
      document.querySelectorAll('#sideBody .poem-btn')[i].click();
      await new Promise(r => requestAnimationFrame(r));
      const title = document.getElementById('pTitle').textContent.trim();
      const panels = [...grid.querySelectorAll('.pn')].map(pn => ({
        img: pn.querySelector('img').getAttribute('src'),
        verse: pn.querySelector('.verse').textContent.trim(),
        scene: pn.querySelector('.scene').textContent.trim(),
        no: pn.querySelector('.pn-no').textContent.trim(),
      }));
      out.push({ i, title, panels });
    }
    return out;
  });

  // 校验：每篇 4 格、诗句非空、src 与序号一致
  const problems = [];
  collected.forEach(p => {
    if (p.panels.length !== 4) problems.push(`${p.title}: panels=${p.panels.length}`);
    p.panels.forEach((pn, k) => {
      if (!pn.verse) problems.push(`${p.title} 第${k + 1}格: 诗句为空`);
      if (!pn.scene) problems.push(`${p.title} 第${k + 1}格: 图注为空`);
      const m = pn.img.match(/recitation-comics\/(.+)\.webp$/);
      if (!m) problems.push(`${p.title} 第${k + 1}格: src 异常 ${pn.img}`);
      else if (!m[1].endsWith(`-c${k + 1}`)) problems.push(`${p.title} 第${k + 1}格: 序号错位 ${m[1]}`);
    });
  });

  // 去重篇名 & 图片总数
  const titles = collected.map(p => p.title);
  const uniqTitles = new Set(titles);
  const allImgs = [...new Set(collected.flatMap(p => p.panels.map(pn => pn.img)))];

  // 真实加载校验：全部设 eager 后轮询
  await page.evaluate(() => {
    document.querySelectorAll('.pn img').forEach(i => { i.loading = 'eager'; });
  });
  const loadCheck = await page.evaluate(async (srcs) => {
    const load = src => new Promise(res => {
      const im = new Image();
      im.onload = () => res(im.naturalWidth > 0);
      im.onerror = () => res(false);
      im.src = src;
    });
    const bad = [];
    const CHUNK = 40;
    for (let i = 0; i < srcs.length; i += CHUNK) {
      const rs = await Promise.all(srcs.slice(i, i + CHUNK).map(load));
      rs.forEach((ok, j) => { if (!ok) bad.push(srcs[i + j]); });
    }
    return bad;
  }, allImgs);

  // 功能校验：看图背诗 / 图注开关 / 灯箱
  await page.click('#btnBlur');
  const blurOn = await page.evaluate(() => document.querySelectorAll('.pn.hide-verse').length);
  await page.click('.pn');
  const revealed = await page.evaluate(() => document.querySelectorAll('.pn.revealed').length);
  await page.click('#btnBlur');
  await page.click('#btnScene');
  const sceneHidden = await page.evaluate(() => document.querySelectorAll('.pn.no-scene').length);
  await page.click('#btnScene');
  await page.click('.pn');
  const lbOpen = await page.evaluate(() => document.getElementById('lb').classList.contains('show'));
  const lbVerse = await page.evaluate(() => document.getElementById('lbVerse').textContent.trim());
  await page.keyboard.press('Escape');

  // 截图：首屏 + 中部一篇
  fs.mkdirSync(path.resolve(__dirname, '../test-results'), { recursive: true });
  await page.goto(file, { waitUntil: 'load' });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.resolve(__dirname, '../test-results/rc-desktop-top.png') });
  await page.evaluate(() => document.querySelectorAll('#sideBody .poem-btn')[40].click());
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.resolve(__dirname, '../test-results/rc-desktop-mid.png') });

  // 看图背诗模式截图
  await page.click('#btnBlur');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, '../test-results/rc-blur-mode.png') });
  await page.click('#btnBlur');

  // 移动端
  const mp = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mp.goto(file, { waitUntil: 'load' });
  await mp.waitForTimeout(1500);
  await mp.screenshot({ path: path.resolve(__dirname, '../test-results/rc-mobile.png') });

  console.log(JSON.stringify({
    sidebar: side,
    poemsCollected: collected.length,
    uniqTitles: uniqTitles.size,
    uniqueImages: allImgs.length,
    problems: problems.slice(0, 10),
    problemCount: problems.length,
    brokenImages: loadCheck.slice(0, 10),
    brokenCount: loadCheck.length,
    blurOn, revealed, sceneHidden, lbOpen, lbVerse,
    pageErrors: errors.slice(0, 5),
  }, null, 2));

  await browser.close();
})();
