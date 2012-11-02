import wx

from geoi.actions.params_action import ParamsAction
from geoi.actions.GridCustTable import CustTableGrid
from geoi import parameters
from parameter import IS_ION, IS_POSITIVE_NUMBER, IS_NUMBER

description =\
       """ 
       To define exchange Species that can react with the aqueous phase. 
       """
HELP = """
       <html><body>
       You will be able to enter here the amounts of an assemblage of exchangers that can react reversibly
       with the aqueous phase. The initial composition of the exchange assemblage can be defined in two ways,
       <b>(1) <b>explicitely</b> by listing the composition of each exchange component or <b>(2)  implicitly</b>,
       by specifying that each exchanger is in equilibrium with a solution of fixed composition.
       You will have access here in an ""<b>user friendly</b>" way to the available exchanger list, database defined and user
       defined ones.<br>
       <b>CaX2</b> 0.3<br>
       <b>MgX2</b> 0.1<br>
       For further notes look at the phreeqC manual 99-4259 page 82

       </body></html>"""
class ExchangeDefinition(ParamsAction):
    """
    Enables the association of materials and aqueous states over the domain
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Exchange setup",description  =description,help=HELP)

    def _createInterface(self, parent, params):
        
        sizer = wx.BoxSizer( wx.VERTICAL )

# aqueous state control
   
        self.exchangeDescription = "you will discover here in a phreeqC written way\n"+\
                                   "the description in terms of amounts and composition\n"+\
                                   "of an assemblage of exchangers." 
        self.aqueousStateList = aqueousStateList = []
        self.parent = parent
        self.params = params
        self.apl_perstate = None
        self.equilibrium_phase = None
#        self.mpl_perstate = None
#        self.mppl_perstate = None
        self.exchangeSpeciesList = None
        self.exchangePropertiesList = None

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
        selectedState.SetValue("")
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
# choice of exchangers
#
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "exchanger association" ) , wx.HORIZONTAL)
#        box3.SetOwnFont(boldFont)
        box3.SetMinSize((600,50))

        
        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box31.SetMinSize((300,30))

        label1 = wx.StaticText(parent,-1,"Exchanger:",size=(80,-1));label1.SetTTS("Selected exchange assemblage")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.selectedExchangers = selectedExchangers = [""]
        self.selectedExchangeSpecies = selectedExchangeSpecies = \
        wx.ComboBox(parent, -1, "",(220, 20), (200, -1),selectedExchangers, wx.CB_DROPDOWN)
        toto.Bind(wx.EVT_COMBOBOX, self._selectedExchangeControl, selectedExchangeSpecies)

        box31.Add(selectedExchangeSpecies, 0., wx.ALIGN_CENTER|wx.ALL, 1)

        box3.Add(box31, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        box32 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box32.SetMinSize((250,20))
        
        self.dbExchangeSpeciesList = dbExchangeSpeciesList = params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getExchangeSpecies().keys()
        dbExchangeSpeciesList += params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getExchangeSpecies().keys()
        
        label2 = wx.StaticText(parent, -1, "D.B. Exchange S.:",size=(110,-1))
        label2.SetOwnFont(boldFont)
        label2.SetTTS("you define the exchanger composition through\navalaible exchange species within that one ")

        box32.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.exchangeComboMessage = "list of available exchange species: "
        exchangeComboboxDefault = ""
        self.availableExchangeCombo = availableExchangeCombo =\
        wx.ComboBox(parent, -1, exchangeComboboxDefault,(240, 20), (200, -1),dbExchangeSpeciesList, wx.CB_DROPDOWN)
        
        availableExchangeCombo.SetToolTipString("available exchange species based on those\nof the selected database\n and user defined ones")
        availableExchangeCombo.SetLabel("available exchange species")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedExchangeControl, availableExchangeCombo)
                                 
        box32.Add(availableExchangeCombo,0,wx.ALIGN_CENTER|wx.ALL, 1)


        box3.Add(box32, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

# initial guesses

        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Exchange definition" ) , wx.HORIZONTAL)
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
        molesAmount.SetTTS("available moles amount within\n the specified solution\nfor the exchange species considered")
        box22.Add(molesAmount, 0, wx.ALIGN_LEFT|wx.ALL, 1)
#
# exchange dependancy control
#
        box21 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box21.SetMinSize((450,20))
        grid2 = wx.FlexGridSizer( 0, 6, 0, 0 )
        grid2.SetFlexibleDirection( wx.HORIZONTAL)

        label2 = wx.StaticText(parent, -1, " Dependancy:");label1.SetTTS("If selected, the Exchange can not precipitate")
        label2.SetOwnFont(boldFont)
        grid2.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        self.dependancy = dependancy = wx.CheckBox(parent, -1, "    ")
        dependancy.SetValue(False)
        toto.Bind(wx.EVT_CHECKBOX, self._dependancy, dependancy)

        grid2.Add(dependancy, 1, wx.ALIGN_CENTRE|wx.ALL, 1)

        
        label1 = wx.StaticText(parent, -1, "Phase\nname:");label1.SetTTS("phase with attached exchange site")
        label1.SetOwnFont(boldFont)
        grid2.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.phase = phase = wx.TextCtrl(parent,-1, "",size=(150,-1))
        phase.SetTTS("name of the phase attached\n to the exchange site")
        phase.Enable(False)
        grid2.Add(phase, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.ratio = ratio = wx.TextCtrl(parent,-1, "0.0",size=(100,-1))
        ratio.SetTTS("ration of the phase attached\n to the exchange site is 0")
        ratio.Enable(False)
        grid2.Add(ratio, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
               
        box21.Add( grid2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        box2.Add( box21, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

        sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# exchange species definition
#
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "already associated exchange species " ) , wx.HORIZONTAL)
        box4.SetMinSize((600,100))

        self.exchangeState = exchangeState = wx.TextCtrl(parent, -1,"",
                       size=(300, 90), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        exchangeState.SetOwnFont(boldFont)
        exchangeState.SetForegroundColour("#1857DE")
	exchangeState.SetTTS(self.exchangeDescription)
        exchangeState.SetInsertionPoint(0)
        toto.Bind(wx.EVT_TEXT, self._evtText, exchangeState)
        
        box4.Add(exchangeState, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.update = update = wx.Button(parent, -1, "Update", (50,50))
        update.SetTTS("used to update the exchange species\nassociated to an aqueous state.\n")
        toto.Bind(wx.EVT_BUTTON, self._updateExchange, update)
        box4.Add(update, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        self.delete = delete = wx.Button(parent, -1, "Delete", (50,50))
        delete.SetTTS("used to delete the selected exchange species\n from the phase definition")
        toto.Bind(wx.EVT_BUTTON, self._deletePhase, delete)
        box4.Add(delete, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        sizer.Add(box4, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)
        
    def _dependancy(self, event):
        if event.IsChecked()==True:
            self.phase.Enable(True)
            self.ratio.Enable(True)
            return self.dependancy.SetValue(True)
        elif event.IsChecked()==False:
            self.phase.Enable(False)
            self.ratio.Enable(False)
            return self.dependancy.SetValue(False)
        
    def _selectedStateControl(self, event):
        selected = event.GetString()
        self.selectedState.SetValue(selected)
        self.ind = self.params.getParam(parameters.AqueousStates_list).getValue().index(selected)
# We get the already defined element, if any        
        self.exchangeSpeciesList = self.params.getParam(parameters.AqueousStates_ExchangeSpecies_list).getValue()
        print "238 selectedStateControl",self.exchangeSpeciesList,self.ind
        self.selectedExchangeSpecies.SetItems(self.exchangeSpeciesList[self.ind])
        self.exchangePropertiesList =\
            self.params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).getValue()
#
# We update the presentation of the exchange state
#
        if self.exchangeSpeciesList[self.ind] != []:
            equiDescription = _exchangeToString(self.exchangeSpeciesList[self.ind],self.exchangePropertiesList[self.ind])
        else:
            equiDescription = ""
        self.exchangeState.SetValue(equiDescription)
        self.selectedExchangeSpecies.SetValue("")
        self.phase.SetValue(str(0.0))
        self.molesAmount.SetValue(str(0.0))
        self.dependancy.SetValue(False)
 
    def _updateExchangeData(self,selected):
# update of the already available values
        print "  self.ind ",self.ind
        if self.ind == None:
            wx.MessageDialog(self.parent, "you have to select an aqueous solution before\n"+\
            "trying to complete that action"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            
            return None
        else:
            print " 256 ",str(selected),self.ind
            print " 256 ",self.exchangePropertiesList
            exchangeSpeciesName = str(selected)
            if exchangeSpeciesName in self.exchangeSpeciesList[self.ind]:
                indiz = self.exchangeSpeciesList[self.ind].index(exchangeSpeciesName)
                self.molesAmount.SetValue(self.exchangePropertiesList[self.ind][indiz][0])
                if self.exchangePropertiesList[self.ind][indiz][1] == 0:
                    self.dependancy.SetValue(False)
                else:
                    self.phase.SetValue(self.exchangePropertiesList[self.ind][indiz][2])
                    self.ratio.SetValue(self.exchangePropertiesList[self.ind][indiz][3])
                    self.dependancy.SetValue(True)
# we set to default values        
            else:
                print " 265",exchangeSpeciesName
                self.exchangeSpeciesList[self.ind].append(exchangeSpeciesName)
                if self.dependancy.GetValue():
                    check = 1
                    mineralName =  self.phase.GetValue()
                    mineralRatio = self.dependancy.GetValue()
                    print "debug 268 ",mineralName,mineralRatio
                else:
                    check = 0
                    mineralName = ""
                    mineralRatio = 0
                self.exchangePropertiesList[self.ind].append((self.molesAmount.GetValue(),check,\
                                                             mineralName,mineralRatio))
                self.phase.SetValue(str(0.0))
                self.molesAmount.SetValue(str(mineralName))
                self.dependancy.SetValue(False)
 
    def _selectedExchangeControl(self, event):
        selected = event.GetString()
        print "selected: ",selected,self.selectedState.GetValue()
        if self.selectedState.GetValue() != "":
            self.selectedExchangeSpecies.SetValue(selected)
            self._updateExchangeData(selected)
        else:
            wx.MessageDialog(self.parent, "you have to select an aqueous solution before\n"+\
            "trying to complete that action"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            

    def _deletePhase(self, event):
        selected = str(self.selectedExchangeSpecies.GetValue())
        if selected != "":
            ind = self.exchangeSpeciesList[self.ind].index(selected)
            del self.exchangeSpeciesList[self.ind][ind]
            del self.exchangePropertiesList[self.ind][ind]
            self.params.getParam(parameters.AqueousStates_ExchangeSpecies_list).setValue(self.exchangeSpeciesList)
            self.params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).setValue(self.exchangePropertiesList)
            
            equiDescription = _exchangeToString(self.exchangeSpeciesList[self.ind],self.exchangePropertiesList[self.ind])
            print "296 equiDescription: ",equiDescription
            self.exchangeState.SetValue(equiDescription)
            self.selectedExchange.SetValue("")
            self.selectedExchange.SetItems(self.exchangeSpeciesList[self.ind])
        else:
            wx.MessageDialog(self.parent, "you have to select an aqueous solution and\n"+\
            "an already associated exchange species to complete that action"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
        return

    def _updateExchange(self, event):
        print "ok"
#
#       First we control that an aqueous state has been selected
#
        stateName = str(self.selectedState.GetValue()).replace(" ","")
        updateControl = None
        if stateName == "":
            wx.MessageDialog(self.parent, "you have to select an aqueous solution first\n"+\
            "before entering an exchange species"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        exchangeName = str(self.selectedExchangeSpecies.GetValue()).replace(" ","")
        print "&&&&&&&&&&&&&&&&&&\n",exchangeName
        print "&&&&&&&&&&&&&&&&&&\n",self.selectedExchangeSpecies.GetValue()
        print "&&&&&&&&&&&&&&&&&&\n",self.ind
        if exchangeName == "":
            wx.MessageDialog(self.parent, "you have to select an exchange species first\n"+\
            "before trying to update the list of exchange species"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        self.exchangeSpeciesList = self.params.getParam(parameters.AqueousStates_ExchangeSpecies_list).getValue()
        self.exchangePropertiesList = self.params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).getValue()
        print "&&&&&&&&&&&&&&&&&&\n",self.exchangeSpeciesList[self.ind]
        if exchangeName in self.exchangeSpeciesList[self.ind]:
            print "if ",self.ind
            exchangeInd =  self.exchangeSpeciesList[self.ind].index(exchangeName)
            if self.dependancy.GetValue():
                self.exchangePropertiesList[self.ind][exchangeInd] =\
                              (str(self.molesAmount.GetValue()),1,str(self.phase.GetValue()),self.ratio.GetValue())
            else:
                self.exchangePropertiesList[self.ind][exchangeInd] =\
                              (str(self.molesAmount.GetValue()),0,"",0.)
                 
        else:
            print "else "
            self.exchangeSpeciesList[self.ind].append(exchangeName)
            if self.dependancy.GetValue():
                self.exchangePropertiesList[self.ind].append((self.molesAmount.GetValue(),1,self.phase.GetValue(),self.ratio.GetValue()))
            else:
                self.exchangePropertiesList[self.ind].append((self.molesAmount.GetValue(),0,"",0.))
            
        self.params.getParam(parameters.AqueousStates_ExchangeSpecies_list).setValue(self.exchangeSpeciesList)
        self.params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).setValue(self.exchangePropertiesList)
# we reinitialize the elements to leere Zeilen, the aqueous state bleibt, only the exchange is reinitialised
        equiDescription = _exchangeToString(self.exchangeSpeciesList[self.ind],self.exchangePropertiesList[self.ind])
        self.exchangeState.SetValue(equiDescription)
        self.selectedExchangeSpecies.SetItems(self.exchangeSpeciesList[self.ind])

    def _evtText(self, event):
        pass
        
    def _onOk(self, params):
# list of states by name:        
        params.getParam(parameters.AqueousStates_ExchangeSpecies_list).setValue(self.exchangeSpeciesList)
# list of list  describing each state:        
        params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).setValue(self.exchangePropertiesList)

        return True
        
def _exchangeToString(exchangeList,exchangePropertiesList):      
    a = ""
    for ind in range (0,len(exchangeList)):
        a+= str(exchangeList[ind]) + " " +\
            str(exchangePropertiesList[ind][0])
        if exchangePropertiesList[ind][1]:     
             + " "+str(exchangePropertiesList[ind][2]) + str(exchangePropertiesList[ind][3]) + "\n"
        else:
            a+= "\n"
    return a

