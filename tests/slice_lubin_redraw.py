#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 /tmp/lubin-mu 的 9 张鲁滨逊重画图切格/落盘，覆盖 classic-comics 原文件。"""
import json
from pathlib import Path
from PIL import Image

SRC = Path('/tmp/lubin-mu')
OUT = Path('/Users/emily/Developer/Projects/owenlearining/chinese/images/classic-comics')
QUADS = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}


def patch_watermark(img):
    w, h = img.size
    x0, x1 = w - 210, w - 8
    src = img.crop((x0, h - 112, x1, h - 66))
    img.paste(src, (x0, h - 52))
    return img


def main():
    m = json.load(open('/tmp/lubin_redraw_manifest.json', encoding='utf-8'))
    by_token = {}
    for f in SRC.glob('鲁重画*.png'):
        by_token[f.name.split('_')[0]] = f
    total, missing = 0, []
    for g in m['groups']:
        f = by_token.get(g['token'])
        if not f:
            missing.append(g['token']); continue
        img = Image.open(f).convert('RGB')
        W, H = img.size
        hw, hh = W // 2, H // 2
        for i, name in enumerate(g['quads']):
            x, y = QUADS[i]
            panel = img.crop((x * hw, y * hh, (x + 1) * hw, (y + 1) * hh))
            if i == 3:
                panel = patch_watermark(panel)
            panel.save(OUT / f"{name}.jpg", quality=84)
            total += 1
    for s in m['singles']:
        f = by_token.get(s['token'])
        if not f:
            missing.append(s['token']); continue
        panel = patch_watermark(Image.open(f).convert('RGB'))
        panel.save(OUT / f"{s['img']}.jpg", quality=84)
        total += 1
    print(f'落盘 {total} 张；缺 {missing}')


if __name__ == '__main__':
    main()
