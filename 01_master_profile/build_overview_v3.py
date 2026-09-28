import base64
import os
import asyncio
from playwright.async_api import async_playwright
import fitz

WORKSPACE = r"D:\Python\yangfu-application\01_master_profile"
PHOTO_PATH = r"D:\Python\yangfu-application\00_source_materials\照片\YEH YANG FU.jpg"
HTML_PATH = os.path.join(WORKSPACE, "09_first_page_overview.html")
PDF_PATH = os.path.join(WORKSPACE, "09_first_page_overview.pdf")
PNG_PATH = os.path.join(WORKSPACE, "09_first_page_overview.png")

with open(PHOTO_PATH, "rb") as f:
    photo_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>葉陽甫｜高中學習與成果總覽</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;800;900&family=Outfit:wght@500;600;700;800&display=swap');

  @page {{
    size: A4 portrait;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  html, body {{
    margin: 0;
    padding: 0;
    background-color: #ffffff;
    font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    -webkit-font-smoothing: antialiased;
  }}

  /* A4 Canvas: 210mm x 297mm，保留 12-14mm 白邊留白 */
  .a4-page {{
    width: 210mm;
    height: 297mm;
    box-sizing: border-box;
    margin: 0 auto;
    background: #ffffff;
    padding: 10.5mm 12mm 9.5mm 12mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  @media print {{
    html, body {{
      background: none;
    }}
    .a4-page {{
      margin: 0;
      width: 210mm;
      height: 297mm;
      page-break-after: avoid;
      page-break-inside: avoid;
    }}
  }}

  /* ----------------------------------------------------
     1. TOP META HEADER (與讀書計畫一致的學術 Navigation)
  ---------------------------------------------------- */
  .top-meta-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 9.5pt;
    color: #64748b;
    letter-spacing: 0.5px;
    padding-bottom: 2.5px;
    border-bottom: 1px solid #cbd5e1;
    margin-bottom: 7px;
  }}

  .top-meta-left {{
    display: flex;
    gap: 12px;
    font-weight: 500;
  }}

  .top-meta-capsule {{
    background-color: #0f294a;
    color: #ffffff;
    font-size: 9pt;
    font-weight: 700;
    padding: 2.5px 9px;
    border-radius: 3px;
    letter-spacing: 0.4px;
  }}

  /* Header Main Area (照片 + 姓名學校 + 一句話定位 + 4大核心標籤) */
  .header-main {{
    display: flex;
    gap: 14px;
    align-items: center;
    margin-bottom: 5px;
  }}

  .header-photo {{
    width: 24mm;
    height: 30mm;
    object-fit: cover;
    border-radius: 3px;
    border: 1px solid #cbd5e1;
    flex-shrink: 0;
  }}

  .header-info {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}

  .header-title-row {{
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 3.5px;
  }}

  .name-text {{
    font-size: 22.5pt;
    font-weight: 900;
    color: #0f294a;
    letter-spacing: 0.5px;
    line-height: 1.1;
  }}

  .school-text {{
    font-size: 13pt;
    font-weight: 700;
    color: #334155;
  }}

  .domain-text {{
    font-size: 11pt;
    font-weight: 700;
    color: #0d9488;
    margin-left: auto;
    letter-spacing: 0.2px;
  }}

  .positioning-statement {{
    font-size: 11.5pt;
    color: #0f294a;
    font-weight: 600;
    margin-bottom: 5px;
    line-height: 1.25;
    background-color: #f8fafc;
    padding: 3.5px 8px;
    border-left: 3.5px solid #0f294a;
    border-radius: 0 3px 3px 0;
  }}

  /* 四大核心標籤（圖標/色塊 Badge 形式並排） */
  .badge-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 8px;
  }}

  .badge-item {{
    display: flex;
    align-items: center;
    gap: 5px;
    background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 3px;
    padding: 2.5px 7px;
    font-size: 10.5pt;
    color: #0f294a;
    font-weight: 600;
    white-space: nowrap;
  }}

  .badge-star {{
    color: #b45309; /* 科技金/琥珀 */
    font-size: 10pt;
  }}

  .badge-highlight {{
    color: #b45309;
    font-weight: 800;
  }}

  .header-divider {{
    height: 1.5px;
    background-color: #0f294a;
    width: 100%;
    margin-top: 4px;
    margin-bottom: 8px;
  }}

  /* ----------------------------------------------------
     2. TWO-COLUMN LAYOUT (左欄 43% ｜ 右欄 55%)
  ---------------------------------------------------- */
  .columns-container {{
    display: grid;
    grid-template-columns: 43% 54.5%;
    gap: 2.5%;
    flex: 1;
  }}

  .col-left {{
    display: flex;
    flex-direction: column;
    gap: 14px;
    border-right: 1px solid #e2e8f0;
    padding-right: 12px;
  }}

  .col-right {{
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding-left: 2px;
  }}

  /* ----------------------------------------------------
     3. SECTION HEADINGS (分類標題 13.5 - 14 pt 深藍)
  ---------------------------------------------------- */
  .section-block {{
    display: flex;
    flex-direction: column;
  }}

  .sec-heading {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13.5pt;
    font-weight: 800;
    color: #0f294a;
    padding-bottom: 3px;
    border-bottom: 1.5px solid #0f294a;
    margin-bottom: 8px;
  }}

  .sec-heading-symbol {{
    color: #0d9488;
    font-size: 11pt;
  }}

  /* ----------------------------------------------------
     4. CONTENT ROWS (正文 >= 12 pt，行距 1.44)
  ---------------------------------------------------- */
  .item-list {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 5.5px;
  }}

  .item-row {{
    font-size: 12pt;
    line-height: 1.44;
    color: #334155;
    letter-spacing: -0.2px;
  }}

  .item-row strong {{
    color: #0f294a;
    font-weight: 800;
  }}

  .item-row .hl-gold {{
    color: #b45309;
    font-weight: 800;
  }}

  .item-row .hl-teal {{
    color: #0d9488;
    font-weight: 800;
  }}

  .bullet {{
    color: #0f294a;
    font-size: 11pt;
    margin-right: 2px;
  }}

  .sep {{
    color: #94a3b8;
    margin: 0 4px;
    font-weight: 400;
  }}

  /* 右欄四大代表成果項目 (固定結構) */
  .national-award-item {{
    display: flex;
    flex-direction: column;
    margin-bottom: 6px;
  }}

  .award-title-row {{
    font-size: 12.5pt;
    font-weight: 800;
    color: #0f294a;
    line-height: 1.35;
    letter-spacing: -0.15px;
  }}

  .award-title-row .award-crown {{
    color: #b45309;
    font-weight: 800;
  }}

  .award-desc-row {{
    font-size: 12pt;
    line-height: 1.42;
    color: #475569;
    padding-left: 12px;
    letter-spacing: -0.2px;
  }}

  .tech-project-block {{
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 5.5px;
  }}

  .tech-title {{
    font-size: 12pt;
    font-weight: 800;
    color: #0f294a;
    line-height: 1.35;
    letter-spacing: -0.15px;
  }}

  .tech-desc {{
    font-size: 12pt;
    line-height: 1.44;
    color: #475569;
    text-align: justify;
    padding-left: 10px;
    letter-spacing: -0.2px;
  }}

  /* ----------------------------------------------------
     5. FOOTER (頁尾 9.5 pt 讀書計畫樣式)
  ---------------------------------------------------- */
  .bottom-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #cbd5e1;
    padding-top: 3px;
    font-size: 9.5pt;
    color: #64748b;
    font-weight: 500;
  }}

  .footer-left {{
    letter-spacing: 0.3px;
  }}

  .footer-right {{
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    color: #475569;
  }}
</style>
</head>
<body>

<div class="a4-page">
  <!-- Content Top Area -->
  <div>
    <!-- 頁首 Meta Header (9.5 pt 讀書計畫風格) -->
    <div class="top-meta-header">
      <div class="top-meta-left">
        <span>個人總覽</span>
        <span style="font-weight: 700; color: #0f294a;">PAGE 00</span>
        <span>高中學習與成果</span>
      </div>
      <div class="top-meta-capsule">
        特殊選才備審核心導航頁
      </div>
    </div>

    <!-- 頂部 HEADER (照片 + 姓名學校 + 一句話定位 + 4大核心標籤) -->
    <div class="header-main">
      <img class="header-photo" src="data:image/jpeg;base64,{photo_b64}" alt="葉陽甫">
      <div class="header-info">
        <div class="header-title-row">
          <span class="name-text">葉陽甫</span>
          <span class="sep" style="font-size: 14pt; color: #cbd5e1;">｜</span>
          <span class="school-text">國立花蓮高級中學</span>
          <span class="domain-text">資訊工程 × AI 教育科技 × 跨域競技</span>
        </div>
        <div class="positioning-statement">
          專注於 LLM 程式生成確定性修復與自適應學習架構的科研自律者
        </div>
        <div class="badge-grid">
          <div class="badge-item">
            <span class="badge-star">★</span>
            <span>育秀盃<span class="badge-highlight">全國首獎</span>（AI應用類金獎）</span>
          </div>
          <div class="badge-item">
            <span class="badge-star">★</span>
            <span>旺宏科學獎 <span class="badge-highlight">全國決賽20強</span>（資工僅4件）</span>
          </div>
          <div class="badge-item">
            <span class="badge-star">★</span>
            <span>神通 AI 扶輪盃 <span class="badge-highlight">全國冠軍</span></span>
          </div>
          <div class="badge-item">
            <span class="badge-star">★</span>
            <span><span class="badge-highlight">TOEIC 945</span> 金色證書 / <span class="badge-highlight">APCS 觀念 5 級分</span></span>
          </div>
        </div>
      </div>
    </div>

    <div class="header-divider"></div>
  </div>

  <!-- 雙欄版型 (左欄 43% ｜ 右欄 55%) -->
  <div class="columns-container">
    
    <!-- ==================== 左側欄：核心素養與自律底質（35% -> 43%） ==================== -->
    <div class="col-left">
      
      <!-- 1. 學業與基礎能力 -->
      <div class="section-block">
        <div class="sec-heading">
          <span class="sec-heading-symbol">◆</span>
          <span>學業與基礎能力</span>
        </div>
        <div class="item-list">
          <div class="item-row">
            <span class="bullet">•</span><strong>總體表現</strong>：高一高二 4 學期班排前五<br>
            <span style="padding-left: 10px;">平均 <strong>84.2</strong>（年排 24/320・<span class="hl-teal">前 8%</span>）</span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>數理資工</strong>：資訊 <span class="hl-teal">前 6%</span>｜數學 <span class="hl-teal">前 6%</span><br>
            <span style="padding-left: 10px;">化學 <span class="hl-teal">前 4%</span>｜地科 <span class="hl-teal">前 2%</span></span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>校內選修</strong>：Arduino <strong>94 分</strong>（第 2 名）<br>
            <span style="padding-left: 10px;">Python <strong>90 分</strong>（第 4 名）</span>
          </div>
        </div>
      </div>

      <!-- 2. 外語溝通實力 -->
      <div class="section-block">
        <div class="sec-heading">
          <span class="sec-heading-symbol">◆</span>
          <span>外語溝通實力</span>
        </div>
        <div class="item-list">
          <div class="item-row">
            <span class="bullet">•</span><strong>TOEIC 945 分</strong>（<span class="hl-gold">金色證書</span>）<br>
            <span style="padding-left: 10px;">聽力 485 / 閱讀 460</span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>全民英檢（GEPT）中高級</strong><br>
            <span style="padding-left: 10px;">聽說讀寫四項全數合格</span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>加權平均</strong>：高一二英文 <strong>91</strong>（<span class="hl-teal">前 4%</span>）<br>
            <span style="padding-left: 10px;">高二下英文 <strong>96</strong>（年排第 7・<span class="hl-teal">前 2%</span>）</span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>競賽表現</strong>：英語演說 初賽 1・複賽 4<br>
            <span style="padding-left: 10px;">校內英文作文 第 2 名</span>
          </div>
        </div>
      </div>

      <!-- 3. 競技運動與自律特質 -->
      <div class="section-block">
        <div class="sec-heading">
          <span class="sec-heading-symbol">◆</span>
          <span>競技運動與自律特質</span>
        </div>
        <div class="item-list">
          <div class="item-row">
            <span class="bullet">•</span><strong>全國五人制足球聯賽</strong>：<br>
            <span style="padding-left: 10px;">高二 <span class="hl-gold">全國第 5 名</span>｜高一 <span class="hl-gold">全國第 6 名</span></span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>全國青年盃公開組</strong>：<span class="hl-gold">全國第 5 名</span><br>
            <span style="padding-left: 10px;">花蓮縣運足球 <strong>冠軍</strong></span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>體能與意志力</strong>：高中足球校隊主力<br>
            <span style="padding-left: 10px;">校運 800m 第 2 名｜9km 越野完跑證明</span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>特質印證</strong>：長期處於高壓賽事訓練，仍維持校內頂尖課業與科研進度
          </div>
        </div>
      </div>

    </div>

    <!-- ==================== 右側欄：AI 科研、工程與代表性成果（65% -> 55%） ==================== -->
    <div class="col-right">
      
      <!-- 1. 代表性科研大獎（National Honors） -->
      <div class="section-block">
        <div class="sec-heading">
          <span class="sec-heading-symbol">◆</span>
          <span>代表性科研大獎（National Honors）</span>
        </div>
        
        <div class="national-award-item">
          <div class="award-title-row">
            1. 第 23 屆 育秀盃創意獎【<span class="award-crown">全國首獎</span>】
          </div>
          <div class="award-desc-row">
            • 榮獲高中職 AI 應用類金獎（獎金 10 萬元）<br>
            • 作品：AI 自適應學習系統架構與實作
          </div>
        </div>

        <div class="national-award-item">
          <div class="award-title-row">
            2. 2026 神通 AI 數位學院扶輪盃【<span class="award-crown">全國冠軍</span>】
          </div>
          <div class="award-desc-row">
            • 全國高中 AI 應用競賽 第一名
          </div>
        </div>

        <div class="national-award-item">
          <div class="award-title-row">
            3. 第 25 屆 旺宏科學獎【<span class="award-crown">全國決賽 20 強</span>】
          </div>
          <div class="award-desc-row">
            • 全領域 846 件作品評選<br>
            <span style="padding-left: 10px;">資工領域全國僅 4 件入圍決賽</span><br>
            • 研究核心：小型語言模型（SLM）之 AST 確定性修復機制
          </div>
        </div>

        <div class="national-award-item">
          <div class="award-title-row">
            4. 第 66 屆 東區科展【<span class="hl-teal">優等第 2 名</span>】
          </div>
          <div class="award-desc-row">
            • 電腦與資訊學科（代表晉級全國評選階段）
          </div>
        </div>
      </div>

      <!-- 2. 核心技術架構與專案 -->
      <div class="section-block">
        <div class="sec-heading">
          <span class="sec-heading-symbol">◆</span>
          <span>核心技術架構與專案</span>
        </div>
        
        <div class="tech-project-block">
          <div class="tech-title">• AST Healer 確定性修復機制：</div>
          <div class="tech-desc">
            針對程式碼生成任務，結合抽象語法樹（AST）進行語法解析與邏輯回饋自癒，有效提升小型模型之代碼可用率。
          </div>
        </div>

        <div class="tech-project-block">
          <div class="tech-title">• AI 自適應學習平台：</div>
          <div class="tech-desc">
            運用大型語言模型結合動態診斷算法，依據學習者即時回饋生成最佳化學習路徑。
          </div>
        </div>
      </div>

      <!-- 3. 程式實作與工程探究 -->
      <div class="section-block">
        <div class="sec-heading">
          <span class="sec-heading-symbol">◆</span>
          <span>程式實作與工程探究</span>
        </div>
        <div class="item-list">
          <div class="item-row">
            <span class="bullet">•</span><strong>APCS 大學程式先修檢測</strong>：<br>
            <span style="padding-left: 10px;">觀念 <strong>92.5 分</strong>（<span class="hl-gold">5 級分・前 3.7%</span>）｜實作 <strong>135 分</strong></span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>IEYI 世界青少年發明展</strong>：2023 臺灣選拔賽【<span class="hl-gold">銀獎</span>】
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>學習歷程課程成果優良甄選</strong>：<br>
            <span style="padding-left: 10px;">Arduino 程式設計【<span class="hl-gold">優等</span>】</span>
          </div>
          <div class="item-row">
            <span class="bullet">•</span><strong>跨領域實作探究</strong>：<br>
            <span style="padding-left: 10px;">- 足球運動數據分析模型實作</span><br>
            <span style="padding-left: 10px;">- 東部物理 IYPT 科學營實驗報告第 3 名</span>
          </div>
        </div>
      </div>

    </div>

  </div>

  <!-- Content Bottom Area (Footer) -->
  <div class="bottom-footer">
    <div class="footer-left">
      葉陽甫｜特殊選才備審資料｜高中學習與成果總覽
    </div>
    <div class="footer-right">
      00 / 03
    </div>
  </div>
</div>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML written to: {HTML_PATH}")

async def export_pdf_and_png():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{HTML_PATH.replace(os.sep, '/')}", wait_until="networkidle")
        
        # PDF options: A4, no margin, background true
        await page.pdf(
            path=PDF_PATH,
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            page_ranges="1"
        )
        await browser.close()
        
    doc = fitz.open(PDF_PATH)
    print(f"Generated PDF page count: {len(doc)}")
    print(f"Page 0 rect: {doc[0].rect}")
    
    # Render PNG at 150 DPI
    pix = doc[0].get_pixmap(dpi=150)
    pix.save(PNG_PATH)
    print("Generated PNG successfully!")

asyncio.run(export_pdf_and_png())
