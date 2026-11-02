# 第 22 章　結構設計（Structures）：Frame、型鋼、板、接頭與平台樓梯

> 船體與舾裝模型裡，總有一類東西既不是管路也不是設備：支撐管路的鋼架、設備基座、走道平台、樓梯、爬梯與欄杆。AVEVA Marine 把這類資料統一放在 **Structures（結構設計）** 之下，用同一套「元素階層＋目錄（Catalogue）引用」的概念來建模。理解它，等於理解了 AVEVA 設計資料庫的縮影：**位置與方向存在 Design 資料庫，形狀與材料存在 Catalogue 資料庫，兩者用一個參考（SpecRef）連起來。**
>
> 這一章的讀者有兩種：**結構設計者**要知道每個功能在做什麼、順序怎麼排、常見坑在哪；**二次開發者**要知道資料長在哪些元素、哪些屬性值得讀，才能寫出可靠的報表與檢查工具。
>
> **資料可信度：** 本章內容取自 AVEVA Marine 12.1 官方離線文件的 **Structures** 章節，涵蓋其下四個子樹：Structural Design（含 Beams and Columns、Panels and Plates、Walls and Floors、Structural Catalog Guide、SteelWork Utilities、Bent Panels）、Access Platforms, Stairs and Ladders（使用者指南）、Access Platforms, Stairs and Ladders Administrator（管理者指南）與 ASL Modeller。本章用自己的話重組為教學順序，並非逐字翻譯。文件中的屬性名稱（如 POSS、POSE、JFRE、CREF）與元素型別（如 STRU、FRMW、SBFR、SCTN、SNOD、SJOI、PANE、PLOO、PAVE、PFIT）引用自文件；**官方這幾頁以 GUI 操作為主，幾乎沒有給出 PML 指令語法**，因此凡涉及「用 PML 怎麼查、怎麼改」之處，本章只列出文件提到的屬性名稱，具體語法一律標〔待核對〕，請在實際專案環境用 `q attributes`（或第 4～6 章教過的查詢方式）驗證。選單路徑（例如 Create > Sections > Straight）以 12.1 文件為準，實際安裝若有客製化，畫面可能不同。另外，文件部分段落仍保留舊產品名稱 PDMS，意思等同於現在的設計模組，本章統一以「設計模組」稱之。

## 22.1 學習目標

讀完本章，你應該能夠：

1. 說明 Structures 的四個應用程式（Beams and Columns、Panels and Plates、Walls and Floors、Access, Stairs and Ladders）各自負責什麼。
2. 畫出結構資料階層：WORLD > SITE > ZONE > STRU > FRMW > SBFR > SCTN，並說明為什麼建立元素必須由上而下。
3. 解釋「Design 與 Catalogue 的交叉參考」：SpecRef、Profile（SPRF）、P-line 與 PKEY 分別是什麼。
4. 完成「初始設定」：Storage Areas、預設型鋼規格（Default Profile Specification）、Justification／Member Line／Joint Line。
5. 建立柱、梁、斜撐，並用 Split、Splice、Merge、Fillet、Miter 修整構件。
6. 說明 SNOD／SJOI 如何表示連接，以及 JFRE（Dominant／Subordinate）如何決定移動時的連動行為。
7. 區分 Explicit（AT）、Relative（BY）、Ship Reference、Extend、Drag 等定位方式，並正確處理方向（Beta Angle、Flip、Rotate）。
8. 建立板（PANE／PLOO／PAVE）、牆、地板、板配件（PFIT）與彎板（BPANEL）。
9. 說明 ASL 組立（STRTWR、STRFLT、LADDER、PLTFRM、HANDRA）的資料階層，以及管理者與使用者的分工。
10. 規劃結構的檢查與報表（材料清單、質量特性、干涉、圖面），並知道二次開發能抓哪些資料。

## 22.2 全貌：四個應用程式與資料怎麼分工

### 22.2.1 四個應用程式

從主選單選 **Design > Structures**，會看到四個應用程式。它們操作同一個設計資料庫，只是工具列與表單不同：

| 應用程式 | 負責的東西 | 典型元素 |
|---|---|---|
| Beams and Columns | 直線型鋼構件：柱、梁、斜撐；節點與接頭；構件配件 | SCTN、GENSEC、SNOD、SJOI、FITT |
| Panels and Plates | 任意方位的平面板：地板鋼板、牆板、屋頂板；板配件、開孔 | PANE、PLOO、PAVE、PFIT、BPANEL |
| Walls and Floors | 牆、地板、整平層（Screed）；牆／地板配件 | WALL、FLOOR、SCREED、CFLOOR |
| Access, Stairs and Ladders（ASL） | 平台、樓梯、爬梯、欄杆等整組立 | STRTWR、STRFLT、LADDER、PLTFRM、HANDRA |

文件另外提到，使用時搭配 **SteelWork Utilities** 工具列（結構複製／鏡射、修剪、接合、刪除端切等），可以大量減少重複操作。

### 22.2.2 Design 與 Catalogue：誰存什麼

結構設計最重要的觀念只有一句話：

```
   Design 資料庫                         Catalogue 資料庫
   (這個構件放在哪裡、朝哪裡)             (這種構件長什麼樣、什麼材料)
 ┌────────────────────────┐          ┌──────────────────────────┐
 │ SCTN  /COL-101          │          │ SPRF  H 400x200x8x13      │
 │   POSS / POSE (起訖點)  │  SpecRef │   Geometry Set (2D 輪廓)  │
 │   Beta Angle (轉角)     │ ───────► │   Point Set (P-point/P-line)│
 │   Justification (對齊線)│          │   材料、參數化尺寸         │
 └────────────────────────┘          └──────────────────────────┘
```

| 資料 | 存在哪裡 | 內容 |
|---|---|---|
| 位置、方向、連接關係 | Design 資料庫 | 起點 POSS、終點 POSE、Beta Angle、Justification、連接的節點與接頭 |
| 斷面形狀、尺寸、材料、接頭／配件形狀 | Catalogue 資料庫 | Geometry Set（幾何）與 Point Set（參考點／參考線） |
| 兩者的連結 | Design 元素上的 Specification Reference（SpecRef） | 指向 Catalogue 內的某個項目 |

這也解釋了一個常見現象：只改 Catalogue 裡的斷面定義，模型中所有引用它的構件都會跟著變；反過來，Design 元素本身不存斷面尺寸。

> **專業提醒：** 板（Panel）、牆與地板是例外。文件說明它們**沒有 Catalogue 項目**，所以它們的 Specification Reference 不帶 Catalogue Reference；規格只是提供一組可選厚度（或單一厚度），建立時厚度還可以被覆寫，甚至規格可以留空（Unset）再手動輸入厚度。因此「板的厚度」是存在 Design 元素本身（Panel Loop 的 HEIG），不能像型鋼一樣追溯到 Catalogue。

### 22.2.3 結構資料階層

所有元素都被其他元素擁有，所以**必須依序由上往下建立**。Structures 專屬的階層長這樣：

```
WORLD (/*)
 └─ SITE
     └─ ZONE
         └─ STRU        結構（Structure）
             ├─ FRMW    框架（Framework）
             │   └─ SBFR  子框架（Subframework）
             │       ├─ SCTN   直線型鋼構件（Section）
             │       │   ├─ SNOD   次要節點（Secondary Node）
             │       │   │   └─ SJOI  次要接頭（Secondary Joint）
             │       │   └─ FITT   構件配件（Fitting）
             │       └─ GENSEC 通用型鋼（Generic Section）
             ├─ PANE 等板類元素（PLOO > PAVE）
             └─ ASL 組立：STRTWR / STRFLT / LADDER / PLTFRM / HANDRA
```

> 上圖是依文件文字說明整理的示意：文件指出「Zone 之下的結構專屬元素為 Structure、Framework、Subframework、SCTN」，以及 SJOI 由 SNOD 擁有、ASL 組立元素由 STRU 擁有。個別元素是否能直接掛在 STRU 或 FRMW 下，請以實際專案的資料庫階層為準〔待核對〕。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Design Explorer 中的結構階層：SITE、ZONE、STRU、FRMW、SBFR 與 SCTN／PANE
*圖 22-1　Design Explorer 中實際的結構階層（SITE > ZONE > STRU > FRMW > SBFR > SCTN／PANE）。（AVEVA 官方文件截圖，僅供內部教學）*

| 元素 | 中文 | 用途 |
|---|---|---|
| STRU | 結構 | 一個完整結構物的容器（例如一座設備鋼架） |
| FRMW | 框架 | 把相關構件分群，便於複製、移動、報表 |
| SBFR | 子框架 | 框架內再細分的群組 |
| SCTN | 型鋼構件 | 每根直線柱、梁、斜撐；形狀來自 Profile（SPRF），位置由 POSS／POSE 決定 |
| SNOD | 節點 | 表示構件上的邏輯連接點；Secondary Node 沿著擁有它的構件定位，構件移動時一起移動 |
| SJOI | 次要接頭 | 兩個構件連接時產生；要有 Catalogue 規格才會有幾何 |
| FITT | 構件配件 | 腹板加勁板、吊耳、防火包覆等 |

節點有兩種：**Primary Node** 的位置獨立指定；**Secondary Node** 沿所屬構件、距起點一段距離，會隨構件移動。節點的兩個用途是：標示相鄰構件的邏輯連接點，以及定義應力如何作用在結構各點（也就是把資料交給外部應力分析程式）。

### 22.2.4 專業提醒：用 Design Explorer 檢視，不要憑感覺

新手常見的問題是「畫面上看得到，但不知道它是什麼元素」。建議養成習慣：建立任何東西之後，立刻在 Design Explorer 確認它掛在哪個 STRU／FRMW／SBFR 之下、型別是什麼、有沒有自動多出 SNOD／SJOI／PLOO／PAVE。

## 22.3 初始設定：先決定規格與儲存位置

建構結構之前，文件要求先做兩件事：**選定預設型鋼規格**與**設定儲存區域（Storage Areas）**。這一步省略的話，後面每建一根構件都要重選，更糟的是構件可能放錯階層。

### 22.3.1 Storage Areas

步驟：

1. 把目前元素（CE）設在要放結構的 SBFR（或對應層級）。
2. 選 **Settings > Storage Areas**。
3. 在視窗中分別指定 **Primary Node** 與 **Sections** 的儲存區域。預設兩者都是 Unset。
4. 設定完畢，新設定會顯示在視窗與主工具列。

| 項目 | 說明 |
|---|---|
| Sections 儲存區域 | 新建的 SCTN 會放進這個元素之下 |
| Primary Node 儲存區域 | 需要建立 Primary Node 時放的地方 |
| 失誤後果 | 構件掛到錯誤的 FRMW／SBFR，後續複製、報表、權限（誰可寫入）都會跟著出問題 |

### 22.3.2 自動型鋼分配與 Primary Node

預設行為是：每建一個新 Section，系統自動關聯一個 Catalogue Profile；在未連接的構件端點**預設不自動建立 Primary Node**。若需要在既有構件端點補一個，用 **Create > PNode at SCTN End**，點選端點後按 Esc 即可。

### 22.3.3 預設型鋼規格（Default Profile Specification）

主工具列的 **Set Default Profile Specification** 會開啟 Section Specification (Default) 視窗，主要分兩區：

| 區域 | 內容 |
|---|---|
| Specification Data | 選擇 Catalogue 內的規格（例如某一標準、某 Generic Type），再選具體尺寸 |
| Pline Settings | **Justification**（對齊線）、**Member Line**（在出圖軟體中顯示的線，例如中心線）、**Joint Line**（接頭幾何使用的 P-line，通常為 NA） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Section Specification 視窗：規格資料與 Pline Settings
*圖 22-2　Section Specification 視窗：上方選規格與尺寸，中段設定 Justification、Member line、Joint line。（AVEVA 官方文件截圖，僅供內部教學）*

三條線各自控制什麼，是初學者最容易混淆的地方：

| 設定 | 影響 | 常見值 |
|---|---|---|
| Justification | 構件的起訖點放在斷面上的哪條 P-line，也就是模型位置的基準 | 例如 TOS、TOAX（文件範例）等 |
| Member Line | 出圖時顯示的線 | 例如中心線 |
| Joint Line | 接頭幾何參考的 P-line | 通常 NA |

> **專業提醒：** Justification 一旦決定，後續所有尺寸（柱的長度、梁頂標高）都是相對那條 P-line 而言。同一個專案請先與團隊約定好預設值，不要每人各設一套，否則同一座鋼架的梁頂標高會隔著人差一個斷面高度。

## 22.4 型鋼斷面、P-line 與 Catalogue

### 22.4.1 Catalogue 項目由什麼組成

每個 Catalogue 項目（斷面、接頭、配件）都由兩組資料定義：

| 資料集 | 內容 | 範例 |
|---|---|---|
| Geometry Set（幾何集） | 用 2D 或 3D 基本形（primitives）描述外形。斷面只有 2D 基本形，在模型裡被拉伸成 3D；接頭與配件由 3D 基本形組成，可含負體積（代表孔洞） | H 型鋼的 2D 輪廓 |
| Point Set（點集） | 疊在幾何上的參考點與方向：**P-point**（1D 點加方向）與 **P-line**（2D 線加方向） | 腹板左下角、鋼頂 |

多個尺寸不同、外形相似的 Catalogue 項目，可以共用同一個 Geometry Set，靠參數化尺寸產生各自的大小。這也是為什麼一個配件類型可以套用到該斷面類別的所有尺寸。

### 22.4.2 P-line 與 PKEY

每條 P-line 用 2～4 個字母的代碼（PKEY）識別，表示它在 2D 斷面上的相對位置，拉伸後就成為沿構件長度方向的一條線。部分常見代碼（取自文件列出的部分清單，實際每種斷面只用其中一部分）：

| PKEY | 意義 |
|---|---|
| BOS | Bottom of steel（鋼底） |
| BOC | Bottom of channel |
| BLW / BRW | 腹板左下／右下 |
| BBH / BBHL / BBHR | 底部螺栓孔（及左／右） |
| TOS | 鋼頂（文件範例中作為預設旋轉中心與 Justification） |
| TOAX | 文件範例中的 Justification Line，用於說明 Beta Angle 繞線旋轉 |
| NA | 中性軸（Neutral Axis） |

文件的 Structural Catalog Guide 另外圖示了常見 Generic Type：**BOX、ANG、TUBE、BEAM**，各自標出 P-line 與參數化尺寸。完整 PKEY 與接頭、配件清單請查 Structural Catalog Guide 與 *Catalogue and Specifications Reference Manual*。

> 〔公開版未收錄：AVEVA 官方產品截圖〕BOX 型斷面的 P-line 與參數化尺寸
*圖 22-3　Generic Type BOX 的 P-line（TOS、BOS、NA 等）與參數標註。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.4.3 對應到二次開發

| 想要的資料 | 文件依據 | 說明 |
|---|---|---|
| 構件用的斷面（Profile） | SCTN 的斷面由 Catalogue Profile（SPRF）元素決定 | 屬性名稱 SPRF 為文件所述；讀取語法〔待核對〕 |
| 起點／終點 | POSS、POSE | 文件明確指出這兩個屬性決定長度與方向；單位與座標系基準（WRT）〔待核對〕 |
| 材料 | 文件說明 Modify > Material 可更換材料 | 材料在 Design 元素與 Catalogue 間如何儲存、對應哪個屬性〔待核對〕 |
| 斷面參數（高、寬、厚） | Catalogue 參數化尺寸 | 如何從 SCTN 取得實際參數值〔待核對〕 |

> **專業提醒：** 寫材料清單工具時，不要自己拿起訖點兩端相減當長度而不處理 Justification、端切（Miter、Trim）；先確認你要的是「理論長度」還是「下料長度」，兩者可能因端部處理而不同〔待核對：官方文件未給出長度的專用屬性，請在專案內以實際屬性驗證〕。

## 22.5 建立構件：柱、梁與斜撐

### 22.5.1 建議的建構順序

文件示範的流程是：先用**明確座標**建立立柱，再用**點選**連接建立橫梁，最後加斜撐。流程如下：

```
 設定 Storage Areas ─► 設定預設型鋼規格
        │
        ▼
 建立柱 (Explicit：輸入座標或點 3D 視圖)
        │
        ▼
 建立梁 (Pick：直接點選柱，Secondary Nodes 勾選，自動連接)
        │
        ▼
 修整 (Trim to Pline / Split / Splice / Miter)
        │
        ▼
 加斜撐與穩定構件 (Continuous 字串、Intersect 點選)
        │
        ▼
 補接頭 (SJOI 指定 Catalogue 規格) 與配件 (FITT)
```

### 22.5.2 直線構件的建立

選單：**Create > Sections > Straight**，會顯示 Section 視窗與 Positioning Control 工具列。幾個關鍵選項：

| 選項 | 意義 |
|---|---|
| String Method：Single | 每根構件各自指定起訖點 |
| String Method：Continuous | 鏈狀建立，下一根的起點自動接在上一根的終點（用 Redefine Start 可覆寫）；建三根連續的梁就適合 |
| Secondary Nodes 勾選 | 建立時自動產生節點與接頭，連接關係同時建立 |
| Confirm 勾選 | 每根新構件加入資料庫前先讓你確認位置 |
| Define Start/End Explicitly | 直接輸入座標或在 3D 視圖點選 |
| Pick Type: Element / Pick Method: Intersect | 以點選既有構件交點決定端點；**第一個點選的構件被視為被連接的擁有者**，所以斜撐要先點柱再點梁，否則間隙修剪不會動作 |

### 22.5.3 快速建立規則排列（Regular Structure）

若模型有大量規則陣列的柱梁，用 **Create > Sections > Specials**，從 Section Creation 視窗選 **Regular Structure**。這個功能一次建出整套完整連接的結構，文件建議：即使不完全規則，先用它建出主體再修改，通常比逐根建立快。使用前確認自動 Profile 分配為 On、Primary Node 建立為 Off。

### 22.5.4 斜撐與鏡射

文件示範：把預設規格改成矩形空心斷面，並把 Justification、Member Line、Joint Line 都設為 NA；斜撐間隙（Bracing gap）可用快捷功能調整；另外三支斜撐用 **Mirror Copy**（以指定平面的軸為準反射複製）完成。另有 **Add Standard Bracing Configurations** 預設配置可直接套用〔具體選項請查官方該頁〕。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Brace Gaps 視窗與斜撐間隙定義方式
*圖 22-4　Brace Gaps 視窗：指定斜撐間隙的方式與預設間隙。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.5.5 複製、鏡射與 SteelWork Utilities

複製結構的重點是：**複製的是容納構件的清單（list），而不是整個 Sub-Frame 本身**。SteelWork Utilities 工具列提供的功能如下：

| 功能 | 說明 |
|---|---|
| Structure Copy/Mirror | 結構複製與鏡射 |
| Mirror Structure with Fittings | 鏡射並帶配件 |
| Trim Selected Sections／with Offset | 修剪選取構件（可帶偏移） |
| Trim and Connect Selected Sections | 修剪並連接 |
| Connect Adjacent Sections | 連接相鄰構件 |
| Delete Joint／Delete End-cut | 刪除接頭／端切 |
| Miter Selected Sections | 對選取構件做斜接 |
| Copy Selected to Another Structure | 複製到另一結構 |
| Include Structure | 納入結構（具體語意請查該頁）〔待核對〕 |
| Delete Section | 刪除構件 |
| Modify Specification of Selection with Picked | 用被點選構件的規格批次修改選取者 |
| Model Dimensions | 模型尺寸標註 |
| Trace Panel with Sections／Trace Section with Panel | 板與型鋼互相描摹輪廓 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Structure Copy / Mirror 視窗
*圖 22-5　SteelWork Utilities 的 Structure Copy / Mirror 視窗：設定鏡射平面原點與方向。（AVEVA 官方文件截圖，僅供內部教學）*

## 22.6 修改構件：規格、位置、方向與材料

### 22.6.1 修改規格與定義

| 操作 | 選單 | 說明 |
|---|---|---|
| 修改規格 | Modify > Section > Specification | 變更 Section 的規格（Profile 等） |
| 修改定義 | Modify > Section > Definition | 變更起點、終點或中心位置；選 Start 只動起點、選 Centre 整根平移等 |
| 修改材料 | Modify > Material | 可選 CE、清單或點選的元素；勾 **Cascade Material to all offspring** 則連配件一併改材料 |

### 22.6.2 位置：Position 選單

文件把位置分成兩大類，加上若干輔助：

| 方式 | 選單 | 行為 |
|---|---|---|
| Explicitly（AT） | Position > Explicitly (AT) | 直接指定座標。Datum 可選 Start（移起點，終點不動）、End、Centre（整根平移）、Designate Position |
| Relatively（BY） | Position > Relatively (BY) | 從目前位置沿一軸或多軸移動一段距離；預設軸向相對於世界座標，也可改用其他設計元素 |
| Using Ship Reference | Position > Using Ship Reference | 結構依格線建立時，可用 Frame、Lg (Horz)、Lg (Vert)、Offset 在網格中移動；**元素必須有 POS 屬性**，否則顯示錯誤 |
| Extend > Through | Position > Extend > Through | 把構件任一端延伸或修剪到一個平面；只沿 Z 軸（拉伸方向）動。End of Section 可選 Nearest end、Start、End、Pick |
| Extend > By | Position > Extend > By | 依距離或比例加長／縮短；正值加長，負值縮短；可勾 Maintain Sections' Node Positions 保持節點位置 |
| Drag Explicitly | Position > Drag Explicitly | 等於三個動作合一：Position > Explicitly (AT)、Connect > Trim to Pline > all attached、Position > Align Secondary Nodes |
| Align Secondary Nodes | Position > Align Secondary Nodes | 構件被移動或延伸後修正節點對齊；可從 SCTN、STRU、ZONE、SITE 層級執行 |

> **專業提醒：** 如果你只用 Explicitly (AT) 搬動構件，相接的構件端點與節點不會自動跟著動。需要連動時用 Drag Explicitly，或搭配 Joint Dominant（見 22.7.3）。

### 22.6.3 方向：Orientate 選單

| 功能 | 說明 |
|---|---|
| Axes | 重新指定 XEast／YNorth／ZUp 對應；**僅適用具有直接 Orientation 屬性的元素**，SCTN、SBFR、FRMW 會跳出警告，所以結構設計中很少用 |
| Rotate | 預設旋轉軸 ZU，位置在起點（例：Justification Pline TOS）；輸入角度後 Apply；負角度可還原 |
| Beta Angle | SCTN 繞自身 ZU 軸的轉角；可用選單以 90 度為單位正負增減（文件範例中 Justification Line 為 TOAX） |
| Flip | 對調起點與終點，也就是 ZU 方向轉 180 度；僅非對稱斷面（角鋼、槽鋼）有可見影響 |

對 SCTN 而言，最常用的方向工具是 **Beta Angle** 與 **Flip**；如果在 SCTN 上用 Axes 失敗，是預期行為。

### 22.6.4 專業提醒：改 Justification 前先想清楚

文件另有 **Modify Wall Justification**、**Modify Floor/Screed Justification** 等頁面，說明牆與地板也有 Justification 概念。對型鋼與板一樣，修改 Justification 會在不改變模型原始位置參數的前提下，改變「元素實際落在 P-line 的哪一側」，若沒有同時調整位置，就會看到構件整體偏移一個斷面尺寸。

## 22.7 連接、接頭與端部處理

### 22.7.1 連接的資料結構

兩個 SCTN 的連接由 **Secondary Joint（SJOI）** 完成，結構如下：

| 元素／屬性 | 說明 |
|---|---|
| Owning Section | 被連接的構件（例如柱） |
| Attached Section | 連上來的構件（例如梁） |
| SNOD | 位於 Owning Section 的 Justification Line 上，在兩構件交點處 |
| SJOI | 由 SNOD 擁有 |
| **CREF**（Connection Reference） | SJOI 的屬性，指向 Attached Section 的名稱 |
| **JOISTART／JOIEND** | Attached Section 的屬性，指向它起點與終點所用的 SJOI 名稱，形成「環狀」互相參照 |

```
   Owning SCTN (柱)                       Attached SCTN (梁)
   └─ SNOD                                  JOISTART ─┐
       └─ SJOI ── CREF ───────────────────────────►  │ (指回梁)
              ▲                                       │
              └─────────── JOISTART／JOIEND 指向 ◄────┘
```

建立 Section 時若勾選 Secondary Nodes，連接會自動產生；也可用 **Connect > Connect** 明確連接：先點被連接的構件，再點要連接的構件端點，Esc 結束。

### 22.7.2 接頭的幾何：需要 Catalogue 規格

自動建立的 SJOI 一開始**沒有幾何**，3D 視圖看不到。要呈現出來，必須讓接頭引用一個 Catalogue 規格，做法與構件引用 Profile 完全一樣。接頭的重要屬性（文件提到者）：

| 屬性／功能 | 用途 |
|---|---|
| **POSL** | 接頭原點平面相對 Owning Section 的設定方式（文件圖示說明） |
| 位置與方向 | 接頭相對於 SNOD 定位與轉向 |
| Connect a Joint to the Start of an Attached Section | 讓接頭與附屬構件端點對應 |
| Compound Joint | **Create > Compound Joint**：行政性質的容器，把多個接頭歸成一組（先 Pick 要合併的構件端點，Esc，再確認） |
| Tidy Joints | **Delete > Tidy Joints**：附屬構件被刪除後，SJOI 的 CREF 變成 Nulref 但元素未刪；用這個功能可從 SITE 到 SCTN 任一層找出並刪除，且可選擇空 SNOD 一併刪除 |

> **專業提醒：** 如果從 Command line 直接刪了梁而不是用 GUI，SJOI 會殘留。這類殘留元素在報表中可能被誤算為「有接頭」，檢查工具應該找 CREF 為 Nulref 的 SJOI。

### 22.7.3 Dominant 與 Subordinate 接頭

接頭有「誰跟著誰動」的問題，由接頭的 **JFRE（Joint Freedom）** 屬性控制：

| JFRE | 稱呼 | 擁有者被移動時，附屬構件的行為 |
|---|---|---|
| False（新接頭預設） | Subordinate（也可說構件為 dominant） | 附屬構件不自動調整 |
| True | Dominant | 附屬構件的端點會跟著重新對齊，保持斜撐間隙等關係 |

可在 **Settings > Tolerances**（Section Tolerances 視窗）改預設，也可事後用 **Connect > Joint Subordinate／Joint Dominant** 對選取的構件端點切換。文件的實作範例是：移動一組柱以加長鋼架時，若兩端的斜撐接頭都設為 Dominant，斜撐會自動重新對齊並保持規定的間隙。標準做法是：**斜撐兩端的接頭都設為 Dominant**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Dominant 與 Subordinate 接頭的比較
*圖 22-6　移動擁有者構件後，JFRE = False（Subordinate）與 JFRE = True（Dominant）的差異。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.7.4 端部處理與修整工具

| 操作 | 說明 |
|---|---|
| Trim to Pline | 把附屬構件修剪到擁有者的指定 P-line（或強制指定 P-line 或被點選的構件）。若 Pline Rule 沒設好，構件長度可能不對；文件強調這類錯誤要先修正，否則連接斜撐時會出問題 |
| **Split** | 把一根構件切成多根（例如梁穿過第三根梁時）。適用 Section、Generic Section、Panel；先整體建模再切成可製造或可組裝的單元 |
| **Splice** | Modify > Sections > Splice：用平面把構件切開，可選擇端對端接合；Primary Node 切換需為 Off，否則會建 Primary Node 而非 Secondary Node；可對 CE、List 或 Pick 的元素同時操作 |
| **Merge** | 合併相同型別（SCTN、PANE、GENSEC）且共線（板則共面）的元素；**第一個選取的為主導元素，其屬性被其他元素繼承** |
| **Fillet** | 把兩根不平行但共面的構件合併成單一 GENSEC，不管規格、Justification 或 Beta Angle；STNC 與 GENSEC 不能互相 Fillet；因為 GENSEC 不能有配件，被 Fillet 的構件上的配件會被刪除 |
| **Miter** | 在條件成立時，把構件或 GENSEC 斜接到另一構件或板 |
| Delete End-cut | 刪除端切 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Splice Section on Plane 視窗
*圖 22-7　Splice Section on Plane 視窗：以平面切開構件。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.7.5 構件配件（Fittings）

Section 配件是 Catalogue 項目，在 Design 中以 **FITT** 元素表示，由 SCTN 擁有；每個配件設計為關聯到特定斷面類別的一或多條 P-line。因為參數化，一種配件通常可用於該類別的所有尺寸。配件沿構件的拉伸方向（Z 方向）相對於起點定位。

建立方式：CE 設為 SCTN，選 **Create > Fitting > Single**，在 Create Fitting 視窗選規格（例如腹板加勁板、吊耳、防火包覆）、子類型與清單項目；Section Type 欄顯示擁有者的 Generic Type（GTYPE）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Fitting 視窗
*圖 22-8　Create Fitting 視窗：選規格、Section Type、Sub-Type 與 Justification。（AVEVA 官方文件截圖，僅供內部教學）*

另有 **Create Fixing**：獨立 Fixing 元素可建在 FRMW 之下，僅限 Panels & Plates 或 Walls & Floors 應用程式；其 TABGRO 必須在 Paragon（Catalogue 建立工具）中建立，且 PURP 與 SPTYPE 設為 STFX（Standalone Fixing），才會出現在 Fixings 視窗。這說明：**要讓設計者有東西可選，管理者要先在 Catalogue 端備料**。

### 22.7.6 二次開發怎麼用

| 目的 | 可用的資料 | 說明 |
|---|---|---|
| 找出未連接或孤立的構件 | JOISTART／JOIEND 是否指向有效 SJOI | 屬性名稱取自文件；空值判斷語法〔待核對〕 |
| 找出殘留接頭 | SJOI 的 CREF 為 Nulref | 文件原文稱此狀況為 redundant |
| 檢查斜撐接頭是否 Dominant | SJOI 的 JFRE | 文件定義 True 為 Dominant |
| 區分 Primary／Secondary 節點 | SNOD 與 PNOD（Primary Node） | 元素型別 PNOD 在本章依 Primary Node 推論，未見文件直接列出〔待核對〕 |
| 批次修改 Dominant／Subordinate | GUI 有選單；PML 指令〔待核對〕 | 請先在小範圍測試並做 Undo／備份 |

## 22.8 板（Panels）、牆與地板

### 22.8.1 板如何表示

**Panel（PANE）** 可代表任何覆蓋結構的片狀材料，不論是水平地板鋼板、垂直牆板或傾斜屋頂板。原理與 Section 類似（斷面拉伸），但板是把使用者定義的 2D 形狀拉伸：

| 元素 | 說明 |
|---|---|
| PANE | 板本身 |
| **PLOO**（Panel Loop） | 板的平面範圍，由一圈相連的頂點組成；**HEIG 屬性 = 拉伸距離 = 板厚** |
| **PAVE**（Panel Vertex） | 板頂點，在板的 2D 座標系有特定位置；每個頂點可有圓角半徑（正值朝頂點外凸方向的圓弧，負值相反；預設 0 代表尖角） |

```
 PANE
  └─ PLOO  (HEIG = 厚度)
      ├─ PAVE 1  (半徑 0)
      ├─ PAVE 2
      ├─ PAVE 3
      └─ PAVE 4
```

> 〔公開版未收錄：AVEVA 官方產品截圖〕板（PANE）、板輪廓（PLOO）與板頂點（PAVE）
*圖 22-9　板的表示方式：PANE、PLOO（HEIG 為板厚）與 PAVE。（AVEVA 官方文件截圖，僅供內部教學）*

文件特別提醒：板的 Justification 結果可能跟建立時頂點是**順時針或逆時針**有關。所以在 Justification 與厚度方向看起來反了時，先檢查頂點建立方向。

### 22.8.2 板的規格與建立

| 步驟 | 說明 |
|---|---|
| 1. 設預設規格 | Panels and Plates 工具列的 Set Panel Default Specification（Plate Specification (Default) 視窗）；可選規格與預設厚度，或 Unset |
| 2. 建立 | **Create > Panel**，在 Create Panel 視窗選 Justification（例如 Bottom，使板底貼在支撐構件頂面）、Thickness（若有規格會顯示預設，輸入新值會跳出是否覆寫為 Unset 的訊息）、Representation（Levels 與 Obstruction 影響 3D 顯示與干涉檢查的處理） |
| 3. 切分 | 文件示範先建覆蓋整個區域的大板，再切成較易製造的尺寸（Split a Panel） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Panel 視窗
*圖 22-10　Create Panel 視窗：名稱、厚度、Justification、Representation 與建立方式。（AVEVA 官方文件截圖，僅供內部教學）*

其他板的操作：**Merge Panels**（共面板合併）、**To Miter a Panel with a Section or GENSEC**、**Create Negative Extrusions**（負拉伸，可做開孔）、**Position Panels／Orientation of Panels**、**Trim Panel**。

### 22.8.3 板的連接

文件說明三種主要連接模式（**Edge to**、**Edges to**、**Drag Edge to**）；另有 Disconnect Panels 還原。各模式的詳細參數請查官方頁面〔本章未深入逐項核對〕。

### 22.8.4 板配件（PFIT）與開孔

**Panel Fitting（PFIT）** 表示附著在板上的東西：穿越的管路、檢查蓋、門、人孔等。幾個要點：

| 項目 | 說明 |
|---|---|
| 型別 | Single、Compound、Sub-Compound 三種 soft element |
| 位置 | 用 **POSI** 相對於擁有者板的原點定位 |
| 方向 | 用 **BANG**（Beta Angle）繞垂直板面軸旋轉 |
| 對齊 | 用 **SJUS** 設為對齊板的頂面、中心面或底面 |
| 開孔 | 配件可含（或完全由）負體積組成，代表在擁有者板上的孔 |
| 初始位置 | 新建時自動置於擁有者板原點，再用標準方式移動 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Panel Fitting 視窗
*圖 22-11　Create Panel Fitting 視窗：以標準人孔蓋（Access Cover）為例，設定 Justification、Beta Angle 與位置。（AVEVA 官方文件截圖，僅供內部教學）*

所以「在板上開人孔」其實是「在板之下建一個帶負體積的 PFIT」，而不是直接修改 PLOO。

### 22.8.5 牆與地板

Walls and Floors 的結構與板類似，牆、地板都是 Panel 的 soft type：

| 元素 | 說明 |
|---|---|
| FLOOR | 建立時自動帶出 PLOO 與四個 PAVE（矩形）；建立前需有預設地板規格、該樓層的儲存區域，且 CE 要是複合地板 **CFLOOR** |
| 直牆／環牆 | Straight Wall、Ring Wall；牆規格的 Pline Settings 與型鋼相同有 Justification、Member Line、Joint Line，並在 Properties 設定牆的厚度與高度 |
| Screed | 整平層，可 Modify Screed Slope（修改斜度）、Split |
| Trace Boundary | 描摹邊界 |
| 牆／地板配件 | Create Wall Fittings、Create Floor Fittings |

與板相同：牆與地板規格沒有 Catalogue Reference，厚度可被覆寫。其他功能：Split／Splice／Merge／Miter Walls，以及 Positioning／Orientation／Connect。

### 22.8.6 彎板（Bent Panels）

彎板由**兩片以上的平面板**組合而成：

| 條件 | 說明 |
|---|---|
| 平面板的選擇順序 | 需依正確順序選，才能得到預期形狀 |
| 相鄰平面不可平行 | 否則無法彎折 |
| 孔與配件 | **不會**被複製到新彎板；需於彎板上另行處理（Fittings and Holes in Bent Panels） |
| 元素型別 | 可選 **BPANEL**（建議）或舊版相容的 Panel |
| Mould line | 選 BPANEL 時要指定，存於 **WJUSLINE** 屬性 |
| 第一片平面板 | 決定位置、方向與厚度，**必須是矩形** |
| 建立 | Create > Bent Panel，或從 SteelWork Utilities 的 Bent Panel 按鈕；可 Modify、Divide |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Bent Panel 視窗
*圖 22-12　Create Bent Panel 視窗：Bent plate type（BPANEL）與 Mouldline 設定。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.8.7 二次開發怎麼用

| 目的 | 資料 | 說明 |
|---|---|---|
| 板厚 | PLOO 的 HEIG | 文件明說 HEIG 為拉伸距離 |
| 板輪廓與面積 | PAVE 的位置與圓角半徑 | 如何取得頂點座標、計算面積的 PML 語法〔待核對〕 |
| 彎板 mould line | WJUSLINE | 屬性名稱取自文件 |
| 板配件位置／轉角／對齊 | POSI、BANG、SJUS | 屬性名稱取自文件 |

## 22.9 Access Platforms, Stairs and Ladders（ASL）

ASL 是一套專門處理平台、樓梯、爬梯與欄杆的組立式功能。文件有三種讀者分工：**Administrator（管理者）**定義標準與規則；**User（使用者）**在模型中建立組立實例；**ASL Modeller** 是較傳統的操作式應用（直接建立平台、樓梯、爬梯、柱與欄杆）。

### 22.9.1 組立（Assembly）概念

ASL 的高階管理元素都由 **STRU** 擁有，並且都是 **POS/ORI** 元素（帶位置與方向）：

| 元素 | 中文 | 說明 |
|---|---|---|
| STRTWR | 樓梯塔 | 由 STRFLT（樓梯段）與 STRLNG（樓梯平台）組成 |
| STRFLT | 樓梯段 | 單一梯段 |
| STRLNG | 樓梯平台（Landing） | 樓梯塔中的平台 |
| LADDER | 爬梯 | 爬梯組立 |
| PLTFRM | 平台 | 邊界由 RPATH 定義 |
| HANDRA | 欄杆 | 欄杆組立 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕ASL 組立元素階層
*圖 22-13　ASL 組立在 STRU 之下的階層：PLTFRM、STRTWR、STRFLT、HANDRA、LADDER。（AVEVA 官方文件截圖，僅供內部教學）*

這些元素本身只是**行政性容器**，實際幾何由既有的鋼構物件（**GENSEC、Panel、Template、Fixing**）擔任。換言之，一座平台在資料庫裡是 PLTFRM 底下掛了一堆熟悉的鋼構元素。這對二次開發者是好消息：你既有的結構報表邏輯大多可以沿用，只要多處理一層組立元素。

### 22.9.2 三個支撐概念

| 概念 | 說明 |
|---|---|
| 簡化參數化 | 把工程準則（參數與規則）與組立幾何脫鉤，任一組立可交給對應的「標準」（standard）驗證與管理 |
| 系統評估工程準則 | 使用者在 3D 環境操作，系統依規則評估屬性並透過階層管理 |
| **APPLDW**（Application Data World） | 管理性質的資料區，用來存放可複製／傳播的組立與模型零件，與 Template 類似但更通用；**不屬於設計本身**，除非特別指示，不會被干涉檢查、質量特性、Collection 等模型查詢存取；也供 Piping 專業使用 |
| **RPATH**（General Routing Path） | 通用的路徑或封閉邊界物件，供 Platform 與 Handrail 等使用；目的是提供可預期、有內部一致性檢查、在修改路徑時仍能保留資料的資料結構 |

> **專業提醒：** APPLDW 內的元素「不是設計」。所以寫報表或檢查程式時，如果從 SITE 遞迴掃描全庫，要確認不要把標準範本當成真實構件；反過來，若需要列出標準定義，才要明確去讀 ASLCONFIG。

### 22.9.3 管理者要準備什麼

| 項目 | 說明 |
|---|---|
| 存取權限 | 管理者需對資料庫與 APPLDW 資料有讀寫權限。文件說明：SYSTEM 使用者需為 **/ASLADMIN** 團隊成員，該團隊擁有 **/ASLCONFIG** 資料庫，隨版本提供的範例準則與組立資料就在其中 |
| MDB 設定 | ASLCONFIG 資料庫應納入所有管理者會建立／修改標準、使用者會建立 ASL 組立的 MDB |
| Storage Area | 建立新標準、次要標準或組立幾何之前要先指定儲存區域，否則系統警告；**Settings > ASL Storage Area** 開啟 ASL – Default Storage Area 表單，管理者可見 Standards 區，一般使用者看不到 |
| 標準與屬性 | 管理者建立 Standards、Secondary Standards、Properties |

管理者指南另有各組立專章：STRTWR、STRFLT、LADDER、PLTFRM、HANDRA 都各有 Database Hierarchy 與 Description of Elements 兩頁，完整元素清單請參閱官方頁面。

### 22.9.4 使用者的操作（ASL 使用者指南）

| 組立 | 重點 |
|---|---|
| 樓梯塔 | Create Stair Tower Definition Form、Stair Landing Layout Definition、Stair Flight Layout Definition |
| 樓梯段 | Create Stair Flight Form |
| 爬梯 | Create Ladder Form |
| 平台 | Create Platform Form；**Platform Opening** 表單可建立、修改、刪除平台開孔，開孔數量顯示在表單的格線；平台邊界可由預設形狀樣板、自由草繪（Route sketching）、或從其他型鋼元素描摹邊界取得 |
| 欄杆 | Create Handrail Form、Handrail Geometry、**Gates**（門）的新增／刪除、修改與刪除作業 |

操作環境：Graphical Previews（圖形預覽）、On Screen Dimensions（螢幕標註）、Storage Areas、Creating Instances of Assemblies（建立組立實例）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Platform 表單
*圖 22-14　Create Platform 表單：名稱、厚度、方向、位置與平台幾何。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.9.5 欄杆組立規則（文件「Handrail Assembly Rules」）

這是了解欄杆為什麼長成這樣的關鍵：

| 類型 | 判定 |
|---|---|
| Regular（非 Panelised）欄杆 | 組立含 **HRPOST** 與任意數量 RAIL，則視為一般非嵌板式欄杆；可選用 **KICKPL**（踢腳板）或嵌板 **HRPANE** |
| Panelised 欄杆 | 以嵌板為主體（細節請查該頁） |
| HRPOST 規則 | 組立中**第一個** HRPOST 被用作所有該欄杆實例中柱子的範本，其餘忽略；柱子依 RPATH 以 ZDIS 及參考點 POINTR 定位，故 HRPOST 應沿 Z 軸對稱建立、下端在原點；若需偏移可設 ZOFF 或 XOFF；應用程式只設定 HRPOST 的 POSREF、ZDIS、XOFF（只改符號，絕對值保留），其餘屬性保持組立中的初始值 |
| 其他元素 | HRTERM（欄杆終端）、KICKPL、HRPANE |

> 〔公開版未收錄：AVEVA 官方產品截圖〕欄杆（HANDRA）組立資料階層
*圖 22-15　欄杆組立的資料階層：RPATH、HRPNSE、HRKPSE、RAILSE、HRFEAT、POSTSE。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.9.6 ASL Modeller

ASL Modeller 是另一條較手動的路徑，文件列出的主要功能：

| 類別 | 功能 |
|---|---|
| 平台與走道 | 建立矩形平台、圓形平台、穿過平台的開孔（Penetration） |
| 樓梯 | 依指定尺寸建立、或在指定樓層間建立 |
| 爬梯 | Step Ladder、前方或側方出口爬梯 |
| 柱、欄杆、踢腳板 | Create Posts and Joints、Create Handrails、Create Kickplates |
| 定位 | 用參考點定位樓梯與爬梯（Reference Points） |
| 細部修改 | Stretch／Trim primitive、Slide primitive、改變樓梯／爬梯欄杆方向 |
| 其他 | 參數預設值（Parameter Default Settings）、Set Drawing Representation Levels（出圖表現層級） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕平台的三種常見型式
*圖 22-16　ASL 平台型式示意：矩形平台、轉角平台與回頭通道平台（含欄杆）。（AVEVA 官方文件截圖，僅供內部教學）*

### 22.9.7 二次開發怎麼用

| 目的 | 資料 | 說明 |
|---|---|---|
| 列出所有平台、樓梯、爬梯、欄杆 | STRU 之下的 PLTFRM、STRFLT／STRTWR、LADDER、HANDRA | 元素型別名稱取自文件；以型別篩選的 PML 語法〔待核對〕 |
| 欄杆長度與柱數 | HRPOST 與 RPATH | 實際屬性〔待核對〕 |
| 組立所依據的標準 | 組立與 ASLCONFIG 中 Standard 的關聯屬性 | 官方管理者指南有說明概念，具體屬性名稱本章未逐頁核對〔待核對〕 |
| 排除範本資料 | APPLDW 下的元素 | 文件說明這些資料預設不被模型查詢存取 |

## 22.10 檢查、報表與圖面輸出

### 22.10.1 設計者的三件事

官方 *Check and Output Design Data* 頁面把輸出歸納為三類，並指出這些與其他專業共用，細節在 *Design Common Functionality User Guide*：

| 輸出 | 內容 |
|---|---|
| 材料報表 | 依斷面型別分類列出建造所需材料 |
| 質量特性分析 | 重心、表面積、重量 |
| 結構佈置圖 | 以 Plot 方式輸出結構佈置 |

另外，設計過程應持續檢查**干涉（clash）**，也就是不同設計元素的空間重疊。文件強調「先解決干涉再出報表」。板、牆與地板的 Representation 設定（Levels、Obstruction）會影響它們在 3D 顯示與干涉檢查中如何被處理。

### 22.10.2 建議的出圖前檢查表

```
□ 所有 SCTN 都有有效的 SpecRef (Profile)
□ 沒有 CREF 為 Nulref 的殘留 SJOI (用 Tidy Joints 清理)
□ 所有構件連接處的 Trim 到正確 P-line
□ 斜撐兩端接頭為 Dominant (若需保持間隙)
□ 板的厚度與規格一致 (沒被不小心覆寫)
□ 板配件 / 開孔位置正確，彎板的孔與配件已重做
□ Storage Area 正確，構件都在預期的 FRMW / SBFR 之下
□ 結構與管路、設備干涉已檢查
□ ASL 組立的開孔、欄杆門都已處理
```

### 22.10.3 圖面輸出

文件的 *Sample Plots* 頁面提供多張結構樣本圖（圖面本身是輸出示範，不在本章插入）。ASL Modeller 提供 **Set Drawing Representation Levels**，可調整組立在圖面中的表現層級；型鋼的 **Member Line**（出圖時顯示的線，例如中心線）決定單線圖面的顯示位置。從模型到圖紙的 Draft／Drawing 流程請參考相關章節。

### 22.10.4 二次開發：典型報表設計

| 報表 | 要抓的資料 | 注意事項 |
|---|---|---|
| 型鋼材料清單 | 每個 SCTN 的 Profile（SPRF）、長度（POSS／POSE 與端部處理）、材料 | 長度與重量的專用屬性是否存在〔待核對〕；先決定要用理論長度還是下料長度 |
| 板材清單 | PLOO 的 HEIG、PAVE 頂點（面積）、材料 | 彎板要另外處理；開孔（PFIT 的負體積）是否要扣面積需明確約定 |
| 連接完整度檢查 | SNOD、SJOI、CREF、JOISTART／JOIEND、JFRE | 本章 22.7.6 |
| ASL 組立清單 | STRU 之下的 PLTFRM、LADDER、HANDRA 等 | 排除 APPLDW 內的範本 |
| 結構樹品質檢查 | 每個 SCTN 所屬 FRMW／SBFR 命名是否符合專案規則 | 命名規則由專案決定 |

> **專業提醒：** 不論哪種報表，建議先在 Design Explorer 對一小段已知結構人工清點，作為你工具輸出的「標準答案」。結構模型的資料關係多、Justification 與端部處理又會影響長度，人工比對比相信程式更可靠。

## 22.11 常見錯誤與排除

| 症狀 | 可能原因 | 處理 |
|---|---|---|
| 新建的構件找不到 | Storage Area 沒設，或設到別的 SBFR | 回 Settings > Storage Areas 檢查，用 Design Explorer 搜尋 |
| 梁與柱連接處長度不對 | Pline Rule 未設好 | 使用 Trim to Pline；並在加斜撐前修正 |
| 斜撐沒有自動保持間隙 | 點選順序錯（先點梁後點柱），或接頭是 Subordinate | 先點被連接的構件；斜撐兩端接頭設為 Dominant |
| 接頭在 3D 視圖看不到 | SJOI 沒有 Catalogue 規格，沒有幾何 | 指定接頭規格 |
| 移動構件後節點錯位 | 沒執行 Align Secondary Nodes | 使用 Drag Explicitly，或事後 Align Secondary Nodes |
| Axes 對 SCTN 失敗 | 元素沒有直接 Orientation 屬性 | 改用 Beta Angle、Flip、Rotate |
| Ship Reference 視窗報錯 | 元素沒有 POS 屬性 | 換用 Explicitly (AT) |
| Fillet 後配件不見 | GENSEC 不能有配件，文件說明會被刪除 | Fillet 前先確認，之後重新加配件 |
| Fixing 視窗是空的 | Paragon 端的 TABGRO 未建立，或 PURP／SPTYPE 沒設為 STFX | 請 Catalogue 管理者補料 |
| 彎板少了孔與配件 | 官方行為：原平面板上的孔與配件不會複製 | 彎板建立後重做 |
| 板的位置上下相反 | 頂點建立方向（順／逆時針）影響 Justification | 檢查頂點順序，或改 Justification |
| 平台／欄杆組立出錯 | 缺少 ASLCONFIG 在 MDB 中，或 Storage Area 未設 | 找系統管理員檢查 MDB 與 /ASLADMIN 團隊設定 |
| 報表多出一堆「構件」 | 掃描到 APPLDW 範本 | 限定掃描範圍 |

## 22.12 本章小結

1. Structures 由四個應用程式組成：Beams and Columns、Panels and Plates、Walls and Floors、Access, Stairs and Ladders；它們共用 STRU 之下的資料階層。
2. 核心觀念是 **Design／Catalogue 分離**：Design 存位置與方向，Catalogue 存形狀與材料，以 SpecRef 相連；板、牆與地板例外，沒有 Catalogue 項目。
3. 構件的位置由 POSS／POSE 與 Justification 決定；P-line（PKEY）是定義「對齊到斷面哪一條線」的語言。
4. 連接靠 SNOD 與 SJOI，CREF 與 JOISTART／JOIEND 互相參照；**JFRE** 決定移動時是否連動。
5. 修整工具各有適用條件：Split／Splice／Merge／Fillet／Miter；Fillet 會刪除配件，彎板不會複製孔與配件。
6. 板的厚度是 PLOO 的 HEIG，頂點是 PAVE，板配件 PFIT 用 POSI、BANG、SJUS 定位並以負體積做開孔。
7. ASL 組立是管理性容器（STRTWR／STRFLT／LADDER／PLTFRM／HANDRA）加上熟悉的鋼構元素；規則在 ASLCONFIG／APPLDW，要先有管理者設定，使用者才能建立。
8. 官方文件對 PML 語法著墨極少。二次開發要建立在「屬性名稱」之上，並自行用實際專案環境驗證查詢語法。

## 22.13 練習題與自我檢核

### 概念題

1. 說明 SCTN 的哪些資料在 Design 資料庫、哪些在 Catalogue 資料庫。為什麼修改 Catalogue 斷面定義會影響模型中所有引用它的構件？
2. Primary Node 與 Secondary Node 的差異是什麼？構件被移動時分別怎麼樣？
3. 解釋 JFRE 為 False 與 True 的差異。為什麼斜撐兩端的接頭通常要設為 Dominant？
4. 為什麼 Fillet 之後配件會消失？Merge 與 Fillet 的適用條件有什麼不同？
5. 板（PANE）的厚度存在哪個元素的哪個屬性？板為什麼沒有 Catalogue Reference？
6. ASL 組立的 PLTFRM、HANDRA 本身是什麼性質的元素？真正的幾何由什麼擔任？APPLDW 內的資料為什麼預設不被模型查詢存取？

### 操作題

7. 建立一組 2 x 2 的柱梁框架：先設定 Storage Areas 與預設型鋼規格，用 Explicit 建柱、用 Pick 建梁，確認 Design Explorer 中每個 SCTN 都掛在預期 SBFR 下並自動產生 SNOD／SJOI。
8. 在上題框架加一支斜撐，兩端接頭設為 Dominant；移動其中一根柱，觀察斜撐是否保持間隙；再改成 Subordinate 重複一次，記錄差異。
9. 在框架上方建立一塊覆蓋整個區域的地板鋼板，切成四塊，並在其中一塊上加一個帶負體積的板配件作為人孔。
10. 若環境已部署 ASL：用 Create Platform Form 建立一座矩形平台，加 Platform Opening 與 Handrail，並在 Design Explorer 找出 PLTFRM 與 HANDRA 之下的元素。

### 二次開發題（設計題）

11. 設計一支「連接完整度檢查」工具：列出所有 SCTN 的 JOISTART／JOIEND 是否有效、所有 SJOI 的 CREF 是否為 Nulref、斜撐接頭的 JFRE。寫出輸入、輸出欄位與你需要〔待核對〕的 PML 語法清單。
12. 設計「型鋼材料清單」報表：決定長度使用理論長度還是下料長度，並說明如何處理 Split、Splice、Miter 之後的構件。
13. 設計「板材清單」報表：說明如何取得厚度、輪廓面積、是否扣除開孔，以及彎板如何處理。

### 自我檢核

| 項目 | 能做到請打勾 |
|---|---|
| 能畫出 STRU > FRMW > SBFR > SCTN > SNOD > SJOI 階層並說明用途 | □ |
| 能說明 SpecRef、SPRF、P-line、PKEY 的關係 | □ |
| 能完成 Storage Areas 與預設規格設定 | □ |
| 能區分 AT、BY、Extend、Drag、Ship Reference 五種位置調整 | □ |
| 能說明 JFRE 與 Dominant／Subordinate | □ |
| 能列出 Split／Splice／Merge／Fillet／Miter 的條件與副作用 | □ |
| 能說明 PANE／PLOO／PAVE／PFIT 的關係 | □ |
| 能說明 ASL 組立與 APPLDW、RPATH、ASLCONFIG 的角色 | □ |
| 能列出結構報表要抓的資料並標出需要驗證的語法 | □ |

## 附錄 22-A　本章〔待核對〕項目彙整

| 編號 | 項目 | 原因 |
|---|---|---|
| A1 | STRU 之下可直接掛哪些元素（FRMW、板、ASL 組立）的確切階層 | 文件僅以文字與圖片說明，離線頁面未取得圖內容 |
| A2 | 長度、重量等專用屬性與 POSS／POSE 的座標基準（WRT） | 文件未給屬性語法 |
| A3 | 材料在 Design 元素中對應的屬性 | 文件只描述 GUI 的 Modify > Material |
| A4 | 如何由 SCTN 取得 Catalogue 參數化尺寸值 | 文件未提供查詢方式 |
| A5 | Primary Node 的元素型別名稱（PNOD） | 本章依文件描述推論 |
| A6 | 判斷 JOISTART／JOIEND、CREF 空值（Nulref）的 PML 寫法 | 文件只提屬性名稱 |
| A7 | 批次切換 Dominant／Subordinate 的 PML 指令 | 文件只提供 GUI 選單 |
| A8 | PAVE 頂點座標、板面積的 PML 取得方式 | 文件未提供 |
| A9 | Include Structure 的具體語意；Panel 三種連接模式的參數細節；Standard Bracing Configurations 的選項 | 本章僅列名稱，未逐頁核對 |
| A10 | ASL 組立與 Standard 關聯屬性名稱；以型別篩選 ASL 元素的語法 | 管理者指南有概念說明，屬性層級未逐頁核對 |
| A11 | 各選單路徑與視窗名稱 | 以 12.1 文件為準，實際安裝若客製化可能不同 |
