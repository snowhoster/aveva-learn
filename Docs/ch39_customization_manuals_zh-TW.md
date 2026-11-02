# 第 39 章　客製化官方手冊導讀：Software Customization、.NET Customization、Data Access Routines 與 Marine Customization

> 第 31–36、38 章已把 PML、PML 表單與 Add-in、.NET（CAF）與 Vitesse 講過一輪（除錯與部署在本章之後的第 40 章）。本章換個角度：**站在官方手冊的目錄前面**，說明 AVEVA Marine 12.1 離線文件 Customization 這一大類有哪幾本書、各自涵蓋什麼、對應本課程哪一章，並補上既有章節沒講到的部分：Data Access Routines（DARs，資料存取常式，FORTRAN／C 介面）、PML 的 Unicode 與升級政策、PML Add-in 與 Core 管理物件、PML Publisher 加密，以及 .NET 手冊中的 UIC 編輯器、資料庫介面、事件、單位與 My Data；最後補「客製化規劃」與「船舶座標顯示客製」兩篇 Marine 專屬短文。不重複 PML 變數、`handle`、表單定義、CAF 基本流程、PML.NET 型別對應等已講透的語法，只用連結導回。
>
> **資料可信度：** 全部取材自 Customization [1105730] 與 Marine Customization [1305437]；程式碼僅取頁面確實出現的片段並標明頁面 ID。注意：(1) 內容多沿用 PDMS 時代手冊，仍有 PDMS、Mk12.0、Visual Studio 2005 等字樣；(2) 部分範例有排版瑕疵（如 C++ 風格的 `->`），已照意思整理並列入〔待核對〕；(3) 離線文件中文欄為機器翻譯，譯名以台灣慣用為準。**能否在你們的 12.1 安裝重現，請用訓練專案驗證。** 章末〔待核對〕與「取材覆蓋」誠實列出未讀與不確定之處。

## 39.1 學習目標

讀完本章，你應該能夠：

1. 說明官方 Customization 五本手冊與 Marine Customization 的結構與用途，並對照第 31–36、38、40 章找到該查哪一本。
2. 依官方 Customization Planning 列出客製化前的準備工作，以及船體、組立、焊接各領域可客製的項目。
3. 說明 Data Access Routines 的定位（**唯讀**、FORTRAN 77、`D3` 常式家族）及與 PML、.NET 資料庫 API 的差異。
4. 讀懂 DARs 程式骨架：`D3INIT`→`D3MMDB`→導覽→讀取→`D3FIN`，並理解錯誤旗標與 `D3ERST`。
5. 說明 PML 的 Unicode 規則、命名前綴與「只改使用者區」的升級政策，並使用 `!!CE`、`VAR … EVALUATE`、`onerror`、`return error`。
6. 說明 PML Add-in、Core 管理物件、EDG 與 PML Publisher 加密的概念與限制。
7. 說明 .NET 客製化的介面組件、CAF 的 `IAddin`／`Command`／`WindowManager`／UIC，以及 `DbElement` 修改管線、事件、偽屬性外掛與 `DbDouble` 單位。
8. 啟用並設定船舶座標的客製化顯示（`SHIPCO`、`RSDIM`），解釋輸出格式與回退規則。

## 39.2 官方客製化手冊地圖

### 39.2.1 手冊結構

Customization [1105730] 約 737 頁，下分四個子樹；另有獨立的 Marine Customization [1305437]（約 15 頁）。

| 官方手冊（頁面 ID） | 規模 | 內容重點 | 本課程對應 |
|---|---|---|---|
| Software Customization [1134643]（指南 [1133230]＋Reference [1134097]） | 約 560 頁 | PML2、表單選單、Gadget、Alert、FMSYS、PML Add-in、Core 管理物件、View 操作；Reference 有物件總表、EDG、PML1 運算式 | [第 32 章](ch32_pml_language_zh-TW.reading.html)、[第 33 章](ch33_pml_database_zh-TW.reading.html)、[第 34 章](ch34_pml_forms_addins_zh-TW.reading.html)、[第 40 章](ch40_debug_deploy_zh-TW.reading.html) |
| PML Publisher [1150394] | 約 20 頁 | `pmlencrypt.exe`、授權、緩衝、存取密碼 | 第 40 章 40.8（本章補 12.1 頁面細節） |
| NET Customization [1147959] | 約 113 頁 | CAF Addin、UIC 選單客製、資料庫介面、PMLNet、Grid、My Data、File Browser | [第 35 章](ch35_dotnet_zh-TW.reading.html)、第 34 章 34.10 |
| Data Access Routines [1135545] | 約 57 頁 | FORTRAN 77／C 的唯讀資料存取常式庫 | 既有章節未涵蓋（39.4） |
| Marine Customization [1305437] | 約 15 頁 | 客製化規劃、`marAPI.dll` 索引、船舶座標顯示 | [第 36 章](ch36_hull_vitesse_zh-TW.reading.html)、第 35 章 |

### 39.2.2 需求到手冊的查找表

| 你想做的事 | 官方哪裡 | 本課程 |
|---|---|---|
| 寫 PML 函式、物件、巨集；表單選單 | Software Customization | 第 32、34 章 |
| 加密 PML 後交付 | PML Publisher | 第 40 章；39.5.8 |
| 寫 C# Addin、PML 呼叫 C# | NET Customization | 第 35 章；39.6 |
| 用 FORTRAN／C 離線讀專案資料 | Data Access Routines | 39.4 |
| 規劃導入與客製化範圍 | Marine Customization | 39.3 |
| 顯示「離某艙壁多遠」 | Marine Customization：Ship Coordinates | 39.7 |

## 39.3 Customization Planning（客製化規劃）

頁面：[1112173] 及其下 8 頁。官方說明其目的是概述客製化選項，作為**擬定詳細實施計畫的基礎**；它列出「許多但非全部」常客製化的功能，細節要到各應用程式專屬文件查。

### 39.3.1 客製化之前的準備（[1112175]）

| 項目 | 官方要點 |
|---|---|
| 實施組織 | AVEVA 與客戶的技術窗口是客戶的 **system manager（系統管理員）**，宜於導入初期就參與 |
| 硬體與使用者訓練 | 硬體與作業系統通常由客戶先裝好；使用者要先受過各應用程式訓練 |
| 實際安裝 | 首次安裝通常由 AVEVA 做，**不含任何客製化**，含預設設定與範例測試專案，以驗收測試收尾；新版與更新通常由客戶管理員處理 |
| 系統管理程序 | 決定存取控制（誰能用哪些工具、目錄、專案）、以授權管理工具設定產品存取、啟動第一個專案、磁碟管理與備份 |
| 工作流程與工法 | 決定位置編號命名規則、對稱慣例；車間生產資訊可高度量身訂做，並建立「團隊—區域—分段—模組」的使用；分包商資訊流；姊妹船資料重用 |

這與 [第 43 章](ch43_system_administration_zh-TW.reading.html) 的系統管理責任一致：**客製化是穩定管理基礎上的第二步**。

### 39.3.2 各領域可客製項目

官方依領域列出「可客製項目→要讀的專題」，頁面本身只是索引（括號為頁面 ID）：

| 領域 | 可客製項目（官方原文要點） |
|---|---|
| 一般（[1112176]） | 標準書（Standard book）、圖框等製圖通用項目（SB028 處理標準物件） |
| 結構設計（[1112177]） | 自動套用船體與製圖的客製化結果 |
| 船體與工廠自動化（[1112178]） | 材料品質、型材開孔（透過巨集）、端切標準與預設端切、坡口標準、法蘭標準、肘板（Bracket）標準、收縮補償、Swedging、型材標準、折曲板、餘量種類、切割用 CL 格式（Generic Postprocessor）、零件名稱控制、角焊縫自動設定（Execution Units）、Clips、變形補償 |
| 組立規劃（[1112179]） | 組立資料庫預設值、零件名稱、組立零件清單、自動組立圖；船體的客製化自動在組立規劃生效 |
| 焊接規劃（[1112180]） | 焊接分析設定與焊接參數 |
| Developer's Toolkit（[1112181]） | 開發新功能的環境（含 Vitesse），官方「強烈建議」客戶研究 |

> **專業提醒：** 這是**客製化範圍盤點表**。專案啟動時把每項標成「用預設／要改／不適用」；能用設定解決的就不寫程式（與第 31 章「不修改官方檔案」原則一致）。

### 39.3.3 Marine .NET API（marAPI.dll）索引

頁面 [1112182] 說明：以下功能在 `marAPI.dll`；要在 Hull Design 與 Marine Drafting 模組使用，須參考 PML 文件中「在 PML 使用組件（assembly）」的方式（即 [第 35 章](ch35_dotnet_zh-TW.reading.html) 的 PML.NET 機制）。索引頁 [1305435] 列出：

- **Modules（8 個）：** MarChm、MarDex、MarDrafting、MarHullPan、MarModelStruct、MarUi、MarUtil、MarWeldMod。
- **Classes（約 90 個）：** 以 `Mar` 開頭，例如 `MarPoint`、`MarVector`、`MarLine`、`MarArc`、`MarPolygon`、`MarContourPlanar`、`MarModel`、`MarSymbol`、`MarText`、`MarWeld`、`MarPanelSchema`、`MarPythonEngine`。

索引只有名稱，沒有方法簽章（〔待核對〕）。

## 39.4 Data Access Routines（DARs，資料存取常式）

頁面：Data Access Routines [1135545] 及子樹約 57 頁。**這是本課程既有章節完全沒有講的一塊。**

### 39.4.1 定位

官方定義：DARs 是一組 **FORTRAN 77 子常式**，可併入使用者自寫的軟體，用來**導覽與讀取** Marine 專案內的資料。預期用途是建立與其他軟體的介面（例如材料統計、管路應力分析、等角圖）。功能分五類：初始化、導覽、屬性讀取、錯誤處理、工具常式。

三個關鍵限制（頁面 [1135545]、[1135556]）：

1. **完全唯讀**。官方明言「不提供寫入或更新資料庫的功能」；初始化常式以唯讀模式開啟所有有權限的資料庫，所以不會因程式或機器故障損毀專案資料。
2. 使用前需要有效的專案名、使用者名稱與密碼，系統會檢查權限；DARs 程式的使用者**計入 Marine 使用者數**，並做 site file（現場授權檔）檢查，致命錯誤時程式不會繼續。
3. 概念沿用 Marine 的**目前元素（current element）**：要讀屬性，必須先用導覽常式移動到該元素，再呼叫對應的讀取常式。

### 39.4.2 與 PML、.NET 資料庫 API 的比較

| 面向 | DARs | PML／`!!CE`（第 33 章） | .NET `DbElement`（39.6.5） |
|---|---|---|---|
| 執行位置 | 獨立外部程式（`.exe`） | Marine 模組內 | Marine 模組內（同一程序） |
| 讀寫 | 只讀 | 讀寫 | 讀寫 |
| 語言 | FORTRAN 77；另有 C／C++ | PML | C#（及其他 .NET 語言） |
| 典型用途 | 離線匯出到其他分析軟體 | 工具、報表、批次修改 | Addin、整合 |

> **專業提醒：** 新專案要匯出資料，優先考慮第 35、38 章的 .NET／報表路線；DARs 的價值在於**既有的 FORTRAN／C 舊程式要接資料**，或需要一支保證不會寫入的獨立程式。手冊仍以 PDMS Mk12.0 為版本基準（39.4.6）。

### 39.4.3 常式家族

常式以 `D3` 開頭，第三個字母表示類別（[1135566]–[1135572]）。

| 類別 | 常式 | 用途 |
|---|---|---|
| 初始化 `D3I` | `D3INIT` | 驗證專案、使用者、密碼；開啟資料庫；設定監看（monitor）等級 |
| 導覽 `D3M` | `D3MMDB`、`D3MCDB`／`D3MEDB`／`D3MDDB`／`D3MQDB` | 選 MDB；對應 `CURRENT`／`EXCHANGE`／`DEFER`／`STATUS` |
| | `D3MNAM`、`D3MNUM`、`D3MREL`、`D3MOWN` | 依名稱／順序位置（如 `BRAN 3`）／相對位置（`LAST MEMB`）／移到擁有者 |
| | `D3MSAV`、`D3MRST` | 儲存／還原位置，須成對，巢狀最深 10 層 |
| 讀取 `D3R` | `D3RTYP`、`D3RNAM`、`D3RREF` | 型別、名稱、參照號 |
| | `D3RINT`／`D3RIA`、`D3RREA`／`D3RRA`、`D3RLOG`／`D3RLA`、`D3RTEX`、`D3RWOR`／`D3RWA`、`D3RRFA` | 整數、實數、邏輯、文字、字（word）、參照（含陣列版） |
| | `D3RPRL`、`D3RORL`、`D3RPAT`、`D3RBOX` | 相對座標系的位置、方位；PPoint；外接盒 |
| 錯誤 `D3E` | `D3ECHK`、`D3EMSG`、`D3ERST` | 開關錯誤處理、取訊息、重設旗標 |
| 工具 `D3U` | `D3UMON`、`D3UDEH`、`D3ULDS`、`D3UINI` | 改監看等級、還原雜湊字、測時戳、查是否已初始化 |
| | `D3UGTU`／`D3UCLU`、`D3ULEN`、`D3UCTI`／`D3UCTR`、`D3UDTM` | 檔案單元、字串有效長度、字串轉數值、日期時間 |
| 結束 `D3F` | `D3FIN`、`D3FEND` | 關閉專案；結束程式 |

另有原始碼形式的「輔助常式庫」（官方**不保證支援**），如 `D3QMEM`、`D3QCMA` 與各資料庫元素的 `D3Q…` 查詢（`D3QPIP`、`D3QBRA`、`D3QEQU`）。UDA 以前導 `:` 識別；未設值的動態陣列回傳「Attribute not found」，動態文字回傳「Attribute unset」（[1135599]、[1135600]）。

### 39.4.4 程式骨架（出處：Example 1，[1135562]）

官方範例：移到 `/100-B-1` 第 1 個 Branch 的最後一個法蘭，取 Spec 參照，再讀元件參數（完整宣告與輸出見官方頁）：

```fortran
      CALL D3INIT( 'DAR', 'SYSTEM', 'XXXXXX', 'FULL', ' ', ID3ERR )
      IF ( ID3ERR .NE. 0 ) GOTO 12345
      CALL D3MMDB( 'DESIGN/PLANT', ' ', ID3ERR )
      CALL D3MNAM( '/100-B-1', ID3ERR )
      CALL D3MNUM( 'BRAN', 1, ID3ERR )
      CALL D3MREL( 'LAST', 'FLAN', ID3ERR )
      CALL D3RNAM( 'SPRE', SPCREF, ID3ERR )
      CALL D3RRA( 'PARA', 100, PARAMS, ID3NOU, ID3ERR )
12345 CONTINUE
      CALL D3EMSG( ID3ERR, .TRUE., CD3MSG )
      CALL D3FIN( ID3ERR )
      CALL D3FEND
```

1. `D3INIT` 五個參數：專案、使用者、密碼、監看等級（`NONE`／`SOME`／`FULL`）、保留的讀寫鑰匙（傳空白）。專案名只取前 3 字元；密碼最多 6 字元且**區分大小寫**；連續三次 `D3INIT` 失敗後續一律失敗（規格頁 [1135573]）。
2. 以 `FULL` 監看時每次呼叫都印出常式名與全部輸入輸出，是**最便宜的除錯方式**；範例輸出可見專案不存在時回傳 108 `Project not found`。

### 39.4.5 錯誤處理與字串規則

**錯誤旗標。** 每個常式以最後一個引數 `ID3ERR` 回傳狀態（0 成功，正值錯誤）。一旦出錯，DARs 設內部旗標，**阻止進入下一個常式**（除 `D3FIN`、`D3EMSG`、`D3ERST`、`D3UMON`），避免拿到無意義的資料。刻意製造的錯誤（例如以「無下一個成員」結束迴圈）要用 `D3ERST` 重設；官方在 `D3QMEM` 範例中對 202、203 呼叫 `D3ERST` 並把 `ID3ERR` 歸零（[1135553]）。

| 錯誤碼區段 | 例子（[1135586]） |
|---|---|
| 0–99 一般 | 2 旗標未重設、3 未 `D3INIT`、4 未 `D3MMDB`、5 輸出字串太短 |
| 101–199 初始化 | 102 密碼錯、103 未知使用者、108 找不到專案、110 找不到 MDB、113 資料庫使用中、115 site file 錯誤、116 專案名無效 |
| 201–299／301–399／401–499 | 導覽／讀取／資料庫 |

**字串。** 傳入字串忽略尾端空白；傳回字串以空白補滿且永不未定義（空字串回 `' '`），有效長度用 `D3ULEN`。字元與邏輯引數須在呼叫端明確宣告（`CD3…`、`LD3…`）。

**多位元組文字（[1135560]、[1135590]）。** 專案以 `PROJECT MBCHARSET` 標為多位元組時，漢字等遠東文字以 `&~` 開始、`&(` 結束的跳脫序列夾住位元組對輸入輸出（真正的 `&~` 寫成 `&&~`）。〔待核對〕12.1 已 Unicode，此規則是否適用，文件未說明。

### 39.4.6 版本、編譯與部署

| 主題 | 官方說明 |
|---|---|
| 版本（[1135575]–[1135577]） | DARs 版本與所含 PDMS 版本一致；同大版本的小版本相容；**跨資料模型（DDL）變更必不相容**。`D3INIT`、`D3MMDB` 會檢查相容性，每次 `D3INIT` 印版本橫幅 |
| 程式庫（[1135578]、[1135579]） | 動態庫 `d3lib.dll`（執行時需在 `PATH`）＋ `d3lib.lib`；另有 `d3extras.f`、`compload.bat`、驗收程式 `d3test`、測試專案 `dar000`／`dar100`；通常在 `%PDMSEXE%\dars` |
| 編譯（[1329751]） | 文字寫 Microsoft `cl` 與 Intel `ifort`；Fortran 需 `/iface:cref /iface:mixed_str_len_arg /libs:dll /threads /recursive /op /real-size:64`，寫在 `ifort.cfg`，以環境變數 `IFORTCFG` 指向 |
| 重新連結 | 新版 DARs 發行後所有既有可執行檔都應重新連結（[1135584]） |

### 39.4.7 C／C++ 介面

DARs 同時提供 C／C++ 介面（[1135591]–[1135596]）：常式名稱相同但**小寫**（`d3init`）；標頭檔 `d3libc.h`（含 `pdms.h`），以 `ccompload.bat`（C）、`cxxcompload.bat`（C++）編譯；**所有引數以位址傳遞**，整數與邏輯輸入也要傳 `&ival`；字串不帶長度，呼叫端必須自行保證輸出字串夠長（例如 `PDMS_TEXT` 長度為 120）。

> **專業提醒：** 官方明說：在 C／C++ 中，錯誤碼 5（字元輸出引數太短）**不會被回傳**，過短的字串會直接溢位並可能損壞其他變數。用 C 呼叫 DARs 時，輸出緩衝一律使用標頭檔定義的型別（`PDMS_TEXT`、`PDMS_NAME`、`PDMS_WORD`），不要自己宣告 `char x[2]`。

## 39.5 Software Customization 補充主題

既有第 32、34 章已講 PML 語法與表單，本節只補**官方手冊中既有章節未講或僅一筆帶過**的主題。

### 39.5.1 PML 的 Unicode 與檔案編碼（[1133231]、[1133355]）

- 自 PDMS 12.1 起，所有文字資訊以 Unicode 表示；PML 字串內部格式為 **UTF-8**，PML 變數名、表單／Gadget 名、方法與函式名也可使用 Unicode 字元。
- PML 原始檔必須是：**含 BOM 的 UTF-8**（優先）、含 BOM 的 UTF-16／UTF-32，或**嚴格 7 位元 ASCII**（32–127）。
- 官方警告：8 位元非 Unicode 字元（如 Latin1 的 °、CP1252 的 €）在 `CADC_LANG` 設為韓、中、日時可能讀不出來；外文檔名在某些版本控制系統可能有問題。

### 39.5.2 升級政策與命名（[1133233]、[1133236]、[1133237]）

官方「嚴重警告」：客製化的巨集不再受 AVEVA 控管，可能與未來版本不相容，AVEVA 只能對自己控制的產品給完整支援。官方的四項建議（只改使用者區的複製品、`PMLLIB` 多目錄搜尋、遵循標準 Appware 風格、新名稱加公司前綴，官方舉例公司 XYZ 以 `XYZ` 開頭）與第 31 章一致，做法詳見[第 31 章 31.6 節](ch31_dev_environment_zh-TW.reading.html)。

官方列出現有 Appware 的前綴，如 `DES`（Design）、`DRA`（Draft）、`HULL`（Hull Design）、`MDRA`（Marine Drafting）、`ASSY`（Assembly）、`ISO`（Isodraft）、`SPL`（Spooler）、`CAT`（Paragon）、`MON`（Monitor）、`GLB`（Global）。**自己的前綴不要與這些重複。**

### 39.5.3 在 Marine 中使用 PML（[1133327]–[1133333]）

| 主題 | 要點 |
|---|---|
| `!!CE` 串接 | 可沿參照串接，如 `!!CE.cref.pspec.rating`；P-point 以下標存取（`!!CE.Pposition[3]`） |
| 指派屬性 | `!!CE.Built = TRUE`；物件型屬性（如 `POSITION`）要先取出、改成員、整個設回 |
| 工作階段資訊 | `current session`、`sessions`、`projects`、`teams`、`users`、`mdbs`、`dbs`；例 `!C = current session`、`!C.MDB()` |
| `RAW` | 表單選單介面預設去掉換行、壓縮空白；`VAR !v RAW …` 關閉 |

`!!CE` 基本用法見[第 33 章 33.3.1 節](ch33_pml_database_zh-TW.reading.html)，`NULREF`／`BADREF` 見[第 33 章 33.3.3 節](ch33_pml_database_zh-TW.reading.html)，`VAR … EVALUATE` 見[第 33 章 33.5.4 節](ch33_pml_database_zh-TW.reading.html)，`MARKDB` 見[第 33 章 33.9.3 節](ch33_pml_database_zh-TW.reading.html)。

### 39.5.4 錯誤處理與偵錯補充（[1133344]–[1133364]）

`handle`／`elsehandle ANY`／`NONE`、`onerror RETURN`／`GOLABEL`／`CONTINUE`／`PAUSE` 與 `return error`（含 `noalert`、自訂編號與 `handle 1`）已在[第 32 章 32.13.3 節](ch32_pml_language_zh-TW.reading.html)逐項列表，此處不重複。官方另有幾點補充：`onerror CONTINUE` 會套用到**之後所有巢狀呼叫**；`onerror PAUSE` 等同 `$M-`，以 `$M+` 繼續，**不可留在正式程式**；`!!Error.Text`／`.Command`／`.Line`／`.Callstack` 可取得錯誤細節與呼叫堆疊。

錯誤 `(46,28)` 中 46 是偵測模組、28 是錯誤碼。檔案物件常見錯誤：`(160,9)` 檔案不存在、`(160,44)` 檔案已存在且不覆寫、`(41,319)` 權限不足。

偵錯工具中，逐行追蹤（`PML TRACE`、`$R100`／`$R0`、環境變數 `PMLTRACE=ON`）見[第 32 章 32.14.2 節](ch32_pml_language_zh-TW.reading.html)，第 40 章 40.2 會整理成除錯工具表。官方補充兩點：`alpha log /file` 記錄全部指令與輸出，但**不含**標準 PML 追蹤，需 `$R102` 導向；`$M-`／`$M+` 暫停與繼續不適用函式與方法。

### 39.5.5 Alert 與 FMSYS（[1133537]–[1133550]）

**Alert** 不必建表單即可顯示訊息，且**一律阻擋**：`!!Alert.Error/Message/Warning('…')`（單一確認鈕）、`!Answer = !!Alert.Confirm('…')`（YES／NO）、`.Question`（YES／NO／CANCEL）、`!!Alert.Input('提示','預設值')`（取文字，相當於 tty 的 `Var !x read`，官方建議少用）；可加 `0.25, 0.1` 指定標準化螢幕位置。

**FMSYS**（Forms and Menus System）提供與特定表單無關的系統方法：

| 方法 | 用途 |
|---|---|
| `SetDefaultFormLayout('VarChars')` | 設預設版面模式；表單可加 `FixChars` 維持舊版面 |
| `setProgress(n)`、`setInterrupt(button)`、`Interrupt()` | 狀態列進度條與使用者中斷長時間 callback |
| `CheckRefs(true)` | 關閉載入表單時的參照檢查，可明顯改善效能 |
| `SplashScreen(false)`、`DocsAtMaxScreen(false)` | 移除殘留啟動畫面；關閉預設放置位置（寬螢幕、雙螢幕） |
| `currentDocument()`、`loadForm(name)`、`SetMain(app)` | 取目前文件表單；強制載入並取得表單參照；切換主應用程式 |

### 39.5.6 PML Add-in 與 Core 管理物件（[1133553]–[1133583]）

**PML Add-in** 可：在主選單列顯示為一個應用程式、定義選單與工具列、對既有應用程式增刪選單欄位、在啟動或切換應用程式時執行函式。官方要求區分「應用程式 Add-in」（出現在 Applications 選單）與「只修改既有應用程式的 Add-in」。

控制物件有 `appCntrl`／`appDefn`（應用程式切換與定義）、`appTbarCntrl`、`appMenuCntrl`（工具列與選單欄位的可用性）、`appFormCntrl`（在建構子中註冊的表單於切換與重進時的行為）。

`.modifyMenus()`、`.modifyForm()` 的呼叫時機與 Add-in 載入流程見[第 34 章 34.12 節](ch34_pml_forms_addins_zh-TW.reading.html)，APPMENU 選單見[第 34 章 34.11 節](ch34_pml_forms_addins_zh-TW.reading.html)。官方補充：工具列以 `frame .name toolbar '說明'` 定義，**表單建立後不能再加工具列**，須由 `.modifyForm()` 於建表單時加入。應用程式定義放在 `module\DFLTS\APPDEFNS`（一應用一檔），取代舊的 `DFLTS\APPLICATIONS`。官方警告這些機制「仍在發展」，建議把 Add-in 定義與功能程式分開。

**Core 管理物件（Appendix A）** 供 AVEVA 核心開發者用：表單以 `SETUP FORM !!myform blockingdialog resi CORE` 宣告，Gadget 與選單欄位也可加 `CORE`（如 `!menu.Add('CORECALLBACK', …)`）；核心管理的表單不應定義 `INITCALL`、`AUTOCALL`、`OKCALL`、`CANCELCALL`。一般客製化用不到，但看到 `CORE` 關鍵字時要知道意思。

### 39.5.7 EDG：事件驅動圖形（[1134214]–[1134229]）

Reference 的 Event-driven Graphics 說明 Design 圖形視窗的**選取（pick）序列**如何以物件組織：全域 `!!edgCntrl` 管理「作用中事件」「堆疊事件」與已註冊圖形視圖；每個事件由 **edgPacket** 定義，其挑選序列由 **edgPickPacket**（含 edgPickType）定義。

> 〔公開版未收錄：AVEVA 官方產品截圖〕EDG 控制系統：!!edgCntrl 含作用中事件、堆疊事件與圖形視圖，視圖的選取動作匯入 Pick Action

*圖 39-1　EDG 控制系統概念圖。（AVEVA 官方文件截圖，僅供內部教學）*

edgPacket 重要成員：`.priority`（0 為主要封包，已有主要封包時會詢問是否取代）、`.form`（加入時自動顯示、移除時自動隱藏）、動作字串 `.initialization`／`.action`／`.close`／`.continue`／`.escape`（**須為標準指令、PML 函式或方法，不可用舊式巨集**）、`.input`／`.return`（以 `!this.input`、`!this.return` 取用）。〔待核對〕僅讀到 edgCntrl、edgPacket、edgPickPacket 三頁，pick 型別與預設挑選序列方法未讀。

> **專業提醒：** 要寫「連續點選幾個東西再執行」的互動工具，EDG 是官方標準做法；第 34 章的表單 callback 只處理表單事件。

### 39.5.8 PML Publisher 的 12.1 頁面細節（[1150394]–[1150423]）

第 40 章 40.8 會介紹 `pmlencrypt.exe` 的基本用法與取捨（[第 40 章 40.8 節](ch40_debug_deploy_zh-TW.reading.html)），本節先補官方 12.1 頁面的細節：

| 項目 | 官方說明 |
|---|---|
| 授權 | 工具另行授權（授權檔需 `VPD-PMLPUBLISHER`）；**加密後的 PML 在任何相容的 AVEVA 程式中執行不需額外授權** |
| 嚴重警告 | AVEVA 可能變更演算法而需重新加密；**強度有限、不保證安全**；加密由所有使用者共用（任何相容版本的人都能執行你們加密的檔案）；加密後不可讀不可編，**官方不提供解密工具**，必須自行保存原始碼 |
| 流程 | 備份原始碼→複製來源夾→從副本加密回來源位置（只覆寫可辨識的 PML）→比對→測試 |
| 緩衝 | 標頭行可含「演算法 ID 後接 `-數字`」，讀過該次數後常駐記憶體；建議 `-buffer 5`；開發中可用 `PML REHASH`、`PML INDEX` 清除 |
| 存取密碼與資料庫保護 | 資料庫可標為「受保護」阻止匯出關鍵屬性；管理者在該 DB 設存取密碼，加密 PML 內密碼相符才能讀受保護屬性；未加密 PML 與 C# 一律拒絕。**程式作者有責任不顯示或匯出屬性值**，需嚴格審查 |
| 錯誤與除錯 | `(46,103)` 檔案損毀、`(46,104)` 過時格式（舊 type 3 須以 type 4 重新加密）；以 `$R` 顯示時每行為 `<hidden>` |

## 39.6 NET Customization 補充主題

第 35 章已逐行解說 `starter-kit-mybrowser` 與 PML.NET。本節補 .NET 手冊中的**架構、CAF 細節、UIC 編輯器、資料庫介面與周邊元件**。

### 39.6.1 架構與介面組件（[1147960]–[1147966]）

官方說明 .NET 客製化可與既有 PML 客製化並存，兩種方法（.NET Addin 與 PML.NET）都是在執行時動態載入 .NET 組件（dll）到模組。

> 〔公開版未收錄：AVEVA 官方產品截圖〕.NET 客製化架構：模組含 CAF、PML Engine、PML.NET Engine、.NET Interfaces 與資料庫層；PML 程式、PML 可呼叫組件、.NET Addin 位於兩側

*圖 39-2　.NET 客製化架構：PML 與 .NET 並存，共用 CAF 與資料庫層。（AVEVA 官方文件截圖，僅供內部教學）*

| 介面組件 | 主要內容 |
|---|---|
| `Aveva.ApplicationFramework.dll`、`…Presentation.dll`（CAF） | 命名空間 `Aveva.ApplicationFramework`：`AddinManager`、`ServiceManager`（元件發布服務並供查詢）、`SettingsManager`（跨工作階段保存設定）；`…Presentation`：`CommandBarManager`、`CommandManager`、`ResourceManager`、`WindowManager` |
| `Aveva.Pdms.Database.dll`、`PDMSFilters.dll` | `DatabaseService`（唯一用途是開專案）、`DbElement`、`DbElementType`、`DbAttribute`、`DB`、`MDB`、`Project`、`DbEvents`、`DbExpression`、`DbRule`、`DbPseudoAttribute`、`DbUserChanges`、`Table` 等 |
| `Aveva.Pdms.Shared.dll`、`…Geometry.dll`、`…Ultilities.dll`（官方拼寫）、`…Graphics.dll` | 目前元素與選取事件；幾何；訊息、字串、追蹤、undo、單位（**也能存取命令列，但不受支援**）；繪製清單與顏色 |

範例在安裝目錄的 `Samples.zip`（須解壓到安裝目錄，否則組件參照失效）：`AttributeBrowserAddin`、`ExamplesAddin`（因會建立並 claim Design 元素，需在 Design 的 multi-write 資料庫執行）、`NetGridExample`、`PMLNetExample`、`PMLGridExample`。範例以 Visual Studio 2005 為基準〔待核對：12.1 實際支援的 Visual Studio 與 .NET 版本〕。

### 39.6.2 Addin 的元件分工（[1147974]、[1147976]）

官方建議把 Addin 拆成四個概念並各自封裝：**Addin 本身行為**（`IAddin`）、**GUI 控制項與對話框**、**應用程式碼**、**管理 GUI 互動的碼**（GUI Manager）；可重用的控制項（如 `NetGridControl`）放獨立組件；要在 TTY 或批次執行的應用碼也應獨立；Addin 之間避免相依。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Addin 元件圖：AVEVA Host 的 Addin Control、Menus／Tools、User PML 經 IAddin、Command、API 介面連到 Addin、GUI Manager、Application code 與 Controls／Dialogues

*圖 39-3　Addin 各元件與宿主程式之間的溝通介面。圓圈是各元件公開的介面。（AVEVA 官方文件截圖，僅供內部教學）*

視窗與控制項在啟動時建立，但**資料等視窗第一次顯示才填入**（lazy evaluation，延遲求值）；官方目標是**單一 Addin 啟動不超過 1 秒**。

### 39.6.3 CAF 服務與 Command（[1147977]–[1147988]）

**WindowManager。** 建立停駐視窗與 `SaveLayout = true`、`WindowLayoutLoaded` 的用法已在[第 35 章 35.5.1 節](ch35_dotnet_zh-TW.reading.html)、[第 35 章 35.5.2 節](ch35_dotnet_zh-TW.reading.html)逐行解說。官方另列 `CreateDockedWindow(key, title, control, DockedPosition)` 與 `CreateMdiWindow` 兩個入口，`Key` 須唯一，建議 `Aveva.<AddinName>.<WindowName>`；啟動時建立的停駐視窗若未設 `SaveLayout = true`，版面還原會出現「Missing／Extra DockedWindow」警告。

**Command。** 官方推薦以 Command 物件連結 UI 與 Addin，強制解耦：應用邏輯改 Command 狀態，Command 同步所有關聯的 UI（同一命令可掛在選單與 LinkLabel）。舊式事件處理的工具列與新式功能區（ribbon）不相容，需雙支援的 Addin 應避免獨立工具列。

| 成員 | 用途 |
|---|---|
| 建構子設 `Key` | UIC 檔以 Key 參照該命令 |
| `Execute()`／`Execute(ArrayList)` | 須覆寫；帶引數版依型別選多載 |
| `Checked`、`Enabled`、`Visible`、`List`、`SelectedIndex`、`Value`、`ValueChanged` | 與 UI 實體雙向同步 |
| `BeforeCommandExecute`、`CommandExecuted` | 可掛在**他人命令**上；前者設 `e.Cancel = true` 可取消執行 |

**其他服務。** `ResourceManager.LoadResourceFile("AttributeBrowserAddin")` 載入多語系資源組（找不到對應語系退回中性）；`<Module>Addins.xml` 與開發時以 `CAF_ADDINS_PATH` 指向副本的做法見[第 35 章 35.3.3 節](ch35_dotnet_zh-TW.reading.html)（[1147982]、[1147983]）。

**追蹤。** 設 `AVEVA_CAF_TRACING=PERFORMANCE`，主控台顯示各 Addin 啟動秒數；程式內可用 `PdmsTrace` 與 `TraceEntry`（後者須以 `using` 區塊確保 `Dispose()`，例外與多重 `return` 時才不會漏掉離開事件）。

**例外與執行緒。** 宿主只能妥善處理 `PdmsException` 與 `PMLNetException`；**其他例外逸出會使宿主不正常終止**，官方建議在每個進入點（如每個 `Command.Execute`）加 `try/catch` 當安全網（[1147986]）。宿主**非執行緒安全**，同時只能有一個執行緒呼叫 DbLayer 或 CAF（[1147987]）。實作 `IAddinTty` 的 Addin 可在 TTY 模式載入（[1147988]），官方以此示範偽屬性型 UDA。

### 39.6.4 選單與工具列客製：UIC 編輯器（[1147989]–[1147997]）

每個 CAF 模組有 `<Module Name>customization.xml`（例：Hull Design 的 `HullDesigncustomization.xml`），列出要載入的 UIC 檔：

```xml
<UICustomizationFiles>
  <CustomizationFile Name="Hull General" Path="AVEVA.Marine.UI.HullGeneral.uic" />
  <CustomizationFile Name="Hull Design" Path="AVEVA.Marine.UI.HullDesign.uic" />
  <CustomizationFile Name="Project" Path="$1.uic" />
</UICustomizationFiles>
```

出處：[1147990]（省略外層 `UICustomizationSet`）。**順序有意義**（後者可把工具放進前者定義的選單）。`$1` 代換為專案名稱、`CAF_UIC_PATH` 與 `AddUICustomizationFile` 的用法見[第 35 章 35.3.3 節](ch35_dotnet_zh-TW.reading.html)；官方補充一點：以 `AddUICustomizationFile` 載入的檔案**先於**設定檔載入，須自建選單或命令列。

編輯方式：在命令列區域彈出選單選 **Customize**，對話框有命令列預覽、作用中客製化檔案、樹、工具清單、屬性格、動作按鈕與資源編輯器。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Customize 對話框：1 命令列預覽、2 作用中客製化檔案、3 樹、4 工具清單、5 屬性格、6 動作按鈕

*圖 39-4　UIC 客製化對話框的主要區域。（AVEVA 官方文件截圖，僅供內部教學）*

| 區域 | 要點 |
|---|---|
| 作用中檔案 | 多個檔案**逐層疊加**；只能改作用中檔案內定義的項目，其餘灰色斜體；無寫入權限的檔案不在下拉清單，但內容仍顯示 |
| 工具清單 | 可把工具拖進樹中的選單或命令列，**含上層檔案（系統）定義者**，用來放進標準選單；上層結構日後變動會使工具「孤兒化」，故以**紅色**標示 |
> 〔公開版未收錄：AVEVA 官方產品截圖〕工具樹與清單：System、Project、User 三層檔案，使用者層的 Sweden 加進系統層的 Standard 命令列，以紅色標示

*圖 39-5　跨層加入的工具以紅色標示。（AVEVA 官方文件截圖，僅供內部教學）*

工具型別含 Button、ComboBox、ControlContainer（放 WinForms 控制項）、List（僅選單，如最近檔案）、StateButton、TextBox 等。**命令類型預設為 Macro**：執行**單一 PML 指令**，讓 PML 開發者不寫 C# 命令類別就能建立選單與按鈕；改選 Core Command 則從已載入的 CAF Command 挑選（[1147995]）。

資源編輯器可編輯字串、圖示與點陣圖資源集（含語言中性與各語系檔）；工具屬性以 `<資源集名稱>:<資源 ID>` 參照；新增圖示可拖放，ID 為檔名大寫加 `ID_`；另有獨立的 `ResourceEditor.exe`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕資源編輯器的字串頁：Resource ID 與 Value 兩欄，上方有存檔、複製、貼上、刪除與語系選擇

*圖 39-6　資源編輯器（字串頁，語言中性資源檔）。（AVEVA 官方文件截圖，僅供內部教學）*

### 39.6.5 資料庫介面（[1147998]–[1148033]）

第 35 章 35.4 只簡述，這裡補上官方的細節。

**資料模型類別。** `DbElementType` 與 `DbAttribute` 各以單一類別代表所有元素型別／屬性，具**值語意**。取得方式優先用全域實例 `DbElementTypeInstance`（如 `NOUN.EQUIPMENT`）與 `DbAttributeInstance`（如 `ATT.XLEN`，常以 `using ATT = Aveva.Pdms.Database.DbAttributeInstance;` 取別名，出處 [1148001]）。

UDET／UDA 要以名稱取得（`GetElementType`、`GetDbAttribute(":NAME")`，**名稱須含冒號**）。型別與屬性的 32 位元雜湊值可供外部系統唯一識別。

**DbElement 基礎（[1148005]–[1148007]）。**

- 取得：`DbElement.GetElement("/VESS1")`（名稱須含 `/`）。身分比對一律用 `DbElement`（值語意）；外部以「參照號＋型別」識別（如 `=123/4567`）。
- 元素可能**無效**（所在資料庫未開、已被刪除），用 `IsValid()` 檢查，無效時屬性存取與導覽都失敗。
- 錯誤風格有三種：丟 `PdmsException`、回傳 `false`、導覽失敗回傳「空元素」（以 `IsNull` 測試，參照為 `=0/0`）。
- 導覽：`Next()`、`Previous()`、`Owner()`、`FirstMember()`、`LastMember()`、`Next(NOUN.EQUIPMENT)`；大量掃描請用迭代器與過濾器。
- 讀屬性依型別區分，如 `myEle.GetDouble(ATT.XLEN)`（元素不是 BOX 會丟例外）；不確定時用 `GetValidDouble` 或 `IsAttributeValid()`。**偽屬性**（數百個，`PSATTS` 查詢可能很慢）以同樣方式查詢，限定詞用 `DbQualifier`：

```csharp
DbQualifier qual = new DbQualifier();
qual.Add(1);
double bore = myele.GetDouble(ATT.PPBO, qual);   // 出處 [1148007]：PPoint 1 的口徑
```

- `GetAsString()` 取得與命令列相同格式的字串；**沒有**通用的「從字串設屬性」方法。

> 〔公開版未收錄：AVEVA 官方產品截圖〕階層範例：Site1 下有 Zone1–Zone4，Zone2 下有 Pipe1–Pipe3 與 Equi1

*圖 39-7　官方導覽範例的階層：在 Zone2 時 `Next()` 為 Zone3、`Owner()` 為 Site1、`FirstMember()` 為 Pipe1。（AVEVA 官方文件截圖，僅供內部教學）*

**次要階層。** 標準導覽無法往下走次要階層，須查偽屬性 `SMEMB`（直接成員）或 `SEXPND`（遞迴展開）。官方範例：S1 含 A、C，S2 含 S1、D、G，則 S2 的 `SMEMB` 為 S1, D, G，`SEXPND` 為 A, C, D, G。

> 〔公開版未收錄：AVEVA 官方產品截圖〕主階層 SITE、ZONE、EQUI、BOX 與次要節點 S1、S2，次要節點以參照指向主階層元素

*圖 39-8　主階層與次要階層。（AVEVA 官方文件截圖，僅供內部教學）*

**修改管線（[1148008]）。** 支援設屬性、建立、刪除、複製、改型別、移動。官方強調一次看似簡單的設屬性實際經過下列步驟：檢查值型別→檢查有效值／範圍→值未變則返回→檢查系統 DB 的使用者存取控制→檢查資料庫以寫入模式開啟→檢查 `LOCK`→claim 檢查（implicit 模式自動 claim）→屬性專屬檢查→實際修改→加入變更清單→屬性專屬後續程式→更新受影響的動態規則。多數步驟可能出錯並丟 `PdmsException`，**呼叫端必須處理**。

| 操作 | 官方範例／要點 | 預檢方法 |
|---|---|---|
| 設屬性 | `ele.SetAttribute(ATT.DESC, "Example description");`（無帶限定詞版本） | `IsAttributeSetable` |
| 建立 | `myZoneElement.Create(1, NOUN.PIPE);` 建在指定位置，超出則在最後 | `IsCreatable` |
| 刪除 | `MyEle.Delete();` 刪主階層所有後代，**不刪次要階層** | `IsHierarchyDeleteable` |
| 複製 | `Copy(other)` 複製到既有元素（型別須同）；`CreateCopyHierarchyAfter(ele, copyoption)` 複製整個子階層；NAME 等不複製，階層內部參照自動更新、外部不變 | `IsCopyable` |
| 移動／改型別 | 可插入到指定元素前後或成員最後，**目前只能在同一資料庫內**（`IsInsertable`）；改型別時新型別無效的屬性**會遺失** | — |

**Claim。** implicit 資料庫修改時自動 claim，explicit 須先 claim，粒度是**主要元素**；大量 claim／release 用 `MDB` 類別的批次方法。可先用偽屬性 `MODATT`、`MODERR`、`DACMOD`、`DACCRE` 查「能不能改、錯誤文字」。`OKCLA`／`OKCLH` 的棄用註記見〔待核對〕。

**運算式與規則（[1148009]）。** 資料庫運算式就是 PML1 運算式，以 `DbExpression.Parse("DIAM OF PREV + 2")` 取得，用 `DbElement.Evaluate…` 求值；**結果一律以 mm 回傳**，運算式 `"10"` 無法判斷單位時須以 `DbAttributeUnit.DIST` 告知，距離單位為 inch 時解讀為 254 mm。跨工作階段比較沒有直接的 C# 方法，但可查偽屬性 `ATTMOD`、`ELECRE`／`ELEDEL`／`ELEMOD`、`LASTM`、`USERM`、`SESSNO`、`HIST`，是做「變更報告」Addin 的基礎（[1148010]）。

**迭代器與過濾器（[1148012]、[1148013]）。** `DBElementCollection` 搭配 `TypeFilter` 的基本寫法見[第 35 章 35.4 節](ch35_dotnet_zh-TW.reading.html)；官方補充這樣能避開不可能符合的子樹，並列出內建過濾器：`TypeFilter`、`AttributeTrueFilter`／`FalseFilter`、`AttributeRefFilter`、`AndFilter`、`OrFilter`、`BelowFilter`。

**Dabacon 表格（[1148015]、[1148016]）。** 索引屬性放在 key／value 表格，value 永遠是擁有該值的元素參照；key 為字串（`ntable`，唯一）、整數（`itable`）或參照（`ftable`，可重複）。**每個資料庫各有自己的表格**，找「誰參照了 X」要查 MDB 內每個已開啟的資料庫。C# 有 `NameTable`、`RefTable`、`IntTable`（單一 DB）與 `MdbNameTable`、`MdbIntTable`（跨 MDB；參照表順序無意義，沒有跨 MDB 迭代器）。

> **專業提醒：** 掃描 Dabacon 表格**一定要放在 `using` 區塊內**。搜尋 token 有限，掃到表尾會自動釋放，中途停止則靠 `Dispose`；沒釋放時命令列會出現「xx dabacon search tokens - Expected none」，直到資料庫關閉才停。

**MDB、DB 與事件（[1148018]–[1148025]）。** `MDB` 是單例類別（open／close、savework／quitwork、claim、抽取 flush／refresh／drop）；每個已開啟的 `DB` 有實例，可用偽屬性 `TYPEDB`、`NAMEDB`、`LPROT`（受保護）、`DBWRITE` 等查資訊。事件有三類：

- **變更捕捉：** `DbEvents.AddChangeEventHandler`，訂閱者收到 `DbUserChanges`（可查到屬性層級）。於 **PML 巨集結束、命令列指令執行後、表單動作完成後**觸發，且僅在確實有變更時。
- **DB／MDB 事件：** `CommitPending`、`ClearCache()`（官方警告單一操作可能呼叫數千次，**處理常式必須很快**）、getwork／undo／redo 與 savework／refresh／drop／flush 的前後事件、claim／release 事件。
- **偽屬性外掛：** 以 delegate 為 UDA 提供計算值（下例）。

```csharp
static private double VolumeCalculation(DbElement ele, DbAttribute att, int qualifier)
{
    return ele.GetDouble(ATT.XLEN) * ele.GetDouble(ATT.YLEN) * ele.GetDouble(ATT.ZLEN);
}
DbAttribute uda = DbAttribute.GetDbAttribute(":VOLUME");
Ps.GetDoubleDelegate dele = new Ps.GetDoubleDelegate(VolumeCalculation);
Ps.AddGetDoubleAttribute(uda, dele);   // 帶 DbElementType 參數則只對該型別生效
```

出處：[1148024]（已精簡）。啟動時註冊一次；可同時註冊多個，查找順序為「UDET＋屬性→基底型別＋屬性→僅屬性」；**事件不允許出錯**，算不出來應回傳合理預設值。

**單位（[1148026]–[1148033]）。** `DbDouble` 是帶單位的實數量（如 `DbDouble.Create("1 kg")`、`ConvertUnits(DbDoubleUnits.GetUnits(DbUnits.LB))`），支援 `+ - * / == != < <= > >=`，不同量綱相加會丟 `PdmsException`；口徑量用 `DbDouble.CreateBore(300)`，格式化用 `DbFormat`。

### 39.6.6 PMLNet（[1148034]–[1148038]）

官方 PMLNet 頁面的規則已併入第 35 章，此處只留圖與補充：

> 〔公開版未收錄：AVEVA 官方產品截圖〕PMLNet 使用示意：C# 與 Design／PMLNet 之間以實線呼叫、虛線事件雙向連結，外部 C# 與 Design 同一程序、同一資料庫工作階段

*圖 39-9　PMLNet 客製化：C# 無法直接呼叫 PML，只能透過事件（虛線）。（AVEVA 官方文件截圖，僅供內部教學）*

PML.NET 類別規則、`import`／`using namespace`、型別對應、事件與例外、`PmlNetControl` 嵌入，均已在[第 35 章 35.6 節](ch35_dotnet_zh-TW.reading.html)（35.6.1–35.6.5）講完，此處不重複。官方補充：Gadget 與資料庫元素是參照語意、其餘為值語意；找不到類別時的完整訊息為 `(46,87) PML: Object definition for NETOBJECT could not be found`；違反匯入規則時，錯誤寫入追蹤記錄且不建立類別定義。圖 39-9 的重點：C# 與 Design 在同一程序、同一資料庫工作階段，C# 只能透過事件（虛線）回呼 PML。

### 39.6.7 Grid Control、My Data 與 File Browser（[1148039]–[1148072]）

**AVEVA C# Grid Control。** 範例 `Samples\NetGridExample` 是一個 Addin，列出專案所有 Equipment 的 Name、Type、Owner，支援選取、排序、過濾、匯出 Excel、預覽列印。授權：官方說明**在自己的 Visual Studio 表單使用此控制項需 Infragistics 設計階段授權**，但執行該 Addin 不需要。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Grid Control 範例 Addin：停駐視窗顯示 17 筆設備，含 Export to Excel、Print Preview、第一列顏色與選取列數

*圖 39-10　NetGridExample 的 Addin 視窗（Total Items = 17，選取 3 列）。（AVEVA 官方文件截圖，僅供內部教學）*

資料來源有 `NetDataSource(TableName, Attributes, Items)`（資料庫元素）、`NetDataSource(TableName, columns, rows)`（非資料庫資料）與 `NetDataSource(TableName, PathName)`（直接讀 Excel，首列為標題）。選單以 UIC 編輯器建立 `NewAddin.SelectMenu`、`NewAddin.HeaderMenu` 兩個 Context Menu（命令 `AVEVA.DrawList.Add`、`AVEVA.Grid.ExportToExcel`），程式在 `UILoaded` 事件以 `RootTools[...]` 取出指定給 Grid。事件 `BeforeCellUpdate` 的陣列第 4 項設 `false` 可否決修改，`NetGridControl.DoDabaconCellUpdate(Array)` 可把儲存格修改寫回元素屬性；Grid 可編輯但**修改不會自動寫回資料庫**。於 Design 加入口是改 `PMLLIB\designormsppdesmain.pmlfrm`（**Marine 模組的對應表單需另查**）。

**AVEVA My Data（[1148049]–[1148071]）。** .NET Addin，把元素分組成「集合」並**跨模組保存**，API 也可由 PML 使用：`IMPORT 'MyDataAddin'`、`USING NAMESPACE 'Aveva.Pdms.Presentation.MyDataAddin'`、`!!mydata = object pmlmydata()`，再用 `addElement('/VESS1')`、`q var !!mydata.collections()` 等（出處 [1148049]、[1148053]、[1148070]）。方法含 `AddElement(s)`、`AddCollection(s)`、`RemoveElement(s)`、`Elements()`、`ElementsInCollection(name)`、`RenameCollection(old, new)`。

**PML File Browser（[1148072]）。** 以 PML 開啟標準 Windows 檔案對話框：

以 `import 'PMLFileBrowser'`、`using namespace 'Aveva.Pdms.Presentation'` 載入後，`!browser = object PMLFileBrowser('OPEN')`，再 `!browser.show('C:\','abc.DOC','My Browser',true,'Word Documents|*.DOC',1)`，以 `q var !browser.file()` 取得選取檔（出處 [1148072]）。

`show` 參數依序為 directory、seed（名稱欄預設）、title、exists（檢查檔案存在）、filter（「說明|副檔名」，可多組）、index；建構時指定 `OPEN` 或 `SAVE`（預設 OPEN）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕PML File Browser 開啟的 Windows 檔案對話框，檔案類型下拉顯示 Word 文件過濾器

*圖 39-11　PML File Browser 顯示的標準 Windows 開啟對話框。（AVEVA 官方文件截圖，僅供內部教學）*

## 39.7 Customizing Presentation of Ship Coordinates（船舶座標顯示客製）

頁面：[1112184]–[1112187]（全部讀過）。偽屬性 `SHIPX`、`SHIPY`、`SHIPZ` 可用船舶座標系呈現座標（例如肋骨位置）；此客製化進一步讓它顯示**離船上功能結構的距離**：

- X：到最近**橫向艙壁**的距離；
- Y：到最近**縱向艙壁**的距離，或離中心線（CL）的距離；
- Z：到最近**甲板**的距離。

### 39.7.1 設定步驟

1. **啟用（[1112185]）。** 所有 Marine 應用程式（含 Marine 環境中的 Isodraft 與 Spooler）可用，預設關閉。在命令列輸入 `SHIPCO ON`；也可寫進啟動巨集，例如 Isodraft 的 `%PDMSUI%\ISO\ADMIN\START`，或 Spooler 的 `%PDMSUI%\DES\ADMIN\START`。
2. **定義有效的功能結構（[1112186]）。** 參考面物件（Reference Surfaces，RSO）代表船上功能結構；以屬性 `RSDIM` 選擇哪些 RSO 可供距離計算，值為 `DIMX`（X 向，橫向艙壁）、`DIMY`（Y 向，縱向艙壁）、`DIMZ`（Z 向，甲板）。操作：把 `HRSO` 元素設為目前元素（CE），在命令列輸入：

```
RSDIM DIMZ
```

3. **輸出格式（[1112187]）。** 從通過量測點、平行於 `SHIPX`／`SHIPY`／`SHIPZ` 所指軸的直線，與 RSO 的交點起算距離，顯示為：

```
<RSO_name>(<X/Y/Z_position_of_RSO>) +/- <distance_from_RSO>
```

若啟用後找不到任何交點，或該方向沒有定義 RSO，則 X 與 Z 方向退回顯示 **FR／LP 位置**（肋骨／縱向位置），Y 方向顯示為離 CL 的距離。

### 39.7.2 實務建議

哪些艙壁與甲板的 `HRSO` 要設 `RSDIM` 屬於**基礎資料設定**，應由負責船體基準的人統一，避免各人設定不同造成輸出不一致；全公司一致時放在啟動巨集，命令列輸入的 `SHIPCO ON` 只影響當次工作階段。〔待核對〕官方沒有說明如何查詢 `SHIPX` 的輸出、`HRSO` 所在的資料庫與是否需要 claim。

## 39.8 常見錯誤

| # | 錯誤 | 後果與對策 |
|---|---|---|
| 1 | 直接修改標準 Appware 檔案 | 升級衝突；只改使用者區複製品並加公司前綴（39.5.2） |
| 2 | PML 檔存成 ANSI／Big5 且含非 ASCII | 他處讀不出來；改 UTF-8 with BOM 或純 ASCII（39.5.1） |
| 3 | 正式程式留 `onerror CONTINUE`／`PAUSE` | 錯誤被吞或卡住；正式程式用 `handle`（39.5.4） |
| 4 | 加密後沒保留原始碼 | 無法修改或重新加密（39.5.8） |
| 5 | 停駐視窗忘了 `SaveLayout = true`；`Command.Execute` 無 `try/catch` | 版面警告；非 Pdms 例外使宿主不正常終止（39.6.3） |
| 6 | 背景執行緒呼叫 DbLayer／CAF | 宿主非執行緒安全（39.6.3） |
| 7 | Dabacon 表格掃描未用 `using`；`ClearCache` 處理常式做重運算 | token 耗盡；單一操作觸發數千次而卡頓（39.6.5） |
| 9 | PML.NET 類別缺 `Assign()` 或預設建構子 | 匯入失敗，PML 報 `(46,87)`（39.6.6） |
| 10 | C 程式以過短輸出字串呼叫 DARs | 記憶體被覆寫且不會有錯誤碼 5（39.4.7） |

## 39.9 本章小結

1. 官方 Customization 是**查閱型**文件，用「需求→手冊」對照表查最有效；Customization Planning 是範圍**盤點表**。
2. DARs 是 FORTRAN 77／C 的**唯讀**常式庫；錯誤旗標會阻擋後續呼叫，`D3ERST` 只用於刻意製造的錯誤。
3. PML 在 12.1 全面 Unicode（含 BOM 的 UTF-8 或純 ASCII）；升級政策是「只改使用者區、加公司前綴」；PML Publisher 不可解密，原始碼自行保存。
4. .NET 客製化核心是 CAF 與資料庫介面；宿主非執行緒安全，非 Pdms 例外不可逸出；PMLNet 只能以事件回呼 PML。
5. 船舶座標顯示以 `SHIPCO ON`、`RSDIM`、`HRSO` 設定，找不到 RSO 時退回 FR／LP 或離 CL 距離。

## 39.10 練習題／自我檢核

1. 要寫一支「讀完專案所有 Equipment 的名稱與位置、輸出給外部分析軟體」的程式，主管要求「絕對不能寫入」。比較 DARs、PML、.NET 三條路線，各自如何滿足「不寫入」，你會選哪條，為什麼。
2. 以 39.4.4 的 Example 1 畫出呼叫順序流程圖，標出每步可能的錯誤碼（至少 108、110、113）與處理方式。
3. DARs 迴圈用 `D3MREL('NEXT','ELEM',ID3ERR)` 走訪成員，結束時得到 203。為什麼必須 `D3ERST`？不呼叫會怎樣？
4. 公司前綴是 `XYZ`，寫出新增表單／函式／全域變數的命名規範，並確認不與 39.5.2 的官方前綴衝突。
5. 寫一段 PML：以 `onerror GOLABEL` 導向標籤，用 `handle ANY` 印出 `!!Error.Text` 與呼叫堆疊，最後 `return error` 讓呼叫者處理。
6. 設計一個 Addin：停駐視窗顯示目前元素的屬性清單，並有選單按鈕控制顯示。列出 `IAddin`、`Command`、UIC、`<Module>Addins.xml` 各做什麼，並說明開發期如何用 `CAF_ADDINS_PATH`、`CAF_UIC_PATH` 避免改安裝目錄。
7. 為 UDA `:WEIGHT` 設計偽屬性外掛：`:MYELE`（UDET）、`SCTN` 與其他元素各用不同算法，說明註冊方式與查找順序。
8. 在 Hull Design 讓使用者看到「X 座標離最近橫向艙壁多遠」，寫出設定步驟並預測找不到 RSO 時的顯示。
9. 自我檢核：能否不查文件說出 (a) DARs 為何唯讀、(b) 修改管線有哪些檢查、(c) PMLNetCallable 類別的必要規則、(d) PML 檔的合法編碼。

## 39.11 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 39 章](appx_d_verification_zh-TW.reading.html#ch39)；取材覆蓋與未讀範圍：見[附錄 E 第 39 章](appx_e_coverage_zh-TW.reading.html#ch39)。
