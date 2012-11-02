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
        Action.__init__(self, win, "Paraview", "Will launch Paraview", menuText = '&Paraview'
                        , iconId = wx.ART_EXECUTABLE_FILE)
    def run(self):
        os.system("/home/dimier/paraview-3.4.0-Linux-i686/bin/paraview&")


