import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters
from geoi.actions.pywrite import *
from geoi.scripting.chemical import _chemical,_addenda
from geoi.scripting.elmer import _algebraicResolution, _chemicaltransportmodule, _elmerimport, _materials,\
                                 _meshimport, _outputs, _problem, _regions, _moduleLooping, _postProcessing
import os
import shutil # shell utility
import subprocess

from wx.lib.embeddedimage import PyEmbeddedImage
import wx.lib.platebtn as platebtn

description =\
       """ 
       Check that you have :
       Defined a Title
       Defined your Aqueous State
       Defined your Materials
       Load a .msh Mesh
       Set Zones
       Completed Parameters First and Second Part for Elmer
       """
HELP = """
           Enables to:
    
          - switch between 
          
                - A constant and a variable temperature
                - Porosity variation
                - Launch of the simulation
       """
       
class SimulateElmer(ParamsAction):

    """
    Enables to:
    
          - switch between 
          
                - A constant and a variable temperature
                - Porosity variation
                - Launch of the simulation
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Simulation",description  =description,help=HELP)
        self.params_mgr = params_mgr

    def _createInterface(self, parent, params):
    	self.params = params  	
    	self.parent = parent  	
    	self.retpython = None
        Monkey = PyEmbeddedImage(
    "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"
    "nMQUbKYAAAAASUVORK5CYII=")
    	flag_green = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAABC9J"
    "REFUOI2lld1vlEUUxp8zc2be9113tx9QGgWtgFAsUTSkUUJCDRd+f1wQE6+4UsOdXKjXJkaC"
    "if+BNyZGxRsDRiGSQIwxSBAqETC1dCnUbVmh3W7pLt33Y+Z4sdsCkUTAkzxXk/nNM+d9nzO0"
    "bt06RUQ+TdPBwcHBn4eHh7cYY4ZFRDUaDd+7tgMnfzyLuy0WESEiENGVSqXyZ5w2q2NjZWx+"
    "dzX1vphHbfwatry5AVZrxKnD8Z0jdwSm9evXo6OjAwA6S6XS0Wq1+hKAywBo19/bZfJETVmj"
    "KbIsUaAlDBhRwBIGjFzACC3fHjw0NETFfFE8+dVTk1Pn4/7ZkVXP93wR2/hQrTZ/LpY4Lebz"
    "YKVxqXIN377zOpoSY6XNo4g8vrxyGon3gABEBAKw+/79oG3btlEx3yGi/OqJixMj8eOztveZ"
    "TiAvYlhdiAL+NbT6VBTwuTDgS6Hl6cDoOhHir74/654dWoONfT1grboApADqAMAEAhEgBBAR"
    "xVmCVNLsPmPZsl5rWK01rN5grcBaCbOat1bPR5Ybu3c+tWBYRRBYAAcAfLwElpv6IgC0JoSW"
    "OQoYhrUERvvAaliryRqtLKsiK1W0VsFoBQjKAnkfgq+bifNhoNF23G52W0YrhFYjDBhGK7JG"
    "68BoBEbDsoI1GoUOC8SSZbH/8LW+/o8eQZf7fOF3SCaYbcQtsPMezjkIhLz3YFYIA0ZkGawV"
    "rFEw3ALnCxYWypeOVfHbycs+3x/uGO2ffbGnMzexrCM8qhV9Y1hdcd6DszRFkiQQLXDOIWCF"
    "0LKEAQsrkjBk5HIG2pOaKS3QhZF5dTVuoPBkzq5YllvOSh1UhANEOJE5f7WnK0J1rglOsxRJ"
    "kgIsyDKHvFaIrKYoZDJKwSce5YtzmCrXUXe+xt3qbHd3eLRgzMFOBKdsg7LJ+jz+mprHZ9uP"
    "3UhemmZIdALyAucyWKsRhaYZBTxcvdA4c/74dGW62RwPB8LRVVvzo/s3jc3guTw2be3C9Q0Z"
    "Huwt6Ac6C7K8M/KflF/FEyuXYWR6DjQwMEBhEAlI1szMzIx2Pe3ee3vf1n17+w5Xfiq9Jd9l"
    "JYyPVzE8fhXeC5KKply3qEJopbsYevGChcQhTjM82rcCezYeWoo0BUEgIrKmVquNlMvlzaTp"
    "zKYdq/Qrezfi9P5JTFSuIT+Qk2gFi1toijIEqFaUj7z8x+2HUJqmUEpBpPXxtCXlEsHYkWn5"
    "9IXjftcPW/DYdYc9A4fvaPgsgbMsA1Hrb3bOwSXiAWChlkhzLsUHDx+6K+AtjttFWZbdsigi"
    "/9pwV44XAc65xSBCRJZuck9g59wSyHsPtJINESHv/T1b5nq9vuQsyzJBaxZB/k8fcGuPiwAM"
    "gIfQekEKi4e0y98k9x/y+qaNGsAvbagCEAEIAdi2uC3dXle4MRQXa+nG/wAkB+eGnJ9P7QAA"
    "AABJRU5ErkJggg==")
        flag_red = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAA95J"
    "REFUOI2dlc1rXFUYxn/n3HvnI5kvm6RgwdhQWmoXXQgp2k033agIlW5cCFYQceVK/AcSKy5V"
    "cCHislUUoZsKUkLRQqm2U7BN7HSaWjsmk0nSMNP5yNw5H6+LTJIJLmr6wHvhcjjPec7zvs+9"
    "6uDBg1op5Y0xk5OTk1eKxeLLURgWBXS71fLx4iLL3rNbhCIiSimUUstLS0uluNtdu7d/P6fm"
    "5tTrzSa9kRGWrKW9dy+pUonp/0msDh06RD6fByjMz8/PrK2tvQZUAbVw5oz8cu2a9sYo8V68"
    "MWI7Hbr1ujSdowGsA89ns+zJ54kbDfAepTXqxIkTKlcoiDg3sbCwUObWrdILYXhuj9Y/jVl7"
    "aywIzApgRLja7XJJ5MlqlSIUQEQQ77HWuiQcEZgOYSozPHx/eGjo94zWN0RkdqLd/vsLpVbv"
    "Qes8xCsjI+6b1VVeAq6Pjz8T1+sG71tfZ7OEauCUjQcAVmkdhun0gUQ+fyDKZN6MhocJ02kJ"
    "0+nmkaGh5hupVDuRza4np6bSq7VaIspmLzQqlU870MppvaGYvurBpiqt0VEkQRT5MJUiymRU"
    "olDQiVwul8jnc0OjoxAEtCqVfxrl8kffzs19dwH850BybGynYsVOKFAoFWy+S78xAVCbnbW1"
    "YnHqrZs3Pwbce8D7wFA+j+92CZ33OOfAOeUHVIsI3nu8c3jnEBECETorK/7Bw4e0Ewk/fuzY"
    "6V+PH3+1Xa0+XL5+faazuPhjp9FYTiaThNYYer0eOIezdpu3P17KWrS1xI2GXq3Xlc1m9ei+"
    "fUxkMgnp9Ua79fpF02xeEOd+89auzAJH45jQGIMxBpzDOrftgohycczjZpP2+jqSTpMvFOqj"
    "xtwO7tyZKd+/f/FctXpjFexxIAQ+G2ySsXZb8TZxDBRrvd4fc73eUiGd/uuoyN2xSuXuK9PT"
    "j7rlMqkrVzgDFM+eDRYvX5ZHt2/7L6tVfgBOQ9+KOAYRnLW6IfLhHq3Pf+9c9e1sVoJ2G4ki"
    "Jk6eJEyl+DOdVpWFBb12+LA8KJX8GLhUFPFsMskHQAmYAUJrLabXQ0Rwzvmycz/f63QWX0wm"
    "g7E4phNFaO+Zv3RJEvW6XG00RIF7rn/9dwGM2agdVhiD1nqTGA3aA3eck0/i2J8KAqwxvFOr"
    "sRuE1tqtwDnn8OABuiISe89Xvd6uCHco7kPZ7XED/pPG3SveJHDObYVPRAY+HU9BvDlim0mD"
    "jWSLiPLeP7XksNVqbSmz1gogfeKn94GdHueACBhn4w+S3TykDz9Q7gnlg4GNAXC1T6qBNJAC"
    "Ev0K+xX01zUbtg02YuvG/wIRNEX6jHrsmwAAAABJRU5ErkJggg==")

    	sizer = wx.BoxSizer( wx.VERTICAL )
    	simul = self.GetDialogPanel()
    	#
    	# Temperature
    	#
    	boxTemp = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        boxTemp.SetMinSize((400,100))
        grid1 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid1.SetFlexibleDirection( wx.VERTICAL) 
    	
    	self.temperature = wx.CheckBox(parent, -1, "variable temperature")
    	if self.params.getParam(parameters.TemperatureVariable).getValue() == "True" :
    	    self.temperature.SetValue(True)
    	else :
    	    self.temperature.SetValue(False)
    	simul.Bind(wx.EVT_CHECKBOX, self._temperature, self.temperature)
    	
    	boxTemp.Add(self.temperature, 0, wx.TOP|wx.ALL, 2)
    	
    	sizer.Add( boxTemp, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
        #
        # Porosity
        #
    	boxPorosity = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        boxPorosity.SetMinSize((400,50))
    	
    	self.porosity = wx.CheckBox(parent, -1, "variable porosity")
    	if self.params.getParam(parameters.PorosityState).getValue() == "variable porosity" :
    	    print " we set to true the check box according to the data "
    	    self.porosity.SetValue(True)
    	else :
    	    self.porosity.SetValue(False)
    	simul.Bind(wx.EVT_CHECKBOX, self._porosity, self.porosity)
    	
    	boxPorosity.Add(self.porosity, 0, wx.TOP|wx.ALL, 2)
    	        
        sizer.Add( boxPorosity, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
        #
        # Simulation And Cancel
        #
#    	boxSimulate = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
#        boxSimulate.SetMinSize((100,100))
    	boxSimulation = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        boxSimulation.SetMinSize((200,50))

        monkey = Monkey.GetBitmap()
        greenFlag = flag_green.GetBitmap()
        redFlag   = flag_red.GetBitmap()
        self.simulate = platebtn.PlateButton(parent, -1, "Simulate       ",greenFlag, (200,150))
        self.simulate.SetOwnForegroundColour(wx.BLUE)
        simul.Bind(wx.EVT_BUTTON, self._simulate, self.simulate)
#        boxSimulate.Add(self.simulate, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
        
#        sizer.Add( boxSimulate, 0, wx.ALIGN_CENTER|wx.ALL, 2 )
        boxSimulation.Add( self.simulate, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
    	#
    	
    	self.stopSimulation = platebtn.PlateButton(parent, -1, "stop simulation",redFlag, (200,150))
        self.stopSimulation.SetOwnForegroundColour(wx.RED)
        simul.Bind(wx.EVT_BUTTON, self._stopSimulation, self.stopSimulation)
        boxSimulation.Add( self.stopSimulation, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )
        sizer.Add( boxSimulation, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.CENTRE|wx.RIGHT|wx.TOP, 2 )
    	#    	
        infos ="                                                                                \n"*3
        self.information = information = wx.StaticText(parent, -1, infos)
        
        sizer.Add( self.information, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
        
    	parent.SetSizerAndFit(sizer)
    	
    	
    def _onOk(self, params):
    
        return True

    def _temperature(self,event) :
        if self.temperature.IsChecked()== True:
            self.params.getParam(parameters.TemperatureVariable).setValue("True")
            self.temperature.SetValue(True)
        else :   
            self.params.getParam(parameters.TemperatureVariable).setValue("False")              
            self.temperature.SetValue(False)

    def _porosity(self,event) :
        if self.porosity.IsChecked()== True:
            self.params.getParam(parameters.PorosityState).setValue("variable porosity")
            self.porosity.SetValue(True)
        else :   
            self.params.getParam(parameters.PorosityState).setValue("constant porosity")
            self.porosity.SetValue(False)
     
    def _stopSimulation(self,event): 
        if self.retpython != None :
            dlg = wx.MessageDialog(self.getParent(), 'Warning\nSimulation will be stopped\nContinue?',
                               'A Message Box',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               )
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == wx.ID_OK:
                os.system("kill -9 " + str(self.retpython.pid))
                
         
    def _simulate(self,event):
#        if not os.path.isdir("/home/david/Wrapper/Api/Geoi/src/geoi/Simulation"):
#     	    os.mkdir("/home/david/Wrapper/Api/Geoi/src/geoi/Simulation")    
#     	else :
#     		pass

     	nameFile = self.params.getParam(parameters.Title).getValue()
     	params=self.params
     	self.retpython = None
#     	directory = params.getParam(parameters.ResultDirectory).getValue()
     	 
#     	os.chdir(directory)
#     	print directory
     	pythonFile = os.getcwd()+"/"+nameFile+".py"
     	f1=open(pythonFile,"w") 
#
# elmer imports
#
        _elmerimport(f1)
      	
     	f1.write("setProblemType(\"ChemicalTransport\")\n\n")
#
# elmer mesh import
#
     	f1.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
     	f1.write("#   Mesh definition\n")
     	f1.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
#
     	_meshimport(self.params,f1)
#     	
     	zone_list = self.params.getParam(parameters.Zones_list).getValue()
     	i=0
     	for zone in zone_list:
     	    f1.write(str(zone)+str(i)+"Body = mesh.getBody(\""+str(zone)+"\")\n")
     	    f1.write(str(zone)+str(i)+"Body.getNodesNumber()\n")
     	    i+=1

        f1.write("numberOfVertices = mesh._getNumberOfVertices()\n")
#
# materials
#
        f1.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
        f1.write("#   Material\n")
        f1.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
#
        _materials(self.params,f1)
#
# regions
#
        f1.write("\n#~~~~~~~~~~~\n")
        f1.write("#~ Regions ~\n")
        f1.write("#~~~~~~~~~~~\n")
#
        zone_Material_AqueousState_list, regionList = _regions(self.params,f1)     
#
# chemistry
#
        _chemical(self.params,f1)
#
#
#
#chemical_state_quartz = ChemicalState ("column", AqueousSolution_column, columnMineralPhase)
#
        f1.write("#~~~~~~~~~~~~~~~~~~~~\n")
        f1.write("# Initial condition ~\n")
        f1.write("#~~~~~~~~~~~~~~~~~~~~\n")
        initialConditionList = self.params.getParam(parameters.InitialConditions_list).getValue()

        boundaryConditionList = self.params.getParam(parameters.BoundaryConditions_list).getValue()
        iCLS = "["
        for iC in initialConditionList:
            iCName = str(iC)+"IC"
            iCLS+=iCName+","
            iCParameters = zone_Material_AqueousState_list[zone_list.index(iC)]
            materialName = str(iCParameters[0]) + "Material"
            aqueousStateName = str(iCParameters[1])+"ChemicalState"
            f1.write(iCName+" = InitialCondition (body  = "+str(iC)+str(zone_list.index(iC))+"Body, value = "+aqueousStateName+")\n")
        if iCLS != "[": iCLS = iCLS[0:len(iCLS)-1]
        iCLS += "]"
        f1.write("#~~~~~~~~~~~~~~~~~~~~~\n")
        f1.write("# Boundary condition ~\n")
        f1.write("#~~~~~~~~~~~~~~~~~~~~~\n")
        bCLS = "["
        for iC in boundaryConditionList:
            iCName = str(iC)+"BC"
            bCLS+=iCName+","
            iCParameters = zone_Material_AqueousState_list[zone_list.index(iC)]
            materialName = str(iCParameters[0])+"Material"
            aqueousStateName = str(iCParameters[1])+"ChemicalState"
            f1.write(iCName+" = BoundaryCondition (boundary = "+str(iC)+str(zone_list.index(iC))+"Body, btype=\"Dirichlet\", value = "+aqueousStateName+")\n")
            
#bIC = BoundaryCondition (boundary = b0Zone, btype='Dirichlet', value = sodaChemicalState)
            
        if bCLS != "[": bCLS = bCLS[0:len(bCLS)-1]
        bCLS += "]"
#
# outputs
#
        f1.write("#~~~~~~~~~~~~~~~~~~~\n")
        f1.write("# Expected outputs ~\n")
        f1.write("#~~~~~~~~~~~~~~~~~~~\n")
#
        _outputs(self.params,f1)
#
# module
#            
        f1.write("#~~~~~~~~~\n")
        f1.write("# Module ~\n")
        f1.write("#~~~~~~~~~\n")
#
        _problem(self.params,f1, regionList, iCLS, bCLS)
        
        _chemicaltransportmodule(self.params,f1,"Elmer")
        
        species = self.params.getParam(parameters.PostprocessingContours_AqueousComponentsToPlot_list).getValue()
        frequency = self.params.getParam(parameters.PostprocessingContours_Parameters_list).getValue()
        if len(species)>0 :
            f1.write("module.setVtkOutputsParameters([") 
            for ind in range(len(species)-1) :
                f1.write("\""+species[ind]+"\",")
            f1.write("\""+species[len(species)-1]+"\"]," +  "\"" + str(frequency[1]) + "\"," + frequency[0] + ")\n\n")   
#        
# algebraic resolution
#        
        _algebraicResolution(self.params,f1)

#
# running module 
#

#        f1.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
#        f1.write("module.run()\n")
#        f1.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        f1.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        f1.write("#  transient algorithm    ~\n")
        f1.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        _moduleLooping(self.params,f1)

#        
# post processing
#        
        f1.write("\n\n")
        f1.write("#~~~~~~~~~~~~~~~~~~~~\n")
        f1.write("#  Post Processing  ~\n")
        f1.write("#~~~~~~~~~~~~~~~~~~~~\n")
      
        _postProcessing(self.params,f1)
        
        f1.flush()
        f1.close()
        while f1.closed == False:
            pass
        
#        wx.MessageDialog(self.parent, "Regarde le Terminal", "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
#        os.chdir(directory)
        
#        try:
#            retcode = subprocess.Popen("rm -f commandfile.eg", shell = True)
#            if retcode < 0:
#                print >>sys.stderr, "Child was terminated by signal", -retcode
#            else:
#                print >>sys.stderr, "Child returned", retcode
#        except OSError, e:
#            print >>sys.stderr, "Execution failed:", e

#        try:
#            retcode = subprocess.Popen("rm -rf " + nameFile , shell = True)
#            if retcode < 0:
#                print >>sys.stderr, "Child was terminated by signal", -retcode
#            else:
#                print >>sys.stderr, "Child returned", retcode
#        except OSError, e:
#            print >>sys.stderr, "Execution failed:", e    
        self.retpython = subprocess.Popen("python  " +nameFile+".py", shell = True)
    
