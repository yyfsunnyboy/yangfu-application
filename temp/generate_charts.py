import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Set font for matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = r"C:\Projects\yangfu-application\temp"
DOCX_PATH = os.path.join(OUTPUT_DIR, "呼吸肌力量訓練_RMST_專業研習完整臨床報告.docx")
CHART1_PATH = os.path.join(OUTPUT_DIR, "chart_physiology_cycle.png")
CHART2_PATH = os.path.join(OUTPUT_DIR, "chart_threshold_vs_resistive.png")
CHART3_PATH = os.path.join(OUTPUT_DIR, "chart_lung_volumes.png")

# 1. Generate Diagram 1: Respiratory Physiology Cycle (Pressure, Volume, Flow)
fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
time = np.linspace(0, 4, 400)
# Inspiration: 0 to 2s, Expiration: 2 to 4s
volume = 0.5 * (1 - np.cos(np.pi * time / 2)) # Tidal volume curve
palv = -2.5 * np.sin(np.pi * time / 2) # Alveolar pressure (- during insp, + during exp)
flow = np.sin(np.pi * time / 2) * 0.5 # Flow

ax.plot(time, volume, label="肺容積變化 Volume (L)", color="#1B365D", linewidth=2.5)
ax.plot(time, palv, label="肺泡內壓 Palv (cmH2O)", color="#C0392B", linewidth=2.5, linestyle="--")
ax.axhline(0, color="gray", linestyle=":", linewidth=1)
ax.axvline(2, color="gray", linestyle="-.", linewidth=1)

ax.text(0.8, 1.2, "【吸氣期 (Inspiration)】\n橫膈/肋間外肌收縮\n胸腔擴張 -> 形成負壓 -> 氣流吸入", 
        fontsize=9, bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", edgecolor="#2980B9"))
ax.text(2.3, 1.2, "【呼氣期 (Expiration)】\n肌肉放鬆/肺彈性回縮\n胸腔縮小 -> 形成正壓 -> 氣流呼出", 
        fontsize=9, bbox=dict(boxstyle="round,pad=0.5", facecolor="#FDEDEC", edgecolor="#C0392B"))

ax.set_title("呼吸生理學：吸氣與呼氣之容積與壓力動態關係圖", fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("時間 (秒) Time (s)", fontsize=10)
ax.set_ylabel("數值變化量", fontsize=10)
ax.legend(loc="lower left", frameon=True)
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(CHART1_PATH)
plt.close()

# 2. Generate Diagram 2: Pressure Threshold vs Resistive Loading
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4), dpi=300)

# Threshold device
ax1.plot([0, 1, 1, 3], [0, 60, 60, 0], color="#27AE60", linewidth=3, label="壓力 (Pressure)")
ax1.plot([0, 0.99, 1, 3], [0, 0, 40, 0], color="#2980B9", linewidth=2.5, linestyle="--", label="氣流 (Flow)")
ax1.axvline(1, color="red", linestyle=":", label="彈簧閥門開啟點 (Threshold)")
ax1.set_title("【壓力門檻式設備 (EMST/IMST)】\n(需先克服彈簧壓力，閥門才開啟)", fontsize=10, fontweight="bold")
ax1.set_xlabel("用力歷程 (時間)", fontsize=9)
ax1.set_ylabel("強度 / 數值", fontsize=9)
ax1.legend(loc="upper right", fontsize=8)
ax1.grid(True, linestyle="--", alpha=0.5)

# Resistive device
ax2.plot([0, 1.5, 3], [0, 40, 0], color="#E67E22", linewidth=3, label="壓力 (Pressure)")
ax2.plot([0, 1.5, 3], [0, 40, 0], color="#8E44AD", linewidth=2.5, linestyle="--", label="氣流 (Flow)")
ax2.set_title("【阻抗式設備 (Resistive Device)】\n(全程氣流洩漏，阻力隨流速改變)", fontsize=10, fontweight="bold")
ax2.set_xlabel("用力歷程 (時間)", fontsize=9)
ax2.set_ylabel("強度 / 數值", fontsize=9)
ax2.legend(loc="upper right", fontsize=8)
ax2.grid(True, linestyle="--", alpha=0.5)

plt.suptitle("壓力門檻式 (EMST 150/75) 與 阻抗式設備 運作原理對比", fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(CHART2_PATH)
plt.close()

# 3. Generate Diagram 3: Lung Volumes and Capacities
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=300)
categories = ['深吸氣量 (IC)', '潮氣容積 (VT)', '功能殘氣量 (FRC)', '肺活量 (VC)', '殘氣容積 (RV)', '總肺容量 (TLC)']
# Normalized proportions
# Let TLC = 6.0L, VC = 4.8L, RV = 1.2L, FRC = 2.4L, VT = 0.5L, IC = 3.6L
vol_values = [3.6, 0.5, 2.4, 4.8, 1.2, 6.0]
colors = ['#3498DB', '#1ABC9C', '#F39C12', '#2ECC71', '#E74C3C', '#34495E']

bars = ax.bar(categories, vol_values, color=colors, width=0.55, edgecolor='black', linewidth=1)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval} L', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylim(0, 7.2)
ax.set_title("成年人典型肺容量與容積分配參考模型 (典型值)", fontsize=12, fontweight="bold", pad=12)
ax.set_ylabel("容積 (公升, L)", fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=15, fontsize=9)
plt.tight_layout()
plt.savefig(CHART3_PATH)
plt.close()

print("Charts generated successfully.")
