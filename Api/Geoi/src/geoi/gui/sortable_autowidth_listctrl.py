from wx.lib.mixins.listctrl import ColumnSorterMixin

import  wx
import  wx.lib.mixins.listctrl  as  listmix

class SortableAutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin
                                ,listmix.ColumnSorterMixin \
                                ):
    def __init__(self, parent, headers=[], values=[], ID=wx.NewId() , pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, autowidth=True):
        style |= wx.LC_REPORT

        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        if autowidth:
            listmix.ListCtrlAutoWidthMixin.__init__(self)

        self.key_max = 0
        self.initData(headers, values)

        listmix.ColumnSorterMixin.__init__(self, len(headers))

#        self.column_sorters = {}

#    def GetColumnSorter(self):
#        "overridden to allow setting custom sorters by column"
#        if str(self.)
#        return self.__ColumnSorter
#
#
#    def setColumnSorterForColumn(self, col, sorter):
#        self.column_sorters[str(col)] = sorter

    def ConvertFromList(self, index):
        """

        Convert a list index to a data row number

        if data has been sorted
        the original row and colums are do not correspond to the actual data
        So this function converts the current indices as displayed in the list
        to the original indices

        example:

        if "foo" was entered initially as in row 1, then after sorting it is
        now displayed in row 10
        then ConvertFromList(10) will return 1

        """
        return self.GetItemData(index)


    def initData(self, headers, values):
        for i in xrange(len(headers)):
            self.InsertColumn(i, headers[i])

        self.itemDataMap = {}     # see wx/lib/mixins/listctrl.py

        row = 0
        for tab in values:
            self.addRow(tab)
            row += 1

    def getKeyForRow(self, row):
        "return the initial key of this current row"
        return self.GetItemData(row)

    def getRowForKey(self, key):
        "return the current row for a given key"
        for row in xrange(self.GetItemCount()):
            if self.getKeyForRow(row) == key:
                return row
        return None

    def insertRow(self, row, tab):
        index = self.InsertStringItem(row, str(tab[0]))

        for col in xrange(1, len(tab)):
            self.SetStringItem(index, col, str(tab[col]))
        self.SetItemData(index, self.key_max) # for ColumnSorterMixin
        self.itemDataMap[self.key_max] = tab
        self.key_max += 1
        return index

    def addRow(self, tab):
        self.insertRow(self.GetItemCount(), tab)

    def changeRow(self, row, tab):
        key = self.GetItemData(row)
        for col in xrange(len(tab)):
            self.SetStringItem(row, col, str(tab[col]))
        self.itemDataMap[key] = tab

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self

    def AutoSizeColumn(self, col, extraSize=20):
        """
        set the width of the column to be adjusted automatically depending
        on its contents, plus an extra width in case of... (actually there is a bug so
        the extra width is a work-around)
        """
        self.SetColumnWidth(col, wx.LIST_AUTOSIZE)
        if extraSize > 0:
            self.SetColumnWidth(col, self.GetColumnWidth(col) + extraSize)


if __name__ == '__main__':
    from geoi.parameters import ParameterSet

    app = wx.App(0)
    f = wx.Frame(None, -1, "test")


    headers = ["Name", "Value", "Default value", "Description", "Possible Values"]
    values = []
    params = ParameterSet()
    for n in params.getParamNames():
        p = params.getParam(n)
        values.append([p.getName(),p.getValue(),p.getDefault(),p.getDescription(), p.getPossibleValues()])

#    import pprint
#    pp = pprint.PrettyPrinter(indent=4)
#    pp.pprint(values)

    table = SortableAutoWidthListCtrl(f, headers=headers, values=values, style=wx.LC_HRULES|wx.LC_VRULES)
    table.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(table, 1, wx.EXPAND)
    f.SetSizerAndFit(sizer)
    f.SetSize((640,400))
    f.CenterOnScreen()
    f.Show()
    app.MainLoop()
