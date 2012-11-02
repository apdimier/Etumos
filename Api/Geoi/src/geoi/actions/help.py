import wx
import os
import sys
import wx.richtext as rt
import  wx.html as  html
from geoi.actions.action import Action
from wx.html import *

class Help(Action):
    "Help: show Help"

    def __init__(self, win):
        Action.__init__(self, win, "Help", "Will show Help", menuText = '&Help'
                        , accelerator = 'CTRL+H', iconId = wx.ART_HELP)
    def run(self):
#        self.htmlControl("Help file")        print " weare here"
        helpFile = os.environ ['WRAPPER'] + "/Doc/menu.html"
        browser = os.environ ['BROWSER']
        os.system(browser+" "+helpFile+"&")
#        frame = exFrame("Help file")
#        frame.Show()
        
    def htmlControl(self,title):
   
#        dialog = RichTextFrame("noch zu entwickeln")
        help = exFrame(title)
        help.Show()

class Frame(wx.Frame):
    def __init__(self,title):
        wx.Frame.__init__(self,parent=None,id=-1,title=title,pos=wx.DefaultPosition,size=wx.DefaultSize,style = wx.DEFAULT_FRAME_STYLE )
        
class RichTextFrame(wx.Frame):
    def __init__(self,title):
        wx.Frame.__init__(self,parent=None,id=-1,title=title,pos=wx.DefaultPosition,size=wx.DefaultSize,style = wx.DEFAULT_FRAME_STYLE )

        self.SetStatusText("Welcome to the interface Help")

        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        wx.CallAfter(self.rtc.SetFocus)

class exHtmlWindow(HtmlWindow):
   def __init__(self, parent, id, frame):
      HtmlWindow.__init__(self,parent,id, style=wx.NO_FULL_REPAINT_ON_RESIZE)

class exHtmlPanel(wx.Panel):
    def __init__(self, parent, id, frame,helpFile):
        wx.Panel.__init__(self,parent,-1)

        self.html = exHtmlWindow(self, -1, frame)
      
        self.printer = html.HtmlEasyPrinting()

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.html, 1, wx.GROW)

        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        self.html.LoadPage(helpFile)
      
        self.printer = html.HtmlEasyPrinting()

        subbox = wx.BoxSizer(wx.HORIZONTAL)

        btn = wx.Button(self, -1, "Load File")
        self.Bind(wx.EVT_BUTTON, self.OnLoadFile, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Load URL")
        self.Bind(wx.EVT_BUTTON, self.OnLoadURL, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "With Widgets")
        self.Bind(wx.EVT_BUTTON, self.OnWithWidgets, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Back")
        self.Bind(wx.EVT_BUTTON, self.OnBack, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Forward")
        self.Bind(wx.EVT_BUTTON, self.OnForward, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Print")
        self.Bind(wx.EVT_BUTTON, self.OnPrint, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "View Source")
        self.Bind(wx.EVT_BUTTON, self.OnViewSource, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        self.box.Add(subbox, 0, wx.GROW)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)

        # A button with this ID is created on the widget test page.
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)

        self.OnShowDefault(None)

    def ShutdownDemo(self):
        # put the frame title back
        if self.frame:
            self.frame.SetTitle(self.titleBase)

    def OnShowDefault(self, event):
        name = os.environ ['WRAPPER'] + '/Doc/index.html'  
#        name = "$WRAPPER/Doc/index.html"
        self.html.LoadPage(name)

    def OnLoadFile(self, event):
        dlg = wx.FileDialog(self, wildcard = '*.htm*', style=wx.OPEN)

        if dlg.ShowModal():
            path = dlg.GetPath()
            self.html.LoadPage(path)

        dlg.Destroy()

    def OnLoadURL(self, event):
        dlg = wx.TextEntryDialog(self, "Enter a URL")

        if dlg.ShowModal():
            url = dlg.GetValue()
            self.html.LoadPage(url)

        dlg.Destroy()

    def OnWithWidgets(self, event):
        os.chdir(self.cwd)
        name = os.environ ['WRAPPER'] + 'data/test.htm'
        self.html.LoadPage(name)

    def OnOk(self, event):
        pass

    def OnBack(self, event):
        if not self.html.HistoryBack():
            wx.MessageBox("No more items in history!")

    def OnForward(self, event):
        if not self.html.HistoryForward():
            wx.MessageBox("No more items in history!")

    def OnViewSource(self, event):
        import  wx.lib.dialogs

        source = self.html.GetParser().GetSource()

        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, source, 'HTML Source')
        dlg.ShowModal()
        dlg.Destroy()

    def OnPrint(self, event):
        self.printer.GetPrintData().SetPaperId(wx.PAPER_LETTER)
        self.printer.PrintFile(self.html.GetOpenedPage())

class exFrame (wx.Frame):
   def __init__(self,title):
#      wx.Frame.__init__(self,parent,ID,title,wxDefaultPosition,wxSize(600,750))
      
      wx.Frame.__init__(self,parent=None,id=-1,title=title,pos=wx.DefaultPosition,size=(600,750),style = wx.DEFAULT_FRAME_STYLE )
      
      helpFile = os.environ ['WRAPPER'] + "/Doc/menu.html"
#      /home/dimier/Wrapper/Api/data/test.htm"

      panel = exHtmlPanel(self, -1, self,helpFile)

      return None
