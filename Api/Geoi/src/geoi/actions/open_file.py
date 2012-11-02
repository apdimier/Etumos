import traceback
import os

import wx

from geoi.actions.action import Action
from geoi import parameters

class OpenFile(Action):
    """
    OpenFile: Open a Geoi file -> CTRL+O
    """

    def __init__(self, win, param_mgr):
        Action.__init__(self, win, "Open..."
                        , 'Open and load a Geoi file holding the configuration settings for a case/study'
                        , accelerator='CTRL+O'
                        , iconId = wx.ART_FILE_OPEN)
        self.param_mgr = param_mgr

    def run(self):
        wildcard = "Geoi file (*.geoi)|*.geoi|All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self.getParent(), message="Choose a geoi file to open",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )

        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            file = dlg.GetPath()
            print 'You selected: %s file:' % file
            self.param_mgr.openFile( file )

        dlg.Destroy()
