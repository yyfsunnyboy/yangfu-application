# 陽明交通大學申請資料來源對照表 (Source Map)

> **核心管理原則**：
> 1. **單一資料庫，多路徑引用**：原始證據、掃描證明、量化數據與母稿存放在既有頂層目錄，各系備審僅作語意改寫與精確路徑引用，嚴禁將同一 PDF 或素材實體拷貝到多個目錄。
> 2. **百川母稿與衍生版本之關係**：`03_nycu/01_baichuan` 保留完整的百川專用備審文件與自傳定稿母版；資工與電機版本在此基礎上，依學系專業特性進行完全獨立的重新敘事，絕不生搬硬套。

---

## 一、Repo 核心資源分布與引用指南

### 1. `01_master_profile/`（事實時間軸與核心規範）
- [01_facts_timeline.md](file:///d:/Python/yangfu-application/01_master_profile/01_facts_timeline.md)：國一至高三完整事實紀錄、時間節點、角色分工、學期成績、競賽名次之唯一客觀事實來源。
- [02_evidence_index.md](file:///d:/Python/yangfu-application/01_master_profile/02_evidence_index.md)：所有原始獎狀、證書、公文的檔案編號與個資遮蔽指引。
- [03_capability_matrix.md](file:///d:/Python/yangfu-application/01_master_profile/03_capability_matrix.md)：十三項能力維度檢核對照。
- [04_portfolio_materials.md](file:///d:/Python/yangfu-application/01_master_profile/04_portfolio_materials.md)：各校系素材適配建議（已包含 CS / EE / 百川等系所適配策略）。
- [05_interview_questions.md](file:///d:/Python/yangfu-application/01_master_profile/05_interview_questions.md)：技術追問與深層面試題庫（Healer 邊界、科展反思等）。
- [06_risk_checklist.md](file:///d:/Python/yangfu-application/01_master_profile/06_risk_checklist.md)：十大風控紅線檢核表。

---

### 2. `00_source_materials/`（原始實體證明與影音歸檔）
- `academic_records/`：高中教務處成績單、段考成績通知單、學測模考成績單、APCS 成績單。
- `awards/`：育秀盃金獎、神通 AI 第一名、東區科展優等、旺宏入圍證明、IEYI 銀獎等正式掃描檔。
- `language/`：GEPT 中高級證書/成績單、校內演講與作文獎狀。
- `sports/`：體育署中等學校五人制足球聯賽獎狀、秩序冊出賽證明。
- `research_competitions/`：東區科展說明書、旺宏研究報告作品原檔。
- `自主學習與學習歷程/`：FBref 爬蟲與足球分析報告、自主學習成果優等證明。
- `compiled_blocks/`：各類已彙整之單元區塊與圖表。

---

### 3. `02_research_project/`（技術專題與原始程式碼）
- 存放 AI 自適應學習系統架構圖、AST Healer 原始碼／測試腳本、基準測試資料庫與實驗日誌。

---

### 4. `03_nycu/01_baichuan/`（百川工作區——既有完整申請資料）
- [00_requirements.md](file:///d:/Python/yangfu-application/03_nycu/01_baichuan/00_requirements.md)：百川學士學位學程簡章提要。
- [01_evidence_inventory.md](file:///d:/Python/yangfu-application/03_nycu/01_baichuan/01_evidence_inventory.md)：百川第二層/第三層素材盤點表（T00～L01）。
- [03_application_form_data.md](file:///d:/Python/yangfu-application/03_nycu/01_baichuan/03_application_form_data.md)：報名表單數據彙整。
- [04_autobiography_1000.md](file:///d:/Python/yangfu-application/03_nycu/01_baichuan/04_autobiography_1000.md)：交大百川自傳 998 字定稿母版。
- [04_story_master.md](file:///d:/Python/yangfu-application/03_nycu/01_baichuan/04_story_master.md)：自傳與學習計畫完整故事母稿。

---

## 二、NYCU 各系所引用與敘事分流

| 申請組別 | 核心主軸 | 主要引用的 Repo 素材來源 | 敘事重構重點 |
| :--- | :--- | :--- | :--- |
| **01_baichuan（百川）** | 跨領域、自主規劃、長期教育科技專題、文武不岐 | • `03_nycu/01_baichuan/`<br>• `01_master_profile/`<br>• `00_source_materials/` | 保留百川成熟之 998 字自傳與第二層素材，圍繞「未解跨域研究課題」與「百川修課地圖」。 |
| **02_cs（資工）** | 軟體架構、程式可靠度、AST 解析、軟體工程與計算理論 | • `01_master_profile/` (S01, S02, S03)<br>• `02_research_project/`<br>• `00_source_materials/research_competitions/` | 聚焦在系統開發中遭遇的可靠度與架構挑戰，強調對資工正統演算法、編譯與系統理論之渴求。 |
| **03_ee（電機）** | 工程實現、軟硬體整合、感測控制、系統工程除錯思維 | • `01_master_profile/` (A02, S01, S02)<br>• `00_source_materials/自主學習與學習歷程/`<br>• `00_source_materials/compiled_blocks/` | 從 Arduino 實體控制與 AI 系統 IPO 架構切入，強調對底層硬體、訊號傳輸與工程控制之探究。 |
