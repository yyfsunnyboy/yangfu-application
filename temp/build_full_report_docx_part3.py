import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

OUTPUT_DIR = r"C:\Projects\yangfu-application\temp"
DOCX_PATH = os.path.join(OUTPUT_DIR, "呼吸肌力量訓練_RMST_重症脫機與頭頸癌整合報告.docx")
CHART1_PATH = os.path.join(OUTPUT_DIR, "chart3_icu_decannulation_pathway.png")
CHART2_PATH = os.path.join(OUTPUT_DIR, "chart3_radiation_fibrosis.png")
CHART3_PATH = os.path.join(OUTPUT_DIR, "chart3_acdf_laryngectomy_progress.png")

doc = Document()

# Set standard margins (1 inch / 2.54 cm)
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Color Palette Constants
COLOR_PRIMARY = RGBColor(27, 54, 93)     # Navy Blue #1B365D
COLOR_SECONDARY = RGBColor(41, 128, 185) # Steel Blue #2980B9
COLOR_DARK = RGBColor(44, 62, 80)        # Dark Slate #2C3E50
COLOR_MUTED = RGBColor(127, 140, 141)    # Muted Gray #7F8C8D
HEX_PRIMARY = "1B365D"
HEX_LIGHT_BG = "F4F6F9"
HEX_ALT_ROW = "EBF5FB"
HEX_BORDER = "BDC3C7"
HEX_HIGHLIGHT = "FEF9E7"
HEX_ACCENT_BORDER = "F39C12"

# Helper function to set table cell background color
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

# Helper function to set table borders
def set_table_borders(table, hex_color=HEX_BORDER):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{hex_color}"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_PRIMARY}"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

# Helper function to add callout box
def add_callout(doc, text, title="重點提示 / Key Takeaway"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, HEX_HIGHLIGHT)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_ACCENT_BORDER}"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    run_title = p.add_run(f"📌 {title}\n")
    run_title.font.bold = True
    run_title.font.size = Pt(10.5)
    run_title.font.color.rgb = RGBColor(183, 110, 0)
    run_title.font.name = "Microsoft JhengHei"
    
    run_text = p.add_run(text)
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = COLOR_DARK
    run_text.font.name = "Microsoft JhengHei"
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Format paragraph helper
def add_custom_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Microsoft JhengHei"
    run.font.bold = True
    
    if level == 1:
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(16)
        run.font.color.rgb = COLOR_PRIMARY
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="4" w:color="{HEX_PRIMARY}"/></w:pBdr>')
        p._p.get_or_add_pPr().append(pBdr)
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_SECONDARY
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_DARK
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Microsoft JhengHei"
        r_pre.font.bold = True
        r_pre.font.size = Pt(10.5)
        r_pre.font.color.rgb = COLOR_PRIMARY
    
    r = p.add_run(text)
    r.font.name = "Microsoft JhengHei"
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_DARK
    return p

# ----------------- DOCUMENT CONTENT GENERATION -----------------

# Header / Title Block
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(2)
r_main = p_title.add_run("呼吸肌力量訓練（RMST）重症脫機、特殊病理與頭頸癌整合應用\n專業研習成果報告（第三部分）")
r_main.font.name = "Microsoft JhengHei"
r_main.font.size = Pt(20)
r_main.font.bold = True
r_main.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("ICU Tracheostomy Decannulation, Head & Neck Radiation Fibrosis, Total Laryngectomy & Complex Clinical Case Protocols")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = COLOR_MUTED
r_sub.font.italic = True

# Metadata Box Table
meta_table = doc.add_table(rows=2, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(meta_table)
meta_data = [
    [("研習主題：", "ICU 氣切脫機、頭頸癌放射纖維化、全喉切除及罕見複雜病理整合"), ("主講專家：", "Lauren, MS, CCC-SLP & Jenny, MS, CCC-SLP")],
    [("主辦機構：", "Aspire Respiratory Products / 國際臨床研習培訓"), ("專業領域：", "重症醫學、頭頸腫瘤外科、語言治療、物理治療、心肺呼吸照護")]
]
for row_idx, row_data in enumerate(meta_data):
    for col_idx, (k, v) in enumerate(row_data):
        cell = meta_table.cell(row_idx, col_idx)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_background(cell, HEX_LIGHT_BG)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        rk = p.add_run(k)
        rk.font.name = "Microsoft JhengHei"
        rk.font.bold = True
        rk.font.size = Pt(9.5)
        rk.font.color.rgb = COLOR_PRIMARY
        rv = p.add_run(v)
        rv.font.name = "Microsoft JhengHei"
        rv.font.size = Pt(9.5)
        rv.font.color.rgb = COLOR_DARK

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 1: Executive Summary
add_custom_heading(doc, "一、 第三階段研習重點執行摘要 (Executive Summary)", 1)
add_body_p(doc, "本階段研習聚焦於呼吸肌力量訓練（RMST）在『加護病房（ICU）脫機與氣切拔管』、『頭頸癌放射線誘發纖維化（RIF）』、『全喉切除術（Total Laryngectomy）造口銜接』、『頸椎前路減壓融合術（ACDF）術後神經麻痺』及『複雜神經罕病邊界判定』等高難度臨床情境的整合應用。核心結論包括：")
add_body_p(doc, "1. 加護病房（ICU）整合評估階梯：落實『套管餘裕 $\\rightarrow$ 氣囊放氣 $\\rightarrow$ 單向說話閥（PMV）耐受 $\\rightarrow$ 臨床表情/膚色監測 $\\rightarrow$ IMST (IA 150) / EMST 介入』之標準化路徑，能有效縮短呼吸器使用天數、加速氣切拔管並降低再插管率。")
add_body_p(doc, "2. 頭頸癌放射線誘發纖維化（RIF）：放療造成進行性膠原蛋白沉積與微血管內皮壞死，需採 8 週以上之長療程 EMST 訓練以維持肌肉順應性；最新 2026 年研究證實 RMST 能顯著降低頭頸癌患者對鴉片類止痛藥（Opioids）之依賴性。")
add_body_p(doc, "3. 全喉切除術（Total Laryngectomy）創新突破：利用圓形轉接頭直接密合氣切造口（Stoma Baseplate），成功在無喉患者中推動 EMST，大幅提升自發排痰力與食道語發聲響度。")
add_body_p(doc, "4. 禁忌與安全邊界：重症肌無力（MG）急性發作期絕對禁忌抗阻訓練；ACDF 頸椎術後或頭頸癌皮瓣重建需經外科醫師確認組織完全癒合後方可施加口咽內壓。")

add_callout(doc,
    "• 重症脫機黃金標準：FiO2 <= 50%、PEEP <= 10 cmH2O、氣囊完整放氣且能耐受 Passy-Muir 說話閥時，即為啟動 IMST/EMST 之最佳窗口。\n"
    "• 臨床觀察重於數據：ICU 訓練時切勿單看血氧儀（SpO2），病患臉部表情緊繃、眼角瞇起或膚色轉為灰暗（Gray hue）即為缺氧/疲勞警訊，應立即拔除設備充分休息。\n"
    "• 保險與行政實務：多數健保（如 Medicare Part B）給付 EMST 75 Lite（需附吞嚥/發聲診斷及醫師處方 Script）；EMST 150 自費約 60 美元，是效益極高的一生單次性投資。",
    "第三階段核心重點速記")

# Section 2: Acute Care & Inter-professional Collaboration
add_custom_heading(doc, "二、 急性照護病房跨科推廣與行政處方實務", 1)
add_body_p(doc, "在急性醫療體系（Acute Care Setting）中，許多神經或骨科病患（如帕金森氏症因髖關節骨折入院）常因臥床而誘發吸入性肺炎。語言治療師應主動打破科別藩籬，建立標準化的轉介與照護流程：")

# Table 1: Inpatient Workflow & Insurance Matrix
ins_table = doc.add_table(rows=5, cols=3)
ins_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(ins_table)
ins_headers = ["醫療照護場域 / 保險類別", "行政處方與照會流程 (Workflow)", "設備取得與給付規則重點"]
for i, h in enumerate(ins_headers):
    cell = ins_table.cell(0, i)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_background(cell, HEX_PRIMARY)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.name = "Microsoft JhengHei"

ins_rows = [
    ("急性病房 (Acute Inpatient)\n[骨科/神經/一般內科]", "主動衛教護理與醫療團隊；針對高風險長者建立『口腔照護 + 預防性 RMST 照會機制』。", "住院期間可由醫院衛材進貨提供，或出院前衛教家屬自費購買備用。"),
    ("門診與居家長照\n(Outpatient / Home Health)", "門診治療師填寫 DME 輔具申請表格，取得主治醫師簽署之醫療醫囑（Doctor Script）。", "多數商業保險與 Medicare Part B 給付 80%（主要針對 EMST 75 Lite 具健保碼）。"),
    ("自費購買途徑\n(Self-Pay Direct)", "若保險核退或需使用 EMST 150，指導患者直接向代理商或官網訂購（約 60-62 美元）。", "治療師應正面衛教：相較於吸入性肺炎住院的高額花費，EMST 為高性價比的健康投資。"),
    ("遠距醫療模式\n(Telehealth / Telepractice)", "臨床試驗證實：每週 2 次線上視訊指導 + 3 次居家自主練習，療效等同實體門診。", "適合帕金森氏症行動不便長者，由治療師線上抽查訓練日誌與吹氣動作。")
]

for row_idx, row in enumerate(ins_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = ins_table.cell(row_idx, col_idx)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_background(cell, bg_color)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK
        r.font.name = "Microsoft JhengHei"

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 3: ICU Decannulation & Weaning Pathway
add_custom_heading(doc, "三、 加護病房（ICU）呼吸器脫離與氣切拔管整合路徑", 1)
add_body_p(doc, "加護病房病患長期依賴呼吸器易產生橫膈肌失用性萎縮（VIDD）與咽喉去敏感化。RMST 結合單向說話閥（Passy-Muir Valve, PMV）為現代重症拔管的核心策略：")

# Insert Diagram 1
if os.path.exists(CHART1_PATH):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    doc.add_picture(CHART1_PATH, width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    rc = p_cap.add_run("圖 1：ICU 氣切脫機、單向說話閥 (PMV) 耐受性評估與 RMST 臨床介入階梯路徑圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

# Table 2: ICU Monitoring & Safety Criteria
icu_table = doc.add_table(rows=5, cols=3)
icu_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(icu_table)
icu_headers = ["評估階梯環節", "合格指標與安全門檻", "紅線禁忌與異常處置原則"]
for i, h in enumerate(icu_headers):
    cell = icu_table.cell(0, i)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_background(cell, HEX_PRIMARY)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.name = "Microsoft JhengHei"

icu_rows = [
    ("1. 生理參數穩定度", "FiO2 <= 50%, PEEP <= 10 cmH2O, 呼吸速率 < 30 次/分, 無大劑量升壓劑 (Pressors)。", "未控制高血壓、活動性心肌梗塞、急性氣胸（Pneumothorax）或氣管食道瘻管絕對禁忌。"),
    ("2. 氣管套管評估", "評估氣切套管尺寸（如大號 Shiley #8 需確認氣道周邊是否有足夠呼氣空間，必要時降號）。", "若套管過粗完全阻斷上呼吸道，氣囊放氣後仍無法通氣者，嚴禁佩戴說話閥或吹氣。"),
    ("3. 說話閥 (PMV) 耐受", "氣囊完全抽氣（Deflated），佩戴在線（In-line）或直接接合 PMV，能維持平穩發聲與呼吸。", "若出現呼吸費力、喘鳴（Stridor）或血氧驟降，立即移除說話閥並重新充氣。"),
    ("4. 臨床細微徵象監測", "全程密切注視病患神情、眼部反射、雙頰張力與唇周膚色變化。", "【研習實例警示】：血氧儀數值正常但病患膚色變灰暗（Gray hue）時，代表微循環障礙，須立即中斷休息。")
]

for row_idx, row in enumerate(icu_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = icu_table.cell(row_idx, col_idx)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_background(cell, bg_color)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK
        r.font.name = "Microsoft JhengHei"

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 4: Head and Neck Radiation Fibrosis
add_custom_heading(doc, "四、 頭頸癌放射線誘發纖維化（RIF）病理機轉與介入指引", 1)
add_body_p(doc, "放射線治療（Radiation Therapy）在消滅腫瘤的同時，會對周邊正常組織造成終生進行性的不可逆損傷，稱為放射線誘發纖維化（Radiation-Induced Fibrosis, RIF）：")

# Insert Diagram 2
if os.path.exists(CHART2_PATH):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    doc.add_picture(CHART2_PATH, width=Inches(6.0))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    rc = p_cap.add_run("圖 2：頭頸癌放療後組織纖維化進程（RIF）與 EMST 長期肌力保護效益對比圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

add_body_p(doc, "1. 纖維化之微觀病理學破壞：", "A. 組織病理學特徵：")
add_body_p(doc, "• 動物與人體切片證實：放射線破壞微血管內皮細胞引起長期缺血；成纖維細胞異常過度活化，在肌肉束間沉積大量無彈性的膠原蛋白與纖維蛋白（Fibrin）。")
add_body_p(doc, "• 骨骼肌細胞核腫脹畸形、粒線體崩解，肌纖維排列由規則緊密轉為嚴重紊亂僵硬，使喉部拉提與咽壁蠕動喪失順應性（Compliance）。")

add_body_p(doc, "2. 臨床研究實證（Dr. Kate Hutcheson, 2018 研究）：", "B. 臨床長療程介入成果：")
add_body_p(doc, "• 對象：64 位放療完成 5 年以上之慢性誤吸頭頸癌病患（91% 初始呼氣壓低於正常值）。")
add_body_p(doc, "• 介入：進行 8 週 EMST 訓練（每週 5 天、每天 25 次）。結果顯示最大呼氣壓（MEP）顯著回升，吞嚥效率與進食問卷（EAT-10）大幅改善。")
add_body_p(doc, "• 2026 最新研究里程碑：放療期間與放療後及早介入 RMST，能減輕組織沾黏疼痛，顯著降低患者對鴉片類止痛藥（Opioids）之使用量與依賴度！")
add_body_p(doc, "• 淋巴水腫（Lymphedema）併用指引：頭頸癌伴隨淋巴水腫之患者，強烈建議在穿戴『加壓頭頸套（Compression Garment）』的包覆狀態下進行 EMST 吹氣，能同步促進淋巴回流並強化肌群。")

# Section 5: Total Laryngectomy & Stoma Application
add_custom_heading(doc, "五、 全喉切除術（Total Laryngectomy）造口直接銜接技術與食道語發聲", 1)
add_body_p(doc, "全喉切除術後氣道與消化道完全分離，傳統認為無法進行常規發聲治療。研習展示了 Vicky Lewis 等學者開創的『造口直接接合 EMST 技術』：")

# Table 3: Total Laryngectomy Application
lar_table = doc.add_table(rows=4, cols=3)
lar_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(lar_table)
lar_headers = ["病患亞型 / 處置環節", "器材連接與操作手法 (Stoma Coupling)", "臨床效益與安全防護核心"]
for i, h in enumerate(lar_headers):
    cell = lar_table.cell(0, i)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_background(cell, HEX_PRIMARY)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.name = "Microsoft JhengHei"

lar_rows = [
    ("無氣管食道穿刺 (Non-TEP)\n全喉切除病患", "拔除口含吹嘴，將圓形底座轉接頭直接緊密貼合於頸部造口基盤 (Baseplate)。", "深吸氣後對造口用力吹氣爆發，增強腹肌與胸廓排痰推力，維持肺泡換氣效率。"),
    ("具 TEP 語音瓣膜者\n(Tracheoesophageal Puncture)", "同上連接方式，但需於極低阻力（如 5~10 cmH2O）起始，由治療師嚴密監控。", "【高風險警戒】：過高氣壓可能導致 TEP 語音瓣膜移位（Dislodgement）或周邊滲漏，需謹慎評估。"),
    ("食道語 (Esophageal Speech)\n訓練病患", "透過 EMST 強化腹肌呼氣幫浦，建立高動能呼氣氣流以注入食道上端。", "提供足夠氣壓振動咽食道交界處（PE segment），大幅提升食道語之音量與音質清晰度。")
]

for row_idx, row in enumerate(lar_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = lar_table.cell(row_idx, col_idx)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_background(cell, bg_color)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK
        r.font.name = "Microsoft JhengHei"

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 6: Vocal Fold Paresis & Post-Injection
add_custom_heading(doc, "六、 聲帶麻痺/萎縮、老年性聲帶退化（Presbyphonia）與注射術後銜接", 1)
add_body_p(doc, "聲帶閉合不全（Glottal Incompetence）常見於喉返神經麻痺（如甲狀腺術後）、老年性聲帶萎縮（Presbyphonia）或帕金森氏症聲帶弓形病變（Bowing）：")

# Insert Diagram 3
if os.path.exists(CHART3_PATH):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    doc.add_picture(CHART3_PATH, width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    rc = p_cap.add_run("圖 3：ACDF 頸椎術後病患 5 週訓練歷程 與 頭頸癌/全喉切除術後功能改善指標圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

add_body_p(doc, "1. 聲帶注射填充術後（Post-Augmentation Injection）銜接訓練：", "A. 喉科術後黃金窗口：")
add_body_p(doc, "• 聲帶注射自體脂肪、玻尿酸或微晶瓷後，待喉科醫師確認組織定型（通常術後 2~3 週），立即啟動 EMST 75 Lite 或 150 訓練。")
add_body_p(doc, "• 臨床實錄個案：老年性聲帶退化長者在注射前因聲門漏氣無法吹開設備；注射後搭配 EMST 訓練，發聲響度、最長發聲時間（MPT）自 6 秒大幅延長至 15 秒以上。")

add_body_p(doc, "2. 聲帶麻痺之『代償幫浦理論』：", "B. 呼吸肌代償喉部閥門缺陷：")
add_body_p(doc, "• 聲帶麻痺無法完全閉合時，RMST 並非修復神經，而是強化下方的『肺部呼氣幫浦』。")
add_body_p(doc, "• 藉由強大的呼氣肌產生倍增的聲門下氣流推力，代償鬆弛漏氣的喉部閥門，達成清晰有力的發聲與有效咳嗽。")

# Section 7: Complex Clinical Cases
add_custom_heading(doc, "七、 複雜臨床病例深度剖析 (Complex Case Studies)", 1)

# Table 4: Case Studies Summary
case_table = doc.add_table(rows=4, cols=4)
case_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(case_table)
case_headers = ["臨床個案背景", "病理機制與診斷挑戰", "RMST 介入處方與策略", "最終治療成效與轉歸"]
for i, h in enumerate(case_headers):
    cell = case_table.cell(0, i)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_background(cell, HEX_PRIMARY)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.name = "Microsoft JhengHei"

case_rows = [
    ("個案 1：61歲男性\n頸椎前路融合術 (ACDF)\n[C2-C4, C6-T1 融合]", "術後咽後壁嚴重血腫水腫壓迫，伴隨右側喉返神經麻痺，固體食物吞嚥困難及發聲疲勞。", "術後 6 週組織癒合後啟動 EMST；自 38 cmH2O 起始，每週調升 1/4 圈至第 5 週達 80 cmH2O。", "舌骨上提恢復正常，VFSS 證實梨狀窩殘留消失，喉部閉合大幅改善，恢復由口正常進食。"),
    ("個案 2：62歲女性\n二尖瓣置換術後 (MVR)\n[插管 8 天，術後聲帶麻痺]", "術後拔管困難，左側聲帶麻痺致聲門閉合不全，進食液體顯著滲漏誤吸，咳嗽微弱無力。", "自加護病房由低強度 EMST (40 cmH2O) 起始，每兩天調升 2 cmH2O 密集訓練。", "第 2 週咳痰力道與聲門下壓顯著提升，經由口進食稠液體無嗆咳，成功拔除鼻胃管出院。"),
    ("個案 3：安寧緩和患者\n帕金森氏症合併頭頸癌\n[雙側口唇下垂漏氣]", "雙側顏面神經受損口角嚴重漏氣，氣體無法聚積，患者最大心願為『能讓妻子聽清楚我說話』。", "由妻子協助用雙手手動捏緊固定病患口唇兩側，以 EMST 75 Lite 進行生活品質導向訓練。", "成功產生爆發性氣流，說話響度大幅提升，達成安寧療護階段極珍貴之家庭溝通目標。")
]

for row_idx, row in enumerate(case_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = case_table.cell(row_idx, col_idx)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_background(cell, bg_color)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK
        r.font.name = "Microsoft JhengHei"

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 8: Controversies & Red Lines
add_custom_heading(doc, "八、 臨床爭議、難治性症狀與安全紅線判定", 1)

add_body_p(doc, "1. 重症肌無力（Myasthenia Gravis, MG）之絕對與相對邊界：", "A. MG 訓練原則：")
add_body_p(doc, "• 急性發作期（Crisis）、急性肌無力進展或接受 IVIG / 血漿置換治療中，【絕對禁忌】進行抗阻 RMST，否則將耗竭神經肌肉接頭之乙醯膽鹼（ACh），引發呼吸衰竭。")
add_body_p(doc, "• 僅在神經科醫師確認進入穩定緩解期（Remission）且認知良好之病患，才可在密切監督下嘗試極低強度訓練（< 20%~30% MEP）。")

add_body_p(doc, "2. 難治性慢性咳嗽（Refractory Chronic Cough）與氣道過敏：", "B. 慢性咳嗽臨床決策：")
add_body_p(doc, "• 若慢性咳嗽源於中風或喉部感覺神經受損，EMST 能有效改善咳嗽排痰效率。")
add_body_p(doc, "• 若為原因不明之氣道高敏感性（Neurogenic Cough），高阻力吹氣有時在初期會誘發咳嗽痙攣；最新文獻（2023）指出短期低阻力 RMST 可改善聲門下氣流協調，需搭配喉部放鬆與氣道減敏手法。")

add_body_p(doc, "3. 震盪呼氣排痰閥（Acapella / Flutter）與 EMST 之本質差異：", "C. 再次釐清設備定位：")
add_body_p(doc, "• 呼吸治療科常用之 Acapella 內部無彈簧，依靠搖臂產生振動氣流以震鬆深層痰液，屬於『阻抗式排痰輔具』。")
add_body_p(doc, "• EMST 具備精密彈簧門，需克服等長收縮閾值，為專門『強化骨骼肌力量』之神經肌肉復健設備，兩者目的截然不同，臨床不可混為一談。")

# Section 9: Complete Workshop Synthesis
add_custom_heading(doc, "九、 全研習三大篇章實踐指南總結 (Synthesis)", 1)
add_body_p(doc, "綜合本次完整專業研習，呼吸肌力量訓練（RMST）已確立為橫跨急性、亞急性與居家慢性期之強效循證工具。臨床治療師應熟練掌握：")
add_body_p(doc, "• 生理基礎：容積、壓力、氣流之物理幫浦連動，吸氣（C3-C5 膈神經）與呼氣（T7-L1 腹肌群）神經支配。")
add_body_p(doc, "• 鑑別診斷：清楚區分『阻抗型』、『彈性型』與『肌力型』障礙。")
add_body_p(doc, "• 處方劑量：標準 5×5×5 協定（75% MEP）或神經退化症 30%~50% 低負荷維持，並落實 1/4 圈漸進調升法則。")
add_body_p(doc, "• 多元適應：在吞嚥咽期喉上提、食道括約肌開啟、自發咳嗽排痰、發聲響度、ICU 脫機拔管與頭頸癌放療纖維化中發揮無可取代的臨床價值。")

# Save document
doc.save(DOCX_PATH)
print(f"Part 3 Word Document successfully created at: {DOCX_PATH}")
