# 📊 ebooks_ALLplatform — Data Query, Visualization & Auto-Reply System

## 📌 專案簡介

本專案為一個以 **Python + Streamlit 開發的資料查詢、統計分析與視覺化系統**，  
並整合 **簡易客服自動回覆模組（Q&A System）**，打造完整的內部營運與外部提案支援工具。

系統核心目標：

> 🔹 將原始資料 → 自動轉換為「可決策資訊」  
> 🔹 提供即時分析、視覺化與問答支援  
> 🔹 降低人工整理與溝通成本  

---

## 🌐 Demo & GitHub
- 🔗 Demo Video: https://sites.google.com/view/myweb-ersha/project/網站系統-web-system
- 🔗 Demo: https://ebooks-allplatform.streamlit.app/
- 🔗 GitHub: https://github.com/xiangtinglin/ebooks_ALLplatform

測試密碼：1234 / 6197

---

## 🧱 系統架構

```text
[ User ]
   │
   ▼
[ Streamlit Web App ]
   │
   ├── Authentication（密碼驗證）
   │
   ├── Data Module
   │     ├── Excel Upload
   │     ├── Data Cleaning (Pandas)
   │     ├── Cache (4 hrs)
   │
   ├── Analysis Engine
   │     ├── Aggregation
   │     ├── Filtering (Multi-condition)
   │     ├── KPI Computation
   │
   ├── Visualization Layer
   │     ├── Bar Charts
   │     ├── Pie Charts
   │     ├── Ranking Analysis
   │
   ├── Q&A Module（客服自動回覆）
   │     ├── Rule-based Response
   │     ├── FAQ Template
   │
   ▼
[ Output ]
   ├── Dashboard
   ├── CSV Export
   ├── Instant Insights
🚀 系統功能
1️⃣ 數據自動生成與分析
將 Excel 原始資料自動轉換為：
統計指標（KPI）
分群分析結果
排名與趨勢

👉 完全不需手動整理資料

2️⃣ 多條件查詢系統

支援：

合約簡編 / ISBN / 單位名稱
模糊搜尋 / 精確搜尋
年份篩選
銷售地區篩選
銷售單位篩選

👉 動態即時更新分析結果

3️⃣ 自動視覺化分析

自動生成圖表：

📊 歷年收益趨勢（Bar Chart）
🌍 海內 / 海外收益占比（Pie Chart）
🏆 銷售單位 Top 5
📚 出版年收益 Top 5

👉 可直接用於簡報 / 商業提案

4️⃣ KPI 即時統計

自動計算：

訂單數
銷售單位數
電子書收益總額
權利金總額
5️⃣ 報表輸出
支援 CSV 下載
可直接用於：
商業報告
簡報
決策分析
6️⃣ 🤖 客服自動回覆系統（Q&A Module）

📁 pages/【客服】_自動回覆Q&A.py

功能：

提供常見問題快速回覆（FAQ）
支援：
合作流程
上架問題
權利金問題
基本客服諮詢
Rule-based 回答機制（可擴展 NLP）

👉 降低人工客服成本
👉 提升回覆效率

🧑‍💻 Tech Stack
🔹 Application
Python
Streamlit
🔹 Data Processing
Pandas
OpenPyXL
🔹 Visualization
Matplotlib
Seaborn
Plotly
📂 專案結構
ebooks_ALLplatform/
│
├── app.py
├── requirements.txt
│
├── pages/
│   ├── 【權利金】歷年總表紀錄_分析圖表.py   # 核心分析系統
│   ├── 【總經銷】書單上架&分析圖表.py      # 書單管理分析
│   ├── 【客服】_自動回覆Q&A.py             # 客服自動回覆系統
│   └── files/
│       └── test_file.xlsx
⚙️ 安裝與執行（Coming soon）
git clone https://github.com/xiangtinglin/ebooks_ALLplatform.git
cd ebooks_ALLplatform

pip install -r requirements.txt
streamlit run app.py

👩‍💻 Author
SIANG-TING LIN（林湘婷）

NTNU CSIE Graduate Student
Machine Learning / Data Analysis / NLP

GitHub: https://github.com/xiangtinglin
