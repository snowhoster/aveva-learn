# 第 26 章　電纜設計與多專業支撐：Cable Design 與 Multi-Discipline Supports

> 管路、通風與結構之外，船上還有一大類「看不到卻處處要走」的系統：電纜。電纜要沿著預留好的通道走，通道要有橋架（Cable Tray）承載，橋架、管路與風管又都需要支撐（Support）固定在鋼構上。**這一章把兩件事放在一起看：先在 Cable Design 預留空間、鋪橋架、為電纜佈線；再用 Multi-Discipline Supports（MDS）為管路、橋架與風管設計共用的支撐。**
>
> 對二次開發者而言，電纜與支撐是典型的「跨專業資料」：電纜長度、填充率、橋架材料表、支撐清單與健康檢查報表，都需要同時讀到電氣、管路與結構的資料，也最容易在設計尚未收斂時讀到過期結果。
>
> **資料可信度：** 本章操作流程、視窗與選單名稱、元素型別（如 `CWAY`、`CWBRAN`、`CTMRL`、`RNODE`、`RATTA`、`POINTR`、`STRU`、`SCTN`）與預設檔名，取自 AVEVA Marine 12.1 官方離線文件的 *Cable Design* 與 *Multi-Discipline Supports* 兩大章節；後者含管理員、自動出圖、客製與使用者四本手冊，本章以使用者手冊為主，其餘僅取概要。文件原為 PDMS／E3D 時代的使用者指南，部分頁面保留舊名，本章照原樣保留。官方文件是操作手冊，**幾乎沒有 PML 指令或程式範例**，因此「二次開發者怎麼接」只在文件提到屬性、元素或檔案名稱時才寫，其餘標〔待核對〕，需在你們的版本與訓練專案實測。Cable Design 原文以 Cabling System 稱呼，其「Cableway」官方機器翻譯為「索道」，本章統稱「電纜通道」。

## 26.1 學習目標

讀完本章，你應該能夠：

1. 說明 Cabling System 的三大部分（Cableway、Cable、Cable Tray Material）與先後順序。
2. 畫出電纜資料階層 `ZONE → CWAY → CWBRAN → CTMRL → 橋架元件`，並說明 `CNODE`、`RNODE`、`RATTA`、`POINTR` 的角色。
3. 設定 Cabling Application Defaults，說明規格如何向下層層繼承（cascade），以及 Storage Area 為何要求 Zone 的 Purpose 為 `CABL`。
4. 依步驟建立 Cableway 與 Cableway Branch，並說明 Head／Tail 的定位方式與 Orthogonal Route。
5. 說明橋架材料的建立與鋪設（Dressing）：Preliminary、Template、Explicit 三種方式。
6. 建立電纜並以 Automatic、Define Route、PRP、Manual、Free Route 五種方式佈線，並解讀 Routing Status。
7. 使用 Fill Level Check 判讀綠／黃／紅，並說明 Fill Check Utility Allowance 的作用。
8. 說明 MDS 支撐的設計流程、三種建立方式（Cursor／Clearance／Dimensions）與 Integrity Checker。
9. 區分 MDS 的標準框架（Framework）、Ancillary、Hanger、Trunnion、Special、Preliminary Support，並知道哪些需要管理員客製。
10. 說明 MDS Reports 與 Health Check Utility 在交付前的用途，並指出各階段二次開發者可接的資料。

## 26.2 全貌與前置條件

### 26.2.1 兩個應用程式的分工

| 項目 | Cable Design（Cabling System） | Multi-Discipline Supports（MDS） |
|---|---|---|
| 所屬 | AVEVA Outfitting 套件中的模組 | Design 內以 `Design > Multi Discipline Supports` 進入 |
| 服務對象 | 電纜、電纜通道、橋架 | 管路、橋架（含管路型橋架 `BRAN` 與 Cabling System 的 `CTRAY`）、風管 |
| 核心資料 | `CWAY`／`CWBRAN`／`CTMRL`／電纜 | `STRU`／`FRMW`／`SCTN`、Ancillary（`ATTA`） |
| 典型輸出 | 電纜長度、填充率、橋架材料 | 支撐清單、Isometric 材料項、支撐圖 |
| 常見使用者 | 電氣設計 | 管路、結構、通風設計與支撐管理員 |

整體順序是：**先預留通道，再放橋架與電纜，最後為所有專業統一設計支撐。** 舾裝總覽見 [第 7 章](ch07_outfitting_zh-TW.reading.html)；管路中的管支架（`REST`／`HANG`）見 [第 21 章](ch21_pipework_zh-TW.reading.html)；支撐所依附的鋼構見 [第 22 章](ch22_structures_zh-TW.reading.html)。本章不重複這些內容，只談電纜與 MDS 新增的部分。

> **專業提醒：** 官方明說電纜設計使用者指南是為「熟悉電纜設計實務」的使用者而寫。本課程不教電氣設計（負載、壓降、線徑選擇），只教軟體如何承載這些決定。

## 26.3 Cable Design：概念與資料階層

### 26.3.1 三個部分與流程

官方把應用程式分成 Cableways、Cables、Cable Tray Material 三部分：

1. **Cableway** 在 3D 建模早期建立，用來在模型中預留空間，供電纜與橋架使用。
2. **Cable** 從目錄（Catalogue）選取，可選擇性連接設備，再沿 Cableway 佈線。
3. **Cable Tray Material** 自動或手動加到 Cableway 上；也可以先做初步鋪設（Preliminary Dressing）。

電纜也可以來自電氣系統的電纜圖（cable diagrams）；與 AVEVA Instrumentation and Electrical 的整合，官方在 Import Cables 下僅提到 `Display > Compare/Update` 這個應用，細節請見該產品手冊〔待核對〕。

### 26.3.2 元素階層

與所有專業相同，元素必須依嚴格順序建立，共用的是 `WORLD`、`SITE`、`ZONE`。電纜專屬元素如下：

| 元素 | 角色 | 備註 |
|---|---|---|
| `CWAY` | Cableway，預留一段空間 | 建立後預設不顯示於 3D 視圖 |
| `CWBRAN` | Cableway Branch，所有其他佈線元素的起點 | 必須在 `CWAY` 之下；有 Head／Tail |
| `CNODE` | Control Node，空間中的一個點，作為早期佈線輔助 | 可位於 `ZONE` 或 `CWAY` 之下 |
| `RNODE`／`RATTA`／`POINTR` | 路徑節點、路徑附著點、路徑點 | 官方描述電纜的 `POINTR` 構成路徑（`RPATH`） |
| `CTMRL` | 橋架材料主元素 | 每個 `CWBRAN` 只能有一個 |
| 橋架元件 | Straight、Bend、Riser、Tee、Cross、Reducer | 在 `CTMRL` 之下 |
| 電纜 | 參照電纜規格，含 Start／End 參照 | 預設存於 Purpose 為 `CABL` 的 Zone |

> **專業提醒：** 若工具列按鈕全部灰掉，或出現錯誤訊息，多半是目前位置不在正確階層（例如不在適當的 Zone 之下），不是軟體壞了。

### 26.3.3 Cabling Application Defaults

進入應用程式時會自動顯示 `Cabling Application Defaults`，之後可從 `Settings > Cabling Defaults` 再開。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Cabling Application Defaults 視窗，含儲存區、電纜資料、規格與電纜通道尺寸

*圖 26-1　Cabling Application Defaults：儲存區、超長、近接距離、填充檢查與自動佈線準則。（AVEVA 官方文件截圖，僅供內部教學）*

| 區塊／欄位 | 官方描述 |
|---|---|
| Storage Areas | 決定 `CableWay` 與 `Cable` 元素存放的位置；清單只列出 Purpose 為 `CABL` 的 Zone，沒有就請系統管理員處理 |
| Cable Data | Excess Lengths（Head／Tail 的超長）與 Proximity Distance（距起點多遠開始尋找通道入口） |
| Fill Check | 勾選則自動檢查填充率 |
| Specifications | 規格決定目錄中哪些元素可用；可設在 Cableway 或 Branch 層級，下層自動沿用，除非更改 |
| Cableway Data | 通道尺寸；`Create Ends RNODEs` 可在 Branch 兩端自動建立 `RNODE` |
| Fill Check Utility Allowance | 填充檢查換色的門檻，必須大於 1 |
| Auto Routing Criteria | `minimize Free Route` 取最近的進出點；`minimize Total Length` 在 `RANEQUIP` 範圍內找總長最短（不一定用最近點） |

### 26.3.4 Cabling System Toolbar

進入後左上角自動出現 Cabling System 工具列，按鈕包括：Create Cableway、Create Cableway Branch、Modify Cableway Branch、Create Cable、Modify Cable、Create Cableway Material、Modify Cableway Material、Copy Cable、Copy Cableway Element。多數操作會再開出「Tasks」視窗當作任務中樞（task hub），引導下一步。

## 26.4 Cableway 與 Cableway Branch

### 26.4.1 建立 Cableway

1. 在 Design Explorer 選取適當的 Zone，按 Create Cableway，開啟 `CableWay Create Tasks`。
2. 輸入 Cableway Name（可按 Autonaming 圖示）、Description、Function、Purpose。
3. 按 Create CableWay，Design Explorer 出現新元素，並接著顯示 `CableWay Branch Create Tasks`。

選用的 `Control Node`（`Create > Control Node`）可先在空間放點，用座標或 Pick Position 定位，日後讓 Route Node 連到它，當作早期佈線的輔助。

### 26.4.2 建立 Cableway Branch

> 〔公開版未收錄：AVEVA 官方產品截圖〕CableWay Branch Create Tasks 視窗，含 Volume Size、Branch Head／Tail 與 Orthogonal Route 設定

*圖 26-2　CableWay Branch Create Tasks：Attributes、體積尺寸、Head／Tail 連接與直交路徑。（AVEVA 官方文件截圖，僅供內部教學）*

此視窗為所有 Branch 任務的中樞。Attributes 區的欄位：

| 欄位 | 說明 |
|---|---|
| Beta Angle | 通道的旋轉角 |
| Bend Radius | 鋪設橋架後套用的彎曲半徑 |
| Open Direction | 鋪設後開口側方向 |
| Justification | 對齊方式，下拉選取 |
| Cable Excess (%) | 電纜在通道上下垂所需的裕度 |
| Maximum Fill (%) | 最大填充率，軟體依橫斷面積自動計算；若設得低於目前填充率會出現警告 |
| Current Fill Level (%) | 目前填充率（唯讀） |
| Interference／Standard Iclass | 干涉等級；可 `Load` 資料庫的干涉值 |
| Cable Route Rule | 控制哪種電纜可走此通道，例如 `IClass EQ POWER` |

Select Volume Size 區選 Rectangular 或 Circular 並輸入寬高。**Head／Tail 的位置**由 `Connect From` 決定：

| 選項 | 行為 |
|---|---|
| X0 Y0 Z0（預設） | 相對世界原點以座標與偏移（Offset By）定位 |
| Head／Tail of Cableway Branch | 接在既有 Branch 的 Head 或 Tail，需 Pick `CWBRAN` |
| Branch Off | 從既有 Branch 的某線段岔出 |
| Route Attachment Point | 接到某個 `RTTA`（路徑附著點） |
| Copy Tail／Pick Head Position | 複製尾端座標／以 3D 視圖點選 |

可勾選 Lock 鎖定座標；勾選 Create Orthogonal Route 並選 Direction Sequence（如 E-N-U），建立後 Branch 會沿直交路徑連接 Head 與 Tail。官方提醒：**Direction Sequence 與 Open Direction 必須相容**（例如 Open Direction 為 U，搭配 U-N-E 或 U-E-N 可能無效）。

> **專業提醒：** Cableway 的定位是「預留空間」。越早建立，結構與管路專業越能避開；但此時尚無橋架，尺寸要用預估值，後面可由 Fill Level 回頭修正。

### 26.4.3 修改與整理

| 作業 | 入口 | 重點 |
|---|---|---|
| Modify CableWay | `Modify > Cableway` | 可改 Description／Function／Purpose；更細的改動回 Branch 視窗；可 Delete Cableway |
| Modify Cableway Branch | 工具列 | 同建立視窗；`List Associated Cables` 看有哪些電纜走過 |
| Modify Branch Elements | 選 Route Point／Route Node／Route Attachment Point | 可改屬性依元素而異 |
| Move Cableway Segment | `Modify > Cableway Segment` | 以 Offset／Increment／Align 移動線段；可勾 Re-route Cables、Re-dress Materials、Display Hole Manager；`Show Issues` 列出受影響的附著點 |
| Copy Cableway Elements | `Create > Copy > Cableway Elements` | 可複製 Zone、Cableway、Branch、含電纜的 Cableway；複製連接電纜時，新電纜不會與設備建立關聯 |
| Split／Merge／Connect Branches | `Utilities` 選單 | 在點上或平面上分割；Merge 與 Connect 需依提示依序選兩條 Branch 並確認 |
| Data Checker | `Utilities > Data Checker` | 檢查 Cableways、Trays、Penetrations；細節見 Data Checker Utility User Guide〔待核對〕 |

## 26.5 橋架材料與鋪設（Dressing）

### 26.5.1 CTMRL 與橋架元件

佈好的 Cableway Branch（不論有無電纜）可以鋪上橋架材料。預設規格決定用於預留空間的橫斷面，也就決定橋架材料。流程如下：

1. 選取目標 Branch 為 CE。
2. `Create > Material > Main`，開啟 `Create Material`，輸入名稱與規格，建立 `CTMRL`（**每個 `CWBRAN` 只能一個**）。
3. 設定 First Gap（每個元件之前的間隙）、Intermediate Gap（相鄰直段間）、Last Gap（元件之後）、Tier Heights（層高），寬高預設取通道尺寸。

單一元件（Straight、Bend、Riser、Tee、Cross、Reducer）以 `Create > Material > Elements` 建立；`Create` 視窗兼具建立與修改，官方只詳述預設的 Create Straight，其他元件比照。

### 26.5.2 三種鋪設方式

> 〔公開版未收錄：AVEVA 官方產品截圖〕Dress using Templates 視窗，含 Dimension Options、整段／部分鋪設與 Remove Dressing

*圖 26-3　Dress using Templates：自樣板 Zone 載入尺寸，整段或部分鋪設橋架。（AVEVA 官方文件截圖，僅供內部教學）*

| 方式 | 入口（Modify Material） | 適用情境 |
|---|---|---|
| Preliminary：使用者定義尺寸 | Dimensions defined by user | 設計初期快速鋪設，尺寸自訂 |
| Preliminary：依 Branch 填充率 | Dimensions based on branch fill levels | 讓橋架寬度反映實際電纜量 |
| Dress using Templates | Other Dressing options | 自 `Load From Template Zone` 載入樣板；可指定直管長度、`Dress Backwards`；可整條或部分（Picked Point、Straights between Picked Components 等）鋪設 |
| Explicit Dressing | Other Dressing options | 逐一建立元件 |

要移除時用 `Remove Dressing`：From Branch、From Segment、From Point，或僅移除 All Straights。

### 26.5.3 Cable Tray Volume：從既有橋架反推通道

若橋架已存在（例如由管路型橋架 `BRAN` 建立），可用 `Utilities > Cable Trays Volumes` 反向建立 Cableway 體積。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Cable Tray Volumes 視窗，Cable Tray List 頁籤列出橋架及其 Head／Tail 連接

*圖 26-4　Cable Tray Volumes：自橋架建立對應的 CWAY／CWBRAN 體積。（AVEVA 官方文件截圖，僅供內部教學）*

官方描述的邏輯：先檢查橋架寬度變化與 Tee／Cross 處的方向變化（這些處需要新 Branch）；每個橋架新建一組 `CWAY`／`CWBRAN`；每個彎頭（BEND／ELBOW）在 Branch 的 `RPATH` 加一個 `POINTR`；每個 Tee 或 Cross 在 Branch 的 `CONSEQ` 之下建一個 `RATTA`；新 Branch 的 `VWidth` 取自第一個元件的 `ABORE` 屬性。

使用前須在目前位置位於 Zone 或其下，且**必須已有 Purpose 設為 `TBAS` 的 Association Group**，用來存放舊橋架與新橋架元素的關聯；不存在時系統會提示並開啟 Organize Association Store 供建立。

> **專業提醒：** 這是少數「由現成幾何反推資料」的功能。反推出的體積不等於設計意圖，使用後仍須檢查填充率與連接。

## 26.6 電纜建立與佈線

### 26.6.1 建立電纜

`Create > Cable` 開啟 `Create Cable`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Cable 視窗，含 Basic Data、Specification、Start 與 End 區塊

*圖 26-5　Create Cable：名稱、Excess Lengths、規格、起訖設備。（AVEVA 官方文件截圖，僅供內部教學）*

| 欄位 | 說明 |
|---|---|
| Name／Primary System | 唯一名稱（可 Autonaming）；可指派所屬系統 |
| Fill Check | On／Off，預設 Off |
| Excess Lengths (mm) | 依序輸入 Head、Head extra、Tail、Tail extra，用於計算電纜切割長度 |
| Proximity Distance | 距 Head 多遠內開始尋找通道入口 |
| Routing Status | 0 Un-routed、1 Routed、2 Routing Failed、3 Partially Routed、4 Partially failed、5 Manually Routed |
| Cable Length／Cable Free Length | 總長（含超長）／在通道外自由佈線的長度 |
| Choose Cable | 開啟 Choose Cable，從 Table 下拉選電纜種類，可看 Properties 與 Plot File |
| Start／End | 以 `Pick` 選設備、閥或接點（Equi／Valve／Pcom／Elconn），或用 `List Equipment`、直接輸入 Reference |

**若未選電纜規格，填充率計算會不準確**，建立時會跳出警告。電纜建立後不會立即顯示於 3D，佈線後才出現。

### 26.6.2 五種佈線方式

`Modify Cable` 視窗兼作佈線入口：

| 方式 | 前提／行為 | 何時用 |
|---|---|---|
| Automatic Routing | 起訖已知；沿所選 Zone 內相連的通道走最短路徑，並直交接到最近的附著點；以 `AutoRoute Cable` 執行 | 絕大多數電纜 |
| Define Route | 指定 Cableway Branch 的進入點與離開點，`AutoRoute from Entry to Exit Point`；可勾 `Auto Head/Tail Free Route` | 需控制走哪條通道 |
| Define Route Through PRPs | 設定必須經過的 Preliminary Route Points | 必經某處（例如貫穿點） |
| Manual Route Cable | 逐段指定同一 Branch 上的進出點，以 Append／Insert（Before／After）／Modify 增修電纜段 | 自動失敗或需精確控制 |
| Free Route | 在通道外用 Pick 定點，產生 `POINTR` | 通道端到設備的最後一段 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Route Through PRPs 視窗，可調整必經路徑點順序

*圖 26-6　Route Through PRPs：以清單排序控制電纜必須通過的路徑點。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Manual Route Cable 視窗，含 Existing Cable Segments 與 Free Route 工作

*圖 26-7　Manual Route Cable：逐段建立、插入、修改與刪除電纜段，並處理 Head／Tail Free Route。（AVEVA 官方文件截圖，僅供內部教學）*

要點：

- **Define Specific Cableway Zones**：未指定時，系統會使用 `WORLD` 下所有 Zone 的通道，大型專案會非常慢，官方明確提醒。
- 起點位置若與進入點不符，電纜只會「部分佈線」，需以 Head Free Route／Tail Free Route 補完；`Delete Free Routes` 可移除兩端的自由段。
- `Modify Routing Status` 可在佈線後手動改狀態，改前會有確認視窗；`UnRoute Cable` 取消佈線並從 3D 移除；`Delete Cable` 刪除電纜。

### 26.6.3 複製、匯入、匯出與批次佈線

| 功能 | 入口 | 重點 |
|---|---|---|
| Copy Cable | `Create > Copy > Cable Elements` | 可選是否複製 Spec Ref、Start Ref、End Ref 與 Route Path；`Head Free Route`／`Tail Free Route` 讓某一端重新自由佈線；複製數大於 1 時不能指定單一新名稱；可 `Edit > Undo` |
| Import Cables | `Utilities > Import Cables` | 讀取電纜參照集資料檔，經 Spreadsheet Import 視窗載入；`Load All Data` 或 `Load New Data` |
| Export Cables | `Utilities > Export Cables` | 匯出到 Excel；須在 Site 或 Zone 層級選取電纜 |
| Cable Data | `Utilities > Cable Data` | 依 Zone 載入全部或僅未佈線電纜，一次對多條電纜 `Route Selected Cable(s)` 或 `Unroute Selected Cable(s)`；另有 Cableway Zones、Route Information 頁籤 |

## 26.7 填充率檢查與資料檢查

`Utilities > Fill Level Check` 以格子顯示每個 Branch Point（HEAD 到 TAIL）的填充率。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Fill Level Check 視窗，Branch Points 格子以綠黃紅標示各點填充率

*圖 26-8　Fill Level Check：Load From 選範圍，格子顏色對應 Fill Check Utility Allowance。（AVEVA 官方文件截圖，僅供內部教學）*

| 顏色 | 意義 |
|---|---|
| 綠 | Branch 最大填充率大於該點填充率 |
| 黃 | 該點填充率已進入「最大填充率減 Allowance」的警戒區 |
| 紅 | 該點填充率超過 Branch 最大填充率 |

舉例：最大填充 75%、Allowance 為 5，當某點進入 5 之內即提示。右鍵可 Navigate to、List of Cables、Export to Excel；`Explain Fill Levels` 開啟說明視窗；`Connections` 窗格顯示該點是否有有效連接。

**判讀順序建議：** 先看紅格，用 List of Cables 找出走過該點的電纜，再決定是改走別的通道、加寬橋架，或調整 Maximum Fill。

## 26.8 報表與出圖：官方範圍

Cable Design 章節本身**沒有獨立的報表與出圖小節**。從文件能確認的輸出是：各種清單視窗的 `Export to Excel`／`Print Preview`、Cable Export、Fill Level Check 匯出，以及橋架材料元素本身（可由目錄與材料表機制取得，細節見 [第 8 章](ch08_catalogue_spec_zh-TW.reading.html)〔待核對〕）。電纜清單、電纜表（cable schedule）與出圖模板是否有預設版本，需在你們的版本實測；一般報表與圖面原理見 [第 16 章](ch16_reports_integration_zh-TW.reading.html) 與 [第 9 章](ch09_drawings_zh-TW.reading.html)。

## 26.9 Multi-Discipline Supports：概念

### 26.9.1 MDS 是什麼

MDS 讓使用者為管路、電纜橋架與風管建立支撐。它高度互動，並由管理員配置專案預設值與可用元件範圍。官方描述的兩大類：

- **標準框架（Framework）**：以結構型鋼組成、由樣板（template）驅動；預設樣板基於英國標準型鋼，可改配置為他國標準。
- **Ancillary**：附在管上的元件，如 U 型螺栓、焊接式滑座（Shoe）、錨定（Anchor）、滑動單元（Slip Unit）。橋架與風管的固定件（fixings）官方明說視為承包商責任，**不在 MDS 處理範圍**。

若標準樣板不合，要請管理員配置，或建為 Special（例如要在樣板外加一根構件），再以標準的 Beams and Columns 應用程式補上。

### 26.9.2 資料與管理員角色

| 項目 | 官方描述 |
|---|---|
| 目錄與規格 | 專案附 MDS 目錄；`/MDS` 規格含所有 Ancillary，`/MDF` 含標準框架的 `SREF` 附件，`/MDP` 含 Preliminary Support，`/RPAD-MDS-PLATE-MATERIAL` 含補強墊材料。**目錄與規格不得修改** |
| 使用者自訂 Ancillary | 另有 USER DEFINED 目錄（MDU 專案），僅 `PTSE`、`GMSE` 的部分元件可改 |
| 預設值 | 管理員在 PARAGON 資料庫的 DATASETS、預設檔與 Design 樣板資料庫設定；`MDS Admin Data` 表單修改 `/MDS/OPTION/DEFAULTS`，須 `Apply` 後再 `Save Work` |
| 結構樣板 | Site `/MDS/TEMPLATES`，每種標準支撐一個 Zone，其下最多 8 個結構樣板 |
| 吊架樣板 | Site `/MDS/HANGERS`，每種配置一個 Zone，每種尺寸以 `REST` 元件表示；附兩家供應商（GRINNELL、PSL）樣板，另三套廠商介面見 26.12 |
| 命名 | 預設用 `DES-SUPP-NAMES` 自動命名檔，可改用同前綴的其他檔 |
| 報表定義 | `MDS-REPORT-DEFS` 與 `MDS-REPORT-HEADINGS` 兩檔搭配，標題編號須一致 |

進入應用程式時，系統會測試 `/MDS/TEMPLATES` 樣板資料庫與 `/MDS`、`/MDF` 規格；缺少就無法進入，須請管理員把所屬資料庫加入你的 MDB。支撐宜存放在 Purpose 設為 `SUPP` 的 Zone（預設值），可建立多個 Support Zone 與 Hanger Zone。

> **專業提醒：** MDS 的標準支撐是「管理員先配置、設計者後使用」的模式。多數問題（找不到支撐類型、尺寸不對、命名不合）應先找管理員，而不是改目錄。

## 26.10 MDS 設計流程

### 26.10.1 官方的十個步驟

官方列出每個支撐的建立流程：選支撐類型；輸入名稱；建立基準附著點（datum atta）並選 Ancillary 類型；設定距離或位置；從清單選鋼構尺寸；以所需方式建立；選雜項選項；必要時選墊塊（packing）；完成（此時 Integrity Checker 自動執行）；最後執行 MDS Health Check Utility 做全面檢查。

### 26.10.2 建立表單

`Create > Multi Discipline Frame` 開啟 `Multi Discipline Frameworks`，依群組列出類型（L Brackets、Cantilevers/Posts、Pedestals、Frames、Braced Brackets、T Posts、Miscellaneous），分組由管理員在 MDS Structure Defaults 設定。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Multi Discipline Frameworks 表單，列出 L Brackets 群組的框架類型（XFT03 等）

*圖 26-9　Multi Discipline Frameworks：依群組選擇框架，名稱可自動產生，View 可預覽工程圖。（AVEVA 官方文件截圖，僅供內部教學）*

名稱可手動輸入或按 AutoName 圖示；`View` 顯示該類型的工程圖。表單也可由既有 Preliminary Support 轉換建立。

### 26.10.3 三種建立方式

| 方式 | 需要的資料 | 特點 |
|---|---|---|
| Create by Cursor | 在 3D 點選兩根與管路平行的鋼構 | 以兩者位置算出尺寸，並自動連接外部鋼構，尺寸存回供日後修改 |
| Create by Clearance | 只需點選一根構件（垂直於管路且在其上方） | 依預設淨空值計算；淨空取自各 Ancillary 標準的 PARAGON 預設，未設則取 `MDS Application Defaults`；`:MDSBUILDSTYL` UDA 決定框架 `INSIDE`（預設）或 `OUTSIDE` |
| Create by Dimensions | 手動輸入尺寸（如 Dimension 1 至 4） | 鋼構尚未建模時使用，可繼續工作；**不會**自動建立結構關聯 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕以 Create by Cursor 建立的支撐立面，標示基準管與三個附著點

*圖 26-10　Create by Cursor 的結果示意：依兩側鋼構位置決定框架尺寸，並可再加橫桿。（AVEVA 官方文件截圖，僅供內部教學）*

建立後可用工具列圖示修改：Add pipe／Add HVAC／Add rack（把另一條管、風管、橋架加入同一框架）、Add cross bar、Mirror framework、Align support，以及 Compensating Plates（補償板，適用 XFT03、04、07、08、09、10、11、13、14、15、17、24）、Reference Supports（把另一管上的既有 Ancillary 加入框架）、Add Packer、Create／Modify Connections。

### 26.10.4 完成檢查（Integrity Checker）

按 `OK` 完成時會自動執行：

| 結果 | 條件 |
|---|---|
| 訊息 | 墊塊間距大於 2 mm 但未超過容許值；Special 提示需建立鋼構 |
| 警告 | 鋼構超過樣板資料庫中為各構件設定的最大長度 |
| 錯誤（OK 失效，須修正） | 超過應用程式預設的最大墊塊距離；支撐附著點與橫桿重疊超過 `MDS Application Defaults` 的最大重疊值；Ancillary 尺寸（如 Shoe）超出 `MDS Ancillary Defaults` 的值；MDS 內使用的參照（如底板參照）已不存在 |

### 26.10.5 複製與重複

| 功能 | 說明 |
|---|---|
| Copy a Support | `Create > Support... > Copy`；**每個複製品都必須改名**，可指定份數與距離 |
| Repeat a Support | 把支撐從一條管重複到另一條；只適用獨立 Ancillary 與支撐框架，**不適用 Trunnion 與 Hanger** |

## 26.11 與管路、通風、電纜、結構的關係

### 26.11.1 對應表

| 專業 | MDS 如何接 | 注意 |
|---|---|---|
| 管路 | 以基準附著點掛在管（tube）上，Ancillary 檢查管徑、材料、保溫厚度、溫度、高程是否仍適用 | 管路改規格後，健康檢查會報告「Ancillary 對管不再有效」 |
| 電纜橋架 | 同時支援管路型橋架（`BRAN`）與 Cabling System 的 `CTRAY`；框架可用 Add rack 加入橋架 | 固定件不在 MDS 範圍 |
| 風管 | 以 Add HVAC 加入框架；Special 可為 HVAC 類型 | 風管 Special 的接頭與 `SCTN` 修改另有專頁〔待核對〕 |
| 結構 | 支撐的鋼構為 `STRU`／`FRMW`／`SCTN`；以 `SNOD`／`SJOI` 連接外部鋼構 | 須對外部鋼構有寫入權限；可能連到錯的 Pline，可用 Force Connect 指定 |

### 26.11.2 結構關聯（Structural Associations）

此功能完全仰賴標準 AVEVA 關聯資料庫 `MASTER/ASSOCDEFN`，必須存在於目前 MDB，官方建議自標準 MAS 專案以 FOREIGN 資料庫方式引入。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Design Explorer 顯示 MDS 支撐與 ASSOWL 下的關聯群組階層

*圖 26-11　MDS 支撐 `STRU`／`SCTN` 與 `ASSOWL` 下 `ASSOGP`／`ASSOC` 的對應階層。（AVEVA 官方文件截圖，僅供內部教學）*

- 以 Cursor 或 Clearance 建立並點選主結構時，**自動**在名為 `<sitename>-MDS-ASSOWL` 的 `ASSOWL` 下產生關聯。
- 以 Dimensions 建立時，既有 `ASSOC` 會被刪除（保留 `ASSOGP`），須以 `Create > MDS SCTN Association` 手動建立：先點 MDS 的 `SCTN`，再點主結構元素。
- 這使結構專業改梁時，有機會知道哪些支撐受影響；關聯管理另可用標準 Associations Manager 表單。結構面見 [第 22 章](ch22_structures_zh-TW.reading.html)。

> **專業提醒：** 要能追蹤「結構改了，支撐要不要跟著改」，就不能只用 Dimensions 建立而不補關聯。

## 26.12 標準支撐類型與客製

### 26.12.1 類型一覽

| 類型 | 入口與重點 |
|---|---|
| 標準框架 | 見 26.10；以樣板驅動 |
| Hanger（固定／可變） | 以供應商吊架元件目錄為基礎、樣板驅動；類型名含 T（Top）、M（Middle）、B（Bottom）前綴，如 T1 M2 B4 |
| Trunnion | 以標準設計，可附補強墊（如 XAT05，由彎頭切取，在 Isometric 列為額外材料）；為取得最佳顯示，官方建議 Holes On、Arctol = 1 |
| Branch Reinforcement | 如 XBR01，以一連串提示選取來定位 |
| Preliminary Support | 18 種，可轉換為框架、Ancillary、Anchor、Hanger、Guide、Stop、Slip Unit、Special、Spring、Trunnion、Vessel、Branch Reinforcement |
| Lighting Support | 專頁，可建立與修改〔待核對細節〕 |
| Special | 不符標準時建立；可為 Multi Discipline、Cable racking、HVAC 類型，不自動建立鋼構；編號是否唯一由 `MDS Admin Data` 控制 |

### 26.12.2 Hanger 的建立

> 〔公開版未收錄：AVEVA 官方產品截圖〕Fixed Hangers using MDS Interface 表單，列出 FH T1 M1 B1 等可用類型與篩選按鈕

*圖 26-12　Fixed Hangers 表單：可用類型清單與依型態篩選的按鈕列。（AVEVA 官方文件截圖，僅供內部教學）*

吊架表單有三種建立模式：**Create and Modify**（預設，建立後可修改、接受或取消）、**Create Once**（以最少按鍵連續建多個，可不同配置）、**Multi Create**（連續建立同配置，依管理員命名規則自動命名）。另提供三家廠商介面：Witch Hanger（Carpenter & Paterson）、PSDesigner（Pipe Supports Ltd.）、LICAD（Lisega）；使用標準樣板時，PARAGON 預設資料庫的 `MDSHANGIF` 關鍵字須設為 `Standard MDS`。

### 26.12.3 客製與出圖

客製屬管理員工作：框架樣板管理（Framework Template Administration）、專案設定、自動出圖（MDS Automatic Drawing Production）、MDS Support Standards、`MDS Structure Defaults` 等表單；這些由 *Customization*、*Automatic Drawing Production* 兩本手冊涵蓋，本章只確認其存在與入口，細節為〔待核對〕。自動出圖使用 Area Based ADP，一般 Draft 使用者只能利用管理員預先定義的 Template 與 Task 出圖；出圖原理見 [第 9 章](ch09_drawings_zh-TW.reading.html)。

## 26.13 報表、控制與健康檢查

### 26.13.1 MDS Reports

`Utilities > MDS Reports` 開啟 `MDS Reports Menu`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕MDS Reports Menu 表單，含 Output Format、Filter、報表清單與 Sorting and Totalling

*圖 26-13　MDS Reports Menu：選報表、輸出格式、過濾運算式與排序合計。（AVEVA 官方文件截圖，僅供內部教學）*

- 預設對整個 MDB 產生；按 `CE` 限定目前元素。
- 輸出格式有 screen、text、csv；後兩者寫入 `%MDSREPORTS%` 環境路徑。
- 報表清單由 `MDS-REPORT-DEFS` 決定，如 MDS Summary、Overall Index、Area、Bedplate Index、Trimmer Report、Data 等；管理員可增修。
- Extended Report 可加 Extra Run-time Filter Expressions（在 Filter 欄輸入有效運算式，例如圖中以 `spref`、`MDSsupptype` 篩選）、自訂標題、排序與合計。

另外，`Isometric Material List Control` 可決定哪些 Ancillary 或支撐框架排除於管路 Isometric 的材料表（可設為 Off，也可選擇以虛線繪出、有無標註）；`Data Access Control` 須專案啟用後，才依 Role、Scope、ACR 控制可操作的範圍。

### 26.13.2 MDS Health Check Utility（HCU）

> 〔公開版未收錄：AVEVA 官方產品截圖〕MDS Health Check Utility 視窗，含輸出格式與 Supports 清單

*圖 26-14　MDS Health Check Utility：載入支撐後產生檢查報表。（AVEVA 官方文件截圖，僅供內部教學）*

因為 MDS 橫跨結構、管路、電氣、風管四個專業，其中任一專業都可能不小心破壞支撐；HCU 就是用來找出這類問題。檢查項目包括：

- **Ancillary**：對管路是否仍有效（Bore、Material、Insulation thickness、Temperature、Elevation），`SPREF`、Guide 等參照是否有效，是否有未知參照。
- **Supports**：支撐類型是否存在、`SREF` 與 DATUM 是否存在、`SPREF` 是否有效；另分別檢查 Hanger、Trunnion 與群組。

操作：`Utilities > MDS Support Health Check`，以 `Add` 的 All 或 CE and Below 載入支撐（群組算一個支撐），選 text file／csv file／screen 輸出。無法載入的支撐會寫入暫存的 load list 檔（位於 `%pdmswk%`），可用 `Load Errors Only` 檢視；文字報表預設目錄為 `%projcodeinfo%`，若不存在則用 `%pdmswk%`。

## 26.14 二次開發者怎麼接

下表彙整本章可確認的接點。官方文件幾乎沒有 PML 範例，因此欄位只寫文件出現過的名稱，其餘為〔待核對〕。

| 目標 | 文件有依據的接點 | 待驗證 |
|---|---|---|
| 讀電纜通道與填充率 | 元素 `CWAY`、`CWBRAN`；Branch 屬性畫面有 Maximum Fill、Current Fill Level；填充檢查結果有 `FLEVEL` 欄名 | 對應的 PML 屬性名稱、取值方式〔待核對〕 |
| 讀電纜佈線狀態與長度 | Routing Status 0 至 5、Cable Length、Cable Free Length；路徑由 `RPATH` 下的 `POINTR` 組成 | 屬性縮寫、`EXTGEO` 內容〔待核對〕 |
| 批次佈線 | Cable Data 視窗支援多條電纜 `Route Selected Cable(s)` | 是否有 PML 物件或指令可呼叫〔待核對〕 |
| 電纜資料交換 | Import Cables（Spreadsheet Import，每欄對應一個屬性）、Export Cables 輸出 Excel | 檔案欄位規格〔待核對〕 |
| 橋架材料量 | `CTMRL` 與元件元素；各清單 `Export to Excel` | 材料表報表範本〔待核對〕 |
| 讀 MDS 支撐 | 元素 `STRU`／`FRMW`／`SCTN`、`SREF`、`SPREF`；UDA `:MDSBUILDSTYL`；Site `/MDS/TEMPLATES`、`/MDS/HANGERS`；`REST` | UDA 完整清單與型別〔待核對〕 |
| 讀結構關聯 | `ASSOWL`／`ASSOGP`／`ASSOC`，命名 `<sitename>-MDS-ASSOWL` | 關聯屬性存取〔待核對〕 |
| 批次報表／檢查 | `MDS-REPORT-DEFS`、`MDS-REPORT-HEADINGS`；輸出到 `%MDSREPORTS%`、`%pdmswk%`、`%projcodeinfo%` | 無人值守執行方式〔待核對〕 |

**開發建議：**

1. **只讀、不改**。MDS 目錄與規格不得修改；支撐資料牽涉自動關聯與 Integrity Checker，貿然用腳本改尺寸，可能繞過檢查。
2. **先看狀態再取數**。電纜要看 Routing Status；支撐要先過 HCU，再匯出清單。
3. **以 csv 輸出為整合介面**，報表與健康檢查都可寫 csv，比抓畫面可靠。

## 26.15 常見錯誤

| 現象 | 常見原因 | 處理 |
|---|---|---|
| 工具列全灰或建立失敗 | 目前階層不對，或缺必要上層元素 | 回到適當 Zone，確認階層 |
| 儲存區清單空白 | 沒有 Purpose 為 `CABL` 的 Zone | 建立或請管理員處理 |
| 佈線很慢 | 未指定 Cableway Zones，掃描整個 `WORLD` | 指定範圍 |
| 電纜只「部分佈線」 | 起點與入口位置不符 | Head／Tail Free Route |
| 填充率不準 | 電纜未選規格 | 補選電纜規格 |
| 建立 Tray Volume 失敗 | 缺少 Purpose 為 `TBAS` 的 Association Group | 依提示建立 |
| Branch 建立後路徑怪異 | Direction Sequence 與 Open Direction 不相容 | 調整其一 |
| 無法進入 MDS | MDB 缺 `/MDS/TEMPLATES` 或 `/MDS`、`/MDF` 規格 | 請管理員加入資料庫 |
| 結構改了支撐沒跟著找到 | 以 Dimensions 建立，未手動建關聯 | `Create > MDS SCTN Association` |
| 想直接改 MDS 目錄 | 誤以為可改 | 官方明禁；改用 Special 或由管理員配置樣板 |

## 26.16 本章小結

1. Cable Design 的順序是 Cableway（預留空間）、Cable（選型與佈線）、Cable Tray Material（鋪橋架）；元素階層為 `CWAY → CWBRAN → CTMRL → 元件`。
2. 規格可設在 Cableway 或 Branch 層級，自動向下沿用；儲存區只認 Purpose 為 `CABL` 的 Zone。
3. 電纜有五種佈線方式與六種 Routing Status；Fill Level Check 的綠黃紅對應最大填充率與 Allowance。
4. MDS 以管理員配置的樣板與預設值驅動標準支撐，涵蓋管路、橋架、風管；目錄不得修改，不合用就做 Special。
5. Cursor、Clearance、Dimensions 三種建立方式各有前提；只有前兩者自動建立結構關聯。
6. 完成時有 Integrity Checker，交付前再跑 HCU；報表可輸出 csv，適合作為整合介面。
7. 官方幾乎無 PML 範例；本章所有程式介面細節均須實測。

## 26.17 練習題／自我檢核

1. 為什麼 Cabling Application Defaults 的 Storage Areas 清單可能是空的？
2. 說明 `minimize Free Route` 與 `minimize Total Length` 的差異，並舉一個後者不選最近點的情況。
3. 一個 Branch 最大填充率 75%、Allowance 設 5，某點填充率 71%，格子會是什麼顏色？
4. 比較 Automatic Routing、Define Route、PRP 與 Manual Route 的適用情境。
5. 為何以 Create by Dimensions 建的支撐，結構專業改梁時難以追蹤？應如何補救？
6. 列舉 Integrity Checker 的三種結果等級與各一個觸發條件。
7. 設計一個報表流程：電纜佈線完成後，如何用本章功能輸出填充率異常的 Branch 清單？哪些步驟需要〔待核對〕？

## 26.18 〔待核對〕彙整

1. AVEVA Instrumentation and Electrical 與 Compare/Update 的整合細節。
2. Data Checker Utility 對 Cableways、Trays、Penetrations 的檢查內容。
3. 橋架材料表、電纜清單與出圖範本是否有預設版本，及其與第 8 章材料機制的關係。
4. 電纜通道、佈線狀態、填充率對應的 PML 屬性名稱與取值方式；`EXTGEO` 內容。
5. 批次佈線與批次健康檢查是否可由 PML 或指令列呼叫。
6. Import Cables 檔案的欄位規格。
7. MDS 完整 UDA 清單、Lighting Support 與 HVAC Special 專頁細節。
8. MDS 的客製（樣板管理、ADP）細節，本章僅確認入口。

**取材限制：** 以 *Cable Design* 全部約 66 頁讀完（部分深層子頁僅讀重點）；Multi-Discipline Supports（約 385 頁）以使用者手冊為主，管理員、客製與自動出圖手冊只讀總覽與重點表單，未逐頁細讀。
