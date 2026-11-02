# 第 29 章　外部整合與舊版開發工具：Interfaces 與 Legacy Applications

> 前面的章節多半在 AVEVA Marine「裡面」做事；這一章看「邊界」。官方文件有兩大區塊專門處理邊界：**Interfaces** 談 Marine 如何和 AVEVA ERM、Catalogue Manager、AVEVA NET、AutoCAD、MicroStation、Rohr2 等外部系統交換資料；**Legacy Applications** 收容舊版開發工具（Developer's Toolkit、Vitesse、Data Extraction 與各種 Keywords）。對二次開發者而言，前者回答「資料要怎麼被別的系統看見」，後者回答「舊的船體與圖面腳本還能不能用、怎麼維護」。
>
> 本章不重講 Vitesse 的目錄與寫法、資料抽取的取值三步驟（見[第 15 章](ch15_hull_vitesse_zh-TW.reading.html)）、檔案與 CSV／ERP 整合的通用做法（見[第 16 章](ch16_reports_integration_zh-TW.reading.html)），也不重講 PML 讀資料庫（見[第 12 章](ch12_pml_database_zh-TW.reading.html)）。本章補的是那些章節沒涵蓋的部分：**ERM–Design 整合的通知機制與設定、材料對應、舊版工具的官方規格（Trigger、Utility／UI 介面、環境變數、批次執行）、Keywords 的結構與外部介面總覽。**
>
> **資料可信度：** 內容取自 AVEVA Marine 12.1 官方離線文件的 *Interfaces* 與 *Legacy Applications* 兩大章節。官方文件是使用者指南，**整合部分幾乎沒有程式碼**，資料表與 PML 函式只列名稱，內部實作看不到；Legacy 部分有 Python 與 PML 片段，本章僅引用文件實際出現者。沒有文件依據的細節一律標〔待核對〕，彙整於 29.16。官方文件仍沿用 PDMS 時代名稱（例如 `PDMSUSER`、`run_pdms_command`），照原樣保留。

## 29.1 學習目標

讀完本章，你應該能夠：

1. 區分 Interfaces 與 Legacy Applications 兩大區塊各收了什麼，並判斷某個整合需求該找哪一份文件。
2. 說明 AVEVA ERM–Design Integration 的角色分工：Design 應用程式、Notification Service、Integration Service、AVEVA ERM。
3. 描述 Update／Acknowledgement／Error 通知的流程，並說明為何已傳送的資料不會重複傳送。
4. 說明 `PublishingStatus`、Design Project Id、External Reference Id（`dabaconid`）與 Sent To Application 的用途。
5. 依畫面設定 Filter Configuration、Catalogue Manager 位置與 Integration Service，並說明 DB View 與 PML Function 兩種資料來源的差別。
6. 說明 Material Category Mapping 的邏輯，以及 Read／Write Attributes PML 函式的用途。
7. 說明標準材料、原板、型材、船體材料控制與刪除流程，並指出各自的資料交換方向。
8. 說明 Developer's Toolkit 在 12.1 的定位（僅 legacy 支援），並使用 Vitesse 選單、Log 視窗與 Batch Vitesse。
9. 區分 Vitesse Trigger、PML Trigger 與動態註冊的 Trigger，知道它們的優先順序。
10. 讀懂 Data Extraction 的語法（Keywords、引數運算子、資料庫來源後綴）與必要的環境變數，並知道完整 Keywords 清單在哪裡。

## 29.2 兩大區塊的地圖

| 區塊 | 約頁數 | 主要內容 | 開發者最常遇到的情境 |
|---|---|---|---|
| **Interfaces** | 655 | ERM–Design 整合、Catalogue Manager、AVEVA NET Gateway、Bocad、Design in Context、ExPLANT-A／-I、ImPLANT-I／-STL、Laser、Mechanical Equipment、Pipe Stress、Query（ODBC） | 材料表與規格要送到 ERP／採購；要把模型輸出給 CAD 或應力分析 |
| **Legacy Applications** | 241 | Developer's Toolkit、Vitesse、Data Extraction、Drafting／Hull／TDM Keywords、Python、.NET 連結 | 維護舊的船體與圖面腳本、Trigger；用資料抽取取船體資料 |

> **專業提醒：** 官方說明 Developer's Toolkit「只有 Vitesse 與 Data Extraction 的 legacy 支援」，意思是**不會再新增功能**，且只涵蓋 Marine Drafting 與 Hull Design。新需求先評估第 11 至 14 章的 PML 與 .NET；Vitesse 的任務是維護既有資產，或船體功能目前只有它能做時才用。

## 29.3 ERM–Design 整合：概念與通知流程

### 29.3.1 整合做什麼

AVEVA ERM–Design Integration 在 AVEVA Marine 與 AVEVA ERM（企業資源管理，管採購、物料、工作包與規劃）之間傳遞材料資訊，核心是**通知機制（Notification）**。入口在各模組的 AVEVA ERM Integration 選單（Hull Design 與 Marine Drafting、Outfitting 與 Outfitting Draft、Paragon 都有）：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull Design 的 View → Addins → AVEVA ERM Integration 選單，含 Settings、Publish to ERM、Notifications

*圖 29-1　整合入口：View → Addins → AVEVA ERM Integration。（AVEVA 官方文件截圖，僅供內部教學）*

選單含 Settings（設定整合）、Material Category Mapping（對應材料類別）、Publish to AVEVA ERM（發佈）與 Notifications（檢視自 ERM 收到的通知）。

版本需求：AVEVA ERM 16.0 以上、AVEVA Marine 12.1.SP5 Fix 19 以上、AVEVA Integration Service 2.0 以上。

### 29.3.2 通知流程

> 〔公開版未收錄：AVEVA 官方產品截圖〕Marine 到 ERM 的整合流程：Dabacon、Marine、Notification Service、Integration Service、ERM、Oracle DB 與五個步驟

*圖 29-2　Marine 發佈、ERM 匯入的通知流程。（AVEVA 官方文件截圖，僅供內部教學）*

流程重點：

1. 傳送端發佈資料。資料先透過 **DB View 或 PML Function** 備妥，且只有狀態為 `Published` 的項目會被列出。
2. 傳送端經 Notification Service 與 Integration Service 發出 **Update** 通知。
3. 接收端取回資料並匯入；成功回 **Acknowledgement**，失敗回 **Error**。
4. 兩種回覆都帶有資料資訊，傳送端據此更新發佈狀態，所以**已傳過的資料在有變更並重新發佈前不會再送**。
5. 失敗的項目，修正後可再發佈。

> 〔公開版未收錄：AVEVA 官方產品截圖〕ERM 到 Marine 的整合流程，方向相反，Marine 端同樣以 DB View 或 PML Function 匯入並回覆 ACK 或 ERR

*圖 29-3　ERM 發佈、Marine 匯入的反向流程。（AVEVA 官方文件截圖，僅供內部教學）*

| 角色 | 職責 |
|---|---|
| Client（ERM、Marine） | 發佈、檢視、更新、刪除通知 |
| Notification Service | 建立 Client 與 Integration Service 之間的通訊 |
| AVEVA Integration Service | 訂閱、儲存並發佈通知 |

### 29.3.3 五個整合概念

| 概念 | 意義與要點 |
|---|---|
| **Status Definition** | 安裝 Lexicon 模組時加入 Status Controller 的兩套狀態。`PublishingStatus`：Identified、WorkInProgress、PendingApproval、Rework、Approved、Published、Imported。`Pipe/HVACPublishingStatus`：IdentifiedPreliminaryPartList、PreliminaryPartListSentToERM、PreliminaryPartListReceivedByERM、FabricationIdentified、FabricationSentToERM、FabricationReceivedByERM。可用 AVEVA Administration 的 Lexicon 模組在 Dictionary Explorer 檢視，Graphical View 以綠、紅、黑箭頭表示 Promote、Demote、手動更新 |
| **Sent To Application** | 從 ERM 角度，通知送往哪個應用程式，依 `s14001 Integration Service` 畫面中「設計專案＋傳輸概念 Id」的設定決定；查不到記錄就送往 `s00033 External Source Applications` 畫面的預設應用程式 |
| **Design Project Id** | ERM 專案與整合設計專案是一對一（例：ABC 對 Design-ABC），隨所有概念傳遞。RawPlate、RawProfile、StandardMaterial 與專案無關，由 ERM 發佈時 Update 通知不帶設計專案；其餘概念皆與專案相關 |
| **External Reference Id** | 即 Marine 端元素的 `dabaconid`，存入 ERM 作識別。支援的概念：標準材料、專案元件、原板、原型材、圖面、設計規格、Fabricate、船體單元。需 ERM 13.0 與 Marine SP5 Fix1 以上；更舊版本需在 ERM 手動匯入同步一次 |
| **Notification Filtering** | Marine 端依「登入的 Project user」與「應用程式名稱（ERM s14001 畫面所定義）」過濾；使用者只看得到自己 Project user 的通知 |

> **專業提醒：** External Reference Id 是日後「對得起來」的關鍵。ERM 先建立的材料，要等 Marine 回覆的 Acknowledgement 帶回 `dabaconid` 才會建立對應；寫自訂程式處理通知時，不要用名稱當鍵值。

## 29.4 設定整合

Settings 視窗依功能分頁（不同模組與版本的分頁組合略有不同，圖例中出現 Filter Configuration、Import & Material Mapping Settings、Integration Service、Work Package To Assembly Mapping）。

### 29.4.1 Filter Configuration

每筆設定都要填：

| 欄位 | 說明 |
|---|---|
| List Based On | 自訂名稱，用來區分不同設定 |
| Select Element Type | 要篩選的元素型別 |
| Status Definition | 固定為 `/PublishingStatus` |
| Filtering Status | 元素處於此狀態時，才會出現在預覽畫面 |
| Publishing Status | 資料對 ERM 可見的狀態；除船體單元（Hull Unit）固定為 `/Identified` 外，一律為 `/Published` |
| Select Transfer List | 讓資料可被 ERM 取得的 DB View 或 PML Function（預設值可選） |

### 29.4.2 Catalogue Manager Settings

設定各類資料匯入 Marine 的位置，全部在 Catalogue Explorer 選位置後按 CE 加入：

| 設定 | 目的地限制 |
|---|---|
| Import Descriptions at、Import Bolts at、Import Wall Thickness at、Import Pipe Data at | 頂層 `CATA` 元素（Catalogue World） |
| Import Weights at | 頂層 `PROP` 元素（Property World） |
| Import Pipe Spec／Cable Spec／Stru Spec／Insulation Spec at | 頂層 `SPWL` 元素（Catalogue World） |

### 29.4.3 Integration Service 與工作包對應

> 〔公開版未收錄：AVEVA 官方產品截圖〕Settings 的 Integration Service 分頁，上為 Integration Service Setting、下為 Notification Service Setting

*圖 29-4　Integration Service 分頁：服務主機、埠號、URL、資料來源與通知服務設定。（AVEVA 官方文件截圖，僅供內部教學）*

| 區塊 | 欄位 | 說明 |
|---|---|---|
| Integration Service | Service Installed On、Port、Service URL | 主機、埠號、服務網址，按 Test 驗證 |
| | DataSource Type、DataSource Table | 必須是 AVEVA ERM；資料來源名稱 |
| | Load data automatically if elements are less than | 勾選後元素少於設定值（預設 200）自動載入 Notifications 畫面 |
| Notification Service | Time Interval (Minutes) | 抓通知的間隔，預設 1 分鐘 |
| | Sent To Application／Sent From Application | 必須為 AVEVA ERM／本端應用程式名稱 |
| | Auto delete when handled messages are more than | 已處理訊息超過數量（預設 10）自動刪除 |

**Work Package To Assembly Mapping**（Hull Design 與 Outfitting 模組）把 ERM 工作包對應到 Marine 的 Assembly：選工作包，在「Assembly Type in AVEVA Planning」下拉選類型，按 Add。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Work Package To Assembly Mapping 分頁：上方為已對應的 Assembly 與 Assembly Type，下方為 Production 階層與類型下拉

*圖 29-5　工作包對應 Assembly：2-BOT 對 Steel、2-MID 對 NonSteel。（AVEVA 官方文件截圖，僅供內部教學）*

### 29.4.4 DB View 與 PML Function

整合的「來源表」有兩種形式：**資料庫視圖（DB View）**與 **PML 函式**。文件列出的對照（節錄）：

| DB View | PML Function | 用途 |
|---|---|---|
| `StandardCatalogue_Published` | `StandardCatalogue` | 已發佈的標準材料 |
| `RawPlates_Published` | `RawPlate` | 已發佈的原板 |
| `RawProfile_Published` | `RawProfile` | 已發佈的原型材 |
| `ProjectComponents_Published` | `ProjectComponent` | 已發佈的專案元件 |
| `HullBlocks_Published` | `HullUnit` | 已發佈的船體塊 |
| `NestingList_Published` | `NestingList` | 已發佈的排料資訊 |
| `SteelPartList_Published` | `PartListSteel` | 船體鋼零件 |
| `Steel_Actualmaterial_Published` | `SteelActualMaterial` | 實際材料用量 |
| `OutfittingPartList_Published` | `PartListDesign` | 管路、HVAC、電纜托架與支架以外、以區域為基礎的零件清單 |
| `OutfittingPartList_Assembly_Published` | `PartListAssembly` | 舾裝零件清單組裝 |
| `FabricatePartList_Published` | `Structure` | 已發佈的 Fabricate 設計資料 |
| `ABOM_Published` | `ABOM` | 來自 AVEVA Diagrams 的 ABoM |
| `ExternalRefSync_Published` | `ExternalRefSync` | 自 ERM 12.2 升級時同步外部參考 |
| （無） | `Cableway`、`DrawingPartList` | 電纜槽、圖面零件清單 |

使用時的限制（文件明載）：用 PML Function 整合時，ERM 必須設為 **PML Safe mode**；用 DB View 時設為 **Non PML Safe mode**（見 ERM 的 s14001 畫面說明）；管路、HVAC 與螺栓零件清單**只能**走 `PartListDesign` PML 函式，沒有對應 DB View。

> **開發人員須知：** 這就是「二次開發者怎麼接」的第一個入口：**客製整合不是去改 Notification，而是提供或調整 PML Function**，讓它回傳 ERM 要的欄位。函式的回傳格式與欄位清單在 Marine 文件中看不到，須取預設函式實測〔待核對〕。

## 29.5 材料對應（Material Mapping）

ERM 以 Material Id 識別標準材料、原板與原型材；Marine 以元件名稱識別，且元件存放在 Catalogue 的 Section 與 Category 結構下。**對應的鍵值是 ERM Material Type**，它隨傳輸欄位一起傳送；Marine 透過 mapping table 把每個 ERM Material Type 對到 Catalogue／Section／Category。

| 情境 | 查表方式 |
|---|---|
| 從 ERM 匯入新材料 | 用傳來的 Material Type 查 mapping，決定存入哪個 Category |
| 找出要傳給 ERM 的新增或修改項目 | 查遍 mapping table 內定義的所有 Category |

附加資料（如重量）可存在元件的 `GPART`（透過 `CMPD`），而不是元件本身；建立 `GPART` 與 `CMPD` 前，要先定義 `PRTWLD`、`PRTELE`、`CMPW`、`CMPT`。多數共用屬性可存為 UDA；可定義 PML 腳本讀寫所有共用屬性。

### 29.5.1 建立與設定

建立新對應：Material Category Mapping 對話方塊 → Material Mapping 分頁 → Add → 選 `GPART`（欄位自動帶入）→ 輸入 ERM Material Type → Apply。也可按 **Auto Generate Mapping**（為目前 MDB 內可用的 `GPART`、`SCOM`、`SPRF` 產生），或 **Auto Generate CE**（目前元素與其子元素）。

| 設定 | 說明 |
|---|---|
| Material Type Max Length | ERM Material Type 長度上限，預設 50 |
| Material Type Auto Generate PML | 自動產生時，從 PML 腳本讀取 Material Type；未提供時預設使用 `ermgetmaterialtype.pmlfnc` |

匯出：File > Export to CSV，產生 `.csv` 供 ERM 貼入其 Material Category Mapping 畫面。

> **專業提醒：** 在匯入或發佈標準材料、原板、原型材之前，兩端的 ERM Material Type 必須已同步。

### 29.5.2 原板、原型材對應

> 〔公開版未收錄：AVEVA 官方產品截圖〕Plate/Profile Mapping 分頁：ERM Material Type、Material Description、Read Attributes、Write Attributes、TABWLD、RPLTAB

*圖 29-6　Plate/Profile Mapping：把原板與原型材對應到 ERM 材料類型。（AVEVA 官方文件截圖，僅供內部教學）*

| 欄位 | 說明 |
|---|---|
| ERM Material Type、Material Description | ERM 材料類型名稱與說明 |
| **Read Attributes** | 讀取與 ERM 共用之元件屬性的 PML 函式 |
| **Write Attributes** | 從 ERM 匯入時設定元件屬性的 PML 函式 |
| TABWLD | 原板或原型材的 Table world |
| RPLTAB／RPRTAB | 原板表／原型材表 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Raw Profile Type Mapping 分頁：Marine 型材類型代碼對應 ERM Dimension Code，例如 10 對 FB-10、30 對 L-30

*圖 29-7　Raw Profile Type Mapping：Marine 型材類型對 ERM 尺寸代碼。（AVEVA 官方文件截圖，僅供內部教學）*

預設的型材類型對應自 ERM 16.0 與 Marine 12.1 SP5 Fix 17 起提供；若自行新增或修改，**必須在傳送原型材之前，於 ERM 加入同樣的對應**。

## 29.6 各類資料的整合

### 29.6.1 目錄類：Catalogue Manager、標準材料、原板、型材

**Catalogue Manager 整合**（方向：Catalogue Manager → Marine）：規格在 AVEVA Catalogue Manager 核准或發佈後，Marine 收到 Update 通知並匯入；成功回 Acknowledgement，失敗回 Error，需重新發佈規格。可匯入的規格：Pipe、Bolt、Cable tray、Insulation、Structure，連同 `SPCO` 元素；每份規格匯入 Material Description、Component Weight、管與壁厚資料、螺栓表資料與規格本身。

- `SPCO` 名稱不得超過 50 字元（Dabacon 資料庫限制）。
- 從 ERM 匯入螺栓或規格前，須先在 ERM 的 `s81060 PDMS Attributes` 畫面建立名為 `MATERIAL_ID` 的 UDA；匯入後 Paragon 中 `SPCO` 元素顯示為 Material_Id、`DTAB` 元素顯示為 Material_Id1。

流程：核准或重新發佈規格 → 確認匯入位置 → 在 Marine 匯入 → 檢視 → Catalogue Manager 收到回饋。

**標準材料**（管、管件、彎頭、法蘭等與專案無關的項目）在兩端都存在：ERM 的材料定義畫面（`s20011`）對應 Marine Paragon 的 `GPART`、`SCOM`、`SPRF`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕標準材料概念：Marine Paragon 的 Standard Material 由 GPARTs、SCOMs、SPRFs 組成，對應 ERM s20011 Material Definition

*圖 29-8　標準材料在兩個系統的對應關係。（AVEVA 官方文件截圖，僅供內部教學）*

| 資料 | 雙向共用的屬性 |
|---|---|
| 標準材料 | Component Name、Material ID、Material Type、Description、Technical description、Design Status、Manufacturer、Design／ERM Technical Responsible User、Weight、External_Ref |
| 原板 | 上列大部分，另含 Quality Code、Height、Length、Width、Density（沒有 Weight、Material ID） |

兩個方向的步驟：

| 方向 | 步驟 |
|---|---|
| Marine → ERM | 設定篩選 → 更新狀態 → 發佈 → 在 ERM 匯入 → 驗證 → ERM 回饋 → Marine 處理回饋 |
| ERM → Marine | ERM 發佈 → 在 Marine 匯入 → 驗證 → Marine 回饋 → ERM 處理回饋 |

原板與原型材的流程相同。ERM 收到 Acknowledgement 時，若帶有 ExternalReferenceId，該材料就取得對應的外部參考。Marine 端手動匯入通知（Manual Import）的概念：Paragon 為 Standard Material、Raw Plate、Raw Profile、Design Specification。

### 29.6.2 專案、系統與零件清單

| 資料 | 要點 |
|---|---|
| System Hierarchy | ERM 的 Systems 是材料、工時與費用的縱向成本歸集；階層可多層或扁平。方向 ERM → Marine，可匯入 Hull Design 與 Outfitting |
| Project Component | 專案元件定義於 AVEVA Engineering 的 Engineering list；Marine 的設備材料也能傳成專案元件。Marine → ERM 前先設定 `EQUIPMENT` 的 material type 與系統。從 AVEVA Engineering 取資料用 `Equipment_View`、`Released_For_Procurement` 兩個 DB View；ERM → AVEVA Engineering 用其 Compare/Update 功能 |
| ABoM | 設計早期的預估採購需求；之後由零件清單的實際需求取代，只有實際需求超過 ABoM 時才新增採購需求。來源 AVEVA Diagrams |
| Part List | 來源表為 PML 腳本；狀態達 `Published` 即可傳送，ERM 取用後 Marine 端狀態改為 `Consumed`，確保同一批資料變更前不再重傳 |
| Zone 型 | 傳送整個 Zone，存成 ERM 圖面目錄（`s20012`）中的一張圖；**不可**用於管路、HVAC、電纜槽的 Zone。傳送前須先發佈各零件清單元素 |
| 圖面型 | 從 Outfitting Draft 或 Marine Drafting 傳送，圖面內所有元素存為零件清單，同時在設計應用程式建立同元素 Assembly，可直接做組裝規劃。元素只會發佈一次，先發佈的圖面成為擁有者；含共同元素的多張圖不可同時發佈。Marine Drafting 僅支援舾裝零件清單 |

### 29.6.3 船體材料控制

船體概念涵蓋 Assembly／Block 以下所有帶有材料或設備參照的物件。資料經 DB View 或 PML Function 識別，並以 Status Control 提升到可傳送的狀態。

> 〔公開版未收錄：AVEVA 官方產品截圖〕船體整合概念：Marine 的 Hull Manufacturing 與 Hull Detail Design 對應 ERM 的 Hull Units s30001、Nesting Hull Info s30002、Fabricate Catalogue s20017、Part list s21000

*圖 29-9　船體概念在 Marine 與 ERM 的對應。（AVEVA 官方文件截圖，僅供內部教學）*

| 步驟 | 說明 |
|---|---|
| Transfer Hull Units | 建立船體單元，用來配置之後排料使用的原板、原型材；Publishing Status 為 `/Identified` |
| Importing Allocated Material for Nesting | 把 ERM 配置的原板、原型材配到 Marine 專案供排料 |
| Transferring Nesting Information | MANPKG 排料完成後傳給 ERM，焊接與切割資訊在 ERM `s30002 Nesting Info - Hull` 維護 |
| Publish Actual Material Usage | 把實際材料用量發佈到 ERM（文件僅概述） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Manufacturing Explorer 與兩個屬性視窗：Avbity 為 Consumed、MidErm 為 473849，並有 MatLength、MatWidth、Thickn、Matref、RplRef 等屬性

*圖 29-10　排料物件上的整合屬性：Avbity、MidErm 與材料尺寸。（AVEVA 官方文件截圖，僅供內部教學）*

整合屬性可在 Attributes 視窗切換 Categorized 後，於 **ERM Integration** 類別下看到完整清單；在 Notifications 或 Publish 視窗的明細區右鍵 **Navigate to**，可在 Design 或 Catalogue Explorer 中定位元素。

### 29.6.4 刪除流程與即時資料

刪除規則：已傳送的資料，在一端刪除需**另一端核准**；未傳送的由擁有者直接刪；非擁有者不能刪（除非具管理員權限）。使用 `CanDeleteRequest`、`CanDeleteAcknowledgement`、`CanDeleteError`、`Delete` 四種訊息。

> 〔公開版未收錄：AVEVA 官方產品截圖〕刪除流程：System 1 發出 CanDeleteRequest，System 2 判斷後回 CanDeleteError 或 CanDeleteAcknowledgement，最後 Delete

*圖 29-11　雙系統刪除流程（兩端皆可作為發起端）。（AVEVA 官方文件截圖，僅供內部教學）*

**即時資料**：Design in Context 的資料也以**虛擬屬性（pseudo attributes）**提供給設計應用程式，可顯示在 Attributes 視窗、Engineering 清單與報表；經 Integration Service 連線，每個物件只連線一次並一併取回。ERM 端以既有 Data Extraction 功能建立 DB View。材料資訊含請購單、採購單、收貨狀態、交期、供應商；規劃資訊含工作包、預定與實際起訖、工時預算、安裝狀態與日期。設定入口為 TOOLS > Context > Configure（需先設定 Dashboard Server）。

> **開發人員須知：** 虛擬屬性讓報表與 PML 能像讀一般屬性一樣取得 ERM 資料；但屬性的 PML 名稱、是否支援 `COLLECTION` 篩選，文件沒有寫，需實測〔待核對〕。

### 29.6.5 常見錯誤

- 發佈後 ERM 看不到：多半是元素狀態未達 Publishing Status，或 Filtering Status 設定不符。
- 管路零件清單走 DB View 失敗：只支援 `PartListDesign` PML 函式，且 ERM 須為 PML Safe mode。
- 匯入規格沒寫入：匯入者無 Write 權，或目的地不是頂層元素。
- ERM 訊息沒被處理：Update 訊息須在 s14002 手動 Process，除非 s14001 勾選 Automatically Picked。

## 29.7 其他外部介面

這些介面各是一份獨立使用手冊；下表只整理定位，細節需進原文件。

| 介面 | 功能 | 備註 |
|---|---|---|
| **NET Gateway** | 把 Marine 的 Design 項目與屬性、SPOOLER 項目、Review 模型、DRAFT 圖面、Isometric 匯出到 AVEVA NET；設定由文字檔與 PML 物件檔組成（如 `%PDMSDFLTS%\DES-VNET-ITEMS`、`SPL-VNET-ITEMS`、`%PMLLIB%\vnet\settings\` 下的 `.pmlobj`） | 匯出設定可存檔載入，且只能載入同一模組存的檔案。AVEVA NET 端的 Breakdown Node 需 Portal 管理員設定 |
| **Bocad Steel Interface** | 以 ABS（專有、加密、壓縮）格式匯出入鋼構 | 安裝會產生 `Bocad_vars.bat`（`BOCMAIN`、`BOCDATA`）；須手動在 `evars.bat` 或 `custom_evars.bat` 加入呼叫，並把 `bocad` 複製到 UI 區的 `addins` 資料夾 |
| **Design in Context** | 在設計時查看 AVEVA AIM Dashboard 的關聯文件、搜尋與收藏集 | 需設定 Dashboard Server；文件列有 C# 的 Design in Context API 章節 |
| **ExPLANT-A／-I** | 將 3D 模型輸出為 DXF（AutoCAD）／dgn 第 7 版（MicroStation），-I 可附屬性文字檔 | 新版 MicroStation 可讀 dgn v7 |
| **ImPLANT-I／-STL** | 把 dgn 或 STL 轉成可匯入的 DESIGN 巨集檔 | STL 是近似曲面，**不保證 100% 精確轉換**；ImPLANT-I 2 對 dgn v8 支援不如 dgn v7 完整 |
| **Pipe Stress R2**、**Mechanical Equipment**、**Laser Model** | 與 Rohr2 交換 NTR 檔與應力結果；匯入 STEP AP203 機械設備模型；另購授權的雷射掃描模型顯示與碰撞 | 僅讀簡介頁 |
| **Query** | 以 SQL 經 **ODBC** 存取外部資料庫，可雙向讀寫；本質是讓使用者撰寫巨集的程式工具包 | 語法以圖表達，指令可縮寫（如 `CONnect` 可打 `CON`） |

> **專業提醒：** Query 與 ODBC 是「Marine 直接讀寫外部資料庫」的官方路徑，但文件只談語法，沒有與 PML 或 .NET 對應的做法；公司規範上，寫入外部資料庫仍建議照[第 16 章](ch16_reports_integration_zh-TW.reading.html)的資料契約與中介表原則，不要直接動對方的業務表。

## 29.8 Developer's Toolkit 與 Vitesse（舊版）

### 29.8.1 定位

Developer's Toolkit 是讓有程式能力的客戶自行開發功能的工具集，在 12.1 僅有 Vitesse 與 Data Extraction，且只支援 **Marine Drafting 與 Hull Design**。官方列出的用途：取模型資料出報表、自動化圖面、自動建立與修改模型資料、開發互動功能、與其他系統整合。

### 29.8.2 安裝與環境變數

| 變數 | 用途 |
|---|---|
| `SB_SYSTEM` | 安裝根目錄 |
| `SB_PYTHON` | Vitesse 主目錄；從檔案瀏覽器執行腳本時的預設目錄 |
| `SBB_TRIGDIR` | Trigger 腳本目錄（預設為安裝根目錄下 `\Vitesse\Trigger`），標準 Trigger 會用，通常不要改 |
| `PYTHONPATH` | Python 搜尋模組的路徑，安裝時自動設定並**覆蓋舊值**；使用者目錄須安裝後再加入 |

> **專業提醒：** 安裝其他軟體可能改動 `PYTHONPATH` 而讓 Vitesse 失效。官方 Installation 頁寫執行階段 Python 函式庫為 **2.4.2** 版，而第 15 章整理的是 Python 2.6 語法限制，兩者不一致，須在公司安裝實測確認版本〔待核對〕。

### 29.8.3 選單、Log 與選項

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull Design 的 Tools → Vitesse 選單：Run script、Run selected、Files、Edit、Debug、Log window、Reload、Options、Stop script

*圖 29-12　Tools → Vitesse 選單與工具列（Hull Design、Marine Drafting）。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 說明 |
|---|---|
| Run script | 從檔案瀏覽器執行；腳本名稱自動加入下拉清單。同名腳本出自不同目錄時，加 (1)、(2) 後綴，滑鼠停留顯示完整路徑 |
| Edit／Re-run | 編輯或重跑清單中選取的最近腳本；在清單上按 Delete 鍵移除項目 |
| Debug | 執行預先指定名稱的腳本以啟動除錯器；除錯器須支援 Embedded Python Interpreter（文件舉 Wing 為例） |
| Reload | **清除所有 Python 緩衝**，磁碟上改過的模組下次 import 時重新載入 |
| Options | 僅選單可用 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Vitesse Log 視窗：上方依序記錄腳本、函式、參數與傳回值，下方只列例外，例如 kcs_PageNotFound 與 kcs_DrawingNotCurrent

*圖 29-13　Vitesse Log 視窗：上為完整呼叫紀錄、下為例外清單。（AVEVA 官方文件截圖，僅供內部教學）*

Log 上框記錄腳本啟動、Trigger 執行、Vitesse 函式呼叫（名稱、參數、傳回值、例外）與重新載入；下框只列例外，**雙擊例外可跳到上框中引發它的呼叫**，適合追查長時間執行中的錯誤。腳本內可用 `kcs_ui.message_debug()` 輸出除錯訊息到此視窗。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Vitesse Options 對話方塊：Editor（Notepad、File association、Custom）、Logging options、Debug script name、Number of recent scripts

*圖 29-14　Vitesse Options：編輯器、記錄選項、除錯腳本名稱與最近腳本數量。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 官方明說所有執行記錄都會拖慢效能，特別是 Logging to log file，只在必要時開；Python 的 `print` 也會顯著降低效能。「最近腳本數量」變更後須重啟程式才生效。

### 29.8.4 Batch Vitesse

Drafting 系列程式可用命令列引數加上結束函式 `exit_program()`，在沒有人操作下批次執行腳本。官方範例（DOS BAT）：

```
marhdes -proj=TTP -username=SYSTEM -pass=XXXXXX -mdb=/TTP -appl=planar -script c:\temp\test.py
```

`-appl` 可為：`curved`（曲面建模）、`jig`（Interactive Jig Pillars）、`nesting`（板材排料）、`panelline`（Panel Line Control）、`planar`（平面建模）、`structural`（Structural Design）。腳本結尾必須呼叫 `exit_program()`，控制權才會回到呼叫端。

### 29.8.5 Trigger：三種機制與優先順序

Trigger 是系統事件啟動的 Python 腳本，每個檔案有預先定義的名稱，分為 Pre 與 Post。傳回值決定事件後續：

| 傳回函式 | 效果 |
|---|---|
| `kcs_util.trigger_ok()` | 繼續執行原功能 |
| `kcs_util.trigger_abort()` | 取消觸發它的功能 |
| `kcs_util.trigger_override()` | 以腳本取代原功能（僅部分 Pre-Trigger 允許） |

| 機制 | 說明 |
|---|---|
| Vitesse Trigger 檔 | 放在 `SBB_TRIGDIR`；標準功能也用同一批檔案，**使用者可加碼但不可破壞既有實作**，建議只加一行呼叫自己模組的程式 |
| **PML Trigger** | 用來取代舊 Vitesse Trigger；名稱為去掉底線並加 `pre` 或 `post` 後綴，如 `trig_draft_init.py` 對應 `trigdraftinitpre.pmlfnc`、`trigdraftinitpost.pmlfnc`；放在 PMLLIB 內，傳回字串 `'OK'`、`'ABORT'` 或 `'OVERRIDE'` |
| 動態註冊 | `kcs_util.register_trigger(name, type, function)`、`unregister_trigger(...)`、`get_registered_triggers()`；type 為 `kcs_util.kcsPRE_TRIGGER` 或 `kcsPOST_TRIGGER`。只能註冊除傳回碼外不傳回額外值的 Trigger；建議在應用程式啟動時註冊、結束前取消 |

**優先順序：只要找到對應的 PML Trigger，就取代同名 Vitesse Trigger（後者不再被考慮）。** 開發 PML Trigger 後要執行 `pml rehash` 更新 PMLLIB 的 `pml.index` 並重啟相關模組。參數型別不是基本型別（string、integer、real）的 Vitesse Trigger——例如 `trig_draft_property_edit` 帶有 `Model` 物件參數——**無法**以 PML Trigger 取代。

文件列出的 Trigger 範圍（節錄）：

| 範圍 | Trigger 名稱 | 事件 |
|---|---|---|
| Drafting | `trig_draft_init` | 每次 Drafting 系列程式啟動（Post 內可使用 `kcs_gui`） |
| | `trig_draft_dwg_new`／`_open`／`_close`／`_save`／`_save_as`／`_print` | File 選單的新增、開啟、關閉、儲存、另存、列印 |
| | `trig_draft_insert_model`、`trig_draft_model_info`、`trig_draft_dwg_verify` | Insert／Model、Tools／Inquiry／Model、Tools／Inquiry／Verify |
| | `trig_draft_insert_model_filter` | Insert/Model 對話方塊按 Filter |
| Hull 平面建模 | `trig_hull_ppan_store` | 板架儲存（Pre 回 override 則不儲存） |

官方給了一個 PML Trigger 範例 `trighullppanstorepost(!panelName is STRING) is STRING`：儲存板架後讀 `STVVAL` 狀態屬性，依結果回傳 'OK' 或 'ABORT'（範例中的 `!!MyGetPanel`、`!!MyStatMgr` 是文件自訂物件，非內建）。

範例檔 `kcs_ex_trig01.py` 可用來觀察 Trigger 的輸入參數與傳回值：複製成 Trigger 名稱（如 `trig_draft_dwg_new.py`）即可啟用，範例位於 `\Vitesse\Trigger` 而非 `\Vitesse\Examples`。

> **專業提醒：** Trigger 在使用者不知情時執行。攔截（`abort`）前務必用 `message_confirm` 說明原因；Pre-Trigger 出錯可能讓 File／New 等基本功能失效，先在訓練專案驗證並保留原始檔。

### 29.8.6 Utility、UI 與 Data Extraction 介面

這三個模組以 `import` 載入，並以例外機制回報錯誤（用 `try ... except`，錯誤類型看 `kcs_util.error`）：

| 模組 | 用途 | 代表函式 |
|---|---|---|
| `kcs_util` | 使用者回應比對、Trigger 傳回碼、環境變數、座標轉換 | `ok()`、`cancel()`、`quit()`、`yes()`、`no()`、`TB_environment_get/set`、`coord_to_pos`、`pos_to_coord`、`tra_coord_ship`、`tra_coord_pan`、`run_pdms_command(cmd)` |
| `kcs_ui` | 簡單互動 | `int_req`、`string_req`、`point2D_req`、`point3D_req`、`answer_req`、`message_confirm`、`message_debug`、`choice_select`、`string_select`、`model_info` 等 |
| `kcs_dex` | 資料抽取（唯讀） | `extract`、`next_result`、`get_int`、`get_real`、`get_string`、`get_reavec3d`、`get_box` 等 |

使用要點：

- UI 函式回傳 `[0]` 為 User Response，要與 `kcs_util.ok()` 等比對；**`ok()` 不要拿去和 `answer_req` 的結果比**。
- 訊息文字上限 512 字元、標題 132 字元。
- `TB_environment_set` 只改目前處理程序，**設定資料庫路徑的變數不會生效**。
- `run_pdms_command(cmd)` 傳回大於 0 為成功、小於 0 為失敗。

## 29.9 Vitesse 的船體與圖面介面（官方規格總覽）

| 模組 | 範圍 | 文件要點 |
|---|---|---|
| `kcs_draft` | Drafting：新增圖面、文字、幾何、符號、元件、視圖、亮顯、子圖等十餘類函式 | `CommonSample.py` 提供可重用函式，如 `SelectView`、`SelectComponent`、`SubpictureInsert`、`Point2DLockReq` |
| `kcs_hullpan` | 平面板架：`pan_init`、`stmt_exec`、`pan_store`、`pan_skip`，另有複製、移動、分割等 | 核心做法是**把板架輸入語句字串逐句交給 `stmt_exec`**，再 `pan_store` 儲存 |
| `kcs_chm` | 曲面船體 | `run_XML(XmlFileName, LogFileName)` 用 XML 建立曲面物件（語言同 Batch Curved Hull），`output_XML` 反向輸出；XML 可用 PyXML 建立 |
| `kcs_weld` | 焊接規劃 | `weld_calculation(assembly_name, recursive)`、`weld_properties_get/set`、`weld_delete` |
| `kcs_modelstruct` | 船體區塊 | `block_new(name, MinPt3d, MaxPt3d)`、`block_delete(name)`；名稱最長 25 字元 |

**客製化掛鉤（Hook）：** 船體提供固定名稱的 Vitesse 腳本讓客戶擴充。

| 掛鉤 | 用途與規格 |
|---|---|
| `_TBhookCustHole` | 客製參數化開孔（如範例 `FH<par1>*<par2>`、`HOS<par1>*<par2>*<par3>*<par4>`）。必須實作 `getHoleName`、`getHoleSegment`、`setHoleContour`（最多 8 個參數），傳回碼 0 OK、1 孔型不明、2 參數個數錯、3 參數不合理、4 無法產生幾何；腳本須放在 `PYTHONPATH` 指到的目錄，使用者介面圖面為 `__SBH_HOLE_MENU__` |
| `_TBhook_Formula.py` | 圖面表單的 `$` 規則：使用者自訂規則編號 10000 至 10999；5000 至 5999 為官方預定用途、由使用者實作；腳本收到模型脈絡與規則編號，傳回文字 |

官方標註：**Geometry Macro Facility（幾何巨集）與表單中的 User Defined Simple Rules 僅供參考，不應由客戶新用**；Geometry Macro 做 Drafting 圖面已不支援，應改用 Vitesse Drafting 函式。

> **專業提醒：** 官方 Development and Migration Guidelines 的建議非常實用：**把 Vitesse 呼叫包進自己的模組**。介面日後有函式被淘汰時只改一處；也能在包裝層統一加日誌（例如把所有 `message_confirm` 訊息寫進檔案）。Trigger 檔同理，只放一行呼叫。

## 29.10 Data Extraction：語法與環境

取值三步驟與 Python 範例見[第 15 章](ch15_hull_vitesse_zh-TW.reading.html)；這裡補官方的語法規格。資料抽取有三種使用方式：查詢程式 `SX700`（命令列互動）、Vitesse（`kcs_dex`）、Geometry Macro 語言（`EXTRACTION` 敘述搭配 `GET/EXTRACT` 或 `GET/RANGE`，官方不建議）。

### 29.10.1 語法規則

| 項目 | 規則 |
|---|---|
| Keyword 階層 | 以 `.` 分隔；第一層通常是應用程式（如 `HULL`），第二層是物件，其後決定物件內的項目；可縮寫到唯一為止 |
| `HELP` | 可替代任何 keyword，結果為「此處可用的 keyword 清單」，例如 `HULL.HELP` |
| 引數 | 一律用括號；字串用單引號、整數或實數直接寫 |
| 運算子 | `*` 萬用字元（僅字串，如 `('PUMP'*)`）、`:` 區間（如 `(1:5)`、`('A':'C'*)`）、`,` 重複（如 `(1,5)`），可組合 |
| 換行 | 超過 80 字元用連字號 `-` 續行 |
| 結果型別 | `s` 字串、`i` 整數、`r` 實數（雙精度）、`3r` 三實數向量；Keywords 表的 OUTPUT 欄註明，多值以倍數表示 |
| 單位 | 除非特別註明，長度 mm、面積 mm²、重量 kg |

官方的 Vitesse 範例用萬用字元加總區塊重量：`HULL.BLOCK('<區塊名>').PANEL(*).WEIGHT`，以迴圈 `next_result()` 取回每塊板架的重量（型別 2 即實數）後加總。

### 29.10.2 資料庫來源後綴

`VOLUME` 與 `DRAWING` 可在名稱後加 `@` 指定來源資料庫；未指定時，Volume 預設 `SBD_VOLUME`、Drawing 預設 `SB_PDB`。

| 物件 | 來源 | 可用寫法（等價） |
|---|---|---|
| `VOLUME` | 專案體積 `SBD_VOLUME`／元件體積 `SBE_GENVOLDB` | 邏輯名、說明文字（"Project volume"、"Component volume"）、整數 1／2 |
| `DRAWING` | 一般圖面 `SB_PDB`、子圖 `SBD_PICT` 等 | 邏輯名、說明文字（如 "General Drawing"）、整數（1 為 `SB_PDB`、3 為 `SBD_PICT`） |

例：`VOLUME('XYZ@SBE_GENVOLDB'*).NAME` 與 `VOLUME('XYZ@2'*).NAME` 等價。**使用區間時，資料庫類型只寫在下限，上限的類型會被忽略。**

### 29.10.3 執行環境

| 變數 | 說明 |
|---|---|
| `SB_PDB`、`SB_OGDB`、`SB_PLDB` | 圖面資料庫、船體資料庫、船體板資料庫；只需指定該次抽取用到者 |
| `SB_PROJECT` | 預設專案；未定義則須在抽取指令中指定專案 |
| `SB_CUSTOMER`、`SB_LANGUAGE` | 預設客戶、預設語言（僅用於元件與設備，未定義為 1） |
| `SBD_ALIAS` | 別名檔（僅圖面） |
| `SB_SREF` | 船體結構參考物件（僅船體抽取） |

> **專業提醒：** 在 Vitesse 以外的環境跑抽取失敗，最常見原因是環境變數未設，先檢查 `SB_PROJECT` 與所需資料庫路徑。

## 29.11 Keywords：Drafting、Hull 與 TDM

Keywords 的完整清單**不在網頁正文**，而是附在各頁的 Excel 表（`Datext_*.xls`、`DatExt_*.xls`）。開發者要寫抽取語句時，應該先取得這些表。

| 領域 | 範圍與表格 |
|---|---|
| **Drafting** | Volume 的通用 keywords（`Datext_Volume.xls`）、Drawing 圖面上所有物件的詳細資訊（`Datext_Drawing.xls`） |
| **Hull** | 以 `HULL` 存取：總覽與曲面、Blocks（區塊所參照的板架，含區塊層級資訊）、Curved Panels、Shell Profiles（可用名稱 `PART` 或在主軸某座標的平面選取，x 座標可用框架項如 `FRA('FR107+100')`）、Panels（板、托板、疊板、加強材、翼板、支柱、邊界；座標為板架局部座標）、Boundary／Plate／Bracket／Doubling／Stiffener／Flange／Pillar／Bead／Hole／Notch／Cutout／Seams／TAP、Plates／Curves（局部 uv 座標，可用變換矩陣換成船體 xyz）、Nested Profiles／Plates、Raw Plates（母板只有名稱與使用量）、Assembly Plates |
| **TDM（資料管理）** | 自各物件取得一般 TDM 資訊（`Datext_TDM.xls`），也可能適用於其他物件 |

官方警語：**現有 keywords 並未涵蓋所有物件的所有資料項目。** 找不到想要的欄位時，不代表資料不存在，也可能是 keyword 未開放；這時改走 marAPI（[第 14 章](ch14_dotnet_zh-TW.reading.html)與[第 15 章](ch15_hull_vitesse_zh-TW.reading.html)）或其他途徑。

## 29.12 Python 與 .NET 的連結

Marine .NET API 見 `NETmarAPI.chm`。各 Vitesse 介面在各應用程式的可用性列於附件 `vitesse_access.xls`。

## 29.13 二次開發者怎麼接：決策表

| 需求 | 建議路徑 | 依據與提醒 |
|---|---|---|
| 材料表、規格、零件清單送採購系統 | 優先評估官方 ERM–Design Integration；客製部分以 PML Function 調整來源表 | 29.4.4；ERM 端另有版本與授權需求〔待核對〕 |
| 非 ERM 的 ERP | 第 16 章的檔案或中介表架構 | 官方整合僅針對 AVEVA ERM |
| 在使用者操作前後攔截（儲存板架、開新圖） | 新做用 PML Trigger；舊 Vitesse Trigger 逐步包裝與遷移 | 29.8.5；帶 `Model` 物件參數者只能維持 Vitesse |
| 批次產生船體曲面或板架 | Batch Vitesse（`marhdes ... -script`）或 `kcs_chm.run_XML` | 屬第 15 章的紅區（會改模型），先在訓練專案 |
| 唯讀取船體資料 | Data Extraction（`kcs_dex` 或 marAPI） | 29.10；先查 `DatExt_*.xls` |
| 輸出給 AutoCAD／MicroStation | ExPLANT-A／-I | 29.7；成品是幾何，屬性需另設文字檔 |
| 讀寫外部資料庫 | Query／ODBC，或 .NET | 29.7 專業提醒 |

## 29.14 本章小結

1. **ERM–Design 整合靠通知機制**：Update／Acknowledgement／Error，加上 `PublishingStatus` 與 External Reference Id（`dabaconid`），確保資料不重送、對得起來。
2. 來源資料由 **DB View 或 PML Function** 供應；PML Function 需 ERM 設為 PML Safe mode，管路與螺栓零件清單只能走 PML 函式。
3. 材料交換的關鍵是 **ERM Material Type 對應**；Read／Write Attributes 是可客製的 PML 掛鉤。
4. 刪除要**對方核准**（CanDeleteRequest 流程），非擁有者不能刪。
5. 其他介面（NET、Bocad、ExPLANT、ImPLANT、Query）各是獨立手冊，先找對文件再進細節。
6. **Developer's Toolkit 在 12.1 僅 legacy 支援**：Vitesse 與 Data Extraction 只維護、不新增。
7. Trigger 有三種機制，**PML Trigger 找到就取代同名 Vitesse Trigger**；使用者只能加碼，不可破壞標準實作。
8. Data Extraction 的語法簡單但 **keywords 清單在 Excel 表**，且並未涵蓋所有資料。

## 29.15 練習題與自我檢核

練習只能在訓練專案進行。

1. 在 Hull Design 找到 View → Addins → AVEVA ERM Integration，列出三個選項，並說明為何不要在正式專案直接按 Publish。
2. 依圖 29-2 的五步流程，標出你們若自訂 PML Function，會影響哪一個步驟。
3. 在 Vitesse 選單開啟 Log window，故意在 `kcs_ui.point2D_req` 前不開啟圖面，觀察 `kcs_DrawingNotCurrent` 如何顯示在下框。
4. 寫出 `HULL.BLOCK('X').PANEL(*).WEIGHT` 各段意義，並指出 `*` 的限制（僅字串引數）。
5. 判斷：舊 Vitesse Trigger `trig_draft_property_edit` 能否改寫成 PML Trigger？為什麼？

**自我檢核**

- [ ] 我能畫出 Marine 與 ERM 之間的通知流程，並說出三種通知。
- [ ] 我知道 PML Safe mode 與 Non PML Safe mode 對應 DB View 或 PML Function 的哪一種。
- [ ] 我能說明 Trigger 三種機制的優先順序。

## 29.16 〔待核對〕彙整

1. 各整合概念的 PML Function／DB View 回傳欄位與格式：文件只列名稱，須在公司版本取預設函式實測。
2. Vitesse 執行階段 Python 版本：Installation 頁寫 2.4.2，第 15 章為 2.6，須實測。
3. 虛擬屬性（ERM 即時資料）的 PML 屬性名稱與是否可用於 `COLLECTION` 篩選。
4. 客製托板與缺口掛鉤（文件另有專章）、Actual Material Usage 發佈、Hull Material Control 中的 Assembly Planning 整合：本章僅概述，未逐頁讀。
5. `NETmarAPI.chm` 與 Vitesse 的 `vitesse_access.xls` 內容：為附件，本章未讀。
6. 各 `Datext_*.xls`／`DatExt_*.xls` 的 keywords 清單：為附件，未讀。
7. ERM 端版本與授權、AVEVA Integration Service 安裝與 s14001／s14002 等畫面的完整設定：屬 ERM 文件範圍。
8. Pipe Stress、ImPLANT、ExPLANT、NET Gateway 的操作細節：僅讀了簡介頁。

## 資料來源

AVEVA Marine 12.1 官方離線文件：*Interfaces*（頁面 1105749，含 ERM–Design Integration、Catalogue Manager、Standard Material、Raw Plates／Profile、Hull Material Control、Deletion、NET Gateway、Bocad、Design in Context、ExPLANT、ImPLANT、Query 等）與 *Legacy Applications*（頁面 1105751，含 Developer's Toolkit、Vitesse、Data Extraction、Drafting／Hull／TDM Keywords）。圖片為官方文件截圖，僅供內部教學。
