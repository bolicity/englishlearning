#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p4 矩阵：给 11 位本页新增人物也加「连环画→」（指向页内 #comic-锚点），使 30 行统一。幂等。"""
import os, shutil

BASE = "/Users/emily/Developer/Projects/owenlearining/chinese"
BACKUP = "/tmp/rulin_backup"
P4 = [
    "fanjin","zhoujin","luxiaojie","qujingluan","zhangjingzhai","pansan",
    "yangzhizhong","zhaoshi","bucheng","libenying","zhangjunmin",
]
NAMES = {
    "fanjin":"范进","zhoujin":"周进","luxiaojie":"鲁小姐","qujingluan":"瞿景鸾",
    "zhangjingzhai":"张静斋","pansan":"潘三","yangzhizhong":"杨执中","zhaoshi":"赵氏",
    "bucheng":"卜诚","libenying":"李本瑛","zhangjunmin":"张俊民",
}

path = os.path.join(BASE, "rulinwaishi-p4-V1.html")
src = open(path, encoding="utf-8").read()
added = 0
for slug in P4:
    name = NAMES[slug]
    old = f'<span class="role-badge">{name}</span></td>'
    if old in src and f'href="#comic-{slug}"' not in src:
        new = (f'<span class="role-badge">{name}</span>'
               f'<a class="comic-link" href="#comic-{slug}">连环画→</a></td>')
        src = src.replace(old, new, 1)
        added += 1
print(f"p4 页内链接新增 {added} 条")
if added:
    os.makedirs(BACKUP, exist_ok=True)
    shutil.copy2(path, os.path.join(BACKUP, "rulinwaishi-p4-V1.html"))
    open(path, "w", encoding="utf-8").write(src)
