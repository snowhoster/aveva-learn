using System;
using System.Windows.Forms;

namespace MyCompany.MyBrowser
{
    public class AttributeListControl : UserControl
    {
        private ListView listView1;

        public AttributeListControl()
        {
            listView1 = new ListView();
            listView1.Dock = DockStyle.Fill;
            listView1.View = View.Details;
            listView1.GridLines = true;
            listView1.Columns.Add("Attribute", 120);
            listView1.Columns.Add("Value", 160);
            Controls.Add(listView1);
        }

        public void AddAttribute(string name, string value)
        {
            ListViewItem it = new ListViewItem(name);
            it.SubItems.Add(value);
            listView1.Items.Add(it);
        }

        public void Clear()
        {
            listView1.Items.Clear();
        }
    }
}
