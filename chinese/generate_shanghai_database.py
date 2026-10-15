# -*- coding: utf-8 -*-
"""
Clean, self-contained generator for Shanghai Zhongkao Chinese Real Exam Question Bank.
"""
import json
import re

from build_shanghai_bank import (
    moxie_questions,
    shici_questions,
    fanyi_questions,
    mingzhu_questions,
    zonghe_questions,
    tongjia_questions
)

from build_full_shanghai_bank import (
    extra_moxie,
    extra_shici,
    extra_fanyi,
    extra_mingzhu,
    extra_zonghe,
    extra_tongjia
)

# Combine uniquely
def dedup_by_stem(q_list):
    seen = set()
    res = []
    for q in q_list:
        key = q["stem"].strip()
        if key not in seen:
            seen.add(key)
            res.append(q)
    return res

full_moxie = dedup_by_stem(moxie_questions + extra_moxie)
full_shici = dedup_by_stem(shici_questions + extra_shici)
full_fanyi = dedup_by_stem(fanyi_questions + extra_fanyi)
full_mingzhu = dedup_by_stem(mingzhu_questions + extra_mingzhu)
full_zonghe = dedup_by_stem(zonghe_questions + extra_zonghe)
full_tongjia = dedup_by_stem(tongjia_questions + extra_tongjia)

all_sections_config = [
    {
        "s": "板块一：历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "list": full_moxie
    },
    {
        "s": "板块二：历年中考真题·课内文言字词释义",
        "sid": "sh-shici",
        "list": full_shici
    },
    {
        "s": "板块三：历年中考真题·课内文言重点句子翻译与文意探究",
        "sid": "sh-fanyi",
        "list": full_fanyi
    },
    {
        "s": "板块四：历年中考真题·名著阅读全景通关",
        "sid": "sh-mingzhu",
        "list": full_mingzhu
    },
    {
        "s": "板块五：历年中考真题·语言文字综合运用",
        "sid": "sh-zonghe",
        "list": full_zonghe
    },
    {
        "s": "板块六：上海中考文言通假字与一词多义专项通关",
        "sid": "sh-tongjia",
        "list": full_tongjia
    }
]

sections_meta = []
final_questions = []

for sec in all_sections_config:
    q_list = sec["list"]
    for i, q in enumerate(q_list, start=1):
        q["s"] = sec["s"]
        q["sid"] = sec["sid"]
        q["n"] = i
        final_questions.append(q)
    sections_meta.append({
        "s": sec["s"],
        "sid": sec["sid"],
        "n": len(q_list)
    })

dataset = {
    "total": len(final_questions),
    "jxN": len(final_questions),
    "sections": sections_meta,
    "questions": final_questions
}

print(f"=== SHANGHAI ZHONGKAO DATABASE ASSEMBLED ===")
print(f"Total Sections: {len(sections_meta)}")
for s in sections_meta:
    print(f"  - {s['s']}: {s['n']} 题")
print(f"Total Authentic Questions: {len(final_questions)}")

# Write json
with open("chinese/shanghai_zhongkao_bank_data.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

# Update HTML
with open("chinese/recitation-bank-V1.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Title & Meta
html = re.sub(r'<title>.*?</title>', 
              f'<title>上海中考语文真题全收录 · 基础题库背诵版（2008–2025 全套真题 {len(final_questions)} 题）</title>', 
              html)

# 2. Update Header
html = re.sub(r'<h1>.*?</h1>\s*<p>.*?</p>', 
              f'<h1>上海中考语文真题库</h1>\n    <p>2008–2025 全套真题 · {len(final_questions)} 题全量收录（默写 / 字词 / 翻译 / 名著 / 综合）</p>', 
              html)

# 3. Update Modal Header
html = re.sub(r'<span class="sub">.*?</span>', 
              f'<span class="sub">{len(final_questions)} 题上海中考真题全局速选</span>', 
              html)

# 4. Update f-img button text to情境题
html = html.replace('<button class="fchip" id="f-img">只看需看图</button>', 
                    '<button class="fchip" id="f-img" title="筛选情境理解性默写与情境应用题">情境题专项</button>')

# 5. Fix filter logic for imgOnly in JS to filter scenario questions
html = html.replace('if(imgOnly && !q.ph) return false;', 
                    'if(imgOnly && !((q.t && q.t.includes("情境")) || (q.stem && q.stem.includes("情境")) || (q.tag && q.tag.includes("情境")))) return false;')

# 6. Inject DATA
p_start = html.find('const DATA = {')
p_end = html.find('const IMGPH =')
if p_start != -1 and p_end != -1:
    json_str = json.dumps(dataset, ensure_ascii=False)
    html = html[:p_start] + f'const DATA = {json_str};\n' + html[p_end:]
    print("Injected new DATA successfully!")

with open("chinese/recitation-bank-V1.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated chinese/recitation-bank-V1.html successfully!")
