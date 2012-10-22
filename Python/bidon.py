#!/usr/bin/env python
class Generic:
    """
    That class is used to provide some standard functionnalities
    """
    def __init__(self):
        pass
    def getHelp(self,method = None):
        """
        Enables to get help on the class and on relevant methods:        
            a = class()
            getHelp(a.method)        
        """
        if method == None:
            print self.__doc__
        else:
            print method.__doc__
        pass

