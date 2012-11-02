import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

description ="""
       Used to define outputs and parameters for the interactive plot
       """
HELP = """
       <html><body>This module allows to plot the last results of the simulation, during the simulation. You will also know the evolution of your model in real time.
       <p>
       Choose in Expected Outputs which outputs you want to plot. Then the parameters:
       <OL start=1><LI type=1>   Rotate    : It affects the disposition of the graphics</li>
       <LI type=1>   Frequency : The simulation time between two refresment would be dt0*Frequancy</li> 
                      dt0 is the time step (refer to time discretisation module)</OL>
       <p>
       It is possible to save these graphics.
       <p>
       Put the cursor over the different controls for more details.</body></html>
       """
class interactivePlot(ParamsAction):
    """
    Used to set the ascii outputs
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Interactive Plot",description  =description,help=HELP)
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
        self.outputList = outputList = self.params.getParam(parameters.IOutputs_list).getValue()

        sizer = wx.BoxSizer( wx.VERTICAL )
        
        
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Choice of the outputs to plot:" ) , wx.HORIZONTAL)
#        box3.SetOwnFont(boldFont)
        box3.SetMinSize((650,50))
        
        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box31.SetMinSize((310,30))

        label1 = wx.StaticText(parent,-1,"Selected\nOutputs:",size=(80,-1));label1.SetTTS("Comment")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.selectedOutputs = selectedOutputs =  self.params.getParam(parameters.IOutputs_list).getValue()

        self.selectedOutput = selectedOutput = \
        wx.ComboBox(parent, -1, "",(230, 30), (200, -1),selectedOutputs, wx.CB_DROPDOWN)
        selectedOutput.SetToolTipString("Outputs which will \nbe interactively ploted")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedOutputControl, selectedOutput)

        box31.Add(selectedOutput, 0., wx.ALIGN_CENTER|wx.ALL, 1)

        box3.Add(box31, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        box32 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box32.SetMinSize((310,20))
        
        self.availableOutputList = availableOutputList = self.params.getParam(parameters.ExpectedOutputs_list).getValue()
        
        
        label2 = wx.StaticText(parent, -1, "Expected\nOutputs:",size=(80,-1))
        label2.SetOwnFont(boldFont)
        label2.SetTTS("Comment")

        box32.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        outputComboboxDefault = ""
        self.availableOutputCombo = availableOutputCombo =\
        wx.ComboBox(parent, -1, outputComboboxDefault,(230, 30), (200, -1),availableOutputList, wx.CB_DROPDOWN)
        
        availableOutputCombo.SetToolTipString("Available outputs to be picked up by\n the user")
        availableOutputCombo.SetLabel("Available Outputs")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedOutputControl, availableOutputCombo)
                                 
        box32.Add(availableOutputCombo,0,wx.ALIGN_CENTER|wx.ALL, 1)


        box3.Add(box32, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        
        
        
# Properties control

		# box4 : Establishment of the placement for properties
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.VERTICAL)
        box4.SetMinSize((650,50))
        
        self.pHRadios = pHRadios = []
		
		
		# box41 : first the check box for choosing rotation or not
		
        box41 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Plot properties" ) , wx.HORIZONTAL)
        box41.SetMinSize((640,30))
        
        label1 = wx.StaticText(parent, -1, "Rotate:",size=(60,-1))
        label1.SetTTS("If no rotation, meters are on y. Else on x")
        label1.SetOwnFont(boldFont)
        box41.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.rotate = rotate = wx.CheckBox( parent, -1, "",style = 0)
        rotate.SetTTS("used to fix the pH ")
        box41.Add(rotate, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        pHRadios.append(rotate)
        self.rotate.SetValue(self.params.getParam(parameters.IRotate).getValue())


		# box41 : second the text control for writing the frequency of the plot
		
        label2 = wx.StaticText(parent, -1, "frequency:",size=(85,-1))
        label2.SetTTS("Number of time steps between two refreshment")
        label2.SetOwnFont(boldFont)
        box41.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        self.frequency = frequency = wx.TextCtrl(parent, -1,"",size=(50,-1))
        frequency.SetTTS("Number of time steps between two refreshment")
        frequency.Enable(True)
        box41.Add(frequency, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        self.frequency.SetValue(str(self.params.getParam(parameters.IFrequency).getValue()))


        # box41 : third the text control for writing the title of the plot
        
        label2 = wx.StaticText(parent, -1, "Title:",size=(50,-1))
        label2.SetTTS("t")
        label2.SetOwnFont(boldFont)
        box41.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        self.plotTitle = plotTitle = wx.TextCtrl(parent, -1,"",size=(120,-1))
        plotTitle.SetTTS("Title of the interactive plot")
        plotTitle.Enable(True)
        box41.Add(plotTitle, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        self.plotTitle.SetValue(self.params.getParam(parameters.ITitle).getValue())
        
        
        # box41 : fourth the text control for writing the subtitle of the plot
        
        label2 = wx.StaticText(parent, -1, "SubTitle:",size=(80,-1))
        label2.SetTTS("")
        label2.SetOwnFont(boldFont)
        box41.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        self.plotSubTitle = plotSubTitle = wx.TextCtrl(parent, -1,"",size=(100,-1))
        plotSubTitle.SetTTS("Second title of the interactive plot")
        plotSubTitle.Enable(True)
        box41.Add(plotSubTitle, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.plotSubTitle.SetValue(self.params.getParam(parameters.ISubTitle).getValue())
        
        
        box4.Add(box41, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        
        # box42 : Save options
        
        box42 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Save options" ) , wx.HORIZONTAL)
        box42.SetMinSize((640,30))
        
        # box42 : first the checkbox for the user to choose if he would save his plots or not
        
        label1 = wx.StaticText(parent, -1, "Save graphics:",size=(120,-1))
        label1.SetTTS("")
        label1.SetOwnFont(boldFont)
        box42.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.save = save = wx.CheckBox( parent, -1, "",style = 0)
        save.SetTTS("If Checkbox is selected, the outputs would be saved")
        box42.Add(save, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 1 )
        self.save.SetValue(self.params.getParam(parameters.ISave).getValue())
        toto.Bind(wx.EVT_CHECKBOX, self._saveOutputs, save)
        
        
        # box42 : second the frequency choice
        label2 = wx.StaticText(parent, -1, "frequency:",size=(100,-1))
        label2.SetTTS("")
        label2.SetOwnFont(boldFont)
        box42.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        self.saveFreq = saveFreq = wx.TextCtrl(parent, -1,"",size=(70,-1))
        saveFreq.SetTTS("Should be a multiple of the plot frequency")
        saveFreq.Enable(self.save.GetValue())
        box42.Add(saveFreq, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        if not self.save.GetValue():
            self.saveFreq.SetValue('No')
        else:
            self.saveFreq.SetValue(str(self.params.getParam(parameters.ISaveFrequency).getValue()))

            
        
        # box42 : third output format
        
        label3 = wx.StaticText(parent, -1, "Format :",size=(80,-1))
        label3.SetTTS("")
        label3.SetOwnFont(boldFont)
        box42.Add(label3, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        outputFormatDefault = self.params.getParam(parameters.IOutputFormat).getValue()
        outputFormatDefault_List = self.params.getParam(parameters.IOutputFormat_List).getValue()
        self.outputFormatCombo = outputFormatCombo =\
        wx.ComboBox(parent, -1, outputFormatDefault,(250, 20), (100, -1),outputFormatDefault_List, wx.CB_DROPDOWN)
        
        outputFormatCombo.SetToolTipString("Format for the saves")
        outputFormatCombo.SetLabel("Available Outputs")
                                 
        box42.Add(outputFormatCombo,0,wx.ALIGN_CENTER|wx.ALL, 1)
        
        box4.Add(box42, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        sizer.Add(box4, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        
#
# outputs definition
#
        box6 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Already selected outputs : " ) , wx.HORIZONTAL)
        box6.SetMinSize((650,120))

        self.selectedOutputList = selectedOutputList = wx.TextCtrl(parent, -1,_outputToString(selectedOutputs),
                       size=(350, 110), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        selectedOutputList.SetOwnFont(boldFont)
        selectedOutputList.SetForegroundColour("#1857DE")
	selectedOutputList.SetTTS("List of already selected outputs")
        selectedOutputList.SetInsertionPoint(0)
#        toto.Bind(wx.EVT_TEXT, self._evtText, mineralPhaseState)
        
        box6.Add(selectedOutputList, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.update = update = wx.Button(parent, -1, "Update", (50,50))
        update.SetTTS("Used to update the output list.\n")
        toto.Bind(wx.EVT_BUTTON, self._updateOutput, update)
        box6.Add(update, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        self.delete = delete = wx.Button(parent, -1, "Delete", (50,50))
        delete.SetTTS("Used to delete the selected species\n from the output list")
        toto.Bind(wx.EVT_BUTTON, self._deleteOutput, delete)
        box6.Add(delete, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 20)
        sizer.Add(box6, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)
        

    def _updateOutput(self, event):
        print "ok"
        outputName = str(self.selectedOutput.GetValue()).replace(" ","")
        print "_updateOutput",outputName
        if outputName == "":
            wx.MessageDialog(self.parent, "You have to select an output name first\n"+\
            "before trying to update the output list"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
            
        self.outputList = self.params.getParam(parameters.IOutputs_list).getValue()
        
        if outputName in self.outputList:
            pass            
        else:
            self.outputList.append(outputName)
        print self.outputList
        self.params.getParam(parameters.IOutputs_list).setValue(self.outputList)
        
# we reinitialize the elements to leere Zeilen, the aqueous state bleibt, only the mineral is reinitialised

        outputDescription = _outputToString(self.outputList)
        self.selectedOutputList.SetValue(outputDescription)
                
        self.selectedOutput.SetItems(self.outputList)

    def _selectedOutputControl(self, event):
        selected = event.GetString()
        self.selectedOutput.SetValue(selected)
    
        
    def _deleteOutput(self, event):
        selected = str(self.selectedOutput.GetValue())
        if selected != "":
            indiz = self.outputList.index(selected)
            del self.outputList[indiz]
            self.params.getParam(parameters.IOutputs_list).setValue(self.outputList)
            
            outputDescription = _outputToString(self.outputList)
            self.selectedOutputList.SetValue(outputDescription)
            self.selectedOutput.SetValue("")
            self.selectedOutput.SetItems(self.outputList)
        else:
            wx.MessageDialog(self.parent, "You have to select an output\nto complete that action."\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
        return
    
    def _saveOutputs(self, event):
        selected = self.save.GetValue()
        self.saveFreq.Enable(selected)
        self.outputFormatCombo.Enable(selected)
        
        if selected:
            self.saveFreq.SetValue(str(self.params.getParam(parameters.ISaveFrequency).getValue()))
            self.outputFormatCombo.SetValue(self.params.getParam(parameters.IOutputFormat).getValue())
        else:
            self.saveFreq.SetValue('No')
            
    
    
    

    def _evtText(self, event):
        pass

    def _onOk(self, params):
#
# saving outputs
#
        self.params.getParam(parameters.IOutputs_list).setValue(self.outputList)
        self.params.getParam(parameters.IRotate).setValue(self.rotate.GetValue())
        
        error = 0																		# Check if frequencies values are coherent
        f = self.frequency.GetValue()
        if f.isdigit():
            f = eval(f)
            if type(f) == float:
                f = int(f)
            if type(f) == int and f !=0:
                self.params.getParam(parameters.IFrequency).setValue(f)
            else:
                error = 1
        else:
            error = 1
        self.params.getParam(parameters.ITitle).setValue(str(self.plotTitle.GetValue()))
        self.params.getParam(parameters.ISubTitle).setValue(str(self.plotSubTitle.GetValue()))
        
        # Graphics Save
               
        self.params.getParam(parameters.ISave).setValue(self.save.GetValue())
        if self.save.GetValue():
        
            g = self.saveFreq.GetValue()
            if g.isdigit():
                g = eval(g)
                if type(g) == float:
                    g = int(g)
                if type(g) == int and type(f) == int and f != 0:
                    if g >= f:
                        self.params.getParam(parameters.ISaveFrequency).setValue(g/f*f)
                    else:
                        if g == 0: error =1
                        self.params.getParam(parameters.ISaveFrequency).setValue(f)
            else:
                error = 1
                    
            self.params.getParam(parameters.IOutputFormat).setValue(self.outputFormatCombo.GetValue())
            
        if error == 1:
            wx.MessageDialog(self.parent,\
                             "Incorrect frequency input. Check :\n\
                              - Plot frequency\n\
                              - Save frequency",\
                             "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            
            
  
        return True
        
def _outputToString(outputList):      
    a = ""
    for ind in range (0,len(outputList)):
        a+= str(outputList[ind]) + "\n"
    return a
        




