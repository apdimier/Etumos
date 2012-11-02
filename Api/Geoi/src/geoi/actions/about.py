import wx
from wx.lib.wordwrap import wordwrap

from geoi.actions import action

LICENSE = \
"""
License type : GPL (see http://www.gnu.org/copyleft/gpl.html)

This is open source software lisenced under GPL. Therefore you may freely use it for academic, educational and even commercial purposes. However, the GPL license includes a viral effect i.e. all derived work, if distributed, must be distributed under the same license. However, it is possible that you would also be licensed under other terms if agreed upon."""
class About(action.Action):
    "About: display an about dialog"

    def __init__(self, win):
        action.Action.__init__(self, win, "About"
                        , 'display an about dialog')

    def run(self):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "geoi"
        info.Version = "1.0.0"
        info.Copyright = "(C) 2008 http://www.Etumos.org"
        info.Description = wordwrap(
            "Graphical User Interface enabling to create a python file\n"
            "for the simulation of a geochemical or a                 \n"
            "geochemical-transport problem with:                      \n"
            " - PHREEQC as geochemical tool,                          \n"
            " - and MT450 or Elmer as transport tools                 \n"
            "                                        \n"
            "The problem is saturated, unsaturated problems will      \n"
            "be treated in the next version of the software.          \n"
            "developments granted from the unemployement fund         \n",
            550, wx.ClientDC(self.getParent()))
        info.WebSite = ("http://www.gnu.org", "GNU home page")
        #("http://www.etumos.org", "ETUMOS home page"))
        info.Developers = [ "Alain Dimier:" ]

        info.License = wordwrap(LICENSE, 500, wx.ClientDC(self.getParent()))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
