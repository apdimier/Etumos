import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters
from geoi.actions.pywrite import *
import os

description =\
       """ 
       To set the splitting parameters and to launch the simulation
       """
HELP = """
       The first order time derivatives may be discretizated by using the following methods:
                The Crank-Nicolson method
                The Backward Differences Formulae (BDF) of several orders
        All the BDF methods are implicit in time and stable. The accuracies of the methods increase along with
        the increasing order. The starting values for the BDF schemes of order n > 1 are computed using the BDF
        schemes of order 1, ..., n-1 as starting procedures. It should be noted that the BDF discretisations of order n > 1
        do not allow the use of variable time step size.
       """
       
class ParametersElmerSecondPart(ParamsAction):

    """
    Enables the choice of the parameters
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "time discretisation parameters",description  =description,help=HELP)
        self.params_mgr = params_mgr
        self.Direct = False
        self.Iterative = False
        
    def _createInterface(self, parent, params):
    	self.params = params  	
    	self.parent = parent
    	
    	
    	sizer = wx.BoxSizer( wx.VERTICAL )
    	simul = self.GetDialogPanel()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    	
    	box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box1.SetMinSize((200,20))
    	
    	label1 = wx.StaticText(parent, -1, "Time Stepping Method:")
        label1.SetHelpText("This is the help text for the label")
        box1.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        TimeSteppingMethod_list = ["BDF","Crank-Nicolson"]
        
        self.TimeSteppingMethod = TimeSteppingMethod = wx.ComboBox(parent, -1, "",
                                 (250, 15), (200, -1),
                                 TimeSteppingMethod_list, 
                                 wx.CB_DROPDOWN)
                                 
        TimeSteppingMethod = params.getParam( parameters.Elmer_Time_Stepping_Method ).getValue()  	
    	self.TimeSteppingMethod.SetValue(TimeSteppingMethod)
    	
    	simul.Bind(wx.EVT_COMBOBOX, self._changeSolver )
    	
    	box1.Add(self.TimeSteppingMethod, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    	
    	
    	box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box2.SetMinSize((200,20)) 
    	 
    	label2 = wx.StaticText(parent, -1, "BDF Order")
        label2.SetHelpText("This is the help text for the label")
        box2.Add(label2, 0, wx.LEFT|wx.ALL, 2)
        
        BDF_list2 = ["1","2","3","4","5"]
        
        self.BDFOrder = BDFOrder = wx.ComboBox(parent, -1, "",
                                 (250, 15), (200, -1),
                                 BDF_list2, wx.CB_DROPDOWN)
                                 
        BDFOrder= params.getParam( parameters.Elmer_BDF_Order ).getValue()   	
    	self.BDFOrder.SetValue(BDFOrder) 
                                 
        self.BDFOrder.Enable(False)
        
        box2.Add(self.BDFOrder, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
    	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    	
    	
    	box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Simulation time control" ) , wx.HORIZONTAL)
        box3.SetMinSize((250,30))

        start = params.getParam( parameters.Elmer_Iterate_InitialTime )
        dt0 = params.getParam( parameters.Elmer_Iterate_InitialTimeStep )
        simulationTime = params.getParam( parameters.Elmer_Iterate_SimulationTime )
        
        label31 = wx.StaticText(parent, -1, "t0:")
        label31.SetHelpText("This is the help text for the label")
        box3.Add(label31, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        self.startCtrl = startCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        startCtrl.SetHelpText("Here's some help text for field #1")
        startCtrl.SetValue( str(start.getValue()) )
        box3.Add(startCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        label32 = wx.StaticText(parent, -1, "dt0:")
        label32.SetHelpText("This is the help text for the label")
        box3.Add(label32, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.dt0Ctrl = dt0Ctrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        dt0Ctrl.SetHelpText("Here's some help text for field #1")
        dt0Ctrl.SetValue( str(dt0.getValue()) )
        box3.Add(dt0Ctrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        label33 = wx.StaticText(parent, -1, "final time:")
        label33.SetHelpText("This is the help text for the label")
        box3.Add(label33, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.simulationTimeCtrl = simulationTimeCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        simulationTimeCtrl.SetHelpText("Here's some help text for field #1")
        simulationTimeCtrl.SetValue( str(simulationTime.getValue()) )
        box3.Add(simulationTimeCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
               
        sizer.Add( box3, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
    	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   	
    	
    	box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box4.SetMinSize((250,30))
        
        label41 = wx.StaticText(parent, -1, "Min Time Step:")
        label41.SetHelpText("This is the help text for the label")
        box4.Add(label41, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        self.minTimeStep = minTimeStep = wx.TextCtrl(parent, -1, "", size=(80,-1))
        minTimeStep.SetHelpText("Here's some help text for field #1")
        minTimeStep.SetValue( str(start.getValue()) )
        box4.Add(minTimeStep, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
        
        minTimeStep= params.getParam( parameters.Elmer_Min_Time_Step ).getValue()   	
    	self.minTimeStep.SetValue( str(minTimeStep) ) 
              
        label42 = wx.StaticText(parent, -1, "Max Time Step:")
        label42.SetHelpText("This is the help text for the label")
        box4.Add(label42, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.maxTimeStep = maxTimeStep = wx.TextCtrl(parent, -1, "", size=(80,-1))
        maxTimeStep.SetHelpText("Here's some help text for field #1")
        maxTimeStep.SetValue( str(dt0.getValue()) )
        box4.Add(maxTimeStep, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        
        maxTimeStep= params.getParam( parameters.Elmer_Max_Time_Step ).getValue()   	
    	self.maxTimeStep.SetValue( str(maxTimeStep) )
    	
        sizer.Add( box4, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
    	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   	

        
    	parent.SetSizerAndFit(sizer)
         
        
        if self.TimeSteppingMethod.GetValue() == "BDF" :
            self.BDFOrder.Enable(True)
        if self.TimeSteppingMethod.GetValue() == "Crank-Nicolson" :
            self.BDFOrder.Enable(False)
            
    def _changeSolver(self,event): 
        if self.TimeSteppingMethod.GetValue() == "BDF" :
            self.BDFOrder.Enable(True)
        if self.TimeSteppingMethod.GetValue() == "Crank-Nicolson" :
            self.BDFOrder.Enable(False)
            
    def _onOk(self, params):
        

        self.params.getParam(parameters.Elmer_Time_Stepping_Method).setValue(self.TimeSteppingMethod.GetValue())
        self.params.getParam(parameters.Elmer_BDF_Order).setValue(self.BDFOrder.GetValue())
        self.params.getParam(parameters.Elmer_Iterate_InitialTime).setValue(float(str(self.startCtrl.GetValue())))
        self.params.getParam(parameters.Elmer_Iterate_InitialTimeStep).setValue(float(str(self.dt0Ctrl.GetValue())))
        self.params.getParam(parameters.Elmer_Iterate_SimulationTime).setValue(float(str(self.simulationTimeCtrl.GetValue())))
        self.params.getParam(parameters.Elmer_Min_Time_Step).setValue(float(str(self.minTimeStep.GetValue())))
        self.params.getParam(parameters.Elmer_Max_Time_Step).setValue(float(str(self.maxTimeStep.GetValue())))      

        return True
