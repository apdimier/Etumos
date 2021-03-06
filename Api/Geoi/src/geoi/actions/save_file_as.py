import wx

from geoi.actions.save_file import SaveFile

class SaveFileAs(SaveFile):
    """
    SaveFileAs: Save a Geoi file as
    """

    def __init__(self, win, param_mgr):
        SaveFile.__init__(self, win, param_mgr, "Save as..."
                        , 'Choose a filename then save a geoi file'
                        , wx.ART_FILE_SAVE_AS
                        , SaveAs = True)

    def run(self):
        self.runWithFilename(None)
