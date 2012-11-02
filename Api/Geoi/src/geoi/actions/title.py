from wx._core import StaticBoxSizer
from wx._controls import StaticText
from wx._controls import StaticBox
import string

import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

class Title(ParamsAction):
    """
    input the Title Parameter of the study
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Set Title"
                              , "define the title of the case/study")

    def _createInterface(self, parent, params):
        title = params.getParam( parameters.Title )

        msg = "Enter text value for parameter : " + title.getName() + "\n" \
                + "N.B: spaces will be turned into underscores"
        sizer = StaticBoxSizer(StaticBox(parent, -1, ""), wx.HORIZONTAL )
        sizer.Add(StaticText(parent, -1, msg), border=5)

        sizer.AddSpacer(10)

        self.textCtrl = textCtrl = wx.TextCtrl(parent, -1, msg)
        textCtrl.SetValue( str(title.getValue()) )
        sizer.Add(textCtrl, wx.EXPAND )
        textCtrl.SetToolTipString( title.getDescription() )
        parent.SetSizerAndFit(sizer)

    def _onOk(self, params):
        title = params.getParam( parameters.Title )
        value = str(string.replace (self.textCtrl.GetValue(), " ", "_"))
        if not self.checkValue(title, value):
            return False
        title.setValue( value )
        return True

