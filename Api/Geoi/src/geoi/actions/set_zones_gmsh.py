import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

ACTION_BY_LABEL = ['Define a new zone','Modify or delete an existing one']

description =\
       """ 
       To define the aqueous solution distribution over the meshed physical domain 
       """
HELP = """
       <html><body>
       The different <b>Aqueous Solutions</b> are distributed over the <b>meshed physical domain</b><br>
       associating aqueous solutions and cells. At the end, each cell is associated to an unique aqueous solution.
       <br>
       First, you have to choose the kind o association you want to conduct, <b>initial condition</b> or <b>boundary condition
       </b>.<br>Then, you choose through combo boxes the <b>material</b> and the <b>aqueous state</b> you want to associate.
       <br>At least, you choose the extension of the domain on which these conditions apply.
       </body></html>
       """
class SetZonesGmsh(ParamsAction):
    """
    Enables the association of materials and aqueous states over the domain
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Set Zones",description  =description,help=HELP)
        self.radios = None
        self.choice = None
        self.cc = None
        self.params_mgr=params_mgr
        self.zoneListAlreadyCreated = []

    def _createInterface(self, parent, params):
        
        sizer = wx.BoxSizer( wx.VERTICAL )

# set zones
   
        actionLabels = ACTION_BY_LABEL
   
        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL )
        box1.SetMinSize((600,40))
        grid1 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid1.SetFlexibleDirection( wx.HORIZONTAL)
        wx.StaticText.SetTTS = wx.StaticText.SetToolTipString
        wx.TextCtrl.SetTTS = wx.TextCtrl.SetToolTipString
        radios1 = []
        self.parent = parent
        self.params = params
        self.zoneCtrl = zoneCtrl = []
        self.Zones_list = Zones_list = params.getParamValue(parameters.Zones_list)
        self.Zone_BCKind_list = Zone_BCKind_list = params.getParamValue(parameters.Zone_BCKind_list)
        self.InitialConditions_list = InitialConditions_list = params.getParamValue(parameters.InitialConditions_list)
        self.Zone_Material_AqueousState_list = Zone_Material_AqueousState_list = params.getParamValue(parameters.Zone_Material_AqueousState_list)
        
        Zone_Material_AqueousState_list
        
        self.CCctrls = CCctrls =[]
        self.materialList = materialList = []
        self.AqueousStateList = AqueousStateList = []
        self.zoneListAlreadyCreated = self.params.getParam(parameters.Zones_list).getValue()      
        
        toto = self.GetDialogPanel()


#defining new zone names

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box1.SetMinSize((600,30))

        start = params.getParam( parameters.Iterate_InitialTime )
        dt0 = params.getParam( parameters.Iterate_InitialTimeStepSize )
        simulationTime = params.getParam( parameters.Iterate_SimulationTime )
        
        
        self.Zones_list_mesh = Zones_list_mesh = []
        try :
            meshName = self.params.getParam(parameters.Gmsh_Name_File2).getValue()
            f1 = open(meshName,"r")
            for i in range(5) :
                a = f1.readline()
            number = int(a)
            for i in range(number) :
            	j=0
            	a = f1.readline().rstrip('\n\r').split(" ")
            	for k in range(len(a)) :
            	    if a[k]!="" :
            	    	j=a[k]
            	Zones_list_mesh.append(j.replace("\"",""))
        except :
            dlg = wx.MessageDialog(self.getParent(), 'No msh file found',
                               'A Message Box',
                               wx.OK | wx.ICON_INFORMATION
                               )
            val = dlg.ShowModal()
            dlg.Destroy()
            
        
        label1 = wx.StaticText(parent, -1, "Zone name:")
        label1.SetHelpText("This is the help text for the label")
        box1.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        self.newZoneCtrl = newZoneCtrl = wx.ComboBox(parent, -1, "",
                                 (250, 20), (200, -1),
                                 Zones_list_mesh, wx.CB_DROPDOWN)
                                 
        self.createdZonesComboMessage = createdZonesComboMessage = "list of zones\n you have to defined: "                         
                                 
        for st in self.Zones_list_mesh: 
        	self.createdZonesComboMessage+= "\n    - "+st
        self.newZoneCtrl.SetToolTipString(self.createdZonesComboMessage)
        newZoneCtrl.SetToolTipString(createdZonesComboMessage)                         
                                 
                                 
        self.zoneList = " list of created zones : \n\n"
        if   len(self.Zones_list)>0:
            for i in self.Zones_list:
                self.zoneList += " "*len(" list of created zones : ")+i + "\n"

        newZoneCtrl.SetToolTipString(self.zoneList)
        box1.Add(newZoneCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
        
        self.boundaryControl = boundaryControl = wx.CheckBox(parent, -1, ": as a boundary")
        box1.Add(boundaryControl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
      
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        

               
               
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Material and Aqueous state association:" ) , wx.HORIZONTAL)
        box3.SetMinSize((600,20))
        materialList = params.getParamValue(parameters.CUSTOM_MATERIAL_DB).getMaterials().keys()
        AqueousStateList = params.getParamValue(parameters.AqueousStates_list)


        self.materialsCombo = materialsCombo = wx.ComboBox(parent, -1, "",
                                 (250, 20), (200, -1),
                                 materialList, wx.CB_DROPDOWN)
        
        box3.Add(materialsCombo,0,wx.LEFT|wx.ALL, 1)
        self.AqueousStateCombo = AqueousStateCombo = wx.ComboBox(parent, -1, "",
                                 (250, 20), (200, -1),
                                 AqueousStateList, wx.CB_DROPDOWN)
        
        box3.Add(AqueousStateCombo,0,wx.LEFT|wx.ALL, 1)
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )  
        
        if self.cc == None or self.cc == False:
            self.newZoneCtrl.Enable(True)
            for elt in zoneCtrl:
                elt.Enable(False)
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
        
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box4.SetMinSize((600,20))
                
        
        label4 = wx.StaticText(parent, -1, "Already defined zones:")
        label4.SetHelpText("This is the help text for the label")
        box4.Add(label4, 0, wx.TOP|wx.ALL, 2)
 
        self.alreadyDefinedZone = alreadyDefinedZone = wx.ComboBox(parent, -1, "",
                                 (250, 20), (200, -1),
                                 self.zoneListAlreadyCreated, wx.CB_DROPDOWN)
                                                               
                                 
        self.createdZonesComboMessage = createdZonesComboMessage = "list of already defined\nzones: "                         
                                 
        for st in self.Zones_list: 
        	self.createdZonesComboMessage+= "\n    - "+st
        self.alreadyDefinedZone.SetToolTipString(self.createdZonesComboMessage)
        alreadyDefinedZone.SetToolTipString(createdZonesComboMessage)                         
                            
        self.zoneList = " list of created zones : \n\n"
        if len(self.zoneListAlreadyCreated)>0:
            for i in self.zoneListAlreadyCreated:
                self.zoneList += " "*len(" list of created zones : ")+i + "\n"

        alreadyDefinedZone.SetToolTipString(self.zoneList)
        box4.Add(alreadyDefinedZone, 1, wx.LEFT|wx.ALL, 2)
        
        self.delete = delete = wx.CheckBox(parent, -1, ": to be deleted")
        delete.Enable(False)
        box4.Add(self.delete, 1, wx.RIGHT|wx.ALL, 2)
       
        sizer.Add( box4, 1, wx.ALIGN_LEFT|wx.ALL, 2 )
        
        toto.Bind(wx.EVT_COMBOBOX, self._changeZone )
        
        toto.Bind(wx.EVT_CHECKBOX, self._deleteOnOff)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box5.SetMinSize((600,20))
        
        infos =""
        self.information = information = wx.StaticText(parent, -1, infos)
        box5.Add(self.information, 1, wx.ALIGN_LEFT|wx.ALL, 2)
        sizer.Add(box5, 1, wx.ALIGN_LEFT|wx.ALL, 2 )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        
        box6 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box6.SetMinSize((800,30))
       
        grid6 = wx.FlexGridSizer( 0, 1, 0, 0 )
        grid6.SetFlexibleDirection( wx.HORIZONTAL)
        box6.Add(grid6)
        
        self.apply = wx.Button(parent, -1, "Apply", (520,250))
        #create.SetTTS("used to create an aqueous state.\n")
        
        toto.Bind(wx.EVT_BUTTON, self._applyZone, self.apply)
        box6.Add(self.apply, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
                  
        parent.SetSizerAndFit(sizer)
      
      
    def _changeZone(self, event) :
        selected = self.alreadyDefinedZone.GetValue()
        if selected != None and selected != "" :
            if selected in self.params.getParam(parameters.Zone_BCKind_list).getValue() :
                infos = selected + " is a boundary\n"
            else :
                infos = selected + " is not a boundary\n"  
            infos += "material assiociated : " 
            ind = 0
            ind = self.Zones_list.index(selected)
            zone_list = self.params.getParam(parameters.Zones_list).getValue()
            zone_Material_AqueousState_list = self.params.getParam(parameters.Zone_Material_AqueousState_list).getValue()
            ICParameters = zone_Material_AqueousState_list[ind]
            infos += ICParameters[0]
            infos += "\naqueous state assiociated : " 
            infos += ICParameters[1]
            self.information.SetLabel(infos)
            self.delete.Enable(True)
      
    
    def _deleteOnOff(self,event) :
        if self.delete.GetValue() :
            self.newZoneCtrl.Enable(False)
            self.boundaryControl.Enable(False)
            self.materialsCombo.Enable(False)
            self.AqueousStateCombo.Enable(False)
        else :
            self.newZoneCtrl.Enable(True)
            self.boundaryControl.Enable(True)
            self.materialsCombo.Enable(True)
            self.AqueousStateCombo.Enable(True)
            
        
    def _selectedZoneControl( self, event ):
        selected = str(event.GetString())
        ind = self.Zones_list.index(selected)
        zoneElements = self.Zone_Material_AqueousState_list[ind]
        self.materialsCombo.SetValue(zoneElements[0])
        self.AqueousStateCombo.SetValue(zoneElements[1])
        return None
        
    def _onCCSelect( self, event ):
        self.radio_selected = radio_selected = event.GetEventObject()
        if event.IsChecked()==True:
#        if radio_selected.GetLabel()=="Define a new zone":
            self.cc = False
            self.newZoneCtrl.Enable(False)
        else:
            self.newZoneCtrl.Enable(True)
            self.cc = True

        for text in self.zoneCtrl:
            if radio_selected.GetLabel()!="Define a new zone":
                text.Enable(True)
                self.newZoneCtrl.Enable(False)
                self.delete.Enable(True)
            else:
                text.Enable(False)
                self.newZoneCtrl.Enable(True)
                self.delete.Enable(False)
                print " we enable zone creation"

    def _applyZone(self, event):
        if self.newZoneCtrl.IsEnabled() == True:
# no zone name newZoneCtrlhas been entered 
            if self.newZoneCtrl.GetValue() == "":
                wx.MessageDialog(self.parent, "you have to enter a name for the zone you want to consider"\
                ,"Warning", wx.OK | wx.ICON_WARNING).ShowModal()           
# a zone name has been entered which is already defined
            elif  self.newZoneCtrl.GetValue() in self.Zones_list:
                wx.MessageDialog(self.parent, "that label has already been used"\
                , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            else:
#
# field
#
                if self.AqueousStateCombo.GetValue() == "" or self.materialsCombo.GetValue() == "" :
                    wx.MessageDialog(self.parent, "an aqueous state combined to a material must be selected"\
                    , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
                    return None
                
                self.Zones_list.append(str(self.newZoneCtrl.GetValue()))
                a = [str(self.materialsCombo.GetValue()),
                     str(self.AqueousStateCombo.GetValue()),
                    ]
                self.Zone_Material_AqueousState_list.append(a)
                if self.boundaryControl.GetValue() == True:
                    self.Zone_BCKind_list.append(str(self.newZoneCtrl.GetValue()))
                    print " we treat a boundary ",self.Zones_list
                    self.params.getParam(parameters.Zone_BCKind_list).setValue(self.Zone_BCKind_list)
#
# update of the boundary condition list
#                    
                    self.params.getParam(parameters.BoundaryConditions_list).setValue(self.Zone_BCKind_list)
                    #self.params.getParam(parameters.AqueousStates_MineralPhases_list).setValue(self.mpl_perstate)
                    print self.Zone_BCKind_list,parameters.Zone_BCKind_list
                else:
                    self.InitialConditions_list.append(str(self.newZoneCtrl.GetValue()))
                    self.params.getParam(parameters.InitialConditions_list).setValue(self.InitialConditions_list)
                    
            self.params.getParam(parameters.Zone_BCKind_list).setValue(self.Zone_BCKind_list)
            self.params.getParam(parameters.Zones_list).setValue(self.Zones_list)
            self.params.getParam(parameters.Zone_Material_AqueousState_list).setValue(self.Zone_Material_AqueousState_list)
            self.zoneList = " list of created zones : \n\n"
            
        else:
            print " is enable is false",self.newZoneCtrl.IsEnabled
#
# zone selection
#
            if self.alreadyDefinedZone.GetValue() == "":
                wx.MessageDialog(self.parent, "you have to select the zone you want to consider."\
                    ,"Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            else:
                
                if self.delete:
                    strtemp = str(self.alreadyDefinedZone.GetValue())
                    self.alreadyDefinedZone.SetValue("")
                    ind = self.Zones_list.index(strtemp)
                    del self.Zone_Material_AqueousState_list[ind]
                    print self.Zone_Material_AqueousState_list
                    self.Zones_list.remove(strtemp)
                    if strtemp in self.Zone_BCKind_list:
                        self.Zone_BCKind_list.remove(strtemp)
                    else:
                        self.InitialConditions_list.remove(strtemp)
                    self.params.getParam(parameters.InitialConditions_list).setValue(self.InitialConditions_list)
                    self.params.getParam(parameters.Zone_BCKind_list).setValue(self.Zone_BCKind_list)
                    self.params.getParam(parameters.Zones_list).setValue(self.Zones_list)
                    self.params.getParam(parameters.Zone_Material_AqueousState_list).setValue(self.Zone_Material_AqueousState_list)
                    self.alreadyDefinedZone.SetItems(self.params.getParam(parameters.Zones_list).getValue())
                    self.information.SetLabel("")
                    self.delete.SetValue(False)
                    self.delete.Enable(False)
                    self.newZoneCtrl.Enable(True)
                    self.boundaryControl.Enable(True)
                    self.materialsCombo.Enable(True)
                    self.AqueousStateCombo.Enable(True)
                else:
                    a = [str(self.materialsCombo.GetValue()),
                         str(self.AqueousStateCombo.GetValue()),str(self.createdZonesCombo.GetValue())]
                    ind = 0
                    for i in self.Zone_Material_AqueousState_list:
                        ind +=1
                        if self.createdZonesCombo == i[2]:
                            break
                    self.Zone_Material_AqueousState_list[ind] = a
                    
        return None
        
    def _onOk(self, params):
        self.params.getParam(parameters.Zone_BCKind_list).setValue(self.Zone_BCKind_list)
        self.params.getParam(parameters.Zones_list).setValue(self.Zones_list)
        self.params.getParam(parameters.Zone_Material_AqueousState_list).setValue(self.Zone_Material_AqueousState_list)
        return True
