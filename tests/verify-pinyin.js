/* 难字注音全量验证：Python 侧生成期望 → 页面实际 ruby 逐格比对 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const expect = JSON.parse(fs.readFileSync(path.join(__dirname, '_py_expect.json'), 'utf8'));

(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto('file://' + path.join(__dirname, '..', 'chinese', 'recitation-comics-V1.html'), { waitUntil: 'load' });
  await page.waitForTimeout(500);

  const got = await page.evaluate(async () => {
    const out = [];
    for (let i = 0; i < TOTAL; i++) {
      go(i);
      const po = { title: flat[i].title, panels: [] };
      document.querySelectorAll('.pn').forEach(pn => {
        const verse = pn.querySelector('.verse');
        const rubys = [...verse.querySelectorAll('ruby')];
        po.panels.push({
          ruby: rubys.length,
          pairs: rubys.map(r => {
            const base = [...r.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('');
            const rt = r.querySelector('rt');
            return [base, rt ? rt.textContent : null];
          })
        });
      });
      out.push(po);
    }
    return out;
  });

  const problems = [];
  let rubyTotal = 0, pairTotal = 0;
  expect.forEach((exp, i) => {
    const act = got[i];
    if (act.title !== exp.title) problems.push(`篇序错位 #${i}: ${act.title} != ${exp.title}`);
    exp.panels.forEach((ep, k) => {
      const ap = act.panels[k];
      if (!ap) { problems.push(`${exp.title} 第${k + 1}格缺失`); return; }
      rubyTotal += ap.ruby;
      pairTotal += ap.pairs.length;
      if (ap.ruby !== ep.n) problems.push(`${exp.title} 第${k + 1}格 注音数 ${ap.ruby} != 期望 ${ep.n}`);
      if (ep.pairs.length !== ap.pairs.length) { problems.push(`${exp.title} 第${k + 1}格 注音字不符`); return; }
      ep.pairs.forEach(([zi, py], m) => {
        const [az, apy] = ap.pairs[m] || [];
        if (az !== zi || apy !== py)
          problems.push(`${exp.title} 第${k + 1}格 第${m + 1}个注音 ${az}=${apy} != 期望 ${zi}=${py}`);
      });
      ap.pairs.forEach(([zi, py]) => {
        if (!zi || zi.length !== 1) problems.push(`${exp.title} 第${k + 1}格 ruby 基底异常: ${zi}`);
        if (!py || !/^[a-zA-Zü\u00c0-\u024f]+$/.test(py)) problems.push(`${exp.title} 第${k + 1}格 拼音异常: ${zi}=${py}`);
      });
    });
  });

  console.log(JSON.stringify({
    poems: expect.length,
    rubyTotal,
    uniquePairs: new Set(expect.flatMap(p => p.panels.flatMap(x => x.pairs.map(q => q.join('='))))).size,
    problemCount: problems.length,
    problems: problems.slice(0, 25),
    pageErrors: errors.slice(0, 5)
  }, null, 1));

  // 关闭拼音开关再验一次（应仍渲染 DOM，仅隐藏）
  const hidden = await page.evaluate(() => {
    document.getElementById('btnPy').click();
    const rt = document.querySelector('.pn rt');
    return { cls: document.body.classList.contains('no-py'), rtDisplay: rt ? getComputedStyle(rt).display : 'none' };
  });
  console.log('拼音开关:', JSON.stringify(hidden));

  await browser.close();
})();
