# 第 1 章　Marine 入門基礎：Getting Started 官方導覽（功能、資料、屬性、GUI 與基本操作）

> 這是整個課程的第一章，對照 AVEVA 給新使用者的第一份官方手冊 *Getting Started with AVEVA Marine*，定位是「**官方入門手冊導讀**」：先建立功能、資料庫、屬性、GUI 與基本操作的整體概念。這裡先給入門層次的說明，讓第一次接觸的人看得懂；細節留給後面的章節：架構與啟動見[第 2 章](ch02_architecture_zh-TW.reading.html)、專案與資料庫見[第 3 章](ch03_project_database_zh-TW.reading.html)、元素階層與屬性見[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html)。本章的重心放在官方入門手冊獨有的 **GUI 基本操作、Drawlist、Outfitting Search Utility、GUI Grid Data、Reference List、Explorer 核心篩選器與產品線**，最後給一份「新手第一天操作指南」。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件 *Marine Getting Started*（共 147 頁，已全部讀完，見 附錄 E）。該文件沿用 PDMS 時代手冊，內文大量寫 PDMS、PlantShip、Design、Draft、Spooler 等舊名稱，本章照原樣保留。手冊是操作導覽，**幾乎沒有程式範例**；命令（`Q CE`、`Q MEM`、`Q ATT`、`SAVEWORK`、`QUIT`、`SLIST`）只引用文件明列者，語法細節見[第 33 章](ch33_pml_database_zh-TW.reading.html)。官方機器翻譯有明顯誤譯（例如把 Marine 譯成「海軍陸戰隊」），本章改用台灣慣用譯名，介面名稱保留英文。與實際版本可能不同之處標〔待核對〕，彙整於 附錄 D。

## 1.1 學習目標

讀完本章，你應該能夠：

1. 說明 Marine 設計流程的順序，以及各模組（Design、Draft、Isodraft、Spooler、Paragon、Specon、Propcon、Admin、Lexicon、Monitor）在流程中的位置。
2. 說出專案內 12 種資料庫各存什麼，並知道哪幾種是使用者平常會碰到的。
3. 用「WORLD → SITE → ZONE → 專業別元素」描述設計資料庫，並解釋 Owner／Member 關係。
4. 讀懂 Attributes window，並會切換分類顯示、篩選屬性、辨識 UDA 與偽屬性、匯出 Excel。
5. 依登入表單逐欄完成登入，並理解 Open Read Only 等選項的作用。
6. 操作表單、選單、工具列、狀態列，並把表單停靠、浮動或自動隱藏。
7. 用 Design Explorer、Members List、My Data 導覽，說明 CE 與 Current List Position。
8. 用 Drawlist 管理 3D 視圖內容（顯示、隱藏、顏色、透明度、本地視圖、複製視圖）。
9. 用 Search Utility 組合名稱、型別、範圍、體積、屬性條件搜尋，並存成 Saved Search。
10. 操作 GUI 網格（排序、篩選、群組、釘選、匯出）與 Reference List。

## 1.2 Marine 功能與設計流程

### 1.2.1 它要解決什麼問題

官方開宗明義：PDMS（Plant Design Management System，本課程對應的是 Marine 的 Outfitting）讓你設計**船舶的 3D 電腦模型**，模型成為所有部門與專業的**單一資料來源**。資料全部放在資料庫，再從不同通道輸出：

> 〔公開版未收錄：AVEVA 官方產品截圖〕資料庫的輸入與輸出通道：2D 工程資料與 2D 設計圖進入資料庫，輸出文字報表、3D 漫遊與工程圖

*圖 1-1　所有資訊進同一組資料庫，再由資料庫輸出報表、3D 漫遊與工程圖。（AVEVA 官方文件截圖，僅供內部教學）*

官方列出的五項品質貢獻：

| 官方說法 | 白話意義 | 對應章節 |
|---|---|---|
| 元件資料一致可靠 | 元件尺寸與幾何預先存在 Catalogue，設計者不能改 | [第 25 章](ch25_catalogue_spec_zh-TW.reading.html) |
| 遵守可定義的工程規範 | 管路、支架、HVAC、電纜架、鋼構都由 Specification 限定可選元件 | [第 26 章](ch26_catalogs_specs_deep_zh-TW.reading.html) |
| 幾何與連接正確 | 內建資料一致性檢查，找出配件長度、法蘭等級不相容、對位錯誤 | [第 24 章](ch24_design_common_zh-TW.reading.html) |
| 避免元件干涉 | 互動式目視檢查，或用 clash 檢查（可互動式或事後補做） | [第 24 章](ch24_design_common_zh-TW.reading.html) |
| 註記與尺寸直接取自資料庫 | 圖面、等角圖、報表永遠是最新版，只有單一來源 | [第 27 章](ch27_drawings_zh-TW.reading.html) |

### 1.2.2 新專案的簡化流程

官方將新專案流程簡化為五步：

1. 用 AVEVA Administration 建立專案、設定管理控制（見[第 43 章](ch43_system_administration_zh-TW.reading.html)）。
2. 用 PARAGON 建立 Catalogue 與 Specification。
3. 用 Design 模組設計各部分，引用目錄項目。
4. 在 Design 模組檢查錯誤與不一致。
5. 用 Draft 與 Isodraft 以圖面、報表、材料表記錄設計。


### 1.2.3 模組分類（Modules in AVEVA Marine）

官方將 PDMS 與 Engineering、Diagrams 共有的模組列為 Monitor、Admin、Lexicon、Paragon、Propcon、Specon；PDMS 另外加上 Design、Draft、Isodraft、Spooler。依用途分四群：

| 群組 | 模組 | 官方描述重點 |
|---|---|---|
| 設計 | Hull Design 各應用（曲面與平面建模、Plate Nesting、Panel Line Control、Jig Pillars、Structural Design、Space Management） | 船體從設計到零件製造與組立 |
| 設計 | Outfitting Design | 圖形驅動的主要建模模組，建立全尺寸 3D 模型，含設備、管路、鋼構；可查干涉、出報表、在不離開 Design 的情況下預覽等角圖 |
| 設計 | SPOOLER | 把管路拆成可預製的管段（spool），再用 Isodraft 出圖 |
| 繪圖 | Outfitting Draft、Marine Drafting、Isodraft | 帶尺寸與註記的圖；標籤隨 3D 位置移動，尺寸在更新圖面時重算；Isodraft 自動出等角圖與材料表 |
| 目錄與規格 | PARAGON、SPECON、PROPCON | 建立元件目錄、元件規格（Specification）、材料性質資料庫 |
| 專案管理 | Monitor | 查使用者與存取權、改自己的密碼、切換使用者、批次與簡單訊息；Free／General 使用者的權限不同；**專案出問題導致其他模組載入失敗時，系統會自動載入 Monitor 供診斷** |

> **專業提醒：** 最後一點對開發者很實用：登入後突然只看到命令列介面的 Monitor，多半不是你選錯模組，而是目標模組載入失敗。先讀錯誤訊息，再找管理員，不要反覆登入。

## 1.3 資料庫與資料存放

### 1.3.1 專案與 12 種資料庫

官方的說法：一個專案由一組資料庫構成，共 12 種，每個模組需要其中一或多種，且只有 Project Administrator 能建立新資料庫。專案、DB 與 MDB 的關係會在[第 3 章](ch03_project_database_zh-TW.reading.html)深入說明（DB 類型見該章 3.3 節），這裡先給官方的用途描述，並加上「開發者通常何時碰到」。

| 類別 | 資料庫 | 官方用途摘要 | 開發者何時碰到 |
|---|---|---|---|
| 設計與繪圖 | Outfitting Design | 建立全尺寸 3D 模型所需的全部資訊（設備、管路、結構、支架） | 幾乎每個工具 |
| 設計與繪圖 | PADD | 圖面的圖形內容與註記、尺寸，專屬 Draft | 出圖工具（見[第 28 章](ch28_draft_admin_production_zh-TW.reading.html)） |
| 設計與繪圖 | ISOD | Spooler 產生的管段圖 | 管段與等角圖（見[第 20 章](ch20_isodraft_zh-TW.reading.html)） |
| 2D 設計 | SCHEMATIC | 2D 系統圖資料與連接關係 | 系統圖整合 |
| 2D 設計 | ENGINEERING | 傳統工程資料 | 同上 |
| 參考 | CATALOGUE | 標準元件的尺寸、可接合關係、螺栓、Specification（壓力、溫度條件） | 讀元件資料 |
| 參考 | DICTIONARY（Lexicon） | **UDA 與 UDET（使用者自訂元素型別）定義** | 用到冒號開頭的屬性 |
| 參考 | 管理 | SYSTEM | 每個 Project Folder 只有一個；DB 清單、使用者與密碼、Team、可用模組、存取控制 | 權限問題時 |
| 管理 | COMMS | 誰在用哪個模組、哪些 DB 是目前的；每位使用者有自己可寫的區塊，別人可讀 | 查「誰佔用」時 |
| 管理 | MISC | 使用者間訊息與跨資料庫巨集；**同一時間只有一個人能以寫入模式開啟**，但多人可讀 | 傳訊息、跨庫巨集時 |
| 管理 | TRANSACTION | 只在安裝 Global 產品時才有，記錄全域命令進度 | 分散式環境 |

DICTIONARY 的 UDET 值得一提：官方例子是把一個 `EQUI` 命名為 `:PUMP` 或 `:VESSEL`，也就是**型別名稱的客製化**，與 UDA 同屬 Lexicon 管轄。

### 1.3.2 設計資料庫是一棵樹

> 〔公開版未收錄：AVEVA 官方產品截圖〕設計資料庫階層：WORLD、SITE、ZONE 為各專業共通，其下依專業分為 STRUCTURE、EQUIPMENT、PIPE

*圖 1-2　設計資料庫的簡化階層。虛線以上各專業共通，虛線以下依專業而定；虛線框為選用層。（AVEVA 官方文件截圖，僅供內部教學）*

官方強調：**所有元素都被另一個元素擁有，只有 WORLD 例外**。被擁有的稱為擁有者的 Member。刪除一個 ZONE，底下全部連帶刪除。官方並指出 SCHEMATIC、ENGINEERING、CATALOGUE、PADD、ISOD、Lexicon、PROPERTIES 也都是階層結構。

簡要整理官方的階層描述：WORLD 是資料庫剛建好時唯一的元素（名稱 `/*`，見 1.4.1）；其下是 SITE（大範圍的集合，不必對應實際區域）與 ZONE（常用來把同類東西放一起，例如一個放管系、另一個放設備），ZONE 以下依專業而定。設備 `EQUI` 由圖元（`NOZZ`、`BOX`、`CYLI`、`PYRA` 等）組成，可直接擁有圖元，或透過選用的 `SUBE` 進一步分割；結構以**純管理性**的 `STRU` 擁有 `FRMW`（可再分 `SBFR`），其下是型鋼 `SCTN`、板 `PANE`、曲線型材 `GENSEC`，型鋼尺寸由 Section Specification 引用目錄；管路以 `PIPE`（像流程圖上的一條線）擁有 `BRAN`（有已知起訖點的段落，起點稱 Head、終點稱 Tail），其下是 `GASK`、`FLAN`、`TEE`、`VALV`、`ELBO` 等管件，由 Piping Specification 引用目錄（100 mm 彎頭每次都取同一筆目錄資料）。各層的用途與型別對照見[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html) 4.2 與 4.3 節；結構見[第 10 章](ch10_assembly_structural_zh-TW.reading.html)，管路見[第 19 章](ch19_pipework_zh-TW.reading.html)。下圖是官方的 Pipe／Branch 範例。

> 〔公開版未收錄：AVEVA 官方產品截圖〕一條 Pipe 含兩個 Branch 的範例：Branch 1 向上、Branch 2 水平延伸

*圖 1-3　官方範例：一條 Pipe 由兩個 Branch 構成，Branch 1 從 Branch 2 分出。（AVEVA 官方文件截圖，僅供內部教學）*

階層與元素型別的完整對照見[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html)與[第 7 章](ch07_data_model_reference_zh-TW.reading.html)，本章只做入門層次的介紹。

## 1.4 屬性：元素的固定欄位

### 1.4.1 屬性基礎（官方的 `CYLI` 範例）

官方以圓柱 `CYLI` 說明：每個元素都有一組固定屬性，有些是各元素共通，有些依型別而不同，例如 `CYLI` 有 `HEIGHT` 與 `DIAMETER`，`BOX` 則由 `XLENGTH`、`YLENGTH`、`ZLENGTH` 決定大小。

> 〔公開版未收錄：AVEVA 官方產品截圖〕圓柱的 Height、Diameter 與長方體的 Xlength、Ylength、Zlength 屬性示意

*圖 1-4　`CYLI` 與 `BOX` 的尺寸屬性。（AVEVA 官方文件截圖，僅供內部教學）*

官方列出 `CYLI` 建立時的預設屬性，用來理解「建立元素時系統會塞一組預設值」：

| 屬性 | 預設值（官方） | 備註 |
|---|---|---|
| `NAME` | 有指定則為該名稱，否則顯示層次描述 | 見下 |
| `TYPE` | `CYLI` | 元素型別 |
| `LOCK` | false | 設為 true 後不可修改，直到解鎖 |
| `OWNER` | 擁有者名稱或層次描述 | Owner／Member 關係 |
| `POSITION` | `N 0mm E 0mm U 0mm`，相對擁有者 | [第 5 章](ch05_coordinates_geometry_zh-TW.reading.html)會深入 |
| `ORIENTATION` | `Y is N and Z is U`，相對擁有者 | 同上 |
| `LEVEL` | `0 10`（表示等級） | 預設 0 到 10，可超出；例如鋼構可只顯示中心線或完整斷面 |
| `OBSTRUCTION` | 2 | 2 = 硬、1 = 軟（通道、維修空間）、0 = 不阻擋 |
| `DIAMETER`、`HEIGHT` | 0 mm | 圓柱尺寸 |

`NAME` 的幾條規則值得單獨記，因為寫工具時最常踩：

- 每個元素都有**不會改變的系統參考號（Refno）**，名稱只是另加的識別；系統內部用參考號，並維護名稱對參考號的對照表。
- 所有名稱以斜線 `/` 開頭，斜線是名稱的一部分；表單在你按 Enter 時自動補上，Design Explorer 與 Members List 不顯示斜線。
- 名稱**不可含空白、區分大小寫**（`/E1302A`、`/E1302a`、`/e1302A` 是三個不同名稱），且在資料庫中唯一。
- WORLD 的名稱是 `/*`。

名稱、參考號與「型別加序號」三種識別方式的比較，會在[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html) 4.4 節說明。

### 1.4.2 UDA 與偽屬性

| 類別 | 官方定義 | 辨識方式 | 可否修改 |
|---|---|---|---|
| UDA | 由系統或專案管理員在 Lexicon 模組定義並指派給元素；可能是公司或專案專用，也可能已有預設值 | 屬性名稱**前面有冒號**，例如 `:COLOUR`（`:HEIGHT` 為一般屬性，官方並列對照） | 與其他屬性相同 |
| 偽屬性（Pseudo-Attribute） | 系統為特定目的設定的屬性 | 見下方「Display Pseudo Attributes」 | **使用者不能改** |

命令列查法會在[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html) 4.7.4 說明。官方介面說法：Attributes 選單裡有 Display UDAs、Display Standard Attributes、Display Pseudo Attributes 三個選項，依序切換要看哪一類（細節官方只寫參見 LEXICON User Guide）。

### 1.4.3 Attributes window

從主選單 `Display > Attributes` 開啟，顯示**目前選取元素（CE）**的屬性，依你的存取權決定哪些可改。視窗可停靠、調整大小、或浮動在 3D 視圖上。預設是兩欄表格：左欄屬性名、右欄值。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Attributes of /E1301 視窗：Track CE 勾選，列出 RefNo、Name、Type、Lock、Owner 等屬性

*圖 1-5　Attributes window 的預設表格顯示。Lock 是核取方塊（布林屬性），Track CE 讓視窗跟著 CE 變。（AVEVA 官方文件截圖，僅供內部教學）*

| 操作 | 官方步驟或說明 |
|---|---|
| Track CE | 勾選後視窗內容跟隨 CE 變動 |
| 布林／有值清單 | Value 欄勾選＝true、取消＝false；有清單的點箭頭選值 |
| 超連結屬性 | 在該屬性雙擊，開啟關聯的 URL、檔案或文件 |
| Attribute Type Selection | 用視窗上的 Attribute Filters 圖示開 Filter 視窗，預設所有屬性型別都勾選；取消不要看的型別，**選擇在 CE 改變後仍保留**；也可用 Text Filters 設自訂條件 |
| Category Filters | 圖示表示是否已套用分類篩選；點它開 Modify Category Filters |

> 〔公開版未收錄：AVEVA 官方產品截圖〕依分類顯示的 Attributes window：Connection、Construction、Default、Design、General、Mass Properties 等分類各列出項數

*圖 1-6　切換成 Categorised 顯示：屬性依分類分組，分類在 Lexicon 設定，沒分類的由系統指派 draft 分類。（AVEVA 官方文件截圖，僅供內部教學）*

### 1.4.4 Attributes 選單（右鍵）

在視窗不同位置按右鍵，可用的選項不同。官方列出的項目：

| 選項 | 作用（官方） | 備註 |
|---|---|---|
| Navigate To | 僅在選到**參照屬性**或**超連結屬性**時可用；超連結會另開視窗 | 參照屬性即[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html) 4.5.3 的「外鍵」 |
| Set Attribute Value to CE | 讓參照屬性把 CE 設為該屬性值 | 相當於「跳過去」 |
| WRT World | 位置、方向、姿態預設相對於擁有者；此選項可改為相對其他元素 | 對照[第 5 章](ch05_coordinates_geometry_zh-TW.reading.html)的 WRT |
| Display P-Points | CE 有 P-Point 時在視窗顯示 |  |
| Categorised／Alphabetical | 分類或字母排序 | 分類在 Lexicon 設定 |
| Modify Category Filters | 勾選要顯示的分類，可 Uncheck all／Check all | **只保留於本次工作階段** |
| Manage Category Filters | 開 Manage Category Filters by Element Type 視窗 | 官方只給畫面，未詳述 |
| Columns > Description／Data Type；Settings > Suppress "unset"／"Nulref" | 多加說明欄、資料型別欄 | 開發者看欄位型別很有用 |
| Export to Excel | 匯出到指定檔案 | 建議配合 Data Type 欄，一併存檔 |

> **專業提醒：** 新手最常問「為什麼我看不到某個屬性」。先檢查：Attribute Type 篩選、Category Filters，以及管理員是否在 Lexicon 設成不顯示。

## 1.5 進入 Marine 與 GUI 基本操作

### 1.5.1 登入表單

官方假設使用者已有有效授權、已安裝軟體、知道如何啟動模組。從開始功能表可選「直接進入某模組」或走預設的 Monitor 入口（官方路徑 `Start > All Programs > AVEVA Marine > Design > PDMSMarine 12.1 (Monitor)`〔待核對〕）。登入表單：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Monitor login 表單：Project、Username、Password、MDB 與 Module 欄位，及四個核取方塊

*圖 1-7　Monitor login 表單。Open Read Only 與 Restore Views 在尚未選項目前呈灰色。（AVEVA 官方文件截圖，僅供內部教學）*

| 欄位／選項 | 官方行為 |
|---|---|
| Project | 下拉清單，顯示專案識別碼（若有定義），否則顯示三字母專案代碼 |
| Username | 選專案後會自動帶入相關項目；清單可顯示括號內的註解；若專案使用 **Windows 驗證**，清單只含目前 Windows 使用者可用者，且不需密碼（欄位反灰）；輸入時清單依開頭字元過濾 |
| Password | **區分大小寫** |
| MDB | 下拉清單；註解在括號內；若資料存取授權不足，MDB 中部分資料庫不會開啟，啟動時會跳錯誤視窗 |
| Module | 選要啟動的模組 |
| Integrate Engineering and Schematics | 與 Engineer、Diagrams 並用時，決定 3D 模組是否看得到工程與系統圖資料（勾選＝唯讀可見） |
| Open Read Only | 勾選後**所有資料庫唯讀開啟**；要修改資料請確認沒勾 |
| Restore Views | Design、Draft 可還原上次的圖形視圖狀態 |
| Change Password | 勾選後在登入完成時出現變更密碼視窗；官方寫密碼**不得超過 6 個字元**〔12.1 實際限制待核對〕；管理員設了 `PASSWORDLOCK ON` 時此選項反灰，須請管理員改 |
| Restore Default Layout | 預設會還原上次的主圖形視窗與 Explorer 佈局；勾此項則在登入完成後確認刪除儲存的狀態、回到預設佈局 |

佈局狀態存在使用者 Documents and Settings 底下的一對目錄（官方舊路徑，Windows 新版本的實際位置待核對）。直接進入個別模組時選項較少，意義相同；進入 Engineering、Diagrams 也類似，只是沒有 Integrate 核取方塊。

### 1.5.2 離開、說明與其他設定

| 主題 | 官方說明 |
|---|---|
| 離開 | `Design > Exit`。有未儲存變更時詢問是否存入資料庫，選 Yes 等於 `SAVEWORK` 後 `QUIT`；沒變更或已儲存則只要求確認離開；離開後回到你啟動時的作業系統位置 |
| 說明 | 主工具列 `Help > Contents／Search／About`。About 顯示版本與授權對象；**Additional Info** 列出 PMLLIB 與 PMLUI 搜尋路徑下所有 `version.dat`；**Appware** 掃描所有 appware 是否被改過，結果列在 Appware Changes from Installed；兩者都有 Copy Info |
| 國際化 | 預設可用 Latin-1 語言；另支援遠東群（日、簡中、韓、**繁中**）、Latin-2、Latin-Cyrillic；除「一種遠東語言與英語混用」外，不支援語言群混用；需對應版本 Windows 與鍵盤，並設 Regional Options〔繁中實際設定待核對〕 |
| 客製化 | 以 PML 設計自己的介面；官方明說自訂巨集脫離 AVEVA 控制，可能與新版不相容，**AVEVA 只對自己控制的產品提供完整支援**，公司內部要有客製政策 |

### 1.5.3 滑鼠、表單與選單

| 滑鼠按鍵 | 官方行為 |
|---|---|
| 左鍵 | 圖形視圖：點設計元素使其成為 CE（要在下一步操作的元素）；選單序列：拖曳至選項放開時執行；表單上依元件而定 |
| 中鍵 | 主要用於操作圖形視圖 |
| 右鍵 | 開啟圖形視窗專屬選單或表單上列示項目的選單 |

表單元件與慣用法：

| 元件 | 重點 |
|---|---|
| Text box | 輸入後要按 **Enter 確認**；未確認的欄位以**黃色背景**標示；有些只收文字或只收數字，型別錯誤不被接受；開表單時第一欄為作用中 |
| Drop-down list | 選一個選項，顯示目前選擇 |
| Option button | 同組互斥，選一個自動取消其他 |
| Check box | 彼此獨立，可任意組合 |
| Scrollable list | 單選或多選；多選清單再點一次可取消 |
| Action button | `OK`（接受並關閉）、`Cancel`（取消並關閉）、`Apply`（接受並保留表單）、`Reset`（取消變更並保留表單）、`Dismiss`（關閉並保留設定）〔五種按鈕的圖示在官方截圖，名稱依該表單標示為準〕 |

選單選項有三種形式：獨立選項（立即執行）、**後面有三個點**（開表單）、**後面有箭頭**（開子選單）。官方文件用 `>` 縮寫選單路徑，例如 `Position>At>Explicit`。本課程沿用同樣寫法。

### 1.5.4 工具列、狀態列、Alert、停靠

- **工具列**在主選單列正下方，有些模組有數條；滑鼠停留顯示提示；在工具列或選單列按右鍵，可勾選要顯示的工具列。
- **狀態列**顯示應用程式正在做什麼，也會提示下一步需要的輸入。官方特別提醒：**系統似乎在等你時，先看狀態列。** 若提示允許重複任意次數（例如用游標連續挑選項目），完成後必須按 **Esc** 表示結束。
- **Alert 表單**顯示錯誤、提示與確認請求。錯誤視窗的 **Save Support Info** 可把擴充訊息存成檔案。
- **停靠**：Design Explorer、My Data 等關鍵表單，以及所有選單列與工具列都可停靠。配置會在結束時儲存、下次還原，切換模組時也盡量維持。

| 物件 | 能做什麼 | 操作 |
|---|---|---|
| 工具列 | 停靠任一邊或浮動 | 雙擊移動把手，或拖離邊緣即浮動；拖標題列到視窗邊緣，或雙擊標題列，可回到先前停靠位置 |
| 選單列 | 停靠任一邊，**不能浮動** | 拖曳移動把手到另一邊 |
| 表單 | 浮動（可任意調整大小）、貼附主視窗任一邊、貼附另一已停靠表單的任一邊、與其他表單疊成頁籤、AutoHide | 拖標題列；拖曳時出現 Docking Tool |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Docking Tool 十字圖示：上、下、左、右停靠與中央（疊成頁籤）

*圖 1-8　拖曳表單時出現的 Docking Tool；放在中央會與目標表單疊成頁籤。（AVEVA 官方文件截圖，僅供內部教學）*

拖曳表單時，滑鼠移到允許位置會顯示半透明色塊預覽最終位置；放到 Docking Tool 中央則與另一表單疊成頁籤，底部有頁籤切換。**AutoHide**：點標題列上的圖釘圖示，表單收成邊緣頁籤，點頁籤再展開。

### 1.5.5 命令視窗

官方態度很明確：**一般用途用 GUI，命令是讓你省時間與自動化**。要建立元素一律用 GUI（官方原文：「You should always use the GUI to create elements」）。簡單的查詢用命令稍快，例如 `Q MEM`（列出 CE 的成員）、`Q ATT`（列出 CE 的屬性）。

| 項目 | 官方說明 |
|---|---|
| 開啟 | `Display > Command Window` |
| 輸入 | 在文字框輸入後按 Enter；清單保留約**最近 1000 行**輸出；上下鍵翻閱歷史命令；雙擊任一行可複製為作用中行 |
| 右鍵選單 | Copy；Paste（貼上的每一行當作獨立命令執行）；**Paste as Macro**（先寫成暫存檔再當巨集執行，命令多時效能較好）；Font Size（Large／Medium／Small）；Clear |
| 檔名 | PDMS 檔名可達 1024 字元、可含空白，例如 `SLIST 'C:\Program files\Aveva\a temporary file.txt'` |

命令列的完整使用見[第 2 章](ch02_architecture_zh-TW.reading.html) 2.8 節與[第 33 章](ch33_pml_database_zh-TW.reading.html)；自訂表單與選單見[第 34 章](ch34_pml_forms_addins_zh-TW.reading.html)。

## 1.6 基本操作：查詢、導覽、修改與新手常用視窗

官方把所有模組中的工作歸結為：告訴系統**要存取哪個資料庫、資料庫階層中哪些元素、要對內容做什麼變更**（新增、更改、讀取、刪除）。

### 1.6.1 查詢與目前元素

- 每個模組有 **Query** 下拉選單（範圍依模組而異）。可查的主題包括：目前使用者、模組與資料庫的使用情形；工作站與行程的唯一碼（可用來產生不衝突的暫存檔名）；命令選項的目前設定；資料庫部分內容；符合條件的元素。
- **不是所有查詢都能用 GUI**，其餘須用 `QUERY` 命令。
- **CE（Current Element）**：你在資料庫中所站的元素。**Current List Position（目前清單位置）**：元素的 Member List 是依編號排序的指標清單，除了站在 CE，系統也認為你在其中一個指標上。你在資料庫中移動時，這兩者持續更新。
- 看 CE 與其成員：點 Design Explorer 中 CE 旁的展開方塊，或用命令 `Q CE`、`Q MEM`。

### 1.6.2 導覽與修改

| 工具 | 官方描述 |
|---|---|
| Design Explorer | 圖形化樹狀檢視（點 `+`、`-` 展開收合），圖示代表元素型別；可導覽、查屬性、改名、刪除、複製貼上；可透過 Drawlist 管理顯示；CE 是樹上反白項，也顯示在主選單列的 **History** 清單（最近造訪項目）。進入 Design 時預設顯示，關掉後用 `Display > Design Explorer` 叫回 |
| Members List | 取代前的舊工具，`Display` 選單仍可開。上下箭頭在 CE 同層級上移動（站在 EQUI 時移到下一個 EQUI）；`Goto > Owner` 到擁有者；`Goto > Reference` 依 CE 型別給選項（EQUI 只能到其 ZONE；`NOZZ` 可透過 `Catref` 進入 Catalogue） |
| My Data | `Display > My Data`。把元素分組成集合並一次操作，**在 Design、Draft、Spooler 等模組之間保留**，也跨工作階段；**依使用者與專案**儲存；`PDMSUSER` 目錄若多人共用則大家看到同樣資料 |

**Explorer 篩選器：** 預設一組資料庫篩選器，由「核心篩選器」組成，可在各 Explorer 開關；**關閉時顯示完整階層**。每個 Explorer 同一時間只有一個系統篩選器作用；另有預設篩選器在 `Setting > Explorer` 視窗，不論系統篩選器是否開啟都可獨立切換。篩選器由五類規則組成：

| 規則 | 作用 | 優先序（低到高） |
|---|---|---|
| Shows | 顯示指定型別及其祖先 | 1 |
| Show Descendants | 顯示指定型別及其後代與祖先 | 2 |
| Skips | 只略過該元素本身，祖先與後代仍出現 | 3 |
| Hide Below | 隱藏指定型別的後代 | 4 |
| Hides | 隱藏指定型別及其後代 | 5 |

官方的預設篩選器分 Piping、Structural、Equipment、Administrator、Hangers and Supports。各 Explorer 的組成不同：Design、Draft、Spooler 的 Design DB 都有 Piping（Show `Branch` 與後代、`Framework`、Nozzles、Hangers；Hide below Bound、Drawing、sections、Panels 與各 world；Skip Sub-Equipment、Skip Template）；Design 另有 Structural、Equipment、Hangers & Supports 與船體類（Curved Hull、Hull Panels、Hull Reference Model、Space Arrangements）；Draft 的 PADD DB 有 General User 與 Administrator（後者 Show 各 Library 後代）；Isodraft 的 Design DB 只有 Pipe（Show Branches）；Spooler 與 Isodraft 的 Fabrication DB 沒有篩選器。完整勾選項目見官方 *Core Filters for Explorers* 頁。

> **專業提醒：** 「樹上少了元素」不一定是被刪除。先關掉 Explorer 篩選器看完整階層，再判斷是被 Hides、Hide Below 還是 Skips 蓋掉。例如 Piping 篩選器預設 Skip Sub-Equipment，設備底下的 SUBE 看起來「不見了」，其實它的後代仍會出現。

## 1.7 Drawlist：控制 3D 視圖裡有什麼

右鍵點 3D View 工具列的 Drawlist 按鈕，選 `Drawlist` 開啟。Drawlist 表單**列出 3D 視圖中顯示的項目名稱**。從 Design Explorer 拖元素進 3D 視圖就會自動加進 Drawlist；可加單一元素，也可整個 ZONE 或 SITE。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Drawlist - 3D View 表單：Drawlist、Graphical Selection、Primitives 頁籤，群組列，以及 Colour、Edges、Translucency 等顯示設定

*圖 1-9　Drawlist 表單與 Drawlist 按鈕的右鍵選單。下方 Select CE in list、Add CE to drawlist、Remove selection 三個按鈕。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 官方說明 |
|---|---|
| 分組與篩選 | 把欄位標題拖到指定位置可分組；清單上方的小工具可用右鍵選單篩選 |
| 右鍵選單 | **Navigate To**（設為 CE）、**Hide**（暫時從顯示移除）、**Show**、**Remove**（自 Drawlist 移除）、**Add to My Data**（也可拖放）、**Export to Excel** |
| 多選 | Windows 慣用法（Shift、Ctrl）；視覺屬性變更套用到所有選取項目 |
| 三個按鈕 | **Add CE to drawlist**、**Select CE in list**（定位 CE 在清單中的位置）、**Remove Selection**（自 3D 視圖移除所選） |
| 預設工具列 | 有三個圖示：把 CE 加入、把 CE 移除、清空整個 Drawlist |
| 視覺屬性 | **Colour**（調色盤）、**Edges**（顯示或取消邊線）、**Translucency**（0% 為實色、100% 全透明） |
| 注意 | CE 以「目前元素顏色」顯示，**直到另一個元素成為 CE 前不受顏色變更影響**；改頂層元素的視覺屬性時，其下層元素一併修改；半透明元素建議開邊線 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Primitives 頁籤：HPANEL 物件的個別圖元 HBRCKT 與 HBRFLA

*圖 1-10　Primitives 頁籤可逐一控制某物件底下圖元的顯示。（AVEVA 官方文件截圖，僅供內部教學）*

Drawlist 按鈕本身左鍵、右鍵功能不同：

| 動作 | 官方說明 |
|---|---|
| 左鍵點 Drawlist | 設定圖形視圖，使**下一個挑選的 3D 物件被隱藏**。目的是多次挑選（例如以兩點定義剪裁盒）中，第二點的目標被擋住時，暫停序列、隱藏擋住的物件後再繼續 |
| 平常隱藏 | 在圖形視圖中右鍵即可隱藏物件，但多次挑選期間無法使用 |
| 重新顯示 | 右鍵 Drawlist 按鈕：**Show Last Hidden Object(s)**（本工作階段最近隱藏的，且仍在 Drawlist 中）、**Show All Hidden Objects**、**Show Hidden Objects**（開表單選擇） |
| Local View | **New Local View of Selection**：以圖形選取的物件建立有自己 Drawlist 的新視圖；第一次從 Design 主選單開視圖時顯示 **global drawlist** 的內容 |
| Clone View | **New Clone View**：複製目前視圖，共用同一份 Drawlist（global 或 local 視產生方式而定） |

> **專業提醒：** 官方有一條容易漏看的行為：**復原（Undo）刪除的元素會把它加回 global drawlist，但不會加回原本含它的 local drawlist**。若你的使用者抱怨「復原後元素在別的視圖不見了」，這是原因。Draft 的 Drawlist（`IDLI`）是另一件事，見[第 28 章](ch28_draft_admin_production_zh-TW.reading.html)。

## 1.8 Outfitting Search Utility

`Display > Search Utility` 開啟 Search 表單，在**所有圖形應用程式**中搜尋模型項，並把結果列在表格。這是新手最該先學會的工具之一：它取代「在 Explorer 裡一層層展開找」。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Search 表單：Search For、Search Filters、Modified、Within Volume、Attribute Filters、Saved Searches 各區

*圖 1-11　Search 表單。注意 In Database 目前選 Catalog，Within Volume 可用 FR／LH／LV 或世界座標輸入。（AVEVA 官方文件截圖，僅供內部教學）*

### 1.8.1 搜尋條件

| 區塊 | 官方行為 |
|---|---|
| Name Contains | 名稱含指定字串，**區分大小寫** |
| Element Type | 可輸入多個型別，以空白、逗號或分號分隔，如 `EQUI PIPE, NOZZ; TEE`；下拉選 `[ALL]` 為目前範圍所有型別；**搜尋前此欄必須有合法值**；歷史記憶於本工作階段，可 Clear History |
| New tab | 預設不勾，結果都進 `Search Results 1`；勾選則每次搜尋開新編號頁籤；**`Search Results 1` 不能關**；其他頁籤右鍵 `Close Tab`；右鍵 `Synchronise Search with Tab` 可把該結果的搜尋參數回填到 Search 視窗 |
| Beneath Element | 搜尋上限（天花板），預設是 WORLD（`/*`）；可輸入元素，或按 **CE** 把目前元素設為天花板；下拉歷史可清除 |
| In Database | 列出你可用的資料庫；切換資料庫時若目前項目不在其中，上限重設為 WORLD |
| Element List／Modified | 可選預定義元素清單（依模組而異）；可依修改日期過濾，並在結果多顯示修改時間 |
| Within Volume | 勾 In Volume 後可選 **Of Element**（某模型元素的體積內，可按 CE 帶入）或 **Explicit Volume**（以 X、Y、Z 設兩個對角點）；**Wholly within** 或 **Wholly & Partially within** 決定完全或部分在體積內 |
| Attribute Filters | 一或多個屬性條件，**同時滿足全部條件**才算命中；條件套用到列出的每個元素型別 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Attribute Filters 網格：AREA Equals 2 且 BUIL Equals True

*圖 1-12　Attribute Filters：Attribute、Operator、Value 三欄，多個條件為「且」。（AVEVA 官方文件截圖，僅供內部教學）*

加條件：點 **Add Filter**，輸入合法屬性，在 Operator 欄接受建議或從下拉選別的，再填 Value。官方特別說明兩個運算子：

| Operator | 官方例子 | 意義 |
|---|---|---|
| In the List | `AREA`、`In the List`、`0 1 3` | 值以空白分隔，命中 AREA 等於 0 或 1 或 3 者 |
| In the Range | `AREA`、`In the range`、`1 10` | 兩個數值（上下限，含邊界），命中 1 到 10 之間（含）的值 |

條件加入後若改屬性，Operator 與 Value 欄會跟著更新；**Delete Filter** 刪除所選列。

### 1.8.2 Saved Searches 與結果

- **Saved Search**＝搜尋條件＋結果欄位。下拉選名稱按 Search 即執行並回填條件；用 `Create "Saved Search" Based on Current Search Criteria` 存檔（問名稱與位置，預設可存到本機 local settings 目錄）；`Delete Selected Saved Search` 刪除，直接刪本機檔案則下次啟動不再載入；另有 Saved Searches 工具列可不開主表單直接執行。已存搜尋在以搜尋名稱為標題的新頁籤開啟（位置不同於 Local Settings 時標題為 `Location/Name`）。
- **結果表格**（`Display Search Results` 連結，或 `Display > Search Results`）：每欄是一個屬性或合法的 Outfitting 表示式；選一列或多列可執行動作，例如在 Design 中**拖放進 3D 視圖**；所有選單動作由 AVEVA 可客製的選單建置程式定義。右鍵欄標題＝一般功能選單，右鍵結果列＝針對所選項目的選單。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Search Results 視窗及右鍵選單：Copy、Paste、Navigate To、3D View（Add、Add Only、Add Connected、Add Within Volume、Remove、Highlight）、Add To My Data

*圖 1-13　Search Results 的右鍵選單。3D View 子選單的 Add Connected、Add Within Volume 與 Reference List 相同。（AVEVA 官方文件截圖，僅供內部教學）*

| 結果表格功能 | 官方說明 |
|---|---|
| Column Setup | 白色空白處右鍵開啟，可新增、修改、刪除屬性欄；**Add Standard Attributes** 加入 CE 的所有標準屬性；Visible 決定顯示（至少留一欄）；**欄位順序變更要等下次搜尋才生效** |
| Clear Results | 選一列、右鍵欄標題、選 Clear Results |
| 設定與編輯 | Enable Group Sorting／Filtering／Column Summaries／Column Sort；Interaction Mode 有 **Read Only**、**Single Cell Edit**、**Bulk Cell Edit**；Feedback Colors 與 Reset Cell Feedback 控制編輯後的高亮；Refresh 重新同步 |
| Export to Excel | 存成 `.xls` 檔案 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Column Setup 視窗：Position、Expression、Heading、Visible 欄位，及 Add Column、Add Standard Attributes、Delete Selected Columns

*圖 1-14　Column Setup：每欄是一個屬性名稱或 Outfitting 表示式。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 官方允許把結果欄設為「表示式」，也允許 **Single／Bulk Cell Edit**。這代表搜尋結果表格可以直接改屬性，等同在資料庫寫入。唯讀探索時請維持 **Read Only** 模式（也是官方預設行為之一：唯讀模式下 Tab 在列間移動）。編輯是否真的寫入還取決於你的存取權與認領狀態（見[第 3 章](ch03_project_database_zh-TW.reading.html)）。

## 1.9 GUI Grid Data：所有表格通用的操作

Drawlist、Search Results、Reference List 等表單的資料，都是同一種**網格控制項**。官方提醒：每個應用程式客製的方式不同，**不是所有功能在每個網格都有**。下圖是 PIPE 與 EQUI 混合的典型網格，注意 `POSITION` 對 PIPE 無效、`PSPEC` 對 EQUI 無效，這些儲存格以紅色驚嘆號圖示標示。

> 〔公開版未收錄：AVEVA 官方產品截圖〕典型資料網格：Name、Type、Description、PSPE 欄；EQUI 列的 PSPE 為紅色驚嘆號

*圖 1-15　網格中的「該型別沒有此屬性」以圖示表示，不是空值。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 操作 |
|---|---|
| 鍵盤 | 單格／批次編輯模式用 `Tab` 往下一格、`Shift+Tab` 往前；**唯讀模式** `Tab` 往下一列 |
| 選取 | 唯讀：點任一處選整列；單格編輯：點儲存格進入編輯；批次編輯：**雙擊**進入編輯，單擊選儲存格，Ctrl／Shift 或拖曳選多格；批次模式右鍵有 **Fill Down、Fill Up、Copy、Paste**，對選取的所有儲存格生效；要選整列，點最左的 row selector 欄 |
| 分割 | 拖曳垂直捲軸頂端與水平捲軸左端的 splitter bar 可切成多個子網格；拖回頂端與左端還原 |
| 釘選 | 有 row selector 時，點圖釘把列固定在頂端（黃色顯示）；欄標題的圖釘把欄固定在左側；再點取消 |
| 排序 | 點欄標題排序，再點反向，箭頭顯示方向；**一次只能排一欄**（想多欄排序請用群組排序） |
| 欄位篩選 | 欄標題下的篩選列：游標停留顯示下拉箭頭；清單列出欄位所有值加 **All**、**Blanks**，取消勾選即排除；多值或含文字篩選時顯示 `Custom`；**Clear Filter**（欄右側）清單欄，網格左側的清除全部；**Text Filters** 開 Custom Filter 視窗，可 Add／Delete 條件，並選 **All**（全部符合）或 **Any**（任一符合） |
| 群組排序 | 把欄標題拖進 Group Sort Area 依該欄分組，可拖多個形成多層；把標籤拖回標題列移除 |
| 其他 | 右鍵 **Export to Excel**；**Import from Excel**（若提供，檔案**第一列必須是欄標題**，其下為資料）；Print Preview |

> 〔公開版未收錄：AVEVA 官方產品截圖〕群組排序：先依 TYPE、再依 AREA 分組的網格，上方為 Group Sort Area

*圖 1-16　Group Sort：先 TYPE 後 AREA 兩層分組，每組顯示項目數。（AVEVA 官方文件截圖，僅供內部教學）*

## 1.10 Reference List

`Display > Reference List` 開啟。視窗**自動列出 CE 所參照的元素**：例如 CE 是設備，會列出連到該設備任何噴嘴的管路；選到某個噴嘴，清單就變成接到那個噴嘴的管。

| 項目 | 官方說明 |
|---|---|
| 列出規則 | 明顯的「實體」連接參照；由 `HREF`、`TREF`、`CREF` 屬性**後代**得到的元素；對 Group 元素則列出 Group 成員 |
| 欄位 | Name、Type；點標題排序，再點反向；空白處右鍵 `Arrange By` 同效果。兩欄**唯讀**，游標停在名稱上的提示顯示名稱、型別與描述 |
| 右鍵：Navigate To | 在 Design Explorer 選取該元素並設為 CE |
| 右鍵：3D View | 僅 Design 資料庫元素有；子選單 **Add**（只加所選）、**Add Connected**（加所選與其連接的所有元素）、**Add Within Volume**（加所選與佔同一體積的元素）；加入 3D 視圖同時加進 Drawlist；也可直接拖放進 3D 視圖 |
| 右鍵：Add To My Data | 加入 My Data |

> **專業提醒：** Reference List 由 `HREF`、`TREF`、`CREF` 推得，是檢查管路連接的快速工具：站在噴嘴上看清單是否出現預期的管。這些屬性的語意沿用[第 17 章](ch17_outfitting_zh-TW.reading.html)與[第 19 章](ch19_pipework_zh-TW.reading.html)〔待核對〕。

## 1.11 產品線與詞彙

### 1.11.1 Product Range

官方把 AVEVA 產品組成「AVEVA Plant（工廠）」與「AVEVA Marine（船舶）」兩大套件，Marine 定位是設計與資訊管理系統，涵蓋「從概念到交付」的整個造船流程，並宣稱 40 年來為造船業事實標準。官方將產品分三類：

- **Engineer：** Initial Design（船型、艙室、靜水力）、Diagrams、Instrumentation、P&ID、Schematic 3D Integrator、Schematic Model Manager。
- **Design：** Hull Structural Design、Hull Finite Element Modeller、Hull Detailed Design、Outfitting、Room Design、Marine Drafting、Assembly Planning、Hull Weld Planning、Mechanical Equipment Interface、Multi-Discipline Supports、Cable Design、Laser Model Interface、Design Reuse。
- **Manage：** Global、Review、ReviewShare、Clash Manager。

與本課程章節的對照：Initial Design／Hull 系列見[第 9 章](ch09_hull_modelling_zh-TW.reading.html)；Outfitting 見[第 17 章](ch17_outfitting_zh-TW.reading.html)；Multi-Discipline Supports 見[第 19 章](ch19_pipework_zh-TW.reading.html)的管支架部分。**哪些產品你們公司有授權，以合約為準，標〔待核對〕。**

### 1.11.2 詞彙（常用 Glossary，台灣譯名）

| 詞彙 | 官方定義摘要 |
|---|---|
| Appware | 為特定設計任務設計的一組表單與巨集（如管路設計）；官方機器翻譯成「應用軟體」，本課程保留原文 |
| Batch／Interactive Mode | 無人介入（如夜間）執行／使用者逐步操作 |
| Head／Tail | BRANCH 在正常流向下的輸入端／輸出端 |
| Member／Offspring／Owner／Parent | 緊接在下／任意層在下／緊接在上／任意層在上；Group member 例外，只間接連到 GROUP |
| My Data | 為日後使用而記住 PDMS 資料的儲存區，常用於在模組間複製元素集合 |
| P-point | 用來操作與連接元素的假想位置與方向；P-line 是朝某方向延伸的 P-point |
| Hit Radius | 指標選點的最大容許誤差，超過則選不到 |
| 縮寫 | `CE`、`CREF`、`HREF`、`TREF`、`DAC`（Data Access Control）、`PADD`、`PML`、`UDA`、`Refno`、`PA`／`PL`（P-Arrive／P-Leave）等 |

## 1.12 新手第一天操作指南

**原則：第一天只讀不寫。** 在訓練專案以唯讀方式探索，把「元素、屬性、導覽、搜尋」四件事走通。

### 1.12.1 步驟

1. **登入。** 開啟 Design，選 Project、Username、MDB；**勾 Open Read Only**。若版面亂，再勾 Restore Default Layout。
2. **看狀態列與主選單。** 確認 Design Explorer 顯示；沒有就 `Display > Design Explorer`。
3. **導覽到一個 EQUI。** 展開 `WORLD > SITE > ZONE`，點選一個設備。確認它成為 CE，History 清單出現它。
4. **開 Attributes window。** `Display > Attributes`，勾 Track CE，在右鍵選單開 Columns > Data Type、Description，看 `NAME`、`TYPE`、`LOCK`、`OWNER`、`POSITION`。切換 Categorised／Alphabetical，各看一次。
5. **查命令對照。** `Display > Command Window` 輸入 `Q CE`、`Q MEM`、`Q ATT`，與 Explorer、Attributes window 對照（只讀命令，[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html)會系統介紹）。
6. **進 3D。** 從 Explorer 拖該設備進 3D 視圖；開 Drawlist，改顏色、勾 Edges、調透明度；試 Hide、Show Last Hidden Object(s)。
7. **用 Search 找東西。** `Display > Search Utility`，Element Type 填 `EQUI`，Name Contains 留空，Search；再改 `PIPE`，加 Attribute Filter。結果列拖進 3D、加入 My Data。
8. **用 Reference List。** CE 站在設備上，`Display > Reference List`，看接到噴嘴的管；右鍵 Add Connected。
9. **整理表格。** 在結果網格試排序、欄位篩選、群組排序、Export to Excel。
10. **離開。** `Design > Exit`。唯讀登入通常會直接問是否離開；若跳出儲存提示，**不要貿然選 Yes**，先確認是否真有變更。

### 1.12.2 常見錯誤

| 症狀 | 常見原因 | 處置 |
|---|---|---|
| 輸入欄的值沒生效 | 沒按 Enter，欄位仍是黃底 | 輸入後按 Enter |
| 連續挑選停不下來 | 提示允許重複挑選 | 按 Esc |
| 找不到元素 | 名稱大小寫不符；Element Type 為空；上限不是 WORLD；篩選器隱藏 | 檢查 Name Contains（區分大小寫）、Beneath Element、Explorer 篩選器 |
| 搜尋結果表格誤改資料 | 切到了 Single／Bulk Cell Edit | 改回 Read Only |

## 1.13 本章小結

1. Marine 是**資料庫驅動**的設計系統：圖、報表、3D 漫遊都是輸出；專案有 12 種資料庫，設計資料庫是以 `WORLD` 為根的階層樹，刪擁有者即刪所有成員。
2. 名稱以 `/` 開頭、不含空白、區分大小寫；UDA 以冒號開頭；偽屬性唯讀。
3. 登入的 Open Read Only 是安全網；輸入按 Enter 確認；系統沒反應先看狀態列；連續挑選用 Esc 結束。
4. Explorer 篩選器優先序：Show < Show Descendants < Skip < Hide Below < Hide。
5. Drawlist 管 3D 視圖內容；Search Utility 組合名稱、型別、範圍、體積、屬性搜尋並可存檔；網格功能三者通用；Reference List 由 `HREF`、`TREF`、`CREF` 推出關聯元素。
6. 第一天只讀不寫：登入、導覽、查屬性、查命令、Drawlist、Search、Reference List。

## 1.14 練習題與自我檢核

**練習**（皆於訓練專案、唯讀登入）：

1. 畫出你的專案的 `WORLD → SITE → ZONE → 專業元素` 階層，標出一個 PIPE 的 BRAN 與其 Head／Tail。
2. 在 Attributes window 對同一元素分別用 Categorised 與 Alphabetical，匯出 Excel；說明哪些欄位是 UDA（冒號開頭）。
3. 用 Search 找「名稱含某字串且 AREA 在 1 到 10」的元素（用 In the Range），存成 Saved Search，再用 Saved Searches 工具列執行。
4. 在 Drawlist 隱藏三個物件，再用三種方式重新顯示，比較差異。
5. 新增 Local View 與 Clone View，說明兩者 Drawlist 的差異。
6. 對 Reference List 與 Attributes 的 `HREF`、`TREF`、`CREF` 結果交叉比對。

**自我檢核：** 我能列出 12 種資料庫並指出哪種存 UDA；我知道 MISC 同時只有一人能寫入；我能說明名稱規則；我能說出 Explorer 篩選器五類規則的優先序；我知道 Undo 對 local drawlist 的影響；我知道 Search 的多個屬性條件是「且」、網格一次只能排序一欄。

## 1.15 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 1 章](appx_d_verification_zh-TW.reading.html#ch01)；取材覆蓋與未讀範圍：見[附錄 E 第 1 章](appx_e_coverage_zh-TW.reading.html#ch01)。
