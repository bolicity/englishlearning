#!/usr/bin/env python3
"""p4 连环画区改造：按矩阵顺序重排 + 折叠式条带 + 展开/收起工具栏 + 返回矩阵浮动按钮 + 图注排版微调。"""
import re

P = "/Users/emily/Developer/Projects/owenlearining/chinese/rulinwaishi-p4-V1.html"
src = open(P, encoding="utf-8").read()

# ---------- 1) 取矩阵顺序 (name, slug) ----------
t0 = src.find('id="matrixTable"'); t1 = src.find('</table>', t0)
matrix = src[t0:t1]
order = re.findall(r'class="role-badge">([^<]+)</span><a class="comic-link" href="#comic-([\w-]+)"', matrix)
assert len(order) == 30, len(order)

# ---------- 2) 抽全部条带块（div 深度配平） ----------
def take(src, start):
    depth = 0
    for t in re.finditer(r'<div\b|</div>', src[start:]):
        depth += 1 if t.group(0).startswith('<div') else -1
        if depth == 0:
            return src[start:start + t.end()]
    raise AssertionError("unbalanced")

blocks = {}
for m in re.finditer(r'<div class="comic-strip" id="comic-([\w-]+)">', src):
    blocks[m.group(1)] = take(src, m.start())
assert len(blocks) == 30, len(blocks)

# ---------- 3) 区块边界（含旧条带） ----------
first_slug = re.search(r'<div class="comic-strip" id="comic-([\w-]+)">', src).start()
last_old_end = max(src.find(b) + len(b) for b in blocks.values())
sec_start = src.rfind('<div class="card-block">', 0, first_slug)
sec_end = src.find('</div>', last_old_end) + len('</div>')  # card-block 闭合

# ---------- 4) 生成新条带（折叠 details，统一缩进，按矩阵顺序） ----------
def to_details(block, open_=False):
    b = block
    b = b.replace('<div class="comic-strip" id="comic-', '<details class="comic-strip" id="comic-', 1)
    b = b.replace('>', '>', 1)
    # 首行 </div> 后的 ">" 需补 details 开标签收尾
    b = re.sub(r'^(<details class="comic-strip" id="comic-[\w-]+")>', r'\1>', b, count=1)
    # head → summary
    b = re.sub(r'<div class="comic-head">(.*?)</div>',
               lambda m: '<summary class="comic-head">' + m.group(1) + '</summary>', b, count=1, flags=re.S)
    # 文案
    b = b.replace('故事连环画（点击可放大）', '故事连环画 · 点此展开四格')
    # 尾部 </div> → </details>
    b = re.sub(r'</div>\s*$', '</details>', b)
    if open_:
        b = b.replace('<details class="comic-strip"', '<details open class="comic-strip"', 1)
    # 统一缩进
    lines = [ln.strip() for ln in b.split('\n') if ln.strip()]
    return '\n'.join('          ' + ln for ln in lines)

new_strips = '\n\n'.join(to_details(blocks[slug]) for _, slug in order)

toolbar = '''          <div class="comic-toolbar">
            <button type="button" id="expandAllComics">展开全部 30 条</button>
            <button type="button" id="collapseAllComics">收起全部</button>
            <span class="comic-toolbar-hint">默认收起；点人物名或矩阵里的「连环画→」即可展开该人四格</span>
          </div>

'''

new_sec = '''<div class="card-block">
          <h2 class="block-title"><span class="icon">画</span> 30位重点人物 · 故事连环画（按矩阵分组排序）</h2>

''' + toolbar + new_strips + '\n        </div>'

src = src[:sec_start] + new_sec + src[sec_end:]

# ---------- 5) CSS ----------
css_add = '''
    /* 折叠式连环画 + 排版微调 */
    details.comic-strip { padding: 0.85rem 1rem; border-left: 3px solid var(--brand-red, #B91C1C); }
    details.comic-strip > summary.comic-head { cursor: pointer; margin-bottom: 0; list-style: none; user-select: none; }
    details.comic-strip > summary.comic-head::-webkit-details-marker { display: none; }
    details.comic-strip > summary.comic-head::after {
      content: "▾ 展开"; margin-left: auto; font-size: 0.72rem; font-weight: 700; color: var(--text-muted, #64748B);
    }
    details.comic-strip[open] > summary.comic-head::after { content: "▴ 收起"; }
    details.comic-strip[open] > summary.comic-head { margin-bottom: 0.7rem; }
    .comic-toolbar { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
    .comic-toolbar button {
      font: inherit; font-size: 0.78rem; font-weight: 700; padding: 0.35rem 0.8rem;
      border-radius: var(--radius-sm, 8px); border: 1px solid var(--border-color, #E2E8F0);
      background: #FFFFFF; color: var(--text-secondary, #475569); cursor: pointer; transition: all 0.18s ease;
    }
    .comic-toolbar button:hover { background: #F1F5F9; color: var(--text-primary); }
    .comic-toolbar-hint { font-size: 0.74rem; color: var(--text-muted, #94A3B8); }
    .back-to-matrix {
      position: fixed; right: 1.25rem; bottom: 1.25rem; z-index: 600; display: none;
      padding: 0.55rem 0.95rem; border-radius: 999px; border: none; cursor: pointer;
      background: var(--brand-red, #B91C1C); color: #FFFFFF; font-size: 0.8rem; font-weight: 700;
      box-shadow: 0 6px 18px rgba(15,23,42,0.22);
    }
    .back-to-matrix.show { display: block; }
    .comic-panels { gap: 0.65rem; }
    .comic-panels figcaption { font-size: 0.76rem; line-height: 1.55; }
  </style>'''
assert src.count('  </style>') == 1
src = src.replace('  </style>', css_add, 1)

# ---------- 6) 浮动按钮 HTML ----------
anchor = '  <!-- Lightbox -->'
assert src.count(anchor) == 1
src = src.replace(anchor, '  <button type="button" class="back-to-matrix" id="backToMatrix">↑ 返回矩阵</button>\n\n' + anchor, 1)

# ---------- 7) JS ----------
js_add = '''
    // === 连环画折叠控制 ===
    (function () {
      var all = document.querySelectorAll('details.comic-strip');
      var ex = document.getElementById('expandAllComics');
      var co = document.getElementById('collapseAllComics');
      if (ex) ex.addEventListener('click', function () { all.forEach(function (d) { d.open = true; }); });
      if (co) co.addEventListener('click', function () { all.forEach(function (d) { d.open = false; }); });
      function fromHash() {
        if (!location.hash) return;
        var el = document.querySelector(location.hash);
        if (el && el.tagName === 'DETAILS') el.open = true;
      }
      window.addEventListener('hashchange', fromHash);
      fromHash();
      // 返回矩阵浮动按钮
      var btn = document.getElementById('backToMatrix');
      var matrix = document.getElementById('matrixTable');
      if (btn && matrix) {
        var upd = function () {
          var r = matrix.getBoundingClientRect();
          btn.classList.toggle('show', window.scrollY > 600 && r.bottom < 0);
        };
        btn.addEventListener('click', function () { matrix.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
        window.addEventListener('scroll', upd, { passive: true });
        upd();
      }
    })();
  </script>'''
assert src.count('  </script>') == 1
src = src.replace('  </script>', js_add, 1)

open(P, "w", encoding="utf-8").write(src)

opens = len(re.findall(r'<div\b', src)) + len(re.findall(r'<details\b', src))
closes = src.count('</div>') + src.count('</details>')
print("条带(details):", len(re.findall(r'<details class="comic-strip"', src)),
      "| summary:", len(re.findall(r'<summary class="comic-head">', src)),
      "| 配平差:", opens - closes)
