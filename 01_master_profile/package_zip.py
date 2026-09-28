import zipfile
import os
import shutil

workspace = r"D:\Python\yangfu-application\01_master_profile"
zip_dir = os.path.join(workspace, "claude_design_bundle")
os.makedirs(zip_dir, exist_ok=True)
assets_dir = os.path.join(zip_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)

# 1. Copy photo
photo_src = r"D:\Python\yangfu-application\00_source_materials\照片\YEH YANG FU.jpg"
shutil.copy(photo_src, os.path.join(assets_dir, "photo.jpg"))

# 2. Copy HTML as index.html and 09_first_page_overview.html
html_src = os.path.join(workspace, "09_first_page_overview.html")
shutil.copy(html_src, os.path.join(zip_dir, "index.html"))
shutil.copy(html_src, os.path.join(zip_dir, "09_first_page_overview.html"))

# 3. Copy PDF and PNG
shutil.copy(os.path.join(workspace, "09_first_page_overview.pdf"), os.path.join(zip_dir, "09_first_page_overview.pdf"))
shutil.copy(os.path.join(workspace, "09_first_page_overview.png"), os.path.join(zip_dir, "09_first_page_overview.png"))

# 4. Create README.md
readme_content = """# 葉陽甫｜高中學習與成果總覽 (Claude Design 編輯包)

本壓縮包專為匯入 **Claude Design / Web Artifacts** 進行視覺檢視、模組化微調與二次設計所打包。

## ▍檔案結構清單
- `index.html`：核心入口網頁（純原生 HTML + CSS，內嵌 Google Fonts 與 Base64 高解析照片，零外部相依性，匯入 Claude Design 或瀏覽器即可即時渲染）。
- `09_first_page_overview.html`：備份原始命名的網頁檔。
- `assets/photo.jpg`：高解析度證件照片原檔。
- `09_first_page_overview.pdf`：標準 A4 單頁列印成果 PDF（100% 比例嚴格鎖定 1 頁，無溢出）。
- `09_first_page_overview.png`：A4 完整渲染高解析度預覽截圖。

## ▍設計規範與色票速查 (Design Tokens)
- **主色（深藍 Navy）**：`#0f294a`（用於主標題、代表大獎、關鍵數字、外框、頁首膠囊）
- **次要文字色（石墨深灰）**：`#334155` / `#475569`
- **強調色 1（科技金／琥珀）**：`#b45309`（用於 4 大核心 Badge 星號與關鍵榮譽）
- **強調色 2（深青綠 Teal）**：`#0d9488`（用於個人定位標籤、前段百分比與次要代表成果）
- **背景淺灰**：`#f8fafc` / `#f1f5f9`
- **字級下限**：正文 >= 12 pt（16px），姓名 22.5 pt，分類標題 13.5–14 pt。
- **畫布比例**：A4 直式（210mm × 297mm），四周邊距約 12–14 mm。
"""

with open(os.path.join(zip_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

# 5. Create ZIP
zip_filename = os.path.join(workspace, "09_first_page_overview_claude_design.zip")
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, zip_dir)
            zipf.write(file_path, arcname)

print("ZIP created successfully at:", zip_filename)
print(f"ZIP size: {os.path.getsize(zip_filename)} bytes")
print("ZIP contents:")
with zipfile.ZipFile(zip_filename, "r") as zipf:
    for name in zipf.namelist():
        print(" -", name)

# Clean up temp folder
shutil.rmtree(zip_dir)
