import wx

from geoi.gui.choiceedit_sortable_autowidth_listctrl import ChoiceEditSortableAutoWitdhListCtrl
from geoi.actions.params_action import ParamsAction
from geoi import parameters

NO_CHOICE_TEXT_COLOUR = 'RED'

class Units(ParamsAction):
    """
    input the Title Parameter of the study
    """

    def __init__(self, win, params_mgr):
        ParamsAction.__init__(self, params_mgr, win, "Units"
                              , "Edit the different units")

    def _createInterface(self, parent, params):
        unitsNames = parameters.UNITS
        unitsNames.sort()
        unitsParams = [params.getParam(i) for i in unitsNames]

        headers = ["Unit Name", "Unit Value", "Description"]

        values = []
        for p in unitsParams:
            values.append([p.getName(), p.getValue(), p.getDescription()])

        table = ChoiceEditSortableAutoWitdhListCtrl(parent, headers=headers, values=values,
                                                    style=wx.LC_HRULES|wx.LC_VRULES)
        self._table = table

        # add choices for edit via choices in table
        for (index,p) in enumerate(unitsParams):
            pv = p.getPossibleValues()
            if pv and len(pv) > 1:
                table.SetChoices(index, 1, pv )
            else:
                table.SetItemTextColour(index, NO_CHOICE_TEXT_COLOUR)

        table.AutoSizeColumn(0)
        table.AutoSizeColumn(1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(table, 1, wx.EXPAND)
        parent.SetSizerAndFit(sizer)

    def _onOk(self, params):
        # assign the values from the controls back to the params
        t = self._table
        for index in xrange(t.GetItemCount()):
            name = t.GetItem(index, 0).GetText()
            text = t.GetItem(index, 1).GetText()
            params.getParam(name).setValue(text)
        return True

