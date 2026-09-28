import os, sys, json
from PIL import Image
import pytesseract

sys.stdout.reconfigure(encoding='utf-8')

jh_cert_dir = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活\獎狀'
jh_fixed_dir = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活\修過的照片'
jh_root = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活'

files_to_ocr = {}

# 1. 獎狀 folder
if os.path.exists(jh_cert_dir):
    for f in os.listdir(jh_cert_dir):
        if f.lower().endswith(('.jpg', '.png', '.jpeg')):
            files_to_ocr[os.path.join(jh_cert_dir, f)] = f"獎狀/{f}"

# 2. 修過的照片 folder
if os.path.exists(jh_fixed_dir):
    for f in os.listdir(jh_fixed_dir):
        if f.lower().endswith(('.jpg', '.png', '.jpeg')) and any(k in f for k in ['獎狀', '證書', '銀牌', '特優', '優等', '一等獎', '優良獎']):
            files_to_ocr[os.path.join(jh_fixed_dir, f)] = f"修過的照片/{f}"

# 3. root specific list files
for f in ['2021太平洋盃科技教育競賽得獎名單.jpg', '2023 IEYI 世界青少年創客發明展暨臺灣選拔賽 銀牌得獎名單.jpg']:
    p = os.path.join(jh_root, f)
    if os.path.exists(p):
        files_to_ocr[p] = f"root/{f}"

results = {}
for full_path, label in files_to_ocr.items():
    try:
        img = Image.open(full_path)
        t = pytesseract.image_to_string(img, lang='chi_tra+eng').strip()
        results[label] = t
        print(f"Processed: {label} (len: {len(t)})")
    except Exception as e:
        results[label] = f"Error: {e}"

with open('jh_key_awards_ocr.json', 'w', encoding='utf-8') as out:
    json.dump(results, out, ensure_ascii=False, indent=2)

print("Saved jh_key_awards_ocr.json successfully.")
