from geoi.actions.action import Action
import os
import os.path
import traceback

import wx

from geoi.chemistry_db import ChemistryDB
from geoi.material_db  import MaterialDB
import parameters

class ParamsManager:
    """
    Manage different sets of Parameters : access to the current sets
    and store previous sets to be able to redo/_undo_action
    """

    def __init__(self):
        self.paramSets = [parameters.ParameterSet()]
        self._current_set = 0
        self.filename = None
        self.chemistry_db_path = None

        self._undo_action = None
        self._redo_action = None

    def createRedoAndUndoActions(self, win):
        self._undo_action = Action(win, "Undo", "Undo the last edit"
                        , accelerator = 'CTRL+Z', iconId = wx.ART_UNDO, callback=self.undo)
        self._undo_action.setDisabled(True)
        self._redo_action = Action(win, "Redo", "Redo the last undone edit"
                        , accelerator = 'CTRL+Y', iconId = wx.ART_REDO, callback=self.redo)
        self._redo_action.setDisabled(True)

    def getUndoAction(self):
        return self._undo_action

    def getRedoAction(self):
        return self._redo_action

    def undo(self):
#        print "_undo_action"
        self._undo_action.getParent().clearDialogPanel()
        self._current_set -= 1
        assert(self._current_set >= 0)
        self._updateUndoRedo()

    def redo(self):
#        print "redo"
        self._redo_action.getParent().clearDialogPanel()
        self._current_set += 1
        assert(self._current_set <= len(self.paramSets)-1)
        self._updateUndoRedo()

    def importCurrentChemistryDB(self, params):
        title = "import CurrentChemistry DB"
        filepath = params.getParam(parameters.CurrentDatabasePath).getValue()
        #
        # we call that function to enable import between users
        #
        if filepath != None:
            filepath = _userDatabaseExchangeEnabling(filepath)
        
        if not filepath:
            filename = self.getCurrentParamValue(parameters.DefaultDatabase)
            path = self.getChemistryDatabasePath()
            if not path:
                self._error(title
                            , "unable to find the path for the default database " + filename)
                return
            filepath = os.path.join(path, filename)
        if not os.path.exists(filepath):
            self._error(title, "file " + filepath + " does not exist, aborting...")
            return
        if filepath == None:
            filepath = os.environ.get("WRAPPER_DAT")+"/"+"phreeqc.dat"
        fh = None
        try:
            fh = open(filepath, "r")
        except:
            self._error(title, "could not open file " + filepath)
            return

        db = ChemistryDB()
        try:
            db.readFromPhreeqcFormat(fh)
        except Exception, err:
            traceback.print_exc()
            self._error(title, "Error importing database " + filepath + " : \n" + str(err))
            return

        params.getParam(parameters.CurrentDatabasePath).setValue(filepath)
        params.getParam(parameters.IMPORTED_CHEMISTRY_DB).setValue(db)
        self._info(title, "database " + filepath + " successfully imported !")
        return True

    def _info(self, title, msg):
        win = wx.GetActiveWindow()
        dlg = wx.MessageDialog(win, msg, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def _error(self, title, msg):
        win = wx.GetActiveWindow()
        dlg = wx.MessageDialog(win, msg, title, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    def getChemistryDatabasePath(self):
        """
        Return the path where the standard databases are to be found.
        This path can either be obtained via the WRAPPER_DAT environment variable
        or be loaded from anywhere else
        """
        if not self.chemistry_db_path:
            self.chemistry_db_path = self._setupChemistryDatabasePath()
        return self.chemistry_db_path

    def getChemistryDB(self):
        return self.getCurrentParamValue(parameters.IMPORTED_CHEMISTRY_DB)

    def _setupChemistryDatabasePath(self):
        # try using the environment variable
        path = os.path.expandvars(parameters.WRAPPER_DAT)
        if not path or not os.path.exists(path):
            # obtain it via user
            msg = """
The path for phreeqc chemistry databases can not be found. You may either define the
%s environment variable before running this software (hit 'Cancel' then Exit),
or select it manually right now by pressing 'Ok'.
            """ % parameters.WRAPPER_DAT
            dlg = wx.MessageDialog(None, msg,'Unknown Chemistry Database Path',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               )

            if dlg.ShowModal() == wx.ID_OK:
                path = self.askForChemistryDatabasePath()
            else:
                return

            dlg.Destroy()

        return path

    def askForChemistryDatabasePath(self):
        win = wx.GetActiveWindow()

        # try to guess a smart default dir
        cwd = os.getcwd()
        f = __file__
        d = os.path.dirname(__file__)
        p = cwd
        if d == cwd: # means that current directory is certainly not choosen by the user
            # use the geoi project data directory
            p = os.path.split(d)[0]
            p = os.path.split(p)[0]
            p = os.path.join(p, "data")

        dlg = wx.DirDialog(win, "Choose the Phreeqc Database directory:", defaultPath=p,
                          style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.DD_CHANGE_DIR)

        path = None
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        return path

    def getFilename(self):
        return self.filename

    def setFilename(self, name):
        self.filename = name

    def getCurrentParamSet(self):
        return self.paramSets[self._current_set]

    def getCurrentParamValue(self, name):
        'shortcut'
        return self.getCurrentParamSet().getParam(name).getValue()

    def isItNew(self, paramSet):
        """
        check if this paramSet is different from the current one
        Returns True if different, False otherwise
        """
        return paramSet != self.getCurrentParamSet()

    def submitNew(self, paramSet):
        """
        submit a new paramSet that may become the new current set

        Return True if accepted, False
        """
        if not self.isItNew(paramSet):
            return False

        self._current_set += 1
        self.paramSets = self.paramSets[:self._current_set]
        self.paramSets.append(paramSet)

        self._updateUndoRedo()

        return True


    def _loadFile(self, filename):
        try:
            case = open (filename,'r')
        except:
            traceback.print_exc()
            msg = 'Could not open file ' + filename + "\n, got exception:" + \
                traceback.format_exc()
            self._error(filename, 'Error opening file', msg)
            return

        p = parameters.ParameterSet()
        p.read(case)

        if not self.submitNew(p):
            pass
#            self._info("Load aborted", "file did not contain new values of parameters")

        db = p.getParamValue(parameters.CurrentDatabasePath)
        if db != "":
            self.importCurrentChemistryDB(p)

        self.setFilename( filename )


    def openFile(self, file):
        try:
            self._loadFile(file)
        except:
            traceback.print_exc()
            msg = 'Error reading file ' + file + "\n, got exception:" + \
            traceback.format_exc()
            self._error('Error reading file', msg)
            return

    def _updateUndoRedo(self):
        self._undo_action.setDisabled(self._current_set == 0)
        self._redo_action.setDisabled( self._current_set ==  len(self.paramSets) - 1)
        
def _userDatabaseExchangeEnabling(filepath):
    """
    that function enables to exchange geoi files between users
    """
    filepath1 = filepath.split('/')
    if 'home' in filepath1:
#        print "filepath1",filepath1
#        print "filepath",filepath1
        newFile = os.getenv("HOME")
        ind = filepath1.index('home')+2
        for i in filepath1[ind:]:
            newFile+="/"+i
#            print "over i ",newFile
#            print "newFile  ",newFile
    else:
        newFile = filepath
    return newFile

