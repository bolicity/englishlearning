// 验证首页语文格改动：主链接 + 快捷入口，网格未被破坏
const { chromium } = require('playwright');
const path = require('path');
const ROOT = '/Users/emily/Developer/Projects/owenlearining';

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });

  await p.goto('file://' + path.join(ROOT, 'index.html'));
  await p.waitForTimeout(500);

  // 1. HTML 合法性：不得有嵌套 <a>
  const nested = await p.evaluate(() => {
    const bad = [];
    document.querySelectorAll('a').forEach(a => {
      if (a.querySelector('a')) bad.push(a.getAttribute('href') + ' 内含 ' + a.querySelector('a').getAttribute('href'));
    });
    return bad;
  });
  console.log('嵌套<a> 违规:', nested.length ? nested : '无');

  // 2. 语文格结构
  const c = p.locator('#subject-chinese');
  console.log('语文格是 <a>?', (await c.evaluate(e => e.tagName)) === 'A' ? '是(不该)' : '否(已改div)');
  console.log('主链接:', await c.locator('a.card-main').getAttribute('href'));
  const quick = await c.locator('.card-quick a').evaluateAll(as => as.map(a => [a.textContent.trim(), a.getAttribute('href')]));
  console.log('快捷入口:', JSON.stringify(quick));

  // 3. 网格完整性
  const n = await p.locator('#section-subjects > .grid > *').count();
  console.log('核心学科卡片数:', n, n === 10 ? '✓' : '✗ 期望10');

  // 4. 副标题不被截断
  const sub = await c.locator('.card-subtag').evaluate(e => ({
    text: e.textContent, clipped: e.scrollWidth > e.clientWidth + 1
  }));
  console.log('副标题:', sub.text, '截断:', sub.clipped ? '是 ✗' : '否 ✓');

  // 5. 三格等高
  const hs = await p.evaluate(() => [...document.querySelectorAll('#section-subjects > .grid > *')]
    .slice(0, 4).map(e => Math.round(e.getBoundingClientRect().height)));
  console.log('前4格高度:', hs.join('/'), new Set(hs).size === 1 ? '✓ 对齐' : '✗ 不齐');

  // 6. 三条链路真实可点
  await c.locator('a.card-main').click();
  await p.waitForTimeout(600);
  console.log('点主链接 →', p.url().split('/').pop());
  await p.goto('file://' + path.join(ROOT, 'index.html'));
  await p.waitForTimeout(400);
  await c.locator('.card-quick a').first().click();
  await p.waitForTimeout(600);
  console.log('点计划 →', p.url().split('/').pop());
  await p.goto('file://' + path.join(ROOT, 'index.html'));
  await p.waitForTimeout(400);
  await c.locator('.card-quick a').nth(1).click();
  await p.waitForTimeout(600);
  console.log('点默写 →', p.url().split('/').pop());

  // 7. 反向：语文中心磁贴也在
  await p.goto('file://' + path.join(ROOT, 'chinese/chinese.html'));
  await p.waitForTimeout(400);
  const tiles = await p.locator('.tile').evaluateAll(as => as.map(a => a.getAttribute('href')));
  console.log('语文中心磁贴含两页:',
    tiles.includes('recitation-drill-V1.html') && tiles.includes('chinese-repair-plan-V1.html') ? '✓' : '✗');

  console.log('\n=== JS 错误 ===', errs.length ? errs : '无');
  await b.close();
})();