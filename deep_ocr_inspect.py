import os, sys, json
import fitz
from PIL import Image
import pytesseract
import io

# 1. Inspect specific files in 獎狀
target_files = [
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260202_神通AI數位學院扶輪盃第一名.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260428_第66屆第七區科學展優等學生獎_東區科展.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\2026神通AI數位學院扶輪盃_第一名.jpg',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\9.115-66電腦與資料-東-優115.4.28 (1).pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\足球獎狀\20251107_全校運動會800公尺高二男子組第二名.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\學業獎狀\20251031_班級幹部服務證書_事務股長.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\學業獎狀\20240926_英語演說複賽第四名.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20250301_113學年校內科展工程學科優勝_香蕉葉環保餐具_日期不確定.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20250301_113學年校內科展工程學科優勝_香蕉葉環保餐具_副本_日期不確定.pdf'
]

print("=== DEEP OCR OF SPECIFIC FILES ===")
for p in target_files:
    fn = os.path.basename(p)
    print(f"\n--- FILE: {fn} ---")
    if p.endswith('.pdf'):
        doc = fitz.open(p)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes('png')))
            t = pytesseract.image_to_string(img, lang='chi_tra+eng')
            print(f"[Page {i+1} Text]:\n{t.strip()}")
    else:
        img = Image.open(p)
        t = pytesseract.image_to_string(img, lang='chi_tra+eng')
        print(f"[Image Text]:\n{t.strip()}")

# 2. Inspect 陽甫國中生活 awards
jh_dir = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活'
print("\n=== INSPECTING JUNIOR HIGH AWARDS ===")
jh_results = {}
for root, dirs, files in os.walk(jh_dir):
    for f in sorted(files):
        if any(ext in f.lower() for ext in ['.jpg', '.jpeg', '.png', '.pdf']):
            full_path = os.path.join(root, f)
            rel = os.path.relpath(full_path, jh_dir)
            try:
                if f.lower().endswith('.pdf'):
                    doc = fitz.open(full_path)
                    t_list = []
                    for page in doc:
                        pix = page.get_pixmap(dpi=200)
                        img = Image.open(io.BytesIO(pix.tobytes('png')))
                        t_list.append(pytesseract.image_to_string(img, lang='chi_tra+eng'))
                    text = '\n'.join(t_list).strip()
                else:
                    img = Image.open(full_path)
                    text = pytesseract.image_to_string(img, lang='chi_tra+eng').strip()
                jh_results[rel] = text
            except Exception as e:
                jh_results[rel] = f"Error: {e}"

with open('jh_ocr_results.json', 'w', encoding='utf-8') as out:
    json.dump(jh_results, out, ensure_ascii=False, indent=2)

print(f"Processed {len(jh_results)} files from 陽甫國中生活.")
