import wx
import wx.richtext as rt
import  wx.html as  html
from geoi.actions.action import Action

class Help(Action):
    "Help: show Help"

    def __init__(self, win):
        Action.__init__(self, win, "Help", "Will show Help", menuText = '&Help'
                        , accelerator = 'CTRL+H', iconId = wx.ART_HELP)
    def run(self):
        print "Help.run()"
        toto = RichTextFrame("noch zu entwickeln")
        toto.Show(True)
        
        self.setDisabled(True)
        
class RichTextFrame(wx.Frame):
    def __init__(self,title):
        wx.Frame.__init__(self,parent=None,id=-1,title=title,pos=wx.DefaultPosition,size=wx.DefaultSize,style = wx.DEFAULT_FRAME_STYLE )

        self.SetStatusText("Welcome to the interface Help")

        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        wx.CallAfter(self.rtc.SetFocus)

