import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

description ="""
       Used to define outputs for the global plot at the end of the simulation
       """
HELP = """
       <html><body>You can choose here the parameters of a plot at the end of the simulation. 
       <p>
       Choose outputs to plot and dates. For each output, one graphic will represent the values of this output at the different selected dates.
       </li>Then, these graphics will be saved
       <p>
       Put the cursor over the different controls for more details.</body></html>
       """
class globalGraphics(ParamsAction):
    """
    Used to set the ascii outputs
    """
    
    

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Global Plot",description  =description,help=HELP)
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
        self.outputList = outputList = self.params.getParam(parameters.GlobalOutputs_list).getValue()
        
        self.nb_letters = 5
        self.unitsReduced = []
        self.datesUnits = self.params.getParam(parameters.GlobalPlotUnits_list).getDefault()
        for i in range(len(self.datesUnits)):
            self.unitsReduced.append(self.datesUnits[i][0:self.nb_letters])

        sizer = wx.BoxSizer( wx.VERTICAL )
        
        
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Choice of the outputs to plot:" ) , wx.VERTICAL)
#        box3.SetOwnFont(boldFont)
        box3.SetMinSize((600,20))
        
        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box31.SetMinSize((600,20))

        label1 = wx.StaticText(parent,-1,"Selected outputs:",size=(60,-1));label1.SetTTS("Comment")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        self.selectedOutputs = selectedOutputs =  self.params.getParam(parameters.GlobalOutputs_list).getValue()

        self.selectedOutput = selectedOutput = \
        wx.ComboBox(parent, -1, "",(250, 20), (200, -1),selectedOutputs, wx.CB_DROPDOWN)
        selectedOutput.SetToolTipString("Outputs which will \nbe global ploted")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedOutputControl, selectedOutput)

        box31.Add(selectedOutput, 0., wx.ALIGN_LEFT|wx.ALL, 1)

        
        
        self.availableOutputList = availableOutputList = self.params.getParam(parameters.ExpectedOutputs_list).getValue()
        
        
        label2 = wx.StaticText(parent, -1, "\t   Expected\n\t   Outputs:",size=(110,30))
        label2.SetOwnFont(boldFont)
        label2.SetTTS("Comment")

        box31.Add(label2, 0,  wx.ALIGN_RIGHT|wx.ALL, 1)

        outputComboboxDefault = ""
        self.availableOutputCombo = availableOutputCombo =\
        wx.ComboBox(parent, -1, outputComboboxDefault,(250, 20), (200, -1),availableOutputList, wx.CB_DROPDOWN)
        
        availableOutputCombo.SetToolTipString("Available outputs to be picked up by\n the user")
        availableOutputCombo.SetLabel("Available Outputs")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedOutputControl, availableOutputCombo)
                                 
        box31.Add(availableOutputCombo,0, wx.ALIGN_RIGHT|wx.ALL, 1)


        box3.Add(box31, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        
        box33 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Updating the output selection" ) , wx.HORIZONTAL)
        box33.SetMinSize((250,10))
        
        # Add a date button
        self.addOutput = addOutput = wx.Button(parent, -1, "Add", (20,20))
        addOutput.SetTTS("Used to add a date to the dates list")
        toto.Bind(wx.EVT_BUTTON, self._addOutput, addOutput)
        box33.Add(addOutput, 10, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        # Delete a date button
        self.delOutput = delOutput = wx.Button(parent, -1, "Del", (20,20))
        delOutput.SetTTS("Used to delete a date to the dates list")
        toto.Bind(wx.EVT_BUTTON, self._delOutput, delOutput)
        box33.Add(delOutput, 10, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        box3.Add(box33, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        sizer.Add(box3, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        
        
        
# Properties control

		# box4 : Establishment of the placement for properties
        box4 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Choose years" ) , wx.HORIZONTAL)
        box4.SetMinSize((600,50))
        
        # Title of Combo box for selected dates
        label1 = wx.StaticText(parent,-1,"Already selected :",size=(70,-1));label1.SetTTS("Comment")
        label1.SetOwnFont(boldFont)
        box4.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        # Combo box for selected dates
        self.selectedDates = selectedDates =  self.params.getParam(parameters.GlobalDates_list).getValue()
        self.selectedDate = selectedDate = wx.ComboBox(parent, -1, "",(250, 20), (120, -1),selectedDates, wx.CB_DROPDOWN)
        selectedDate.SetToolTipString("Dates at which outputs will be ploted")
        toto.Bind(wx.EVT_COMBOBOX, self._selectedDateControl, selectedDate)
        box4.Add(selectedDate, 0., wx.ALIGN_CENTER|wx.ALL, 1)
        
        # Title for the choice of a new date
        label2 = wx.StaticText(parent,-1,"  | New date :",size=(85,-1));label1.SetTTS("Comment")
        label2.SetOwnFont(boldFont)
        box4.Add(label2, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        # Text control for the date
        self.newDate = newDate = wx.TextCtrl(parent, -1,"",size=(50,-1))
        newDate.SetTTS("Value of a new date")
        newDate.Enable(True)
        box4.Add(newDate, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        self.newDate.SetValue('')
        
        # Combo box for the unit of the new date
        self.datesUnits = datesUnits =  self.params.getParam(parameters.GlobalPlotUnits_list).getDefault()
        self.dateUnit = dateUnit = wx.ComboBox(parent, -1, "",(250, 20), (70, -1),datesUnits, wx.CB_DROPDOWN)
        dateUnit.SetToolTipString("Outputs which will \nbe global ploted")
        box4.Add(dateUnit, 0., wx.ALIGN_CENTER|wx.ALL, 1)
        
        # Space between the combobox and the buttons
        label3 = wx.StaticText(parent,-1,"   ",size=(20,-1));label1.SetTTS("Comment")
        label3.SetOwnFont(boldFont)
        box4.Add(label3, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        
        # Add a date button
        self.addDate = addDate = wx.Button(parent, -1, "Add", (20,20))
        addDate.SetTTS("Used to add a date to the dates list")
        toto.Bind(wx.EVT_BUTTON, self._addDate, addDate)
        box4.Add(addDate, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        # Delete a date button
        self.delDate = delDate = wx.Button(parent, -1, "Del", (20,20))
        delDate.SetTTS("Used to delete a date to the dates list")
        toto.Bind(wx.EVT_BUTTON, self._delDate, delDate)
        box4.Add(delDate, 0, wx.ALIGN_CENTER|wx.ALL, 1)


        

        sizer.Add(box4, 0, wx.ALIGN_LEFT|wx.ALL, 1 )
        
#
# outputs definition
#
        box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Selected plot properties : " ) , wx.HORIZONTAL)
        box5.SetMinSize((600,120))
        
        text = "Selected outputs :\n" + _outputToString(selectedOutputs) + "\n\nSelected dates :\n" + _outputToString(selectedDates)
        self.selectedOutputList = selectedOutputList = wx.TextCtrl(parent, -1,text,
                       size=(300, 110), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        selectedOutputList.SetOwnFont(boldFont)
        selectedOutputList.SetForegroundColour("#1857DE")
        selectedOutputList.SetTTS("List of already selected outputs")
        selectedOutputList.SetInsertionPoint(0)
#        toto.Bind(wx.EVT_TEXT, self._evtText, mineralPhaseState)
        box5.Add(selectedOutputList, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        sizer.Add(box5, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)
        

    def _selectedOutputControl(self, event):
        selected = event.GetString()
        self.selectedOutput.SetValue(selected)
    
    def _selectedDateControl(self, event):    
        selected = event.GetString()        
        
        if selected != "":
            self.newDate.SetValue(selected.split()[0])
            self.dateUnit.SetValue(self.datesUnits[self.unitsReduced.index(selected.split()[1])])

    def _evtText(self, event):
        pass


    #~~~~~~~~~~~~~~~~
    #  Date control
    #~~~~~~~~~~~~~~~~
 
    def _addDate(self, event):
        value = self.newDate.GetValue()
        value.replace(' ', '')
        print 'value = ', value
        unit = self.dateUnit.GetValue()
        print 'unit = ', unit
        
        if value.isdigit():
            value = int(eval(value))
            DateToAdd = str(value) + ' ' + unit[0:self.nb_letters]
            if DateToAdd not in self.selectedDates:
                
                i = 0
                found = False
                while not found:
                    if i + 1 > len(self.selectedDates):
                        found = True
                    elif self.unitsReduced.index(DateToAdd.split()[1]) < self.unitsReduced.index(self.selectedDates[i].split()[1]):
                        # if the unit is lower as the place
                        found = True
                    elif self.unitsReduced.index(DateToAdd.split()[1]) == self.unitsReduced.index(self.selectedDates[i].split()[1]):
                        if eval(DateToAdd.split()[0]) < eval(self.selectedDates[i].split()[0]):
                            found = True
                        else:
                            i += 1
                    else:
                        i += 1
                        
                self.selectedDates.insert(i, DateToAdd)
                print DateToAdd
                print self.selectedDates
        else:
            wx.MessageDialog(self.parent, "Date value should be an integer"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        
        # we reinitialize the elements to leere Zeilen, the aqueous state bleibt, only the mineral is reinitialised

        outputDescription = "Selected outputs :\n" + _outputToString(self.selectedOutputs) + "\n\nSelected dates :\n" + _outputToString(self.selectedDates)
        self.selectedOutputList.SetValue(outputDescription)
        self.selectedDate.SetValue("")
        self.dateUnit.SetValue("")
        self.newDate.SetValue("")
        self.selectedDate.SetItems(self.selectedDates)
        
    
    def _delDate(self, event):
        value = self.newDate.GetValue()
        value.replace(' ', '')
        print 'value = ', value
        unit = self.dateUnit.GetValue()
        print 'unit = ', unit
        
        if value.isdigit():
            value = int(eval(value))
            DateToDel = str(value) + ' ' + unit[0:self.nb_letters]
            if DateToDel in self.selectedDates:
                self.selectedDates.remove(DateToDel)
            
            outputDescription = "Selected outputs :\n" + _outputToString(self.selectedOutputs) + "\n\nSelected dates :\n" + _outputToString(self.selectedDates)
            self.selectedOutputList.SetValue(outputDescription)
            self.selectedDate.SetValue("")
            self.dateUnit.SetValue("")
            self.newDate.SetValue("")
            self.selectedDate.SetItems(self.selectedDates)
            
            
            
    #~~~~~~~~~~~~~~~~~
    # Outputs control
    #~~~~~~~~~~~~~~~~~
    
                
    def _addOutput(self, event):
        
        output2add = self.availableOutputCombo.GetValue()
        if output2add == "":
            wx.MessageDialog(self.parent, "You have to select an output name first\n"+\
            "before trying to update the output list"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
            
        self.selectedOutputs = self.params.getParam(parameters.GlobalOutputs_list).getValue()
        
        if output2add in self.selectedOutputs:
            pass            
        else:
            self.selectedOutputs.append(output2add)

        self.params.getParam(parameters.GlobalOutputs_list).setValue(self.selectedOutputs)
        
# we reinitialize the elements to leere Zeilen, the aqueous state bleibt, only the mineral is reinitialised

        outputDescription = "Selected outputs :\n" + _outputToString(self.selectedOutputs) + "\n\nSelected dates :\n" + _outputToString(self.selectedDates)
        self.selectedOutputList.SetValue(outputDescription)
        self.selectedOutput.SetValue("")
        self.availableOutputCombo.SetValue("")
        self.selectedOutput.SetItems(self.selectedOutputs)
        
    
    def _delOutput(self, event):
        output2delete = self.selectedOutput.GetValue()
        print 'output2delete = ', output2delete
        
        self.selectedOutputs =  self.params.getParam(parameters.GlobalOutputs_list).getValue()
        

        if output2delete == "":
            wx.MessageDialog(self.parent, "You have to select an output name first\n"+\
            "before trying to delete the output from the list"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
            
        self.outputList = self.params.getParam(parameters.GlobalOutputs_list).getValue()
        self.selectedOutputs =  self.params.getParam(parameters.GlobalOutputs_list).getValue()
        
        if output2delete not in self.selectedOutputs:
            pass            
        else:
            self.outputList.remove(output2delete)
        print self.outputList
        self.params.getParam(parameters.GlobalOutputs_list).setValue(self.outputList)
        outputDescription = "Selected outputs :\n" + _outputToString(self.selectedOutputs) + "\n\nSelected dates :\n" + _outputToString(self.selectedDates)
        self.selectedOutputList.SetValue(outputDescription)
        self.selectedOutput.SetValue("")
        self.availableOutputCombo.SetValue("")
        self.selectedOutput.SetItems(self.outputList)
    
    

    def _onOk(self, params):
#
# saving outputs
#
        self.params.getParam(parameters.GlobalOutputs_list).setValue(self.outputList)
        self.params.getParam(parameters.GlobalDates_list).setValue(self.selectedDates)
        

  
        return True
        
    
        
def _outputToString(outputList):      
    a = ""
    for ind in range (0,len(outputList)):
        a+= str(outputList[ind]) + "\n"
    return a
