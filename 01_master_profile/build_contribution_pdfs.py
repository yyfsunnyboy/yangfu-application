import os
import sys
import win32com.client
import fitz

WORKSPACE = r"C:\Projects\yangfu-application"
PROFILE_DIR = os.path.join(WORKSPACE, "01_master_profile")

HTML_YUXIU = os.path.join(PROFILE_DIR, "09a_yuxiu_cup_contribution_certificate.html")
PDF_YUXIU = os.path.join(PROFILE_DIR, "09a_yuxiu_cup_contribution_certificate.pdf")

HTML_WANGHONG = os.path.join(PROFILE_DIR, "09b_wanghong_award_contribution_certificate.html")
PDF_WANGHONG = os.path.join(PROFILE_DIR, "09b_wanghong_award_contribution_certificate.pdf")

# CSS template for official single-page A4 academic certificates
COMMON_STYLE = """
<style>
  @page {
    size: A4 portrait;
    margin: 5.5mm 9mm 4.5mm 9mm;
  }
  * {
    box-sizing: border-box;
  }
  body {
    font-family: "標楷體", "DFKai-SB", "Microsoft JhengHei", "微軟正黑體", sans-serif;
    color: #0f172a;
    background: #ffffff;
    margin: 0;
    padding: 0;
    line-height: 1.15;
    font-size: 8.0pt;
  }
  .header-box {
    text-align: center;
    border-bottom: 1.8px solid #1e3a8a;
    padding-bottom: 2px;
    margin-bottom: 2.5px;
  }
  .school-title {
    font-size: 13.5pt;
    font-weight: bold;
    color: #1e3a8a;
    letter-spacing: 2px;
    margin: 0 0 1px 0;
  }
  .doc-title {
    font-size: 10.8pt;
    font-weight: bold;
    color: #0f172a;
    letter-spacing: 1px;
    margin: 0 0 1px 0;
  }
  .sub-tag {
    font-size: 8.3pt;
    color: #475569;
    font-weight: bold;
  }
  .cert-text {
    font-size: 8.0pt;
    text-indent: 2em;
    margin: 2.5px 0;
    line-height: 1.22;
    text-align: justify;
  }
  .section-title {
    font-size: 8.6pt;
    font-weight: bold;
    color: #1e3a8a;
    border-left: 3px solid #1e3a8a;
    padding-left: 5px;
    margin: 2.5px 0 1.5px 0;
  }
  table.info-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 2px;
    font-size: 7.7pt;
  }
  table.info-table th, table.info-table td {
    border: 1px solid #64748b;
    padding: 1.8px 3.8px;
    vertical-align: top;
    line-height: 1.15;
  }
  table.info-table th {
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: bold;
    text-align: center;
  }
  table.info-table td.center {
    text-align: center;
  }
  .highlight-member {
    background-color: #f8fafc;
  }
  .statement-box {
    border: 1px solid #94a3b8;
    background-color: #f8fafc;
    padding: 3px 5.5px;
    border-radius: 3px;
    font-size: 7.7pt;
    margin: 2.5px 0 2px 0;
    line-height: 1.2;
    text-align: justify;
  }
  .sign-section {
    margin-top: 2.5px;
    display: table;
    width: 100%;
  }
  .sign-to {
    display: table-cell;
    width: 25%;
    font-size: 8.6pt;
    font-weight: bold;
    vertical-align: middle;
  }
  .sign-fields {
    display: table-cell;
    width: 75%;
    font-size: 8.0pt;
    line-height: 1.38;
  }
  .sign-line {
    border-bottom: 1px solid #334155;
    display: inline-block;
    width: 150px;
  }
  ul.duty-list {
    margin: 1px 0;
    padding-left: 11px;
  }
  ul.duty-list li {
    margin-bottom: 1px;
  }
</style>
"""

# HTML Content for Yuxiu Cup (Exact 1 page)
content_yuxiu = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>第23屆育秀盃創意獎_團隊分工與個人貢獻度證明書</title>
{COMMON_STYLE}
</head>
<body>

<div class="header-box">
  <div class="school-title">國立花蓮高級中學</div>
  <div class="doc-title">學生參與科技創新競賽・團隊分工與個人實質貢獻度證明書</div>
  <div class="sub-tag">【 2026 第 23 屆育秀盃創意獎 高中職 AI 應用類 金獎（全國首獎） 】</div>
</div>

<div class="cert-text">
  茲證明本校學生 <strong>葉陽甫</strong>（身分證字號：___________________，國立花蓮高級中學三年五班），於在學期間指導參與 <strong>財團法人育秀教育基金會</strong> 主辦之 <strong>「2026 第 23 屆育秀盃創意獎」</strong>，榮獲 <strong>高中職 AI 應用類 金獎（全國首獎，獎金新臺幣拾萬元整）</strong>。本獲獎專案依據正式提報之參賽企劃書（SA237853）與決賽簡報，其全端研發架構、團隊工作職責與申請人個人實質貢獻比例說明如下：
</div>

<div class="section-title">一、獲獎專案基本資訊</div>
<table class="info-table">
  <tr>
    <th style="width: 18%;">競賽名稱</th>
    <td style="width: 82%;">2026 第 23 屆育秀盃創意獎（高中職 AI 應用類）</td>
  </tr>
  <tr>
    <th>專案企劃編號</th>
    <td><strong>SA237853</strong></td>
  </tr>
  <tr>
    <th>參賽作品名稱</th>
    <td><strong>〈自適應性輔助學習系統〉</strong>（<em>An Adaptive AI-Assisted Tutoring System</em>，智學 AIGC 賦能平台）</td>
  </tr>
  <tr>
    <th>大賽獲獎成績</th>
    <td><strong>金獎 Gold Winner（全台高中職第一名首獎，獲大會獎金 10 萬元）</strong>［已證實］</td>
  </tr>
  <tr>
    <th>專案核心架構</th>
    <td>由葉陽甫同學主導設計並實作包含「後台資料庫與教材流水線、中台程式出題引擎、前台多模態作答與蘇格拉底 AI 助教」之全端學習系統，並整合強化學習推薦與檢索模組，實地導入花蓮高商課堂試用。</td>
  </tr>
</table>

<div class="section-title">二、三人研發團隊架構與成員具體職責分工</div>
<table class="info-table">
  <tr>
    <th style="width: 18%;">研發成員／班級</th>
    <th style="width: 68%;">系統架構模組與具體研發權責（前後台建置、部署與核心功能）</th>
    <th style="width: 14%;">實質貢獻度</th>
  </tr>
  <tr class="highlight-member">
    <td class="center" style="vertical-align: middle;"><strong>葉陽甫</strong><br>(申請人／主責)<br>三年五班</td>
    <td>
      <strong>【前後台全系統架構設計、後台資料庫規劃建置、教材流水線、Code-as-Content 出題、前台蘇格拉底作答與線上部署上線】</strong>
      <ul class="duty-list">
        <li><strong>後台資料庫規劃、建置與系統上線維運</strong>：獨立規劃底層階層式知識圖譜資料庫骨架（年級&rarr;冊次&rarr;章節&rarr;知識節點先後關係），建置題庫、學生歷程與診斷數據庫；負責伺服器環境配置、系統部署與實際上線，實地導入花蓮高商數學課堂進行教學試用。</li>
        <li><strong>後台流水線教材輸入（Automated Import Pipeline）</strong>：建置教材自動化解析流程，支援教師上傳 PDF/Word 講義後自動萃取內容並對齊課綱節點，保留 Human-in-the-loop 機制供教師審核與修訂。</li>
        <li><strong>中台 Code-as-Content（程式即內容）出題引擎</strong>：主導「算邏分離」出題架構，以 Python 直譯腳本即時動態生成無限變體題並精算標準答案，根除大模型數值計算幻覺；並在出題代碼排查中奠定後續 AST 容錯研究起點。</li>
        <li><strong>前台多模態作答系統 &times; 蘇格拉底 AI 助教</strong>：建置學生作答介面，整合 Canvas 手寫板與考卷拍照（Vision AI）辨識解題中間步驟；設計「蘇格拉底式 AI 助教」，不直接給答案，而是透過階梯式提問引導學生自我推理；內建 Explainable AI 決策可視化介面與教學／評量雙模式。</li>
        <li><strong>全端模組閉環整合（Pipeline Integration）</strong>：統籌前後端狀態機同步與 API 介面契約，將隊友研發之 PPO 推薦決策模型與搜尋檢索時調用之 Hybrid RAG 模組完整整合進系統主線流程，落實「教材進得來、題目生得出、學生寫得下、系統看得懂」之端到端學習閉環。</li>
      </ul>
    </td>
    <td class="center" style="font-size: 13pt; font-weight: bold; color: #1e3a8a; vertical-align: middle;">50 %</td>
  </tr>
  <tr>
    <td class="center" style="vertical-align: middle;"><strong>蔡昕諾</strong><br>三年五班</td>
    <td>
      <strong>【大腦 Brain 模組——PPO 強化學習導航推薦】</strong><br>
      主責企劃書「學習路徑決策」模組，負責 Local APR 與 PPO 強化學習演算法之開發與調校，依據學生作答歷史與知識狀態，動態計算留在主線、進入補救或返回主線之推薦決策，供主系統串接調用。
    </td>
    <td class="center" style="font-size: 10pt; font-weight: bold; vertical-align: middle;">25 %</td>
  </tr>
  <tr>
    <td class="center" style="vertical-align: middle;"><strong>林昕佑</strong><br>三年五班</td>
    <td>
      <strong>【嘴巴 Mouth 模組——搜尋檢索專用之 Hybrid RAG】</strong><br>
      主責企劃書「RAG 解題輔助」模組，建置高職數學教材知識庫，整合語意向量檢索與 BM25 關鍵字檢索，提供學生在學習主線卡關需要向系統搜尋時才調用之 Hybrid RAG 語意檢索技術。
    </td>
    <td class="center" style="font-size: 10pt; font-weight: bold; vertical-align: middle;">25 %</td>
  </tr>
  <tr style="background-color: #f8fafc; font-weight: bold;">
    <td class="center">全體團隊合計</td>
    <td style="text-align: right; padding-right: 15px;">全體研發團隊工作實質貢獻度總計：</td>
    <td class="center" style="font-size: 11pt; color: #1e3a8a;">100 %</td>
  </tr>
</table>

<div class="statement-box">
  <strong>指導老師查核與評審陳述：</strong><br>
  本專案由本人全程擔任正式指導老師。葉陽甫同學在研發過程中扮演全端系統核心架構師，獨立完成了後台資料庫規劃與建置、教材自動化流水線、中台程式出題引擎、前台蘇格拉底作答介面，並統籌系統伺服器部署與課堂上線試用，同時整合隊友之演算法模組形成可操作之閉環平台，為本作品奪得全台首獎之關鍵核心。上述研發分工內容與貢獻比例均由本人審慎核實，特此出具證明。
</div>

<div class="sign-section">
  <div class="sign-to">
    此致<br>
    各大專校院招生委員會
  </div>
  <div class="sign-fields">
    指導老師簽章：<span class="sign-line"></span>（親筆簽名）<br>
    服務學校：國立花蓮高級中學 &nbsp;&nbsp;&nbsp;&nbsp; 現任職稱：專任教師<br>
    聯絡電話：(03) 822-6108 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 電子信箱：___________________________<br>
    中華民國 115 年 10 月 ______ 日
  </div>
</div>

</body>
</html>
"""

# HTML Content for Wang Hong Science Award (Deepened & Focused on AST Healer, Benchmark & Zero-Blackbox)
content_wanghong = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>第25屆旺宏科學獎_團隊分工與個人貢獻度證明書</title>
{COMMON_STYLE}
</head>
<body>

<div class="header-box">
  <div class="school-title">國立花蓮高級中學</div>
  <div class="doc-title">學生參與學術科學競賽・團隊分工與個人實質貢獻度證明書</div>
  <div class="sub-tag">【 第 25 屆旺宏科學獎（Wang Hong Science Award） 全領域全國決賽 20 強 】</div>
</div>

<div class="cert-text">
  茲證明本校學生 <strong>葉陽甫</strong>（身分證字號：___________________，國立花蓮高級中學三年五班），於高二至高三期間參與 <strong>財團法人旺宏教育基金會</strong> 主辦之 <strong>「第 25 屆旺宏科學獎」</strong>，於全台各高中職共 846 件全領域參賽作品中脫穎而出，<strong>榮獲入圍「全領域全國決賽 20 強」（電腦資訊類全台僅 4 件）</strong>。本研究依據正式繳交大會審查之完整創意說明書（SA25-016，30 頁）與版本控制審計紀錄（自建代碼量 132,749 行，個人 Git 提交 931 次），經大會評審建議全面聚焦核心原創貢獻，其分工與實質貢獻比例說明如下：
</div>

<div class="section-title">一、旺宏參賽研究專案基本資訊</div>
<table class="info-table">
  <tr>
    <th style="width: 18%;">專案研究編號</th>
    <td style="width: 32%;"><strong>SA25-016</strong>（隊伍：工人智慧）</td>
    <th style="width: 18%;">參賽領域類別</th>
    <td style="width: 32%;">資訊學科（電腦資訊類入圍代表）</td>
  </tr>
  <tr>
    <th>參賽研究題目</th>
    <td colspan="3"><strong>〈基於人工智慧之自適應輔助學習架構探究〉</strong>（<em>An Adaptive Intelligent Tutoring Architecture via Neural-Symbolic Repair and Multi-Objective RL</em>）</td>
  </tr>
  <tr>
    <th>核心創新技術</th>
    <td colspan="3">AST（抽象語法樹）主動自癒機制、Tier A～D 四級確定性修復、Answer-Blind 防篡改邊界、提示鷹架工程、PPO 多目標學習路徑推薦、Hybrid RAG 混合檢索</td>
  </tr>
  <tr>
    <th>大會入圍成果</th>
    <td colspan="3"><strong>入圍全領域全國決賽 20 強（電腦資訊類全台僅 4 件代表入圍）</strong>［已證實］<br><span style="font-size: 7.3pt; color: #475569;">（決賽口試已於 115 年 9 月 5 日完成，官方正式獲獎名次待 10 月 24 日頒獎典禮正式公布）</span></td>
  </tr>
</table>

<div class="section-title">二、系統功能架構、說明書各章節具體分工權責與代碼庫鑑識</div>
<table class="info-table">
  <tr>
    <th style="width: 18%;">研究成員／班級</th>
    <th style="width: 68%;">說明書對應章節、實質研究貢獻範疇與代碼庫鑑識依據</th>
    <th style="width: 14%;">實質貢獻度</th>
  </tr>
  <tr class="highlight-member">
    <td class="center" style="vertical-align: middle;"><strong>葉陽甫</strong><br>(第一作者／<br>AST Healer 發明人<br>兼系統架構師)<br>三年五班</td>
    <td>
      <strong>【說明書第四章第一節：提示鷹架與 AST 語法樹自癒機制之生成優化；暨全系統架構與標準 Benchmark 驗證】</strong>
      <ul class="duty-list">
        <li><strong>核心原創發明：神經符號 AST Active Healer 自癒引擎（自建 47,661 行）</strong>：針對大會評審建議「聚焦真正原創貢獻並做深」，手寫 Python 原生 AST（抽象語法樹）遍歷修復演算法，建立四級確定性修復梯隊：Tier A（語法閉合與全形標點）、Tier B（呼叫語法與 LaTeX 數學括號）、Tier C（領域 API 命名正規化）、Tier D（命名空間遮蔽清理與最優重載選取）。實作 Proof-Carrying Repair 與嚴格 <strong>Answer-Blind（絕不碰答案）</strong> 邊界防禦，達成 <strong>0 Regression（零語義退化）</strong>，大幅縮小生成標準差，獲評審最具體讚許。</li>
        <li><strong>提示詞鷹架工程（Prompt Scaffolding）與保守學術定位</strong>：設計 Ab1 至 Ab2d 鷹架與 JIT 題目生成器（<code>scaler.py</code>）。化解評審「基準不對等」疑慮：不妄稱小模型超越巨型模型，而是證實「神經符號工程能為本地邊緣小模型築起確定性防線，消除計算與語法幻覺，達成可靠出題」。</li>
        <li><strong>深度外部驗證：Math16 標準基準測試（Test Harness 58,422 行測試代碼）</strong>：克服評審「淺層驗證」質疑，獨立建構涵蓋 Math16 開發集（240 單元）與保留集（720 單元）共 <strong>960 單元</strong> 消融驗證管線，每輪測試均附獨立 SHA256 驗證指紋，確保學術高度可再現性。</li>
        <li><strong>自主研發零外部依賴實證（化解大學實驗室質疑）</strong>：代碼庫鑑識證實：跨專案自建代碼 13.2 萬行，個人累計 <strong>931 次 Git 提交（佔全案 93% 以上）</strong>，全套 AST 自癒模組皆為高中團隊原生手寫實作，無任何外部大學實驗室協助或黑盒代碼。</li>
      </ul>
    </td>
    <td class="center" style="font-size: 13pt; font-weight: bold; color: #1e3a8a; vertical-align: middle;">50 %</td>
  </tr>
  <tr>
    <td class="center" style="vertical-align: middle;"><strong>蔡昕諾</strong><br>(第二作者／<br>強化學習主責)<br>三年五班</td>
    <td>
      <strong>【說明書第四章第二節：基於強化學習之自適應學習題目推薦】</strong><br>
      主責第二節研究，負責 AKT（Attentive Knowledge Tracing，注意力知識追蹤，ASSISTments 數據集 AUC 0.7277）學生狀態建模；建置 Gymnasium 自訂環境（<code>AKTEnv</code>）與 PPO（近端策略最佳化）策略網路；特別落實評審讚許之<strong>「情感維度多目標獎勵函數」</strong>（將連續挫折懲罰、無聊適配度、APR 學習進展、題型多樣性、時間損耗納入獎勵塑造），深度貼近教育心理情境。
    </td>
    <td class="center" style="font-size: 10pt; font-weight: bold; vertical-align: middle;">25 %</td>
  </tr>
  <tr>
    <td class="center" style="vertical-align: middle;"><strong>林昕佑</strong><br>(第三作者／<br>檢索系統主責)<br>三年五班</td>
    <td>
      <strong>【說明書第四章第三節：基於混合 RAG 提升 LLM 問答品質】</strong><br>
      主責第三節研究，負責均一教育平台 301 篇教材語料整理與錯題診斷映射；實作 Hybrid RAG（混合檢索增強生成，Chroma 向量檢索 + BM25Okapi 關鍵字索引，運用 RRF 倒數排名融合達成 Top-5 54.15% 命中率）；建置 &lt;0.1 秒本地動態意圖路由（Fast/Advanced Path），大幅節省雲端 API 成本。
    </td>
    <td class="center" style="font-size: 10pt; font-weight: bold; vertical-align: middle;">25 %</td>
  </tr>
  <tr style="background-color: #f8fafc; font-weight: bold;">
    <td class="center">全體團隊合計</td>
    <td style="text-align: right; padding-right: 15px;">全體研發團隊工作實質貢獻度總計（全專案自建代碼 132,749 行）：</td>
    <td class="center" style="font-size: 11pt; color: #1e3a8a;">100 %</td>
  </tr>
</table>

<div class="statement-box">
  <strong>指導老師查核與評審陳述：</strong><br>
  本研究為國立花蓮高級中學歷經一年以上之重點科研專案，由本人全程擔任正式指導老師。針對大會評審建議「聚焦真正原創貢獻並做深」，葉陽甫同學作為第一作者，專注深耕最具原創性之「神經符號 AST Active Healer 四層自癒引擎、Answer-Blind 防篡改邊界與 960 單元 Math16 自動化標準 Benchmark 回歸驗證」，並化解基準對等疑慮；兩位隊友則分別主責情感向度強化學習推薦與混合檢索。經軟體工程代碼審計（全專案自建代碼 13.2 萬行、931 次個人 Git 提交），證實全套系統皆由學生團隊自主自研自測，無外部大學實驗室黑盒依賴。上述研究分工、代碼鑑識數據與 50% / 25% / 25% 實質貢獻比例均由本人嚴格查核屬實，特此出具證明。
</div>

<div class="sign-section">
  <div class="sign-to">
    此致<br>
    各大專校院招生委員會
  </div>
  <div class="sign-fields">
    指導老師簽章：<span class="sign-line"></span>（親筆簽名）<br>
    服務學校：國立花蓮高級中學 &nbsp;&nbsp;&nbsp;&nbsp; 現任職稱：專任教師<br>
    聯絡電話：(03) 822-6108 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 電子信箱：___________________________<br>
    中華民國 115 年 10 月 ______ 日
  </div>
</div>

</body>
</html>
"""

with open(HTML_YUXIU, "w", encoding="utf-8") as f:
    f.write(content_yuxiu)

with open(HTML_WANGHONG, "w", encoding="utf-8") as f:
    f.write(content_wanghong)

# Convert HTML to PDF via Word COM
word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    # 1. Yuxiu Cup
    doc1 = word.Documents.Open(HTML_YUXIU)
    doc1.PageSetup.TopMargin = 16 # ~5.6 mm
    doc1.PageSetup.BottomMargin = 15
    doc1.PageSetup.LeftMargin = 24 # ~8.5 mm
    doc1.PageSetup.RightMargin = 24
    doc1.ExportAsFixedFormat(PDF_YUXIU, 17)
    doc1.Close(False)

    # 2. Wanghong Science Award
    doc2 = word.Documents.Open(HTML_WANGHONG)
    doc2.PageSetup.TopMargin = 15 # ~5.3 mm
    doc2.PageSetup.BottomMargin = 14
    doc2.PageSetup.LeftMargin = 23 # ~8.1 mm
    doc2.PageSetup.RightMargin = 23
    doc2.ExportAsFixedFormat(PDF_WANGHONG, 17)
    doc2.Close(False)

finally:
    word.Quit()

# Inspect generated PDFs
for pdf_path in [PDF_YUXIU, PDF_WANGHONG]:
    d = fitz.open(pdf_path)
    print(f"Verified {os.path.basename(pdf_path)}: {len(d)} pages, Size: {os.path.getsize(pdf_path)/1024:.1f} KB")
