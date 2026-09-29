import pymupdf
import os
import shutil

target_files = [
    r"c:\Users\yehya\Documents\GitHub\yangfu-application\陽甫調整\NTHU\EE\清大電機自傳_讀書計畫_final.pdf",
    r"c:\Users\yehya\Documents\GitHub\yangfu-application\陽甫調整\NTHU\EE\清大電機自傳_讀書計畫_v23.pdf",
    r"c:\Users\yehya\Downloads\清大電機自傳_讀書計畫_final.pdf",
    r"c:\Users\yehya\Downloads\清大電機自傳_讀書計畫_v23.pdf",
    r"c:\Users\yehya\Documents\GitHub\yangfu-application\陽甫調整\build_7page_final.pdf"
]

new_uri = "https://www.youtube.com/watch?v=gZmmkk7PP_w"
old_key = "1bLvNYKtLrL44qFtmK9ETaoxTniMMk5lB"

for fpath in target_files:
    if not os.path.exists(fpath):
        print(f"Skipping (not found): {fpath}")
        continue
    
    doc = pymupdf.open(fpath)
    count = 0
    for pno, p in enumerate(doc):
        for l in p.get_links():
            uri = l.get("uri", "")
            if old_key in uri:
                xref = l["xref"]
                doc.xref_set_key(xref, "A/URI", f"({new_uri})")
                count += 1
                print(f"[{os.path.basename(fpath)}] Page {pno+1}: updated link xref {xref} -> {new_uri}")
    
    # Save safely
    temp_path = fpath + ".tmp.pdf"
    doc.save(temp_path, clean=False)
    doc.close()
    shutil.move(temp_path, fpath)
    print(f"Saved: {fpath} ({count} link(s) updated)\n")

# Verify all files
print("=== VERIFICATION ===")
for fpath in target_files:
    if os.path.exists(fpath):
        doc = pymupdf.open(fpath)
        p2_links = doc[1].get_links()
        print(f"[{os.path.basename(fpath)}] Page 2 links:")
        for l in p2_links:
            print("  -", l.get("uri"))
        doc.close()
