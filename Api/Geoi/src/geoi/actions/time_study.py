import wx
import math
from geoi.actions.params_action import ParamsAction
from geoi import parameters

description ="""
       Used to obtain the results versus time
       """
HELP = """
       need to set an help
       """
class TimeStudy(ParamsAction):

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Time study",description  =description,help=HELP) 

    def _createInterface(self, parent, params):
        toto = self.GetDialogPanel()
        self.parent = parent
        self.params = params
        
        outputComboboxDefault = ""
        
        self.meshFile = params.getParam(parameters.Gmsh_Name_File2).getValue()
        f1 = open(self.meshFile,"r")
        sizer = wx.BoxSizer( wx.VERTICAL )
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
     
        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box1.SetMinSize((300,30))
        grid1 = wx.FlexGridSizer( 0, 1, 0, 0 )
        grid1.SetFlexibleDirection( wx.HORIZONTAL)
        label1 = wx.StaticText(parent, -1, "Output to study")
        label1.SetHelpText("")
        box1.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        availableOutputList = self.params.getParam(parameters.ExpectedOutputs_list).getValue()
        self.availableOutputCombo = availableOutputCombo =\
        wx.ComboBox(parent, -1, outputComboboxDefault,(250, 20), (200, -1),availableOutputList, wx.CB_DROPDOWN)
        box1.Add(availableOutputCombo, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add( box1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )  
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        box2 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box2.SetMinSize((300,110))
        
        label1 = wx.StaticText(parent, -1, "Point")
        label1.SetHelpText("Select a point")
        box2.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        a=f1.readline().rstrip('\n\r').split(" ")
        while "$Nodes" not in a :
            a=f1.readline().rstrip('\n\r').split(" ")
        a=f1.readline().rstrip('\n\r').split(" ")
        i=0
        while a[i]=="" or a[i]==" " :
            i+=1
        numberOfPoints = int(a[i])
        availablePoints = []
        for i in range (numberOfPoints) :
            availablePoints.append(str(i+1))
        self.availablePointsCombo = availablePointsCombo =\
        wx.ComboBox(parent, -1, outputComboboxDefault,(250, 20), (200, -1),availablePoints, wx.CB_DROPDOWN)
        box2.Add(availablePointsCombo, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        toto.Bind(wx.EVT_COMBOBOX, self._obtainCoord, self.availablePointsCombo)
        
        self.xCtrl = xCtrl = wx.TextCtrl(parent, -1, "", size=(130,-1))
        self.yCtrl = yCtrl = wx.TextCtrl(parent, -1, "", size=(130,-1))
        self.zCtrl = zCtrl = wx.TextCtrl(parent, -1, "", size=(130,-1))
        
        label21 = wx.StaticText(parent, -1, "X")
        box2.Add(label21, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box2.Add(xCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        label22 = wx.StaticText(parent, -1, "Y")
        box2.Add(label22, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box2.Add(yCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        label23 = wx.StaticText(parent, -1, "Z")
        box2.Add(label23, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box2.Add(zCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.PointCtrl = PointCtrl = wx.CheckBox( parent, -1, "",style = 0)
        
        box2.Add(PointCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sizer.Add( box2, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )         
      
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        
        box3 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.HORIZONTAL)
        box3.SetMinSize((300,50))
        grid3 = wx.FlexGridSizer( 2, 5, 2, 0 )
        grid3.SetFlexibleDirection( wx.HORIZONTAL)
        
        self.xCtrlCoor = xCtrlCoor = wx.TextCtrl(parent, -1, "", size=(90,-1))
        self.yCtrlCoor = yCtrlCoor = wx.TextCtrl(parent, -1, "", size=(90,-1))
        self.zCtrlCoor = zCtrlCoor = wx.TextCtrl(parent, -1, "", size=(90,-1))
        
        label31 = wx.StaticText(parent, -1, "X")
        box3.Add(label31, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box3.Add(xCtrlCoor, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        label32 = wx.StaticText(parent, -1, "Y")
        box3.Add(label32, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box3.Add(yCtrlCoor, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        label33 = wx.StaticText(parent, -1, "Z")
        box3.Add(label33, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box3.Add(zCtrlCoor, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        label34 = wx.StaticText(parent, -1, "precision")
        box3.Add(label34, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.precision = precision = wx.TextCtrl(parent, -1, "", size=(90,-1))
        
        box3.Add(precision, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.search = wx.Button(parent, -1, "Search", (520,250))
        box3.Add(self.search, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        toto.Bind(wx.EVT_BUTTON, self._search, self.search)
        
        self.PointCoor = PointCoor = wx.TextCtrl( parent, -1, "",style = 0)
        label35 = wx.StaticText(parent, -1, "Point")
        box3.Add(label35, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box3.Add(PointCoor, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sizer.Add( box3, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        
        self.PointCoorCtrl = PointCoorCtrl = wx.CheckBox( parent, -1, "",style = 0)
        
        box3.Add(PointCoorCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
 
 
        listAvailable = []
        for parameter in self.params.getParam( parameters.TimeStudy).getValue() :
            element = parameter[0] + "_at_Point_" + str(parameter[1])
            listAvailable.append(element) 
        self.alreadyCreated = wx.ComboBox(parent, -1, "",(300, 20), (300, -1),listAvailable , wx.CB_DROPDOWN)
        sizer.Add(self.alreadyCreated, 0, wx.LEFT|wx.ALL, 5 )
        """
        self.information = wx.TextCtrl(parent, -1,\
                        size=(300, 110), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        toSay = ""
        for parameter in self.params.getParam( parameters.TimeStudy).getValue() :
            toSay += parameter[0] + " at Point " + str(parameter[1]) + ".  "
        self.information.SetValue(toSay)
        sizer.Add(self.information, 0, wx.LEFT|wx.ALL, 5 )
        """
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        
        self.destroy = wx.Button(parent, -1, "Destroy", (370,250))
        
        toto.Bind(wx.EVT_BUTTON, self._destroy, self.destroy)
        
        self.apply = wx.Button(parent, -1, "Apply", (520,250))
        
        toto.Bind(wx.EVT_BUTTON, self._applyZone, self.apply)
        
        parent.SetSizerAndFit(sizer)
        
        f1.close()
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 


    def _obtainCoord(self, event):
        number = self.availablePointsCombo.GetValue()
        f1 = open(self.meshFile,"r")
        a=f1.readline().rstrip('\n\r').split(" ")
        while "$Nodes" not in a :
            a=f1.readline().rstrip('\n\r').split(" ")
        a=f1.readline().rstrip('\n\r').split(" ")
        a=f1.readline().rstrip('\n\r').split(" ")
        while a[0]!=number and a[1]!=number :
            a=f1.readline().rstrip('\n\r').split(" ")
        if a[0]==number :
            i=1
        else :
            i=2
        for j in range(3) :
            while a[i]=="" or a[i]==" " :
                i+=1
            if j == 0 :
                self.xCtrl.SetValue(a[i])
            elif j ==1 :
                self.yCtrl.SetValue(a[i])
            else :
                self.zCtrl.SetValue(a[i])
            i+=1 
            
            
    def _search(self,event) :
        if self.xCtrlCoor.GetValue() != "" :
            x = float(self.xCtrlCoor.GetValue()) 
        else :
            x=0
        if self.yCtrlCoor.GetValue() != "" :
            y = float(self.yCtrlCoor.GetValue()) 
        else :
            y=0
        if self.zCtrlCoor.GetValue() != "" :
            z = float(self.zCtrlCoor.GetValue()) 
        else :
            z=0
        mini = 10 * float(self.precision.GetValue())
        f1 = open(self.meshFile,"r")
        a=f1.readline().rstrip('\n\r').split(" ")
        while "$Nodes" not in a :
            a=f1.readline().rstrip('\n\r').split(" ")
        a=f1.readline().rstrip('\n\r').split(" ")
        a=f1.readline().rstrip('\n\r').split(" ")   
        while "$EndNodes" not in a :
            i=0
            for j in range(4) :
                while a[i]=="" :
                    i+=1
                if j == 0 :
                    nbr = a[i] 
                elif j == 1 :
                    x1 = float(a[i])
                elif j == 2 :
                    y1 = float(a[i])
                else :
                    z1 = float(a[i])
                i+=1        
            dis = math.sqrt((x-x1)**2+(y-y1)**2+(z-z1)**2)
            if dis < mini :
                mini = dis
                nbrFound = nbr
                xFound = x1
                yFound = y1
                zFound = z1
            a=f1.readline().rstrip('\n\r').split(" ")
        if mini > float(self.precision.GetValue()) :
            self.PointCoor.SetValue("not found")
        else :
            self.PointCoor.SetValue(nbrFound)    
            
    def _destroy(self,event) :
        if self.alreadyCreated.GetValue() != "" :
            toRemove = self.alreadyCreated.GetValue()
            index = self.alreadyCreated.GetSelection()
            self.alreadyCreated.Delete(index)
            output = toRemove.split("_at_Point_")[0]                 
            point = int(toRemove.split("_at_Point_")[1])
            self.params.getParam( parameters.TimeStudy).getValue().remove([output,point])
                   
    def _applyZone(self, event):  
        if self._verification() :   
            if self.PointCtrl.IsChecked()==True :
                point = self.availablePointsCombo.GetValue() 
            else :   
                point = self.PointCoor.GetValue() 
            timeStudy = self.params.getParam( parameters.TimeStudy).getValue()
            print self.availableOutputCombo.GetValue()
            timeStudy.append([self.availableOutputCombo.GetValue(),int(point)]) 
            self.params.getParam( parameters.TimeStudy).setValue(timeStudy)
            self.alreadyCreated.Append(self.availableOutputCombo.GetValue() + "_at_Point_" +  point)
            

    def _verification(self) :   
        if self.PointCtrl.IsChecked()==True :
            if self.PointCoorCtrl.IsChecked()==True:
                dlg = wx.MessageDialog(self.getParent(), 'The two check box are checked',
                               'A Message Box',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               )
                val = dlg.ShowModal()
                dlg.Destroy()
                result = False
            else :
                if self.availableOutputCombo.GetValue() != "" and self.availablePointsCombo.GetValue() != "" :
                    result = True
                elif self.availableOutputCombo.GetValue() == "" :
                    dlg = wx.MessageDialog(self.getParent(), 'You need to choose an output',
                               'A Message Box',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               )
                    val = dlg.ShowModal()
                    dlg.Destroy()
                    result = False
                else :
                    dlg = wx.MessageDialog(self.getParent(), 'You need to choose a point',
                               'A Message Box',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               )
                    val = dlg.ShowModal()
                    dlg.Destroy()
                    result = False
        elif self.PointCoorCtrl.IsChecked()==True :
            if self.availableOutputCombo.GetValue() != "" and self.PointCoor.GetValue() != "" and self.PointCoor.GetValue() != "not found":
                result = True
            elif self.availableOutputCombo.GetValue() == "" :
                dlg = wx.MessageDialog(self.getParent(), 'You need to choose an output',
                           'A Message Box',
                           wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                           )
                val = dlg.ShowModal()
                dlg.Destroy()
                result = False
            elif self.PointCoor.GetValue() != "":
                dlg = wx.MessageDialog(self.getParent(), 'You need to choose a point',
                           'A Message Box',
                           wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                           )
                val = dlg.ShowModal()
                dlg.Destroy()
                result = False
            else :
                dlg = wx.MessageDialog(self.getParent(), 'Choose a correct point',
                           'A Message Box',
                           wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                           )
                val = dlg.ShowModal()
                dlg.Destroy()
                result = False
        else :
            dlg = wx.MessageDialog(self.getParent(), 'You need to check a checkbox',
                               'A Message Box',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               )
            val = dlg.ShowModal()
            dlg.Destroy()
            result = False
        return result

        



    def _onOk(self, params):
        return True
            
