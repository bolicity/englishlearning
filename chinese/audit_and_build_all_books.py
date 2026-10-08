import json

with open('chinese/classic-reading-ocr-raw-V1.json', 'r', encoding='utf-8') as f:
    raw_pages = json.load(f)

# 打印各页的原始文本块
page_texts = {p['page']: p['text'] for p in raw_pages}
print("Loaded all 39 pages.")
