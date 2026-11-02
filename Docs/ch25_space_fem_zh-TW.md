# 第 25 章　空間管理與有限元素模型：Space Management 與 Finite Element Model

> 前面談船體建模（[第 5 章](ch05_hull_modelling_zh-TW.reading.html)）與生產資料（[第 6 章](ch06_hull_production_zh-TW.reading.html)）時，模型的主角是「鋼板與加強材」。這一章換兩個視角：**把船切成「空間」來管理**（艙室、區域、分段、塗裝區），以及**把鋼結構簡化成「有限元素模型」交給外部結構分析軟體**。
>
> 兩者看似無關，其實共用同一條脈絡：它們都吃 Structural Design 的共同參考模型（Common Reference Model），都在艙室、分段或板架的「邊界」上做文章，也都把結果丟給下游——前者丟給水動力計算、載重電腦、生產計畫與塗裝估算，後者丟給 ANSYS、Patran、Nastran、Sesam 與 MAESTRO。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的 **Space Management** 與 **Finite Element Model** 兩個模組（頁面含英文原文與機器中文對照，本章以自己的話重組並以英文原文為準）。官方文件對「空間」只描述功能與屬性，**沒有給出資料庫元素的完整型別階層**，也沒有說明 FE 模型的載重與邊界條件如何設定，這些在文中標為〔待核對〕。檔案格式只寫文件有給出者（Block CSV、Space 目的控制檔、材料 XML、Hull Steel XML 的存在）；沒有依據的「二次開發接點」一律標〔待核對〕，不編造指令。圖片取自官方文件，僅供內部教學。

## 25.1 學習目標

讀完本章，你應該能夠：

1. 說明「空間」不是逐一建模，而是由「封閉邊界（Envelope）」被「分割限制（Dividing Boundary）」自動切出來的。
2. 區分 Space World（空間世界）、Arrangement（空間佈置）與 Space（空間），以及六種佈置類型各自的用途與預設顏色。
3. 說明 Reference Surface Object（RSO）、Envelope、Block 與 Surface 在共同參考模型中的角色，並知道哪些功能放在 Project 與 Functional Structure 選單。
4. 依序完成「建 Space World → 設 Envelope → 分割 → 布林運算 → Apply」並用 Merge、Rename、Purge、Void 整理成果。
5. 設定空間用途（Space Purpose）與絕緣圖形控制檔，並說明它們對計算與圖面的影響。
6. 用 Get Structure within 取出空間內的鋼結構，計算塗裝面積、重量重心、材料清單與焊接長度，並讀懂 `SPM*` 屬性。
7. 說明空間如何轉成艙室（Compartment）、生產分段（Block），以及如何輸出給水靜力計算模組。
8. 說明 FE 模型兩階段流程：Idealization（理想化）→ FE Model（網格前處理），以及每階段的主要參數。
9. 解讀 Holes、Stiffeners、Swages 等處理規則，並用 FE Image 與 Statistics 檢查網格品質。
10. 列出五種 FE 輸出方式與材料資料來源，並說明二次開發者目前有依據的串接點與待核對項目。

## 25.2 兩個模組在整體中的位置

兩個模組都在 Structural Design（Hull）環境中，板架與曲面來自第 5 章。差異如下：

- **Space Management**：輸入是曲面、RSO、Envelope 與既有空間；產物是 Space World／Arrangement／Space；輸出是艙室、生產分段、水靜力 XML、Excel 報表與 CSV。艙室輸出接 [第 19 章](ch19_loading_computer_zh-TW.reading.html)。
- **Finite Element Model**：輸入是 Block 或 Panel、曲面與接縫、材料資料；產物是理想化區塊與 FE 幾何；輸出是 ANSYS APDL、Patran PCL、Nastran BDF、Sesam FEM、MAESTRO MNF 與 Hull Steel XML。功能所在選單〔待核對〕。

> **專業提醒：** 這兩個模組處理的都是「**簡化後的幾何**」。空間是以邊界切出來的體積，FE 模型是理想化的中面。它們都不是施工圖，也不是原始模型本身；改了原始板架或曲面，必須重新產生（Recreate／重新理想化），否則下游拿到的是舊資料。

---

# 第一部分　Space Management

## 25.3 基本概念

### 25.3.1 空間是「切」出來的，不是「畫」出來的

官方文件強調：**個別空間不是逐一建模的**。流程是：

1. 使用者定義一個**封閉體積**作為外框，稱為 **Envelope（包絡）**。它可以由曲面與 RSO 圍成，也可以直接選用另一個佈置中已存在的某個空間（此時會形成空間階層）。
2. 用雕塑曲面（sculptured surface）與 RSO 當作**分割限制（Dividing Boundary）**。
3. 分割是全自動的；只要切出封閉體積，就在 Arrangement 裡產生 Space。

好處是：艙壁改位置，只要重做分割，空間就跟著變，不用手工重畫每個艙。

### 25.3.2 Space World、Arrangement 與 Space

| 層級 | 說明 | 重點 |
|---|---|---|
| Space World | 空間世界，建立時就指定「類型」 | 其下所有佈置都是同一類型；類型決定屬性集合與預設顏色、透明度 |
| Arrangement | 空間佈置，同一目的下的一整套切分方案 | 同一個 World 可有多套 Arrangement，方便比較方案 |
| Space | 單一空間（封閉體積） | 預設名稱形式為 `<佈置名>_<空間名>` |

六種預設類型如下（官方文件以顏色名稱與透明度列出）：

| 類型 | 用途 | 預設顏色 | 透明度 |
|---|---|---|---|
| Generic | 其他類型都不適用時使用 | Salmon | 50% |
| Compartment | 適合水靜力與水動力計算 | Brightred | 50% |
| Layout | 一般佈置工作；可規劃、儲存並追蹤質量屬性 | Pink | 50% |
| Painting Areas | 塗裝面積計算 | Deeppink | 50% |
| Production Blocks | 定義生產分段結構 | Maroon | 50% |
| Zones | 定義船體結構的區域 | Orangered | 50% |

> **重要：** 某些功能只能用在特定類型。例如「生產分段」只能由 Production Blocks 類型的佈置產生；塗裝面積只能存在 Layout 或 Painting Areas 的空間；重量重心只能存在 Layout 或 Production Blocks 的空間。建立 World 時選錯類型，後面就改不了（類型下拉選單在 World 建立後會反灰）。

### 25.3.3 幾何運算與 Void

任何封閉體積（雕塑曲面，或另一個佈置的空間）都能被**加入（Add）**或**減去（Subtract）**於佈置，兩個相鄰空間也能**合併（Merge）**成一個。對不感興趣的空間，可設為 **Void（空）**，它就不顯示、不參與運算與計算。

> **專業提醒：** Void 不是刪除。空間仍在資料中，只是被排除。需要「不計入重量」或「不顯示」時用 Void；真正不要時才用 Purge（見 25.6.3）。

## 25.4 專案設定

官方文件把 Project Set-up 分成四件事：Space World、圖面表現（絕緣）、Space Purpose、塗裝區設定。

### 25.4.1 建立 Space World

建立 World 與其底下所有佈置時，**預設使用第一個可寫入的資料庫**。若要存放在指定資料庫，需從命令列明確建立 World 元素，官方給出的語法是：

```text
NEW SPMSW /<name> DB <team>/<dbname>
```

這裡的 `<team>/<dbname>` 即第 20 章談過的「團隊名／資料庫名」命名（見 [第 20 章](ch20_system_administration_zh-TW.reading.html)）。

> **專業提醒：** 空間資料量不大，但**資料庫歸屬**很重要：它決定誰能寫、備份跟著哪個 DB、分散式專案是否要 Extract。多人同時規劃不同佈置時，建議事先規劃專屬的 DB 與 Team，而不是任由系統挑「第一個可寫 DB」。

### 25.4.2 圖面中的絕緣圖形（控制檔）

絕緣元件本身**不含**在圖面如何表現的資訊，要另外定義。流程：寫一份控制檔，由 **Inithull** 程式編譯，產生控制物件 `__SPACE_INSULATION__`。重點：**絕緣元件名稱與控制檔中 `INS` 敘述的名稱必須完全相同。**

`INS` 敘述的結構（依官方語法整理）：

| 參數 | 意義 |
|---|---|
| `INS,<絕緣元件名>` | 要定義圖形表現的絕緣元件 |
| `/LT_SECTION`、`/COL_SECTION` | 剖面圖的線型與顏色 |
| `/LT_PLANE`、`/COL_PLANE` | 平面圖的線型與顏色 |
| `/HATCH_ANGLE` | 平面圖剖面線角度（度） |
| `/HATCH_DIST` | 剖面線間距（mm） |

顏色與線型名稱請查 Marine Drafting User Guide 的 Color Tables 與 Line Types。絕緣元件本身在 Paragon 的 Steelwork Application 中定義（見第 8 章目錄與規格）。

### 25.4.3 空間用途（Space Purpose）與控制檔

**Layout、Compartment、Zones** 類型的空間是為特定用途而設計，需帶有計算與下游設計要用的屬性。為了簡化指定，官方提供「**先定義所有可能性質，再組合成用途**」的機制。可預先定義六類性質，各以「代碼＋說明」建立：

- 內容類型 `TYPE_SEL`：儲物、居住、機艙、空、乾貨、液貨、使用者定義（`TYPE_UD1`～`TYPE_UD50`）。
- 密性 `TIGHT_SEL`：氣密、非密、油密、水密、風雨密、使用者定義。
- 噪音類別 `NOISE_SEL`、進出 `ACCESS_SEL`（僅船員、僅高級船員、受限、不受限）、安全 `SAFETY_SEL`（Class A／B／C）、保全 `SECURITY_SEL`（機密、祕密、非機密），皆可再加使用者定義。

然後以 `PURP` 敘述把這些性質與三個數值組合成「用途」：

| 參數 | 意義 | 限制 |
|---|---|---|
| `/DENS` | 密度（kg/m³） | — |
| `/STRUC` | 結構裕度 | 0 到 1 |
| `/PERM` | 滲透率 | 0 到 1 |

控制檔另有 `MODE` 敘述（`/NEW` 新建並可能覆蓋舊物件、`/UPDATE` 更新既有物件）與 `LIST` 敘述（列出現有內容；若無物件則列出預設）。編譯成功後，系統存入控制物件 `__COMP_PURP__`。第一次使用 Attributes 功能時，系統會自動產生預設物件，可先 `LIST` 當作客製化的起點。

> **專業提醒（接載重電腦）：** 把空間輸出到水靜力計算（見 25.7）時，內容類型是否被正確解讀，取決於用途所關聯的**類型定義**。類型定義要自訂並給唯一 ID，說明必須是 Liquid、Solid、Grain 或 Untrimmed 其中之一，其關聯密度會用在該空間上。所以 `/DENS` 不是隨便填的註解，而是會進計算的數值。

### 25.4.4 塗裝區設定

文件這一節只指向「Surface Treatment Selection Tables」（見第 8 章目錄與規格）。塗裝區面碼（Face Code）的設定來源與格式，本章〔待核對〕，僅知 Face Code 功能依賴它（見 25.6.5）。

## 25.5 共同參考模型：Project 與 Functional Structure 選單

空間要靠曲面與 RSO 當邊界，而它們都屬於「共同參考模型」。官方把相關功能分在兩個選單。理解它們，才知道空間的邊界從哪裡來。

### 25.5.1 Project 選單（整個專案層級的設定）

- **Surfaces**：登錄主船殼、甲板與附加曲面（需先由 Lines 或 Surface/Compartment 釋出）；除主船殼外後綴必須唯一；只能有一個 Main Hull、一個 Main Deck。
- **FR/LP Positions**：肋骨與縱向位置，以 start／step／end 表示；可定義多組位置表（例如鋼製下半＋鋁製上半）。
- **Block**：建立與維護 Design／Production Block（Edit、Recreate、Create from CSV、Extract to CSV）。
- **Midbody Surface**：快速建立平行中體曲面。
- **Envelope**：以曲面與 RSO 組成封閉體積，作為 RSO 的外邊界；需 Save Envelope。
- **Verify Model**：檢查板架與分段的拓撲相依性，透過 Job Launcher 執行。
- **Recreate Limit Tables**：重建接縫、縱材、橫材的限制表（為了效能，每個曲面一組）。
- **Project Information**、**Change View Mode**：專案主尺度，以及 Design／Production 檢視模式切換（多視圖專案才可切換）。

**Verify Model** 值得多說一句：它是從結構設計進到細部設計（Block Splitting）前的「體檢」。官方列出的警告例子包含板架名稱太長（建議最長 17 字元，超過 19 就應改名）、邊界引用的曲線或板架不存在、輪廓無法重建缺口、拓撲物件不存在或與板架不一致等。多數處理方式是「重新產生並儲存板架以更新拓撲物件」，拓撲資料庫不一致時則需用公用程式更新（文件提及 `sj903`）。

### 25.5.2 Block：CSV 批次建立

Block 的 CSV 是本章**少數有明確欄位定義的檔案格式**，對二次開發最有用。檔案規則（依官方整理）：

- 第一列視為註解，不處理。
- 每一列一個分段，欄位依序為：類型（`D` 設計分段或 `P` 生產分段）、名稱、六個名義限制（Aft、Stbd、Bot、For、Port、Top）、所屬分段（Encl. Block，只在建生產分段且專案同時有設計分段時需要）、六個偏移值（mm）、六個限制物件、對稱（Yes／No）、顏色（整數）。
- 名義座標可用 X／Y／Z，也可用肋骨與 LP 位置。
- 限制物件以前綴指定類型：`SUR/` 曲面、`RSO/` 參考面物件、`PLA/` 儲存平面。
- 區塊已存在且資料有變，才會更新；沒變就不動。

反向的 **Extract to CSV** 會把目前的分段結構輸出成同格式檔案，放在 `SB_SHIPDATA`，並透過 Job Launcher 取用。

> **專業提醒：** Create from CSV 與 Extract to CSV 同格式，所以可做出「抽出 → 在試算表調整 → 再匯入」的迴圈。每次調整後建議先在測試專案跑一次，再套到正式專案；欄位順序一旦錯一格，名義限制與偏移值會對錯位置。

### 25.5.3 Functional Structure 選單：RSO 與曲面

**RSO（Reference Surface Object，參考面物件）** 是一個有邊界的平面（或由多片子平面組成），用來代表艙壁、甲板、桁材等「結構面」。它既是 Envelope 與空間的分割限制，也可讓板架引用它的位置——引用 RSO 的好處是：即使 RSO 最初含有巨大的 jumbo 板架，之後再細分成細部設計用的板架，引用仍然穩定。

| 功能 | 說明 |
|---|---|
| Key In | 以輸入位置並選取限制物件建立 RSO |
| Sketch 2D | 在 Symbolic Planar View 或 Backdrop View 以 2D 工具畫折線，建立 RSO；有 Draw／Select／Trim；可開 Grid、Mirror Copy |
| From Backdrop | 由 Backdrop 視圖建立 RSO（Backdrop 須在主平面），視圖內所有幾何存為 RSO 上的 marking |
| From Panel | 由既有板架建立或更新 RSO，可選擇讓板架改為依賴 RSO 定位 |
| Recreate | 限制物件或 Envelope 改變後重建幾何 |
| Edit Shape | 以剖面表格修改形狀（見下） |
| Copy／Move／Rename | 複製（可用重複語法一次多份）、移動、改名 |
| Change Envelope | 把 RSO 移到另一個 Envelope |
| Properties | 為 RSO 加建模屬性，以便自動產生鋼結構 |
| Generate Panels | 依 RSO 自動產生第一版鋼板架 |
| Disconnect／Delete | 解除或刪除 RSO，並把引用它的板架改為以主軸位置或三點定位 |
| Create Curved Surface | 建立參數曲面：Cylinder、Cone、Fillet 三類 |

**Rename 的限制**：改名會更新位於該 RSO 內的板架與拓撲相依的 RSO 邊界，但**其他拓撲相依不會自動更新**，例如以該 RSO 為邊界限制的船體板架需手動更新。

#### Edit Shape：剖面驅動的形狀編輯

> 〔公開版未收錄：AVEVA 官方產品截圖〕RSO 的 Edit Shape 對話框：上方限制與 Envelope，下方以剖面（Profile）與剖面點表格定義形狀

*圖 25-1　RSO 的 Edit Shape 對話框。形狀由數個剖面（Cross-section）及相同數量的定義點組成。（AVEVA 官方文件截圖，僅供內部教學）*

要點：所有剖面的定義點數量必須相同；RSO 的**四邊形面不得有折角（knuckle）**。「Keep profile parallel」自動調整相關值避免折角；「Single cell edit」關閉這套演算法，改完後選一個不動的剖面按 **Iron** 讓其餘剖面重新符合。編輯歷史與 Undo/Redo 不同：往回走後再修改是**新增**一筆歷史。「Show absolute coordinates」勾選時，輸入也被當成絕對值，**輸入前先確認勾選狀態**。

#### Properties 與 Generate Panels：自動產生第一版鋼結構

Properties 的前置條件之一，是從 Surface/Compartment 釋出時，Main Deck 與 Envelope 的限制要正確標記，否則限制可能被命名為 `HULL_NOT_KNOWN`，且曲面需另外在 Project > Surfaces 登錄。

Generate Panels 只處理已標記要自動產生鋼結構、且有功能描述（Functional Description）的 RSO。流程是先甲板、再其他板架，全部放進名為 `JUMBO` 的 Block（不存在就自動建立）；板架名稱形式為 `JUMBO-><RSO 名去前綴>_<面編號>`。依功能描述碼產生的內容：

依功能描述碼產生：甲板（9000–9099）為板材加橫向縱材位置的加強材；縱艙壁（9100–9199）為板材加垂直縱材；橫艙壁（9200–9299）為板材加加強材，可依要求加肘板；一般肋板構件（9400）依相交的 RSO 產生肋板、斗櫃橫向腹板與垂直腹板；其他功能描述只產生板材。加強材與其他 RSO（例如縱艙壁與甲板）相交處不放。

所有板架類型都會加切口（Cutout），定義取決於自動切口設定。使用 FRP（玻璃纖維）選項時，需指定預設積層代碼的邏輯變數 `SBH_GRP_LAM`。

> **專業提醒：** Generate Panels 產生的是「**第一次嘗試**」，不是最終板架。官方自己的措辭就是 first attempt。它的價值在早期設計階段快速得到可用於量化的 jumbo 板架，之後仍要細分、補強材與細部設計。

## 25.6 建立與管理空間

### 25.6.1 Space 選單總覽

Space Management 選單的功能大致分六組：建立與整理（Space XML Input、Select and Create、Merge two spaces、Rename、Purge、Void State）；絕緣（Insulation、Legend、Report）；取出結構與計算（Get Structure within、Add Extract as View、Hide/Unhide、PaintArea、WCOG、Material List、Weld）；顯示與屬性（View Property、Face Code、Attributes、Copy Attributes、Distributed Attributes、Planning Mass Prop.）；CE and Draw；以及產生下游資料的 Generate 子選單。

### 25.6.2 Select and Create：建立或修改一個佈置

這是整個模組的核心對話框：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Space Arrangement 對話框：World、Arrangement、Type，Envelope、Dividing Boundaries 與 Boolean Operations 三區

*圖 25-2　Select and Create 的 Space Arrangement 對話框。左側為可用的 Surfaces 與 RSO，中間為 Envelope 邊界與分割邊界，右下為布林運算。（AVEVA 官方文件截圖，僅供內部教學）*

操作步驟：

1. **選或鍵入** World 與 Arrangement 名稱。新 World 必須指定 Type（建立後鎖定）；選已存在的佈置，會帶出它的 Envelope、分割邊界與布林運算。
2. **定義 Envelope**。二選一：從 Surfaces／RSO 清單選取，用 `A>>` 或右鍵加入 Boundaries 清單；或選「Select Space」，以 Pick in Dwg 在圖上點選，或鍵入佈置名與空間名。若選到的是 Envelope（而非單純曲面），會沿用其定義資料。
3. **分割**：同樣用 `A>>` 或右鍵把曲面與 RSO 加入 Dividing Boundaries；`<<R` 移除選取項目。
4. **布林運算**：曲面在 Surface 清單選，空間用 Pick in Dwg 或右鍵選單，指定加入或減去。
5. 按 **Apply** 建立（或重建）。結果會畫在 3D Canvas。

**Space XML Input** 則是另一條路：選一個 XML 檔，系統依檔內指定的內容建立佈置。官方沒有給出 XML 的結構。

> **專業提醒：** 重新 Apply 同一個佈置時，原有空間不會立刻消失；「重建後殘留的舊空間」會被保留，可用來複製屬性（Copy Attributes 的 Option 就能看到這些 obsolete 空間）。這既是便利，也是日後 Purge 的原因。

### 25.6.3 合併、改名、清理與 Void

| 功能 | 做什麼 | 注意 |
|---|---|---|
| Merge two spaces | 在 2D Canvas 點選兩個相鄰空間合併 | 新空間的屬性取自**先選**的那一個；要拿到另一個的屬性，請用 Copy Attributes |
| Rename | 在圖面點選空間改名 | 語法 `新名稱<數字>(<步進>)` 可連續編號；Cancel 可還原最後一次改名；系統預設命名 `<佈置名>_<空間名>`，只需給空間名，格式會保留 |
| Purge | 刪除佈置內因重建或合併而殘留的過時空間 | 執行後無法再從它們複製屬性 |
| Void State | 設為空（不顯示、不參與運算），或取消 | 先指定顯示狀態（顯示 void 或 non-void），再點選空間切換 |
| CE and Draw | 把點選的空間設為 CE（Current Element）並畫在 3D Canvas | 方便用其他功能或 PML 繼續操作 |

### 25.6.4 設定空間的屬性

空間本身只是幾何，工程資料要靠屬性。

| 功能 | 做什麼 |
|---|---|
| Attributes | 依 Space Purpose 設定基本屬性；僅適用 Layout、Compartment、Zones；與類型無關的欄位會反灰；說明文字會成為符號視圖上的標註 |
| Copy Attributes | 把全部或選取屬性從一個空間複製到另一個；可顯示過時空間作為來源 |
| Distributed Attributes | 設定「分佈式屬性」：先在設定階段建立 bound attribute 組合，再於格狀對話框填值 |
| Face Code | 為 Painting Area 佈置中的空間指定面碼 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Space Purpose 對話框：Purpose、Type、Description 與密性、噪音、進出、安全、保全等欄位

*圖 25-3　Attributes 功能的 Space Purpose 對話框。欄位內容來自 25.4.3 的用途控制檔。（AVEVA 官方文件截圖，僅供內部教學）*

> **專業提醒：** 「分佈式屬性」的設定細節，官方在 Space Management 模組中只說「set-up of attributes must have been made」，沒有說在哪裡設定。本章〔待核對〕；建議向熟悉專案設定的管理員確認，不要自行假設。

### 25.6.5 圖面表現

**View Property** 設定符號視圖（Symbolic View）中每個空間要顯示什麼：空間名、說明、體積、面碼（塗裝區佈置）、絕緣，以及分佈式屬性。

> 〔公開版未收錄：AVEVA 官方產品截圖〕符號視圖中的空間標註：空間名稱、說明（Pump room、Access trunk）與體積（m3）

*圖 25-4　View Property 控制下的空間標註範例：名稱、說明與體積。（AVEVA 官方文件截圖，僅供內部教學）*

## 25.7 空間與艙室、分區、設備的關係

### 25.7.1 官方文件明確給出的關係

| 關係 | 說明 | 做法 |
|---|---|---|
| 空間 → 艙室（Compartment） | Compartment 類型佈置可轉成 Surface and Compartment 模組可用的艙室 | Generate > Blocks and Compartments |
| 空間 → 生產分段 | Production Blocks 類型佈置可轉成生產分段 | 同一對話框，含建資料庫與頂層元素的前置工作 |
| 空間 → 水靜力計算 | Compartment 佈置與 Zone 限制可輸出給計算模組 | Generate > Calculation Geometry，產出可被 calc 讀取的 XML |
| 空間 → 圖面 | 空間在符號視圖中以標註呈現 | View Property、Legend |
| 空間 → 結構資料 | 取出空間內鋼結構，量化後寫回空間屬性 | Get Structure within 與其後續功能 |

**Blocks and Compartments 產生生產分段的流程**（官方描述）：

1. 先用 **Admin Data** 產生一份 Excel，內含「每個分段一個資料庫」的資料，且全部使用 `HULL` 團隊；它是**範本**，可編輯後，在 Admin 模組以 Utilities > Import 匯入。**Team 必須先在 Admin 手動建好。**
2. 用 **Top Element Data** 產生一個 PML 函式檔，執行後會在這些資料庫建立頂層元素；同樣是可編輯的範本。
3. 最後 **Generate Blocks** 由空間建立 Block 物件；若空間名為 `<佈置名>_<空間名>` 形式，只取空間名作為 Block 名。

> **專業提醒：** 這一流程橫跨三個地方：空間模組、Admin 模組（見 [第 20 章](ch20_system_administration_zh-TW.reading.html)）與 PML。分段數量多時，建議先在測試專案演練一次，確認 Admin 匯入權限、資料庫數量與命名後再套正式專案。

### 25.7.2 與載重電腦／水艙資料（第 19 章）的分工

[第 19 章](ch19_loading_computer_zh-TW.reading.html) 討論的是「**載重電腦需要什麼資料**」：水艙特性表、測深、自由液面、重量重心。本章的 Space Management 是其中**艙室幾何與內容類型的上游來源之一**。分工如下：

| 項目 | 本章 Space Management | 第 19 章 |
|---|---|---|
| 艙室邊界與體積 | 由 Envelope 與分割產生 | 不重複 |
| 內容類型與密度 | 由 Purpose／類型定義提供，`Liquid／Solid／Grain／Untrimmed` | 說明如何對應水艙表 |
| 輸出介面 | Calculation Geometry → XML 給 calc 模組 | 載重電腦端如何接收與對帳 |
| 水艙特性表（測深、容積、LCG、自由液面） | **官方文件未涵蓋**〔待核對〕 | 完整說明 |

「**設備與管路**」與空間的關係，官方 Space Management 章節沒有提及設備位置判定、設備掛到空間之類的功能，本章不推測〔待核對〕。若要判斷某設備落在哪個艙室，可能需要自行用位置與空間邊界比對，屬於二次開發題目，見 25.9。

### 25.7.3 官方的三個設計情境

官方以生產規劃（Production Blocks）、塗裝區規劃（Painting Areas）、穩度計算（Compartment）三個情境說明為何需要多種佈置，三者共通模式是**先估算（Estimated）、再計算（Calculated）、最後比對**，這正是 25.8 中 `SPME*` 與 `SPMC*` 屬性成對出現的原因。

## 25.8 從空間取結構、算量與報表

### 25.8.1 工作流程

空間量化的順序可以用下面這條線記住（依 25.8.2 的官方功能說明整理，非官方圖）：

```text
Select and Create（建佈置）
  -> Get Structure within（取出空間內的暫時結構，同一 session）
  -> [Hide/Unhide 排除不計入的板架]
  -> PaintArea / WCOG / Material List / Weld（計算）
  -> 結果寫回空間屬性 SPMCAS / SPMCWS / SPMCOS，或輸出 CSV
  -> Planning Mass Prop. 與 Report（Excel 報表）
```

**Get Structure within** 取出位於空間內或邊界上的所有船體鋼結構，並產生一個「**在空間邊界處精確切斷**」的**暫時性模型**。重點：

- 這個暫時模型**不會**在 Save Work 時永久存入資料庫。
- 結果放在自動命名為 `_D<流水號>` 的 Block 中。
- 位於空間邊界上的板架，應位於對應的 RSO 內，否則會有公差問題。
- 之後的 Paint Area、Weight and Center of Gravity、Material List、Weld **必須在同一個工作階段（session）內**接著做，因為取出的模型不會被保存。

相關功能：

| 功能 | 做什麼 |
|---|---|
| Add Extract as View | 把暫時 Block 加為圖面中的新視圖 |
| Hide/Unhide | 隱藏取出的板架，使其不參與計算；隱藏者以薄表示，不畫加強材與肘板 |

### 25.8.2 計算與結果去向

| 功能 | 結果去向 | 限制 |
|---|---|---|
| PaintArea | Log Viewer；塗裝面積存於屬性 `SPMCAS` | 只能存在 Layout 或 Painting Areas 空間；面碼會進報表 |
| WCOG（重量與重心） | Log Viewer；重量存 `SPMCWS`，重心存 `SPMCOS` | 只能存在 Layout 或 Production Blocks 空間 |
| Material List | Log Viewer | 板材與型材的材料清單 |
| Weld | 專案 list 目錄下的 CSV，檔名 `ed_weld_<流水號>.csv` | 焊接報告 |

### 25.8.3 Planning Mass Properties 與 `SPM*` 屬性

這個功能以格狀對話框管理質量屬性（重量、面積、焊長），欄位對應空間屬性。以 Layout 佈置為例：

| 欄位 | 屬性 | 欄位 | 屬性 |
|---|---|---|---|
| Estimated Steel Weight | `SPMEWS` | Calculated Steel Weight | `SPMCWS` |
| Calculated Center of Steel | `SPMCOS` | Estimated Steel Area | `SPMEAS` |
| Calculated Steel Area | `SPMCAS` | Estimated Weight of Space Content | `SPMEWC` |
| Calculated Weight of Space Content | `SPMCWC` | Estimated Fillet Weld Length | `SPMEWL` |
| Calculated Fillet Weld Length | `SPMCWL` | Estimated Butt Weld Length | `SPMEWB` |
| Calculated Butt Weld Length | `SPMCWB` | | |

Production Blocks 佈置只有鋼重（`SPMEWS`、`SPMCWS`）、鋼重心（`SPMCOS`）與鋼面積（`SPMEAS`、`SPMCAS`）；Painting Areas 佈置只有鋼面積（`SPMEAS`、`SPMCAS`）。**估算值可由使用者填寫**，按 OK 後寫入屬性；**計算值由 PaintArea、WCOG、Weld 功能算出**。官方註明「Calculated Weight of Space Content」**尚未實作**。

### 25.8.4 報表

| 報表 | 產生者 | 內容 |
|---|---|---|
| Insulation Report | PML 函式 `insulationReport.pmlfnc`（安裝目錄 `PMLLIB\design\functions`） | Excel：空間名、面號、面積（m²）、絕緣元件、總厚度、密度（kg/m³）、體積（m³）、重量（kg）、價格參考 |
| Mass Properties Report | PML 函式 `massPropReport.pmlfnc`（同目錄） | Excel：空間名、估算重量（噸）、計算重量（噸）、鋼重心（m） |
| Weld Report | Weld 功能 | CSV `ed_weld_<n>.csv` |
| Legend | Legend 功能 | 圖面上的絕緣表（符號、說明、各層厚度與類型、總厚度、固定方式） |

官方明講兩支 PML 函式使用者可以修改，使報表**完全客製**——這是二次開發最直接、有依據的切入點。

> **專業提醒：** 修改 `insulationReport.pmlfnc` 或 `massPropReport.pmlfnc` 時，請**複製到自己的 PMLLIB 路徑**，不要直接改安裝目錄下的原檔，以免升級時被覆蓋（路徑搜尋與部署見第 10、17 章）。

## 25.9 二次開發者怎麼接（Space Management）

下表只列官方文件有依據的接點；沒有依據者標〔待核對〕。

| 接點 | 依據 | 說明 |
|---|---|---|
| Block CSV（輸入／輸出） | 官方給出欄位格式 | 用腳本產生或解析，批次建立／更新設計與生產分段；Extract 檔放於 `SB_SHIPDATA` |
| Space XML Input | 官方只說可從 XML 建立佈置 | XML 結構〔待核對〕 |
| 建立 Space World 的命令 | 官方給出 `NEW SPMSW /<name> DB <team>/<dbname>` | 可放進 PML 或命令檔批次建立 |
| 用途控制檔 | 官方給出 `MODE`／`TYPE_SEL`／`PURP` 等語法 | 可由公司標準自動產生，再由 Inithull 編譯 |
| 絕緣圖形控制檔 | 官方給出 `INS` 語法 | 同上 |
| 報表 PML 函式 | 官方指出兩支 `.pmlfnc` 可修改 | 客製欄位、單位、價格 |
| `SPM*` 屬性 | 官方列出屬性名 | 可由 PML 或 .NET 讀取空間上的值（讀取語法見第 12 章；屬性是否可由 .NET 直接讀取〔待核對〕） |
| Weld CSV | 官方給出檔名規則 | 後處理工具直接讀 |
| 計算模組 XML | 官方說明輸出可被 calc 讀取 | XML 結構〔待核對〕 |
| 空間與設備位置比對 | 官方未涵蓋 | 若自行開發：取空間幾何與設備座標比對〔待核對，屬推論〕 |

> **專業提醒：** 空間的類型、命名與屬性（特別是 `Purpose` 代碼與 `/DENS`）一旦被下游工具依賴，就等於成為**介面契約**。改名或重新編譯用途控制檔（`/NEW`）前，先查有哪些報表、腳本與計算在使用。

### 25.9.1 空間模組常見錯誤

- **World 類型選錯**：類型鎖定後不能改，之後無法產生分段或存重量；建立前先確認用途。
- **Envelope 未封閉**：分割後沒有切出空間；確認曲面與 RSO 構成封閉體積。
- **取出結構後換了工作階段**：PaintArea、WCOG 找不到取出的模型；取出後同一 session 立即計算。
- **邊界板架不在 RSO 內**：取出結構有公差缺漏。
- **類型不符**：塗裝面積只能存 Layout／Painting Areas，重量只能存 Layout／Production Blocks。
- **Merge 後屬性遺失**：先用 Copy Attributes 補，再 Purge。
- **絕緣名稱與 `INS` 名稱不一致**：圖面不再顯示絕緣圖形。

---

# 第二部分　Finite Element Model

## 25.10 用途與整體流程

**有限元素分析（FEA）** 要的不是細部設計模型，而是簡化後的**中面（moulded plane）**幾何、用 shell／beam／truss 表示的元素，以及材料與元素屬性。AVEVA Marine 的 FE Model 模組負責「**預網格（pre-mesh）**」：從 Hull 板架模型產生一份接近最終網格的 FE 幾何，再輸出給外部軟體做最後網格、載重與求解。

| 階段 | 官方名稱 | 做什麼 | 產物 |
|---|---|---|---|
| 0. 前置 | Prerequisites | 建立 `FEMWLD` 元素 | FE 世界元素 |
| 1. 理想化 | Idealized Model | 選 Block／Panel、可選邊界盒、設定理想化參數 | 理想化區塊（Idealized Block） |
| 2. FE 建模 | FE Model Creation | 由理想化區塊產生 shell／beam／truss，並整理網格 | FE 幾何 |
| 3. 檢查 | FE Image、Statistics、Check | 視覺化與統計檢查 | FE 影像物件、統計 |
| 4. 輸出 | FE Model Output | 匯出給外部軟體 | APDL、PCL、BDF、FEM、MNF、Hull Steel XML |

> **注意：** 官方文件沒有提供「載重」與「邊界條件」如何設定的說明；材料性質以外的分析定義，本章推論是在外部 FE 軟體中完成（輸出說明都寫「for further meshing and analysis」）。〔待核對：是否有任何載重或邊界條件資料隨輸出傳遞〕

### 25.10.1 前置：FEMWLD

執行任何理想化前，必須先有 `FEMWLD` 元素；否則會出現訊息 *A FEMWLD element needs to be created before this function can be used*。建立方式有二：在 DbPrompt 設定專案時建立，或在 Hull Structural Design 的命令視窗輸入：

```text
NEW FEMWLD /FEMWLDNAME DB DBNAME
```

`FEMWLDNAME` 是要建立的世界元素名，`DBNAME` 是既有的設計資料庫。這同樣牽涉資料庫歸屬（見第 20 章）。

## 25.11 第一步：理想化（Idealization）

### 25.11.1 理想化做了什麼

選取一部分模型（Block 或 Panel，可跨多個 Block，可選邊界盒），結果是一種新的區塊，內含**理想化板架**。理想化會：

- 移除不重要的零件；
- 幾何以**中面**表示，彷彿板沒有厚度、加強材沒有斷面；
- 邊界盒外的部分被裁掉（部分在盒內的平面板架會被裁切；完全在盒外者忽略）；
- 板面以半透明、加強材與折邊以輪廓顯示，與一般板架區隔，也可用 Scheme Editor 調整。

> 〔公開版未收錄：AVEVA 官方產品截圖〕一般板架（Ordinary panels）：完整的板與加強材，綠色板面與紅色加強材

*圖 25-5　理想化前的一般板架。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕理想化後的板架：半透明板面與輪廓加強材

*圖 25-6　理想化後的板架。不重要的零件已被移除，板以半透明面、加強材以輪廓表示。（AVEVA 官方文件截圖，僅供內部教學）*

**曲面板架（Curved panel）處理方式不同**：它只用來取得曲面上開孔的幾何，以及在未指定邊界盒（或盒超出板架範圍）時計算 FE 模型的邊界盒。建 FE 模型**不一定要有**曲面板架，因為要建模的曲面部分是由平面板架與曲面相交的軌跡曲線決定。

### 25.11.2 選取模型

> 〔公開版未收錄：AVEVA 官方產品截圖〕Finite Element Idealiser 對話框的 Selection 頁籤：Model objects 樹、Selected model objects、邊界盒與區塊設定

*圖 25-7　Finite Element Idealiser 的 Selection 頁籤。左為模型樹，下方為邊界盒與區塊選項。（AVEVA 官方文件截圖，僅供內部教學）*

操作：

1. 在 Model objects 樹選取 Block 或 Panel，按 **Add**。
2. 需要時設定邊界盒（Xmin／Xmax 等，預設 `NO_LIMIT`）。
3. 指定理想化區塊名稱。區塊不存在時，套用 Idealisation Settings 頁籤的設定；已存在時，可勾選 **Get idealisation settings from block** 沿用區塊內存的設定。
4. 可選 **Add to existing block** 把板架加到既有區塊；此時請確定被選的板架在該區塊內**尚無**理想化版本。

### 25.11.3 理想化設定（Idealisation Settings）

> 〔公開版未收錄：AVEVA 官方產品截圖〕Idealisation Settings 頁籤：分析類型、預期元素尺寸與各零件頁籤

*圖 25-8　Idealisation Settings 頁籤：Global／Local／Detailed／Fine 分析與預期元素尺寸（示例 400×400），下方是各零件的忽略規則與 Girder 元素型式。（AVEVA 官方文件截圖，僅供內部教學）*

設定完可直接按 OK，或先 **Save Settings** 存入資料庫物件；**Default Settings** 可還原預設。主要參數整理：

| 參數 | 作用 | 重點 |
|---|---|---|
| Type of Analysis | Global、Local、Detailed、Fine | 決定網格粗細、使用不同參數集；部分過小的板架會被略過，系統產生清單檔列出被略過者 |
| Intended Element Size | 預期元素尺寸 | 同時控制曲面、孔洞與板架邊界以直線逼近的程度；預網格元素邊長不一定等於此值 |
| Ignore Panel Components | 依面積或平均邊長忽略零件 | 各零件頁籤（Panel、Pillar、Stiffener、Flange、Hole、Notch、Cutout、Doubling、Bracket、Swage、Seam） |
| Finite Element Type | 決定 shell／beam／truss 使用 | 官方提醒：全域模型中肋板可建為 beam，細部模型可能需要腹板與面板都用 shell；元素型式對 FEA 的規模與時間影響很大 |
| Stiffeners | Lumped beams、Beam、Shell and truss | Beam 可為 offset 或 hybrid；Shell and truss 是腹板用 shell、面板用 truss |
| Effective Width Factor | 帶板有效寬度，預設 40（倍腹板厚） | 只在 **Hybrid beams** 時有效；**Offset beams** 時自動設 0 且不可改 |
| Lumped Beams | 在主要構件相接處把加強材集中 | 太小的加強材在理想化就被排除，其餘在 FE 建模時 lump；用於全域模型保持粗網格 |
| Swages | 波紋 | 全域模型不建出波紋，板以**正交異向**材料的 shell 表示；局部模型用 shell 加 beam；細部分析需照實建模 |
| Holes | 孔洞 | 見 25.11.4 |
| Unit System | 單位換算 | 換算係數與理想化區塊一起存放，並寫入 APDL 檔供使用者知悉；ANSYS 本身不再做換算 |

**Connect Ends Along/perp**：理想化時，加強材端點若離「與其他零件交點」小於容許值，就吸附到交點。Along 沿加強材定義線交截；perp 則以端點垂直於加強材的線交截。超出容許值者不在理想化處理，而在 FE 建模階段延伸加強材並**切分**所屬 shell 元素。

**功能描述碼（Functional Codes）**：板架建立時的功能描述有特殊意義，會決定套用的理想化選項。

| 代碼 | 意義 | 備註 |
|---|---|---|
| 9901 | Bracket | |
| 9902 | Flange | |
| 9905 | Girder／Web frame | 板形需接近矩形且單一限制上有單一折邊；其餘限制（除與折邊相鄰的兩個之外）形成 beam 軌跡 |
| 9906 | Transition girder（拱形甲板） | |
| 9907 | Stiffener | |

沒使用這些功能描述，例如兩片板組成的肋板會被當作一般板架，兩片都理想化成 shell，**不會**套用 girder 專用選項。

> **專業提醒：** 在板架建立階段就決定好功能描述，比事後補救容易。若你們公司另有板架命名或功能描述規範，需與上述特殊代碼協調，否則 girder 會被當一般板處理，分析結果偏離設計意圖。

### 25.11.4 孔洞（Holes）規則

孔洞依大小分流處理：

1. 夠小的孔在理想化步驟就被移除。
2. 面積大於預期元素尺寸，或與接縫相交的孔，會作為**自由邊（free edge）**併入板中。
3. 其餘的孔會造成所在 shell 元素的**厚度折減**，有兩個控制參數：絕對最小厚度與剩餘材料最小百分比。折減後低於任一值，該 shell 元素就**從模型移除**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕孔洞與 shell 元素的尺寸示例：元素 1000×500，孔 600×400

*圖 25-9　孔洞折減範例。（AVEVA 官方文件截圖，僅供內部教學）*

官方的算例：在孔的主方向，元素寬 1000、孔 600，剩 400，比例 0.4，高於預設 0.25；但垂直方向元素寬 500、孔 400，剩 100，比例 0.2，低於下限，所以該元素被移除。**任一方向過弱就移除。**

孔的圓角在 FE 模型中一律變成直線段；元素尺寸夠小時看起來像圓，放大才看得到線段。理想化板架中則保留圓角。

### 25.11.5 執行理想化

按 OK 執行。若過程有錯誤會通知，官方要求**仔細查證**，因為錯誤的幾何可能導致後續 FE 建模產生不可預期的結果。**重新理想化同一區塊前，必須先刪除舊模型**：到 FE geometry 對話框 Analysis > Create FE Model，在樹中選區塊，右鍵 Delete，確認。

## 25.12 第二步：建立 FE 模型

理想化區塊完成後才能建 FE 模型。轉換規則：

| 理想化後的零件 | FE 元素 |
|---|---|
| 板面（板、肘板） | Shell 元素 |
| 加強材、支柱 | Beam 元素 |
| 折邊 | Truss 元素 |

理想的 shell 元素：**拓撲上相連、盡量四邊形、角度在限制內、扭曲（warping）在限制內**。曲面上常需要三角形元素。

### 25.12.1 先決：模型要有封閉邊界

平面板架與船殼、甲板等曲面的拓撲連接，決定了曲面哪些部分納入 FE 模型。FE Modeller 會計算這些板架軌跡曲線的邊界盒，用主平面切出交線，形成邊界多邊形，再以殼縱材、接縫等曲線細分。因為曲面形狀變化大，自動找邊界不一定成功，官方建議：

- 至少準備一個視圖，建立或選取接縫或殼曲線，形成封閉邊界多邊形；
- 曲線交點與 FE 模型邊界盒的距離**不得超過 5 倍元素尺寸**；
- 左舷與右舷分開處理，模型跨過中心線時，中心線附近也需要一條曲線。

### 25.12.2 FE Model Options

> 〔公開版未收錄：AVEVA 官方產品截圖〕FE Model 對話框：選取區塊、Mode、各項前處理選項與影像選項

*圖 25-10　FE Model 對話框。Mode 選擇建立或修改，下方為整理網格的選項與 FE 影像輸出。（AVEVA 官方文件截圖，僅供內部教學）*

| 選項 | 說明 | 預設（圖中值） |
|---|---|---|
| Create from Idealized Model | 區塊中尚無 FE 幾何時必選；已有時可用不同設定整個重建 | — |
| Modify Existing | 區塊已有 FE 幾何時，不重建、只套用下列選項調整 | — |
| Remove Transition Steps Smaller than | 處理斜板與平板的連接處（如拱形甲板）；小於容許值的階差忽略；否則於元素邊用 truss 理想化，過渡處的 girder 須有特殊功能碼 | 100 mm |
| Connect Adjacent Geometry | 合併容許值內的重合點與線：點對點、點對線吸附、線與線相交或合併、面與面連接 | 容許 0.5 mm |
| Combine Shell Elements | 避免小元素：短於「Max Distance Factor × 元素尺寸」的線被刪除並合併端點 | 0.3 倍 |
| Divide Shell Elements | 精煉過程，為滿足 FEA 軟體限制（點數、角度等），作用於**所有** shell 元素 | 見下 |
| Unwarp Shell Elements | 控制板面扭曲，沿連接邊界點的線分割扭曲元素 | 由 Divide 參數控制 |

**Combine 與 Divide 的互相約束**：Max Distance Factor 必須小於 Min Line Length Factor，否則精煉階段產生的線可能被刪除。

**Divide Shell Elements 的準則**（圖中值）：

| 準則 | 意義 | 圖中值 |
|---|---|---|
| Max number of Edges | 一個面最多邊數；一般偏好四邊形 | 4 |
| Max Face Warping Factor | 邊高度偏差 ÷ 面積平方根 | 0.1 |
| Max Thickness Warping Factor | 邊高度偏差 ÷ 平均元素厚度 | 1 |
| Min Line Length Factor | 精煉時新線不短於此倍元素尺寸 | 0.4 |
| Max Angle Deviation | 相鄰線與直角的偏差 | 45 度 |

準則互有取捨：消除扭曲的要求**強於**角度準則（扭曲的元素無法使用，尖角只是不理想），所以結果可能仍有元素的邊數超過 Max number of Edges。官方特別提醒：**ANSYS Mechanical APDL 一個面最多 18 個點**。

> **專業提醒：** 這些係數官方稱為「第一次猜測值」，可調整。實務上建議用**一個代表性區塊**反覆調整（Modify Existing 不必整個重來），穩定後存為公司標準，再套用到其他區塊。

## 25.13 檢查：FE Image、Statistics、Check

FE 模型可在 AVEVA Marine 內先檢查再輸出。**FE Image** 是把結果以折線畫出的物件，可從 Design Explorer 拖放顯示，或插入模型時勾選 FE Image 準則。命名規則：

- `_FGS<區塊名>`：Shell Element Image，所有 shell 多邊形（無著色）。
- `_FGB<區塊名>`、`_FGT<區塊名>`：beam 與 truss 折線。以上三種在 FE Model 選項中勾選。
- 以下由理想化區塊右鍵選單建立：`_FGA` Angle Image（角度偏差小於設定值處）、`_FGF` Free Edge Image（只屬於一個面的線）、`_FGL` Line Image（全部的線）、`_FGP` Point Image（全部的點，與輸出一致）；Element Image 則一次建立 shell、beam、truss。

沒有對應元素時，該物件不會被建立（例如模型沒有 truss 就沒有 `_FGT...`）。**所有影像不需重建整個 FE 幾何即可建立。**

> 〔公開版未收錄：AVEVA 官方產品截圖〕Shell 影像範例：以簡單封閉折線畫出的 shell 元素網格

*圖 25-11　Shell Element Image 範例。（AVEVA 官方文件截圖，僅供內部教學）*

Free Edge Image 特別好用：自由邊本來就會出現在板架邊界未連到其他物件處或孔洞處，**但出現在別的地方，可能代表模型零件之間漏了連接**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Free Edge Image 範例：自由邊以橘色線疊在 shell 影像上

*圖 25-12　Free Edge Image 疊加在 shell 影像上，橘色線為只屬於一個面的邊。（AVEVA 官方文件截圖，僅供內部教學）*

Angle Image 則標示出過小角度處；曲面部分難以完全避免，因為要用三角形把扭曲的元素拆開。

右鍵選單的其他功能：

| 功能 | 用途 |
|---|---|
| Statistics | 顯示預網格資料量 |
| Check | 檢查 FE 模型錯誤（如相交或重合的線），偏進階除錯 |
| Dump | 把所選項目的詳細資訊寫到主控台，視層級可為單一多邊形或整個板架／區塊的幾何與屬性 |
| Delete | 刪除所選理想化區塊與所有相關物件 |
| Delete Images | 只刪除該區塊的影像 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕FE Model Statistics：Hull Log 視窗列出分析類型、元素尺寸與各元素數量

*圖 25-13　Statistics 範例：Local 分析、元素尺寸 400，約 9,234 個 surface 元素、467 個 beam、487 個 truss、10,503 個點。（AVEVA 官方文件截圖，僅供內部教學）*

Statistics 會列出邊界盒、分析類型與元素尺寸、物件數、折線數（含大量只用來構成曲面的殼曲線與軌跡曲線）、surface／beam／truss 元素數，以及線與點總數（輸出時一併寫出）。

> **專業提醒：** 輸出前，用 Statistics 的元素數粗略判斷模型規模是否適合外部軟體與授權限制。元素數比預期大一個數量級，多半是元素尺寸設太小或沒有忽略小零件。

## 25.14 輸出與外部軟體交換

### 25.14.1 五種輸出方式

| 輸出 | 格式 | 官方給出的重點 |
|---|---|---|
| ANSYS APDL | ANSYS 命令檔 | 可在 ANSYS Mechanical APDL（Classic）處理，建立幾何或節點與元素、屬性、材料 |
| Patran PCL | Patran session 檔 | 宜在 Patran 以 batch 模式播放，產生資料庫檔 |
| Nastran BDF | Nastran Bulk Data 檔 | Beam 屬性可輸出為 `PBEAML`（尺寸）或 `PBEAM`（積分特性） |
| Sesam FEM | Sesam Input Interface 檔 | 含節點、元素、材料與元素屬性 |
| MAESTRO MNF | MNF 檔 | 供 MAESTRO 使用 |

另外，**Hull Steel XML Export** 可選擇理想化區塊匯出，加選項時一併匯出對應的 FE 模型：包含節點、shell／beam／truss 元素與屬性，以及**對原船模型板架的參考**。

### 25.14.2 ANSYS 與 Patran 的細節

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create ANSYS Input File 對話框：選區塊、Geometry 或 Mesh、元素型別

*圖 25-14　匯出 ANSYS APDL 的對話框：選含 FE 幾何的區塊，選 Geometry 或 Mesh 與 ANSYS 元素型別。（AVEVA 官方文件截圖，僅供內部教學）*

| 設定 | 元素型別（官方給出） |
|---|---|
| 預設（New Types，不含中間節點） | `SHELL181`、`BEAM188`、`LINK180` |
| New Types 含中間節點 | `SHELL281`、`BEAM189`、`LINK180` |
| Old Types | `SHELL63`、`BEAM44`、`LINK8`，**不建議**，因為 ANSYS 已不再文件化 |

平面與曲面部分可選不同型別，但會影響在 ANSYS 內的網格順序（詳見 ANSYS 說明）。Patran 輸出的設定為：分析碼 `MSC.Nastran`、分析類型 Structural，元素為 Shell（Thin、Homogenous、Standard Formulation）、Beam（General Section，CBEAM）、Rod（General Section、Standard Formulation）。

### 25.14.3 材料資料

**AVEVA Marine 不明確管理材料等級，但 FEA 一定需要。** 做法：把材料性質寫在 XML 檔，在 Structural Design 選單用 **XML > Import > Hull Steel Import** 匯入，建立一個材料物件，之後輸出時就用它提供外部軟體材料資料。官方範例（節錄）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Ship xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="M:\xml\schema\Export\HullPanel.xsd" Version="1.3">
  <Material Grade="A" Density="7840" YoungsModulus="206E3" PoissonRatio="0.3"
            YieldStress="220" UltimateStress="360"/>
  <Material Grade="A32" Density="7790" YoungsModulus="205E3" PoissonRatio="0.3"
            YieldStress="320" UltimateStress="510" ThermalExpansionCoefficient="0.011"/>
</Ship>
```

欄位為 `Grade`、`Density`、`YoungsModulus`、`PoissonRatio`、`YieldStress`、`UltimateStress`，以及選用的 `ThermalExpansionCoefficient`。單位未在官方頁面說明〔待核對：從數值（`YoungsModulus="206E3"`、`Density="7840"`）看，疑為 MPa 與 kg/m³，但請以所用 schema 為準〕。

> **專業提醒：** 材料等級要和板架上的材料等級名稱**逐字相符**，否則輸出時找不到性質。建議由公司材料表產生這份 XML，而非手工維護，並隨船級規則版本管控。

## 25.15 二次開發者怎麼接（FE Model）

| 接點 | 依據 | 說明 |
|---|---|---|
| 材料 XML 匯入 | 官方給出欄位與匯入選單 | 用腳本由材料資料庫產生；schema 路徑 `...\xml\schema\Export\HullPanel.xsd` 為官方範例 |
| 命令建立 `FEMWLD` | 官方給出 `NEW FEMWLD /<name> DB <dbname>` | 納入專案初始化腳本 |
| 五種輸出檔 | 官方列出格式與主要設定 | 以腳本接 ANSYS／Nastran 等批次流程；APDL 與 PCL 由外部軟體批次執行 |
| Hull Steel XML（含 FE 模型） | 官方說明內容概要與可參照原模型板架 | 結構細節〔待核對：官方頁面未給 XML 元素名稱〕 |
| FE Image 物件名稱 | 官方列出 `_FGS`、`_FGB` 等命名 | 可用 PML 依命名規則尋找並檢查 |
| 以命令列／PML 驅動理想化與輸出 | 官方未給命令 | 〔待核對〕；目前有依據的操作皆為圖形介面 |
| 批次化大量區塊 | 官方未涵蓋 | 若要自動化，建議先確認有無對應 PML 物件或命令，再評估外部自動化方式〔待核對〕 |
| 外部分析結果回寫 | 官方未涵蓋 | 本章不推測 |

### 25.15.1 FE 模型常見錯誤

- **沒建 `FEMWLD`**：無法執行理想化。
- **重理想化前沒刪舊區塊**，或把板架加入已有其理想化版本的區塊：重複或衝突。
- **功能描述碼缺失**：girder 被當一般板處理。
- **曲面邊界不封閉**：曲面部分建不起來；需建視圖並建立接縫或殼曲線。
- **元素尺寸太小**：模型過大、計算極慢；先用 Statistics 評估。
- **單位不一致或材料名稱對不上**：外部結果量級錯、屬性缺漏；設定 Unit System，材料 XML 與板架材料逐字相符。
- **忽略非預期的自由邊**：外部軟體出現不連續；用 Free Edge Image 檢查。

## 25.16 本章小結

1. **空間由邊界切出**：Envelope + Dividing Boundary + 布林運算；World 類型鎖定並決定屬性與可用功能。
2. **用途控制檔是介面契約**：`PURP`、`TYPE_SEL` 與 `/DENS` 會進計算。
3. **取結構要即時算**：Get Structure within 的暫時模型不存檔，PaintArea、WCOG、Weld 要在同一 session 完成；估算（`SPME*`）與計算（`SPMC*`）成對比較。
4. **報表可客製**：兩支 `.pmlfnc` 官方明講可修改，是最有依據的二次開發接點。
5. **FE 分兩步**：先理想化（中面、簡化），再建 FE（shell／beam／truss）並整理網格；孔洞與加強材有明確規則。
6. **先檢查再輸出**：FE Image、Free Edge、Statistics。
7. **官方未涵蓋處標〔待核對〕**：載重、邊界條件、XML 細節與自動化命令，不要憑印象寫進工具。

## 25.17 練習題與自我檢核

**練習題**

1. 建立一個 Compartment 類型的 World，用兩道橫艙壁與一道縱艙壁切分一個 Envelope。切完後把兩個相鄰艙合併，檢查新空間取得哪個空間的屬性，並用 Copy Attributes 補齊。
2. 寫一份用途控制檔，定義兩種水密液貨用途（密度各自不同）與一種機艙用途；編譯後在 Attributes 中指定給空間，並確認對話框顯示的值。
3. 對一個 Layout 佈置執行 Get Structure within，依序做 WCOG 與 PaintArea，說明為何不能先結束 session 再算。
4. 依 25.11.4 的算例，自編一組孔與元素尺寸，判斷該元素是否被移除。
5. 為 Local 分析選擇元素尺寸，建立理想化區塊與 FE 模型，用 Statistics 記錄元素數，再把尺寸減半重做，觀察元素數成長。
6. 用 Free Edge Image 檢查一個板架模型，列出哪些自由邊屬正常（邊界、孔），哪些可能代表遺漏連接；再寫一份材料 XML 並說明 `PBEAML` 與 `PBEAM` 的差別。

**自我檢核**：我能說出六種佈置類型與各自可儲存的計算結果；知道 Get Structure within 的結果不永久儲存；知道 `NEW SPMSW` 與 `NEW FEMWLD` 的用途；能解釋孔洞為何讓 shell 元素被移除；清楚哪些二次開發接點有官方依據、哪些待核對。

## 25.18 〔待核對〕項目彙整

| # | 項目 | 原因 |
|---|---|---|
| 1 | FE 模型功能所在選單的確切位置 | 官方頁面只提到 Analysis > Create FE Model 與 Structural Design |
| 2 | 塗裝區 Face Code 的設定來源與格式 | 官方只指向 Surface Treatment Selection Tables |
| 3 | 分佈式屬性（Distributed Attributes）與 bound attribute 的設定位置 | 官方只說明須先設定 |
| 4 | Space XML Input 的 XML 結構 | 官方未給 |
| 5 | Calculation Geometry 輸出的 XML 結構與 calc 模組版本 | 官方未給 |
| 6 | 空間與設備、管路位置的比對功能 | 官方未涵蓋 |
| 7 | 水艙特性表（測深、容積、自由液面）是否由本模組產生 | 官方只說輸出幾何給水靜力模組 |
| 8 | 空間資料庫元素的完整型別階層與 `SPM*` 屬性可否由 .NET 直接讀取 | 官方只列屬性名 |
| 9 | FE 輸出中是否攜帶載重與邊界條件 | 官方只說輸出節點、元素、屬性與材料 |
| 10 | Hull Steel XML（含 FE 部分）的元素名稱與 schema | 官方只說內容概要 |
| 11 | 材料 XML 的單位 | 官方範例未註明單位 |
| 12 | 理想化與輸出是否有命令列或 PML 介面 | 官方只描述圖形介面 |
| 13 | 空間範圍與 FE 範圍是否可自動連動 | 官方未說明 |

## 25.19 取材與延伸

- AVEVA Marine 12.1 官方離線文件：**Space Management**（Some Design Scenarios、Project Set-up、Basic Concepts、Functions Overview，含 Project、Functional Structure、Space Management 三個選單與右鍵選單）。
- AVEVA Marine 12.1 官方離線文件：**Finite Element Model**（Idealized Model、FE Model Creation、FE Model Output、Material Qualities）。
- 本課程相關章節：[第 5 章](ch05_hull_modelling_zh-TW.reading.html)、[第 6 章](ch06_hull_production_zh-TW.reading.html)、[第 15 章](ch15_hull_vitesse_zh-TW.reading.html)、[第 19 章](ch19_loading_computer_zh-TW.reading.html)、[第 20 章](ch20_system_administration_zh-TW.reading.html)。
