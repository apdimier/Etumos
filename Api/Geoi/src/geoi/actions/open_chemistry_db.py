import os.path

import wx
import  wx.lib.filebrowsebutton as filebrowse

from geoi.actions.params_action import ParamsAction
from geoi import parameters

class OpenChemistryDB(ParamsAction):
    """
    Choose a ChemistryDB and load it
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Open Chemistry DB", 
                    """ 
Choose and import a chemistry database
                    """)
    def _fetchAvailableDatabases(self, path):
        ext = parameters.CHEMISTRY_DB_EXTENSION
        if not path or not os.path.exists(path):
            return []
        l = filter(lambda d : d.endswith(ext), os.listdir(path))
        return l

    def _createInterface(self, parent, params):
        pcd = params.getParam(parameters.CurrentDatabasePath)
   
        sizer = wx.BoxSizer( wx.VERTICAL )
        box = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "" ) , wx.VERTICAL )
        
        #### current database info ###
        hbox = wx.BoxSizer( wx.HORIZONTAL )
        label = wx.StaticText(parent, -1,  pcd.getDescription() )
        textctrl = wx.TextCtrl(parent, -1, pcd.getValue())
        textctrl.SetEditable(False)
        hbox.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL)
        hbox.AddSpacer(5)
        hbox.Add(textctrl, 1, wx.ALIGN_CENTRE_VERTICAL|wx.EXPAND)
        box.Add( hbox, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.EXPAND, 5 )
        
        #### available dbs ###
        default_db = params.getParam(parameters.DefaultDatabase).getValue()
        hbox = wx.BoxSizer( wx.HORIZONTAL )
        path = self.getParamsMgr().getChemistryDatabasePath()
        dbs = self._fetchAvailableDatabases(path)
        hbox.Add(wx.StaticText(parent, -1,  "Available Database" ), 0, wx.ALIGN_CENTRE_VERTICAL)
        choice = wx.Choice(parent, -1, choices=dbs)
        choice.Bind(wx.EVT_CHOICE
                    , lambda e : self.setFileToImport(os.path.join(path, choice.GetStringSelection()), 1) )
        index = -1
        try:
            index = dbs.index(default_db)
        except:
            pass
        if index >= 0:
            choice.SetSelection( index )
        hbox.AddSpacer(5)
        hbox.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL)
        box.Add( hbox, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
    
        ####  database to import ###
        import_box = wx.StaticBoxSizer(wx.StaticBox( parent, -1, "Database to import" ) , wx.VERTICAL )
        self.fbbh = filebrowse.FileBrowseButtonWithHistory(parent, -1
                                                           , labelText="file to import"
                                                           , changeCallback = self.fbbhCallback
                                                           , fileMask = "*" + parameters.CHEMISTRY_DB_EXTENSION)
        import_box.Add(self.fbbh, 1, wx.EXPAND)
        box.Add( import_box, 1, wx.EXPAND, 5 )
        
        sizer.Add( box, 0, wx.ALIGN_CENTRE|wx.ALL| wx.EXPAND, 5 )

        parent.SetSizerAndFit(sizer)

    def _onOk(self, params):
        filepath = self.fbbh.GetValue()
        if os.path.exists(filepath):
            params.getParam(parameters.CurrentDatabasePath).setValue(file)
        return self.getParamsMgr().importCurrentChemistryDB(params)
        
    def setFileToImport(self, file, callback):
        history = self.fbbh.GetHistory()
        self.fbbh.SetValue(file, callback)
        if file not in history:
            history.append(file)
            self.fbbh.SetHistory(history)
            self.fbbh.GetHistoryControl().SetStringSelection(file)
    
    def fbbhCallback(self, evt):
        print "fbbhCallback"
        value = evt.GetString()
        self.setFileToImport(value, 0)

