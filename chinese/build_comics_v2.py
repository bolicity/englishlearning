import json
import re

# 读取 drill 数据（获取考纲完整原文与易错生僻字）
with open('chinese/recitation-drill-V1.html', 'r', encoding='utf-8') as f:
    text_drill = f.read()

m_drill = re.search(r'const DATA = (\[[\s\S]*?\]);\s*const NOTES', text_drill)
drill_data = json.loads(m_drill.group(1))

drill_map = {}
for vol in drill_data:
    for it in vol['items']:
        clean_title = it['title'].replace('《', '').replace('》', '').strip()
        drill_map[clean_title] = it

# 读取 comics V1
with open('chinese/recitation-comics-V1.html', 'r', encoding='utf-8') as f:
    v1_content = f.read()

m_comics = re.search(r'const DATA = (\[[\s\S]*?\]);\s*\n', v1_content)
comics_data = json.loads(m_comics.group(1))

# 将 86 篇完整原文与生僻字注入到 comics_data 中
for vol in comics_data:
    for it in vol['items']:
        c_title = it['title'].replace('《', '').replace('》', '').strip()
        match = drill_map.get(c_title)
        if not match:
            for k in drill_map:
                if c_title in k or k in c_title:
                    match = drill_map[k]
                    break
        if match:
            it['paras'] = match.get('paras', [])
            it['hard'] = match.get('hard', '')
            it['hardList'] = match.get('hardList', [])
        else:
            print(f"Warning: no match for {c_title}")

comics_json_str = json.dumps(comics_data, ensure_ascii=False)

v2_content = v1_content

# 1. 标题与头部更新
v2_content = v2_content.replace(
    "<title>初中必背 86 篇 · 四格连环画记忆 | 语文复习中心</title>",
    "<title>初中必背 86 篇 · 四格连环画记忆 V2.0（含考纲全篇原文与易错字） | 语文复习中心</title>"
)

v2_content = v2_content.replace(
    '<div class="brand-title">必背 86 篇 · 四格连环画</div>',
    '<div class="brand-title">必背 86 篇 · 四格连环画 <span style="font-size: 11px; background: #DBEAFE; color: #1E40AF; padding: 2px 7px; border-radius: 4px; font-weight: 700; margin-left: 6px;">V2.0 考纲原文版</span></div>'
)

# 2. 工具栏增加“📜 考纲原文”与“📋 复制”按钮
old_toolbar = '''        <div class="toolbar">
          <button class="btn" id="btnPrev">← 上一篇</button>
          <button class="btn" id="btnNext">下一篇 →</button>
          <button class="btn" id="btnBlur">👁 看图背诗</button>
          <button class="btn on" id="btnPy">🔤 拼音</button>
          <button class="btn on" id="btnScene">📝 图注</button>
          <span class="counter" id="pCounter"></span>
        </div>'''

new_toolbar = '''        <div class="toolbar">
          <button class="btn" id="btnPrev">← 上一篇</button>
          <button class="btn" id="btnNext">下一篇 →</button>
          <button class="btn" id="btnBlur">👁 看图背诗</button>
          <button class="btn on" id="btnPy">🔤 拼音</button>
          <button class="btn on" id="btnScene">📝 图注</button>
          <button class="btn on" id="btnFulltext" style="background: #EFF6FF; color: #2563EB; border-color: #BFDBFE;">📜 考纲原文</button>
          <span class="counter" id="pCounter"></span>
        </div>'''

v2_content = v2_content.replace(old_toolbar, new_toolbar)

# 3. 在四格网格下方添加考纲原文卡片容器
old_grid_section = '<div class="grid" id="grid"></div>\n    </section>'
new_grid_section = '''<div class="grid" id="grid"></div>

      <!-- 考纲标准全篇原文与生僻字速记卡片 (浅色商务风格) -->
      <div class="fulltext-section" id="fulltextSection">
        <div class="fulltext-head">
          <div class="fulltext-title">
            <span>📜 27 届上海中考考纲标准原文 & 易错字速记</span>
            <span class="fulltext-badge">考纲必背</span>
          </div>
          <div class="fulltext-actions">
            <button class="btn btn-sm" id="btnCopyFulltext" onclick="copyCurrentFulltext()" title="复制全文">📋 复制原文</button>
            <button class="btn btn-sm" id="btnFoldFulltext" onclick="toggleFulltextFold()">▲ 收起</button>
          </div>
        </div>
        <div class="fulltext-body" id="fulltextBody">
          <div class="fulltext-content" id="fulltextContent"></div>
          <div class="hard-box" id="hardBox">
            <div class="hard-box-head">
              <span>✍️ 上海中考核心生僻字 / 易错字 / 通假字点拨：</span>
            </div>
            <div class="hard-pill-list" id="hardPillList"></div>
            <div class="hard-raw-note" id="hardRawNote"></div>
          </div>
        </div>
      </div>
    </section>'''

v2_content = v2_content.replace(old_grid_section, new_grid_section)

# 4. 插入新的 CSS 样式
custom_css = '''
  /* ---------- 考纲标准全篇原文与生僻字样式 (浅色商务风格) ---------- */
  .btn-sm{padding:.32rem .65rem;min-height:30px;font-size:.76rem}
  .fulltext-section{margin-top:1.25rem;background:#FFFFFF;border:1px solid var(--border);
      border-radius:var(--r-m);box-shadow:var(--shadow);overflow:hidden;transition:.2s}
  .fulltext-section.folded .fulltext-body{display:none}
  .fulltext-head{padding:.8rem 1.1rem;background:#F8FAFC;border-bottom:1px solid var(--border);
      display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
  .fulltext-title{font-size:.96rem;font-weight:700;color:var(--tp);display:flex;align-items:center;gap:8px}
  .fulltext-badge{font-size:11px;font-weight:700;padding:2px 7px;border-radius:4px;
      background:#EFF6FF;color:#2563EB;border:1px solid #BFDBFE}
  .fulltext-actions{display:flex;align-items:center;gap:6px}
  .fulltext-body{padding:1.25rem 1.35rem;background:#FFFFFF}
  .fulltext-content{font-family:'Noto Serif SC',serif;font-size:1.1rem;color:#1E293B;
      line-height:2.05;letter-spacing:.02em;background:#FBF9F4;border:1px solid #EFE8DA;
      border-radius:var(--r-s);padding:1.15rem 1.35rem;margin-bottom:1rem;white-space:pre-wrap}
  .fulltext-content p{margin-bottom:.75rem}
  .fulltext-content p:last-child{margin-bottom:0}
  .hard-box{background:#FFFDF8;border:1px solid #FDE68A;border-radius:var(--r-s);padding:.85rem 1.1rem}
  .hard-box-head{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:#92400E;margin-bottom:8px}
  .hard-pill-list{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:6px}
  .hard-pill{display:inline-flex;align-items:center;gap:5px;background:#FFFFFF;border:1px solid #FCD34D;
      border-radius:6px;padding:3px 9px;font-size:12.5px;box-shadow:0 1px 2px rgba(0,0,0,.03)}
  .hard-pill .hz{color:#B45309;font-weight:700;font-family:'Noto Serif SC',serif;font-size:14px}
  .hard-pill .py{color:#D97706;font-family:'Inter',monospace;font-weight:600}
  .hard-raw-note{font-size:12.5px;color:#78350F;line-height:1.6;padding-top:6px;border-top:1px dashed #FDE68A}
'''

v2_content = v2_content.replace('</style>', custom_css + '\n</style>')

# 5. 替换 DATA 数组
v2_content = re.sub(
    r'const DATA = \[[\s\S]*?\];\s*\n',
    f'const DATA = {comics_json_str};\n',
    v2_content
)

# 6. 更新 JS 中的渲染与交互逻辑
old_render_logic = '''  $('pCounter').textContent = `${cur + 1} / ${TOTAL}`;

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
    </article>`).join('');'''

new_render_logic = '''  $('pCounter').textContent = `${cur + 1} / ${TOTAL}`;

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

  // 渲染考纲标准全篇原文
  const fullContentEl = $('fulltextContent');
  if (p.paras && p.paras.length) {
    fullContentEl.innerHTML = p.paras.map(para => {
      // 对全篇原文中难字进行权威注音高亮标注
      return `<p>${annotate(para, PYM[p.id])}</p>`;
    }).join('');
  } else {
    // 降级使用四格的合集
    fullContentEl.innerHTML = `<p>${p.panels.map(pn => annotate(pn.v, PYM[p.id])).join('　')}</p>`;
  }

  // 渲染生僻/易错字速记药丸
  const pillListEl = $('hardPillList');
  const rawNoteEl = $('hardRawNote');
  const hardBoxEl = $('hardBox');
  if (p.hardList && p.hardList.length) {
    hardBoxEl.style.display = 'block';
    pillListEl.innerHTML = p.hardList.map(h => `
      <span class="hard-pill">
        <span class="hz">${h.zi}</span>
        <span class="py">${h.py}</span>
      </span>
    `).join('');
    rawNoteEl.innerHTML = `<strong>【PDF考纲原注】</strong>${p.hard || '—'}`;
  } else if (p.hard) {
    hardBoxEl.style.display = 'block';
    pillListEl.innerHTML = '';
    rawNoteEl.innerHTML = `<strong>【PDF考纲原注】</strong>${p.hard}`;
  } else {
    hardBoxEl.style.display = 'none';
  }'''

v2_content = v2_content.replace(old_render_logic, new_render_logic)

# 7. 添加考纲原文展开折叠与复制函数
helper_functions = '''
/* ---------- 考纲原文展开/折叠与复制 ---------- */
let fulltextFolded = false;
let fulltextVisible = true;

function toggleFulltextFold() {
  const sec = $('fulltextSection');
  const btn = $('btnFoldFulltext');
  fulltextFolded = !fulltextFolded;
  sec.classList.toggle('folded', fulltextFolded);
  btn.textContent = fulltextFolded ? '▼ 展开' : '▲ 收起';
}

function toggleFullText() {
  const sec = $('fulltextSection');
  const btn = $('btnFulltext');
  fulltextVisible = !fulltextVisible;
  sec.style.display = fulltextVisible ? 'block' : 'none';
  btn.classList.toggle('on', fulltextVisible);
  btn.textContent = fulltextVisible ? '📜 考纲原文' : '📜 考纲原文（隐藏）';
  if (fulltextVisible) {
    sec.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}
if ($('btnFulltext')) {
  $('btnFulltext').onclick = toggleFullText;
}

function copyCurrentFulltext() {
  const p = flat[cur];
  const text = (p.paras && p.paras.length) ? p.paras.join('\\n') : p.panels.map(pn => pn.v).join('\\n');
  const fullTextToCopy = `${p.title} —— ${p.author}\\n\\n${text}\\n\\n${p.hard ? '【生僻/易错字：' + p.hard + '】' : ''}`;
  navigator.clipboard.writeText(fullTextToCopy).then(() => {
    const btn = $('btnCopyFulltext');
    const old = btn.textContent;
    btn.textContent = '✅ 已复制全文！';
    setTimeout(() => { btn.textContent = old; }, 1800);
  }).catch(() => {
    alert('复制成功：\\n' + fullTextToCopy);
  });
}
'''

v2_content = v2_content.replace('/* ---------- init ---------- */', helper_functions + '\n/* ---------- init ---------- */')

with open('chinese/recitation-comics-V2.html', 'w', encoding='utf-8') as f:
    f.write(v2_content)

print("Successfully created chinese/recitation-comics-V2.html")
