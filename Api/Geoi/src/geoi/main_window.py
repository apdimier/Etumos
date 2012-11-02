import wx
import wx.lib.customtreectrl as CT
import wx.aui

from geoi.actions.open_shell import OpenShell
from geoi.actions.inspector import Inspector
from geoi.actions.action import Action, TREE_CHECKBOX

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.idsToAction = {}

        self.CreateStatusBar()

                # tell FrameManager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self.dialogPanel = wx.Panel(self)
        self.dialogPanel.SetName("Perpectives")
        Satz = "GUI dialog panel"
        tc = wx.StaticText(self.dialogPanel, -1, Satz)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.dialogPanel.SetSizer( sizer )

    def getAuiManager(self):
        return self._mgr

    def getDialogPanel(self):
        return self.dialogPanel

    def clearDialogPanel(self):
        self.getDialogPanel().DestroyChildren()

    def setup(self, actionsTree):
        self.createMenusForWindow(actionsTree)
        self.setupCentralWidget(actionsTree)

    def setupCentralWidget (self, actionsTree):
        textArea = wx.TextCtrl(self)

        self.tree = tv = self.createTreeView(self, actionsTree)

        self._mgr.AddPane(tv, wx.aui.AuiPaneInfo().
                          Name("dialog tree").
                          Caption("dialog tree").
                          Floatable(True).
                          Left().CloseButton(False).
                          MaximizeButton(True).
                          MinimizeButton(True).
                          Movable(True).
                          Dockable(True).
                          MinSize( (170,500)) )

        self._dialogPane = self._mgr.AddPane(self.getDialogPanel(), wx.aui.AuiPaneInfo().
                          Name("Dialog").
                          Caption("Dialog").
                          Center().
                          CloseButton(False).
                          MaximizeButton(True).
                          Floatable(True).
                          Dockable(True).
                          BestSize( (600,570)) )

        self._mgr.AddPane(textArea, wx.aui.AuiPaneInfo().
                          Name("Output").
                          Caption("Output").
                          BestSize( (600,50) ).
                          Bottom().
                          CloseButton(True).
                          MaximizeButton(True))



        self._mgr.Update()



    def createTreeView(self, parent, tree):
        tv = CT.CustomTreeCtrl(parent, style =
                         wx.SUNKEN_BORDER | CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT
                         | wx.TR_FULL_ROW_HIGHLIGHT
                         | wx.TR_HIDE_ROOT
                         )
        tv.EnableSelectionVista(True)

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        tv.SetImageList(il)

        self.root = tv.AddRoot("Root")

        tv.SetItemImage(self.root, self.fldridx, which = wx.TreeItemIcon_Normal)
        tv.SetItemImage(self.root, self.fldropenidx, which = wx.TreeItemIcon_Expanded)

        for elt in tree[1:]:
            self._rec_createTreeView(tv, elt, self.root)

        tv.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.treeView_DoubleClicked)
        tv.Bind(CT.EVT_TREE_ITEM_CHECKED, self.treeView_Checked)

        tv.SetImageList(il) # redo it (cf a few lines above) as a workaround for a bug on linux
#
# 12/09/08: if you want to have all element tree directly accessible, uncomment the next line: tv.ExpandAll
#
#        tv.ExpandAll()
        return tv

    def _rec_createTreeView(self, tv, tree, previous):
        if len(tree) < 2:
            return previous

        child = tv.AppendItem(previous, tree[0])

        tv.SetItemImage(child, self.fldridx, which = wx.TreeItemIcon_Normal)
        tv.SetItemImage(child, self.fldropenidx, which = wx.TreeItemIcon_Expanded)

        child.action = None # added attribute used by the treeView_DoubleClicked() callback

        for action in tree[1:]:
            if isinstance(action, list):
                self._rec_createTreeView(tv, action, child)
            else:
                action.addToCustomTreeCtrl(tv, child)

        return child

    def treeView_DoubleClicked(self, evt):
        item = evt.GetItem()
        if self.tree.GetItemType(item) == TREE_CHECKBOX:
            self.tree.CheckItem(item, not item.IsChecked())
        else:
            self.doRunAction(item)

    def doRunAction(self, itemId):    
        if itemId:
            action = self.tree.GetItemPyData(itemId)
            if action:
                action.run()
        

    def treeView_Checked(self, evt):
        self.doRunAction(evt.GetItem())

#    def createHelpMenu(self):
#        menu = wx.Menu()
#
#        actions = ['Help', help.Help(mw), show_params.ShowParams(mw, params_mgr), About(mw)]
#
#        OpenShell(self).addToMenu(menu)
#        Inspector(self).addToMenu(menu)
#
#        id = wx.NewId()
#        menu.Append(id, "integrate dialog")
#        self.Bind(wx.EVT_MENU, self.integrateDialog, id=id)
#
#        self.GetMenuBar().Append(menu, "Debug")

    def createPerspectivesMenu(self):
        menu = wx.Menu()

        FloatDialogPaneAction(self).addToMenu(menu)
        DockDialogPaneAction(self).addToMenu(menu)

        self.GetMenuBar().Append(menu, "Perspectives")

    def integrateDialog(self, evt):
    #    d = wx.MessageDialog(self, "coucou")

        c = wx.StaticText(self,-1,"coucou")
        self._mgr.AddPane(c, wx.LEFT )

        self._mgr.Update()

    def createMenusForWindow(self, tree):
        self.SetMenuBar( wx.MenuBar() )

        id = 1
        for elt in tree[1:]:
            id = self._rec_createMenus(self.GetMenuBar(), elt, id)

        #self.createHelpMenu()
        self.createPerspectivesMenu()


    def _rec_createMenus(self, parent, tree, id):
        name = tree[0]
        menu = wx.Menu()
        if parent is self.GetMenuBar(): #toplevel
            parent.Append(menu, '&' + name)
        else:

            parent.AppendSubMenu(menu, name)
            id += 1
#        parent.insertItem ('&' + name, menu)
        for action in tree[1:]:
            if isinstance(action, list):
                id = self._rec_createMenus(menu, action, id)
            else:
                action.addToMenu(menu, id)
            id += 1

        return id

    def menuClicked(self,id):
        action = self.idsToAction[str(id)]
        action.run()

class FloatDialogPaneAction(Action):
    "FloatDialogPane: make the (center) dialog pane floating"

    def __init__(self, win):
        Action.__init__(self, win, "Float the Dialog Pane"
                        , 'make the center dialog pane to be floating around')


    def run(self):
        w = self.getParent(); mgr = w.getAuiManager()
        paneinfo = mgr.GetPane(w.getDialogPanel())
        paneinfo.Float()
        paneinfo.CloseButton(False)
        mgr.Update()

class DockDialogPaneAction(Action):
    "DockDialogPaneAction: make the (center) dialog pane docked"

    def __init__(self, win):
        Action.__init__(self, win, "Dock the Dialog Pane"
                        , 'make the center dialog pane to be docked')


    def run(self):
        w = self.getParent(); mgr = w.getAuiManager()
        paneinfo = mgr.GetPane(w.getDialogPanel())
        paneinfo.Dock()
        mgr.Update()


if __name__ == '__main__':
    app = wx.App(0)
    #app = init_qt_and_set_styles(sys.argv)
    mw = MainWindow(None, -1, "coucou")
    tree = ['Root', ['Toto', ['titi'] , ['Tutu']]
            ]
    mw.createMenusForWindow(tree)
    mw.CenterOnScreen()
    mw.Show()
    app.MainLoop()

