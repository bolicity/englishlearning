#!/usr/bin/env python3
"""收割 /tmp/rc/pool 里的连环画原图：按【slug-cN】前缀改名，裁掉底部水印，转 webp 入库。

用法: python3 tests/harvest_rc_images.py
"""
import pathlib
import re
import sys

from PIL import Image

POOL = pathlib.Path('/tmp/rc/pool')
DEST = pathlib.Path(__file__).resolve().parent.parent / 'chinese' / 'images' / 'recitation-comics'
CROP_BOTTOM = 0.085          # 去掉右下角 AI 生成水印
MAX_SIDE = 760               # webp 输出最长边

PAT = re.compile(r'_([a-z0-9_]+?)_c(\d)_')


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    done = skipped = 0
    for src in sorted(POOL.glob('*.png')):
        m = PAT.match(src.name)
        if not m:
            skipped += 1
            continue
        slug, idx = m.group(1).replace('_', '-'), m.group(2)
        out = DEST / f'{slug}-c{idx}.webp'
        if out.exists():
            src.unlink()
            done += 1
            continue
        im = Image.open(src).convert('RGB')
        w, h = im.size
        im = im.crop((0, 0, w, int(h * (1 - CROP_BOTTOM))))
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        im.save(out, 'WEBP', quality=82, method=6)
        src.unlink()
        done += 1
    total = len(list(DEST.glob('*.webp')))
    print(f'harvested={done} skipped={skipped} total_in_dest={total}')


if __name__ == '__main__':
    sys.exit(main())
