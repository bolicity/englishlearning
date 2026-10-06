#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 /tmp/classic-mu-redraw 的 21 张重画图切格/落盘，覆盖 classic-comics 原文件。"""
import json
from pathlib import Path
from PIL import Image

SRC = Path('/tmp/classic-mu-redraw')
OUT = Path('/Users/emily/Developer/Projects/owenlearining/chinese/images/classic-comics')
QUADS = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}


def patch_watermark(img):
    w, h = img.size
    x0, x1 = w - 210, w - 8
    src = img.crop((x0, h - 112, x1, h - 66))
    img.paste(src, (x0, h - 52))
    return img


def main():
    m = json.load(open('/tmp/redraw_manifest.json', encoding='utf-8'))
    files = sorted(SRC.glob('重画*.png'))
    by_token = {}
    for f in files:
        tok = f.name.split('_')[0]
        assert tok not in by_token, f'撞名: {tok}'
        by_token[tok] = f
    total = 0
    missing = []
    for idx, g in enumerate(m['groups'], 1):
        tok = g['token']
        f = by_token.get(tok)
        if not f:
            missing.append(tok)
            continue
        img = Image.open(f).convert('RGB')
        W, H = img.size
        hw, hh = W // 2, H // 2
        for i, img_name in enumerate(g['quads']):
            x, y = QUADS[i]
            panel = img.crop((x * hw, y * hh, (x + 1) * hw, (y + 1) * hh))
            if i == 3:
                panel = patch_watermark(panel)
            panel.save(OUT / f"{img_name}.jpg", quality=84)
            total += 1
    for s in m['singles']:
        f = by_token.get(s['token'])
        if not f:
            missing.append(s['token'])
            continue
        panel = Image.open(f).convert('RGB')
        panel = patch_watermark(panel)
        panel.save(OUT / f"{s['img']}.jpg", quality=84)
        total += 1
    print(f'落盘 {total} 张；缺 {missing}')


if __name__ == '__main__':
    main()
