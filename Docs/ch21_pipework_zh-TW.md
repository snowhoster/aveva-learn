# 第 21 章　管路設計（Pipework）：從 PIPE／BRAN 到 Spool、Isometric 與管支架

> 第 7 章用一節篇幅介紹過 `PIPE`、`BRAN` 與元件的資料結構。這一章把管路當成一門完整的設計工作來看：**設計者從建立 Pipe 開始，經過佈管、檢查、穿孔、拆分、預製管段（Spool）、生產檢查、管段圖與等角圖，最後走到管支架（Hangers and Supports）。**
>
> 管路是舾裝裡資料量最大、規則最多、也最容易被二次開發盯上的領域：材料表、管段清單、焊口、彎管 NC 資料，全都從這裡長出來。開發者若不懂設計者每一步在做什麼，寫出來的工具很容易讀到「尚未完成」的資料，或在錯的階段改動模型。
>
> **資料可信度：** 本章的操作流程、視窗與選單名稱、元素型別與屬性名（例如 `PIPE`、`BRAN`、`TUBI`、`SPLDRG`、`SFLimit`、`BendMacReference`、`REST`、`HANG`），取自 AVEVA Marine 12.1 官方離線文件的 *Pipework* 與 *Pipework Support Design* 兩大章節。該文件原為 PDMS 時代的使用者指南，12.1 版沿用，故部分頁面仍寫 PDMS、SPOOLER、ISODRAFT 等舊名稱，本章照原樣保留。官方文件是操作手冊，**幾乎沒有 PML 指令或程式範例**；因此「二次開發者可以怎麼取資料」一欄，只在文件有提到屬性或元素名稱時才寫，其餘一律標〔待核對〕，需要在你們公司的版本與訓練專案實測。HEAD／TAIL 相關屬性縮寫（如 `HREF`、`TREF`）沿用第 7 章的整理，同樣屬於〔待核對〕範圍。

## 21.1 學習目標

讀完本章，你應該能夠：

1. 畫出管路資料階層 `WORLD → SITE → ZONE → PIPE → BRAN → 元件`，並說明每一層的責任。
2. 說明 Pipe 與 Branch 各自可以設定哪些預設值（Pspec、Bore、Insulation、Tracing、Temperature、Pressure、Slope Ref），以及「等級向下傳遞」的規則。
3. 依步驟建立 Pipe 與 Branch，定義 Head／Tail 的位置、口徑、連接型式與流向，並區分「已定位」與「已連接」。
4. 說明元件建立與佈管的順序，並知道直管（`TUBI`）是由系統隱含產生的。
5. 區分 Quick Pipe Routing 與 Pipe Router 的適用情境與前置條件。
6. 說明管路穿孔為何需要 Hole Management，以及請求、核准、產生實際孔洞的資料流程。
7. 執行 Disconnect／Reconnect、修改規格與口徑、Split／Merge 等修改作業，並知道各自的限制。
8. 說明 Spooling 的 SPOOL／FIELD／Spool Break／Shop Flag 概念，以及 Production Checks 的檢查對象。
9. 說明 Pipe Sketch、Isometric 預覽與 Pipe Fabrication 四階段（建模、Spooling、檢查、圖面與輸出）的關係。
10. 說明管支架的資料階層（`REST`／`HANG`／`FRMW`／`SBFR`）與建立流程，並指出各階段二次開發者可讀取的資料。

## 21.2 管路設計全貌

### 21.2.1 流程總覽

```
建立 Pipe/Branch ─► 定 Head/Tail ─► 放元件/佈管 ─► 檢查(干涉、一致性)
        │                                              │
        ▼                                              ▼
   穿孔請求 ◄──────────────── 修改 / 拆分 ◄───────── 修正
        │
        ▼
   Spooling(SPOOL/FIELD) ─► Production Checks ─► Pipe Sketch / Isometric
        │                                              │
        ▼                                              ▼
   Pipe Fabrication 匯出(NC XML)                管支架設計(REST/HANG)
```

官方把管路相關功能放在 Design 模組的 Pipework 應用程式，並提供 Pipework Toolbar 作為入口；Spooling 與 Pipe Sketch 則牽涉 Fabrication 資料庫與 Draft／ISODRAFT。

> **專業提醒：** 開發者最常犯的錯，是在設計還在變動時就讀管段資料。管路資料有明確階段：設計中、已 Spooling、已通過 Production Checks；先問「這條管現在在哪個階段」，再決定能不能取資料。每節的「二次開發觀點」說明可取的資料與待核對項目。

## 21.3 資料階層

### 21.3.1 嚴格的建立順序

官方強調：資料庫元素都由其他元素擁有，必須依嚴格順序建立。所有設計專業共用的是 `WORLD`、`SITE`、`ZONE`；管路專屬的是以下三層：

| 層級 | 元素 | 官方描述的角色 | 本課程類比 |
|---|---|---|---|
| 管線 | `PIPE` | 管理性元素，可擁有多個 Branch，共用一組預設管等級，可有任意多個端點 | 管線號主檔 |
| 分支 | `BRAN` | 擁有一段由管路元件組成的管，有已知的 Head 與 Tail | 有序串列 |
| 元件 | 各種管件／閥件 | 決定管路的形狀與幾何；可從 Head 走到 Tail，也可連到其他 Branch（例如三通） | 串列節點 |

```
WORLD
└─ SITE
   └─ ZONE                 (建 Pipe 前，World/Site/Zone 必須已存在)
      └─ PIPE
         ├─ BRAN           主管
         │   ├─ FLAN / ELBO / VALV ...
         │   └─ TEE ───────┐
         └─ BRAN           支管 ◄┘  (Head 連到三通)
```

## 21.4 預設管等級（Pspec）、口徑與保溫伴熱

### 21.4.1 Pspec 的概念

目錄（Catalogue）中所有管等級（piping specification）都會出現在 Default Specification 視窗。**目前選定的預設等級，決定你能從目錄選到哪些元件。** 為了避免每個元件都重選一次，預設等級可以設在 Pipe 或 Branch 層級，往下層自動沿用，直到有人改掉為止，官方稱為 cascade（向下傳遞）。

在 Pipework Toolbar 按 Set Default Pipe Specification 開啟視窗，可同時選擇等級、保溫與伴熱規格。官方範例等級代號：

| 代號 | 說明（官方範例） |
|---|---|
| `A1A` | ANSI class 150 碳鋼 |
| `A3B` | ANSI class 300 碳鋼 |
| `F1C` | ANSI class 150 不銹鋼 |

這些是範例；你們公司的實際等級代號以自己的 Catalogue 為準。

### 21.4.2 Pipe 層級的設定項目

建立 Pipe 時（見 21.5）會看到下列欄位：

| 欄位 | 預設值 | 意義 |
|---|---|---|
| Pipe Name | `PIPE` | 管線名稱 |
| Primary System | No System | 所屬主系統 |
| Pipe Specification | 沿用 Default Pipe Specification | 可為個別 Pipe 另選 |
| Bore | 未設定 | 公稱口徑；**不影響路徑** |
| Insulation | None | 保溫規格 |
| Tracing | None | 伴熱規格 |
| Temperature | -10000 degC | 此值代表「忽略溫度」 |
| Pressure | 0 pascal | 設計壓力 |
| Slope Ref | 無 | 坡度參考屬性 |

> **專業提醒：** `-10000degC` 與壓力 `0` 都是「沒有填」的哨兵值。開發者讀取溫度與壓力做報表時，必須先排除這些值，否則材料表會出現 -10000 度的管線。

新的保溫或伴熱規格不是設計者自己建的，官方一再提醒要找系統管理員（見第 20 章）。

### 21.4.3 一條管線內要換等級怎麼辦

官方註明：Branch 之下之後建立的所有元件都使用該規格。**若同一條管線內需要不同等級，必須在換等級的位置另建一個 Branch。** 這是等級邊界（spec break）在資料模型中的做法，很重要。

## 21.5 建立 Pipe 與 Branch

### 21.5.1 建立 Pipe

1. 在 Design Explorer 選到正確的 Zone。
2. Pipework Toolbar 按 Show pipe creation form，開啟 Create Pipe 視窗。
3. 填 Pipe Name、Primary System、等級、Bore、Insulation、Tracing、Temperature、Pressure、Slope Ref。
4. 按 Apply。系統會**同時建立一個 Pipe 與一個 Branch**，並顯示 Modify Pipe 視窗讓你定義 Branch。
5. Cancel 會放棄輸入並關閉視窗。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Pipe 視窗

*圖 21-1　Create Pipe 視窗：填入管名、等級、口徑、保溫、伴熱、溫度與壓力。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.5.2 Modify Pipe 視窗：雙用途

Modify Pipe 視窗既用於新建 Branch 的細節與連接，也用於修改既有 Branch。重要區塊與按鈕：

| 區塊／按鈕 | 用途 |
|---|---|
| Connectivity 窗格 + New Branch | 在目前的 Pipe 下新增 Branch |
| Change Detail | 改規格（Pipe 或 Branch 層級） |
| Set Pipe | 把另一個 Pipe 設為 CE（Current Element，目前元素） |
| Head Detail／Tail Detail + Change | 明確指定端點的位置與細節 |
| Head Connection／Tail Connection + Change | 把端點連到元件、管嘴或其他 Branch |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Modify Pipe 視窗

*圖 21-2　Modify Pipe 視窗：Connectivity 窗格、Head 口徑、連接與位置。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.5.3 定義 Head 與 Tail 的細節

在 Head Detail 按 Change 後，可設定：

| 項目 | 說明 |
|---|---|
| Bore | 從目錄提供的口徑清單選擇 |
| Connection | 從目錄提供的連接型式清單選擇 |
| Direction | 自 Head 離開時的流向。官方定義：**Head 方向是流動方向，Tail 方向是它的相反** |
| Position wrt World | 以世界座標明確輸入；右鍵 Format 可切換格式；可用 Offset By 輸入偏移；Pick Position 在 3D 視圖點選 |
| Copy To Head | 複製管路的 Head |

按 Apply 後，端點被**定位但尚未連接**，連接狀態可在 Connectivity 窗格看到。

### 21.5.4 定義連接

Head／Tail Connection 可以連到三通等元件、設備管嘴（nozzle），或另一個 Branch。作法：按 Pick 在 3D 視圖點選，或從 List of connections 選取。規則：

- 只有「尚未連接」的元素可以被選。選到已連接的元素會報錯。
- Pick 後會出現可用連接清單；只有當清單項目為 Unset 時，Connect 按鈕才可用。
- 連接完成後，Branch 暫時是一段 Head 到 Tail 之間的單一直管，以**紅色虛線**顯示，代表路徑在幾何上尚不正確。

> 〔公開版未收錄：AVEVA 官方產品截圖〕路徑未定義的 Branch 以虛線顯示

*圖 21-3　Head 與 Tail 已連接但路徑未定義時，Branch 以紅色虛線顯示。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.5.5 非標準分支連接

有時支管是接在主管表面任意一點，例如開孔後把支管焊上去。官方稱為 Non-standard 連接：

| 項目 | 說明 |
|---|---|
| 連接點 | 元件上的笛卡兒點 `PIPCA`；管對管則用 Pipe Tapping `PTAP` |
| 目錄需求 | 不需在等級中另設 TEE／OLET 元件，但需要 AVEVA 提供的 `/General-Tappings` 規格（位於 AVEVA MAS 專案的 `MASTER/PIPECATA`） |
| 操作 | 先建立並定位連接點，再「連接既有 Branch」或「建立新 Branch」 |

這類連接與預製的 excess（餘量）有關，見 21.13。

### 21.5.6 二次開發觀點

| 要取的資料 | 文件依據 | 備註 |
|---|---|---|
| Pipe 的規格、保溫、伴熱、溫度、壓力 | Create Pipe 欄位名稱 | 對應的 PML 屬性名稱〔待核對〕 |
| Branch 的 Head／Tail 位置、口徑、連接、流向 | Head／Tail Detail 欄位 | 屬性縮寫（`HPOS`／`TPOS`／`HBOR`／`HREF`／`TREF` 等）見第 7 章 7.4.2〔待核對：Marine 12.1 實測〕 |
| 未連接的端點 | 「Unset」連接狀態 | 常用於寫「找出所有未連接 Branch」的檢查工具〔待核對〕 |

> **專業提醒：** 「已定位」與「已連接」是兩件事。定位只是座標對了，連接才建立參照。移動設備後，定位的端點不會跟著動，連接的才會（見 21.8 Reconnect）。

## 21.6 管路元件與路由

### 21.6.1 建立元件的流程

官方示範以「一種元件」為例，說明其餘元件的流程相同：

1. 在 Branch（或其下元件）層級，按 Show pipe component creation form 開啟 Component Creation 視窗。
2. 視窗顯示目前等級可用的所有元件。可改選替代等級、保溫與伴熱後按 Done。
3. 從 Component Types 選元件種類，並以 Filter By 依子型式篩選（例如法蘭種類）。
4. 選擇建立方向：預設沿流向（Head → Tail），也可逆流向。
5. 兩個關鍵勾選：

| 選項 | 作用 |
|---|---|
| Auto. Create Adjacent | 自動判斷是否需要相鄰元件（例如閥門旁的法蘭與墊片）並選擇適當者 |
| Skip Connected Comps. | 自動判斷哪些元件已連接，並概略定出建立點 |

6. 按 Connect 把元件接到前一個元件或 Branch 的 Head／Tail；接反了用 Flip Components 翻轉。

通常從 Head 開始依序加元件，定位與定向後一路到 Tail；若要插入元件，先導覽到插入點之前的元件，再建立新元件。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Component Creation 視窗

*圖 21-4　Component Creation 視窗與可用的元件種類。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.6.2 隱含直管 TUBI

官方明確寫道：**直管不是明確建立的**，而是在相鄰元件之間自動隱含產生，在 Design Explorer 中顯示為 `TUBI`，在 3D 視圖中顯示為隱含管（implied tubing）。

| 動作 | 結果 |
|---|---|
| 移動一個彎頭 | 前後 `TUBI` 長度自動改變 |
| 刪掉一個元件 | 兩側的 `TUBI` 合併重算 |
| 想「畫一段直管」 | 不能；用元件位置控制 |

元件的定位與定向使用 Model Editor，或 Piping toolbar 的 Align selection/component 與 Direct selection/component。

> 〔公開版未收錄：AVEVA 官方產品截圖〕3D 視圖中的隱含直管

*圖 21-5　元件之間自動隱含產生的直管（implied tubing）。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.6.3 二次開發觀點

- `BRAN` 的元件有順序，順序即流向，這是第 7 章 7.4.5 範例的基礎。
- `TUBI` 是 Design Explorer 看得到的元素型別，但它是隱含產生。要讀直管長度，應以相鄰元件的出入口點推算，或讀 `TUBI` 本身〔待核對：`TUBI` 能讀取哪些屬性〕。
- Pipe Assemblies（元件與 Branch 的完整複本）可重複使用常見管組，也用於 Pipe Splitting；自動建立元件的 PML 指令〔待核對〕，請查 Marine 12.1 指令參考。

## 21.7 Quick Pipe Routing 與 Pipe Router

### 21.7.1 兩種路由工具的差別

| 項目 | Quick Pipe Routing | Pipe Router |
|---|---|---|
| 性質 | 互動式，設計者用滑鼠逐段決定方向 | 規則式，可自動佈單一或多條管 |
| 前提 | Head 與 Tail 已定義，路徑未定義 | Pipe、Branch 已建立，Head／Tail 已連接或定位，口徑已定義；若 Branch 已有元件，需被選取 |
| 輸出路徑 | 設計者控制，可含非正交（坡度） | 正交、彎頭最少、盡可能無干涉 |
| 入口 | Model Editor 模式的 Quick Routing Handle | Utilities > Pipe Router |
| 適合 | 少量、特殊、需要斜管 | 大量標準管線 |

### 21.7.2 Quick Pipe Routing 的操作與診斷

當 Head 與 Tail 已定義但路徑未定義時，Branch 以**虛線**顯示（官方稱 ill-defined route）。常見的原因有：

- 相鄰元件的離開與到達方向不匹配（受設計容差：偏移、角度、比例影響）。
- Head 或 Tail 未定義或定義不完整：端點屬性仍為預設（unset），或端點有參照但位置不在該參照物上。

操作：點選虛線（變綠色），從主選單切換到 Model Editor，此時 Head 與 Tail 會出現 Quick Routing Handle，用滑鼠與 Model Editor 選項拉出路徑。方向改變處會自動插入彎頭或彎管（依等級而定）；在方向把手上右鍵，選 Component Choice > Use Elbows 可指定用彎頭。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Quick Pipe Routing 的路由把手

*圖 21-6　Quick Routing Handle 與 End Route Handle。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.7.3 Slope（坡度）

一般管路走水平與垂直，但排水管等需要坡度。官方的說法：可以設定元件的離開方向使連接到下一個元件的管子達到指定坡度，但**只適用於 Branch，以及幾何有方向改變且角度可變的元件（如彎頭）**。另有新功能可對現有 Pipe（含所有 Branch 與元件）套坡度：

| 入口 | 視窗 |
|---|---|
| Branch Slope | AutoSlope 視窗 |
| Pipe Slope | Slope Pipe 視窗 |

官方也註明：Quick Pipe Routing 的 Model Editor 選項**除了 Slope 功能以外**，Slope 只在 Piping 應用程式提供。

### 21.7.4 Pipe Router 的運作

Pipe Router 從 Branch 的 Head 出發，結束於 Tail，沿路定位並定向元件（例如縮管與焊口），必要時加入法蘭與墊片等連接元件。**流向固定是 Head 到 Tail**。可用 routing point、plane、rule、pipe rack 限制路徑，路徑建好後仍可手動修改。所有 Pipe Router 工作都從中央的 Pipe Router 視窗（任務樞紐，task hub）啟動；其管理（Automatic Pipe Routing Administration）是獨立子樹，屬管理者設定規則的範圍。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Pipe Router 視窗

*圖 21-7　Pipe Router 視窗（任務樞紐）。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.7.5 二次開發觀點

| 問題 | 說明 |
|---|---|
| 能不能用程式觸發 Pipe Router？ | 官方文件只提供視窗操作，沒有指令；〔待核對〕Marine 12.1 是否提供可從 PML 呼叫的路由指令 |
| 能不能判斷「路徑是否還是虛線」？ | 文件描述的是畫面狀態；對應的資料屬性〔待核對〕，可改以「端點是否 unset／連接是否為空」近似 |
| 路由前資料檢查 | Define a Route 的前置條件（Pipe、Branch、端點、Bore）可寫成預檢工具，避免使用者在視窗裡才遇到錯誤 |

> **專業提醒：** 自動路由是輔助工具，不是設計決策。Pipe Router 只保證正交與最少彎頭；是否符合工藝配置、維修空間與支架位置，仍要設計者檢查。

## 21.8 修改管路

### 21.8.1 常見修改作業

| 作業 | 入口與步驟摘要 | 注意事項 |
|---|---|---|
| 斷開（Disconnect） | 選 Pipe 或 Branch，按 Show pipe modification form；Set Pipe 設為 CE；在 Head Connection 按 Change，再按 Disconnect | Head 與 Tail 操作相同，Back 可放棄 |
| 重新連接（Reconnect） | 對**被移動過的設備**，同樣步驟後按 Reconnect | 設備被搬動後常用 |
| 修改 Pipe 基本資料 | Change Detail，內容與 Create Pipe 視窗相同 | 見 21.4.2 |
| 修改 Branch 資料 | 同上，但針對 Branch | 規格改動只影響之後建立的元件？〔待核對〕 |
| Pipe Modification | 修改選定 Pipe／Branch 的口徑或規格，也可設保溫與伴熱 | 官方功能描述 |
| 修改元件／方向 | Modify 子樹有 Component 與 Orientate Component | 〔待核對〕詳細欄位本章未展開 |
| 坡度 | 與 21.7.3 的 Slope 相同 | — |

### 21.8.2 Pipe Splitting 與 Merge

設計完成後，常因專案規定或圖面清晰度需要把管線拆成多個 Branch 或 Pipe。官方列出可拆分的方式：**依元件、依平面、依 Spool**。所有拆分作業從 Utilities > Pipe Splitting 開啟的 Split Pipe 視窗啟動，預設顯示 Split/Merge 頁籤。

待拆分的元素可用以下方式加入清單：

| 按鈕 | 作用 |
|---|---|
| Add Ce | 把目前選取的元素加入 |
| Add Selected | 在 3D 視圖點選一或多個 Branch，Esc 結束 |
| ID Selection | 在 3D 視圖一次點選多個 Branch |
| Clear all | 清空清單 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Split Pipe 視窗

*圖 21-8　Split Pipe 視窗（Split/Merge 頁籤）。（AVEVA 官方文件截圖，僅供內部教學）*

合併（Merge）時，在 Merge Unit 選 One Pipe（合併成一條 Pipe）或 One Bran（合併成一個 Branch），按 Merge 後依提示在 3D 視圖先點來源元件、再點目標元件。限制：

- 要合併的區段必須與目前元素**共線**（以起點與終點連線為準）。
- 合併後所有材料屬性取自 CE 的設定。
- 無法合併時會顯示錯誤；可按 Flow 檢視目前流向、Undo 放棄、Dismiss 關閉。

## 21.9 管路穿孔與 Hole Management

### 21.9.1 為什麼需要管控

船體甲板、艙壁、地板上開孔，會影響結構完整性與成本，因此不能讓管路設計者自己動手。官方描述的專業分工：甲板與壁板由結構部門建立，存在別的資料庫，管路設計者對它只有讀取權限。需要一套「請求、核准、駁回」機制，這就是 Hole Management。

### 21.9.2 資料流程

```
管路設計者                              結構設計者(面板擁有者)
  │ 在設計應用程式指定孔位與大小
  │ ──► 在 PANE 上建立「虛擬孔」
  │       = FRMW + 2 個 FIXING + ASSOC
  │ 進入 Hole Management 提出請求 ─────►  審查
  │                                        │ 核准: 建立實際孔洞 PFIT(屬 PANE)
  │ ◄───────────────────────────────────── │ 駁回: 回報狀態
```

| 元素 | 角色 |
|---|---|
| `FRMW` + 兩個 `FIXING` | 虛擬孔本體；每個 `FIXING` 有 `Spref`，指向目錄中的孔定義 |
| `ASSOC` | 關聯元素，參照所有構成孔的元素 |
| `PFIT` | 核准後產生的實際孔洞，由 `PANE` 擁有 |

Hole Management 應用程式做三件事：依權限確保只有合適的人能建孔、對管控中的孔做驗證與回報狀態、產生報表。只有通過驗證的孔才能核准；歷史與狀態會被儲存。若是結構穿孔，申請者與核准者可由同一位結構設計者擔任，若公司要求分離，需靠 DAC（第 20 章）管控。

### 21.9.3 二次開發觀點

這是與第 7 章 7.9 互相呼應的好題目：孔洞有明確的元素型別與狀態，非常適合做追蹤報表。

| 要做什麼 | 文件依據 | 備註 |
|---|---|---|
| 列出某區域的待核准孔 | 文件說明「狀態與歷史會被儲存」 | 狀態屬性名稱〔待核對〕 |
| 找出虛擬孔 | `FRMW` + `FIXING` + `ASSOC` 結構 | 以元素型別與 `Spref` 篩選〔待核對〕 |
| 檢查孔與管徑 | `Spref` 指向孔定義 | 孔尺寸與管外徑加餘隙是否足夠，是應用層規則，不是官方功能 |

> **專業提醒：** 不要在工具裡直接建立 `PFIT` 來繞過核准。這會破壞責任分工與稽核紀錄。

## 21.10 設計檢查與輸出

官方指出，設計者要檢查管路佈置的錯誤與不一致，包括**干涉（spatial interference）**；解決後輸出設計資料報表並產生等角圖。這些功能在所有 Design 應用程式都可用，可跨專業一併檢查。

與 Spooling 相關的一致性檢查，見 21.12.2：SPOOLER 在一致性檢查有「錯誤」時無法正常運作，但「警告」不影響。

| 檢查 | 入口 | 備註 |
|---|---|---|
| 資料一致性 | Utilities > Data Consistency（Spooling 前使用） | 以 ZONE 為 CE |
| 干涉 | Check and Output Design Data 子樹 | 〔待核對〕本章未深讀，入口與規則請查原頁 |
| 報表 | 官方提及 Reports Utility | 範本與欄位〔待核對〕 |

## 21.11 Isometrics Preview

在不離開應用程式的情況下，可預覽管系統或個別管的等角圖，效果如同由 ISODRAFT 產出。

| 入口 | 內容 |
|---|---|
| Utilities > Show Pipe System | 在 3D 視圖醒目標示 CE，便於確認要預覽的管 |
| Utilities > Pipe Isometric | 單一管的等角圖：標註、尺寸、材料表、標題、管線用途與符號說明 |
| Utilities > System Isometric | 以 CE 為基礎的系統等角圖（目前未顯示於 3D 視圖的元素也會加入）；若 Pipe 有多個 Branch，每個 Branch 分頁顯示 |

Preview Isometric Drawing 視窗另有自己的工具列（〔待核對〕按鈕細節）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕管等角圖預覽

*圖 21-9　Preview Isometric Drawing 視窗中的管等角圖預覽。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 預覽只是預覽，不等於正式出圖。正式的 Isometric 由 ISODRAFT 或 Pipe Fabrication 的 Fabrication Isometrics／Installation Isometrics 產生（21.15）。

## 21.12 Pipework Spooling

### 21.12.1 概念

官方描述 SPOOLER 為管路 Spooling 模組：把管路設計切成適合預製的邏輯區段，再用 ISODRAFT 輸出為等角圖。它處理的是 **Spool Drawing（`SPLDRG`）**：由設計者選取一組相互連接的元件網路加入圖中，系統檢查是否為有效網路。

| 名詞 | 定義 |
|---|---|
| `SPLDRG` | Spool Drawing，裝一組完整的 SPOOL 與 FIELD；**Spool 不能橫跨兩張 Spool Drawing** |
| SPOOL | 預製時接合的一連串元件與直管 |
| FIELD | 在船上安裝階段才接合的單一或一組元件 |
| Spool Break | Spool 的分界，通常在 Shop Flag 改變處由系統決定 |
| Shop Flag | 標示元件是預製（SHOP，為真）還是現場安裝（FIELD，為假） |
| `SFLimit` | `SPLDRG` 的屬性，設為 `BRAN`、`PIPE`、`ZONE` 或 `SITE`（預設為 `WORLD`），則在對應層級的任何變動處強制 Spool Break |

選取元素時，系統向外尋找所有相連的元件與直管，把與它 Shop Flag 相同的相鄰元件歸入同一個 Spool 或 Field。也可以用**現場焊口（Field Weld）或接頭（Joint）**強制 Spool Break；例如一個沒有墊片的法蘭接頭。

### 21.12.2 準備與資料庫

SPOOLER 使用兩個資料庫：

| 資料庫 | 內容 | SPOOLER 的權限 |
|---|---|---|
| Fabrication database | 全部 Spooling 資料 | 完整讀寫，可建立階層與增刪元素 |
| Design database | 專案的設計資料 | 只能改與預製有關的屬性（例如指定現場焊口） |

Spooling 前的建議：

1. 在 Design 中先確認資料一致性，必要時補上明顯需要的 Shop／Field Weld。
2. 把 `ZONE SPOOLER-PIPE` 設為 CE，執行 Utilities > Data Consistency。
3. 一致性檢查有錯誤時 SPOOLER 無法正常運作；警告不影響。

### 21.12.3 管段（Pipe Piece）與管預製段（Pipe Spool）

Pipework Spooling 子樹中有 Pipe Piece and Pipe Spool Data、Pipe Spool Manager 與 Pipe Spool Reporting Data，涵蓋底層物件與資料庫屬性、偽屬性（pseudo-attribute）。本章的摘要如下：

| 名詞 | 官方定義 | 誰建立 |
|---|---|---|
| Pipe Piece | 管中最低層的預製單元：一段可由庫存材料製作的連續管；記錄起點與終點元件的參照 | **系統推導，使用者不能建立或刪除** |
| Pipe Spool | 管或 Branch 的預製部分，通常在工廠焊接後送到現場；常見為兩端焊法蘭的彎管，也可含分支、縮管、閥門；**不包含墊片** | **系統推導，使用者不能建立或刪除** |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Pipe Piece 示意

*圖 21-10　Pipe Piece 示意：兩端元件不屬於該 Pipe Piece，僅被參照。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Pipe Spool 示意

*圖 21-11　Pipe Spool 示意：墊片不包含在 Spool 內。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.12.4 二次開發觀點

Shop／Field 狀態的屬性名稱〔待核對〕；Spool 清單與焊口數見 Pipe Spool Reporting Data 子頁的偽屬性〔待核對〕。Pipe Piece 與 Pipe Spool 由系統推導，**不要寫工具去建立或刪除**；要改變它們，改上游的 Shop Flag、焊口、Spool Break 與元件位置。

## 21.13 Production Checks

### 21.13.1 檢查什麼

Production Checks 檢查 Pipe Piece 與 Pipe Spool 是否已具備生產條件：

- 對焊接機與彎管機的限制。
- 圖面與報表上的管子切割長度。
- 庫存管材的定長（stock length）。

官方註明：目前的製作機只限於彎管與自動焊接。

> **重要限制：** Pipe Fabrication 是預設功能，Production Checks 與 Pipe Fabrication **互不相容**，由 `evars.bat` 內的環境變數 `PRODUCTIONCHECKSENABLED` 決定啟用哪一個。系統管理員在安裝時要先確認公司採用哪一套（見第 20 章）。

### 21.13.2 操作方式

在 Design 模組的 Pipework 應用程式，選 Utilities > Production Checks 開啟 Pipe Production Checks 視窗（任務樞紐）。條件與限制：

| 條件 | 說明 |
|---|---|
| 對象 | 必須是**已經建立 Spool 的 Pipe**；不能對目前層級「隨便」執行 |
| 層級 | 目前元素必須是 Pipe，或 Pipe 之下的 Branch／元件 |
| 前置 | 先用 Setup Production Checks 設定檢查參數 |
| 結果 | 視窗流程中會依選擇出現其他視窗，結束後回到主視窗繼續 |

Production Checks 子樹還包含 Individual Renaming、Automatic Flange Alignment、Fabrication Machine 與 Database Support，本章不展開〔待核對〕。

### 21.13.3 Fabrication Machine

製作機器的測試請求由 Fabrication Machine Manager 處理，可取得焊接與彎管機的操作資訊與對應的活動表（activity tables）。

### 21.13.4 二次開發觀點

- 如果你要做「批次檢查工具」，先看 Pipe Fabrication 的 Spooling and Checks（21.15）：官方描述它應該能**互動**與**整批**（從 Block、Area 等 Explorer 層級取清單）兩種模式執行。
- 檢查結果的資料格式〔待核對〕。
- 常見錯誤類型（官方列出）：最小彎管距離不足、與底部或彎管機或碰撞平面衝突、擠出機高度不足、焊口間最小距離不足。可作為你設計報表分類的依據。

## 21.14 Pipe Sketch 與 Pipe Spool Drawing

### 21.14.1 Pipe Sketch 是什麼

Pipe Sketch 可在 Automatic Drawing Production（ADP）中，依**已通過生產檢查的 Spool 資料**自動產生；內容是 Spool 的尺寸標註比例圖，加上相關製造資料表。

| 功能 | 說明 |
|---|---|
| Pipe Sketch 應用程式 | 不必關閉 Design — Pipework 再進 Spooler，就能對有效 Spool 建立 Spool Drawing，並顯示或清除管尺寸 |
| Pipe Spool Drawing 視窗 | Pipe Fabrication > Drawings > Spool Drawings，是建立、修改、列印、設定與處理錯誤的任務樞紐 |
| 底圖（backing sheet）與覆蓋圖（overlay） | 不是在此應用程式定義，需參考 Draft Administrator 的 Sheet Library Administration |
| Drawing Template／Administration | 子樹中有 Drawing Template 與 Pipe Spool Drawing Administration，屬管理者設定〔待核對〕 |

### 21.14.2 Pipe Fabrication 的三種圖

| 圖 | 用途 |
|---|---|
| Pipe Spool Drawings | 預製管段圖 |
| Fabrication Isometrics | 製作用等角圖 |
| Installation Isometrics | 安裝用等角圖 |

> **專業提醒：** Pipe Sketch 的品質取決於上游資料：Spool 切分是否正確、焊口是否合理、生產檢查是否通過。圖面不對，先查資料，不要先調底圖。

## 21.15 Pipe Fabrication

### 21.15.1 目標與四階段

官方描述 Pipe Fabrication 的目標：直接從 3D 模型產出製造所需的所有資訊；目錄資料提供元件的製造資訊，專案與製程相關屬性在設計階段補上，並支援多種外包情境（例如尖峰負荷）。官方描述的**四階段**：

| 階段 | 內容 | 本章位置 |
|---|---|---|
| 建模（Model） | 定義與製造有關的特徵：製作管端、指派彎管機、設計檢查；另有額外的目錄元件 | 21.15.2 |
| Spooling | 依設計資料切 Spool | 21.12 |
| 檢查（Checks） | 檢查彎管、焊接、擠出 | 21.13 |
| 圖面與輸出 | Spool Drawing、Isometric、NC 資料 | 21.14、21.15.3 |

### 21.15.2 設定與建模

可設定項目（Configuration 選單）：Fabrication Machine Manager、彎管與焊接的最佳化條件、鍍鋅槽容積、焊接間隙、建模一致性檢查、螺紋端、預設值。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Pipe Fabrication 的 Configuration 選單

*圖 21-12　Pipe Fabrication > Configuration 選單。（AVEVA 官方文件截圖，僅供內部教學）*

預設值（Pipe Fabrication > Configuration > Defaults）儲存於應用資料世界 `APPLDW` 元素，需要正確的存取權限。部分欄位如下：

| 預設值 | 意義 |
|---|---|
| Default excess for loose components | 元件設為 loose 時的預設餘量 |
| Default excess for insert／surface／saddle／boss／mitre connection | 各種分支連接的預設餘量 |
| Default Weld Prefix | 以 Weld Handling 視窗建立焊口時自動使用的前綴 |
| Apply default mitre excess to all mitre pieces | 是否對中央管兩端也加餘量；不勾選則只加在到達與離開的管 |
| Negative first feed | 第一個 feed 值是否為負 |
| XYZ Bending Table | 彎管表以 XYZ 座標顯示，還是以 feed／rot／bend 顯示 |

> **注意：** 修改 mitre 餘量或預設 mitre 長度之後，所有受影響的 Spool 必須重新驗證。

**用彎管機決定彎管半徑**需滿足三個條件：

1. 該 Branch、Pipe 或 Zone 的 `BendMacReference` 屬性已設定，並指向有效的 Fabrication Machine World（`FMWL`）、機群（`FMGRP`）或彎管機（`FMBEND`），其彎管尺寸（`FMBDIM`）要與管外徑完全相符。
2. 管等級中，BEND 標題不能已有預設半徑（`RADI`）。
3. Paragon 中必須定義變角度／變半徑的彎管元件（`SCOM`），其 `CompType` 為 `VAR`。

查找順序是 Branch、Pipe、Zone 沿階層往上；找不到符合的尺寸時，半徑要由使用者手動設定。

### 21.15.3 輸出：NC Data

Pipe Fabrication > Export Fabrication Data > Bending Machine NC Data：把彎管資訊存成 XML，與機器無關，後處理成各廠牌 CNC 語言再由 post processor 負責。

| 選項 | 說明 |
|---|---|
| CE | 以目前選取元素為工作元素 |
| File | One File（單一檔）、By Pipe Piece、By Spool、By Pipe（各一檔） |
| Name | Element Name（用 `PPIECE`／`PSPOOL`／`PIPE` 名稱），或 Date & Sequence（例如 `20121107235358-1.xml`） |
| Folder | 輸出資料夾 |
| XYZ Bending Table | 以 XYZ 座標，或 feed／rot／bend 顯示 |
| Save Options | 把選項存檔 |
| Export | 輸出所選管段的 NC 資料 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Bending Machine NC Data 視窗

*圖 21-13　Bending Machine NC Data 視窗。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.15.4 二次開發觀點

這是管路領域最容易整合外部系統的地方，因為**輸出是中立的 XML**：

- 你不需要 PML 就能用 Python、C# 等語言解析 XML，餵給排程、MES 或報價系統。
- XML 的結構〔待核對〕：本章沒有讀取該頁以外的範例，實際欄位請以匯出檔為準。
- 輸出檔名選 Date & Sequence 時，不要用檔名當唯一識別；以 `PPIECE`／`PSPOOL` 名稱或檔案內容識別較穩定。

## 21.16 管支架設計（Pipework Support Design）

### 21.16.1 範圍

官方的 Pipe Hangers and Supports 應用程式，可讓設計者用一組可自訂的標準設計與大量支架元件，詳細建立管支架；標準支架依標準圖出圖，並可產生含參數化尺寸等自訂資料的 Support Schedule。支架可同時包含鋼構與吊架元件：例如門型支架（goalpost）可由三支以上型鋼、接頭、墊塊與 U 型螺栓組成；只有吊架的則可由吊耳、吊桿、花籃螺絲與管夾組成。

官方的前提假設（精簡）：讀者熟悉吊架設計，了解 PARAGON 與 SPECON 的目錄／等級管理、Design 基礎，若要出圖還要熟悉 Draft。

### 21.16.2 資料階層

| 元素 | 角色 | 類比 |
|---|---|---|
| `REST`（Restraint） | 支架的主要管理元素，名稱即支架名；在 Zone 之下建立 | 近似 `PIPE` |
| `HANG`（Hanger） | 由 `REST` 擁有；連接管路與鋼構或土建 | 近似 `BRAN` |
| `FITT` | 鋼構或土建上的接點 | — |
| `ATTA` | 管路上的接點 | — |
| `FRMW`（Framework） | 每個支架總成都有一個；擁有至少一個 `SBFR` | — |
| `SBFR`（Subframework） | 含鋼構資料；吊架若在不同平面，每個平面各建一個 | — |
| `STRUC`／`SUBS` | 擁有 `FRMW` | — |

支架中的任何部分都能經由參照回溯到 `REST`。官方教學使用的示範 MDB 稱為 `/HANGER`，含有 `DEMO/SITE`（起始模型）、`DEMO/H&S`（空白 Zone，放新建支架）與 `HS-Admin`（輔助建構用）三個 Site。

> 〔公開版未收錄：AVEVA 官方產品截圖〕支架資料庫階層圖

*圖 21-14　支架的資料庫階層：REST／HANG／ATTA 與 FRMW／SBFR／SCTN／FITT 的參照關係。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.16.3 設計流程（Goalpost 範例）

| 步驟 | 說明 |
|---|---|
| 1. Position Support Plane | 用 `BOX`（位於 `HS-Admin/Admin/SUPPLANE`）定義支架平面：主方向 PD、橫向 XM 與支架原點；可依被支撐管或柵線（Gridline）定位 |
| 2. 建立 Framework 與分類 | Framework 與 Support Class（僅管路需分類） |
| 3. 建立 Subframework 與樣板構件 | 一個平面一個 Subframework |
| 4. Configure the Support | 從規格選配置類型：Goalpost（兩立柱、多橫樑）、Cantilever（一或二橫樑，可選斜撐）、L-bracket；支架型式可為 Standard 或 Special |
| 5. 修改樣板 | Standard 只能改尺寸，不應加構件；Special 可加構件與修改接頭 |
| 6. 檢查構件連接 | 每個構件有 Start／End，連接型式為 Attached、Anchored、Owner 或 None；兩構件之間為 Joint，有 Owner 與 Attached |
| 7. 套用型鋼斷面 | 選 Support Steel Spec、Profile Type 與 Permissible Profiles，套到全部或指定構件，並檢查端部餘隙 |
| 8. Build the Support | 建立吊架元件，選擇、定向、定位並檢查長度與自由度 |
| 9. Support Schedule | Utilities > Schedules，對目前元素之下所有支架輸出表 |

要點：

- **Invert** 與 **Mirror** 會重設配置並移除已加入樣板的額外構件，所以應在加構件之前先決定方向。
- 餘隙檢查只會把型鋼向外移，建好之前畫面上仍可能看起來與管相交。
- 無鋼構的獨立吊架（如彈簧吊架加吊桿與管夾）使用「標準吊架配置」：設計者選管線與結構上的連接點、從規格選配置，所有元件由吊架規格自動選擇、定尺寸、定向與連接，必要時會詢問設計參數（例如彈簧預設值）。
- 雙平面支架（管往兩個方向走）：每個方向一個 Subframework，常見組合是 Goalpost 加 L-bracket，並把 L-bracket 未接的一端接到 Goalpost 的立柱。
- 斜撐構件的作法：在 Modify Support Template 加入構件，依提示選 Owner，並用 Position 指定起點距離與角度。

> 〔公開版未收錄：AVEVA 官方產品截圖〕支架範例

*圖 21-15　管夾與支柱構成的支架範例。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕雙平面支架配置

*圖 21-16　雙平面支架：Goalpost 加 L-bracket 的平面配置。（AVEVA 官方文件截圖，僅供內部教學）*

### 21.16.4 Support Schedule 與出圖

Support Schedule 的標準欄位包括：Support No.、Hanger No.、Supported Line（被支撐的 Pipe）、Pipe Nom Size、Support Type／Description、Support Drwg No.（來自支架目錄的 UDA `:DRAINFO`）、Support Coords（支架原點）、Parameters（樣板參數尺寸），以及可自訂「相對於 Hanger」運算式的 Additional 欄位。

輸出可選 File、Screen 或兩者，並可設頁長、表頭與表尾。

出圖則使用 Draft 的 Hangers and Supports Automatic Drawing Production 工具：產生完整標註與尺寸的製造圖，包括位置圖、完整材料統計與支架清單；設定可存成一或多個巨集，批次執行。基本圖面版型由使用者定義的 backing sheet 控制。

### 21.16.5 二次開發觀點

| 要取的資料 | 文件依據 | 備註 |
|---|---|---|
| 某 Zone 的所有支架 | `REST` 在 Zone 之下 | 以元素型別走訪〔待核對：PML 語法〕 |
| 每個支架支撐哪些管 | Support Schedule 的 Supported Line 欄 | 官方欄位已定義；對應屬性〔待核對〕 |
| 支架對管的負載 | 官方提到可在設計時輸入工作負載以確定元件尺寸 | 屬性位置〔待核對〕 |
| 批次出圖 | 設定可存成巨集 | 可由外部排程呼叫巨集〔待核對：Marine 12.1 命令列呼叫方式〕 |
| 自訂報表欄位 | Additional 運算式欄位 | 最低風險的擴充方式：不改程式，只改運算式 |

> **專業提醒：** 支架在管路後期才完成，但碰撞與位置問題在早期就該處理。官方提到可在設計過程中隨時進行跨專業的線上干涉檢查，應善用。

## 21.17 常見錯誤彙整

| 錯誤 | 後果 | 對策 |
|---|---|---|
| 在非 Branch 層級建元件 | 系統報錯 | 先導覽到 Branch |
| 以為 Pspec 改變會自動換既有元件 | 材料表與模型不一致 | 用 Modify Pipework 或 Pipe Modification |
| 同一 Branch 內混用不同等級 | 等級邊界不清 | 在換等級處另建 Branch |
| 設備移動後沒有 Reconnect | 管沒有跟著設備 | 對被移動的設備執行 Reconnect |
| 改了 mitre 設定沒重新驗證 Spool | 管段長度不含新餘量 | 修改後重新驗證受影響 Spool |
| Spooling 前未做一致性檢查 | SPOOLER 無法正常運作 | 先跑 Data Consistency 並修正錯誤 |
| 同時開啟 Production Checks 與 Pipe Fabrication | 功能互斥 | 以 `PRODUCTIONCHECKSENABLED` 擇一 |
| 自己動手開船體孔 | 責任與稽核混亂 | 走 Hole Management |

## 21.18 本章小結

- 管路資料是 `PIPE → BRAN → 元件` 三層，直管是系統隱含產生的 `TUBI`。
- Pspec 可設在 Pipe 或 Branch 並向下傳遞；換等級要另建 Branch。
- 設計流程：建立 Pipe/Branch、定位並連接 Head/Tail、放元件、路由（Quick Pipe Routing 或 Pipe Router）、檢查、修改與拆分。
- 穿孔由 Hole Management 管控：請求、核准、產生 `PFIT`。
- Spooling 依 Shop Flag 切 SPOOL 與 FIELD；Pipe Piece 與 Pipe Spool 由系統推導，不能手動建立。
- Production Checks 與 Pipe Fabrication 互斥；Pipe Fabrication 的 NC 輸出是中立 XML，最適合與外部系統整合。
- 管支架用 `REST`／`HANG` 管連接，用 `FRMW`／`SBFR` 管鋼構；Support Schedule 與 Draft 批次出圖是主要輸出。
- 對二次開發者：官方文件只給操作，不給 PML；所有屬性與指令請在實機驗證。

## 21.19 練習題與自我檢核

### 練習（只能在訓練專案）

1. **階層圖。** 用自己的話畫出 `WORLD→SITE→ZONE→PIPE→BRAN→元件`，標出哪些層級是通用、哪些是管路專屬。
2. **建立與連接。** 在訓練專案建一個 Pipe，定義 Head 與 Tail，並區分「已定位」與「已連接」，記下 Connectivity 窗格的差異。
3. **虛線診斷。** 故意讓兩元件方向不匹配，觀察虛線，再以 Quick Pipe Routing 修好。
4. **Pspec 實驗。** 在 Pipe 層級改等級，觀察既有元件與新建元件的差異。
5. **Split 與 Merge。** 把一個 Branch 拆成兩個，再合併回去；嘗試合併不共線區段並記下錯誤訊息。
6. **Spool 觀察。** 在已設定 Shop／Field 的管上執行 Spooling，說明 Spool Break 發生的位置。
7. **屬性清單。**（開發者）用 Design Explorer 檢視 `BRAN` 與元件的屬性，列出你認為可用於「未連接檢查」的屬性，並標註〔待核對〕直到實測完成。
8. **XML 解析。**（開發者）匯出一份 Bending Machine NC Data，用任何語言寫一段解析並統計管段數量。
9. **支架。** 依官方範例建立單一吊架與門型支架，輸出 Support Schedule。

### 自我檢核

- [ ] 我能畫出管路資料階層並說明每層責任。
- [ ] 我能說明 Pspec 的向下傳遞與等級邊界作法。
- [ ] 我能區分 Head／Tail 的「定位」與「連接」。
- [ ] 我知道 `TUBI` 是隱含產生，不是我建立的。
- [ ] 我能說明 Quick Pipe Routing 與 Pipe Router 的適用情境。
- [ ] 我能說明穿孔的請求、核准與 `PFIT` 的產生。
- [ ] 我能說明 SPOOL、FIELD、Spool Break 與 Shop Flag。
- [ ] 我知道 Pipe Piece／Pipe Spool 不能手動建立或刪除。
- [ ] 我能說明 Production Checks 與 Pipe Fabrication 為什麼不能同時啟用。
- [ ] 我能說明 `REST`／`HANG`／`FRMW`／`SBFR` 的關係。
- [ ] 我能針對每個階段說出可取用的資料，並指出哪些仍待核對。

## 資料來源

- AVEVA Marine 12.1 官方離線文件：*Pipework*（Hierarchy、Default Pipe Specification、Pipe Element、Branch Element、Pipework Components、Quick Pipe Routing、Pipe Router、Pipe Penetration、Modify Pipework、Pipe Splitting、Pipework Spooling、Production Checks、Pipe Sketches、Isometrics Preview、Pipe Fabrication）。
- AVEVA Marine 12.1 官方離線文件：*Pipework Support Design*（Pipe Hangers and Supports、Hangers and Supports Database Hierarchy、Create Goalpost Support、Create a Single Hanger、Create a Two-plane Support、Create Bracing Members、Automatic Drawing Production）。
- 本課程延伸：[第 7 章 舾裝設計](ch07_outfitting_zh-TW.reading.html)、[第 12 章 PML 資料庫操作](ch12_pml_database_zh-TW.reading.html)、[第 20 章 系統管理與維運](ch20_system_administration_zh-TW.reading.html)。

> **授權與界線：** 本章文字與表格為本課程依官方文件自行整理；章中少量操作畫面與示意圖截自官方文件，僅供內部教學參考，不重製長段原文。官方文件原屬 PDMS 時代手冊，Marine 12.1 實際選單與行為請以你們安裝的版本為準；所有標〔待核對〕的項目都需要實機驗證後才可用於正式工具。
