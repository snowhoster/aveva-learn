# 附錄 C　參考文獻導讀與繁中摘要

> 本附錄是[附錄 A](appx_a_resources_zh-TW.reading.html) 的「深入閱讀版」。附錄 A 告訴你哪裡有資料；本附錄用繁體中文說明每份資料**在講什麼、能補哪一章、閱讀時要注意什麼**。
>
> 原文多為英文、韓文或簡體中文。以下是**摘要與導讀，不是全文翻譯**；數字、指令與專有名詞仍以原文與公司安裝版本為準。查核日期：2026-11-02。

## C.1 使用方式與標記

同樣一份資料，三種讀法：

1. **補概念**：先讀 C.3（官方手冊）與 C.4 的「一句話」與「繁中摘要」，建立骨架。
2. **找做法**：看 C.4、C.6 的「可借鏡的做法」，再回到原文確認語法與參數。
3. **找說法**：簡報或提案需要引用時，用 C.8 的格式回到原始出處，不引用本附錄的轉述。

本附錄的可信度分級沿用附錄 A：**A 官方、B 學術、C 社群**。另外用下列標記說明查核程度：

| 標記 | 意思 | 使用建議 |
|---|---|---|
| 〔已核對〕 | 本次已開啟頁面或取得完整書目資料 | 可直接引用 |
| 〔摘要依題名〕 | 只取得題名、摘要或公開片段，未讀全文 | 引用前先讀原文 |
| 〔待公司確認〕 | 與 Marine 12.x 版本、授權或安裝內容有關 | 向 IT／AVEVA 確認 |

> **版權提醒：** 本附錄只做摘要與連結，不重製原文圖表或長段文字。官方手冊與論文圖表的授權不同，轉貼前請看附錄 A.8。

## C.2 官方文件的三個世代

AVEVA 的文件常讓人混淆，因為同一套技術有三個世代的入口。先分清楚，再決定查哪裡。

| 世代 | 入口 | 優點 | 限制 | 建議用途 |
|---|---|---|---|---|
| **Marine 12.1** | [docs.aveva.com/bundle/hull-and-outfitting](https://docs.aveva.com/bundle/hull-and-outfitting/page/1224159.html) | 版本最接近公司系統；有 Marine 專屬模組與版本說明 | 頁面需要 JavaScript，無法直接抓取或離線全文檢索 | 查 Marine 專屬功能、畫面、SP 變更 |
| **E3D 2.1** | [help.aveva.com/AVEVA_Everything3D/2.1](https://help.aveva.com/AVEVA_Everything3D/2.1/NCUG/NCUG3.04.3.html) | 靜態頁可直接開啟；本課程既有連結多用此版 | 版本較舊，部分 API 與 12.1 不同 | 對照本課程既有章節 |
| **E3D 3.1** | [help.aveva.com/AVEVA_Everything3D/3.1](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG_FP.html) | 靜態頁；手冊最完整、目錄最清楚 | 部分 API、命名與 Marine 12.x 有差異 | 學語法、架構與資料模型 |

**判讀原則：** 語法與架構看 3.1；Marine 專屬功能與畫面看 12.1；兩者衝突時，以公司安裝版本為準。這是本課程一貫的作法，也是[第 31 章](ch31_dev_environment_zh-TW.reading.html)所說的「版本敏感」。

## C.3 官方手冊導讀（E3D 3.1）

E3D 3.1 的優點是每一本手冊都有穩定的靜態目錄頁，適合當成「查得到、可書籤」的參考書。目前可靜態存取的共有七本（PMLPUG、NCUG、DMRM、CSUG、ISOUG、DBRM、SCRM），以下只挑與本課程最相關的主題頁。

### C.3.1 PML Customisation（PMLPUG）

**一句話：** PML 與 PML2 的官方語言手冊，從變數、物件、陣列、錯誤處理，一路講到表單、選單與 PML Add-in。

入口：[PML Customisation](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG_FP.html)

| 主題 | 官方頁面 | 繁中重點 | 對應章節 |
|---|---|---|---|
| 物件模型 | [Variables, Objects, Functions and Methods](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG3.03.01.html) | 變數、物件、函式與方法是同一套型別系統的四種用法；先懂物件，再寫方法 | 第 32 章 |
| IF 判斷 | [IF Construct](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG6.06.02.html) | `if / elseif / else / endif` 的完整語法與巢狀寫法 | 第 32 章 |
| 陣列 | [Arrays](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG7.07.01.html) | 起始索引為 1、陣列方法、多維陣列；與其他語言的差異要先記住 | 第 32 章 |
| 錯誤處理 | [Errors and Error Handling](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG11.11.1.html) | `handle / elsehandle / endhandle`、錯誤碼與 `!!error` 的關係 | 第 32、40 章 |
| 檔案處理 | [Handling Files and Directories](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG12.12.1.html) | `FILE` 物件、開檔模式、逐行讀寫、檔案錯誤處理 | 第 38 章 |
| 追蹤除錯 | [PML Tracing](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG13.13.06.html) | `$R`、alpha log、診斷訊息的官方說明 | 第 40 章 |
| 表單入門 | [Form Concepts: Getting Started](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG14.14.1.html) | 表單、gadget、成員與載入流程的最小範例 | 第 34 章 |
| 回呼 | [Form and Gadget Callbacks](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG15.15.01.html) | 字串回呼、方法回呼、open callback 與事件時機 | 第 34 章 |
| 版面 | [Form Layout](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG18.18.01.html) | `path`、`at`、`anchor`、`dock` 的定位與自動調整 | 第 34 章 |
| 選單 | [Menus](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG17.19.01.html) | bar menu、popup menu、toggle menu 與動態選單 | 第 34 章 |
| PML Add-in | [PML Add-ins](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG24.27.01.html) | 定義檔、UIC、PowerWheel 與完整範例 | 第 34 章 |

**閱讀建議：** 不要從第一頁線性讀完。建議順序是 3.03（物件模型）→ 6、7（控制與陣列）→ 11（錯誤）→ 12（檔案）→ 14–15（表單與回呼）→ 18（版面）→ 24（Add-in）。每一段都開一個小範例在訓練專案跑一次，比讀十頁有效。

### C.3.2 .NET Customisation（NCUG）

**一句話：** 用 C# 寫 CAF Add-in、呼叫資料庫 API、把 .NET 控制項嵌進 PML 表單的官方指南。

入口：[.NET Customisation](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG_FP.html)

| 主題 | 官方頁面 | 繁中重點 | 對應章節 |
|---|---|---|---|
| 整體架構 | [.NET Customisation Architecture](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG1.02.02.html) | CAF、共用介面與 Add-in 的載入關係 | 第 35 章 |
| IAddin | [The IAddin Interface](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG2.03.02.html) | `Start()`、`Stop()` 與初始化順序；例外被吞掉的常見原因 | 第 35 章 |
| 環境變數 | [Environment Variables for .NET Customisation](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG3.04.3.html) | `CAF_ADDINS_PATH`、`CAF_UIC_PATH`、Addins.xml 的搜尋規則 | 第 35 章 |
| 資料庫介面 | [Database Interface](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG4.05.01.html) | `DbElement`、`DbAttribute`、`DbAttributeInstance` 的關係 | 第 35 章 |
| 元素存取 | [Element Access](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG4.05.07.html) | 取得目前元素、依名稱或參照找元素 | 第 35 章 |
| 讀取屬性 | [Getting Attribute Values](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG4.05.09.html) | 屬性值的型別轉換與單位 | 第 35 章 |
| PML.NET | [Using PML.NET](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG5.07.3.html) | `import`、`using namespace`、`Assign`、事件與例外 | 第 35 章 |
| Grid 控制項 | [Create a C# Addin which Contains an AVEVA Grid Control](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG6.08.02.html) | 官方表格控制項的完整範例 | 第 34、35 章 |

**閱讀建議：** 先看 1.02.02 建立架構感，再看 2.03.02 與 3.04.3 把一個最小 Add-in 跑起來，最後才看 4.05 與 5.07.3 處理資料。

### C.3.3 Data Model（DMRM）

**一句話：** 元素型別與屬性的字典；寫查詢、寫工具、猜屬性名稱時的第一站。

入口：[Data Model](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM_FP.html)

| 元素 | 官方頁面 | 用途 | 對應章節 |
|---|---|---|---|
| `HBLWLD` | [Hull Block World Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.339.html) | 船體區塊世界的根 | 第 4、9 章 |
| `HPANEL` | [Planar Panel Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.406.html) | 平面板架 | 第 4、9 章 |
| `HPLATE` | [Planar Panel Plate Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.408.html) | 板架中的板 | 第 9 章 |
| `HSTIFF` | [Planar Panel Stiffener Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.419.html) | 板架中的加強材 | 第 9 章 |
| `CHOLE` | [Shell Hole Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.263.html) | 外板開孔 | 第 9、17、41 章 |
| `CPANEL` | [Curved Panel Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.265.html) | 曲面板架 | 第 9 章 |
| `CPLATE` | [Shell Plate Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.268.html) | 外板板片 | 第 9 章 |
| `CSTIFF` | [Shell Stiffener Element](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.280.html) | 外板縱骨 | 第 9 章 |

> 〔待公司確認〕3.1 與 2.1 的 `HPANEL`、`HSTIFF` 頁碼相同，但 3.1 可能新增屬性。實際可用的屬性仍以公司安裝版本的 `Dictionary.chm` 或 `Q ATT` 輸出為準。

### C.3.4 Catalogues and Specifications（CSUG）

**一句話：** 目錄（CATA／SECT／CATE／SCOM）與等級（SPEC／SELE／SPCO）的操作與資料結構。

入口：[Catalogues and Specifications](https://help.aveva.com/AVEVA_Everything3D/3.1/CSUG/CSUG_FP.html)

| 主題 | 官方頁面 | 繁中重點 | 對應章節 |
|---|---|---|---|
| 階層 | [Hierarchy](https://help.aveva.com/AVEVA_Everything3D/3.1/CSUG/CSUG3.03.03.html) | 目錄與等級的樹狀結構 | 第 25 章 |
| 結構目錄 | [Structures](https://help.aveva.com/AVEVA_Everything3D/3.1/CSUG/CSUG11.10.01.html) | 型鋼與結構件的目錄組織 | 第 25 章 |
| 型鋼 | [Profile](https://help.aveva.com/AVEVA_Everything3D/3.1/CSUG/CSUG11.10.03.html) | 型鋼參數與幾何 | 第 25 章 |
| 參數 | [Understanding Parameters](https://help.aveva.com/AVEVA_Everything3D/3.1/CSUG/CSUG11.10.08.html) | 參數如何驅動元件幾何 | 第 25 章 |

### C.3.5 ISODRAFT（ISOUG）

**一句話：** 管路 ISO 圖的產生、標註、材料表與圖框設定的官方手冊。

入口：[ISODRAFT](https://help.aveva.com/AVEVA_Everything3D/3.1/ISOUG/ISOUG_FP.html)

| 主題 | 官方頁面 | 繁中重點 | 對應章節 |
|---|---|---|---|
| ISO 類型 | [Types of Isometrics](https://help.aveva.com/AVEVA_Everything3D/3.1/ISOUG/ISOUG3.03.03.html) | 系統圖、管段圖、spool 圖的差異 | 第 27 章 |
| 出圖指令 | [Isometric Detailing Commands](https://help.aveva.com/AVEVA_Everything3D/3.1/ISOUG/ISOUG3.03.25.html) | 批次出圖與指令列用法 | 第 27 章 |
| 材料表 | [Material List and Other Reports](https://help.aveva.com/AVEVA_Everything3D/3.1/ISOUG/ISOUG9.09.01.html) | 材料表、管段表與欄位設定 | 第 27 章 |

### C.3.6 Database Management Reference Manual（DBRM）

**一句話：** 資料庫層的參考手冊，定義屬性型別、查詢屬性、偽屬性與相對定位；寫 `Q ATT`、`Q POS WRT` 或批次查詢前，先來這裡確認語意。

入口：[Database Management Reference Manual](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM_FP.html)

| 主題 | 官方頁面 | 繁中重點 | 對應章節 |
|---|---|---|---|
| 屬性 | [Attributes](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM3.04.01.html) | 屬性型別、陣列屬性、單位與儲存方式 | 第 4、33 章 |
| 查詢屬性 | [Query Attributes](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM3.04.09.html) | `Q ATT`、`ATTLIS`、`ATTOUT`、`UDALIS`、`PSATTS` 的用途與輸出格式 | 第 4、38 章 |
| 偽屬性 | [Pseudo Attributes](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM1.02.17.html) | 不在資料庫中、即時計算的屬性（位置、方向、長度等） | 第 4、5、33 章 |
| 相對定位 | [Relative Positions, Directions, Orientations](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM3.04.14.html) | `Q POS WRT` 的參考座標、方向與姿態 | 第 5 章 |

**閱讀建議：** 先讀「Pseudo Attributes」與「Query Attributes」，再回頭查「Attributes」的型別表。寫查詢前先確認三件事：屬性是否存在、是不是偽屬性、單位是什麼。

> 〔待公司確認〕3.1 與 2.1 的 DBRM 頁碼大致相同，但 3.1 可能新增屬性；實際可用屬性仍以公司安裝版本的 `Dictionary.chm` 或 `Q ATT` 輸出為準。

### C.3.7 Software Customisation Reference Manual（SCRM）

**一句話：** PML 物件與指令的「字典」：每個物件的成員、方法、參數與傳回值，寫程式卡住時查這裡，比在論壇猜答案快。

入口：[Software Customisation Reference Manual](https://help.aveva.com/AVEVA_Everything3D/3.1/SCRM/SCRM_FP.html)

| 主題 | 官方頁面 | 繁中重點 | 對應章節 |
|---|---|---|---|
| FILE 物件 | [FILE Object](https://help.aveva.com/AVEVA_Everything3D/3.1/SCRM/SCRM3.3.37.html) | 開檔、讀寫、關閉、錯誤處理；`openfile` 的各種模式 | 第 32、38 章 |
| WRT | [WRT (AVEVA E3D Only)](https://help.aveva.com/AVEVA_Everything3D/3.1/SCRM/SCRM6.5.18.html) | 相對座標查詢與轉換，和 `Q POS WRT` 對應 | 第 5、32 章 |

**閱讀建議：** SCRM 很大，不要線性讀。先從你手上的物件名稱查起（例如 `!!file`、`!!ce`、`!!gadget`），再看方法的參數與回傳值；查完立刻在訓練專案跑一次。

**注意：** SCRM 標題含「Software Customisation」，但內容不限於 UI；PML 的內建物件與指令多半都在這裡。3.1 與 Marine 12.x 的物件成員可能不同，編譯或執行失敗時先比對版本。

## C.4 論文與技術文獻導讀

以下文獻與本課程最直接相關，包含期刊論文、會議簡報、專利與產業標準。每篇都附上「可以借鏡的做法」與「不要照抄的地方」；專利與簡報不是同儕審查文獻，會另外標示。

### C.4.1 Son, Kang & Kim (2014)：用 Scheme 重用船體區塊模型

| 項目 | 內容 |
|---|---|
| 原文標題 | AVEVA Marine Scheme-based Modeling for Reuse of Ship Hull Block Model |
| 作者 | Myeong-Jo Son、Hyungwoo Kang、Tae-Wan Kim |
| 出處 | Transactions of the Society of CAD/CAM Engineers（2014-03） |
| DOI | [10.7315/cadcam.2014.041](https://doi.org/10.7315/cadcam.2014.041) |
| 可信度 | B〔已核對書目；摘要依題名與公開摘要〕 |
| 語言 | 韓文（英文題名與摘要） |
| 對應章節 | [第 9 章](ch09_hull_modelling_zh-TW.reading.html)、[第 15 章](ch15_hull_production_zh-TW.reading.html) |

**一句話：** 把船體區塊的建模過程視為可分析的 Scheme 檔，開發複製與再利用相似區塊的程式。

**繁中摘要：**

- AVEVA Marine 的 3D 模型可以用 Scheme 檔描述；Scheme 不是黑箱，而是可解析的建模敘述。
- 作者分析 Scheme 檔的結構，找出區塊層級的模型定義與可參數化的部分。
- 在此基礎上開發區塊複製程式，讓相似船型或相似區塊不必從零建模。
- 這種做法把「模型」與「建模規則」分開，和本課程第 9 章強調的拓撲參考、第 15 章的重用觀念一致。

**可以借鏡：** 如果你的工具要做「類似區塊快速複製」，先研究 Scheme 的結構，而不是直接複製元素樹。前者可參數化，後者容易產生孤兒參考。

**不要照抄：** 論文是 2014 年、針對當時版本的 Scheme 格式；公司版本的 Scheme 語法與可用屬性可能不同，必須先在訓練專案驗證。

### C.4.2 Cheon 等 (2013)：AVEVA Marine 管模型轉到 SmartMarine3D

| 項目 | 內容 |
|---|---|
| 原文標題 | A Method for Translating Pipe Models from Aveva Marine to SmartMarine3D |
| 作者 | Sanguk Cheon、Jae-Jun Lee、Min-Cheol Cho、Kwang Lee |
| 出處 | Transactions of the Society of CAD/CAM Engineers（2013-10） |
| DOI | [10.7315/cadcam.2013.329](https://doi.org/10.7315/cadcam.2013.329) |
| 可信度 | B〔已核對書目；摘要依題名〕 |
| 語言 | 韓文（英文題名） |
| 對應章節 | [第 17 章](ch17_outfitting_zh-TW.reading.html)、[第 38 章](ch38_reports_integration_zh-TW.reading.html) |

**一句話：** 兩套船舶 CAD 之間的管模型轉換，重點在管件階層、幾何與屬性的對應，而不是單純匯出中立格式。

**繁中摘要：**

- 不同 CAD 對「管線—管段—管件」的階層與命名不同，轉換時必須先建立對應表。
- 幾何可以靠中立格式交換，但設計屬性（等級、材質、流向、保溫）通常會遺失，需要另外映射。
- 轉換後要做一致性檢查：管徑、中心線、連接關係、材料表。

**可以借鏡：** 第 38 章談外部系統整合時，先做「資料字典對照表」，再做轉換程式；不要期待通用格式能保留所有工程語意。

**不要照抄：** 論文對象是 SmartMarine3D，不是你的 ERP／PDM；對應表要依公司欄位重新建立。

### C.4.3 Kim, Park & Yang (2020)：用 AVEVA Marine 自動產生外板開孔

| 項目 | 內容 |
|---|---|
| 原文標題 | Development of an automatic shell plate hole generation system using AVEVA Marine |
| 作者 | Chang-Su Kim、Dong-Woo Park、Young-Jun Yang |
| 出處 | Journal of Advanced Marine Engineering and Technology 44(3), 196–202（2020-06） |
| DOI | [10.5916/jamet.2020.44.3.196](https://doi.org/10.5916/jamet.2020.44.3.196) |
| 授權 | CC BY-NC 3.0（非商業用途） |
| 可信度 | B〔已核對書目；本課程第 41 章已引用其畫面〕 |
| 語言 | 英文 |
| 對應章節 | [第 17 章](ch17_outfitting_zh-TW.reading.html)、[第 36 章](ch36_hull_vitesse_zh-TW.reading.html)、[第 41 章](ch41_case_studies_zh-TW.reading.html) |

**一句話：** 把「依管路與設備位置在外板開孔」這件事，從人工量測變成可重複執行的 PML 流程。

**繁中摘要：**

- 系統先從 AVEVA Marine 模型取得外板與相關構件資訊，找出需要開孔的位置。
- 以 PML 計算開孔中心、方向與大小，建立 virtual hole，必要時再轉成實際開孔。
- 流程包含前置檢查、開孔建立、結果輸出與例外處理。
- 論文附有實機畫面與程式片段，適合對照本課程第 41 章的案例。

**可以借鏡：** 開孔這類「跨專業介面」的自動化，價值不只在省時間，更在於把規則寫死、減少漏開與錯開。設計時要先定義「什麼情況不自動處理」。

**不要照抄：** 開孔規則與公司船體標準、管路等級有關；論文中的門檻值只能當範例。

### C.4.4 Han 等 (2021)：AVEVA Marine 與 Smart 3D 的結構資料轉換

| 項目 | 內容 |
|---|---|
| 原文標題 | A study on structural CAD data conversion between AVEVA MARINE® and Intergraph Smart 3D® |
| 作者 | Young-Soo Han、KyungHo Lee、JungMin Lee、JaeJun Lee、ByeongWook Nam |
| 出處 | Ships and Offshore Structures（2021-11） |
| DOI | [10.1080/17445302.2021.1998852](https://doi.org/10.1080/17445302.2021.1998852) |
| 可信度 | B〔已核對書目；摘要依題名〕 |
| 語言 | 英文 |
| 對應章節 | [第 9 章](ch09_hull_modelling_zh-TW.reading.html)、[第 38 章](ch38_reports_integration_zh-TW.reading.html) |

**一句話：** 船體結構資料在兩套 CAD 之間轉換時，真正難的是階層、板與型材的屬性對應。

**繁中摘要：**

- 結構模型的轉換不是「匯出 STEP 就好」；板、型材、開孔、邊界與參考關係都要有對應規則。
- 作者比較兩套系統的結構資料模型，建立轉換方法並討論資料遺失與驗證。
- 這類研究對「船廠換 CAD」或「與設計公司交換模型」特別有用。

**可以借鏡：** 轉換前先盤點「一定要保留」的欄位（材料、厚度、等級、開孔），其餘欄位可重建。這比追求 100% 轉換務實。

### C.4.5 Li 等 (2024)：船體區塊吊裝的整合設計系統

| 項目 | 內容 |
|---|---|
| 原文標題 | Development of multi-functional integrated design system for ship block lifting process |
| 作者 | Rui Li、Quanyou Zhang、Xiuguang Zhan、Julin Shan、Hexin Wan |
| 出處 | International Journal of Naval Architecture and Ocean Engineering 16, 100593（2024） |
| DOI | [10.1016/j.ijnaoe.2024.100593](https://doi.org/10.1016/j.ijnaoe.2024.100593) |
| 授權 | CC BY-NC-ND 4.0 |
| 可信度 | B〔已核對書目〕 |
| 語言 | 英文 |
| 對應章節 | [第 15 章](ch15_hull_production_zh-TW.reading.html)、[第 38 章](ch38_reports_integration_zh-TW.reading.html) |

**一句話：** 從 AVEVA Marine 模型抽取區塊資料，建立含吊點、吊索、強度與流程資訊的吊裝設計系統。

**繁中摘要：**

- 系統從 AM 模型取出區塊的幾何與屬性資料，避免人工重 key。
- 把吊裝流程資訊（吊點位置、吊索配置、工況）與模型資料結合，形成可計算的設計資料。
- 後續可做強度檢核、吊裝模擬與報表輸出。
- 這是「模型 → 生產資訊 → 專業計算」的典型資料流，和第 15 章說的衍生資料觀念一致。

**可以借鏡：** 把專業計算需要的輸入欄位，反推回模型端定義 UDA 或命名規則；不要讓下游每次都用 Excel 補資料。

### C.4.6 Kunkera 等 (2022)：造船專案中的數位孿生

| 項目 | 內容 |
|---|---|
| 原文標題 | Using Digital Twin in a Shipbuilding Project |
| 作者 | Zoran Kunkera、Tihomir Opetuk、Neven Hadžić、Nataša Tošanović |
| 出處 | Applied Sciences 12(24), 12721（2022-12） |
| DOI | [10.3390/app122412721](https://doi.org/10.3390/app122412721) |
| 授權 | CC BY（開放取用） |
| 可信度 | B〔已核對書目〕 |
| 語言 | 英文 |
| 對應章節 | [第 2 章](ch02_architecture_zh-TW.reading.html)、[第 38 章](ch38_reports_integration_zh-TW.reading.html) |

**一句話：** 用一個造船專案說明數位孿生要整合哪些資料、牽涉哪些角色，以及為什麼「有模型」不等於「有數位孿生」。

**繁中摘要：**

- 數位孿生不是把 3D 模型搬上網，而是設計、生產、營運資料的持續同步。
- 文章整理造船專案的資料來源與整合需求，並討論導入時的組織與流程問題。
- 對開發人員的啟示：工具要能被整合，介面與資料格式比功能多寡更重要。

**可以借鏡：** 別把「數位孿生」當成單一專案；先從一條可閉環的資料流（例如開孔申請 → 模型 → 生產）做起。

### C.4.7 Li 等 (2024)：把 AM 匯出的船體 XML 轉成有限元素模型

| 項目 | 內容 |
|---|---|
| 原文標題 | Ship hull model data processing algorithm for fast FEM modeling |
| 作者 | Rui Li、Mingfa Wang、Zhaochuang Meng、Guolei Liu、Yongtian Qiu（大連理工大學、大連船舶重工） |
| 出處 | Chinese Journal of Ship Research（中國艦船研究）19(5), 49–56（2024-10） |
| DOI | [10.19693/j.issn.1673-3185.03660](https://doi.org/10.19693/j.issn.1673-3185.03660) |
| 授權 | 開放取用（期刊網站標示；轉載前仍請確認） |
| 可信度 | B〔已核對書目與英文摘要〕 |
| 語言 | 中文（英文摘要） |
| 對應章節 | [第 15 章](ch15_hull_production_zh-TW.reading.html)、[第 38 章](ch38_reports_integration_zh-TW.reading.html)、[第 41 章](ch41_case_studies_zh-TW.reading.html) |

**一句話：** 設計軟體匯出的船體幾何不能直接拿去做有限元素分析；論文用 XML 當中介，先把模型「簡化」成分析模型。

**繁中摘要：**

- 問題：AVEVA Marine 匯出的船體幾何模型，與有限元素建模規範之間有落差，手工重建很耗時。
- 方法：解析 AM 匯出的 XML，先確認幾何資料的表達規則，再依 FEM 規範自動處理。
- 處理內容：刪除或簡化開孔、缺口等局部特徵；轉換球扁鋼與肘板；移動型材與板縫。
- 結果：處理後的模型可直接匯入 HyperMesh，並保留材質、板架厚度等屬性；論文指出效率明顯優於手工建模。

**可以借鏡：** 這是「設計模型 → 分析模型」的典型資料轉換。若公司要做 FEM 前處理，先把 XML 的欄位、單位與座標系固定下來，再寫特徵簡化規則；不要讓工程師每次手工刪特徵。

**不要照抄：** 特徵簡化規則與網格品質要求因公司和船型而異；論文的方法可以當骨架，門檻值要重新訂。

### C.4.8 Yang 等 (2022)：K-SUPPORT 資料驅動的管支架設計自動化

| 項目 | 內容 |
|---|---|
| 原文標題 | Data-centric Piping Support Design Automation (K-SUPPORT) |
| 作者 | Seung-sam Yang（KEPCO E&C）、Youngho Lee、Sanghwi Lee（LEEBRIDGE） |
| 出處 | AVEVA World Conference 2022（2022-11-17，舊金山） |
| 連結 | [簡報 PDF](https://cdn.osisoft.com/osi/presentations/2022-AVEVA-San-Francisco/UC22NA-03EE10-KEPCO-Yang-Data-centric-piping-support.pdf) |
| 可信度 | B〔已核對簡報全文；會議簡報，未經同儕審查〕 |
| 語言 | 英文 |
| 對應章節 | [第 17 章](ch17_outfitting_zh-TW.reading.html)、[第 27 章](ch27_drawings_zh-TW.reading.html)、[第 38 章](ch38_reports_integration_zh-TW.reading.html)、[第 41 章](ch41_case_studies_zh-TW.reading.html) |

**一句話：** 在 E3D 裡把「管支架選型、建模、出圖、BOM」串成一條資料流，用 PML 與內建目錄處理十二萬個支架。

**繁中摘要：**

- 背景：核電廠 1、2 號機約有 12.1 萬個管支架（大口徑 3.2 萬、小口徑 8.9 萬），人工建模與出圖無法負荷。
- 目錄：內建 LISEGA、SEONGHWA、UNISON HKR 等廠商的支架 3D 目錄，並標準化產品資料。
- 建模：以 PML 查詢管路模型的管徑、位置、荷重與位移，依容許荷重自動選型，再用樣板產生支架與預埋板。
- 出圖與報表：批次產生 2D 設計圖、BOM 與計算書所需資料，並與公司資料庫、Excel 交換。
- 擴充：新增支架型式時，主要改一份 PML 原始碼與 UIC，必要時加 CATA／SPEC 與樣板。
- 成效：簡報自述處理速度約為 E3D 原生管支架功能的 10 倍；這是廠商自述，並非獨立量測。

**可以借鏡：** 先做「邏輯支架」與一致性檢查，再生成實體模型。這樣管路變更時可以重算，而不是重畫；BOM 與圖面也不會和模型脫節。

**不要照抄：** 核電廠的荷重規範、支架目錄與船廠不同；簡報的倍數與數量是特定專案情境。

### C.4.9 專利文獻：PML 自動化的兩種典型

專利不是學術論文，但常比論文更完整地描述「步驟怎麼做」。以下兩件與本課程直接相關；專利狀態不代表技術可用性或授權狀態。

| 專利 | 主題 | 申請人／發明人 | 公開日 | 狀態 | 對應章節 |
|---|---|---|---|---|---|
| [CN104537150A](https://patents.google.com/patent/CN104537150A/zh) | 在 PDMS 中統計管支架材料 | 劉偉、楊少林、徐杰、李萌 | 2015-04-22 | 申請視為撤回（公開文獻仍可讀） | 第 17、27、38 章 |
| [CN122133263A](https://patents.google.com/patent/CN122133263A/zh) | 以自然語言與向量資料庫生成 PML 模型語句 | 高威、倪慧、鄒振山、徐舟（中遠海運重工揚州） | 2026-06-02 | 申請中 | 第 32、34 章 |

**CN104537150A 的重點：** 用 PML 建立管線清單 → 抓出每個支架的型材與管卡 → 依規格排序、加總型材長度與管卡數量 → 用 `openfile` 的 `overw` 模式輸出 CSV。專利自述：5000 米管線的支架材料統計可由一個月縮到一天。對第 38 章的報表自動化，這是一個完整的最小可行範例。

**CN122133263A 的重點：** 把 AM 匯出的 PML 語句放進向量資料庫（FAISS／ChromaDB、Sentence-Transformers、INT8 量化），用自然語言指令檢索相似語句、調整參數，最後產生可執行的 PML。這是 2026 年的新方向（LLM／RAG 輔助建模），但目前只有專利申請，沒有公開的準確率或生產驗證；課堂上適合當「趨勢觀察」，不建議直接導入生產。

**使用提醒：** 專利公開內容可以引用與討論，但不要直接把說明書裡的程式碼貼進公司系統；仍需確認授權、資安與版本相容性。

### C.4.10 產業標準：ISO 10303-242（STEP AP242）

| 項目 | 內容 |
|---|---|
| 標準 | ISO 10303-242:2022《Industrial automation systems and integration — Product data representation and exchange — Part 242: Managed model-based 3D engineering》 |
| 連結 | [ISO 官方摘要頁](https://www.iso.org/standard/84667.html) |
| 可信度 | B〔已核對官方書目；條文需付費〕 |
| 語言 | 英文 |
| 對應章節 | [第 38 章](ch38_reports_integration_zh-TW.reading.html) |

**一句話：** 跨 CAD 交換 3D 模型、組立與 PMI 的國際標準；對方說「給我們 STEP 檔」時，先問是不是 AP242。

**繁中摘要：**

- STEP 不是單一格式，而是一系列應用協定（Application Protocol, AP）。AP242 整併了航太的 AP203 與汽車的 AP214。
- 它支援幾何、組立結構、產品製造資訊（PMI）、材質與長期歸檔，是目前 PLM 互通與存檔常用的協定。
- 它規定「資料怎麼表達」，不規定「公司欄位怎麼對應」；所以匯出後仍要做語意對照與驗證。
- 管路等級、塗裝、焊道、製造屬性等工程語意，通常無法只靠 AP242 完整帶過去。

**可以借鏡：** 在介面規格書寫明「STEP AP242、單位、座標系、PMI 與組立需求」，比只寫「STEP 檔」清楚；驗收時用固定案例比對，不要只看檔案能不能開。

**注意：** ISO 條文需付費取得；本課程只連到官方摘要頁，不轉載條文。

## C.5 學位論文與技術報告

### C.5.1 船體結構特徵在 CAD 之間的資料轉移（LUT 碩士論文）

| 項目 | 內容 |
|---|---|
| 原文標題 | 3D model data transfer of ship hull structure features between CAD programs |
| 作者／年份 | 〔待核對〕 |
| 出處 | LUT University 公開典藏（LUTPub） |
| 連結 | [PDF](https://lutpub.lut.fi/bitstream/10024/164883/1/3D%20-%20MODEL%20DATA%20TRANSFER%20OF%20SHIP%20HULL%20STRUCTURE%20FEATURES%20BETWEEN%20CAD%20PROGRAMS.pdf) |
| 可信度 | B〔摘要依題名與公開片段；全文未讀〕 |
| 對應章節 | 第 9、15、38 章 |

**已知重點：** 從公開片段看，論文討論 AVEVA Marine Hull 與其他 CAD 之間，船體結構特徵（板、型材、開孔、父子關係）的轉移，並提到 AVEVA Marine Steel Databank 的父子關係。適合搭配 C.4.4 一起讀。

**閱讀建議：** 先讀摘要與結論的「資料遺失清單」，再回頭看方法章。不要一開始就鑽研轉換演算法。

### C.5.2 逯濤 (2019)：AVEVA Marine 船體生產設計軟體的二次開發（大連理工大學碩士論文）

| 項目 | 內容 |
|---|---|
| 原文標題 | AVEVA Marine船体生产设计软件的二次开发 |
| 作者 | 逯濤 |
| 出處 | 大連理工大學碩士論文（2019） |
| 連結 | CNKI 收錄（需機構帳號；本課程未取得全文） |
| 可信度 | B〔摘要依題名與 CNKI 引用資訊；全文未讀〕 |
| 語言 | 簡體中文 |
| 對應章節 | 第 9、15、36、38 章 |

**已知重點：** 從題名與 CNKI 的引用資訊看，論文以 AVEVA Marine 的船體生產設計為對象，討論二次開發的流程與工具；可能涵蓋零件抽取、生產資料或建模輔助。實際章節、方法與成效需讀全文確認。

**閱讀建議：** 先看摘要與「系統架構」章，確認它處理的是建模、生產資料還是出圖；再對照本課程第 15 章與第 38 章。若公司有 CNKI 帳號，這是少數直接以 AM 船體生產設計為題的中文碩士論文。

### C.5.3 Hmeshah (2016)：造船產品資料模型的品質管理（羅斯托克大學博士論文）

| 項目 | 內容 |
|---|---|
| 原文標題 | Quality Management Approach of Product Data Models for Shipbuilding |
| 作者 | Khaldoun Hmeshah |
| 出處 | University of Rostock，博士論文（2016） |
| 連結 | [PDF（開放取用）](https://rosdok.uni-rostock.de/file/rosdok_disshab_0000001750/rosdok_derivate_0000037174/Dissertation_Hmeshah_2017.pdf) |
| 可信度 | B〔已核對全文目錄、附錄與 AVEVA Marine 相關章節〕 |
| 語言 | 英文 |
| 對應章節 | 第 15、38、40 章 |

**繁中摘要：**

- 問題：船廠的產品資料模型常有缺漏、矛盾、格式不一致；錯誤越晚發現，修正成本越高。
- 方法：建立產品資料品質（Product Data Quality, PDQ）流程與檢查框架，定義資訊模型與檢查演算法。
- 檢查範圍：零件資訊、製程與結構功能；並討論 CAD 資料品質需求與詳細設計階段的錯誤分類。
- 實作：以 CAD 系統（附錄包含 AVEVA Marine 的 XML 檔與輸入結構）實作檢查，並用物件關聯對應（ORM）存到資料庫。

**可以借鏡：** 第 40 章的測試策略可以借用它的「檢查項目 → 規則 → 報告」結構；第 38 章做外部整合時，先定義資料品質門檻，再談格式轉換。

**不要照抄：** 論文是 2016 年、以德國船廠流程為背景；檢查規則與容許值要重新對應公司標準。

### C.5.4 Lee (2019)：以 3D 設計資訊計算管支架塗裝量（韓國木浦大學碩士論文）

| 項目 | 內容 |
|---|---|
| 原文標題 | 3D 설계정보를 활용한 선박 Pipe support 의장품의 도장물량 산출 프로그램 개발에 대한 연구 |
| 繁中題名 | 利用 3D 設計資訊開發船舶管支架舾裝品塗裝量計算程式之研究 |
| 作者 | 이은세（Lee Eunse） |
| 指導教授 | 조두연（Cho Doo-yeon） |
| 出處 | 木浦大學校 大學院（목포대학교 대학원），2019 |
| 連結 | [dCollection 書目](https://dcollection.mokpo.ac.kr/srch/srchDetail/000000022239) |
| 可信度 | B〔摘要依公開書目與摘要；全文未讀〕 |
| 語言 | 韓文 |
| 對應章節 | 第 17、27、38 章 |

**繁中摘要：**

- 從 AVEVA Marine 的管支架模型，用 PML 抽出 3D 設計資訊。
- 依支架構件的表面積與塗裝規則，計算塗料需求量。
- 提供給支架製造商估算塗裝工時與材料，減少人工量測與估算誤差。

**可以借鏡：** 這是「模型 → 工程量 → 採購／製造」的典型。和 C.4.9 的支架材料統計一起看，可以湊成一套「支架 BOM + 塗裝量」的範例。

**不要照抄：** 塗裝規則、膜厚與損耗率因公司與塗料而異；論文的重點是流程，不是固定公式。

## C.6 簡體中文與影音資源的重點整理

簡體中文資源的優點是貼近船廠實務，缺點是版本與品質參差。以下只整理「讀完能帶走什麼」，不轉載原文。

### C.6.1 艙室絕緣快速建模（《造船技術》2022 年第 1 期）

| 項目 | 內容 |
|---|---|
| 原文標題 | 基于 AVEVA Marine 二次开发的舱室绝缘快速建模方法 |
| 作者 | 〔待核對〕 |
| 出處 | 《造船技術》2022 年第 1 期 |
| 連結 | [CNKI 書目](https://www.cnki.com.cn/Article/CJFDTotal-ZCJS202201005.htm) |
| 可信度 | B〔摘要依公開摘要〕 |
| 對應章節 | [第 17 章](ch17_outfitting_zh-TW.reading.html) |

**繁中摘要：**

- 問題：艙室隔艙的曲面絕緣與型材絕緣，人工建模重複且容易漏。
- 方法：以 PML 在 AVEVA Marine 中建立快速建模流程，分別處理曲面絕緣與型材絕緣。
- 價值：把「絕緣厚度、包覆範圍、型材穿越」等規則寫進工具，減少年人工。

**可以借鏡：** 這類「規則明確、重複性高」的舾裝工作，是二次開發投報率最高的題目。先做唯讀預覽，再開放寫入。

### C.6.2 船舶鐵舾設計中的 AM 二次開發（2025，待核對）

| 項目 | 內容 |
|---|---|
| 原文標題 | 船舶铁舾设计中 AM 软件的二次开发与工程应用实践 |
| 出處 | ResearchGate 公開頁面（期刊／會議待確認） |
| 連結 | [ResearchGate](https://www.researchgate.net/publication/405030565) |
| 可信度 | C〔摘要依公開摘要；出版資訊待核對〕 |
| 對應章節 | [第 17 章](ch17_outfitting_zh-TW.reading.html)、[第 41 章](ch41_case_studies_zh-TW.reading.html) |

**繁中摘要：** 文章以鐵舾設計為場景，說明以 PML 為核心的參數化建模與工程應用，重點在「把設計規則參數化」與「工具要能被設計人員日常使用」。實際成效數字與版本請回到原文確認。

### C.6.3 龍船學院「平面建模」8 集影片

| 集數 | 主題 | 繁中說明 | 搭配章節 |
|---|---|---|---|
| 1 | 板架與邊界 | 板架的建立順序與邊界條件 | 第 9 章 |
| 2 | 板縫與坡口焊接 | 接縫、坡口與焊接資訊 | 第 9、15 章 |
| 3–4 | 曲線與拓撲 | 以參考曲線建立相依關係 | 第 9 章 |
| 5 | 型材 | 加強材的建立與方向 | 第 9 章 |
| 6 | 折邊與端切 | 型材端部處理 | 第 9、15 章 |
| 7 | 角隅開孔 | 角落開孔的規則 | 第 9、17 章 |
| 8 | 肘板 Scheme | 以 Scheme 建立肘板 | 第 9 章 |

> 第 3、4 集合併為一列，所以 8 集只占 7 列。舊版學習地圖仍在 `Docs/_archive/`，可對照每集的預習目標。

**觀看建議：** 影片是操作示範，不是規格書。看的時候記下「指令順序」與「系統提示」，再回公司訓練專案重做一次；不要直接套用到生產專案。

### C.6.4 部落格與 CSDN 文章的使用原則

- 多數文章是舊版 PDMS／Tribon 的經驗，指令可能仍可用，但介面與 API 已變。
- 看到「完整源碼」先確認授權與資安，不要直接貼進公司 PMLLIB。
- 有價值的通常是小技巧（例如 `Q ATT` 的用法、表單版面調整），而不是整套系統。

### C.6.5 南勝 NanSheng：C# 二次開發系列（博客園）

**一句話：** 少數把「C# 掛進 AM」寫成逐步教學的中文部落格，從環境設定、讀取分段、批次抽板架，到呼叫 MarJobLauncher 都有實作紀錄。

| 文章 | 繁中重點 | 對應章節 |
|---|---|---|
| [Aveva Marine C# 二次開發入門 001](https://www.cnblogs.com/NanShengBlogs/p/11107956.html) | 編譯出的 DLL 放到安裝目錄、修改載入設定，讓自訂功能出現在介面 | [第 35 章](ch35_dotnet_zh-TW.reading.html) |
| [C# AVEVA MARINE 二次開發讀取分段](https://www.cnblogs.com/NanShengBlogs/p/17766066.html) | 以 `MyAmFunctionAtt` 掛載功能，快速讀取與篩選分段元素 | [第 4 章](ch04_hierarchy_attributes_zh-TW.reading.html)、[第 35 章](ch35_dotnet_zh-TW.reading.html) |
| [Aveva Marine C# 二次開發提取批量板架語句](https://www.cnblogs.com/NanShengBlogs/p/16324820.html) | 批次取出板架、轉成可再利用的語句 | [第 9 章](ch09_hull_modelling_zh-TW.reading.html)、[第 35 章](ch35_dotnet_zh-TW.reading.html) |
| [AVEVA MARINE C# 程式執行 MarJobLauncher 工作](https://www.cnblogs.com/NanShengBlogs/p/18169353.html) | 從外部程式觸發批次工作，適合夜間出圖或大量計算 | [第 27 章](ch27_drawings_zh-TW.reading.html)、[第 40 章](ch40_debug_deploy_zh-TW.reading.html) |

**可以借鏡：** 它示範了 .NET 開發的「最小閉環」：先讓功能出現在介面，再談資料。若公司要用 C# 而不是 PML，這四篇是最快的起點。

**使用提醒：** 文章是個人實作紀錄，沒有版本矩陣與錯誤處理說明；API 名稱、載入設定與 DLL 放置路徑在不同 AM 版本可能不同。照做之前先在自己的訓練環境備份設定檔。

### C.6.6 YouTube：AVEVA E3D PML 播放清單

| 項目 | 內容 |
|---|---|
| 連結 | [AVEVA E3D - PML 播放清單](https://www.youtube.com/playlist?list=PLjChkog_p_LGhfPnFczX64gLhZsX6rxwx) |
| 可信度 | C〔社群影片；無官方審核，內容依版本而異〕 |
| 語言 | 英文；多為示範操作，旁白與字幕依影片而異 |
| 對應章節 | [第 32 章](ch32_pml_language_zh-TW.reading.html)、[第 34 章](ch34_pml_forms_addins_zh-TW.reading.html)、[第 38 章](ch38_reports_integration_zh-TW.reading.html) |

**繁中重點：** 清單以短示範為主，常見主題包括：從 mesh 建立 primitive、在 Draw 模組用 TDS PML 產生清單、簡化 PML 程式碼結構、PMLCMD 與介面客製。

**觀看建議：** 影片適合「看指令順序與畫面回饋」，不適合當語法依據。看到不熟的函式，回到 C.3.1（PMLPUG）與 C.3.7（SCRM）查簽章，再自己重打一次；直接複製畫面裡的程式碼很容易漏掉前後文。

### C.6.7 AVEVA Community：PDMS/E3D Macros & Tools 版

| 項目 | 內容 |
|---|---|
| 連結 | [PDMS/E3D Forum — Macros & Tools](https://community.aveva.com/aveva-engineering/pdms-e3d-forum/f/macros-tools/) |
| 可信度 | B〔官方社群；回答品質不一，需自行驗證〕 |
| 語言 | 英文 |
| 對應章節 | [第 32 章](ch32_pml_language_zh-TW.reading.html)、[第 34 章](ch34_pml_forms_addins_zh-TW.reading.html)、[第 40 章](ch40_debug_deploy_zh-TW.reading.html) |

**繁中重點：** 這是 AVEVA 官方社群中專門討論巨集與工具的版面。常見問題類型：

- PML 巨集載入後沒出現：`PML REHASH`、`PML LOAD COMMAND` 與 `pmlcmd` 檔的放置位置。
- 表單（Form）版面跑掉、Gadget 沒有更新：事件與 callback 的順序問題。
- 工具列與指令客製：如何把自訂指令掛進既有工具列。
- 跨版本升級後失效：物件成員或載入機制改變。

**使用建議：** 搜尋時把錯誤訊息原文貼進去（去掉專案名稱與路徑），比用中文描述有效。找到答案後，務必在自己的訓練專案重現一次；社群回答常有「剛好能用」但沒有解釋原因的情況。

## C.7 章節延伸閱讀路線

| 章 | 先讀 | 再讀 | 讀完做什麼 |
|---|---|---|---|
| 1 | C.2 版本對照 | A.2.1 Marine 12.1 文件入口 | 建立公司環境卡：版本、模組、環境變數 |
| 3 | C.3.3 Data Model | C.3.6（屬性與偽屬性）、`Dictionary.chm`、`Q ATT` | 整理 10 種元素的屬性筆記 |
| 4 | C.3.6（相對定位） | C.3.7（WRT） | 用 `Q POS WRT` 驗證三個元素的相對關係 |
| 5 | C.3.3、C.4.1 | C.4.4、C.5.2 | 畫出一個板架的相依圖 |
| 6 | C.4.5 | C.4.1、C.5.1、C.4.7 | 追蹤一個零件從模型到生產資料 |
| 7 | C.6.1 | C.4.2、C.4.3、C.4.8 | 列出一個艙室的絕緣與開孔規則 |
| 8 | C.3.4 | 公司目錄維護窗口 | 追蹤一個閥門的 SPEC → SELE → SPCO → CATE |
| 9 | C.3.5 | 公司圖框與 ISO 樣式、C.4.8 | 批次出一張 ISO 圖並檢查材料表 |
| 11 | C.3.1、C.3.7 | C.6.5、C.6.7 | 寫一個含錯誤處理的小工具 |
| 12 | C.3.6 | C.3.3、C.6.6 | 寫一支可用 `Q ATT` 驗證的批次查詢 |
| 13 | C.3.1 表單章節 | C.3.7、C.6.6 | 做一個有輸入檢查的小表單 |
| 14 | C.3.2 | 安裝目錄 `Samples\`、C.6.5 | 編譯並掛載一個最小 Add-in |
| 15 | C.4.3 | `Vitesse.chm`、`kcs_ex_*.py` | 用 Vitesse 輸出板厚報表 |
| 16 | C.4.2、C.4.4 | C.4.6、C.4.10、C.5.3 | 設計一份外部系統欄位對照表 |
| 17 | C.3.1 追蹤章節 | C.3.2 例外章節、C.5.3 | 為工具加上日誌與回復腳本 |
| 18 | C.4.3 | C.6.2、C.4.8、C.5.4 | 完成一個可展示的最小案例 |
| 19 | C.3.6（重量與座標屬性） | C.3.3、C.4.1、公司載重電腦文件、IACS UR L5 | 建立一份重量／艙表匯出契約並完成對帳 |
| 20 | AUGA（DB、Teams、DICE、Session、Upgrade） | 公司 IT 備份政策、Windows Server 文件、AVEVA 支援 | 寫出一份含備份範圍、還原順序與演練的維運手冊 |

## C.8 引用格式與授權

### C.8.1 建議引用格式

**期刊論文（APA 風格）：**

> Son, M.-J., Kang, H., & Kim, T.-W. (2014). AVEVA Marine Scheme-based modeling for reuse of ship hull block model. *Transactions of the Society of CAD/CAM Engineers*. https://doi.org/10.7315/cadcam.2014.041

**官方手冊：**

> AVEVA. (n.d.). *PML Customisation User Guide* (AVEVA Everything3D 3.1). Retrieved November 2, 2026, from https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG_FP.html

**網頁文章：**

> 作者（年份）。〈標題〉。*網站名稱*。網址（擷取日期）。

### C.8.2 授權與使用界線

| 資料 | 可以做的事 | 不建議做的事 |
|---|---|---|
| AVEVA 官方手冊 | 摘要、導讀、內部教學引用 | 整段翻譯後散布、截圖對外公開 |
| CC BY 論文 | 引用、改作（註明出處） | 忽略姓名標示 |
| CC BY-NC 論文 | 非商業內部使用、註明出處 | 用於商業產品或對外收費課程 |
| CC BY-NC-ND 論文 | 非商業引用、不修改 | 改作、再散布修改版 |
| 部落格與影片 | 註明出處後引用重點 | 整段轉載、去除浮水印 |

> 公司內部教材若會放到公開網站，請先移除官方截圖與付費論文圖片，只保留連結與自製圖解。`export_public.py` 已處理官方截圖，但文字摘要仍要確認授權。

## C.9 本次增補與待辦

### C.9.1 本次新增

- 官方文件：E3D 3.1 可靜態存取的七本手冊入口（PMLPUG、NCUG、DMRM、CSUG、ISOUG、DBRM、SCRM）與 40 個主題頁。
- 論文與技術文獻（C.4）：Son 等 (2014)、Cheon 等 (2013)、Kim 等 (2020)、Han 等 (2021)、Li 等 (2024，吊裝整合)、Kunkera 等 (2022)、Li 等 (2024，XML→FEM)、K-SUPPORT 簡報 (2022)，共 8 篇。
- 專利與標準（C.4.9、C.4.10）：CN104537150A、CN122133263A，以及 ISO 10303-242:2022（STEP AP242）。
- 學位論文（C.5）：LUT 船體結構特徵轉移論文（全文待讀）、逯濤 (2019)、Hmeshah (2016)、Lee (2019)，共 4 篇。
- 簡體中文與影音（C.6）：《造船技術》艙室絕緣論文、2025 年鐵舾設計二次開發文章（出版資訊待核對）、龍船學院 8 集影片、南勝 NanSheng 的 C# 系列 4 篇、YouTube E3D PML 播放清單、AVEVA Community 的 Macros & Tools 版。
- 導讀工具：依章節的閱讀路線（C.7，涵蓋第 2–5、9、15、17、25、27、31–36、38、40–43 章）與引用格式／授權界線（C.8）。

### C.9.2 待辦

- [ ] 以公司帳號開啟 docs.aveva.com 的 Marine 12.1 頁面，補上實際主題連結與版本號。
- [ ] 取得 Son 等 (2014)、Cheon 等 (2013) 的韓文全文，補完方法段摘要。
- [ ] 讀完 LUT 論文，補上作者、年份與「資料遺失清單」。
- [ ] 讀完逯濤 (2019) 與 Lee (2019) 全文，補上方法與成效數字；目前僅依公開書目與摘要。
- [ ] 確認 2025 年鐵舾設計文章的期刊、作者與授權。
- [ ] 確認 CN104537150A 的申請人中文全名與現行法律狀態（Google Patents 顯示申請視為撤回）。
- [ ] 向公司確認 TM-2101～TM-2108、TM-2401 等手冊是否已授權。
- [ ] 把 C.4 的案例與公司實際專案對照，標記哪些規則可以直接沿用。
- [ ] 為 C.3.6（DBRM）補上 3.0 與 3.1 的屬性差異註記，避免誤用新版屬性。

### C.9.3 變更紀錄

| 日期 | 變更 | 影響章節 |
|---|---|---|
| 2026-11-02 | 新增本附錄；補 E3D 3.1 手冊、六篇論文與兩篇簡中文章 | 全課程，重點 9、15、17、27、35、38、41 |
| 2026-11-02 | 第二批增補：DBRM／SCRM 手冊（C.3.6–C.3.7）、XML→FEM 與 K-SUPPORT（C.4.7–C.4.8）、兩件專利與 STEP AP242（C.4.9–C.4.10）、三篇學位論文（C.5.2–C.5.4）、C# 與影音社群資源（C.6.5–C.6.7）；重寫 C.7 閱讀路線與 C.9 統計 | 第 4、5、9、15、17、27、32–35、38、40、41 章 |
