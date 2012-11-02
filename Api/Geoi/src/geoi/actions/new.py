import wx

from geoi.actions.action import Action

class New(Action):
    "New File action : reset to defaults ?"

    def __init__(self, win, params_mgr):
        Action.__init__(self, win, "New", "Reset parameters", menuText='&New'
                        , accelerator='CTRL+N', iconId = wx.ART_NEW, )
        self.params_mgr=params_mgr

    def run(self):
    	dlg = wx.MessageDialog(self.getParent(), 'You will lose all the parameters.\nDo you want to continue?',
                               'A Message Box',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               )
        val = dlg.ShowModal()
        dlg.Destroy()
        if val == wx.ID_OK:
            dlg.Destroy()
            while self.params_mgr._current_set>0:
        	    self.params_mgr._undo_action.run()

