# 附錄 D　〔待核對〕項目總表

各章章末原本都有〔待核對〕彙整。為了讓章節只保留教學內容，這些彙整集中在這個附錄，依章號排列；章內仍保留逐處的〔待核對〕標記，並在章末指向本附錄。**〔待核對〕表示該處來自官方文件但文件本身不完整、前後矛盾，或需要在公司實際安裝的版本上驗證，使用前請先核對。**

## 各章概況

| 章 | 內文〔待核對〕標記數 | 彙整 |
|---|---|---|
| 第 1 章 | 5 | [見本附錄](#ch01) |
| 第 2 章 | 5 | （章內標記為主） |
| 第 3 章 | 8 | （章內標記為主） |
| 第 4 章 | 11 | （章內標記為主） |
| 第 5 章 | 5 | （章內標記為主） |
| 第 6 章 | 5 | [見本附錄](#ch06) |
| 第 7 章 | 14 | [見本附錄](#ch07) |
| 第 8 章 | 12 | [見本附錄](#ch08) |
| 第 9 章 | 3 | （章內標記為主） |
| 第 10 章 | 11 | [見本附錄](#ch10) |
| 第 11 章 | 17 | [見本附錄](#ch11) |
| 第 12 章 | 15 | [見本附錄](#ch12) |
| 第 13 章 | 7 | [見本附錄](#ch13) |
| 第 14 章 | 5 | [見本附錄](#ch14) |
| 第 15 章 | 6 | （章內標記為主） |
| 第 16 章 | 7 | [見本附錄](#ch16) |
| 第 17 章 | 5 | （章內標記為主） |
| 第 18 章 | 11 | [見本附錄](#ch18) |
| 第 19 章 | 24 | （章內標記為主） |
| 第 20 章 | 11 | [見本附錄](#ch20) |
| 第 21 章 | 17 | [見本附錄](#ch21) |
| 第 22 章 | 17 | [見本附錄](#ch22) |
| 第 23 章 | 8 | [見本附錄](#ch23) |
| 第 24 章 | 11 | [見本附錄](#ch24) |
| 第 25 章 | 4 | （章內標記為主） |
| 第 26 章 | 5 | [見本附錄](#ch26) |
| 第 27 章 | 6 | （章內標記為主） |
| 第 28 章 | 12 | [見本附錄](#ch28) |
| 第 29 章 | 5 | [見本附錄](#ch29) |
| 第 30 章 | 14 | [見本附錄](#ch30) |
| 第 31 章 | 9 | （章內標記為主） |
| 第 32 章 | 3 | （章內標記為主） |
| 第 33 章 | 9 | （章內標記為主） |
| 第 34 章 | 6 | （章內標記為主） |
| 第 35 章 | 11 | （章內標記為主） |
| 第 36 章 | 19 | （章內標記為主） |
| 第 37 章 | 6 | [見本附錄](#ch37) |
| 第 38 章 | 12 | （章內標記為主） |
| 第 39 章 | 9 | [見本附錄](#ch39) |
| 第 40 章 | 7 | （章內標記為主） |
| 第 41 章 | 2 | （章內標記為主） |
| 第 42 章 | 6 | （章內標記為主） |
| 第 43 章 | 7 | （章內標記為主） |
| 第 44 章 | 6 | [見本附錄](#ch44) |
| 第 45 章 | 3 | [見本附錄](#ch45) |
| 第 46 章 | 9 | [見本附錄](#ch46) |
| 第 47 章 | 3 | [見本附錄](#ch47) |

<a id="ch01"></a>

## 第 1 章　Marine 入門基礎：Getting Started 官方導覽（功能、資料、屬性、GUI 與基本操作）

| 項目 | 原因 |
|---|---|
| 開始功能表路徑與模組名稱 | 官方為 PDMSMarine 12.1，各公司安裝名稱可能不同 |
| 密碼「不超過 6 字元」；佈局儲存位置 | 官方舊文件說法與舊路徑，12.1 實際值未實測 |
| 繁體中文搭配 Windows 區域與字型 | 官方只說明支援遠東語言群，未實測 |
| Action Button 名稱 | 官方以圖示呈現，文字抽取不完整 |
| `HREF`、`TREF`、`CREF` 連接語意 | 官方只提及 Reference List 由其後代推得 |
| PDMS 與 Marine 介面名稱對應；產品授權 | 官方沿用舊名；授權依合約 |
| Search 結果表格寫入的條件 | 官方只列 Edit 模式，未說明權限與認領 |

<a id="ch06"></a>

## 第 6 章　船體概念與基礎：Product Information Model、模型物件、拓撲與命名

| # | 項目 | 位置 |
|---|---|---|
| 1 | MANU 命名表序號 2 加強材範例 `-S2S` 疑為筆誤 | 6.8 |
| 2 | y 軸方向（"against portside"）在 12.1 的正負號 | 6.10 |
| 3 | 中途改變專案層級環境變數（對稱、型材參考點）的後果 | 6.11 |
| 4 | TXHSTL-M 範例 `HoleGroup` 未關閉；TXHCM 範例 `Z="FR50"` 疑為筆誤 | 6.13 |
| 5 | 12.1 實際 XML schema 與官方文字（M3SP4）是否一致；各 XML 的匯入匯出入口 | 6.13、6.16 |
| 6 | 中途改用 Project Material 的後果 | 6.14 |
| 7 | Production database（Oracle）細節；.NET PML name sequence 介面 | 6.16 |
| 8 | 與 E3D 元素 `HPANEL`／`CPANEL` 的對映細節；CAT 全稱兩處不一致 | 6.15、6.16 |

<a id="ch07"></a>

## 第 7 章　資料模型參考導讀：Data Model Reference Manual

1. `Name` 型長度：簡介頁 51 字元，總表 `NAME` 為 `string(500)`。
2. `Word` 型長度：簡介頁 4 字元；ch3 引用的版本說 4 或 6 字元；`TYPE` 說截為 4 或 6。
3. `TYPE` 回傳的型別代碼與條目標題代碼的對應（如 `EQUIPMENT` 對 `EQUI`）。
4. `LASTMOD` 在 12.1 是否存在（總表未見）。
5. 命令列對 qualifier 型偽屬性（`ELEMOD`、`MODATT` 等）的語法。
6. PML 中 integer、logical、word、ori、陣列型的對應型別。
7. UDA 在 PML 的 `:` 寫法（見第 33 章）。
8. 條目中「Global tab」缺漏處的實際擁有者／成員。
9. 命令列 `Q` 輸出的實際格式。
10. .NET 取值與資料模型的關係，本次未取材。

<a id="ch08"></a>

## 第 8 章　初始設計（Initial Design）：型線、曲面、靜水力、艙室與水動力

| 編號 | 項目 | 說明 |
|---|---|---|
| 1 | 跨版本 `tidexp` 匯入 | 匯出端與船廠端 Initial Design 版本不同時的支援範圍 |
| 2 | Britfair 完整欄位格式 | 官方 Users Guide 只描述行為與關聯檔，完整欄位需查原文件或實測 |
| 3 | DML（Hull Form）、Lines／Surface Datastore、`tidexp`、`CALC` 內部格式 | 官方未公開，視為黑盒子 |
| 4 | FCT、GDS、LoadMate Fluidtnk 檔格式 | 本章只知道類型與用途 |
| 5 | HCL 檔欄位格式 | 只知道內容項目 |
| 6 | Hydro 的 `.wgt`、`.ls`、`.voy`、`.dat`、`.bin`、`.rao` 格式 | 只有 `.rat` 在本章讀到完整欄位 |
| 7 | Calc 輸出與載重電腦的對應 | 是否能直接作為載重電腦輸入，依廠商格式而定（對照[第 42 章](ch42_loading_computer_zh-TW.reading.html)） |
| 8 | Calc XML 報表輸出的結構 | 官方標示尚未 100% 完成 |
| 9 | Geometry XML 缺值時 Calc 的預設行為 | 用你們版本實測 |
| 10 | Surface、Calc、Hydro 是否支援非互動（batch）執行 | 本章讀到的頁面未提及 |
| 11 | 法規準則檔的具體數值與版本 | 以官方頁面與法規本文為準，並確認你們適用的版本 |
| 12 | 各模組全部指令清單與全部對話框欄位 | 本章只深讀總覽與代表性頁面 |

<a id="ch10"></a>

## 第 10 章　裝配規劃與船體結構初步設計：Assembly Planning 與 Hull Structural Design

`ASMBLD` 等擬似屬性的查詢語法；`AADD`、`AREMOVE` 完整語法；`.uic` 撰寫語法（官方指向 .NET Customization）；批次巨集是否明文寫入密碼；`AssemblySelection` 範例的變數可見性；Quick Panel 的 Vitesse API；XML schema（TXHBD、TXHSTL、TXSUR）與各驗船機構的對應；Log Viewer `applications.xml` 自訂作業語法；組立樹與 Weld Planning 的欄位交換。

<a id="ch11"></a>

## 第 11 章　曲面管理與分區：Surface Manager、Block Division 與多視圖專案

| 項目 | 說明 |
|---|---|
| Scene Template 路徑 | 官方只列 Windows XP／Vista／7；新版 Windows 的實際路徑 |
| Save Camera 快速鍵 | 官方表格寫作 `Cltr+S`，本章依合理推測改為 Ctrl+S |
| 取樣點檔格式 | 只有官方一個範例；編碼、換行、相鄰重複點的原因未說明 |
| `sj708` 取得與使用 | 官方稱不含標準安裝，需洽本地支援；在 AVEVA Marine 12.1 的可用性待確認 |
| Surface Manager 自動化介面 | 文件未提及腳本、命令列或 API |
| blines、`.tbw`、`SceneTemplates.dat` 內部格式 | 文件未提供 |
| Job Setup 預設值單位 | 畫面為 50／100，單位文件未明說 |
| Stored panels 與 Stored planes | Cutters 兩處用詞不同，以實機為準 |
| `SBH_CONCODES` 檔案格式、`PAN_SPLIT_ECUT_*` 所在設定檔 | 官方此頁未說明 |
| Block Division 批次執行 | 官方指向 *Batch Utilities*，本章未取材 |
| Block Division 的 Logs 是否可匯出 | 文件未提及 |
| Multi-View 轉換工具 | 官方指向 *Create/Remove Design Blocks and Panels*，本章未取材 |
| Design／Production 在資料庫的屬性與型別 | 文件未提供 |

<a id="ch12"></a>

## 第 12 章　空間管理與有限元素模型：Space Management 與 Finite Element Model

| # | 項目 | 原因 |
|---|---|---|
| 1 | FE 模型功能所在選單的確切位置 | 官方頁面只提到 Analysis > Create FE Model 與 Structural Design |
| 2 | 塗裝區 Face Code 的設定來源與格式 | 官方只指向 Surface Treatment Selection Tables |
| 3 | 分佈式屬性（Distributed Attributes）與 bound attribute 的設定位置 | 官方只說明須先設定 |
| 4 | Space XML Input 的 XML 結構 | 官方未給 |
| 5 | Calculation Geometry 輸出的 XML 結構與 calc 模組版本 | 官方未給 |
| 6 | 空間與設備、管路位置的比對功能 | 官方未涵蓋 |
| 7 | 水艙特性表（測深、容積、自由液面）是否由本模組產生 | 官方只說輸出幾何給水靜力模組 |
| 8 | 空間資料庫元素的完整型別階層與 `SPM*` 屬性可否由 .NET 直接讀取 | 官方只列屬性名 |
| 9 | FE 輸出中是否攜帶載重與邊界條件 | 官方只說輸出節點、元素、屬性與材料 |
| 10 | Hull Steel XML（含 FE 部分）的元素名稱與 schema | 官方只說內容概要 |
| 11 | 材料 XML 的單位 | 官方範例未註明單位 |
| 12 | 理想化與輸出是否有命令列或 PML 介面 | 官方只描述圖形介面 |
| 13 | 空間範圍與 FE 範圍是否可自動連動 | 官方未說明 |

<a id="ch13"></a>

## 第 13 章　船體詳細設計（一）：設定與標準、初始化工具、平面板架建模

1. 各 hook 的 Python 版本、執行環境與載入路徑（`PYTHONPATH` 以外）。
2. `_TbhookCustHole`、`_TbhookCustNotch`、`_TBhookCustBracket` 的完整介面（官方指向另一份 Vitesse 文件，本章未讀）。
3. 以程式產生 scheme 並批次生成的實際啟動方式與錯誤回報格式；`inithull` 能否無人值守執行。
4. Planar 功能與 Scheme 陳述式的 PML 屬性對照。
5. 官方文件為 TBH 時代手冊，12.1 實際選單位置（如 View > Addins）與預設檔名稱需核對。

<a id="ch14"></a>

## 第 14 章　船體詳細設計（二）：曲面板架建模、選用功能與雜項工具

| 項目 | 說明 |
|---|---|
| XML 輸入語言元素 | 僅知可涵蓋所有曲面模型物件；詳細語法在 *Hull Model Concept*，未讀 |
| DB 元素型別與屬性 | Seam、Shell Plate、Shell Stiffener、Curved Panel 等在資料庫中的型別與屬性名文件未寫 |
| PML／Vitesse 介面 | 三個子樹皆無 PML 範例；曲面船體能否由 PML 或 Vitesse 存取待實測 |
| 選用功能授權 | FRP、Stiffener Nesting、GPP 等的授權名稱與啟用方式待向管理員確認 |
| 環境變數名稱 | 文件沿用 `SB_`／`SBH_` 前綴，12.1 實機是否同名、由何處設定待確認 |
| Operators Instructions | 子頁多與 User Guide 重複，只抽讀少數頁，是否有額外前置條件待核對 |
| Customizing dialogs in Hull | 標準孔與缺口的選單客製細節未讀 |

<a id="ch16"></a>

## 第 16 章　船體詳細設計（三）：製造資訊與鐵舾裝生產特徵

1. `ppanparts.ip`、`cpanparts.ip` 的完整關鍵字清單與預設值（本章僅列部分）。
2. 自動套料 Plug-In 的 C++ 例程簽章（官方 *Interface routines* 子頁未展開）。
3. `KcsSketchDimensioning` 模組中 `DimensionSet` 的完整方法與欄位。
4. 以 PML、.NET 或 Vitesse 從外部呼叫 Job Launcher 並指定 `SB_INPUT1` 的做法。
5. 以程式查詢 `SB_PLDB`、`SBH_PROFDB` 等製造資料庫的 API。
6. 機器人介面輸出與第 30 章 Weld Planning 資料如何銜接。
7. 各 `.ip`、限制檔的關鍵字在不同 12.1 SP 的差異。
8. 鐵舾裝 `FITT`／`FIXING` 在 Design 或 PML 中的設值語法。
9. 官方頁面標題的拼寫問題（如 `KscSketchDimensioning`、Plate Jigs 清單錨點）是否影響實際類別名稱，需實測。

<a id="ch18"></a>

## 第 18 章　通風與設備設計：HVAC Designer 與 Equipment

- 程式化讀取 HVAC 元件尺寸、`BRAN` 成員、設備 P-point 與管嘴位置的 PML 語法；`HSLIST` 與官方圖 `HLIST` 寫法差異。
- `SUBE`（子設備）元素型別名稱（官方只稱 Sub-Equipment，第 17 章亦標〔待核對〕）。
- Equipment Association 的 PML／.NET API 簽章（官方僅指向 *.Net customization User Guide*、*Data Model Reference Manual*，本章未讀）。
- `IF` 表達式內 `LDPR`、`TMPL` 等關鍵字的完整語法。
- HVAC Menu Map 部分 Available Type 與視窗標題疑似錯置，以實際介面為準；`!!hvacSketch` 範例中方法名不一致（`openLog`／`openLogFile`、`!!processhvacSketches`／`.apply()`）。
- 型錄屬性清單中「`BANG`＝`DESP[10]`」似為官方筆誤（參數表為 `DESP[63]`，且 `AOFF` 為 `DESP[10]`）。

<a id="ch20"></a>

## 第 20 章　管路等角圖：Isodraft

| 編號 | 項目 | 待確認內容 |
|---|---|---|
| 1 | 模組名稱與入口 | 文件沿用 PDMS 名稱；Marine 12.1 實際的模組切換、選單名稱（Isometrics > Standard 等）需在訓練專案確認 |
| 2 | ATEXT 與中文 | 官方限定字元集不含中文；中文標題欄、字型（`TTFONT`）與 DXF/PDF 輸出的實測 |
| 3 | `COFORMAT SHIP` | 船舶肋位座標格式的實際可用性與設定 |
| 4 | `FILE` 預設模式 | 單檔或多檔的預設值；3275 的單位 |
| 5 | `CHARHEIGHT`／`CHARSIZE` | 兩個寫法哪個在 12.1 有效 |
| 6 | 選項檔文字語法 | 直接編輯選項檔的語法細節 |
| 7 | PML／.NET 呼叫 | 如何從 PML 呼叫 Isodraft 指令、取回 `QUERY` 結果；有無 .NET 物件 |
| 8 | 傳輸檔格式 | 官方未公開格式 |
| 9 | COMPIPE | 是否仍用於你們流程 |
| 10 | `PREPROCESS`／`POSTPROCESS` | 兩頁敘述重複，實際差異與執行時機 |
| 11 | 螺栓長度計算與 Reference Dimension | 本章未細讀，需補讀 |
| 12 | Symbol Keys 附錄與 ATEXT 編號 | 各 SKEY 與 P-point 圖、ATEXT 完整編號表未讀 |

<a id="ch21"></a>

## 第 21 章　結構設計（Structures）：Frame、型鋼、板、接頭與平台樓梯

| 編號 | 項目 | 原因 |
|---|---|---|
| A1 | STRU 之下可直接掛哪些元素（FRMW、板、ASL 組立）的確切階層 | 文件僅以文字與圖片說明，離線頁面未取得圖內容 |
| A2 | 長度、重量等專用屬性與 POSS／POSE 的座標基準（WRT） | 文件未給屬性語法 |
| A3 | 材料在 Design 元素中對應的屬性 | 文件只描述 GUI 的 Modify > Material |
| A4 | 如何由 SCTN 取得 Catalogue 參數化尺寸值 | 文件未提供查詢方式 |
| A5 | Primary Node 的元素型別名稱（PNOD） | 本章依文件描述推論 |
| A6 | 判斷 JOISTART／JOIEND、CREF 空值（Nulref）的 PML 寫法 | 文件只提屬性名稱 |
| A7 | 批次切換 Dominant／Subordinate 的 PML 指令 | 文件只提供 GUI 選單 |
| A8 | PAVE 頂點座標、板面積的 PML 取得方式 | 文件未提供 |
| A9 | Include Structure 的具體語意；Panel 三種連接模式的參數細節；Standard Bracing Configurations 的選項 | 本章僅列名稱，未逐頁核對 |
| A10 | ASL 組立與 Standard 關聯屬性名稱；以型別篩選 ASL 元素的語法 | 管理者指南有概念說明，屬性層級未逐頁核對 |
| A11 | 各選單路徑與視窗名稱 | 以 12.1 文件為準，實際安裝若客製化可能不同 |

<a id="ch22"></a>

## 第 22 章　電纜設計與多專業支撐：Cable Design 與 Multi-Discipline Supports

1. AVEVA Instrumentation and Electrical 與 Compare/Update 的整合細節。
2. Data Checker Utility 對 Cableways、Trays、Penetrations 的檢查內容。
3. 橋架材料表、電纜清單與出圖範本是否有預設版本，及其與第 25 章材料機制的關係。
4. 電纜通道、佈線狀態、填充率對應的 PML 屬性名稱與取值方式；`EXTGEO` 內容。
5. 批次佈線與批次健康檢查是否可由 PML 或指令列呼叫。
6. Import Cables 檔案的欄位規格。
7. MDS 完整 UDA 清單、Lighting Support 與 HVAC Special 專頁細節。
8. MDS 的客製（樣板管理、ADP）細節，本章僅確認入口。

**取材限制：** 以 *Cable Design* 全部約 66 頁讀完（部分深層子頁僅讀重點）；Multi-Discipline Supports（約 385 頁）以使用者手冊為主，管理員、客製與自動出圖手冊只讀總覽與重點表單，未逐頁細讀。

<a id="ch23"></a>

## 第 23 章　艙室設計與原理圖：Room Design 與 Schematics

1. Room Design 工具列六組功能的完整名稱與順序（文件只列出其中部分頁面）。
2. `STRWLL` 與 `STRWEL` 哪一個是實際型別名。
3. Room 的面積、淨高、Function、Occupancy 等屬性在 PML 中的實際屬性名。
4. `RPATH` 的屬性、API 與在 `CTWALL` 中的使用方式（文件指向 *Software Customization*）。
5. Room Design 是否有 PML 物件、事件或 Add-in 擴充點。
6. Room Design 專屬報表範本與 MTO 輸出方式。
7. Integrator 在無圖形模式下可用的功能範圍（文件僅提到 `openReport()` 不可用於 non-graphics）。
8. Schematic Model Manager 與 AVEVA Diagrams 在 Marine 12.1 實際授權與安裝情況（文件僅在相容性頁面提及）。
9. Tags 模組與 Integrator 在本公司專案的使用範圍（本章只概述，未逐頁讀取 Tags 內容）。

<a id="ch24"></a>

## 第 24 章　設計共通功能：Clash Manager、Data Checker、Design Model Editor 與 Reporting

1. Hole Management 在 Global 專案的 extract 與 claim 細節（以官方 Global 文件為準）。
2. `OBST = 0` 的語意。
3. Data Checker 函式簽章 `CHKDEFINITION` 與 `CHECKDEFINITION` 拼法不一致。
4. 檢查函式是否允許寫入資料庫（本章建議唯讀）。
5. `PMLREPORT()` 的方法、參數與回傳值。
6. Model Editor 的 PML undoable 物件定義方式。
7. `excelio` 在 Design 模組是否可用。
8. Clash Manager 資料庫結構與可程式化存取方式。
9. `PDMSUI`、`PDMSDFLTS` 等舊路徑變數在 12.1 實際安裝是否相同。
10. Clash Manager 的 Model Management Wizard 與獨立版建立流程未讀。

<a id="ch26"></a>

## 第 26 章　目錄與等級深入：Catalogs and Specifications 與 Design Templates

1. 以 PML 判斷 `SPCO` 的 `CATREF` 或 `TMPREF` 是否為 `Nulref`（命令列顯示 `=0/0`）的寫法。
2. 以 PML 遍歷 `TPWL > TMAR > TMPL`、讀取 `DDAT`、`VVALUE` 的寫法。
3. 以 PML 觸發 `CHECK` 並擷取訊息；結構目錄是否有等效檢查（文件稱目前不支援）。
4. PARAGON／SPECON 指令在公司 Marine 12.1 安裝版本的實際可用性（文件沿用 PDMS 說明）。
5. `TMPREF` 與 `TMPR` 縮寫並用，實際屬性名以公司版本查詢為準。
6. 吊架與支架慣例（保留 Datakey 等）是否與公司吊架目錄版本一致。
7. 船體專用標準目錄（型材、肘板、端部處理）未出現在所讀頁面，是否適用同一套慣例。
8. 設計樣板在船舶專案中的實際用途（官方範例為工廠設備與結構）。
9. Part World／Selection Table 的 PML 存取方式與公司啟用狀況。
10. 譯名以台灣慣用語整理，術語對照以公司內部詞彙表為準。

<a id="ch28"></a>

## 第 28 章　Draft 圖面管理與出圖流程：Draft Administrator、AutoDRAFT、Drawing Production 與 PLOT

1. Draft 管理團隊的實際名稱：文件同時出現 Draft Admin 與 `DRAFTADMIN`。
2. 公司 Marine 12.1 版本是否仍使用本章所述選單與預設值檔；官方原文為 PDMS 時代手冊，未逐項驗證。
3. AutoDRAFT 支援的 AutoCAD 版本（文件寫 2007、2008、2010）與公司實際版本是否相符。
4. DXF 傳輸檔英制單位手動註解的實際格式（官方原文排成 `999 P` 與 `DMS_UNITS INCH` 兩行）。
5. Hangers and Supports ADP 的 Backing Sheet 完整欄位定義（本章僅讀到前半）。
6. 以 PML 建立與更新 `DRWG`／`SHEE`／`VIEW`、讀取 Draft 屬性的語法；四份文件均未提供。
7. `Create Batch Macro` 產生的巨集內容，以及如何在背景或排程執行。
8. PLOT 的退出碼數值；以及從 Draft 命令列產生繪圖檔的完整選項（只看到 `PLOT SHEE DXF filename [CUTMARKS OFF]`）。
9. `$M/` 載入巨集的完整語法（文件僅提及）。
10. [第 27 章](ch27_drawings_zh-TW.reading.html)依據 E3D DRAW 文件撰寫，選單名稱可能與本章 12.1 官方文件不同，以本章與公司實機為準。

<a id="ch29"></a>

## 第 29 章　Marine Drafting 與 Design Draft：船體與舾裝的圖面製作

1. 第 27 章 27.2 表把 Marine Drafting 圖面存放標為「船體圖面 Databank〔待核對〕」；本章依官方文件確認為 **PADD 資料庫加 `.SDB` 檔**，第 27 章該列建議修正。
2. Config Note hook 五個方法的資料形態、回傳型別，以及 Vitesse 腳本可呼叫的 Marine Drafting API（與第 36 章 `kcs_draft` 的關係）未讀到。
3. 選單文件有複製貼上錯誤：`Modules > Hull Design` 頁寫「click Modules, then Monitor」、`Outfitting` 頁寫「switch to the Draft module」；實際行為以現場系統為準。
4. Design Draft 的 PML 指令（`UPDATE DESIGN`、`AUTOSCALE` 等）能否用於 Marine Drafting 圖面，文件僅在 ADP 與 Change Highlighting 提到相容；視為不可用。
5. `Geometry Mode` 各種點／線／弧定義等選單子功能只讀到標題；「圖面版本 8」「元素上限 1,073,741,824」「錯誤 301」等數字照文件原文，未實測。

<a id="ch30"></a>

## 第 30 章　其他設計模組速覽：Design Reuse、Area Based ADP、Weld Planning 與 Factory Automation

1. 各模組在你們公司版本中是否已授權、安裝與啟用（Design Reuse、ABA、Robot Interface 2、Panel Line Control）。
2. Design Reuse 的 General Settings File 與 Item Settings File 的實際路徑與欄位（文件僅提及檔名類別）。
3. Design Reuse 的 PML 改名函式簽名與範例函式的完整程式碼（本章取自概述，未見完整原始碼）。
4. ABA 的 Limitations 三小節（名稱長度、Rule 運算式、Task 與 Symbol Template）詳細內容；Auto-Number 的 Format PML 運算式寫法。
5. ABA 區域的建立畫面、Template View 與 Keyplan Layers 的細節（本章僅整理 Library 與 Task 層級）。
6. `weld Position.def` 官方原文含空白的檔名是否為筆誤。
7. Weld Planning 的 Vitesse 介面、Part Name Control 規則與 Execution Units 自動焊接定義（見 Hull Setup and Customization）。
8. 焊接相關是否有 PML／.NET 物件可直接讀取 `MWLDJT`、`MWELD`；報表 csv 加入 UDA 後的欄位順序是否穩定。
9. TRI/2 中 `assembly`、`plate`、`stiffener` 等船體實體的完整欄位，及與 Weld Report 欄位的對照。
10. Factory Automation 各選項（Profile／Plate Cutting Interface、GSD、Shrinkage 等）的控制參數與預設檔名稱，須參閱 Hull 的 Manufacturing 與 Setup 章節。
11. Panel Line Control 是否仍被支援，以及非 ESSI／NCE510 後處理器的取得方式。

<a id="ch37"></a>

## 第 37 章　外部整合與舊版開發工具：Interfaces 與 Legacy Applications

1. 各整合概念的 PML Function／DB View 回傳欄位與格式：文件只列名稱，須在公司版本取預設函式實測。
2. Vitesse 執行階段 Python 版本：Installation 頁寫 2.4.2，第 36 章為 2.6，須實測。
3. 虛擬屬性（ERM 即時資料）的 PML 屬性名稱與是否可用於 `COLLECTION` 篩選。
4. 客製托板與缺口掛鉤（文件另有專章）、Actual Material Usage 發佈、Hull Material Control 中的 Assembly Planning 整合：本章僅概述，未逐頁讀。
5. `NETmarAPI.chm` 與 Vitesse 的 `vitesse_access.xls` 內容：為附件，本章未讀。
6. 各 `Datext_*.xls`／`DatExt_*.xls` 的 keywords 清單：為附件，未讀。
7. ERM 端版本與授權、AVEVA Integration Service 安裝與 s14001／s14002 等畫面的完整設定：屬 ERM 文件範圍。
8. Pipe Stress、ImPLANT、ExPLANT、NET Gateway 的操作細節：僅讀了簡介頁。

<a id="ch39"></a>

## 第 39 章　客製化官方手冊導讀：Software Customization、.NET Customization、Data Access Routines 與 Marine Customization

1. 12.1 安裝目錄是否實際附有 DARs（`d3lib.dll`、`dars` 目錄），及 Intel Fortran／Microsoft C++ 版本要求是否適用。
2. 12.1 為 Unicode，DARs 的 FECs（`&~`）多位元組規則是否仍適用。
3. `marAPI.dll` 各類別的方法簽章（官方索引只列名稱）。
4. 官方範例以 Visual Studio 2005 為基準，12.1 實際支援的 Visual Studio 與 .NET 版本。
5. `IAddinTty` 範例用 `Aveva.Core.Database`、其他用 `Aveva.Pdms.Database`，是否同一組件；導覽範例的 `->` 寫法推測為文件瑕疵。
6. `OKCLA`／`OKCLH` 「棄用」註記日期異常（寫到 2026 年）。
7. 「資料庫屬性唯讀」（[1133342]）與「可透過 `DBREF` 指派屬性」（[1133329]）措辭差異，需實測。
8. `ResourceManager` 的 `zh-TW` 語系資源載入細節。
9. Grid 範例的 `appdesmain.pmlfrm` 是 Design 的做法，Marine 模組的對應表單。
10. `SHIPX` 的查詢語法、`HRSO` 所在資料庫與 claim 需求。
11. Marine 12.1 安裝是否附 `pmlencrypt.exe`（第 40 章已列同一問題）。

<a id="ch44"></a>

## 第 44 章　Monitor 與 Marine 執行環境：Monitor Reference、Program Environment、Runtime 與命令列工具

1. Catalogue DB 在 MDB 中的排序對單位設定的實際影響（44.3.5）。
2. 選單項目與命令的對應（44.4.1）。
3. Monitor 啟動巨集（`Imacro`）的修改方式（44.8）。
4. PML 內取得 `LIST`／`QUERY` 輸出的 API 與可用範圍（44.8）。
5. PML 錯誤處理在批次中的寫法（見 *Software Customization Guide*，本章未讀）（44.6.3、44.8）。
6. `ACTIONS OFF` 命令的說明（44.9）。
7. Monitor 訊息是否還有未列出的編號（44.9）。
8. `PASSWORD` 密碼長度與字元規則（44.14）。
9. `MESSAGE ID` 的識別碼格式（44.14）。
10. `tbstartjob.exe` 與 `marjobstarter.exe` 的關係（44.11.3）。
11. `SBD_DEF1` 的說明差異；`SBB_` 前綴變數的用途；Oracle 相關變數是否啟用（44.12.1）。
12. `marenvutil` 的 `Unset` 與 `Remove` 差異（44.12.2）。
13. 批次模式的啟動方式（見 *Marine Software Installation Guide*，本章未讀）（44.6.1）。

<a id="ch45"></a>

## 第 45 章　資料庫管理深入：Database Management、SQL Direct 與 Status Control

1. SQL Direct 12.0 在 Marine 12.1 現行安裝中是否仍附工具與相容的 Windows／64 位元／SQL Server 版本。
2. 以 .NET 連線 PDMSProv OLE DB Provider 的連線字串寫法（官方僅示範 ADO／VB6／Office）。
3. SQL Direct 於多使用者／伺服器端部署的可行性（官方明言為單一使用者工具）。
4. Status Control DAC 範例中 `STVLSK` 與 Pseudo Attribute `STVLST` 是否為筆誤。
5. C# 範例的完整型別簽章與事件參數（官方以 Object Browser 截圖呈現）。
6. Distributed Attributes 的設定步驟與新語法（本章僅讀概念頁）。
7. Marine 12.1 是否支援「Copying Data between Projects」（官方頁僅說不適用 Plant）。
8. `MERGE CHANGES`、`BACKTRACK`、`REVERT <database>` 於 Admin 的完整語法（本章只取自概念頁範例，見 Administrator 手冊）。

<a id="ch46"></a>

## 第 46 章　船體資料庫與分散式專案：Hull Dabacon 與 Global

1. 船體資料專屬的 Global 配置與分發步驟（官方僅指向 AVEVA Marine Support）。
2. Copy Assistant 的實際操作步驟與功能（官方簡介頁無細節）。
3. Global Server 的硬體與作業系統需求在 12.1 的現行版本（文件寫 Windows XP/2003 時代規格）。
4. 多地點 NSEQ 序號區間的建議數值。
5. Hull 側別、對稱屬性的實際屬性名稱（官方指向附錄，本章未讀附錄）。
6. `mpfind`、`mffind` 回傳型別與 PML 使用方式。
7. Extract 與 MANU、MDB 的 Marine 專屬設定細節。
8. 〈Example Macro for Collecting and Deleting Old Commands〉內容。
9. Hull 專屬 PML 物件／方法；本章僅列官方明文者。

<a id="ch47"></a>

## 第 47 章　12.1 版本說明與升級：Release Bulletin、設定需求與功能變更


1. **環境需求矛盾**：SP5 作業環境表寫 .NET Framework 4.6.1，另一頁寫需要 .NET 3.5；IE 7/8、Office 2007/2010、Windows XP 等敘述疑為舊版遺留，實際以 AVEVA 支援網站與《Minimum System Requirements Marine》為準。
2. **Windows Server 與虛擬化／Citrix**：ALS「利於 Citrix 支援」的實際條件，以及不再支援 thin client 後的部署方式。
3. **About this Bulletin** 同時出現「自 12.1.SP4 以來的變更」與「自 12.0 以來的變更」兩種描述，推測為多版本文字並存。
4. **ASL**：SP4 一頁說已移除並由 Vantage Marine 11.6 的 primitive 型能力取代；「Future Considerations」一頁說將改稱 SLH，兩頁的先後與現況待核對。
5. **Optional Upgrade 12010401** 官方稱僅含項目 93792「一般資料庫變更」，內容細節未說明。
6. **MANU 資料模型升級**的 ManuConfig 具體步驟，在《12.0 to 12.1 Upgrade》手冊，不在本文件。
7. **Windows 專案路徑空白**問題在 SP5 之後是否已解決。
8. **「Known Issues」的 SP5 General Issues** 只指向外部發行文件，未提供清單。
