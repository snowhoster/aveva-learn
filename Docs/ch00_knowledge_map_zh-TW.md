# 第 0 章　課程總覽與知識地圖

> 這是整套「AVEVA Marine 與二次開發」課程的總綱。它說明**學會 AVEVA Marine 並能進行二次開發需要哪些知識點**、章節順序、每章的學習成果與自我檢核方式。
>
> 本課程的目標讀者是**開發人員**：具備一般程式設計經驗（任何語言皆可，懂 SQL 或物件導向更好），但不一定有造船背景。課程會把船舶設計的領域知識，轉譯成開發人員熟悉的概念，例如資料模型、樹狀結構、外鍵、事件、外掛架構。

## 0.1 為什麼開發人員要先懂業務

AVEVA Marine 的二次開發，九成的困難不在語法，而在**資料**：

- 不知道「板架」「加強材」「管段」在資料庫裡是什麼元素、屬性叫什麼，就寫不出查詢。
- 不知道船體修改會連動哪些構件，就寫不出安全的批次修改工具。
- 不知道目錄與等級的關係，就會寫出產生錯誤材料表的工具。

所以本課程分成三大部分，**先建立系統與資料模型的概念，再理解業務領域，最後才進入開發技術**。

```
第一部分　系統與資料模型（第 1–4 章）
        ↓   懂得「資料長什麼樣子、存在哪裡」
第二部分　船舶設計業務領域（第 5–9 章）
        ↓   懂得「資料代表什麼工程意義、怎麼流動」
第三部分　二次開發技術（第 10–18 章）
            懂得「怎麼安全地讀、寫、呈現與整合這些資料」
```

## 0.2 開發人員視角的概念對照表

| AVEVA Marine 概念 | 開發人員熟悉的對應概念 | 說明章節 |
|---|---|---|
| 專案（Project） | 一套資料庫系統的執行個體 | 第 2 章 |
| DB（DESI、CATA、PADD…） | 資料庫中的 schema 或資料表群組 | 第 2 章 |
| MDB | 連線時掛載的資料庫組合（類似 search path） | 第 2 章 |
| Team／Claim | 寫入權限與資料列鎖定 | 第 2 章 |
| Session | 交易紀錄與版本快照 | 第 2 章 |
| 元素（Element） | 樹狀結構中的節點（類似 XML DOM 節點） | 第 3 章 |
| 元素型別（SITE、ZONE、PIPE…） | 節點的類別（Class） | 第 3 章 |
| 屬性（Attribute） | 節點的欄位 | 第 3 章 |
| 參照屬性（SPRE、CREF…） | 外鍵 | 第 3 章 |
| UDA（使用者自訂屬性） | 自訂欄位、擴充欄位 | 第 3 章 |
| CE（Current Element） | 目前游標所在的節點 | 第 3 章 |
| 目錄與等級 | 主檔資料與允許值規則 | 第 8 章 |
| 船體拓撲（板架參考） | 相依圖（Dependency Graph） | 第 5 章 |
| 生產資訊抽出 | 由模型產生的衍生資料（Materialized View） | 第 6 章 |
| PML | 內嵌於系統的腳本語言 | 第 11–13 章 |
| PML2 表單 | 宣告式 GUI | 第 13 章 |
| .NET Add-in | 外掛（Plugin），以依賴注入取得服務 | 第 14 章 |
| Vitesse | 船體模組的 Python 2.6 腳本環境 | 第 15 章 |

## 0.3 章節地圖

### 第一部分　系統與資料模型

| 章 | 標題 | 核心問題 |
|---|---|---|
| 1 | [產品架構、模組與啟動環境](ch01_architecture_zh-TW.reading.html) | Marine 由哪些模組組成？從哪裡啟動？環境變數做什麼？ |
| 2 | [專案、資料庫、MDB 與權限](ch02_project_database_zh-TW.reading.html) | 資料存在哪裡？誰能改？如何追蹤變更？ |
| 3 | [資料階層、元素、屬性與導覽](ch03_hierarchy_attributes_zh-TW.reading.html) | 資料樹怎麼組織？怎麼查詢屬性？ |
| 4 | [座標、方向與幾何](ch04_coordinates_geometry_zh-TW.reading.html) | 位置與方向怎麼表示？船體定位系統是什麼？ |

### 第二部分　船舶設計業務領域

| 章 | 標題 | 核心問題 |
|---|---|---|
| 5 | [船體建模：曲面、板架與拓撲](ch05_hull_modelling_zh-TW.reading.html) | 船體結構如何建模？為什麼改一處會牽動很多處？ |
| 6 | [船體生產資訊、套料與裝配](ch06_hull_production_zh-TW.reading.html) | 模型如何變成切割與裝配資料？ |
| 7 | [舾裝設計：設備、管路、結構、通風與電纜](ch07_outfitting_zh-TW.reading.html) | 舾裝物件怎麼建模？管路設計流程是什麼？ |
| 8 | [目錄與等級](ch08_catalogue_spec_zh-TW.reading.html) | 元件從哪裡來？等級如何約束設計？ |
| 9 | [圖面、ISO 圖與報表輸出](ch09_drawings_zh-TW.reading.html) | 圖面如何從模型產生並保持更新？ |

### 第三部分　二次開發技術

| 章 | 標題 | 核心問題 |
|---|---|---|
| 10 | [開發環境：PMLLIB、檔案類型與部署結構](ch10_dev_environment_zh-TW.reading.html) | 程式放在哪裡？系統如何找到它？ |
| 11 | [PML 語言核心](ch11_pml_language_zh-TW.reading.html) | 變數、型別、流程控制、函式、物件、錯誤處理 |
| 12 | [PML 資料庫操作](ch12_pml_database_zh-TW.reading.html) | 如何導覽、查詢、建立、修改與刪除元素？ |
| 13 | [PML2 表單、選單與 Add-in](ch13_pml_forms_addins_zh-TW.reading.html) | 如何做出使用者介面並掛進系統選單？ |
| 14 | [.NET 開發：PML.NET 與 CAF Add-in](ch14_dotnet_zh-TW.reading.html) | 什麼時候用 C#？怎麼寫、怎麼部署？ |
| 15 | [船體開發：Vitesse Python 與資料抽取](ch15_hull_vitesse_zh-TW.reading.html) | 船體資料怎麼用程式讀取？ |
| 16 | [報表、檔案與外部系統整合](ch16_reports_integration_zh-TW.reading.html) | 如何輸出 Excel／CSV、與 ERP／PDM 交換資料？ |
| 17 | [除錯、測試、部署與版本管理](ch17_debug_deploy_zh-TW.reading.html) | 如何讓工具可靠、可維護、可安全上線？ |
| 18 | [實戰案例與完整範例](ch18_case_studies_zh-TW.reading.html) | 真實專案怎麼做？完整範例怎麼部署？ |

### 附錄

| 附錄 | 標題 |
|---|---|
| A | [專業資源與官方訓練地圖](appx_a_resources_zh-TW.reading.html) |
| B | [術語表與指令速查](appx_b_glossary_zh-TW.reading.html) |

## 0.4 各章知識點清單

以下是每章必須掌握的知識點。可以把它當作學習檢核表：每一項都能用自己的話解釋，或能寫出對應的程式，才算學會。

### 第 1 章　產品架構、模組與啟動環境

- [ ] AVEVA Marine 的來源：Tribon M3（船體）與 PDMS（舾裝）的整合。
- [ ] 主要應用模組：Hull Structural Design、Hull Detailed Design（平面、曲面、生產）、Outfitting（Design）、Marine Drafting、Outfitting Draft、Isodraft、Assembly Planning、Weld Planning。
- [ ] 共用管理模組：Monitor、Admin、Lexicon、Paragon、Propcon、Specon。
- [ ] 啟動流程：啟動批次檔、專案選擇、使用者／MDB 登入、模組選擇。
- [ ] 環境變數的角色：專案資料路徑（`XXX000` 形式）、`PMLLIB`、`PDMSUI`、`PDMSEXE`、`CAF_ADDINS_PATH`。
- [ ] 船體與舾裝資料的差異：船體使用 Databank，舾裝使用 Dabacon 資料庫。
- [ ] 命令列（Command Window）的角色：所有介面操作背後都是命令。

### 第 2 章　專案、資料庫、MDB 與權限

- [ ] 專案的組成：系統資料庫（SYST）與各類型資料庫。
- [ ] 資料庫類型：DESI、CATA、PADD、DICT、PROP、ISOD、SYST，以及船體 Databank。
- [ ] Team 擁有 DB，User 屬於 Team；寫入權限的判斷方式。
- [ ] MDB：可讀可寫的 DB 組合與搜尋順序。
- [ ] Claim（認領）機制：顯式與隱式認領、Release。
- [ ] Session、Savework、Getwork：變更何時寫入、何時對他人可見。
- [ ] Extract（衍生資料庫）與合併。
- [ ] Global 多地點同步的概念。
- [ ] 開發人員須知：工具為什麼會「寫入失敗」，常見原因與檢查方式。

### 第 3 章　資料階層、元素、屬性與導覽

- [ ] 元素樹：WORLD → SITE → ZONE → 物件 → 子元件。
- [ ] 主要元素型別：EQUI、PIPE／BRAN、STRU／FRMW／SCTN／PANE、HVAC、船體板架相關元素（HPANEL、HPLATE、HSTIFF、HBRCKT 等）。
- [ ] 元素識別：名稱（以 `/` 開頭）、參照（DBREF，如 `=12345/678`）、型別與序號。
- [ ] 屬性分類：系統屬性、幾何屬性、參照屬性、偽屬性（Pseudo Attribute）、UDA。
- [ ] 常用屬性：NAME、TYPE、OWNER、MEMBERS、DESC、POS、ORI、SPRE、PURP、FUNC。
- [ ] CE（目前元素）與導覽：上一層、成員、依名稱跳轉。
- [ ] 以命令查詢屬性：`Q` 指令與 `Q ATT` 列出所有屬性。
- [ ] 元素的合法成員（Legal Members）：哪些型別可以放在哪些型別底下。

### 第 4 章　座標、方向與幾何

- [ ] 世界座標：E／N／U（東、北、上）與船舶座標 X／Y／Z 的對應。
- [ ] POS 與 ORI：位置與方向的表示法，例如 `E 1000 N 2000 U 300`、`Y is N and Z is U`。
- [ ] `WRT`（With Respect To）：相對座標系統與座標轉換。
- [ ] 船體定位系統：肋位（FR）、縱向位置（LP）、甲板高度與偏移寫法。
- [ ] 左右舷與對稱的表示。
- [ ] PML 的幾何物件：POSITION、DIRECTION、ORIENTATION、LINE、PLANE。
- [ ] 單位：長度單位、角度單位，與船體／圖面單位設定。

### 第 5 章　船體建模：曲面、板架與拓撲

- [ ] 船體資料鏈：初始設計（曲面、參考面）→ 結構設計 → 詳細設計 → 生產。
- [ ] 平面板架的組成：型面、邊界、接縫、板、加強材、折邊、肘板、缺口、切口、開孔。
- [ ] 設計板架與生產板架的差別。
- [ ] 拓撲參考與相依鏈：參考而非數值的設計原則。
- [ ] 曲面船體：接縫與對接縫、外板縱骨、外板展開。
- [ ] 變更影響評估與重建。
- [ ] 船體 Scheme（文字化的建模描述）。
- [ ] 開發人員須知：哪些船體資料適合用程式讀取，哪些修改不應自動化。

### 第 6 章　船體生產資訊、套料與裝配

- [ ] 零件抽出：從模型產生板零件與型材零件。
- [ ] Databank：型線、板零件、型材零件、套料、生產資料庫。
- [ ] 套料：鋼板利用率、零件方向、劃線、坡口。
- [ ] 型材草圖、樣板與胎架。
- [ ] 收縮補償與裝配劃線。
- [ ] 裝配規劃（組立樹）與焊接規劃。
- [ ] 開發人員須知：生產資料是模型的「快照」，與模型的一致性問題。

### 第 7 章　舾裝設計：設備、管路、結構、通風與電纜

- [ ] 設備：基本體、管嘴、樣板、維修空間。
- [ ] 管路：PIPE／BRAN 結構、Head／Tail、元件順序、連接與流向。
- [ ] 管路設計流程：P&ID → 佈管 → 干涉檢查 → 支架 → 貫穿孔 → 管段 → ISO。
- [ ] 鐵舾裝結構：FRMW、SCTN、PANE、節點。
- [ ] 通風（HVAC）與電纜托架。
- [ ] 干涉檢查與跨專業協調。
- [ ] 船體與舾裝的介面：貫穿孔與開孔申請。

### 第 8 章　目錄與等級

- [ ] 目錄階層：CATA → SECT → CATE → SCOM，以及幾何集（GMSE）與點集（PTSE）。
- [ ] 參數化元件：參數如何驅動幾何。
- [ ] 等級階層：SPEC → SELE → SPCO，選擇條件（口徑、型式）。
- [ ] 設計元件的 SPRE 如何連到等級，再連到目錄。
- [ ] 型鋼、材料、螺栓等其他目錄。
- [ ] 目錄管理的權限與流程。
- [ ] 開發人員須知：為什麼工具不應自行建立「看起來像」的元件。

### 第 9 章　圖面、ISO 圖與報表輸出

- [ ] Marine Drafting（船體圖面）與 Outfitting Draft（舾裝圖面）的差異。
- [ ] 圖面資料階層：DEPT → REGI → DRWG → SHEE → VIEW 與標註。
- [ ] 關聯尺寸與自動標註、圖面更新。
- [ ] 表現規則（Representation）與圖層。
- [ ] Isodraft：ISO 圖產生與樣式設定。
- [ ] 系統內建報表與材料表（MTO）。
- [ ] 開發人員須知：批次出圖與報表自動化的切入點。

### 第 10 章　開發環境：PMLLIB、檔案類型與部署結構

- [ ] 開發路線比較：PML、PML.NET、.NET Add-in、Vitesse。
- [ ] `PMLLIB` 搜尋路徑與 `pml.index`；`pml rehash all`、`pml index`。
- [ ] 檔案類型與命名規則：`.pmlmac`、`.pmlfnc`、`.pmlfrm`、`.pmlobj`、`.pmlcmd`（檔名須小寫且與定義名稱一致）。
- [ ] `PDMSUI` 與 Add-in 定義目錄。
- [ ] 不修改官方檔案的原則：以平行目錄擴充、以搜尋順序覆蓋。
- [ ] 開發用專案與帳號、編輯器與語法高亮。
- [ ] 公司工具庫的目錄結構建議。

### 第 11 章　PML 語言核心

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

### 第 12 章　PML 資料庫操作

- [ ] 導覽：設定 CE、`!!ce`、`OWNER`、`MEMBERS`、依名稱跳轉。
- [ ] 讀取屬性：`!elem.attr`、`ATTRIB`、`Q` 與程式取值的差異。
- [ ] 查詢：`COLLECTION` 物件、`EXPRESSION` 篩選、`var !x collect ... for ...`、`evaluate`。
- [ ] 建立元素：`NEW <型別>`、命名、設定屬性。
- [ ] 修改元素：設定屬性、移動、重新命名。
- [ ] 刪除元素與相依檢查。
- [ ] 認領、儲存與復原：`claim`、`savework`、`undo` 標記。
- [ ] 批次修改的安全模式：先預覽、記錄、再寫入；失敗時回復。
- [ ] 效能：減少 CE 切換、使用收集而非遞迴走訪。

### 第 13 章　PML2 表單、選單與 Add-in

- [ ] 表單定義：`setup form ... exit`、表單型別（dialog、main、document）。
- [ ] 版面：`path`、`hdist`／`vdist`、`frame`、`at` 定位、`anchor`／`dock`。
- [ ] 控制項（Gadget）：button、text、toggle、option、list、textpane、paragraph、frame、container。
- [ ] 回呼（Callback）：字串回呼與方法回呼、`!this`、事件時機（`initcall`、`okcall`、`cancelcall`）。
- [ ] 表單成員與方法：把狀態放在表單物件上。
- [ ] .NET 控制項嵌入：`container ... pmlNetControl`、`NETGRIDCONTROL`。
- [ ] 選單：`APPMENU`、`!!appMenuCntrl`、工具列。
- [ ] Add-in 定義檔與 `.modifyMenus()` 掛勾。
- [ ] 表單設計原則：唯讀預設、確認對話框、進度回饋。

### 第 14 章　.NET 開發：PML.NET 與 CAF Add-in

- [ ] CAF（Common Application Framework）架構。
- [ ] `IAddin`、`ServiceManager`、`WindowManager`、`CommandManager`、`CommandBarManager`。
- [ ] Command 模式與 UIC 介面自訂檔；`Key` 與 `CommandId` 一致。
- [ ] 資料庫 API：`DbElement`、`DbAttribute`、`DbAttributeInstance`、`CurrentElement`。
- [ ] PML.NET：`[PMLNetCallable]`、在 PML 中 `import` 與 `using namespace`、物件生命週期。
- [ ] 建置設定：目標 .NET Framework 版本、x86／x64、`Copy Local = false`。
- [ ] 部署：`<模組>Addins.xml`、`CAF_ADDINS_PATH`。
- [ ] 除錯：附加到處理程序、`Start()` 例外被吞掉的問題。

### 第 15 章　船體開發：Vitesse Python 與資料抽取

- [ ] Vitesse 的定位：船體模組的 Python 2.6 腳本環境。
- [ ] 主要模組：`kcs_ui`、`kcs_draft`、`kcs_dex`、`kcs_util` 等。
- [ ] 資料抽取語言：`HULL.PANEL('名稱').PLA(1).THICKNESS` 這類語句與結果型別。
- [ ] Trigger、右鍵選單、批次腳本三種掛載方式。
- [ ] 從 PML／.NET 呼叫船體資料的方式〔依版本而異〕。
- [ ] 船體資料自動化的安全界線。

### 第 16 章　報表、檔案與外部系統整合

- [ ] PML 檔案讀寫：`FILE` 物件、開檔模式、逐行讀寫。
- [ ] 文字編碼：中文名稱、UTF-8 與系統編碼問題。
- [ ] CSV 與 Excel 輸出（含表格控制項匯出）。
- [ ] 讀取外部資料驅動建模（例如從 Excel 匯入標準件尺寸）。
- [ ] 與 ERP／PDM 交換：檔案交換、資料庫、Web API（以 .NET 實作）。
- [ ] 排程與批次執行。

### 第 17 章　除錯、測試、部署與版本管理

- [ ] 除錯工具：`$R` 追蹤、`$P` 輸出、`!!alert`、AID 輔助圖形、錯誤碼查詢。
- [ ] 常見錯誤與排除：找不到函式、表單未更新、權限不足、型別錯誤。
- [ ] 測試策略：訓練專案、測試資料、唯讀優先、回歸測試清單。
- [ ] 程式碼規範：命名、註解標頭、錯誤處理、不寫死路徑。
- [ ] 版本管理：用 Git 管理 PMLLIB 工具庫、分支與發佈。
- [ ] 部署：測試 → 試用 → 正式；部署與回復腳本。
- [ ] 保護：PML Publisher（加密）與 .NET DLL 的取捨。
- [ ] 升級相容性：Service Pack 升級時要重測什麼。

### 第 18 章　實戰案例與完整範例

- [ ] 案例：外板開孔自動化（論文，含實機畫面與實際 PML）。
- [ ] 案例：PML 管支架自動建立。
- [ ] 範例：PML 設備收集與 Excel 匯出（可部署）。
- [ ] 範例：C# 停靠視窗屬性瀏覽器（可部署）。
- [ ] 範例：Vitesse 船體板厚報表。
- [ ] 公司工具開發的優先順序與立案方式。

## 0.5 建議學習進度（12 週）

| 週 | 章節 | 產出 |
|---|---|---|
| 1 | 第 1–2 章 | 公司環境卡：版本、專案、MDB、環境變數、訓練專案帳號 |
| 2 | 第 3–4 章 | 用命令列查詢 10 種元素的屬性，整理成筆記 |
| 3 | 第 5 章 | 讀懂一個板架的完整定義與參考關係 |
| 4 | 第 6 章 | 追蹤一個零件從模型到套料的資料 |
| 5 | 第 7–8 章 | 追蹤一個閥門從設計到等級到目錄的關聯 |
| 6 | 第 9 章 | 產生一張圖並觀察模型修改後的更新 |
| 7 | 第 10–11 章 | 建立個人 PMLLIB，寫出第一個函式與物件 |
| 8 | 第 12 章 | 唯讀查詢工具：列出某 ZONE 的設備與屬性 |
| 9 | 第 13 章 | 把查詢工具做成表單並掛到選單 |
| 10 | 第 14 或 15 章 | 依工作需求選擇 .NET 或 Vitesse，完成範例 |
| 11 | 第 16–17 章 | 加入匯出、錯誤處理與部署腳本，用 Git 管理 |
| 12 | 第 18 章 | 完成一個公司實際需求的小工具並提交審查 |

## 0.6 能力等級

| 等級 | 能做到 | 對應章節 |
|---|---|---|
| L1 使用者 | 瀏覽模型、查詢屬性、看懂圖面 | 1–4 |
| L2 領域理解 | 說明船體與舾裝的資料關係與設計流程 | 5–9 |
| L3 工具開發 | 撰寫唯讀查詢、報表與表單工具 | 10–13、16 |
| L4 進階開發 | 撰寫建立／修改工具、.NET 外掛、船體抽取 | 12、14、15 |
| L5 工具負責人 | 設計工具架構、規範、部署與維護流程 | 17、18 |

## 0.7 課程使用說明

- 每章結構一致：**學習目標 → 概念說明 → 實際畫面或圖解 → 程式範例（若適用）→ 開發人員須知 → 練習 → 自我檢核 → 資料來源**。
- 標示 **〔待核對〕** 的內容，請在公司版本中確認。
- 程式碼若標示「示意」，表示未在實機驗證；未標示者為官方文件或開源範例中的寫法，仍建議先在訓練環境執行。
- 所有會修改資料的練習，只能在**訓練專案**中進行。
- 系統截圖來源與授權，見各圖片資料夾的 `README.txt`。
