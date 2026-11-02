# 第 29 章　Marine Drafting 與 Design Draft：船體與舾裝的圖面製作

> 第 27 章已經用一個概觀告訴你：AVEVA Marine 有兩套圖面工具，一套給船體（Marine Drafting），一套給舾裝（Draft）。那一章回答「圖面是什麼、為什麼能更新」；這一章回答「**圖面到底怎麼做出來**」：Marine Drafting 的圖面怎麼存、子圖怎麼分層、尺寸與註記怎麼下；Design Draft 的 `DRWG → SHEE → VIEW` 怎麼建、Id List 與表現規則怎麼決定畫什麼、剖面與標籤怎麼配合；最後把 Marine Drafting 的選單逐一對應到功能。
>
> 兩套工具思路相反：Marine Drafting 像互動式 2D 繪圖軟體，幾何真的存在圖面裡；Design Draft 把圖面當成資料庫查詢，只記「畫哪些元素、怎麼畫」，線條在更新時即時算出。弄懂這個差異，才知道哪些修改會在模型改版後存活。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的 *Marine Drafting*、*Design Draft*（Draft 資料庫指令層級手冊）與 *Marine Drafting Application Menus* 三塊。選單功能多半只讀到各頁的「用途／操作／結果」摘要；Design Draft 的指令語法與屬性名稱照文件原文保留。文件本身有幾處自相矛盾（見 附錄 D）。Draft 管理（Draft Administrator）、AutoDRAFT、Drawing Production 與 PLOT 另見[第 28 章](ch28_draft_admin_production_zh-TW.reading.html)；ISO 圖與報表見[第 27 章](ch27_drawings_zh-TW.reading.html)。**課堂練習只可在訓練專案進行。**

## 29.1 學習目標

讀完本章，你應該能夠：

1. 說明 Marine Drafting 的兩個目的，以及它與 Draft（Design Draft）的分工。
2. 說明 Marine Drafting 圖面的「雙重儲存」：PADD 資料庫與 `.SDB` 檔，並解釋 `Save Work` 為何不存目前圖面。
3. 依圖面類型（Drawing Type）判斷圖面落在哪個 `DEPT／REGI`，並設定使用者自訂類型。
4. 說明三層子圖（Subpicture）、圖層（Layer）、Drawing Reference、Envelope 的用途。
5. 用 Insert Model、拖放、Tools > Model View 系列功能，把模型放進圖面並更新。
6. 區分 Linear／Angle／Radius／Diameter／Coordinate／Curve Length／Area 尺寸，並用 Hull 專用註記標示船體零件。
7. 在 Design Draft 建立 `DEPT → REGI → DRWG → SHEE → VIEW`，用 `AUTOSCALE`／`AUTOSIZE`、Id List 與 `UPDATE DESIGN` 產生圖形。
8. 設定 `VIEW` 屬性（`VSCA`、`DIR`、`VTYP`、`RRSF`）、表現規則、自動填充與剖面（`PPLA`／`FPLA`／`SPLA`）。
9. 說明 Dimension、Label、Autotagging 的資料模型，以及 Change Highlighting 如何標出改版。
10. 讀懂 Marine Drafting 十四個功能表的結構，並指出哪些功能是 PML／Vitesse 的客製化切入點。

## 29.2 Marine Drafting：概念與資料結構

### 29.2.1 它是什麼

官方文件給 Marine Drafting 兩個目的：一是提供自動、半自動與手動的繪圖工具，建立造船過程中**任何類型**的圖；二是作為 Hull 建模活動的**介面**：圖面是在模型被定義的同時產生的。系統涵蓋三件事：

系統涵蓋三件事：檢視模型資訊（船體、管路、設備、電纜托架、組件）並投影剖切成去除隱藏線的 2D 圖；一般 2D 繪圖（也常用來替模型視圖加尺寸與標籤）；圖面上的模型投影連回模型物件，模型改了可重建、註記可自動更新。

文件還說明，Draft 的多數功能可經由「自動圖面產生（ADP）」讓 Marine Drafting 使用者取得。ADP 涵蓋一般圖、組裝圖、管路草圖、HVAC 草圖與鋼構細部圖，各自用 PML 客製化（見第 28 章）。已知差異：Marine Drafting 內的 General ADP 與 Draft 版本長相不完全相同，因為刻意讓成果**與手動建立的圖相容**，尤其是尺寸，這樣才能再用 Marine Drafting 的尺寸功能修改；另已知限制是不支援尺寸中的引線文字（Leader line text）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull Drafting 主視窗：左側 Design Explorer 與 Draft Explorer，中央 2D Canvas，下方 Messages 與工具列

*圖 29-1　Marine Drafting（視窗標題為 Hull Drafting）主視窗：選單列、左側 Explorer、中央畫布、下方訊息窗與兩列工具列。（AVEVA 官方文件截圖，僅供內部教學）*

### 29.2.2 圖面的「雙重儲存」與三個重要規則

一張 Marine Drafting 圖面由兩部分組成：**資料庫部分**與**另存成檔案的部分**。儲存圖面時做兩次儲存：一次進 PADD 資料庫，一次存成個別 `.SDB` 檔。

| 項目 | 說明 |
|---|---|
| PADD 資料庫 | 圖面依部門（`DEPT`）與登錄冊（`REGI`）組織；Draft 的元素樹見 29.5 |
| `.SDB` 檔 | 放在 `<專案名>drg` 資料夾下的子資料夾；每次儲存產生新版本，預設刪掉舊版 |
| `KEEP_SESSION_FILES` | 預設關鍵字設為 `YES` 才保留舊版，可做 DABACON 的 roll back，但檔案會膨脹 |
| 清除過期 `.SDB` | 可用管理員的 Merge Session 指令，或 PML 表單 `show !!RemoveObsoleteSDB`（需 FREE 權限、無其他使用者連線） |

三個重要規則，每個都會影響工作流程：

1. **只有「已持久化」的圖面才能做模型更新。** 從 Command Window 下的指令不保證圖面被持久化；文件的態度是：除非某指令明文標示給 Marine Drafting 使用者，否則不要用 Command Window（View 選單的 Command Window 頁也註明「不建議在 Marine Drafting 使用」）。
2. **`Save Work` 不存目前圖面。** Marine Drafting 以「目前圖面」為工作單位，它放在排除清單中，不受 `Save Work` 影響；要用 `Save Drawing` 或 `Save Drawing As`。反過來，`Save Work` 用來存「圖面中建模」所產生的**模型物件**。
3. **圖面擁有權：存進 Marine Drafting 就是 Marine Drafting 的圖。** 無論是手繪、ADP、開啟 Draft 做的圖或匯入，只要存進 Marine Drafting，就視為它的圖，**不應再回 Draft 更新**。

> **專業提醒：** 規則 2 是新手最常踩的坑：改了船體模型（Save Work）以為圖也存了，結果關閉後圖面沒變；或存了圖卻忘了存模型。養成固定順序：`Save Work`（模型）→ `Save Drawing`（圖面）。

### 29.2.3 圖面類型與落點

圖面存放的 `DEPT／REGI` 由圖面類型決定：優先用 `DEPT` 的 `PADDXP` 屬性（編譯過的 PML 運算式，如 `set PADDXP (marpty eq 1)`）找部門；找不到就取 `d065` 檔的環境變數（如 `SB_PDB_PADD = General;MarDwg`，分號前為 `DEPT`、後為 `REGI`；`REGI` 永遠由環境變數取得）；都沒有就用內建名稱，元素不存在會自動建立。自 12.1SP4 起，環境變數中的 `<DEPT>` 只在沒有符合的 `PADDXP` 時才作備援。每個類型還要有一個「值等於自己名稱」的環境變數（如 `SP_PDB` 設成 `SP_PDB`）。

系統類型約 30 種，例如：1 General Drawing（`SB_PDB`）、3 General Subpicture、4 Assembly Drawing、7 Pipe Sketch、8–16 與 17–20、26、27 的各種 Hull 圖（重量重心、零件表、型材草圖、套料、治具、彎曲樣板、平面／曲面零件、驗收、標記文字）、21 Settings、22 Drawing Form、23 Standard Subpicture，以及 28–33 的各類 ADP 圖（Assembly、HVAC、Isometric、Steelwork Detailing、Area-Based、Multi-Discipline）。完整對照見官方 Drawing Types 附錄。

**自訂類型：** 準備文字檔，每行 `<類型號>,<描述>`（類型號 1001–1999，例 `1001,ClassDwg`），用環境變數 `SB_DRAWINGTYPE_LIST` 指向它；落點同樣由 `PADDXP` 或 `SB_PDB001_PADD = EarlyDesign;ClassDwg` 控制。

### 29.2.4 三層子圖、圖層與 Drawing Reference

圖面是三層**子圖（Subpicture）**的階層：第 1 層（View）、第 2 層（Sub-view）、第 3 層（Component），所有幾何都在第 3 層之下。三層永遠存在，可用 Create、Split、Regroup 自由重組，用來整組移動、刪除、換色。

> 〔公開版未收錄：AVEVA 官方產品截圖〕圖面階層：Drawing 之下為第 1 層 View、第 2 層 Sub-view，最底層為 Geometry

*圖 29-2　三層子圖階層。所有幾何（G）都在最底的第 3 層之下。（AVEVA 官方文件截圖，僅供內部教學）*

模型投影加進圖面時，每個投影視圖（第 1 層）自動依固定結構建立第 2 層子視圖：**Hull parts、Curved panels、Hull surfaces、Fairing curves、Draft、Assemblies**。使用者加的 2D 資訊放進「目前選取的子圖」或「最近的子圖」：選在第 1 層，每個新實體都會建立新的第 2、3 層；選在第 2 層，只建立第 3 層。

| 概念 | 說明 | 重點 |
|---|---|---|
| 圖層（Layer） | 以數字識別的圖元群組，可隱藏或顯示；用 Layer Alias 檔（`SB_LAYER_ALIAS`）加文字描述 | 系統圖層為**負數**，使用者圖層為**正數** |
| Layer Class | 外部檔（`SBD_LAYER_CLASS`）定義，把尺寸、註記、位置編號、填充、2D 幾何、文字、符號各指到某圖層 | 類別未涵蓋的項目，其圖層為「未定義」 |
| 系統圖層 | `-1` 尺寸、`-2` 位置編號、`-3` 註記、`-4` 構造線、`-6` 隱藏線、`-9` Markup、`-11` 標籤、`-202` 填充、`-212` Cloud | 圖面表單為 `-300` 系列；投影為 `-1001`～`-1006`，船體零件有 `-1101` 起的專屬層 |
| Drawing Reference | 在目前圖面「引用」另一張圖（常當底圖）；可 Collapse（只存引用）／Expand | 儲存時自動 Collapse；列印一定會印出被引用的圖；被引用的圖受保護不可改；**不能引用已有引用或子圖的圖** |
| Envelope | 暫時把某個子圖換成同大小的外框符號，加快大圖操作 | 圖面大小不變、資料保留 |
| 標準細節 | 任何子圖可存為 Standard Detail（`SB_STD`），使用者填充樣式也存此處 | `Tools > Subpicture > Save as std detail` |

### 29.2.5 圖面表單與動態文字規則

圖面表單分「Modelling drawing form」（含投影配置，如 CV4）與當背景的一般表單。動態文字用規則：`$2000` 這類單項規則（`$` 加整數）會被取代為圖名，`@600` 這類表格規則（最多 20 列）用於版次表；取代時沿用原文字的位置、高度與旋轉。規則編號只在同一張表單內有意義。建立流程：`File > New` 畫版面（規則文字以 `$`／`@` 開頭）→ `Tools > Drawing Form > Save`；改舊表單用 `Tools > Drawing Form > Open`（以 `F_<表單名>` 開啟）。批次填文字用 `SY006`，自訂規則建議從 10000 起算以免衝突。

> 〔公開版未收錄：AVEVA 官方產品截圖〕圖面表單的欄位與規則編號對照：圖號 $2000、標題 $2101、繪製者 $2102、日期 $2104、比例 $2108、版次 $2112 等

*圖 29-3　圖面表單的欄位與規則編號對照（例：Drawing no 為 $2000）。（AVEVA 官方文件截圖，僅供內部教學）*

## 29.3 Marine Drafting 的操作

### 29.3.1 日常工作流程

`File > New Drawing`（預設名 `UNTITLED1`，不改名視為「系統命名」，之後 `Save Drawing` 會跳出另存對話框）→ `Insert > Drawing Form`（插入後自動 AutoScale）→ `Insert > Model` 或拖放放入模型 → `Tools > Model View` 調整視圖 → `Dimension`、`Annotate` 標註 → 模型改版後用 `Tools > Model View > Update Design／Annotations／All` 更新 → `Validate` 檢查（以**時間戳**判斷）→ `Save Work`（模型）加 `Save Drawing`（圖面）。

### 29.3.2 放入模型：Insert Model 與拖放

`Insert > Model` 開啟 Model Selection 對話框：反覆選型別、輸入名稱（可用逗號分隔、可含萬用字元）與模組來收集模型，空白名稱或模組代表「符合任何」。拖放則等價於 Insert Model：圖面必須以讀寫模式開啟；左鍵從 Design Explorer 拖到 2D Canvas，**沒有視圖會要求選投影；落在某視圖內只更新該視圖；落在視圖外則更新或插入所有視圖**；右鍵拖放則詢問 `New view…`／`Selected view`／`All views`。選投影的方式有：Same As View、Point Vector、Three Points、Two Cursor Positions、3D Rotate、預設投影（系統可預先定義 5 個標準投影，並有 `-1001`～`-1005` 對應圖層）。

### 29.3.3 尺寸與註記

尺寸分七類：**Linear、Angle、Radius、Diameter、Coordinate、Curve Length、Area**。版面參數由預設檔初始化（前綴 `DIM_LIN_`、`DIM_ANG_`、`DIM_RAD_`、`DIM_DIA_`，如 `DIM_LIN_DEC` 小數位、`DIM_LIN_ARROW` 箭頭、`DIM_LIN_TEXTH` 文字高度），可在功能內或 `Format > Defaults` 修改。

- **2D Linear 三型：** Normal（連續點之間，同一尺寸線）、Chain（基準點到各點）、Staircase（同方向、不同尺寸線）；3D Linear 永遠是 Normal。
- **Radius／Diameter：** 各有 straight、knuckled、cross 三型；Linear／Angle／Diameter／Radius 可加對稱或不對稱公差。
- **3D 專用：** Weight and COG、Shell Profile Mounting Angle（邊別由 `DIM_ANG_SHELL_PROF_SIDE` 控制）、Distance to RSO。
- **Hull Mould Line：** 從模線量測，箭頭標示材料側，**只能用在符號化船體視圖**，箭頭線長由 `MOULD_LINE_ARROW_LENGTH` 控制。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Dimensioning : Linear 2D 對話框：方向、型式、公差、文字與箭頭版面、Blank out 與 Margin

*圖 29-4　Dimensioning: Linear 2D 對話框。可選方向、型式（Normal／Chain／Staircase）、公差與遮蔽。（AVEVA 官方文件截圖，僅供內部教學）*

`Annotate` 分**通用註記**（General Note、Position Number、Label、Autotagging、Markup、Ruler、Cloud…）與**船體專用 Hull Note**：Pos No、Assembly（所屬組件）、Bevel、Grinding（孔磨平符號）、Hole Dimension（Panel 孔的標記與尺寸，在 Hull View 中是關聯式的，View 重建時更新）。

**Config Note（可設定註記）** 由 Vitesse hook 設定：檔名固定為 `_TBhook_ConfigNote.py`，放在 `PYTHONPATH` 指的目錄，必須有五個固定方法：`getNoteName (<NoteInd>)`、`getNoteChar (<NoteInd>)`、`getNoteFilter (<NoteInd>, <FilterInd>)`、`getNoteData (<ItemNo>)`、`setNoteData (<NoteNo>, <ModelType>, <Model>, <PartType>, <Part>, <SubPartType>, <SubPart>)`，**輸入參數與回傳值不可更動**。

> **專業提醒：** 註記符號必須先存在：Note 符號用標準符號字型 #21 的 31–60 號，位置編號符號用 61–80 號；要更多就用 #41 字型並以 `NOTE_SYMB_EXTENDED_RANGE`、`POSNO_SYMB_EXTENDED_RANGE` 啟用。

### 29.3.4 選取、修改與常用輔助功能

**Multiple Select（多重選取）：** 在 Choose function 模式下，Ctrl＋左鍵加入或移除（來自 Drawing Reference View 的資訊不能加入）；Ctrl＋右鍵開選項選單：`Box`、`Polygon`、`Inside`、`Crossing`、層級過濾（Comp／Subview／View）、幾何過濾（Contour／Text／Symbol）與 `Advanced filter…`（顏色、線型、字型、文字高度、圖層等，**多個條件須全部符合**）。可多選的功能：Trim、Extend、Transform、Copy、Delete、Change Properties。

> 〔公開版未收錄：AVEVA 官方產品截圖〕多重選取的彈出選單：Comp／Subview／View、Contour／Text／Symbol、Box／Polygon／Inside／Crossing、Advanced filter

*圖 29-5　Multiple Select 彈出選單。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 設了 `Advanced filter` 後，**所有操作都作用在「過濾後」清單，而不是畫面上高亮的「選取」清單**（可用 Show selected／filtered elements 切換）。Delete 時尤其危險。Copy 是否排除模型資訊，由預設關鍵字 `MODEL_SUBPICTURE_2DREGROUP_ALLOW` 決定。

**Trim／Extend：** 單一輪廓不必先選，在輪廓附近按右鍵即可；找到兩個交點就挖出缺口，只找到一個就修掉靠近點擊位置的那端。**其他：** 3D 點定義有鎖定（LOCK U／V／X／Y／Z／XY…）、`Add (3D) Offset`、`Verify`；點、線、弧的定義是遞迴的；字串輸入框可用 `!CANCEL`、`!OC`、`!GRAPHIC` 等指令；列印時可用 `SBD_LSFILE` 改輸出線型而不改圖面。

### 29.3.5 匯入匯出

2D DXF／IGES 只處理 2D：DXF 匯出時符號與註記被炸開、Chain 與 Staircase 尺寸拆成單一尺寸，預設全在圖層 0，可用五欄的圖層控制檔（模型類型、圖層名、顏色、線型、線寬）分層；DXF 匯入以 R12 為基礎，複雜線型只會畫成實線。3D DXF 只匯出**船體模型**（舾裝模型需另購的 Explant-A 或 Mechanical Equipment Interface），檔案很大，帶孔 Panel 約為無孔的 3 倍。

## 29.4 Marine Drafting 的維運與二次開發切入點

### 29.4.1 預設檔與批次公用程式

Drafting 的預設值存在**預設檔**，由環境變數 `SBD_DEF1` 指定，啟動時讀入；每行「關鍵字 冒號或等號 值」，順序無關。其他設定檔：圖層別名檔 `SB_LAYER_ALIAS`、圖層類別檔 `SBD_LAYER_CLASS`、軟度別名檔 `SB_MTRL_ALIAS`。線型顯示由 `SB_LINETYPE_THIN_WIDTH`（0.125 mm）、`WIDE`（0.25）、`XWIDE`（0.5）等一組環境變數控制，應集中維護，同時影響螢幕與列印。

| 公用程式 | 用途 | 重點（照文件） |
|---|---|---|
| `SY013` | 把 Tribon M3 輸出的 `.SDB` 遷入 PADD | `sy013 <登入資訊> -name <物件> -dwgtype <類型號> [-list] [-onlyfromfiles]`；舊 `TBSystemFont` 需用 `TB_SYSTEMFONT_MAP` 對應到 TrueType |
| `SY015` | 批次複製圖面 | `sy015 -from <SHEE／DRWG／REGI／DEPT> -to <REGI／DEPT>`，可加前後綴與 `-logfile` |
| `SY007` | 舊版圖面一次驗證 | 圖面版本為 8，低於 8 不支援 |
| `SY010` | 檢查並修復損毀圖面 | `sy010 [-name] [-sourcedb] [-report｜-repair] [-logdir] [-targetdb]`；嚴重度 Fatal／Error／Warning／Informational |
| `SB028`、`TBGENPREVIEW` | 管理標準資料庫頁面；產生開啟對話框的預覽圖 | `SB028` 需要名為 `STDFORM` 的表單 |

> **專業提醒：** `SY010` 預設把修復結果存回原資料庫、**覆蓋原圖**。一律先加 `-report` 看診斷，要修再用 `-targetdb` 存到別處；Fatal 等級可能無法復原。

**備份與還原：** 圖面檔可隨 Datal 一起備份：先 `OUTPUTDRAWINGS "資料夾"` 開啟（預設關閉），只支援完整清單，備份時**一定要用 `SAMEREF`**。還原時先確認元素不在資料庫、導航到擁有者、執行 DB 清單巨集（內含 `LOADDRAWINGS`）後 `SAVEWORK`；還原元素的 `PVNO` 要大於歷史值，預設只往回掃 100 個 Session，可用 `AVEVA_RESTORE_MAXSESSIONS` 加大。還原後的圖面可能與目前 Design 不一致，需驗證，或把 MDB 以 Backtrack 退回指定 Stamp（見[第 43 章](ch43_system_administration_zh-TW.reading.html)）。

### 29.4.2 二次開發者怎麼接

只列文件有明確依據的切入點，其餘標〔待核對〕。

| 切入點 | 文件依據 |
|---|---|
| Config Note hook | Vitesse（Python）檔 `_TBhook_ConfigNote.py`，五個固定方法（29.3.3）；資料形態與回傳型別細節未讀〔待核對〕 |
| Model Info 客製 | PML pre-trigger `trig_draft_model_info` 與 `ModelInfo` 物件，方法：`DBREFGET()`、`ADDPROPERTY(STRING, STRING)`、`REMOVEPROPERTY(REAL)`、`MODELINFOPROPERTIES()`、`PROPERTYTITLE(REAL)`、`PROPERTYVALUE(REAL)`、`EDITPROPERTYTITLE(REAL, STRING)`、`EDITPROPERTYVALUE(REAL, STRING)`；標題必須唯一 |
| Vitesse 腳本 | `Tools > Vitesse > Run Script`，位置由 `SB_PYTHON` 定義；可用的 Marine Drafting API 未讀〔待核對〕，見[第 36 章](ch36_hull_vitesse_zh-TW.reading.html) |
| 批次 | `SY013`、`SY015`、`SY010`、`SY006`，都需附專案登入（`-proj=MAR -user=SYSTEM -pass=… -mdb=/ALL_NO_MDS`） |
| ADP 與預設檔 | `AutoDP` 表單以 PML 客製（第 28 章）；`SBD_DEF1` 可統一發佈 |

> **專業提醒：** Marine Drafting 圖面不能用 Command Window 隨意改（29.2.2）。想程式化改圖，走上表的 hook、批次與 Vitesse，不要把 Design Draft 的指令（29.5 起）直接用在 Marine Drafting 圖面上。

## 29.5 Design Draft：資料庫與圖面建立

### 29.5.1 Design Draft 是什麼

Design Draft 產出完整註記、按比例的圖，內容取自 Design 模型並與其完全整合；可從任意方向看模型，隱藏線自動移除或改線型，一張圖可同時有平面、立面與等角視圖。圖由三種圖形構成：代表 3D 模型的圖形、多張圖共用的底圖與覆蓋圖（backing／overlay sheets）、註記（尺寸、文字、引線與標籤框）。

**Draft 資料庫不存幾何**，只描述圖形該如何呈現；圖面由它加上 Design 與 Catalogue 資料庫即時產生，反映當下設計狀態。本文件是**指令層級**手冊，寫給要自訂圖形介面的人；GUI 操作見第 28 章。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Draft 資料庫階層全貌：WORLD 之下有 LIBY、DEPT、REGI、REPO、DRWG、SHEE、VIEW 與 LAYE 底下的註記元素

*圖 29-6　Draft 資料庫階層（Basic Hierarchy，已省略自動建立的系統元素）。圖面元素由 `DEPT → REGI → DRWG → SHEE → VIEW → LAYE` 向下，右側 `LIBY` 放圖庫。（AVEVA 官方文件截圖，僅供內部教學）*

| 元素 | 意義 |
|---|---|
| `DRWG`／`SHEE` | 圖面（相當紙本圖）／圖紙（「第 1 張，共 3 張」），可顯示於視圖的最高層元素 |
| `VIEW` | 3D 模型某部分的投影，屬性含視線方向、通過點、比例、紙上大小與位置，並參照 Id List 決定畫什麼 |
| `LAYE` | 圖層，擁有尺寸、標籤與視圖註記；`PURP` 決定可擁有的元素，`LVIS` 控制顯示，共用屬性由圖層向下串接 |
| `LIBY`／`DLLB`／`IDLI` | 圖庫、Drawing List Library、Id List |
| `RPLB`／`RRST`／`RRUL`／`STYL` | 表現規則庫、規則集、規則、樣式（29.6） |
| `PLLB`／`PPLA`／`FPLA`／`SPLA`／`VSEC` | 剖面庫、三種剖面、視圖剖面（29.6） |
| `SHLB`／`BACK`／`OVER` | 圖紙庫、底圖樣板（當圖框）、覆蓋圖樣板（疊關鍵位置圖） |

### 29.5.2 建立圖面骨架與產生圖形

從 World 開始，用指令建立階層：

```
NEW DEPT /PIPES
NEW REGI /PIPREG
NEW DRWG /PD101
NEW SHEET /SHEET1
NEW VIEW /PLAN
```

若只有一個部門、一個登錄冊與一張圖紙，**除 `NEW DRWG` 與 `NEW VIEW` 外都可省略**；缺少的管理元素會自動建立。決定 `VIEW` 內容有兩法：直接參照單一 Design 元素（小到一個 `BRANCH`、大到整個 `SITE`），或間接參照 **Id List**（`IDLI`）。

**`AUTOSCALE` 與 `AUTOSIZE`** 是兩個「自動」指令，一次設好三項關鍵屬性：

| 指令 | 設定的屬性 | 使用現有的 |
|---|---|---|
| `AUTOSCALE [元素或 IdList]` | `IDLN`（若尚未設定）、`THPO`（通過點）、`VSCA`（比例，使內容剛好放進視圖框） | `DIR` 與 `SIZE` |
| `AUTOSIZE [元素或 IdList]` | `IDLN`（若尚未設定）、`THPO`、`SIZE`（視圖框大小） | `DIR` 與 `VSCA` |

也可用 `AUTOSCALE LIMITS OF /idlist` 或 `AUTOSIZE FROM position TO position` 以範圍而非設計項目計算。注意：`IDLN` 只在**尚未設定時**才被改，第二次執行不會換清單。

屬性設好後，**`UPDATE DESIGN`** 在記憶體的 Central Picture Store（CPS）建立視圖圖形，**`SAVEWORK`** 把圖形存成 Picture File，下次工作階段不必重新更新。

> **專業提醒：** 以 `QUIT` 離開 Draft，CPS 中的圖形**不會存**；切換到另一個模組則隱含 `SAVEWORK`。

### 29.5.3 Id List 與視圖屬性

Id List 放在 Drawing List Library（`DLLB`），用 `ADD`／`REMOVE` 建立（系統自動產生 `ADDE`／`REME`）：

```
NEW LIBY /LIB1
NEW DLLB /DLB1
NEW IDLI /ID1
ADD /ZONE.PIPES2-1
REMOVE /PIPE2-1-12
```

- **順序很重要：** 被移除的項目必須先被（隱含地）加入，`REMOVE` 不應是第一筆；用另一個清單移除一批分支時，那個清單要用 `ADD /BRAN1, /BRAN2` 定義，**不要**寫成 `REM`。
- **選取語法：** `ADD ALL EQUI FOR /SITE/99` 是**展開後**存入，清單可能很長；加 `RULE`（`ADD RULE ALL ZONE WITH ( FUNC EQ 'PIPING')`）則把條件存在 `CRIT`，到 `UPDATE DESIGN` 才展開。
- **空間範圍：** `ADD ... WITHIN E5000 N5000 U5000 TO W1000 S1000 U0` 用 Marine 空間地圖；地圖不是最新，結果會錯。較穩定的做法是設 `IDLI` 的 `LIMI`（`LIMITS` 指令）並只加入相關 `SITE`／`ZONE`。
- **清理與查詢：** `DELETE NULL IDLIstmembers`；`Q IDLN DESC`、`Q VOLUME`、`Q WINDOW`。網格系統（`GRIDSY`／`GRIDAX`）可加進清單但不能是唯一成員。

主要 `VIEW` 屬性（改了視線、通過點、旋轉或透視後，圖形即過期，需 `UPDATE DESIGN`）：

| 屬性／指令 | 意義 |
|---|---|
| `LFRA`、`SIZE`、`VREGION` | 視圖框是否顯示（預設 OFF）、紙上大小、用游標框選大小 |
| `XYPS`、`ONPOS` | 視圖中心在圖紙上的位置；內容中心相對視圖中心的偏移 |
| `VSCA`、`VRAT` | 比例（值越大圖形越大）；`VRAT 1 TO 75` 以比值設定，直接設 `VSCA` 會使 `VRAT` 失效 |
| `ADEG`／`TURN`、`RCOD`、`PERS` | 內容旋轉（相對 0，不是相對上次）、連視圖一起旋轉、透視（預設 0 為平行投影） |
| `DIR`、`THPO`、`FRPO` | 視線由方向、通過點、起點任兩項決定，如 `LOOK N45W`、`ISO3`、`PLAN` |
| `RRSF`、`HRSF`、`CRSF` | 參照表現規則集、填充規則集、變更規則集 |
| `ATOL`、`VGAP`、`NOCLIP`、`IGNDUN` | 弧容許誤差、視圖線缺口（預設 1.5 mm）、不裁切、忽略 `DUNION` |
| `VTYP` | 隱藏線表現，見下 |

**`VTYP` 六種等級**（精確度與運算成本遞增）：`WIRE`（線框，預設）→ `MWIR`（modelled wireline）→ `WIREHL`（僅對各重要元素移除自身隱藏線）→ `LOCAL` → `GLOBAL`（全域移除隱藏線）→ `UNIV`（Universal：全域，並補上互相穿透之重要元素的交線）。初稿用低等級，定稿才用高等級。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Wireline 視圖：所有邊線可見，含隱藏線

*圖 29-7　`VTYP WIRE`：傳統線框圖，所有邊都畫出。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Universal HLine 視圖：全域移除隱藏線，並補上穿透交線（紅圈處）

*圖 29-8　`VTYP UNIV`：移除全部隱藏線，並產生衝突元素之間的交線（紅圈為補上的交線）。（AVEVA 官方文件截圖，僅供內部教學）*

**2D 符號化與查詢：** 在 2D 視圖中，設計元素可用符號代替或附加於幾何；符號由符號樣板（`SYTM`）與文字標籤樣板（`TXTM`）產生，**用哪個樣板記在 Catalogue 資料庫**，故同一元素可依視圖方向與分類有不同表現。符號以 `DESSYM` 放進 `DSLAYE`，由 Draft 自動建立與刪除。`Q VSCAN`、`Q FIND gid IN view`（回答 `FOUND`／`MISSING`／`INVALID ELEMENT`）可查某元素是否出現在視圖；可見性是掃描**圖形資料**而非 Id List，被隱藏線移除的元素找不到，只擁有別的重要元素而無可見圖元的 `EQUI`、`STRU`、`FRMW` 也找不到。

### 29.5.4 背景處理管理員（BPM）

更新很費時時，可用 Background Process Manager 在背景更新，前景可繼續做別的視圖；前景與 BPM 不必同時運作（可夜間跑），一次只跑一個工作。前置條件是環境變數 `PDMSEXE`、`PDMSWK` 與專案的 `XXX000`、`XXXISO`、`XXXMAC`、`XXXPIC`，並用 `BPM.bat` 啟動。

流程：在 Draft 導航到 `VIEW`（或 `SHEET`、`DRAWING`）→ `SAVEWORK` → `UPDATE Design NOWAIT` 加入佇列 → BPM 表單點 `Start manager`（背景用隱藏 Draft 工作階段，每個視圖產生前綴 `X` 的中間視圖檔 IVF）→ 完成後回前景用 `UPDATE REFRESH` 取回，滿意才 `SAVEWORK`，不滿意則**不要存**，重新選取圖紙載回舊內容。log 存於 `PDMSWK`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Background Process Manager 表單：工作清單、Manager status、Start manager、Manager log

*圖 29-9　Background Process Manager 表單：上方為工作清單與狀態，下方為 Manager log。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 重新整理某視圖前，先存好同圖紙其他視圖尚未儲存的變更，否則重新載回圖紙會一併捨棄。另：Design 資料庫刪除重建後，可用 `UPDATE 元素 REFS` 依系統文字屬性 `DDNX`、`IDLX`、`IDNX` 恢復參照，前提是被參照元素都有名稱。

## 29.6 Design Draft：表現規則、填充與剖面

### 29.6.1 表現規則與樣式

表現規則（`RRUL`）決定每種設計元素怎麼畫並參照樣式（`STYL`）；規則存在規則集（`RRST`），規則集與樣式存在表現規則庫（`RPLB`）。`VIEW` 以 `RRSF` 參照規則集，或直接擁有**本地規則**，本地規則優先於庫規則。

> 〔公開版未收錄：AVEVA 官方產品截圖〕表現規則階層：Library、RPLB、RRST、RRUL、STYL，與 VIEW 的 RRSF 及 RRUL 的 STYF 參照

*圖 29-10　表現規則的資料庫階層：`VIEW` 以 `RRSF` 指向 `RRST`，`RRUL` 以 `STYF` 指向 `STYL`。（AVEVA 官方文件截圖，僅供內部教學）*

樣式屬性包括：旗標 `TUBEF`、`CLIN`、`PSYM`、`OBSTF`、`INSU`、`PRFG`、`PLFG`，以及成對的樣式與顏色：`FFSTYLE`（正面邊，預設 SOLID／1）、`CLSTYLE`（中心線，預設 CHAIN／1）、`BFSTYLE`（背面邊，預設 OFF）、`OBSTYLE`（被擋住的正面邊，Global 隱藏線視圖用，預設 OFF）、`PLNSTYLE`（P-line）、`MLNSTYLE`（構件中心線）、`PINSSTYLE`（保溫，`INSU` 為真才畫）。

```
NEW RRST /RSET1
NEW RRUL /R11
USE /S2 FOR ALL EQUIP
OMIT ALL BRAN WITH ( HBORE LE 80 AND TBORE LT 30 )
```

Draft 由上往下掃規則清單，**第一個符合的規則生效**；沒有符合者就用預設樣式。因此**特定規則放前面**：先寫小口徑規則，再寫 `USE /ST2 FOR ALL BRAN`。`OMIT` 設定 `OMITFG` 並取消該規則的 `STYF`。指定具名元素（`USE /S2 FOR /PUMP1-1`）時**元素必須有名稱**，`CE`、`FIRST EQUI` 不行。條件用 PML 運算式（`EQ`、`NE`、`LT`、`LE`、`GE`、`GT`、`AND`、`OR`、`NOT`）；一次套用多類別要加括號：`USE /ST1 FOR (ALL BRAN ALL SUBS) WI (…)`，否則條件只作用在最後一類。2D 符號化用 `USE SYMBOLOGY FOR crit`。網格線若要不被隱藏線處理遮擋，規則要套在 `GRIDSY`／`GRIDAX`（並把 `RRUL` 的 `NoHLRFlag` 設為真），**不要套在 `GRIDLN`**。

### 29.6.2 自動填充（Automatic Hatching）

被剖面切出的面與指定圖元表面，可由填充規則自動畫填充，屬 `UPDATE DESIGN` 的一部分。結構與表現規則平行：`HRUL`（規則）→ `HSTYL`（樣式）→ `HRST`（規則集）→ `RPLB`，`VIEW` 以 `HRSF` 參照或直接擁有本地 `HRUL`。

- **規則屬性：** `HSTYF`、`FCODE`（`SECTionedfaces`／`PRIMitivefaces`）、`DCODE`（All／Perpendicular／Specified 方向）、`NORM`、`CRIT`。
- **對象與限制：** 剖面填充要選**重要元素**（`BRAN`、`EQUI`、`SUBS`、`FRMW`…），選 `BOX`、`VALV` 不會有填充；一條規則只能二擇一（剖面面或圖元表面）；一個設計元素只套用**一條**規則。
- **樣式：** `OLSTYLE`（外框，預設 Off）、`FSTYLE`（預設 `SYSTEM PATTERN 1`）、`PIPESYM`（預設 TRUE，切到圓或矩形管時畫典型剖面符號，關掉才改用一般填充）；填充角度與間距是絕對值，不受比例影響。

### 29.6.3 剖面（Section Planes）

文件指出 GUI 有大量剖面功能（見第 28 章），本節是資料庫層。三種元素構成四種剖面：

| 剖面 | 元素 | 定義 |
|---|---|---|
| 垂直平面 | `PPLA` | 只有 `POS`，永遠垂直於視圖方向；不能反轉動作 |
| 平面 | `FPLA` | `POS` 加 `NORM`（法向量，如 `N45W`、`ISO2`） |
| 階梯平面 | `SPLA`（`GTYP OPEN`） | 由 `WPOS` 點序列構成折疊平面，沿 `DIR` 無限延伸 |
| 封閉平面 | `SPLA`（`GTYP CLOSED`） | 首尾點重合，形成無限長的管 |

平面存放在平面庫（`PLLB`），可供多個視圖使用，且**只能用在 modelled 視圖**（`VTYP` 為 `MWIR` 以上），不能用在基本線框視圖。

> 〔公開版未收錄：AVEVA 官方產品截圖〕階梯平面：一列點定義的折疊平面，兩端延伸至無限遠

*圖 29-11　階梯平面（Stepped Plane）：十字為定義平面的點，箭頭表示延伸到無限遠。（AVEVA 官方文件截圖，僅供內部教學）*

視圖要用剖面，需在 `VIEW` 下建 `VSEC`：`PLRF`（平面）、`IDLN`（要剖的清單，預設整個 World）、`PMOD`（`STANDARD`／`REVERSE` 反轉保留側／`OFF`）、`CLMO`（設為 OFF 則管路元件的線元素不被剖，管件被切掉仍留中心線）。視圖屬性 `SMOD` 設為 `OMIT FRACtional PCOMponents` 時，原點落在前後剖面外的管件整個省略。階梯平面用 `NEW SPLA`、`DIR U`、`GTYP OPEN`、`STEP @ @ @ @` 建立（一次最多四點，可追加）；系統會檢查並回報 `Splane /name is satisfactory`，自身重疊則需調整點序或改成封閉型。`CHANGE ACTION` 反轉平面本身的保留側（不同於改 `VSEC` 的 `PMOD`，後者只影響該視圖）；`SKETCH PLANE` 在視圖畫出平面當繪圖輔助。

> 〔公開版未收錄：AVEVA 官方產品截圖〕同一設備以不同階梯剖面切開的結果：上下兩組各為平面視圖與等角視圖

*圖 29-12　階梯剖面的使用結果：同一設備以不同折疊剖面切開，斜線為剖面填充。（AVEVA 官方文件截圖，僅供內部教學）*

### 29.6.4 游標、輸出與顏色樣式

- **游標辨識：** `ID @` 選最底層元素；`ID DESEL／PADEL／DRAEL @` 限制只選 Design 或 Draft 元素；`IDP @`、`IDPL @`、`IDPE/ND @` 取 P-point 與 P-line，例：`NEW GLAB ON IDPE @`。
- **2D 與 3D 座標互查：** `Q ENUPOSITION OF 紙上位置`、`Q SHPOSITION OF 位置`；視圖必須是**非透視的軸測圖**且位置在視圖框內。
- **輸出：** `PLOT /SHEET1 /SH1.PLT A3 OVER`；延伸格式有 `PDF`、`IMAGE`、`METAFILE`、`PRINT` 與 DXF／DWG（`LIEXEC /Draft_DXF_LI 'DXFOUT' ConfigData '…'`）。已知限制：智慧遮蔽圖元不輸出、許多自訂線型被轉成固定虛線。PLOT 與各格式設定見第 28 章。

## 29.7 Design Draft：註記、標籤與改版標示

### 29.7.1 註記的資料模型

註記元素包括尺寸、標籤與 2D 繪圖元素。**尺寸與標籤由圖層（`LAYE`）擁有**；其他文字、符號、圖形由 `NOTE`（圖紙註記）或 `VNOT`（視圖註記）擁有。圖層的 `PURP` 決定可以放什麼，`LVIS` 控制整層顯示。

> 〔公開版未收錄：AVEVA 官方產品截圖〕註記元素階層：SHEE 之下有 NOTE 與 VIEW，VIEW 之下 LAYE 擁有 VNOT、尺寸（ADIM、LDIM、PDIM、RDIM）與標籤（SLAB、GLAB），另有 DSLAYE 與 DESSYM

*圖 29-13　註記元素階層：2D 繪圖元素（`TEXP`、`SYMB`、`CIRC`…）、尺寸元素與標籤元素各歸其類。（AVEVA 官方文件截圖，僅供內部教學）*

### 29.7.2 尺寸

`LDIM`（線性，擁有 Dimension Point）、`RDIM`（半徑，由元素加屬性定義，如 `CYLI` 的 `DIAM`）、`PDIM`（節圓）、`ADIM`（角度）。尺寸由游標快速建立，許多屬性由所屬 `LAYE` 串接，且掛在設計元素上，所以設計改變後 `UPDATE` 會重算。注意這與 Marine Drafting 的關聯尺寸是不同機制，不要混用經驗。

> 〔公開版未收錄：AVEVA 官方產品截圖〕線性尺寸的組成：Dimension Line、Dimension Text、Projection Lines、Dimension Point

*圖 29-14　線性尺寸的組成：尺寸線、尺寸文字、延伸線與尺寸點。（AVEVA 官方文件截圖，僅供內部教學）*

### 29.7.3 標籤、Autotagging 與遮蔽

標籤有 **General Label（`GLAB`）** 與 **Special Label（`SLAB`）**，後者的外觀與文字由標籤樣板（文字樣板 `TXTM`、符號樣板 `SYTM`，放在 `LALB`）決定。最小例子：

```
NEW GLAB
DDNM ID @
```

預設文字 `#NAME` 是附著點處元素的名稱（無名稱則顯示錯誤文字，由 `LAYE` 的 `NTEXT` 自訂）。附著點可用 `NPPT`、`PKEY`（如 `TOS`、`MEML`）、`PKDI` 變化，或 `ON IDP @` 一次設定；標籤原點預設距附著點 x25 mm、y25 mm，`AT` 的座標永遠被當絕對座標；`BTEX 'NOZZLE 2#/#NAME'` 混用明文與智慧文字（`#/` 換行）。

**Autotagging（自動標籤）** 由規則批次產生標籤：`NEW TRLB`、`NEW TRST`、`NEW TAGR /TR1` → `TMRF /LAB1`（外觀，指向 `GLAB`、`SLAB`、`SYTM` 或 `TXTM`）→ `IDLN`（範圍，預設視圖自己的 Id List）→ `TAG ALL NOZZ`（條件，語法同 `USE … FOR`）→ `UPDATE TAGGING`。每個標籤的 `SORF` 指回 `TAGR`。再次更新（不加 `OVERWRITE`）時，既有標籤更新位置、新元素補標、已刪除或不符條件者被刪；加 `OVERWRITE` 則重建，**手動編輯過的標籤會被丟掉**。不在 Id List、落在視圖框外或被剖面排除的元素不產生標籤，但被別的元素擋住的仍會產生（可設 `LVIS FALSE`）。Datal 輸出無法重現 `TAGR` 與標籤的連結，資料庫間轉移要用 `RECONFIGURER`。搭配 Tab 碼（`#NAME#15#P1BOR#25#CREF`）、等寬字型與 PML 可在圖面上產生明細表。

**標籤擺放與遮蔽：** `SPREAD LOCAL` 把標籤擺在重要元素周圍，避免重疊與引線交叉；`SPREAD REMOTE` 排到視圖邊框外圍（可設 `MARGIN`、`GAP`、`OMIT TOP`），所有選項要寫同一行，不會記住前次參數。`AUTOBLANKING ON/OFF` 讓尺寸、標籤與註記底下的 3D 圖形留空（`BLNK`、`BMAR`）；關閉時螢幕不遮蔽但 **plotfile 一律產生**。

### 29.7.4 報告、傳閱清單、修訂與 Change Highlighting

`REPO`（報告）、`CLLB`／`CIRL`／`RECI`（傳閱清單庫、清單、收件人，圖面以 `CLRF` 參照）與 `REVI`（修訂，可屬於 `DRWG` 或 `SHEE`：`RVSN`、`RVDT`、`RVAU` 建立時自動設定，另有 `APPR`、`APDT`、`STEXT`）。偽屬性 `SREVAY`、`DREVAY` 回傳所有 `REVI`（最多 50），可搭配智慧文字 `#RVSN` 等產生修訂表。

**Change Highlighting（變更標示）** 比較「現在」與「比較日期」兩個時間點，把改過的設計與註記畫成不同樣式：

1. 建 `CRST`，內含 `DCRULE`（設計）與 `ACRULE`（註記），分別參照 `DCSTYL`、`ACSTYL`；**沒有本地變更規則**。
2. `DCRULE` 的 `CRIT` 用 `CREATED()`、`MODIFIED()`，如 `CRIT ALL BRAN MEM WITH (MODIFIED (GEOM))`；已刪除元素不畫在圖上，所以 `DELETED()` 無意義。
3. 樣式：`DCSTYL` 預設為粗線、顏色 8；`ACSTYL` 可改字型、加括號或底線；`UNChanged` 表示沿用原樣式。
4. 視圖 `CRSF` 指向規則集（未設則用預設規則）。
5. `SETCOMPDATE 31 March 2002` 或 `SETCOMPDATE STAMP /Prelim-Milestone`（Stamp 由 Marine Administrator 建立）。
6. `UPDATE DESIGN／ANNOTATION／ALL … SHOW CHANGES`，只在 `VIEW` 以上有效。

註記只比對**展開後的文字字串**：`#NAME` 的標籤因元素移動而移位不算變更，`#NAME at #POS` 則算。常見錯誤：`64,446`（沒有 Comparison Date 或 Stamp）、`64,445`（規則集內無規則）。在 Marine Drafting 中，船體項目**只能在 Global 或 Universal Hidden Line 視圖中標示**，且**只檢查標籤（`GLABEL`）**。

## 29.8 Marine Drafting Application Menus：選單地圖與功能對照

選單列為 `File`、`Edit`、`View`、`Insert`、`Format`、`Zap`、`Tools`、`Dimension`、`Annotate`、`Modify`、`Project`、`AutoDP`、`Window`、`Help`（見圖 29-1）。

| 選單 | 主要功能 | 重點與提醒 |
|---|---|---|
| `File` | `Save and Unclaim`、`Save Work`、`Get Work`、`Extract Control`；`New／Open／Close／Save／Save As Drawing`；`Print Preview`、`Print`；`Drawing Reference`（Define／Collapse／Expand／Exchange／Dissolve／Show）；`Transfer`；`Import`／`Export`（DXF、DWG、IGES、SDB 等）；`Data Bank`（List／Delete／Copy Drawings）；`Properties`；`Modules`；`Exit` | `Save Work` 存模型、`Save Drawing` 存圖；`Save As` 可改圖面類型與 `REGI`；`Transfer` 把選取資訊複製到另一張圖（不存在則建立）；`Properties` 要求圖面含表單；`Modules` 可切到 Monitor、Hull Design、Outfitting Draft、Spooler、Isodraft 等 |
| `Edit` | `Delete` 的各類實體（Geometry、Dimension、Note、Label、Hatch Pattern、Cloud、Symbol、Text、By Layer、By Area、Last Entity…） | `Last Entity` 可撤銷剛建立的實體 |
| `View` | `Repaint`、`Zoom`、`Pan`、`Layer`、`Grid`、`Envelope`、`2D Restrictions`、`New／Shaded Viewport`、`Shading`、`Explorers`（Design／Manufacturing／Draft／Drawing）、`Addins`、`Command Window`、`Link Documents` | `Layer` 有 hide／show 兩種模式；`Shaded Viewport` 對模型視圖開著色視窗；Command Window **不建議使用** |
| `Insert` | `Model`、`Point／Line／Arc／Polyline／Spline／Conic／Rectangle…`、`Hatch Pattern`、`Construction Lines`、`Text`、`Symbol`、`Subpicture`、`Standard Detail`、`Plate Part`、`Drawing Form` | `Construction Lines` 模式下幾何成為白色、短虛線、圖層 `-4`；`Plate Part` 從 `SB_PLDB` 取入零件作子圖 |
| `Format` | `Colour`、`Line Type`、`Layer`、`Hatch Pattern`、`Defaults`、`Local Origin`、`Geometry Mode`（2D／3D 點、線、弧、Conic、Polyline 的定義方式） | 格式變更**不回溯**；未指定圖層時為圖層 0 |
| `Zap` | `Operation Complete`、`Quit`、`Cancel`、`Options`、`All`、`Subpicture Level` | 互動流程控制 |
| `Tools` | `Model`、`Model View`、`Backdrop`、`Subpicture`、`Vitesse`、`Inquiry`、`Drawing Form`、`Symbol`、`Inspect Drawing`、`Clean Workspace`、`Claim Lists`、`DB Listing`、`Settings`、`Preferences` | 見下 |
| `Dimension` | `Linear`、`Radius`、`Diameter`、`Angle`、`Curved`、`Area`、`Distance`、`3D`（Linear、Coordinate、Weight and COG、Shell Profile Mounting Angle、Distance to RSO／Plane…） | 見 29.3.3 |
| `Annotate` | `General Note`、`Position Number`、`Config Note`、`Hull Note`、`Label`、`Autotagging`、`Markup`、`Ruler`、`Position Ruler`、`Coordinate Axis`、`Cloud` 等 | `Position Ruler` 可建 Base Line、Center Line、Frame Ruler、Longitudinal Ruler；Markup 在圖層 `-9`、Label 在 `-11` |
| `Modify` | `Move`、`Copy`、`Transform`、`Trim`（To Entity／By Length／Gap／Cutout／Fillet）、`Stretch`、`Chain`、`Properties`、`Dimension`、`Label Placement`、`Colour`、`Line Type`、`Fill Style`、`Layer`、`General` | `General`：把符合「搜尋屬性」的所有幾何改為「新屬性」（例：所有紅色設為不可見）；`Label Placement` 是 `SPREAD` 的 GUI（圖 29-15） |
| `Project`／`AutoDP` | `Change View Mode`（design／production view mode）；`Assembly Deliverables`、`HVAC Sketches`、`Pipe Sketches` | 單視圖專案無法切換；AutoDP 開自動出圖表單，見第 28 章 |
| `Window`／`Help` | 視窗排列、`Main Viewport`；`Contents`、`Index`、`About` | 視窗管理與說明 |

**`Tools > Model View`** 是改版更新的核心：`Update Design／Annotations／All` 更新所選視圖；`AutoScale` 貼合表單預設的視圖大小；`Change Projection`；`2D Restriction` 設視圖框與裁切；`Slice` 以兩個切面呈現切片；`Split`、`Clear`；`Explode` 爆炸拆開 Panel、Longitudinal、Transversal；`Hull Symmetry` 切換 P／S／雙側；`Validate` 找出「過期」模型，但只比**時間戳**，重畫結果相同也可能被判過期。`Tools > Model` 另有 `Present`（剖切僅限船體）、`Cross Section`（需兩個正交視圖）、`Panel Intersect`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Intelligent Label Placement 對話框：Remote／Local 模式與選取標籤的按鈕

*圖 29-15　Intelligent Label Placement 對話框（`Modify > Label Placement`）：Remote／Local 模式，以及 Identify labels、Select region 等選取方式。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 文件指出，在 Marine Drafting 使用 `Autotagging` 時，**所有要標籤的模型都必須落在視圖範圍內**；但 Marine Drafting 的視圖範圍不明顯，除非用 `Tools > Model View > 2D Restriction` 明確設定，因此建議先設 2D Restriction。

## 29.9 常見錯誤與文件陷阱

- 模型改了、圖面沒存：`Save Work` 不存圖面，要另做 `Save Drawing`。
- 從 Command Window 改圖後無法更新模型：圖面未持久化。
- 設了 `Advanced filter` 卻刪錯：操作作用在過濾後的清單。
- `SY010` 修復後原圖被覆蓋：未指定 `-targetdb`，先用 `-report`。
- Id List 的 `REMOVE` 無效：順序錯。
- Autotagging 重跑後手動編輯消失：用了 `OVERWRITE`。

## 29.10 練習（只在訓練專案）

1. **圖面落點：** 新建一張 General Drawing 與一張自訂類型（`1001,ClassDwg`）的圖，到 Draft Explorer 找出各自的 `DEPT／REGI`，說明由 `PADDXP` 或哪個環境變數決定。
2. **Save Work 與 Save Drawing：** 放入一個 Panel，只做 `Save Work`，關閉重開觀察；再做 `Save Drawing`，寫下兩者各存了什麼。
3. **Id List 與 AUTOSCALE：** 依 29.5.2 建立 `DRWG→SHEE→VIEW`，Id List 加一個 `ZONE`、移除一條分支，`AUTOSCALE`、`UPDATE DESIGN`、`SAVEWORK`，再比較 `VTYP GLOBAL` 與 `UNIV`。
4. **規則順序與剖面：** 建兩條 `RRUL`（小口徑不畫、其餘用 `/S2`）再對調順序；建 `SPLA` 與 `VSEC`，用 `PMOD REVERSE` 切換保留側。
5. **自動標籤與改版：** 建 `TAGR`（`TAG ALL NOZZ`）並 `UPDATE TAGGING`，移動設備後分別以不加與加 `OVERWRITE` 更新；設 `SETCOMPDATE` 後用 `UPDATE ALL SHOW CHANGES`。

## 29.11 本章小結

- Marine Drafting 是互動式 2D 繪圖加模型介面，圖面雙重儲存（PADD＋`.SDB`）；`Save Work` 存模型、`Save Drawing` 存圖；存入後即歸 Marine Drafting。
- 圖面由三層子圖與圖層組織，類型決定 `DEPT／REGI`；尺寸七類，船體另有 Hull Note 與 Mould Line；可程式化切入點只有文件列出的 hook、批次公用程式與 Vitesse。
- Design Draft 的 `VIEW` 不存幾何：Id List 決定內容、`VTYP` 決定隱藏線等級、規則與 `VSEC` 決定外觀，`UPDATE DESIGN` 產生圖形、`SAVEWORK` 存 Picture File。
- 規則順序決定結果；Autotagging 的 `OVERWRITE` 會丟掉手動編輯；Change Highlighting 靠 Comparison Date 與 `CREATED()`／`MODIFIED()`。

## 29.12 自我檢核

- [ ] 說出圖面的兩個儲存位置，以及 `Save Work` 與 `Save Drawing` 的差別。
- [ ] 說明圖面類型如何決定 `DEPT／REGI`，並設定自訂類型。
- [ ] 說出尺寸七類與 Hull Note 五種，以及三層子圖與圖層正負號。
- [ ] 寫出 `DRWG→SHEE→VIEW` 與 `AUTOSCALE`、`UPDATE DESIGN`、`SAVEWORK` 的指令序列。
- [ ] 解釋 Id List 順序、`VTYP` 六等級、規則「先符合者生效」與三種剖面元素。
- [ ] 說明 Autotagging 兩次更新的差別與 Change Highlighting 的步驟，並指出可擴充的切入點。

## 29.13 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 29 章](appx_d_verification_zh-TW.reading.html#ch29)；取材覆蓋與未讀範圍：見[附錄 E 第 29 章](appx_e_coverage_zh-TW.reading.html#ch29)。
