# 第 26 章　目錄與等級深入：Catalogs and Specifications 與 Design Templates

> [第 25 章](ch25_catalogue_spec_zh-TW.reading.html)回答了「元件從哪裡來、等級如何約束設計」，並畫出 `CATA → SECT → CATE → SCOM` 與 `SPEC → SELE → SPCO` 兩棵樹。這一章是深入篇：**目錄管理員到底要遵守哪些慣例才能讓標準應用程式正常運作、參數有哪幾種、等級表格怎麼寫、元件特例（隱含直管、斜接彎頭）怎麼處理、如何檢查目錄一致性，以及官方的 Design Templates（參數化設計樣板）如何把一組基本體包成「像目錄元件一樣可選用」的物件。**
>
> 二次開發者要讀這章，是因為材料表、ISO 圖、碰撞檢查與管支架都依賴這些資料的「約定格式」；格式不符的錯誤不會出現在目錄端，而是在下游悄悄發生。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的 *Catalogs and Specifications* 大章（含 Design Conventions、Design Templates、Reference 與 GUI 四冊）。該文件沿用 PDMS 時代的 PARAGON 與 SPECON 說明，許多頁面仍寫 PDMS，本章照原樣保留。與第 25 章的分工：第 25 章講概念與參照鏈，本章講慣例、建置細節與樣板；第 25 章已講過的 `SPREF → SPCO → CATREF → SCOM → GMREF／PTREF` 不重複。官方文件是操作與語法手冊，**沒有可直接套用的 PML 範例程式**，因此「二次開發者怎麼接」一節只寫文件有明載的指令、屬性與偽屬性，其餘標〔待核對〕，需在你們公司的版本與訓練專案實測。章末列出實際讀了幾頁、哪些子樹沒讀。

## 26.1 學習目標

讀完本章，你應該能夠：

1. 說明目錄與等級必須遵守「設計慣例」的原因，以及不符時標準應用程式會怎樣失效。
2. 依慣例設定鋼構目錄與結構等級（型鋼、拼板厚度限制、附件、接頭），並說明 `ANY`、`NONE` 的意義。
3. 列出目錄資料庫完整階層，說明六類參數與求值單位規則。
4. 說明 `PTAXI`、`PTCAR`、`PTMIX` 與 P-line，以及 `LEVEL`、`TUFLA`、`CLFLA`、`OBST` 如何決定顯示與碰撞。
5. 說明等級表格的 Heading、Defaults、答案列與 `*`、`+`、`-`、`=`；說明 `DELETE` 與 `REMove` 的差別。
6. 說明 `PBORE0`、COCO 連接相容表與保溫等級的寫法。
7. 走過 Design Template 的建立、性質、規則、`TMPREF` 掛載、測試與變更傳播。
8. 使用 `CHECK` 檢查目錄，並說明二次開發者可讀取哪些屬性與偽屬性。

## 26.2 設計慣例（Design Conventions）

### 26.2.1 為什麼必須「照慣例」

官方的說明很直接：目錄與等級的資料庫階層原則上彈性很大，但在同一專案內必須嚴守慣例，才能確保資料完全相容；若要使用標準的 PARAGON 建庫應用程式與 Design 的選用應用程式，資料結構必須與應用程式巨集預期的一致，否則資料的往返可能失敗，應用程式也可能出錯。官方並特別提醒，目錄的某些部分會存放「看起來不像目錄資料、但對設計應用程式必不可少」的資訊，例如 Hangers and Supports 應用程式就用目錄與等級裡的使用者自訂屬性（UDA）去找相關資訊。

> **專業提醒：** **目錄裡不只有元件定義，還有給應用程式讀的「設定資料」。** 這些資料看起來像普通的 SELE／SPCO／TEXT，一改就可能讓某個設計應用程式失效；修改前先確認它是不是慣例的一部分。

### 26.2.2 鋼構目錄慣例（Set Steelwork Conventions）

鋼構目錄共有三種，各用不同的 `Purpose` 讓等級與應用程式辨識：

| 層級 | 必須設定 | 說明 |
|---|---|---|
| `CATA`（目錄） | `Purpose` = `STL`／`FITT`／`JOIN`／`PFIT` | 型鋼等級找 `STL`，接頭等級找 `JOIN`，管件附件等級找 `FITT`，拼板附件等級找 `PFIT`；建議再加有意義的 `Description` |
| `STSEC`（結構節） | `Purpose` = `REF`（參考資料）、`PRFL`（型鋼）、`FITT`、`JOIN`、`PFIT` | 與上層對應 |
| `STCA`（結構類別） | 同上 | `Purpose` 要對應等級中該項目的 `STYP` |
| 元件 | 必須設定 `GTYPE` | 例如 `GTYPE` 為 `BEAM` 的型鋼才能與 `GTYPE` 為 `BEAM` 的接頭搭配；`GTYPE` 為 `FITT` 的附件可用於任何 Fitting 等級 |
| `CSTANdard` | 文字，純供資訊與管理 | 例如英國型鋼標準 BS 5950 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕鋼構目錄的參考資料：STSE 之下的 STCA 擁有 GMSE、GMSS、PTSE、PTSS、NGMS、DTSE 六種集合

*圖 26-1　鋼構目錄結構：參考資料放在 `STCA` 之下，包含 3D 幾何集（GMSE）、2D 幾何集（GMSS）、點集（PTSE）、線集（PTSS）、負幾何集（NGMS）與資料集（DTSE）。（AVEVA 官方文件截圖，僅供內部教學）*

三種鋼構目錄的分層方式不同：

| 目錄 | 分層原則 | 要點 |
|---|---|---|
| Profile（型鋼） | 同一通用型式的斷面放同一個 `STSEC`；其下用類別分群 | 英國標準每個類別放相同序列尺寸，DIN 標準則同一類（IPE、IPB）放一起；多數情況每種通用型式只需一個 profile set 與一個 geometry set |
| Fitting（附件） | 同通用型式的附件放同一節（例如吊耳、加強板） | 節下再依「可用於哪種型鋼」分類（I、H、L、COLU、BEAM）；拼板附件 `PFIT` 格式相同 |
| Joint（接頭） | 同通用型式放同一節（角鋼片、端板、底板） | 節下依「可連接的斷面型式」分類（I-I、I-Chan、I-L）；斷面的通用型式存在 `Ownconn` 與 `Attconn` 屬性 |

### 26.2.3 結構等級的屬性階層

結構等級的運作方式與管路不同：官方強調應用程式以「表格形式」讀取等級，`Description` 必須放在正確層級，`Tanswer` 必須輸入，表單與選單才會正確建出；而且鋼構等級**可以有多個答案**（兩根梁的典型連接可以是栓接或焊接，同一個問題可有兩個答案）。

| 等級 | `SPEC` 的 `Purpose`／`Question` | `SELE` 的答案 | `SPCO` 指標 |
|---|---|---|---|
| 型鋼 | `STL`／`GYTP` | `Tanswer` = 型鋼通用型式 | `Catref` 指向目錄 `HPRF`，`Detref` 指向細部文字 |
| 拼板厚度限制 | `PLT`／`THK`（`Tquestions` = thickness） | — | 以 `SPCO` 的 `Ans`、`Maxans` 限定最小與最大板厚；**不使用 `CATREF`**，因為幾何在 Design 模組中定義 |
| 管件附件 | `FITT`／`TYPE` | 第一層 `Tanswer` = 可擁有此附件的型鋼型式，`ANY` 表示任何型鋼；第二層 `STYP` = 子型式（如 LUG、HOLE） | `Catref` 指向 `HFIT` |
| 拼板附件 | `PFIT`／`TYPE` | `STYP` 的子型式（如 Door、Window） | `Catref` 指向 `PFIT` |
| 接頭 | `JOIN`／`OTYP` | `OTYP` 為可擁有接頭的型鋼型式（`ANY` 任何、`NONE` 可設定 `PJOI` 的 specref）；`ATYP` 為可接上的型鋼型式（`ANY` 任何） | `Catref`、`Detref` |

> 〔公開版未收錄：AVEVA 官方產品截圖〕結構型鋼等級：SPEC 之下依型式（UB、UC、RHS、CHS）分 SELE，再往下是各規格的 SPCO

*圖 26-2　型鋼等級的階層：第一層 `SELE` 以通用型式（UB、UC、RHS、CHS）分流，葉節點 `SPCO` 是一個個斷面規格。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 拼板厚度限制說明同一套等級機制也能當作**允許值範圍**使用；檢查板厚是否合規時應讀這類等級，不要在程式裡寫死。

材料（`MATR`）要能在 Design 設定，必須能看到含材料的 Properties DB：在 Admin 把 PARAGON 對 Properties DB 改為可讀寫（`edit module PARAGON mode PROP rw`），於 PROPCON 建 `MATW`，再於 PARAGON 執行載入巨集 `MLOADPROP`，預設把 PDMSDFLTS 的 `DENSITY.DAT`（名稱、描述、密度 kg/m³）載入第一個找到的材料世界。

### 26.2.4 吊架與支架慣例（Hangers and Supports）

吊架目錄與管路目錄類似，使用 `PCLA`（管夾）、`HELE`（吊架元素）、`ROD`、`SCLA`（鋼夾）。要點：`PBOR` 對吊架解讀為等效吊桿直徑，不以吊桿尺寸選用的項目（管鞋、焊接附件）設為 0；`PCLA` 的 `P1` 一律指向管內流向；文字分別放在 `HMTE` 的 `XTEX`（材料）與 `HDTE` 的 `RTEX`（圖面長描述）、`STEX`（MTO 訂購碼）；Dataset 的 `PPROP` 設成設計參數運算式、`PURP` 設 `DESP`，保留的 Datakey 如 `POD`、`SWID`、`FLTH`、`CRAD`、`RINA`、`VSLO`；吊架等級的第一個問題必須是 `PBOR0`（`CHOOSE` 指令才能運作），`PURP` 設 `HANG`、`:VISI` 設 True，並放在 `Purpose` 為 `HSUP` 的 `SPWL`。

吊架組態（Hanger Configuration）存在目錄元素中、經由等級存取，與 `SPREF` 類似；組態 `CATE` 有 `:HCONN`、`:TCONN`、`:MAXLEN`／`:MINLEN` 等屬性，每個組態對應一支 PML 建構巨集 `MHB-{後綴}`（位於 `DES/SUPP`），以 `CALLSUP` 呼叫 `XHBPCLA`、`XHBHELE`、`XHBSCLA` 等工具子程式。

另有三張以等級階層存放的資料表（須放在 `Purpose` 為 `HSUP` 的 `SPWL`，`:VISI` 為 false）：吊架長度表（`HMML`，依管徑與材質查最小／最大長度，存於 `COMM`）、吊架間隙表（`HCLR`）、最大無支撐跨距表（`HSPT`，以 `TDEF` 運算式與 `TANS` 測試依列表順序取第一個符合者）。這是「用等級樹當查表資料庫」的好例子。

> **常見錯誤：** 把 `HSUP` 的資料表等級當成一般管路等級來整理或刪除。它們的 `:VISI` 為 false，本來就不給設計者選用，卻是吊架應用程式運作的依據。

## 26.3 目錄資料庫全貌

### 26.3.1 完整階層

> 〔公開版未收錄：AVEVA 官方產品截圖〕目錄資料庫完整階層：WORLD 之下有 TABWLD、CCTA、BLTA、CATA、UNIT、SPWL、GPWL、PRTWLD

*圖 26-3　目錄資料庫階層。與 `CATA` 同層的還有 `TABWLD`（表格定義）、`CCTA`（連接）、`BLTA`（螺栓）、`UNIT`（單位）、`SPWL`（等級）、`GPWL`（群組）、`PRTWLD`（零件世界）；`CATA` 下分管路（`SECT`／`CATE`）與鋼構（`STSE`／`STCA`）兩條線。（AVEVA 官方文件截圖，僅供內部教學）*

這張圖比第 25 章的簡化樹完整許多，建議開發者當作地圖：

| 元素 | 角色 | 重點 |
|---|---|---|
| `CATA` | 目錄頂層 | 屬性 `DESC`、`PURP`（要與使用它的等級相同，如 `PIPE`、`FITT`）、`CSTA` |
| `SECT`／`STSEC` | 節，**必備** | 管路節與結構節 |
| `CATE`／`STCA` | 類別，選用但建議 | `PURP` 要與等級中的 `STYPE` 一致（如 `VALV` 的 `GLOB`、`GATE`）；另有 `SKEY`（ISO 圖符號鍵）、`PTRE`、`GMRE`、`DTRE`、`CDET` |
| `PTSET`／`GMSET`／`DTSET`／`DTEX`／`MTEX` | 節與類別皆可擁有 | 點集、3D 幾何集、資料集、細部文字、材料文字 |
| `PTSSET`／`NGMSET`／`GMSSET` | 僅結構節／類別 | 結構點集（P-line）、負 3D 幾何集（孔、端部處理）、2D 結構幾何集 |
| `COMP`（`SCOM`）、`PROF`（`SPRF`）、`JOIN`（`SJOI`）、`FITT`（`SFIT`） | 目錄元件 | 沒有成員元素；官方建議一個節只放一種元素，不同種類放不同類別（例如全部管件點集放一節、幾何集放另一節） |
| `TEXT` | 通用文字 | `STEX` 最長 120 字元，可出現在 `UNIT`、`CATA`、`SECT`、`CATE`、`SPEC` 等多處；與 `DTEX` 的 `STEX` 無關 |

所有等級會引用的元素，都必須存在於某個 `CATA` 階層內；目錄通常先以「目錄巨集」建成程式庫，專案再挑選組成。

### 26.3.2 六種參數

參數定義元件的尺寸與特性，用來設定 Pointset、Geomset 與 Dataset 的屬性。第 25 章講了三種，官方實際有更細的分類：

| 參數 | 縮寫 | 存放與用途 |
|---|---|---|
| 元件參數 | `PARAM`（`PARA`） | 目錄元件上，可為數值、運算式或字詞；全部四類元件可用 |
| 保溫參數 | `IPARAM` | 主元件從保溫元件的 `PARAM` 取尺寸；未保溫時為 0 |
| 附屬參數 | `APARAM` | 接頭與管件從「所連接的斷面」取 `PARAM`（對 Profile 無意義） |
| 擁有參數 | `OPARAM` | 次要接頭與附件從「擁有它的斷面」取 `PARAM` |
| 設計參數 | `DES PARAM` | 設計元件有 10 個值的設計參數陣列；任何有 `SPREF` 的元件都能用 |
| 設計附屬／擁有參數 | `DES APARAM`、`DES OPARAM` | 取自附屬或擁有斷面的設計元素 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕參數與元件適用表：Piping Component、Profile、Primary Joint、Secondary Joint、Fitting 可使用的參數種類

*圖 26-4　參數適用表：元件參數與保溫參數、設計參數五類元件皆可用；附屬參數只給接頭；擁有參數給次要接頭與附件。（AVEVA 官方文件截圖，僅供內部教學）*

必須記住的規則：

1. 目錄元件除 `PARAM` 外的屬性，必須是實際值（字詞或元素參照），不能用參數定義。
2. 表示式中的參數可帶單位限定詞（例如 `PARAM 5 90degrees 10inch` 會以 5、90、254 存入並記錄其物理量為 NONE、DIST、ANGL）；量綱不合的運算（距離加角度）會產生警告或錯誤。
3. 求值幾何時，**目前的工作單位全部暫停，一律以資料庫單位計算**（距離為 mm）；`+3` 就是 3 mm，要 3 英吋必須加 `inch` 限定詞。
4. 預設與樣本值用 `MODEL SETTINGS PARAM 1 10`、`MODEL SETTINGS IPARAM 3 25`、`MODEL SETTINGS APARAM 2 300`、`MODEL SETTINGS DES PARAM 7 9.5` 設定，**只在目前 PARAGON 工作階段有效，不寫入資料庫**；`MODEL SETTINGS DEFAULT` 會清除全部預設與樣本值。

官方的參數化範例：滑套法蘭用 5 個參數，縮徑三通用 12 個，Universal Beam 用 4 個，角鋼接頭用 3 個元件參數加 2 個附屬參數。

### 26.3.3 點集、幾何集與 P-point

**3D Pointset（`PTSET`）** 內可放三種 P-point，編號用 `NUMB`：

| 型別 | 位置定義 | 方向定義 | 共通可選屬性（僅管路元件） |
|---|---|---|---|
| `PTAXI` 軸向 | 沿某軸 `PAXI` 的距離 `PDIS` | 由軸決定 | `PCON` 連接型式、`PBOR` 口徑、`PSKEY` |
| `PTCAR` 笛卡兒 | 座標 `PX`、`PY`、`PZ` | `PTCDIR`（如 `X45Y`） | 同上 |
| `PTMIX` 混合 | 座標 | 軸向 `PAXI` | 同上 |

`PCON` 與 `PBOR` 對接頭與附件沒有意義。沒定義距離、座標、口徑或編號時一律當作 0；沒定義方向則預設 `DIR Y`。官方的縮徑三通範例用三個 `PTAX`：`P1` 沿 -Y，距離 `PARA[5]`，連接 `PARA[7]`，口徑 `PARA[1]`；`P2` 沿 +Y；`P3` 沿 X，距離 `PARA[6]`，連接 `PARA[8]`，口徑 `PARA[3]`。

`PSKEY` 可設 `BW`、`CP`、`FL`、`SC`、`SW`、`PL` 替 Isodraft 疊加端部符號（疊加在 `SKEY` 標準符號之上，預設 NULL）。

**結構 Pointset（`PTSSET`）** 內是 P-line，屬性有 `PKEY`（如 `TOS` 頂面、`BOS` 底面、`NA`／`NAXI`／`ZAXI` 中性軸）、`PLAXI`、`PX`、`PY`、`CLFLA`、`TUFLA`。**務必設定 `NAREF`（中性軸參照）**；沒設時 Design 會依序找第一個 `PKEY` 為 `NA`、`NAXI`、`ZAXI` 的 P-line，都沒有就假設中性軸在元件原點、沿 +Y。

**3D Geomset（`GMSET`）** 是一組 3D 基本體，同時決定「畫什麼」與「碰撞幾何」。每個基本體必須設 `OBST`；要顯示的還要設 `LEVEL`、`TUFLA`、`CLFLA`。基本體有 `SBOX`、`BOXI`、`SCON`、`LCYL`、`SCYL`、`SSLC`、`SDIS`、`SDSH`、`LINE`、`LPYR`、`SCTO`、`SRTO`、`LSNO`、`SSPH`、`TUBE`、`SEXT`、`SREV` 等；負基本體放在 `NGMSET`。**Design 的碰撞檢查只考慮 Geomset 中 `OBST` 為 1 或 2 的前 20 個基本體。**

### 26.3.4 顯示與碰撞：LEVEL、TUFLA、CLFLA、OBST

| 屬性 | 意義 |
|---|---|
| `LEVEL` | 一對整數，繪圖層級範圍；PARAGON 目前 `LEVEL` 在範圍內才會被考慮繪製 |
| `TUFLA` | 管（雙線）表示是否畫（預設 FALSE） |
| `CLFLA` | 中心線（單線）表示是否畫（預設 FALSE） |
| `OBST` | 0 無、1 軟（虛線）、2 硬（實線）；與 TUBE／CL 獨立運作 |

`REPRESENTATION` 指令用來覆蓋顯示而不改屬性，預設為 `CL ON`、`TUBE OFF`、`OBSTRUCTIONS OFF`、`LEVEL 0`、`PPOINTS ON LENGTH 50 NUMBERS OFF`、`PLINES ON PKEYS OFF`，`REPRESENTATION DEFAULT` 可復原。多個設定請寫在同一行，元件才只重繪一次。

結構元件的 `Tubeflag` 必須為 TRUE 才會可見；`SPRF` 通常建三套幾何：Simplified（`LEVEL` 0–4、`OBST` 0）、Actual（5–8、`OBST` 2）、Obstruction（9–10、`OBST` 1）。

### 26.3.5 Dataset：目錄裡給設計與出圖查詢的資料

`DTSET` 底下是 `DATA` 元素，用來存放「必須能從 Design 或 Draft 直接查詢、卻無處可放」的目錄資料。重要屬性：

| 屬性 | 意義 |
|---|---|
| `DKEY` | 資料鍵，以 `Q PROP dkey` 查詢 |
| `PTYP` | 性質型別（`REAL`、`DIST`、`BORE`、`WORD`、`TEXT` 或複合單位如 `1kg/m3/degC`）；量綱不合時會警告 |
| `DTIT`、`PPRO`、`DPRO` | 標題、性質運算式、預設值（運算式算不出時使用） |
| `PURP`、`NUMB`、`PUNI`、`RUSE` | 用途（`PARA`、`DESP`、`DATA`）、編號、單位、可否當 `RPROP` 使用（需預先求值） |

官方範例：`DKEY` 為 `DEPT`、`PPRO` 為 `(PARAM [1])`、`DPRO` 為 600，則 Design 下 `Q PROP DEPT` 回傳梁深（算不出時回傳 600）。Pointset／Geomset 屬性也可寫成 `PBORE ( RPROP DBOR )`，此類元素的 `RFLG` 為 1，加入模型時需預先求值。

### 26.3.6 Part World 與 Selection Table（新式選用）

12.1 另提供不經等級的新機制：`GPART`（元件零件）在 Part World（`PRTWLD`）之下，可在一處完整定義元件，具有與 `SPCO` 相同的標準屬性（`CATREF`、`DETREF`、`MATXT`、`CMPREF`、`BLTREF`），另有 `TMPREF`（3D Template）、`DRSSREF`（2D 符號）、`SRFTREF`（表面處理），並可加任意 UDA。`PRTELE` 可建任意層數的分組。Parts 可放進 **Selection Tables** 供各專業（管路除外）在設計中選用；管路則可像 `SPCO` 一樣把 Parts 加進管路等級。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Selection Table 階層：SPWL 之下依序為 TABGRO、CTABLE，CTABLE 下有 TABITE 與 TABHEA、TABQUE 與 TABHQU

*圖 26-5　Selection Table 階層：Table Group 收納相關選取表；每張 Selection Table 有一個 Table Header（定義選擇問題）與多個 Table Item（指向 Part、存放答案）。（AVEVA 官方文件截圖，僅供內部教學）*

選取方式可依設計情境的準則（如船長室或船員室、船體內外）、屬性過濾或兩者合用。Utilities 的 **Convert Spec** 可把舊式等級轉成 `GPART` 家族（管路）或 `TABGRO > CTABLE > TABITE`（非管路）。

### 26.3.7 其他表格與單位

| 項目 | 要點 |
|---|---|
| 連接相容表 `CCTA` > `COCO` | 連接兩個管路元件時，先比對第一個的 leave `PCON` 與第二個的 arrive `PCON` 是否為相容對；不符再比兩者的 leave，符合就把第二個「翻轉」；都不符則報 incompatible connection type 並維持原位 |
| 螺栓表 `BLTAB` | 專供 Isodraft；`SBOL` 的 `NSTD` 指向非標準長度陣列 |
| 口徑與分支／縮徑表 `TABWLD` | `NOMTAB`、`BRTAB`（`PURP` 為 `BRAN`、`REDU`、`PTAP`）、`WTHTAB`、`PDATAB`，建等級用 |
| 單位 `UNIT` | `BUNI`、`DUNI` 可設 MM、INCH、MIL、FINC；模組以第一個 `CATA` DB 的第一個 `UNIT` 初始化 |
| 自訂標稱尺寸 `NBRWLD` | `PURP` 為 `BORE`、`BDIA`、`BLEN`、`ROD`；存在時改用自訂口徑 |

連接型式碼有 Isodraft 的命名限制：法蘭的 `PCON` 首字母必須是 `F` 或 `L`（鬆套法蘭），墊片 `G`，夾式（wafer）`W`；官方範例有 `FGD`（300 磅突面法蘭）、`GGD`、`BWD`（對焊）、`SWF`（承插焊）。**連接相容表是專案最早要做的工作之一**，不同壓力等級的法蘭與墊片要用不同型式碼，接錯才會警告。

> **專業提醒：** Isodraft 圖上的項目代碼取自元件 `SPREF` 的第二段（等級中的名稱），螺栓長度取自 `SBOL` 名稱，細部取自 `DTEX` 的 `RTEX`，材料取自 `MTEX` 的 `XTEX`。命名因此是**跨資料庫的外鍵**。需區分的相同項目可加後綴（預設分隔字元為冒號，`/TEE.FS:AA` 與 `/TEE.FS:AB` 視為同一項目碼）。

### 26.3.8 用 PARAGON 建目錄：指令與表單

指令方式：`NEW CATA`、`NEW SECT`、`NEW STSEC`、`NEW CATEG`、`NEW STCAT`；元件以 `NEW SCOM` 建立再設屬性：

```
NEW SCOM
GTYPE ELBO
PTREF /PSE1
GMREF /GSE1
PARAM 20 19.1 12.7 37.1 BWD
```

注意：一次下 `PARAM` 並給四個值，會設好前四個並**刪除其餘參數**；`PARAM[n]` 只能改已存在的參數。管路元件 `GTYPE` 必須是官方列表中的值（`ELBO`、`TEE`、`VALV`、`FLAN`、`GASK`、`REDU`、`TUBE`、`NOZZ`、`ATTA`、`BEND` 等），否則含該元件的 Branch 做資料一致性檢查會出錯；結構元件的 `GTYPE` 可為任意字詞，建議 `BEAM`、`COLU`、`BRAC`。圖形介面方式見圖 26-6（Create 選單依序建 Catalogue、Section、Category，另有 Profile、Joint、Fitting、Templates 專用類別表單）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Category 表單：左側為 Model References 與 Parameter Definitions，右側為模型預覽，下方為類別屬性表格

*圖 26-6　PARAGON 的類別建立表單：上方顯示目錄元件的 Points、Geometry、Data、Bolting 參照與參數定義，下方表格逐列維護各元件的 Name、Gtype 與參數值。（AVEVA 官方文件截圖，僅供內部教學）*

## 26.4 等級構築：Specification Constructor（SPECON）

### 26.4.1 表格式等級的讀法

官方的比喻：一份 `SPEC` 等同工程規範，可含「某材質的所有元件」或「某壓力等級的所有管路元件」，以表格呈現，**每個標題欄位是一個 `SELEC`，每一列是一個 `SPCOM`**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕等級表格示意：上方為 MATREF、FLUREF、RATING、LINETYPE，下方為 HEADING、DEFAULTS 與各列 SPCOM

*圖 26-7　管路等級表格：先是整份等級的指標與設定，再是各元件型式的 Heading、Defaults 與答案列（每列一個 SPCOM，含 CATREF、DETAIL、MATXT、CMPREF、BLTREF）。（AVEVA 官方文件截圖，僅供內部教學）*

表格由三種資料組成，順序固定：Heading（問題列）必須在最上、Defaults 緊接在後、其餘是答案列。選用時系統沿 `SELEC` 做問答，**任何一組答案應對應到唯一一個 `SPCOM`**；第一個答案相符的 `SELE` 或 `SPCO` 被採用。

| 規則 | 說明 |
|---|---|
| 特殊字元 `*` | 代表目前等級名稱，如 `*/20GA` 全名為 `/RF300/20GA` |
| `+` | 「同上」 |
| `-` | 只能用在 Defaults 列，表示不適用；`TYPE`、`NAME` 欄必須是 `-` |
| `=` | 只在 Defaults 列，表示依列表順序取第一個 |
| 標題欄上限 | 最多 20 欄；**等級建好後欄數無法更改，標題要先想清楚** |
| 不可有預設值 | `NAME`、`TYPE` 與 `CATREF`、`DETAIL`、`MATXT` 等指標 |
| 單位字樣 | 字詞答案不可寫成 `MM`、`IN`、`FT`、`KG` 等單位字樣，否則被當成單位（`25` 後接 `FT` 會被讀成 25 英尺） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕設計資料庫、等級與目錄三者的實例：FLAN 元件的 SPREF 指向 SPEC 的一列，該列的 CATREF、DETAIL、MATXT、BLTREF 各指向目錄中的元素

*圖 26-8　一個法蘭的完整參照實例：設計端 `SPREF` 指向等級 `/RF300` 的 `/FLANWN300100`，該列的四個指標分別落到目錄的元件、細部文字、材料文字與螺栓表；連接型式則受 `CCTA` 約束。（AVEVA 官方文件截圖，僅供內部教學）*

### 26.4.2 常用的選擇問題（Selectors）

| 適用 | 問題 | 說明 |
|---|---|---|
| 管路 | `PBORE n`、`PCONN n` | 第 n 個 P-point 的口徑與連接；多通元件可有 `PBORE1`、`PBORE2` 等 |
| 管路 | `STYPE` | 通用型式下的子型式，如 `VALV` 的 `GATE`、`GLOB`、`CHEC` |
| 管路 | `ANGle`、`RADIus` | 當 Pointset 使用 `DDANGL`、`DDRADI` 時，答案可為單值或範圍（如 `45.0,90.0`） |
| 管路 | `TEMperature`、`PRessure`、`RATing`、`SHOP` | 操作條件、壓力等級；`SHOP` 為 TRUE 表工廠預製，FALSE 為現場組裝 |
| 結構 | `DEPth`、`WIDth`、`WEIGht`、`DIMEn n`、`CTYPE n`（`CTYS`、`CTYE`、`CTYA`、`CTYO`）、`INERtia n`、`THICkness n`、`FIXty`、`AREA`、`GRADe` | 型鋼斷面屬性與連接型式（`RIVET`、`BOLT`、`WELD`、`GLUE`） |
| 自訂 | 任意最多四字母的字詞 | 例如替縮徑管加 `COL1`、`COL2` 顏色問題，選用時以 `WITH COL1 RED` 指定，省略則用預設答案 |

**P-point Zero（`PBORE0`／`PCONN0`）：** 一般 `PBORE1` 對應 arrive 口徑，但法蘭被翻轉後 `P2` 變成 arrive，以 `PBORE1` 就比對不到。使用 `PBORE0` 時，會依編號順序用新元件的所有 P-point 去比對前一元件的 leave，只要 `P1` 或 `P2` 相符就選中。

等級層級的設定：`MATREF`（指向 Properties DB 的 `SOLID`）、`FLUREF`（`FLUID`）、`RATING`（壓力等級，Isodraft 用來判斷管線壓力等級變化點，預設 0）、`LINETYPE`（`FP` 固定管、`FX` 固定長度，影響材料表是否附加長度，預設 `NUL`）。每列 `SPCOM` 的指標：`CATREF`（**唯一必填**，且被指向的元件必須先存在，否則出現 `Undefined Name`、`CATREF` 顯示 `=0`）、`DETAIL`、`MATXT`、`BLTREF`（僅需螺栓的元件）、`CMPREF`。

### 26.4.3 保溫等級

保溫不是由設計者「選用」，而是 Design 等模組在需要時**自動查詢**保溫等級，因此格式必須嚴格。通常以 `TEMP`（溫度範圍，如 `101,200`）與 `PBOR0`（口徑範圍）兩個問題決定厚度；由於範圍可能重疊，**標題中 `TEMP` 必須排在 `PBOR0` 之前**。範例的 `INSU` 型式列：`TEMP` 0,100、`PBOR0` 1,8、`CATREF` `/IC1`。

### 26.4.4 SPECON 的操作

在 PARAGON 命令列輸入 `SPECONMODE` 進入。主要指令：

| 目的 | 指令 | 備註 |
|---|---|---|
| 建立 | `NEW SPEC /RF300` | 簡寫 `NEW /RF300`；`TEXT '...'` 設描述（不超過 50 字元） |
| 開啟 | `OLD SPEC /RF300` 或直接輸入名稱 | |
| 輸入表格 | `HEADING`（換行後接欄位）、`DEFAULTS`（換行）、答案列 | 輸入時是 `TYPE NAME ...`，**修改與輸出時順序變成 `NAME TYPE ...`** |
| 使用者自訂屬性 | `EXTRA :colour 'green'` | UDA 必須先在 Lexicon 定義並以 `SPCOM` 為合法元件 |
| 註解 | `COMMENT text` | 解讀時忽略，輸出與重讀時保留 |
| 複製 | `COPY /SPEC1 RENAME /SPEC1 /SPEC2` | 先 `NEW SPEC /SPEC2`；`SPCOM` 名稱的舊前綴換新前綴 |
| 輸出 | `OUTput /RF300`、`OUTput NEW VALV FLAN /RF300` | `FILE` 先指定檔案；`OUTput NEW` 的格式可重新輸入；`BORES ACTual／NOMinal` 控制口徑輸出（預設標稱） |

巨集輸入是最有效率的做法：把等級輸出成文字檔（`OUTPUT NEW`），用文字編輯器大幅修改後重新載入。除 `NAME` 與 `TYPE` 外，`SPCOM` 的任何部分都能這樣改，因為改了 `NAME` 或 `TYPE` 系統就找不到要覆蓋的列。

**刪除與移除的差別（重要）：**

| 指令 | 效果 | 對既有設計的影響 |
|---|---|---|
| `DELETE spcom...`／`DELETE SPEC`／`DELETE ALL` | 從目錄資料庫完全消除；官方明說**不會檢查設計資料** | 設計中指向它的 `SPREF` 失效，之後存取（例如出圖）會出錯 |
| `REMove spcom...`／`REMove ALL` | 除了 `CATREF` 與 `DETAIL` 外清除答案，移轉到封存等級 `/*LIMBOSPEC` | `SPREF` 在原等級找不到時會自動到 `/*LIMBOSPEC` 找，既有設計仍有效，但新設計無法選用 |

被移除的項目可用修改 `SPCOM` 的語法重新帶入（含其名稱），會自動移回原等級。多個目錄 DB 時每個 DB 各有一個封存等級（`/*LIMBOSPEC`、`/*LIMBOSPEC_1`...）。GUI 對應的是 Specification 表單上的 Remove to Limbo、Delete Permanently 與 Add From Limbo。

### 26.4.5 用 GUI 建等級

Create > Specification > Specification 建立等級後，會開啟「任務」式的 Specification 表單；它主要為管路等級設計，其他專業另有表單。流程如下：

> 〔公開版未收錄：AVEVA 官方產品截圖〕PARAGON 的 Specification 表單：上方 Headings 下拉與格線，下方 Tasks 分為 Specification、Tables、Headings、Items 四欄連結

*圖 26-9　Specification 表單的 Tasks 區：Edit Spec Atts／Edit CAD Atts／Update Atts／Rename Spec／Export，三種尺寸表（Size Range、Branch、Reducer、Tapping），Add／Edit Heading，以及 Add New Items、Add From Limbo、Edit Answers 等項目任務。（AVEVA 官方文件截圖，僅供內部教學）*

1. 建 Spec World（`SPWL`）與 Specification（`SPEC`）。
2. Edit Spec Atts（描述、Spec Type：Piping、Insulation、Tracing、Bolting）與 Edit CAD Atts（綁定 Nominal Bore／Tapping 表，也可設材料、流體與螺栓參照）。
3. Add Heading：加入問題欄位，每個問題建立一個 `SELEC`；可用 Standard Headings（維護於 `PDMSUI>cats>dflts` 的 `standard-headings` 檔）。
4. Add New Items：指定 Size Range、`STYPE`、Heading Type（GTYPE），從 Category 或 Part Family 抓零件。
5. Edit Answers、Edit Ref/Attributes、Edit Extra UDAs；若等級元件所引用的 Part 屬性事後被改，要用 Update Atts 同步。
6. Rename Spec、Export（輸出檔供巨集日後匯入）。

## 26.5 Design Templates：參數化設計樣板

### 26.5.1 概念與定位

設計樣板是一組設計基本體、拼板與管嘴的組合，可被其他設計資料庫的部分當成單一項目參照。它的行為像目錄元件，差別在：

| 比較 | 目錄元件 | 設計樣板（`TMPL`） |
|---|---|---|
| 存放位置 | Catalogue DB | Design DB 專用區域（`TPWL` > `TMAR` > `TMPL`） |
| 可否拆解 | 否 | 可拆成組成部分，供報表、標註、MTO 等 |
| 選用後留在設計 DB | 只存 `SPRE` 指標 | **整份樣板被複製**進設計階層，可局部修改 |
| 可被誰參照 | — | Equipment、Sub-Equipment、Panel Fitting、Section Fitting、Primary Joint |

官方以兩個教學範例貫穿：簡單的踢腳板（kickplate，繞著拼板開孔）與進階的臥式儲槽（可選兩端封頭與支座）。

### 26.5.2 建立流程（以踢腳板為例）

先規劃：樣板要先想好哪些尺寸要參數化，就像建目錄元件前先畫草圖。踢腳板有 5 個性質：總長、總寬、高度、壁厚、拼板厚度。

> 〔公開版未收錄：AVEVA 官方產品截圖〕踢腳板範例：正方塊為外殼，第一個負方塊挖空，第二個負方塊貫穿拼板；標示總長、總寬、總高、壁厚與拼板厚度

*圖 26-10　踢腳板樣板的幾何與尺寸：實線為正方塊（外殼）、虛線為第一個負方塊（挖空內部，只留壁厚）、點線為第二個負方塊（貫穿所設置的拼板）。（AVEVA 官方文件截圖，僅供內部教學）*

| 步驟 | 動作 | 要點 |
|---|---|---|
| 1 | 在 Equipment 應用程式建 SITE、ZONE、`EQUI`，其下建 `BOX` 與其下的 `NBOX` | 樣板以現有設計元素為基礎 |
| 2 | 切到 Design Templates 應用程式，Create > Template World、Template Area | Template World 建在 WORLD 之下，與目前層級無關；Template Browser 顯示的是 Description，Design Explorer 顯示的是 Name |
| 3 | 瀏覽到 `EQUI`，Create > Template：填 Name、Purpose、Description、Function、Generic Type（如 `PENH`） | 勾選 Add Properties 與 Add Points 會建好空的 `DDSE` 與 Pointset |
| 4 | 定原點：Pick Type 設 Ppoint、Pick Method 設 Snap，在 3D View 選 P-point | **原點一旦在參數化後再改，已設的規則會失效** |
| 5 | 在 `TMPL` 之下加第二個 `NBOX` | 要切穿拼板的負幾何必須由 `TMPL` 直接擁有，不能放在正方塊之下 |
| 6 | Modify > Property Definitions 定義屬性 | 見 26.5.3 |
| 7 | Modify > Parameterization 寫規則 | 見 26.5.4 |
| 8 | 在 PARAGON 的等級中加 `SPCO`，設 `TMPREF` | 見 26.5.5 |

建立樣板時有兩個選項：*Maintain world orientation*（以世界座標決定元素方向）與 *Ignore elements that cannot be in Templates*（含 `SUBE` 的設備預設不能做樣板，勾選後階層被壓平）。**不可把含 `TMPL` 的元素複製進新樣板。**

> 〔公開版未收錄：AVEVA 官方產品截圖〕樣板階層：左側設計階層 SITE、ZONE、EQUI、BOX、NBOX，複製到右側 TPWL、TMAR、TMPL、BOX、NBOX

*圖 26-11　樣板階層：樣板放在 WORLD 之下專用的 `TPWL`（Template World）與 `TMAR`（Template Area）內；建立樣板就是把設計幾何複製到 `TMPL` 之下。（AVEVA 官方文件截圖，僅供內部教學）*

### 26.5.3 性質（Properties）與資料集

每個性質存在 `DDAT`（Design Data）元素，由 `DDSE`（Design Dataset）擁有，`DDSE` 又由 `TMPL` 擁有。性質的「Definition」決定值怎麼來：

| Definition | 值的來源 |
|---|---|
| Design Parameter | 實例化時設計者輸入的設計資料（編號 1–10） |
| Attribute | 具名屬性（Short Key 設成屬性名） |
| Expression | 運算式求值，例如 `HEIG of PLOO 1 of PANEL`（拼板厚度） |
| Plotfile | 要顯示的 plot 檔（位於 `PDMSPLOTS` 環境變數指定的目錄下，加入時會檢查路徑與檔名） |
| Specification Ref | 可設定 SpecRef（例如 Profile） |
| Sub Element Ref | 實例化時設定指向子元素（如 Sub-Equipment）的指標 |

每個性質有 Key（如 `LENG`、`WIDT`、`HEIG`、`WTHK`、`PTHK`）、Data Type（Distance 等）、Default（外部值取不到時使用）與限制：

| 限制 | 儲存 | 效果 |
|---|---|---|
| Range | `DDAT` 的 `MinMax` | 僅接受範圍內的值 |
| Values | `DDAT` 擁有的 `VVALUE` 元素的 `ValidV` | 僅能從清單選；清單要含預設值，否則設計者改了就難以重設 |

切換成 Range 會自動清掉 Values 資料，避免誤設。`PTHK` 這類來自外部元素（擁有它的拼板）的值，**必須定義成帶預設值的性質，不可在規則中直接引用外部值**，因為樣板世界裡並不存在那個擁有者，規則會在定義時求值失敗。

### 26.5.4 規則與存取方式

規則是「屬性運算式」，結果型別必須符合屬性。Template Member Parameters 表單列出成員，選一個屬性（X length、Y length、Position、Orientation...）即可設規則；未設規則的屬性（如 Orientation）表示每次實例化都由設計者決定。

| 偽屬性 | 從哪裡查 | 說明 |
|---|---|---|
| `PROP key` | 從 `PFIT` 等擁有層 | 往下經 `TMPL` 與 `DDSE` 找性質，例如 `Q PROP LENG`；Query > Template Properties 列出全部 |
| `CDPR key` | 從樣板內的元素（如 `BOX`） | 往上找擁有的 `TMPL`，再往下經其 `DDSE`；規則中最常用，如 `CDPR LENG` |

官方列出的完整偽屬性表（依資料集類型）：

| 內容 | 現行（Current） | 本地（Local） | 樣板（Template） |
|---|---|---|---|
| 性質鍵清單 | `CDPL` | `DEPL` | `PRLS` |
| 實數值 | `CDPR` | `LDPR` | `TDPR` |
| 文字或實數 | `TCDP` | `DEPR` | `PROP` |
| 預設值 | `TCDD` | `DEPD` | `PRDE` |
| 參照 | `CFDP` | `LFDP` | `TFDP` |

此外 `RPRO` 可取目錄參數。`DDAT` 的 `DKEY` 存鍵、`DDPR` 存性質運算式、`DDDF` 存預設值。三種資料集的位置：**本地**資料集由目前元素直接擁有，**樣板**資料集由目前元素之下第一個樣板擁有，**現行**資料集與目前元素同層、同一擁有者。

踢腳板的規則範例：`X length = CDPR LENG`、`Y length = CDPR WIDT`、`Z length = CDPR HEIG`、`Position = U (CDPR HEIG / 2)`（運算子前後要有空白）；內層負方塊 `X = CDPR LENG - 2 * CDPR WTHK`，`Y` 同理；第二個負方塊高度 `CDPR PTHK`、位置向下移其高度一半。**Copy Rules／Paste Rules** 可把規則複製到另一成員，只覆蓋對應屬性。

### 26.5.5 選用樣板：從等級掛上去

設計者並不知道自己選的是樣板還是目錄元件。機制是：`SPCO` 除 `CATREF` 外還有 **`TMPREF`**（Template Reference）可指向 `TMPL`；選取時系統把樣板實例複製到設計階層。

> 〔公開版未收錄：AVEVA 官方產品截圖〕設計 DB 中 PFIT 的 SPREF 指向目錄 DB 的 SPEC／SELE／SPCO，SPCO 的 TMPREF 再指向 TPWL／TMAR／TMPL

*圖 26-12　樣板的選用路徑：拼板附件 `PFIT` 的 `SPREF` 指到等級的 `SPCO`，`SPCO` 的 `TMPREF` 指到 `TMPL`，於是樣板被複製到 `PFIT` 之下。（AVEVA 官方文件截圖，僅供內部教學）*

官方的設定步驟（PARAGON 的 GUI 沒有修改等級的功能，要開 Display > Command Window 下指令）：瀏覽到目標 `SELE`，下

```
NEW SPCO /TMPL/SAMPLE/KICKPLATE
TMPREF /Kickplate-1
```

然後 `Q ATTRIBUTES` 確認 `Catref` 為 `Nulref`（`=0/0`）、`Tmpref` 為樣板名稱，存檔離開。對照一般 `SPCO`：`Catref` 指向元件、`Tmpref` 為 `Nulref`。

### 26.5.6 進階：子零件、有效值規則與設計點

臥式儲槽範例把設計拆成主體（`EQUI` 內正圓柱加負圓柱）、兩端封頭與支座（各為 `SUBE` 的子樣板）：

> 〔公開版未收錄：AVEVA 官方產品截圖〕臥式儲槽：主體 EQUI、左側錐形封頭 SUBE、右側碟形封頭 SUBE、兩個支座 SUBE，標示 LENG、DIAM、CHEI 與原點

*圖 26-13　儲槽樣板：主體由 `LENG`、`DIAM`、`CHEI`、`THKN` 等設計參數控制；封頭與支座是以等級選用的子設備樣板。（AVEVA 官方文件截圖，僅供內部教學）*

| 技術 | 做法 |
|---|---|
| 設計點 | `DPSE` 內可建笛卡兒點（`DPCA`）、圓柱面點（`DPCY`）、球面點（`DPSP`），像 p-point 有位置與方向；如 `AT PP1 of LNID /Main-Body` |
| 本地名稱 | 實例中的元素名稱不會被複製（Design DB 名稱不可重複），只能靠 `NBOX 1 of TMPL 1 of PFIT` 的序位辨識。**本地名稱**（最多 20 字元、每樣板最多 500 個）存於定義中並複製到每個實例；規則以 `LNID /name` 或 `MLNID /name` 引用 |
| 求值順序 | 預設由上往下；A 相對於 B 定位時要讓 B 先求值，以 Modify > Order Local Names 排序 |
| 子設備指標 | 性質設為 Sub Element Ref，Values 放指向等級 `SPCO` 的名稱；每個 `VVALUE` 可附位置與方向規則（存於 `ATTRRL` 的 `AttRule`），如 `AT LNID /Datum-Point-2 of TMPL 1 of EQUIP`、`Y is S and Z is U` |
| 標註 | Create > Dimension Points 建成對的球面設計點，Control > AutoBuild 為每個設計參數自動建一對，以 `CDPR` 運算式定位才會隨尺寸縮放 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕儲槽樣板的資料結構：EQUIP 下有 TMPL（含 DDSE、DDAT）與兩個 SUBE；DDAT 的 VVALUE 指向 SPCO，SPCO 的 TMPR 指向端部樣板

*圖 26-14　有效值如何選出子樣板：`DDAT` 下的 `VVALUE` 存 `SPCO` 的參照；子設備 `SUBE` 以 `SPRE` 指向該 `SPCO`，`SPCO` 的 `TMPR`（TMPREF）再指到端部樣板。（AVEVA 官方文件截圖，僅供內部教學）*

官方特別提醒：設計樣板工作區看不到完整的儲槽，因為子設備規則要到實例化時才執行，所以規則必須非常仔細。

### 26.5.7 測試、變更傳播與搜尋

**測試：** 唯一能測整體效果的方式是把樣板放進等級（可用專門的測試等級）、再到設計模組建立實例，逐一變更每個主要性質。釋出前必做。

**變更傳播：** 樣板修改後，既有實例不會自動更新。Utilities > Propagate Changes 列出所有連結實例，狀態為 Suspect 表示主樣板在同一或之後的工作階段被改過。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Propagate Changes 表單：列出 ADV/VESS004 的所有連結實例與其狀態 Suspect，下方有 Show All、Select All、Display、Print、Update 等按鈕

*圖 26-15　樣板變更傳播：選取要更新的實例後按 Update，成功與失敗會顯示於 State 欄（Updated 或 Failed），失敗原因在 Message 欄。（AVEVA 官方文件截圖，僅供內部教學）*

限制：實例須能完全修改（被 claim 或受 Data Access Control 限制則失敗）；被更新的實例會被替換，**與其連結的標註與標籤不再連到元素**；主樣板的參數個數不能改（已變就須刪除重建實例）；更新後立刻 Undo 可還原。單一實例可用 Equipment 的 Modify > Update from Template，狀態為 up to date、Update（樣板較新）或 Suspect（同一工作階段，無法判斷先後）。

**搜尋與進階：** Query > Template Search 可依名稱（區分大小寫）、描述、Generic Type 搜尋；重複元素（Repeat Rule）有 Cartesian、Linear、Radial 三種型式，重複次數以運算式提供（正整數）。

### 26.5.8 官方給樣板設計者的建議

官方的建議：先畫草圖定好性質與預設值；原點與方向一開始就定對；外部值一律定義成帶預設值的性質；規則中的常數一定寫單位（`RPROP` 取出的目錄值永遠是 mm）；負基本體由樣板直接擁有；釋出前一定在設計中實測。

> **常見錯誤：** 在規則裡直接寫「擁有者元素的屬性」（例如 `HEIG of PLOO 1 of PANEL`）卻沒包成性質。樣板區裡沒有那塊拼板，規則在定義時就會失敗。正確做法是 26.5.3 的 `PTHK`：性質用該運算式、再給預設值，規則只引用 `CDPR PTHK`。

## 26.6 Properties Constructor（PROPCON）：目錄的「物理性質」夥伴

Properties DB（類型 `PROP`）在 Admin 以 `CReate DB teamname/dbname PROP` 建立，須加入 MDB 才能使用，通常指派給管路應力分析團隊。它存放應力分析與安全稽核需要的資料，也提供結構應用程式計算重量與重心用的材料密度。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Properties DB 階層：WORLD 之下有 GPWL、CASH、RUNW、MATW、CMPW、CONW 六個分支

*圖 26-16　Properties 資料庫階層：材料（`MATW`）、案例（`CASH`）、元件（`CMPW`）、約束（`CONW`）、執行（`RUNW`）與群組（`GPWL`）。（AVEVA 官方文件截圖，僅供內部教學）*

| 分支 | 內容 | 與目錄、設計的連結 |
|---|---|---|
| `MATW` | 固體與流體性質（密度、Poisson 比、膨脹係數、Young 模數、容許應力），以表加點存成隨溫度與壓力變化的表格 | `SPCOM` 的 `MATR`、`FLUR`；設計端 `PIPE`、`BRAN` 也有，**設計端有設定時優先** |
| `CASH` | 溫度、壓力等操作案例（`PTEM`、`IPRE`、`WPRE` 等） | `PIPE`／`BRAN` 的 `CASR` |
| `CMPW` > `CMPT` > `CMPD`／`TUBD` | 目錄沒有的物理資料：外徑、重量（`CWEI`，`TUBD` 為單位重 `UWEI`）、`SIF`、腐蝕裕量等；`CWEI` 等可用參數化運算式，讓各專業都能算重量與重心 | `SPCOM` 的 **`CMPR`（CMPREF）** |
| `CONW` | 約束：力、位移、柔度、摩擦係數等 | 設計端 `ATTA` 的 `CSTR` |
| `RUNW` | 應力分析軟體執行所需資料 | 依介接的軟體而定 |

群組（`GROU`）用來分組案例；**不要刪除群組內的案例，否則會真的從資料庫刪除，應用 `REMOVE`**。偽屬性 `PROPRE` 可在設計元素上查詢計算結果，例如 `Q PROPRE OUTD`。

## 26.7 元件特例與目錄一致性檢查

### 26.7.1 P-point 編號慣例（Isodraft 才認得）

| 元件 | 慣例 |
|---|---|
| 直管（`TUBE`） | 只有 `P1`，同時定義兩端的口徑與連接型式 |
| 管嘴 | 接 Branch 的連接 P-point 必須是 `P1` |
| 雙通 | arrive／leave 為 `P1`、`P2`（順序不拘）；雙通閥的閥桿方向用 `P3` |
| 三通 | 支線為 `P3`；三通閥閥桿用大於 `P3` 且口徑未設的 P-point |
| 四通 | 兩條直通為 `P1/P2` 與 `P3/P4`；閥桿用大於 `P4` 的 P-point |
| 偏心異徑管 | 無連接點時平面側用 `P3`；有連接點時 `P3` 設有效口徑，平面側用口徑未設的 `P9` |

### 26.7.2 隱含直管與斜接彎頭

| 特例 | 規則 |
|---|---|
| 隱含直管 | 只需一個 P-point、不需 Geomset；參數 1 = 標稱口徑、2 = 外徑、3 = 連接型式；要保溫時 `IPARAM 1` = 保溫厚度的兩倍 |
| 斜接彎頭 | 12.0 起，`GTYPE` 為 `BEND` 且 `GMREF` 未設時用內建幾何集；參數 1–3 同上，**4 = 預設切割數 `NCUTS`** |
| `NCUTS` | 參數 4 為正數：切割數固定、設計者無法改；0：視為彎製彎頭；**負數：由設計者指定切割數**；上限 25；設計端 `BEND` 的 `NCUTS` 預設為 0 |
| 偽屬性 | `ACTNCU`（實際切割數，0 表示不是斜接彎頭）；`ATLE`、`LTLE`、`TLE`、`FITLEN` 回傳最大切割長度；各段長度用 `BSCLL`、`BSMXL`、`BSMNL`、`BVSCLL` 等；動態 P-point 編號為 n×10 起（10 中心線、11 內側、12 外側） |

PARAGON 無法顯示具有隱含幾何集的元件，只能顯示點集位置。

### 26.7.3 CHECK：目錄資料一致性檢查

指令 `CHECK <gid>`，`<gid>` 可為 `SPEC`、`SELE`、`SPCO` 或 `COMP`。從等級開始會檢查所有經它參照的元件；從 `COMP` 開始只檢查該元件與其下元素。**目前只能檢查管路目錄，不能檢查結構目錄。**

| 層級 | 檢查項目 |
|---|---|
| `SPEC` | 問題不重複；必須有 `TYPE` 問題；`TYPE` 與 `COMP` 的 `GTYPE` 相同；`SDTE` 的 `SKEY` 正確；點集符合 Isodraft 的幾何要求 |
| `SPCO` | `CATREF`、`DETAIL`、`MATX`、`CMPR`、`BLTREF` 皆已設（`BLTREF` 僅在連接型式以 F 或 L 開頭時需要） |
| `COMP` | 有有效的 `PTREF`、`GMREF`；點集有 P-point 且編號不重複；幾何集有基本體且非退化、無無效 P-point 編號或參數；每個 P-point 連接型式存在於 COCO 表（建構用 P-point 可為 `0.0`、`NUL`、`NULL`）；口徑為標稱口徑（建構用或連接型式 `CLOS` 可為 0） |

可用 `TOLerance CATAlogue ...` 調整：`CMPRef`、`GMREf`、`BORE`、`ISOMetric`，`DEFault` 重置。預設不檢查任何 `CMPREF`、忽略 `ATTA`、`FLAN`、`TUBE`、`BOLT` 的 `GMREF`、檢查 6 mm 至 2150 mm 的標稱口徑、檢查所有 Isodraft 相關設定。注意：此檢查用目錄參數，**若基本體只由設計與保溫參數構成會產生假警告**。

主要錯誤代碼成對出現：`C30`–`C120` 為 `SPCO` 的 `DETA`、`MATX`、`CMPR`、`BLTR`、`CATR` 未設（偶數為未知參照）；`C130`–`C160` 為 `PTRE`、`GMRE`；`C170`–`C210` 為點集（重複編號、無 P-point、未知連接型式、`GTYPE` 與 `TYPE` 不符、非標準口徑）；`C220`–`C310` 為幾何集與 Isodraft 角度、共線；`C820`–`C840` 為 `SKEY`。

## 26.8 二次開發者怎麼接

官方的 Catalogs and Specifications 四冊是**使用與資料模型手冊，不含 PML 程式範例**，本節只整理文件明載、可在 PML 或命令列取用的屬性、偽屬性與指令；PML 寫法請參考[第 32 章](ch32_pml_language_zh-TW.reading.html)與[第 33 章](ch33_pml_database_zh-TW.reading.html)，並全部在訓練專案實測。

| 想做的事 | 文件載明的依據 | 提醒 |
|---|---|---|
| 查目錄計算性質 | `Q PROP dkey`、`Q RPROP dkey`、`Q PRDE dkey`、`Q PRLS` | `RPROP` 在 `PPRO` 是文字時回傳 `RPROP unset`；參數運算式以系統求值，單位為 mm |
| 查樣板性質 | `Q PROP key`、`CDPR`、`LDPR`、`TDPR`、`PRLS`、`CDPL` | 見 26.5.4 偽屬性表 |
| 判斷樣板或目錄元件 | `SPCO` 的 `TMPREF` 非 `Nulref`（`=0/0`）、`CATREF` 為 `Nulref` | 〔待核對〕PML 判斷參照為空的寫法 |
| 找出所有樣板 | `TMPL` 在 `TPWL > TMAR` 之下 | 〔待核對〕PML 遍歷寫法 |
| 檢查一致性 | `CHECK <gid>`、`TOLerance CATAlogue ...`、錯誤碼 | 〔待核對〕如何由 PML 擷取輸出 |
| 斜接彎頭、Properties | `ACTNCU`、`BSCLL`；`Q PROPRE OUTD` | |
| 輸出等級 | SPECON `OUTput NEW`、Specification 表單的 Export | 輸出檔即巨集輸入格式 |

**開發守則：** (1) 讀鋼構或吊架目錄前先確認符合 26.2 的慣例，否則寧可跳過並回報；(2) 讀等級時要同時處理 `/*LIMBOSPEC`，已移除的項目在既有設計中仍有效；(3) 工具永遠不要執行 `DELETE`，淘汰元件只能向管理員提出 `REMove` 需求；(4) 樣板實例是複製品，會與主樣板漂移（Suspect），傳播變更會讓連結標註失效；(5) 文件沒寫的 PML 取值方式一律先在訓練專案實測。

## 26.9 實務建置流程與檢查

### 26.9.1 新管路等級的建置順序

1. 設定 `UNIT`、連接相容表 `CCTA`（含 `CKEY`）、口徑表（官方建議為專案最早的工作）。
2. 建 `CATA`／`SECT`／`CATE`：點集、幾何集、資料集、`DTEX`、`MTEX`、螺栓表；一節一種元素。
3. 建元件 `SCOM`：`GTYPE`、`PTREF`、`GMREF`、`PARAM`；隱含直管與斜接彎頭遵守 26.7.2。
4. 建 `SPWL` 與 `SPEC`：先定標題與 Defaults（欄數不能改），再填答案列；保溫等級單獨建。
5. 執行 `CHECK`；如有 Properties DB，設 `CMPREF`、`MATR`、`FLUR`。
6. 在測試專案選用元件、出 ISO 圖、做碰撞檢查，通過後依第 25 章變更流程發佈。

管路設計見[第 19 章](ch19_pipework_zh-TW.reading.html)；結構目錄先確認 26.2.2 的 `Purpose` 與 `GTYPE`，並設好 `NAREF` 與三套幾何層級，設計應用見[第 21 章](ch21_structures_zh-TW.reading.html)；設備樣板與目錄見[第 18 章](ch18_hvac_equipment_zh-TW.reading.html)。

### 26.9.2 檢查清單

目錄：`Purpose`、`GTYPE`、`NAREF` 已設，一節一種元素。點集與幾何集：P-point 編號、連接型式、標稱口徑符合規定，每個基本體有 `OBST`。等級：每個 `SPCO` 有 `CATREF`，欄位不超過 20，一組答案對應唯一 `SPCOM`，淘汰用 `REMove`。樣板：原點方向正確、外部值皆為性質、單位已寫、已在設計中實測。

最常見的錯誤：慣例不符導致應用程式取不到資料；建 `SPCO` 時 `CATREF` 對象尚不存在（顯示 `=0`）；用 `PBORE1` 而非 `PBORE0`；以 `DELETE` 刪除已被設計使用的 `SPCOM`；樣板規則直接引用外部值或事後改原點。

## 26.10 本章小結

1. 「慣例」是標準應用程式運作的前提；目錄裡有一類資料是給應用程式讀的設定資料。
2. 目錄階層比第 25 章完整（加上 `CCTA`、`BLTAB`、`TABWLD`、`UNIT`、`PRTWLD`）；參數有六類，求值一律用資料庫單位。
3. 顯示與碰撞由 `LEVEL`、`TUFLA`、`CLFLA`、`OBST`、`REPRESENTATION` 決定；碰撞只看前 20 個 `OBST` 為 1 或 2 的基本體。
4. 等級是表格；每組答案唯一對應一個 `SPCOM`；`REMove` 保護既有設計，`DELETE` 會讓 `SPREF` 失效。
5. 設計樣板以性質（`DDAT`）與規則（`CDPR`）參數化，以 `SPCO` 的 `TMPREF` 掛到等級，選用時被複製進設計，變更需要傳播。
6. 二次開發者只讀、不改目錄；文件沒寫的取值方式一律實測。

## 26.11 練習題／自我檢核

**練習 26-1（訓練專案，只讀）：** 選一個鋼構目錄，列出 `CATA`、`STSEC`、`STCA` 的 `Purpose` 與 `GTYPE`，對照 26.2.2 是否符合慣例。

**練習 26-2：** 找出一份管路等級中閥門的 Heading、Defaults 與答案列，說明 `=` 與 `-` 出現在哪；用 `OUTput NEW` 輸出成檔，比較 `NAME`、`TYPE` 的順序。

**練習 26-3：** 在測試專案對小型等級執行 `CHECK`，把錯誤代碼分類成等級、點集、幾何集問題。

**練習 26-4：** 完成官方踢腳板範例（5 個性質、規則、`SPCO` 加 `TMPREF`），再從 Panels 應用程式建立 Panel Fitting 實測；然後修改壁厚預設值並執行 Propagate Changes，觀察連結標註。

**練習 26-5（思考題）：** 你要寫報表工具列出所有已被設計使用的 `SPCO`，請列出至少三個特殊情況（提示：`/*LIMBOSPEC`、`TMPREF`、`GPART`）。

**自我檢核：** 我能說出鋼構目錄、結構等級、吊架目錄的必設 `Purpose`；列出六類參數；說明 `DELETE` 與 `REMove` 的差別、`PBORE0` 為何能處理翻轉法蘭、`CDPR` 與 `PROP` 的查詢位置、外部值為何要定義成帶預設值的性質、樣板傳播的限制，以及二次開發中哪些取值有文件依據。

## 26.12 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 26 章](appx_d_verification_zh-TW.reading.html#ch26)；取材覆蓋與未讀範圍：見[附錄 E 第 26 章](appx_e_coverage_zh-TW.reading.html#ch26)。
