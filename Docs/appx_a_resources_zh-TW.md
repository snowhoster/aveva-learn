# 附錄 A　專業資源與官方訓練地圖

> 本附錄整理學習 AVEVA Marine 與二次開發可用的外部資源，依**可信度與合法性**分級，並對應到本課程的章節。本課程是自主撰寫的導讀；要達到專業水準，最終仍需要官方文件、官方訓練與公司內部標準。
>
> **資料可信度：** 連結於 2026-10-28 調查確認；2026-11-02 兩度增補 E3D 3.1 手冊、論文、專利、標準與社群資源。`docs.aveva.com` 需要在瀏覽器中啟用 JavaScript 才能閱讀；`help.aveva.com` 上的 E3D 靜態頁面可以直接開啟，但版本有 1.1、2.1 與 3.1 三代，與 Marine 12.1 屬同一技術系譜，細節可能不同。訓練手冊編號來自公開搜尋摘要，標為〔待核對〕者請向 AVEVA 或授權代理商確認。ISO 官方頁對自動抓取回 403，瀏覽器可正常開啟；本課程只連摘要頁，不轉載條文。
>
> **想讀重點而不是只看清單？** 本附錄只告訴你「哪裡有資料」；每份資料的繁中摘要、閱讀順序與可借鏡的做法，整理在[附錄 C　參考文獻導讀與繁中摘要](appx_c_reading_list_zh-TW.reading.html)。

## A.1 資源分級原則

| 等級 | 說明 | 使用方式 |
|---|---|---|
| A 官方 | AVEVA 官方文件、產品內附說明、官方訓練、官方產品資料 | 作為最終依據 |
| B 學術 | 同儕審查的期刊論文、開放取用文章 | 作為方法與案例參考 |
| C 社群 | 資深開發者文章、開源專案、影片課程 | 作為入門與靈感，須自行驗證 |
| 不建議 | 未經授權轉載的官方手冊（各類 PDF 分享站） | 不下載、不散布；改向公司或 AVEVA 取得授權版本 |

> **專業提醒：** 網路上可以搜到許多官方訓練手冊的轉載 PDF。這些檔案的版權屬於 AVEVA，公司使用有法律風險，版本也無法確認。本課程不收錄、也不連結這些檔案。

## A.2 A 級：官方資源

### A.2.1 Marine 12.1 線上文件

| 資源 | 內容 | 連結 | 對應章節 |
|---|---|---|---|
| Hull and Outfitting 12.1 文件入口 | Marine 12.1 全部線上說明；12.1 起不再另外提供 PDF 手冊 | [docs.aveva.com](https://docs.aveva.com/bundle/hull-and-outfitting/page/1224159.html) | 全部 |
| Navigating the AVEVA Marine Documentation | 文件的組織方式：Hull Basic Features and Concepts、Hull Structural Design、Design、Draft、Marine Customization 等 | [連結](https://docs.aveva.com/bundle/hull-and-outfitting/page/1225292.html) | 第 1 章 |
| Hull Detailed Design 版本說明 | 各 SP 的新功能，例如 12.1 SP4 的套料改善 | [連結](https://docs.aveva.com/bundle/hull-and-outfitting/page/1224401.html) | 第 5、6、17 章 |
| Planar Hull 面板概念 | 平面板架的組成 | [連結](https://docs.aveva.com/bundle/hull-and-outfitting/page/1110536.html) | 第 5 章 |

12.1 文件的主題包括：Hull Detailed Design、Hull Structural Design、Marine Drafting、Outfitting Draft、Outfitting Module、Outfitting Design Applications、Assembly Planning、Weld Planning、Design Reuse。

### A.2.2 E3D 3.1 手冊入口（靜態頁，2026-11 增補）

`help.aveva.com` 的 E3D 3.1 手冊是靜態頁，可直接開啟、加書籤與全文搜尋，是目前**最完整的免費官方語法與架構參考**。它與 Marine 12.1 同源，但 API、名稱空間與部分功能有版本差異；語法看 3.1、Marine 專屬功能看 12.1，衝突時以公司安裝版本為準。

| 手冊 | 入口 | 內容 | 對應章節 |
|---|---|---|---|
| PML Customisation | [PMLCG_FP](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG_FP.html) | PML／PML2 語言、物件、陣列、錯誤、檔案、表單、選單、Add-in | 第 11–13、16、17 章 |
| .NET Customisation | [NCUG_FP](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG_FP.html) | CAF Add-in、ServiceManager、資料庫 API、PML.NET、Grid 控制項 | 第 13、14 章 |
| Data Model | [DMRM_FP](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM_FP.html) | 元素型別與屬性字典（`HPANEL`、`HSTIFF`、`CHOLE` 等） | 第 3、5、7 章 |
| Catalogues and Specifications | [CSUG_FP](https://help.aveva.com/AVEVA_Everything3D/3.1/CSUG/CSUG_FP.html) | 目錄、等級、選擇條件與參數化元件 | 第 8 章 |
| ISODRAFT | [ISOUG_FP](https://help.aveva.com/AVEVA_Everything3D/3.1/ISOUG/ISOUG_FP.html) | ISO 圖類型、出圖指令、標註與材料表 | 第 9 章 |
| Database Management Reference | [DBRM_FP](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM_FP.html) | 屬性型別、查詢屬性、偽屬性、相對定位與方向 | 第 3、4、12、16 章 |
| Software Customisation Reference | [SCRM_FP](https://help.aveva.com/AVEVA_Everything3D/3.1/SCRM/SCRM_FP.html) | PML 物件與指令字典：FILE、WRT、Gadget、資料庫物件的方法與參數 | 第 11、12、13、16 章 |

**精選主題頁：** PML 物件模型 [3.03.01](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG3.03.01.html)、陣列 [7.07.01](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG7.07.01.html)、錯誤處理 [11.11.1](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG11.11.1.html)、表單入門 [14.14.1](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG14.14.1.html)、PML Add-in [24.27.01](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG24.27.01.html)；.NET 的 `IAddin` [2.03.02](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG2.03.02.html)、環境變數 [3.04.3](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG3.04.3.html)、PML.NET [5.07.3](https://help.aveva.com/AVEVA_Everything3D/3.1/NCUG/NCUG5.07.3.html)；資料模型的 `HPANEL` [5.09.406](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.406.html)、`HSTIFF` [5.09.419](https://help.aveva.com/AVEVA_Everything3D/3.1/DMRM/DMRM5.09.419.html)。

**資料庫與程式設計字典：** 屬性 [DBRM3.04.01](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM3.04.01.html)、查詢屬性 [DBRM3.04.09](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM3.04.09.html)、偽屬性 [DBRM1.02.17](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM1.02.17.html)、相對定位 [DBRM3.04.14](https://help.aveva.com/AVEVA_Everything3D/3.1/DBRM/DBRM3.04.14.html)；`FILE` 物件 [SCRM3.3.37](https://help.aveva.com/AVEVA_Everything3D/3.1/SCRM/SCRM3.3.37.html)、`WRT` [SCRM6.5.18](https://help.aveva.com/AVEVA_Everything3D/3.1/SCRM/SCRM6.5.18.html)。

### A.2.3 E3D 2.1 精選靜態頁（既有連結，版本較舊）

這些頁面是 E3D 2.1 的官方說明，PML 語法、資料模型與 .NET 架構與 Marine 12.1 同源，適合對照本課程既有章節；名稱空間、組件版本與 Marine 專屬功能請以公司安裝版本為準。

| 文件 | 版本 | 內容 | 對應章節 |
|---|---|---|---|
| [.NET Customisation User Guide：環境變數](https://help.aveva.com/AVEVA_Everything3D/2.1/NCUG/NCUG3.04.3.html) | E3D 2.1 | `CAF_ADDINS_PATH`、`CAF_UIC_PATH`、Addins.xml 與 Customization.xml 的搜尋規則 | 第 14 章 |
| [.NET Customisation User Guide：Using PML.NET](https://help.aveva.com/AVEVA_Everything3D/2.1/NCUG/NCUG5.07.3.html) | E3D 2.1 | `import`、`using namespace`、`Assign`、型別對應、事件、例外、限制 | 第 14 章 |
| [.NET Customisation User Guide：PMLGridExample](https://help.aveva.com/AVEVA_Everything3D/2.1/NCUG/NCUG1.02.17.html) | E3D 2.1 | PML 表單中使用 .NET 表格的官方範例（安裝目錄 `Samples.zip`） | 第 13、14 章 |
| [PML Customisation User Guide：檔案處理](https://help.aveva.com/AVEVA_Everything3D/2.1/PMLPUG/PMLCG12.12.1.html) | E3D 2.1 | `FILE` 物件、讀寫、錯誤處理 | 第 16 章 |
| [Software Customisation Reference Manual：FILE 物件](https://help.aveva.com/AVEVA_Everything3D/2.1/SCRM/SCRM3.3.37.html) | E3D 2.1 | 物件方法參考 | 第 11、16 章 |
| [PML Publisher](https://help.aveva.com/AVEVA_Everything3D/1.1/PMLPUG/PMLPUG3.3.01.html) | E3D 1.1 | `pmlencrypt.exe` 加密工具 | 第 17 章 |
| [Data Model Reference（HPANEL 等）](https://help.aveva.com/AVEVA_Everything3D/2.1/DMRM/DMRM5.09.419.html) | E3D 2.1 | 元素型別與屬性 | 第 3、5 章 |
| [Catalogues and Specifications User Guide](https://help.aveva.com/AVEVA_Everything3D/2.1/CSUG/CSUG3.03.02.html) | E3D 2.1 | 目錄與等級觀念 | 第 8 章 |

### A.2.4 產品內附文件（公司安裝目錄）

Marine 12.1 的安裝目錄 `Documentation\` 附有大量說明檔與範例，是**版本最吻合**的官方資料。以下清單整理自開源知識庫對 12.1 SP4 安裝目錄的調查〔待核對：公司安裝是否完整〕：

| 檔案 | 內容 | 對應章節 |
|---|---|---|
| `PMLPUG.chm`、`Customisation_Guide.chm`、`SOFTCG.chm` | PML 使用手冊與客製化指南 | 第 10 至 13 章 |
| `Setup_Customisation.chm` | 環境變數與安裝客製化 | 第 1、10 章 |
| `Dictionary.chm` | 屬性與物件字典 | 第 3 章 |
| `Vitesse.chm`、`Python.chm`、`Data_Extraction.chm`、`vitesse_access.xls` | Vitesse 與資料抽取 | 第 15 章 |
| `NETmarAPI.chm`、`marAPI.chm`、`NETAveva.Marine.PlanarAPI.chm` | Marine 專屬 .NET API | 第 14、15 章 |
| 安裝根目錄的 `ApplicationFramework.xml`、`ApplicationFramework.Presentation.xml` | CAF 框架的 API 說明（Visual Studio 可直接顯示） | 第 14 章 |
| `Samples\`（含 `Samples.zip`） | 官方 C# 範例：ExamplesAddin、AttributeBrowserAddin、NetGridExample、PMLNetExample、PMLGridExample、ImportDXF | 第 14、16 章 |
| `Vitesse\Examples\` | 官方 Vitesse 範例 `kcs_ex_*.py` | 第 15 章 |

> **開發人員須知：** 遇到 API 問題時，查找順序建議是：產品內附文件與官方範例 → help.aveva.com 的 E3D 頁面（注意版本差異）→ 開源知識庫 → 網路文章。越往後越需要在實機驗證。

### A.2.5 官方訓練

| 資源 | 說明 | 連結 |
|---|---|---|
| AVEVA Learning Academy | AVEVA 統一的訓練平台：講師授課、自學課程、實作練習與認證 | [learningacademy.aveva.com](https://learningacademy.aveva.com/) |
| Marine 12.1.5 Hull Detailed Design – Planar Hull Modelling | 講師授課，目標是建立達生產標準的平面船體板架 | [課程頁](https://learningacademy.aveva.com/courses/aveva-marine-1215-hull-detailed-design-planar-hull-modelling-instructor-led-training) |
| Marine 12.1.5 Hull Instructor-Led Training | 船體系列講師授課課程 | [課程頁](https://learningacademy.aveva.com/courses/aveva-marine-1215-hull-instructor-led-training?courseId=d63a15bc-661e-4bad-a9d1-83a9948ac326) |

### A.2.6 官方訓練手冊編號（請向公司或 AVEVA 申請授權版本）

依公開搜尋結果整理，請 IT 或訓練負責人確認公司是否已取得：

| 編號 | 名稱 | 對應本課程章節 |
|---|---|---|
| TM-2101 | Hull Structural Design | 第 5 章 |
| TM-2102 | Hull Detailed Design – Planar Hull Modelling | 第 5 章 |
| TM-2103 | Hull Detailed Design – Curved Hull Modelling | 第 5 章 |
| TM-2106 | Hull Detailed Design – Production Information | 第 6 章 |
| TM-1401 | PML Macros and Functions（Plant 系列） | 第 11、12 章 |
| TM-1402 | PML Design Forms and Menus（Plant 系列） | 第 13 章 |
| TM-1403 | PML Applied（Plant 系列） | 第 12、16、17 章 |

〔待核對〕TM-14xx 屬 AVEVA Plant（PDMS）系列，內容與 Marine 舾裝端相通；舾裝、圖面與系統管理也有對應的 TM 手冊，編號請向 AVEVA 確認。

**聯絡窗口：** AVEVA Training and Product Support，或公司的 AVEVA 授權代理商。

### A.2.7 官方產品資料

- [AVEVA Hull and Outfitting Datasheet](https://www.aveva.com/content/dam/aveva/documents/perspectives/datasheets/Datasheet_HullandOutfitting.pdf.coredownload.inline.pdf)（本課程 `images/aveva/` 截圖來源）
- [AVEVA Hull Detailed Design Brochure](https://www.aveva.com/content/dam/aveva/documents/brochures/Brochure_AVEVA_HullDetailedDesign_11-18.pdf)
- [AVEVA Outfitting Brochure](https://www.aveva.com/content/dam/aveva/documents/brochures/Brochure_AVEVA_Outfitting.pdf)
- [AVEVA Hull and Outfitting 產品頁](https://www.aveva.com/en/products/hull-and-outfitting/)

## A.3 B 級：學術論文

| 論文 | 主題 | 取得方式 | 對應章節 |
|---|---|---|---|
| Kim, Park & Yang (2020), JAMET 44(3) | 以 AVEVA Marine 自動產生外板開孔，附實機畫面與 PML 程式 | [開放取用](https://doi.org/10.5916/jamet.2020.44.3.196) | 第 7、15、17、18 章 |
| Son, Kang & Kim (2014), Trans. Soc. CAD/CAM Engineers | 分析 AVEVA Marine 的 Scheme 檔，開發船體區塊複製與重用程式 | [DOI](https://doi.org/10.7315/cadcam.2014.041) | 第 5、6 章 |
| Cheon 等 (2013), Trans. Soc. CAD/CAM Engineers | AVEVA Marine 管模型轉到 SmartMarine3D 的對應方法 | [DOI](https://doi.org/10.7315/cadcam.2013.329) | 第 7、16 章 |
| Han 等 (2021), Ships and Offshore Structures | AVEVA Marine 與 Intergraph Smart 3D 的船體結構資料轉換 | [DOI](https://doi.org/10.1080/17445302.2021.1998852) | 第 5、16 章 |
| Li 等 (2024), IJNAOE 16 | 從 AM 模型抽取資料，建立船體區塊吊裝整合設計系統（CC BY-NC-ND） | [DOI](https://doi.org/10.1016/j.ijnaoe.2024.100593) | 第 6、16 章 |
| Kunkera 等 (2022), Applied Sciences 12(24) | 造船專案導入數位孿生的資料整合與組織課題（CC BY） | [DOI](https://doi.org/10.3390/app122412721) | 第 1、16 章 |
| 大韓造船學會特別論文集 (2013) | 以 AVEVA Marine 自動套用鋼料餘量的建模系統 | [KoreaScience](https://koreascience.kr/article/CFKO201323436147171.pub) | 第 6 章 |
| 《造船技術》(2022) 第 1 期 | 以 PML 快速建立艙室曲面絕緣與型材絕緣 | [CNKI 書目](https://www.cnki.com.cn/Article/CJFDTotal-ZCJS202201005.htm) | 第 7 章 |
| 賀幫永、張乖平 (2024)，《廣東造船》 | AVEVA Marine 在船體生產設計中的應用 | [NAPSTIC](https://search.napstic.cn/literature/periodical/010gdzc202401018) | 第 6 章 |
| 王星宇等 (2024) | C# 二次開發加快船舶元件庫建立 | [NAPSTIC](https://search.napstic.cn/literature/periodical/010zcjs202401018) | 第 8、14 章 |
| 《海洋工程裝備與技術》(2018) 5(1) | PDMS 二次開發在海上石油平台的應用 | [上海交大期刊網](https://www.qk.sjtu.edu.cn/oeet/CN/Y2018/V5/I1/74) | 第 12、18 章 |
| Li 等 (2024), Chinese Journal of Ship Research 19(5) | 解析 AM 匯出的船體 XML，簡化特徵後快速建立 FEM 模型 | [DOI](https://doi.org/10.19693/j.issn.1673-3185.03660) | 第 6、16、18 章 |
| Yang 等 (2022), AVEVA World Conference | K-SUPPORT：資料驅動的管支架選型、建模、出圖與 BOM 自動化 | [簡報 PDF](https://cdn.osisoft.com/osi/presentations/2022-AVEVA-San-Francisco/UC22NA-03EE10-KEPCO-Yang-Data-centric-piping-support.pdf) | 第 7、9、16、18 章 |

**專利與產業標準（不是同儕審查文獻，引用時請註明性質）：**

| 文獻 | 主題 | 取得方式 | 對應章節 |
|---|---|---|---|
| CN104537150A（2015-04-22 公開） | 在 PDMS 中以 PML 統計管支架型材與管卡材料 | [Google Patents](https://patents.google.com/patent/CN104537150A/zh) | 第 7、9、16 章 |
| CN122133263A（2026-06-02 公開） | 以自然語言、向量資料庫與 PML 生成建模語句（中遠海運重工揚州） | [Google Patents](https://patents.google.com/patent/CN122133263A/zh) | 第 11、13 章 |
| ISO 10303-242:2022（STEP AP242） | 跨 CAD 交換 3D 模型、組立與 PMI 的國際標準 | [ISO 摘要頁](https://www.iso.org/standard/84667.html)（條文需付費） | 第 16 章 |

更多論文可在中國知網、萬方以 `AVEVA Marine`、`PDMS 船舶`、`船体生产设计` 等關鍵字搜尋；韓國論文可在 KoreaScience 以 `AVEVA Marine` 搜尋。

**學位論文：**

| 論文 | 主題 | 取得方式 | 對應章節 |
|---|---|---|---|
| LUT University（作者與年份〔待核對〕） | 船體結構特徵在 CAD 之間的資料轉移 | [PDF](https://lutpub.lut.fi/bitstream/10024/164883/1/3D%20-%20MODEL%20DATA%20TRANSFER%20OF%20SHIP%20HULL%20STRUCTURE%20FEATURES%20BETWEEN%20CAD%20PROGRAMS.pdf) | 第 5、6、16 章 |
| 逯濤 (2019)，大連理工大學碩士論文 | AVEVA Marine 船體生產設計軟體的二次開發（簡體中文，全文待讀） | CNKI 收錄，需機構帳號 | 第 5、6、15、16 章 |
| Hmeshah (2016)，University of Rostock 博士論文 | 造船產品資料模型的品質管理；附錄含 AVEVA Marine XML 範例 | [PDF（開放取用）](https://rosdok.uni-rostock.de/file/rosdok_disshab_0000001750/rosdok_derivate_0000037174/Dissertation_Hmeshah_2017.pdf) | 第 6、16、17 章 |
| Lee Eunse (2019)，木浦大學碩士論文 | 以 3D 設計資訊計算管支架塗裝量（韓文，全文待讀） | [dCollection 書目](https://dcollection.mokpo.ac.kr/srch/srchDetail/000000022239) | 第 7、9、16 章 |

## A.4 C 級：社群資源

### A.4.1 開發

| 資源 | 說明 | 對應章節 | 使用注意 |
|---|---|---|---|
| [aveva-marine-dev-skill](https://github.com/912141548/aveva-marine-dev-skill) | Marine 12.1 SP4 二次開發知識庫：PML、17 卷命令參考、.NET API、marAPI、Vitesse、範本與檢查工具。本課程三個範例的來源 | 第 10 至 18 章 | 此連結是 fork；上游為 [erbi112211-boop/aveva-marine-dev-skill](https://github.com/erbi112211-boop/aveva-marine-dev-skill)。`TODO-UNVERIFIED` 須實機確認；腳本需經公司審查才能執行 |
| [PDMS-12.1-Net-skill](https://github.com/garychemis/PDMS-12.1-Net-skill) | PDMS 12.1 .NET Public Interface 的 API 文件整理（已併入上一項） | 第 14 章 | API 文件源自 PDMS 12.0 時代，與 E3D 有差異 |
| [AVEVA Community：PDMS／E3D 討論區](https://community.aveva.com/aveva-engineering/pdms-e3d-forum/) | 官方社群論壇，含 Isodraft、PML、模組操作與錯誤排除的實際問答 | 全課程 | 回答品質不一；版本與環境要自行核對，勿直接貼公司資料 |
| [AVEVA Community：Macros & Tools 版](https://community.aveva.com/aveva-engineering/pdms-e3d-forum/f/macros-tools/) | 巨集與工具專版：`PML REHASH`、表單版面、工具列客製、跨版本失效等問題 | 第 11、13、17 章 | 搜尋時貼錯誤訊息原文，找到答案仍要在訓練專案重現 |
| [南勝 NanSheng：C# 二次開發系列](https://www.cnblogs.com/NanShengBlogs/p/11107956.html) | 四篇實作紀錄：入門與 DLL 掛載、讀取分段、批次抽板架、呼叫 MarJobLauncher | 第 3、5、9、14、17 章 | 個人實作紀錄，無版本矩陣；照做前先備份載入設定 |
| [eryar：AVEVA .NET Quick Start Guide](https://developer.aliyun.com/article/235787) | .NET Add-in 入門（2012） | 第 14 章 | 版本較舊 |
| [eryar：用 PML 寫管支架程序](https://blog.csdn.net/eryar/article/details/4457072) | 物件化 PML 工具的實例 | 第 18 章 | 版本較舊 |
| [PoByBolek/PmlUnit](https://github.com/PoByBolek/PmlUnit) | PML 單元測試框架 | 第 17 章 | 與 Marine 12.1 的相容性〔待核對〕 |
| [k-awata/pml-json](https://github.com/k-awata/pml-json)、[k-awata/pmlsqlite](https://github.com/k-awata/pmlsqlite) | PML 的 JSON 編解碼、SQLite 存取 | 第 16 章 | 以 E3D 為主，Marine 相容性〔待核對〕 |

### A.4.2 操作與影片

| 資源 | 說明 | 對應章節 |
|---|---|---|
| [龍船學院：AVEVA MARINE 船舶生產設計基礎教學](https://edu.imarine.cn/course-248.html) | 平面建模系列：板架與邊界、板縫坡口焊接、曲線拓撲、型材、折邊端切、角隅開孔、肘板 Scheme | 第 5 章 |
| [Bilibili：AM 船舶生產設計基礎教學：平面建模](https://www.bilibili.com/video/av721011726/) | 與上述課程對應的 8 集影片 | 第 5 章 |
| [龍船社區 AVEVA MARINE 版](https://club.imarine.cn/softtec/t52-2.html) | 中文使用者討論區 | 全部 |
| [YouTube：AVEVA E3D – PML 播放清單](https://www.youtube.com/playlist?list=PLjChkog_p_LGhfPnFczX64gLhZsX6rxwx) | 短示範：mesh 建 primitive、TDS PML 清單、PMLCMD 與介面客製 | 第 11、13、16 章 |

### A.4.3 產業動態

- Zaliv Ship Design：[AVEVA Marine Curved Hull Modeling 訓練紀錄](https://www.zalivdesign.com/the-training-of-aveva-marine-curved-hull-modeling/)（2019，三天課程，可作為內訓排程參考）。

## A.5 依章節的資源地圖

| 章 | 主題 | 首選資源 | 補充資源 |
|---|---|---|---|
| 1 | 產品架構與啟動 | 12.1 文件入口、Navigating 頁、`Setup_Customisation.chm` | Datasheet |
| 2 | 專案、資料庫與權限 | 12.1 文件（Admin、Monitor 主題） | 公司系統管理員 |
| 3 | 資料階層與屬性 | `Dictionary.chm`、Data Model Reference | DBRM 屬性／查詢屬性／偽屬性（A.2.2）、開源知識庫的元素屬性表 |
| 4 | 座標與幾何 | 12.1 文件（Hull Basic Features and Concepts） | DBRM 相對定位、SCRM 的 `WRT`（A.2.2） |
| 5 | 船體建模 | TM-2101／2102／2103、Planar Hull 面板概念 | 龍船學院影片、Son 等 (2014) Scheme 重用、逯濤 (2019) |
| 6 | 船體生產資訊 | TM-2106、Hull Detailed Design 版本說明 | Li 等 (2024) 吊裝系統、Li 等 (2024) XML→FEM、Hmeshah (2016)、2013 韓國論文、2024《廣東造船》 |
| 7 | 舾裝設計 | 12.1 文件（Outfitting 主題） | Datasheet、JAMET 論文、艙室絕緣論文、K-SUPPORT、CN104537150A、Lee (2019) |
| 8 | 目錄與等級 | Catalogues and Specifications User Guide（3.1 入口見 A.2.2） | 王星宇等 2024 |
| 9 | 圖面與報表 | 12.1 文件（Marine Drafting、Outfitting Draft） | ISODRAFT 3.1 手冊（A.2.2）、K-SUPPORT 出圖段、南勝 MarJobLauncher |
| 10 | 開發環境 | `Customisation_Guide.chm`、`Setup_Customisation.chm` | 開源知識庫 PML 開發技能 |
| 11 | PML 語言 | `PMLPUG.chm`、TM-1401 | [PML 互動課程](aveva_pml_learning_guide.html)、SCRM 物件字典、CN122133263A、YouTube PML 清單 |
| 12 | PML 資料庫操作 | `PMLPUG.chm`、TM-1403 | DBRM 查詢屬性與偽屬性、開源知識庫屬性操作卷 |
| 13 | 表單與 Add-in | TM-1402、PMLGridExample | MyCollect 範例、SCRM、AVEVA Community Macros & Tools |
| 14 | .NET | .NET Customisation 3.1（A.2.2）、安裝目錄 `Samples\` | MyBrowser 範例、南勝 C# 系列、eryar 入門 |
| 15 | Vitesse | `Vitesse.chm`、`Data_Extraction.chm`、`Vitesse\Examples\` | Vitesse 報表範例、JAMET 論文 |
| 16 | 報表與整合 | PML Customisation 檔案章節（A.2.2） | Cheon 等 (2013)、Han 等 (2021)、ISO 10303-242、Hmeshah (2016)、pml-json、pmlsqlite |
| 17 | 除錯與部署 | PML Publisher、PML 3.1 追蹤章節（A.2.2） | PmlUnit、AVEVA Community Macros & Tools、Hmeshah (2016) 的檢查框架 |
| 18 | 案例 | JAMET 論文 | K-SUPPORT、中文期刊論文、2025 鐵舾二次開發文章 |

> **延伸閱讀：** 上表的資料「怎麼讀、先讀哪一段、能帶走什麼」，見[附錄 C](appx_c_reading_list_zh-TW.reading.html)。C.7 另有一份依章節排列的閱讀路線。

## A.6 建議的專業進修路線

對應第 0 章的能力等級：

| 等級 | 目標 | 本課程 | 外部資源 |
|---|---|---|---|
| L1 使用者 | 瀏覽模型、查詢屬性、看懂圖面 | [第 1 至 4 章](ch01_architecture_zh-TW.reading.html) | 12.1 線上文件、龍船學院影片 |
| L2 領域理解 | 說明船體與舾裝的資料關係與設計流程 | [第 5 至 9 章](ch05_hull_modelling_zh-TW.reading.html) | TM-2101 至 2106、Learning Academy 課程 |
| L3 工具開發 | 唯讀查詢、報表與表單工具 | [第 10 至 13 章](ch10_dev_environment_zh-TW.reading.html)、[第 16 章](ch16_reports_integration_zh-TW.reading.html) | TM-1401、1402、`PMLPUG.chm` |
| L4 進階開發 | 建立／修改工具、.NET 外掛、船體抽取 | [第 12 章](ch12_pml_database_zh-TW.reading.html)、[第 14 章](ch14_dotnet_zh-TW.reading.html)、[第 15 章](ch15_hull_vitesse_zh-TW.reading.html) | .NET Customisation User Guide、`Vitesse.chm`、開源知識庫 |
| L5 工具負責人 | 工具架構、規範、部署與維護流程 | [第 17 章](ch17_debug_deploy_zh-TW.reading.html)、[第 18 章](ch18_case_studies_zh-TW.reading.html) | PML Publisher、公司 IT 規範 |

## A.7 向公司確認的事項

要把學習成果用在實際工作上，以下資訊必須向公司取得：

- [ ] AVEVA Marine 的確切版本與 Service Pack。
- [ ] 已授權的模組清單，例如是否有 Curved Hull、Nesting、Assembly Planning。
- [ ] 公司是否已有官方訓練手冊或 Learning Academy 帳號。
- [ ] 安裝目錄的 `Documentation\`、`Samples\`、`Vitesse\Examples\` 是否完整，可否複製到開發機。
- [ ] 肋位／縱向定位系統說明與命名規範。
- [ ] 目錄、等級的維護窗口與申請流程。
- [ ] 訓練專案的位置與開發帳號權限。
- [ ] `PMLLIB`、`PDMSUI`、`CAF_ADDINS_PATH`、`CADC_LANG` 等環境變數的公司設定。
- [ ] PML／.NET／Vitesse 工具的部署、審查與升級流程，以及工具負責人。

## A.8 使用與授權注意

| 資源 | 注意事項 |
|---|---|
| AVEVA 官方文件與截圖 | 版權屬於 AVEVA。本課程只做摘要與導讀，截圖僅供公司內部教學辨識介面，不對外散布；完整翻譯或散布需取得授權 |
| JAMET 論文圖片 | CC BY-NC 3.0，非商業用途並註明出處 |
| aveva-marine-dev-skill 範例 | MIT 授權，保留授權聲明（見 [`examples/LICENSE-aveva-marine-dev-skill.txt`](examples/LICENSE-aveva-marine-dev-skill.txt)） |
| 開源腳本 | 下載後先依公司資安規範審查，不要直接在生產環境執行 |
| 部落格與影片 | 版權屬原作者；引用時註明出處，不整段轉載 |

## 資料來源

- 本附錄所列連結，於 2026-10-28 調查確認；E3D 3.1 手冊、論文、專利、標準與社群資源於 2026-11-02 兩度增補。官方文件見 A.2，論文見 A.3，社群資源見 A.4。
- E3D 3.1 手冊目錄與主題頁：`help.aveva.com/AVEVA_Everything3D/3.1/` 的 PMLPUG、NCUG、DMRM、CSUG、ISOUG、DBRM、SCRM 靜態頁（共 7 本入口、40 個主題頁）。
- 論文書目與 DOI：Crossref API 查詢結果（2026-11-02）；K-SUPPORT 簡報取自 AVEVA World 2022 公開議程。
- 專利：Google Patents（CN104537150A、CN122133263A）；標準：ISO 官方摘要頁（條文需付費，未轉載）。
- 產品內附文件清單：開源知識庫 [aveva-marine-dev-skill](https://github.com/912141548/aveva-marine-dev-skill)（上游 [erbi112211-boop](https://github.com/erbi112211-boop/aveva-marine-dev-skill)）之《AVEVA-Marine-NET開發技能》《AVEVA-Marine-PML開發技能》《Marine-Vitesse-Python軌道速查》。
- 訓練手冊編號：AVEVA 公開課程與搜尋結果摘要；TM-14xx 系列參考本課程 PML 互動課程頁的整理。
- 無法自動取得的資源：`docs.aveva.com` 的 Marine 12.1 需 JavaScript；ISO 官方頁對自動抓取回 403；ResearchGate、CNKI 全文需帳號。
- 每份資料的繁中摘要與查核狀態，見[附錄 C](appx_c_reading_list_zh-TW.reading.html)。
