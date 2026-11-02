# 第 47 章　12.1 版本說明與升級：Release Bulletin、設定需求與功能變更

> [第 20 章](ch20_system_administration_zh-TW.reading.html)講了升級的基本觀念（Part Upgrade、all-or-nothing、升級後不能 Backtrack）。這一章換成**規劃者與維運者的視角**：手上拿到一份 12.1 的版本公告（Release Bulletin），要怎麼讀它、從中抽出「會影響我們專案的變更」、排出升級順序，並在升級前後知道該檢查什麼。
>
> 官方文件裡名為「Hull and Outfitting」的那一大塊，其實不是操作手冊，而是 **AVEVA Hull and Outfitting 12.1／12.1.SP5 的 User Bulletin**（約 587 個子頁）。它的價值在於：每個功能都標了哪一個 Service Pack 加進來，也標了相容性限制。本章把它整理成「版本差異與升級風險」表。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件：*Hull and Outfitting*（Release Bulletin，12.1.SP5 版）、*What's New in AVEVA Marine?*、*Welcome to the AVEVA Marine Documentation*、*Terminology*、*Abbreviations in the User Documentation*。**公告本身是 SP5 時期的舊文件，部分內容為 12.0 或更早版本遺留（例如 Windows XP、IE 7/8、.NET 3.5 的敘述），與 SP5 的需求表互相矛盾處，本章標〔待核對〕。**官方沒有給「升級耗時」「硬體規格數字」，本章不編造。「升級檢查清單」中，標〔官方〕者來自公告，標〔一般實務〕者是常見 IT 維運做法，不代表 AVEVA 的要求。完整的 12.0→12.1 步驟在另一份官方《12.0 to 12.1 Upgrade》手冊，不在本文件範圍。

## 47.1 學習目標

讀完本章，你應該能夠：

1. 說明 Release Bulletin 的結構，並用 SP2／SP3／SP4／SP5 標記判斷某個功能是哪一版加入的。
2. 說明 12.1 安裝的幾個重點：MSI 靜默安裝、ALS 授權、不可有空白字元的安裝路徑、修復版本（fix release）的套用方式。
3. 說明「升級號碼」（upgrade number）、Database Version Control 與唯讀開啟的關係，並讀懂 R/W、R、X 矩陣。
4. 區分強制升級與 Optional Upgrade（12010301、12010401），並說明套用後的相容性代價。
5. 依官方 16 步驟寫出升級流程，並說明 Extract、Working Extract、Offline Location 的處理方式。
6. 說明 Unicode 與度量單位（Units of Measure）兩項「資料表示法」變更，對舊資料與自訂 PML 的影響。
7. 列出 SP5 的作業環境需求，並辨認公告內互相矛盾的舊敘述。
8. 說明資料庫層的主要新增：ENGI、Design Reference DB、DBRange、Database Views、Distributed Attributes、Dabacon buffer。
9. 依領域（Hull、Outfitting、Draft、Catalogue、Global…）查出 12.1 的變更，並判斷哪些屬於「行為改變」而非單純新功能。
10. 產出一份升級前後的檢查清單，並說明哪些項目要先在測試專案驗證。

## 47.2 版本公告怎麼讀

### 47.2.1 這份文件是什麼

| 項目 | 內容（來源：About 各頁） |
|---|---|
| 對象 | AVEVA Hull and Outfitting 12.1，是 12.0 的「重大更新」（major update） |
| 12.1.SP5 | 完整版本（full release），取代 12.1.SP4 與其後所有部分修復版本；包含 SP4 修復版本中的錯誤修正，以及早期採用者與 AVEVA 測試計畫發現的問題 |
| 主要讀者 | 從 12.0 升級的使用者；更早版本的使用者還要讀 12.0 的 User Bulletin（最好是 SP6 版） |
| 涵蓋產品 | 同一張 DVD-R 上的相關產品，分成 Engineer、Design、Manage 三個家族 |
| SP5 新增標記 | 內文以 `*12.1.SP5*` 標示 SP5 才引進的重大變更 |

*What's New in AVEVA Marine?* 這頁只有一段話：Release Notes 說明新功能、期望、限制、已知問題與已修復問題，**放在 AVEVA Knowledge & Support Center 的 Product Hub**（softwaresupport.aveva.com），離線文件裡沒有。換句話說，離線文件中的「公告」不等於當前最新的發行說明，升級前仍要去官方站查最新版。*Welcome* 頁則一句話定位 AVEVA Marine：從早期計算到控制製造機器人的一體化船體與舾裝設計與生產方案，資料來自「唯一且拓樸相連的 3D 模型」，並與其他 AVEVA 工程與設計方案保持相容。

> 〔公開版未收錄：AVEVA 官方產品截圖〕12 系列使用者文件的線上說明索引：AVEVA Marine 下分 Design、Engineer、Manage、Read Me First

*圖 47-1　12 系列使用者文件的索引頁。Hull、Outfitting、Administration、Assembly Planning、Space Management、Surface Manager、Weld Planning 等各有獨立的使用者指南。（AVEVA 官方文件截圖，僅供內部教學）*

12.1 的文件改動：全部手冊更新、新增《12.0 to 12.1 Upgrade》手冊與 Design Reuse、Space Management、Surface Manager、Report Designer、Tags、Isometric ADP 等新手冊；PDF 手冊不再單獨提供。

### 47.2.2 版本標記速查

| 標記 | 意義 | 讀法 |
|---|---|---|
| 無標記 | 12.1 初版（或 SP1）引進 | 從 12.0 升上來都會遇到 |
| `12.1.SP2` | SP2 引進 | 從 SP2 以前升上來才有 |
| `12.1.SP3` | SP3 引進 | 常伴隨 Optional Upgrade 12010301 |
| `12.1.SP4` | SP4 引進 | 常伴隨 Optional Upgrade 12010401 |
| `12.1.SP5` | SP5 引進 | 含 Administration 1.5、入口與 ERM 整合等 |

每一則功能說明的固定格式是：Description、Benefits、**Compatibility Constraints**、For More Information、Affected Programs。**規劃升級時最先掃的是 Compatibility Constraints 與 Affected Programs**，這兩欄告訴你有沒有行為改變、會波及哪些程式。

> **專業提醒：** 「Compatibility Constraints：None」只代表「該功能本身沒有相容性問題」，不代表升級對你的自訂 PML、報表或批次工具沒有影響。公告多次寫「僅在此註記」（Only noted here），這類功能的細節要自己在測試專案驗證。

## 47.3 軟體發行與安裝

### 47.3.1 官方的安裝重點

| 主題 | 公告內容 | 對維運的意義 |
|---|---|---|
| 媒體 | 12.1.SP5 以 DVD-R 發行，用標準 Microsoft 安裝程序自行安裝 | 完整套件通常裝在各 PC，授權伺服器與授權檔裝在網路 Windows 伺服器 |
| 授權 | 需要 **AVEVA Licensing System（ALS）**與適當授權，**不能用 FlexMan**；ALS 支援虛擬環境，並利於 Citrix 支援；ALS **不在產品 DVD 上**，要從 AVEVA 網站下載 | 升級前先確認授權伺服器版本與授權檔 |
| 安裝技術 | 標準 MSI，可用標準 MSI 方式靜默安裝，通常由 `setup.exe` 觸發 | 可用於大量部署 |
| 安裝程式數量 | 比以前少，每個 AVEVA「release」一個；Hull & Outfitting／Marine 安裝程式含多數相關產品的選項 | 部分產品仍用獨立安裝程式 |
| Global | 安裝程式含 Global client 選項；**Global server 另有安裝程式**，通常裝在另一台不一定有 Hull and Outfitting 的伺服器 | 規劃時 client 與 server 要分開排程 |
| 捷徑 | 可選擇在桌面或開始功能表裝批次檔與捷徑，並可自動設定 pml index | |
| 瘦客戶端 | **不再支援** thin client 安裝 | 以 Citrix 等方式部署時要另行評估〔待核對〕 |
| 變更／修復／移除 | 一律從「控制台的新增或移除程式」進行，會視需要要求原始 DVD | 確保裝的是 AVEVA 測試過的一致產品組合 |
| 修復版本（Fix release） | 用標準更新流程，會檢查並在必要時「修復」既有安裝；可從新增或移除程式移除；**套用到一起安裝的所有產品，不是個別產品**；建議用最新的修復版本（包含先前所有修復） | 不要只對單一產品打補丁 |
| 路徑限制 | 可改安裝路徑，但**路徑中不可含有空白字元的資料夾** | 不要裝在 `C:\Program Files\…`〔見下方 Global 例外說明〕 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕AVEVA Marine Setup 的 Custom Setup 畫面：AVEVA Marine Suite 12.1.SP5 下可選 Hull and Outfitting、Global Client、Area Based ADP、Schematic 3D Integrator 等功能，預設安裝位置為 AVEVA 資料夾下的 Marine 目錄

*圖 47-2　Marine 安裝程式的功能樹。路徑範例為 `C:\AVEVA\Marine\OH12.1.SP5\`，不含空白。（AVEVA 官方文件截圖，僅供內部教學）*

### 47.3.2 空白路徑與 Cache Service

- **專案路徑含空白**：12.1 **不完全支援**專案資料夾路徑有空白，官方說「正在處理，尚無確定日期」。Known Issues 另記載：Global daemon 裝在 `C:\Program Files\` 能運作，但 `REMOTE CHECK` 在 daemon 目錄含空白時無法執行 Standalone DICE（部分原因是分號分隔符）。
- **AVEVA Database Cache Service（SP3 起）**：把讀過的專案資料以高度最佳化的副本存在本機磁碟，對「跨網路重複讀專案資料」有效；必須在執行 AVEVA 應用程式的**客戶端機器**上啟用，同機器的使用者共用；已在本機磁碟的專案不會被快取。Hull Design、Outfitting、Marine Drafting、Outfitting Draft 可使用；**可選用**；需啟用 MSMQ，步驟見《Marine Software Installation Guide》。

### 47.3.3 範例專案（Test Projects）

DVD 提供 `MAR` 範例專案與 `MAS`（Catalogue）專案。`MAR` 的 MDB 包含：`ALL_NO_MDS`、`ALL_WITH_MDS`（專案設定用）以及依角色劃分的 `PLANARHULL`、`CURVEDHULL`、`HULLNESTING`、`INITDES`、`ASSYPLANNING`、`PIPEAFT`、`HVACAFT`、`SCHEMATICS`、`WELDPLANNING`、`PROJADMIN` 等（共約 20 個）。各 MDB 可由系統（FREE）使用者 `SYSTEM/XXXXXX` 進入，也各有專用使用者；專案頂層有 `MARProjectDescription.pdf`、`MASProjectDescription.pdf`，內含團隊與使用者（含密碼）。

> **專業提醒：** 範例專案是做升級演練、驗證自訂工具的最佳沙盒。**專案說明 PDF 內含預設密碼，進入正式環境前務必清除或改密碼。**〔一般實務〕

**常見錯誤：** 把 12.1 裝在 `C:\Program Files` 下、或把專案放在有空白的路徑，結果某些功能（Global 檢查、批次工具）出現難以解釋的失敗。

## 47.4 升級框架：版本控管、Optional Upgrade 與流程

### 47.4.1 Part Upgrade 與升級框架

升級概述的核心概念（第 20 章已介紹，這裡只列公告新增的細節）：

- 12.1 的許多增強需要資料庫升級，每一項個別變更稱為 **Part Upgrade**；多數設計成「可選」，未升級的資料庫軟體仍能用，但**只能唯讀**，部分新功能不可用（graceful degradation）。
- 這讓客戶可以繼續與**外來資料庫（Foreign DB）**共用，例如與 12.0 專案共用的公司層級 Catalogue DB。
- 全部 Part Upgrade 由 **Upgrade Framework** 在 Admin 執行；以 `lock`、`dbupgrade project to latest`、`unlock` 啟動。Global 專案可用，但要額外預防措施。
- **更早的專案要先升級到 12.0。** Schematic Model Manager 有自己的單位處理與升級機制，軟體會提示是否需執行。

框架內的 Part Upgrade 項目（官方清單）：

| 項目 | 說明 |
|---|---|
| UKEY | 現在含資料庫編號以避免重複 |
| 元素尋找效能 | 依 type 建索引 |
| Module Definitions | 新增 TAGS 模組；Drafting 模組更名為 Marine Drafting |
| 字元處理 | 名稱與文字改用 Unicode 表示 |
| HULL FEM Data Model | |
| Compressed HULL Objects | 壓縮的 Hull 物件，同時新增 Hull object type 索引 |
| Name Sequence 起始值 | |
| Assembly POS 屬性 | |
| Draft 線寬 | 細、中、粗線寬改存於系統資料庫 |

升級工具會在資料庫放一個**升級編號**，用於開啟時偵測是否已升級，也供 Reconfigure 使用。框架外還有「非框架升級」：彼此獨立、可任意順序套用，但**無法回溯（backtrack）到升級前的 Session**。

### 47.4.2 Database Version Control

軟體啟動時，會比對資料庫的升級版本與軟體版本，限制最大開啟模式：

| 軟體版本＼資料庫升級版本 | 12.1 前 | 12.1.1 | 未來（如 12.2） |
|---|---|---|---|
| 12.1 前 | R/W | X | X |
| 12.1.1 | R | R/W | X |
| 未來（如 12.2） | R | R | R/W |

R/W＝可讀寫，R＝唯讀，X＝無法存取。**但 12.1 之前的版本不做這個檢查，所以偵測不到已升級到 12.1 的資料庫**——舊版軟體仍可能去開、去寫，這是官方明文警告的「版本混用風險」。

> 〔公開版未收錄：AVEVA 官方產品截圖〕警告視窗：有資料庫的升級編號與此軟體（12010103）不符，有 2 個資料庫未升級，將以唯讀開啟

*圖 47-3　從尚未升級的專案開啟 MDB 時的警告。官方說明這代表專案需要升級到最新版本才能取得寫入權限。（AVEVA 官方文件截圖，僅供內部教學）*

### 47.4.3 Optional Upgrade（SP3、SP4）

| 升級等級 | 版本 | 內容 | 相容性代價 |
|---|---|---|---|
| 12010301 | 12.1.SP3 | 2893：儲存 space arrangement 定義；2931：GENPRI 下儲存座標系實體（STEP 匯入）；38541：PADD 的 marine drawing type 表屬性；15251：PADD 舾裝模型的新 Layers 與 ID；45823：新的 Marine drawing types（ADP） | 套用後**不再相容 12.1.SP2 或更早版本** |
| 12010401 | 12.1.SP4 | 僅一項：93792，一般資料庫變更 | 同一專案混用 SP4 與舊版會造成資料庫不一致；套用後資料庫**不會被 SP4 之前的任何版本更新**（官方「強烈建議但非強制」） |

- 套用方式：`DBUP PROJECT TO LATEST OPTIONAL`；`Q UPGRADE LIST` 會對可選的升級給簡短提示（例如 `12010301 ... Optional upgrade version`）。
- **套用時機**：由系統管理員在「專案中所有使用者都已在跑該 SP」時才套用。
- **SP2 與 SP3 並行**：只有在 SP2 使用者都裝了特定 hotfix（官方說稍後公布）、且**沒有**套用 SP3 的 Optional Upgrade 時，兩個版本才能共用同一專案資料庫。
- **Global Server**：Global Server 12.1SP2 支援 Marine 12.1SP3，但僅限**尚未套用** Optional Upgrade 的專案；Global Server 12.1SP3 隨 Marine 12.1SP3 hotfix 1 發行，不論有沒有套用都可使用。

> **專業提醒：** Optional Upgrade 的好處是「可選擇何時不相容」。**最穩的做法是：全員升到同一 SP、穩定一段時間後，才套用 Optional Upgrade；一旦套用，視為單向門。**〔一般實務，依官方「套用後不相容舊版」推論〕

### 47.4.4 升級流程（官方順序）

升級由負責各地點的系統管理員執行；一次只升級一個專案，多專案要協調順序；升級期間專案須鎖定、所有使用者離線。

| 步驟 | 動作 | 備註 |
|---|---|---|
| 1 | 確認所有使用者已離開專案 | |
| 2 | 在**所有地點**鎖定專案（升級會檢查） | 專案整體不能鎖，只能鎖各地點；可從 HUB 用 `LOCK AT <location>` 鎖所有線上地點；`QUERY LOCK AT <location>` 確認 |
| 3 | 必要時停用自動更新事件 | 建議但非必要 |
| 4 | Expunge 本地系統所有使用者 | |
| 5 | 清空 Working Extract 的資料 | 這些不被考慮；Global 專案中應刪除 |
| 6 | 用 **DICE** 檢查專案 | 有問題先處理再重跑；處理期間可解鎖，但最後一次 DICE 前要再排除所有使用者並鎖定 |
| 7 | 備份所有地點的專案 | |
| 8 | 暫時把所有非外部（non-Foreign）DB 遷到其主要（master）的 Primary 地點 | |
| 9 | 確認沒有 Transient Databases | |
| 10 | 在每個地點升級專案 | |
| 11 | （可選）合併 Sessions | |
| 12 | （可選）為 Unicode 重新設定（Reconfigure） | |
| 13 | 再做一次 DICE | |
| 14 | 把 Extract 遷回原地點 | |
| 15 | 若適用，執行非框架升級 | |
| 16 | 解鎖專案 | |

升級的核心限制：**每個資料庫必須整體處於「已升級」或「未升級」其中之一**，所以任何資料庫的所有 Extract 都必須在升級期間處理；整個專案（Foreign DB 除外）應一次升完。

### 47.4.5 Extract 與 Offline Location

| 情況 | 官方要求 |
|---|---|
| 一般 Extract 階層 | 不需要改階層、也不需要在 Extract 之間 `FLUSH`／`ISSUE`／`DROP`，也不必刪除 Extract family 只留 Master；但所有 Extract 都要**遷到單一地點**（不必是 HUB） |
| Working Extract | 因為只屬於單一地點、無法傳播，所有資料**必須 flush**，並把 claim 釋放給父層；只有 Working Extract 有此要求 |
| Offline Location | Global 支援 Offline 地點，HUB 不一定有連線；Offline 地點不支援分散式 Extract（可支援獨立 Extract family），**無法從別的地點協調升級**，要各自獨立處理 |

### 47.4.6 Unicode 與度量單位：兩項「資料表示法」變更

**Unicode：**
- 12.1 新建資料庫，名稱與文字屬性預設用 Unicode；**舊資料庫不強制升級**，依專案字元集（Admin 的 `PROJECT CHARSET`／`PROJECT MBCHARSET`）處理，Reconfigure 時也依此轉換，所以這個設定必須正確。
- 需要擴充字元範圍時，可用 Reconfigure 把「舊版（legacy）」資料庫轉成 Unicode 編碼。官方範例（Lexicon 的 DICT 資料庫）流程：`FROM DB MASTER/DICT` → `TO FILE ...` → `RCFCOPY ALL` → `RECONFIG SESSIONS` → `FROM FILE ...` → `TO DB MASTER/DICT` → `RECONFIG`。FROM 階段用 `RECONFIG SESSIONS` 可保留 Session 與參考，不必刪除重建 DB、也不必重新加入 MDB。
- 內部字串格式為 UTF-8；循序文字檔預設以**含 BOM 的 UTF-8** 讀寫，另附命令列 transcoder。PML 字串都支援 Unicode，PML 語言檔建議用含 BOM 的 UTF-8 或純 ASCII；檔名建議用 ASCII（DXF、DGN 輸出與 PML Publisher 有問題）。
- 相容性：舊版（legacy）資料庫可被 12.1 與更早版本**讀**，也可被 12.1 與非 Unicode 版本寫（字元範圍受專案設定限制）；**Unicode 編碼的資料庫，12.1 以前的版本不能開（讀寫皆不行）**。
- 限制：只處理由左至右的語言（不含阿拉伯文、希伯來文）；繪圖輸出只能用 Admin 設定的 TrueType 字型（預設 font 5＝Arial Unicode MS），無法產生 plotfile。**Hull Design 建立的物件名稱即使在 Unicode 專案中，仍只能用大寫 A–Z、數字與 `- . _ +`。**

**度量單位（Units of Measure）：**
- 12.1 內建大量單位與換算（壓力、質量、溫度、角度、能量等），多數實數屬性有預設儲存單位（通常 SI）；新的 `UNITS` 指令（例如 `UNITS MM DISTANCE`、`UNITS POUND MASS`），指令列行為有改變，**自訂的 PML 應用程式要重新檢查**，並可由 .NET Units 介面使用。
- 距離與口徑（bore）沿用舊方式，不需轉換；其他屬性**首次設定 UNIT 欄位**。以前它們是「憑慣例」存的無單位數值，不同應用程式、不同專案可能不同。相容作法是把該維度設為 `NUMERIC`，等於停用該維度的單位換算（也就得不到新功能的好處）。
- 部分單位**區分大小寫**（例如 `m`／`M`、`s`／`S`），Imperial 單位與 `MM` 等舊單位除外。
- **升級要做的事**（官方）：標準屬性已設好；客戶要為自己的 UDA、Catalogue／Design 參數與屬性設好維度（例如角度 UDA 要設 `UUNIT` 為 `ANGL`）。依既有資料狀況分四種：資料已存成新資料庫單位 → 只設 `UUNIT`，並可刪除原本記錄單位的 UDA 與自製換算 appware；資料存成同一個非新單位 → 以 `UNITS NUMERIC <維度>` 輸出 datal，再在設好目前單位（如 `UNITS DEGF TEMPERATURE`）後讀回；混合單位且有 UDA 記錄單位 → 輸出「值＋單位」檔、檢查格式、讀回；只靠「慣例」的混合單位 → 短期設為 `NUMERIC`，並規劃更嚴謹的單位使用。不必一次改完全部維度。
- Hull 與 Drafting 的單位設定**與 Outfitting 不同**：呈現格式只有 SI（預設）或 Imperial，由環境變數與 default 變數控制。
- Schematic Model Manager 先前專用的單位支援不再需要；升級包含它的 Part Upgrade，且 12.1 以前匯入的 Schematic 資料**必須升級**（進入模組時自動檢查並警告）。CATA 元素 `MSET`、`MTYP`、`ATLI`、`USEC`、`UDEF` 不再使用，日後移除。

> **專業提醒：** 單位變更是「看不到錯誤、數字卻不對」的升級風險。實務上要挑壓力、溫度、質量三類，在測試專案做 12.0 與 12.1 的報表數字對照。〔一般實務〕

**常見錯誤：** (1) `PROJECT CHARSET` 設錯，Reconfigure 時把舊資料轉成亂碼；(2) 把 Unicode 編碼的資料庫放回仍有 12.0 使用者的專案。

## 47.5 設定需求

### 47.5.1 作業環境（Operating Environment，SP5）

| 項目 | 官方內容 |
|---|---|
| 必要作業系統 | Windows 7 Professional／Enterprise + SP1、Windows Server 2008 R2 + SP1、Windows 8.1、Windows Server 2012 R2、Windows 10 |
| .NET | Microsoft .NET Framework **4.6.1** |
| 建置作業系統 | Windows Server 2012 R2 |
| 附註 | Windows 7 SP1／Server 2008 R2 SP1 需先裝 Windows Platform Update，才能在 3D canvas 精確繪製 2D（例如文字） |

### 47.5.2 Windows、顯示卡、環境變數

| 主題 | 公告內容 |
|---|---|
| 桌面 | 不再支援 Windows XP Professional；**單一 32 位元版本**，可跑在 32 與 64 位元的受支援 Windows；Windows 7 的 UAC 使需要寫入的檔案必須讓非管理員使用者可存取 |
| Internet Explorer | 線上說明需要 IE；建議 7 或 8（9 當時無法正常運作）〔待核對：SP5 時期此敘述是否仍適用〕 |
| .NET | 另有一段寫 12.1 需要 **.NET Framework 3.5**（隨 DVD，必要時安裝）〔待核對：與 SP5 表的 4.6.1 並存，推測 3.5 為舊版遺留〕 |
| .NET 附加元件 | 部署在網路上的 .NET add-in 可能無法執行；AVEVA 建議每台機器本機安裝；跨網路時 local intranet 預設非 Full Trust，可用 `caspol` 調整 |
| Office | 支援 Office 2007 與 2010；即使在 64 位元 Windows，也建議用 **32 位元 Office（含 Visio）**，因 64 位元版曾遇到問題 |
| 顯示卡 | 不在文件列出支援清單（硬體變動太快），請看 AVEVA Product Support 網站 IT Configuration 的已測試清單 |
| 環境變數 | 專案資料庫資料夾與使用者工作區位置等設定依賴環境變數 |

### 47.5.3 官方文件中提到的環境變數與開關

| 名稱 | 作用 | 版本 |
|---|---|---|
| `PDMSBUF` | 使用者層級設定 Dabacon buffer（MB）；大於 1000 會被忽略 | 12.1 |
| `AVEVA_NOCONSOLE=TRUE` | 隱藏 console 視窗（亦可 `-noconsole` 啟動參數） | SP5 |
| `MARINE_DESIGN_EXPLORER_PLAIN` | 設任何值即關閉 Design Explorer 對 hull 零件的「第二名稱」顯示 | 12.1 |
| `SBH_ENABLE_SOLID_PLATES=YES` | 啟用殼板新的 Generic Primitive 表示（建立速度會變慢） | SP4 |
| `SBH_FREE_SEAMPROF_NAMES` | 自由命名；改由 InitHull 設定，此變數僅作最後手段 | 12.1 |
| `SBH_GRP=Mixed` | 同專案混用 FRP 與 Steel | SP4 |
| `SBH_NO_IND_SYMPARTS` | **已移除**：對稱結構產生的零件一律個別儲存（左右舷各一） | SP2 |

> **專業提醒：** 這張表是「升級時環境變數稽核」的起點：先盤點現行啟動腳本裡設了哪些，再逐一對照有無改義或移除。Marine 的 `SBH_*` 變數是否仍被讀取，要在目標版本驗證。〔一般實務〕

## 47.6 系統與資料庫變更

### 47.6.1 一般系統變更

| 變更 | 說明 | 升級風險 |
|---|---|---|
| ASL（SP4） | 12.0／12.1 開發的 Access platforms, Stairs and Ladders 應用程式**被移除**，由 Vantage Marine 11.6 的 primitive 型能力取代；「Future Considerations」頁另說新應用將改稱 Stairs, Ladders and Handrailing（SLH），平台改用一般 Beams & Columns、Panels & Plates，可搭配 Standard Model Library | 用到 ASL 的專案要規劃替代方式〔待核對：兩頁敘述的先後關係〕 |
| 密碼保護 | 建立沒有密碼的使用者時會跳確認；Generate Script 對話框會檢查專案登入密碼；USER 物件新增 `ConfirmID()` 方法（與 SESSION 物件類似） | 低 |
| Status Control | 新增偽屬性 `STVMOD`／`STVUSE`、`STM COMMENT` 指令、PML2 屬性查詢；**Status Change Event Methods 的第一個引數改為物件陣列**；`StatusProjectHandler`、`StatusData` PML 物件已更新 | **客製的 StatusProjectHandler 要移到新版** |
| 報表 | 新 Reporting add-in（DevExpress XtraReports），可輸出多種格式並送到 AVEVA NET；Design、Paragon、Spooler、Draft、Isodraft 與部分 Engineer 模組可用；舊式 PML 報表改稱 Standard Reporting，**輸出單位會改變**（距離預設 mm，單位轉換 Off 時數值會附單位，例如 `25.4mm`） | 報表輸出格式要重新驗證 |
| GML 效能 | 針對 Mechanical Equipment Interface 匯入資料的繪圖加速 | 低 |

### 47.6.2 資料庫變更

| 變更 | 重點 |
|---|---|
| ENGI 資料庫 | 新型別，存不出現在示意圖上的工程資料；頂層元素為 `SATWLD`；已加入 `modmac.mac` 與 Admin／Global 表單 |
| Design Reference DB | 受限的 Design 資料庫：不可含 SITE 或 HULL 資料、不可為 MDB 預設 DB、僅在建立時設旗標（不可事後取消）；用於存 Systems 與 Areas，適合只有 2D 授權的使用者 |
| 資料庫存取 | Hull & Outfitting 使用者可讀寫 3D 資料庫；要碰 Schematic／Engineering 需 Schematic 3D Integrator 授權；Diagrams 使用者可讀寫 Schematic，只可讀 3D 與 ENGI；Engineering 使用者可讀寫 Schematic 與 ENGI，只可讀 3D；既有 Diagrams、Schematic Model Manager、Schematic 3D Integrator 使用者**需要更新的授權檔** |
| 資料庫數量 | 專案上限提高到 **250,000**；250,001–255,000 與 7,001–8,000 保留給 AVEVA；可建 **DBRange** 元素（`DBRBEG`／`DBREND`，位於 SYSTEM 或 GLOBAL 資料庫 STAT 之下）；`CREATE DB ... UNIQUE` 與偽屬性 `NXTDBU`；編號可用 10,000–250,000 |
| Database Views | 管理者用 Database Views Editor 設定，存於 Lexicon（DICT）的 Database View World（`DBVWWL`）；也可存本機設定檔；用來彙整分散在多個資料庫的元素與屬性，供報表與 Excel 匯入／匯出使用 |
| Distributed Attributes | 屬性群組分散在 DESI 與 ENGI 資料庫（目前僅此兩型），以「binding 元素」綁定；提高並行度、縮小 claim、簡化存取控制（以資料庫歸屬）、減少 Global Extract 需求 |
| UDA／UDET 鍵 | UKEY 現在含資料庫編號，避免合併資料時的名稱衝突；Lexicon 新指令可重新配置既有 UKEY，舊鍵存於 `OLDKEY` |
| `BACKREF`／`CLEANUP`（SP3） | `Q BACKREF` 回答「誰參考我」；`CLEANUP` 清除空參考與無效參考 |
| Extract Control | 對有 Integrator link 的元素 flush／issue／drop 時自動包含連結物件；新參考陣列屬性 `INCFLU`；Extract Control 表單以「R」標示 |
| PBS（SP4） | Project Breakdown Structure：管理者在 Lexicon 於 `PBSWLD`／`PBSTPL` 下定義，供 Engineering 與 Diagrams 的 PBS Explorer 使用 |
| Draft 線寬 | 系統線寬存於系統資料庫，預設 ISO：Thin 0.25 mm、Medium 0.35 mm、Thick 0.70 mm |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Database 表單：Database Type 為 Design，勾選 2D Reference Only 即建立 Design Reference 資料庫；右側有 DB Number 的 Unique 按鈕

*圖 47-4　建立 Design Reference 資料庫的方式：建立時勾選 2D Reference Only（只能在建立時設定）。DB Number 欄位旁的 Unique 按鈕對應 DBRange 的新功能。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Database Views Editor：View Definition Set 區可 Open、Close、New、Delete、Save，下方有 Views 與 View Sets 分頁

*圖 47-5　Database Views Editor。目前在 Lexicon 與 Tags 模組的 Display > Database Views Editor 可使用。（AVEVA 官方文件截圖，僅供內部教學）*

### 47.6.3 Dabacon buffer 與效能

| 項目 | 12.0 | 12.1 |
|---|---|---|
| buffer 範圍 | 32,000–51,200,000 整數（預設 12,800,000，約 50 MB，上限 200 MB） | **20 MB–1 GB** |
| 新專案預設 | | Monitor 20 MB；Admin、Specon、Propcon、Isodraft、Lexicon、DARs、Toolbox 200 MB；Design、Draft、Paragon、Spooler 與 Diagrams、Schematic Model Manager、Tags 500 MB |

設定方法：以 Admin 的 `ED MOD <module> <size>` 修改（可用 MB 或整數，256000 整數＝1 MB）、或初始專案設定的 `modmac.mac`、或使用者環境變數 `PDMSBUF`；`Q DABACON AVAIL` 可查未用量。buffer 大於可用記憶體會增加分頁而抵銷效益。另有 Dabacon index tables 擴充（依 Hull object type code、元素型別、UDET 或 UDA 值加速選取），以及 Hull 物件新的儲存模型（I/O 最多減少 40%，需依升級文件選擇性轉換）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Extract Data Control 表單：Get All Changes、From parent extract only／From all extract ancestors、Update CE、Extract Claimlists、User Claimlists，清單左側以 H、M、R 等字母標示狀態

*圖 47-6　Extract Data Control。12.1 在 Extract 中對含 Integrator link 的元素 flush、issue、drop 時，會自動帶入連結物件並以「R」標示。（AVEVA 官方文件截圖，僅供內部教學）*

**常見錯誤：** 把 buffer 全部設到 1 GB 卻忘了每個模組各自佔用，多開幾個模組後記憶體不足，反而變慢。

## 47.7 使用者介面與管理

### 47.7.1 使用者介面變更

| 變更 | 說明 | 版本 |
|---|---|---|
| 進入系統 | 可直接進入任何模組，不必經 Monitor；登入表單帶對應啟動畫面，並提供桌面與開始功能表捷徑；**登入表單移除「Integrate Engineering and Schematics」選項**，授權功能 `ENGI-DB-RO-ACCESS`、`SCHE-DB-RO-ACCESS` 不再需要 | SP5 |
| Save Work | 現在會顯示表單，可一併「Unclaim All」 | SP5 |
| 儲存與還原視圖 | 3D View 新圖示，儲存目前 drawlist、視圖屬性與縮圖；**舊的編號式視圖不再可用** | 12.1 |
| PML Collection | **範圍為空現在代表 ALL 而不是 NONE**（會慢很多） | 12.1 |
| Attributes Utility | 取代舊的 Query Attributes 與 Attributes 表單，可在權限允許下編輯 | 12.1 |
| Auto-naming | 命名規則可用 PML1 `IFTRUE`；**整個 Format 必須全是 PML1，不可混用 PML2** | 12.1 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕HullDesign login 表單：Project、Username、Password、MDB，以及 Open Read Only 與 Restore Views 兩個選項

*圖 47-7　SP5 的直接登入表單（以 HullDesign 為例）。Options 區有 Open Read Only 與 Restore Views。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 「PML Collection 空範圍變 ALL」和「Auto-naming 不可混用 PML1／PML2」這類不顯眼的行為改變，最容易讓自訂工具在升級後變慢或出錯。要在升級盤點時 `grep` 專案的 PML 找 collection 與命名規則。〔一般實務〕

### 47.7.2 Administration 與 Global 的變更

- **AVEVA Administration 成為獨立產品（SP5）**：Hull and Outfitting 12.1.SP5 不再內建管理功能，改用通用 **Administration 1.5**；因此 AVEVA 決定**終止從 Tribon 移轉資料到 12.1 的能力**，需要的客戶要保留獨立的 12.1.SP4 安裝，再把結果搬到 12.1.SP5 專案（見 47.8.5）。
- 管理 GUI：使用者、團隊可從 Excel 匯入；UDA／USDA 的 Lists of Values 可設「Optional」（PML 方法 `LIMITSVALIDOPTIONAL`）。
- **Global**：支援 Linked Documents 傳播（預設關閉，Admin Project 選單開啟；`GLINKP` 屬性；`SYNCHR <dbname> LINKDOC FORCE` 可強制）；**Database Distribution 表單**（Data 選單）以矩陣顯示各資料庫在各地點的狀態（`+` primary、`-` 配置於此但 primary 在他處、`>` 轉移中、`*` foreign）並可批次改 primary 地點；DB Sessions 表單顯示 Session 的「Reason」。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Admin 的 Data 選單：Database Distribution 項目位於 Database Allocation 與 Update 之間

*圖 47-8　Admin 的 Data 選單中的 Database Distribution…。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕DB Sessions 視窗：左側資料庫清單，右側顯示 Session Number、Author、Date、Reason（savework）與 Comment

*圖 47-9　DB Sessions 現在會顯示建立 Session 的原因（Reason）。（AVEVA 官方文件截圖，僅供內部教學）*

### 47.7.3 Global 相容性重點

| 項目 | 說明 |
|---|---|
| Global WCF（12.0.SP6.6 起） | 以 WCF 取代 RPC，可套用 WCF 的傳輸層安全等設定（XML 設定檔） |
| WCF 服務名稱 | 為了強制 12.0.SP6 與 12.1 之間的介面變更，端點改為 `.../GlobalWcfService_11_1_201011`，WSDL、服務合約同步改名；**從 12.0.SP6 沿用的 `GlobalWcfClient.config` 與 `admindWCF.exe.config` 必須手動改** |
| Claim 指令 | 對 Extract 的 Global Claim **必須全部成功才通過**（以前部分失敗也會通過） |
| `ADUUID` | 屬性長度由 120 縮為 40 字元 |
| 已知問題 | RPC daemon 偵測不到已在跑的 WCF daemon；Database Distribution 在 HUB daemon 停止時會卡住直到所有重新配置指令逾時；預設繪圖檔與 Stencil 不會在建立新地點時傳播；分散式 Extract 的 issue 失敗時 claim 可能遺失（出現「has been deleted in a later session」） |

## 47.8 各領域新功能與變更彙整

> 以下依公告章節整理，標示 SP 版本；「行為變更」欄是對升級影響的判斷，來自各頁的 Compatibility Constraints 或描述中的「不再…／改為…」。數量龐大（Hull Detailed Design 單章逾 100 則），只列代表項目。

### 47.8.1 通用與 Initial Design

| 項目 | 版本 | 說明 |
|---|---|---|
| Hull 物件與 Extract | 12.1 | 在 Extract 修改 hull 物件時**自動嘗試 claim**，不必明確 claim |
| 無名 Hull 元素識別 | 12.1 | 顯示名稱由 `HSTIFF 3 of ...` 改為 `HSTIFF idsp 6003 of ...`（依 `TBID` 值）〔行為變更：依序號辨識的腳本要檢查〕 |
| NameSeq | 12.1 | `SetStart` 不再重新開始序列，改為儲存起始值；新增 `ReStart` 方法〔行為變更〕 |
| `!!HullNewBlock` | 12.1 | PML 函數，在指定資料庫建立 BLOCK |
| 孤兒 STALNK | SP2 | `!!stmcleanup()` 清除 CELREF 無效的 STALNK |
| Initial Design（SP3–SP4） | | ALYS 資料庫型別（存放 Hydrostatics 輸出）；Oil Outflow（MARPOL）；SOLAS 2009 機率穩度；多個 Lightship 重量；各 Loading Condition 設海水密度；Lines 的 PACE 新功能；專案資料支援 roaming profile |
| Release of Weights to Calc | 12.1 | 預設改為**關閉**〔行為變更〕 |

### 47.8.2 Hull

| 領域 | 版本 | 代表項目 | 行為變更／升級注意 |
|---|---|---|---|
| General | SP2–SP5 | Ship coordinate 對 RSO 標註（SP3）、HPLATE 與 HPREND 的 Ppoints、Hull Notes 與 Posno 分開、Surface 上限 100→**1000**、Hull Qualities 移到 CATA（`HullCreateQualityList`）、raw plate 由 MANU 移到 CATA（`HullDefineRawPlates`）、`SBH_FREE_SEAMPROF_NAMES` 改由 InitHull 設定、殼板 Generic Primitive 表示（SP4） | 自由命名、Hull Qualities 要依升級手冊轉換 |
| Surface Manager | 12.1–SP5 | **取代 Surface Server**：所有曲面必須釋放進資料庫；可匯入 IGES、SAT、STEP、dml；曲面比較、水靜力資料、Flip Normals、匯出 blines（SP5） | 依賴 Surface Server 的流程要改 |
| Space Management | SP3 | 空間定義資料存於資料庫、可重建；Space Interrogation API 偽屬性（`SPMAS`、`SPMCF`、`SPMRSO`、`RSOPP`）；需特別授權 | 需 Optional Upgrade 項目 2893 |
| Structural Design | SP2–SP5 | Create RSO from Panel（RSO Sketch 2D，SP5）、Block Divide 新介面（SP4）、RSO 重建／改名／改 Envelope、Patran 介面（SP2）、FEMWLD 容納 HIBLO／HIPAN／FEMODL／FEMIMG、**Jumbo panels 移除**、Envelope 可用 box 產生 | `COR` 關鍵字統一，**升級前建立的 panel 重建後可能改變** |
| Detailed Design（一般） | SP2–SP5 | 新 Bevel 類型 117 等與 profile endcut、FRP 擴充（doubling、seam、notch、hole beads）、Mixed FRP 與 Steel 專案、Hull Marks 重寫（SP3 起存於 Hull Mark world）、Jig Pillar、Reporting（SP3） | |
| 生產資料（MANU） | 12.1 | **MBLOCK／MPANEL 作廢**，生產零件改存於 `MANPKG`（含 `MPKGFT` 規則與 `MPKGFL` 資料夾）；生產程式**不再更新 DESI**；sub panel plate parts、bracket panel plate parts 不再儲存；曲板 template／jig／pillar 資訊改存 MANU | **舊專案必須用 ManuConfig add-in 的 Upgrade tool 升級** |
| Design Reuse | SP4 | 專案間複製設計資料；支援 Distributed Attributes；PML Triggers | |
| Assembly Planning | SP2–SP5 | Verify naming（SP5）、Assembly ADP 圖紙類型與 parts list 展開、`AssemblySelection` PMLNET 物件、ASMBLY 新增 POS 屬性 | |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Envelopes 對話框：勾選 Generate from Box 後，可輸入 Min. Point 與 Max. Point，或用 Box from GP 取得

*圖 47-10　Envelope 以軸向對齊的 box 產生：官方說明從 General Particulars 取值時會在各方向各加一公尺。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕設計樹狀：FEMWLD 之下有 FEMIMG、HIBLO、HIPAN、FEMODL 等元素，與 BLOCK 並列於 Design WORLD

*圖 47-11　新的 FEM 世界 FEMWLD：容納理想化區塊（HIBLO）、理想化平面（HIPAN）、FE 模型（FEMODL）與 FE 影像（FEMIMG）。（AVEVA 官方文件截圖，僅供內部教學）*

### 47.8.3 Marine Drafting 與 Outfitting Draft

| 領域 | 版本 | 代表項目 | 注意 |
|---|---|---|---|
| 模組改名 | 12.1 | **Hull Drafting 改名 Marine Drafting**：`PDMSUI\hdra` → `PDMSUI\mdra`、`PMLLIB\hulldrafting` → `PMLLIB\marinedrafting` | **自訂 PML 路徑與引用要改** |
| 觸發器 | SP4 | 新 PML Triggers 要取代舊 Vitesse triggers | 舊觸發器遷移 |
| 圖紙類型與 ADP | SP3 | 新的 marine drawing types、General ADP、Steelwork Detailing、Autotagging 引入 Marine Drafting；圖紙清單效能大幅提升 | 需 Optional Upgrade 項目 38541、45823、15251 |
| 圖層 | SP3 | 舾裝模型不再全放同一層（原本是 `-2501`） | 依圖層過濾的流程要重新檢查 |
| SP5 變更 | SP5 | Blanking 控制、Insert Model 預設目標視圖、**無效的 model subview 處理**、**邏輯資料庫名稱（D065 檔）**、Open Drawing 圖紙類型比對、`MarAPI DwgOpen`／`DwgExist` 行為改變、Insert Fillet | `DwgOpen` 傳入全名與圖紙類型時，類型不符就不會開啟〔行為變更〕 |
| SP2 | SP2 | **SZ021 批次程式不再支援**（改用 C# 或 PML 搭配 Marine .NET API） | |
| 輸出格式 | 12.1 | **移除 CGM 與 TIFF PackBits** 匯出 | |
| Outfitting Draft | 12.1 | 線寬在所有輸出格式精準輸出（ISO 128：0.18、0.25、0.35、0.5…）；使用者線型不再轉成 0.2 mm 的倍數；可設定 DXF/DWG/DGN 匯出（建議 AutoCAD 2007–2010，DXF 版本為 AutoCAD 2006）；Unicode 文字 | 預設 `MINLW` 欄位自 Plot 表單移除；DXF General 表單的「Polyline width factor」與「Character encoding」移除 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Open Drawing 對話框：Drawing type 下拉選單最後一項 Assembly ADP drawing 以紅框標示

*圖 47-12　12.1 新增的 Assembly ADP drawing 圖紙類型，專供 Assembly Automatic Document Production 建立的圖紙。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Plotting Options 表單：Colour correction mode（Standard、Colour Plus、Greyscale、Black & White）與 AVEVA-Plot-Service、Postscript、HPGL、Print、Other documents 五個列印選項

*圖 47-13　Draft 的 Plotting Options 表單。12.1 起，Minimum Line Width 欄位已自此表單移除。（AVEVA 官方文件截圖，僅供內部教學）*

### 47.8.4 Outfitting、Catalogue、Global、Engineer

| 領域 | 版本 | 代表項目 |
|---|---|---|
| Model Editor | 12.1–SP5 | Offset From Feature…；結構 primitives 可像設備一樣編輯；Move／Drag Move／Plane Move 新定位選單（含 WRT gadget）；Reorder Hierarchy（SP5）；Weight and CofG 表單移除 Within Area |
| 變更管理 | 12.1 | Session 顯示原因；`REVert` 指令；Extract Data Control 與 Model Changes add-in（Query > DB Changes）可在 3D 圖形標示變更 |
| Mechanical Equipment Interface | SP3–SP4 | Tesselation cache、匯入 SUBE 層級、STEP 座標系實體（需 Optional Upgrade 2931）、單一 STEP 檔匯出 |
| Equipment／Piping | SP3–SP5 | CSV import 擴及 Piping、HVAC、Cable Tray；非標準管路連接（tappings、boss，SP4）；管製造新能力（SP4）；Pipe Sketch 表單大幅修改（新增 Drawing Name、Revision、Status 欄，SP5）；斜率管路（`OFFTOL`）；直接設定保溫厚度與材料；彎管機 NC 輸出；管製造檢查用自訂庫存長度；Pipe Penetration seal 元件 |
| Structures | SP4 | 新元素 `BPANEL`（彎曲面板）；鋼構連接介面改用 EDG |
| Hole Management | SP4–SP5 | 建立、合併、修改孔；Hole Association Manager；Design 與 Outfitting 中的孔管理（SP5） |
| 其他 | 12.1 | Standard Model Library；Clash Utility 新表單；Cable Design 手動路由；HVAC 分多個 Branch 與新屬性（`HEADW`、`HEADH`、`TAILW`、`TAILH` 等，SP5） |
| Isodraft | 12.1 | 輸出 PDF、Image、EMF；TrueType 字型；大座標；PSPOOL 繪製 |
| Catalogue | 12.1–SP2 | Model Settings 只改 catalogue 參數；Detail Text 可用以 `(` 開頭 `)` 結尾的文字運算式；結構 catalogue 的 Copy 按鈕；SPRF 一致性檢查新增多項警告（SP2） |
| Global | SP3 | 見 47.7.3 |
| Diagrams／Engineering | SP2–SP5 | **SP5 起 AVEVA Diagrams（14.1.SP1）與 AVEVA Engineering（14.2）為獨立產品，不隨 H&O 12.1.SP5 安裝**；Tags 模組、Compare/Update、Datasheets、Ribbon UI、Diagrams Rules、Design Reuse 等 |

### 47.8.5 ERM 整合與 Tribon 移轉

- **AVEVA ERM 整合（SP5）**：原本是獨立安裝的 add-in，現在是標準功能。三個新方向：在 Marine Catalogue 定義 raw profiles 並與 ERM 同步；在 ERM 預留與配置 raw plates／profiles 供 Marine 套料，並在兩者間傳輸；把 Schematics 資料庫為基礎的預備零件表轉成 ERM 的 Advance Bill of Material。
- **Tribon M3 移轉能力終止（SP5）**：原因是 Administration 1.5 為通用模組，難以支援 Tribon 的專用能力；需要持續移轉的客戶可保留獨立的 12.1.SP4 安裝，再把結果搬到 12.1.SP5。另：讀取原生 Tribon indexed databanks 的能力已移除，移轉前須先把 Tribon databank 升級成中性格式；Tribon 5 Curved Hull 輸入資料的轉換選項也已不存在。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Catalogue Explorer 與 Material Category Mapping 表單：ERM Material Type、Material Description、Plate/Profile Mapping 分頁與 TABWLD、RPRTAB 欄位

*圖 47-14　AVEVA ERM 整合的 Material Category Mapping 表單：把 ERM 材料類型對應到 Catalogue 的 raw profile（RAWPRM）。（AVEVA 官方文件截圖，僅供內部教學）*

### 47.8.6 已知問題

SP5 的 General Issues 只寫「請見發行文件的更新清單」，離線文件裡沒有具體清單。可看到的已知問題：PML 表單 layout 變更會影響既有表單（SP3，KB4453）；Global 的幾項問題（見 47.7.3）；新 Reporting add-in 的限制（批次效能、RTF 背景色、浮水印、表格不能 Copy/Cut/Paste、calculated field 不能引用 summary 等）。

## 47.9 升級檢查清單

> 〔官方〕來自公告；〔一般實務〕為維運常見做法，需依公司政策調整。

| 階段 | 檢查項目 | 來源 |
|---|---|---|
| 規劃 | 確認目前版本與目標版本；**早於 12.0 的專案先升 12.0** | 官方 |
| 規劃 | 通讀公告的 Compatibility Constraints、Affected Programs，列出與我們使用領域有關的行為變更 | 一般實務 |
| 規劃 | 確認授權：ALS 而非 FlexMan；Diagrams／Schematic Model Manager／Schematic 3D Integrator 使用者要更新授權檔 | 官方 |
| 規劃 | 決定 Optional Upgrade 的時機與是否需要與舊版並行（SP2＋SP3 需要特定 hotfix 與不套用 Optional Upgrade） | 官方 |
| 規劃 | 確認路徑無空白；規劃 Cache Service（MSMQ） | 官方 |
| 規劃 | 盤點自訂 PML：Status handler、Auto-naming、PML Collection、單位相關指令、Marine Drafting 路徑改名、Vitesse trigger、SZ021、`SBH_*` 變數 | 官方＋一般實務 |
| 規劃 | 盤點 UDA／Catalogue 參數的單位，決定每個維度採新單位或 `NUMERIC` | 官方 |
| 規劃 | 確認 `PROJECT CHARSET`／`PROJECT MBCHARSET`；決定哪些 DB 轉 Unicode | 官方 |
| 演練 | 在複製的專案先走完整流程，含 Global 與 Extract 情境 | 一般實務 |
| 升級前 | 使用者全部離線、各地點鎖定、清 Working Extract、Expunge、DICE（問題先修）、備份所有地點 | 官方 |
| 升級前 | 非外部 DB 遷到其 master 的 Primary 地點；確認無 Transient DB | 官方 |
| 升級 | `lock` → `dbupgrade project to latest` → 可選合併 Session 與 Reconfigure → DICE → Extract 遷回 → 非框架升級 → `unlock` | 官方 |
| 升級後 | 確認沒有「以唯讀開啟」警告；舊版軟體使用者全數汰除 | 官方（舊版不做檢查） |
| 升級後 | 跑報表對照、單位數字對照、圖紙更新、批次工具回歸（見 [第 17 章](ch17_debug_deploy_zh-TW.reading.html) 的 SP 回歸清單） | 一般實務 |
| 回復 | 官方：升級後無法 backtrack 到升級前的 Session（詳見 [第 20 章](ch20_system_administration_zh-TW.reading.html)）；回復只能靠升級前備份 | 官方＋一般實務 |

### 47.9.1 版本差異與升級風險排序

| 風險 | 事項 | 原因 |
|---|---|---|
| 高 | 舊版軟體仍開已升級的資料庫 | 12.1 以前版本不做檢查，可能造成不一致 |
| 高 | Unicode 編碼資料庫被 12.0 使用者開啟 | 讀寫皆不可 |
| 高 | 套用 Optional Upgrade 後仍有 SP2 或更舊使用者 | 不相容 |
| 高 | MANU 資料模型改變（MBLOCK／MPANEL 作廢） | 舊專案需 ManuConfig 升級 |
| 中 | 單位換算 | 資料正確性（數字與單位） |
| 中 | 自訂 PML（Status、命名、Collection、模組改名） | 行為改變 |
| 中 | Global WCF 設定檔與服務名稱 | 沿用舊設定檔會連不上 |
| 中 | SP5 起 Diagrams、Engineering、Administration 為獨立產品 | 安裝與授權要另外規劃 |

> **專業提醒：** 上表風險排序是依公告敘述做的判斷〔一般實務〕，不是官方分級。

## 47.10 術語與縮寫重點

### 47.10.1 Terminology（官方詞彙表重點）

官方詞彙表以 Outfitting 為語境，另有 Macro、Batch Mode、Plotfile、Level 等一般詞條，此處不列。

| 詞條 | 重點 |
|---|---|
| Element／Attribute | 資料庫中的離散資料項，由編號或名稱識別，由屬性定義 |
| Database／MDB | 階層式資料庫；MDB 是為特定目的行政上連結的一組資料庫，使用者要有包含該資料庫之 MDB 的存取權 |
| Team／Member | Team 是共享資料庫存取權的使用者行政分組 |
| WORLD | 任何資料庫的最高層元素，名稱固定為 `/*` |
| Owner／Member／Parent／Offspring | Owner 是直接上層，Parent 是任意上層；Member 是直接下層，Offspring 是任意下層；GROUP 成員只是間接連結 |
| Name | 使用者指派的識別字，以 `/` 開頭；永遠另有系統自動指派的參考號 |
| Current Element (CE) | 使用者在資料庫導覽中目前所處的元素 |
| P-point／P-line | 想像的位置與方向，用於操作與連接元素；P-line 是朝特定方向擠出的 P-point |
| Primitive | 構成物理實體的基本形狀（box、cylinder 等） |
| PIPE／BRANCH | PIPE 是 BRANCH 的集合，意義可能與一般工程用法不同；Head 是 BRANCH 輸入端，Tail 是輸出端 |
| Appware | 為特定設計任務（如管路設計）設計的一組 forms 與 macros |
| Form／Docking | Form 即對話框；可停靠（dockable）的表單與工具列 |
| User-Defined Attribute | 名稱與內容類型由使用者定義的屬性 |

### 47.10.2 Abbreviations（Marine 專用縮寫）

| 縮寫 | 全名 | 縮寫 | 全名 |
|---|---|---|---|
| AP | Assembly Planning | PIM | Product Information Model |
| APL | Assembly Parts List | PLCM | Panel Line Control Module |
| AWR | Assembly Weld Report | PM | Production Manager |
| CAT | Curve and Table | PPI | Production Program Interface |
| CVBA | Continuously Varying Bevel Angle | RSO | Reference Surface Object |
| DM | Design Manager | RWS | Read, Write and Change Status |
| FD | Functional Description | TDM | Data Management |
| GPP | Generic Postprocessor | TDT | Developer's Toolkit |
| GSD | Gütesicherungsdreiecke（品質保證三角） | TID | Initial Design |
| IP | Information to the Program | TIL | Interpretative Language |
| WOP | Work Preparation | TJL | Job Launcher |
| WP | Weld Planning | TRI | Robot Interface |

官方說明：這張表只收 AVEVA Marine 特有的縮寫，**不含**造船或資訊領域通用縮寫，也不含變數、databank 名稱、互動函數名稱、輸入檔指令等（這些在一般使用者文件中說明）。

## 47.11 本章小結

1. Release Bulletin 是「版本差異」的主要依據；用 SP 標記與 Compatibility Constraints 抽出對自己有影響的項目。
2. 12.1 的升級是「Part Upgrade＋升級編號＋版本控管」；舊版軟體不做檢查，是最大的混用風險。
3. Optional Upgrade（12010301、12010401）是單向門；套用前確認全員版本與 Global Server 版本。
4. 升級流程的關鍵：鎖定、DICE、備份、Extract 處理、再 DICE；Working Extract 必須 flush。
5. Unicode 與單位是資料表示法變更，要分別針對資料庫與自訂 PML 驗證。
6. SP5 把 Administration、Diagrams、Engineering 拆成獨立產品，並終止 Tribon 移轉；安裝與授權規劃要跟著改。
7. 領域新功能中，「行為變更」（MANU 資料模型、模組改名、命名規則、Status handler、PML Collection）比「新功能」更影響升級。

## 47.12 練習題／自我檢核

1. 一個專案資料庫的升級編號是 12.1.1，用 12.1 前的軟體開啟會發生什麼事？用未來的 12.2 軟體開啟呢？
2. 為什麼 Working Extract 在升級前必須 flush，而一般 Extract 不必？
3. 你的公司有 12.1.SP2 與 12.1.SP3 使用者要共用一個專案，條件是什麼？
4. 列出把 UDA 的壓力屬性改用新單位的步驟（依資料存放現況）。
5. 說明 Unicode 編碼的資料庫為何不能放回 12.0 使用者的專案。
6. 為何「Compatibility Constraints：None」不等於可以略過測試？
7. 練習：從公告裡挑三個你們專案常用的功能，找出其版本標記與 Affected Programs，整理成一頁升級風險表。

**自我檢核**

- [ ] 我能解釋 R/W、R、X 矩陣。
- [ ] 我能說出 Optional Upgrade 的代價。
- [ ] 我能依官方順序寫出升級流程。
- [ ] 我能分辨公告中 SP5 與舊版遺留的環境需求。
- [ ] 我能列出升級前後各自該檢查的項目。

## 47.13 〔待核對〕項目與取材覆蓋

### 待核對

1. **環境需求矛盾**：SP5 作業環境表寫 .NET Framework 4.6.1，另一頁寫需要 .NET 3.5；IE 7/8、Office 2007/2010、Windows XP 等敘述疑為舊版遺留，實際以 AVEVA 支援網站與《Minimum System Requirements Marine》為準。
2. **Windows Server 與虛擬化／Citrix**：ALS「利於 Citrix 支援」的實際條件，以及不再支援 thin client 後的部署方式。
3. **About this Bulletin** 同時出現「自 12.1.SP4 以來的變更」與「自 12.0 以來的變更」兩種描述，推測為多版本文字並存。
4. **ASL**：SP4 一頁說已移除並由 Vantage Marine 11.6 的 primitive 型能力取代；「Future Considerations」一頁說將改稱 SLH，兩頁的先後與現況待核對。
5. **Optional Upgrade 12010401** 官方稱僅含項目 93792「一般資料庫變更」，內容細節未說明。
6. **MANU 資料模型升級**的 ManuConfig 具體步驟，在《12.0 to 12.1 Upgrade》手冊，不在本文件。
7. **Windows 專案路徑空白**問題在 SP5 之後是否已解決。
8. **「Known Issues」的 SP5 General Issues** 只指向外部發行文件，未提供清單。

### 取材覆蓋

- **已取得**：*Hull and Outfitting* [1224159] 下全部 587 頁（含根頁）皆已轉出純文字並掃描標題。其中**逐字讀完**的約 140 頁：About、Software Distribution and Installation、Test Projects、Upgrading from Previous Releases 全部、Configuration、General System Changes、Database changes、User Interface、Administration、Global 與 Catalogue 部分頁面、Known Issues 與少數 Hull 生產資料頁面。**只讀開頭（約 280–700 字元）**的約 440 頁：各領域新功能（Initial Design、Hull General、Surface Manager、Space Management、Structural Design、Hull Detailed Design、Weld Planning、Assembly Planning、Marine Drafting、Outfitting Draft、Diagrams、Engineering、Outfitting Module 與 Design Applications）。這些頁只擷取 Description 與標題，Benefits、For More Information、Compatibility Constraints 的細節大多未完整讀，因此 47.8 的彙整表是「代表項目」而非完整清單。
- 另讀：*What's New in AVEVA Marine?* [1105760]、*Welcome to the AVEVA Marine Documentation* [1526835]、*Terminology* [1225318]、*Abbreviations in the User Documentation* [1109374] 全文。
- **未讀**：*Before you Begin* [1211036] 下的 Marine Getting Started 子樹（Assumptions、Database Types、Attributes、GUI 基本操作、Product Range、Glossary of Terms and Abbreviations 的 Definitions／Abbreviations、Core Filters for Explorers 等，約 50 頁，只列出清單）；以及公告中 AVEVA Licensing System [883754]、AVEVA Manufacturing [988916]、AVEVA Marine [879117] 三個夾在 Hull Detailed Design 中的頁面（只看到標題，內容未深入）。
- 圖片共 14 張，皆經預覽確認後加入。
- 相關章節：[第 20 章](ch20_system_administration_zh-TW.reading.html) 系統管理與維運、[第 42 章](ch42_database_management_zh-TW.reading.html) 資料庫管理（Session、Extract、Global 概要）。
