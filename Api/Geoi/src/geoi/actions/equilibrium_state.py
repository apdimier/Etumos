import wx

from geoi.actions.params_action import ParamsAction
from geoi.actions.GridCustTable import CustTableGrid
from geoi import parameters
from parameter import IS_ION, IS_POSITIVE_NUMBER, IS_NUMBER

description =\
       """ 
       Assemblage of pure phases that can react reversibly with the aqueous phase. 
       """
HELP = """
       <html><body>
       You will be able to enter here the amounts of an assemblage of pure phases that can react reversibly
       with the aqueous phase.When theses <b>phases</b> are brought in contact with the <b>aqueous solution</b>, each phase
       will dissolve or precipitate to achieve equilibrium or will dissolve completely.<br>
       Pure phases include minerals with fixed composition. <br>
       You will have access here in an, informatician hope, ""<b>user friendly</b>" way to the available mineral list,
       database defined and user defined ones.<br>. you can only setup a mineral list within the association to an aqueous state.
       <br>
       <b>Chalcedony</b> 0.0 0.0<br>
       <b>Calcite</b> 0. 0.<br>
       For further notes look at the phreeqC manual 99-4259 page 118
       </body></html>"""
class EquilibriumPhasesDefinition(ParamsAction):
    """
    Enables the association of materials and aqueous states over the domain
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Equilibrium Phase setup",description  =description,help=HELP)

    def _createInterface(self, parent, params):
        
        sizer = wx.BoxSizer( wx.VERTICAL )

# aqueous state control
   
        self.equilibriumStateDescription = "The user retrieves here the mineral composition for the cell considered,\n each material being"+\
        " associated to its saturation index and its amount"
        self.aqueousStateList = aqueousStateList = []
        self.parent = parent
        self.params = params
#        self.apl_perstate = None
        self.equilibrium_phase = None
#        self.mpl_perstate = None
#        self.mppl_perstate = None
        self.equi_phase_mineralList = None
        self.equi_phase_mineralPropertiesList = None

        self.ind = None
        print " aqueous paramaters ",self.params.getParam(parameters.AqueousStates_Properties_list).getValue()
        toto = self.GetDialogPanel()
        wx.TextCtrl.SetTTS = wx.TextCtrl.SetToolTipString
        wx.StaticText.SetTTS = wx.StaticText.SetToolTipString
        wx.CheckBox.SetTTS = wx.CheckBox.SetToolTipString
        wx.Button.SetTTS = wx.Button.SetToolTipString
        f = wx.Font(10, wx.ROMAN, wx.ITALIC, wx.BOLD, True)
        boldFont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")

        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Aqueous State selection" ) , wx.HORIZONTAL)
        box1.SetMinSize((500,30))
        grid1 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid1.SetFlexibleDirection( wx.HORIZONTAL)
# selected aqueous statestate
        self.selectedState = selectedState = wx.TextCtrl(parent, -1, "", size=(200,-1))
        selectedState.SetTTS("selected aqueous state")
        selectedState.SetValue( "" )
        grid1.Add(selectedState, 1, wx.ALIGN_CENTRE|wx.ALL, border = 1)
        grid1.AddSpacer(15)

        self.aqueousStateList = aqueousStateList = params.getParamValue(parameters.AqueousStates_list)
        self.stateComboMessage = stateComboMessage = "list of already defined\naqueous states: "
        if aqueousStateList == []:
            comboboxDefault = ""
            stateComboMessage+="[]"
        else:
            comboboxDefault = aqueousStateList[0]
            for st in self.aqueousStateList: stateComboMessage+="\n"+st
        self.createdAStatesCombo = createdAStatesCombo = wx.ComboBox(parent, -1, comboboxDefault,
                                 (250, 20), (200, -1),
                                 self.aqueousStateList, wx.CB_DROPDOWN)
        createdAStatesCombo.SetToolTipString(stateComboMessage)
        createdAStatesCombo.SetLabel("Aqueous states")
                                 
        grid1.Add(createdAStatesCombo,0,wx.LEFT|wx.ALL, 1)
        toto.Bind(wx.EVT_COMBOBOX, self._selectedStateControl, createdAStatesCombo)

        box1.Add( grid1, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#        
# choice of minerals
#
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Mineral phase association" ) , wx.HORIZONTAL)
#        box3.SetOwnFont(boldFont)
        box3.SetMinSize((600,50))

        
        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box31.SetMinSize((300,30))

        label1 = wx.StaticText(parent,-1,"Mineral:",size=(60,-1));label1.SetTTS("Selected mineral")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.selectedMinerals = selectedMinerals = [""]
        self.selectedMineral = selectedMineral = \
        wx.ComboBox(parent, -1, "",(250, 20), (200, -1),selectedMinerals, wx.CB_DROPDOWN)
        toto.Bind(wx.EVT_COMBOBOX, self._selectedMineralControl, selectedMineral)

        box31.Add(selectedMineral, 0., wx.ALIGN_CENTER|wx.ALL, 1)

        box3.Add(box31, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        box32 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box32.SetMinSize((250,20))
        self.dbMineralsList = dbMineralsList = params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getMineralPhases().keys()
        dbMineralsList += params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getMineralPhases().keys()
        label2 = wx.StaticText(parent, -1, "D.B. Minerals:",size=(100,-1))
        label2.SetOwnFont(boldFont)
        label2.SetTTS("you define the mineral phase composition through\navalaible phases element within that one ")

        box32.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.mineralComboMessage = "list of available mineral phases: "
        mineralComboboxDefault = ""
        self.availableMineralCombo = availableMineralCombo =\
        wx.ComboBox(parent, -1, mineralComboboxDefault,(250, 20), (200, -1),dbMineralsList, wx.CB_DROPDOWN)
        
        availableMineralCombo.SetToolTipString("available minerals among the selected database ones\n and user defined ones")
        availableMineralCombo.SetLabel("available Minerals")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedMineralControl, availableMineralCombo)
                                 
        box32.Add(availableMineralCombo,0,wx.ALIGN_CENTER|wx.ALL, 1)


        box3.Add(box32, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

# initial guesses

        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Data" ) , wx.HORIZONTAL)
        box2.SetMinSize((300,20))
        box21 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box21.SetMinSize((300,20))
        grid2 = wx.FlexGridSizer( 0, 6, 0, 0 )
        grid2.SetFlexibleDirection( wx.HORIZONTAL)
        
        label1 = wx.StaticText(parent, -1, "Saturation Index:");label1.SetTTS("saturation index")
        label1.SetOwnFont(boldFont)
        grid2.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.saturationIndex = saturationIndex = wx.TextCtrl(parent,-1, "0.0",size=(70,-1))
        saturationIndex.SetTTS("default saturation index is 0")
        grid2.Add(saturationIndex, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        label2 = wx.StaticText(parent, -1, " Dis. only:");label1.SetTTS("If selected, the mineral can not precipitate")
        label2.SetOwnFont(boldFont)
        grid2.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        self.dissolveOnly = dissolveOnly = wx.CheckBox(parent, -1, "    ") ;dissolveOnly.SetValue(False)
        grid2.Add(dissolveOnly, 1, wx.ALIGN_CENTRE|wx.ALL, 1)
               
        box21.Add( grid2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        box2.Add( box21, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# Moles amount control control
#
        box22 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box2.Add( box22, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        box22.SetMinSize((300,20))
        label221 = wx.StaticText(parent, -1, "  moles amount:")
        label221.SetTTS("available moles amount within\nthe specified solution")
        label221.SetOwnFont(boldFont)
        box22.Add(label221, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        self.molesAmount = molesAmount = wx.TextCtrl(parent, -1, "0.0", size=(130,-1));
        molesAmount.SetTTS("available moles amount within\n the specified solution")
        box22.Add(molesAmount, 0, wx.ALIGN_LEFT|wx.ALL, 1)

        sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# mineral phase definition
#
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Already associated phases " ) , wx.HORIZONTAL)
        box4.SetMinSize((600,100))

        self.mineralPhaseState = mineralPhaseState = wx.TextCtrl(parent, -1,"",
                       size=(300, 90), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        mineralPhaseState.SetOwnFont(boldFont)
        mineralPhaseState.SetForegroundColour("#1857DE")
	mineralPhaseState.SetTTS(self.equilibriumStateDescription)
        mineralPhaseState.SetInsertionPoint(0)
        toto.Bind(wx.EVT_TEXT, self._evtText, mineralPhaseState)
        
        box4.Add(mineralPhaseState, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.update = update = wx.Button(parent, -1, "Update", (50,50))
        update.SetTTS("used to update the mineral phase\nassociated to an aqueous state.\n")
        toto.Bind(wx.EVT_BUTTON, self._updateMineralPhase, update)
        box4.Add(update, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        self.delete = delete = wx.Button(parent, -1, "Delete", (50,50))
        delete.SetTTS("used to delete the selected mineral\n from the phase definition")
        toto.Bind(wx.EVT_BUTTON, self._deletePhase, delete)
        box4.Add(delete, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        sizer.Add(box4, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)
        

        
    def _selectedStateControl(self, event):
        selected = event.GetString()
        self.selectedState.SetValue(selected)
        self.ind = self.params.getParam(parameters.AqueousStates_list).getValue().index(selected)
# we get the already defined element, if any        
        self.equi_phase_mineralList = self.params.getParam(parameters.AqueousStates_MineralPhases_list).getValue()
        self.selectedMineral.SetItems(self.equi_phase_mineralList[self.ind])
        self.equi_phase_mineralPropertiesList =\
            self.params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).getValue()
        #### a faire : mise a jour de la description de l'etat
        if self.equi_phase_mineralList[self.ind] != []:
            equiDescription = _mineralToString(self.equi_phase_mineralList[self.ind],self.equi_phase_mineralPropertiesList[self.ind])
        else:
            equiDescription = ""
        self.mineralPhaseState.SetValue(equiDescription)
        self.selectedMineral.SetValue("")
        self.saturationIndex.SetValue(str(0.0))
        self.molesAmount.SetValue(str(0.0))
        self.dissolveOnly.SetValue(False)
 
    def _updateMineralData(self,selected):
# update of the already available values
        if self.ind == None:
            self.saturationIndex.SetValue(str(0.0))
            self.molesAmount.SetValue(str(0.0))
            self.dissolveOnly.SetValue(False)
        elif selected in self.equi_phase_mineralList[self.ind]:
            indiz = self.equi_phase_mineralList[self.ind].index(selected)
            self.saturationIndex.SetValue(str(self.equi_phase_mineralPropertiesList[self.ind][indiz][0]))
            self.molesAmount.SetValue(str(self.equi_phase_mineralPropertiesList[self.ind][indiz][1]))
            self.dissolveOnly.SetValue(self.equi_phase_mineralPropertiesList[self.ind][indiz][2])
# we set to default values        
        else:
            self.saturationIndex.SetValue(str(0.0))
            self.molesAmount.SetValue(str(0.0))
            self.dissolveOnly.SetValue(False)
 
    def _selectedMineralControl(self, event):
        selected = event.GetString()
        self.selectedMineral.SetValue(selected)
        self._updateMineralData(selected)

    def _deletePhase(self, event):
        selected = str(self.selectedMineral.GetValue())
        if selected != "":
            indiz = self.equi_phase_mineralList[self.ind].index(selected)
            del self.equi_phase_mineralList[self.ind][indiz]
            del self.equi_phase_mineralPropertiesList[self.ind][indiz]
            self.params.getParam(parameters.AqueousStates_MineralPhases_list).setValue(self.equi_phase_mineralList)
            self.params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).setValue(self.equi_phase_mineralPropertiesList)
            
            equiDescription = _mineralToString(self.equi_phase_mineralList[self.ind],self.equi_phase_mineralPropertiesList[self.ind])
            self.mineralPhaseState.SetValue(equiDescription)
            self.selectedMineral.SetValue("")
            self.selectedMineral.SetItems(self.equi_phase_mineralList[self.ind])
        else:
            wx.MessageDialog(self.parent, "you have to select an aqueous solution and\n"+\
            "an already associated mineral to complete that action"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
        return

    def _updateMineralPhase(self, event):
        print "ok"
#
#       First we control that an aqueous state has been selected
#
        stateName = str(self.selectedState.GetValue()).replace(" ","")
        updateControl = None
        if stateName == "":
            wx.MessageDialog(self.parent, "you have to select an aqueous solution first\n"+\
            "before entering a mineral composition"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        mineralName = str(self.selectedMineral.GetValue()).replace(" ","")
        if mineralName == "":
            wx.MessageDialog(self.parent, "you have to select a mineral name first\n"+\
            "before trying to update the mineral phase"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        self.equi_phase_mineralList = self.params.getParam(parameters.AqueousStates_MineralPhases_list).getValue()
        self.equi_phase_mineralPropertiesList = self.params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).getValue()
        if mineralName in self.equi_phase_mineralList[self.ind]:
            print "if ",self.ind
            mineralInd =  self.equi_phase_mineralList[self.ind].index(mineralName)
            self.equi_phase_mineralPropertiesList[self.ind][mineralInd] =\
                              (str(self.saturationIndex.GetValue()),str(self.molesAmount.GetValue()),0)            
        else:
            print "else "
            self.equi_phase_mineralList[self.ind].append(mineralName)
            self.equi_phase_mineralPropertiesList[self.ind].append((self.saturationIndex.GetValue(),self.molesAmount.GetValue(),0))
        self.params.getParam(parameters.AqueousStates_MineralPhases_list).setValue(self.equi_phase_mineralList)
        self.params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).setValue(self.equi_phase_mineralPropertiesList)
# we reinitialize the elements to leere Zeilen, the aqueous state bleibt, only the mineral is reinitialised
        equiDescription = _mineralToString(self.equi_phase_mineralList[self.ind],self.equi_phase_mineralPropertiesList[self.ind])
        self.mineralPhaseState.SetValue(equiDescription)
        self.selectedMineral.SetItems(self.equi_phase_mineralList[self.ind])

    def _evtText(self, event):
        pass

        
    def _onOk(self, params):
# list of states by name:        
        params.getParam(parameters.AqueousStates_list).setValue(self.aqueousStateList)
# list of list  describing each state:        
        params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).setValue(self.equi_phase_mineralPropertiesList)

        return True
        
def _mineralToString(equi_phase_mineralList,equi_phase_mineralPropertiesList):      
    a = ""
    for ind in range (0,len(equi_phase_mineralList)):
        a+= str(equi_phase_mineralList[ind]) + " " +\
            str(equi_phase_mineralPropertiesList[ind][0]) + " " +\
            str(equi_phase_mineralPropertiesList[ind][1])+"\n"
    return a

