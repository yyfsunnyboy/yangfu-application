"""Build Interview Booklet V8 - Academic Clean & Calm Edition (典雅學術·沉穩清爽版).

全面檢查並修訂版本：
- 依據 00_備審資料首頁, 07_東區科展到旺宏入圍, 08_研究介紹, 09_AI學習系統介紹, 英文能力, 高中足球 六份正式備審資料進行事實核對
- 語氣改為高中生本人能自然講解、真誠嚴謹的風格；完全移除誇張修飾詞與刻意對比句
- P1: 保留雙欄六區塊，修訂東區科展優等（未晉級全國）、國中足球聯賽乙組季軍、AST Healer 與 AI 自適應系統準確描述
- P2: 依據 09_系統介紹，詳述父親課堂需求、三項核心功能、規則式自適應複習部分單元實作、真實數據截至 2026/10/04，精簡技術棧為真實落地實作，平實銜接 P3
- P3: 依據 08_研究介紹，簡潔標題避免碰撞；放大流程圖與模型比較圖；12*3*4*5=720 測試公式；720->342->42->9 (2.63%救回率)；更正三種模型名稱（Qwen 4B/9B, Gemini Flash），移除 CodeLlama；如實呈現 MCRI 97.41 綜合分數與決賽獨立測試之邊界反思
- P4: 足球競技修正四項成績（114五人制第5、113五人制第6、青年盃11人制第5、縣運11人制亞軍），FBref 做為跨域程式練習；英文重構為 A 檢定、B 競賽在校表現、C 實際工具運用 三區塊，移除論文閱讀等不實敘述；頁底加入 Demo 與 GitHub 雙 QR Code 與點擊連結
"""
import os
import subprocess
import fitz
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "陽甫調整" / "其他表現資料"
ASSETS = ROOT / "陽甫調整" / "4頁對折本_assets"
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = ROOT / "tmp" / "booklet_v8"
TMP_DIR.mkdir(parents=True, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def build_html():
    def p(fname):
        path = (ASSETS / fname).resolve().as_posix()
        return f"file:///{path}"

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: 210mm 297mm;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  html, body {{
    margin: 0;
    padding: 0;
    width: 210mm;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
    color: #1e293b;
    font-size: 10pt;
    line-height: 1.48;
  }}
  
  .page {{
    width: 210mm;
    height: 297mm;
    page-break-after: always;
    position: relative;
    padding: 11mm 13mm 10mm 13mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    background: #ffffff;
  }}

  /* Top Bar Header */
  .header {{
    border-bottom: 2px solid #0f2942;
    padding-bottom: 5px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .header-left {{
    display: flex;
    flex-direction: column;
    gap: 2.5px;
    max-width: 68%;
  }}
  
  /* Unified Academic Badges */
  .badge-tag {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 8.8pt;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 2px 7px;
    border-radius: 3px;
    width: fit-content;
  }}
  .badge-primary {{
    background: #0f2942;
    color: #ffffff;
  }}
  .badge-sub {{
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #cbd5e1;
  }}

  .page-title {{
    font-size: 15.5pt;
    font-weight: 900;
    color: #0f2942;
    letter-spacing: -0.3px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    line-height: 1.25;
  }}
  .page-subtitle {{
    font-size: 9.6pt;
    color: #475569;
    font-weight: 500;
    line-height: 1.35;
  }}
  .header-right {{
    text-align: right;
    max-width: 32%;
  }}
  
  /* Academic Citation Award Badge */
  .header-award-badge {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #b45309;
    color: #0f2942;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 9.3pt;
    font-weight: 800;
    display: inline-block;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    white-space: nowrap;
  }}
  .header-award-badge.secondary {{
    border-left-color: #1e3a8a;
  }}

  /* Grid Layouts */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
  }}
  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
  }}

  /* Unified Academic Metric Cards */
  .metric-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 2.5px solid #1e3a8a;
    border-radius: 5px;
    padding: 6px 7px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  }}
  .metric-val {{
    font-size: 15.5pt;
    font-weight: 900;
    color: #0f2942;
    line-height: 1.15;
    letter-spacing: -0.2px;
  }}
  .metric-lbl {{
    font-size: 8.6pt;
    color: #64748b;
    margin-top: 2.5px;
    font-weight: 600;
    line-height: 1.25;
  }}

  /* Content Cards */
  .card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 8px 10px;
    margin-bottom: 7px;
  }}
  .card-header {{
    font-size: 10.8pt;
    font-weight: 800;
    color: #0f2942;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .card-header-bar {{
    width: 3.5px;
    height: 13px;
    border-radius: 2px;
    background: #1e3a8a;
  }}

  /* Process Steps */
  .process-step {{
    display: flex;
    gap: 7px;
    margin-bottom: 5px;
    align-items: flex-start;
  }}
  .step-num {{
    background: #0f2942;
    color: #ffffff;
    font-size: 8.5pt;
    font-weight: 800;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1.5px;
  }}
  .step-content {{
    flex: 1;
  }}
  .step-title {{
    font-weight: 800;
    font-size: 10pt;
    color: #0f2942;
  }}
  .step-desc {{
    font-size: 9.3pt;
    color: #475569;
    line-height: 1.4;
  }}

  /* Refined Academic Bridge Cards */
  .bridge-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #1e3a8a;
    border-radius: 5px;
    padding: 8px 11px;
    margin-top: 5px;
  }}
  .bridge-title {{
    font-size: 10.5pt;
    font-weight: 800;
    color: #0f2942;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
  }}

  .p3-bridge-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #1e3a8a;
    border-radius: 5px;
    padding: 8px 11px;
    margin-bottom: 8px;
  }}

  /* Footer */
  .footer {{
    border-top: 1px solid #cbd5e1;
    padding-top: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 8.8pt;
    color: #64748b;
    font-weight: 500;
  }}

  /* Image Containers */
  .img-box {{
    border-radius: 5px;
    overflow: hidden;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
  }}
  .img-box img {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .img-caption {{
    font-size: 8.6pt;
    color: #475569;
    text-align: center;
    padding: 3px 5px;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    font-weight: 600;
    line-height: 1.3;
  }}

  /* Page 1 Specific Styling */
  #page1 {{
    padding: 10mm 13mm 9mm 13mm;
  }}
  .p1-top-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
    margin-bottom: 6px;
    font-size: 9pt;
    color: #64748b;
  }}
  .p1-top-badge {{
    background: #0f2942;
    color: #ffffff;
    font-weight: 700;
    font-size: 8.8pt;
    padding: 1.5px 7px;
    border-radius: 3px;
    letter-spacing: 0.3px;
  }}
  .p1-header-main {{
    display: flex;
    gap: 13px;
    align-items: center;
    margin-bottom: 5px;
  }}
  .p1-header-photo {{
    width: 24mm;
    height: 30mm;
    object-fit: cover;
    border-radius: 3px;
    border: 1px solid #cbd5e1;
    flex-shrink: 0;
  }}
  .p1-header-info {{
    flex: 1;
    min-width: 0;
  }}
  .p1-header-title-row {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 2.5px;
  }}
  .p1-name-text {{
    font-size: 22pt;
    font-weight: 900;
    color: #0f2942;
    letter-spacing: 0.5px;
    line-height: 1.1;
  }}
  .p1-school-text {{
    font-size: 12pt;
    font-weight: 700;
    color: #334155;
    margin-left: 8px;
  }}
  .p1-domain-tag {{
    font-size: 9.8pt;
    font-weight: 700;
    color: #1e3a8a;
    white-space: nowrap;
  }}
  .p1-positioning-statement {{
    font-size: 10pt;
    color: #334155;
    font-weight: 600;
    background: #f8fafc;
    border-left: 3.5px solid #0f2942;
    padding: 2.5px 7px;
    margin-bottom: 4px;
    line-height: 1.3;
    white-space: nowrap;
  }}
  .p1-badge-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3.5px 7px;
  }}
  .p1-badge-item {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #1e3a8a;
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 9.2pt;
    color: #0f2942;
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .p1-badge-item.gold {{
    border-left-color: #b45309;
  }}
  .hl-blue {{
    color: #1e3a8a;
    font-weight: 800;
  }}
  .hl-gold {{
    color: #b45309;
    font-weight: 800;
  }}
  .p1-header-divider {{
    height: 1.5px;
    background: #0f2942;
    margin-top: 2px;
    margin-bottom: 7px;
  }}
  .p1-columns-container {{
    display: grid;
    grid-template-columns: 46% 51.5%;
    gap: 2.5%;
  }}
  .p1-col-left {{
    display: flex;
    flex-direction: column;
    gap: 13px;
    border-right: 1px solid #cbd5e1;
    padding-right: 11px;
  }}
  .p1-col-right {{
    display: flex;
    flex-direction: column;
    gap: 13px;
    padding-left: 2px;
  }}
  .p1-section-block {{
    display: flex;
    flex-direction: column;
  }}
  .p1-sec-heading {{
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 12.2pt;
    font-weight: 800;
    color: #0f2942;
    padding-bottom: 2.5px;
    border-bottom: 1.5px solid #0f2942;
    margin-bottom: 5.5px;
  }}
  .p1-sec-heading-symbol {{
    font-size: 9.8pt;
    color: #1e3a8a;
  }}
  .p1-item-list {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 5.6px;
  }}
  .p1-item-row {{
    font-size: 10.3pt;
    line-height: 1.38;
    color: #334155;
    display: flex;
    align-items: baseline;
    gap: 4px;
  }}
  .p1-bullet {{
    flex-shrink: 0;
    width: 8.5px;
    font-weight: 700;
    color: #1e3a8a;
    line-height: 1.38;
  }}
  .p1-item-content {{
    flex: 1;
    line-height: 1.38;
  }}
  .p1-item-title {{
    font-weight: 700;
    color: #0f2942;
  }}
  .p1-award-item {{
    margin-bottom: 5.5px;
    font-size: 10.2pt;
    color: #334155;
  }}
  .p1-award-title {{
    font-size: 11pt;
    font-weight: 800;
    color: #0f2942;
    line-height: 1.35;
  }}
  .p1-award-desc {{
    padding-left: 6px;
    color: #475569;
    font-size: 9.8pt;
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-top: 2px;
  }}
  .p1-sub-bullet-row {{
    display: flex;
    align-items: baseline;
    gap: 4px;
    line-height: 1.36;
  }}
  .p1-sub-bullet-row .p1-bullet {{
    width: 8.5px;
    line-height: 1.36;
  }}
  .p1-sub-bullet-row .p1-bullet-content {{
    flex: 1;
    line-height: 1.36;
  }}
  .p1-tech-item {{
    margin-bottom: 5.5px;
    font-size: 10.1pt;
    color: #334155;
  }}
  .p1-tech-title {{
    font-weight: 800;
    color: #0f2942;
    font-size: 10.5pt;
    display: flex;
    align-items: baseline;
    gap: 4px;
    line-height: 1.35;
  }}
  .p1-tech-desc {{
    color: #475569;
    padding-left: 12.5px;
    text-align: left;
    font-size: 10pt;
    line-height: 1.38;
    margin-top: 2px;
  }}
  .p1-tech-links {{
    margin-top: 3.5px;
    padding-left: 12.5px;
    display: flex;
    gap: 14px;
    font-size: 9.6pt;
    font-weight: 700;
  }}
  .p1-tech-links a {{
    color: #1e3a8a;
    text-decoration: underline;
  }}
</style>
</head>
<body>

<!-- PAGE 1: Personal Overview & Master Profile -->
<div class="page" id="page1">
  <div>
    <!-- Top Meta Navigation -->
    <div class="p1-top-meta">
      <div>
        <span>特殊選才面試資料</span> ｜ <b style="color:#0f2942;">個人總覽</b> ｜ <span>高中學習與成果摘要</span>
      </div>
      <div class="p1-top-badge">
        國立花蓮高級中學
      </div>
    </div>

    <!-- Header Main Area: Photo + Name + Tags + 4 Key Badges -->
    <div class="p1-header-main">
      <img src="{p('YEH YANG FU.jpg')}" class="p1-header-photo" alt="葉陽甫個人證件照">
      <div class="p1-header-info">
        <div class="p1-header-title-row">
          <div>
            <span class="p1-name-text">葉陽甫</span>
            <span class="p1-school-text">國立花蓮高級中學 普通科</span>
          </div>
          <span class="p1-domain-tag">特殊選才備審核心總覽</span>
        </div>
        <div class="p1-positioning-statement">
          資訊工程 · 數學自適應系統實作 · 程式生成局部修復研究 · 足球運動競技
        </div>
        <!-- 4 Key Verified Badges -->
        <div class="p1-badge-grid">
          <div class="p1-badge-item gold" title="育秀盃創意獎 全國金獎 (AI應用類 · 10萬元)">
            🥇 育秀盃創意獎【<span class="hl-gold">全國金獎</span>】(AI類 · 10萬元)
          </div>
          <div class="p1-badge-item gold" title="旺宏科學獎 全國決賽20強 (資訊領域僅4件)">
            🏅 旺宏科學獎【<span class="hl-gold">全國決賽20強</span>】(資訊領域僅4件)
          </div>
          <div class="p1-badge-item" title="全國五人制足球聯賽 全國第 5 名 (校隊主力)">
            ⚽ 全國五人制足球聯賽【<span class="hl-blue">全國第 5 名</span>】(校隊主力)
          </div>
          <div class="p1-badge-item" title="TOEIC 945（金色證書）｜ APCS 觀念 5 級分">
            📜 <span class="hl-blue">TOEIC 945</span>（金色證書）｜ <span class="hl-blue">APCS 觀念 5 級分</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Divider -->
    <div class="p1-header-divider"></div>
  </div>

  <!-- Two-Column Main Content (46% | 51.5%) -->
  <div class="p1-columns-container">
    <!-- Left Column: Academic, English, Soccer -->
    <div class="p1-col-left">
      <!-- 1. 學業與基礎能力 -->
      <div class="p1-section-block">
        <div class="p1-sec-heading">
          <span class="p1-sec-heading-symbol">◆</span>
          <span>學業與基礎能力</span>
        </div>
        <div class="p1-item-list">
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">總體表現</span>：4學期班排前五，學業平均 <b>84.2</b><br><span style="white-space:nowrap;">（年排 24/320 · <span class="hl-blue">前 8%</span>）</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">數理資工</span>：<span style="white-space:nowrap;">資訊科 <span class="hl-blue">前 6%</span> ｜</span> <span style="white-space:nowrap;">數學科 <span class="hl-blue">前 6%</span> ｜</span><br><span style="white-space:nowrap;">化學科 <span class="hl-blue">前 4%</span> ｜</span> <span style="white-space:nowrap;">地科 <span class="hl-blue">前 2%</span></span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">校內選修</span>：Arduino 程式設計 <b>94 分</b>（第 2 名）、<br><span style="white-space:nowrap;">Python <b>90 分</b>（第 4 名）</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">數理競賽</span>：JHMC 國中數學競賽<br><span style="white-space:nowrap;"><b>團體一等獎／個人優良獎</b></span> ｜ 更生盃 <b>銀牌</b>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. 外語溝通能力 -->
      <div class="p1-section-block">
        <div class="p1-sec-heading">
          <span class="p1-sec-heading-symbol">◆</span>
          <span>外語溝通能力</span>
        </div>
        <div class="p1-item-list">
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">TOEIC 945 分</span>（<span class="hl-gold">金色證書</span>）：<br><span style="white-space:nowrap;">聽力 <b>485</b> ／ 閱讀 <b>460</b></span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">全民英檢（GEPT）中高級</span>：<br><span style="white-space:nowrap;">聽、說、讀、寫四項全數通過</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">在校英文成績</span>：高一二平均 <b>91 分</b>（<span class="hl-blue">前 4%</span>），<br><span style="white-space:nowrap;">高二下 <b>96 分</b></span>（年排第 7 · <span class="hl-blue">前 2%</span>）
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">語文競賽成果</span>：花蓮縣英文作文高中組 <b>甲等</b> ｜<br><span style="white-space:nowrap;">校內作文 <b>第 2 名</b></span><br>校內英語演說 <span style="white-space:nowrap;">初賽第 1 名</span>、<span style="white-space:nowrap;">全校複賽第 4 名</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">國中語文延續</span>：國中英文作文 <b>優等</b> ｜<br><span style="white-space:nowrap;">英語讀者劇場 <b>特優</b></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. 足球競技與長期投入 -->
      <div class="p1-section-block">
        <div class="p1-sec-heading">
          <span class="p1-sec-heading-symbol">◆</span>
          <span>足球競技與長期投入</span>
        </div>
        <div class="p1-item-list">
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">全國五人制足球聯賽</span>：<span style="white-space:nowrap;">114 學年 <span class="hl-gold">全國第 5 名</span></span> ｜<br><span style="white-space:nowrap;">113 學年 <span class="hl-gold">全國第 6 名</span></span><br><span style="color:#475569;">（連續兩年符合教育部運動績優甄試資格）</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">全國青年盃公開組</span>：<span class="hl-gold">全國第 5 名</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">花蓮縣運足球</span>：<span style="white-space:nowrap;">2025 社會男子組 <b>亞軍</b></span> ｜<br><span style="white-space:nowrap;">2022 國中男子組 <b>冠軍</b></span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">球隊經歷</span>：花蓮高中五人制校隊主力球員<br><span style="white-space:nowrap;">（背號 42 號）</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">體能表現</span>：校運 800m <b>第 2 名</b> ｜ <span style="white-space:nowrap;">體育成績 <b>84.5 分</b></span><br><span style="white-space:nowrap;">（年排 13/320 · <span class="hl-blue">前 4%</span>）</span>
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">國中運動延續</span>：國中足球聯賽 <span class="hl-blue">全國乙組季軍</span> ｜<br>花崗國中男足隊長（參與全國甲級聯賽）
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Research Awards, Core Projects, Engineering Exploration -->
    <div class="p1-col-right">
      <!-- 1. 代表性科研成果 -->
      <div class="p1-section-block">
        <div class="p1-sec-heading">
          <span class="p1-sec-heading-symbol">◆</span>
          <span>代表性科研成果</span>
        </div>
        <div class="p1-award-item">
          <div class="p1-award-title">1. 第 25 屆 旺宏科學獎【<span class="hl-gold">全國決賽 20 強</span>】</div>
          <div class="p1-award-desc">
            <div class="p1-sub-bullet-row">
              <span class="p1-bullet">•</span>
              <div class="p1-bullet-content">全領域 846 件作品評選，資訊領域全國僅 4 件入選決賽</div>
            </div>
            <div class="p1-sub-bullet-row">
              <span class="p1-bullet">•</span>
              <div class="p1-bullet-content">研究核心：小型語言模型之 AST 程式碼局部錯誤修復研究</div>
            </div>
          </div>
        </div>
        <div class="p1-award-item">
          <div class="p1-award-title">2. 第 23 屆 育秀盃創意獎【<span class="hl-gold">全國金獎</span>】</div>
          <div class="p1-award-desc">
            <div class="p1-sub-bullet-row">
              <span class="p1-bullet">•</span>
              <div class="p1-bullet-content">高中職 AI 應用類金獎（獎金 10 萬元），作品為 AI 自適應輔助學習系統。</div>
            </div>
          </div>
        </div>
        <div class="p1-award-item">
          <div class="p1-award-title">3. 2026 神通 AI 數位學院扶輪盃【<span class="hl-gold">全國冠軍</span>】</div>
          <div class="p1-award-desc">
            <div class="p1-sub-bullet-row">
              <span class="p1-bullet">•</span>
              <div class="p1-bullet-content">全國高中 AI 應用競賽 第一名</div>
            </div>
          </div>
        </div>
        <div class="p1-award-item" style="margin-bottom:0;">
          <div class="p1-award-title">4. 第 66 屆 東區科展【<span class="hl-blue">電腦與資訊學科優等</span>】</div>
          <div class="p1-award-desc">
            <div class="p1-sub-bullet-row">
              <span class="p1-bullet">•</span>
              <div class="p1-bullet-content">高級中等學校分區科展（未晉級全國科展）</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. 核心技術架構與專案 -->
      <div class="p1-section-block">
        <div class="p1-sec-heading">
          <span class="p1-sec-heading-symbol">◆</span>
          <span>核心技術架構與專案</span>
        </div>
        <div class="p1-tech-item">
          <div class="p1-tech-title">
            <span class="p1-bullet">•</span>
            <span class="p1-bullet-content">AST Active Healer 程式修復機制：</span>
          </div>
          <div class="p1-tech-desc">
            以固定規則修正 AI 產生的程式中部分能明確判斷的錯誤，並透過測試確認哪些情況能修復、哪些無法修復。
          </div>
        </div>
        <div class="p1-tech-item" style="margin-bottom:0;">
          <div class="p1-tech-title">
            <span class="p1-bullet">•</span>
            <span class="p1-bullet-content">AI 自適應輔助學習系統：</span>
          </div>
          <div class="p1-tech-desc">
            由 AI 建立可重複使用的 Python 出題程式，驗證後產生變化題與答案，並結合數學判題、AI 助教及學習紀錄。系統已在花蓮高商兩個班級使用，部分單元提供規則式自適應複習。
          </div>
          <div class="p1-tech-links">
            <a href="https://mathb.math-adaptive.org/review-demo" target="_blank">▶ 線上 Demo 展示頁 ↗</a>
            <a href="https://github.com/yyfsunnyboy/Mathproject_tvet_mathB" target="_blank">▶ 專案 GitHub ↗</a>
          </div>
        </div>
      </div>

      <!-- 3. 程式實作與工程探究 -->
      <div class="p1-section-block">
        <div class="p1-sec-heading">
          <span class="p1-sec-heading-symbol">◆</span>
          <span>程式實作與工程探究</span>
        </div>
        <div class="p1-item-list">
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">APCS 大學程式先修檢測</span>：觀念 <b>92.5 分</b>（<span class="hl-gold">5 級分 · <span style="white-space:nowrap;">前 3.7%</span></span>） ｜ 實作 <b>135 分</b>（2 級分）
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">IEYI 世界青少年發明展</span>：2023 臺灣選拔賽【<span class="hl-gold">銀獎</span>】
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">資訊學科能力競賽</span>：校內初賽【<b>佳作</b>】
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">學習歷程課程成果</span>：Arduino 程式設計【<span class="hl-gold">優等</span>】
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">跨領域數據分析實作</span>：使用 Python 抓取 FBref 足球數據進行分析練習
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">東部物理 IYPT 科學營</span>：實驗報告【<b>第 3 名</b>】
            </div>
          </div>
          <div class="p1-item-row">
            <span class="p1-bullet">•</span>
            <div class="p1-item-content">
              <span class="p1-item-title">第 65 屆校內科展</span>（工程學科(二)）：【<b>優勝</b>】<span style="white-space:nowrap;">（未晉級東區）</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span>葉陽甫 · 國立花蓮高級中學 ｜ 特殊選才面試精華摺頁冊</span>
    <span>第 1 頁 · 個人總覽 (封面)</span>
  </div>
</div>

<!-- PAGE 2: AI Adaptive Learning System (Engineering Project) -->
<div class="page" id="page2">
  <div>
    <!-- Top Header -->
    <div class="header">
      <div class="header-left">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-primary">02 / 系統工程篇</span>
          <span class="badge-tag badge-sub">跨頁主線 (上) · 系統落地</span>
        </div>
        <h1 class="page-title">
          AI 自適應輔助學習系統
        </h1>
        <div class="page-subtitle">從數學課堂的實際需求出發，逐步開發並投入教學使用的系統。</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge secondary">🏆 神通扶輪盃 全國第一名</div>
        <div class="header-award-badge" style="margin-top:3px;">🥇 育秀盃創意獎 全國金獎</div>
      </div>
    </div>

    <!-- 4 Key Metrics (Grounded Factual Style) -->
    <div class="grid-4" style="margin-bottom: 8px;">
      <div class="metric-card">
        <div class="metric-val">2 個班級</div>
        <div class="metric-lbl">課堂實際使用班級</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">50 名</div>
        <div class="metric-lbl">正式課堂學生帳號</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">1,224 次</div>
        <div class="metric-lbl">系統累積作答筆數</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">67%</div>
        <div class="metric-lbl">學生平均答對率</div>
      </div>
    </div>
    <div style="text-align:center; font-size:8.4pt; color:#64748b; margin-top:-4px; margin-bottom:8px;">
      （數據統計截至 2026/10/04；平均答對率為目前課堂作答現況，學習成效仍持續驗證中）
    </div>

    <!-- Main Two Column Grid -->
    <div class="grid-2" style="margin-bottom: 8px;">
      <!-- Left Column: Core System Pipeline & Role -->
      <div style="display:flex; flex-direction:column; justify-content:space-between;">
        <div class="card" style="padding:6px 10px;">
          <div class="card-header" style="margin-bottom:3px;">
            <div class="card-header-bar"></div>
            開發起點與課堂需求
          </div>
          <div style="font-size:9.1pt; color:#334155; line-height:1.4; text-align:justify; margin-bottom:4px;">
            我的父親在花蓮高商教授數學。開發初期，我先了解他在實際教學中遇到的問題，整理出四項需求：
          </div>

          <div style="display:flex; flex-direction:column; gap:3.5px; margin-bottom:5px;">
            <div>
              <div style="font-size:8.9pt; font-weight:800; color:#0f2942; line-height:1.3;">
                <span style="color:#1e3a8a;">01｜</span>教材整理費時
              </div>
              <div style="font-size:8.4pt; color:#475569; line-height:1.32; letter-spacing:-0.18px;">
                數學教材包含公式、圖形與大量例題，逐題輸入系統相當費時。
              </div>
            </div>

            <div>
              <div style="font-size:8.9pt; font-weight:800; color:#0f2942; line-height:1.3;">
                <span style="color:#1e3a8a;">02｜</span>固定題庫難以反覆練習
              </div>
              <div style="font-size:8.4pt; color:#475569; line-height:1.32; letter-spacing:-0.18px;">
                同一題目做過後容易記住答案，需要能持續產生變化題的方式。
              </div>
            </div>

            <div>
              <div style="font-size:8.9pt; font-weight:800; color:#0f2942; line-height:1.3;">
                <span style="color:#1e3a8a;">03｜</span>學生的學習程度不同
              </div>
              <div style="font-size:8.4pt; color:#475569; line-height:1.32; letter-spacing:-0.18px;">
                同班學生可能卡在不同數學概念，需要依作答情況安排補強。
              </div>
            </div>

            <div>
              <div style="font-size:8.9pt; font-weight:800; color:#0f2942; line-height:1.3;">
                <span style="color:#1e3a8a;">04｜</span>數學作答不只是輸入文字
              </div>
              <div style="font-size:8.5pt; color:#475569; line-height:1.34; letter-spacing:-0.15px;">
                學生需要輸入公式、手寫計算與作圖，普通文字表單並不適合。
              </div>
            </div>
          </div>
        </div>

        <div class="card" style="padding:8px 10px;">
          <div class="card-header">
            <div class="card-header-bar"></div>
            三項主要功能
          </div>
          <div class="process-step">
            <div class="step-num">1</div>
            <div class="step-content">
              <div class="step-title">教材整理與匯入</div>
              <div class="step-desc">將 Word、PDF 數學教材整理成章節、技能與例題，並保留題目來源。</div>
            </div>
          </div>
          <div class="process-step">
            <div class="step-num">2</div>
            <div class="step-content">
              <div class="step-title">AI 建立出題程式</div>
              <div class="step-desc">先讓 AI 產生 Python 出題程式，驗證通過後，再由程式反覆產生不同數值的同類型題目與答案。</div>
            </div>
          </div>
          <div class="process-step" style="margin-bottom:0;">
            <div class="step-num">3</div>
            <div class="step-content">
              <div class="step-title">學生練習與回饋</div>
              <div class="step-desc">學生可以在系統上解題，程式負責判斷答案，AI 助教提供提示，作答紀錄供學生與老師查看。</div>
            </div>
          </div>
        </div>

        <div class="card" style="margin-bottom:0; padding:8px 10px;">
          <div class="card-header" style="font-size:10.2pt;">
            <div class="card-header-bar"></div>
            <span>規則式自適應複習｜根據作答紀錄安排補強</span>
          </div>
          <div style="background:#f1f5f9; border:1px solid #e2e8f0; padding:4px 8px; border-radius:4px; font-size:8.6pt; color:#1e293b; text-align:center; font-weight:700; line-height:1.45; margin-bottom:5px;">
            學生作答 → 更新技能能力值與錯誤紀錄 → 判斷卡點 →<br>前置技能練習 → 返回原進度
          </div>
          <div style="font-size:9.2pt; color:#334155; line-height:1.45; text-align:justify;">
            系統記錄每道題對應的數學技能、作答結果與時間，藉此整理學生的學習狀態。當技能表現符合預設卡點條件時，安排前置技能練習；達到補救條件後，再返回原本進度。目前僅在部分單元實作，跨單元擴充與學習成效仍待驗證。
          </div>
        </div>
      </div>

      <!-- Right Column: Visual Evidence & Screenshot -->
      <div style="display:flex; flex-direction:column; gap:6px;">
        <div class="img-box" style="margin-bottom:0;">
          <img src="{p('ai_student_practice_screen.png')}" style="height:172px; width:100%; object-fit:cover; object-position:top; display:block;" alt="學生線上解題與 AI 助教介面">
          <div class="img-caption" style="padding:2.5px 5px; font-size:8.3pt;">▲ 真實正式系統：學生線上解題、即時數理判題與 AI 助教引導（mathb.math-adaptive.org）</div>
        </div>

        <div class="grid-2" style="gap:6px;">
          <div class="img-box" style="margin-bottom:0;">
            <img src="{p('rotary_award_photo.png')}" style="height:86px; width:100%; object-fit:cover; object-position:center; background:#ffffff;" alt="神通扶輪盃第一名頒獎照片">
            <div class="img-caption" style="padding:2px 4px; font-size:8.2pt;">▲ 神通扶輪盃 全國第一名</div>
          </div>
          <div class="img-box" style="margin-bottom:0;">
            <img src="{p('yuxiu_award_photo.png')}" style="height:86px; width:100%; object-fit:cover; object-position:center 70%; background:#ffffff;" alt="育秀盃金獎頒獎照片">
            <div class="img-caption" style="padding:2px 4px; font-size:8.2pt;">▲ 育秀盃創意獎 全國金獎</div>
          </div>
        </div>

        <div class="card" style="background:#f8fafc; border:1px solid #cbd5e1; margin-bottom:0; padding:6.5px 10px;">
          <div class="card-header" style="font-size:10.2pt; margin-bottom:1px; display:flex; align-items:center; gap:5px;">
            <div class="card-header-bar"></div>
            <span style="color:#0f2942; font-weight:800;">葉陽甫 ｜ 個人主要負責的系統工程</span>
          </div>
          <div style="font-size:8.2pt; color:#64748b; margin-top:-1px; margin-bottom:5.5px; padding-left:8.5px;">
            涵蓋系統架構、教材處理、程式化出題、學生互動與部署維護
          </div>

          <div style="display:flex; flex-direction:column; gap:5.5px;">
            <div>
              <div style="font-size:9.2pt; font-weight:800; color:#0f2942; line-height:1.32;">
                <span style="color:#1e3a8a;">01｜</span>教材匯入與結構化整理
              </div>
              <div style="font-size:8.8pt; color:#475569; line-height:1.36; padding-left:1px;">
                將 Word／PDF 教材整理為章節、技能與題目資料。
              </div>
            </div>

            <div>
              <div style="font-size:9.2pt; font-weight:800; color:#0f2942; line-height:1.32;">
                <span style="color:#1e3a8a;">02｜</span>程式即內容（Code-as-Content）
              </div>
              <div style="font-size:8.8pt; color:#475569; line-height:1.36; padding-left:1px;">
                建立 AI 產生 Python 出題程式及驗證流程，支援反覆變題。
              </div>
            </div>

            <div>
              <div style="font-size:9.2pt; font-weight:800; color:#0f2942; line-height:1.32;">
                <span style="color:#1e3a8a;">03｜</span>多模態數學作答介面
              </div>
              <div style="font-size:8.8pt; color:#475569; line-height:1.36; padding-left:1px;">
                整合公式輸入、手寫畫布、作圖互動與 AI 助教提示。
              </div>
            </div>

            <div>
              <div style="font-size:9.2pt; font-weight:800; color:#0f2942; line-height:1.32;">
                <span style="color:#1e3a8a;">04｜</span>數學判題與程式驗證
              </div>
              <div style="font-size:8.8pt; color:#475569; line-height:1.36; padding-left:1px;">
                使用 SymPy 驗證數學答案，並建立程式測試流程。
              </div>
            </div>

            <div>
              <div style="font-size:9.2pt; font-weight:800; color:#0f2942; line-height:1.32;">
                <span style="color:#1e3a8a;">05｜</span>正式部署與維護
              </div>
              <div style="font-size:8.8pt; color:#475569; line-height:1.36; padding-left:1px;">
                負責資料庫、家用主機部署及課堂問題排除。
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- GROUNDED ENGINEERING REALITIES -->
    <div class="card" style="padding:7px 10px; margin-bottom:8px; background:#f8fafc; border:1px solid #cbd5e1;">
      <div class="card-header" style="margin-bottom:4px; justify-content:space-between;">
        <div style="display:flex; align-items:center; gap:6px;">
          <div class="card-header-bar"></div>
          <span>課堂落地工程實作與問題修正</span>
        </div>
        <span style="font-size:8.8pt; color:#334e68; font-weight:700;">真實使用回饋 · 持續測試修訂</span>
      </div>
      <div class="grid-3" style="font-size:9.2pt; line-height:1.38; gap:8px;">
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 7px;">
          <b style="color:#0f2942;">1. 題目規格與回歸測試</b><br>
          課堂曾遇到題目參數缺漏、變題超出合理範圍等問題，因此加入出題程式測試，減少相同錯誤再次出現。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 7px;">
          <b style="color:#0f2942;">2. 數理答案等價判定</b><br>
          使用 Python 與 SymPy 判斷分數、根號、小數及區間等答案是否等價，減少直接比對文字造成的誤判。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:4px; padding:5px 7px;">
          <b style="color:#0f2942;">3. 書房主機與外部連線</b><br>
          正式主機設於家中書房，透過 HiNet 與 Cloudflare Tunnel 對外提供服務，讓學校師生能連線使用。
        </div>
      </div>
    </div>

    <!-- Bridge to P.3: Narrative Link -->
    <div class="bridge-card" style="padding:8px 11px;">
      <div class="bridge-title" style="margin-bottom:4px;">
        <span>⚡ 銜接研究：從出題系統的成本與錯誤，延伸為程式碼修復研究</span>
        <span style="font-size:9.5pt; font-weight:800; color:#1e3a8a;">接續右頁研究 ➔</span>
      </div>
      <div style="font-size:9.5pt; color:#334155; line-height:1.45; text-align:justify;">
        在開發出題系統時，我發現每次使用雲端 AI 產生程式都會增加成本。因此開始測試本地小型模型，但它產生的程式<span style="white-space:nowrap;">常出現格式、函式名稱</span>或其他局部錯誤。這讓我進一步研究：<b>哪些錯誤能用固定規則修正，哪些仍需要模型重新處理？</b>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span>葉陽甫 · 國立花蓮高級中學 ｜ 特殊選才面試精華摺頁冊</span>
    <span>第 2 頁 · 系統工程篇 (跨頁左面)</span>
  </div>
</div>

<!-- PAGE 3: AST Active Healer Research (Scientific Research) -->
<div class="page" id="page3">
  <div>
    <!-- Top Header -->
    <div class="header">
      <div class="header-left" style="max-width: 62%;">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-primary">03 / 科學研究篇</span>
          <span class="badge-tag badge-sub">跨頁主線 (下) · 深化科研</span>
        </div>
        <h1 class="page-title" style="font-size: 12.8pt; letter-spacing: -0.4px;">
          AST Active Healer｜AI 生成程式碼的局部錯誤修復研究
        </h1>
        <div class="page-subtitle">研究哪些程式錯誤能用固定規則修正，以及這種方法的限制。</div>
      </div>
      <div class="header-right" style="max-width: 37%;">
        <div class="header-award-badge">🏅 第25屆旺宏科學獎 全國決賽20強</div>
        <div class="header-award-badge secondary" style="margin-top:3px;">🎖️ 第66屆東區科展 電腦與資訊學科優等</div>
      </div>
    </div>

    <!-- P3 Top Connecting Box -->
    <div class="p3-bridge-card" style="padding:7px 10px; margin-bottom:8px;">
      <div style="font-size:10.5pt; font-weight:800; color:#0f2942; display:flex; justify-content:space-between; margin-bottom:2.5px;">
        <span>🔬 研究問題意識與出發點</span>
        <span style="font-size:9.2pt; color:#1e3a8a; font-weight:700;">承接左頁出題系統問題 ◄</span>
      </div>
      <div style="font-size:9.5pt; color:#334155; line-height:1.42; text-align:justify;">
        本地小模型產生 Python 程式時，經常出現格式、函式介面或局部結構錯誤。我嘗試設計固定規則修復器，只修改能<span style="white-space:nowrap;">明確判定</span>的部分，再透過測試確認是否真的修好。（AST 抽象語法樹：用來分析與檢查程式結構的樹狀資料表示法）。
      </div>
    </div>

    <!-- Core Mechanism Diagram & Benchmark Chart (Side-by-Side, Enlarged) -->
    <div class="grid-2" style="margin-bottom: 8px; align-items: stretch;">
      <!-- Left: AST Active Healer Flowchart -->
      <div class="card" style="padding: 7px 9px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 4px; justify-content: space-between; align-items: flex-start;">
          <div style="display: flex; align-items: flex-start; gap: 5px;">
            <div class="card-header-bar" style="margin-top: 3px;"></div>
            <span style="font-size: 10.5pt; font-weight: 800; line-height: 1.25;">三步驟修復機制<br><span style="white-space:nowrap;">（答案盲與固定規則）</span></span>
          </div>
          <span style="font-size: 8.4pt; color: #475569; background:#f1f5f9; padding:1.5px 5px; border-radius:3px; font-weight: 700; white-space:nowrap; margin-top:2px;">能確定才修 · 不能確定不修改</span>
        </div>
        <div class="img-box" style="border: 1px solid #e2e8f0; margin-bottom: 4px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff;">
          <img src="{p('healer_blind_repair_rules.png')}" style="height: 200px; width: 100%; object-fit: contain;" alt="AST Healer 答案盲修復與固定規則流程圖">
        </div>
        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 4px 7px; font-size: 8.7pt; color: #334155; line-height: 1.34;">
          <div style="margin-bottom:3px;">
            <b style="color:#0f2942;">① 檢查原始失敗程式</b><br>
            不讀取正確答案，逐筆檢查失敗案例。
          </div>
          <div style="margin-bottom:3px;">
            <b style="color:#0f2942;">② 依固定規則修改</b><br>
            只有修法明確時才修改局部程式；無法確定時不修改。
          </div>
          <div>
            <b style="color:#0f2942;">③ 重新測試</b><br>
            使用相同測試，確認程式是否由失敗轉為通過。
          </div>
        </div>
      </div>

      <!-- Right: Benchmark Experiment Chart -->
      <div class="card" style="padding: 7px 9px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 4px; justify-content: space-between; align-items: center;">
          <div style="display: flex; align-items: center; gap: 5px;">
            <div class="card-header-bar"></div>
            <span style="font-size: 10.5pt; font-weight: 800; white-space:nowrap;">正式測試與模型表現</span>
          </div>
          <span style="font-size: 8.4pt; color: #475569; background:#f1f5f9; padding:1.5px 5px; border-radius:3px; font-weight: 700; white-space:nowrap;">正式保留測試｜720 筆</span>
        </div>
        <div class="img-box" style="border: 1px solid #e2e8f0; margin-bottom: 4px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff;">
          <img src="{p('healer_chart_user.png')}" style="height: 200px; width: 100%; object-fit: contain;" alt="三種模型在四種 Prompt 條件下的原始通過率與 Healer 新增救援">
        </div>
        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 4.5px 7px; font-size: 8.9pt; color: #334155; line-height: 1.35;">
          <b>模型與條件觀察</b>：測試三種模型（<span style="white-space:nowrap;">Qwen 3.5 4B</span>、<span style="white-space:nowrap;">Qwen 3.5 9B</span>、<span style="white-space:nowrap;">Gemini 3.5 Flash</span>）<br>在四種 Prompt 下的表現；342 筆失敗中，42 筆觸發修復規則，9 筆安全救回<span style="white-space:nowrap;">（救回率 2.63%）</span>。
        </div>
      </div>
    </div>

    <!-- 4 Rigorous Benchmark Metrics with Formula -->
    <div style="background:#f1f5f9; border:1px solid #cbd5e1; border-radius:4px; padding:4px 8px; font-size:8.8pt; color:#0f2942; font-weight:700; text-align:center; margin-bottom:6px; line-height:1.4;">
      <span style="color:#475569; font-weight:600;">Math16 資料集：4 題用於規則開發，其餘 12 題保留為正式獨立測試</span><br>
      <span style="white-space:nowrap;">12 題 × 3 種模型 × 4 種 Prompt × 5 組隨機種子</span> ＝ <span style="white-space:nowrap;"><b>720 筆正式測試</b></span>
    </div>

    <div class="grid-4" style="margin-bottom: 5px;">
      <div class="metric-card">
        <div class="metric-val">720 筆</div>
        <div class="metric-lbl">保留正式測試單元</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">342 筆</div>
        <div class="metric-lbl">原始生成失敗案例</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">42 筆</div>
        <div class="metric-lbl">觸發修復規則修改</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">9 筆</div>
        <div class="metric-lbl">失敗轉為通過 (救回率 2.63%)</div>
      </div>
    </div>
    <div style="text-align:center; font-size:8.3pt; color:#64748b; margin-bottom:8px;">
      註：救回率 2.63%（9 ÷ 342）為原始失敗案例的救回比例，非整體生成成功率；42 筆實際修改案例中轉為通過的比例為 21.4%（9 ÷ 42）。
    </div>

    <!-- Two Column Reflection and Science Spirit -->
    <div class="grid-2" style="margin-bottom: 8px;">
      <!-- Left: Research Turning Point -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:8px 10px;">
        <div>
          <div class="card-header">
            <div class="card-header-bar"></div>
            研究歷程：從初版指標到決賽重新驗證
          </div>
          <div style="font-size:9.2pt; color:#334155; line-height:1.44; text-align:justify;">
            <p style="margin:0 0 3px 0;">初版研究使用自訂 MCRI 指標評估程式與數學品質，最高階段的整體平均分數為 97.41。這是綜合評估分數，並非程式通過率。東區科展未晉級全國後，我重新檢視初版評估方式的限制。</p>
            <p style="margin:0;">進入旺宏科學獎決賽準備階段，我將修復規則開發與正式測試資料分開，重新驗證修復器真正能救回多少失敗案例。</p>
          </div>
        </div>
        <div style="background:#f1f5f9; border:1px solid #cbd5e1; border-left:3.5px solid #b45309; border-radius:4px; padding:3.5px 6px; font-size:8.8pt; color:#0f2942; font-weight:700; margin-top:5px;">
          ✦ 旺宏科學獎全領域 846 件作品報名，資訊領域僅 4 件入選決賽 20 強
        </div>
      </div>

      <!-- Right: Boundary & Conclusion -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:8px 10px;">
        <div>
          <div class="card-header">
            <div class="card-header-bar"></div>
            研究結果與修復機制的真實限制
          </div>
          <div style="font-size:9.2pt; color:#334155; line-height:1.44; text-align:justify;">
            <p style="margin:0 0 3px 0;">正式測試中，342 筆原始失敗案例有 9 筆經修復後通過，成功案例主要集中於格式、介面及局部資料處理問題。涉及題意理解或核心演算法的錯誤，固定規則無法直接解決。</p>
            <p style="margin:0;">這次重新驗證讓我更清楚修復器的適用範圍，也看見初版綜合指標無法直接代表實際修復效果。</p>
          </div>
        </div>
        <div style="background:#f1f5f9; border:1px solid #cbd5e1; border-left:3.5px solid #1e3a8a; border-radius:4px; padding:3.5px 6px; font-size:8.8pt; color:#0f2942; font-weight:700; margin-top:5px;">
          ✦ 第 66 屆東區科展 電腦與資訊學科【優等】
        </div>
      </div>
    </div>

    <!-- Error Taxonomy Card -->
    <div class="card" style="margin-bottom:0; background:#f8fafc; border:1px solid #cbd5e1; padding:7px 10px;">
      <div style="font-size:10pt; font-weight:800; color:#0f2942; margin-bottom:4px; display:flex; justify-content:space-between;">
        <span>錯誤類型分類與固定規則處理邊界</span>
        <span style="font-size:8.5pt; color:#64748b; font-weight:600;">旺宏決賽 342 筆失敗案例深度分析</span>
      </div>
      <div class="grid-3" style="font-size:8.9pt; line-height:1.38; gap:7px;">
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:2.5px solid #15803d; border-radius:4px; padding:4.5px 7px;">
          <span style="font-weight:800; color:#15803d; font-size:8.8pt; display:block; margin-bottom:2px;">1｜修復後通過 (9 筆)</span>
          輸出格式與介面：6 筆；<br>執行與資料流：2 筆；語法解析：1 筆。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:2.5px solid #b45309; border-radius:4px; padding:4.5px 7px;">
          <span style="font-weight:800; color:#b45309; font-size:8.8pt; display:block; margin-bottom:2px;">2｜修改後仍未通過 (33 筆)</span>
          修復器曾依固定規則修改，但重新測試後仍未通過。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:2.5px solid #b91c1c; border-radius:4px; padding:4.5px 7px;">
          <span style="font-weight:800; color:#b91c1c; font-size:8.8pt; display:block; margin-bottom:2px;">3｜未進行修改 (300 筆)</span>
          未符合可介入的固定修復規則，保留原始程式，不進行無明確依據的修改。
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span>葉陽甫 · 國立花蓮高級中學 ｜ 特殊選才面試精華摺頁冊</span>
    <span>第 3 頁 · 科學研究篇 (跨頁右面)</span>
  </div>
</div>

<!-- PAGE 4: Back Cover (Soccer on Top, English in Middle, Portfolio & QR on Bottom) -->
<div class="page" id="page4">
  <div>
    <!-- Top Header -->
    <div class="header">
      <div class="header-left">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-primary">04 / 跨域實踐篇</span>
          <span class="badge-tag badge-sub">多元發展 · 自律與體能</span>
        </div>
        <h1 class="page-title">
          足球競技與英文能力
        </h1>
        <div class="page-subtitle">高中五人制校隊聯賽競技 ｜ 語言檢定、在校表現與實際工具運用</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge secondary">⚽ 全國五人制聯賽 全國第 5 名</div>
        <div class="header-award-badge" style="margin-top:3px;">🌟 TOEIC 945 金色 ｜ GEPT 中高級</div>
      </div>
    </div>

    <!-- UPPER HALF: SOCCER ATHLETICS -->
    <div style="margin-bottom: 8px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
        <div style="font-size:12pt; font-weight:900; color:#0f2942; display:flex; align-items:center; gap:5px;">
          <span style="font-size:12.5pt;">⚽</span>
          <span>足球競技｜從國中校隊到高中全國聯賽</span>
        </div>
        <span style="font-size:8.8pt; font-weight:700; color:#1e293b; background:#f1f5f9; border:1px solid #cbd5e1; padding:1.5px 6px; border-radius:3px;">背號 42 號 · 花蓮高中校隊</span>
      </div>

      <!-- Soccer 4 Metrics -->
      <div class="grid-4" style="margin-bottom: 7px;">
        <div class="metric-card">
          <div class="metric-val">全國第 5 名</div>
          <div class="metric-lbl">114學年度五人制聯賽 (高二)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">全國第 6 名</div>
          <div class="metric-lbl">113學年度五人制聯賽 (高一)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">公開組第 5 名</div>
          <div class="metric-lbl">全國青年盃11人制公開組</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">社會組亞軍</div>
          <div class="metric-lbl">2025 花蓮縣運11人制社會組</div>
        </div>
      </div>

      <!-- Soccer Content + Team Photo -->
      <div class="grid-2" style="align-items: start;">
        <div style="display:flex; flex-direction:column; gap:6px;">
          <div class="card" style="margin-bottom:0; padding:8px 10px;">
            <div style="font-size:9.3pt; color:#334155; line-height:1.42; text-align:justify;">
              <div>
                我從幼兒園開始踢足球。國小參加<span style="white-space:nowrap;">全國學童盃</span>獲第三名；國二在全國乙組聯賽獲第三名。國三擔任花崗國中男子足球隊隊長，並參加全國<span style="white-space:nowrap;">國男甲級聯賽</span>。這些年我一直跟著球隊訓練，逐步接觸不同層級的正式賽事。
              </div>
              <div style="margin-top:3.5px;">
                升上<span style="white-space:nowrap;">花蓮高中</span>後，我繼續代表五人制足球校隊出賽。<span style="white-space:nowrap;">113 學年度</span>，球隊在全國 63 支參賽隊伍中獲第六名；<span style="white-space:nowrap;">114 學年度</span>，在 57 支隊伍中獲第五名，決賽以 5:3 擊敗臺中惠文高中。高中這兩年，我同時安排課業、資訊專案與校隊訓練，持續參與全國聯賽。
              </div>
            </div>
            <div style="font-size:8.8pt; color:#0f2942; font-weight:700; margin-top:4px; background:#f1f5f9; border:1px solid #cbd5e1; border-left:3px solid #1e3a8a; padding:2.5px 6px; border-radius:3px; line-height:1.35;">
              ◆ 連續兩年符合教育部運動績優甄試資格<br>
              <span style="white-space:nowrap;">113 學年全國第 6 名</span> ｜ <span style="white-space:nowrap;">114 學年全國第 5 名</span>
            </div>
          </div>

          <!-- FBref analytics highlight -->
          <div class="card" style="margin-bottom:0; background:#f8fafc; border:1px solid #cbd5e1; padding:7px 10px;">
            <div style="font-size:9.8pt; font-weight:800; color:#0f2942; margin-bottom:2.5px; white-space:nowrap;">
              📊 足球數據分析實作｜FBref × Python
            </div>
            <div style="font-size:9.2pt; color:#475569; line-height:1.42; text-align:justify;">
              因為對足球與程式設計都有興趣，我使用 Python 整理 FBref 公開數據，嘗試分析球員及球隊的比賽表現，作為跨領域程式實作練習。
            </div>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:6px;">
          <!-- 足球代表隊合影與緊鄰說明文字（說明文字緊貼照片，無多餘空隙） -->
          <div class="img-box" style="margin-bottom:0;">
            <img src="{p('soccer_team_perfect_circled.png')}" style="width:100%; height:auto; display:block; object-fit:contain;" alt="花蓮高中足球代表隊合影">
            <div class="img-caption" style="padding:2.5px 5px; font-size:8.2pt;">▲ 114學年度全國中等學校五人制足球聯賽決賽現場：<span style="white-space:nowrap;">花蓮高中代表隊合影</span><br>（紅圈處為葉陽甫，受獎代表左後方）</div>
          </div>

          <!-- 足球轉播精彩畫面 連結與 QR Code -->
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; align-items:center; justify-content:space-between; gap:8px;">
            <div style="font-size:8.8pt; line-height:1.35;">
              <a href="https://www.youtube.com/watch?v=Td-Z96Bm1TE" target="_blank" style="color:#0f2942; font-weight:800; text-decoration:none;">
                ▶ 114學年決賽直播精彩畫面 ↗
              </a><br>
              <span style="color:#64748b; font-size:7.8pt;">教育部／五人制足協官方直播賽事錄影</span>
            </div>
            <a href="https://www.youtube.com/watch?v=Td-Z96Bm1TE" target="_blank" style="text-decoration:none; flex-shrink:0;">
              <img src="{p('qr_soccer_highlight.png')}" style="width:34px; height:34px; display:block; border:1px solid #cbd5e1; border-radius:3px;" alt="足球直播精彩畫面 QR Code">
            </a>
          </div>

          <!-- FBref 足球數據分析 GitHub 專案連結與 QR Code -->
          <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:5px 8px; display:flex; align-items:center; justify-content:space-between; gap:8px;">
            <div style="font-size:8.8pt; line-height:1.35;">
              <a href="https://github.com/yyfsunnyboy/fbref-player-analysis" target="_blank" style="color:#0f2942; font-weight:800; text-decoration:none;">
                ▶ 足球數據分析 GitHub 專案 ↗
              </a><br>
              <span style="color:#64748b; font-size:7.8pt;">FBref 爬蟲腳本與球員數據整理原始碼</span>
            </div>
            <a href="https://github.com/yyfsunnyboy/fbref-player-analysis" target="_blank" style="text-decoration:none; flex-shrink:0;">
              <img src="{p('qr_fbref_github.png')}" style="width:34px; height:34px; display:block; border:1px solid #cbd5e1; border-radius:3px;" alt="足球數據分析 GitHub QR Code">
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- DIVIDER -->
    <div style="border-top: 1px solid #cbd5e1; margin: 6px 0 7px 0;"></div>

    <!-- LOWER HALF: ENGLISH PROFICIENCY -->
    <div style="margin-bottom: 7px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
        <div style="font-size:12pt; font-weight:900; color:#0f2942; display:flex; align-items:center; gap:5px;">
          <span style="font-size:12.5pt;">🌐</span>
          <span>英文能力｜語言檢定、在校表現與實際工具運用</span>
        </div>
        <span style="font-size:8.8pt; font-weight:700; color:#0f2942; background:#f1f5f9; border:1px solid #cbd5e1; padding:1.5px 6px; border-radius:3px;">CEFR B2+ ｜ 在校英文平均 91 分</span>
      </div>

      <!-- English 4 Metrics -->
      <div class="grid-4" style="margin-bottom: 7px;">
        <div class="metric-card">
          <div class="metric-val">945 分</div>
          <div class="metric-lbl">TOEIC 多益金色證書</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">全數通過</div>
          <div class="metric-lbl">GEPT 中高級聽說讀寫</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">485 / 460</div>
          <div class="metric-lbl">多益聽力 / 閱讀</div>
        </div>
        <div class="metric-card">
          <div class="metric-val" style="font-size: 12.8pt;">花蓮縣英文作文甲等</div>
          <div class="metric-lbl">花蓮縣高中組作文競賽</div>
        </div>
      </div>

      <!-- English Content (Three Sub-blocks) + 2 Certificate Photos -->
      <div class="grid-2">
        <!-- Left: Three Clear Sub-blocks A, B, C -->
        <div style="display:flex; flex-direction:column; gap:6px;">
          <!-- A: 語言檢定 -->
          <div class="card" style="padding:6.5px 9px; margin-bottom:0;">
            <div style="font-size:9.8pt; font-weight:800; color:#0f2942; margin-bottom:2.5px;">
              A｜語言檢定成績
            </div>
            <div style="display:flex; flex-direction:column; gap:3px; font-size:9.2pt; color:#334155;">
              <div style="display:flex; align-items:baseline; gap:4px; line-height:1.38;">
                <span style="flex-shrink:0; width:8px; font-weight:700; color:#1e3a8a;">•</span>
                <div style="flex:1;"><b>TOEIC 945 分</b>（金色證書：聽力 485、閱讀 460）。</div>
              </div>
              <div style="display:flex; align-items:baseline; gap:4px; line-height:1.38;">
                <span style="flex-shrink:0; width:8px; font-weight:700; color:#1e3a8a;">•</span>
                <div style="flex:1;"><b>全民英檢（GEPT）中高級</b>聽、說、讀、寫四項全數通過（聽力 111、閱讀 87、口說 80、寫作 80）。</div>
              </div>
            </div>
          </div>

          <!-- B: 英文競賽與在校表現 -->
          <div class="card" style="padding:6.5px 9px; margin-bottom:0;">
            <div style="font-size:9.8pt; font-weight:800; color:#0f2942; margin-bottom:2.5px;">
              B｜英文競賽與在校表現
            </div>
            <div style="display:flex; flex-direction:column; gap:3px; font-size:9.2pt; color:#334155;">
              <div style="display:flex; align-items:baseline; gap:4px; line-height:1.38;">
                <span style="flex-shrink:0; width:8px; font-weight:700; color:#1e3a8a;">•</span>
                <div style="flex:1;">花蓮縣英文作文競賽高中 A 組<b>甲等</b>、<br>校內英文作文<span style="white-space:nowrap;">二年級<b>第二名</b></span>。</div>
              </div>
              <div style="display:flex; align-items:baseline; gap:4px; line-height:1.38;">
                <span style="flex-shrink:0; width:8px; font-weight:700; color:#1e3a8a;">•</span>
                <div style="flex:1;">校內英語演說一年級初賽<b>第一名</b>、全年級複賽<b>第四名</b>。</div>
              </div>
              <div style="display:flex; align-items:baseline; gap:4px; line-height:1.38;">
                <span style="flex-shrink:0; width:8px; font-weight:700; color:#1e3a8a;">•</span>
                <div style="flex:1;">高一至高二英文平均 <b>91 分</b>（校排前 4%）；<br><span style="white-space:nowrap;">高二下 <b>96 分</b></span>、年級第七名（前 2%）。</div>
              </div>
            </div>
          </div>

          <!-- C: 英文的實際使用 -->
          <div class="card" style="padding:6.5px 9px; margin-bottom:0; background:#f8fafc;">
            <div style="font-size:9.8pt; font-weight:800; color:#0f2942; margin-bottom:2px;">
              C｜英文的實際使用
            </div>
            <div style="font-size:9.2pt; color:#475569; line-height:1.42; text-align:justify;">
              在程式學習時，我會查閱英文技術資料，了解新工具的使用方法；平常也會觀看國外足球分析影片、閱讀英文足球資訊。英文是我學習資訊與足球時持續使用的工具。
            </div>
          </div>
        </div>

        <!-- Right: Two Certificates Vertically Stacked -->
        <div style="display:flex; flex-direction:column; gap:6px;">
          <div class="img-box" style="margin-bottom:0;">
            <img src="{p('english_img2.jpeg')}" style="height:109px; width:100%; object-fit:contain; background:#ffffff;" alt="TOEIC 945 金色證書">
            <div class="img-caption" style="padding:2.5px 5px; font-size:8.4pt;">▲ TOEIC 官方成績證書（945 / 990 · 金色證書）</div>
          </div>
          <div class="img-box" style="margin-bottom:0;">
            <img src="{p('english_img1.jpeg')}" style="height:147px; width:100%; object-fit:contain; background:#ffffff;" alt="GEPT 中高級證書">
            <div class="img-caption" style="padding:2.5px 5px; font-size:8.4pt;">▲ 全民英檢 GEPT 中高級合格證書（聽說讀寫全數通過）</div>
          </div>
        </div>
      </div>
    </div>

    <!-- DIGITAL PORTFOLIO & QR CODE BAR -->
    <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:5px; padding:7px 12px; display:flex; justify-content:space-between; align-items:center; margin-top:2px;">
      <div style="display:flex; gap:16px; align-items:center;">
        <!-- QR Code 1: Demo -->
        <div style="display:flex; align-items:center; gap:7px;">
          <a href="https://mathb.math-adaptive.org/review-demo" target="_blank" style="text-decoration:none;">
            <img src="{p('qr_demo.png')}" style="width:16mm; height:16mm; display:block; border:1px solid #cbd5e1; border-radius:3px;" alt="Demo QR Code">
          </a>
          <div style="font-size:9.2pt; white-space:nowrap;">
            <a href="https://mathb.math-adaptive.org/review-demo" target="_blank" style="color:#0f2942; font-weight:800; text-decoration:none;">
              AI 自適應輔助學習系統 Demo ↗
            </a>
          </div>
        </div>

        <!-- QR Code 2: GitHub -->
        <div style="display:flex; align-items:center; gap:7px;">
          <a href="https://github.com/yyfsunnyboy/Mathproject_tvet_mathB" target="_blank" style="text-decoration:none;">
            <img src="{p('qr_github.png')}" style="width:16mm; height:16mm; display:block; border:1px solid #cbd5e1; border-radius:3px;" alt="GitHub QR Code">
          </a>
          <div style="font-size:9.2pt; white-space:nowrap;">
            <a href="https://github.com/yyfsunnyboy/Mathproject_tvet_mathB" target="_blank" style="color:#0f2942; font-weight:800; text-decoration:none;">
              GitHub 系統程式碼 ↗
            </a>
          </div>
        </div>
      </div>

      <div style="font-size:9.4pt; color:#334155; font-weight:700; text-align:right; line-height:1.42; white-space:nowrap;">
        葉陽甫 ｜ 國立花蓮高級中學<br>
        <span style="color:#64748b; font-weight:normal; font-size:8.5pt;">誠摯感謝各位教授審閱與指導</span>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span>葉陽甫 · 國立花蓮高級中學 ｜ 特殊選才面試精華摺頁冊</span>
    <span>第 4 頁 · 跨域實踐篇 (封底)</span>
  </div>
</div>

</body>
</html>
"""
    return html

def main():
    html_content = build_html()
    html_file = TMP_DIR / "pages_academic.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Wrote unified 4-page HTML to {html_file}")

    # Render via Chrome headless
    pdf_4pages = TMP_DIR / "pages_academic.pdf"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_4pages}",
        str(html_file)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Chrome error:", res.stderr)
        return
    print(f"Rendered {pdf_4pages} successfully ({os.path.getsize(pdf_4pages)} bytes)")

    doc = fitz.open(pdf_4pages)
    page_count = len(doc)
    print(f"Total rendered pages: {page_count}")
    if page_count != 4:
        print(f"WARNING: Expected 4 pages, but got {page_count} pages! Please verify layout heights.")

    # Save A4 4-Page Reading PDF
    out_a4 = OUT_DIR / "葉陽甫_面試四面小冊_典雅學術版_A4閱讀.pdf"
    doc.save(out_a4, garbage=4, deflate=True)
    print(f"Saved A4 booklet: {out_a4} ({len(doc)} pages)")

    # Also update SRC / 00_葉陽甫備審資料首頁.pdf with the updated Page 1
    p1_doc = fitz.open()
    p1_doc.insert_pdf(doc, from_page=0, to_page=0)
    p1_path = SRC / "00_葉陽甫備審資料首頁.pdf"
    p1_doc.save(p1_path, garbage=4, deflate=True)
    print(f"Updated master cover PDF: {p1_path}")

    # Assemble A3 Landscape Duplex Printable PDF
    # Sheet 1 (Outside): Left = P4 (Back), Right = P1 (Cover)
    # Sheet 2 (Inside): Left = P2 (System), Right = P3 (Research)
    a3_doc = fitz.open()
    a3_w, a3_h = 1190.55, 841.89 # A3 landscape points (420mm x 297mm)

    for left_idx, right_idx in [(3, 0), (1, 2)]:
        sheet = a3_doc.new_page(width=a3_w, height=a3_h)
        sheet.show_pdf_page(fitz.Rect(0, 0, a3_w / 2, a3_h), doc, left_idx)
        sheet.show_pdf_page(fitz.Rect(a3_w / 2, 0, a3_w, a3_h), doc, right_idx)

        # Copy clickable links from left page
        for l in doc[left_idx].get_links():
            if 'uri' in l:
                sheet.insert_link({'kind': fitz.LINK_URI, 'from': l['from'], 'uri': l['uri']})

        # Copy clickable links from right page (shifted right by a3_w / 2)
        for l in doc[right_idx].get_links():
            if 'uri' in l:
                r = l['from']
                new_r = fitz.Rect(r.x0 + a3_w / 2, r.y0, r.x1 + a3_w / 2, r.y1)
                sheet.insert_link({'kind': fitz.LINK_URI, 'from': new_r, 'uri': l['uri']})

    out_a3 = OUT_DIR / "葉陽甫_面試四面小冊_典雅學術版_A3雙面列印.pdf"
    a3_doc.save(out_a3, garbage=4, deflate=True)
    print(f"Saved A3 printable booklet: {out_a3} ({len(a3_doc)} sheets)")

    # Render preview images
    preview_dir = ROOT / "tmp" / "booklet_v8_preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    for i, p_item in enumerate(doc):
        pix = p_item.get_pixmap(dpi=150)
        pix.save(str(preview_dir / f"a4_p{i+1}.png"))
    for i, s_item in enumerate(a3_doc):
        pix = s_item.get_pixmap(dpi=150)
        pix.save(str(preview_dir / f"a3_sheet{i+1}.png"))
    print(f"Previews saved to {preview_dir}")

if __name__ == "__main__":
    main()
