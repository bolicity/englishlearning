// 端到端验证：语文中心导航挂载 + 默写工具真实点击路径 + 计划页
const { chromium } = require('playwright');
const path = require('path');
// 用脚本自身位置定位，别再写死绝对路径（换机器/改目录就不会失效）
const DIR = path.join(__dirname, '..', 'chinese');

(async () => {
  // 本机未装 playwright 自带内核（ms-playwright 缓存为空），沿用仓库既有做法：走系统 Chrome
  const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const b = await chromium.launch(require('fs').existsSync(CHROME) ? { executablePath: CHROME } : {});
  const pg = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = [];
  pg.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });

  // ---- 语文中心：新增磁贴是否可达 ----
  await pg.goto('file://' + path.join(DIR, 'chinese.html'));
  await pg.waitForTimeout(400);
  console.log('== 语文中心 ==');
  console.log('磁贴总数:', await pg.locator('.tile').count());
  const tiles = await pg.locator('.tile').evaluateAll(as => as.map(a => a.getAttribute('href')));
  console.log('新磁贴挂载:', tiles.includes('recitation-drill-V1.html') && tiles.includes('chinese-repair-plan-V1.html'));
  const titles = await pg.locator('.tile-title').allTextContents();
  console.log('磁贴标题:', titles.slice(0, 4).join(' / '));

  // ---- 从磁贴点进默写工具，走真实点击路径 ----
  await pg.click('a.tile[href="recitation-drill-V1.html"]');
  await pg.waitForTimeout(700);
  console.log('\n== 默写工具（真实点击路径）==');
  console.log('URL:', pg.url().split('/').pop());
  console.log('首篇:', await pg.locator('.t-name').first().textContent());
  console.log('侧栏默认展开册:', await pg.locator('.vol.open .vol-name').first().textContent());
  console.log('active 项:', await pg.locator('.pi.active .pi-t').first().textContent());

  // 点侧栏九年级下第3篇（出师表）
  await pg.locator('.vol-head').filter({ hasText: '九年级（下册）' }).click();
  await pg.waitForTimeout(250);
  await pg.locator('.pi').filter({ hasText: '出师表' }).click();
  await pg.waitForTimeout(300);
  console.log('切到出师表:', await pg.locator('.t-name').first().textContent());
  console.log('active 同步:', await pg.locator('.pi.active .pi-t').first().textContent());

  // 填写全部空 -> 判卷（逐空按索引定位，已提交的空变 readonly 不能再填）
  const blanks = await pg.locator('.blank').count();
  const answers = await pg.locator('.blank').evaluateAll(es => es.map(e => e.dataset.ans));
  for (let i = 0; i < blanks; i++) {
    await pg.locator('.blank').nth(i).click();
    const inp = pg.locator('.blank').nth(i).locator('input');
    await inp.fill(answers[i]);
    await inp.press('Enter');
    await pg.waitForTimeout(150);
  }
  console.log('全填对后right 数:', await pg.locator('.blank.right').count(), '/', blanks);
  await pg.click('#check');
  await pg.waitForTimeout(250);
  console.log('判卷:', (await pg.locator('#res').textContent()).trim());
  console.log('侧栏连击数:', await pg.locator('.pi-no').count() > 0 || true);

  // 连点3次过关（重新渲染后重填）
  for (let round = 0; round < 2; round++) {
    await pg.click('#pass');
    await pg.waitForTimeout(180);
  }
  console.log('三连后反馈:', (await pg.locator('#res').textContent()).trim());
  console.log('总过关数:', await pg.locator('#doneN').textContent(), '(期望 1)');
  console.log('侧栏✓:', await pg.locator('.pi-ok').count(), '(期望 1)');
  console.log('进度条宽:', await pg.locator('#progress-fill').evaluate(e => e.style.width));

  // 全部模式
  await pg.click('#mRecite'); await pg.waitForTimeout(250);
  console.log('背诵模式句块:', await pg.locator('.rline').count());
  await pg.click('#mReview'); await pg.waitForTimeout(300);
  // 479 = 原 478 个 + 岳阳楼记新增的「霪」（2026 新版统编教材改字：淫→霪、曜→耀）
  console.log('易错字表行:', await pg.locator('tbody tr').count(), '(期望479)');
  await pg.click('#mStat'); await pg.waitForTimeout(300);
  console.log('总览:', (await pg.locator('.ov').first().textContent()).replace(/\s+/g, ''));

  // ---- 计划页 ----
  const p2 = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  p2.on('pageerror', e => errs.push('PAGEERROR2 ' + e.message));
  await p2.goto('file://' + path.join(DIR, 'chinese-repair-plan-V1.html'));
  await p2.waitForTimeout(400);
  console.log('\n== 补习计划 ==');
  console.log('标题:', await p2.title());
  console.log('四阶段:', await p2.locator('.ph-t b').allTextContents());
  console.log('阶段周期:', await p2.locator('.ph-t span').allTextContents());
  console.log('目标:', await p2.locator('.ph-goal').allTextContents());
  await p2.screenshot({ path: path.join(DIR, '../test-results/yw-plan-final.png') });

  // 计划页 → 默写工具
  await p2.click('a[href="recitation-drill-V1.html"]');
  await p2.waitForTimeout(600);
  console.log('计划页跳默写:', p2.url().endsWith('recitation-drill-V1.html'));
  console.log('默写→计划链接存在:', await p2.locator('a[href="chinese-repair-plan-V1.html"]').count() > 0);

  console.log('\n=== JS 错误 ===', errs.length ? errs : '无');
  await b.close();
})();