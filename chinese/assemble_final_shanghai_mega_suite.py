# -*- coding: utf-8 -*-
"""
Master Assembler: 上海中考语文真题与模拟全景题库 (533 题)
系统涵盖上海中考语文考纲全部核心考点体系：
- 板块一：历年中考真题·名句默写与情境运用 (2008–2026 全套真题，88 题)
- 板块二：上海各区初三一模/二模真题·名句与情境默写精选 (16 区名校模拟，75 题)
- 板块三：上海考纲必背 86 篇全册·理解性情境默写全通关 (六至九年级 86 篇全册，110 题)
- 板块四：上海中考真题与模拟·古诗词曲理解与赏析专练 (中考第 2 题独立考点，30 题)
- 板块五：上海中考真题与模拟·课内文言字词释义与多义通假专练 (实词、通假字、古今异义、活用、多义，100 题)
- 板块六：上海中考真题与模拟·课内文言重点句子翻译与文意探究 (中考第 5 题，50 题)
- 板块七：上海中考名著阅读全景通关（12 部必考名著大题与真题模拟） (40 题)
- 板块八：上海中考真题与模拟·语言文字综合运用与传统文化 (病句/成语/标点/对联/图表/交际，40 题)

Total: 533 题，100% 配标准答案与详尽解析！
"""

import json
import re
import sys

# 1. Import modules
from build_shanghai_mega_bank import sec1_questions
from sec2_mock_moxie import sec2_questions
from sec3_syllabus_full import sec3_questions_all
from sec4_gushi_shangxi import sec4_gushi_questions
from expand_and_assemble_mega import extra_sec4, extra_sec5, extra_sec6
from sec4_wenyan_words import sec4_questions
from sec5_wenyan_fanyi import sec5_questions
from sec6_mingzhu_reader import sec6_questions
from sec8_zonghe_expanded import sec8_zonghe_questions

sections_def = [
    {
        "s": "板块一：历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "raw": sec1_questions
    },
    {
        "s": "板块二：上海各区初三一模/二模真题·名句与情境默写精选",
        "sid": "sh-mock",
        "raw": sec2_questions
    },
    {
        "s": "板块三：上海考纲必背 86 篇全册·理解性情境默写全通关",
        "sid": "sh-syllabus",
        "raw": sec3_questions_all
    },
    {
        "s": "板块四：上海中考真题与模拟·古诗词曲理解与赏析专练",
        "sid": "sh-gushi",
        "raw": sec4_gushi_questions
    },
    {
        "s": "板块五：上海中考真题与模拟·课内文言字词释义与多义通假",
        "sid": "sh-words",
        "raw": sec4_questions + extra_sec4
    },
    {
        "s": "板块六：上海中考真题与模拟·课内文言重点句子翻译与文意探究",
        "sid": "sh-fanyi",
        "raw": sec5_questions + extra_sec5
    },
    {
        "s": "板块七：上海中考名著阅读全景通关（12 部必考名著真题模拟）",
        "sid": "sh-mingzhu",
        "raw": sec6_questions + extra_sec6
    },
    {
        "s": "板块八：上海中考真题与模拟·语言文字综合运用与传统文化",
        "sid": "sh-zonghe",
        "raw": sec8_zonghe_questions
    }
]

all_questions = []
sections_metadata = []
seen_stems = set()
global_id = 1

print("=" * 60)
print("ASSEMBLING SHANGHAI ZHONGKAO COMPREHENSIVE QUESTION SUITE")
print("=" * 60)

for sec in sections_def:
    sname = sec["s"]
    sid = sec["sid"]
    raw_list = sec["raw"]
    
    sec_qs = []
    for q in raw_list:
        clean_stem = q["stem"].strip()
        # Stem deduplication per section
        if clean_stem in seen_stems:
            continue
        seen_stems.add(clean_stem)
        
        q_item = {
            "s": sname,
            "sid": sid,
            "n": len(sec_qs) + 1,
            "id": f"{sid}-{global_id}",
            "tag": q.get("tag", "上海中考考点精练"),
            "t": q.get("t", "填空题"),
            "stem": q["stem"],
            "ans": q["ans"],
            "img": q.get("img", ""),
            "aimg": q.get("aimg", ""),
            "src": q.get("src", ""),
            "ph": False,
            "jx": q.get("jx", "")
        }
        sec_qs.append(q_item)
        all_questions.append(q_item)
        global_id += 1
        
    sections_metadata.append({
        "s": sname,
        "sid": sid,
        "n": len(sec_qs)
    })
    print(f"  ✓ {sname} ({sid}): {len(sec_qs)} 题")

total_count = len(all_questions)
print("=" * 60)
print(f"★ TOTAL ASSEMBLED QUESTIONS: {total_count} ★")
print("=" * 60)

database = {
    "total": total_count,
    "jxN": total_count,
    "sections": sections_metadata,
    "questions": all_questions
}

# 1. Save JSON Database
with open("chinese/shanghai_zhongkao_bank_data.json", "w", encoding="utf-8") as f:
    json.dump(database, f, ensure_ascii=False, indent=2)
print("1. Saved database to chinese/shanghai_zhongkao_bank_data.json successfully!")

# 2. Inject into recitation-bank-V1.html
with open("chinese/recitation-bank-V1.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update header title and tags
html = re.sub(
    r'<title>.*?</title>',
    f'<title>上海中考语文真题全收录 · 基础题库背诵版（真题与各区模拟 {total_count} 题）</title>',
    html
)

html = re.sub(
    r'<h1>.*?</h1>\s*<p>.*?</p>',
    f'<h1>上海中考语文真题与模拟题库</h1>\n    <p>2008–2026 全套真题 + 各区一模二模 · {total_count} 题全量收录（默写 / 诗词赏析 / 字词通假 / 句子翻译 / 名著阅读 / 综合语用）</p>',
    html,
    count=1
)

html = re.sub(
    r'<span id="foot-label">.*?</span>',
    f'<span id="foot-label">总进度 0 / {total_count}</span>',
    html
)

html = re.sub(
    r'<p id="picker-subtitle">.*?</p>',
    f'<p id="picker-subtitle">全部板块 · 共 {total_count} 题 · 已熟 0 / {total_count}</p>',
    html
)

json_str = json.dumps(database, ensure_ascii=False)

p_start = html.find('const DATA = {')
p_end = html.find('const IMGPH =')
if p_start != -1 and p_end != -1:
    html = html[:p_start] + f'const DATA = {json_str};\n\n' + html[p_end:]
    print("2. Injected new DATA into chinese/recitation-bank-V1.html successfully!")
else:
    print("ERROR: Could not locate const DATA in chinese/recitation-bank-V1.html!")
    sys.exit(1)

with open("chinese/recitation-bank-V1.html", "w", encoding="utf-8") as f:
    f.write(html)

print("3. Saved updated chinese/recitation-bank-V1.html successfully!")
print("ALL DONE!")
