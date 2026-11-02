from pathlib import Path
import markdown
from html import escape

root = Path(__file__).resolve().parent
# 課程結構：章號 -> 部分。章節檔以 chNN_* 命名，標題取自檔案第一行（# 標題）。
PARTS = [
    ('課程總覽', [0]),
    ('第一部分　入門與資料模型', range(1, 8)),
    ('第二部分　船體設計', range(8, 17)),
    ('第三部分　舾裝設計', range(17, 25)),
    ('第四部分　目錄與圖面', range(25, 31)),
    ('第五部分　二次開發', range(31, 43)),
    ('第六部分　系統管理與維運', range(43, 48)),
]
APPX = '附錄'


def first_heading(path):
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError(f'{path.name} 沒有標題')


books = []
for stage, nums in PARTS:
    for n in nums:
        found = sorted(root.glob(f'ch{n:02d}_*_zh-TW.md'))
        if len(found) != 1:
            raise SystemExit(f'第 {n} 章檔案數不是 1：{[f.name for f in found]}')
        books.append((found[0].name, first_heading(found[0]), stage))
for path in sorted(root.glob('appx_*_zh-TW.md')):
    books.append((path.name, first_heading(path), APPX))
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


# 舊章號網址的轉址頁（章節重新編號後，避免已發佈或收藏的連結失效）
import json as _json
_redir = root / 'legacy_redirects.json'
if _redir.exists():
    for old, new in _json.loads(_redir.read_text(encoding='utf-8')).items():
        if old == new:
            continue
        (root / old).write_text(
            '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{new}">'
            '<title>章節已移動</title></head><body style="font:16px/1.8 sans-serif;max-width:640px;margin:60px auto;padding:0 20px">'
            f'<p>本章已改為新的章號與網址，<a href="{new}">請前往新位置</a>。</p></body></html>',
            encoding='utf-8')
