#!/usr/bin/env python3
"""p4：把连环画并入矩阵——每条条带插入到对应人物行下方（<tr class="comic-row">），
删除原独立连环画板块，工具栏上移到表格上方。"""
import re

P = "/Users/emily/Developer/Projects/owenlearining/chinese/rulinwaishi-p4-V1.html"
src = open(P, encoding="utf-8").read()

# ---------- 1) 抽 30 条 details 条带 ----------
def take(src, start, tag):
    depth = 0
    pat = r'<%s\b|</%s>' % (tag, tag)
    for t in re.finditer(pat, src[start:]):
        depth += 1 if t.group(0).startswith('<' + tag) else -1
        if depth == 0:
            return src[start:start + t.end()]
    raise AssertionError('unbalanced ' + tag)

blocks = {}
for m in re.finditer(r'<details class="comic-strip" id="comic-([\w-]+)">', src):
    blocks[m.group(1)] = take(src, m.start(), 'details')
assert len(blocks) == 30, len(blocks)

# ---------- 2) 工具栏 HTML（先取出） ----------
tm = re.search(r'          <div class="comic-toolbar">.*?</div>\n', src, re.S)
assert tm, 'toolbar not found'
toolbar = tm.group(0)

# ---------- 3) 删掉独立连环画 card-block ----------
title_pos = src.find('30位重点人物 · 故事连环画')
cb_start = src.rfind('<div class="card-block">', 0, title_pos)
assert cb_start != -1, 'comic card-block not found'
cb_block = take(src, cb_start, 'div')
cb_end = cb_start + len(cb_block)
assert 'comic-toolbar' in cb_block and cb_block.count('<details') == 30, 'unexpected comic block'
src = src[:cb_start].rstrip('\n ') + '\n' + src[cb_end:].lstrip('\n')

# ---------- 4) 往矩阵每行后插条带行 ----------
rows = list(re.finditer(r'<tr data-group="(group\d)">.*?</tr>', src, re.S))
assert len(rows) == 30, len(rows)
out = []
last = 0
for r in rows:
    row = r.group(0)
    g = r.group(1)
    ms = re.search(r'href="#comic-([\w-]+)"', row)
    assert ms, 'no slug in row'
    slug = ms.group(1)
    blk = blocks[slug]
    blk = blk.replace('<details class="comic-strip" id="comic-%s">' % slug, '<details class="comic-strip">', 1)
    lines = [ln.strip() for ln in blk.split('\n') if ln.strip()]
    inner = '\n'.join('                      ' + ln for ln in lines)
    comic_row = (
        '\n                <tr class="comic-row" data-group="%s" id="comic-%s">\n'
        '                  <td colspan="3">\n%s\n                  </td>\n                </tr>' % (g, slug, inner)
    )
    out.append(src[last:r.end()])
    out.append(comic_row)
    last = r.end()
out.append(src[last:])
src = ''.join(out)

# ---------- 5) 工具栏放到 filter-tabs 之后 ----------
ft = re.search(r'<div class="filter-tabs">.*?</div>\n', src, re.S)
assert ft, 'filter-tabs not found'
src = src[:ft.end()] + toolbar + src[ft.end():]

# ---------- 6) 标题文案 ----------
old_t = '<span class="icon">30</span> 30位重点人物全解群像大矩阵'
new_t = '<span class="icon">30</span> 30位重点人物全解群像大矩阵（每人行下即其故事连环画）'
assert old_t in src
src = src.replace(old_t, new_t, 1)

# ---------- 7) CSS ----------
css = '''
    /* 连环画并入矩阵行（上下板块合并） */
    tr.comic-row > td { padding: 0.5rem 0.75rem 0.65rem; background: #F8FAFC; }
    tr.comic-row details.comic-strip { background: #FFFFFF; }
    tr.comic-row summary.comic-head { font-size: 0.84rem; }
  </style>'''
assert src.count('  </style>') == 1
src = src.replace('  </style>', css, 1)

# ---------- 8) JS：锚点可能落在 tr 上，需展开其内部 details ----------
old_js = '''      function fromHash() {
        if (!location.hash) return;
        var el = document.querySelector(location.hash);
        if (el && el.tagName === 'DETAILS') el.open = true;
      }'''
new_js = '''      function fromHash() {
        if (!location.hash) return;
        var el = document.querySelector(location.hash);
        if (!el) return;
        if (el.tagName === 'DETAILS') { el.open = true; return; }
        var d = el.querySelector ? el.querySelector('details.comic-strip') : null;
        if (d) d.open = true;
      }'''
assert old_js in src
src = src.replace(old_js, new_js, 1)

open(P, "w", encoding="utf-8").write(src)

o = len(re.findall(r'<div\b', src)) + len(re.findall(r'<details\b', src)) + len(re.findall(r'<tr\b', src))
c = src.count('</div>') + src.count('</details>') + src.count('</tr>')
print('comic-row:', len(re.findall(r'<tr class="comic-row"', src)),
      '| details:', len(re.findall(r'<details class="comic-strip">', src)),
      '| 独立连环画块残留:', src.count('30位重点人物 · 故事连环画'),
      '| 开闭差:', o - c)
