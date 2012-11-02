
import wx

from geoi.gui.validators import ParameterValidator


class MultiFieldDialog(wx.Dialog):
    """ a generic dialog that will input a list of fields
        The result values as edited in the dialog are directly set in the
        parameters
    """

    def __init__(self, parent, title, params, help=None ):
        wx.Dialog.__init__(self,parent, -1, title, style=wx.RESIZE_BORDER |wx.CAPTION)
        
        self._grid = None
        self._params = params
        self._editors = None
        self._default_bg_color = None
        self.createInterface(self, params)
        self._editors[params[0].getName()].SetFocus()
  
    def getGrid(self):
        "return the FlexGridSizer that layouts the labels and editors"
        return self._grid

    def setEditorIsReadOnly(self, name):
        editor = self.getEditorByName(name)
        editor.SetEditable(False)
        # unbind events


    def getEditorsDict(self):
        "return a dict whose keys are the parameters names and the values the text ctrl"
        return self._editors

    def getEditorByName(self, name):
        "return an editor (TextCtrl) by its parameter name"
        return self.getEditorsDict()[name]

    def isValid(self):
        """true iff all values are valid, to be used by callers"""
        for p in self._params:
            if not p.checkValue(p.getValue()):
                return False
        return True

    def addToGrid(self, component, col):
        self._grid.Add( component, col, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 5 )

    def createInterface(self, parent, params):
        sizer = wx.BoxSizer( wx.VERTICAL )
        box = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.VERTICAL )
        self._grid = grid = wx.FlexGridSizer( 0, 2, 0, 0 )
        grid.AddGrowableCol(1, 1)
        self._editors = editors = {}
        for p in params:
            t = wx.StaticText( parent, -1, p.getName() )
            t.SetToolTipString( p.getDescription() )
            self.addToGrid(t, 0)

            edit = self.createEditor(parent, p)
            editors[p.getName()] = edit
            self._default_bg_color = edit.GetBackgroundColour() # trick
            self.addToGrid(edit, 1)
  

        box.Add( grid, 1, wx.ALIGN_CENTRE|wx.EXPAND|wx.ALL, 5 )
        sizer.Add( box, 1, wx.ALIGN_CENTRE|wx.EXPAND|wx.ALL, 5 )

        bsizer = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add( bsizer, 0, wx.EXPAND, 5)

        parent.SetSizerAndFit(sizer)
        
    
    def createEditor(self, parent, p):
        validator = ParameterValidator(p)
        edit = wx.TextCtrl( parent, -1, "", name=p.getName(), size=(300,-1), validator=validator )
        edit.SetToolTipString( p.getDescription() )
        return edit
        

if __name__ == '__main__':

    from geoi.parameter import Parameter, IS_POSITIVE_NUMBER


    app = wx.App(0)
    f = wx.Frame(None, -1, "test")

    l = []
    not_empty = lambda s: s != ""
    l.append(Parameter("blahblah", "fefedfgdgdddddddddddddddddddddddddf",
                       'Species Name: the element name must begin with a capital letter'
                       , not_empty) )

    l.append(Parameter("FORMULA", "",
                       'Aqueous Species formula.\nExamples:\n   BF2(OH)2-'
                       , not_empty) )

    l.append(Parameter("Alkalinity", 12.46464645,
                       'Alkalinity contribution of the specie (0 if N/A)'
                       , IS_POSITIVE_NUMBER) )

    l.append(Parameter("equation", "dsfqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                       'Chemical Formation Reaction : specie is the first member of right member'
                       ) )

    d = MultiFieldDialog(f, "coucou", l, "au secours")
    d.addToGrid(wx.StaticText(d,-1, "coucou"), 0)
    
    box = wx.BoxSizer(wx.HORIZONTAL)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sampleList = ['zero', 'one', 'two']

    rb = wx.RadioBox(
            d, -1, "law type", wx.DefaultPosition, wx.DefaultSize,
            sampleList, 1, wx.RA_SPECIFY_COLS
            )
    box.Add(rb)
    
    vbox = wx.BoxSizer(wx.HORIZONTAL)
    vbox.Add( wx.TextCtrl(d,-1,"")  )
    box.Add( vbox )
    d.addToGrid( box, 1)
    
    d.Fit()
    
    b = wx.Button(f, -1, "click")
    b.Bind(wx.EVT_BUTTON, lambda e: d.Show())
    app.SetTopWindow(f)
    f.Show()
    app.MainLoop()
