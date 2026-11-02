# 第 6 章　船體概念與基礎：Product Information Model、模型物件、拓撲與命名

> 第 9 章教你「把板架建出來」，第 13、14 章逐項講平面與曲面船體細部功能。這一章講這些功能共用的**語彙與規則**：Product Information Model（產品資訊模型，PIM）、設計模型與零件的差別、Block／Panel／Part 結構、Data Bank、拓撲（Topology）、命名、座標與相對位置，以及可批次進出船體資料的 XML 介面。
>
> 對二次開發者特別重要：名稱規則決定能不能從字串推出所屬板架；拓撲決定重建順序；XML 介面（TXSUR、TXHBD、TXHSTL、TXHCM）是官方提供、不碰內部資料庫的批次進出口。
>
> **資料可信度：** 依 AVEVA Marine 12.1 離線文件 Hull Concepts（241 頁）與 Hull Basic Features and Concepts（95 頁）撰寫，兩模組 338 頁皆已讀取（TIL 與英制頁僅摘要，見 附錄 E）。官方為機器翻譯，本章改用台灣慣用譯名並保留英文；環境變數、資料型別號碼、XML 元素與屬性名稱照抄原文；文件未說明者標〔待核對〕。XML 部分官方文字提及的版本（M3SP4）較舊，12.1 實際支援範圍以安裝的 schema 為準。

## 6.1 學習目標

讀完本章，你應該能夠：

1. 說明 PIM、Hull Product Model、Design Model 與 Hull Parts 的關係，以及「隱式」與「標稱尺寸」的意義。
2. 畫出 Hull Structure → Block → Panel → Part，並說明 Plane Panel 與 Curved Panel 的差別。
3. 區分 Design View、Assembly View 與 Shell Profile 的 Functional View。
4. 列出船體 Data Bank 與環境變數（`SB_OGDB`、`SB_CGDB`、`SB_PLDB` 等）及 object code 1 的分段。
5. 說明拓撲的兩種參照、在 Recreate／Copy／Move 的作用，以及「好拓撲」的原則。
6. 套用命名規則：Ship Letters、Explicit／Derived／Composed、24 字元上限、板架與零件名稱格式、縱橫骨編號。
7. 以 `FR`、`LP` 寫出相對位置，並寫出座標表輸入檔。
8. 說明 Run Mode Control 三層級及對稱、板厚補償、型材參考點的環境變數。
9. 讀懂 Functional Description 的編碼區段與四種 XML 格式的用途與關鍵元素。
10. 說明 Project Material 的限制，並能查 Marine Dictionary 重點詞條。

## 6.2 Hull Basics 與 Marine Concepts

| 主題 | 官方重點 | 實務提醒 |
|---|---|---|
| 錯誤處理 | 錯誤分三類：作業系統 Run-time、基礎程序套件、程式自身訊息。開始功能表的 **Error Lookup** 需先選錯誤前綴（如 `FFIX=`、`QERROR=`、`SSP ERROR=`、`SYSTEM ERROR=`）再輸入代碼；需 `SBB_ERRMESS` 指向 `SB_SYSTEM` 的 `sb_error_codes.txt` | Hull 的部分錯誤碼直接顯示給使用者；程式專屬錯誤固定在 1000–1100，說明在各程式文件；前綴選錯則訊息錯 |
| 幾何 | 基本元素是 segment（線段或帶 amplitude vector 的圓弧），連續 segment 成 contour | 與 XML 的幾何表示一致 |
| TIL | Interpretative Language：識別字 1–32 字元、不分大小寫、`!` 註解、`;` 結束敘述 | Hull 輸入檔語法基礎 |
| 英制 | 資料庫一律公制；輸入輸出可由 `SB_LINEAR_MEASURE_UNIT`、`SB_COORDINATE_UNIT` 等環境變數改為英制 | 英制值須以數字開頭（`6I` 合法） |

> **專業提醒：** 「概念頁」中的設計決策（幾何不存、只存技術資料與關聯；設計與生產分開）直接決定你能讀到什麼。設計模型裡找不到板的完整幾何不是 bug。

## 6.3 Product Information Model

| 名稱 | 官方定義 |
|---|---|
| PIM | 構成最終產品的所有實體零件及其關聯的完整資訊，涵蓋船體、舾裝、組立規劃等所有應用 |
| Hull Product Model | PIM 中由 Hull 建立與發展的部分，不含組立與焊接規劃資訊 |
| Design Model | 設計活動的直接結果，依 Hull Design Structure 組織；**隱式**（零件不展開完整幾何）且存**標稱尺寸**（斜切、收縮補償等生產修改尚未套用）。不嚴格時「Hull Model」即指它 |
| Hull Parts | 由「自動零件產生」依規則（打標、斜切、收縮補償）從隱式模型取出（released）的板（由板材）與型材（由棒材） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕同一個 PIM 提供設計與生產兩種觀點。

*圖 6-1　設計與生產共用同一個 PIM。（AVEVA 官方文件截圖，僅供內部教學）*

PIM 的特性（Marine Concepts）：

| 特性 | 內容 |
|---|---|
| 物件導向、不存幾何 | 幾何由技術資料需要時推導；顯示用 Solids 與 Light Solids（以標準表示取代邊界表示的簡化實體）。改設計是改技術資料，不是改圖形 |
| 多人並行、單一資料庫容納整船 | 設計變更即時可見；可依 Block、系統、位置等條件跨專案取資料 |
| 逐階段精進 | 早期輸入、後期擴充；船體與舾裝同一 PIM，建模與繪圖緊密連結 |
| 關聯性（Associativity） | 存技術資料與拓撲而非純數值幾何；船形改了但關聯不變，結構幾何可由舊資料快速重建 |
| 由技術資料推導資訊 | 焊接量由「加強材焊在鄰板」規則推得；肘板由尺寸與使用規則自動算出完整幾何，設計者只指定 scantling 與材質 |
| 多重階層 | 同一物件可同時被設計階層與生產階層參照，可在設計後才依建造策略分組 |

官方名詞：**Surface**（曲面，劃分艙區的主要結構如主甲板、內底）、**Compartment**（艙區，由封閉邊界曲面界定）、**Block**（可整塊吊裝的實體區域）、**Module**（為組裝目的歸在一起的區域）、**Assembly**（在某階段接合的零件或次組立）。

PIM 內有三棵樹：

| 結構 | 內容 |
|---|---|
| Initial Design Objects | 曲面（船殼、甲板、縱向艙壁、橫向艙壁四種用途）與艙區；曲面可再分板架與簡化結構特徵 |
| Hull Objects | 船體分 Block，Block 分 Panel，Panel 由 Plate、Stiffener、Seam、Notch、Bracket、Flange 等組成；整船由互不重疊、無間隙的 Block 構成（圖 6-2） |
| Production Assembly Hierarchy | 船廠自訂的組立階層，層數無實質限制，不隱含組立順序或時間（圖 6-4） |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull Data Structure：Ship Model → Block → Panel → 邊界、Seams、Plates、Stiffeners、Holes、Cutouts、Notches、Brackets。

*圖 6-2　船體資料結構概觀。（AVEVA 官方文件截圖，僅供內部教學）*

船體主要流程：建立船形與船體標準後，曲面與平面兩個建模模組產生 Hull Model 與圖面；**Parts Generation** 拆成 Plate Parts 與 Profile Parts，再套料、輸出切割機或機器人。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull 模組與功能流程：圓形是資料，方框是功能。

*圖 6-3　從船形、建模、零件產生、套料到切割。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Production Assembly 結構：Assembly 可含船體、管路、電纜物件。

*圖 6-4　生產組立階層。（AVEVA 官方文件截圖，僅供內部教學）*

**TDM（Data Management）** 內建於核心，管理狀態、存取控制、圖面修訂與模型版本，可介接商用 PDM。**技術實作：** PIM 邏輯上分成多個 Data Bank（模型物件的永久儲存單位），同專案的 Data Bank 通常集中在一個目錄，專有的物件導向實作，自動保持不碎片化。

## 6.4 模型物件與 Parts

| 物件 | 官方描述 |
|---|---|
| Block | **不等於**組立節點；是「受地理限制的板架容器」，用以建立設計結構 |
| Panel | 建立船體結構的中心建模單元；Marine 的 Panel 比一般造船術語寬，可小到單板肘板、大到含數百零件的整層甲板。平面者 Plane Panel，任意形狀者 Curved Panel（即使碰巧是平的） |
| RSO（Reference Surface Object） | 代表主要內部結構，通常在 Initial Design 產生，Structural Design 可有限度產生；用於賦予鋼材屬性並自動產生大型板架，或當手動板架的穩定位置與邊界參照 |

Plane Panel 由邊界限定，各邊界負責外輪廓一段稱 **limit**，limit 間連接點為 **corner**；一般板位於 **mould plane**，板架有局部座標系 uvw（uv 在 mould plane）。

| 詞彙 | 定義（整理） |
|---|---|
| Bracket | 通常最多一塊板，可加加強與角隅 notch；分 type standard bracket 與 panel bracket |
| Clip | 型材 cutout 中的小板片（lug、collar） |
| Hole／Cutout／Notch | 板內封閉開口／供型材穿過的板緣開口（slot、scallop）／角隅或邊緣標準化小開口（rat hole） |
| Profile | stiffener、flange、pillar 的通稱，一律當棒材製造；Flange 含焊接翼板（face plate）與折邊（folded flange，板折彎而成，非真正型材）；Pillar 為只在兩端焊接的自由型材 |
| Swedging／Excess／Quality | 小波紋取代加強材／多留料（overmaterial、green material）／材質等級（grade） |

產生型材的三個關鍵屬性：**profile type**、**endcut type**、**connection code**。曲面中的加強材稱 **shell stiffener**，分兩層：**shell profile**（以編號識別、沿全船收集多個零件，本身只存參照）與 shell stiffener（實際存一支型材）；沿船長者為 **longitudinal**，主要沿橫向者為 **transversal**。

**Parts：** Part 是最終需製造的每一件。**AVEVA Marine name** 是 Data Bank 內部名稱；**part name** 是車間標在零件上的生產名，詢問時才由屬性組成；其中區分同組立內各零件的一段稱 **position number**（可為字串）。例：`A2N-C3-4` 中 `A2N`、`C3` 為組立名，`4` 為位置號。型材長度分 **moulded length**（設計模型沿 trace 兩端點）與 **used length**（所需棒材最短長度，已計端切、bevel gap、收縮補償）。

**殼板展開**（plate development）把曲面殼板反向成形以便從平板切出，**不等於** shell expansion（產生外板展開圖）。方法是切成條帶並三角化，由中性面（base plane，交線稱 base line）往兩向攤平，通常算出第一、第二 roll axis。檢查用 bending template；殼板在 jig（胎架）上組成曲面板架。另有 **Dotori**（自動選角焊 bevel 型）、**Genauigkeit**（刻度標記）、**Generic format**（零件中性 ASCII 格式）。

## 6.5 Model Structures：設計結構與組立結構

不同階段看法不同：初期看主要尺度與艙劃分，基本設計看甲板艙壁的功能性質，生產看組立，詳細設計則是功能與組立的混合，目的是轉成生產零件同時**保護設計意圖**。

| 視圖 | 導向與建立 | 內容 |
|---|---|---|
| Design View | 地理導向；完全在 Hull／Structural Design 建立，任何應用可讀 | 只含船體物件 |
| Assembly View | 生產導向；通常在 Assembly Planning 建立 | 含船體與舾裝等，另有組立專屬資訊（如組立時的方位） |
| Functional View | 只針對 shell profile；**必有** | 以縱骨編號等跨全船參照，不受位置影響 |

組立模型是「對映到設計模型上」建立的；所有船體零件須先進入設計模型，才能被組立結構參照（舾裝鋼料在 Structure 應用建模）。殼板型材同時屬於設計、組立、縱橫向三個結構。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Hull model structure：Hull Structure → Block → Panel → Part；Panel 上的圓圈箭頭表示零件隱式存於板架內。

*圖 6-5　Hull 設計結構（三到四層）。（AVEVA 官方文件截圖，僅供內部教學）*

| 層 | 說明 |
|---|---|
| Hull Structure Object | 進入設計結構的入口，只存對所有 Block 的參照；由 `inithull` 與 Structure Reference（`Structref`）同時建立，Block 增刪改時自動更新；設計者不直接接觸 |
| Block Object | 不含模型資訊，只存外包盒位置；由 `inithull` 或 Structural Design 建立，板架增刪改時自動更新 |
| Panel | Data Bank 存放模型資訊的層級 |
| Part | 平面板架零件**隱式存於板架內**；僅 panel bracket 單獨存放 |

Block 的要點：建立時須定義粗略範圍（box），所屬板架最好完全在盒內，不同 Block 的盒可重疊；同一 Block 可含兩舷板架，限於舷側的 Block 只需定義左舷範圍，右舷有效的板架經中心線鏡射後在盒內也屬於它，跨中心線的 Block 要定義真實範圍。切分 Block 的考量：配合階段、便於分派設計者並使拓撲參照多留在 Block 內、搜尋效能；全模型對所有人始終可用，跨 Block 參照沒有問題。

**Plane Panel** 必須：一般板在同一平面；能形成封閉外輪廓（所以不適合把複雜腹板環做成單一板架）。它是容器，含多為隱式的零件及產生零件所需的特徵（外輪廓、seam、板厚與材質、折邊、bevel、型材特性、hole／notch／cutout、excess、swedging、收縮補償）。隱式板**只明確存板厚與材質**，幾何參照外輪廓與限制它的 seam；取出時特徵才影響幾何，並自動為焊在其上的零件加標記線。**對稱：** 板架可建在半邊但兩舷有效，仍可個別取兩舷零件；可描述在任一舷。

| 特殊板架 | 官方描述 |
|---|---|
| Panel Bracket | 標準肘板直接建在板架上；太特殊者建成小板架。**不能**直接屬於 Block，須連到一或多個板架，是平面板架下唯一單獨存放的零件 |
| Knuckled Panel | 含多平面（含波紋板）：每個平面建成子板架（sub-panel），收集成折角主板架並彼此連接；只有主板架插入結構 |
| Outfitting Steel Panel | 舾裝鋼料經 PPM（Production Preparation Model）轉入，每塊板與加強材各有自己的 transformation；**不由** Statement Wizard 處理，只能在 Outfitting Steel 應用或經 Hull schema 修改 |

取出零件雖不算模型物件，但板架與零件可互相找到；某些屬性**從不複製**到取出零件而是每次經模型取得，修改後不必重取。

**Curved Panel** 與平面板架同樣登記在 Block，但是**純容器**：只收集先前已獨立產生的殼板與殼型材，不能經板架為零件加屬性，對零件永遠是外部參照；用於生產輸出、胎架計算等。

**設計與組立的對映**通常在 Assembly Planning 完成，以名稱建立組立樹節點與設計零件間的**雙向指標**（指向隱式零件，不是取出零件），且總在零件層級：同一板架的零件可進不同層級組立，同一組立可含不同 Block 板架的零件。

> 〔公開版未收錄：AVEVA 官方產品截圖〕設計結構與組立結構之間任意的零件對映。

*圖 6-6　設計結構到組立結構的對映。（AVEVA 官方文件截圖，僅供內部教學）*

> **常見錯誤：** 把 Block 當生產分段算重量或工時。官方明說 Block 是設計用地理容器，生產分段以組立結構為準；同一零件在兩邊各有一個名稱（6.8），報表混用最易對帳錯誤。

## 6.6 Object Types 與 Data Banks

船體資訊以兩種物件型別存放：**CAT**（Contour And Table）物件存除圖面外所有船體物件，內部結構依型別而異，以 **object code 1（data type）** 識別（由 AVEVA 集中註冊）；**Picture** 物件存視圖與圖面，各應用（尤其 Drafting）通用，故船體與其他應用資訊可合併成一張圖。

Data Bank 名稱由環境變數（logical name）決定，程式引用變數而非檔名：

| Data Bank | 環境變數 | 內容 |
|---|---|---|
| Form | `SB_CGDB` | 型線（曲面、hull curves、seams／butts） |
| Structure | `SB_OGDB` | 船體模型 |
| Plate／Profile | `SB_PLDB`／`SBH_PROFDB` | 取出、可生產的板／型材零件 |
| Nesting／Nesting standard／Profile nesting | `SB_NPL`／`SB_NSTD`／`SBH_NEST_PROFDB` | 套料板與切割草圖／標準板與掛鉤／套料型材 |
| Drawing／Picture／Receipt | `SB_PDB`／`SBD_PICT`／`SBH_RECEIPT` | 圖面／單獨存放的視圖／經 Production Program Interface 的收據圖 |
| Assembly／Topology／TID | `SB_ASSDB`／`SB_REFDB`／`SB_TID` | 組立資料／拓撲物件／曲面（RSO）與艙區 |
| Standard／Form（繪圖） | `SBD_STD`／`SBD_FORM` | 圖框等 |

另有 `SB_HREF`、`SB_SREF`（Hull／Structure Reference 物件名）、`SB_SHIP`（預設檔目錄）、`SB_SYSTEM`（系統檔，含 `xml` 子目錄）。

| Form Data Bank 的 data type | 說明 |
|---|---|
| 1／2／3／4／5／6／7／8 | Ship surface／Hull reference／座標表／座標界限表／Frame／Waterline／Buttock curves／Seams and Butts（另 1005–1007 為斜平面曲線，12、13、55 為任意曲線、標記參考線、任意平面） |

| Structure Data Bank 的 data type | 說明 |
|---|---|
| 50／51／52 | Structure reference／Hull Structure Object／Block |
| 9／10／11 | Longitudinal frame／Transversal frame／Shell stiffener |
| 58／59／60／61／70 | Endcut table／收縮補償／Swedging／Cutout 標準／Hull standard（命名、bevel、折邊等） |
| 100–499、700–999／500–599 | Plane panels／Curved panels |

曲面通常在 Hull 外（如 Initial Design）處理，Hull 呼叫 surface processing 模組取資訊，但資料庫中每個曲面須有名稱相符的物件，由 `inithull` 登記時建立。**Hull Reference** 記錄 Form Data Bank 物件的名稱與命名規則：船的特徵尺度、主船殼與甲板曲面的名稱與 suffix、frame／waterline／buttock 的 group name、座標表、seam／butt 的 group name 與 x、z 向界限表，以及**是否允許 Seam 與 Shell Profile 自由命名**；每個曲面另有選項決定 shell profile trace 與平面板架邊界是否依殼板厚調整。**Structure Reference** 記錄 ship letters、Hull Structure 物件名、縱橫骨 group name 與其 x 向延伸表（y、z 向表名加 `Y`、`Z`）、專案名稱。皆由 `inithull` 建立。

## 6.7 Topology（拓撲）

PIM 中物件間相依關係幾乎都以**參照**記錄，構成拓撲。Hull 中有兩種：**定義參照**（每個設計物件存其定義所需的物件，如定義板架邊界的曲面、曲線、板架，因此可用參照重新產生）與**相依參照**（「誰依賴我」，同一資訊從另一端看，存於拓撲物件，Data Bank `SB_REFDB`）。

| 原則 | 說明 |
|---|---|
| 用參照，不用座標 | 終止於甲板的艙壁，限制應是對該甲板的參照，其外輪廓才同時依賴甲板位置與板厚 |
| 避免循環參照 | 相連的兩層甲板不應互相參照邊界；兩者參照同一預定義平面，或一者用座標、另一者參照前者 |
| 以元件層級思考 | 艙壁邊界參照甲板、甲板加強材又參照艙壁加強材，看似循環，實際依賴的是不同元件，仍可排出重建順序 |

用途：**Topology** 功能高亮顯示定義與相依物件；**Planar/Panel/Recreate** 依拓撲推導順序重建被啟用的板架（有些板架可能先只部分產生，因依賴尚未重建者）；**Planar/Panel/Copy**、**Move** 以拓撲排序。**Planar/Model/Split STI** 等功能可能打亂板架內元件群順序，導致無法由 scheme 重建；但**儲存板架時**元件群會依正確順序排序並更新拓撲物件。

> **專業提醒：** 拓撲讓改動「傳得出去」，也讓錯誤傳得出去。改 Seam 或主甲板前先用 Topology 看相依物件（延續第 9 章 9.6）。

## 6.8 About Naming：名稱規則

**兩套名稱：** 同一模型、同一批零件，設計視圖與生產視圖的名稱不同。

| 名稱 | 特性 |
|---|---|
| AVEVA Marine name（設計名） | 零件一建立就給，設計者設定，內部與繪圖室用，**設定後固定** |
| Part name（生產名） | 分段與組立完成後才給，漆在零件上、用於生產清單；**動態**：詢問時才組成，規則或任一組成改變，下次就得新名稱 |

**通則：** 長度**不得超過 24 字元**（生產名無此限）；有效字元 `A–Z`、`0–9`、`.`、`-`、`_`；同一程式可能同時處理的物件須名稱唯一（官方舉例：圖面與 Block 可同名，但以該 Block 在該圖面產生視圖時會衝突，甚至損毀物件）。**Ship letters**（通常 1–2 字母）登記在 Structure Reference，加在模型物件名稱開頭，表明所屬專案（姊妹船可共用 Data Bank）及這是設計名；**系統不會自動加**，且使用與否是選擇性的。例子皆假設為 `AA`。

| 原則 | 說明與範例 |
|---|---|
| Explicit | 設計者任意選；建議板架名以所屬 Block 名開頭，建模時就不必另指定 Block |
| Derived | 取出零件時自動衍生，設計者無法影響：板架 `AA123-4` 的板零件為 `AA123-4-1S` 或 `-1P` |
| Composed | group name + 使用者給的編號（須小於 10000）：seam group `AAS` + 599 = `AAS599`；多曲面專案加一個字母的 surface suffix（定義在 Hull Reference，主船殼可不加）：`AASC123` |

| 物件 | 規則 |
|---|---|
| Hull Structure Object | 任意，建議 `AAHULLSTRUCT` |
| Block | 任意，但常是板架名前段，宜短（`AA123`） |
| Panel | 任意；建議「Block 名 + `-` + 序號」（`AA123-4`）；取零件時名稱會延伸，**不宜超過 16 字元** |
| Panel bracket／Knuckled 子板架 | 任意；建議含所屬板架名：`AA123-4B01`／`AA123-4K01` |
| Curved panel（暫時規則） | 後綴表示對稱：對稱者以數字結尾、`P` 左舷專屬、`S` 右舷專屬、`SP` 跨中心線；Block 名**不可含 `-`**（它是 Block 與板架名的分隔符） |
| RSO | Structural Design 中一律 `_RSO_` 開頭（未給則自動加），含前綴最長 25 字元 |

**平面板架零件**（板架 `AA123-4`、序號 9；各類零件在板架內各有序號，可有空洞）：

| 零件 | 兩舷共用 | 左舷（PS） | 右舷（SB）／跨中心線 |
|---|---|---|---|
| Plate | `AA123-4-9` | `…-9P` | `…-9S`（跨 CL：`…SP`） |
| Bracket | `AA123-4-9B` | `…-9BP` | `…-9BS` |
| Clip | `AA123-4/C9` | `…/C9P` | `…/C9S` |
| Stiffener／Flange／Pillar | `AA123-4/S9`、`/F9`、`/P9` | 加 `P` | 加 `S` |
| 肘板上的加強材／翼板 | `AA123-4/9/S1`、`/9/F1` | 加 `P` | 加 `S` |
| Doubling plate | `AA123-4-9D` | `…-9DP` | `…-9DS` |

對稱板架預設左右舷各存一份（`P`、`S`），也可只存一份。組合型材可拆腹板與翼板，名稱加 `W`、`F`（`AA123-4/S9PW`）。經 PLCM 產生板線 NC 的「組立零件」名為「板架名-最低層組立名」（`AA123-4-ABC`）。

**曲面板架零件**：殼板與殼型材先是結構 Data Bank 的獨立物件，執行 **Curved Part Generation**（`sf831d`）時才轉入板／型材 Data Bank。

| 位置 | 格式 |
|---|---|
| Shell stiffener（結構 Data Bank） | `<FreeName>-S<seq>[<symmetry>]`，對稱省略、左舷 `P`、右舷 `S`；例 `AA567-8-S25P` |
| Shell stiffener（板／型材 Data Bank） | `<panel_name>/S<seq>[P\|S\|SP][W\|F]`；`<seq>` 為加入板架時給的中性序號，Assembly Planning 參照同一號碼；例 `AA567-8/S5PP` |
| Shell plate（結構／板 Data Bank） | 任意／`<panel_name>-<seq>[S\|P]` |

官方 MANU 範例（板架 `SP241-30`）：序號 1 的板 `SPSHP-200` 轉出為 `SP241-30-1S`、`-1P`；序號 1 的加強材 `SPL960-S3` 轉出 `SP241-30/S1S`、`/S1P`。〔待核對：官方表中序號 2 的加強材寫成 `SP241-30-S2S`，與前述格式不一致，疑為筆誤。〕

**Shell profile 編號：** composed name 為 `<group_name>[<surface_suffix>]<number>`，例 `AAL250`，設計者永遠以編號稱呼。縱向、橫向有各自 group name（建議 `AAL`、`AAT`）與界限表（`AALLIM`、`AATLIM`；y、z 向表加 `Y`、`Z`）。編號規則（部分為暫時性；違反主要影響符號式視圖自動產生斷面）：

| 項目 | 縱向 | 橫向 |
|---|---|---|
| 範圍與型式 | 整數 5–999 | 整數 1–4999，通常等於肋位號，不可為負 |
| 比例 | 圖面號碼**乘 10**（讓艏艉插入的縱骨仍是整數），出圖除以 10 | 有半肋位可乘 10 |
| 甲板 | 比同距中心線的舷側縱骨**加 1000**，出圖減去 | 無特別規定 |
| 右舷專屬 | 比左舷同位置**加 2000**（甲板者大於 3000） | **加 5000** |

> 〔公開版未收錄：AVEVA 官方產品截圖〕縱骨編號規則：右舷專屬者加 2000（L2020、L2360、L3020）。

*圖 6-7　縱骨編號規則。（AVEVA 官方文件截圖，僅供內部教學）*

Hull curves（frame、waterline、buttock，皆平面曲線；seam／butt 可為任意形狀）：現代 Marine 可直接參照曲面，不一定需預定義曲線；編號通常為正（frame 可為負）、小於 10000，frame 在 [-899, 2766]。建議 group name `AAX`、`AAY`、`AAZ`、`AAS`（frames、buttocks、waterlines、seams／butts）；座標表 `AAXTAB`、`AAYTAB`、`AAZTAB`；seam 界限表 `AASLIMX`、`AASLIMZ`。啟用**自由命名**後 seam 與 shell profile 可用任意名稱。

**自由命名需要 NSEQ 資料庫：** (1) 建 Name Sequence 型資料庫（update 模式；用 Global 時每個會建 seam／profile 的 site 各一個）；(2) 加入適當 MDB；(3) 不用 Global 即完成，否則須經 **.Net PML 介面**手動定義序列：每個曲面一個 `CSEAM_<曲面名>_`（如 `CSEAM_HULL_`），縱橫向用 `CLONG_`、`CTRANS_`，各 site 範圍互不重疊，序號 0–9999；(4) 在 Hull Design 新建曲面後須先定義序列才能建模。**自動命名生產草圖**的規則屬性 `/AUTO_SEQNO` 同樣用 NSEQ（Hulldesign 需讀寫權限），Global 時須手動定義 `PPAN`、`CPAN`、`WCOG`、`PARTL`、`PSKETCH`、`PNEST`、`BENDTPL`、`JIGPILLAR`、`PLATEJIG` 等序列（序號 0–21477483647）。

**自動板架命名：** Planar Modelling 需要板架名時，若 Vitesse 程式庫目錄有 `_TBhook_AutoPanelName.py` 就啟動它；Hull 隨附範例，建議依船廠慣例修改或移除；範例名 `AA123-FR26SBP_3`（Block、肋位 26、對稱碼、流水號）。多數情況仍可明確指定名稱覆蓋。

## 6.9 Standards：設計標準

Hull 的設計標準影響零件的**物理性質**。實作分三類：**Closed**（焊死在程式碼，變更須由 AVEVA 提供，但立即可用、協作最順）、**Toolbox**（客戶組合工具自建）、**Open**（完全自訂，最彈性但須先設定；與外部交換模型時**須連同標準設定一併交付**，否則可能同名異物或異名同物）。選擇看變更頻率、彈性與易用性取捨、協作便利。

| 標準 | 類型與重點 |
|---|---|
| Holes／Notches | 大量內建型式，尺寸由參數指定；任何封閉曲線可當孔、與外輪廓相交的開放曲線可當缺口；全新型式須由 AVEVA 新增 |
| Profile Cutouts／Clips | Cutout 可由內建樣式實例化，或以 geometry macro 描述，完全開放；Clip 以 macro 建立，不可有孔，目前不能與型材 cutout 關聯 |
| Profile Types | **封閉**：保留型號與固定順序的尺寸參數，新型式須由 AVEVA 實作 |
| Endcuts／Connection codes | Endcut 部分開放（可就支援型式建新實例，隨附設定檔）；connection code 實務上完全開放 |
| Stiffener Connections | RSO 的屬性 `TIGHT`、`SNIPE`、`OVERLAP`；對照存於標準物件 `__SBED_STIFF_ENDS__` |
| Folded Flanges／Brackets | 工具箱；肘板由標準 toe 與連接、參數自動計算規則組成，一組參數即該型式的一個「實例」；太特殊者做 panel bracket |
| Bevels／Swedging／Knuckling／Shrinkage | Bevel 工具箱含對接焊、固定角角焊、變角角焊（依板厚與連接角自動選）三類；收縮補償可手動或依船廠經驗表格自動套用 |

> **專業提醒：** Closed 類標準不要在專案中途試圖繞過，否則升級與支援都有風險。

## 6.10 座標系與相對位置

所有零件定位在座標系，可為局部、可巢狀，最終須相對於一個**全域座標系**。船的規則：原點在船艉端、最好在底部與中心線（CL）上（放在艉垂線之後使所有 x 為正，或放在艉垂線）；x 朝船艏；y 朝「against portside」（官方原文）；z 朝上。平面零件描述在局部座標系 uvw 的 uv 平面；uv 與 xyz 主平面重合時有標準擺法。Data Bank 中座標**一律為毫米**。

> 〔公開版未收錄：AVEVA 官方產品截圖〕全域座標系與 frame、waterline、buttock 的局部 uv 方向。

*圖 6-8　全域座標系與局部 uv。（AVEVA 官方文件截圖，僅供內部教學）*

〔待核對：y 軸方向文字易誤讀，請對照[第 5 章](ch05_coordinates_geometry_zh-TW.reading.html)與官方圖，並在訓練專案以實際點位驗證正負。〕

**相對位置：** 縱向座標太大，造船傳統用「肋位號 + 前後距離」。

| 寫法 | 意義 |
|---|---|
| `X=FR45 +100`／`X=FR45 -150` | 肋位 45 向艏 100 mm／向艉 150 mm |
| `Y=LP10 +100` | 縱向位置（Longitudinal Position）10 向左舷 100 mm（底部 LP 通常只定義左舷） |
| `Z=LP35 -100` | 舷側 LP35 之下 100 mm |
| `Y=LP-20+100` | 右舷對應位置以**負的 LP 編號**表示 |

肋位規則：須為數字（不可含字母）、可為負；範圍 [-899, 2766]；總數目前限 500，**連續編號**時範圍 [-99, 500]（600 個）；編號與位置關係可任意、肋距可變；對照存於客戶設定的表。轉換建議：艉尖艙的 A、B、C 改負數（A→-1）；中間肋位 56A、56B 改 561、562。LP 規則：編號 [0, 999]；水平與垂直位置號碼**不應相同**；可在 CL（y=0）定義編號 0；LP 構成網格，**不必**與實際縱骨一一對應。

> 〔公開版未收錄：AVEVA 官方產品截圖〕中艙剖面與縱向位置：十字點為 Y=LP6、Z=LP26.5。

*圖 6-9　Midship section 與縱向位置。（AVEVA 官方文件截圖，僅供內部教學）*

**座標表輸入檔：** 純文字檔（檔名任意、格式自由、建議一行一筆、行寬 80），由 `inithull` 讀入，結果存為表格物件 `__SBH_GENTAB__`（`SB_OGDB`）。記錄 `<type> <F_No> <step_No> <L_No> <F_coord> <step_coord>`：`type` 20＝frame、30＝水平縱向位置（y）、40＝垂直縱向位置（z）；編號 `F_No` 得 `F_coord`，`F_No+step_No` 得 `F_coord+step_coord`，直到 `L_No`。官方範例：

```
20  -10  1  295  -7450.0  745.0
30    0  1   15      0.0  750.0
40   18  1   31    600.0  675.0
```

## 6.11 Run Mode Control

| 層級 | 控制方式 |
|---|---|
| Module | 預設參數檔（default／ip file），須放在 `SB_SHIP` 目錄（`ppanparts`、`bendtempl`、`cpanparts`、`profnest`、`matplate`、`jigpillar`、`platejigs`、`mark3axis`、`wcog`、Nesting、PLCM）；環境變數**只填檔名不填路徑**，因檔名常存在物件內（如套料板），改目錄後仍有效 |
| Facility | ASCII 檔（connection code、預設 cutout、cutout 號碼與 macro 關聯；執行時讀入，可由 `inithull` 檢查），或結構 Data Bank 內的物件（TIL 類語法，固定名稱，有時由環境變數控制） |
| Application | 專案環境、命名與肋位縱向間距規則（`inithull`）、對稱處理（環境變數，通常定義在專案檔） |

**對稱狀態：** 板架可為對稱、左舷、右舷或在／跨中心線，**建模時必須明確指定**。代碼：`SBPS`（對稱，一份定義、兩舷各一副本）、`P`（左舷專屬）、`S`（右舷專屬）、`SP`（在／跨 CL，如中心線桁、兩舷都有零件的甲板）。`P`、`S` 板架可稍延伸到對面，但不可在對面存完整零件，否則視為 `SP`。Curved panel 的對稱暫由名稱後綴控制，所有板架（跨 CL 除外）應描述在左舷。Marine 假設板零件**存放在其實際位置**，與板架建在哪舷無關；對稱板架取出時預設兩舷各建獨立實例（不必完全鏡像）。

Panel bracket 取出板零件只有一件，各使用處另建幾乎空的零件，僅含管理資訊與指向該板零件的指標，幾何由被指者繼承。

**殼板厚度補償：** 雙層殼或「平面」外殼必須自動考慮板厚及隨角度的變形。Hull curve 與 shell profile trace 以與型面的交線儲存；hull curve 當板架邊界時依殼板厚與交角轉換；參照 shell profile 斷面時移到所焊殼板的正確側，使 cutout 與連接的加強材、肘板尺寸正確。以環境變數 **`SBH_ENABLE_SHPLACOMP`**（任意值）啟用，僅在需要的專案開（影響效能）；涉及 shell profile 參照時必須用自動功能。

> 〔公開版未收錄：AVEVA 官方產品截圖〕板架對殼板建立：左為手動平行移動型面曲線補償，右為啟用自動板厚補償。

*圖 6-10　無／有自動殼板厚度補償。（AVEVA 官方文件截圖，僅供內部教學）*

**殼板圖形表示：** 預設依展開條帶產生**面片**原始體；設 **`SBH_ENABLE_SOLID_PLATES=YES`** 則依曲面與 seam 產生**實體**原始體，精度高、3D 可顯示孔，適合匯出機械軟體或啟用殼板補償，產生稍慢。

**型材參考點：** 影響連接加強材、肘板、clip、cutout 的位置與高度，通常在腹板下緣 mould line 側。已定義自動 trace bevel 時預設型材與毗鄰板架無間隙（若設 `SBH_CHECK_PROF_TRACE` 且腹板是轉成板零件的候選——經 `SBH_PROF_TO_PLDB` 指定檔案——則 mould 側在毗鄰板面上）；否則由 **`SBH_PROFPT_ADJUST`** 決定：未設（預設）＝參考點在板面，忽略傾斜抬升；`TRUE`＝假設腹板焊接邊為矩形（腹板與板面夾角大於 90° 時型材抬高）；`MID`＝腹板中點在板面。

> **專業提醒：** 這些都是**專案層級**行為開關，建模開始後不要中途改。〔待核對：官方未說明中途切換的後果，此為保守建議。〕

## 6.12 Functional Descriptions（FD）

**FD** 是可指派給 RSO、板架或板架內零件（板、加強材、翼板、柱、肘板、複板、clip）的描述性字串，跟著零件走完專案。可當名稱標籤（便於 `Info/Model` 與零件表），也可控制自動評估（如焊腳尺寸、由 RSO 自動產生板架）；設在鋼構件上（如把甲板加強材設成 deck girder），符號式視圖會畫成毗鄰板架。

- 字串最長 75 字元，可含預定義參數；FD＝字串 + 功能碼（整數 0–32767，與字串一對一）；模型物件只存**碼**。
- 碼 0 是預設 FD；未定義的碼有時可用，被詢問時可能出錯。AVEVA 預留 **9000–10999**。水密與否不在 FD，用 Data Types 表示。

| 群組 | 碼 | 例 |
|---|---|---|
| Decks | 9000–9099 | 9001 Weather Deck、9003 Main Deck、9004 Strength Deck、9010 Inner Bottom、9012 Tank Top |
| Longitudinal Bulkheads | 9100–9199 | 9101 Centerline、9105 Wash、9106 Corrugated |
| Transversal Bulkheads | 9200–9299 | 9201 Aft Peak、9202 Collision |
| Girders／Web-frame／Shell／Misc. | 9300–9699 | 9303 Deck Girder、9401 Floor、9501 Keel、9505 Sheerstrake、9601 Hatch Coaming（各群依序 9300、9400、9500、9600 起） |
| Part Information | 9900–9903 | General Part、Bracket、Flange、Doubling（以小板架表示肘板或複板時用） |

## 6.13 XML Interfaces：給二次開發者的主角

| 格式 | 用途 |
|---|---|
| **TXSUR** | 曲面：HullSurface、AdditionalSurfaces（如煙囪）、ReferenceSurfaces（RSO）。目前（M3SP4 敘述）只有 CurveRepresentation 可用 |
| **TXISUR** | RSO 的**定義資料**，可用來產生 RSO、支援自寫建立編輯功能、跨專案重用；匯入匯出是 MDS Marine Hull Structural Design 的功能 |
| **TXHBD** | 早期設計導向描述：Units、ShipParameters、CoordinateTables、Spaces（目前只實作 compartment）、CrossSections2D |
| **TXHSTL** | 船體鋼構。**-M**（Modelling，輸入，重拓撲與參數）、**-R**（Reporting，輸出，重幾何與材質）。最早用於把 Structural Design 資料送到 ClassNK PrimeShip 與 MSC Patran／Nastran |
| **TXHCM** | 以 XML 輸入檔建立**曲面船體**物件 |

**XML 基礎：** 文件是只有單一根元素的樹；元素組織屬性，**屬性才載資料**；屬性值須**雙引號**；每個 start tag 要有 end tag（或空元素 `<Ship/>`）；**區分大小寫**；版面與屬性順序自由；tag 不可交叉。Vocabulary 以 DTD、XML Schema 或 XML Data Reduced 描述，根元素以 `xsi:noNamespaceSchemaLocation="CurvedHull.xsd"` 引用才能驗證。官方範例：

```xml
<Ship>
  <Defaults Surface="SPHULL" XMin="FR40" YMin="0" XMax="FR80"/>
  <HullCurve ObjId="SPX951"><ByPrincipalPlane X="FR30"/></HullCurve>
</Ship>
```

> 〔公開版未收錄：AVEVA 官方產品截圖〕XML 樹：Ship 下有 Defaults 與 HullCurve。

*圖 6-11　官方範例的 XML 樹。（AVEVA 官方文件截圖，僅供內部教學）*

### 6.13.1 TXHBD 與 TXHSTL

TXHBD：`Units` 定義長度、面積、重量、角度、速度單位；`ShipParameters` 含 `MainParticulars`（LBP、LOA、LWL、Draft、Depth、BOA、Cb 等）、`Classification`、`General`；`CrossSections2D` 由 `TransverseSection`（`Name`、`X`）組成，內有 `PlanePanel`（`Instance`、`FunctionalProperty`、`Tightness`、`ModelRef`、`Trace`、`Boundary`）、`PlateGroup`、`StiffenerGroup`、`KnuckledPanel`、`CurvedPanel`（無 `ModelRef`，因總參照船殼）、`Compartment`。

TXHSTL 的根元素 `Ship` 下有 `Material`、`BarSection`、`HoleDef`、`NotchDef`（定義標準，供 `Block` 內零件參照）、`Block`，另有 `Joint`；schema 為 `TXHSTL-R.xsd`、`TXHSTL-M.xsd`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕TXHSTL 的 Ship 根元素。

*圖 6-12　TXHSTL schema 的根。（AVEVA 官方文件截圖，僅供內部教學）*

```xml
<Material Grade="A27" Density="7790" YoungsModulus="205000" PoissonRatio="0.3"
          YieldStress="270" UltimateStress="490" ThermalExpansionCoefficient="0.011"/>
<BarSection BarSectionId="LBar180*90*10*10">
  <LBar Height="180" Width="90" WebThickness="10" FlangeThickness="10"/>
  <SectionProperties Area="2620" NeutralAxisU="117.2" NeutralAxisV="18.5" InertiaU="880" InertiaV="151"/>
</BarSection>
<HoleDef HoleDefId="HO800*600"><Manhole Height="800" Width="600"/></HoleDef>
<NotchDef NotchDefId="VUF250*150*50"><VUF Width="250" Height="150" Radius="50"/></NotchDef>
```

在 **-M** 中，每出現一個 `Material`（以 `Grade` 為鍵）就是「不存在則建、存在則更新」；帶 `SectionProperties` 的 `BarSection` 成為斷面標準，-R 輸出時型材與之比對，符合就附斷面性質；`HoleDef`／`NotchDef` 可被參照，也可直接以 `HoleShape` 的 `HoleType` 與 `Parameters` 定義。**`Block` 以 `ObjId` 命名，已存在則更新**，板架、群組、元件同理，因此可只送要改的部分。官方範例（更新板架 `ES123-730` 的孔）：

```xml
<Ship><Block ObjId="ES123"><PlanePanel ObjId="ES123-730">
  <HoleGroup GroupId="5"><HoleShape HoleType="HO"><Parameters>800 400</Parameters></HoleShape></HoleGroup>
</PlanePanel></Block></Ship>
```

（官方原文 `HoleGroup` 未關閉，已補正；依 `TXHSTL-M.xsd` 驗證。〔待核對〕）

**-R 的基本型別：** `ObjId`／`GroupId`／`CompId` 唯一識別物件、元件群、單一元件；`ModelRef` 以 `ObjType`、`ObjId`、`CompType`、`CompId` 參照物件或其一部分；**幾何一律是圓弧段構成的曲線輪廓**（終點加 amplitude vector——弦中點垂直指向弧頂——定義一段，零長即直線）；`PlanePanelT` 幾何相對 `CoordSys`；`PlaneBoundaryT` 有 `SimpleContour`（不含 cutout、notch）與 `DetailedContour`（含）；`PlaneStiffenerT` 以 `Trace`、`Offset`、`Inclination` 描述，建實體須把 `BarShape` 的 `Crossection` 沿 trace 移動；`CurvedPanelT` 幾何在**全域座標系**，可附 `FacetSurfaceT`（點矩陣三角面片）。**Idealizer 選項**輸出供 FEM 用的理想化幾何（板無厚度、型材無高寬厚、消除間隙）。

### 6.13.2 TXHCM：以 XML 建立曲面船體

這是對開發者最實用的一種：批次產生曲面船體物件，等價於互動 Curved Hull。Schema `CurvedHull.xsd` 與 `HullBasic.xsd` 位於 `SB_SYSTEM\xml`；根元素 `Ship` 須引用 schema，其下 1 到無限個子元素：`Defaults`、`Seam`、`ShellPlate`、`ShellProfile`、`ShellStiffener`、`CurvedPanel`、`HullCurve`、`PrincipalPlane`、`Plane`。

> 〔公開版未收錄：AVEVA 官方產品截圖〕TXHCM 的 Ship 根元素：九種子元素的 Choice，1 到無限個。

*圖 6-13　曲面船體輸入語言的根。（AVEVA 官方文件截圖，僅供內部教學）*

讀 schema 圖：Choice 任選、Sequence 依序全部出現、**虛線框為選用**，屬性清單列型別、必填、預設值。

> 〔公開版未收錄：AVEVA 官方產品截圖〕ShellProfile：Material 必填，Position 選用，Branch 1–999，Features 選用。

*圖 6-14　ShellProfile 的 schema 圖。（AVEVA 官方文件截圖，僅供內部教學）*

| 元素 | 重點 |
|---|---|
| `Defaults` | `Surface`、`XMin…ZMax`（省略即無限）。**模態**：作用至下一個 `Defaults`，新的**完全覆蓋**前一個（連預設曲面也清空） |
| `Point`／`Plane` | `Point` 有 `Explicit`、`Polar`、`OnSurface`、`OnCurve`、`Moved`、`Stored`；`Plane` 有 `ByPoints`、`AxisParallel`、`Angled`、`Rotated`、`Stored`；座標值用「傳統 Marine 格式」如 `FR50-125` |
| `PrincipalPlane`／`ByPrincipalPlane` | `X`／`Y`／`Z` 擇一；前者有必填 `ObjId` 並存入資料庫，後者只用於定義 seam／curve 且有 `Surface` |
| `Seam` | `ObjId`（必填）、`Refl`、`Symmetry`（`Auto`／`Symmetric`／`SB`／`PS`／`CL`）、`BlockLimit`；曲線五選一：平面交線、`ByCylinder`（`GeneratorX/Y/Z`，2–100 點）、`Parallel`（`Displacement` 的 `Side`、`Method`＝`X`/`Y`/`Z`/`Perp`、`End1`/`End2` 的 `Distance`、`Excess`）、`Combined`、`Stored`；可選 `Box`。`HullCurve` 幾乎相同但無 `Symmetry`、`BlockLimit` |
| `ShellProfile` | `ObjId`、`SubType`（`Long`／`Trans`，必填）、`Delete`、`Skip`（兩者皆真＝只刪不產生）；`Material`（`Type`、`Parameters`、`Grade`）、`Position`、`Branch`、`Features` |
| `ShellStiffener` | `Posno`、`BevelTrace`、`Shrinkage`、`WeldDepth`、`Dummy`；`End1`／`End2`（`Endcut`、`Connection`）、`Inclination`、`GeneralPurpose`（`GPS1`–`GPS4` 等）。可在 `Branch` 內，或直接在 `Ship` 下（另有 `ObjId`、`ShellProfileId`、`SubType`），後者 trace 目前限平面曲線或沿具名曲線 |
| `ShellPlate` | `ObjId`（後綴反映對稱）、`PosNo`；3–12 個 `Edge`（以 seam 圍成輪廓，須**由外側向內看順時針、從最艉的開始**；可帶 `Bevel`、`Excess`、`Compensation`）；`ShellPlateData`（`Material`、`Position`、`GeneralPurpose`、`DevOptions`、`PPI`） |
| `CurvedPanel` | `ObjId`、`Symmetry`、`Block`（必填）；含 `ShellPlate`、`ShellStiffener`、`ShellProfile`（自動選外包盒在板架盒內者，可設 `Tolerance`）、`Hole` |

**Shell profile 的分割點：** 一條 profile 沿 branch 依「分割點」切成多支 shell stiffener，分割點可為主平面、板架、seam、曲線或另一 shell profile，**依輸入順序逐一切分**，須依沿 trace 的出現順序給（順向反向皆可，但至少兩個才能偵測反向）。分割點寫在 `End2/Connection`：第一支的 `End2` 是第一與第二支之間；**最後一支的 `End2` 不是分割點，是整條末端界限**；第一支的 `End1/Connection` 是起端界限。因此產生的 shell stiffener 數**必等於**輸入的 `ShellStiffener` 元素數。多個交點時可用 `Approx` 給近似點，否則取沿 trace 第一個。`Stored` 的 `ObjType` 可為 `HullCurve`、`Plane`、`PlanePanel`、`Seam`、`ShellProfile`。`End1`／`End2` 指輸入順序的方向，若與 trace 相反，寫在 `End1` 的資料會設到物件的 end 2。`Connection` 有 `Type`（connection code）、`Clearance`（覆蓋 connection code）、`Plane`（`Cutting`／`Frame`／`Buttock`／`Waterline`）。

**Features：** `HoleGroup`（`Height`、先 `Position` 後 `Shape`；位置字串可含重複語法如 `"FR10(5)FR100"`、`"1000 2000 3000"`）、`NotchGroup`、`CutoutGroup`（以 `ShellProfile` 的 `ObjIds` 指定穿過者）、`MarkingGroup`。參數字串以**空白**分隔，`"100,10"` 不合法。**`DevOptions`**（皆選用）：`RollAxes`、`WorkshopMethod`（`Contraction` 預設／`Expansion`／`NoDeformation`，後者只適用單曲率或近單曲率板）、`RawPlateMargin`、`StripDirection`（`Auto` 預設）、`NumStrips`、`SplineTolerance`。**`PPI`** 含 `BendTempl` 與 `CPanParts`（`MarkTemplate`、`MarkLong` 等旗標覆蓋該板預設標記；列出某群 `ObjIds` 後**只標記所列者**）。Curved panel 的 `Hole` 位置原點為「線與曲面的交點」，線有三種：有限 `Line`（兩點）、平行座標軸的 `Axis`（需 `Approx` 近似座標）、`AsStored`（任意曲線輪廓沿其平面法向投影）；非對稱孔需 `RotationPoint`。

〔待核對：官方 `Defaults` 範例以 `Z="FR50"`（肋位當 z 座標）疑為筆誤，勿照抄。〕

**重要限制：** (1) 每次執行都**從頭計算**：同名 shell profile 會先刪除再產生（輸入檔失敗則舊的保留），故「XML 產生 → 互動 Curved Hull 修改 → 再跑 XML」會**使互動修改全部消失**；(2) curved panel 序號（殼型材、殼板各一序列，板架範圍內）在加入板架時指派，被組立參照並構成 `SB_PLDB`／`SBH_PROFDB` 零件名的一部分，**元素順序不變，重跑序號才相同**；(3) 逐支產生 shell profile 時系統會合併相鄰 dummy 區間、移除兩端與全 dummy 的 branch，需自管 dummy 區間時應改用 `ShellProfile`。

> **專業提醒：** XML 批次是可重播、每次重算的做法，與互動修改互斥。選定一種並遵守：要用 XML 管理的物件，就只在 XML 檔裡改。

## 6.14 Project Material（專案材料）

套料用原材料定義在目錄，**數量視為無限**。與 ERM 整合須用 Project Material：參照目錄項目並追蹤每張原材料實例（可有各自 ERM 識別碼；見官方《AVEVA Marine - ERM Integration User Guide》）。

| 項目 | 說明 |
|---|---|
| 位置與限制 | 存於 Manufacturing database，材料指派給單元（通常是生產 Block）或專案池。**全或無**：一旦使用須整個專案都用 |
| 專案池 | 須存在元素 `FMTRPO`，以通用語法新增：`NEW FMTRPO /ProjMtrl` |
| 實例 | `FPRJIN`（板與型材共用），屬性 `Avbity`：`Available`、`Consumed`（有套料板或型材參照）、`Reserved`、`Proposed` |
| 性質與餘料 | 性質由目錄項目取得（`RprRef`、`RplRef`），唯讀；套料餘料存於同單元或專案池，參照來源材料 |

> 〔公開版未收錄：AVEVA 官方產品截圖〕Manufacturing Explorer 的專案型材元素與屬性。

*圖 6-15　Project Material 的型材規格與實例。（AVEVA 官方文件截圖，僅供內部教學）*

> **常見錯誤：** 已有部分生產 Block 完成套料後才中途改用 Project Material。官方要求全專案一致。〔待核對：中途切換的實際後果官方未說明。〕

## 6.15 Marine Dictionary 重點詞條

Marine Dictionary 是**詞條表**（A–Z 共 24 個字母頁，每頁「Index／Explanation」兩欄）。依主題歸納重點：

| 主題 | 詞條（官方定義整理） |
|---|---|
| 資料 | **object**；**object type**（由 Databank code、Object code 1、Object code 2 唯一識別）；**data bank**（專案中同類資料）；**database**（一個專案的資料集合）；**environment variable／logical name**（以 Windows 環境變數實作的專案參數）；**default file／IP file**（information to the program，控制程式行為，客製化重要工具）；**type code**（使用者自訂，四個欄位，type code 1 即 object subtype）；**alias name**（四個欄位） |
| 結構 | **block**（一次吊裝單位；Hull 中是地理容器）；**panel**；**section**（總段）；**zone**（為規劃預先定義的連續區域）；**compartment**（不一定水密）；**module** |
| 零件特徵 | **piece part**（組立階層最低層，可能因補償收縮或 excess 而與標稱設計零件不同）；**seam**（沿船長的板間邊界，船橫向者稱 **butt**）；**hole**（Hull 中若孔幾何部分在板外或跨多片板，分割時轉成相關板的 cutout）；**doubling**（柱底小複板）；**shell profile**；**stanchion＝pillar**；**scallop／slot＝cutout**；**rat hole＝notch** |
| 拓撲與流程 | **topology**（多指板架間相依，改一個可連帶改多個）；**input scheme**（讀入後建立資料的輸入檔，常指平面板架批次檔）；**modelling** |
| 狀態與權限 | 物件有四個獨立 **status**：Design、Material Control、Manufacturing、Assembly；**access level**：None／Read／Read & Write／Read & Write & Change status，權限關聯 **Role** |
| 工具 | **Trigger**（啟動 Vitesse／Python 腳本的事件，可調整功能行為或連接外部軟體）；**Vitesse**；**data extraction**（以 Data Extraction 工具取資料） |

縮寫表（節錄）：**PIM**、**FD**、**RSO**、**CAT**（縮寫表作 Curve and Table，Hull 文件作 Contour And Table）、**TID**（Initial Design）、**TDM**、**TJL**（Job Launcher）、**PPI**、**PLCM**、**CVBA**、**AP**（Assembly Planning）、**WP**（Weld Planning）。

## 6.16 二次開發者怎麼接

| 需求 | 途徑（依據） |
|---|---|
| 批次建立或更新曲面船體物件 | **TXHCM**（6.13.2） |
| 批次更新板架內元件（孔尺寸、材質） | **TXHSTL-M**，「存在即更新」 |
| 匯出鋼構供 FEM／他系統 | **TXHSTL-R**（可開 Idealizer） |
| 讀船體專屬資料、報表 | Vitesse 資料抽取（[第 36 章](ch36_hull_vitesse_zh-TW.reading.html)） |
| 自動板架命名 | Vitesse trigger `_TBhook_AutoPanelName.py` |
| 定義 name sequence（Global） | .NET PML 介面〔細節見官方 .NET customization 手冊，本章未讀〕 |
| 自寫生產程式 | Production database（Oracle）〔待核對〕 |

設計時要記得：

1. **名稱是索引但不是唯一資料來源。** `Block-序號` 與 `P`／`S`／`SP` 後綴可解析，但 Curved Panel 的後綴是「暫時」規則，且啟用自由命名後 seam 與 shell profile 不再遵守；優先讀屬性。
2. **區分設計名（固定）與生產名（動態）**；別把生產名當主鍵。
3. **隱式零件讀不到完整幾何**：走取出後的 Plate／Profile Data Bank 或 TXHSTL-R。
4. **拓撲決定順序**：自寫批次重建板架須遵守拓撲順序，或呼叫官方 Recreate。
5. **XML 與互動修改互斥**；`Defaults` 模態與元素順序影響序號是批次最常見的非預期來源。
6. 與 E3D 元素（`HPANEL`、`CPANEL`）的對映見第 9 章 9.3；本章未涉及兩者對映細節〔待核對〕。

## 6.17 本章小結

1. PIM 是設計與生產共用的資料庫；Design Model 隱式、標稱尺寸，Hull Parts 才是取出後的結果。
2. 設計結構是 Hull Structure → Block → Panel → Part；Block 是地理容器；平面板架含隱式零件，曲面板架是純容器；組立結構以名稱雙向對映。
3. 拓撲＝定義參照＋相依參照；用參照不用座標、避免循環。
4. 設計名固定、生產名動態；設計名 ≤24 字元，有嚴格的後綴與編號規則。
5. 座標單位 mm，位置用 `FR`、`LP` 表示；Run Mode Control 的對稱與板厚補償是專案層級環境變數。
6. XML 有四種格式；TXHCM 與 TXHSTL-M 可批次建立／更新，但每次重算，與互動修改互斥。

## 6.18 練習題／自我檢核

1. 設計模型為何沒有板的完整幾何？取得完整幾何有哪兩條路？
2. Block 與 Assembly 差在哪？平面與曲面板架在「零件來源」上的最大差別？
3. 定義參照與相依參照各是什麼？後者存在哪個 Data Bank？
4. 板架 `AA123-4`、序號 9：左舷板零件與右舷加強材名稱各為何？
5. 縱骨編號 250 出圖顯示多少？右舷專屬、位於甲板的同位置縱骨編號是多少？
6. `X=FR45 -150` 與 `Y=LP-20+100` 各代表何處？
7. TXHCM 連續兩個 `Defaults`，後者與前者的關係？重跑 XML 前曾互動修改該物件會怎樣？
8. 練習（訓練專案）：檢查一個板架的 Block 與名稱是否符合建議；用 Topology 畫相依圖；手寫含 `Defaults` 與一條 `Seam` 的 XML，**先對 `CurvedHull.xsd` 驗證**。〔待核對：匯入入口依公司版本。〕

## 6.19 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 6 章](appx_d_verification_zh-TW.reading.html#ch06)；取材覆蓋與未讀範圍：見[附錄 E 第 6 章](appx_e_coverage_zh-TW.reading.html#ch06)。

## 資料來源

AVEVA Marine 12.1 離線官方文件：Hull Concepts（1110533 及子頁）、Hull Basic Features and Concepts（1105739 及子頁）。圖片取自該文件，僅供內部教學。
