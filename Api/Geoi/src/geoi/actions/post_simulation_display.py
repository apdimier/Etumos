import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters
import os, sys
import Gnuplot, Gnuplot.funcutils
import subprocess
import time

description ="""
       Used to plot the simulation of the different expected outputs at differents times
       """
HELP = """
       <html><body>If you ask to plot only one AqueousConcentration, it will be plot as Concentration
       <p>
       You can change ploting options with changing the parameters of the .dem file
       </body></html>
       """
class displayOptions(ParamsAction):
    """
    Used to set the ascii outputs
    """
    
    

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Post Simulation Display",description  =description,help=HELP)
        
        
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
        
# Box 2 : Get the datafile
        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, ""), wx.VERTICAL)
        box2.SetMinSize((600,20))
        self.dataFileCWD = dataFileCWD = self.params.getParam(parameters.DataFileCWD).getValue()
        self.label = label = wx.StaticText(parent, -1, "Data File :  \t" + dataFileCWD.split('/')[-1],(200,100))
        box2.Add(label, 0, wx.LEFT|wx.ALL, 2)
        
        self.load = load = wx.Button(parent, -1, "Load", (200,100))
        toto.Bind(wx.EVT_BUTTON, self._load, self.load)
        box2.Add(load, 0, wx.LEFT|wx.ALL, 2)
        
        sizer.Add(box2, 0, wx.ALIGN_LEFT|wx.ALL, 1 )

# Box 3 : Select dates and outputs
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Choice of the outputs to plot:" ) , wx.VERTICAL)
#        box3.SetOwnFont(boldFont)
        box3.SetMinSize((600,20))
        
        box31 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "") , wx.HORIZONTAL)
        box31.SetMinSize((600,20))

        label1 = wx.StaticText(parent,-1,"   Species : ",size=(80,-1));label1.SetTTS("Comment")
        label1.SetOwnFont(boldFont)
        box31.Add(label1, 0, wx.ALIGN_LEFT|wx.ALL, 1)
        self.availableSpecies = availableSpecies =  self.params.getParam(parameters.AvailableSpecies_list).getValue()

        self.selectedSpecies = selectedSpecies = \
        wx.ComboBox(parent, -1, "",(250, 20), (200, -1),availableSpecies, wx.CB_DROPDOWN)
        selectedSpecies.SetToolTipString("Outputs which will \nbe global ploted")


        box31.Add(selectedSpecies, 0., wx.ALIGN_LEFT|wx.ALL, 1)

        
        
        self.availableDates = availableDates = self.params.getParam(parameters.AvailableDates_list).getValue()
        
        
        label2 = wx.StaticText(parent, -1, "     Dates : ",size=(80,30))
        label2.SetOwnFont(boldFont)
        label2.SetTTS("Comment")

        box31.Add(label2, 0,  wx.ALIGN_RIGHT|wx.ALL, 1)

        
        self.selectedDate = selectedDate =\
        wx.ComboBox(parent, -1, "",(250, 20), (200, -1),availableDates, wx.CB_DROPDOWN)
        
        selectedDate.SetToolTipString("Available outputs to be picked up by\n the user")
        selectedDate.SetLabel("Available Outputs")
                                 
        box31.Add(selectedDate,0, wx.ALIGN_RIGHT|wx.ALL, 1)


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
        
        
#
# outputs definition
#
        box5 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Selected plot properties : " ) , wx.HORIZONTAL)
        box5.SetMinSize((600,120))
        
        
        self.speciesSelection = speciesSelection = self.params.getParam(parameters.SpeciesSelection_list).getValue()
        self.datesSelection = datesSelection = self.params.getParam(parameters.DatesSelection_list).getValue()
        
        
        
        text = _dataToString(speciesSelection, datesSelection)
        self.selectedOutputOptions = selectedOutputOptions = wx.TextCtrl(parent, -1,text,
                       size=(300, 110), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        selectedOutputOptions.SetOwnFont(boldFont)
        selectedOutputOptions.SetForegroundColour("#1857DE")
        selectedOutputOptions.SetTTS("List of already selected outputs")
        selectedOutputOptions.SetInsertionPoint(0)
#        toto.Bind(wx.EVT_TEXT, self._evtText, mineralPhaseState)
        box5.Add(selectedOutputOptions, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        box51 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Create Display" ) , wx.VERTICAL)
        
# Properties control

		# box511 : Establishment of the placement for properties
        box511 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box511.SetMinSize((200,50))
        
        # Title of Combo box for selected dates
        label1 = wx.StaticText(parent,-1,"Format :",size=(70,-1));label1.SetTTS("Comment")
        label1.SetOwnFont(boldFont)
        box511.Add(label1, 0, wx.ALIGN_CENTER|wx.ALL, 1)
        
        # Combo box for selected dates
        self.availableformats = availableformats =  self.params.getParam(parameters.IOutputFormat_List).getValue()
        self.format = format = wx.ComboBox(parent, -1, "",(250, 20), (120, -1),availableformats, wx.CB_DROPDOWN)
        format.SetToolTipString("Saving format")
        self.format.SetValue(self.params.getParam(parameters.SavingFormat).getValue())
        box511.Add(format, 0., wx.ALIGN_CENTER|wx.ALL, 1)
        
        box51.Add(box511, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        # Create Button
        
        self.create = create = wx.Button(parent, -1, "Create", (200,100))
        toto.Bind(wx.EVT_BUTTON, self._create, self.create)
        box51.Add(create, 0, wx.CENTRE|wx.ALL, 2)
        
        
        box5.Add(box51, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        
        
        sizer.Add(box5, 1, wx.ALIGN_LEFT|wx.HORIZONTAL, 1 )
               
        parent.SetSizerAndFit(sizer)
        

    


    def _evtText(self, event):
        pass

    def _load(self, event):
        place = os.getcwd()
        wildcard = ".idat file (*.idat)|*.idat|All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self.getParent(), message="Choose a .idat file to open\n",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            try:
                self.dataFileCWD = dlg.GetPath()
                self.label.SetLabel("Data File :  \t" + self.dataFileCWD.split('/')[-1])
                self.availableDates = self._extractDates(self.dataFileCWD)
                self.availableSpecies = self._extractSpecies(self.dataFileCWD)
                self.selectedDate.SetItems(self.availableDates)
                self.selectedSpecies.SetItems(self.availableSpecies)
                self.speciesSelection = []
                self.datesSelection = []
                text = _dataToString(self.speciesSelection,self.datesSelection)
                self.selectedOutputOptions.SetValue(text)
                
            except:
                wx.MessageDialog(self.parent, "Problem with the file:" + self.dataFileCWD\
                , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
                
                
    def _create(self, event):
        if self.format.GetValue() not in self.availableformats:
            wx.MessageDialog(self.parent, "Output format is not registered"\
            , "Warning", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        
        # Making a tuple with quantities
        speciesAndQuantities = self.params.getParam(parameters.ExpectedOutputsQuantity_list).getValue()
        speciesTupleQuantity = {}
        print 'speciesAndQuantities = ', speciesAndQuantities
        
        for species in self.speciesSelection:
            speciesTupleQuantity.update({species : 'Concentration'})
        
        for double in speciesAndQuantities:
            print 'double = ', double
            if double[0] in self.speciesSelection:
                speciesTupleQuantity[double[0]] = double[1]
        
        print 'speciesTupleQuantity = ', speciesTupleQuantity 
            
        _saved2Plot(self.dataFileCWD, speciesTupleQuantity, self.datesSelection, self.format.GetValue(), self.availableSpecies)
        
        
    
    
        
    def _extractDates(self, fileName):
        openedfile = open(fileName, 'r')
        f = openedfile.read().split('\n')
        extractedDates = []
        for i in range(len(f)):
            if f[i] != '' and f[i].split()[0] == 'date':
                extractedDates.append(str(eval(f[i].split()[1])))
        openedfile.close()
        return extractedDates


    def _extractSpecies(self, fileName):
        openedfile = open(fileName, 'r')
        f = openedfile.read().split('\n')
        extractedSpecies = []
        indizConcentrations = f.index('Concentrations')
        if f[indizConcentrations+1] != '': extractedSpecies += f[indizConcentrations+1].split()
        if f[indizConcentrations+3] != '': extractedSpecies += f[indizConcentrations+3].split()
        openedfile.close()
        while 'None' in extractedSpecies:
            extractedSpecies.remove('None')
        return extractedSpecies
        
        
    #~~~~~~~~~~~~~~~~~
    # Outputs control
    #~~~~~~~~~~~~~~~~~
    
                
    def _addOutput(self, event):
        speciesChoice = self.selectedSpecies.GetValue()
        dateChoice = self.selectedDate.GetValue()
        
        if speciesChoice in self.availableSpecies and dateChoice in self.availableDates:
            if speciesChoice not in self.speciesSelection:
                self.speciesSelection.append(speciesChoice)
                self.datesSelection.append([])
            
            speciesIndiz = self.speciesSelection.index(speciesChoice)
            if float(dateChoice) not in self.datesSelection[speciesIndiz]:
                self.datesSelection[speciesIndiz].append(float(dateChoice))
                self.datesSelection[speciesIndiz].sort()
                text = _dataToString(self.speciesSelection,self.datesSelection)
                self.selectedOutputOptions.SetValue(text)
        
        
        
        
        
    
    def _delOutput(self, event):
        speciesChoice = self.selectedSpecies.GetValue()
        dateChoice = self.selectedDate.GetValue()
        
        if speciesChoice in self.speciesSelection:
            speciesIndiz = self.speciesSelection.index(speciesChoice)
            if float(dateChoice) in self.datesSelection[speciesIndiz]:
                self.datesSelection[speciesIndiz].remove(float(dateChoice))
                if self.datesSelection[speciesIndiz] == []:
                    self.datesSelection.pop(speciesIndiz)
                    self.speciesSelection.pop(speciesIndiz)
                text = _dataToString(self.speciesSelection,self.datesSelection)
                self.selectedOutputOptions.SetValue(text)
        

    def _onOk(self, params):
#
# saving outputs
#
        self.params.getParam(parameters.DataFileCWD).setValue(self.dataFileCWD)
        self.params.getParam(parameters.SavingFormat).setValue(self.format.GetValue())
        self.params.getParam(parameters.AvailableSpecies_list).setValue(self.availableSpecies)
        self.params.getParam(parameters.AvailableDates_list).setValue(self.availableDates)
        self.params.getParam(parameters.SpeciesSelection_list).setValue(self.speciesSelection)
        self.params.getParam(parameters.DatesSelection_list).setValue(self.datesSelection)
  
        return True
        
    
        
def _dataToString(speciesList, datesList):      
    text = ""
    for species in speciesList:
        text += 'Plot species ' + species + ' at :\n'
        for date in datesList[speciesList.index(species)]:
            text += '\t' + str(date) + '\n'
        text += '\n'
    return text



#
# Function for ploting
#

def _saved2Plot(fileName, speciesTuple, dates, format, availableSpecies):
    """ This functions extracts from fileName the species concentrations or physic values at different times. 
    fileName is the obtained during a simulation with function called - updateDataSaving - in module chemicaltransportmodule.py"""
    f = open(fileName, 'r')
    f = f.read().split('\n')
    aqueousEcart = 0    		# The difference between maxima and minima value of AqueousConcetration axis value
    aq = 0 						# Equal to 1 if there is already one Aqueous Concentration species which have been saved
    species = speciesTuple.keys()
    
    # we need to class Concentrations before, and next AqueousConcentrations
    aqSpecies    = []
    otherSpecies = []
    aqDates      = []
    otherDates   = []
    
    for specie in species:
        if speciesTuple[specie] == 'AqueousConcentration' :
            aqSpecies.append(specie)
            aqDates.append(dates[species.index(specie)])
        else:
            otherSpecies.append(specie)
            otherDates.append(dates[species.index(specie)])
    nb_other = len(otherSpecies)
    species = otherSpecies + aqSpecies
    dates = otherDates + aqDates
    
    if len(aqSpecies) == 1:
        speciesTuple[aqSpecies[0]] = 'Concentration'
    
    print 'species = ', species
    print 'dates = ', dates
    
    namesToDelete = []
    rotate = False
    gnuFile = open('duwab.dem', "w")
    gnuFile.write("reset\n")
    if format =='png':
        gnuFile.write("set term "+format+"\n")
    else:
        gnuFile.write("set term postscript\n")
    gnuFile.write("set style data lines\n")
    
    data2Plot = []
    
    print '1'
    for specie in species:
        print '2'
        data2Plot.append([])
        k = species.index(specie)
        zbl = 0
        
        for date in dates[k]:
            print '3'
                                                                                                #
                                                                                                # Checking the data
                                                                                                #
            l = dates[k].index(date)
            data2Plot[k].append([])
            # Locate the date's line
            i = 0
            indizLine = -1
            while i < len(f) and indizLine == -1:
                if f[i][0:4] == 'date':
                    if float(f[i].split()[1]) == date:
                        indizLine = i

                i+=1
            print '4', indizLine
            if indizLine == -1:
                return
            i = indizLine + 1
            XListe = []
            while i < len(f) and f[i][0:4] != 'date' and f[i] != '':
                # splited line
                splitedLine = f[i].split()
                XListe.append(eval(splitedLine[0]))
                data2Plot[k][l].append(eval(splitedLine[availableSpecies.index(specie)+1]))
                i+=1
            
                                                                                                #
                                                                                                # Saving the plot
                                                                                                #            
            print '5'
            temp = open('gnuTempFile'+str(k)+'_'+str(l)+'.dat', "w")
            namesToDelete.append('gnuTempFile'+str(k)+'_'+str(l)+'.dat')
            rot  = 'x'
            rot2 = 'y'
            
            speciesDates = ''
            if speciesTuple[specie] == 'Concentration' :
                for value in dates[k]:
                    speciesDates += str(value) + '_'
                gnuFile.write("set output \"int_"+str(specie)+"_"+str(speciesDates)+"y."+format+"\"\n")
            elif speciesTuple[specie] == 'AqueousConcentration' :
                gnuFile.write("set output \"int_AqueousConcentration."+format+"\"\n")
                                                                                                #
                                                                                                # Label and scale of output axis
                                                                                                #
            print '6'
            gnuFile.write("set title '" + str(specie) +" profil'\n")
            
            ecart = max(data2Plot[k][l])-min(data2Plot[k][l])
            
            if speciesTuple[specie] == 'AqueousConcentration' :
                if ecart < aqueousEcart: ecart = aqueousEcart
                else: aqueousEcart = ecart
            
            
            _gnuWriteStep1(gnuFile, rot, ecart, specie)
            
                                                                                                #
                                                                                                # plot
                                                                                                #
            last_var = data2Plot[k][l]
            abscisse = XListe
            courbes  = []
            
            if speciesTuple[specie] == 'AqueousConcentration' :
                if zbl == 0:
                    legend = ' title "'+ str(specie) + '" linetype ' + str((k-nb_other)%7 +1)
                else:
                    legend = ' notitle linetype ' + str((k-nb_other)%7 +1)
            elif speciesTuple[specie] == 'Concentration' :
                legend = ' title "'+ str(date) + '"'
            
            _gnuWriteStep2(gnuFile, temp, k, l, legend, zbl, last_var, abscisse, rot, aq, speciesTuple[specie])
            
            
            zbl =1
            if speciesTuple[specie] == 'AqueousConcentration' : aq = 1

    gnuFile.write("exit\n")
    gnuFile.close()
    
    time.sleep(1)
    print '7'
    
#    subprocess.Popen("gnuplot duwab.dem", shell = True)

    print '8'
    
    
#    for i in range(len(namesToDelete)):
#        os.remove(namesToDelete[i])

    
def _gnuWriteStep1(gnuFile, rot, ecart, specie):
    if rot == 'x':
        rot2 = 'y'
    else :
        rot2 = 'x'
        
    if rot == 'x':
        gnuFile.write("set " + rot + "tics 0," + str(ecart/3) + " rotate by -20\n")
    else:
        gnuFile.write("set " + rot + "tics 0," + str(ecart/3)+"\n")
    gnuFile.write("set format " + rot + " \"%10.4e\"\n")
    gnuFile.write("set " + rot + 'label \"' + str(specie) + '\"\n')
                                                                                        #
                                                                                        # Label and scale of depth axis
                                                                                        #        
    ecart = 12.5
    gnuFile.write('set ' + rot2 + 'label \"m\"\n')
    gnuFile.write('set ' + rot2 + 'tics 0,' + str(ecart/5)+'\n')
    gnuFile.write('set format ' + rot2 + ' \"%5.2f\"\n')
    
    
def _gnuWriteStep2(gnuFile, temp, k, l, legend, zbl, last_var, abscisse, rot, aq, cType):
    if zbl == 0 and (aq == 0 or cType != 'AqueousConcentration'):
        gnuFile.write('plot ' + '"gnuTempFile'+str(k)+'_'+str(l)+'.dat" ' + 'using 1:2' + legend +'\n')
    else:
        gnuFile.write('replot ' + '"gnuTempFile'+str(k)+'_'+str(l)+'.dat" ' + 'using 1:2'+ legend +'\n')
    for i in range(len(last_var)):
        if rot == 'x':
            temp.write(" %10.5e %10.5e\n"%(last_var[i], abscisse[i]))
        else:
            temp.write(" %10.5e %10.5e\n"%(abscisse[i], last_var[i]))
            temp.write("e\n")
