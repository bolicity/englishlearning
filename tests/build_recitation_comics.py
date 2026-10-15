#!/usr/bin/env python3
"""由 recitation_comics_data.py 生成 chinese/recitation-comics-V1.html（四格连环画 · 图↔诗对照）。

用法: python3 tests/build_recitation_comics.py
产出: chinese/recitation-comics-V1.html
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'chinese'))
import recitation_comics_data as M  # noqa: E402

IMG_DIR = 'images/recitation-comics'

VOL_COLOR = {
    '六年级（上册）': '#DC2626',
    '六年级（下册）': '#EA580C',
    '七年级（上册）': '#D97706',
    '七年级（下册）': '#059669',
    '八年级（上册）': '#0891B2',
    '八年级（下册）': '#2563EB',
    '九年级（上册）': '#7C3AED',
    '九年级（下册）': '#DB2777',
}
CN_NUM = ['①', '②', '③', '④']


def build_payload():
    pym = json.load(open(ROOT / 'chinese' / 'recitation-pinyin-V1.json', encoding='utf-8'))
    vols = []
    idx = 0
    for v in M.DATA:
        items = []
        for it in v['items']:
            panels = []
            for i, (verse, scene) in enumerate(it['panels'], 1):
                panels.append({
                    'v': verse,
                    's': scene,
                    'img': f'{IMG_DIR}/{it["slug"]}-c{i}.webp',
                    'no': CN_NUM[i - 1],
                })
            items.append({
                'id': idx,
                'slug': it['slug'],
                'title': it['title'],
                'author': it['author'],
                'type': it['type'],
                'panels': panels,
                'py': pym.get(it['slug'], {}),
            })
            idx += 1
        vols.append({
            'vol': v['vol'],
            'color': VOL_COLOR.get(v['vol'], '#DC2626'),
            'items': items,
        })
    return vols


HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>初中必背 86 篇 · 四格连环画记忆 | 语文复习中心</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Serif+SC:wght@400;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --bg-main:#F8FAFC; --bg-card:#FFFFFF; --bg-subtle:#F1F5F9;
    --border:#E2E8F0; --tp:#0F172A; --ts:#475569; --tm:#64748B;
    --red:#DC2626; --red-l:#EF4444; --red-bg:#FEF2F2;
    --shadow:0 1px 3px rgba(15,23,42,.06);
    --shadow-md:0 8px 24px rgba(15,23,42,.10);
    --r-s:8px; --r-m:12px; --r-l:16px;
    --sidebar-w:264px;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{-webkit-text-size-adjust:100%}
  body{font-family:'Inter',system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;
       background:var(--bg-main);color:var(--tp);line-height:1.6}

  /* ---------- header ---------- */
  header{background:var(--bg-card);border-bottom:1px solid var(--border);
         position:sticky;top:0;z-index:60;box-shadow:var(--shadow)}
  .nav{max-width:1500px;margin:0 auto;padding:.7rem 1.1rem;display:flex;
       justify-content:space-between;align-items:center;gap:1rem}
  .brand{display:flex;align-items:center;gap:.7rem;text-decoration:none;color:var(--tp)}
  .brand-logo{width:38px;height:38px;background:linear-gradient(135deg,var(--red),var(--red-l));
       color:#fff;border-radius:var(--r-s);display:flex;align-items:center;justify-content:center;
       font-weight:800;font-size:.95rem;flex:none}
  .brand-title{font-family:'Outfit',sans-serif;font-weight:700;font-size:1.08rem;color:var(--red)}
  .brand-sub{font-size:.72rem;color:var(--tm)}
  .nav-right{display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}
  .btn{display:inline-flex;align-items:center;gap:.35rem;padding:.5rem .85rem;min-height:40px;
       background:var(--bg-subtle);color:var(--ts);border:1px solid var(--border);
       border-radius:var(--r-s);text-decoration:none;font-weight:600;font-size:.82rem;
       cursor:pointer;transition:.18s;white-space:nowrap}
  .btn:hover{background:var(--red-bg);color:var(--red-l);border-color:#FECDD3}

  /* ---------- layout ---------- */
  .shell{max-width:1500px;margin:0 auto;display:flex;gap:1.1rem;padding:1.1rem;align-items:flex-start}

  /* ---------- sidebar ---------- */
  aside{width:var(--sidebar-w);flex:none;background:var(--bg-card);border:1px solid var(--border);
        border-radius:var(--r-l);box-shadow:var(--shadow);position:sticky;top:74px;
        max-height:calc(100vh - 92px);display:flex;flex-direction:column;overflow:hidden;transition:.22s}
  aside.collapsed{width:0;opacity:0;border-width:0;margin-right:-1.1rem}
  .side-head{padding:.85rem 1rem;border-bottom:1px solid var(--border);display:flex;
        justify-content:space-between;align-items:center;flex:none}
  .side-head h2{font-family:'Outfit',sans-serif;font-size:.92rem;font-weight:800;color:var(--tp)}
  .side-head span{font-size:.7rem;color:var(--tm)}
  .side-body{overflow-y:auto;padding:.5rem .55rem 1rem}
  .vol{margin-bottom:.3rem}
  .vol-btn{width:100%;display:flex;align-items:center;gap:.45rem;padding:.5rem .6rem;
        background:none;border:none;border-radius:var(--r-s);cursor:pointer;text-align:left;
        font-family:inherit;font-size:.83rem;font-weight:700;color:var(--ts);transition:.15s}
  .vol-btn:hover{background:var(--bg-subtle)}
  .vol-btn .dot{width:8px;height:8px;border-radius:2px;flex:none}
  .vol-btn .cnt{margin-left:auto;font-size:.68rem;color:var(--tm);font-weight:600}
  .vol-btn .arw{font-size:.6rem;color:var(--tm);transition:.2s}
  .vol.open .arw{transform:rotate(90deg)}
  .vol-list{display:none;padding:.1rem 0 .25rem .55rem}
  .vol.open .vol-list{display:block}
  .poem-btn{width:100%;display:flex;align-items:baseline;gap:.35rem;padding:.36rem .55rem;
        background:none;border:none;border-left:2px solid var(--border);border-radius:0 var(--r-s) var(--r-s) 0;
        cursor:pointer;text-align:left;font-family:inherit;font-size:.8rem;color:var(--ts);transition:.15s}
  .poem-btn:hover{background:var(--bg-subtle);color:var(--tp)}
  .poem-btn.active{background:var(--red-bg);border-left-color:var(--red);color:var(--red);font-weight:700}
  .poem-btn .pno{font-size:.66rem;color:var(--tm);font-variant-numeric:tabular-nums;flex:none;min-width:1.4em}
  .poem-btn.active .pno{color:var(--red-l)}

  /* ---------- main ---------- */
  main{flex:1;min-width:0;display:flex;flex-direction:column;gap:1rem}
  .panel-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-l);
        box-shadow:var(--shadow);padding:1.4rem 1.5rem}
  .poem-head{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;flex-wrap:wrap}
  .poem-title{font-family:'Outfit','Noto Serif SC',serif;font-size:1.75rem;font-weight:800;color:var(--tp);line-height:1.25}
  .poem-meta{display:flex;align-items:center;gap:.5rem;margin-top:.4rem;flex-wrap:wrap}
  .chip{font-size:.72rem;font-weight:700;padding:.18rem .55rem;border-radius:999px;
        background:var(--bg-subtle);color:var(--tm)}
  .chip.vol{color:#fff}
  .chip.type{background:#EFF6FF;color:#1D4ED8}
  .toolbar{display:flex;gap:.45rem;flex-wrap:wrap;align-items:center}
  .btn.on{background:var(--red-bg);color:var(--red);border-color:#FECDD3}
  .counter{font-size:.75rem;color:var(--tm);font-variant-numeric:tabular-nums}

  /* ---------- panels ---------- */
  .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem;margin-top:1rem}
  .pn{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-m);
      overflow:hidden;display:flex;flex-direction:column;transition:.2s;cursor:zoom-in;position:relative}
  .pn:hover{box-shadow:var(--shadow-md);transform:translateY(-2px);border-color:#FECDD3}
  .pn-img{position:relative;background:#FBF9F4;aspect-ratio:1/1;overflow:hidden}
  .pn-img img{width:100%;height:100%;object-fit:cover;display:block}
  .pn-no{position:absolute;top:.55rem;left:.55rem;width:28px;height:28px;border-radius:50%;
      background:rgba(255,255,255,.92);border:1px solid var(--border);display:flex;align-items:center;
      justify-content:center;font-size:.85rem;color:var(--red);font-weight:700;z-index:2;
      box-shadow:0 1px 4px rgba(0,0,0,.08)}
  .pn-txt{padding:.75rem .85rem .85rem;display:flex;flex-direction:column;gap:.4rem;
      border-top:1px solid var(--border);background:#FFFDFB}
  .verse{font-family:'Noto Serif SC',serif;font-size:.95rem;font-weight:700;color:var(--red);
      line-height:2.05;letter-spacing:.01em}
  .scene{font-size:.72rem;color:var(--tm);line-height:1.6}

  /* ---------- 难字注音 ---------- */
  ruby{ruby-position:over}
  rt{font-family:'Inter','PingFang SC',sans-serif;font-size:.5em;font-weight:500;
     color:var(--tm);letter-spacing:0;line-height:1.1;text-indent:0}
  .verse ruby,.lb-txt .verse ruby{ruby-align:center}
  body.no-py rt{display:none}
  body.no-py .verse{line-height:1.6}
  .pn.hide-verse .verse{filter:blur(6px);opacity:.55;user-select:none;transition:.25s}
  .pn.hide-verse .scene{opacity:.45}
  .pn.hide-verse .pn-img img{filter:brightness(.97)}
  .pn.revealed .verse{filter:none;opacity:1}
  .reveal-tip{position:absolute;bottom:.55rem;left:50%;transform:translateX(-50%);
      background:rgba(15,23,42,.72);color:#fff;font-size:.68rem;padding:.2rem .6rem;border-radius:999px;
      pointer-events:none;opacity:0;transition:.2s}
  .pn.hide-verse:not(.revealed) .reveal-tip{opacity:1}
  .no-scene .scene{display:none}

  /* ---------- lightbox ---------- */
  .lb{position:fixed;inset:0;background:rgba(15,23,42,.92);z-index:200;display:none;
      align-items:center;justify-content:center;padding:1.5rem;cursor:zoom-out}
  .lb.show{display:flex}
  .lb-inner{max-width:min(96vw,1000px);width:100%;background:var(--bg-card);border-radius:var(--r-l);
      overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.4)}
  .lb-inner img{width:100%;display:block;background:#FBF9F4}
  .lb-txt{padding:.9rem 1.1rem 1.1rem}
  .lb-txt .verse{font-size:1.15rem}
  .lb-txt .scene{margin-top:.3rem}
  .lb-close{position:absolute;top:1rem;right:1.1rem;width:42px;height:42px;border-radius:50%;
      background:rgba(255,255,255,.16);color:#fff;border:none;font-size:1.3rem;cursor:pointer}
  .lb-nav{position:absolute;top:50%;transform:translateY(-50%);width:46px;height:46px;border-radius:50%;
      background:rgba(255,255,255,.16);color:#fff;border:none;font-size:1.3rem;cursor:pointer}
  .lb-nav.prev{left:1rem}.lb-nav.next{right:1rem}

  footer{max-width:1500px;margin:0 auto;padding:1.6rem 1.1rem 3rem;text-align:center;
      color:var(--tm);font-size:.78rem}

  /* ---------- mobile ---------- */
  .side-toggle{display:none}
  @media(max-width:1080px){
    .shell{padding:.8rem}
    aside{position:fixed;left:0;top:0;bottom:0;z-index:100;border-radius:0;max-height:100vh;width:280px;
          box-shadow:0 0 40px rgba(0,0,0,.2)}
    aside.collapsed{transform:translateX(-100%);width:280px;opacity:1;border-width:1px;margin:0}
    .side-toggle{display:inline-flex}
    .mask{position:fixed;inset:0;background:rgba(15,23,42,.45);z-index:90;display:none}
    .mask.show{display:block}
  }
  @media(max-width:1080px){
    .grid{grid-template-columns:repeat(2,1fr)}
  }
  @media(max-width:760px){
    .grid{grid-template-columns:repeat(2,1fr);gap:.6rem}
    .verse{font-size:.82rem}
    .scene{font-size:.66rem}
    .pn-txt{padding:.5rem .6rem .6rem}
    .poem-title{font-size:1.35rem}
    .panel-card{padding:1.05rem}
    .brand-sub{display:none}
    .nav{padding:.6rem .8rem}
  }
</style>
</head>
<body>
<header>
  <div class="nav">
    <a href="chinese.html" class="brand">
      <div class="brand-logo">画</div>
      <div>
        <div class="brand-title">必背 86 篇 · 四格连环画</div>
        <div class="brand-sub">看图成诵 · 图与诗逐格对照</div>
      </div>
    </a>
    <div class="nav-right">
      <button class="btn side-toggle" id="sideToggle">☰ 篇目</button>
      <a class="btn" href="recitation-drill-V1.html">✍️ 默写自测</a>
      <a class="btn" href="chinese.html">← 返回</a>
    </div>
  </div>
</header>

<div class="mask" id="mask"></div>
<div class="shell">
  <aside id="sidebar">
    <div class="side-head">
      <h2>篇目导航</h2>
      <span id="sideCount">86 篇</span>
    </div>
    <div class="side-body" id="sideBody"></div>
  </aside>

  <main>
    <section class="panel-card">
      <div class="poem-head">
        <div>
          <div class="poem-title" id="pTitle">—</div>
          <div class="poem-meta" id="pMeta"></div>
        </div>
        <div class="toolbar">
          <button class="btn" id="btnPrev">← 上一篇</button>
          <button class="btn" id="btnNext">下一篇 →</button>
          <button class="btn" id="btnBlur">👁 看图背诗</button>
          <button class="btn on" id="btnPy">🔤 拼音</button>
          <button class="btn" id="btnScene">📝 图注</button>
          <span class="counter" id="pCounter"></span>
        </div>
      </div>
      <div class="grid" id="grid"></div>
    </section>
  </main>
</div>

<div class="lb" id="lb">
  <button class="lb-close" id="lbClose">×</button>
  <button class="lb-nav prev" id="lbPrev">‹</button>
  <button class="lb-nav next" id="lbNext">›</button>
  <div class="lb-inner">
    <img id="lbImg" alt="">
    <div class="lb-txt">
      <div class="verse" id="lbVerse"></div>
      <div class="scene" id="lbScene"></div>
    </div>
  </div>
</div>

<footer>
  © 2026 初中语文复习中心 · 86 篇 × 4 格 = 344 幅连环画 · 插画为 AI 生成（工笔线描水墨风），仅供个人学习背诵使用
</footer>

<script>
const DATA = __DATA__;
const flat = [];
DATA.forEach(v => v.items.forEach(it => flat.push({...it, vol: v.vol, color: v.color})));
const TOTAL = flat.length;

const $ = id => document.getElementById(id);
let cur = 0, curPanel = 0, blurMode = false, showScene = true;

/* ---------- 难字注音 ---------- */
const PYM = {};
flat.forEach(p => { PYM[p.id] = p.py || {c:{}, w:{}}; });

function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function annotate(text, m) {
  if (!m) return esc(text);
  const marks = new Array(text.length).fill(null);
  const words = m.w || {}, chars = m.c || {};
  Object.keys(words).forEach(w => {
    const syl = String(words[w]).split(' ');
    let from = 0, i;
    while ((i = text.indexOf(w, from)) !== -1) {
      for (let k = 0; k < w.length; k++) marks[i + k] = syl[k] || '';
      from = i + w.length;
    }
  });
  Object.keys(chars).forEach(zi => {
    for (let i = 0; i < text.length; i++) if (text[i] === zi && !marks[i]) marks[i] = chars[zi];
  });
  let out = '';
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    out += marks[i] ? `<ruby>${esc(ch)}<rt>${esc(marks[i])}</rt></ruby>` : esc(ch);
  }
  return out;
}

/* ---------- sidebar ---------- */
let html = '';
DATA.forEach((v, vi) => {
  html += `<div class="vol${vi === 0 ? ' open' : ''}" data-vol="${vi}">
    <button class="vol-btn">
      <span class="dot" style="background:${v.color}"></span>${v.vol}
      <span class="cnt">${v.items.length}</span><span class="arw">▶</span>
    </button>
    <div class="vol-list">`;
  v.items.forEach(it => {
    html += `<button class="poem-btn" data-id="${it.id}">
      <span class="pno">${String(it.id + 1).padStart(2, '0')}</span><span>${it.title}</span>
    </button>`;
  });
  html += `</div></div>`;
});
$('sideBody').innerHTML = html;
$('sideCount').textContent = TOTAL + ' 篇';

$('sideBody').addEventListener('click', e => {
  const vb = e.target.closest('.vol-btn');
  if (vb) { vb.parentElement.classList.toggle('open'); return; }
  const pb = e.target.closest('.poem-btn');
  if (pb) { go(+pb.dataset.id); closeSide(); }
});

/* ---------- render ---------- */
function go(i) {
  cur = (i + TOTAL) % TOTAL;
  const p = flat[cur];
  $('pTitle').textContent = p.title;
  $('pMeta').innerHTML =
    `<span class="chip vol" style="background:${p.color}">${p.vol}</span>` +
    `<span class="chip">${p.author}</span>` +
    `<span class="chip type">${p.type}</span>` +
    `<span class="chip">四格连环画</span>`;
  $('pCounter').textContent = `${cur + 1} / ${TOTAL}`;

  $('grid').innerHTML = p.panels.map((pn, k) => `
    <article class="pn${blurMode ? ' hide-verse' : ''}${showScene ? '' : ' no-scene'}" data-k="${k}">
      <div class="pn-img">
        <span class="pn-no">${pn.no}</span>
        <img src="${pn.img}" alt="${p.title} 第${k + 1}格" loading="${k < 2 ? 'eager' : 'lazy'}">
        <span class="reveal-tip">点击看图猜诗句</span>
      </div>
      <div class="pn-txt">
        <div class="verse">${annotate(pn.v, PYM[p.id])}</div>
        <div class="scene">${pn.s}</div>
      </div>
    </article>`).join('');

  document.querySelectorAll('.poem-btn').forEach(b => b.classList.toggle('active', +b.dataset.id === cur));
  const volBox = document.querySelector(`.vol[data-vol="${DATA.findIndex(v => v.vol === p.vol)}"]`);
  if (volBox) volBox.classList.add('open');
  const act = document.querySelector('.poem-btn.active');
  if (act) act.scrollIntoView({block: 'nearest'});
  window.scrollTo({top: 0, behavior: 'smooth'});
  history.replaceState(null, '', '#' + p.slug);
}

/* ---------- panel interactions ---------- */
$('grid').addEventListener('click', e => {
  const pn = e.target.closest('.pn');
  if (!pn) return;
  const k = +pn.dataset.k;
  if (blurMode && !pn.classList.contains('revealed')) {
    pn.classList.add('revealed');
  } else {
    openLb(k);
  }
});

/* ---------- lightbox ---------- */
function openLb(k) {
  curPanel = k;
  const p = flat[cur], pn = p.panels[k];
  $('lbImg').src = pn.img;
  $('lbVerse').innerHTML = annotate(pn.v, PYM[p.id]);
  $('lbScene').textContent = `${p.title} · ${p.author}　|　${pn.s}`;
  $('lb').classList.add('show');
}
function closeLb() { $('lb').classList.remove('show'); }
$('lbClose').onclick = closeLb;
$('lb').onclick = e => { if (e.target === $('lb') || e.target.id === 'lbImg') closeLb(); };
$('lbPrev').onclick = e => { e.stopPropagation(); openLb((curPanel + 3) % 4); };
$('lbNext').onclick = e => { e.stopPropagation(); openLb((curPanel + 1) % 4); };
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeLb();
  if ($('lb').classList.contains('show')) {
    if (e.key === 'ArrowLeft') openLb((curPanel + 3) % 4);
    if (e.key === 'ArrowRight') openLb((curPanel + 1) % 4);
    return;
  }
  if (e.key === 'ArrowLeft') go(cur - 1);
  if (e.key === 'ArrowRight') go(cur + 1);
});
document.addEventListener('touchstart', e => { tsx = e.touches[0].clientX; }, {passive: true});
let tsx = 0;
document.addEventListener('touchend', e => {
  if ($('lb').classList.contains('show')) return;
  const dx = e.changedTouches[0].clientX - tsx;
  if (Math.abs(dx) > 90) go(cur + (dx < 0 ? 1 : -1));
}, {passive: true});

/* ---------- toolbar ---------- */
$('btnPrev').onclick = () => go(cur - 1);
$('btnNext').onclick = () => go(cur + 1);
$('btnBlur').onclick = () => {
  blurMode = !blurMode;
  $('btnBlur').classList.toggle('on', blurMode);
  $('btnBlur').textContent = blurMode ? '👁 背诗中' : '👁 看图背诗';
  document.querySelectorAll('.pn').forEach(pn => {
    pn.classList.toggle('hide-verse', blurMode);
    pn.classList.remove('revealed');
  });
};
$('btnPy').onclick = () => {
  const off = document.body.classList.toggle('no-py');
  $('btnPy').classList.toggle('on', !off);
  $('btnPy').textContent = off ? '🔤 拼音（隐藏）' : '🔤 拼音';
};
$('btnScene').onclick = () => {
  showScene = !showScene;
  $('btnScene').classList.toggle('on', !showScene);
  $('btnScene').textContent = showScene ? '📝 图注' : '📝 图注（隐藏）';
  document.querySelectorAll('.pn').forEach(pn => pn.classList.toggle('no-scene', !showScene));
};

/* ---------- sidebar toggle (mobile) ---------- */
function closeSide() { if (innerWidth <= 1080) { $('sidebar').classList.add('collapsed'); $('mask').classList.remove('show'); } }
$('sideToggle').onclick = () => {
  const c = $('sidebar').classList.toggle('collapsed');
  $('mask').classList.toggle('show', !c);
};
$('mask').onclick = closeSide;

/* ---------- init ---------- */
const hash = decodeURIComponent(location.hash.replace('#', ''));
if (innerWidth <= 1080) { $('sidebar').classList.add('collapsed'); }
const startIdx = hash ? flat.findIndex(p => p.slug === hash) : 0;
go(startIdx < 0 ? 0 : startIdx);
</script>
</body>
</html>
'''


def main():
    payload = build_payload()
    n_poems = sum(len(v['items']) for v in payload)
    n_panels = sum(len(it['panels']) for v in payload for it in v['items'])
    out = HTML.replace('__DATA__', json.dumps(payload, ensure_ascii=False, separators=(',', ':')))
    dest = ROOT / 'chinese' / 'recitation-comics-V1.html'
    dest.write_text(out, encoding='utf-8')
    print(f'wrote {dest}  poems={n_poems} panels={n_panels} bytes={len(out.encode())}')


if __name__ == '__main__':
    main()
