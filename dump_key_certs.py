import fitz
from PIL import Image
import pytesseract
import io
import os

files = [
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260202_神通AI數位學院扶輪盃第一名.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\2026神通AI數位學院扶輪盃_第一名.jpg',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260428_第66屆第七區科學展優等學生獎_東區科展.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260428_第66屆第七區科學展優等學生獎_東區科展(教育部).jpg',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\9.115-66電腦與資料-東-優115.4.28 (1).pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\科展獎狀\20260606_花蓮區學習成果分享會銅獎.pdf',
    r'd:\Python\yangfu-application\00_source_materials\獎狀\足球獎狀\20251107_全校運動會800公尺高二男子組第二名.pdf'
]

with open('key_certs_text.txt', 'w', encoding='utf-8') as out:
    for f in files:
        fn = os.path.basename(f)
        out.write(f"============================================================\nFILE: {fn}\n")
        if f.endswith('.pdf'):
            doc = fitz.open(f)
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes('png')))
                txt = pytesseract.image_to_string(img, lang='chi_tra+eng')
                out.write(f"--- Page {i+1} ---\n{txt}\n")
        else:
            img = Image.open(f)
            txt = pytesseract.image_to_string(img, lang='chi_tra+eng')
            out.write(f"--- Image ---\n{txt}\n")

print("Finished writing key_certs_text.txt")
