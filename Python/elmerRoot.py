# -*- coding: utf-8 -*-
"""
That file entails an object common to all other elmer classes.

"""

from __future__ import absolute_import
from __future__ import print_function
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
from six.moves import input

class ElmerRoot:
    """
    Ground class, receptor of the common methods for mechanics, flow and transport elmer classes:
    
    elmer
    elmerhydro
    """
    def __init__(self, meshFileName="elmerMesh"):
        
        self.meshFileName=meshFileName
        #
        # the file is as string imported
        #
        if type(meshFileName) == "StringType" and meshFileName[-4:]  == ".msh":
            self.meshFileName      = meshFileName
            self.meshDirectoryName = self.meshFileName[0:-4]
            pass
        #
        # the file is as a mesh object imported
        #
        elif isInstance(meshFileName,CommonMesh):
            self.meshFileName      = meshFileName.getName()
            self.meshDirectoryName = self.meshFileName[0:-4]
            pass 
        else:
            print(" debug ELMERROOT")
            pass
        
    def rawInput(self,arg):
        return input("dbg"+self.__class__.__name__ +" "+str(arg))
        
    
