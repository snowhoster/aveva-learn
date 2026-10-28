# AVEVA Marine 與二次開發課程

[← 學習中心首頁](../index.html)

給開發人員的完整課程：先建立系統與資料模型的概念，再理解船舶設計業務，最後進入二次開發技術。共 18 章與 2 個附錄。每份閱讀頁底部都有「上一篇／下一篇」導覽。

從 [第 0 章　課程總覽與知識地圖](ch00_knowledge_map_zh-TW.reading.html) 開始，裡面有各章知識點清單、12 週進度與能力等級。

## 課程章節

| 章 | 標題 | 原稿 |
|---|---|---|
| 0 | [課程總覽與知識地圖](ch00_knowledge_map_zh-TW.reading.html) | [md](ch00_knowledge_map_zh-TW.md) |
| **第一部分** | **系統與資料模型** | |
| 1 | [產品架構、模組與啟動環境](ch01_architecture_zh-TW.reading.html) | [md](ch01_architecture_zh-TW.md) |
| 2 | [專案、資料庫、MDB 與權限](ch02_project_database_zh-TW.reading.html) | [md](ch02_project_database_zh-TW.md) |
| 3 | [資料階層、元素、屬性與導覽](ch03_hierarchy_attributes_zh-TW.reading.html) | [md](ch03_hierarchy_attributes_zh-TW.md) |
| 4 | [座標、方向與幾何](ch04_coordinates_geometry_zh-TW.reading.html) | [md](ch04_coordinates_geometry_zh-TW.md) |
| **第二部分** | **船舶設計業務領域** | |
| 5 | [船體建模：曲面、板架與拓撲](ch05_hull_modelling_zh-TW.reading.html) | [md](ch05_hull_modelling_zh-TW.md) |
| 6 | [船體生產資訊、套料與裝配](ch06_hull_production_zh-TW.reading.html) | [md](ch06_hull_production_zh-TW.md) |
| 7 | [舾裝設計：設備、管路、結構、通風與電纜](ch07_outfitting_zh-TW.reading.html) | [md](ch07_outfitting_zh-TW.md) |
| 8 | [目錄與等級](ch08_catalogue_spec_zh-TW.reading.html) | [md](ch08_catalogue_spec_zh-TW.md) |
| 9 | [圖面、ISO 圖與報表輸出](ch09_drawings_zh-TW.reading.html) | [md](ch09_drawings_zh-TW.md) |
| **第三部分** | **二次開發技術** | |
| 10 | [開發環境：PMLLIB、檔案類型與部署結構](ch10_dev_environment_zh-TW.reading.html) | [md](ch10_dev_environment_zh-TW.md) |
| 11 | [PML 語言核心](ch11_pml_language_zh-TW.reading.html) | [md](ch11_pml_language_zh-TW.md) |
| 12 | [PML 資料庫操作](ch12_pml_database_zh-TW.reading.html) | [md](ch12_pml_database_zh-TW.md) |
| 13 | [PML2 表單、選單與 Add-in](ch13_pml_forms_addins_zh-TW.reading.html) | [md](ch13_pml_forms_addins_zh-TW.md) |
| 14 | [.NET 開發：PML.NET 與 CAF Add-in](ch14_dotnet_zh-TW.reading.html) | [md](ch14_dotnet_zh-TW.md) |
| 15 | [船體開發：Vitesse Python 與資料抽取](ch15_hull_vitesse_zh-TW.reading.html) | [md](ch15_hull_vitesse_zh-TW.md) |
| 16 | [報表、檔案與外部系統整合](ch16_reports_integration_zh-TW.reading.html) | [md](ch16_reports_integration_zh-TW.md) |
| 17 | [除錯、測試、部署與版本管理](ch17_debug_deploy_zh-TW.reading.html) | [md](ch17_debug_deploy_zh-TW.md) |
| 18 | [實戰案例與完整範例](ch18_case_studies_zh-TW.reading.html) | [md](ch18_case_studies_zh-TW.md) |
| **附錄** | | |
| A | [專業資源與官方訓練地圖](appx_a_resources_zh-TW.reading.html) | [md](appx_a_resources_zh-TW.md) |
| B | [術語表與指令速查](appx_b_glossary_zh-TW.reading.html) | [md](appx_b_glossary_zh-TW.md) |

## 練習工具

- [PML 互動課程](aveva_pml_learning_guide.html)：程式範例、小測驗與學習進度，搭配第 11–13 章。
- [Marine 3D 學習實驗室](marine_3d_lab.html)：切換船體、設備與管線，搭配第 3–7 章。

## 資料夾說明

| 資料夾 | 內容 |
|---|---|
| `images/diagrams/` | 本課程自繪的 SVG 圖解（37 張） |
| `images/aveva/` | 公開版不收錄 AVEVA 官方截圖，頁面以說明文字代替 |
| `images/cases/` | CC BY-NC 開放取用論文的實機畫面，以及範例的版面示意圖 |
| `examples/` | MIT 授權的二次開發範例原始碼（PML 表單、C# 外掛、Vitesse 腳本） |
| `vendor/` | 3D 實驗室使用的 three.js |

各圖片資料夾的 `README.txt` 有出處與授權說明。

## 維護說明

- 修改任何章節的 `.md` 後，執行 `python -X utf8 build_reading_pages.py`，重新產生 `.reading.html` 閱讀頁。
- 新增章節時，在 `build_reading_pages.py` 的 `books` 清單加入，並同步更新本檔、`ch00` 知識地圖與 `../index.html`。
- 每章結構：學習目標 → 概念 → 畫面與圖解 → 範例 → 開發人員須知 → 練習 → 自我檢核 → 資料來源。
- 標示〔待核對〕的項目，在公司版本確認後請改寫為確定內容並移除標記。

## 版權與適用範圍

課程內容依 AVEVA 官方公開文件、開放取用論文與開源範例自主撰寫，不是官方手冊的翻譯，未收錄未經授權轉載的訓練手冊。官方文件多為 E3D 2.1 版本，與 AVEVA Marine 12.x 可能有差異，實際操作請核對公司安裝版本、授權與專案規範。
