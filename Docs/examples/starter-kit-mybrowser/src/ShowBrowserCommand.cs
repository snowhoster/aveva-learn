using System;
using Aveva.ApplicationFramework.Presentation;

namespace MyCompany.MyBrowser
{
    public class ShowBrowserCommand : Command
    {
        private readonly DockedWindow _window;
        public ShowBrowserCommand(DockedWindow window)
        {
            Key = "MyCompany.MyBrowser.Show";   // must match uic CommandId exactly
            _window = window;
            _window.Closed += delegate { Checked = false; };
            WindowManager.Instance.WindowLayoutLoaded += delegate { Checked = _window.Visible; };
        }
        public override void Execute()
        {
            if (Checked) _window.Show(); else _window.Hide();
        }
    }
}
