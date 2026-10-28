# 附錄 B　術語表與指令速查

> 本附錄收錄整套課程使用的術語與命令列常用指令，方便閱讀各章或寫程式時查閱。術語以「英文（縮寫）→ 中文 → 一句話解釋 → 主要章節」排列；指令速查依用途分組。
>
> 術語解釋是本課程的自主整理。指令部分，來自 AVEVA E3D 2.1 官方參考手冊、本課程開源範例或實際程式截圖的寫法未加標記；屬於 PDMS／Marine 常見用法、但尚未在官方頁面或實機上確認的寫法，標示 **〔待核對〕**，請在公司版本的訓練專案中驗證後，再寫入公司內部的速查表。會修改資料的指令，只能在訓練專案中使用。

## B.1 如何使用本附錄

- 讀章節時遇到不熟的詞，先查 B.2 的術語表，再回到「主要章節」欄位所列的章節。
- 寫程式時，先查 B.3 的指令速查找到寫法，再到第 11、12 章看完整語法。
- 建議把 B.3 複製一份，加上公司版本的驗證結果與錯誤訊息原文，作為團隊的內部速查表。

各章連結：[第 1 章](ch01_architecture_zh-TW.reading.html)、[第 2 章](ch02_project_database_zh-TW.reading.html)、[第 3 章](ch03_hierarchy_attributes_zh-TW.reading.html)、[第 4 章](ch04_coordinates_geometry_zh-TW.reading.html)、[第 5 章](ch05_hull_modelling_zh-TW.reading.html)、[第 6 章](ch06_hull_production_zh-TW.reading.html)、[第 7 章](ch07_outfitting_zh-TW.reading.html)、[第 8 章](ch08_catalogue_spec_zh-TW.reading.html)、[第 9 章](ch09_drawings_zh-TW.reading.html)、[第 10 章](ch10_dev_environment_zh-TW.reading.html)、[第 11 章](ch11_pml_language_zh-TW.reading.html)、[第 12 章](ch12_pml_database_zh-TW.reading.html)、[第 13 章](ch13_pml_forms_addins_zh-TW.reading.html)、[第 14 章](ch14_dotnet_zh-TW.reading.html)、[第 15 章](ch15_hull_vitesse_zh-TW.reading.html)、[第 16 章](ch16_reports_integration_zh-TW.reading.html)、[第 17 章](ch17_debug_deploy_zh-TW.reading.html)、[第 18 章](ch18_case_studies_zh-TW.reading.html)。

## B.2 術語表

### B.2.1 產品、模組與環境

| 英文（縮寫） | 中文 | 一句話解釋 | 主要章節 |
|---|---|---|---|
| AVEVA Marine | AVEVA Marine | 整合 Tribon M3 船體與 PDMS 舾裝的造船設計系統 | 1 |
| Tribon M3 | Tribon M3 | AVEVA Marine 船體模組的前身，造船專用設計與生產系統 | 1、15 |
| PDMS（Plant Design Management System） | 工廠設計管理系統 | AVEVA Marine 舾裝與管理模組的前身 | 1 |
| AVEVA E3D（Everything3D） | E3D | PDMS 的後繼產品；其官方文件可用來理解舾裝資料模型 | 1、3 |
| Hull Structural Design | 船體結構設計 | 基本設計階段快速建立主要構件的模組 | 1、5 |
| Hull Detailed Design | 船體詳細設計 | 涵蓋平面、曲面船體與生產資訊的船體模組 | 1、5、6 |
| Outfitting（Design） | 舾裝設計 | 設備、管路、鐵舾裝、通風、電纜托架的建模模組 | 1、7 |
| Marine Drafting | 船體圖面 | 承襲 Tribon 的船體出圖工具 | 1、9 |
| Outfitting Draft | 舾裝圖面 | 承襲 PDMS Draft 的舾裝出圖工具 | 1、9 |
| Isodraft | ISO 圖產生器 | 依管線自動產生等角管段圖 | 1、9 |
| Assembly Planning | 裝配規劃 | 建立分段與組立樹、規劃裝配順序 | 1、6 |
| Weld Planning | 焊接規劃 | 管理焊接資訊與焊接規劃 | 1、6 |
| Monitor | Monitor | 登入專案後的起點模組 | 1 |
| Admin | 系統管理模組 | 管理使用者、Team、DB、MDB 與 Session 的模組 | 1、2 |
| Lexicon | Lexicon | 定義 UDA 與 UDET 的模組，資料存於 DICT | 1、3 |
| Paragon | Paragon | 建立與維護目錄元件的模組 | 1、8 |
| Propcon | Propcon | 維護材料性質（PROP）的模組 | 1、8 |
| Specon | Specon | 以命令方式建立等級的模組 | 1、8 |
| Command Window | 命令列 | 輸入命令與查看輸出的視窗；介面操作背後都是命令 | 1、3 |
| Environment Variable | 環境變數 | 啟動時決定程式與資料位置的設定 | 1、10 |
| `PDMSEXE` | 安裝目錄變數 | 執行檔與系統資料所在目錄 | 1 |
| `PMLLIB` | PML 搜尋路徑 | 系統依序搜尋 PML 檔案的目錄清單 | 1、10 |
| `PDMSUI` | 介面檔搜尋路徑 | 介面檔與 PML Add-in 定義的搜尋路徑 | 1、10、13 |
| `CAF_ADDINS_PATH` | .NET Add-in 設定路徑 | 讓 .NET Add-in 設定檔可放在安裝目錄以外 | 1、14 |
| `XXX000` | 專案資料路徑變數 | 專案代碼加 `000`，指向該專案的資料庫檔案目錄 | 1、2 |
| `pml.index` | PML 索引檔 | 每個 PMLLIB 目錄的檔案索引，新增檔案後要重建 | 10 |
| Service Pack（SP） | 服務更新包 | 同一版本的累積更新，例如 12.1 SP4 | 1、17 |

### B.2.2 專案、資料庫與權限

| 英文（縮寫） | 中文 | 一句話解釋 | 主要章節 |
|---|---|---|---|
| Project | 專案 | 一組資料庫的集合，以三字元代碼識別 | 2 |
| Dabacon | Dabacon 資料庫引擎 | PDMS 系產品的樹狀資料庫引擎 | 1、2 |
| Databank | 船體 Databank | 承襲 Tribon 的船體資料存放方式 | 1、6、15 |
| DB（Database） | 資料庫 | 專案中的一個資料單位，由一個 Team 擁有 | 2 |
| SYST | 系統資料庫 | 記錄使用者、Team、DB、MDB 定義的資料庫 | 2 |
| DESI | 設計資料庫 | 存放設計模型（SITE、ZONE、設備、管路等） | 2、3 |
| CATA | 目錄資料庫 | 存放目錄元件與等級 | 2、8 |
| PADD | 圖面資料庫 | 存放舾裝圖面 | 2、9 |
| DICT | 字典資料庫 | 存放 UDA、UDET 定義 | 2、3 |
| PROP | 性質資料庫 | 存放材料性質 | 2、8 |
| ISOD | Isodraft 資料庫 | 存放 ISO 圖樣式設定 | 2、9 |
| Team | 團隊 | 擁有 DB 的群組；成員才能寫入該 DB | 2 |
| User | 使用者 | 登入帳號，屬於一或多個 Team | 2 |
| MDB（Multiple Database） | 多資料庫組合 | 登入時掛載的 DB 清單與順序，決定看得到什麼 | 2 |
| Current DB／Deferred DB | 目前／延後的 DB | MDB 中本次開啟或暫不開啟的 DB〔Marine 用語待核對〕 | 2 |
| Multiwrite | 多寫入 | 允許多人同時寫入同一 DB，以認領協調 | 2 |
| Claim | 認領 | 修改元素前取得的元素層級鎖定 | 2、12 |
| Implicit Claim | 隱式認領 | 修改時系統自動認領 | 2 |
| Explicit Claim | 顯式認領 | 必須先執行 `claim` 才能修改 | 2 |
| Unclaim／Release | 釋放 | 把認領的元素交還給其他人 | 2 |
| Session | Session | 每次 Savework 在 DB 中產生的版本紀錄 | 2 |
| Savework | 儲存工作 | 把自己的修改寫入 DB，等同 commit | 2、12 |
| Getwork | 取得工作 | 重新讀取 DB，看到別人已儲存的變更 | 2、12 |
| Merge Changes | 合併變更 | 管理員合併 Session 以縮小 DB | 2 |
| Extract | 衍生資料庫 | 從 Master DB 衍生的子 DB，類似 Git 分支 | 2 |
| Flush | 寫回 | 把 Extract 的變更寫回 Master〔命令名稱待核對〕 | 2 |
| Global | 多地點同步 | 跨地點複製與同步 DB 的機制 | 2 |
| Primary Location | 主要地點 | Global 環境中唯一可寫入某 DB 的地點 | 2 |

### B.2.3 資料模型、元素與屬性

| 英文（縮寫） | 中文 | 一句話解釋 | 主要章節 |
|---|---|---|---|
| Element | 元素 | 資料庫樹中的一個節點 | 3 |
| Element Type | 元素型別 | 元素的類別，決定屬性與合法成員 | 3 |
| Attribute | 屬性 | 元素的欄位 | 3 |
| Owner | 擁有者 | 元素在樹中的父節點 | 3 |
| Member | 成員 | 元素在樹中的子節點，有順序 | 3 |
| Legal Owner／Legal Member | 合法擁有者／合法成員 | 資料模型規定某型別可以放在哪裡、可以包含什麼 | 3 |
| CE（Current Element） | 目前元素 | 命令列的游標，多數命令預設作用在它上面 | 3、12 |
| DBREF | 資料庫參照 | 元素的內部識別，例如 `=12345/678` | 3、12 |
| Reference Attribute | 參照屬性 | 存放另一元素 DBREF 的屬性，相當於外鍵 | 3 |
| Pseudo Attribute | 偽屬性 | 查詢時才計算、不存在資料庫中的屬性 | 3 |
| UDA（User Defined Attribute） | 使用者自訂屬性 | 公司在 Lexicon 定義的擴充欄位，名稱以 `:` 開頭 | 3 |
| UDET（User Defined Element Type） | 使用者自訂元素型別 | 公司在 Lexicon 定義的元素型別 | 3 |
| Word | Word 型別 | 最多 4 或 6 個大寫字元的代碼型屬性值 | 3 |
| WORLD | 根元素 | 每個 DB 樹的根 | 3 |
| SITE | 場區 | 最上層的管理分區 | 3 |
| ZONE | 區域 | 第二層管理分區，可巢狀 | 3 |
| EQUI | 設備 | 設備元素，含基本體與管嘴 | 3、7 |
| SUBE | 子設備 | 設備底下的分組 | 3、7 |
| NOZZ | 管嘴 | 設備上與管路連接的接口 | 3、7 |
| PIPE | 管線 | 管路的主要元素 | 3、7 |
| BRAN | 分支 | 管線的組成單位，有 Head 與 Tail | 3、7 |
| Head／Tail（HREF／TREF） | 起點／終點參照 | 分支兩端連接的元素 | 3、7 |
| STRU | 結構 | 鐵舾裝結構的主要元素 | 3、7 |
| FRMW／SBFR | 框架／子框架 | 結構的組成單位 | 3、7 |
| SCTN | 型鋼 | 結構中的型鋼構件 | 3、7 |
| PANE | 板 | 結構中的板構件 | 3、7 |
| HVAC | 通風 | 通風風管的主要元素 | 3、7 |
| HBLWLD | 船體分段世界 | E3D 2.1 資料模型中船體分段的上層元素 | 3、5 |
| BLOCK | 分段 | 船體分段元素，包含板架 | 3、5 |
| HPANEL | 平面板架 | 平面船體建模的基本元素 | 3、5 |
| CPANEL | 曲面板架 | 曲面船體的板架元素 | 3、5 |
| HPLATE | 板 | 平面板架中的板 | 3、5 |
| HSTIFF | 加強材 | 平面板架中的加強材 | 3、5 |
| HBRCKT | 肘板 | 平面板架中的肘板 | 3、5 |
| HSEAM | 接縫 | 把板架切成多塊板的線 | 3、5 |
| TBID | Tribon ID | 船體元素對應的 Tribon 識別碼屬性 | 3、15 |
| NAME／TYPE／OWNER／MEMBERS | 名稱／型別／擁有者／成員 | 所有元素共通的系統屬性 | 3 |
| DESC／PURP／FUNC | 描述／用途／功能 | 常見的一般屬性 | 3 |
| SPRE | 等級元件參照 | 設計元件指向等級元件（SPCO）的外鍵 | 3、8 |
| PSPE | 管線等級 | 管線或分支使用的等級 | 3、8 |
| CATR | 目錄參照 | 等級元件指向目錄元件的外鍵 | 3、8 |
| ATTLIS／ATTOUT／UDALIS／PSATTS | 屬性清單偽屬性 | 分別列出一般屬性、`Q ATT` 顯示的屬性、UDA、偽屬性 | 3 |
| WVOL | 世界包圍盒 | 元素在世界座標中的包圍盒偽屬性 | 3、18 |

### B.2.4 座標與幾何

| 英文（縮寫） | 中文 | 一句話解釋 | 主要章節 |
|---|---|---|---|
| E／N／U | 東／北／上 | 舾裝世界座標的三個方向 | 4 |
| X／Y／Z | 船舶座標 | X 向艏、Y 向左舷、Z 向上 | 4 |
| POS（Position） | 位置 | 元素相對於擁有者的位置 | 4 |
| ORI（Orientation） | 姿態 | 元素局部座標軸的朝向，例如 `Y is N and Z is U` | 4 |
| Direction | 方向 | 不含位置的指向，例如 `N 45 E` | 4 |
| WRT（With Respect To） | 相對於 | 指定以哪個元素的座標系表示位置 | 4 |
| P-point（PPOS） | 連接點 | 元件上的連接點，例如 `PPOS(1)` | 4、8 |
| FR（Frame） | 肋位 | 沿船長方向的肋骨位置編號 | 4、5 |
| LP（Longitudinal Position） | 縱向位置 | 縱向構件的 Y 或 Z 方向位置編號 | 4、5 |
| AP（Aft Perpendicular） | 艉垂線 | 船舶座標原點常用的參考位置 | 4 |
| CL（Centre Line） | 中心線 | Y = 0 的船舶縱向中線 | 4 |
| Port／Starboard（PS／SB） | 左舷／右舷 | Y > 0 為左舷，Y < 0 為右舷 | 4 |
| Mould Plane | 型面 | 板架所在平面，也是板架的局部座標平面 | 4、5 |
| RSO（Reference Surface Object） | 參考面物件 | 初始設計建立的參考面，用於定位 | 4、5 |
| POSITION／DIRECTION／ORIENTATION／LINE／PLANE | PML 幾何物件 | PML2 中表示點、方向、姿態、直線、平面的物件 | 4、11 |
| AID | 輔助圖形 | 在 3D 視圖畫臨時圖形，用於除錯 | 4、17 |
| Bore | 口徑 | 管路的公稱尺寸，可與距離採用不同單位 | 4、7 |

### B.2.5 船體與舾裝業務

| 英文（縮寫） | 中文 | 一句話解釋 | 主要章節 |
|---|---|---|---|
| Planar Panel | 平面板架 | 位於一個平面上的船體結構單位 | 5 |
| Curved Panel | 曲面板架 | 外板等曲面構件組成的板架 | 5 |
| Boundary | 邊界 | 板架的封閉外輪廓 | 5 |
| Seam／Butt | 接縫／對接縫 | 板與板之間的分界 | 5 |
| Stiffener | 加強材 | 貼在板上的型材 | 5 |
| Bracket | 肘板 | 構件交接處的補強板 | 5 |
| Flange | 折邊 | 板緣的折邊 | 5 |
| Notch | 缺口 | 切入外輪廓的去除區，例如焊道避讓孔 | 5 |
| Cutout | 切口 | 讓穿越型材通過的開口 | 5 |
| Hole | 開孔 | 位於板內部的封閉開孔 | 5、18 |
| Topology | 拓撲參考 | 以參考其他構件描述位置的建模方式 | 5 |
| Scheme | 建模描述 | 以文字描述板架定義的形式 | 5 |
| Block | 分段 | 船體建造時的分段單位 | 5、6 |
| Part Generation | 零件抽出 | 從模型產生板零件與型材零件 | 6 |
| Nesting | 套料 | 把零件排在鋼板上以提高利用率 | 6 |
| Profile Sketch | 型材草圖 | 型材加工用的草圖 | 6 |
| Shrinkage Compensation | 收縮補償 | 預先補償焊接收縮量 | 6 |
| P&ID | 管路儀表圖 | 管路系統的邏輯圖 | 7 |
| Spool | 管段 | 工廠預製的管路單位 | 7、9 |
| Penetration | 貫穿孔 | 管路、風管、電纜穿過船體結構的開孔 | 7、18 |
| Clash Check | 干涉檢查 | 檢查物件之間的重疊或侵入 | 7 |
| Catalogue | 目錄 | 元件的參數化定義 | 8 |
| Specification（Spec） | 等級 | 某系統允許使用的元件清單與選擇條件 | 8 |
| SPEC／SELE／SPCO | 等級／選擇／等級元件 | 等級的三層元素 | 8 |
| CATA／SECT／CATE／SCOM | 目錄／區段／類別／目錄元件 | 目錄的階層元素 | 8 |
| GMSE／PTSE | 幾何集／點集 | 目錄元件的參數化幾何與連接點定義 | 8 |
| DEPT／REGI／DRWG／SHEE／VIEW | 部門／登記／圖／圖紙／視圖 | 舾裝圖面的階層元素 | 9 |
| Representation | 表現規則 | 決定模型在圖面上如何呈現的規則 | 9 |
| MTO（Material Take-Off） | 材料表 | 由模型產生的材料數量清單 | 9、16 |

### B.2.6 開發技術

| 英文（縮寫） | 中文 | 一句話解釋 | 主要章節 |
|---|---|---|---|
| PML（Programmable Macro Language） | PML | AVEVA 內嵌的腳本語言 | 10、11 |
| PML1／PML2 | PML1／PML2 | 早期以巨集與字串替換為主／物件導向的新版 PML | 11 |
| Macro（`.pmlmac`） | 巨集 | 依序執行的命令檔 | 10、11 |
| Function（`.pmlfnc`） | 函式 | 以 `define function` 定義的全域函式 | 10、11 |
| Form（`.pmlfrm`） | 表單 | 以 `setup form` 定義的 GUI | 10、13 |
| Object（`.pmlobj`） | 物件 | 以 `define object` 定義的自訂型別 | 10、11 |
| Gadget | 控制項 | 表單上的按鈕、文字框、清單等 | 13 |
| Callback | 回呼 | 使用者操作控制項時執行的動作 | 13 |
| Add-in | 外掛 | 掛進系統選單與工具列的擴充功能 | 13、14 |
| COLLECTION | 收集物件 | 在範圍內依型別與條件找元素的 PML 物件 | 12 |
| Handle | 錯誤處理 | `handle ... endhandle` 攔截錯誤 | 11、17 |
| PML.NET | PML.NET | 讓 PML 呼叫 .NET 類別的機制 | 14 |
| CAF（Common Application Framework） | 通用應用程式框架 | .NET Add-in 的外掛架構 | 14 |
| `IAddin` | Add-in 介面 | .NET 外掛主類別實作的介面 | 14 |
| `ServiceManager` | 服務管理器 | .NET 外掛取得系統服務的入口 | 14 |
| UIC | 介面自訂檔 | 定義選單與工具列的檔案 | 14 |
| `DbElement`／`DbAttribute` | .NET 資料庫類別 | .NET API 中代表元素與屬性的類別 | 14 |
| Vitesse | Vitesse | 船體模組的 Python 2.6 腳本環境 | 15 |
| `kcs_*` 模組 | Vitesse 模組 | 例如 `kcs_ui`、`kcs_draft`、`kcs_dex` | 15 |
| Data Extraction | 資料抽取 | 以 `kcs_dex` 讀取船體資料的機制 | 15 |
| PML Publisher | PML 加密工具 | 加密 PML 原始碼以便發佈 | 17 |
| Alpha log | 命令列日誌 | 把命令列輸出錄到檔案 | 17 |

## B.3 指令速查

以下指令在命令列（Command Window）輸入，不分大小寫。範例名稱（如 `/P-101`）請換成訓練專案中的實際名稱。

標示說明：

- 未標示：寫法出自 AVEVA E3D 2.1 官方參考手冊、本課程開源範例或論文實際程式。
- 〔待核對〕：PDMS／Marine 常見寫法，尚未在官方頁面或實機確認。
- 〔寫入〕：會修改資料，只能在訓練專案中使用。

### B.3.1 查詢屬性

| 指令 | 用途 | 狀態 | 章節 |
|---|---|---|---|
| `Q NAME` | 查詢 CE 的名稱 | 常見用法〔待核對輸出格式〕 | 3 |
| `Q TYPE` | 查詢 CE 的型別 | 同上 | 3 |
| `Q OWNER` | 查詢 CE 的擁有者 | 同上 | 3 |
| `Q MEMBERS` | 列出 CE 的成員 | 〔待核對，可能可縮寫為 `Q MEM`〕 | 3 |
| `Q ATT` | 列出 CE 的一般屬性（不含偽屬性與隱藏屬性） | 官方（DBRM，ATTOUT 清單） | 3 |
| `Q DESC`、`Q PURP`、`Q FUNC` | 查詢一般屬性 | 常見用法 | 3 |
| `Q POS` | CE 相對於擁有者的位置 | 官方（SCRM） | 4 |
| `Q POS OF /EQUIP1` | 指定元素相對於其擁有者的位置 | 官方（SCRM） | 3、4 |
| `Q POS WRT /*` | CE 的世界座標 | 官方（SCRM） | 4 |
| `Q POS WRT /MYBRAN` | 以指定元素座標系表示的位置 | 官方（DBRM） | 4 |
| `Q PPOS(1) WRT /MYBRAN` | 第 1 個連接點的位置 | 官方（DBRM） | 4 |
| `Q ORI` | CE 的姿態 | 常見用法 | 4 |
| `Q SPRE` | 等級元件參照 | 常見用法 | 3、8 |
| `Q NAME OF CREF`、`Q NAME OF SPRE` | 沿參照屬性查詢對方的屬性 | 〔待核對〕 | 3 |
| `Q ATTLIS`、`Q UDALIS`、`Q PSATTS` | 列出一般屬性、UDA、偽屬性清單 | 官方（DBRM 定義的偽屬性） | 3 |
| `Q :VENDOR` | 查詢 UDA（名稱為示意） | 〔待核對〕 | 3 |
| `Q WVOL` | 世界座標包圍盒 | 論文實際程式使用 `WVOL of` | 3 |
| `Q LASTMOD(ATTNAME XLEN)` | 某屬性的最後修改資訊 | 官方（AVEVA Engineering 文件）；Marine〔待核對〕 | 2、3 |
| `Q CUTLENGTH` | 型鋼切割長度（偽屬性） | 官方（DBRM 範例）；屬性縮寫〔待核對〕 | 3 |
| `Q LIST` | 列出 CE 的合法成員型別 | 〔待核對〕 | 3 |
| `Q REF` | 查詢 CE 的 DBREF | 〔待核對〕 | 3 |
| `Q (N 100 WRT /BOX1)` | 計算位置表示式 | 官方（SCRM） | 4 |

### B.3.2 導覽（移動 CE）

| 指令 | 用途 | 狀態 | 章節 |
|---|---|---|---|
| `/P-101` | 依名稱移到元素 | 常見用法 | 3 |
| `=12345/678` | 依 DBREF 移到元素 | 〔待核對〕 | 3 |
| `END` | 移到擁有者 | 〔待核對〕 | 3 |
| `NOZZ 1`、`ELBO 3` | 移到 CE 底下第 n 個該型別成員 | 〔待核對〕 | 3 |
| `NEXT`、`PREV`、`FIRST`、`LAST` | 同層或成員間移動 | 〔待核對〕 | 3 |
| `GOTO SPRE` | 沿參照屬性移動 | 〔待核對〕 | 3 |
| `!!ce = !elem` | PML2 中設定 CE | 常見 PML2 寫法 | 12 |

### B.3.3 環境、使用者與工作階段

| 指令 | 用途 | 狀態 | 章節 |
|---|---|---|---|
| `q evar PMLLIB` | 查詢環境變數 | 開源範例使用 | 1、10 |
| `q user` | 目前使用者 | 〔待核對〕 | 2 |
| `q mdb` | 目前 MDB | 〔待核對〕 | 2 |
| `q dbname` | 元素所在 DB | 〔待核對〕 | 2 |
| `claim /P-101` | 認領元素〔寫入前置〕 | 常見用法〔語法細節待核對〕 | 2、12 |
| `unclaim /P-101` | 釋放元素 | 〔待核對〕 | 2、12 |
| `savework` | 儲存修改並產生 Session | 常見用法 | 2、12 |
| `getwork` | 取得他人已儲存的變更 | 常見用法 | 2、12 |

### B.3.4 修改資料（僅限訓練專案）

| 指令 | 用途 | 狀態 | 章節 |
|---|---|---|---|
| `DESC 'text'` | 設定 CE 的描述 | 〔寫入〕常見用法 | 3、12 |
| `POS E 1000 N 2000 U 300` | 設定位置 | 〔寫入〕常見用法 | 4、12 |
| `ORI Y is N and Z is U` | 設定姿態 | 〔寫入〕常見用法 | 4、12 |
| `BY E 100` | 相對移動 | 〔寫入〕〔待核對〕 | 4 |
| `NEW EQUI /NAME` | 建立新元素 | 〔寫入〕〔建立位置規則待核對〕 | 12 |
| `DELETE EQUI` | 刪除元素 | 〔寫入〕〔語法與相依檢查待核對〕 | 12 |

### B.3.5 PML 管理與除錯

| 指令 | 用途 | 狀態 | 章節 |
|---|---|---|---|
| `pml rehash all` | 重建所有 PMLLIB 目錄的索引記憶 | 官方文件主題（Rebuilding All PML File Indexes）；開源範例使用 | 10 |
| `pml index` | 為目錄產生 `pml.index` | 〔待核對〕 | 10 |
| `pml reload form !!myform` | 重新載入修改過的表單 | 〔待核對〕 | 13、17 |
| `show !!mycollect` | 顯示表單 | 開源範例使用 | 13 |
| `$m /path/macro.pmlmac` | 執行巨集 | 常見用法〔路徑寫法待核對〕 | 11 |
| `$P text` | 在命令列輸出文字 | 常見用法 | 11、17 |
| `$!x` | 在命令中展開變數 | 常見用法 | 11 |
| `$R+`、`$R-` | 開啟／關閉 PML 追蹤 | 〔追蹤層級參數待核對〕 | 11、17 |
| `q var !x` | 查詢變數型別與內容 | 常見用法 | 11、17 |
| `alpha log /file.txt`、`alpha log end` | 把命令列輸出錄到檔案 | 〔待核對〕 | 17 |
| `aid sphere $!pos dia 200` | 在 3D 視圖畫輔助球 | 論文實際程式使用 | 4、17 |
| `aid line $!p1 to $!p2` | 在 3D 視圖畫輔助線 | 論文實際程式使用 | 4、17 |

### B.3.6 PML2 程式中常見的對應寫法

| 命令列 | PML2 程式（示意） | 說明 |
|---|---|---|
| `Q NAME` | `!n = !!ce.name` | 取值而不是印出 |
| `Q OWNER` | `!o = !!ce.owner` | 回傳 DBREF |
| `Q MEMBERS` | `!m = !!ce.members` | 回傳 DBREF 陣列 |
| `Q POS OF /P-101` | `!p = object DBREF('/P-101').pos` | 不移動 CE |
| `Q ATT` | `!a = !!ce.attributes()` | 使用 ATTLIS 清單〔方法名稱待核對〕 |
| `/P-101` | `!!ce = object DBREF('/P-101')` | 移動 CE |

## B.4 常見縮寫一覽

| 縮寫 | 全稱 | 中文 |
|---|---|---|
| CE | Current Element | 目前元素 |
| DB | Database | 資料庫 |
| DBREF | Database Reference | 資料庫參照 |
| MDB | Multiple Database | 多資料庫組合 |
| UDA | User Defined Attribute | 使用者自訂屬性 |
| UDET | User Defined Element Type | 使用者自訂元素型別 |
| WRT | With Respect To | 相對於 |
| FR | Frame | 肋位 |
| LP | Longitudinal Position | 縱向位置 |
| AP | Aft Perpendicular | 艉垂線 |
| CL | Centre Line | 中心線 |
| PS／SB | Port Side／Starboard | 左舷／右舷 |
| P&ID | Piping and Instrumentation Diagram | 管路儀表圖 |
| ISO | Isometric Drawing | 等角管段圖 |
| MTO | Material Take-Off | 材料表 |
| NC | Numerical Control | 數值控制（切割機） |
| CAF | Common Application Framework | 通用應用程式框架 |
| PML | Programmable Macro Language | AVEVA 腳本語言 |
| RSO | Reference Surface Object | 參考面物件 |
| SP | Service Pack | 服務更新包 |

## B.5 資料來源

- AVEVA E3D 2.1 DBRM：Query Attributes（ATTLIS、ATTOUT、UDALIS、PSATTS）：<https://help.aveva.com/AVEVA_Everything3D/2.1/DBRM/DBRM3.04.09.html>
- AVEVA E3D 2.1 DBRM：Pseudo Attributes：<https://help.aveva.com/AVEVA_Everything3D/2.1/DBRM/DBRM1.02.17.html>
- AVEVA E3D 2.1 DBRM：Relative Positions, Directions, Orientations：<https://help.aveva.com/AVEVA_Everything3D/2.1/DBRM/DBRM3.04.14.html>
- AVEVA E3D 2.1 SCRM：Positions、WRT：<https://help.aveva.com/AVEVA_Everything3D/2.1/SCRM/SCRM6.5.17.html>、<https://help.aveva.com/AVEVA_Everything3D/2.1/SCRM/SCRM6.5.18.html>
- AVEVA E3D 2.1 DMRM：Zone、HPANEL、HBRCKT、BLOCK 元素頁：<https://help.aveva.com/AVEVA_Everything3D/2.1/DMRM/DMRM5.09.082.html>、<https://help.aveva.com/AVEVA_Everything3D/2.1/DMRM/DMRM5.09.406.html>、<https://help.aveva.com/AVEVA_Everything3D/2.1/DMRM/DMRM5.09.393.html>、<https://help.aveva.com/AVEVA_Everything3D/2.1/DMRM/DMRM5.09.288.html>
- AVEVA Engineering 線上文件：偽屬性限定詞：<https://docs.aveva.com/bundle/engineering/page/911892.html>
- AVEVA Hull and Outfitting 12.1 線上文件入口：<https://docs.aveva.com/bundle/hull-and-outfitting/page/1224159.html>
- 開源範例 aveva-marine-dev-skill（MIT 授權）：<https://github.com/912141548/aveva-marine-dev-skill>
- Kim, Park & Yang (2020), JAMET 44(3)，CC BY-NC 開放取用：<https://doi.org/10.5916/jamet.2020.44.3.196>
