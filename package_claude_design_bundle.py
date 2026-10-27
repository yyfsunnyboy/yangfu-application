import os
import re
import base64
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_ASSETS = ROOT / "陽甫調整" / "4頁對折本_assets"
OUT_PDF_DIR = ROOT / "output" / "pdf"
PREVIEW_DIR = ROOT / "tmp" / "booklet_v8_preview"

BUNDLE_DIR = ROOT / "tmp" / "claude_design_bundle"
if BUNDLE_DIR.exists():
    shutil.rmtree(BUNDLE_DIR)
BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Subdirectories
(BUNDLE_DIR / "assets").mkdir(parents=True, exist_ok=True)
(BUNDLE_DIR / "preview").mkdir(parents=True, exist_ok=True)
(BUNDLE_DIR / "pdf").mkdir(parents=True, exist_ok=True)

# 2. Import base HTML from build_interview_booklet_v8_academic_clean
import build_interview_booklet_v8_academic_clean as v8
raw_html = v8.build_html()

# Extract all referenced assets
asset_filenames = sorted(set(re.findall(r"file:///[^\"']+/([^\"'/]+\.(?:png|jpe?g|svg|webp))", raw_html, re.IGNORECASE)))
print(f"Found {len(asset_filenames)} asset references in HTML:")
for fn in asset_filenames:
    print(" -", fn)

# 3. Copy referenced assets to bundle/assets
base64_map = {}
for fn in asset_filenames:
    src_file = SRC_ASSETS / fn
    if src_file.exists():
        dst_file = BUNDLE_DIR / "assets" / fn
        shutil.copy2(src_file, dst_file)
        
        # Build base64 data uri
        mime = "image/jpeg" if fn.lower().endswith((".jpg", ".jpeg")) else "image/png"
        with open(src_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            base64_map[fn] = f"data:{mime};base64,{b64}"
    else:
        print(f"WARNING: Asset not found: {src_file}")

# 4. Generate index.html (Relative paths: assets/...)
html_relative = re.sub(
    r"file:///[^\"']+/([^\"'/]+\.(?:png|jpe?g|svg|webp))",
    r"assets/\1",
    raw_html,
    flags=re.IGNORECASE
)
(BUNDLE_DIR / "index.html").write_text(html_relative, encoding="utf-8")
print("Generated index.html with relative asset paths.")

# 5. Generate index_standalone.html (Base64 embedded images, zero dependencies)
def replace_with_base64(match):
    fn = match.group(1)
    return base64_map.get(fn, f"assets/{fn}")

html_standalone = re.sub(
    r"file:///[^\"']+/([^\"'/]+\.(?:png|jpe?g|svg|webp))",
    replace_with_base64,
    raw_html,
    flags=re.IGNORECASE
)
(BUNDLE_DIR / "index_standalone.html").write_text(html_standalone, encoding="utf-8")
print("Generated index_standalone.html with Base64 embedded assets.")

# 6. Generate A3 Spread View HTML (a3_spread_view.html)
# Split pages from html_relative
pages = re.findall(r'(<div class="page" id="page\d">[\s\S]*?</div>\s*<!-- PAGE \d|\Z)', html_relative)
# Clean extract of page1, page2, page3, page4
p1_m = re.search(r'(<div class="page" id="page1">[\s\S]*?</div>)\s*(?:<!-- PAGE 2|$)', html_relative)
p2_m = re.search(r'(<div class="page" id="page2">[\s\S]*?</div>)\s*(?:<!-- PAGE 3|$)', html_relative)
p3_m = re.search(r'(<div class="page" id="page3">[\s\S]*?</div>)\s*(?:<!-- PAGE 4|$)', html_relative)
p4_m = re.search(r'(<div class="page" id="page4">[\s\S]*?</div>)\s*(?:</body>|$)', html_relative)

head_m = re.search(r'([\s\S]*?<style>[\s\S]*?</style>[\s\S]*?</head>)', html_relative)

if p1_m and p2_m and p3_m and p4_m and head_m:
    head_content = head_m.group(1)
    # Add A3 spread styling
    a3_style = """
<style>
  @page {
    size: 420mm 297mm;
    margin: 0;
  }
  body {
    background: #e2e8f0;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }
  .a3-sheet {
    width: 420mm;
    height: 297mm;
    background: #ffffff;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    display: flex;
    position: relative;
    page-break-after: always;
    overflow: hidden;
  }
  .a3-sheet .page {
    width: 210mm !important;
    height: 297mm !important;
    page-break-after: avoid !important;
    border: none !important;
    box-shadow: none !important;
  }
  .fold-line {
    position: absolute;
    left: 210mm;
    top: 0;
    bottom: 0;
    width: 0;
    border-left: 1.5px dashed #cbd5e1;
    z-index: 999;
    pointer-events: none;
  }
  .sheet-tag {
    position: absolute;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 41, 66, 0.85);
    color: #ffffff;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 4px;
    z-index: 1000;
    pointer-events: none;
  }
</style>
"""
    head_a3 = head_content.replace("</head>", f"{a3_style}\n</head>")
    
    # Sheet 1 (Outside): Left = P4 (Back), Right = P1 (Cover)
    # Sheet 2 (Inside): Left = P2 (System), Right = P3 (Research)
    a3_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
{head_a3[head_a3.find('<head>'):]}
<body>

<!-- SHEET 1 (外側面，雙面列印外折): 左邊第 4 頁 (封底) ｜ 右邊第 1 頁 (封面) -->
<div class="a3-sheet" id="sheet1">
  <div class="sheet-tag">A3 外側對折跨頁：左 = 第 4 頁 (封底) ｜ 右 = 第 1 頁 (封面)</div>
  <div class="fold-line"></div>
  {p4_m.group(1)}
  {p1_m.group(1)}
</div>

<!-- SHEET 2 (內側面，翻開內頁): 左邊第 2 頁 (系統工程) ｜ 右邊第 3 頁 (科學研究) -->
<div class="a3-sheet" id="sheet2">
  <div class="sheet-tag">A3 內側跨頁展開：左 = 第 2 頁 (系統工程) ｜ 右 = 第 3 頁 (科學研究)</div>
  <div class="fold-line"></div>
  {p2_m.group(1)}
  {p3_m.group(1)}
</div>

</body>
</html>
"""
    (BUNDLE_DIR / "a3_spread_view.html").write_text(a3_html, encoding="utf-8")
    print("Generated a3_spread_view.html with A3 folding spread preview.")

# 7. Copy Compiled PDFs
a3_pdf = OUT_PDF_DIR / "葉陽甫_面試四面小冊_典雅學術版_A3雙面列印.pdf"
a4_pdf = OUT_PDF_DIR / "葉陽甫_面試四面小冊_典雅學術版_A4閱讀.pdf"
if a3_pdf.exists():
    shutil.copy2(a3_pdf, BUNDLE_DIR / "pdf" / a3_pdf.name)
    shutil.copy2(a3_pdf, BUNDLE_DIR / a3_pdf.name)
if a4_pdf.exists():
    shutil.copy2(a4_pdf, BUNDLE_DIR / "pdf" / a4_pdf.name)

# 8. Copy Previews (Only official page and sheet renders)
if PREVIEW_DIR.exists():
    for pv in PREVIEW_DIR.iterdir():
        if pv.is_file() and pv.suffix.lower() == ".png" and (pv.name.startswith("a4_p") or pv.name.startswith("a3_sheet")):
            shutil.copy2(pv, BUNDLE_DIR / "preview" / pv.name)

# 9. Create README.md & prompt_for_claude.md
readme_text = r"""# 葉陽甫｜面試四面小冊 (典雅學術版) Claude Design 設計匯入包

本壓縮包專為匯入 **Claude Design / Claude Artifacts / Web Projects** 進行高自由度視覺編輯、排版微調與二次設計所打包。

---

## ▍檔案結構速覽

```text
├── index.html                   # 核心網頁檔 (A4 4頁直式排列，使用 assets/ 相對路徑)
├── index_standalone.html        # 單檔自包含網頁 (所有圖片已轉 Base64 內嵌，零外部依賴，可直接貼入 Claude Artifacts 即時預覽)
├── a3_spread_view.html          # A3 雙面列印對折跨頁模擬檢視 (Sheet 1: P4+P1, Sheet 2: P2+P3，帶中折虛線)
├── README.md                    # 本文件 (設計規範、排版結構與色票速查)
├── prompt_for_claude.md         # 專門提供給 Claude Design 的設計引導提示詞 (Prompt Template)
├── assets/                      # 13 張原解析度影像資產
│   ├── YEH YANG FU.jpg          # P1 學生證件大頭照
│   ├── ai_student_practice_screen.png # P2 數學自適應系統實際操作截圖
│   ├── rotary_award_photo.png   # P2 神通AI扶輪盃全國第一名得獎合影
│   ├── yuxiu_award_photo.png    # P2 育秀盃創意獎全國金獎得獎合影
│   ├── healer_blind_repair_rules.png # P3 AST Healer 答案盲修復與固定規則架構圖
│   ├── healer_chart_user.png    # P3 4種 Prompt × 3模型測試救援柱狀圖
│   ├── soccer_team_perfect.png  # P4 花中足球校隊全國聯賽決賽現場團體合影 (比例提升·切齊微調版)
│   ├── qr_soccer_highlight.png  # P4 114學年決賽直播精彩畫面 QR Code
│   ├── qr_fbref_github.png      # P4 FBref 足球數據分析 GitHub 專案 QR Code
│   ├── english_img2.jpeg        # P4 TOEIC 945 金色證書
│   ├── english_img1.jpeg        # P4 GEPT 全民英檢中高級合格證書 (工整對齊版)
│   ├── qr_demo.png              # P4 AI 學習系統公開 Demo QR Code
│   └── qr_github.png            # P4 系統專案 GitHub 原始碼 QR Code
├── pdf/                         # 原始編譯輸出之高畫質 PDF
│   ├── 葉陽甫_面試四面小冊_典雅學術版_A3雙面列印.pdf # A3 橫向雙面列印對折版 (2 張 A3)
│   └── 葉陽甫_面試四面小冊_典雅學術版_A4閱讀.pdf     # A4 單頁直式閱讀版 (4 頁 A4)
└── preview/                     # 各頁 150 DPI 高解析渲染截圖 (a4_p1~p4.png, a3_sheet1~2.png)
```

---

## ▍設計規範與色票系統 (Design Tokens)

- **主色 (Oxford Navy)**：`#0f2942`（標題、大獎抬頭、頂部膠囊、關鍵徽章、底線）
- **深藍次強調色 (Academic Blue)**：`#1e3a8a`（關鍵排名數據、重要超連結、數理亮點）
- **琥珀金強調色 (Achievement Gold)**：`#b45309`（全國金獎、全國第一名、多益金色證書）
- **石墨深灰 (Body Slate)**：`#1e293b` / `#334155`（內文主要文字）
- **鋼鐵冷灰 (Secondary Slate)**：`#475569` / `#64748b`（說明文字、次級標籤、頁尾）
- **背景淺灰 (Card Surface)**：`#f8fafc` / `#f1f5f9`（區塊背景、引言卡片）
- **邊框灰 (Border Slate)**：`#cbd5e1` / `#e2e8f0`（微細分隔線、照片外框）

---

## ▍版面結構與列印尺寸規格

- **頁面物理尺寸**：
  - **A4 直式**：`210mm × 297mm`，頁面留白四周約 `10mm ~ 13mm`，嚴格鎖定無溢出。
  - **A3 橫向對折**：`420mm × 297mm`（外側：左 P4、右 P1；內側：左 P2、右 P3，中折線為 $x = 210\,\text{mm}$）。
- **四面內容架構**：
  - **第 1 頁 (封面 / 個人總覽)**：個人資訊、4 大成就標籤、學業與基礎能力、外語溝通能力、足球競技投入、代表性科研、核心專案、程式實作。
  - **第 2 頁 (跨頁左面 / 系統工程篇)**：AI 自適應輔助學習系統從需求拆解到花蓮高商課堂部署、全端微服務架構、真實得獎合影、跨頁技術痛點銜接。
  - **第 3 頁 (跨頁右面 / 科學研究篇)**：AST Active Healer 答案盲修復機制、固定 Tier 規則、旺宏決賽 720 獨立測試、研究邊界與科學反思。
  - **第 4 頁 (封底 / 跨域實踐篇)**：高中足球聯賽長期投入（主力背號 42）、FBref 數據分析、TOEIC 945 金色證書與 GEPT 中高級合格證書、作品線上入口。

---

## ▍在 Claude Design 中使用的推薦方式

1. **直接匯入檔案**：
   - 將解壓縮後的資料夾上傳至 Claude Project 或對話中，並搭配 `prompt_for_claude.md` 指示 Claude 進行修改。
2. **單檔極速預覽 (Claude Artifacts)**：
   - 打開 `index_standalone.html`，全選並複製原始碼貼入 Claude，即可在右側 Artifact 視窗中即時互動與所見即所得渲染！
"""
(BUNDLE_DIR / "README.md").write_text(readme_text, encoding="utf-8")

prompt_text = """# Claude Design 專用設計微調指示提示詞 (Prompt)

將本檔案內容複製後，在 Claude 對話中貼上，即可讓 Claude 理解四面小冊的排版架構與設計約束：

```markdown
你好！這是我準備參加大學資訊工程學系「特殊選才」面試使用的四面小冊（A3 橫向雙面列印、對折成 A4 的四面折頁履歷）：

1. 請幫我基於現有的 HTML / CSS 架構進行設計檢視與優化。
2. 核心規範：
   - 保持嚴謹、穩重、高質感的 Oxford Navy & Steel Slate 學術風格。
   - 嚴格遵守真實客觀原則，不使用過度浮誇的行銷形容詞。
   - 每頁物理尺寸嚴格鎖定為 A4（210mm × 297mm），確保 A3 雙面列印對折時版面不溢出、無大片空白。
   - 保持 P2（系統工程）與 P3（科學研究）的跨頁雙線連動性。
3. 四頁對應關係：
   - A3 外側面：左邊為第 4 頁（封底·跨域實踐），右邊為第 1 頁（封面·個人總覽）
   - A3 內側面：左邊為第 2 頁（系統工程），右邊為第 3 頁（科學研究）
```
"""
(BUNDLE_DIR / "prompt_for_claude.md").write_text(prompt_text, encoding="utf-8")

# 10. Create ZIP package
zip_out_root = ROOT / "output" / "葉陽甫_面試四面小冊_典雅學術版_Claude_Design設計包.zip"
zip_out_pdf = ROOT / "output" / "pdf" / "葉陽甫_面試四面小冊_典雅學術版_Claude_Design設計包.zip"

with zipfile.ZipFile(zip_out_root, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(BUNDLE_DIR):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(BUNDLE_DIR)
            zipf.write(file_path, str(arcname))

shutil.copy2(zip_out_root, zip_out_pdf)

print(f"Created ZIP bundle successfully at:")
print(f"  1. {zip_out_root} ({zip_out_root.stat().st_size} bytes)")
print(f"  2. {zip_out_pdf} ({zip_out_pdf.stat().st_size} bytes)")

print("\nZIP File Structure:")
with zipfile.ZipFile(zip_out_root, "r") as z:
    for name in sorted(z.namelist()):
        print(f"  - {name}")

# Clean up temp bundle dir
shutil.rmtree(BUNDLE_DIR)
print("\nTemporary folder cleaned up.")
