from geoi.actions import action

class Exit(action.Action):
    def __init__(self, win):
        action.Action.__init__(self, win, "exit"
                        , 'Get the heck outta here'
                        , accelerator = 'F10', iconId = 'wx.ART_IMAGES_' + 'exit')
        self.shell = None

    def run(self):
        self.getParent().Close()
