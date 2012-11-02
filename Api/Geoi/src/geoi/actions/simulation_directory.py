import traceback
import os

import wx
from geoi.actions.params_action import ParamsAction

from geoi import parameters

description =\
       """
       Allow you to define the directory in which results will be written
       """

HELP =\
       """ 
       Allow you to define the directory in which results will be written
       The directory will be named with (the name of your test) + Simulation
       """

class SimulationDirectory(ParamsAction):
    "Define the directory for the results"

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr,  win, "Define result directory",description=description,help=HELP)
        self.param_mgr = params_mgr
        self.param_mgr.gmshMesh = ""


    def _createInterface(self, parent, params):
    	self.params = params  	
    	self.parent = parent  	
    	
    	sizer = wx.BoxSizer( wx.VERTICAL )
    	simul = self.GetDialogPanel()
    	
    	
    	box = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box.SetMinSize((200,20)) 
    	 
    	label = wx.StaticText(parent, -1, "actual directory :\n" + params.getParam(parameters.ResultDirectory).getValue())
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.LEFT|wx.ALL, 2)
        
        self.select = wx.Button(parent, -1, "Select", (200,100))
        simul.Bind(wx.EVT_BUTTON, self._select, self.select)
        
    	parent.SetSizerAndFit(sizer) 
    	  	
    def _onOk(self, params):
        return True
    
    def _select(self,event):
        params = self.params
        dlg = wx.DirDialog(
            self.getParent(), message="Choose your directory for the results\n",
            defaultPath="",
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            directory = dlg.GetPath()
            print 'You selected: %s directory:' % directory
            
            params.getParam(parameters.ResultDirectory).setValue(directory)
        dlg.Destroy()
        return None
