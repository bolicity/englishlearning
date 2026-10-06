#!/usr/bin/env python3
"""p4：把 p1-p3 的 19 条连环画条带内联进本页，外跳链接改页内锚点。"""
import re, os

BASE = "/Users/emily/Developer/Projects/owenlearining/chinese"
LINKS = [  # (source_page, slug) 按矩阵出现顺序
    ("p1","wangmian"),("p1","wanghui"),("p1","tangfeng"),
    ("p1","yangongsheng"),("p1","yanjiansheng"),
    ("p2","lubianxiu"),("p2","maer"),("p2","baowenqing"),("p2","hutuhu"),
    ("p2","kuangchaoren"),("p2","niupulang"),("p2","qugongsun"),
    ("p3","dushaoqing"),("p3","yuyude"),("p3","zhuangshaoguang"),
    ("p3","shenqiongzhi"),("p3","guoxiaozi"),("p3","xiaoyunxian"),("p3","fengsilaodie"),
]

def extract_strip(src, slug):
    """按 div 深度配平截取 id="comic-SLUG" 的完整条带块。"""
    m = re.search(r'<div class="comic-strip" id="comic-' + slug + r'">', src)
    assert m, "strip not found: " + slug
    i = m.start()
    depth = 0
    for t in re.finditer(r'<div\b|</div>', src[i:]):
        depth += 1 if t.group(0).startswith('<div') else -1
        if depth == 0:
            return src[i:i + t.end()]
    raise AssertionError("unbalanced strip: " + slug)

p4p = os.path.join(BASE, "rulinwaishi-p4-V1.html")
p4 = open(p4p, encoding="utf-8").read()

# 1) 幂等：已内联过就不再插
if 'id="comic-wangmian"' not in p4:
    strips = []
    for pg, slug in LINKS:
        src = open(os.path.join(BASE, f"rulinwaishi-{pg}-V1.html"), encoding="utf-8").read()
        s = extract_strip(src, slug)
        # 条带图注保留原页图路径（images/ 相对路径四页通用），无需改写
        strips.append(s)
    # 2) 插到最后一条条带（张俊民）之后、card-block 闭合之前
    tail_anchor = '④ 宴席上周旋名流，志得意满</figcaption></figure>\n          </div>\n        </div>'
    assert p4.count(tail_anchor) == 1, p4.count(tail_anchor)
    p4 = p4.replace(tail_anchor, tail_anchor + "\n\n" + "\n\n".join(strips), 1)

# 3) 外跳链接 → 页内锚点
n_ext = len(re.findall(r'href="rulinwaishi-p\d-V1\.html#comic-', p4))
p4 = re.sub(r'href="rulinwaishi-p\d-V1\.html#comic-', 'href="#comic-', p4)

# 4) 区块标题文案
old_t = '11位新增人物 · 故事连环画（其余 19 位点击矩阵中的“连环画→”跳转）'
new_t = '30位重点人物 · 故事连环画（点击矩阵中“连环画→”直达对应条带）'
assert old_t in p4
p4 = p4.replace(old_t, new_t, 1)

open(p4p, "w", encoding="utf-8").write(p4)

# 校验
opens = len(re.findall(r'<div\b', p4)); closes = p4.count('</div>')
inline = len(re.findall(r'id="comic-', p4))
ext = len(re.findall(r'href="rulinwaishi-p\d-V1\.html#comic-', p4))
print(f"p4: 内联条带 {inline} 条 | 外跳链接 {ext} 个 | div配平差 {opens-closes}")
