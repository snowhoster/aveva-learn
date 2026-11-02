# 第 8 章　初始設計（Initial Design）：型線、曲面、靜水力、艙室與水動力

> 第 9 章談的是在 Dabacon 模型資料庫裡建造船殼結構，第 42 章談的是載重電腦所需的靜水力與艙容資料。這兩章都有一個前提：**船體外形與艙室分割已經存在**。這一章往上游走一步，看「那份外形與艙室是怎麼來的」：設計者從一組不太平順的型值表（Offset Data）出發，經過型線整修（Fairing）、曲面生成、艙室分割，再把結果交給靜水力與水動力計算。這整段工作在 AVEVA Marine 裡叫 **Initial Design**（初始設計）。
>
> 對二次開發者而言，Initial Design 有點特別：它的七個模組（Data、Lines、Surface、Compartment、Hydrostatics、Hydrodynamics、Utilities）**大多不是 PML 應用**，而是各自獨立的桌面程式，用**檔案**與**專案資料夾**互相交換資料。所以這一章的二次開發重點不在「呼叫哪個 PML 物件」，而在「哪個檔案由誰產出、誰讀入、格式長什麼樣」。
>
> **資料可信度：** 本章的模組分工、選單路徑、對話框名稱、環境變數（`SB_NAVARCH`、`SB_TID`）、檔案類型（Britfair、DML、GPF、FCT、GDS、CALC、Geometry XML、`tidexp`）與 XML 元素名稱，取自 AVEVA Marine 12.1 官方離線文件的 *Initial Design* 章節下 Data、Lines、Surface、Hydrostatics（Calc）、Compartment、Hydrodynamics（Hydro）與 Utilities 各份 Users Guide 與 Operators Instructions。該文件是由舊版 Tribon M3 文件延續而來，**畫面截圖與部分文字仍寫 Tribon**，本章照原樣保留。官方整棵子樹約 2,200 頁，本章只深讀各模組總覽與代表性操作頁，未逐頁核對；細項參數、全部指令語法與各計算方法請以原文件為準。文件幾乎沒有程式範例，**「二次開發者怎麼接」只寫文件有依據的檔案與命令介面，其餘標〔待核對〕**，不得當成已驗證的 API。

## 8.1 學習目標

讀完本章，你應該能夠：

1. 說明 Initial Design 在整體船體設計流程中的位置，並畫出七個模組之間「釋出（Release）與使用（Use）」的資料流。
2. 區分獨立（Stand-alone）專案與納入 PIM（Product Information Model）的專案，並說明 `SB_NAVARCH`、`SB_TID` 兩個環境變數的用途。
3. 使用 Initial Design Project Tool 管理專案與設計（Design），並說明匯出、匯入、關聯（Associate）與釋出的差別。
4. 說明 Lines 以 B-Spline 描述型線的原理，以及從匯入型值、整修曲線、水線端部到分塊生成曲面的工作順序。
5. 說明 Hull Form Definition 的角色，以及為什麼「整修中的型線」與「下游使用的船體」要分開釋出。
6. 說明 Surface 模組（ACIS／NURBS 幾何核心）能做什麼，以及它與 Lines 的分工。
7. 說明 Compartment 的 Envelope、內部曲面、艙室與 Calculation Geometry 之間的關係，並用 Sectional Area Curve 檢查艙室定義。
8. 說明 Hydrostatics（Calc）的輸入幾何格式、計算樹結構與常見計算項目，並指出它與第 42 章載重電腦的資料銜接點。
9. 說明 Hydrodynamics（Hydro）的四類計算（Powering、Manoeuvring、Seakeeping、Dynamic Positioning）與資料檔。
10. 說明 Utilities（Command Interface、Digit、Plot、Edit Britfair、DXF to Britfair）的用途，並列出二次開發者可串接的檔案與命令介面。

## 8.2 Initial Design 在設計流程中的位置

### 8.2.1 它做什麼、不做什麼

造船設計通常從「概念」走向「詳細」。Initial Design 負責的是前段：**決定船體外形、初步分艙、驗證浮力與穩度、評估推進與耐海性**。它產生的資料，之後才被船體結構設計（Structural Design、Hull，見[第 9 章](ch09_hull_modelling_zh-TW.reading.html)與[第 15 章](ch15_hull_production_zh-TW.reading.html)）當成「曲面骨架」使用。

| 問題 | 回答 |
|---|---|
| 它建立鋼構件（板、肋骨）嗎 | 不。它只建立曲面、甲板、艙壁面與艙室這類**幾何邊界**；板件與型材在 Structural Design／Hull 建立。 |
| 它的資料存在哪裡 | 設計（Design）存在專案資料夾；納入 PIM 時，釋出的物件會寫到 Initial Design 資料庫（databank）。 |
| 靜水力計算會改幾何嗎 | 不會。Calc 只是「評估模組」，幾何只能回到幾何建模程式修改（見 8.7）。 |
| 它和第 42 章載重電腦的關係 | 載重電腦需要的船體靜水性能表與艙區定義，源頭常是這裡的幾何與 Calc 計算結果。 |

### 8.2.2 七個模組的分工

| 模組 | 程式內名稱 | 一句話職責 | 主要產出 |
|---|---|---|---|
| Data | Initial Design Project Tool | 專案、設計、依賴與釋出的管理 | 專案目錄、`tidexp` 匯出檔 |
| Lines | Lines／PACE | 以 B-Spline 描述並整修型線，產生曲面片（Patch） | Lines Datastore、Hull Form（DML）、Loft Book、IGES／VRML |
| Surface | Surface | 3D 實體／曲面建模（附屬體、複雜曲面、布林運算） | Surface Datastore、SAT、DXF／Plot 檔 |
| Compartment | Compartment | Surface 的延伸：包覆體、艙壁、甲板、艙室、貨櫃排列 | Design、Calculation Geometry |
| Hydrostatics | Calc | 靜水力、穩度、艙容校準、載況、法規檢查 | CALC 檔、報表（HTML／LaTeX／XML／DXF） |
| Hydrodynamics | Hydro | 阻力與推進、操縱、耐海性、動態定位 | Hydro 設計檔、各類資料檔與報表 |
| Utilities | Command Interface、Digit、Plot、Edit Britfair、DXF to Britfair | 周邊小工具：命令介面、數化、繪圖檔編修、型值編修與 DXF 轉換 | Britfair、`.3d`、Plot 檔 |

### 8.2.3 釋出與使用：資料怎麼往下游流

Initial Design 的核心概念只有兩個動詞：**釋出（Release）**與**使用（Use）**。設計者在自己的設計裡持續修改；準備好給別人用時才「釋出」，下游的人再「使用」那一版。釋出之前，資料雖然已存在專案或 PIM 裡，但對其他流程是**私有**的。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Initial Design 資料流：Hull Form 設計釋出 Hull Form，Compartment 使用並釋出 Design 與 Calculation Geometry，結構設計使用 Design，Calc／Hydro 使用 Calculation Geometry

*圖 8-1　Initial Design 的釋出與使用。中央是船舶資料庫（PIM），四個設計程序圍繞它。（AVEVA 官方文件截圖，僅供內部教學）*

這個設計讓上下游可以**平行作業**。官方文件給的範例情境如下，圖 8-2 把它畫成時間軸：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Initial Design 工作流程時間軸：粗略船型、船型整修、艙室分割、靜水力與基本設計、再生成

*圖 8-2　範例工作流程。步驟 1 用型值表快速產生粗略船型；步驟 8、12 只有在資料存放於 PIM 時才需要。（AVEVA 官方文件截圖，僅供內部教學）*

1. 用型值表與很少的資料，快速產生一個粗糙船型（Lines 與 PACE）。
2. 釋出粗糙船型。
3. 一邊繼續整修型線，一邊用粗糙船型進行艙室分割（Compartment）。
4. 釋出以粗糙船型為基礎的計算幾何與設計。
5. 用計算幾何做初步靜水力（Calc），並可同時進行基本設計。
6. 型線整修到位後，釋出新版本。
7. 艙室分割重新使用新船型並更新，再釋出計算幾何；重算靜水力，視需要重新生成基本設計。

下表整理「什麼東西從哪裡釋出、給誰用」，這也是日後排查「為什麼下游看不到我的修改」的第一張檢查表：

| 可釋出資料 | 釋出者 | 釋出物件 | 使用者 |
|---|---|---|---|
| Hull Form | Lines | Patch、curve | Surface、Compartment、Structural Design、Hull、Design Manager |
| Design | Surface、Compartment | 曲面、curve、艙壁、甲板、艙室 | Structural Design、Hull、Design Manager |
| Calculation Geometry | Surface、Compartment | 艙壁、甲板、艙室 | Hydrostatics（Calc／Hydro） |

> **專業提醒：** 「改了型線，下游沒更新」九成是沒有重新釋出。設計者應養成「改完一個里程碑就釋出一次」的習慣；專案主管則應規定哪個釋出版本是「正式版」，並記在設計的 Description 欄。

## 8.3 Data：專案與設計管理

### 8.3.1 兩種專案：獨立與 PIM

官方文件把 Initial Design 的資料位置分成兩種做法，**一旦專案建好，之後的操作方式完全相同**：

| 項目 | 納入 PIM | 獨立（Stand-alone） |
|---|---|---|
| 與結構設計的連線 | 直接共用，釋出後即可被 Structural Design／Hull 使用 | 沒有直接連線 |
| 專案選擇 | 用 Project Selection 應用程式選專案 | 用 Initial Design Project Tool，勾選 Stand-alone |
| 必要環境變數 | `SB_NAVARCH`、`SB_TID` | 無 |
| 適用情境 | 船廠內部完整流程 | 設計代理商、早期概念、不在船廠網路內的工作 |

納入 PIM 時，要用 AVEVA Marine Control Panel 的 Environment Setup 把環境變數設好：

- `SB_NAVARCH`：存放 Initial Design 各設計的資料夾，通常是主專案資料夾下的子資料夾。
- `SB_TID`：指到「Initial Design 物件要存入、並供 Structural Design 與 Hull 使用」的資料庫（databank）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕專案資料夾結構：dat、db、def、geomac、lst、nc、nest、plot、prg、sch、tid，其中 SB_NAVARCH 指向 tid，下含曲線與曲面片、縱向構件與艙室、靜水力與 Trim 表、已釋出的 Hull Form 與 Calculation Geometry

*圖 8-3　專案資料夾與 `SB_NAVARCH`。`dat` 子資料夾放輸入輸出檔，`tid` 放各種 Initial Design 設計。（AVEVA 官方文件截圖，僅供內部教學）*

所有輸入／輸出檔預設都放在專案資料夾的 `dat` 子資料夾，開檔與另存新檔對話框也預設指向那裡。**建議把所有外部輸入檔（型值表、DXF、GPF）集中放在 `dat`**，這是日後備份與搬遷最不容易漏檔的做法。

### 8.3.2 Initial Design Project Tool

> 〔公開版未收錄：AVEVA 官方產品截圖〕Initial Design Project Tool：左側專案樹與 Stand-alone 勾選，右側設計清單顯示類型、修改時間、使用者與鎖定者

*圖 8-4　Initial Design Project Tool。範例專案內有 Lines、Surface／Compartment、Calc／Hydro、Hull Form 與 Calculation Geometry 五種設計。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 選單／按鈕 | 說明 |
|---|---|---|
| 新建／註冊專案 | Project > New／Register | New 建立獨立專案；Register 把別人建好的既有專案掛到自己的專案樹，適合共用 |
| 選取專案 | Project > Select | 設為目前專案；設計只有在「目前專案」下才能 Open 或 Release |
| 取消註冊 | Project > Unregister | 只從樹上移除，**不刪**專案資料夾與設計 |
| 關聯（Associate） | Project > Associate | 把獨立專案關聯到完整專案資料庫（Dabacon），並選 MDB；之後釋出的 Hull Form、內部曲面、艙室才會寫入完整專案資料庫 |
| 匯出／匯入專案 | Project > Export／Import | 產生／讀入 `tidexp` 檔，可整個專案、只含已註冊設計、或只含選取設計 |
| 設計操作 | Design > Open、Copy、Delete、Rename、Release、Properties、Unlock | Copy／Delete 同時處理設計歷史；Unlock 只能在確定鎖定者已不在使用時才用 |
| 預設值 | Design > Defaults | 設定新設計會繼承的預設值（一般尺寸、肋位表、單位等） |

**設計預設值的行為：** 新設計會繼承專案預設值。若預設值在設計上次存檔之後被改過，下次開啟該設計時會出現 Update from Design Defaults 對話框，可以逐項勾選要不要更新，按 Cancel 則全部保留設計原值。

**一般尺寸檔（GPF，General Particulars File）：** 純文字檔，共 14 行，每行一項，依序為船名描述（最長 80 字元）、全長、垂標間長（LBP）、船寬、吃水、中站型深、平板龍骨半寬、半船寬處的舭升高、舭圓弧半徑、龍骨傾斜量、艉懸伸、艏懸伸、最大總高、基線下最小高度。格式簡單、官方有明文，是少數**可以安全由外部程式產生**的輸入檔。

### 8.3.3 設計、依賴與歷史

每個設計程序（型線設計、艙室分割、靜水力計算）各建立自己的設計，同一個程序可以有多個設計（例如不同版本）。新建設計：啟動對應程式，File > New，輸入名稱與簡述即可，系統會帶入專案預設值。

當一個設計透過 Use Design 對話框使用另一個設計時，兩者產生**依賴（Dependency）**。例如 Compartment 設計用某個 Hull Form 產生 Envelope，則該 Hull Form 就是它的依賴。Hull Form 之後被改版，下次開啟 Compartment 設計時會出現 Update Dependencies 對話框，同意後 Compartment 會用新 Hull Form 重做 Envelope。Design Properties 的 Dependencies 頁可以移除依賴，但**只斷開連結，不刪除設計本身**。

### 8.3.4 把 Initial Design 資料交給結構設計

結構設計（Structural Design、Hull、Design Manager）要用 Initial Design 資料前，資料必須**已納入 PIM 並已釋出**。官方列了三種情境：

| 情境 | 條件 | 要做的事 |
|---|---|---|
| 1 | 設計一開始就建在 PIM 內 | 確認專案已關聯到有 databank 的完整專案；釋出 Hull Form、內部曲面、艙室；用 Initiate Hull Standards 登錄名稱 |
| 2 | 獨立專案，但與 PIM 在同一網路 | 用 Associate 連到 PIM；把專案資料夾（含子資料夾）複製到專案伺服器較佳；設 `SB_TID`；釋出；登錄名稱 |
| 3 | 獨立專案在遠端（例如設計代理商） | 遠端端 Export Project 產生 `tidexp`；船廠端建好資料夾與專案並 Associate，設 `SB_TID`，Import Project，再釋出與登錄。後續若有更新版匯出檔，重新 Import 並重新釋出即可 |

登錄的對象：釋出的 Hull Form、Envelope 或 Surface 要在 **Initiate Hull Standards** 登錄為船殼曲面、甲板曲面或額外曲面；曲線隨 Hull Form 一起可用；艙壁與甲板釋出後成為參考曲面物件（RSO，Reference Surface Object）；艙室釋出後即可使用。船廠端**必須安裝 Initial Design，但匯入與釋出不需要 Initial Design 授權**。

> **專業提醒：** 情境 3 是最容易出包的一種。匯出檔的版本與船廠端 Initial Design 版本要對得上〔待核對：跨版本匯入的支援範圍〕；匯入後務必核對 Hull Form 名稱有沒有在 Initiate Hull Standards 重新登錄，否則結構設計會繼續用舊曲面。

### 8.3.5 常見錯誤

| 錯誤 | 後果 | 做法 |
|---|---|---|
| 設計檔散落各人電腦 | 無法共用、無法備份 | 專案放伺服器，其他人用 Register 掛載 |
| 沒設 `SB_TID` 就釋出 | 結構設計看不到資料 | 釋出前先檢查環境變數 |
| 以為 Unregister 會刪資料 | 誤判專案已清除 | 它只移除樹節點 |
| 強制 Unlock 他人正在開的設計 | 兩人同時寫入造成資料遺失 | 先確認 Locked By 的使用者已離開 |

## 8.4 Lines：型線設計與整修

### 8.4.1 概念：B-Spline 取代木條

Lines 用 2D 與 3D 空間曲線描述船體，數學基礎是 **B-Spline**。這個設計有個很貼近放樣傳統的比喻：以前放樣工人用一根細長的彈性木條，加上鉛塊（ducks）壓住，彎出順暢的曲線；Lines 的 B-Spline 就是數學上的木條，**控制多邊形的頂點與節點向量（knot vector）決定曲線形狀**，而「鉛塊的重量」則由指定在特定點上的節點條件（KNOTS）取代。

對教學來說，要記住 B-Spline 的幾個實用性質：

- 可以顯示多邊形頂點，並直接拖動頂點修改局部形狀。
- 可以產生**折角（Knuckle）**，也就是一階導數的不連續點，而不影響整條曲線的定義。
- 能穩定擬合不均勻、不規則間距的點。
- 容易查詢曲線性質：座標、斜率、曲率、包圍面積。「平順度（Fairness）」的主要判斷依據就是**曲率半徑倒數（曲率）**沿曲線的變化。

### 8.4.2 介面與曲線種類

> 〔公開版未收錄：AVEVA 官方產品截圖〕Lines 主畫面：下拉選單、工具列、曲線與 Hull Form 樹、多個圖形視窗、命令列、輸出視窗與點緩衝區

*圖 8-5　AVEVA Initial Design Lines 主畫面。左側樹列出 Boundary、Section、Waterline、Buttock、Knuckle 等曲線類型；下方有命令列與輸出視窗。（AVEVA 官方文件截圖，僅供內部教學）*

左側 Lines View 樹把曲線分門別類，從畫面可見的類型有：

| 曲線類型 | 用途 |
|---|---|
| Boundary | 邊界曲線，如 FOS（甲板邊線）、FOB（底部）、艏艉輪廓、半徑、切線、偏心、過渡與端面（EndSurface） |
| Section／Waterline／Buttock | 橫剖線、水線、縱剖線，構成型線圖三視圖 |
| Knuckle／Tangent／Pline | 折角線、切線、空間折線，用來保持折角、甲板邊、艉封板等特徵 |
| Sheer／Camber／Angle curves | 舷弧、梁拱與角度曲線，用於甲板與 3D 擬合 |

### 8.4.3 工作順序

官方的「Major Tasks」把一個設計的流程拆成這些階段：

| 階段 | 做什麼 | 重點 |
|---|---|---|
| 1. 建立設計 | 匯入或數化一組橫剖面型值與各控制曲線 | Lines 是開放系統，**沒有強制的曲線或步驟**，依船型調整 |
| 2. 整修（Fairing） | 在 Edit 對話框中移除／替換／移動／插入點、設定折角／切線／一般點、偏移頂點、插入或刪除節點，或自動整修 | 可用游標或直接輸入 U、V 值；滿意後以 Accept 存入剖面目錄 |
| 3. 3D 曲線整修 | 用 3D 曲線與可選的角度曲線，減少資料量並以角度控制形狀 | 建議**艏艉分開成兩個設計**，因為很難用同一組 3D 曲線同時適配兩段船體 |
| 4. PACE 編修 | 在 Patch and Curve Editor 中半自動產生並互動調整曲面 | 官方建議的曲面生成主要方式 |
| 5. 水線端部與框腳 | 建立 End Surface，把水線併入，再擬合新的剖面 | 見 8.4.4 |
| 6. 甲板 | 產生甲板曲面 | 事先必須建好舷弧（Sheer）與梁拱（Camber）曲線；若甲板用舷墻頂緣則另需定義 Gunwhale |
| 7. 船體變形 | 以橫剖面積曲線（SAC，Sectional Area Curve）做 1-Cp 或 Lackenby 變形，或線性縮放主尺度 | 1-Cp 可改 CB；Lackenby 可改 CB、LCB、前平行中體（PBF）、後平行中體（PBA） |
| 8. 生成曲面 | 把整修後的船體用 Patch 描述成曲面 | 主法 PACE；次法用 Surface Patches 對話框手動逐片產生 |
| 9. 釋出 Hull Form | 定義並釋出 Hull Form Definition | 見 8.4.5 |

Lines 的 Operators Instructions 列出約 29 個對話框，這些對話框名稱本身就是很好的「功能地圖」：Create Curve、Fairing、2D／3D Construction、Edit、Analyze Curve、Parallel MidBody、Deck Generation、Plotting、Loft Book Generation、Distortion、Surface Patches、Export、Split、Join、Curve Endings、Hull Form Properties、Macro Editor、Customize 等。

### 8.4.4 水線端部與框腳

艏艉端部的水線形狀最難整修，Lines 的處理方式是建立一個**端面（End Surface）**：一個真正的數學曲面，讓既有或新建的水線併入其上，新擬合的剖面也會與它相交。艏艉各可建立一個。

> 〔公開版未收錄：AVEVA 官方產品截圖〕水線端部構造：被截斷的水線、與過渡曲線的交點、與端面的交點與端面剖面

*圖 8-6　水線端部（Waterline Ending）構造。水線在與過渡曲線的交點被截斷，再接上由端面交線導出的新曲線段。（AVEVA 官方文件截圖，僅供內部教學）*

若各水線高度的端部半徑事先未知，官方建議的步驟是：建立半寬曲線（Half Siding）→ 把水線擬合到半寬曲線 → 由半寬與水線導出半徑曲線 → 可選建立偏心曲線 → 建立端面 → 建立過渡曲線（可選但建議）→ 更新水線。若半徑已知，則可手動建立半徑曲線並從第 4 步做起。更新水線時，每條水線在與過渡曲線的交點被截斷，再嵌入一段盡可能平順、且與截斷水線及端部連續的新曲線。

過渡曲線可以省略，前提是水線本身已平順、只想改端部；此時若有切線曲線，水線在切點截斷，否則就在與端面的交點截斷，**該交點必須本來就平順，否則水線會出現不連續**。

### 8.4.5 Hull Form Definition 與釋出

整修與曲面生成之後，設計要拆成給下游使用的 **Hull Form**。Hull Form Definition 是一組曲面片與曲線的集合，用來定義主船體、甲板、附屬體等，它**引用**既有的曲線與曲面片，而不是複製。這樣 Lines 設計可以繼續整修，下游則使用已釋出的那一版。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull Form 樹：Hull Form Definitions 下的 Mainhull，含 Boundary、Knuckle、Tangent、Pline、Surface 節點與右鍵選單 Add to Hull Form Definition

*圖 8-7　在 Hull Form 樹中把曲面片加入 Hull Form Definition。（AVEVA 官方文件截圖，僅供內部教學）*

建立步驟：

1. 切到 Hull Form 樹頁，對 Hull Form Definitions 節點按右鍵，選 Create。
2. 輸入 Hull Form 名稱並按 Enter，隨即出現 Hull Form Properties 對話框。
3. 指定類型：Main Hull、Main Deck、Deck（主甲板以外）、Other（例如附屬體）；以及位於 Port、Starboard 或 Both 側。
4. 在子樹選取曲線與曲面，按右鍵選 Add to Hull Form Definition（或用左側核取方塊逐項加入）。
5. 釋出：對單一 Hull Form 用右鍵選單的 Release，或用 File > Release > Release Hull Forms 一次釋出全部。

### 8.4.6 輸出：Britfair、IGES、VRML、Loft Book

| 輸出 | 說明 |
|---|---|
| Surface Patches > Output：File | 每個 Patch 輸出成獨立 ASCII 檔（點網格），僅限 REGULAR 型 Patch |
| IGES | IGES 128（B-Spline 曲面）格式，選取的 Patch 輸出成同一個檔；PACE 產生的平面 Patch 目前不能輸出 |
| VRML | 面片化後輸出成 VRML 2.0 檔；同樣不含 PACE 平面 Patch |
| Loft Book | 以 Loft Book Generation 對話框產出型值表（見 8.5.4） |
| Plotting | 產生 General Plot 檔，可再以 Plot 工具（見 8.9）編修 |

**檔案格式摘要：** 官方只對「含觸發字元（trigger）的檔案，如 Britfair」給了格式，Knuckle 一類輸入檔格式如下（分隔符可為空白或逗號）：

| 輸入 | 每行內容 |
|---|---|
| 艏艉輪廓（Stem & Stern Profile） | X, Z 一對 |
| 艏艉半徑／偏心／過渡 | 半徑 (或偏心、或 X)、Z 一對 |
| FOB、FOS、Knuckle、Tangent、Pline | X, Y, Z 一組 |
| Cline | U, V 一對（U、V 視其定義所在視圖而定） |
| Sheer curve | X, Z 一對 |
| Camber curves | Y, Z 一對 |
| Angle curves | U, V 一對，U 為正交曲線值、V 為相交角度（度） |

> **專業提醒：** 型線整修是「主觀判斷」加「工具輔助」的工作。官方也明講「平順度的最終判斷是主觀的」。不要為了追求曲率圖完美，把設計者修過的特徵（折角、艉封板、舭龍骨）也一起磨平；需要保留的位置一律先標成折角。

### 8.4.7 常見錯誤

| 錯誤 | 症狀 | 做法 |
|---|---|---|
| 艏艉共用同一組 3D 曲線 | 曲線擬合怪異、難以控制 | 艏艉分成兩個設計再合併 |
| 沒有舷弧或梁拱就產生甲板 | 產生失敗 | 先建 Sheer 與 Camber 曲線 |
| 在不平順的交點做水線端部 | 水線出現不連續 | 先整修交點位置，再接端面 |
| 把整修版與釋出版混用 | 下游拿到舊形狀 | 用 Hull Form Definition 管理釋出版 |

## 8.5 Surface：曲面與附屬體建模

### 8.5.1 Surface 與 Lines 的分工

Lines 用「點與曲線」描述一般船型，Surface 則用 3D 實體／曲面建模，處理 Lines 不容易表達的對象：**船體附屬體、潛艇船體、半潛式平台、特殊內部佈置**等複合曲面。常規船體通常由 Lines 先產生初步曲面定義，再匯入 Surface 做後續處理；潛艇或半潛平台則可以整個定義都在 Surface 內完成。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Surface 與其他模組的關係：Surface／Compartment、Lines／PACE、Design Hull、Surface Manager、非 AVEVA 應用程式與 Hydrostatics／Hydrodynamics 都透過資料庫交換設計幾何與計算幾何

*圖 8-8　Surface 與其他程式的資料交換。（AVEVA 官方文件截圖，僅供內部教學）*

Surface 的技術基礎有三個關鍵字：

- **ACIS 幾何核心：** 把線框、曲面與實體整合在一個模型裡，支援有界、無界與非流形（non-manifold）物件。
- **NURBS：** 曲線與曲面皆以非均勻有理 B-Spline 表示，並支援 n 邊形曲片做融合（blending）。
- **回溯／前進（Roll back／forward）：** 以線性序列快速復原與重做模型狀態，等於提供「what-if」功能。

此外它有 100 個圖層可存放與顯示幾何，指令可存成巨集（Macro）執行，介面可自訂圖示，這些對二次開發者都是現成可利用的自動化入口（見 8.9 與 8.10）。

### 8.5.2 建立設計與匯入來源

建立新設計沒有強制檔案；一般尺寸、肋位表、單位與座標軸取自目前專案預設值。常用路徑如下：

| 來源 | 選單 | 說明 |
|---|---|---|
| Lines 的 Hull Form（DML 檔） | File > New 後 File > Use > Hull Form... | 可能帶有一般尺寸，並以其為新設計基礎 |
| 型值表（Britfair 檔） | File > Use > Offset Data | 以兩條相鄰曲線的點之間做三角平面片，形成粗略曲面 |
| 其他系統的 ACIS 檔 | File > Import > ACIS SAT File > General | 之後要自行指定與專案不同的一般尺寸 |
| Lines Datastore | File > Import > Lines Datastore，或命令 `IMPORT LINES $F` | 曲線以 B-Spline 匯入並轉成 ACIS 實體；可匯入所有邊界曲線、Section、Waterline、Buttock、Knuckle、Tangent、Pline |
| 回寫 Lines | File > Export > Lines Datastore，或命令 `EXPORT LINES $F` | 在 Surface 修改過的曲線可送回 Lines |

一般尺寸可由 Tools > Options 的 General Particulars 頁手動輸入，或用 Import 按鈕讀 GPF 檔。要注意：**Surface 不會自動存檔**，要定期 File > Save，並可用 File > Save As 重新命名。

### 8.5.3 從型值表建立曲面的技巧

從 Britfair 稀疏資料產生粗略曲面時，資料的幾個處理規則很重要，也是 Britfair 輸入檔品質的核對清單：

- **點類型：** 目前只有 Section，剖面由一般點與折角點（knuckle）組成。
- **重複點：** 距離小於 0.1 mm 的兩點視為同一點，檔案中較後面的那個會被忽略。
- **Y=0 平面上的面：** 完全落在中心線面上的平面片會被刪除，避免球鼻上方等位置生成多餘面。
- **邊線精簡：** 預設會移除落在同一平面、相鄰面之間不必要的邊，可關閉。
- **同 X 位置多個剖面：** 允許在同一個 X 值定義多於一個剖面，用於定義甲板階梯、折角數量轉換與問題剖面。
- **折角對應：** 若要讓某特徵（如舭線、艉封板、舵）從一個剖面延續到下一剖面，兩個剖面的折角點數量必須相同，系統才會把「第 N 個折角」連到相鄰剖面的「第 N 個折角」。要做折角數量轉換時，可建立兩個位置相同、但標示折角點不同的剖面。
- **球鼻：** 用一對折角在艏輪廓的反曲點處起算，下折角定義球鼻頂、上折角定義艏柱；球鼻最前端的第一點與下折角點可置於 Y=0 並相距 1 mm，以免被當成同一點。範例設計有 `FeatExam1`、`BulbExam1`、`BulbExam2`。

### 8.5.4 附屬體、融合、分析與輸出

**附屬體（Appendage）：** 可由 3D 基本形體、2D 基本形體或兩者組合建立。標準附屬體可存成 DM datastore 或 SAT 檔，再與模型合併；參數化附屬體可靠巨集達成。**建議一律在全域原點 (0,0,0) 建立，再平移或旋轉到定位**，因為 3D 基本形體永遠建在全域原點，平移功能通常以全域原點為基準。官方範例有「推進器管（thruster tube）加整流板」與「簡化舵」兩個，且列出所用指令，指令可線上輸入或用對話框操作。

> 〔公開版未收錄：AVEVA 官方產品截圖〕艏側推器圓柱與船體相交的精確幾何，以圓角曲面（fillet）處理

*圖 8-9　Surface 的曲面相交與圓角：艏側推器圓柱與船體的相交線，以融合工具產生圓角曲面。（AVEVA 官方文件截圖，僅供內部教學）*

**融合（Blending）：** 三種型式為圓角（round）、倒角（chamfer）、頂點融合（vertex）。倒角目前只適用於平面與圓錐曲面。融合可套在邊上立即生成，複雜情況可先把融合當屬性設在邊與頂點上，再一次產生完整網路。

**縮放（Scaling）：** 由型值表產生的船體若已定義一般尺寸，可用 Hull-Modeller > Hull Scaling 縮放 Lpp、船寬與吃水，並可保持長寬比。兩種方式：**Geosim**（各方向等比縮放）與**非均勻縮放**（長、寬、吃水／型深各自獨立）。同時縮放一般尺寸與內部曲面後，內部要用 Regenerate Internals 重新生成。

**曲面分析：** 以相交曲線或曲面方式檢查平順度，包含曲率渲染、平順度參數檢查等視覺化功能。

**繪圖與型值表：** Plotting 對話框產生 General Plot 檔；要先把正交曲線與 3D 曲線放在不同圖層，因為 Plotting 以圖層顯示對話框控制每個視圖要畫哪些內容。Loftbook 則產生指定曲線群組相交處的座標表：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Loftbook 對話框：Cross 與 With 下拉選單、Add 按鈕與已選的交會組合 Waterlines／Sections、Buttocks／Sections、Buttocks／Waterlines

*圖 8-10　Loftbook 對話框。Cross 選的曲線成為表格欄標題，With 選的成為列標題；可輸出成格式化報表或簡單文字檔。（AVEVA 官方文件截圖，僅供內部教學）*

Loftbook 輸出為文字檔時，可控制頁寬、每頁行數與行距；剖面識別可用肋位號（Frame）、站號（Station）或 X 距離，單位依目前設定（公尺或公釐）。

> **專業提醒：** Surface 的 `File > Save` 要有人負責。它不是自動存檔，曲面運算又很吃資源，建議每完成一個大步驟（相交、融合、縮放）就存一次，並利用 Save As 保留里程碑版本。

## 8.6 Compartment：艙室分割與計算幾何

### 8.6.1 它和 Surface 的關係

Compartment 是 Surface 的**延伸模組**：它建在同一個圖形介面與 ACIS 模型上，額外加上內部曲面（艙壁、甲板）、艙室與貨櫃排列等功能，結果存進 Surface Datastore。它特別有一個 **SLICE MODE** 檢視模式，專門方便觀看與調整內部曲面。啟動方式是先啟動 Surface，再建立一個新的 Compartmentation 設計。

### 8.6.2 Envelope：所有分艙的起點

任何內部艙壁、甲板與艙室，都是在某個 **Envelope（包覆體）**內產生的。Envelope 包含：

| 組成 | 說明 |
|---|---|
| Barehull | 至少要有，即船體外形 |
| Main Deck | 用來切掉 Barehull 的上半部 |
| Appendage 清單 | 正向元件（加進 Barehull）或負向元件（從 Barehull 扣掉），例如用圓柱基本形體扣除側推器隧道 |

Envelope 可以隨時修改（拿到更平順的船體、改型深、改附屬體），然後**整份內部佈置重新生成**。多個 Envelope 則用來分割子體積。**Envelope 必須完全封閉**（沒有破洞）才能產生艙室；檢查方式是在 View 工具列選 ID，或在圖形視窗右鍵選 IDENTIFY FLASH 後點選 Envelope，開放邊會閃爍。這個檢查通常先做在準備當 Barehull 的曲面上，因為它最可能有破洞。

建立基本 Envelope：在 Full View 樹選要當 Barehull 的曲面，按右鍵選 SET AS ENVELOPE；或用 Compartmentation > Envelope > Create 互動點選。之後必須用 SET ENVELOPE（或 Compartmentation > Envelope > Set Active Envelope）設為目前 Envelope，才能開始在其中建內部。

### 8.6.3 內部曲面與艙室

艙室被定義為由六個邊界（頂、底、艉、艏、左舷、右舷）圍成的概念空間。所有邊界都是平面時最簡單的結果是一個箱型；任何邊界也可以是外部 Envelope，因此能形成複雜形狀。極複雜的艙室可以用**合併數個基本艙室**達成。

橫艙壁、縱艙壁與甲板的產生方式非常相近，都是三個正交方向之一的平面。以 Predefined 方式建立的流程：

1. 開啟 Compartmentation > Internal Surfaces > Editor...，模式設為 Create，選內部類型（Transverse、Longitudinal、Deck）。
2. 在 Geometry 頁選 Creation Method 的 Predefined，填入 Position 與 ID。Position 的單位為目前單位；若數字後加 `(fr)` 或 `(stn)`，表示以肋位或站號（僅限 x 軸）輸入。
3. 切到 Constraints 頁，邊界維持 `*`（代表父 Envelope），按 Apply 產生簡單平面艙壁。重複此步建立所有艙壁與甲板。
4. 把模式改成 Edit，把要編輯的內部曲面放進清單（右鍵 GET 互動點選，或從 Full View／Compartment View 樹拖放）。
5. 在 Constraints 頁，用其他內部曲面限制其範圍。例如讓雙層底甲板延伸在艏尖艙壁與艉尖艙壁之間。可以互動點選邊界曲面、用下拉選單選、或把樹節點拖放到對應按鈕上。
6. 按 Apply，圖形視窗更新。

其他建立方式有 Interactive 與 Offset Shell（後者專用於縱艙壁）。每種內部曲面還有波紋（Corrugation）、墩座（Stool）與複雜幾何的定義上限，如官方表列：橫艙壁與縱艙壁各為 4，甲板的波紋與墩座各為 7、複雜幾何為 4。

**貨櫃排列（Container Arrangement）：** Compartment 可自動產生貨櫃貨艙格（Bay），在最少的約束下定義最大貨櫃排列：先設定貨櫃類型（預設為 ISO 標準，可改、可增），在指定位置定義貨艙格，系統依貨櫃尺寸自動堆出層（Tier）與列（Row），同時保留與船殼的最小距離、避開甲板起重機等障礙，也可定義視線（sightline）使貨櫃堆不擋視野。之後可手動增減貨櫃或加間隔，並由貨艙格產生簡易艙口蓋，輸出報表。這份資訊最後經由釋出 Calculation Geometry 傳到 Hydrostatics。

**預估重量分析（Preliminary Weight Analysis）：** 可對 Envelope 與內部曲面做初步的重量與重心分析，要傳遞的重量項目用 Weight Analysis 工具選取。

### 8.6.4 用 SAC 檢查艙室定義

在複雜的佈置裡，很容易不小心選錯邊界，造成體積被重複計算。官方介紹的檢查方法是**橫剖面積曲線（SAC）**：

1. 開啟 Compartmentation > Sectional Area Curve...，吃水填一個高過船體頂部的值，Trim 保持 0。
2. 在 Envelopes 清單選一個 Envelope，Compartments 清單會列出其艙室；選取所有代表內部體積的艙室（不要選只是為了合併而產生的暫存艙室）。通常選 Calculation Geometry 選項會自動選到對的。
3. 按 Generate，同時畫出 Envelope 的曲線與所選艙室的曲線。

若兩條曲線重合，代表所有內部空間都已定義。**艙室曲線高出 Envelope 曲線，代表有艙室重複包含同一體積，定義有誤；艙室曲線低於 Envelope 曲線，代表有些體積沒有被任何艙室定義**，這在你刻意不納入載重或破損穩度考量時是正常的。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Compartment 的 SAC 檢查：紅線為艙室曲線，在某段超出綠色的 Envelope 曲線，代表該段艙室體積重複

*圖 8-11　艙室 SAC 超出 Envelope SAC，表示有艙室重複計算體積，需回頭檢查邊界。（AVEVA 官方文件截圖，僅供內部教學）*

### 8.6.5 釋出 Calculation Geometry

Hydrostatics 與 Hydrodynamics 用的幾何與結構設計用的設計是兩回事。**Calculation Geometry** 只保留分析模組需要的艙室與面：合併過程中用到的暫存元件、與機率式破損穩度分區無關的內部曲面，都不必釋出。標記方式：

1. 在 Compartment View 樹的 Envelopes 節點下，確認每個要釋出的項目前面打勾；沒打勾時，點方塊或用右鍵選單 CALC STATUS > ON（OFF 清除、TOGGLE 切換，可多選）。
2. 用 File > Release > Calculation Geometry，或樹右鍵選單 RELEASE CALC GEOM 釋出。

兩點限制要記住：**一個 Surface／Compartment 設計只對應一個 Calculation Geometry 設計**；**Hydrostatics 使用的是面片（facet）資訊**，元件在產生時依 Options 對話框 Faceter 頁的設定面片化，除非個別元件另用 Faceting Parameters 設定。

> **專業提醒：** 面片化的精細度直接影響體積與重心的精確度。曲率大的面會用更多三角形；若發現 Calc 算出的排水量與 Compartment 的體積差了一點點，先查面片化設定，再查幾何。

### 8.6.6 常見錯誤

| 錯誤 | 症狀 | 做法 |
|---|---|---|
| Envelope 有破洞 | 艙室無法產生或體積錯誤 | 用 IDENTIFY FLASH 找開放邊，先修 Barehull |
| 選錯邊界 | SAC 艙室曲線高於 Envelope | 逐一檢查艙室的六個邊界 |
| 忘記設 Active Envelope | 內部曲面建在錯誤的包覆體 | 建好 Envelope 後立即 SET ENVELOPE |
| 暫存合併艙室也被釋出 | Calc 重複計算體積 | 只對真正的艙室標記 CALC STATUS |

## 8.7 Hydrostatics：靜水力與穩度（Calc）

### 8.7.1 定位與輸入

Hydrostatics 在程式介面與手冊中簡稱 **Calc**。它提供靜水力、穩度與其他例行造船計算，主要使用者是造船工程師，用於設計、評估船體特性與內部佈置、載重的影響，也可用於下水與傾斜試驗的分析。Calc 設計給單體船，但在某些限制下可用於許多浮體；**較新版本也包含船體水動力性能評估功能，那部分原屬 Hydrodynamics 模組**（見 8.8）。

Calc 的關鍵規則：它**只是評估模組**，依賴幾何建模程式輸入船舶定義（含一般尺寸與艙室名稱）。幾何只能在 AVEVA Marine 幾何建模程式裡改，**Calc 內只能重新命名艙室與設定滲透率（permeability）**。

| 資料類型 | 典型輸入檔 | 說明 |
|---|---|---|
| 面片資料（Facetted） | Facet（FCT）檔 | 三角面片 |
| 分段資料（Portion） | GDS 檔 | 以截面分段 |
| 剖面資料（Section） | Britfair（BRI）檔 | 橫剖面型值 |
| 校準資料（Calibration） | LoadMate Fluidtnk 檔 | 艙容校準點 |
| 全部類型 | Initial Design Geometry XML 檔 | **官方的首選方式**，另含開口、甲板邊緣點、艙室類別等 |

新設計時，Calc 會在專案內建立一個 Calc 資料檔（`CALC`），並附上一份標準準則檔（Master Criteria File）的副本。幾何匯入後會**複製並內嵌在 `CALC` 檔**，原始幾何檔不再需要。但若 Surface／Compartment 之後又釋出新的 Calculation Geometry，使用者下次開啟該設計時，Calc 會提示更新。新建專案要在 New Project 對話框指定專案名稱、專案檔（Calc 檔）、幾何檔（預設為 Geometry XML）與樣板（Template）；樣板可沿用過去專案的設定與計算配置。既有 `.calc` 或 `.cdf` 檔可用 File > Open 開啟；讀入 Release 4 的 CDF 檔時，因為舊版沒有 Calculation Tree，程式會建立預設樹並盡量沿用既有資料。

### 8.7.2 計算樹與主要計算

Calc 的操作大多對「目前選取的樹節點」進行。節點有四類：根節點、區段節點（Section，一組相關計算）、計算節點（Calculation，如靜水力）與報表節點（Report，可含文字與圖形）。報表只能屬於計算，計算只能屬於區段，區段屬於根。

樹節點的主要操作（工具列、選單或右鍵選單皆可）如下：

| 操作 | 說明 |
|---|---|
| Edit | 開啟該計算的設定對話框 |
| Calculate／Recalculate | Calculate 只算尚未算過的節點與其子節點；Recalculate 不管算過與否全部重算（修改了平衡容差、穩度準則等全域選項後用它） |
| Lock／Unlock | 鎖定節點（含子節點）；摘要會記錄鎖定者與日期，鎖定期間不可編輯也不能重算 |
| Cut／Copy／Paste、New Node、Delete Node | 調整樹結構，刪除會連同子節點 |
| Print／Print Preview／Toggle Printing | 控制哪些節點要列印 |
| Output | HTML（可轉入 Word 編修）、LaTeX（再轉 PDF）、XML（尚未 100% 完成）、LS（縱向強度資料，供水動力計算用）、DXF（艙容圖、載重圖、曲線圖等 2D 輸出） |

Calc 的計算區段（Operators Instructions > Calculations）涵蓋：

| 區段 | 內容 |
|---|---|
| Preferences、Options、Note | 全域偏好與選項 |
| General Particulars | 船舶一般資料、主要尺寸、主船體、穩度、座標軸、波浪、肋位表 |
| Tank Calibrations | 艙容校準：以最多 10 個 Trim、單一橫傾角，一次算出容量、橫向與縱向二次矩與重心位置 |
| Grain Calibrations | 散裝穀物艙校準 |
| Form Calculations | 船型係數與靜水力表 |
| Stability Calculations | 確定性穩度：由初始吃水、Trim、KGf 與橫傾角，計算完整與破損狀態；最多 10 個吃水與 5 個 Trim，破損情境數不限 |
| Probabilistic Stability | 機率式破損穩度：需先建立 Damage Scenarios 節點、在 Ship Data 選機率規則、在 Tankplan–Surfaces 對話框標記分區邊界面，並備妥受保護與未受保護開口資料 |
| Loading Conditions | 載況：由空船加分布死重量產生載況報告（艙室裝載、平衡吃水、靜水力、GZ 曲線、穩度檢查與縱向強度檢查），另含 Loading/Ballasting Sequences 與連續浸水（Continuous Flooding）模擬 |
| Regulations、Miscellaneous | 法規檢查與其他計算 |
| Report Editing | 重新排序、刪除報表元素、表格行列與圖形曲線 |

確定性穩度結果包含條件摘要、平衡時的靜水力、GZ 曲線表，以及所有開口與甲板邊緣點的浸水角與距水線距離，且船被視為可自由縱傾與橫傾。載況的縱向強度除了靜水彎矩與剪力，也可在船舶靜置於單一波峰或兩波之間的假設下輸出彎矩與剪力分布，但**純屬靜態平衡，不含動態慣性效應**。

**計算方法的特色：** 傳統手算以辛普生法則（Simpson's Rule）近似積分；Calc 則把主船體與每個艙室邊界面表示成**三角面片**（曲率愈大，面片愈多），直接計算面片包圍的體積性質再做簡單積分。破損穩度一律用**喪失浮力原理（lost buoyancy）**，同時考慮船體喪失浮力與水線面特性的變化。

### 8.7.3 約定、準則與可重用設定

- **座標約定：** x 向船艏為正，y 向右舷為正，z 由基線向上為正；原點通常在艉垂線、中心線與基線，但依模型而定。橫傾角向右舷為正，艏傾（trim by the head）為正。
- **標準準則檔：** Calc 內建的 CRITERIA 檔含 IMO A167、A749 非客船與客船、IMO Weather Criterion、MARPOL 73/78（油輪）、Load Line 等準則；例如 IMO 完整穩度準則的 GZ 曲線下面積、最大 GZ、初始 GM 下限等，具體數值以官方頁面與法規本文為準。〔待核對：你們使用的法規版本與是否需自行修訂準則檔〕
- **HCL 檔：** 作為設定專案預設資料的便利方式，可用 File/Import/HCL File 匯入，也可從任一專案匯出供下個專案使用。內容包含 BM 與 SF 限值、平衡容差、吃水標記、水密度、橫傾範圍、完整與破損準則組、艙口細節、甲板邊緣點、內容物項目、艙室指派、水面濕面積、螺旋槳資料、Stepped GZ 選項、甲板上水、波浪選項、受保護與未受保護開口、輪廓點、艙室類別、艙室滲透率。

### 8.7.4 與第 42 章載重電腦的銜接

[第 42 章](ch42_loading_computer_zh-TW.reading.html)講的載重電腦，需要的「空船、死重量項目、水艙特性表、靜水性能與艙區定義」，在造船工程師的實務裡常由 Calc 產出或驗證。以下是本章能看到的銜接點，**是否直接作為載重電腦輸入，需看你們載重電腦廠商的格式**〔待核對〕：

| Calc 輸出 | 可能的下游用途 |
|---|---|
| Tank Calibration 結果（容量、重心、自由液面矩） | 水艙特性表 |
| Form Calculations 與穩度結果 | 船體靜水性能表、KN 或 Cross Curves |
| Geometry XML 內的艙室 `perm`、`damperm`（滲透率）與類別 | 破損艙區定義與滲透率 |
| 報表 HTML／XML／LaTeX／DXF | 試航資料、穩度手冊與審圖文件 |

> **專業提醒：** 載重電腦的輸入資料務必註明來自哪一版 Calculation Geometry、哪一份 Criteria 與哪一次 Recalculate。船殼改版後，只要有人忘了重算靜水力，載重電腦的資料就是舊的，而且看不出來。

### 8.7.5 常見錯誤

| 錯誤 | 症狀 | 做法 |
|---|---|---|
| 想在 Calc 裡改艙室形狀 | 找不到功能 | 回 Surface／Compartment 修改並重新釋出 |
| 沒有完整內部分艙就做破損穩度 | 結果不可信 | 先確認艙室定義完整，並以 SAC 驗證 |
| 改了全域選項卻只 Calculate | 舊結果仍在 | 用 Recalculate |
| 忘了更新 Calculation Geometry | CALC 檔使用舊幾何 | 開啟設計時依提示更新 |
| 同時有多人修改同節點 | 資料衝突 | 用 Lock 鎖定已確認節點 |

## 8.8 Hydrodynamics：水動力性能（Hydro）

### 8.8.1 四類計算

Hydrodynamics 在程式與手冊中簡稱 **Hydro**，用來預測與評估船舶的水動力性能，包含四種計算：

| 計算 | 做什麼 | 輸出 |
|---|---|---|
| Powering | 阻力成分、推進因子、有效馬力與軸馬力；可用幾個經驗法則，部分使用艏艉船型因子（U、V 形狀因子） | 阻力表、有效與軸馬力曲線、螺旋槳 KT、KQ 與敞水效率曲線 |
| Manoeuvring | 迴旋、Z 形與反向螺旋等操縱計算 | 操縱摘要與圖形 |
| Seakeeping | 耐海性：各剖面水動力係數、規則波與不規則波響應、附加阻力、動態載荷、長期性能評估 | 剖面係數表、短期與長期結果、運動曲線與極座標圖 |
| Dynamic Positioning | 動態定位：推力、環境力與 ERN（THRUST、ENVIRO、ERN 三種計算） | 各風向的環境力與推進器力／方向、動態定位足跡圖 |

做水動力計算只需要輸入主要尺度、水密度與溫度，以及附屬體資料；其他則依計算項目另行輸入（Data Requirements）。

### 8.8.2 耐海性的計算鏈

耐海性是四類中計算鏈最長的，也是理解 Hydro 資料流的好例子。官方資料流程圖如下：

> 〔公開版未收錄：AVEVA 官方產品截圖〕耐海性資料流程圖：由船名、船體定義、吃水與縱傾進入 Hydrodynamics，經規則波響應、動態載荷、附加阻力，到不規則波響應與長期性能評估

*圖 8-12　Seakeeping 資料流程。左側為各階段所需的輸入（船速、LCG、VCG、迴轉半徑、附屬體、重量分布、海象、評估準則與波浪統計）。（AVEVA 官方文件截圖，僅供內部教學）*

1. 由水下船體在多個橫剖面上的型值、吃水與縱傾，算出各剖面對一系列波浪頻率的水動力係數（heave、sway、roll、sway-roll 的附加質量與阻尼）。有兩種理論可選：**Ursell-Tasai 多重勢理論**（以兩參數 Lewis 剖面表示）與 **Frank close-fit 理論**（以若干源奇點表示）。
2. 規則波響應模組依船速與浪向的遭遇頻率內插係數，累加成全船特性，由船速、重量分布參數（LCG、KG、迴轉半徑）與附屬體資料解出運動方程，得到傳遞函數（相對波峰的運動振幅與相位）。非線性橫搖阻尼以準線性項加入，用疊代求解，各項貢獻用 Ikeda 方法計算。
3. 附加阻力與動態載荷模組使用先前算好的剖面係數與規則波響應，分別算附加阻力係數、以及任意位置的規則剪力、彎矩與扭矩。
4. 不規則波響應模組結合海象資料（波譜與擴散函數），算出短期海況下的運動、載荷與平均附加阻力，也用相對運動與速度評估砰擊（slamming）、甲板上浪與螺旋槳出水的發生率。
5. 長期性能評估模組把一連串短期響應與波浪統計及耐海性準則結合，評估長期耐海性能。

### 8.8.3 檔案與資料格式

Hydro 同樣會在專案內建立資料檔，幾何輸入來自 Calculation Geometry（XML）或 FCT、GDS 等，匯入後內嵌，與 Calc 的行為相同。其他輸入與輸出檔如下（副檔名僅是慣例，**非必須**）：

| 檔案 | 用途 | 副檔名 | 方向 |
|---|---|---|---|
| Point Weight File | 動態載荷計算 | `.wgt` | 輸入／輸出 |
| Distributed Weight File | 動態載荷計算 | `.ls` | 輸入（輸出也會產生 `.ls`） |
| Voyage Data File | 長期計算 | `.voy` | 輸入 |
| Wave Data File（ASCII） | 長期計算 | `.dat` | 輸入 |
| Wave Data File（binary） | 長期計算 | `.bin` | 輸入／輸出 |
| Ratios File | 阻力計算 | `.rat` | 輸入／輸出 |
| RAO File | 修正或模型試驗的響應振幅算子 | `.rao` | 輸入；計算出的 RAO 可匯出 |

Ratios 檔的結構官方有詳細描述：第 1 記錄是用方括號括住的阻力方法名稱（每個方法一次，共十次），第 2 記錄是弗勞德數 Fn 與理論計算對模型試驗阻力的比值 r（每個適用的 Fn 一筆），第 3 記錄是以 `0 0` 表示的區塊結束記號。這是少數官方給出完整欄位說明的 Hydro 資料格式，其他格式請查原文件 *Data File Structures*〔待核對：本章未逐檔核對〕。

### 8.8.4 與 Calc 的關係

Calc 的 Output 選單可輸出 **LS（縱向強度資料，供水動力計算用）**，這就是兩個模組之間最直接的銜接點之一：Calc 的載況結果可以當作 Hydro 動態載荷的輸入。**二次開發若要自動化這條鏈，必須先確認 `.ls` 檔的格式**〔待核對〕。

### 8.8.5 常見錯誤

| 錯誤 | 症狀 | 做法 |
|---|---|---|
| 沒輸入附屬體就算操縱或耐海性 | 結果缺失或與試驗差異大 | 依 Data Requirements 補齊附屬體 |
| 把短期響應當作長期性能 | 設計裕度誤判 | 需要長期結果時要跑到 Long-term 模組 |
| 把 Calc 的靜態波浪彎矩當作動態載荷 | 低估載荷 | 靜態波峰平衡不含慣性效應，要用 Hydro 的動態載荷 |
| 檔案副檔名依慣例卻內容不符 | 讀入失敗 | 副檔名非必須，以內容格式為準 |

## 8.9 Utilities：命令介面與周邊工具

### 8.9.1 Command Interface（命令介面）

Lines 與 Surface／Compartment 都用同一套**命令驅動介面**：指令可由鍵盤在命令列視窗輸入，也可由巨集（用 Macro Editor 建立）輸入。各應用程式的指令與語法不同，但介面的結構與操作一致。

| 項目 | 內容 |
|---|---|
| 指令格式 | `Command <Parameter> <Qualifier(s)>`；指令與參數一律轉成大寫，大小寫不拘 |
| 語法記號 | `( )` 必選其一；`< >` 可選；`!` 表示「或」；`$W` 單一識別字；`$L` 一個以上識別字（以空白或逗號分隔）；`$F` 檔名；`$N` 單一數字；`$S` 一個以上數字 |
| 保留指令 | 一律以 `$` 開頭，與應用程式無關。一般類：`$DEFINE`、`$ECHO`、`$EVALUATE`、`$HELP`、`$LOG`、`$NOLOG`、`$PROMPT`、`$SHOW`。巨集類：`$DELETE`、`$DEFAULT`、`$DIRECTORY`、`$DO`、`$EXIT`、`$FREE`、`$GOTO`、`$IF`、`$INQUIRE`、`$LOAD`、`$MAC`（也可用 `@巨集名`）、`$PRINT`、`$SET`、`$TRACE`、`$VARIABLE`、`$WAIT` |
| 回傳值 | 部分指令的結果存進預設變數 `RET_CNT`（回傳值個數）、`RET_1`、`RET_2`…；下一個指令會覆蓋它們，所以要用 `$SET` 存到自己的變數 |

官方範例（節錄概念）展示了典型的巨集寫法：先用 `$VARIABLE` 宣告變數，執行 `INTERSECT SECTION 5 WITH FOS` 這類應用程式指令，再用 `$IF RET_CNT = 0 THEN $GOTO %NO-INT` 檢查有無交點，有則 `$SET intx RET_1` 等存下座標，沒有則 `$PRINT` 訊息後 `$EXIT`。

Lines 另有完整的 Command Reference（約 100 個指令，如 `ACCEPT`、`ADD`、`CHECK`、`COPY`、`CREATE`、`DEFINE PARTICULARS`、`DIRECTORY`、`DISPLAY`、`EXTRAPOLATE` 等）；Surface 也有自己的一份。**這是 Initial Design 裡唯一有文件根據的「程式化」入口**（見 8.10）。

### 8.9.2 Digit（數化）

Digit 設計給「放在連接主機的數化板上的圖」做數化輸入，也可以讀、寫與編輯 Britfair 格式的點資料。主要按鈕：Load（載入 Britfair，艏艉資料為 X、Z）、Merge（合併多個 Britfair 檔）、Save／Save As、Axis（設定座標原點與站號）、GPF（匯入一般尺寸以設定檢視範圍）、Reset、Window（放大）、Setup Digitizer（校準數化板）、Exit。

### 8.9.3 Plot（繪圖檔編修）

Plot 是互動式圖形編輯器，用來編修由 Lines、Surface 等產生的 **General Plot 檔**。元素定義為「任何一串相連的線」；可用游標選取元素，或框選區域（**只有完全在區域內的元素才會被選到**）。可加簡單的文字與指引線，但**所有文字都會被拆成移動與繪線指令**，只能以整體用區域選取的方式操作，不能當文字編輯。

### 8.9.4 Edit Britfair（型值編修）

Edit Britfair 處理儲存在 Britfair 及相關檔案中的型值：可互動編輯個別剖面的點，也能對整份型值做縮放、平移，以及用 Lackenby 方法做非線性變形。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Edit Britfair 的 Distortions 對話框：Scale ship、Geosim 與 Lackenby 三種變形，Lackenby 可設定 Cb、LCB、Entrance、Run 的目標值

*圖 8-13　Edit Britfair 的 Distortions 對話框。Lackenby 模式給定吃水後，可以把目前的 Cb、LCB、Entrance 與 Run 設成目標值。（AVEVA 官方文件截圖，僅供內部教學）*

使用變形前有三個條件：必須用 Load 載入 Britfair 檔、必須定義一般尺寸，且**同一資料夾內必須有同名的 `name.stn`（艉輪廓 X/Z 座標）、`name.stm`（艏輪廓 X/Z 座標）與 `name.gpf`（一般尺寸）**，`name` 即 Britfair 檔 `name.bri` 的主檔名。三種變形：Scale ship（改 Lpp、Beam、Depth）、Geosim（三方向等比，可指定目標 Lpp 或排水量）、Lackenby（X 向非線性縮放，達成新的方塊係數、LCB、進流段、去流段）。

### 8.9.5 DXF to Britfair（DXF 轉型值）

DXF to Britfair 把 **3D DXF** 資料轉成 Lines 可匯入的 Britfair 及相關檔案。它的主要目的是找出剖面曲線並產生 Britfair 檔：蒐集所有定義在同一 x 平面上的 POLYLINE、LINE、LWPOLYLINE，把共享同一 x 值的點排序後，輸出成一個 Britfair 剖面。**支援 AutoCAD R12 的 DXF，較新版本建議先轉成 R12**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕DXF to Britfair 對話框：輸入 DXF、重複點容差、線段容差、縮放係數、排序與建立 Lines 巨集，下方為產生的檔案訊息

*圖 8-14　DXF to Britfair 對話框與產生的檔案清單。（AVEVA 官方文件截圖，僅供內部教學）*

| 選項 | 說明 |
|---|---|
| Duplicate Point tolerance | 縮放前，距離在容差內的點視為重複並移除 |
| Linear Segment tolerance | 以弧度表示的容差，落在直線上的點被移除 |
| Scale Factor | 縮放係數，例如把 DXF 的公釐轉成公尺 |
| Sort | 剖面資料依指定的 Y/Z 座標用最近點排序 |
| Create Lines Macro | 指定巨集檔名後，產生可把 Britfair 與 3D 檔讀入 Lines 的巨集 |

產出檔案：`Sections.bri`（剖面型值）、`CC0001.3d … CCnnnn.3d`（3D 曲線資料，3 欄 x,y,z，可在 Lines 中建立 Pline、Knuckle 或 Tangent）、以及選項勾選時的巨集檔。使用方式有兩種：手動——在 Lines 新設計後，用 Create Curve 對話框的 Curve Points 頁讀入 3D 曲線、用 Design 頁讀入 Britfair 資料，再用 Fairing 對話框 Fit 頁（Interpolation 選 Design）擬合剖面；或自動——開啟 Macro Editor 載入產生的巨集並 Execute。

> **專業提醒：** DXF 轉型值只適合「已經有 3D 線框」的情況。若 DXF 裡的剖面沒有放在同一個 x 平面，或用了 R12 不支援的實體類型，轉換結果就會缺剖面。轉完後務必用 Lines 的 Section 視圖逐站檢查。

## 8.10 二次開發者怎麼接

### 8.10.1 先確認一件事：它不是 PML 世界

Initial Design 各模組是獨立桌面程式，官方文件沒有提供 PML 物件模型或 .NET API。**能寫進課程的串接點，只有文件寫明的檔案、巨集與命令介面。**下表把本章看過的可串接點整理出來，並標明依據強度：

| 串接點 | 方向 | 文件依據 | 可做什麼 |
|---|---|---|---|
| GPF 一般尺寸檔（14 行純文字） | 外部程式 → Lines／Surface／Edit Britfair | 有完整欄位 | 由專案管理系統自動產生船舶主尺度檔 |
| Britfair（`.bri`）型值檔，搭配 `.stn`、`.stm`、`.gpf` | 外部 → Lines／Surface／Digit／Edit Britfair／Calc | 有行為描述；完整欄位格式〔待核對〕 | 把外部設計軟體的型值轉成 Britfair 匯入 |
| 3 欄 `.3d` 曲線點檔、艏艉輪廓與 Knuckle 輸入檔 | 外部 → Lines | 有欄位格式（見 8.4.6） | 批次匯入控制曲線 |
| DXF → Britfair 轉換（含產生 Lines 巨集） | 外部 DXF → Lines | 有選項與輸出檔 | 把 AutoCAD 線框導入型線設計 |
| Lines Datastore 匯出／匯入（`EXPORT LINES`、`IMPORT LINES`） | Lines ↔ Surface | 有命令 | 在兩個模組間往返曲線 |
| Hull Form（DML 檔） | Lines → Surface | 有檔案名稱；內部格式〔待核對〕 | 一般不需自行解析 |
| IGES 128、VRML 2.0、Patch ASCII 網格 | Lines → 其他系統 | 有格式名稱 | 與 CAD、視覺化工具交換曲面 |
| Initial Design Geometry XML | Surface／Compartment ↔ Calc／Hydro | **文件有完整元素表** | 見 8.10.2 |
| FCT、GDS、LoadMate Fluidtnk 檔 | 外部 → Calc | 有類型與用途；欄位格式〔待核對〕 | 由其他幾何軟體餵給 Calc |
| HCL 檔 | Calc ↔ Calc | 有內容清單；欄位格式〔待核對〕 | 跨專案複製預設設定 |
| Calc Output：HTML、LaTeX、XML、LS、DXF | Calc → 外部 | 有名稱；XML 結構標示「尚未 100% 完成」 | 報表後處理、穩度手冊、轉載重電腦 |
| Hydro 的 `.wgt`、`.ls`、`.voy`、`.dat`、`.bin`、`.rat`、`.rao` | 雙向 | `.rat` 有完整欄位；其他〔待核對〕 | 試驗資料轉入、結果取出 |
| `tidexp` 匯出檔 | Project Tool 之間 | 只說是匯出檔，格式〔待核對〕 | 當作黑盒子傳遞，不建議自行解析 |
| Command Interface 與巨集（`$` 指令、`RET_n`） | 程式化操控 Lines／Surface | 有完整語法 | 以巨集批次建立曲線、檢查交點與輸出 |
| 環境變數 `SB_NAVARCH`、`SB_TID` | 部署設定 | 有說明 | 部署腳本設定專案環境 |

### 8.10.2 Initial Design Geometry XML：最值得投資的一個格式

這個檔案是官方明說的「Initial Design 各模組之間傳遞幾何與其他固定資料的首選方式」，符合國際 XML 標準，Surface／Compartment 與 Calc 都能匯出，兩者也都能匯入。對二次開發者來說，這是**最穩健的整合邊界**：結構明確、文件有欄位說明、不必碰二進位資料庫。

根元素 `tid_geometry`，下面都是選用元素：

| 元素 | 內容 |
|---|---|
| `description` | 一般說明文字 |
| `general_particulars` | 屬性 `units`（`meters` 或 `feet`），含 `main_dimensions`、`ship_classification`、`frame_table` |
| `ship_classification` | 屬性如 `yard_no`、`imo_number`、`gross_tonnage`、`net_tonnage`、`displacement`、`lightship`、`load_draft`、`ship_name`、`ship_type`、`flag`、`builder`、`year_of_build` 等；全選用，預設為空白 |
| `frame_table` | 屬性 `origin_to_frame0`（AP 至 0 號肋位的距離），含一個以上 `frame_spacing`（屬性 `from`、`spacing`，單位 m） |
| `compartments` | 屬性 `units`；含選用的 `categories` 與零個以上 `compartment` |
| `compartment` | 屬性 `id`（必填）、`name`、`description`、`type`（`facet`／`portion`／`section`／`calibration`）、`perm`（結構滲透率或裕度 %）、`damperm`（破損滲透率 %）、`buoyant`、`category`、`modified`；含 `total_volume`，選用 `min_extent`／`max_extent`，以及依類型之一：`faces`、`portions`、`sections`、`calibrations` |
| `total_volume` > `mp` | 體積性質：`volume`、`lcb`、`tcb`、`vcb`、`wp_area`、`lcf`、`tcf`、`ixx`、`iyy`、`ixy`（整體體積時水線面相關屬性為 0） |
| `faces` > `face` | 含 `vertices`（`vertex` 的 x、y、z）與 `facets`（`facet` 的索引 `i0`、`i1`、`i2`，**順序重要**）。描述三角面片 |
| `portions`／`sections` | 以 x 位置（`xposition`）與 y、z 的 `point2d` 描述截面；組成 portion 的 section 必須恰好 3 個點，其他 section 的點必須形成封閉曲線 |
| `calibrations` > `calibration` | 屬性 `sounding`（測深）、`capacity`、`lcg`、`tcg`、`vcg`、`fsm`（自由液面矩）；**須依測深遞增排列** |
| `surfaces` > `surface` | 如艙壁／甲板面，屬性 `type`：`trans_bulkhead_facet`、`deck_facet`、`long_bulkhead_facet`，含 `faces` |
| `reference_points` | 含 `unprotected_openings`、`protected_openings`、`deck_edge`、`profile`；每個 `opening` 有 x、y、z，並可有 `compid`、`compid2`（相連艙室）、`state` |
| `categories` > `category` | 屬性 `id`（必填）、`name`、`default_contents`；用來分組功能類似的艙室，如壓載水艙 |

可以怎麼用：（以下為依文件結構的**推論性建議**，非官方範例）

1. **產出端：** 從 Calc 或 Surface 匯出 XML，用任何語言（PML 之外也行）解析，取艙室容積、重心與滲透率，產生艙容表或與其他系統比對。
2. **輸入端：** 若公司有其他船型軟體，可寫轉換器把它的艙室與面片寫成 `tid_geometry` 檔餵給 Calc。校驗重點：面片頂點索引順序、`calibration` 排序、portion 的 3 點限制。
3. **品質閘門：** 用腳本檢查 XML 內所有 `compartment` 是否都有 `perm` 與 `damperm`、單位是否一致、`total_volume` 是否為正，作為 Calc 前的前置驗證。〔待核對：缺值時 Calc 的預設行為，請用你們版本實測〕

### 8.10.3 巨集與命令介面的自動化

Lines 與 Surface 的巨集是官方明文支援的自動化機制：`$MAC` 或 `@巨集名` 執行，`$DO`、`$IF`、`$GOTO`、`$SET`、`$INQUIRE` 提供流程控制，`$VARIABLE` 宣告變數，`$LOG` 開啟工作階段紀錄。實際可做的批次工作包括：

- 把專案外來資料（DXF 轉出的 `.3d`）批次讀進一個新 Lines 設計（DXF to Britfair 已能自動產生這種巨集，可當成學習範本）。
- 對一批剖面站求相交（`INTERSECT SECTION n WITH FOS` 並讀回 `RET_1`..`RET_3`）。
- 在 Surface 建立參數化附屬體（官方明說可用巨集）。
- 用 `$LOG` 紀錄整段操作，當作可稽核的設計歷史。

**限制：** 本章深讀的頁面只涵蓋指令介面的通則與兩三個範例，完整指令清單與每個指令的參數在各模組 Command Reference，本章未逐一核對。**不得假設兩個模組的指令相同。**〔待核對：Surface 與 Calc／Hydro 是否支援非互動（batch／headless）執行，文件本章未見說明。〕

### 8.10.4 不建議做的事

| 做法 | 理由 |
|---|---|
| 直接解析 `CALC`、Lines／Surface Datastore 或 `tidexp` | 官方未公開其內部格式；版本變更時極容易壞掉 |
| 在 Calc 外部「修補」幾何 | Calc 的資料一致性靠「幾何只能從幾何建模程式改」維持 |
| 跳過釋出，直接複製 `tid` 資料夾給下游 | 釋出同時處理 databank 與登錄；手動複製會讓兩邊不一致 |
| 假設釋出會自動通知下游 | 下游要在開啟設計時被提示更新依賴，沒有自動推送 |

## 8.11 本章小結

1. Initial Design 是整體船體設計的**前段**：把型值轉成型線與曲面，再切成艙室，最後算靜水力與水動力；它輸出的是「幾何骨架」，鋼構件在 Structural Design／Hull。
2. 七個模組之間靠兩個動詞銜接：**釋出（Release）與使用（Use）**。沒釋出，下游就看不到；釋出之後下游使用的是那一版，不會隨你繼續修改而改變。
3. 專案分**獨立**與**納入 PIM**；`SB_NAVARCH`、`SB_TID` 決定設計與 databank 的位置，Project Tool 管理專案、設計、依賴、匯出匯入與關聯。
4. Lines 以 **B-Spline** 描述型線，整修靠曲率判斷與折角／節點控制；水線端部靠端面與過渡曲線；整修完成後以 **Hull Form Definition** 釋出。
5. Surface 以 ACIS／NURBS 處理附屬體、融合、布林運算與縮放；Compartment 在其上用 **Envelope** 建立內部曲面與艙室，並以 **SAC** 驗證，再釋出 **Calculation Geometry**。
6. Calc 是**評估模組**，幾何不可在其內修改，只能改艙室名稱與滲透率；它以面片計算體積性質，用喪失浮力原理做破損穩度，輸出多種報表格式。
7. Hydro 涵蓋 Powering、Manoeuvring、Seakeeping、Dynamic Positioning，資料檔多、計算鏈長。
8. 二次開發者的串接點是**檔案**：Initial Design Geometry XML 與 GPF 最適合當整合邊界；Britfair、DXF 轉換、巨集與命令介面為輔；二進位資料檔與 `tidexp` 當黑盒子。

## 8.12 練習題與自我檢核

1. 畫出 Initial Design 七個模組之間的釋出與使用箭頭，並標出每個箭頭傳遞的資料名稱（Hull Form、Design、Calculation Geometry）。
2. 一個獨立專案放在遠端設計代理商，船廠要拿來做 Structural Design。列出你要做的步驟（匯出、匯入、關聯、設環境變數、釋出、Initiate Hull Standards 登錄），並說明船廠端需不需要 Initial Design 授權。
3. 為什麼 Lines 設計要用 Hull Form Definition 而不是直接把整個設計釋出？
4. 說明 B-Spline 的「折角（Knuckle）」是什麼；在從型值表產生粗略曲面時，為什麼剖面之間的折角數量必須相同？
5. 你拿到一個 Britfair 檔，裡面兩個點相距 0.05 mm。Surface 會怎麼處理？
6. 甲板產生失敗，列出至少兩個先要檢查的前置曲線。
7. 在 Compartment 中，Envelope 由哪三種東西組成？Envelope 有破洞時，如何用 IDENTIFY FLASH 找出？
8. 用 SAC 檢查艙室：如果艙室曲線超出 Envelope 曲線代表什麼？低於呢？哪種情況可以被接受？
9. 說明 Calculation Geometry 與 Design（結構設計用）的差別，並列舉兩種「不必釋出為 Calculation Geometry」的內部曲面。
10. 在 Calc 裡你發現某個艙室形狀錯了。你可以直接在 Calc 改嗎？應該怎麼做？
11. Calc 的 Calculate 與 Recalculate 差別在哪？什麼情況下一定要用 Recalculate？
12. 寫出 Initial Design Geometry XML 的根元素與其下五個選用元素；`compartment` 的 `perm` 與 `damperm` 各是什麼？
13. 列出 Hydro 的四類計算，並指出哪一類的計算鏈最長（需要先算規則波、再算不規則波、最後算長期）。
14. 為什麼說「Calc 的靜態波浪彎矩」不能直接當動態載荷？
15. 設計一個「Britfair 轉 Geometry XML 前置驗證腳本」：列出要檢查的五項規則（例如單位、頂點索引順序、重複點、calibration 排序、滲透率）。標出哪些規則有官方依據、哪些屬於推論〔待核對〕。
16. 為什麼不建議直接解析 `CALC` 或 `tidexp` 檔？若確實需要它們的資料，有哪些替代的輸出管道？

## 8.13 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 8 章](appx_d_verification_zh-TW.reading.html#ch08)；取材覆蓋與未讀範圍：見[附錄 E 第 8 章](appx_e_coverage_zh-TW.reading.html#ch08)。
