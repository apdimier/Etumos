import traceback
import os
import os.path

import wx

from geoi.actions.action import Action
from geoi import parameters

GEOI_EXTENSION = '.geoi'

class SaveFile(Action):
    """
    SaveFile: Save a Geoi file
    """

    def __init__(self, win, param_mgr, name="Save"
                 , description='Save a Geoi file holding the configuration settings for a case/study'
                 ,iconId=wx.ART_FILE_SAVE
                 , SaveAs = False):
                 
        if SaveAs == False:
            Action.__init__(self, win, name, description, accelerator='CTRL+S',iconId=iconId)
        else:
            Action.__init__(self, win, name, description, accelerator='CTRL+SHIFT+S',iconId=iconId)
        self.param_mgr = param_mgr

    def _saveFile(self, filename):
        try:
            case = open (filename,'w')
        except:
            traceback.print_exc()
            msg = 'Could not write file ' + filename + "\n, got exception:" + \
                traceback.format_exc()
            self._error(filename, msg)
            return

        self.param_mgr.getCurrentParamSet().save( case )

        print "\n\n\n\n\n"
        print "#----------------------------------#"
        print "#     Your file has been saved     #"
        print "#----------------------------------#"
        print "\nin file : ", filename, "\n\n\n"

        return True

    def chooseFile(self):
        wildcard = "Geoi file (*"+GEOI_EXTENSION+")|*"+GEOI_EXTENSION+"|All files (*.*)|*.*"
        defaultFile = self.param_mgr.getCurrentParamValue(parameters.Title)
        dlg = wx.FileDialog(
            self.getParent(), message="Choose a geoi file to save as",
            defaultDir=os.getcwd(),
            defaultFile=defaultFile,
            wildcard=wildcard,
            style=wx.SAVE | wx.CHANGE_DIR |wx.FD_OVERWRITE_PROMPT
            )

        if dlg.ShowModal() == wx.ID_OK:
            file = str(dlg.GetPath())
            ext = os.path.splitext(file)[1]
            if ext == "" or ext != GEOI_EXTENSION:
                file += GEOI_EXTENSION
            print "file=", file
            
            return file
        return None

    def runWithFilename(self, filename):
        if not filename:
            filename = self.chooseFile()
            if not filename or filename == "":
                return
        try:
            if self._saveFile(filename):
                self.param_mgr.setFilename( filename )
        except:
            traceback.print_exc()
            msg = 'Could not save file ' + filename + "\n, got exception:" + \
                traceback.format_exc()
            self._error(filename, 'Error saving file', msg)
            return


    def run(self):
        self.runWithFilename(self.param_mgr.getFilename())
