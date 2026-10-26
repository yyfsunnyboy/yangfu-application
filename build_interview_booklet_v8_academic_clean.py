"""Build Interview Booklet V8 - Academic Clean & Calm Edition (典雅學術·沉穩清爽版).

Designed specifically for University Special Selection Review Professors (特殊選才評審教授):
- Restrained, cohesive Oxford Navy & Steel Slate color system
- Strict adherence to factual experiences, eliminating hype adjectives and AI narrative cliches
- All 4 pages (P1 Cover, P2 System, P3 Research, P4 Athletics & English) unified in one HTML template
- True venue accuracy: System deployed at Hualien Commercial High School (花蓮高商, father's classes)
- Precise AST Healer research history: From MCRI score critique to independent test set & boundary recognition
- Authentic soccer and English records: factual data, clear test scores, and research limitations
"""
import os
import subprocess
import fitz
from pathlib import Path

ROOT = Path(r"C:\Projects\yangfu-application")
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
    font-size: 11.5px;
    line-height: 1.5;
  }}
  
  .page {{
    width: 210mm;
    height: 297mm;
    page-break-after: always;
    position: relative;
    padding: 12mm 14mm 11mm 14mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    background: #ffffff;
  }}

  /* Top Bar Header */
  .header {{
    border-bottom: 2px solid #0f2942;
    padding-bottom: 6px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .header-left {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  
  /* Unified Academic Badges */
  .badge-tag {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 2.5px 8px;
    border-radius: 4px;
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
    font-size: 20px;
    font-weight: 900;
    color: #0f2942;
    letter-spacing: -0.3px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 9px;
    white-space: nowrap;
  }}
  .page-subtitle {{
    font-size: 11px;
    color: #475569;
    font-weight: 500;
  }}
  .header-right {{
    text-align: right;
  }}
  
  /* Academic Citation Award Badge */
  .header-award-badge {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #b45309;
    color: #0f2942;
    padding: 3.5px 9px;
    border-radius: 4px;
    font-size: 10.5px;
    font-weight: 800;
    display: inline-block;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  }}
  .header-award-badge.secondary {{
    border-left-color: #334e68;
  }}

  /* Grid Layouts */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 11px;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 9px;
  }}
  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 9px;
  }}

  /* Unified Academic Metric Cards */
  .metric-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 3px solid #1e3a8a;
    border-radius: 6px;
    padding: 7px 9px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  }}
  .metric-val {{
    font-size: 20px;
    font-weight: 900;
    color: #0f2942;
    line-height: 1.1;
    letter-spacing: -0.2px;
  }}
  .metric-lbl {{
    font-size: 9.8px;
    color: #64748b;
    margin-top: 3px;
    font-weight: 600;
  }}

  /* Content Cards */
  .card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 9px;
  }}
  .card-header {{
    font-size: 13px;
    font-weight: 800;
    color: #0f2942;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .card-header-bar {{
    width: 3.5px;
    height: 14px;
    border-radius: 2px;
    background: #1e3a8a;
  }}

  /* Process Steps */
  .process-step {{
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
    align-items: flex-start;
  }}
  .step-num {{
    background: #0f2942;
    color: #ffffff;
    font-size: 9px;
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
    font-weight: 700;
    font-size: 11.8px;
    color: #0f2942;
  }}
  .step-desc {{
    font-size: 11px;
    color: #475569;
    line-height: 1.4;
  }}

  /* Refined Academic Bridge Cards */
  .bridge-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #1e3a8a;
    border-radius: 6px;
    padding: 10px 13px;
    margin-top: 6px;
  }}
  .bridge-title {{
    font-size: 12.5px;
    font-weight: 800;
    color: #0f2942;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
  }}

  .p3-bridge-card {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #334e68;
    border-radius: 6px;
    padding: 9px 12px;
    margin-bottom: 10px;
  }}

  /* Footer */
  .footer {{
    border-top: 1px solid #cbd5e1;
    padding-top: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10px;
    color: #64748b;
    font-weight: 500;
  }}

  /* Image Containers */
  .img-box {{
    border-radius: 6px;
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
    font-size: 9.2px;
    color: #475569;
    text-align: center;
    padding: 3.5px 6px;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    font-weight: 600;
  }}

  /* Page 1 Specific Styling */
  .p1-badge-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px 8px;
    margin-top: 5px;
  }}
  .p1-badge-item {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #1e3a8a;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 10.5px;
    color: #0f2942;
    font-weight: 700;
  }}
  .p1-badge-item.gold {{
    border-left-color: #b45309;
  }}
  .p1-section-header {{
    font-size: 12.8px;
    font-weight: 800;
    color: #0f2942;
    padding-bottom: 3px;
    border-bottom: 1.5px solid #0f2942;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .p1-list {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
    font-size: 11px;
    color: #334155;
    line-height: 1.45;
  }}
  .p1-item-title {{
    font-weight: 700;
    color: #0f2942;
  }}
  .hl-blue {{
    color: #1e3a8a;
    font-weight: 700;
  }}
  .hl-gold {{
    color: #b45309;
    font-weight: 700;
  }}
</style>
</head>
<body>

<!-- PAGE 1: Personal Overview & Master Profile -->
<div class="page" id="page1">
  <div>
    <!-- Top Meta Navigation -->
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:8px; font-size:10px; color:#64748b;">
      <div>
        <span>特殊選才面試資料</span> ｜ <b style="color:#0f2942;">個人總覽</b> ｜ <span>高中學習與成果摘要</span>
      </div>
      <div style="background:#0f2942; color:#ffffff; font-weight:700; font-size:9.5px; padding:2px 8px; border-radius:3px;">
        國立花蓮高級中學
      </div>
    </div>

    <!-- Header Main Area: Photo + Name + Tags + 4 Key Badges -->
    <div style="display:flex; gap:14px; align-items:center; margin-bottom:8px;">
      <img src="{p('YEH YANG FU.jpg')}" style="width:25mm; height:31mm; object-fit:cover; border-radius:4px; border:1px solid #cbd5e1; flex-shrink:0;" alt="葉陽甫個人證件照">
      <div style="flex:1;">
        <div style="display:flex; align-items:baseline; justify-content:space-between; margin-bottom:3px;">
          <div style="display:flex; align-items:baseline; gap:8px;">
            <span style="font-size:23px; font-weight:900; color:#0f2942; letter-spacing:0.5px;">葉陽甫</span>
            <span style="font-size:13.5px; font-weight:700; color:#334155;">國立花蓮高級中學 普通科</span>
          </div>
          <span style="font-size:10.5px; font-weight:700; color:#1e3a8a;">特殊選才備審核心總覽</span>
        </div>
        <div style="font-size:11px; color:#334155; font-weight:600; background:#f8fafc; border-left:3.5px solid #0f2942; padding:3px 8px; margin-bottom:5px;">
          資訊工程 · 數學自適應系統實作 · 程式生成局部修復研究 · 足球運動競技
        </div>
        <!-- 4 Key Verified Badges -->
        <div class="p1-badge-grid">
          <div class="p1-badge-item gold">
            🥇 育秀盃創意獎【<span class="hl-gold">全國金獎</span>】(AI應用類 · 10萬元)
          </div>
          <div class="p1-badge-item gold">
            🏅 旺宏科學獎【<span class="hl-gold">全國決賽20強</span>】(資訊領域全國僅4件)
          </div>
          <div class="p1-badge-item">
            ⚽ 全國五人制足球聯賽【<span class="hl-blue">全國第 5 名</span>】(高中校隊主力)
          </div>
          <div class="p1-badge-item">
            📜 <span class="hl-blue">TOEIC 945</span>（金色證書）｜ <span class="hl-blue">APCS 觀念 5 級分</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Divider -->
    <div style="height:1.5px; background:#0f2942; margin-bottom:9px;"></div>

    <!-- Two-Column Main Content (45% | 55%) -->
    <div style="display:grid; grid-template-columns: 45% 53%; gap: 2%;">
      <!-- Left Column: Academic, English, Soccer -->
      <div style="display:flex; flex-direction:column; gap:10px;">
        <!-- 1. 學業與在校表現 -->
        <div class="card" style="margin-bottom:0; padding:9px 11px;">
          <div class="p1-section-header">
            <span>◆ 學業與在校表現</span>
          </div>
          <div class="p1-list">
            <div>
              • <span class="p1-item-title">總體成績</span>：高一至高二 4 學期班排前五，學業平均 <b>84.2</b>（年級前 8% · 24/320）
            </div>
            <div>
              • <span class="p1-item-title">數理資工表現</span>：資訊科 <span class="hl-blue">前 6%</span> ｜ 數學科 <span class="hl-blue">前 6%</span> ｜ 化學科 <span class="hl-blue">前 4%</span> ｜ 地科 <span class="hl-blue">前 2%</span>
            </div>
            <div>
              • <span class="p1-item-title">校內選修表現</span>：Arduino 程式設計 <b>94 分</b>（第 2 名）｜ Python 程式設計 <b>90 分</b>（第 4 名）
            </div>
            <div>
              • <span class="p1-item-title">數理競賽</span>：JHMC 國中數學競賽 團體一等獎／個人優良獎 ｜ 更生盃數學 銀牌
            </div>
          </div>
        </div>

        <!-- 2. 外語檢定與表現 -->
        <div class="card" style="margin-bottom:0; padding:9px 11px;">
          <div class="p1-section-header">
            <span>◆ 外語檢定與表現</span>
          </div>
          <div class="p1-list">
            <div>
              • <span class="p1-item-title">TOEIC 945 分</span>（<span class="hl-gold">金色證書</span>）：聽力 485 / 閱讀 460
            </div>
            <div>
              • <span class="p1-item-title">全民英檢（GEPT）中高級</span>：聽、說、讀、寫四項全數合格
            </div>
            <div>
              • <span class="p1-item-title">在校英文平均</span>：高一至高二平均 <b>91 分</b>（<span class="hl-blue">前 4%</span>），高二下 <b>96 分</b>（年排第 7 · <span class="hl-blue">前 2%</span>）
            </div>
            <div>
              • <span class="p1-item-title">語文競賽</span>：花蓮縣英文作文高中組甲等 ｜ 校內英語演說初賽第 1 名、全校複賽第 4 名
            </div>
          </div>
        </div>

        <!-- 3. 足球運動經歷 -->
        <div class="card" style="margin-bottom:0; padding:9px 11px;">
          <div class="p1-section-header">
            <span>◆ 足球運動經歷</span>
          </div>
          <div class="p1-list">
            <div>
              • <span class="p1-item-title">全國五人制足球聯賽</span>：114 學年 <span class="hl-gold">全國第 5 名</span> ｜ 113 學年 <span class="hl-gold">全國第 6 名</span>
            </div>
            <div>
              • <span class="p1-item-title">全國青年盃公開組</span>：<span class="hl-gold">全國第 5 名</span> ｜ 具教育部運動績優甄試資格
            </div>
            <div>
              • <span class="p1-item-title">地方賽事</span>：花蓮縣運社會男子組亞軍 ｜ 國中男子組冠軍
            </div>
            <div>
              • <span class="p1-item-title">球隊經歷</span>：花蓮高中五人制校隊主力球員（背號 42 號）｜ 花崗國中足球隊隊長
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Research Awards, Core Projects, Engineering Exploration -->
      <div style="display:flex; flex-direction:column; gap:10px;">
        <!-- 1. 代表性科研與競賽成果 -->
        <div class="card" style="margin-bottom:0; padding:9px 11px;">
          <div class="p1-section-header">
            <span>◆ 代表性科研與競賽成果</span>
          </div>
          <div class="p1-list">
            <div>
              <b>1. 第 23 屆 育秀盃創意獎【<span class="hl-gold">全國金獎</span>】</b><br>
              • 高中職 AI 應用類金獎（獎金 10 萬元） ｜ 作品：AI 自適應輔助學習系統
            </div>
            <div>
              <b>2. 第 25 屆 旺宏科學獎【<span class="hl-gold">全國決賽 20 強</span>】</b><br>
              • 全領域 846 件評選，資訊領域全國僅 4 件入圍決賽 ｜ 題目：AST 程式碼局部修復研究
            </div>
            <div>
              <b>3. 2026 神通 AI 數位學院扶輪盃【<span class="hl-gold">全國冠軍</span>】</b><br>
              • 全國高中 AI 應用競賽 第一名
            </div>
            <div>
              <b>4. 第 66 屆 東區科展【<span class="hl-blue">優等第 2 名</span>】</b>（電腦與資訊學科）
            </div>
          </div>
        </div>

        <!-- 2. 核心專案與實作 -->
        <div class="card" style="margin-bottom:0; padding:9px 11px;">
          <div class="p1-section-header">
            <span>◆ 核心專案與實作</span>
          </div>
          <div class="p1-list">
            <div>
              • <span class="p1-item-title">AI 自適應輔助學習系統</span>：<br>
              由 Python 出題程式動態生成題目與答案，結合 SymPy 判題引擎，於花蓮高商數學課堂實際使用（2 班 50 人、累積 1,224 次作答）。<br>
              <span style="font-size:10px; color:#475569;">🌐 上線網址：<b>mathb.math-adaptive.org</b> ｜ 📁 GitHub：<b>bit.ly/yangfu-adaptive</b></span>
            </div>
            <div>
              • <span class="p1-item-title">AST Active Healer 程式修復機制</span>：<br>
              以抽象語法樹與固定規則，研究小型模型程式生成錯誤之局部修復範圍與限制，探索非黑箱的確定性修復能力邊界。
            </div>
          </div>
        </div>

        <!-- 3. 程式能力與工程探究 -->
        <div class="card" style="margin-bottom:0; padding:9px 11px;">
          <div class="p1-section-header">
            <span>◆ 程式能力與工程探究</span>
          </div>
          <div class="p1-list">
            <div>
              • <span class="p1-item-title">APCS 大學程式先修檢測</span>：<br>
              觀念 <b>92.5 分</b>（<span class="hl-gold">5 級分 · 前 3.7%</span>） ｜ 實作 <b>135 分</b>（2 級分）
            </div>
            <div>
              • <span class="p1-item-title">IEYI 世界青少年發明展</span>：2023 臺灣選拔賽【<span class="hl-gold">銀獎</span>】
            </div>
            <div>
              • <span class="p1-item-title">足球數據分析實作</span>：使用 Python 抓取 FBref 資料整理球員與球隊表現
            </div>
            <div>
              • <span class="p1-item-title">其他表現</span>：校內資訊學科能力競賽佳作 ｜ 東部物理 IYPT 科學營第 3 名
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
        <div class="page-subtitle">從高中數學課堂需求出發，開發並實際投入教學使用的學習平台</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge">🏆 神通扶輪盃 全國第一名 冠軍</div>
        <div class="header-award-badge" style="margin-top:3px; border-left-color:#b45309;">🥇 育秀盃創意獎 全國金獎 (10萬元)</div>
      </div>
    </div>

    <!-- 4 Key Metrics (Calm Unified Style) -->
    <div class="grid-4" style="margin-bottom: 10px;">
      <div class="metric-card">
        <div class="metric-val">2 班</div>
        <div class="metric-lbl">正式課堂持續使用</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">50 人</div>
        <div class="metric-lbl">真實高中學生帳號</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">1,224 次</div>
        <div class="metric-lbl">累積實際作答次數</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">67%</div>
        <div class="metric-lbl">全體平均答對率</div>
      </div>
    </div>

    <!-- Main Two Column Grid -->
    <div class="grid-2" style="margin-bottom: 9px;">
      <!-- Left Column: Core System Pipeline & Role -->
      <div style="display:flex; flex-direction:column; justify-content:space-between;">
        <div class="card" style="padding:9px 11px;">
          <div class="card-header">
            <div class="card-header-bar"></div>
            起點問題與需求拆解
          </div>
          <div style="font-size:11.4px; color:#334155; line-height:1.48;">
            父親為技術型高中數學老師，長年面臨<b>「題目難以數位化批次輸入、固定題庫無法反覆變題練習、課堂學生雙峰差距極大」</b>之教學痛點。我著手自主開發適性化學習系統，在花蓮高商（父親任教班級）實際投入課堂使用與測試。
          </div>
        </div>

        <div class="card" style="padding:9px 11px;">
          <div class="card-header">
            <div class="card-header-bar"></div>
            三大核心技術模組流程
          </div>
          <div class="process-step">
            <div class="step-num">1</div>
            <div class="step-content">
              <div class="step-title">結構化教材自動解析與匯入</div>
              <div class="step-desc">解析 Word/PDF 講義，自動對齊冊、章、節與前置知識節點樹，保留教師審核修訂機制。</div>
            </div>
          </div>
          <div class="process-step">
            <div class="step-num">2</div>
            <div class="step-content">
              <div class="step-title">Code-as-Content 程式即內容出題</div>
              <div class="step-desc">由 Python 出題程式動態生成不同數值的題目及對應答案。</div>
            </div>
          </div>
          <div class="process-step" style="margin-bottom:0;">
            <div class="step-num">3</div>
            <div class="step-content">
              <div class="step-title">嚴格數學判題器 × AI 助教分層導航</div>
              <div class="step-desc">以程式進行數學答案驗證，降低直接使用語言模型判題的錯誤風險；AI 助教負責思路提示。</div>
            </div>
          </div>
        </div>

        <div class="card" style="margin-bottom:0; padding:9px 11px;">
          <div class="card-header">
            <div class="card-header-bar"></div>
            自適應學習路徑設計
          </div>
          <div style="background:#f1f5f9; border:1px solid #e2e8f0; padding:4px 7px; border-radius:4px; font-size:10.5px; color:#1e293b; text-align:center; font-weight:700; margin-bottom:4px;">
            學生作答 ➔ 能力診斷 ➔ 適性決策 ➔ 概念補強／進階 ➔ 再次評量
          </div>
          <div style="font-size:11px; color:#475569; line-height:1.42;">
            系統整合知識狀態診斷，動態判斷學生目前卡點。若前置基礎不穩，自動引導返回前置技能複習；若熟練則前進高階題目。
          </div>
        </div>
      </div>

      <!-- Right Column: Visual Evidence & Screenshot -->
      <div style="display:flex; flex-direction:column; justify-content:space-between;">
        <div class="img-box">
          <img src="{p('ai_student_practice_screen.png')}" style="width:100%; height:auto; display:block;" alt="學生適性解題與 AI 助教介面">
          <div class="img-caption" style="font-size:9px; padding:3px 4px; white-space:nowrap;">▲ 真實正式網站：學生適性解題、畫布運算與 AI 助教介面 (mathb.math-adaptive.org)</div>
        </div>

        <div class="grid-2">
          <div class="img-box">
            <img src="{p('yuxiu_img1.png')}" style="height:152px; object-fit:contain; background:#ffffff;" alt="育秀盃金獎證書">
            <div class="img-caption">▲ 育秀盃創意獎 全國金獎 (獎金10萬)</div>
          </div>
          <div class="img-box">
            <img src="{p('rotary_img_2.jpeg')}" style="height:152px; object-fit:contain; background:#ffffff;" alt="扶輪盃冠軍獎狀">
            <div class="img-caption">▲ 神通扶輪盃 全國第一名 冠軍</div>
          </div>
        </div>

        <div class="card" style="background:#f8fafc; border:1px solid #cbd5e1; margin-bottom:0; padding:8px 11px;">
          <div style="font-size:11.2px; color:#334155; line-height:1.45;">
            <b>葉陽甫個人核心研發職責（貢獻度 70%，獲指導老師認證）</b>：<br>
            負責系統架構設計、前後端全端實作、教材匯入與結構化解析、SymPy 判題機制、PostgreSQL 資料庫設計、Docker 部署與花蓮高商課堂持續維護。
          </div>
        </div>
      </div>
    </div>

    <!-- FULL-STACK ARCHITECTURE & DEVOPS CARD -->
    <div class="card" style="padding:8px 11px; margin-bottom:9px; background:#f8fafc; border:1px solid #cbd5e1;">
      <div class="card-header" style="margin-bottom:5px; justify-content:space-between;">
        <div style="display:flex; align-items:center; gap:6px;">
          <div class="card-header-bar"></div>
          <span>全端工程架構與真實課堂落地技術棧（Full-Stack & DevOps）</span>
        </div>
        <span style="font-size:9.5px; color:#334e68; font-weight:700;">班級實機部署 · 微服務架構</span>
      </div>
      <div class="grid-3" style="font-size:10.5px; line-height:1.4; gap:9px;">
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:5px; padding:5px 8px;">
          <b style="color:#0f2942;">🖥️ 前端作答與公式渲染</b><br>
          Next.js / React 全端架構，整合 KaTeX 動態解析數學符號與 LaTeX 公式，支援幾何 Canvas 動態互動與座標繪圖。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:5px; padding:5px 8px;">
          <b style="color:#0f2942;">⚙️ 後端非同步與數理判題</b><br>
          FastAPI 非同步處理，以 SymPy 符號運算引擎進行數學等價性驗證，精確判別同解，降低語言模型判題錯誤風險。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:5px; padding:5px 8px;">
          <b style="color:#0f2942;">🚀 容器部署與正式維運</b><br>
          Docker 容器化封裝、Nginx 反向代理、PostgreSQL 狀態追蹤，處理課堂實際使用遭遇的「公式輸入格式、缺參數、變題邊界」等工程問題。
        </div>
      </div>
    </div>

    <!-- Bridge to P.3: Narrative Link -->
    <div class="bridge-card" style="padding:9px 12px;">
      <div class="bridge-title" style="margin-bottom:5px;">
        <span>⚡ 跨頁銜接：系統實際使用後發現的技術問題 ➔ 延伸為程式碼修復研究</span>
        <span style="font-size:11px; font-weight:800; color:#1e3a8a;">接續右頁研究 ➔</span>
      </div>
      <div class="grid-2" style="font-size:10.8px; line-height:1.42; gap:9px; margin-bottom:5px;">
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:5px; padding:5px 8px;">
          <b style="color:#0f2942;">☁️ 雲端大型模型限制</b>：<br>
          課堂高頻呼叫 API 產生連線延遲與費用負擔，且有校園學生資料隱私考量；因此開始探索本地模型部署的可能性，以減少外部 API 依賴。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:5px; padding:5px 8px;">
          <b style="color:#0f2942;">💻 本地小模型生成程式碼的可靠性問題</b>：<br>
          本地小模型生成出題程式碼時，容易產生 <b>SyntaxError 語法錯誤、未引用變數或介面格式不符</b>；若要求模型重新生成，耗費算力且結果不穩定。
        </div>
      </div>
      <div style="font-size:11px; color:#1e293b; line-height:1.42; background:#edf2f7; border-left:3px solid #334e68; padding:5px 9px; border-radius:4px; font-weight:600;">
        💡 <b>核心研究問題</b>：「在無正確答案（Ground Truth）的前提下，能否以確定性規則在本地端安全修復局部程式碼？」——從課堂系統開發中發現的這項問題，延伸出右頁的抽象語法樹（AST）修復研究。
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
      <div class="header-left">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-primary">03 / 科學研究篇</span>
          <span class="badge-tag badge-sub">跨頁主線 (下) · 深化科研</span>
        </div>
        <h1 class="page-title">
          AST Active Healer｜小型語言模型生成程式碼的局部修復研究
        </h1>
        <div class="page-subtitle">以抽象語法樹與固定規則，研究程式碼錯誤可修復的範圍與限制</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge">🏅 第25屆旺宏科學獎 全國決賽20強</div>
        <div class="header-award-badge secondary" style="margin-top:3px;">🎖️ 第66屆東區科展 優等第2名</div>
      </div>
    </div>

    <!-- P3 Top Connecting Box -->
    <div class="p3-bridge-card" style="padding:9px 11px; margin-bottom:10px;">
      <div style="font-size:11.8px; font-weight:800; color:#0f2942; display:flex; justify-content:space-between; margin-bottom:3px;">
        <span>🔬 科研問題意識：把真實痛點抽離為嚴謹的科學研究</span>
        <span style="font-size:10.5px; color:#334e68; font-weight:700;">承接左頁系統工程痛點 ◄</span>
      </div>
      <div style="font-size:11.2px; color:#334155; line-height:1.46;">
        從系統開發中發現的問題，延伸為程式碼修復研究。聚焦於<b>「小模型生成受限環境程式的局部修復能力與邊界」</b>，設計以固定規則運作的 AST Active Healer，探索不將錯誤重新丟回模型、直接在語法樹層級進行確定性修復的可行性與限制。
      </div>
    </div>

    <!-- Core Mechanism Diagram & Benchmark Chart (Side-by-Side) -->
    <div class="grid-2" style="margin-bottom: 10px; align-items: stretch;">
      <!-- Left: AST Active Healer Flowchart -->
      <div class="card" style="padding: 9px 10px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 4px; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 5px;">
            <div class="card-header-bar"></div>
            <span style="font-size: 11.8px; font-weight: 800;">AST Healer 三階段局部修復流程</span>
          </div>
          <span style="font-size: 9.2px; color: #475569; background:#f1f5f9; padding:1.5px 5px; border-radius:3px; font-weight: 700;">語法樹靜態解析架構</span>
        </div>
        <div class="img-box" style="border: 1px solid #e2e8f0; margin-bottom: 5px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff;">
          <img src="{p('healer_flowchart.png')}" style="height: 230px; width: 100%; object-fit: contain;" alt="AST Healer 流程圖">
        </div>
        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 5px 7px; font-size: 10px; color: #334155; line-height: 1.38;">
          <b>修復機制流程</b>：① <b>Scaffold 骨架</b>約束輸入輸出介面 ➔ ② <b>AST 解析</b>捕捉語法樹與未引用變數 ➔ ③ <b>固定規則局部修復</b>，若超出安全規則則<b>主動棄權 (Abstain)</b>。
        </div>
      </div>

      <!-- Right: Benchmark Experiment Chart -->
      <div class="card" style="padding: 9px 10px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 4px; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 5px;">
            <div class="card-header-bar"></div>
            <span style="font-size: 11.8px; font-weight: 800;">4 種 Prompt × 3 模型測試救援表現</span>
          </div>
          <span style="font-size: 9.2px; color: #475569; background:#f1f5f9; padding:1.5px 5px; border-radius:3px; font-weight: 700;">旺宏決賽獨立測試集</span>
        </div>
        <div class="img-box" style="border: 1px solid #e2e8f0; margin-bottom: 5px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff;">
          <img src="{p('healer_chart_user.png')}" style="height: 230px; width: 100%; object-fit: contain;" alt="三種模型在四種 Prompt 條件下的原始通過率與 Healer 新增救援">
        </div>
        <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 5px 7px; font-size: 10px; color: #334155; line-height: 1.38;">
          <b>實驗觀察</b>：Qwen 與 CodeLlama 在各提示條件之基準通過率不同；342 個失敗案例中，42 個觸發規則，最終 9 個案例由 Healer 安全救回（救回率 2.63%）。
        </div>
      </div>
    </div>

    <!-- 4 Rigorous Benchmark Metrics -->
    <div class="grid-4" style="margin-bottom: 10px;">
      <div class="metric-card">
        <div class="metric-val">720</div>
        <div class="metric-lbl">保留測試單元 (Math16×3×4 組合)</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">342</div>
        <div class="metric-lbl">原始生成失敗案例 (涵蓋語法與邏輯)</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">42</div>
        <div class="metric-lbl">觸發修復規則案例 (命中局部特徵)</div>
      </div>
      <div class="metric-card">
        <div class="metric-val">9</div>
        <div class="metric-lbl">失敗案例安全救回 (救回率 2.63%)</div>
      </div>
    </div>

    <!-- Two Column Reflection and Science Spirit -->
    <div class="grid-2" style="margin-bottom: 10px;">
      <!-- Left: Research Turning Point -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:10px 12px;">
        <div>
          <div class="card-header">
            <div class="card-header-bar"></div>
            研究方法的調整：從初版指標到獨立測試
          </div>
          <div style="font-size:11.2px; color:#334155; line-height:1.48;">
            <b>研究歷程與重新檢視評估方法</b>：<br>
            初版研究參加東區科展取得優等第 2 名（未晉級全國科展）。當時評估使用自訂 MCRI 指標取得 97.41 分，但該數字為綜合指標而非程式通過率，且指標混淆了題型固有通過率與修復機制的因果關係。<br>
            入圍旺宏科學獎全國決賽後，參考評審建議重新設計實驗：建立 12 題獨立保留測試資料（Holdout Dataset），涵蓋 3 種開源小模型與 4 種提示條件，在固定隨機種子下凍結修復規則進行盲測，以客觀呈現修復能力的真實邊界。
          </div>
        </div>
        <div style="background:#f1f5f9; border:1px solid #cbd5e1; border-left:3.5px solid #b45309; border-radius:4px; padding:4px 7px; font-size:10.2px; color:#0f2942; font-weight:700; margin-top:5px;">
          ✦ 第 25 屆旺宏科學獎 全國決賽 20 強（全領域 846 件作品報名，資訊類僅 4 件入選）
        </div>
      </div>

      <!-- Right: Boundary & Conclusion -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:10px 12px;">
        <div>
          <div class="card-header">
            <div class="card-header-bar"></div>
            研究結果與修復機制的限制
          </div>
          <div style="font-size:11.2px; color:#334155; line-height:1.48;">
            <b>能力邊界確立與研究限制</b>：<br>
            實驗證實在 342 個原始失敗案例中，共有 42 個觸發修復規則，最終安全救回 9 個案例（佔失敗案例比例 2.63%）。成功案例高度集中於未引用變數、函式介面命名等局部語法與介面錯誤。<br>
            <b>研究限制與後續方向</b>：固定規則適合處理部分介面、格式及變數相關錯誤；涉及核心解題邏輯的錯誤，仍需要其他驗證或處理方式。後續系統設計建議先以 Scaffold 補齊結構資訊，再以 Healer 進行局部修補。
          </div>
        </div>
        <div style="background:#f1f5f9; border:1px solid #cbd5e1; border-left:3.5px solid #1e3a8a; border-radius:4px; padding:4px 7px; font-size:10.2px; color:#0f2942; font-weight:700; margin-top:5px;">
          ✦ 第 66 屆東區科展 電腦與資訊學科【優等第 2 名】
        </div>
      </div>
    </div>

    <!-- Error Taxonomy Card -->
    <div class="card" style="margin-bottom:0; background:#f8fafc; border:1px solid #cbd5e1; padding:9px 12px;">
      <div style="font-size:11.5px; font-weight:800; color:#0f2942; margin-bottom:5px; display:flex; justify-content:space-between;">
        <span>錯誤分類學與三層修復行為架構（Error Taxonomy）</span>
        <span style="font-size:9.5px; color:#64748b; font-weight:600;">旺宏全國 20 強成果整理</span>
      </div>
      <div class="grid-3" style="font-size:10.2px; line-height:1.42; gap:8px;">
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:2.5px solid #15803d; border-radius:4px; padding:5px 8px;">
          <span style="font-weight:700; color:#15803d; font-size:9.8px; display:block; margin-bottom:2px;">● 可確定修復 (Safe Repair)</span>
          未引用變數清除、介面函式名命名偏差校正、回傳格式不符重構。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:2.5px solid #b45309; border-radius:4px; padding:5px 8px;">
          <span style="font-weight:700; color:#b45309; font-size:9.8px; display:block; margin-bottom:2px;">▲ 語法修復但語義仍錯 (Partial)</span>
          補齊 SyntaxError 語法缺損，但解題數值邏輯仍錯誤（由後端判題器精準攔截）。
        </div>
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-top:2.5px solid #b91c1c; border-radius:4px; padding:5px 8px;">
          <span style="font-weight:700; color:#b91c1c; font-size:9.8px; display:block; margin-bottom:2px;">■ 主動棄權邊界 (Safe Abstention)</span>
          演算法死循環、核心數學原理推導錯誤（避免規則強行修改導致副作用，主動放棄）。
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

<!-- PAGE 4: Back Cover (Soccer on Top, English on Bottom) -->
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
        <div class="page-subtitle">高中校隊聯賽競技經驗 ｜ 語言檢定、在校成績與技術資料研讀能力</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge" style="border-left-color:#1e3a8a;">⚽ 全國五人制聯賽 全國第 5 名</div>
        <div class="header-award-badge" style="margin-top:3px; border-left-color:#b45309;">🌟 TOEIC 945 金色 ｜ GEPT 中高級</div>
      </div>
    </div>

    <!-- UPPER HALF: SOCCER ATHLETICS -->
    <div style="margin-bottom: 11px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <div style="font-size:14.5px; font-weight:900; color:#0f2942; display:flex; align-items:center; gap:6px;">
          <span style="font-size:15px;">⚽</span>
          <span>足球競技｜從國中校隊到高中全國聯賽</span>
        </div>
        <span style="font-size:9.8px; font-weight:700; color:#1e293b; background:#f1f5f9; border:1px solid #cbd5e1; padding:2px 7px; border-radius:4px;">背號 42 號 · 花蓮高中校隊</span>
      </div>

      <!-- Soccer 4 Metrics -->
      <div class="grid-4" style="margin-bottom: 9px;">
        <div class="metric-card">
          <div class="metric-val">全國第 5 名</div>
          <div class="metric-lbl">114學年度五人制聯賽 (高二)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">全國第 6 名</div>
          <div class="metric-lbl">113學年度五人制聯賽 (高一)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">全國第 5 名</div>
          <div class="metric-lbl">全國青年盃五人制公開組</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">縣運亞軍</div>
          <div class="metric-lbl">2025 花蓮縣運社會組</div>
        </div>
      </div>

      <!-- Soccer Content + Team Photo -->
      <div class="grid-2">
        <div style="display:flex; flex-direction:column; justify-content:space-between;">
          <div class="card" style="margin-bottom:8px; padding:10px 12px;">
            <div style="font-size:11.5px; color:#334155; line-height:1.52;">
              <b>校隊經歷與賽事成果</b>：<br>
              國中時擔任花崗國中足球隊隊長，高中持續參加花蓮高中五人制足球校隊。113、114 學年度分別取得全國第 6 名與第 5 名。長期訓練與比賽讓我累積團隊合作、臨場判斷及面對比賽壓力的經驗。
            </div>
            <div style="font-size:10px; color:#0f2942; font-weight:700; margin-top:5px; background:#f1f5f9; border:1px solid #cbd5e1; border-left:3px solid #1e3a8a; padding:3px 7px; border-radius:4px;">
              ✦ 符合教育部運動績優甄試資格 ｜ 114 學年度 5:3 擊敗台中惠文高中獲全國第 5 名
            </div>
          </div>

          <!-- FBref analytics highlight -->
          <div class="card" style="margin-bottom:0; background:#f8fafc; border:1px solid #cbd5e1; padding:8px 11px;">
            <div style="font-size:11.2px; font-weight:800; color:#0f2942; margin-bottom:3px;">
              📊 足球數據分析｜FBref 資料整理與 Python 實作
            </div>
            <div style="font-size:10.8px; color:#475569; line-height:1.45;">
              結合足球與程式設計的興趣，使用 Python 蒐集及整理 FBref 公開足球數據，探索球員與球隊表現的分析方法，將程式實作應用於自己熟悉的運動領域。
            </div>
          </div>
        </div>

        <div class="img-box" style="display:flex; flex-direction:column; justify-content:space-between;">
          <img src="{p('soccer_team_perfect.png')}" style="height:210px; width:100%; object-fit:cover;" alt="花蓮高中足球代表隊合影">
          <div class="img-caption">▲ 114學年度全國中等學校五人制足球聯賽決賽現場：花蓮高中代表隊合影 (前排右四 葉陽甫)</div>
        </div>
      </div>
    </div>

    <!-- DIVIDER -->
    <div style="border-top: 1px solid #cbd5e1; margin: 8px 0 9px 0;"></div>

    <!-- LOWER HALF: ENGLISH PROFICIENCY -->
    <div style="margin-bottom: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <div style="font-size:14.5px; font-weight:900; color:#0f2942; display:flex; align-items:center; gap:6px;">
          <span style="font-size:15px;">🌐</span>
          <span>英文能力｜語言檢定、學業與競賽成果</span>
        </div>
        <span style="font-size:9.8px; font-weight:700; color:#0f2942; background:#f1f5f9; border:1px solid #cbd5e1; padding:2px 7px; border-radius:4px;">CEFR B2+ ｜ 在校英文平均 91 分</span>
      </div>

      <!-- English 4 Metrics -->
      <div class="grid-4" style="margin-bottom: 9px;">
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
          <div class="metric-val">全縣甲等</div>
          <div class="metric-lbl">花蓮縣英文作文競賽</div>
        </div>
      </div>

      <!-- English Content + 2 Certificate Photos (TOEIC Top, GEPT Bottom) -->
      <div class="grid-2">
        <!-- Left: Rewritten English Narrative -->
        <div class="card" style="margin-bottom:0; padding:12px 14px; display:flex; flex-direction:column; justify-content:center;">
          <div style="font-size:11.8px; color:#334155; line-height:1.62;">
            高中期間持續累積英語能力，取得 <b>TOEIC 945 分（金色證書）</b>，並通過<b>全民英檢中高級</b>聽、說、讀、寫四項測驗。<br><br>
            高一至高二英文平均成績 <b>91 分（年級前 4%）</b>，高二下學期 <b>96 分（年級第 7 名 · 前 2%）</b>。此外，也曾參加校內英語演說（初賽第一名、全校複賽第四名）及花蓮縣英文作文競賽（高中組甲等）。<br><br>
            在資訊與程式學習方面，英文能力有助於查閱國外技術資料、理解專業術語及尋找問題的解決方法，也為未來進一步學習專業文獻奠定基礎。
          </div>
        </div>

        <!-- Right: Two Certificates Vertically Stacked -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div class="img-box" style="margin-bottom:0;">
            <img src="{p('english_img2.jpeg')}" style="height:124px; width:100%; object-fit:contain; background:#ffffff;" alt="TOEIC 945 金色證書">
            <div class="img-caption" style="padding:2.5px 6px;">▲ TOEIC 945 金色證書</div>
          </div>
          <div class="img-box" style="margin-bottom:0;">
            <img src="{p('english_img1.jpeg')}" style="height:148px; width:100%; object-fit:contain; background:#ffffff;" alt="GEPT 中高級證書">
            <div class="img-caption" style="padding:2.5px 6px;">▲ GEPT 全民英檢中高級合格</div>
          </div>
        </div>
      </div>
    </div>

    <!-- DIGITAL PORTFOLIO & CONTACT BAR -->
    <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:9px 13px; display:flex; justify-content:space-between; align-items:center;">
      <div style="font-size:10.8px; color:#1e293b; font-weight:700;">
        <span style="color:#0f2942;">📁 作品與專案線上入口：</span><br>
        <span style="color:#475569; font-weight:500;">
          🌐 系統上線網址：<b>mathb.math-adaptive.org</b> ｜ 📄 遮雨棚發明專利簡報：<b>bit.ly/yangfu-invention</b>
        </span>
      </div>
      <div style="font-size:10.5px; color:#334155; font-weight:700; text-align:right;">
        葉陽甫 ｜ 國立花蓮高級中學<br>
        <span style="color:#64748b; font-weight:normal;">誠摯感謝各位教授審閱與指導</span>
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
