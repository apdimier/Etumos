import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

description ="""
       Used to define outputs for the post processing
       """
HELP = """
       <html><body>You can define here the different unknowns to study as outputs of the chemical-transport study. Available unknowns are to be chosen among <br><b>components</b>, <b>secondary species</b> and <b>minerals</b>.</body></html>
       """
class PostProcessing(ParamsAction):
    """
    Used to set the ascii outputs
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Ascii Post Processing",description  =description,help=HELP)
        self.radios = None
        self.choice = None

    def _createInterface(self, parent, params):
#velocity components
        toto = self.GetDialogPanel()
        wx.TextCtrl.SetTTS = wx.TextCtrl.SetToolTipString
        wx.CheckBox.SetTTS = wx.CheckBox.SetToolTipString
        wx.StaticText.SetTTS = wx.StaticText.SetToolTipString
        wx.Button.SetTTS = wx.Button.SetToolTipString
        f = wx.Font(10, wx.ROMAN, wx.ITALIC, wx.BOLD, True)
        boldFont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")
        self.parent = parent
        self.params = params
        self.outputList = outputList = self.params.getParam(parameters.ExpectedOutputs_list).getValue()

        sizer = wx.BoxSizer( wx.VERTICAL )
#        
# choice of outputs
#
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Choice of the outputs:" ) , wx.HORIZONTAL)
#        box3.SetOwnFont(boldFont)
        box3.SetMinSize((600,100))

        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box31.SetMinSize((300,30))

        # Combo box for expected outputs selection
        
        label1 = wx.StaticText(parent,-1,"Expected\nOutputs:",size=(80,-1));label1.SetTTS("Already selected unknowns")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.selectedOutputs = selectedOutputs =  self.params.getParam(parameters.ExpectedOutputs_list).getValue()

        self.selectedOutput = selectedOutput = \
        wx.ComboBox(parent, -1, "",(250, 20), (200, -1),selectedOutputs, wx.CB_DROPDOWN)
        toto.Bind(wx.EVT_COMBOBOX, self._selectedOutputControl, selectedOutput)

        box31.Add(selectedOutput, 0., wx.ALIGN_CENTER|wx.ALL, 1)

        box3.Add(box31, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        # Combo box for avaible outputs
        
        box32 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.VERTICAL)
        box32 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box32.SetMinSize((250,20))
        
        self.availableOutputList = availableOutputList = ["pH","Is"]
        availableOutputList += params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getMineralPhases().keys()
        availableOutputList += params.getParamValue(parameters.CUSTOM_CHEMISTRY_DB).getSolutionSecondarySpecies().keys()

        availableOutputList += params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getSolutionSecondarySpecies().keys()
        availableOutputList += params.getParamValue(parameters.IMPORTED_CHEMISTRY_DB).getMineralPhases().keys()        
        
        label2 = wx.StaticText(parent, -1, "Available outputs:",size=(100,-1))
        label2.SetOwnFont(boldFont)
        label2.SetTTS("You pick up outputs through\navailable components, secondary species and phases")

        box32.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        outputComboboxDefault = ""
        self.availableOutputCombo = availableOutputCombo =\
        wx.ComboBox(parent, -1, outputComboboxDefault,(250, 20), (200, -1),availableOutputList, wx.CB_DROPDOWN)
        
        availableOutputCombo.SetToolTipString("Available outputs to be picked up by\n the user")
        availableOutputCombo.SetLabel("Available Outputs")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedOutputControl, availableOutputCombo)
                                 
        box32.Add(availableOutputCombo,0,wx.ALIGN_CENTER|wx.ALL, 1)

        box3.Add(box32, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
#
# outputs definition
#
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Already selected outputs: " ) , wx.HORIZONTAL)
        box4.SetMinSize((600,120))

        self.selectedOutputList = selectedOutputList = wx.TextCtrl(parent, -1,_outputToString(selectedOutputs),
                       size=(300, 110), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        selectedOutputList.SetOwnFont(boldFont)
        selectedOutputList.SetForegroundColour("#1857DE")
	selectedOutputList.SetTTS("List of already selected outputs")
        selectedOutputList.SetInsertionPoint(0)
#        toto.Bind(wx.EVT_TEXT, self._evtText, mineralPhaseState)
        
        box4.Add(selectedOutputList, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.update = update = wx.Button(parent, -1, "Update", (50,50))
        update.SetTTS("Used to update the output list.\n")
        toto.Bind(wx.EVT_BUTTON, self._updateOutput, update)
        box4.Add(update, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        self.delete = delete = wx.Button(parent, -1, "Delete", (50,50))
        delete.SetTTS("Used to delete the selected species\n from the output list")
        toto.Bind(wx.EVT_BUTTON, self._deleteOutput, delete)
        box4.Add(delete, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        sizer.Add(box4, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)

##############
#            #
#  Controls  #
#            #
##############

    def _updateOutput(self, event):
    
        outputName = str(self.selectedOutput.GetValue()).replace(" ","")
        
        if outputName == "":
            wx.MessageDialog(self.parent, "You have to select an output name first\n"+\
            "before trying to update the output list"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
            
        self.outputList = self.params.getParam(parameters.ExpectedOutputs_list).getValue()
        
        if outputName in self.outputList:
            pass            
        else:
            self.outputList.append(outputName)

        self.params.getParam(parameters.ExpectedOutputs_list).setValue(self.outputList)
        
# we reinitialize the elements to leere Zeilen, the aqueous state bleibt, only the mineral is reinitialised

        outputDescription = _outputToString(self.outputList)
        self.selectedOutputList.SetValue(outputDescription)
                
        self.selectedOutput.SetItems(self.outputList)

    def _selectedOutputControl(self, event):
        selected = event.GetString()
        self.selectedOutput.SetValue(selected)
    
    def _ExpectedOutputControl(self, event):
        selected = str(self.selectedOutput.GetValue())
        ExpectedOutputsQuantity_list = self.params.getParam(parameters.ExpectedOutputsQuantity_list).getValue()
        quantity = ''
        for couple in ExpectedOutputsQuantity_list:
           if couple[0] == selected:
               quantity = couple[1]
        self.availableQuantityCombo.SetValue(quantity)
        
    def _deleteOutput(self, event):
        selected = str(self.selectedOutput.GetValue())
        if selected != "":

            #delete it from expected outputs
            
            indiz = self.outputList.index(selected)
            del self.outputList[indiz]
            self.params.getParam(parameters.ExpectedOutputs_list).setValue(self.outputList)
            
            outputDescription = _outputToString(self.outputList)
            self.selectedOutputList.SetValue(outputDescription)
            self.selectedOutput.SetValue("")
            self.selectedOutput.SetItems(self.outputList)
        else:
            wx.MessageDialog(self.parent, "You have to select an output\nto complete that action."\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
        return

    def _evtText(self, event):
        pass

    def _onOk(self, params):
#
# saving outputs
#
        self.params.getParam(parameters.ExpectedOutputs_list).setValue(self.outputList)
  
        return True
        
def _outputToString(outputList):      
    a = ""
    for ind in range (0,len(outputList)):
        a+= str(outputList[ind]) + "\n"
    return a

