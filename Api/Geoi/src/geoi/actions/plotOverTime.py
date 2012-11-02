import traceback
import os

import wx

from geoi.actions.action import Action
from geoi import parameters

class PlotOverTime(Action):
    "OpenFile: Open a Geoi file"

    def __init__(self, win, param_mgr):
        Action.__init__(self, win, "Plot results over time"
                        , ''
                        , iconId = wx.ART_FILE_OPEN)
        self.param_mgr = param_mgr

    def run(self):
        wildcard = "Gnuplot file (*.plt)|*.plt|All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self.getParent(), message="Choose a Gnuplot file to open",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )

        if dlg.ShowModal() == wx.ID_OK:
            file = dlg.GetPath()
            directory = os.path.split(file)[0]
            name = os.path.split(file)[1]
            os.chdir(directory)
            os.system("gnuplot " + name)
