import os
import base64
import asyncio
from playwright.async_api import async_playwright

WORKSPACE = r"D:\Python\yangfu-application"
PHOTO_PATH = os.path.join(WORKSPACE, "00_source_materials", "照片", "YEH YANG FU.jpg")
OUTPUT_PDF = os.path.join(WORKSPACE, "01_master_profile", "07_personal_profile_summary.pdf")
OUTPUT_SINGLE_PDF = os.path.join(WORKSPACE, "01_master_profile", "07_personal_profile_single_page.pdf")

with open(PHOTO_PATH, "rb") as f:
    photo_b64 = base64.b64encode(f.read()).decode("utf-8")

# HTML Template with precise A4 pagination (4 pages exact)
html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>葉陽甫｜個人經歷與得獎事蹟總表</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Outfit:wght@400;600;700;800&display=swap');

  @page {{
    size: A4 portrait;
    margin: 8mm 9mm 8mm 9mm;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft JhengHei", sans-serif;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-size: 8.5pt;
    line-height: 1.38;
  }}

  .page-container {{
    width: 100%;
    height: 279mm;
    max-height: 279mm;
    box-sizing: border-box;
    padding: 2px 2px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    overflow: hidden;
  }}

  .page-container:last-child {{
    page-break-after: avoid;
  }}

  .header {{
    display: flex;
    align-items: center;
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 6px;
    margin-bottom: 6px;
    position: relative;
  }}

  .avatar-box {{
    width: 66px;
    height: 82px;
    flex-shrink: 0;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    border: 2px solid #2563eb;
    margin-right: 12px;
  }}

  .avatar-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .header-info {{
    flex: 1;
  }}

  .name-row {{
    display: flex;
    align-items: baseline;
    gap: 12px;
  }}

  .name {{
    font-size: 20pt;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: 2px;
  }}

  .school {{
    font-size: 11pt;
    font-weight: 700;
    color: #1e40af;
  }}

  .tag-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 3px;
  }}

  .tag {{
    font-size: 7.5pt;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 4px;
    background: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
  }}

  .tag.primary {{
    background: #eff6ff;
    color: #1d4ed8;
    border-color: #bfdbfe;
  }}

  .tag.gold {{
    background: #fefce8;
    color: #a16207;
    border-color: #fde047;
  }}

  .two-column {{
    display: flex;
    gap: 10px;
    flex: 1;
  }}

  .col-left {{
    width: 37.5%;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .col-right {{
    width: 62.5%;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 5px 8px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  }}

  .card-title {{
    font-size: 9.3pt;
    font-weight: 800;
    color: #1e3a8a;
    border-left: 3.5px solid #2563eb;
    padding-left: 6px;
    margin-bottom: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .card-subtitle {{
    font-size: 8.2pt;
    font-weight: 700;
    color: #0369a1;
    margin-top: 2px;
    margin-bottom: 1px;
    border-bottom: 1px dashed #e0f2fe;
    padding-bottom: 1px;
  }}

  ul.item-list {{
    margin: 0;
    padding-left: 13px;
    list-style-type: square;
  }}

  ul.item-list li {{
    margin-bottom: 1.5px;
    color: #334155;
    font-size: 8.1pt;
    line-height: 1.34;
  }}

  .highlight {{
    font-weight: 700;
    color: #0f172a;
  }}

  .badge-first {{
    color: #dc2626;
    font-weight: 800;
  }}

  .badge-gold {{
    color: #b45309;
    font-weight: 800;
  }}

  .badge-blue {{
    color: #2563eb;
    font-weight: 700;
  }}

  /* Academic Trend Box */
  .trend-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 3px 6px;
    margin-top: 3px;
  }}

  .chart-svg {{
    width: 100%;
    height: 44px;
  }}

  /* PAGES 2, 3, 4: TABLES */
  .doc-title {{
    font-size: 13.5pt;
    font-weight: 900;
    color: #0f172a;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 4px;
    margin-top: 0;
    margin-bottom: 6px;
  }}

  .section-h2 {{
    font-size: 10pt;
    font-weight: 800;
    color: #1e3a8a;
    margin-top: 6px;
    margin-bottom: 4px;
    border-left: 3.5px solid #3b82f6;
    padding-left: 6px;
  }}

  table.detail-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 6px;
    font-size: 7.7pt;
    line-height: 1.32;
  }}

  table.detail-table th, table.detail-table td {{
    border: 1px solid #cbd5e1;
    padding: 3.5px 5.5px;
    text-align: left;
    vertical-align: top;
  }}

  table.detail-table th {{
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
    font-size: 7.8pt;
  }}

  table.detail-table tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  .file-path {{
    font-family: Consolas, monospace;
    font-size: 6.9pt;
    color: #475569;
    background: #f1f5f9;
    padding: 1px 2px;
    border-radius: 2px;
    word-break: break-all;
  }}

  .page-footer {{
    font-size: 7.3pt;
    color: #94a3b8;
    text-align: right;
    border-top: 1px solid #f1f5f9;
    padding-top: 2px;
    margin-top: auto;
  }}
</style>
</head>
<body>

<!-- ==================== PAGE 1: RESUME SHEET ==================== -->
<div class="page-container">
  <div>
    <div class="header">
      <div class="avatar-box">
        <img src="data:image/jpeg;base64,{photo_b64}" alt="葉陽甫">
      </div>
      <div class="header-info">
        <div class="name-row">
          <span class="name">葉 陽 甫</span>
          <span class="school">國立花蓮高級中學 普通科（自然組）</span>
        </div>
        <div class="tag-container">
          <span class="tag primary">資訊與自適應學習架構</span>
          <span class="tag gold">多益 945 金色證書（聽485 / 讀460）</span>
          <span class="tag primary">APCS 觀念滿級 5 級（92分）</span>
          <span class="tag">GEPT 中高級 CEFR B2+ 四項全合格</span>
          <span class="tag">全國足球聯賽 第5名 / 第6名</span>
          <span class="tag">旺宏科學獎 全國20強入圍</span>
        </div>
      </div>
    </div>

    <div class="two-column">
      <!-- LEFT COLUMN -->
      <div class="col-left">
        <!-- 幹部經歷 -->
        <div class="card">
          <div class="card-title">幹部經歷</div>
          <ul class="item-list">
            <li><span class="highlight">班級事務股長</span>（高二上、高二下 連任）</li>
            <li><span class="highlight">班級圖書資訊股長</span>（高一上）</li>
            <li><span class="highlight">花崗國中足球隊隊長</span>（國三甲級聯賽）</li>
            <li><span class="highlight">111 學年度班級模範生</span>（文武兼備肯定）</li>
          </ul>
        </div>

        <!-- 社團經歷 -->
        <div class="card">
          <div class="card-title">社團經歷</div>
          <ul class="item-list">
            <li><span class="highlight">花蓮高中資訊研究社</span> 社員（幹訓研習）</li>
            <li><span class="highlight">花蓮高中足球校隊</span> 主力隊員（征戰全國五人制聯賽）</li>
          </ul>
        </div>

        <!-- 研習經歷 -->
        <div class="card">
          <div class="card-title">研習經歷</div>
          <ul class="item-list">
            <li><span class="highlight">東部物理 IYPT 科學營</span> 實驗報告發表第三名</li>
            <li><span class="highlight">第 25 屆科學傳承營</span> 結業證明</li>
            <li><span class="highlight">C 語言程式設計課程</span> 中英文雙語結業證書</li>
            <li><span class="highlight">資訊研究社聯合幹部訓練</span> 研習證明</li>
            <li><span class="highlight">東華大學國際文化夜</span> 交流參與證明</li>
            <li><span class="highlight">花蓮區自主學習成果分享會</span> 參展交流證明</li>
          </ul>
        </div>

        <!-- 專題經歷 -->
        <div class="card">
          <div class="card-title">專題經歷</div>
          <ul class="item-list">
            <li><span class="highlight">足球員數據分析</span>（FBref 爬蟲 + pandas，成果獎）</li>
            <li><span class="highlight">Arduino 智慧節能防呆警報器</span>（微控制感測整合）</li>
            <li><span class="highlight">多功能智慧遮雨棚</span>（Arduino × App Inventor，IEYI銀獎）</li>
            <li><span class="highlight">香蕉葉環保餐具探究</span>（花中校內科展工程類優勝）</li>
          </ul>
        </div>

        <!-- 學業表現 -->
        <div class="card">
          <div class="card-title">學業表現</div>
          <ul class="item-list">
            <li><span class="highlight">四學期班排前五</span>：3 → 3 → 5 → 3（兩度全班智育第三）</li>
            <li><span class="highlight">資訊選修卓越</span>：Python 90 分、Arduino 94 分</li>
            <li><span class="highlight">學測模擬考</span>：自然組第 1 名（34人）、校排 10/325（數A 12級）</li>
            <li><span class="highlight">歷史成果甄選</span>：全校佳作（跨域文理思辨）</li>
          </ul>
          <div class="trend-box">
            <div style="font-size: 7.1pt; color: #475569; display: flex; justify-content: space-between; font-weight: 600;">
              <span>高二段考成績成長趨勢</span>
              <span style="color: #1d4ed8;">年排 40 → 19 名</span>
            </div>
            <svg class="chart-svg" viewBox="0 0 200 42">
              <line x1="20" y1="36" x2="180" y2="36" stroke="#cbd5e1" stroke-width="1" />
              <polyline fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"
                points="45,28 155,10" />
              <circle cx="45" cy="28" r="3.2" fill="#2563eb" />
              <circle cx="155" cy="10" r="3.6" fill="#dc2626" />
              <text x="45" y="39" font-size="6.8" fill="#64748b" text-anchor="middle">期中1 (78.56)</text>
              <text x="155" y="39" font-size="6.8" fill="#1e3a8a" font-weight="700" text-anchor="middle">期中2 (84.44)</text>
              <text x="155" y="7" font-size="6.2" fill="#dc2626" font-weight="800" text-anchor="middle">+5.88分</text>
            </svg>
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN -->
      <div class="col-right">
        <!-- 競賽 / 檢定 -->
        <div class="card">
          <div class="card-title">競賽／檢定</div>

          <div class="card-subtitle">資訊與人工智慧競賽</div>
          <ul class="item-list">
            <li><span class="badge-first">第一名（冠軍）</span>｜2026 神通 AI 數位學院扶輪盃高中 AI 競賽</li>
            <li><span class="badge-gold">金獎（10萬獎金）</span>｜第 23 屆育秀盃創意獎 高中職 AI 應用類</li>
            <li><span class="badge-blue">入圍全國決賽 20 強</span>｜第 25 屆旺宏科學獎（846件選20件，資工僅4件）</li>
            <li><span class="highlight">優等學生獎（第 2 名）</span>｜第 66 屆東區科展 電腦資訊學科</li>
            <li><span class="highlight">優勝</span>｜114 學年度花中校內科展 電腦資訊學科</li>
            <li><span class="highlight">銅獎</span>｜花蓮區高級中等學校學生自主學習成果分享會</li>
            <li><span class="highlight">佳作</span>｜113 學年度數理及資訊學科能力競賽 資訊科</li>
            <li><span class="highlight">銀獎</span>｜2023 IEYI 世界青少年創客發明展暨臺灣選拔賽（遮雨棚）</li>
            <li><span class="highlight">金獎</span>｜2021 太平洋盃科技教育競賽 創意創客組（國一團隊觀摩）</li>
          </ul>

          <div class="card-subtitle">專業檢定與數理能力</div>
          <ul class="item-list">
            <li><span class="badge-first">APCS 觀念題 92 分（第 5 級分，滿級分）</span>／實作 135 分（2級分）</li>
            <li><span class="highlight">AMC12A 美國數學競賽</span> 參賽證書／成績檢定</li>
            <li><span class="badge-gold">銀牌獎</span>｜2022 更生日報盃數學大賽 國中二年級組</li>
            <li><span class="highlight">團體一等獎／個人優良獎</span>｜2023 JHMC 國中數學競賽花蓮示範賽</li>
          </ul>

          <div class="card-subtitle">語文能力與檢定</div>
          <ul class="item-list">
            <li><span class="badge-gold">多益 945 分【金色證書】</span>（聽力 485 逼近滿分、閱讀 460，近母語水準）</li>
            <li><span class="badge-blue">全民英檢（GEPT）中高級證書</span>（CEFR B2+，聽說讀寫四項全合格）</li>
            <li><span class="highlight">全民英檢（GEPT）中級合格</span>（CEFR B1+，聽說讀寫全合格）</li>
            <li><span class="highlight">全校英文比賽</span>：高一英語演說初賽第一／複賽第四、高二英文作文第二</li>
            <li><span class="highlight">全縣英文競賽</span>：114 年作文甲等（國中曾獲讀者劇場特優、作文優等）</li>
          </ul>

          <div class="card-subtitle">體育競技與全人發展</div>
          <ul class="item-list">
            <li><span class="badge-first">全國第五名</span>｜114 學年全國中等學校足球聯賽（5人制）高中男生組（勝惠文）</li>
            <li><span class="highlight">全國第六名</span>｜113 學年全國中等學校足球聯賽（5人制）高中男生組</li>
            <li><span class="highlight">全國第五名</span>｜2024 年全國青年盃足球錦標賽公開組</li>
            <li><span class="highlight">第二名（銀牌）</span>｜114 年校運會 800m 男子組（越野賽完跑；國中曾獲第1）</li>
            <li><span class="highlight">全國季軍</span>｜111 學年國中足球聯賽（乙級）決賽（PK 戰踢進關鍵決勝球）</li>
          </ul>
        </div>

        <!-- 資訊學習和實作 -->
        <div class="card">
          <div class="card-title">資訊學習和實作</div>
          <ul class="item-list">
            <li><span class="highlight">自學 Python 爬蟲與資料科學</span>：運用 BeautifulSoup 與 pandas 清洗 FBref 足球數據，自主克服 IP Rate Limiting 反爬限制。</li>
            <li><span class="highlight">自學微控制器與軟硬體整合</span>：掌握 Arduino Uno、I2C 通訊、感測器與伺服控制。</li>
            <li><span class="highlight">LLM 應用工程與動態代碼生成</span>：掌握 Prompt Engineering 與 Code-as-Content 架構。</li>
            <li><span class="highlight">AST 語法樹與確定性修復演算法</span>：深入 Python AST 編譯原理，自製確定性程式修復器（AST Active Healer）與自適應棄權機制（Abstention Mechanism）。</li>
          </ul>
        </div>

        <!-- 研究經歷 -->
        <div class="card">
          <div class="card-title">研究經歷</div>
          <ul class="item-list">
            <li><span class="highlight">《基於人工智慧之自適應輔助學習架構探究》</span>（旺宏全國 20 強，高二至高三）<br>
              聚焦 AST Healer 邊界實驗、對照組驗證與棄權機制，以嚴謹基準評估模型可靠度。</li>
            <li><span class="highlight">自適應輔助學習架構科展探究</span>（第 66 屆東區科展優等第二名，高二）<br>
              經歷東區科展評審答辯反思，誠懇檢討焦點過大缺口，重新補強對照實驗。</li>
            <li><span class="highlight">多模組自適應輔助學習系統開發</span>（第 23 屆育秀盃金獎，高二）<br>
              負責整合 Brain(PPO) + Hands(Code) + Mouth(RAG)，完成跨模組狀態閉環。</li>
            <li><span class="highlight">自適應學習系統原型實作</span>（2026 神通 AI 盃冠軍，高二）<br>
              負責教材匯入至多模態作答回傳之完整資料主線與結構化資料庫規劃。</li>
            <li><span class="highlight">花蓮高商高職課堂場域試用導入</span>（高二至高三）<br>
              協助教師部署系統並收集課堂教學反饋，梳理出八大跨域未解實務課題。</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="page-footer">葉陽甫個人經歷與得獎事蹟總表 • 頁 1 / 4</div>
</div>

<!-- ==================== PAGE 2: 經歷與獲獎細部索引表 (幹部、社團、研習、專題) ==================== -->
<div class="page-container">
  <div>
    <h1 class="doc-title">葉陽甫｜個人經歷與得獎事蹟完整分類詳表</h1>

    <div class="section-h2">1. 幹部服務經歷 (Cadre & Leadership)</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 16%;">期間／學年度</th>
          <th style="width: 17%;">擔任職務／身分</th>
          <th style="width: 18%;">服務單位／班級</th>
          <th style="width: 23%;">佐證檔案路徑</th>
          <th>證明力與工作內涵說明 [已證實]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>113學年第1學期</b></td>
          <td>班級圖書資訊股長</td>
          <td>花蓮高中 105 班</td>
          <td><span class="file-path">獎狀/學業獎狀/20250114_班級幹部服務證書_圖書資訊股長.pdf</span></td>
          <td>正式服務證書；負責班級資訊設備維護、電腦軟體管理與圖書資源推廣。</td>
        </tr>
        <tr>
          <td><b>114學年第1學期</b></td>
          <td>班級事務股長</td>
          <td>花蓮高中 205 班</td>
          <td><span class="file-path">獎狀/學業獎狀/20251031_班級幹部服務證書_事務股長.pdf</span></td>
          <td>正式服務證書；負責班級公共事務推動、總務器材保管與全班各項事務協調。</td>
        </tr>
        <tr>
          <td><b>114學年第2學期</b></td>
          <td>班級事務股長</td>
          <td>花蓮高中 205 班</td>
          <td><span class="file-path">獎狀/學業獎狀/20260630_班級幹部服務證書_事務股長.pdf</span></td>
          <td>正式服務證書；連任事務股長，具備高度責任感、細膩執行力與師生信賴。</td>
        </tr>
        <tr>
          <td><b>111學年（國三）</b></td>
          <td>足球校隊隊長</td>
          <td>花崗國中足球隊</td>
          <td><span class="file-path">陽甫國中生活/HFL甲組合影_含標題.png</span></td>
          <td>挑戰中等學校足球聯賽甲級賽事，帶領全隊日常訓練、高壓臨場戰術執行與心態穩定。</td>
        </tr>
        <tr>
          <td><b>111學年（國中）</b></td>
          <td>全校班級模範生</td>
          <td>花崗國中 909 班</td>
          <td><span class="file-path">陽甫國中生活/修過的照片/111學年模範生獎狀.jpg</span></td>
          <td>導師評語：「品學兼優，文武兼備，參加校外發明展、科技競賽、英語文、數學及足球競賽成績優異」。</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">2. 社團與研習活動 (Clubs & Seminars)</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 14%;">日期／學年</th>
          <th style="width: 21%;">活動／社團名稱</th>
          <th style="width: 21%;">主辦單位／身分</th>
          <th style="width: 23%;">佐證檔案路徑</th>
          <th>成果與實質經歷 [已證實]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>113～114學年</td>
          <td>花蓮高中資訊研究社</td>
          <td>花中資研社／社員</td>
          <td><span class="file-path">獎狀/學業獎狀/20250913_資訊研究社聯合幹訓研習證明.pdf</span></td>
          <td>參與演算法研討、資訊技術交流與幹部培訓研習。</td>
        </tr>
        <tr>
          <td>113～114學年</td>
          <td>花蓮高中足球校隊</td>
          <td>花中足球隊／主力隊員</td>
          <td><span class="file-path">獎狀/足球獎狀/（各項體育署聯賽獎狀）</span></td>
          <td>普通班高強度課業下自律練球，代表學校征戰全國中等學校五人制足球聯賽。</td>
        </tr>
        <tr>
          <td>2024/08/15</td>
          <td>第 25 屆科學傳承營</td>
          <td>國立花蓮高級中學等</td>
          <td><span class="file-path">獎狀/科展獎狀/20240815_第25屆科學傳承營結業證明書.pdf</span></td>
          <td>完成科學實驗設計、專題探討與跨領域科研方法傳承營隊訓練。</td>
        </tr>
        <tr>
          <td>2024/10/20</td>
          <td>東部物理 IYPT 科學營</td>
          <td>中華民國物理教育學會</td>
          <td><span class="file-path">獎狀/科展獎狀/20241020_物理IYPT營報告第三名.pdf</span></td>
          <td>針對開放性物理現象設計實驗觀測並完成公開簡報，獲實驗報告發表第三名。</td>
        </tr>
        <tr>
          <td>2024/10/25</td>
          <td>C 語言程式設計課程</td>
          <td>專業認證機構</td>
          <td><span class="file-path">獎狀/科展獎狀/20241025_C語言課程結業證書_中英文版.pdf</span></td>
          <td>完成結構化程式設計、陣列、指標與演算法基礎課程，獲中英文雙語證書。</td>
        </tr>
        <tr>
          <td>2025/11/28</td>
          <td>東華大學國際文化夜</td>
          <td>國立東華大學</td>
          <td><span class="file-path">獎狀/其他獎狀/20251128_東華大學國際文化夜參與證明.pdf</span></td>
          <td>積極拓展國際視野，與外籍青年學人進行跨文化交流與互動。</td>
        </tr>
        <tr>
          <td>2026/06/06</td>
          <td>花蓮區自主學習分享會</td>
          <td>花蓮區高中課程中心</td>
          <td><span class="file-path">獎狀/科展獎狀/20260606_花蓮區自主學習分享會參展證明.pdf</span></td>
          <td>自主學習專案公開參展交流，獲大會頒發參展證明書與發表評定。</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">3. 專題實作與自主學習 (Projects & Self-Directed Learning)</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 14%;">期間／日期</th>
          <th style="width: 22%;">專題名稱</th>
          <th style="width: 24%;">核心技術與個人職責</th>
          <th style="width: 21%;">佐證檔案路徑</th>
          <th>榮譽與成果 [已證實]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>2025/06/30</td>
          <td><b>足球員數據分析專題</b></td>
          <td>Python 爬蟲（BeautifulSoup）、pandas 處理 FBref 數據，自主排除 Rate Limiting 節流。</td>
          <td><span class="file-path">獎狀/科展獎狀/20250630_自主學習成果獎狀_足球數據.pdf</span></td>
          <td>獲花中自主學習成果獎狀；成功串聯足球興趣與數據科學技能。</td>
        </tr>
        <tr>
          <td>2024～2025</td>
          <td><b>Arduino 節能防呆警報器</b></td>
          <td>獨立整合 Uno、感測器、伺服馬達、LED/蜂鳴器，完成 input → logic → output 循序除錯。</td>
          <td><span class="file-path">academic_records/114學年學期成績.pdf</span></td>
          <td>校內 Arduino 程式設計選修 94 分，展現軟硬體整合問題拆解能力。</td>
        </tr>
        <tr>
          <td>2026/01/09</td>
          <td><b>AI 輔助自適應學習系統</b></td>
          <td>探討高職數學課堂適性學習，設計自動化教材剖析與動態題目生成原型。</td>
          <td><span class="file-path">獎狀/科展獎狀/20260109_自主學習獎狀_AI自適應系統.pdf</span></td>
          <td>獲花中自主學習成果獎狀；為後續神通 AI 與育秀盃研究奠定根基。</td>
        </tr>
        <tr>
          <td>2026/06/26</td>
          <td><b>AI 自適應學習架構深化</b></td>
          <td>深化 AST Healer 確定性修復演算法、模型能力邊界與棄權機制驗證。</td>
          <td><span class="file-path">獎狀/科展獎狀/20260626_自主學習獎狀_AI自適應架構.pdf</span></td>
          <td>獲花中自主學習成果獎狀；深化科研驗證方法與嚴謹統計對照。</td>
        </tr>
        <tr>
          <td>2022～2023</td>
          <td><b>多功能智慧遮雨棚</b>（國中）</td>
          <td>三人隊伍；陽甫負責 Arduino 接線與程式、App Inventor 藍牙手機端情境控制。</td>
          <td><span class="file-path">陽甫國中生活/發明展 (2)/2023_IEYI銀獎證書.jpg</span></td>
          <td>獲 2023 IEYI 臺灣選拔賽便利生活類銀獎、花蓮縣科技發明展佳作。</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">葉陽甫個人經歷與得獎事蹟總表 • 頁 2 / 4</div>
</div>

<!-- ==================== PAGE 3: 競賽與檢定詳表 (資訊AI、數理檢定、語文、體育) ==================== -->
<div class="page-container">
  <div>
    <h1 class="doc-title">葉陽甫｜競賽、檢定與研究經歷詳表</h1>

    <div class="section-h2">4. 資訊科技與人工智慧競賽 (IT & AI Competitions)</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 11%;">獲獎日期</th>
          <th style="width: 25%;">競賽名稱</th>
          <th style="width: 18%;">主辦／合辦單位</th>
          <th style="width: 21%;">獲得獎項／名次</th>
          <th>佐證檔案路徑 [已證實]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>2026/02/02</td>
          <td>2026 神通 AI 數位學院扶輪盃高中 AI 賽</td>
          <td>神通科技、扶輪社</td>
          <td><b style="color: #dc2626;">高中組 第一名（冠軍）</b></td>
          <td><span class="file-path">獎狀/科展獎狀/20260202_神通AI第一名.pdf</span></td>
        </tr>
        <tr>
          <td>2026/04/24</td>
          <td>第 23 屆育秀盃創意獎</td>
          <td>育秀教育基金會</td>
          <td><b style="color: #b45309;">高中職 AI 應用類 金獎（10萬）</b></td>
          <td><span class="file-path">獎狀/科展獎狀/20260424_育秀盃金獎.pdf</span></td>
        </tr>
        <tr>
          <td>2026/07</td>
          <td>第 25 屆旺宏科學獎</td>
          <td>旺宏電子教育基金會</td>
          <td><b style="color: #2563eb;">全國決賽入圍 20 強</b>（資工僅4件）</td>
          <td>官方公告（編號 SA25-016，決賽待公布）</td>
        </tr>
        <tr>
          <td>2026/04/28</td>
          <td>第 66 屆東區科展（第七區科學展覽會）</td>
          <td>國教署、宜蘭高中</td>
          <td><b>電腦資訊學科 優等學生獎（第2名）</b></td>
          <td><span class="file-path">獎狀/科展獎狀/20260428_東區科展優等.pdf</span></td>
        </tr>
        <tr>
          <td>2026/03/01</td>
          <td>花蓮高中第 66 屆校內科學展覽會</td>
          <td>國立花蓮高級中學</td>
          <td><b>電腦資訊學科 優勝</b></td>
          <td><span class="file-path">獎狀/科展獎狀/20260301_校內科展資訊優勝.pdf</span></td>
        </tr>
        <tr>
          <td>2026/06/06</td>
          <td>花蓮區高中自主學習成果分享會</td>
          <td>花蓮區高中課程中心</td>
          <td><b>銅獎</b>（作品公開發表展示）</td>
          <td><span class="file-path">獎狀/科展獎狀/20260606_學習成果分享會銅獎.pdf</span></td>
        </tr>
        <tr>
          <td>2024/10/01</td>
          <td>113 學年度數理及資訊學科能力競賽</td>
          <td>教育部國教署</td>
          <td><b>資訊科 佳作</b></td>
          <td><span class="file-path">獎狀/科展獎狀/20241001_學科能力競賽資訊佳作.pdf</span></td>
        </tr>
        <tr>
          <td>2025/03/01</td>
          <td>花中 113 學年校內科展（香蕉葉餐具）</td>
          <td>國立花蓮高級中學</td>
          <td><b>工程學科 優勝</b></td>
          <td><span class="file-path">獎狀/科展獎狀/20250301_校內科展工程優勝.pdf</span></td>
        </tr>
        <tr>
          <td>2023 年</td>
          <td>2023 IEYI 青少年創客發明展臺灣選拔賽</td>
          <td>臺灣師範大學等</td>
          <td><b>國中組便利生活類 銀獎</b></td>
          <td><span class="file-path">陽甫國中生活/2023_IEYI銀獎證書.jpg</span></td>
        </tr>
        <tr>
          <td>2021 年</td>
          <td>2021 太平洋盃科技教育競賽</td>
          <td>花蓮縣政府</td>
          <td><b>創意創客組 金獎</b></td>
          <td>花蓮縣教育處官方獲獎名單</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">5. 專業檢定與語文能力 (Certifications & Language)</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 14%;">檢定項目</th>
          <th style="width: 14%;">測驗／發證日期</th>
          <th style="width: 25%;">測驗分數與級別</th>
          <th style="width: 22%;">佐證檔案路徑</th>
          <th>能力水準與實質意義 [已證實]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>多益英語 (TOEIC)</b></td>
          <td>2026/09/11 查詢</td>
          <td><b style="color: #b45309;">總分 945 分【金色證書】</b><br>(聽力 485、閱讀 460)</td>
          <td><span class="file-path">獎狀/各項檢定/20260911_多益945.jpg</span></td>
          <td>近母語水準；流暢參與國際技術研討、全英文論文研讀與跨國專案會議。</td>
        </tr>
        <tr>
          <td><b>全民英檢 中高級</b></td>
          <td>2026/09/04 發證<br>(2026/07/25 考)</td>
          <td><b style="color: #2563eb;">CEFR B2+ 四項測驗全合格</b><br>(證書號: H000068382)</td>
          <td><span class="file-path">獎狀/各項檢定/20260910_GEPT中高級證書.pdf</span></td>
          <td>LTTC 正式證書；聽說讀寫全方位獨立學術研究與流暢學術溝通能力。</td>
        </tr>
        <tr>
          <td><b>APCS 程式先修檢測</b></td>
          <td>2026/01/10</td>
          <td><b style="color: #dc2626;">觀念題 92 分（第 5 級分，滿級）</b><br>實作題 135 分（第 2 級分）</td>
          <td><span class="file-path">獎狀/各項檢定/20260110_APCS成績單.pdf</span></td>
          <td>程式識讀、複雜度與演算法觀念達全國頂尖水準（准考號 115011002）。</td>
        </tr>
        <tr>
          <td><b>AMC12A 數學競賽</b></td>
          <td>2024/11/07</td>
          <td>完成測驗並獲官方參賽證書</td>
          <td><span class="file-path">獎狀/各項檢定/20241107_AMC12A證書.pdf</span></td>
          <td>主動挑戰國際高階數學思維，拓展數理分析廣度與推理穩定度。</td>
        </tr>
        <tr>
          <td><b>校內外英文競賽</b></td>
          <td>2024～2025</td>
          <td>高一演說初賽第1、複賽第4<br>高二英文作文第2、全縣作文甲等</td>
          <td><span class="file-path">獎狀/學業獎狀/20240926_演說第一名.pdf 等</span></td>
          <td>展現優異臨場英語口語表達、論辯台風與結構化寫作實力。</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">6. 體育競技與全人發展 (Athletics & Character)</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 12%;">賽事日期</th>
          <th style="width: 26%;">賽事名稱</th>
          <th style="width: 20%;">代表單位／角色</th>
          <th style="width: 17%;">獲得名次</th>
          <th>佐證檔案路徑 [已證實]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>2026/04/03</td>
          <td>114學年中等學校足球聯賽 (5人制)</td>
          <td>花蓮高中五人制校隊／主力</td>
          <td><b style="color: #dc2626;">全國第五名</b>（勝惠文）</td>
          <td><span class="file-path">獎狀/足球獎狀/20260403_足球聯賽全國第五名.pdf</span></td>
        </tr>
        <tr>
          <td>2025/04/02</td>
          <td>113學年中等學校足球聯賽 (5人制)</td>
          <td>花蓮高中五人制校隊／隊員</td>
          <td><b>全國第六名</b></td>
          <td><span class="file-path">獎狀/足球獎狀/20250402_足球聯賽全國第六名.pdf</span></td>
        </tr>
        <tr>
          <td>2024/11/17</td>
          <td>2024 全國青年盃足球錦標賽公開組</td>
          <td>花蓮高中足球隊／隊員</td>
          <td><b>全國第五名</b></td>
          <td><span class="file-path">獎狀/足球獎狀/20241117_青年盃公開組第五名.pdf</span></td>
        </tr>
        <tr>
          <td>2025/11/07</td>
          <td>花中全校運動會 800 公尺高二男子組</td>
          <td>個人參賽</td>
          <td><b style="color: #b45309;">第二名（銀牌）</b></td>
          <td><span class="file-path">獎狀/足球獎狀/20251107_校運會800m第二名.pdf</span></td>
        </tr>
        <tr>
          <td>2023/03/19</td>
          <td>111學年國中足球聯賽 (乙級決賽)</td>
          <td>花崗國中足球隊（國三隊長）</td>
          <td><b>全國季軍</b>（PK決勝球）</td>
          <td>體育署官方紀錄、決賽戰報、進球影片</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">葉陽甫個人經歷與得獎事蹟總表 • 頁 3 / 4</div>
</div>

<!-- ==================== PAGE 4: 研究經歷與全人特質深度剖析 ==================== -->
<div class="page-container">
  <div>
    <h1 class="doc-title">葉陽甫｜科研探究深化與全人特質解讀</h1>

    <div class="section-h2">7. 科學研究歷程的五個關鍵轉折</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 17%;">研究階段</th>
          <th style="width: 18%;">對應競賽與專案</th>
          <th style="width: 25%;">個人核心技術貢獻</th>
          <th>研究反思與科學素養進階 [已證實]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>起點：需求轉化為原型</b><br>(高二上)</td>
          <td>2026 神通 AI 高中競賽<br>（全國冠軍）</td>
          <td>負責教材結構化剖析、題庫資料庫規劃、Code-as-Content 題目生成至多模態作答之完整資料管線。</td>
          <td>成功將高中職數學教學現場的適性化學習痛點轉譯為可實際運作的 AI 軟體原型。在動態生成題目過程中，首次觀察到 LLM 代碼生成的可靠度缺口。</td>
        </tr>
        <tr>
          <td><b>整合：多模組系統閉環</b><br>(高二下前期)</td>
          <td>第 23 屆育秀盃創意獎<br>（AI 應用類金獎）</td>
          <td>負責多模組系統整合，將 Brain (PPO推薦)、Hands (Code生成) 與 Mouth (Hybrid RAG) 接合為學生可用介面。</td>
          <td>團隊分工清晰（葉陽甫：系統整合與Prompt/Healer；蔡昕諾：PPO；林昕佑：Hybrid RAG），作品具備高度工程完整性與學習閉環，但仍偏向工程功能導向。</td>
        </tr>
        <tr>
          <td><b>轉折：面對批判啟動反思</b><br>(高二下中期)</td>
          <td>第 66 屆東區科學展覽會<br>（優等第二名）</td>
          <td>校內科展獲優勝後代表出征東區科展，負責研究架構、展示系統與現場口頭答辯。</td>
          <td><b>本案關鍵轉折點</b>：現場遭遇評審質疑研究範疇過大、驗證對照組不足。團隊不怨天尤人，坦然承認研究焦點分散，立即啟動嚴格的反思與研究問題收斂。</td>
        </tr>
        <tr>
          <td><b>深化：聚焦邊界與棄權機制</b><br>(高二至高三)</td>
          <td>第 25 屆旺宏科學獎<br>（全國 20 強入圍）</td>
          <td>放棄包山包海的宏大敘事，聚焦 AST Active Healer 邊界實驗，設計棄權演算法、對照組統計檢驗。</td>
          <td>重新檢討早期自建評估指標，改採標準基準測試、pass/fail 與修復率。體認到「真正的科學探究，研究者不只要檢查模型，更要嚴格檢驗自己的評估工具」。</td>
        </tr>
        <tr>
          <td><b>閉環：回歸高職教育現場</b><br>(高二至高三進行中)</td>
          <td>花蓮高商數學課堂場域導入</td>
          <td>協助第一線高職數學教師（陽甫父親）架設雲端環境、配置題庫資料庫並收集學生課堂試用反饋。</td>
          <td>形成「教育需求 → 技術研發 → 競賽洗禮 → 科學修正 → 課堂驗證」之完整閉環，梳理出八大未解問題，確立申請頂大跨域學程的堅定動機。</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h2">8. 核心素養與個人特質摘要</div>
    <table class="detail-table">
      <thead>
        <tr>
          <th style="width: 18%;">特質維度</th>
          <th style="width: 36%;">代表性佐證事實</th>
          <th>大學審查與教授關注重點</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>自律與時間管理</b></td>
          <td>身處普通班自然組，每週維持高強度足球校隊訓練，征戰全國聯賽奪全國前五名；同時維持四學期班排前五，高二段考自我拉回至全校第 19 名。</td>
          <td>證明具備極強的時間顆粒度掌控力與體能耐受力，能兼顧繁重學業與自主研究。</td>
        </tr>
        <tr>
          <td><b>面對挫折的自我修正</b></td>
          <td>東區科展未晉級全國後，不諉過於評審，反思收斂研究問題，補強對照實驗與修復邊界，最終入圍全國頂尖之旺宏科學獎決賽 20 強。</td>
          <td>展現極具價值的「自我修正（Self-Correction）」特質，具備真正科學家的研究潛力。</td>
        </tr>
        <tr>
          <td><b>國際接軌與語言工具力</b></td>
          <td>多益 945 分（金色證書，聽力 485 / 閱讀 460）、GEPT 中高級證書（CEFR B2+ 四項全通過），多次獲全校英文演講與作文優勝。</td>
          <td>外語能力已達流暢閱讀國際學術論文、與海外學者交流與主持專案之母語級水準。</td>
        </tr>
        <tr>
          <td><b>問題驅動的動手實作</b></td>
          <td>因熱愛足球自學爬蟲與資料分析；為解決長者與曬衣痛點製作遮雨棚；因父親教學痛點研發自適應系統與語法修復器。</td>
          <td>每一項專案皆源於真實生活痛點，展現「因問題而自學全新技術」的自驅工程思維。</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="page-footer">葉陽甫個人經歷與得獎事蹟總表 • 頁 4 / 4</div>
</div>

</body>
</html>
"""

# Write HTML to temporary file
html_path = os.path.join(WORKSPACE, "01_master_profile", "_temp_profile.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML template written to:", html_path)

async def convert_to_pdf():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Open the HTML file
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        await page.goto(file_url, wait_until="networkidle")
        
        # 1. Generate the full 4-page PDF
        await page.pdf(
            path=OUTPUT_PDF,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print("Full PDF generated successfully:", OUTPUT_PDF)
        
        # 2. Generate the single-page PDF (Page 1 only)
        await page.pdf(
            path=OUTPUT_SINGLE_PDF,
            format="A4",
            page_ranges="1",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print("Single Page PDF generated successfully:", OUTPUT_SINGLE_PDF)
        
        await browser.close()

asyncio.run(convert_to_pdf())
