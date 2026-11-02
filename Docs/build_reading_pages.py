from pathlib import Path
import markdown
from html import escape

root = Path(__file__).resolve().parent
# 依課程章節排序：(檔名, 標題, 部分)
PART0 = '課程總覽'
PART1 = '第一部分　系統與資料模型'
PART2 = '第二部分　船舶設計業務領域'
PART3 = '第三部分　二次開發技術'
PART4 = '第四部分　系統管理與維運'
PART5 = '第五部分　設計領域補充'
PART6 = '第六部分　官方文件深入'
APPX = '附錄'
books = [
    ('ch00_knowledge_map_zh-TW.md', '第 0 章　課程總覽與知識地圖', PART0),
    ('ch01_architecture_zh-TW.md', '第 1 章　產品架構、模組與啟動環境', PART1),
    ('ch02_project_database_zh-TW.md', '第 2 章　專案、資料庫、MDB 與權限', PART1),
    ('ch03_hierarchy_attributes_zh-TW.md', '第 3 章　資料階層、元素、屬性與導覽', PART1),
    ('ch04_coordinates_geometry_zh-TW.md', '第 4 章　座標、方向與幾何', PART1),
    ('ch05_hull_modelling_zh-TW.md', '第 5 章　船體建模：曲面、板架與拓撲', PART2),
    ('ch06_hull_production_zh-TW.md', '第 6 章　船體生產資訊、套料與裝配', PART2),
    ('ch07_outfitting_zh-TW.md', '第 7 章　舾裝設計：設備、管路、結構、通風與電纜', PART2),
    ('ch08_catalogue_spec_zh-TW.md', '第 8 章　目錄與等級', PART2),
    ('ch09_drawings_zh-TW.md', '第 9 章　圖面、ISO 圖與報表輸出', PART2),
    ('ch10_dev_environment_zh-TW.md', '第 10 章　開發環境：PMLLIB、檔案類型與部署結構', PART3),
    ('ch11_pml_language_zh-TW.md', '第 11 章　PML 語言核心', PART3),
    ('ch12_pml_database_zh-TW.md', '第 12 章　PML 資料庫操作', PART3),
    ('ch13_pml_forms_addins_zh-TW.md', '第 13 章　PML2 表單、選單與 Add-in', PART3),
    ('ch14_dotnet_zh-TW.md', '第 14 章　.NET 開發：PML.NET 與 CAF Add-in', PART3),
    ('ch15_hull_vitesse_zh-TW.md', '第 15 章　船體開發：Vitesse Python 與資料抽取', PART3),
    ('ch16_reports_integration_zh-TW.md', '第 16 章　報表、檔案與外部系統整合', PART3),
    ('ch17_debug_deploy_zh-TW.md', '第 17 章　除錯、測試、部署與版本管理', PART3),
    ('ch18_case_studies_zh-TW.md', '第 18 章　實戰案例與完整範例', PART3),
    ('ch19_loading_computer_zh-TW.md', '第 19 章　載重電腦整合：從 AVEVA 取得重量重心與水艙資料', PART3),
    ('ch20_system_administration_zh-TW.md', '第 20 章　系統管理與維運：安裝、資料庫、帳號、備份與檔案管理', PART4),
    ('ch21_pipework_zh-TW.md', '第 21 章　管路設計（Pipework）：從 PIPE／BRAN 到 Spool、Isometric 與管支架', PART5),
    ('ch22_structures_zh-TW.md', '第 22 章　結構設計（Structures）：型鋼、板、接頭與平台梯欄', PART5),
    ('ch23_initial_design_zh-TW.md', '第 23 章　初始設計（Initial Design）：型線、曲面、靜水力、艙室與水動力', PART5),
    ('ch24_surface_block_zh-TW.md', '第 24 章　曲面管理與分區：Surface Manager、Block Division 與多視圖專案', PART5),
    ('ch25_space_fem_zh-TW.md', '第 25 章　空間管理與有限元素模型：Space Management 與 Finite Element Model', PART5),
    ('ch26_cable_supports_zh-TW.md', '第 26 章　電纜設計與多專業支撐：Cable Design 與 Multi-Discipline Supports', PART5),
    ('ch27_room_schematics_zh-TW.md', '第 27 章　艙室設計與原理圖：Room Design 與 Schematics', PART5),
    ('ch28_other_modules_zh-TW.md', '第 28 章　其他設計模組速覽：Design Reuse、Area Based ADP、Weld Planning 與 Factory Automation', PART5),
    ('ch29_interfaces_legacy_zh-TW.md', '第 29 章　外部整合與舊版開發工具：Interfaces 與 Legacy Applications', PART5),
    ('ch30_monitor_runtime_zh-TW.md', '第 30 章　Monitor 與 Marine 執行環境：Monitor Reference、Program Environment、Runtime 與命令列工具', PART6),
    ('ch31_draft_admin_production_zh-TW.md', '第 31 章　Draft 圖面管理與出圖流程：Draft Administrator、AutoDRAFT、Drawing Production 與 PLOT', PART6),
    ('ch32_marine_drafting_zh-TW.md', '第 32 章　Marine Drafting 與 Design Draft：船體與舾裝的圖面製作', PART6),
    ('ch33_hull_detail_planar_zh-TW.md', '第 33 章　船體詳細設計（一）：設定與標準、初始化工具、平面板架建模', PART6),
    ('ch34_hull_detail_curved_zh-TW.md', '第 34 章　船體詳細設計（二）：曲面板架建模、選用功能與雜項工具', PART6),
    ('ch35_hull_detail_manufacturing_zh-TW.md', '第 35 章　船體詳細設計（三）：製造資訊與鐵舾裝生產特徵', PART6),
    ('ch36_hull_concepts_zh-TW.md', '第 36 章　船體概念與基礎：Product Information Model、模型物件、拓撲與命名', PART6),
    ('ch37_dabacon_global_zh-TW.md', '第 37 章　船體資料庫與分散式專案：Hull Dabacon 與 Global', PART6),
    ('ch38_assembly_structural_zh-TW.md', '第 38 章　裝配規劃與船體結構初步設計：Assembly Planning 與 Hull Structural Design', PART6),
    ('ch39_hvac_equipment_zh-TW.md', '第 39 章　通風與設備設計：HVAC Designer 與 Equipment', PART6),
    ('ch40_isodraft_zh-TW.md', '第 40 章　管路等角圖：Isodraft', PART6),
    ('ch41_catalogs_specs_deep_zh-TW.md', '第 41 章　目錄與等級深入：Catalogs and Specifications 與 Design Templates', PART6),
    ('ch42_database_management_zh-TW.md', '第 42 章　資料庫管理深入：Database Management、SQL Direct 與 Status Control', PART6),
    ('ch43_data_model_reference_zh-TW.md', '第 43 章　資料模型參考導讀：Data Model Reference Manual', PART6),
    ('ch44_customization_manuals_zh-TW.md', '第 44 章　客製化官方手冊導讀：Software Customization、.NET Customization、Data Access Routines 與 Marine Customization', PART6),
    ('ch45_design_common_zh-TW.md', '第 45 章　設計共通功能：Clash Manager、Data Checker、Design Model Editor 與 Reporting', PART6),
    ('ch46_getting_started_zh-TW.md', '第 46 章　Marine 入門基礎：Getting Started 官方導覽（功能、資料、屬性、GUI 與基本操作）', PART6),
    ('ch47_release_upgrade_zh-TW.md', '第 47 章　12.1 版本說明與升級：Release Bulletin、設定需求與功能變更', PART6),
    ('appx_a_resources_zh-TW.md', '附錄 A　專業資源與官方訓練地圖', APPX),
    ('appx_b_glossary_zh-TW.md', '附錄 B　術語表與指令速查', APPX),
    ('appx_c_reading_list_zh-TW.md', '附錄 C　參考文獻導讀與繁中摘要', APPX),
]
css = '''
:root{color-scheme:light;--ink:#193531;--muted:#60736d;--green:#116b58;--line:#dce6df;--paper:#f4f6f0}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.85 "Segoe UI","Microsoft JhengHei",sans-serif}header{background:#143b35;color:#fff;padding:20px max(24px,calc((100vw - 1300px)/2));}header a{color:#d8f36a;text-decoration:none;font-weight:700;font-size:13px}.wrap{max-width:1300px;margin:auto;padding:34px 24px 70px;display:grid;grid-template-columns:250px minmax(0,1fr);gap:30px}aside{position:sticky;top:25px;align-self:start;max-height:90vh;overflow:auto;padding:18px;border:1px solid var(--line);background:#fff;border-radius:14px}aside strong{font-size:12px;letter-spacing:.1em;color:var(--green)}aside ul{list-style:none;padding-left:14px;margin:8px 0}aside>div>ul{padding-left:0}aside a{font-size:13px;line-height:1.5;text-decoration:none;color:#526963;display:block;padding:4px 0}aside a:hover{color:var(--green)}article{min-width:0;background:#fffefa;border:1px solid var(--line);border-radius:18px;padding:clamp(24px,5vw,60px);box-shadow:0 12px 40px #163b2d0b}h1,h2,h3,h4{line-height:1.35;scroll-margin-top:25px}h1{font-size:clamp(28px,4vw,42px);letter-spacing:-.035em;margin:0 0 24px}h2{font-size:25px;margin:48px 0 16px;padding-bottom:10px;border-bottom:1px solid var(--line)}h3{font-size:19px;margin:30px 0 10px}h4{font-size:16px}p,li{overflow-wrap:anywhere}article img{display:block;max-width:100%;height:auto;margin:20px auto;border:1px solid var(--line);border-radius:14px}li{margin:5px 0}a{color:var(--green)}blockquote{margin:24px 0;padding:5px 20px;border-left:4px solid #7fbca3;background:#f0f7f1;color:#49635a;border-radius:0 10px 10px 0}pre{overflow:auto;background:#122a26;color:#dcece2;border-radius:12px;padding:20px;font:13px/1.7 Consolas,monospace}code{background:#eaf2ec;color:#215c4d;padding:2px 5px;border-radius:4px;font-size:.9em}pre code{padding:0;background:none;color:inherit}table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;min-width:100px}th{background:#edf4ee}hr{border:0;border-top:1px solid var(--line);margin:35px 0}.stage{display:inline-block;margin-bottom:12px;background:#e9f2e9;color:var(--green);font-size:12px;font-weight:800;padding:4px 10px;border-radius:20px}nav.pager{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:50px;padding-top:24px;border-top:1px solid var(--line)}nav.pager a{display:block;padding:14px 16px;border:1px solid var(--line);border-radius:12px;text-decoration:none;font-size:14px}nav.pager a small{display:block;color:var(--muted);font-size:12px}nav.pager .next{grid-column:2;text-align:right}footer{color:var(--muted);font-size:12px;text-align:center;padding:20px}@media(max-width:800px){.wrap{display:block;padding:16px}aside{position:static;max-height:220px;margin-bottom:16px}article{padding:24px 20px}h2{font-size:22px}}
.theme-toggle{border:1px solid #ffffff55;background:transparent;color:#d8f36a;border-radius:20px;padding:6px 14px;font:700 12px/1 "Segoe UI","Microsoft JhengHei",sans-serif;cursor:pointer;margin-left:16px}.theme-toggle:hover{background:#ffffff14}
html[data-theme=dark]{color-scheme:dark}html[data-theme=dark] body{background:#0f1512;color:#d9e5de}html[data-theme=dark] header{background:#0b1210}html[data-theme=dark] aside{background:#141d19;border-color:#2b3a33}html[data-theme=dark] aside a{color:#93a89e}html[data-theme=dark] aside a:hover{color:#79c9ab}html[data-theme=dark] article{background:#161f1a;border-color:#2b3a33;box-shadow:0 12px 40px #00000066}html[data-theme=dark] h2{border-bottom-color:#2b3a33}html[data-theme=dark] a{color:#6cc0a4}html[data-theme=dark] blockquote{background:#1b2620;color:#bccfc5;border-left-color:#43836a}html[data-theme=dark] code{background:#23332c;color:#a5d6bd}html[data-theme=dark] pre{background:#0c1412}html[data-theme=dark] th{background:#1d2a24}html[data-theme=dark] th,html[data-theme=dark] td{border-color:#2c3b34}html[data-theme=dark] hr{border-top-color:#2c3b34}html[data-theme=dark] .stage{background:#20302a;color:#79c9ab}html[data-theme=dark] nav.pager a{border-color:#2c3b34;color:#c6d6cd}html[data-theme=dark] nav.pager a:hover{border-color:#6cc0a4}html[data-theme=dark] footer{color:#7d9188}html[data-theme=dark] article img[src$=".svg"]{filter:invert(.92) hue-rotate(180deg) saturate(.85)}html[data-theme=dark] article img:not([src$=".svg"]){filter:brightness(.82) saturate(.92)}
'''
theme_script = '''<script>(function(){var k='aveva-theme';function cur(){var t=localStorage.getItem(k);if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}cur();document.addEventListener('DOMContentLoaded',function(){var b=document.querySelector('.theme-toggle');if(!b)return;function lbl(){b.textContent=document.documentElement.dataset.theme==='dark'?'☀ 浅色':'🌙 深色';}lbl();b.addEventListener('click',function(){var n=document.documentElement.dataset.theme==='dark'?'light':'dark';localStorage.setItem(k,n);document.documentElement.dataset.theme=n;lbl();});matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(e){if(!localStorage.getItem(k))document.documentElement.dataset.theme=e.matches?'dark':'light';});});})();</script>'''
def reading_name(filename):
    return Path(filename).with_suffix('.reading.html').name


def pager(i):
    links = []
    if i > 0:
        prev_file, prev_title, _ = books[i - 1]
        links.append(f'<a class="prev" href="{reading_name(prev_file)}"><small>← 上一篇</small>{escape(prev_title)}</a>')
    if i < len(books) - 1:
        next_file, next_title, _ = books[i + 1]
        links.append(f'<a class="next" href="{reading_name(next_file)}"><small>下一篇 →</small>{escape(next_title)}</a>')
    return f'<nav class="pager" aria-label="上一篇與下一篇">{"".join(links)}</nav>'


for i, (filename, title, stage) in enumerate(books):
    md = markdown.Markdown(extensions=['toc', 'fenced_code', 'tables', 'sane_lists'])
    content = md.convert((root / filename).read_text(encoding='utf-8-sig'))
    page = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | AVEVA 學習工作室</title><style>{css}</style><script>(function(){{var k='aveva-theme',t=localStorage.getItem(k);if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}})();</script></head><body><header><a href="../index.html">← 返回學習中心</a><button class="theme-toggle" type="button" aria-label="切換深淺色">🌙 深色</button></header><div class="wrap"><aside><strong>目錄 CONTENTS</strong>{md.toc}</aside><article><span class="stage">{escape(stage)} · {i + 1} / {len(books)}</span>{content}{pager(i)}</article></div><footer>AVEVA 學習工作室 · 本地離線教材</footer>{theme_script}</body></html>'''
    (root / reading_name(filename)).write_text(page, encoding='utf-8')



