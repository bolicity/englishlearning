#!/usr/bin/env python3
"""第二批挂载用母图切格：8 位新人物 4 格 + 雅号 7 单格 + 12 张叙事表画廊 r 序列。

母图在 /tmp/classic-mu/mu-*.png（1024x1024，2×2 四格）。
输出到 chinese/images/classic-comics/，文件名与 mount_comics_v4.py 的引用一致。
"""
from pathlib import Path
from PIL import Image

MU = Path('/tmp/classic-mu')
OUT = Path('/Users/emily/Developer/Projects/owenlearining/chinese/images/classic-comics')
OUT.mkdir(parents=True, exist_ok=True)

# mu 名 -> [(quad_index 1..4, 输出文件名)]；输出名不带 .jpg
PLAN = {
    # ---- 新人物 4 格 ----
    **{n: [(i, f'{n}-c{i}') for i in range(1, 5)] for n in [
        'shaoyimingyi', 'zude', 'huangfeng', 'shengqianglang', 'hongmayi',
        'wuyong', 'yangongsheng', 'huaziliang']},
    # ---- 雅号单格 ----
    'yahao-1': [(1, 'et-yahao-liuyuxi'), (2, 'et-yahao-lihe'), (3, 'et-yahao-mengjiao'), (4, 'et-yahao-jiadao')],
    'yahao-2': [(1, 'et-yahao-chenziang'), (2, 'et-yahao-wangbo'), (3, 'et-yahao-xiaolidu')],
    # ---- 鲁滨逊 14 事件 ----
    'lubinxun-1': [(1, 'et-lubinxun-r01'), (2, 'et-lubinxun-r02'), (3, 'et-lubinxun-r03'), (4, 'et-lubinxun-r04')],
    'lubinxun-2': [(1, 'et-lubinxun-r05'), (2, 'et-lubinxun-r06'), (3, 'et-lubinxun-r07'), (4, 'et-lubinxun-r08')],
    'lubinxun-3': [(1, 'et-lubinxun-r09'), (3, 'et-lubinxun-r10'), (4, 'et-lubinxun-r11')],
    'lubinxun-4': [(1, 'et-lubinxun-r12'), (3, 'et-lubinxun-r13'), (4, 'et-lubinxun-r14')],
    # ---- 朝花夕拾 10 篇 ----
    'zhaohua-1': [(1, 'et-zhaohua-r01'), (2, 'et-zhaohua-r02'), (3, 'et-zhaohua-r03'), (4, 'et-zhaohua-r04')],
    'zhaohua-2': [(1, 'et-zhaohua-r05'), (2, 'et-zhaohua-r06'), (3, 'et-zhaohua-r07'), (4, 'et-zhaohua-r08')],
    'zhaohua-3': [(1, 'et-zhaohua-r09'), (2, 'et-zhaohua-r10')],
    # ---- 祥子三起三落 3 行 ----
    'sanqisanlu': [(1, 'et-sanqisanlu-r01'), (3, 'et-sanqisanlu-r02'), (4, 'et-sanqisanlu-r03')],
    # ---- 海底两万里 6 险境 ----
    'haidi-1': [(1, 'et-haidi-r01'), (2, 'et-haidi-r02'), (3, 'et-haidi-r03'), (4, 'et-haidi-r04')],
    'haidi-2': [(1, 'et-haidi-r05'), (2, 'et-haidi-r06')],
    # ---- 长征 6 阶段 ----
    'changzheng-1': [(1, 'et-changzheng-r01'), (2, 'et-changzheng-r02'), (3, 'et-changzheng-r03'), (4, 'et-changzheng-r04')],
    'changzheng-2': [(1, 'et-changzheng-r05'), (2, 'et-changzheng-r06')],
    # ---- 经典常谈 13 篇 ----
    'jingdian-1': [(1, 'et-jingdian-r01'), (2, 'et-jingdian-r02'), (3, 'et-jingdian-r03'), (4, 'et-jingdian-r04')],
    'jingdian-2': [(1, 'et-jingdian-r05'), (2, 'et-jingdian-r06'), (3, 'et-jingdian-r07'), (4, 'et-jingdian-r08')],
    'jingdian-3': [(1, 'et-jingdian-r09'), (2, 'et-jingdian-r10'), (3, 'et-jingdian-r11'), (4, 'et-jingdian-r12')],
    'jingdian-4': [(1, 'et-jingdian-r13')],
    # ---- 钢铁 10 行（6 阶段 + 4 次死里逃生，g1c3 同时用于 r03/r07）----
    'gangtie-1': [(1, 'et-gangtie-r01'), (2, 'et-gangtie-r02'), (3, 'et-gangtie-r03'), (4, 'et-gangtie-r04')],
    'gangtie-1b': [(3, 'et-gangtie-r07')],
    'gangtie-2': [(1, 'et-gangtie-r05'), (2, 'et-gangtie-r06'), (3, 'et-gangtie-r08'), (4, 'et-gangtie-r09')],
    'gangtie-3': [(1, 'et-gangtie-r10')],
    # ---- 艾青 10 首 ----
    'aiqing-1': [(1, 'et-aiqing-r01'), (2, 'et-aiqing-r02'), (3, 'et-aiqing-r03'), (4, 'et-aiqing-r04')],
    'aiqing-2': [(1, 'et-aiqing-r05'), (2, 'et-aiqing-r06'), (3, 'et-aiqing-r07'), (4, 'et-aiqing-r08')],
    'aiqing-3': [(1, 'et-aiqing-r09'), (2, 'et-aiqing-r10')],
    # ---- 简·爱 4 阶段 ----
    'jianai-1': [(1, 'et-jianai-r01'), (2, 'et-jianai-r02'), (3, 'et-jianai-r03'), (4, 'et-jianai-r04')],
    # ---- 红岩 6 场景 ----
    'hongyancj-1': [(1, 'et-hongyancj-r01'), (2, 'et-hongyancj-r02'), (3, 'et-hongyancj-r03'), (4, 'et-hongyancj-r04')],
    'hongyancj-2': [(1, 'et-hongyancj-r05'), (2, 'et-hongyancj-r06')],
    # ---- 唐诗体裁 6 行 ----
    'tangshi-1': [(1, 'et-tangshiti-r01'), (2, 'et-tangshiti-r02'), (3, 'et-tangshiti-r03'), (4, 'et-tangshiti-r04')],
    'tangshi-2': [(1, 'et-tangshiti-r05'), (2, 'et-tangshiti-r06')],
}


def patch_watermark(img):
    """第 4 格右下角 AI 水印：用正上方纸面纹理覆盖。"""
    w, h = img.size
    x0, x1 = w - 210, w - 8
    src = img.crop((x0, h - 112, x1, h - 66))
    img.paste(src, (x0, h - 52))
    return img


QUADS = {1: (0, 0), 2: (1, 0), 3: (0, 1), 4: (1, 1)}
total = 0
for mu_name, jobs in PLAN.items():
    mu_file = MU / f'mu-{mu_name.rstrip("b")}.png' if mu_name.endswith('b') else MU / f'mu-{mu_name}.png'
    img = Image.open(mu_file).convert('RGB')
    W, H = img.size
    hw, hh = W // 2, H // 2
    for q, out_name in jobs:
        x, y = QUADS[q]
        panel = img.crop((x * hw, y * hh, (x + 1) * hw, (y + 1) * hh))
        if q == 4:
            panel = patch_watermark(panel)
        panel.save(OUT / f'{out_name}.jpg', quality=84)
        total += 1
print(f'切格完成 {total} 张 -> {OUT}')
print(f'目录现有 {len(list(OUT.glob("*.jpg")))} 个 jpg')
