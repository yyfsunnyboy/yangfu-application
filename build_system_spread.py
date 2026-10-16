"""Build a continuous A3 interior spread from original system screenshots."""
from pathlib import Path
from PIL import Image
import fitz

ROOT = Path(__file__).parent
SCREENS = ROOT / '00_source_materials' / '照片' / '系統截圖'
OUT = ROOT / 'output' / 'gpt'
OUT.mkdir(parents=True, exist_ok=True)
APPROVED = ROOT / 'output' / 'pdf' / '葉陽甫_面試四面小冊_A3雙面列印版.pdf'
REG = r'C:\Windows\Fonts\NotoSansTC-VF.ttf'
BOLD = r'C:\Windows\Fonts\msjhbd.ttc'
REG_FONT, BOLD_FONT = fitz.Font(fontfile=REG), fitz.Font(fontfile=BOLD)
W, H = 1190.55, 841.89

def rgb(s): return tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))
NAVY, INK, TEAL = rgb('#102A43'), rgb('#17324A'), rgb('#007E80')
GREEN, ORANGE = rgb('#216D52'), rgb('#EB6B24')
CREAM, PALE = rgb('#FFF4DE'), rgb('#EFF7F3')
LINE, GRAY, WHITE = rgb('#B9D2CE'), rgb('#526A76'), (1, 1, 1)

def rect(p, x, y, w, h, fill, stroke=None, lw=1):
    p.draw_rect(fitz.Rect(x, y, x + w, y + h), color=stroke, fill=fill, width=lw)

def txt(p, x, y, value, size=10, color=INK, bold=False):
    p.insert_text((x, y), value, fontfile=BOLD if bold else REG,
                  fontname='BoldTC' if bold else 'NotoTC', fontsize=size, color=color)

def wrap(p, x, y, value, width, size=10, leading=15, color=INK, bold=False):
    font = BOLD_FONT if bold else REG_FONT
    row = ''
    for ch in value:
        if row and font.text_length(row + ch, size) > width:
            txt(p, x, y, row, size, color, bold); y += leading; row = ch
        else: row += ch
    if row: txt(p, x, y, row, size, color, bold); y += leading
    return y

def arrow(p, a, b, color=ORANGE, width=3):
    p.draw_line(a, b, color=color, width=width)
    x, y = b
    p.draw_polyline([(x - 7, y - 5), (x, y), (x - 7, y + 5)],
                    color=color, width=width)

def screenshot(p, filename, crop, box, caption, tag, accent=TEAL):
    """Crop a real screenshot without changing its UI."""
    x0, y0, x1, y1 = box
    rect(p, x0 - 2, y0 - 2, x1 - x0 + 4, y1 - y0 + 4, WHITE, NAVY, .8)
    view = Image.open(SCREENS / filename).convert('RGB').crop(crop)
    pix = fitz.Pixmap(fitz.csRGB, view.width, view.height, view.tobytes(), False)
    p.insert_image(fitz.Rect(x0, y0, x1, y1 - 27), pixmap=pix, keep_proportion=False)
    rect(p, x0, y1 - 27, x1 - x0, 27, NAVY)
    rect(p, x0, y1 - 27, 4, 27, accent)
    txt(p, x0 + 11, y1 - 9, caption, 9.2, WHITE, True)
    rect(p, x1 - 30, y1 - 27, 30, 27, accent)
    txt(p, x1 - 22, y1 - 9, tag, 10, WHITE, True)

doc = fitz.open()
p = doc.new_page(width=W, height=H)
rect(p, 0, 0, W, H, WHITE)
rect(p, 0, 0, W, 102, NAVY)
rect(p, 0, 0, 10, 102, ORANGE)
txt(p, 40, 28, 'SYSTEM  →  CLASSROOM  →  RESEARCH', 10, rgb('#7FE0D3'), True)
txt(p, 40, 66, '把數學老師的備課難題，做成學生每天能用的 AI 學習系統', 23, WHITE, True)
txt(p, 902, 28, '育秀盃金獎  ·  扶輪盃全國第一名', 9.4, WHITE, True)
rect(p, 0, 99, W, 4, TEAL)

txt(p, 40, 137, '從教師出發', 15, NAVY, True)
wrap(p, 40, 159, '父親是技術型高中數學老師。我將 Word／PDF 教材整理成章節與技能，建立程式化出題、數學判題與 AI 提示，再部署到正式課堂。', 500, 10, 15)
txt(p, 630, 137, '在真實課堂反覆驗證', 15, NAVY, True)
wrap(p, 630, 159, '兩班 50 位學生使用，累積 1,224 次作答，平均答對率 67%。系統記錄技能與錯誤，部分單元已有規則式自適應複習。', 520, 10, 15)
for x, num, label in [(40, '2', '正式使用班級'), (315, '50', '真實學生'),
                      (630, '1,224', '實際作答'), (945, '67%', '平均答對率')]:
    rect(p, x, 191, 205, 47, PALE, LINE, .7)
    rect(p, x, 191, 5, 47, TEAL)
    txt(p, x + 14, 222, num, 19, TEAL, True)
    txt(p, x + (92 if num in ('1,224', '67%') else 79), 220, label, 9, INK, True)

# Diagonal connective bands cross the fold behind the system views.
p.draw_polyline([(0, 272), (595, 332), (W, 275), (W, 343),
                 (595, 400), (0, 342)], closePath=True, color=None, fill=GREEN)
p.draw_polyline([(0, 540), (595, 490), (W, 543), (W, 612),
                 (595, 559), (0, 609)], closePath=True, color=None, fill=NAVY)
rect(p, 0, 255, W, 8, ORANGE)
txt(p, 40, 279, '教 師 端', 10, NAVY, True)
txt(p, 520, 279, '學 生 作 答  ×  AI 引 導', 10, NAVY, True)
txt(p, 1050, 279, '學 習 診 斷', 10, NAVY, True)

# The work-area / AI-tutor boundary of the central screen lands on the fold.
screenshot(p, '教師首頁04.png', (200, 130, 3000, 1700),
           (40, 304, 296, 443), '班級總覽  ·  2 班 50 人', '01')
screenshot(p, 'S05_教師4.png', (0, 0, 719, 475),
           (40, 462, 296, 601), 'Word／PDF 教材匯入', '02')
screenshot(p, '03學生作答畫面.jpg', (150, 188, 1416, 739),
           (314, 304, 877, 601), '學生手寫解題', '03', ORANGE)
txt(p, 627, 592, 'AI 逐步提示', 9.2, WHITE, True)
screenshot(p, 'S05_學生4.png', (0, 240, 894, 825),
           (895, 304, 1150, 443), '知識圖譜  ·  找出技能關聯', '04')
screenshot(p, '學生學習趨勢.jpg', (0, 195, 2053, 1450),
           (895, 462, 1150, 601), '技能分析  ·  找出學習卡點', '05')
for y in (374, 531):
    arrow(p, (297, y), (311, y))
    arrow(p, (879, y), (893, y))

rect(p, 40, 620, 1110, 47, CREAM, ORANGE, .8)
rect(p, 40, 620, 7, 47, ORANGE)
txt(p, 57, 640, '課堂系統遇到的瓶頸', 10.7, NAVY, True)
txt(p, 57, 657, '小模型生成的 Python 出題程式，仍可能有語法、介面與資料流錯誤。如何只修得動、修得安全？', 9.5, INK)
rect(p, 40, 681, 532, 111, PALE, LINE, .8)
rect(p, 40, 681, 6, 111, TEAL)
txt(p, 55, 704, '我完成的工程工作', 12.5, NAVY, True)
wrap(p, 55, 724, '教材匯入、前後端、GenCode 出題、判題、AI 整合、資料庫與 Docker 部署。出題程式經隔離執行、隨機試跑、答案檢查與人工驗收，才發布給學生。', 500, 9.2, 14)
txt(p, 55, 779, '2026-10-04 使用快照；學習成效仍待對照驗證。', 8.2, GRAY)
txt(p, 55, 763, '技術：Next.js  ·  FastAPI  ·  SymPy  ·  PostgreSQL  ·  Docker', 8.5, TEAL, True)
rect(p, 589, 681, 561, 111, NAVY)
rect(p, 589, 681, 6, 111, ORANGE)
txt(p, 606, 704, '由系統難題延伸：AST Active Healer 研究', 12.5, WHITE, True)
txt(p, 606, 724, '以語法樹與確定性規則，修復可驗證的局部程式錯誤。', 9.2, WHITE)
for x, val, label in [(608, '720', '正式測試'), (738, '342', '原始失敗'),
                      (868, '42', '實際修改'), (998, '9', '成功救回')]:
    rect(p, x, 735, 118, 43, WHITE)
    txt(p, x + 9, 759, val, 17, ORANGE if val == '9' else TEAL, True)
    txt(p, x + 53, 757, label, 8, INK)
txt(p, 606, 786, '安全救回 9/342 = 2.63%  ·  旺宏全國 20 強  ·  東區科展優等第 2 名', 8.3, rgb('#BCE8DE'), True)
rect(p, 0, 808, W, H - 808, NAVY)
txt(p, 40, 830, '葉陽甫  /  AI 自適應輔助學習系統與程式可靠性研究', 8.8, WHITE)
txt(p, 940, 830, 'A3 內頁跨頁  ·  對折後 A4', 8.4, WHITE)

spread = OUT / '葉陽甫_AI學習系統與研究_A3跨頁.pdf'
doc.save(spread, garbage=4, deflate=True)
old = fitz.open(APPROVED)
booklet = fitz.open()
booklet.insert_pdf(old, from_page=0, to_page=0)
booklet.insert_pdf(doc)
full = OUT / '葉陽甫_面試四面小冊_系統跨頁版_A3雙面列印.pdf'
booklet.save(full, garbage=4, deflate=True)
print(spread)
print(full)
