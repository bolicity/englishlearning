#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 66 张扩图母图切成 264 格，写到 chinese/images/classic-comics/。"""
import json
from pathlib import Path
from PIL import Image

MU = Path('/tmp/classic-mu')
OUT = Path('/Users/emily/Developer/Projects/owenlearining/chinese/images/classic-comics')
QUADS = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}


def patch_watermark(img):
    w, h = img.size
    x0, x1 = w - 210, w - 8
    src = img.crop((x0, h - 112, x1, h - 66))
    img.paste(src, (x0, h - 52))
    return img


def main():
    m = json.load(open('/tmp/comics_expand_manifest.json', encoding='utf-8'))
    total = 0
    missing = []
    for g in m['groups']:
        mu = MU / f"{g['mu']}.png"
        if not mu.exists():
            missing.append(mu.name)
            continue
        img = Image.open(mu).convert('RGB')
        W, H = img.size
        hw, hh = W // 2, H // 2
        for i, q in enumerate(g['quads']):
            x, y = QUADS[i]
            panel = img.crop((x * hw, y * hh, (x + 1) * hw, (y + 1) * hh))
            if i == 3:
                panel = patch_watermark(panel)
            panel.save(OUT / f"{q['img']}.jpg", quality=84)
            total += 1
    print(f'切格 {total} 张；缺母图 {missing}')
    print(f'目录现有 {len(list(OUT.glob("*.jpg")))} 个 jpg')


if __name__ == '__main__':
    main()
