# 第 40 章　管路等角圖：Isodraft

> 第 21 章談到管路設計的最後一步是 Spooling、Pipe Sketch 與 Isometric；第 9 章用一節介紹過 Isodraft 的概念。這一章把 **Isodraft（等角圖產生器）** 當成一個獨立的產品來看：它如何從資料庫「自動」算出一張帶尺寸、帶材料表、可以直接交給預製廠與現場的 ISO 圖，以及你要在哪裡動手腳，圖才會長成公司要的樣子。
>
> 最重要的一句話先說：**Isodraft 不是繪圖軟體，而是「資料庫 → 圖面」的轉換器。** 圖面好不好，七成取決於 Design、Catalogue（目錄）與 Spooling 的資料品質，三成取決於選項檔（Options file）。ISO 圖出錯時，先查模型與目錄，再查選項。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的 *Isodraft*（使用指南）與 *ISODRAFT Reference*（指令參考）兩大塊，共約 402 頁；實際讀過的範圍與未讀子樹列於 40.11。文件是 PDMS 時代的手冊，12.1 沿用，所以內文仍出現 PDMS、PARAGON、SPOOLER、COMPIPE 等舊名稱，本章照原樣保留。文件的指令語法（如 `DETAIL`、`ISOTYPE`、`MATERIALLIST`）有完整語法圖，可信度高；**但它不含 PML 程式範例或 .NET API**，因此「二次開發者怎麼接」一節只寫文件有依據的指令、屬性與檔案格式，其餘一律標〔待核對〕。官方機器翻譯的譯名生硬，本章改用台灣慣用說法。

## 40.1 學習目標

讀完本章，你應該能夠：

1. 說明 Isodraft 的輸入（Design、Catalogue、Fabrication 資料庫）、輸出（PLOT 檔、材料清單、各類報表）與它在管路出圖流程中的位置。
2. 區分四種 ISO 圖：合併式（Combined）、僅預製（Fabrication）、僅安裝（Erection）、Spool 圖，並指出各自的內容差異。
3. 用 GUI 與命令列兩種方式產生 ISO 圖，並說明 `CHECK` 與 `DETAIL` 的差別。
4. 說明選項檔（Options file）的三種存放區（Project／Company／Local）與主要選項類別。
5. 說明符號鍵（SKEY）、P-point、DTEXT／MTEXT 與 SHOP 旗標如何決定元件在圖上怎麼畫、列在材料表的哪一區。
6. 說明尺寸標註的三種型式（String、Composite、Overall）、歪斜與落差管線的表示法。
7. 設定材料清單、切管清單（Cut pipe list）、螺栓報表與損耗係數，並知道各報表檔如何輸出。
8. 說明輸出格式（PLOT、DXF、PDF、影像、EMF）與傳輸檔（Transfer file）的用途。
9. 說明 SPOOLER 產生的編號與 Isodraft 的關係，以及分頁、可重複性（Repeatability）、系統等角圖與設備組件（Equipment trim）。
10. 依錯誤訊息編號與常見症狀，判斷問題在模型、目錄還是選項。

## 40.2 Isodraft 在管路出圖流程的位置

### 40.2.1 它做什麼

官方定義：Isodraft 從 **Design 或 Fabrication 資料庫**，依你要求的標準，為管線與管網產生等角圖的繪圖檔，主要用於管路預製，也可用於現場安裝。它會一併產生你要求的材料清單（管路元件、螺栓、切管長度），資料取自專案的 **Design、Catalogue 與 Fabrication** 三種資料庫。

可處理的元素有 Zone、Pipe、Branch、Spool Drawing（SPLDRG）或混合；另外可畫**系統等角圖**（整個管網）與**設備組件圖**（Equipment trim）。

> 限制：**Design 與 Fabrication 的元素不能混在同一張圖**，即使是系統等角圖也一樣。

> 〔公開版未收錄：AVEVA 官方產品截圖〕標準 Isodraft 圖紙配置：左側材料清單、中央等角圖、右下角標題欄、左下切管清單與管線用途摘要

*圖 40-1　Isodraft 輸出圖紙的一般配置：左側材料清單、右上視角箭頭與等角圖區、底部為切管清單、管線摘要與標題欄。（AVEVA 官方文件截圖，僅供內部教學）*

### 40.2.2 與其他章節的分工

| 主題 | 在哪一章 | 本章做法 |
|---|---|---|
| 管路建模、Spooling、Production Checks | [第 21 章](ch21_pipework_zh-TW.reading.html) | 只引用結果（SPLDRG、焊口編號），不重講建立步驟 |
| 目錄、Spec、SPCOM | [第 8 章](ch08_catalogue_spec_zh-TW.reading.html) | 只講「Isodraft 要求目錄長什麼樣」 |
| 圖面與報表總覽、Isodraft 簡介 | [第 9 章](ch09_drawings_zh-TW.reading.html) | 本章深入選項、符號、材料表與輸出 |
| Draft 管理、2D 出圖、符號編輯 | [第 31 章](ch31_draft_admin_production_zh-TW.reading.html) | 自訂符號與詳圖（Detail plot）在 Draft 做，本章只講如何掛接 |

### 40.2.3 四種 ISO 圖

| 類型（`ISOTYPE`） | 內容 | 用途 |
|---|---|---|
| Combined（預設） | 完整尺寸與註記，材料清單含所有元件與螺栓，預製與安裝分區 | 一張圖兩用 |
| Fabrication | 少了工廠座標、安裝材料、「接至／續於」註記 | 預製廠 |
| Erection | 材料表除了鬆套法蘭（Loose flange），不含預製材料 | 現場 |
| Spool | 只含預製資訊，每個管段（Spool）一張；標題欄管線編號後附 `SPL[n]` | 管段預製 |

也可以讓圖面區留白、只出材料清單；`ISOTYPE NONE` 則完全不出圖，只出文字報表。

> **專業提醒：** 要正確配置 Spool 分界，**所有元件（含直管 Tube）的 SHOP 旗標都必須是 TRUE**。Tube 的預設是 FALSE，隱含的直管會被漏算而讓 Spool 尺寸錯誤。詳見 40.5.3。

## 40.3 如何產生 Iso 圖（工作流程）

### 40.3.1 整體流程

```
資料一致性檢查 ─► 選 ISO 類型與選項檔 ─► 選元素(CE 或 Detail List)
      │                                          │
      ▼                                          ▼
 修正 Design / Catalogue ◄── 讀訊息檔 ◄── CHECK / DETAIL ─► PLOT 檔 + 材料清單
                                                     │
                                       DXF / PDF / 影像 / 列印 / 報表檔
```

官方反覆強調：**在跑 Isodraft 前，先在 Design（或 INTREPID）對管線做資料一致性檢查（Data consistency check）**，批次模式尤其重要。許多 Isodraft 訊息其實來自設計或目錄錯誤，而不是操作錯誤。

> 〔公開版未收錄：AVEVA 官方產品截圖〕範例資料庫階層：World PIPING/AREA-A 之下有 Site、Zone、Pipe 與 Branch

*圖 40-2　官方命令列範例使用的資料庫階層：可從 Zone、Pipe 或 Branch 層級下 `DETAIL`。（AVEVA 官方文件截圖，僅供內部教學）*

### 40.3.2 GUI 操作步驟

啟動 Isodraft 的方式有兩種：啟動時選 Isodraft 模組，或從其他模組切換到 Isometric Generator (Isodraft)。進入後會看到 Application Window 與 Isodraft Explorer；要用命令列，從主選單 `Display > Command Window` 開啟 Isodraft Command Input & Output 視窗。

| 步驟 | 操作 | 說明 |
|---|---|---|
| 1 | `Isometrics > Standard` | 開啟 Standard Isometrics 表單；系統／設備組件圖則選 System/Trim |
| 2 | 在 Options 下拉選 Project、Company 或 Local，再點選項檔 | 官方附 BASIC.MET、ADVANCED.MET（公制）與 BASIC.IMP、ADVANCED.IMP（英制） |
| 3 | 在 Isodraft Explorer 或 Members 清單選 Pipe（Design）或 Spool Drawing（Fabrication），按 CE 按鈕 | 換了 CE 後必須再按一次 CE，否則處理的還是舊元素 |
| 4 | Detail 下拉選 Current Element 或 Detail List | Detail List 可跨區、跨資料庫一次處理多個元素 |
| 5 | Produce 下拉選 Isometrics、Transfer file、Batch macro 或 Bolt report | 輸出種類 |
| 6 | 按 Apply | 依選項檔指定的目錄建立 PLOT 檔；若啟用則同時建立材料清單檔 |

完成後會顯示 Display Isometric 視窗，並跳出 Isodraft Message 與 Display List 兩個表單（後者列出所有可用的圖）。若 CE 是 Zone、Group 或 ISOREG，會處理其下所屬的 Pipe 或 Spool Drawing。Detail List 只接受 Zone、Group、Pipe、Branch、ISOREG、Spool Drawing。

### 40.3.3 命令列操作

命令列流程固定：**設輸出檔 → 設訊息檔 → 設選項 → 組 Detail List → DETAIL**。沒有指定輸出裝置與訊息檔，任何管線都無法處理。

| 指令 | 作用 | 重點 |
|---|---|---|
| `FILE /ISOFILE SINGLE` | 指定輸出 PLOT 檔名 | 自動附 001、002…；每個 `DETAIL` 產生一個檔；`MULTIPLE 值` 可限制紙卷長度 |
| `MESSAGEFILENAME /ISOMESS` | 指定訊息檔 | 記錄已處理、被拒絕（含原因）的管線、警告與輸出檔名 |
| `ADD gid…` ／ `REMOVE gid…` | 組 Detail List | Add 與 Remove 清單各最多 100 筆；某管線在 Remove 出現過一次就不處理 |
| `CHECK` | 擷取資料但不出圖 | 用於批次前預檢，或只產生傳輸檔 |
| `DETAIL` | 處理並出圖 | `DETAIL CE`、`DETAIL ALL`、`DETAIL /PIPE1 /PIPE2` |
| `QUERY OPTIONS` ／ `Q 設定名` | 查詢目前選項 | 例如 `Q SIZE`、`Q WASTAGE` |
| `OPTIONS DEFAULT` | 全部選項還原預設 | 還原後需重設輸出裝置與訊息檔 |
| `RECREATE OPTIONS` ／ `RECREATE DETAILLIST` | 存成巨集檔 | 日後重新讀入還原 |
| `SAVEWORK` ／ `GETWORK` | 存檔／取得他人在 multi-write 模式下的變更 | 官方建議常用 SAVEWORK |

官方範例：

```
CHECK /PIPE-Y /PIPE-Z          -- 在 Design 先做一致性檢查
FILE /ISOFILE SINGLE           -- 兩管各一個檔：/ISOFILE001、/ISOFILE002
MESSAGEFILENAME /ISOMESS
QUERY OPTIONS
ADD /ZONE-1
REMOVE /PIPE-X
DETAIL ALL                     -- 或直接 DETAIL /PIPE-Y /PIPE-Z
```

`DETAIL` 與 `CHECK` 能處理的最低層級是 Branch（Design）或 Spool／Field（Fabrication）。Pipe 以上（Site、Zone、Group、GPWLD）會展開成所有 Pipe；元素中的 Equipment 與 Structure 一律忽略。單一指令最多 100 個元素識別碼。

### 40.3.4 `DETAIL` 的進階形式

| 寫法 | 效果 |
|---|---|
| `DETAIL CE AS 'System Name'` | 把相連的多條管線畫成一張**系統等角圖** |
| `DETAIL ... AS EQUIPMENT 文字` | 設備組件圖（見 40.8.4） |
| `DETAIL SHEETN 2 /PIPE-2` | 重畫某一張圖（需先用 Repeatability 存過分頁點） |
| `DETAIL SHEETN SING /PIPE2` | 強制單張圖 |
| `DETAIL PSPOOL2 OF PSLIST1 OF PIPE /…` | 畫單一 PSPOOL；PSPOOL／PSLIST 由 Design 的 Pipe Production Checks 建立 |

### 40.3.5 完成旗標：`MARK`

預設 Isodraft 處理完不改資料庫。`MARK DETAIL ON` 在成功後把各 Branch 的 `DETA` 屬性設為 TRUE；`MARK REVISION ON` 把 Pipe 的 `REV` 加一（顯示於標題欄 `ISS: n`，文字可由 ATEXT 254 改成 `REV: n`）。**Isodraft 不直接寫資料庫**，而是產生一個 inter-DB 巨集（放在專案的 XXXMAC 目錄），在模組切換或 `SAVEWORK` 時才建立，回 Design 執行後才生效。只要有一個 Branch 的 `DETA` 為 TRUE，該管線預設就不會再被處理，除非 `MARK IGNORE ON`。

> **常見錯誤：** 重畫時報「沒東西可畫」，其實是上次 `MARK DETAIL ON` 已把 `DETA` 設為 TRUE；或重畫後版次沒變，是因為 inter-DB 巨集還沒在 Design 執行。

## 40.4 選項檔與設定

### 40.4.1 選項檔是什麼

圖面上顯示什麼、怎麼顯示，**由選項檔決定**。選項檔本質上是一份巨集：每次產生 ISO 圖時被當成巨集執行。存放區：

| 存放區 | 內容 |
|---|---|
| Project | 目前專案的標準設定 |
| Company | 公司標準（官方附 BASIC／ADVANCED 的 .MET／.IMP） |
| Local | 目前目錄下的檔案 |

要建立或修改選項檔，必須是 **ISOADMIN 團隊**成員才看得到相關表單；使用 `Options > Modify`（建立用 Create）選檔後，進入各分類表單（如 Dimensioning Options、Annotation Options、Change Highlighting）。實務上，使用者選現成選項檔，管理員維護並以巨集批次出圖。

### 40.4.2 單位的陷阱

Isodraft 載入進入模組時的目前單位，但自己對孔徑與距離有一套單位，寫在選項檔中。重量、壓力、溫度的輸出單位則以目前單位解讀再轉換（例如壓力內部是 Pa，圖上要 bar，就必須在選項檔末端加上單位設定區塊）。修改選項檔時（`Options > Modify > Dimensioning > Other Unit Settings`，視窗 Current Session Units）會把目前單位附加進該選項檔。

| 注意事項 | 說明 |
|---|---|
| UDA 不做單位轉換 | 以資料庫單位直接輸出 |
| 輸入單位與輸出單位分開 | 輸入用 `BORES`、`DISTANCES`；輸出用 `UNITS` |
| 預設輸出 | 長度公制、孔徑英制（`UNITS METIMP`）；可改 `METRIC`、`IMPERIAL [FT] [BOMDEC]` |

### 40.4.3 選項類別總覽

指令參考共有約 120 個設定指令。依用途分類如下（括號內為文件所述預設或要點）：

| 類別 | 代表指令 | 要點 |
|---|---|---|
| 設定與流程 | `FILE`、`MESSAGEFILENAME`、`ADD`、`REMOVE`、`CHECK`、`DETAIL`、`OPTIONS`、`QUERY`、`RECREATE`、`INSTALL SETUP`、`MARK` | 40.3 |
| 圖紙版面 | `SIZE`（預設 A2）、`MARGIN`（預設 5 mm）、`RESERVE`、`FRAME`、`CUTMARKS`（預設 OFF）、`PLOTTINGSCALE`、`STACKINGARRANGEMENT`、`UNDERLAYPLOTNAME`（最多 8 個底圖） | 40.7 |
| 圖面文字 | `ATEXT`、`TITLEBLOCK`、`PROJECTNUMBER`、`DATE`、`POSITION`、`CHARHEIGHT`、`TTFONT` | 40.4.4 |
| 尺寸與座標 | `DIMENSIONS`、`DIMDIST`、`SUPPORTS`、`BENDRADIUS`、`TRUNCATE`、`COORDINATES`、`COFORMAT`、`COUNITS`、`AXES`、`ELEVATION`、`TOLERANCE` | 40.5.5 |
| 歪斜與落差 | `SKEWBOX`、`FALLINGLINES`、`FALLSKEWS`、`OVERALLSKEWS`、`ZEROLENGTHSKEWS` | 40.5.5 |
| 焊口、標籤 | `WELDTYPE`、`WELDNUMBERS`、`WELDID`、`TAGGING`、`ITEMCODE`、`OUTCOM`、`FLOWARROWS` | 40.5.4 |
| 材料與報表 | `MATERIALLIST`、`MATLISTFILENAME`、`CUTTINGLIST`、`CUTPIPELISTFILE`、`CLLENGTHFILE`、`SUPPORTFILENAME`、`BOLTING`、`BOLTREPORT`、`WASTAGE AREA`、`CUTBACK`、`LOOSEFLANGEALLOWANCE` | 40.6 |
| Spool 與分頁 | `ISOTYPE`、`SPOOLNUMBERS`、`SPLIT`、`REPEATABILITY`、`TUBESPLITS`、`CONTNOTES`、`CONTSHEETS`、`CONTWELDS` | 40.8 |
| 變更標示 | `CHANGE HIGHLIGHTING`、`SETCOMPDATE` | 40.4.5 |

### 40.4.4 替代文字（ATEXT）

圖上所有標準文字（材料清單標題、`CONN. TO`、`CONT. ON`、`BATCH REF`、`PIPING SPEC`…）都有唯一的 **ATEXT 編號**。`ATEXT 編號 '文字'` 取代標準字句；`ATEXT 編號 ''` 刪除；單打 `ATEXT 編號` 還原。可改的編號範圍為 201–500；文字只能用 A–Z、a–z、0–9、空白與 `+ - * . , [ ] ( ) : # ' = |`。範例：`ATEXT 15 'STRAIGHT TUBE'`、`ATEXT 410 ''`（刪除管線摘要註記）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Alternative Texts 表單，下拉選單選擇區域，下方列出編號與預設文字

*圖 40-3　Alternative Texts 表單：先選區域（如 Drawing Area），再選編號與編輯文字。座標標示的 E、N、EL 即 ATEXT 201–206。（AVEVA 官方文件截圖，僅供內部教學）*

官方將 ATEXT 分為九個區域：等角圖區、標題欄、繪製的材料清單、管線摘要區、列印的材料清單、焊口摘要、彎管表、動態詳圖區、螺栓報表。**做繁體中文化圖面時，ATEXT 是首選入口**，但要注意字元集限制（含中文的處理方式〔待核對〕）。

### 40.4.5 變更標示（Change Highlighting）

可把「自比較日期以來有變更」的項目用指定顏色畫出：

| 要素 | 說明 |
|---|---|
| 開關與顏色 | Change Highlighting 表單的 Show Change Highlighting 核取方塊與 Colour 按鈕 |
| 規則 | 以 Create／Delete／Clear 管理；For 選元件類型，With 加條件，如 `MODIFIED(POS)`、`CREATED()` |
| 比較日期 | `SETCOMPDATE`，可指定實際時間，或引用 **Stamp**（在 Admin 建立）；**未設定時會報錯並中止出圖** |
| 限制 | 沒有規則就不上色；選了 ALL 又沒條件則全部上色；**刪除的項目無法標示**；每次執行的選項必須相同；成組標籤（如 `F8 L9 G10 B11`）無法單獨標出哪個變了，螺栓與墊片只以標籤出現，需看材料表 |

## 40.5 符號與標註

### 40.5.1 Isodraft 對目錄的要求

Isodraft 的參考資料大多在 Catalogue DB：元件品項代碼與描述、每種元件的 2D 符號（SKEY）、特殊端部型式、法蘭螺栓需求。**目錄沒設好，Isodraft 就無法正確運作。**

元件描述拆成兩到三段：

> 〔公開版未收錄：AVEVA 官方產品截圖〕目錄階層 WORLD、CATA、SECT、CATE 下方的 DTEXT 與 MTEXT 元素及其屬性 RTEX、STEX、TTEX、SKEY、XTEX、YTEX、ZTEX

*圖 40-4　目錄中的描述文字：DTEXT（ADTE～SDTE）提供幾何描述與符號鍵，MTEXT（AMTE～SMTE）提供材質描述。（AVEVA 官方文件截圖，僅供內部教學）*

| 部分 | 來源 | 預設屬性 |
|---|---|---|
| 幾何描述 | DTEXT | `RTEX`（另有 `STEX`、`TTEX`，可用 `DTEXTS` 指令切換，例如做多語言） |
| 材質描述 | MTEXT | `XTEX`（另有 `YTEX`、`ZTEX`，用 `MTEXTS`） |
| 附加文字 | `ATTEXTS 運算式 ON 選擇規則` | 可用 UDA 或屬性運算式，附加在符合 GTYP 條件的元件描述後 |

最終描述 = RTEX + XTEX + ATTEXT。`DTEXT IGNORE`／`MTEXT IGNORE` 可整段略過。

> 〔公開版未收錄：AVEVA 官方產品截圖〕管路元件經由 SPREF 指向規格元件 SPCOM，再由 DETAIL 指向 DTEXT、MATXT 指向 MTEXT

*圖 40-5　元件與描述文字的關係：Pipe component 的 SPREF → SPCOM，DETAIL 指向 DTEXT（RTEX、SKEY），MATXT 指向 MTEXT（XTEX）。（AVEVA 官方文件截圖，僅供內部教學）*

### 40.5.2 符號鍵（SKEY）與 P-point

每種元件在圖上的 2D 符號由 DTEXT 的 **`SKEY`** 屬性（如 `SKEY 'KABW'`）指定。同一通用型別（GTYPE）可選多個鍵，例如 CAP 可用 KABW、KACP、KASC、KASW。**SKEY 錯誤時，圖上只會在元件位置畫一個預設矩形。** 標準符號庫涵蓋 CAP、CLOS、COUP、CROS、ELBO／BEND、FBLI、FILT、FLAN、FTUB、INST、LJSE、PCOM、REDU、SHU、TEE／OLET、TRAP、UNIO、VALV、VENT、VFWA、VTWA、WELD、樓板貫穿 ATTA 與焊接吊耳等；每個符號都標明所需的 P-point 配置，**目錄元件必須遵守**。

| P-point 規則 | 說明 |
|---|---|
| P0 | 自動設定，為元件原點 |
| 兩通元件 | 到達與離開為 P1、P2；兩通閥門的閥桿方向用 P3 |
| 三通元件 | 支路為 P3；三通閥閥桿用大於 P3 且孔徑未設的 P-point |
| 四通元件 | 兩個直通流向為 P1/P2、P3/P4；閥桿用大於 P4 的 P-point |
| 偏心異徑管 | 無接口：P3 指示平面側；有接口：P3 為接口、P9（孔徑未設）指示平面側 |
| U 型彎管（超過 135 度） | 依各符號圖示設定 |

**端部型式：** 預設每個 SKEY 有一種標準端部；可對 BEND、CROS、ELBO、FILT、FLAN、INST、OLET、PCOM、REDU、SHU、TEE、TRAP、VALV、VFWA、VTWA 個別設定。做法是在 Paragon 把 P-point（PTAXI、PTCAR、PTMIX）的 `PSKEY` 設為下表代碼；設為 NULL 即回到預設。

> 〔公開版未收錄：AVEVA 官方產品截圖〕六種端部型式與代碼：BW 對焊、CP 壓接、FL 法蘭、SC 螺紋、SW 承插焊、PL 平口

*圖 40-6　可表示的端部型式：BW（Butt Weld）、CP（Compression）、FL（Flanged）、SC（Screwed）、SW（Socket Weld）、PL（Plain）。（AVEVA 官方文件截圖，僅供內部教學）*

### 40.5.3 SHOP 旗標與材料表分區

Isodraft 以元件的 `SHOP` 旗標把材料表分成**預製（TRUE）**與**安裝（FALSE）**兩區；未設時預設 FALSE。常見做法是在 Spec 設 SHOP 欄，選用時自動帶入；個案以 `NEW FLAN SEL WITH SHOP FALS` 覆蓋。

| 情境 | 做法 |
|---|---|
| 一般慣例 | 螺栓、墊片、閥門等為安裝品；其餘為預製品 |
| 同一元件兩種 SHOP | Spec 建兩個 SPCOM，名稱只差**後綴分隔符號**（預設冒號），如 `*/FL100:T`、`*/FL100:F`；Isodraft 忽略後綴，材料表仍顯示同一品項代碼並合計 |
| 直管（Tube） | SHOP 取自 Spec；小口徑常設 FALSE、大口徑 TRUE，需兩條 TUBE SPCOM；選擇用 `SEL TUBE WITH SHOP FALS` |
| Spool 圖 | 直管必須 SHOP TRUE |

建議把小口徑的 FALSE 行排在前面、大口徑 TRUE 行排前面，避免預設選錯。

### 40.5.4 元件如何標註

官方「Piping Components in Isodraft」一章用圖例說明各元件的標註規則，歸納如下：

| 元件 | 圖上表示 |
|---|---|
| 一般直通元件、閥 | 方框內為材料表編號；旁有流向箭頭（可用 `FLOWARROWS` 關閉）；閥桿方向正確，歪斜者畫到最近的主方向並加註實際方向 |
| 閥門名稱 | 名稱存在 Design 時，`TAGGING` 開啟後顯示在編號方框下 |
| 法蘭 | 同組法蘭＋墊片＋螺栓編號一起標，例如 `F3 G8 B10` |
| 成對相同法蘭 | 兩個符號，編號只標一次，墊片與螺栓只算一組 |
| 夾式（Wafer）元件 | 兩片法蘭夾一個蝶閥或孔板，共用加長螺栓，兩個墊片 |
| 三通、OLET | 主管與支管口徑用訊息連到交叉點；補強式支管加 `REINFORCED` |
| 異徑管 | 顯示 `大 x 小 NS`；偏心者畫出平面側並標偏移量；`FLAT DOWN` 之類文字需用 ATEXT 另加 |
| 彎頭與彎管 | 對焊、承插焊、螺紋彎頭在兩側加記號；彎製管（Pulled bend）視為直管的一部分，長度沿中心線計入；非直角者標銳角度數 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕閥門符號：兩側法蘭、閥桿方向與材料表編號 3，下方標註 SPINDLE U 30.00 N

*圖 40-7　閥門標註範例：方框內為材料表編號，旁有流向箭頭，歪斜的閥桿以註記標明實際方向（SPINDLE U 30.00 N）。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕法蘭符號與標籤 F3 G8 B10：法蘭、墊片、螺栓編號並列

*圖 40-8　法蘭、墊片與螺栓以一組標籤標示。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕兩種三通符號：標註 6 X 3 NS 的對焊三通，與標註 6 X 1 NS 的 set-on 支管

*圖 40-9　三通與 set-on 支管：主管與支管口徑以訊息標示（6 X 3 NS、6 X 1 NS）。（AVEVA 官方文件截圖，僅供內部教學）*

**管端與接續：**

- 管線起點、離線 Branch 終點與管線終點會標座標（E/W、N/S、EL）。
- 連到其他管線的管端前綴 `CONT. ON`；接設備噴嘴為 `CONN. TO`；跨圖為 `CONT. ON`／`CONT. FROM` 加圖號。
- Branch 端 `OPEN`、`CLOS` 不另加文字，只標座標；要加訊息用 ATEXT。
- `COORDINATES` 控制何時標座標，可關閉噴嘴、續接管、OPEN／CLOS／VENT／DRAN 端；`COFORMAT` 可選 USER、ENU、XYZ、SHIP（船舶肋位坐標，如 `FR41-396`）、NUMBERS 五種格式。船舶專案要用肋位座標時，這是對應入口；實際可用性〔待核對〕。
- `CONTINUATIONSYMBOLS` 在合併式與安裝式 ISO 圖的設備連接處畫虛線噴嘴；`CONTNOTES` 與 `CONTWELDS` 加續接註記與臨時焊口編號。

**預設座標系為 World**；`AXES` 可改用任何有原點的元素（Site、Zone 等）的座標系。

> 〔公開版未收錄：AVEVA 官方產品截圖〕World、Site、Zone 三層座標軸，同一元件在三者下有不同的 E、N 值

*圖 40-10　各層級有自己的座標原點，同一元件在 World、Site、Zone 下座標不同；以 `AXES` 選擇圖上採用的座標系。（AVEVA 官方文件截圖，僅供內部教學）*

**現場補焊與鬆套法蘭：** 現場需加工，因此以訊息標在管端（如 `FFW`、`LEFT LOOSE`）。啟用切管清單（`CUTPIPELISTFILE`）時，Isodraft 會對屬性 `LOOSE` 為 TRUE 的法蘭，以及 SKEY 為 `WF` 的現場焊口，自動加上現場配合裕量：優先取該焊口或法蘭的 `ALLO` 屬性，沒設或為零則預設 **150 mm**，可用 `LOOSEFLANGEALLOWANCE` 改。Tube 中的現場焊口，裕量加在焊口前的直管；要加到後一段，需在 Design 把焊口翻轉使 P-arrive 為 P2。圖上顯示的仍是設計尺寸。

> 〔公開版未收錄：AVEVA 官方產品截圖〕現場補焊 FFW 與標註 229，以及鬆套法蘭 LEFT LOOSE 的標籤 F2 G3 B4

*圖 40-11　現場補焊（Field-fit Weld）與鬆套法蘭（Loose Flange）的標註。（AVEVA 官方文件截圖，僅供內部教學）*

### 40.5.5 尺寸、彎管、歪斜與落差

> 〔公開版未收錄：AVEVA 官方產品截圖〕三種尺寸標註：(a) String、(b) Composite、(c) Overall

*圖 40-12　尺寸標註方式：String（逐段）、Composite（合併直接相連的元件）、Overall（整段）。（AVEVA 官方文件截圖，僅供內部教學）*

| 型式 | 說明與預設 |
|---|---|
| String | 預設。從 Branch 起點、轉向點、元件接點（法蘭、焊口、螺紋、壓接，不含墊片）逐點量測；細節最多 |
| Composite | 忽略預製廠無法控制的單一元件尺寸，直接相連的非法蘭元件視為一個整體；法蘭仍是斷點；三通處一律斷開 |
| Overall | 起點到第一轉向、轉向到轉向、末轉向到終點、落差盒、Branch 接點之間；預設標示距離 16 mm |
| Critical | `DIME OVER CRIT`：量到關鍵元件，適用於採購交給當地廠商、元件尺寸尚未定的情況 |

常用寫法：`DIME OFF`（不標尺寸）、`DIME COMP ON`、`DIME OVER ON ACR`（跨 Branch 接點）、`DIME OVER CEN`（量到閥中心線）、`DIME DEFAULT`。預設是 String 開、Overall 關、支架尺寸開、閥中心線關。標示距離（Standout）預設 String／Composite 為 11 mm、Overall 為 16 mm、支架為 6 mm，三者不可設為同值（`DIMDIST`）。

標註的取整：所有尺寸四捨五入到 1 mm 或 1/16 吋，**預設把餘數帶到下一個尺寸**以減少累積誤差，代價是相同管件可能差 1 mm；要關閉用 `TRUNCATE`。彎製管預設標半徑（SKEY 以 PB 開頭），`BENDRADIUS` 可改為孔徑倍數、設標準半徑，或關閉。孔徑可選標稱或實際（`PRECISION BORES`）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕支架尺寸標示位置：(a) 預設與其他尺寸同側，(b) 支架尺寸置於相反側，含 6 mm、11 mm、16 mm 標示距離

*圖 40-13　支架尺寸可與 String 同側（預設）或置於相反側（`DIMENSIONS HANGERS`）；各線標示距離不同。（AVEVA 官方文件截圖，僅供內部教學）*

| 項目 | 規則 |
|---|---|
| 歪斜管（Skewed） | 以歪斜盒（Skewbox）表示，`SKEWBOX` 選完整盒或三角形，三角形可加剖面線（預設間距 3 mm）、擺動角、H／V 註記 |
| 落差管（Falling） | 落差小於限值（預設 5 度）時改用落差箭頭＋ `FALL` 與角度；`FALLINGLINES` 改限值 |
| 歪斜且落差 | 預設用 3D 歪斜盒；`FALLSKEWS` 可改成箭頭加單一 2D 盒 |
| 圖面易讀性 | `CHARHEIGHT`（註記字高；文件另有 `CHARSIZE` 寫法〔待核對〕）、`PICTURESCALE`（只縮放符號與註記對管長的比例，不縮放材料表）、`MESSAGEACCURACY`（引線搜尋精度 1～3 與迭代次數；先從 1 開始，高精度犧牲效能） |

**保溫與伴熱：** 管線的 `ISPEC`／`TSPEC` 有設時可在圖上標示；保溫起訖點可用 `INPP` 型 ATTA 標示；保溫規格註記標在起點，伴熱規格名稱標在標題欄。以 `INSULATIONCONTROL`、`TRACINGCONTROL` 控制只畫直管或含元件。

**規格變更：** 以箭頭訊息同時標出原規格與新規格，預設元件層級，`SPECBREAK` 可改 Branch 層級；同一點最多 10 項變更。

**焊口：** 符號代碼 `WS`（現場焊）、`WF`（現場配合焊）、`WW`（工廠焊）；`WELDTYPE` 可限只顯示工廠焊、現場焊、全不顯示或全部視為工廠焊。`WELDNUMBERS FROMDB` 取用 SPOOLER 產生的編號（若發現未編號焊口會顯示錯誤並**中止出圖**）；不用 SPOOLER 時 Isodraft 可自行編號，但**版次之間不保證維持**；附加焊口（AWELD）可用 `BALLOON 數量` 控制為個別圓框或合併橢圓。`DIMENSIONS OFF` 配 `WELDNUMBERS` 可產生無尺寸、有焊口編號的圖，用於記錄射線檢測結果。

**自訂標籤：** `OUTCOM` 把元件屬性與 UDA 以六種外框（含無框、空白手寫框）標在圖面。

### 40.5.6 自訂符號

標準符號庫的符號可在 Draft 或其他 2D 繪圖程式重新定義（建立方法見 [第 31 章](ch31_draft_admin_production_zh-TW.reading.html) 與 Draft 官方文件）。要點：

- 新符號必須衍生自「具所需特性」的既有符號；彎頭、彎管、三通、十字是以管段畫的，**不可重新定義**；儀表錶盤 IDFL、IDPL 不應重定義。
- 同時存在的自訂符號最多 **300** 個。
- 符號屬性（在 Draft 設定）：`SCale`（100 為原大）、`ORIentation`（NONE、FLOW、REDUcer、FLANge）、`FLWA`（流向箭頭）、`DIMEnsion`、`Fill`。ORI FLAN／REDU 的符號會自動依管線元件順序翻轉；ORI FLOW 依流向翻轉。
- 閥桿 SKEY：`SPINdle ON/OFF/skey`。若符號本無閥桿，可把軸向 P-point（PTAX）的 `PURP` 設為 `SPIN`。
- **通用符號 `UNIV`**：給 PCOM 的「幽靈」符號——一個圓（預設半徑 10 mm，`SKeyScale` 以百分比調整）加連到各接點的線；不表示實際幾何，需用詳圖或 Draft 圖補充；端部型式由各 P-point 的 `PSKEY` 設定（BW、CP、SW、FL、SC、PL，未設視為 PL）；接點旁輸出 P-point 編號（前綴為 ATEXT 388，預設 `P`，設空白則不輸出）。非標準品項多的專案（如食品、製藥）特別有用。

> 〔公開版未收錄：AVEVA 官方產品截圖〕12 種標準閥桿符號 01SP 至 13SP（缺 04SP）

*圖 40-14　官方提供的標準閥桿 SKEY，可用 `SPINDLE skey` 替換原閥桿形狀。（AVEVA 官方文件截圖，僅供內部教學）*

## 40.6 材料清單與報表

### 40.6.1 材料清單的結構

預設材料清單畫在圖紙**左側**，中等字高；合併圖中預製與安裝分開，每區依「管、管件與法蘭、墊片、螺栓、閥／管內元件、儀表、支架」分組。每筆有流水號（與圖面編號對應）、描述、公稱尺寸、品項代碼與數量。**每張分頁各有一份材料清單，流水號每頁從 1 重新開始**；溢出的行預設接在一張空白的「假」圖上。

`MATERIALLIST` 控制：是否畫出、單檔或每圖一檔、預製區是否依 Spool 排序、排除品項、位置、字大小（小／中／大）、行距、品項代碼欄寬（預設 8、最大 29 字元，不含開頭 `/`）、是否含描述、溢出處理、頁碼樣式、**是否加重量欄**與預製／安裝／合計重量。欄位可選標準欄（編號、描述、品項代碼、公稱尺寸、數量、備註）或其他元件／Spec 屬性與 UDA，重量欄找不到時顯示 `--`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Material List Column Definitions 視窗：欄位標題、Fill、From、Width

*圖 40-15　Material List Column Definitions 視窗：每欄可設定標題（兩行）、填入內容（如 BORE、PARTNUMBER、ITEMCODE）、來源與欄寬。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 此視窗預設載入 ATEXT 標題，但**編輯欄標題不會回寫 ATEXT**，而是存於選項檔的欄位定義；欄位留白會得到空白標題。

### 40.6.2 品項代碼與零件編號

| 主題 | 說明 |
|---|---|
| 預設品項代碼 | SPCOM 名稱去掉 Spec 名稱與開頭 `/`，如 `RF300/100CRMM` → `100CRMM` |
| 完整名稱 | `ITEMCODE LENGTH`；同時要加寬 `MATERIALLIST CODE` |
| 替代品項代碼 | 在 SPCOM 建 UDA（如 `:clienta`），以 `ITEMCODE` 指定來源；螺栓的 UDA 建在 DTAB；支架可取自 ATTA 自身屬性。**UDA 中分隔符號之後的文字會被截掉** |
| 後綴合計 | 名稱或 SPREF 不能重複，故以後綴區別；Isodraft 辨識分隔字元（預設 `:`）後移除並合計；`ITEMCODE SEPARATE` 讓描述不同者分列；`DELIMITER` 可改分隔符號 |
| 儀表 | 名稱併入描述（品項代碼欄留白），或以 `INSTNAME` 改用 SPREF；其他可標籤類型要用 `KEYS` 賦予鍵編號才視同儀表 |
| 零件編號 | `PARTNUMBERS FROMDB` 取用 SPOOLER 所定（跨版次保持）；`GENERATED` 由 Isodraft 產生（**不跨版次保持**） |
| 排除品項 | 用屬性 `MTOC`／`MTOT`（Branch 成員與離管）、`MTOH`（首段管）：`ON`、`OFF`（不列表但照畫）、`DOTD`（不列表、虛線並標尺寸）、`DOTU`（虛線不標） |
| 額外品項 | 元件的參考陣列 `MTOR` 最多指向 20 個額外 SPREF（如法蘭頂開螺絲、閥手輪鏈、試壓用盲板），長度或數量由 `MTOL`、`MTOQ` 設定，列於 Miscellaneous items |

### 40.6.3 螺栓

螺栓需求存於目錄：**Bolt Set（BTSE）**及其下的 Bolt Point（BLTP），與 **Bolt Table（BLTAB）**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕目錄中螺栓資料的階層：CATA 下 SECT、BTSE、BLTP；BLTAB 下 BLIST、SBOLT 與 LTAB、DTAB

*圖 40-16　螺栓資料的目錄階層：BTSE／BLTP 存螺栓孔與規格，BLTAB 下的 BLIST／SBOLT 與 LTAB／DTAB 存螺栓種類與可用長度。（AVEVA 官方文件截圖，僅供內部教學）*

| 元素／屬性 | 說明 |
|---|---|
| `BTSE`：`NOFF`、`BDIA`、`BTHK`、`BTYPE` | 標準螺栓孔數、直徑、通過法蘭的長度、螺栓類型 |
| `BLTP`：`NUMB`、`BDIA`、`BTHK`、`BTYPE` | 非標準孔、頂開螺栓（NUMB 為 0）；孔須沿螺栓圈依序編號，使兩個相同法蘭反轉後仍可對接 |
| 元件的 `BLRF` | 指向一個或多個 Bolt Set |
| `DTAB`：`BLEN` | 某直徑與材質可用的所有螺栓長度；Isodraft 計算後取 **大於等於需求** 的最小長度 |
| Spec 的 `BSPEC` | 螺栓規格；未設則取法蘭元件所在的管路規格 |
| 螺栓類型 `BTYP` | `MACH`（機械螺栓）、`STU`（雙頭螺栓）、`CAP`、`JACK`、`TAP`；`BOLT` 表示用 Spec DEFAULT 欄的預設型式 |
| 選擇規則 | 兩側皆 BOLT 取預設；一側 BOLT 另一側非 BOLT 取後者；兩側相同且非 BOLT 取該型；不同且皆非 BOLT 取起點側 |

供應商一併供應螺栓者（如孔板法蘭組），把 `BLTREF` 或 `CATREF` 設為空即不輸出該接頭的螺栓。螺栓的 SHOP 規則與直管相同（兩個 SPCOM 加後綴）。

`BOLTING` 控制長度顯示位置（預設：描述欄顯示、品項代碼尾端附加；`INSERT AT 'Here'` 可取代指定字串；`BOLTING OFF` 全關），並設定材料控制檔的單位旗標。`BOLTREPORT` 另出螺栓報表（ASCII，頁長可設；可附法蘭中心線座標），與 `DETAIL` 同樣掃描，但只報與螺栓有關的診斷，不要求整條管線幾何完全正確，**但連接關係必須正確**。螺栓長度的詳細計算（法蘭－墊片－法蘭、夾式、混合需求、噴嘴、額外螺帽墊圈）在官方指南的 Bolting 章，本章未逐頁細讀（見 40.11）。

### 40.6.4 切管清單與其他報表

| 報表 | 指令 | 內容與說明 |
|---|---|---|
| 切管清單（圖上） | `CUTTINGLIST ON`（預設 OFF） | 每段切管：尖括號切片編號 `<1>`、長度、孔徑、備註；可加品項代碼與端部加工（`PE` 平、`BE` 斜口、`TH` 螺紋、`SC`、`SA` 鞍口，皆為可改的 ATEXT）；`PERDRAWING` 讓編號每圖重排 |
| 切管報表檔 | `CUTPIPELISTFILE` | 品項代碼、描述、孔徑、切割長度、計算長度（不含端部加工裕量）、特殊需求、切片編號、批次參考（Zone 名） |
| 完整材料清單檔 | `MATLISTFILENAME` | 文字檔，每圖一檔或全部一檔；僅輸出檔時圖上仍有編號 |
| 支架明細 | `SUPPORTFILENAME` | **系統等角圖不寫入** |
| 管長摘要 | `CLLENGTHFILE` | 管中心線長度摘要，或含保溫；兩者擇一，不能同時產生 |
| 彎管表 | `POSITION BENDTABLE` | 彎管示意圖加長度、半徑、角度；可輸出 ASCII 供彎管機 |
| 焊口表／修訂表／系統表 | `POSITION WELDTABLE`／`REVISIONTABLE`／`SYSTEMTABLE` | 焊口表需 `WELDNUMBERS FROMDB`；修訂表只能用 UDA（最多 10 個版次）；系統表列管線屬性與 UDA |
| 詳圖（Detail plot） | `POSITION DETAILPLOTS` | 元件的 `DPFN` 指定詳圖 PLOT 檔，最多 20 個；用 `DPGRID` 的 3×3 格號定位時最多 9 個；手動與疊排不能混用；`PLOTDETAILDATA` 可附屬性值 |

**損耗與加工裕量：**

- `WASTAGE AREA n 係數`：全廠最多 10 個損耗區（0–9），區 0 固定為 1。Branch 的 `EREC` 屬性設區號（`EREC=10` 視為區 0，11 為區 1…）；Spec 直管的 `PWAS` 為百分比。官方例：管長 1000 mm、`PWAS`=10、區 3 係數 1.2，損耗為 1000 x 10% x 1.2 = 120 mm，圖上切管長 1120 mm。
- `CUTBACK`：確保彎管機與螺紋機有足夠夾持長度，不足就在切管長度加長，事後切除；規則逐條比對，**第一條成立者生效，順序很重要**；備註顯示 ATEXT 186（CUT START）、187（CUT END）。例：`CUTB 200 ON ALL BEND` 作為最後的收尾規則。

### 40.6.5 材料控制檔與 COMPIPE 介面

**Material Control File** 是 ASCII 檔，記錄圖中所有材料，供外部材料管制程式讀取；每筆記錄最多 14 個字、每字 5 位整數，依記錄編號區分直管（100）、管件（200）、法蘭（300）、墊片（400）、螺栓（500）、閥（600）、儀表（700）、支架（800）等。欄位格式為圖片，本章未逐欄整理。

**COMPIPE 介面**（輸出給 COMPIPE 模組）：`COMPIPEFile /前綴` 啟動，產生 `前綴.LINE001`（Linelist）與 `前綴.MTO001`（MTO）；`COMPIPEFile OFF` 關閉。選項可串接：`COMPIPE MTO DRWG|PIPE`、`ITEMcodes User|Client`、`DESCriptions Short|Long`、`SUPPorts ON|OFF`，預設為 `MTO DRWG ITEMcodes User DESCriptions Short SUPPorts ON`；MTO DRWG 要求材料表溢出選項不是預設的 DUMMY。管線需有 `CARE`（必填，4 字元）、`CNUM`、`CDRG` 等屬性，DTEXT 需有 `SCOD`（必填，3 字元；標準組件用 `SAN`）；缺短碼的元件會使整條管線不產生 COMPIPE 檔。限制包含含 `/` 的品項代碼、系統與 Spool 圖等。此介面是否仍用於你們的流程〔待核對〕。

## 40.7 輸出格式與繪圖

### 40.7.1 FILE 指令與輸出格式

`FILE` 同時指定 PLOT 檔名與其他格式。Isodraft 在檔名後自動加三位序號，並跳過已存在的號碼；DXF、PDF、影像、EMF 會再加 `.dxf`、`.pdf`、`.tif／.bmp／.jpg／.png／.dif`、`.emf`。

| 格式 | 語法與選項 |
|---|---|
| PLOT（原生） | `FILE /名稱 [SINGLE｜MULTIPLE [紙長 mm]]`；預設行為在官方文字中有兩種說法，以實測為準〔待核對〕 |
| DXF | `FILE DXF /名稱`；日文環境可加 `SHIFTJIS` 或 `EUC` |
| PDF | `FILE SET PDF [VIEW｜NOVIEW] [COMP｜NOCOMP] …`：是否自動以 Adobe Reader 開啟、壓縮 |
| 直接列印 | `FILE SET PRINT [NOFIT｜REDUCETOFIT｜EXPANDTOFIT｜ALLFIT] [DIALOG｜NODIALOG｜ONEDIALOG]` |
| 影像 | `FILE SET IMAGE [TIF｜TIFLZW｜TIFGFOUR｜JPG｜BMP｜GIF｜PNG] [REDUCE 0.01–0.99]` |
| EMF | `FILE SET EMF …` |
| 共通 | 色彩模式 `STANDARD`、`BW`、`GRAYSCALE`、`COLOURPLUS`（把近黑近白的灰全轉黑白，對比最大）；`MINLINEWIDTH 0.01–9.99 mm`；`BINDPAGES`（全部頁合成一檔）或 `NOBINDPAGES`（每頁一檔） |

範例：`FILE AND DXF PDF PRINT IMAGE EMF "plot" SINGLE` 一次輸出所有格式並列印；`FILE SET PDF Noview Nocomp Colourplus Bindpages`。查詢用 `Q OUTPUT`、`Q OUTPUT PDF` 等。**TrueType 字型只能用在 DXF、PDF、影像、EMF 輸出**（`TTFONT`）。文件提到 PDMS 的繪圖尺寸上限為「3275mm2」，單位表達疑有誤，原文照錄〔待核對〕。

多張圖排在同一紙卷用 `STACKINGARRANGEMENT`（單檔模式不可疊排）。底圖用 `UNDERLAYPLOTNAME`（最多 8 個；必須與 Isodraft 輸出圖紙尺寸相同），適合預印圖框；此時可用 `FRAME` 關掉自繪圖框。

### 40.7.2 圖紙版面

| 項目 | 指令與預設 |
|---|---|
| 紙張 | `SIZE A3`（ISO A0–A4）、`SIZE AA`（美規 A–E）、`SIZE H 300 W 400`；預設 A2 |
| 實際出圖尺寸 | 預設同設計尺寸；`PLOTTINGSCALE` 可更小 |
| 邊界與保留區 | `MARGIN`；`RESERVE` 在圖面區頂部／底部或材料表底部留空（供標準註記、預印資料、詳圖） |
| 剪裁記號 | `CUTMARKS`（預設 OFF） |
| 視角 | `ISO` 設北向箭頭位置：預設左上，可改右上、右下；`BOX` 在箭頭外加框 |
| 標題欄 | `TITLEBLOCK` 加行（最多 25 行，可用底線與直線畫框）；`PROJECTNUMBER`；`DATE`（預設英式，可改歐式、美式或關閉）；把文字用 `POSITION` 放到 0,0 可抑制 |
| 使用者定位文字 | `POSITION` 可定位北向箭頭、Spool 編號、頁碼、專案編號、彎管半徑、系統名稱、日期，並可加入最多 100 個管線屬性（含 UDA）；**不檢查位置，請放在邊界**；`POSITION 文字 OFF` 取消 |

### 40.7.3 傳輸檔與處理指令

Isodraft 先從 Design 與 Catalogue 處理資料，產生**中間資料檔（IDF，Transfer file）**，再由 ISODRAW 轉成 PLOT 檔。

| 指令 | 說明 |
|---|---|
| `TRANSFERFILENAME 檔名` | 另存 ASCII 傳輸檔；`OFF` 取消；預設傳輸檔 `/trans` 每次 `DETAIL`／`CHECK` 都會覆寫 |
| `PROCESS TRANSFERFILENAME 檔名` | 以傳輸檔直接產生 PLOT 檔，不再讀資料庫 |
| `PREPROCESS`、`POSTPROCESS` | 各可定義最多五個系統指令（以整數編號），在傳輸檔寫完之後、ISODRAW 呼叫前後執行 |

10.3 版以前的傳輸檔是二進位，無法用 `PROCESS` 處理。傳輸檔也是向 AVEVA 支援回報問題（PUR）時常用的附件。這給二次開發者一個「不碰資料庫就能重現或後處理」的切入點，見 40.9。

### 40.7.4 匯入 MicroStation

官方有一份 MicroStation/J 的建議：DXF 沒有顯式顏色，**以圖層名 `GT_n` 對應 Marine 顏色 n**，直接匯入會全白無法出圖；需在 `dwglevel.tbl` 加上 `GT_1`→層 1 等對照，並另行安裝字型。細節本章未細讀。

## 40.8 Spool 與 Isometric 圖

### 40.8.1 SPOOLER 與 Isodraft 的分工

SPOOLER 做的事（資料在 **Fabrication 資料庫**，交叉參照 Design）：定義獨立於 Pipe／Branch 階層的 Spool Drawing（SPLDRG）、互動加入 Spool 分界、建立焊口、彎製管、零件、Spool 與接頭編號。一個 SPLDRG 通常對應 Isodraft 的一張等角圖（可跨多頁），內含若干 Spool（預製組件）與 Field（安裝件）。SHOP 旗標變化處自動分出 Spool 與 Field；也可強制 Spool Break、加現場焊；`SFLimit`（BRAN、PIPE、ZONE、SITE、WORLD，預設 WORLD）則強制在指定層級的元素變更處分界。詳細建立步驟見 [第 21 章](ch21_pipework_zh-TW.reading.html)。

要把 SPOOLER 的編號畫到圖上，需開啟對應指令：

| 編號 | Isodraft 指令 |
|---|---|
| Spool | `SPOOLNUMBERS FROMDB` |
| 零件 | `MATERIALLIST PARTNUMBERS FROMDB` |
| 焊口 | `WELDNUMBERS FROMDB` |
| 接頭 | `JOINTNUMBERS ON` |
| 彎製管 | `PBENDNUMBERS ON` |

不用 `FROMDB` 而只開 `SPOOLNUMBERS ON`，則由 Isodraft 自行編號，從管線起點依序，遇三通先走離線再回主線，**編號不跨 session 保持**；Spool 編號以方括號標在首段（如 `[8]`）並列於材料表尾；`PERDRAWING` 每頁重排；`PREFIX` 可帶 Design 的 `SPLP` 屬性或使用者文字，並以 `*` 通配符插入圖號與 Spool 號。

### 40.8.2 附著點元素（ATTA）

Isodraft 利用 Design 中的 ATTA 標示支架位置、附註與流向，依 `ATTY` 屬性分類：

| ATTY | 用途 |
|---|---|
| 未設（Unset） | 預設的支架 ATTA，標在中心線上；在管內時顯示在前一元件的 P-leave 或 Branch 起點，可能使後續支架尺寸漏標 |
| `Hang`／`Weld` | Hangers & Supports 用；Weld 型以 P3 使符號畫在前一元件內固定距離處 |
| `CCCC` | 帶指引線的註記（例如樓板貫穿），未標尺寸處會補標 |
| `CCNN` | 同上，但不標尺寸（例如油漆顏色） |
| `FLOW` | 管中的流向箭頭；需 `FLOWARROWS INLINE` 才會繪出；比例對應 3D 位置 |
| `XXXX` | 一般等角圖的分頁點 |
| `SSSS` | 系統等角圖或設備組件圖的分頁點；一般 XXXX 在系統圖會被忽略 |
| `INPP` | 保溫起訖 |

檢查：Support ATTA 位置或方向不對時，一致性檢查會報錯，除非 `ATTACHECK OFF`。**不要把 ATTA 放在法蘭或帶法蘭元件之間**，否則可能破壞材料清單輸出。`ATTANAME` 決定是否顯示支架名稱與品項代碼來源。

### 40.8.3 分頁與可重複性

管線太長或太複雜時 Isodraft 自動分頁，圖號標 `DRG 1 OF …`，管端標 `CONT. ON`／`CONT. FROM`。

| 控制 | 說明 |
|---|---|
| `SPLIT 3 DRwgs`、`SPLIT 75 PERCENT` | 指定張數或複雜度係數（預設 100；大於 100 每張更複雜）；只有單一管線能指定固定張數 |
| Split ATTA（`XXXX`） | 使用者在 Design 指定分頁點時，Isodraft **一律採用，不自行計算** |
| `TUBESPLITS` | 管中分頁時可輸出 `UNACCEPTABLE SPLIT POINT` 訊息，或乾脆不出圖 |
| `REPEATABILITY ON` | 把自動分頁點寫回 Design（以 inter-DB 巨集建立 `XXXX` ATTA），設計變更後仍在同位置分頁，可只重畫受影響的頁 |

Repeatability 的限制：已有分頁 ATTA 時不再自動建立；**重排 Branch 會破壞資料完整性**；大改設計時應先清除（SPOOLER 有清除功能）再重建；不適用系統圖與設備組件圖。有此資料後，可把單頁或單一 Spool 加進 Detail List。

### 40.8.4 系統等角圖與設備組件圖

| 型式 | 要點 |
|---|---|
| 系統等角圖 | `DETAIL … AS '名稱'`；系統名稱畫在管線參考框；個別管線名稱與規格在變更處標示；材料表是整個系統的，**不會有各管線分項**；支架檔不寫入 |
| 設備組件圖 | `DETAIL … AS EQUIPMENT`；只含圖框、使用者定位文字與材料表，適合材料估算，圖形部分另以 Draft 底圖補上；建模時每個噴嘴（或相連的噴嘴群）一條 Pipe；材料表標題如 `NOZZLE REF - A`，編號預設每噴嘴重排，`EQUIPMENTNUMBERING` 可連續；**不能出切管清單**；分頁用 `SSSS` ATTA 放在兩組噴嘴之間 |

## 40.9 二次開發者怎麼接

官方 Isodraft 文件沒有 PML 函式庫或 .NET API，但它的設計本身提供了幾個可批次化、可擴充的接點。以下僅列文件有依據者。

| 接點 | 文件依據 | 用法 | 風險 |
|---|---|---|---|
| 選項檔（巨集） | 選項檔每次執行時當巨集執行；`RECREATE OPTIONS` 產生巨集 | 以程式產生或修改選項檔，依專案／客戶切換 | 選項檔內容由 GUI 維護最安全；直接改文字檔語法細節〔待核對〕 |
| 命令列批次 | `FILE`、`MESSAGEFILENAME`、`ADD`、`DETAIL ALL`、`RECREATE DETAILLIST` | 用巨集依管線清單批次出圖，事後解析訊息檔判斷成敗 | 單次指令最多 100 元素；訊息檔格式為文字，編號（33:xxx）可當解析依據 |
| 預檢 | `CHECK`、Design 一致性檢查 | 批次前先跑，失敗者不進 `DETAIL` | 一致性檢查指令在 Design 模組 |
| 傳輸檔 | `TRANSFERFILENAME`、`PROCESS`、`PREPROCESS`／`POSTPROCESS` | 擷取一次、後處理或重繪；在 ISODRAW 前後掛自訂系統指令 | 10.3 以前為二進位；格式文件未公開，不要自行解析〔待核對〕 |
| 輸出檔 | DXF／PDF／影像、材料清單檔、切管報表、螺栓報表、支架明細、管長摘要、Material Control File | 以檔案為介面餵 ERP／MTO／NC；Material Control File 有記錄編號與字寬可解析 | 材料清單檔與 PLOT 檔的欄位定位以實際輸出為準 |
| 資料來源屬性 | `SHOP`、`SPREF`、`DETA`、`REV`、`EREC`、`PWAS`、`MTOC`／`MTOT`／`MTOH`／`MTOR`、`ATTY`、`SFLimit`、`LOOSE`、`ALLO`、`DPFN` 等 | 在二次開發的檢查工具中，先驗證這些屬性是否齊備，再呼叫 Isodraft | 屬性名稱以文件為準；PML 的讀取語法見第 11、12 章 |

PML 巨集如何呼叫 Isodraft 指令、如何從 PML 取回 `QUERY` 結果、.NET 端是否有 Isodraft 專屬物件，官方 Isodraft 文件未說明〔待核對〕。另見[第 16 章](ch16_reports_integration_zh-TW.reading.html)。

> **專業提醒：** 與其寫工具去「修 Isodraft 的輸出」，不如寫工具在出圖**之前**檢查資料：SHOP 旗標、SKEY 與 P-point、焊口編號是否齊、ATTA 位置、Spec 中 Tube 的 SHOP 設定。官方已明說多數訊息來自設計或目錄錯誤。

## 40.10 疑難排解

Isodraft 自己產生的訊息編號以 **33** 開頭；內部繪圖模組 ISODRAW 的訊息以 **35** 開頭，多半是達到程式上限，請洽 AVEVA 支援。

| 症狀或訊息 | 可能原因 | 處理 |
|---|---|---|
| `(33:149) SYSTEM ERROR Unable to scan pipe network` | 設計不一致；或合法但 Isodraft 無法掃描的組態 | 跑一致性檢查、看 Branch 接點流向；常可將管線**拆成較多 Branch** 解決 |
| `(33:168) Cannot find FLANGE to match PPOINT n` | 閥或元件的 P-point 沒有配對的法蘭 | 檢查設計與目錄 P-point 設定 |
| `(33:155) The DETAIL list is empty` | Add 沒有項目，或被 Remove 全部抵銷 | 檢查 Add／Remove |
| `(33:156) PLOT FILE NAME/PREFIX or TERM have not been specified` | 未指定輸出檔 | 先下 `FILE` |
| 元件被畫成預設矩形 | SKEY 錯誤 | 修正 DTEXT 的 `SKEY` |
| 焊口編號導致中止出圖 | `WELDNUMBERS FROMDB` 遇到未編號焊口 | 回 SPOOLER 重新編號，或暫用 Isodraft 自行編號 |

> **常見錯誤清單：** (1) 沒做一致性檢查就批次出圖；(2) 換了 CE 沒按 CE 按鈕；(3) 目錄元件沒遵守 SKEY 的 P-point 配置；(4) 把 ATTA 放在兩片法蘭之間；(5) 把 Design 與 Fabrication 元素混在同一張系統圖。

## 40.11 取材覆蓋說明

- **整體：** Isodraft 子樹約 402 頁，本章實際讀過約 **225 頁**（含少量只略讀的頁面）。
- **完整讀過：** 使用指南的使用方式、GUI 與命令列、查詢與選項預設、目錄需求（描述文字、SKEY、P-point 端部、替代品項代碼、SHOP 旗標）、螺栓前半（儲存、BTSE、BLTAB、規格與選擇規則）、設計需求（SPOOLER、ATTA、額外品項）、管路元件標註、圖紙客製、材料清單、等角圖繪製、變更標示、符號基本原則與通用符號、傳輸檔。
- **指令參考只讀了約 45 頁：** Setting Up、`DETAIL`、`CHECK`、`FILE`、`OPTIONS`、`ISOTYPE`、`SPLIT`、`MARK`、`SIZE`、`TRANSFERFILENAME`、`PREPROCESS`／`POSTPROCESS`／`PROCESS`、`UNITS`、`MATERIALLIST`、`DIMENSIONS`、`CUTTINGLIST`、`SPOOLNUMBERS`、`ATEXT`、`OUTCOM`、`BOLTING`、`CUTBACK`、`WASTAGE AREA`、`WELDNUMBERS`、`SUPPORTS`、`FRAME`、`POSITION`、`COFORMAT`、`COIMPP`、`CONTSHEETS`、`REPEATABILITY`、`REMOVE`（部分）。
- **幾乎沒讀：** 其餘約 90 個指令頁（如 `ADD`、`BENDRADIUS`、`SKEWBOX`、`ITEMCODE`、`KEYS`、`TAPPING` 等，僅依使用指南描述轉述）；Symbol Keys 附錄約 30 頁；Alternative Texts 附錄的 ATEXT 編號清單；Error Messages 只讀前段；Material Control File 欄位圖；COMPIPE 的 Linelist／MTO 格式；DXF 轉 MicroStation 的字型細節。
- **使用指南未細讀：** 螺栓長度計算各小節（標準法蘭、夾式、混合、噴嘴、額外螺帽）、Reference Dimensions 的設定與錯誤、「多於四個接口的元件」、偏置與角度管件。
- **官方文件本身的疑點：** `FILE` 預設單檔或多檔說法不一；`PREPROCESS`／`POSTPROCESS` 兩頁敘述重複；`CHARHEIGHT` 與 `CHARSIZE` 名稱不一；「3275mm2」單位存疑。皆需實測。

## 40.12 本章小結

1. Isodraft 是資料庫到圖面的轉換器，輸入 Design、Catalogue、Fabrication，輸出 PLOT 檔、材料清單與各類報表；Design 與 Fabrication 不可混在同一張圖。
2. 流程固定：一致性檢查 → 選 ISO 類型與選項檔 → 選元素 → `CHECK`／`DETAIL` → 讀訊息檔。圖面差異主要由**選項檔**控制，維護者需為 ISOADMIN 成員。
3. 元件怎麼畫由目錄決定：SKEY、P-point、PSKEY 端部型式、DTEXT／MTEXT 描述、SHOP 旗標、BLTAB／BTSE 螺栓資料。目錄錯，圖就錯。
4. 材料清單、切管清單、螺栓報表、焊口表、彎管表等是同一次處理的不同輸出，用各自的指令開關與檔名設定。
5. Spool 圖依賴 SPOOLER 產生的編號與分界；`FROMDB` 才能讓編號跨版次保持；Repeatability 讓分頁位置穩定。
6. 二次開發最有價值的位置是出圖前的資料檢查、批次呼叫與訊息檔解析、以及輸出檔的下游整合。

## 40.13 練習題／自我檢核

1. 請說明 `CHECK` 與 `DETAIL` 的差別，以及什麼情況下你會先跑 `CHECK`。
2. 一份 ISO 圖的某個閥門被畫成預設矩形。依本章，你會依序檢查哪幾個地方？
3. 為什麼 Spool 圖要求直管的 SHOP 旗標為 TRUE？若 Spec 只有一條 SHOP FALSE 的 TUBE SPCOM，你要怎麼補？
4. 某管線的焊口編號用 `WELDNUMBERS FROMDB` 時中止出圖，可能原因為何？退而求其次有什麼做法，代價是什麼？
5. 比較 String、Composite、Overall 三種尺寸；若採購由當地廠商負責、元件尺寸尚未定，建議哪一種？
6. 某管線的切管長度為何比量得的距離多 120 mm？請用損耗區 `EREC`、`PWAS` 與係數說明計算方式。
7. 設計變更後重畫圖，分頁位置跟舊圖不同。請說明原因與預防做法，並指出 Repeatability 的限制。
8. 設計一支批次出圖巨集的流程（只寫步驟，不寫程式）：從管線清單到訊息檔檢查，要用到哪些指令與哪些檢查？

## 40.14 〔待核對〕項目彙整

| 編號 | 項目 | 待確認內容 |
|---|---|---|
| 1 | 模組名稱與入口 | 文件沿用 PDMS 名稱；Marine 12.1 實際的模組切換、選單名稱（Isometrics > Standard 等）需在訓練專案確認 |
| 2 | ATEXT 與中文 | 官方限定字元集不含中文；中文標題欄、字型（`TTFONT`）與 DXF/PDF 輸出的實測 |
| 3 | `COFORMAT SHIP` | 船舶肋位座標格式的實際可用性與設定 |
| 4 | `FILE` 預設模式 | 單檔或多檔的預設值；3275 的單位 |
| 5 | `CHARHEIGHT`／`CHARSIZE` | 兩個寫法哪個在 12.1 有效 |
| 6 | 選項檔文字語法 | 直接編輯選項檔的語法細節 |
| 7 | PML／.NET 呼叫 | 如何從 PML 呼叫 Isodraft 指令、取回 `QUERY` 結果；有無 .NET 物件 |
| 8 | 傳輸檔格式 | 官方未公開格式 |
| 9 | COMPIPE | 是否仍用於你們流程 |
| 10 | `PREPROCESS`／`POSTPROCESS` | 兩頁敘述重複，實際差異與執行時機 |
| 11 | 螺栓長度計算與 Reference Dimension | 本章未細讀，需補讀 |
| 12 | Symbol Keys 附錄與 ATEXT 編號 | 各 SKEY 與 P-point 圖、ATEXT 完整編號表未讀 |
