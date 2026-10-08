import json

# Load raw OCR text
with open('chinese/classic-reading-ocr-raw-V1.json', 'r', encoding='utf-8') as f:
    ocr_pages = json.load(f)

print(f"Loaded {len(ocr_pages)} pages of OCR data.")
