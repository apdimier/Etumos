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
class SetZones(ParamsAction):
    """
    Enables the association of materials and aqueous states over the domain
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Set Zones",description  =description,help=HELP)
        self.radios = None
        self.choice = None
        self.cc = None

    def _createInterface(self, parent, params):
        
        sizer = wx.BoxSizer( wx.VERTICAL )

# set zones
   
        actionLabels = ACTION_BY_LABEL
   
        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "set zones" ) , wx.HORIZONTAL )
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
        choice1 = None
        
        currentAction = str(ACTION_BY_LABEL[0])
        for (i,n) in enumerate(ACTION_BY_LABEL):
            print " i n ",i
            print " i n ",n
            if i == 0:    
                style = wx.RB_GROUP
            else:
                style = 0
            radio = wx.RadioButton( parent, -1, n,  style=style )
            
            radio.SetToolTipString("action is " + ACTION_BY_LABEL[i])
            grid1.Add( radio, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 2 )
            radios1.append( radio )
            radio.SetValue( currentAction == ACTION_BY_LABEL[i] )

        self.radios1 = radios1
        self.choice1 = choice1
        box1.Add( grid1, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
        toto = self.GetDialogPanel()
        for radios in radios1:
            toto.Bind(wx.EVT_RADIOBUTTON, self._onCCSelect, radios )

#defining new zone names

        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "zone name") , wx.HORIZONTAL)
        box1.SetMinSize((600,30))

        start = params.getParam( parameters.Iterate_InitialTime )
        dt0 = params.getParam( parameters.Iterate_InitialTimeStepSize )
        simulationTime = params.getParam( parameters.Iterate_SimulationTime )
        
        label1 = wx.StaticText(parent, -1, "New zone name:")
        label1.SetHelpText("This is the help text for the label")
        box1.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
 
        self.newZoneCtrl = newZoneCtrl = wx.TextCtrl(parent, -1, "", size=(80,-1));newZoneCtrl.Enable(True)
        self.zoneList = " list of created zones : \n\n"
        if   len(self.Zones_list)>0:
            for i in self.Zones_list:
                self.zoneList += " "*len(" list of created zones : ")+i + "\n"

        newZoneCtrl.SetToolTipString(self.zoneList)
        box1.Add(newZoneCtrl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
        
        self.boundaryControl = boundaryControl = wx.CheckBox(parent, -1, ": as a boundary")
        box1.Add(boundaryControl, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
      
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 2 )
#        
# already created zones gestion
#
        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Already created zones" ) , wx.HORIZONTAL)
        box2.SetMinSize((600,20))
        
        label1 = wx.StaticText(parent, -1, "Created zones:",size=(120,-1));label1.SetHelpText("list of already created zones")
        box2.Add(label1, 0, wx.LEFT|wx.ALL, 1)
#
# Zones_list
#
        self.createdZonesComboMessage = createdZonesComboMessage = "list of already defined\nzones: "

        self.createdZonesCombo = createdZonesCombo = wx.ComboBox(parent, -1, "",
                                 (250, 20), (200, -1),Zones_list, wx.CB_DROPDOWN)
        for st in self.Zones_list: self.createdZonesComboMessage+= "\n    - "+st
        self.createdZonesCombo.SetToolTipString(self.createdZonesComboMessage)
        createdZonesCombo.SetToolTipString(createdZonesComboMessage)

        box2.Add(createdZonesCombo,0,wx.LEFT|wx.ALL, 1);zoneCtrl.append(createdZonesCombo)
        toto.Bind(wx.EVT_COMBOBOX, self._selectedZoneControl, self.createdZonesCombo)
        
        self.delete = delete = wx.CheckBox(parent, -1, ": to be deleted");delete.Enable(False)
        box2.Add(delete, 1, wx.ALIGN_CENTRE|wx.ALL, 2)
        sizer.Add(box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )  
               
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Material and Aqueous state association:" ) , wx.HORIZONTAL)
        box3.SetMinSize((600,20))
        materialList = params.getParamValue(parameters.CUSTOM_MATERIAL_DB).getMaterials().keys()
        AqueousStateList = params.getParamValue(parameters.AqueousStates_list)
#
#        print " list of aqueous states : ",AqueousStateList
#
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
              

        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "zone bounds:" ) , wx.HORIZONTAL)
        box4.SetMinSize((500,40))

# controlling i domain extension
       
        grid4 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid4.SetFlexibleDirection( wx.HORIZONTAL)
        box4.Add(grid4)
        self.label41 = label41 = wx.StaticText(parent, -1, "I lower bound:",size=(150,-1))
        label41.SetHelpText("This is the help text for the label")
        CCctrls.append(label41)
        grid4.Add(label41, 0, wx.LEFT|wx.ALL, 1)
 
        self.iminCtrl = iminCtrl = wx.TextCtrl(parent, -1,"1",size=(50,-1))
        iminCtrl.SetHelpText("Here's some help text for field #1")
        CCctrls.append(iminCtrl)
        grid4.Add(iminCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        self.label42 = label42 = wx.StaticText(parent, -1, "  I upper bound:",size=(150,-1))
        CCctrls.append(label42)
        grid4.Add(label42, 0, wx.LEFT|wx.ALL, 1)

        self.imaxCtrl = imaxCtrl = wx.TextCtrl(parent, -1,"1", size=(50,-1))
        CCctrls.append(imaxCtrl)
        grid4.Add(imaxCtrl, 1, wx.LEFT|wx.RIGHT, 1)

        sizer.Add(box4, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

# controlling j domain extension

        box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box5.SetMinSize((500,40))

        grid5 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid5.SetFlexibleDirection( wx.HORIZONTAL)
        box5.Add(grid5)
        
        self.label51 = label51 = wx.StaticText(parent, -1, "J lower bound:",size=(150,-1));label51.SetHelpText("This is the help text for the label")
        CCctrls.append(label51)
        grid5.Add(label51, 0, wx.LEFT|wx.ALL, 1)
 
        self.jminCtrl = jminCtrl = wx.TextCtrl(parent, -1,"1",size=(50,-1))
        CCctrls.append(jminCtrl)
        grid5.Add(jminCtrl, 1, wx.LEFT|wx.RIGHT, 1)
       
        self.label52 = label52 = wx.StaticText(parent, -1, "  J upper bound:",size=(150,-1))
        CCctrls.append(label52)
        grid5.Add(label52, 0, wx.LEFT|wx.ALL, 1)

        self.jmaxCtrl = jmaxCtrl = wx.TextCtrl(parent, -1,"1", size=(50,-1))
        CCctrls.append(jmaxCtrl)
        grid5.Add(jmaxCtrl, 1, wx.LEFT|wx.RIGHT, 1)
        
        sizer.Add(box5, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
       
        box6 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box6.SetMinSize((800,80))

# bindings creation
       
        grid6 = wx.FlexGridSizer( 0, 6, 0, 0 )
        grid6.SetFlexibleDirection( wx.HORIZONTAL)
        box6.Add(grid6)
        self.apply = wx.Button(parent, -1, "Apply", (520,250))
        #create.SetTTS("used to create an aqueous state.\n")
        
        toto.Bind(wx.EVT_BUTTON, self._applyZone, self.apply)
        box6.Add(self.apply, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
                  
        parent.SetSizerAndFit(sizer)
        
    def _selectedZoneControl( self, event ):
        selected = str(event.GetString())
        print " _selectedZoneControl",selected
        ind = self.Zones_list.index(selected)
        zoneElements = self.Zone_Material_AqueousState_list[ind]
        self.materialsCombo.SetValue(zoneElements[0])
        self.AqueousStateCombo.SetValue(zoneElements[1])
        self.iminCtrl.SetValue(zoneElements[2])
        self.imaxCtrl.SetValue(zoneElements[3])
        self.jminCtrl.SetValue(zoneElements[4])
        self.jmaxCtrl.SetValue(zoneElements[5])
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
                     str(self.iminCtrl.GetValue()),str(self.imaxCtrl.GetValue()),
                     str(self.jminCtrl.GetValue()),str(self.jmaxCtrl.GetValue())]
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
            self.createdZonesCombo.SetItems(self.Zones_list)
            self.zoneList = " list of created zones : \n\n"
            for i in self.Zones_list:
                self.zoneList += " "*len(" list of created zones :    ")+i + "\n"
        else:
            print " is enable is false",self.newZoneCtrl.IsEnabled
#
# zone selection
#
            if self.createdZonesCombo.GetValue() == "":
                wx.MessageDialog(self.parent, "you have to select the zone you want to consider."\
                    ,"Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            else:
                
                if self.delete:
                    strtemp = str(self.createdZonesCombo.GetValue())
                    ind = self.Zones_list.index(str(self.createdZonesCombo.GetValue()))
                    del self.Zone_Material_AqueousState_list[ind]
                    print self.Zone_Material_AqueousState_list
                    self.Zones_list.remove(str(self.createdZonesCombo.GetValue()))
                    print " str ",strtemp
                    if strtemp in self.Zone_BCKind_list:
                        self.Zone_BCKind_list.remove(strtemp)
                    else:
                        self.InitialConditions_list.remove(strtemp)
                    self.params.getParam(parameters.InitialConditions_list).setValue(self.InitialConditions_list)
                    self.params.getParam(parameters.Zone_BCKind_list).setValue(self.Zone_BCKind_list)
                    self.params.getParam(parameters.Zones_list).setValue(self.Zones_list)
                    self.params.getParam(parameters.Zone_Material_AqueousState_list).setValue(self.Zone_Material_AqueousState_list)
                    self.createdZonesCombo.SetItems(self.Zones_list)
                    self.delete.Enable(False)
                else:
                    a = [str(self.materialsCombo.GetValue()),
                         str(self.AqueousStateCombo.GetValue()),str(self.createdZonesCombo.GetValue()),
                         str(self.iminCtrl.GetValue()),str(self.imaxCtrl.GetValue()),
                         str(self.jminCtrl.GetValue()),str(self.jmaxCtrl.GetValue())]
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
       
