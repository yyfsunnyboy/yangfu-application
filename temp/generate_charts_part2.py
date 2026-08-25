import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Set font for matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = r"C:\Projects\yangfu-application\temp"
CHART1_PATH = os.path.join(OUTPUT_DIR, "chart2_calibration_steps.png")
CHART2_PATH = os.path.join(OUTPUT_DIR, "chart2_cough_dynamics.png")
CHART3_PATH = os.path.join(OUTPUT_DIR, "chart2_swallow_hyoid.png")

# 1. Chart 1: Quarter-Turn Calibration Progression
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)
turns = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]) # Quarter turns (0 to 8 = 2 full turns)
emst150_pressures = 30 + turns * 6 # 30 cmH2O base + 6 per 1/4 turn
emst75_pressures = 5 + turns * 4   # 5 cmH2O base + 4 per 1/4 turn

ax.plot(turns, emst150_pressures, marker='o', linewidth=2.5, color='#1B365D', label='EMST 150 (每 1/4 圈約增加 6 cmH2O)')
ax.plot(turns, emst75_pressures, marker='s', linewidth=2.5, color='#E67E22', linestyle='--', label='EMST 75 Lite (每 1/4 圈約增加 4 cmH2O)')

for i, txt in enumerate(emst150_pressures):
    ax.annotate(f"{txt}", (turns[i], emst150_pressures[i]+1.5), fontsize=8.5, ha='center', color='#1B365D', fontweight='bold')
for i, txt in enumerate(emst75_pressures):
    ax.annotate(f"{txt}", (turns[i], emst75_pressures[i]-3), fontsize=8.5, ha='center', color='#E67E22', fontweight='bold')

ax.set_title("臨床無壓力計時之 1/4 圈旋鈕刻度校準模型 (Quarter-Turn Rule)", fontsize=11.5, fontweight='bold', pad=12)
ax.set_xlabel("旋鈕調整幅度 (每 1 格 = 1/4 圈 Quarter Turn)", fontsize=9.5)
ax.set_ylabel("估算壓力閾值 (cmH2O)", fontsize=9.5)
ax.set_xticks(turns)
ax.set_xticklabels(['起始點(0)', '1/4圈', '2/4圈', '3/4圈', '1全圈', '1又1/4', '1又2/4', '1又3/4', '2全圈'])
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig(CHART1_PATH)
plt.close()

# 2. Chart 2: Cough Flow Dynamics (Normal vs Impaired)
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)
time = np.linspace(0, 1.2, 500)
# Normal cough: rapid rise to 400 L/min, rapid compression and expulsion
normal_cough = np.zeros_like(time)
for i, t in enumerate(time):
    if t < 0.2: # inspiratory phase
        normal_cough[i] = -150 * np.sin(np.pi * t / 0.2)
    elif 0.2 <= t < 0.25: # compression phase (flow 0)
        normal_cough[i] = 0
    elif 0.25 <= t < 0.6: # expiratory blast
        normal_cough[i] = 450 * np.exp(-(t-0.25)*15)
    else:
        normal_cough[i] = 0

# Impaired cough (Dystussia): weak inspiratory, weak rise, low peak flow (120 L/min)
impaired_cough = np.zeros_like(time)
for i, t in enumerate(time):
    if t < 0.25: # weak inspiration
        impaired_cough[i] = -60 * np.sin(np.pi * t / 0.25)
    elif 0.25 <= t < 0.35: # sluggish compression
        impaired_cough[i] = 0
    elif 0.35 <= t < 0.9: # sluggish weak blast
        impaired_cough[i] = 110 * np.exp(-(t-0.35)*5)
    else:
        impaired_cough[i] = 0

ax.plot(time, normal_cough, color='#27AE60', linewidth=2.5, label='正常有效咳嗽 (Normal Cough, 峰值流速 > 300 L/min)')
ax.plot(time, impaired_cough, color='#C0392B', linewidth=2.5, linestyle='--', label='無效咳嗽/誤吸高風險 (Dystussia / Aspiration Risk < 130 L/min)')
ax.axhline(0, color='gray', linestyle=':', linewidth=1)

ax.text(0.35, 320, "正常衝擊波：\n• 快速容積加速 (CVA)\n• 高峰值呼氣流速 (PCF)\n• 有效清除氣道異物", 
        fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F8F5", edgecolor="#27AE60"))
ax.text(0.55, 140, "受損咳嗽波 (如 ALS / PD / 中風)：\n• CVA 上升遲緩、聲門閉合不良\n• 呼氣肌力弱，異物無法咳出", 
        fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", facecolor="#FDEDEC", edgecolor="#C0392B"))

ax.set_title("自發性咳嗽氣流動力學波形對比圖 (正常 vs. 咳嗽效能不全)", fontsize=11.5, fontweight='bold', pad=12)
ax.set_xlabel("時間 (秒)", fontsize=9.5)
ax.set_ylabel("氣流速率 (L/min)", fontsize=9.5)
ax.legend(loc='lower right', fontsize=8.5)
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(CHART2_PATH)
plt.close()

# 3. Chart 3: Swallow Hyoid Displacement & Muscle EMG Duration
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8), dpi=300)

# Bar chart of sEMG Duration
conditions = ['一般乾吞嚥\n(Dry Swallow)', '一般水吞嚥\n(Wet Swallow)', '用力吞嚥\n(Effortful Swallow)', 'EMST 吹氣訓練\n(EMST Loading)']
durations = [0.85, 0.92, 1.45, 2.30] # seconds
colors = ['#BDC3C7', '#3498DB', '#9B59B6', '#E74C3C']

bars = ax1.bar(conditions, durations, color=colors, width=0.55, edgecolor='black', linewidth=1)
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05, f'{yval}s', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
ax1.set_ylim(0, 2.8)
ax1.set_title("舌骨上肌群 (sEMG) 活化持續時間對比", fontsize=10, fontweight='bold')
ax1.set_ylabel("肌肉活化時間 (秒)", fontsize=9)
ax1.grid(axis='y', linestyle='--', alpha=0.6)

# Hyoid displacement comparison
categories = ['舌骨前向位移\n(Anterior)', '舌骨上向位移\n(Superior)', '食道上括約肌\n開啟寬度 (UES)']
sham_group = [6.2, 11.5, 7.8] # mm
emst_group = [9.8, 16.2, 12.4] # mm

x = np.arange(len(categories))
width = 0.35
ax2.bar(x - width/2, sham_group, width, label='對照組 (Sham)', color='#95A5A6', edgecolor='black')
ax2.bar(x + width/2, emst_group, width, label='EMST 訓練組', color='#2980B9', edgecolor='black')

ax2.set_ylabel("位移幅度 / 開啟度 (mm)", fontsize=9)
ax2.set_title("Troche et al. 吞嚥咽期喉部運動學改善", fontsize=10, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=8.5)
ax2.legend(loc='upper left', fontsize=8)
ax2.set_ylim(0, 20)
ax2.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig(CHART3_PATH)
plt.close()

print("Part 2 charts generated successfully.")
