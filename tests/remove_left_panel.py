#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四个儒林页：删除左侧「官方教研原图」大图预览面板，
改为 content-panel 顶部的一条附件式链接（新标签打开原图）。
split-layout 只剩一栏，加 .single 让它占满整行。
改前备份到 /tmp/rulin_backup/。
"""
import os, re, shutil

BASE = "/Users/emily/Developer/Projects/owenlearining/chinese"
BACKUP = "/tmp/rulin_backup"
PAGES = ["rulinwaishi-p1-V1.html", "rulinwaishi-p2-V1.html",
         "rulinwaishi-p3-V1.html", "rulinwaishi-p4-V1.html"]

CSS = """
    /* 原图附件链接（替代左侧大图预览） */
    .split-layout.single { grid-template-columns: 1fr; }
    .origin-attach { display: flex; align-items: center; gap: 0.5rem; padding: 0.7rem 1rem; background: #F8FAFC; border: 1px dashed var(--border-color); border-radius: 8px; font-size: 0.82rem; color: var(--text-muted); flex-wrap: wrap; }
    .origin-attach a { color: var(--brand-blue, #1D4ED8); font-weight: 700; text-decoration: none; }
    .origin-attach a:hover { text-decoration: underline; }
"""

for f in PAGES:
    path = os.path.join(BASE, f)
    src = open(path, encoding="utf-8").read()
    if 'class="origin-attach"' in src:
        print(f"{f}: 已处理，跳过")
        continue

    start = src.find('<div class="image-preview-panel">')
    assert start != -1, f"{f} 找不到左侧面板"
    end_m = re.search(r"<!-- 右侧文字[^>]*-->", src[start:])
    assert end_m, f"{f} 找不到右侧注释"
    end = start + end_m.start()
    left = src[start:end]
    m = re.search(r"openLightbox\('([^']+)'\)", left)
    assert m, f"{f} 找不到原图路径"
    img = m.group(1)
    t = re.search(r"<h3>([^<]*)</h3>", left)
    title = t.group(1).strip() if t else "官方教研原图"

    # 1) 删除左侧面板（含其前注释与空白）
    cstart = src.rfind("<!-- 左侧原图 -->", 0, start)
    if cstart != -1:
        start = cstart
    src = src[:start] + src[end:]

    # 2) content-panel 顶部插入附件链接
    cp = src.find('<div class="content-panel">')
    assert cp != -1, f"{f} 找不到 content-panel"
    insert_at = cp + len('<div class="content-panel">')
    attach = (f'\n\n        <div class="origin-attach">📎 '
              f'<a href="{img}" target="_blank" rel="noopener">{title} · 点击查看大图</a></div>')
    src = src[:insert_at] + attach + src[insert_at:]

    # 3) split-layout 单栏
    assert src.count('class="split-layout"') == 1, f"{f} split-layout 数量异常"
    src = src.replace('class="split-layout"', 'class="split-layout single"', 1)

    # 3.5) hero 描述里“左侧展示原件”的说法已失效，顺手去掉
    src = re.sub(r"(左侧展示教研原件，|左侧展示原件，)", "", src)

    # 4) CSS
    if ".origin-attach" not in src:
        assert src.count("  </style>") == 1, f"{f} style 收口异常"
        src = src.replace("  </style>", CSS + "  </style>", 1)

    os.makedirs(BACKUP, exist_ok=True)
    shutil.copy2(path, os.path.join(BACKUP, f))
    open(path, "w", encoding="utf-8").write(src)
    print(f"{f}: 左侧面板 → 附件链接（{img}）")
