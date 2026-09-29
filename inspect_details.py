import os, sys, json
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import fitz
import io

sys.stdout.reconfigure(encoding='utf-8')

# Inspect 20260814_232503.jpg (縣運足球)
p = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活\獎狀\20260814_232503.jpg'
img = Image.open(p).rotate(180, expand=True)
# Crop center award part
w, h = img.size
crop_img = img.crop((w*0.1, h*0.2, w*0.9, h*0.8))
txt = pytesseract.image_to_string(crop_img, lang='chi_tra')
print("=== 20260814_232503.jpg ===")
print(txt)

# Inspect 20260814_232648.jpg
p2 = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活\獎狀\20260814_232648.jpg'
img2 = Image.open(p2)
for rot in [0, 90, 180, 270]:
    t = pytesseract.image_to_string(img2.rotate(rot, expand=True), lang='chi_tra+eng')
    if any(k in t for k in ['獎', '名', '第', '證', '花', '中']):
        print(f"=== 20260814_232648.jpg (rot={rot}) ===\n{t}")

# Inspect 20260814_232756.jpg
p3 = r'd:\Python\yangfu-application\00_source_materials\陽甫國中生活\獎狀\20260814_232756.jpg'
img3 = Image.open(p3)
for rot in [0, 90, 180, 270]:
    t = pytesseract.image_to_string(img3.rotate(rot, expand=True), lang='chi_tra+eng')
    if any(k in t for k in ['獎', '名', '第', '證', '花', '中']):
        print(f"=== 20260814_232756.jpg (rot={rot}) ===\n{t}")

# Inspect 20260202_神通AI數位學院扶輪盃第一名.pdf
p4 = r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260202_神通AI數位學院扶輪盃第一名.pdf'
doc = fitz.open(p4)
page = doc[0]
pix = page.get_pixmap(dpi=300)
img4 = Image.open(io.BytesIO(pix.tobytes('png')))
txt4 = pytesseract.image_to_string(img4, lang='chi_tra+eng')
print(f"=== 神通第一名 PDF ===\n{txt4}")

# Inspect 2026神通AI數位學院扶輪盃_第一名.jpg
p5 = r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\2026神通AI數位學院扶輪盃_第一名.jpg'
img5 = Image.open(p5)
txt5 = pytesseract.image_to_string(img5, lang='chi_tra+eng')
print(f"=== 神通第一名 JPG ===\n{txt5}")

# Inspect 20260428_第66屆第七區科學展優等學生獎_東區科展.pdf
p6 = r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260428_第66屆第七區科學展優等學生獎_東區科展.pdf'
doc6 = fitz.open(p6)
page6 = doc6[0]
pix6 = page6.get_pixmap(dpi=300)
img6 = Image.open(io.BytesIO(pix6.tobytes('png')))
txt6 = pytesseract.image_to_string(img6, lang='chi_tra+eng')
print(f"=== 東區科展 PDF ===\n{txt6}")

# Inspect 9.115-66電腦與資料-東-優115.4.28 (1).pdf
p7 = r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\9.115-66電腦與資料-東-優115.4.28 (1).pdf'
doc7 = fitz.open(p7)
page7 = doc7[0]
pix7 = page7.get_pixmap(dpi=300)
img7 = Image.open(io.BytesIO(pix7.tobytes('png')))
txt7 = pytesseract.image_to_string(img7, lang='chi_tra+eng')
print(f"=== 9.115-66 電腦與資料 PDF ===\n{txt7}")
