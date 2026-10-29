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

prompt_text = r"""# Claude Design 專用：葉陽甫特殊選才面試四面小冊（典雅學術版）設計與編輯 Prompt

請直接複製以下整段 Prompt，貼給 Claude（可在對話中直接附帶本專案的 `index_standalone.html` 或將整個解壓資料夾上傳至 Claude Project）：

---

```markdown
# 任務：審閱、排版優化與編輯《葉陽甫 特殊選才面試四面小冊（典雅學術版）》

你好！這是我準備參加大學資訊工程學系「特殊選才」教授實體面試時，發給每位口試教授親手翻閱的「四面折頁履歷小冊」（由一張 A3 橫向雙面彩色印刷，對折成 4 頁 A4）。

請基於我提供的 HTML／CSS 原始碼與文字內容，以最高水準的數位設計師與學術排版專家標準，協助我進行審閱、排版微調與視覺設計提升。

---

## ▍核心設計規範 (Design System)

1. **色彩系統 (Academic Oxford & Steel Slate)**：
   - **主色 (Oxford Navy)**：`#0f2942`（標題、大獎抬頭、頂部膠囊、關鍵徽章、底線）
   - **深藍次強調色 (Academic Blue)**：`#1e3a8a`（關鍵排名、重要連結、數理亮點）
   - **琥珀金強調色 (Achievement Gold)**：`#b45309`（全國金獎、全國第一名、多益金色證書）
   - **石墨深灰 (Body Slate)**：`#1e293b` / `#334155`（內文主要文字）
   - **鋼鐵冷灰 (Secondary Slate)**：`#475569` / `#64748b`（說明文字、次級標籤、頁尾）
   - **背景淺灰 (Card Surface)**：`#f8fafc` / `#f1f5f9`（區塊背景、引言卡片）
   - **邊框灰 (Border Slate)**：`#cbd5e1` / `#e2e8f0`（微細分隔線、照片外框）

2. **版面規格與折頁結構**：
   - **物理尺寸**：每頁嚴格為標準 A4（`210mm × 297mm`）。整體為一張 A3（`420mm × 297mm`）雙面印刷對折。
   - **A3 外側跨頁 (Sheet 1)**：左面為**第 4 頁（封底·跨域實踐）**，右面為**第 1 頁（封面·個人總覽）**。中折線位於 $x = 210\,\text{mm}$。
   - **A3 內側跨頁 (Sheet 2)**：翻開後左右並列，左面為**第 2 頁（跨頁左面·系統工程篇）**，右面為**第 3 頁（跨頁右面·科學研究篇）**，兩頁底部設有跨頁銜接導引（`⚡ 銜接研究 ➔` 與 `承接左頁出題系統問題 ◄`）。
   - **邊界保護**：內頁留白約 10mm~13mm，所有卡片與元件嚴格鎖定無溢出。

3. **文字與排版原則**：
   - **真實客觀**：不誇張渲染，避免典型 AI 廣告文案（如「突破極限」、「頂尖」、「致命」）。
   - **中文排版流暢**：一般段落自然齊頭折行，不可每逢逗號強制 `<br>`，避免階梯式短句。
   - **專有名詞與數字完整**：排名、百分比、成績（如 `TOEIC 945`、`前 3.7%`、`84.5 分`、`國男甲級聯賽`）不可拆裂到不同行。

---

## ▍四頁完整內容架構 (Content Structure)

### 【第 1 頁：封面｜個人總覽與高中成果】
- **頁首導航**：國立花蓮高級中學 普通科 ｜ 特殊選才面試資料 · 個人總覽
- **個人核心**：葉陽甫 ｜ 普通科 ｜ 特殊選才備審核心總覽
- **定位聲明**：資訊工程 · 數學自適應系統實作 · 程式生成局部修復研究 · 足球運動競技
- **4 大關鍵徽章**：
  1. 🥇 育秀盃創意獎【全國金獎】(AI類 · 10萬元)
  2. 🏅 旺宏科學獎【全國決賽20強】(資訊領域僅4件)
  3. ⚽ 全國五人制足球聯賽【全國第 5 名】(校隊主力)
  4. 📜 TOEIC 945 (金色證書) ｜ APCS 觀念 5 級分
- **左欄 1：學業與基礎能力**
  - 總體表現：4學期班排前五，學業平均 84.2（年排 24/320 · 前 8%）
  - 數理資工：資訊科 前 6% ｜ 數學科 前 6% ｜ 化學科 前 4% ｜ 地科 前 2%
  - 校內選修：Arduino 程式設計 94 分（第 2 名）、Python 90 分（第 4 名）
  - 數理競賽：JHMC 國中數學競賽 團體一等獎／個人優良獎 ｜ 更生盃 銀牌
- **左欄 2：外語溝通能力**
  - TOEIC 945 分（金色證書）：聽力 485 ／ 閱讀 460
  - 全民英檢（GEPT）中高級：聽、說、讀、寫四項全數通過
  - 在校英文成績：高一二平均 91 分（前 4%），高二下 96 分（年排第 7 · 前 2%）
  - 語文競賽成果：花蓮縣英文作文高中組 甲等 ｜ 校內作文 第 2 名 ｜ 校內英語演說 初賽第 1 名、全校複賽第 4 名
  - 國中語文延續：國中英文作文 優等 ｜ 英語讀者劇場 特優
- **左欄 3：足球競技與長期投入**
  - 全國五人制足球聯賽：114 學年 全國第 5 名 ｜ 113 學年 全國第 6 名（連續兩年符合教育部運動績優甄試資格）
  - 全國青年盃公開組：全國第 5 名
  - 花蓮縣運足球：2025 社會男子組 亞軍 ｜ 2022 國中男子組 冠軍
  - 球隊經歷：花蓮高中五人制校隊主力球員（背號 42 號）
  - 體能表現：校運 800m 第 2 名 ｜ 體育成績 84.5 分（年排 13/320 · 前 4%）
  - 國中運動延續：國中足球聯賽 全國乙組季軍 ｜ 花崗國中男足隊長（參與全國甲級聯賽）
- **右欄 1：代表性科研成果**
  - 1. 第 25 屆 旺宏科學獎【全國決賽 20 強】：全領域 846 件作品評選，資訊領域全國僅 4 件入選決賽；研究核心：小型語言模型之 AST 程式碼局部錯誤修復研究。
  - 2. 第 23 屆 育秀盃創意獎【全國金獎】：高中職 AI 應用類金獎（獎金 10 萬元），作品為 AI 自適應輔助學習系統。
  - 3. 2026 神通 AI 數位學院扶輪盃【全國冠軍】：全國高中 AI 應用競賽 第一名。
  - 4. 第 66 屆 東區科展【電腦與資訊學科優等】：高級中等學校分區科展（未晉級全國科展）。
- **右欄 2：核心技術架構與專案**
  - AST Active Healer 程式修復機制：以固定規則修正 AI 產生的程式中部分能明確判斷的錯誤，並透過測試確認哪些情況能修復、哪些無法修復。
  - AI 自適應輔助學習系統：由 AI 建立可重複使用的 Python 出題程式，驗證後產生變化題與答案，並結合數學判題、AI 助教及學習紀錄。系統已在花蓮高商兩個班級使用，部分單元提供規則式自適應複習。
  - 專案入口：線上 Demo 展示頁（mathb.math-adaptive.org/review-demo） ｜ 專案 GitHub（github.com/yyfsunnyboy/Mathproject_tvet_mathB）。
- **右欄 3：程式實作與工程探究**
  - APCS 大學程式先修檢測：觀念 92.5 分（5 級分 · 前 3.7%） ｜ 實作 135 分（2 級分）
  - IEYI 世界青少年發明展：2023 臺灣選拔賽【銀獎】
  - 資訊學科能力競賽：校內初賽【佳作】
  - 學習歷程課程成果：Arduino 程式設計【優等】
  - 跨領域數據分析實作：使用 Python 抓取 FBref 足球數據進行分析練習
  - 東部物理 IYPT 科學營：實驗報告【第 3 名】
  - 第 65 屆校內科展（工程學科(二)）：【優勝】（未晉級東區）

---

### 【第 2 頁：跨頁左面｜系統工程篇】
- **主標題**：02 / 系統工程篇 ｜ 跨頁主線 (上) · 系統落地
- **大字主軸**：AI 自適應輔助學習系統 —— 從數學課堂的實際需求出發，逐步開發並投入教學使用的系統。
- **頂部雙獎**：🏆 神通扶輪盃 全國第一名 ｜ 🥇 育秀盃創意獎 全國金獎
- **4 大課堂驗證指標**：
  - 2 個班級（課堂實際使用班級）
  - 50 名（正式課堂學生帳號）
  - 1,224 次（系統累積作答筆數）
  - 67%（學生平均答對率，數據截至 2026/10/04）
- **左欄 1：開發起點與課堂需求**
  - 開發背景：我的父親在花蓮高商教授數學。開發初期，我先了解他在實際教學中遇到的問題，整理出四項需求：
  - 01｜教材整理費時：數學教材包含公式、圖形與大量例題，逐題輸入系統相當費時。
  - 02｜固定題庫難以反覆練習：同一題目做過後容易記住答案，需要能持續產生變化題的方式。
  - 03｜學生的學習程度不同：同班學生可能卡在不同數學概念，需要依作答情況安排補強。
  - 04｜數學作答不只是輸入文字：學生需要輸入公式、手寫計算與作圖，普通文字表單並不適合。
- **左欄 2：三項主要功能**
  - 1. 教材整理與匯入：將 Word、PDF 數學教材整理成章節、技能與例題，並保留題目來源。
  - 2. AI 建立出題程式：先讓 AI 產生 Python 出題程式，驗證通過後，再由程式反覆產生不同數值的同類型題目與答案。
  - 3. 學生練習與回饋：學生可以在系統上解題，程式負責判斷答案，AI 助教提供提示，作答紀錄供學生與老師查看。
- **左欄 3：規則式自適應複習 ｜ 根據作答紀錄安排補強**
  - 流程：學生作答 → 更新技能能力值與錯誤紀錄 → 判斷卡點 → 前置技能練習 → 返回原進度
  - 說明：系統記錄每道題對應的數學技能、作答結果與時間，藉此整理學生的學習狀態。當技能表現符合預設卡點條件時，安排前置技能練習；達到補救條件後，再返回原本進度。目前僅在部分單元實作，跨單元擴充與學習成效仍待驗證。
- **右欄 1：真實正式系統截圖**
  - 學生線上解題、即時數理判題與 AI 助教引導（mathb.math-adaptive.org）
- **右欄 2：雙賽獲獎合影**
  - 神通扶輪盃 全國第一名合影 ｜ 育秀盃創意獎 全國金獎合影
- **右欄 3：葉陽甫 ｜ 個人主要負責的系統工程**
  - 01｜教材匯入與結構化整理：將 Word／PDF 教材整理為章節、技能與題目資料。
  - 02｜程式即內容（Code-as-Content）：建立 AI 產生 Python 出題程式及驗證流程，支援反覆變題。
  - 03｜多模態數學作答介面：整合公式輸入、手寫畫布、作圖互動與 AI 助教提示。
  - 04｜數學判題與程式驗證：使用 SymPy 驗證數學答案，並建立程式測試流程。
  - 05｜正式部署與維護：負責資料庫、家用主機部署及課堂問題排除。
- **下方全幅：課堂落地工程實作與問題修正**
  - 1. 題目規格與回歸測試：課堂曾遇到題目參數缺漏、變題超出合理範圍等問題，因此加入出題程式測試，減少相同錯誤再次出現。
  - 2. 數理答案等價判定：使用 Python 與 SymPy 判斷分數、根號、小數及區間等答案是否等價，減少直接比對文字造成的誤判。
  - 3. 書房主機與外部連線：正式主機設於家中書房，透過 HiNet 與 Cloudflare Tunnel 對外提供服務，讓學校師生能連線使用。
- **底部跨頁導引**：⚡ 銜接研究：從出題系統的成本與錯誤，延伸為程式碼修復研究（接續右頁研究 ➔）

---

### 【第 3 頁：跨頁右面｜科學研究篇】
- **主標題**：03 / 科學研究篇 ｜ 跨頁主線 (下) · 深化科研
- **大字主軸**：AST Active Healer ｜ AI 生成程式碼的局部錯誤修復研究 —— 研究哪些程式錯誤能用固定規則修正，以及這種方法的限制。
- **頂部雙獎**：🏅 第25屆旺宏科學獎 全國決賽20強 ｜ 🏅 第66屆東區科展 電腦與資訊學科優等
- **頂部引言**：🔬 研究問題意識與出發點 —— 本地小模型產生 Python 程式時，經常出現格式、函式介面或局部結構錯誤。我嘗試設計固定規則修復器，只修改能明確判定的部分，再透過測試確認是否真的修好。（AST 抽象語法樹：用來分析與檢查程式結構的樹狀資料表示法）。
- **左欄：三步驟修復機制（答案盲與固定規則）**
  - 核心原則：能確定才修 · 不能確定不修改
  - 機制架構圖（healer_blind_repair_rules.png）
  - 三大步驟：
    - ① 檢查原始失敗程式：不讀取正確答案，逐筆檢查失敗案例。
    - ② 依固定規則修改：只有修法明確時才修改局部程式；無法確定時不修改。
    - ③ 重新測試：使用相同測試，確認程式是否由失敗轉為通過。
- **右欄：正式測試與模型表現**
  - 測試規格：正式保留測試 ｜ 720 筆
  - 救援實驗圖表（healer_chart_user.png）
  - 觀察說明：測試三種模型（Qwen 3.5 4B、Qwen 3.5 9B、Gemini 3.5 Flash）在四種 Prompt 下的表現；342 筆失敗中，42 筆觸發修復規則，9 筆安全救回（救回率 2.63%）。
- **4 大嚴謹數據與公式**：
  - Math16 資料集：4 題用於規則開發，其餘 12 題保留為正式獨立測試
  - 12 題 × 3 種模型 × 4 種 Prompt × 5 組隨機種子 ＝ 720 筆正式測試
  - 720 筆（保留正式測試單元）
  - 342 筆（原始生成失敗案例）
  - 42 筆（觸發修復規則修改）
  - 9 筆（失敗轉為通過，救回率 2.63%）
  - 備註：救回率 2.63%（9 ÷ 342）為原始失敗案例的救回比例，非整體生成成功率；42 筆實際修改案例中轉為通過的比例為 21.4%（9 ÷ 42）。
- **左下：研究歷程（從初版指標到決賽重新驗證）**
  - 初版研究使用自訂 MCRI 指標評估程式與數學品質，最高階段的整體平均分數為 97.41。這是綜合評估分數，並非程式通過率。東區科展未晉級全國後，我重新檢視初版評估方式的限制。
  - 進入旺宏科學獎決賽準備階段，我將修復規則開發與正式測試資料分開，重新驗證修復器真正能救回多少失敗案例。
  - 榮譽：✦ 旺宏科學獎全領域 846 件作品報名，資訊領域僅 4 件入選決賽 20 強
- **右下：研究結果與修復機制的真實限制**
  - 正式測試中，342 筆原始失敗案例有 9 筆經修復後通過，成功案例主要集中於格式、介面及局部資料處理問題。涉及題意理解或核心演算法的錯誤，固定規則無法直接解決。
  - 這次重新驗證讓我更清楚修復器的適用範圍，也看見初版綜合指標無法直接代表實際修復效果。
  - 榮譽：✦ 第 66 屆東區科展 電腦與資訊學科【優等】
- **下方全幅：錯誤類型分類與固定規則處理邊界**
  - 1｜修復後通過 (9 筆)：輸出格式與介面：6 筆；執行與資料流：2 筆；語法解析：1 筆。
  - 2｜修改後仍未通過 (33 筆)：修復器曾依固定規則修改，但重新測試後仍未通過。
  - 3｜未進行修改 (300 筆)：未符合可介入的固定修復規則，保留原始程式，不進行無明確依據的修改。

---

### 【第 4 頁：封底｜跨域實踐篇】
- **主標題**：04 / 跨域實踐篇 ｜ 多元發展 · 自律與體能
- **大字主軸**：足球競技與英文能力 —— 高中五人制校隊聯賽競技 ｜ 語言檢定、在校表現與實際工具運用
- **頂部三標籤**：⚽ 全國五人制聯賽 全國第 5 名 ｜ 🌟 TOEIC 945 金色 ｜ GEPT 中高級
- **上半部：足球競技 ｜ 從國中校隊到高中全國聯賽**
  - 身份標記：背號 42 號 · 花蓮高中校隊
  - 4 大賽事戰績：
    - 全國第 5 名（114學年度五人制聯賽 · 高二）
    - 全國第 6 名（113學年度五人制聯賽 · 高一）
    - 公開組第 5 名（全國青年盃11人制公開組）
    - 社會組亞軍（2025 花蓮縣運11人制社會組）
  - 足球成長歷程（兩段流暢平實敘事）：
    > 我從幼兒園開始踢足球。國小參加全國學童盃獲第三名；國二在全國乙組聯賽獲第三名。國三擔任花崗國中男子足球隊隊長，並參加全國國男甲級聯賽。這些年我一直跟著球隊訓練，逐步接觸不同層級的正式賽事。
    >
    > 升上花蓮高中後，我繼續代表五人制足球校隊出賽。113 學年度，球隊在全國 63 支參賽隊伍中獲第六名；114 學年度，在 57 支隊伍中獲第五名，決賽以 5:3 擊敗臺中惠文高中。高中這兩年，我同時安排課業、資訊專案與校隊訓練，持續參與全國聯賽。
  - 灰底重點框：◆ 連續兩年符合教育部運動績優甄試資格 ｜ 113 學年全國第 6 名 ｜ 114 學年全國第 5 名
  - 足球數據分析實作｜FBref × Python：因為對足球與程式設計都有興趣，我使用 Python 整理 FBref 公開數據，嘗試分析球員及球隊的比賽表現，作為跨領域程式實作練習。
  - 右側媒體：
    - 114學年度全國中等學校五人制足球聯賽決賽現場：花蓮高中代表隊合影（紅圈處為葉陽甫，受獎代表左後方）
    - ▶ 114學年決賽直播精彩畫面 ↗（附官方直播 QR Code）
    - ▶ 足球數據分析 GitHub 專案 ↗（附專案原始碼 QR Code）
- **中部分隔線**：細緻灰色邊界線
- **下半部：英文能力 ｜ 語言檢定、在校表現與實際工具運用**
  - 標籤：CEFR B2+ ｜ 在校英文平均 91 分
  - 4 大英語指標：
    - 945 分（TOEIC 多益金色證書）
    - 全數通過（GEPT 中高級聽說讀寫）
    - 485 / 460（多益聽力 / 閱讀）
    - 花蓮縣英文作文甲等（高中組作文競賽）
  - 左欄 A｜語言檢定成績：
    - TOEIC 945 分（金色證書：聽力 485、閱讀 460）。
    - 全民英檢（GEPT）中高級聽、說、讀、寫四項全數通過（聽力 111、閱讀 87、口說 80、寫作 80）。
  - 左欄 B｜英文競賽與在校表現：
    - 花蓮縣英文作文競賽高中 A 組甲等、校內英文作文二年級第二名。
    - 校內英語演說一年級初賽第一名、全年級複賽第四名。
    - 高一至高二英文平均 91 分（校排前 4%），高二下 96 分、年級第七名（前 2%）。
  - 左欄 C｜英文的實際使用：
    > 在程式學習時，我會查閱英文技術資料，了解新工具的使用方法；平常也會觀看國外足球分析影片、閱讀英文足球資訊。英文是我學習資訊與足球時持續使用的工具。
  - 右側雙證書照片：TOEIC 945 金色證書 ＆ GEPT 中高級合格證書（工整垂直堆疊）
- **頁尾數位作品入口列**：
  - AI 自適應輔助學習系統 Demo ↗（附 QR Code）
  - GitHub 系統程式碼 ↗（附 QR Code）
  - 葉陽甫 ｜ 國立花蓮高級中學 誠摯感謝各位教授審閱與指導

---

## ▍請執行的具體工作

1. 請檢視所附 HTML / CSS 架構，在保持上述完整文字與數據 100% 不變的前提下，協助微調 CSS 視覺細節（如邊框圓角、字級微調、陰影、間距）。
2. 若使用 Claude Artifacts 渲染，請確保所有照片與 QR Code 以 Base64 或可讀方式正確顯示，並確保 4 頁各自在 A4 比例下無溢出。
3. 提供你對整體版面、教授閱讀動線（Eye Tracking）與學術質感的優化建議。
```
"""
(BUNDLE_DIR / "prompt_for_claude.md").write_text(prompt_text, encoding="utf-8")

# 10. Copy unzipped bundle to output/claude_design_bundle (Keep for direct user access)
unpacked_dir = ROOT / "output" / "claude_design_bundle"
if unpacked_dir.exists():
    shutil.rmtree(unpacked_dir)
shutil.copytree(BUNDLE_DIR, unpacked_dir)
print(f"Unpacked bundle preserved at: {unpacked_dir}")

# 11. Create ZIP package
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

# Clean up temp bundle dir
shutil.rmtree(BUNDLE_DIR)
print("\nTemporary folder cleaned up.")

