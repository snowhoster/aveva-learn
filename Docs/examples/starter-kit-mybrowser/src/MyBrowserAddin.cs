using System;
using Aveva.ApplicationFramework;
using Aveva.ApplicationFramework.Presentation;
using Aveva.Pdms.Shared;
using Aveva.Pdms.Database;

namespace MyCompany.MyBrowser
{
    public class MyBrowserAddin : IAddin
    {
        private DockedWindow _window;
        private AttributeListControl _control;

        public string Name { get { return "MyBrowserAddin"; } }
        public string Description { get { return "CE attribute docked browser"; } }

        public void Start(ServiceManager serviceManager)
        {
            try
            {
                // 1. Docked window (content = plain WinForms control)
                WindowManager wm = (WindowManager)serviceManager.GetService(typeof(WindowManager));
                _control = new AttributeListControl();
                _window = wm.CreateDockedWindow("MyCompany.MyBrowser.List",
                                                "My Attributes", _control, DockedPosition.Right);
                _window.Width = 260;
                _window.SaveLayout = true;

                // 2. Command (state button)
                CommandManager cm = (CommandManager)serviceManager.GetService(typeof(CommandManager));
                cm.Commands.Add(new ShowBrowserCommand(_window));

                // 3. CE change -> refresh
                CurrentElement.CurrentElementChanged += OnCurrentElementChanged;

                // 4. Icon resources (MyBrowserAddin.resources alongside dll)
                ResourceManager rm = (ResourceManager)serviceManager.GetService(typeof(ResourceManager));
                rm.LoadResourceFile("MyBrowserAddin");

                // 5. uic mount
                CommandBarManager cbm = (CommandBarManager)serviceManager.GetService(typeof(CommandBarManager));
                cbm.AddUICustomizationFile("MyBrowser.uic", "MyBrowser");
            }
            catch (Exception ex)
            {
                // Start() exceptions are silently swallowed by the framework - self-log
                System.IO.File.WriteAllText(@"C:\mydev\mybrowser_start_err.txt", ex.ToString());
            }
        }

        public void Stop() { }

        private void OnCurrentElementChanged(object sender, CurrentElementChangedEventArgs e)
        {
            if (_window == null) return;
            _window.Title = "Attr: " + CurrentElement.Element.GetAsString(DbAttributeInstance.FLNM);
            _control.Clear();
            foreach (DbAttribute att in CurrentElement.Element.GetAttributes())
                _control.AddAttribute(att.Name, CurrentElement.Element.GetAsString(att));
        }
    }
}
