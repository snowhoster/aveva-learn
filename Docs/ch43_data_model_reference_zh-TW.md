# 第 43 章　資料模型參考導讀：Data Model Reference Manual

> 前面各章用到的 `EQUIPMENT`、`BRANCH`、`SPRE`、`WVOL`，每個名字在官方文件裡都有一個「條目」。這些條目集中在《Data Model Reference Manual》（以下簡稱 DMRM）。它不是教學書，而是**字典**：你不會從頭讀到尾，而是在寫 PML、設計報表、查 UDA、判斷「某型別能不能放在某型別底下」時翻它。
>
> 這一章的目標是讓你**會查、查得快、看得懂**：知道手冊怎麼分、一個條目長什麼樣、屬性有哪些資料型別、偽屬性與 UDA 在哪裡找、手冊的限制在哪裡。章末挑出約 50 個代表型別做成速查表。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 離線文件的 DMRM（頁面 ID 1135676 底下，約 1,110 頁）。型別描述、屬性名稱、合法擁有者／成員、資料型別皆來自實際讀到的條目；中文名為本課程翻譯。官方頁面沒有說明的行為（單位語法、限定詞語法、PML 對應寫法）標〔待核對〕，不憑印象補寫。本手冊的前言自稱寫給 MarinePlant 的使用者，內文仍沿用 PDMS 的名稱（例如 `USER` 條目寫「PDMS User Element」）。資料庫管理、SQL Direct 與 Status Control 在第 42 章，本章不重複。章末附實際閱讀範圍。

## 43.1 學習目標

讀完本章，你應該能夠：

1. 說明 DMRM 的整體分區：各資料庫的元素型別、偽屬性、屬性簡介與屬性總表。
2. 讀懂一個元素型別條目的四個部分：描述、屬性、合法擁有者、合法成員。
3. 區分一般屬性、特殊屬性、偽屬性與 UDA，並知道各去哪一區查。
4. 說出屬性的資料型別（Name、Real、Integer、Reference、Logical、Word、String、Datetime、各種 Array、Noclaim）及其限制。
5. 理解「屬性長名稱」（條目內）與「屬性縮寫」（總表、命令列）的差別。
6. 憑型別地圖，判斷一個元素屬於哪個資料庫與哪個類別，以及設計庫的主要階層。
7. 查出常用型別（設備、管路、結構、船體、目錄、Draft、系統）的重要屬性與擁有關係。
8. 用 `Q LIST`、`Q OLIS`、`Q ATT`、`Q PSATTS`、`Q UDALIS` 等查詢確認元素的合法成員與屬性清單。
9. 把 DMRM 的資料型別對應到 PML 取值，並知道哪些對應仍需實測。
10. 說明手冊的限制：船體條目很薄、部分頁面有轉檔缺漏、版本差異，以及遇到時的處理方式。

## 43.2 手冊的結構與查閱方法

### 43.2.1 一張地圖

DMRM 依「資料庫類型」切成章。每一章列出該資料庫所有元素型別，每個型別一頁。

| 區 | 內容 | 型別／頁數（依列表） | 用途 |
|---|---|---|---|
| Assumptions | 讀者假設 | 1 頁 | 手冊寫給需要寫批次巨集、客製 GUI 的熟練使用者 |
| Catalogue Database | 目錄庫元素 | 122 型別 | 規格、元件、點集、幾何集、資料集 |
| Communications Database | 通訊庫 | 2 型別（`COMM`、`COMW`） | 通訊庫型別，本章未展開 |
| Elements in the Design Database | 設計庫元素，依 34 個類別分組 | 約 500 型別 | 模型主體，最大的一章 |
| Dictionary Database | 字典庫 | 37 型別 | UDA、UDET、資料表視圖、Status 定義 |
| Draft Database | 繪圖庫 | 114 型別 | 圖面、視圖、標註、樣式、規則 |
| Global Database | 全域庫 | 22 型別 | 分散式（DB、Team、Role、Stamp） |
| Manu Database | 製造庫 | 40 型別 | 船體製造套件、板件、型材 |
| Property Database | 物性庫 | 39 型別 | 流體、材料、應力分析載荷 |
| Schematic Database | 示意圖庫 | 34 型別 | P&ID 類（`SCEQUIPMENT` 等） |
| Spooler Database | 預製庫 | 15 型別 | 管段、焊口、管段圖 |
| System Database | 系統庫 | 48 型別 | USER、TEAM、DB、MDB、ACR |
| Transaction Database | 交易記錄庫 | 16 型別 | 交易與訊息記錄（`TRMESSAGE`、`TRFAILURE` 等） |
| Other Databases | 其他 | 3 型別（`ENGGRP` 等） | 工程整合 |
| Pseudo Attributes | 偽屬性，依 67 個類別分組 | 67 頁 | 計算屬性查詢 |
| Introduction to Attributes | 屬性簡介、屬性型別、**屬性總表** | 3 頁 | 全部屬性的縮寫、型別、說明 |
| Mapping of Data Extraction Keywords | 船體區 Data Extraction 關鍵字與屬性對照 | 1 頁，連到 `Data_Extraction_to_Attributes.xls` | 把舊報表改用報表工具 |

> 數字依第 43 章取材時的目錄清單，型別數以各章列表項目數計，可能含少量重複出現的型別（例如 `WORLD`、`TEXT` 在多個庫各有一列，同一型別在不同庫的條目是同一頁）。

設計庫的 34 個類別，依型別數排序前幾名是：Accommodation（住艙，67）、Hull Planar（33）、Structural（32）、Hull General（31）、Piping Component（29）、Hanger Component（28）、Primitive（24）、Cabling（22）、HVAC Component（22）。船體相關有四個類別：Hull Curved、Hull General、Hull Manufacturing、Hull Planar（共 88 型別）。

### 43.2.2 一個型別條目長什麼樣

以 `VALVE`（閥）為例，條目結構是固定的：

| 區塊 | 內容 | 開發者怎麼用 |
|---|---|---|
| 標題 | `Valve Element (VALVE)`：英文全名與括號中的型別代碼 | 代碼用於命令與 `TYPE` 比對 |
| 類別 | 如「Piping Component Element」 | 判斷屬於哪個類別 |
| Description | 一兩句用途說明；許多條目是空的 | 確認這個型別是「做什麼的」 |
| Attributes | 屬性長名稱＋一句說明，約 3 到 70 項 | 看這個型別有哪些欄位 |
| Legal Owners | 可以擁有它的型別 | 建立元素前，找出 CE 該放哪 |
| Legal Members | 它可以擁有的型別 | 走訪樹、收集條件 |

`VALVE` 的 Legal Owners 只有 `BRANCH`、Legal Members 是 None：閥只能放在分支底下，自己不能再放東西。

> 〔公開版未收錄：AVEVA 官方產品截圖〕設計庫最上層階層：WORLD 下有 SITE、AREA WORLD、GROUP WORLD；SITE 下有 ZONE、BOUNDARY、DRAWING、GROUND MODEL；ZONE 下有 STRUCTURE、PIPE、EQUIPMENT、HVAC 等

*圖 43-1　設計庫階層的頂層：WORLD → SITE → ZONE，再往下才是結構、管路、設備與 HVAC。星號是原圖腳註標記。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕設備與管路階層：EQUIPMENT 擁有設計基本體、NOZZLE 與 SUBEQUIPMENT；PIPE 擁有 BRANCH 與管件；RESTRAINT 擁有 HANGER

*圖 43-2　設備與管路的階層。EQUIPMENT 底下有基本體、NOZZLE 與 SUBEQUIPMENT；PIPE → BRANCH → 管件；RESTRAINT → HANGER → 吊架元件。（AVEVA 官方文件截圖，僅供內部教學）*

這些階層圖放在設計庫章的最前面，是整本手冊最值得先看的幾張圖。它們還包括 Structure 往下的五張子階層圖（43.4.4 節）。

### 43.2.3 三條查閱路線

| 你的問題 | 先去哪裡 | 例子 |
|---|---|---|
| 「這個型別有什麼欄位？」 | 該型別的條目 | `NOZZLE` 的 Temperature、Pressure、Catref |
| 「這個屬性是什麼型別、什麼意思？」 | Introduction to Attributes 的**屬性總表** | `SPRE`：element，Component spec reference |
| 「這個計算值有沒有現成的？」 | Pseudo Attributes 的分類頁 | Positional 類的 `WVOL`、`POS`、`ORI` |
| 「型別 A 可以放在型別 B 底下嗎？」 | A 條目的 Legal Owners，或命令列 `Q OLIS`／`Q LIST` | `HPLATE` 的擁有者只有 `HPANEL` |

屬性總表有 Attribute Name、Data Type、Qualifier、Description 四欄，約 3,000 列（本課程用腳本統計，Data Type 欄為 real 約 800、string 約 625、element 約 500、integer 約 470、logical 約 290、word 約 180、pos 約 100、dir 約 47、ori 6）。這是最完整的屬性字典，但**不告訴你哪個型別有這個屬性**，要靠型別條目對照。

### 43.2.4 長名稱與縮寫

型別條目裡的屬性用**長名稱**（如 `Position`、`Spref`、`Desparam`、`Ispec`），總表與偽屬性頁用**縮寫**（如 `POS`、`SPRE`、`DESP`、`ISPE`）。兩者對不上字母是常態：

| 條目中看到 | 總表中的縮寫 | 資料型別（總表） | 說明 |
|---|---|---|---|
| Position | `POS` | pos | 位置 |
| Orientation | `ORI` | ori | 方向 |
| Spref | `SPRE` | element | Component spec reference |
| Pspec | `PSPE` | element | Pipe specification |
| Desparam | `DESP` | real(100) | Design parameters |
| Built | `BUIL` | logical | Built/Unbuilt flag |
| Ispec | `ISPE` | element | Insulation spec reference |
| Stspec | `STSP` | element | Structural specification |

總表以最多 4 或 6 個字元為主；本章取樣中，`XLEN`、`DIAM`、`HEIG` 等長度屬性在總表中是縮寫，但 `BOX` 條目裡寫的是 `Xlength`。因此：

- 命令列與批次巨集可以用縮寫；
- PML 程式官方建議用完整名稱（見[第 12 章](ch12_pml_database_zh-TW.reading.html)）；
- 找不到對應時，用 `Q ATT` 在實際元素上驗證，不要靠猜。

> **專業提醒：** 條目的長名稱與總表縮寫**沒有一個統一的轉換規則**。不要寫程式「自動截成前 4 字母」；如果要做屬性映射表，從實際元素用 `Q ATT` 或 `ATTLIST` 取得清單。

常見錯誤：

- **把條目標題的型別代碼當成 `TYPE` 的回傳值。** `TYPE` 的說明是「Type of the element, ignoring UDET, truncated to 4 or 6 characters」，所以型別代碼可能被截短；`FULLT` 則回傳完整型別，`ACTTYPE` 在非 UDET 時同樣截短。比對型別前先用 `Q TYPE` 實測。
- **在總表找到屬性就以為每個元素都有。** 總表是全域清單，是否可用要看型別條目或實測。

## 43.3 屬性的分類與資料型別

### 43.3.1 一般屬性與特殊屬性

「Introduction to Attributes」把屬性分成兩類：

| 類別 | 定義 | 例子（手冊所舉） |
|---|---|---|
| General attributes | 遍及資料庫，大多數元素都有 | `OWNER`（每個設計元素都有擁有者）、`POS`、`ORI`、`BUILT` |
| Special attributes | 屬於特定元素或元素類別，有特定意義 | Branch 的 `FLOWD`（流向） |

另有三點在簡介頁說得很清楚：

1. **所有屬性都能查詢與設定**，但很多是命令自動設定的；只有「通常需要明確設定」的屬性才完整說明，自動設定的屬性則因為「可以拿來做報表」而保留。
2. 有些屬性只被 PDMS 模組使用，手冊不列。
3. 有些特殊屬性只用於 Isodraft 或 Draft 的繪圖控制，用法在各自的參考手冊。

### 43.3.2 屬性資料型別

下表依「Attribute Types」頁整理，並補上總表常見的記法。

| 型別 | 官方說明（摘要） | 限制 | 例子 |
|---|---|---|---|
| Name | 以 `/` 開頭，可含多個以 `/` 分隔的名稱段 | 頁面寫最長 51 字元；`$`、`@` 不能出現；STAR 命令啟用後 `*` 有特殊意義 | `/HX42`、`/HX42/NOZ1` |
| Real | 單一實數，通常存尺寸 | — | `DIAM`、`XLEN` |
| Integer | 單一整數 | 管件的 `ARRIV`、`LEAVE` 連接點；Primitive 的 `OBSTR` | `1`、`-2` |
| Reference | 另一元素的內部參考號（如 `=12/106`），不是名稱 | 可限制只能指向某些型別，限制顯示在條目括號中 | `SPREF` 只能指向 `SPCOM` |
| Logical | `TRUE`／`FALSE` | — | `BUILT` |
| Word | 最多 4 個字元 | 與 ch3 引用的 DBRM 所說 4 或 6 字元略有出入〔待核對〕 | 流向 `FORW`、`BACK` |
| String | 最多 120 個英數字元 | 以單引號或豎線 `|…|` 包住，後者便於輸入英制 `|4'6|` | `'HP STEAM'` |
| Datetime | 日期時間，依目前 locale 格式 | — | 見 `DATE` 類 |
| Real Array | 多個實數 | — | `POS`：X、Y、Z 三值 |
| Integer Array | 多個整數 | — | `LEVEL` 兩個整數，控制繪圖細節範圍 |
| Reference Array | 多個參考 | — | `CRFA`：四通閥（`VFWAY`）與 `CROSS` 的連接 |
| Noclaim | 不必認領元素即可修改的屬性 | 兩人接到同一個管嘴時**沒有警告**，最後 `savework` 的人勝出 | 分支連到設備 |

總表的資料型別欄另有專屬記法，這些在簡介頁沒有解釋，是從總表與偽屬性頁歸納出來的：

| 記法 | 意思 | 例子 |
|---|---|---|
| `real(6)` | 固定長度的 Real 陣列 | `WVOL`：包圍盒六個值 |
| `real(100)` | 最多 100 個元素的陣列 | `DESP` |
| `string(120)` | 最長 120 字元的字串 | `DESC`、`FUNC` |
| `string(500)`、`string(700)` | 較長字串 | `NAME`（500）、`FLNN`（700） |
| `element(10000)` | 元素參考陣列，上限 10,000 | `MEMB` |
| `word(2000)` | Word 陣列 | `LIST`、`ATTLIST` |
| `pos`、`dir`、`ori` | 位置、方向、姿態 | `POS`、`HDIR`、`ORI` |
| Qualifier 欄 | 查詢時要多給的參數類型：`attr`、`elemtype`、`integer`、`element` | `ELEMOD`（logical，qualifier 為 integer：自某 session 起是否被改過） |

> 資料型別的細節與前一版的差異：ch3 引用的 E3D 2.1 DBRM 說 `Name` 型最長 51 字元，12.1 屬性總表中 `NAME` 是 `string(500)`，`FLNN` 是 `string(700)`。以實際系統行為為準〔待核對〕。

### 43.3.3 單位

DMRM **沒有一頁專門說明單位**。本次取材只在三處看到與單位有關的條目：

| 位置 | 說明 |
|---|---|
| UDA 的 `Uunits` | 「Units of attribute values (bore/distance/text)」：UDA 的值是 bore、distance 還是文字 |
| 目錄 `DATA` 的 `Punits` | 「Data Property Units」：資料屬性的單位 |
| Draft 的 `Ucode` | 「Units code」：圖層／圖面的單位代碼 |

也就是說，Real 屬性的單位由資料庫與目前單位設定決定，手冊本身不給換算。單位的實務請看[第 3 章](ch03_hierarchy_attributes_zh-TW.reading.html)的「屬性值的單位與格式」一節與專案單位設定。

> **專業提醒：** 把 Real 屬性寫入報表或交換檔之前，一律**標明單位**。尺寸屬性（`DIAM`、`XLEN`、`HEIG`）與 `BORE` 的單位不一定相同，數值相同並不代表量一樣。

## 43.4 各領域型別地圖與代表條目

### 43.4.1 怎麼讀下面的表

下面的表格欄位是：**型別（手冊代碼）｜中文名｜用途｜重要屬性（條目的前幾項或與任務相關者）｜擁有者→成員**。屬性取自條目中實際出現者；「前幾項」指條目順序，不代表重要性排序。擁有者與成員為條目所列的子集（成員太多時只舉代表）。

### 43.4.2 管理層與設備、管路（設計庫）

| 型別 | 中文名 | 用途與重要屬性 | 擁有者 → 成員 |
|---|---|---|---|
| `WORLD` | 世界根節點 | 階層頂端，不能刪除或複製；只有 Name；由 ADMINISTRATION 模組控制 | 無 → 各庫不同（如 `SITE`、`TEAMWORLD`） |
| `SITE` | 場地 | 最大的可建立、刪除、複製、搬移的單位；Function、Purpose、Number、Area、Position、Orientation、Module | `WORLD` → `ZONE`、`BOUNDARY`、`DRAWING`、`GRDMODEL`、`TEXT` |
| `ZONE` | 區域 | 第三層管理元素；Pspec、Ispec、Tspec、DUnion 等；可直接擁有設備、土建、管路 | `APPLDATA`、`SITE`、`ZONE` → `EQUIPMENT`、`PIPE`、`HVAC`、`CWAY`、`CABLE`、`DATUM`、`ZONE` 等二十多種 |
| `TEXT` | 文字 | 通用元素，可放在多數位置，存附加資訊；Stext | 許多型別 → 無 |
| `EQUIPMENT` | 設備 | 容器、泵、換熱器等；29 個屬性，含 Usrweight、Usrcogravity、Desparam、Built、Ispec | `ZONE` → 基本體、`NOZZLE`、`SUBEQUIPMENT`、`ELCONN`、`LOAPOINT` 等 |
| `SUBEQUIPMENT` | 子設備 | 與設備類似，被設備擁有，且不能再擁有子設備 | `EQUIPMENT` → 同設備 |
| `NOZZLE` | 管嘴 | 設備與管路的連接點；Temperature、Pressure、TPressure、Cref、Catref、Height、Angle、Radius | `EQUIPMENT`、`SUBEQUIPMENT`、`TMPLATE` → `DDSE`、`DPSET`、`TMPLATE` |
| `PIPE` | 管 | 一或多個雙端 `BRANCH` 的管理擁有者；Bore、Temperature、Pressure、Pspec、Ispec、Tspec、Matref | `ZONE` → `BRANCH`、`PPLIST`、`PSLIST`、`RESTRAINT`、`TEXT` |
| `BRANCH` | 分支 | 所有有路徑的管路的關鍵元素，由 Head、Tail 與成員序列定義；Hposition、Tposition、Href、Tref | `PIPE`、`HVAC` → 管件、HVAC 元件 |
| `HVAC` | 通風 | 與 `PIPE` 結構相似；42 個屬性，含 Bore、Pspec、Fluref | `ZONE` → `BRANCH`、`HSLIST`、`RESTRAINT`、`TEXT` |
| `RESTRAINT` | 支撐 | 管理 `HANGER` 的行政元素；Hspec、StlRef | `PIPE`、`HVAC`、`ZONE` 等 → `HANGER`、`TEXT` |
| `HANGER` | 管吊架 | 在分支與鋼構之間的雙端元素；Hspec、Hsrod、Htype、Nload | `RESTRAINT` → 吊架元件（`CLEVIS`、`HROD`、`PCLAMP` 等） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕NOZZLE 的幾何：P0 為原點，P1 與 P2 為連接點，HEIGHT 為管嘴高度

*圖 43-3　NOZZLE 條目的示意圖：以 P0、P1、P2 三個連接點與 Height 描述管嘴形狀。（AVEVA 官方文件截圖，僅供內部教學）*

**管件（Piping Component Category，29 型別）** 的條目格式幾乎一致。以 `VALVE` 為例，條目有約 70 個屬性；`FLANGE`（49）、`ELBOW`（50）、`TEE`（52）、`REDUCER`（46）、`GASKET`（46）、`INSTRUMENT`（51）、`ATTACHMENT`（54）的屬性前段都是下列共通欄位：

| 長名稱 | 意義 | 說明 |
|---|---|---|
| Spref | Component spec reference | 指向規格元件 `SPCOM`（外鍵，見 43.4.6） |
| Arrive、Leave | Arrive／Leave Ppoint | 連接點編號（Integer） |
| Lstube | Leave tube reference | 離開側的管子 |
| Cref | Connection reference | 連接的對象（如管嘴） |
| Desparam | Design parameters | 設計參數陣列 |
| Built、Shop、Isohidden | 已建／車間／Iso 隱藏旗標 | Logical |
| Ispec、Tspec | 保溫／伴熱規格參考 | Reference |
| Orrf、Cmpx | 模板來源、比較排除 | 見條目說明 |
| 預製類（Spln、Splt、Ptno 等） | 舊 Spooler 的管段編號 | 條目標為「Old spooler …」 |

這些管件的 Legal Owners 只有 `BRANCH`，Legal Members 為 None。`ATTACHMENT`（`ATTA`）的條目還說明它有三種用途：給吊架接點、標記可標註的特殊點、讓應力分析施加力與力矩。

### 43.4.3 基本體

設備與結構的幾何由基本體組成：`BOX`、`CYLINDER`、`CONE`、`DISH`、`PYRAMID`、`SNOUT`、`CTORUS`、`RTORUS`、`SLCYLINDER`，再加 `POLYHEDRON`、`EXTRUSION`、`REVOLUTION`。每一種都有一個**負體積**版本（前綴 N：`NBOX`、`NCYLINDER` 等），可被正基本體擁有，用來挖空。

> 〔公開版未收錄：AVEVA 官方產品截圖〕BOX 的幾何：XLEN、YLEN、ZLEN 三個尺寸與 P0 到 P6 的點

*圖 43-4　BOX 條目示意圖：以 Xlength、Ylength、Zlength 三個尺寸與 P0～P6 連接點描述長方體。（AVEVA 官方文件截圖，僅供內部教學）*

| 型別 | 中文名 | 重要屬性 | 備註 |
|---|---|---|---|
| `BOX` | 長方體 | Xlength、Ylength、Zlength、Position、Orientation、Level、Obstruction | 擁有者含 `EQUIPMENT`、`STRUCTURE`、`SUBEQUIPMENT`、`TMPLATE` 等；成員為各負基本體 |
| `CYLINDER` | 圓柱 | Diameter、Height | 同上 |
| `NBOX` | 負長方體 | 同 BOX；條目註明 Zlength 須是穿透擁有者表面的那一維 | 只能被正基本體擁有 |
| `POLYHEDRON` | 多面體 | 由 `POLFAC`、`POLOOP` 等定義；11 個屬性 | 條目有完整說明 |

`Level`（繪圖層級）與 `Obstruction`（阻礙等級，供干涉檢查）是基本體共通的兩個整數屬性。

### 43.4.4 結構（Structural）

結構階層比較深，手冊用五張圖表示：STRUCTURE 最上層、SECTION 的成員、Generic Section、Primary Node 與 Panel。

> 〔公開版未收錄：AVEVA 官方產品截圖〕STRUCTURE 最上層：SUBSTRUCTURE、DRAWING、FRAMEWORK、POLYHEDRON、LOAD CASE DESCRIPTOR、ROUTING PLANE GROUP；FRAMEWORK 下可有選用的 SUBFRAMEWORK，再往下有 SECTION、GENERIC SECTION、PRIMARY NODE、PANEL、PANEL LINEAR JOINT

*圖 43-5　結構階層頂層：STRUCTURE 下有 FRAMEWORK，其下（可經 SUBFRAMEWORK）擁有 SECTION、GENERIC SECTION、PRIMARY NODE 與 PANEL。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕SECTION 底下的成員：Section Distributed Load、Section Point Load、Secondary Node、Fitting、Compound Fitting、Section Linear Joint；Secondary Node 下有 Joint、Compound Joint、Release、Nodal Displacement、Nodal Load

*圖 43-6　SECTION 的成員。SECTION 是型鋼，次要節點（SNODE）再擁有接頭、釋放、位移與載荷。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕GENERIC SECTION 底下：SPINE 擁有 POINSP 與 CURVE；JLDATUM 擁有 PLDATUM，再擁有 FIXING

*圖 43-7　Generic Section 的成員：SPINE（脊線）與 JLDATUM／PLDATUM（接頭線基準）。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕PRIMARY NODE 底下：Primary Joint、Release、Nodal Load、Nodal Displacement、Primary Compound Joint、Fixing

*圖 43-8　Primary Node 的成員：主要接頭、釋放、載荷、位移、複合接頭與 Fixing。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕PANEL 底下：Panel Loop、Panel Linear Joint、Panel Fitting、Cofitting、Compound Panel Fitting、negative design primitives

*圖 43-9　Panel 的成員：板的輪廓（Loop）、線性接頭、配件與負基本體。（AVEVA 官方文件截圖，僅供內部教學）*

| 型別 | 中文名 | 重要屬性 | 擁有者 → 成員 |
|---|---|---|---|
| `STRUCTURE` | 結構 | 建築物、管架等；Function、Purpose、Number、Usrweight 等 22 個；不能擁有 Nozzle | `ZONE` → 基本體、`CTWALL`、`HANDRA`、`LADDER`、`SBFRAMEWORK`、`SUBSTRUCTURE` 等 |
| `SBFRAMEWORK` | 子框架 | 把 `FRMW` 再細分；Stspec、Matref、Grade、Firesistance、Ptspec、Inschedule；部分屬性會往成員傳遞 | → `SCTN`、`STWALL`、`WALL`、`SCREED`、`FIXING` 等 |
| `SCTN` | 型鋼斷面 | 40 個屬性：Gtype、Bangle、Posstart、Posend、Joistart 等；**長度是推導值，不存屬性**；斷面由目錄 `PROFILE` 定義 | `CFLOOR`、`CWALL`、`SBFRAMEWORK`、`TMPLATE` → `FITTING`、`SNODE`、`SELJOINT`、`SPLOAD`、`SDLOAD` 等 |
| `SNODE` | 次要節點 | 型鋼之間的「分析」連接點；Zdistance、Fixity、Level | `SCTN`、`STWALL` → `NODISPLACEMENT`、`NOLOAD`、`SJOINT`、`SCOJOINT` 等 |

### 43.4.5 船體相關（四個類別）

船體的條目與管路相比**非常薄**。例如 `HPANEL` 只列 3 個屬性（Name、Description、`SymmEle`），`HPLATE` 5 個，大多數幾何不在這些屬性裡。條目中常見的是變更計數與 Tribon 識別：

| 型別 | 中文名 | 屬性（條目所列） | 擁有者 → 成員 |
|---|---|---|---|
| `HBLWLD` | 船體分段世界 | Name、Description | `WORLD` → `BLOCK` |
| `BLOCK` | 分段 | Function、Purpose、`CHNGD`（變更計數）、Number、`ExtBox`（含偏置的分段包圍盒）；7 個屬性 | `HBLWLD`、`WORLD` → `CPANEL`、`HPANEL` |
| `HPANEL` | 平面板架 | `SymmEle`（對稱側板架參考，非對稱則不設定） | `BLOCK` → `HPLATE`、`HSTIFF`、`HBRCKT`、`HSEAM`、`HHOLE`、`HNOTCH`、`HFLANG`、`HPANBO` 等 |
| `HPLATE` | 平面板架的板 | `CHNGD`、`TBID`（Tribon ID）、Number | `HPANEL` → 無 |
| `HSTIFF` | 平面板架加強材 | Desparam、Spref、`CHNGD`、`TBID`、Number | `HPANEL` → `HPREND`、`HPRCUT`、`HPRHOL`、`HPRNOT` |
| `HBRCKT` | 肘板 | `CHNGD`、`TBID`、Number | `HPANEL` → `HBRABO`、`HBRFLA`、`HBRSTI` |
| `CPANEL` | 曲面板架 | `CHNGD`、`SymmEle` | `BLOCK` → `CPANBO`、`CPNISE`、`CSTIFF` |
| `CPLATE` | 殼板 | `SymmEle`、`HRDPRX`（曲面板架參考） | `CSURPX` → 無 |
| `CSURF` | 曲面 | `CHNGD`、`TBID` | `SSOWLD` → `CCURVE` |
| `CSTIFF` | 殼板加強材 | `SymmEle`、`HRDPRX` | `CPANEL`、`CPROTR`、`HICPAN` → `CPRCUT`、`CPREND`、`CPRHOL`、`CPRMRK`、`CPRNOT` |
| `HIPAN` | 理想化平面板架 | Name、Description、Purpose（FEM 理想化） | `HIBLO` → `HIBOU`、`HIBRA`、`HICUT`、`HIHOL`、`HIPLA` 等 |
| `MWELD` | 焊縫 | 21 個：`Wlen`、`Wlegl`、`Wproc`、`WldPos`、`WnLay`、`WcAng` 等 | `MWLDJT` → 無 |
| `MPLATE`（Manu 庫） | 板件 | 47 個：`BrnLen`、`BlsLen`、`Curved`、`Bent`、`Corrug` 等製造量值 | `MPKGFL` → 無 |

這幾頁反映一個事實：Dabacon 中的船體元素主要是**識別用的外殼**，詳細的板形、孔、邊界由船體系統維護，並透過偽屬性（Hull 類別，見 43.5）計算出來。想改船體，仍要走船體模組，而不是直接寫屬性。船體概念請看[第 36 章](ch36_hull_concepts_zh-TW.reading.html)。

> **專業提醒：** `CHNGD`（變更計數）與 `TBID`（Tribon ID）是船體條目最常見的兩個屬性，適合拿來做「這塊板有沒有變過」的差異比對；但它們是系統維護的，工具不要寫入。

### 43.4.6 目錄庫（Catalogue）

目錄庫的關鍵是一條「規格 → 元件 → 點／幾何／資料」的鏈：

| 型別 | 中文名 | 重要屬性 | 擁有者 → 成員 |
|---|---|---|---|
| `CATALOGUE` | 目錄 DB 元素 | Purpose、Cstandard | `WORLD` → `BTSET`、`STSECTION`、`TEXT` |
| `SPECIFICATION` | 規格 | Matref、Fluref、Rating、Linetype、Nomreference（口徑表）、Pdareference 等 26 項 | `SPWLD` → `SELEC`、`SPCOMPONENT` |
| `SPCOMPONENT` | 規格元件（`SPCOM`） | `Catref`（目錄參考）、`Cmpref`、`Bltref`、Matref、`Tmpref`、`Pdareference` | `SELEC`、`SPECIFICATION` → 無 |
| `SCOMPONENT` | 目錄元件 | `Ptref`（點集）、`Gmref`（幾何集）、`Dtref`（資料集）、Gtype、Param | `CATEGORY`、`BTSET` → 無 |
| `PTSET` | 3D 點集 | Gtype、Skey | → `PTCAR`、`PTAXIS`、`PTMIX`、`PTPOS` |
| `PTCAR` | 笛卡兒 Ppoint | Pconnect、Pbore、Px、Py、Pz、Direction、Pskey | `PTSET` → 無 |
| `GMSET` | 3D 幾何集 | Gtype、Skey | → `SBOX`、`SCYLINDER`、`SCONE`、`LINE` 等 |
| `DTSET` / `DATA` | 資料集／資料 | `Dkey`、`Ptype`、`Pproperty`、`Dproperty`、`Punits`、`Lhide` | `DTSET` → `DATA` |
| `NOMINB` | 公稱口徑 | `Incbore`、`MMbore` | `NBRWLD` → 無 |

這條鏈對應設計庫的 `Spref` → `SPCOM` → `Catref` → `SCOMPONENT` → `Ptref`／`Gmref`／`Dtref`。手冊不畫這張圖，但條目中的 Reference 屬性把它串起來，如[第 3 章](ch03_hierarchy_attributes_zh-TW.reading.html)的外鍵圖。

### 43.4.7 Draft、系統、字典與其他庫

| 型別 | 庫 | 中文名 | 重要屬性 | 擁有者 → 成員 |
|---|---|---|---|---|
| `DRWG` | Draft | 圖面 | Date、Size、Font、Rrsf（Rep 規則集）、Hrsf（影線規則集）、Layarf、Laydrf 等 52 項 | `REGISTRY` → `SHEET`、`LIBY`、`REVISION`、`TASK` |
| `SHEET` | Draft | 圖紙 | Size、Bsrf（底圖）、Idlname（Drawlist）、Title 等 31 項 | `DRWG` → `VIEW`、`NOTE`、`OLAYER`、`VMSUBV` |
| `VIEW` | Draft | 視圖 | Direction、Vscale、Vtype、Rrsf、Hrsf、Crsf 等 42 項 | `SHEET` 等 → `LAYER`、`RRULE`、`HRULE`、`VSECTION` |
| `LAYER` | Draft | 視圖標註圖層 | 66 項：Lvisibility、Font、Tpen、Dlpen 等 | `VIEW` → `LDIMENSION`、`GLABEL`、`SLABEL`、`TAGRULE` 等 |
| `LDIMENSION` | Draft | 線性尺寸 | Direction、Doffset、Dposition、Dterminator 等 48 項 | `LAYER` → `DPOINT`、`DPPT`、`DPBA` |
| `USER` | System | 使用者 | Password、Security、Acrli（指派的 ACR） | `USERWORLD` → `EXTLI`、`TMLI` |
| `TEAM` | System | 團隊 | Teastatus | `TEAMWORLD` → `DBLI` |
| `DB` | System／Global | 資料庫 | Numbdb、Fino、Accessdb、Claimdb、LCtrolled、LVariant、ExtNo、ExtOwner | `DBLI`、`EXTLI` → 無 |
| `MDB` | System | 多資料庫 | Dbls（所屬 DB）、Curdbs（目前 DB） | `MDBW` → `DB` |
| `UDA` | Dictionary | 使用者自訂屬性 | Ukey、Utype、Ulength、Uunits、Elelist 等 23 項 | `UGROUP`、`UWRLD` → `ULIMIT`、`UVALID` |
| `UDET` | Dictionary | 使用者自訂元素型別 | BaseTy、UDMList、UDOList、UDHLIS | `UDETGR`、`UDETWL` → 無 |
| `ASMBLY` | Design（Assembly） | 組裝 | AsName、AsWLoc、AsBuil、AsBPan、AsEWei、AsECoG | `ASMBLY`、`ASWLD` → `ASITEM`、`ASMBLY` |
| `GRIDAXIS` | Design（Grid） | 格線軸 | GRDAXE、GRDLBL | `GRIDSYSTEM` → `GRIDLN` |
| `CWAY`／`CABLE` | Design（Cabling） | 電纜路徑／電纜 | Function、Purpose、Position；`CABLE` 另有 Spref、FEQDES、TEQDES 等 24 項 | `ZONE` → `CWBRAN`；`CORE`、`RPATH` 等 |
| `LADDER` | Design | 梯 | Matref、FireRating、ORise、OGoing、Rise、RWidth 等 25 項 | `DETGRP`、`STRUCTURE` → `HANDRA`、`LDRCAGE`、`LDRRUN` 等 |
| `ROOM` | Design（Accommodation） | 房間 | Heidefault、FlrHeight、ClnHeight、OccType 等 48 項 | `BLEVEL`、`STRUCTURE` 等 → 多種 |
| `PPIECE` | Design（Pipe Piece） | 管件預製片 | BENDMC、STOCKL 等 20 項 | `PPLIST` → 無 |
| `SPOOL` | Spooler | 管段 | Splprefix、Splnumber、Spltbl | `SPLDRG`、`SPLTMP` → 無 |
| `SCEQUIPMENT` | Schematic | 示意設備 | Distag、Prefix、Number、Suffix、Scsysf 等 27 項 | `SCGROUP` → `SCNOZZLE`、`SCSUBEQUIPMENT`、`TEXT` |
| `FLUID` | Property | 流體材料 | Name、Description；成員有密度、膨脹係數、楊氏模數等表 | `MATWORLD` → `TDENSITY`、`TEXPANSION`、`TYOUNG` 等 |

> `DRWG` 擁有者是 `REGISTRY`（Draft 庫）；`Rrsf`、`Hrsf`、`Crsf` 分別指向表示規則、影線規則、變更規則集，Draft 的使用請見[第 31 章](ch31_draft_admin_production_zh-TW.reading.html)。

**常見錯誤：** 把 `SPCOMPONENT`（規格元件，指向目錄）與 `SCOMPONENT`（目錄元件，擁有點／幾何／資料參考）搞混；兩者只差一個字母，卻在不同階層。`SPCOM` 的 `Catref` 是進入 `SCOMPONENT` 的入口。

## 43.5 偽屬性

### 43.5.1 怎麼找

手冊的 Pseudo Attributes 章依**用途分成 67 個類別**，每頁是一張 Attribute Name／Data Type／Qualifier／Description 的表。

| 類別（頁名） | 代表偽屬性（取樣） | 用途 |
|---|---|---|
| Positional | `POS`、`ORI`、`WVOL`、`EVOL`、`POSX`、`POSU`、`POSN`、`GRDPOS` | 位置與座標分量 |
| Name Related | `FLNN`、`FLNM`、`NAMN`、`ISNAMED`、`NAMETY`、`NAMESQ` | 名稱的各種格式 |
| Element Type Related | `TYPE`、`ACTTYPE`、`FULLT`、`OSTYPE`、`TYSEQU`、`AHLIS` | 型別與序號 |
| Data Model | `LIST`、`OLIS`、`HLIS`、`LLIS`、`DLIST` | 合法成員、擁有者、階層內可能型別 |
| Attribute Related | `ATTLIST`、`ATTOUT`、`ATTRAW`、`PSATTS`、`UDALIS`、`UDASET` | 屬性清單 |
| Database | `DBAC`、`DBCL`、`DBNA`、`DBNU`、`DBTY`、`DBREF`、`DBWRITE` | 元素所在資料庫 |
| Claim Related | `LCLM`、`CLMNUM`、`CLMID`、`OKCLA`、`OKREL` | 認領狀態 |
| Allowed Operation | `DACCLA`、`DACCRE`、`DACDEL`、`DACMOD`、`MODATT`、`MODERR` | 能不能做某操作 |
| Change History | `ELEMOD`、`ELECRE`、`ELEDEL`、`CRDATE`、`CRUSER`、`ATTMOD` | 變更與建立歷史 |
| Mass Properties | `GWEI`、`NWEI`、`GVOL`、`GCOF`、`DNST` | 重量、體積、重心、慣性矩 |
| Spatial | `WVOL`、`LVOL`、`CSGBOX`、`GTAREAS` | 包圍盒與所在區域 |
| Status Related | `STVNAM`、`STVNUM`、`STVLST`、`STVTRV` | Status 值與可轉換狀態 |
| Catalog Values for Design Item | `CATR`、`GMRE`、`CPAR`、`APAR`、`DTXR`、`MATR` | 設計元素取得的目錄值 |
| Catalog Values for Piping Item | `ABOR`、`ACON`、`APOS`、`ADIR`、`AOD`、`ATWALL` | 管件的 Arrive／Leave 端值 |
| Design Parameters | `ADESP`、`DDESP`、`ODESP`、`WDESP` | 設計參數的各種版本 |
| Rules Related | `RCOU`、`NRULEE`、`RULSET`、`DEPATT` | 規則數量與錯誤 |
| Hull | `BEVEL`、`CMBOX`、`CMCAT`、`CMFLW`、`ATWLEN` 等 | 船體計算值（頁面很長，約 17,000 字元） |
| Draft ×6、Schematic、SPOOLER、Stairs、Cabling… | 各專業計算值 | 各專業用 |

另有其他類別，如 Global、Lexicon、Link Related、Pline Related、PPoint Related、Piping Specification、Project Copy、Space Management 等，本章未逐一展開。

此外，`Pseudo Attributes` 章首頁本身還列出一批未分類的屬性（`ALIST`、`UUID`、`UUIDREF`、`XRLIST` 等）。

### 43.5.2 實用偽屬性速查

| 偽屬性 | 型別 | 說明 | 用途 |
|---|---|---|---|
| `FLNN` | string(700) | 完整名稱（不含開頭 `/`） | 報表、輸出 |
| `TYPE` | word | 型別，截為 4 或 6 字元 | 型別比對 |
| `FULLT` | string | 完整型別 | 型別比對 |
| `DBREF` | element | DB reference | 內部識別 |
| `LOCK` | logical | 元素是否鎖定 | 檢查 |
| `WVOL` | real(6) | 世界座標包圍盒 | 空間查詢 |
| `LIST` | word(2000) | 所有可能成員型別 | 查合法成員 |
| `OLIS` | word(2000) | 所有可能擁有者型別 | 查合法擁有者 |
| `ATTLIST` | word(2000) | 元素全部屬性 | 屬性探索 |
| `ATTOUT` | word(2000) | 排除隱藏屬性（即 `Q ATT` 的輸出） | 屬性探索 |
| `PSATTS` | word(500) | 偽屬性清單 | 偽屬性探索 |
| `UDALIS` | word(2000) | UDA 清單 | UDA 探索 |
| `LCLM` | logical | 元素是否被認領 | 寫入前檢查 |
| `DACMOD` | logical，qualifier attr | DAC 是否允許改某屬性 | 權限檢查 |
| `MODATT` | logical，qualifier attr | 某屬性能否被修改 | 寫入前檢查 |
| `MODERR` | string(120)，qualifier attr | 修改失敗時的錯誤文字 | 診斷 |
| `GWEI`、`NWEI` | real | 毛重、淨重 | 重量報表 |
| `CATR` | element | 目錄參考 | 沿鏈查目錄 |

> 本課程在 ch3 提到的 `LASTMOD`，**這次在 12.1 的屬性總表中搜尋不到**（搜尋縮寫 `LAST` 與全名皆無）。Change History 類別提供的是 `ELEMOD`、`ATTMOD`、`CRDATE`、`CRUSER` 等。若要查「最後修改」，改用這些，並在實際系統驗證〔待核對〕。

> **專業提醒：** 偽屬性是**查詢時計算**的，不存在資料庫中，也不能當成穩定的歷史欄位。`Q ATT` 不列偽屬性；要看用 `Q PSATTS`。重量與體積類偽屬性對大量元素計算昂貴，批次報表前先小範圍測試。

## 43.6 使用者自訂屬性（UDA）

### 43.6.1 命名與定義位置

簡介頁說明：元素除標準屬性外，可有一或多個 UDA；設定與使用方式相同，但**名稱以冒號 `:` 開頭**。詳細定義方式交給 Administration 的 LEXICON 文件。

UDA 本身是 Dictionary 庫裡的元素。`UDA` 條目（23 個屬性）的幾個關鍵欄位：

| 屬性 | 意義 | 說明 |
|---|---|---|
| Utype | Type of attribute value | 值的型別 |
| Ulength | Length of data or text | 長度 |
| Uunits | Units of attribute values (bore/distance/text) | 單位類別 |
| Elelist | Types of elements (including UDETs) to which this attribute applies | 套用到哪些型別 |
| Reflist | 參考型 UDA 可指向的型別 | 參考範圍 |
| Dflt | 預設值 | |
| Upseud | 設為 true 時計算值而非存入資料庫，需提供使用者程式碼 | 「偽」UDA |
| Uprote | 設為 true 則在受保護資料庫中不能檢視 | |
| Uhide、Uteams | 隱藏屬性、哪些 Team 看得到 | |
| Uhyper | 把值當成外部資源的具名連結 | |
| Udname | 使用者自訂名稱 | 即冒號後的名稱 |
| Udpend | 依賴的其他屬性 | |

限制值放在 `ULIMIT`（`Umin`、`Umax`），合法值清單放在 `UVALID`（`Uvval`），兩者都是 `UDA` 的成員。`UDET`（使用者自訂元素型別）用 `BaseTy` 指定基底型別，並以 `UDMList`、`UDOList` 定義允許的成員與擁有者型別。

### 43.6.2 與標準屬性的差別

| 面向 | 標準屬性 | UDA |
|---|---|---|
| 名稱 | 無前綴 | 以 `:` 開頭 |
| 定義 | 資料模型（DMRM） | 專案的 Dictionary 庫（LEXICON） |
| 手冊是否列出 | 是 | **否**：每個專案不同 |
| 可算值 | 偽屬性 | `Upseud` 為 true 的 UDA |
| 查詢 | `Q ATT` | `Q UDALIS`、`Q UDASET` |

> **專業提醒：** UDA 定義在專案內，**DMRM 不會有你公司的 UDA**。每個專案先用 `Q UDALIS` 查出實際清單，再寫程式。UDA 名稱 `:` 開頭的 PML 寫法見第 12 章，那裡標為〔寫法待核對〕。

## 43.7 與 PML／.NET 取值的關係

### 43.7.1 DMRM 在程式中的位置

DMRM 的 Assumptions 說這本書是給需要寫批次巨集或客製 GUI 的使用者；PML 語法本身在 Software Customization（手冊內明指，並說完整屬性與偽屬性清單可在該處查）。換句話說：

- **DMRM 回答「資料庫裡有什麼」**（型別、屬性、型別、擁有關係）；
- **PML 手冊回答「怎麼取出來」**；
- 本課程第 12 章已經收錄 PML 取值的寫法，本章不重複。

### 43.7.2 資料型別怎麼對應

下表混合了手冊的資料型別與第 12 章已列的 PML 取值結果；沒有出現在第 12 章的對應標為〔待核對〕。

| DMRM 資料型別 | PML 取值（第 12 章） | 備註 |
|---|---|---|
| string(n) | `!e.desc` → STRING | 超長字串依屬性上限 |
| real | REAL | 單位依專案設定 |
| integer | REAL（PML 數值型別）〔待核對〕 | |
| logical | BOOLEAN〔待核對〕 | |
| word | STRING 或 WORD〔待核對〕 | 寫入前驗證長度 |
| element | DBREF | 可能是 NULREF，要先判斷 |
| pos | POSITION | `!e.position` |
| ori | ORIENTATION〔待核對〕 | |
| real(n)、element(n) | ARRAY〔待核對〕 | `!e.members` 回傳陣列 |

### 43.7.3 實務查詢範例（只讀）

以下範例的寫法都有依據：`Q ATT`、`Q PSATTS`、`Q UDALIS` 見簡介頁與偽屬性頁說明；PML 的 `.flnn`、`.type`、`.owner`、`.members` 見第 12 章。命令列輸出格式依實際系統〔待核對〕。

**範例 1：先確認元素有什麼屬性**

```
Q TYPE
Q ATT
Q PSATTS
Q UDALIS
```

`Q ATT` 的輸出等於偽屬性 `ATTOUT`（排除隱藏屬性）；`PSATTS` 列出偽屬性；`UDALIS` 列出 UDA。

**範例 2：確認合法擁有者與成員**

```
Q OLIS
Q LIST
```

`OLIS` 是「所有可能擁有者型別」，`LIST` 是「所有可能成員型別」（Data Model 類別）。建立元素前先查它，比猜更可靠。

**範例 3：寫入前的檢查**

```
Q LCLM
Q DBWRITE
```

`LCLM` 是「元素是否被認領」，`DBWRITE` 是「是否在可寫入的 DB」。兩個都是偽屬性（Claim Related、Database 類別）；寫入前用 `MODATT`（需給屬性名稱當 qualifier，語法〔待核對〕）再確認。

**範例 4：PML 中讀取（沿用第 12 章）**

```pml
!e = !!ce
!n   = !e.flnn
!t   = !e.type
!own = !e.owner
!kids = !e.members
```

> **專業提醒：** DMRM 的屬性清單可能比你所在專案實際可用的多。實務流程是**先在訓練專案用 `Q ATT` 驗證，再把屬性名稱寫進程式**，而且寫程式用完整名稱（見第 12 章）。

### 43.7.4 .NET 與其他取值路徑

本次取材的 DMRM 沒有 .NET 內容。.NET 與資料模型的關係應查 .NET 客製化相關章節，不在本章範圍〔待核對〕。

## 43.8 手冊的限制與陷阱

| 現象 | 說明 | 建議 |
|---|---|---|
| 船體條目很薄 | `HPANEL` 只列 3 個屬性；多數船體資訊透過偽屬性計算 | 以偽屬性 Hull 類別與船體模組為主；見第 36 章 |
| 轉檔缺漏 | 部分條目（如 `SBFRAMEWORK`、`NBOX`、`SCTN`）的擁有者／成員列中出現「Global tab」字樣，原頁面應是分頁內容未轉出 | 用 `Q OLIS`、`Q LIST` 在系統上確認 |
| 描述空白 | 許多條目 Description 為空（如 `BOX`、`HPLATE`） | 看屬性與擁有關係，或查其他手冊 |
| 長名稱與縮寫不一致 | 見 43.2.4 | 以 `Q ATT` 實測 |
| 沿用 PDMS 名稱 | `USER` 條目稱「PDMS User Element」 | 閱讀時自行換算 |
| 版本差異 | 12.1 與 E3D 2.1／3.1 的屬性、型別字元上限可能不同；`LASTMOD` 在 12.1 總表未見 | 以 12.1 實測為準 |
| 無單位表 | 見 43.3.3 | 以專案單位設定為準 |
| 廢止標記 | 部分偽屬性（如 `OKCLA`、`OKCLH`）註明已廢止且恆回傳 True | 不要用來做權限判斷 |

## 43.9 本章小結

1. DMRM 是字典，不是教學書：依資料庫分章，每個型別一頁，內含描述、屬性、合法擁有者與合法成員；設計庫約 500 型別，是最大的一章。
2. 屬性分一般與特殊兩類；另有偽屬性（67 類，查詢時計算）與 UDA（冒號開頭，專案自訂，手冊不列）。
3. 屬性資料型別包括 Name、Real、Integer、Reference、Logical、Word、String、Datetime，與三種陣列、Noclaim；總表的 `real(6)`、`element(500)` 記法標示陣列上限。
4. 型別條目用長名稱，總表與命令列用縮寫，兩者沒有統一轉換規則；查詢要以 `Q ATT` 實測。
5. 階層是設計核心：WORLD → SITE → ZONE → EQUIPMENT／PIPE／STRUCTURE／HVAC；PIPE → BRANCH → 管件；EQUIPMENT → NOZZLE；STRUCTURE → FRAMEWORK → SECTION。
6. 目錄鏈：`Spref` → `SPCOM` → `Catref` → `SCOMPONENT` → 點集、幾何集、資料集。
7. 船體條目很薄，多為 `CHNGD`、`TBID` 識別與計算偽屬性；寫入走船體模組。
8. 合法成員與擁有者用 `Q LIST`、`Q OLIS` 實測最穩；寫入前查 `LCLM`、`DBWRITE`、`MODATT`。
9. 手冊不講單位，單位看專案設定。

## 43.10 練習題／自我檢核

**練習（訓練專案，唯讀）**

1. 選一個 `EQUIPMENT`，執行 `Q ATT`，把結果與 DMRM 的 `EQUIPMENT` 條目對照：哪些屬性條目有、命令列沒列？哪些相反？
2. 在 `BRANCH` 上執行 `Q LIST`，與條目 Legal Members 比對。
3. 找出 5 個長名稱與縮寫不同的屬性，做成對照表（如 `Spref`／`SPRE`）。
4. 對一個管件執行 `Q SPRE`，再沿 `Catref` 找到 `SCOMPONENT`，查它的 `Ptref`、`Gmref`、`Dtref`（需要目錄庫在目前 MDB 中）。
5. 在 `PSATTS` 輸出中選 3 個偽屬性，到 Pseudo Attributes 章找出它們屬於哪個類別。
6. 用 `Q UDALIS` 看專案 UDA；找到一個，查它在 Dictionary 庫中的 `Utype`、`Elelist`。
7. 對一塊板（若有）查 `Q ATT`，觀察船體條目為何屬性少（見 43.4.5）。

**自我檢核**

- [ ] 我能說出 DMRM 的主要分區，並知道設計庫有多少個類別。
- [ ] 我能讀懂一個型別條目的四個部分。
- [ ] 我知道 Word 型屬性有長度限制，過長會截斷（見 ch3）。
- [ ] 我能說明偽屬性與 UDA 的差別，並知道去哪裡查。
- [ ] 我知道條目長名稱與總表縮寫不能互相推導。
- [ ] 我知道 `Q LIST`、`Q OLIS` 可以查合法成員與擁有者。
- [ ] 我知道手冊沒有單位表，也知道船體條目很薄。

## 43.11 〔待核對〕彙整

1. `Name` 型長度：簡介頁 51 字元，總表 `NAME` 為 `string(500)`。
2. `Word` 型長度：簡介頁 4 字元；ch3 引用的版本說 4 或 6 字元；`TYPE` 說截為 4 或 6。
3. `TYPE` 回傳的型別代碼與條目標題代碼的對應（如 `EQUIPMENT` 對 `EQUI`）。
4. `LASTMOD` 在 12.1 是否存在（總表未見）。
5. 命令列對 qualifier 型偽屬性（`ELEMOD`、`MODATT` 等）的語法。
6. PML 中 integer、logical、word、ori、陣列型的對應型別。
7. UDA 在 PML 的 `:` 寫法（見第 12 章）。
8. 條目中「Global tab」缺漏處的實際擁有者／成員。
9. 命令列 `Q` 輸出的實際格式。
10. .NET 取值與資料模型的關係，本次未取材。

## 43.12 資料來源與取材範圍

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

與資料庫管理（Database Management）、SQL Direct、Status Control 有關的內容在第 42 章。
