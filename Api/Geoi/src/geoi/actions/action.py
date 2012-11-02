import wx
import wx.lib.customtreectrl as CT

TREE_NORMAL = 0
TREE_CHECKBOX = 1

class Action:
    "Main class for user interactivity"

    def __init__(self, win, name, description, menuText=None, accelerator=None
                 , iconId=None, callback=None, help=None):
        self.__parent = win
        self.__text = name
        self._callback = callback
        self._help = help

        if menuText is not None:
            self.__menuText = menuText
        else:
            self.__menuText = name

        self.__accelerator = accelerator
        self.__iconId = iconId
        self.__description = description
        #self.connect(self, SIGNAL('activated()'), self.run)
        self.__customAddedTo = []
        self.__correspondingWidgets = []
        self.__enabled = True
        self.__iconBitmap = None

    def getParent(self):
        return self.__parent

    def getText(self):
        return self.__text

    def getMenuText(self):
        return self.__menuText

    def getAccelerator(self):
        return self.__accelerator

    def getIconId(self):
        return self.__iconId

    def getDescription(self):
        return self.__description
        
#    def getCorrespondingWidgets(self):
#        return self.__correspondingWidgets

    def getHelp(self):
        return self._help

    def run(self):
        print "run :", self._callback
        if self._callback:
            self._callback()

#    def addTo(self, stuff):
#        if isinstance(stuff, wx.Menu):
#            self.addToMenu( stuff )

    def addToMenu(self, menu, id=None, kind=None):
        "add the action to the menu, and return the corresponding menuitem"
        if id is None:
            id = wx.NewId()
        if kind is None:
            kind = wx.ITEM_NORMAL
        menuText = self.getMenuText()
        if self.getAccelerator():
            menuText += "\t" + self.getAccelerator()
        item = wx.MenuItem(menu, id, menuText, self.getDescription(), kind=kind)
        if self.getIconBitmap():
            item.SetBitmap( self.getIconBitmap() )
        menu.AppendItem( item )
        self.getParent().Bind(wx.EVT_MENU, lambda e:self.run(), id=id)
        self.__correspondingWidgets.append((item, menu, id))
            
        self._applyDisabledState()   
        return item

    def addToCustomTreeCtrl(self, tree, parentItem, kind=None):
        if kind is None:
            kind = TREE_NORMAL
        #text = self.getText() + " : " + self.getDescription()
        text = self.getText()
        item = tree.AppendItem(parentItem, text, ct_type=kind)
        tree.SetItemPyData(item, self) # to handle events (see treeView_DoubleClicked() )
        if self.getIconBitmap():
            il = tree.GetImageList()
            idx = il.Add( self.getIconBitmap( size=il.GetSize(0) ))
            tree.SetItemImage(item, idx, which=wx.TreeItemIcon_Normal)
        self.__correspondingWidgets.append((item, tree))
        
        self._applyDisabledState()
        
        return item

    def getIconBitmap(self, client=wx.ART_OTHER, size=wx.DefaultSize):
        if not self.getIconId():
            return None
        return wx.ArtProvider.GetBitmap( self.getIconId(), client=client, size=size )

    def isEnabled(self):
        return self.__enabled

    def setDisabled(self, disabled):
        self.__enabled = not disabled
        self._applyDisabledState()
                
    def _applyDisabledState(self):
        disabled = not self.isEnabled()
        for tuple in self.__correspondingWidgets:
            item = tuple[0]
            if isinstance(item, wx.MenuItem):
                item,menu,id = tuple
                menu.Enable(id, self.isEnabled())
            if isinstance(item, CT.GenericTreeItem):
                item, tree = tuple
                tree.EnableItem(item, not disabled)
                #tree.SelectItem(item, not disabled)
        

    def _info(self, title, msg):
        dlg = wx.MessageDialog(self.getParent(), msg, title,
                               wx.OK | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def _error(self, title, msg):
        dlg = wx.MessageDialog(self.getParent(), msg, title, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        
def _helpSyntaxControl(help):
    """
    to get a better representation of the help string.
    """
    return help.replace(".",".\n")   
