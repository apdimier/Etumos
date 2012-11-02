import wx

from geoi.actions.params_action import ParamsAction
from geoi import parameters

ilabel = "horizontal structured mesh definition "
jlabel = "vertical structured mesh definition   "

DISCRETISATION_BY_LABEL = {'Upwind':parameters.MT3D_ADVECTION_UPWIND,
                           'Central':parameters.MT3D_ADVECTION_CENTRAL,
                           'T.V.D.':parameters.MT3D_ADVECTION_TVD }

PRECONDITONER_BY_LABEL = {'Jacobi':parameters.MT3D_CGP_JACOBI,
                          'MIC':parameters.MT3D_CGP_MIC,
                          'SSOR':parameters.MT3D_CGP_SSOR }

description = \
       """ 
       Used as a constructor for a 2 dimensional cartesian mesh
       """
HELP = """
       A <b>structured mesh</b> is a mesh with an algebraic relation between lines and points.<br>
       Here we handle a <b>cartesian structued mesh</b> enabling a mt3d simulation.

       """
class MeshConstructor(ParamsAction):
    """
       A structured mesh is a mesh with an algebraic relation between lines and points.
       the position of point (i,j) is known by the position of point (i,0) and (0,j) on the axes
       Here we handle a cartesian structued mesh enabling a mt3d simulation.
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Cartesian mesh constructor",description  =description,help=HELP)
        self.radios = None
        self.choice = None
        self;win = win

    def _createInterface(self, parent, params):
        
   
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.parent = parent   
        self.meshinI = params.getParam(parameters.Mesh_list_InI)
        self.meshinJ = params.getParam(parameters.Mesh_list_InJ)
        
        box1 = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "mesh definition:" ) , wx.VERTICAL )
        box1.SetMinSize((600,200))
        grid1 = wx.FlexGridSizer( 0, 4, 0, 0 )
        grid1.SetFlexibleDirection( wx.VERTICAL)

        radios1 = []
        choice1 = None
# I mesh                                                 
        self.cpi = cpi = wx.CollapsiblePane(parent, label=ilabel,
                                          style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE,size=(600,125))
#        toto = self.GetDialogPanel()
#        toto.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cpi)
        
        self.IMeshControl(cpi.GetPane())

        box1.Add(cpi, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        pSizer = wx.BoxSizer(wx.VERTICAL)
        box1.Add(pSizer, 0, wx.ALIGN_CENTER|wx.ALL,1)
# J mesh                                          
        self.cpj = cpj = wx.CollapsiblePane(parent, label=jlabel,
                                          style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE,size=(600,125))
                                          
        toto = self.GetDialogPanel()
        toto.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cpj)
        
        self.JMeshControl(cpj.GetPane())
        box1.Add(cpj, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        pSizer = wx.BoxSizer(wx.VERTICAL)
        box1.Add(pSizer, 0, wx.ALIGN_CENTRE|wx.ALL,1)

        self.radios1 = radios1
        self.choice1 = choice1
        
        sizer.Add( box1, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        parent.SetSizerAndFit(sizer)

        
    def OnPaneChanged(self, cp,evt=None):
        if evt:
            self.log.write('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % evt.Collapsed)
        
    def IMeshControl(self, pane):
        
        addrSizer = wx.FlexGridSizer(rows = 3,cols=1, hgap=2, vgap=2)
        addrSizer.AddGrowableCol(1)
#        iext = wx.StaticText(pane, -1, "horizontal ext.:")
#        addrSizer.Add(iext, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        
        iextSizer = wx.BoxSizer(wx.HORIZONTAL)
        cst0Lbl = wx.StaticText(pane, -1, "I nb cells per zone:",size=(170,20))
        iextSizer.Add(cst0Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        mI = self.meshinI.getValue()
        self.i1 = i1 = wx.TextCtrl(pane, -1, str(mI[0][0]), size=(50,-1));iextSizer.Add(i1, 0, wx.ALIGN_LEFT|wx.RIGHT, 1)
        self.i2 = i2 = wx.TextCtrl(pane, -1, str(mI[1][0]), size=(50,-1));iextSizer.Add(i2, 0, wx.LEFT|wx.RIGHT, 1)
        self.i3 = i3 = wx.TextCtrl(pane, -1, str(mI[2][0]), size=(50,-1));iextSizer.Add(i3, 0, wx.LEFT|wx.RIGHT, 1)
        self.i4 = i4 = wx.TextCtrl(pane, -1, str(mI[3][0]), size=(50,-1));iextSizer.Add(i4, 0, wx.LEFT|wx.RIGHT, 1)
        self.i5 = i5 = wx.TextCtrl(pane, -1, str(mI[4][0]), size=(50,-1));iextSizer.Add(i5, 0, wx.LEFT|wx.RIGHT, 1)
        self.i6 = i6 = wx.TextCtrl(pane, -1, str(mI[5][0]), size=(50,-1));iextSizer.Add(i6, 0, wx.LEFT|wx.RIGHT, 1)
        self.i7 = i7 = wx.TextCtrl(pane, -1, str(mI[6][0]), size=(50,-1));iextSizer.Add(i7, 0, wx.LEFT|wx.RIGHT, 1)
        self.i8 = i8 = wx.TextCtrl(pane, -1, str(mI[7][0]), size=(50,-1));iextSizer.Add(i8, 0, wx.LEFT|wx.RIGHT, 1)
        
        addrSizer.Add(iextSizer, 0, wx.ALIGN_LEFT|wx.ALL)
        
        extSizer = wx.BoxSizer(wx.HORIZONTAL)
        cst1Lbl = wx.StaticText(pane, -1, "I zone extension in meters:",size=(170,20))
        extSizer.Add(cst1Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.l1 = l1 = wx.TextCtrl(pane, -1, str(mI[0][1]), size=(50,-1));extSizer.Add(l1, 0, wx.ALIGN_LEFT|wx.RIGHT, 1)
        self.l2 = l2 = wx.TextCtrl(pane, -1, str(mI[1][1]), size=(50,-1));extSizer.Add(l2, 0, wx.LEFT|wx.RIGHT, 1)
        self.l3 = l3 = wx.TextCtrl(pane, -1, str(mI[2][1]), size=(50,-1));extSizer.Add(l3, 0, wx.LEFT|wx.RIGHT, 1)
        self.l4 = l4 = wx.TextCtrl(pane, -1, str(mI[3][1]), size=(50,-1));extSizer.Add(l4, 0, wx.LEFT|wx.RIGHT, 1)
        self.l5 = l5 = wx.TextCtrl(pane, -1, str(mI[4][1]), size=(50,-1));extSizer.Add(l5, 0, wx.LEFT|wx.RIGHT, 1)
        self.l6 = l6 = wx.TextCtrl(pane, -1, str(mI[5][1]), size=(50,-1));extSizer.Add(l6, 0, wx.LEFT|wx.RIGHT, 1)
        self.l7 = l7 = wx.TextCtrl(pane, -1, str(mI[6][1]), size=(50,-1));extSizer.Add(l7, 0, wx.LEFT|wx.RIGHT, 1)
        self.l8 = l8 = wx.TextCtrl(pane, -1, str(mI[7][1]), size=(50,-1));extSizer.Add(l8, 0, wx.LEFT|wx.RIGHT, 1)
        
        addrSizer.Add(extSizer, 0, wx.ALIGN_LEFT|wx.ALL)
        
        cst2Lbl = wx.StaticText(pane, -1, "I pt distribution coeff.:",size=(170,20))
        powSizer = wx.BoxSizer(wx.HORIZONTAL)
        powSizer.Add(cst2Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.p1 = p1 = wx.TextCtrl(pane, -1, str(mI[0][2]), size=(50,-1));powSizer.Add(p1, 0, wx.LEFT|wx.RIGHT, 1)
        self.p2 = p2 = wx.TextCtrl(pane, -1, str(mI[1][2]), size=(50,-1));powSizer.Add(p2, 0, wx.LEFT|wx.RIGHT, 1)
        self.p3 = p3 = wx.TextCtrl(pane, -1, str(mI[2][2]), size=(50,-1));powSizer.Add(p3, 0, wx.LEFT|wx.RIGHT, 1)
        self.p4 = p4 = wx.TextCtrl(pane, -1, str(mI[3][2]), size=(50,-1));powSizer.Add(p4, 0, wx.LEFT|wx.RIGHT, 1)
        self.p5 = p5 = wx.TextCtrl(pane, -1, str(mI[4][2]), size=(50,-1));powSizer.Add(p5, 0, wx.LEFT|wx.RIGHT, 1)
        self.p6 = p6 = wx.TextCtrl(pane, -1, str(mI[5][2]), size=(50,-1));powSizer.Add(p6, 0, wx.LEFT|wx.RIGHT, 1)
        self.p7 = p7 = wx.TextCtrl(pane, -1, str(mI[6][2]), size=(50,-1));powSizer.Add(p7, 0, wx.LEFT|wx.RIGHT, 1)
        self.p8 = p8 = wx.TextCtrl(pane, -1, str(mI[7][2]), size=(50,-1));powSizer.Add(p8, 0, wx.LEFT|wx.RIGHT, 1)
        addrSizer.Add(powSizer, 0, wx.ALIGN_LEFT|wx.ALL)
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)
        pane.SetSizer(border)
        
    def JMeshControl(self, pane):
        
        addrSizer = wx.FlexGridSizer(rows = 3,cols=1, hgap=2, vgap=2)
        addrSizer.AddGrowableCol(1)
#        iext = wx.StaticText(pane, -1, "horizontal ext.:")
#        addrSizer.Add(iext, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        
        JextSizer = wx.BoxSizer(wx.HORIZONTAL)
        cstj0Lbl = wx.StaticText(pane, -1, "J nb cells per zone:",size=(170,20))
        JextSizer.Add(cstj0Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        mj = self.meshinJ.getValue()
        self.j1 = j1 = wx.TextCtrl(pane, -1, str(mj[0][0]), size=(50,-1));JextSizer.Add(j1, 0, wx.ALIGN_LEFT|wx.RIGHT, 1)
        self.j2 = j2 = wx.TextCtrl(pane, -1, str(mj[1][0]), size=(50,-1));JextSizer.Add(j2, 0, wx.LEFT|wx.RIGHT, 1)
        self.j3 = j3 = wx.TextCtrl(pane, -1, str(mj[2][0]), size=(50,-1));JextSizer.Add(j3, 0, wx.LEFT|wx.RIGHT, 1)
        self.j4 = j4 = wx.TextCtrl(pane, -1, str(mj[3][0]), size=(50,-1));JextSizer.Add(j4, 0, wx.LEFT|wx.RIGHT, 1)
        self.j5 = j5 = wx.TextCtrl(pane, -1, str(mj[4][0]), size=(50,-1));JextSizer.Add(j5, 0, wx.LEFT|wx.RIGHT, 1)
        self.j6 = j6 = wx.TextCtrl(pane, -1, str(mj[5][0]), size=(50,-1));JextSizer.Add(j6, 0, wx.LEFT|wx.RIGHT, 1)
        self.j7 = j7 = wx.TextCtrl(pane, -1, str(mj[6][0]), size=(50,-1));JextSizer.Add(j7, 0, wx.LEFT|wx.RIGHT, 1)
        self.j8 = j8 = wx.TextCtrl(pane, -1, str(mj[7][0]), size=(50,-1));JextSizer.Add(j8, 0, wx.LEFT|wx.RIGHT, 1)
        
        addrSizer.Add(JextSizer, 0, wx.ALIGN_LEFT|wx.ALL)
        
        extSizerj = wx.BoxSizer(wx.HORIZONTAL)
        cstj1Lbl = wx.StaticText(pane, -1, "J zone extension in meters:",size=(170,20))
        extSizerj.Add(cstj1Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.jl1 = jl1 = wx.TextCtrl(pane, -1, str(mj[0][1]), size=(50,-1));extSizerj.Add(jl1, 0, wx.ALIGN_LEFT|wx.RIGHT, 1)
        self.jl2 = jl2 = wx.TextCtrl(pane, -1, str(mj[1][1]), size=(50,-1));extSizerj.Add(jl2, 0, wx.LEFT|wx.RIGHT, 1)
        self.jl3 = jl3 = wx.TextCtrl(pane, -1, str(mj[2][1]), size=(50,-1));extSizerj.Add(jl3, 0, wx.LEFT|wx.RIGHT, 1)
        self.jl4 = jl4 = wx.TextCtrl(pane, -1, str(mj[3][1]), size=(50,-1));extSizerj.Add(jl4, 0, wx.LEFT|wx.RIGHT, 1)
        self.jl5 = jl5 = wx.TextCtrl(pane, -1, str(mj[4][1]), size=(50,-1));extSizerj.Add(jl5, 0, wx.LEFT|wx.RIGHT, 1)
        self.jl6 = jl6 = wx.TextCtrl(pane, -1, str(mj[5][1]), size=(50,-1));extSizerj.Add(jl6, 0, wx.LEFT|wx.RIGHT, 1)
        self.jl7 = jl7 = wx.TextCtrl(pane, -1, str(mj[6][1]), size=(50,-1));extSizerj.Add(jl7, 0, wx.LEFT|wx.RIGHT, 1)
        self.jl8 = jl8 = wx.TextCtrl(pane, -1, str(mj[7][1]), size=(50,-1));extSizerj.Add(jl8, 0, wx.LEFT|wx.RIGHT, 1)
        
        addrSizer.Add(extSizerj, 0, wx.ALIGN_LEFT|wx.ALL)
        
        cstj2Lbl = wx.StaticText(pane, -1, "J pt distribution coeff.:",size=(170,20))
        powSizerj = wx.BoxSizer(wx.HORIZONTAL)
        powSizerj.Add(cstj2Lbl, -1,wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        self.jp1 = jp1 = wx.TextCtrl(pane, -1, str(mj[0][2]), size=(50,-1));powSizerj.Add(jp1, 0, wx.LEFT|wx.RIGHT, 1)
        self.jp2 = jp2 = wx.TextCtrl(pane, -1, str(mj[1][2]), size=(50,-1));powSizerj.Add(jp2, 0, wx.LEFT|wx.RIGHT, 1)
        self.jp3 = jp3 = wx.TextCtrl(pane, -1, str(mj[2][2]), size=(50,-1));powSizerj.Add(jp3, 0, wx.LEFT|wx.RIGHT, 1)
        self.jp4 = jp4 = wx.TextCtrl(pane, -1, str(mj[3][2]), size=(50,-1));powSizerj.Add(jp4, 0, wx.LEFT|wx.RIGHT, 1)
        self.jp5 = jp5 = wx.TextCtrl(pane, -1, str(mj[4][2]), size=(50,-1));powSizerj.Add(jp5, 0, wx.LEFT|wx.RIGHT, 1)
        self.jp6 = jp6 = wx.TextCtrl(pane, -1, str(mj[5][2]), size=(50,-1));powSizerj.Add(jp6, 0, wx.LEFT|wx.RIGHT, 1)
        self.jp7 = jp7 = wx.TextCtrl(pane, -1, str(mj[6][2]), size=(50,-1));powSizerj.Add(jp7, 0, wx.LEFT|wx.RIGHT, 1)
        self.jp8 = jp8 = wx.TextCtrl(pane, -1, str(mj[7][2]), size=(50,-1));powSizerj.Add(jp8, 0, wx.LEFT|wx.RIGHT, 1)
        addrSizer.Add(powSizerj, 0, wx.ALIGN_LEFT|wx.ALL)
        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)
        pane.SetSizer(border)

    def _onOk(self, params):
    
# mesh line direction choice    
        listInI = []
        ict = 1
        if int(self.i1.GetValue())<=0:
            message = "for a mesh zone, you have \n"+\
            				       "to set the number of points\n to a positive number"+\
            				       " check the mesh zones points number"
            dlg = wx.MessageDialog(self.parent,message,
                               'A Message Box',
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            self.i1.SetValue("1")   

        _control(self.parent,listInI,self.i1.GetValue(),self.l1.GetValue(),float(self.p1.GetValue()),ict)
        _control(self.parent,listInI,self.i2.GetValue(),self.l2.GetValue(),float(self.p2.GetValue()),ict)
        _control(self.parent,listInI,self.i3.GetValue(),self.l3.GetValue(),float(self.p3.GetValue()),ict)
        _control(self.parent,listInI,self.i4.GetValue(),self.l4.GetValue(),float(self.p4.GetValue()),ict)
        _control(self.parent,listInI,self.i5.GetValue(),self.l5.GetValue(),float(self.p5.GetValue()),ict)
        _control(self.parent,listInI,self.i6.GetValue(),self.l6.GetValue(),float(self.p6.GetValue()),ict)
        _control(self.parent,listInI,self.i7.GetValue(),self.l7.GetValue(),float(self.p7.GetValue()),ict)
        _control(self.parent,listInI,self.i8.GetValue(),self.l8.GetValue(),float(self.p8.GetValue()),ict)
        MeshLineInILength = 0.
        MeshLineInINumberOfCells = 0
        for ind in listInI:
            if ind[0]!=0:
                MeshLineInINumberOfCells += ind[0]
                MeshLineInILength += ind[1]
            else:
                break
        params.getParam(parameters.MeshLineInINumberOfCells).setValue(MeshLineInINumberOfCells)
        params.getParam(parameters.MeshLineInILength).setValue(MeshLineInILength)
        params.getParam(parameters.Mesh_list_InI).setValue(listInI)
        listInJ = []
        _control(self.parent,listInJ,self.j1.GetValue(),self.jl1.GetValue(),float(self.jp1.GetValue()),ict)
        _control(self.parent,listInJ,self.j2.GetValue(),self.jl2.GetValue(),float(self.jp2.GetValue()),ict)
        _control(self.parent,listInJ,self.j3.GetValue(),self.jl3.GetValue(),float(self.jp3.GetValue()),ict)
        _control(self.parent,listInJ,self.j4.GetValue(),self.jl4.GetValue(),float(self.jp4.GetValue()),ict)
        _control(self.parent,listInJ,self.j5.GetValue(),self.jl5.GetValue(),float(self.jp5.GetValue()),ict)
        _control(self.parent,listInJ,self.j6.GetValue(),self.jl6.GetValue(),float(self.jp6.GetValue()),ict)
        _control(self.parent,listInJ,self.j7.GetValue(),self.jl7.GetValue(),float(self.jp7.GetValue()),ict)
        _control(self.parent,listInJ,self.j8.GetValue(),self.jl8.GetValue(),float(self.jp8.GetValue()),ict)
        MeshLineInJLength = 0.
        MeshLineInJNumberOfCells = 0
        for ind in listInJ:
            if ind[0]!=0:
                MeshLineInJNumberOfCells += ind[0]
                MeshLineInJLength += ind[1]
            else:
                break
        params.getParam(parameters.MeshLineInJNumberOfCells).setValue(MeshLineInJNumberOfCells)
        params.getParam(parameters.MeshLineInJLength).setValue(MeshLineInJLength)
        params.getParam(parameters.Mesh_list_InJ).setValue(listInJ)
        return True
        
def _control(parent,liste,inter,length,power,ict):

    if int(inter) != 0 and abs(float(length)) > 1.e-10 and ict ==1:
        if (int(inter)<0) :
            message = "for a mesh zone, you have \n"+\
            				       "to set the number of points\n to a positive number"+\
            				       " check the mesh zones points number"
            dlg = wx.MessageDialog(parent,message,
                               'A Message Box',
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            liste.append((0,0.,1))
            it = 0
        elif float(length)<0:
            message = "for a mesh zone, you have \n"+\
            				       "to set the length\n to a positive number"+\
            				       " check the mesh zones points number"
            dlg = wx.MessageDialog(parent,message,
                               'A Message Box',
                               wx.OK | wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            liste.append((int(inter),abs(float(length)),_pcontrol(power)))
        else:
            liste.append((int(inter),abs(float(length)),_pcontrol(power)))
    else:
        it = 0
        liste.append((0,0.,1))

def _pcontrol(power):
    if power > 1:
        power = min(1.1,abs(power))
    elif power > 0.9:
        power = max(0.9,abs(power))
    else:
        power = 1.
    return power
    
