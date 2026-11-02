# 第 45 章　資料庫管理深入：Database Management、SQL Direct 與 Status Control

> 第 3 章講「專案與資料庫的基本概念」，第 33 章講「用 PML 讀寫資料庫」，第 43 章站在系統管理員位置講「安裝、帳號、備份、DICE」。這一章是**深入篇**：把官方 *Database Management* 手冊裡，前面章節只點到為止的機制拆開來講，再加上兩份獨立手冊——**SQL Direct**（用 SQL／ODBC／Excel 讀寫 Marine 資料）與 **Status Control**（模型物件的生命週期狀態管控）。
>
> 對開發者而言：Database Management 解釋「為什麼我改了別人看不到」「Merge 後歷史為何不見」「Extract 為何衝突」；SQL Direct 是**不寫 PML 就能把資料拉進 Excel／Access／報表工具**的官方通道；Status Control 把「核可、發行」做進資料模型，並可由 PML 或 C# 擴充。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件 *Database Management*、*SQL Direct* 與 *Status Control*。SQL Direct 手冊明言「以 AVEVA Plant 撰寫、Marine 客戶同樣可用」，內容以 PDMS 12.0、Windows XP 時代的工具為準，與現行版本的差異標為〔待核對〕。**與其他章的分工：** 資料庫型別、Team／User／MDB、認領與 Session 的基本觀念在[第 3 章](ch03_project_database_zh-TW.reading.html)，元素、識別方式與屬性的基本觀念在[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html)；DICE、備份還原等管理員操作在第 43 章。本章只補機制細節（認領、Extract 運作、Merge 保留規則、Revert 與 Backtrack 的差別、清理指令、NameSeq 等），重複的基本觀念以摘要加連結帶過。Data Model Reference Manual（元素型別與屬性字典）在[第 7 章](ch07_data_model_reference_zh-TW.reading.html)，不在此重複。

## 45.1 學習目標

讀完本章，你應該能夠：

1. 說明 Reference Number（`=db/seq`）、Name 與 Constructed Name 的差異，以及為什麼程式應以 Refno 為穩定識別。
2. 說明 Team、DB、MDB 的多對多關係，以及「Team 決定基本寫入權、MDB 決定這次能看到什麼」。
3. 區分 Primary Hierarchy 與 Secondary Hierarchy（GPSET），並解釋 Pseudo Attribute 與 UDA／UDET 的角色。
4. 說明修改資料庫時系統自動做的檢查（DAC、寫入模式、LOCK、認領），以及 Move／Copy 對 Refno 的影響。
5. 解釋 Savework／Getwork、Session、Stamp、Merge Changes 的運作，並能用 Undo、Backtrack、Revert 選擇正確的「回頭」方式。
6. 說明 Multi-write 的 Claim 與 Extract 的 Issue／Flush／Drop／Refresh，以及 Merge 演算法的衝突規則。
7. 使用 `STATUS`、`SYSTAT`、`Q CLAIMLIST`、`DIFFERENCE`、`REVERT`、`CLEANUP` 與 NameSeq。
8. 說明 SQL Direct 的元件（Configuration、Table Designer、PDMS Provider、PDMS Server），並能設計 Table Schema 把元素屬性映射成表格欄位。
9. 說明以 Excel／ADO／SQL Server 讀寫資料的路徑與限制（不支援 `INSERT`）。
10. 設計 Status Definition，說明 STADEF／STAVAL／STALNK，並用 `STM`、DAC、PML 與 C# 事件控制狀態。

## 45.2 Database Management：資料庫的基本結構

### 45.2.1 專案、DB 型別與編號

官方將專案組成列為：**每個專案各一個 System、Comms、Misc DB**，加上多個 Design、Catalog、Drawing、Dictionary DB 與圖檔。新專案只有前三者，其餘由管理員建立。各 DB 型別（System、Dictionary、Catalog、Model／DESI、Draw 等）存放的內容見[第 3 章](ch03_project_database_zh-TW.reading.html) 3.3 節與[第 1 章](ch01_getting_started_zh-TW.reading.html) 1.3.1 節；本章官方另列出 Property（各種屬性的單位）、SPOOL／MANU／Materials／Diagrams／Schematic／Transaction（管段、生產、船體材料、圖表、PI&D、Global 交易記錄）與 NSEQ（儲存名稱序號，見 45.6）。

每個 DB 有專案內唯一的 **DB number**：使用者 DB 為 1–7000，7000–8000 保留給 AVEVA 提供的 DB，8000–8192 保留給系統 DB；建立時可指定，否則取下一個可用值。所以**從別的專案 Include DB 時，該編號在目標專案必須未使用**。

### 45.2.2 Team 與 MDB

Team 與 MDB 的基本規則（Team 擁有 DB、User 屬於 Team、MDB 決定這次連線看得到哪些 DB）已在[第 3 章](ch03_project_database_zh-TW.reading.html) 3.4、3.5 節說明；官方在此強調的是「DB 屬於**一個** Team，可出現在**多個** MDB」，進入模組時必須指定 MDB。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Team 與 MDB 的關係：World 底下有 Team list 與 MDB list，DB 屬於一個 Team 但可被多個 MDB 引用

*圖 45-1　Team 與 MDB 的多對多關係：DB /B 同時在 MDB /X 與 /Y。（AVEVA 官方文件截圖，僅供內部教學）*

- 從**其他專案 Include 進來的 DB 一律唯讀**，不論 Team（Team 決定基本寫入權的規則見[第 3 章](ch03_project_database_zh-TW.reading.html) 3.4 節）。
- 拆成多個 DB 的理由（官方）：以 DB 為存取控制單位、降低多寫入者競爭、Global 按 DB 決定可寫地點、可對外包隱藏 DB。

### 45.2.3 元素、Refno、Name

資料庫（Dabacon）的所有資料都存為**元素**；元素型別決定可用屬性，每種 DB 型別允許的元素型別不同。三種識別方式的入門比較見[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html) 4.4 節，下表是 12.1 官方文件的完整規則。

| 識別方式 | 規則 | 穩定性 |
|---|---|---|
| Reference Number | 兩個 32 位元整數，顯示如 `=1234/6789`；第一個編碼 DB 編號（`Q DBNUMBER`），第二個是從 0 起、每建一個元素加一的序號；建立後**永不改變**；刪除後**不重用** | 最穩定 |
| Name | 以 `/` 開頭，可改名；Design／MANU／SCHE／ENGI 型 DB 在同一 MDB 內名稱可重複（不同 DB 可各有 `/FRED`） | 可變 |
| Constructed Name | 無名元素由「相對位置至第一個有名祖先」組成，如 `BOX 2 OF SUBEQUIPMENT 1 OF /VESS1` | 最不穩定（成員順序會變） |

> **專業提醒：** 官方明說名稱區分大小寫（`/FRED` 找不到 `/fred`），建議全用大寫。程式與外部系統要記住物件時，存 Refno，不要存 Name。

### 45.2.4 階層、屬性與規則

- **Primary Hierarchy：** 一個元素在主階層只存在一次。結構由 AVEVA 固定，但可用 **UDET**（User Defined Element Type）以既有型別為基礎自訂，例如以 Equipment 為基礎的 `:PUMP`，並可限縮允許的成員／擁有者；以 Zone 為基礎的 UDET 還可擁有其他 UDET。
- **Secondary Hierarchy：** 如 Group Set（GPSET），同一元素可再出現在群組裡。多數指令可作用於次階層（把 `/GPSET1` 加到 3D 視圖等同加入其成員），但**刪除 GPSET 不會刪成員**；與主階層不同，次階層可跨 DB。Shared Collection 由 GPWL → GPSET → GPITEM 組成，可用 `GADD`／`GREMOVE` 增減成員，也可對 GPSET 的 `SCOSEL` 屬性設定動態選取式（例如 `ALL PIPE WHERE (BORE GT 80)`，每次使用時動態計算，有效能代價）。
- **屬性、UDA 與 Pseudo Attribute：** 所有元素都有 `NAME`、`TYPE`、`LOCK`、`OWNER`、`MEMBERS`；`Ref` 型屬性是指向其他元素的指標（如 BRANCH 的 `CREF` 指向連接的 NOZZLE），是網路與交叉關係的基礎。UDA 可為任何元素型別（含 UDET）加使用者屬性，已存在的元素也立即生效；Pseudo Attribute 在查詢時才計算，一般不能直接設值。屬性型別與分類見[第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html) 4.5 節，12.1 的資料型別、偽屬性與 UDA 條目見[第 7 章](ch07_data_model_reference_zh-TW.reading.html) 7.3、7.5、7.6 節。
- **Expression 與 Rule：** 資料庫運算式支援代數、布林、文字、ID、位置、方向、方位，用 `OF` 指涉其他元素（`(PURP EQ 'HS' AND AREA OF OWNER EQ 1)`）；與 PML 運算式相似，但**不能含 PML 變數或函式**（`(XLEN * !MYVAR)` 無效）。Rule 把屬性值定義成運算式（如 `XLEN` 為 `(YLEN * 2)`），結果存回屬性；**靜態** Rule 只在要求時重算，**動態** Rule 於相關屬性改變時自動重算，且可跨元素、跨 DB。

> **動態 Rule 可能不傳播**（官方列舉）：目標元素所在 DB 不在 MDB 中、DB 唯讀、無法認領、元素被 LOCK、或被 DAC 擋住。因此另有指令可驗證 Rule 結果是否最新。

### 45.2.5 匯出資料庫：DATAL 與 Reconfigurer

**Data Listing（DATAL）** 把資料狀態（所有屬性、UDA、Rule）輸出成可回讀的指令檔，用於長期封存與跨專案複製部分資料；**Reconfigurer** 輸出二進位（最快）或文字檔，搬移整個 DB 或 World 層元素時建議使用，較低層元素用 DATAL 或 Copy。

## 45.3 修改資料庫：自動檢查、指令與 DAC

### 45.3.1 修改前的共同檢查

任何修改都先經過：存取控制（DAC）、DB 是否以寫入模式開啟、元素的 `LOCK` 是否為 false；若為 Multi-write DB，還要做認領檢查並視需要自動認領。**完整性檢查在資料庫介面之下執行**，所以不論用 PML 或 C# 修改都安全（例如 `OBST` 只能設 0、1、2）。

### 45.3.2 五種基本修改

| 操作 | 規則 |
|---|---|
| Create | 一次一個，只能建在合法的階層位置；自動配發唯一 Refno，預設值可能由擁有者往下繼承；特殊情況可指定 Refno（例如重建一份完全相同的 DB 以維持跨 DB 參照），**不建議一般使用** |
| Delete | 其下整個主階層子孫一併刪除；Refno 不重用 |
| Copy | 可複製單一元素或含子孫；可跨 DB；完全在複製結構內的參照會改指新元素；一律複製到**同型別**既有元素之上；可改名、可選擇是否重跑 Rule |
| Move | 元素與子孫一起搬；**搬到不同 DB 時 Refno 會改變**，指向它的 Ref 屬性會自動更新 |
| Modify attribute | 檢查值型別與屬性對該元素是否有效 |

交叉參照屬性的完整性會被維護：改變連接一端時，舊連接另一端的屬性會被清空，新連接對象若原本已連接也會被清空，**一次修改最多更新四個元素**。

### 45.3.3 指令語法（官方 Database Modification 章）

| 目的 | 語法 |
|---|---|
| 建立（接在目前清單位置之後） | `NEW element_type [name]` |
| 指定位置 | `NEW TEE AFTER /ELBO3`、`NEW TEE BEFORE 8`、`NEW TEE AFTER LAST ELBO` |
| 指定在特定 DB 建頂層元素 | `NEW SITE /MYSITE DB MYTEAM/MYDB` |
| 刪除目前元素 | `DELETE element_type`（兩行指令：先導覽，再刪，且須確認型別；刪除後 Owner 成為 CE） |
| 刪除成員 | `DELETE BRAN MEMBERS 5 TO 7` |
| 重排成員 | `REORDER /ELBO3 BEFORE FIRST ELBO` |
| 搬入既有元素（改 Owner） | `INCLUDE /PIPE2` |
| 複製（先 `NEW EQUI /EQUIPB`） | `COPY /EQUIPA`、`COPY MEMBERS 12 TO 20 OF /MAINLINE`、`COPY ATTRIBUTES OF`、`COPY LIKE`、`... RENAME /FRACT1 /FRACT2` |

`COPY` 不複製 `NAME` 與 `LOCK`；CE 已有成員時不能這樣複製；不加 `RENAME` 則新元素無名；`COPY ATTRIBUTES` 不複製對 DESI 的參照與 OWNER，`COPY LIKE` 另外不複製位置、方向、方位與角度。

> **專業提醒：** DAC 相關 Pseudo Attribute（`DACCRE`、`DACDEL`、`DACCOP`、`MODATT`、`MODDEL`、`DACERR`）可在動手**前**查詢操作是否被允許，開發工具應先查。

### 45.3.4 DAC：ACR、Role、Scope、PEROP

第 43 章已介紹 DAC 的用途；這裡補官方的結構。基本存取控制是 Team Owning Databases；細粒度的是 **ACR**（Access Control Rights）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕DAC 階層：User 擁有 ACR，ACR 由 Scope 與 Role 組成，Role 包含 Perop

*圖 45-2　DAC 資料庫階層：User → ACR → Scope／Role → PEROP。（AVEVA 官方文件截圖，僅供內部教學）*

- **ROLE** 是一組 **PEROP**（Permissible Operation）；**SCOPE** 指出 Role 適用範圍，可為運算式（如 `all ZONE WHERE (FUNC eq 'TEAMA')`）。PEROP 含適用元素、操作（Create、Modify、Delete、Claim、Issue、Drop、Output、Export、Copy，各設 Allow／Disallow／Ignore）、可選的屬性清單、限定條件與拒絕訊息。
- 取得更新權須：Role 中至少一個 PEROP 允許，**且沒有任何 PEROP 明確拒絕**。

## 45.4 Session、Savework 與「回頭」：Stamp、Merge、Undo、Backtrack、Revert

### 45.4.1 Savework／Getwork 與 Session

三個動作的基本概念與快照隔離見[第 3 章](ch03_project_database_zh-TW.reading.html) 3.7 節，以下補官方的運作細節。資料只在要求時寫入，也只在要求時看到別人的變更：寫的人要 `SAVEWORK`，讀的人要 `GETWORK`。每次 Savework 在 DB 檔**尾端附加**一個新 Session（與前一 Session 的差異 delta，含日期、使用者、描述），DB 標頭指向最後一個 Session；**Session 一旦寫入就永不更改**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕DB 在 19 個 Session 與 39 個 Session 之後，標頭指標指向最新 Session

*圖 45-3　Session 以附加方式累積；你看的是 Session 19，就不會看到別人後來寫的內容，直到 Getwork 把你帶到最新（例如 Session 39）。（AVEVA 官方文件截圖，僅供內部教學）*

| 指令 | 說明 |
|---|---|
| `SAVEWORK 'comment' [n]` | 不離開模組即存檔；`n` 是 `STATUS` 輸出順序中的 DB 序號，省略則整個 MDB |
| `GETWORK [n]` | 更新所有唯讀 DB 的視圖；官方提醒會使後續讀取變慢（需重新讀磁碟），應節制使用 |
| `SESSION COMMENT 'text'` | 設定目前 Session 註解，可 `Q SESSComment integer` 查詢 |

Session 1、2 在 ADMIN 建立 DB 與 World 時產生，第一個使用者 Session 是 3。

### 45.4.2 Session 歷史與比較

- `DIFF`（`DIFFERENCE`）：報告變更。預設比較自上次 Savework 以來；可指定 `SINCE` 日期時間、`SESSION nn`、`LATEST`、`EXTRACT`。輸出列出建立、刪除與各屬性的舊／新值。注意比較的是**Savework 之間的狀態**。
- 查詢：`Q LASTMOD`／`SESSMOD`／`USERMOD`、`Q HISTORY DIAM`（**最多 120 個** Session）、`Q SESSCOMM／SESSUSER／SESSDATE 58`、`Q SESSION ON <日期>`。
- **Comparison Date**：`SETCOMPDATE <日期>`、`SETCOMPDATE STAMP /STAMP1`、`SETCOMPDATE NOW`、`SETCOMPDATE FOR <DB> TO SESSION 99／EXTRACT`；之後可用 `OLD` 查舊值（`Q OLD XLEN`）。
- Marine／E3D 的 **Model Changes** 視窗（Manage → History）有 Model Timeline、Stamps、Element History 窗格：`All Changes Since` 顯示某 Session／Stamp 後到目前（含未存檔）的變更，`Only Changes At` 只顯示該 Session 的變更，並可在 3D 視圖高亮；任何變更或 Savework／Getwork 後需重按 Refresh。

### 45.4.3 Stamp 與 Merge Changes

**Stamp** 標記一組 DB 的里程碑，只能在 **Admin** 建立。DB 會因保存全部變更而成長較快，可用 Admin 的 `MERGE CHANGES` 把多個 Session 併成一個（可全部或指定範圍）。保留規則：

- 被 Stamp 使用的 Session **一定保留**；
- Session **1、2 與最後一個 Session** 一定保留；
- 因此**壓縮前要先為需要的比較點建立 Stamp**。

官方範例：Session 10 有 Stamp，Merge 後保留 1、2、10、39，其中 10 含 3–10 的累積變更，39 含 11–39 的累積變更。

> **專業提醒：** 對有 Extract 的 DB 做 `MERGE CHANGES` 不應輕率：所有下層 Extract 都要調整，被子 Extract 連結的 Session 會保留，且下層 Extract 上**不可有使用者**；官方建議由下而上。Global 下須所有下層 Extract 都在本地為 Primary。

### 45.4.4 四種「回頭」方式的比較

| 方式 | 範圍 | 是否永久刪資料 | 可否跨 Savework | 備註 |
|---|---|---|---|---|
| `MARKDB` / `UNDODB` / `REDODB` | 目前 Session 內的交易（以 micro session 實作） | 否 | **否**；Savework 或 Getwork 後 Undo 堆疊清空 | 第一次修改資料庫時自動建立初始標記；`UNDODB n` 可退多步；Undo 後再改資料，Redo 堆疊作廢；標記清單可由 PML 的 `MARKDB` 取得 |
| `REVERT <element/hierarchy> AT/BEFORE <時間／Session／STAMP／EXTRACT>` | 單一元素或階層 | 否（產生新變更） | 是 | 先驗證每個建立、Include、Reorder、刪除與屬性變更都被允許；任一失敗（合法性、唯讀、DAC）則**整個取消**並報錯 `(43,615)`；原本未鎖的元素不被 LOCK 擋 |
| `REVERT <database name> TO ...`（Admin、命令列） | 整個 DB | 否 | 是 | 新增一個 Session（如 137）宣告忽略 135、136，視圖等同回到 134；舊 Session 仍在 |
| `BACKTRACK <database name> TO <session／stamp／時間>`（Admin、命令列） | 整個 DB | **是，永久且不可逆** | 是 | 例如回到 134，則 135、136 永久刪除；此功能僅限管理員 |

> **專業提醒：** 與第 43 章「Backtrack 不是備份」同一主題：能用 `REVERT` 就不要 `BACKTRACK`，且先做完整備份。

## 45.5 Multi-write、Claim 與 Extract

### 45.5.1 Multi-write 的兩種技術

認領的動機與顯式／隱式模式見[第 3 章](ch03_project_database_zh-TW.reading.html) 3.6 節。UPDATE DB 同時只允許一人寫入，MULTIWRITE DB 允許多人同時寫入，靠兩種機制：

1. **Claim（認領）**：修改時認領元素，鎖住別人。**粒度是 Primary 元素**（如 SITE、ZONE、EQUI、SUBE），修改 `BOX` 這種非 Primary 元素時要認領其往上第一個 Primary 元素。可顯式認領，也可由系統在修改時隱式認領。
2. **Last Back Wins**：不用鎖，於屬性層級合併，同一屬性衝突時最後存檔者勝。適用：部分連接屬性（改 BRANCH 的 `TREF` 不必認領）、含 Primary 元素的成員清單（在 SITE 下建 ZONE 不必認領 SITE）、變體（Variant）Extract 的發回、動態 Rule 連動、空間地圖值。

### 45.5.2 認領指令與限制

| 指令 | 說明 |
|---|---|
| `CLAIM /ZoneA /EQUIP100`、`CLAIM /ZoneA HIERARCHY` | 認領指定元素（可含整個階層）；認領非 Primary 元素會認領其 Primary 上層 |
| `UNCLAIM /PIPE-100`、`UNCLAIM ALL` | 釋放；離開模組或切換模組時自動釋放 |

- 無法認領的原因：被其他使用者或 Extract 認領；自上次 Getwork／Savework 後已被修改（要先 `GETWORK`）。
- 有未存變更不能釋放（先 `SAVEWORK`）；**要刪除元素，該元素與其整個子階層都須已認領**。
- 清單中部分失敗時，其餘仍會處理；每次認領／釋放都會存取底層 DB，所以**盡量一次處理多個元素**。
- 到 Savework／Getwork 才會發現的衝突：兩人同名（第二位必須改名）、一人在 `/PIPE1` 下插入 Primary 元素而另一人刪了 `/PIPE1`（要搬走或刪除，或放棄刪除）。任何錯誤，**整個操作中止**。
- 相關屬性：`DBAC`（`CONTROL`／`UPDATE`／`MULTIWRITE`）、`DBCL`（`EXPLICIT`／`IMPLICIT`）、`LCLM`、`USERC`、`EXTRC`、`CLMNUM`（Extract 編號為負值）；DAC 對應 `DACCLA`、`DACISS`。

### 45.5.3 Extract 的家族與 Session

Extract 是 Multi-write 的延伸，從既有 Multi-write DB 產生（該 DB 成為 **Master**）。第 3 章用「Git 分支」比喻；這裡補官方細節：

- 能力：長期認領（切換模組不釋放）、發回與 Savework 分離、部分發回／捨棄、變體、私人工作區，並可搭配 DAC 實作核可週期。
- 一個 Extract 家族最多 **8000** 個 Extract；可從 Extract 再建 Extract；同一家族的兩個 Extract 不可放入同一 MDB。
- 限制：不能 `COPY` Extract；Exclude 前須先 Exclude 所有子 Extract。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Extract 家族：Master DB 底下三個 Extract，Extract1 底下再有兩個 Extract

*圖 45-4　Extract 家族：Master DB 下有三個 Extract，Extract1 下再有兩個。（AVEVA 官方文件截圖，僅供內部教學）*

Extract 有自己的一串 Session，是從 Master 某 Session（官方例：19）分支出來；未更動的資料透過指標回讀 Master。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Extract 從 Master 的 Session 19 分支，擁有自己的 Session 1 到 10

*圖 45-5　Extract 從 Master 的 Session 19 分支並累積自己的 Session。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.5.4 Extract 操作

| 指令 | 效果 |
|---|---|
| `EXTRACT CLAIM ...` | 認領到 Extract；可用運算式選取（`EXTRACT CLAIM ALL STRU WHERE (:OWNER EQ 'USERA') HIERARCHY`）。Extract 認領**跨 Savework 保留**，且會逐層往上自動認領 |
| `EXTRACT FLUSH` | 把變更寫回父 Extract，**保留** Extract 認領（Issue 但不 Release） |
| `EXTRACT ISSUE` | 寫回並**釋放** Extract 認領 |
| `EXTRACT RELEASE` | 釋放（僅限已 Flush 的變更；有未決更新、或被使用者／下層 Extract 認領時不可） |
| `EXTRACT DROP` | 捨棄尚未 Flush／Issue 的本地變更（須先 Unclaim 自己的認領） |
| `EXTRACT REFRESH` | 以父 Extract 的變更更新自己，等同單一 DB 中的 Getwork；可一個指令往上全部 Refresh |
| `EXTRACT FLUSH RESET` | Global 環境 Flush 失敗後，通知子 Extract 重設比較基準 |

`FLUSHWithoutrefresh` 另有一個關鍵字；語法圖為 `EXTRACT {FLUSH|FLUSHW|RELEASE|ISSUE|DROP|REFRESH} [element... [HIERARCHY] | DB dbname]`。Flush、Issue、Release、Drop 只作用一層，Refresh 可跨層；標準 Flush／Issue 同時會做 Refresh，確保下次操作有合適的基準 Session。每次 Flush 都建立一個新 Session，**一次 Flush 很多元素比逐個 Flush 好**。

**部分操作的額外檢查：** 非 Primary 元素換了 Owner 時，新舊 Primary Owner 須同時發回；建立的元素與其 Owner、刪除的元素與其 Owner 須一起處理。部分 Issue／Drop 後**不保證工程正確**，官方建議跑 Clasher 或 Datacon。

### 45.5.5 Merge 演算法與 Variant

發回時，Extract 的變更以屬性層級套用到父 Extract：**不同屬性可合併，同一屬性則最後送回者勝**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕合併的三個 Session：Base Session 與 From Session 比較，差異套用到 To Session

*圖 45-6　合併演算法：比較 Base Session 與 From Session，把差異套用到 To Session；Savework／Getwork 使用同一演算法。（AVEVA 官方文件截圖，僅供內部教學）*

兩個例外：**元素一旦被刪就一直是刪除**（使用者 1 刪 `/BOX` 先發回，使用者 2 的屬性修改無效）；**元素型別被改變時改以元素層級合併**，其他人的屬性變更會遺失。系統保證合併後在原始資料庫層級是 DICE 乾淨的，但**無法保證工程一致性**，因此變體資料發回後應跑 DATACON 與 Clasher。

**Variant** 是不做 Extract 認領的 Extract：多人可在不同變體同時改同一元素，但衝突到 Flush 才發現。

### 45.5.6 Global 環境（概要）

Global 把 DB 分散於不同地點，由 daemon 傳播新 Session；同一 DB 只有一份可寫（Primary），其餘為 Secondary；跨地點的 Extract Claim 與 Flush 為**非同步**。細節見 [第 46 章](ch46_dabacon_global_zh-TW.reading.html)。

### 45.5.7 常用查詢指令

| 指令 | 用途 |
|---|---|
| `STATUS [INFO]` | 目前使用者、Team、MDB 與目前／延後（Deferred）DB 及其 R／RW 模式；`INFO` 會說明存取模式與預期不同的原因 |
| `SYSTAT` | 專案內所有使用者、模組、MDB 與 DB 模式（唯讀／讀寫）與工作站 |
| `Q DBNAME／DBTYPE／DBFNUMBER／DBFILE` | 目前 DB 的名稱、型別、檔案編號與路徑 |
| `Q CLAIMLIST [OTHER／EXTRACT [FREE／OTHER]] [DB name]` | 自己、他人或 Extract 的認領清單；`CLAIMLIST EXTRACT` 告訴你能 Flush 什麼，`OTHER` 告訴你不能認領什麼 |

### 45.5.8 Inter-DB 連接巨集

連接他 Team 唯讀 DB 時，系統自動產生 **inter-DB connection macro**（如 `abc001.mac`，存於 `ABCMAC`），由有寫入權者在 Model 以 `$M /%ABCMAC%/abc001.mac` 執行，再 `DELETE MACRO 1`。執行前，發起者的一致性檢查會出現「incompatible connection reference」。

## 45.6 清理、序號、文件連結與分散屬性

### 45.6.1 `CLEANUP`：清除失效參照

用邏輯屬性判斷參照狀態：`NULLREF`（為 `=0/0`）、`UNRESOLVED`（指向無法確認存在的元素，可能是 DB 不在 MDB）、`INVREF`（指向不存在的元素，且應容納它的 DB 已在 MDB 中）。語法：

```text
CLEANUP NULLREF | INVALID | UNRESOLVED attribute [ON noun] [FOR ele] [SETNULL | DELETE]
CLEANU NULL STLREF ON EQUI DELETE          -- 刪除 STLREF 為 null 的 EQUI
CLEANU UNRES CATREF FOR /PIPES SETNULL     -- 把 /PIPES 階層下無法解析的 CATREF 設為 null
```

> **專業提醒：** `DELETE` 會刪元素，`SETNULL` 只清參照；先以 `Q NULLRE (ATTNAME att)` 確認範圍，備份後再執行。

### 45.6.2 NameSeq：並行環境的唯一名稱

NameSeq 用獨立的 **NSEQ 型 DB**（覆寫型）儲存序號，由 Admin 建立並如一般 DB 加入 MDB；序號元素受保護，不可手動編輯，主要透過 PML 的 `NameSeq` 物件使用。

```text
import 'aveva.model.nameseq'
using namespace 'aveva.model.nameseq'
!seq = object NameSeq('TEST')
!seq.SetStart(1000)
q var !seq.next()        -- TEST1001
```

常用方法：`NameSeq(string)`（不存在則建立）、`Next()`、`SetStart`（預設 0）／`SetMax`（預設 2147483647）／`SetStep`（預設 1）、`SetWraparound()`／`SetNoWraparound()`（到最大值後繞回或報錯）、`GetCurrent()`、`ReStart`、`Remove()`。

**Global 專案：** NSEQ DB 各地點區域性、**不複製**，各地點應用 `SetStart()` 設定不同起始值以維持名稱唯一。

### 45.6.3 Link Documents 與 Distributed Attributes（概要）

- **Link Documents：** 以 Link Descriptor（`LNDESC`，含說明與 URL）把資料庫元素連到外部檔案、網頁或內部圖面（URL 例：`file:///…`、`dabref://=12345/6789`、`http://…`），階層為 `LINKWL` → `LNFOLD` → `LNDESC`，並可用 `LNCLAS` 分類，做到「找出所有被分類為 Installation 的文件」或「沒有 Certificate 文件的泵」。外部文件不存於 Dabacon DB。
- **Distributed Attributes：** 把物件的屬性群組（以 `XPITEM` 為基礎的 UDET）分散到不同階層與 DB，改善並行與認領粒度；由 Lexicon 維護。〔設定細節未讀。〕

## 45.7 SQL Direct：用 SQL 與 Office 讀寫 Marine 資料

### 45.7.1 它是什麼

**SQL Direct** 讓支援 Microsoft Universal Data Access（ODBC、OLE DB、ADO）的軟體，直接存取 Design 資料庫：Word、Excel、Access、Oracle、Sybase、用 Visual Basic／Visual C++ 寫的程式、Crystal Reports 等。可查詢 DESIGN 模組能存取的**一切資料：屬性、Pseudo Attribute 與 UDA**。官方明言手冊用 Plant 撰寫，Marine 客戶同樣適用，且**不需要 SQL Server 也能讀**；SQL Server（或 MSDE）是選配，用來做更複雜的 SQL、與其他資料來源 Join，並可寫回。

> 〔公開版未收錄：AVEVA 官方產品截圖〕SQL Direct 架構：資料消費端經 PDMS Provider、PDMS Server 到 PDMS 與 DESI 資料庫，TableSchema.tsf 與 ProjectSchema 由 Configuration 與 Table Designer 管理

*圖 45-7　SQL Direct 元件與資料流：Excel／Access／SQL Server → PDMSProv OLE DB Provider → PDMSServer.exe → PDMS Design → DESI 資料庫。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 每次查詢都由 PDMS Server 透過 PDMS 本身取資料，所以仍受登入使用者的存取權、MDB 與 Session 視圖影響。大量離線分析未必比 PML 報表合適；讓非程式人員以 Excel 取數則很實用。

### 45.7.2 元件與角色

| 元件 | 角色 |
|---|---|
| SQL Direct Configuration | 設定連線資訊（專案、MDB、環境變數、Table Schema 檔），並可從 Tools 選單啟動 Table Designer、啟停 PDMS Server 與 SQL Server、**Configure SQL Server**（建立與 Table Schema 一致的資料檢視） |
| Table Designer | 設計「哪些元素型別的哪些屬性要變成哪些表格欄位」，存成 `.tsf` |
| PDMS Provider（`PDMSProv OLE DB Provider`） | 日常運作的 OLE DB 資料提供者，依需求組成 rowset |
| PDMS Server | 負責所有與 PDMS 之間的資料存取；由 Provider 與 Table Designer 自動啟動 |

**登入：** 用一般 PDMS 帳號與密碼，存取權依該使用者的權限而定。連線需三項資訊：連線字串（Connection String）、使用者名稱、密碼；缺少時 PDMS Server 會跳出登入表單。官方警告：**把密碼留在用戶端快取會降低資料安全**。

**共用 PC：** SQL Direct 是**單一使用者**工具，登入後同一階段不能換使用者或連線字串（否則 access denied）。換身分前先關 PDMS Server：Tools 選單、關閉 PDMS Command Line 視窗，或執行 `<SQL Direct 安裝路徑>PDMS Server /STOP`。

### 45.7.3 設定連線（Connection Properties）

> 〔公開版未收錄：AVEVA 官方產品截圖〕PDMS Connection Properties：Connection String、Standard Variables、Project Details 與 Database Variables

*圖 45-8　PDMS Connection Properties 表單：以連線字串識別一組專案／MDB／環境變數設定。（AVEVA 官方文件截圖，僅供內部教學）*

| 欄位 | 內容（皆為必填） |
|---|---|
| Connection String | 這組設定的唯一識別；用戶端設定 Provider 連結時要引用的字串 |
| Standard Variables | `PDMSEXE`（安裝目錄）、`PDMSWK`（工作目錄）、`PDMSUI`（PML 表單與程式）、`PMLLIB`（通用 PML） |
| Project Details | Project Name、MDB、**Table Schema**（`.tsf` 檔位置） |
| Database Variables | 專案資料庫目錄變數（如專案 `SAM` 對應 `SAM000`、`SAMMAC`；PIC、ISO 欄位為未來使用可留空） |
| More Env Vars | 一個檔案，每行 `SET <varName>=<value>`，定義額外環境變數（如外部 DB 位置） |

`Test Connection` 會啟動 ADOTest（ADO 用戶端）測試。

### 45.7.4 Table Designer：把屬性映射成表格

**名詞：**

| 術語 | 定義 |
|---|---|
| Project Schema file | 列出專案所有元素型別與屬性；因 UDA 各專案不同，所以按專案產生（`Schema > Generate Project Schema`）；一份可供多個 Table Schema 使用 |
| Table Schema file（`.tsf`） | 描述用來取資料的表格；不同報表領域可有不同 Schema |
| Table | 邏輯群組；由 Column（屬性值）與 Row（元素型別）組成 |
| Table row | 一個元素型別與每一欄的 Binding |
| Binding | 欄位與元素屬性的映射 |
| Key column | 唯一識別物件的欄；**必須先有 Key column 才能將其他欄設為可寫**；實務上只能用 `REFNO` 或 `NAME`（建議 `REFNO`），Key 欄一律唯讀 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕SQL-Direct Table Designer：左側為表格與欄位樹，右側為 Rows of 與各欄屬性綁定

*圖 45-9　Table Designer：左側表格樹（如 STRUCTURAL_ITEM 的 REFNO、OWNER、TYPE、NAME），右側為元素型別（sctn）與欄位綁定。（AVEVA 官方文件截圖，僅供內部教學）*

**步驟：**

1. 產生 Project Schema（若尚無）。
2. `File > New` 並選 Project Schema，`Insert > Table` 新增表格（預設名 `NEWTABLE`，建議改成 `SITES`、`PIPING` 之類；表格名只能用字母、數字、底線，**不能有空白**；欄名可含空白）。
3. `Insert > Column`（新欄插在目前選取欄的右邊，若選表格名則成第一欄）；欄名若恰為屬性名（如 `REFNO`），Designer 自動綁定。
4. `Insert > Row`，在 `Rows of` 下拉選元素型別；欄位若顯示 `unset`，雙擊選屬性。新增列時 Designer 會沿用上一列的綁定，所以**先把第一列做對再加其他列**。
5. 要寫回資料：設定 Key column（`Schema > Key Column`），再對欲開放寫入的欄取消 `Read Only`。官方提醒：**寫入是否合理由設計者負責，Designer 不強制任何唯讀規則**。
6. 檢查：`Check Selected Table`、`Check Table Schema`（檢查每個表至少一列一欄、每個交叉點有有效綁定；「有效」僅指屬性屬於該型別，不代表語意合理）；狀態列的笑臉顯示檢查結果（笑／哭／未決）。使用中的 Schema 若有錯誤，**不能存回同一檔**。
7. 存成 `.tsf`，回 SQL Direct Configuration，把檔案設進連線設定才生效。
8. 欄位資料型別可選 `STRING`（預設，長度預設 22）、`INTEGER`、`REAL`；Table Schema 以絕對或相對路徑引用 Project Schema（一份集中的 Project Schema 配分散的 Table Schema 用 Absolute，一起散布用 Relative，需先存檔一次）。

### 45.7.5 讀取範例（不需要 SQL Server）

**Excel：** `Data > Import External Data > Import Data…` → New Source → **Other/Advanced** → **PDMSProv OLE DB Provider 12.0**，`Data Source` 填連線字串，輸入使用者名稱與密碼（取消 Blank Password），選表格並存成連線檔。

- Excel 內改資料**不會寫回 PDMS**；資料在 PDMS 修改並 `SAVEWORK` 後，用 `Refresh Data` 取得更新；存檔後 Refresh 失敗多半因密碼預設不存，到 `Edit Query…` 補 `Password=<password>;`。

**ADO／Visual Basic：** 範例程式 `ADOTEST`（位於 `C:\AVEVA\SQL-Direct12.0\Samples`，需 VB6 的 `MSVBVM60.DLL`）示範以 ADO Connection／Recordset 列出表格、顯示於格線。可寫欄位為白底，唯讀為灰底；在 Cell Text 編輯、按 `Update Cell`，**要到關閉連線（`PDMS > Close Connection`）時才詢問是否提交**：Yes 提交到 PDMS，No 放棄。

### 45.7.6 搭配 SQL Server：真正的 SQL

需要較複雜的 SQL 查詢，或與其他 Provider 的資料 Join 時，需要 SQL Server（SQL Server Express 或更早的 MSDE，免費）。官方以 MSDE 2000 SP4 測試。

1. 安裝 SQL Server（Express 免費），必要時建立指向本機的 ODBC 資料來源（File DSN 或 System DSN）。
2. 在 Table Designer 存好表格後，在 SQL Direct Configuration 執行 **Configure SQL Server**：它會在 SQL Server 的 `master` 資料庫為每個表格建立**資料檢視（view）**，名稱與 Table Designer 的表格名相同。**每次安裝後、使用 SQL Server 路徑的應用程式之前都必須做。**
3. 使用有 SQL 命令視窗的工具（官方列 SQL Server Management Studio 2005 等）。

```sql
-- EQUIPMENT 是你在 Table Designer 建立的表格，REFNO 是欄位
SELECT * FROM EQUIPMENT WHERE REFNO = '=12345/67'

UPDATE EQUIPMENT SET AREA = 100 WHERE REFNO = '=12345/67'

DELETE FROM EQUIPMENT WHERE REFNO = '=12345/67'
```

| 能做 | 不能做／注意 |
|---|---|
| `SELECT`（字元值用單引號） | **`INSERT` 不支援**（包含在結果格線新增列也不行） |
| `UPDATE`、`DELETE`；也可直接在結果格線編輯值後離開該列 | SQL Server 2000／MSDE 要確認 **Distributed Transaction Coordinator (DTC)** 已啟動才能以格線編輯更新 |
| Access 連結資料表：**ODBC 方式（官方建議）可寫回**；選 `REFNO` 為 Unique Record Identifier | Access 經 **OLE DB（Linked Server）方式不可寫回** |

> **專業提醒：** `DELETE` 與 `UPDATE` 等於直接修改模型，會受登入使用者的存取權、Team 寫入權、DAC 與 Multi-write 認領規則限制（45.3.1），也會建立 Session。官方範例的寫入工具一律假設在訓練專案或正式授權下操作；**不要拿正式專案練習 `DELETE`**。

### 45.7.7 二次開發者怎麼接 SQL Direct

文件有依據的接法：

- **ADO（VB6／.NET 均可用 ADO 概念）：** 以 Provider 名稱 `PDMSProv OLE DB Provider 12.0`、Data Source 為連線字串、帶使用者名稱與密碼開啟連線，查詢你定義的表格名；官方提供 `ADOTest` 的 Visual Basic 原始碼。
- **經 SQL Server：** 任何能連 SQL Server 的程式（含 .NET `SqlClient`、ODBC）都可查 `master` 資料庫中由 Configure SQL Server 建立的檢視，語法即上述 T-SQL。
- **設計原則：** 先在 Table Designer 設計「元素型別→欄位」映射；開發者應把 `REFNO` 一律設為 Key column（45.2.3 的穩定識別）；要寫回的欄位事先挑好，其餘維持唯讀。

文件**沒有**說明、本章標為〔待核對〕：現行 Marine 12.1 是否仍附 SQL Direct 12.0 與 64 位元相容性；較新 Windows／SQL Server 的支援；以 .NET 連 OLE DB Provider 的連線字串；多使用者部署（文件明說是單一使用者工具）；大量資料查詢效能。

## 45.8 Status Control：生命週期狀態管控

### 45.8.1 概念

**Status Control** 控制並回報單一模型物件在生命週期中的進展，可套用到任何模型物件（標記項目、目錄元件、圖面等），可表達為「Approved for Construction」「80% Complete」「Clash Free」等。管理員在 **Lexicon** 建立 **Status Definition**，最終使用者在任何建構模組（Design、Outfitting、Paragon、Spooler、Diagrams、Hull、Draft、Marine Drafting）以 **Status Controller** 套用。可與 DAC 緊密結合：只有特定人員能核可，或某狀態後禁止修改。

**Controlled Object（受控物件）** 指被指派一個或多個 Status Value 的模型物件；一個物件可同時受多個狀態定義控管（設計、製造、施工等）。

官方範例 Design Status 的主要路徑為 Work Pending → Work Started → Work Completed → For Check → Checked → Approved → Released，另有 Work Suspended、Preliminary、Rework 分支。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Design Status 範例工作流程，數字代表各狀態的 Numerical value，從 Work Pending 0 到 Released 100

*圖 45-10　範例 Design Status：括號數字是 Numerical value（Work Pending 0、Work Started 20、Work Completed 50、For Check 60、Checked 80、Approved 90、Released 100）。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.8.2 資料模型：STADEF、STAVAL、STALNK

一個 **Status Definition（STADEF）** 擁有一組 **Status Value（STAVAL）**；個別模型物件透過 **Status Link（STALNK）** 參照某個 Status Value。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Status Control 資料模型：Dictionary 資料庫中的 Status Definition 與 Status Value，設計資料庫中的 Status Link World 與 Status Link，以及 Equipment 的 Pseudo Attribute

*圖 45-11　資料模型：STALNK 在模型所在的 DB，保存對物件與 Status Value 的參照及註解；狀態資料以 Pseudo Attribute 呈現。（AVEVA 官方文件截圖，僅供內部教學）*

- **STALNK 與被控制的模型物件放在同一個 DB**，因此會隨模型物件一起 Global 分佈；它保存對物件與 Status Value 的參照，加上註解與歷史屬性。
- 狀態資料**不直接存在模型物件上**，所以使用者**不需要對模型物件有寫入權**就能設定其狀態。
- STALNK 對終端使用者不可見，但狀態資料可從物件的 Pseudo Attribute 取得；管理員需知道其存在以便設計 DAC。

> **專業提醒：** 核可者不必能改幾何，只要能改 STALNK；Dictionary DB 若被使用者 Defer，狀態參照會無法解析，需用 DAC 補洞。

### 45.8.3 在 Lexicon 設定 Status Definition

1. Dictionary Explorer 在 Dictionary WORLD 右鍵 → **New Status World** 並命名。
2. 在 Status World 右鍵 → **New Status Definition**（也可建 Status Group 容納定義）；輸入 Name 與 Description（Description 可含空白，若有設定，Status Controller 會使用）。
3. 以選取按鈕開 `Select element types`，指定 **Controllable element types**（例如 `EQUIPMENT`；可加多個型別）。
4. 在 Definition 右鍵 → **New Status Value**，輸入 Name、Description、**Numerical value**（可選，可當百分比或單純數值）。Status Value 名稱的唯一性只在所屬 Definition 內，不同 Definition 可重複 `Preliminary`、`Released`。
5. 對每個 Status Value 設定 **Valid transitions**（可轉移到的值），並選 **Promote** 與 **Demote**（可選，僅代表主流程；未標成 Promote／Demote 的有效轉移仍可在 Status Controller 使用）。
6. Status Definition 的 **Initial status** 預設為第一個 Status Value，可改。
7. 右鍵 **Graphical View** 可看工作流程圖；完成後 Save work 並離開 Lexicon。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Lexicon 的 Graphical View：DesignStatus 工作流程圖，綠色箭頭為前進，紅色為退回

*圖 45-12　Lexicon 中 Status Definition 的 Graphical View，可檢視轉移是否與設計一致。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.8.4 使用者端：Status Controller

在建構模組以 **Display > Status Controller** 開啟，初始為空。

1. 首次開啟會要求以 `Set Layout Scope Elements` 選擇納入的擁有者元素（可用 Explorer 與 Search 頁籤）；取消則納入**所有**可控制元素，**可能耗時數分鐘**。不確定時，先選一個子孫少的 Zone，之後可再改。
2. 以 `Status Layout` 下拉的 `New Status Layout`（或格線右鍵 `Status Layout`）選 `Select Status Columns`，勾選要顯示的狀態欄位；多個定義時可指定 **Focus Status**（用於 Edit Status）。範圍越小，顯示越快。
3. 欄標題右鍵 `Column Setup` 可看狀態欄的 Pseudo Attribute 運算式（例如對 SCEQUI 顯示連結 EQUI 的狀態：`STVDSC( /DesignStatus ) of Deslnk numb 1`）；`Save Status Layout`／`Save Status Layout As` 存佈局，亦有 `Settings`、`Export to Excel`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Status Controller 視窗：Status Layout 與 Focus Status 工具列，格線列出物件與 Equipment Design Status 欄位，全部為 Not Controlled

*圖 45-13　Status Controller：以 Equipment Design Status 為 Focus Status，105 個設備皆為 Not Controlled。（AVEVA 官方文件截圖，僅供內部教學）*

**Edit Status：** 選取列後右鍵 `Edit Status`。初始皆為 `Not Controlled`（尚未對該定義指派；可能受其他定義控管）；下拉選 `Assign to the initial value`，可附 Comment，按 OK 或 Apply。之後下拉選項依有效轉移而定；已定義 Promote／Demote 時可直接選。多選的物件若值相同顯示實際值，否則為 mixed。`Remove Status` 刪除狀態資料使其不再受控；`Navigate To` 僅在單選時啟用，會設為目前元素。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Edit Status 對話框：顯示選取的兩個元素、Status last modified 與 modified by、Value 下拉與 Comment

*圖 45-14　Edit Status：Value 預設為 Not Controlled (No Change)，可附註解。（AVEVA 官方文件截圖，僅供內部教學）*

其他：**Status History** 列出狀態轉移與其他 Session 歷史（可 Export to Excel）；**Statistical Report** 對 Focus Status 的選取物件顯示資料與圖表（懸停看數字、右鍵 `List Elements`、可切換圖表類型與圖例位置）；工具列含 Promote、Demote、Edit Status、Remove Status、Status History、Statistical Report，與 `Select CE in Grid` 等；列可**拖放到 3D 視圖加入 drawlist**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Statistical Report：以 3D 圓柱堆疊顯示各 Design Status 值的物件數量與圖例

*圖 45-15　Statistical Report 的 3D 圓柱圖範例，圖例列出 Work Pending 至 Released 與 unset。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.8.5 Pseudo Attribute 與 `STM` 指令

**物件上的 Pseudo Attribute（以 STADEF 為 Qualifier）：** `STVVAL`（目前 STAVAL）、`STVNAM`／`STVDSC`／`STVNUM`／`STVCOM`（名稱／說明／數值／註解）、`STVPRO`／`STVDEM`（Promote／Demote 目標）、`STVLST`（已指派的 STADEF）、`STVASD`／`STVTRV`（可適用的定義／有效轉移）、`STVMOD`／`STVUSE`／`STVHIS`（最後修改時間／人／歷史）、`STVUNR`（無法解析的參照）。STADEF 上另有 `STVREF`、`STVUSD`（受控元素清單）。

查詢帶 Qualifier 的屬性，在命令列要在括號結尾前留一個空格：`Q STVVAL(/DesignStatus )`。PML2：`!!ce.attribute('STVVAL', !statusDefinitions)`。

> **常見陷阱：** 在 Collection 條件中用 `stvval(...) eq /Approved` **不會得到預期結果**，因為 Status Value 名稱只在其 Definition 內有意義。官方建議改用：`var !myItems collect all equi with (stvnam( /EquipmentDesignStatus ) eq '/ Approved')` 或 `(stvnum( /EquipmentDesignStatus ) gt 75)`。

**`STM` 指令（`SELELE` 省略則為目前元素）：**

| 指令 | 說明 |
|---|---|
| `STM ASS /Definition [to SELELE] ['comment']` | 指派並設為初始值（INIVAL）；有註解則設定，否則清除舊註解 |
| `STM REM /Definition [from SELELE]` | 移除，使其不再受控 |
| `STM RESET /Definition [on SELELE] ['comment']` | 重設為初始值，**不需**有效轉移 |
| `STM PRO`／`STM DE /Definition [on SELELE] ['comment']` | 設為 Promote／Demote 值 |
| `STM SET /Definition [/Value] [on SELELE] ['comment']` | 設為指定值，**需有有效轉移** |
| `STM CO /Definition [on SELELE] 'comment'` | 只改註解，不改值 |

刪除受控物件會留下**孤兒 STALNK**（其 `CELREF` 被 DICE 報為 `BADREF`）；執行 `!!stmcleanup()` 清理所有 `CELREF` 無效的 STALNK。

### 45.8.6 與 DAC 及 Auto Color 結合

官方示範的 DAC 作法：一個 Role 的第一個 PEROP 授予全部權限，後續 PEROP 在特定條件下拒絕。

| 目的 | PEROP 條件（拒絕對象） |
|---|---|
| 完成度達 50% 後禁止修改設備 | 對 Equipment 拒絕 Modify、Delete；`COND ( ATTRIB STVNUM(ID /DesignStatus ) GE 50 )` |
| 進入 For Check 後不得由此人移出 | 對 STALNK 的 `VALREF` 拒絕 Modify、Delete；條件為 `OWNER OF VALREF` 為 `/DesignStatus` 且 `DESC OF VALREF` 為 `'For Check'` |
| 使用者只能修改狀態 | 對 `STLNKW HIERARCHY` 授予所有操作，且只指派這一個 PEROP（屬「正向 DAC」，無法自訂拒絕訊息，會顯示通用訊息） |
| 狀態不足不得 Issue | 拒絕 Issue；`COND ( UNSET( STVLSK ) OR ATTRIB STVNUM(ID / DesignStatus ) LT 100 )` |

〔官方該範例條件寫為 `STVLSK`，而 Pseudo Attribute 表為 `STVLST`，疑為文件筆誤，待核對。〕

**Auto Color：** Status Value 可用於 Element Rules，例如 `attrib stvnum( /DesignStatus ) eq 0`（Pending）、`ge 50`（Completed）、`badref ( attrib stvval( /DesignStatus ) )`（Not Controlled），再搭配 Auto Color 規則，如已完成綠色、待辦黃色、未受控紅色。

### 45.8.7 二次開發者怎麼接 Status Control

**PML 事件：** 所有 Status Controller 的操作都能以 PML 完成；客製使用事件，事件方法接受**一個陣列參數**。

事件：`Before／AfterStatusAssign`、`Before／AfterStatusRemove`、`Before／AfterStatusChange`（變更、Promote、Demote）、`BeforeControlledElementDelete`，以及資料庫變更事件 `Before／AfterSavework`、`Before／AfterFlush`（有狀態資料變更時）。

狀態變更事件的引數：(1) 受控物件 Refno 字串陣列、(2) Status Definition Refno、(3) 目標 Status Value Refno（可為 `=0/0`）、(4) 回傳訊息——**設定訊息即中止操作，但僅 Before 事件有效**。資料庫變更事件引數為 Definition、被指派／被變更／被移除的物件清單、回傳訊息（同樣僅 Before 可中止）。

**StatusProjectHandler 框架：** `pmllib\common\objects` 下的 `statusProjectHandler.pmlobj`，進入建構模組時建立全域實例並登記事件處理器。

- 除錯：`!!statusProjectHandler.debugOn()`／`debugOff()`。客製程式碼只能加在各方法的 `Start of customisation` 與 `End of customisation` 之間，**其他部分不要修改**。
- Before 方法以 `!returnMessage = |Status error: ...|` 中止操作（預設只禁止一般使用者刪除受控物件）；After 方法可做連動變更（如把組合件狀態擴散到子孫）；`AfterSavework`／`AfterFlush` 用於同步外部系統。

**`statusData` 物件**（`pmllib\common\objects\statusData.pmlobj`）封裝單一或多個「物件×定義」組合：建構子可傳目前元素、定義名稱、DBREF 或陣列；方法有 `assign`／`assignStatus`、`remove`、`promote`、`demote`、`setStatus(def, valueName[, comment])`、`output`／`print`、`refresh`，`refreshModeNone()` 為預設（效能最佳）。

**核心物件**（需 `import 'Aveva.Pdms.DataManagement.PML'` 與 `using namespace`）：`STATUSMANAGEMENT`、`STATUSEVENTS`（`addEventHandler`）、`STATUS`、`STATUSVALUE`、`ASSIGNEDSTATUS`。

```text
!status = object status('/DesignStatus')
!status.assign('/E1301')
!status.promote('/E1301', 'Ready for checking')
!currentStatus = object assignedStatus('/DesignStatus', '/E1301')
!valueName = !currentStatus.currentValue().name()
!comment   = !currentStatus.comment()

```

**C#（.NET）：** 類別在 `Aveva.Pdms.DataManagement.dll`（位於 `PDMSEXE`），同時需參考 `Aveva.Pdms.Database.dll`；命名空間 `Aveva.Pdms.DataManagement` 與 `Aveva.Pdms.Database`。可用類別：靜態 `StatusManagement`（`Statuses` 屬性回傳 `Status[]`）、`Status`、`StatusValue`、靜態 `StatusCommand`（等同 `Status` 的功能）、`StatusEvents`。事件處理示範：

```csharp
Status status = Status("/DesignStatus");   // 官方範例寫法
StatusEvent statusEvent = status.Event;
statusEvent.BeforeStatusChange += new StatusEvent.BeforeStatusChangeEventHandler(My_BeforeStatusChange);

private void My_BeforeStatusChange(object sender, CancelStatusEventArgs e)
{
    if (/* 需要中止 */) { e.Cancel = true; e.Message = "reason not to proceed"; }
}
```

〔官方範例省略 `new` 與完整類別宣告，上列照原文；實際型別簽章需以 Visual Studio Object Browser 為準，待核對。〕

**散佈與升級：**

- **統一 Status Layout：** 使用者各自存的 Layout 位於使用者 Local Settings 下 `…\Application Data\Aveva\PDMS\<專案>StatusGridProfiles`；管理員可把自己建好的檔案複製給其他使用者，**不必複製** `LastSelectedStatusGridProfile` 與 `WindowsLayout`（會自動建立）。
- **自 Model Manager 升級：** 其狀態值清單可對應成 Status Definition，有篩選條件的型別用 UDET（如 `:CivilsPipe`），再以巨集迴圈指派定義並設為對應值。

## 45.9 常見錯誤

| # | 錯誤 | 後果 | 對策 |
|---|---|---|---|
| 1 | 外部識別用 Name 或 Constructed Name | 改名或順序變動後找錯物件 | 存 Refno |
| 2 | Merge Changes 前沒建 Stamp | 比較點被併掉 | 先建 Stamp；有 Extract 時由下而上 |
| 3 | 把 Backtrack 當後悔藥 | 後面的 Session 永久刪除 | 優先 `REVERT`；先備份 |
| 4 | 逐一 Claim／Flush 元素 | 每次存取 DB 並產生 Session | 一次處理一批或用 Collection |
| 5 | 部分 Issue／Drop 後不檢查 | 工程不一致 | 執行 Datacon 與 Clasher |
| 6 | `CLEANUP … DELETE` 範圍未確認 | 大量元素被刪 | 先查範圍，備份後再做 |
| 7 | SQL Direct 表格沒有 `REFNO` 或 `NAME` Key 欄，或以為支援 `INSERT` | 無法寫回、語句失敗 | 設 `REFNO` 為 Key；新增元素改用 PML 的 `NEW` |
| 8 | Collection 以 `stvval(...) eq /Approved` 篩選 | 找不到物件 | 用 `stvnam`／`stvnum` |
| 9 | 刪除受控物件後未清孤兒 STALNK | DICE 報 BADREF | 執行 `!!stmcleanup()` |

## 45.10 本章小結

- **Database Management：** Refno 是穩定識別；Session 只增不改，Savework／Getwork 控制可見性；Stamp 保護比較點，Merge Changes 回收空間，Backtrack 永久刪除而 Revert 不會。
- **Multi-write 與 Extract：** Claim 以 Primary 元素為粒度，其餘用屬性層級的 Last Back Wins；Extract 以 Flush／Issue／Drop／Refresh 管理，工程一致性要靠 Datacon 與 Clasher。
- **SQL Direct：** Table Designer 設計 Table Schema，經 PDMS Provider 與 Server 用 Excel、ADO 或 SQL Server 讀取模型；不支援 `INSERT`，工具為舊世代，需核對相容性。
- **Status Control：** STADEF→STAVAL→STALNK 讓狀態不改動模型物件；`STM`、Pseudo Attribute、DAC、Auto Color 與 PML／C# 事件把工作流程做成可強制的規則。

## 45.11 練習題／自我檢核

**練習（只在訓練專案進行）：**

1. 用 `Q DBNUMBER` 與 `Q REFNO` 解讀某元素 Refno 的兩段整數。
2. 以兩個使用者連同一個 MULTIWRITE DB，製造「兩人同名」衝突，觀察第二位 `SAVEWORK`。
3. 修改設備屬性後，用 `DIFF`、`Q LASTMOD`、`Q HISTORY`、`SETCOMPDATE NOW` 與 `Q OLD <屬性>` 取回舊值。
4. 用 `REVERT HIER /某元素 BEFORE LATEST` 還原一次修改，說明它與 `BACKTRACK` 的差異。
5. 用 Table Designer 建立 `EQUIPMENT` 表，以 Excel 讀入，Savework 後 Refresh 驗證。
6. 在 Lexicon 建立 3 個值的 Status Definition，用 `STM ASS`、`STM PRO`、`Q STVNAM(/Def )` 驗證，並設一條 DAC 規則禁止達 100 後修改。

**自我檢核：**

- [ ] 我能說明 Team 與 MDB 對寫入與視圖各自的影響。
- [ ] 我能說出 Undo、Revert、Backtrack 的差別與風險。
- [ ] 我能說明 Claim 的粒度與 Last Back Wins 適用情況。
- [ ] 我能區分 Flush、Issue、Release、Drop、Refresh。
- [ ] 我能說明 SQL Direct 的四個元件與資料流。
- [ ] 我能說出 SQL Direct 透過 SQL Server 可執行與不可執行的語句。
- [ ] 我能畫出 STADEF／STAVAL／STALNK 的關係。
- [ ] 我能寫出 `STM` 指令，並說明 Before／After 事件如何中止或延伸操作。

## 45.12 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 45 章](appx_d_verification_zh-TW.reading.html#ch45)；取材覆蓋與未讀範圍：見[附錄 E 第 45 章](appx_e_coverage_zh-TW.reading.html#ch45)。
