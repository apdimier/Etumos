import wx
import os
import subprocess
import sys

from geoi.actions.params_action import ParamsAction
from geoi import parameters

description = """ 
       \nUsed to set the Darcy velocity Field through\nsteady components or Head boundary conditions
       """
HELP = """
       <html><body>
       <p>Used to define the components of a <b>Darcy</b> velocity;<br><br>
<li type=1><div align="two options:"> 
<blockquote>- a three dimensional constant velocity field in time and space can be defined.</blockquote>
<blockquote>
 - a stationary Darcy velocity field depending on head and on boundaries<br>&nbsp;&nbsp; can also be defined.</blockquote><blockquote>
 - otherwise, only diffusion is relevant.</blockquote></div></li>
<br>
       </body></html>

       """
class DarcyVelocityComponentsElmer(ParamsAction):
    """
    Used to set the Darcy velocity components
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Darcy Velocity",description  =description,help=HELP)
        
    def _createInterface(self, parent, params):
#velocity components
        self.params = params
        self.checkButton_ctrls = []

        toto = self.GetDialogPanel()
        wx.CheckBox.SetTTS = wx.CheckBox.SetToolTipString
        sizer = wx.BoxSizer( wx.VERTICAL )
        
        
        
        self.diffusionOnly = diffusionOnly = wx.CheckBox( parent, -1, "diffusion only",style = 0)
        self.checkButton_ctrls.append(diffusionOnly)
        diffusionOnly.SetTTS("used to have only diffusion, ie no flow  field")
        sizer.Add(diffusionOnly, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        if params.getParam( parameters.DarcyVelocityStaticElmer).getValue()=="False" and\
           params.getParam( parameters.DarcyVelocityHeadElmer).getValue()  =="False" and\
           params.getParam( parameters.ReadDarcyVelocity).getValue()       =="False":
            self.diffusionOnly.SetValue(True)
        else :
            self.diffusionOnly.SetValue(False)
        self.diffusionOnly.Enable(True)
        toto.Bind(wx.EVT_CHECKBOX, self._selectControl, diffusionOnly)
        
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Constant velocity field components" ) , wx.HORIZONTAL)
        box3.SetMinSize((300,50))
        grid3 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid3.SetFlexibleDirection( wx.HORIZONTAL)

        velocity = params.getParam( parameters.DarcyVelocityStatic_list_elmer)
        
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
        self.checkButton_ctrls.append(DarcyControl)
        DarcyControl.SetTTS("used to control a constant Darcy Velocity,\n default being a zero normed one ")
        box3.Add(DarcyControl, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        toto.Bind(wx.EVT_CHECKBOX, self._darcyControl, DarcyControl)
         
        self.DarcyControl.SetValue(eval(params.getParam( parameters.DarcyVelocityStaticElmer).getValue()))
        self.DarcyControl.Enable(True) 
               
        sizer.Add( box3, 0, wx.ALIGN_LEFT|wx.ALL, 5 )  
        
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        box6 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Darcy velocity with head" ) , wx.VERTICAL)
        box6.SetMinSize((620,200))
        grid6 = wx.FlexGridSizer( 3, 1, 0, 0 )
        grid6.SetFlexibleDirection( wx.VERTICAL)
        
        self.DarcyControl2 = DarcyControl2 = wx.CheckBox( parent, -1, "constant velocity field",style = 0)
        self.checkButton_ctrls.append(DarcyControl2)
        DarcyControl2.SetTTS("used to control a Darcy Velocity defined by heads,\n default being a zero normed one ")
        box6.Add(DarcyControl2, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        toto.Bind(wx.EVT_CHECKBOX, self._darcyControl2, DarcyControl2)
        
        
        self.DarcyControl2.SetValue(eval(params.getParam( parameters.DarcyVelocityHeadElmer).getValue()))
        self.DarcyControl2.Enable(True)
        
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "New zone" ) , wx.HORIZONTAL)
        box4.SetMinSize((200,50))
        grid4 = wx.FlexGridSizer( 0, 3, 0, 0 )
        grid4.SetFlexibleDirection( wx.HORIZONTAL)
        
        label1 = wx.StaticText(parent, -1, "Set\nZones:")
        label1.SetHelpText("This is the help text for the label")
        box4.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        
        zones_not_used = []
        zones_not_used2 = params.getParam( parameters.Zone_BCKind_list).getValue()
        BCHList = params.getParam(parameters.Boundary_Condition_Head).getValue()
        for zones in zones_not_used2 :
            absent = True
            for i in range(len(BCHList)) :
                if zones == BCHList[i][0] :
                    absent = False
                   
            if absent :
                zones_not_used.append(zones)     

        self.zoneCtrl = zoneCtrl = wx.ComboBox(parent, -1, "",\
        (200, 20), (200, -1), zones_not_used, wx.CB_DROPDOWN)
        zoneCtrl.SetHelpText("Here's some help text for field #1")

        
        box4.Add(zoneCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        label2 = wx.StaticText(parent, -1, "Head Value:")
        label2.SetHelpText("This is the help text for the label")
        box4.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.HeadValueCtrl = HeadValueCtrl = wx.TextCtrl(parent, -1, "", size=(60,-1))
        HeadValueCtrl.SetHelpText("Here's some help text for field #1")
        
        
        box4.Add(HeadValueCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
               
        box6.Add( box4, 0, wx.TOP|wx.ALL, 5 )  
        
        #~~~~~~~~~~~~~~~~~~~~~~~~
        
        box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Zones already defined" ) , wx.HORIZONTAL)
        box5.SetMinSize((620,50))
        grid5 = wx.FlexGridSizer( 0, 3, 0, 0 )
        grid5.SetFlexibleDirection( wx.HORIZONTAL)

        
        label1 = wx.StaticText(parent, -1, "Zones:")
        label1.SetHelpText("This is the help text for the label")
        box5.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        zones_already_defined = []
        for zones in params.getParam(parameters.Boundary_Condition_Head).getValue() :
            zones_already_defined.append(zones[0])

        self.zoneCtrlAlreadyD = zoneCtrlAlreadyD = wx.ComboBox(parent, -1, "",\
        (180, 20), (180, -1), zones_already_defined, wx.CB_DROPDOWN)
        zoneCtrlAlreadyD.SetHelpText("Here's some help text for field #1")
        
        toto.Bind(wx.EVT_COMBOBOX, self._alreadyDZoneHead, zoneCtrlAlreadyD)
        
        box5.Add(zoneCtrlAlreadyD, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        label2 = wx.StaticText(parent, -1, "Head Value:")
        label2.SetHelpText("This is the help text for the label")
        box5.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.HeadValueCtrlAlreadyD = HeadValueCtrlAlreadyD = wx.TextCtrl(parent, -1, "", (60,-1), (200, -1))
        HeadValueCtrlAlreadyD.SetHelpText("Here's some help text for field #1")
        
        
        box5.Add(HeadValueCtrlAlreadyD, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
        
        label3 = wx.StaticText(parent, -1, "Delete")
        label3.SetHelpText("This is the help text for the label")
        box5.Add(label3, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.delete = delete = wx.CheckBox( parent, -1, "",style = 0)
        delete.SetTTS("used to delete a head zone ")
        box5.Add(delete, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        toto.Bind(wx.EVT_CHECKBOX, self._delete, delete)

               
        box6.Add( box5, 0, wx.BOTTOM|wx.ALL, 5 )  
        sizer.Add( box6, 0, wx.ALIGN_LEFT|wx.ALL, 5 ) 
        
        
        self.apply = wx.Button(parent, -1, "Apply", (380,50))
        
        toto.Bind(wx.EVT_BUTTON, self._applyZone, self.apply)
        sizer.Add(self.apply, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALL, 10)
        
        
        
        
        
        if DarcyControl.GetValue()==False:
            self.vxCtrl.Enable(False)
            self.vyCtrl.Enable(False)
            self.vzCtrl.Enable(False)
            if DarcyControl2.GetValue()==True:
                self.DarcyControl.Enable(False)
         
        if DarcyControl2.GetValue()==False:
            self.zoneCtrl.Enable(False)
            self.HeadValueCtrl.Enable(False)
            self.zoneCtrlAlreadyD.Enable(False)
            self.HeadValueCtrlAlreadyD.Enable(False)
            self.delete.Enable(False)
                
        self.readVelocity = readVelocity = wx.CheckBox( parent, -1, "Read Velocity",style = 0)
        self.checkButton_ctrls.append(readVelocity)
        readVelocity.SetTTS("used to read the velocity un a file called HeVel.ep")
        sizer.Add(readVelocity, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        self.readVelocity.SetValue(eval(self.params.getParam(parameters.ReadDarcyVelocity).getValue()))
        self.readVelocity.Enable(True)
        toto.Bind(wx.EVT_CHECKBOX, self._selectControl, readVelocity)
                
        parent.SetSizerAndFit(sizer)

    def _selectControl( self, event ):
        button_selected = event.GetEventObject()
        ind = 0
        for checkButton in self.checkButton_ctrls: 
            if checkButton is button_selected:
                if checkButton.GetValue() == True:
                    ind=1
                else:
                    checkButton.SetValue(False)
            else:
                checkButton.SetValue(False)
        if ind == 0 :
            self.diffusionOnly.SetValue(True)

        self.vxCtrl.Enable(False)
        self.vyCtrl.Enable(False)
        self.vzCtrl.Enable(False)
        self.zoneCtrl.Enable(False)
        self.HeadValueCtrl.Enable(False)
        self.zoneCtrlAlreadyD.Enable(False)
        self.HeadValueCtrlAlreadyD.Enable(False)
        self.delete.SetValue(False)
        
    def _darcyControl(self, event):
        self._selectControl(event)
        
        if event.IsChecked()==True:
            self.vxCtrl.Enable(True)
            self.vyCtrl.Enable(True)
            self.vzCtrl.Enable(True)

        return True    
        
    def _darcyControl2(self, event):
        self._selectControl(event)
        
        if event.IsChecked()==True:
            self.zoneCtrl.Enable(True)
            self.HeadValueCtrl.Enable(True)
            self.zoneCtrlAlreadyD.Enable(True)
            self.HeadValueCtrlAlreadyD.Enable(True)
            self.delete.SetValue(True)

        return True
        
    def _delete(self, event) :
        if event.IsChecked()==True:
            self.zoneCtrl.Enable(False)
            self.HeadValueCtrl.Enable(False)
        else :
            self.zoneCtrl.Enable(True)
            self.HeadValueCtrl.Enable(True)
    
    def _alreadyDZoneHead(self, event) :
        zoneName = self.zoneCtrlAlreadyD.GetValue()
        
        for zones in self.params.getParam(parameters.Boundary_Condition_Head).getValue() :
            if zones[0] == zoneName :
                value = zones[1]
        self.HeadValueCtrlAlreadyD.SetValue(str(value))
      
      
    def _applyZone(self, event):
        self._applyZoneValidation(event)
        self._calculVelocity(event)
        return None
        
    def _applyZoneValidation(self, event):
        gesch = []
        velocity = self.params.getParam( parameters.DarcyVelocityStatic_list_elmer)
        if self.DarcyControl.GetValue() == True:    # constant velocity    
            value = self.vxCtrl.GetValue()
            gesch.append(value)
        
            value = self.vyCtrl.GetValue()
            gesch.append(value)
        
            value = self.vzCtrl.GetValue()
            gesch.append(value)
        
            velocity.setValue( gesch )
            
            self.params.getParam( parameters.DarcyVelocityStaticElmer).setValue("True")
            self.params.getParam( parameters.DarcyVelocityHeadElmer).setValue("False")
        elif self.DarcyControl2.GetValue() == True:                                 # with hydraulic heads
            velocity.setValue( gesch )
            
            if self.delete.IsChecked() == True :                                    # delete an hydraulic head
                headCondition = self.params.getParam(parameters.Boundary_Condition_Head).getValue()    
                i=0   
                for zones in headCondition : 
                    if zones[0] ==  self.zoneCtrlAlreadyD.GetValue() :
                        j=i
                    else :
                        i += 1
                zoneToDelete = headCondition[j]
                headCondition.remove(zoneToDelete)
                self.params.getParam(parameters.Boundary_Condition_Head).setValue(headCondition) 
                toRemove = self.zoneCtrlAlreadyD.GetValue()
                index = self.zoneCtrlAlreadyD.GetSelection()
                self.zoneCtrlAlreadyD.Delete(index)
                self.zoneCtrl.Append(toRemove) 
                self.zoneCtrlAlreadyD.SetValue("") 
                self.HeadValueCtrlAlreadyD.SetValue("")      
            else : # create an hydraulic
                if self.zoneCtrl.GetValue() != "" :
                    headConditionNew = [self.zoneCtrl.GetValue(),int(self.HeadValueCtrl.GetValue())]
                    headCondition = self.params.getParam(parameters.Boundary_Condition_Head).getValue()  
                    headCondition.append(headConditionNew)    
                    self.params.getParam(parameters.Boundary_Condition_Head).setValue(headCondition)
                    self.zoneCtrlAlreadyD.Append(self.zoneCtrl.GetValue())
                    index = self.zoneCtrl.GetSelection()
                    self.zoneCtrl.Delete(index)
                    self.zoneCtrl.SetValue("")
                    self.HeadValueCtrl.SetValue("")
            self.params.getParam( parameters.DarcyVelocityStaticElmer).setValue("False")
            self.params.getParam( parameters.DarcyVelocityHeadElmer).setValue("True")
            
        else :
            self.params.getParam( parameters.DarcyVelocityStaticElmer).setValue("False")
            self.params.getParam( parameters.DarcyVelocityHeadElmer).setValue("False")
            
        return None
    
    def _calculVelocity(self, event) :
        if self.params.getParam( parameters.DarcyVelocityHeadElmer).getValue() == "True" :
        
            nameFile = self.params.getParam(parameters.Title).getValue()
            params=self.params 
            
            directorie = params.getParam(parameters.ResultDirectory).getValue()
            
            meshFileName = params.getParam(parameters.Gmsh_Name_File2).getValue()
            meshFileName2 = meshFileName
            while "/" in meshFileName2 :
                i=0
                while meshFileName2[i] != "/" :
             	    i+=1
                meshFileName2=meshFileName2[i+1:len(meshFileName2)]	
            
            if meshFileName == directorie +"/"+\
                nameFile + ".msh" :
                    pass
            else :    
                nameFileMesh = directorie +"/" +\
                nameFile + ".msh" 
                f2 = open(nameFileMesh,"w")
                f1 = open(meshFileName,"r")
                f2.write(f1.read())
                f2.close()
                f1.close()
                meshFileName = nameFileMesh
           
            os.chdir(directorie)
            
            f0=open(directorie + "/" + nameFile + "Velocity.py","w") 
            
            f0.write("import os\n")
            f0.write("from mesh import *\n")
            f0.write("from datamodel import *\n")
            f0.write("from math import *\n")
            f0.write("from hydraulicmodule import *\n")
            f0.write("import sys\n")
            f0.write("from time import time\n")
            f0.write("from material import *\n")
            f0.write("from exceptions import Exception\n")
            f0.write("from hydraulicproblem import *\n\n")
            
            f0.write("ProblemName  = \"" + nameFile + "\" + \"testHydraulic\"\n")
            
            f0.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
            f0.write("#   Mesh definition\n")
            f0.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
            
            f0.write("mesh = MeshReader(\"" + nameFile + ".msh\")\n")
            
            zone_list = self.params.getParam(parameters.Zones_list).getValue()
            i=0
            for zone in zone_list:
         	    f0.write(str(zone)+str(i)+"Body = mesh.getBody(\""+str(zone)+"\")\n")
         	    f0.write(str(zone)+str(i)+"Body.getNodesNumber()\n")
         	    i += 1
         			
            f0.write("numberOfVertices = mesh._getNumberOfVertices()\n\n")
            
            f0.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
            f0.write("#   Material\n")
            f0.write("#~~~~~~~~~~~~~~~~~~~~~~\n")
	
            materials = self.params.getParamValue(parameters.CUSTOM_MATERIAL_DB).getMaterials()
            for ind in materials.keys():
                materialName = str(ind)+"Material"
                longDisp =  str(materials[ind]["LongitudinalDispersivity"])
                transDisp = str(materials[ind]["TransverseDispersivity"])
                f0.write(materialName+" = Material (name = \""+str(ind)+"\",")
                f0.write("effectiveDiffusion = EffectiveDiffusion ("+str(materials[ind]["EffectiveDiffusion"])+",unit=\"m**2/s\"),\\")
                f0.write("\npermeability = Permeability(value = "+str(materials[ind]["KxPermeability"])+"),\\")
                f0.write("\nporosity = Porosity(value = "+str(materials[ind]["EffectivePorosity"])+"),\\")
                f0.write("\nkinematicDispersion = KinematicDispersion ("+longDisp+","+transDisp+"),\\")
                f0.write("\nhydraulicconductivity=HydraulicConductivity(value = " + str(materials[ind]["HydraulicConductivity"]) + "))\\\n")
            
            f0.write("\n#~~~~~~~~~~~\n")
            f0.write("#~ Regions ~\n")
            f0.write("#~~~~~~~~~~~\n")
            zone_list = self.params.getParam(parameters.Zones_list).getValue()
            print zone_list
            zone_Material_AqueousState_list = self.params.getParam(parameters.Zone_Material_AqueousState_list).getValue() 
            ind = 0
            regionList = "["
            for zone in zone_list:
	            if ind!=0: 
	                regionList+=","
	            materialName = str(zone_Material_AqueousState_list[ind][0])+"Material"
	            f0.write(str(zone)+str(ind)+"Region = Region(support="+str(zone)+str(ind)+"Body, material= "+materialName+")\n")
	            regionList+=str(zone)+str(ind)+"Region"
	            ind+=1
            regionList+="]" 
          
            f0.write("\n#~~~~~~~~~~~\n")
            f0.write("#~ Head Condition ~\n")
            f0.write("#~~~~~~~~~~~\n")      
          
            BoundaryConditionHead = self.params.getParam(parameters.Boundary_Condition_Head).getValue()
            
            j=0
            l=0
            m=0
            for zones in zone_list :
                absent = True
                for i in range(len(BoundaryConditionHead)) :
                    if zones == BoundaryConditionHead[i][0] :
                        absent = False
                        k=i       
                if absent :
                    f0.write("InitHead" + str(l) + " = InitialCondition(" + zones + str(j) + "Region" +\
                    ", Head(0.,\"m\"))\n")
                    l += 1
                else :
                    f0.write("BCHead" + str(m) + " = BoundaryCondition(" + str(BoundaryConditionHead[k][0]) + str(j) + "Region" +\
                    ", \"Dirichlet\", Head(" + str(BoundaryConditionHead[k][1]) + ", \"m\"))\n")
                    m += 1
                j += 1     

                    
            f0.write("\n")
            
            f0.write("#\n")
            f0.write("# Problem definition\n")
            f0.write("#\n\n")
            
            f0.write("problem = HydraulicProblem( name                     = \"" + nameFile + "SteadyHydraulic\",\\\n")
            f0.write("                            saturation               = \"saturated\",\\\n")
            
            f0.write("                            regions                  = [")
            for i in range(len(zone_list)-1) :
                f0.write(zone_list[i] + str(i) + "Region, ")
            f0.write(zone_list[len(zone_list)-1] + str(len(zone_list)-1) + "Region],\\\n")
                        
            f0.write("                            boundaryConditions       = [")
            for i in range(len(BoundaryConditionHead)-1) :
                f0.write("BCHead" + str(i) + ", ")
            f0.write("BCHead" + str(len(BoundaryConditionHead)-1) + "],\\\n")
            
            f0.write("                            initialConditions        = [")
            for i in range(len(zone_list)-len(BoundaryConditionHead)-1) :
                f0.write("InitHead" + str(i) + ", ")
            f0.write("InitHead" + str(len(zone_list)-len(BoundaryConditionHead)-1) + "],\\\n") 
            f0.write("                            source                   = None,\\\n")
            f0.write("                            outputs                  = [])\n\n")
            
            f0.write("# Module initialisation\n")
            f0.write("module = HydraulicModule()\n")
            f0.write("module.setData(problem,mesh = mesh)\n")
            f0.write("module.setComponent(\"elmer\")\n\n")

           
            f0.write("module.setParameter                   (linearSystemSolver               = \"iterative\",\\\n")
            f0.write("                                       linearSystemIterativeMethod      = \"BiCGStab\",\\\n")
            f0.write("                                       linearSystemMaxIterations        = 100,\\\n")
            f0.write("                                       linearSystemConvergenceTolerance = 1.e-15,\\\n")
            f0.write("                                       linearSystemPreconditioning      = \"ILU0\",\\\n")
            f0.write("                                       steadyStateConvergenceTolerance  = 1.0e-08,\\\n")
            f0.write("                                       stabilize                        = True")
           
            f0.write("                                      )\n") 
            f0.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            f0.write("module.run()\n")
            f0.write("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")

            f0.write("points, charge, velocity = module.getOutput(\"velocity\")\n")
            f0.write("module.writeVelocityPlot()\n\n")


            f0.flush()
            f0.close()
            while f0.closed == False:
                pass   
            
            os.chdir(directorie)
            
            
            try:
                retcode = subprocess.Popen("rm -f commandfile.eg", shell = True)
                if retcode < 0:
                    print >>sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child returned", retcode
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e

            try:
                retcode = subprocess.Popen("rm -rf " + nameFile , shell = True)
                if retcode < 0:
                    print >>sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child returned", retcode
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e    
                        
            os.chdir(directorie)
            os.system("python  " +nameFile+ "Velocity.py")
            
        else :
            os.chdir(directorie)
            try:
                retcode = subprocess.Popen("rm -f commandfile.eg", shell = True)
                if retcode < 0:
                    print >>sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child returned", retcode
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e

            try:
                retcode = subprocess.Popen("rm -rf " + nameFile , shell = True)
                if retcode < 0:
                    print >>sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child returned", retcode
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e    
                        
            os.chdir(directorie)
            os.system("python  " +nameFile+ "Velocity.py")

    
        
    def _onOk(self, params):
        self._applyZoneValidation(self, event)
        self.params.getParam(parameters.ReadDarcyVelocity).setValue(str(self.readVelocity.GetValue()))
        return True
      
        
        
    def _onOk_old(self, params):
#
# parameters
#
        gesch = []
        velocity = params.getParam( parameters.DarcyVelocityStatic_list_elmer)
        if self.DarcyControl.GetValue() == True:        # case static velocity
            value = self.vxCtrl.GetValue()
            gesch.append(value)
        
            value = self.vyCtrl.GetValue()
            gesch.append(value)
        
            value = self.vzCtrl.GetValue()
            gesch.append(value)
        
            velocity.setValue( gesch )
            
            self.params.getParam( parameters.DarcyVelocityStaticElmer).setValue("True")
            self.params.getParam( parameters.DarcyVelocityHeadElmer).setValue("False")
        elif self.DarcyControl2.GetValue() == True:     # case head velocity
            velocity.setValue( gesch )
            
            if self.delete.IsChecked() == True :
                headCondition = params.getParam(parameters.Boundary_Condition_Head).getValue()    
                i=0   
                for zones in headCondition : 
                    if zones[0] ==  self.zoneCtrlAlreadyD.GetValue() :
                        j=i
                    else :
                        i += 1
                zoneToDelete = headCondition[j]
                headCondition.remove(zoneToDelete)
                params.getParam(parameters.Boundary_Condition_Head).setValue(headCondition)          
            else :
                if self.zoneCtrl.GetValue() != "" :
                    headConditionNew = [self.zoneCtrl.GetValue(),int(self.HeadValueCtrl.GetValue())]
                    headCondition = params.getParam(parameters.Boundary_Condition_Head).getValue()  
                    headCondition.append(headConditionNew)    
                    params.getParam(parameters.Boundary_Condition_Head).setValue(headCondition)
            
            self.params.getParam( parameters.DarcyVelocityStaticElmer).setValue("False")
            self.params.getParam( parameters.DarcyVelocityHeadElmer).setValue("True")
            
        else :                                          #case no velocity
            self.params.getParam( parameters.DarcyVelocityStaticElmer).setValue("False")
            self.params.getParam( parameters.DarcyVelocityHeadElmer).setValue("False")
            
        return True
        

