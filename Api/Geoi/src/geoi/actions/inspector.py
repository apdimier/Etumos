import wx

from geoi.actions.action import Action

class Inspector(Action):
    "Inspector: Open Widget Inspector"

    def __init__(self, win):
        Action.__init__(self, win, "Open &Widget Inspector"
                        , 'A tool that lets you browse the live widgets and sizers in an application'
                        , accelerator = 'F6', iconId = 'wx.ART_IMAGES_inspect')

    def run(self):
        self.OnOpenWidgetInspector(None)

    def OnOpenWidgetInspector(self, evt):
        "borrowed from the wxPython demo (from Main.py)"
        # Activate the widget inspection tool
        from wx.lib.inspection import InspectionTool
        if not InspectionTool().initialized:
            InspectionTool().Init()

        # Find a widget to be selected in the tree.  Use either the
        # one under the cursor, if any, or this frame.
        wnd = wx.FindWindowAtPointer()
        if not wnd:
            wnd = self
        InspectionTool().Show(wnd, True)
