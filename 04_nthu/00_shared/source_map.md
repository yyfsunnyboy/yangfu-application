# 清華大學申請資料來源對照表 (Source Map)

> **核心管理原則**：
> 1. **單一資料庫，多路徑引用**：原始證據、掃描證明、量化數據與母稿存放在既有頂層目錄，各系備審僅作**語意改寫與精確路徑引用**，嚴禁將同一 PDF 或素材實體拷貝到多個目錄。
> 2. **獨立敘事，拒絕抄襲**：清大三個申請版本（CS / EE / IPTH）皆以各自學門邏輯重新構思自傳與計畫，**嚴禁直接複製百川申請敘事**。

---

## 一、Repo 現有核心資源分布與引用指南

### 1. `01_master_profile/`（事實時間軸與規範標準）
- [01_facts_timeline.md](file:///d:/Python/yangfu-application/01_master_profile/01_facts_timeline.md)：國一至高三完整事實紀錄、時間節點、角色分工、學期成績、競賽名次之**唯一客觀事實來源**。
- [02_evidence_index.md](file:///d:/Python/yangfu-application/01_master_profile/02_evidence_index.md)：所有原始獎狀、證書、公文的檔案編號與個資遮蔽指引。
- [03_capability_matrix.md](file:///d:/Python/yangfu-application/01_master_profile/03_capability_matrix.md)：十三項能力維度檢核對照。
- [04_portfolio_materials.md](file:///d:/Python/yangfu-application/01_master_profile/04_portfolio_materials.md)：各校系素材適配建議（已具備 CS / EE / 不分系之初步指引）。
- [05_interview_questions.md](file:///d:/Python/yangfu-application/01_master_profile/05_interview_questions.md)：技術追問與深層面試題庫（Healer 邊界、科展反思等）。
- [06_risk_checklist.md](file:///d:/Python/yangfu-application/01_master_profile/06_risk_checklist.md)：十大風控紅線，撰寫各系文稿前必須逐項對照。

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

### 4. `03_nycu/01_baichuan/`（百川工作區——僅供參照架構，不得直接複製內文）
- `01_evidence_inventory.md`：百川所建立的 T00～L01 素材分類表格範例。
- `03_application_form_data.md`：現成校對完畢之學歷、競賽、幹部數據格式。
- `04_story_master.md`：百川的故事母稿（注意：清大各系必須完全獨立改寫，不可沿用百川語句）。

---

## 二、清大各系與原始素材對應關係

| 清大申請模組 | 核心訴求與學術主軸 | 主要引用的 Repo 素材來源 | 敘事重構重點（與百川差異） |
| :--- | :--- | :--- | :--- |
| **01_cs（資工）** | 系統可靠性、軟體架構、AST 編譯解析、資料工程 | • `01_master_profile/` (S01, S02, S03)<br>• `02_research_project/`<br>• `00_source_materials/research_competitions/` | 擺脫「喜歡 AI」的表層敘事，聚焦在建構系統時面臨的**程式可靠度、邊界條件、軟體工程與計算基礎**。 |
| **02_ee（電機）** | 軟硬體整合、感測控制、工程除錯思維、計算底層 | • `01_master_profile/` (A02, S01, S02)<br>• `00_source_materials/自主學習與學習歷程/`<br>• `00_source_materials/compiled_blocks/` | 從 Arduino 實體控制與 AI 系統 IPO 架構出發，探究支撐大型智慧系統背後的**硬體、訊號、通訊與工程實踐**。 |
| **03_ipth（清華學院學士班 IPTH）** | 資訊/運動/外語三線並行、持續推進的教育科技實踐 | • `01_master_profile/` (P01, P02, L01, S01)<br>• `00_source_materials/sports/`<br>• `00_source_materials/language/` | 不寫成「因未決定方向而選不分系」，而是聚焦於**已有具體教育科技專案，需結合資訊、認知教育與社會場域進行跨域推進**。 |
