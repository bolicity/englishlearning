#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由 recitation-data-V1.json 的 hardList 生成「难字→拼音」映射（按篇）。

用法: python3 tests/build_pinyin_map.py
产出: chinese/recitation-pinyin-V1.json   {slug: {字: 拼音}}

清洗规则：
1. 取 py 第一个「，/ ,」之前的部分（去掉释义）
2. 含「、」多段拼音 → 取与单字默认读音一致的那段，否则取第一段
3. 含空格的多音节词（如 wēi yí）→ 取最后一个音节（目标字都在词尾）
4. 提取失败 → 用 pypinyin 兜底
"""
import json
import pathlib
import re
import sys

from pypinyin import Style, pinyin

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'chinese'))
import recitation_comics_data as M  # noqa: E402

PY_CHARS = r'a-zA-ZüÜ\u00c0-\u024f'          # 含带声调拉丁字母
RE_TOKEN = re.compile(rf'^[{PY_CHARS}\s]+')

# ---- 人工修订 ----
# 1) 现教材审定读音（旧读或数据有误）
MANUAL_CHAR = {
    'shengyuyouhuan': {'舜': 'shùn', '拂': 'fú'},  # 「行拂乱其所为」fú（bì 在「法家拂士」）
    'shuidiaogetou': {'胜': 'shèng'},              # 「高处不胜寒」，现读 shèng
    'jiangchengzi': {'骑': 'qí'},                  # 「千骑卷平冈」，现读 qí
    'jiezishu': {'治': 'zhì'},                     # 「险躁则不能治性」，修养，读 zhì
    # 2) 本页 4 格诗句中该字读常规音（特殊音出现在未入选的句子）
    'lunyu': {'有': 'yǒu'},          # 「有朋自远方来」「必有我师」皆 yǒu（yòu 在「十有五」）
    'tiaotiao': {'间': 'jiān'},      # 「盈盈一水间」读 jiān
    'hezhouji': {'有': 'yǒu'},       # 「明有奇巧人曰王叔远」（yòu 在「三十有四」）
    'mashuo': {'食': 'shí'},         # 「食不饱」（sì 在「食马者」）
    'yuwosuoyuye': {'与': 'yǔ'},     # 「呼尔而与之」（yú 在「得我与」）
    'suiyoujiaoyao': {'学': 'xué'},  # 「弗学」「学然后知不足」（xiào 在「教学相长」）
    'mulanshi': {'帖': 'tiě', '裳': 'cháng'},  # 「军帖」tiě；「旧时裳」cháng
}
# 3) 词组级注音（优先于单字）
MANUAL_WORD = {
    'suiyoujiaoyao': {'教学相长': 'jiào xiào xiāng zhǎng'},
}


def auto_py(zi: str) -> str:
    if not zi:
        return ''
    return pinyin(zi, style=Style.TONE)[0][0]


def clean_py(zi: str, raw: str):
    """返回 (拼音, 说明)；说明记录人工值是否被修正。"""
    head = re.split(r'[，,]', raw.strip())[0]
    tokens = re.findall(rf'[{PY_CHARS}]+', head)
    if not tokens:
        return auto_py(zi), f'提取失败→自动({raw})'
    if len(tokens) == 1:
        return tokens[0], ''

    # 多 token：优先取与单字默认读音一致者（处理「娟 chán、juān」类）
    a = auto_py(zi)
    for t in tokens:
        if t == a:
            return t, '' if tokens[0] == t else f'多段匹配({raw})'
    # 否则按词音尾字规则（目标字均在词尾：逶迤 wēi yí → 迤 yí）
    return tokens[-1], f'词音取末({raw})'


def main():
    data = json.load(open(ROOT / 'chinese' / 'recitation-data-V1.json', encoding='utf-8'))
    # title -> slug（以连环画数据为准）
    title2slug = {}
    for v in M.DATA:
        for it in v['items']:
            title2slug.setdefault(it['title'], it['slug'])

    out, fixes, missing = {}, [], []
    n_entries = 0
    for v in data:
        for it in v['items']:
            slug = title2slug.get(it['title'])
            if not slug:
                missing.append(it['title'])
                continue
            slot = out.setdefault(slug, {})
            for h in (it.get('hardList') or []):
                zi = h['zi'].strip()
                if not zi:
                    continue
                py, note = clean_py(zi, h['py'])
                slot[zi] = py
                n_entries += 1
                if note:
                    fixes.append((it['title'], zi, h['py'], py, note))

    # 人工修订
    for slug, m in MANUAL_CHAR.items():
        if slug not in out:
            continue
        for zi, py in m.items():
            old = out[slug].get(zi, '(无)')
            out[slug][zi] = py
            if old != py:
                if old == '(无)':
                    fixes.append((slug, zi, '补充', py, '补齐易错字'))
                else:
                    fixes.append((slug, zi, old, py, '读音修订'))

    words = {k: v for k, v in MANUAL_WORD.items() if k in out}
    payload = {slug: {'c': chars, 'w': words.get(slug, {})}
               for slug, chars in out.items()}

    dest = ROOT / 'chinese' / 'recitation-pinyin-V1.json'
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding='utf-8')

    n_py = sum(len(m['c']) for m in payload.values())
    print(f'wrote {dest}')
    print(f'篇数 {len(payload)}/{len(M.DATA)}  难字条目 {n_entries}  去重后 {n_py}')
    print(f'未匹配篇 {len(missing)} {missing}')
    print(f'自动/人工修正 {len(fixes)} 条：')
    for f in fixes:
        print(f'  {f[0]} | {f[1]} | raw={f[2]} → {f[3]}  [{f[4]}]')

    # 覆盖率：诗句中出现的难字
    hit = tot = 0
    for v in M.DATA:
        for it in v['items']:
            m = payload.get(it['slug'], {}).get('c', {})
            for verse, _ in it['panels']:
                for ch in verse:
                    if ch in m:
                        hit += 1
    print(f'诗句中难字命中 {hit} 处')


if __name__ == '__main__':
    main()
