# 第 33 章　船體詳細設計（一）：設定與標準、初始化工具、平面板架建模

> 第 5 章講「船體資料長什麼樣子」，第 6 章講「怎麼把模型變成生產資料」，第 15 章講「Vitesse 怎麼讀船體資料」。這一章把視角拉到**詳細設計的第一個動作**：在建任何一塊板之前，**一個船廠的標準（part name、bevel、型材、endcut、開孔、肘板……）要先被「編譯」進資料庫**，然後才輪到設計師用 Planar Modelling 一塊一塊建板架。
>
> Hull Detailed Design 整章約 2,451 頁，本課程分三章處理。**本章**：Setup, Customization and Standards（標準與客製化）、Initialization Utility Program（`inithull`）、Planar Modelling（平面板架建模）。曲面建模、選用功能與雜項工具見第 34 章；生產製造、舾裝鋼構與 F1 說明文字見第 35 章。
>
> **資料可信度：** 檔案格式、陳述式語法、環境變數、物件名稱與預設值取自 AVEVA Marine 12.1 官方離線文件（Hull Detailed Design 下的三個子樹，實際讀取頁數見 33.11）。官方文件極少給 PML／Vitesse 程式碼，僅 Part name、Configurable Note 與 Scheme 版面三個 Vitesse hook 附有介面或範例；其餘「二次開發怎麼接」一律標〔待核對〕，待在訓練專案實測。官方機器翻譯譯名生硬，本章造船術語改用台灣慣用說法。文件原屬 TBH 時代手冊，部分頁面仍用 SB_OGDB、SJ001 等舊名稱，本章照原樣保留。

## 33.1 學習目標

讀完本章，你應該能夠：

1. 說明 Hull Detailed Design 三章的分工，以及本章三個子樹彼此的先後關係。
2. 說明標準的運作模式：文字控制檔 → `inithull` 編譯 → 資料庫物件 → 環境變數啟用。
3. 列出主要標準（part name、bevel、型材、endcut、flange、hole／notch、cutout／clip、bracket、shrinkage 等）各自對應的環境變數與控制物件。
4. 操作 `inithull`，區分 create function 與 check function，並建立 Hull Reference 與 Block。
5. 說明 panel、input scheme、statement 三層關係，以及互動模式、背景模式、separate／in view 兩種產生方式。
6. 讀懂並修改 Scheme：`PANEL`、`BOUNDARY`、`SEAM`、`PLATE`、`STIFFENER`、`FLANGE`、`HOLE`、`NOTCH`、`CUTOUT`、`BRACKET`、`DOUBLING` 等陳述式。
7. 使用 Plane Panel Editor 與 Planar 選單（Model、Panel、Scheme、View、PosNo、RSO、Select）。
8. 用 Create View 衍生符號視圖，並理解 Recreate 與模型同步的關係。
9. 設定預設檔（default file）的重要參數，並指出可供二次開發的 hook 與須實測的項目。

## 33.2 Hull Detailed Design 全貌

### 33.2.1 三章分工與本章定位

| 章節 | 官方子樹 | 內容 |
|---|---|---|
| **第 33 章（本章）** | Setup, Customization and Standards／Initialization Utility Program／Planar Modelling | 標準編譯、`inithull`、平面板架 |
| 第 34 章 | Hull Curved Modelling／Optional Hull Functions／Miscellaneous Utilities | 曲面（外板）、選用功能、雜項 |
| 第 35 章 | Manufacturing／Production Features for Outfit Steel／F1 Help Texts | 零件抽出以後的生產、舾裝鋼構、說明文字 |

與既有章節的分工：[第 5 章](ch05_hull_modelling_zh-TW.reading.html)已講板架解剖（邊界、接縫、板、加強材、拓撲參考）與 Scheme 概念，[第 6 章](ch06_hull_production_zh-TW.reading.html)已講零件抽出與收縮補償概念，[第 15 章](ch15_hull_vitesse_zh-TW.reading.html)已講 Vitesse 三種掛載方式。本章**不重講概念**，只補它們沒講的：標準檔案怎麼寫、`inithull` 怎麼跑、陳述式的關鍵字與限制、預設檔參數。

### 33.2.2 先後順序

```
Hull form(曲面) ─► inithull：Hullref / Structref / Blocks / gentab
                ─► inithull：各項標準編譯（bevel、endcut、bracket、cutout…）
                ─► 設環境變數指向控制檔／物件
                ─► Planar Modelling 建板架 ─► 零件抽出(第6、35章)
```

> **專業提醒：** 順序反了是最常見的新專案問題：標準沒編譯就建板，結果是 endcut 畫不出來、bevel 代碼不被接受、part name 報錯。官方明說：沒有 endcut table，側視圖中加強材的 endcut 不會正確繪出。

## 33.3 Setup, Customization and Standards

### 33.3.1 運作模式：控制檔、編譯、物件、環境變數

幾乎所有標準都走同一條路：

1. 用文字編輯器寫控制檔（多數是 **TIL**，The Interpretive Language；副檔名常為 `.dat`）。
2. 在 `inithull` 以 **create function** 編譯；成功就把物件存進結構資料庫（`SB_OGDB`），並產生 `.lst` 回條清單（經 Job Launcher 啟動時由 Job Launcher 保存；否則放在專案的 print 目錄）。
3. 部分標準另需**環境變數**指向控制檔（官方稱 check function 的檔案不編譯成物件，而是由應用程式直接載入）。
4. 物件存在、或環境變數有設，功能才啟動；例如進階 bevel 處理「以該物件存在」啟動。

| 標準 | 控制檔／環境變數 | 資料庫物件（固定名稱） |
|---|---|---|
| Part name | `TB_PARTNAME_CTRL`（檔名不含副檔名）、`TB_PARTNAME_LEVEL` | `__TB_PARTNAME_CTRL__` |
| Functional Description | `.dat`（`DESCR`／`INTERVAL`） | `__FUNCTIONAL_PROPERTY__` |
| Bevel | `SBH_BEVEL_CTRL`、`SBH_BEVEL_SETS` | `__SBH_BEVEL_CTRL__` |
| 焊接 Execution Unit | `SB_WELDDB`（資料庫）、`SB_EU_ORDER` | EU 物件 |
| I／U 型材 | `SBH_I_U_BARS` | （檔案直接載入） |
| 啟用型材 | `SBH_PROF_CTRL` | （檔案） |
| Connection code | `SBH_CONCODES` | （檔案） |
| Endcut table／預設 endcut | `SB_ECUT`／`SBH_ENDCUT_CTRL` | endcut table（SB_OGDB） |
| 外部 cutout | `SBH_CUTSTDOBJ` | `__CUTSTDOBJ__` |
| Cutout／clip macro | `SBH_CUTOUT_MACRO`、clip macro 對應檔 | （檔案；macro 在 `SBB_GEO_MACRO_BIN`） |
| 自動 cutout | `SBH_CUTOUT_CTRL` | （檔案） |
| Bracket | — | `__SBH_BRACKET_CTRL__`（範例檔 `sbh_bracket_ctrl.dat`） |
| 材質／去向／表面處理 | 材質 Paragon 腳本；`SBH_DESTINATION_CTRL`；`SBH_TREATMENT_CTRL` | 材質存於 Property World |

> **專業提醒：** 這張表是「新專案設定檢核表」。把它的環境變數與檔案放進專案的版本控制，並記錄每次編譯的 `.lst`，是最便宜的稽核手段。

### 33.3.2 Part name（零件名稱）控制
part name 是生產用名稱，**不等於**資料庫內部零件名；相同零件可共用 part name。長度上限 48 字元，**建議 24 以內**（部分應用不接受長名稱）。控制檔（TIL）有四種陳述式：`LEVEL`（命名層級如 `FULL`／`SHORT`，最多 10 個，須在規則之前）、`SYMMETRY`（`/PS`、`/SB`、`/CL` 標記，預設 `P`／`S`／`SP`）、`BUILT_PROFILE`（組合型材 `/TOTAL`、`/WEB`、`/FLANGE`）與命名規則：`<part_type> /LEVEL=… <constituent>｜<delimiter>…`。

零件類型：`HGEN`（一般，可帶 FD 代碼，**優先順序最高**）、`HPPL`、`HSPL`、`HBPL`、`HCPL`、`HPPR`、`HSPR`、`HBPR`、`HDOU`。組成項如 `/PROJ`、`/ASS=n`、`/BLOCK`、`/SBLOCK`（去船字母）、`/POS`、`/BPOS`、`/LPOS`、`/SYM`、`/BUILT`、`/GPS1…4`；分隔符 `/DEL`、`/ZDEL`（後項為空時略過）。官方範例（區塊 `AA123`、position number 皆 1）：

```
HPPL /LEVEL='FULL'  /SBLOCK /DEL='-' /POS;      ! 123-1
HBPL /LEVEL='FULL'  /SBLOCK /DEL='-B' /POS;     ! 123-B1
HPPR,'31' /LEVEL='FULL' /BLOCK /DEL='-L-' /POS; ! AA123-L-1
```

**沒有預設規則**，所有會用到的零件類型都要寫。`TB_PARTNAME_LEVEL` 檔可為特定模組指定層級（每行「模組 層級」）。**Vitesse 後處理**：套用規則之後，若 `PYTHONPATH` 內有 `_TBhook_CustPartName.py`，系統呼叫其 `getPartName(Project, Assembly, Block, Module, System, Drawing, Location, PositionName, PositionNo, BracketPositionNo, SymmetryCode, BuiltProfile, GPS1…GPS4, MarinePartName, StoringCode, RulePartName)`，回傳 `CustPartName`；**簽名不可更動**。

### 33.3.3 Functional Description 與 Configurable Note
- **Functional Description（FD）**：附在板架與零件上的描述標籤，≤ 75 字元，索引 0–32767（0 為預設）。`DESCR, <index> /VALUE='…';` 定義，`INTERVAL /<part_type> /MIN= /MAX=;` 限制 GUI 顯示區間；值內可用 `!X`／`!Y`／`!Z`（轉為 FR／LP，如 "Bottom web at FR85"）。檔案是**增量合併**：刪除 FD 要把字串設為空並保留索引；改索引會新增一筆而舊的仍在。FD 亦用於自動焊腳。
- **Configurable Note**：純 Vitesse hook，檔名 `_TBhook_ConfigNote.py`，置於 `PYTHONPATH`。必備方法（簽名不可變）：`getNoteName`、`getNoteChar`（回 `(reference, placement, colour, layer, flip_angle)`）、`getNoteFilter`、`getNoteData`、`setNoteData(NoteNo, ModelType, Model, PartType, Part, SubPartType, SubPart)`。紀錄順序限制：第一筆必為 reference symbol 且只能一筆。

### 33.3.4 Bevel、Excess 與焊接
**Bevel**（開槽）分**對接**（butt，剖面沿焊道恆定）與**角接**（fillet，可為固定角或隨連接角連續變化）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Bevel 剖面名詞：正側、負側、倒角、開口角、鈍邊、E 值

*圖 33-1　Bevel 基本名詞：positive／negative side、chamfer、opening angle、nose、E-measure。（AVEVA 官方文件截圖，僅供內部教學）*

AVEVA 內建「基本 bevel type」（對接如 10、20、30、40、50 等；固定角接如 15、25、35；變角如 16、26、36），**客戶定義 bevel code（1–999）作為其實例。系統沒有預設 bevel 標準，必須自建。**

| 概念 | 說明 |
|---|---|
| Variant | 0＝基本型；1／2＝厚薄不同且倒角；3／4＝厚板不倒角；9＝共中心面雙側倒角 |
| 編譯與啟用 | 定義檔編譯為 `__SBH_BEVEL_CTRL__`，`SBH_BEVEL_CTRL` 指向檔案；物件存在即啟動進階處理 |
| 自動選擇 | `SBH_BEVEL_SETS`（`CUTOUT_SET`、`BRACKET_SET`、`PROF_END_SET`、`PROF_TRACE_SET` 等）；建模給 `-1` 取消、給代碼則覆蓋 |
| 常用語法 | `CHAMFER`（預設 18 度）、`VARIANT /TOL= /LIM= /OPEN= /SQUARE=`（預設 0.5／10／3,5 mm）、`BEVEL, <code> /TYPE= /GAP= /ALPHA= /SYMBOL=…;`，變角用 `/VAR_ALPHA` 並搭配 `AUTO_SELECT` 等 |

建模寫法：`[-]<code>[<variant><E 值兩位>]`，如 `BEV=201107`；或名稱加 `BVA`、`BEM`。接縫上通常只給代碼，variant 與 E 值由系統算；**使用者明給的值優先**。

**Excess 與 Compensation** 須設計師明確給定（bevel gap、shrinkage 則由系統自動處理）。excess 符號放符號字型 92。

**自動焊腳（Execution Unit，EU）**：偵測到角焊且建模沒給焊腳（WLL）時，先算 weld factor，再依板厚轉 WLL。規則存於 `SB_WELDDB`；EU 類型 `/COMP`、`/COMP_TYPE`（官方註明尚未完全支援，勿用於生產）、`/RSO`、`/GEO`、`/PAN`；預設搜尋順序 `P_RSO_C_CT_G`，可用 `SB_EU_ORDER` 改。`RULE /ABUTTED= /ABUTTING= /WELD_FACTOR=` 以 FD 代碼配對；`DEFAULT` 給缺省值。

### 33.3.5 型材、Connection code 與 Endcut
AVEVA 型材以**系統固定整數型別**挑選（不支援 56、64、65）：10 扁鋼、20／21／23 球扁鋼、30／31 角鋼、35–38 組合角鋼、40 T 型、50–59 U／I 型、100–110 swage。**限制**：flange（面板）只能是 10；殼縱骨與加強材可為 10–55；柱通常 50–74。

> 〔公開版未收錄：AVEVA 官方產品截圖〕型材型別、斷面圖與參數代號對照表

*圖 33-2　型材型別代碼、斷面與參數（a、b、s、t、c、u）對照。（AVEVA 官方文件截圖，僅供內部教學）*

| 項目 | 控制檔 | 重點 |
|---|---|---|
| U／I 型尺寸表 | `SBH_I_U_BARS` | `TYPE=50…`；每行 `H,B,Tw,Tf,R1[,R2]`；分號結尾、無空行、行寬 ≤ 80；建模取最近值 |
| 專案啟用型材 | `SBH_PROF_CTRL` | `TYPE = 10 'Flat bar'` 後接尺寸列；行寬 ≤ 132；字串出現在互動選單 |
| Connection code | `SBH_CONCODES` | 四數：`<code 1–9999> <type> <dist> <offset>`，最多 100；`dist`>0 間隙、=0 相接、<0 重疊；與內建碼同號即覆蓋 |
| Endcut table | `SB_ECUT` | 記錄 `600`（表名）、`601`（選擇列／參數列）、`602`（自訂名）；**選擇列由 AVEVA 設，客戶勿改**，只增參數列 |
| 預設 endcut | `SBH_ENDCUT_CTRL` | `TYPE=`、`PROF=`、`1102 CON=5,10,12`：遇到該連接碼時預設用此 endcut（最多 20 個 CON） |

endcut 概念：**type**（10–326，AVEVA 固定）＋**code**（type 加兩位數，每型最多 100 個，客戶可調半徑與固定角）＋**explicit parameters**（最多 6 個：長度 a、b、c 與角度 a1–a3）。建模 `CUT = 1112, 80` 表示 code 1112、第一個明確參數 80；角度未給時有連接則自動算，否則 90 度。自訂 endcut 在 PARAGON 以 `SFIT`＋`DTSE`＋`NGMS` 定義，名稱須列於 endcut table 的 602 記錄。Structural Design 的 `SNIPE`／`TIGHT`／`OVERLAP` 標準連接存於 `__SBED_STIFF_ENDS__`；亦可自訂 `CON_NAME, MY_TIGHT /PROFILE='10' /CON=87 /CUT='1210,70,35';`，建模寫 `CON=MY_TIGHT`。

### 33.3.6 Flange、Hole 與 Notch

**折邊（Folded flange）**：控制檔只有兩個陳述式。`FLA_TYPE` 定義寬度與標記線位置：`FLA_W = W_H_FACT*H + W_RAD_FACT*R + W_T_FACT*T + W_CONST`（`MARK_D` 同理）；`FLA_END` 以基本端型（1、2、3、4、5、9）加參數（`/KN_*_FACT`、`/FLA_V` 預設 30 度、`/R1`、`/R2`、`/TOE_H`、`/TOE_L`、`/R_FILLET` 軟化尖角）。至少要各有一個 type 與 end；`/DEFAULT` 指定預設，否則取檔內第一個；`FLA_TYPE` 編號**不可介於 200–300**。

**Hole**：封閉輪廓；分 physical（3D 也開孔）與 fictitious（只標記，3D 預設不顯示，須設 `SBH_INPM_FICT_HOLE`）。標準孔以「型別 ＋ 參數用星號連接」指定，如 `D250`（直徑 250）、`HE250*125`（橢圓）；新標準孔須由 AVEVA 實作，客戶改走 `_TbhookCustHole`（輪廓用 2D 本地座標，原點是定位參考點，建議順時針）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕標準孔型選單：D、HO、HOR、HE、HSE、HER、HR、HRM、HT

*圖 33-3　AVEVA 標準孔型選單。（AVEVA 官方文件截圖，僅供內部教學）*

**Notch**：標準缺口分三類（角／邊兩用：R、RW、KEH、KUH；角專用：KS、VU 等；邊專用：KD、KE、KO、KR 等），例 `R50`（半徑 50 圓弧）、`HE250*125*100`；省略中間的選填參數要用 0 占位（`NOT*<a>*<b>*0*<d>`）。部分缺口有尖角趾，可用 `SBH_NOTCH_TOER`、`SBH_NOTCH_TOEH` 軟化。任意缺口必須「開放輪廓且與零件輪廓恰有兩個交點」。視圖符號以 `SBH_PENETR_SYMB_CTRL` 檔對應：每行 `NOT|HOL, <designation>, <symbol no>;`（符號字型 94），designation 可只寫前綴當萬用字元，空 designation 是預設符號。

### 33.3.7 Cutout 與 Clip

穿過板的加強材開口稱 **cutout**，補強用小板稱 **clip（collar）**。cutout 有三種來源，**同一 cutout 號碼可混用，優先序為 macro 最高**：

1. 內建 cutout（寫死，不可改參數）。
2. 外部定義（External Cutout Definition）：`CUT, <number> /TYPE=<main type> /PROF=(…) /ARC=… /RAD=… /H_LIM=… /GAP=…;`，編譯為 `__CUTSTDOBJ__`；半徑 `R<0` 為 KS 缺口、`R=0` 為折角、`R>0` 為圓弧；可依型材高度分段給半徑（例 `/RAD=(-10,40,60) /H_LIM=(100,250)`）。
3. 幾何 macro：macro 名稱須同檔名，對應檔由 `SBH_CUTOUT_MACRO` 指定，每行 `<cutout> '<macro>' <no_prof> <ptype…>`；效能略慢於外部定義。

另有**具名 cutout**（`CUTOUT, <name> /CUT_NO= /CLIP_1= /CLIP_2= /CLIP_3=;`，可同時綁定 clip 組合）、**自動設定 cutout**（`SBH_CUTOUT_CTRL`：`TYPE = <型材>` 下列 `<panel data type 遮罩> <cutout> <clip>`，遮罩可含 `%`，**較特定的遮罩要放前面**）與**交叉 cutout 9999**（雙板互嵌如蛋箱，兩片板都要各設一次，見 33.5.8）。clip 可用內建簡單 clip（三位碼 XYZ 分別表示肋骨側、非肋骨側、頂部，0 表示無）或 macro；clip 零件名為 `<panel>/C<clip_no>[S|P]`。

### 33.3.8 Bracket（肘板）標準

肘板必須是**單一板件、不可有孔、必屬某個 panel**。分兩類：**type standard bracket**（以名稱登記，兩臂或三臂，臂端有 toe）與 **panel bracket**（以小板架建出，用於非標準肘板，或走 `_TBhookCustBracket`）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕肘板連接類型示意：Panel/Profile、Panel/Panel、Profile/Profile

*圖 33-4　肘板典型連接情形。（AVEVA 官方文件截圖，僅供內部教學）*

定義檔（編譯為 `__SBH_BRACKET_CTRL__`）有階層：低階 `PROFILE`、`CONNECTION`、`TOE`、`NOTCH`、`CUTOUT`、`PATTERN`；中階 `STIFFENER`、`FLANGE`、`FACE_PLATE`；最高階 `BRACKET`；**被引用的須先定義**。`TOE` 以基本 toe 型別（1–4、8、9、11–15、31–37、101、102、131–136 等）加參數（`TOE_H`、`H_TOT`、`O_LAP`＋`O_LAP_LIM`、`R_ANG`、`TOE_L`＋`TOE_L_LIM`、`RAD`…）；`CONNECTION` 共 0–7 型。範例檔 `sbh_bracket_ctrl.dat`；建議刪除用不到的肘板以縮短選單。

**Bracket instance**：另一個檔，`BRACKET, 'B';` 後接多個 `INSTANCE, 'B10' /A=200 /B=200 /MAT=8 /NOTCH='KS10';`，instance 名稱須以 bracket 型別開頭；建模時 `BRA, B350, SYN=2` 等同 `BRA, B, MAT=9, A=350, B=350, SYN=2`。**bracket 指定值被使用者改過就以使用者為準**。

### 33.3.9 Tap、Knuckle、Swage 與 Shrinkage

| 項目 | 要點 |
|---|---|
| Tap（焊接延伸片） | `TAP, <type> /A= /B= [/R=];`，每型只保留最後一筆；每次編譯**取代**既有 `__SBH_TAP_CTRL__` |
| Knuckled panel | 子板架合成主板架；knuckle 線上的孔、缺口、cutout、加強材**不支援**；彎曲參數在 `SBH_KNUCKLE_CTRL`（`TYPE`、`RADIUS`、`THICKNESS` 群組，板厚須遞增；預設彎曲型 9999） |
| Swage（小波紋） | 型材型別 100–110；`SWEDGE`、`PROFILE`、`SIZE` 三種陳述式；零件抽出時自動補伸長量 |
| Shrinkage | **局部法**與**統計法**；`SBH_LOCAL_SHRINKAGE`＝`EDGES_AND_FILLETS`／`EDGES`／`EDGES_BUTTS`；使用者手動給 `M5`、`M6` 就整個切到統計法 |
| 組合型材焊接補償 | 以 5 點重建腹板中心線（端點移 M1、四分點移 `CONSTANT*M1`，預設 0.25）；腹板曲率須 < 3 度 |

### 33.3.10 其他設定
- **GSD**（組裝標記三角）：`SBH_GSD` 預設檔每行「關鍵字＝值」（如 `SHAPE`、`SIZE`、`TRACE_LIM`、`REDUCE_DIR_X／Y／Z`）；標記面由 `SBH_MARKING_SIDE`（`MOULDED` 預設）決定，單一板架可用 `PANEL` 的 `GMS=` 覆蓋。
- **型材轉板**：`SBH_PROF_TO_PLDB` 決策表，**不可有空行**；轉成的板 data type 為 87。受限制檔、彎曲餘量等屬製造範疇，見第 35 章。
- **材質、去向、表面處理**必須先登記，建模時給未登記值會報錯；材質代碼不可在專案中途更動，代碼 0 為預設材質。
- **FRP**：`SBH_GRP=MIXED` 時每個 block 須指定鋼或 FRP；FRP 專案中密度大於 0.000001 kg/mm³ 的材質視為鋼，不出現在選單。
- **對話框客製**：選單由「設定圖」產生（`__SBH_BKT_MENU__`、`__SBH_CUTOUT_TYPES__`、`__SBH_ECUT_MENU__`）；改了 bracket 名稱要同步改設定圖。

## 33.4 Initialization Utility Program（`inithull`）

### 33.4.1 用途與執行

`inithull` 在**新專案初期**使用：設定預設值、初始化資料庫、編譯各項標準。**環境（目錄、資料庫、專案檔）須先備妥**。通常由系統或專案經理執行，一般使用者不應執行。啟動方式：Hull Log Viewer 內選 **Hull > Hull Init**。功能以樹狀選單分組。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Initiate Hull Standards 視窗

*圖 33-5　Initiate Hull Standards 視窗：左側為功能樹，右側為 create function 的共通表單（物件名稱、輸入檔、Edit TIL File、Create Object）。（AVEVA 官方文件截圖，僅供內部教學）*

### 33.4.2 三類功能

| 類別 | 說明 | 表單重點 |
|---|---|---|
| 精靈型 | 以 wizard 互動建物件，部分可選擇以檔案建立 | 如 Hullref、Structref |
| **Create（編譯）** | 輸入檔經編譯，成功即把標準物件存入 `SB_OGDB`，並輸出 compiler list | `Source Input File`（預設從 `SB_SHIP` 的 def 目錄取）、`Edit TIL File`（開 Notepad，**須關閉才能繼續**；改檔要用 Notepad 的 File 存檔）、`Create Object`；`Generate TIL` 多半未實作 |
| **Check** | 檔案不產生物件，而是由應用載入；功能只做診斷 | `Environment variable` 欄顯示變數與值、`Edit`、`Check` |

> **專業提醒：** 官方註明第 2、3 類功能「**每次啟動 `inithull` 通常只能執行一次**」：第一次呼叫會設旗標、抑制後續動作。輸入檔有錯修正後，**要重新啟動 `inithull`**，不要在同一次 session 反覆按。

### 33.4.3 功能總表

| 群組 | 功能 | 類型 |
|---|---|---|
| Initiate Hull Model | Hullref、Structref、Blocks、Frame/long. positions | 精靈或檔案 |
| Cutouts and Clips | 外部 cutout 定義、macro cutout／clip 檢查、自動 cutout 選擇、具名 cutout、cutout setting | create／check |
| Profiles and Flanges | 專案型材、U／I 型、connection codes、endcut table、endcut selection、adjust endcuts | check／create |
| Other Standard Set-up | bracket standard／instance、bevel standard、shrinkage、Execution Unit、焊接補償表、Tap | create |
| Naming | autopos 設定、part name control（五步精靈）、functional properties | create |
| Production Support | 參考平面、型材限制、型材轉板、殼縱骨曲率、FRP | create／check |
| Release for AVEVA Everything3D | 把 hull 環境變數（`d065` 檔）複製進資料庫 | 一次性動作 |

### 33.4.4 Hull Reference、Structure Reference 與 Block

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Hull Reference Object 表單

*圖 33-6　Hullref 表單：垂線 X 座標、型寬、最大座標、主曲面與甲板曲面名稱、frame／waterline／buttock 座標表名、seam 表名。（AVEVA 官方文件截圖，僅供內部教學）*

1. **Hullref**（`Hullref, create`）：開啟時以 `SB_HREF` 指向的物件預填欄位；欲看別的物件，在名稱欄鍵入後按 `Extract Data from DB`（**不會警告並放棄未存修改**）。`Maximum coordinate`（預設 1000000）是合理性檢查，任何船體座標超出即報錯；`Name of the hull form` 是曲面名稱，必須正確。`Additional Surfaces…` 加其他曲面（名稱、後綴、Shell 或 Deck）。建好後可在 Structural Design 切幾條曲線驗證曲面，並讓 `SB_HREF` 指向。**從舊專案複製預設檔時，要移除舊的 hull reference 參照。**
2. **Structref**：與 Hullref 同樣的表單邏輯，`SB_SREF` 指向；不相關的欄位（如無橫向構件的船）留空。
3. **Blocks**：CSV 檔，首列為註解。欄位：`Type(D|P)`（設計／生產 block）、`Name`、`Nom. Aft/Stbd/Bot/For/Port/Top`、`Encl. Block`、`Offset ×6`、`Limit ×6`（前綴 `SUR/`、`RSO/`、`PLA/`）、`Sym`（Yes／No）、`Colour`、`envelope`。**已存在的 block 只在內容真的變更時更新**；`Type` 填 `DELETE` 即刪除。
4. **Frame/long. positions**：建立 `gentab`（主網格：肋骨號、位置與舯部縱向位置）。注意：Structural Design 也可互動建立 gentab，**從檔案再跑一次會覆蓋**互動結果，反向則不會回寫檔案。

## 33.5 Planar Modelling（平面板架建模）

### 33.5.1 概念與資料庫
Planar Hull Modelling 涵蓋「早期設計 → 生產準備」，**不含強度計算**，支援英制單位。三個活動：產生模型、由模型衍生視圖、發展圖面；兩種模式：互動（正常）與背景（只能由備好的 scheme 產生板架、由輸入檔產生視圖）。

資料庫：`SB_CGDB`（曲面、hull reference、seams／butts、肋骨／水線／縱剖線）、`SB_OGDB`（structure reference、blocks、板架、bracket、planes、endcut table）、`SBD_PICT`（板架圖與視圖）、`SB_PDB`（圖面）、`SBD_STD`／`SBD_FORM`（標準與圖框）、`SB_REFDB`（拓撲物件）、`SB_TID`（早期設計：主要尺度、RSO、艙室）。

**三層結構**：**panel**（板架）是最小可獨立儲存單位，含「平面＋封閉邊界」；panel 內有 **component group**（同類型零件一組，修改刪除以「組」為單位）；panel 亦可用文字 **input scheme** 完整描述，**scheme 與 panel 物件互為等價、可互相衍生**。

### 33.5.2 Plane Panel Editor

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull Editor 視窗：scheme 文字與生成錯誤區

*圖 33-7　Hull Editor：上方為 scheme 陳述式（紅色底線者為出錯陳述式），下方為生成錯誤訊息。（AVEVA 官方文件截圖，僅供內部教學）*

這是 **modeless** 對話框，可在開啟時使用其他功能（如 Planar > Model > Create）並讓內容更新。**Planar > Scheme > Input／Edit、Planar > Model > Edit** 都會開啟它。每個 scheme 描述一個 panel（名稱相同）；**一組類似板架（如雙層底的肋板）可同時啟用並一起修改**，編輯器顯示第一塊，修改套用到全部。knuckled panel 與含 bracket panel 時，編輯器會連同子 panel／bracket panel 的 scheme 一起顯示（**bracket panel 可被多個主板架共用，改一處會影響其他主板架**）。

- **顏色**：識別行為綠色；已改未執行為紫色，執行成功後轉黑；錯誤亮紅，只有警告則暗紅；目前陳述式有底線。雙擊錯誤行會跳到出錯陳述式。
- **分號不能手動增刪**：用選單新增／刪除陳述式。刪除**已執行過**的陳述式時，關鍵字會被改成 `DEL` 並執行以移除元件，文字仍留在編輯器。

### 33.5.3 Planar 選單功能一覽
**Model**（作用於 component 群組，須有已啟用 panel）：`Create`／`Modify`／`Edit`（互動建立；Create 預設加入既有 panel，**新建 panel 須在 indicate 提示輸入 `OPTIONS`**）、`Assembly`（群組內零件要分屬不同組裝，先 `Divide`）、`Divide`、`Split_STI`（支援 `FR24(6)60` 重複語法）、`Modify_STI_end`、`Delete`。

**Panel**（作用於整塊 panel）：

| 功能 | 說明 |
|---|---|
| Copy／Move | 位置可絕對或沿主軸相對（`--FR30` 向後 30 個肋骨，`+LP5` 向上 5 個縱向位置）；名稱可用重複語法如 `AB123-8<12(10)32>P`；絕對位置須保持原法向向量 |
| Split | 以座標、視圖中的線、相交 panel 或 RSO 分割；**加強材被切時 connection code 取自 Connection Control File（panel 切用 type 4、平面切用 type 5；未定義則用 40、70）** |
| Remove Seam | 移除接縫並合併兩側板、加強材、flange；屬性不同時彈出三欄表單逐項挑選 |
| Recreate／Topology | 依原定義重生（自動拓撲排序）；圖示相依物件（Defining／Dependent） |
| Compare Panels | 比較大 panel 與衍生生產 panel：紅（較小或材質不同）、藍（較大同材質）、綠（相同）、白（無對應） |
| Rename／Modify Symmetry Code／Knuckled／Jumbo Split | Rename 更新所有參照；`Modify Symmetry Code` 把 SBP 板分成 P、S（須設 `SBH_MOD_SYM=MIRR` 才真分割）；官方稱多數情況 Split 優於 Jumbo Split |
| Toggle Divide | 見 33.5.12 |

**其他群組**：`Scheme`（`Input`、`Show`、`Edit`、`Run Mode`：`Confirm` 開啟時 boundary／curve 逐段顯示以查錯；`Gen in Background`，經 Job Launcher，可選 `.schlst` 清單；`Create Lists`）。`View`（`Create`、`Detail`、`Recreate`、`Modify`、`Select`、`Edit`、`Properties`）。`PosNo`（`Scope` 設作用範圍、`Set`、`Change`、`Copy` 只複製「最終」號碼〔`POSNO_PREFIX`／`SUFFIX` 判定〕、`Auto` 啟動 autopos）。`RSO`（`Create RSO`：**RSO 參照比 panel 參照穩定，jumbo 之後再細分也不會斷**）。`Select`：**修改前必須 `Activate`**（讀出並鎖定；外框 `S`＝已存、`M`＝已修改）、`Store`、`Skip`、`Store and Skip`、`List Activated`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕右鍵快顯功能表：Activate、Deactivate、Stiffener > Symmetry、Generate Parts

*圖 33-8　對 panel 元件按右鍵：啟用／取消啟用、修改元件對稱性、直接 Generate Parts。（AVEVA 官方文件截圖，僅供內部教學）*

**Hull Tools**：`Note`（Position Number、Assembly、Bevel、Config Set／Move）、`Curve > Create Curve`（多條曲線名稱格式 `<prefix><start>(<step>)<end>`，如 `SBX34()46`）與 `Store Curve`、`Functional Description`、`Shrinkage Info`（顯示主收縮方向與各板係數，mm/m）、`Re Init`、`Painting Areas`、`Part Checking`、`Vitesse`（列出 `SB_PYTHON` 目錄的腳本供執行）。

### 33.5.4 設計語言：Scheme 的基本規則

**結構**：scheme 第一行是 identifier（不含關鍵字、不需分號，只看前 72 欄，前 12 字元會印在繪圖上）；之後是 `PANEL`（必為識別行之後的第一個陳述式，或先放 `ONLY` 以容納前置註解）、`BOUNDARY`，再接各 component 陳述式。陳述式以分號結尾（scheme 檔行寬不可超過 72 字元），關鍵字超過三字元可縮寫為前三字元（`PAN`、`BOU`、`STI`）。

| 規則 | 說明 |
|---|---|
| 重複語法 | `start(step)end` 或 `start-step-end`：`10-15`、`6(2)14`、`1.5(0.3)2.1`；一個陳述式最多處理 25 個元件 |
| 值個數規則 | 每個關鍵字給的值個數須是 0（用預設）、1（全部共用）或 n（逐一對應）；違反通常報錯 |
| 座標 | 本地 `U`、`V` 或全域 `X`、`Y`、`Z`；**可用 `FR`（肋骨）與 `LP`（縱向位置）項**，如 `FR123.5`、`FR123(5)133+500`、`LP-15`（負值表示另一舷） |
| 拓撲點 | `P5`、`P5()7+100`；`UV=P5`、`XYZ=P1()2` |
| 數值變數 | `N1`–`N99`（負號取反），以 `NUM` 陳述式給值，**一旦給值不可重定義** |

### 33.5.5 PANEL 與 BOUNDARY

```
PAN, 'AA334-6', Y=6503, DT=104;                                  ! 一般板架，位置由主軸座標定義
PAN, 'AA999-9', ORI=FR111,1000,0,333, UAX=FR113,1100,0, VAX=FR111,2000,100, DT=999;
PAN, 'PANEL_BKT', BRA;                                           ! bracket panel
```

- **命名**：只能用字母、數字、`-`、`_`；建議 `'<block>-<pan>'`，block 預設取自名稱。
- **有效側（`pan_loc`）**：`SBP`（左右舷各一、互為鏡像）、`S`、`P`、`SP`（跨或位於 CL，須依實際位置描述，不可鏡射）。**跨板參照時要記得：參照永遠是對「該板儲存的位置」**——例如描述在左舷的右舷肋板，邊界參照右舷縱桁時要加 `REF`。
- **Data type（DT）**：整數，使用者分類用；**jumbo 為 800–899，957 bracket panel、958 knuckled 子板、959 舾裝鋼構轉入的專用板**；第二位數 9 表水密艙壁、8 非水密、0–7 其他（影響隱藏相交 panel 的線型）。Structural Design 的設計板固定為 1600，水密改用 `WT`。可由 `SBH_PANEL_DT`／`SBH_PANEL_GT` 檔限制可選值；檔案不存在則預設 101。
- 其他：`GT`（幾何型別，預設 101，90 為可轉型材的 panel profile、958 為 knuckled 主板）、`MAR`、`WOR`、`LIS`、`AS1`–`AS4`、`AR`／`ARP`／`ARS`（組裝參照）、`GMS`（標記面）、`BUI`（建造號；預設檔 `CHECK_BUILD` 0／1／2 控制檢查）、`WT`／`NOWT`、`STO=PS|SB`。
- **Knuckled 主板**：`PAN,'TB123-1',SBP,DT=343, SUB='TB123-SUB1':'TB123-SUB2';` 或 `SUB='TB123-*'`；子板以 `PAN,'…',SUB,Z=15000;` 宣告，boundary 以 `CON`（預設彎曲型 9999）標示彎折線。

**BOUNDARY**：最多 12 條邊界，**逆時針**、以 `/` 分隔，每條方向可任意（系統自動轉）。邊界種類：

| 種類 | 範例 | 備註 |
|---|---|---|
| 曲線參照 | `FR105`、`WL2`、`BT0` | 只能在第一條；`SYM` 反射接成跨 CL 邊界 |
| 直線 | `U=…`、`V=…`、`X=FR75` | 有限制線與無限制線 |
| 曲面 | `SURF='…'` 搭配 `XMIN`…`ZMAX`、`SID` | 預設 `YMIN=0`；反射曲面要用負值限制 |
| 相交 plane／panel／RSO | `'BULKH', SID=PS`、`'_RSO_DECK1', SID=BOT, COR=750` | `COR` 平行位移；兩側板厚差由 `CHAMFER_ADJUST` 控制；自動加 hook 延伸（可用 `REDUCE_HOOKS` 縮減） |
| 同平面 panel | `'NAME', LIM=…` | 取其某一邊或 flange |
| 型材斷面 | `CROSS, L140, COR=50`、`'AA124', SL14, SHORT` | 取型材與本板平面的相交 |
| 沿型材邊 | `ALONG, L470, X=FR117, COR=50` | 正值重疊、負值留間隙；延伸 500（殼板縱骨）或 1000 mm |
| 重疊型材端 | `OVERLAP, L320, SID=FOR, 'PANA', R, M1=-50` | 參數 `R`（凸耳）、`M1`–`M4` |

> **專業提醒：** `BOUNDARY` 是最容易引發連鎖錯誤的陳述式。官方指出 `PANEL`、`BOUNDARY` 或 `SAVE` 之前的陳述式出錯，常導致後續陳述式一起出錯；除錯時先開 `Run Mode > Confirm`，逐段檢查邊界。

### 33.5.6 SEAM 與 PLATE

- **SEAM**：把 panel 切成板。`SEAM[,BEV=|LBEV=|RBEV=][,SID=][,EXC=|LEXC=|REXC=][,GRI=][,WEL=] <定義>`。定義方式：沿線（`Z=1500`、兩點）、與既有 seam／limit 平行（`LIM=`／`SEAM=`＋`M1`、`M2`、`NUMB`）、垂直於 limit（`LIM=`）、為相交 panel 產生（`'PANEL'`，兩側各一條）、沿曲線。`FROM`／`TO` 指定起止於哪條 seam。
- **PLATE**：`PLATE[, <point>] , MAT=<厚>[, MSIDE=][, QUAL=][, DEST=][, SURF=][, RAW=][, POS=][, AS1…][, COLOUR=]`。每塊板用一點定位（只有一塊時可省略）。`MAT` 的值是**沿 panel 法向的座標**：一值表示一面與 mould plane 重合（正負決定板在哪一側），兩值是兩面的座標；同一陳述式有多塊板時，每塊給一個 `MAT` 值（**不是**兩面座標）。材質預設為軟鋼；`QUAL` 可用代碼或已登記字串。

```
PLA, MAT=14;                              ! 整塊 panel 一塊板
PLA, X=FR75(2)77, Z=1500, MAT=15, MSIDE=PS;
```

### 33.5.7 STIFFENER、FLANGE 與 PILLAR

**STIFFENER**（含 swedging）：四種子語法——

| 子語法 | 做法 | 範例 |
|---|---|---|
| Mould line first | 先定義 mould line（直接給線，或平行於 limit／線：`LIM=`、`M1`、`M2`、`NUMB`），再逐端定義終止方式 | `STI, SID=AFT, LIM=-3, PRO=10,200,12, NUMB=3, M1=900, M2=750, V1=5000/CON=14;` |
| End points first | 先定義兩端；一端可同時定義方向（接縱桁），也可用 `T=` 明給方向 | `STI, L300-320, CUT=1100, CON=4/ 'LSK1', SL30-32, CUT=1100, CON=4;` |
| Connection stiffener | 高度自動化：type 4（一端接加強材／flange／外輪廓，另一端自由）與 type 5（兩端皆接，預設 `PRO=10,200,12`、`CUT=1220,100 / 1120`）；方向自動選 | `STI, 4, SID=AFT, L190-250;` |
| Curved stiffener | 用 `CURVED`，平行於 limit、孔或沿曲線 | `STI, CUR, LIM=3, M1=20, CON=14/CON=14;` |

重點：`PRO=<type>,<param…>`、`CON=`（連接碼）、`CUT=`（endcut code＋參數）；**斜線 `/` 前為第一端、後為第二端**；加強材腹板位於 mould line **左側**；一個陳述式可產生最多 25 支。型材終止於外輪廓時，視連接碼類型當成對相切線或相切面的 flange 處理（前者 endcut 角通常 90 度，後者可為任意角）。

- **FLANGE**：兩類——**焊接 flange**（扁鋼或圓棒／管，沿 limit 或孔，`LIM=`／`CNO=`，`UNSYM=` 偏置）；**折邊 flange**（僅能沿外輪廓直線段，`SID`、`LIM`、`TYPE`、`H`＝名義高、端點 `CUT`、`M1`，須先設 `SBH_FLANGE_CTRL` 才用客戶定義，否則用內建標準、角度預設 30 度）。加折邊會改變外輪廓，常需重跑 `BOUNDARY`；反之重跑 `BOUNDARY` 也要重跑 `FLANGE`。非扁鋼或不垂直板面的「flange」要用 `STIFFENER` 建。
- **PILLAR**：自由柱，兩端連接；位置用「線＋端點限制」或明給端點；方向三種：沿船主方向、`T=`角度（僅限描述線沿 w 軸）或給額外點；**不對稱型材須用 `SID` 指定翼板方向**。官方註明柱的連接碼「不用於計算」。

### 33.5.8 HOLE、NOTCH、CUTOUT 與 Clip

**HOLE**（板）：`HOLE, <標準孔|物件>, <位置>…[, FIC][, PIL=][, M1=][, P|S][, CRO][, SPC=…][, BEV=][, BRI…][, HOO…]`。位置可用點（加 `T=` 角度或 `XT/YT/ZT` 第二點）或「沿 limit」（`LIM=`、`M1`、`ALONG`、`PARALLEL`、`INC`）。重點：

| 項目 | 說明 |
|---|---|
| `FIC`（fictitious） | 不當孔分割，只作標記輪廓 |
| 穿越物件 | 參照穿越的 panel（`PIL=` 柱號）或物件，系統自動依物件幾何開孔；`M1` 為相對斷面輪廓的平行位移 |
| Bridge／Hook 孔 | 接縫穿過孔時：`BRI`（橋，`BRW` 寬、`BRR` 角半徑；預設 `BRIDGE_WIDTH`＝100、`BRIDGE_RADIUS`＝15）、`HOO`（鉤，`HGP` 間隙、`HRA` 半徑、`HTY` 型別 0–3；預設 `HOOK_GAP`＝25、`HOOK_RADIUS`＝15） |

加強材上的孔以 `D=<距端點>` 或 `U|V|X|Y|Z=` 相交位置、`M1`（孔心到板面距離）、`INC` 與 `S-ref` 指定；**加強材與其孔分屬不同陳述式時，可能需整批重跑，否則系統只警告並盡量處理。**

**NOTCH**（板）：位置有「角」（`COR=`，不對稱缺口要再用 `LIM=` 指定落在哪條邊）、「沿 limit」（`LIM=`＋`U|V|X|Y|Z=`＋`ALONG`）、「為接縫」（`SEAM=`，可帶相鄰板名或曲面名）。範例：`NOT, VUF200*75*50, COR=1, LIM=3;`、`NOT, R50, LIM=1, Y=10000(400)12000;`。預設檔 `CORNER_NOTCH_CHECK`、`SEAM_NOTCH_CHECK` 可檢查重複定義。加強材缺口則有「接縫處」、「距端點距離」、「與線相交處」三種位置。

**CUTOUT**（為穿過的加強材）：`CUTOUT, [TYPE=]<code> [,P|S] , <ext_prof_ref>｜<inters_pan> [,REF][,C=][,M1=][,CLIP=|CT1/CT2/CT3=][,CL1…][,MAT=][,WELD=…][,BWEB=…][,NABU][,NABI]…`。重點關鍵字：

| 關鍵字 | 說明 |
|---|---|
| `CLIP=XYZ` | 內建 clip 三位碼；與 `CT1`／`CT2`／`CT3`（客戶 clip 型別）**不可併用** |
| `WELD`／`WCLIP`／`WPROF`／`WSHELL` | 焊腳；`BCLIP`、`BWEB`、`BFLA`、`BSHELL`（含 `BC…` 版）為各處 bevel |

範例：`CUT, TYP=53, CLI=012, AREA=60, L110-230;`；客戶 clip：`CUT, TYP=10, CT1=101, CT2=102, L120(1)5, SID=FOR, MAT=8;`。**加強材上的 cutout 只能為同 panel 的其他加強材設，不可帶 clip**，語法 `CUT, 5, SL1-10/ SF105(3)111;`（被穿者在斜線前，最多 300 組）。互動模式（Planar > Model > Create > Cutout）可逐一點選，也可沿某邊或所有邊**自動設定**。

**交叉 cutout 9999**（蛋箱式互嵌）：兩片 panel 都要各設一次，且 panel B 須先建好再設 panel A 的 cutout。`CUTOUT, 9999, 'B', DIR=BOT, R1=50, R2=100 [, M1…M4]`；`R1<0` 為 KS 缺口（預設 −10）。三個環境變數控制自由空間：`SBH_INTERCROSS_CUTOUT_TOPDIST`（5 mm，兩側平分）、`…_SIDEDIST`（1.5 mm）、`…_TOPRADIUS`（3 mm）；兩 panel 在至少一條 limit 上要有共同點。分割時若另一側未設或方向不對，系統會發警告。

> 〔公開版未收錄：AVEVA 官方產品截圖〕蛋箱式交叉 cutout 控制參數 TD、SD、TR、R1、R2、M1–M4

*圖 33-9　交叉 cutout（9999）的控制參數。（AVEVA 官方文件截圖，僅供內部教學）*

### 33.5.9 BRACKET（肘板）

**BRACKET 陳述式**四種主語法：(1) 由周邊結構產生的 type standard bracket，共七種子語法（對應連接情形）；(2) 明給參數；(3) 掛接 bracket panel 或零件；(4) 複製既有 bracket。

> 〔公開版未收錄：AVEVA 官方產品截圖〕七種子語法對應的典型肘板連接情形

*圖 33-10　Bracket 子語法 1–6 的典型佈置（子語法 7 另有圖）。（AVEVA 官方文件截圖，僅供內部教學）*

| 子語法 | 連接情形 |
|---|---|
| 1 | panel／profile：一臂終止於相交型材，其他可為 panel 面 |
| 2 | 同 1，但兩臂完全自由；可做三臂肘板 |
| 3 | panel／panel：肘板與兩 panel 共平面 |
| 4 | profile／profile：兩型材約共平面 |
| 5 | panel／profile，如 2 但型材端被重疊 |
| 6 | profile／profile，至少一端重疊 |
| 7 | 周圍結構任意，肘板平面由使用者指定（二臂或三臂） |

共通關鍵字：`BRA, <型別>[,COR=][,MIRR][,SYN=]`、`MAT=`（板厚）、`R`／`RA`／`RB`（半徑）、`TOLA`／`TOLB`（趾長）、`NOT／NOA／NOB／NOC`（角缺口，給 `-1` 為取消、負號為對角平分線鏡射）、`SID`（相對 panel 的位置）、`PSID`（加強材側）、`PRA…PRE`（肘板上加強材尺寸，`p_type=-1` 刪除）、`WELD`（二臂最多 4 值：`w_a, w_b, w_toea, w_toeb`）、`BEV`、`VAR`（1–8）、`SEP`／`BEL`、`BRPAN`、`BHO`（肘板上的孔，一個肘板一種孔型）。**3 臂肘板可用「深度」控制尺寸（子語法 2、3、7）**。肘板名稱格式為 `<型別><A臂 cm>/<B臂 cm>-<x><y><z>`，例如 `BS50/50-200`（標準）、`EA80/75-209`（個別）；z＝0 標準、9 個別、1–8 使用者變體。

```
BRA, A, COR=5, SID=AFT, PSIDE=SB, MAT=12, L160/S1;          ! 子語法 1，斜線前為「外來」元件
BRA, 'BRA_PAN', MOVE, X=0(700)2800;                         ! 掛接 bracket panel 並複製 4 份
BRA, COPY= 'AA171-7', FCNO=5;                               ! 複製他板的肘板
```

### 33.5.10 其他陳述式

| 陳述式 | 要點 |
|---|---|
| `EXCESS` | `EXC, LIM=<n>, M1=<量>[, TYP=<名>];` 沿 limit 加 excess；一條邊最多 5 種；只存於 panel，**不存入板零件** |
| `DOUBLING` | 疊板：`DOU, CNO=2, M1=250, M2=15, MAT=12, SID=AFT, POS=8;`，位置由孔（`CNO`）、缺口（`NOT`）或曲線（`CUR`）決定；`CLO` 全蓋、`M2` 為內緣間距 |
| `CMP` | 楔形補償：`CMP, TYPE=1\|2, LIM=, M1=[, M2=, COR=]`；`M1>0` 向外 |
| `SHRINKAGE` | `SHR[,<line>][,M1…M6]`；`SHR,;` 全自動，須有 shrinkage 物件；補償在零件產生時進行 |
| `WELD` | 沿 limit 分區間指定 bevel 與焊腳：`WELD, LIM=1, TO=1, BEV=2, WELD=6.5;`；`AUTO`、`EQUAL`、`KNA`／`KNP` |
| `CURVE`／`POINT`／`PLN` | 臨時曲線、拓撲點、臨時平面（不存資料庫）；`PLN,'X-PLANE',X=FR175+100;` |
| `MARKING`／`TAP`／`SWAGE` | GSD 與標記線；seam 與孔／缺口／cutout 交點加延伸片（`TAP, TYP=2, SEA=1, LIM=2;`）；小波紋（`SWA, TYP=101, SID=FOR, U=500, M2=1200;`） |

FRP 專案時，多數元件陳述式有 FRP 版本，另有 `BEAD` 與 `LAMINATE_*`。

### 33.5.11 由模型衍生視圖與圖面
視圖來源有三：互動 `View > Create`／`Detail`、背景 `Hull Model Drawings`（`SJ002`）、在 view 內生成 panel 時逐步長出的圖。**符號視圖**把 panel 畫成外輪廓、seam＋bevel 符號、加強材（mould line＋endcut 符號＋材料側符號）、肘板、flange、clip，視 panel 與繪圖平面夾角採「投影」或「相交」。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create View 對話框：Plane、Limits、Select、Outfit、Misc 五個頁籤

*圖 33-11　Create View：Plane 頁籤選擇切面（X／Y／Z、3 points、Panel、Curve、RSO）、Looking 方向與比例。（AVEVA 官方文件截圖，僅供內部教學）*

五個頁籤：**Plane**（切面可由座標、三點、panel〔含 bracket、加強材、flange 腹板〕、曲線、RSO〔可指定 face〕定義）、**Limits**（盒子與深度）、**Select**（`Design View` 或 `Assembly View`；`Automatic selection`；Block／Panel 包含與排除）、**Outfit**（舾裝以 3D 切片呈現，但 `Wireline`、`Wireline Hidden Line` **不切片**，完整顯示）、**Misc**（座標軸、剖面符號）。`Detail` 預設比例為當前視圖的兩倍。**`Recreate`** 依原資料重生並**加入範圍內新 panel**（`OPTIONS` 可抑制），已加的量測保留；預設檔 `UPDATE_NOTE` 可更新 note。

背景視圖輸入語言（目錄 `SB_SHIPDATA`）：`NAME,'<view>'[/SCALE=]; PLANE …; LOOKING,…; DEPTH, d1, d2; LIMITS,…; SELECT /AUTOSELECT /PANEL= …; RECREATE,'<d>';`；`PLANE` 可用三點、`CL`／`BL`／`FR<n>`、`X:=`、`/PANEL=`、`/CURVE=` 等；`DEPTH` 預設 100；結果存 `SBD_PICT`，清單 `SB<jobno>.LST`。

**生成方式與一致性**：板架可 **separate**（空白畫面）或 **in view**（有開啟圖面時）生成；in view 時每個 `PANEL` 範圍只處理一個 panel。**同一 panel 以不同方式生成，圖與模型可能不一致**；解法是 `View > Recreate`／`Modify` 或背景 `TBHMDWG`。**Envelope**（以最小外框代替視圖）可加速重繪，並避免資訊加到錯誤子圖。

### 33.5.12 Toggle Divide、Corrugated Bulkhead 與 Jumbo Panel
**Toggle Divide**：**改變相交 panel 的優先順序**（誰連續、誰被切）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Toggle Divide 對話框

*圖 33-12　Toggle Divide：選擇連續 panel、被相交 panel，並可 Check 或 Merge and Split。（AVEVA 官方文件截圖，僅供內部教學）*

路徑 Planar Hull > Panel > Toggle divide。選「連續 panel」（兩塊相容 panel，或一塊帶 seam 者）與「被相交 panel」；`Check` 預覽新 scheme；`Merge and Split` 合併連續 panel、為被相交者加 seam、合併連續者的加強材、切斷被相交者的加強材並**加 cutout**。**限制**：儲存碼須相容；多視圖專案**只能合併設計 panel**；混合對稱與非對稱 panel 時，系統自動先分舷，之後須在另一舷再執行一次。

**Corrugated Bulkhead**（View > Addins）：四個頁籤——General Information（以參數、RSO 或既有 2D 幾何建立；參數有 Radius、Height、Width、Breadth、Start Length、Start Position）、Boundary Limits、Seam Position（橫艙壁填 Y 值、縱艙壁填 X 值）、General Purpose String（`Weld & Excess` 設主板與子板的焊接屬性）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Corrugated Bulkhead 附加功能對話框

*圖 33-13　Corrugated Bulkhead：板架資訊、方向（Transverse／Longitudinal）與波紋參數。（AVEVA 官方文件截圖，僅供內部教學）*

**Jumbo panel**：早期設計把整片甲板、艙壁當一塊（技術上與一般 panel 相同，須單平面、不可 knuckle），日後再細分。**data type 保留 800–899**；建議集中放在自己的 block。

### 33.5.13 預設檔（default file）
純文字 `參數=值`；未寫者用系統預設；`SJ001`（互動）、`SJ011`（背景產生）、`SJ002`（背景視圖）各有預設檔。重要參數：

| 群組 | 參數 |
|---|---|
| 基礎 | `NEW_BKT`（**啟用延伸肘板處理，通常應設**）、`KNUCKLED_STIFFENERS`、`MAX_KNUCKLED_ANGLE`（30）、`SURFACES`、`SURFACE_REFERENCE`（`EXISTING`／`CUT`）、`FR_TERM_OUT`、`LP_TERM_OUT` |
| 編輯 | `SCH_CREATE`、`SCH_DELETE`、`SBH_OPEN_DLG`（`KEYIN` 預設，目錄檔案多時建議）、`STORE_FR`／`STORE_LP`（儲存肋骨號而非數值，使 panel 跟著肋骨表變動） |
| 建模 | `CHAMFER_ADJUST`（99＝依 bevel 設定，**有 bevel 定義檔時強烈建議**）、`CHAMFER_STEP`（3 mm）、`CHECK_BUILD`、`EARLY_DESIGN`、`BRIDGE_*`、`HOOK_*`、`POSNO_PREFIX`／`SUFFIX`、`SPIGOT`、`STD_CLIP_TCODE`、`USER_TAG_UNIQUE`、`SHRINK_OBJ` |
| 視圖 | `DRAWINGSCALE`（100）、`DRAW_EXCESS`（0–3）、`DRAW_PAN`、`EXC_TYPE_1…5`、`BEVEL_COLOUR_OS／TS`、`CURR_BLOCK`、`ABUT_PROF_DIST`（30 mm） |

背景產生（Job Launcher）**只能處理備好的 scheme、且只能 separate 生成**；同名 panel 已存在則**整個取代**；各陳述式獨立處理，但 `PANEL`、`BOUNDARY` 或 `SAVE` 前的錯誤會連帶；警告元件仍產生，**錯誤則通常不產生**。

## 33.6 二次開發怎麼接

| 目標 | 可用接點 | 依據 | 狀態 |
|---|---|---|---|
| 客製 part name | `_TBhook_CustPartName.py::getPartName(...)`，簽名固定 | 官方有完整參數清單與範例 | 語法有依據；**Python 版本與環境**〔待核對〕 |
| 可設定 note | `_TBhook_ConfigNote.py` 五個方法 | 官方有介面與範例 | 有依據 |
| 首次建 boundary 後動作 | PML 函式 `!!pHullTriggerPostBoundaryCreation()` | 官方有範例（預設被註解） | 有依據；改後須回歸測試 |
| Scheme 版面、孔／缺口／肘板 hook | `_TBhook_PPanScheme`（`SplitIntoLines`、`FormatLine`）；`_TbhookCustHole`、`_TbhookCustNotch`、`_TBhookCustBracket` | 前者官方有說明；後三者僅說明存在 | 後三者介面〔待核對〕 |
| 批次視圖與資料讀取 | 背景視圖語言（33.5.11）；Data Extraction／Vitesse（第 15 章）、PML（第 12 章） | 官方語法完整；屬性對照無 | 屬性對照〔待核對〕 |
| 產生 scheme | 直接寫 `.sch` 文字（行寬 ≤ 72、分號結尾），經 `Gen in Background` 或 Job Launcher 批次生成 | 官方描述 scheme 與 panel 等價、背景模式 | 語法有依據；自動產生的**驗證流程與 CLI 啟動方式〔待核對〕** |
| 標準檔案產生器 | 以腳本產生 TIL 檔，再用 `inithull` 編譯 | 官方檔案格式完整 | 格式有依據；`inithull` 是否可無人值守執行〔待核對〕 |

> **專業提醒：** 不要用程式直接改資料庫內的標準物件；標準物件只能由 `inithull` 編譯產生。批次產生 scheme 前，先確認該標準已編譯、環境變數已設（見 33.3.1）。

## 33.7 常見錯誤

| 錯誤 | 後果與對策 |
|---|---|
| 標準未編譯就建板 | bevel 不被接受、endcut 不顯示、part name 失敗；依 33.2.2 順序並檢查 `.lst` |
| `inithull` 同一次 session 反覆執行 | 第二次起動作被抑制；改檔後重啟 |
| 沒有 part name 規則或規則不全 | 官方沒有預設規則 |
| `FLA_TYPE` 編號落在 200–300；改 endcut 選擇列 | 不被接受／破壞標準；只增參數列 |
| 蛋箱 cutout 只設一側 | 分割時警告；兩 panel 各設一次且方向相反 |
| 改了 Boundary 沒重跑 Flange | 折邊與輪廓不一致；兩者互相重跑 |
| 對稱 panel 的參照少加 `REF` | 參照落在錯舷；依「儲存位置」寫 |
| 用數值座標而非 FR／LP／拓撲點 | 變更時不連動（第 5 章） |

## 33.8 本章小結

1. **標準先於建模**：控制檔 → `inithull` 編譯 → `SB_OGDB` 物件 → 環境變數啟用；part name 與 bevel 沒有預設標準，必須自建。
2. **`inithull` 是一次性初始化工具**，同一次 session 通常只能執行一次，應由系統或專案經理操作。
3. **panel 是最小單位，scheme 與 panel 等價**；陳述式順序 `PANEL → BOUNDARY → 各元件`，盡量用 FR／LP 與拓撲參照。
4. 加強材、孔、cutout、肘板都有多種子語法，要記的是各自的限制。
5. 視圖與模型可能不同步，用 Recreate 同步；**Toggle Divide** 處理相交 panel 的優先順序。
6. 官方文件只對少數 hook 給出介面，其餘二次開發項目須實測。

## 33.9 練習題與自我檢核

### 練習（只能在訓練專案）

1. **標準盤點**：依 33.3.1 的表，列出專案已設環境變數與對應檔案，找出缺漏。
2. **part name**：寫含 `FULL`／`SHORT` 兩層、涵蓋 `HPPL`、`HPPR`、`HBPL` 的控制檔，用 `inithull` 編譯並對照 `.lst`。
3. **讀 Scheme**：開啟一塊既有雙層底肋板，說出每個陳述式的作用並指出拓撲參照。
4. **BOUNDARY 除錯**：故意把邊界順序寫反，用 `Run Mode > Confirm` 觀察。
5. **Toggle Divide**：選一對相交 panel，先 `Check` 再決定是否 `Merge and Split`。

### 自我檢核

- [ ] 我能說明標準編譯與環境變數啟用流程，並知道 `inithull` 為何要重啟。
- [ ] 我知道 part name 與 bevel 沒有預設標準。
- [ ] 我能區分 endcut type、code 與 explicit parameters。
- [ ] 我能說出 flange、肘板、cutout 各自的限制。
- [ ] 我能說明 `PANEL`、`BOUNDARY` 順序與 `FR`／`LP`／拓撲點寫法。
- [ ] 我知道 panel 必須先 Activate 才能修改，以及視圖與模型為何不同步。

## 33.10 〔待核對〕彙整
1. 各 hook 的 Python 版本、執行環境與載入路徑（`PYTHONPATH` 以外）。
2. `_TbhookCustHole`、`_TbhookCustNotch`、`_TBhookCustBracket` 的完整介面（官方指向另一份 Vitesse 文件，本章未讀）。
3. 以程式產生 scheme 並批次生成的實際啟動方式與錯誤回報格式；`inithull` 能否無人值守執行。
4. Planar 功能與 Scheme 陳述式的 PML 屬性對照。
5. 官方文件為 TBH 時代手冊，12.1 實際選單位置（如 View > Addins）與預設檔名稱需核對。

## 33.11 資料來源與取材覆蓋
- AVEVA Marine 12.1 官方離線文件：*Hull Detailed Design* 之 **Setup, Customization and Standards**、**Initialization Utility Program**、**Planar Modelling**。
- 本課程延伸：[第 5 章](ch05_hull_modelling_zh-TW.reading.html)、[第 6 章](ch06_hull_production_zh-TW.reading.html)、[第 15 章](ch15_hull_vitesse_zh-TW.reading.html)。

**取材覆蓋（誠實說明）**：實際讀取約 **590 頁**（Setup 約 230、`inithull` 約 53、Planar 約 310），其餘未讀。
- **`inithull`**：全部子頁已讀。
- **Setup**：讀概述、概念與主要檔案格式頁；**未逐頁讀**各 Bevel type（10–149）、Endcut type、Notch type、Bracket Toe（1–136）、Flange End type 的圖解頁，以及 Bending Excess（M1／M2）與 Symbolic Hull Views 的語法細節。
- **Planar**：讀 Users Guide 概念、互動功能、背景視圖語法、預設檔前半與 Design Language 主要陳述式；**未讀**選單頁（與 Users Guide 重複，僅取目錄）、Painting Areas 全部子頁、Part Checking 的 System settings、Notch at Plate Corner 子頁、Special Side Webs 102／103／104、Curve 各子語法、Marking 的後四種子語法、Bracket 子語法 2–7 逐項細節、Special FRP Additions、預設檔 Picture Derivation 後半與 Drawing Development。

> **授權與界線：** 本章文字與表格為本課程依官方文件自行整理；截圖取自官方文件，僅供內部教學參考，不重製長段原文。

