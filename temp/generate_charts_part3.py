import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Set font for matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = r"C:\Projects\yangfu-application\temp"
CHART1_PATH = os.path.join(OUTPUT_DIR, "chart3_icu_decannulation_pathway.png")
CHART2_PATH = os.path.join(OUTPUT_DIR, "chart3_radiation_fibrosis.png")
CHART3_PATH = os.path.join(OUTPUT_DIR, "chart3_acdf_laryngectomy_progress.png")

# 1. Chart 1: ICU Tracheostomy & Weaning Assessment Flowchart
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
ax.axis('off')

# Draw hierarchical boxes
boxes = [
    (0.5, 0.90, "【第 1 階：生理與氣道評估】\n意識清醒配合、FiO2 <= 50%、PEEP <= 10、無未控制高血壓/氣胸", "#1B365D", "white"),
    (0.5, 0.70, "【第 2 階：氣管套管餘裕與氣囊評估】\n評估氣切管號數 (大號如 #8 評估降號 Downsizing) -> 氣囊完整放氣 (Cuff Deflated)", "#2980B9", "white"),
    (0.5, 0.50, "【第 3 階：單向說話閥 (PMV) 耐受測試】\n裝配 Passy-Muir Valve (在線 Inline 或氣切口) -> 監測呼氣通暢度與膚色表情", "#27AE60", "white"),
    (0.5, 0.30, "【第 4 階：啟動呼吸肌力量訓練 (RMST)】\n• 吸氣肌 (IMST / IA 150)：強化橫膈肌，加速呼吸器脫機\n• 呼氣肌 (EMST 75/150)：強化咳嗽排痰與吞嚥咽期驅動力", "#8E44AD", "white"),
    (0.5, 0.10, "【臨床終點：安全拔管 (Decannulation) 與出院】\n縮短氣切留置天數、減少呼吸器依賴、降低再插管率與吸入性肺炎", "#C0392B", "white")
]

for x, y, text, bg, fg in boxes:
    ax.text(x, y, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=fg,
            bbox=dict(boxstyle="round,pad=0.5", facecolor=bg, edgecolor='black', linewidth=1.2))

# Draw connecting arrows
for y_start, y_end in [(0.83, 0.77), (0.63, 0.57), (0.43, 0.37), (0.23, 0.17)]:
    ax.annotate('', xy=(0.5, y_end), xytext=(0.5, y_start),
                arrowprops=dict(facecolor='#34495E', shrink=0.05, width=2, headwidth=7))

ax.set_title("加護病房 (ICU) 氣切脫機、單向說話閥 (PMV) 與 RMST 整合決策路徑", fontsize=12, fontweight='bold', pad=10)
plt.tight_layout()
plt.savefig(CHART1_PATH)
plt.close()

# 2. Chart 2: Radiation-Induced Fibrosis Muscle Degradation Timeline
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=300)
years = np.array([0, 1, 2, 3, 4, 5])
# Normal elasticity vs. Fibrotic Tissue stiffness & Collagen deposition
collagen_deposition = np.array([10, 35, 60, 78, 88, 95]) # % fibrosis accumulation
mep_strength = np.array([120, 95, 80, 70, 65, 60])       # Untreated MEP baseline decline
mep_with_emst = np.array([120, 115, 110, 108, 105, 102])  # MEP with RMST intervention

ax.plot(years, collagen_deposition, color='#C0392B', marker='o', linewidth=2.5, label='組織纖維化 / 膠原蛋白沉積率 (%)')
ax.plot(years, mep_strength, color='#7F8C8D', marker='x', linestyle='--', linewidth=2, label='未接受 RMST 之呼氣肌力自然衰退 (cmH2O)')
ax.plot(years, mep_with_emst, color='#27AE60', marker='s', linewidth=2.5, label='規律介入 RMST 之呼氣肌力維持 (cmH2O)')

ax.set_title("頭頸癌放療後組織纖維化進程 (RIF) 與 RMST 長期保護效益", fontsize=11.5, fontweight='bold', pad=12)
ax.set_xlabel("放射線治療完成後年數 (Years Post-Radiation)", fontsize=9.5)
ax.set_ylabel("纖維化程度 (%) / 呼氣壓力 (cmH2O)", fontsize=9.5)
ax.set_ylim(0, 135)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='center right', fontsize=8.5)

ax.text(2.5, 30, "【放療纖維化病理】\n• 血管微內皮水腫壞死\n• 骨骼肌粒線體結構畸變\n• 需長療程 (8+週) RMST 抵抗僵硬", 
        fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF9E7", edgecolor="#F39C12"))

plt.tight_layout()
plt.savefig(CHART2_PATH)
plt.close()

# 3. Chart 3: Clinical Progress in ACDF & Laryngectomy Cases
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8), dpi=300)

# ACDF Patient MEP progression over 5 weeks
weeks = ['評估起點', '第 2 週', '第 4 週', '第 5 週 (結案)']
acdf_mep = [38, 58, 72, 80]
ax1.plot(weeks, acdf_mep, marker='o', color='#2980B9', linewidth=2.5)
for i, v in enumerate(acdf_mep):
    ax1.text(i, v + 2.5, f"{v} cmH2O", ha='center', fontsize=8.5, fontweight='bold', color='#1B365D')
ax1.set_ylim(25, 95)
ax1.set_title("61歲 ACDF 頸椎融合術後 EMST 壓力進階歷程", fontsize=9.5, fontweight='bold')
ax1.set_ylabel("訓練壓力設定 (cmH2O)", fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.6)

# Head & Neck / Laryngectomy outcomes
metrics = ['最大發聲時間 (MPT)', '呼氣峰值流速 (PCF)', '吞嚥殘留評分 (EAT-10)']
pre_vals = [6.5, 180, 26]
post_vals = [14.2, 340, 8]

x = np.arange(len(metrics))
width = 0.35
ax2.bar(x - width/2, pre_vals, width, label='介入前 (Pre)', color='#95A5A6', edgecolor='black')
ax2.bar(x + width/2, post_vals, width, label='EMST 8週後 (Post)', color='#27AE60', edgecolor='black')
ax2.set_title("頭頸癌/全喉切除術後臨床功能改善指標", fontsize=9.5, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(metrics, fontsize=8.5)
ax2.legend(loc='upper right', fontsize=8)
ax2.set_ylim(0, 400)
ax2.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig(CHART3_PATH)
plt.close()

print("Part 3 charts generated successfully.")
