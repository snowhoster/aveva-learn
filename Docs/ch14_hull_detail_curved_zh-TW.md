# 第 14 章　船體詳細設計（二）：曲面板架建模、選用功能與雜項工具

> [第 9 章](ch09_hull_modelling_zh-TW.reading.html)把船體建模的概念走過一遍，[第 13 章](ch13_hull_detail_planar_zh-TW.reading.html)講平面板架（Planar Modelling）。這一章處理船體詳細設計裡「另一半」：**曲面板架（Curved Hull Modelling）**，也就是外板的接縫、外板縱骨、外板展開與曲面板架；接著是一組**選用功能（Optional Hull Functions）**，以及零件表、領料、重量重心、船體標記等**雜項工具（Miscellaneous Utilities）**。
>
> 曲面船體有一個和內部結構很不同的特性：**它幾乎不靠輸入檔，而是在畫面上「物件－動作」地互動建模**，每個物件記著自己的定義，曲面改了可以重建（Recreate）。對二次開發者而言，這意味著資料入口不是 PML 腳本，而是官方文件反覆提到的 XML 輸入語言、批次程式與 Job Launcher 的輸入／輸出檔。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件 *Hull Detailed Design* 底下三個子樹：Hull Curved Modelling、Optional Hull Functions、Miscellaneous Utilities（頁面為英文並附機器中譯，譯名生硬處本章改用台灣造船慣用語）。文件是操作手冊，**沒有 PML 範例**，也沒有曲面船體資料庫的屬性字典；因此「二次開發者怎麼接」只寫文件明講的檔案、環境變數、參數與 XML 元素名，其餘標〔待核對〕。部分頁面沿用 Tribon 時代名稱（`SB_` 開頭的環境變數、`Tribon part name` 等），本章照錄。讀了多少頁、哪些沒讀，見 附錄 E。

## 14.1 學習目標

讀完本章，你應該能夠：

1. 說明曲面船體（Curved Hull）在設計各階段的用途與限制，以及它與初始設計、平面建模、製造模組的上下游關係。
2. 解釋「工作區（Workspace）」「選取清單（select list）」「物件－動作」「由下而上／由上而下」等互動原則。
3. 說明 Seam、Butt、Shell Profile、Shell Stiffener、Shell Plate、Curved Panel 的概念與命名規則。
4. 依步驟建立 Seam/Butt、Shell Plate、Shell Profile，並設定超長（excess）、補償（compensation）、斜角（bevel）與傾角點。
5. 使用 Split／Combine／Modify Curve／To Manufacturing DB 處理外板縱骨，並建立開孔、缺口、切口與標記線。
6. 使用 Geometry 功能（點、平面、一般柱面、外板曲線）從下而上建構定義曲線，並理解 Recreate 與 Topology 的作用。
7. 建立 Shell Expansion、Bodyplan、Developed Plate、Curved Panel 等視圖，並用 Advanced Selection 管理選取。
8. 說明外板展開方法（基準線、分條、間隙／重疊、滾軸），並知道何時要調整 Strip 控制。
9. 說明七類選用功能（FRP、Stiffener Nesting、Painting Areas、GPP、Factory Automation 等）各自解決什麼問題。
10. 說明零件表、領料、重量重心與船體標記程式的輸入輸出方式，並指出二次開發者可用的檔案介面。

## 14.2 曲面船體概觀

### 14.2.1 用途與限制

官方把船舶設計到生產粗分為專案計算、設計、詳細設計、生產四階段。Curved Hull 的定位是**從早期設計一路用到生產準備**：

| 階段 | Curved Hull 的用途 |
|---|---|
| 設計（分級圖階段） | 建立曲面船體構件的早期數值模型；由模型導出視圖作分級圖；作為初估重量、初估領料的基礎 |
| 詳細設計 | 持續精煉模型，把早期模型拆成生產單元並補細節；導出工作圖；供各類生產資訊使用 |

限制須先記住：**系統內沒有強度計算模組**，船級規範只在有限程度內內建（集中於 micro standards）；目前涵蓋接縫與對接縫、一般用途的船體曲線與外板縱骨，外板可定義並展開，曲面板架由既有的外板與外板縱骨組合而成。

### 14.2.2 與其他模組的關係

| 類別 | 內容 |
|---|---|
| 提供基礎資訊 | 資料庫初始化工具；船形產生模組（如 Initial Design，可產出符合生產精度的船形）；也可匯入第三方 AVEVA Surface Manager 曲面（見[第 11 章](ch11_surface_block_zh-TW.reading.html)） |
| 輔助模組 | 部分功能可批次執行，例如視圖導出：一支程式處理平面切割視圖，另一支處理外板展開；結果仍須帶回 Curved Hull 中完成成圖 |
| 使用其產出 | 外板產生的接縫與縱骨曲線會被平面建模引用（建內部結構）；外板厚度與材料方向會影響貼在其上的內部結構幾何 |

不論曲面是最終或初步船形，Curved Hull 用起來沒有差別。

## 14.3 互動建模的核心概念

### 14.3.1 工作區與選取清單

- **工作區（Workspace）**：互動發生在一張「圖」裡，圖內有多個視圖：3D、符號船體視圖、橫剖線圖（body plan）、外板展開視圖，以及「單一物件」視圖（展開板、縱骨、曲面板架）。可在任何視圖中挑選物件，所有視圖同步高亮。新建物件會顯示於所有相關視圖（單物件視圖通常不含）。工作區雖是圖，卻不必有圖框。
- **物件－動作原則**：先選物件、再啟動功能。建立的物件可作為下一個功能的輸入，因此能把複雜物件拆成小而可重用的功能（由下而上）。
- **由下而上與由上而下**：若選取清單中已有所需物件，功能直接進行；若沒有，系統彈出選單問你要用哪種功能產生所需物件（由上而下）。兩種可混用。
- **選取清單（select list）**：功能啟動時先找清單中的物件；通常「用掉」的物件被移出清單，產生的物件被加入清單。例如 Curve by Plane 會對清單中每個平面切曲面得到曲線，平面移出、曲線加入。
- **套用與復原**：建立或修改後的物件可 Apply（確認，最終寫入資料庫）或復原（Deactivate，回到上一次套用的版本）。

### 14.3.2 暫時物件與儲存物件

建立 Seam 時，它依賴一條曲線，該曲線又依賴其他幾何物件，這些幾何物件是**暫時物件**，系統自動命名為底線加數字（如 `_12`）。**儲存時，所有底層暫時物件的定義會收進 Seam 自己**，以減少資料庫內的物件間連結；之後從資料庫讀回（例如曲面改了要重建），暫時物件才被重新建立並接回。

建立物件的三種方式：

1. 在既有曲面上建曲線：Seam、Butt、Hull Curve、Shell Profile。
2. 蒐集既有物件：展開板（Developed Plate）、曲面板架；曲面板架也可由接縫與對接縫的矩陣一併產生外板。
3. 把既有物件拆成多個：Shell Stiffener（由 Split 產生）。

定義曲線的方法有：曲面與平面相交、與柱面相交、平行於另一曲線（含縱骨軌跡）、組合兩條曲線、由既有曲線／Hull Curve／Lines fairing 曲線建立（亦可用外部曲面系統的曲線）。

### 14.3.3 詞彙與命名規則

官方的術語中，**Shell Profile** 是縱向構件（longitudinal）與橫向構件（transversal）的總稱，**在現實中並不存在**，實際生產的是被切成小段的 **Shell Stiffener**；位置由其**軌跡曲線（trace curve）**決定。一個 Profile 可有多條軌跡，但單一 Stiffener 只屬於一條。**Shell Plate** 則是外板，建立時自動展開。

| 物件 | 預設命名 | 說明 |
|---|---|---|
| Seam／Butt | `<接縫群組名><接縫號>` | 群組名登錄於 Hull Reference Object（由 Initiate Hull Standards 程式初始化），號碼 1–9999 |
| Shell Profile | `<群組名><曲面字尾><縱骨號>` | 群組名與曲面字尾於 Initiate Hull Standards 設定；曲面字尾讓不同曲面可有同號縱骨 |
| Shell Stiffener | `<縱骨名>-S<流水號><對稱碼>` | 對稱碼 `P` 為左舷專用或跨中心線，`S` 為右舷專用，對稱件省略；例：`ESL120-S1`，分割後新增 `ESL120-S2` |
| 軌跡曲線 | `<縱骨名>_CV<流水號>` | 若軌跡來自既有 Hull Curve 則沿用原名；例：`EST104_CV1` |
| Shell Plate | 任意 | 可自訂 |
| Curved Panel | `<分段名>-<板架名><對稱碼>` | 對稱碼 `P`、`S`、`SP`（跨中心線）；例：`ES123-45S` |
| Hull Curve／Storable Point／Storable Plane | 無限制 | |

邏輯變數 `SBH_FREE_SEAMPROF_NAMES` 設為 YES 時，Seam 與 Shell Profile 可用任意名稱，且永遠以全名辨識；**官方明確建議：專案已建立 Seam 或縱骨之後，不要再改這個設定。**

### 14.3.4 預設曲面與預設盒

- **Default Surface**：建立 Seam、縱骨等物件都要指定曲面，只需選一次；工作階段一開始預設為船的主曲面。
- **Default Box**：某些運算（如曲面與平面相交）使用的限制盒，結果曲線會被盒裁切。工作階段開始時涵蓋整個左舷（Y 最小值為 0）；若設定預設參數 `DEF_YMIN_NO_LIMIT`，則各方向皆無限。

> **專業提醒：** 新手最常抱怨「我切出來的曲線只有一半」，多半是 Default Box 把右舷裁掉了。要建右舷或跨中心線的物件，先到 Default 選單改 Box，或在表單上按 Starboard／Any 快速設定。

## 14.4 Curved 選單：Model 子選單

曲面船體的專用功能位於繪圖視窗的 Curved 選單，通用功能（視圖、符號等）屬於 Drafting。以下依官方分類逐一說明。

### 14.4.1 Create Seam/Butt

由曲線建立接縫或對接縫。選取清單中若已有曲線，系統用它們做 Seam（若是 lines fairing 曲線或 Hull Curve 會複製一份，且 Seam 記得來源曲線的參照）；若沒有曲線，則跳出分頁表單要你定義。

> 〔公開版未收錄：AVEVA 官方產品截圖〕建立接縫與對接縫的表單，含 General、Limit、Curve Data 分頁

*圖 14-1　Create Seam/Butt 表單。（AVEVA 官方文件截圖，僅供內部教學）*

| 欄位 | 說明 |
|---|---|
| Name／Curve name | 接縫名稱；多條曲線可自動編號；系統會檢查名稱是否合法，重名時詢問是否覆蓋 |
| Type／Block Limit | 普通接縫或分段界線接縫（Block Limit，部分視圖以粗線畫） |
| Symmetry | 兩舷皆有、單舷、或跨中心線（為了讓板跨過中心線而延伸到對舷的對接縫，**不要**登錄成跨中心線） |
| Bevel | 接縫預設斜角，當它用作板邊時成為預設，可被外板覆寫 |
| Limit 分頁 | 限制盒 Xmin…Zmax，可用肋位；按鈕 Portside（Ymin=0）、Starboard（Ymax=0）、Any（跨中心線）、Default |
| Curve Data 分頁 | 曲線型態：主平面（Axis＋Coordinate）、平行曲線、兩物件間平行曲線序列 |

平行曲線的關鍵參數（與 Geometry 的 Parallel Curve 同）：

| 參數 | 意義 |
|---|---|
| Distance／Distance end 2 | 偏移距離；兩端不同則沿曲線漸變 |
| Method | X／Y／Z 沿主平面截曲面位移；**Perp** 沿垂直於原曲線的平面位移，可得兩邊等距的展開板，雙向使用可得（近）矩形板 |
| Excess End 1／2 | 位移前暫時延長曲線兩端，不改原曲線 |
| Approximate plane | 只位移三點（兩端與中點）並建平面，結果曲線為平面曲線 |
| Tolerance／Iterations | 精度（預設 3 mm）與最大迭代次數（預設 20） |

### 14.4.2 Create Shell Plate

建立外板。單板模式：依**順時針**（由曲面內側往外看）點選 3 至 12 條 Seam，**必須從較短的一邊開始**；多板模式：先依序點所有 Butt（由最艉者開始）→ Operation Complete，再點所有 Seam（由離中心線周長最大者開始）→ Operation Complete。資料在四個分頁輸入。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Shell Plate 的 General 分頁

*圖 14-2　Create Shell Plate 表單的 General 分頁，含名稱、位置號、材料（內外側厚度、材質）與通用字串。（AVEVA 官方文件截圖，僅供內部教學）*

| 分頁 | 主要內容 |
|---|---|
| General | Plate Name；Add Position No.／Add Symmetry Suffix／Auto Name（多板時依序編號）；PS／SB 位置號；Mat./Pos. Side（厚度正側，空白則為接縫順時針看的那一側）；Create closed plate（同一接縫區間可兩次作邊界，用於圓柱形外板）；Inside／Outside 厚度；Quality；Laminate；Parts List、Surface Treatment、Destination、Raw Plate、GPS 1–4 |
| Limits | 接縫清單（Add／Replace／Remove／Clear／Move Up／Move Down）、Developed plate limit（在展開用的理想四邊形中的邊號）、Excess、Compensation、Grinding、Bevel |
| Development | Workshop Method、Strip Control／Direction／No of Strips、Spline Tolerance、Neutral Plane Loc. Factor、Raw Plate Margin、Roll Axes、Shrinkage（縱向、橫向與其 Partition） |
| Production | Bending Template Info（樣板位置，會覆寫彎曲樣板功能的預設 ip 檔）、Marking Information（供 `cpanparts` 發放外板時的標記，選項 IP 表示依 ip 檔） |

補償（Compensation）：沿板邊加上線性遞增或遞減的長度；正值表示沿板邊環繞方向由 0 漸增到給定值，負值反之。同一板邊若同時定義斜角與超長，通常**斜角間隙會被忽略**；設環境變數 `SBH_BEVELGAP_AT_EXC = <r>` 則在 excess 不超過 r 時兩者並存。Drafting 預設值 `HATCH_SCL_MODE` 應設為 0 才能得到合理的剖面線。

### 14.4.3 Create Shell Profile 與傾角點

由軌跡曲線建立縱骨或橫骨（選取清單的行為與 Seam 類似）。為精確控制特定位置的傾角，一個 Profile 最多可加 **100 個傾角點（Inclination Points）**；位置由軌跡與某物件（Seam、Hull Curve、平面、平板架或另一縱骨）或主平面的交點決定，角度在主平面內相對於軸正向量測：

| 平面 | 表單選項 | 0 度沿 | 90 度沿 |
|---|---|---|---|
| X-Y | XT | X 軸 | Y 軸 |
| Y-Z | YT | Y 軸 | Z 軸 |
| X-Z | ZT | Z 軸 | X 軸 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕傾角點表單

*圖 14-3　Inclination Points 表單：Axis/Type、Position/Name、Incl. Type、Angle，以及 Add／Copy／Remove／First／Prev／Next／Last 按鈕。（AVEVA 官方文件截圖，僅供內部教學）*

**Split Symmetric Profile**：把對稱縱骨拆成左、右舷專用兩根，連帶所有 Stiffener、軌跡曲線與拓撲相連物件一起更新（如跨中心線橫骨上對應縱骨的切口，會變成左右各一）。傳統命名下右舷縱骨號碼為原號加 2000（橫骨加 5000）；自由命名時加字尾 S。以 Apply 確認，以 Deactivate 撤銷，撤銷其中一根會連動撤銷另一根。

### 14.4.4 Shell Stiffener：Split、Combine、Modify Curve、To Manufacturing DB

| 功能 | 作用 | 要點 |
|---|---|---|
| Split | 以 Seam、暫時曲線、平面、縱骨或平板架把 Stiffener 切成更多段 | 一次可切多根、用多個切割物件，但**同一次不能混用不同種類的切割物件**；與板架或縱骨相交時兩端會依板厚錯開；新端點取預設端切（垂直）與連接碼 |
| Combine | Split 的反向 | 條件：屬於同一縱骨的同一曲線分支，且在軌跡上相鄰；資料不同時採選取清單中第一根的資料；型材種類不同時端切可能被改 |
| Modify Curve | 修改單根 Stiffener 的軌跡曲線 | 會建立新的曲線分支；用 Apply 確認 |
| To Manufacturing DB | 在製造資料庫產生生產用的 Stiffener 零件 | 後續 Shell Stiffener View 需要它存在 |

Stiffener 沒有獨立的 create 功能，修改它的表單分四頁：General（名稱前綴、流水號、Posno、GPS、Shrinkage mm/m、Weld Depth…）、Profile Data（Symmetry，設 Dummy 即無材料的虛擬構件；Bevel Trace；Automatic Bevel 即 Dotori；Type、Parameters、Quality、Laminate、Bead）、End Data（Incl. Type：Default／Perp／Perp Whole／XT／YT／ZT；Conn. Code；Clearance；Endcut Type；Bevel Web／Flange；Excess）。修改多根時可用遞增重複式如 `1(2)9`、`100(-2)92`。若設定邏輯變數 `SBH_AN_POSNO`，GPS 1、2 會被當成字母數字位置號的前後綴（前綴 ABC、後綴 DEF、號碼 10，得 `ABC10DEF`）。

### 14.4.5 Create Feature：開孔、缺口、切口、標記線

Hole、Notch、Cutout、Marking 統稱 **feature**，**一律定義在 Shell Profile 層級**，一次定義可在多根縱骨上產生大量 feature；同一定義、同一縱骨的 feature 屬於一個 feature group，**不能只刪組內某幾個孔，要改整組定義**。

| 功能 | 位置決定方式 | 說明 |
|---|---|---|
| Hole | Positions＋Axis（座標或重複式） | Type：Standard／Arbitrary（取自物件）／Menu／Same As；Mirrored；Inclination Angle；Dist. From Trace |
| Notch | Reference：Coordinates／Normal Seams／Refl. Seams；Positions 可寫座標或 Seam 名稱，支援重複式 | 例 `ESS1010(10)1050,ESS1070`、`FR10(5)25`（每隔 5 肋位）；可勾選圖上點選 |
| Cutout | Reference：Normal／Refl. Profiles；Positions 填相交縱骨名 | 例 `ESL110(10)150,ESL170`；Cutout Type |
| Marking | Positions＋Axis | Length 或 Profile Height；Symmetric；Direction：Plane／Perp／Angle；Marking Text |

可選的標準孔與缺口可自訂（官方指向 *Customizing dialogs in Hull*，本章未讀）。

### 14.4.6 曲面板架（Curved Panel）與開孔

建立曲面板架只是**蒐集既有外板與 Stiffener**，所有零件會依命名規則自動改名。表單欄位：Panel Name、Sym（PS／SB／PS+SB／Over CL）、Block Name、Shrinkage 與 Partition（板的預設收縮，未設者繼承）；修改模式才有 Add／Remove Plates 與 Stiffeners 以及 Handle Holes。對稱板架內的外板也必須對稱；跨中心線板架可含任何板。

**板架上的開孔**是廣義概念，三類：

1. 標準孔；2. 任意封閉輪廓，視同標準孔；3. 封閉或開放輪廓、以轉換矩陣定位（存於 Form Data bank 的平面曲線物件）。

類 1、2 以「參考點沿某線投影到曲面」定位，線可平行於主軸或過兩點；類 3 沿其局部座標 w 軸投影，多重交點時要給近似座標。開口可作**標記**或**切割（burnt）**；重量重心計算**只計入切割的孔**。孔會自動歸屬到所屬外板，可跨板界，輪廓在轉入板資料庫時自動加入展開板。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Handle Holes 表單

*圖 14-4　Handle Holes 表單：Designation、Hole to be（Developed）、Hole Along、PS/SB、Excess／Compensation、Bevel／Dotori、Grinding。（AVEVA 官方文件截圖，僅供內部教學）*

要點：Developed 勾選則算孔柱與曲面的真正交線，否則保留原形（圓孔仍是圓）；Compensation、Excess 只對將成為外輪廓的孔有意義；Bevel 可給明確代碼或用 Dotori（連續變化斜角，並指定 Bevel set）。孔曲線取點距離受暫時環境變數 `SBH_HOLEMARK_PART` 控制，預設 500 mm，縮小可提高精度但降低效能。**Combine Curved Panels** 只能合併板相鄰的板架，不能合成含板洞或板島的板架。

### 14.4.7 其他 Model 功能

| 功能 | 說明 |
|---|---|
| Create Hull Curve | 把暫時曲線存成具名 Hull Curve；若名稱符合專案設定的肋位、縱剖線或水線前綴，後接不超過 32767 的整數，且曲線在對應主平面上，則**同時更新肋位／縱剖線／水線表**（例：平面 X=FR40、名稱 `ESX40`、前綴 `ESX`）。Auto Name 用 `<…>` 標出遞增部分，如 `AB<10(5)20>C` 產生 `AB10C`、`AB15C`、`AB20C` |
| Create Storable Plane／Point | 把暫時平面／點存成具名物件，名稱任意，Auto Name 規則同上 |
| Delete | 刪除模型物件與縱骨 feature；刪縱骨會連帶刪其 Stiffener 與軌跡曲線 |
| Recreate | 重新計算物件。例：ESS100 定義為平行於 ESS101，ESS101 移動後選 ESS100 再 Recreate，即重新平行 |
| Modify | 修改各類物件，表單與建立時相同並帶入原定義 |
| Topology | 沿相依樹找物件：Dependent primary（直接依賴者，如某 Seam 圍出的外板）、Dependent all、Defining（被誰定義）、List names、Select（放入選取清單，可接著 Recreate）、Undo、Cleanup |

> **專業提醒：** 船殼曲面改了之後，不是逐物件修。官方建議用 Advanced Selection 的 **Select All Objects**（選出所有縱骨、板架、外板、Seam、Hull Curve、Storable Plane），再執行 Recreate；Stiffener 與 feature 會在對應縱骨重建前自動重建，不必另選。

## 14.5 Geometry、Default、View、Select 子選單

### 14.5.1 Geometry：暫時幾何物件

Geometry 建立的點、平面、柱面、曲線都是**暫時物件，只存在於工作區，不進資料庫**，由系統命名。想保存就要用 14.4.7 的 Create Hull Curve／Storable Plane／Storable Point，或由 Seam、縱骨等把它們收進去。

| 類型 | 方法 | 要點 |
|---|---|---|
| Point | Three Co-ordinates；On Surface（給兩座標，沿軸線與曲面求交，多重交點用 Approximate Coord 選最近者）；Curve + Plane／Plane Panel 交點；Moved Along Curve（重複式 `1000(2000)5000` 得 1000、3000、5000 mm）；At Intersecting Curves；Reflected（對中心線鏡射） | 基點若為點，須是由曲線交點或移動而來者 |
| Plane | Principal（`FR40(10)80`、`FR40,FR50,FR60`）；3 Points；2 Points + Axis（若兩點的曲面法向量近似同向，會自動選軸，可用 `NO_AUTO_PLANE_AXIS` 停用；兩點連線平行該軸時計算失敗）；2 Points + Angle；Rotated（主平面繞軸旋轉，角度**相對於所選軸而非基準面**）；Reflected | 平面顯示受限於 Default Box，但計算時無限延伸 |
| General Cylinder | 一般柱面：在 XY、XZ 或 YZ 平面的曲線 C（準線 directrix）沿垂直於該平面的直線 L（母線 generator）移動所成之面 | 三步驟：選母線軸向、定義準線（輸入或在垂直視圖點選）、設資料（Min/Max Coord、兩端角度；角度在 [-360, 360]，不得為 ±90、±270） |
| Shell Curve | By Plane；By General Cylinder；Parallel；Combined（選兩曲線再點起訖端）；From External Surface（取存於曲面中的曲線，例如早期 AVEVA Marine Lines 做的；Initial Design 曲面會列出全部曲線）；Reflected | Modify 時可換曲面、改平面／柱面、改 Box、換曲線型態 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕一般柱面示意：準線與母線

*圖 14-5　一般柱面（General Cylinder）：準線 directrix 為曲線，母線 generator 沿它移動成面。（AVEVA 官方文件截圖，僅供內部教學）*

### 14.5.2 Default：Surface 與 Box

Surface 改預設曲面；Box 設六個座標（空白為無限）。**From View** 可從二維視圖（Shell Expansion 等）取範圍，**From Object** 可從 Seam、曲線、縱骨、Stiffener、Storable Plane 取範圍，Show 可圖形預覽。

### 14.5.3 View：全模型視圖

這些視圖與模型連動（不是靜態圖）：

| 視圖 | 內容與重點參數 |
|---|---|
| Shell Expansion | 外板展開圖，沿肋位曲線展開。參數：Side（PS／SB／Over CL）、Surface、Developed from、Limits（Stern／Stem／Upper／Lower）、Panels／Blocks／Seams／Longitudinals／Transversals／Curves 的包含或排除（Auto Selection ON 為排除）。板厚、材質、位置號可顯示，並可附板厚剖面線圖例 |
| Bodyplan | 橫剖線圖，多個肋位剖面疊合。Looking（Default 取自預設檔 `VIEWX` 關鍵字、FOR、AFT）、Long section image（Full／Mould／Tick）、Long section frame、Draw every_frame、顏色、Grid spacing |
| Developed Plate | 一或數塊展開外板；清單有板則顯示，否則點選 Seam 圍出外輪廓即時展開。若選的是既有板則不跳表單 |
| Shell Stiffener | 把 Stiffener 畫成彎曲前的直棒，標長度、剖面與反彎曲線；需製造資料庫已有生產零件 |
| Curved Panel | 把板架投影到適當平面（有胎架計算則用工廠地板）。可顯示內部 Seam、板號、材料、縱骨、端切、板架名、胎架行列與柱高（需胎架系統第二階段完成）、方向標記、開孔十字標記 |
| Recreate／Select／Modify | Recreate 依模型更新視圖（暫時物件也先重做）；Select 決定哪些視圖為 active（有框為 active、有 X 為 inactive）；目前只有 Curved Panel 視圖可 Modify |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Shell Expansion View Properties 表單

*圖 14-6　Shell Expansion View Properties：General、Limits 與各物件分頁（Panels、Blocks、Seams/Butts、Longitudinals、Transversals、Curves、Penetrations）。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Bodyplan View Properties 表單

*圖 14-7　Bodyplan View Properties：View properties 控制縱骨剖面畫法、間隔、顏色與格線。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕曲面板架視圖範例

*圖 14-8　曲面板架視圖範例：以方框標出板號、板厚與材質，格線為接縫與肋位曲線。（AVEVA 官方文件截圖，僅供內部教學）*

### 14.5.4 Select：選取與確認

| 功能 | 說明 |
|---|---|
| In Drawing | 在圖上點選物件，Options 進入進階模式；**要選 Stiffener 必須用進階模式**，否則預設選到 Shell Profile |
| Advanced Selection | 依名稱（`*` 任意多字元、`?`／`%` 單一字元）、型別、曲面、盒範圍組合條件；Action 為 Add／Remove／Restrict；Select All Objects；Apply 只更新計數；Pick、List、Undo |
| Apply | 確認變更；縱骨的 Stiffener 與軌跡曲線一併套用；**單根 Stiffener 的變更不能單獨 Apply，會連整根縱骨一起套用** |
| Deactivate／Deactivate All | 移出選取清單；未套用的變更會逐一詢問，Yes 還原、All 其餘不再問、No 保留。幾何物件不會被詢問 |
| List／Show Object Definition／Apply and Deactivate | 列出選取物件；查看定義；套用後立即移出（連暫時物件也一併移出） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Advanced Selection 表單

*圖 14-9　進階選取表單：名稱、型別、曲面與座標盒條件，加上 Add／Remove／Restrict 動作。（AVEVA 官方文件截圖，僅供內部教學）*

官方範例：選 40–60 肋位間所有物件 → 限縮為 Shell Profile → 排除名稱以 `EST23` 開頭者，可得 EST10、EST20、EST30，而 EST23、EST231 被排除。

> **常見錯誤：**（1）改了物件卻沒按 Apply 就關閉，資料庫沒有更新；（2）只想套用某根 Stiffener 的變更，卻一併改了整根縱骨；（3）用 In Drawing 想選 Stiffener 卻選到 Profile；（4）建立 Seam 時 Default Box 沒涵蓋右舷。

## 14.6 Batch、Hull Tools 與預設參數

### 14.6.1 Batch 子選單與 XML 輸入語言

- **Generate In Batch**：選取 XML 檔，啟動批次工作（在 Log Viewer 觀看）。
- **Output XML**：把選取的物件輸出成 XML 描述檔。支援點、平面、Hull Curve、Seam、Shell Profile、Shell Stiffener、Shell Plate、Curved Panel；**暫時物件會被忽略**。

XML 輸入語言的設計目標：一種語言涵蓋所有曲面模型物件、與互動式建模相容、使用開放的 XML 格式。語言本身的詳細說明在另一份 *Hull Model Concept* 文件，**本章未讀**，故不列元素名稱〔待核對〕。

### 14.6.2 Hull Tools 選單（與平面建模、結構設計共用）

| 功能 | 說明 |
|---|---|
| Create Curve | 以一或多個平面切曲面得曲線，存入 `SB_CGDB` 對應的船形資料庫；可選擇更新肋位／水線／縱剖線表。曲線名多條時用 `<前綴><起>(<步>)<迄>`，如 `SBX34()46`、`CUR10(0.2)10.8`；座標值用 `FR52(2)60+375` 之類，**名稱個數須等於座標值個數** |
| Store Curve | 把當前圖中的曲線存為 CAT 物件（非標準缺口、孔，或要重複當板邊界的複雜曲線） |
| Functional Description | 以互動方式指派功能描述（板架層級指派對其零件皆有效，也可在零件層級補充） |
| Default Parameters | 列出、修改、儲存、重設 Curved Hull 預設參數；儲存時只寫與標準不同者；未設定的布林參數顯示 `<NOT SET>` |
| Production Program Interface Hull | 生產與報表入口，屬製造章節（第 16 章） |
| Dimensioning | 沿曲線量測：從某曲線到其他相交曲線，可量 Hull Curve、Seam、Stiffener、胎架行列曲線、肋位曲線、平面板架界線、孔十字標記；所有量測須從同一曲線出發；相交缺失時**靜默跳過** |
| Coordinates and Angles | 檢查曲面形狀：Search Angle（兩個主平面求交，報切線角）、Search Coord（給主平面與角度，找所有切線角相等的點） |
| Recreate Limit Tables | 掃描資料庫重建 Seam／縱骨／橫骨的界限表（Structural Design 中此功能在 Project 選單） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Dimensioning 在曲面板架視圖上的量測結果

*圖 14-10　Dimensioning：由邊界 Seam 沿內部 Seam 量到縱骨的距離，起點為小圓、終點為箭頭。（AVEVA 官方文件截圖，僅供內部教學）*

### 14.6.3 預設檔 sh700.sbd

曲面船體的行為由預設檔控制，檔名為 `sh700.sbd`，置於環境變數 `SB_SHIP` 所指目錄；一般互動預設檔為 `SBD_DEF1`，若在 `SBGD_DEF` 目錄有 `SBD_CHM.DEF` 則改用它。檔案是純文字，規則：值以 `=` 或 `:` 指定、多值用逗號、一行一個參數、順序無關、**參數名不可縮寫**；不寫的參數取系統預設。

| 群組 | 參數與意義 |
|---|---|
| General | `FR_TERM_OUT`（-1 不用肋位表示；0 含可能的偏移，預設 0）、`LP_TERM_OUT`（-1、0、1 僅偏移為零、2 含半個 LP；預設 1）、`TRACEON`（輸出測試資訊，僅供維護） |
| Shell Expansion | `SHX_PARTITION`（展開曲線間距，預設 5000）、`SHX_ENDCUT_SYMB`、`SHX_BUTTS_OVER_CL`、`SHX_HOLE_SIZE`（預設 50 000 mm²）、`SHX_HOLE_DIST`（預設 200 mm）、`SHX_LNO_DIST`、`SHX_DRAW_PLATES`（TEXT／DRAW／未設）、`SHX_SHOW_POSNO`、`SHX_SHOW_MATQ`、`SHX_NO_SHELLPLATES` |
| Plate Development | `PDV_NO_ROLLAXIS`、`PDV_STRIP`（x／y／z，通常展不開時指定）、`PDV_METHOD`（Expansion／Contraction／No Deformation）、`PDV_RAW_PLATE_MARGIN`、`PDV_NUM_STRIPS`、`PDV_SPLINE_TOL` |
| Modelling | `DEF_YMIN_NO_LIMIT`、`NO_AUTO_PLANE_AXIS` |

符號視圖的參數沿用 Planar Hull Modelling 的預設檔，此處不重複（Drawing Development 子頁未讀）。

## 14.7 外板展開方法與生產雜項

### 14.7.1 外板展開（Shell Plate Development）

鋼板零件由平面原板切割，因此非平面的外板要有工具把三維板轉成平面形狀，成形後才能吻合空間中的界線。常見工法是**收縮成形**（加熱冷卻使局部收縮）；替代法是**擴張成形**（局部或整體加壓）。系統可配合工法，並輸出原板尺寸、所需收縮／擴張量與分布、主要曲率方向。純冷作成形可設環境變數 `SBH_COLDFORMING`。

| 概念 | 說明 |
|---|---|
| 邊界／限制 | 外板須有 3–12 條 Seam；內部處理一律視為**四邊形**（最小外接矩形，邊 1、3 為兩端、邊 4 下長邊、邊 2 上長邊；邊 1 或 3 可塌縮成點作三角板）；超過四邊時系統自動把相鄰邊串成一條，必要時可在表單中手動接管 |
| 基準線（Baseline） | 在邊 1 與 3 之間產生的平面空間曲線，通常連兩端中點；展開後在草圖中以紫色虛線畫出；限制與分條方向一定後無法再改 |
| 分條（Strips） | 沿基準線等分成條，每條由兩條平面分條曲線界定。三種控制：主平面、垂直於基準線（Perpendicular）、沿邊 2 與 4 等比分佈（Distributed）。條件：每條須與基準線及邊 2、4 恰好各交一次，且彼此不相交 |
| 輪廓 | 每條切成相連三角形「滾開」，輪廓是通過各條導出點的樣條。條數有限，**細節如圓角半徑可能無法精確保留** |
| 間隙／重疊 | 各條接合後不可能完全吻合：收縮法留間隙（要靠成形時收縮消除），擴張法記成重疊。可指導工人在何處需多少壓力 |
| 滾軸（Roll Axes） | 主、次滾軸由最大相對曲率的兩條邊定義，導引初始輥軋；純圓柱時兩軸重合；草圖中主軸為粗實線 |
| 特殊板 | 封閉圓柱（如艏側推器通道）與封閉廣義錐面：須有一條「切開」的 Seam，在定義中**出現兩次**並勾選 Create Closed Plate；例：`B/A/B/C` |

> 〔公開版未收錄：AVEVA 官方產品截圖〕三種分條控制的比較

*圖 14-11　三種分條控制：Principal plane、Distributed、Perpendicular baseline。官方指出出現不唯一交點（knuckle）時改用 Perpendicular Baseline 可解。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕展開外板的檢查草圖

*圖 14-12　外板展開的檢查草圖：外接矩形尺寸、基準線（點劃線）與各段間隙／重疊數值。（AVEVA 官方文件截圖，僅供內部教學）*

草圖中的板輪廓是**名義值**，不含 excess、收縮與斜角間隙補償（外接矩形的計算則已考慮 excess 與斜角間隙，但不含收縮）。

> **專業提醒：** 展開失敗時的處理順序：先改 Strip Control（Perpendicular／Distributed），再指定 `PDV_STRIP` 或表單中的 Strip Direction，最後才考慮把幾何簡化成「包絡」再用廣義孔扣除（官方圖例說明某些邊沿會使任何主平面分條都有多重交點）。

### 14.7.2 Mould Data on Shell Members、Hull Geometry Utility 與參照驗證

| 程式 | 執行檔／入口 | 用途與輸入 |
|---|---|---|
| Hull Mould Data on Shell | `sf408d`，經 Job Launcher（JL）；`SB_INPUT1`（`.dat`）、`SB_OUTPUT1`（`.log`） | 產生肋位曲線與縱骨、Seam 或其他 Hull Curve 的交點與周長；輸入語法 `OUTPUT,<字串>;`、`FRAME/FROM=<整數>/TO=<整數>/Step=<整數>`（1–10 句）、`SEAM/…`、`LONG/…`（各最多 10 句）、`CURVE,<字串>;`（最多 100 句）；**SEAM、LONG、CURVE 不可混用**；結果檔預設放 `SB_SHIPPRINT` |
| Hull Geometry Utility | `sf304d`，JL；`SB_INPUT1`（`.dat`）、`SB_OUTPUT1`（`.lst`） | 任意曲線相交等幾何計算，輸出固定關鍵字的通用檔，便於客製後處理。輸入以空白分隔的「記錄」，首項為記錄編號：1 設曲面名、2 一群曲線的座標／角度、3 單曲線、5 曲線與 xyz 平面交點兩側角度、7 兩空間曲線交點、14／15 xyz 與 uvw 轉換、16／17 交點角度、18 把 SBH3 3D 曲線轉成 SSP Hull Curve；單獨輸入 `H` 會把輸入選項印在 log |
| MarHullVerify | 批次程式 | 驗證 Curved Hull 物件間的參照，指出每個物件參照了誰、哪些參照錯誤。輸入 XML（根元素 `<Verify>`，子元素 `CurvedPanel`、`ShellPlate`、`ShellProfile`、`ShellStiffener`、`HullCurve`、`Seam`、`Plane`、`Point`，屬性 `ObjId`，可用萬用字元如 `SIDE*`、`*`）；`SB_INPUT1` 指輸入 XML，`SB_OUTPUT1` 指 log（會被覆寫）；參數 `-ns` 不驗證 XML 語法（仍檢查剖析錯誤，可直接吃 Curved Hull 輸出的 XML）、`-nx` 純文字輸出、`-v` 詳列所有參照（僅文字模式）；用 `MarEnvUtil` 設環境參數 |

## 14.8 Optional Hull Functions：選用功能

官方此節是一頁式「功能目錄」，每項選用功能只簡述其目的，並指向其他章節的詳細說明。

| 選用功能 | 解決的問題 | 官方指向的詳細文件 |
|---|---|---|
| FRP Hull Modelling | 玻璃纖維強化塑膠（FRP）船體：內外殼曲線（以母曲面產生平行曲面）、芯材與表層積層分別控制（以可修改的積層表定義代號、密度、厚度）、特殊加強型式、接頭加強珠（bead）及其重量重心、孔緣處理、FRP 專用符號圖規則 | Hull／Set-up and customization／(Fiber) Reinforced Plastics |
| Stiffener Nesting | 把來自平板架（stiffener、face plate、pillar）與外板縱骨的型材零件，自動套排到使用者提供的原料型材堆上；可考慮端切與對稱截面的方向；結果存特殊資料庫，輸出收料清單與排版圖，可作為型材切割機器人線的基礎 | Hull／Stiffener Production |
| Splitting of Built Profiles | 組合型材（腹板與面板在船廠焊接）與扁鋼的生產資訊：腹板轉為板零件，面板轉為板零件或新型材零件；全自動，由客戶撰寫的控制檔決定，判定條件為型式、尺寸、長度、斜角定義、材質 | Hull／Stiffener Production |
| Painting Areas | 計算艙室與表面的鋼構塗裝面積 | Planar Modelling／Interactive Planar Hull Modelling Functions／Painting Areas |
| Generic Post Processor - Plate Cutting（GPP） | 針對各廠牌切割機與控制器，從通用「排版板」檔格式產生控制資訊；部分機型支援文字標示與開斜角；並非所有控制器功能都支援 | Hull／Generic Post Processor |
| Factory Automation | 一組自動化與精度控制選項，常整合在各設計功能中（以下六項） | 另有 *Factory Automation* 文件 |

Factory Automation 下與船體相關的六項：

| 子選項 | 說明與指向 |
|---|---|
| Profile Cutting Interface | 為切割機器人或外部型材製造軟體建立基礎資料（Hull／Manufacturing／Profile Manufacturing、Profile Interface、Profile Cutting Interface） |
| Dotori | 連續變化斜角角度的計算，支援角焊用斜角的定義與使用（Bevel Handling、Profile Cutout Standards、Weld Statement） |
| Plate Cutting Interface | 把資料庫中的板零件取出成通用格式，供 AVEVA Marine 以外程式處理（Hull／Manufacturing／Plate Manufacturing／Plate Interface） |
| Genauigkeit（GSD Marking Triangles） | 組立標記三角形，用於組裝對位或組裝後精度檢查（Alignment Marking／Marks for Assembly） |
| Reference Planes | 船廠可在產品模型中加入對位用參考面，並標記在板與型材上（Alignment Marking／Reference Planes） |
| Extended Shrinkage Handling | 自動擴充收縮補償（可手動覆寫），在自動由船體模型擷取零件時套用，補償加熱收縮（Shrinkage Compensation） |

> **專業提醒：** 選用功能多半是**授權選項**，頁面本身沒寫授權名稱與啟用方式。公司是否有這些選項、各選項在 ADMIN 中如何啟用，一律〔待核對〕，不要在教材中假設一定可用。

## 14.9 Miscellaneous Utilities：雜項工具

這些工具的共同模式相同：**由互動式船體應用經「生產程式介面（Production Program Interface）」的通用選取工具自動產生輸入檔，再用 Job Launcher 執行批次程式**，所有資料都取自板與型材資料庫，因此**前提是零件已自動產生**。輸出多為逗號分隔檔（可用 Excel 或任意報表工具客製），部分可輸出成圖。

| 工具 | 執行檔 | JL 名稱 | 輸入／輸出 |
|---|---|---|---|
| Parts List | `sf101d` | Hull Parts List | `SB_INPUT1`（`.dat`）、`SB_OUTPUT1`（`.log`）、`SB_OUTPUT2`（`.csv1` 板）、`SB_OUTPUT3`（`.csv2` 型材） |
| Material Ordering of Bars | `sf500d` | Hull Material Bars | `SB_OUTPUT2` 為清單檔（`.lst`），`SB_OUTPUT3`、`SB_OUTPUT4` 為暫存可刪 |
| Material Ordering of Plates | `sf501d` | Hull Material Plates | 同上；控制檔 `matplate.ip` |
| Material List for Nestings | `se032` | Hull Material Nestings | `SB_OUTPUT2`（`.csv1` 板）、`SB_OUTPUT3`（`.csv2` 型材）；依頂層組立排序 |
| Material List | `sf103d` | Hull Material List | 蒐集零件的排版參照，適用小型船廠或檢查；進階領料建議由 Production Data Interface 處理 |
| WCOG Weight Calculation | `sf102d` | Hull Weight & COG | `SB_OUTPUT2` 板零件；控制檔 `wcog.ip` |

ip 檔放在 `SB_SHIP` 所指目錄。

### 14.9.1 零件表（Parts List）

控制檔 `partlist.ip` 目前只有 `SINGLE_LINE`：預設下列屬性相同的零件行會合併——零件名（依 part name control）、分段名、組立名、排版所在；定義 `SINGLE_LINE` 則每個零件單獨一行。

板零件表欄位（依序）：Part name、Quantity、Block、Side、Weight、Stock Number、Steel quality、GPS 1–4、Ship number、Identification（來自建模時的 `LIS` 敘述）、Nested on、Type of Part、Area、Length、Width、Thickness、左舷數、右舷數、Functional property index／description、Assembly name、Position number、Tribon part name。型材零件表把 Area／Length／Width／Thickness 換成 Shape（HP、FB…）、Dimension string、Length，並多一欄 Profile sketch。

輸出圖需要標準資料庫（`SBD_STD`）內已定義零件表用圖框；圖存於 `SBH_PARTLIST_DWG` 與 `SBH_PARTLIST_DWG_PADD` 指向的 PADD 資料庫，未指定時存在標準圖所在 PADD（`SB_PDB_PADD`）；`SBH_NSKETCH_DWG` 應指向自己（相關圖框名稱與規則子頁未讀）。

### 14.9.2 領料（Material Ordering）

- **Bars（型材）**：清單依序排序：識別號（每個新號換頁；由分段號、板架號與流水號組成，流水號在任一位變動時從 01 重新開始）→ 分段號 → 型式 → 尺寸 → 長度遞增。表頭欄位 `LOC TYPE PROF NO LENGTH TYPE A B S T EXCESS ENDCUTTYPE NOTES`；長度含製造 excess；型式依 VIS 標準；L 型或 T 型由扁鋼焊成者拆成兩行；NOTES 欄用代碼註記（`BR,<no>` 肘板上型材、`H,<no>` 孔內、`L<no>`／`T<no>` 縱橫骨、`FR<no>`／`LP<no>` 肋位或縱向位置；`FB` 表示曲率超過可彎值，**恐無法彎曲**）。船名字母取自 `SB_HREF`，沒定義則取板架名首字母；廠名取自 `SB_YARD`（最多 45 字元）。
- **Plates（板）**：板可屬平面或曲面板架，也包含該板架的肘板。`matplate.ip` 的 `STEELDENSITY, <density>,`（噸／立方公尺，預設 7.86）與 `EXCESS, <excess>,`（平面板每邊每長寬方向加的毫米數，預設 15 mm，**只適用平面板**，展開板的 excess 由展開程式控制）。重量由零件實際面積計算，廢料百分比由外接矩形與零件面積算出；沿長與沿寬的 excess 由各 excess 區間的右手法向量最大分量決定：`EXCESS,LE = |e2| + |e3|`、`EXCESS,BR = |e1|`。
- **Material List for Nestings／Material List**：以排版為單位的清單，結果為逗號分隔檔。

### 14.9.3 重量重心（WCOG）

計算分兩步：（1）板架存檔時為每個元件算**初估值**，不考慮板的 excess、收縮與補償，也不考慮型材的端切、缺口、切口與孔；（2）以 `ppanparts`／`cpanparts` 發放生產時算**精確值**，含與不含 excess 及收縮兩組，兩組值都存在板架、曲面板或 Shell Stiffener 物件中。

| 元件 | 計算要點 |
|---|---|
| 平面板 | 外輪廓面積與力矩減去內輪廓（孔），重量＝面積×板厚×鋼密度（密度取自品質控制檔）；重心移到板厚中心 |
| 直型材／直面板 | 模型線長×剖面積×密度；剖面依指定角度旋轉並移到板架指定側（考慮第一塊板厚） |
| 曲面板（外板） | 面積×板厚×密度；**孔不納入計算** |
| 曲型材 | 自 `SB_OGDB` 讀取；模型線依屬性 101（DIC）的 `ss`、`se` 在端點縮短；剖面轉到 (ts+te)/2 角；調整中性軸長度使端切可視為垂直而體積不失真 |
| 肘板、夾板（clip） | 肘板輪廓含缺口與切口，減孔；夾板重心取中心並考慮板厚位移 |

`wcog.ip` 參數：`WCOG_MODE, EXACT | EXACT_WITHOUT_EXCESS`（取含或不含 excess 與收縮的精確值；尚未精確計算則回傳簡易值；可放在 `START_GROUP`／`END_GROUP` 之間）、`WCOG_SEP_BUILT_PROF`（組合型材分成腹板、面板兩行）、`WCOG_DATE_MISMATCHES`（板架修改後尚未重新產生零件時，仍依 `WCOG_MODE` 取值）。**屬性 `GWEI` 為零件設計重量，`MANWGH` 為製造重量**，兩者的差別與各設定下顯示何者，官方以圖說明。輸出檔欄位有 Weight、COG X／Y／Z、Panel、Block、Type of part、Side、Steel quality、GPS 1–4、Nested on，以及板的面積、外接長寬、厚度、或型材的 Shape、Dimension string、Total／Moulded length。

### 14.9.4 船體標記（Hull Marks）

在平面與曲面板上標記文字與符號。字源有六種：TrueType 字型、符號字型（Symbol font）、設定圖（Settings drawing）、一般或標準副圖（Subpicture）、DXF 檔，或螢幕上選取的幾何。

| 概念 | 說明 |
|---|---|
| Hull Text | 任意字元與符號序列，以 Hull Tools > Hull Text 建立（Key in／By symbol）、修改、儲存；存成特殊的「Hull mark texts」圖，所在資料庫以環境變數 `SBH_MARK_PICT` 指定 |
| Hull Mark | Hull Text 投影到曲面或平面板架的結果，以 Hull Tools > Hull Mark > Create 建立。型態兩種：**切成板零件再焊到被標記板上**（Plate），或沿字元輪廓**走焊道**（Cont. Weld／Weld Pattern）。存於 Hull mark world（`HMKWLD`，**須事先存在**） |
| 設定圖作字型 | 每個視圖含單一子視圖；元件名 `L`（下點）、`U`（上點）、`M`（參考點）；若要當作字型使用，視圖名必須是對應字元的 ASCII 碼 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Hull Mark 對話框

*圖 14-13　Create Hull Mark：Hull Mark Type、Placement（Surface／Panel、Perpendicular）、Looking（Reference Point、Looking from／towards、Rotation Angle）。（AVEVA 官方文件截圖，僅供內部教學）*

要點：Perpendicular 勾選時沿曲面法向量投影以減少失真；Looking towards 設為 Any 時只有平面板架可朝任意方向投影；**不支援有折角（knuckled）的板架**；Reference Point（Left／Middle／Right）決定放在 Looking from 的那一點，方便在左右舷放置船名。板零件命名為 `<hull mark name>-<流水號>`。標記線會在零件發放時自動加入：平面板由 `ppanparts` 發放，受其 ip 檔關鍵字 `HULLMARKINGS` 控制；外板由 `cpanparts` 發放，受 `MARK_HULLM` 控制；外板標記品質受展開條數與 `SBH_HOLEMARK_PART` 影響。

## 14.10 二次開發者怎麼接

官方這三個子樹**沒有任何 PML 指令**，也沒有曲面船體物件的屬性字典。以下只列文件有依據的介面：

| 介面 | 依據 | 用途 |
|---|---|---|
| Output XML／Generate In Batch | 14.6.1 | 把互動建好的物件輸出成 XML；或以 XML 檔批次產生物件。XML 元素細節在 *Hull Model Concept*〔待核對，未讀〕 |
| MarHullVerify | 14.7.2 | 批次驗證參照，輸入輸出皆為 XML，可納入 CI 式自動檢查；需以 `MarEnvUtil` 設 `SB_INPUT1`／`SB_OUTPUT1` |
| JL 批次程式的輸入輸出檔 | 14.7.2、14.9 | `.dat` 輸入、`.log`、`.lst`、`.csv1`、`.csv2` 輸出；CSV 欄位表已列於 14.9，可直接寫報表程式或匯入 ERP／MIS |
| ip／預設檔 | 14.6.3、14.9 | `sh700.sbd`、`partlist.ip`、`matplate.ip`、`wcog.ip` 為純文字，可由程式產生或版控 |
| 環境變數 | 全章 | `SB_SHIP`、`SBH_FREE_SEAMPROF_NAMES`、`SBH_COLDFORMING`、`SBH_HOLEMARK_PART`、`SBH_BEVELGAP_AT_EXC`、`SBH_AN_POSNO`、`SBH_MARK_PICT` |
| 資料庫屬性 | 14.9.3 | `GWEI`（設計重量）、`MANWGH`（製造重量）為文件明講的屬性 |

下列為文件**沒有說**，必須實測〔待核對〕：Curved Hull 物件（Seam、Shell Plate、Curved Panel 等）在 DB 中的元素型別與屬性名；`CPANEL` 的成員關係（第 9 章已提到 `CPANEL` 屬於 `BLOCK`，但曲面船體實際存放在 `SB_` 開頭的船體資料庫而非 DESIGN 資料庫，兩者的橋接方式文件未寫）；是否能用 PML 直接操作這些物件；Vitesse（[第 36 章](ch36_hull_vitesse_zh-TW.reading.html)）能呼叫哪些曲面船體功能。

> **專業提醒：** 曲面船體的物件**儲存時會把依賴的暫時幾何定義收進物件本身**，且曲面改變後要 Recreate。所以任何讀取外部曲面或幾何的程式，**不能假設資料庫裡的曲線形狀永遠與曲面一致**；寫自動檢查時，應先確認 Recreate 已執行，再讀資料。

## 14.11 本章小結

1. Curved Hull 在互動畫面裡以「物件－動作」建模，工作區含多視圖，選取清單與 Apply／Deactivate 是資料是否進庫的關鍵。
2. 物件階層：Seam／Butt → Shell Plate；Shell Profile → Shell Stiffener；兩者收進 Curved Panel。Shell Profile 在現實並不存在，生產的是 Stiffener。
3. 縱骨的 feature（孔、缺口、切口、標記線）定義於 Profile 層級，成組管理。
4. Geometry 功能產生的是暫時物件；要保存須用 Hull Curve、Storable Plane／Point，或收進 Seam 與縱骨。
5. 外板展開是「基準線＋分條＋滾開」的演算法，成形方法（收縮或擴張）決定間隙或重疊的意義。
6. 七類選用功能多半是授權選項，官方此處只給目錄式說明。
7. 零件表、領料、WCOG 皆為 JL 批次程式，輸入輸出檔固定，是二次開發最容易下手的介面。
8. 船體標記以 Hull Text 投影成 Hull Mark，在 `ppanparts`／`cpanparts` 發放零件時自動加入標記。

## 14.12 練習題／自我檢核

1. 為什麼說「Shell Profile 在現實中不存在」？它與 Shell Stiffener、軌跡曲線的關係是什麼？
2. 某縱骨名為 `ESL120`，將第一段 Stiffener 切成兩段後，新段叫什麼？若縱骨為左舷專用，名稱又如何變化？
3. 建立外板時，要依哪個方向、從哪種邊開始點選 Seam？如何建立圓柱形封閉外板？
4. 你選了 40–60 肋位間的所有物件，只想留下橫骨，並排除 `EST23*`。請寫出 Advanced Selection 的操作步驟。
5. 曲面船形更新後，如何一次把相關物件全部重新計算？為什麼不必另選 Stiffener？
6. 比較 Principal plane、Distributed、Perpendicular baseline 三種分條控制，並說明何時要改用第三種。
7. 設計一個自動檢查流程：用 MarHullVerify 驗證某艘船所有以 `SIDE` 開頭的外板，需要哪些環境設定與命令列參數？
8. `GWEI` 與 `MANWGH` 有何不同？`WCOG_MODE, EXACT_WITHOUT_EXCESS` 影響的是哪一種？
9. 若要為船廠產出領料 CSV，要考慮哪些 JL 程式與輸出檔？零件需先滿足什麼條件？
10. 為什麼 Hull Mark 不能放在有折角的板架上？它與 `HMKWLD` 有何關係？

## 14.13 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 14 章](appx_d_verification_zh-TW.reading.html#ch14)；取材覆蓋與未讀範圍：見[附錄 E 第 14 章](appx_e_coverage_zh-TW.reading.html#ch14)。
