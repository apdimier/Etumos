import wx

from geoi.actions.params_action import ParamsAction
from geoi.scripting.chemical import _chemical,_addenda
from geoi import parameters
from geoi.actions.pywrite import *
import os

ITERATE_ALGORITHMS_BY_LABEL = {'NI':parameters.ITERATE_ALGORITHM_ONESTEP,'CC':parameters.ITERATE_ALGORITHM_CC }

description =\
       """ 
       To set the splitting parameters and to launch the simulation
       """
HELP = """
       <html><body>
       <a><b>Ni</b> designates a non iterative algorithm, using <b>primary species</b> as main unknowns.</a><br>
       <a><b>CC</b> is an iterative method using primary species as main unknowns,<br>
       the convergence over a time step being reached within a <b>Picard</b> algorithm.
       </a>
       </body></html>
       """


    
class CouplingAlgorithm(ParamsAction):
    """
    Enables the choice of transport discretisation and of the algebraic solver
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Simulate",description  =description,help=HELP)
        self.cc = None
        self.choice = None
        self.radios = None

    def _createInterface(self, parent, params):
        
        self.parent = parent
        sizer = wx.BoxSizer( wx.VERTICAL )
#
# Coupling algorithm
#
        couplingAlgorithmLabels = ITERATE_ALGORITHMS_BY_LABEL.keys()
        #discretisationLabels.sort()
   
        couplingAlgorithm = params.getParam(parameters.Iterate_Default_Algorithm)
        if couplingAlgorithm.getValue() == "CC": self.cc = True
#
        box0 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Splitting algorithm" ) , wx.VERTICAL )
        box0.SetMinSize((150,30))
        grid1 = wx.FlexGridSizer( 1, 4, 0, 0 )
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
        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Simulation time control" ) , wx.HORIZONTAL)
        box1.SetMinSize((250,30))

        start = params.getParam( parameters.Iterate_InitialTime )
        dt0 = params.getParam( parameters.Iterate_InitialTimeStepSize )
        simulationTime = params.getParam( parameters.Iterate_SimulationTime )
        
        label1 = wx.StaticText(parent, -1, "t0:")
        label1.SetHelpText("This is the help text for the label")
        box1.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        self.startCtrl = startCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        startCtrl.SetHelpText("Here's some help text for field #1")
        startCtrl.SetToolTipString("starting time for the simulation")
        startCtrl.SetValue( str(start.getValue()) )
        box1.Add(startCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        label2 = wx.StaticText(parent, -1, "dt0:")
        label2.SetToolTipString("time step")
        label2.SetHelpText("This is the help text for the label")
        box1.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.dt0Ctrl = dt0Ctrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        dt0Ctrl.SetHelpText("Here's some help text for field #1")
        dt0Ctrl.SetToolTipString("time step")
        dt0Ctrl.SetValue( str(dt0.getValue()) )
        box1.Add (dt0Ctrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
       
        label3 = wx.StaticText(parent, -1, "final time:")
        label3.SetHelpText("This is the help text for the label")
        box1.Add(label3, 0, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.simulationTimeCtrl = simulationTimeCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1))
        simulationTimeCtrl.SetHelpText("Here's some help text for field #1")
        simulationTimeCtrl.SetToolTipString("final time to be simulated")
        simulationTimeCtrl.SetValue( str(simulationTime.getValue()) )
        box1.Add(simulationTimeCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
               
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
#        
#Iterative coupling algorithm
#
        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Iterative algorithm parameters" ) , wx.HORIZONTAL)
        box2.SetMinSize((40,20))

        dtmin = params.getParam( parameters.Iterate_MinTimeStep )
        dtmax = params.getParam( parameters.Iterate_MaxTimeStep )
        picardTargetNumber = params.getParam( parameters.Iterate_PicardTargetNumber )
        picardMaxOfIterations = params.getParam( parameters.Iterate_PicardMaxOfIterations )
        epsPicard = params.getParam( parameters.Iterate_CouplingPrecision )
        
        label1 = wx.StaticText(parent, -1, "Max. Picard Iterations:",size=(180,-1))
        CCctrls.append(label1)
        
        label1.SetHelpText("This is the help text for the label")
        box2.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
 
        self.maxPicardCtrl = maxPicardCtrl = wx.TextCtrl(parent, -1,str(picardMaxOfIterations.getValue()),size=(60,20))
        CCctrls.append(maxPicardCtrl)
        maxPicardCtrl.SetHelpText("Here's some help text for field #1")
        box2.Add(maxPicardCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        label2 = wx.StaticText(parent, -1, "Target iteration N.:",size=(150,-1))
        box2.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        CCctrls.append(label2)

        self.targetCtrl = targetCtrl = wx.TextCtrl(parent, -1,str(picardTargetNumber.getValue()), size=(60,20))
        CCctrls.append(targetCtrl)
        box2.Add(targetCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        label3 = wx.StaticText(parent, -1, "epsilon:",size=(80,-1))
        label3.SetHelpText("This is the help text for the label")
        CCctrls.append(label3)
        box2.Add(label3, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.epsPicardCtrl = epsPicardCtrl = wx.TextCtrl(parent, -1, str(epsPicard.getValue()), size=(60,20))
        CCctrls.append(epsPicardCtrl)
        box2.Add(epsPicardCtrl, 1, wx.LEFT|wx.RIGHT, 1)
               
        sizer.Add(box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )        
#
# time step bounds
#
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "time step bounds:" ) , wx.HORIZONTAL)
        box3.SetMinSize((480,20))

        dtmin = params.getParam( parameters.Iterate_MinTimeStep )
        dtmax = params.getParam( parameters.Iterate_MaxTimeStep )
        
        label31 = wx.StaticText(parent, -1, "Min. time step:",size=(180,-1))
        label31.SetHelpText("This is the help text for the label")
        CCctrls.append(label31)
        box3.Add(label31, 0, wx.LEFT|wx.ALL, 1)
 
        self.minCtrl = minCtrl = wx.TextCtrl(parent, -1,str(dtmin.getValue()),size=(40,20))
        minCtrl.SetHelpText("Here's some help text for field #1")
        CCctrls.append(minCtrl)
        box3.Add(minCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        label32 = wx.StaticText(parent, -1, "Max. time step:",size=(150,-1))
        CCctrls.append(label32)
        box3.Add(label32, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.maxCtrl = maxCtrl = wx.TextCtrl(parent, -1,str(dtmax.getValue()), size=(40,20))
        CCctrls.append(maxCtrl)
        box3.Add(maxCtrl, 1, wx.LEFT|wx.RIGHT, 1)

        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )        
#
# Relaxation factor bounds
#
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "relaxation factor bounds:" ) , wx.HORIZONTAL)
        box4.SetMinSize((480,20))

        omegaMin = params.getParam( parameters.Iterate_RelaxationMinFactor )
        omegaMax = params.getParam( parameters.Iterate_RelaxationMaxFactor )
        
        label41 = wx.StaticText(parent, -1, "Min. relaxation:",size=(180,-1))
        label41.SetHelpText("This is the help text for the label")
        CCctrls.append(label41)
        box4.Add(label41, 0, wx.LEFT|wx.ALL, 1)
 
        self.omegaMinCtrl = omegaMinCtrl = wx.TextCtrl(parent, -1,str(omegaMin.getValue()),size=(40,20))
        omegaMinCtrl.SetHelpText("Here's some help text for field #1")
        CCctrls.append(omegaMinCtrl)
        box4.Add(omegaMinCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        label42 = wx.StaticText(parent, -1, "Max. relaxation:",size=(150,-1))
        CCctrls.append(label42)
        box4.Add(label42, 0, wx.LEFT|wx.ALL, 1)

        self.omegaMaxCtrl = omegaMaxCtrl = wx.TextCtrl(parent, -1,str(omegaMax.getValue()), size=(20,20))
        CCctrls.append(omegaMaxCtrl)
        box4.Add(omegaMaxCtrl, 1, wx.LEFT|wx.RIGHT, 1)

        sizer.Add(box4, 0, wx.ALIGN_LEFT|wx.ALL, 1 )        
        
        if self.cc == None or self.cc == False:
            for text in self.CCctrls:
                text.Enable(False)

# bindings creation
       
        box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box5.SetMinSize((800,80))
        grid5 = wx.FlexGridSizer( 0, 6, 0, 0 )
        grid5.SetFlexibleDirection( wx.HORIZONTAL)
        box5.Add(grid5)
        self.simulate = wx.Button(parent, -1, "Simulate", (500,200))
        #create.SetTTS("used to create an aqueous state.\n")
        
        toto.Bind(wx.EVT_BUTTON, self._simulate, self.simulate)
        box5.Add(self.simulate, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)

               
        parent.SetSizerAndFit(sizer)
        
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
        print 
# coupling algotithm        
        radio1 = filter(lambda r: r.GetValue(), self.radios1)[0]
        name = radio1.GetLabelText()
        params.getParam(parameters.Iterate_Default_Algorithm).setValue(ITERATE_ALGORITHMS_BY_LABEL[name])

# NI time parameters
        start = params.getParam( parameters.Iterate_InitialTime )
        value = self.startCtrl.GetValue()
        start.setValue(float(str(value)))
        
        dt0 = params.getParam( parameters.Iterate_InitialTimeStepSize )
        value = self.dt0Ctrl.GetValue()
        dt0.setValue(float(str(value)))
        
        simulationTime = params.getParam( parameters.Iterate_SimulationTime )
        value = self.simulationTimeCtrl.GetValue()
        simulationTime.setValue(float(str(value)))
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
            value = self.minCtrl.GetValue()
            dtmin.setValue( value )

            dtmax = params.getParam( parameters.Iterate_MaxTimeStep )
            value = self.maxCtrl.GetValue()
            dtmax.setValue(str(value))
 
            omegaMin = params.getParam( parameters.Iterate_RelaxationMinFactor )
            value = self.omegaMinCtrl.GetValue()
            omegaMin.setValue(str(value))

            omegaMax = params.getParam( parameters.Iterate_RelaxationMaxFactor )
            value = self.omegaMaxCtrl.GetValue()
            omegaMax.setValue(str(value))
        else:
            self.params.getParam(parameters.Iterate_Algorithm).setValue("NI")

        return True

    def _phaseTuple(self,string):
        #string = "Ca5(PO4)3OH + 4 H+ = H2O + 3 HPO4-2 + 5 Ca+2"
        a = string.split(" ")[1:]
        liste = []
        ind = a.index("=")
        dig = 1
        for i in a:
            if i.isdigit():
                dig = i
            elif i not in ["+","-","=",""]:
                if a.index(i) < ind:
                    print "dig",dig
                    digi = dig
                    dig = "-"+str(digi)
                    liste.append((i,dig))
                else:
                    liste.append((i,dig))
            dig = 1        
        return liste
        
    def _addenda(self,mineralPhaseName,exchangeName):
        string = ""
        if mineralPhaseName != "":
            string += ",mineralPhase = "+mineralPhaseName
            if exchangeName != "":
                string += " "+exchangeName
        else:
            if exchangeName != "":
                string += " "+exchangeName
            
        return string

    def _simulate(self,event):
        if self.params.getParam(parameters.Mode_is_structured).getValue():
            studyName = self.params.getParam(parameters.Title).getValue()
            dataBase = self.params.getParam(parameters.CurrentDatabasePath).getValue()
            darcy = self.params.getParam(parameters.DarcyVelocity_list).getValue()
            if darcy != []:
                darcyVelocity = str(darcy[0])+","+str(darcy[1])+","+str(darcy[2])
            initialTime = self.params.getParam(parameters.Iterate_InitialTime).getValue()
            finalTime = self.params.getParam(parameters.Iterate_SimulationTime).getValue()
            simulationTime = "["+str(initialTime)+","+str(finalTime)+"]"
            structuredCase = open (studyName+".py",'w')
            
            structuredCase.write("from constant import epspH\n")
            structuredCase.write("from datamodel import *\n")
            structuredCase.write("import fields\n")
            structuredCase.write("from listtools import normMaxListComparison, subtractLists\n")
            structuredCase.write("from chemicaltransport import *\n")
            structuredCase.write("from chemicaltransportmodule import *\n")

            structuredCase.write("from mt3d import Mt3d              # mt3d\n")
            structuredCase.write("from cartesianmesh import *        # Cartesian mesh\n")
            structuredCase.write("from phreeqc import *              # phreeqc\n")
            structuredCase.write("\n")
            structuredCase.write("import os\n")

            structuredCase.write("Phreeqc_file = \""+studyName+".txt\"      # bounded to Phreeqc\n")
            structuredCase.write("ProblemName  = \""+studyName+"\"          # Phreeqc file \n")
            structuredCase.write("mesh = CartesianMesh2D(\"global\",\"XY\")\n")
            nx = self.params.getParam(parameters.MeshLineInINumberOfCells).getValue()
            ny = self.params.getParam(parameters.MeshLineInJNumberOfCells).getValue()
            structuredCase.write("nx  = "+str(nx)+"\n")
            structuredCase.write("ny  = "+str(ny)+"\n")
#
# writing the mesh extension
#            
            structuredCase.write("#~~~~~~~~~~~~~~~~~~\n")
            structuredCase.write("#~ Mesh extension ~\n")
            structuredCase.write("#~~~~~~~~~~~~~~~~~~\n")
            structuredCase.write("deltax = []\n")
            xlist = self.params.getParam(parameters.Mesh_list_InI).getValue()
            ind = 0
            while xlist[ind][0] != 0:
                structuredCase.write("dx = ["+str(xlist[ind][1])+"/"+str(xlist[ind][0])+"]*"+str(xlist[ind][0])+"\n")
                structuredCase.write("deltax.extend(dx)\n")
                ind+=1
            structuredCase.write("deltay = []\n")
            ylist = self.params.getParam(parameters.Mesh_list_InJ).getValue()
            ind = 0
            while ylist[ind][0] != 0:
                structuredCase.write("dy = ["+str(ylist[ind][1])+"/"+str(ylist[ind][0])+"]*"+str(ylist[ind][0])+"\n")
                structuredCase.write("deltay.extend(dy)\n")
                ind+=1
            structuredCase.write("mesh.setdAxis(\"X\",deltax)\n")
            structuredCase.write("mesh.setdAxis(\"Y\",deltay)\n")
            zone_list = self.params.getParam(parameters.Zones_list).getValue()
            zone_Material_AqueousState_list = self.params.getParam(parameters.Zone_Material_AqueousState_list).getValue()
            ind = 0
            for zone in zone_list:
                structuredCase.write(str(zone)+str(ind)+"Body = CartesianMesh2D(\""+str(zone)+"\", \"XY\")\n")
                imin = zone_Material_AqueousState_list[ind][2]
                imax = zone_Material_AqueousState_list[ind][3]
                jmin = zone_Material_AqueousState_list[ind][4]
                jmax = zone_Material_AqueousState_list[ind][5]
                string = str(zone)+str(ind)
                structuredCase.write(string+"Body.setZone(\""+str(zone)+"\",index_min = Index2D ("+str(imin)+","+str(jmin)+\
                "), index_max = Index2D ("+str(imax)+","+str(jmax)+"))\n")
                ind+=1
                
            structuredCase.write("#~~~~~~~~~~~~~\n")
            structuredCase.write("#~ Materials ~\n")
            structuredCase.write("#~~~~~~~~~~~~~\n")
            
            materials = self.params.getParamValue(parameters.CUSTOM_MATERIAL_DB).getMaterials()
            for toto in materials.keys():
                materialName = str(toto)+"Material"
                longDisp =  str(materials[toto]["LongitudinalDispersivity"])
                transDisp = str(materials[toto]["TransverseDispersivity"])
                structuredCase.write(materialName+" = Material (name = \""+str(toto)+"\",")
                structuredCase.write("effectiveDiffusion = EffectiveDiffusion ("+str(materials[toto]["EffectiveDiffusion"])+",unit=\"m**2/s\"),\\")
                structuredCase.write("\npermeability = Permeability(value = "+str(materials[toto]["KxPermeability"])+"),\\")
                structuredCase.write("\nporosity = Porosity(value = "+str(materials[toto]["EffectivePorosity"])+"),\\")
                structuredCase.write("\nkinematicDispersion = KinematicDispersion ("+longDisp+","+transDisp+"))\n")
                
#            print materials

            structuredCase.write("\n#~~~~~~~~~~~\n")
            structuredCase.write("#~ Regions ~\n")
            structuredCase.write("#~~~~~~~~~~~\n")
             
            ind = 0
            regionList = "["
            for zone in zone_list:
                if ind!=0: regionList+=","
                materialName = str(zone_Material_AqueousState_list[ind][0])+"Material"
                structuredCase.write(str(zone)+str(ind)+"Region = Region(support="+str(zone)+str(ind)+"Body, material= "+materialName+")\n")
                regionList+=str(zone)+str(ind)+"Region"
                ind+=1
            regionList+="]"
#
#
            _chemical(self.params,structuredCase)
#
#
#
#chemical_state_quartz = ChemicalState ("column", AqueousSolution_column, columnMineralPhase)
#
            structuredCase.write("#~~~~~~~~~~~~~~~~~~~~\n")
            structuredCase.write("# Initial condition ~\n")
            structuredCase.write("#~~~~~~~~~~~~~~~~~~~~\n")
            initialConditionList = self.params.getParam(parameters.InitialConditions_list).getValue()
            print "initialConditionList: ",initialConditionList
            boundaryConditionList = self.params.getParam(parameters.BoundaryConditions_list).getValue()
            iCLS = "["
            for iC in initialConditionList:
                iCName = str(iC)+"IC"
                iCLS+=iCName+","
                iCParameters = zone_Material_AqueousState_list[zone_list.index(iC)]
                materialName = str(iCParameters[0]) + "Material"
                aqueousStateName = str(iCParameters[1])+"ChemicalState"
                structuredCase.write(iCName+" = InitialCondition (body  = "+str(iC)+str(zone_list.index(iC))+"Body, value = "+aqueousStateName+")\n")
            iCLS = iCLS[0:len(iCLS)-1]
            iCLS += "]"
            structuredCase.write("#~~~~~~~~~~~~~~~~~~~~~\n")
            structuredCase.write("# Boundary condition ~\n")
            structuredCase.write("#~~~~~~~~~~~~~~~~~~~~~\n")
            bCLS = "["
            for iC in boundaryConditionList:
                iCName = str(iC)+"BC"
                bCLS+=iCName+","
                iCParameters = zone_Material_AqueousState_list[zone_list.index(iC)]
                materialName = str(iCParameters[0])+"Material"
                aqueousStateName = str(iCParameters[1])+"ChemicalState"
                structuredCase.write(iCName+" = BoundaryCondition (boundary = "+str(iC)+str(zone_list.index(iC))+"Body, btype=\"Dirichlet\", value = "+aqueousStateName+")\n")
                
#bIC = BoundaryCondition (boundary = b0Zone, btype='Dirichlet', value = sodaChemicalState)
                
            bCLS = bCLS[0:len(bCLS)-1]
            bCLS += "]"
            structuredCase.write("#~~~~~~~~~~~~~~~~~~~\n")
            structuredCase.write("# Expected outputs ~\n")
            structuredCase.write("#~~~~~~~~~~~~~~~~~~~\n")
            outputList = self.params.getParam(parameters.ExpectedOutputs_list).getValue()
#            print "outputList",outputList
            if outputList != []:
                string = "expectedOutputs = ["
                for out in outputList:
                    if str(out) == "pH":
                        string+="ExpectedOutput(\"pH\",format=\"table\",name=\"pH_output\"),\n"
                    else:
                        string+="ExpectedOutput(\"Concentration\",\""+out+"\",format=\"table\",name=\""+out+"Output\"),\n"
                string = string[0:-2]+"]\n"
                structuredCase.write(string)
            else:        
                structuredCase.write("expectedOutputs = []\n")
                
            structuredCase.write("#~~~~~~~~~\n")
            structuredCase.write("# Module ~\n")
            structuredCase.write("#~~~~~~~~~\n")
            
            structuredCase.write("module = ChemicalTransportModule()\n")

            structuredCase.write("problem  = ChemicalTransportProblem(name               = \""+\
            str(studyName)+"\",\\")
            structuredCase.write("\n                                    regions            = "+regionList+",\\\n")
            structuredCase.write("                                    initialConditions  = "+iCLS+",\\\n")
            structuredCase.write("                                    boundaryConditions = "+bCLS+",\\\n")
            structuredCase.write("                                    calculationTimes   = "+simulationTime+",\\\n")
            structuredCase.write("                                    sources            = None,\\\n")
            if darcy == []:
                structuredCase.write("                                    darcyVelocity      = None,\\\n")
            else:
                structuredCase.write("                                    darcyVelocity      = Velocity(Vector(["+darcyVelocity+"])),\\\n")
            #
            # The database should be placed in the Phreeqc_dat directory
            #
            dataBase = os.path.split(dataBase)[-1]
            structuredCase.write("                                    chemistryDB        = \""+dataBase+"\",\\\n")
            structuredCase.write("                                    speciesBaseAddenda = speciesAddenda,\\\n")
            structuredCase.write("                                    kineticLaws        = None,\\\n")
            structuredCase.write("                                    activityLaw        = None,\\\n")
            structuredCase.write("                                    outputs            = expectedOutputs)\n")

            algorithm = self.params.getParam(parameters.Iterate_Algorithm).getValue()
            structuredCase.write("module.setData (problem, trace = 0, mesh = mesh, algorithm=\""+algorithm+"\")\n")
            structuredCase.write("\nmodule.setComponent(\"mt3d\",\"phreeqc\")\n") 
            scheme = self.params.getParam(parameters.Mt3d_advection).getValue()
            structuredCase.write("module.setTransportParameters(\""+scheme+"\")\n")
            preconditionner = self.params.getParam(parameters.Mt3d_ConjugateGradientPreconditioner).getValue()
            epsPred = str(self.params.getParam(parameters.Mt3d_cclose).getValue())
            structuredCase.write("module.setTransportParameters(\""+preconditionner+"\","+epsPred+")\n")

            if str(algorithm) == "NI":
                minStepSize = self.params.getParam(parameters.Iterate_InitialTimeStepSize).getValue()
                maxStepSize = self.params.getParam(parameters.Iterate_InitialTimeStepSize).getValue()
            else:
                minStepSize = self.params.getParam(parameters.Iterate_MinTimeStep).getValue()
                maxStepSize = self.params.getParam(parameters.Iterate_MaxTimeStep).getValue()

            structuredCase.write("module.setCouplingParameter(initialTimeStep        = "+\
            str(self.params.getParam(parameters.Iterate_InitialTimeStepSize).getValue())+","+\
            "\n                            minTimeStep            = "+\
            str(minStepSize)+","\
            "\n                            maxTimeStep            = "+\
            str(maxStepSize)+","\
            "\n                            couplingPrecision      = "+\
            str(self.params.getParam(parameters.Iterate_CouplingPrecision).getValue())+","\
            "\n                            optimalIterationNumber = "+\
            str(self.params.getParam(parameters.Iterate_PicardTargetNumber).getValue())+","\
            "\n                            maxIterationNumber     = "+\
            str(self.params.getParam(parameters.Iterate_PicardMaxOfIterations).getValue())+","\
            "\n                            decreaTimeStepCoef     = "+\
            str(self.params.getParam(parameters.Iterate_RelaxationMinFactor).getValue())+","\
            "\n                            increaTimeStepCoef     = "+\
            str(self.params.getParam(parameters.Iterate_RelaxationMaxFactor).getValue())+")")
            if self.params.getParam(parameters.PostprocessingContours_AqueousComponentsToPlot_list).getValue() != []:
                structuredCase.write("\n#~~~~~~~~~~~\n")
                structuredCase.write("# Contours ~\n")
                structuredCase.write("#~~~~~~~~~~~\n")
                string = "module.setVtkOutputsParameters(["
                for species in self.params.getParam(parameters.PostprocessingContours_AqueousComponentsToPlot_list).getValue():
                    string += "\""+str(species)+"\","
                string = string[0:len(string)-1]+"],"
                string += "\""+str(self.params.getParam(parameters.PostprocessingContours_Parameters_list).getValue()[1])+"\","
                string += str(self.params.getParam(parameters.PostprocessingContours_Parameters_list).getValue()[0])+")\n"
                structuredCase.write(string)
#           module.setVtkOutputsParameters(["Na"],"days",2)
            structuredCase.write("\nmodule.run()\n")
            if string!= "":
                structuredCase.write("#~~~~~~~~~~~~~~~~~~\n")
                structuredCase.write("# Post processing ~\n")
                structuredCase.write("#~~~~~~~~~~~~~~~~~~\n")
                string = self.params.getParam(parameters.PyOutputHandler).getValue()
                structuredCase.write(string)
            lenString = len("        End of the ")+len(studyName)+len(" case ~")
            en = "~"*lenString   
            structuredCase.write("\nprint \""+en+"\"\n")
            structuredCase.write("print \"        End of the "+studyName+" case ~\"") 
            structuredCase.write("\nprint \""+en+"\"\n")
            structuredCase.write("\nmodule.end()\n")
            
            structuredCase.close()
            #
            # Running the generated file in a PyShell
            #
            from wx import py
            import wx.py as py
            #namespace = { 'wx'    : wx,
            #              'app'   : wx.GetApp(),
            #              'frame' : self,
            #              }
            #DEFAULT_SHELL_WINDOW_SIZE = (640,480)
            #self.shell = py.shell.ShellFrame(None, title = " interactive launch browser", locals=namespace)
            #self.shell.SetSize( DEFAULT_SHELL_WINDOW_SIZE )
            #self.shell.Show()
            os.system("python "+studyName+".py")
            #toto  = Myne("Coupling browser",studyName+".py")
        else:  # case of an unstructured file. In that case, we should restructure that if/elif statement
            print("noch zu machen")
        return True
        
def _strHandlung(string):
     string = string.replace("+","p")
     string = string.replace("-","m")
     return string

