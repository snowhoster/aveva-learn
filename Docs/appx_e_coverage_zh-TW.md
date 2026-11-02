# 附錄 E　取材覆蓋總表

各章的取材覆蓋說明集中在這個附錄，依章號排列：每章讀了官方文件多少、哪些子樹沒讀。**官方文件約 1.5 萬頁，各章多是以模組為單位的導讀，並非逐頁讀完；沒有讀到的範圍請直接查官方文件。**

<a id="ch01"></a>

## 第 1 章　Marine 入門基礎：Getting Started 官方導覽（功能、資料、屬性、GUI 與基本操作）

- 官方：AVEVA Marine 12.1 離線文件 *Marine Getting Started*（頁面 ID 1139647 以下全部子頁）。
- **實際讀了 147 頁**，含全部 Assumptions、Marine Functions（含四個 Modules 子頁）、Databases（12 種資料庫）、How Marine Data is Stored（元素型別、屬性、UDA、偽屬性、Attributes window 與 Attributes menu 全部子頁）、Using Marine Products、Basic GUI Features、Basic Operations（含 Drawlist、Outfitting Search Utility、GUI Grid Data、Reference List）、Product Range、Glossary 的 Definitions 與 Abbreviations and Acronyms、Core Filters for Explorers。
- **沒有逐條展開的部分：** Glossary 只摘常用條目（其餘約 50 條如 DDL、IGES、PTRANS、VDM 未收）；Core Filters 只摘要，完整勾選項目請查官方頁面；官方大量小圖示未逐一解說。
- **沒有的內容：** 本手冊沒有 PML 範例或 `.NET` API；章內命令只用於說明，未實測。
- 圖片：16 張取自官方文件；小圖示與模糊的停靠畫面截圖未採用。

<a id="ch06"></a>

## 第 6 章　船體概念與基礎：Product Information Model、模型物件、拓撲與命名

- **Hull Concepts [1110533]**：清單 241 頁，全部讀取並逐頁閱讀（含 XML Interfaces 全部子頁、Standards、Naming、Run Mode Control、Functional Descriptions、Project Material）。
- **Hull Basic Features and Concepts [1105739]**：清單 95 頁，全部讀取。深讀：Marine Concepts（含 PIM 全部子頁）、Marine Dictionary 24 字母頁、縮寫表、Error Handling、Geometry Handling。**僅摘要：** TIL 字元集、詞法與運算子（約 40 頁）及 Imperial Units 語法（約 8 頁），因與船體概念關聯較低。
- **圖片：** 官方頁面含大量 XML 元素結構圖（TXSUR、TXHBD 各元素等），僅選 15 張，其餘依官方文字寫入。XML schema 實檔（`.xsd`、`.chm`）與範例檔不在離線文件內，**未檢視**。
- **未涵蓋：** 本章提到但屬其他文件者（Planar Modelling 的 Panel Statement 與 Design Language、`inithull` 手冊、Assembly Planning、.NET customization 手冊、ERM Integration User Guide、Statement Wizard）。
- 本章無實機驗證，涉及 12.1 實際行為者須在訓練專案確認。

<a id="ch07"></a>

## 第 7 章　資料模型參考導讀：Data Model Reference Manual

資料來源：AVEVA Marine 12.1 離線文件，Data Model Reference Manual（頁面 ID 1135676 及其子頁，含 Assumptions、Elements in the Design Database 各類別、Catalogue／Draft／System／Dictionary／Manu／Schematic／Property／Spooler 等資料庫章、Pseudo Attributes、Introduction to Attributes、Attribute Types、List of All Attributes）。

**閱讀範圍（誠實紀錄）：**

| 項目 | 數字或內容 |
|---|---|
| 全手冊頁數（目錄深度 3 內的清單） | 約 1,110 頁（包含各章首頁、約 1,000 個型別或偽屬性分類頁） |
| 實際取得的頁面檔 | 約 180 頁 |
| 逐字細讀 | 約 20 頁：Assumptions、Introduction to Attributes、Attribute Types、Design Database 首頁與階層圖、Pseudo Attributes 首頁及約 10 個類別頁、數個代表條目（VALVE、HPANEL 等）、`UDA`、`UVALID`、`ULIMIT` |
| 以腳本摘要讀取 | 約 70 個型別條目：每條取描述、前 15 到 30 個屬性、擁有者與成員（前段）。腳本只截取前段，因此表中「重要屬性」不是完整清單 |
| 屬性總表（約 3,000 列、約 344,000 字元） | 只做資料型別統計與約 30 個關鍵屬性的逐條查詢，**沒有通讀** |
| 涵蓋領域 | 設計庫（管理、設備、管路、管件、基本體、結構、船體四類、電纜、梯、房間、組裝、格線、預製片）、目錄庫、Draft、System、Dictionary、Schematic、Property、Manu、Spooler、Global（`DB`） |
| **未讀或僅看目錄** | Accommodation 其餘約 60 型別、Hull General 的 FEM 與理想化型別（除 `HIPAN`、`HIBLO`）、Area、Association、Hanger 元件、Laser Modelling、Link、Router、Stress Analysis、Template、Transaction、Communications、Other Databases；Pseudo Attributes 約 50 個類別頁；`Data_Extraction_to_Attributes.xls` 對照表未開啟 |
| 圖片 | 取用 9 張（設計庫階層圖 7 張、`NOZZLE` 與 `BOX` 示意圖各 1 張）；其他條目圖片（約 3 張，如 `CYLINDER`、`NBOX`）未採用 |

與資料庫管理（Database Management）、SQL Direct、Status Control 有關的內容在第 45 章。

<a id="ch08"></a>

## 第 8 章　初始設計（Initial Design）：型線、曲面、靜水力、艙室與水動力

- 本章取自官方離線文件的 *Initial Design* 子樹，共 7 大塊、約 2,200 頁。**實際深讀的是各 Users Guide 總覽、Technical Brief、Project Management、Major Tasks 中的代表頁，以及 Operators Instructions 的 Data 與部分 Calc 頁**；Lines 的 Command Reference、Surface 與 Compartment 的 Screen Based Reference Guide、Hydro 的各計算參數與 Calc 各對話框，均只讀到章節標題層級。
- 官方文件有多處機器翻譯的中英對照，部分譯名生硬（例如 Hydrostatics 被譯成「流體靜力學」，Compartment 被譯成「艙區」「隔間」），本章統一採台灣造船常用的「靜水力」「艙室」。
- 畫面與部分文字仍寫 Tribon（AVEVA Marine 的前身產品名稱），這代表文件延續自舊版本，**實際 12.1 畫面可能與截圖不完全相同**〔待核對〕。
- 本章所有「二次開發」建議，除明標「文件有依據」者外，均為依文件結構的推論，須在你們的版本與訓練專案實測。

<a id="ch10"></a>

## 第 10 章　裝配規劃與船體結構初步設計：Assembly Planning 與 Hull Structural Design

- 清單展開：Assembly Planning 124 頁；Hull Structural Design 入口 9 頁；Design Scenarios 3 頁；Project Set-up 3 頁；Functions Overview 14 頁；Functional Structure 18 頁；XML 10 頁；Analysis 10 頁加右鍵選單 2 頁；Default File 1 頁；Batch Utilities 9 頁；Planar 57 頁、Curved 59 頁。
- **讀過操作內容（約 210 頁）：** Assembly Planning 全部（Admin 內 Row、Overflow、Cells 與 Parts List Cell Data 約 10 頁僅略讀）；Structural Design 入口、Scenarios、Project Set-up、Project、Functional Structure、XML、Analysis、Default File、Batch Utilities。
- **只讀用途摘要（約 116 頁）：** Planar、Curved 兩選單（由第 13、14 章負責）。
- **未讀：** Hull Model Concepts（XML Interfaces、Standards、Functional Descriptions、Surface Setup）、Vitesse 與 NET Customization 文件。

<a id="ch12"></a>

## 第 12 章　空間管理與有限元素模型：Space Management 與 Finite Element Model

- AVEVA Marine 12.1 官方離線文件：**Space Management**（Some Design Scenarios、Project Set-up、Basic Concepts、Functions Overview，含 Project、Functional Structure、Space Management 三個選單與右鍵選單）。
- AVEVA Marine 12.1 官方離線文件：**Finite Element Model**（Idealized Model、FE Model Creation、FE Model Output、Material Qualities）。
- 本課程相關章節：[第 9 章](ch09_hull_modelling_zh-TW.reading.html)、[第 15 章](ch15_hull_production_zh-TW.reading.html)、[第 36 章](ch36_hull_vitesse_zh-TW.reading.html)、[第 42 章](ch42_loading_computer_zh-TW.reading.html)、[第 43 章](ch43_system_administration_zh-TW.reading.html)。

<a id="ch13"></a>

## 第 13 章　船體詳細設計（一）：設定與標準、初始化工具、平面板架建模

- AVEVA Marine 12.1 官方離線文件：*Hull Detailed Design* 之 **Setup, Customization and Standards**、**Initialization Utility Program**、**Planar Modelling**。
- 本課程延伸：[第 9 章](ch09_hull_modelling_zh-TW.reading.html)、[第 15 章](ch15_hull_production_zh-TW.reading.html)、[第 36 章](ch36_hull_vitesse_zh-TW.reading.html)。

**取材覆蓋（誠實說明）**：實際讀取約 **590 頁**（Setup 約 230、`inithull` 約 53、Planar 約 310），其餘未讀。
- **`inithull`**：全部子頁已讀。
- **Setup**：讀概述、概念與主要檔案格式頁；**未逐頁讀**各 Bevel type（10–149）、Endcut type、Notch type、Bracket Toe（1–136）、Flange End type 的圖解頁，以及 Bending Excess（M1／M2）與 Symbolic Hull Views 的語法細節。
- **Planar**：讀 Users Guide 概念、互動功能、背景視圖語法、預設檔前半與 Design Language 主要陳述式；**未讀**選單頁（與 Users Guide 重複，僅取目錄）、Painting Areas 全部子頁、Part Checking 的 System settings、Notch at Plate Corner 子頁、Special Side Webs 102／103／104、Curve 各子語法、Marking 的後四種子語法、Bracket 子語法 2–7 逐項細節、Special FRP Additions、預設檔 Picture Derivation 後半與 Drawing Development。

> **授權與界線：** 本章文字與表格為本課程依官方文件自行整理；截圖取自官方文件，僅供內部教學參考，不重製長段原文。

<a id="ch14"></a>

## 第 14 章　船體詳細設計（二）：曲面板架建模、選用功能與雜項工具

本章三個子樹合計 357 頁（含標題頁）。實際抓取並閱讀約 **243 頁**，約三分之二；官方頁面只有少數有大篇幅，許多是只有一兩句話的標題頁或表格行。

**已讀**：
- Hull Curved Modelling：Users Guide Interactive 幾乎全部（概念、命名、Model／Geometry／Default／View／Select／Batch 子選單、Hull Tools 選單、預設參數）；Users Guide Batch；Plate Development Method 全部；Miscellaneous 中的 Mould Data（General、Set-up、Input）、Hull Geometry Utility（General、Set-up、記錄類型列表）、Verify Curved Hull References 全部；Operators Instructions 只讀 Create Seam/Butt 與兩個標題頁。
- Optional Hull Functions：12 頁全部。
- Miscellaneous Utilities：Parts List、Material Ordering、WCOG、Hull Marks 的概念、設定、輸入輸出頁。

**未讀或只略讀**：
- **Operators Instructions 約 83 頁**（Model 其餘 22 頁、Geometry 19 頁、Default、View、Select 子頁），內容與 User Guide 對應功能重複，只抽讀 1 頁。
- Hull Geometry Utility 的**各 Record Type 詳細輸入輸出頁**（約 30 頁，含範例）。
- Mould Data 的輸出檔格式兩頁；Default Parameters 的 Drawing Development／Notes 兩頁。
- 零件表與重量重心的**圖框名稱、圖框規則、收據草圖名稱**頁（Parts List 3 頁、WCOG 3 頁）；Material List for Nestings 與 Material List 的輸出欄位頁（約 5 頁）。
- 所有圖片只看了本章引用的 13 張，其餘公式圖與示意圖未逐張檢視。

另外，每一章只是官方手冊的摘要，具體操作請對照實機。

<a id="ch16"></a>

## 第 16 章　船體詳細設計（三）：製造資訊與鐵舾裝生產特徵

- 本章範圍的頁面總數約 740 頁（Manufacturing 約 651、Outfit Steel 約 18、F1 Help Texts 約 71）。
- 實際以工具取回並閱讀約 **365 頁**：Outfit Steel 全部 18 頁（全文）；F1 Help Texts 約 50 頁（TIL Interface、File Check Interface、Block Objects 取全文，其餘條目只讀標題與前段）；Manufacturing 約 300 頁，其中多數只讀前 400–700 字元的摘要。
- 讀得較完整：Autopos（含各陳述）、套料概念與初始化、GPP 預設檔（前半）、3 軸、型材套料、Panel Line 概論、PPI、型材輸出（尤其端切觸發器）、Jig／樣板概論、Robot 中性檔概論、鐵舾裝全部。
- **沒讀或只讀標題的子樹**：Hull Plate Nesting 的各個 Functions Overview 單一功能頁（約 100 頁，只讀概念頁）；Operator's Instructions 的逐指令頁（約 100 頁，只讀群組頁）；Generic Postprocessor 的 Kerf Format 1–8 逐頁；Robot Interface 的各 Record Type、Message Records 逐頁；Bending Templates 各子頁（Normal／Flexible／Special／Cross 的 Default 檔範例與規則）；Plate Jigs 與 Jig Pillar 的各陳述細頁；型材輸出的 Endcut Dimensioning 子頁（Linear／Angle／Radius）、Nested Profile Sketch 的三個範例頁；F1 Help Texts 的各 Check／Create 條目內容（只歸納結構）；F1 頁面中文機器翻譯多不通順，一律以英文原文為準。
- 圖片：採用 14 張官方圖，其餘低解析或關聯弱未採用；鐵舾裝端切頁（`1122733`）的圖未出現在擷取內容中。

<a id="ch18"></a>

## 第 18 章　通風與設備設計：HVAC Designer 與 Equipment

- **Equipment：** 根頁 `1152005` 與全部子頁（清單 116 行，含重複的練習頁）皆已讀過。
- **HVAC Designer：** 清單共 463 行，**實際讀過約 200 頁**：HVAC Administrator 全部上層頁、教學練習（`1155017`–`1155038`）與 Draft Sketches 子頁；HVAC 使用指南的概念、階層、HVAC Window 與屬性、System／Branch、Divide、Assembly、Tiles／Grid、Autofill、工具與 Query、Split、Spool、Sketch、Menu Map、Work Area、Palettes、設計參數表，以及代表性元件視窗（Straight、Radiused Bend、Boot、Motorized Damper、General Plant Item、Grille off Brco、Air Handling Unit、Nozzles）與 Joint／Stiffener 清單。
- **未逐頁讀（約 260 頁）：** `Components` 下其餘約 150 個個別元件視窗（欄位清單，結構同已讀頁）與 `HVAC Catalog` 下約 100 個型錄元素頁（多為參數化幾何示意圖）。
- **圖片：** 16 張皆先預覽再加入（Equipment 9 張、HVAC 7 張）。

<a id="ch20"></a>

## 第 20 章　管路等角圖：Isodraft

- **整體：** Isodraft 子樹約 402 頁，本章實際讀過約 **225 頁**（含少量只略讀的頁面）。
- **完整讀過：** 使用指南的使用方式、GUI 與命令列、查詢與選項預設、目錄需求（描述文字、SKEY、P-point 端部、替代品項代碼、SHOP 旗標）、螺栓前半（儲存、BTSE、BLTAB、規格與選擇規則）、設計需求（SPOOLER、ATTA、額外品項）、管路元件標註、圖紙客製、材料清單、等角圖繪製、變更標示、符號基本原則與通用符號、傳輸檔。
- **指令參考只讀了約 45 頁：** Setting Up、`DETAIL`、`CHECK`、`FILE`、`OPTIONS`、`ISOTYPE`、`SPLIT`、`MARK`、`SIZE`、`TRANSFERFILENAME`、`PREPROCESS`／`POSTPROCESS`／`PROCESS`、`UNITS`、`MATERIALLIST`、`DIMENSIONS`、`CUTTINGLIST`、`SPOOLNUMBERS`、`ATEXT`、`OUTCOM`、`BOLTING`、`CUTBACK`、`WASTAGE AREA`、`WELDNUMBERS`、`SUPPORTS`、`FRAME`、`POSITION`、`COFORMAT`、`COIMPP`、`CONTSHEETS`、`REPEATABILITY`、`REMOVE`（部分）。
- **幾乎沒讀：** 其餘約 90 個指令頁（如 `ADD`、`BENDRADIUS`、`SKEWBOX`、`ITEMCODE`、`KEYS`、`TAPPING` 等，僅依使用指南描述轉述）；Symbol Keys 附錄約 30 頁；Alternative Texts 附錄的 ATEXT 編號清單；Error Messages 只讀前段；Material Control File 欄位圖；COMPIPE 的 Linelist／MTO 格式；DXF 轉 MicroStation 的字型細節。
- **使用指南未細讀：** 螺栓長度計算各小節（標準法蘭、夾式、混合、噴嘴、額外螺帽）、Reference Dimensions 的設定與錯誤、「多於四個接口的元件」、偏置與角度管件。
- **官方文件本身的疑點：** `FILE` 預設單檔或多檔說法不一；`PREPROCESS`／`POSTPROCESS` 兩頁敘述重複；`CHARHEIGHT` 與 `CHARSIZE` 名稱不一；「3275mm2」單位存疑。皆需實測。

<a id="ch23"></a>

## 第 23 章　艙室設計與原理圖：Room Design 與 Schematics

本章依 *Room Design*（約 149 頁）與 *Schematics*（約 283 頁）的總覽與關鍵子頁撰寫，Tags 指南僅依目錄概述。圖片取自官方文件，均已預覽確認主題相符。

<a id="ch24"></a>

## 第 24 章　設計共通功能：Clash Manager、Data Checker、Design Model Editor 與 Reporting

本章對應的 *Design* 節點約 911 頁，**沒有逐頁讀完**。實際閱讀如下。

- Data Checker Utility（17 頁）：全部讀完。
- Clash Manager（177 頁）：約 89 頁；概念、設計工作流程、Procedures、Entry Information、Performance Hints、`mmscmd` 全讀，GUI 僅讀 Clash Manager、Run Clash Set、Configuration 各分頁與 Test Rules。
- Design Common Functionality（105 頁）：每頁讀開頭約 1500 字元，概覽級。
- Design Model Editor（80 頁）：約 73 頁，多數截取前約 1100 字元。
- Reporting（136 頁）：約 80 頁；Reference 中 Report Settings、Report Controls、Styles and Conditional Formatting 細節未讀。
- Reporting Reference（46 頁）：全部讀到，每頁約前 1300 字元。
- Design Reference（344 頁）：僅約 62 頁（Utilities 的 Data Consistency Checking 與 Clash Detection）；**Creating a Model、General Commands、Display、Interacting with a Graphical View、Error Messages、Copying Model Data from Marine to Review 均未讀**。

未讀或只略讀：Clash Manager 的 Clash Report、Filter、Consolidated Report、Element Report、Options 表單頁、Model Management Wizard；Reporting 的控制項與帶屬性參考；Schematic Gateway；Design Reference 的指令語法圖整體。總計約 470 頁有不同程度閱讀，其中完整讀完的約 100 頁。圖片 16 張來自官方文件，皆已逐張預覽確認。

<a id="ch26"></a>

## 第 26 章　目錄與等級深入：Catalogs and Specifications 與 Design Templates

本章依 AVEVA Marine 12.1 官方離線文件的 Catalogs and Specifications [1105729] 子樹整理，該子樹共 448 個頁面。已取得全部頁面文字，但實際逐頁閱讀並用於本章的範圍如下，其餘不宣稱已讀：

- Design Conventions（約 32 頁）：全部讀完；吊架命名慣例各頁僅有圖片，未逐張檢視。
- Design Templates（約 53 頁）：全部讀完。
- Reference（約 235 頁）：讀約 120 頁（目錄結構、參數、元件、建目錄、P-point／Geomset、顯示表示法、DATA、一致性檢查、管路元件特例、Specification Constructor、SPECON、典型等級、Properties Constructor）；未讀約 110 頁（Common Commands、各 3D 基本體個別頁、`MODEL SETTINGS` 與 `REPRESENTATION` 完整語法、SPECON 與 PROPCON 語法圖、錯誤訊息表、Nominal Pipe Size Tables、典型元件建構巨集）。
- GUI 冊 [1153196]（約 124 頁）：讀約 40 頁（Create 選項各表單、Convert Spec、Pipework 與 Steelwork 部分工具、Understanding Parameters）；未讀約 85 頁（通用 GUI 工具、報表、Lists、Extract Data Control、Spec Generator、Room Design、Electrical、Equipment、Surface Treatment、Bolting Specifications 等）。

整體而言，448 頁中約 245 頁實際閱讀、約 200 頁未讀；圖片 16 張皆取自已讀頁面的官方插圖，經逐張預覽確認主題後加入。

<a id="ch28"></a>

## 第 28 章　Draft 圖面管理與出圖流程：Draft Administrator、AutoDRAFT、Drawing Production 與 PLOT

- AVEVA Marine 12.1 離線文件 *Draft Administrator Application* [1130842]、*AutoDRAFT* [1130636]、*Drawing Production* [1132409]、*PLOT* [1132720]（英文為準，中文為機器對照）。
- 四個子樹共約 317 個頁面 ID，全部轉成文字；實際逐段閱讀：Draft Administrator 約 90／105 頁、Drawing Production 約 64／68 頁、PLOT 約 40／52 頁、AutoDRAFT 約 70／92 頁。
- **未讀或略讀：** Draft Admin 的 Change Style 與 Tag Rule 部分頁尾、H&S ADP 完整 BOM 欄位、管理者選單與附錄（以圖為主）；Drawing Production 的 Radial Dimensions 細節與附錄；PLOT 的 BENSON、CALCOMP、HOUSTON、HPGL2、LASERJET、PENMAN、XDUMP、POSTSCRIPT 完整選項與 Driver Quick Reference；AutoDRAFT 的 Symbol／Frame Editor 命令檔衍生細節、命名規則、PDMS/J 專用頁、選單頁。
- 圖片：共 15 張，皆為官方文件截圖，僅供內部教學；已實際檢視確認後加入（檔名皆以 ch31_ 開頭，存放於 aveva 圖片資料夾）。
- 本章不涵蓋：Marine Drafting、Design Draft、Marine Drafting Application Menus（由其他章處理）與 Area Based ADP（[第 30 章](ch30_other_modules_zh-TW.reading.html)）。

<a id="ch29"></a>

## 第 29 章　Marine Drafting 與 Design Draft：船體與舾裝的圖面製作

- **實際取得約 450 頁**（Marine Drafting 約 125、Design Draft 約 150、選單約 175）。**完整讀過：** Marine Drafting 的概念、圖面、子圖、圖層、表單、標註、DXF／IGES、多重選取、公用程式（`SY006/007/010/013/015`、`SB028`）、附錄的圖面類型與系統圖層；Design Draft 的資料庫、畫圖面、視圖屬性、表現規則、填充、剖面、游標、輸出、顏色、修訂、Change Highlighting、標籤與 Autotagging。選單頁只讀每頁「用途／操作／結果」前 650 字。
- **沒讀（或只取得未讀內文）：** Marine Drafting 的鍵盤快捷鍵、線型與點定義子頁、各尺寸類型版面細節、SZ024／SZ004 中性檔、預設檔關鍵字附錄、色彩表；Design Draft 的 DGN 輸出、標準 DXF 細節、各尺寸元素屬性、Intelligent Text 語法細節、字型、P-line 註記、Underlays/Overlays、2D Drafting 圖元、Isodraft 符號、點線構造；選單的 `Geometry Mode` 數十個子功能。

<a id="ch39"></a>

## 第 39 章　客製化官方手冊導讀：Software Customization、.NET Customization、Data Access Routines 與 Marine Customization

**資料來源：** AVEVA Marine 12.1 離線文件：Customization [1105730]（Data Access Routines [1135545]、NET Customization [1147959]、Software Customization [1134643]、PML Publisher [1150394]）、Marine Customization [1305437]。

各子樹（頁數／實際讀了）：Marine Customization 約 15／15（全讀，無圖片）；Data Access Routines 約 57／約 46（詳細常式規格 [1135573] 只讀 `D3ECHK`～`D3INIT` 數個）；NET Customization 約 113／約 85；Software Customization（含 Reference）約 565／約 73；PML Publisher 約 20／約 12。

合計約 **219 頁**（部分只讀前段）。

**沒讀或只略讀：** DARs 的 Example 2、輔助常式庫逐常式規格、C 標頭檔；NET 的 Grid API、輸入遮罩、My Data 其餘約 18 頁；Software Customization 的 Reference 物件／成員／方法總表與 Gadget 語法圖（約 130 頁）、PML1 運算式（約 14 頁）、基礎語法與 Gadget／Form／Layout 各頁（約 300 頁，與第 32、34 章重疊，只抽樣）、EDG 其餘約 8 頁。離線文件中文欄為機器翻譯，本章以英文原文為準。

<a id="ch44"></a>

## 第 44 章　Monitor 與 Marine 執行環境：Monitor Reference、Program Environment、Runtime 與命令列工具

**實際讀了多少：** *Monitor Reference*（根頁 1151778）底下約 54 頁全數讀完（Assumptions、Access Rights 全部子頁、Using Monitor 全部子頁、Command Summary 全部 19 個命令頁、Error Messages、Menu Maps）。*Marine Administration*（根頁 1103794）底下 17 頁全數讀完（Program Environment 全部子頁、Projects、Runtime System、Command-line Utilities、Data Bank Utilities、Programs）。

**只讀了部分：** 兩頁超大型表格——「List of Executables」（約 160 項）已全讀，但本章只列代表項；「All Logical Names」（約 375 個環境變數）只讀了開頭與以前綴統計抽樣，**並未逐項核對全部變數說明**，所以 44.12.1 的前綴數量為約略值。

**沒讀的：** 文件內提及但不在這兩個根頁底下的 *Administration User Guide*、*Marine Software Installation Guide*、*Software Customization Guide*、*Database Management Reference Manual*（Extract 與 Working Extract 細節）。

**圖片：** Monitor Reference 的 Menu Maps 共 6 張小圖，採用其中 4 張（Monitor > Modules、Project、Display、Help）；其餘兩張（僅主選單列、Window 選單）資訊量低，未收。Marine Environment utility 1 張。44.2 的架構示意以文字圖呈現，無圖檔。

**延伸閱讀：** [第 2 章](ch02_architecture_zh-TW.reading.html)（架構與模組）、[第 3 章](ch03_project_database_zh-TW.reading.html)（專案與資料庫）、[第 31 章](ch31_dev_environment_zh-TW.reading.html)（開發環境）、[第 40 章](ch40_debug_deploy_zh-TW.reading.html)（部署）、[第 43 章](ch43_system_administration_zh-TW.reading.html)（系統管理）。

<a id="ch45"></a>

## 第 45 章　資料庫管理深入：Database Management、SQL Direct 與 Status Control

- **實際讀取頁數：** 約 **250 頁**（Database Management 約 123 頁、SQL Direct 62 頁全讀、Status Control 約 62 頁；PML 物件重複的方法表僅略讀）。預覽約 24 張圖，採用 15 張。
- **Database Management 已讀：** Database Concepts 全樹（除 Hierarchical Data Model、Element Instances）、Database Modification、Save/Get Work、Multi-write Claims and Extracts、Undo and Redo、Shared Collections、Comparisons Across Sessions and Stamps、Project Queries、Link Documents 概念、Inter-DB Macros、Sequence Number Generator、Distributed Attributes 概念、Cleanup。
- **未讀子樹：** Navigation and Query Syntax、Attributes、Expressions、Rules、Collections 全樹；Link Documents 與 Distributed Attributes 的設定細節（多為語法字典，與第 7、33 章重疊）。
- **SQL Direct：** 全樹已讀（逐步操作的 Excel／Access／Word／Crystal Reports 畫面圖未逐張採用）。
- **Status Control：** 全樹已讀；`statusData` 內部方法、`STATUS` 物件重複列出的多載與 C# 類別的 Object Browser 截圖僅略讀。

<a id="ch46"></a>

## 第 46 章　船體資料庫與分散式專案：Hull Dabacon 與 Global

- **Hull Dabacon**（根 ID 1109645）共 98 頁，全部讀完（含兩層以下所有子頁）。圖片預覽 14 張、採用 7 張；其餘（如 Manu 對話框、材料工具視窗）因過小或資訊量低未採用。
- **Global**（根 ID 1105738）共 319 頁：已讀 Global Server Installation（6 頁）、Global User Guide（約 126 頁，Scheduler 與個別視窗欄位僅讀重點）、Global WCF Configuration（約 50 頁）；Running Global Projects（約 135 頁）實際讀了約 60 頁（運作模式、Daemon 與診斷、Merge、Pending 檔、更新與傳播、Reverse Propagation、備份、Extract 概念、防火牆、Housekeeping、Project Setup Guidelines）。
- **未讀或只略讀的子樹：** Running Global Projects 中的 *Transaction Audit Trail*（TRINCO／TROUCO／TROPER，約 40 頁）、Extract 指令語法與 Claim／Flush 失敗原因、*Distributed Extract Hierarchy*、各管理角色、*Recovery from Reverse Propagation Errors*、*Using Global to Distribute Catalogue Data*、*Example Macro*；Global User Guide 的個別視窗欄位與 Global Scheduler 細節僅讀重點；WCF 憑證綁定與各安全模式範例設定檔僅略讀。
- 全章圖片共 16 張，皆已預覽確認後加入（檔名皆以 ch37_ 開頭，存放於 aveva 圖片資料夾）。

<a id="ch47"></a>

## 第 47 章　12.1 版本說明與升級：Release Bulletin、設定需求與功能變更


- **已取得**：*Hull and Outfitting* [1224159] 下全部 587 頁（含根頁）皆已轉出純文字並掃描標題。其中**逐字讀完**的約 140 頁：About、Software Distribution and Installation、Test Projects、Upgrading from Previous Releases 全部、Configuration、General System Changes、Database changes、User Interface、Administration、Global 與 Catalogue 部分頁面、Known Issues 與少數 Hull 生產資料頁面。**只讀開頭（約 280–700 字元）**的約 440 頁：各領域新功能（Initial Design、Hull General、Surface Manager、Space Management、Structural Design、Hull Detailed Design、Weld Planning、Assembly Planning、Marine Drafting、Outfitting Draft、Diagrams、Engineering、Outfitting Module 與 Design Applications）。這些頁只擷取 Description 與標題，Benefits、For More Information、Compatibility Constraints 的細節大多未完整讀，因此 47.8 的彙整表是「代表項目」而非完整清單。
- 另讀：*What's New in AVEVA Marine?* [1105760]、*Welcome to the AVEVA Marine Documentation* [1526835]、*Terminology* [1225318]、*Abbreviations in the User Documentation* [1109374] 全文。
- **未讀**：*Before you Begin* [1211036] 下的 Marine Getting Started 子樹（Assumptions、Database Types、Attributes、GUI 基本操作、Product Range、Glossary of Terms and Abbreviations 的 Definitions／Abbreviations、Core Filters for Explorers 等，約 50 頁，只列出清單）；以及公告中 AVEVA Licensing System [883754]、AVEVA Manufacturing [988916]、AVEVA Marine [879117] 三個夾在 Hull Detailed Design 中的頁面（只看到標題，內容未深入）。
- 圖片共 14 張，皆經預覽確認後加入。
- 相關章節：[第 43 章](ch43_system_administration_zh-TW.reading.html) 系統管理與維運、[第 45 章](ch45_database_management_zh-TW.reading.html) 資料庫管理（Session、Extract、Global 概要）。
