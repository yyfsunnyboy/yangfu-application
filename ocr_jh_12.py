import os, sys, json
from PIL import Image, ImageEnhance, ImageOps
import pytesseract

sys.stdout.reconfigure(encoding='utf-8')

jh_cert_dir = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活\獎狀'
results = {}

for f in sorted(os.listdir(jh_cert_dir)):
    if not f.lower().endswith(('.jpg', '.png', '.jpeg')):
        continue
    p = os.path.join(jh_cert_dir, f)
    img = Image.open(p)
    
    # Try different rotations (0, 90, 180, 270) to see which gives best Chinese text
    best_txt = ""
    best_rot = 0
    
    for rot in [0, 90, 180, 270]:
        rotated = img.rotate(rot, expand=True)
        # Enhancing contrast
        gray = ImageOps.grayscale(rotated)
        enh = ImageEnhance.Contrast(gray).enhance(1.5)
        txt = pytesseract.image_to_string(enh, lang='chi_tra+eng').strip()
        # Count Chinese chars
        zh_count = sum(1 for c in txt if '\u4e00' <= c <= '\u9fff')
        if zh_count > sum(1 for c in best_txt if '\u4e00' <= c <= '\u9fff'):
            best_txt = txt
            best_rot = rot
            
    results[f] = {
        'best_rotation': best_rot,
        'text': best_txt
    }
    print(f"File {f}: rot={best_rot}, len={len(best_txt)}, zh={sum(1 for c in best_txt if '\u4e00' <= c <= '\u9fff')}")

with open('jh_12_certs_deep.json', 'w', encoding='utf-8') as out:
    json.dump(results, out, ensure_ascii=False, indent=2)

print("Saved jh_12_certs_deep.json")
