@echo off
rem ============================================================
rem MyCollect starter kit installer (starter-kit-mycollect)
rem 调用方式: install.cmd  (把三件东西装到对应目录)
rem   1. PML 源码 -> %PMLLIB% (平行目录 myco)
rem   2. ADDIN 定义 -> %PDMSUI%\DES\DFLTS\ADDINS\
rem   3. 提示手动确认 evars 前置(不改标准文件)
rem ============================================================

if "%PMLLIB%"=="" (
  echo [ERR] 请先在 Marine 启动环境里运行本脚本 ^(marine.bat 环境^)
  goto :eof
)
if "%PDMSUI%"=="" (
  echo [ERR] PDMSUI 未定义
  goto :eof
)

set KIT=%~dp0

rem --- 1. PML 源码 -> PMLLIB 下平行目录(复制而非改标准文件) ---
xcopy /s /y /i "%KIT%pmllib\myco" "%PMLLIB%myco"
if errorlevel 1 ( echo [ERR] PML 源码复制失败 & goto :eof )

rem --- 2. ADDIN 定义文件(菜单入口注册) ---
copy /y "%KIT%addins-des\MYCOLLECT" "%PDMSUI%DES\DFLTS\ADDINS\MYCOLLECT"
if errorlevel 1 ( echo [ERR] ADDIN 文件复制失败 & goto :eof )

echo.
echo [OK] 部署完成。请重启 Outfitting^(或 Design^)后验证:
echo   q evar pmllib          ^&^& 确认 myco 路径可见
echo   pml rehash all         ^&^& 重建索引
echo   等待约 10 秒
echo   show !!mycollect       ^&^& 冒烟
echo   Utilities 菜单应出现 "My EQUI Collector..."
echo.
echo 卸载: 删除 %PMLLIB%myco 与 %PDMSUI%DES\DFLTS\ADDINS\MYCOLLECT
