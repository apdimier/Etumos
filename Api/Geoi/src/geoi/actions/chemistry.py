import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

class Chemistry(ParamsAction):
    """
    Choose the Chemistry software
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Chemistry software",\
        """Let you choose the chemistry tool to be used.
This choice determines the way a state will be defined.
                    """)

    def _createInterface(self, parent, params):
        tool = params.getParam(parameters.ChemistryTool)
   
        sizer = wx.BoxSizer( wx.VERTICAL )
        box = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Solvers" ) , wx.VERTICAL )
   
        radios = []
        currentTool = str( tool.getValue() )
        for (i,n) in enumerate(parameters.CHEMISTRY_TOOLS):
            if i == 0:    
                style = wx.RB_GROUP
            else:
                style = 0
            radio = wx.RadioButton( parent, -1, n,  style=style )
            box.Add( radio, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            radios.append( radio )
            radio.SetValue( currentTool == n )
            
        self.radios = radios
        sizer.Add( box, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        parent.SetSizerAndFit(sizer)

    def _onOk(self, params):
        radio = filter(lambda r: r.GetValue(), self.radios)[0]
        name = radio.GetLabelText()
        params.getParam(parameters.ChemistryTool).setValue( name )

        return True
        

