#----------------------------------------------------------------------

ilabel = "horizontal structured mesh definition  "
jlabel = "vertical structured mesh definition  "
label2 = "Click here to hide pane"

import wx

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        title = wx.StaticText(self, label="structured mesh definition")
        title.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour("blue")

        self.cp = cp = wx.CollapsiblePane(self, label=ilabel,
                                          style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cp)
        self.IMeshControl(cp.GetPane())

        self.cp2 = cp2 = wx.CollapsiblePane(self, label=jlabel,
                                          style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cp2)
        self.IMeshControl(cp2.GetPane())

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add(title, 0, wx.ALL, 30)
        sizer.Add(cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 50)
        pSizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.EXPAND,50)
        sizer.Add((30,40))
        sizer.Add(cp2, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 50)

    def OnPaneChanged(self, cp,evt=None):
        if evt:
            self.log.write('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % evt.Collapsed)

        # redo the layout
#        self.Layout()
        

    def IMeshControl(self, pane):
        
        addrSizer = wx.FlexGridSizer(rows = 3,cols=1, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
#        iext = wx.StaticText(pane, -1, "horizontal ext.:")
#        addrSizer.Add(iext, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        
        extSizer = wx.BoxSizer(wx.HORIZONTAL)
        cst0Lbl = wx.StaticText(pane, -1, "I nb cells/zone:",size=(150,20))
        extSizer.Add(cst0Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.i1 = i1 = wx.TextCtrl(pane, -1, "1", size=(50,-1));extSizer.Add(i1, 0, wx.ALIGN_LEFT|wx.RIGHT, 1)
        self.i2 = i2 = wx.TextCtrl(pane, -1, "0", size=(50,-1));extSizer.Add(i2, 0, wx.LEFT|wx.RIGHT, 1)
        self.i3 = i3 = wx.TextCtrl(pane, -1, "0", size=(50,-1));extSizer.Add(i3, 0, wx.LEFT|wx.RIGHT, 1)
        self.i4 = i4 = wx.TextCtrl(pane, -1, "0", size=(50,-1));extSizer.Add(i4, 0, wx.LEFT|wx.RIGHT, 1)
        self.i5 = i5 = wx.TextCtrl(pane, -1, "0", size=(50,-1));extSizer.Add(i5, 0, wx.LEFT|wx.RIGHT, 1)
        self.i6 = i6 = wx.TextCtrl(pane, -1, "0", size=(50,-1));extSizer.Add(i6, 0, wx.LEFT|wx.RIGHT, 1)
        self.i7 = i7 = wx.TextCtrl(pane, -1, "0", size=(50,-1));extSizer.Add(i7, 0, wx.LEFT|wx.RIGHT, 1)
        self.i8 = i8 = wx.TextCtrl(pane, -1, "0", size=(50,-1));extSizer.Add(i8, 0, wx.LEFT|wx.RIGHT, 1)
        
        addrSizer.Add(extSizer, 0, wx.ALIGN_LEFT|wx.ALL)
        
        cst1Lbl = wx.StaticText(pane, -1, "I pt distribution coeff.:",size=(150,20))
        powSizer = wx.BoxSizer(wx.HORIZONTAL)
        powSizer.Add(cst1Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.p1 = p1 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p1, 0, wx.LEFT|wx.RIGHT, 1)
        self.p2 = p2 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p2, 0, wx.LEFT|wx.RIGHT, 1)
        self.p3 = p3 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p3, 0, wx.LEFT|wx.RIGHT, 1)
        self.p4 = p4 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p4, 0, wx.LEFT|wx.RIGHT, 1)
        self.p5 = p5 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p5, 0, wx.LEFT|wx.RIGHT, 1)
        self.p6 = p6 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p6, 0, wx.LEFT|wx.RIGHT, 1)
        self.p7 = p7 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p7, 0, wx.LEFT|wx.RIGHT, 1)
        self.p8 = p8 = wx.TextCtrl(pane, -1, "1.", size=(50,-1));powSizer.Add(p8, 0, wx.LEFT|wx.RIGHT, 1)
#        addrSizer.Add(powSizer, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        addrSizer.Add(powSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.EXPAND)
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)
        pane.SetSizer(border)
        
        
#    def _onOk(self, params):
    def _onOk(self):
        pass

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.CollapsiblePane</center></h2>

A collapsable panel is a container with an embedded button-like
control which can be used by the user to collapse or expand the pane's
contents.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    print sys.argv[0]
