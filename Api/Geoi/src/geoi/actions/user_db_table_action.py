
import wx
import wx.lib.dialogs

from geoi.actions.params_action import ParamsAction
from geoi.parameter import *
from geoi import parameters
from geoi.gui.sortable_autowidth_listctrl import SortableAutoWidthListCtrl
from geoi.gui.multi_field_dialog import MultiFieldDialog

USER_DB_COLOR = "GREEN"

class UserDBTableAction(ParamsAction):
    """
    This class is a base class for actions displaying a list of entries
    mixed from imported ones and user edited ones.
    Examples of derived actions are AqueousMasterSpecies and AqueousSecondarySpecies

    The derived class must implement getImportedDB(), getUserDB() and defineParameters()
    """

    def __init__(self, params_mgr, win, name, description, data_model, **kargs):
        """
        - import_db and user_db are the dictionaries holding the imported and user-edited
        entries
        - headers is a dict mapping the entry keys to the labels to be displayed
        - order is an ordered list of the entry keys, whose order will be use for the GUI
        """
        ParamsAction.__init__(self, params_mgr, win, name, description, **kargs)

        self._data_model = data_model
#        self._headers = headers
#        self._order = order
        self._colourdb = wx.ColourDatabase()
        self._editButton = None
        self._createFromSelection = None
        self._deleteButton = None
#        self._params = None
        self._table = None
        self._entry_dialog = None

    def getDataModel(self):
        return self._data_model

    def getNameForRow(self, row):
        return str(self._table.GetItem(row, self.getDataModel().getEntryIdColumn()).GetText())

    def _createInterface(self, parent, params):
        self._params = params
        self.getDataModel().load(params)
        self._table = table = self._createTable(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(table, 1, wx.ALL | wx.EXPAND , border=10)
        sizer.Add(self._createEditButtons(parent), 0, wx.ALIGN_CENTER_HORIZONTAL, border=5)

        parent.SetSizerAndFit(sizer)

    def _createEditButtons(self, parent):
        "create the buttons : createFromNew, createFromSelection..., and return a sizer"
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        createNew = wx.Button(parent, -1, "Create New")
        createNew.Bind(wx.EVT_BUTTON, self._onCreateNew)
        sizer.Add(createNew, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self._editButton = edit =  wx.Button(parent, -1, "Edit Custom")
        edit.Enable(False)
        edit.Bind(wx.EVT_BUTTON, self._onEdit)
        sizer.Add(edit, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self._deleteButton = delete =  wx.Button(parent, -1, "Delete Custom")
        delete.Enable(False)
        delete.Bind(wx.EVT_BUTTON, self._onDelete)
        sizer.Add(delete, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self._createFromSelection = cfs = wx.Button(parent, -1, "Create from selection")
        cfs.Enable(False)
        cfs.Bind(wx.EVT_BUTTON, self._onCreateFromSelection)
        sizer.Add(cfs, flag=wx.ALIGN_CENTER_HORIZONTAL, border=5)

        return sizer

    def _createTable(self, parent):
        "create and return the table displaying the entries"

        dm = self.getDataModel()
        values = dm.getAllStringValues()
        table = SortableAutoWidthListCtrl(parent, headers=dm.getHeaders(), values=values,
                                          style=wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL)
        table.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        table.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeSelected)

        # set colour for custom entries
        namecol = dm.getEntryIdColumn()
        for (index,entry) in enumerate(values):
            if dm.isCustomEntry(entry[namecol]):
                table.SetItemTextColour(index, USER_DB_COLOR)

        table.AutoSizeColumn(0)
        table.AutoSizeColumn(1)

        return table

    def _isCustomEntryByIndex(self, index):
        return self.getDataModel().isCustomEntry( self.getNameForRow(index) )

    def onItemSelected(self, evt):
        self._createFromSelection.Enable(True)
        index = evt.GetIndex()
        self._editButton.Enable(self._isCustomEntryByIndex(index))
        self._deleteButton.Enable(self._isCustomEntryByIndex(index))

    def onItemDeSelected(self, evt):
        self._createFromSelection.Enable(False)
        self._editButton.Enable(False)
        self._deleteButton.Enable(False)

    def createEntryEditDialog(self, params_list):
        """create the dialog to edit an entry. Can be overriden to
        customize the dialog"""
        if self._entry_dialog:
            self._entry_dialog.Destroy()

        self._entry_dialog = MultiFieldDialog(self.getParent(), self.getText(), params_list)
        return self._entry_dialog

    def getCurrentEntryEditDialog(self):
        "return the current entry dialog (see createEntryEditDialog() ) if any"
        return self._entry_dialog

    def _createEntry(self, params_list):
        d = self.createEntryEditDialog(params_list)

        if  wx.ID_OK != d.ShowModal() or not d.isValid() :
            return
        self._makeNewEntryFromParamList(params_list)

    def _makeNewEntryFromParamList(self, params_list):

        name = self.getDataModel().submitNewEntry(params_list)
        if name:
            index = self._table.insertRow(0, self.getDataModel().getStringsForEntry(name))
            self._table.SetItemTextColour(index, USER_DB_COLOR)
        else:
            wx.lib.dialogs.alertDialog(self.getParent(), "This element is not new", "Error")

    def _onCreateNew(self, evt):
        params_list = self.getDataModel().getParamsForNewEntry()
        self._createEntry(params_list)

    def _onCreateFromSelection(self, evt):
        index = self._table.GetFirstSelected()
        if index == -1:
            return

        name = self.getNameForRow(index)

        params_list = self.getDataModel().getParamsForNewEntryFrom(name)

        self._createEntry(params_list)

    def _onEdit(self, evt):
        index = self._table.GetFirstSelected()
        if index == -1:
            return

        name = self.getNameForRow(index)
        dm = self.getDataModel()
        params_list = dm.getParamsForEntryEdit(name)
        d = self.createEntryEditDialog(params_list)

        if  wx.ID_OK != d.ShowModal() or not d.isValid() :
            return

        new_name = dm.submitEditedEntry(name, params_list)
        if new_name:
            # refresh the row in the table
            self._table.changeRow(index, dm.getStringsForEntry(new_name))
        else:
            wx.lib.dialogs.alertDialog(self.getParent(), "This element is not new", "Error")

    def _onDelete(self, evt):
        index = self._table.GetFirstSelected()
        if index == -1:
            return
        name = self.getNameForRow(index)
        self.getDataModel().deleteEntry(name)
        self._table.DeleteItem(index)

    def _onOk(self, params):
        return True
