# 端到端示例:Vitesse Python 船体脚本(Trigger + kcs_dex 抽取 + 右键菜单)

> 第 27 轮:第五个可复制模板——**Python 侧的抽取-报告-右键菜单三件套**(场景:读取船体板数据生成报告;右键菜单触发)。
> 硬约束:**Python 2.6 语法**(`print` 语句/`except X, e`);依据全部来自官方源码——`TBhook_ConfigNote.txt`(kcs_dex 用法)、`trig_draft_popup_menu.py`(上下文注入)、`ctx_menu1.py`(菜单入口)、`kcs_ex_draft1.py`(kcs_ui/kcs_draft 函数族)、Vitesse 速查。

---

## 1. 三件套架构(官方机制)

```
Vitesse\Trigger\trig_draft_popup_menu.py   ← 系统按文件名约定加载,把右键上下文
                                            (ContextPoint/Element/Model/Subpictures)
                                            注入 kcs_draft 模块变量,并 AppendPythonPath
Vitesse\Context_Menu\ctx_my_report.py      ← 菜单项脚本,def run(*args) 入口
Vitesse\Lib\myhelpers.py                    ← 共享工具(kcs_dex 抽取封装)
```

**注册方式**:文件放对目录即生效(系统按 `trig_<模块>_<事件>.py` 约定扫描;菜单项注册见 Basic_Design 的 `kcs_gui.menu_item_usr_add(菜单, 序号, '标签', '脚本名')`)。

## 2. 共享抽取工具(Vitesse\Lib\myhelpers.py)

```python
## -*- coding: utf-8 -*-
import kcs_dex, kcs_util

ok = kcs_util.success()

def get_integer(est):
    """抽取语句 -> INT;est 形如 HULL.PANEL('DECK01').PLA(1).THICKNESS"""
    res = kcs_dex.extract(est)
    if res == ok:
        typ = kcs_dex.next_result()
        if typ == 1:                       # 1=INT, 2=REAL, 3=STRING, >10=索引实数列表
            return kcs_dex.get_int()
    return None

def get_real(est):
    res = kcs_dex.extract(est)
    if res == ok:
        typ = kcs_dex.next_result()
        if typ == 2:
            return kcs_dex.get_real()
    return None

def get_string(est):
    res = kcs_dex.extract(est)
    if res == ok:
        typ = kcs_dex.next_result()
        if typ == 3:
            return kcs_dex.get_string()
    return None

def get_rea_list(est):
    res = kcs_dex.extract(est)
    if res == ok:
        typ = kcs_dex.next_result()
        if typ > 10:                       # 列表:类型码-10 = 元素个数
            n = typ - 10
            return [kcs_dex.get_indexedreal(i) for i in range(n)]
    return []
```
(与官方 TBhook_ConfigNote.txt 的 getIntegerValue/getRealValue/getStringValue/getReaListValue 同构——**先查再抄官方**。)

## 3. 右键菜单脚本(Vitesse\Context_Menu\ctx_my_report.py)

```python
import kcs_draft
import kcs_ui

def run(*args):
    if not hasattr(kcs_draft, 'ContextElement') or kcs_draft.ContextElement is None:
        kcs_ui.message_confirm('No element under cursor!')
        return
    # ContextModel 里取面板名(trig 注入;或 geometry_identify 自取)
    model = getattr(kcs_draft, 'ContextModel', None)
    if model is None:
        kcs_ui.message_confirm('Not a model element.')
        return
    panel = model.get_name()                      # KcsModel 包装类方法
    # 抽取报告
    lines = []
    lines.append('PANEL  %s' % panel)
    thi = get_real("HULL.PANEL('%s').PLA(1).THICKNESS" % panel)
    if thi is not None:
        lines.append('PLATE   t=%s mm' % thi)
    qual = get_string("HULL.PANEL('%s').PLA(1).QUALITY.STRING" % panel)
    if qual:
        lines.append('QUALITY %s' % qual)
    kcs_ui.message_confirm('\n'.join(lines))      # 简单展示;复杂对话框用 wxPython(见 ctx_menu1)
```

## 4. 批处理变体(不经右键,直接跑脚本)

```python
# Vitesse\Lib\my_batch_report.py —— 从 marAPI 触发(MarPythonEngine.RunPythonScript)
# 或独立跑:pythonpath 指到 Vitesse 各目录后 python26 运行(需会话环境,见 evars.bat)
import kcs_ui, kcs_dex
from myhelpers import get_real, get_string

panels = ('DECK01', 'DECK02', 'SIDE01')
out = []
for p in panels:
    t = get_real("HULL.PANEL('%s').PLA(1).THICKNESS" % p)
    q = get_string("HULL.PANEL('%s').PLA(1).QUALITY.STRING" % p)
    out.append('%s  t=%s  Q=%s' % (p, t, q))
f = open('C:/mydev/panel_report.txt', 'w')
f.write('\n'.join(out))
f.close()
```
触发方式三选一:① `MarPythonEngine.RunPythonScript(路径)`(.NET/PML,见 marAPI 姿势表 §3.11);② Trigger 文件内调用;③ Basic_Design 菜单项(`menu_item_usr_add` 指脚本名)。

## 5. 官方细节与坑

| 要点 | 出处 |
|---|---|
| **Python 2.6 only**:`print x` 语句、`except Exception, e`、无 f-string | python26.dll + 全部官方脚本 |
| kcs_dex 结果类型码:**1=INT / 2=REAL / 3=STRING / >10=索引实数列表(个数=码-10)** | TBhook_ConfigNote |
| 抽取语句与 MarDex 完全同源(`HULL.PANEL('名字').PLA(1).THICKNESS`)——**两轨共享抽取语言**,可互换实现 | 两边语料对照 |
| 右键上下文四变量:`kcs_draft.ContextPoint/ContextElement/ContextModel/ContextSubpictures` | trig_draft_popup_menu |
| 新脚本目录要进搜索路径:`KcsPythonUtil.PythonUtil().AppendPythonPath(...)` | trig_draft_popup_menu |
| GUI 用 wxPython(wxPySimpleApp),复杂对话框参考 Ctx*Dlg.py | ctx_menu1 |
| `kcs_ui.error` 是错误码字符串(不是异常);`kcs_gui.error` 同 | kcs_ex_ui1/basic_design_menu |
| 部署:脚本放 `Vitesse\Lib`(工具)/`Context_Menu`(菜单)/`Trigger`(钩子);**不要改官方文件,新增文件即可** | Vitesse 速查 §2 |

## 6. 与其他轨互转

- 同一抽取语句在 PML 侧 = `MARDEX.extractPML(...)`(姿势表 §3.6)——**先选轨再选 API**;
- 船体建模算法优先 Python(Tribon 三十年沉淀);界面与通用 DB 优先 PML;复杂 UI 优先 .NET。
