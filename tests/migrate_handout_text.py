#!/usr/bin/env python3
"""把旧版(HEAD) BOOKS_DB.pages_data 的原版讲义逐行文字移植到新版 classic-reading-V4。

- 按 data-book-title 对齐 16 部名著；
- 插在每部名著 scan-gallery-box（影印区）之前，默认折叠，点开即读；
- 空/页眉行过滤，逐行 <p> 渲染。
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DST = ROOT / 'chinese' / 'classic-reading-V4.html'
HEAD_DB = json.loads(re.search(
    r'const BOOKS_DB = (\[.*?\]);\n',
    (ROOT / '.workbuddy' / 'head_classic_v4.json').read_text(encoding='utf-8'), re.S).group(1)) \
    if (ROOT / '.workbuddy' / 'head_classic_v4.json').exists() else None

def load_head_db():
    import subprocess
    raw = subprocess.run(['git', 'show', 'HEAD:chinese/classic-reading-V4.html'],
                         capture_output=True, text=True, cwd=ROOT).stdout
    return json.loads(re.search(r'const BOOKS_DB = (\[.*?\]);\n', raw, re.S).group(1))

CSS = """
  /* ===== 原版讲义纯文字区 ===== */
  .handout-text-box { padding: 18px 28px 6px; background: #F8FAFC; border-top: 1px dashed var(--border-color); }
  .handout-text-title { font-size: 14px; font-weight: 700; color: var(--text-muted); margin-bottom: 10px; }
  .handout-page { background: #fff; border: 1px solid var(--border-color); border-radius: 8px; margin-bottom: 8px; overflow: hidden; }
  .handout-page summary { cursor: pointer; padding: 10px 16px; font-size: 13px; font-weight: 700; color: var(--primary); background: #F1F5F9; list-style: none; display: flex; align-items: center; gap: 6px; }
  .handout-page summary::before { content: '▸'; transition: transform .15s; font-size: 11px; }
  .handout-page[open] summary::before { transform: rotate(90deg); }
  .handout-lines { padding: 14px 18px; font-size: 13.5px; line-height: 1.9; color: var(--text-main); }
  .handout-lines p { margin: 0 0 2px; }
  .handout-lines p.h-line { font-weight: 700; color: var(--primary); margin-top: 10px; }
  .handout-lines p.blank { height: .5em; }
"""

def esc(s):
    return html.escape(s.strip())

def render_pages(pd):
    parts = []
    for p in pd:
        num = p.get('page_num')
        lines = [l for l in (p.get('lines') or [])]
        # 过滤纯符号/超短噪声行，保留空行标记
        ps = []
        for l in lines:
            t = l.strip()
            if not t:
                ps.append('<p class="blank"></p>')
            elif re.fullmatch(r'[—\-_·•\. ]+', t):
                continue
            elif t.startswith(('一、','二、','三、','四、','五、','六、','七、','八、','九、','十、','十')) and '、《' in t:
                ps.append(f'<p class="h-line">{esc(t)}</p>')
            else:
                ps.append(f'<p>{esc(t)}</p>')
        parts.append(
            f'      <details class="handout-page">\n'
            f'        <summary>原版讲义 第 {num} 页 · 逐行全文</summary>\n'
            f'        <div class="handout-lines">\n' + '\n'.join(ps) + '\n        </div>\n      </details>')
    return '\n'.join(parts)

def main():
    db = load_head_db()
    by_title = {b['title']: b.get('pages_data') or [] for b in db}

    src = DST.read_text(encoding='utf-8')
    assert 'handout-text-box' not in src, '已移植过，请勿重复执行'

    # 按 article 切块处理
    parts = re.split(r'(?=<article class="book-section")', src)
    done = 0
    for i, blk in enumerate(parts):
        m = re.search(r'data-book-title="([^"]+)"', blk)
        if not m:
            continue
        title = m.group(1)
        pd = by_title.get(title)
        if not pd:
            print(f'!! {title} 无讲义数据'); continue
        anchor = '<footer class="scan-gallery-box">'
        assert anchor in blk, f'{title} 缺影印区锚点'
        box = (f'<div class="handout-text-box">\n'
               f'        <div class="handout-text-title">📝 原版讲义 · 纯文字完整还原（点击页码展开）：</div>\n'
               f'{render_pages(pd)}\n      </div>\n\n      ')
        blk = blk.replace(anchor, box + anchor, 1)
        parts[i] = blk
        done += 1

    src = ''.join(parts)
    src = src.replace('</style>', CSS + '</style>', 1)
    DST.write_text(src, encoding='utf-8')
    print(f'OK 已移植 {done} 部名著的讲义文字 -> {DST.name} ({len(src)/1024:.0f} KB)')

if __name__ == '__main__':
    sys.exit(main())
