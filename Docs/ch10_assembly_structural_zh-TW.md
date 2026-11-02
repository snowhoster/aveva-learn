# 第 10 章　裝配規劃與船體結構初步設計：Assembly Planning 與 Hull Structural Design

> 前面的章節把船體模型建出來了，這一章處理兩件「模型之外」的事：**第一，把設計模型重新整理成生產用的組立樹，並自動產出組立圖與零件表（Assembly Planning）；第二，在尚未進入詳細設計之前，用最少的資料快速建出主結構，估算鋼料、重量與焊接量，並平順交給詳細設計（Hull Structural Design）。**
>
> 兩者剛好位於設計流程的兩端：Structural Design 在前端，決定「大概長什麼樣、夠不夠強」；Assembly Planning 在後端，決定「怎麼分、怎麼組、先裝哪個」。從資料庫角度看，前者建立的是設計物件（RSO、Panel、Block），後者在旁邊另建一棵只用代理（proxy）指向設計物件的樹。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的 Assembly Planning（含 Admin、Assembly Drawing、Assembly Planning 三部分）與 Hull Structural Design 各功能選單頁。Planar／Curved 選單因與[第 13 章](ch13_hull_detail_planar_zh-TW.reading.html)與第 14 章重疊，只讀各功能的用途摘要，未逐頁讀操作細節。文中所有屬性名、指令、檔名、環境變數均出自官方頁面；官方頁面沒有寫的行為（例如組立樹與 Weld Planning 的實際資料交換欄位）標〔待核對〕。版本為 12.1，部分畫面為舊版介面截圖。章末列出實際閱讀範圍。

## 10.1 學習目標

讀完本章，你應該能夠：

1. 說明 Assembly Planning 要解決的問題，以及組立樹（production breakdown structure）與設計樹的差別。
2. 說出 `ASWL`、`ASMBLY`、`ASITEM` 三種元件的關係，並解釋為什麼零件只能屬於一個組立。
3. 使用 Assembly Planning 視窗建立組立樹、收集（collect）零件、設定組立方向（`ASORI`）並播放裝配順序。
4. 描述 Assembly ADP 的資料結構：Drawing Template、Backing Sheet、Task、Parts List Template 與組態檔 `assydrwg.cfg`。
5. 以 Assembly Drawing 工具列產生單張、整棵樹、多選與批次的組立圖及零件表。
6. 說明 Hull Structural Design 的四大目標：快速建模、早期分析與估算、出圖、平順轉入詳細設計。
7. 說明 RSO（Reference Surface Object）如何變成 Functional Structure，再自動產生 Functional Panel。
8. 列出 Project、Functional Structure、XML、Analysis 四個選單的主要功能與使用順序。
9. 使用 Block CSV、`sj701`～`sj706` 批次程式處理分區與 RSO 資料，並知道 `sj700.sbd` 預設檔可調的參數。
10. 辨別哪些介面有官方依據可做二次開發（PML、PMLNet、`.uic`），哪些仍須〔待核對〕。

## 10.2 兩個模組在整體流程中的位置

| 階段 | 模組 | 主要輸出 |
|---|---|---|
| 初步設計 | Hull Structural Design | Functional Panel、重量重心、鋼料表、焊接長度、油漆面積、分級社圖面 |
| 詳細設計 | Hull Detailed Design（[第 13 章](ch13_hull_detail_planar_zh-TW.reading.html)、第 14 章） | 完整平面板架與曲面殼板 |
| 生產規劃 | Assembly Planning | 組立樹、組立圖、組立零件表 |

[第 15 章](ch15_hull_production_zh-TW.reading.html)會概念性介紹組立與焊接規劃，Weld Planning 在[第 30 章](ch30_other_modules_zh-TW.reading.html)；分區、Multi-View 與有限元素會在[第 11、12 章](ch11_surface_block_zh-TW.reading.html)深入說明，本章只在銜接處交代。

---

# 第一部分　Assembly Planning

## 10.3 Assembly Planning 是什麼

官方定義：Assembly Planning 提供管理船舶**生產分解結構**的功能，支援建造策略的定義與組立生產資料的產生。這棵樹與設計與建模**並行**建立：專案早期先定粗略的建造策略，隨模型細化再細化；模型零件一旦存在，就可以收集到樹上的節點。因此組立視角從設計一開始就存在，不必等到設計完成。

重點有三：

- **範圍不限船體。** 生產階層含船體、設備、機械、電氣、風管與艤裝鋼構的安裝。
- **組立不一定是實體鋼構。** 也可對應一個空間（艙室、房間），把要裝進去的預製單元、材料與元件收在一起。
- **主要功能：** 組立樹編修、零件收集、自動組立圖與零件表、包圍盒與投影資料計算。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Assembly Planning 作業畫面：左為 Design Explorer，右上為 3D 視圖，下方為組立樹與清單

*圖 10-1　Assembly Planning 作業畫面。左側 Design Explorer、右側 3D Viewer，下方為 Assembly Tree 與 Assembly List。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 組立樹與設計樹是「同一批零件的兩種分法」。設計樹依構件，組立樹依建造順序（同一板架的零件可能分屬不同小組立）。類比為同一張資料表依另一欄位 group by。

## 10.4 資料模型

| 元件 | 角色 | 說明 |
|---|---|---|
| `ASWL` | Assembly World | 組立結構的最上層 |
| `ASMBLY` | 組立節點 | 可擁有子組立與代理 |
| `ASITEM` | 代理（proxy） | 使用者看不到，負責指向設計零件 |
| 設計零件 | 板、扁鋼、設備、管…… | 透過 `ASITEM` 被收集，本身不被複製 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕組立資料模型：Assembly 透過看不見的 Proxy 參考設計零件

*圖 10-2　組立資料模型。左邊是設計階層（HBLO 到 HPAN 到零件），右邊的 Assembly 經由虛線 Proxy 指到零件。（AVEVA 官方文件截圖，僅供內部教學）*

### 10.4.1 `ASMBLY` 的主要屬性

| 屬性 | 意義 | 型別 |
|---|---|---|
| `NAME` | 組立完整路徑名 | 文字 |
| `ASNAME` | 本節點名稱 | 文字 |
| `DESC`、`ASWLOC`、`ASDEST`、`ASBUIL` | 說明、作業位置、目的地、建造策略 | 文字 |
| `ASORI` | 預設組立方向 | 整數 |
| `ORI`、`POS` | 方向與位置 | 實數陣列 |
| `ASBPAN` | 基準板架（`ASORI` 為 7 或 8 時使用） | 參考 |
| `ASEWEI`、`ASECOG` | 預估重量、預估重心 | 實數、實數陣列 |

`ASORI` 的預設值：1 = 正放（upright）、2 = 倒置、3 = 艏朝下、4 = 艉朝下、5 = 左舷朝下、6 = 右舷朝下、7 = 指定板架（specific panel）、8 = 自動、9 = 手動。官方強調：**組立方向永遠相對於世界座標，而不是相對於母組立。**

### 10.4.2 代理與擬似屬性（pseudo attribute）

`ASITEM` 有 `ASIQUA`（數量）與 `ASMREF`（指向設計零件）。`ASMBLY` 的擬似屬性有 `SMEMB`（直接成員）、`SEXPND`（整棵子樹下被參考的零件）、`ASORIS`、`ASSEQ`（順序號）、`ASNORM`／`ASVDIR`（組立平面法向量／視線方向）。任何可被收集的元件則多出 `ASIOWN`、`ASMOWN`（所屬組立）、`ASMBLD`（是否已組立）、`ASMBLS`（`'A'` 或 `'NA'`）、`ASMBLB`（此類型能否被收集）。

> **專業提醒：** 擬似屬性是二次開發最實用的入口，例如用 `ASMBLD` 找出尚未收集的零件。官方只列屬性名，沒有範例查詢語法，具體寫法〔待核對〕。

## 10.5 啟動與介面

### 10.5.1 啟動

Assembly Planning 是**附加元件（add-in）**，可在任何設計模組（例如 Hull Design）中以 `View > Addins > Assembly Planning` 啟動。官方列出的交付檔：`Aveva.Marine.AssemblyPlanning.dll`、`AssemblyPlanningAddin.dll`、`Aveva.Marine.AssemblyPlanning.Utilities.dll`、`AssemblyPlanningAddin.uic`。

視窗由四塊組成：Design Explorer、3D Viewer、Assembly Tree 與 Assembly List；樹與清單之間支援拖放，清單支援多選。Design Explorer 的零件節點會加註 `A`（已組立）或 `NA`（未組立）。

### 10.5.2 工具列功能

Filter（依使用者定義元件類型 UDET 過濾）、Sort Tree（依名稱或組立順序；依順序排時 `Parts` 資料夾消失）、On Level Up、Edit Sequence（開啟後可在清單拖放改順序）、Collect Rules（勾選收集時考慮的元件類型）、Visuals（已收集與未收集零件在 3D 的顯示差異）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Collect Rules 對話框：勾選哪些類型可直接被收集

*圖 10-3　Collect Rules。勾選的類型可直接收集；不勾選則改收集其下的子孫或其上的祖先。（AVEVA 官方文件截圖，僅供內部教學）*

## 10.6 建立與維護組立樹

右鍵選單的內容依選取節點類型而不同。主要功能：

| 功能 | 說明與注意 |
|---|---|
| New Assembly | 在選取節點下建子組立。從樹操作時新節點被選取，從清單操作時母節點維持選取，這決定了連續建同階層還是逐層建立 |
| Insert Assembly | 在現有節點之間插入一層，進入功能前選取的零件、組立或 Parts 資料夾會被放入新組立 |
| Remove | 移除組立及其子結構，零件的收集關係解除（零件本身不刪）；對零件則是取消收集 |
| Rename、Cut/Copy/Paste、拖放 | 搬移或複製；UDET 子型別可限制哪種組立可放在哪種之下，複製與搬移也受此限制 |
| Copy Hull Symmetrical Parts | 一般複製**不包含**已收集零件；此功能會把對稱船體零件的對應件指派給複製出的組立 |
| Collect / Decollect | 由 Design Explorer 拖放到組立，或用 Collect Graphical Selection 在 3D 視圖選取後收集 |
| Verify Naming、Make Selection | 前者回報目前 MDB 內重名的組立；後者把樹中選取內容在 3D 視圖選起來（Make Hierarchy Selection 含所有子組立的零件） |
| Show Sequence | 在 3D 中依順序逐一由透明漸顯，可播放、暫停、重新開始，Settings 調速度 |
| Properties | 編輯屬性、換 UDET 型別；自動支援 UDA 與 USDA（限定值會變成下拉選單） |
| Set as root、User Columns Setup | 暫時縮小大樹；為清單增加自訂欄位 |
| Report | Hull Material Summary、Parts List（見 10.9） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Show Sequence：依序播放組立成員，Seq 欄標示已顯示的項目

*圖 10-4　Show Sequence 動畫控制。播放時組立樹隱藏，清單變成播放控制台。（AVEVA 官方文件截圖，僅供內部教學）*

### 10.6.1 收集規則的關鍵限制

1. **一個設計零件只能屬於一個組立。** 若已屬於他處，系統會詢問是否改派到新組立。
2. 臨時性、不屬於設計的物品（例如吊環螺栓）可用目錄的 `GPART` 通用零件收集，且 **`GPART` 可同時收集到多個組立**。無法顯示的 `GPART` 收集時會跳出「not a usable item」，官方說可忽略。
3. 收集哪些類型，由 Collect Rules 決定；選錯層級是「樹上看不到零件」的常見原因。

### 10.6.2 組立方向設定

`ASORI` 決定製造時的擺放方向，**也決定自動組立圖的視線方向**。設為指定板架或自動時必須指定基準板：指定模式由使用者選；自動模式取面積最大的板架，並轉成平面圖、讓多數零件在上側。若材料在下側，須相應修改 material side。指定板架可選平面或曲面板架，但曲面板架需事先完成支撐胎架（jig）計算。

### 10.6.3 命令列介面

可用一般 `NEW`、`DELETE` 建立與刪除組立節點，用 `AADD`、`AREMOVE` 改變組立內容。這兩個指令的完整語法官方頁面未列，細節〔待核對〕。

> **專業提醒：** 建議先在 UDET 與 USDA 定義「哪種組立（分段、大組立、小組立、艤裝單元）能放在哪種之下」及屬性允許值，再開始建樹；事後補規則只能靠人工檢查。

### 10.6.4 常見錯誤

拖放零件沒反應，多半是 Collect Rules 沒勾該類型；零件突然從舊組立消失，是重新收集時確認了「改派」；複製組立後零件是空的，因一般複製不含收集內容；組立圖視角不對，檢查 `ASORI` 與 `ASBPAN`；重名組立請跑 Verify Naming。

---

## 10.7 Assembly Planning Admin：Assembly ADP 的建置

Assembly Drawing 與零件表由 **Assembly ADP（Automatic Drawing Production）** 產生，它使用 Marine PML 語言搭配 PDMS Draw 策略，並有一組預設圖面版型與支援函式庫。標準範例專案已載入完成；**新專案則需自行完成以下四件事。**

### 10.7.1 新專案安裝清單

1. 專案要定義 **True-Type Font 6**（官方圖面以 Lucida 系字型間距為基準；改字型要檢查背圖與標籤是否文字重疊）。
2. 載入 Assembly ADP 資料庫函式庫到要出圖的 MDB：Outfitting Draft 會多出 `Create > Assembly ADP Library...` 選單；Marine Drafting 沒有選單，須在命令視窗輸入 `show !!assyDbs`，工具列也要從 AutoADP 選單初始化。
3. 在繪圖資料庫建立 `DEPT` 與 `REGI`，其 `SPPURP` 為 `ASMBLY`、`FONT` 設為 True-Type。
4. 若用 Marine Drafting 輸出 PDF，須定義 PDF Print Driver；僅用 Outfitting Drafting 則使用產品內建 PDF 函式庫，不需要。

升級提醒：12.1.SP2 新增相同零件合併計數的版型 `AD-001-SUM` 與 `PL-001-SUM`；舊版載入的專案須在命令視窗執行 `$M /\PMLLIB\assembly\data\assembly_adp_library_acc.txt`（公制，英制另有 `_imperial_acc.txt`）補上。

### 10.7.2 函式庫內容

Drawing Template、Backing Sheet、Task 定義、Parts List 設定、Labels 與 Symbols、Representation Rules，共六類。

### 10.7.3 Drawing Template 結構

製圖時使用者選一個 `DRTMPL`，系統建立 `DRWG` 並做 **copy-like**；`DRWG` 以 `LINKREF` 指回來源樣板，之後樣板修改後可據此找出需要更新的圖。

> 〔公開版未收錄：AVEVA 官方產品截圖〕DRTMPL 與 DRWG 的資料庫階層：DEPT、REGI、DRWG、SHEE 與 DRTMLB、DRTMPL、SHTMPL

*圖 10-5　Drawing Template 階層。右邊為樣板庫，經 COPY LIKE 產生左邊的實際圖面。（AVEVA 官方文件截圖，僅供內部教學）*

| 元素 | 必要屬性與意義 |
|---|---|
| `DRTMLB` | `SpPurp ASTMPL`（讓程式找到）、`Function`（主表單的 Drawing Type 下拉文字）、`Ntext`（範例縮圖檔，如 `001.png`） |
| `DRTMPL` | `Size 420 297`（尺寸選單）、`Bsrf`（背圖參考）、`SpPurp ASTMPL` |
| `SHTMPL` | `Size`、`Bsrf`、`Title`、`SpPurpose ASTMPL`；範例樣板每個含一張圖紙、兩個視圖（主視圖通常等角、次視圖正交） |
| `VIEW` | 每個視圖內只放一個組立元件；視圖下的圖層須符合 Outfitting Draft 的圖層方法 |
| `TASK` | 在製圖過程中呼叫 PML 函式（10.7.5） |

搜尋規則由組態檔 `libraryRule` 決定，範例為 `"WITH SPPURPOSE EQ 'ASTMPL'"`；`descAttribute` 決定用哪個屬性當選單文字。

### 10.7.4 Backing Sheet 與保留區

Backing Sheet 是不可操作的固定層，內含 Frame（外框線）、Title Block（含 `#DRWGN` 這類智慧文字 hash code）與 **Reserved Area（保留區）**。保留區是 `BACK` 下 `NOTE` 內的 `TABL` 元件，預設不可見（`LVIS` 設 `TRUE` 可顯示），以 `spPurp` 區分：`ASMBLY` 為組立屬性表，`PARTSL` 為零件表。表格另有 `Nrows`（最大列數，與列高、符號標籤高度要吻合）、`Filldirection`（如 `DOWN`）、`Origin Topleft`（原點位置，**必須與填表用符號標籤的原點一致**）。讀取背圖的 PML 物件是 `ASSYBACKSHEET`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕保留區示意：A 為組立屬性表區域，B 為零件表區域

*圖 10-6　Backing Sheet 的兩個保留區。A 為 Assembly Properties 表，B 為 Parts List 表。（AVEVA 官方文件截圖，僅供內部教學）*

### 10.7.5 Task：樣板內的自動化

`TASK` 的三個關鍵屬性：`SpPurp STASK`（D = 圖、S = 圖紙、V = 視圖）、`Function`（說明文字）、`PMLFunction`（如 `'!!assyProperties(!array)'`）。引數存在其下的 `TPVAL` 元件，所以同一函式可在不同樣板用不同參數；執行時由應用程式把引數塞進 `!array`。

| 層級 | PML 函式 | 作用與主要參數 |
|---|---|---|
| Drawing | `!!assyDrwgNo` | 產生圖號寫入 `DRWGN`；參數含是否用 Name Sequence 資料庫、前綴、後綴、起始號、分隔字元 |
| Sheet | `!!assyProperties` | 建立組立屬性表（`PROPVW` 視圖、`ASPROP` 圖層）；以 `SLAB` 參考 `SYTM`，hash code 直接從 `ASMBLY` 取值 |
| Sheet | `!!assyPartsList` | 建立零件表（`PARTVW`、`PRTLST`）；用 Title、Header、Row、Overflow、Cell 五種符號樣板，末參數 `ACCUMULATE` 可合併相同零件 |
| View | `!!assyTagParts` | 為每個合適零件建立零件編號標籤（`PRTTAG` 圖層）；更新時只為未標示者補標 |
| View | `!!assyArrange` | 沿視圖四邊排列標籤；參數為各邊開關、邊距、最小間距 |
| View | `!!assyCrAxes` | 建立軸符號 `AXESYM`，並讓視圖反映組立方向 |
| View | `!!assyBoundBox` | 繪出 WORLD 或 LOCAL 包圍盒與尺寸字 |

三個細節很容易被忽略：

1. **圖號索引的效能。** 預設做法會掃描 MDB 內所有圖找下一個未用編號，圖數多時會嚴重變慢；官方建議改用 Name Sequence 資料庫（NSEQ），引數 1 設 `YES`、引數 5 設如 `0`，識別字 `'ASSEMBLYADP'` 在 PML 函式中有兩處。
2. **更新時不重跑的任務。** 把 `SPPURPOSE` 設為 `DTASKX`、`STASKX`、`VTASKX`（圖、圖紙、視圖），任務只在建立時執行；樣板改了之後，已產生圖內的同名任務要手動同步。
3. **合併相同零件。** 判定條件由 `%PMLLIB%\assembly\userfunctions` 內的 `assyPartCompareAttsForAccumulation`、`assyPartsIdenticalForAccumulation`、`assyPartValidForAccumulation`（`.pmlfnc`）決定，可改寫。

### 10.7.6 Parts List Template 與其他函式庫

零件表樣板以 `LALB` 的 `SpPurp ASPLST` 被找到，`Function` 為「Parts List Type」下拉文字，其下 `SYTM` 決定組立屬性與零件清單的儲存格資料。符號庫 `SYLB`、標籤庫 `LALB`（零件編號標籤 `/Assembly-Planning/PartNo`）與表示規則庫 `RPLB`（`RRST /Assembly/General/All` 依管、設備、`PANEL`、`GENSEC`、鋼構、風管、電氣等類型指定顏色與線型）皆可依公司標準改寫。

### 10.7.7 組態設定

組態檔為 `%PDMSDFLTS%\assembly\assydrwg.cfg`。以管理員身分進入繪圖模組時，工具列多一個 **Modify Settings** 按鈕，開啟 Assembly Drawing Configuration Editor；每一項設定對應 `ASSYDRWGCONFIG` 物件的同名方法（例如 `createDrawing = YES` 對應 `.createDrawing`），表單為 `!!assyDrwgConfig`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Assembly Drawing Configuration Editor：Department & Registry、Drawing、Parts List、Administration 四區

*圖 10-7　組態編輯器。四個區段分別控制出圖位置、圖面輸出、獨立零件表與檔案管理。（AVEVA 官方文件截圖，僅供內部教學）*

| 區段 | 主要設定 |
|---|---|
| Department & Registry | 搜尋與建立用的 `SpPurpose`（預設 `ASMBLY`）、新建 Department 的根名稱 |
| Drawing | 是否出圖、`DRTMLB` 搜尋規則、說明屬性、預設類型與尺寸、圖號屬性（須與背圖 hash code 一致）、是否輸出 PDF 與路徑 |
| Parts List | 是否輸出獨立零件表、`LALB` 規則、屬性與零件兩個 `SYTM` 搜尋規則、輸出格式 `.txt`／`.csv`／`.xls`、輸出資料夾 |
| Administration | 記錄檔資料夾（預設 `%PDMSUSER%\Assembly-Logs`）、批次檔資料夾、文件連結資料夾（Link Folder）規則 |

出圖後系統以 `!!assyDocLink` 為每個組立建立連結資料夾，把圖、PDF 與零件表連回來源 `ASMBLY`；**該 Link Folder 必須事先存在，否則連結建不起來。** 重新更新或再生圖時會重用既有連結。

### 10.7.8 使用者 PML 函式

位於 `%PMLLIB%\assembly\userFunctions` 共 17 個 `.pmlfnc`，如 `assycog`、`assyweight`、`assyqty`、`assydrwgno`、`assydoclink`、`assyexpandsubparts`。

### 10.7.9 常見錯誤

| 症狀 | 常見原因 |
|---|---|
| 零件表錯位或溢出 | 保留區 `Nrows`、`Origin` 與符號標籤列高不一致 |
| 圖號不出現、大量出圖越來越慢 | 圖號屬性與 hash code 不一致；仍用掃描 MDB 算圖號 |
| 文件連結失敗、改了樣板舊圖沒變 | Link Folder 規則找不到；圖是 copy 出來的，須同步舊圖內元件 |

---

## 10.8 Assembly Drawing：產生組立圖與零件表

### 10.8.1 工具列

Assembly ADP 使用兩條工具列（在主表單右鍵選單打開）；Design Draft 內還須先進入 `Draft > Auto Drawing Production`。

- **Assembly Department 工具列**：指定圖要建在哪個 Department／Registry；若沒有 Assembly Department，系統會在第一個可用資料庫建一個。可用 Create Assembly Hierarchy 表單新建 `DEPT`（含自動 `REGIS`）或在既有 Department 下加 `REGIS`。
- **Assembly Drafting 工具列**：產生圖、多張圖、搜尋圖、列印、看記錄檔、修改偏好（僅管理員）、列印目前圖紙。

### 10.8.2 三種出圖方式

| 方式 | 說明 |
|---|---|
| Draw This Assembly | 只畫 Design Explorer 中目前選取的組立 |
| Draw All Assemblies | 畫目前組立及其下所有子組立，完成後以 Assembly Drawings 表單瀏覽 |
| Multiple Drawings | 由 Assembly Planning Deliverables 表單搜尋後多選 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Assembly Planning Deliverables 表單：搜尋範圍、過濾條件、結果表、位置與處理按鈕

*圖 10-8　Assembly Planning Deliverables 表單。A 搜尋範圍，B 過濾，C 結果表，D、E 圖面存放位置，F Batch，G Now，H 零件表選項，N 圖面選項。（AVEVA 官方文件截圖，僅供內部教學）*

### 10.8.3 多選出圖流程

1. 設搜尋範圍（預設 `*` 為整個 MDB；可點 CE 改為目前元件之下）。
2. 選過濾條件：**Those not drawn**（尚未出圖）、**Those drawn**、**Those drawn by me**、**Bad Drawing Reference**（連到未知圖）、**All Assemblies**。
3. 按 Search，結果表顯示組立名稱、是否有有效內容、是否已出圖、目前使用者能否修改相關圖，以及處理模式（Create；已有圖則為 Update 或 Regenerate）。
4. Ctrl 多選，必要時把模式由預設的 Update 改為 Recreate。
5. 展開 Drawing 與 Parts List 區設定出圖與否、樣板類型與紙張、PDF、獨立零件表類型與格式、輸出位置。
6. 按 **Now**（立即處理）或 **Batch**（產生批次巨集稍後處理）。

右鍵選單可全選、取消、移除項目、設為目前元件、顯示相關圖（Display Drawing）與顯示 3D 組立（Display Assembly，開啟 Assembly Model View）。

> **專業提醒：** Update 會盡量保留圖面並重新整理圖形、表格與註解；Regenerate 則刪除圖面內容重建。人工在圖上做過的調整，只有 Update 有機會保留，所以排程批次時預設選 Update，且先確認沒有 `…TASKX` 任務被誤重跑。

### 10.8.4 批次出圖

立即處理會鎖住繪圖模組。改按 Batch 會開啟 Assembly Drawing Batch Macro 表單，設定輸出資料夾、執行批次的使用者與密碼，以及將執行的巨集命令，按 Apply 後產生三類檔案：Marine 進入與離開批次檔、設定環境變數的批次檔、實際出圖的 Marine 巨集。**之後需自行以作業系統工作排程器執行進入批次檔。**

> 〔公開版未收錄：AVEVA 官方產品截圖〕Assembly Drawing Batch Macro 表單：資料夾、Run As User、巨集內容預覽

*圖 10-9　Assembly Drawing Batch Macro。顯示將產生的巨集內容（含 `!!assyCallMacro` 載入筆色與線型設定、建立 `ASSYDRWGAPPLICATION` 物件）。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 此表單要輸入使用者名稱與密碼（官方以 `SYSTEM` 示範）；實務上應為批次作業另建專用帳號並限制權限（見[第 43 章](ch43_system_administration_zh-TW.reading.html)）。巨集是否明文寫入密碼，官方未說明，〔待核對〕。

### 10.8.5 輸出與零件表

| 項目 | 說明 |
|---|---|
| 圖 | 可列印或輸出 PDF |
| 零件表 | 可印在圖上，或輸出 `.txt`／`.csv`／`.xls` 的獨立檔案 |
| 內容 | 組立屬性（專案名、組立路徑、說明、目的地、作業位置、方向、建造策略、預估與計算重量與重心、包圍盒、基準板等）加零件清單（名稱、類型、說明、數量、尺寸等） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕組立零件表輸出：Notepad 文字檔、CSV 與 Excel 三種格式

*圖 10-10　獨立零件表的輸出範例。含組立屬性區與零件清單，可為 txt、csv、xls。（AVEVA 官方文件截圖，僅供內部教學）*

### 10.8.6 搜尋、修改與維護

- **Assembly Drawings 表單**：以 All Drawings、Those drawn by me、Those drawn by me today、Bad Drawing Reference 搜尋；結果顯示圖號、對應組立、作者、日期、使用樣板、紙張大小與修改權限；多張圖紙可前後切換；可匯出 Excel、批次列印（份數、逐份、縮放至紙張、彩色或黑白）。
- **更新參照**：圖與組立的內部參照失效時，結果表出現警告符號。右鍵 Go to Drawing，在命令視窗輸入 `UPDATE REFS`，仍失敗則 Update 重新產生。
- **Change Projection**：結果表右鍵選取，從下拉選視圖並按方向按鈕（如 Iso-2）。Marine Drafting 的 `Tools > Model view > Change projection` 可選擇性重生標籤與包圍盒，由 PML 函式 `mdraupdatetasks` 負責，客製過 Assembly ADP 時須同步客製。
- **Rerun Arrange Label**：視圖縮放後，Update Annotation 會讓標籤錯亂，此選項重跑排列任務。記錄檔預設在 `%PDMSUSER%\Assembly-Logs`。
- **使用限制**：以 `AXESYM`（`AsmblR` 指向組立、`Axstype MARINE`、`AXSsize`）讓視圖反映組立方向後，該視圖的 Drawlist **不可**設為 `IDLI`（必須直接指向組立），也**不可**用來建剖面平面（須改用以世界座標為方向的標準視圖）。

---

## 10.9 報表與二次開發入口

### 10.9.1 報表

| 報表 | 說明 |
|---|---|
| Hull Material Summary | 只列出組立中的船體元件；PML 表單，可從命令列用 `show !!hullreport` 開啟 |
| Parts List | 組立資料加完整零件表，四種範圍：僅本組立擁有、含下層全部零件、各子組立各出一份等；可從命令列 `show !!assypartsreport` 開啟 |
| Weld | 見[第 30 章](ch30_other_modules_zh-TW.reading.html) Weld Planning |

### 10.9.2 二次開發怎麼接

| 入口 | 官方依據 | 做法 |
|---|---|---|
| `AssemblyPlanningAddin.uic` | 官方：可附加使用者函式至右鍵選單；出廠時已含 Hull Material Summary 與 Parts List | 編輯 `.uic`（參考官方 .NET Customization 文件，語法〔待核對〕） |
| `AssemblySelection` 物件 | PMLNet 物件，匯入 `Aveva.Marine.AssemblyPlanning.Utilities` | 方法 `Assemblies`、`Parts`、`AddEventHandler`、`RemoveEventHandler`、`Remove`，事件名 `AssemblySelectionEvent` |
| `!!assy…` PML 函式與 `.pmlfnc` | 10.7.8 清單 | 改寫既有函式、仿照寫新任務 |
| `ASSYDRWGCONFIG` 物件 | 組態方法與 `.cfg` 同名 | 以 PML 讀寫組態 |
| 擬似屬性 `ASMBLD`、`SEXPND` 等 | 10.4.2 | 查詢與報表 |

官方範例用 `!o = object AssemblySelection('MyObjectName')` 建物件，以 `!o.addeventhandler('AssemblySelectionEvent', !this, 'myHandler')` 註冊事件，在 `define method .myHandler(!array is ARRAY)` 內以 `!o.assemblies()`、`!o.parts()` 取得選取的陣列（元素用 `.dbref()` 轉成資料庫參照），關閉表單前須 `removeeventhandler` 並 `remove()`。官方範例本身有一處變數名不一致（`!a.addeventhandler` 應為 `!o`），且 `!o` 在方法內是否可見取決於物件存放位置，實作時請改為表單成員變數，〔待核對〕。

---

# 第二部分　Hull Structural Design

## 10.10 Structural Design 的定位

官方說明：初步設計比詳細設計省資源，但詳細設計的工作量高度取決於初步設計做到什麼程度；造價的大部分在設計初期就已決定。Structural Design 的目標是**初步階段做的定義，直接被詳細設計與生產資訊重用，不必重做**，並因此能比較更多方案、更早取得驗船機構（classification society）核可。四大面向：

| 面向 | 內容 |
|---|---|
| Fast Modelling | 由 RSO 定義 Functional Structure 後自動產生 Functional Panel；用 Vitesse 技術寫 Quick Panel |
| Early Analysis and Estimates | 內建工具（如斷面模數）與 XML 介面連到外部軟體（如驗船機構） |
| Generation of Drawings | 建模與製圖完全整合，可在任何製圖視圖上建模 |
| Smooth Transition to Detail Design | Functional Panel 即一般板架；依分區切出生產板架 |

### 10.10.1 快速建模的兩個工具

- **Functional Structures。** 在 Surface/Compartments 模組定義艙室時，艙室界限就是主要 RSO，構成 Functional Structure 的基礎；Structural Design 另可在主平面額外定義 RSO。為 RSO 設定材料、端部連接等屬性，就把 RSO 變成 Functional Structure，進而**自動產生內部結構的 Functional Panel**。
- **Quick Panels。** Quick Panel 是客製化的 **Vitesse 腳本**，用來產生特定型態的船體結構。系統提供數種主要內部結構型式的範例函式，目的是作為客戶改寫的範本，可依船廠習慣或船型修改。Vitesse 的語法與函式庫在本章讀到的頁面都沒有說明，〔待核對〕。

### 10.10.2 早期分析與估算

可輸出四類報表：**重量與重心**、**鋼料明細**、**焊接長度估算**、**油漆面積計算**。分析工具在有 Functional Panel 後即可使用。

### 10.10.3 出圖

視圖功能在 Planar 與 Curved 的 View 選單中，可產出總布置（General Arrangement）、橫剖面（Body Plan）、外板展開（Shell Expansion）、舯剖面（Midship Section）、立面與縱剖、典型剖面。模型圖與設計圖同時產生，不需額外程序。

### 10.10.4 轉入詳細設計

目前版本的 Functional Panel 可視為一般板架（同時有結構設計與詳細設計兩種視角屬後續版本）。切成生產用 Production Panel 則用 Block Division（見[第 11 章](ch11_surface_block_zh-TW.reading.html)）。

## 10.11 設計情境與專案設定

### 10.11.1 兩種情境

| 情境 | 起點 | 步驟概要 |
|---|---|---|
| 情境 1：從零開始（典型商船） | 最終船殼面尚未提供，先建只描述平行舯體的粗略曲面與主 RSO | 先建縱向主要構件（外板、縱骨、甲板、縱艙壁、桁材、縱桁）→ 以板架自動產生或 Quick Panel 建內部結構 → **檢查斷面模數，不足就調整縱骨材料反覆迭代** → 再建橫向構件（橫艙壁、肋板、底肋板）→ 取得驗船機構舯剖面首次核可 → 匯入初步或最終全船曲面，延伸到艏艉 |
| 情境 2：既有初步設計資料（郵輪） | 船殼面與艙室劃分已定 | 由 RSO 建甲板與艙壁 → 定義加強筋與縱骨並檢查斷面模數 → 建典型橫艙壁、肋板與底肋板 |

兩者之後的共同工作：主要設備的定義與放置、估算、出圖、把鋼構切成主要建造分區。

### 10.11.2 專案設定

- 安裝附帶**範本專案（Template Project）**，位於 AVEVA Marine 根目錄下，內含預設設定與標準；官方建議客戶**依船型建立自己的範本專案**，避免每次重做專案設定。
- **Surface。** 要存取已釋出曲面的交線與曲線資料，專案內須建立 **Hull Reference Object**（定義可存取的曲面與其類型，設定細節在 Hull 使用手冊的 Surface Setup）。建立後以 `Project > Surfaces` 登記其他曲面。
- **Standards。** 包含船廠與專案專屬標準；範本專案通常含特定船型的船廠標準，專案專屬部分必須在每個新專案設定。

## 10.12 功能選單總覽

Structural Design 的功能是「Structural Design 專屬功能」加「所有船體模組共通的船體功能」，再加完整的 Drafting 功能。官方文件主要詳述專屬功能。

| 選單 | 用途 |
|---|---|
| Project | 整個專案的設定：肋骨與縱骨位置、Block、舯體曲面、Envelope、模型檢查 |
| Functional Structure | 處理 RSO、定義屬性成為 Functional Structure、產生板架、合併板架、分區 |
| Planar | 平面板架的建模、板架整體操作、Scheme、Editor、View、PosNo、Select |
| Curved | 曲面殼板、殼縱骨、特徵、幾何、預設值、視圖、選取 |
| XML | 以 XML 匯入匯出模型資料 |
| Analysis | 斷面模數、焊接、重量重心、材料表、油漆、FE 模型 |

Planar 與 Curved 的功能與詳細設計相同，細節請見[第 13 章](ch13_hull_detail_planar_zh-TW.reading.html)與第 14 章；本章只在 10.12.6 摘要。

### 10.12.1 Project 選單

| 功能 | 說明 |
|---|---|
| Surfaces | `Register Surfaces` 對話框列出已釋出曲面。欄位：Registered（核取後登記，數字為 `SURFACES` 預設參數的編號）、Name、Suffix（建縱骨、橫肋、殼縱骨與殼縱骨軌跡曲線時的後綴；主船殼不用，其餘曲面須唯一）、Type（Main Hull、Main Deck、Shell、Deck；Main Hull 與 Main Deck 各只能有一個）、Source、Design。登記結果存入 Hull Reference Object |
| FR/LP Positions | 肋位與縱向位置以起點、間隔、終點輸入；可定義多組位置表（例如鋼製下半部與鋁製上半部），但尺寸標註一律使用預設表 |
| Block > Edit | 以樹狀對話框建立、修改、重建、複製、刪除 Design Block 與 Production Block；可修改名義界限與偏移，並指定界限物件（Stored Plane、RSO、Surface）取得精確外形；變更須按 Save Block Data |
| Block > Recreate | 在目前圖面挑選要重建的 Block |
| Block > Create from CSV | 由 CSV 建立或更新 Block（格式見下） |
| Block > Extract to CSV | 把目前 Block 結構輸出為 CSV 到 `SB_SHIPDATA`，從 Log Viewer 取得 |
| Midbody Surface | 快速建立平行舯體曲面：艉艏端、船寬、型深、底升高、平龍骨、舭型（None／Flat／Circular）與舭點等；存入資料庫並登記到 `hullref` |
| Envelope | 以多個曲面與 RSO 組成封閉體積，作為建立或修改 RSO 的外邊界；右鍵 New／Add／Remove／Delete 或 Pick in Dwg，按 Save Envelope 儲存 |
| Verify Model | 使用 Block Splitting 前檢查所有拓樸相依性，結果顯示在 Log Viewer |
| Recreate Limit Tables | 重建縫、縱骨、橫肋的界限表（每個曲面一份，用於提升效能） |
| Project Information | 檢視或修改自 AVEVA Initial Design 釋出的專案與主要尺度，供報表標頭與計算使用 |
| Change View Mode | 在 Design View 與 Production View 之間切換；僅 Multi-View 專案可切，單視圖專案兩者皆灰色 |

**Block CSV 格式：** 每列依序為 Type（`D` Design 或 `P` Production）、Name、六個名義座標（Aft、Stbd、Bot、For、Port、Top，可用肋位與縱向位置）、Encl. Block（建 Production Block 且專案有 Design Block 時才需要）、六個偏移（mm）、六個界限物件（前綴 `SUR/`、`RSO/`、`PLA/`）、Sym（Yes／No）與 Colour（整數）。第一列視為註解；已存在的 Block 只有內容改變才會更新。

**Verify Model 的警告範例：** 板架名稱過長（建議上限 17 字元，因為會加前後綴，超過 19 字元風險更高，應改名）；邊界參照的物件不存在（檢查 CGDB 與是否被刪除）；外輪廓無法連同缺口與開孔重建；肘板或翼板參照在拓樸物件中缺漏或失效（重新產生並儲存板架）。

> **專業提醒：** Verify Model 是「轉入詳細設計」的必經檢查。板架名稱長度是最常被忽略、卻在分區後才爆發的問題；建議在設計階段就定好命名規則並限制在 17 字元內。

### 10.12.2 Functional Structure 選單：RSO 的一生

RSO 的用途：作為空間、Block 或艙室的邊界；作為鋼模型參照的底層結構；把 2D 背景圖（backdrop）以 3D 呈現。類型有五種：Compartment Limits、General Inner Structure、Block Limits、General Limits、Backdrops。**鋼模型只能放在 Compartment Limit 與 General Inner Structure 兩類 RSO 上。**

| RSO 功能 | 說明 |
|---|---|
| Key In | 以輸入位置並選平面與界限物件建立，結果為受 Envelope 與界限限制的平面 |
| Sketch 2D | 在 Symbolic Planar View 或 Backdrop View 上用 Draw（折線，可配 Grid）、Select、Trim、Panel（挑板架，依其平面建 RSO 並讓板架改為參照該 RSO）建立；自動以平面座標命名（`-` 換 `N`、`+` 換 `P`）；類型預設 General Inner Structure；選項有 Grid、Mirror Copy、Verify Name and Limits |
| From Backdrop | 以位於主平面的 Backdrop 視圖建立 Backdrop 型 RSO，視圖幾何存為標記；X、Y 主平面的 RSO 以船殼與上甲板（名為 `WEATHER` 的 RSO，沒有則自動建立）為界 |
| From Panel | 由既有板架建立或更新 RSO。優點：之後即使 RSO 內的巨大板架被細分成詳細設計用板架，對 RSO 的參照仍穩定 |
| Recreate | 界限物件或 Envelope 改變後重建 RSO 幾何 |
| Edit Shape | 以剖面表格修改外形；核心要求是各面不折角，提供 Keep profile parallel（自動調整前一線或後一線）、Single cell edit 加 Iron（修正其餘剖面使之合規）與 Profile history（類似 Undo 但不清除後續步驟） |
| Copy | 複製，位置可為相對或絕對；Position 欄可用重複語法 `<Start value>[(Step)<End value][+-Offset]`，名稱 `XXX10(10)` 會得 `XXX10, XXX20, XXX30...`；Block Limit 類可勾 Keep Connection |
| Move、Rename、Change Envelope | 移動並重建；改名會更新其上的板架與拓樸相依的 RSO，**其他相依（如以該 RSO 為界限的船體板架）須手動更新**；Change Envelope 把 RSO 移到另一個 Envelope |
| Properties | 為 SB_TID 資料庫的 RSO 加入建模屬性（功能描述、材料、型材資料、端部切割），以供自動產鋼 |
| Disconnect、Delete | 解除或刪除 RSO，並把參照它的板架位置轉成主軸位置或三點定位；板架邊界內對該 RSO 的參照**不會**自動轉換 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕RSO 2D Definition 對話框：Grid、Mirror copy、Verify Name and Limits 與 Trim、Select、Draw、Panel 按鈕

*圖 10-11　RSO Sketch 2D 對話框。右側選 RSO Type 與 Envelope，下方按鈕對應繪製、選取、修剪與由板架建立。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕RSO 外形編輯：Limits、Envelope、Profile 表格與 Iron 按鈕

*圖 10-12　Edit Shape 對話框。以剖面表格調整 RSO 形狀，Iron 修正折角。（AVEVA 官方文件截圖，僅供內部教學）*

**Properties 的釋出前置條件：** 從 Surface/Compartment 釋出到 PIM（`File / Release / Design`）時須定義並釋出 Main Deck，RSO 參照的外殼面名稱依 Envelope、barehull、Hull Form（dml）的順序判定，都沒有則為 `HULL_NOT_KNOWN`；這些曲面須以 `Project / Surfaces` 或 Initiate Hull Standards 登記。

**Generate Panels：自動產鋼的規則**

先處理甲板，再處理其他。每塊板架放入第一個幾何上完全包住它的 Block，找不到就放入預設的 `JUMBO` Block；板架命名為 `<block_name>-><RSO name without prefix>_<face number>`。內容依 RSO 的功能描述（functional description）碼決定：

| 功能碼範圍 | 類型 | 產生內容 |
|---|---|---|
| 9000–9099 | 甲板 | 板材加水平縱向位置的加強筋；與縱艙壁 RSO 相交處不放加強筋 |
| 9100–9199 | 縱艙壁 | 板材加垂直縱向位置的加強筋；與甲板相交處不放 |
| 9200–9299 | 橫艙壁 | 板材與加強筋；若以甲板為界，連接到甲板加強筋，並可依需求建肘板 |
| 9400 | 一般肋板構件 | 依相交 RSO 判斷：與內底、雙層底、艙頂板（9010–9012）相交者建底肋板，再依 Hopper Tank Sloping（9104）建 Hopper 橫肋，再依內側板（9102）建垂直肋板 |
| 其他 | | 只產生板材 |

所有板架型式都會依「自動設定開孔（Automatic Setting of Cutouts）」的設定加開孔；FRP（玻璃纖維）選項須指定邏輯變數 `SBH_GRP_LAM` 為預設積層碼。結果會存入並顯示在現有視圖；沒有視圖則在目前圖面新建。

**Merge Panels 與分區：**

| 功能 | 條件與結果 |
|---|---|
| Merge Panels | 須共用一個界限、周圍定義相同、同一平面、對稱碼相容；可勾 Only check if panels can be merged 先試算；多塊時遞迴比較，最後只能剩一塊。Multi-View 專案只能合併 Design Panel（已有 Production Panel 則建 Block Seam 取代）；Production Panel 須用 Planar > Panel > Remove Seam 兩兩處理 |
| Pending updates | 僅 Multi-View 專案：當對應板架被修改時，更新 Design 或 Production 板架 |
| Divide into Blocks | Multi-View 專案：由 Design Panel 建 Production Panel，或把 Design Block 細分；單視圖專案：把 Block 細分成更小單元。細節見[第 11 章](ch11_surface_block_zh-TW.reading.html)的 Block Division |

### 10.12.3 XML 選單

| 功能 | 格式與前置 | 說明 |
|---|---|---|
| Structural Design Import | TXHBD；需有連到 `SB_TID` 的資料庫 | 只匯入 Ship Parameter 資料 |
| Hull Steel Import | TXHSTL-M；連到 `SB_OGDB` | 只匯入材料資料 |
| 2D Import | TXHBD；連到 `SB_OGDB`、`SB_CGDB`、`SB_TID` | 自動建平行舯體曲面、殼結構、RSO 與平面板架。須有 `MainParticulars` 段，功能屬性須符合預先定義的 Functional Descriptions；GL Poseidon 子集可用文字檔加環境變數 `GL_ENABLED YES`、`GL_FUNCTIONAL_PROPERTIES` 啟用。可勾覆寫 General Particulars 與 FR/LP positions；同名物件會被取代 |
| RSO Import | 使用者指定檔案 | 匯入 RSO；XML 內參照的所有 Envelope 必須事先存在 |
| Surface Export | TXSUR；`SB_TID` | 選 MainSurface、曲線方向 X 或 Z、間隔 `[Start],[Step],[Stop]` 與 ReferenceSurface（可用萬用字元） |
| Structural Design Export | TXHBD；`SB_TID`、`SB_OGDB` | 勾選類別，輸入空間、艙室名稱（可萬用字元）與要切出的肋位（`FR 25`、`FR25-200` 或絕對座標 `27500`） |
| Hull Steel Export | TXHSTL-R；`SB_OGDB` 與 `SB_CGDB` | 從樹狀視圖挑 Block 或板架；第二頁可啟用 Idealization、設 snap 距離與 Joint Lines |
| RSO Export | 使用者指定檔案 | 匯出所有現有 RSO |

> 〔公開版未收錄：AVEVA 官方產品截圖〕2D XML Import 設定對話框

*圖 10-13　2D XML Import Settings 對話框。設定平行舯體曲面名稱與前後端位置、板架放入的 Block 名稱，以及是否覆寫 General Particulars 與 FR/LP 位置。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** XML 是與驗船機構與外部分析軟體交換資料的主要通道，但「哪個驗船機構接受哪個格式」官方此處只提到 GL Poseidon 範例，其他社的對應〔待核對〕。

### 10.12.4 Analysis 選單

| 功能 | 輸入 | 結果與重點 |
|---|---|---|
| Section Modulus | 目標位置的橫剖面視圖 | 計算總面積、中和軸高度、慣性矩、龍骨與甲板處的斷面模數；個別項目可設折減係數（存在視圖內，下次沿用）。輸出 `SEC_MOD_<X-position>_<running number>.csv`（如 `SEC_MOD_FR54_1.csv`）到 `SB_SHIPPRINT`；`SBH_SECMOD_FD` 改以功能描述顯示，`SBH_SECMOD_NAMES` 指定的檔案可控制全域流水號 |
| Weld Calculation | 選一個或多個 Block | 列出所有連接的焊接型式與長度（CSV） |
| Block Preliminary WCOG | 逗號分隔的輸入檔（三種格式：完整 Block 格式、Block Create from CSV 格式、單純 Block 名稱清單） | 以多個軸對齊盒子虛擬切分船體，計算各盒內鋼料重量與重心，結果附加到輸入檔每列尾端；固定密度 `7.84E-6`（不考慮實際材料），不計 Design Block；可反覆重跑，格式 2 被接受後可直接用同一檔建 Production Block |
| WCOG | 選船體板架 | 重量與重心；兩階段：存入板架時（不含斜角間隙、餘量、加強筋缺口與開孔）以及切成生產零件時 |
| Material List | 選船體板架 | 板與型材的材料估算，與生產零件是否存在無關；輸出 CSV，可在 `applications.xml` 改副檔名為固定格式；內容同 Material Ordering of Bars 與 Plates |
| Painting Areas | 樹狀對話框中的 Painting Rooms | 可由 TID Compartments 加界限定義；不含塗裝定義，只做面積分析 |
| Idealize Model | 需有 `FEMWLD` 元件與含板架的 Block | 建立理想化板架 Block（可用限制盒切出局部），可存四組分析參數 |
| Create FE Model | 理想化 Block | Recreate FE geometry、Divide／Combine shell elements、Connect FE model、Remove transition step、Unwarp shell elements；影像物件前綴 `_FGS`、`_FGB`、`_FGT`、`_FGA` |
| Export FE Model to ANSYS APDL | 理想化 Block 加 FE 模型 | 產生 `apdl` 檔；建議用新元素型式 |
| Export FE Model to Patran PCL | 同上 | 產生 `ses` 檔 |

在 2D 畫面對 RSO 或 Block 按右鍵，也會出現依物件類型而不同的分析選單。FE 模型的詳細操作請見[第 12 章](ch12_space_fem_zh-TW.reading.html)。

> **專業提醒：** Block Preliminary WCOG 用固定密度估算，只適合在分區策略階段比較方案，**不可**拿去當重量報告。要正式重量重心，請在板架切成生產零件之後用 WCOG。

### 10.12.5 一條典型工作流

設定專案（範本專案、Hull Reference Object、`Project > Surfaces`、`FR/LP Positions`）→ 無最終曲面時用 `Midbody Surface` → 定義 Envelope 與 RSO → `Properties` 加功能描述、材料、型材與端部連接並勾選自動產鋼 → `Generate Panels` 或 Quick Panel 與 Planar 功能細修 → `Section Modulus` 檢查並迭代 → `Weld Calculation`、`Material List`、`WCOG`、`Painting Areas` 出估算 → `Block > Create from CSV` 建分區並以 `Block Preliminary WCOG` 比較 → `Verify Model` 無警告後 `Divide into Blocks` 轉入詳細設計。

### 10.12.6 Planar 與 Curved 選單摘要（只讀用途，詳見第 13、14 章）

- **Planar：** Model（建立、修改、切分加強筋等）、Panel（Copy、Move、Rename、Split、Remove Seam、Modify Symm、Topology、Compare、Knuckled）、Scheme 與 Editor（以 scheme 文字檔建板架）、View、PosNo、Select。
- **Curved：** Model（Seam/Butt、Shell Plate、Shell Profile、Shell Stiffener、Feature、Curved Panel、Hull Curve、Storable Plane/Point）、Geometry（點、平面、Shell Curve）、Default、View、Select。

## 10.13 預設檔與批次工具

### 10.13.1 預設檔 `sj700.sbd`

Structural Design 的預設參數定義在 `sj700.sbd`；Planar 與 Curved 建模的預設參數對它也有效。一般互動式 Marine 模組的預設檔由環境變數 `SBD_DEF1` 指定；若 `SBGD` 目錄下存在 `SBD_ED.DEF`，則改用它。

| 參數 | 意義 | 預設 |
|---|---|---|
| `PROD_PAN_VIEW` | 僅 Multi-View 專案有意義；設定後以 production view 模式啟動，否則以 design view | 未設 |
| `MIN_PLA_WIDTH = <width>` | 切板架時板條最小寬度，切後更窄就不切 | 50 mm |
| `MIN_STI_LENGTH = <length>` | 切板架時加強筋最小長度，更短就不分割 | 100 mm |
| `PAN_SPLIT_ECUT_*` | Block Division 定義加強筋偏移時額外可用的端切類型 | |
| `BLOCK_DIV_SSTI_OVER = <dist>` | 曲面板架分區時殼加強筋重疊量（移動切割平面使其距板架邊緣一段距離切斷） | -50 mm |

### 10.13.2 批次工具

批次程式透過 Log Viewer（JL）啟動，以邏輯變數（`SB_INPUT1`、`SB_OUTPUT1`）傳遞輸入輸出檔。

| 程式 | JL 名稱 | 作用 |
|---|---|---|
| `sj701` | Hull Block Division | 批次分區。輸入檔 `.dat`、輸出記錄 `.log` |
| `sj703` | Extract RSOs to CSV | 輸出每個 RSO 的屬性，**每個 RSO 兩列**（第二列放 Envelope 名稱與邊界）；可手動編輯 |
| `sj704` | Update RSOs from CSV file | 讀回編輯後的 CSV 更新 RSO 屬性，或新建 RSO（**僅限主平面且單一面**；複雜 RSO 須用互動工具建立） |
| `sj705` | Generate Steel from RSO | 依 RSO 屬性批次產生簡單板架，規則同 Generate Panels |
| `sj706` | Create Design Project / Remove Design Project | 建立或移除 Design Block 與板架；**Remove 選項須由系統管理員在 Log Viewer 控制檔啟用**，建議先備份 OGDB |

`sj703` 與 `sj704` 也可不經 JL，直接以命令列傳 CSV 檔名，例如 `sj703 c:\temp\rso.csv`。

**`sj701` 輸入檔語法：**

| 敘述 | 說明 |
|---|---|
| `MAIN_BLOCK, <block_name>;` | 要切分的主 Block（只能出現一次） |
| `FORCE { /MAIN \| /CURRENT };` | 被界限切到的板架放哪：留在原 Block，或放到目前處理的 Block（預設 CURRENT） |
| `KEEP { /YES \| /NO };` | 是否保留原板架；保留者失去所有拓樸資料，不能再用於生產或修改（預設 NO） |
| `PLANE, X=FR58+400;` | 切割平面，可重複 |
| `MODEL_TYPE { /ALL \| /PLANE_PANELS \| /CURVED_PANELS };` | 處理平面、曲面或兩者 |
| `SEAM, <seam_name>;`、`RSO, <RSO_name>;`、`STORED_PLANE, <plane_name>;` | 以現有 Block Seam、RSO 或 Stored Plane 作為切割體 |
| `FUNCTIONAL_BLOCK_SEAM { /CREATE \| /CREATE_ONLY \| /USE };` | Design Panel 上 Block Seam 的處理：建立、只建 Seam 不建新板架、或用作切割體 |
| `PROFILE_END /CUTTER=… /PANEL=… /DIRECTION=… /SHIFT=… /SLANT=… /FLANGE_SHIFT=… /NOTCH=…;` | 切口兩側加強筋的端部細節（SHIFT、SLANT 單位 mm；`FLANGE_*` 僅適用組合型材） |
| `BLOCK, <res_block>;` | 接收切分後板架的 Block，可重複 |

官方範例：

```
MAIN_BLOCK, 'BLOCK1';
FORCE /MAIN;
KEEP /NO;
PLANE, X=FR58+400;
PLANE, X=FR72-200;
SEAM, AAS44;
BLOCK, AABLOCK1;
BLOCK, AABLOCK2;
BLOCK, AABLOCK3;
```

**`sj703` 的 CSV 欄位：** Function（功能描述碼）、Tight、Name、Face、Principle Plane、Coord.、Auto Gen.、Mtrl Side／Th.／Qual.、Auto Stiffeners、Stiffener Side、Profile Type、Profile Dim.（如 `220*12`），以及重複的 Limits/Stiff. Ends（第一列為界限，第二列為端部連接，肘板以 `/` 接在後，如 `SNIPE/B16`）。

### 10.13.3 二次開發怎麼接

最穩定的外部整合點是 **CSV 往返**（`sj703` 匯出、`sj704` 寫回）與 Block CSV、`sj701` 輸入檔，語法官方皆完整，可由 Python 或 C# 產生後經 JL 執行。Quick Panel（Vitesse API）、XML schema、`applications.xml` 自訂作業語法本章依據不足，〔待核對〕。

> **專業提醒：** 先用 `sj703` 匯出 CSV，用 Excel 或 Python 找出尚未設定 Auto Gen.、材質或型材的 RSO，比逐一開 Properties 快得多；批次改完用 `sj705` 一次產鋼，最後記得 `Verify Model`。

## 10.14 本章小結

- Assembly Planning 以 `ASWL`、`ASMBLY`、`ASITEM` 三層把設計零件重組成生產樹；零件經看不見的代理被參照，一件只能屬於一個組立（`GPART` 除外）。`ASORI` 決定製造擺放方向，也決定組立圖視角。
- Assembly ADP 的核心是 Drawing Template、Backing Sheet 保留區、Task 與 PML 函式、Parts List Template 與 `assydrwg.cfg`；可靠度關鍵在 Update 路徑、圖號索引與 Link Folder。
- Structural Design 主線：RSO、Properties、Generate Panels、分析估算、Verify Model、Divide into Blocks。
- 可靠的程式整合點是 Assembly 擬似屬性與 `AssemblySelection`、Structural Design 的 CSV 往返與 Block CSV；Vitesse 與 XML schema 本章依據不足。

## 10.15 練習題與自我檢核

1. 畫出 `ASWL`、`ASMBLY`、`ASITEM`、設計零件的關係，並說明為何刪除組立不會刪除零件。
2. 一塊板架已屬於組立 A，拖進組立 B 會怎樣？若要讓吊環同時出現在兩個組立，該用什麼？
3. `ASORI = 8` 時系統如何選基準板？
4. 保留區的 `Nrows`、`Origin Topleft` 為什麼要與符號標籤一致？
5. 圖號用 MDB 掃描方式在 5,000 張圖後會怎樣？如何改用 NSEQ？
6. 設計每晚為「Those not drawn」組立出圖的批次作業，需要哪些檔案、帳號與排程？
7. 某 RSO 功能碼為 9200，Generate Panels 會產生什麼？
8. 用 `sj703` 與 `sj704` 設計流程，把 100 個 RSO 的板厚統一改為 12 mm。

自我檢核：我能列出 `ASORI` 九個值；分辨 Update 與 Regenerate；說出新專案四件事與 Generate Panels 的功能碼範圍；指出哪些二次開發介面有官方依據。

## 10.16 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 10 章](appx_d_verification_zh-TW.reading.html#ch10)；取材覆蓋與未讀範圍：見[附錄 E 第 10 章](appx_e_coverage_zh-TW.reading.html#ch10)。
