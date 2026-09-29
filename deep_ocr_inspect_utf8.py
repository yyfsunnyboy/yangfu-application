import os, sys, json
import fitz
from PIL import Image
import pytesseract
import io

sys.stdout.reconfigure(encoding='utf-8')

# Target files in 獎狀
target_files = [
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260202_神通AI數位學院扶輪盃第一名.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260428_第66屆第七區科學展優等學生獎_東區科展.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\2026神通AI數位學院扶輪盃_第一名.jpg',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\9.115-66電腦與資料-東-優115.4.28 (1).pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\足球獎狀\20251107_全校運動會800公尺高二男子組第二名.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\學業獎狀\20251031_班級幹部服務證書_事務股長.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\學業獎狀\20240926_英語演說複賽第四名.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20250301_113學年校內科展工程學科優勝_香蕉葉環保餐具_日期不確定.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20250301_113學年校內科展工程學科優勝_香蕉葉環保餐具_副本_日期不確定.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260428_第66屆第七區科學展優等學生獎_東區科展(教育部).jpg'
]

deep_results = {}
for p in target_files:
    fn = os.path.basename(p)
    if not os.path.exists(p):
        continue
    if p.endswith('.pdf'):
        doc = fitz.open(p)
        pages_t = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes('png')))
            t = pytesseract.image_to_string(img, lang='chi_tra+eng')
            pages_t.append(f"--- Page {i+1} ---\n{t.strip()}")
        deep_results[fn] = "\n".join(pages_t)
    else:
        img = Image.open(p)
        t = pytesseract.image_to_string(img, lang='chi_tra+eng')
        deep_results[fn] = t.strip()

with open('deep_cert_ocr.json', 'w', encoding='utf-8') as out:
    json.dump(deep_results, out, ensure_ascii=False, indent=2)

print("Target certs saved.")

# Inspect 陽甫國中生活 awards
jh_dir = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活'
jh_results = {}
if os.path.exists(jh_dir):
    for root, dirs, files in os.walk(jh_dir):
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.pdf']:
                full_path = os.path.join(root, f)
                rel = os.path.relpath(full_path, jh_dir)
                try:
                    if ext == '.pdf':
                        doc = fitz.open(full_path)
                        pages_t = []
                        for page in doc:
                            pix = page.get_pixmap(dpi=200)
                            img = Image.open(io.BytesIO(pix.tobytes('png')))
                            pages_t.append(pytesseract.image_to_string(img, lang='chi_tra+eng'))
                        t = "\n".join(pages_t).strip()
                    else:
                        img = Image.open(full_path)
                        t = pytesseract.image_to_string(img, lang='chi_tra+eng').strip()
                    jh_results[rel] = t
                except Exception as e:
                    jh_results[rel] = f"Error: {e}"

with open('jh_ocr_results.json', 'w', encoding='utf-8') as out:
    json.dump(jh_results, out, ensure_ascii=False, indent=2)

print(f"Junior high materials processed: {len(jh_results)} files.")
