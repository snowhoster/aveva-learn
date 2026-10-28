MyBrowser Starter Kit(模板② 可编译版)
==========================================

内容
----
src\MyBrowserAddin.cs          IAddin 入口(停靠窗+命令+CE事件+资源+uic 挂载)
src\ShowBrowserCommand.cs      状态按钮命令(与窗可见性双向同步)
src\AttributeListControl.cs    WinForms UserControl(ListView 两列)
MyBrowser.uic                  UI 定制(StateButtonTool + CommandBar)
README.txt                     本文件

构建(Visual Studio)
--------------------
1. 新建 C# 类库工程(.NET Framework 3.5,x86 平台)
2. 把 src\ 三个 .cs 加入工程;命名空间 MyCompany.MyBrowser
3. 添加引用(HintPath = C:\AVEVA\Marine\OH12.1.SP4,Copy Local = false):
   Aveva.ApplicationFramework
   Aveva.ApplicationFramework.Presentation
   Aveva.Pdms.Shared
   Aveva.Pdms.Database
4. 生成 → bin\x86\Debug\MyBrowserAddin.dll

部署
----
1. 拷 MyBrowserAddin.dll + MyBrowser.uic 到 C:\AVEVA\Marine\OH12.1.SP4\
2. OutfittingAddins.xml 加 <string>MyBrowserAddin</string>
3. 重启 Outfitting(marodes.exe)
4. 工具条出现 My Browser 状态按钮;点击开合停靠窗;CE 切换自动刷新

调试
----
工程属性 → 调试 → 启动外部程序 = marodes.exe;工作目录 = 安装目录;F5 断点打在 Start()
Start() 内异常会自写 C:\mydev\mybrowser_start_err.txt(静默失败的兜底)

排错
----
见 AVEVA-Marine-uic定制与部署调试手册.md §3.4 排错树
或跑:python PML语料\net_consistency.py <部署根> --src <本src> --uic MyBrowser.uic --dll <exe目录>
