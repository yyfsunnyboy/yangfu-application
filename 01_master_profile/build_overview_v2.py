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

  /* A4 Canvas: 210mm x 297mm */
  .a4-page {{
    width: 210mm;
    height: 297mm;
    box-sizing: border-box;
    margin: 0 auto;
    background: #ffffff;
    padding: 6mm 12mm 5mm 12mm;
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
     1. TOP HEADER (9.5 - 10 pt，比照讀書計畫頂部 Header)
  ---------------------------------------------------- */
  .top-meta-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10pt;
    color: #475569;
    letter-spacing: 0.5px;
    padding-bottom: 2.5px;
    border-bottom: 1px solid #cbd5e1;
    margin-bottom: 4px;
  }}

  .top-meta-left {{
    display: flex;
    gap: 14px;
    font-weight: 500;
  }}

  .top-meta-capsule {{
    background-color: #0f294a;
    color: #ffffff;
    font-size: 9.5pt;
    font-weight: 700;
    padding: 2.5px 9px;
    border-radius: 3px;
    letter-spacing: 0.4px;
  }}

  /* ----------------------------------------------------
     2. MAIN TITLE (主標題 25 pt)
  ---------------------------------------------------- */
  .main-title-section {{
    margin-bottom: 4px;
  }}

  .title-primary {{
    font-size: 25pt;
    font-weight: 900;
    color: #0f294a;
    letter-spacing: 0.5px;
    line-height: 1.15;
    margin-bottom: 3px;
  }}

  .title-divider {{
    height: 1.5px;
    background-color: #0f294a;
    width: 100%;
  }}

  /* ----------------------------------------------------
     3. TWO-COLUMN LAYOUT (左欄 38% ｜ 右欄 59.5%)
  ---------------------------------------------------- */
  .columns-container {{
    display: grid;
    grid-template-columns: 38% 59.5%;
    gap: 2.5%;
    flex: 1;
    margin-top: 3px;
    margin-bottom: 2px;
  }}

  .col-left {{
    display: flex;
    flex-direction: column;
    gap: 12px; /* 統一 Section 節奏 ~16-18pt */
    border-right: 1px solid #e2e8f0;
    padding-right: 11px;
  }}

  .col-right {{
    display: flex;
    flex-direction: column;
    gap: 12px; /* 自然流暢閱讀流，移除巨大空白 */
    padding-left: 2px;
  }}

  /* ----------------------------------------------------
     4. PROFILE / PHOTO SECTION (人物區)
  ---------------------------------------------------- */
  .profile-block {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-bottom: 4px;
    border-bottom: 1px solid #e2e8f0;
  }}

  .profile-photo {{
    width: 31mm;
    height: 39mm;
    object-fit: cover;
    border-radius: 3px;
    border: 1px solid #cbd5e1;
    margin-bottom: 3px;
  }}

  .profile-name {{
    font-size: 23pt;
    font-weight: 900;
    color: #0f294a;
    line-height: 1.15;
    letter-spacing: 1px;
    margin-bottom: 1px;
  }}

  .profile-school {{
    font-size: 12pt;
    font-weight: 700;
    color: #334155;
    line-height: 1.25;
    margin-bottom: 3px;
  }}

  .profile-tagline {{
    font-size: 12pt;
    font-weight: 700;
    color: #0d9488; /* 青綠強調色 */
    line-height: 1.35;
  }}

  /* ----------------------------------------------------
     5. SECTION HEADINGS (分類標題 14.5 pt)
  ---------------------------------------------------- */
  .section-group {{
    display: flex;
    flex-direction: column;
  }}

  .sec-title {{
    font-size: 14pt;
    font-weight: 800;
    color: #0f294a;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
    letter-spacing: 0.3px;
  }}

  .sec-title::before {{
    content: "";
    display: inline-block;
    width: 3.5px;
    height: 13pt;
    background-color: #0f294a;
    border-radius: 1px;
    flex-shrink: 0;
  }}

  .sec-title-right {{
    font-size: 14pt;
    font-weight: 800;
    color: #0f294a;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 4px;
    letter-spacing: 0.3px;
    border-bottom: 1.2px solid #cbd5e1;
    padding-bottom: 2px;
  }}

  .sec-title-right .main-text {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .sec-title-right .main-text::before {{
    content: "";
    display: inline-block;
    width: 3.5px;
    height: 13pt;
    background-color: #0f294a;
    border-radius: 1px;
    flex-shrink: 0;
  }}

  .sec-subtitle {{
    font-size: 12pt;
    font-weight: 500;
    color: #64748b;
  }}

  /* ----------------------------------------------------
     6. LIST & TEXT ITEMS (正文全部 >= 12 pt，行距 1.32)
  ---------------------------------------------------- */
  .item-list {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .item-row {{
    font-size: 12pt;
    line-height: 1.32;
    color: #334155;
  }}

  .item-row strong {{
    color: #0f294a;
    font-weight: 800;
  }}

  .sep {{
    color: #94a3b8;
    margin: 0 4px;
    font-weight: 400;
  }}

  /* 右欄四大代表成果項目 (兩行固定結構，結構緊密) */
  .award-block {{
    display: flex;
    flex-direction: column;
    margin-bottom: 3px;
  }}

  .award-name-line {{
    font-size: 13pt;
    font-weight: 800;
    color: #0f294a;
    line-height: 1.25;
  }}

  .award-sub-line {{
    font-size: 12pt;
    line-height: 1.32;
    color: #475569;
  }}

  .award-sub-line strong {{
    color: #0f294a;
    font-weight: 800;
  }}

  /* 足球四階段對齊排版 (年分固定、名稱固定、成績靠右) */
  .football-timeline {{
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin-bottom: 2px;
  }}

  .football-row {{
    display: flex;
    align-items: baseline;
    font-size: 12pt;
    line-height: 1.32;
    color: #334155;
  }}

  .football-year {{
    width: 44px;
    flex-shrink: 0;
    font-weight: 800;
    color: #0f294a;
  }}

  .football-league {{
    flex: 1;
    color: #475569;
  }}

  .football-result {{
    flex-shrink: 0;
    font-weight: 800;
    color: #0f294a;
  }}

  /* ----------------------------------------------------
     7. FOOTER (9.5 - 10 pt，比照讀書計畫頁尾)
  ---------------------------------------------------- */
  .page-footer {{
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
    <!-- 頁首 Meta Header (10 pt 讀書計畫風格) -->
    <div class="top-meta-header">
      <div class="top-meta-left">
        <span>個人總覽</span>
        <span style="font-weight: 700; color: #0f294a;">PAGE 00</span>
        <span>高中學習與成果</span>
      </div>
      <div class="top-meta-capsule">
        個人主軸｜資訊 × 科研 × 足球
      </div>
    </div>

    <!-- 主標題 (25 pt) -->
    <div class="main-title-section">
      <div class="title-primary">葉陽甫｜高中學習與成果總覽</div>
      <div class="title-divider"></div>
    </div>
  </div>

  <!-- 雙欄版型 (左欄 38% ｜ 右欄 59.5%) -->
  <div class="columns-container">
    
    <!-- ==================== 左欄 (人物輪廓・學業・語言・服務・跨域) ==================== -->
    <div class="col-left">
      
      <!-- 人物區 (照片占左欄約 1/4 高度 + 姓名 + 學校 + 二行定位) -->
      <div class="profile-block">
        <img class="profile-photo" src="data:image/jpeg;base64,{photo_b64}" alt="葉陽甫">
        <div class="profile-name">葉陽甫</div>
        <div class="profile-school">國立花蓮高級中學</div>
        <div class="profile-tagline">
          資訊工程 × AI教育 × 科學研究<br>外語能力 × 足球競技
        </div>
      </div>

      <!-- 學業表現 (完整 6 語意單位，零斷裂，全部 >= 12 pt) -->
      <div class="section-group">
        <div class="sec-title">學業表現</div>
        <div class="item-list">
          <div class="item-row">四學期班排前五<span class="sep">｜</span><strong>3 → 3 → 5 → 3</strong></div>
          <div class="item-row">四學期平均 <strong>84.2</strong></div>
          <div class="item-row">年排 <strong>24 / 320</strong><span class="sep">｜</span><strong>前 8%</strong></div>
          <div class="item-row">英文加權 91<span class="sep">｜</span><strong>前 4%</strong></div>
          <div class="item-row">高二下英文 <strong>96</strong><span class="sep">｜</span>年排 7・<strong>前 2%</strong></div>
          <div class="item-row">數學 <strong>前6%</strong><span class="sep">｜</span>化學 <strong>前4%</strong></div>
          <div class="item-row">地科 <strong>前2%</strong><span class="sep">｜</span>資訊 <strong>前6%</strong></div>
          <div class="item-row">Arduino<span class="sep">｜</span><strong>94</strong>・選修班第 2 / 20</div>
          <div class="item-row">Python<span class="sep">｜</span><strong>90</strong>・選修班第 4 / 32</div>
        </div>
      </div>

      <!-- 英文與語文 (清晰能力與成果，零拆字，全部 >= 12 pt) -->
      <div class="section-group">
        <div class="sec-title">英文與語文</div>
        <div class="item-list">
          <div class="item-row">TOEIC <strong>945</strong><span class="sep">｜</span><strong>金色證書</strong></div>
          <div class="item-row">GEPT 中高級<span class="sep">｜</span><strong>四項全合格</strong></div>
          <div class="item-row">英語演說<span class="sep">｜</span>初賽第 1・複賽第 4</div>
          <div class="item-row">英文作文<span class="sep">｜</span>校內第 2・縣賽甲等</div>
          <div class="item-row">國中英文作文優等<span class="sep">｜</span>英語讀者劇場特優</div>
        </div>
      </div>

      <!-- 幹部・社團・服務 (全部 >= 12 pt) -->
      <div class="section-group">
        <div class="sec-title">幹部・社團・服務</div>
        <div class="item-list">
          <div class="item-row">高一<span class="sep">｜</span>圖書資訊股長</div>
          <div class="item-row">高二上下<span class="sep">｜</span>事務股長連任</div>
          <div class="item-row">花中資訊研究社<span class="sep">｜</span>資訊研究社聯合幹訓</div>
        </div>
      </div>

      <!-- 跨域學習 (全部 >= 12 pt) -->
      <div class="section-group">
        <div class="sec-title">跨域學習</div>
        <div class="item-list">
          <div class="item-row">歷史課程成果<span class="sep">｜</span>佳作</div>
          <div class="item-row">東華大學國際文化交流</div>
          <div class="item-row">C語言程式課程<span class="sep">｜</span>第25屆科學傳承營</div>
        </div>
      </div>

    </div>

    <!-- ==================== 右欄 (核心成果：科研・工程實作・足球競技) ==================== -->
    <div class="col-right">
      
      <!-- 資訊・AI・科研 (固定結構：競賽名稱 + 類別/範圍｜結果) -->
      <div class="section-group">
        <div class="sec-title-right">
          <span class="main-text">資訊・AI・科研</span>
          <span class="sec-subtitle">代表性大成果</span>
        </div>
        <div class="item-list">
          <div class="award-block">
            <div class="award-name-line">第23屆育秀盃創意獎</div>
            <div class="award-sub-line">高中職 AI 應用類<span class="sep">｜</span><strong>金獎（全國首獎・10萬元獎金）</strong></div>
          </div>
          <div class="award-block">
            <div class="award-name-line">2026 神通 AI 數位學院扶輪盃</div>
            <div class="award-sub-line">高中 AI 競賽<span class="sep">｜</span><strong>第一名（全國冠軍）</strong></div>
          </div>
          <div class="award-block">
            <div class="award-name-line">第25屆旺宏科學獎</div>
            <div class="award-sub-line">全領域 846 件評選<span class="sep">｜</span><strong>全國決賽 20 強（資工僅 4 件）</strong></div>
          </div>
          <div class="award-block">
            <div class="award-name-line">第66屆東區科展</div>
            <div class="award-sub-line">電腦與資訊學科<span class="sep">｜</span><strong>優等第 2 名</strong></div>
          </div>
          
          <div class="item-row" style="margin-top: 1.5px;">
            校內電腦與資訊科展優勝<span class="sep">｜</span>資訊學科能力競賽佳作
          </div>
          <div class="item-row">
            花蓮區自主學習成果銅獎<span class="sep">｜</span>AI 自適應學習自主學習成果
          </div>
          <div class="item-row" style="color: #0d9488; font-weight: 700; margin-top: 1px;">
            技術關鍵字<span class="sep">｜</span>AST Healer 確定性修復<br>
            LLM 程式生成<span class="sep">｜</span>自適應學習系統
          </div>
        </div>
      </div>

      <!-- 程式・工程・自主實作 (全部 >= 12 pt) -->
      <div class="section-group">
        <div class="sec-title-right">
          <span class="main-text">程式・工程・自主實作</span>
          <span class="sec-subtitle">檢定與專題探究</span>
        </div>
        <div class="item-list">
          <div class="item-row">
            APCS 程式先修檢測<span class="sep">｜</span>觀念 <strong>92・5 級分（前 3.7%）</strong><span class="sep">｜</span>實作 <strong>135</strong>
          </div>
          <div class="item-row">
            2023 IEYI 臺灣選拔賽<span class="sep">｜</span><strong>銀獎</strong>
          </div>
          <div class="item-row">
            高一校內工程科展<span class="sep">｜</span><strong>優勝</strong>
          </div>
          <div class="item-row">
            東部物理 IYPT 科學營<span class="sep">｜</span>實驗報告 <strong>第 3 名</strong>
          </div>
          <div class="item-row">
            Arduino 課程成果<span class="sep">｜</span><strong>優等</strong>
          </div>
          <div class="item-row" style="color: #475569; margin-top: 1px;">
            足球數據分析自主學習<span class="sep">｜</span>AI 自適應學習系統自主學習與架構深化
          </div>
        </div>
      </div>

      <!-- 足球・體育 (固定對齊，無孤字，全部 >= 12 pt) -->
      <div class="section-group">
        <div class="sec-title-right">
          <span class="main-text">足球・體育</span>
          <span class="sec-subtitle">長期高壓競技與自律</span>
        </div>
        
        <!-- 四年聯賽固定對齊 -->
        <div class="football-timeline">
          <div class="football-row">
            <span class="football-year">2023</span>
            <span class="sep">｜</span>
            <span class="football-league">國中足球聯賽（乙級11人制）</span>
            <span class="sep">｜</span>
            <span class="football-result">全國季軍</span>
          </div>
          <div class="football-row">
            <span class="football-year">2024</span>
            <span class="sep">｜</span>
            <span class="football-league">全國青年盃五人制（公開組）</span>
            <span class="sep">｜</span>
            <span class="football-result">全國第 5 名</span>
          </div>
          <div class="football-row">
            <span class="football-year">2025</span>
            <span class="sep">｜</span>
            <span class="football-league">高中五人制足球聯賽</span>
            <span class="sep">｜</span>
            <span class="football-result">全國第 6 名</span>
          </div>
          <div class="football-row">
            <span class="football-year">2026</span>
            <span class="sep">｜</span>
            <span class="football-league">高中五人制足球聯賽</span>
            <span class="sep">｜</span>
            <span class="football-result">全國第 5 名</span>
          </div>
        </div>

        <div class="item-list">
          <div class="item-row" style="margin-top: 2px;">
            校運會 800m 高二男子組 <strong>第 2 名</strong><span class="sep">｜</span>花蓮縣運足球 <strong>冠軍</strong>
          </div>
          <div class="item-row">
            體育學年成績<span class="sep">｜</span>年排 13 / 320<span class="sep">｜</span><strong>前 4%</strong>
          </div>
          <div class="item-row" style="color: #475569;">
            國中足球隊隊長<span class="sep">｜</span>高中足球校隊主力
          </div>
          <div class="item-row" style="color: #475569;">
            花中 9km 越野賽<span class="sep">｜</span><strong>完跑證明</strong>
          </div>
        </div>
      </div>

    </div>

  </div>

  <!-- Page Footer (9.5 pt，比照讀書計畫頁尾格式) -->
  <footer class="page-footer">
    <div class="footer-left">
      葉陽甫｜特殊選才備審資料｜高中學習與成果總覽
    </div>
    <div class="footer-right">
      00 / 03
    </div>
  </footer>
</div>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML written to:", HTML_PATH)

async def convert():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        file_url = f"file:///{HTML_PATH.replace(os.sep, '/')}"
        await page.goto(file_url, wait_until="networkidle")
        await page.pdf(
            path=PDF_PATH,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        await browser.close()
    
    doc = fitz.open(PDF_PATH)
    print(f"Generated PDF page count: {len(doc)}")
    for i, page in enumerate(doc):
        print(f"Page {i} rect: {page.rect}")
    pix = doc[0].get_pixmap(dpi=150)
    pix.save(PNG_PATH)
    print("Generated PNG successfully!")

if __name__ == "__main__":
    asyncio.run(convert())
