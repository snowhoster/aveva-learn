MyCollect Starter Kit(模板① 可部署版)
==========================================

内容
----
pmllib\myco\forms\mycollect.pmlfrm   收集表单(网格 + Excel 导出)
pmllib\myco\objects\appmycollect.pmlobj  addin 对象(向 Utilities 菜单注入入口)
addins-des\MYCOLLECT                 ADDIN 定义文件(DES 模块)
install.cmd                          一键部署脚本(marine.bat 环境下运行)
README.txt                           本文件

部署
----
1. 打开 Marine 环境(marine.bat 已跑过,PMLLIB/PDMSUI 已定义)
2. 运行 install.cmd
3. 重启 Outfitting 或 Design
4. Utilities 菜单 → "My EQUI Collector..."
5. 冒烟:Collect → Export... → Close

卸载
----
删 %PMLLIB%myco 与 %PDMSUI%DES\DFLTS\ADDINS\MYCOLLECT 两处即可。

质量
----
两个 PML 文件已通过 pml_audit.py 16 规则审计(0 违规):
python PML语料\pml_audit.py pmllib
设计依据:AVEVA-Marine端到端示例-收集导出工具.md
官方范式:abaarea.pmlfrm(容器)/appdesavevamarine.pmlobj(addin 对象)/
          commonmsgfiles.pmlfnc 同目录约定
