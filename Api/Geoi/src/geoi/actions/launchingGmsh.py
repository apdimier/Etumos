import wx
import os
import sys
import wx.richtext as rt
import  wx.html as  html
from geoi.actions.action import Action
from wx.html import *

class Run(Action):
    "Help: show Help"

    def __init__(self, win):
        Action.__init__(self, win, "Gmsh", "Will launch Gmsh", menuText = '&Gmsh'
                        , iconId = wx.ART_EXECUTABLE_FILE)
    def run(self):
        os.system("$GMSH/gmsh&")
