// 验证：理解性默写自测页的答案解析（chinese/recitation-drill-V1.html）
// 覆盖：解析渲染 / 判错自动展开 / 显示解析切换 / 全文对照 / 背诵模式逐句解析 / 易错字表改字 / 命题说明
//       以及「86 篇每一空的答案都是可作答的句子」这条本轮修复的核心断言
//
// 跑法（必须 HTTP 起服，仓库根目录）：
//   python3 -m http.server 8899 --bind 127.0.0.1 &
//   NODE_PATH=./node_modules node tests/verify-recitation-notes-V1.js
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = process.env.BASE || 'http://127.0.0.1:8899';
const URL = BASE + '/chinese/recitation-drill-V1.html';

// 本机未装 playwright 自带内核（ms-playwright 缓存为空），沿用仓库里既有的做法：走系统 Chrome
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const launchOpts = fs.existsSync(CHROME) ? { executablePath: CHROME } : {};

const ok = (c, msg) => console.log((c ? '  ✓ ' : '  ✗ ') + msg);
let fails = 0;
const check = (c, msg) => { if (!c) fails++; ok(c, msg); };

(async () => {
  const b = await chromium.launch(launchOpts);
  const pg = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = [], bad = [];
  pg.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  pg.on('console', m => {
    if (m.type() !== 'error') return;
    const u = (m.location() && m.location().url) || '';
    if (/\/favicon\.ico$/.test(u)) return;          // 同上，全站性既有 404
    errs.push('CONSOLE ' + m.text() + ' @' + u);
  });
  // 4xx/5xx 既不会触发 pageerror 也不会触发 requestfailed，必须单独听响应状态。
  // /favicon.ico 是浏览器自动发起、全站皆无的既有 404，与页面无关，排除。
  pg.on('response', r => {
    if (r.status() >= 400 && !/\/favicon\.ico$/.test(r.url())) bad.push(r.status() + ' ' + r.url());
  });

  await pg.goto(URL, { waitUntil: 'load' });
  await pg.waitForTimeout(400);

  console.log('== 首屏（宿建德江）==');
  check((await pg.title()).indexOf('理解性默写') >= 0, '标题：' + await pg.title());
  check(await pg.locator('.t-name').first().textContent() === '宿建德江', '首篇为宿建德江');

  const firstAns = await pg.locator('.blank').first().getAttribute('data-ans');
  check(firstAns === '野旷天低树，江清月近人。', '首空答案正确：' + firstAns);

  const nAna = await pg.locator('.qblock .ana').count();
  const hidden = await pg.locator('.qblock .ana[hidden]').count();
  check(nAna === 1 && hidden === 1, `解析块 ${nAna} 个，初始全部隐藏（hidden=${hidden}）`);

  console.log('\n== 写错 → 自动展开解析 ==');
  await pg.locator('.blank').first().click();
  await pg.locator('.blank').first().locator('input').fill('野旷天低树，江清月远人。');   // 故意写错「近」
  await pg.locator('.blank').first().locator('input').press('Enter');
  await pg.waitForTimeout(250);
  check(await pg.locator('.blank.wrong').count() === 1, '该空标记为 wrong');
  check(await pg.locator('.qblock .ana[hidden]').count() === 0, '写错后该句解析已展开');
  const anaTxt = await pg.locator('.qblock .ana').first().innerText();
  ['为什么是这句', '句意', '易错字', '考点'].forEach(k =>
    check(anaTxt.includes(k), '解析含「' + k + '」段'));
  check(anaTxt.includes('以景结情'), '解析内容为真（命中该篇考点「以景结情」）');

  console.log('\n== 显示解析 / 收起解析 ==');
  check(await pg.locator('#toggleAna').textContent() === '收起解析', '判错自动展开后按钮同步为「收起解析」');
  await pg.click('#toggleAna'); await pg.waitForTimeout(200);
  check(await pg.locator('.qblock .ana[hidden]').count() === 1, '点击后全部收起');
  check(await pg.locator('#toggleAna').textContent() === '显示解析', '按钮变「显示解析」');
  await pg.click('#toggleAna'); await pg.waitForTimeout(200);
  check(await pg.locator('.qblock .ana[hidden]').count() === 0, '再点后重新展开');
  check(await pg.locator('#toggleAna').textContent() === '收起解析', '按钮恢复「收起解析」');

  console.log('\n== 全文对照带解析 ==');
  await pg.click('#showAll'); await pg.waitForTimeout(300);
  check(await pg.locator('#ansCard').isVisible(), '全文对照卡片显示');
  check((await pg.locator('#ansCard .ana').count()) === 1, '对照卡内附 1 条解析');

  console.log('\n== 背诵模式逐句解析 ==');
  await pg.click('#mRecite'); await pg.waitForTimeout(300);
  check((await pg.locator('#reciteAna').isHidden()), '解析卡初始隐藏');
  await pg.click('#showReciteAna'); await pg.waitForTimeout(300);
  check(await pg.locator('#reciteAna').isVisible(), '点击后显示');
  check((await pg.locator('#reciteAna .ana').count()) === 1, '含 1 条逐句解析');

  console.log('\n== 易错字表：2026 教材改字已同步 ==');
  await pg.click('#mReview'); await pg.waitForTimeout(400);
  const zi = await pg.locator('tbody tr td:first-child').allTextContents();
  check(zi.includes('霪'), '易错字表含「霪」');
  check(zi.includes('耀'), '易错字表含「耀」');
  check(!zi.includes('曜'), '易错字表已无「曜」');
  check(zi.includes('淫'), '「淫」仍保留（诫子书「淫慢」、富贵不能淫）');
  const warnTxt = await pg.locator('.warn').first().innerText();
  check(warnTxt.includes('霪') && warnTxt.includes('耀'), '改字提示条已渲染');

  console.log('\n== 命题说明（原数据附注已移出正文）==');
  await pg.click('#mStat'); await pg.waitForTimeout(400);
  const statTxt = await pg.locator('#view').innerText();
  check(statTxt.includes('命题说明') && statTxt.includes('所学即所考'), '命题说明卡片已渲染');
  check(statTxt.includes('26'), '文言文篇数卡片在');

  console.log('\n== 全篇扫描：86 篇每一空的答案都必须真能作答 ==');
  await pg.click('#mHide'); await pg.waitForTimeout(300);
  // 侧栏是手风琴式：先确保目标册展开，再点篇目（否则 .pi 不可见）
  const ensureOpen = async (head) => {
    if (!(await head.evaluate(h => h.parentElement.classList.contains('open')))) {
      await head.click();
      await pg.waitForTimeout(80);
    }
  };
  const openVolByName = async (name) => {
    const head = pg.locator('.vol-head').filter({ hasText: name });
    await ensureOpen(head);
    return head;
  };
  const vols = await pg.locator('.vol').count();
  let totalBlanks = 0, punctuOnly = [], missingNote = 0, noBlank = [];
  const EMPTY = /^[\s，。！？；：、""''《》（）·…—”’'’""()\[\]【】]*$/;
  const volHeads = pg.locator('.vol-head');
  for (let v = 0; v < vols; v++) {
    await ensureOpen(volHeads.nth(v));
    const items = await pg.locator(`.vol[data-v="${v}"] .pi`).count();
    for (let i = 0; i < items; i++) {
      await pg.locator(`.vol[data-v="${v}"] .pi`).nth(i).click();
      await pg.waitForTimeout(70);
      const ans = await pg.locator('.blank').evaluateAll(es => es.map(e => e.dataset.ans));
      const notes = await pg.locator('.blank').evaluateAll(es => es.map(e => e.dataset.note));
      if (!ans.length) noBlank.push(await pg.locator('.t-name').first().textContent());
      totalBlanks += ans.length;
      ans.forEach((a, n) => { if (EMPTY.test(a)) punctuOnly.push(notes[n] + ' → ' + JSON.stringify(a)); });
      notes.forEach(n => { if (!n) missingNote++; });
    }
  }
  check(totalBlanks === 91, `总空位数 ${totalBlanks}（期望 91）`);
  check(punctuOnly.length === 0, '无「答案只剩标点」的坏空位' + (punctuOnly.length ? '：' + punctuOnly.join(' / ') : ''));
  check(noBlank.length === 0, '无整篇挖不出空的篇目' + (noBlank.length ? '：' + noBlank.join('、') : ''));
  check(missingNote === 0, '每个空都带 data-note 便于取解析');

  console.log('\n== 三处修复篇目复核 ==');
  await openVolByName('九年级（下册）');
  await pg.locator('.pi').filter({ hasText: '浣溪沙（身向云山那畔行）' }).click();
  await pg.waitForTimeout(250);
  const schAns = await pg.locator('.blank').evaluateAll(es => es.map(e => e.dataset.ans));
  check(schAns.length === 1 && schAns[0] === '古今幽恨几时平！', '浣溪沙只剩 1 空且答案正确：' + schAns.join('|'));
  check((await pg.locator('#view').innerText()).includes('42 字'), '浣溪沙字数已修为 42 字');

  await openVolByName('九年级（上册）');
  await pg.locator('.pi').filter({ hasText: '岳阳楼记' }).click();
  await pg.waitForTimeout(250);
  const ylAns = await pg.locator('.blank').evaluateAll(es => es.map(e => e.dataset.ans));
  check(ylAns.length === 1 && ylAns[0] === '时六年九月十五日。', '岳阳楼记答案正确：' + ylAns.join('|'));
  await pg.click('#showAll'); await pg.waitForTimeout(300);
  const ylAna = await pg.locator('#ansCard .ana').first().innerText();
  check(ylAna.includes('霪') && ylAna.includes('耀'), '岳阳楼记解析已注明新教材改字');

  await openVolByName('九年级（下册）');
  await pg.locator('.pi').filter({ hasText: '曹刿论战' }).click();
  await pg.waitForTimeout(250);
  const cgAns = await pg.locator('.blank').first().getAttribute('data-ans');
  check(cgAns === '吾视其辙乱，望其旗靡，故逐之。”', '曹刿论战答案已补全：' + cgAns);

  await pg.screenshot({ path: '/Users/emily/Documents/Projects/owenlearining/test-results/recitation-notes-review.png', fullPage: true });

  console.log('\n=== pageerror / console.error ===', errs.length ? errs : '无');
  console.log('=== 4xx/5xx ===', bad.length ? bad : '无');
  if (errs.length || bad.length) fails++;
  console.log(fails === 0 ? '\n全部通过 ✓' : `\n${fails} 项未通过 ✗`);
  await b.close();
  process.exit(fails === 0 ? 0 : 1);
})();
