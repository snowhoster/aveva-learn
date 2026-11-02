# 第 31 章　Draft 圖面管理與出圖流程：Draft Administrator、AutoDRAFT、Drawing Production 與 PLOT

> [第 9 章](ch09_drawings_zh-TW.reading.html)從「圖面是模型的視圖」切入，介紹了 `DEPT → REGI → DRWG → SHEE → VIEW` 階層。這一章換成**管理者與出圖作業**的角度：管理者先備好圖庫、規則與預設值，使用者才能建圖紙、視圖、標註；圖面做好後，交給 AutoDRAFT 補圖，或交給 PLOT 轉成印表機能吃的格式。二次開發者要記住：**圖庫與規則先於圖面**，找不到對的 Library、Drawlist 或 Rule Set，結果一定是空圖或樣式錯誤。
>
> **資料可信度：** 本章的操作流程、視窗與選單名稱、元素型別（`LIBY`、`SHLB`、`BACK`、`OVER`、`SYLB`、`SYTM`、`RPLB`、`RRUL`、`TRST`、`TAGR`、`IDLI` 等）與命令列語法，取自 AVEVA Marine 12.1 官方離線文件的四個部分：*Draft Administrator Application*、*AutoDRAFT*、*Drawing Production*、*PLOT*（以英文原文為準，中文機器翻譯僅作對照）。官方文件沿用 PDMS 時代的名稱（PDMS、Isodraft、AutoCAD 2007–2010），12.1 的實際版本差異未逐項驗證。官方文件是操作手冊，**幾乎沒有二次開發範例**，「二次開發者怎麼接」只列有依據的語法，其餘標〔待核對〕。Marine Drafting（船體圖面）、Design Draft 與 Area Based ADP 另見[第 28 章](ch28_other_modules_zh-TW.reading.html)與相關章節，本章不重複。

## 31.1 學習目標

讀完本章，你應該能夠：

1. 說明 Draft 在「3D 設計 → 圖面 → 輸出」流程中的位置，以及 Draft、ADP、AutoDRAFT 三個應用程式各自負責什麼。
2. 說明 Draft Administrator 要負責的八類 Library，以及誰有權進入管理者選單（`DRAFTADMIN` 團隊）。
3. 說明預設值檔（`DRA-GEN-SYSTEM`、`DRA-SETUP` 等）如何被載入，Full load 與 Partial load 的差異。
4. 說明 Layer Purpose、圖層建立定義、圖紙尺寸與命名規則各自控制什麼。
5. 說明 Representation Rule、Style、Hatching Rule、Change Rule、Drawlist、Tag Rule 之間的引用關係。
6. 說明 Backing Sheet 上的特殊 Note（`/LIMITS`、`/SCHEDULE`、`/KEYPLAN` 等）如何讓 ADP 自動化。
7. 依步驟建立 Department、Registry、Drawing、Sheet、View，並區分 User-Defined View 與 Limits-Defined View。
8. 說明標籤、尺寸、2D 繪圖與剖面平面（Section Plane）的基本作業與更新方式。
9. 說明 AutoDRAFT 三個子系統（Drawing Editor、Symbol Editor、Frame Editor）與 DXF／巨集往返流程，以及兩種建議工作模式。
10. 用 `plot driver plotfile output [options]` 做格式轉換、縮放、筆號對應，並知道 PLOT 與 Draft 管理者「Plotting Options」的關係。

## 31.2 Draft 在出圖流程中的位置

### 31.2.1 三個應用程式

官方文件把 Draft 描述為「由 3D 設計資料直接產生完整標註工程圖」的模組，圖面可隨設計變更更新。Draft 內有三個應用程式：

| 應用程式 | 用途 | 使用者 |
|---|---|---|
| General（一般 Draft） | 建立圖紙、視圖，加標籤、尺寸、2D 註記、剖面 | 繪圖員 |
| Automatic Drawing Production（ADP，自動出圖） | 依規則自動建視圖並加標註；含 General ADP、Steelwork Detailing、Hangers & Supports 三種 | 繪圖員／管理者 |
| AutoDRAFT | Draft 與 AutoCAD 的雙向介面 | 繪圖員／管理者 |

### 31.2.2 全貌

3D 模型經 Drawlist（畫哪些）與 Representation Rule（怎麼畫）進入 Draft 圖面（PADD 資料庫），加標籤、尺寸、Tag、2D 註記與剖面；圖庫由 Administrator 維護。完成後可經 AutoDRAFT（DXF）到 AutoCAD 補圖，或產生 Plot file 交給 PLOT 轉成 PostScript、HPGL、DXF、PNG 或螢幕預覽。

> **專業提醒：** 圖面上的尺寸與標籤都「掛」在設計元素上，不是死文字。官方強調標註內容直接取自設計資料，模型改了只要執行更新（`Graphics > Update > Annotation` 等）即可同步。因此「在 AutoCAD 裡手改尺寸」與「更新 Draft」是互相衝突的，31.6 節會說明。

## 31.3 Draft Administrator：管理者要設定什麼

> 〔公開版未收錄：AVEVA 官方產品截圖〕Draft System Defaults 視窗，列出 Master Project Defaults 與 Local Project Defaults 的圖庫指標

*圖 31-1　Draft System Defaults：各類 Library 的指標與名稱分隔符號。（AVEVA 官方文件截圖，僅供內部教學）*

### 31.3.1 角色與權限

管理者負責五件事：預設值（Library 指標、圖層、圖紙尺寸、命名規則、名稱分隔符號）、八類 Library（Sheet、Symbol、Isodraft Symbol、Label、Style、Representation Rules、Drawlist、Auto Tagging Rule）、ADP 規則、AutoDRAFT 的符號與圖框、以及以 `Settings > Load data file` 建立新專案區域與資料庫更新。

進入管理者選單的條件有兩個：以屬於 **Draft Admin 團隊**的使用者進入 Marine，且對存放 Library 的 Draft（PADD）資料庫有 **Read/Write** 權限。ADP 管理選單另外要求是 `DRAFTADMIN` 團隊成員，且從 ADP 應用程式進入，不在 Administration 應用程式裡。這些由系統管理員（[第 20 章](ch20_system_administration_zh-TW.reading.html)）在專案設定時處理；團隊名稱在文件中兩種拼法並存（Draft Admin／DRAFTADMIN），〔待核對〕實際團隊名。

### 31.3.2 隨附 Library 與搜尋順序

範例專案帶兩個 Department：`Master_Libraries`（任何專案可引用）與 `Project_Libraries`（專案專屬規則）。

使用者建立標籤等元素時，系統依 `DEPT` 下 `LIBY` 的**排列順序**找適用的 Library，找到第一個後把它與後面的 `LIBY` 都加入選單，直到遇到不含該類 `LALB` 的 `LIBY` 為止。兩個推論：

- 要對使用者隱藏某個 `LIBY`，把它排到 `DEPT` 成員清單最後。
- 不同類型的 Library 必須放在同一個 `DEPT` 下，使用者才看得到。

### 31.3.3 預設值檔

預設值檔存放在 `PDMSDFLTS` 環境變數指向的資料夾。進入 Draft 載入表單選單時，巨集 `%PDMSUI%/DRA/Admin/START` 會呼叫使用者可改的 `%PDMSDFLTS%/DRA-SETUP DRAFT`，再由它指向主預設值檔 `DRA-GEN-SYSTEM`。**官方明確建議：要改啟動行為，只改 `DRA-SETUP`，不要動 AVEVA 自訂的 START 或 VARS 檔。**

- 一般：`DRA-GEN-SYSTEM`（`.IMP` 英制、`.bak` 備份）、`DRA-SETUP`、`DRA-GEN-FONTS`（四個字型名）、`DRA-GEN-TEXT`。
- 圖層設定巨集：`DRA-GEN-DEFLAY`、`-DIMLAY`、`-LABLAY`、`-NOTLAY`、`-TAGLAY`、`-MATLAY`（Matchline）等，圖層建立後執行。
- ADP：`DRA-GENADP-PIPING`／`-EQUILOCN`／`-PLOTPLAN`／`-SUPPORTS`、`DRA-ADP-*LAY`、`DRA-SDADP-MACRO`；H&S：`DRA-SUPP*`；細部視圖：`DRA-LOC-*`、`DRA-DET-*`；尺寸：`DRA-DIM-PDIM`／`RDIM`（每次建立 PDIM／RDIM 時執行）。

> **專業提醒：** 每個使用者實際吃到哪一份預設值，由**他自己**的 `PDMSDFLTS` 決定。公司若有多種出圖標準（例如不同船東），做法是複製多份預設值檔並由使用者環境指向不同資料夾，而不是在同一份檔案裡塞條件。

### 31.3.4 System Defaults 視窗

進入方式：`Draft > Administration` 之後選 `Settings > System Defaults`。視窗上半是 Master Project Defaults（2D Symbols、Symbolic Labels、Backing Sheets、Tagging Templates 等），下半是 Local Project Defaults（Drawlists、Overlay Sheets、Representation Rules、Hatching Rep Rules、Local Styles、Hatching Styles、Tagging Rules、Circulation lists、Changes Rules、Drawing Template Prefix）。可直接輸入元素名稱，或導覽到元素後按 `CE`。

一般使用者在 `Options > Defaults` 的 User Defaults 視窗看到同一組指標；它以管理者設定初始化，使用者的修改只**覆蓋**、不會改動管理者的預設值。名稱分隔符號預設為斜線（例如 `SHEETS/SHLB1/BACK1/SN1`），可為 Style、Label Library、Drawlist Library 個別指定。

存檔與載入（視窗 `File` 選單）：

- Save／Save As 存檔，每次存檔，舊設定自動備份成 `DRA-GEN-SYSTEM.bak`；Restore Backup 可還原；Display Errors 顯示載入錯誤（含檔案行號）。
- **Full load**：先清掉現有值，再檢查最低必要設定（所有 layer purpose、命名規則、圖紙尺寸），缺的用 AVEVA 標準值補。
- **Partial load**：不清除現有值，只覆蓋檔內項目，**不檢查一致性**。

### 31.3.5 圖層、圖紙尺寸與命名

> 〔公開版未收錄：AVEVA 官方產品截圖〕Layer Purpose Definitions 視窗，標示 Purpose 必須三個字元、Setup File 與 Attribute Groups

*圖 31-2　Layer Purpose Definitions：每種圖層用途對應一個設定巨集與屬性群組。（AVEVA 官方文件截圖，僅供內部教學）*

| 設定 | 重點 |
|---|---|
| Layer Purpose Definitions | 每個圖層 `LAYE` 有 `PURP` 屬性（四字元關鍵字）。表單輸入**三個字元**，第四個字元由系統加（A、B、C…），讓同一個 `VIEW` 可有多個同類圖層。例如 `DIM` 用途可產生 `STLDIM`（`DIMA`）、`EQUDIM`（`DIMB`）、`PIPDIM`（`DIMC`）。`Setup File` 是圖層建立後執行的巨集；`Dim／Note／Text／Lab／Symb` 勾選決定 Layer Attributes 表單顯示哪些屬性群。 |
| 保留字 `TAG` | 自動標籤（Autotagging）專用，必須存在；若缺會在初始化時自動補上，**不能刪除**。 |
| Layer Creation Definitions | 建立 `VIEW` 時要自動建哪些圖層、怎麼命名（同一 Purpose 可建多層）。 |
| Layer Purpose Filtering | 決定哪些圖層出現在工具列的 Layer Note 下拉清單。 |
| Sheet Size Defaults | 最多 **15** 種標準圖紙尺寸（尺寸與說明）。 |
| Naming Conventions | 「必填命名」：`DEPT`、`REGI`、`DRWG`、`SHEE`、`VIEW`（例如圖號前綴填在 Drawing 的 Prefix）；「選填命名」：`VNOT`、`NOTE`、`RRUL`、`VSEC`，以 Named 勾選是否自動命名。 |

**常見錯誤：** Purpose 輸入四個字元（只輸入三個）；漏掉或刪掉 `TAG` 用途；用 Partial load 載入不完整的檔案，之後才發現圖層或圖紙尺寸缺項。

## 31.4 Library 管理

### 31.4.1 工作 Library 與 Library 類型

進入各管理應用程式後要先選 Working Library（`Draft > Select Working Library`，Type 可選 Sheet、Symbol、Isodraft Symbol、Label）。畫面頂端的選項清單記錄本工作階段選過的 Library，可用 `+` 鈕把目前元素加入。

| Library | 元素 | 要點 |
|---|---|---|
| Sheet Library | `SHLB` → `BACK`（Backing Sheet）、`OVER`（Overlay Sheet） | `SHLB` 像圖紙樣板，尺寸向下傳給 `BACK`／`OVER`；`BACK` 上放 `NOTE`（2D 圖元、`TEXP` 文字、`SYMB` 符號）；`OVER` 另可擁有 `VIEW`（常用於索引圖 keyplan），`VIEW` 可引用 Rule Set。 |
| Symbol Library | `SYLB` → `SYTM`（符號樣板） | `SYLB` 像一張圖紙排放各 `SYTM`；原點標記與說明文字放在另一張 `BACK`，以 `Modify > Symbol Library > Definition` 的 Backing Sheet Reference 連回，避免它們被選進圖面。 |
| Isodraft Symbol Library | `ISOLB` → `ISOTM` | 由 straights（實線、虛線＝保溫、鏈線＝伴熱）與 markers 組成；可匯入 Isodraft 符號巨集。 |
| Label Library | `LALB` → `SYTM`、`TXTM`（文字樣板） | `TXTM` 無成員，以 `BTEX` 存字串，可含 `#` 開頭的**智慧文字**（例如 `#NAME`），顯示時換成設計資料庫的屬性值。 |
| Style Library | `RPLB` → `STYL` | 見 31.4.2。 |
| Representation Library | `RPLB` → `RRST`／`HRST`／`CRST` | 見 31.4.2。 |
| Drawlist Library | `DLLB` → `IDLI` | 見 31.4.3。 |
| Tag Rule Library | `TRLB` → `TRST` → `TAGR` | 見 31.4.3。 |

> **專業提醒：** Backing Sheet 的 `NOTE` 名稱很講究。例如在 `BACK` 底下建一個名為 `backing_sheet_name/LIMITS` 的 Note，只放一個 `RECT`，使用者執行 `Create > View > Pre-defined Frame` 時，視圖會自動縮進這個矩形，不會蓋到圖框。

### 31.4.2 Style、Representation 與 Hatching／Change Rule

這一組決定「模型在圖上長什麼樣子」：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Representation 與 Hatching Library 的引用關係，VIEW 引用 HRST，RRUL 引用 STYL，HRUL 引用 HSTYL

*圖 31-3　Representation Library 的資料階層：左側為使用者定義（View 的本地規則），右側為管理者定義。（AVEVA 官方文件截圖，僅供內部教學）*

- `STYL`：決定線型、顏色與繪圖層級（`DLEV`）；六種線型（Frontface、Backface 等）各設顏色與樣式，標準線型 10 種、線寬 3 種；表現旗標 Tube、Piping Symbols、Obstructions、Insulation、Profile、P-Line、Centreline（關掉 Tube 就不畫管子）。`HSTYL` 為剖面線樣式（標準填充 18 種）。
- `RRST` → `RRUL`：`For` 指定元素類型或具名元素，`With` 填 PDMS 表示式（如 `(HBOR GT 100) AND (TBOR GT 80)`），引用**同一個 `LIBY`** 內的 `STYL`；`Symbology` 勾選表示以 2D 符號表示。`HRST` → `HRUL` 控制哪些面填剖面線。
- `CRST` → `DCRULE`／`ACRULE`：設計變更（`DCSTYL`）與標註變更（`ACSTYL`）如何標示。**`CRST` 不會隨 Change Library 自動建立**，`View` 也不能擁有變更規則，只能引用 Change Ruleset。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Representation Rules 視窗：Rule Sets、For、With、Style 設定

*圖 31-4　Representation Rules 視窗：對 Branches 加 With 條件並引用 STYL。（AVEVA 官方文件截圖，僅供內部教學）*

流程是：先建立 `LIBY`，再建 Style Library，再建 Representation Library，最後把規則引用到 Style。建立 `RPLB` 時，Representation 庫會自動帶一個 `RRST`，Hatching 庫會自動帶 `HRST`。

### 31.4.3 Drawlist 與 Tag Rule

> 〔公開版未收錄：AVEVA 官方產品截圖〕Drawlist Management 視窗：Drawlist Library 與 IDLI 清單，含 Create、Create Copy、Delete、Clean Up

*圖 31-5　Drawlist Management：管理者與使用者共用的同一個視窗。（AVEVA 官方文件截圖，僅供內部教學）*

- **Drawlist（`IDLI`）：** 決定視圖畫哪些設計元素。由 Add 清單（`ADDE`）與 Remove 清單（`REME`）組成，可挑元素、引用其他 Drawlist，或用 Volume Defined 以兩個對角座標框出體積，凡部分或全部落在體積內的重要元素都會加入。管理者建在 Library 層，使用者則建在本地層，視窗相同。
- **Tag Rule（`TAGR`）：** 在 Tagging Library 視窗建立。每條規則指定要標的元素類別（`Tag`）、PDMS 表示式（`With`，例如 `POSE FT E1000`）、引用的標籤樣板（`SYTM` 或 `TXTM`），可再綁定一個 Drawlist 限制範圍。**Tag Rule 名稱由系統自動產生，不能改**；新規則的屬性取自按下 Create 時表單上的設定，所以要先填好再按。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Tag Rule 表單：Rule、Tag、With、Template Reference、Drawlist 與 Drawlist Ref

*圖 31-6　Tagging Library 視窗下半部：TAGR 的元素類別、條件與標籤樣板。（AVEVA 官方文件截圖，僅供內部教學）*

### 31.4.4 2D 符號表示法（Symbolic Representation）

執行 `Update Design` 時以 2D 符號取代設計元素，需 Draft 與 Catalogue 管理者合作：Catalogue 新增 `DRSSET` 與 `DRSYLK`（`SCOM`、`SPRE`、`JOIN`、`SFIT` 有指向 Draft Symbol Set 的參考）；一個 `DRSSET` 對一個 `GPART`；在 `DRSYLK` 以 `%XYSC` 可做非等比縮放；符號方向由 `SYTM`／`TXTM` 的 `PPDI` 對應目錄元件 P-point 的 `%NUM`。設計符號庫放在主專案 MDB 的 Draft 資料庫，**避免使用 `BACK`**，以免 Global 分發複雜化。

### 31.4.5 ADP 管理

ADP 有三種：General ADP（設備與管路）、Steelwork Detailing ADP（SDA）、Hangers and Supports ADP。管理者在 ADP 應用程式內設定。

**General ADP：**

- 預設值在 ADP Defaults File Editor（`Settings > General ADP Defaults`）編輯，載入 `DRA-GENADP-*` 檔。尺寸分三種：Type 1 管路、Type 2 設備中心、Type 3 格線；處理順序預設 3、2、1（因為各型可能繼承其他型的尺寸點，被繼承的必須先存在）。各型規則用 **PML 表示式**定義。
- `Restrict USER Access` 打開後，使用者不能修改預設值檔，只有 `DRAFTADMIN` 成員可改。
- 範例預設規則：Volume 內全部加入，但擁有者 Zone 的 Function 為 Heating 或 Electrical 的 `PIPE` 會被移除。
- Tagging 與 Schedule 各自有 Tag Rule Library；Schedule 的 `TRST` 底下規則 `/LOCAL` 產生圖面標籤，`/ENTRY` 引用含 `prefix/ENTRY`、`prefix/HEADER`、`prefix/OFFSET` 的特殊 `SYTM` 產生表格列（`OFFSET` 的 `BTEX` 如 `X 0 Y -10` 表示每列往下 10 單位）。

**Backing Sheet 控制 Note（全部 Note 的可見度設為 false）：**

| Note 名稱 | 用途 | 不存在時 |
|---|---|---|
| `/REFDRWGS` | 參考圖清單區 | GUI 控制項停用 |
| `/LIMITS` | 視圖可用範圍（單一 `RECT`，`LVIS` 設 FALSE） | 假設整張圖紙 |
| `/SCHEDULE` | 擁有兩個 `MRKP`：`/SCHEDULE/ORIGIN` 與 `/SCHEDULE/EXTENT`；超出 EXTENT 的列會被隱藏並警告溢出 | 提示使用者輸入位置 |
| `/KEYPLAN` | `/KEYPLAN/ORIGIN` 的 `MRKP`（索引圖位置） | 放在 X0 Y0 |
| `/TITLE` | 標題欄區域，用於縮放 | GUI 控制項停用 |

標準 A0 圖紙範例：`/DRA/MAS/BACKS/METRIC/A0`。

**Steelwork Detailing ADP（SDA）：** 需要含圖框的 Sheet Library、符號庫、Style Library、Representation Rule Library 與一或多個 `SDAOPT`（範例庫 `DRA/MAS/SDADP` 有 `SDA-Default`、`SDA-Main-Views`）。`SDAOPT` 的 `UPDCB` 指向客製巨集 `%PDMSDFLTS%/DRA-SDADP-MACRO`，SDA 每產生一個主要項目就呼叫一次，控制圖紙命名、筆與文字位置，可用 PML 修改。官方提醒：SDA 製造圖有時尺寸不足，但至少達所需的 70%；隨附巨集不會替 `DEPT`、`REGI`、`DRWG` 命名。

**Hangers and Supports ADP：** 隨附 Backing Sheet 有 12 個 Note，`HS_Matl_List`、`Frame`、`Supported_Items`、`Support_Steel`、`LIMITS` 為必要；Note 內 `TEXP` 的 `BTEX` 以 `H&S_MATL_LIST:value1, value2`、`REF_X:value` 等格式定位 BOM 欄位。完整欄位表〔待核對〕。

### 31.4.6 AutoDRAFT 管理與資料更新

- `Draft > AutoDRAFT`：`Edit > Symbols` 啟動 Symbol Editor，`Edit > Sheet Frame` 啟動 Frame Editor，`Import > Symbols`／`Import > Sheet Frame` 把巨集讀回。只有 AVEVA 軟體與 AutoCAD 不在同一部機器時才需手動匯入；同機時由 AutoDRAFT 直接寫回資料庫，或先定位到正確層級後以 `$M/` 指令執行巨集檔。細節見 31.6 節。
- `Settings > Load data file`：載入 Main Libraries、Template Drawings、Application Department，用來為新專案建立基礎資料。
- 資料庫更新（只在特定情況做）：

- `Graphics > System Update > Picture`：圖片檔損毀（如 RECONFIGURER 之後，或顯示舊版建立的 `VIEW`）；被系統提示時才做。標註圖形一定能恢復，設計圖形不一定。
- `... > Instances`：`LIBNO NEW` 之後，重建 `SYMB`、`OLAY`、`BACK` 等實例化圖形。
- `... > Refs`／`Names`：設計資料庫被刪除並以巨集重建之後，更新 Draft 元素對設計元素的參考與其隱藏名稱屬性。

## 31.5 Drawing Production：使用者出圖作業

### 31.5.1 資料階層與起手式

> 〔公開版未收錄：AVEVA 官方產品截圖〕Draft 資料庫階層：WORLD、DEPT、REGI、DRWG、SHEE

*圖 31-7　Draft 圖面階層：Department 擁有 Registry，Registry 擁有 Drawing，Drawing 擁有 Sheet。（AVEVA 官方文件截圖，僅供內部教學）*

此處的階層與[第 9 章](ch09_drawings_zh-TW.reading.html)一致，另需注意：**行政元素只能建在已存在元素的下一層**，因此要在新分支建圖，必須先建 `DEPT` 再建 `REGI`，才能建 `DRWG` 與 `SHEE`。

1. `Create > Department`：預設名 `DEPT1`；Attributes 有 Size & Units、Intelligent Text、Pens、Miscellaneous 四個標籤頁，這些屬性是其下 Registry 的預設，往下傳遞，任何層級都可再改。
2. `Create > Registry`：可勾 Create Drawing（Explicitly 或 From Template）。
3. `Create > Drawing`：Explicitly 要自己建所有成員；From Template 選模板來源、圖紙尺寸、張號；工具列 Create from Default Template 可一鍵建圖。

由樣板建立的圖，會自動帶 `SHEE`、至少一個 `VIEW`、若干 `LAYE`，以及擁有的 Library；官方叮嚀**不要重新命名或刪除這些 Library 或其成員**。

**預設圖紙以唯讀開啟的規則：** 唯讀的可繪元素只會開在 Reference View（不開在 Main View），因此只有你有寫入權限的元素才能修改。Draft Explorer 對圖紙按右鍵 `Open Sheet`，或在 Reference View 右鍵 `Add CE`。

### 31.5.2 字型

支援 AVEVA 與 TrueType 字型；TrueType 須每台工作站都裝並註冊在專案 SYSTEM 資料庫（每專案最多 23 種），**同一張圖紙不能混用兩種字型**。`SHEE`、`BACK`、`OVER`、`SYLB`、`LALB` 的系統屬性 `TTFENA` 依擁有者 `FONT` 屬性自動決定且不可改；要建可用 TrueType 的 `SHEE`，其 `DRWG` 的 `FONT` 須先設成 TrueType，且 `BACK` 的字型類型必須相容。最好整個 `REGI` 或 `DEPT` 一開始就設好。

### 31.5.3 視圖：User-Defined 與 Limits-Defined

視圖決定 Sheet 上顯示哪些設計項目，內容含：視角（方向、比例）、視圖框在圖紙上的大小位置方向、內容（Drawlist）。

| 類型 | 適用 | 特性 |
|---|---|---|
| User-Defined View | 畫個別項目或一組項目、不知道體積時 | 視圖框大小與內容無關；比例可自動設定以讓內容填滿視圖框 |
| Limits-Defined View | 畫指定體積的內容 | 界限以專案座標定義，視圖框大小依所選比例決定；可顯示 Matchline（接合線）與座標文字 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕User-Defined View 視窗：General 標籤頁含 View Type、Section Mode、Style、Hatching Rules、Change Rules、Direction，底部 Update Design on Apply 選項

*圖 31-8　User-Defined View：General 標籤頁與 Update Design on Apply? 選項。（AVEVA 官方文件截圖，僅供內部教學）*

**修改既有視圖為 User-Defined：** `Modify > View > User-defined`，在 General 標籤頁設 Title、View Type、Section Mode、Style（可設管路保溫：`PIPE+PIPEINSUL-Solid`／`-Dashed`）、Hatching Rules、Change Rules、Direction；以 `Graphics > Drawlist` 設內容；Scale 標籤頁選 Metric、Architectural、Engineering 或 Auto Scale。「Update Design on Apply?」有 No Update、Update Design、Use Background Process 三選項：**任何設定變更後，必須選 Update Design 並按 Apply，圖才會重算**（或執行 `Graphics > Update > Design`）。

**建立含 Limits-Defined View 的 Sheet：** `Create > Sheet > Explicitly`（須在 Drawing 層級或以下）→ `Create > View > Limits-defined`，表單有 General、Limits、Scale、Intelligent Text 四個標籤頁與 Matchlines 勾選；內容以 `Graphics > Drawlist` 建 Drawlist，再用 `Graphics > Drawlist Ref` 引用。Matchline 若超出圖框，可用 `Frame > Position > Cursor > Top Right` 重新擺放。

### 31.5.4 3D View

> 〔公開版未收錄：AVEVA 官方產品截圖〕Draft 的 3D View 視窗，洋紅色方框為 Viewfinder，工具列含同步模式下拉選單

*圖 31-9　3D View：Viewfinder 方框代表投影到 2D View 的範圍，同步模式為 Auto Update。（AVEVA 官方文件截圖，僅供內部教學）*

3D View 讓你在 3D 中組裝設計元素，確認內容後再變成 2D 圖面。加入項目：從 Design Explorer 拖到 3D View、右鍵 `3D View > Add`、或工具列 Add to View。**Viewfinder**（洋紅色框）可互動縮放、移動、旋轉，變更會反映到 2D View；它相當於一個窗口，對 3D 設計拍 2D 快照。

同步模式：On Demand（按圖示才同步）、Auto Update（立刻）、Background（閒置時）。

> **專業提醒：** Auto Update 與 Background 在大型圖面上可能使系統明顯變慢。另外，在 2D View 增減項目**不會**自動回到 3D View，須按 Update 3D View from 2D View。

### 31.5.5 標籤

`Create > Label > General/Symbolic` 開 Labels 表單：Create NEW／Create COPY、Attach to（元素類型）、Re-Attach、PPoint／Pline／Rotate、Blanking 與 Blank Margin、Attributes、Offset、Create Gaps。Draft 會自動切到 Label 圖層（建立 `VIEW` 時一併建好 Label、Dimension、Note、Tag 等圖層）。預設標籤內容是元素名稱 `#NAME`，也可改成其他文字或智慧文字。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Labels 表單：General Labels 標籤頁，含 Attach to、PPoint、Pline、Blanking、Attributes、Offset

*圖 31-10　Labels 表單的 General Labels 標籤頁。（AVEVA 官方文件截圖，僅供內部教學）*

**圖形化修改：** 點工具列箭頭進入 Modify Mode，點選標籤後可拖曳標籤本體、旋轉把手、Attachment Point、Connection Point 與引線彎折點；右鍵選單提供定位選項：

右鍵選單的定位選項：2D cursor hit（預設，跟隨游標；開啟 Snap to Grid 時改對齊格點）、End／Mid／Centre Point of（吸附到線、弧、圓）、Intersect at／between、Nearest to。

Gap Manager 可在引線、尺寸線與投影線開缺口，**每個標籤最多 10 個**。標籤線型與顏色的修改只影響目前這個標籤；要影響之後新建的標籤，須改圖層屬性並重新建立。

設計符號（`DESSYM`）由 Draft 標註時自動建立，可像標籤一樣拖曳，但位置、方向、引線若被管理者鎖定就不能改。

### 31.5.6 尺寸

四種尺寸：Linear（`LDIM`）、Angular（`ADIM`）、Radial（`RDIM`）、Pitch Circle Diameter（`PDIM`）。尺寸元素建在 `VIEW` 之下對應用途的圖層。

線性尺寸流程：選對應的 Dimensions 圖層 → `Create > Dimension > Dimension Linear` → 在 Create Linear Dimension 視窗設 Type（Chain、Tail、Truncate）、尺寸線方向、端點符號、投影線文字／角度 → OK 後進 Linear／Angular Dimensions 視窗，用 Create 在 2D 或 3D View 逐一點選 P-point、P-line 或元素，按 Esc 結束。尺寸點（`DPPT`）與 3D 模型元素連結，所以尺寸文字直接取自設計資料；設計改了，執行 `Graphics > Update > Annotation` 即更新。**Draft 所有尺寸都以 3D 世界座標方向定義。**

圖形化修改很有限：線性尺寸只能改投影線長度、移到被標註物件另一側、改文字退距（standout）；角度尺寸只能改偏移與退距。

### 31.5.7 2D 繪圖與剖面

- **2D 繪圖：** 圖元（Primitive）是 `NOTE`（圖紙層）、`VNOT`（圖層層）或 `SYTM` 的成員；`VNOT` 內的圖元可用 3D 設計座標定義。官方註明此功能不打算取代繪圖軟體。`Draw > Primitives` 的 2D Draughting 視窗有 Lines、Shapes、Symbols、Text 四個標籤頁。各圖元的熱點（Hotspot）操作在 Modify Mode 以拖曳完成；Outlines 分 Polyarc（弧線與直線串接）與 Spline。
- **剖面平面：** 在 3D View 建立與管理，新平面預設跨滿整個視圖與模型深度，可移動、對齊、旋轉，也可做階梯式平面（`Insert Step After`）。每個平面有自己的 Clipping List，`Flip` 切換被剪的一側。刪除平面時系統會問是否連同引用它的 `VSEC` 一起刪；被多個 `VSEC` 引用的 Library 平面通常不應刪除。

### 31.5.8 Automatic Drawing Production（General ADP）

General ADP 用特殊的 Backing Sheet 自動放置明細表與參考圖清單，並用「智慧索引圖」（以 Overlay 呈現）界定圖面涵蓋的模型範圍。入口：`Draft > Auto Drawing Production`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Modify General ADP Drawing 視窗：Frame（Backing Sheet）、Title、Date、Drn、Create ADP Sheet

*圖 31-11　Modify General ADP Drawing：選 Backing Sheet 與標題，再建立 ADP Sheet。（AVEVA 官方文件截圖，僅供內部教學）*

ADP 以三層表單逐步下到 View：`Create > General ADP > Drawing`（在目前 `REGI` 下建 `DRWG`，填 Frame＝Backing Sheet 與 Title）→ Create ADP Sheet（選 Keyplan、Area、Reference Drawings）→ Create ADP View（Function 指到對應預設值檔，例如 `DRA-GENADP-PIPING`）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Modify General ADP View 視窗：Drawlist、Style、Type、Direction，Limits，Scale，Tagging、Schedules、Attributes

*圖 31-12　Modify General ADP View：Drawlist、Limits、Scale 與 Tagging／Schedules／Attributes 按鈕。（AVEVA 官方文件截圖，僅供內部教學）*

View 表單：Drawlist 可選「Volume Defined」以 From／To 方向座標界定體積；Limits 可來自 Drawlist 或 Keyplan；Scale 按 Nearest 自動選能顯示完整圖面的比例。按 Update 可勾選 Design Graphics、Schedules、Tagging、Annotation、Piping、Equipment、Gridline，**Update Now** 立即產生（官方說可能需數分鐘），**Create Batch Macro** 為該 View 產生批次巨集。

> **專業提醒：** Create Batch Macro 是文件中唯一明確指向「批次出圖」的功能。巨集的內容與如何在背景執行文件未說明，〔待核對〕。Area Based ADP（依區域自動出圖）的做法另見[第 28 章](ch28_other_modules_zh-TW.reading.html)。

### 31.5.9 使用者自訂選單

`Utilities > General Utilities` 的 `Control > Define` 可定義選單，執行 Draft 命令或顯示表單（填表單**名稱**而非標題）。命令語法見 Draft User Guide。

### 31.5.10 二次開發者怎麼接

| 項目 | 文件依據 | 狀態 |
|---|---|---|
| 預設值檔、圖層巨集、`DRA-SDADP-MACRO` | PML 文字巨集，可複製修改；`SDAOPT.UPDCB` 指向客製巨集 | 有依據 |
| ADP 尺寸規則、Rule 的 `With` | PML／PDMS 表示式 | 有依據 |
| 圖面建立／更新的命令語法 | 文件只講 GUI；命令語法在 Draft User Guide，本章未讀 | 〔待核對〕 |
| 以 PML 批次建 `DRWG`／`SHEE`／`VIEW`、讀取 Draft 屬性 | 文件未提供語法（屬性如 `PURP`、`BTEX`、`TTFENA` 有出現） | 〔待核對〕 |

## 31.6 AutoDRAFT：Draft 與 AutoCAD 的雙向介面

### 31.6.1 三個子系統與資料流

> 〔公開版未收錄：AVEVA 官方產品截圖〕AutoDRAFT 資料流：Drawing Editor 以 DXF 送到 AutoCAD，Symbol Editor 與 Frame Editor 以 ASCII 巨集檔回到 Draft

*圖 31-13　AutoDRAFT 的三個子系統與資料流向。（AVEVA 官方文件截圖，僅供內部教學）*

| 子系統 | 方向與格式 | 用途 |
|---|---|---|
| Drawing Editor | Draft／Isodraft → **DXF** → AutoCAD | 把圖紙送進 AutoCAD 補充細節 |
| Symbol Editor | AutoCAD → **Draft 命令巨集**（ASCII，預設檔名 `symbols.mac`）→ Draft | AutoCAD 圖塊（Block）轉成 `SYTM`，內含 2D 圖元 |
| Frame Editor | AutoCAD → Draft 命令巨集（預設 `pdmsback.mac`）→ Draft | AutoCAD 圖框轉成 `BACK` 或 `OVER` |

官方版本資訊：支援 AutoCAD 2007、2008、2010；Unicode 文字從 AutoCAD 2007 起支援，若 AutoCAD 輸出編碼異常，可用環境變數 `PDMSAUTODRAFT_ENCODING` 指定編碼（細節請洽 AVEVA 支援）。Isodraft 的等角圖只能用 Drawing Editor，不能用 Symbol／Frame Editor。〔待核對〕公司 AutoCAD 版本是否在此清單內。

### 31.6.2 Drawing Editor 的操作

**兩種啟動方式：**

- 同機器：從 Draft 選 `Draft > AutoDRAFT > Edit > Drawing`，DXF 轉換與傳輸自動完成（會自動加 `CUTMARKS OFF`）。
- 不同機器：先在 Draft 以命令 `PLOT SHEE DXF /SHEET1.dxf CUTMARKS OFF`（檔名必須以 `.dxf` 結尾）產生檔案，以 FTP 等方式傳到 AutoCAD 機器，再執行 `adraftde` 指令：

| 目的 | 指令（官方範例） |
|---|---|
| 新建 | `adraftde -new dwg_filename -trfile transfer_filename [-model \| -paper]` |
| 以新圖更新既有圖 | `adraftde -update dwg_filename -trfile transfer_filename [-model \| -paper]` |
| 只開啟 | `adraftde -open dwg_filename [-model \| -paper]` |

`.dwg`、`.dxf` 副檔名由腳本自動加，不可自行輸入；省略時預設 `-paper`。

**幾條不能違反的規則：**

- Draft 的圖形在 AutoCAD 裡位於名為 **`GT_` 加數字**的圖層。**不要自己建 `GT_` 開頭的圖層**，下次 Draft 圖面更新時整層會被清掉。
- 在 `GT_` 層上做的修改，下次更新都會消失；使用者新增的圖形應放在自己的 AutoCAD 圖層，更新時保留。
- 傳輸檔以毫米為單位；以 `PLOT` 命令自行產生 DXF 時沒有單位註解，需要英制須手動在檔尾加兩行 `999` 與 `PDMS_UNITS INCH`（官方原文排版疑有切割，〔待核對〕）。
- AutoCAD 圖面是 Draft 圖紙的模型，比例與圖紙一致；官方建議**所有尺寸都在 Draft 裡標**，因為在 AutoCAD 標的是紙上長度，不是模型長度。
- Draft 的字元間距屬性 `CSPA` 在 AutoCAD 沒有對應，轉出時被忽略，字串長度會不同。

**Drawing Editor 新增的 AutoCAD 命令（`PDMS Draw` 選單）：** `pdms_blank_create`／`pdms_blank`／`pdms_blank_edit`（Autoblanking）、`pdms_layer_mapping`、`pdms_layers`（`GT_` 層或使用者層 ON／OFF／Freeze／Thaw）、`pdms_colour`（為 `GT_1`～`GT_272` 套 AVEVA 標準顏色）、`pdms_textfile`、`pdms_copy`、`pdms_view_create`／`pdms_view_sel`、`pdms_quitacad`／`pdms_endacad`。

**Autoblanking 要點：** 遮蓋形狀放在 `PDMS_BLANKS` 圖層；**文字不會被遮蓋**；只對 Z=0 平面有效；耗時，建議出圖前才做；plot 要從 AutoCAD **主選單**執行，隱形邊界才不會被忽略；Draft 自動套用的遮蓋不能用 `pdms_blank_edit` 編輯。

**Layer Mapping 要點：** `pdmslaymap.txt` 每行：Draft 圖層名、AutoCAD 圖層名、顏色號（1–255）、線型；前兩欄必填。**之後還要從 Draft 更新的圖不要做 Layer Mapping**，否則可能出現重複圖形。

### 31.6.3 Symbol Editor 與 Frame Editor

> 〔公開版未收錄：AVEVA 官方產品截圖〕AutoDRAFT Symbol Editor 視窗：AutoCAD Work Directory、Symbol Drawing Name、Replace All Symbols、Requested action、Units、Symbol Library name

*圖 31-14　AutoDRAFT Symbol Editor 啟動視窗。（AVEVA 官方文件截圖，僅供內部教學）*

**Symbol Editor 的 AutoCAD 作業規則：**

- 每個符號樣板是一個 Block 的 Insert，必須帶屬性 **`PDMS_NAME`**（Draft 符號名稱，插入圖塊時回答此提示）。
- 可含的實體：Line、Point、Circle、Arc、Text（Generation Normal）、含上述圖元的 Insert；3D 實體、頂層 Insert 的其他屬性、小於 0.01 mm 的實體可能被忽略或簡化。
- 符號 Insert 要與註解放不同圖層；圖面範圍必須符合 `SYLB` 圖紙大小（例如 A0 公制以 AutoCAD 命令 `limits` 設 `0,0` 至 `1189,841`）。
- 若符號庫要加註解，註解放另一層，凍結符號圖層後用 Frame Editor 建 `BACK`，再在 Draft 於 `SYLB` 的 `BSRF` 屬性參照這張 `BACK`。
- 巨集啟動：`adraftse -new dwg_filename` 或 `adraftse -open dwg_filename`；同機器則由 Draft 選單進入。同名 `SYTM` 已存在時，舊圖元會被刪除並以新定義取代；「Replace All Symbols」勾選則所有同名符號直接覆蓋，否則匯入時逐個詢問。

**Frame Editor：** 啟動腳本為 `adraftbe`（`-new`／`-open` 同理）。圖框名稱必須是合法的 AVEVA 資料庫名稱；與同庫既有 `BACK` 同名時視為替換，舊圖形被刪除；若與其他類型元素同名，命令檔中止。**已含 `VIEW` 的 `OVER` 不會被覆蓋。**

**AutoCAD 轉 Draft 對應（節錄）：** Line／Point／Circle／Arc／Text 對應 `STRA`／`MRKP`／`CIRC`／`ARC`／`TEXP`；Insert 展開為 2D 圖元且不可非等比縮放；`GTSOLID`／`GTDASH`／`GTDOT`／`GTCHAIN` 對應 `NLSTYLE` 的 SOLID／DASHED／DOTTED／CHAINED。所有實體必須在 model space，未列入對應表的實體會被忽略。AutoCAD 的線型比例被忽略，虛線長度可能有差異。AutoDRAFT 匯出使用者線型時會建立 `pdmsuser.lin`，**該檔已存在則 AutoDRAFT 無法運作**。

### 31.6.4 兩種建議工作模式

- **工作法 1（AutoCAD 為主）：** 最終圖是 AutoCAD 圖，用 AutoCAD plot。Draft 負責隱藏線視圖、尺寸、智慧標籤；AutoCAD 負責圖框、符號、文字、細部視圖。更新時在 Draft 更新視圖再重送，`GT_` 層被換新、AutoCAD 層保留。Symbol Editor 可在專案初期建智慧標籤符號庫。
- **工作法 2（Draft 為主）：** 最終圖是 Draft 圖，用 AVEVA 出圖（PLOT）。專案初期用 Symbol／Frame Editor 建符號與圖框庫；每張圖在 Draft 建圖紙、視圖、尺寸、標籤；需補圖時送 AutoCAD，再用 Frame Editor 把補的內容送回 `BACK`／`OVER` 並刪除 AutoCAD 圖。更新後若要再送，先刪掉 AutoCAD 產生的 BACK／OVER 中要重畫的項目。

Isodraft 只有工作法 1 的形式：送入 Drawing Editor 補圖，用 AutoCAD plot。

### 31.6.5 二次開發者怎麼接

- 文件有依據的接口：命令（`PLOT SHEE DXF`、`adraftde`、`adraftse`、`adraftbe`、各 `pdms_*`）、環境變數 `PDMSAUTODRAFT_ENCODING`、`pdmslaymap.txt` 格式、Draft 命令巨集檔；可由外部指令稿呼叫，但**文件未提供腳本驅動範例**，〔待核對〕。
- `$M/` 載入巨集的語法請依官方原文，本章不推導其他引數。

## 31.7 PLOT：圖檔轉換與輸出

### 31.7.1 PLOT 是什麼

PLOT 是獨立工具，把 AVEVA 程式產生的偽碼（pseudo-code）繪圖檔轉成標準格式，再送到硬體、檔案或螢幕。

| 輸入格式（自動辨識） | 說明 |
|---|---|
| PDMS | 圖形輸出模組預設格式，二進位，與裝置無關 |
| HPGL／HP-GL/2 | 兩者相關但 HP-GL/2 不是 HPGL 的超集，官方建議視為不同格式 |
| DXF | ASCII；檔案不記錄單位，不是毫米時要明確縮放；解譯所有區段（含 `LTYPE`、`LAYER` 表與 Blocks 的 `INSERT`） |
| GPGP（GP2） | ASCII |

輸出驅動：`BENSON`、`CALCOMP`、`DXF`、`HOUSTON`、`HP`／`HPGL`、`HPGL2`、`LASERJET`、`LIST`、`PDMS`、`PENMAN`、`PNG`、`POSTSCRIPT`／`PS`、`SCREEN`、`XDUMP`。其中 HPGL、HPGL2、PDMS、DXF 與輸入格式對應，所以 PLOT 也可在這些格式之間雙向轉換。

### 31.7.2 基本用法

```
plot driver plotfile output [options]
```

| 參數 | 說明 |
|---|---|
| `driver` | 輸出驅動名稱 |
| `plotfile` | 輸入偽碼檔；格式由檔頭自動辨識，無法指定 |
| `output` | 輸出檔名；或 `-0`（減零）表示命令提示視窗 |
| `options` | 選項；**驅動專屬選項必須用引號包起來，多個選項以逗號分隔**；一般選項（如 `scale=`）直接寫在命令列 |

官方範例：

```
plot pdms plot12 ulay.pl
plot screen plota2 -0
plot hp view.pl view.hp scale=0.8 "CE Y"
plot dxf view1.pl view1.dxf "UNITS INCHES"
plot png in.dxf out.png "BITMAP 32 32"
```

不加參數輸入 `plot` 顯示語法摘要，`plot -version` 查版本，`plot -drivers` 查驅動選項，`plot -message` 把預設訊息複製成 `PLOT.MF` 供修改（例如改成其他語言）。

### 31.7.3 一般命令列選項（所有驅動適用）

- `SCALE=factor`：輸出／輸入比例（0.5 為半尺寸）；只能用在命令列，對自動填滿紙張的驅動（Laserjet、PostScript、Screen、Xdump）無效。
- `ADJUst`：太大時自動縮小至紙張，否則報錯終止。`AUTOsize`：以圖形外框取代檔內圖紙大小（僅 DXF、HPGL、HP-GL/2 輸入）。
- `ARCSize integer`：一圈圓的弦數，12–175，預設 90。
- `PENS` 與 `ATTR`：筆號、線型、線寬對應（最多 256 支筆；模式 Yes、No、Attr、Same）。例如 `PENS YES,ATTR 1 4,ATTR 2 5` 把輸入筆 1、2 換成輸出筆 4、5。
- `DEKInk`：去除重疊線並重排以縮短筆行程。`SPLIt width height`：切成多張（如 A0）；`BORDer integer`：加邊框；`CUTMARK`：畫裁切標記。

### 31.7.4 軟驅動（Soft Driver）

軟驅動讓你替「標準驅動＋一組選項」取個名字，定義在檔案 `PLOTDRIVERS`，格式為：

```
soft_driver|standard_driver|option1, option2, ...
```

以 `|` 分隔三段，選項以逗號分隔，過長行可用 `\` 續行；名稱不得與標準驅動相同，不分大小寫。`PLOT` 搜尋此檔的順序是 `CADC_PLOT_DIR` 指向的目錄、目前目錄、最後是 PLOT 程式所在目錄。命令列選項會放在軟驅動選項之後，因此**優先**。

官方範例：

```
PSRGB|POSTSCRIPT|BANNER Y,RGB,PTYPE 'statusdict begin 2 setpapertray end'
```

之後 `plot psrgb plota22 plota22.out` 即等同完整的 `plot postscript ...` 加同樣選項。

若定義名稱與標準驅動同名（如 `screen|screen|RGB 0 0 0.2 0.2`），可改該驅動的預設選項，但只在直接使用該驅動時生效，經軟驅動呼叫時不影響。標準 `PLOTDRIVERS` 已用此機制讓 `SCREEN` 與 `PNG` 預設使用 PDMS 顏色。

### 31.7.5 幾個常用驅動

- `SCREEN`：預覽用，`-0` 取代輸出檔；Windows 上 `Ctrl-P` 列印、`Ctrl-S` 輸出 **EMF**（並複製到剪貼簿）。
- `PNG`：`BItmap width height`（預設 600×400，上限 8000×8000）、`LAyout`、`RGb`、`TRan`（透明背景）。
- `DXF`：選項 `HEader`、`POlylines Y/N`、`UNits`（預設 MM）、`ZAxis`；實體類型 `LINE`、`CIRCLE`、`ARC`、`TEXT`、`POLYLINE`、`VERTEX`。
- `POSTSCRIPT`／`PS`：預設 A4、單色／灰階、300 dpi；`HP`／`HPGL`／`HPGL2`：HP 用絕對座標與弦近似，HPGL 用相對座標與真圓弧。
- `PDMS`：AVEVA 偽碼檔，檔頭含使用者代號、日期、時間，輸出必須是檔案；`LIST`：輸出檔案內容摘要（格式、圖號、尺寸、用筆、圖元數量）。

常見訊息：`Cannot create/open output file`、`Cannot open input file`、`Interpretation or data error`、`Plot too large for media`（加 `ADJUST`）、`Unknown device type`；PLOT 的錯誤皆為致命。Windows 上可把 PLOT 做成桌面捷徑（`screen` 驅動、輸入檔寫 `"*"`）逐一預覽多個檔。

### 31.7.6 Draft 管理者的 Plotting Options

> 〔公開版未收錄：AVEVA 官方產品截圖〕Plotting Options 視窗：Colour correction mode、System command string、AVEVA-Plot-Service、Postscript、HPGL、Print、Other documents

*圖 31-15　Plotting Options：每個選項對應一條作業系統命令字串，檔名以關鍵字 FILE 代入。（AVEVA 官方文件截圖，僅供內部教學）*

管理者在 `Settings > Plotting Defaults` 設定使用者按 `Utilities > Plot` 時實際執行什麼命令：

- 命令字串，例如 `plotcadc FILE ps \printserver\psprint01`：`plotcadc` 是批次檔 `PLOTCADC.BAT`（用 Plot Utility 轉檔，再用 Windows `print` 送印）；`FILE` 由系統換成繪圖檔路徑；`ps` 是 PLOT 驅動名；最後是網路印表機路徑。
- 直接送預設印表機：`PlotViewer /p FILE`（列印**非真正 100% 比例**，會略小）。預覽後再印：`plotcadc FILE screen -0`，預覽視窗按 `Ctrl-P`。
- `PRINT`：用標準 Windows 列印對話方塊，不產生中間繪圖檔。
- Other Documents：輸出圖檔或 PDF（PDF 由 Acrobat Reader 開啟，須已安裝）；其他格式在 Configure viewers 以 `FILE` 代入路徑指定檢視指令（如 `mspaint "FILE"`）。**變更後要回主表單再存檔**，因為檢視器設定與繪圖選項存在一起。
- Colour correction mode：Standard、Black & White、Grayscale、Colour Plus。

> **專業提醒：** 出圖失敗要先分段排查：是 Draft 沒產生繪圖檔，還是 `PLOTCADC.BAT` 或 PLOT 轉檔失敗，還是印表機路徑與權限問題。把命令字串貼到命令提示字元手動執行，通常最快看出是哪一段。

### 31.7.7 二次開發者怎麼接

PLOT 是命令列工具，適合被外部程式呼叫：官方給出 `plot driver plotfile output [options]` 語法、`-0` 輸出到命令視窗與錯誤訊息文字；可批次轉出 PS、PNG、DXF，或用 `LIST` 驅動檢查檔案。驅動專屬選項必須加引號並以逗號分隔。PLOT 的錯誤皆為致命，但文件**未提供**退出碼數值，〔待核對〕；從 Draft 產生繪圖檔的命令只見到 `PLOT SHEE DXF filename [CUTMARKS OFF]`，完整選項〔待核對〕。

## 31.8 常見錯誤彙整

- 新建圖是空的：沒按 Update Design、Drawlist 無效或為空，或視圖界限沒涵蓋模型。
- 管理者選單看不到：不是 Draft Admin 團隊，或對存放 Library 的資料庫沒有 Read/Write。
- 找不到某 Library：`LIBY` 順序不對，或不同類型 Library 不在同一個 `DEPT`。
- AutoCAD 補的內容在 Draft 更新後消失：做在 `GT_` 層。

## 31.9 本章小結

1. Draft 的核心是「**圖庫與規則先於圖面**」：管理者備好 Library、預設值與 Backing Sheet 控制 Note，使用者才能用 Drawlist 與 Representation Rule 產生視圖與標註。
2. 預設值有層次：`DRA-SETUP` → `DRA-GEN-SYSTEM` → 使用者 `Options > Defaults`（只覆蓋不改動管理者設定）。載入分 Full 與 Partial，前者會補齊最低必要設定，後者不檢查一致性。
3. `STYL`、`RRUL`、`HRUL`、`TAGR`、`IDLI` 之間的引用關係，是排查「圖長得不對」的主要線索；`RRUL` 只能引用同一 `LIBY` 的 Style。
4. 使用者出圖以 Department → Registry → Drawing → Sheet → View 為主幹，變更設定後務必 Update Design；標註內容取自設計資料，用 Update Annotation 同步。
5. AutoDRAFT 以 DXF 與巨集檔往返；`GT_` 層屬於 Draft，不屬於你。兩種工作模式的差別在最終圖面是 AutoCAD 圖還是 Draft 圖。
6. PLOT 是命令列轉檔工具，核心語法 `plot driver plotfile output [options]`；管理者透過 Plotting Options 決定使用者「列印」時實際執行的命令。
7. 二次開發者在這一塊的可靠接口是：PML 巨集與表示式（預設值、ADP 規則）、`PLOT` 命令列、AutoDRAFT 腳本與環境變數。圖面建立與更新的 PML 命令語法在本章四份文件中未出現。

## 31.10 練習（只能在訓練專案）

1. 打開 System Defaults，列出 Master 與 Local 的 Library 指標，並與 `DRA-GEN-SYSTEM` 檔內容比對。
2. 複製 `DRA-GEN-SYSTEM` 為新檔，改一個指標，分別用 Full 與 Partial load 載入，比較錯誤清單。
3. 用 Drawing from Template 建圖，分別以 User-Defined 與 Limits-Defined View 畫同一區域。
4. 以 `PLOT SHEE DXF` 輸出一張圖，在 AutoCAD 加自建圖層內容，再從 Draft 更新並重送，確認 `GT_` 層與自建層的結果。

## 31.11 〔待核對〕彙整

1. Draft 管理團隊的實際名稱：文件同時出現 Draft Admin 與 `DRAFTADMIN`。
2. 公司 Marine 12.1 版本是否仍使用本章所述選單與預設值檔；官方原文為 PDMS 時代手冊，未逐項驗證。
3. AutoDRAFT 支援的 AutoCAD 版本（文件寫 2007、2008、2010）與公司實際版本是否相符。
4. DXF 傳輸檔英制單位手動註解的實際格式（官方原文排成 `999 P` 與 `DMS_UNITS INCH` 兩行）。
5. Hangers and Supports ADP 的 Backing Sheet 完整欄位定義（本章僅讀到前半）。
6. 以 PML 建立與更新 `DRWG`／`SHEE`／`VIEW`、讀取 Draft 屬性的語法；四份文件均未提供。
7. `Create Batch Macro` 產生的巨集內容，以及如何在背景或排程執行。
8. PLOT 的退出碼數值；以及從 Draft 命令列產生繪圖檔的完整選項（只看到 `PLOT SHEE DXF filename [CUTMARKS OFF]`）。
9. `$M/` 載入巨集的完整語法（文件僅提及）。
10. [第 9 章](ch09_drawings_zh-TW.reading.html)依據 E3D DRAW 文件撰寫，選單名稱可能與本章 12.1 官方文件不同，以本章與公司實機為準。

## 資料來源與取材覆蓋

- AVEVA Marine 12.1 離線文件 *Draft Administrator Application* [1130842]、*AutoDRAFT* [1130636]、*Drawing Production* [1132409]、*PLOT* [1132720]（英文為準，中文為機器對照）。
- 四個子樹共約 317 個頁面 ID，全部轉成文字；實際逐段閱讀：Draft Administrator 約 90／105 頁、Drawing Production 約 64／68 頁、PLOT 約 40／52 頁、AutoDRAFT 約 70／92 頁。
- **未讀或略讀：** Draft Admin 的 Change Style 與 Tag Rule 部分頁尾、H&S ADP 完整 BOM 欄位、管理者選單與附錄（以圖為主）；Drawing Production 的 Radial Dimensions 細節與附錄；PLOT 的 BENSON、CALCOMP、HOUSTON、HPGL2、LASERJET、PENMAN、XDUMP、POSTSCRIPT 完整選項與 Driver Quick Reference；AutoDRAFT 的 Symbol／Frame Editor 命令檔衍生細節、命名規則、PDMS/J 專用頁、選單頁。
- 圖片：共 15 張，皆為官方文件截圖，僅供內部教學；已實際檢視確認後加入（檔名皆以 ch31_ 開頭，存放於 aveva 圖片資料夾）。
- 本章不涵蓋：Marine Drafting、Design Draft、Marine Drafting Application Menus（由其他章處理）與 Area Based ADP（[第 28 章](ch28_other_modules_zh-TW.reading.html)）。
