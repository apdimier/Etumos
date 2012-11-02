import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

DISCRETISATION_BY_LABEL = {'Upwind':parameters.MT3D_ADVECTION_UPWIND,
                           'Central':parameters.MT3D_ADVECTION_CENTRAL,
                           'T.V.D.':parameters.MT3D_ADVECTION_TVD }

PRECONDITONER_BY_LABEL = {'Jacobi':parameters.MT3D_CGP_JACOBI,
                          'MIC':parameters.MT3D_CGP_MIC,
                          'SSOR':parameters.MT3D_CGP_SSOR }

description =\
       """ 
       Used to determine the spatial discretisation and the related algebraic solver
       """
HELP = """
       <html><body><a><b>MXITER</b> is the maximum number of outer iterations; it should be set to
              an integer greater than one (1) only when a nonlinear sorption isotherm
              is included in simulation.</a><br>
       <b>ITER1</b> is the maximum number of inner iterations; a value of 30-50
             should be adequate for most problems.<br>
       <b>ACCL</b> is the relaxation factor for the SSOR option; a value of 1.0 is generally adequate.<br>
       <b>CCLOSE</b> is the convergence criterion in terms of relative concentration;
              a real value between 10-4 and 10-6 is generally adequate. It is set by default to 1.e-16 here.</body></html>
       """
class Mt3dSolverParameters(ParamsAction):
    """
    Enables the choice of transport discretisation and of the algebraic solver
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Mt3d Solver",description  =description,help=HELP)
        self.radios = None
        self.choice = None

    def _createInterface(self, parent, params):
        
   
        sizer = wx.BoxSizer( wx.VERTICAL )
# Advection
        discretisationLabels = DISCRETISATION_BY_LABEL.keys()
        #discretisationLabels.sort()
   
        discretisation = params.getParam(parameters.Mt3d_Default_Discretisation)
        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Advection" ) , wx.HORIZONTAL )
        box1.SetMinSize((250,50))
        grid1 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid1.SetFlexibleDirection( wx.HORIZONTAL)

        radios1 = []
        radios2 = []
        choice1 = None
        currentDiscretisation = str( discretisation.getValue() )
        for (i,n) in enumerate(discretisationLabels):
            if i == 0:    
                style = wx.RB_GROUP
            else:
                style = 0
            radio = wx.RadioButton( parent, -1, n,  style=style )
            radio.SetToolTipString("discretisation is " + DISCRETISATION_BY_LABEL[n])
            grid1.Add( radio, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            radios1.append( radio )
            radio.SetValue( currentDiscretisation == DISCRETISATION_BY_LABEL[n] )
#            e = wx.StaticText(parent, -1, "")
#            grid.Add( e, 0, wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        self.radios1 = radios1
        self.choice1 = choice1
        box1.Add( grid1, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
# Preconditioner
        preconditionerLabels = PRECONDITONER_BY_LABEL.keys()
        #preconditionerLabels.sort()
        preconditioning = params.getParam(parameters.Mt3d_Default_CGPreconditioner)
        choice2 = None
        currentPreconditioning = str(preconditioning.getValue() )
        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "CG Preconditioner" ) , wx.HORIZONTAL )
        box2.SetMinSize((250,50))
        grid2 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid2.SetFlexibleDirection( wx.HORIZONTAL)
        for (i,n) in enumerate(preconditionerLabels):
            if i == 0:    
                style = wx.RB_GROUP
            else:
                style = 0
            radio2 = wx.RadioButton( parent, -1, n,  style=style )
            radio2.SetToolTipString("preconditioner is " + PRECONDITONER_BY_LABEL[n])
            grid2.Add( radio2, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            radios2.append( radio2 )
            radio2.SetValue( currentPreconditioning == PRECONDITONER_BY_LABEL[n] )
        self.radios2 = radios2
        self.choice2 = choice2
        box2.Add( grid2, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

#Parameters
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Algebraic parameters" ) , wx.HORIZONTAL)
        box3.SetMinSize((250,100))
        grid3 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid3.SetFlexibleDirection( wx.HORIZONTAL)

        mxiter = params.getParam( parameters.Mt3d_mxiter )
        iter1 = params.getParam( parameters.Mt3d_iter1 )
        accl = params.getParam( parameters.Mt3d_accl )
        cclose = params.getParam( parameters.Mt3d_cclose )
        
        label1 = wx.StaticText(parent, -1, "mxiter")
        label1.SetHelpText("This is the help text for the label")
        box3.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
 
        grid3.SetFlexibleDirection( wx.HORIZONTAL)

        self.mxiterCtrl = mxiterCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        mxiterCtrl.SetHelpText("Here's some help text for field #1")
        mxiterCtrl.SetValue( str(mxiter.getValue()) )
        box3.Add(mxiterCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        label2 = wx.StaticText(parent, -1, "iter1")
        label2.SetHelpText("This is the help text for the label")
        box3.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.iter1Ctrl = iter1Ctrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        iter1Ctrl.SetHelpText("Here's some help text for field #1")
        iter1Ctrl.SetValue( str(iter1.getValue()) )
        box3.Add(iter1Ctrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        label3 = wx.StaticText(parent, -1, "accl")
        label3.SetHelpText("This is the help text for the label")
        box3.Add(label3, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.acclCtrl = acclCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        acclCtrl.SetHelpText("Here's some help text for field #1")
        acclCtrl.SetValue( str(accl.getValue()) )
        box3.Add(acclCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        label4 = wx.StaticText(parent, -1, "cclose")
        label4.SetHelpText("This is the help text for the label")
        box3.Add(label4, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.ccloseCtrl = ccloseCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        ccloseCtrl.SetHelpText("Here's some help text for field #1")
        ccloseCtrl.SetValue( str(cclose.getValue()) )
        box3.Add(ccloseCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sizer.Add( box3, 0, wx.ALIGN_LEFT|wx.ALL, 5 )        
        parent.SetSizerAndFit(sizer)
        
    def _onOk(self, params):
# convection discretisation        
        radio1 = filter(lambda r: r.GetValue(), self.radios1)[0]
        name = radio1.GetLabelText()
        params.getParam(parameters.Mt3d_Default_Discretisation).setValue(DISCRETISATION_BY_LABEL[name])
# preconditioner        
        radio2 = filter(lambda r: r.GetValue(), self.radios2)[0]
        name = radio2.GetLabelText()
        params.getParam(parameters.Mt3d_Default_CGPreconditioner).setValue(PRECONDITONER_BY_LABEL[name])
# parameters
        mxiter = params.getParam( parameters.Mt3d_mxiter )
        value = self.mxiterCtrl.GetValue()
        mxiter.setValue(float(value))
        
        iter1 = params.getParam( parameters.Mt3d_iter1 )
        value = self.iter1Ctrl.GetValue()
        iter1.setValue(float(value))
        
        accl = params.getParam( parameters.Mt3d_accl )
        value = self.acclCtrl.GetValue()
        accl.setValue(float(value))
        
        cclose = params.getParam( parameters.Mt3d_cclose )
        value = self.ccloseCtrl.GetValue()
        cclose.setValue(float(value))

        return True
        

