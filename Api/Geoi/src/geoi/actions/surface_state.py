import wx

from geoi.actions.params_action import ParamsAction
from geoi.actions.GridCustTable import CustTableGrid
from geoi import parameters
from parameter import IS_ION, IS_POSITIVE_NUMBER, IS_NUMBER

description =\
       """ 
       Surface species that can react reversibly with the aqueous phase. 
       """
HELP = """
       <html><body>
       You will be able to enter here the amounts and composition of each surface assemblage.
       Initial composition of the surface assemblage can be defined in two ways,
       <b>(1) <b>explicitely</b> by defining the amounts of the surfaces in their neutral form or <b>(2)  implicitly</b>,
       by specifying that the surface is in equilibrium with a solution of fixed composition.
       You will have access here in an ""<b>user friendly</b>" way to the available surfacer list, database defined and user
       defined ones.<br>
       <b>Surfa_w</b> 1.0 1000. 0.33<br>
       <b>Surfa_s</b> 0.01<br>
       For further notes look at the phreeqC manual 99-4259 page 163

       </body></html>"""
class SurfaceDefinition(ParamsAction):
    """
    Enables the association of materials and aqueous states over the domain
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Surface setup",description  =description,help=HELP)

    def _createInterface(self, parent, params):
        
        sizer = wx.BoxSizer( wx.VERTICAL )

# aqueous state control
   
        self.surfaceDescription = "you will discover here in a phreeqC written way\n"+\
                                   "the description in terms of amounts and composition\n"+\
                                   "of an assemblage of surfacers." 
        self.aqueousStateList = aqueousStateList = []
        self.parent = parent
        self.params = params
        self.apl_perstate = None
        self.equilibrium_phase = None
#        self.mpl_perstate = None
#        self.mppl_perstate = None
        self.surfaceSpeciesList = None
        self.surfacePropertiesList = None

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
# choice of surfacers
#
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "surfacer association" ) , wx.HORIZONTAL)
#        box3.SetOwnFont(boldFont)
        box3.SetMinSize((600,50))

        
        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box31.SetMinSize((300,30))

        label1 = wx.StaticText(parent,-1,"Surfacer:",size=(60,-1));label1.SetTTS("Selected surface assemblage")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.selectedSurfacers = selectedSurfacers = [""]
        self.selectedSurfaceSpecies = selectedSurfaceSpecies = \
        wx.ComboBox(parent, -1, "",(250, 20), (200, -1),selectedSurfacers, wx.CB_DROPDOWN)
        toto.Bind(wx.EVT_COMBOBOX, self._selectedSurfaceControl, selectedSurfaceSpecies)

        box31.Add(selectedSurfaceSpecies, 0., wx.ALIGN_CENTER|wx.ALL, 1)

        box3.Add(box31, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        box32 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box32.SetMinSize((250,20))
        self.dbSurfaceSpeciesList = dbSurfaceSpeciesList = params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getSurfaceSpecies().keys()
        dbSurfaceSpeciesList += params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSurfaceSpecies().keys()
        #print params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getSurfaceSpecies()
        label2 = wx.StaticText(parent, -1, "D.B. Surface S.:",size=(110,-1))
        label2.SetOwnFont(boldFont)
        label2.SetTTS("you define the surface composition through\navailable surface species within that one ")

        box32.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.surfaceComboMessage = "list of available surface species: "
        surfaceComboboxDefault = ""
        self.availableSurfaceCombo = availableSurfaceCombo =\
        wx.ComboBox(parent, -1, surfaceComboboxDefault,(240, 20), (200, -1),dbSurfaceSpeciesList, wx.CB_DROPDOWN)
        
        availableSurfaceCombo.SetToolTipString("available surface species based on those\nof the selected database\n and user defined ones")
        availableSurfaceCombo.SetLabel("available surface species")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedSurfaceControl, availableSurfaceCombo)
                                 
        box32.Add(availableSurfaceCombo,0,wx.ALIGN_CENTER|wx.ALL, 1)


        box3.Add(box32, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

# initial guesses

        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Surface definition" ) , wx.HORIZONTAL)
        box2.SetMinSize((350,20))
        
#
# Moles amount control
#
        box22 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box2.Add( box22, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        box22.SetMinSize((200,20))
        label221 = wx.StaticText(parent, -1, "moles\namount:")
        label221.SetOwnFont(boldFont)
        box22.Add(label221, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        self.molesAmount = molesAmount = wx.TextCtrl(parent, -1, "0.0", size=(100,-1));
        molesAmount.SetTTS("available moles amount within\n the specified solution\nfor the surface species considered")
        box22.Add(molesAmount, 0, wx.ALIGN_LEFT|wx.ALL, 1)
#
# surface specific area control
#
        box21 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box21.SetMinSize((450,20))
        grid2 = wx.FlexGridSizer( 0, 6, 0, 0 )
        grid2.SetFlexibleDirection( wx.HORIZONTAL)

        label2 = wx.StaticText(parent, -1, " Spec. Area :")
        label1.SetTTS("enables to define a a specific area of surface, in m**2/g. Default is 600 m**2/g")
        label2.SetOwnFont(boldFont)
        grid2.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        self.specificArea = specificArea = wx.CheckBox(parent, -1, "    ")
        specificArea.SetTTS("enables to define a a specific area of surface, in m**2/g. Default is 600 m**2/g")
        specificArea.SetValue(False)
        toto.Bind(wx.EVT_CHECKBOX, self._specificArea, specificArea)

        grid2.Add(specificArea, 1, wx.ALIGN_CENTRE|wx.ALL, 1)

        
        label1 = wx.StaticText(parent, -1, "/g:");label1.SetTTS("phase with attached surface site")
        label1.SetOwnFont(boldFont)
        grid2.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.specificAreaPerGram = specificAreaPerGram = wx.TextCtrl(parent,-1, "600.",size=(100,-1))
        specificAreaPerGram.SetTTS("specific area per gram\n")
        specificAreaPerGram.Enable(False)
        specificAreaPerGram.SetLabel("toto");specificAreaPerGram.Update()
        grid2.Add(specificAreaPerGram, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        label2 = wx.StaticText(parent, -1, "mass:");label1.SetTTS("phase with attached surface site")
        label2.SetOwnFont(boldFont)
        grid2.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.ratio = ratio = wx.TextCtrl(parent,-1, "0.0",size=(100,-1))
        ratio.SetTTS("mass")
        ratio.Enable(False)
        grid2.Add(ratio, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
               
        box21.Add( grid2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        box2.Add( box21, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

        sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# surface species definition
#
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "already associated surface species " ) , wx.HORIZONTAL)
        box4.SetMinSize((600,100))

        self.surfaceState = surfaceState = wx.TextCtrl(parent, -1,"",
                       size=(300, 90), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        surfaceState.SetOwnFont(boldFont)
        surfaceState.SetForegroundColour("#1857DE")
	surfaceState.SetTTS(self.surfaceDescription)
        surfaceState.SetInsertionPoint(0)
        toto.Bind(wx.EVT_TEXT, self._evtText, surfaceState)
        
        box4.Add(surfaceState, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.update = update = wx.Button(parent, -1, "Update", (50,50))
        update.SetTTS("used to update the surface species\nassociated to an aqueous state.\n")
        toto.Bind(wx.EVT_BUTTON, self._updateSurface, update)
        box4.Add(update, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        self.delete = delete = wx.Button(parent, -1, "Delete", (50,50))
        delete.SetTTS("used to delete the selected surface species\n from the specificAreaPerGram definition")
        toto.Bind(wx.EVT_BUTTON, self._deletePhase, delete)
        box4.Add(delete, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        sizer.Add(box4, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)
        
    def _specificArea(self, event):
        if event.IsChecked()==True:
            self.specificAreaPerGram.Enable(True)
            self.ratio.Enable(True)
            return self.specificArea.SetValue(True)
        elif event.IsChecked()==False:
            self.specificAreaPerGram.Enable(False)
            self.ratio.Enable(False)
            return self.specificArea.SetValue(False)
        
    def _selectedStateControl(self, event):
        selected = event.GetString()
        self.selectedState.SetValue(selected)
        self.ind = self.params.getParam(parameters.AqueousStates_list).getValue().index(selected)
# We get the already defined element, if any        
        self.surfaceSpeciesList = self.params.getParam(parameters.AqueousStates_SurfaceSpecies_list).getValue()
        print "238 selectedStateControl",self.surfaceSpeciesList,self.ind
        self.selectedSurfaceSpecies.SetItems(self.surfaceSpeciesList[self.ind])
        self.surfacePropertiesList =\
            self.params.getParam(parameters.AqueousStates_SurfaceSpecies_Properties_list).getValue()
#
# We update the presentation of the surface state
#
        if self.surfaceSpeciesList[self.ind] != []:
            equiDescription = _surfaceToString(self.surfaceSpeciesList[self.ind],self.surfacePropertiesList[self.ind])
        else:
            equiDescription = ""
        self.surfaceState.SetValue(equiDescription)
        self.selectedSurfaceSpecies.SetValue("")
        self.specificAreaPerGram.SetValue(str(0.0))
        self.molesAmount.SetValue(str(0.0))
        self.specificArea.SetValue(False)
 
    def _updateSurfaceData(self,selected):
# update of the already available values
        print " 256 ",str(selected)
        surfaceSpeciesName = str(selected)
        if surfaceSpeciesName in self.surfaceSpeciesList[self.ind]:
            ind = self.surfaceSpeciesList[self.ind].index(surfaceSpeciesName)
            self.specificAreaPerGram.SetValue(self.surfacePropertiesList[self.ind][ind][0])
            self.molesAmount.SetValue(self.surfacePropertiesList[self.ind][ind][1])
            self.specificArea.SetValue(self.surfacePropertiesList[self.ind][ind][2])
# we set to default values        
        else:
            print " 265",surfaceSpeciesName
            self.surfaceSpeciesList[self.ind].append(surfaceSpeciesName)
            if self.specificArea.GetValue():
                check = 1
                mineralName =  self.specificAreaPerGram.GetValue()
                mineralRatio = self.specificArea.GetValue()
                print "debug 268 ",mineralName,mineralRatio
            else:
                check = 0
                mineralName = 0
                mineralRatio = 0
            self.surfacePropertiesList[self.ind].append((self.molesAmount.GetValue(),check,\
                                                             mineralName,mineralRatio))
            self.specificAreaPerGram.SetValue(str(0.0))
            self.molesAmount.SetValue(str(0.0))
            self.specificArea.SetValue(False)
 
    def _selectedSurfaceControl(self, event):
        selected = event.GetString()
        print "selected: ",selected
        self.selectedSurfaceSpecies.SetValue(selected)
        self._updateSurfaceData(selected)

    def _deletePhase(self, event):
        selected = str(self.selectedSurfaceSpecies.GetValue())
        if selected != "":
            ind = self.surfaceSpeciesList[self.ind].index(selected)
            del self.surfaceSpeciesList[self.ind][ind]
            del self.surfacePropertiesList[self.ind][ind]
            self.params.getParam(parameters.AqueousStates_SurfaceSpecies_list).setValue(self.surfaceSpeciesList)
            self.params.getParam(parameters.AqueousStates_SurfaceSpecies_Properties_list).setValue(self.surfacePropertiesList)
            
            equiDescription = _surfaceToString(self.surfaceSpeciesList[self.ind],self.surfacePropertiesList[self.ind])
            print "296 equiDescription: ",equiDescription
            self.surfaceState.SetValue(equiDescription)
            self.selectedSurfaceSpecies.SetValue("")
            self.selectedSurfaceSpecies.SetItems(self.surfaceSpeciesList[self.ind])
        else:
            wx.MessageDialog(self.parent, "you have to select an aqueous solution and\n"+\
            "an already associated surface species to complete that action"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
        return

    def _updateSurface(self, event):
        print "ok"
#
#       First we control that an aqueous state has been selected
#
        stateName = str(self.selectedState.GetValue()).replace(" ","")
        updateControl = None
        if stateName == "":
            wx.MessageDialog(self.parent, "you have to select an aqueous solution first\n"+\
            "before entering an surface species"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        surfaceName = str(self.selectedSurfaceSpecies.GetValue()).replace(" ","")
        print "&&&&&&&&&&&&&&&&&&\n",surfaceName
        print "&&&&&&&&&&&&&&&&&&\n",self.selectedSurfaceSpecies.GetValue()
        print "&&&&&&&&&&&&&&&&&&\n",self.ind
        if surfaceName == "":
            wx.MessageDialog(self.parent, "you have to select a surface species first\n"+\
            "before trying to update the list of surface species"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        self.surfaceSpeciesList = self.params.getParam(parameters.AqueousStates_SurfaceSpecies_list).getValue()
        self.surfacePropertiesList = self.params.getParam(parameters.AqueousStates_SurfaceSpecies_Properties_list).getValue()
        if surfaceName in self.surfaceSpeciesList[self.ind]:
            print "if ",self.ind
            surfaceInd =  self.surfaceSpeciesList[self.ind].index(surfaceName)
            self.surfacePropertiesList[self.ind][surfaceInd] =\
                              (str(self.molesAmount.GetValue()),0,str(self.specificAreaPerGram.GetValue()),0.)            
        else:
            print "else "
            self.surfaceSpeciesList[self.ind].append(surfaceName)
            self.surfacePropertiesList[self.ind].append((self.specificAreaPerGram.GetValue(),self.molesAmount.GetValue(),0))
        self.params.getParam(parameters.AqueousStates_SurfaceSpecies_list).setValue(self.surfaceSpeciesList)
        self.params.getParam(parameters.AqueousStates_SurfaceSpecies_Properties_list).setValue(self.surfacePropertiesList)
# we reinitialize the elements to leere Zeilen, the aqueous state bleibt, only the surface is reinitialised
        equiDescription = _surfaceToString(self.surfaceSpeciesList[self.ind],self.surfacePropertiesList[self.ind])
        self.surfaceState.SetValue(equiDescription)
        self.selectedSurfaceSpecies.SetItems(self.surfaceSpeciesList[self.ind])

    def _evtText(self, event):
        pass
        
    def _onOk(self, params):
# list of states by name:        
        params.getParam(parameters.AqueousStates_list).setValue(self.aqueousStateList)
# list of list  describing each state:        
        params.getParam(parameters.AqueousStates_Properties_list).setValue(self.apl_perstate)

        return True
        
def _surfaceToString(surfaceList,surfacePropertiesList):      
    a = ""
    for ind in range (0,len(surfaceList)):
        a+= str(surfaceList[ind]) + " " +\
            str(surfacePropertiesList[ind][0])
        if surfacePropertiesList[ind][1]:     
             + " "+str(surfacePropertiesList[ind][2]) + str(surfacePropertiesList[ind][3]) + "\n"
        else:
            a+= "\n"
    return a

