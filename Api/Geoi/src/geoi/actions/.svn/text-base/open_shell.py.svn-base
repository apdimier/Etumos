import wx

from geoi.actions.action import Action

DEFAULT_SHELL_WINDOW_SIZE = (640,480)

class OpenShell(Action):
    "OpenShell: Open a PyShell Window"

    def __init__(self, win):
        Action.__init__(self, win, "Open Py&Shell Window"
                        , 'An interactive interpreter window with the demo app and frame objects in the namespace'
                        , accelerator = 'F5', iconId = 'wx.ART_IMAGES_' + 'pyshell')
        self.shell = None

    def run(self):
        self.OnOpenShellWindow(None)

    def OnOpenShellWindow(self, evt):
        "borrowed from the wxPython demo (from Main.py)"
        if self.shell:
            # if it already exists then just make sure it's visible
            s = self.shell
            if s.IsIconized():
                s.Iconize(False)
            s.Raise()
        else:
            # Make a PyShell window
            from wx import py
            namespace = { 'wx'    : wx,
                          'app'   : wx.GetApp(),
                          'frame' : self,
                          }
            self.shell = py.shell.ShellFrame(None, locals=namespace)
            self.shell.SetSize( DEFAULT_SHELL_WINDOW_SIZE )
            self.shell.Show()

            # Hook the close event of the main frame window so that we
            # close the shell at the same time if it still exists
            def CloseShell(evt):
                if self.shell:
                    self.shell.Close()
                evt.Skip()
            self.getParent().Bind(wx.EVT_CLOSE, CloseShell)
