# 第 37 章　船體資料庫與分散式專案：Hull Dabacon 與 Global

> 前面章節談過船體概念、建模與生產。這一章回答兩個「資料放在哪裡、怎麼跨地點共用」的問題：**船體資料在 Dabacon 資料庫裡長什麼樣子、專案怎麼建起來、資料庫怎麼維護；以及當設計團隊分散在多個地點時，AVEVA Global 如何讓每個地點擁有自己的資料庫副本並自動同步。**
>
> 船廠的現實是設計、舾裝與生產分處多地，卻都想「像在同一個專案裡工作」。系統管理者要知道哪些設定一旦做錯很難回頭（例如 Global 專案不能轉回標準專案），二次開發者要知道自己的批次與報表在分散式環境下會看到什麼資料。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的 *Hull Dabacon* 與 *Global* 兩個模組（含 Global Server Installation、Running Global Projects、Global User Guide、Global WCF Configuration）。官方「Distribution of Hull Data Using Global」頁只有一句「請聯絡 AVEVA Marine Support」，**船體資料專屬的 Global 配置沒有官方細節**，本章不編造；Global 的通用機制（位置、分配、更新、Extract、WCF）則有完整文件。Global 文件多處以 PDMS／Plant 為例、提到 Windows XP／2003 等舊平台，操作概念適用，細節以 12.1 實際安裝為準，標〔待核對〕。

## 37.1 學習目標

讀完本章，你應該能夠：

1. 說明船體資料在 Dabacon 中以「二進位 blob＋明確儲存資料」並存，以及 Apply 為何是同步點。
2. 區分 Reference Surfaces、Design panels、Production panels 三種模型視角與參照穩定性規則。
3. 說明 Hull 工作流程指令（Activate、Apply、SaveWork、Unclaim、GetWork）的先後與影響範圍。
4. 列出船體專案需要的資料庫型別與主要 World 元素。
5. 使用 DbPrompt 建立頂層元素、批次建立 BLOCK，並知道 `NEW` 與 `!!HullNewBlock` 的用途。
6. 說明哪些 Dabacon 管理工具可用於船體資料、哪些要避免。
7. 說明 Global 的 Hub／Satellite、Primary／Secondary、Daemon、Transaction database 等核心概念。
8. 依順序建立 Global 專案：make global、初始化 Hub、建立位置、安裝 Satellite、分配資料庫、設定 Update event。
9. 使用 Command Transactions 視窗、Daemon 追蹤與日誌診斷同步問題，並知道恢復與備份的原則。
10. 說明 RPC 與 WCF 的差異、設定檔關係與防火牆埠設定，以及二次開發者在分散式環境下的注意事項。

## 37.2 本章定位與既有章節分工

本章只補既有章節沒講的部分：Team／MDB／Claim／Extract 基本概念與 Global 簡介見 [第 2 章](ch02_project_database_zh-TW.reading.html) 2.9；專案建立、DICE、Merge、Replicate、備份見 [第 20 章](ch20_system_administration_zh-TW.reading.html)；船體 Databank 與 Dabacon 對應（TBID）見 [第 5 章](ch05_hull_modelling_zh-TW.reading.html)；船體概念（分段、板、骨材）見 [第 36 章](ch36_hull_concepts_zh-TW.reading.html)；DEXTR／Vitesse 見 [第 15 章](ch15_hull_vitesse_zh-TW.reading.html)。本章補的是：船體資料在 Dabacon 內的落點，以及 Global 的實際建置、分配、監控與 WCF。

## 37.3 船體資料如何存在 Dabacon

### 37.3.1 資料庫型別與儲存方式

所有船體資料都存在 Dabacon 資料庫：**Hull 設計模型（Initial、Structural、Detail）存 DESI 型別，Hull 製造資料存 MANU 型別**。船體資料以「二進位資料（blob）＋明確儲存資料」混合保存：blob 只供 Hull 應用程式內部使用，明確資料則供 Design、Assembly Planning、Accommodation、通用框架（3D 顯示、Explorer、屬性查詢）與 PML 使用。blob 與明確資料在 **Apply** 時同步。

幾何（2D／3D）**不明確存在 Hull 元素中**，而是在 3D 顯示、2D 繪圖、Clasher 等需要時即時產生；Hull 製造元素不能顯示在 3D 圖形視窗，要看圖時用 Marine Drafting 畫布。

### 37.3.2 三種模型視角

平面船體（Planar Hull）有三種模型資料：**Reference Surfaces**（Initial 階段建立）、**Design panels**（Structural 階段）、**Production panels**（主要用於 Detail 階段）。三者使用相同的元素型別（含下屬元素），以一個屬性區分是設計還是生產版本；Clasher、3D Display、質量特性計算可切換以設計或生產視角作為障礙物。

> 〔公開版未收錄：AVEVA 官方產品截圖〕船體三種模型視角：Reference Surfaces、Design Panels、Production Panels，下層參照上層

*圖 37-1　三種模型視角與參照方向。（AVEVA 官方文件截圖，僅供內部教學）*

設計方（舾裝等）可以參照任何一種視角，但資料庫中的關聯**永遠指向最穩定的元素**：有 Reference Surface 就指它，其次 Design Panel，最後才是 Production Panel。

### 37.3.3 元素與命名規則

| 項目 | 官方說明 | 對開發者的意義 |
|---|---|---|
| 對稱 | 每個實體 Hull 項目是獨立元素；對稱分段 AAA 會有 AAA 與 AAA_R 兩個 | 統計重量、數量時不要漏掉 `_R`；名稱衝突時自動加序號（從 1 起） |
| 側別屬性 | 有屬性可查 Starboard／Portside／OverCL、是否對稱、是否鏡射 | 屬性名稱〔待核對〕 |
| 無名元素 | 預設顯示如 `HSTIFF 3 of HPANEL /ER2-LP32_2`（第 3 個同型子元素） | 位置會變，不可當識別碼 |
| 以 TBID 識別 | 有 `TBID` 的無名元素顯示為 `HSTIFF idsp 6003 of HPANEL /ER2-LP32_2`；`IDSP` 關鍵字對應虛擬屬性 `IDSPU` | 以 GID graph 為基礎的指令可用此格式識別 |
| Hull Block World | 可含一或多個 Hull Block World；**HBLWLD 為選用**，BLOCK 可直接作頂層 | 由客戶決定是否使用此層 |
| PPoints | `HPLATE` 的 `PPOS` 回傳角點事件點：索引 0–49 為 DIST(1) 側、50–99 為 DIST(2) 側、100–149 為模板面（mould plane）；`PPLS` 列出有效索引、`PPVI` 列出可見索引 | 取板角點座標的官方依據 |
| 其他資料庫 | 型鋼規格取自 Marine Steel Catalogue（須在 Hull MDB 內）；NSEQ（Name Sequence）供曲面船體自動命名縱材、橫材、外板縫與生產草圖 | 見 37.5 |

### 37.3.4 製造資料：MANPKG 規則式分包

製造資料庫以「製造包（Manufacturing Package）與資料夾」為核心，用可自訂規則把生產零件分類：

| 元素 | 內容 | 規則 |
|---|---|---|
| `MANPKG` | 至少一個 Filter 與一或多個 Folder | 依 MDB 內順序，生產零件存入**第一個**規則為真的製造包；找不到則回報系統錯誤 6701 |
| `MPKGFT` | 單一規則，PML 1.1 邏輯運算式 | 例：`MATCHWILD ( ATTRIB NAMN, 'ER5*')` |
| `MPKGFL` | 資料夾，各有一條規則，可巢狀 | 例：`ATTRIB TYPE EQ 'MPLATE'`、`TRUE`；可設一個預設資料夾收容不符規則者 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕製造包結構：MANPKG 下含 Filter 與巢狀 Folder，右側為 MANU Explorer 樹

*圖 37-2　製造包、篩選器與資料夾的階層，以及在 MANU Explorer 的呈現。（AVEVA 官方文件截圖，僅供內部教學）*

為了效能，系統會**先測試上次命中的製造包**，若規則彼此重疊結果可能不可預期；此時須設環境變數 `SBH_OVERLAP_MANPKGRULES=YES`，強制每次從第一個製造包開始比對，代價是儲存零件時變慢。單一規則為 `( true )` 的製造包不受此優化影響。屬性 `mpfind` 可查設計或生產元素會存到哪個製造包、`mffind` 可查會存到哪個資料夾。

### 37.3.5 Hull 工作流程：工作區、Apply 與 SaveWork

每個 Hull 應用程式內部有一個 **Hull workspace**（Hull 物件的暫存快取）。圖形互動走 Marine Drafting；更新在執行 **Apply** 之前，工作區外都看不到。

| 指令 | 作用 | 舊稱 |
|---|---|---|
| Activate | 啟用面板供更新（隱含 Claim） | Curved Hull 稱 select |
| Apply | 接受變更，與 Dabacon session 同步，使 Explorer、3D、查詢、PML 看得到 | store |
| Deactivate | 還原工作區中的變更 | skip |
| Apply and Deactivate | 接受並停用 | store and skip |
| SaveWork | 提交變更到資料庫，其他 session 才可見 | — |
| GetWork | 取回其他 session 的最新更新，工作區隱含更新 | — |
| Unclaim | 解除全部或選定元素的鎖定 | — |

> 〔公開版未收錄：AVEVA 官方產品截圖〕兩位船體使用者與舾裝使用者透過 Dabacon 的資料流：Apply、SaveWork、GetWork

*圖 37-3　Hull 使用者 1 SaveWork 後，舾裝使用者與 Hull 使用者 2 須 GetWork 才看得到。（AVEVA 官方文件截圖，僅供內部教學）*

- **隱含 Claim：** Hull 物件（平面板、曲面板、縱材）在被啟用更新時自動 Claim；其下屬元素（加強筋、板）不能單獨 Claim。SaveWork 之後仍須明確 Unclaim 其他人才能改（離開應用程式時也會自動 Unclaim）；官方提供把 SaveWork 與 Unclaim 合併的功能。
- **Deactivate 不還原 Dabacon session：** Apply 之後的變更不能用 Deactivate 還原。
- **更新限制：** Hull 元素只能由專屬 Hull 指令更新，例外包括新增／編輯 UDA、文件連結與一般 Association。其餘（查詢、Explorer、`Query`、`Attribute` 指令）可照一般 Dabacon 方式讀取。
- **批次作業：** 在 Hull 設計應用程式內啟動批次前，必須先 SaveWork 與 Unclaim；批次結束後必須 GetWork 才看得到結果。

> **專業提醒：** 寫給 Hull 資料用的 PML 或批次工具，最常見的錯誤是讀到「還沒 SaveWork／GetWork」的資料。流程是：Hull 使用者 Apply → SaveWork（＋Unclaim）→ 你的程式所在 session GetWork → 才讀取。官方說 DEXTR 關鍵字仍支援（例如可由 Vitesse 使用），但**不會再擴充**。

## 37.4 圖面在 Dabacon

Marine 圖面由兩部分組成：**PADD 資料庫中的資料**，以及**一個含 Marine 圖面物件的檔案**（每個 `SHEET` 元素一個檔案），位於環境變數 `<project>drg` 指向的目錄，路徑由 SHEET 虛擬屬性 `DOFILE` 指出。圖面存在 PADD 資料庫的 `DEPT`（Department）與 `REGI`（Registry）階層下。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Draft WORL 下的 DEPT 與 REGI 階層：ProfNest、NestPlt、General、WeightCoG 等

*圖 37-4　PADD 資料庫中依圖種組織的 DEPT／REGI 階層。（AVEVA 官方文件截圖，僅供內部教學）*

圖種如何分到 DEPT／REGI，由 Marine 專案設定檔（d065 檔）的邏輯變數控制，例如 `SB_PDB_PADD = General;MarDwg` 表示一般圖面存在 DEPT=General、REGI=MarDwg；`SB_NPL_DGW_PADD = NestPlt;NplDwg` 表示套料草圖存於 NestPlt／NplDwg。規劃時可把板與型材套料草圖放不同 PADD、或依 SITE、BLOCK、ZONE 分庫，並控制單一 REGI 內圖數以維持效能。

**重要：圖面獨立於設計資料儲存**，一般 SaveWork **不會**存 Marine 圖面；必須用 Save Drawing 或 Save Drawing As。（反過來存圖面也不會存 Hull 設計。）圖面細節見 [第 9 章](ch09_drawings_zh-TW.reading.html) 與 Marine Drafting 相關章節。

## 37.5 資料庫與 World 元素

官方建議：**所有 Hull 設計使用者的 MDB 都應含全部 Hull DESI 資料庫**（以主資料庫或 Extract 形式）；為效能可只含正在做的分段加鄰近分段，但所有 Curved Hull 與 Standards 資料庫都應納入。存取權依角色給 Read 或 Write。World 元素須在 Hull 初始化時以 DbPrompt 預先建立；唯一例外是系統在需要時自動建立的暫時分段：`_P<design block>`（分割分段時）與 `JUMBO`（某些 Structural Design 功能）。

| 型別 | World 元素 | 內容 | 建議配置 |
|---|---|---|---|
| DESI | `RSOWLD` | Reference Surface Objects | 專案通常一個；Initial／Structural 使用者可寫 |
| DESI | `COMWLD` | 艙室物件 | 專案**只有一個** |
| DESI | `SSOWLD` | 曲面物件與曲面定義曲線 | 可多個；與穩度計算有關的曲面建議獨立一個 |
| DESI | `HCMWLD` | 曲面船體物件（外板、縫） | 每個 SSOWLD 一個；其下有 Surface Proxy 擁有曲面板與型材 |
| DESI | `MOGWLD` | 設定物件（structref、hullstruct、gentab）與雜項物件 | 設定用一個、雜項可多個 |
| DESI | `STDWLD` | 標準物件（Bracket panels、標準設定） | 建議一個放共用資料、另一個放肘板 |
| DESI | `GRDWLD` | 船體格線（Gentab） | 專案只有一個 |
| DESI | `HBLWLD`／`BLOCK` | 分段與面板 | **每分段一個資料庫** |
| DESI | `MWLWLD` | 焊接 | 一個專用資料庫 |
| DESI | `FEMWLD`、`SPMSW` | 有限元素、空間管理 | 依使用者角色 |
| MANU | `MANPKG` | 製造資料 | 分庫方式同 BLOCK；**所有 MANPKG 須預先建立** |
| MANU | `MOGWLD`、`MRESTQ` | 設定與製造雜項、餘料板 | `MRESTQ` 須依 `/RestQuality:A` 命名 |
| NSEQ | `SEQWOR` | 名稱序列 | 多地點時每個地點一個，各有互不重疊的序號區間 |
| CATA | `SPCO`、`MATW`、`TABWLD` | 型材規格、材質、原板 | 通常由 AVEVA 隨 MAS 專案提供，納入每個 Hull 專案 |

組立規劃的 `ASWLD` 建議放獨立資料庫（每區一個，或全船一個）；組立圖另需 `LINKWL`、PADD 與 NSEQ。

## 37.6 專案建立與初始資料結構

### 37.6.1 流程

1. **建立專案：** 最簡單是用 Project Create Wizard（處理專案資料、專案變數、資料夾與檔案、Marine 環境變數）；手動做法是編輯 evars 專案檔、用 make 工具建立、再以 Marine environment setup 設定 Marine 環境變數（見 [第 20 章](ch20_system_administration_zh-TW.reading.html)）。
2. **建立 Team、資料庫、MDB、使用者：** Team 擁有資料庫；Marine 專案中資料庫自動為 Marine 型別；**Hull 資料庫存取模式建議 Multiwrite 與 Implicit claim**；Hull 應用對 MDB 有特殊要求，部分資料庫必須存在。
3. **建立初始資料結構：** 用 DbPrompt 建頂層元素，再執行 Inithull 建立分段資料與設定標準。

### 37.6.2 DbPrompt

DbPrompt 用來在 DESI 與 MANU 資料庫中互動建立、刪除（空的）頂層節點、匯出匯入定義、驗證必要頂層元素是否齊備。

```
dbprompt -proj=XXX -user=SYSTEM -pass=XXXXXX -mdb=/XXX
dbprompt -in=top_in.csv -out=top_out.csv -proj=xxx
dbprompt -proj=XXX -user=SYSTEM -pass=XXXXXX -mdb=/XXX -blk=sj702.csv
dbprompt -proj=XXX -user=SYSTEM -pass=XXXXXX -mdb=/XXX -in=top.csv -dupname
```

> 〔公開版未收錄：AVEVA 官方產品截圖〕DbPrompt 工具視窗：樹狀顯示資料庫與頂層節點，右鍵選單可新增 SITE、RSOWLD、HBLWLD 等

*圖 37-5　DbPrompt 互動新增頂層節點（此例新增 RSOWLD）。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕以 Excel 編輯的頂層節點 CSV：第一欄資料庫、第二欄 World 型別、第三欄名稱

*圖 37-6　頂層節點定義 CSV：資料庫、元素型別、名稱，BLOCK 可再接子分段欄位。（AVEVA 官方文件截圖，僅供內部教學）*

| 情境 | 做法 | 備註 |
|---|---|---|
| 匯出匯入頂層定義 | `-in`、`-out`（CSV，可用 Excel 編輯） | **先處理 `-in` 再產生 `-out`** |
| 批次建分段 | `-blk=<檔>`（或 `-blockin`） | 區塊 CSV 新增第 25 欄放資料庫名 |
| MANU 內同名元素 | `-duplicate_name`／`-dupname`（預設 false）；互動時 Options 選單 | — |
| 製造包結構 | Tools > Create MANPKG structure：讀 `<project>mac` 的 `manuPkgTemplate.mac`，為每個設計分段、套料、PLCM 套料、型材套料產生指令 | 輸出 `dbpromptManuPkg.mac`，**須先填入正確資料庫名才能用** |

### 37.6.3 指令與 PML（官方有的才列）

```
NEW <element_type> <element_name> DB <database_name>
NEW DEPT /MYDEPT DB MYTEAM/MYDB

!!HullNewBlock(!blkName is STRING, !ownName is STRING) is DBREF
!blk = !!HullNewBlock('MYBLOCK', 'MYTEAM/MYDB')   -- 指定資料庫
!blk = !!HullNewBlock('MYBLOCK', '/MYHBLWLD')     -- 指定 HBLWLD
```

`NEW` 用於非 BLOCK 的頂層元素（`DB` 關鍵字選用）。`!!HullNewBlock` 的 `ownName` 選用但須傳空字串 `''`；成功回傳新 BLOCK 的 DBREF，失敗則顯示錯誤、結果未定義。DEPT／REGI 可用 DbPrompt、指令或 Draft 應用程式建立，由 Draft 建立時要把目標 PADD 在 MDB 中設為目前資料庫，才會存到正確位置。

### 37.6.4 ManuConfig 增益集與專案材料工具

ManuConfig add-in 左側列製造包與資料夾、右側顯示內容並可改規則；可建立、插入、移除製造包與資料夾（僅限內無生產零件者），並可 Dump 成巨集供別的專案使用。規則改變後須 Resort：**Resort manufacturing package** 只評估包內資料夾規則、零件不會換包；**Resort manufacturing items** 零件可能換包。專案材料工具包含 XML 匯出匯入、Material Ordering（Matplate／Matbar，長度或面積加 10% 並取目錄中最大者，標為 proposed）與 Move Rest Material（餘料移到專案材料池）。

> **專業提醒：** 製造包規則改了卻忘了 Resort，是常見的「零件在錯的包裡」原因。同時，Resort manufacturing items 會讓零件換包，下游（NC、報表）若以包為單位要重新產生。

## 37.7 船體資料庫管理

官方整理了通用 Dabacon 管理工具在船體資料上的適用性：

| 工具 | 船體資料適用性 | 重點 |
|---|---|---|
| Replicate | 可複製含船體資料的完整專案 | 專案層級複製見 [第 20 章](ch20_system_administration_zh-TW.reading.html) |
| Reconfigure | 可，**四原則** | 一律複製整個資料庫（不要選個別頂層元素）；一律用 `SAMEREF`；所有資料庫同時複製；一律 Reconfigure 到**空的**資料庫 |
| Stamps | 可 | Stamp 應包含專案內**所有**資料庫，避免模型不一致 |
| Revert／Backtrack | 可 | 同樣須對專案內所有資料庫同時做 |
| Merge Changes | 可 | 與一般 Dabacon 相同 |
| Datal | **不建議複製船體資料** | 無法正確處理 Hull 參照，改用 Marine Copy Assistant |
| Access Control | 資料庫 Team 擁有權、或 DAC | DAC 最低只到 Hull 物件層（如平面板）；**不能對下屬元素或個別屬性設 DAC**；MANU 建議不用 DAC，要控管就以資料庫為單位 |
| Undo／Redo | **Hull 應用目前不支援** | — |
| Extract 資料庫 | 可用於船體與圖面 | 設定 MDB 須格外小心，官方建議聯絡 AVEVA Marine Support |

> **專業提醒：****船體資料的參照橫跨設計階層、關聯、拓樸、圖面、組立，所以任何會「改變或複製資料庫」的操作，都必須對整個專案的所有資料庫一起做。** 只還原一個資料庫是最常見的毀損來源。

## 37.8 專案生命週期與階段

> 〔公開版未收錄：AVEVA 官方產品截圖〕專案時間軸：建立專案、Initial Design、Basic Design、Detail Design、Manufacturing

*圖 37-7　簡化的專案生命週期；實務上各階段互有重疊與反覆。（AVEVA 官方文件截圖，僅供內部教學）*

| 階段 | 主要工作與應用 | 涉及的資料 |
|---|---|---|
| 建立與初始化 | Project Create Wizard、Admin 建資料庫（DESI、CATA、PADD、SCHE、DICT）、DbPrompt、InitHull | 檔案系統、系統資料庫、各頂層元素（MOGWLD、BLOCK、GRDWLD、COMWLD、RSOWLD、SSOWLD、HCMWLD、STDWLD） |
| Initial Design | 主曲面、內部與參考面、艙室劃分；完成後 Release 到 Marine 資料庫 | Initial 設計資料庫（**Initial Design 應用不使用 Dabacon**）；RSOWLD、SSOWLD、COMWLD、SPMSW |
| Basic Design | Structural Design、Curved Modelling、Space Management、分段劃分 | BLOCK、MOGWLD、STDWLD、HCMWLD、NAMESEQ DB |
| Detail 與生產設計 | Planar Hull Modelling、分段再分割；以 Ppanparts／Cpanparts 釋出到 MANU；Assembly Planning | 上述加 MANU 資料庫、`ASWL` |
| Manufacturing | 切割（2／3 軸板套料、型材套料、組立套料 PLCM）、彎曲（模板、Jig、型材彎曲）、組立資訊 | MANU、PADD；產出 NC 資料、草圖、報表、圖面 |

## 37.9 Copy Assistant 與 Global 分發入口

**Copy Assistant** 支援專案之間複製模型與圖面，官方指定用它取代 Datal 複製船體資料；詳細功能在 *Database Management Reference Manual*，本章依據的頁面只有簡介，操作步驟〔待核對〕。

**船體資料的 Global 分發：** 官方僅請聯絡 AVEVA Marine Support。已知的相關要求：多地點 NSEQ 序號區間（37.5）、Marine 圖面檔強制傳播（37.10.4）、Extract 與 MDB 設定須格外小心（37.7）。

## 37.10 Global：分散式專案概念

### 37.10.1 角色與詞彙

| 詞彙 | 意義 |
|---|---|
| Location | 專案的一個地點；每個地點有自己的資料庫副本與 Global Daemon |
| Hub | 負責整體專案管理的地點；**Team、資料庫、Role、其他 Location 與 Location Group 只能在 Hub 建立** |
| Satellite | Hub 以外的地點 |
| Primary／Secondary | 資料庫**只能在一個地點寫入**（Primary），其他地點為唯讀副本（Secondary） |
| Global Daemon | 每個專案每個地點一個背景程序（亦稱 Admin daemon），負責檢查變更並傳播 |
| Global database | 存 Team、資料庫、Location、Role 資訊；只能在 Hub 修改，傳播到各 Satellite |
| System database | 每個地點自己一份（`prjsys`），存 Users、MDB 等；自動傳播到所有地點 |
| Transaction database | 記錄已發出命令進度；預設**不傳播**，只在 Hub 與所屬地點 |

「讓專案 Global」會把原本的 System database **拆成 Global database 與新的 System database**，執行地點成為 Hub（日後可更換）。**Global 專案不能轉回標準專案**；單地點 Global 專案對一般使用者行為與標準專案相同。若要以標準專案形式複製結構，可用 `REPLICATE SYSTEM STANDALONE`。

### 37.10.2 網路結構與通訊

> 〔公開版未收錄：AVEVA 官方產品截圖〕兩個地點各有檔案伺服器、基礎產品資料庫與 Daemon，Daemon 之間以通訊連線互連

*圖 37-8　每個地點一個 Daemon，建議與資料庫放在同一台檔案伺服器。（AVEVA 官方文件截圖，僅供內部教學）*

- 通訊網路必須是**樹狀結構**（任兩地點之間路徑唯一），Hub 為根；以父、子、祖先、後代描述關係。連線速度最低支援到 48K。
- **Location Group：** 一群彼此直接連線的地點，可繞過父子路徑縮短傳遞時間；群組有一個 Root（Hub 到群組路徑上的第一個地點），其他成員必須是 Root 的子節點，只有 Root 可有群組外的父節點。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Location Group 示意：Group A 與 Group B，Root 與群組內直接連線以粗線表示

*圖 37-9　Location Group：群組內成員直接相連，群組外仍依父子樹。（AVEVA 官方文件截圖，僅供內部教學）*

- **Off-line Location：** 只與 Hub 以磁帶等媒介傳遞更新（見 37.16.4），Remote 操作不可用。
- **斷線不中斷作業：** 連線中斷時各地點仍可用現有資料工作；恢復後在下次更新自動補齊。更新以 session 為單位，只傳完整 session，通訊中斷造成的不完整 session 不會被採用。

### 37.10.3 資料庫如何被傳播

資料庫逐 session 更新：每次 SaveWork 就在檔尾加一個新 session，Global 比對 **Session Number** 決定誰要更新誰。**注意：Merge 或 Backtrack 壓縮過的資料庫會整份重傳**，所以大型資料庫應使用 Daemon 的遠端合併。使用者在 session 內要 GetWork 才看得到更新。

命令處理是 **non-blocking（非阻斷式）**：Global 中跨地點的命令並行處理，下一個命令可能在上一個完成前就開始，避免長交易卡住使用者；Daemon 本身就像另一位 Admin 使用者，其寫入結果要 **GETWORK** 才看得到，通常需數分鐘。受阻的命令存入該地點的 Transaction database（保證日後執行，但時間不可預測）；少數核心（kernel）命令（如 `ISOLATION`、`LOCK`/`UNLOCK`、`PREVOWNER HUB`，以及衛星端的 `ALLOCATE`、`CHANGE PRIMARY`）改存 pending 檔（見 37.15.3）。

### 37.10.4 哪些檔案會傳、哪些不會

| 類型 | 預設 | 說明 |
|---|---|---|
| 一般資料庫（Propagate Database 勾選） | 傳播 | 建立／修改資料庫視窗可設是否傳播；**不傳播的資料庫仍必須存在於其 Primary 到 Hub 之間所有地點** |
| Transaction database、Working Extract | 不傳播 | Working Extract 只存在於 Satellite |
| Foreign database | 不傳播 | 只能在 Hub 納入，永遠唯讀、沒有 Primary |
| Draw Picture／Neutral Format 檔 | 不傳播 | 通常只需傳專案級 Draw overlay sheet 的圖 |
| **Marine Hull Drawing、Diagram、Stencil、Template** | **強制傳播** | 次要地點無法重新產生，故不論勾選與否都傳；daemon 啟動腳本須設環境變數 `{ABC}DRG`、`{ABC}DIA`、`{ABC}STE`、`{ABC}TPL`（SVG 用 `{ABC}DIA`） |
| Isodraft、外部 PLOT、Design Manager、BRIDGE 檔 | 不傳播 | 另用檔案傳輸（Daemon 可用 `%IMPORT%`、`%EXP_<loc>%` 目錄搬移） |
| Linked documents | 需啟用 | Link Description（`LNDESC`）設 `LNKPRP SEND`、URL 為 `file:///` 且資料夾須存在於目的地；只複製缺少的檔、Allocate／Recover 時一定複製、不做清理 |
| Inter-db macros | 傳播 | 各地點須有 macro 目錄與對應專案環境變數 |

> **專業提醒：** 「**Access 為 Update 的資料庫在傳播時會把使用者鎖在外面**」（SaveWork、GetWork、切模組時看起來像當機）。官方建議 Global 專案只用 Multiwrite 資料庫；否則 Update event 要排在非上班時間。多重寫入資料庫（Extract）在 Global 中的 Claim 模式建議用 **EXPLICIT**，除非所有子項都在同一地點為 Primary。

## 37.11 Global Server 安裝

### 37.11.1 需求

| 項目 | 官方內容 | 備註 |
|---|---|---|
| 位置 | **建議 Daemon 裝在獨立檔案伺服器** | 避免被使用者誤停而漏更新 |
| 硬體與作業系統 | 文件為舊規格（雙核 CPU、1 GB RAM、Windows 7/XP、Server 2008 R2/2003 或更新） | 〔待核對〕12.1 現行需求 |
| 通訊層 | RPC（Windows 內建）或 WCF（需 .NET 4.0 以上） | **兩者擇一，且須與基礎產品安裝一致** |
| 授權 | AVEVA Licensing System（ALS）；Hub 每個專案 Daemon 取一個 `GLOBAL`，Satellite 取 `GLOBALSAT`（無時可借用多餘 `GLOBAL`） | 沒設好時 Daemon 會顯示授權錯誤 |

一個專案在一個地點需要一個 Daemon；任何要跑 Daemon 的機器都要安裝 Global Server。

### 37.11.2 安裝與靜默安裝

```
msiexec /i "C:\Temp\Downloads\baseproduct\Global\Global12.14.msi" /lv "C:\Temp\Downloads\Global12.14.log" /qb- ADDLOCAL=RPC
msiexec /i "...\Global12.14.msi" /lv "...\Global12.14.log" /qb ADDLOCAL=ALL GLOBALMANAGERSERVICEHOST=hostname GLOBALNOTIFICATIONSERVICEHOST=notifyname
```

互動式安裝在「Collaboration Communications Options」畫面選 WCF 或 RPC（只能擇一）。**Global Notifications Service（訊息）與 Scheduler Service（排程）僅 WCF 可用**，需要時須用靜默安裝指定主機。

## 37.12 建立 Global 專案

### 37.12.1 前置作業

標準專案須已存在於將成為 Hub 的地點，專案環境變數已設定，資料夾 `abc000`、`abcmac`、`abcpic`、`abciso` 與應用所需資料夾（Marine 例如 `abcmar`、`abcdrg`）俱在。可在區域網路內完成全部建置再分發。須在建立 Satellite 前把 RHOST 設對（並手動複製到 Global database）。

### 37.12.2 步驟

| 步驟 | 動作 | 要點 |
|---|---|---|
| 1 | Admin 中 `Lock`，通知使用者離開 | 專案內不能有使用者 |
| 2 | `make global`，再 `unlock` | 專案目錄會多出 `projglb` |
| 3 | 離開 Admin 再進入 | 顯示 Hub 尚未初始化；選單列出現 Administering、DAC 與 Isolation 按鈕 |
| 4 | Elements > Locations，選 Hub 按 Modify | 名稱預設 PROJECTHUB、Location ID 預設 HUB（三字元碼）；Hostname 可為主機名、IP 或完整網域名稱 |
| 5 | 設定 Global Extract Range 與 Working Extract Number Range | 資料庫／Extract 編號 1–8191；**在建立 Extract 前先規劃各地點 Working Extract 區間，避免撞號** |
| 6 | Apply，確認 Initialize Hub | Hub 須先有 Transaction database；初始化後 Location ID 與 Hostname 一般不可改 |
| 7 | 設定 transfer 目錄環境變數 `XXX_LOC` | 例如 `set ABC_OXF=...\projects\transfer` |
| 8 | Create Location：填名稱、三字元 ID、Hostname、Parent、Admin Loc | Apply 後把 Hub 上資料庫複製到 transfer 目錄，並建立與配置該地點的 Transaction database |
| 9 | 把 transfer 目錄複製到 Satellite（FTP、DVD 等） | **地點必須依由上到下（先父後子）安裝** |
| 10 | 在 Satellite 設環境並啟動 Daemon，再 `initialize`（Project > Initialize Location） | 以 `/GLOC`、`GETWORK`、`Q ATT` 檢查 `LINIT` 為 TRUE；**Hub 管理者要 GETWORK 才看到** |
| 11 | 設 Primary、Allocate、建 Update event | 見 37.13、37.14 |

官方以 PFB 地點的巨集示範整條流程（節錄）：

```
/*GL
NEW LOC /PFB
LOCID 'PFB'
RHOST 'sg132'
CR DB TRANSACTION/PFB
GENERATE LOCATION PFB NOALLOCATE
ALLOCATE pipeworkarea/fabwork/A PRIMARY AT PFB
```

`NOALLOCATE` 只複製 System DB 檔，`ALLOCATE` 複製所有專案檔；官方以 `savework`／`getwork` 搭配 `pause` 迴圈等待 `LINIT`、`DBALL` 成員數到位，因為 Daemon 的寫入是非同步的。

### 37.12.3 啟動 Daemon

Daemon 可用命令列 `admind start ABC`（WCF 為 `admindWCF`）啟動、`admind stop ABC` 停止；看到 Ready 訊息即運作，Windows 工作管理員可見 `admind` 程序。命令列啟動的缺點是登出就停，所以正式環境應作為**服務**執行：

| 方式 | 指令 | 說明 |
|---|---|---|
| 單一專案服務 | `DemonServiceSingle /install /project ABC /location singleds` | 批次檔 `singleds.bat`；`/location` 是批次檔路徑，不是地點代碼 |
| 多專案服務 | `DemonServiceMulti /install /location <path>\multids` | 增減專案須停服務、改批次檔再啟動；無法單獨停某個專案 |

批次檔須設定：`AVEVA_DESIGN_EXE`（Global 安裝路徑，並在 `PATH` 中）、`AVEVA_DESIGN_WORK`（如 `c:	emp`，遠端 DICE 需要）、各專案變數（Marine：`ABCDRG`、`ABCMAR`、`ABCMAC`、`ABCDIA`、`ABCSTE`、`ABCTPL`）、`USERNAME=SYSTEM`。**服務不繼承使用者的環境變數，也無法對應網路磁碟機**，專案目錄與 Daemon 檔須在本機磁碟；批次檔的 `%1` 不可改成固定 `start`，因為停止服務也用同一檔。

> **專業提醒：** 服務起不來多半是環境變數或網路磁碟機問題：先清空環境後手動執行 `singleds start ABC` 看訊息。同機只能有一個 Daemon；**RPC Daemon 偵測不到 WCF Daemon 已在執行**。

## 37.13 資料庫分配與主要位置

### 37.13.1 規則

- 每個資料庫都**必須存在於 Hub**；Satellite 不需要全部資料庫，但資料庫必須存在於 Hub 到任何需要它的地點之間**所有中間地點**（系統自動分配到中間地點）。
- 分配順序影響更新順序：Dictionary → Properties → Catalogue → Design → Draft；Update Order 視窗的 Automatic re-order 會依此排序，並讓 Extract 的父層先於子層。
- 資料庫在系統內以 `+`（目前地點為 Primary）、`-`（Secondary）、`*`（Foreign）、`>`（傳送中）標示。

> 〔公開版未收錄：AVEVA 官方產品截圖〕三個地點的資料庫配置範例：A 為 Hub 擁有 CATA 與 PIPE 的 Primary，B 擁有 STEEL 與 ISOS，C 擁有 DRAFT

*圖 37-10　三地點範例：+ 表 Primary、- 表 Secondary；B 為中間地點，必須持有 Hub 到 C 路徑上需要的資料庫。（AVEVA 官方文件截圖，僅供內部教學）*

### 37.13.2 操作

| 工作 | 位置 | 要點 |
|---|---|---|
| 確認通訊 | Query > Global States > Communications 或 `PING <loc>` | 先確認兩端 Daemon 都在跑 |
| 分配 | Data > Database Allocation（By Database／By Location） | 大量分配用巨集；分配後 `GETWORK` 並檢查 `DBALL`；**確認 Transaction 中沒有該筆再重做** |
| 設 Primary | Modify Database 的 Primary Loc，或 Database Distribution 視窗 Change Primary Location | 只能在 Hub；舊 Primary 地點使用者離開後才會切換；可預約時間 |
| 取消分配 | 取消分配視窗 | **不能取消 Primary 資料庫**，須先改 Primary；有人讀取則停滯直到離開；不能從 Primary 的父節點取消 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Database Distribution 視窗：每個地點一欄，顯示 + - > * 狀態，下方可改 Primary 地點

*圖 37-11　Database Distribution 視窗總覽各地點的資料庫狀態並可變更 Primary。（AVEVA 官方文件截圖，僅供內部教學）*

分配的內部機制：資料庫先複製到目標與中間地點，Hub 更新 Global database 後再傳給目標，之後才可用，因此有延遲；取消分配則在無讀取者時刪檔，MDB 內的參照自動移除。暫時取消分配（如重新設定資料庫）可勾 **Keep MDBs while de-allocating DBs**。

**變更 Primary 失敗：** 若在 Primary 變更尚未完成時就 Deallocate，會出現 `relocation already in progress`（Transient）。恢復步驟：`RECOVER <db> AT <primary-location> FROM <secondary>` → `PREVOWN <db>` → 重做 `CHANGE PRIMARY` → **等它完成才 DEALLOCATE**。

**更換 Hub：** 僅限命令列（`hublocation OXF`），前提是全部資料庫（含所有 Transaction database）已分配到新 Hub 並已同步，兩端 Daemon 在線、已備份原 Hub 專案與各 Satellite 的 Global database。完成後以 `/*GL` 查詢 `HUBRF` 確認、重新進入 Admin；Hub 恢復動作（Data > Recover > Hub Location）**可能造成兩個 Hub，須極度謹慎**。

## 37.14 更新、同步與傳播

### 37.14.1 Update event

自動更新必須在成對的地點之間建立 **Update event**（父子或同群組，只需建一端）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Update Event 視窗：名稱、更新地點、Frequency 五欄位 Cron 式、Max Retries、Retry Interval、前後 Transfer Script

*圖 37-12　建立 Update event：頻率、重試次數、間隔與前後腳本。（AVEVA 官方文件截圖，僅供內部教學）*

| 設定 | 說明 |
|---|---|
| Name | 少於 32 字元、在專案地點內唯一 |
| Frequency | 五欄位以空白分隔（每日、每小時、每週、每月或組合） |
| Max. Retries／Retry Interval | 1–100 次；1–14400 秒；**Global WCF 下忽略，改用設定檔** |
| Transfer Scripts | 更新前後各一個腳本，收兩個參數：目前地點與遠端地點 ID |
| Suppress Scheduled Updates | 暫停排程（屬性 `LNOUPD`） |

建立或刪除 Update event 最多延遲 15 分鐘生效（Daemon 每 2.5 分鐘檢查 pending 檔，六次後才重讀 System 資料庫），重啟 Daemon 可縮短。排程更新交換兩地點之間所有已分配資料庫；**多個更新不要同時開始**（避免爭用 Global database），例如 AAA-BBB-CCC 鏈每小時更新，AAA-BBB 整點、BBB-CCC 半點。官方建議一般每個工作日約 4 次，關鍵時期可縮到 15 分鐘，並留出時間給合併（例如週日合併）。Global 與 System 資料庫有變更時會盡快傳播，不受 Update event 限制。

### 37.14.2 手動更新與同步

| 操作 | 方向 | 說明 |
|---|---|---|
| Synchronise（Data > Synchronise） | 單向，只接收 | 把目前地點的 Secondary 與 Primary 或指定地點對齊 |
| Update（Data > Update） | 雙向，鄰近地點 | 雙方以較新者為準 |
| Update Direct | 兩個非鄰近地點 | **不建議**：會導致排程更新的 Reverse propagation 錯誤 |

Off-line 地點不可用同步與恢復；遠端版本（Remote 選單）可由 Hub 或管理地點代為執行。

### 37.14.3 Reverse propagation 保護

每次更新會先檢查方向，若發現是從舊資料庫傳向新資料庫，就中止並顯示 `Prevented reverse update`（Secondary 的 session 或標頭頁超過 Primary，error 611）或 `Prevented reverse copying`（NACCNT 超過 Primary，error 612）。判斷依據為 Non-additive Changes Count（`NACCNT`）、Header Changes Count（`HCCNT`）、Claim List Changes Count（`CLCCNT`）與最新 session。System database 用 `STAT /*S`、Global database 用 `GSTAT /*GS` 查詢。解法通常是從 Primary 做 Recover。

> **專業提醒：** 「Secondary 壞了，直接複製 Primary 檔案」可能讓 Secondary 誤認自己是 Primary。官方建議**依序手動更新、每次確認成功再做下一次**；備份還原後也要確認 Secondary 沒有比 Primary 更新的 session，必要時從 Primary Recover。

### 37.14.4 合併（Merge）

資料庫只能在 **Primary 地點**合併；合併會讓 session 消失，Global 失去只傳增量的能力，下次更新整份重傳。因此要用 **Global Merge**（Remote > Global Change Management > Global Merge Changes，或 `REMOTE MERGE`）：先合併 Primary，再自動合併所有 Secondary。合併前須停止排程更新並避免臨時更新，否則可能整檔複製並造成反向傳播；Primary 有使用者在庫內時無法合併；**擁有其他 Extract 的 Extract 不能用 `REMOTE MERGE`**，須把它與所有直接子 Extract 的 Primary 搬到同一地點後在 Admin 手動合併。建議在剛建好專案及重大設定變更後合併 Global 與 System 資料庫；被 Stamp 的 session 視為永久，不會被合併。

## 37.15 運作監控與診斷

### 37.15.1 Command Transactions

> 〔公開版未收錄：AVEVA 官方產品截圖〕Command Transactions 視窗：過濾條件與命令清單

*圖 37-13　Command Transactions 視窗（Utilities > Transactions）：依使用者、模組、命令、狀態與日期篩選。（AVEVA 官方文件截圖，僅供內部教學）*

| 狀態 | 意義 |
|---|---|
| Waiting／Stalled | 等待執行／暫時無法執行（附原因） |
| In Progress | 執行中（重試時會在 In Progress 與 Stalled 之間切換） |
| Complete | 成功完成 |
| Cancelled | 重試中被使用者取消 |
| Redundant | 所依賴的命令已取消，故不必執行 |
| Timed Out | 超過結束時間或重試次數 |

管理員可查看所有使用者與 Local／Remote Daemon、Timed Updates 的命令；右鍵選單可查 Transaction Messages、Flag（預設 `Follow Up`）、Delete Selected（僅限已結束者）、Cancel Selected Commands（**僅限 Waiting 或 Stalled**）。Settings > Transaction Timings 可調 Event Loop（建議 5 秒）、Timeout、Retries；**逾時設太短會讓 Claim 與 Flush 失敗**。Transaction database 可設自動 Merge/Purge，合併前須先停 Daemon。

### 37.15.2 Daemon 診斷

| 類型 | 設定 | 數值 |
|---|---|---|
| Tracing | 環境變數 `DEBUG_ADMIND`（位元相加） | 例：`80` 追蹤 Systems DB 存取與 Event Loop；`896` 適合追蹤命令；`3071` 全部。完整追蹤會很快填滿磁碟 |
| Logging | Daemon > Daemon Settings，填 Diagnostic Logfile 與 Diagnostic Level | 位元相加：1／2 收到摘要／詳細、4／8 傳送、16／32 Dabacon 執行緒、64／128 傳播執行緒、255 全部；Daemon 每 15 分鐘檢查日誌位置 |
| 其他 | `Q REMOTE <loc> BANNER` 查遠端 Daemon 版本；Dabacon buffer 預設 2560000（`GLOBALDAEMON` 模組定義可調） | Daemon 以服務執行時務必設診斷檔 |

### 37.15.3 Pending 檔與常見失敗

Pending 檔位於專案目錄（如 `abc000\pending`），可用 Global 安裝資料夾的 `glbpend.exe <路徑>` 讀取；檔案大小為零代表沒有待處理核心命令。Daemon 命令若無法 Claim Global database 元素（通常是 Admin 仍 Claim 著）就會失敗，包括 Allocate、`initialize`、Set Primary、Change Hub 等。Scheduled update 失敗的代表性錯誤：610 資料庫使用中（通常暫時）、611／612 反向更新／複製、613 Global database 使用中、614 資料庫頁不連續（毀損，須從 Primary Recover）、628 檔案使用中無法覆蓋（保留 `.admnew` 以待後續）、630 因前一個 Extract 失敗而跳過。更新時資料庫檔先複製成 `.admnew` 再提交；有使用者在庫內或有 dead user 且未開 Overwriting 時就無法提交。

## 37.16 恢復、備份與日常維護

### 37.16.1 備份與復原原則

- **備份所有地點的所有檔案**；備份只還原到該地點，必要時才用其他地點備份（工作損失較大）。
- Hub 的 Global database（如 `abcglb`）是**主 Global database**，重大管理作業前先備份；Transaction database 可用 `RENEW` 重建（檔案被刪則 Daemon 啟動會自動重建）。
- **複製 Global 專案**（`REPLICATE`）後，新專案必須有**不同的專案 UUID**，否則 Daemon 無法正常運作；UUID 存於 `/*GL` 的 `ADUUID`，可用 `NEWUID` 產生。

### 37.16.2 資料庫恢復

| 毀損對象 | 作法 |
|---|---|
| Secondary | 從最新的鄰近地點（通常是 Primary）Recover |
| Primary | 工作損失難免；若所有 Secondary 都比備份舊或未同步，從備份還原；若某 Secondary 較新且完好，從該 Secondary 還原 |
| Global database（Satellite 過期） | 先試 `RECOVER GLOBAL AT <loc>`；不行再停 Daemon、通知全員離線、實體複製 Hub 的 Global database、重啟 |
| Transaction database | 停 Daemon →（需要時）Reconfigure 成檔案 → `Renew delete Transaction /ABC` → 啟動 Daemon（自動依 Global database 重建）；**Renew 若未 Reconfigure 會移除執行中的命令** |

### 37.16.3 日常維護與檔案鎖

官方的房屋維護比喻：越早建立例行作業越省力。要點如下：

- **DICE：** 每日對專案內所有資料庫（含完整 Extract family 與 Secondary）跑完整報告；Foreign 專案（如集中式 Catalogue）頻率可較低。修復（patch）模式可修部分問題（如 `Child extract 12 not listed on header page`），其他須 Reconfigure（如名稱表不一致）。大量交付前兩三天要特別仔細；使用者回報 Dabacon 當機時**先 DICE**。Global 還提供 Remote Integrity Checker（Remote > Integrity Checker），**不能用在 Extract 資料庫**。
- **對齊檢查：** 用巨集以 `Q REMOTE <loc> <db> LASTSESSION` 比對各 Secondary 與 Primary 的最新 session。
- **管理作業前（合併、Reconfigure）：** 廣播通知離線 → Lock 專案 → 停 Daemon → Expunge User Process 切斷聯絡不上的人 → Expunge All Users 清 phantom users 並釋放 Claim → 用 pstools 的 `PsFile` 在檔案伺服器找出並關閉被鎖或開啟的資料庫檔。正常以模組 GUI 或 `FINish` 離開，不要直接關閉背景視窗，可減少隨機檔案鎖。
- **Overwrite DB Users（`LCPOVW`）：** 允許以 `.admnew` 覆蓋被鎖檔案，預設關；專案若被其他專案當 Foreign 用，**不要開**（那些讀取者不記錄在本專案的 session 資料中，會導致當機）。
### 37.16.4 Off-line 地點

Off-line 地點在 Generate Location 視窗勾選 Off-line 建立，不需初始化或 Daemon；以 Utilities > Offline Transfer 的 Export／Import Data 搭配 transfer 目錄與媒介更新，**離線地點的 transfer 目錄要保留**。使用 Extract 時整個階層須在該地點同為 Primary 或 Secondary；初始化後不要改為離線。

## 37.17 Extract 與 Global

Extract 從 Multiwrite 資料庫（DESI、PADD、CATA、ISOD，Marine 另有 MANU、SCHE）建立，初始為空、以指標指回主資料庫（Master），本身也是 Multiwrite；不能從 Foreign 或 Copy 資料庫建立。Extract family 最多 10 層、共 8191 個、每個最多 408 個子 Extract，目前只能在樹的最底層新增。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Extract 階層範例：PIPES 為 Master，PIPES_X1、PIPES_X2 為子，PIPES_X10 到 X12 為孫

*圖 37-14　Extract family：Master 與多層子 Extract。（AVEVA 官方文件截圖，僅供內部教學）*

| 概念 | 說明 |
|---|---|
| User claim | 一般 Multiwrite 的使用者鎖，Implicit 或 Explicit；離開模組即解除 |
| Extract claim | 另外的 Extract 層級鎖，**跨 session 持久**；元素被 Claim 到 Extract 後，只有該 Extract 的寫入者才能再做 user claim |
| 指令 | `EXTRACT CLAIM`／`FLUSH` 等；`CLAIM`／`UNCLAIM` 為 user claim |

在衛星端的建構模組中開啟 Extract，其所有父 Extract 都必須分配到該衛星。Global Scheduler可排程 Extract 的 Claim、Issue、Refresh、Flush，建議每小時 Non-transfer、每日一到兩次 Transfer；Marine 專案中 Extract 與 MANU、MDB 的搭配官方只提醒須格外小心，細節〔待核對〕。

## 37.18 WCF 設定與防火牆

### 37.18.1 RPC 與 WCF

RPC 依賴埠 135 與大於 1024 的動態埠，且傳輸綁定支援有限；WCF 的好處是**完全由 XML 設定檔客製**安全層級與埠。啟用 WCF 不改變 Global 的運作方式。基礎產品的 Global 用戶端預設 RPC（E3D 預設 WCF）；**GlobalWCFClient.config 不存在或沒被參照時預設回到 RPC**。

| 設定 | 選項 | 說明 |
|---|---|---|
| 安全模式 | None／Transport／Message | Transport：端到端、一旦驗證即信任、跨超過一個信任邊界不適用、適合內網；Message：每則訊息帶憑證、WS-Security、適合網際網路 |
| 綁定 | `netTcp`、`basicHttp`、`wsHttp` | 同一專案**所有 Daemon 節點須用同一種**（不支援多重端點）；不同專案可各用各的 Global Server 副本與設定 |
| 埠 | 任意（HTTP 預設 8000，未指定則 80） | **每個專案建議獨立埠**；多專案共用 netTcp 埠要 `portSharingEnabled="true"` 並啟動 port-sharing 服務 |

### 37.18.2 設定檔

> 〔公開版未收錄：AVEVA 官方產品截圖〕基礎產品各模組設定檔（adm、des、dra、mar）都指向 GlobalWCFClient.config；Admind 使用 AdmindWCF.exe.config

*圖 37-15　設定檔關係：各模組參照同一份用戶端設定；Daemon 端另有服務設定。（AVEVA 官方文件截圖，僅供內部教學）*

| 檔案 | 用途 |
|---|---|
| `GlobalWCFClient.config` | 用戶端設定（客戶端到 Daemon、Daemon 到 Daemon）；**內容須與基礎產品及 Global Server 兩邊一致** |
| `AdmindWCF.exe.config` | Daemon 服務端安全設定，端點須能接收基礎產品的通訊 |
| `GlobalWCF_SampleConfigFiles` | 範例：NoSecurity／TransportSecurity／MessageSecurity × Windows／Certificate × basicHttp／netTcp／wsHttp |

啟用：在 `GlobalWCFClient.config` 設 `<add key="GLOBAL_PROTOCOL" value="WCF" />`（缺此鍵預設 RPC，改後須重開基礎產品）；Daemon 批次檔 `singleds.bat` 同樣把 `set GLOBAL_PROTOCOL=RPC` 改為 `WCF`。端點的 `baseaddress`（兩個檔都要設）形如 `http://localhost:8000/Design_Time_Addresses/GlobalWcfServiceLib/...`，`Design_Time_Addresses` 於執行時自動換成專案 UUID，其餘不要動；綁定在 Client 與 Service 區塊各改 `binding` 屬性。**請用純文字編輯器編輯，勿用 WordPad。**

### 37.18.3 防火牆

> 〔公開版未收錄：AVEVA 官方產品截圖〕兩個地點各有防火牆，只允許 Global 伺服器之間的 TCP 135 與 5000-5020

*圖 37-16　RPC 跨防火牆：限制動態埠範圍後僅開放 135 與 5000-5020。（AVEVA 官方文件截圖，僅供內部教學）*

| 通訊 | 要開的埠 |
|---|---|
| RPC | TCP 135 加上動態範圍；可用登錄檔限制為例如 5000–5020（`HKLM\Software\Microsoft\Rpc\Internet` 下建 `Ports`（MULTI_SZ）、`PortsInternetAvailable`、`UseInternetPorts`，後兩者為 `Y`），須用 REGEDT32、重開機；值內**不可加冒號**；兩端雙向開放 |
| WCF | 設定檔指定的埠，雙向開放；可把 `AdmindWCF.exe` 設為受信任程式 |

若專案已全面改用 WCF，建議關閉原本給 RPC 用的埠（主要 135）。

### 37.18.4 WCF 疑難排解

| 症狀 | 原因與處理 |
|---|---|
| `(400) Bad Request` | 緩衝太小：加倍 `maxReceivedMessageSize` 與 `maxBufferSize`（後者僅 `basicHttpBinding`；範圍 64 KB 至 4 GB） |
| 資料庫超過約 5000 的龐大專案序列化錯誤 | 調高 `maxItemsInObjectGraph`（預設 65536，上限 2147483647） |
| `The request channel timed out ...` | 網路慢：調大 `sendTimeout` 等（格式 `HH:MM:SS`） |

> **專業提醒：** WCF 模式的 Daemon 啟動較 RPC 慢，首次通訊也有延遲；不要在這幾分鐘內判斷失敗。

## 37.19 系統管理者與二次開發者怎麼接

### 37.19.1 系統管理者

指定一位 Admin Lead 對 Global 備份與恢復負責、每個 Satellite 一位 Co-ordinator；改網路拓樸前先 `PING` 確認 Daemon 在線；例行作業含每日 DICE、對齊檢查巨集、Transaction database 自動清理與 Daemon 日誌輪替。

### 37.19.2 二次開發者

以下語法**皆有官方文件依據**；沒有依據的項目標〔待核對〕。

| 目的 | 官方文件中的寫法 | 備註 |
|---|---|---|
| 在指定資料庫建分段 | `!!HullNewBlock('MYBLOCK','MYTEAM/MYDB')` | 見 37.6.3 |
| 建頂層元素 | `NEW DEPT /MYDEPT DB MYTEAM/MYDB` | 非 BLOCK |
| 查製造包／資料夾 | 屬性 `mpfind`、`mffind` | 回傳型別〔待核對〕 |
| 取板角點／端切點 | `PPOS`、`PPLS`、`PPVI`、`PPCOUNT`、`PDIR` | 索引規則見 37.3.3 |
| 查詢地點狀態 | `LINIT`（Location 屬性）、`Q REMOTE <loc> <db> LASTSESSION`、`Q REMOTE <loc> BANNER` | `LINIT` 為 TRUE 表已初始化 |
| 等待非同步命令 | `savework`／`getwork` 搭配 `pause` 迴圈檢查屬性（官方 PML 範例） | 迴圈中有 `skip` 檔案檢查可中斷 |

分散式環境下的開發原則：

1. **寫入只能在 Primary 地點**；批次工具要先判斷目標資料庫的 Primary。
2. **讀到的資料可能不是最新**；報表前以 `LASTSESSION` 比對，或在報表標註更新時間。
3. **Daemon 是另一位 Admin 使用者**；管理指令結果要 `GETWORK` 才看得到。
4. **只讀明確資料**（blob 內部不公開）；Hull 專屬 PML 物件與方法官方沒有範例，標〔待核對〕，需在訓練專案實測。

## 37.20 常見錯誤彙整

| # | 症狀 | 原因 | 處理 |
|---|---|---|---|
| 1 | 其他使用者看不到 Hull 更新 | 只 Apply 未 SaveWork，或對方未 GetWork | 完整走 Apply → SaveWork → GetWork |
| 2 | 還原單一資料庫後模型錯亂 | 船體參照橫跨多庫 | Revert／Backtrack／Reconfigure 對全部資料庫同做 |
| 3 | 用 Datal 複製船體資料後參照遺失 | Datal 不處理 Hull 參照 | 改用 Copy Assistant |
| 4 | 更新後變慢、整檔重傳 | Merge 破壞增量傳播 | Global Merge、先停排程更新 |
| 5 | 複製 Global 專案後 Daemon 異常 | 專案 UUID 相同 | `NEWUID` 改 `ADUUID` |
| 6 | `Prevented reverse update/copying` | Secondary 比 Primary 新 | 查 `NACCNT`／`HCCNT`；從 Primary Recover |

## 37.21 本章小結

1. 船體資料以 blob 加明確資料並存於 Dabacon；**Apply 是同步點，SaveWork 與 GetWork 決定跨使用者可見性。**
2. 關聯指向最穩定的模型視角；製造包以規則決定零件去向，規則改了要 Resort。
3. 船體資料庫的備份、Reconfigure、Revert、Stamp 一律以**整個專案的所有資料庫**為單位；Datal 與 Undo/Redo 不適用。
4. Global 讓每個資料庫只有一個可寫的 Primary 地點，其他為唯讀 Secondary；Hub 管理 Team、資料庫與地點。
5. **Global 專案不可逆**；建立順序為 make global → 初始化 Hub → 建立位置 → 安裝 Satellite → 分配 → Update event。
6. 所有跨地點命令都是非阻斷且非同步的：看 Command Transactions、GETWORK、Daemon 日誌。
7. Merge 要用 Global Merge 並先停排程更新；WCF 兩端設定必須一致。

## 37.22 練習題與自我檢核

1. 某 Hull 使用者 Apply 完成，舾裝使用者卻看不到。列出所有可能原因與處理順序。
2. 規劃一個三地點（A Hub、B、C）專案，A 做 Catalogue 與管路、B 做鋼結構、C 做圖面。畫出各資料庫的 Primary／Secondary 與中間地點配置，說明 C 為何需要 B 持有哪些資料庫。
3. 製造包規則互相重疊會發生什麼事？有哪兩種處理方式與代價？
4. 為何 Secondary 損毀時不建議直接複製 Primary 檔案？官方建議做法為何？

**自我檢核**

- [ ] 我能說明 Apply、SaveWork、GetWork、Unclaim 各自的作用。
- [ ] 我知道哪些 Dabacon 管理工具不適用船體資料。
- [ ] 我能依序說出建立 Global 專案的步驟並指出不可逆之處。

## 37.23 〔待核對〕項目彙整

1. 船體資料專屬的 Global 配置與分發步驟（官方僅指向 AVEVA Marine Support）。
2. Copy Assistant 的實際操作步驟與功能（官方簡介頁無細節）。
3. Global Server 的硬體與作業系統需求在 12.1 的現行版本（文件寫 Windows XP/2003 時代規格）。
4. 多地點 NSEQ 序號區間的建議數值。
5. Hull 側別、對稱屬性的實際屬性名稱（官方指向附錄，本章未讀附錄）。
6. `mpfind`、`mffind` 回傳型別與 PML 使用方式。
7. Extract 與 MANU、MDB 的 Marine 專屬設定細節。
8. 〈Example Macro for Collecting and Deleting Old Commands〉內容。
9. Hull 專屬 PML 物件／方法；本章僅列官方明文者。

## 37.24 取材範圍

- **Hull Dabacon**（根 ID 1109645）共 98 頁，全部讀完（含兩層以下所有子頁）。圖片預覽 14 張、採用 7 張；其餘（如 Manu 對話框、材料工具視窗）因過小或資訊量低未採用。
- **Global**（根 ID 1105738）共 319 頁：已讀 Global Server Installation（6 頁）、Global User Guide（約 126 頁，Scheduler 與個別視窗欄位僅讀重點）、Global WCF Configuration（約 50 頁）；Running Global Projects（約 135 頁）實際讀了約 60 頁（運作模式、Daemon 與診斷、Merge、Pending 檔、更新與傳播、Reverse Propagation、備份、Extract 概念、防火牆、Housekeeping、Project Setup Guidelines）。
- **未讀或只略讀的子樹：** Running Global Projects 中的 *Transaction Audit Trail*（TRINCO／TROUCO／TROPER，約 40 頁）、Extract 指令語法與 Claim／Flush 失敗原因、*Distributed Extract Hierarchy*、各管理角色、*Recovery from Reverse Propagation Errors*、*Using Global to Distribute Catalogue Data*、*Example Macro*；Global User Guide 的個別視窗欄位與 Global Scheduler 細節僅讀重點；WCF 憑證綁定與各安全模式範例設定檔僅略讀。
- 全章圖片共 16 張，皆已預覽確認後加入（檔名皆以 ch37_ 開頭，存放於 aveva 圖片資料夾）。
