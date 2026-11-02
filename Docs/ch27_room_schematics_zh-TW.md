# 第 27 章　艙室設計與原理圖：Room Design 與 Schematics

> 前面幾章處理的都是「船體與管線這類大結構」。船上還有另一半工作：住艙、廚房、控制室、走道的**艙室配置**（牆、天花、地板覆蓋、門窗、家具與各類配件），以及在 3D 模型之前就存在、在模型之後必須對得起來的**原理圖**（P&ID、系統圖、線表）。
>
> 這一章把兩件事放在一起，因為它們共用一個問題：**「設計意圖」與「3D 模型」如何保持一致。** Room Design 把建築式的設計意圖（房間類型、淨高、牆厚、天花格柵）存成專屬資料結構；Schematic 3D Integrator 與 Compare/Update 則把原理圖資料與 3D 資料逐項比對、連結、更新。
>
> **資料可信度：** 本章操作流程、視窗名稱、元素型別（`BBLOCK`、`BLEVEL`、`ROOM`、`CTWALL`、`CYMLNK` 等）與 PML 方法名，取自 AVEVA Marine 12.1 官方離線文件的 *Room Design* 與 *Schematics* 兩大章節。須注意兩點：（1）Room Design 的使用者指南多為視窗欄位說明，且 `RPATH` 一節明載「將於後續 Service Pack 提供」，內容偏薄；（2）文件中的 *Schematics* 實際涵蓋 Compare/Update、Schematic 3D Integrator 與 Tags 三份指南，**並不教你如何繪製原理圖**（那屬於 AVEVA Diagrams／P&ID 產品，不在本文件範圍內）。官方頁面的中文為機器翻譯，譯名生硬，本章改用台灣慣用譯名並保留英文術語。文件僅有 Compare/Update 與 Integrator 有 PML 範例；Room Design 沒有任何 PML 範例，相關處一律標〔待核對〕。

## 27.1 學習目標

讀完本章，你應該能夠：

1. 說明 Room Design 的資料階層 `BBLOCK → BLEVEL → ROOM → DETGRP`，並指出各層的責任。
2. 從 Design > Room Design 啟動應用，並說明工具列、Navigator 與 Layout／Detailing 兩組工作視窗的分工。
3. 依步驟建立 Building Block、Floor Elevation 與 Room，並說明 Room Type、淨高與房間邊界的設定。
4. 說明牆（`CTWALL`）、天花（`CEILIN`）、地板覆蓋（`FLRCOV`）、隔熱需求（`INSURQ`）的建立入口與細部（Panel／Profile／Joiner）。
5. 說明家具、配件與固定設備如何經 Room Design Specification（`SPWL`／`TABGROUP`／`CTABLE`／`TABITEM`／`GPART`）選取。
6. 說明門窗與配件的貫穿孔機制（`OPGE`／`HPGE`），以及為何船殼開孔需經 Hole Management 核准。
7. 說明原理圖資料類型，以及 Integrator 的三大功能：Compare、Build、Link。
8. 讀懂比較報表與顏色代碼，並知道如何接受差異、自動連結、自動更新屬性。
9. 說明 Compare/Update 的 Scope by Source／Scope by Destination 與 Dabacon 元素的比對對應。
10. 指出二次開發的接點：`CompareUpdate`、`integrator`、`IntegratorProjectHandler` 與 `CYMLNK` 偽屬性，並分辨哪些在文件中有依據。

## 27.2 Room Design：艙室配置

### 27.2.1 定位與既有章節的分工

Room Design 是 Outfitting 模組中的建築式艙室配置工具，資料與 3D 模型同屬 DABACON 資料庫，因此可以與管路、設備在同一個模型中瀏覽與出報表。它與其他章節的分工如下：

| 主題 | 在哪一章 |
|---|---|
| 舾裝資料階層與元件概念 | [第 7 章](ch07_outfitting_zh-TW.reading.html) |
| 管路穿過牆或殼板的「開孔」協調 | 本章 27.2.6 概述，管路端見 [第 21 章](ch21_pipework_zh-TW.reading.html) |
| 艙室作為「空間」被計算、分析 | [第 25 章](ch25_space_fem_zh-TW.reading.html)（Space Management） |

本章只談 Room Design 這套**專屬的資料模型與操作**，不重複上述章節。

### 27.2.2 工作區與介面

從主選單 **Design > Room Design** 啟動。官方文件的說明是：Create 選單提供建立入口，Modify 選單依「目前元素（Current Element）」的情境啟用；Room Design 視窗可停駐（docking），並以**連結標籤**（link label）引導使用者走完某項工作的各步驟。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Room Design 工作區：標題列顯示 Outfitting - Room Design，左為 Design Explorer，右為 3D View

*圖 27-1　Room Design 工作區（Design > Room Design）。（AVEVA 官方文件截圖，僅供內部教學）*

Room Design 工具列把主要建模功能分成六組（文件僅說明六組，未逐一列名，詳見〔待核對〕），其中最常用的是兩個任務視窗：

| 任務視窗 | 用途 | 主要項目 |
|---|---|---|
| Main Layout Tasks（工具列 Layout） | 配置房間的基本骨架 | Create：Walls、Doors and Windows、Geometry for defined Room、Stairwell；Modify：Walls；Delete：Delete Selected Walls |
| Main Detailing Tasks（工具列 Detailing） | 細化與加料 | Wall details、Doors and Windows、Ceilings、Ceiling grids、Ceiling supports、Ceiling fittings、Floor coverings、Furniture, Fittings and Fixtures、Insulation Requirements |
| Room Design Main Data（Building Block Tasks） | 管理上層容器 | Building Block Tasks、Floor Elevation Tasks、Room Tasks |

> **專業提醒：** 「Geometry for defined Room」只有在目前元素是 `BLEVEL` 時才會啟用；若發現按鈕灰掉，多半是 Current Element 停在錯誤的層級。Wall 的「Enhance」（紅色高亮）對已有 Wall Detail 的牆不起作用，這是文件明載的限制，不是畫面故障。

### 27.2.3 資料階層

Room Design 的擁有者元素是 **Building Block（`BBLOCK`）**，官方說明其角色「類似 `SITE`」，是 World 之下的行政元素，用來把建築或艙室類元素分組。

```
WORLD
└─ BBLOCK        建築分塊（類似 SITE）
   ├─ BLEVEL     Building Level，即 Floor Elevation（樓層／甲板標高）
   │   └─ ROOM   艙室
   │       └─ DETGRP   Detail Group：CTWALL、CEILIN、FLRCOV、INSURQ、HANDRA、LADDER…
   ├─ OPENSP 開放空間   RSTARE 限制區域   RUTVOL 路徑體積
   ├─ STRWEL 梯井       DETGRP            BNDLIN 邊界線   AREADE 區域定義
```

| 元素 | 說明（依官方文件） |
|---|---|
| `BBLOCK` | 主要行政元素，包含 Room 與 Floor Elevation |
| `BLEVEL` | 代表模型中的主要標高，容納各樓層的 Room、`RSTARE`、`RUTVOL`、`OPENSP`、`REFDAT`、`BNDLIN`、`SPBSET`、`INVLST`，並可含 `STRWEL`、`DETGRP`、`AREADE`、`ACCSET` |
| `ROOM` | 定義艙室的設計準則與基本定義；其下的子元素類型與 `BLEVEL` 同一組 |
| `DETGRP` | 純行政分組，把外觀類似的實體（牆、門窗、地板覆蓋…）放在一起 |
| `RPATH` | General Routing Path：描述開放路徑或封閉邊界的通用機制（例如牆的路徑）；**官方文件寫明使用者資訊留待後續版本** |

> 〔公開版未收錄：AVEVA 官方產品截圖〕BLEVEL 之下可擁有的元素階層圖

*圖 27-2　`BLEVEL` 的資料庫階層：ROOM、RSTAR、RUTVO、OPENS、REFDA、BNDLIN、SPBSE、INVLST，以及 STRWE、DETGR、AREAD、ACCSE。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕ROOM 之下的元素階層圖

*圖 27-3　`ROOM` 的資料庫階層，子元素型別與 `BLEVEL` 相同一組。（AVEVA 官方文件截圖，僅供內部教學）*

> 文件在拼字上不一致：工作區頁寫 `STRWLL`，管理員指南寫 `STRWEL`。實際型別名請在你的專案中以 `Query` 或型別列表確認，標〔待核對〕。

### 27.2.4 建立 Building Block、Floor Elevation 與 Room

建議順序是由上而下：**BBLOCK → BLEVEL → ROOM → 牆 → 細部**。

1. 在 Room Design Main Data 選 Building Block Tasks → Create → Building Block。
2. 在 Building Block Tasks 視窗選 Create → Floor Elevation，建立 `BLEVEL`。
3. 在 Room Tasks 選 Create > Room，開啟 Create Room 視窗。
4. 填名稱、Description、Number，按 **Room Type** 開啟 Room Types 視窗選擇類型；選定並按 Apply 後，Function、Room Type 與 Occupancy 會自動帶入。
5. 設定 Floor height、Ceiling height、Room Offset（可圖形化點選 X、Y）與 Angle from Floor Elevation 的北向角度。
6. 展開 Design Criteria、Environmental Settings、Defaults 三個面板輸入準則。
7. 按 **Define Room geometry** 開啟 Define Room Boundary：選形狀、輸入尺寸與原點，或用 Pick Corner Points 圖形化選角點，再按 Define Boundary。
8. 勾選 Create ceiling、Create ceiling grid、Create floor covering（對應 `CEILIN`、`CLNPNG`、`FLRCOV`），最後按 **Create Room**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Room 視窗：名稱、Room Type、高度、Offset 與 Create options

*圖 27-4　Create Room 視窗（範例：Junior class／CABIN，Floor height 100 mm、Ceiling height 2400 mm、矩形 2000 x 2500 mm）。（AVEVA 官方文件截圖，僅供內部教學）*

| 建立方式 | 路徑 | 說明 |
|---|---|---|
| 一般房間 | Create > Room | 如上 |
| 標準艙室 | Create > Room > Standard | 從 Assembly 或既有 Room 複製出標準房間設計 |
| 補定義幾何 | Layout > Geometry for defined Room | 對「已建立但尚無幾何」的 Room 補上邊界，可用 Define points 或 Derive from graphics |
| 複製 | Create > Copy | 三種：Offset、Rotate、Mirror |

> **專業提醒：** Room 可以先建立元素、後定義幾何。若你用腳本或批次先佈好房間清單，之後再補邊界，應走「Geometry for defined Room」而非重建，才不會產生重複的 `ROOM`。

### 27.2.5 牆、天花、地板與細部

**牆（`CTWALL`，Constant Thickness Wall）。** 從 Main Layout Tasks 選 Create > Walls，在 Wall Definition Tasks 設定 Thickness、Height、Justification，並選擇定義方式：Derive from selection、Define points、Derive from graphics、Define Points Explicitly；Modify Points 可 Re-Pick、Insert Point after 或 Remove Point。按 Create wall 後產生 `CTWALL` 並進入 Wall Modification Tasks。

**牆細部（Wall Detailing）。** 從 Main Detailing Tasks 進入 Wall details，可對牆建立／修改／刪除三類細部：**Wall Panels**、**Wall Profiles**、**Wall Joiners**。窗格上方列出 Room Design Navigator 目前選取項目之下的所有牆。

**其他細部元素：**

| 元素 | 型別 | 入口與重點 |
|---|---|---|
| 天花 | `CEILIN` | 由支撐格柵與天花元件（板、燈具）組成。子功能包含 Ceiling Grid、Ceiling Tiles、Ceiling Profile、Ceiling Supports and Hangers、Ceiling Fitting；Profile 可複製 |
| 地板覆蓋 | `FLRCOV` | 可定義 Floor Layers（多層構造）與 Camber/Sheer Planes（船舶甲板的拱度與舷弧平面） |
| 隔熱需求 | `INSURQ` | 以 Profile Editor 定義覆蓋範圍 |
| 梯井 | `STRWLL`／`STRWEL` | 由 Layout 的 Stairwell 建立 |
| 門、窗 | `DOOR`、`WINDOW` | 見 27.2.6 |

每一類元素的視窗幾乎都是同一個模式：**Create／Modify（定義與幾何分開）／Delete**，並以 Confirm 訊息框確認刪除。這使 Room Design 容易學，但也意味著「定義」與「幾何」是兩個獨立的 Modify 動作，修改尺寸時別只改了其中一個。

### 27.2.6 家具、配件、門窗與貫穿孔

**建立位置（儲存區）。** 家具、配件與固定設備（`ELFITT`、`HVACFI`、`FIXTUR`、`FURNIT`）必須建立在某個 `ROOM` 或 `CTWALL` 之下。在 Furniture, Fittings and Fixtures - Element Tasks 視窗中，先以 **Graphical selection**（選畫面元素或框選）或 **Current Element** 產生可用的「儲存區」清單，選定後按 Edit Selected Element 才能建立、修改或刪除。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Furniture, Fittings and Fixtures - Element Tasks：列出可用儲存區 /Room_1 與 CTWALL

*圖 27-5　先選定儲存區（ROOM 或 CTWALL），才能進入元件的建立與修改。（AVEVA 官方文件截圖，僅供內部教學）*

**元件如何被選到：Room Design Specification。** Room Design 的選取並非直接指向 `SFIT`，而是指向 `GPART`；`GPART` 可透過 `CATREF` 或 `TMPREF` 指向目錄的 `SFIT` 或設計庫的樣板 `TMPL`，因此兩者可互換使用。選取表結構如下：

```
SPWL（Specification World）
└─ TABGROUP   一類元件（依 Purpose 區分）
   └─ CTABLE  子分類
      └─ TABITEM   以 PARTREFERENCE 連到 GPART；可含 TABQUESTION 供 Choose 表增加欄位
CTABLE 另有 TABHEA（表頭）→ TABHQU（表頭問題，Purpose 與 TABQUESTION 對應）
```

> 〔公開版未收錄：AVEVA 官方產品截圖〕目錄中的 Room Design 規格世界：Furniture、Door、Window、HVAC 等 TABGROUP

*圖 27-6　範例資料中 `SPWL` 之下的各類 `TABGROUP`。（AVEVA 官方文件截圖，僅供內部教學）*

| TABGROUP 類別 | Purpose |
|---|---|
| Furniture | `FURN` |
| Ceiling Tiles | `CLTI` |
| Doors | `DOOR` |
| Windows | `WIND` |
| Electrical Fittings | `ELFI` |
| Fire Protection Fittings | `FPFI` |
| HVAC Fittings | `HVFI` |
| Information Fittings | `INFI` |
| Wall Panels | `WLPN` |

要在選取視窗多出 TYPE、WIDT、HEIG 等欄位，需三個 `TABQUESTION`（`Tpurpose = TYPE／WIDT／HEIG`，`Tanswer` 為對應內容），並在 `CTABLE` 之下有三個 `TABHQU` 提供欄位標題。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Choose DOOR 視窗：TYPE、WIDT、HEIG 欄位來自 TABQUESTION

*圖 27-7　門的選取視窗（Choose DOOR），欄位由 `TABQUESTION` 與 `TABHQU` 產生。（AVEVA 官方文件截圖，僅供內部教學）*

**貫穿孔。** Room Design 可改自己的牆，但**不被預期直接修改船殼**；船殼板或牆板的開孔必須經 **Hole Management** 核准後才產生。形狀由目錄項目中負幾何（`NSEX` 下的 `SLOOP`）的 Purpose 決定：

| Purpose | 意義 | 用於 |
|---|---|---|
| `OPGE` | Outfitting Penetrating Geometry Element | 穿過 `CTWALL` 的開孔 |
| `HPGE` | Hull Penetrating Geometry Element | 不穿牆、但穿船殼板或 panel 的開孔 |

即使兩種開孔形狀相同，也必須各有一個 loop 並分別標 `OPGE` 與 `HPGE`（鋼構切口與壁板切口常不同）。樣板（`TMPL`）則改用 `EXTR`／`NXTR`（含 `LOOP`、`VERT`）作為穿孔輪廓，並在 `PORS` 之下建立 `PORI`，以其 `tarf` 屬性參照該 `LOOP`，Purpose 同樣標 `OPGE`／`HPGE`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕穿孔示意：鋼構切口與壁板切口

*圖 27-8　貫穿元件需分別定義「結構鋼切口」與「壁板切口」。（AVEVA 官方文件截圖，僅供內部教學）*

操作上，在 Select Opening 視窗按 **Managed Hole**，或在配件視窗選支援管理孔的配件後按 Create options 的 Managed Hole，選定壁板並確認，系統即建立一筆**孔關聯**，之後由 Utilities 選單的 Hole Management 管理。

> **專業提醒：** 文件明講「目錄必須以特定方式建立」才能走 Managed Hole。若你的專案目錄缺 `OPGE`／`HPGE` 的 `SLOOP`，按鈕會無法使用或孔形不正確；這屬於目錄管理員的工作，與 [第 8 章](ch08_catalogue_spec_zh-TW.reading.html) 的目錄概念相通。

### 27.2.7 報表與二次開發接點

Room Design 資料在同一資料庫，因此可用既有報表機制（見 [第 16 章](ch16_reports_integration_zh-TW.reading.html)）。官方文件說明資料模型兼顧「設計意圖」與「用於 MTO（材料統計）與生產的細節」，但**未提供專屬報表範本或 PML 範例**。

| 項目 | 文件依據 | 開發者做法 |
|---|---|---|
| 元素型別與階層 | 有（27.2.3） | 以型別名遍歷 `BBLOCK`／`BLEVEL`／`ROOM`／`DETGRP` |
| 規格選取結構 | 有（27.2.6） | 以 `TABGROUP` Purpose 查詢目錄 |
| 房間屬性名（面積、淨高、類型的 PML 屬性名） | 視窗欄位有名稱，屬性名未列 | 〔待核對〕在專案以 Query 對照 |
| `RPATH` 屬性與 API | 文件指向 *Software Customization*（本章未涵蓋） | 〔待核對〕 |
| Room Design 的 PML 物件／事件 | 無 | 〔待核對〕 |

## 27.3 Schematics：原理圖與 3D 的一致性

### 27.3.1 本節涵蓋什麼

官方 *Schematics* 章節有三份指南：

| 指南 | 用途 |
|---|---|
| Compare/Update | 在 Design、Schematic、Engineering 資料庫之間，或自 AVEVA Instrumentation、Electrical、P&ID 匯入的資料之間，比對並更新 |
| Schematic 3D Integrator | 原理圖物件與 3D 物件的 Compare、Build、Link |
| Tags | 以清單方式瀏覽與管理標籤資料、狀態、認領（claim）、匯出入、資料表 |

> **專業提醒：** 這裡的「原理圖」是**資料庫中的 schematic 物件**（型別以 `SC` 開頭，如 `SCEQUI`、`SCPLIN`、`SCVALV`）。圖面由 AVEVA Diagrams 或 Schematic Model Manager 匯入而來，Integrator 用 Diagram Viewer 顯示它們，但不負責繪圖。

### 27.3.2 原理圖資料類型

Schematic 資料庫有一組型別階層：Schematic Group、System、P&ID 圖紙，其下為 Equipment（含 Nozzle）、Pipeline／HVACline（含 Branch，Branch 之下有 Valve、Fitting、Instrument）、Offline Instrument、Cable。每個 schematic 物件都參照一張或多張圖，Integrator 靠這個參照決定物件可在哪張圖上看到。

> 〔公開版未收錄：AVEVA 官方產品截圖〕原理圖資料類型階層：Equipment、Pipeline/HVACline、Offline Instrument、Cable

*圖 27-9　原理圖資料類型階層。（AVEVA 官方文件截圖，僅供內部教學）*

| Schematic 型別 | 對應 3D 型別 |
|---|---|
| `SCEQUI`（設備） | `EQUI` |
| `SCSUBE`、`SCNOZZ` | `SUBE`、`NOZZ`（樣板內的 `NOZZ` 可與 `SCEQUI` 下的 `SCNOZZ` 跨層對應） |
| `SCPLIN`（管線）、`SCBRANCH` | `PIPE`、`BRAN`（一條 pipeline 可對多條 pipe） |
| `SCVALV`、`SCFITT`、`SCINST` | `VALV`、管件、`INST`（僅比對有名稱者） |
| `SCHVFI`（HVAC 管件） | HVAC 管件 |
| 電纜 | `CABLE` |

### 27.3.3 Integrator 三大功能

啟動：Integrator 選單 **Show**。畫面通常包含主表（Main Table）、子類型表（Subtype Table）、Diagram Viewer 與 3D 視圖。右鍵選單中的 **Compare**、**Build**、**Link／Unlink** 是三個核心動作。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Integrator 使用者介面：3D 視圖與 Diagram Viewer 並排

*圖 27-10　Integrator 的 3D 視圖與 Diagram Viewer 並排，顏色反映比對結果。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 作用 | 備註 |
|---|---|---|
| Compare | 比對連接關係、元件順序與屬性 | 依設定檔規則；輸出報表並為圖面與 3D 上色 |
| Build | 由原理圖資料在 3D 建立設備、管路、HVAC、電纜、離線儀表 | 建立後自動 Link；需 `Releaseto3dstatus` 已設（語法 `RESTAT 1`） |
| Link／Unlink | 將既有 3D 物件與 schematic 物件建立或移除關聯 | 適用已先行建模的情形 |

**Compare 的三個面向：** (1) 連接：設備的 nozzle、管路的 head／tail 與 connection reference；(2) 元件順序：儀表、閥、三通、大小頭是否漏掉或順序不同；(3) 屬性：例如 name 由 prefix、suffix、function 組成，bore 與 spec reference 必須相符。**Comparison Category** 可決定哪類差異（Names、Spec Attributes、Other Attributes）要被回報，以便聚焦。

**顏色代碼**（可設定，下列為典型設定）：

| 顏色 | 意義 |
|---|---|
| 綠 | 比對相符 |
| 紅 | 一邊有、另一邊缺（缺元件時，所缺的管段標紅；缺 nozzle 時，設備本體標紅） |
| 藍 | 連接錯誤 |
| 黃 | 屬性不符、匹配不明確（如同一閥匹配到兩處）、owner 錯誤 |
| 青（cyan） | 未比對 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Compare 結果：Diagram Viewer 與 3D 視圖皆以顏色標出缺少的閥

*圖 27-11　比對後圖面與 3D 同步著色：紅色代表缺漏，綠色代表相符。（AVEVA 官方文件截圖，僅供內部教學）*

Integrator 會另開一個專用 3D 視圖與獨立 drawlist，以免影響你既有的視圖。比對報表有 Summary 與 Details 兩個分頁；點 Summary 的某列會自動切到 Details 並過濾。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Integrator 比較報表 Summary 分頁：設備、nozzle、管線、閥的比對數量與錯誤

*圖 27-12　比較報表 Summary：例如 Valves 8 項中 6 項 Compared OK、2 項 Not Matched。（AVEVA 官方文件截圖，僅供內部教學）*

**接受差異。** 當 3D 與原理圖的細節層級不同（例如排氣、排放、儀表接口、焊接附件），可選擇：Accept Differences（連結物件的差異）、Accept Missing Element（缺的元素，若日後補上仍會匹配）、Disable Matching（永不匹配，例如 trunnion 用的三通）。這些動作可還原，且接受後需重跑比對才見效果；可能需要多輪。MDS trunnion 會被自動忽略。

**Build 的行為。** 以設備為例：依規則決定 `SITE` 與 `ZONE`（缺則依設定可建立，預設不自動建立）、建立 `EQUI`、`SUBE`、`NOZZ`／`ELCONN`、複製 spec 參照、套用位置與屬性，最後連結；若樣板已有 bore 相同的 `NOZZ`，會改為連結樣板內者並刪除自動建立者。管路則建立 `PIPE`、`BRAN` 與元件，無法唯一選型時彈出 Choose 表讓人選。

> **常見錯誤與注意事項**
> - **Build 按鈕灰掉：** 通常是 schematic 物件尚未 release to 3D。
> - **Build 時從 Diagram Viewer 開右鍵選單：** 會把 Current Element 切到 schematic 物件，Integrator 就無法在你預期的 `ZONE` 建立。應從 Main Table 的選單操作。
> - **一條 pipeline 想建成多條 pipe：** 目前不支援自動建；需先以 Pipework 建好各 pipe 再 Link（詳見 [第 21 章](ch21_pipework_zh-TW.reading.html)）。
> - **建立多條相連管線：** 官方建議先建主線，再建支線。
> - **訊息「Project Configuration Rules evaluation FAILED」：** 檢查該 `SCFITT`、`SCVALV`、`SCINST`、`SCHVFI` 是否有有效的 `GTYP`。
> - **設備先建、後才選 spec：** 不會再做 nozzle 自動匹配；先設 spec 再改 spec，則先前自動複製到樣板 nozzle 的連結與資料會被刪除。

### 27.3.4 連結資料與管理

Integrator 的連結存為獨立的 `CYMLNK` 物件：`deslnk` 指向 3D 物件、`schlnk` 指向原理圖物件、`cmpstatus` 記錄比對狀態；兩端物件皆有 `cmplnk` 指回該連結。`CYMLNK` 歸入 `CYMGRP`，統一置於單一 `CYMWRL`（link world）。另有偽屬性 `schlnk`、`deslnk`（兩端直接導覽）與 `cmpsts`（比對狀態描述）。`CYMLNK` 另有 `englnk` 指向工程物件，但 Integrator 本身不用。連結基數多為 0..1 對 0..1，**例外**是 schematic pipeline 可連多條 pipe、HVAC line 可連多條 HVAC。

管理要點：
- 所有 Integrator 使用者都須對單一 `CYMWRL` 有寫入權；12.1 起建議建立獨立的 Design Reference 資料庫放 link world，並讓其在所有 MDB 上為 current。
- 舊版（12.1 之前）link world 放在 Design 資料庫，可用 **Manage Links** 合併到新庫。
- Global project 需在各站點建立 link world 資料庫的 extract 並指定一個為 primary。
- 在 extract 資料庫中，Issue／Flush／Drop 有被連結參照的元素時，會自動包含連結物件；`INCFLU` 屬性可回傳參照該元素的連結。

### 27.3.5 設定檔與規則

規則存在專案設定檔，預設位於 Marine 執行檔資料夾，專案客製應複製到 Project Defaults 的 ModelManagement 資料夾，例如 `%SAMDFLTS%\ModelManagement\ProjectConfiguration.xml`；管理員用 **Project Configuration Explorer** 編輯。

| 設定區段 | 作用 |
|---|---|
| Project Defaults | Real Tolerance（預設 0.00001）、Distance Tolerance（預設 0.01）、單位 mm／inch、Can Create Site／Zone（預設 false）、是否比較法蘭／接頭／unions |
| Dictionaries | 鍵值對照，供公式使用 `Lookup()` |
| Spec Queries | 管路等級中可供 Selector 規則使用的選擇器（如 `STYP`） |
| Compare Colours | 各比對狀態的顏色：Accepted Difference、Connection Error、Difference、Error、Highlight、Missing、Not Compared、OK |
| Rules | Rule Set → Rule Group（Source Type）→ Create／Assign 規則 |
| Comparison Category、Categories | 控制哪些差異被回報 |

**規則概念：** 每個 Rule Group 針對一個來源（source）schematic 型別，如 `SCEQUI`；Create 規則決定要建／要比的 3D 型別（可用 `Variant(TEE, OLET, FLAN)` 列出多個可接受型別，Build 時取第一個）；Assign 規則設定或比較某屬性，並可指定 **Build Action**（`set`／`ignore`）、**Compare Action**（`match`、`matchorexceed`、`matchornotexceed`、`matchaskeyattribute`、`ignore`）與 **Mismatch Severity**（`criticalerror`、`error`、`warning`、`information`）。範例公式：`Format('/{0}-{1:D2}-EQUIP', Lookup('Discipline',FUNC of source), AREA of target)`。

> **專業提醒：** 文件警告 Build 時 `target` 尚未存在，以 `target` 為依據的名稱規則（例如以 owner 的 owner 組 ZONE 名）可能得不到預期結果。規則應盡量只依 `source`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Comparison Category 設定後的報表：標題含類別名，被忽略的差異不再以紅色回報

*圖 27-13　套用 Comparison Category 後的比對報表（標題含類別 `NoName:SpecOther`）。（AVEVA 官方文件截圖，僅供內部教學）*

### 27.3.6 Compare/Update：跨資料來源同步

Compare/Update 是產品通用能力，可在 Design、Schematic、Engineering 資料庫之間比對並更新，也能自 AVEVA Instrumentation、Electrical、P&ID 取資料。兩種範圍：

| 模式 | 範圍 | 能做的事 |
|---|---|---|
| Scope by Source | 來源庫中選定型別的全部物件 | 找出目標庫缺少的物件與差異，可自動新增缺漏物件並複製屬性 |
| Scope by Destination | 目前工作範圍（drawlist、目前圖、目前清單、目前選取或 Current Element） | 回報來源庫沒有的物件與差異，並可複製屬性 |

兩者**都不會刪除**物件，只能用結果觸發人工處理。預設比對以 Name 為準；pipeline 對 pipe 建議改用 key attributes（一對多）；已連結者優先於名稱規則。Design 的 Valves 與 Piping Specials 只比對有名稱的元素，且 **Compare/Update 無法新增**這兩類（插入位置須在 Pipework 應用中審慎決定）。多對一比對時，只允許 Link 與 Unlink。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Compare/Update 視窗：左為管線比對結果，右為 Side-by-Side 的屬性差異

*圖 27-14　Compare/Update：Accept 欄選取要更新的列，右側顯示 Schematic 與 Engineering 值的差異。（AVEVA 官方文件截圖，僅供內部教學）*

流程：選 Source → 登入（Instrumentation／Electrical／P&ID 需另登入專案）→ 選來源群組或設定（Configuration）→ 自動比對 → 用 Accept 選項（All Displayed／All Linked／All Matched／All Unmatched／None）或逐列勾選 → **Update Database**。

### 27.3.7 二次開發者怎麼接

以下皆有官方文件依據。

**Compare/Update 的 `CompareUpdate` 物件**（需先在介面設好 Options and Mappings）：

```pml
!run = object CompareUpdate()
!run.selectEngineering()
!run.compareEquipment()
!run.acceptAllDisplayed()
!run.updateLink()
```

主要方法：`selectDesign()`／`selectSchematic()`／`selectEngineering()`、`compareEquipment()`／`compareLines()`／`comparePipes()`／`compareInstruments()`／`compareValves()`／`comparePipingSpecials()`、`compare(STRING)`、`owner(STRING)`、`acceptAllDisplayed／Linked／Matched／Unmatched()`、`updateLink()`、`updateUnlink()`、`export(elementsFile, attributesFile)`（輸出 csv）。Instrumentation、Electrical、P&ID 整合**不支援命令列**，僅能互動。

**Integrator 物件**（先 `!!integratorInit()`）：`build`、`compare`、`link`、`unlink`（字串或陣列；有重名時用參照如 `=123/45678`）、`projectConfigurationFile`、`getConfigurations`、`configuration`、`compareColours／compareCategory／compareRuleset`、`setReportVisible(false)`、`setReportPath(path)`、`openReport()`、`setCompareAutoLinkMatches`、`setCompareAutoUpdateAttributes`、`validateLinks()`。`validateLinks()` 僅可在所有被連結物件所在資料庫皆為 MDB current 時使用。

文件另附完整範例巨集：用 `COLLECTION` 以 `diaref` 取某張圖上的 `SCEQUI` 與 `SCPLIN`，轉成字串陣列後呼叫 `!!integrator.compare(!comlist)`，並將報表輸出為 xml。

**連結與圖面物件。** 舊式 `mmTools`／`mmViewer`／`mmManageLinks` 需 `import 'MMservices'`；**12.1.SP4 起這三者不可用**，改用 `!!integrator.link／unlink／validateLinks` 與 `IntegratorManager`（`import 'IntegratorAddin'`），後者提供 `findOnDrawing`、`setColour`、`resetDiagramColours`、`closeDiagram` 等。由 3D 元素找圖面的範例：`!itemList[1] = !!ce.schlnk.ref.string()`。

**客製化回呼。** `IntegratorProjectHandler` 物件（位於 `pmllib\Integrator\objects`）提供 `BeginBuildCallback`、`PreCreateCallback`、`PostCreateCallback`、`EndBuildCallback`、`BeginCompareCallback`、`EndCompareCallback`，只可在標示「Start/End of customization」的區段內加入程式；其他 AVEVA 提供的 PML 修改可能破壞資料完整性。

**整合 UDA。** 要在比對時保存來源資料庫參照，需在 Lexicon 建立 Indexed text UDA，如 `pmg-sch-ai`、`pmg-sch-ae`、`pmg-design-ai`、`pmg-design-ae`（長度 50，掛在 `EQUIPMENT`、`CABLE`、`INSTRUMENT` 等型別）。

**HVAC 對照表。** HVAC build 讀 `HVACStypeTable.xml`（先找 `%<proj>dflts%\modelmanagement`，再找 pdmsexe），可依公司需求修改。

| 想做的事 | 建議接點 |
|---|---|
| 夜間排程比對並輸出報表 | `integratorInit()` + `compare(array)` + `setReportPath`（需確認無圖形模式下的限制，〔待核對〕） |
| 在 Build 前後套公司規則 | `IntegratorProjectHandler` 的 `PreCreate／PostCreate` |
| 報表中顯示對應的 schematic 名稱 | `schlnk` 偽屬性（官方稱可用於報表與交付物） |
| 清理死連結 | `validateLinks()` |
| 讀 Room Design 資料 | 見 27.2.7，目前無文件依據 |

## 27.4 本章小結

- Room Design 把艙室配置分成 `BBLOCK → BLEVEL → ROOM → DETGRP` 四層，牆、天花、地板覆蓋等外觀元素放在 `DETGRP`；家具與配件則建在 `ROOM` 或 `CTWALL` 之下。
- 元件選取透過 `SPWL → TABGROUP → CTABLE → TABITEM → GPART`；`TABGROUP` 的 Purpose 決定在哪個視窗出現。
- 船殼與牆板開孔須經 Hole Management 核准；目錄需有 `OPGE`／`HPGE` 兩種 loop。
- 原理圖不是圖面檔，而是資料庫物件；Integrator 提供 Compare、Build、Link 三種動作，以 `CYMLNK` 保存關聯。
- 差異可被「接受」或以 Comparison Category 過濾，但不是修好；兩種做法的目的不同。
- Compare/Update 不刪除物件，且對 Valves／Piping Specials 不能新增。
- 二次開發的文件依據集中在 `CompareUpdate`、`integrator`、`IntegratorProjectHandler`；Room Design 沒有 PML 依據，一律需實測。

## 27.5 練習題／自我檢核

1. 畫出 `BBLOCK`、`BLEVEL`、`ROOM`、`DETGRP`、`CTWALL` 的階層，並說明為何 `DETGRP` 是純行政元素。
2. 在 Create Room 視窗中，哪些欄位會在選了 Room Type 之後自動帶入？「Create ceiling grid」勾選後，產生哪個型別？
3. 為什麼門的選取視窗可能缺少 WIDT、HEIG 欄位？需要補哪些元素？
4. 說明 `OPGE` 與 `HPGE` 的差別，以及為何兩個形狀相同也要各做一個 loop。
5. Integrator 的 Build 按鈕灰掉，列出兩個可能原因。
6. 某 pipeline 在 3D 被拆成三條 pipe，應該用什麼方式比對？能不能用 Compare/Update 新增或更新這些 pipe？
7. 寫出一段巨集大綱，比較某張圖上所有 `SCEQUI` 並將報表輸出到檔案。
8. 在 12.1.SP4 環境中，`mmViewer.findOnDrawing` 要改成什麼？

## 27.6 〔待核對〕彙整

1. Room Design 工具列六組功能的完整名稱與順序（文件只列出其中部分頁面）。
2. `STRWLL` 與 `STRWEL` 哪一個是實際型別名。
3. Room 的面積、淨高、Function、Occupancy 等屬性在 PML 中的實際屬性名。
4. `RPATH` 的屬性、API 與在 `CTWALL` 中的使用方式（文件指向 *Software Customization*）。
5. Room Design 是否有 PML 物件、事件或 Add-in 擴充點。
6. Room Design 專屬報表範本與 MTO 輸出方式。
7. Integrator 在無圖形模式下可用的功能範圍（文件僅提到 `openReport()` 不可用於 non-graphics）。
8. Schematic Model Manager 與 AVEVA Diagrams 在 Marine 12.1 實際授權與安裝情況（文件僅在相容性頁面提及）。
9. Tags 模組與 Integrator 在本公司專案的使用範圍（本章只概述，未逐頁讀取 Tags 內容）。

## 27.7 取材範圍與限制

本章依 *Room Design*（約 149 頁）與 *Schematics*（約 283 頁）的總覽與關鍵子頁撰寫，Tags 指南僅依目錄概述。圖片取自官方文件，均已預覽確認主題相符。
