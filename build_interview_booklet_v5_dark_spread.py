import os
import subprocess
import fitz
from pathlib import Path

ROOT = Path(r"C:\Projects\yangfu-application")
SRC = ROOT / "陽甫調整" / "其他表現資料"
ASSETS = ROOT / "陽甫調整" / "4頁對折本_assets"
SPREAD_UI = ASSETS / "spread_ui"
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = ROOT / "tmp" / "booklet_v5"
TMP_DIR.mkdir(parents=True, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def build_html():
    def p(fname):
        path = (ASSETS / fname).resolve().as_posix()
        return f"file:///{path}"

    def p_ui(fname):
        path = (SPREAD_UI / fname).resolve().as_posix()
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
    background: #090d16;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
    color: #e2e8f0;
    font-size: 11px;
    line-height: 1.45;
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
    background: #090d16;
    background-image: 
      radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.05) 0%, transparent 40%),
      radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.05) 0%, transparent 40%);
  }}

  /* Top Bar Header */
  .header {{
    border-bottom: 2px solid rgba(255, 255, 255, 0.15);
    padding-bottom: 5px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .header-left {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  .badge-tag {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 9.2px;
    font-weight: 800;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    padding: 2.5px 7px;
    border-radius: 4px;
    width: fit-content;
  }}
  .badge-cyan {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); }}
  .badge-purple {{ background: rgba(192, 132, 252, 0.15); color: #c084fc; border: 1px solid rgba(192, 132, 252, 0.35); }}
  .badge-emerald {{ background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.35); }}
  .badge-amber {{ background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.35); }}
  .badge-spread {{ 
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.3) 0%, rgba(168, 85, 247, 0.3) 100%); 
    color: #ffffff; 
    border: 1px solid rgba(255, 255, 255, 0.3);
    font-weight: 800; 
  }}

  .page-title {{
    font-size: 19.5px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.3px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
  }}
  .page-subtitle {{
    font-size: 10.5px;
    color: #94a3b8;
    font-weight: 500;
  }}
  .header-right {{
    text-align: right;
  }}
  .header-award-badge {{
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.25) 100%);
    border: 1px solid #f59e0b;
    color: #fde68a;
    padding: 2.5px 7px;
    border-radius: 5px;
    font-size: 10px;
    font-weight: 800;
    display: inline-block;
  }}

  /* Grid Layouts */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8.5px;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 7.5px;
  }}
  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 7.5px;
  }}

  /* Dark Metric Cards with Neon Highlights */
  .metric-card {{
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 6px;
    padding: 5px 7px;
    text-align: center;
    position: relative;
    border-top: 3px solid #38bdf8;
  }}
  .metric-card.gold {{ border-top-color: #f59e0b; background: #161b26; }}
  .metric-card.purple {{ border-top-color: #a855f7; background: #171528; }}
  .metric-card.teal {{ border-top-color: #14b8a6; background: #111e24; }}
  .metric-val {{
    font-size: 19.5px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
  }}
  .metric-card.gold .metric-val {{ color: #fbbf24; }}
  .metric-card.teal .metric-val {{ color: #2dd4bf; }}
  .metric-card.purple .metric-val {{ color: #c084fc; }}
  .metric-lbl {{
    font-size: 9.5px;
    color: #94a3b8;
    margin-top: 2px;
    font-weight: 600;
  }}

  /* Dark Content Cards */
  .card {{
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 7px 9px;
    margin-bottom: 6.5px;
  }}
  .card-header {{
    font-size: 12.2px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .card-header-bar {{
    width: 3.5px;
    height: 12px;
    border-radius: 2px;
    background: #38bdf8;
  }}
  .card-header-bar.amber {{ background: #f59e0b; }}
  .card-header-bar.teal {{ background: #14b8a6; }}
  .card-header-bar.purple {{ background: #a855f7; }}

  /* Process Steps */
  .process-step {{
    display: flex;
    gap: 6.5px;
    margin-bottom: 4px;
    align-items: flex-start;
  }}
  .step-num {{
    background: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #38bdf8;
    font-size: 8.5px;
    font-weight: 800;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
  }}
  .step-content {{
    flex: 1;
  }}
  .step-title {{
    font-weight: 700;
    font-size: 11px;
    color: #f1f5f9;
  }}
  .step-desc {{
    font-size: 10.2px;
    color: #94a3b8;
    line-height: 1.35;
  }}

  /* Dark Theme Mockup Window Box */
  .mockup-window {{
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    overflow: hidden;
    background: #0f172a;
    box-shadow: 0 3px 8px rgba(0,0,0,0.35);
    display: flex;
    flex-direction: column;
  }}
  .mockup-bar {{
    background: #1e293b;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 3px 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .mockup-dots {{
    display: flex;
    gap: 3.5px;
  }}
  .mockup-dot {{
    width: 5.5px;
    height: 5.5px;
    border-radius: 50%;
  }}
  .mockup-dot.red {{ background: #f87171; }}
  .mockup-dot.yellow {{ background: #fbbf24; }}
  .mockup-dot.green {{ background: #34d399; }}
  .mockup-title {{
    font-size: 8.8px;
    font-weight: 700;
    color: #94a3b8;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .mockup-caption {{
    font-size: 9px;
    color: #cbd5e1;
    background: #111827;
    padding: 3px 6px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-weight: 600;
    line-height: 1.3;
  }}

  /* Dark Tech Spread Bridge Banners */
  .spread-bridge-p2 {{
    background: linear-gradient(135deg, #0f172a 0%, #0369a1 70%, #0284c7 100%);
    color: #ffffff;
    border-radius: 7px;
    padding: 7.5px 11px;
    margin-top: 5px;
    position: relative;
    border: 1px solid #38bdf8;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
  }}
  .spread-bridge-p3 {{
    background: linear-gradient(135deg, #0284c7 0%, #4338ca 45%, #6b21a8 100%);
    color: #ffffff;
    border-radius: 7px;
    padding: 7.5px 11px;
    margin-bottom: 7.5px;
    position: relative;
    border: 1px solid #c084fc;
    box-shadow: 0 0 12px rgba(192, 132, 252, 0.2);
  }}

  /* Footer */
  .footer {{
    border-top: 1.5px solid rgba(255, 255, 255, 0.12);
    padding-top: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 9.3px;
    color: #64748b;
    font-weight: 500;
  }}

  .img-box {{
    border-radius: 5px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: #0f172a;
  }}
  .img-box img {{
    width: 100%;
    height: auto;
    display: block;
  }}

  .tag-pill {{
    display: inline-block;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 9.3px;
    font-weight: 700;
    margin-right: 3px;
  }}
  .tag-pill.green {{ background: rgba(52, 211, 153, 0.2); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.4); }}
  .tag-pill.amber {{ background: rgba(251, 191, 36, 0.2); color: #fde68a; border: 1px solid rgba(251, 191, 36, 0.4); }}
  .tag-pill.red {{ background: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }}
</style>
</head>
<body>

<!-- PAGE 2: AI Adaptive Learning System (Engineering Project & Rich UI Spread - Dark Tech) -->
<div class="page" id="page2">
  <div>
    <!-- Top Header -->
    <div class="header">
      <div class="header-left">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-cyan">02 / 系統工程篇</span>
          <span class="badge-tag badge-spread">跨頁連動主線 (左面) · 課堂工程實戰</span>
        </div>
        <h1 class="page-title">
          AI 自適應輔助學習系統
        </h1>
        <div class="page-subtitle">從真實教學痛點出發，落實於高中課堂長期維運的完整自適應平台（正式上線運作）</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge">🏆 神通扶輪盃 全國第一名 冠軍</div>
        <div class="header-award-badge" style="margin-top:3px; background:linear-gradient(135deg, rgba(234, 88, 12, 0.25) 0%, rgba(194, 65, 12, 0.3) 100%); border-color:#ea580c; color:#fdba74;">🥇 育秀盃創意獎 全國金獎 (10萬元)</div>
      </div>
    </div>

    <!-- 4 Key Metrics -->
    <div class="grid-4" style="margin-bottom: 7.5px;">
      <div class="metric-card teal">
        <div class="metric-val">2 班</div>
        <div class="metric-lbl">正式課堂持續使用</div>
      </div>
      <div class="metric-card teal">
        <div class="metric-val">50 人</div>
        <div class="metric-lbl">真實高中學生帳號</div>
      </div>
      <div class="metric-card teal">
        <div class="metric-val">1,224 次</div>
        <div class="metric-lbl">累積實際作答次數</div>
      </div>
      <div class="metric-card teal">
        <div class="metric-val">67%</div>
        <div class="metric-lbl">全體平均答對率</div>
      </div>
    </div>

    <!-- Main Section: Left = Engineering Core, Right = Rich System UI Showcase -->
    <div class="grid-2" style="margin-bottom: 6.5px;">
      <!-- Left Column: Problem, Modules, Algorithm -->
      <div>
        <div class="card" style="margin-bottom:5.5px; border-left: 3px solid #38bdf8; padding:5.5px 8.5px;">
          <div class="card-header" style="margin-bottom:2px; font-size:11.8px;">起點問題與真實需求拆解</div>
          <div style="font-size:10.4px; color:#cbd5e1; line-height:1.4;">
            父親為技術型高中數學老師，長年面臨<b>「題目難以數位化批次輸入、固定題庫無法反覆變題練習、課堂學生雙峰差距極大」</b>之教學痛點。我著手自研自適應學習系統，拒做紙上 Demo，落實於花蓮高中班級正式上線運作。
          </div>
        </div>

        <div class="card" style="margin-bottom:5.5px; padding:5.5px 8.5px;">
          <div class="card-header" style="margin-bottom:3px; font-size:11.8px;">
            <div class="card-header-bar"></div>
            三大核心技術模組流程
          </div>
          <div class="process-step">
            <div class="step-num">1</div>
            <div class="step-content">
              <div class="step-title">結構化教材解析與匯入</div>
              <div class="step-desc">解析 Word/PDF 講義，自動對齊章節知識點樹，保留教師最後審核調整權。</div>
            </div>
          </div>
          <div class="process-step">
            <div class="step-num">2</div>
            <div class="step-content">
              <div class="step-title">Code-as-Content 程式即內容出題</div>
              <div class="step-desc">讓 AI 依題型建立 Python 出題腳本，動態生成無窮數值變體與精確標準答案。</div>
            </div>
          </div>
          <div class="process-step" style="margin-bottom:0;">
            <div class="step-num">3</div>
            <div class="step-content">
              <div class="step-title">嚴格數學判題器 × AI 助教導航</div>
              <div class="step-desc">公式由嚴格程式運算，杜絕 AI 幻覺；AI 僅負責思維引導與手寫輔導。</div>
            </div>
          </div>
        </div>

        <!-- Adaptive Loop -->
        <div class="card" style="margin-bottom:0; background:rgba(6, 78, 59, 0.25); border:1px solid rgba(52, 211, 153, 0.35); padding:5.5px 8.5px;">
          <div style="font-size:10.8px; font-weight:800; color:#6ee7b7; margin-bottom:2px;">
            🔄 自適應閉環路徑演算法 (學生端作答迴路)
          </div>
          <div style="font-size:9.8px; color:#a7f3d0; line-height:1.35;">
            <b>學生作答 ➔ 能力診斷 ➔ 適性決策 ➔ 補強/繼續 ➔ 再次評量</b><br>
            系統整合知識狀態診斷，動態判斷掌握盲點；若前置基礎不穩，自動引導回前置技能複習；熟練則前進高階題目。
          </div>
        </div>
      </div>

      <!-- Right Column: Prominent System UI Showcase (Rich & Clear) -->
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3.5px;">
          <span style="font-size:11.4px; font-weight:800; color:#38bdf8;">🖥️ 真實課堂運作系統介面巡禮</span>
          <span style="font-size:9.2px; color:#94a3b8; font-weight:700;">跨頁連動展示 ➔</span>
        </div>
        
        <!-- Large Featured Screen: Math Practice with LaTeX & Handwriting -->
        <div class="mockup-window" style="margin-bottom:4.5px;">
          <div class="mockup-bar">
            <div class="mockup-dots"><div class="mockup-dot red"></div><div class="mockup-dot yellow"></div><div class="mockup-dot green"></div></div>
            <div class="mockup-title">學生作答介面 · LaTeX 動態公式渲染與數位手寫區</div>
          </div>
          <img style="width:100%; height:74px; object-fit:cover; object-position:top;" src="{p_ui('ui_math_practice.jpg')}" alt="學生作答介面">
          <div class="mockup-caption">
            動態渲染 LaTeX 題目、支援手寫作答與步驟引導，杜絕大模型數理幻覺。
          </div>
        </div>

        <!-- 2 Side-by-Side Screens: Learning Trend & Teacher Dashboard -->
        <div class="grid-2" style="gap:4.5px; margin-bottom:4.5px;">
          <!-- Screen: Learning Trend -->
          <div class="mockup-window">
            <div class="mockup-bar">
              <div class="mockup-dots"><div class="mockup-dot red"></div><div class="mockup-dot yellow"></div><div class="mockup-dot green"></div></div>
              <div class="mockup-title">學生學習趨勢</div>
            </div>
            <img style="width:100%; height:60px; object-fit:cover; object-position:top;" src="{p_ui('ui_learning_trend.jpg')}" alt="學習趨勢">
            <div class="mockup-caption">即時掌握答對率與熟練度累積曲線</div>
          </div>
          <!-- Screen: Teacher Dashboard -->
          <div class="mockup-window">
            <div class="mockup-bar">
              <div class="mockup-dots"><div class="mockup-dot red"></div><div class="mockup-dot yellow"></div><div class="mockup-dot green"></div></div>
              <div class="mockup-title">導師大數據後台</div>
            </div>
            <img style="width:100%; height:60px; object-fit:cover; object-position:top;" src="{p_ui('ui_teacher_dash.jpg')}" alt="導師後台">
            <div class="mockup-caption">全班即時進度雷達與分層補強建議</div>
          </div>
        </div>

        <!-- Awards & Official URL info -->
        <div style="background:#111827; border:1px solid rgba(255, 255, 255, 0.1); border-radius:5px; padding:4px 7px; display:flex; justify-content:space-between; align-items:center;">
          <div style="font-size:9.3px; color:#94a3b8; line-height:1.35;">
            🌐 系統正式網址：<b style="color:#38bdf8;">mathb.math-adaptive.org</b><br>
            👤 研發職責：全端架構、前端/後端、出題引擎（貢獻度 70%）
          </div>
          <div style="display:flex; gap:4px;">
            <img src="{p('yuxiu_img1.png')}" style="height:34px; border:1px solid #f59e0b; border-radius:3px;" alt="育秀金獎">
            <img src="{p('rotary_img_3.jpeg')}" style="height:34px; border:1px solid #38bdf8; border-radius:3px;" alt="扶輪冠軍">
          </div>
        </div>
      </div>
    </div>

    <!-- Full-Stack Architecture -->
    <div class="card" style="margin-bottom: 5.5px; padding: 5.5px 8.5px; background: #0f172a;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
        <span style="font-size: 11.4px; font-weight: 800; color: #f8fafc;">全端工程架構與真實課堂維運 (Full-Stack & DevOps)</span>
        <span style="font-size: 9px; color: #38bdf8; font-weight: 700;">班級實體部署 · 微服務架構</span>
      </div>
      <div class="grid-3" style="font-size: 9.8px; line-height: 1.35; gap: 6.5px;">
        <div style="background:#1e293b; border:1px solid rgba(255,255,255,0.06); border-radius:4px; padding:4.5px 6.5px;">
          <b style="color:#38bdf8;">🖥️ 前端作答與公式渲染</b><br>
          Next.js / React 全端架構，整合 KaTeX 動態解析數學符號與 LaTeX 公式，支援幾何 Canvas 動態互動與座標繪圖。
        </div>
        <div style="background:#1e293b; border:1px solid rgba(255,255,255,0.06); border-radius:4px; padding:4.5px 6.5px;">
          <b style="color:#38bdf8;">⚙️ 後端非同步與數理判題</b><br>
          FastAPI 高併發非同步處理，自研 SymPy 符號運算等價性驗證引擎，精確判別數學等解，杜絕大型模型數理幻覺。
        </div>
        <div style="background:#1e293b; border:1px solid rgba(255,255,255,0.06); border-radius:4px; padding:4.5px 6.5px;">
          <b style="color:#38bdf8;">🚀 容器部署與正式維運</b><br>
          Docker 容器化封裝、Nginx 反向代理、PostgreSQL 狀態追蹤，克服真實課堂「公式手寫辨識、缺參數、變題碰撞」考驗。
        </div>
      </div>
    </div>

    <!-- SPREAD BRIDGE BANNER (LEFT SIDE): Connecting P2 into P3 -->
    <div class="spread-bridge-p2">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3.5px;">
        <div style="font-size:11.8px; font-weight:900; letter-spacing:0.2px; display:flex; align-items:center; gap:6px;">
          <span>⚡ 跨頁主線對接：課堂落地遭遇的致命工程瓶頸 ➔ 抽離問題啟動科研</span>
        </div>
        <span style="background:#38bdf8; color:#0b0f19; font-weight:900; font-size:9.5px; padding:2px 7px; border-radius:4px;">
          接續右頁科研 ➔➔
        </span>
      </div>
      <div class="grid-2" style="font-size:10.2px; line-height:1.38; gap:7px; margin-bottom:3px;">
        <div style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:4px; padding:4px 6.5px;">
          <b>☁️ 雲端大型模型瓶頸</b>：課堂高頻呼叫 API 造成高昂費用與連線延遲，且涉及校園學生資料外洩；全面推動邊緣端（Edge AI）部署勢在必行。
        </div>
        <div style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:4px; padding:4px 6.5px;">
          <b>💻 本地小模型（SLM）生成崩潰</b>：邊緣端小模型生成出題程式時頻爆 <b>SyntaxError 語法缺損、未引用變數、介面格式偏差</b>；重產耗算力且不收斂。
        </div>
      </div>
      <div style="font-size:10.2px; color:#7dd3fc; font-weight:600; line-height:1.32;">
        💡 <b>核心研究假說</b>：「如何在無正確答案（Ground Truth）前提下，以確定性規則在邊緣端安全修復局部程式碼？」——這個真實工程卡點，催生了右頁深層語法樹科研！
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span>葉陽甫 · 國立花蓮高級中學 ｜ 特殊選才面試精華摺頁冊</span>
    <span>第 2 頁 · 系統工程篇 (跨頁左面 · 真實課堂落地)</span>
  </div>
</div>

<!-- PAGE 3: AST Active Healer Research (Scientific Research & Spread Continuation - Dark Tech) -->
<div class="page" id="page3">
  <div>
    <!-- Top Header -->
    <div class="header">
      <div class="header-left">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-purple">03 / 科學研究篇</span>
          <span class="badge-tag badge-spread">跨頁連動主線 (右面) · 深化編譯科研</span>
        </div>
        <h1 class="page-title">
          AST Active Healer 程式生成可靠性
        </h1>
        <div class="page-subtitle">從工程痛點抽離的純學術探索：以抽象語法樹與確定性修復突破生成邊界</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge" style="background:linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.3) 100%); border-color:#d97706; color:#fde68a;">🏅 第25屆旺宏科學獎 全國決賽20強</div>
        <div class="header-award-badge" style="margin-top:3px; background:rgba(255, 255, 255, 0.08); border-color:#64748b; color:#cbd5e1;">🎖️ 第66屆東區科展 優等第2名</div>
      </div>
    </div>

    <!-- SPREAD BRIDGE BANNER (RIGHT SIDE): Matching P2 Transition -->
    <div class="spread-bridge-p3">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3.5px;">
        <span style="background:#c084fc; color:#0b0f19; font-weight:900; font-size:9.5px; padding:2px 7px; border-radius:4px;">
          ◄◄ 承接左頁課堂痛點
        </span>
        <div style="font-size:11.8px; font-weight:900; letter-spacing:0.2px;">
          🔬 科研問題意識：把真實痛點抽離為嚴謹的科學假說
        </div>
      </div>
      <div style="font-size:10.4px; line-height:1.4; color:#f8fafc;">
        抽離特定數學業務，將問題聚焦為<b>「小模型生成受限環境程式的局部修復能力與邊界」</b>。設計以固定規則運作的 AST Active Healer，探索不將錯誤重新丟回模型黑箱、直接在語法樹層級進行確定性修復的極限。
      </div>
    </div>

    <!-- 4 Rigorous Benchmark Metrics (Aligned with P2 Metrics) -->
    <div class="grid-4" style="margin-bottom: 7.5px;">
      <div class="metric-card gold">
        <div class="metric-val">720</div>
        <div class="metric-lbl">正式保留測試單元 (Math16×3×4)</div>
      </div>
      <div class="metric-card gold">
        <div class="metric-val">342</div>
        <div class="metric-lbl">原始程式生成失敗 (涵蓋語法與邏輯)</div>
      </div>
      <div class="metric-card gold">
        <div class="metric-val">42</div>
        <div class="metric-lbl">觸發靜態修復規則 (命中局部特徵)</div>
      </div>
      <div class="metric-card gold">
        <div class="metric-val">9</div>
        <div class="metric-lbl">成功安全救回 (無副作用 2.63%)</div>
      </div>
    </div>

    <!-- Core Mechanism Diagram & Benchmark Chart (Side-by-Side) -->
    <div class="grid-2" style="margin-bottom: 7.5px; align-items: stretch;">
      <!-- Left: AST Active Healer Flowchart -->
      <div class="card" style="padding: 6.5px 8.5px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 3px; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 5px;">
            <div class="card-header-bar purple"></div>
            <span style="font-size: 11.4px; font-weight: 800;">AST Healer 三階段主動修復流程</span>
          </div>
          <span style="font-size: 8.8px; color: #c084fc; font-weight: 700;">語法樹靜態解析架構</span>
        </div>
        <div class="img-box" style="border: 1px solid rgba(255,255,255,0.08); margin-bottom: 3.5px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff; border-radius: 4px; padding: 2px;">
          <img src="{p('healer_flowchart.png')}" style="height: 202px; width: 100%; object-fit: contain;" alt="AST Healer 流程圖">
        </div>
        <div style="background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 4px; padding: 4px 6px; font-size: 9.5px; color: #cbd5e1; line-height: 1.32;">
          <b>修復機制管線</b>：① <b>Scaffold 骨架</b>約束合約 ➔ ② <b>AST 解析</b>捕捉語法樹與未引用變數 ➔ ③ <b>確定性修復</b>安全局部，超限則<b>主動棄權 (Abstain)</b>。
        </div>
      </div>

      <!-- Right: Benchmark Experiment Chart (User Added) -->
      <div class="card" style="padding: 6.5px 8.5px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 3px; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 5px;">
            <div class="card-header-bar amber"></div>
            <span style="font-size: 11.4px; font-weight: 800;">4 種 Prompt × 3 模型盲測救援率</span>
          </div>
          <span style="font-size: 8.8px; color: #fbbf24; font-weight: 700;">旺宏決賽嚴格測試集</span>
        </div>
        <div class="img-box" style="border: 1px solid rgba(255,255,255,0.08); margin-bottom: 3.5px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff; border-radius: 4px; padding: 2px;">
          <img src="{p('healer_chart_user.png')}" style="height: 202px; width: 100%; object-fit: contain;" alt="盲測救援率柱狀圖">
        </div>
        <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 4px; padding: 4px 6px; font-size: 9.5px; color: #fde68a; line-height: 1.32;">
          <b>實驗洞察</b>：Gemini 基準較高；Qwen 在 Ab2d+spec 表現最佳；342 格失敗中僅 9 格安全救回（2.63%），確證確定性工具應守住安全邊界，不強行修補深度語義。
        </div>
      </div>
    </div>

    <!-- Two Column Reflection and Science Spirit -->
    <div class="grid-2" style="margin-bottom: 7.5px;">
      <!-- Left: Research Turning Point -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:7.5px 9.5px;">
        <div>
          <div class="card-header" style="font-size:11.6px;">
            <div class="card-header-bar amber"></div>
            研究轉折：推翻虛高分數的求真態度
          </div>
          <div style="font-size:10.3px; color:#cbd5e1; line-height:1.4;">
            <b>從 97.41 到獨立測試集的震撼教育</b>：<br>
            初版研究曾以自建 MCRI 指標取得 97.41 高分。但在東區科展評審提問與未晉級反思中，我意識到指標混淆了「題型固有通過率」與「修復機制獨立因果」。進入旺宏決賽後，我<b>果斷推翻虛高分數</b>，以 Math16 題庫、3 種模型、4 種提示條件與固定隨機種子，建立 12 題嚴格保留測試集，凍結修復規則進行盲測。
          </div>
        </div>
        <div style="background:rgba(245, 158, 11, 0.15); border:1px solid rgba(245, 158, 11, 0.35); border-radius:4px; padding:3px 6px; font-size:9.6px; color:#fde68a; font-weight:700; margin-top:4px;">
          ✦ 旺宏全領域 846 件作品報名 · 進入全國決賽 20 強（電腦資訊類僅 4 件入選）
        </div>
      </div>

      <!-- Right: Boundary & Conclusion -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:7.5px 9.5px;">
        <div>
          <div class="card-header" style="font-size:11.6px;">
            <div class="card-header-bar amber"></div>
            能力邊界確立與研究收束
          </div>
          <div style="font-size:10.3px; color:#cbd5e1; line-height:1.4;">
            <b>看清工具的極限，才是真正的科學</b>：<br>
            實驗證實 9/342 被安全救回，救援成功率 2.63%。成功案例高度集中於介面、格式與變數流等局部錯誤；而牽涉解題推理與演算法邏輯之錯誤，不可交由固定規則硬修。<br>
            <b>最終結論</b>：在系統落地時，應<b>「先以 Scaffold 補齊領域工具與流程資訊，再以 Healer 進行確定性局部修補」</b>，形成完整工程閉環。
          </div>
        </div>
        <div style="background:rgba(52, 211, 153, 0.15); border:1px solid rgba(52, 211, 153, 0.35); border-radius:4px; padding:3px 6px; font-size:9.6px; color:#6ee7b7; font-weight:700; margin-top:4px;">
          ✦ 第 66 屆東區科展 電腦與資訊學科【優等第 2 名】
        </div>
      </div>
    </div>

    <!-- Error Taxonomy Card -->
    <div class="card" style="margin-bottom:0; background:#0f172a; border:1px solid rgba(255,255,255,0.1); padding:6.5px 9.5px;">
      <div style="font-size:10.8px; font-weight:800; color:#f8fafc; margin-bottom:3.5px; display:flex; justify-content:space-between;">
        <span>錯誤分類學與三層修復行為架構（Error Taxonomy）</span>
        <span style="font-size:9px; color:#94a3b8;">旺宏全國 20 強深化成果</span>
      </div>
      <div class="grid-3" style="font-size:9.6px; line-height:1.32; gap:6.5px;">
        <div style="background:#1e293b; border:1px solid rgba(52, 211, 153, 0.3); border-radius:4px; padding:3.5px 5.5px;">
          <span class="tag-pill green" style="margin-bottom:2px; display:inline-block;">可確定修復 (Safe Repair)</span><br>
          未引用變數清除、介面函式名命名偏差校正、回傳格式不符重構。
        </div>
        <div style="background:#1e293b; border:1px solid rgba(251, 191, 36, 0.3); border-radius:4px; padding:3.5px 5.5px;">
          <span class="tag-pill amber" style="margin-bottom:2px; display:inline-block;">語法修復但語義仍錯 (Partial)</span><br>
          補齊 SyntaxError 語法缺損，但解題數值邏輯仍錯誤（交由判題器精準攔截）。
        </div>
        <div style="background:#1e293b; border:1px solid rgba(239, 68, 68, 0.3); border-radius:4px; padding:3.5px 5.5px;">
          <span class="tag-pill red" style="margin-bottom:2px; display:inline-block;">主動棄權邊界 (Safe Abstention)</span><br>
          演算法死循環、核心數學原理推導錯誤、模型幻覺（嚴禁以規則硬修，主動棄權）。
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span>葉陽甫 · 國立花蓮高級中學 ｜ 特殊選才面試精華摺頁冊</span>
    <span>第 3 頁 · 科學研究篇 (跨頁右面 · 深化科研)</span>
  </div>
</div>

<!-- PAGE 4: Back Cover (Soccer on Top, English on Bottom - Dark Tech) -->
<div class="page" id="page4">
  <div>
    <!-- Top Header -->
    <div class="header">
      <div class="header-left">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-emerald">04 / 跨域實踐篇</span>
          <span class="badge-tag badge-amber">多元表現 · 體育競技與國際語文</span>
        </div>
        <h1 class="page-title">
          綠茵競技與國際視野
        </h1>
        <div class="page-subtitle">花中足球隊主力防守中場 · 全國高中五人制錦標賽第 5 名 ｜ 英文日常工具 · TOEIC 945 / GEPT 中高級</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge" style="background:linear-gradient(135deg, rgba(22, 163, 74, 0.25) 0%, rgba(21, 128, 61, 0.3) 100%); border-color:#16a34a; color:#86efac;">⚽ 全國錦標賽 全國第五名</div>
        <div class="header-award-badge" style="margin-top:3px; background:linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.3) 100%); border-color:#f59e0b; color:#fde68a;">🏆 多益 945 金色證書</div>
      </div>
    </div>

    <!-- PART A: High School Soccer -->
    <div style="margin-bottom: 8.5px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4.5px;">
        <div style="font-size:12.8px; font-weight:800; color:#f8fafc; display:flex; align-items:center; gap:6px;">
          <span style="font-size:14px;">⚽</span>
          <span>競技運動領導力：花蓮高中足球隊 (111-113學年度主力防守中場 #14)</span>
        </div>
        <span style="font-size:9.5px; color:#34d399; font-weight:700;">全國五人制第 5 名 · 11人制全國預賽晉級</span>
      </div>

      <!-- 4 Soccer Metrics -->
      <div class="grid-4" style="margin-bottom: 5.5px;">
        <div class="metric-card teal">
          <div class="metric-val">全國第 5</div>
          <div class="metric-lbl">112學年全國五人制錦標賽</div>
        </div>
        <div class="metric-card teal">
          <div class="metric-val">3 年主力</div>
          <div class="metric-lbl">身披 14 號 · 防守中場樞紐</div>
        </div>
        <div class="metric-card teal">
          <div class="metric-val">800+ 小時</div>
          <div class="metric-lbl">晨操夜訓 · 兼顧頂尖課業</div>
        </div>
        <div class="metric-card teal">
          <div class="metric-val">隊史最佳</div>
          <div class="metric-lbl">花中歷屆普通班最優戰績</div>
        </div>
      </div>

      <!-- Soccer Content + Full Team Photo + Action Shots -->
      <div class="grid-2" style="margin-bottom: 4.5px;">
        <div class="card" style="margin-bottom:0; padding:6.5px 8.5px; display:flex; flex-direction:column; justify-content:space-between;">
          <div style="font-size:10.5px; color:#cbd5e1; line-height:1.4;">
            <b>防守中場（Holding Midfielder）：球場上的系統架構師</b><br>
            足球是我人格特質最重要的淬鍊場。身為全隊攻守轉換的中樞，我必須在極短時間內掃描全場空間、預判對手傳球線路、指揮防線站位，並在巨大比分壓力下做出冷靜且最優化的出球決策。<br>
            這種<b>「高壓抗壓性、全局戰略視野、溝通協調能力與團隊自驅力」</b>，正是支持我獨立主導高難度 AI 自適應系統開發與科研攻關的核心動能。
          </div>
          <div style="background:rgba(52, 211, 153, 0.15); border:1px solid rgba(52, 211, 153, 0.35); border-radius:4px; padding:3px 5.5px; font-size:9.4px; color:#6ee7b7; font-weight:700; margin-top:3.5px;">
            ✦ 普通班學生挑戰體育班傳統強權，以無畏韌性寫下花中普通班隊史最佳紀錄！
          </div>
        </div>

        <div class="grid-2" style="gap:4.5px;">
          <div class="img-box">
            <img src="{p('soccer_img1.jpeg')}" style="height:96px; object-fit:cover;" alt="花中足球隊先發陣容">
            <div style="font-size:8.8px; color:#94a3b8; text-align:center; padding:2px; background:#111827;">▲ 全國錦標賽先發陣容 (前排右一)</div>
          </div>
          <div class="img-box">
            <img src="{p('soccer_img4.jpeg')}" style="height:96px; object-fit:cover;" alt="賽事進球慶祝">
            <div style="font-size:8.8px; color:#94a3b8; text-align:center; padding:2px; background:#111827;">▲ 關鍵進球慶祝與團隊默契</div>
          </div>
        </div>
      </div>

      <!-- Soccer Wide Panoramic Team Photo -->
      <div class="img-box" style="margin-bottom:0;">
        <img src="{p('soccer_team_perfect.png')}" style="height:56px; object-fit:cover; object-position:center 38%;" alt="花蓮高中足球隊全體合影">
        <div style="font-size:8.8px; color:#94a3b8; text-align:center; padding:2px; background:#111827;">▲ 花蓮高中足球隊全體隊職員與教練於全國賽事合影 (全隊凝聚力與光榮時刻)</div>
      </div>
    </div>

    <!-- PART B: English Competency -->
    <div style="margin-bottom: 6.5px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3.5px;">
        <div style="font-size:12.8px; font-weight:800; color:#f8fafc; display:flex; align-items:center; gap:6px;">
          <span style="font-size:14px;">🌐</span>
          <span>國際學術與科技溝通：英語作為探索前沿技術的日常工具</span>
        </div>
        <span style="font-size:9.5px; color:#fbbf24; font-weight:700;">TOEIC 945 · 全民英檢中高級合格</span>
      </div>

      <!-- 4 English Metrics -->
      <div class="grid-4" style="margin-bottom: 4.5px;">
        <div class="metric-card gold">
          <div class="metric-val">945 分</div>
          <div class="metric-lbl">TOEIC 金色證書 (頂標)</div>
        </div>
        <div class="metric-card gold">
          <div class="metric-val">中高級</div>
          <div class="metric-lbl">GEPT 全民英檢通過 (B2高標)</div>
        </div>
        <div class="metric-card gold">
          <div class="metric-val">485 / 460</div>
          <div class="metric-lbl">多益聽力 / 閱讀</div>
        </div>
        <div class="metric-card gold">
          <div class="metric-val">全縣甲等</div>
          <div class="metric-lbl">花蓮縣英文作文競賽</div>
        </div>
      </div>

      <!-- English Content + 2 Certificate Photos -->
      <div class="grid-2">
        <div style="display:flex; flex-direction:column; justify-content:space-between;">
          <div class="card" style="margin-bottom:4.5px; padding:6.5px 8.5px;">
            <div style="font-size:10.3px; color:#cbd5e1; line-height:1.4;">
              <b>英文是探索世界與前沿知識的日常工具</b>：<br>
              在執行 AST Healer 研究與自適應系統時，我能<b>直接研讀 arXiv 上最新出爐的 AI、編譯器與軟體工程英文論文</b>，精準理解數學公式、演算法推導與國際 Benchmark 設計。<br>
              高一至高二英文累積成績校排前 4%（高二下 96 分、校排第 7・前 2%）；榮獲花蓮縣英文作文競賽高中組甲等、校內英語演說初賽第一名。
            </div>
          </div>

          <!-- Academic Paper & Open Source Card -->
          <div class="card" style="margin-bottom:0; background:rgba(245, 158, 11, 0.12); border:1px solid rgba(245, 158, 11, 0.3); padding:4.5px 7.5px;">
            <div style="font-size:10.3px; font-weight:800; color:#fbbf24; margin-bottom:2px;">
              📚 前沿學術研讀 × 國際開源技術生態接軌
            </div>
            <div style="font-size:9.6px; color:#fde68a; line-height:1.33;">
              高中期間直接研讀國外頂會 AI 前沿論文（Tree-of-Thoughts、Self-Refine、SWE-bench），並流暢研讀 PyTorch、FastAPI 官方技術文件，具備國際學術發表與跨國技術協作實力。
            </div>
          </div>
        </div>

        <div class="grid-2" style="gap:4.5px;">
          <div class="img-box" style="background:#ffffff; padding:2px;">
            <img src="{p('english_img1.jpeg')}" style="height:138px; object-fit:contain;" alt="GEPT 中高級證書">
            <div style="font-size:8.8px; color:#64748b; text-align:center; padding:1.5px; background:#f8fafc;">▲ GEPT 全民英檢中高級合格</div>
          </div>
          <div class="img-box" style="background:#ffffff; padding:2px;">
            <img src="{p('english_img2.jpeg')}" style="height:138px; object-fit:contain;" alt="TOEIC 945 金色證書">
            <div style="font-size:8.8px; color:#64748b; text-align:center; padding:1.5px; background:#f8fafc;">▲ TOEIC 945 金色證書</div>
          </div>
        </div>
      </div>
    </div>

    <!-- DIGITAL PORTFOLIO & CONTACT BAR -->
    <div style="background:#0f172a; border:1px solid rgba(56, 189, 248, 0.35); border-radius:6px; padding:5.5px 9px; display:flex; justify-content:space-between; align-items:center;">
      <div style="font-size:10px; color:#f8fafc; font-weight:700;">
        <span style="color:#38bdf8;">📁 數位作品與開源專案線上入口：</span><br>
        <span style="color:#94a3b8; font-weight:500;">
          🌐 系統正式上線網址：<b style="color:#ffffff;">mathb.math-adaptive.org</b> ｜ 📄 遮雨棚發明專利簡報：<b style="color:#ffffff;">bit.ly/yangfu-invention</b>
        </span>
      </div>
      <div style="font-size:9.5px; color:#cbd5e1; font-weight:700; text-align:right;">
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
    html_file = TMP_DIR / "pages_234_dark_spread.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Wrote HTML to {html_file}")

    # Render via Chrome headless
    pdf_234 = TMP_DIR / "pages_234_dark_spread.pdf"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_234}",
        str(html_file)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Chrome error:", res.stderr)
        return
    print(f"Rendered {pdf_234} successfully ({os.path.getsize(pdf_234)} bytes)")

    # Assemble A4 4-Page Reading PDF
    cover_pdf = SRC / "00_葉陽甫備審資料首頁.pdf"
    cover_doc = fitz.open(cover_pdf)
    doc_234 = fitz.open(pdf_234)

    booklet = fitz.open()
    booklet.insert_pdf(cover_doc) # P1
    booklet.insert_pdf(doc_234)    # P2, P3, P4

    out_a4 = OUT_DIR / "葉陽甫_面試四面小冊_深色科技旗艦版_A4.pdf"
    booklet.save(out_a4, garbage=4, deflate=True)
    print(f"Saved A4 booklet: {out_a4} ({len(booklet)} pages)")

    # Assemble A3 Landscape Duplex Printable PDF
    a3_doc = fitz.open()
    a3_w, a3_h = 1190.55, 841.89 # A3 landscape points (420mm x 297mm)

    for left_idx, right_idx in [(3, 0), (1, 2)]:
        sheet = a3_doc.new_page(width=a3_w, height=a3_h)
        sheet.show_pdf_page(fitz.Rect(0, 0, a3_w / 2, a3_h), booklet, left_idx)
        sheet.show_pdf_page(fitz.Rect(a3_w / 2, 0, a3_w, a3_h), booklet, right_idx)

    out_a3 = OUT_DIR / "葉陽甫_面試四面小冊_深色科技旗艦版_A3雙面列印.pdf"
    a3_doc.save(out_a3, garbage=4, deflate=True)
    print(f"Saved A3 printable booklet: {out_a3} ({len(a3_doc)} sheets)")

    # Render preview images
    preview_dir = ROOT / "tmp" / "booklet_v5_preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(booklet):
        pix = p.get_pixmap(dpi=150)
        pix.save(str(preview_dir / f"a4_p{i+1}.png"))
    for i, p in enumerate(a3_doc):
        pix = p.get_pixmap(dpi=150)
        pix.save(str(preview_dir / f"a3_sheet{i+1}.png"))
    print(f"Previews saved to {preview_dir}")

if __name__ == "__main__":
    main()
