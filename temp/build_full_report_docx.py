import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

OUTPUT_DIR = r"C:\Projects\yangfu-application\temp"
DOCX_PATH = os.path.join(OUTPUT_DIR, "呼吸肌力量訓練_RMST_專業研習完整臨床報告.docx")
CHART1_PATH = os.path.join(OUTPUT_DIR, "chart_physiology_cycle.png")
CHART2_PATH = os.path.join(OUTPUT_DIR, "chart_threshold_vs_resistive.png")
CHART3_PATH = os.path.join(OUTPUT_DIR, "chart_lung_volumes.png")

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
        # Bottom border for H1
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
r_main = p_title.add_run("呼吸肌力量訓練（RMST）臨床應用與生理機制\n專業研習完整成果報告")
r_main.font.name = "Microsoft JhengHei"
r_main.font.size = Pt(22)
r_main.font.bold = True
r_main.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("Clinical Application & Physiological Principles of Respiratory Muscle Strength Training (EMST / IMST)")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = COLOR_MUTED
r_sub.font.italic = True

# Metadata Box Table
meta_table = doc.add_table(rows=2, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(meta_table)
meta_data = [
    [("研習主題：", "呼吸肌力量訓練（RMST / EMST / IMST）全方位臨床實務"), ("主講講師：", "Lauren, MS, CCC-SLP & Jenny, MS, CCC-SLP")],
    [("主辦機構：", "Aspire Respiratory Products / 國際臨床研習培訓"), ("適用領域：", "語言治療 (SLP)、物理治療 (PT)、呼吸治療 (RT)、神經/重症醫學")]
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
add_custom_heading(doc, "一、 研習總結與核心執行摘要 (Executive Summary)", 1)
add_body_p(doc, "呼吸肌力量訓練（Respiratory Muscle Strength Training, RMST）包含呼氣肌力量訓練（EMST）與吸氣肌力量訓練（IMST），已從傳統單純的肺復原擴展為語言治療（SLP）、神經復健及重症拔管的核心介入技術。呼吸肌本質上屬於骨骼肌（Skeletal Muscles），完全符合骨骼肌運動生理學中的『漸進式超負荷原則（Progressive Overload Principle）』與『特異性原則（Specificity Principle）』。")
add_body_p(doc, "本報告彙整研習核心精華，深入探討呼吸生理力學（容積、壓力、氣流）、中樞與周邊神經解剖控制、三大呼吸障礙病理分類、壓力門檻設備（Pressure Threshold Device）相較於阻抗設備之機制優勢，以及標準 5×5×5 臨床訓練 Protocol 在吞嚥障礙、發聲困難、排痰咳嗽防護與 ICU 呼吸器脫離/氣切拔管之實證應用。")

add_callout(doc, 
    "1. 呼吸肌是骨骼肌：只要給予適當負荷刺激（70%~80% 最大呼氣/吸氣壓），即能在 2~4 週內產生 50%~80% 之肌力顯著增長。\n"
    "2. 壓力門檻 vs. 阻抗式：只有壓力門檻式設備（如 EMST 150/75）具備定量彈簧加載，需先產生足夠等長收縮（Isometric）開啟閥門，才允許氣流通過，是實現真正肌力增強的關鍵。\n"
    "3. 跨系統綜效：EMST 訓練不僅強化呼吸幫浦，更能同步活化舌骨上肌群（Suprahyoid muscles），有效增強聲門下壓、吞嚥咽期驅動力與咳嗽異物清除力。",
    "研習核心結論精華")

# Section 2: Origins and Landmark Studies
add_custom_heading(doc, "二、 呼吸肌力量訓練之起源與里程碑實證研究", 1)
add_body_p(doc, "RMST 的發展始於 1990 年代，由佛羅里達大學（University of Florida）Dr. Paul Davenport 與 Dr. Christine Sapienza 等先驅學者開創，經歷了由個案驗證、健康人肌群訓練到神經與重症臨床的大規模拓展：")

# Table 1: Milestone Studies
studies_table = doc.add_table(rows=4, cols=4)
studies_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(studies_table)
studies_headers = ["年代 / 學者", "研究對象 / 族群", "介入協定與強度", "主要臨床成果與意義"]
for i, h in enumerate(studies_headers):
    cell = studies_table.cell(0, i)
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

studies_rows = [
    ("1990s 早期研究", "23 歲先天幼年型喉乳頭狀瘤女性 (呼吸困難/運動不耐)", "4 週 IMST 吸氣肌負荷訓練 (壓力門檻式)", "最大吸氣壓 (MIP) 顯著提升 57%，運動耐受度改善，證實呼吸肌可被漸進超負荷訓練。"),
    ("1997 年\nDr. Davenport &\nDr. Sapienza", "18 歲高中管樂薩克斯風學生 (呼氣肌先驅研究)", "75% MEP 強度，每天 24 次呼氣，每週 5 天，共 2 週", "證實呼氣肌 (Expiratory Muscles) 同樣具備高度可訓練性，奠定 EMST 設備研發基礎。"),
    ("2000s 中風對照研究\n(Sapienza 等)", "27 位中風後吞嚥障礙患者 (真機 vs. 假機 Sham 組)", "70% MEP 強度 EMST 訓練 4 週 vs. 無彈簧假機組", "sEMG 證實活化舌骨上肌群，顯著降低滲漏/誤吸量表評分 (PAS score)，改善吞嚥安全性。")
]

for row_idx, row in enumerate(studies_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = studies_table.cell(row_idx, col_idx)
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

# Section 3: Respiratory Physiology
add_custom_heading(doc, "三、 呼吸生理學基礎：容積 (Volume)、壓力 (Pressure) 與氣流 (Flow)", 1)
add_body_p(doc, "呼吸運動本質上是物理幫浦力學的展現，三大物理量構成持續循環：")

add_body_p(doc, "容積是胸廓與肺部容器的空間大小。吸氣時容器變大，呼氣時容器縮小。", "1. 容積（Volume）：")
add_body_p(doc, "氣體分子推擠肺壁的力量。氣體流動永遠遵循『高壓流向低壓』的壓力梯度（Pressure Gradient）。大氣壓設為 0 cmH2O。", "2. 壓力（Pressure）：")
add_body_p(doc, "氣體在單位時間內進出呼吸道的流動速率。氣流大小取決於壓力梯度差與呼吸道阻抗。", "3. 氣流（Flow）：")

# Insert Diagram 1
if os.path.exists(CHART1_PATH):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    doc.add_picture(CHART1_PATH, width=Inches(6.0))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(8)
    rc = p_cap.add_run("圖 1：吸氣與呼氣循環之肺容積、肺泡內壓（Palv）與氣流動力學關係圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

# Section 4: Neuroanatomy & Muscles
add_custom_heading(doc, "四、 吸氣與呼氣之神經解剖與肌肉控制機制", 1)
add_body_p(doc, "呼吸肌受自主（腦幹）與隨意（大腦皮質）雙重神經系統精密支配，吸氣為生理性主動收縮，呼氣在靜息時為被動彈性回縮，在用力狀況下轉為由腹肌與肋間內肌主導的主動收縮：")

# Table 2: Neuroanatomy
neuro_table = doc.add_table(rows=3, cols=5)
neuro_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(neuro_table)
neuro_headers = ["呼吸動作", "主被動狀態", "主要作用肌群", "支配神經", "神經元胞體所在脊髓節段"]
for i, h in enumerate(neuro_headers):
    cell = neuro_table.cell(0, i)
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

neuro_rows = [
    ("吸氣 (Inspiration)", "主動 (Active)\n肌肉收縮擴張胸廓", "1. 橫膈膜 (Diaphragm)\n2. 肋間外肌 (External Intercostals)\n3. 輔助吸氣肌 (胸鎖乳突肌/斜角肌)", "1. 膈神經 (Phrenic nerve)\n2. 肋間神經 (Intercostal nerves)", "1. 頸髓 C3 - C5 腹角\n2. 胸髓 T1 - T11 腹角"),
    ("主動用力呼氣\n(Active Expiration)\n[發聲/咳嗽/EMST]", "主動 (Active)\n強力壓縮胸廓與腹腔", "1. 腹肌群 (腹直肌/腹內外斜肌/腹橫肌)\n2. 肋間內肌 (Internal Intercostals)", "1. 脊神經前支 (腰/下胸神經)\n2. 肋間神經", "1. 胸腰髓 T7 - L1 節段\n2. 胸髓 T1 - T11 節段")
]

for row_idx, row in enumerate(neuro_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = neuro_table.cell(row_idx, col_idx)
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

add_body_p(doc, "中樞控制中樞：延腦（Medulla）負責產生基本的自主呼吸節律；橋腦（Pons）負責微調呼吸深度與頻率。若患者發生橋腦或延腦中風（Pontine/Medullary Stroke），呼吸的自主協調與精細控制將嚴重受損，出現節律不整與換氣不足。")

# Section 5: 3-Tier Clinical Classification
add_custom_heading(doc, "五、 臨床呼吸障礙之三大病理分類（臨床鑑別診斷模型）", 1)
add_body_p(doc, "研習中講師提出極具臨床實用性的『三大病理分類框架』，協助治療師在評估患者時迅速釐清病因根源：")

# Table 3: 3-Tier Model
cat_table = doc.add_table(rows=4, cols=4)
cat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(cat_table)
cat_headers = ["病理分類範疇", "病理機制與解剖位置", "典型臨床疾病範例", "主要介入策略與考量"]
for i, h in enumerate(cat_headers):
    cell = cat_table.cell(0, i)
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

cat_rows = [
    ("1. 阻抗 / 氣流依賴型\n(Resistive / Flow-Dependent)", "上呼吸道或喉部通道物理性狹窄、阻塞，導致氣流進出阻力劇增。", "聲帶息肉/結節、喉腫瘤、喉乳頭狀瘤、聲帶麻痺、聲門下狹窄、運動誘發喉阻塞 (EILO)。", "外科切除/喉部手術解除結構阻塞；搭配發聲治療與氣道減敏。"),
    ("2. 彈性 / 容積依賴型\n(Elasticity / Volume-Dependent)", "肺實質或胸壁組織硬化失去彈性（順應性 Compliance 降低），肺擴張或回縮受限。", "特發性肺纖維化 (IPF)、COPD/肺氣腫、放射線照射後組織纖維化、肺葉切除術後、胸壁僵硬。", "胸廓活動度運動、肺復原（Pulmonary Rehab）、藥物抗纖維化及呼吸調節訓練。"),
    ("3. 肌力 / 壓力門檻型\n(Pressure Threshold / Weakness)", "神經傳導中斷或肌肉失用性萎縮，呼吸幫浦無法產生足夠進氣/排氣壓力。", "肌萎縮側索硬化症 (ALS)、帕金森氏症 (PD)、多發性硬化症 (MS)、中風、脊髓損傷、長期臥床失能。", "【RMST / EMST / IMST 之核心適應症】透過漸進超負荷訓練強化吸/呼氣骨骼肌群。")
]

for row_idx, row in enumerate(cat_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = cat_table.cell(row_idx, col_idx)
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

# Section 6: Lung Volumes & Capacities
add_custom_heading(doc, "六、 肺容量與通氣指標解析 (Lung Volumes & Minute Ventilation)", 1)
add_body_p(doc, "掌握肺容積（Volumes）與肺容量（Capacities）是解讀肺功能報告（PFT）與評估說話氣流儲備的基礎：")

# Insert Diagram 3
if os.path.exists(CHART3_PATH):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    doc.add_picture(CHART3_PATH, width=Inches(5.8))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    rc = p_cap.add_run("圖 2：成年人靜息與最大呼吸容積與肺容量分配模型圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

# Table 4: Lung Volumes
vol_table = doc.add_table(rows=6, cols=3)
vol_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(vol_table)
vol_headers = ["術語名稱 (縮寫)", "生理學定義", "臨床評估與語言治療意義"]
for i, h in enumerate(vol_headers):
    cell = vol_table.cell(0, i)
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

vol_rows = [
    ("潮氣容積 (Tidal Volume, VT)", "安靜平靜呼吸時，每次吸入或呼出的氣體量（約 500 mL）。", "反映基本靜態通氣量；呼吸急促淺快時 VT 降低。"),
    ("功能殘氣量 (FRC)", "平靜呼氣結束後，肺內依然殘留的氣體容積。", "胸廓外彈力與肺向內回縮力達成平衡的靜止點。"),
    ("肺活量 (Vital Capacity, VC)", "最大全力吸氣後，所能盡力呼出的最大氣體總量。", "語音發聲、大聲朗讀與長句發聲的最主要氣流動能來源。"),
    ("殘氣容積 (Residual Volume, RV)", "全力最大呼氣後，肺內依然無法排出的殘餘氣量。", "避免肺泡完全塌陷；肺氣腫/氣道受阻時 RV 常異常升高。"),
    ("每分鐘通氣量 (Minute Ventilation)", "每分鐘進出肺部的氣體總量：Minute Ventilation = VT × 呼吸頻率 (f)。", "重症與吞嚥病患呼吸負擔與換氣效率的核心監測指標。")
]

for row_idx, row in enumerate(vol_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = vol_table.cell(row_idx, col_idx)
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

# Section 7: Device Mechanism Comparison
add_custom_heading(doc, "七、 訓練設備運作原理：壓力門檻式 vs. 阻抗式設備深度對比", 1)
add_body_p(doc, "市售呼吸訓練器材琳瑯滿目，研習中特別強調『壓力門檻式（Pressure Threshold）』與『阻抗式（Resistive）』在肌力訓練生理上的根本差異：")

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
    rc = p_cap.add_run("圖 3：壓力門檻式設備（EMST）與阻抗式設備之壓力/氣流響應曲線對比圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

# Table 5: Device Comparison
dev_table = doc.add_table(rows=6, cols=3)
dev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(dev_table)
dev_headers = ["比較維度", "壓力門檻式設備 (如 EMST 150 / 75)", "阻抗式設備 (如 吸管、小孔呼吸器)"]
for i, h in enumerate(dev_headers):
    cell = dev_table.cell(0, i)
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

dev_rows = [
    ("核心機械構造", "內部具備精密『彈簧與止逆閥門（Spring-loaded Valve）』。", "內部無彈簧，僅透過改變孔徑大小（Orifice size）提供阻力。"),
    ("閥門與氣流反應", "起始閥門完全關閉，無氣流通過；只有當口腔內壓達到預設閾值，閥門才瞬間開啟允許氣流通過。", "吹氣一開始即有氣流洩漏流出，全程無閉合閥門阻擋。"),
    ("肌肉收縮型態", "【等長收縮 (Isometric) + 等張收縮 (Isotonic)】高強度肌肉徵召。", "純動態流動阻抗，肌肉收縮強度隨流速快慢浮動。"),
    ("負荷量化與超負荷", "可精確校準壓力（如 30 ~ 150 cmH2O），提供穩定的超負荷刺激。", "阻力高度依賴患者當下的吹氣流速，無法提供精確的壓力定量。"),
    ("臨床主要目標", "【骨骼肌力量強化】增強咳嗽力、喉上提幅度、發聲響度與排痰力。", "【呼吸耐力/步調調節】調整呼吸速率、氣道減敏或運動耐力調控。")
]

for row_idx, row in enumerate(dev_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = dev_table.cell(row_idx, col_idx)
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

# Section 8: Clinical Protocol
add_custom_heading(doc, "八、 標準臨床訓練協定與劑量設定 (The 5 × 5 × 5 Protocol)", 1)
add_body_p(doc, "為確保呼吸肌獲得足夠的生理刺激並避免疲勞過度，文獻建立了標準化的『5×5×5 訓練協定』：")

# Table 6: Protocol Table
prot_table = doc.add_table(rows=5, cols=2)
prot_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(prot_table)
prot_headers = ["訓練參數項目", "標準臨床訓練協定 (Protocol) 規範與指引"]
for i, h in enumerate(prot_headers):
    cell = prot_table.cell(0, i)
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

prot_rows = [
    ("訓練組數與次數 (5 × 5)", "每次連續吹氣 5 次為 1 組，組間休息 15~30 秒；每天進行 5 組，全天總計 25 次有效吹氣。"),
    ("訓練頻率與週期 (5 × 5)", "每週訓練 5 天，連續介入 4 至 5 週為一個標準療程。"),
    ("目標強度設定", "設定於患者最大呼氣壓（MEP）或最大吸氣壓（MIP）的 70% ～ 80% 閾值。"),
    ("去適應效應 (De-training)", "訓練停止後約 7 週肌力開始退步，建議療程後維持每週 2~3 天、每天 25 次的保養訓練。")
]

for row_idx, row in enumerate(prot_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = prot_table.cell(row_idx, col_idx)
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

# Section 9: Clinical Indications
add_custom_heading(doc, "九、 多元臨床族群適應症與跨科別應用效益", 1)
add_body_p(doc, "RMST 不僅是呼吸器官的復健，更是跨越吞嚥、語音發聲、咳嗽排痰與重症照護的多功能治療媒介：")

# Table 7: Indications
ind_table = doc.add_table(rows=6, cols=3)
ind_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(ind_table)
ind_headers = ["臨床適應領域 / 疾病族群", "生理功能缺陷", "RMST 介入效益與機制"]
for i, h in enumerate(ind_headers):
    cell = ind_table.cell(0, i)
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

ind_rows = [
    ("吞嚥困難 (Dysphagia)\n[中風 / 帕金森氏症 / 衰老]", "喉部上提不足、會厭軟骨翻轉不全、環咽肌開啟困難、吞嚥後咽部殘留及誤吸。", "EMST 活化舌骨上肌群，大幅增加喉部向前向上拉提位移，改善食道入口開啟並降低嗆咳率。"),
    ("發聲障礙 (Dysphonia)\n[肌張力性/帕金森/專業用聲者]", "聲門下壓不足、說話氣息微弱、句尾沒氣、代償性聲帶緊繃與肌肉疲乏。", "強化呼氣肌肉幫浦，建立穩定充足的聲門下氣壓，提升發聲響度與音質持久度。"),
    ("咳嗽效能不全 (Dystussia)\n[ALS / 神經肌肉疾病 / SCI]", "腹肌與肋間肌無力，無法產生足夠呼氣峰值流速（PCF）清除氣道痰液。", "顯著提升最大呼氣壓（MEP）與咳嗽氣流衝擊力，提升自我排痰能力，預防吸入性肺炎。"),
    ("加護病房 (ICU) / 氣切拔管\n(Tracheostomy Decannulation)", "呼吸器依賴性廢用萎縮、膈肌無力、氣切拔管困難及延長住院天數。", "IMST 強化吸氣膈肌；EMST 增強上呼吸道肌力與咳嗽力，顯著縮短脫機與拔管時間。"),
    ("頭頸部腫瘤 (Head & Neck Cancer)\n[放療/化療後纖維化]", "放療後頸部肌肉纖維化僵硬、喉部活動度受限、慢性吸入性肺炎高風險。", "維持呼吸肌收縮力道，減緩放射線纖維化對吞嚥與發聲的長期衝擊。")
]

for row_idx, row in enumerate(ind_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = ind_table.cell(row_idx, col_idx)
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

# Section 10: Clinical Q&A and Practical Tips
add_custom_heading(doc, "十、 臨床問答實務重點與執行注意事項", 1)
add_body_p(doc, "1. 吹嘴選用技巧（Mouthpiece Selection）：", "A. 口唇密封困難之處置：")
add_body_p(doc, "對於顏面神經麻痺、中風單側無力或口唇閉合不全的患者，應優先選用『舒適型扁形吹嘴（Comfort Mouthpiece）』或輔助口角手動加壓密封，以防止氣體由嘴角側漏導致壓力無法建立。")

add_body_p(doc, "2. 遠距醫療（Telepractice / Telehealth）實施可行性：", "B. 遠距與居家訓練：")
add_body_p(doc, "文獻證實 EMST 具備極佳的遠距教學適應性。治療師可透過視訊教導患者設備讀數設定、正確腹式用力方式並線上審核每日訓練日誌（Training Log）。")

add_body_p(doc, "3. 禁忌症與安全防範（Contraindications）：", "C. 臨床安全紅線：")
add_body_p(doc, "未經治療之氣胸（Pneumothorax）、近期鼓膜破裂/中耳手術、未控制的嚴重高血壓、主動脈瘤、近期腹部/眼科手術或肋骨骨折患者，應暫緩進行高阻力 EMST 訓練，或於醫師許可下從極低阻力開始。")

# Save document
doc.save(DOCX_PATH)
print(f"Document successfully created at: {DOCX_PATH}")
