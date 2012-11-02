import wx

from geoi.actions.action import Action, TREE_CHECKBOX

class ToggleAction(Action):
    """
    An action that toggles something, and so can be represented by a checkbox in a menu.

    You just need to override the onToggleOn() and onToggleOff() methods
    """

    def __init__(self, win, name, description, menuText=None, accelerator=None, iconId=None):
        Action.__init__(self, win, name, description, menuText, accelerator, iconId)
        self._isToggled = False

    def toggle(self):
        self.setToggleState(not self._isToggled)

    def onToggleOn(self):
        "to be overriden"
        pass

    def onToggleOff(self):
        "to be overriden"
        pass

    def isToggled(self):
        return self._isToggled

    def setToggleState(self, setToToggled):
        if self._isToggled == setToToggled: # nothing to do
            return
        self._isToggled = setToToggled
        if self._isToggled:
            self.onToggleOn()
        else:
            self.onToggleOff()

    def run(self):
        self.toggle()

    def addToMenu(self, menu, id=None, ):
        return Action.addToMenu(self, menu, id, kind=wx.ITEM_CHECK)

    def addToCustomTreeCtrl(self, tree, parentItem):
        return Action.addToCustomTreeCtrl(self, tree, parentItem, TREE_CHECKBOX)

