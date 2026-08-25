import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

OUTPUT_DIR = r"C:\Projects\yangfu-application\temp"
DOCX_PATH = os.path.join(OUTPUT_DIR, "呼吸肌力量訓練_RMST_臨床實務與進階病例處方報告.docx")
CHART1_PATH = os.path.join(OUTPUT_DIR, "chart2_calibration_steps.png")
CHART2_PATH = os.path.join(OUTPUT_DIR, "chart2_cough_dynamics.png")
CHART3_PATH = os.path.join(OUTPUT_DIR, "chart2_swallow_hyoid.png")

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
r_main = p_title.add_run("呼吸肌力量訓練（RMST）臨床實務操作與進階病例處方\n專業研習成果報告（第二部分）")
r_main.font.name = "Microsoft JhengHei"
r_main.font.size = Pt(21)
r_main.font.bold = True
r_main.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("Advanced Clinical Protocols, Manometry Calibration, Neuroplasticity & Disease-Specific RMST Applications")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = COLOR_MUTED
r_sub.font.italic = True

# Metadata Box Table
meta_table = doc.add_table(rows=2, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(meta_table)
meta_data = [
    [("課程主題：", "RMST 臨床實務、設備校準、神經可塑性與進階個案解析"), ("主講講師：", "Lauren, MS, CCC-SLP & Jenny, MS, CCC-SLP")],
    [("主辦機構：", "Aspire Respiratory Products / 國際臨床研習培訓"), ("重點範疇：", "ALS/PD/中風處方、1/4圈校準法、咳嗽氣流動力學、吞嚥肌電圖分析")]
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
add_custom_heading(doc, "一、 第二階段研習重點執行摘要 (Executive Summary)", 1)
add_body_p(doc, "本階段研習深入探討呼吸肌力量訓練（RMST）在臨床實務中的執行技術、精準設備校準、神經可塑性生物學機制，以及在不同神經與器質性疾病中的個別化處方。重點涵蓋：")
add_body_p(doc, "1. 神經可塑性十大原則（Kleim & Jones）如何引導 RMST 之運動單元徵召（Motor Unit Recruitment）、突觸新生（Synaptogenesis）與骨骼肌肥大（Hypertrophy）。")
add_body_p(doc, "2. 臨床壓力計（Manometer）客觀測量計算流程 vs. 無壓力計時的『1/4 圈旋鈕校準法（Quarter-Turn Method）』。")
add_body_p(doc, "3. 吞嚥咽期喉部運動學（Troche et al. 研究）：證實 EMST 顯著增加舌骨上提位移、擴大食道上括約肌（UES）開啟並延長舌骨上肌群 sEMG 活化時間。")
add_body_p(doc, "4. 自發性咳嗽氣流動力學（Plowman et al. 研究）：咳嗽容積加速（CVA）與呼氣峰值流速（PCF）作為吞嚥誤吸風險的強效預測指標。")
add_body_p(doc, "5. 漸凍症（ALS 30%~50% 低負荷維持）、帕金森氏症（早期預防性介入）、痙攣性發聲障礙鑑別診斷、頭頸癌皮瓣重建及心臟術後之精準決策。")

add_callout(doc,
    "• 臨床黃金法則：高科技（壓力計）以 75% MEP/MIP 起始；低科技（無壓力計）以『旋緊至吹不開，回退 1/4 圈』為第一週起始點，後續每週調升 1/4 圈。\n"
    "• 1/4 圈增幅基準：EMST 150 每 1/4 圈約增加 6 cmH2O；EMST 75 Lite 每 1/4 圈約增加 4 cmH2O。\n"
    "• 維持期（Maintenance）：密集訓練 4~5 週後，去適應（De-training）約 7~8 週發生。維持期每週僅需訓練 1~3 天（每天 25 次），即可長期鎖定肌力增長。",
    "臨床核心實務速記")

# Section 2: Neuroplasticity & Muscle Remodeling
add_custom_heading(doc, "二、 神經可塑性十大原則與呼吸肌重塑機制", 1)
add_body_p(doc, "呼吸肌力量訓練之所以能產生迅速且持久的臨床效益，核心在於同時驅動了『中樞神經系統重塑』與『周邊骨骼肌肥大』。研習將神經復健經典的十大原則（Kleim & Jones, 2008）具體實踐於 RMST：")

# Table 1: 10 Principles of Neuroplasticity
np_table = doc.add_table(rows=6, cols=3)
np_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(np_table)
np_headers = ["神經可塑性原則 (Principle)", "神經生理學意涵", "RMST 臨床具體實踐方式"]
for i, h in enumerate(np_headers):
    cell = np_table.cell(0, i)
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

np_rows = [
    ("1. 用之則進 / 不用則退\n(Use It and Improve It)", "未使用的神經迴路會退化；針對性訓練能驅動神經突觸生長與皮質重組。", "及早介入帕金森氏症或中風患者，防止呼吸幫浦廢用性萎縮並強化神經突觸新生。"),
    ("2. 特異性 (Specificity)", "訓練性質決定了神經可塑性與肌肉纖維轉變的特異方向。", "欲增強咳嗽力與喉上提需給予呼氣肌超負荷（EMST）；欲增強通氣與脫機需吸氣肌負荷（IMST）。"),
    ("3. 強度關鍵 (Intensity Matters)", "足夠的生理刺激強度是誘導運動單元徵召與皮質改變的前提。", "常規設定於 75%~80% MEP/MIP；神經退化症（如 ALS）設定於 30%~50% 避免過勞。"),
    ("4. 重複次數 (Repetition Matters)", "足夠的重複次數才能鞏固神經可塑性並轉化為長期記憶。", "5×5 協定（每天 25 次、每週 5 天、共 4~5 週）提供充足重複刺激。"),
    ("5. 遷移性 (Transference)", "單一技能的訓練可促進相關神經功能或相鄰肌群的表現。", "EMST 訓練呼氣肌同時活化舌骨上肌群，遷移並改善吞嚥咽期驅動力與發聲強度。")
]

for row_idx, row in enumerate(np_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = np_table.cell(row_idx, col_idx)
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

add_body_p(doc, "肌肉生理重塑階梯：訓練第 1 週即可觀察到顯著進步，主要來自『神經運動單元徵召增加（Motor Unit Recruitment）』與神經傳導速度提升；持續 4~6 週後，則轉變為實質的『肌纖維橫截面積增大（骨骼肌肥大 Hypertrophy）』與粒線體/肌球蛋白重構。")

# Section 3: Maintenance & De-training
add_custom_heading(doc, "三、 維持期訓練協定與去適應效應 (Maintenance & De-training)", 1)
add_body_p(doc, "臨床研究指出，密集訓練 4~5 週後，呼吸肌力可維持數週，去適應（De-training）效應約在停止訓練後第 7~8 週顯現。為長期維持療效，需制定合理的維持期計畫：")

# Table 2: Maintenance Protocol
maint_table = doc.add_table(rows=4, cols=3)
maint_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(maint_table)
maint_headers = ["訓練階段", "科學實證處方 (Evidence-based)", "臨床實務與動機考量 (Behavioral/MI)"]
for i, h in enumerate(maint_headers):
    cell = maint_table.cell(0, i)
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

maint_rows = [
    ("密集主動期 (Weeks 1-5)", "每週 5 天，每天 5 組 × 5 次 (共 25 次)，設定 75% MEP。", "建立每日固定訓練習慣（如晨間服藥後或特定作息配合）。"),
    ("維持期 (Maintenance)", "每週 1 至 3 天，每天維持 5 組 × 5 次 (共 25 次)。", "若患者容易遺忘，建議設定固定每週 3 天（如一三五），避免完全中斷。"),
    ("急性住院中斷處置", "若因急性共病住院中斷 2~3 週，無需過度焦慮肌力歸零。", "出院後由原先設定或調降 1/4 圈重新啟動，患者肌力記憶能迅速恢復。")
]

for row_idx, row in enumerate(maint_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = maint_table.cell(row_idx, col_idx)
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

# Section 4: Manometry vs Quarter-Turn
add_custom_heading(doc, "四、 臨床壓力評估與阻力校準實戰 (高科技 vs. 低科技法)", 1)
add_body_p(doc, "在評估患者最大呼氣壓（MEP）或最大吸氣壓（MIP）並設定訓練器材時，研習詳細對比了兩種臨床路徑：")

add_body_p(doc, "1. 高科技路徑（數位壓力計 Manometer 測量法）：", "A. 數位壓力計計算流程：")
add_body_p(doc, "• 佩戴鼻夾，讓患者全力最大呼氣/吸氣連續 3 次，記錄數值取平均值，再乘以 0.75（75% 目標強度）。")
add_body_p(doc, "• 實例演練一（健康專業用聲者）：三次呼氣壓為 112、99、122 cmH2O $\rightarrow$ 平均值 111 cmH2O $\rightarrow 111 \times 0.75 = 83.25\text{ cmH}_2\text{O} \rightarrow$ 選用 EMST 150。")
add_body_p(doc, "• 實例演練二（62 歲帕金森氏症早期）：三次呼氣壓為 84、80、76 cmH2O $\rightarrow$ 平均值 80 cmH2O $\rightarrow 80 \times 0.75 = 60\text{ cmH}_2\text{O} \rightarrow$ 選用 EMST 150 或 75 Lite。")
add_body_p(doc, "• 實例演練三（吸氣肌 MIP 測量）：三次吸氣壓為 -195、-218、-180 cmH2O $\rightarrow$ 平均值 -197 cmH2O $\rightarrow 197 \times 0.75 = 148\text{ cmH}_2\text{O} \rightarrow$ 選用 IA 150 吸氣適配器 + EMST 150。")

add_body_p(doc, "2. 低科技路徑（無壓力計之 1/4 圈校準法 Quarter-Turn Rule）：", "B. 臨床無壓力計時的精準替代方案：")
add_body_p(doc, "• 機構無壓力計時，治療師將旋鈕自最低阻力逐步旋緊，每次請患者短促用力吹氣，直到『閥門無法被吹開』為止。")
add_body_p(doc, "• 將旋鈕往回退 1/4 圈（最後一次能成功吹開之刻度），即為該患者第 1 週之最佳訓練起始設定。")
add_body_p(doc, "• 每週門診複查時，依據患者適應狀況向上調升 1/4 圈（Progression）。")

# Insert Diagram 1
if os.path.exists(CHART1_PATH):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    doc.add_picture(CHART1_PATH, width=Inches(6.0))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    rc = p_cap.add_run("圖 1：EMST 150 與 EMST 75 Lite 之 1/4 圈旋鈕刻度壓力遞增模型圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

# Table 3: Device Scale Reference
scale_table = doc.add_table(rows=3, cols=4)
scale_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(scale_table)
scale_headers = ["設備型號", "壓力總範圍", "每 1/4 圈 (Quarter Turn) 壓力增幅", "臨床病歷紀錄與適用對象"]
for i, h in enumerate(scale_headers):
    cell = scale_table.cell(0, i)
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

scale_rows = [
    ("EMST 150\n(標準型)", "30 ~ 150 cmH2O", "約 6 cmH2O / 1/4圈\n(1全圈約 24~30 cmH2O)", "紀錄方式：30 cmH2O (起點) -> 36 -> 42 -> 48 cmH2O。\n適用：中風、帕金森早期、發聲障礙、運動員及一般成人。"),
    ("EMST 75 Lite\n(輕量型)", "5 ~ 75 cmH2O", "約 4 cmH2O / 1/4圈\n(1全圈約 16~20 cmH2O)", "紀錄方式：5 cmH2O (起點) -> 9 -> 13 -> 17 cmH2O。\n適用：ALS/重症肌無力、小兒神經疾病、嚴重虛弱及老年患者。")
]

for row_idx, row in enumerate(scale_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = scale_table.cell(row_idx, col_idx)
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

# Section 5: Hands-on Techniques & Troubleshooting
add_custom_heading(doc, "五、 臨床操作細節、常見錯誤與故障排除 (Troubleshooting)", 1)
add_body_p(doc, "臨床執行時，患者常因代償或操作不當削弱訓練效果，治療師應落實以下指導細節：")

# Table 4: Clinical Techniques
tech_table = doc.add_table(rows=7, cols=3)
tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tech_table)
tech_headers = ["操作環節", "常見臨床錯誤 / 代償動作", "標準指導語與矯正手法"]
for i, h in enumerate(tech_headers):
    cell = tech_table.cell(0, i)
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

tech_rows = [
    ("吹氣動力模式", "緩慢、綿長地吐氣（如同吹氣球），導致無法產生足夠等長峰值壓力突破閥門。", "【吹熄生日蠟燭法】：吸飽氣後，短促、強力、爆發性地猛力一吹（Short & fast blast!）。"),
    ("臉頰固定 (Cheeks)", "吹氣時雙頰鼓起（Cheek puffing），壓力被頰部軟組織吸收而無法傳遞至喉部。", "雙手扶住臉頰或治療師協助加壓，維持頰肌緊繃，確保所有壓力導向設備。"),
    ("鼻夾使用 (Nose Clip)", "未使用鼻夾，氣流從鼻腔軟顎漏出（Velopharyngeal Insufficiency, VPI）。", "神經疾病與老年患者一律配戴鼻夾（向上夾住鼻翼），杜絕鼻部漏氣。"),
    ("口唇密封 (Lip Seal)", "口角無力漏氣，或患者習慣用力咬住吹嘴（Biting）。", "換用扁平舒適型吹嘴（Comfort Mouthpiece），提醒『用唇包覆，不要用牙齒咬』。"),
    ("姿勢調節 (Posture)", "帕金森氏症常見駝背低頭（Kyphosis），壓迫胸廓與橫膈下移空間。", "調整為端坐、胸廓挺直、雙肩向後向下放鬆，維持氣道通暢直線。"),
    ("設備清潔消毒", "使用滾燙熱水、洗碗機或漂白水消毒，導致內部精密彈簧與塑膠閥門變形損壞。", "僅使用常溫/微溫洗碗精肥皂水浸泡晃動 15-30 秒，清水沖淨後甩乾自然風乾。")
]

for row_idx, row in enumerate(tech_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = tech_table.cell(row_idx, col_idx)
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

# Section 6: Dysphagia & sEMG Mechanism
add_custom_heading(doc, "六、 吞嚥障礙（Dysphagia）的生理學深層機制與咽期運動學", 1)
add_body_p(doc, "EMST 對吞嚥障礙的改善並非間接效應，而是直接透過神經肌肉共享機制強化了咽期關鍵構造：")

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
    rc = p_cap.add_run("圖 2：EMST 訓練時舌骨上肌群（sEMG）活化時間與 Troche et al. 喉部運動學改善對比圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

add_body_p(doc, "1. 舌骨上肌群（Suprahyoid Muscles）活化：", "A. 表面肌電圖 (sEMG) 實證：")
add_body_p(doc, "• 研究顯示，吹入 EMST 時，頦舌骨肌（Geniohyoid）、下頜舌骨肌（Mylohyoid）及二腹肌前腹（Anterior Digastric）之 sEMG 振幅與持續時間，顯著高於一般乾吞嚥與水吞嚥（活化時間自 0.9 秒延長至 2.3 秒以上）。")

add_body_p(doc, "2. 喉部結構拉提與食道括約肌開啟（Troche et al. 2008 研究）：", "B. 電視螢光吞嚥攝影 (VFSS) 運動學證據：")
add_body_p(doc, "• 舌骨前向上向位移（Hyoid Displacement）：顯著增加喉部上提幅度，促使會厭軟骨充分翻轉覆蓋氣道。")
add_body_p(doc, "• 食道上括約肌（UES / PES）開啟：喉部上提增加牽引力，擴大 UES 最大開啟寬度，大幅減少梨狀窩（Pyriform sinus）與會厭谷（Valleculae）食物殘留。")
add_body_p(doc, "• 滲漏/誤吸評分（PAS Score）：顯著降低誤吸等級，提升由口進食之安全性。")

# Section 7: Voluntary Cough & Aspiration Prediction
add_custom_heading(doc, "七、 自發性咳嗽生理力學與誤吸預測模型 (Plowman et al. 研究)", 1)
add_body_p(doc, "『咳嗽與吞嚥是一體兩面（Hand in Hand）』。當患者吞嚥出現誤吸時，咳嗽是清除氣道異物的最後一道防線。自發性咳嗽（Voluntary Cough）包含三大相：吸氣相 $\rightarrow$ 壓迫相（聲門閉合） $\rightarrow$ 爆發性呼氣相。")

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
    rc = p_cap.add_run("圖 3：正常咳嗽波形與神經退化/誤吸高風險咳嗽波形動力學對比圖")
    rc.font.size = Pt(9)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED
    rc.font.name = "Microsoft JhengHei"

# Table 5: Cough Parameters
cough_table = doc.add_table(rows=4, cols=3)
cough_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(cough_table)
cough_headers = ["咳嗽動力學參數", "正常參考範圍", "臨床病理意義與誤吸風險預測"]
for i, h in enumerate(cough_headers):
    cell = cough_table.cell(0, i)
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

cough_rows = [
    ("呼氣峰值流速\n(Peak Cough Flow, PCF)", "> 300 ~ 500 L/min\n(低於 130~160 L/min 異常)", "PCF 低於 130 L/min 時定義為咳嗽無效（Dystussia），高度預測氣道分泌物無法咳出與吸入性肺炎。"),
    ("咳嗽容積加速\n(Cough Volume Acceleration, CVA)", "高斜率快速上升\n(迅速釋放氣流衝擊波)", "Plowman et al. (2017) 證實 ALS 患者中，CVA 降低與呼氣峰值上升時間延長能精準預測吞嚥誤吸風險。"),
    ("最大呼氣壓 (MEP)", "> 100 ~ 150 cmH2O", "呼氣肌肉力量的核心指標。EMST 訓練直接提升 MEP，帶動 PCF 與 CVA 之全面恢復。")
]

for row_idx, row in enumerate(cough_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = cough_table.cell(row_idx, col_idx)
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

# Section 8: Disease-Specific Protocols
add_custom_heading(doc, "八、 各類特殊疾病族群處方決策與臨床案例解析", 1)

# Table 6: Disease Specific Guidelines
dis_table = doc.add_table(rows=7, cols=4)
dis_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(dis_table)
dis_headers = ["臨床疾病族群", "推薦設備型號", "訓練強度與處方劑量", "關鍵考量與臨床決策重點"]
for i, h in enumerate(dis_headers):
    cell = dis_table.cell(0, i)
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

dis_rows = [
    ("肌萎縮側索硬化症 (ALS)\n[漸凍症 - 輕中度早期]", "EMST 75 Lite\n(必要時加 IA 75)", "【低負荷】30% ~ 50% MEP/MIP\n組間延長休息，可分次執行", "目標在活化維持現存運動單元，嚴禁超量高強度訓練以防氧化壓力（Oxidative Stress）加速運動神經元死亡。"),
    ("帕金森氏症 (PD)\n[早期至中晚期]", "EMST 150\n(晚期改 75 Lite)", "【標準超負荷】75% MEP\n5×5×5 協定，每週 5 天", "早期即應預防性介入（即使患者主訴未嗆咳）；維持排痰咳嗽力與說話響度，延緩晚期吞嚥惡化。"),
    ("痙攣性發聲障礙 (SD)\nvs. 肌張力性發聲 (MTD)", "先轉診喉科確診\n(肉毒注射後輔助)", "視個案評估調整", "【研習個案】：32 歲男性 DJ 誤診為 MTD，發聲治療無效且 MEP 僅 72 cmH2O，經複查確診為內收型痙攣性發聲障礙。"),
    ("頭頸癌皮瓣重建術後\n(Free Flap / 咽成形)", "EMST 150 / 75 Lite", "經外科醫師評估皮瓣完全癒合\n(通常術後數週至數月)", "必須先取得外科醫師核准（避免高口咽壓造成皮瓣吻合處裂開 Dehiscence）；改善放療後纖維化。"),
    ("心臟胸骨切開術後\n(Cardiac Surgery)", "IMST 優先 (IA 150)\n(暫緩高阻力呼氣)", "低至中強度吸氣訓練", "嚴格遵守胸骨保護原則（Sternal Precautions），吸氣肌訓練可促進肺擴張並改善心肺耐力。"),
    ("小兒神經復健族群\n(Pediatrics, 5~21 歲)", "EMST 75 Lite\n(口形配合小吹嘴)", "個別化評估配合度", "適用於腦性麻痺、小兒中風與腦腫瘤術後；以遊戲化引導短促有力吹氣。")
]

for row_idx, row in enumerate(dis_rows, start=1):
    bg_color = HEX_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row):
        cell = dis_table.cell(row_idx, col_idx)
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

# Section 9: Comprehensive Summary
add_custom_heading(doc, "九、 研習重點總結與臨床實踐指引", 1)
add_body_p(doc, "1. 呼吸肌力量訓練（RMST）具備深厚的神經與骨骼肌生理學基礎，是語言治療與心肺復健的核心實證工具。")
add_body_p(doc, "2. 評估時善用數位壓力計（或低科技 1/4 圈刻度回退法），能精準為病患量身設定 75% MEP/MIP 起始閾值。")
add_body_p(doc, "3. 5×5×5 標準訓練協定結合正確操作手法（戴鼻夾、扶雙頰、短促爆發吹氣），可在 4 週內顯著提升吞嚥喉上提、食道上括約肌開啟、咳嗽排痰力與發聲響度。")
add_body_p(doc, "4. 針對 ALS、帕金森氏症、中風與頭頸癌病患，給予疾病特異性的劑量調控，能最大化功能獨立性並預防吸入性肺炎等致死性併發症。")

# Save document
doc.save(DOCX_PATH)
print(f"Part 2 Word Document successfully created at: {DOCX_PATH}")
