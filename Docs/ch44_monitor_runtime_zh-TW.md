# 第 44 章　Monitor 與 Marine 執行環境：Monitor Reference、Program Environment、Runtime 與命令列工具

> 第 2 章把 Monitor 列在「進入專案後的起點」，第 3 章講了 User、Team、MDB 與寫入權限，第 43 章從系統管理員的角度談了備份、DICE 與升級。這一章補上它們都沒細講的兩塊：**第一，Monitor 這個模組本身有哪些命令、會丟出哪些錯誤訊息；第二，Marine 程式是怎麼被啟動的（Job Launcher、`MarJobs.xml`）、環境變數怎麼層層覆蓋，以及有哪些命令列工具。**
>
> 這些內容看起來瑣碎，但二次開發與維運時最常卡在這裡：批次作業登入失敗、`MDB not found`、自家工具想被 Job Launcher 掛起來卻沒有出現在 Log Viewer、某位使用者的預設檔想改又不想影響別人。
>
> **資料可信度：** 本章取自 AVEVA Marine 12.1 離線文件的 *Monitor Reference*（約 54 頁）與 *Marine Administration*（約 17 頁，含 Program Environment、Projects、Runtime System、Command-line Utilities）。官方文件帶有 PDMS 時代的殘留（例如 `PDMSEXE`、`PDMSWK`、`PDMSUI`、`PDMS_ID`），且機器翻譯品質不一，譯名已改為台灣慣用說法。文件之間有互相矛盾之處（見 44.14），一律標〔待核對〕。文件沒有講的（例如 Monitor 與 PML 的細節 API）不編造。與 Marine 專案目錄、備份、DICE 的管理面請回到[第 43 章](ch43_system_administration_zh-TW.reading.html)，資料庫類型與 Team／MDB 概念請見[第 3 章](ch03_project_database_zh-TW.reading.html)。

## 44.1 學習目標

讀完本章，你應該能夠：

1. 說明進入 Marine 的順序（`PROJECT` → `USERNAME` → 選 MDB → 切模組），以及 Monitor 為什麼會擋住你。
2. 區分 Free／General 使用者、Free／Restricted 模組，並判斷「為什麼這個人進不了 Admin」。
3. 解釋 Current 與 Deferred（non-current）資料庫，並正確使用 `CURRENT`、`DEFER`、`EXCHANGE`。
4. 使用 `LIST`、`QUERY`、`STATUS`、`SYSTAT` 查詢專案、使用者與資料庫狀態。
5. 用 `PROTECT` 暫時降低自己的存取權，並知道它不能升權。
6. 設計批次作業：`BATCH COPY`／`NOCOPY` 的語意、登入失敗行為、帳密保護與 COMMS DB 風險。
7. 看懂 Monitor 錯誤訊息 `(39,n)` 的意義與處置。
8. 說明 Job Launcher、Session、Job、`MarJobs.xml` 與 `marjobstarter.exe` 的關係。
9. 解釋 `<proj>MAR` 目錄、Default File、環境變數三層覆蓋順序與 Marine Environment utility。
10. 說明 `SA004` 資料庫工具能做什麼，以及它的使用界線。

## 44.2 本章在整體架構中的位置

```
 專案環境變數（<proj>MAR、d065、環境表）
        |                          |
   Monitor 線                 Job Launcher 線
 PROJECT/USERNAME/MDB      MarJobs.xml -> marjobstarter.exe
 -> mon、adm、lex、設計模組   -> sf416d、sj902、sa004 等 exe -> Log Viewer
```

實務上可以把 Marine 分成兩條線：

| 線 | 代表程式 | 管什麼 | 本章章節 |
|---|---|---|---|
| Monitor 線（Dabacon 資料庫模組） | `mon`（Monitor）、`adm`（Admin）、`lex`（Lexicon）、設計與出圖模組 | 專案、使用者、MDB、DB 的 Current／Deferred、模組切換 | 44.3–44.9 |
| Job Launcher 線（獨立執行檔） | `sf416d`、`sj902`、`sa004` 等數百支 exe | 以 Session／Job 形式啟動、輸入輸出參數、Log Viewer | 44.10–44.13 |

兩條線共用同一組專案環境與環境變數，所以管理員常要同時懂兩邊。

## 44.3 進入 Marine：Access Rights 的完整流程

### 44.3.1 Monitor 的前提

官方 *Monitor Reference* 的「Assumptions」只有兩句：讀者已有有效授權且軟體已安裝、已完成 AVEVA 基礎訓練；手冊是寫給「需要自訂介面或撰寫巨集」的人。這也是本章的定位。

### 44.3.2 進入順序

| 步驟 | 命令 | 說明 |
|---|---|---|
| 1 | `PROJECT proj_name` | 指定專案，例如 `PROJECT SAM`。可先查詢有哪些專案。 |
| 2 | `USERNAME` | 指定使用者名稱與密碼。登入前就能查詢使用者與 MDB，但**設定 MDB 之前必須先給 username**。 |
| 3 | 進入 Monitor | 帳密正確後即在 Monitor 內，可用本章的命令。 |
| 4 | 指定 MDB | 要進入任何其他模組（ADMIN 除外）前，Monitor 會檢查是否已選 MDB。 |
| 5 | 輸入模組名稱 | 進入有權使用的模組；在任何模組輸入 `Monitor` 可回到 Monitor。 |

> **專業提醒：** 非圖形模式下，官方建議**單獨輸入** `USERNAME`，等系統提示後再輸入帳密（畫面不回顯）。不要寫成 `USERNAME SYSTEM/XXXXXX` 一行完成，那是安全風險。文件中的 `USER SYSTEM/XXXXXX` 範例只適用於不得已的巨集情境，詳見 44.6.3 的批次安全。

### 44.3.3 資料庫類型（Monitor 視角）

第 3 章已有完整的資料庫類型表，這裡只列 Monitor 文件的分法，方便讀 `LIST` 輸出：

| 類別 | 內容 |
|---|---|
| System Databases | SYSTEM（存取控制資料）、COMMS（誰在用哪個模組、有哪些模型 DB 可用）、MISC（使用者間訊息、跨 DB 巨集）；Global 專案另有 Global DB 與 transaction DB |
| Model Databases | DESIGN、CATALOGUE、PADD（Draft 圖面資料）、PROPERTIES、DICTIONARY（UDA 定義，Lexicon 維護）、ISOD（SPOOLER 的管段圖） |
| Marine 專案另有 | SCHE（P&ID 模組的流程圖資料）、MANU（製造資料）、NSEQ（名稱序列） |

### 44.3.4 資料庫存取控制與 Team 命名

使用者對某個 DB 的存取只有三種：**Read/Write**、**Read-only**、**None**。每個 DB 另有存取模式 `UPDATE`（同時只有一位 Read/Write）、`MULTIWRITE`（多位同時 Read/Write）與 `CONTROLLED`（由外部系統控制），管理面的說明見[第 43 章 43.8.2 節](ch43_system_administration_zh-TW.reading.html)。

DB 名稱格式為 `teamid/identifier`，例如 `PIPING/PIPING-A`。`teamid` 即擁有完整 Read/Write 的團隊；管路團隊對 `MASTER/CATALOGUE-1` 則只有唯讀。**外部資料庫（Foreign DB）**是從別的專案納入的，常用於 Catalogue，讓許多人讀同一份而不必複製；`LIST` 輸出中會標示 `Foreign`。

使用者等級由系統管理員指派：Free 對所有資料庫都有 Read/Write；General 只對「目前 MDB 中自己團隊擁有的 DB」Read/Write，其他 DB 唯讀。帳號管理的實務見[第 43 章 43.7.2 節](ch43_system_administration_zh-TW.reading.html)。

### 44.3.5 模組存取控制

模組分 **Free** 與 **Restricted**：只有 Free 使用者可用 Restricted 模組；General 使用者只能用 Free 模組。出廠設定中**只有 Admin 與 Lexicon 是 Restricted**，其餘皆 Free。這是「為什麼一般設計者進不了 Admin」的答案（錯誤 `(39,14)`，見 44.9）。

> **專業提醒：** MDB 最多可含 1000 個 DB，且可任意多個同時為 Current。但選 MDB 進入設計模組時，**UNITS 設定取自第一個 Current 的 Catalogue DB**，所有 Current Catalogue DB 的連接相容（COCO）表都會可用。所以 Catalogue DB 在 MDB 裡的排序不是隨便的。〔排序對實際單位的影響，待核對〕

## 44.4 Monitor 的日常操作

> 〔公開版未收錄：AVEVA 官方產品截圖〕Monitor 主視窗的 Monitor 選單，展開 Modules 子選單可見 Admin、Hull Design、Marine Drafting 等模組

*圖 44-1　Monitor 主選單列的 Monitor > Modules 子選單：列出本安裝可進入的模組（Admin、Hull Design、Marine Drafting、Outfitting、Outfitting Draft、Isodraft、Spooler、Paragon、Specon、Lexicon、Propcon 等）。（AVEVA 官方文件截圖，僅供內部教學）*

### 44.4.1 Monitor 選單地圖

官方「Menu Maps」共 6 張圖，涵蓋 Monitor 主選單列的 Monitor／Display／Project／Window／Help 五個選單。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Monitor 的 Project 選單，含 Inter-db Macros、User Status、List（Users、Teams、DBs、MDBs、User Rights）與 Change Password

*圖 44-2　Project 選單：Inter-db Macros...、User Status...、List（Users...、Teams...、DBs...、MDBs...、User Rights...）、Change Password...。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Monitor 的 Display 選單，含 Monitor、Command Window、Show Descriptions、Show Names

*圖 44-3　Display 選單：Monitor...、Command Window...、Show Descriptions、Show Names。（AVEVA 官方文件截圖，僅供內部教學）*

> 〔公開版未收錄：AVEVA 官方產品截圖〕Monitor 的 Help 選單，含 Contents、Search、About

*圖 44-4　Help 選單：Contents、Search、About。（AVEVA 官方文件截圖，僅供內部教學）*

選單與命令的對應（依圖文推斷，官方未逐項對照，〔對應關係待核對〕）：

| 選單項目 | 對應的命令概念 |
|---|---|
| Project > List > Users／Teams／DBs／MDBs | `LIST USERS`／`TEAMS`／`MDBS`／`DBS` |
| Project > User Status... | `STATUS` |
| Project > Inter-db Macros... | 跨 DB 連接巨集（`QUERY MACRO`／`DELETE MACRO`） |
| Project > Change Password... | `PASSWORD` |
| Display > Command Window... | 命令視窗，可直接輸入本章命令 |
| Monitor > Modules > ... | 以模組名稱切換模組 |

> **專業提醒：** 圖形介面的操作最後都會轉成命令字串（第 2 章已提過）。想知道某個選單「到底做了什麼」，就開 Command Window 看對應命令。

### 44.4.2 常用操作速查

| 想做的事 | 作法 | 備註 |
|---|---|---|
| 改密碼 | `PASSWORD password` | 管理員可以鎖定（見 44.5.3） |
| 看自己的狀態 | `STATUS` | 專案、使用者（含主機）、所屬 Teams、MDB、各 DB 與 RW／R 模式 |
| 看誰在線上 | `SYSTAT` | 每位使用者的 ID、登入名、主機、進入時間、模組、MDB、各 DB 模式 |
| 設目前團隊 | `SET TEAM SAMPLE` | 之後可寫 `Q DB /DESI` 取代 `Q DB SAMPLE/DESI` |
| 傳訊息 | `MESSAGE` | 訊息要用單引號包住；只送給目前已在專案內的人，且在對方**下次切換模組**時才顯示 |
| 輸出到檔案 | `ALPHA FILE`（建議）或 `FILE` | `ALPHA FILE END` 回到螢幕；`FILE` 要用 `TERMINAL` 回螢幕 |
| 更換輸出裝置 | `DEVICE GRAPHICS／NOGRAPHICS／TTY` | `Query DEVICE` 查詢目前值 |
| 離開 | `FINISH`（Monitor 內可縮寫 `FIN`） | 其他模組內必須完整輸入 |

輸出預設為「螢幕、每行 80 字元」。`ALPHA FILE` 與 `FILE` 還能設定每行字元數、每頁行數，以及是否覆寫。

### 44.4.3 命令語法的讀法（Syntax Graph）

官方以語法圖表示命令，讀法如下，後面幾章（以及其他模組的命令手冊）都用同樣慣例：

| 慣例 | 意義 |
|---|---|
| 大寫字母 | 最小縮寫，例如 `Query` 可打 `Q`、`QU`、`QUE`、`QUER`、`QUERY` |
| 全大寫的命令 | 不可縮寫（例如 `DELETE`，為防誤刪） |
| 小寫斜體 | 引數描述，要換成實際值 |
| `+` 接點 | 選項，擇一，或直接 Enter 取預設 |
| `*` 接點 | 迴圈，選項可重複 |

| 引數 | 定義 | 例 |
|---|---|---|
| `name` | 元素名稱 | `PIPE-A63` |
| `refno` | 參考編號 | `=23/1403` |
| `integer` | 正整數 | `3` |
| `value` | 正或負數 | `3.142` |
| `word` | 最多 4 個字母 | `FLOW` |
| `text` | 英數字串 | `'Enclose in quotes'` |
| `filename` | 檔案路徑 | `/c:\\testing` |

**注意：Marine 的所有名稱都以斜線開頭**，所以完整路徑也要先加一個 `/`。這也是 `PASSWORD /SECRET` 的由來。命令大小寫不拘。

## 44.5 Current、Deferred 與資料庫切換

### 44.5.1 三個命令

| 命令 | 作用 | 語法 |
|---|---|---|
| `CURRENT` | 把指定 DB 設為 Current，並插在 Current 清單第 n 個位置（1–1000） | `CUrrent dbname n ...` |
| `DEFER` | 把 DB 從 Current 清單移除，改為 Deferred | `DEfer dbname ...` |
| `EXCHANGE` | 用一個 Deferred DB 取代一個 Current DB | `EXchange dbname dbname ...`（成對） |

官方範例：MDB `/DESIGN` 的 Current 為 `PIPING/PIPING-A`、`PIPING/PIPING-C`、`MASTER/CATA-D`，Deferred 為 `PIPING/PIPING-B`、`MASTER/PIPING-E`。執行

```
EXCHANGE PIPING/PIPING-A PIPING/PIPING-B MASTER/PIPING-E MASTER/CATA-D
```

後，Current 變成 `PIPING/PIPING-B`、`PIPING/PIPING-C`、`MASTER/PIPING-E`，Deferred 變成 `PIPING/PIPING-A`、`MASTER/CATA-D`。名稱的先後不重要（MDB 自己知道誰是 Current），**但多於兩個名稱時必須正確配對**。`CURRENT PIPING/PIPING-A 1 MASTER/CATA-D 4` 則是依序把兩者插入第 1、第 4 位，且**位置是以前一次插入完成後的清單為準**。

### 44.5.2 LIST／QUERY 輸出怎麼讀

| 命令 | 輸出重點 |
|---|---|
| `LIST USERS` | 每位使用者的等級（Free／General）與所屬 Teams |
| `LIST TEAMS` | 每個 Team 的成員與其 DB |
| `LIST MDBS` | 每個 MDB 的 Current DBs（序號、`team/db`、類型、模式如 `Update`、是否 `Foreign`）與 Deferred DBs |
| `LIST DBS` | 每個 DB 的類型、`Number`（資料庫編號）、模式、`Size ... pages`、含它的 MDBs |
| `LIST COPIES` | 從別的專案複製來的 DB 與其副本名稱 |
| `LIST MODULES` | 每個模組的 Security（Free／Restricted）、`Imacro`、`Open Attlib`、`Open Message`、`Resume` 路徑（如 `/%PDMSEXE%/mon`） |

`LIST` 另有 `EXTERNAL`（外部 DB）、`TYPES`、`FILES`、`SIZES`（頁數與 Mbytes）、`MACROS`、`AREA n`、`MESSAGES`、`ALL`、`WORKING EXTRACTS [FOR username]`、`AUTHUSERS`（NT 授權使用者）。

`QUERY` 的 Monitor 版可查：

| 查詢 | 例 |
|---|---|
| 使用者 | `Q USER`、`Q USER SAMPLE`、`Q USER SYSTEM ACCESS`（僅 Free 使用者可得）、`DESCRIPTION`、`PASS` |
| 在線人數 | `Q ACTIVE` |
| Team／MDB | `Q TEAM SAMPLE`、`Q MDB /SAMPLE`、`Q SET TEAM` |
| DB 屬性 | `Q DB SAMPLE/DESI`，後接 `TYPE`、`FILE`、`NUMBER`、`SIZE`、`FOREIGN`、`ACCESS`、`DESCRIPTION` |
| 副本、巨集 | `Q COPIES SAMPLE/DESI`、`Q MACRO 1`（`FILENAME`／`FROMDB`／`TODB`） |
| 其他 | `Q PASSWORDLOCK`、`Q PROJ`（`NAME`／`NUMBER`／`DESCRIPTION`／`MESSAGE`）、`Q DEVICE` |

DESCRIPTION 類輸出必須事先設定過描述才有內容；DB 的詳細查詢「主要供系統管理員參考」。

> **專業提醒：** `Q DB 名稱 FILE` 會直接回傳實際檔名（官方範例 `/%MAS000%/mas005`，其中 `MAS000` 是 Area 環境變數），是追查「這個 DB 到底在哪個檔案」最快的方法，比到磁碟上找快得多。這與第 43 章的 DB 檔案命名一致。

### 44.5.3 PROTECT 與 PASSWORD

`PROTECT dbname RW|Read|None` 可暫時降低自己對目前 MDB 內某 DB 的權限，**只能降、不能升**，且只在當前 Session 有效。範例：`PROT PIPING/AREA-B READ`，之後 `STATUS` 的 MODE 欄由 `RW` 變成 `R`。這對「我只想檢查，不要不小心寫入」很實用。

`PASSWORD` 在管理員打開 PASSWORDLOCK 時不能用，可先 `Q PASSWORDLOCK` 確認；被鎖時改密碼要請管理員處理（錯誤 `(39,36)`）。若輸入錯誤密碼導致自己進不去，也只能請管理員。〔密碼長度與字元限制，見 44.14。〕

### 44.5.4 跨 DB 連接巨集

在設計模組要連接到「沒有寫入權限的另一個 DB 裡的元素」時，系統會建立 **inter-DB 連接巨集**，要由適當的使用者（擁有寫入權的團隊）在 Design 內執行，系統再自動刪除。Monitor 的 `LIST MACROS`、`Q MACRO n`、`DELETE MACRO n` 管理它們。`DELETE` 不可縮寫；對方團隊還沒讀取的巨集不能刪（`(39,19)`）。

## 44.6 批次模式（Batch）

### 44.6.1 批次的基本規則

批次作業要以**批次模式啟動 Marine**（細節見 *Marine Software Installation Guide*，本課程資料中未涵蓋）。你要先寫一個檔案，內容是平常在鍵盤上輸入的所有命令，再用作業系統的一般方式執行。

| 項目 | 互動模式 | 批次模式 |
|---|---|---|
| 帳密嘗試次數 | 3 次 | **1 次**，錯了就把控制權還給作業系統並終止 |
| 專案名／帳號／密碼錯誤 | 重試 | 立即中止 |
| 其他錯誤 | 顯示後繼續 | 立即中止，**除非使用 PML 錯誤處理** |
| `BATCH` 命令 | 被忽略，產生 `(39,23)` | 有效 |

### 44.6.2 BATCH COPY／NOCOPY

批次作業預設若沒給 `COPY`，會**複製所有 Design DB**；若完全不複製，原始 DB 一律以 **Read-only** 存取（不論原本權限）。複製的目的是讓批次作業用副本（可寫，例如自動建群組需要寫入），互動使用者繼續用正式版。

| 命令 | 效果 |
|---|---|
| `BATCH COPY DESI DRWG` | 複製選定 MDB 的所有 Design 與 Drawing DB |
| `BATCH COPY PIPING/DES74A CIVIL/DES13B` | 複製指定的兩個 DB |
| `BATCH COPY ALL` | 複製 MDB 內全部 |
| `BATCH COPY NONE` | 不複製任何 DB |
| `BATCH NOCOPY PIPING/DES74A` | 此 DB 不複製 |

`dbtype` 可為 `DESI`、`CATA`、`PROP`、`PADD`、`DICT`、`ISOD`。**COPY 是累加的**：官方例子依序下 `COPY NONE`、`COPY PIPING/DES75A PIPING/DES37C`、`COPY DRWG`，結果只有那兩個 DESI 被標記複製（因為該 MDB 沒有 DRWG 類）。

何時真的複製：第一次「切換模組」命令之後才複製。若選了新 MDB，或重選同一個 MDB 而殘存上次的副本，**舊副本全部刪除再重新複製**。副本是暫時的，批次結束（不論成功）或選新 MDB 時消失；要永久副本須由管理員用 Admin 建立。

此外，透過 Admin 與 RECONFIGURER 存取 DB 只能 Read-only，嘗試修改專案結構會得到 `Trying to alter a read-only database`。

### 44.6.3 批次的安全與資料完整性

- **帳密存在檔案裡**：批次檔必須用作業系統權限保護；許多批次系統會把提交的檔案複製到他處，使用者若看得到那份副本，帳密仍會外洩，專案協調者應與 IT 確認。
- **COMMS DB 風險**：唯讀批次時唯一會被寫入的是 COMMS DB，批次若中途被打斷有損毀風險。官方建議：不要遠端下指令中止批次作業、不要使用有 CPU 或經過時間限制的批次佇列、有磁碟將滿風險時不要執行。
- **磁碟**：每次選 MDB 都重新複製，批次使用者必須評估對磁碟空間的影響。

> **專業提醒：** 把批次用的 Marine 帳號做成專用帳號、給最小權限、密碼獨立輪替，並讓批次檔所在目錄只開給該服務帳號。批次作業要偵測失敗時，在 PML 層面加錯誤處理（官方指向 *Software Customization Guide*，本章未涵蓋），否則「遇錯即停」會讓夜間批次半途而廢。

## 44.7 Monitor 命令總表

官方「Command Summary」共 18 個命令，加上 `QUERY`：

| 命令 | 官方功能 | 本章章節 |
|---|---|---|
| `BATCH` | 指定批次作業處理方式 | 44.6 |
| `CURRENT` | 使資料庫成為 Current | 44.5.1 |
| `DEFER` | 使資料庫成為 Deferred | 44.5.1 |
| `DELETE` | 刪除 inter-DB 連接巨集 | 44.5.4 |
| `DEVICE` | 指定裝置類型 | 44.4.2 |
| `EXCHANGE` | 用 Deferred DB 取代 Current DB | 44.5.1 |
| `FINISH` | 離開 Marine | 44.4.2 |
| `LIST` | 列出專案資訊 | 44.5.2 |
| `MESSAGE` | 傳訊息給其他使用者 | 44.4.2 |
| `PASSWORD` | 改密碼 | 44.5.3 |
| `PROJECT` | 指定目前專案 | 44.3.2 |
| `PROTECT` | 變更對 DB 的存取權 | 44.5.3 |
| `QUERY` | 查詢命名的管理元素 | 44.5.2 |
| `RUN` | 執行無法透過一般模組切換命令啟動的模組 | 見下 |
| `SET` | 設定目前團隊（`SET TEAM teamid`） | 44.4.2 |
| `STATUS` | 目前狀態與可存取的 DB | 44.4.2 |
| `SYSTAT` | 專案目前活動狀態 | 見下 |
| `USERNAME` | 指定使用者名稱與密碼 | 44.3.2 |

**`SYSTAT`** 預設列出全專案每位在線使用者，也可篩選：`SYSTAT USER pdms_id`、`NAME 'login_id'`、`HOST 'host_id'`、`MODULE module`、`MDB mdb_name`。管理員常用它在維護前確認「誰還在用哪個 DB、是 R 還是 RW」，再搭配 `MESSAGE` 通知。例如 `MESS TEAM PIPING 'LATEST PIPE ROUTING HAS BEEN APPROVED'`。`MESSAGE` 的收件對象可指定為 `n`、`HOST hostname`、`ID descript`、`LOGIN loginid`、`USER userid`、`TEAM teamid`，不指定則為全部在線使用者。

**`RUN module`**：官方明確寫「僅應在 AVEVA 建議下使用」。**本課程不建議自行嘗試。**

> **專業提醒：** `SYSTAT` 的 R 與 RW 很重要：看到某個 UPDATE 模式的 DB 被別人以 RW 佔著，就能說明為什麼你寫不進去（第 3 章 3.10 的原因之一）；但它看不到「未存檔的 Session 內容」，維護前仍須主動通知。

## 44.8 二次開發者與管理者怎麼接 Monitor

| 情境 | 文件依據 | 作法 |
|---|---|---|
| 想做自己的登入或啟動巨集 | Monitor Reference 假設讀者會「自訂介面或撰寫巨集」；`LIST MODULES` 顯示每個模組有 `Imacro`（如 `/%PDMSUI%/MON/ADMIN/START`） | 沿用官方啟動巨集的路徑慣例；修改其內容的細節〔待核對，文件未說明〕 |
| 想在工具裡列出 MDB 或 DB | `LIST`／`QUERY` 的輸出格式已列於 44.5.2 | 以命令取得輸出，再解析；PML 內取得輸出的 API 及其行為〔待核對：本章資料未涵蓋〕 |
| 想在批次中遇錯不中止 | 文件：除非使用 PML 錯誤處理 | 依 *Software Customization Guide*〔本章未讀〕 |
| 想把輸出導到檔案 | `ALPHA FILE`／`FILE`／`TERMINAL` | 見 44.4.2 |
| 排查「為什麼進不了模組」 | `(39,8)`、`(39,13)`、`(39,14)` | 見 44.9 |
| 想讓使用者別看到圖形 | `DEVICE NOGRAPHICS` | 批次或自動化測試時有用 |

## 44.9 Monitor 錯誤訊息

官方說明：Monitor 專屬的訊息編號都以 **39** 開頭，格式 `(39,n)`；螢幕輸出含編號，訊息檔則省略編號。其他模組的訊息不在此列。以下為官方列出的全部項目，處置欄為本課程依文意補充。

| 編號 | 訊息 | 官方原因 | 處置 |
|---|---|---|---|
| (39,3) | MDB not found | 引用的 MDB 名稱在目前專案不存在 | `LIST MDBS` 查名稱；MDB 名以 `/` 開頭 |
| (39,4) | DB not found | DB 名稱不存在 | `LIST DBS`；記得 `team/db` 格式或先 `SET TEAM` |
| (39,5) | TEAM not found | Team 不存在 | `LIST TEAMS` |
| (39,6) | Insufficient status to set this mode | 使用者權限不允許修改相關檔案 | 找管理員，或確認是否為 Free |
| (39,7) | USER not found | 該使用者不是指定（或目前）Team 的成員 | 先確認 Team 成員 |
| (39,8) | MODULE not found | 專案資料庫內找不到該模組的 runfile，須由管理員用 Admin 設定 | 管理員處理 |
| (39,11) | DB not current | `EXCHANGE`／`DEFER` 指定的 DB 不是 Current | 先 `LIST MDBS` 確認 |
| (39,12) | User number not found | 沒有使用者以該 ID 登入 | `SYSTAT` 查 ID |
| (39,13) | Resume file not found | 找不到模組的 runfile（同 39,8） | 管理員處理 |
| (39,14) | Insufficient status to run module | 你沒有該模組的存取權 | 見 44.3.5：Restricted 模組只有 Free 使用者可用 |
| (39,15) | No MDB has been specified | 進入大多數模組、或設 DB 為 Current 前，必須先選 MDB | 先選 MDB |
| (39,16) | DB is not part of this MDB | 該 DB 不在指定（或目前）MDB 內 | `LIST MDBS` |
| (39,17) | DB already current | `CURRENT`／`EXCHANGE` 指定的 DB 已是 Current | 忽略或調整命令 |
| (39,18) | Filing error - cannot delete macro file | `DELETE MACRO` 的巨集 ID 無效 | `LIST MACROS` 查 ID |
| (39,19) | Cannot delete - macro not yet read | 接收團隊尚未讀取該巨集 | 等對方執行 |
| (39,20) | Current position out of range | 加入 Current 的位置須為 1–1000 | 修正位置 |
| (39,21) | There are already 1000 current DBs | MDB 同時最多 1000 個可存取 DB | 用 `EXCHANGE` 或 `DEFER` 騰出空間 |
| (39,22) | Actions turned off | 已下過 `ACTIONS OFF` | 〔`ACTIONS` 命令文件未收錄，待核對〕 |
| (39,23) | BATCH command ignored for interactive use | `BATCH` 只在以批次選項進入時有效 | 以批次模式啟動 |
| (39,25) | /* is not a valid MDB | MDB 必須完整指名，不可用萬用字元 | 寫出完整名稱 |
| (39,36) | User password not changed - passwordLock is on | 管理員已將 PASSWORDLOCK 設為 ON | 請管理員改 |


## 44.10 Marine 系統目錄與檔案

### 44.10.1 安裝根目錄

系統一律安裝在一個 root 目錄下：

| 子目錄 | 官方用途 |
|---|---|
| `Config` | 目前的專案組態與設定 |
| `customize` | 與專案無關的範例檔 |
| `Documentation` | 線上 HTMLHelp 文件 |
| `Etc` | 訊息檔、語法檔、符號檔 |
| `Projects` | 隨系統安裝的範例專案 |
| `Template project` | 建立新專案時使用的範本專案 |
| `Vitesse` | Vitesse 原始碼檔 |
| `Python` | Python 原始碼檔 |

**`Bin`、`Config`、`Documentation` 是系統安裝本體，不得手動編輯。**客製內容請放在專案目錄或自己的工具庫，不要放進這三個目錄。（Vitesse 見[第 36 章](ch36_hull_vitesse_zh-TW.reading.html)。）

### 44.10.2 `<proj>MAR` 與 Default File

除了第 43 章談過的建立專案程序，Marine 專案還要設一個 Windows 環境變數 `<proj>MAR`（專案叫 ABC 就是 `ABCMAR`），指向額外的 Marine 專案資料。標準子目錄：

| 子目錄 | 內容 |
|---|---|
| `<Proj>\MAR\dat` | 各種輸入資料檔 |
| `<Proj>\MAR\def` | 預設值與標準（例如 Default File） |
| `<Proj>\MAR\lst` | 輸出與日誌檔 |
| `<Proj>\MAR\nc` | 輸出給 NC 機器的資料 |
| `<Proj>\MAR\sch` | 結構生成方案、曲面板方案 |
| `<Proj>\MAR\navarch` | 曲面（Surface）檔 |

三種設定載體：

| 載體 | 說明 |
|---|---|
| **Default File** | 以「關鍵字加值」組成的純文字檔，應用程式透過「指向其路徑檔名的環境變數」存取。例：`SBD_DEF1` 指向出圖類應用的預設檔 |
| **IP File** | Hull 應用的預設檔對應物 |
| **Settings Objects** | 某些應用設定以物件形式存在資料庫中 |

> **專業提醒：** 這與第 15、36 章的 Hull 製造資料有直接關係：Hull 的輸入、輸出與預設檔散落在這幾個子目錄，備份專案時只備份 DB 而漏掉 `MAR` 目錄，會讓預設檔與輸出紀錄一起遺失。備份清單請與[第 43 章](ch43_system_administration_zh-TW.reading.html)對照補齊。

## 44.11 Job Launcher：Marine 程式如何被啟動

### 44.11.1 名詞

| 名詞 | 官方定義 |
|---|---|
| Session | 單一應用程式（任一個 exe）的一次執行，例如 Hull Extract Scheme、Hull Parts List、Ppanparts |
| Environment | 環境表中所有環境變數；Marine 專用的環境表**與 Windows 系統及使用者變數分開** |
| Job | Session 加上其輸入輸出參數 |
| Job file | 某個 Job 的實例，內含應用名稱、輸入輸出參數、執行日期；**是暫時性的，不含真正資料**，存在 `%PDMSWK%` 下的 `jobs` 子目錄 |

Job file 對使用者是隱形的；Log Viewer 用它來顯示輸入輸出參數與追蹤執行狀態。

### 44.11.2 `MarJobs.xml`：應用程式定義檔

所有應用（工具程式除外）定義在 `SB_SYSTEM` 目錄的 `MarJobs.xml`。每個應用一個 `<application>` 節點，包含：名稱、簡稱（用於 log 檔命名）、執行檔名稱、輸入參數（描述與型別）、輸出參數（描述、型別與副檔名）。官方範例：

```xml
<application>
  <name>Hull Plane Part Gen.</name>
  <short_name>ppanparts</short_name>
  <executable>sf416d.exe</executable>
  <inputs><input>Input Selection</input></inputs>
  <outputs>
    <output extension="log">Check of input selection</output>
    <output extension="lst">List file</output>
  </outputs>
</application>
```

輸出檔的**檔名由 Job Launcher 在執行時決定，副檔名由此定義**。`<executable>` 只給檔名時，Job Launcher 在 `%PDMSEXE%` 找；要啟動別處的程式則要寫完整路徑（官方範例為 `c:\windows\system32\notepad.exe`）。

### 44.11.3 啟動方式與主控台應用

每個 Session 由專用的啟動程式 `marjobstarter.exe` 啟動，讓每個 Session 擁有環境的私有副本並備齊輸入資料；Job Launcher 在背景等待程式結束，並把執行狀態通知 Log Viewer。官方範例：

```
marjobstarter.exe -input c:\input.dat -application "Hull Parts List"
```

要跑**主控台應用**（例如 `sa004.exe`），有兩個參數：

| 參數 | 作用 |
|---|---|
| `-stdin_file <fname>` | 從指定檔案讀標準輸入，適合無人值守的批次 |
| `-console_stdout` | 把標準輸出寫到主控台；僅限主控台應用。省略時預設把 stdout 轉向檔案（可在 Log Viewer 看） |

三種用法（官方範例）：

| 目的 | 命令 |
|---|---|
| 互動使用，輸出在主控台 | `marjobstarter.exe -console_stdout -application sa004` |
| 主控台輸出並提供輸入檔 | `marjobstarter.exe -console_stdout -stdin_file c:\input.txt -application sa004` |
| 輸出轉檔並提供輸入檔 | `marjobstarter.exe -stdin_file c:\input.txt -application sa004` |

要讓應用被 Job Launcher 看見，必須先定義在 `MarJobs.xml`。官方範例在 `<system name="User">` 區塊下加入 `<application>`（`<name>sa004</name>`、`<short_name>sa004</short_name>`、`<executable>sa004.exe</executable>`）。**自家的批次工具若要納入 Log Viewer 追蹤，這是文件有依據的掛入點**。

> **專業提醒：** 文中一處寫 `marjobstarter.exe`，一處寫 `tbstartjob.exe` 包含這兩個參數，兩者是同一機制的不同名稱或版本差異〔待核對〕。實務請以你安裝目錄裡實際存在的檔案為準。另外，`MarJobs.xml` 屬於安裝內容，修改前應備份並建立變更紀錄，升版時需重新合併。

### 44.11.4 主要執行檔清單

官方列出「主要 Marine 執行檔」，並提醒不是每家客戶都有（取決於授權、客製開發與 Software Pack 版本）。依群組整理如下，只列代表項，完整清單約 160 項：

| 群組 | 代表執行檔（exe → 說明） |
|---|---|
| Early Design／Hull | `marhdes`（Hull Design）、`maridCalc`（Hydrostatics & Hydrodynamics）、`maridLines`、`maridSurface`（Surface and Compartment）、`sj701`／`sj702`（Block Division／Block Create）、`sj706`（Create Design Project） |
| Hull | `sf416d`（Plane Parts Generation，ppanparts）、`sf831d`（Curved Parts Generation）、`sj902`（Extract Scheme）、`sf101d`（Hull Parts List）、`sf103d`（Hull Material List）、`sf609d`（Profile Cutting）、`se032`（Material Nesting）、`sg011`（Weld Planning Batch）、`sj011`（Hull Modelling Batch）、`inithull`（Hull Init） |
| Migration | `marhullmigrate`（從 M3 遷移 Hull）、`marHullVerify`、`marassmigrate` |
| Outfitting | `marodes`、`marodra`（Outfitting Draft）、`diagrams`、`smm`（Schematic Model Manager）、`iss`（IsoDraft）、`isd`（IsoDraw）、`spc`（Specon） |
| Drafting | `marhdra`（Hull Drafting）、`sb021`–`sb023`（Symbol Font 相關）、`sz004`（Create Model pictures in Batch）、`sz005`（Hidden Lines Removal - batch）、`sz020`／`sz021`（DXF Transfer） |
| Basic | `sx700`（Data Extraction）、`ea255`（Error Look Up）、`sa004`（Hull DB Utility）、`tbdbutil`（Hull Object Listing）、`marenvutil`（Hull Environment Utility）、`MarLogViewer`（Hull Log Viewer）、`MarJobStarter`（Job Launcher）、`tbsetup`（Toolkit Preferences） |
| Admin | `adm`（Admin）、`mon`（Monitor）、`lex`（Lexicon）、`BackgroundProcessManager`、`make`（Make Project）、`ProjectCreation`（Project Creation Wizard）、`ResourceEditor`、`PDMSConsole`、`PDMSWait`、`marsurfservmaint`、`Launcher`、`dop`（DICE outside PDMS, global） |

> 清單裡的 `mon` 與 `adm` 正是 `LIST MODULES` 中 `Resume /%PDMSEXE%/mon`、`Resume /%PDMSEXE%/adm` 指向的檔案，這是 Monitor 線與 Job Launcher 線在檔案層面的交會點。`sa004` 與 `tbdbutil` 備註「僅用於列表，不處理圖面」。

## 44.12 Runtime：環境變數與 Marine Environment utility

### 44.12.1 環境變數清單

官方文件另附「All Logical Names」（原為獨立 Excel 表，後轉成網頁表，約 375 個項目；不一定所有變數都適用所有客戶或版本）。欄位為：變數名、型別、說明。變數型別有 `string`、`filename`、`databank`、`real`、`directory`、`file`、`enum units`、`object`、`integer` 等。依前綴約略分群：

| 前綴 | 數量（約） | 性質 | 範例 |
|---|---|---|---|
| `SBH_` | 168 | Hull 應用設定 | 多為 Hull 預設檔與資料庫指定 |
| `SB_` | 129 | 通用設定與資料庫 | `SB_ASSDB`（Assembly 資料庫）、`SB_CGDB`（船型資料庫）、`SB_BACK_COL`（互動應用的背景色）、`SB_COORDINATE_UNIT`、`SB_AREA_UNIT`、`SB_TEMPERATURE_UNIT`（`enum units`，單位）、`SB_CSV_SEPARATOR`、`SB_DB_LOC1`–`9`（資料庫伺服器位置字串）、`SB_PROJ`（內部專案名）、`SB_CUSTOMER` |
| `SBB_` | 23 | 另一組 Hull 相關設定 | 〔本章未逐項核對〕 |
| `SBD_` | 9 | 出圖／標準 | `SBD_DEF1`（預設檔）、`SBD_STD`（標準與表格 DB）、`SBD_PICT`（圖片 DB）、`SBD_LAYER_CLASS` |
| `DXF_`、`IGES_` | 約 10 | 資料交換 | `DXF_LAYER_CTRL`（DXF 圖層控制檔）、`DXFOUT_EXPLODE_DIM`、`IGES_TO_VENDOR` |
| `TB_` | 10 | Tribon 時期遺留 | `TB_CUSTOMER`、`TB_PARTNAME_CTRL`（零件名控制檔） |

`SBD_DEF1` 在專案文件說明為「出圖類預設檔」，變數表寫「Default file General Design」，兩處措辭不同〔待核對〕。此外有若干變數名稱帶 Oracle 相關描述（如 `SB_CMP_SOURCE` 設定零件從 Oracle 或原生資料庫讀取），可見環境變數會牽涉到外部資料庫。〔實際啟用與否依你們的組態，待核對。〕

### 44.12.2 Marine Environment utility

`marenvutil.exe` 可從已設好 Windows 環境變數（例如 `MAR000`、`MARMAR`）以定義專案的命令提示字元啟動，用來**覆蓋專案定義檔（d065）中的 Marine 環境變數**。典型情境：某位使用者暫時要用不同的 Marine Drafting 預設檔，改 `SBD_DEF1` 的值而不影響他人。

> 〔公開版未收錄：AVEVA 官方產品截圖〕Marine Environment utility 視窗：Project 與 System 兩個分頁，上方列出專案變數，下方為使用者變數與 Set、Unset、Remove 按鈕

*圖 44-5　Marine Environment utility：Current project 為 MAR，分頁分「Project」與「System」；Project 頁上半為專案變數（如 `DRAW_BEVEL_COLOURS`、`REVIEW_EXPORT`、`SB_ASSDB`），下半為使用者變數（範例為 `SB_TEST`＝`test`），並可輸入 User variable 與 Value 後按 `Set`、`Unset`、`Remove`。（AVEVA 官方文件截圖，僅供內部教學）*

| 覆蓋層級 | 儲存位置 | 影響範圍 |
|---|---|---|
| User variables（專案層） | 使用者設定檔 | 僅該專案、僅該 Windows 使用者、僅該台機器 |
| System overrides | 安裝目錄中的檔案 | 同一安裝下所有使用者與專案 |
| 專案定義檔 d065 | 專案 | 該專案 |

**執行時指派順序**：1. 讀系統變數；2. 讀 d065 檔的變數；3. 讀使用者變數。後者遮蔽前者，所以**使用者變數 ＞ d065 ＞ 系統變數**。用此工具設定的任何值**都不會修改 d065 檔**。

> **專業提醒：** 「我這邊沒問題、他那邊有問題」多半是環境變數差異：先看使用者層有沒有被覆蓋（`marenvutil` 的 User variables 清單），再看 d065。排查時可請對方截圖該視窗。要還原，選取後按 `Remove` 即可；`Unset` 與 `Remove` 的細節差異〔文件未說明，待核對〕。

## 44.13 命令列工具：SA004

官方在「Command-line Utilities」一節先聲明：**控制台小程式（Control Panel applets）是首選工具**，命令列程式僅提供部分功能。其中 Data Bank Utilities 是為索引式資料庫（data bank）的備份、復原與其他維護而設計的一族工具，**僅限管理員，不應給一般使用者**；備份或重整（reorganization）期間，建議不要讓其他應用存取該 data bank。

> 注意：此處的 data bank 是 Hull 側的索引式資料庫，與第 3 章的 Dabacon DB（DESI、CATA 等）是不同的東西。兩者的備份各自處理。

`SA004`（Data Bank Utility）可處理索引式或循序式資料庫，**輸入由程式互動詢問**：

| 操作 | 說明 |
|---|---|
| Copy | 在資料庫之間複製物件，可改名 |
| Move | 在資料庫之間搬移物件，可改名；**不可從循序資料庫搬出** |
| Delete | 從索引式資料庫刪除物件 |
| List | 列出資料庫中的物件 |
| Archive | 與 Move 相同，但**保留物件的建立日期** |

物件可用下列條件指定，並可任意組合：物件名稱、物件碼 1、物件碼 2、`After date`、`Before date`。名稱規則：

| 寫法 | 意義 | 例 |
|---|---|---|
| `*` | 任意數量字元 | `TB-272-*-1`、`*272*` |
| `%` | 恰好一個字元 | `TB%72*` |
| 結尾加 `*` | 群組名稱 | `TB272*`、`TB*` |

給了確切名稱或群組名稱時可同時指定新名稱，例如 Object name `TB272*`、New object name `TB114*`。若資料庫在別的目錄，必須另外指定目錄。錯誤訊息輸出在標準輸出裝置，文件稱「不需解釋」；**執行過的操作會寫入 `sa004.lst`**。

> **專業提醒：** `SA004` 的 Move、Delete、Archive 會改動資料。使用前先備份該 data bank；用於「只想看內容」時，以 List 為限。要在無人值守的流程使用，請搭配 44.11.3 的 `-stdin_file` 與輸出轉檔，並檢查 `sa004.lst`，作業前先在測試專案演練。

## 44.14 文件內的矛盾與缺口

| 項目 | 文件內容 | 狀態 |
|---|---|---|
| 密碼規則 | Using Monitor 寫「`PASS` 後接 `/` 與新密碼，最多 15 字元，不可含 `'@$/*"`」；命令頁則寫「最多 6 個英文字母」 | 〔待核對，以實測或管理員政策為準〕 |
| 命令縮寫 | 使用說明寫 `PASS`，命令頁寫 `PASSword`、`USERname`（輸入時以 `USER` 簡寫） | 縮寫規則依 44.4.3 |
| `MESSAGE ID` 範例 | 範例 `ID '64da-36'`，說明卻為「process/host identifier 64da-ws36」 | 格式〔待核對〕 |
| `LIST` 的語法圖 | `DBs` 重複出現；範例用 `MDBS`、`DBS` | 不影響使用 |
| `tbstartjob.exe` 與 `marjobstarter.exe` | 同一節兩個名稱 | 〔待核對〕 |
| 平台殘留 | `PDMSEXE`、`PDMSWK`、`PDMSUI`、`PDMS_ID`、`Imacro` 路徑 | 以實際安裝的變數為準 |

## 44.15 常見錯誤

| 症狀 | 常見原因 | 處置 |
|---|---|---|
| 批次作業一開始就結束 | 帳密、專案名錯誤（批次只給 1 次機會） | 先用互動模式驗證相同帳密 |
| 批次作業可讀不可寫 | 沒有 `BATCH COPY`，原件被以 Read-only 開啟 | 加 `BATCH COPY`，並評估磁碟 |
| 批次中途中止留下 COMMS DB 問題 | 被遠端強制中止、佇列有時間限制、磁碟滿 | 見 44.6.3，並對 COMMS DB 跑完整性檢查〔見第 43 章 DICE〕 |
| 進不了 Admin／Lexicon | 帳號是 General，而這兩者是 Restricted | 不要為此提升為 Free，改請管理員代辦 |
| `MDB not found`／`No MDB has been specified` | MDB 名稱未以 `/` 開頭，或還沒選 MDB | 先 `LIST MDBS` 再選 |
| 在大量 Current DB 的 MDB 無法再加 DB | 已達 1000 個 | `DEFER` 或 `EXCHANGE` |
| `EXCHANGE` 後結果怪異 | 多於兩個名稱時配對錯誤 | 兩兩成對，先 Current 後 Deferred，再 `LIST` 驗證 |
| 自家 exe 沒出現在 Log Viewer | 沒有定義在 `MarJobs.xml` | 補 `<application>`（44.11.2） |
| 同事的預設檔改動影響他人 | 改了系統層覆蓋而非使用者層 | 用 `marenvutil` 的 User variables |
| 備份後還原，Hull 預設值不見 | 只備份了資料庫，漏了 `<proj>MAR` 子目錄 | 補進備份清單 |
| 直接改動 `Config`／`Bin` | 官方不得手動編輯 | 還原安裝，改放客製位置 |

## 44.16 本章小結

要點：進入順序為 `PROJECT`、`USERNAME`、選 MDB、切模組；存取權由使用者等級、DB 的 Team 與模式、模組分級三層決定；Current／Deferred 用 `CURRENT`、`DEFER`、`EXCHANGE` 管理，`PROTECT` 只能降權；批次只給一次登入機會、遇錯即停，`BATCH COPY` 累加且副本暫時；Monitor 錯誤皆為 `(39,n)`；Hull 程式由 Job Launcher 依 `MarJobs.xml` 啟動；環境變數優先順序為使用者 ＞ d065 ＞ 系統；`SA004` 僅限管理員。

## 44.17 練習題（只能在訓練專案或唯讀測試環境）

1. 以 General 帳號登入 Monitor，用 `STATUS` 與 `LIST MDBS` 記錄你的 MDB、Current DB 與各 DB 的 RW／R；再用 `SYSTAT` 比較。
2. 在 MDB 中以 `PROTECT` 將一個 RW 的 DB 降為 `READ`，再用 `STATUS` 驗證；嘗試再把它升回 `RW`，記錄結果並解釋原因。
3. 用 `Q DB team/db FILE`、`NUMBER`、`SIZE` 找出三個 DB 的實際檔名與大小，並與磁碟實際檔案核對。
4. 故意輸入不存在的 MDB、DB、Team，記錄 `(39,3)`、`(39,4)`、`(39,5)`，並對照 44.9 的處置欄。
5. 寫出一份批次作業需求書：它要複製哪些 DB？副本會佔多少磁碟？帳密放哪裡？失敗時如何通知？
6. 用 `marenvutil` 為自己的 Windows 帳號覆蓋一個無害變數（例如 `SB_TEST`），確認不影響其他帳號與 d065，再 `Remove`。
7. 在測試安裝內，依 44.11.3 的格式把一支唯讀的主控台程式定義進 `MarJobs.xml`（先備份），用三種 `marjobstarter` 命令各跑一次，查看輸出位置。

## 44.18 自我檢核

- [ ] 我能依序說出進入 Marine 的五個步驟，以及每一步可能出現的錯誤。
- [ ] 我能解釋 General 使用者為什麼進不了 Admin。
- [ ] 我能說出 Current、Deferred 與 `EXCHANGE` 配對規則。
- [ ] 我知道批次模式與互動模式在登入次數與錯誤處理上的差異。
- [ ] 我能舉出至少五個 `(39,n)` 錯誤與處置。
- [ ] 我能說出 Session、Job、Job file 與 `MarJobs.xml` 的關係。
- [ ] 我知道環境變數三層覆蓋順序，以及 `marenvutil` 不會修改 d065。
- [ ] 我知道 `SA004` 屬於管理員工具，使用前要備份。

## 44.19 待核對項目與取材覆蓋

> 〔待核對〕項目彙整：見[附錄 D 第 44 章](appx_d_verification_zh-TW.reading.html#ch44)；取材覆蓋與未讀範圍：見[附錄 E 第 44 章](appx_e_coverage_zh-TW.reading.html#ch44)。
