# 第 28 章　其他設計模組速覽：Design Reuse、Area Based ADP、Weld Planning 與 Factory Automation

> 前面幾章把船體、舾裝、圖面與管路講成主線。實際專案裡還有四個「不在主選單中央，卻常被問到」的功能：**把設計資料從一個專案搬到另一個專案的 Design Reuse、以區域與樣板批次出圖的 Area Based ADP、為組立計算焊接資訊的 Weld Planning，以及把設計資料交給切割機與焊接機器人的 Factory Automation。** 這一章用同一套框架（用途、核心概念、典型流程、操作要點、與其他章節的關係）逐一速覽，讓你知道它們存在、解決什麼問題、與你要開發的工具如何銜接。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的 *Design Reuse*、*Area Based ADP*、*Weld Planning*、*Factory Automation* 四個章節（已與中文機器翻譯對照；譯名生硬處改用台灣慣用詞）。官方文件是操作與設定手冊，指令（`MCEXP`、`MCIMP`）、設定檔名稱（`DRA-ABA-DEFAULTS`、`weldDefaults.def`）、輸入語法（`POSITION`、`LEGLENGTH`）與 TRI/2 實體欄位均有原文依據；凡文件沒寫的（例如各模組的 PML 物件、Vitesse 呼叫方式、實際安裝路徑）一律標〔待核對〕，不得當成事實。Factory Automation 一章在官方文件中多為「選項簡介」，細節分散於 Hull 的 Manufacturing 與 Setup 章節，本章只整理概覽。

## 28.1 學習目標

讀完本章，你應該能夠：

1. 說明 Design Reuse 的「匯出 → Transfer Set → 匯入」模式，以及 Transfer Set 存的是「資料定義」而非二進位資料。
2. 使用 Design Reuse 的 GUI 與 `MCEXP`／`MCIMP` 指令完成一次匯出與匯入，並知道匯入的前置條件與限制。
3. 說明 Name Changes（改名函式）如何讓資料適應目標專案的命名慣例。
4. 說明 Area Based ADP（ABA）的核心物件：Area、Template、Classification、Task、Tag Rule、Keyplan。
5. 區分 ABA 管理員與使用者各自的工作，並依步驟用 Process Drawings Control 批次產生圖面。
6. 說明 Weld Planning 的偵測、編輯、更新模型、報表與 Batch 流程，以及三個 `.def` 設定檔的作用。
7. 說明 Manual Weld 的用途與 Weld Joint／Weld／Segment 三層概念。
8. 列出 Factory Automation 各選項（Profile／Plate Cutting Interface、Dotori、GSD、Shrinkage、Robot Interface、Panel Line Control）的用途。
9. 讀懂 TRI/2（Robot Interface 2）中立檔的基本結構：`welded_joint`、`weld`、`weld_sequence`、`assembly_weld_table`。
10. 指出哪些環節可以由二次開發接入（檔案格式、PML 函式、報表 csv），哪些屬〔待核對〕。

## 28.2 四個模組在哪裡、彼此什麼關係

| 模組 | 一句話 | 資料流向 | 主要使用者 |
|---|---|---|---|
| Design Reuse | 跨專案複製設計資料 | 專案 A → Transfer Set → 專案 B | 設計者、專案管理 |
| Area Based ADP | 以「區域 × 樣板」批次出圖 | 3D 模型 → Draft 圖面 | 製圖管理員、製圖者 |
| Weld Planning | 計算組立的焊接資訊 | 組立樹 → 焊接表 → 報表／機器人檔 | 生產設計、焊接部門 |
| Factory Automation | 對接切割與焊接設備 | 模型 → 通用檔／中立檔 → 預處理器 | 生產技術、設備廠商 |

```
         ┌──────────────┐  Transfer Set   ┌──────────────┐
         │ 專案 A 設計  │ ───────────────► │ 專案 B 設計  │   Design Reuse
         └──────┬───────┘                  └──────────────┘
                │ 3D 模型
                ▼
      Area Based ADP ──► Draft 圖面（Plant/Marine 的 Draft，不含 Marine Drafting）
                │
   組立樹 (Assembly Planning) ──► Weld Planning ──► 焊接表 ──► Robot Interface 2 (TRI/2)
                │                                                 │
          Hull 零件 ───────────► Factory Automation ──► 切割／焊接設備（需預處理器）
```

> **專業提醒：** 這四項在官方文件各自成冊，授權與安裝也可能各自獨立（Design Reuse 需有效授權；ABA 另有安裝指南；Robot Interface 2 為選項）。上線前先向管理員確認你們的版本是否有這些模組〔待核對〕。

## 28.3 Design Reuse：跨專案重複使用設計

### 28.3.1 用途與核心概念

Design Reuse 簡化「在專案之間複製設計資料」的工作。官方強調：被複製的資料**不是原封不動拷貝，而是重新生成並適應目標專案的設計脈絡**；過程採「匯出—匯入」兩段式，中間以 **Transfer Set（傳輸集）** 暫存。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Design Reuse 概念：專案 A 匯出到 Transfer Set，再匯入專案 B

*圖 28-1　Design Reuse 概念：匯出、Transfer Set、匯入。（AVEVA 官方文件截圖，僅供內部教學）*

| 名詞 | 官方意義 | 白話 |
|---|---|---|
| Transfer Set | 暫存的傳輸集；存「資料定義」，不是二進位資料 | 一包可重播的建模指令加對照表 |
| Transfer Item | Design Reuse 處理的實體，可為模型物件或圖紙 | 清單中的一列 |
| Data Definition | 每種 Transfer Item 自有的定義格式，常見 `.sch`（船體 scheme）、`.dtl`（datal）、`.xml`、`.sdb`、`.til` | 重建該物件所需的語句 |
| Control File | `<Transfer Set 名稱>.xml`，記錄來源專案資訊與所有 Item 的原名與改名函式 | 目錄 |

因為存的是定義，匯入時系統是依參照、關聯與拓撲「重新建模」，而不是還原資料庫快照。這也是為什麼它能在目標專案改名、替換參照。

### 28.3.2 可處理的物件

| 類別 | 元素型別（官方列舉） |
|---|---|
| Assembly | `ASMBLY` |
| Room | `BLEVEL` |
| Outfitting | `CABLE`、`CWAY`、`EQUI`、`HVAC`、`PIPE`、`STRU` |
| Hull | `CCURVE`、`CPANEL`、`CPLANE`、`CPLATE`、`CPOINT`、`CPROF`、`CSEAM`、`CSTIFF`、`HPANEL`、`HRSO`、`MPLNST`、`MPRNST` |
| Drafting | `DRWG` |
| Link Documents | `LNDESC` |
| Diagrams | `SCDIAG`、`SCTEMP`、`SCPLIN`、`SCBRAN`、`SCSEG` 等 |
| Tags | `ENGITE` |

自訂的 UDET（使用者定義元素型別）與 UDA 會在傳輸中被處理；Hull 項目可在 Item Settings 決定是否帶 UDA。**Distributed Attributes 的定義不會被傳輸**，必須先在目標專案以 Lexicon 模組建好。狀態（Status）資料因與原專案緊密綁定，匯出時被忽略。

### 28.3.3 匯出與匯入的操作

Design Reuse 可從 Hull Design、Outfitting Design、Marine Drafting、Diagrams、Tags 模組進入，GUI 是 .NET addin，並與指令介面共用同一份資料，可任意混用。**匯出不限元素型別，匯入只能匯入該應用程式平常能建立的型別**，混合型別的 Transfer Set 可能需要切換模組分次匯入。

匯出步驟：

1. 選取要匯出的元素：從 Design／Draft Explorer 拖放、用 Search 結果、在 3D 視圖點選，或用右鍵 `Add To Design Reuse Export List`。
2. 用 `Get referred items` 把被選元素所參照的元素也加入（可重複），確保關聯物件不漏。
3. 按 `Export`，在視窗選資料夾與 Transfer Set 名稱（預設為前綴加流水號，可改），按 OK。
4. 用 `Display export info` 看匯出記錄。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Design Explorer 右鍵加入匯出清單，Design Reuse 視窗列出 HPANEL／CPANEL

*圖 28-2　以拖放或右鍵選單把元素加入 Design Reuse 匯出清單。（AVEVA 官方文件截圖，僅供內部教學）*

匯入步驟：先把**目標專案設為目前專案**，用 `Open` 開啟 Transfer Set，勾選要匯入的項目，按 `Import`；`Display log` 查看結果。`Topology Order` 欄顯示匯入順序，因為項目之間有相依，系統會反覆迭代，直到全部完成或無法再解析為止。

> 〔公開版未收錄：AVEVA 官方產品截圖〕匯入清單：已存在的項目不勾選、不適用的 DRWG 標示 Invalid

*圖 28-3　匯入清單：Topology Order 欄顯示順序，已存在或不適用的項目會被標示。（AVEVA 官方文件截圖，僅供內部教學）*

### 28.3.4 指令介面與批次

| 指令 | 子命令 | 用途 |
|---|---|---|
| `MCEXP` | `ADD`、`ADD REF`、`REMOVE`、`LIST`、`EXP` | 匯出選擇與執行 |
| `MCIMP` | `OPEN`、`EXCLUDE`、`INCLUDE`、`SHOW`、`IMP` | 開啟、排除、匯入 |
| `MCCONF` | `RESET` | 使用者設定重置 |

官方的典型情境：

```
> MCEXP ADD CE            // 把目前元素加入匯出選擇
> MCEXP ADD REF ALL       // 依目前選擇加入所有被參照的元素
> MCEXP LIST              // 檢視選擇
> MCEXP EXP /MyTSet       // 匯出到預設資料夾

> MCIMP OPEN /MyTSet      // 開啟 Transfer Set
> MCIMP SHOW              // 檢視內容
> MCIMP EXCLUDE <text>    // 排除某項
> MCIMP IMP               // 匯入
```

批次執行：準備一般 `*.bat`，在 tty 模式啟動模組，再呼叫 PML command macro；**PML 名稱函式在批次時不應與使用者互動**，且需在 macro 中為各 Transfer Set 設好正確的模組與應用程式。

### 28.3.5 各類物件的重點與限制

| 類型 | 傳輸方式 | 重點／限制 |
|---|---|---|
| 圖紙 `DRWG` | PADD 資料庫經 datal，加上 Marine 繪圖物件 `.SDB`；參照存 xml | 一張圖通常有 `<名>.dtl`、`<名>_R.dtl`、`<名>_1.SDB`、`<名>_1_refs.xml`；多張 sheet 有多個 SDB；Hull Design 可匯出，**只有 Marine Drafting 可匯入圖紙** |
| 舾裝 | datal，分兩段：先建結構，再設參照 | **元素必須有名稱**，參照維護靠名稱 |
| 船體 | 沿用批次輸入格式（scheme、XML） | 目標專案須已建立並初始化船體模型、Block 與參照曲面須存在、標準物件至少相當；**自由命名與傳統命名專案之間不支援、不能傳 Production Parts** |
| 組立 | datal | `NAMN` 由階層區域名稱組成，改名函式應針對 `ASNAME` 而非 `NAMN` |
| Diagrams | 元素與其成員 | 參照的元素要手動加入；Library 元素須先在目標建好；上層元素須命名，否則匯入可能當機 |

### 28.3.6 名稱調整（Name Changes）

匯出時，Transfer Set 內的名稱會被替換成「改名函式呼叫，並以目前名稱為必要參數」；匯入重新生成時才執行，把原名換成適合新脈絡的名稱。設計重點：

- 改名函式是**使用者自寫的 PML function**，官方附有範例函式。
- 元素型別與改名函式的對應，在 Item Settings 檔設定；UDET 可有獨立規格。
- 除了必要的名稱引數，可再加上以屬性或運算式為值的額外引數，並可選擇連同下屬元素改名。

> **專業提醒：** 圖 28-4 的 datal 定義裡 `'$[buildHPANELName('FB1-FR17_3','FB1')]'` 就是改名函式的呼叫形式：匯入時才求值。想把「FB1」換成目標專案的 Block 命名規則，就是改 `buildHPANELName` 這類函式，而不是改 Transfer Set。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Transfer Set 內的 datal 資料定義，名稱以 buildHPANELName 函式呼叫語法改名

*圖 28-4　Transfer Set 中的資料定義檔：名稱以改名函式呼叫表示。（AVEVA 官方文件截圖，僅供內部教學）*

### 28.3.7 二次開發怎麼接

| 接點 | 文件依據 | 可做的事 |
|---|---|---|
| 改名函式 | 官方明言為 PML function，並附範例 | 實作公司命名規則（Block、Panel、Assembly） |
| 批次 | `.bat` + PML macro | 排程匯出／匯入、搭配第 20 章的備份流程 |
| Transfer Set 檔案 | `.xml` 控制檔、`.dtl`、`.sdb` 等 | 外部檢查：Item 清單、命名是否衝突 |
| Settings 檔 | General／Item Settings | 預設資料夾、UDA 處理、Resolve References 開關 |
| 檔案路徑與設定檔格式細節 | 文件只說「見 General Settings File」 | 〔待核對〕 |

### 28.3.8 常見錯誤

| 現象 | 原因 | 處理 |
|---|---|---|
| 匯入後缺少 UDA／分散式屬性 | 目標專案沒預先建立定義 | 先用 Lexicon 建立 |
| 匯入圖紙失敗 | 在 Hull Design 匯入 | 切到 Marine Drafting |
| 匯入結果重複建立 | 匯出元素沒有名稱 | 先命名再匯出 |
| 圖面參照斷掉 | 被參照的模型元素沒一併匯出 | 匯出前用 `Get referred items` |

## 28.4 Area Based ADP：以區域與樣板批次出圖

### 28.4.1 用途與適用範圍

Area Based ADP（Automatic Drawing Production，以下簡稱 ABA）是 Draft 模組的擴充：**管理員預先定義「區域（Area，3D 中的長方體範圍）」與「樣板（Template，描述視圖、圖形表現與標註的圖面格式）」，使用者只要選區域與樣板的組合，就能批次產生圖面。** 官方舉的典型情境是：維修專案更改模型後，使用者進入 Draft、啟動 ABA、選區域，把該區域的所有圖面過夜重產。

> **專業提醒：** 官方明確寫著 **ABA 可搭配 AVEVA Plant 或 AVEVA Marine 的 Draft 模組，但不適用於 Marine Drafting 模組。** 若你們的製圖主力是 Marine Drafting（見[第 9 章](ch09_drawings_zh-TW.reading.html)），ABA 不是它的替代品，而是 Outfitting／Draft 那一側的出圖工具。

### 28.4.2 管理員與使用者的分工

| 角色 | 工作 | 權限 |
|---|---|---|
| ABA Drafting Administrator | 建立與維護 Libraries（樣板、區域、分類、Keyplan、符號、標註、任務）、預設值 | 須屬於 `DRAFTADMIN` 團隊，並對放置 library 的 PADD DB 有讀寫權；自由／一般使用者皆可擔任 |
| 一般使用者 | 只能使用管理員定義好的元素來產生圖面 | 一般製圖權限 |

建議把符號、標註、樣板放在一般使用者唯讀的資料庫；管理員進入 Draft 時只載入由管理員產生的 binary，否則看不到管理選單。

### 28.4.3 資料階層

> 〔公開版未收錄：AVEVA 官方產品截圖〕ABA 樣板階層：LIBY 之下有 DRTMLB、TASKLB、DLLB、TRLB、SHLB、SYLB

*圖 28-5　Area Based ADP 的樣板階層：各元素的 Purpose 設為 `ABAT`。（AVEVA 官方文件截圖，僅供內部教學）*

| Library 元素 | 內容 | 說明 |
|---|---|---|
| `LIBY` | 最上層 library | 持有所有 ABA 管理元素 |
| `DRTMLB` | Drawing Template Library，內含 `DRTMPL` | 圖面樣板 |
| `TASKLB` | Task Library，內含 `TASK`、`TKPARA` | 任務與參數 |
| `DLLB` | Area 定義、Classification，內含 `IDLI`（ID List） | 區域邊界座標與分類規則 |
| `TRLB` | Tag Rule Library，內含 `TRST`、`TAGR` | 標註規則 |
| `SHLB` | Keyplan 的 overlay，內含 `OVER` | 索引圖 |
| `SYLB` | 符號（如指北針） | `SYTM` |

預設值檔 `DRA-ABA-DEFAULTS` 放在 `%PDMSDFLTS%`，分為一般預設、可用視圖比例、符號樣板名稱，以及英制／公制圖紙尺寸等區段；使用者每次載入的記錄存於 `%PDMSUSER%/aba_defaults`。ABA Defaults 表單可指定各 library 位置，`Create Hierarchy` 能自動建立上述階層（只偵測 `LIBY` 是否存在，不檢查其下元素）。可為不同專業建立多份預設檔與 library。

> 〔公開版未收錄：AVEVA 官方產品截圖〕ABA Defaults 表單：Library、Template、Area、Classification、Keyplans、Symbols、Labelling、Tasks 的位置

*圖 28-6　ABA Defaults 表單：左側為各 library 位置，右側為對應元素型別。（AVEVA 官方文件截圖，僅供內部教學）*

### 28.4.4 管理員的建置工作

| 工作 | 入口 | 重點 |
|---|---|---|
| 區域 Area | Create → Area ADP Library → Area Library | 區域是 `DLLB` 下的 ID List，可依專業拆多個 library 並以 Function 區分 |
| 分類 Classification | Create → Area ADP Library → Classification | 準則有兩種：Rule（如 `ALL PIPE WITH PSPEC EQ A1A`）與 Element；**`ALL` 必須搭配型別，否則評估很慢** |
| 任務 Task | Create → Area ADP Library → Task | 分 View、Drawing、Process、Naming 四類；名稱不可有空白，前綴 `*` 表 AVEVA 供應 |
| 標註 Labelling | Create → Area ADP Library → Labelling | Tag Rule Set 內含多條 Tag Rule，每條有規則與 Label Template |
| 樣板 Template | Create → Area ADP Library → Template Drawing | 依序設定 Drawing → Sheet → View；Function 用來分類與自動編號 |
| Keyplan 圖層 | Keyplan Layers | 兩種做法：View Based 與 Overlay Sheet |
| 自動編號 | Auto-Number Rules | 規則存 `dra-nam.pmldat`、元素規則存 `dra-element-rules.pmldat`（預設在 `%PDMSUSER%`） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕ABA Task Definition 表單：Task Types、Name、Function、Task Parameters

*圖 28-7　ABA Task Definition：Function 欄指向 PML 函式檔，Parameters 以 String／Real／Distance／Boolean 設定。（AVEVA 官方文件截圖，僅供內部教學）*

**任務是 ABA 的擴充點。** 官方說明：每個新任務要有對應的 PML function 檔，放在 `PMLLIB` 路徑內（例如 `ABAARRANGE` 對應 `abaarrange.pmlfnc`）；任務資訊存在 Tasks Library。供應的任務包括：

| 類型 | 任務 | 作用 |
|---|---|---|
| Process | Plots Drawings | 把一次處理的所有圖面依格式與目錄出圖 |
| Process | Report Labels | 對整批圖面輸出標註報表（內容由外部預設檔控制） |
| Process | Hyper_Plant | 產生四種檔案（`-dra1.plt`、`-dra1.hit`、`-pdms_dsheet.out`、`-pdms_item_to_dsheet.out`），可查「某設備出現在哪些圖」 |
| Drawing | Keyplan_View | 以 Overlay Sheet 方式產生索引圖 |
| Drawing | Report_Labels／Schedule | 單張圖報表；依分類產生表格 |
| View | Arrange Labels | 把標註排到視圖邊界（僅對 `TXTM` 標註樣板正確，`SYTM` 的原點不定） |
| View | Draw_MeasureLines／North_Arrow | 畫刻度尺；加指北針（只支援平面與 Iso 1–4 視圖） |

Naming Task 是一個特例：它在圖面加入處理清單時執行，收到的第 1、2 個參數是樣板名與區域名，必須回傳字串；回傳空字串則用預設名（樣板名-區域名，例如 `/DRTM-PIPING-A0-A101`）。官方提供 `!!abanewdrwgs.checkname(!namestring)` 檢查重名，回傳 0（可用）、1（Draft 資料庫已用）、2（本批次待建清單已用）。

### 28.4.5 使用者的出圖流程

進入 Draft 後，選 **Draft → Auto Drawing Production** 啟動 ABA，再 **Create → Area ADP Drawings** 開啟 `Process Drawings Control`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Process Drawings Control：New Drawings、Existing Drawings、Drawing Registry Area、Process Settings、Batch Process

*圖 28-8　Process Drawings Control：由上而下依序是新圖、既有圖、登錄區、處理設定、開始處理。（AVEVA 官方文件截圖，僅供內部教學）*

1. **New Drawings**：按 `Select` 開啟 `ABA New Drawing List`，在樣板與區域兩個清單選組合，右鍵 `Add Selection to List`。
2. **Existing Drawings**：用 `Select`、或以 CE／Current List 加入既有圖面，用於更新、重生或重編號。
3. **Drawing Registry Area**：指定存放的 `REGI`，可自動建立或選既有的。
4. **Process Settings**：選 Process Tasks 與 Process Type；Auto Numbering 可開關。
5. **Start Processing**：`Process Now`，或勾 `Batch Process` 產生 `Name.bat` 與 `Name.mac`，再用 Windows 工作排程器排程（預設位置 `%PDMSABABATCH%`）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕ABA New Drawing List：左為樣板，右為設計區域，右鍵選單可加入清單

*圖 28-9　選擇樣板與區域組合，產生預設名稱為「樣板-區域」的新圖面。（AVEVA 官方文件截圖，僅供內部教學）*

三種 Process Type 差異很重要：

| Process Type | 行為 | 使用者自行加的 2D 圖層 |
|---|---|---|
| Create & Update | 建新圖；既有圖重跑設計圖形、標註與任務 | 保留（不刪除圖層） |
| Create & Regen(erate) | 建新圖；既有圖等於刪除重建 | 消失 |
| Process Tasks Only | 只執行所選 Process Task（如出圖），不改圖面 | 不受影響 |

**Variant 樣板：** 新圖一律用 master 樣板，只有既有圖才能用 `Modify Variant` 切到 variant（清單以 M、V1、V2 標示）；一個 master 可有多個 variant，且**變體無法還原為 master**。適用情境如「95% 的管路配置圖用 master，其餘需要多一個等角視圖」。

每次處理會產生 log，記錄所用區域、樣板、時間與警告，位置由 Defaults 表單指定。

### 28.4.6 二次開發怎麼接

| 接點 | 文件依據 | 備註 |
|---|---|---|
| 新任務 | PML function 檔（`.pmlfnc`）放 `PMLLIB` | 參數以 `TKPARA` 設定，修改表單預設為文字 |
| Naming Task | 回傳字串；`!!abanewdrwgs.checkname` | 文件有範例 |
| 編號規則 Format | 可用 PML 運算式呼叫函式／方法 | 文件說明有限，細節〔待核對〕 |
| Report Labels／Hyper_Plant 輸出 | 文字檔、分號分隔 | 可由外部程式讀取，詳見第 16 章 |
| Batch | 產生 `.bat`／`.mac` | 可納入排程 |
| 自訂 Rule／Classification 語法 | 文件僅給範例 | 〔待核對〕 |

與其他章：ABA 是 Draft 側工具，樣板與標註需先熟悉[第 9 章](ch09_drawings_zh-TW.reading.html)的圖面概念；PML 基礎見[第 11 章](ch11_pml_language_zh-TW.reading.html)；報表輸出見[第 16 章](ch16_reports_integration_zh-TW.reading.html)。

> **專業提醒：** 官方在 Limitations 只寫「一般 Draft 的限制皆適用」，另列名稱長度、規則運算式、Task 與 Symbol Template 三個小節，內容為標題而已，**細節〔待核對〕**。

### 28.4.7 常見錯誤

| 現象 | 原因 | 處理 |
|---|---|---|
| 看不到管理選單 | 載入了使用者建立的 binary、或不在 `DRAFTADMIN` | 離開 Draft，用管理員 macro 重新進入 |
| Classification 計算很慢 | `ALL` 沒指定元素型別 | 加型別限定，如 `ALL PIPE WITH ...` |
| Create Hierarchy 圖示不笑 | 預設表單中 library 路徑不正確 | 檢查階層；注意只檢查 `LIBY` |
| 重產後 2D 註記不見 | 選了 Regen | 改用 Create & Update |
| 圖名衝突 | 預設名稱重複 | 在 Naming Task 內檢查並回傳空字串 |

## 28.5 Weld Planning：組立焊接分析與機器人資料

### 28.5.1 用途

Weld Planning 對**已用 Assembly Planning 定義好的船體組立**做焊接分析與規劃，依 Product Information Model（PIM）的拓撲與實際幾何計算。功能包含：單一組立焊接計算、連同所有子組立的遞迴計算、自動計算焊腳長（Weld Leg Length）與焊接姿勢（Weld Position）。組立規劃與焊接規劃的概念介紹見[第 6 章](ch06_hull_production_zh-TW.reading.html)的 6.8，本節只補操作與設定；船體模型見[第 5 章](ch05_hull_modelling_zh-TW.reading.html)。

### 28.5.2 核心概念

| 概念 | 說明 |
|---|---|
| Weld Table | 組立的焊接資料集合，對應 TRI/2 的 `assembly_weld_table` |
| Welded Joint | 兩個（以上）零件的焊接連接，由一或多道 Weld 組成；UDA 型別為 `MWLDJT` |
| Weld | 一道焊縫；UDA 型別為 `MWELD` |
| Suspension | 焊縫起訖的避讓（不焊的）距離，可依規則或係數計算 |
| Return Weld | 零件端部沿厚度方向的短焊縫 |

### 28.5.3 功能操作

在 Assembly Planning 樹選取組立節點，右鍵選單即出現焊接功能。

> 〔公開版未收錄：AVEVA 官方產品截圖〕組立節點右鍵選單：Detect Welds、Create Weld Report、Create Robot Control File、Edit Welds、Update Model

*圖 28-10　組立節點的右鍵選單，焊接功能位於中段。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 作用 | 要點 |
|---|---|---|
| Detect Welds | 對所選組立計算焊接 | 先算每個零件的外接盒，以減少零件配對；可按 Cancel 中斷；結果顯示於 3D |
| Detect All Welds (Top-Down) | 遞迴：先所有子組立，再所選組立 | 與逐一計算結果相同但省時 |
| Create Robot Control File／Create All… | 產生機器人控制檔 | 內容含組立的完整幾何、屬性、焊接幾何與參數 |
| Edit Welds | 編輯計算結果與 UDA | 顯示 Edit Weld Properties 視窗 |
| Update Model | 把 Weld Table 的焊腳長寫回船體模型 | 只更新平面板、肘板、加強材；之後可用於圖面 bevel note、scheme 檔 |
| Create Weld Report | 產生 csv 報表 | 見 28.5.5 |
| Manual Weld | 手動指定焊縫 | 見 28.5.6 |

注意：支柱（pillar）的焊接尚未完整開發，因此預設封鎖支柱與其他零件間的自動焊接；若要保留（部分不正確的）功能，可設環境變數 `SBH_AUTO_WELD_PILLAR`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕自動偵測焊縫後在 3D 視圖以顏色標示的船體結構

*圖 28-11　焊接計算結果顯示於 3D 視圖。（AVEVA 官方文件截圖，僅供內部教學）*

編輯視窗分 Welded Joints 與 Weld for Joints 兩頁。Joint 可改 comment 與 UDA；Weld 可改 comment、position、leg length、layers、process、standard process、test procedure、start／end suspension 與 UDA；零件厚度、bevel、connection angle 等為唯讀。選取某焊縫時，它會成為目前元素並在 3D 或圖面上高亮。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Edit Weld Properties：每道焊縫的位置、尺寸、長度、層數、bevel、厚度、suspension、連接角

*圖 28-12　Edit Weld Properties 的 Weld for Joints 頁。（AVEVA 官方文件截圖，僅供內部教學）*

此外，焊縫與整個 Weld Table 可從資料庫 Explorer 或組立樹拖放到 symbolic hull view；view 屬性可切換顯示平面焊與斷面焊。

### 28.5.4 設定檔（Weld Planning Setup）

所有設定檔都是以通用 TIL 格式寫成的純文字，放在 `SB_SHIP` 目錄。

| 檔名 | 語句 | 作用 |
|---|---|---|
| `weld Position.def`（官方原文如此，檔名含空白，〔待核對〕） | `POSITION` | 依 JIS Z 3003-1963 的旋轉角與傾斜角定義焊接姿勢區間 |
| `weldLegLength.def` | `LEGLENGTH` | 依焊接型式、兩零件厚度與材質定義焊腳長 |
| `weldDefaults.def` | 每個預設參數一個語句 | 各種計算開關與機器人檔標頭資訊 |
| `weldSuspension.def` | `PLATE_RULES`、`PROFILES_RULES`、`SUSPENSIONFACTOR` | 定義各種缺口、切口前後的避讓距離 |

`POSITION` 的語法（官方原文）：

```
POSITION, <pos name>
  /WELD_TYPE=<fillet|butt> /DESCRIPTION=<說明>
  /MIN_ROT=.. /MAX_ROT=.. /MIN_INCL=.. /MAX_INCL=..;
```

**判斷順序有意義**：系統依檔案順序逐條檢查，找到第一個符合者。官方範例中姿勢代號有 F（Flat 平焊）、V（Vertical 立焊）、H（Horizontal 橫焊）、O（Overhead 仰焊），以及對應的 IF、IV、IH、IO 中間姿勢；姿勢名稱最長 26 字元。

`LEGLENGTH` 的語法：`LEGLENGTH, <焊腳長> /WELD_TYPE=.. /PART1_THICK=.. /PART2_THICK=.. /PART1_QUAL=.. /PART2_QUAL=..;`，厚度給 `-1` 表示不檢查，材質給 `'*'` 表示不檢查。官方範例如 FILLET 型板厚 5 對應焊腳 3、板厚 40 對應焊腳 11。焊腳長也可改用 Hull 的 Execution Units 計算（見 *Hull Setup and Customization*，本章未涵蓋）。

`weldDefaults.def` 的主要參數：

| 參數 | 值 | 作用 |
|---|---|---|
| `ADD_RETURN_WELD` | Yes／Separate／No | 是否自動建立 Return Weld；Yes 併成一道，Separate 分開（從 Structural Design 使用時恆為 Yes） |
| `MINIMUM_WELD_LENGTH` | 數值 | 短於此長度的焊縫刪除 |
| `MIXED_WELD_TYPE` | 型式 | 兩側焊縫型式不同時的 Joint 型式 |
| `WELD_TYPE_TOLERANCE` | 角度 | 兩板夾角小於此值視為對接焊，否則填角焊 |
| `CALCULATE_LEGLENGTH` | Yes／No／FromModel | 是否計算焊腳長，或取自模型 |
| `CALCULATE_POSITION`／`CALCULATE_SUSPENSION` | Yes／No | 是否計算姿勢、避讓 |
| `REMOVE_FULL_SUSPENSION` | Yes／No | 完全被避讓的焊縫是否移除 |
| `CREATE_WELD_REPORT` | Yes／No | 計算後自動產生報表 |
| `WELD_PRESENT_SIZE` | 數值 | 顯示時小於此焊腳者以此尺寸顯示（系統預設 10.0） |
| `AUTHORIZATION`／`ORGANIZATION`／`AUTHOR` | 文字 | 寫入機器人檔標頭 |
| `ADD_SYM_PART_REF`／`INCLUDE_SUBASS_WELD` | Yes／No | 對稱零件雙邊資料；是否含子組立焊接表 |

避讓若設了 `SUSPENSIONFACTOR`，就以「係數 × 兩零件較小厚度」計算，**此時 suspension 規則完全不使用**。

### 28.5.5 Weld Planning Batch 與 Weld Report

批次輸入檔只有一種語句，可重複：

```
ASSEMBLY, 'R007-B010-KS0101' /CALC_WELD /ROBOT_CTRL;
ASSEMBLY, 'R007*' /WELD_REPORT;
```

組立名稱結尾加 `*` 表示連同所有子組立，由上而下處理；`/CALC_WELD` 做焊接計算，`/ROBOT_CTRL` 產生機器人檔，`/WELD_REPORT` 經 Vitesse 產生報表，每個組立兩個 csv。從 Weld Planning 群組雙擊 Weld Planning Batch 圖示，再選輸入檔。

Weld Report 原始資料存成 `weld-<組立使用者名稱>.csv`，位置在環境變數 `SB_SHIPPRINT` 所指目錄。**第一列是組立總覽**（專案名、組立路徑、Weld Table 註解、建立日期、狀態、總焊長、總連接長、總避讓長），**其後每道焊縫一列**，欄位依序為：

| 欄位群 | 欄位 |
|---|---|
| 1–6 | Joint 名稱、Joint 註解、兩零件名稱（內建規則）、兩零件自訂名稱（Part Name Control 規則） |
| 7–12 | 兩零件厚度、兩零件 bevel code、兩零件材質 |
| 13–17 | 焊接 Joint 型式、兩個未使用欄（0、0.0）、焊縫名稱、焊縫註解 |
| 18–24 | 焊腳長、焊長、層數、焊接姿勢、製程、標準製程、測試程序 |
| 25–31 | 起／迄避讓、連接角、旋轉角、傾斜角、Joint 總焊長、Joint 總避讓 |
| 32–35 | 兩零件的組立名稱與組立路徑 |
| 36 起 | `MWLDJT` 與 `MWELD` 的 UDA |

Manual Weld 建立的焊縫在報表中會多一欄標示（1 手動、0 自動）。

### 28.5.6 Manual Weld

自動計算有時產不出焊縫，這時用 Manual Weld：在 3D 視圖點選零件與多個點，手動建立焊縫；產出的 Joint 與自動焊縫一樣進報表。慣例是：**Joint（`J-<N>`）由多條 Weld（`W-<N>`）組成，Weld 由多個 Segment（直線或圓弧）組成，Segment 由點定義。**

> 〔公開版未收錄：AVEVA 官方產品截圖〕Manual Weld 視窗：Part one／two、Type、Leg Length、Segment type、Create weld、Create joint

*圖 28-13　Manual Weld 視窗。（AVEVA 官方文件截圖，僅供內部教學）*

流程：

1. 在 Assembly Planning 樹對組立右鍵，選 Weld → Manual weld（視窗上方顯示目標組立，換選組立會變）。
2. 用 Pick 選 Part one 與 Part two，選 Type（預設 Fillet），輸入 Leg Length（mm）。
3. 選 Segment type：Lines（起迄點）或 Arcs（起點、弧上一點、終點）；按 `Start from new point`，以 Graphics and Cursor 在面、邊、角點上取點；Esc 可撤銷最後一點。
4. 按 `Create weld` 把線段轉為焊縫；要多道焊縫就重複；最後按 `Create joint`，存入 Weld Table。

手動焊縫會以後綴 `: M` 顯示在組立瀏覽器中，**自動偵測不會刪掉它**。大張角的圓弧會被拆成三段以避免弦高大於半徑。

### 28.5.7 二次開發怎麼接

| 接點 | 文件依據 | 備註 |
|---|---|---|
| 批次輸入檔 | 官方語法 | 自動化夜間計算，對所有組立加 `*` |
| csv 報表 | 官方列出全部欄位 | 可由 Python／.NET 讀取彙整焊長、焊材；欄位序號固定，但新增 UDA 會延後欄位〔建議依表頭動態解析，待核對〕 |
| `.def` 設定檔 | 官方語法完整 | 純文字，可由外部檢查工具驗證、版本控管 |
| UDA | `MWLDJT`、`MWELD` | 可加入公司自訂欄位並在 Edit Welds 編輯 |
| TRI/2 中立檔 | 見 28.6.3 | 供機器人或外部系統解析 |
| Vitesse 產生報表 | 文件僅說經 Vitesse，見[第 15 章](ch15_hull_vitesse_zh-TW.reading.html) | Vitesse 介面細節〔待核對〕 |
| 焊接相關 PML 或 .NET API | 官方未提供 | 〔待核對〕 |

### 28.5.8 常見錯誤

| 現象 | 原因 | 處理 |
|---|---|---|
| 計算不出焊縫 | 幾何或拓撲條件不符 | 用 Manual Weld 補 |
| 姿勢全落在錯誤類別 | `POSITION` 順序不當（依序命中第一條） | 調整檔案順序 |
| 避讓規則沒有生效 | 設了 `SUSPENSIONFACTOR` | 擇一使用 |
| 焊腳長沒寫進模型 | 沒執行 Update Model，或零件不是平板／肘板／加強材 | 檢查 |
| 重算後手動焊縫消失？ | 不會，官方說明自動偵測不刪手動焊縫 | 以 `: M` 識別 |

## 28.6 Factory Automation：與設備對接

### 28.6.1 概覽

Factory Automation 是「造船自動化」選項的集合，可單選、也可組合，通常**整合在各設計功能裡**，詳細文件分散於 Hull 的 Manufacturing、Setup 等章節。要依各廠設備與慣例做適當設定，設定工具都有文件。多數接口**只負責輸出中立格式**，接收端必須有預處理器（preprocessor），AVEVA 不提供轉成特定機器人語言或控制器的翻譯。

| 選項 | 用途 | 輸出／輸入重點 |
|---|---|---|
| Profile Cutting Interface | 輸出型材切割資料給機器人或外部型材軟體 | 一個巢狀（nesting，官方稱 order）一個 ASCII「generic file」；含各型材零點位置與端切（end-cut）巨集，孔、缺口、切口以完整幾何表達；附預處理器範本，需客戶或機器人廠商自行開發預處理器 |
| Plate Cutting Interface | 把資料庫中的板件抽成通用格式供外部程式處理 | 獨立選項；可依組立、Block、Panel、單一零件、或某日期後更動者選取 |
| Dotori | 變動斜角（Bevel）計算，與 Hull 的 Bevel Handling 緊密整合 | 填角焊的斜角可依連接角決定；可依連接角與板厚設規則自動選型；規則可分「set」給不同產線；可自動修正零件輪廓；斜角資訊進入 Nesting 與 Burning，以明確角度輸出 |
| Genauigkeit（GSD Marking Triangles） | 組裝用三角形標記，提升精度、減少現場修整 | 板角、型材跡線、肘板、船中心線、殼板邊界等位置；與標記軌跡可由 Nesting 合併為單一幾何 |
| Reference Planes | 在產品模型加入對位用參考面並標記在板與型材上 | 平面可為主平面、三點或點加法向量；Hull 能顯示穿過目前 Panel 的所有平面 |
| Extended Shrinkage Handling | 焊接收縮補償的進階版 | 垂直焊縫方向局部補償、沿焊縫方向以比例縮放；平面與曲面均可；以 shrinkage object 定義量 |
| Extended Bevel Handling | 基本 Bevel 的擴充 | 擴及型材與肘板，僅限處理平面零件的模組 |
| Robot Interface | 把生產零件傳給焊接機器人設備 | ASCII 傳輸檔；零件以體積（如一般圓柱）加輪廓傳送，可依名稱、日期、空間盒選取；僅傳有限生產資訊（材質、表面處理、位置號、目的地） |
| Panel Line Control | 在大張原板上巢狀排列、產生噴砂／標記／切割／文字標註的 NC | 僅有 ESSI 與 ESAB NCE510 後處理器；其他需客製開發；〔僅依需求提供〕 |
| Robot Interface 2 | 以 STEP 為基礎的新版機器人介面 | 見下節 |

> **專業提醒：** 「生產設備能不能吃」取決於**預處理器**，而不是這些選項本身。選型前先釐清接收端有沒有現成的預處理器、誰來寫、輸入格式規格由誰維護。

### 28.6.2 Dotori 與斜角資訊的串接

Dotori 的資料脈絡是：**設計時指定斜角類型與規則 → 零件抽出時自動帶入斜角資訊與修正輪廓 → 巢狀與切割以明確尺寸輸出 → 後處理器轉成燒切機控制碼。** 官方亦提到：已拆為腹板與翼板的組合型材，腹板轉為板件時可自動算沿軌跡斜角，但目前只能產生緊密連接（tight connection）的斜角類型，無法選擇。製程面的概念見[第 6 章](ch06_hull_production_zh-TW.reading.html)。

### 28.6.3 Robot Interface 2（TRI/2）中立檔

Robot Interface 2 讀取 Weld Planning 已計算的組立焊接資料，連同組立結構與零件幾何，**每個組立輸出一個中立檔**，檔名 `tri-<組立名稱>.spf`，放在 `SB_STEPPRINT`（沒有就放 `SB_SHIPPRINT`）。資料模型參照 ISO 10303-218（焊接資料）、以 EXPRESS（ISO 10303-11）描述，檔案格式參照 ISO 10303-21（STEP），但官方註明**並非完全相容**。介面提供樹狀瀏覽器（可拖放、可查詢組立資訊）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕TRI/2 中立檔範例：ISO-10303-21 標頭，後接 #id=實體(屬性…) 的資料列

*圖 28-14　Robot Interface 2 中立檔範例開頭（官方範例檔截圖）。（AVEVA 官方文件截圖，僅供內部教學）*

檔案語法重點：

```
ISO-10303-21;
HEADER;
FILE_DESCRIPTION('...'); FILE_NAME('...'); FILE_SCHEMA(('TRI/2','2.6'));
ENDSEC;
DATA;
#<唯一編號>=<實體名稱>(<屬性列表>);
...
ENDSEC;
END-ISO-10303-21;
```

- 每個實體有唯一 `#id`，可在其他實體的屬性中當指標；字串以單引號，實數可用 `12.2785` 或 `0.122785E+02`，清單以括號，空清單 `()`，未指定屬性以 `$` 表示。
- HEADER 的 `FILE_NAME` 含時間戳記、author、organization、前處理器版本、原系統與 authorization，其中 author、organization、authorization 取自 `weldDefaults.def`。

焊接相關實體（官方列出的屬性數）：

| 實體 | 屬性數 | 說明 |
|---|---|---|
| `assembly_weld_table` | 11 | 一個組立的焊接表；含 `joints`、`weld_sequences`、`weld_length`、`suspension_length`、`connection_length` |
| `welded_joint` | 10 | 零件連接；含 `weld_type`（butt／fillet）、`manual`（是否手動）、`closed`、`parts`、`welds` |
| `weld` | 26 | 焊縫；含 `size`、`layers`、`wlength`、`position`、`start_suspension`、`end_suspension`、`part_1/2`、`bevel_1/2`、`thickness_1/2`、`connection_angle`、`rotation_angle`、`inclination_angle`、`torch_vector`、`weld_flag`、`weld_contour`、`weld_geometry` |
| `weld_sequence` | 6 | 焊接順序；含 `start_offset`、`end_offset`、`welds`（`directed_weld` 清單） |
| `directed_weld` | 2 | 指定焊縫方向（`True`：起點到終點） |

列舉型別：`weld_type` 為 `butt`／`fillet`；`weld_flag_option` 為 `bridge`／`thickness`／`knuckled`／`none`；`bevel_code`、`shrinkage_margin` 為整數。另有 `assembly`（32 個屬性）、船體相關的 `plate`、`stiffener`、`bracket`、`panel`、`part`、`endcut` 等實體，本章未逐一展開。

> **專業提醒：** `weld` 實體的 `bevel_1/2`、`torch_vector` 等欄位，可以直接對應 28.5.5 報表中的 bevel code 與角度欄位，但兩者**欄位順序與命名並不相同**，不可混用解析器。

### 28.6.4 二次開發怎麼接

| 接點 | 文件依據 | 備註 |
|---|---|---|
| TRI/2 檔案解析 | EXPRESS 實體定義完整、語法簡單 | 最適合以 Python 寫解析器做檢查（例如焊長加總與報表比對）；只依官方實體定義，勿假設未列出的屬性 |
| Generic file 預處理器 | 官方提供範本，由客戶或廠商開發 | 屬於接收端系統，常為本地化專案 |
| Nesting／Burning 後處理器 | 僅 ESSI、NCE510 標準提供 | 其他設備須客製〔待核對〕 |
| 控制參數 | 多為預設檔與 logical variables | 名稱與路徑在 Hull Manufacturing 章節，本章未取材〔待核對〕 |

### 28.6.5 常見錯誤

| 現象 | 原因 | 處理 |
|---|---|---|
| 以為輸出可直接餵機器人 | 官方明言不含轉換為機器人語言或控制器 | 先確認預處理器 |
| TRI/2 沒有焊縫資料 | 未先在 Weld Planning 計算 | 先 Detect Welds |
| 檔案不在預期目錄 | `SB_STEPPRINT` 未設則用 `SB_SHIPPRINT` | 檢查環境變數 |
| Panel 輸出無焊接資訊 | 單一 Hull panel 的輸出不含焊接 | 改以組立為單位輸出 |

## 28.7 四個模組的銜接與選用

| 情境 | 建議用法 |
|---|---|
| 新船案想沿用舊船的 Block 結構與板架 | Design Reuse，並先寫好改名函式 |
| 維修專案模型變動，需整批重出管路／設備平面圖 | ABA，用 Create & Update 保留 2D 註記 |
| 想知道某組立總焊長與姿勢分佈 | Detect Welds + Weld Report |
| 焊接機器人需要焊縫軌跡與零件幾何 | Create Robot Control File（TRI/2） |
| 型材與板件要送自動切割線 | Profile／Plate Cutting Interface + 預處理器 |

> **專業提醒：** 四個模組的共同特徵是「**設定檔與外部預處理器決定成敗**」。把設定檔（`DRA-ABA-DEFAULTS`、`weldDefaults.def` 等）放進版本控管，並記錄對應的專案與版本，是最划算的二次開發前置工作；備份與升級見[第 20 章](ch20_system_administration_zh-TW.reading.html)。

## 28.8 本章小結

- **Design Reuse**：匯出到 Transfer Set（資料定義加參照加改名函式），再匯入重新生成；匯入受目前應用程式限制，需有名稱、目標專案需預先準備；`MCEXP`／`MCIMP`／`MCCONF` 提供指令介面與批次。
- **Area Based ADP**：管理員定義 Area、Template、Classification、Task、Tag Rule、Keyplan；使用者在 Process Drawings Control 選區域與樣板組合批次出圖；Task 是 PML 擴充點；不適用 Marine Drafting。
- **Weld Planning**：以右鍵選單偵測、編輯、更新模型與報表；四個 `.def` 設定檔控制姿勢、焊腳長、預設與避讓；Manual Weld 補足自動計算不足。
- **Factory Automation**：一組對接切割與焊接設備的輸出接口，格式中立、需預處理器；Robot Interface 2 以 STEP 風格輸出組立、焊縫與幾何。
- 二次開發接點集中在：PML 改名函式與 Task、批次檔、設定檔、csv 與 TRI/2 檔案解析。

## 28.9 練習題與自我檢核

1. 為什麼 Design Reuse 的 Transfer Set 要存「資料定義」而不是資料庫快照？這帶來哪些好處與限制？
2. 匯出一批 `PIPE` 時，為什麼要先確認每個元素都有名稱？沒有會發生什麼事？
3. 說明 ABA 的 `Create & Update` 與 `Create & Regen` 差異；什麼情況選哪一個？
4. 寫出一個 Naming Task 應有的流程（取得樣板名與區域名、檢查重名、回傳字串）。
5. 若 `weldDefaults.def` 設 `MINIMUM_WELD_LENGTH` 為 20，而 `weldSuspension.def` 又設了 `SUSPENSIONFACTOR`，結果會如何？
6. 在 `POSITION` 檔中把 `O`（仰焊）放在 `IO` 之後，可能發生什麼？
7. 為什麼 Robot Interface 2 要求先做 Weld Planning？
8. 設計一個 Python 腳本：讀取 `weld-*.csv`，對每個組立加總焊長，並與 TRI/2 的 `assembly_weld_table.weld_length` 比對（說明需要哪些前提與〔待核對〕之處）。

## 28.10 〔待核對〕彙整

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
