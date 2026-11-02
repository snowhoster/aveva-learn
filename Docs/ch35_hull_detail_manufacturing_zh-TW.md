# 第 35 章　船體詳細設計（三）：製造資訊與鐵舾裝生產特徵

> 第 33、34 章處理了船體詳細設計的建模面（初始化、平面與曲面建模）。這一章處理「模型之後」：**Manufacturing（製造）** 把船體模型變成工廠拿得到的東西，包括板零件與型材零件、位置編號、套料與切割資料、型材草圖與製造清單、彎曲樣板與胎架（Jig）、焊接機器人資料；接著是 **Production Features for Outfit Steel（鐵舾裝生產特徵）**，說明舾裝鋼（FRMW／SBFR）怎樣丟進船體生產流程；最後是 **F1 - Help Texts**，也就是初始化用的 TIL 介面與檔案檢查表單的說明。
>
> 第 6 章已用概念層次講過「模型到生產資料」的管線、套料利用率與型材草圖；第 15 章談 Vitesse 與資料抽取；第 28 章談 Weld Planning 與 Factory Automation。本章**不重複**這些，只補官方 Manufacturing 章節中它們沒講到的細節：每個程式的 Job Launcher 設定、環境變數、IP／Restriction 檔、輸入語言、輸出資料庫與清單。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件 Hull Detailed Design 之 *Manufacturing*（約 650 頁）、*Production Features for Outfit Steel*（約 18 頁）、*F1 - Help Texts*（約 70 頁）。官方頁面是 Tribon 時代 M3 的使用者手冊沿用，所以大量出現 `sf416d`、`SB_PLDB`、Job Launcher 等舊式名稱，本章照原樣保留。文件**幾乎沒有 PML 範例**，唯一有程式介面的地方是 Vitesse（Python）的 `trig_hull_endcut_dim` 觸發器與自動套料 Plug-In（C++ DLL）；其他「怎麼接」一律標〔待核對〕。官方機器翻譯譯名生硬（例如把 Nesting 譯為「嵌套」、Burner 譯為「燒嘴」），本章改用台灣造船業慣用詞（套料、切割）。取材範圍與未讀子樹見章末。

## 35.1 學習目標

讀完本章，你應該能夠：

1. 說明 Production Program Interface（PPI）的三步驟（選取、執行、顯示），並使用選取工具與篩選條件。
2. 說明平面零件（`sf416d`）與曲面零件（`sf831d`）自動產生程式的輸入、IP 檔與輸出資料庫（`SB_PLDB`、`SBH_PROFDB`）。
3. 說明 Autopos 位置編號的規則物件、`CASE`／`BUNDLE`／`SORT` 與執行用的 `SCOPE`／`OVERWRITE`／`LIST_ONLY` 陳述。
4. 說明板材套料系統的元件、概念（橋、起點、輔助功能、自動重新套料、剩料）與資料庫、預設檔、燒嘴資料。
5. 說明套料到切割資料的鏈：Generic File（`.gen`）→ Generic Post Processor（GPP）的預設檔與 Kerf 檔。
6. 說明 3 軸燒嘴、型材套料、Panel Line Control（PLCM）各自處理的對象與設定檔。
7. 說明型材製造輸出：草圖、製造清單、彎曲資訊、端切尺寸標註與 `trig_hull_endcut_dim` 觸發器。
8. 說明曲面板製造資訊：胎架柱（Jig Pillars）、板胎架（Plate Jigs）與五種彎曲樣板。
9. 說明鐵舾裝（FRMW／SBFR）轉進船體生產所需的目錄設定（`SFCODE`、`TRCLIN`）、`PDNAME`／`OPTBLO` 與倒角、餘量的設定方式。
10. 說明 F1 Help Texts 中 TIL Interface／File Check Interface 的用法，以及零件名稱精靈與製造資料的對應。

## 35.2 製造資料全貌與 Production Program Interface

### 35.2.1 Manufacturing 子樹的地圖

官方 Manufacturing 章節的第一層可整理為下表。所謂「對象」是這個功能處理的船體資料；「程式」是官方記載的執行檔名（透過 Job Launcher，簡稱 JL，啟動）。

| 子章節 | 對象 | 主要輸出 | 官方程式名稱 |
|---|---|---|---|
| Plane Panel Parts | 平面板（含肘板） | 板零件、型材零件、收據清單、零件草圖 | `sf416d` |
| Auto Generation of Curved Parts | 曲面板（已展開） | 加入劃線與收縮量的展開板、殼板加強材 | `sf831d` |
| Auto Generation Number Setting | 板零件 | 位置編號（Autopos） | 見 35.4 |
| Hull Nesting | 板、型材、組立 | 套料板、Burning Sketch、Generic File | 板：互動式；3 軸 `sf623d`；型材 `sf605d`；單件 `se016` |
| Generic Postprocessor | Generic File | 機器控制碼（NC） | GPP（SF 001） |
| Manufacturing Curved Plates | 曲面板 | 胎架柱、板胎架、彎曲樣板 | `sf824d`、`sf821d` |
| Plate Manufacturing | 板、組立 | 焊接機器人中性檔、Generic File | `pg101`、`TbGeneric2Plate` |
| Profile Manufacturing | 型材 | 型材草圖、製造清單、切割資料 | Profile Interface／Profile Cutting Interface |
| Hull Production Program Interface | 全部 | 選取與呼叫統一入口 | PPI |

### 35.2.2 PPI：選取、執行、顯示

官方把所有製造與報表功能的共通做法歸納成三步：**(a) 選取**要處理的對象，**(b) 執行**生產或報表功能，**(c) 顯示**結果。製造程式本身（平面零件、曲面零件、型材清單、3 軸套料……）的輸入「通常是由 PPI 自動產生」，使用者不需要自己寫輸入檔。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Production interface 起始選單：Select、Show、Plane Part Generation、Parts List、Material List、Profile Sketch and List、Profile Nesting、Profile Cutting、Weight and COG、Curved Part Generation、Bending Templates and Jigs、Interfaces
*圖 35-1　PPI 起始選單。尚未選取時多數功能反灰，選取之後才會啟用。（AVEVA 官方文件截圖，僅供內部教學）*

選取工具（General Selection Tool）可以在下列層級選取：Block、Assembly、Panel、Plate、Profile、Graphical、Nested Profile、Nested Plate、Framework（鐵舾裝框架）與 Manufacturing Package。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Production data selection 表單：Block、Assembly、Panel、Plate、Profile、Graphical、Nested Profile、Nested Plate、Filter、List、Framework、Manu Package、Reset
*圖 35-2　General Selection Tool 的選取表單。（AVEVA 官方文件截圖，僅供內部教學）*

篩選器（Filter）可依日期（Date Before／Since）、舷別、材質（Quality）、板厚、「尚未套料（Not nested）」與各種型材條件過濾，另有 Exclude（排除）與 Apply to all（套用到全部）。官方的範例：要選一個 Block 內「除了某材質以外」的所有板，要分兩次選取，先不加篩選選整個 Block，再用「Quality + Exclude」選一次。

| PPI 機制 | 說明 |
|---|---|
| 目前選取（current selection） | 選取後會保留，可被後續多個功能共用 |
| IP 檔群組 | 副檔名 `.IP` 的預設檔可加 `START_GROUP_<名稱>,` … `END_GROUP,`，執行時選擇要套用哪一組關鍵字 |
| 草圖自動命名 | 由 `SBH_DWGNAME_RULES` 指定的規則檔決定，規則以應用代號起頭 |

命名規則的應用代號包括 `PPAN`（平面零件）、`CPAN`（曲面零件）、`PART_PLATE`、`PART_PROFILE`、`WCOG`（重量與重心）、`PROF_SKETCH`、`COMB_PSKETCH`、`PLATE_NES…`（套料）、`BENDTPL`（彎曲樣板）等。預設規則例如平面零件為 `/DELIM='PPAN_' /COMPUTER=7 /DELIM='_' /JOBNO`。限制：`/COUNTNO` 只能用於 `PROF_SKETCH`、`COMB_PSKETCH`、`BENDTPL`。

> **專業提醒：** 「選取」是狀態，不是參數。製造程式吃的是 PPI 當下保留的選取，所以開發者若要批次觸發（見 35.12），務必先確認選取內容，否則可能對上一次選到的東西重跑。

### 常見錯誤

- 以為每個製造程式要自己準備輸入檔。實際上由 PPI 產生；只有 Jig Pillar、Plate Jigs 與 3 軸套料有可手寫的 TIL 輸入語言（35.8、35.6）。

## 35.3 平面零件與曲面零件的自動產生

### 35.3.1 Plane Panel Parts（`sf416d`）

這個功能把結構資料庫中的**平面板拆成個別的板零件**，並選擇性地拆出型材零件；肘板（Bracket）上的板與型材也比照處理，同時自動計算劃線（Marking）。

| 項目 | 內容 |
|---|---|
| JL 名稱 | Plane Part Generation |
| 輸入 | `SB_INPUT1`（`.dat`，通常由 PPI 產生） |
| 執行時輸出 | `SB_OUTPUT1`（`.log`，作為第一個輸出檔） |
| 預設檔 | `ppanparts.ip`，固定檔名，放在 `SB_SHIP` 指向的目錄 |
| 板資料庫 | `SB_PLDB`：實際寫入孔、切口與缺口幾何；接縫穿過切口、餘量與坡口缺口的處理順序都由程式處理 |
| 型材資料庫 | `SBH_PROFDB`：若有定義才寫入型材零件；可選擇把型材轉成板零件（見官方 Setup for Production / Conversion of Profiles to Plates，本章未展開） |
| 收據清單 | `ppanparts_<job No.>.lst`，位於專案的 print 目錄；列出每個板的零件名稱、是否為新零件、劃線資訊（`NOMARKLIST` 可關閉） |
| 紀錄檔 | 嚴重錯誤才有內容，例如 `INCORRECT IP`、`<dname> MISSING`；預設檔有錯整個程式會中止 |
| 圖面 | `PPAN_<job No.>`，存在 `SBH_PPART_DWG` 與 `SBH_PPART_DWG_PADD` 指定的 PADD 資料庫，每個板零件一張草圖 |

`ppanparts.ip` 的關鍵字很多（`ADD_LABELS`、`ADD_ASS_BRA_LABELS`、`ADD_KNU_MARKING`、`ADD_BEVEL_DETAILS`、`ATTACH_ANGLE`、`ATTACH_TYPE` 等），細節請查官方原頁；本章不逐一整理〔待核對：實際可用關鍵字依版本〕。環境變數方面，通用的有 `SB_HREF`（Hull Reference 物件名）、`SB_SREF`（Structure Reference 名）、`SB_YARD`（船廠名，會印在清單上），

> 〔公開版未收錄：AVEVA 官方產品截圖〕平面零件結果：一塊帶有四根加強材切口、劃線與文字標示的板零件草圖，板厚 TH=12.0
*圖 35-3　平面零件產生的結果：板外形含缺口，並自動加上劃線與標示文字。（AVEVA 官方文件截圖，僅供內部教學）*

### 35.3.2 Auto Generation of Curved Parts（`sf831d`）

曲面板在建模時定義展開後，這個程式**自動加入劃線、收縮量（shrinkage）**，並把展開板與殼板加強材「放行」給生產。

| 項目 | 內容 |
|---|---|
| JL 名稱 | Hull Curved Part Gen. |
| IP 檔 | `cpanparts.ip`（放 `SB_SHIP`），可設 `ATTACH_ANGLE`、`ATTACH_TYPE`（`MARKSIDE`／`NON_MARKSIDE`／`ACUTE`）、`ATTACH_TOL`、`ATTACH_DIST`、`ATTACH_LEG`、`NOMINALCONTOUR`、`OPTIMIZECONTOUR` 等 |
| 劃線行為 | `SBH_TRACE_OLD` 設任何值＝劃線不考慮角隅切口，維持舊行為；`SBH_OLD_TEMPL_MARK` 保留舊的樣板劃線行為 |
| 追加劃線 | 執行時若對「Additional curves to be marked?」回答 Yes，可再選取額外曲線 |
| 輸出 | 板存入 `SB_PLDB`；殼板加強材以生產物件存入 `SBH_PROFDB` |
| 圖面 | 存入 `SBH_CPART_DWG`／`SBH_CPART_DWG_PADD` 指定的 PADD；沒設 PADD 時嘗試存到標準圖所在的 `SB_PDB_PADD` |

展開板在套料時會自動轉成套料用格式，劃線曲線可依 `SBH_DEVOBJ_IP` 指向的 IP 檔加上識別（`CURVEIDENT`、`MARKGAP`、`TEXTHEIGHT`、`MATERIALSYMBOL`、`TEMPLATE` 等）；此 IP 檔同時作用於曲面零件、Plate Interface 與板套料。

> **專業提醒：** 這些程式的路徑與資料庫全由**環境變數**決定（`SB_SHIP`、`SB_PLDB`、`SBH_PROFDB`、`SB_PADD` 系列）。移機、換專案時最常壞的不是程式，是這些變數指到舊位置。可與第 20 章的環境與備份檢查表合併檢查。

## 35.4 自動位置編號（Autopos）

Autopos 是在**平面板零件**上自動設定位置（零件）編號的工具：它先依使用者定義的條件排序，再比對零件是否「相同」，相同者給同一個編號；編號本身是取自使用者定義區間的連續號碼，可再加前綴、後綴以標示設計階段。

### 35.4.1 設計意圖與啟用前提

官方設計意圖是：建模時**不設位置編號**（因此零件名也不定），等建模完成、甚至拆成組立之後，才由 Autopos 統一設定；建模剛結束時所有位置編號為 0。

| 項目 | 內容 |
|---|---|
| 規則物件 | `__SBH_AUTOPOS_CTRL__`，存在 `SB_OGDB`；由 `inithull`（Naming / Autoposition Set-Up）編譯規則檔產生，通常只做一次 |
| 啟用變數 | `SB_POSNO_SETS` 必須設定 |
| 補洞 | 設 `SBH_POSNO_INSERT` 時，找第一個空號（填補編號缺口），否則取目前系列最後號碼的下一號 |
| 前後綴 | 需設 `SBH_AN_POSNO`；英數混合編號時不能再使用「general purpose strings」，因為兩者佔用同一空間 |
| 「最終」編號 | 以 Hull Planar Modelling 預設檔的 `POSNO_PREFIX`、`POSNO_SUFFIX` 組合判定；例如前綴 A、B、K 且後綴 `HAI` 者視為最終，不會被 Autopos 或建模修改 |

### 35.4.2 規則檔（設定一次）

規則檔用 TIL 語法，編譯後建立物件。語句如下：

| 陳述 | 語法重點 | 作用 |
|---|---|---|
| `NEW;` | 無參數 | 覆寫既有 Autopos 物件（通常要加） |
| `SYM_EQUAL;` | 無參數 | 左右舷對稱的鏡像零件只給一個編號 |
| `SORT` | `/AFT_FOR`｜`/FOR_AFT`、`/SB_PS`｜`/PS_SB`｜`/SHELL_CL`｜`/CL_SHELL`、`/BOT_TOP`｜`/TOP_BOT` | 比對前依物理位置排序；可複合，依給定順序生效 |
| `BUNDLE` | `<part_type>` 兩個以上 | 把不同類型一起比對與排序，類型有 `/PLATE`、`/BRACKET`、`/CLIP`、`/DOUBLING`、`/SPIGOT`、`/STIFFENER`、`/BPROFILE`、`/FLANGE`、`/PILLAR`、`/FUN=<n>` |
| `CASE` | `CASE, <name>` 後接零件群組：`[criteria] /START=<n> /MAX=<n> /<type>…;` | 一組編號規則；準則 `/GEO`（依 SORT）、`/MAT_ASC`、`/MAT_DESC`；一份設定至少一個 CASE，最多 12 個 |

官方範例（簡單情境，型材全部合併、各類從 1 起編）：

```
NEW;
BUNDLE /STI /FLA /PIL /BPR;
CASE, 'NORMAL'
  /START=1 /MAX=1000 /STI /FLA /PIL /BPRO
  /START=1 /MAX=1000 /PLA
  /START=1 /MAX=1000 /BRA
  /START=1 /MAX=1000 /CLI
  /START=1 /MAX=1000 /DOU
;
```

### 35.4.3 執行檔（每次作業）

實際執行通常由 Hull Planar Modelling 的 **Pos No** 功能產生輸入檔並啟動獨立程序，使用者不必手寫；陳述如下。

| 陳述 | 作用 |
|---|---|
| `SCOPE` | 指定處理範圍（Block、Panel 等模型物件，可重複給）；沒有預設範圍。鐵舾裝框架用 `SCOPE /PANEL='/名稱'` |
| `CASE, <name>;` | 選用哪組規則；只有一組時可省略 |
| `PART` | 本次處理的零件類型（預設不處理任何類型），`/ALL` 表示全部；即使類型被 BUNDLE，也必須在此逐一列出 |
| `PREFIX`、`SUFFIX` | 本次所有編號加前後綴 |
| `OVERWRITE` | `/EMPTY`（預設，只更新空編號）、`/TEMPORARY`（也更新非最終編號）、`/FINAL`（連最終編號也更新）；三者獨立 |
| `LIST_ONLY [/SORT]` | 不寫回資料庫，只產生清單；`/SORT` 依排序後印出 |
| `COMPARISON` | 控制零件比對的範圍（預設在整個 SCOPE 內比；可改為例如「只在同一 Panel 內比」） |

比對相同零件的容許值寫死在程式內，使用者**無法修改**：板不比對（每塊板一個唯一編號）；肘板比對的條件包括面積差 ≤ 200 mm²、厚度差 ≤ 0.1 mm、名稱相同、肘板上型材型式與參數相同（容許 0.1 mm）、型材位置側別相同、材質等。

> **專業提醒：** `LIST_ONLY` 是最安全的上線方式：先對一個 Block 看清單，確認分組合理再 `OVERWRITE`。已發行給工廠的編號要設為「最終」，不要依賴人的記憶。與第 6 章的「快照」概念互補：編號改動也應走「修改→重新抽出→通知」流程。

## 35.5 板材套料（Hull Plate Nesting）

### 35.5.1 系統元件與資料流

套料系統由程式、資料庫與資料檔組成，**只有套料程式本身需要在工作站上互動執行**。輸入：板零件、標準母板（Standard parent plates）、標準鉤（Hooks）、預設資訊、標準圖框；輸出：套料板、列印、Generic File、板零件、標準板與清單。系統內含建立標準母板、鉤、預設值與圖框的功能，符號字型 2 為使用者符號、字型 92 為餘量符號。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Nesting System 資訊流圖：Nesting 位於中心，連接 Plate Parts、Backup、Curves、Hooks、Drawing Forms、Standard Plates、Defaults 等資料，輸出 Nested Plates、CL-descr（給後處理器）與 Plate（給繪圖機）
*圖 35-4　套料系統的資訊流（官方圖：方框為程式，圓圈為資料，雙圈為資料庫物件）。（AVEVA 官方文件截圖，僅供內部教學）*

### 35.5.2 官方概念表

| 概念 | 官方說明（整理） |
|---|---|
| 座標系 | 套料板的原點在母板左下角；在系統內建立的零件使用操作員定義的座標系 |
| 自動重新套料（Automatic Renesting） | 開啟舊套料板修改時，系統一律使用「最新版」零件；零件自上次套料後若有修改，或已套料零件被移動，會重建生產資訊（橋、起點等） |
| 切割橋（Burning Bridges） | 9 種：Gap、雙中心橋（正／負）、單中心橋、十字中心橋、雙偏置橋（正／負）、單偏置橋、十字偏置橋、切口內雙偏置橋、含自由切割幾何的 Gap |
| 輔助功能（Auxiliary Functions） | 基本功能（工具開關、劃線開關、劃線偏移、切口補償 kerf、快移、停止）自動產生；特殊用途可由操作員定義在節點、輪廓任意點、或角隅圈（Corner Loop）的 3 個預設點 |
| 起點（Starts） | 劃線起點與切割起點可手動定義或自動產生；工具路徑順序就是建立順序（有重新編號功能）；劃線起點永遠在劃線末端，以箭頭表示 |
| 自動重啟 | 遇到 Gap 時目前切割路徑結束，工具空走到另一端後重新開始 |
| 原料板 | 套料使用的原料板必須先在目錄（Catalogue）中定義（Paragon 手動或 PML 腳本），可整合到專案材料（Project Material）或較鬆散地手動對應 |
| 剩料（Restplate） | 一般鋼材只在 Burning Sketch 上以文字標示，分「一般剩板」與「工廠剩料」（太小不算剩板、又太大不算廢料）；剩板名稱來自 `SBH_NSQ_RESTPLATE_TABLE`（每行：剩板名、適用板厚）；特殊鋼材的剩板存入標準資料庫，可當標準母板再次使用；一個套料作業最多 32767 代 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕切割橋類型 1 至 7：Gap、雙中心橋、單中心橋、十字中心橋等的示意
*圖 35-5　切割橋（Burning Bridge）類型 1–7 示意。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕切割起點的定義：游標位置與實際產生的起點記號
*圖 35-6　劃線起點（Marking Start）：游標位置決定起點，起點必定在劃線末端。（AVEVA 官方文件截圖，僅供內部教學）*

### 35.5.3 功能群組（Operator's Instructions）

官方的操作員指令把套料功能分成下列群組，各有數十個指令；本章只列群組與代表指令，逐一的 Purpose／Prerequisites／Instruction 格式請查原文。

| 群組 | 代表功能 |
|---|---|
| Nest Job | New／Open／Save／Rename、Data Bank（List／Delete）、Return to Drawing、Open Multiple |
| Nesting Parts | Nest（以零件名、資料檔或零件選單定義要放的零件）、Parts Menu、Transform、Verify、Bump Curve、Clustering |
| Transform | 移動（Bump／Parallel／DX DY／Two Positions／Dynamically）、旋轉（Angle／±90／45／180／Two Positions／Dynamically／Define Centre）、Mirror U/V、Lock U/V |
| Exchange | 換原料板（Raw Plate）、換零件（Part）、Autonest |
| Nesting Tools | Bridge、Start（Burn／Mark／Label／Automatic／Move／Sequence）、Labelling Text／Symbol、Auxiliary Function、Corner Loop、Hooks、Parts（建立板與型材零件）、Check Post Processor |
| Nest PPI | Create Standard Plates、Generic Post Processor、Batch Nesting |

其他套料相關功能：**One-Part Nesting**（`se016`，JL 名稱 Nesting One-Part；每個作業只含一塊板零件，自動放到最小的可用原料板，輸出 NC 資料與 Burning Sketch，NC 預設放 `SB_TAPE`）；**Nesting Plug-In**（35.5.5）。

### 35.5.4 初始化與預設值

| 項目 | 內容 |
|---|---|
| 預設檔（Defaults） | 以檔名識別的系統參數檔，路徑含名稱不超過 75 字元；用來配合不同工廠的切割作業；由 `SBH_NEST_DEF1`、`SBH_NEST_DEF2` 指定 |
| 燒嘴資料 | 以專用語言的 `BURNER,<name>,<no>,<type> /BURNER_ID= /PREP_MAIN= …` 語句描述，可多台；檔案名放 `SBH_BURNER_DATA`；路徑時間計算需要 `SBH_BURNER_ID` |
| 材質互換（Quality Exchange） | 以文字檔指定「某材質的零件可套在哪些材質的原料板上」，由 `SBH_QUALITY_EXCH` 指定 |
| 套料篩選檔 | `SBH_NEST_FILTER`，在標準篩選（名稱、板厚、材質）之外加 `INCLUDE`／`EXCLUDE` 條件，位於 `SBH_PRODUCTION_SETTINGS` 或 `SB_SHIP` |
| 坡口資訊 | 建模時定義的坡口會隨拆分傳到零件；`SBH_BEVEL_CTRL` 指定延伸坡口處理；可在 Show Production Information 檢視，並插入 Burning Sketch |

### 35.5.5 自動套料 Plug-In（對二次開發者最有用的一段）

套料系統可接外部圖樣產生器（pattern generator）。官方說明：AVEVA 提供另外授權的自動套料 Plug-In，但**任何外部 Plug-In 都可接**。

| 項目 | 內容 |
|---|---|
| 輸入給 Plug-In | 零件幾何（bump contour，即切坡口時的最大外形）、材質、板厚、組立、生產日期；原料板尺寸與數量；套料預設（鏡像旗標、旋轉增量、零件間／零件到板邊距離） |
| Plug-In 回傳 | 零件原點座標、旋轉角、鏡像旗標 |
| 模式 | 互動：先建立套料作業與 Parts Menu，再由 Automatic nesting 功能送出；批次：以輸入檔指定零件與原料板，可由系統自動設起點、定工具路徑、建立 Burning Sketch 與 Generic File |
| 連結方式 | `SBH_AUTONEST_PLUGIN` 指定要連接的 Plug-In |
| 介面形式 | 一組 C++ 例程與 Microsoft Visual Studio 專案（含 define 檔），建成 DLL；另有「套料順序演算法」的 Plug-In 介面 |

> **專業提醒：** 這是 Manufacturing 章節中少數有真正擴充點的地方：你可以自己寫套料演算法（例如針對自家板厚分組策略），但責任也跟著來，零件的 bump contour、鏡像與旋轉限制都要自行遵守。介面例程的確切函式簽章在官方 *Interface routines* 子頁，本章未逐一展開〔待核對〕。

## 35.6 切割資料、3 軸、型材套料與 Panel Line

### 35.6.1 Generic File 與 Generic Post Processor

套料系統的 **Verify** 指令會在 `SB_TAPE` 目錄產生 Generic File（`*.gen`），其中含幾何與屬性、並由套料決定作業順序（吹砂、劃線、GSD 定位符號、切割、文字與符號）。**Generic Post Processor（GPP，SF 001）** 讀取 `.gen`（來自套料或 Panel Line Control），依使用者的機器設定檔輸出控制碼。

| 設定 | 說明 |
|---|---|
| 執行 | 從 Nesting PPI 或套料內的 Verify 呼叫 |
| 預設檔 | 以套料預設 `GPP_CTRL_FILE=<檔名>` 指定，須在 `SB_SHIP` 目錄；每行 `keyword = value`，單位 mm |
| 必要參數 | `CONTROLLER`、`VARIANT`（控制器與型號）；`BURNER_TYPE`（`GAS`／`PLASMA`）；`MARKING_TYPE`（`PUNCH`／`POWDER`）；`UNITS_MM_OR_INCH`；`INCR_OR_ABS` |
| 幾何限制 | `INCREMENT`、`RADIUS_MIN`（預設 8.0）、`RADIUS_MAX`、`STRAIGHT_LINE_MIN`（預設 8.0）、`AMPLITUDE_TOLERANCE`（預設 0.5）等；另有炬感測點（`TORCH_SENSOR_DISTANCE` 等）與輸出檔名／副檔名（`TAPE_FILE_EXTENSION`） |
| Kerf 檔 | `GPP_KERF_FILE`；某些控制器與型號組合需要，依板厚、坡口側別／角度／深度取得 kerf 預選偏移與切割速度，必要時內插；官方定義 Format 1–8 八種格式 |

### 35.6.2 3 軸燒嘴（`sf623d`）

用於把一塊或多塊展開板排在原料板上，產生**給 3 軸切割設備**的製造資料。

| 項目 | 內容 |
|---|---|
| JL 名稱 | Nesting 3-Axis；工作代碼 `nest3ax` |
| 限制檔 | `SBH_3AX_RESTRICT`：關鍵字檔，含全板厚通用區段與依板厚區段 |
| 鉤選擇檔 | 依孔型（如 `D`）、板厚，決定起鉤與結束鉤；先找孔型再找尺寸完全吻合者 |
| 燒嘴資料 | `SBH_BURNER_DATA`、`SBH_BURNER_ID`（路徑時間計算用） |
| 圖框 | 與平面零件套料用的 `$` 值相同，另需 `$3998`（左下角）與 `$3999`（右上角）定位套料板 |
| 結果 | 每個套料一個 Generic File，檔名再列於另一個檔案，供後處理器單一入口讀取 |

### 35.6.3 型材套料（`sf605d`）

把生產資料庫中的型材組合成套料型材；**一維**問題，預設不允許旋轉。

| 項目 | 內容 |
|---|---|
| JL 名稱 | Hull Profile Nesting |
| 限制檔 | `SBH_PROF_RESTRICT` |
| 原料型材 | 目錄中定義；可整合專案材料。自動選擇原料時，每根型材最多選出 5 種可能材料（同型式、尺寸、材質），由套料結果決定最終選用；材質互換僅在「指定原料且不自動選擇」時啟用 |
| 旋轉 | `SBH_PROFILE_ROTATION`：`NO`（預設）、`UD`（上下翻轉）、`EE`（頭尾對調）、`UDEE`（兩者） |
| 輸出 | 套料型材存入 `SBH_NEST_PROFDB`；清單檔（含材料用量摘要）；逗號分隔檔（欄位含套料型材名、燒嘴標記、型材型式、材質碼、參數 A/B/S/T/C/U、原料總長／使用長度／餘料長度等）；套料圖存入 `SBH_RECEIPT`，名稱為套料名加 `P` |

### 35.6.4 Hull Panel Line Control（PLCM）

大型船舶的大平面板結構（平底、舷側、甲板、艙壁）在**平板生產線（Panel Line）** 生產。PLCM 是一個類似板套料的互動程式，主要用於控制第 3 工站的**切割與吹砂／劃線門架**，另可選擇性控制第 1 工站的零件平行切割。

| 面向 | 重點 |
|---|---|
| 零件抽出 | 由 PPANPARTS 在「Panel Line 模式」執行：設 `SBH_PANEL_LINE` 指向「組立名稱檔」（每行一個最低階組立，可用萬用字元 `*` 與 `%`）；此模式同時抽出 Piece Parts 與 Assembly Parts，Piece Parts 不存劃線，劃線只加在組立零件上 |
| 組立零件命名 | `<panel_name>-<assembly_name>`，例如 `AB123-4-U2B` |
| 例外處理 | 有倒角或幾何太複雜的零件不走第 1 工站，直接到輪廓切割機；以特殊物件碼標記為 Chamfer Parts，不參與組立套料，需另在套料系統處理 |
| 對位 | 某些切割機需要在其中一個零件上加兩個「板對位十字」，第 1 工站劃出並加到組立零件上 |
| 座標 | 套料的組立零件原點在母板左下角；套料的 Piece Parts 原點在右下角 |
| 後處理 | 需把 CL 檔轉成門架控制資訊；官方只現成提供 NCE 510 控制器的後處理器，其他格式要由 AVEVA 或客戶依 Generic 格式開發 |

> **專業提醒：** 3 軸、型材套料、Panel Line 三者都靠「限制檔／預設檔＋Job Launcher」。第 28 章提到的 Factory Automation 若要承接這些輸出，接點就是 Generic File（`.gen`）而非畫面，建議以 `.gen` 做離線驗證。

> 〔公開版未收錄：AVEVA 官方產品截圖〕型材路徑時間（pathtime）統計檔：列出套料型材名稱、各型材端切型式與 Ki 值、轉運、簽字、劃線、切割與附加項時間，總時間 361.9 秒
*圖 35-7　型材切割介面產生的路徑時間計算範例（燒嘴 ID 為 ROBBIE）。（AVEVA 官方文件截圖，僅供內部教學）*

## 35.7 型材製造輸出

官方 Profile Manufacturing 由兩支程式負責：**Profile Interface**（產生型材草圖、製造清單與 Generic File，輸入為 PPI 選取的型材）與 **Profile Cutting Interface**（針對套料型材，輸出切割機資料與路徑時間；同樣可產生草圖與清單）。

### 35.7.1 輸出類型與開關

| 輸出 | 開關（型材限制檔 `SBH_PROF_RESTRICT` 中設 `YES`） | 存放與設定 |
|---|---|---|
| 型材草圖 | `PSKETCH` | PADD：`SBH_PSKETCH_DWG` 與 `SBH_PSKETCH_DWG_PADD`；草圖限制檔 `SBH_SKETCH_RESTRICT`，圖框關鍵字 `FORM_NAME`（平面）、`FORM_NAME_SHELL`（殼板） |
| 套料型材草圖 | `NSKETCH` | `SBH_NSKETCH_DWG`／`_PADD`；限制檔 `SBH_NSKETCH_RESTRICT` |
| 製造清單（固定格式） | `MANSTIFF` | 版面由 `IDENT_MAN`、`LENGTH_IN_LIST`、`MANSTIFF_ECUT` 等控制 |
| 製造清單（逗號分隔，適合報表工具） | `MANSTIFF_CSV` | 同上 |
| Generic File（給機器人、外部系統） | — | 副檔名 `.GEN`；第一個關鍵字是 `TYPE_OF_GENERIC_FILE=`，值為 `NESTED_PROFILE`、`LISTED_PROFILE` 或 `BASIC_PROFILE`；關鍵字與值之間不可有空白 |

圖框上的規則：型材草圖框必須有 `$4501`、`$4502` 定位草圖區（型材高度會縮放填滿草圖框高度，長度伸縮填滿框長）；套料型材圖框必須有 `$3998`、`$3999`；彎曲方向符號用 `$4519`／`$4520`（矩形左下與右上角）。

### 35.7.2 草圖上的進階資訊

| 功能 | 設定 |
|---|---|
| 殼板型材彎曲資訊 | 官方以「中性曲線（neutral curve）」為基礎：型材彎曲時存在不伸縮的中性曲線，與軌跡（trace）平行、相距 d |
| 彎曲資訊畫在型材圖內 | 草圖限制檔中 `BENDING_RADIUS_LOW_LIMIT` 等關鍵字限定何時顯示彎曲半徑與角度 |
| 沿型材劃線 | 預設以「沿軌跡位置＋角度」表示；設特定關鍵字（草圖限制檔）可改成「沿軌跡一個尺寸、沿翼板側一個尺寸」 |
| Dotori | `DOTORI_ON_AXIS=YES`：沿軌跡軸顯示；假設一定有 V 型接頭，否則不顯示 |
| 過近邊緣的孔 | 型材限制檔 `SKIPHOLE_DIST` 大於 0：太靠近型材底邊、無法自動加工的孔，會從草圖、Generic File 與製造清單中略去 |
| 斜削翼板（Sniped Flange） | `SNIPED_FLANGE_LDIMENSION=YES/NO`：增加額外尺寸標註 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕殼板縱骨彎曲資訊：型材投影在 U-V 平面，標出翼板、中性曲線、軌跡、彎曲線與距離 d
*圖 35-8　殼板型材彎曲資訊的計算模型：中性曲線與軌跡距離 d。（AVEVA 官方文件截圖，僅供內部教學）*

### 35.7.3 端切尺寸標註與 Vitesse 觸發器

這是官方文件**唯一寫出 Python 介面**的製造功能。建立型材草圖時會觸發 `trig_hull_endcut_dim`，讓你客製端切與翼板切口的尺寸標註。官方在 Vitesse 程式庫新增模組 `KcsSketchDimensioning.py`（頁面標題誤作 `KscSketchDimensioning`），含類別 `KcsSketchDimensioning.ProfileSketch`，方法如 `GetProfileType()`（整數型材型式）、`GetProfileParams()`（六個實數參數）。

| 觸發器項目 | 內容（取自官方表格） |
|---|---|
| 事件／型式 | End cut dimensioning／Pre |
| 輸入參數 | `sketchData`：`ProfileSketch`（正確標註所需的型材參數） |
| 回傳 | `kcs_util.trigger_ok()` 或 `kcs_util.trigger_abort()`；若回 abort，端切碼與參數只會顯示在 `$4601`–`$4800` 範圍的 `$` 值 |
| 輸出參數 | `endCutDimensions`、`flangeCutDimensions`：`DimensionSet`（分別畫在腹板端切區與翼板切口區） |
| 覆寫 | None |
| 備註 | 觸發時草圖其餘資訊已畫完，已確保 `minx/miny/maxx/maxy` 正確，避免文字重疊；每根型材觸發**兩次**（左、右端切分開處理），右端結果由程式水平翻轉，腳本只需處理左端 |

官方範例已實作的端切型式（以型材種類分）：扁鋼 69、114、116、65；球扁鋼與 L 型 25、129、119、120；不對稱 T 139、164、162、40；T 型 4、83、39、145；I 型 175、181；U 型 188、190。標註種類有 Linear（含 Excess）、Angle、Radius 三種。

> **專業提醒：** 左端專用、右端自動翻轉，是官方明講的設計。寫腳本時不要自己對右端做鏡像，否則會翻兩次。第 15 章的 Vitesse 環境設定（`kcs_util` 觸發器註冊）請沿用，不在此重述。

## 35.8 曲面板製造資訊：胎架柱、板胎架與彎曲樣板

### 35.8.1 Jig Pillars（胎架柱，`sf824d`）

模組計算曲面殼板的**胎架柱**：柱位於固定網格的節點上，位置預先決定，**高度由程式計算**。基本資料通常是資料庫中的曲面板，也可由接縫臨時組成面板。

| 項目 | 內容 |
|---|---|
| 輸入語言 | TIL 格式，定義 `SB_INPUT1` 時使用；`PANEL`（既有面板）與 `PANEL_NAME`（臨時面板）二擇一，且只能一個；`PANEL_NAME` 要搭配 `SEAM, <1–12> / NAME='…'`（順時針由內向外看） |
| 其他陳述 | `VALID`、`ASSEMBLY_PLANE`、`ADD_SEAM`、`ADD_HULLCURVE`（把船體曲線加進胎架圖）、`JIG_PLANE_POSITION`（必須給：`/SEAM`、`/THICKNESS`、`/DIST_FROM_SEAM`、`/DIST_TO_ROW`、`/DISTANCE_FIRST_ROW`、`/DISTANCE_FIRST_PILLAR`，選用 `/SEAM_PARALLEL_SIGHTLINE`） |
| 輸出 | 胎架物件，名稱為面板名加 `-JIG`（或 `-JIGP`、`-JIGS`，依 `VALID`）；清單（柱高、面板角隅位置、到胎架排的距離）；圖面存入 `SBH_PINJIG_DWG`／`_PADD` |
| 互動工具 | Interactive Jig Pillars：New／Adjust／Open／Save／Preferences；可選一塊曲面板或在折角處焊接的兩塊平面板；Adjust 時選取區反灰，只可調整組裝面 |

### 35.8.2 Plate Jigs（板胎架，`sf821d`）

產生**放在車間地面的曲面胎架**，使曲面殼板貼合其上；胎架垂直立於地面，使面板盡量水平，或依輸入定義的組裝面放置。

| 項目 | 內容 |
|---|---|
| IP 檔 | `platejigs.ip`（`SB_SHIP`）；環境變數 `SB_HREF`、`SB_YARD` |
| 輸入語言 | `PANEL`、`JIG_ROW_POSITION`（`/x`：胎架排平面與組裝面的交線平行於肋位面；`/z`：平行於水線面）、`ASSEMBLY_PLANE`、`DISTANCES`、`SEAM`、`PROD_INFO`（`/XP`、`/YP`、`/ZP` 主平面，計算檢查資訊） |
| 輸出 | Plate Jig 物件存入資料庫並更新對應面板；清單；圖面 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕板胎架：曲面板置於組裝面之上，顯示 Panel、Seam or Butt、Jig row、Frame or waterline plane 與 Assembly plane
*圖 35-9　胎架排（Jig row）以肋位面或水線面為方向，與組裝面相交。（AVEVA 官方文件截圖，僅供內部教學）*

### 35.8.3 Bending Templates（殼板彎曲樣板）

成形曲面殼板時，常以樣板控制與檢查。模組可為已展開的殼板產生多種樣板與多種輸出（實體樣板或可調整樣板的設定資料）。樣板含：封閉樣板輪廓（上緣為直線，所有樣板上緣應在同一「視線面」，寬度須吻合板寬）、方向記號等。

| 樣板類型 | 特徵 |
|---|---|
| Standard | 垂直於板面，沿板面最佳化分佈（間距與方向） |
| Standard Frame | 永遠位於肋位上（可選擇距短邊一個距離），不必額外定位資訊；缺點是肋位面與板面夾角小時檢驗效果差 |
| Normal | 彼此平行；以板中間附近一塊樣板定義平面，其餘依距離平行排列 |
| Special Frame（Flexible） | 兩種變體：真正位於肋位面，或只在板邊在肋位上但全部垂直於基準面；中國造船業常用的柔性樣板（柔性部分加帶視標的支架） |
| Cross | 沿基準面 v 軸方向（內側樣板）與 u 軸方向（交叉樣板）兩個主方向，皆垂直於基準面 |

另有 Edge Seam Templates：當短邊不在肋位面時，增加平行短邊的樣板，避免大片區域沒有樣板。

| 設定 | 內容 |
|---|---|
| IP 檔 | `bendtempl.ip`（`SB_SHIP`），預設參數必須「完全依規定寫、且每項後面一定要逗號」；`ENGLISH,`／`GERMAN,` 等語言選項；Normal 模式以預設關鍵字 `NORMAL_TEMPLATES` 啟動 |
| 輸出 | 資料庫（樣板）、清單（含銷高度表）、樣板圖 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕彎曲樣板示意：曲面殼板 Plate 1 至 Plate 4 上立有樣板，標示 sight line、placing marks、direction mark、templates 與 curved shell plate
*圖 35-10　彎曲樣板的使用：樣板上緣落在視線面，並以方向記號與擺放記號定位。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Standard 樣板：垂直於殼板表面，上方為視線面 sight plane
*圖 35-11　Standard 樣板垂直於殼板表面，上緣位於同一個視線面。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Cross 樣板：青綠色曲面板上，內側樣板與交叉樣板垂直相交成格子
*圖 35-12　Cross 樣板：兩個方向的樣板皆垂直於基準面。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 樣板與胎架都以「肋位」「水線」為座標骨架，因此它們直接依賴第 33、34 章建立的 Hull Reference 與肋位定義。肋位表若不一致，樣板位置會偏，而且不一定報錯。

## 35.9 焊接機器人與 Plate Interface

### 35.9.1 Robot Interface（`pg101`）

把產品模型資料轉成**電弧焊接機器人或類似生產設備**可用的資料。輸入同樣來自 PPI 的選取（組立、Block、Panel 等）。

| 項目 | 內容 |
|---|---|
| JL 名稱 | Hull Robot Interface |
| 結果 | 讀輸入檔的診斷、建立中性檔的診斷，以及轉換後的**中性文字檔** |
| 中性檔結構 | 由「物件」組成，每個物件（Panel、板、加強材、夾片、組立）以 start-of-object 與 end-of-object 兩行框住，其後接訊息記錄（非圖形資訊） |
| 記錄型態 | RT 1（物件開始）、2（訊息）、15（輪廓開始）、16（線段）、7（群組開始／結束）、9（圖層）、99（物件結束） |
| 群組／物件碼 | panel 701、panel contour 702、hole 703、stiffener 704、pillar 705、flange 706、doubling 708、bracket 721、bracket plate 722、clip 724、endcut 750、cutout 751、notch 752、assembly 735 |
| 訊息記錄 | 生產日期時間、名稱、Volume、型材型式、生產資訊、組立與 Panel 轉換、子體積型式、切口與缺口起點、夾片巨集識別碼等 |
| ATX Viewer | `TbATXViewer`，檢視 `.atx`（Robot Interface 輸出）的圖形工具；含主選單、工具列、樹狀檢視、設定面板、點面板；可能需要再開 gentab 檔以取得船體座標 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕TbATXViewer 視窗：左側樹狀列出 ER1-FR32_1 下的零件、孔與 Endcut，右側以綠色顯示兩個加強板與紅色焊線，右下為座標軸，下方為屬性表
*圖 35-13　ATX Viewer 檢視機器人介面輸出：樹狀節點對應中性檔中的物件與子物件。（AVEVA 官方文件截圖，僅供內部教學）*

### 35.9.2 Plate Interface 與 Generic 資料

| 項目 | 內容 |
|---|---|
| Plate Interface | 把板資料抽成 Generic Format 檔，供產生草圖、製造清單的程式再處理；板厚與材質相同者存在同一檔，檔名取其中一個板零件名並加 `.gen` |
| Create Plate Parts from Generic Files | 執行檔 `TbGeneric2Plate`（Log Viewer 中稱 Hull Generic to Plate），可從 `SB_TAPE` 的 Generic Files 反向建立板零件；也可由命令列把檔案路徑寫進輸入檔執行 |

與第 28 章的 Weld Planning 的關係：官方寫明 Weld Planning 可對任何隸屬組立的框架（鐵舾裝）計算；機器人介面的焊接輸出如何銜接到 Weld Planning 資料，**本章未讀到文件依據**〔待核對〕。

## 35.10 鐵舾裝的生產特徵（Production Features for Outfit Steel）

### 35.10.1 觀念

舾裝鋼（Outfit Steel）模型是以 **框架（FRMW 或 SBFR）層級**轉進船體系統：當使用者要求製造板或型材、或計算焊接時才轉換，而且**只轉換被標為「ready for production」的框架**。系統內部用**船體 Panel 當作中間模型物件**，這些 Panel 預設只是暫存、不存進資料庫、也不參與碰撞檢查（除非另行要求，見 `OPTBLO`）。

### 35.10.2 目錄設定

| 項目 | 說明 |
|---|---|
| 板 | 不需要特殊設定 |
| 型材 | 目錄的 `SPRF` 元素必須定義 `SFCODE` 與 `TRCLIN` 兩個屬性 |
| `SFCODE` | 整數，即船體型材型式（例如 10＝扁鋼），對照 AVEVA Marine 的 Profile Types |
| `TRCLIN` | 字串，是舾裝型材與船體型材之間的連結，指定舾裝型材上**哪一條 Pline** 是船體型材斷面定義點（圖中的叉號）的位置 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕船體型材斷面定義點：L、扁鋼、球扁鋼、T、C、I、圓、半圓、六角、八角與方管等斷面，每個斷面上以叉號標示定義點
*圖 35-14　船體型材斷面定義點（叉號）；`TRCLIN` 要指向舾裝型材上對應此點的 Pline。（AVEVA 官方文件截圖，僅供內部教學）*

### 35.10.3 端切（End Cuts）的三種情境

| 情境 | 做法 |
|---|---|
| 1. 斜削端（Sniped） | 使用 `Drnstart`／`Drnend` 屬性，不需目錄轉換，轉成標準的船體斜削端切；**不能與其他負幾何組合**，若需要組合，改用情境 2 或 3 |
| 2. 對映端切 | 框架型材以目錄中的對映端切建模，與船體端切一一對應；目錄版本在 Marine 提供的 MAS 專案的 `/MARINE/MAPPING_ENDCUTS`，可能需配合船體端切設定做相同客製；要求製造資訊時才轉換 |
| 3. 船體使用者定義端切 | 框架型材的端切直接使用船體生產用的 User defined end cut；要求：屬性 `bangle` 為 0，且使用者定義端切的負幾何定義點需對應框架型材斷面定義點 |

### 35.10.4 讓框架「Ready for Production」：`PDNAME` 與 `OPTBLO`

| 屬性 | 說明 |
|---|---|
| `PDNAME` | **必須給**，框架才會被考慮轉換；內容是生產名稱 |
| 板命名 | `<PDNAME>-<板號><舷別 P 或 S>` |
| 型材命名 | `<PDNAME>/S<型材號><舷別 P 或 S>` |
| 彎板（BPANEL） | 板名多一個前綴：`<PDNAME>_Z<流水號>-<板號><舷別>` |
| `OPTBLO` | 選用；可填船體 Block 名，若填，轉換用的 Panel 會永久存在該 Block 之下，不參與碰撞，但可用標準船體工具修改；再次轉換時比對時間戳記，若已存 Panel 的儲存日期晚於框架的原始時間，就使用已存 Panel |

### 35.10.5 倒角（Bevel）與餘量（Excess）

倒角與餘量以資料附在板或型材上，轉入船體生產時才被套用。官方以「活動、屬性 Purpose 的內容、屬性 Desparam 的內容、屬性 Zdistance 的內容」表格描述；**Section 與 Panel 類用配件（FITT），GENSEC 用固定件（FIXING）**。

| 活動 | `Purpose` | `Desparam` | Zdistance／位置 |
|---|---|---|---|
| 餘量 | `EXC` | [1] 餘量大小 | 最靠近要加餘量那一端的位置值 |
| 腹板端倒角 | `BEVW` | [1] 倒角碼，[2] 連接角，[3] 倒角組（bevel set） | 同上（最靠近端部） |
| 翼板端倒角 | `BEVF` | 同上 | 同上 |
| 沿軌跡倒角 | `BEVT` | 同上 | 任意位置皆有效 |
| 板邊倒角（BPANEL／PANE） | `BEV` | 同上 | 最靠近板邊的位置 |

倒角碼與倒角組依船體系統設定；官方範例：`200,0,0` → 直接使用倒角碼 200；`0,30,3` → 沒給倒角碼，依連接角 30 度與倒角組 3 以船體倒角控制規則算出。GENSEC 的 `Zdistance` 屬性位於階層中 GENSEC 上方的 `JKDATU` 元素。

### 35.10.6 在船體生產中使用框架

| 功能 | 互動方式 | 批次方式 |
|---|---|---|
| 自動零件產生（Ppanparts） | 圖面上右鍵框架選 Generate Parts；或在 HULL PPI 用 Select 選框架 | 框架名加斜線前綴，如 `PANEL,'/PPM-TEST2X';`；名稱不合船體命名慣例（太長、字元不允許）時改用資料庫參考，如 `PANEL,'=24104/277536';` |
| 零件清單、材料清單、型材草圖與清單、型材套料、重量與重心、Plate Interface | 同上，用 PPI Select | 同上，Panel 語法 |
| 自動位置編號 | 範圍選單用 Frameworks | `SCOPE /PANEL='/PPM-TEST2';` |
| Weld Planning | 屬於組立的框架均可計算 | — |

特別設定：要在船體**平面 Panel 上標示框架的劃線**，需在 Ppanparts 使用的 IP 檔加入關鍵字 `STRUCTURE`。**同步**：自動從框架產生的 Panel 每次儲存時，會把生產屬性 Position Number 與 Part Name 同步回原框架的板與型材。

### 35.10.7 生產限制

| 對象 | 限制 |
|---|---|
| 板 | 單一框架最多 1000 個板零件；不支援 Seam、Marking、Cutout、Swage |
| 型材 | 單一框架最多 700 根型材；型式 10、20、21、23、30、31、33、35–38、40、43、50–55 支援直型材、端切、孔與缺口、單向彎曲（腹板面）；型式 60、70–74 支援直型材與單向彎曲；型式 56、61、62、64、65 僅支援直型材 |

> **專業提醒：** `PDNAME` 是最常被忘的一步；沒有它，框架在 PPI 裡就是不會出現。兩頭資料庫的名稱規則也不同：舾裝端名稱受 Paragon／Design 規則約束，生產名稱則受船體命名慣例約束，不合時改用 `=` 開頭資料庫參考。第 22 章（結構）談 FRMW、SBFR 與 GENSEC 時，可回頭對照本節。

### 常見錯誤

- 型材只在目錄設 `SFCODE` 忘了 `TRCLIN`；以為 Sniped 端切可疊加缺口（官方明寫不能）；轉換 Panel 預設不存資料庫，需查時指定 `OPTBLO`。

## 35.11 F1 - Help Texts：初始化介面的結構

F1 Help Texts 是 Hull 初始化（`inithull`）使用的一組 Windows 表單的說明，約 70 頁。內容高度規律，可歸納成下列結構。

### 35.11.1 三種表單型態

| 型態 | 用途 | 操作 |
|---|---|---|
| TIL Interface | 選輸入檔，編輯後建立對應的**控制物件** | 輸入完整路徑或按 Browse；選定後啟用 Edit TIL File（開 Notepad，關閉後才能繼續；改了要用 Notepad 存檔）與 Create Object；對應的語法檔須在 `SBB_SYNTDIR` 指向的目錄；注意介面**不會檢查輸入檔是否存在**；Wizard 按鈕一直可按，但目前只有 Part Name Control 有精靈，其他按下會有訊息 |
| File Check Interface | 檢查既有檔案的語法或正確性 | 對應環境變數須先指向該檔；Edit 開 Notepad；Check 呼叫檢查程序，結果以對話框回報 |
| 專用表單 | Structref（Structure Reference／Hull Structure 物件）、Hullref（Hull Reference 物件）、Blocks（Block 物件）、Functional Properties、Part Names Wizard、Result Dialog 等 | 見下 |

### 35.11.2 條目對照

| 類別 | 條目（官方標題，簡化） |
|---|---|
| Create（TIL） | Folded Flange、Part Name Control、Frame/Long. Positions、Functional prop.、Bevel std、Reference Plane、Bracket Std、Bracket Instance Object、Autopos Set-up、Shrinkage Obj.、Cutouts Ext. Def.、Endcut Table、Swedging |
| Check（File Check） | Qualities、Connection Codes、Interactive Bracket Default File、Autom. Cutout Sel.、Endcut Selection、Profiles for Project、Bracket Characteristics File、Quality Exchange、Knuckle ctrl、Cutouts via Macro、Profiles to Plate、Clips via Macro、U- and I- Bar Set-up、Profile Restrictions、Shell Stiff. Curvature |
| 專用物件 | Structref Create（需有效的 OGDB 與 CGDB）、Hullref Create（可另管理 Hull Reference Object Surfaces 的額外曲面）、Blocks Manipulate |

### 35.11.3 Block 物件、功能屬性與零件名稱精靈

| 表單 | 重點 |
|---|---|
| Block Objects | 名稱前 `*` 表示 Block 物件確實在資料庫，`!` 表示只在 `hullstruct` 物件中被參考；以 Get Data from OGDB 讀取、Update OGDB 寫入；取回資料時不會警告覆蓋未存改動；「Referenced values」勾選可在 FR/LP（肋位／縱向位置）表示與一般數值間切換 |
| Functional Properties Wizard | 與 Functional Properties 物件互動；要求環境指向有效 OGDB；可就地編輯索引號與值（文字） |
| Part Names Wizard | 五步：(1) 層級名稱（最多 10 個、不可重複，預設 `SHORT` 與 `FULL`）、(2) 對稱陳述值、(3) Built profile 陳述值、(4) 名稱「建構塊」的成分／分隔符號對，並以樹表示 TIL 檔結構、(5) 以純 TIL 顯示並可 Save |
| Result Dialog | 操作後顯示結果，提供「Copy to Clipboard」，利於把錯誤貼給支援人員 |

> **專業提醒：** 這些表單都是「文字檔＋編譯成物件」。排查製造結果不對時，先檢查控制物件是否是**最新編譯**的，而不是只看文字檔。

## 35.12 二次開發者怎麼接

官方這三塊內容，可對照到的介面如下；未列出者表示文件未提供。

| 需求 | 文件有依據的做法 | 狀態 |
|---|---|---|
| 客製型材端切尺寸標註 | Vitesse 觸發器 `trig_hull_endcut_dim`，型別 Pre；回傳 `kcs_util.trigger_ok()`／`trigger_abort()`；使用 `KcsSketchDimensioning.ProfileSketch` 與 `DimensionSet` | 有依據；`DimensionSet` 的建構與欄位細節見官方 *Linear/Angle/Radius Dimension* 子頁，本章未逐一展開〔待核對〕 |
| 自家套料演算法 | 自動套料 Plug-In：C++ DLL 與 Visual Studio 專案，`SBH_AUTONEST_PLUGIN` 指向；互動與批次兩種 | 有依據；例程簽章〔待核對〕 |
| 批次觸發製造程式 | 製造程式以 Job Launcher 啟動、輸入為 `SB_INPUT1` 的 `.dat`、輸出為 `SB_OUTPUT1` 的 `.log` | 檔案層級有依據；以 PML／.NET 呼叫 JL 的方式本章未讀到〔待核對〕 |
| 讀取機器資料 | 解析 Generic File（`.gen`、`.GEN`）、Robot 中性檔（`.atx`）、型材逗號分隔清單 | 格式有依據；皆為純文字，離線讀取不需 AVEVA API |

> **專業提醒：** 從開發者角度，Manufacturing 的穩定接點是**檔案**（`.ip`、限制檔、`.dat`、`.gen`、`.atx`、`.lst`）與**環境變數**，而不是 API。把檔案當介面，可以離線測試、版本控管，也最不怕升版。

## 35.13 本章小結

1. Manufacturing 的共通模式：**PPI 選取 → Job Launcher 執行程式（輸入 `SB_INPUT1`、輸出 `SB_OUTPUT1`）→ 結果進資料庫、清單、PADD 圖面**；設定靠 IP 檔、限制檔、環境變數。
2. 零件層：平面零件 `sf416d`、曲面零件 `sf831d`；Autopos 以「規則物件＋每次執行檔」設位置編號，`LIST_ONLY` 先看再寫。
3. 切割層：套料（板、型材、單件、3 軸、Panel Line）→ Generic File → GPP／後處理器。自動套料 Plug-In 是少數真正的擴充點。
4. 型材層：草圖、製造清單、彎曲資訊與路徑時間；端切標註可用 Vitesse 觸發器客製。
5. 曲面層：胎架柱、板胎架與五種彎曲樣板，依肋位與水線座標。
6. 鐵舾裝：框架要有 `PDNAME` 才進得了生產；目錄需 `SFCODE`／`TRCLIN`；倒角餘量用 FITT／FIXING；有 1000 板／700 型材與型式限制。
7. F1 Help Texts 是初始化的 TIL／檔案檢查表單集，規律很強。

## 練習題與自我檢核

### 練習 35-1：PPI 與零件
1. 在訓練專案開 Production interface，選取一個 Panel，執行 Plane Part Generation，找出 `ppanparts_<job>.lst` 與 `PPAN_<job>` 圖。
2. 記錄 `SB_PLDB`、`SBH_PROFDB`、`SB_SHIP` 實際指到哪裡。

### 練習 35-2：Autopos

用 `LIST_ONLY /SORT` 對一個 Block 看清單，再切換 `OVERWRITE` 選項，觀察哪些編號被改。

### 練習 35-3：套料與鐵舾裝

開新套料作業放三個零件並加橋與起點，Verify 後讀 `SB_TAPE` 內 `.gen`；為一個 FRMW 設 `PDNAME`，用 PPI 的 Framework 選取產生零件。

### 自我檢核

- [ ] 我能說出 PPI 的三個步驟，與選取如何影響後續功能。
- [ ] 我知道平面零件與曲面零件各自的 IP 檔檔名與位置。
- [ ] 我能解釋 Autopos 的 `BUNDLE`、`CASE`、`OVERWRITE`、`LIST_ONLY`。
- [ ] 我能列出 Generic File 到機器碼的路徑與涉及的預設／Kerf 檔。
- [ ] 我知道 `trig_hull_endcut_dim` 每根型材觸發兩次，且只需處理左端。
- [ ] 我能說出鐵舾裝框架進入生產所需的目錄與屬性設定。
- [ ] 我能區分 TIL Interface 與 File Check Interface。

## 〔待核對〕彙整

1. `ppanparts.ip`、`cpanparts.ip` 的完整關鍵字清單與預設值（本章僅列部分）。
2. 自動套料 Plug-In 的 C++ 例程簽章（官方 *Interface routines* 子頁未展開）。
3. `KcsSketchDimensioning` 模組中 `DimensionSet` 的完整方法與欄位。
4. 以 PML、.NET 或 Vitesse 從外部呼叫 Job Launcher 並指定 `SB_INPUT1` 的做法。
5. 以程式查詢 `SB_PLDB`、`SBH_PROFDB` 等製造資料庫的 API。
6. 機器人介面輸出與第 28 章 Weld Planning 資料如何銜接。
7. 各 `.ip`、限制檔的關鍵字在不同 12.1 SP 的差異。
8. 鐵舾裝 `FITT`／`FIXING` 在 Design 或 PML 中的設值語法。
9. 官方頁面標題的拼寫問題（如 `KscSketchDimensioning`、Plate Jigs 清單錨點）是否影響實際類別名稱，需實測。

## 取材覆蓋說明

- 本章範圍的頁面總數約 740 頁（Manufacturing 約 651、Outfit Steel 約 18、F1 Help Texts 約 71）。
- 實際以工具取回並閱讀約 **365 頁**：Outfit Steel 全部 18 頁（全文）；F1 Help Texts 約 50 頁（TIL Interface、File Check Interface、Block Objects 取全文，其餘條目只讀標題與前段）；Manufacturing 約 300 頁，其中多數只讀前 400–700 字元的摘要。
- 讀得較完整：Autopos（含各陳述）、套料概念與初始化、GPP 預設檔（前半）、3 軸、型材套料、Panel Line 概論、PPI、型材輸出（尤其端切觸發器）、Jig／樣板概論、Robot 中性檔概論、鐵舾裝全部。
- **沒讀或只讀標題的子樹**：Hull Plate Nesting 的各個 Functions Overview 單一功能頁（約 100 頁，只讀概念頁）；Operator's Instructions 的逐指令頁（約 100 頁，只讀群組頁）；Generic Postprocessor 的 Kerf Format 1–8 逐頁；Robot Interface 的各 Record Type、Message Records 逐頁；Bending Templates 各子頁（Normal／Flexible／Special／Cross 的 Default 檔範例與規則）；Plate Jigs 與 Jig Pillar 的各陳述細頁；型材輸出的 Endcut Dimensioning 子頁（Linear／Angle／Radius）、Nested Profile Sketch 的三個範例頁；F1 Help Texts 的各 Check／Create 條目內容（只歸納結構）；F1 頁面中文機器翻譯多不通順，一律以英文原文為準。
- 圖片：採用 14 張官方圖，其餘低解析或關聯弱未採用；鐵舾裝端切頁（`1122733`）的圖未出現在擷取內容中。
