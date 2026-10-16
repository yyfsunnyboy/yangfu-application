"""Create the four-panel interview booklet and an imposed A3 print file."""
from pathlib import Path
import fitz

ROOT = Path(__file__).parent
SRC = ROOT / '陽甫調整' / '其他表現資料'
ASSETS = ROOT / '陽甫調整' / '4頁對折本_assets'
OUT = ROOT / 'output' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)
FONT_PATH = r'C:\Windows\Fonts\NotoSansTC-VF.ttf'
FONT = fitz.Font(fontfile=FONT_PATH)
W, H = 595, 842

def rgb(code): return tuple(int(code[i:i+2], 16) / 255 for i in (1, 3, 5))
NAVY = rgb('#10243E'); INK = rgb('#10243E'); BLUE = rgb('#1659B7')
TEAL = rgb('#008F93'); ORANGE = rgb('#ED6B32'); GOLD = ORANGE
MINT = rgb('#B9E7DA'); PALE = rgb('#E4EFF8'); GRAY = rgb('#36546A')
LINE = rgb('#6C98A8'); WHITE = (1, 1, 1)

def box(p, x, y, w, h, fill, stroke=None, radius=0):
    shape=p.new_shape()
    r=fitz.Rect(x,y,x+w,y+h)
    if radius: shape.draw_rect(r)
    else: shape.draw_rect(r)
    shape.finish(fill=fill,color=stroke)
    shape.commit()

def rule(p,x1,y1,x2,y2,color=LINE,width=1): p.draw_line((x1,y1),(x2,y2),color=color,width=width)
def t(p,x,y,s,size=11,color=INK):
    p.insert_text((x,y),s,fontfile=FONT_PATH,fontname='NotoTC',fontsize=size,color=color)
def wrap(p,x,y,s,width,size=11,leading=18,color=INK):
    line=''
    for ch in s:
        if FONT.text_length(line+ch,size)>width:
            t(p,x,y,line,size,color); y+=leading; line=ch
        else: line+=ch
    if line: t(p,x,y,line,size,color); y+=leading
    return y
def pill(p,x,y,w,label,accent=TEAL):
    box(p,x,y,w,32,accent)
    t(p,x+13,y+21,label,10.3,WHITE)

def header(p,num,kicker,title,subtitle):
    box(p,0,0,W,94,NAVY)
    box(p,0,0,11,94,ORANGE)
    box(p,496,0,99,11,TEAL)
    t(p,40,28,f'{num}  /  {kicker}',10,rgb('#4EE0D6'))
    t(p,40,61,title,23,WHITE)
    t(p,40,81,subtitle,9.2,rgb('#DCE9F0'))

def footer(p,num):
    box(p,0,791,W,51,NAVY)
    box(p,0,791,W,4,ORANGE)
    t(p,40,823,'葉陽甫  ·  國立花蓮高級中學  ·  面試四面小冊',8,WHITE)
    t(p,523,823,f'{num} / 4',8,WHITE)

def image_clip(dest, source, source_page, clip, rect):
    dest.show_pdf_page(fitz.Rect(*rect),source,source_page,clip=fitz.Rect(*clip))

def image_file(dest, filename, rect):
    dest.insert_image(fitz.Rect(*rect),filename=str(ASSETS/filename),keep_proportion=True)

cover=fitz.open(SRC/'00_葉陽甫備審資料首頁.pdf')
sys=fitz.open(SRC/'09_AI自適應輔助學習系統介紹.pdf')
research=fitz.open(SRC/'08_研究介紹.pdf')
football=fitz.open(SRC/'03_高中足球_精華單頁版.pdf')
english=fitz.open(SRC/'英文能力.pdf')
book=fitz.open(); book.insert_pdf(cover)

# 2: one system, from classroom need to deployed practice.
p=book.new_page(width=W,height=H)
header(p,'02','系統實作','讓數學練習真正進入課堂','AI 自適應輔助學習系統  /  從教師需求到正式部署')
pill(p,40,107,250,'扶輪盃  ·  全國冠軍 / AI 應用競賽')
pill(p,300,107,255,'育秀盃  ·  AI 應用類全國金獎',GOLD)
t(p,40,169,'一位老師的問題，變成兩個班級使用的系統。',16.2,NAVY)
box(p,40,177,82,4,ORANGE)
wrap(p,40,193,'父親是技術型高中數學老師。教材如何匯入、題目如何持續變化、AI 產題如何驗證，都是從課堂回饋逐步拆出的工程問題。我負責把教材、出題、判題、提示與學習紀錄接成正式系統。',510,10.7,16)
t(p,40,257,'從教材到學生練習',12.5,TEAL)
for x,num,title,desc in [
    (40,'01','教材結構化','保留冊／章／節／技能'),
    (215,'02','程式化出題','AI 產生可重複出題程式'),
    (390,'03','練習與補救','判題、提示與學習紀錄')]:
    color={40:BLUE,215:TEAL,390:ORANGE}[x]
    box(p,x,272,165,62,color)
    t(p,x+12,294,num,12,WHITE); t(p,x+43,294,title,11.2,WHITE)
    t(p,x+12,317,desc,8.5,WHITE)
rule(p,205,303,215,303,NAVY,2); rule(p,380,303,390,303,NAVY,2)
t(p,40,357,'正式系統：教師首頁 × 學習分析',12.5,TEAL)
image_file(p,'ai_p1_img1.png',(40,369,291,548))
image_file(p,'ai_p7_img1.png',(304,369,555,548))
rule(p,297,369,297,548,ORANGE,2)
t(p,40,571,'我做的工程工作',12.2,TEAL)
rule(p,40,580,555,580,ORANGE,2)
t(p,40,601,'教材與出題',10.8,NAVY)
wrap(p,40,620,'匯入 B1～B4 教材；由 AI 建立 Python 出題程式，經隔離執行、試跑、答案檢查、回歸測試與人工驗收才發布。',238,9.3,15)
t(p,302,601,'練習與部署',10.8,NAVY)
wrap(p,302,620,'整合數學等價判題、手寫畫布、AI 助教、學習紀錄與部分單元的規則式補救；負責前後端、資料庫及正式主機維護。',252,9.3,15)
t(p,40,674,'目前已有真實課堂使用紀錄；學習成效仍需前後測與對照設計驗證。',8.8,GRAY)
box(p,40,686,515,57,NAVY)
box(p,40,686,8,57,ORANGE)
t(p,56,712,'2 班',15,WHITE); t(p,149,712,'50 人',15,WHITE)
t(p,255,712,'1,224 次',15,WHITE); t(p,392,712,'67%',15,WHITE)
t(p,56,730,'正式上線',8,rgb('#C9DDDE')); t(p,149,730,'真實學生',8,rgb('#C9DDDE'))
t(p,255,730,'實際作答',8,rgb('#C9DDDE')); t(p,392,730,'平均答對率',8,rgb('#C9DDDE'))
box(p,40,750,515,34,ORANGE)
t(p,52,772,'系統遇到的難題：AI 生成的出題程式，怎麼證明可靠？  →',10.8,WHITE)
footer(p,'2')
p.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(40,369,555,548),'uri':'https://mathb.math-adaptive.org/review-demo'})

# 3: a research question extracted from the engineering system.
p=book.new_page(width=W,height=H)
header(p,'03','從系統抽出研究','AI 產生的程式，能安全修好多少？','AST Active Healer  /  程式生成可靠性研究')
pill(p,40,107,250,'東區科展  ·  優等第 2 名')
pill(p,300,107,255,'旺宏科學獎  ·  全國決賽 20 強',GOLD)
box(p,40,153,515,92,NAVY)
box(p,40,153,8,92,ORANGE)
t(p,55,177,'系統中的具體困難',10.5,rgb('#4EE0D6'))
wrap(p,55,201,'為降低正式系統的雲端生成成本，我嘗試讓本地小模型建立出題程式；卻反覆遇到格式、介面、程式結構與資料流錯誤。研究因此聚焦：哪些錯誤能以固定規則安全修復？',480,10.4,16,WHITE)
t(p,40,269,'從工程問題拆出的兩個方法',12.8,TEAL)
rule(p,40,281,555,281,ORANGE,2)
box(p,40,294,245,87,BLUE)
box(p,302,294,253,87,TEAL)
t(p,52,318,'01  生成前：Scaffolding',11.4,WHITE)
wrap(p,52,340,'提供題型規格與 Domain Functions，減少模型自行規劃工具、參數與解題流程的負擔。',221,9.4,15,WHITE)
t(p,314,318,'02  生成後：Active Healer',11.4,WHITE)
wrap(p,314,340,'用 AST 與固定規則定位局部錯誤；只有修法可唯一判定時才修改，不讀正確答案。',228,9.4,15,WHITE)
box(p,40,397,515,137,PALE)
box(p,40,397,8,137,ORANGE)
t(p,55,423,'從初版 97.41 分，走向獨立驗證',12,NAVY)
wrap(p,55,448,'初版使用自建 MCRI 指標；旺宏評審追問原創貢獻、獨立驗證與公平比較後，我改用 Math16 題庫。3 模型 × 4 提示條件 × 5 固定種子，4 題開發規則、12 題保留正式測試；正式測試前凍結 Prompt 與 Healer。',480,10.1,16)
t(p,55,515,'判定方式：原始失敗 → 固定規則修復 → 使用相同測試重新評估。',9.3,TEAL)
t(p,40,562,'正式測試：720 個單元的逐筆追蹤',12.8,TEAL)
for x,value,label in [(40,'720','測試單元'),(170,'342','原始失敗'),(300,'42','實際修改'),(430,'9','失敗轉通過')]:
    color={40:BLUE,170:NAVY,300:TEAL,430:ORANGE}[x]
    box(p,x,581,125,72,color)
    t(p,x+12,612,value,21,WHITE)
    t(p,x+12,637,label,9,WHITE)
t(p,40,694,'2.63%',27,ORANGE)
t(p,148,687,'原始失敗救援率 ＝ 9 / 342',11.4,NAVY)
wrap(p,148,710,'9 個救回案例主要是介面、格式與資料流；144 個答案／演算法錯誤皆未救回。',404,10.1,16)
box(p,40,746,515,39,TEAL)
t(p,52,768,'研究收束：補足領域工具與流程資訊，再保守修復可確定的局部錯誤。',10.3,WHITE)
footer(p,'3')

# 4: clear upper and lower halves.
p=book.new_page(width=W,height=H)
header(p,'04','跨域能力','足球 × 英文','球場的長期投入  /  研究所需的英文能力')
t(p,40,133,'上半頁  /  足球',13.5,TEAL)
t(p,40,165,'連續兩年全國五人制聯賽決賽八強',16.5,NAVY)
image_file(p,'soccer_img1.jpeg',(40,185,297,357))
box(p,312,185,243,172,NAVY)
box(p,312,185,8,172,ORANGE)
t(p,328,216,'全國第 5 名',18,WHITE)
t(p,328,239,'114 學年度',9.5,rgb('#B6D9DF'))
rule(p,328,252,539,252,TEAL)
t(p,328,283,'全國第 6 名',18,WHITE)
t(p,328,306,'113 學年度',9.5,rgb('#B6D9DF'))
t(p,328,329,'114 年 57 隊  /  113 年 63 隊',8.9,WHITE)
t(p,328,347,'兩年皆正式主力  ·  背號 42',9.2,rgb('#4EE0D6'))
wrap(p,40,379,'國三擔任花崗國中足球隊隊長；高中連續兩年帶隊進入全國決賽八強。114 學年度以 5：3 擊敗惠文高中，取得全國第五。長期訓練讓我學會在壓力下溝通與執行。',515,10.2,16)
rule(p,40,446,555,446,ORANGE,3)
t(p,40,477,'下半頁  /  英文',13.5,TEAL)
t(p,40,508,'直接閱讀英文論文與技術資料',16.5,NAVY)
box(p,40,519,250,68,BLUE); box(p,300,519,255,68,TEAL)
t(p,53,547,'TOEIC  945 / 990',16.5,WHITE)
t(p,53,572,'聽力 485  /  閱讀 460',9.4,WHITE)
t(p,313,547,'GEPT  中高級四項通過',13,WHITE)
t(p,313,572,'聽 111  ·  讀 87  ·  說 80  ·  寫 80',8.6,WHITE)
image_file(p,'english_img1.jpeg',(40,596,290,714))
image_file(p,'english_img2.jpeg',(305,596,555,714))
box(p,40,717,515,67,TEAL)
t(p,52,741,'英文不只是考試成績，也是研究時使用的工具',10.8,WHITE)
wrap(p,52,761,'花蓮縣英文作文甲等；校內英語演說初賽第 1、複賽第 4；英文校排前 4%。研究中直接閱讀英文論文與技術資料。',488,9.1,14,WHITE)
footer(p,'4')

reading=OUT/'葉陽甫_面試四面小冊_A4閱讀版.pdf'
book.save(reading,garbage=4,deflate=True)

spread=fitz.open(); aw,ah=1191,842
for left,right in [(3,0),(1,2)]:
    page=spread.new_page(width=aw,height=ah)
    page.show_pdf_page(fitz.Rect(0,0,aw/2,ah),book,left)
    page.show_pdf_page(fitz.Rect(aw/2,0,aw,ah),book,right)
printable=OUT/'葉陽甫_面試四面小冊_A3雙面列印版.pdf'
spread.save(printable,garbage=4,deflate=True)
print(reading); print(printable)
