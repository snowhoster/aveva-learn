# 第 39 章　通風與設備設計：HVAC Designer 與 Equipment

> [第 7 章](ch07_outfitting_zh-TW.reading.html)用一節篇幅介紹過設備（`EQUI`）與通風（`HVAC`）的資料結構。這一章把兩者拆開來，當成兩門完整的設計工作：**Equipment 負責把一台泵、一座壓力容器、一台熱交換器變成帶有管嘴與定位點的 3D 模型；HVAC Designer 負責把風管、風門、消音器、空調箱連成一張可預製、可出圖的風管網路。**
>
> **資料可信度：** 本章的操作流程、視窗與選單名稱、元素型別與屬性名（`EQUI`、`NOZZ`、`DPSE`、`ASSOC`、`TESTEV`、`HVAC`、`BRAN`、`HSLIST`、`HSPOOL`、`DESP[n]`、`WKSF` 等）與少數 PML 範例，取自 AVEVA Marine 12.1 官方離線文件的 *Equipment*、*HVAC Administrator*、*HVAC* 三份指南。原文是 PDMS 時代的使用者指南，仍寫 PDMS、PARAGON、`%pdmsui%` 等舊名稱，本章照原樣保留。官方的 PML 範例只出現在 HVAC Administrator（Spool、Sketch、Joint 存放）與 Equipment 的表達式與報表欄位；**其餘「怎麼用程式取資料」一律標〔待核對〕**。圖片皆為官方截圖，僅供內部教學。

## 39.1 學習目標

讀完本章，你應該能夠：

1. 說明 `WORLD → SITE → ZONE → EQUI／HVAC` 的資料階層，以及為何建議按專業把設備、管路、通風放在不同 ZONE。
2. 依步驟建立設備、子設備、基本體（Primitive）、負基本體、管嘴與電氣元件，並說明 P-point 在定位中的角色。
3. 區分「手工用基本體建模」與「從 Specification／Selection Table 建立標準設備」，並說明參數化設計樣板（Design Template）的三類參數。
4. 使用 Positioning Control、Equipment Point、Orientate、Connect 與 Model Editor 把設備放到正確位置與方向。
5. 建立、測試與回報 Equipment Association（Mate、Align、Parallel 等八種），並用 Association Manager 與 Equipment Report 取得檢查結果。
6. 說明 HVAC 階層（`HVAC → BRAN → 元件`，以及 `HSLIST → HSPOOL`）與 HVAC Window 的 Categories／Available Types 操作模式。
7. 說明 HVAC 管理者需要準備的東西：樣本型錄、Detail Specification、Insulation Specification、Joint、Stiffener、Defaults、使用者自訂風管配件。
8. 依序建立 HVAC System、Main Branch、元件與 Side Branch，正確選擇 Joint 與 Connect 方式，並用 Autofill 把隱含風管換成實際直管。
9. 使用 Divide Main、Assembly、Tiles/Grid、Itemizing、重量／重心、Data Consistency 與 Split HVAC 等輔助工具。
10. 說明 HVAC Spool 的產生、驗證、修改，以及 HVAC Sketch 如何從 Design 的 Spool 資料出圖，並指出哪些二次開發介面有官方依據。

## 39.2 兩個模組怎麼分工

| 面向 | Equipment | HVAC Designer |
|---|---|---|
| 進入方式 | Design > Equipment | Design > HVAC Designer（也可由登入畫面直接進入） |
| 主要元素 | `EQUI`、`SUBE`〔待核對〕、基本體、`NOZZ`、電氣元件、設計點 | `HVAC`、`BRAN`、風管元件、`HSLIST`、`HSPOOL` |
| 圖形來源 | 手工基本體，或參數化設計樣板 | HVAC 型錄（Catalogue）的幾何集（Geometry Set）與點集（Point Set） |
| 與管路的介面 | 管嘴 `NOZZ`（見[第 21 章](ch21_pipework_zh-TW.reading.html)） | 風管嘴（HVAC Equipment Nozzle）與 Branch Head／Tail |
| 管理者工作 | 設備型錄與樣板（[第 8 章](ch08_catalogue_spec_zh-TW.reading.html)） | HVAC 型錄、Detail／Insulation Spec、Joint、Stiffener、Defaults |

兩者共用最上面三層：`WORLD` 擁有 `SITE`，`SITE` 擁有 `ZONE`。官方範例在 `SITE /SITE_EXAMPLE` 下分 `/AMO-EQUIP`、`/AMO-STRUCTURE`、`/AMO-CABLEWAYS`、`/AMO-HVAC`、`/AMO-PIPE` 五個 ZONE，並建議 SITE／ZONE 先留在原點。

> **專業提醒：** 元素必須由正確的上層擁有，所以建立前一定先確認自己站在對的階層：沒有 `SITE` 就不能建 `ZONE`，沒有 `ZONE` 就不能建設備。官方也提醒元素名稱不可含空白、**區分大小寫**，且資料庫內不得重名（`/YY9001A` 與 `/YY9001a` 是兩個名字）。

# 第一部分　Equipment（設備）

## 39.3 設備的概念與工作環境

官方的比喻是「像組裝塑膠模型，只是以 1:1 建模」：設備由一組**基本體（Primitive）**排列而成，在某個程度上模擬真實物件。實務上有兩條路：

| 路線 | 做法 | 適用 |
|---|---|---|
| 一次性設備 | 在 ZONE 下建空的 `EQUI`，再逐一加基本體與管嘴 | 專案專用、不重複使用的特製件 |
| 標準／外購設備 | 用 Create Standard Equipment 從 Specification 或 Selection Table 選型，填參數 | 泵、熱交換器、容器等可重複使用的標準件 |

官方說明：實務上通常用 Design Template 應用程式建立可跨專案使用、與型錄關聯的設備，特別適合第三方標準外購件；若設備只屬於單一專案，就不必放進型錄。

### 39.3.1 Equipment 工具列與基本設定

Equipment 工具列提供 Create Standard Equipment、Modify Properties、Modify Position、Modify Orientation 與 Navigation Level（箭頭可在設備、Sub Equipment、Element 等層級間導覽）。

| 項目 | 操作 | 重點 |
|---|---|---|
| 建 SITE／ZONE | 在 Design Explorer 導覽到 `WORLD`，Create > Site；再導覽到該 `SITE`，Create > Zone | 建 Zone 時要選 Purpose；範例名稱 `/A_DECK_AFT`、`/AWO-EQUIPMENT` |
| 命名 | 建立表單可直接輸入（不必打開頭的 `/`，系統自動補）；事後用 Modify > Name | 勾 Re-name all 會把設備、管嘴、子設備一併改成同一名稱前綴 |
| 命名慣例 | 管嘴通常是「設備名＋後綴」，如 `/YY9001-N1`、`/YY9001/N1`、`/YY9001/1` | 專案規格通常規定慣例，並可設定 Autonaming 規則 |
| List | Utilities > Lists；Add 選單可加入 CE、CE Members、Identified、Selection | Selection 可輸入元素型別與 PML 條件（`with Rule`），例如 `GTYP NE 'ANG'` |
| 匯入 | Utilities > Import Equipment Data | 從 CSV 或 XLS 匯入標籤、描述與其他屬性；細節在 *Design Common Functionality* 指南（本章未讀） |

List 的 Action 欄可直接對清單下指令（官方範例 `BY X 600`、`SPREF /DIN-SPEC/HE200A`），但官方建議不熟語法就搭配表單使用。

## 39.4 建立設備

### 39.4.1 Equipment Creation 表單

導覽到要放設備的 ZONE，Create > Equipment，開啟 Equipment Creation 視窗：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Equipment Creation 視窗：Name、Ship Position（FR、LH、LV 與 X、Y、Z）與 Attributes 欄位

*圖 39-1　Equipment Creation 視窗。上方以船舶座標（Frame、Lg Horz、Lg Vert）或世界座標定位，下方填 Description、Function、Design Code、Paint Specification、Inspection Schedule。（AVEVA 官方文件截圖，僅供內部教學）*

| 區塊 | 欄位 | 說明 |
|---|---|---|
| Ship Position | `FR`、`LH`、`LV` 與各自 Offset；`X`、`Y`、`Z` | 以船舶參考系或世界座標定位；官方也說可先建在 SITE 原點，之後再移 |
| 座標切換 | 圖示切換到 Outfitting coordinates | 可用另一個元素當參考（`wrt`，with respect to） |
| Lock | X／Y／Z 各一個核取方塊 | 固定該軸座標 |
| Attributes | Description、Function、Design Code、Paint Specification、Inspection Schedule | 其中油漆規格與檢驗計畫對應後面報表會用到的屬性 |

座標方向：X 東、Y 北、Z 上；負值用 -X、-Y、-Z。

### 39.4.2 子設備、基本體與管嘴

- **Sub-Equipment**：先選上層設備為 CE，再 Create > Sub-Equipment；表單的 Wrt 欄顯示上層設備，輸入 Name 與 Position 即可。
- **Primitives**：設備建好後，Create > Primitives 開啟 Primitives 表單，選 Cylinder、Box、Dish、Extrusion、Solid of Revolution 等。官方範例：圓柱 Height 500、Diameter 250，按 Create 後表單展開出 Datum、Position、Rotate、Align with P-Point。

| 功能 | 說明 |
|---|---|
| Levels（Used for） | 設定基本體在哪些細節層級（Representation level）可見，例如本體 1–3、底座 5–7、管嘴 8–10；目前可見層級由 Settings > Graphics > Representation 決定 |
| Datum | 把基準點移到原點或任一 P-point，方便之後重新定位 |
| Position | 相對另一元素（`wrt`）定位；官方建議先在 0,0,0 建好再移 |
| Rotate | 例如圓柱繞 X 軸轉 90 度形成槽體本體 |
| Align with P-Point | 讓目前元素對齊另一元素的 P-point |


**負基本體（Negative Primitive）**：必須屬於一個實體基本體。選實體基本體後 Create > Primitives，按 Switch to Negative Primitives，建立後旋轉、再進 Model Editor 用 Edit Members of Equipment 移到位。要看到孔洞，需到 Settings > Graphics > Representation 勾 Holes Drawn。

**檢查 P-point**：用 Query > General 選 P-points 逐點檢查，預設相對設備、也可選 world／site／zone。官方指出常見錯誤只會出在位置、尺寸、方向三類。盒子的 P0 在中心，其餘 P-point 在各面中心；圓柱有 P0 與兩端的 P1、P2。

**管嘴（Nozzle）**是設備與管路的介面點。它像其他基本體一樣定位、定方向、給高度，但**必須從型錄經 Specification 選取**（口徑由此給）：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Nozzle 視窗：Nozzle Type、Nominal Bore、Height、Position 與 Orientate P1

*圖 39-2　Create Nozzle 視窗。Nozzle Type 選型錄中的法蘭管嘴（例如 DIN2635 PN40 RF），Height 是管嘴長度，Orientate P1 is 決定管嘴朝向。（AVEVA 官方文件截圖，僅供內部教學）*


**電氣元件（Electrical Component）**：Create > Electrical Component，是設備與電纜的連接點（小到電纜密封套、大到發電機）。必須從型錄經 Selection Table 選取；可選 User Defined Element Type（建立在 `ELCONN` 型別之上）；建好後在設備原點，再用 Component Position 面板或事件驅動圖形定位，方向用 Orientate > Rotate 或 Axes。與[第 26 章](ch26_cable_supports_zh-TW.reading.html)的電纜設計銜接。

### 39.4.3 標準設備（Create Equipment 表單）

Create > Standard Equipment（或工具列圖示）從參數化設計樣板建立設備：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Equipment 表單：Name、Specification 選 CADC Standard Equip，下方列出 Vessels、Heat Exchangers、Standard Pumps、Air Coolers

*圖 39-3　Create Equipment 表單。選 Specification 後以問答方式逐層往下，直到 Selection complete；也可改用 Selection Table。（AVEVA 官方文件截圖，僅供內部教學）*

| 步驟 | 動作 |
|---|---|
| 1 | 導覽到 ZONE，輸入名稱（或用 Autoname，需專案已設規則） |
| 2 | 選 Specification（或 Selection Table）；Auto Select 在只剩一個選項時自動選 |
| 3 | 逐層選到 Selection complete；Current Selection 清單顯示目前選擇 |
| 4 | 按 Properties 開 Modify Properties 填參數；不填則用預設值；Plotfile 可看該設備的尺寸圖 |
| 5 | 按 Apply，出現 Positioning Control，用 Explicit Position 或游標拾取設備原點 |



### 39.4.4 設計點（Design Points）

Create > Points 建立或修改設計點；沒有點集時會建立 Design Pointset（`DPSE`）。點依型別存在對應元素：`DPCA`（Cartesian）、`DPCY`（Cylindrical）、`DPSP`（Spherical）。官方範例建立 Cartesian 點，Connection 選 `FBW`（Flange Butt Weld），Point Direction 填 `EZ`、Normal 填 `SY`，再用 Positioning Control 設 Ppoint 與 Snap 對準設備上的點，結果出現 `DP1`。設計點也是後面 Equipment Association 的參考特徵來源。

> **專業提醒：** 設備「長得對」不等於「資料對」。官方練習把錯誤分成尺寸、位置、方向三類，並提醒「所有設備都應在正交軸上定向」。建模完先用 P-point 查詢核對，再往下接管路。

**常見錯誤：** 負基本體放在設備而不是實體基本體底下；管嘴沒有選型錄（口徑無來源）；用 Create 建好卻忘記改管嘴名稱，導致後續管路 Head／Tail 參照難辨認。

## 39.5 定位、定向與 Model Editor

官方指出設定位置有四種方式：Explicitly（`AT`）、Relatively（`BY`）、Using Ship References、Using the Model Editor。

> 〔公開版未收錄：AVEVA 官方產品截圖〕兩個基本體以 P-point 連接：選取圓柱 P-point，確認對話框後圓柱移動並對齊方盒

*圖 39-4　用 P-point 定位。Connect > Primitive > ID Point 讓兩個 P-point 重合並面對面，系統會問 Return to Original Position?，按 No 才保留新位置。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 路徑 | 說明 |
|---|---|---|
| Positioning Control | 事件驅動圖形時自動出現 | Pick Type 限制可拾取對象（Any、Element、Aid、Pline、Ppoint、Screen、Graphics）；Pick Method 決定位置推導（Snap、Distance、Mid-Point、Fraction、Proportion、Intersect、Cursor）；Working Plane 可把點投影到工作平面 |
| Position At | Position > Explicitly (AT) | 輸入座標，`WRT` 指定參考元素；Datum 可指定原點或某個 ID Design 點；Explicit Position 可跳過拾取，右鍵 Format > Format XYZ |
| Ship Reference | Position > Using Ships References | 追蹤式表單，顯示船舶參考系與 XYZ |
| Relatively (BY) | Position > Relatively (BY) | 相對目前原點移動指定量 |
| Equipment Point | Position > Equipment Point > At Explicit／At General／Through／Clearance／Towards | 移動設備，使其某個 P-point 到達目標；Clearance 以 Infront／Behind、Onto／Under、From／To 指定淨距 |
| Orientate | Orientate > Axes／Rotate／Primitive > Point | 分三類是為了避免把設備與基本體混淆 |
| Connect | Connect > Primitive > ID Point／Explicit | 讓一個基本體的 P-point 與另一個重合；**不建立連接交叉參照**，只是移動對齊 |


### 39.5.1 Model Editor

Model Editor 可用滑鼠動態拖曳選取的元素，由 Model Editor 工具列圖示或 Edit > Model Editor 進入／離開。選取後出現操控手把（Locator Handle）：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Model Editor 手把：線性移動、平面移動與旋轉三種控制

*圖 39-5　Model Editor 手把。U、V、W 三軸各有線性手把，兩軸之間是平面手把，弧線是旋轉手把。（AVEVA 官方文件截圖，僅供內部教學）*

| 操作 | 右鍵選單 |
|---|---|
| 線性手把 | Enter Value、Align with Feature、Snap to Point、Move Handle、Cancel |
| 旋轉手把 | Enter Value、Orient to Point、Align with Direction、Align With、Rotate Handle（含 To World）、Cancel |
| 鎖定 | Modify > Lock：Lock CE、Lock CE and below、Unlock CE、Unlock CE and below；被鎖定的元素無法修改或刪除 |

編輯設備內部基本體時，右鍵點設備選 Edit Equipment；若用子設備組成則再選 Edit SubEquipment；離開用 Exit Equipment Editor。進入後其他元素會變半透明。官方註明：圖形化設備編輯**不需要**在 Equipment 應用程式內。

## 39.6 修改、複製與刪除

| 工作 | 路徑 | 注意 |
|---|---|---|
| 改屬性 | Modify > Attributes | 先選屬性、輸入新值、OK，最後要 Apply 才寫回資料庫；圓柱用 `Height`、`Diameter`，方盒用 `Xlength`、`Ylength`、`Zlength` |
| 改設備規格 | Modify > Equipment Specification | Specification 下拉有 AVEVA Standard Equipment、AVEVA Advanced Equipment、Marine Standard Equipment、Reload；可開 Properties 與 Plotfile |
| 改參數 | Modify Properties 表單 | Reset 回原值、Default 回預設值 |
| 改管嘴規格 | Modify > Nozzle Specification | 可改 Specification、Generic Type、Nominal Bore；改管嘴高度要用 Modify > Attributes |
| 拉伸／修剪基本體 | Modify > Stretch/Trim > To P-Point | 端點 P-point 移到另一個 P-point；不適用於管嘴與圓環（torus） |
| 複製 | Create > Copy > Offset／Rotate／Mirror | 輸入份數與偏移；Object to copy 可選 CE、List、Pick；copy to 可選 CE 或 Rel.（同階層相對位置）；複製後用 Modify > Name 改名並同步改管嘴名 |
| 刪除設備／基本體 | 右鍵 Delete、預設工具列 Delete CE，或 Delete > CE | 出現 Confirm；未儲存前可用 Model Editor 工具列的 Undo 還原 |


## 39.7 參數化設計樣板設備

官方的建模選項分兩條：

1. **最簡單：** 在 Design 建 `EQUI`，底下放一批基本體與管嘴，不使用 Design Template。適合不會重複使用的獨特設備。
2. **需要樣板：** 若設備含有管路與 HVAC 連接、支撐鋼構，並希望由設備規格（Equipment Specification）選取，就必須建立 Equipment Template。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Modify Properties 表單：參數化尺寸、參數化元件與參數化子組件三類參數

*圖 39-6　參數化設計樣板設備的 Modify Properties。粉紅框是參數化尺寸（長度、支撐高度、管嘴偏移），橙色框是參數化元件（進出口管嘴尺寸），藍色框是參數化子組件（支座、端蓋型式）。（AVEVA 官方文件截圖，僅供內部教學）*

參數表達式支援條件式：

```text
IF(<Boolean Expression>, <True Expression>, <False Expression>)

IF(LDPR LENG OF TMPL lt 2400, (ID/BS-SPEC/45x45x4.0),
   (ID/BS-SPEC/50x50x5.0) )
```

第二式（官方範例）是「依樣板的 `LENG` 屬性決定型鋼規格參照」。`True`／`False` 兩個表達式必須回傳相同資料型別；因為 `IF` 是 PDMS 表達式函式，可以巢狀使用。這是本章**少數有官方依據的設備端語法**。

## 39.8 設備空間關聯（Equipment Spatial Associations）

Equipment Associations 讓使用者對設備與周圍環境加上**幾何約束**，供後續設計檢查：每一條關聯是一條系統可檢查的設計規則，滿足回報成功，否則回報失敗。這與[第 25 章](ch25_space_fem_zh-TW.reading.html)的 Space Management 相鄰但不同：Space 管的是區域與體積，關聯管的是兩個設備特徵之間的幾何關係。

### 39.8.1 管理者設定

| 項目 | 內容 |
|---|---|
| 載入定義 | 標準定義在 Master 專案的 Association World `/AVEVA-Std-Association-Definitions`：`/AV-STDMATE`、`/AV-STDALIGN`、`/AV-STDPARALLEL`、`/AV-STDPARALLELOFFSET`、`/AV-STDDISTANCE`、`/AV-STDHORIZDIST`、`/AV-STDABOVELINE`、`/AV-STDELEVATION`；一般使用者只需唯讀，建議放在共用 Master 專案 |
| 儲存結構 | `ASSOWL`（Association World）→ `ASSOGP`（Association Group）→ `ASSOC`（Association） |
| 加入特徵 | P-point、Design Point、P-line 可當參考；建議在樣板的設計點／型錄 P-point 的 `PURPOSE` 設成 4 字元、**後兩碼為 `FA`**，例如 `CLFA`（中心線）、`BOFA`（底面）、`TOFA`（頂面） |

### 39.8.2 建立、修改與刪除

在 Equipment 應用程式選 Utilities > Equipment Associations：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Equipment Associations 視窗：八種關聯類型單選、Select new Association partner 與已參與的關聯清單

*圖 39-7　Equipment Associations。先 Select Association Item 選主元素，從八種類型選一種，再 Select new Association partner 選對象；下方列出該元素已參與的關聯，可 Modify 或 Delete。（AVEVA 官方文件截圖，僅供內部教學）*

| 類型 | 意義 |
|---|---|
| Mate | 兩個面貼合（共面）或相隔指定距離；兩面法向平行且反向 |
| Align | 兩個面對齊（共面）或相隔指定距離；法向平行且同向 |
| Parallel | 兩個方向平行，可同向或反向 |
| Parallel Offset | 兩條線平行且相隔指定距離 |
| True Distance | 兩點重合或相隔指定距離 |
| Elevation | 兩點的高程差為指定值 |
| Horizontal Distance | 一點在另一點正上方，或水平面上相隔指定距離 |
| Point above line | 一點在某線的正上方或正下方，容許誤差內 |

選好雙方後出現參考幾何視窗：My data 與 Partner data 各選一個特徵（如 `CLFA` Reference Plane）；若元素沒有預先定義，按 Pick reference plane 再拾取 P-point 或 P-line。

> 〔公開版未收錄：AVEVA 官方產品截圖〕兩台泵的 CLFA 中心線平行約束：左側 3D 視圖標出 CLFA，右側是 Parallel 設定面板

*圖 39-8　對兩台泵的中心線（`CLFA`）建立 Parallel 約束。右側可命名關聯、設定 Separation，並檢視兩物件之間已存在的關聯與 Test 結果（Passed）。（AVEVA 官方文件截圖，僅供內部教學）*

部分類型可帶間距參數：**最小間距**、**最大間距**或**精確間距**，由 Separation 下拉清單與數值欄輸入。建立後，右鍵關聯可 Navigate To、Test this Association、Association Details。修改選取關聯後按 Modify Association；刪除按 Delete Association。

### 39.8.3 Association Manager 與報表

Association Manager（Design 模組 Utilities > Associations）檢視專案內所有關聯，分三個面板：關聯清單（名稱、描述、`PURP`、Status 即 Passed／Failed、兩個元素名稱）、組成關聯的限制（Restriction）與狀態、被選限制的細節。官方範例：限制失敗是因為距離限定值 2000，實際距離 913。多數關聯只含一個限制，少數含多個，任一失敗就導致整條失敗。右鍵可 View Association Items（只顯示相關元素）、導覽、刪除、存成 Excel。

**元素被刪除時：** 該關聯的 `TESTEV` 測試回傳 FALSE；可檢查成員的 `AMEMRF` 屬性是否為無效參照，找出被刪的元素。

### 39.8.4 二次開發依據

這是 Equipment 章節裡**屬性層級依據最完整**的地方。官方列出報表與客製化常用的屬性（以下皆出自官方表格）：

| 元素 | 屬性 | 型別／用途 |
|---|---|---|
| `ASSOC` | `NAME`、`TESTEV`（Logical：測試是否滿足）、`ADEFRF`（定義參照）、`DESP`／`WDESP`（設計參數陣列） | 關聯本體 |
| `RESTRI` | `TESTEV`、`ASSDFS` | 限制 |
| `ASSMBR` | `AMEMRF`（參照的設計物件）、`POSEV`（特徵位置）、`DIREV`（特徵方向） | 關聯成員 |

用一般報表（Reporting）輸出關聯：Type 設 `ASSOC`，With condition 設 `PURP OF AMEMRF EQ 'ASEQ'`，欄位可選 `Name`、`Description`、`TESTEV`、以及 `fullname of amemrf of assmbr 1`／`2`（兩個成員名稱）。官方說可寫 PML 工具做客製報表，並可用 .NET API 客製化 Associations（見 *.Net customization User Guide* 與 *Data Model Reference Manual*，本章未讀，API 簽章〔待核對〕）。


## 39.9 Equipment Report

Utilities > Equipment Report 開啟報表表單，三階段：在 Columns 頁籤選屬性、到 Output 頁籤檢視與排序、存成 Excel。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Equipment Report 視窗：Columns 頁籤左側是可用屬性，右側是選定屬性，中間為移動箭頭

*圖 39-9　Equipment Report 的 Columns 頁籤。左邊列出目前元素的所有屬性（含 Attribute、Description、Data Type、Report Header），右邊是要輸出的欄位。（AVEVA 官方文件截圖，僅供內部教學）*

| 操作 | 方式 |
|---|---|
| 選欄位 | 點選（Shift 連續、Ctrl 非連續）後按 `>`；`>>` 全選 |
| 移除 | `<` 移除選取，`<<` 全移除 |
| 調順序 | 上下箭頭 |
| Pseudo Attributes | 勾選後顯示偽屬性名而非系統名 |
| 分組 | 把欄標題拖到上方標頭區，出現 `+` 展開 |
| 篩選 | 欄標題左側圖示開篩選清單 |
| 儲存 | SAVE 產生 Equipment Report Filename，存檔並開啟 Excel；可再存成 CSV 或 Tab 分隔 |

**限制：** 官方註明目前會報告**目前 MDB 內所有設備**，沒有選取選項；官方練習會跑 `Equipment_Report.tmp` 與 `nozz_sched.tmp`（檔案位置〔待核對〕）。

# 第二部分　HVAC Designer（通風設計）

## 39.10 HVAC 設計全貌與資料階層

HVAC Designer 是 AVEVA Marine 內的模組，讓你在完整 3D 環境設計與詳細化複雜風管網路，並提供無碰撞設計的輔助工具。官方強調它採用「標準預設值先快速建出概念佈置、細節留到核准之後」的工作方式。

> 〔公開版未收錄：AVEVA 官方產品截圖〕HVAC 階層：WORLD、SITE、ZONE 為所有專業共用，其下 HVAC 擁有 BRAN 與 HLIST；BRAN 擁有 HVAC 元件，HLIST 擁有 HVAC Spool

*圖 39-10　HVAC 資料階層。`WORLD`、`SITE`、`ZONE` 共用，其下為 HVAC 專屬元素。（AVEVA 官方文件截圖，僅供內部教學）*

| 層級 | 元素 | 官方描述 |
|---|---|---|
| 系統 | `HVAC` | Design 資料庫的頂層元素，底下建 `BRAN` 與 Spools |
| 分支 | `BRAN` | 在 Branch Head 與 Branch Tail 之間的風管元件序列 |
| 元件 | 風管、彎頭、風門、風機… | 單一風管件，組成設計 |
| 預製清單 | `HSLIST`（官方圖寫 HLIST）〔待核對〕 | 一組 HVAC Spool 的集合 |
| 預製段 | `HSPOOL` | 一段結合在一起、便於預製的元件序列 |

與管路（[第 21 章](ch21_pipework_zh-TW.reading.html)）的對照：同樣是「分支擁有有序元件」，但風管元件的連接點叫 P-arrive／P-leave（`PA`／`PL`），側向連接用 P3；分支之間還有 `BRCO`（Branch Connector）。第 7 章引用的 Data Model Reference 說明 `BRAN` 的合法擁有者包括 `PIPE` 與 `HVAC`，兩者共用 `BRAN` 型別。

### 39.10.1 進入與工作區

選 Design > HVAC Designer。所有建立與修改都從中央的 **HVAC Window**（Create > HVAC）發動，它像一個任務中樞：

| 區域 | 功能 |
|---|---|
| Categories 下拉 | 標準風管類別：HVAC/Branches、Rectangular、Circular、Flat Oval、Transformations、Branch Connectors、Inline Plant Equipment、Extra Inline Equipment、Equipment Nozzles，以及 User Defined Fittings 與 Assemblies |
| Available Types 下拉 | 依類別列出具體類型，選後彈出該元件的建立／修改視窗 |
| 下半部 | Orientation、Position、Connect 三組修改工具（每組獨立作用） |
| Copy ID | 在 3D 視圖點選現有元件，以其屬性為基礎建立新元件 |
| Modify CE | 修改目前元素；也可由 Modify > HVAC 進入 |
| Transpose Head Tubing | Branch Head 與第一個元件之間的隱含風管若轉了 90 度，用它轉正 |

某些類型必須在正確的階層位置才能建立；位置不對時會出現錯誤訊息，例如「必須在 HVAC Branch 或 HVAC Component 之下」。HVAC Window 可用 Full 或 Brief 版面（HVAC Defaults 視窗的 Style 選單），Full 多了 Plane Positioning（以平面方向加 P-arrive 點定義構造平面）。


## 39.11 管理者設定：型錄、規格與預設值

HVAC Administrator 指南面向「建立使用者自訂風管配件、設定預設值、製作 HVAC Sketch 圖面樣板與表格」的管理者。官方假設管理者熟悉 Catalogue and Specifications、會寫與編輯巨集（macro）、具備基本 PML 與 HVAC Designer 知識。與[第 8 章](ch08_catalogue_spec_zh-TW.reading.html)的目錄與等級概念直接相關，但 HVAC 另有幾個**不在規格資料庫、而在系統檔案**的設定：

| 項目 | 位置與做法 |
|---|---|
| 應用檔案 | 一般在 `%pdmsui%/des/hvacadv`；控制檔 `xmaincontrol` 可用文字編輯器修改預設值 |
| Detail Specification | 定義不同 Joint、標準長度、板厚或加勁的規則表；**存於系統檔案**而非規格資料庫，預設目錄 `%pdmsdflts%/hvacadvspecs`（可在 `xmaincontrol` 改）；可選清單在 `aaaspeclist`（官方列 `DW142TABLE6`、`DW142TABLE7`、`MODELONLY`、`TUTORIAL`）；管理者需讀寫權，使用者永遠唯讀 |
| Insulation Specification | 在 Branch 層以 `ISPEC` 屬性設定；系統只內建 `/CADCHVACISPEC`，要自訂就在 CATA 資料庫複製再改名 |
| Defaults | 標準預設值存於 `/CADCHVACDFLTS`；自訂時 `new cata /USERHVACDFLTS copy /CADCHVACDFLTS rename ...`，再改資料值；用戶透過 Settings > Ductwork Defaults 選擇 |
| Units | 以全域變數 `!!CDHVACUNITS` 設為 `'MM'` 或 `'INCH'`；預設值單位必須與之一致，否則 500 可能被當成 500 英寸；系統附 `CADMETRIC.DEF` 與 `CADCIMPERIAL.DEF` |
| Spool／Sketch | 見 39.15 |

### 39.11.1 樣本型錄與規格

官方提供的樣本型錄放在 Master 專案資料庫 `/MASTER-HVACCATA`：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Catalogue Explorer：MASTER/HVACCATA 下有 CATA CADCHVACCATA、CATA CADCHVACDFLTS、SPWL CADCHVACSPECS 等，SPEC 下的 SELE 層層展開到 SPCO

*圖 39-11　HVAC 樣本型錄與規格的 Catalogue Explorer。`SPWL` 下的 `SPEC` 以 `SELE` 逐層分類，最後到 `SPCO`（Spec Component），如 `RMELBOW`、`CELBOW`、`FELBOW`。（AVEVA 官方文件截圖，僅供內部教學）*

| 元素 | 名稱範例 | 說明 |
|---|---|---|
| `CATA` | `/CADCHVACCATA` | HVAC Designer 標準型錄 |
| `SECT`／`CATE`／`PTSE`／`GMSE`／`SCOM` | `/RMELBOW-SECT`、`/RMELBOW` | 矩形斜接彎頭：點集、幾何集、元件 |
| `DTSE`／`DATA` | `/RMELBOW-DETAIL-DATA` | 資料集與各屬性（Property）資料 |
| `SDTE` | `/RMELBOW-DETAIL` | Detail Text |
| `SPWL`／`SPEC`／`SELE`／`SPCO` | `/CADCHVACSPECS`、`/CADCHVACSPEC` | 規格；`SELE` 依 `TYPE`、`STYPE` 選擇 |

每個型錄項目由兩組資料定義：**Geometry Set**（以 3D 基本體組成外形，可含負基本體當孔洞）與 **Point Set**（疊在幾何上的參考點與方向，即 P-point）。相似外形的元件共用同一組幾何與點集；尺寸不寫死在型錄，而以**設計參數（Design Parameters，`DESP`）**表達，使用時才指定或由相鄰元件推導。

### 39.11.2 Joint 與 Stiffener：12.0 之後可自訂

12.0 版前接頭是固定集合（如 `FJ25`、`FJ30`、`RE`，寫死在巨集 `hvcjoints.pmlobj`）；現在 Joint 與 Stiffener 改成型錄資料，管理者可新增、移除。

| 項目 | 儲存位置 | 每個資料集的資料元素 |
|---|---|---|
| Joint（矩形／圓形／扁圓） | 六個 `SECT`：`/CADCHVACCATA-Joints-RECT`、`-CIRC`、`-FOVA`，及各自的 `-Imp`（英制）版本 | `DESC`、`CODE`、`ALPH`、`NUME`、`HVJA`、`HVJB`、`HVJC`（A、B、C 尺寸） |
| Stiffener | `SECT` `/CADCHVACCATA-Stiffeners` | `DESC`、`CODE`、`HVSA`、`HVSB`、`HVSC`、`CONFIG`（`EXTERNAL`／內外配置）、`SHAPE`（如 `L`） |

標準 Joint 碼分兩群：任何形狀適用的有 `MALE`／`FEMA`（承插公母）、`FJ25`…`FJ100`（角鋼法蘭）、`FB…`（扁鋼）、`CH…`（槽鋼）、`RE`（Raw edge）、`SF25`／`SF40`／`SF50`（Self flange）、`WELD`；只適用矩形的有 `RE25`／`RE40`／`RE50`、`DM30`／`DM40`（Ductmate）、`IDC`、`IDF`、`VM20`／`VM30`／`VM40`（Verromez）、`FLAT`。Stiffener 碼有角鋼、扁鋼與槽鋼三類，碼可以是任何文字。


Joint 儲存位置由 PML 物件 `HVACJOINTS` 的 `.hvcJoints()` 方法唯一控制：依 `!!cdHVACunits` 為 `'MM'` 與否，把 `rectangularJointsStorage`、`circularJointsStorage`、`flatOvalJointsStorage` 指向公制或 `-Imp`（英制）的 `SECT`（以 `object DBREF(...)` 設定）。


### 39.11.3 使用者自訂風管配件（User Defined Fittings）

標準元件不夠用時，HVAC 表單有 User Defined Fittings 類別，但**必須由管理者先建立自訂型錄與規格**。官方的教學式練習以六個標準型錄沒有的三通（Y 型與 Angled 型各三種）為例，流程如下：

1. **前置：** 在 Admin 設 `EDIT MODULE DESI MODE CATA RW`，讓 Design 可讀寫型錄；另建獨立型錄資料庫，不要寫進 AVEVA 原廠資料庫。
2. **頂層元素：** `NEW CATA`、`SECT`、`CATE`、`SPWL`（`PURP HVAC`）、`SPEC`（`PURP FITT`）；**這兩個 PURP 決定新規格會不會出現在 User Defined Fittings 表單**。
3. **複製相似元件：** 用巨集複製 `/RSTHRE`（矩形方形三通）再改名，連同 `DTSE` 資料集；再以巨集建 `SELEC`、`SPCOMPONENT`，設 `TANS`（顯示於表單的文字，太長會塞不進）、`Catref`、`Detref`。
4. **草圖與慣例：** 手繪並標示設計參數；P0 通常在 P1 與 P2 交點，P1 arrive、P2 leave、P3 第三接點；Z 與 PArrive 反向。
5. **屬性：** 用 `LHIDE true` 隱藏用不到的 `DATA`，只留 `AARR`（`DESP[2]`）、`BARR`、`ALEA`、`ABRA`（`DESP[41]`）、`ATHR`、`LTHR`、`BRLE`、`AOFF` 等；`TYPE`（`DESP[66]`）、`STYP`（`[67]`）、`SHAP`（`[40]`）、`FACE`（`[30]`）為隱藏屬性；初始 Joint 建議 `RE`；建立 `LSTU` 指定 Leave Tubing（直管用 `RTUBEB`，彎頭、三通等用 `RTUBEA`）；Sketch 必要的 `RTEX`、`DUCT`、`DETA`、`JOIN`、`FIXI` 五個文字屬性。
6. **點集與幾何集：** P1、P2、P3 保留給 arrive、leave、branch；**每個元件都要有 P6**（在 PL、垂直於 PL）；`P61`、`P62` 系列為出圖關鍵尺寸點；表現層級：一般 0–10、負體 9–10、法蘭 6–10、保溫 7–10。
7. **PLOT 與測試：** 以 Draft 做平面、立面加等角圖，檔名與 `CATREF` 同名；在層級 6、4、9、7 搭配 holes 與 insulation 開關檢視，並測 Autofill、Spooling 與 Sketch。


**常見錯誤：** `SPWL` 與 `SPEC` 的 `PURP` 沒設成 `HVAC`／`FITT`，表單看不到新規格；`TANS` 太長；忘了 `P6`；三通新增後還沒設設計參數就拿來用，幾何顯示不正確；預設值單位與 `!!CDHVACUNITS` 不一致。

## 39.12 設計流程：System、Branch 與元件

**流程總覽：**

```text
建 HVAC System ─► 建 Main Branch ─► 依序建元件(含 Joint、Connect) ─► Side Branch
        │                                                        │
        ▼                                                        ▼
   Autofill 隱含風管 ─► Itemizing/重量/檢查 ─► Split ─► Spool ─► Sketch
```

### 39.12.1 建立 System 與 Branch

| 步驟 | 動作 | 要點 |
|---|---|---|
| 1 | HVAC Window > HVAC/Branches > HVAC System Element | HVAC Name 與 Primary System（預設 No System，另列 Purpose 為 HVAC 的系統）；表單是 Create／Modify 雙用，左上角下拉切換 |
| 2 | HVAC/Branches > Main Branch Element | Main Branch 是起點（branch head），必須建在既有 HVAC System 之下 |
| 3 | 逐一建元件 | Categories 選 Rectangular／Circular／Flat Oval 等，再選 Available Type |
| 4 | 側向支管 | 先在 Main 加三通類元件，再建 Side Branch，它會自動配合所選三通設定 Head 方向、寬、深、形狀與起點 |


Branch 層另有**Detailing Specification**：元件的構造細節由目前的 detailing spec 決定，只能在 Branch 層切換；同一條風管中要換 spec，就要在換 spec 處另建一個新 Branch。切換下拉位於主選單列。

### 39.12.2 元件視窗共通結構

所有元件視窗版面一致：尺寸欄預填型錄預設值（Picture 看示意圖、Transpose width/depth 交換寬深）；Arrjoint／Leajoint 以 Choose 選接頭（Prev 取前件的 Leajoint）；Leave Direction 用 X、Y、Z、-X、-Y、-Z；**Connect**（建立時預設）接到前一件，**Unchanged**（修改時預設）不連接而放在座標 0.00 浮動；Defaults 回到初始尺寸；Fit 使前一件 P-leave 對齊下一件 P-arrive。


### 39.12.3 Choose Joint

> 〔公開版未收錄：AVEVA 官方產品截圖〕Choose Joint 視窗：Shape 選 Rectangular，Joint 選 Arrive／Leave／3rd Joint，清單列出 MALE、FEMA、FJ25 等

*圖 39-12　Choose Joint。Shape 預設是目前元件的形狀，也可換成 Circular 或 Flat Oval，清單隨之改變；清單首列 Specification Automatic Selection (Spec) 表示交由規格自動選。（AVEVA 官方文件截圖，僅供內部教學）*

三個單選鈕決定要設哪一端：Arrive、Leave，以及 **3rd Joint**（三通等有第三接點者）。選好後，被選的接頭填回元件視窗對應欄位（如選 Arrive 則填入 Arrjoint）。

### 39.12.4 位置、方向與連接修改

HVAC Window 下半部三組工具各自獨立：

| 工具 | 可做的事 |
|---|---|
| Orientation | 設 Leave Direction（X、Y、Z、-X、-Y、-Z）與 Leave 'A' Axis（繞 Leave Direction 的旋轉） |
| Position | At（Cursor、ID P-Point、ID Element、Next、Previous）；Through（沿 arrive-leave 軸移動，可用 Cursor、ID P-Point、ID Element、Next）；Move by（相對移動）；Distance（沿 P-leave 軸遠離前一件保留指定距離） |
| Connect | To Previous（不是軸對稱的件，如直管、變徑）；Leave East／West／North／South／Up／Down（二通且會轉向，如彎頭）；P3 is East／…（側向連接或不對稱件，如三通、偏心變徑）；to Next；to Branch Tail。Branch 的 Head 或 Tail 可接到其他 Branch 或元件：Tail／Head of ID Branch、ID Branch Connector、ID Threeway Piece、ID Centrifugal Fan、ID Air Handling Unit、ID Equipment Nozzle、First Member |

離心風機的 P-arrive 與 P-leave 都在矩形法蘭面，P3 在圓形法蘭面；空調箱的 P3 是輔助法蘭（例如回風入口）。

## 39.13 元件類別與設計參數

HVAC Window 選類別時若在 HVAC Defaults 勾 Show Pixmaps，會顯示該類別的圖形選單（Palette）：

> 〔公開版未收錄：AVEVA 官方產品截圖〕HVAC Rectangular Ductwork 圖形選單：直管、變徑、彎頭、三通、風門、導流葉片等縮圖

*圖 39-13　矩形風管圖形選單。點縮圖即開啟對應的建立／修改視窗；不是每個類別都有圖形選單。（AVEVA 官方文件截圖，僅供內部教學）*

Menu Map 的類別與代表類型：

- **Rectangular：** Straight、Taper、各式 Bend／Elbow／Offset、四種 Threeway、Cap End、Mesh End、Weather Skirt；Two Bend Setfill（自動填充）；子元件 Stiffening、Access Panel、Test Point、Splitter、Deflectrol、Internal Damper、Gasket、Turning Vanes。
- **Circular：** 直管、Male Coupling、Taper、3／4／5 Segment Bend、Breeches、Side Branch Tee、Flexible Tube／Bend、Roof Cowl；Setfill／Flexfill；子元件另有 Saddle。
- **Branch Connectors：** 矩形、圓形、扁圓三組，各有 Boot、Square、Fish、Angled 等；矩形 branch connector 可接任何形狀的風管。
- **Inline Plant Equipment：** 防火閘門（Fire Damper）、Control／Motorised Damper、Heater／Cooler Battery、Silencer、Grille、Air Handling Unit、Centrifugal／Axial Flow Fan 等。
- **Equipment Nozzles：** Rectangular／Circular／Flat Oval Nozzle 與 Modify Existing Nozzle。

幾個有條件限制的類型（來自 Menu Map 與各頁說明）：Grille off Brco 只能在 branch connector 之下建立；Air Handling Unit 只能是 HVAC branch 的**第一個**元件；Rectangular／Circular Nozzle 必須由設備（`EQUI`）啟動，所以**必須先建好設備才能建 HVAC Equipment Nozzle**，這就是 Equipment 與 HVAC 的銜接點。


## 39.14 輔助工具

### 39.14.1 分支與組件

**Divide Main（Utilities > Divide HVAC Main into Multiple Branches）：** 把一條主風管切成多條較小支管，從主風管最後一件的 leave 方向出發，例如末端大風管往天花板多個送風口分流。系統在主支管加入 `BRCO` 元素並建立次級 `BRAN`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Divide HVAC Main into Multiple Branches 視窗：CE、Main Duct 尺寸、Number of Branches、Divisions X1–X5 與 Y1–Y5、Summary、Preview 與 Apply

*圖 39-14　Divide HVAC Main into Multiple Branches。上方顯示 Main Duct 的尺寸與方向，Number of Branches 設 X、Y 方向數量，Auto-Fill 自動等分，也可在 Divisions 手動輸入；Preview 預覽後再 Apply。（AVEVA 官方文件截圖，僅供內部教學）*

流程：按 CE 指定主支管 → 選 X、Y 方向支管數 → Auto-fill 自動等分（或勾 Create Single Branch Only 後輸入偏移）→ Summary 看每條支管尺寸位置 → Preview／Clear Preview → Apply。

**Assemblies（Utilities > HVAC Assemblies）：** 組件是預先定義、可多次複製的元件組合，存放在獨立的 Application Data World 階層（Assembly World → Area → Assembly，其下有存放 Assembly Rules 的 Design Data Set）。3D 視圖按住 Ctrl 選元素後 Copy Design；**組件建好後不能再追加內容**。使用時於 HVAC Window 的 Assemblies 類別選取，可 Create connected to element 或 Create at tube position。


### 39.14.2 Autofill、Itemising 與計算

**Autofill With Straights：** 使用者建 Branch 時常只指定有功能的元件（彎頭、側接、消音器、風門），元件之間的空隙以**隱含風管（implied ducting）**自動補在 3D 圖上。要能預製並產出完整材料表，必須把空隙換成實際的標準與非標準直管。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Highlight Implied Ductwork 視窗：列出各段需要的標準與非標準直管長度，例如 1 Straight of 2085 required only (Standard = 3000)

*圖 39-15　Show Gaps 的結果。每個空隙列出位置、長度與「標準直管幾支＋剩餘非標準長度」的組合，對應的隱含風管在 3D 視圖以紅色高亮。（AVEVA 官方文件截圖，僅供內部教學）*

- **Show Gaps**（Utilities > Autofill with Straights > Show Gaps）：選 Branch 則顯示整條所有空隙；選單一元件則只顯示它到下一件之間的空隙。
- **Fill Gaps**：用實際直管取代隱含風管，並在階層中顯示。

| 工具 | 路徑 | 功能 |
|---|---|---|
| Automatic Itemising | Utilities > Automatic Itemising | 對所有風管件與廠房設備依序編項目號；Naming Prefix 格式 `PREFIXnumber`（如 `/HITEM1`）；額外與 inline 設備已有前綴者不變；works fitted 的件用小數編號（如 3.1 是裝在 3 號件上的 branch connector）；**works fitted 由 `WKSF` 屬性為 true 定義** |
| Surface Area & Weight | Utilities > Surface Area & Weight | 面積與重量在建立或修改時依型錄資料計算；本工具顯示 Branch、單件或設備的表面積與重量 |
| Centre of Gravity | Utilities > Centre of Gravity | 計算一組元素的合併重心與總重；需先建 Group World → Group → 在 CE 右鍵 Add Current Elements 加成員；計算對象是 `GPSET` |
| Data Consistency | Utilities > Data Consistency | 對選定元素執行客製檢查；HVAC Consistency Check Options 可調參數，Tube Range 調管徑公差；輸出可選 Screen 或 File（New file、Overwrite、Append） |
| Query | Query > Item Details／Position／Orientation／Gap to next | Item Details 有 Brief Description、Item Number、Detailing Spec、Insulation Depth、Taper Side Angles；Position 可查 Origin（P0）、PA、PL、P3、PH（Branch Head）、PT（Branch Tail）；Gap to next 查 CE 與下一件的距離 |

**常見錯誤：** 沒做 Fill Gaps 就想要完整材料表（隱含風管不在材料表裡）；把「Show Gaps」當成修正動作（它只高亮與計算）；`WKSF` 沒設好，導致 Itemising 的小數編號與 Spool 切分不如預期。

## 39.15 Split、Spool 與 Sketch

### 39.15.1 Split HVAC

當風管路徑已穩定，Modify > Split HVAC 可在地形特徵的邏輯斷點或指定位置切開 HVAC 系統（例如在艙壁或防火分區處）。

| 區塊 | 說明 |
|---|---|
| Branches to Split | 以 CE、List、Graphical Pick、Window Selection 加入要切的 Branch |
| Split Marker | 選 Marker 或 Assembly；Marker 用 Create Marker 在定義平面上建立 |
| Plane Definition | 用 Plane Size 與方法：DB Planner Element、Element、Ppoints、Pline、Reference Grid、Explicitly |
| Reposition Marker | Explicitly At、Relatively By，或 Using Ship Reference（參照船舶格線與 XYZ） |
| Split Assembly | 若以組件當分割標記，Apply 後組件插在切面交會處 |
| 存放位置 | 切完的元素可放在 Current HVAC、New HVAC 或 Existing HVAC；可 Flip Head Tube |
| Merge Branches | Modify > Merge Branches：先點要合併的相連 Branch，再點合併目標，確認 |

### 39.15.2 HVAC Spool

HVAC Spool 在 Design 產生，是「一組在工場先接好、再到現場組裝的連接 HVAC 元件」。資料庫階層為 `HVAC → BRAN → 元件`，並有 `HSLIST → HSPOOL`。

操作：Utilities > HVAC Spooling 開 HVAC Spool Manager；Set HVAC 設定目前系統；命名方式二選一：**Auto Name**（系統自動命名規則，預設）或 **User Defined Name**（自訂 Spool List Name 與 Spool Prefix）；Generate Spools 產生。預設勾選 `Rename spools generated by 'Remove Spool Elements'` 與 Use First available data：若 10 個 Spool 的第 6 個被修改而產生新 Spool，勾選後的顯示順序是 `1,2,3,4,5,11,6,7,8,9,10`；沒勾則新 Spool 是 `unnamed`。

| 功能 | 說明 |
|---|---|
| Delete Spools／Regenerate | 刪除全部／重新產生 |
| Verify HVAC／Verify HVAC Spools | 驗證全部或選定的 Spool；結果欄為 Successful 或 Failed，並列失敗細節 |
| Add Spool Elements | 在 3D 視圖拾取元件加入選定 Spool，按 Esc 結束；只有**相鄰元件**可選 |
| Add Spool Elements (by picking last only) | 只點最後一件，加入一個範圍 |
| Combine Spools | 把兩個選定 Spool 合成一個 |
| Remove Spool Elements | 從選定 Spool 移除元件 |

修改後必須重新產生並驗證。Spool 條件由系統管理員設定。

官方列出一個核心 PML 物件可查詢 Spool：

```text
!x = object HVACSPOOLMANAGER()
```

| 方法 | 回傳 | 說明 |
|---|---|---|
| `GENERATEHVACSPOOLS(DBREF)` | — | 傳入任何 HVAC 元素，產生 `HSLIST` 與 `HSPOOL`；若該元素已有 `HSLIST`，會驗證現狀，OK 就不動，有差異才重新產生相關 Spool，並保留有效 Spool 的參照編號，使既有圖面不受影響 |
| `DELETEHVACSPOOLS(DBREF)` | — | 刪除該 HVAC 擁有的 `HSLIST` 與 `HSPOOL`；**不能用 `Delete HSPOOL` 刪除** |
| `VERIFYHVACSPOOLS(DBREF)` | 字串陣列 | 不符合有效 Spool 條件時回傳錯誤訊息，格式 `<ELEMENT NAME> : <ERROR MESSAGE>`；全部符合則回傳 unset 陣列 |
| `VERIFYSPOOL(DBREF)` | 字串 | 輸入一個 `HSPOOL`；失敗回傳錯誤訊息，成功回傳 `"Successful"` |

> **專業提醒：** `GENERATEHVACSPOOLS` 保留既有 Spool 編號是為了讓已出的圖不被破壞。對二次開發者的意思是：**要重算 Spool 就呼叫它，不要先刪除再重建**，否則已出的 HVAC Sketch 會失去對應。

### 39.15.3 HVAC Sketch（Draft 出圖）

HVAC Sketch 是用 Design 的 Spool 資料，在 Draft 模組的 Automatic Drawing Production 自動產生有尺寸、有比例的 Spool 圖，圖上含 Spool 與組裝資料（依 `WKSF` 決定）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Draft 的 Automatic Drawing Production：左側 Draft Explorer，中間為 HVAC Sketch 圖面，右側是 HVAC Sketches 搜尋與建立視窗

*圖 39-16　HVAC Sketch。右側 HVAC Sketches 視窗以 Production Status 與 Sketch Status 篩選 Spool 並 Create Sketches；中間圖面含多視角與 MTO、Assembly、End Points 表格。（AVEVA 官方文件截圖，僅供內部教學）*

使用者流程：Design > Modules > Draft > Macro Files 啟動 Draft，Draft > Auto Drawing Production，Create > HVAC Sketches；用 CE 指定要搜尋的 `HVAC`，可依 Spool 名稱、Production Status（Any、Valid、Not Valid）與 Sketch Status（Any、Created、Not Created）搜尋；結果表有 Name、Valid、Sketch、Drawn 欄；右鍵可 Select All、Clear Selection、Print Sketch、Delete Sketch。建立前需指定 Sketch Template（既有 `DRWG` 或 `DRTMPL`）、儲存的 Registry（`REGI`）與 Log File。

**管理者要準備的圖面元件：**

| 元件 | 說明 |
|---|---|
| Backing Sheet | 圖框、標題欄與表格位置；標題欄用智慧文字（如 `#DATE<FR DRWG>`）；表格以 `NOTE` 識別，`function` 為 `'MTO'`、`'ASSEMBLY'` 或 `'ENDPOINT'`，`SpPurpose` 為 `'TABLE'`（標題）與 `'CELLS'`（內容） |
| MTO 與 Assembly 表 | 儲存格資料是 `HSPOOL` 屬性（如 `DTXR`、`DTXS`，或 `PROP FIXI`、`PROP RTEX`、`PROP DUCT`、`PROP DETA`）；End Point 表由系統控制 |

**核心 PML 物件 `!!hvacSketch`（官方有依據）：**

| 成員 | 說明 |
|---|---|
| `.createIn` | 必須是既有 Registry（`REGI`）的 `DBREF` |
| `.selectedTemplate` | 必須是既有 Drawing（`DRWG`）的 `DBREF` |
| `.hvacSpool` | 必須是既有 `HSPOOL` 的 `DBREF` |
| 日誌 | `!!hvacSketchesLog('text')`、`.emptyLogData()`、`.openLog()`、`.writeLog()`、`.closeLog()` |


## 39.16 二次開發者怎麼接

以下整理本章兩模組「有官方依據」與「需要核對」的介面：

| 需求 | 官方依據 | 備註 |
|---|---|---|
| 讀設備關聯檢查結果 | `ASSOC.TESTEV`、`ASSMBR.AMEMRF`、元素的 `ASSOS`／`DASSOS` 偽屬性；一般 Reporting 的 `Type ASSOC`、`PURP OF AMEMRF EQ 'ASEQ'` | 有依據；PML 與 .NET API 簽章〔待核對〕 |
| 設備參數條件式 | `IF(<Boolean>, <True>, <False>)`，範例 `IF(LDPR LENG OF TMPL lt 2400, ...)` | 有依據；`LDPR` 等關鍵字展開〔待核對〕 |
| HVAC Spool 管理 | `HVACSPOOLMANAGER()` 與五個方法 | 有依據 |
| HVAC Sketch 批次 | `!!hvacSketch` 成員、`!!hvacSketchesLog` | 有依據，但範例有方法名不一致 |
| Joint 儲存位置 | PML 物件 `HVACJOINTS`、`.hvcJoints()`、`!!CDHVACUNITS` | 有依據 |
| 元件屬性 | `DESP[n]`、`WDESP[n]`、`DDESP[n]`（型錄內用）與 Property 碼 | 有依據（官方表格）；在 PML 取值語法〔待核對〕 |
| 型錄與規格建立巨集 | `NEW CATA`、`NEW SPCOMPONENT`、`model set des para`、`LHIDE` 等 | 有依據；應在測試專案實測 |
| 讀 HVAC 元件尺寸、`BRAN` 成員、Head／Tail | 官方僅說明 UI | 〔待核對〕 |

> **專業提醒：** 對開發者最危險的是「隱含風管」。Branch Head 與第一件之間、元件之間的空隙是系統**顯示**用的，不是資料庫元素；沒有先 Fill Gaps，程式讀到的元件清單就缺少這些直管。同理，Spool 與 Sketch 只認 Design 目前有效的 Spool，讀取前先驗證（`VERIFYHVACSPOOLS`）。

## 39.17 常見錯誤彙整

| 錯誤 | 預防 |
|---|---|
| CE 站錯層級，建立時出現階層錯誤 | 先在 Design Explorer 確認層級；Zone 之前先有 Site |
| 名稱含空白或大小寫不一致 | 團隊約定命名慣例 |
| 管嘴沒走型錄 Specification；複製設備後沒改名 | 一律用 Nozzle Type；複製後立刻 Modify > Name |
| Modify > Attributes 只按 OK 沒按 Apply | 養成按 Apply 習慣 |
| 以為 Association 會自動修正位置 | 指定負責人與檢查週期 |
| 預設值單位與 `!!CDHVACUNITS` 不符 | 改預設值時同時檢查單位 |
| 修改元件時 Connect 維持 Unchanged，元件跑到 0.00 | 官方明言它不連接 |
| 未 Fill Gaps 就出材料表；組件建好後想追加元件；刪除 Spool 重建 | 先 Fill Gaps；組件先定案；用 `GENERATEHVACSPOOLS` 重算 |

## 39.18 本章小結

- **Equipment：** 設備是基本體加管嘴的集合，核心概念是 P-point（定位與連接）、Nozzle（與管路的介面）、Design Point（與關聯的參考）。一次性設備手工建模，標準設備走參數化設計樣板，條件式表達式為 `IF(...)`。
- **HVAC：** 風管網路是 `HVAC → BRAN → 元件`，所有動作經 HVAC Window 的 Categories／Available Types 發動；元件間的空隙是隱含風管，需 Autofill 變成實體直管。

## 39.19 練習題與自我檢核

1. 畫出 `ZONE → EQUI → 基本體／NOZZ` 與 `ZONE → HVAC → BRAN → 元件／HSLIST → HSPOOL` 兩條階層，標出連接點。
2. 為什麼負基本體必須屬於實體基本體？要看到孔洞需要什麼設定？
3. Connect > Primitive > ID Point 與管路的「連接」有何不同？
4. 為什麼關聯參考點的 PURPOSE 要以 `FA` 結尾？列出八種關聯類型並各舉一個船上情境。
5. HVAC Window 的 Connect 與 Unchanged 有何差別？
6. 比較 Detail Specification 與 Insulation Specification 的存放位置，備份策略有何不同？
7. 自訂三通要出現在 User Defined Fittings 表單，`SPWL`、`SPEC` 的 `PURP` 要設什麼？

## 39.20 〔待核對〕項目彙整

- 程式化讀取 HVAC 元件尺寸、`BRAN` 成員、設備 P-point 與管嘴位置的 PML 語法；`HSLIST` 與官方圖 `HLIST` 寫法差異。
- `SUBE`（子設備）元素型別名稱（官方只稱 Sub-Equipment，第 7 章亦標〔待核對〕）。
- Equipment Association 的 PML／.NET API 簽章（官方僅指向 *.Net customization User Guide*、*Data Model Reference Manual*，本章未讀）。
- `IF` 表達式內 `LDPR`、`TMPL` 等關鍵字的完整語法。
- HVAC Menu Map 部分 Available Type 與視窗標題疑似錯置，以實際介面為準；`!!hvacSketch` 範例中方法名不一致（`openLog`／`openLogFile`、`!!processhvacSketches`／`.apply()`）。
- 型錄屬性清單中「`BANG`＝`DESP[10]`」似為官方筆誤（參數表為 `DESP[63]`，且 `AOFF` 為 `DESP[10]`）。

## 39.21 取材覆蓋

- **Equipment：** 根頁 `1152005` 與全部子頁（清單 116 行，含重複的練習頁）皆已讀過。
- **HVAC Designer：** 清單共 463 行，**實際讀過約 200 頁**：HVAC Administrator 全部上層頁、教學練習（`1155017`–`1155038`）與 Draft Sketches 子頁；HVAC 使用指南的概念、階層、HVAC Window 與屬性、System／Branch、Divide、Assembly、Tiles／Grid、Autofill、工具與 Query、Split、Spool、Sketch、Menu Map、Work Area、Palettes、設計參數表，以及代表性元件視窗（Straight、Radiused Bend、Boot、Motorized Damper、General Plant Item、Grille off Brco、Air Handling Unit、Nozzles）與 Joint／Stiffener 清單。
- **未逐頁讀（約 260 頁）：** `Components` 下其餘約 150 個個別元件視窗（欄位清單，結構同已讀頁）與 `HVAC Catalog` 下約 100 個型錄元素頁（多為參數化幾何示意圖）。
- **圖片：** 16 張皆先預覽再加入（Equipment 9 張、HVAC 7 張）。
