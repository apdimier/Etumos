import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters
from parameter import IS_ION, IS_POSITIVE_NUMBER, IS_NUMBER, IS_UNIT
from geoi.actions.pywrite import *
import os
description =\
       """ 
       To define the aqueous state to be studied 
       """
HELP = """
       <html><body>
       You will be able to enter here <b>temperature</b>,<br> the <b>pH</b>, the <b>pe</b>
       pH can be adjusted to achieve charge balance. If <b>charge</b> is specified for pH, it may
       not be specified for any other element<br>
       You cans naturally introduce ions distribution within the solution as within the phreeqC solution keyword:<br>
       Ca 1<br>
       Na 10<br>
       K 1.0e-3<br>
       You can also introduce the <b>unit</b> keyword and any supported unit definition on a single line.<br>
       After validation, it will be replaced by molalities and units adjusted ion concentrations.<br>
       For further notes look at the phreeqC manual 99-4259 page 149
       </body></html>"""
class AqueousStatesDefinition(ParamsAction):
    """
    Enables the association of materials and aqueous states over the domain
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Aqueous States setup",description  =description,help=HELP)
        self.radios = None
        self.choice = None
        self.cc = None

    def _createInterface(self, parent, params):
        
        sizer = wx.BoxSizer( wx.VERTICAL )

# aqueous state control
   
        self.aqueousStateDescription = aqueousStateDescription = ""
        self.aqueousStateList = aqueousStateList = []
        self.parent = parent
        self.params = params
        self.apl_perstate = None
        self.asl_perstate = None
        #print " aqueous parameters ",self.params.getParam(parameters.AqueousStates_Properties_list).getValue()
        toto = self.GetDialogPanel()
        wx.TextCtrl.SetTTS = wx.TextCtrl.SetToolTipString
        wx.StaticText.SetTTS = wx.StaticText.SetToolTipString
        wx.CheckBox.SetTTS = wx.CheckBox.SetToolTipString
        wx.Button.SetTTS = wx.Button.SetToolTipString
#        points = t4.GetFont().GetPointSize()  # get the current size
        f = wx.Font(10, wx.ROMAN, wx.ITALIC, wx.BOLD, True)
        boldFont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")
#        t4.SetStyle(63, 77, wx.TextAttr("BLUE", wx.NullColour, f))
        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Aqueous state control" ) , wx.HORIZONTAL)
        box1.SetMinSize((600,30))
        grid1 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid1.SetFlexibleDirection( wx.HORIZONTAL)
# selected aqueous state
        self.selected = selected = wx.TextCtrl(parent, -1, "", size=(200,-1));selected.SetTTS("aqueous state to define or update")
        selected.SetValue( "" )
        grid1.Add(selected, 1, wx.ALIGN_CENTRE|wx.ALL, border = 1)
        grid1.AddSpacer(15)
 
        self.aqueousStateList = params.getParamValue(parameters.AqueousStates_list)
        self.stateComboMessage = stateComboMessage = "list of already defined\naqueous states: "
        if aqueousStateList == []:
            comboboxDefault = ""
            stateComboMessage+="[]"
        else:
            comboboxDefault = aqueousStateList[0]
            for st in self.aqueousStateList: stateComboMessage+="\n"+st
        self.selectedStateCombo = selectedStateCombo = wx.ComboBox(parent, -1, comboboxDefault,
                                 (250, 20), (200, -1),
                                 self.aqueousStateList, wx.CB_DROPDOWN)
        selectedStateCombo.SetToolTipString(stateComboMessage)
        selectedStateCombo.SetLabel("Aqueous states")
                                 
        grid1.Add(selectedStateCombo,0,wx.LEFT|wx.ALL, 1)
        toto.Bind(wx.EVT_COMBOBOX, self._selectedStateControl, selectedStateCombo)

        box1.Add( grid1, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#        
# ph and pe control
#
        self.pHRadios = pHRadios = []
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box3.SetMinSize((600,50))
#
# pH control
#        
        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "pH Control" ) , wx.HORIZONTAL)
        box31.SetMinSize((300,30))
        
        label1 = wx.StaticText(parent, -1, "Fixed:",size=(40,-1))
        label1.SetTTS("you fix the pH by introducing\n an acid or a base")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.pHControl = pHControl = wx.CheckBox( parent, -1, "",style = 0)
        pHControl.SetTTS("used to fix the pH ")
        box31.Add(pHControl, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        toto.Bind(wx.EVT_CHECKBOX, self._pHControl, pHControl)
        pHRadios.append(pHControl)

        label2 = wx.StaticText(parent, -1, "charge:",size=(50,-1))
        label2.SetTTS("you fix the pH by introducing\n an acid or a base")
        label2.SetOwnFont(boldFont)
        box31.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)
#
# Indicates pH is to be adjusted to achieve charge balance. If charge is specified for pH, it may
# not be specified for any other element. That means chargeControl and chargeBalancecontrol exclude each other.
#
        self.chargeControl = chargeControl = wx.CheckBox( parent, -1, "",style = 0)
        chargeControl.SetTTS("used to reach nul charge ")
        box31.Add(chargeControl, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        toto.Bind(wx.EVT_CHECKBOX, self._chargeControl, chargeControl)
        pHRadios.append(chargeControl)

        self.moles = moles = wx.TextCtrl(parent, -1,"",size=(50,-1))
        moles.SetTTS("available mole quantity\nto reach equilibrium")
        moles.Enable(False)
        box31.Add(moles, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        label2 = wx.StaticText(parent, -1, "moles of:",size=(55,-1))
        label2.SetTTS("you fix the pH by introducing\n an acid or a base")
        label2.SetOwnFont(boldFont)
        box31.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.ion = ion = wx.TextCtrl(parent, -1,"",size=(50,-1));ion.SetTTS("ion to be introduced")
        ion.Enable(False);
        box31.Add(ion, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        box3.Add(box31, 0, wx.ALIGN_LEFT|wx.ALL, 1)
#
# charge control
#        
#
# p. 151 of the phreeqC manual
#
# Indicates the concentration of this element will be adjusted to achieve charge balance. The element
# must have ionic species. If charge is specified for one element, it may not be specified for
# pH or any other element.
#
        box32 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "charge control" ) , wx.HORIZONTAL)
        box32.SetMinSize((250,20))
       
        label1 = wx.StaticText(parent, -1, "Elec. balance:",size=(100,-1))
        label1.SetTTS("you reach charge balance by introducing\n an element having ionic species")
        label1.SetOwnFont(boldFont)
        box32.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.chargeBalanceControl = chargeBalanceControl = wx.CheckBox( parent, -1, "",style = 0)
        chargeBalanceControl.SetTTS("used to reach nul charge ")
        box32.Add(chargeBalanceControl, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        toto.Bind(wx.EVT_CHECKBOX, self._chargeBalanceControl, chargeBalanceControl)
        pHRadios.append(chargeBalanceControl)

        self.cbmoles = cbmoles = wx.TextCtrl(parent, -1,"",size=(50,-1));
        cbmoles.SetTTS("available element quantity\nto reach charge balance")
        cbmoles.Enable(False)
        box32.Add(cbmoles, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        label2 = wx.StaticText(parent, -1, "moles of:",size=(55,-1))
        label2.SetTTS("you fix the pH by introducing\n an acid or a base")
        label2.SetOwnFont(boldFont)
        box32.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.cbion = cbion = wx.TextCtrl(parent, -1,"",size=(50,-1));cbion.SetTTS("element to be introduced\nto reach charge balance")
        cbion.Enable(False);
        box32.Add(cbion, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        box3.Add(box32, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

# initial guesses

        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Initial guess values" ) , wx.HORIZONTAL)
        box2.SetMinSize((300,20))
        box21 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box21.SetMinSize((300,20))
        grid2 = wx.FlexGridSizer( 0, 6, 0, 0 )
        grid2.SetFlexibleDirection( wx.HORIZONTAL)
        
        label1 = wx.StaticText(parent, -1, "pH:");label1.SetTTS("pH labelling help")
        label1.SetOwnFont(boldFont)
        grid2.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        currentpH = str(params.getParam(parameters.AqueousStates_Default_pH)) 
        self.pH = pH = wx.TextCtrl(parent, -1, currentpH, size=(70,-1));pH.SetTTS("default pH is 7")
        pH.SetValue( str(params.getParam(parameters.AqueousStates_Default_pH).getValue()))
        pH.Enable(True)
        grid2.Add(pH, 1, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        self.pHInitialGuess = pHInitialGuess = wx.CheckBox(parent, -1, "    ") ;pHInitialGuess.SetValue(True)
        toto.Bind(wx.EVT_CHECKBOX, self._pHInitialGuess, pHInitialGuess)
        
        grid2.Add(pHInitialGuess, 1, wx.ALIGN_CENTRE|wx.ALL, 1)
               
        label2 = wx.StaticText(parent, -1, "pe:")
        label2.SetHelpText("pe labelling help")
        label2.SetOwnFont(boldFont)

        grid2.Add(label2, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        currentpe = str(params.getParam(parameters.AqueousStates_Default_pe))
        self.pe = pe = wx.TextCtrl(parent, -1, currentpe, size=(70,-1));pe.SetTTS("pe default value is 4 ")
        pe.SetValue( str(params.getParam(parameters.AqueousStates_Default_pe).getValue()) )
        pe.Enable(False)
        grid2.Add(pe, 1, wx.ALIGN_CENTRE|wx.ALL, 2)

        self.peControl = peControl = wx.CheckBox(parent, -1, "    ")
        toto.Bind(wx.EVT_CHECKBOX, self._peInitialGuess, peControl)
        grid2.Add(peControl, 1, wx.ALIGN_CENTRE|wx.ALL, 1)
               
        box21.Add( grid2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        box2.Add( box21, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
#Temperature control
#
        box22 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box2.Add( box22, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        box22.SetMinSize((300,20))
        label221 = wx.StaticText(parent, -1, "  Temperature:  ")
        label221.SetTTS("temperature labelling help")
        label221.SetOwnFont(boldFont)
        box22.Add(label221, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        currentTemperature = str(params.getParam(parameters.AqueousStates_Default_Temperature)) 
        self.temperature = temperature = wx.TextCtrl(parent, -1, currentTemperature, size=(50,-1))
        temperature.SetTTS("default temp is of 25 Celcius degree")
        temperature.SetValue( str(params.getParam(parameters.AqueousStates_Default_Temperature).getValue()))
        temperature.Enable(True)
        box22.Add(temperature, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        label222 = wx.StaticText(parent, -1, "Celcius  ");label1.SetTTS("")
        label222.SetOwnFont(boldFont)
        box22.Add(label222, 0, wx.ALIGN_CENTRE|wx.ALL, 1)

        sizer.Add( box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# Aqueous state definition
#
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Aqeous state definition" ) , wx.HORIZONTAL)
        box4.SetMinSize((600,100))

        self.aqueousState = aqueousState = wx.TextCtrl(parent, -1,"",
                       size=(300, 90), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        aqueousStateDescription = "list of elements, each element followed by its concentration.\n"+\
                                  "Concentrations can only be expressed in mmol/l or mol/l; mol/l being the default one."+\
                                  "Only a single concentration unit can be entered,\nimplying an automatic conversion"+\
                                  "in the default unit."
	aqueousState.SetTTS(aqueousStateDescription)
        aqueousState.SetForegroundColour("#1857DE")	
        aqueousState.SetInsertionPoint(0)
        aqueousState.SetOwnFont(boldFont)
        toto.Bind(wx.EVT_TEXT, self._evtText, aqueousState)
#        toto.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, aqueousState)
        
        box4.Add(aqueousState, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.create = create = wx.Button(parent, -1, "Create", (50,50));create.SetTTS("used to create an aqueous state.\n")
        toto.Bind(wx.EVT_BUTTON, self._createState, create)
        box4.Add(create, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        self.equilibrate = equilibrate = wx.Button(parent, -1, "Equilibrate", (50,50))
        equilibrate.SetTTS("used to get the equilibrium.")
        box4.Add(equilibrate, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        toto.Bind(wx.EVT_BUTTON, self._equilibrate, equilibrate)
        sizer.Add(box4, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)

    def _selectedStateControl(self, event):
        selected = event.GetString()
        print " self.selected",self.selected
        self.selected.SetValue(selected)
        ind = self.params.getParam(parameters.AqueousStates_list).getValue()
#        print " liste of states:",ind
#        print " liste des proprietes ",self.params.getParam(parameters.AqueousStates_Properties_list).getValue()
        ind = self.params.getParam(parameters.AqueousStates_list).getValue().index(selected)
        print " getselected",ind
#        print " parameters.AqueousStates_Properties_list:     ",parameters.AqueousStates_Properties_list
        a = self.params.getParam(parameters.AqueousStates_Properties_list).getValue()[ind]
        print "toto ",type(a),a
        print "toto ",type(a),a[0]
        b = _aqueousToString(self.params.getParam(parameters.AqueousStates_Species_list).getValue()[ind])
        self.aqueousState.SetValue(b)
        if self.pe.IsEnabled():
            self.pe.SetValue(a[2][1])
        self.pe.SetValue(a[2][1])
        self.pH.SetValue(a[0][1])

        self.temperature.SetValue(a[1][1])
#
# That par could be simplified, but would necesitate the modification of the GUI data model aqueousstatepropertieslist
#        
        if a[3][0] == "0":    # no pH control, no pH charge, no pe default control
            self.pHControl.SetValue(False);self.moles.Enable(False);self.ion.Enable(False)
            self.chargeControl.SetValue(False)
            self.peControl.SetValue(False)
        elif a[3][0] == "1":  # pH control: pH fixed, no pH charge, no pe default control
            self.peControl.SetValue(False)
            self.pHControl.SetValue(True);self.moles.SetValue(a[3][1][0]);self.moles.Enable(True)
            self.ion.SetValue(a[3][1][1]);self.ion.Enable(True)
            self.chargeControl.SetValue(False)
        elif a[3][0] == "2":  # pH control: no pH fixed, pH charge, no pe default control
            self.pHControl.SetValue(False);self.moles.Enable(False);self.ion.Enable(False)
            self.peControl.SetValue(False)
            self.chargeControl.SetValue(True)
        elif a[3][0] == "5":    # no pH control, no pH charge, pe default control
            self.pHControl.SetValue(False);self.moles.Enable(False);self.ion.Enable(False)
            self.chargeControl.SetValue(False)
            self.peControl.SetValue(True);self.pe.SetValue(a[2][1]);self.pe.Enable(True)
        elif a[3][0] == "3":  # pH control: pH fixed, no pH charge, and pe default control
            self.peControl.SetValue(True);self.pe.SetValue(a[2][1]);self.pe.Enable(True)
            self.pHControl.SetValue(True)
            self.moles.SetValue(a[3][1][0]);self.moles.Enable(True)
            self.ion.SetValue(a[3][1][1]);self.ion.Enable(True)
            self.chargeControl.SetValue(False)
        elif a[3][0] == "4":  # pH control: no pH fixed, pH charge and pe default control 
            self.pHControl.SetValue(False);self.moles.Enable(False);self.ion.Enable(False)
            self.chargeControl.SetValue(True)
            self.peControl.SetValue(True);self.pe.SetValue(a[2][1]);self.pe.Enable(True)
        if a[4][0] == "0":    # no charge control
            self.chargeBalanceControl.SetValue(False)
            self.cbmoles.SetValue(a[4][1][0]);self.cbmoles.Enable(False)
            self.cbion.SetValue(a[4][1][1]);self.cbion.Enable(False)
        else:                 # charge control
            self.chargeBalanceControl.SetValue(True)
            self.cbmoles.SetValue(a[4][1][0]);self.cbmoles.Enable(True)
            self.cbion.SetValue(a[4][1][1]);self.cbion.Enable(True)

    def _state(self,stateList, ionList,concList):
        stateList
        ind = 0
        for i in ionList: 
            stateList.append([i,concList[ind]])
            ind+=1
        return stateList 

    def _createState(self, event):
        name = str(self.selected.GetValue()).replace(" ","")
        creationControl = None
        if name == "":
            wx.MessageDialog(self.parent, "give a name to the aqueous state"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        elif name in self.aqueousStateList:
            creationControl = self.aqueousStateList.index(name)
            pass
        else:
            self.aqueousStateList.append(name)
        print " creation control value ",  creationControl
        print " self.aqueousStateList",self.aqueousStateList,type(self.aqueousStateList[0]),self.aqueousStateList[0]
        self.params.getParam(parameters.AqueousStates_list).setValue(self.aqueousStateList)
            
        stateList = [["pH",str(self.pH.GetValue())],["T",str(self.temperature.GetValue())]]
        if self.pe.IsEnabled():
            stateList.append(["pe",str(self.pe.GetValue())])
        else:
            stateList.append(["pe","4"])
#
# pH control
#        
        if self.pHControl.GetValue() == False:
            if self.chargeControl.GetValue() == True:
                if self.peControl.GetValue() == False:
                    stateList.append(["2",("","")])
                else:
                    stateList.append(["5",("","")])                
            else:
                if self.peControl.GetValue() == False:
                    stateList.append(["0",("","")])
                else:
                    stateList.append(["4",("","")])
        else:
            if self.peControl.GetValue() == False:
                stateList.append(["1",(str(self.moles.GetValue()),str(self.ion.GetValue()))])
            else:
                stateList.append(["3",(str(self.moles.GetValue()),str(self.ion.GetValue()))])
#
# pH control
#            
        if self.chargeBalanceControl.GetValue() == False:
            stateList.append(["0",("","")])
        else:
            stateList.append(["1",(str(self.cbmoles.GetValue()),str(self.cbion.GetValue()))])
            
        a = str(self.aqueousState.GetValue())
        concList = filter(lambda x: IS_POSITIVE_NUMBER(x), a.split())
        print " ionList ",concList
        ionList = filter(lambda x: IS_ION(x), a.split())
        print " concList ",ionList
        unitList = filter(lambda x: x in ["mol/l","moles/l","mmol/l","mmoles/l"], a.split())
        if len(ionList) != len(concList): 
            message = "check your definition of the aqueous state,\nespecially, the ion distribution.\n"\
            +"look eventually at the html documentation"
            wx.MessageDialog(self.parent, message, "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        else:
            if len(unitList) >1:
                message = "a unique unit statement should be entered, mol/l or mmol/l, mol/l being the default moles/l or mmoles/l are ok"
                wx.MessageDialog(self.parent, message, "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            
            else:
                if unitList != []:
                    if unitList[0].lower() in ["mmol/l","mmoles/l"]:
                        for i in range(len(concList)):
                            print i
                            concList[i] = str(float(concList[i])*0.001)
                    elif unitList[0].lower() not in ["mmol/l","mmoles/l"]:
                        message = "check the unit,\nit should be one of the following:\nmol/l, mmol/l, moles/l or mmoles/l"
                        wx.MessageDialog(self.parent, message, "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
                
                self.stateTupleList = stateTupleList = []
                stateTupleList = self._state(stateTupleList,ionList,concList)

        print " 261",str(self.selected.GetValue())
#
# We retrieve from the base the elements already created
#
        self.apl_perstate = self.params.getParam(parameters.AqueousStates_Properties_list).getValue()
        self.asl_perstate = self.params.getParam(parameters.AqueousStates_Species_list).getValue()
        self.mpl_perstate = self.params.getParam(parameters.AqueousStates_MineralPhases_list).getValue()
        self.mppl_perstate = self.params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).getValue()
        self.exl_perstate = self.params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).getValue()
        self.expl_perstate = self.params.getParam(parameters.AqueousStates_ExchangeSpecies_list).getValue()
        self.sul_perstate = self.params.getParam(parameters.AqueousStates_SurfaceSpecies_list).getValue()
        self.supl_perstate = self.params.getParam(parameters.AqueousStates_SurfaceSpecies_Properties_list).getValue()
        print "AqueousStates_MineralPhases_list ",self.mpl_perstate
        print "AqueousStates_MineralPhases_Properties_list ",self.mppl_perstate
        print "AqueousStates_ExchangeSpecies_list ",self.exl_perstate
        print "AqueousStates_SurfaceSpecies_list ",self.sul_perstate
        print " from get value ",a
        
        print " updating of aqueous state properties list ",stateTupleList
        if creationControl == None:
            self.apl_perstate.append(stateList)
            self.asl_perstate.append(stateTupleList)
            self.mpl_perstate.append([])
            self.mppl_perstate.append([])
            self.exl_perstate.append([])
            self.expl_perstate.append([])
            self.sul_perstate.append([])
            self.supl_perstate.append([])
        else:
            print " here my dear creation control ",creationControl
            print " here my dear stateTupleList:  ",stateTupleList
            print " here my dear stateList:  ",stateList
            print type(self.apl_perstate),len(self.apl_perstate),self.apl_perstate,creationControl
            self.apl_perstate[creationControl] = stateList
            self.asl_perstate[creationControl] = stateTupleList
        
        self.params.getParam(parameters.AqueousStates_Species_list).setValue(self.asl_perstate)
        self.params.getParam(parameters.AqueousStates_Properties_list).setValue(self.apl_perstate)
        
        self.params.getParam(parameters.AqueousStates_MineralPhases_list).setValue(self.mpl_perstate)
        self.params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).setValue(self.mppl_perstate)
        self.params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).setValue(self.exl_perstate)
        self.params.getParam(parameters.AqueousStates_ExchangeSpecies_list).setValue(self.expl_perstate)
        self.params.getParam(parameters.AqueousStates_SurfaceSpecies_list).setValue(self.sul_perstate)
        self.params.getParam(parameters.AqueousStates_SurfaceSpecies_Properties_list).setValue(self.supl_perstate)
        
        a = self.params.getParam(parameters.AqueousStates_Properties_list).getValue()
#        if creationControl == None: self.selectedStateCombo.SetItems(self.aqueousStateList)
        self.selectedStateCombo.SetItems(self.aqueousStateList)
        self.selected.SetValue("")
        self.aqueousState.SetValue("")
        self.pH.SetValue( str(self.params.getParam(parameters.AqueousStates_Default_pH).getValue()))
        self.pH.Enable(True)
        self.pe.SetValue(str(self.params.getParam(parameters.AqueousStates_Default_pe).getValue()))
        self.pe.Enable(False)
        self.temperature.SetValue(str(self.params.getParam(parameters.AqueousStates_Default_Temperature).getValue()))
        print " list of states ",a
        self.comboMessage = "list of already defined\naqueous states: "
        for st in self.aqueousStateList: self.comboMessage+= "\n    - "+st
        self.selectedStateCombo.SetToolTipString(self.comboMessage)

    def _evtText(self, event):
        pass
#        print 'EvtText: %s\n' % event.GetString()

    def _pHInitialGuess( self, event ):
        if event.IsChecked()==True:
            self.moles.Enable(False)
            self.ion.Enable(False)
            for cB in self.pHRadios:
                cB.SetValue(False)
            return self.pH.Enable(True)
        else:
            self.pH.Enable(False)
        
    def _pHControl( self, event ):
        if event.IsChecked()==True:
            self.moles.Enable(True)
            self.ion.Enable(True)
            self.pHInitialGuess.SetValue(False)
            self.pHRadios[1].SetValue(False)
            self.pH.Enable(True)
            self.pHInitialGuess.SetValue(True)
        else:
            self.moles.Enable(False)
            self.ion.Enable(False)
            self.pH.Enable(False)
            self.pHInitialGuess.SetValue(False)
        
    def _chargeControl( self, event ):
        if event.IsChecked()==True:
            self.moles.Enable(False)
            self.ion.Enable(False)
            self.pHInitialGuess.SetValue(False)
            self.pHRadios[0].SetValue(False)
            self.chargeBalanceControl.SetValue(False)
            self.cbmoles.Enable(False)
            self.cbion.Enable(False)
            self.pH.Enable(True)
        else:
            self.pH.Enable(False)
        
    def _peInitialGuess( self, event ):
        if event.IsChecked()==True: return self.pe.Enable(True)
        return self.pe.Enable(False)
        
    def _chargeBalanceControl( self, event ):
        if event.IsChecked()==True:
            self.cbmoles.Enable(True)
            self.cbion.Enable(True)
            self.pHRadios[1].SetValue(False)
        else:
            self.cbmoles.Enable(False)
            self.cbion.Enable(False)
            return self.pe.Enable(False)
        
    def _onOk(self, params):
# list of states by name:        
        params.getParam(parameters.AqueousStates_list).setValue(self.aqueousStateList)
# list of list  describing each state:        
        if self.asl_perstate!=None:
            params.getParam(parameters.AqueousStates_Species_list).setValue(self.asl_perstate)
        if self.apl_perstate!=None:
            params.getParam(parameters.AqueousStates_Properties_list).setValue(self.apl_perstate)
#AqueousStates_Species_list

        return True
        
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
        
    def _equilibrate(self,event):
    
        studyName = self.selectedStateCombo.GetValue()
        if studyName == "":
            wx.MessageDialog(self.parent, "select an aqueous state\nbefore trying equilibrium"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        
        print " dbg aqueous_state.py equilibrate ",studyName
        dataBase = self.params.getParam(parameters.Available_Databases_list).getValue()[0]
        chemicalCase = open (studyName+".py",'w')
        chemicalCase.write("from chemistry import *\n")
        chemicalCase.write("from chemicalmodule import *\n")
        chemicalCase.write("from phreeqc import *\n")

        chemicalCase.write("\n")

        chemicalCase.write("Phreeqc_file = \""+studyName+".txt\"      # bounded to Phreeqc\n")
        chemicalCase.write("ProblemName  = \""+studyName+"\"          # Phreeqc file \n")
#
# writing the mesh extension
#
        chemicalCase.write("#~~~~~~~~~~~~~~~~~~~\n")
        chemicalCase.write("# Chemical Addenda ~\n")
        chemicalCase.write("#~~~~~~~~~~~~~~~~~~~\n")
        chemicalCase.write("speciesAddenda = []\n")
#
# solution master species
#        
        ams = self.params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSolutionMasterSpecies()
        for i in ams.keys() :
            print " debug element ",ams[i]['ELEMENT']
            string = _strHandlung(str(i)) + " = AqueousMasterSpecies("
            length = len(string)
            string += "symbol = \""+ ams[i]['SPECIES']+"\",\\\n"
            chemicalCase.write(string)
            string = " "*length + "name = \""+ ams[i]['ELEMENT']+"\",\\\n"
            chemicalCase.write(string)
            string = " "*length + "element = \""+ ams[i]['FORMULA']+"\",\\\n"
            chemicalCase.write(string)
            string = " "*length + "molarMass = MolarMass("+ str(ams[i]['GFW'])+",\"g/mol\"),\\\n"
            chemicalCase.write(string)
            string = " "*length + "alkalinity = "+ str(ams[i]['LOGK'])+")\n"
            chemicalCase.write(string)
            chemicalCase.write("speciesAddenda.append("+_strHandlung(str(i))+")\n")
#
# solution secondary species
#        
        ass = self.params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSolutionSecondarySpecies()
        for i in ass.keys() :
            string = _strHandlung(i) + "SSp = AqueousSecondarySpecies("
            length = len(string)
            string += "symbol = \""+ ass[i]['FORMULA']+"\",\\\n"
            chemicalCase.write(string)
            #equation = ass[i]['EQUATION']
            #string = " "*length + "formationReaction = ["+ str(ass[i]['LOGK'])+",\\\n"
            #chemicalCase.write(string)
            tlist = ""
            print " equatio ",ass[i]['EQUATION']
            print " equatio ",ass[i]['EQUATION'].split(" ")
            a = str(ass[i]['EQUATION']).split(" ")
            print " a split ",a
            print "ass[i]['FORMULA']",ass[i]['FORMULA']
            ind0 = a.index("=")
            print " a ind ",a[ind0],ind0
            print " a ind ",a[ind0:]
            liste = []
            b = a[ind0+1:]
            ind = b.index(ass[i]['FORMULA'])
            print " a ind 1",ind,a[ind+1]

            a.remove(a[ind0+ind+1])
            print " a dbg ",a
            dig = 1
            for el in a:
                if el.isdigit():
                    dig = el
                elif el not in ["+","-","=",""]:
                    if a.index(el) > ind0:
                        print "dig",dig
                        digi = dig
                        dig = "-"+str(digi)
                        liste.append((el,dig))
                    else:
                        liste.append((el,dig))
                    dig = 1        
            print liste
            for el in liste:
                tlist += "(\""+el[0]+"\","+str(el[1])+"),"
            tlist = tlist[0:-1]
            print " tlist ",tlist
            string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
            chemicalCase.write(string)
            string = " "*length + "logK25 = "+ str(ass[i]['LOGK'])+",\\\n"
            chemicalCase.write(string)
            string = " "*length + "name = \""+ ass[i]['ELEMENT']+"\",)\n"
            chemicalCase.write(string)
            chemicalCase.write("speciesAddenda.append("+_strHandlung(i)+"SSp)\n")
#
# exchange master species
#            
        exms = self.params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getExchangeMasterSpecies()
        for i in exms.keys() :
            string = str(i) + " = SorbingSiteMasterSpecies("
            string += "symbol = \"" + exms[i]['FORMULA']+"\","
            string += "name   = \"" + str(exms[i]['NAME'])+"\")\n"
            chemicalCase.write(string)
            chemicalCase.write("speciesAddenda.append("+str(i)+")\n")
#
# exchange species
#            
        exs = self.params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getExchangeSpecies()
        for i in exs.keys():
            if i not in exms.keys(): continue
            if str(i)[-1] == "-":
                stresp = str(i)[0:-1]+"m"
                string = stresp + "ESp = SorbedSecondarySpecies("
            else:
                stresp = str(i)[0:]
                string = stresp + "ESp = SorbedSecondarySpecies("
           
            length = len(string)
            string += "symbol = \""+ exs[i]['FORMULA']+"\",\\\n"
            chemicalCase.write(string)
            #equation = exs[i]['EQUATION']
            #string = " "*length + "formationReaction = ["+ str(exs[i]['LOGK'])+",\\\n"
            #chemicalCase.write(string)
            tlist = ""
                
            a = str(exs[i]['EQUATION']).split(" ")
            liste = []
            ind = a.index("=")
            a.remove(a[ind+1])
            dig = 1
            for el in a:
                if el.isdigit():
                    dig = el
                elif el not in ["+","-","=",""]:
                    if a.index(el) > ind:
                        print "dig",dig
                        digi = dig
                        dig = "-"+str(digi)
                        liste.append((el,dig))
                    else:
                        liste.append((el,dig))
                    dig = 1        
            for el in liste:
                tlist += "(\""+el[0]+"\","+str(el[1])+"),"
            tlist = tlist[0:-1]
            string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
            chemicalCase.write(string)
            string = " "*length + "logK25 = "+ str(exs[i]['LOGK'])+",\\\n"
            chemicalCase.write(string)
            string = " "*length + "name = \""+ exs[i]['ELEMENT']+"\",)\n"
            chemicalCase.write(string)
            chemicalCase.write("speciesAddenda.append("+stresp+"ESp)\n")

        for i in exs.keys():
            if i in exms.keys(): continue
            if str(i)[-1] == "-":
                stresp = str(i)[0:-1]+"m"
                string = stresp + "ESp = SorbedSecondarySpecies("
            else:
                stresp = str(i)[0:]
                string = stresp + "ESp = SorbedSecondarySpecies("
           
            length = len(string)
            string += "symbol = \""+ exs[i]['FORMULA']+"\",\\\n"
            chemicalCase.write(string)
            #equation = exs[i]['EQUATION']
            #string = " "*length + "formationReaction = ["+ str(exs[i]['LOGK'])+",\\\n"
            #chemicalCase.write(string)
            tlist = ""
                
            a = str(exs[i]['EQUATION']).split(" ")
            liste = []
            ind = a.index("=")
            a.remove(a[ind+1])
            dig = 1
            for el in a:
                if el.isdigit():
                    dig = el
                elif el not in ["+","-","=",""]:
                    if a.index(el) > ind:
                        print "dig",dig
                        digi = dig
                        dig = "-"+str(digi)
                        liste.append((el,dig))
                    else:
                        liste.append((el,dig))
                    dig = 1        
            for el in liste:
                tlist += "(\""+el[0]+"\","+str(el[1])+"),"
            tlist = tlist[0:-1]
            string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
            chemicalCase.write(string)
            string = " "*length + "logK25 = "+ str(exs[i]['LOGK'])+",\\\n"
            chemicalCase.write(string)
            string = " "*length + "name = \""+ exs[i]['ELEMENT']+"\",)\n"
            chemicalCase.write(string)
            chemicalCase.write("speciesAddenda.append("+stresp+"ESp)\n")
#
# mineral species
#
        ePhases = self.params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getMineralPhases()
        for i in ePhases.keys() :
            print " ~~~~~~~~~~~~~~~~~~~~~\nmineral species ",i,_strHandlung(i)
            elementName = _strHandlung(i)
            elementName = elementName.replace("(","").replace(")","")
                
            string = elementName + "Ad = MineralSecondarySpecies("
            length = len(string)
            string += "symbol = \""+ ePhases[i]['FORMULA']+"\",\\\n"
            chemicalCase.write(string)
                #equation = ass[i]['EQUATION']
                #string = " "*length + "formationReaction = ["+ str(ass[i]['LOGK'])+",\\\n"
                #chemicalCase.write(string)
            tlist = ""
            #
            # some users type blanks at the beginning of the equation "
            #
            ind = 0
            while ePhases[i]['EQUATION'][ind] in [" ","+","-"]:
                print " il y a un blan "
                ind+=1
            #    
            a = str(ePhases[i]['EQUATION'][ind:]).split(" ")[1:]
            print ' a ',a
            liste = []
            ind = a.index("=")
            dig = 1
            for el in a:
                if el.isdigit():
                    dig = el
                elif el not in ["+","-","=",""]:
                    if a.index(el) < ind:
                        print "dig",dig
                        digi = dig
                        dig = "-"+str(digi)
                        liste.append((el,dig))
                    else:
                        liste.append((el,dig))
                    dig = 1        
            print "liste",liste
            for el in liste:
                tlist += "(\""+el[0]+"\","+str(el[1])+"),"
            tlist = tlist[0:-1]
            print " tlist ",tlist
            string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
            chemicalCase.write(string)
            string = " "*length + "logK25 = "+ str(ePhases[i]['LOGK'])+",\\\n"
            chemicalCase.write(string)
            string = " "*length + "name = \""+ ePhases[i]['NAME']+"\",\\\n"
            if str(ePhases[i]['DENSITY']) == "":  
                string = string[0:-3] + ")\n"
            else:
                string +=" "*length + "density = Density("+ str(ePhases[i]['DENSITY'])+",\"kg/m**3\"))\n"
                
            chemicalCase.write(string)
            chemicalCase.write("speciesAddenda.append("+elementName+"Ad)\n")
#
# surface master species
#
        eSurface = self.params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSurfaceMasterSpecies()
        for i in eSurface.keys() :
            spec = str(i).replace("+","p")
            spec = str(spec).replace("-","m")
            spec = str(spec).replace(" ","")
            string = spec + " = SurfaceMasterSpecies("
            length = len(string)
            string += "symbol = \""+ eSurface[i]['FORMULA']+"\",\\\n"
            chemicalCase.write(string)
            string = " "*length + "name = \"" + eSurface[i]['NAME'] + "\")\n"
            chemicalCase.write(string)
#
# surface species
#
        eSurface = self.params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSurfaceSpecies()
        for i in eSurface.keys() :
#
# we replace + by p and - by m; the name being the species name on the right of "="
#        
            spec = str(i.split("=")[1]).replace("+","p")
            spec = str(spec).replace("-","m")
            spec = str(spec).replace(" ","")
            string = spec + " = SurfaceSecondarySpecies("
            length = len(string)

            string += "symbol = \""+ eSurface[i]['EQUATION'].split()[-1]+"\",\\\n"
            chemicalCase.write(string)
                #equation = ass[i]['EQUATION']
                #string = " "*length + "formationReaction = ["+ str(ass[i]['LOGK'])+",\\\n"
                #chemicalCase.write(string)
            tlist = ""

            a = str(eSurface[i]['EQUATION']).split(" ")[1:]
            liste = []
            ind = a.index("=")
            liste = _anal(str(eSurface[i]['EQUATION']).split("=")[0])
            for el in liste:
                tlist += "(\""+el[0]+"\","+str(el[1])+"),"
            tlist = tlist[0:-1]
            #print " tlist ",tlist
            string = " "*length + "formationReaction = ["+ tlist+"],\\\n"
            chemicalCase.write(string)
            string = " "*length + "logK25 = "+ str(eSurface[i]['LOGK'])+")\n"
            chemicalCase.write(string)
            chemicalCase.write("speciesAddenda.append("+spec+")\n")
        print "eSurface"
        print "eSurface",eSurface
        print "eSurface"
        del(ass)
        del(ams)
     
#Nabis = AqueousSecondarySpecies (symbol="Na+",
#                                 formationReaction = [("Na+", 1)],
#                                 logK25 =0.0,
#                                 name ="Na")

            
        chemicalCase.write("#~~~~~~~~~~~~~~~~~\n")
        chemicalCase.write("# Chemical State ~\n")
        chemicalCase.write("#~~~~~~~~~~~~~~~~~\n")
        chemicalCase.write("ChemicalStateList = []\n")
        aqueousStatesList = self.params.getParam(parameters.AqueousStates_list).getValue()
        aqueousStatesPropertiesList = self.params.getParam(parameters.AqueousStates_Properties_list).getValue()
        aqueousSpeciesList = self.params.getParam(parameters.AqueousStates_Species_list).getValue()
        mineralPhaseList = self.params.getParam(parameters.AqueousStates_MineralPhases_list).getValue()
        mineralPhasePropertiesList = self.params.getParam(parameters.AqueousStates_MineralPhases_Properties_list).getValue()
        exchangeSpeciesList = self.params.getParam(parameters.AqueousStates_ExchangeSpecies_list).getValue()            
        exchangeSpeciesPropertiesList = self.params.getParam(parameters.AqueousStates_ExchangeSpecies_Properties_list).getValue()
        #print "mineralPhasePropertiesList",mineralPhasePropertiesList[0],mineralPhasePropertiesList[1][0][1]
        ind = 0
        for aStates in aqueousStatesList:
            print " dbg aStates ",str(aStates),studyName
            if studyName == str(aStates):
                aSName = str(aStates) + "AqueousSolution"
                aSData = aqueousStatesPropertiesList[ind]
                print aSData
                pHString = "pH = " + aSData[0][1]
                peString = "pe = " + aSData[2][1]
                tempString = "temperature =" + aSData[1][1]
                #print "dbg tempString",aSData[1][1]
                eCList = ""
                indiz = 1
                stringAssociation = ""
                for elementConcentration in aqueousSpeciesList[ind]:
                    if elementConcentration[0].find("[") != -1:
                        ionAssociation = elementConcentration[0][0:elementConcentration[0].find("[")]
                        mineralAssociation = elementConcentration[0][elementConcentration[0].find("["):elementConcentration[0].find("]")]
                        self.Association = [ionAssociation,mineralAssociation]
                        stringAssociation = ",mineralEquilibrium = [("+ionAssociation+","+mineralAssociation+","+elementConcentration[1]+")]"
                        
                    else:
                        eCList += "ElementConcentration (\""+str(elementConcentration[0])+"\","+\
                                  str(elementConcentration[1])+","+"\"mol/l\"),\n"
                        if indiz < len(aqueousSpeciesList[ind]) :
                            eCList += " "*(len(aSName)+len(" = AqueousSolution (elementConcentrations = ")+1)
                            indiz+=1
                eCList = eCList[0:-2]+"\n"
#                
# mineralPhase associated to an aqueous state
#
                mineralPhaseName = str(aStates) + "MineralPhase = MineralPhase("
                mineralPhaseName_Length = len(mineralPhaseName)
                ePList = ""
                if len(mineralPhaseList[ind]) == 0:
                    ePList = "[])"
                    mineralPhaseName = ""
                else:
                    ePList = "["
                    indM = 0
                    for equilibriumPhase in mineralPhaseList[ind]:
                        if indM == 0:
                            ePList += "MineralTotalConcentration(\"" + str(equilibriumPhase) + "\"," +\
                        str(mineralPhasePropertiesList[ind][indM][1])+", \"mol/l\",saturationIndex = "+mineralPhasePropertiesList[ind][indM][0]+"),\n"
                        else:
                            ePList += " "*mineralPhaseName_Length+\
                        "MineralTotalConcentration(\"" + str(equilibriumPhase) + "\"," +\
                        str(mineralPhasePropertiesList[ind][indM][1])+", \"mol/l\",saturationIndex = "+mineralPhasePropertiesList[ind][indM][0]+"),\n"                    
                        indM+=1
                    ePList = ePList[0:len(ePList)-2]+"])"
                    chemicalCase.write(mineralPhaseName+ePList+"\n")
                    mineralPhaseName = str(aStates) + "MineralPhase"


#                mineralPhaseName = str(aStates) + "MineralPhase"
#                ePList = ""
#                if len(mineralPhaseList[ind]) == 0:
#                    ePList = "[])"
#                else:
#                    ePList = "["
#                indM = 0
#                for equilibriumPhase in mineralPhaseList[ind]:
#                    ePList = ePList + "MineralTotalConcentration(\"" + str(equilibriumPhase) + "\"," +\
#                    str(mineralPhasePropertiesList[ind][indM][1])+", \"mol/l\"),\n"
#                    indM+=1
#                if len(mineralPhaseList[ind]) != 0: ePList = ePList[0:len(ePList)-2]+"])"
#                chemicalCase.write(mineralPhaseName+" = MineralPhase("+ePList+"\n")
#
#
#
# exchange associated to an aqueous state
#
                exchangeName = str(aStates) + "IonicExchangers"
                iEList = ""
                if len(exchangeSpeciesList[ind]) == 0:
                    iEList = "[])"
                else:
                    iEList = "["
                indM = 0
                for exchangeSpecies in exchangeSpeciesList[ind]:
                    iEList = iEList + "ExchangeBindingSpecies(\"" + str(exchangeSpecies) + "\", MolesAmount(" +\
                    str(exchangeSpeciesPropertiesList[ind][indM][0])+", \"mol\")),\n"
                    indM+=1
                if len(exchangeSpeciesList[ind]) != 0: 
                    iEList = iEList[0:len(iEList)-2]+"])"
                    chemicalCase.write(exchangeName+" = IonicExchangers("+iEList+"\n")
                    exchangeName = ",ionicExchanger = "+exchangeName
                    print "exchangeName::",exchangeName
                else:
                    exchangeName = ""
#
#
#                
                stringLength = " "*(len(aSName)+len(" = AqueousSolution ("))
                eCList += " "*(len(aSName)+len(" = AqueousSolution (elementConcentrations = "))
                chemicalCase.write(aSName+" = AqueousSolution (elementConcentrations = ["+eCList+"],\\\n")
                chemicalCase.write(stringLength+pHString+",\\\n")
                chemicalCase.write(stringLength+tempString+",\\\n")
                chemicalCase.write(stringLength+peString+")\n")
                cSName = str(aStates) + "ChemicalState"
                addenda = self._addenda(mineralPhaseName,exchangeName)
                if self.chargeControl.GetValue() == False:
                    if self.pHControl.GetValue() == False and self.chargeBalanceControl.GetValue() == False:
                        chemicalCase.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+")\n\n")
                    elif self.pHControl.GetValue() == True and self.chargeBalanceControl.GetValue() == False:
                        chemicalCase.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+",phFixed = (\""+\
                        str(self.ion.GetValue())+"\","+str(self.moles.GetValue())+"))\n\n")
                    elif self.pHControl.GetValue() == False and self.chargeBalanceControl.GetValue() == True:
                        chemicalCase.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+",chargeBalance = (\""+\
                        str(self.cbion.GetValue())+"\","+str(self.cbmoles.GetValue())+"))\n\n")
                    else:
                        chemicalCase.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+",phFixed = (\""+\
                        str(self.ion.GetValue())+"\","+str(self.moles.GetValue())+",chargeBalance = (\""+\
                        str(self.cbion.GetValue())+"\","+str(self.cbmoles.GetValue())+"))\n\n")
                else:
                    if self.pHControl.GetValue() == False:
                        chemicalCase.write(cSName+" = ChemicalState (\""+str(aStates)+"\","+aSName+addenda+",charge=True)\n\n")
            ind+=1
#
#chemical_state_quartz = ChemicalState ("column", AqueousSolution_column, columnMineralPhase)
#
        chemicalCase.write("#~~~~~~~~~\n")
        chemicalCase.write("# Module ~\n")
        chemicalCase.write("#~~~~~~~~~\n")
            
        chemicalCase.write("module = Chemical()\n")

        chemicalCase.write("problem  = ChemicalProblem(name               = \""+\
        str(studyName)+"\",\\\n")
        chemicalCase.write("                           chemistryDB        = \""+dataBase+"\",\\\n")
        chemicalCase.write("                           speciesBaseAddenda = speciesAddenda,\\\n")
        chemicalCase.write("                           chemicalState      = "+cSName+")\n")

        chemicalCase.write("module.setData(problem)\n")
        chemicalCase.write("module.initialise()\n")
#        chemicalCase.write("module.setParameter(\"OutputFile\",\""+str(studyName)+".out\")\n")
        chemicalCase.write("module.setParameter(\""+str(studyName)+".out\")\n")
        chemicalCase.write("module.run()\n")
        chemicalCase.write("module.outputStateSaving()\n")
#        string = self.params.getParam(parameters.PyOutputHandler).getValue()
#        if string!= "":
#            chemicalCase.write("#~~~~~~~~~~~~~~~~~~\n")
#            chemicalCase.write("# Post processing ~\n")
#            chemicalCase.write("#~~~~~~~~~~~~~~~~~~\n")
#            string = self.params.getParam(parameters.PyOutputHandler).getValue()
#            chemicalCase.write(string)
        
#chem_soude  = Chemical()
#chem_soude.setData(problem_soude)
#chem_soude.initialise()
#chem_soude.setParameter('OutputFile','chemicalmodule_phreeqc_cas2_soude')
#chem_soude.run()
#chem_soude.outputStateSaving()
        
        lenString = len("        End of the ")+len(studyName)+len(" case ~")
        en = "~"*lenString   
        chemicalCase.write("\nprint \""+en+"\"\n")
        chemicalCase.write("print \"        End of the "+studyName+" case ~\"") 
        chemicalCase.write("\nprint \""+en+"\"\n")
            
        chemicalCase.close()
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
        #toto  = Myne("Equilibrium browser",studyName+".py")
        os.system("python "+studyName+".py")
        return None
    
def _aqueousToString(Liste):      
    a = ""
#    print "Liste2",Liste[3:]
    for i in Liste: a+=i[0]+" "+i[1]+" "
    return a

def _anal(a):
    b = a.split()
    liste = []
    for i in b:
        dig = 1
        if i[0].isalpha():
            liste.append((i,dig))
        elif i[0] in ["-"]:
             dig = -1
             if len(i) != 1:
                 ind = 1
                 while i[ind].isdigit():
                     ind+=1
                 dig = i[0:ind]
                 liste.append((i[ind:],dig))
        elif i[0] in ["+"]:
             if len(i) != 1:
                 ind = 1
                 while i[ind].isdigit():
                     ind+=1
                 dig = i[0:ind]
                 liste.append((i[ind:],dig))
    return liste             

def _strHandlung(string):
     string = string.replace("+","p")
     string = string.replace("-","m")
     string = string.replace("(","_")
     string = string.replace(")","_")
     return string

