#!/usr/bin/env python3
"""把 /tmp/classic-mu/mu-*.png 的 2×2 四格母图切成 4 张方图，写入 chinese/images/classic-comics/。

- 命名：{base}-c1..4.jpg
- 第 4 格右下角有生图水印，用正上方纸面纹理做补丁覆盖。
"""
import sys
from pathlib import Path
from PIL import Image

MU = Path('/tmp/classic-mu')
OUT = Path(__file__).resolve().parent.parent / 'chinese' / 'images' / 'classic-comics'
QUALITY = 84


def patch_watermark(img):
    w, h = img.size
    band_t, band_b = h - 52, h - 6
    x0, x1 = w - 210, w - 8
    src = img.crop((x0, band_t - 60, x1, band_b - 60))
    img.paste(src, (x0, band_t))
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mus = sorted(MU.glob('mu-*.png'))
    if not mus:
        print('没有找到母图'); return 1
    n = 0
    for mu in mus:
        base = mu.stem[3:]
        img = Image.open(mu).convert('RGB')
        W, H = img.size
        hw, hh = W // 2, H // 2
        for i, (x, y) in enumerate([(0, 0), (hw, 0), (0, hh), (hw, hh)], 1):
            panel = img.crop((x, y, x + hw, y + hh))
            if i == 4:
                panel = patch_watermark(panel)
            panel.save(OUT / f'{base}-c{i}.jpg', quality=QUALITY)
            n += 1
    files = list(OUT.glob('*.jpg'))
    print(f'切格 {n} 张；目录现有 {len(files)} 个文件，{sum(f.stat().st_size for f in files)/1048576:.1f} MB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
