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
       <html><body>
       <a><b>Linear systems</b> may be solved in a robust way by using direct methods.<br>
       There are two different options for direct methods in ElmerSolver.<br> 
       The default method utilizes the well-known <b>LAPACK</b> collection of subroutines for band matrices.<br>
       ElmerSolver provides access to a set of Krylov subspace methods for the iterative solution of linear systems.<br>
       These methods may be applied to the solution large linear systems;<br>
       but rapid convergence generally requires that these methods have to be used in combination with preconditioning.<br>
       The Krylov subspace methods available in ElmerSolver are:<br>
       <OL start=1><LI type=1>Conjugate Gradient (<b>CG</b>)</li>
       Conjugate Gradient Squared (<b>CGS</b>)</li>
       <LI type=1>Biconjugate Gradient Stabilized (<b>BiCGStab</b>)</li>
       <LI type=1>Transpose-Free Quasi-Minimal Residual (<b>TFQMR</b>)</li>
       <LI type=1>Generalized Minimal Residual (<b>GMRES</b>)</li>
        </OL>
       </body></html>

       """
       
class ParametersElmer(ParamsAction):

    """
    Enables the choice of the parameters
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Algebraic Solver parameters",description  =description,help=HELP)
        self.params_mgr = params_mgr
        self.Direct = False
        self.Iterative = False
        
    def _createInterface(self, parent, params):
    
        self.params = params  	
    	self.parent = parent
    	
#
# Sizer / 
#    	
    	sizer = wx.BoxSizer( wx.VERTICAL )
    	simul = self.GetDialogPanel()
    
        
   	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        wx.TextCtrl.SetTTS = wx.TextCtrl.SetToolTipString
        wx.StaticText.SetTTS = wx.StaticText.SetToolTipString
        wx.CheckBox.SetTTS = wx.CheckBox.SetToolTipString
        wx.Button.SetTTS = wx.Button.SetToolTipString
    	
    	box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box1.SetMinSize((100,20))
    	
    	label1 = wx.StaticText(parent, -1, "Linear System Solver:")
        label1.SetHelpText("This is the help text for the label")
        box1.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        LinearSystemSolver_list = ["Direct","Iterative"]
        
        self.LinearSystemSolver = LinearSystemSolver = wx.ComboBox(parent, -1, "",
                                 (250, 15), (200, -1),
                                 LinearSystemSolver_list, 
                                 wx.CB_DROPDOWN)
        self.LinearSystemSolver.SetToolTipString("Choice of the algebraic resolution method")
        LinearSystemSolver = params.getParam( parameters.Elmer_Linear_Solver ).getValue()  	
    	self.LinearSystemSolver.SetValue(LinearSystemSolver)
    	
    	simul.Bind(wx.EVT_COMBOBOX, self._changeSolver )
    	
    	box1.Add(self.LinearSystemSolver, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#    	
#    Linear System Direct Method:	
#    	
    	box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box2.SetMinSize((200,20))
    	  
    	lab2 = "Linear System " + "Direct " + "Method:"
    	Method_list2 = ["Banded" , "Umfpack"]  
    	 
    	label2 = wx.StaticText(parent, -1, lab2)
        label2.SetHelpText("This is the help text for the label")
        box2.Add(label2, 0, wx.LEFT|wx.ALL, 2)
        
        self.SolverMethodD = SolverMethodD = wx.ComboBox(parent, -1, "Banded",
                                 (150, 15), (100, -1),
                                 Method_list2, wx.CB_DROPDOWN)
        self.SolverMethodD.SetToolTipString("The default is banded, or a sparse matrix solver with value umfpack")
                                 
        Elmer_Direct_Method = params.getParam( parameters.Elmer_Direct_Method ).getValue()   	
    	self.SolverMethodD.SetValue(Elmer_Direct_Method) 
                                 
        self.SolverMethodD.Enable(False)
        
        box2.Add(self.SolverMethodD, 0, wx.LEFT|wx.ALL, 1)
#    	sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

#        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
#        box3.SetMinSize((100,20))
    	  
    	Choice = ["True" , "False"]  
    	 
    	label3 = wx.StaticText(parent, -1, "Optimize Bandwidth")
        label3.SetHelpText("The default is banded, or a sparse matrix solver with value umfpack")
        box2.Add(label3, 0, wx.LEFT|wx.ALL, 2)
        
        self.Bandwidth = Bandwidth = wx.ComboBox(parent, -1, "",
                                 (250, 15), (100, -1),
                                 Choice, wx.CB_DROPDOWN)
        self.Bandwidth.SetToolTipString("")
        
        Elmer_Optimize_Bandwidth = params.getParam( parameters.Elmer_Optimize_Bandwidth ).getValue()   	
    	self.Bandwidth.SetValue(Elmer_Optimize_Bandwidth) 
                                 
        self.Bandwidth.Enable(False)
        
        box2.Add(self.Bandwidth, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
    	
    	
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~          
        
        
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box4.SetMinSize((200,20))
    	     
    	
    	label4 = wx.StaticText(parent, -1, "Linear System Convergence Tolerance")
        label4.SetHelpText("This is the help text for the label")
        box4.Add(label4, 0, wx.LEFT|wx.ALL, 2)
        
        self.ConvergenceTolerance = ConvergenceTolerance = wx.TextCtrl(parent, -1,"",size=(50,-1))
        
        Elmer_Convergence_Tolerance = params.getParam( parameters.Elmer_Convergence_Tolerance ).getValue()   	
    	self.ConvergenceTolerance.SetValue(str(Elmer_Convergence_Tolerance) )
        
        box4.Add(self.ConvergenceTolerance, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box4, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   	
        
        box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box5.SetMinSize((200,20))
    	 
    	Method_list5 = ["CG" , "CGS" , "BICGStab" , "TFQMP" , "GMRES"] 
    	   
    	label5 = wx.StaticText(parent, -1, "Linear System Iterative Method:")
        label5.SetHelpText("This is the help text for the label")
        box5.Add(label5, 0, wx.LEFT|wx.ALL, 2)
        
        self.SolverMethodI = SolverMethodI = wx.ComboBox(parent, -1, "CG",
                                 (250, 15), (100, -1),
                                 Method_list5, wx.CB_DROPDOWN)
        self.SolverMethodI.SetToolTipString("Choice of the iterative solver method,\nthe conjugate gradient solver is the default")
        
        Elmer_Iterative_Method = params.getParam( parameters.Elmer_Iterative_Method ).getValue()   	
    	self.SolverMethodI.SetValue(Elmer_Iterative_Method) 
        
        self.SolverMethodI.Enable(False)
        
        box5.Add(self.SolverMethodI, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box5, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        
        box6 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box6.SetMinSize((200,20))
    	   
    	label6 = wx.StaticText(parent, -1, "Linear System GMRES Restart")
        label6.SetHelpText("This is the help text for the label")
        box6.Add(label6, 0, wx.LEFT|wx.ALL, 2)
        
        self.GMRESRestart = GMRESRestart = wx.TextCtrl(parent, -1,"",size=(50,-1))
        
        Elmer_GMRES_Restart = params.getParam( parameters.Elmer_GMRES_Restart ).getValue()   	
    	self.GMRESRestart.SetValue(str(Elmer_GMRES_Restart)) 
        
        self.GMRESRestart.Enable(False)
        
        box6.Add(self.GMRESRestart, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box6, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# - Linear System Preconditioning
#    	
        box7 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box7.SetMinSize((200,20))
    	   
    	Preconditioning_list = ["ILU0" , "ILU1" , "ILU2" , "ILU3" , "ILU4" , "ILU5" , "ILU7" , "ILU7" ,\
"ILU8" , "ILU9" , "ILUT" , "Multigrid"]   
    	
    	label7 = wx.StaticText(parent, -1, "Linear System Preconditioning")
        label7.SetHelpText("This is the help text for the label")
        box7.Add(label7, 0, wx.LEFT|wx.ALL, 2)
        
        self.Preconditioning = SolverMethodI = wx.ComboBox(parent, -1, "",
                                 (250, 20), (100, -1),
                                 Preconditioning_list, wx.CB_DROPDOWN)
        
        Elmer_Preconditioning = params.getParam( parameters.Elmer_Preconditioning ).getValue()   	
    	self.Preconditioning.SetValue(Elmer_Preconditioning) 
        
        self.Preconditioning.Enable(False)
        
        box7.Add(self.Preconditioning, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box7, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# - Linear System ILUT Tolerance
#    	
    	box8 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box8.SetMinSize((200,20))
    	     
    	
    	label8 = wx.StaticText(parent, -1, "Linear System ILUT Tolerance")
        label8.SetHelpText("This is the help text for the label")
        box8.Add(label8, 0, wx.LEFT|wx.ALL, 2)
        
        self.ILUTTolerance = ILUTTolerance = wx.TextCtrl(parent, -1,"",size=(50,-1))
        
        Elmer_ILUT_Tolerance = params.getParam( parameters.Elmer_ILUT_Tolerance ).getValue()   	
    	self.ILUTTolerance.SetValue(str(Elmer_ILUT_Tolerance)) 
        
        self.ILUTTolerance.Enable(False)
        
        box8.Add(self.ILUTTolerance, 0, wx.LEFT|wx.ALL, 1)
    	sizer.Add( box8, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

        
    	
        
    	parent.SetSizerAndFit(sizer)
        
        if self.LinearSystemSolver.GetValue() == "Direct" :
            self.SolverMethodD.Enable(True)
            self.Bandwidth.Enable(True)
            self.SolverMethodI.Enable(False)
        if self.LinearSystemSolver.GetValue() == "Iterative" :
            self.SolverMethodD.Enable(False)
            self.Bandwidth.Enable(False)
            self.SolverMethodI.Enable(True)
        if self.LinearSystemSolver.GetValue() == "Iterative" and self.SolverMethodI.GetValue() == "GMRES" :
            self.GMRESRestart.Enable(True)
            self.Preconditioning.Enable(True)
        else :
            self.GMRESRestart.Enable(False)
            self.Preconditioning.Enable(False)
        if self.LinearSystemSolver.GetValue() == "Iterative" and self.SolverMethodI.GetValue() == "GMRES" and self.Preconditioning.GetValue() == "ILUT" :
            self.ILUTTolerance.Enable(True)  
        else :
            self.ILUTTolerance.Enable(False)
            
            
            
    def _changeSolver(self,event):
        if self.LinearSystemSolver.GetValue() == "Direct" :
            self.SolverMethodD.Enable(True)
            self.Bandwidth.Enable(True)
            self.SolverMethodI.Enable(False)
        if self.LinearSystemSolver.GetValue() == "Iterative" :
            self.SolverMethodD.Enable(False)
            self.Bandwidth.Enable(False)
            self.SolverMethodI.Enable(True)
        if self.LinearSystemSolver.GetValue() == "Iterative" and self.SolverMethodI.GetValue() == "GMRES" :
            self.GMRESRestart.Enable(True)
            self.Preconditioning.Enable(True)
        else :
            self.GMRESRestart.Enable(False)
            self.Preconditioning.Enable(False)
        if self.LinearSystemSolver.GetValue() == "Iterative" and self.SolverMethodI.GetValue() == "GMRES" and self.Preconditioning.GetValue() == "ILUT" :
            self.ILUTTolerance.Enable(True)  
        else :
            self.ILUTTolerance.Enable(False)
            
     
    def _onOk(self, params):
        

        self.params.getParam(parameters.Elmer_Linear_Solver).setValue(self.LinearSystemSolver.GetValue())
        self.params.getParam(parameters.Elmer_Direct_Method).setValue(self.SolverMethodD.GetValue())
        self.params.getParam(parameters.Elmer_Iterative_Method).setValue(self.SolverMethodI.GetValue())
        self.params.getParam(parameters.Elmer_Optimize_Bandwidth).setValue(self.Bandwidth.GetValue())
        try :
            self.params.getParam(parameters.Elmer_Convergence_Tolerance).setValue(float(str(self.ConvergenceTolerance.GetValue())))
        except :
            dlg = wx.MessageDialog(self.getParent(), 'Convergence Tolerance should be a real',
                               'A Message Box',
                               wx.OK | wx.ICON_INFORMATION
                               )
            val = dlg.ShowModal()
            dlg.Destroy() 
        try :
            self.params.getParam(parameters.Elmer_GMRES_Restart).setValue(int(str(self.GMRESRestart.GetValue())))
        except :
            dlg = wx.MessageDialog(self.getParent(), 'GMRES Restart should be an integer',
                               'A Message Box',
                               wx.OK | wx.ICON_INFORMATION
                               )
            val = dlg.ShowModal()
            dlg.Destroy() 
        self.params.getParam(parameters.Elmer_Preconditioning).setValue(self.Preconditioning.GetValue())
        try :
            self.params.getParam(parameters.Elmer_ILUT_Tolerance).setValue(float(str(self.ILUTTolerance.GetValue())))
        except :
            dlg = wx.MessageDialog(self.getParent(), 'ILUT Tolerance should be a real',
                               'A Message Box',
                               wx.OK | wx.ICON_INFORMATION
                               )
            val = dlg.ShowModal()
            dlg.Destroy() 
    
        return True
