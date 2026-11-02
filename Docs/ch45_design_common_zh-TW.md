# 第 45 章　設計共通功能：Clash Manager、Data Checker、Design Model Editor 與 Reporting

> 前面各章依專業（管路、結構、艙室、纜線）說明 Design 模組怎麼建模。這一章換個角度，談**每個專業都會用到、卻不屬於任何單一專業**的那一層：系統階層、穿孔管理、干涉檢查（Clash Manager）、資料一致性檢查（Data Checker）、用滑鼠改模型（Design Model Editor）與報表（Reporting）。
>
> 對二次開發者而言，Data Checker 的檢查函式是**標準的 PML 擴充點**，Reporting 有 PML 批次介面，Excel 匯入匯出有 `excelio` 物件，都是不必改核心就能接進去的位置。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件 *Design* 章節下的七個子節點：Clash Manager、Data Checker Utility、Design Common Functionality、Design Reference（僅讀 Data Consistency Checking 與 Clash Detection 兩個 Utilities）、Design Model Editor、Reporting、Reporting Reference。文件多半沿用 PDMS 時代內容，仍出現 PDMS、PDMSUSER、Outfitting、PE Workbench 等舊名稱，本章照原樣保留。**Reporting 在文件裡其實是兩套東西**：新的 Report Designer（`.repx`／`.repv`，圖形化設計器）與舊的 Standard Reporting（`.tmp`／`.rep`，表單式範本），本章分開寫。官方多為操作手冊，PML 語法只在文件有給範例時才寫（Data Checker 有完整範例）；其餘標〔待核對〕，不編造。章末列出實際閱讀範圍。

## 45.1 學習目標

讀完本章，你應該能夠：

1. 說明 System Hierarchy（`SYGPWL`／`SYGPAR`／`SYSGRP`）與標準 `SITE/ZONE` 階層的差別，以及為何能用「系統」一次對跨區元素做檢查。
2. 說明 Hole Management 的受管孔（Managed Hole）、虛擬孔（Virtual Hole）、實孔（Real Hole）與請求—核准的狀態流程。
3. 區分 Design 內建的 Clashes 視窗、`DESCLASH` 指令與獨立的 Clash Manager 三者的定位。
4. 說明 Clash Manager 的資料模型：Clash Set、Clash Group、Discipline、Status、Level／Type。
5. 讀懂 Clash Manager 的 Assign／Accept 規則（Rule Expression）、Regular Expression 與 Oracle 萬用字元兩套語法，並用 Test Rules 驗證。
6. 規劃夜間批次：`mmscmd ... -clash set` 與 Track Changes，並判讀 `pclam.*` 記錄檔。
7. 使用 Data Checker 視窗檢查元素、保存失敗清單，並寫出一個符合官方規格的檢查設定檔與 PML 檢查函式。
8. 在 Design Model Editor 中用 Locator Handle 與 GCM 移動、旋轉元件，並知道選取集（Selection Set）規則。
9. 區分 Report Designer 的 Layout Template 與 Report Definition，完成資料來源綁定、參數化與執行。
10. 使用舊式 Standard Reporting 範本（欄位、排序、小計、變數、批次），並知道何時該用哪一套。

## 45.2 Design 模組共通功能與介面

官方 *Design Common Functionality* 收錄約一百頁「多個專業共用」的功能。下表是本章的導覽地圖（Clash 與報表會在後面專節說明）。

| 功能 | 入口（官方選單） | 用途 | 注意 |
|---|---|---|---|
| System Hierarchy | `Create > System Hierarchy`、`Display > Explorers > System Explorer` | 以「系統」而非 `SITE/ZONE` 組織與檢視元素 | 範例以 HVAC 為主，其他專業功能相同 |
| Modify Design System | `Utilities > Systems` | 把元素加入／移出系統、指定主系統 | 元素可屬於多個系統 |
| Hole Management | `Utilities > Hole Management` | 受管孔的請求、核准與報表 | 見 45.2.2 |
| Clashes 視窗 | `Utilities > Clashes` | 即時檢查目前元素的碰撞 | 與 Clash Manager 不同 |
| Mass Properties | `Utilities > Mass Properties` | 體積、表面積、重量、重心 | 見 45.2.3 |
| Excel Import／Export | Wizard 與 `excelio` | 多工作表與資料庫往返 | 見 45.7 |

另有 User Grid Systems、Standard Model Library（把多專業元素存成可重複放置的庫項）、Import Data（CSV／XLS 預填設備，見 45.7）、Current Session Units 與 Schematic Gateway，本章僅列名；定位與定向見 45.2.4。

### 45.2.1 System Hierarchy：用「系統」看模型

標準階層是 `SITE/ZONE/…`；同一批 HVAC 資料也可以用系統（System）檢視。系統的好處是**跨資料庫、跨 SITE／ZONE 的元素能立即歸在一起**，方便對整個系統下達 clash 檢查、資料檢查、加入 3D 視圖等指令。

系統元素放在設計資料庫的 `WORL*` 之下，三層結構如下。

| 層級 | 元素類型 | 說明 |
|---|---|---|
| 系統群組世界 | `SYGPWL` | 有四碼的 `PURP` 屬性，標明用途 |
| 系統群組區域 | `SYGPAR` | 同樣有 `PURP` |
| 系統 | `SYSGRP` | 可再擁有子 `SYSGRP`（子系統） |

`SYSGRP` 下另有 `SYSMDA`（存 Function 與 Description，會複製到被指派到此系統且這兩屬性尚未設定的元素）與 `SYSCDA`（多提供管路專用預設值）。輸入名稱時系統自動加 `/` 前綴。

在 `Utilities > Systems` 的 Modify Design System 視窗中，只有擁有 `MDSYSF` 屬性的元素才能被加入系統。**Main Systems** 分頁顯示元素直接參照的系統，**Owning Systems** 分頁顯示連同繼承自上層元素的所有系統；元素屬於多個系統時，可用 `Make this System Primary` 指定主系統。

### 45.2.2 Hole Management：穿孔的請求與核准

第 [21 章](ch21_pipework_zh-TW.reading.html) 已從管路角度說明為何開孔要走核准。本節補共通機制。Hole Management 負責**受管孔**的資料傳遞、一致性檢查與報表，服務 Equipment、Piping、HVAC、Cable、Outfit Steel 與 Room Design 六種專業。三個關鍵名詞如下。

| 名詞 | 官方定義 |
|---|---|
| Managed Hole（受管孔） | 由 Hole Management 管控的元素與資料 |
| Virtual Hole（虛擬孔） | 所需孔形的建模表示 |
| Real Hole（實孔） | 孔在模型中的實際幾何 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hole Management 的請求與核准流程，左為申請者，右為核准者

*圖 45-1　Hole Management 流程：申請者建立虛擬孔並設為 REQUESTED，核准者檢查後設為 APPROVED（同時產生實孔）或 REJECTED。（AVEVA 官方文件截圖，僅供內部教學）*

流程中的狀態值包含 `REQUESTED`、`REJECTED`、`APPROVED`、`CANCELLED`、`REDUNDANT`、`WITHDRAWN`：申請者在核准前可取消或修改；已核准的孔若不再有效，要回頭修改；不再需要時由申請者設為 `REDUNDANT`，核准端對應為 `WITHDRAWN`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hole Association Manager 視窗，上方為篩選條件，中間為關聯清單

*圖 45-2　Hole Association Manager：可依 Discipline、Status、Claimed、Valid 篩選受管孔，並在清單中檢視與修改。（AVEVA 官方文件截圖，僅供內部教學）*

各專業（Piping、HVAC、Cable Tray、Structural、Equipment、Room Design）建立穿孔的入口都在 `Utilities` 選單，流程相同：`Pick Penetrated Items`（被穿透者，如甲板）→ `Pick Penetrating Items`（穿透者，如管）→ `OK` 計算位置 → 進入 Hole Management Definition 視窗。管路預設以 `ATTA` 標記位置，也可放 `COUP` 當套管；設備穿孔需有被指定為穿孔輪廓的擠出圖元；Room Design 的門窗需有用途為 `HPGE` 的穿孔輪廓。

Hole Management Definition 視窗的重點：**Single**（每個穿透者一個孔）與 **Merged**（合併成一個孔，孔形類別變成 User Defined Profile，可用 loop vertex editor 修改）；孔形類別有 Standard Types 與目錄中設定的 Selection Tables。孔尺寸可由零件屬性控制：

| 屬性（DKEY） | 意義 |
|---|---|
| `AHDI` | 圓孔直徑；有設定時 Clearance 值會被忽略，否則以管外徑加 Clearance |
| `AHX`、`AHY` | 矩形孔的 X、Y 尺寸（HVAC 元件） |

專案要啟用 Hole Management，需有五項設定：add-in 檔（`PDMSUI/des/addins/holemanagement`，註解或刪除即停用）、關聯定義（範例專案 `/HM-ASSDEF`）、目錄孔定義（`/HM-FIXI-PTWLD`、`/HM-FIXI-CATA`）、設備設定與儲存區。Selection Table（`TABGROUP`）以 `PURP` 區分專業：`PPEN`、`HPEN`、`CPEN`、`TPEN`、`SPEN`、`FIXI`、`FLOO`。孔尺寸屬性可在目錄以 `NEW DATA ... DKEY AHX ... PPRO ( ATTRIB DDESP[2 ] + 100 mm )` 之類的指令定義。

> **專業提醒：** 在 Global 專案中，若申請者與核准者在不同地點，關聯資料必須放在有 extract 的資料庫，且每次狀態變更前後要 `Save and Unclaim`，查看他人變更要按 `Get all changes`。這一點與第 37 章的 Global 概念相關，細節以官方 Global 文件為準〔待核對〕。

### 45.2.3 Mass Properties 與 Clashes 視窗

**Mass Properties**：可對任何有圖形的元素查詢體積、表面積、重量、重心，來源有使用者輸入（`USRWEIGHT`、`USRWWEIGHT` 濕重、`USRCOG`）、目錄、系統依 3D 模型與密度計算、船體元素解析計算。指令以 `N`／`G`／`R` 前綴區分淨值、毛值與粗估（`NVOL`／`GVOL`／`RVOL`、`NWEI`、`NCOFG` 等）；`Negatives` 設 `Consider (Net)` 會扣除孔洞，`REPRE MASS 6` 設定質量表示層級。

**Clashes 視窗**（`Utilities > Clashes`）供設計者隨時檢查，提供 `Check`、`Check CE`、`Check Support`、`Recheck Support`，結果同時出現在可篩選的格線與 3D 視圖，右鍵可 `Print Preview` 或 `Save to Excel`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Design 的 Clashes 視窗，左為分頁與格線，右為 3D 視圖

*圖 45-3　Clashes 視窗：上方 Check 欄決定檢查對象，下方分頁為 Clashes、Obstructions/Exclusions、Limits、Options、Report。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.2.4 定位與定向（Position／Orientate）

定位選單有：`Position > Explicitly (AT)`（相對世界或另一元素，基準可選 Origin、P-Point）、`Using Ship References`（框架與格線加偏移）、`Relative (BY)`（相對目前位置移動）、`Move`（Distance、Through、Clearance、Towards 四種方式）、`Drag`（同四種，但連同受約束網路移動）；定向用 `Orientate > Axes`，指定兩軸、第三軸自動決定。

重要差異：**一般 `Move` 移動設備時，連接的管路不會跟著動；`Drag` 才會移動受約束的網路。** `Towards` 的 `Next`、`Tail`、`Previous` 選項只適用管路。

## 45.3 Clash Manager：碰撞檢查與管理

### 45.3.1 三個層次的碰撞檢查

文件中出現三種不同層次的碰撞機制，不要混為一談。

| 機制 | 位置 | 本質 | 適合 |
|---|---|---|---|
| `DESCLASH` 指令模式 | Design Reference Utilities | 指令式碰撞偵測引擎 | 自行寫巨集、細部設定 |
| Clashes 視窗 | `Utilities > Clashes` | 對上述引擎的圖形前端，即時檢查 | 設計者自查 |
| Clash Manager | Model Management 的延伸，或獨立版 | 記錄、分組、指派、核准與趨勢 | 專案級管理 |

官方明說 Clash Manager 是「補充內建碰撞能力」：它協助組裝輸入資料、**透明地執行 desclash**，把輸出載入**另一個資料庫**（Oracle 或 SQL Server），再提供報表、檢視與核准。相容產品為 AVEVA Marine Design 12.0 以上；作為 Model Management 的一部分搭配 PE Workbench，獨立版（Standalone）則不需要。

### 45.3.2 核心概念

| 名詞 | 說明 |
|---|---|
| Clash | 兩個元素的部分在 3D 空間重疊；元素不可是 `SITE` 或 `ZONE` |
| Group | 同一對元素在一定範圍內的多個碰撞合併成一組，可整組檢視、報表、核准 |
| Discipline | 負責解決該組碰撞的專業，可自動或手動指派 |
| Status | `Unknown`、`Unapproved`、`Pending`、`Conditional`、`Approved` |
| Clash Set | 要檢查的範圍：MDB、Obstruction List、Check List、Exclude List |
| Type | `Clash`、`Clearance`、`Touching` |
| Level | `Hard/Hard`（HH）、`Hard/Insulation`（HI）、`Hard/Soft`（HS）、`Insulation/Insulation`（II）、`Insulation/Soft`（IS）、`Soft/Soft`（SS）、`Not Proven`（NP） |

Clash Set 的三個清單：**Obstruction List** 是被撞者（牆、建築、主結構等大件）；**Check List** 是要檢查是否撞到障礙的項目；**Exclude List** 從障礙清單排除，例如 Site 下 30 個 Zone 要納入 28 個，就把 Site 放進障礙清單，再把 2 個 Zone 放進排除清單。

狀態值的語意要特別留意：

| 狀態 | 官方語意 | 報表意義 |
|---|---|---|
| Unknown | 新碰撞且無自動接受規則命中時的預設值 | 最差情況 |
| Unapproved | 尚未審查，仍是待處理 | 待處理 |
| Pending | 設計團隊正在審查 | 處理中 |
| Conditional | 已在模型中解決，下次執行後不再出現 | **報表視為已解決** |
| Approved | 審查後認定可接受，後續仍會出現但保留狀態 | 視為 Clash Free |

「最差情況」依上表由上而下排序；專案可插入自訂狀態，例如 `Piping to Verify`、`For Design Review`。

### 45.3.3 存取權限

Clash Manager 的管理者權限**以 Windows 登入帳號為基礎，直接在 Clash Manager 內設定**，不同於其他 Model Management 管理權限，這樣才能不依賴 PE Workbench 使用。權限有兩個面向：User Access Levels（誰是各專業的 Member 或 Supervisor）與 Security Levels（Clash、Owner、Clash Check CE、Comments 四種動作各自的門檻）。每種 Security Level 有 High、Medium High、Medium、Medium Low、Low 五個預設狀態，預設為 Medium，也可自訂。

預設規則（Medium）：狀態由擁有者專業的 Supervisor 更新；擁有者可由新專業的 Supervisor 接手（acquire）或由現任 Supervisor 轉派（assign）；備註可由任一涉及專業的 Member 新增。**準備與執行碰撞、修改選項、進階工作只有 Admin 專業的 Supervisor 能做。**

官方提出三種角色分工：全體專業設計者自負責（中大型，安全等級偏 Low）、Supervisor 或少數指定人員（中小型，Medium）、單一碰撞協調員（小型，偏 High）。

### 45.3.4 設計流程總覽

官方工作流以 Admin 專業的 Supervisor 為主角：先在 Clash Manager Configuration 完成 Project、Discipline、Security、Group、Assign 五個必做分頁（其餘分頁小專案可用預設），再建立並執行 Clash Set、指派專業；設計者改模型與加備註、擁有者 Supervisor 更新狀態；之後重跑、Track Changes，並定期清除失效資料。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Clash Manager Configuration 的 Project 分頁

*圖 45-4　Clash Manager Configuration 的 Project 分頁：Project、Userid、Default MDB、顯示單位，以及 Project Defined Field（例中以 `:AREACODE of zone` 把區域碼加入報表）。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.3.5 組態：Group、Accept、Assign、Test Rules

**Group 分頁**決定碰撞怎麼合併。「Group Clashes between element pairs within +/-」的距離預設 100 mm；官方指出實務常改成 2000 mm 讓分組更有效，但需與各專業主設計者討論，且**專案中途大幅更動會要求重新計算（Recomputation），不建議**。因為是正負值，分組體積邊長是設定值的兩倍。預設分組層級為 `PIPE-PIPE`、`EQUI-EQUI`、`STRU-SCTN`、`HVAC-HVAC`、`REST-REST`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Group 分頁：分組距離、預設分組層級與例外規則

*圖 45-5　Group 分頁：上方為分組距離（例中 1000 mm）與各專業預設分組層級，下方為依 GTYPE 設定的例外。（AVEVA 官方文件截圖，僅供內部教學）*

**Accept 分頁**決定哪些碰撞自動接受並設為指定狀態。規則由上而下檢查，每條規則由多個 Rule Expression 組成，**第一條所有運算式皆為真者生效**，並自動在碰撞紀錄附上命中規則的備註。官方列舉的合理自動接受情境如支撐與主鋼構、樓梯與其他專業、套管與其他專業的 Touch／Clear，以及所有 Soft/Soft。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Accept 分頁：以狀態為節點的規則樹

*圖 45-6　Accept 分頁：上方是以 Status 為主節點的規則樹（Accept Rule1～3），下方為所選規則的運算式（Element、Attribute、Value）。（AVEVA 官方文件截圖，僅供內部教學）*

**Assign 分頁**決定擁有專業如何自動指派。測試依序進行直到有結果：Assignment Rules、Class、Priority、Element Discipline。Class 與 Priority 以兩元素的 Order 比較，**較不重要者的專業成為擁有者**；Element Discipline 通常最後，同專業就取該專業，不同則用預設（通常 `UNALLOCATED`）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Assign 分頁：套用順序與專業規則

*圖 45-7　Assign 分頁：Order of Application 決定四種測試的順序與是否啟用，下方為各專業的指派規則。（AVEVA 官方文件截圖，僅供內部教學）*

**Rule Expression 語法。** 每個運算式由 Element、Attribute、Value 三欄組成，同一條規則內各運算式為 **AND**，**沒有 OR**。

| 欄位 | 可用內容 |
|---|---|
| Element | `@general`（碰撞本身）、`@element-1`、`@element-2`（無特定順序，與報表的元素 1、2 無關） |
| Attribute | 關鍵字（`@class`、`@priority`、`@discipline`、`@gtype`、`@status`、`@level`、`@type`、`@setDiscipline`）或任何 Marine 屬性 |
| Value | 選單值、Regular Expression 或關鍵字（如 `@element-2`、`@ref-of-element-N`、`@first`、`@last-n`） |

Level 可選 HH、HS、HI、II、IS、SS、NP；Type 可選 `CLAsh`、`CLEarence`、`TOUch`。數值屬性可用 `> >= < <=`。`@setDiscipline` 只用於指派規則，可把擁有者設為任一元素的專業或第三方專業。

| 用途 | 範例 | 意義 |
|---|---|---|
| 組態用 Regular Expression | `^[AB]305$` | 以 A 或 B 開頭並以 305 結尾 |
| 否定 | `!^/S45` | 不以 `/S45` 開頭（開頭 `!` 為否定運算子） |
| GUI 篩選的萬用字元 | `%pipe%`、`pipe_` | Oracle／SQL Server 風格：`%` 任意長度，`_` 單一字元 |

**兩套萬用字元不可混用：組態一律用 Regular Expression，GUI 篩選一律用 `%` 與 `_`。**

Clash Set 的 Obstruction／Check／Exclude 清單另有一套元素規則語法：`<attribute> [OF <gtype>|<eleName>] [NOT] <op> <value>`，運算子有 `eq ne gt lt = != <> > < like`。例如 `name of zone like ^/STRU`（名稱以 `/STRU` 開頭的 ZONE）、`bore of pipe gt 100`、`!PIPE`（從結果清單中移除名稱含 PIPE 者）。注意 `name of pipe not like 'PIPE'`（往清單**加入**）與 `!PIPE`（只**移除**）完全不同；字串與關鍵字混淆時要加引號；預設分組層級以外的類型（如 `BBLOCK`）要先加進 Gtype/Tracking 清單。

**Test Rules 表單**可在不重算整個資料庫的前提下，對現有碰撞紀錄試跑新規則，顯示 New Discipline 與 New Status，但**不會儲存**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Test Rules 表單

*圖 45-8　Test Rules 表單：以 Group／Detail 選擇範圍，Query 取出紀錄，Evaluate Rules 套用新規則，Get Work 重設 MDB 並取得 `SaveWork` 之後的模型變更。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.3.6 執行、批次與記錄檔

手動執行：`View > Clash Manager`，`Tools > Run Clash Set`，或在 `Tools > Clash Sets` 選取後按 `Run Desclash`。表單選項如下。

| 選項 | 說明 |
|---|---|
| Branch Check Type | A Check：逐圖元完整檢查，不建議常用；B Check：簡化，忽略分支內部分元件對，一般使用 |
| MAP Override | 忽略 Spatial Map 錯誤（否則會中止） |
| Check ADD | 檢查清單自動加入障礙清單，原障礙清單內容被忽略 |
| Ignore Connections | 忽略鋼構接點處的碰撞 |
| Modified Checklist Items Only | 只重檢自上次執行後幾何有變動或未檢過的項目，未變動者沿用舊結果 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Run Clash Set 表單

*圖 45-9　Run Clash Set 表單：選 Branch A／B Check、MAP Override 等選項，下方進度列顯示「Waiting for completion of CheckList item 1 of 5」。（AVEVA 官方文件截圖，僅供內部教學）*

**批次執行**是大型專案的常態，因為 desclash 很耗時。官方做法是寫一個 `.bat`：先設好專案環境變數（呼叫 `evars.bat`），再執行 `mmscmd`，並以 Windows 工作排程器排程。

```
mmscmd <userid> <password> <connectString> <project> <configFile> <logfile> -clash <選項>
  -clash set <set_number> "<comments>"                 -- 執行 Clash Set
  -clash trackChanges "<comments>"                     -- 建立里程碑
  -clash loadFile <set_number> "<comments>" <file> [-L] -- 載入 desclash 輸出
```

`<logfile>` 可含 `#date#`、`#time#`；載入檔案時 `-L` 可略過第二階段（設定群組最差情況、垃圾回收、更新元素最差狀態），多檔載入時**最後一次不可加 `-L`**。官方建議：夜間跑較小的 Clash Set、週末跑全域 Clash Set；**Clash Set 要依序執行，不要平行**，否則 Oracle 資料爭用。

記錄檔位於 `%TEMP%` 下的 `Pclam_<專案碼>_<Windows 使用者>_<Clash Set 號>` 子目錄：

| 檔案 | 用途 |
|---|---|
| `pclam.fin` | 無錯誤時內容為 `OK`，有錯誤則寫入 Marine 錯誤訊息 |
| `pclam.log` | 主記錄；結尾有 `Normal Termination` 才算成功 |
| `pclam.mon` | 各階段耗時與載入時間戳 |
| `pclam.pmlmac`、`pclam_check.pmlmac`、`pclam_nnnn.OUT` | 執行用 PML 巨集，及每個檢查元素各一個輸出檔 |

### 45.3.7 重跑、狀態演算與維護

重跑時，若兩筆碰撞明細在**同一對元素且位置在分組容差內**，視為同一筆。比較新舊 Level/Type：變差則修訂狀態；若有接受規則適用則依規則重算，無規則則設為預設值；相同或較好則不動。全部處理完後，每個受影響群組的狀態**重設為其成員明細中最差者**。

進階工作（Options 表單的 Advanced 分頁，限 Admin Supervisor）：

進階工作（Options 表單的 Advanced 分頁，限 Admin Supervisor）：**Track Changes** 建立里程碑供趨勢圖；**Recompute Properties** 在組態或模型大改後重算；**Load Clash File** 在載入被中斷時整批載入或合併進最近一次執行；**Reset Group Status／Owner** 在群組內明細一致時提升到群組；**Delete All Unreferenced Groups, Elements and Comments** 清除失效明細（**備註一併消失**）；**Delete All Clash Data** 專案結束時清空碰撞資料與歷史（保留組態與 Clash Set 定義），有兩次確認且**不可還原**。

專案層級報表，官方列出四種方式：Business Objects（官方建議，需 BO universe）、Track Changes 里程碑、Microsoft Excel（定期存主表統計自行做趨勢）、螢幕截圖。

**效能提示：** 「Worst Case Update Threshold」設太低會嚴重拖慢；Clash History Count 越大越慢；批次改多個群組狀態時關掉 `Auto View` 與 `Auto Display Clash Detail`。

> **專業提醒：** Clash Set 數量要克制。官方經驗是專案初期常建立上百個，之後被迫整併為數十個。盡量用萬用字元建清單，新增的 Zone 才會自動納入。

### 45.3.8 底層引擎：DESCLASH 指令（Design Reference）

Design Reference 的 Utilities 記錄了指令式引擎：`DESCLASH` 進入碰撞檢查模式（選項全域保存、`EXIT` 離開），以 `OBSTRUCTION`／`EXCLUDE` 累加障礙清單、`LIMITS` 限制範圍、`TOUCHING`／`CLEARANCE` 設定觸碰（預設 overlap 2 mm、gap 0）與間隙，`ACHECK`／`BCHECK` 對應 Run Clash Set 的 A／B Check，`CHECK`、`BOXCHECK`（只做障礙盒重疊的第一階段）、`CHECKADD` 執行，並可用 `Q CLASH 2 FIRST／SECOND／TYPE／POSITION／ALL` 直接查詢。判定依圖元 `OBST` 屬性：`2` 為硬障礙、`1` 為軟障礙（`0` 的語意以原頁為準〔待核對〕）。檢查分兩階段：先比障礙限制盒，重疊再比實際幾何。

### 45.3.9 常見錯誤

| 錯誤 | 建議 |
|---|---|
| 組態與 GUI 篩選用了同一套萬用字元 | 組態用 Regular Expression，篩選用 `%`、`_` |
| 規則裡想寫 OR | 沒有 OR，拆成多條規則 |
| 專案中途改群組距離 | 初期就與各專業主設計者定案，否則要重算 |
| 並行執行多個 Clash Set | 依序執行，避免 Oracle 資料爭用 |
| 清除失效資料前沒保存備註 | 歷史備註會永久遺失，先匯出報表 |
| 把 Conditional 當成「核准」 | Conditional 是「已解決、待重跑確認」，Approved 才是接受 |

## 45.4 Data Checker：資料檢查

### 45.4.1 它是什麼

Data Checker 是官方提供的「資料一致性檢查框架」：**用 PML 寫檢查函式，再以設定檔註冊，標準的使用者介面、螢幕與檔案報表、點擊導航到失敗元素等功能都由框架提供。** 官方明說可快速把公司或專案的檢查加進 Design。入口在任何 Design 應用程式的 `Utilities > Data Checker`，開啟 Checker 視窗。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Checker 視窗，含 Check Items、Classes、Groups、Checks

*圖 45-10　Checker 視窗：上方 Check Items 是要檢查的元素，下方依 Classes → Groups → Checks 逐層選擇檢查項目，按 Check 執行。（AVEVA 官方文件截圖，僅供內部教學）*

### 45.4.2 使用步驟

**步驟 1：指定要檢查的元素**（Check Items 清單）。

| `Add` 選項 | 加入的內容 |
|---|---|
| `CE` | 目前元素 |
| `CE Members` | 目前元素的所有成員（不含自己） |
| `Pick` | 在圖形視圖挑選 |
| `Failed List` | 上一次檢查失敗的所有元素（修正後複查用） |
| `List list_name` | 以 `Utilities > Lists` 建立的清單，可用選取規則（如 `all pipes with pspec eq /A1A`）或體積建立 |

`Remove` 選單對應有 `All`、`Selected`、`CE`、`CE Members`、`Pick`、`List`。

**步驟 2：選檢查函式。** 依 Class（通常對應專業）→ Group → Check 三層選。官方附帶的標準檢查如下。

標準檢查的 Class／Group 包含：Rules & Connections（Rule Errors、Connection Errors 等）、Steelwork（Sections）、HVAC（Branches、Components、Rectangular Tapers、Branch Connectors、Flexible Ductwork、Implied Tube）、Cabling App（Cableways、Trays、Penetrations）、Hole Management（PIPE、HVAC、ATTA Checks）。

Hole Management 檢查有重要限制：它們只回報「目前孔小於需求孔」，孔較大視為通過；穿透管徑變了而 `ATTA` 尺寸沒變時偵測不到，要靠 Data Consistency Checks 補。`ATTA Checks` 找出 `ATTYPE = PENI` 卻沒被任何 Hole Management 關聯參照的孤兒 `ATTA`，常見於複製含穿孔 `ATTA` 的管，或不經 Hole Management Delete 就刪了資料。

**步驟 3：高亮與執行。** `Highlight` 選單可把檢查項目、通過者、失敗者以不同顏色標在圖形視圖（只有已在 Drawlist 的元素會被標示）。按 `Check` 後開啟 Checker Results：Passed 清單與 Failed 清單，失敗者附簡短原因，點選即可導航到該元素。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Checker Results：Passed 與 Failed 清單

*圖 45-11　Checker Results：綠色為通過（58 筆），紅色為失敗（73 筆），失敗項目列出元素與原因（例中為 End Connections：Section End is unconnected）。（AVEVA 官方文件截圖，僅供內部教學）*

**步驟 4：保存與重載。**

存檔與重載：`Control > Save > Results` 存通過與失敗結果；`Control > Save > Failed Reference` 只存失敗元素的資料庫參照與所做檢查，日後可用 `Control > Load > Failed References` 重新載入複查；修改或新增檢查後用 `Control > Reload Checks` 更新清單。

> **專業提醒：** 檢查前先清掉「資料一致性」問題。官方在 Hole Management 檢查處就警告：有資料一致性錯誤時，驗證失敗可能被漏掉。順序應是先一致性，再專業規則。

### 45.4.3 新增自訂檢查：設定檔

自訂檢查的註冊檔名為 `des-checks.pmldat`，**AVEVA 自帶檢查在 `com-checks.pmldat`，不可修改**。使用者檔放在三處，載入時合併顯示：

| 目錄 | 範圍 |
|---|---|
| `PDMSDFLTS` | 公司層級，所有專案可用 |
| `ABCDFLTS`（ABC 為專案名） | 專案層級 |
| `PDMSUSER` | 單一使用者 |

每個檢查條目依官方範例如下（`--` 開頭為註解）。

```
!Check = object CHECK()
!Check.Name     = 'LOOPCHECK'
!Check.Title    = 'Check Panel Boundary'
!Check.Class    = 'Steelwork'
!Check.Group    = 'Panels'
!Check.Types    = 'PANE'
!Check.Rule     = ''
!Check.Function = '!!EdgeCheck'
!Check.Module   = 'Design'
!Check.FileType = '$1'
!!AddCheckerCheck(!Check)
```

| 成員 | 說明 |
|---|---|
| `.Name` | 檢查名稱，唯一 |
| `.Title` | 顯示在 Checks 選擇框與失敗清單中的標題 |
| `.Class`、`.Group` | 歸屬的類別與群組 |
| `.Types` | 要送進函式的元素類型，空白分隔，例如 `'PANE SCTN FRMW SBFR'` |
| `.Rule` | 對 `.Types` 再過濾的規則，例如 `'FUNC OF ZONE eq \|PS\|'` |
| `.Function` | 檢查函式名，**必須以 `!!` 開頭**，且須在 PMLLIB 搜尋路徑中 |
| `.Module` | 可執行的模組，如 `'Design'` |
| `.FileType` | 官方註明「必要的一行」，範例固定為 `'$1'` |

函式檔名規則：函式 `!!PSNameCheck` 對應檔 `psnamecheck.pml`（全小寫加 `.pml`）。**同一 Class 與 Group 內的所有檢查，`.Types`、`.Rule`、`.Module` 必須完全相同**，否則多項檢查同時執行時結果不可靠。

### 45.4.4 檢查函式的寫法

官方規格：

```
define function !!FunctionName ( !ItemRef is DBREF, !Check is CHKDEFINITION ) is CHKRETURN
```

- `!ItemRef` 是待檢元素的 `DBREF`，`!Check` 含設定檔資訊，**兩個參數都是唯讀，不可在函式內重設**。
- 回傳值必須是 `CHKRETURN` 物件，包含 `.Passed`（BOOLEAN）與 `.Messages`（ARRAY，通過時為空，失敗時至少一筆）。
- 建議開頭初始化，失敗時設 `.Passed = false` 並 `append` 訊息，最後 `return !Result`。
- 函式可在第一個錯誤就回傳，也可收集多個錯誤。若函式本身出錯，框架會把它記在失敗清單。

官方範例一（面板邊界檢查）示範：以 `( PLOOP 1 OF $!PanelRef )` 取面板輪廓並用 `Handle any ... endhandle` 處理不存在的情況；以 `VAR !Vertices COLLECT ALL PAVE FOR $!PloopRef` 收集頂點；頂點少於 3 個、或相鄰頂點距離小於 0.01 mm 就設 `.Passed = false` 並 `append` 訊息後 `return !Result`。

範例二（鋼構名稱檢查）以 `!ZoneRef.attribute(':PRODNO')` 讀 Zone 上的 UDA，檢查 `SCTN`、`PANE`、`FRMW`、`SBFR` 名稱前兩碼是否等於生產編號前兩碼，並以 `!Name.substring(1,1) eq '='` 判斷尚未命名。兩個範例都附有輸出報表（通過與失敗清單及訊息）。

修改設定檔後要 `Control > Reload Checks`；函式檔搬動位置則需重啟或執行 PML `REHASH`。

> **專業提醒：** 官方範例的函式簽章寫 `CHKDEFINITION`，但「Checker Objects」小節與設定檔說明有處寫成 `CHECKDEFINITION`。實作時以你們版本實際可編譯者為準〔待核對〕。

### 45.4.5 與 Design Reference 的 DATACON 對照

Design Reference 另有指令式的 Data Consistency Checking Utility（DATACON）：`CHECK /ZONE-1`（一次最多 10 個元素）、`TOL OFFSET 1`、`TOL TUBE 100`、`MAXANGLE`、`ECC SECT DIST 1`、`SECTION DEFAULT 1000 9500` 等，檢查管路連接、偏移、最小管長、彎頭角度與結構斷面、接點的偏心與長度。無問題時輸出 `*--*  NO DATA INCONSISTENCIES  *--*`，診斷訊息有代碼（如 `A 10 HEAD REFERENCE NOT SET`、`D100 REFERENCE SPREF UNSET`）。這是標準檢查背後的邏輯，與自訂檢查互補。

### 45.4.6 常見錯誤

| 錯誤 | 建議 |
|---|---|
| 修改 `com-checks.pmldat` | 只改 `des-checks.pmldat`，否則升級被覆蓋 |
| 同組檢查的 `.Types` 不一致 | 依 Class／Group 分組，結果才可靠 |
| `.Function` 忘了 `!!`，或檔名大寫 | 檔名全小寫，放在 PMLLIB 路徑 |
| 在函式裡改 `!ItemRef` 或 `!Check` | 官方明列禁止，只讀不寫 |
| 在檢查函式內修改模型 | 本章建議唯讀（文件未明說）〔待核對〕 |

## 45.5 Design Model Editor：圖形化模型操作

### 45.5.1 三種 3D 視圖模式與術語

3D View 有三種模式：**Navigate**（預設，點選即導航並成為 CE）、**Event Driven Graphics（EDG）**（滑鼠點選作為事件驅動指令的一部分）、**Model Editor**（選取元素後動態移動或旋轉）。EDG 與 Model Editor **不能同時進入**。以工具列的 Model Editor 按鈕或 `Edit > Model Editor` 切換。

| 術語 | 說明 |
|---|---|
| Graphical Selection | 準備用 Locator Handle 操作的一個或多個元素 |
| Selection Set | Navigate 模式下一次點選選到的元素；設備選整個圖元，管件會連帶選到相連元件 |
| Locator Handle | 一組把手，提供定位與定向 |

選取外觀：可修改者以**綠色線框**高亮，無權限者以**紅色線框**；但操作是否被接受最終仍由 Data Access Control 決定。

### 45.5.2 選取規則

| 情況 | 行為 |
|---|---|
| 選管件（如閥） | 連帶選相關法蘭與墊片；到方向改變處（如彎頭）為止 |
| 選彎頭 | 只選彎頭本身與相連的零長度元件（如焊口） |
| 左鍵 | 選元素與相連元素 |
| 右鍵 | 只選指標下的元素 |
| `Select > Connected`／`Leg` | 選相連元件／同一管段 |
| `Select > BRAN`／`PIPE` | 選所屬分支／管線 |
| `Ctrl` + 點選 | 加入或移出選取 |
| 框選 | `Wholly Within` 或 `Wholly And Partially Within`，由右鍵框選設定 |
| `Edit > Re-Select` | 找回上一次選取 |
| 離開 Model Editor | 清除選取，但可用 `Re-Select` 還原 |

官方特別設計：**相連的零長度或不可見元件，永遠不會因鄰件被取消選取而落單。** 可修改的元素類型列於 Selectable Items，包含 `EQUI`、`PIPE`、`BRAN`、管件、`HVAC`、`REST`、`HANG`、`PTRA`、`RPLA` 等；鋼構 `SCTN` 屬於 `FRMW` 或 `SBFR` 時可移動，屬於 `TMPL` 時不行。

### 45.5.3 Locator Handle：移動與旋轉

> 〔公開版未收錄：AVEVA 官方產品截圖〕Locator Handle 示意：沿軸移動、平面移動、單軸旋轉

*圖 45-12　Locator Handle：三根線性把手沿軸向移動、三個平面把手限制在平面內移動、三段弧形把手繞單軸旋轉。（AVEVA 官方文件截圖，僅供內部教學）*

三種移動／旋轉方式：直接拖曳把手、與其他元素的特徵對齊、輸入偏移或角度值。要點：

- 拖曳以 **Movement Increment** 為步距，可用 `Selection > Set Increments` 設定；拖曳中按 `+`、`-` 一次移動一個增量以微調。
- **Feature Highlighting**：`Selection > Feature Highlighting`，或滑鼠在視圖上時按 `F` 切換。開啟後拖曳會吸附到點、線、P-point 與 P-line；Design Aid 圖形不能當特徵。
- Locator Handle 可**脫離 Graphical Selection 單獨移動**（按住把手再按 `H` 切換），用來設定基準點或旋轉軸。
- 非受約束定位：`Move Selection／Handle` 提供 `Offset in 3D`、`Set 3D Position`、`Snap to Point`；旋轉有 `To World`（Y 指北、Z 指上）與繞 X／Y／Z。
- 若要區分只動選取或只動把手，選 `Move Selection` 或 `Move Handle`。

### 45.5.4 設備圖形修改（GEM）與元件圖形修改（GCM）

進入 Model Editor 後，對 `EQUI`、`STRU`、`SUBS`、`VOLM`、`SVOLM`、`PTRA`、`AREADE` 右鍵選 `Edit Equipment` 等，即進入 Graphical Equipment Modification，可往下編輯圖元層級，其他非設備項目會變半透明，負圖元以線框顯示；離開用 `Exit Equipment Editor`。

**Graphical Component Modification（GCM）** 在 Model Editor 點選管件時自動進入，不需開啟 Pipework 應用程式，可沿管路移動元件並繞管中心線旋轉。

> 〔公開版未收錄：AVEVA 官方產品截圖〕GCM 的元件修改把手：沿管路方向的移動把手與繞管軸的旋轉把手

*圖 45-13　GCM 把手：洋紅色線沿管路方向表示移動，弧形箭頭表示繞管中心線旋轉；可被拖入的管段以青綠色標示。（AVEVA 官方文件截圖，僅供內部教學）*

GCM 規則：把手只在選取集為「單一進出方向平行的元件」或「同一管段內相連的一組元件」時出現；必須有足夠 implied tube 容納；移動後資料庫階層順序自動調整；快捷鍵 `Esc` 中止、`F` 特徵高亮、`P` 循環候選位置、`+`／`-` 增量、`D` 切換尺寸回饋（到上下游元件、到 Branch Head／Tail）；旋轉可繞管中心線 360°，右鍵拖曳放開時會出現確認或取消選單。

Undo／Redo 在 Model Editor 內可一步步退回；其他可還原操作可定義成 PML undoable 物件〔待核對〕。

### 45.5.5 檢視與剪裁

視圖操作入口有 `View` 選單、右鍵選單、3D View Manipulation Toolbar、功能鍵（`F2` 縮放、`F3` 平移、`F5` 旋轉）與滑鼠中鍵。**Clipping** 可設為 CE、Owner、Limits Box 或 Pick，**Six-Plane Clipping** 最多六個任意角度平面（與剪裁盒互斥）。**Save and Restore Views** 保存 Drawlist、視圖屬性與縮圖，縮圖只是存檔當下的圖片，元素若已刪除，還原後可能是空視圖。

> **專業提醒：** 只顯示必要元素；不要大量選取，批次移動分小組做；不要顯示孔洞或細圓弧容差。

### 45.5.6 常見錯誤

| 錯誤 | 建議 |
|---|---|
| 用 Move 搬設備、期待管跟著動 | 用 `Position > Drag` |
| 對紅色線框元素硬移 | 會被 Data Access Control 拒絕，先確認權限，見第 [20 章](ch20_system_administration_zh-TW.reading.html) |

## 45.6 Reporting 與 Reporting Reference

### 45.6.1 先分清兩套報表工具

| 項目 | Reporting（Report Designer） | Reporting Reference（Standard Reporting） |
|---|---|---|
| 性質 | 圖形化視覺報表設計器 | 表單式範本，輸出純文字 |
| 檔案 | 版型 `.repx`、報表定義 `.repv` | 範本 `.tmp`、報表 `.rep` |
| 資料來源 | Database Views、User Views、Data Source Wizard、Search Grid | 以 Hierarchy、Type(s)、With 條件直接選元素 |
| 批次 | PML 物件 `PMLREPORT()` | 範本即巨集：`$M/template-name` |
| 輸出 | 預覽、列印、PDF、RTF、HTML、XLS 等 | 螢幕、檔案、CSV |

**選擇原則：** 需要版面、圖形、頁首頁尾、圖表的正式交付物，用 Report Designer；快速、純文字、可由巨集呼叫的清單，Standard Reporting 仍很好用。第 [16 章](ch16_reports_integration_zh-TW.reading.html)談的是用 PML 自行寫檔與 CSV／Excel，並不重複本節。

### 45.6.2 Report Designer：概念與流程

兩種檔案是核心概念：**Layout Template（`.repx`）只有格式、圖形與呈現，沒有資料來源，不能執行**，用來統一全公司或專案的版面風格；**Report（Report Definition，`.repv`）含版面與資料來源，可執行**。`.repv` 可另存為 `.repx`（會警告資料來源將被捨棄）。範例報表在 `PDMS Installation Location\PDMSUI\dflts\data\reports`，同時有版型與報表。

存放位置分三層：Product `%PDMSDFLTS%\Data\Reports`、Project `%<PRJ>INFO%\Reports`、User `%PDMSUSER%\Data\Reports`，也可 Browse 到其他資料夾。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Report Designer 的整體工作流程圖

*圖 45-14　Reporting 工作流程：開啟 Report Designer 後，分別開啟版型或報表定義；報表定義可預覽、改版面、重新指派資料來源、綁定欄位，再儲存或執行。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Report Designer 主畫面，含 Tool Box、設計區、Field List 與 Property Grid

*圖 45-15　Report Designer：左為 Tool Box（含 AVEVA 專屬的 Project Info），中間為各 Band，右為 Field List 與 Property Grid；上方工具列有 Data source、Scope、Run Report。（AVEVA 官方文件截圖，僅供內部教學）*

**資料來源（Data Source）。** 按 `Data source` 開啟 Data Source Wizard：`New`、`Copy`、`Edit`。新資料來源要選至少一個 Base Element Type。資料來源分三類：

資料來源有三類：**Element**（系統為每個基本元素類型自動建立一個視圖，最簡單）、**Project**（存在 Lexicon 字典資料庫，需讀取權，通常由管理者設定並附範例）、**User**（使用者本機儲存的查詢）。

`Scope` 按鈕再限制資料範圍：只檢視指定元素及其以下階層；勾選 `CE` 則範圍隨目前元素變動。一份報表只能綁 Dabacon 專案資料或其他資料庫其中之一，不能兩者同時。也可綁定 Access 等非 Dabacon 資料來源，透過資料連結精靈。

**報表結構。** 報表由「帶（Band）」組成：Report Header／Footer（整份一次）、Page Header／Footer（每頁一次）、Detail（每筆資料一次，**不可刪除**）、Group Header／Footer（每組）、Page Margin、Detail Report（主從式報表）。控制項（Control）有 Label、Table、Chart、Pivot Grid、Page Info、Rich Text 與 AVEVA 專用的 Project Info 等。資料綁定的控制項右上角有黃色資料庫圖示，從 Field List 拖到控制項或 Band 即可綁定。

編輯重點（官方）：排序在 Detail Band 的 Smart Tag 設 Sort Fields（可多欄）；篩選用報表的 `Filter String` 屬性；分組加入 Group Header band 並設 Group Fields；合計把欄位以 Ctrl 拖到 Report Footer 後設 `Summary`；計算欄位用 Field List 右鍵 `Add Calculated Field`（**匯總欄位不能用於計算欄位**）；參數用 Parameters 右鍵 `Add Parameter`，每次預覽都會詢問；浮水印只在預覽與 HTML View 顯示，匯出 HTML 不含。

報表型態有 Static、Table、Master-Detail、Multi-Column、Cross-Tab（Pivot Grid）、Parameterized 與 Chart，並可建立書籤、超連結與交叉參照。

**預覽與執行的差異（常見陷阱）。** 預覽只取前 **20 筆**並快取，資料變動不會即時反映，需 `Run Report` 或重新開啟；Quick Report 的預覽則顯示全部資料。`Run Report` 才取回全部資料，並可列印、匯出多種檔案格式，或以 PDF 發佈到 AVEVA Asset Information Management（含關聯，需設定）。匯出多位元組字元（如中文）時，官方建議用支援多位元組的 Arial Unicode MS 字型。

**Run Report 視窗**可不開設計器直接執行，從 Product、Project、User 或 Browse 選擇，預覽顯示前 20 筆，有參數或範圍時會先詢問。**Quick Report** 則從 Search Results 格線欄位標題右鍵 `Quick Report` 進入，可把常用 Saved Search 與版面存起來重複使用。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Run Report 視窗，列出 Product 位置的範例報表並顯示預覽

*圖 45-16　Run Report：左側列出範例報表（如 `DESIGN-Nozzle_Schedule`、`DESIGN-Pipe_List`、`DESIGN-Steel_MTO_ByZone`），右側顯示版面預覽（前 20 筆）。（AVEVA 官方文件截圖，僅供內部教學）*

**實數顯示。** 實數小數位由 `PRECISION` 指令控制；批次模式若不是在 TTY 模式建立格式，結果可能不同，官方建議在巨集中初始化 `!!comDefineGlobal(object COMFORMATS())`，帶單位的實數可用 `FormatDouble` 格式化。資料來源取值出錯（例如 PML1 運算式錯誤）時，欄位顯示 `!!Error`。

### 45.6.3 Standard Reporting（Reporting Reference）：範本式報表

操作入口 `Utilities > Standard Reporting > Reports`，有 `Create`、`Run`、`Modify`、`Delete`。範例範本在 `%PDMSUI%/REPORTS` 的 `TEMPLATES` 目錄，副檔名 `.tmp`，產生的報表 `.rep`；範本本質是 PDMS 巨集；要使用範例需設定變數 `$PDMSREPDIR`。

官方範例範本與用途：

| 範本 | 內容 |
|---|---|
| `nozz_sched` | 噴嘴（Nozzle）清單：依名稱排序，列 P1 口徑、連接型式、方向與位置 |
| `line_list` | 分支清單：依所屬管線名排序 |
| `pipe_mto` | 管路 MTO（各項目類型數量） |
| `centre_line` | 中心線長度報表 |

建立步驟（以官方的簡易 Nozzle Schedule 為例）：

1. `Utilities > Standard Reporting > Reports > Create`，開啟 New Report Template。
2. Destination 選 Screen；Type(s) 輸入 `NOZZ`；Hierarchy 以 `/E1301`（**元素名必須以 `/` 開頭**，可空白分隔多個）取代 `WORLD`。
3. Columns 以 `New` 建欄：第一欄 Expression `NAME`、第二欄 `P1 BORE`（Units 選 mm）、第三欄 `POS`。每欄 Expression 可為屬性、偽屬性或運算式。
4. `Apply` 即執行並顯示於視窗。

`Column Layout` 可調整 Spaces before Column、Column width、Justification、Numeric Display 與標題文字（表達式文字、預設屬性全名或自訂）。

**執行時提示（Runtime Prompts）** 可決定報表執行時詢問哪些項目：File name、Type(s)、With、Hierarchy、Volume、From。

**選取範圍。** Hierarchy 列出頂層元素（含其擁有者以下）；Volume 為 `Completely within` 或 `Partially within` 限制盒（從整個 MDB 選，此時 From 不可用）；From 可選 `MDB`、`Drawlist`、`Obstruction list`（後兩者 Hierarchy 留空）；With 以運算式篩選，如 `(ABORE GT 50) AND (ABORE LT 100)`，運算子 `EQ NE GT GE LE LT`，可用 `AND OR NOT`。

**排序與合計。** 每欄可設 Sorting（0-9、9-0、Aa to zZ 等）與 Precedence（排序優先序）；`Totalling` 對數值欄加總；`Subtotals` 設為某排序欄的編號，即在該欄值改變時小計；`Values` 選項（On、Off、`1st`、`Sub`）控制重複值的顯示。官方 `pipe_mto` 的設計是：以 TYPE 與 DTXR 排序，ITLE 與 QUANTITY 欄 `Subtotals` 設為 2，讓相同 Detail Text 的項目合計。

**檔案報表。** Destination 設為 File，檔案存在 `PDMSUSER/REPORTS`；檔案已存在時可選 `Append`、`New`（確認覆寫）、`Overwrite`（不警告）。只有檔案報表才有頁首、頁尾、頁長（**需 5 到 500 行**才顯示頁首頁尾）、Introduction 與 Summary。特殊變數有 `!pageno`、`!date`、`!time`、`!filename`、`!seltype`、`!selhierarchy`、`!selvolume`、`!selfrom`、`!criteria`、`!selsize`（符合元素數）、`!selno`（元素序號，需搭配欄位 Sort 設為 Fix），**必須搭配延遲求值函式** `vtext`（文字）、`vlogical`（邏輯）、`vvalue`（數值），否則按 OK 時就會立即求值。官方範例：`'Page No. ' + vtext (!pageno)`、`'Summary: ' + vtext(!selsize) + ' Nozzles in Schedule'`；文字用單引號，多段以 `+` 連接。

其他：`System Command` 欄位可在報表完成後執行系統指令（如送印表機）；`Options > Other Formats` 可輸出 CSV 並設定分隔符與文字界定符；**批次模式範本不可設任何 Runtime Prompts**。

### 45.6.4 常見錯誤

| 錯誤 | 建議 |
|---|---|
| 以為預覽就是完整結果 | 預覽只有前 20 筆，用 Run Report 驗證 |
| 把 `.repx` 當報表執行 | 要執行的是 `.repv` |
| `.repv` 另存 `.repx` 後仍期待有資料 | 資料來源已被捨棄 |
| Standard Reporting 的 Hierarchy 漏寫 `/` | 名稱一律以 `/` 開頭 |
| 頁首變數沒用 `vtext` | 變數會在儲存範本時就被求值 |
| 批次範本留著 Runtime Prompts | 批次前關掉所有提示 |

## 45.7 二次開發者怎麼接

| 對象 | 擴充方式（官方依據）與注意 |
|---|---|
| Data Checker | `des-checks.pmldat` 註冊 + `.pml` 檢查函式 + `CHKRETURN` 物件；45.4 有完整規格與範例，是最穩的 PML 擴充點 |
| Reporting（Designer） | PML 物件 `PMLREPORT()` 可程式化執行報表、支援批次；**方法名稱與參數本章引用的頁面沒有，只指向 Software Customization 文件〔待核對〕** |
| Standard Reporting | 範本即巨集，可用 `$M/template-name` 批次呼叫；運算式可含 PML 變數；批次範本不可有 Runtime Prompts |
| Clash Manager | `mmscmd ... -clash` 命令列與 `pclam.*` 記錄檔；官方未說明資料表結構，不可直接讀寫庫表〔待核對〕 |
| Model Editor | 可還原操作可定義為 PML undoable 物件，細節在 Software Customisation Guide〔待核對〕 |

`excelio` 的官方介面如下：

```
!e = object excelio()
!result = !e.import('<filename>')                       -- 自動對應：工作表名 = 元素類型、欄名 = 屬性名
!result = !e.import('<filename>','<configname>')        -- 使用已儲存的組態
!result = !e.export('<filename>','<configname>')        -- 匯出
```

三個方法回傳 `-1` 錯誤、`0` 成功、`1` 警告。第一種呼叫會「盡力猜測」對應，**所有識別出的變更都會直接套用到資料庫，沒有預覽確認**；GUI 版則會先列變更摘要，可選擇接受哪些。官方註明 Excel 匯入匯出目前只在 AVEVA Diagrams、Schematic Model Manager 與 Tags 中可用，所以對 Design 模組是否可用須在你們的版本確認〔待核對〕。Import Data（CSV／XLS 預填設備）的檔案規則：首列為標題；必須有 `NAME`（既存名稱視為更新列）與 `TYPE` 欄（元素類型或 UDET，如 `:PUMP`）；可選 `OWNER` 欄，只對新建元素有效，既有設備不能改擁有者；它是兩階段流程，先分析並回報錯誤，再選擇匯入。

相關章節：PML 基礎見第 [11 章](ch11_pml_language_zh-TW.reading.html)、第 [13 章](ch13_pml_forms_addins_zh-TW.reading.html)；階層與 UDA 見第 [3 章](ch03_hierarchy_attributes_zh-TW.reading.html)；圖面見第 [9 章](ch09_drawings_zh-TW.reading.html)；纜線與 Data Checker 的纜線檢查見第 [26 章](ch26_cable_supports_zh-TW.reading.html)；結構面板與孔見第 [22 章](ch22_structures_zh-TW.reading.html)。

> **專業提醒：** 開發者最安全的切入順序是：**先寫 Data Checker 檢查（唯讀、官方有範例）→ 再用 Reporting 範本輸出清單 → 最後才考慮批次模型修改。** 前兩者不寫入資料庫，出錯的代價低。

## 45.8 本章小結

- **共通功能**：System Hierarchy 提供跨區系統視圖；Hole Management 以受管孔與 REQUESTED／APPROVED 狀態管理穿孔；Move 與 Drag 不同。
- **Clash Manager**：引擎之上的記錄、分組、指派與核准系統；規則 AND-only；組態用 Regular Expression、篩選用 `%`／`_`；批次 `mmscmd -clash` 依序執行。
- **Data Checker**：PML 擴充點，`des-checks.pmldat` 註冊、`.pml` 實作、回傳 `CHKRETURN`。
- **Model Editor**：Locator Handle 與 GCM；Navigate、EDG、Model Editor 互斥。
- **Reporting**：兩套工具（`.repx`／`.repv` 與 `.tmp`／`.rep`），預覽只取 20 筆。

## 45.9 練習題與自我檢核

**練習（只能在訓練專案）**

1. 以 `Utilities > Systems` 建立 `SYGPWL`／`SYGPAR`／`SYSGRP` 結構，加入三個跨 Zone 的 HVAC 分支，比較 Main Systems 與 Owning Systems 分頁。
2. 建立 Clash Set（障礙為結構、檢查為管路），Group 距離 1000 mm 執行後，改 100 mm 重算，比較群組數量。
3. 在 Accept 分頁寫一條「Support 與管路的 Touch、Clear 自動接受」規則，先用 Test Rules 驗證。
4. 依 45.4.3、45.4.4 寫一個檢查 `SCTN` 名稱不得為空的 `des-checks.pmldat` 與 `.pml`，`Reload Checks` 載入並驗證 `Save > Failed Reference` 與 `Add > Failed List`。
5. 開啟 `DESIGN-Nozzle_Schedule` 只改版面另存 `.repx`，確認它不能直接 Run；再以 Standard Reporting 建立相同內容清單並比較。

**自我檢核**

- [ ] 我能說出 Hole Management 的三個名詞與狀態流程，並區分 `DESCLASH`、Clashes 視窗與 Clash Manager。
- [ ] 我能說明 Conditional 與 Approved 的差異、規則為何只能 AND、批次為何要依序。
- [ ] 我知道 `Move` 與 `Drag`、`.repx` 與 `.repv` 的差別，以及 `vtext` 延遲求值為何必要。

## 45.10 〔待核對〕項目彙整

1. Hole Management 在 Global 專案的 extract 與 claim 細節（以官方 Global 文件為準）。
2. `OBST = 0` 的語意。
3. Data Checker 函式簽章 `CHKDEFINITION` 與 `CHECKDEFINITION` 拼法不一致。
4. 檢查函式是否允許寫入資料庫（本章建議唯讀）。
5. `PMLREPORT()` 的方法、參數與回傳值。
6. Model Editor 的 PML undoable 物件定義方式。
7. `excelio` 在 Design 模組是否可用。
8. Clash Manager 資料庫結構與可程式化存取方式。
9. `PDMSUI`、`PDMSDFLTS` 等舊路徑變數在 12.1 實際安裝是否相同。
10. Clash Manager 的 Model Management Wizard 與獨立版建立流程未讀。

## 45.11 取材範圍（誠實揭露）

本章對應的 *Design* 節點約 911 頁，**沒有逐頁讀完**。實際閱讀如下。

- Data Checker Utility（17 頁）：全部讀完。
- Clash Manager（177 頁）：約 89 頁；概念、設計工作流程、Procedures、Entry Information、Performance Hints、`mmscmd` 全讀，GUI 僅讀 Clash Manager、Run Clash Set、Configuration 各分頁與 Test Rules。
- Design Common Functionality（105 頁）：每頁讀開頭約 1500 字元，概覽級。
- Design Model Editor（80 頁）：約 73 頁，多數截取前約 1100 字元。
- Reporting（136 頁）：約 80 頁；Reference 中 Report Settings、Report Controls、Styles and Conditional Formatting 細節未讀。
- Reporting Reference（46 頁）：全部讀到，每頁約前 1300 字元。
- Design Reference（344 頁）：僅約 62 頁（Utilities 的 Data Consistency Checking 與 Clash Detection）；**Creating a Model、General Commands、Display、Interacting with a Graphical View、Error Messages、Copying Model Data from Marine to Review 均未讀**。

未讀或只略讀：Clash Manager 的 Clash Report、Filter、Consolidated Report、Element Report、Options 表單頁、Model Management Wizard；Reporting 的控制項與帶屬性參考；Schematic Gateway；Design Reference 的指令語法圖整體。總計約 470 頁有不同程度閱讀，其中完整讀完的約 100 頁。圖片 16 張來自官方文件，皆已逐張預覽確認。

## 資料來源

- AVEVA Marine 12.1 官方離線文件：*Design*（頁面 ID 1105732）及其子節點 Clash Manager（1151437）、Data Checker Utility（1140310）、Design Common Functionality（1140385）、Design Reference（1225246，僅 Utilities 部分）、Design Model Editor（1140903）、Reporting（1154116）、Reporting Reference（1156876）。
