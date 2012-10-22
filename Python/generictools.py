"""
        That file contains generic coupling modules:

         D -> Darcy
         R -> Richards
        2P -> 2 phases
         C -> Chemistry
         M -> Mechanics

"""
from listtools import toList

from types import ListType

import resource

from sys import version_info

class Generic:
    """
    That class is only used as a generic container
    to provide help on class and associated methods to the user
    """
    def __init__(self):
        self.pyversion = version_info[0] + version_info[1]*0.1
        pass

    def getHelp(self,method = None):
        """
        Enables to get help on the class and on relevant methods:        
            a = class()
            getHelp(a.method)        
        """
        if method == None or type(method) != MethodType:
            print self.__doc__
        else:
            print method.__doc__
        pass
        
    def rawInput(self,arg):
        return raw_input("dbg"+self.__class__.__name__ +" "+str(arg))

class GenericModule(Generic):
    """
    That class is only used as a generic container for new modules
    
    Modules are supposed by default to be transient
    """
    def __init__(self) :
        """
        
        """
        Generic.__init__(self)
        
        self.spatialInteractiveOutputs = None 
        self.spatialSaveOutputs = None  
        self.vtkFileWriter = None
	self.vtkFrequency = None
	
        self.outputs = {}
        
        self.maxTimeStep = 1.e+15
        self.minTimeStep = 1.e-15
        
        self.simulatedTime = None
        self.timeStepNumber = None
        #
        self.debug = 0
        
    def cpuTime(self):
        """
        Used to determine the cpu time
        """
        return resource.getrusage(resource.RUSAGE_SELF)[0]

class GenericCTModule(GenericModule):
    """
    That class is only used as a generic container
    for new modules
    """
    def __init__(self) :
        """
        
        """
        GenericModule.__init__(self)
        self.dT = None
        self.dispersivityBody = None      
        self.effectiveDiffusionZone = None
    
        self.vtkFieldSpecies = None
        
        self.chemicalOutputs = []      
        self.chemicalOutputNames = {}
        self.chemicalOutputDict = {}

class GenericWD_CTModule(GenericModule):
    """
    That class is only used as a generic container
    enabling a transient one phase Darcy coupled to a chemical transport module.
    """
    def __init__(self) :
        """
        
        """
        GenericModule.__init__(self)


def listTypeCheck(liste, typ):
    if type(liste) != ListType:
        raise TypeError, " the supposed list is not of type list"
    if type(typ) != ListType:
        typ = [typ]
    for unb in liste:
        if type(unb) not in typ:
            print type(unb),typ
            raise TypeError, " the listed components are not all of the right type"
        pass
    return None
    
def checkClass(x, classes, message=None):
    """to check if x is not an instance of one of the classes list """
    try:
        if x.__class__ == classes.__class__:
            return
        pass
    except:
        pass
    if not isInstance(x, classes):
        if message is None:
            if hasattr(x, "__repr__"): xstr = x.__repr__()
            else: xstr = `type(x)`
            xstr = `type(x)`       
	raise TypeError, " x of type "+xstr+" is not within ["+_classesNameVerbose(classes)+"]"
    return

def checkClassList(liste, classes):
    """to check if elements of liste  are instances of classes list classes"""
    liste = list(liste)
    for x in liste: checkClass(x, classes)
    return None
    
def checkList(x, liste):
    """
    x should be an element of the liste list
    Raises an exception if x is not in liste.
    """
    if x not in liste :
        l = liste.__str__()
        raise Exception, x + " not in list argument "+ l
    pass
    
listCheck = checkList
    
def checkDict (x, dictionnary):
    """Raises an exception if an item is not a dictionnary key."""
    if x not in dictionary.keys() :
        raise "key " + `x` + " not included in given dictionary"

dictCheck = checkDict

def isInstance(x, klassenprobe):
    """Returns true if x is an instance of one of the classes within the testclasses, false otherwise"""
    if type(klassenprobe) is not ListType:
	    if isinstance(x, klassenprobe):
	        return 1
    else:
        for klasse in klassenprobe:
	    if isinstance(x, klasse):
	        return 1
            pass
    return 0
    
def memberShip(x,liste,message = None):
    if not isinstance(x,tuple(toList(liste))):
        if message == None: message = "of "+x.__class__.__name__
        print x
        raw_input("membership")
        raise Exception, "check instantiation %s %s"%(message, x)
        
def makeDict(**options):
    return options

makeDico = makeDict
        
def _classesNameVerbose(liste):
    """returns a string made of the different classes names within a list,
       so it supposes each element has __name__ as attribute.
    """ 
    liste = toList(liste)
    return (' '.join([elt.__name__ for elt in liste]))

def IS_NUMBER(x):
    try:
        x = float(x)
        return True
    except:
        return False

def SET_NUMBER(x):
    if IS_NUMBER(x):
        return x
    else: raise Exception, " is not a number" 
        
