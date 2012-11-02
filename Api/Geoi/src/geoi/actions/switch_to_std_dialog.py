from geoi.actions import toggle_action, params_action

class SwitchToStdDialog(toggle_action.ToggleAction):
    def __init__(self, win):
        toggle_action.ToggleAction.__init__(self, win, "Standard dialogs"
                        , 'Switch to standard dialog mode where dialogs are displayed in standalone windows')

    def onToggleOn(self):
        params_action.ParamsAction.SetDialogPanel(None)
        self.getParent().clearDialogPanel()

    def onToggleOff(self):
        params_action.ParamsAction.SetDialogPanel( self.getParent().getDialogPanel() )
