import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

description = """ 
       Used to set the Darcy velocity components
       """
HELP = """
       Used to define the components of a darcy velocity. For Mt3d only two components
       are accessible. while for Elmer a three dimensional velocity can be defined.
       If the checkbox is not selected a Darcy velocity will be read from a file given by the user.

       """
class DarcyVelocityComponents(ParamsAction):
    """
    Used to set the Darcy velocity components
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Darcy Velocity",description  =description,help=HELP)
        self.radios = None
        self.choice = None

    def _createInterface(self, parent, params):
#velocity components
        toto = self.GetDialogPanel()
        wx.CheckBox.SetTTS = wx.CheckBox.SetToolTipString
        sizer = wx.BoxSizer( wx.VERTICAL )
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Static velocity field components" ) , wx.HORIZONTAL)
        box3.SetMinSize((300,100))
        grid3 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid3.SetFlexibleDirection( wx.HORIZONTAL)

        velocity = params.getParam( parameters.DarcyVelocity_list)
        grid3.SetFlexibleDirection( wx.HORIZONTAL)
        
        label1 = wx.StaticText(parent, -1, "Vx")
        label1.SetHelpText("This is the help text for the label")
        box3.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
 
        self.vxCtrl = vxCtrl = wx.TextCtrl(parent, -1, "", size=(90,-1))
        vxCtrl.SetHelpText("Here's some help text for field #1")
        if velocity.getValue() != []:
            [vx,vy,vz]  = velocity.getValue()
        else:
            vx = None
            vy = None
            vz = None
            
        if vx != None:
            vxCtrl.SetValue( str(vx) )
            vxCtrl.Enable(True)
        else:
            vxCtrl.Enable(False)
        
        box3.Add(vxCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        label2 = wx.StaticText(parent, -1, "Vy")
        label2.SetHelpText("This is the help text for the label")
        box3.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.vyCtrl = vyCtrl = wx.TextCtrl(parent, -1, "", size=(90,-1))
        vyCtrl.SetHelpText("Here's some help text for field #1")
        if vy != None:
            vyCtrl.SetValue( str(vy) )
            vyCtrl.Enable(True)
        else:
            vyCtrl.Enable(False)
        box3.Add(vyCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        label3 = wx.StaticText(parent, -1, "Vz")
        label3.SetHelpText("This is the help text for the label")
        box3.Add(label3, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.vzCtrl = vzCtrl = wx.TextCtrl(parent, -1, "", size=(90,-1))
        vzCtrl.SetHelpText("Here's some help text for field #1")
        if vz != None:
            vzCtrl.SetValue( str(vz) )
            vzCtrl.Enable(True)
        else:
            vzCtrl.Enable(False)
        box3.Add(vzCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.DarcyControl = DarcyControl = wx.CheckBox( parent, -1, "",style = 0)
        DarcyControl.SetTTS("used to control a constant Darcy Velocity,\n default being a zero normed one ")
        box3.Add(DarcyControl, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        toto.Bind(wx.EVT_CHECKBOX, self._darcyControl, DarcyControl)
        if vzCtrl.IsEnabled() == True:
            DarcyControl.SetValue(True)
        else:
            DarcyControl.SetValue(False)
        
               
        sizer.Add( box3, 0, wx.ALIGN_LEFT|wx.ALL, 5 )        
        parent.SetSizerAndFit(sizer)
        
    def _darcyControl(self, event):
        if event.IsChecked()==True:
            self.vxCtrl.Enable(True)
            self.vyCtrl.Enable(True)
            self.vzCtrl.Enable(True)
        
        else:
            self.vxCtrl.Enable(False)
            self.vyCtrl.Enable(False)
            self.vzCtrl.Enable(False)
        return True
        
    def _onOk(self, params):
#
# parameters
#
        gesch = []
        velocity = params.getParam( parameters.DarcyVelocity_list)
        if self.DarcyControl.GetValue() == True:
            value = self.vxCtrl.GetValue()
            gesch.append(value)
        
            value = self.vyCtrl.GetValue()
            gesch.append(value)
        
            value = self.vzCtrl.GetValue()
            gesch.append(value)
        
            velocity.setValue( gesch )
        else:
            velocity.setValue( gesch )
  
        return True
        

