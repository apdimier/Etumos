# -*- coding: utf-8 -*-
"""
That file entails an object common to all other elmer classes.

"""

from elmertools import *

from exceptions import Exception


from generictools import memberShip

from listtools import toList

#from tools import *

from listtools import elimCommonElementsInList

import os

import string

from types import NoneType

from vector import V

class ElmerRoot:
    """
    Ground class, receptor of the commone methods for flow and transport elmer classes:
    
    elmer
    elmerhydro
    """
    def __init__(self, meshFileName="elmerMesh"):
        
#	print " debug ELMERROOT",
        self.meshFileName=meshFileName
#	print " debug ELMERROOT",
        #
        # the file is as string imported
        #
        if type(meshFileName) == "StringType" and meshFileName[-4:]  == ".msh":
#            print "toto"
#            raw_input()
	    self.meshFileName      = meshFileName
	    self.meshDirectoryName = self.meshFileName[0:-4]
        #
        # the file is as a mesh object imported
        #
	elif isInstance(meshFileName,CommonMesh):
	    self.meshFileName      = meshFileName.getName()
	    self.meshDirectoryName = self.meshFileName[0:-4]
	    
	else:
	    print " debug ELMERROOT"
	    
    def rawInput(self,arg):
        return raw_input("dbg"+self.__class__.__name__ +" "+str(arg))
        
    
