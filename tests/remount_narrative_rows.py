#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""叙事表改造：删掉「表后单格画廊」，改为每行文字下方紧跟 4 格连环画（与人物表一致）。

- ① = 原有 {prefix}-r{NN}.jpg，图注 ①行名
- ②③④ = {prefix}-r{NN}-b2/b3/b4.jpg，图注取自 expand_plan.ROWS
"""
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from expand_plan import ROWS

ROOT = pathlib.Path(__file__).resolve().parent.parent
DST = ROOT / 'chinese' / 'classic-reading-V4.html'
IMG = 'images/classic-comics'

# (h3 关键字, 图名前缀, 行数, 旧画廊标题)
TABLES = [
    ('四次出海历险', 'et-lubinxun', 14, '鲁滨逊历险 14 事件连环画（按行序）'),
    ('十篇回忆散文全景分析表', 'et-zhaohua', 10, '《朝花夕拾》十篇散文连环画（按行序）'),
    ('三起三落', 'et-sanqisanlu', 3, '祥子「三起三落」连环画（按行序）'),
    ('环球航线与六大险境表', 'et-haidi', 6, '「鹦鹉螺号」六大险境连环画（按行序）'),
    ('长征路线关键节点表', 'et-changzheng', 6, '红军长征六阶段连环画（按行序）'),
    ('十三篇核心章节全景考点表', 'et-jingdian', 13, '《经典常谈》十三篇连环画（按行序）'),
    ('六大成长阶段与四次死里逃生表', 'et-gangtie', 10, '保尔成长六阶段连环画（按行序）'),
    ('十首经典诗作鉴赏全景表', 'et-aiqing', 10, '《艾青诗选》十首诗作连环画（按行序）'),
    ('人生四大阶段环境蜕变与精神成长表', 'et-jianai', 4, '简·爱成长四阶段连环画（按行序）'),
    ('六大革命斗争场景与环境表', 'et-hongyancj', 6, '《红岩》六大斗争场景连环画（按行序）'),
    ('诗歌体裁演变全景表', 'et-tangshiti', 6, '唐诗体裁演变连环画（按行序）'),
]


def row_html(prefix, n, colspan):
    key = f'{prefix}-r{n:02d}'
    name, _scenes, caps = ROWS[key]
    pairs = [(f'{IMG}/{key}.jpg', f'①{name}')]
    pairs += [(f'{IMG}/{key}-b{i}.jpg', f'{c}') for i, c in zip((2, 3, 4), caps)]
    figs = '\n'.join(
        f'                <figure><img src="{img}" alt="{name}第{i+1}格" loading="lazy" '
        f'onclick="openModal(this.src, this.alt)"><figcaption>{cap}</figcaption></figure>'
        for i, (img, cap) in enumerate(pairs))
    return (f'\n              <tr class="comic-row"><td colspan="{colspan}" style="padding-top:0.2rem;">\n'
            f'                <div class="comic-strip">\n'
            f'                  <div class="comic-head">\n'
            f'                    <span class="comic-title-badge">🎞 四格连环画</span>\n'
            f'                    <span class="comic-chapter">{name} · 情节画传（点击可放大）</span>\n'
            f'                  </div>\n'
            f'                  <div class="comic-panels">\n{figs}\n                  </div>\n'
            f'                </div>\n'
            f'              </td></tr>')


def cut_div(src, start):
    """按 div 深度配平，返回该 div 的结束位置（不含）。"""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', src[start:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth == 0:
            return start + m.end()
    raise AssertionError('div 未配平')


def main():
    src = DST.read_text(encoding='utf-8')

    # 1) 删除旧画廊条（保留雅号表那条）
    removed = 0
    for _key, _prefix, _n, title in TABLES:
        i = src.find(title)
        assert i > 0, f'未找到旧画廊标题：{title}'
        # 往前找到所在 comic-strip 的起始
        s = src.rfind('<div class="comic-strip">', 0, i)
        assert s > 0
        e = cut_div(src, s)
        # 连同前面的空白换行一起删
        seg = src[s:e]
        assert 'comic-strip' in seg
        src = src[:s] + src[e:]
        removed += 1
    print(f'删除旧画廊条 {removed} 条（雅号表保留）')

    # 2) 每行下方插入 4 格 comic-row
    inserts = []
    for key, prefix, nrows, _title in TABLES:
        h = src.find(key)
        assert h > 0, f'未找到表：{key}'
        tm = re.search(r'<table class="data-table">(.*?)</table>', src[h:], re.S)
        assert tm, key
        body = tm.group(1)
        # body 起点 = h + tm.start() + '<table class="data-table">'.__len__()
        base = h + tm.start() + len('<table class="data-table">')
        trs = list(re.finditer(r'</tr>', body))
        # 数据行 = 除表头行外的 tr；表头行含 <th>
        data_rows = []
        for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', body, re.S):
            if '<th' in tr.group(1):
                continue
            data_rows.append(base + tr.end())
        assert len(data_rows) == nrows, f'{key}: 行数 {len(data_rows)} != {nrows}'
        colspan = len(re.findall(r'<th', re.search(r'<thead>(.*?)</thead>', body, re.S).group(1)))
        for i, pos in enumerate(data_rows, 1):
            inserts.append((pos, row_html(prefix, i, colspan)))
    print(f'待插入 comic-row {len(inserts)} 条')

    for pos, text in sorted(inserts, reverse=True):
        src = src[:pos] + text + src[pos:]

    DST.write_text(src, encoding='utf-8')
    print(f'OK -> {DST.name} ({len(src)/1024:.0f} KB)')


if __name__ == '__main__':
    main()
