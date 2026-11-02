# 第 0 章　課程總覽與知識地圖

> 這是整套「AVEVA Marine 與二次開發」課程的總綱。它說明**學會 AVEVA Marine 並能進行二次開發需要哪些知識點**、章節順序、每章的學習成果與自我檢核方式。
>
> 本課程的目標讀者是**開發人員**：具備一般程式設計經驗（任何語言皆可，懂 SQL 或物件導向更好），但不一定有造船背景。課程會把船舶設計的領域知識，轉譯成開發人員熟悉的概念，例如資料模型、樹狀結構、外鍵、事件、外掛架構。

## 0.1 為什麼開發人員要先懂業務

AVEVA Marine 的二次開發，九成的困難不在語法，而在**資料**：

- 不知道「板架」「加強材」「管段」在資料庫裡是什麼元素、屬性叫什麼，就寫不出查詢。
- 不知道船體修改會連動哪些構件，就寫不出安全的批次修改工具。
- 不知道目錄與等級的關係，就會寫出產生錯誤材料表的工具。

所以本課程分成六大部分，**先建立入門與資料模型的概念，再依船體、舾裝、目錄與圖面理解業務領域，接著進入二次開發技術，最後掌握系統管理與維運**。

```
第一部分　入門與資料模型（第 1–7 章）
        ↓   懂得「資料長什麼樣子、存在哪裡、底層概念是什麼」
第二部分　船體設計（第 8–16 章）
第三部分　舾裝設計（第 17–24 章）
第四部分　目錄與圖面（第 25–30 章）
        ↓   懂得「資料代表什麼工程意義、怎麼流動、怎麼變成圖與製造資料」
第五部分　二次開發（第 31–42 章）
        ↓   懂得「怎麼安全地讀、寫、呈現與整合這些資料」
第六部分　系統管理與維運（第 43–47 章）
            懂得「怎麼讓整套系統被安裝、授權、備份、還原、升級與維護」
```

> **沒有造船背景的讀者，建議先讀[造船領域知識](shipbuilding_fundamentals.html)。** 那是一門獨立的十單元課程，用船廠的語言說明船型尺寸、幾何性能、船體結構、建造流程、舾裝、塗裝與焊接檢驗，每個單元都會標示對應的 AVEVA 模組與元素。讀完再回來看第 12、23、27、36、40 章，你會發現那些元素型別突然有了現場意義。

> 想練 PML 語法的人，另見 [PML 互動課程](aveva_pml_learning_guide.html)（8 個階段、6 個實作工作坊）。

## 0.2 開發人員視角的概念對照表

| AVEVA Marine 概念 | 開發人員熟悉的對應概念 | 說明章節 |
|---|---|---|
| 專案（Project） | 一套資料庫系統的執行個體 | 第 3 章 |
| DB（DESI、CATA、PADD…） | 資料庫中的 schema 或資料表群組 | 第 3 章 |
| MDB | 連線時掛載的資料庫組合（類似 search path） | 第 3 章 |
| Team／Claim | 寫入權限與資料列鎖定 | 第 3 章 |
| Session | 交易紀錄與版本快照 | 第 3 章 |
| 元素（Element） | 樹狀結構中的節點（類似 XML DOM 節點） | 第 4 章 |
| 元素型別（SITE、ZONE、PIPE…） | 節點的類別（Class） | 第 4 章 |
| 屬性（Attribute） | 節點的欄位 | 第 4 章 |
| 參照屬性（SPRE、CREF…） | 外鍵 | 第 4 章 |
| UDA（使用者自訂屬性） | 自訂欄位、擴充欄位 | 第 4 章 |
| CE（Current Element） | 目前游標所在的節點 | 第 4 章 |
| 目錄與等級 | 主檔資料與允許值規則 | 第 25 章 |
| 船體拓撲（板架參考） | 相依圖（Dependency Graph） | 第 9 章 |
| 生產資訊抽出 | 由模型產生的衍生資料（Materialized View） | 第 15 章 |
| PML | 內嵌於系統的腳本語言 | 第 32–34 章 |
| PML2 表單 | 宣告式 GUI | 第 34 章 |
| .NET Add-in | 外掛（Plugin），以依賴注入取得服務 | 第 35 章 |
| Vitesse | 船體模組的 Python 2.6 腳本環境 | 第 36 章 |

## 0.3 章節地圖

章節依**學習順序**排列：先入門與資料模型，再依業務領域（船體、舾裝、目錄與圖面）深入，之後是二次開發，最後是系統管理與維運。每章的概覽與深入內容都已分開，各章章末的〔待核對〕與取材覆蓋集中在[附錄 D](appx_d_verification_zh-TW.reading.html) 與[附錄 E](appx_e_coverage_zh-TW.reading.html)。

### 第一部分　入門與資料模型

| 章 | 標題 | 核心問題 |
|---|---|---|
| 1 | [Marine 入門基礎：Getting Started 官方導覽（功能、資料、屬性、GUI 與基本操作）](ch01_getting_started_zh-TW.reading.html) | 第一次打開 Marine，該懂哪些資料與 GUI 的基本操作？ |
| 2 | [產品架構、模組與啟動環境](ch02_architecture_zh-TW.reading.html) | Marine 由哪些模組組成？從哪裡啟動？環境變數做什麼？ |
| 3 | [專案、資料庫、MDB 與權限](ch03_project_database_zh-TW.reading.html) | 資料存在哪裡？誰能改？如何追蹤變更？ |
| 4 | [資料階層、元素、屬性與導覽](ch04_hierarchy_attributes_zh-TW.reading.html) | 資料樹怎麼組織？怎麼查詢屬性？ |
| 5 | [座標、方向與幾何](ch05_coordinates_geometry_zh-TW.reading.html) | 位置與方向怎麼表示？船體定位系統是什麼？ |
| 6 | [船體概念與基礎：Product Information Model、模型物件、拓撲與命名](ch06_hull_concepts_zh-TW.reading.html) | 船體資料模型的底層概念是什麼？XML 介面怎麼接？ |
| 7 | [資料模型參考導讀：Data Model Reference Manual](ch07_data_model_reference_zh-TW.reading.html) | 怎麼查資料模型手冊？各領域有哪些元素型別與屬性？ |

### 第二部分　船體設計

| 章 | 標題 | 核心問題 |
|---|---|---|
| 8 | [初始設計（Initial Design）：型線、曲面、靜水力、艙室與水動力](ch08_initial_design_zh-TW.reading.html) | 從型線到艙室、靜水力與耐海性，初始設計的資料怎麼流動、怎麼交給後續設計？ |
| 9 | [船體建模：曲面、板架與拓撲](ch09_hull_modelling_zh-TW.reading.html) | 船體結構如何建模？為什麼改一處會牽動很多處？ |
| 10 | [裝配規劃與船體結構初步設計：Assembly Planning 與 Hull Structural Design](ch10_assembly_structural_zh-TW.reading.html) | 組立怎麼規劃並出圖？結構初步設計如何順暢轉入詳細設計？ |
| 11 | [曲面管理與分區：Surface Manager、Block Division 與多視圖專案](ch11_surface_block_zh-TW.reading.html) | 曲面如何檢查與整理、早期模型如何切成生產分段、設計與生產如何共用同一模型？ |
| 12 | [空間管理與有限元素模型：Space Management 與 Finite Element Model](ch12_space_fem_zh-TW.reading.html) | 空間如何建立並用於算量，結構模型如何理想化成有限元素模型並交給外部分析？ |
| 13 | [船體詳細設計（一）：設定與標準、初始化工具、平面板架建模](ch13_hull_detail_planar_zh-TW.reading.html) | 船體詳細設計要先設定哪些標準？平面板架怎麼建？ |
| 14 | [船體詳細設計（二）：曲面板架建模、選用功能與雜項工具](ch14_hull_detail_curved_zh-TW.reading.html) | 曲面外板與加強材怎麼建模與展開？有哪些選用功能？ |
| 15 | [船體生產資訊、套料與裝配](ch15_hull_production_zh-TW.reading.html) | 模型如何變成切割與裝配資料？ |
| 16 | [船體詳細設計（三）：製造資訊與鐵舾裝生產特徵](ch16_hull_detail_manufacturing_zh-TW.reading.html) | 船體模型如何轉成製造資料？套料與切割輸出怎麼運作？ |

### 第三部分　舾裝設計

| 章 | 標題 | 核心問題 |
|---|---|---|
| 17 | [舾裝設計：設備、管路、結構、通風與電纜](ch17_outfitting_zh-TW.reading.html) | 舾裝物件怎麼建模？管路設計流程是什麼？ |
| 18 | [通風與設備設計：HVAC Designer 與 Equipment](ch18_hvac_equipment_zh-TW.reading.html) | 設備與風管如何建立、修改並出圖？ |
| 19 | [管路設計（Pipework）：從 PIPE／BRAN 到 Spool、Isometric 與管支架](ch19_pipework_zh-TW.reading.html) | 一條管線從建模、路由、穿孔到 Spooling 與出圖，資料如何流動？ |
| 20 | [管路等角圖：Isodraft](ch20_isodraft_zh-TW.reading.html) | 管路等角圖怎麼產生與客製？材料清單與標註如何設定？ |
| 21 | [結構設計（Structures）：Frame、型鋼、板、接頭與平台樓梯](ch21_structures_zh-TW.reading.html) | 型鋼構件、接頭、板與平台梯欄在資料庫裡如何表示？ |
| 22 | [電纜設計與多專業支撐：Cable Design 與 Multi-Discipline Supports](ch22_cable_supports_zh-TW.reading.html) | 電纜如何佈線並檢查填充率？跨專業的支撐如何統一設計與管理？ |
| 23 | [艙室設計與原理圖：Room Design 與 Schematics](ch23_room_schematics_zh-TW.reading.html) | 艙室如何建模？原理圖與 3D 模型如何比對並同步？ |
| 24 | [設計共通功能：Clash Manager、Data Checker、Design Model Editor 與 Reporting](ch24_design_common_zh-TW.reading.html) | 怎麼檢查碰撞與資料正確性？報表工具怎麼選與使用？ |

### 第四部分　目錄與圖面

| 章 | 標題 | 核心問題 |
|---|---|---|
| 25 | [目錄與等級](ch25_catalogue_spec_zh-TW.reading.html) | 元件從哪裡來？等級如何約束設計？ |
| 26 | [目錄與等級深入：Catalogs and Specifications 與 Design Templates](ch26_catalogs_specs_deep_zh-TW.reading.html) | 目錄、等級與設計樣板怎麼建置、檢查與維護？ |
| 27 | [圖面、ISO 圖與報表輸出](ch27_drawings_zh-TW.reading.html) | 圖面如何從模型產生並保持更新？ |
| 28 | [Draft 圖面管理與出圖流程：Draft Administrator、AutoDRAFT、Drawing Production 與 PLOT](ch28_draft_admin_production_zh-TW.reading.html) | 出圖流程需要管理者先設定什麼？圖怎麼從模型產生並輸出？ |
| 29 | [Marine Drafting 與 Design Draft：船體與舾裝的圖面製作](ch29_marine_drafting_zh-TW.reading.html) | 船體與舾裝的圖面資料怎麼存？視圖、標註與修訂怎麼運作？ |
| 30 | [其他設計模組速覽：Design Reuse、Area Based ADP、Weld Planning 與 Factory Automation](ch30_other_modules_zh-TW.reading.html) | 還有哪些設計輔助模組、各自解決什麼問題、何時該用？ |

### 第五部分　二次開發

| 章 | 標題 | 核心問題 |
|---|---|---|
| 31 | [開發環境：PMLLIB、檔案類型與部署結構](ch31_dev_environment_zh-TW.reading.html) | 程式放在哪裡？系統如何找到它？ |
| 32 | [PML 語言核心](ch32_pml_language_zh-TW.reading.html) | 變數、型別、流程控制、函式、物件、錯誤處理 |
| 33 | [PML 資料庫操作](ch33_pml_database_zh-TW.reading.html) | 如何導覽、查詢、建立、修改與刪除元素？ |
| 34 | [PML2 表單、選單與 Add-in](ch34_pml_forms_addins_zh-TW.reading.html) | 如何做出使用者介面並掛進系統選單？ |
| 35 | [.NET 開發：PML.NET 與 CAF Add-in](ch35_dotnet_zh-TW.reading.html) | 什麼時候用 C#？怎麼寫、怎麼部署？ |
| 36 | [船體開發：Vitesse Python 與資料抽取](ch36_hull_vitesse_zh-TW.reading.html) | 船體資料怎麼用程式讀取？ |
| 37 | [外部整合與舊版開發工具：Interfaces 與 Legacy Applications](ch37_interfaces_legacy_zh-TW.reading.html) | Marine 如何與 ERM 等外部系統整合？舊版 Vitesse 與 Data Extraction 還要懂多少？ |
| 38 | [報表、檔案與外部系統整合](ch38_reports_integration_zh-TW.reading.html) | 如何輸出 Excel／CSV、與 ERP／PDM 交換資料？ |
| 39 | [客製化官方手冊導讀：Software Customization、.NET Customization、Data Access Routines 與 Marine Customization](ch39_customization_manuals_zh-TW.reading.html) | 官方客製化手冊各講什麼？與本課程第 10–17 章如何對應？ |
| 40 | [除錯、測試、部署與版本管理](ch40_debug_deploy_zh-TW.reading.html) | 如何讓工具可靠、可維護、可安全上線？ |
| 41 | [實戰案例與完整範例](ch41_case_studies_zh-TW.reading.html) | 真實專案怎麼做？完整範例怎麼部署？ |
| 42 | [載重電腦整合：從 AVEVA 取得重量重心與水艙資料](ch42_loading_computer_zh-TW.reading.html) | 載重電腦要什麼？怎麼匯出、對帳與送認可？ |

### 第六部分　系統管理與維運

| 章 | 標題 | 核心問題 |
|---|---|---|
| 43 | [系統管理與維運：安裝、資料庫、帳號、備份與檔案管理](ch43_system_administration_zh-TW.reading.html) | 系統怎麼安裝、授權、備份、還原、升級與稽核？ |
| 44 | [Monitor 與 Marine 執行環境：Monitor Reference、Program Environment、Runtime 與命令列工具](ch44_monitor_runtime_zh-TW.reading.html) | 進入 Marine 前後，Monitor 與執行環境在做什麼？命令與錯誤怎麼讀？ |
| 45 | [資料庫管理深入：Database Management、SQL Direct 與 Status Control](ch45_database_management_zh-TW.reading.html) | 資料庫怎麼管理、回溯與合併？怎麼用 SQL 查 Marine 資料？ |
| 46 | [船體資料庫與分散式專案：Hull Dabacon 與 Global](ch46_dabacon_global_zh-TW.reading.html) | 船體資料存在哪裡？多地點協作的 Global 怎麼運作與維護？ |
| 47 | [12.1 版本說明與升級：Release Bulletin、設定需求與功能變更](ch47_release_upgrade_zh-TW.reading.html) | 12.1 有哪些變更？升級前要確認什麼、有哪些風險？ |

### 附錄

| 附錄 | 標題 |
|---|---|
| A | [專業資源與官方訓練地圖](appx_a_resources_zh-TW.reading.html) |
| B | [術語表與指令速查](appx_b_glossary_zh-TW.reading.html) |
| C | [參考文獻導讀與繁中摘要](appx_c_reading_list_zh-TW.reading.html) |
| D | [〔待核對〕項目總表](appx_d_verification_zh-TW.reading.html) |
| E | [取材覆蓋總表](appx_e_coverage_zh-TW.reading.html) |

### 獨立課程

| 課程 | 標題 | 適合誰 |
|---|---|---|
| 01 | [PML 互動課程](aveva_pml_learning_guide.html) | 已讀過第 32–34 章，想動手寫語法與工作坊練習的人 |
| 02 | [造船領域知識](shipbuilding_fundamentals.html) | 沒有造船背景、想先聽懂現場語言的開發人員 |

## 0.4 各章知識點清單

第 2–5、9、15、17、25、27、31–36、38、40–43 章的知識點為人工整理；其餘章節的清單取自各章「學習目標」。

### 第 1 章　Marine 入門基礎：Getting Started 官方導覽（功能、資料、屬性、GUI 與基本操作）

- [ ] 說明 Marine 設計流程的順序，以及各模組（Design、Draft、Isodraft、Spooler、Paragon、Specon、Propcon、Admin、Lexicon、Monitor）在流程中的位置。
- [ ] 說出專案內 12 種資料庫各存什麼，並知道哪幾種是使用者平常會碰到的。
- [ ] 用「WORLD → SITE → ZONE → 專業別元素」描述設計資料庫，並解釋 Owner／Member 關係。
- [ ] 讀懂 Attributes window，並會切換分類顯示、篩選屬性、辨識 UDA 與偽屬性、匯出 Excel。
- [ ] 依登入表單逐欄完成登入，並理解 Open Read Only 等選項的作用。
- [ ] 操作表單、選單、工具列、狀態列，並把表單停靠、浮動或自動隱藏。
- [ ] 用 Design Explorer、Members List、My Data 導覽，說明 CE 與 Current List Position。
- [ ] 用 Drawlist 管理 3D 視圖內容（顯示、隱藏、顏色、透明度、本地視圖、複製視圖）。
- [ ] 用 Search Utility 組合名稱、型別、範圍、體積、屬性條件搜尋，並存成 Saved Search。
- [ ] 操作 GUI 網格（排序、篩選、群組、釘選、匯出）與 Reference List。

### 第 2 章　產品架構、模組與啟動環境

- [ ] AVEVA Marine 的來源：Tribon M3（船體）與 PDMS（舾裝）的整合。
- [ ] 主要應用模組：Hull Structural Design、Hull Detailed Design（平面、曲面、生產）、Outfitting（Design）、Marine Drafting、Outfitting Draft、Isodraft、Assembly Planning、Weld Planning。
- [ ] 共用管理模組：Monitor、Admin、Lexicon、Paragon、Propcon、Specon。
- [ ] 啟動流程：啟動批次檔、專案選擇、使用者／MDB 登入、模組選擇。
- [ ] 環境變數的角色：專案資料路徑（`XXX000` 形式）、`PMLLIB`、`PDMSUI`、`PDMSEXE`、`CAF_ADDINS_PATH`。
- [ ] 船體與舾裝資料的差異：船體使用 Databank，舾裝使用 Dabacon 資料庫。
- [ ] 命令列（Command Window）的角色：所有介面操作背後都是命令。

### 第 3 章　專案、資料庫、MDB 與權限

- [ ] 專案的組成：系統資料庫（SYST）與各類型資料庫。
- [ ] 資料庫類型：DESI、CATA、PADD、DICT、PROP、ISOD、SYST，以及船體 Databank。
- [ ] Team 擁有 DB，User 屬於 Team；寫入權限的判斷方式。
- [ ] MDB：可讀可寫的 DB 組合與搜尋順序。
- [ ] Claim（認領）機制：顯式與隱式認領、Release。
- [ ] Session、Savework、Getwork：變更何時寫入、何時對他人可見。
- [ ] Extract（衍生資料庫）與合併。
- [ ] Global 多地點同步的概念。
- [ ] 開發人員須知：工具為什麼會「寫入失敗」，常見原因與檢查方式。

### 第 4 章　資料階層、元素、屬性與導覽

- [ ] 元素樹：WORLD → SITE → ZONE → 物件 → 子元件。
- [ ] 主要元素型別：EQUI、PIPE／BRAN、STRU／FRMW／SCTN／PANE、HVAC、船體板架相關元素（HPANEL、HPLATE、HSTIFF、HBRCKT 等）。
- [ ] 元素識別：名稱（以 `/` 開頭）、參照（DBREF，如 `=12345/678`）、型別與序號。
- [ ] 屬性分類：系統屬性、幾何屬性、參照屬性、偽屬性（Pseudo Attribute）、UDA。
- [ ] 常用屬性：NAME、TYPE、OWNER、MEMBERS、DESC、POS、ORI、SPRE、PURP、FUNC。
- [ ] CE（目前元素）與導覽：上一層、成員、依名稱跳轉。
- [ ] 以命令查詢屬性：`Q` 指令與 `Q ATT` 列出所有屬性。
- [ ] 元素的合法成員（Legal Members）：哪些型別可以放在哪些型別底下。

### 第 5 章　座標、方向與幾何

- [ ] 世界座標：E／N／U（東、北、上）與船舶座標 X／Y／Z 的對應。
- [ ] POS 與 ORI：位置與方向的表示法，例如 `E 1000 N 2000 U 300`、`Y is N and Z is U`。
- [ ] `WRT`（With Respect To）：相對座標系統與座標轉換。
- [ ] 船體定位系統：肋位（FR）、縱向位置（LP）、甲板高度與偏移寫法。
- [ ] 左右舷與對稱的表示。
- [ ] PML 的幾何物件：POSITION、DIRECTION、ORIENTATION、LINE、PLANE。
- [ ] 單位：長度單位、角度單位，與船體／圖面單位設定。

### 第 6 章　船體概念與基礎：Product Information Model、模型物件、拓撲與命名

- [ ] 說明 PIM、Hull Product Model、Design Model 與 Hull Parts 的關係，以及「隱式」與「標稱尺寸」的意義。
- [ ] 畫出 Hull Structure → Block → Panel → Part，並說明 Plane Panel 與 Curved Panel 的差別。
- [ ] 區分 Design View、Assembly View 與 Shell Profile 的 Functional View。
- [ ] 列出船體 Data Bank 與環境變數（`SB_OGDB`、`SB_CGDB`、`SB_PLDB` 等）及 object code 1 的分段。
- [ ] 說明拓撲的兩種參照、在 Recreate／Copy／Move 的作用，以及「好拓撲」的原則。
- [ ] 套用命名規則：Ship Letters、Explicit／Derived／Composed、24 字元上限、板架與零件名稱格式、縱橫骨編號。
- [ ] 以 `FR`、`LP` 寫出相對位置，並寫出座標表輸入檔。
- [ ] 說明 Run Mode Control 三層級及對稱、板厚補償、型材參考點的環境變數。
- [ ] 讀懂 Functional Description 的編碼區段與四種 XML 格式的用途與關鍵元素。
- [ ] 說明 Project Material 的限制，並能查 Marine Dictionary 重點詞條。

### 第 7 章　資料模型參考導讀：Data Model Reference Manual

- [ ] 說明 DMRM 的整體分區：各資料庫的元素型別、偽屬性、屬性簡介與屬性總表。
- [ ] 讀懂一個元素型別條目的四個部分：描述、屬性、合法擁有者、合法成員。
- [ ] 區分一般屬性、特殊屬性、偽屬性與 UDA，並知道各去哪一區查。
- [ ] 說出屬性的資料型別（Name、Real、Integer、Reference、Logical、Word、String、Datetime、各種 Array、Noclaim）及其限制。
- [ ] 理解「屬性長名稱」（條目內）與「屬性縮寫」（總表、命令列）的差別。
- [ ] 憑型別地圖，判斷一個元素屬於哪個資料庫與哪個類別，以及設計庫的主要階層。
- [ ] 查出常用型別（設備、管路、結構、船體、目錄、Draft、系統）的重要屬性與擁有關係。
- [ ] 用 `Q LIST`、`Q OLIS`、`Q ATT`、`Q PSATTS`、`Q UDALIS` 等查詢確認元素的合法成員與屬性清單。
- [ ] 把 DMRM 的資料型別對應到 PML 取值，並知道哪些對應仍需實測。
- [ ] 說明手冊的限制：船體條目很薄、部分頁面有轉檔缺漏、版本差異，以及遇到時的處理方式。

### 第 8 章　初始設計（Initial Design）：型線、曲面、靜水力、艙室與水動力

- [ ] 說明 Initial Design 在整體船體設計流程中的位置，並畫出七個模組之間「釋出（Release）與使用（Use）」的資料流。
- [ ] 區分獨立（Stand-alone）專案與納入 PIM（Product Information Model）的專案，並說明 `SB_NAVARCH`、`SB_TID` 兩個環境變數的用途。
- [ ] 使用 Initial Design Project Tool 管理專案與設計（Design），並說明匯出、匯入、關聯（Associate）與釋出的差別。
- [ ] 說明 Lines 以 B-Spline 描述型線的原理，以及從匯入型值、整修曲線、水線端部到分塊生成曲面的工作順序。
- [ ] 說明 Hull Form Definition 的角色，以及為什麼「整修中的型線」與「下游使用的船體」要分開釋出。
- [ ] 說明 Surface 模組（ACIS／NURBS 幾何核心）能做什麼，以及它與 Lines 的分工。
- [ ] 說明 Compartment 的 Envelope、內部曲面、艙室與 Calculation Geometry 之間的關係，並用 Sectional Area Curve 檢查艙室定義。
- [ ] 說明 Hydrostatics（Calc）的輸入幾何格式、計算樹結構與常見計算項目，並指出它與第 45 章載重電腦的資料銜接點。
- [ ] 說明 Hydrodynamics（Hydro）的四類計算（Powering、Manoeuvring、Seakeeping、Dynamic Positioning）與資料檔。
- [ ] 說明 Utilities（Command Interface、Digit、Plot、Edit Britfair、DXF to Britfair）的用途，並列出二次開發者可串接的檔案與命令介面。

### 第 9 章　船體建模

- [ ] 船體資料鏈：初始設計（曲面、參考面）→ 結構設計 → 詳細設計 → 生產。
- [ ] 平面板架的組成：型面、邊界、接縫、板、加強材、折邊、肘板、缺口、切口、開孔。
- [ ] 設計板架與生產板架的差別。
- [ ] 拓撲參考與相依鏈：參考而非數值的設計原則。
- [ ] 曲面船體：接縫與對接縫、外板縱骨、外板展開。
- [ ] 變更影響評估與重建。
- [ ] 船體 Scheme（文字化的建模描述）。
- [ ] 開發人員須知：哪些船體資料適合用程式讀取，哪些修改不應自動化。

### 第 10 章　裝配規劃與船體結構初步設計：Assembly Planning 與 Hull Structural Design

- [ ] 說明 Assembly Planning 要解決的問題，以及組立樹（production breakdown structure）與設計樹的差別。
- [ ] 說出 `ASWL`、`ASMBLY`、`ASITEM` 三種元件的關係，並解釋為什麼零件只能屬於一個組立。
- [ ] 使用 Assembly Planning 視窗建立組立樹、收集（collect）零件、設定組立方向（`ASORI`）並播放裝配順序。
- [ ] 描述 Assembly ADP 的資料結構：Drawing Template、Backing Sheet、Task、Parts List Template 與組態檔 `assydrwg.cfg`。
- [ ] 以 Assembly Drawing 工具列產生單張、整棵樹、多選與批次的組立圖及零件表。
- [ ] 說明 Hull Structural Design 的四大目標：快速建模、早期分析與估算、出圖、平順轉入詳細設計。
- [ ] 說明 RSO（Reference Surface Object）如何變成 Functional Structure，再自動產生 Functional Panel。
- [ ] 列出 Project、Functional Structure、XML、Analysis 四個選單的主要功能與使用順序。
- [ ] 使用 Block CSV、`sj701`～`sj706` 批次程式處理分區與 RSO 資料，並知道 `sj700.sbd` 預設檔可調的參數。
- [ ] 辨別哪些介面有官方依據可做二次開發（PML、PMLNet、`.uic`），哪些仍須〔待核對〕。

### 第 11 章　曲面管理與分區：Surface Manager、Block Division 與多視圖專案

- [ ] 說明 Surface Manager 在曲面流程中的位置，以及為什麼曲面需要先檢查再使用。
- [ ] 認得 Surface Manager 的視窗元件，並說明 Hull Surfaces 與 Primitive Assemblies 兩個區域的差別。
- [ ] 區分 Workspace（`.tbw`）與 Scene 的用途，並使用 Scene Template 重複使用顯示設定。
- [ ] 說明 Import from File、Import from Project、Release Surface、Export to File 與 Export to BLines File 的資料流向與限制。
- [ ] 依用途選擇 Analyze、Combine、Sew、Optimize、Restrict、Mirror、Intersect Surface 與 Compare Surfaces 等操作。
- [ ] 說明 Block Division 的三種用途，以及來源面板、切割器（Cutter）與目標分段（Target Block）三項輸入。
- [ ] 依步驟完成一個 Block Divide Job：建立、選面板、Verify、套用切割器、Divide、排序（Sort）、檢查結果。
- [ ] 設定目標分段的標稱框與偏移量，避免面板落入錯誤分段或同時被兩個分段包含。
- [ ] 說明 Design View／Production View、Design Block／Production Block 的關係與建立專案的規則。
- [ ] 說明二次開發者可以在哪些地方接上這些流程，以及哪些部分文件沒有提供依據。

### 第 12 章　空間管理與有限元素模型：Space Management 與 Finite Element Model

- [ ] 說明「空間」不是逐一建模，而是由「封閉邊界（Envelope）」被「分割限制（Dividing Boundary）」自動切出來的。
- [ ] 區分 Space World（空間世界）、Arrangement（空間佈置）與 Space（空間），以及六種佈置類型各自的用途與預設顏色。
- [ ] 說明 Reference Surface Object（RSO）、Envelope、Block 與 Surface 在共同參考模型中的角色，並知道哪些功能放在 Project 與 Functional Structure 選單。
- [ ] 依序完成「建 Space World → 設 Envelope → 分割 → 布林運算 → Apply」並用 Merge、Rename、Purge、Void 整理成果。
- [ ] 設定空間用途（Space Purpose）與絕緣圖形控制檔，並說明它們對計算與圖面的影響。
- [ ] 用 Get Structure within 取出空間內的鋼結構，計算塗裝面積、重量重心、材料清單與焊接長度，並讀懂 `SPM*` 屬性。
- [ ] 說明空間如何轉成艙室（Compartment）、生產分段（Block），以及如何輸出給水靜力計算模組。
- [ ] 說明 FE 模型兩階段流程：Idealization（理想化）→ FE Model（網格前處理），以及每階段的主要參數。
- [ ] 解讀 Holes、Stiffeners、Swages 等處理規則，並用 FE Image 與 Statistics 檢查網格品質。
- [ ] 列出五種 FE 輸出方式與材料資料來源，並說明二次開發者目前有依據的串接點與待核對項目。

### 第 13 章　船體詳細設計（一）：設定與標準、初始化工具、平面板架建模

- [ ] 說明 Hull Detailed Design 三章的分工，以及本章三個子樹彼此的先後關係。
- [ ] 說明標準的運作模式：文字控制檔 → `inithull` 編譯 → 資料庫物件 → 環境變數啟用。
- [ ] 列出主要標準（part name、bevel、型材、endcut、flange、hole／notch、cutout／clip、bracket、shrinkage 等）各自對應的環境變數與控制物件。
- [ ] 操作 `inithull`，區分 create function 與 check function，並建立 Hull Reference 與 Block。
- [ ] 說明 panel、input scheme、statement 三層關係，以及互動模式、背景模式、separate／in view 兩種產生方式。
- [ ] 讀懂並修改 Scheme：`PANEL`、`BOUNDARY`、`SEAM`、`PLATE`、`STIFFENER`、`FLANGE`、`HOLE`、`NOTCH`、`CUTOUT`、`BRACKET`、`DOUBLING` 等陳述式。
- [ ] 使用 Plane Panel Editor 與 Planar 選單（Model、Panel、Scheme、View、PosNo、RSO、Select）。
- [ ] 用 Create View 衍生符號視圖，並理解 Recreate 與模型同步的關係。
- [ ] 設定預設檔（default file）的重要參數，並指出可供二次開發的 hook 與須實測的項目。

### 第 14 章　船體詳細設計（二）：曲面板架建模、選用功能與雜項工具

- [ ] 說明曲面船體（Curved Hull）在設計各階段的用途與限制，以及它與初始設計、平面建模、製造模組的上下游關係。
- [ ] 解釋「工作區（Workspace）」「選取清單（select list）」「物件－動作」「由下而上／由上而下」等互動原則。
- [ ] 說明 Seam、Butt、Shell Profile、Shell Stiffener、Shell Plate、Curved Panel 的概念與命名規則。
- [ ] 依步驟建立 Seam/Butt、Shell Plate、Shell Profile，並設定超長（excess）、補償（compensation）、斜角（bevel）與傾角點。
- [ ] 使用 Split／Combine／Modify Curve／To Manufacturing DB 處理外板縱骨，並建立開孔、缺口、切口與標記線。
- [ ] 使用 Geometry 功能（點、平面、一般柱面、外板曲線）從下而上建構定義曲線，並理解 Recreate 與 Topology 的作用。
- [ ] 建立 Shell Expansion、Bodyplan、Developed Plate、Curved Panel 等視圖，並用 Advanced Selection 管理選取。
- [ ] 說明外板展開方法（基準線、分條、間隙／重疊、滾軸），並知道何時要調整 Strip 控制。
- [ ] 說明七類選用功能（FRP、Stiffener Nesting、Painting Areas、GPP、Factory Automation 等）各自解決什麼問題。
- [ ] 說明零件表、領料、重量重心與船體標記程式的輸入輸出方式，並指出二次開發者可用的檔案介面。

### 第 15 章　船體生產資訊、套料與裝配

- [ ] 零件抽出：從模型產生板零件與型材零件。
- [ ] Databank：型線、板零件、型材零件、套料、生產資料庫。
- [ ] 套料：鋼板利用率、零件方向、劃線、坡口。
- [ ] 型材草圖、樣板與胎架。
- [ ] 收縮補償與裝配劃線。
- [ ] 裝配規劃（組立樹）與焊接規劃。
- [ ] 開發人員須知：生產資料是模型的「快照」，與模型的一致性問題。

### 第 16 章　船體詳細設計（三）：製造資訊與鐵舾裝生產特徵

- [ ] 說明 Production Program Interface（PPI）的三步驟（選取、執行、顯示），並使用選取工具與篩選條件。
- [ ] 說明平面零件（`sf416d`）與曲面零件（`sf831d`）自動產生程式的輸入、IP 檔與輸出資料庫（`SB_PLDB`、`SBH_PROFDB`）。
- [ ] 說明 Autopos 位置編號的規則物件、`CASE`／`BUNDLE`／`SORT` 與執行用的 `SCOPE`／`OVERWRITE`／`LIST_ONLY` 陳述。
- [ ] 說明板材套料系統的元件、概念（橋、起點、輔助功能、自動重新套料、剩料）與資料庫、預設檔、燒嘴資料。
- [ ] 說明套料到切割資料的鏈：Generic File（`.gen`）→ Generic Post Processor（GPP）的預設檔與 Kerf 檔。
- [ ] 說明 3 軸燒嘴、型材套料、Panel Line Control（PLCM）各自處理的對象與設定檔。
- [ ] 說明型材製造輸出：草圖、製造清單、彎曲資訊、端切尺寸標註與 `trig_hull_endcut_dim` 觸發器。
- [ ] 說明曲面板製造資訊：胎架柱（Jig Pillars）、板胎架（Plate Jigs）與五種彎曲樣板。
- [ ] 說明鐵舾裝（FRMW／SBFR）轉進船體生產所需的目錄設定（`SFCODE`、`TRCLIN`）、`PDNAME`／`OPTBLO` 與倒角、餘量的設定方式。
- [ ] 說明 F1 Help Texts 中 TIL Interface／File Check Interface 的用法，以及零件名稱精靈與製造資料的對應。

### 第 17 章　舾裝設計

- [ ] 設備：基本體、管嘴、樣板、維修空間。
- [ ] 管路：PIPE／BRAN 結構、Head／Tail、元件順序、連接與流向。
- [ ] 管路設計流程：P&ID → 佈管 → 干涉檢查 → 支架 → 貫穿孔 → 管段 → ISO。
- [ ] 鐵舾裝結構：FRMW、SCTN、PANE、節點。
- [ ] 通風（HVAC）與電纜托架。
- [ ] 干涉檢查與跨專業協調。
- [ ] 船體與舾裝的介面：貫穿孔與開孔申請。

### 第 18 章　通風與設備設計：HVAC Designer 與 Equipment

- [ ] 說明 `WORLD → SITE → ZONE → EQUI／HVAC` 的資料階層，以及為何建議按專業把設備、管路、通風放在不同 ZONE。
- [ ] 依步驟建立設備、子設備、基本體（Primitive）、負基本體、管嘴與電氣元件，並說明 P-point 在定位中的角色。
- [ ] 區分「手工用基本體建模」與「從 Specification／Selection Table 建立標準設備」，並說明參數化設計樣板（Design Template）的三類參數。
- [ ] 使用 Positioning Control、Equipment Point、Orientate、Connect 與 Model Editor 把設備放到正確位置與方向。
- [ ] 建立、測試與回報 Equipment Association（Mate、Align、Parallel 等八種），並用 Association Manager 與 Equipment Report 取得檢查結果。
- [ ] 說明 HVAC 階層（`HVAC → BRAN → 元件`，以及 `HSLIST → HSPOOL`）與 HVAC Window 的 Categories／Available Types 操作模式。
- [ ] 說明 HVAC 管理者需要準備的東西：樣本型錄、Detail Specification、Insulation Specification、Joint、Stiffener、Defaults、使用者自訂風管配件。
- [ ] 依序建立 HVAC System、Main Branch、元件與 Side Branch，正確選擇 Joint 與 Connect 方式，並用 Autofill 把隱含風管換成實際直管。
- [ ] 使用 Divide Main、Assembly、Tiles/Grid、Itemizing、重量／重心、Data Consistency 與 Split HVAC 等輔助工具。
- [ ] 說明 HVAC Spool 的產生、驗證、修改，以及 HVAC Sketch 如何從 Design 的 Spool 資料出圖，並指出哪些二次開發介面有官方依據。

### 第 19 章　管路設計（Pipework）：從 PIPE／BRAN 到 Spool、Isometric 與管支架

- [ ] 畫出管路資料階層 `WORLD → SITE → ZONE → PIPE → BRAN → 元件`，並說明每一層的責任。
- [ ] 說明 Pipe 與 Branch 各自可以設定哪些預設值（Pspec、Bore、Insulation、Tracing、Temperature、Pressure、Slope Ref），以及「等級向下傳遞」的規則。
- [ ] 依步驟建立 Pipe 與 Branch，定義 Head／Tail 的位置、口徑、連接型式與流向，並區分「已定位」與「已連接」。
- [ ] 說明元件建立與佈管的順序，並知道直管（`TUBI`）是由系統隱含產生的。
- [ ] 區分 Quick Pipe Routing 與 Pipe Router 的適用情境與前置條件。
- [ ] 說明管路穿孔為何需要 Hole Management，以及請求、核准、產生實際孔洞的資料流程。
- [ ] 執行 Disconnect／Reconnect、修改規格與口徑、Split／Merge 等修改作業，並知道各自的限制。
- [ ] 說明 Spooling 的 SPOOL／FIELD／Spool Break／Shop Flag 概念，以及 Production Checks 的檢查對象。
- [ ] 說明 Pipe Sketch、Isometric 預覽與 Pipe Fabrication 四階段（建模、Spooling、檢查、圖面與輸出）的關係。
- [ ] 說明管支架的資料階層（`REST`／`HANG`／`FRMW`／`SBFR`）與建立流程，並指出各階段二次開發者可讀取的資料。

### 第 20 章　管路等角圖：Isodraft

- [ ] 說明 Isodraft 的輸入（Design、Catalogue、Fabrication 資料庫）、輸出（PLOT 檔、材料清單、各類報表）與它在管路出圖流程中的位置。
- [ ] 區分四種 ISO 圖：合併式（Combined）、僅預製（Fabrication）、僅安裝（Erection）、Spool 圖，並指出各自的內容差異。
- [ ] 用 GUI 與命令列兩種方式產生 ISO 圖，並說明 `CHECK` 與 `DETAIL` 的差別。
- [ ] 說明選項檔（Options file）的三種存放區（Project／Company／Local）與主要選項類別。
- [ ] 說明符號鍵（SKEY）、P-point、DTEXT／MTEXT 與 SHOP 旗標如何決定元件在圖上怎麼畫、列在材料表的哪一區。
- [ ] 說明尺寸標註的三種型式（String、Composite、Overall）、歪斜與落差管線的表示法。
- [ ] 設定材料清單、切管清單（Cut pipe list）、螺栓報表與損耗係數，並知道各報表檔如何輸出。
- [ ] 說明輸出格式（PLOT、DXF、PDF、影像、EMF）與傳輸檔（Transfer file）的用途。
- [ ] 說明 SPOOLER 產生的編號與 Isodraft 的關係，以及分頁、可重複性（Repeatability）、系統等角圖與設備組件（Equipment trim）。
- [ ] 依錯誤訊息編號與常見症狀，判斷問題在模型、目錄還是選項。

### 第 21 章　結構設計（Structures）：Frame、型鋼、板、接頭與平台樓梯

- [ ] 說明 Structures 的四個應用程式（Beams and Columns、Panels and Plates、Walls and Floors、Access, Stairs and Ladders）各自負責什麼。
- [ ] 畫出結構資料階層：WORLD > SITE > ZONE > STRU > FRMW > SBFR > SCTN，並說明為什麼建立元素必須由上而下。
- [ ] 解釋「Design 與 Catalogue 的交叉參考」：SpecRef、Profile（SPRF）、P-line 與 PKEY 分別是什麼。
- [ ] 完成「初始設定」：Storage Areas、預設型鋼規格（Default Profile Specification）、Justification／Member Line／Joint Line。
- [ ] 建立柱、梁、斜撐，並用 Split、Splice、Merge、Fillet、Miter 修整構件。
- [ ] 說明 SNOD／SJOI 如何表示連接，以及 JFRE（Dominant／Subordinate）如何決定移動時的連動行為。
- [ ] 區分 Explicit（AT）、Relative（BY）、Ship Reference、Extend、Drag 等定位方式，並正確處理方向（Beta Angle、Flip、Rotate）。
- [ ] 建立板（PANE／PLOO／PAVE）、牆、地板、板配件（PFIT）與彎板（BPANEL）。
- [ ] 說明 ASL 組立（STRTWR、STRFLT、LADDER、PLTFRM、HANDRA）的資料階層，以及管理者與使用者的分工。
- [ ] 規劃結構的檢查與報表（材料清單、質量特性、干涉、圖面），並知道二次開發能抓哪些資料。

### 第 22 章　電纜設計與多專業支撐：Cable Design 與 Multi-Discipline Supports

- [ ] 說明 Cabling System 的三大部分（Cableway、Cable、Cable Tray Material）與先後順序。
- [ ] 畫出電纜資料階層 `ZONE → CWAY → CWBRAN → CTMRL → 橋架元件`，並說明 `CNODE`、`RNODE`、`RATTA`、`POINTR` 的角色。
- [ ] 設定 Cabling Application Defaults，說明規格如何向下層層繼承（cascade），以及 Storage Area 為何要求 Zone 的 Purpose 為 `CABL`。
- [ ] 依步驟建立 Cableway 與 Cableway Branch，並說明 Head／Tail 的定位方式與 Orthogonal Route。
- [ ] 說明橋架材料的建立與鋪設（Dressing）：Preliminary、Template、Explicit 三種方式。
- [ ] 建立電纜並以 Automatic、Define Route、PRP、Manual、Free Route 五種方式佈線，並解讀 Routing Status。
- [ ] 使用 Fill Level Check 判讀綠／黃／紅，並說明 Fill Check Utility Allowance 的作用。
- [ ] 說明 MDS 支撐的設計流程、三種建立方式（Cursor／Clearance／Dimensions）與 Integrity Checker。
- [ ] 區分 MDS 的標準框架（Framework）、Ancillary、Hanger、Trunnion、Special、Preliminary Support，並知道哪些需要管理員客製。
- [ ] 說明 MDS Reports 與 Health Check Utility 在交付前的用途，並指出各階段二次開發者可接的資料。

### 第 23 章　艙室設計與原理圖：Room Design 與 Schematics

- [ ] 說明 Room Design 的資料階層 `BBLOCK → BLEVEL → ROOM → DETGRP`，並指出各層的責任。
- [ ] 從 Design > Room Design 啟動應用，並說明工具列、Navigator 與 Layout／Detailing 兩組工作視窗的分工。
- [ ] 依步驟建立 Building Block、Floor Elevation 與 Room，並說明 Room Type、淨高與房間邊界的設定。
- [ ] 說明牆（`CTWALL`）、天花（`CEILIN`）、地板覆蓋（`FLRCOV`）、隔熱需求（`INSURQ`）的建立入口與細部（Panel／Profile／Joiner）。
- [ ] 說明家具、配件與固定設備如何經 Room Design Specification（`SPWL`／`TABGROUP`／`CTABLE`／`TABITEM`／`GPART`）選取。
- [ ] 說明門窗與配件的貫穿孔機制（`OPGE`／`HPGE`），以及為何船殼開孔需經 Hole Management 核准。
- [ ] 說明原理圖資料類型，以及 Integrator 的三大功能：Compare、Build、Link。
- [ ] 讀懂比較報表與顏色代碼，並知道如何接受差異、自動連結、自動更新屬性。
- [ ] 說明 Compare/Update 的 Scope by Source／Scope by Destination 與 Dabacon 元素的比對對應。
- [ ] 指出二次開發的接點：`CompareUpdate`、`integrator`、`IntegratorProjectHandler` 與 `CYMLNK` 偽屬性，並分辨哪些在文件中有依據。

### 第 24 章　設計共通功能：Clash Manager、Data Checker、Design Model Editor 與 Reporting

- [ ] 說明 System Hierarchy（`SYGPWL`／`SYGPAR`／`SYSGRP`）與標準 `SITE/ZONE` 階層的差別，以及為何能用「系統」一次對跨區元素做檢查。
- [ ] 說明 Hole Management 的受管孔（Managed Hole）、虛擬孔（Virtual Hole）、實孔（Real Hole）與請求—核准的狀態流程。
- [ ] 區分 Design 內建的 Clashes 視窗、`DESCLASH` 指令與獨立的 Clash Manager 三者的定位。
- [ ] 說明 Clash Manager 的資料模型：Clash Set、Clash Group、Discipline、Status、Level／Type。
- [ ] 讀懂 Clash Manager 的 Assign／Accept 規則（Rule Expression）、Regular Expression 與 Oracle 萬用字元兩套語法，並用 Test Rules 驗證。
- [ ] 規劃夜間批次：`mmscmd ... -clash set` 與 Track Changes，並判讀 `pclam.*` 記錄檔。
- [ ] 使用 Data Checker 視窗檢查元素、保存失敗清單，並寫出一個符合官方規格的檢查設定檔與 PML 檢查函式。
- [ ] 在 Design Model Editor 中用 Locator Handle 與 GCM 移動、旋轉元件，並知道選取集（Selection Set）規則。
- [ ] 區分 Report Designer 的 Layout Template 與 Report Definition，完成資料來源綁定、參數化與執行。
- [ ] 使用舊式 Standard Reporting 範本（欄位、排序、小計、變數、批次），並知道何時該用哪一套。

### 第 25 章　目錄與等級

- [ ] 目錄階層：CATA → SECT → CATE → SCOM，以及幾何集（GMSE）與點集（PTSE）。
- [ ] 參數化元件：參數如何驅動幾何。
- [ ] 等級階層：SPEC → SELE → SPCO，選擇條件（口徑、型式）。
- [ ] 設計元件的 SPRE 如何連到等級，再連到目錄。
- [ ] 型鋼、材料、螺栓等其他目錄。
- [ ] 目錄管理的權限與流程。
- [ ] 開發人員須知：為什麼工具不應自行建立「看起來像」的元件。

### 第 26 章　目錄與等級深入：Catalogs and Specifications 與 Design Templates

- [ ] 說明目錄與等級必須遵守「設計慣例」的原因，以及不符時標準應用程式會怎樣失效。
- [ ] 依慣例設定鋼構目錄與結構等級（型鋼、拼板厚度限制、附件、接頭），並說明 `ANY`、`NONE` 的意義。
- [ ] 列出目錄資料庫完整階層，說明六類參數與求值單位規則。
- [ ] 說明 `PTAXI`、`PTCAR`、`PTMIX` 與 P-line，以及 `LEVEL`、`TUFLA`、`CLFLA`、`OBST` 如何決定顯示與碰撞。
- [ ] 說明等級表格的 Heading、Defaults、答案列與 `*`、`+`、`-`、`=`；說明 `DELETE` 與 `REMove` 的差別。
- [ ] 說明 `PBORE0`、COCO 連接相容表與保溫等級的寫法。
- [ ] 走過 Design Template 的建立、性質、規則、`TMPREF` 掛載、測試與變更傳播。
- [ ] 使用 `CHECK` 檢查目錄，並說明二次開發者可讀取哪些屬性與偽屬性。

### 第 27 章　圖面、ISO 圖與報表輸出

- [ ] Marine Drafting（船體圖面）與 Outfitting Draft（舾裝圖面）的差異。
- [ ] 圖面資料階層：DEPT → REGI → DRWG → SHEE → VIEW 與標註。
- [ ] 關聯尺寸與自動標註、圖面更新。
- [ ] 表現規則（Representation）與圖層。
- [ ] Isodraft：ISO 圖產生與樣式設定。
- [ ] 系統內建報表與材料表（MTO）。
- [ ] 開發人員須知：批次出圖與報表自動化的切入點。

### 第 28 章　Draft 圖面管理與出圖流程：Draft Administrator、AutoDRAFT、Drawing Production 與 PLOT

- [ ] 說明 Draft 在「3D 設計 → 圖面 → 輸出」流程中的位置，以及 Draft、ADP、AutoDRAFT 三個應用程式各自負責什麼。
- [ ] 說明 Draft Administrator 要負責的八類 Library，以及誰有權進入管理者選單（`DRAFTADMIN` 團隊）。
- [ ] 說明預設值檔（`DRA-GEN-SYSTEM`、`DRA-SETUP` 等）如何被載入，Full load 與 Partial load 的差異。
- [ ] 說明 Layer Purpose、圖層建立定義、圖紙尺寸與命名規則各自控制什麼。
- [ ] 說明 Representation Rule、Style、Hatching Rule、Change Rule、Drawlist、Tag Rule 之間的引用關係。
- [ ] 說明 Backing Sheet 上的特殊 Note（`/LIMITS`、`/SCHEDULE`、`/KEYPLAN` 等）如何讓 ADP 自動化。
- [ ] 依步驟建立 Department、Registry、Drawing、Sheet、View，並區分 User-Defined View 與 Limits-Defined View。
- [ ] 說明標籤、尺寸、2D 繪圖與剖面平面（Section Plane）的基本作業與更新方式。
- [ ] 說明 AutoDRAFT 三個子系統（Drawing Editor、Symbol Editor、Frame Editor）與 DXF／巨集往返流程，以及兩種建議工作模式。
- [ ] 用 `plot driver plotfile output [options]` 做格式轉換、縮放、筆號對應，並知道 PLOT 與 Draft 管理者「Plotting Options」的關係。

### 第 29 章　Marine Drafting 與 Design Draft：船體與舾裝的圖面製作

- [ ] 說明 Marine Drafting 的兩個目的，以及它與 Draft（Design Draft）的分工。
- [ ] 說明 Marine Drafting 圖面的「雙重儲存」：PADD 資料庫與 `.SDB` 檔，並解釋 `Save Work` 為何不存目前圖面。
- [ ] 依圖面類型（Drawing Type）判斷圖面落在哪個 `DEPT／REGI`，並設定使用者自訂類型。
- [ ] 說明三層子圖（Subpicture）、圖層（Layer）、Drawing Reference、Envelope 的用途。
- [ ] 用 Insert Model、拖放、Tools > Model View 系列功能，把模型放進圖面並更新。
- [ ] 區分 Linear／Angle／Radius／Diameter／Coordinate／Curve Length／Area 尺寸，並用 Hull 專用註記標示船體零件。
- [ ] 在 Design Draft 建立 `DEPT → REGI → DRWG → SHEE → VIEW`，用 `AUTOSCALE`／`AUTOSIZE`、Id List 與 `UPDATE DESIGN` 產生圖形。
- [ ] 設定 `VIEW` 屬性（`VSCA`、`DIR`、`VTYP`、`RRSF`）、表現規則、自動填充與剖面（`PPLA`／`FPLA`／`SPLA`）。
- [ ] 說明 Dimension、Label、Autotagging 的資料模型，以及 Change Highlighting 如何標出改版。
- [ ] 讀懂 Marine Drafting 十四個功能表的結構，並指出哪些功能是 PML／Vitesse 的客製化切入點。

### 第 30 章　其他設計模組速覽：Design Reuse、Area Based ADP、Weld Planning 與 Factory Automation

- [ ] 說明 Design Reuse 的「匯出 → Transfer Set → 匯入」模式，以及 Transfer Set 存的是「資料定義」而非二進位資料。
- [ ] 使用 Design Reuse 的 GUI 與 `MCEXP`／`MCIMP` 指令完成一次匯出與匯入，並知道匯入的前置條件與限制。
- [ ] 說明 Name Changes（改名函式）如何讓資料適應目標專案的命名慣例。
- [ ] 說明 Area Based ADP（ABA）的核心物件：Area、Template、Classification、Task、Tag Rule、Keyplan。
- [ ] 區分 ABA 管理員與使用者各自的工作，並依步驟用 Process Drawings Control 批次產生圖面。
- [ ] 說明 Weld Planning 的偵測、編輯、更新模型、報表與 Batch 流程，以及三個 `.def` 設定檔的作用。
- [ ] 說明 Manual Weld 的用途與 Weld Joint／Weld／Segment 三層概念。
- [ ] 列出 Factory Automation 各選項（Profile／Plate Cutting Interface、Dotori、GSD、Shrinkage、Robot Interface、Panel Line Control）的用途。
- [ ] 讀懂 TRI/2（Robot Interface 2）中立檔的基本結構：`welded_joint`、`weld`、`weld_sequence`、`assembly_weld_table`。
- [ ] 指出哪些環節可以由二次開發接入（檔案格式、PML 函式、報表 csv），哪些屬〔待核對〕。

### 第 31 章　開發環境

- [ ] 開發路線比較：PML、PML.NET、.NET Add-in、Vitesse。
- [ ] `PMLLIB` 搜尋路徑與 `pml.index`；`pml rehash all`、`pml index`。
- [ ] 檔案類型與命名規則：`.pmlmac`、`.pmlfnc`、`.pmlfrm`、`.pmlobj`、`.pmlcmd`（檔名須小寫且與定義名稱一致）。
- [ ] `PDMSUI` 與 Add-in 定義目錄。
- [ ] 不修改官方檔案的原則：以平行目錄擴充、以搜尋順序覆蓋。
- [ ] 開發用專案與帳號、編輯器與語法高亮。
- [ ] 公司工具庫的目錄結構建議。

### 第 32 章　PML 語言核心

- [ ] PML1 與 PML2 的差別。
- [ ] 變數：區域 `!x` 與全域 `!!x`；變數不需宣告型別，但值有型別。
- [ ] 內建型別：STRING、REAL、BOOLEAN、ARRAY、DBREF、POSITION 等。
- [ ] 運算子與比較：`eq`、`ne`、`gt`、`lt`、`ge`、`le`、`and`、`or`、`not`。
- [ ] 流程控制：`if/elseif/else/endif`、`do ... enddo`（from/to、values、index）、`break`、`skip`、`golabel`。
- [ ] 字串處理：串接 `&`、`.substring()`、`.split()`、`.upcase()`、`.real()`、`.string()`。
- [ ] 陣列：起始索引為 1、`.append()`、`.size()`、`.sort()`、多維陣列。
- [ ] 函式（`define function`）與引數、回傳值。
- [ ] 物件（`define object`、`member`、`define method`）、建構子、`!this`。
- [ ] 錯誤處理：`handle`／`elsehandle`／`endhandle`、錯誤碼 `(模組,編號)`、`!!error`。
- [ ] 巨集執行：`$m`、`$P` 輸出、`$!` 變數展開、`$R` 追蹤。

### 第 33 章　PML 資料庫操作

- [ ] 導覽：設定 CE、`!!ce`、`OWNER`、`MEMBERS`、依名稱跳轉。
- [ ] 讀取屬性：`!elem.attr`、`ATTRIB`、`Q` 與程式取值的差異。
- [ ] 查詢：`COLLECTION` 物件、`EXPRESSION` 篩選、`var !x collect ... for ...`、`evaluate`。
- [ ] 建立元素：`NEW <型別>`、命名、設定屬性。
- [ ] 修改元素：設定屬性、移動、重新命名。
- [ ] 刪除元素與相依檢查。
- [ ] 認領、儲存與復原：`claim`、`savework`、`undo` 標記。
- [ ] 批次修改的安全模式：先預覽、記錄、再寫入；失敗時回復。
- [ ] 效能：減少 CE 切換、使用收集而非遞迴走訪。

### 第 34 章　PML2 表單、選單與 Add-in

- [ ] 表單定義：`setup form ... exit`、表單型別（dialog、main、document）。
- [ ] 版面：`path`、`hdist`／`vdist`、`frame`、`at` 定位、`anchor`／`dock`。
- [ ] 控制項（Gadget）：button、text、toggle、option、list、textpane、paragraph、frame、container。
- [ ] 回呼（Callback）：字串回呼與方法回呼、`!this`、事件時機（`initcall`、`okcall`、`cancelcall`）。
- [ ] 表單成員與方法：把狀態放在表單物件上。
- [ ] .NET 控制項嵌入：`container ... pmlNetControl`、`NETGRIDCONTROL`。
- [ ] 選單：`APPMENU`、`!!appMenuCntrl`、工具列。
- [ ] Add-in 定義檔與 `.modifyMenus()` 掛勾。
- [ ] 表單設計原則：唯讀預設、確認對話框、進度回饋。

### 第 35 章　.NET 開發

- [ ] CAF（Common Application Framework）架構。
- [ ] `IAddin`、`ServiceManager`、`WindowManager`、`CommandManager`、`CommandBarManager`。
- [ ] Command 模式與 UIC 介面自訂檔；`Key` 與 `CommandId` 一致。
- [ ] 資料庫 API：`DbElement`、`DbAttribute`、`DbAttributeInstance`、`CurrentElement`。
- [ ] PML.NET：`[PMLNetCallable]`、在 PML 中 `import` 與 `using namespace`、物件生命週期。
- [ ] 建置設定：目標 .NET Framework 版本、x86／x64、`Copy Local = false`。
- [ ] 部署：`<模組>Addins.xml`、`CAF_ADDINS_PATH`。
- [ ] 除錯：附加到處理程序、`Start()` 例外被吞掉的問題。

### 第 36 章　船體開發

- [ ] Vitesse 的定位：船體模組的 Python 2.6 腳本環境。
- [ ] 主要模組：`kcs_ui`、`kcs_draft`、`kcs_dex`、`kcs_util` 等。
- [ ] 資料抽取語言：`HULL.PANEL('名稱').PLA(1).THICKNESS` 這類語句與結果型別。
- [ ] Trigger、右鍵選單、批次腳本三種掛載方式。
- [ ] 從 PML／.NET 呼叫船體資料的方式〔依版本而異〕。
- [ ] 船體資料自動化的安全界線。

### 第 37 章　外部整合與舊版開發工具：Interfaces 與 Legacy Applications

- [ ] 區分 Interfaces 與 Legacy Applications 兩大區塊各收了什麼，並判斷某個整合需求該找哪一份文件。
- [ ] 說明 AVEVA ERM–Design Integration 的角色分工：Design 應用程式、Notification Service、Integration Service、AVEVA ERM。
- [ ] 描述 Update／Acknowledgement／Error 通知的流程，並說明為何已傳送的資料不會重複傳送。
- [ ] 說明 `PublishingStatus`、Design Project Id、External Reference Id（`dabaconid`）與 Sent To Application 的用途。
- [ ] 依畫面設定 Filter Configuration、Catalogue Manager 位置與 Integration Service，並說明 DB View 與 PML Function 兩種資料來源的差別。
- [ ] 說明 Material Category Mapping 的邏輯，以及 Read／Write Attributes PML 函式的用途。
- [ ] 說明標準材料、原板、型材、船體材料控制與刪除流程，並指出各自的資料交換方向。
- [ ] 說明 Developer's Toolkit 在 12.1 的定位（僅 legacy 支援），並使用 Vitesse 選單、Log 視窗與 Batch Vitesse。
- [ ] 區分 Vitesse Trigger、PML Trigger 與動態註冊的 Trigger，知道它們的優先順序。
- [ ] 讀懂 Data Extraction 的語法（Keywords、引數運算子、資料庫來源後綴）與必要的環境變數，並知道完整 Keywords 清單在哪裡。

### 第 38 章　報表、檔案與外部系統整合

- [ ] PML 檔案讀寫：`FILE` 物件、開檔模式、逐行讀寫。
- [ ] 文字編碼：中文名稱、UTF-8 與系統編碼問題。
- [ ] CSV 與 Excel 輸出（含表格控制項匯出）。
- [ ] 讀取外部資料驅動建模（例如從 Excel 匯入標準件尺寸）。
- [ ] 與 ERP／PDM 交換：檔案交換、資料庫、Web API（以 .NET 實作）。
- [ ] 排程與批次執行。

### 第 39 章　客製化官方手冊導讀：Software Customization、.NET Customization、Data Access Routines 與 Marine Customization

- [ ] 說明官方 Customization 五本手冊與 Marine Customization 的結構與用途，並對照第 31–36、38、40 章找到該查哪一本。
- [ ] 依官方 Customization Planning 列出客製化前的準備工作，以及船體、組立、焊接各領域可客製的項目。
- [ ] 說明 Data Access Routines 的定位（**唯讀**、FORTRAN 77、`D3` 常式家族）及與 PML、.NET 資料庫 API 的差異。
- [ ] 讀懂 DARs 程式骨架：`D3INIT`→`D3MMDB`→導覽→讀取→`D3FIN`，並理解錯誤旗標與 `D3ERST`。
- [ ] 說明 PML 的 Unicode 規則、命名前綴與「只改使用者區」的升級政策，並使用 `!!CE`、`VAR … EVALUATE`、`onerror`、`return error`。
- [ ] 說明 PML Add-in、Core 管理物件、EDG 與 PML Publisher 加密的概念與限制。
- [ ] 說明 .NET 客製化的介面組件、CAF 的 `IAddin`／`Command`／`WindowManager`／UIC，以及 `DbElement` 修改管線、事件、偽屬性外掛與 `DbDouble` 單位。
- [ ] 啟用並設定船舶座標的客製化顯示（`SHIPCO`、`RSDIM`），解釋輸出格式與回退規則。

### 第 40 章　除錯、測試、部署與版本管理

- [ ] 除錯工具：`$R` 追蹤、`$P` 輸出、`!!alert`、AID 輔助圖形、錯誤碼查詢。
- [ ] 常見錯誤與排除：找不到函式、表單未更新、權限不足、型別錯誤。
- [ ] 測試策略：訓練專案、測試資料、唯讀優先、回歸測試清單。
- [ ] 程式碼規範：命名、註解標頭、錯誤處理、不寫死路徑。
- [ ] 版本管理：用 Git 管理 PMLLIB 工具庫、分支與發佈。
- [ ] 部署：測試 → 試用 → 正式；部署與回復腳本。
- [ ] 保護：PML Publisher（加密）與 .NET DLL 的取捨。
- [ ] 升級相容性：Service Pack 升級時要重測什麼。

### 第 41 章　實戰案例與完整範例

- [ ] 案例：外板開孔自動化（論文，含實機畫面與實際 PML）。
- [ ] 案例：PML 管支架自動建立。
- [ ] 範例：PML 設備收集與 Excel 匯出（可部署）。
- [ ] 範例：C# 停靠視窗屬性瀏覽器（可部署）。
- [ ] 範例：Vitesse 船體板厚報表。
- [ ] 公司工具開發的優先順序與立案方式。

### 第 42 章　載重電腦整合

- [ ] 分工：AVEVA 提供幾何、重量與艙櫃資料；載重電腦負責穩度、俯仰與縱向強度。
- [ ] 四類輸入：空船重量重心、死重量、水艙特性表、靜水性能與艙區。
- [ ] 重量分組：船體鋼材、鐵舾裝、設備、管路、電纜、絕緣塗裝、裕度。
- [ ] 重量屬性：`NWEI`／`GWEI`、`NCOF`／`GCOF`、淨重與毛重的差異。
- [ ] 水艙表：測深／空距、容積、LCG／TCG／VCG、FSM、滿艙與空艙的邊界。
- [ ] 自由液面：`FSM = ρ × I`、`FSC = ΣFSM / Δ`、液位與艙形的影響。
- [ ] 座標與單位：X／Y／Z 原點與正負、t 與 kg、m 與 mm、密度。
- [ ] 資料契約：schema、版本、單位、座標、穩定 ID、筆數、雜湊。
- [ ] 對帳：明細 vs 分組、分組 vs WCoG、匯入後 vs 匯出檔。
- [ ] 測試：空船、滿載、半艙、橫傾、俯仰、受損。
- [ ] 法規：SOLAS XII/11、2008 IS Code、IACS UR L5、CSR 與船級認可。

### 第 43 章　系統管理與維運

- [ ] 責任邊界：系統管理員、設計主管、IT 基礎設施各負責什麼。
- [ ] 安裝需求：作業系統、記憶體、磁碟、網路、MSMQ、授權與權限。
- [ ] 資料存放：模型資料在專案目錄的專屬 DB 檔，不是 SQL Server。
- [ ] 專案結構：`ABC000`、`ABCMAC`、`ABCPIC`、`ABCISO`、`ABCDFLTS`、Area 變數。
- [ ] DB 檔名 `xxxnnnn_mmmm`、DB 編號範圍與 Extract 編號。
- [ ] 建立專案：目錄、環境變數、產品腳本、SYSTEM 登入、Teams／Users／DBs／MDBs。
- [ ] 複製專案：`Project > Replicate`，不可直接複製目錄，複製後要重設密碼。
- [ ] 帳號：FREE／GENERAL、Team 成員、帳號生命週期、NT Authentication。
- [ ] DB 模式：UPDATE、MULTIWRITE、CONTROLLED、Extract 與轉換限制。
- [ ] MDB 順序與新建頂層元素的落點。
- [ ] DAC：Role、Scope、ACR，與 Team 的差異。
- [ ] Session：編號規則、Savework 附加、Stamp、Merge、Backtrack。
- [ ] 備份：範圍、靜止資料庫、DICE、3-2-1、RPO／RTO、還原順序與演練。
- [ ] 檔案管理：磁碟配置、SMB、防毒排除、Cache Service、環境變數版本化。
- [ ] DICE：檢查項目、External References、Patch 的界線與排程。
- [ ] 升級：Part Upgrade、all-or-nothing、升級後不能 Backtrack。
- [ ] 災難復原：DB 損毀、目錄誤刪、伺服器損毀、勒索軟體與回復計畫。

### 第 44 章　Monitor 與 Marine 執行環境：Monitor Reference、Program Environment、Runtime 與命令列工具

- [ ] 說明進入 Marine 的順序（`PROJECT` → `USERNAME` → 選 MDB → 切模組），以及 Monitor 為什麼會擋住你。
- [ ] 區分 Free／General 使用者、Free／Restricted 模組，並判斷「為什麼這個人進不了 Admin」。
- [ ] 解釋 Current 與 Deferred（non-current）資料庫，並正確使用 `CURRENT`、`DEFER`、`EXCHANGE`。
- [ ] 使用 `LIST`、`QUERY`、`STATUS`、`SYSTAT` 查詢專案、使用者與資料庫狀態。
- [ ] 用 `PROTECT` 暫時降低自己的存取權，並知道它不能升權。
- [ ] 設計批次作業：`BATCH COPY`／`NOCOPY` 的語意、登入失敗行為、帳密保護與 COMMS DB 風險。
- [ ] 看懂 Monitor 錯誤訊息 `(39,n)` 的意義與處置。
- [ ] 說明 Job Launcher、Session、Job、`MarJobs.xml` 與 `marjobstarter.exe` 的關係。
- [ ] 解釋 `<proj>MAR` 目錄、Default File、環境變數三層覆蓋順序與 Marine Environment utility。
- [ ] 說明 `SA004` 資料庫工具能做什麼，以及它的使用界線。

### 第 45 章　資料庫管理深入：Database Management、SQL Direct 與 Status Control

- [ ] 說明 Reference Number（`=db/seq`）、Name 與 Constructed Name 的差異，以及為什麼程式應以 Refno 為穩定識別。
- [ ] 說明 Team、DB、MDB 的多對多關係，以及「Team 決定基本寫入權、MDB 決定這次能看到什麼」。
- [ ] 區分 Primary Hierarchy 與 Secondary Hierarchy（GPSET），並解釋 Pseudo Attribute 與 UDA／UDET 的角色。
- [ ] 說明修改資料庫時系統自動做的檢查（DAC、寫入模式、LOCK、認領），以及 Move／Copy 對 Refno 的影響。
- [ ] 解釋 Savework／Getwork、Session、Stamp、Merge Changes 的運作，並能用 Undo、Backtrack、Revert 選擇正確的「回頭」方式。
- [ ] 說明 Multi-write 的 Claim 與 Extract 的 Issue／Flush／Drop／Refresh，以及 Merge 演算法的衝突規則。
- [ ] 使用 `STATUS`、`SYSTAT`、`Q CLAIMLIST`、`DIFFERENCE`、`REVERT`、`CLEANUP` 與 NameSeq。
- [ ] 說明 SQL Direct 的元件（Configuration、Table Designer、PDMS Provider、PDMS Server），並能設計 Table Schema 把元素屬性映射成表格欄位。
- [ ] 說明以 Excel／ADO／SQL Server 讀寫資料的路徑與限制（不支援 `INSERT`）。
- [ ] 設計 Status Definition，說明 STADEF／STAVAL／STALNK，並用 `STM`、DAC、PML 與 C# 事件控制狀態。

### 第 46 章　船體資料庫與分散式專案：Hull Dabacon 與 Global

- [ ] 說明船體資料在 Dabacon 中以「二進位 blob＋明確儲存資料」並存，以及 Apply 為何是同步點。
- [ ] 區分 Reference Surfaces、Design panels、Production panels 三種模型視角與參照穩定性規則。
- [ ] 說明 Hull 工作流程指令（Activate、Apply、SaveWork、Unclaim、GetWork）的先後與影響範圍。
- [ ] 列出船體專案需要的資料庫型別與主要 World 元素。
- [ ] 使用 DbPrompt 建立頂層元素、批次建立 BLOCK，並知道 `NEW` 與 `!!HullNewBlock` 的用途。
- [ ] 說明哪些 Dabacon 管理工具可用於船體資料、哪些要避免。
- [ ] 說明 Global 的 Hub／Satellite、Primary／Secondary、Daemon、Transaction database 等核心概念。
- [ ] 依順序建立 Global 專案：make global、初始化 Hub、建立位置、安裝 Satellite、分配資料庫、設定 Update event。
- [ ] 使用 Command Transactions 視窗、Daemon 追蹤與日誌診斷同步問題，並知道恢復與備份的原則。
- [ ] 說明 RPC 與 WCF 的差異、設定檔關係與防火牆埠設定，以及二次開發者在分散式環境下的注意事項。

### 第 47 章　12.1 版本說明與升級：Release Bulletin、設定需求與功能變更

- [ ] 說明 Release Bulletin 的結構，並用 SP2／SP3／SP4／SP5 標記判斷某個功能是哪一版加入的。
- [ ] 說明 12.1 安裝的幾個重點：MSI 靜默安裝、ALS 授權、不可有空白字元的安裝路徑、修復版本（fix release）的套用方式。
- [ ] 說明「升級號碼」（upgrade number）、Database Version Control 與唯讀開啟的關係，並讀懂 R/W、R、X 矩陣。
- [ ] 區分強制升級與 Optional Upgrade（12010301、12010401），並說明套用後的相容性代價。
- [ ] 依官方 16 步驟寫出升級流程，並說明 Extract、Working Extract、Offline Location 的處理方式。
- [ ] 說明 Unicode 與度量單位（Units of Measure）兩項「資料表示法」變更，對舊資料與自訂 PML 的影響。
- [ ] 列出 SP5 的作業環境需求，並辨認公告內互相矛盾的舊敘述。
- [ ] 說明資料庫層的主要新增：ENGI、Design Reference DB、DBRange、Database Views、Distributed Attributes、Dabacon buffer。
- [ ] 依領域（Hull、Outfitting、Draft、Catalogue、Global…）查出 12.1 的變更，並判斷哪些屬於「行為改變」而非單純新功能。
- [ ] 產出一份升級前後的檢查清單，並說明哪些項目要先在測試專案驗證。

## 0.5 建議學習進度（12 週）

| 週 | 章節 | 產出 |
|---|---|---|
| 1 | 第 1–3 章 | 公司環境卡：版本、專案、MDB、環境變數、訓練專案帳號 |
| 2 | 第 4、5 章 | 用命令列查詢 10 種元素的屬性，整理成筆記 |
| 3 | 第 6、9 章 | 讀懂一個板架的完整定義與參考關係 |
| 4 | 第 15 章 | 追蹤一個零件從模型到套料的資料 |
| 5 | 第 17、25 章 | 追蹤一個閥門從設計到等級到目錄的關聯 |
| 6 | 第 27 章 | 產生一張圖並觀察模型修改後的更新 |
| 7 | 第 31、32 章 | 建立個人 PMLLIB，寫出第一個函式與物件 |
| 8 | 第 33 章 | 唯讀查詢工具：列出某 ZONE 的設備與屬性 |
| 9 | 第 34 章 | 把查詢工具做成表單並掛到選單 |
| 10 | 第 35、36 章 | 依工作需求選擇 .NET 或 Vitesse，完成範例（二選一） |
| 11 | 第 38、40 章 | 加入匯出、錯誤處理與部署腳本，用 Git 管理 |
| 12 | 第 41 章 | 完成一個公司實際需求的小工具並提交審查 |

> 上表只排「資料基礎＋業務主線＋開發主線」。**第 7、8、10–14、16、18–24、26、28–30、37、39、42–47 章**是領域深入與維運深入篇，請依角色與工作需要選讀，不佔用 12 週基本進度。
>
> 第 42 章（載重電腦整合）是整合專題，建議在第 38–41 章之後，搭配公司實際的載重電腦輸入格式練習。
>
> 第 43–47 章（系統管理與維運）是**另一個職能**，建議由系統管理員或工具負責人依公司環境選讀；一般開發人員至少要知道備份範圍、DB 模式與 DICE，不必一開始就深入安裝與授權細節。
>
> 想先看全貌或只查特定主題的人，可以直接用第一部分的第 1 章（入門）與第 7 章（資料模型參考）當索引，再跳到對應領域章節。

## 0.6 能力等級

| 等級 | 能做到 | 對應章節 |
|---|---|---|
| L1 使用者 | 瀏覽模型、查詢屬性、看懂圖面 | 1–7 |
| L2 領域理解 | 說明船體與舾裝的資料關係與設計流程 | 8–30 |
| L3 工具開發 | 撰寫唯讀查詢、報表與表單工具 | 31–34、38 |
| L4 進階開發 | 撰寫建立／修改工具、.NET 外掛、船體抽取、外部整合 | 33、35–37、39 |
| L5 工具負責人 | 設計工具架構、規範、部署與維護流程 | 40–42 |
| L6 系統管理 | 安裝、帳號、MDB、備份還原、DICE、升級與稽核 | 43–47 |

## 0.7 課程使用說明

- 每章結構一致：**學習目標 → 概念說明 → 實際畫面或圖解 → 程式範例（若適用）→ 開發人員須知 → 練習 → 自我檢核 → 資料來源**。
- 想深入某一章的主題時，先看[附錄 A](appx_a_resources_zh-TW.reading.html) 找資料，再看[附錄 C](appx_c_reading_list_zh-TW.reading.html) 的繁中摘要與閱讀順序（C.7 有依章節排列的路線）；各章的〔待核對〕與取材覆蓋見[附錄 D](appx_d_verification_zh-TW.reading.html)、[附錄 E](appx_e_coverage_zh-TW.reading.html)。
- 標示 **〔待核對〕** 的內容，請在公司版本中確認。
- 程式碼若標示「示意」，表示未在實機驗證；未標示者為官方文件或開源範例中的寫法，仍建議先在訓練環境執行。
- 所有會修改資料的練習，只能在**訓練專案**中進行。
- 系統截圖來源與授權，見各圖片資料夾的 `README.txt`。
