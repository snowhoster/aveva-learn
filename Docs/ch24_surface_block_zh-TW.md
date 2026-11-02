# 第 24 章　曲面管理與分區：Surface Manager、Block Division 與多視圖專案

> 船殼、艏側推器隧道、錨管這類曲面，是船體模型的「地基」；而把早期的大模型切成能生產的分段，則是從設計走向生產的「分水嶺」。這一章把兩件看似不相干的事放在一起談：**曲面進得來、檢查過、放得出去（Surface Manager）**，以及**模型切得下去、放進正確的分段、設計與生產兩個視圖不脫節（Block Division 與 Multi-View Project）**。
>
> 兩者的共同點是「拓撲正確性」：曲面有縫、板架邊界對不上，下游的交線、體積、套料全部會出問題。很多團隊的麻煩不在建模技巧，而在匯入的曲面沒有先檢查、分段切完才發現偏移量設錯、或不了解設計視圖與生產視圖其實是同一個模型的兩種看法。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 官方離線文件的三個模組：*Surface Manager*（約 22 頁）、*Block Division*（約 22 頁）與 *Multi-View Project*（約 10 頁）。操作名稱、選單、參數與限制以官方原文為準，內容以自己的話重組成教學順序。官方文件沒有寫的部分（版本差異、實際檔案格式細節、批次指令語法、授權與模組啟用條件、效能數字）一律標為〔待核對〕，未編造任何指令或檔案格式。官方圖片均為文件截圖，僅供內部教學；部分截圖畫面風格較舊，介面細節以你實際安裝的版本為準。第 5 章（船體建模）已介紹過分段劃分的概念與設計／詳細設計視角，第 6 章（生產資訊）談零件抽出與套料，本章聚焦「操作層」，不重複那兩章的內容。

## 24.1 學習目標

讀完本章，你應該能夠：

1. 說明 Surface Manager 在曲面流程中的位置，以及為什麼曲面需要先檢查再使用。
2. 認得 Surface Manager 的視窗元件，並說明 Hull Surfaces 與 Primitive Assemblies 兩個區域的差別。
3. 區分 Workspace（`.tbw`）與 Scene 的用途，並使用 Scene Template 重複使用顯示設定。
4. 說明 Import from File、Import from Project、Release Surface、Export to File 與 Export to BLines File 的資料流向與限制。
5. 依用途選擇 Analyze、Combine、Sew、Optimize、Restrict、Mirror、Intersect Surface 與 Compare Surfaces 等操作。
6. 說明 Block Division 的三種用途，以及來源面板、切割器（Cutter）與目標分段（Target Block）三項輸入。
7. 依步驟完成一個 Block Divide Job：建立、選面板、Verify、套用切割器、Divide、排序（Sort）、檢查結果。
8. 設定目標分段的標稱框與偏移量，避免面板落入錯誤分段或同時被兩個分段包含。
9. 說明 Design View／Production View、Design Block／Production Block 的關係與建立專案的規則。
10. 說明二次開發者可以在哪些地方接上這些流程，以及哪些部分文件沒有提供依據。

## 24.2 全章地圖

| 主題 | 解決的問題 | 輸入 | 輸出 | 本章節 |
|---|---|---|---|---|
| Surface Manager | 外部曲面不乾淨、不能直接建模 | STEP／SAT／IGES／DML 或 Marine 專案曲面 | 檢查、修補過的 Hull Surface，釋放到設計專案 | 24.3–24.4 |
| Block Division | 早期模型要切成生產分段 | 來源面板、切割器、目標分段 | 新的生產面板、排進正確分段 | 24.5–24.6 |
| Multi-View Project | 設計與生產對模型的需求不同 | Design Block／Panel | 同一模型的兩個視圖與其連接 | 24.7 |

> **專業提醒：** 三個模組的前後關係是「曲面（船殼）進得來 → 結構以船殼為邊界建模 → 在設計視圖完成大板架 → Block Divide 產生生產面板」。曲面的品質問題，會一路傳到分段切割之後；所以曲面檢查要在最前面做，而不是等 Block Divide 出錯才回頭。

## 24.3 Surface Manager：曲面的健檢中心

### 24.3.1 為什麼需要它

官方的說法是：AVEVA Marine 對雕刻曲面（sculptured surface）做的是數學運算，例如求交線與產生體積。這類運算要求曲面「拓撲正確」，才能在設計與生產得到正確結果。Surface Manager 提供匯入、檢查、驗證，以及某些情況下修復曲面的工具，且不論曲面從哪個系統來。

它的內部模型是 **Brep（Boundary Representation，邊界表示）**：幾何由一組修剪過的 NURBS 曲面（trimmed NURBS surfaces）組成，並以邊界彼此相連。跨系統傳遞複雜形狀時，最常見的問題包含針狀小面（needle face）、退化面（degenerated face）與過大的間隙，會讓匯入的模型不適合繼續建模。

官方也點出三個實務用途，可以當作導入這個工具的理由：

| 用途 | 說明 |
|---|---|
| 檢查與修復匯入曲面 | 偵測缺陷，能修的就修，降低之後建模工具失敗的風險 |
| 只分享需要的部分 | 船殼曲面可能含有造船廠想保留的細節，要給分包商時可只輸出相關區域 |
| 減少平坦區域的補片 | 外部系統常在平坦區產生大量補片，影響求交等運算效能，可合併以提升整體效能 |

### 24.3.2 介面元件

Surface Manager 啟動後是一個整合式應用程式視窗：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Surface Manager 預設視窗：左側 Workspace Explorer 的模型樹、中間圖形視窗、右側導覽工具列、底部訊息視窗

*圖 24-1　Surface Manager 的預設版面。左為模型樹，中為圖形視窗，右為導覽工具列，底部是顯示 Complexity 統計的訊息視窗。（AVEVA 官方文件截圖，僅供內部教學）*

| 元件 | 用途 |
|---|---|
| Application Frame（應用程式框架） | 把所有視窗收在同一個框架內，可自由拖曳排列 |
| Graphics Window（圖形視窗） | 顯示目前 Scene 的內容；導覽工具在右側工具列 |
| Workspace Explorer（工作區總管） | 兩個頁籤式樹狀檢視：Models（匯入的模型）與 Scenes（場景），預設停靠左側 |
| Model View（模型視圖） | 檢視匯入的模型及其結構；可選取後拖曳到圖形視窗，或以右鍵選單呼叫功能 |
| Scenes View（場景視圖） | 檢視已建立的場景及其中的 model drop；右鍵可新增、設為目前、刪除、改屬性 |
| Message Window（訊息視窗） | 位於底部，顯示工具輸出與錯誤／資訊訊息 |
| Auxiliary Model View（輔助模型視圖） | 在樹的任一節點分出第二棵樹，一邊看細節一邊保留總覽 |

圖形視窗中的邊線顏色是判讀曲面品質的第一線索，值得記住：

- 面（face）以著色曲面顯示。
- 剛好被兩個面共用的邊畫成**黃色**；其餘的邊畫成**藍色**。
- 曲面內部出現藍色邊，表示相鄰的面沒有連起來。常見原因是來源檔案中它們本來就沒連接，或間隙太大。
- 小黑點是頂點位置。

> 〔公開版未收錄：AVEVA 官方產品截圖〕一個船艏／艏樓風格的曲面，黃色線為共用邊、藍色線為外邊界，黑點為頂點

*圖 24-2　Brep 曲面的邊線表示法。黃色為正好連接兩個面的邊，藍色為邊界邊（位於曲面內部時代表有未連接的接縫）。（AVEVA 官方文件截圖，僅供內部教學）*

沒連起來的邊可以縫合（Sew）：間隙小時直接連接；間隙稍大時，先略為放大內部公差再連接。

### 24.3.3 模型樹：Hull Surfaces 與 Primitive Assemblies

模型樹分成兩個主要區域，用法類似，但目的不同：

| 區域 | 適合 | 匯入時的樹結構 |
|---|---|---|
| Hull Surfaces | 準備釋放（Release）到設計專案的船殼曲面 | 組裝樹被**壓平** |
| Primitive Assemblies | 較一般的模型（例如外購設備、參考幾何） | 組裝樹**保留** |

> 〔公開版未收錄：AVEVA 官方產品截圖〕模型樹：Hull Surfaces 下有 HULL 與 Prim001；Primitive Assemblies 下保留多層組裝與面清單

*圖 24-3　模型樹範例。Hull Surfaces 區是一條船殼曲面（內含 Primitive），Primitive Assemblies 區保留匯入檔案的組裝階層，往下可展開到個別 Face。（AVEVA 官方文件截圖，僅供內部教學）*

階層從上到下是：曲面（Hull Surface）→ Primitive → Faces（面）。後面所有操作對象，都在這個階層裡選。

### 24.3.4 Workspace 與 Scene

**Workspace（工作區）** 是一次作業中「匯入的模型加上建立的 Scene」的集合，存檔後就像目前作業的快照。

| 動作 | 做法 |
|---|---|
| 新增 | 工具列 New，或 `File > New` |
| 開啟 | Open Workspace 圖示或 `File > Open Workspace`（目前的工作區會關閉，以所開啟的內容建立新的） |
| 儲存 | Save Workspace 圖示或 `File > Save Workspace`，存成 `<workspace name>.tbw` |

**Scene（場景）** 是一組模型物件，加上你選擇的顯示方式（旋轉、角度、透視視點）。永遠有一個 Scene 是目前的（current），也就是圖形視窗所顯示的那個。系統預設兩個 Scene：

| Scene | 設定 |
|---|---|
| Browse0 | Browse 型：新模型加入前，先移除場景中所有模型 |
| Normal0 | 一般型 |

Scene 的屬性以屬性頁（property pages）呈現，Box Filter 除外（它是獨立指令與對話框）。幾個重點：

- **Model Type Filter：** 限制只顯示某些型別的模型。注意必須先選到父模型，才看得到子模型。設定在 Type Filter 屬性頁。
- **Scene Template：** 把一個設定好的 Scene 另存成範本，之後新建場景時套用。每個 Scene 都以某個範本為基礎，系統有兩個預設範本。範本只含基本屬性（場景型別、呈現選項、篩選設定），不含暫時性的內容（模型選取、限制框、已存的相機位置）。
- 範本預設存放位置依作業系統而定，官方列出的 Vista／Windows 7 路徑為 `%AppData%\AVEVA\SurfaceManager\SceneTemplates.dat`（官方原文寫成 `[Drive]:\Users\<user>\AppData\Roaming\AVEVA\SurfaceManager\SceneTemplates.dat`）。較新的 Windows 版本路徑是否相同〔待核對〕。

Scene 工具列的常用工具：

| 工具 | 作用 |
|---|---|
| New Scene | 以預設範本快速建立 Scene；從 Scenes 的右鍵選單選 New 可改用其他範本 |
| Previous／Next Scene | 切換到上一個／下一個 Scene |
| Box Selection Filter | 定義選取框，只有框內或部分在框內的模型才會被加入 Scene |
| Save as Scene Template | 在 Scene 右鍵選單中，把該 Scene 存成範本（要填名稱與說明） |

> **專業提醒：** 曲面檢查常常要反覆「只看這一小塊」。與其每次手動隱藏，不如建立一個 Browse 型 Scene 加 Box Filter，再存成範本，之後同類曲面直接套用。

### 24.3.5 顯示與導覽

顯示模型的方式很單純：從模型樹把一個或多個項目**拖曳**到圖形視窗。一般以 Primitive 為單位加入；若要在畫面上單獨選取某些面，可改拖曳 Primitive 底下的 `Faces` 節點，變成逐面加入。

導覽工具集中在右側工具列。操作規則：選一個工具後，游標變成該工具的形狀，直到你選別的工具為止；移動時，方向與速度由「按下位置」與「目前游標位置」的距離決定，放開按鍵就停。無論目前工具為何，滑鼠滾輪永遠可縮放。

| 類別 | 工具 | 操作重點 |
|---|---|---|
| 選取 | Select | 單擊或框選；按住 Ctrl 加選；選取的模型會高亮 |
| 縮放 | Auto Scale、Zoom Window、Zoom and Pan | Auto Scale 讓模型適配視窗且不改變目前工具；Zoom Window 按右鍵拖曳框；Zoom and Pan 上下為縮放、左右為平移 |
| 移動 | Slide、Spin、Walk、Tilt | Spin 的旋轉中心是按下當下游標下最近的模型點；Walk 只能搭配透視相機；Tilt 繞視圖中心旋轉 |
| 相機 | Save／Restore Camera、Perspective Camera | 存取視角；在透視與平行相機之間切換 |
| 標準視角 | Top、Frame（看 AFT／FOR）、Side（看左舷）、Isometric（看 AFT／FOR） | 一鍵適配並切換到標準方向 |
| 量測 | Simple Measuring | 點選模型顯示座標；按住拖曳到另一點顯示兩點距離 |

快速鍵（官方表格；官方把 Save Camera 誤寫成 `Cltr+S`，應為 Ctrl+S，此處依合理推測更正，建議實機確認〔待核對〕）：

| 功能 | 快速鍵 |
|---|---|
| Auto Scale | Ctrl+A |
| Zoom to Model | Ctrl+B |
| Restore Camera | Ctrl+E |
| Zoom Window | Ctrl+I |
| Walk | Ctrl+M |
| Spin | Ctrl+R |
| Save Camera | Ctrl+S |
| Slide | Ctrl+T |
| 切換到下一個／上一個視窗 | F6／Shift+F6 |
| 全螢幕與一般模式切換 | F11 |

多數模型項目共用一組**通用指令**（在樹或圖形視窗選取後按右鍵）：

| 指令 | 用途 |
|---|---|
| New Window from Here | 把右鍵點到的節點設為輔助樹的新根；`View > Auxiliary Tree` 可切換顯示 |
| Hide／Unhide | 在圖形視圖隱藏或再顯示項目 |
| Select in View | 快速縮放到選取的項目（即使該項目目前不在圖形視窗內） |
| Rename | 改項目名稱（模型項目或 Scene 皆可） |
| Delete | 刪除模型項目（船殼曲面、Primitive、Face、Scene 或 Scene 內容） |

### 24.3.6 匯入、釋放與匯出

這是 Surface Manager 與外界的界面，也是二次開發者最關心的部分，所以獨立整理成一張流向表。

| 動作 | 來源 → 目的 | 支援格式／限制 |
|---|---|---|
| Import from File | 檔案 → Hull Surfaces 或 Primitive Assemblies | STEP 203、SAT、IGES、DML（Initial Design Hull Forms 的原生格式）；可一次選多檔，也可從 Windows 檔案總管拖曳檔案到樹節點 |
| Import from Project | Marine 專案中的船殼曲面 → Surface Manager | 第一次使用匯入／釋放功能時要選專案；**本次作業內專案不能更換** |
| Release Surface | Hull Surfaces 中的曲面（含所屬曲線）→ Marine 設計專案 | 只能從 Hull Surfaces 區直接釋放 |
| Release Surface as Symmetric | 同上，但在資料庫中標記為對稱 | 對稱曲面**不得跨越中心線** |
| Export to File | 單一曲面／Primitive 或整個階層 → 單一檔案 | STEP、IGES 或 SAT |
| Export to BLines File | 曲面與曲線資料 → Lines／PACE 可接續編修的 blines 檔 | 含完整曲線資訊與資料點；資料點以近似方式產生，與原曲線誤差在固定 0.5 mm 容差內 |

三個容易踩到的規則：

1. **從專案匯入、再釋放到另一個專案：** 因為專案在一次作業內固定，官方給的步驟是：先從專案 A 匯入船殼曲面 → 儲存 Workspace → 重啟 Surface Manager 並開啟剛存的 Workspace → 釋放到專案 B。
2. **Primitive Assemblies 區的 Primitive 不能直接釋放。** 做法是把它拖到 Hull Surfaces 節點建立新曲面，用 Rename 取好名字，再釋放。
3. **曲面含多個 Primitive 時只釋放第一個。** 釋放前須先用 Combine 把它們併成單一 Primitive（見下一節）。

### 24.3.7 曲面與 Primitive 的操作

官方把這些工具定位為「找出並（可選地）修復匯入幾何的缺陷或弱點」。

| 操作 | 用途 | 重點 |
|---|---|---|
| Analyze | 報告相連曲面網格中的幾何間隙 | 超過整體模型容差的間隙記為「曲面事件（surface incident）」並加到被分析的 Primitive；稍大於曲面容差者為 warning，更大者為 error |
| Combine | 把屬於同一 Hull Surface 的所有 Primitive 併成單一 Primitive | 釋放前必做（若有多個 Primitive） |
| Intersect Surface | 以一個或多個平面切曲面，產生曲線 | 曲線與被切模型存在一起，名稱由 prefix、曲線型別與主座標值組成 |
| Mirror | 把原模型與其對中心線的鏡像合併成新模型 | 原模型不得跨越中心線 |
| Optimize | 提高模型品質 | 合併平面面，並把部分退化曲面換成較不易出問題的曲面 |
| Restrict | 移除落在指定軸向對齊方盒（axis-aligned box）之外的部分 | 可用來只取要分享或要檢查的區域 |
| Sew | 把拓撲分離但幾何相鄰的面縫合 | 縫合時整體 Primitive 容差可能會放大 |
| Compare Surfaces | 以取樣點計算曲面與另一曲面（或外部取樣點）的距離 | 偏差超過相交容差（通常 0.5 mm）的點進入新資料夾與報告 |
| Combine Curves（選單） | 合併端點距離小於 10 mm 的曲線 | 大於 10 mm 則操作失敗 |
| Connect Curves（工具列） | 為 Lines／PACE 準備：以直線段連接曲線端點 | 結果有多條分支時，連接最靠近的端點；有歧義時連接靠近選取點的端點 |

**Intersect Surface 的欄位：**

> 〔公開版未收錄：AVEVA 官方產品截圖〕Intersect by Plane 對話框：Curve prefix、Starting point、Direction and distance、Ending point

*圖 24-4　Intersect Surface 對話框。Curve prefix 為曲線名稱前綴；Direction and distance 的向量方向是切割平面法向、長度是相鄰平面的間距；只要 Ending point 仍在目前切割平面「前方」就持續產生曲線。（AVEVA 官方文件截圖，僅供內部教學）*

| 欄位 | 說明 |
|---|---|
| Curve prefix | 曲線名稱的前半段 |
| Starting point | 第一個切割平面上的一點 |
| Direction and distance | 切割平面的法向量；向量長度就是連續切割平面之間的距離 |
| Ending point | 只要終點還在目前切割平面前方，就繼續產生新的交線 |

**Compare Surfaces 的兩種模式：**

- **曲面對曲面：** 在 Hull Surfaces 中選兩個曲面，右鍵選 Compare Surface；對話框可調整比較區域與取樣點密度。取樣點取自「先選的那個」，拿去和「後選的那個」比。
- **曲面對外部取樣點：** 選單一曲面，右鍵選 Surface Compare，讀入外部取樣點檔。把產生的偏差資料夾拖進圖形視圖，每個偏差以「取樣點、曲面上最近點、連線」表示，線長與距離成正比，顏色代表偏差範圍。

> **專業提醒：** Compare 是「曲面搬家有沒有走樣」的驗收工具。例如從別的船體系統搬進 AVEVA 後，用取樣點確認偏差都在 0.5 mm 容差內，再開始建模，比建完才發現船殼偏掉便宜得多。

### 24.3.8 附錄：取樣點檔（Sample Points）

官方附錄描述一個從 TRIBON M3 環境產生取樣點檔的外部程式（程式名稱 `sj708`）：它以 surface server 對原生曲面或 NAPA 曲面切出剖面與水線，對切出的曲線擬合雙圓弧（bi-arc），取雙圓弧的起訖點當取樣點，輸出檔供 Surface Manager 的 Compare Surface 讀取。官方註明：此程式不含在標準安裝內，需洽原廠本地支援取得。

執行 `sj708` 時需提供的資料：

| 提示項目 | 說明 |
|---|---|
| 輸出檔完整路徑與檔名 | 取樣點檔的存放位置 |
| 曲面檔所在資料夾（dml 或 dms） | 若專案已設 `SB_NAVARCH`，或使用 NAPA 曲面則不會詢問 |
| 曲面名稱 | 要取樣的曲面 |
| 剖面與水線的範圍 | AFT、FWD、下限、上限 |
| 切割間距 | 相鄰切割的距離 |

雙圓弧擬合使用曲面求交的預設容差（通常為 0.5 mm）。官方範例檔的欄位排列如下，這是目前文件中**唯一**有依據的檔案格式描述，可供二次開發者讀寫（欄位含義依官方註解，編碼與換行格式〔待核對〕）：

| 行（依序） | 含義 |
|---|---|
| 曲面名稱（範例 `SPHULL`） | Surface name |
| 容差（範例 `0.500`） | Intersection tolerance |
| 平面型別（範例 `1`） | 官方註解為「Plane x=1, y=2, z=3」，即 1 表示 x 平面 |
| 平面座標（範例 `-3997.767`） | Plane coordinate |
| 切割產生的輪廓數 | Number of contours resulting from cut |
| 輪廓內取樣點數（範例 `23`） | Number of sample points in contour |
| 其後每行三個數值 | 取樣點座標（x、y、z）；範例中相鄰兩點在輪廓連接處會重複出現，原因官方未說明〔待核對〕 |

> **常見錯誤（Surface Manager）：**
> 1. 匯入後直接釋放，沒有 Analyze：曲面事件留到建模才爆發。
> 2. 曲面含多個 Primitive 卻沒有 Combine：只有第一個 Primitive 進設計專案，其餘無聲消失。
> 3. 對稱曲面跨過中心線卻選了 Release Surface as Symmetric。
> 4. 想直接從 Primitive Assemblies 釋放。
> 5. 在同一次作業中想換專案：必須存檔、重啟、再開啟 Workspace。
> 6. 以為 Sew 沒有代價：縫合可能放大整體 Primitive 容差，之後要再用 Analyze 確認。

## 24.4 二次開發者怎麼接：Surface Manager 的整合點

官方 Surface Manager 文件**只描述互動式 GUI**，沒有提供 PML 指令、.NET API 或命令列參數。以下依「文件有依據」與「需要自行核對」分開寫：

| 整合點 | 依據 | 做法／限制 |
|---|---|---|
| 曲面檔（STEP 203、SAT、IGES、DML）進出 | 文件明列 | 外部系統（CAD、NAPA 等）以這些標準格式交換；對外輸出只想給局部時，先 Restrict 再 Export to File |
| blines 檔 | 文件明列 Export to BLines File | 供 Lines／PACE 續編；格式細節文件未提供〔待核對〕 |
| 取樣點檔 | 文件有範例（24.3.8） | 格式簡單，可由自家程式產生；用於 Compare Surface 驗收 |
| Workspace（`.tbw`） | 文件明列副檔名 | 內部格式文件未提供；不建議自行解析〔待核對〕 |
| Scene Template（`SceneTemplates.dat`） | 文件明列路徑 | 內部格式未提供；可整檔複製分發給團隊，作為標準顯示設定 |
| 自動化／批次操作 | 文件**未提及** | 是否有腳本介面、命令列或 API〔待核對〕；不要假設可用 |
| 與 Marine 專案的連接 | Import from Project／Release | 以專案資料庫為界面；釋放後在 Marine 內的物件結構請參考第 5 章與你的專案設定 |

> **專業提醒：** 沒有官方 API 的情況下，最穩當的自動化切入點是「檔案介面」：用程式驗證輸入檔（副檔名、大小、必要欄位）、規範檔案命名、整理交付清單，並把 Surface Manager 的 Analyze 結果截圖或訊息視窗輸出存檔，作為品質紀錄。不要試圖自行解析專有二進位檔。

## 24.5 Block Division：把早期模型切成生產分段

### 24.5.1 它是什麼、用在哪裡

Block Division（Block Divide）是結構設計的重要功能，主要用途是把早期模型細分成面向生產的模型。主要輸入有三類：**來源面板（Source Panels）、切割器（Cutters）、目標分段（Target Blocks）**。第 5 章已介紹「分段是造船廠的建造單位」這個概念，本章只講如何操作。

官方列出三種用途：

| 用途 | 說明 | 原面板的下場 |
|---|---|---|
| 把一個分段分成兩個或更多分段 | 從原分段的面板產生新面板 | 原面板刪除，原分段變空 |
| 由設計模型產生生產模型 | 來源為 Design Block、目標為 Production Block，以切割器從設計面板切出生產面板 | 設計面板**保持完整** |
| 把面板分類進分段 | 以上兩種的特例，**不使用切割器** | 只搬移（可能改名） |

主要活動是三件事：**面板選取（Panel Selection）→ 切割（Cutting）→ 排序（Sorting）**。

### 24.5.2 切割與排序的規則

**面板選取：** 來源面板通常透過分段選取，但一般面板選取工具的選項都可使用，平面與曲面面板皆可。前提是所選面板必須能無錯誤地通過 `Verify`，否則不能參與流程。

**切割：** 可定義多個切割器，每個切割器與所有選定面板比對，相交者被切成兩塊。切割器類型：

| 切割器類型 | 說明 |
|---|---|
| Principal planes（主平面） | 任意 X、Y、Z 平面 |
| RSO | 取得多平面或有限範圍平面的方式 |
| Shell Block Seams | 標為 Block Seam 的平面殼縫 |
| Stored planes | 資料庫中已儲存的命名平面 |
| Design Panel Block Seams | 設計面板上預先定義的 Block Seam，當生產面板由設計面板產生時使用；幾何可任意，包含圓弧半徑 |

> 注意：**曲面面板只能使用平面切割器。** 此時切割器先建立一條 Shell Block Seam，再以它切曲面面板的殼板與殼加強材。

**排序：** 把面板從選定面板搬到目標分段，處理兩種面板：切割產生的新面板，以及剛好落在切割器之間的面板。規則：

- 若分段名稱是面板名稱的一部分，排序時面板會依目標分段改名。
- 面板**完全位於**某個目標分段內，才會被搬進去；不在任何目標分段內者，留在來源分段。
- 設計分段切成生產分段時，設計面板留在設計分段，並與生產面板建立連接（見 24.7）。
- 由設計面板產生、卻不在任何指定生產分段內的生產面板，無法放回來源設計分段，會落入系統自動建立的**預設生產分段**，名稱為來源分段名前加 `_P`。

### 24.5.3 邊界產生、特殊形狀與元件處理

面板被切割器切開時，兩個新邊界由原邊界與切割器定義推導而成。這並不簡單，因為切割器與周圍邊界的相交方式，可能不同於原邊界各界限彼此相交的方式。必要時系統會自動為平面面板的新邊界補上額外的限制方盒值（例如 `XMAX`、`YMIN`）。

兩個特殊情況：

- **大開孔：** 一個含大開孔的平面面板被兩個平行切割器橫跨開孔切過時，中間的面板會有兩塊分離的板區，系統會在孔內自動加一條縫。
- **U 形面板：** 一般平面面板要能被分割，切割器與面板邊界必須恰好兩個交點；但水平切割 U 形面板的情形有特別處理，結果是**三塊**面板，而不是兩塊。

> 〔公開版未收錄：AVEVA 官方產品截圖〕U 形面板被水平切開，產生三塊面板

*圖 24-5　U 形面板的特殊情形。切割器水平切過 U 形，結果是三塊面板（開口兩側各一塊與底部一塊），而非常規的兩塊。（AVEVA 官方文件截圖，僅供內部教學）*

面板內的元件在切割時依型別分四類處理，這是理解「切完之後少了什麼、多了什麼」的關鍵：

| 類別 | 元件 | 處理方式 |
|---|---|---|
| Atomic（原子） | Bracket、Pillar、Doubling plate、Tap | 為實體零件，必須完整地出現在其中一塊新面板；跨過切割器時只放進其中一塊 |
| Sharable（可共用） | Hole、Notch、Cutout、Excess、Compensation、Shrinkage | 屬於特徵或屬性，可加到單一或多塊新面板（跨過切割器時） |
| Cuttable（可切割） | Seam、Plate、Stiffener、Flange、Welding、Marking | 完整落在某塊就原樣加入；跨過切割器就切成兩半並修改定義後保存 |
| Referred（被引用） | Topological point、Curve、Plane | 只有被其他元件引用時才加到某塊新面板 |

**Block Seam 的特性：** Block Seam 只存在於沒有生產資料的設計面板上，但可以拿來「傳遞生產資料」到生產面板的邊界：在 Block Divide 之前先於 Block Seam 設定 bevel（坡口）與 excess（餘裕），這些值就會在分割過程套用到生產面板的邊界。

> **專業提醒：** 切割後最容易被誤解的是 Atomic 與 Cuttable 的差別：肘板（Bracket）不會被切成兩半，而是整個放進其中一塊；加強材（Stiffener）則會被切斷，並另受「最小加強材長度」與端部處理（24.6.4）的規則影響。檢查時別把「肘板在邊界上」當成錯誤。

### 24.5.4 驗證結果與反覆分段

結果主要看來源與目標分段的內容：

- 兩者**同型**（同為設計或同為生產），且目標分段吻合切割器並涵蓋來源分段的體積，成功後來源分段應該是**空的**。
- 來源是設計分段、目標是生產分段時，設計面板會保留；每個設計面板都會得到一個或多個對應生產面板。若目標分段沒涵蓋整個來源體積，剩下的生產面板放入預設生產分段。
- 新面板名稱依內建規則由原面板推導；若分段名稱是面板名稱的一部分，會被換成目標分段名稱。
- 最後仍應以 `Verify` 功能確認新面板沒問題。

**反覆分段（Iterative Block Division）：** 可把來源分段當成「信箱」使用。設計分段已被切成生產分段後，仍可往設計分段加新的設計面板；用**相同輸入**再跑一次 Block Divide，只有新加的設計面板會被處理。同型分段之間也一樣：往已清空的來源分段加入新面板再跑一次，這些面板會被切並加到目標分段。

## 24.6 Block Division 的操作

### 24.6.1 目標分段與切割器：先把「盒子」規劃好

官方一再強調：目標分段與切割器的定義是**分開**的，系統不檢查兩者是否一致。因此你要自己確保：切割器與目標分段吻合、目標分段涵蓋所選面板的範圍、相鄰分段之間有合理的重疊。

定義分段時，可給一個**標稱方盒（nominal box）**與六個面的偏移量（offset）；特殊情況可對任一面另指定限制物件。官方建議：相鄰分段的標稱方盒面「相接」，然後在每一面加偏移；標稱方盒也要對應 Block Divide 用的切割器。

偏移量的取捨：要大到足以收納例如延伸到面板板緣之外的加強材，又要小到不讓任何面板完全落入多個目標分段。兩個典型案例：

**案例一：切割平面落在肋骨平面，切過甲板面板。** 偏移必須包住延伸到面板外的加強材：後方分段的前緣要包住加強材（通常幾百 mm），前方分段的後緣偏移可較小。

> 〔公開版未收錄：AVEVA 官方產品截圖〕肋骨平面切割示意：紅線為切割平面，虛線為含偏移的分段盒

*圖 24-6　切割平面在肋骨平面時的分段盒偏移。紅線是切割器，不同顏色的虛線代表相鄰兩個分段含偏移後的範圍。（AVEVA 官方文件截圖，僅供內部教學）*

**案例二：切割平面就在甲板平面上，且甲板要歸下方分段。** 偏移必須更小：上方分段的下限不得包住整個甲板，但仍要包住站在甲板上的面板（通常要大於板厚、小於型材高度）；下方分段的上限要包住甲板，偏移略大於最大板厚即可，不必更多。

> 〔公開版未收錄：AVEVA 官方產品截圖〕切割平面在甲板平面時的分段盒偏移

*圖 24-7　切割平面在甲板平面時的偏移設定。上方分段的下限只略低於甲板，避免把甲板整塊包進去。（AVEVA 官方文件截圖，僅供內部教學）*

官方給的規則：

- 兩種案例的偏移**都不得小於** Block Divide 中設定的最小加強材長度（minimum stiffener length）。
- 更複雜的情況，通則是考慮最小板寬、最小加強材長度與加強材延伸到面板外的量，去決定偏移。
- 仍有面板進錯分段時，可用 Rename 功能（可同時設定面板名稱與分段）把它搬到另一分段。

| 設定項 | 建議 |
|---|---|
| 標稱方盒 | 相鄰分段的面相接，並與切割器位置一致 |
| 偏移 | 大於加強材外延與板厚的需要，但不使面板完全落在兩個分段內 |
| 重疊 | 要「明確」：每個面板只能唯一歸屬一個分段 |
| 驗證 | 目標分段要用 Verify 確認可存取且可修改 |

### 24.6.2 介面：Block Division 視窗與樹狀流程

按選單中的 `Block Divide...` 按鈕，會出現 Block Division 視窗（若尚未存在），內有樹狀檢視。所有功能都透過右鍵彈出選單，在視窗空白處或樹節點上呼叫。

樹狀檢視的設計理念是把流程分步驟，用節點狀態顯示進度；使用者可在每一步檢查結果，也可在過程中增刪面板、切割器與目標分段。

重要規則：

- 所有放進流程的模型物件**都必須先通過 Verify** 才能繼續。
- 任何修改模型物件的操作，都會自動寫入資料庫。因此流程進行中仍可修改模型物件，但樹中已記錄的物件**不應被刪除**。
- 官方建議：開始 Block Divide 之前先執行 `Save Work`，建立模型物件的基準點（baseline）。
- 面板可從樹拖到圖形畫布檢視：逐一拖，或拖父節點成組（例如全部選定面板、某切割器節點下的全部面板）。

### 24.6.3 Job：建立與設定

視窗為空時唯一可用的功能是 `New Job`，會開啟 `Create Job` 表單，內有自動產生、可修改的作業名稱，之後在多視圖專案中可設定所處理的面板型別（單視圖專案此區塊呈灰色不可選），最後選擇是否加入 Cutters 與／或 Target Blocks 節點。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Create Job 表單：Name、Job Type（Production Panels to Production Panels／Design Panels to Design Panels）、Add Cutters、Add Target Blocks

*圖 24-8　Create Job 表單。Job Type 有「生產面板到生產面板」與「設計面板到設計面板」兩種，單視圖專案此區為灰階；Configuration 勾選是否加入 Cutters 與 Target Blocks 節點。（AVEVA 官方文件截圖，僅供內部教學）*

接受設定後，樹中出現 Job 節點與子節點，子節點的順序固定，對應典型流程；但文件說明使用者仍可用別的順序操作，某些情況可藉此得到不同結果。節點上的綠色圖示表示目前沒問題。**Selected Objects 與 Logs 為必要節點；Cutters 與 Target Blocks 視作業而定為選用。**

Job 節點的右鍵選單有 `Add`（補加 Cutters／Target Blocks 節點）、`Setup`（整體控制參數）、`Delete`（刪除整個 Job）。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Job Setup 對話框：Minimum plate width、Minimum stiffener length、Allow symmetrical Panels in Block pairs、Include warnings in Verify Log

*圖 24-9　Job Setup。畫面上的預設值為最小板寬 50、最小加強材長度 100（單位依官方畫面，文件未明說，視為 mm〔待核對〕）。（AVEVA 官方文件截圖，僅供內部教學）*

| 設定 | 說明 |
|---|---|
| Minimum plate width | 能形成新面板的最小板條；切割後若有一塊板窄於此值，**該次切割被忽略** |
| Minimum stiffener length | 加強材切割後若有一段短於此值，**加強材不被切**，整根歸於其中一塊面板 |
| Allow symmetrical Panels in Block pairs | 即使排進左右舷兩個分段，也維持面板對稱。兩個分段須以共同字根命名，左舷尾加 `P`、右舷尾加 `S`，且不得存在名稱等於該共同字根的分段 |
| Include warnings in Verify Log | 警告也寫入 Verify 紀錄；但此時警告必須修正後，面板才能繼續在 Block Divide 中處理 |

### 24.6.4 各節點的功能

**Selected Objects（選取物件）：** 右鍵功能為 `Add`、`Verify`、`Remove`。

- `Add`：用一般面板選取工具挑面板，重複使用會累加；`Remove` 一次清除所有已選面板。
- 選取後圖示變為藍色問號（未驗證）；執行 `Verify` 後，通過者變綠色勾，失敗者為紅色驚嘆號。
- 失敗原因列在 `Logs` 節點下。處理方式二擇一：修正模型錯誤，或把該面板排除。樹中多數節點（包含每個面板節點）都有 `Delete`；問題解決、驗證通過後，圖示轉為綠勾。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Block Division 樹狀視窗：Selected Objects 下 BDR4-1 驗證失敗、BDR4-2 通過；Logs 下列出失敗訊息

*圖 24-10　驗證失敗的 Job。Selected Objects 中的 BDR4-1 為紅色驚嘆號，原因列在 Logs 的 Verify Selected Objects 下（例如缺少拓撲物件、指定標記的加強材不存在）。重新執行 Verify 並修正後，紀錄會被清除。（AVEVA 官方文件截圖，僅供內部教學）*

**Cutters（切割器）：** 節點右鍵有 `Add`、`Offset`、`Delete`。切割器共四種來源（官方此頁列「Principal planes、RSO、shell block seams、stored panels」，與前述「Stored planes」可能是用詞差異，以實機畫面為準〔待核對〕），皆從清單挑選。

定義後的切割器有自己的右鍵選單：

> 〔公開版未收錄：AVEVA 官方產品截圖〕Cutter 右鍵選單：Find Panels、Apply、Offset...、Divide、Delete

*圖 24-11　切割器節點的右鍵選單。典型順序是 Find Panels、Apply、Divide；Offset 為選用。（AVEVA 官方文件截圖，僅供內部教學）*

| 功能 | 作用 |
|---|---|
| Find Panels | 檢查所有選定面板，與切割器相交者加到該切割器節點下 |
| Apply | 在找到的平面面板上建立暫時縫、在曲面面板上建立殼縫（由切割器與面板的交線而來）；套用後面板以簡化方式繪製、暫時縫被強調，節點旁出現藍色 Tag 符號 |
| Offset | 設定加強材端部偏移（可對所有切割器、單一切割器，甚至切割器下的單一面板） |
| Divide | 真正把面板切成兩塊；切割器節點下不再有面板，Selected Objects 持有全部結果面板 |
| Delete | 刪除切割器；若其下仍有已 Apply 的面板則**不能刪** |

使用時要記住：

- 套用前可決定「不對稱方式被切到的對稱面板」要保持對稱還是拆成左右各一。例如已有 Y=8000 的切割器、又會定義 Y=-8000 的切割器時，保持對稱可能較有利。
- 可定義多個切割器，但一個切割器 Apply 之後，必須先 Divide，才能對另一個切割器重複同樣步驟。

**加強材端部（Offset 功能）：** 被切斷的加強材端部可指定 shift（位移）、slant（斜切）與 notch（缺口）；組合型材（built profile）另可設 flange shift 與 flange notch。shift 與 slant 以 mm 為單位，notch 取自 endcut 表中的缺口。

> 〔公開版未收錄：AVEVA 官方產品截圖〕加強材端部示意：Shift、Slant、Notch、Flange notch、Flange shift 的位置關係

*圖 24-12　加強材切斷端的各項參數。Shift 與 Slant 為端部位置與斜切量，Notch 為腹板側缺口，Flange shift 與 Flange notch 只適用於組合型材。（AVEVA 官方文件截圖，僅供內部教學）*

這些對話框的值會轉換成一組連接碼（connection code）與端切碼（endcut code，可帶參數）：

| 項目 | 官方說明 |
|---|---|
| 可用的 shift 值 | 由環境變數 `SBH_CONCODES` 所指向的檔案控制；必須定義配對碼，一個為正 shift、一個為負 shift（間隙） |
| 預設端切型別 | 11、21、31 |
| 需要額外端切型別時 | 用預設關鍵字 `PAN_SPLIT_ECUT_FLATBAR`、`PAN_SPLIT_ECUT_BULB_LBAR`、`PAN_SPLIT_ECUT_TBAR`、`PAN_SPLIT_ECUT_BUILT_TBAR` 設定 |

官方給的設定範例（逐字保留，因為是設定值，不是說明文字）：

```text
PAN_SPLIT_ECUT_FLATBAR    = 11,12
PAN_SPLIT_ECUT_BULB_LBAR  = 21,22
PAN_SPLIT_ECUT_TBAR       = 31,32
PAN_SPLIT_ECUT_BUILT_TBAR = 130,131,140,141
```

這些關鍵字寫在哪個設定檔、檔案位置與載入方式，官方這一頁沒有說明〔待核對〕；請與你的系統管理員（參考[第 20 章](ch20_system_administration_zh-TW.reading.html)）確認。

**Target Blocks（目標分段）：** 收集切割後面板要放入的分段。**若不給目標分段，面板留在原分段。** 右鍵有 `Add`（從清單挑分段）、`Verify`（確認分段可存取且可修改）、`Sort`、`Delete`。

- `Sort`：比對 Selected Objects 下的全部面板與目標分段，**只要面板完全在某目標分段內就搬過去**。排序前先出現對稱處理確認表單：第一個勾選項與 Job Setup 相同；第二個控制「左右舷面板各落在兩個不成對的不同分段時，是否拆開對稱」。
- 切割器與目標分段盒不吻合時，「先切還是先排」會得到兩種不同結果：**先排序再切**，完全落在某目標分段的面板已被移出 Selected Objects 子節點，所以不會被切；**先全部切再排序**，凡與切割器相交的選定面板都會被切。也可以混合，以得到想要的結果。
- `Delete` 會移除 Target Blocks 節點，但**不會還原**已完成的排序。

**Logs：** 放驗證面板或分段時的錯誤訊息；排除問題後重新執行 Verify，紀錄會被清掉。

### 24.6.5 一個典型 Job 的操作順序

下列步驟是依官方各節點描述整理出的**標準流程**；其中並非每一步都是強制順序（官方說明可自由調整順序）：

1. 在 Block Divide 前先執行 `Save Work`，建立基準點。
2. 按 `Block Divide...`，於空視窗右鍵選 `New Job`，確認名稱、Job Type 與是否加入 Cutters／Target Blocks。
3. 對 Job 節點選 `Setup`，設定最小板寬、最小加強材長度與對稱選項。
4. 在 Selected Objects 選 `Add` 選取來源面板（通常經由分段），再執行 `Verify`；處理 Logs 中的失敗項。
5. 在 Cutters 選 `Add` 挑選切割器；若需要，用 `Offset` 設定加強材端部。
6. 對每個切割器依序：`Find Panels` → `Apply` → 拖到圖形視窗檢查暫時縫 → `Divide`。
7. 在 Target Blocks 選 `Add` 挑選目標分段，`Verify`，再 `Sort`。
8. 檢查結果：來源分段是否清空（同型分段）、設計面板是否都有對應生產面板、預設生產分段（`_P`）是否出現意外面板、新面板用 `Verify` 確認。
9. 有誤放的面板，用 Rename 同時改面板名稱與分段。

> **專業提醒：** 切割與排序的順序會影響結果。若目標分段盒與切割器對得很齊，兩種順序結果相同；一旦不齊，順序就成為「參數」。團隊內應先約定標準順序並寫進作業指引，而不是由每位使用者憑感覺決定。

> **常見錯誤（Block Division）：**
> 1. 目標分段沒涵蓋來源面板的全部範圍：剩餘面板落入 `_P` 預設生產分段（設計到生產的情況）或留在來源分段。
> 2. 偏移量小於最小加強材長度，或大到讓面板同時完全落入兩個分段。
> 3. 在樹中已登錄的物件被刪除，導致節點與資料庫不一致。
> 4. 沒先 Save Work，切壞了沒有基準可回。
> 5. 對曲面面板使用非平面切割器：曲面面板只能用平面切割器。
> 6. 忘了切割器 Apply 後要先 Divide 才能處理下一條切割器。
> 7. 對稱分段命名不符規則（字根加 `P`／`S`），或存在與字根同名的分段。
> 8. 把 Verify 失敗的面板當成沒事，繼續往下。

### 24.6.6 二次開發者怎麼接：Block Division

| 整合點 | 依據 | 說明 |
|---|---|---|
| 背景（批次）執行 | 官方一句話：Block Division 可在 batch process 執行，詳見 *Batch Utilities* | 本章資料來源未包含 Batch Utilities 頁面，指令語法與輸入檔格式〔待核對〕；請先讀該章，不要自行推測 |
| 環境變數 `SBH_CONCODES` | 文件明列 | 指向連接碼檔，控制可用的 shift 值；與部署／設定管理相關 |
| 預設關鍵字 `PAN_SPLIT_ECUT_*` | 文件明列四個 | 可由設定管理或部署工具統一發布 |
| 結果驗證 | 文件描述的檢查準則 | 可寫成檢查腳本：來源分段應為空、每個設計面板應有對應生產面板、預設生產分段應為空等；實際查詢資料庫的方法請見[第 12 章](ch12_pml_database_zh-TW.reading.html)，並在訓練專案驗證 |
| 作業紀錄 | Logs 節點 | 圖形介面上的驗證紀錄；是否可匯出成檔案〔待核對〕 |

> **專業提醒：** 文件沒有提供「用 PML 或 .NET 直接呼叫 Block Divide」的依據。若想做自動化，現階段較有把握的是：（1）批次執行（待依 Batch Utilities 確認）；（2）事前驗證（面板能否通過 Verify、目標分段是否存在且可寫）；（3）事後檢查（上述準則）。不要編造 PML 指令。

## 24.7 Multi-View Project：同一模型的兩個視圖

### 24.7.1 為什麼需要兩個視圖

早期設計階段的重點是把模型定義到足以滿足強度等功能需求，並能以可接受的精度算出鋼重與焊接長度。後期則要提供製造零件與組合裝配所需的全部資訊。兩個階段對「船體模型的視圖」要求不同，於是有了 Multi-View Project：

| 視圖 | 面板特性 | 分段特性 |
|---|---|---|
| Design View（設計視圖） | 大面板、**沒有**生產細節 | 少數幾個分段 |
| Production View（生產視圖） | 完整生產細節 | 依製造需求組織的分段 |

Multi-View 是一個**選項**；一般的單視圖（Single View）環境仍可使用。設計視圖與生產視圖是「同一個船體產品模型的兩個視圖」，兩者同時存在，使用者選擇由哪個視圖進入模型。在完整建立的模型中，設計視圖的分段或面板，在生產視圖中有對應的分段或面板。（官方註明：除非另有說明，本章所稱面板皆指平面面板。）

切換視圖用一個模式開關：設計視圖只顯示設計分段與設計面板，生產視圖只顯示生產分段與生產面板；所有圖形檢視與分段／面板清單都遵守這個規則。**Hull Detail Design 永遠使用並看到生產視圖；Outfitting 可自由選擇顯示與參照哪個視圖。**（Outfitting 參見[第 7 章](ch07_outfitting_zh-TW.reading.html)。）

### 24.7.2 設計面板與生產面板、設計分段與生產分段

| 關係 | 說明 |
|---|---|
| 生產面板 → 設計面板 | 每個生產面板**連到單一**設計面板 |
| 設計面板 → 生產面板 | 一個設計面板可以由**多個**生產面板表示（專案進展到該階段後） |
| 生產分段 → 設計分段 | 每個生產分段連到單一設計分段，且該設計分段必須**包住**它 |
| 設計分段 → 生產分段 | 一個設計分段可以參照多個生產分段 |

設計面板與生產面板其實是**各自獨立的物件**，只是系統自動維護兩者的連接。設計面板的修改會反映到其生產面板，反之亦然：這是自動的，但受使用者控制。例如設計面板修改並提交（commit）後，連接的生產面板被啟用時會提示使用者是否接受更新。

> 〔公開版未收錄：AVEVA 官方產品截圖〕設計面板（左）與其三塊生產面板（右）的雙向連接

*圖 24-13　設計面板與生產面板的對應。左側為一塊大的設計面板，右側為它被分割後的三塊生產面板，雙向箭頭代表系統維護的連接；設計面板上的紅色加強材會在生產面板上對應。（AVEVA 官方文件截圖，僅供內部教學）*

設計與生產的連接也代表**空間上的一致**：設計分段參照涵蓋同一空間的生產分段，生產分段參照包住它的設計分段；設計面板被切成生產面板後，兩者佔據同一空間並代表產品模型的同一部分。設計面板內的元件，依型別與位置，在生產面板中可能由「某一塊的一個元件」或「多塊的多個元件」表示（對照 24.5.3 的四類元件）。

### 24.7.3 建立 Multi-View 專案

| 情況 | 規則 |
|---|---|
| 判定 | 專案含**至少一個** Design Block 即為 Multi-View；若存在的分段都不是設計分段，就是一般專案 |
| 新專案 | 由**第一個建立的分段**決定型態：先建 Design Block 則成為 Multi-View；先建 Production Block（一般分段）則成為一般專案 |
| 初期內容 | 新的 Multi-View 專案先只有設計分段與設計面板 |
| 進入生產階段 | 模型在某區域準備好後，建立生產分段，並用 Block Divide 產生生產面板（見 24.5–24.6） |
| 建立限制 | Design Block／Panel 只能建在 Multi-View 專案；Multi-View 內的生產分段／面板都必須連到設計分段／面板 |
| 直接建立生產面板 | 在 Multi-View 專案中建立生產面板時，系統自動在連接的設計分段內建立一份複製的設計面板當作對應 |

**轉換既有專案：** 官方提供特殊工具（文件指向 *Create/Remove Design Blocks and Panels*，本章來源未涵蓋，指令與步驟〔待核對〕），可把一般專案轉成 Multi-View，或轉回單視圖。轉換時：建立設計分段，把既有分段連到這些設計分段而成為真正的生產分段，並為每個（生產）面板建立設計面板複製；之後使用者可把設計面板複製合併，產生較大的設計面板，例如甲板與縱向艙壁。

> 〔公開版未收錄：AVEVA 官方產品截圖〕左：許多小塊的生產面板；右：合併後的大設計面板

*圖 24-14　轉換既有專案。左為既有的許多小面板（成為生產面板，每個複製成設計面板），右為合併後的大設計面板，適合早期設計階段使用。（AVEVA 官方文件截圖，僅供內部教學）*

### 24.7.4 設計與生產的連接細節

**Block Seam：** 只出現在設計面板的特殊元件，代表「設計面板如何被分成生產面板」。它在用於從設計視圖產生生產視圖的 Block Division 之前或過程中建立。修改一條已有連接生產面板的 Block Seam 時，比一般縫多了限制：

- 不可移動到越過另一條 Block Seam。
- 與其他 Block Seam 的**相交數量必須保持**：不能有原有相交消失，也不能出現新的相交（相交位置當然可以移動）。
- 刪除 Block Seam 只能用 `Remove Seam` 功能，受影響的生產面板會**兩兩自動合併**。

**面板邊界：** 設計面板分割成生產面板時，生產面板的邊界完全由設計面板邊界與其 Block Seam 決定。因此生產面板的邊界被所連的設計面板完全約束：每個邊界界限不是對應設計面板的邊界界限，就是對應某條 Block Seam（該縫可能被多個生產面板的邊界界限引用）。所以**生產面板的邊界定義不能修改**；例外是 Multi-View 專案中直接建立的生產面板（設計面板是一對一的複製），其邊界可修改，並讓設計面板配合調整。

**生產資料：** 設計面板**不帶**生產資料，由生產面板持有。設計面板被細分之後再修改設計面板，更新生產面板時不會破壞已加在生產面板上的生產資料。例如透過設計面板改某些加強材的斷面，其對應生產面板上加強材已定義的 bevel 會被保留。官方列為生產資料的包括：

| 類別 | 項目 |
|---|---|
| 工藝加工 | bevel（坡口）、weld（焊接）、excess（餘裕）、marking（打標）、taps、grinding（研磨）、surface treatment（表面處理）、shrinkage compensation（收縮補償） |
| 識別與管理 | position numbers（位置編號）、general purpose strings（通用字串）、workshop destination（車間去向）、raw plate name（原板名） |

這與[第 6 章](ch06_hull_production_zh-TW.reading.html)談的零件生產資訊互相呼應：生產資料不放在設計視圖，是為了讓早期設計能隨意改動而不污染已投入的生產設定。

> **專業提醒：** 把 Multi-View 想成「設計面板是藍圖、生產面板是施工單」。藍圖改了要通知施工單，但施工單上的加工資料（坡口、餘裕）不能因藍圖改了就被洗掉；這正是官方設計成「更新不破壞生產資料」的原因。

> **常見錯誤（Multi-View）：**
> 1. 以為設計面板可以帶生產資料：它不帶，生產資料只在生產面板。
> 2. 在 Multi-View 專案內想修改由設計面板切出的生產面板邊界：不允許，要改設計面板或 Block Seam。
> 3. 在已有連接的 Block Seam 上做「越過另一條縫」或「改變相交數量」的修改。
> 4. 在一般專案內想建立 Design Block：只有 Multi-View 專案能建。
> 5. 第一個建立的分段型別選錯，專案型態就此決定（要改需用轉換工具）。
> 6. Hull Detail Design 使用者以為可以切回設計視圖：它永遠使用生產視圖。

### 24.7.5 二次開發者怎麼接：Multi-View

文件對 Multi-View 的描述是概念與限制，**沒有提供**可程式化的屬性名稱或指令。可以確定的事實有：判定規則（至少一個 Design Block）、視圖開關是模式開關、轉換用特殊工具、更新連接時會提示使用者接受。下列則〔待核對〕：

- 設計／生產分段與面板在資料庫中的型別名稱與連接屬性。
- 視圖切換在 PML 或 .NET 中是否有對應物件／指令。
- 轉換工具是否有批次執行方式。

> **專業提醒：** 在還不知道屬性名稱前，不要寫依賴猜測欄位的程式。建議先在訓練專案用 Hull Detail Design 或你的瀏覽工具觀察 Design 與 Production 分段的屬性差異，再把觀察到的結果寫成內部文件，並標註版本。

## 24.8 把三個模組串起來：一個完整的情境

假設一個外購曲面船殼要進入專案，並完成到生產分段：

| 階段 | 動作 | 對應章節 |
|---|---|---|
| 1. 取得曲面 | 以 STEP／IGES／SAT 從外部系統匯入 Surface Manager | 24.3.6 |
| 2. 健檢 | Analyze、Sew、Optimize；視需要 Combine、Restrict | 24.3.7 |
| 3. 驗收 | Compare Surfaces（對原系統取樣點）；Intersect Surface 取關鍵剖面曲線 | 24.3.7–24.3.8 |
| 4. 釋放 | Release Surface（或 as Symmetric）到設計專案 | 24.3.6 |
| 5. 設計建模 | 在 Multi-View 專案的設計視圖建大面板（見[第 5 章](ch05_hull_modelling_zh-TW.reading.html)） | 24.7 |
| 6. 規劃分段 | 定義切割器、目標分段標稱盒與偏移 | 24.6.1 |
| 7. 切割與排序 | 建 Job → Verify → Apply／Divide → Sort | 24.6.3–24.6.5 |
| 8. 驗證 | 來源分段、`_P` 預設分段、Verify | 24.5.4 |
| 9. 後續 | 在生產視圖補生產資料，之後接零件抽出與套料（見[第 6 章](ch06_hull_production_zh-TW.reading.html)） | 24.7.4 |

## 24.9 本章小結

- Surface Manager 是曲面進入 Marine 的「檢疫站」：匯入、Analyze、修補、驗收、釋放。關鍵規則是 Hull Surface 才能直接釋放、多 Primitive 要先 Combine、對稱曲面不得跨中心線、專案在一次作業中固定。
- Block Division 以「來源面板、切割器、目標分段」三項輸入驅動：選取 → Verify → Apply → Divide → Sort。目標分段的盒子與偏移由使用者自己負責，系統不檢查與切割器是否一致；最小板寬與最小加強材長度決定切割是否被忽略。
- 切割時元件分成 Atomic、Sharable、Cuttable、Referred 四類，各有處理規則；設計到生產的分割保留設計面板，沒涵蓋的部分進入 `_P` 預設生產分段。
- Multi-View Project 是同一模型的兩個視圖：設計面板是大塊、無生產資料的「藍圖」，生產面板帶完整生產資料；Block Seam 是兩者的橋梁，生產面板的邊界完全由設計面板與 Block Seam 決定。
- 對二次開發者，文件有依據的整合點主要在「檔案」層（STEP／SAT／IGES／DML、blines、取樣點檔）與「設定」層（`SBH_CONCODES`、`PAN_SPLIT_ECUT_*`）；Block Division 的批次執行與 Multi-View 的資料庫屬性需補讀其他官方章節〔待核對〕。

## 24.10 練習題與自我檢核

### 練習（只在訓練專案或測試用工作區進行）

**練習 24-1　曲面健檢。** 匯入一個測試用 STEP 或 IGES 曲面，記錄圖形視窗中藍色邊的位置；執行 Analyze，整理 warning 與 error 數量；執行 Sew，再 Analyze 一次，比較前後差異。

**練習 24-2　切剖面。** 用 Intersect Surface 以 X 方向每 1000 mm 切一組剖面曲線，說明 Direction and distance 與 Ending point 如何決定產生的曲線數量。

**練習 24-3　Scene Template。** 建立一個含 Box Filter 的 Browse 型 Scene，另存成 Scene Template，再用它建立新 Scene，確認哪些屬性有被帶走、哪些沒有。

**練習 24-4　偏移量推演。** 假設在肋骨平面切割甲板面板，加強材延伸到面板外 250 mm，最小加強材長度 100 mm。請分別為前方分段與後方分段提出偏移建議，並說明理由。（答案方向：後方分段的前緣至少需包住加強材外延且不小於最小加強材長度；前方分段的後緣可較小，但仍不得小於最小加強材長度。實際數字依專案規則。）

**練習 24-5　Job 順序。** 在測試分段上建立一個 Job，分別試「先 Sort 再 Divide」與「先全部 Divide 再 Sort」（用複本或 Save Work 基準），記錄哪些面板的結果不同。

**練習 24-6　Multi-View 判定。** 對下列情況判斷專案型態並說明理由：（a）空專案先建立 Design Block；（b）空專案先建立一般分段；（c）一般專案中想建立 Design Block。

### 自我檢核

1. Hull Surfaces 與 Primitive Assemblies 兩區在匯入時，對組裝樹的處理有什麼不同？
2. 為什麼釋放含多個 Primitive 的曲面前必須 Combine？
3. 在 Surface Manager 一次作業中，如何把曲面從專案 A 匯入、再釋放到專案 B？
4. Analyze 的 warning 與 error 如何區分？
5. Block Division 的三種用途是什麼？哪一種不用切割器？
6. 曲面面板可以使用哪種切割器？為什麼要先建立 Shell Block Seam？
7. Atomic、Sharable、Cuttable、Referred 四類元件各舉兩個例子，並說明跨過切割器時各自如何處理。
8. 設計分段切成生產分段後，設計面板留在哪裡？不在任何生產分段內的生產面板去哪裡？
9. 最小板寬與最小加強材長度分別在什麼情況下使切割「被忽略」？
10. 設計面板與生產面板中，哪一個帶生產資料？更新時為何不會洗掉生產資料？
11. 為什麼生產面板的邊界定義不能修改？有什麼例外？
12. Hull Detail Design 與 Outfitting 對視圖的選擇有何不同？

## 24.11 〔待核對〕彙整

| 項目 | 說明 |
|---|---|
| Scene Template 路徑 | 官方只列 Windows XP／Vista／7；新版 Windows 的實際路徑 |
| Save Camera 快速鍵 | 官方表格寫作 `Cltr+S`，本章依合理推測改為 Ctrl+S |
| 取樣點檔格式 | 只有官方一個範例；編碼、換行、相鄰重複點的原因未說明 |
| `sj708` 取得與使用 | 官方稱不含標準安裝，需洽本地支援；在 AVEVA Marine 12.1 的可用性待確認 |
| Surface Manager 自動化介面 | 文件未提及腳本、命令列或 API |
| blines、`.tbw`、`SceneTemplates.dat` 內部格式 | 文件未提供 |
| Job Setup 預設值單位 | 畫面為 50／100，單位文件未明說 |
| Stored panels 與 Stored planes | Cutters 兩處用詞不同，以實機為準 |
| `SBH_CONCODES` 檔案格式、`PAN_SPLIT_ECUT_*` 所在設定檔 | 官方此頁未說明 |
| Block Division 批次執行 | 官方指向 *Batch Utilities*，本章未取材 |
| Block Division 的 Logs 是否可匯出 | 文件未提及 |
| Multi-View 轉換工具 | 官方指向 *Create/Remove Design Blocks and Panels*，本章未取材 |
| Design／Production 在資料庫的屬性與型別 | 文件未提供 |

## 資料來源

- AVEVA Marine 12.1 官方離線文件：*Surface Manager*（含 Overview、Interface Components、Tools and Functions、Keyboard Shortcuts、Appendices）、*Block Division*（Purpose、Panel Selection、Cutting、Sorting、Target Blocks and Cutters、Boundary Creation、Components、Block Seam Properties、Verification of the Result、Iterative Block Division、The Interactive Interface）、*Multi-View Project*（Design View - Production View、Creating a Multi-View Project、Design - Production Connections、Production Data）。
- 本課程延伸：[第 5 章 船體建模](ch05_hull_modelling_zh-TW.reading.html)、[第 6 章 船體生產資訊、套料與裝配](ch06_hull_production_zh-TW.reading.html)、[第 7 章 舾裝設計](ch07_outfitting_zh-TW.reading.html)、[第 12 章 PML 資料庫操作](ch12_pml_database_zh-TW.reading.html)、[第 20 章 系統管理與維運](ch20_system_administration_zh-TW.reading.html)。
