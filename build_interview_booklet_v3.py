import os
import subprocess
import fitz
from pathlib import Path

ROOT = Path(r"C:\Projects\yangfu-application")
SRC = ROOT / "陽甫調整" / "其他表現資料"
ASSETS = ROOT / "陽甫調整" / "4頁對折本_assets"
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = ROOT / "tmp" / "booklet_v3"
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
    padding: 13mm 14mm 12mm 14mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    background: #ffffff;
  }}

  /* Top Bar Header */
  .header {{
    border-bottom: 2.5px solid #0f2942;
    padding-bottom: 7px;
    margin-bottom: 11px;
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
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    padding: 2.5px 8px;
    border-radius: 4px;
    width: fit-content;
  }}
  .badge-blue {{ background: #e0f2fe; color: #0369a1; }}
  .badge-purple {{ background: #f3e8ff; color: #6b21a8; }}
  .badge-teal {{ background: #ccfbf1; color: #0f766e; }}
  .badge-amber {{ background: #fef3c7; color: #b45309; }}

  .page-title {{
    font-size: 20.5px;
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
  .header-award-badge {{
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border: 1px solid #f59e0b;
    color: #78350f;
    padding: 3.5px 9px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 800;
    display: inline-block;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
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

  /* Metric Cards */
  .metric-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 7px;
    padding: 7px 10px;
    text-align: center;
    border-top: 3.5px solid #0284c7;
  }}
  .metric-card.gold {{ border-top-color: #d97706; background: #fffdfa; }}
  .metric-card.teal {{ border-top-color: #0d9488; background: #fafffe; }}
  .metric-card.navy {{ border-top-color: #1e3a8a; background: #f8faff; }}
  .metric-card.purple {{ border-top-color: #9333ea; background: #faf5ff; }}
  .metric-val {{
    font-size: 21px;
    font-weight: 900;
    color: #0f2942;
    line-height: 1.1;
  }}
  .metric-card.gold .metric-val {{ color: #b45309; }}
  .metric-card.teal .metric-val {{ color: #0f766e; }}
  .metric-card.purple .metric-val {{ color: #7e22ce; }}
  .metric-lbl {{
    font-size: 10px;
    color: #64748b;
    margin-top: 3px;
    font-weight: 600;
  }}

  /* Content Cards */
  .card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 7px;
    padding: 10px 12px;
    margin-bottom: 9px;
  }}
  .card-header {{
    font-size: 13.5px;
    font-weight: 800;
    color: #0f2942;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .card-header-bar {{
    width: 4px;
    height: 14px;
    border-radius: 2px;
    background: #0284c7;
  }}
  .card-header-bar.amber {{ background: #d97706; }}
  .card-header-bar.teal {{ background: #0d9488; }}
  .card-header-bar.purple {{ background: #9333ea; }}

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
    font-size: 12px;
    color: #0f2942;
  }}
  .step-desc {{
    font-size: 11px;
    color: #475569;
    line-height: 1.4;
  }}

  /* Hook Bridge Card connecting P2 and P3 */
  .bridge-card {{
    background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
    border: 2px dashed #0284c7;
    border-radius: 8px;
    padding: 11px 14px;
    margin-top: 7px;
  }}
  .bridge-title {{
    font-size: 13px;
    font-weight: 800;
    color: #0369a1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
  }}
  .bridge-desc {{
    font-size: 11.2px;
    color: #1e3a8a;
    line-height: 1.48;
  }}

  .p3-bridge-card {{
    background: linear-gradient(135deg, #fefce8 0%, #f0fdf4 100%);
    border: 1.8px solid #ca8a04;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 10px;
  }}

  /* Footer */
  .footer {{
    border-top: 1.5px solid #e2e8f0;
    padding-top: 7px;
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
    background: #f1f5f9;
  }}
  .img-box img {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .img-caption {{
    font-size: 9.5px;
    color: #475569;
    text-align: center;
    padding: 3px 6px;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    font-weight: 600;
  }}

  .tag-pill {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    margin-right: 4px;
  }}
  .tag-pill.green {{ background: #dcfce7; color: #166534; }}
  .tag-pill.amber {{ background: #fef3c7; color: #92400e; }}
</style>
</head>
<body>

<!-- PAGE 2: AI Adaptive Learning System (Engineering Project) -->
<div class="page" id="page2">
  <div>
    <!-- Top Header -->
    <div class="header">
      <div class="header-left">
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="badge-tag badge-blue">02 / 系統工程篇</span>
          <span class="badge-tag badge-amber">跨頁主線 (上) · 系統落地</span>
        </div>
        <h1 class="page-title">
          AI 自適應輔助學習系統
        </h1>
        <div class="page-subtitle">從真實教學痛點出發，落實於高中數學課堂的完整自適應平台</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge">🏆 神通扶輪盃 全國第一名 冠軍</div>
        <div class="header-award-badge" style="margin-top:3px; background:linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); border-color:#ea580c; color:#7c2d12;">🥇 育秀盃創意獎 全國金獎 (10萬元)</div>
      </div>
    </div>

    <!-- 4 Key Metrics -->
    <div class="grid-4" style="margin-bottom: 11px;">
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

    <!-- Main Two Column Grid -->
    <div class="grid-2" style="margin-bottom: 10px;">
      <!-- Left Column: Core System Pipeline & Role -->
      <div style="display:flex; flex-direction:column; justify-content:space-between;">
        <div class="card" style="padding:10px 12px;">
          <div class="card-header">
            <div class="card-header-bar teal"></div>
            起點問題與需求拆解
          </div>
          <div style="font-size:11.5px; color:#334155; line-height:1.5;">
            父親為技術型高中數學老師，長年面臨<b>「題目難以數位化批次輸入、固定題庫無法反覆變題練習、課堂學生雙峰差距極大」</b>之教學痛點。我著手自主開發適性化系統，不只做 Demo，更在花蓮高中班級正式上線運行。
          </div>
        </div>

        <div class="card" style="padding:10px 12px;">
          <div class="card-header">
            <div class="card-header-bar teal"></div>
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
              <div class="step-desc">讓 AI 模型依題型規格建立 Python 出題腳本，動態生成無窮數值變題與精確標準答案。</div>
            </div>
          </div>
          <div class="process-step" style="margin-bottom:0;">
            <div class="step-num">3</div>
            <div class="step-content">
              <div class="step-title">嚴格數學判題器 × AI 助教分層導航</div>
              <div class="step-desc">公式計算由後端嚴格程式判題，AI 模型僅負責思路引導與解題提示，杜絕數理幻覺。</div>
            </div>
          </div>
        </div>

        <div class="card" style="margin-bottom:0; padding:10px 12px;">
          <div class="card-header">
            <div class="card-header-bar teal"></div>
            自適應閉環路徑演算法
          </div>
          <div style="background:#f1f5f9; padding:5px 8px; border-radius:5px; font-size:11px; color:#1e293b; text-align:center; font-weight:700; margin-bottom:5px;">
            學生作答 ➔ 能力診斷 ➔ 適性決策 ➔ 補強／繼續 ➔ 再次評量
          </div>
          <div style="font-size:11.2px; color:#475569; line-height:1.45;">
            系統整合知識狀態診斷，動態判斷學生目前卡點。若前置基礎不穩，自動引導返回前置技能複習；若熟練則前進高階題目。
          </div>
        </div>
      </div>

      <!-- Right Column: Visual Evidence & Screenshot -->
      <div style="display:flex; flex-direction:column; justify-content:space-between;">
        <div class="img-box">
          <img src="{p('ai_p7_img2.png')}" style="height:205px; width:100%; object-fit:cover;" alt="學生個人學習分析儀表板">
          <div class="img-caption">▲ 真實正式網站：學生個人知識狀態診斷與答題紀錄後台 (mathb.math-adaptive.org)</div>
        </div>

        <div class="grid-2">
          <div class="img-box">
            <img src="{p('yuxiu_img1.png')}" style="height:155px; object-fit:contain; background:#ffffff;" alt="育秀盃金獎證書">
            <div class="img-caption">▲ 育秀盃創意獎 全國金獎 (獎金10萬)</div>
          </div>
          <div class="img-box">
            <img src="{p('rotary_img_2.jpeg')}" style="height:155px; object-fit:contain; background:#ffffff;" alt="扶輪盃冠軍獎狀">
            <div class="img-caption">▲ 神通扶輪盃 全國第一名 冠軍</div>
          </div>
        </div>

        <div class="card" style="background:#f8fafc; border:1px solid #cbd5e1; margin-bottom:0; padding:9px 12px;">
          <div style="font-size:11.5px; color:#334155; line-height:1.48;">
            <b>葉陽甫個人核心研發職責（貢獻度 70%）</b>：<br>
            主導整體系統架構、前後端全端實作、教材匯入演算法、數學判題引擎、資料庫架構、Docker 部署與花中班級長期正式維護。
          </div>
        </div>
      </div>
    </div>

    <!-- FULL-STACK ARCHITECTURE & DEVOPS CARD -->
    <div class="card" style="padding:9px 12px; margin-bottom:10px; background:#f8fafc; border:1px solid #cbd5e1;">
      <div class="card-header" style="margin-bottom:6px; justify-content:space-between;">
        <div style="display:flex; align-items:center; gap:6px;">
          <div class="card-header-bar teal"></div>
          <span>全端工程架構與真實課堂落地技術棧（Full-Stack & DevOps）</span>
        </div>
        <span style="font-size:10px; color:#0f766e; font-weight:700;">班級實機部署 · 微服務架構</span>
      </div>
      <div class="grid-3" style="font-size:10.8px; line-height:1.42; gap:10px;">
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:5px; padding:6px 9px;">
          <b style="color:#0f2942;">🖥️ 前端作答與公式渲染</b><br>
          Next.js / React 全端架構，整合 KaTeX 動態解析數學符號與 LaTeX 公式，支援幾何 Canvas 動態互動與座標繪圖。
        </div>
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:5px; padding:6px 9px;">
          <b style="color:#0f2942;">⚙️ 後端非同步與數理判題</b><br>
          FastAPI 高併發非同步處理，自研 SymPy 符號運算等價性驗證引擎，精確判別數學同解，杜絕大模型數理幻覺。
        </div>
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:5px; padding:6px 9px;">
          <b style="color:#0f2942;">🚀 容器部署與正式維運</b><br>
          Docker 容器化封裝、Nginx 反向代理、PostgreSQL 狀態追蹤，克服真實課堂「公式手寫辨識、缺參數、變題碰撞」三大工程考驗。
        </div>
      </div>
    </div>

    <!-- Bridge to P.3: The Crucial Narrative Link -->
    <div class="bridge-card" style="padding:10px 13px;">
      <div class="bridge-title" style="margin-bottom:6px;">
        <span>⚡ 跨頁銜接核心：真實課堂落地遭遇的致命瓶頸 ➔ 抽離問題啟動科研</span>
        <span style="font-size:11.5px; font-weight:800; color:#0284c7;">接續右頁研究 ➔</span>
      </div>
      <div class="grid-2" style="font-size:11px; line-height:1.45; gap:10px; margin-bottom:6px;">
        <div style="background:#ffffff; border:1px solid #bae6fd; border-radius:5px; padding:6px 9px;">
          <b style="color:#0369a1;">☁️ 雲端大型模型瓶頸</b>：<br>
          課堂高頻呼叫 API 造成高昂費用與連線延遲，且涉及校園學生個人資料外洩風險；全面推動校園邊緣端（Edge AI）部署勢在必行。
        </div>
        <div style="background:#ffffff; border:1px solid #bae6fd; border-radius:5px; padding:6px 9px;">
          <b style="color:#0369a1;">💻 本地小模型（SLM）生成崩潰</b>：<br>
          邊緣端小模型生成出題程式時頻繁出現 <b>SyntaxError 語法錯誤、未引用變數、介面格式偏差</b>；若要求重產極耗算力且結果不收斂。
        </div>
      </div>
      <div style="font-size:11.2px; color:#0c4a6e; line-height:1.45; background:#e0f2fe; padding:6px 10px; border-radius:5px; font-weight:600;">
        💡 <b>核心研究假說</b>：「如何在無正確答案（Ground Truth）的前提下，以確定性規則在邊緣端安全修復局部程式碼？」——這個在真實工程中卡住的痛點，催生了右頁的深層語法樹編譯研究！
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
          <span class="badge-tag badge-purple">03 / 科學研究篇</span>
          <span class="badge-tag badge-amber">跨頁主線 (下) · 深化科研</span>
        </div>
        <h1 class="page-title">
          AST Active Healer 程式生成可靠性
        </h1>
        <div class="page-subtitle">從工程痛點抽離的純學術探索：以抽象語法樹與確定性修復突破生成邊界</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge" style="background:linear-gradient(135deg, #fed7aa 0%, #fde68a 100%); border-color:#d97706; color:#78350f;">🏅 第25屆旺宏科學獎 全國決賽20強</div>
        <div class="header-award-badge" style="margin-top:3px; background:#f1f5f9; border-color:#94a3b8; color:#334155;">🎖️ 第66屆東區科展 優等第2名</div>
      </div>
    </div>

    <!-- P3 Top Connecting Box -->
    <div class="p3-bridge-card" style="padding:10px 12px; margin-bottom:11px;">
      <div style="font-size:12.2px; font-weight:800; color:#854d0e; display:flex; justify-content:space-between; margin-bottom:4px;">
        <span>🔬 科研問題意識：把真實痛點抽離為嚴謹的科學假說</span>
        <span style="font-size:11px; color:#a16207;">承接左頁系統工程痛點 ◄</span>
      </div>
      <div style="font-size:11.4px; color:#713f12; line-height:1.5;">
        抽離特定數學業務，將問題聚焦為<b>「小模型生成受限環境程式的局部修復能力與邊界」</b>。設計以固定規則運作的 AST Active Healer，探索不將錯誤重新丟回模型黑箱、直接在語法樹層級進行確定性修復的極限。
      </div>
    </div>

    <!-- Core Mechanism Diagram & Benchmark Chart (Side-by-Side) -->
    <div class="grid-2" style="margin-bottom: 11px; align-items: stretch;">
      <!-- Left: AST Active Healer Flowchart -->
      <div class="card" style="padding: 10px 11px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 5px; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 5px;">
            <div class="card-header-bar purple"></div>
            <span style="font-size: 12px; font-weight: 800;">AST Healer 三階段主動修復流程</span>
          </div>
          <span style="font-size: 9.5px; color: #6b21a8; font-weight: 700;">語法樹靜態解析架構</span>
        </div>
        <div class="img-box" style="border: none; margin-bottom: 6px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff;">
          <img src="{p('healer_flowchart.png')}" style="height: 235px; width: 100%; object-fit: contain;" alt="AST Healer 流程圖">
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 6px 8px; font-size: 10.2px; color: #475569; line-height: 1.4;">
          <b>修復機制管線</b>：① <b>Scaffold 骨架</b>約束輸入輸出合約 ➔ ② <b>AST 解析</b>捕捉語法樹與未引用變數 ➔ ③ <b>確定性修復</b>安全局部，超限則<b>主動棄權 (Abstain)</b>。
        </div>
      </div>

      <!-- Right: Benchmark Experiment Chart (User Added) -->
      <div class="card" style="padding: 10px 11px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card-header" style="margin-bottom: 5px; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 5px;">
            <div class="card-header-bar amber"></div>
            <span style="font-size: 12px; font-weight: 800;">4 種 Prompt × 3 模型盲測救援率</span>
          </div>
          <span style="font-size: 9.5px; color: #b45309; font-weight: 700;">旺宏決賽嚴格測試集</span>
        </div>
        <div class="img-box" style="border: none; margin-bottom: 6px; flex: 1; display: flex; align-items: center; justify-content: center; background: #ffffff;">
          <img src="{p('healer_chart_user.png')}" style="height: 235px; width: 100%; object-fit: contain;" alt="三種模型在四種 Prompt 條件下的原始通過率與 Healer 新增救援">
        </div>
        <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 4px; padding: 6px 8px; font-size: 10.2px; color: #78350f; line-height: 1.4;">
          <b>實驗洞察</b>：Gemini 基準較高；Qwen 在 Ab2d+spec 表現最佳；342 格失敗中僅 9 格安全救回（2.63%），確證確定性工具應守住安全邊界，不強行修補深度語義。
        </div>
      </div>
    </div>

    <!-- 4 Rigorous Benchmark Metrics -->
    <div class="grid-4" style="margin-bottom: 11px;">
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

    <!-- Two Column Reflection and Science Spirit -->
    <div class="grid-2" style="margin-bottom: 11px;">
      <!-- Left: Research Turning Point -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:11px 13px;">
        <div>
          <div class="card-header">
            <div class="card-header-bar amber"></div>
            研究轉折：推翻虛高分數的求真態度
          </div>
          <div style="font-size:11.4px; color:#334155; line-height:1.52;">
            <b>從 97.41 到獨立測試集的震撼教育</b>：<br>
            初版研究曾以自建 MCRI 指標取得 97.41 高分。但在東區科展評審提問與未晉級反思中，我意識到指標混淆了「題型固有通過率」與「修復機制獨立因果」。進入旺宏決賽後，我<b>果斷推翻虛高分數</b>，以 Math16 題庫、3 種模型、4 種提示條件與固定隨機種子，建立 12 題嚴格保留測試集，凍結修復規則進行盲測。
          </div>
        </div>
        <div style="background:#fef3c7; border:1px solid #fde68a; border-radius:4px; padding:5px 8px; font-size:10.5px; color:#78350f; font-weight:700; margin-top:6px;">
          ✦ 旺宏全領域 846 件作品報名 · 進入全國決賽 20 強（電腦資訊類僅 4 件入選）
        </div>
      </div>

      <!-- Right: Boundary & Conclusion -->
      <div class="card" style="margin-bottom:0; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:11px 13px;">
        <div>
          <div class="card-header">
            <div class="card-header-bar amber"></div>
            能力邊界確立與研究收束
          </div>
          <div style="font-size:11.4px; color:#334155; line-height:1.52;">
            <b>看清工具的極限，才是真正的科學</b>：<br>
            實驗證實 9/342 被安全救回，救援成功率 2.63%。成功案例高度集中於介面、格式與變數流等局部錯誤；而牽涉解題推理與演算法邏輯之錯誤，不可交由固定規則硬修。<br>
            <b>最終結論</b>：在系統落地時，應<b>「先以 Scaffold 補齊領域工具與流程資訊，再以 Healer 進行確定性局部修補」</b>，形成完整工程闭環。
          </div>
        </div>
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:4px; padding:5px 8px; font-size:10.5px; color:#166534; font-weight:700; margin-top:6px;">
          ✦ 第 66 屆東區科展 電腦與資訊學科【優等第 2 名】
        </div>
      </div>
    </div>

    <!-- Error Taxonomy Card -->
    <div class="card" style="margin-bottom:0; background:#f8fafc; border:1px solid #cbd5e1; padding:10px 13px;">
      <div style="font-size:11.8px; font-weight:800; color:#0f2942; margin-bottom:6px; display:flex; justify-content:space-between;">
        <span>錯誤分類學與三層修復行為架構（Error Taxonomy）</span>
        <span style="font-size:10px; color:#64748b;">旺宏全國 20 強深化成果</span>
      </div>
      <div class="grid-3" style="font-size:10.5px; line-height:1.45; gap:9px;">
        <div style="background:#ffffff; border:1px solid #bbf7d0; border-radius:4px; padding:6px 9px;">
          <span class="tag-pill green" style="margin-bottom:4px; display:inline-block;">可確定修復 (Safe Repair)</span><br>
          未引用變數清除、介面函式名命名偏差校正、回傳格式不符重構。
        </div>
        <div style="background:#ffffff; border:1px solid #fed7aa; border-radius:4px; padding:6px 9px;">
          <span class="tag-pill amber" style="margin-bottom:4px; display:inline-block;">語法修復但語義仍錯 (Partial)</span><br>
          補齊 SyntaxError 語法缺損，但解題數值邏輯仍錯誤（交由判題器精準攔截）。
        </div>
        <div style="background:#ffffff; border:1px solid #fecaca; border-radius:4px; padding:6px 9px;">
          <span class="tag-pill" style="background:#fee2e2; color:#991b1b; border-color:#f87171; margin-bottom:4px; display:inline-block;">主動棄權邊界 (Safe Abstention)</span><br>
          演算法死循環、核心數學原理推導錯誤、模型幻覺（嚴禁以規則硬修，主動棄權）。
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
          <span class="badge-tag badge-teal">04 / 跨域實踐篇</span>
          <span class="badge-tag badge-amber">全人發展 · 自律與視野</span>
        </div>
        <h1 class="page-title">
          競技運動與外語溝通實力
        </h1>
        <div class="page-subtitle">長期投入的高壓競技淬鍊 × 無縫研讀國際前沿論文的語言利器</div>
      </div>
      <div class="header-right">
        <div class="header-award-badge" style="background:#f0fdf4; border-color:#16a34a; color:#15803d;">⚽ 全國五人制聯賽 全國第 5 名</div>
        <div class="header-award-badge" style="margin-top:3px; background:#fefce8; border-color:#ca8a04; color:#854d0e;">🌟 TOEIC 945 金色 ｜ GEPT 中高級</div>
      </div>
    </div>

    <!-- UPPER HALF: SOCCER ATHLETICS -->
    <div style="margin-bottom: 11px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <div style="font-size:15px; font-weight:900; color:#0f2942; display:flex; align-items:center; gap:6px;">
          <span style="font-size:16px;">⚽</span>
          <span>高中足球競技：連續兩年打入全國決賽八強（長期投入）</span>
        </div>
        <span style="font-size:10px; font-weight:700; color:#0369a1; background:#e0f2fe; padding:2px 7px; border-radius:4px;">背號 42 號 主力球員</span>
      </div>

      <!-- Soccer 4 Metrics -->
      <div class="grid-4" style="margin-bottom: 9px;">
        <div class="metric-card teal">
          <div class="metric-val">全國第 5 名</div>
          <div class="metric-lbl">114學年度五人制聯賽</div>
        </div>
        <div class="metric-card teal">
          <div class="metric-val">全國第 6 名</div>
          <div class="metric-lbl">113學年度五人制聯賽</div>
        </div>
        <div class="metric-card teal">
          <div class="metric-val">全國第 5 名</div>
          <div class="metric-lbl">全國青年盃公開組</div>
        </div>
        <div class="metric-card teal">
          <div class="metric-val">縣運亞軍</div>
          <div class="metric-lbl">2025 花蓮縣運社會組</div>
        </div>
      </div>

      <!-- Soccer Content + Team Photo -->
      <div class="grid-2">
        <div style="display:flex; flex-direction:column; justify-content:space-between;">
          <div class="card" style="margin-bottom:8px; padding:10px 12px;">
            <div style="font-size:11.5px; color:#334155; line-height:1.5;">
              <b>從國中隊長到高中校隊主力</b>：<br>
              國三擔任花崗國中男足隊長，帶隊出賽全國甲級聯賽；高中持續代表花中出戰最高殿堂「中等學校五人制足球聯賽」，在全國近 60 支傳統強權中連兩年打入決賽，114學年以 5:3 擊敗台中惠文高中奪全國第 5 名。<br>
              <b>競技運動鍛鍊的核心特質</b>：<br>
              五人制空間極小、節奏飛快。高強度訓練磨練出<b>「高壓環境下的冷靜決策力、逆境抗挫力與團隊戰術溝通」</b>，這份堅韌成為面對複雜工程 Bug 與漫長科研實驗時最堅實的心態支柱。
            </div>
            <div style="font-size:10px; color:#0369a1; font-weight:700; margin-top:5px; background:#f0f9ff; padding:3px 6px; border-radius:4px;">
              ✦ 符合教育部運動績優甄試資格 ｜ 5:3 擊敗台中惠文高中奪全國第 5 名
            </div>
          </div>

          <!-- FBref analytics highlight -->
          <div class="card" style="margin-bottom:0; background:#f8fafc; border:1px solid #cbd5e1; padding:8px 11px;">
            <div style="font-size:11.2px; font-weight:800; color:#0369a1; margin-bottom:3px;">
              📊 資訊跨域落地：自主開發 FBref 足球數據分析模型
            </div>
            <div style="font-size:10.5px; color:#475569; line-height:1.42;">
              結合資訊能力與運動熱愛，撰寫 Python 爬蟲抓取海外 FBref 頂級賽事資料庫，建立五人制攻防跑位、高壓傳球成功率與體能熱區分析腳本，以量化數據輔助球隊戰術決策。
            </div>
          </div>
        </div>

        <div class="img-box" style="display:flex; flex-direction:column; justify-content:space-between;">
          <img src="{p('soccer_team_perfect.png')}" style="height:215px; width:100%; object-fit:cover;" alt="花蓮高中足球代表隊合影">
          <div class="img-caption">▲ 114學年度全國中等學校五人制足球聯賽決賽現場：花蓮高中代表隊合影 (前排右四 葉陽甫)</div>
        </div>
      </div>
    </div>

    <!-- DIVIDER -->
    <div style="border-top: 2px dashed #cbd5e1; margin: 9px 0 10px 0;"></div>

    <!-- LOWER HALF: ENGLISH PROFICIENCY & RESEARCH APPLICATION -->
    <div style="margin-bottom: 11px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <div style="font-size:15px; font-weight:900; color:#0f2942; display:flex; align-items:center; gap:6px;">
          <span style="font-size:16px;">🌐</span>
          <span>外語溝通實力：直接研讀前沿論文的科研利器（語言能力）</span>
        </div>
        <span style="font-size:10px; font-weight:700; color:#b45309; background:#fef3c7; padding:2px 7px; border-radius:4px;">CEFR B2+ ｜ 高中全校前 2%</span>
      </div>

      <!-- English 4 Metrics -->
      <div class="grid-4" style="margin-bottom: 9px;">
        <div class="metric-card gold">
          <div class="metric-val">945 分</div>
          <div class="metric-lbl">TOEIC 多益金色證書</div>
        </div>
        <div class="metric-card gold">
          <div class="metric-val">全數通過</div>
          <div class="metric-lbl">GEPT 中高級聽說讀寫</div>
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
          <div class="card" style="margin-bottom:8px; padding:10px 12px;">
            <div style="font-size:11.5px; color:#334155; line-height:1.5;">
              <b>英文是探索世界與前沿知識的日常工具</b>：<br>
              英文對我而言從不是應試科目，而是無縫接軌國際頂尖科技的必備工具。在執行 AST Healer 研究與自適應系統架構時，我能<b>直接研讀 arXiv 上最新出爐的 AI、編譯器與軟體工程英文論文</b>，精準理解數學公式、演算法推導與國際 Benchmark 設計。<br>
              <b>多元語文競賽成果</b>：<br>
              高一至高二英文累積成績校排前 4%（高二下 96 分、校排第 7・前 2%）；榮獲花蓮縣英文作文競賽高中組甲等、校內英語演說初賽第一名、全校複賽第四名。
            </div>
          </div>

          <!-- Academic Paper & Open Source Card -->
          <div class="card" style="margin-bottom:0; background:#fffdfa; border:1px solid #fde68a; padding:8px 11px;">
            <div style="font-size:11.2px; font-weight:800; color:#b45309; margin-bottom:3px;">
              📚 前沿學術研讀 × 國際開源技術生態接軌
            </div>
            <div style="font-size:10.5px; color:#78350f; line-height:1.42;">
              高中期間直接研讀國外頂會 AI 前沿論文（Tree-of-Thoughts、Self-Refine、SWE-bench），並流暢研讀 PyTorch、Transformers、FastAPI 官方全英技術文件，具備國際學術發表與跨國技術協作實力。
            </div>
          </div>
        </div>

        <div class="grid-2">
          <div class="img-box">
            <img src="{p('english_img1.jpeg')}" style="height:182px; object-fit:contain; background:#ffffff;" alt="GEPT 中高級證書">
            <div class="img-caption">▲ GEPT 全民英檢中高級合格</div>
          </div>
          <div class="img-box">
            <img src="{p('english_img2.jpeg')}" style="height:182px; object-fit:contain; background:#ffffff;" alt="TOEIC 945 金色證書">
            <div class="img-caption">▲ TOEIC 945 金色證書</div>
          </div>
        </div>
      </div>
    </div>

    <!-- DIGITAL PORTFOLIO & CONTACT BAR -->
    <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; border-radius:7px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center;">
      <div style="font-size:11px; color:#1e293b; font-weight:700;">
        <span style="color:#0284c7;">📁 數位作品與開源專案線上入口：</span><br>
        <span style="color:#475569; font-weight:500;">
          🌐 系統正式上線網址：<b>mathb.math-adaptive.org</b> ｜ 📄 遮雨棚發明專利簡報：<b>bit.ly/yangfu-invention</b>
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
    html_file = TMP_DIR / "pages_234.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Wrote HTML to {html_file}")

    # Render via Chrome headless
    pdf_234 = TMP_DIR / "pages_234.pdf"
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

    out_a4 = OUT_DIR / "葉陽甫_面試四面小冊_A4閱讀版.pdf"
    booklet.save(out_a4, garbage=4, deflate=True)
    print(f"Saved A4 booklet: {out_a4} ({len(booklet)} pages)")

    # Assemble A3 Landscape Duplex Printable PDF
    # Sheet 1 (Outside): Left = P4 (Back), Right = P1 (Cover)
    # Sheet 2 (Inside): Left = P2 (System), Right = P3 (Research)
    a3_doc = fitz.open()
    a3_w, a3_h = 1190.55, 841.89 # A3 landscape points (420mm x 297mm)

    for left_idx, right_idx in [(3, 0), (1, 2)]:
        sheet = a3_doc.new_page(width=a3_w, height=a3_h)
        sheet.show_pdf_page(fitz.Rect(0, 0, a3_w / 2, a3_h), booklet, left_idx)
        sheet.show_pdf_page(fitz.Rect(a3_w / 2, 0, a3_w, a3_h), booklet, right_idx)

    out_a3 = OUT_DIR / "葉陽甫_面試四面小冊_A3雙面列印版.pdf"
    a3_doc.save(out_a3, garbage=4, deflate=True)
    print(f"Saved A3 printable booklet: {out_a3} ({len(a3_doc)} sheets)")

    # Render preview images
    preview_dir = ROOT / "tmp" / "booklet_v3_preview"
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
