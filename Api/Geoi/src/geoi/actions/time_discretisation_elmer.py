import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters
from parameter import inSecondsConverter, inUnitConverter
from geoi.actions.pywrite import *
import os

ITERATE_ALGORITHMS_BY_LABEL = {'NI':parameters.ITERATE_ALGORITHM_ONESTEP,'CC':parameters.ITERATE_ALGORITHM_CC }

description =\
       """ 
       To set the splitting parameters and the time parameters
       """
HELP = """
<h1> order time derivative</h1>

<b>The first order time derivatives</b> may be discretized by using the following methods:<br>
<OL start=1><LI type=1>The Crank-Nicolson method</li>
 <LI type=1>The Backward Differences Formulae (<b>BDF</b>) of several orders</li>
</OL>
<br>
All the BDF methods are implicit in time and stable.<br>
The accuracies of the methods increase along with the increasing order.<br>
The starting values for the BDF schemes of order n > 1 are computed using the BDF
schemes of order 1, ..., n-1 as starting procedures.<br>
It should be noted that the BDF discretisations of order n > 1
do not allow the use of variable time step size. That means,
<br>somes of the options available here will be freezed within the coupling algorithm.
       """
       
class ElmerCouplingAlgorithm(ParamsAction):

    """
    Enables the choice of the time discretisation parameters
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "time discretisation parameters",description  =description,help=HELP)
        self.params_mgr = params_mgr
        self.cc = None
        self.choice = None
        self.radios = None
        
    def _createInterface(self, parent, params):
    	self.params = params
    	  	
    	self.parent = parent
    	sizer = wx.BoxSizer( wx.VERTICAL )

    	self.Unit = Unit = self.params.getParam(parameters.TimeUnit).getValue()     # define now the unit for times
#
# Coupling algorithm
#
        couplingAlgorithmLabels = ITERATE_ALGORITHMS_BY_LABEL.keys()
        #discretisationLabels.sort()
   
        couplingAlgorithm = params.getParam(parameters.Iterate_Default_Algorithm)
        if couplingAlgorithm.getValue() == "CC": self.cc = True
#
        box0 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Splitting algorithm" ) , wx.HORIZONTAL )
        box0.SetMinSize((150,30))
        grid1 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid1.SetFlexibleDirection( wx.HORIZONTAL)

        self.radios1 = radios1 = []
        self.CCctrls = CCctrls = []
        self.choice1 = choice1 = None
        self.params = params
        
        currentDiscretisation = str( couplingAlgorithm.getValue() )
        for (i,n) in enumerate(couplingAlgorithmLabels):
            if i == 0:    
                style = wx.RB_GROUP
            else:
                style = 0
            radio = wx.RadioButton( parent, -1, n,  style=style )
            grid1.Add( radio, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
            radios1.append( radio )
            radio.SetToolTipString("coupling algorithm is " + ITERATE_ALGORITHMS_BY_LABEL[n])
            radio.SetValue( currentDiscretisation == ITERATE_ALGORITHMS_BY_LABEL[n] )

        box0.Add( grid1, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
        sizer.Add( box0, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
        toto = self.GetDialogPanel()
        for radios in radios1:
            toto.Bind(wx.EVT_RADIOBUTTON, self._onCCSelect, radios )
#
#Simulation time control
#
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
        TimeSteppingMethod.SetToolTipString("time discretisation, cf. to the help.")
        TimeSteppingMethod = params.getParam( parameters.Elmer_Time_Stepping_Method ).getValue()  	
    	self.TimeSteppingMethod.SetValue(TimeSteppingMethod)
    	
    	simul.Bind(wx.EVT_COMBOBOX, self._changeSolver )
    	
    	box1.Add(self.TimeSteppingMethod, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    	
    	
    	box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box2.SetMinSize((200,20)) 
    	 
    	label2 = wx.StaticText(parent, -1, "BDF Order:")
        label2.SetHelpText("This is the help text for the label")
        box2.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
        
        BDF_list2 = ["1","2","3","4","5"]
        
        self.BDFOrderCtrl = BDFOrderCtrl = wx.ComboBox(parent, -1, "",
                                                (250, 15), (200, -1),
                                                BDF_list2, wx.CB_DROPDOWN)
                                 
        BDFOrderCtrl.SetToolTipString("order of the BDF method, use BDF=1\nif you are not familiar with, cf to the help")	
        BDFOrder= params.getParam( parameters.Elmer_BDF_Order ).getValue()
    	self.BDFOrderCtrl.SetValue(BDFOrder) 
                                 
        self.BDFOrderCtrl.Enable(False)
        
        box2.Add(self.BDFOrderCtrl, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
    	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    	
#
#
    	
    	box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Simulation time control:" ) , wx.HORIZONTAL)
        box3.SetMinSize((250,30))

        startTime = inUnitConverter(params.getParam( parameters.Elmer_Iterate_InitialTime ).getValue(), self.Unit)
        dt0 = inUnitConverter(params.getParam( parameters.Elmer_Iterate_InitialTimeStep ).getValue(), self.Unit)
        simulationTime = inUnitConverter(params.getParam( parameters.Elmer_Iterate_SimulationTime ).getValue(), self.Unit)
        
        label31 = wx.StaticText(parent, -1, "t0:")
        label31.SetHelpText("This is the help text for the label")
        box3.Add(label31, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        self.startCtrl = startCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        startCtrl.SetHelpText("Here's some help text for field #1")
        startCtrl.SetValue( str(startTime) )
        startCtrl.SetToolTipString("Beginning of the simulation")
        box3.Add(startCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        label32 = wx.StaticText(parent, -1, "dt0:")
        label32.SetHelpText("This is the help text for the label")
        box3.Add(label32, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.dt0Ctrl = dt0Ctrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        dt0Ctrl.SetHelpText("Here's some help text for field #1")
        dt0Ctrl.SetValue( str(dt0) )
        dt0Ctrl.SetToolTipString("Initial time step")
        box3.Add(dt0Ctrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        label33 = wx.StaticText(parent, -1, "final time:")
        label33.SetHelpText("This is the help text for the label")
        box3.Add(label33, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.simulationTimeCtrl = simulationTimeCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        simulationTimeCtrl.SetHelpText("Here's some help text for field #1")
        simulationTimeCtrl.SetToolTipString("Final time of the simulation")
        simulationTimeCtrl.SetValue( str(simulationTime) )
        box3.Add(simulationTimeCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
               
        # Combo box for the unit of the dates
        
        label34 = wx.StaticText(parent, -1, "   Times unit:")
        label34.SetHelpText("This is the help text for the label")
        box3.Add(label34, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
        
        self.datesUnits = datesUnits =  self.params.getParam(parameters.GlobalPlotUnits_list).getDefault()
        self.dateUnit = dateUnit = wx.ComboBox(parent, -1, "",(250, 20), (70, -1),datesUnits, wx.CB_DROPDOWN)
        dateUnit.SetToolTipString("Unit for all time values")
        self.dateUnit.SetValue(self.Unit)
        box3.Add(dateUnit, 0., wx.ALIGN_CENTER|wx.ALL, 1)
        simul.Bind(wx.EVT_COMBOBOX, self._changeUnit )

        sizer.Add( box3, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
#
# Coupling algorithm
#
#        
#Iterative coupling algorithm
#
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Iterative algorithm parameters:" ) , wx.HORIZONTAL)
        box4.SetMinSize((40,20))

        dtmin = params.getParam( parameters.Iterate_MinTimeStep )
        dtmax = params.getParam( parameters.Iterate_MaxTimeStep )
        picardTargetNumber = params.getParam( parameters.Iterate_PicardTargetNumber )
        picardMaxOfIterations = params.getParam( parameters.Iterate_PicardMaxOfIterations )
        epsPicard = params.getParam( parameters.Iterate_CouplingPrecision )
        
        label1 = wx.StaticText(parent, -1, "Max. Picard Iterations:",size=(180,-1))
        CCctrls.append(label1)
        
        label1.SetHelpText("This is the help text for the label")
        box4.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
 
        self.maxPicardCtrl = maxPicardCtrl = wx.TextCtrl(parent, -1,str(picardMaxOfIterations.getValue()),size=(60,20))
        CCctrls.append(maxPicardCtrl)
        maxPicardCtrl.SetHelpText("Here's some help text for field #1")
        box4.Add(maxPicardCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        label2 = wx.StaticText(parent, -1, "Target iteration N.:",size=(150,-1))
        box4.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        CCctrls.append(label2)

        self.targetCtrl = targetCtrl = wx.TextCtrl(parent, -1,str(picardTargetNumber.getValue()), size=(60,20))
        CCctrls.append(targetCtrl)
        box4.Add(targetCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        label3 = wx.StaticText(parent, -1, "epsilon:",size=(60,-1))
        label3.SetHelpText("This is the help text for the label")
        CCctrls.append(label3)
        box4.Add(label3, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.epsPicardCtrl = epsPicardCtrl = wx.TextCtrl(parent, -1, str(epsPicard.getValue()), size=(60,20))
        CCctrls.append(epsPicardCtrl)
        box4.Add(epsPicardCtrl, 1, wx.LEFT|wx.RIGHT, 1)
               
        sizer.Add(box4, 0, wx.ALIGN_LEFT|wx.ALL, 1 )        
#
# time step bounds
#  	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   	
    	
    	box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "time step bounds:" ) , wx.HORIZONTAL)
        box5.SetMinSize((250,30))
        
        label51 = wx.StaticText(parent, -1, "Min Time Step:")
        label51.SetHelpText("This is the help text for the label")
        CCctrls.append(label51)
        box5.Add(label51, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        self.minTimeStep = minTimeStep = wx.TextCtrl(parent, -1, "", size=(80,-1))
        minTimeStep.SetHelpText("Here's some help text for field #1")
        minTimeStep.SetToolTipString("time step control: minimal time step")
        minTimeStep.SetValue( str(startTime) )
        CCctrls.append(minTimeStep)
        box5.Add(minTimeStep, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
        
        minTimeStep= inUnitConverter(params.getParam( parameters.Elmer_Min_Time_Step ).getValue(), self.Unit)
    	self.minTimeStep.SetValue( str(minTimeStep) ) 
              
        label52 = wx.StaticText(parent, -1, "Max Time Step:")
        label52.SetHelpText("This is the help text for the label")
        CCctrls.append(label52)
        box5.Add(label52, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.maxTimeStep = maxTimeStep = wx.TextCtrl(parent, -1, "", size=(80,-1))
        maxTimeStep.SetHelpText("Here's some help text for field #1")
        maxTimeStep.SetToolTipString("time step control: maximal time step")
        maxTimeStep.SetValue( str(dt0) )
        CCctrls.append(maxTimeStep)
        box5.Add(maxTimeStep, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        maxTimeStep= inUnitConverter(params.getParam( parameters.Elmer_Max_Time_Step ).getValue(), self.Unit)
    	self.maxTimeStep.SetValue( str(maxTimeStep) )
    	
        sizer.Add( box5, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
#
# Relaxation factor bounds
#
        box6 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "relaxation factor bounds:" ) , wx.HORIZONTAL)
        box6.SetMinSize((480,20))

        omegaMin = params.getParam( parameters.Iterate_RelaxationMinFactor )
        omegaMax = params.getParam( parameters.Iterate_RelaxationMaxFactor )
        
        label61 = wx.StaticText(parent, -1, "Min. relaxation:",size=(180,-1))
        label61.SetHelpText("This is the help text for the label")
        CCctrls.append(label61)
        box6.Add(label61, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
 
        self.omegaMinCtrl = omegaMinCtrl = wx.TextCtrl(parent, -1,str(omegaMin.getValue()),size=(40,20))
        omegaMinCtrl.SetHelpText("Here's some help text for field #1")
        CCctrls.append(omegaMinCtrl)
        box6.Add(omegaMinCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        label62 = wx.StaticText(parent, -1, "Max. relaxation:",size=(150,-1))
        CCctrls.append(label62)
        box6.Add(label62, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.omegaMaxCtrl = omegaMaxCtrl = wx.TextCtrl(parent, -1,str(omegaMax.getValue()), size=(20,20))
        CCctrls.append(omegaMaxCtrl)
        box6.Add(omegaMaxCtrl, 1, wx.LEFT|wx.RIGHT, 1)

        sizer.Add(box6, 0, wx.ALIGN_LEFT|wx.ALL, 1 )        
        
        if self.cc == None or self.cc == False:
            for text in self.CCctrls:
                text.Enable(False)
    	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   	

        
    	parent.SetSizerAndFit(sizer)
         
        
        if self.TimeSteppingMethod.GetValue() == "BDF" :
            self.BDFOrderCtrl.Enable(True)
        if self.TimeSteppingMethod.GetValue() == "Crank-Nicolson" :
            self.BDFOrderCtrl.Enable(False)
            
    def _changeSolver(self,event): 
        if self.TimeSteppingMethod.GetValue() == "BDF" :
            self.BDFOrderCtrl.Enable(True)
        if self.TimeSteppingMethod.GetValue() == "Crank-Nicolson" :
            self.BDFOrderCtrl.Enable(False)
            
    def _changeUnit(self, event):
        newUnit = self.dateUnit.GetValue()
        print newUnit
        oldUnit = self.Unit
        boxes = [ self.startCtrl, self.dt0Ctrl, self.simulationTimeCtrl, self.minTimeStep, self.maxTimeStep ]
        for box in boxes:
            box.SetValue(str(inSecondsConverter(str(box.GetValue()) + ' ' + oldUnit, False)))
            box.SetValue(str(inUnitConverter(box.GetValue(), newUnit)))
        self.Unit = newUnit

    def _onCCSelect( self, event ):
        radio_selected = event.GetEventObject()
        if radio_selected.GetLabel()=="CC":
            self.cc = True
        else:
            self.cc = False

        for text in self.CCctrls:
            if radio_selected.GetLabel()=="CC":
                text.Enable(True)
            else:
                text.Enable(False)
        
    def _onOk(self, params):
# coupling algotithm        
        radio1 = filter(lambda r: r.GetValue(), self.radios1)[0]
        name = radio1.GetLabelText()
        params.getParam(parameters.Iterate_Default_Algorithm).setValue(ITERATE_ALGORITHMS_BY_LABEL[name])

        unit = ' ' + self.dateUnit.GetValue()
# NI time parameters
        self.params.getParam(parameters.Elmer_Time_Stepping_Method).setValue(self.TimeSteppingMethod.GetValue())
        self.params.getParam(parameters.Elmer_BDF_Order).setValue(self.BDFOrderCtrl.GetValue())
        self.params.getParam(parameters.Elmer_Iterate_InitialTime).setValue(float(inSecondsConverter(str(self.startCtrl.GetValue()) + unit, False)))
        self.params.getParam(parameters.Elmer_Iterate_InitialTimeStep).setValue(float(inSecondsConverter(str(self.dt0Ctrl.GetValue()) + unit, False)))
        self.params.getParam(parameters.Elmer_Iterate_SimulationTime).setValue(float(inSecondsConverter(str(self.simulationTimeCtrl.GetValue()) + unit, False)))
        self.params.getParam(parameters.Elmer_Min_Time_Step).setValue(float(inSecondsConverter(str(self.minTimeStep.GetValue()) + unit, False)))
        self.params.getParam(parameters.Elmer_Max_Time_Step).setValue(float(inSecondsConverter(str(self.maxTimeStep.GetValue()) + unit, False)))
        self.params.getParam(parameters.TimeUnit).setValue(self.Unit) 
#
# CC algorithms
#        
        if self.cc:
            
            self.params.getParam(parameters.Iterate_Algorithm).setValue("CC")
            
            picardMaxOfIterations = params.getParam( parameters.Iterate_PicardMaxOfIterations )
            value = self.maxPicardCtrl.GetValue()
            picardMaxOfIterations.setValue(str(value))

            picardTargetNumber = params.getParam( parameters.Iterate_PicardTargetNumber )
            value = self.targetCtrl.GetValue()
            picardTargetNumber.setValue(str(value))

            epsPicard = params.getParam( parameters.Iterate_CouplingPrecision )
            value = self.epsPicardCtrl.GetValue()
            epsPicard.setValue(str(value))
 
            dtmin = params.getParam( parameters.Iterate_MinTimeStep )
            value = self.minTimeStep.GetValue()
            dtmin.setValue( int(inSecondsConverter(str(value) + unit, False)) )

            dtmax = params.getParam( parameters.Iterate_MaxTimeStep )
            value = self.maxTimeStep.GetValue()
            dtmax.setValue(int(inSecondsConverter(str(value) + unit, False)) )
 
            omegaMin = params.getParam( parameters.Iterate_RelaxationMinFactor )
            value = self.omegaMinCtrl.GetValue()
            omegaMin.setValue(str(value))

            omegaMax = params.getParam( parameters.Iterate_RelaxationMaxFactor )
            value = self.omegaMaxCtrl.GetValue()
            omegaMax.setValue(str(value))
        else:
            self.params.getParam(parameters.Iterate_Algorithm).setValue("NI")
            
#        print '\n\n\nt0 = ', self.params.getParam(parameters.Elmer_Iterate_InitialTime).getValue()
#        print 'dt0 = ', self.params.getParam(parameters.Elmer_Iterate_InitialTimeStep).getValue()
#        print 'tmax = ', self.params.getParam(parameters.Elmer_Iterate_SimulationTime).getValue()
#        print 'dtmin = ', self.params.getParam(parameters.Elmer_Min_Time_Step).getValue()
#        print 'dtmax = ', self.params.getParam(parameters.Elmer_Max_Time_Step).getValue()
#        print 'maintenant le CC:'
#        print 'dtmin = ', self.params.getParam(parameters.Iterate_MinTimeStep).getValue()
#        print 'dtmax = ', self.params.getParam(parameters.Iterate_MaxTimeStep).getValue()

        return True

