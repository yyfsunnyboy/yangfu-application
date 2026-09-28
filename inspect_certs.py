import json
import os

with open('cert_ocr_results.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('cert_summary_readable.txt', 'w', encoding='utf-8') as out:
    for item in items:
        rel = item['rel_path']
        ocr = item['ocr_text'].strip()
        emb = item['text_embedded'].strip()
        txt = ocr if ocr else emb
        out.write(f"================================================================================\n")
        out.write(f"ID: {item['id']:02d}\n")
        out.write(f"FILE: {rel}\n")
        out.write(f"PAGES: {item['pages_count']}\n")
        out.write(f"TEXT CONTENT:\n{txt}\n\n")

print(f"Summary written for {len(items)} items.")
