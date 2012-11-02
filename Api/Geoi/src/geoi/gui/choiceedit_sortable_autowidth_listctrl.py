from geoi import parameters
import wx

from geoi.gui.choice_edit_listmixin import ChoiceEditMixin
from geoi.gui.sortable_autowidth_listctrl import SortableAutoWidthListCtrl
from geoi.parameters import ParameterSet

class ChoiceEditSortableAutoWitdhListCtrl(SortableAutoWidthListCtrl, ChoiceEditMixin):
    def __init__(self, parent, headers=[], values=[], ID=wx.NewId() , pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        SortableAutoWidthListCtrl.__init__(self, parent, headers, values, ID, pos, size, style)
        ChoiceEditMixin.__init__(self)

    def SetChoices(self, index, col, choices):
        row = self.ConvertFromList(index)
        return ChoiceEditMixin.SetChoices(self, row, col, choices)

    def GetChoices(self, index, col):
        row = self.ConvertFromList(index)
        return ChoiceEditMixin.GetChoices(self, row, col)


if __name__ == '__main__':
    app = wx.App(0)
    f = wx.Frame(None, -1, "test")


#    headers = ["Name", "Value", "Default value", "Description", "Possible Values"]
#    values = []
#    params = ParameterSet()
#    for n in params.getParamNames():
#        p = params.getParam(n)
#        values.append([p.getName(),p.getValue(),p.getDefault(),p.getDescription(), p.getPossibleValues()])
#
#
##    import pprint
##    pp = pprint.PrettyPrinter(indent=4)
##    pp.pprint(values)
#
#    table = ChoiceEditSortableAutoWitdhListCtrl(f, headers=headers, values=values
#                                                , style=wx.LC_HRULES|wx.LC_VRULES)
#
#    for (i,n) in enumerate(params.getParamNames()):
#        p = params.getParam(n)
#        pv = p.getPossibleValues()
#        if pv and len(pv) > 1:
#            table.SetChoices(i, 1, pv)
#
#    table.SetColumnWidth(0, wx.LIST_AUTOSIZE)
#    table.SetColumnWidth(1, wx.LIST_AUTOSIZE)
#
#    sizer = wx.BoxSizer(wx.VERTICAL)
#    sizer.Add(table, 1, wx.EXPAND)
#    f.SetSizerAndFit(sizer)
#    f.SetSize((640,400))
#    f.CenterOnScreen()
#    f.Show()

    params = ParameterSet()
    unitsNames = parameters.UNITS
    unitsNames.sort()
    unitsParams = [params.getParam(i) for i in unitsNames]

    headers = ["Unit Name", "Unit Value", "Description"]

    values = []
    for p in unitsParams:
        values.append([p.getName(), p.getValue(), p.getDescription()])

    #values.append(["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","",""])

    table = ChoiceEditSortableAutoWitdhListCtrl(f, headers=headers, values=values,
                                                style=wx.LC_HRULES|wx.LC_VRULES)

    # add choices for edit via choices in table
    for (index,p) in enumerate(unitsParams):
        pv = p.getPossibleValues()
        if pv and len(p.getPossibleValues()) > 1:
            table.SetChoices(index, 1, p.getPossibleValues() )
#            else:
#                table.SetItemTextColour(index, NO_CHOICE_TEXT_COLOUR)


    table.AutoSizeColumn(0)
    table.AutoSizeColumn(1)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(table, 1, wx.EXPAND)
    f.SetSizerAndFit(sizer)
    f.SetSize((640,400))
    f.CenterOnScreen()
    f.Show()

    app.MainLoop()
