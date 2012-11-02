import wx
import wx.html

class HtmlHelpWindow(wx.Dialog):

    def __init__(self, parent, title, helptext):
        wx.Dialog.__init__(self,parent, -1, title, style=wx.RESIZE_BORDER |wx.CAPTION)
        hw = wx.html.HtmlWindow(self, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        hw.SetPage( helptext )
        btnsizer = self.CreateStdDialogButtonSizer(wx.OK)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hw, proportion=1, flag=wx.EXPAND| wx.ALL)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
#        dlg.SetSizer( sizer)
        self.SetSizer(sizer)
        self.SetSize( (640, 400) )



if __name__ == '__main__':
    msg = """
<h1>Head1</h1>
du texte

    """

    app = wx.App(0)
    f = wx.Frame(None, -1, "test")

    d = HtmlHelpWindow(f, "coucou", msg)
    b = wx.Button(f, -1, "click")
    b.Bind(wx.EVT_BUTTON, lambda e: d.Show())
    app.SetTopWindow(f)
    f.Show()
    app.MainLoop()

