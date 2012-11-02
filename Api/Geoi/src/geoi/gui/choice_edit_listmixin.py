from bisect import bisect
import sys

import  wx
import  wx.lib.mixins.listctrl  as  listmix

from geoi.gui.sortable_autowidth_listctrl import SortableAutoWidthListCtrl

"""
define classes :
ChoiceEditMixin
ChoiceEditableListCtrl
SortableChoiceEditableListCtrl
"""

class MyChoice(wx.Choice):
    def SetValue(self, list, row, col):
        choices = list.GetChoices(row, col)
        if not choices:
            return False
        #clear the choice item
        while self.GetCount():
            self.Delete(0)
        # add the data
        self.AppendItems(choices)

        index = self.FindString(list.GetItem(row, col).GetText() )
        if index == wx.NOT_FOUND:
            index = 0
     
        self.SetSelection( index )

        return True

    def SetSelection(self, froms, to=None):
#        print "SetSelection, froms=", froms, " to=", to
        if to is None:
            wx.Choice.SetSelection(self, froms)
#        else:
#            print "SetSelection"

    def GetValue(self):
        return self.GetString(self.GetSelection())


class ChoiceEditMixin(listmix.TextEditMixin):
    """
    A Hack by Karl Forner to replace the TextCtrl Editor of the wx.lib.mixins.listctrl.TextEditMixin
    by a wx.Choice control

    To use it, eiher mix your ListCtrl class with this mixin, or derive from the supplied
    ChoiceEditableListCtrl class

    Then use the SetChoices() method to set the different possible value for the cells
    which should be editable with the Choice control

    """

    def __init__(self):
        listmix.TextEditMixin.__init__(self)
        self.curRow = -1 # workaround for a bug in TextEditMixin
        self.choices = {}

    def SetChoices(self, index, col, choices):
        if not self.choices.get(index):
            self.choices[index] = {}
        self.choices[index][col] = choices


    def GetChoices(self, index, col):
        if not self.choices.has_key(index) or not self.choices.get(index).has_key(col):
            return None
        return self.choices[index][col]

    def make_editor(self, col_style=wx.LIST_FORMAT_LEFT):

        editor = MyChoice(self.GetMainWindow(), -1)
        editor.SetBackgroundColour(self.editorBgColour)
        editor.SetForegroundColour(self.editorFgColour)
        font = self.GetFont()
        editor.SetFont(font)

        self.curRow = 0
        self.curCol = 0

        editor.Hide()
#        if hasattr(self, 'editor'):
#            self.editor.Destroy()
        self.editor = editor

#        self.col_style = col_style
        self.editor.Bind(wx.EVT_CHAR, self.OnChar)
        self.editor.Bind(wx.EVT_KILL_FOCUS, self._onKillFocus)
        self.Bind(wx.EVT_CHOICE, self.choiceChanged)

    def _onKillFocus(self, evt):
        self.CloseEditor(evt)
    
    def OnLeftDown(self, evt=None):
        ''' Examine the click and double
        click events to see if a row has been click on twice. If so,
        determine the current row and columnn and open the editor.'''
        
        if self.editor.IsShown():
            self.CloseEditor()
            
        x,y = evt.GetPosition()

        row,flags = self.HitTest((x,y))
    
        if row != self.curRow: # self.curRow keeps track of the current row
            evt.Skip()
            return
        
        col = self.findColumn(x)     
        self.OpenEditor(col, row)

    def getXscrollPosition(self):
        xscroll = self.GetScrollPos(wx.HORIZONTAL)
        # take into account the scroll position if needed (e.g . for gtk)
        mw = self.GetMainWindow()
        if isinstance(mw, wx.ScrolledWindow): 
            xscroll *= mw.GetScrollPixelsPerUnit()[0]
        return xscroll

    def findColumn(self, x):
        xcols = [0]
        loc = 0
        for n in xrange(self.GetColumnCount()):
            loc = loc + self.GetColumnWidth(n)
            xcols.append(loc)
        
        xscroll = self.getXscrollPosition()
        col = bisect(xcols, x + xscroll) - 1
        return col
        
    def getColumnX(self, col):
        x = 0
        for n in xrange(col):
            x += self.GetColumnWidth(n)
        return x

    def OpenEditor(self, col, row):
        ''' Opens an editor at the current position. '''
#        print "OpenEditor, row=", row, " col=", col

        # give the derived class a chance to Allow/Veto this edit.
        evt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_BEGIN_LABEL_EDIT, self.GetId())
        evt.m_itemIndex = row
        evt.m_col = col
        item = self.GetItem(row, col)
        evt.m_item.SetId(item.GetId())
        evt.m_item.SetColumn(item.GetColumn())
        evt.m_item.SetData(item.GetData())
        evt.m_item.SetText(item.GetText())
        ret = self.GetEventHandler().ProcessEvent(evt)
        if ret and not evt.IsAllowed():
            return   # user code doesn't allow the edit.

        # set the contents of the editor if any
        if not self.editor.SetValue(self, row, col): #karl
            return


#        if self.GetColumn(col).m_format != self.col_style:
#            self.make_editor(self.GetColumn(col).m_format)

#        x0 = self.col_locs[col]
#        x1 = self.col_locs[col+1] - x0
#
        scrolloffset = self.getXscrollPosition()

        # desactivated by karl : scroll pos are screwed up
#        # scroll forward
#        if x0+x1-scrolloffset > self.GetSize()[0]:
#            if wx.Platform == "__WXMSW__":
#                # don't start scrolling unless we really need to
#                offset = x0+x1-self.GetSize()[0]-scrolloffset
#                # scroll a bit more than what is minimum required
#                # so we don't have to scroll everytime the user presses TAB
#                # which is very tireing to the eye
#                addoffset = self.GetSize()[0]/4
#                # but be careful at the end of the list
#                if addoffset + scrolloffset < self.GetSize()[0]:
#                    offset += addoffset
#
#                self.ScrollList(offset, 0)
#                scrolloffset = self.GetScrollPos(wx.HORIZONTAL)
#            else:
#                # Since we can not programmatically scroll the ListCtrl
#                # close the editor so the user can scroll and open the editor
#                # again
##                if not self.editor.SetValue(self, row, col): #karl
##                    return
#                #self.editor.SetValue(self.GetItem(row, col).GetText())
#                self.curRow = row
#                self.curCol = col
#                self.CloseEditor()
#                return

        r = self.GetItemRect(row)
        y0 = r[1]
  
        x1 = self.GetColumnWidth(col)
        editor = self.editor

        y = y0
        #x = x0-scrolloffset
        x = self.getColumnX(col) - scrolloffset
#        print "initial coords=", x, " ", y
        mw = self.GetMainWindow() # the inner scrolled window
        # convert to main window coordinates on platforms where mainwindow is handled by wx
        # to take into account the column headers
        if mw is not self:
            pos = mw.GetPosition()
            x -= pos[0]
            y -= pos[1]
#            print "translated coords=", x, " ", y

        editor.SetPosition( (x, y) )
        editor.SetSize( (x1,-1) )

        editor.Raise()
        editor.SetFocus()
        editor.Show()

        self.curRow = row
        self.curCol = col

    def choiceChanged(self, evt):
        text = evt.GetString()
        item = self.GetItem(self.curRow, self.curCol)
        oldText = item.GetText()
#        print "choiceChanged, text=", text, "oldText=", oldText
        self.SetStringItem(self.curRow, self.curCol, text)

        # FIXME: this function is usually called twice - second time because
    # it is binded to wx.EVT_KILL_FOCUS. Can it be avoided? (MW)
    def CloseEditor(self, evt=None):
        ''' Close the editor and save the new value to the ListCtrl. '''
#        print "CloseEditor:", evt

        if not self.editor.IsShown():
            return

        text = self.editor.GetValue()
        #text = evt

        self.editor.Hide()
        self.SetFocus()



        # post wxEVT_COMMAND_LIST_END_LABEL_EDIT
        # Event can be vetoed. It doesn't has SetEditCanceled(), what would
        # require passing extra argument to CloseEditor()
        evt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT, self.GetId())
        evt.m_itemIndex = self.curRow
        evt.m_col = self.curCol
        item = self.GetItem(self.curRow, self.curCol)
  
        evt.m_item.SetId(item.GetId())
        evt.m_item.SetColumn(item.GetColumn())
        evt.m_item.SetData(item.GetData())
        evt.m_item.SetText(text) #should be empty string if editor was canceled
        ret = self.GetEventHandler().ProcessEvent(evt)
        if not ret or evt.IsAllowed():
            if self.IsVirtual():
                # replace by whather you use to populate the virtual ListCtrl
                # data source
                self.SetVirtualData(self.curRow, self.curCol, text)
            else:
                self.SetStringItem(self.curRow, self.curCol, text)
        self.RefreshItem(self.curRow)

class ChoiceEditableListCtrl(wx.ListCtrl,
                #   listmix.ListCtrlAutoWidthMixin,
                   ChoiceEditMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
   #     listmix.ListCtrlAutoWidthMixin.__init__(self)
        ChoiceEditMixin.__init__(self)


if __name__ == '__main__':



    listctrldata = {
    1 : ("Hey!", "You can edit", "me!"),
    2 : ("Try changing the contents", "by", "clicking"),
    3 : ("in", "a", "cell"),
    4 : ("See how the length columns", "change", "?"),
    5 : ("You can use", "TAB,", "cursor down,"),
    6 : ("and cursor up", "to", "navigate"),
    }

    class TestListCtrlPanel(wx.Panel):
        def __init__(self, parent, log):
            wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

            self.log = log
            tID = wx.NewId()

            sizer = wx.BoxSizer(wx.VERTICAL)

            if wx.Platform == "__WXMAC__" and \
                   hasattr(wx.GetApp().GetTopWindow(), "LoadDemo"):
                self.useNative = wx.CheckBox(self, -1, "Use native listctrl")
                self.useNative.SetValue(
                    not wx.SystemOptions.GetOptionInt("mac.listctrl.always_use_generic") )
                self.Bind(wx.EVT_CHECKBOX, self.OnUseNative, self.useNative)
                sizer.Add(self.useNative, 0, wx.ALL | wx.ALIGN_RIGHT, 4)


            self.list = ChoiceEditableListCtrl(self, tID,
                                     style=wx.LC_REPORT
                                     | wx.BORDER_NONE
                                     | wx.LC_SORT_ASCENDING
                                     )

            self.Populate(self.list)

            sizer.Add( wx.StaticText(self, -1, "coucou coucou") )
            sizer.Add(self.list, 1, wx.EXPAND)
            self.SetSizer(sizer)
            self.SetAutoLayout(True)

        def Populate(self, list):


            # for normal, simple columns, you can add them like this:
            list.InsertColumn(0, "Column 1")
            list.InsertColumn(1, "Column 2")
            list.InsertColumn(2, "Column 3")
            list.InsertColumn(3, "Len 1", wx.LIST_FORMAT_RIGHT)
            list.InsertColumn(4, "Len 2", wx.LIST_FORMAT_RIGHT)
            list.InsertColumn(5, "Len 3", wx.LIST_FORMAT_RIGHT)

            items = listctrldata.items()
            for key, data in items:
                index = self.list.InsertStringItem(sys.maxint, data[0])
                self.SetStringItem(index, 0, data[0])
                self.SetStringItem(index, 1, data[1])
                self.SetStringItem(index, 2, data[2])
                self.list.SetItemData(index, key)

            list.SetChoices(0,0, ['toto','titi','tutu'])
            list.SetChoices(1,1,['ta mere en short','toto','titi','tutu'])
            list.SetChoices(5,5,['grouik','toto','titi','tutu'])
            self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.list.SetColumnWidth(2, 100)

            self.currentItem = 0

        def SetStringItem(self, index, col, data):
            if col in range(3):
                wx.ListCtrl.SetStringItem(self.list, index, col, data)
                wx.ListCtrl.SetStringItem(self.list, index, 3+col, str(len(data)))
            else:
                try:
                    datalen = int(data)
                except:
                    return

                wx.ListCtrl.SetStringItem(self.list, index, col, data)

                data = self.list.GetItem(index, col-3).GetText()
                wx.ListCtrl.SetStringItem(self.list, index, col-3, data[0:datalen])

    app = wx.App(0)
    frame = wx.Frame(None, -1, "coucou")
    list = TestListCtrlPanel(frame, 0)
    frame.Show()
    app.MainLoop()

