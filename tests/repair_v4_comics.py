#!/usr/bin/env python3
"""修复 mount_comics_v4.py 造成的 HTML 损坏，并补全被截断的人物名。

损坏模式（每个人物行）：
  ...善意。</div\\n                <tr class="comic-row">   ← 数据行 td/tr 未闭合
  ...</td></tr>></td>\\n              </tr>                ← 挂载行尾部垃圾
修复后：
  数据行正常闭合，comic-row 作为独立兄弟行（colspan 通栏，连环画在文字行下方全宽显示）。
另：人物名按前置 row-key-col 全文重建（修 [:14] 截断丢右括号）。
"""
import re
import pathlib

DST = pathlib.Path('/Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-V4.html')
src = DST.read_text(encoding='utf-8')

# 1) 数据行未闭合： </div\n<tr class="comic-row">  →  补 </td></tr>
n1 = src.count('</div\n                <tr class="comic-row">')
src = src.replace('</div\n                <tr class="comic-row">',
                  '</div></td>\n              </tr>\n              <tr class="comic-row">')

# 2) 挂载行尾部垃圾
n2 = src.count('</td></tr>></td>')
src = src.replace('</td></tr>></td>', '</td></tr>')

# 3) 重建人物名（comic-row 前最近一个 row-key-col）
fixed_titles = 0
def fix_block(m):
    global fixed_titles
    block = m.group(0)
    pre = src[:m.start()]
    km = re.findall(r'<td class="row-key-col">(.*?)</td>', pre, re.S)
    if not km:
        return block
    name = re.sub(r'<[^>]+>', '', km[-1]).strip()
    new = re.sub(r'(<span class="comic-chapter">)[^<]*(</span>)',
                 lambda mm: mm.group(1) + f'{name} · 典型情节画传（点击可放大）' + mm.group(2), block)
    new = re.sub(r'alt="[^"]*连环画第(\d)格"',
                 lambda mm: f'alt="{name}连环画第{mm.group(1)}格"', new)
    if new != block:
        fixed_titles += 1
    return new

src = re.sub(r'<tr class="comic-row">.*?</tr>', fix_block, src, flags=re.S)

# 4) 校验
assert '</div\n' not in src.replace('</div\n\n', ''), '仍有未闭合 div'
bad = src.count('</td></tr>></td>')
div_open = len(re.findall(r'<div\b', src))
div_close = src.count('</div>')

DST.write_text(src, encoding='utf-8')
print(f'未闭合数据行修复 {n1} 处；尾部垃圾修复 {n2} 处；人物名重建 {fixed_titles} 条')
print(f'残留垃圾 {bad}；div 配平 open={div_open} close={div_close}；大小 {len(src)/1024:.0f} KB')
